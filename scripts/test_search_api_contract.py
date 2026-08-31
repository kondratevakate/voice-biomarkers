#!/usr/bin/env python
"""Contract tests for the deterministic-search parameters in run_formal_search.py.

Relevance ranking is not stable over time, so the formal search sorts every
source on a deterministic key and paginates instead of truncating. Those sort
keys and pagination tokens are external API contracts: if a provider renames or
drops one, the search silently falls back to its default ordering and the review
stops being reproducible.

Run before committing any change to the search script:

    python scripts/test_search_api_contract.py

Network access is required. Failures are reported per source; the script exits
non-zero if any contract is broken.
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.parse
import time
import urllib.request
import xml.etree.ElementTree as ET

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))

from run_formal_search import (  # noqa: E402
    FAMILIES,
    POLITE_MAILTO,
    USER_AGENT,
    PAGE_SIZE,
    SORT_ARXIV,
    SORT_EUROPE_PMC,
    SORT_OPENALEX,
    SORT_PUBMED,
)

ARXIV_SANE_MAX_HITS = 100_000
RETRIES = 4
BACKOFF_SECONDS = 6
UA = {"User-Agent": USER_AGENT}
PROBE = "voice biomarker"


def get(url: str) -> bytes:
    """Fetch with retries so a transient DNS blip or rate limit cannot fail the gate."""
    last: Exception | None = None
    for attempt in range(RETRIES):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as response:
                return response.read()
        except Exception as exc:  # noqa: BLE001 - retried, then reported
            last = exc
            if attempt < RETRIES - 1:
                time.sleep(BACKOFF_SECONDS * (attempt + 1))
    raise last  # type: ignore[misc]


def check_pubmed() -> None:
    params = {
        "db": "pubmed",
        "retmode": "json",
        "retmax": "5",
        "retstart": "0",
        "sort": SORT_PUBMED,
        "term": PROBE,
    }
    data = json.loads(get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + urllib.parse.urlencode(params)))
    result = data["esearchresult"]
    assert "ERROR" not in result, f"PubMed rejected sort={SORT_PUBMED}: {result.get('ERROR')}"
    assert result.get("idlist"), "PubMed returned no ids"
    # retstart must actually shift the window, otherwise pagination is a no-op.
    params["retstart"] = "5"
    shifted = json.loads(get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + urllib.parse.urlencode(params)))
    assert shifted["esearchresult"]["idlist"] != result["idlist"], "PubMed retstart did not paginate"


def check_europe_pmc() -> None:
    params = {
        "query": PROBE,
        "format": "json",
        "pageSize": "5",
        "resultType": "core",
        "sort": SORT_EUROPE_PMC,
        "cursorMark": "*",
    }
    data = json.loads(get("https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urllib.parse.urlencode(params)))
    results = data.get("resultList", {}).get("result", [])
    assert results, f"Europe PMC returned no results for sort={SORT_EUROPE_PMC}"
    assert data.get("nextCursorMark"), "Europe PMC did not return nextCursorMark"
    years = [int(r["pubYear"]) for r in results if r.get("pubYear", "").isdigit()]
    assert years == sorted(years, reverse=True), f"Europe PMC not sorted descending by date: {years}"


def check_openalex() -> None:
    params = {"search": PROBE, "per-page": "5", "sort": SORT_OPENALEX, "cursor": "*"}
    if POLITE_MAILTO:
        params["mailto"] = POLITE_MAILTO
    data = json.loads(get("https://api.openalex.org/works?" + urllib.parse.urlencode(params)))
    results = data.get("results", [])
    assert results, f"OpenAlex returned no results for sort={SORT_OPENALEX}"
    assert data.get("meta", {}).get("next_cursor"), "OpenAlex did not return next_cursor"
    dates = [r["publication_date"] for r in results if r.get("publication_date")]
    assert dates == sorted(dates, reverse=True), f"OpenAlex not sorted descending by date: {dates}"


def check_arxiv() -> None:
    params = {
        "search_query": 'all:"voice biomarker"',
        "start": "0",
        "max_results": "5",
        "sortBy": SORT_ARXIV,
        "sortOrder": "descending",
    }
    text = get("https://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)).decode("utf-8", "replace")
    assert "<feed" in text, "arXiv did not return an Atom feed (API error or rate limit)"
    root = ET.fromstring(text)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    published = [e.findtext("atom:published", "", ns) for e in root.findall("atom:entry", ns)]
    assert published, f"arXiv returned no entries for sortBy={SORT_ARXIV}"
    assert published == sorted(published, reverse=True), f"arXiv not sorted descending: {published}"


def check_arxiv_queries_are_topical() -> None:
    """Regression test for a malformed arXiv query.

    The arXiv query used to be assembled from the family label and an
    80-character slice of the generic query string. That produced unbalanced
    quotes, so arXiv parsed it as a disjunction of bare words and matched its
    entire corpus (3.1 million records), pulling ~2000 unrelated physics and
    mathematics papers into the candidate pool. Each family now carries a
    hand-written arXiv query. Assert both that the result set is plausibly
    scoped and that returned titles are actually about speech or voice.
    """
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    topical = ("voice", "vocal", "speech", "acoustic", "audio", "speaker", "dysarthr", "phon")
    for family in FAMILIES:
        params = {
            "search_query": family.arxiv,
            "start": "0",
            "max_results": "20",
            "sortBy": SORT_ARXIV,
            "sortOrder": "descending",
        }
        text = get("https://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)).decode("utf-8", "replace")
        assert "<feed" in text, f"arXiv returned no feed for {family.key}"
        root = ET.fromstring(text)
        total = int(root.findtext("{http://a9.com/-/spec/opensearch/1.1/}totalResults", "0") or 0)
        assert total < ARXIV_SANE_MAX_HITS, (
            f"arXiv query for {family.key} matched {total} records, at or above the "
            f"{ARXIV_SANE_MAX_HITS} sanity bound - the query is almost certainly malformed"
        )
        # The queries target abs:, so judge topicality on the abstract, not the
        # title: a legitimately retrieved paper may not carry "speech" in its title.
        entries = root.findall("atom:entry", ns)
        assert entries, f"arXiv returned no entries for {family.key}"
        abstracts = [" ".join((e.findtext("atom:summary", "", ns) or "").split()).lower() for e in entries]
        on_topic = sum(any(t in a for t in topical) for a in abstracts)
        assert on_topic >= (len(abstracts) * 3) // 4, (
            f"arXiv results for {family.key} are off-topic: only {on_topic} of {len(abstracts)} "
            f"abstracts mention voice, speech, or audio"
        )
        time.sleep(3.2)


def main() -> int:
    assert PAGE_SIZE > 0, "PAGE_SIZE must be positive"
    failures = []
    for name, check in [
        ("PubMed", check_pubmed),
        ("Europe PMC", check_europe_pmc),
        ("OpenAlex", check_openalex),
        ("arXiv", check_arxiv),
        ("arXiv query scope", check_arxiv_queries_are_topical),
    ]:
        try:
            check()
            print(f"PASS {name}")
        except (AssertionError, urllib.error.URLError, KeyError, ValueError) as exc:
            failures.append((name, exc))
            print(f"FAIL {name}: {type(exc).__name__}: {exc}")
    if failures:
        print(f"\n{len(failures)} of 5 source contracts broken - do not trust the search until fixed.")
        return 1
    print("\nAll 5 source contracts hold; the formal search is deterministic and paginates.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
