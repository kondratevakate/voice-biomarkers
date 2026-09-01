#!/usr/bin/env python
"""Run formal multi-database searches for the voice biomarkers review.

No third-party dependencies. Saves raw API outputs and a deduplicated candidate CSV.
"""

from __future__ import annotations

import csv
import json
import os
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "sources" / "raw" / "formal"
RAW.mkdir(parents=True, exist_ok=True)

# Reproducibility controls (PRISMA-S: searches must be re-runnable).
# Relevance ranking is not stable over time and a single page silently truncates
# large result sets, so every source is sorted on a deterministic key and
# paginated. Truncation at MAX_RECORDS is reported, never silent.
PAGE_SIZE = 100
OPENALEX_PAGE_SIZE = 200
MAX_RECORDS = 8000
SORT_PUBMED = "pub_date"
SORT_EUROPE_PMC = "P_PDATE_D desc"
SORT_OPENALEX = "publication_date:desc"
SORT_ARXIV = "submittedDate"
FETCH_RETRIES = 4
# Identify the client to every API. OpenAlex and Crossref grant higher rate
# limits to requests carrying a contact address ("polite pool"), but an address
# is personal data sent to a third party, so it is opt-in via the environment
# and never hard-coded.
USER_AGENT = "voice-biomarkers-review/1.0 (systematic mapping review; +https://github.com/kondratevakate/voice-biomarkers)"
POLITE_MAILTO = os.environ.get("OPENALEX_MAILTO", "").strip()
FETCH_BACKOFF_SECONDS = 5


@dataclass(frozen=True)
class QueryFamily:
    key: str
    label: str
    plain: str
    pubmed: str
    arxiv: str
    dblp: str


# The disease clause is deliberately paired with an explicit voice-analysis
# construct. The previous single disease_monitoring family combined bare terms
# ("screening OR monitoring OR diagnosis") with a long disease list and matched
# 886,668 OpenAlex records against a 1,000-record retrieval ceiling, so it
# retrieved roughly 0.1 percent of its own result set. Requiring a named
# voice, speech, or acoustic construct restores a retrievable result set.
VOICE_ANALYSIS_PLAIN = (
    '"voice biomarker" OR "vocal biomarker" OR "speech biomarker" OR '
    '"acoustic biomarker" OR "voice-based digital biomarker" OR '
    '"speech-based digital biomarker" OR "voice analysis" OR '
    '"speech analysis" OR "acoustic analysis" OR "acoustic features" OR '
    '"speech features" OR "vocal features" OR "voice features"'
)

VOICE_ANALYSIS_PUBMED = (
    '("voice biomarker"[Title/Abstract] OR "vocal biomarker"[Title/Abstract] OR '
    '"speech biomarker"[Title/Abstract] OR "acoustic biomarker"[Title/Abstract] OR '
    '"voice-based digital biomarker"[Title/Abstract] OR '
    '"speech-based digital biomarker"[Title/Abstract] OR "voice analysis"[Title/Abstract] OR '
    '"speech analysis"[Title/Abstract] OR "acoustic analysis"[Title/Abstract] OR '
    '"acoustic features"[Title/Abstract] OR "speech features"[Title/Abstract] OR '
    '"vocal features"[Title/Abstract] OR "voice features"[Title/Abstract])'
)

VOICE_ANALYSIS_ARXIV = (
    'abs:"voice biomarker" OR abs:"vocal biomarker" OR abs:"speech biomarker" OR '
    'abs:"acoustic biomarker" OR abs:"voice-based digital biomarker" OR '
    'abs:"speech-based digital biomarker" OR abs:"speech analysis" OR '
    'abs:"acoustic features" OR abs:"pathological speech"'
)


def _disease_family(
    key: str, label: str, plain_terms: str, pubmed_terms: str, arxiv_terms: str, dblp: str
) -> "QueryFamily":
    """Build a disease subfamily as (voice-analysis construct) AND (disease terms)."""
    return QueryFamily(
        key,
        label,
        f"({VOICE_ANALYSIS_PLAIN}) AND ({plain_terms})",
        f"{VOICE_ANALYSIS_PUBMED} AND ({pubmed_terms})",
        f"({VOICE_ANALYSIS_ARXIV}) AND ({arxiv_terms})",
        dblp,
    )


FAMILIES = [
    QueryFamily(
        "core_terminology",
        "Core terminology",
        '"voice biomarker" OR "vocal biomarker" OR "speech biomarker" OR '
        '"speech-based digital biomarker" OR "voice-derived digital biomarker" OR '
        '"speech-derived digital biomarker"',
        '("voice biomarker"[Title/Abstract] OR "vocal biomarker"[Title/Abstract] OR '
        '"speech biomarker"[Title/Abstract] OR "speech-based digital biomarker"[Title/Abstract] OR '
        '"voice-derived digital biomarker"[Title/Abstract] OR "speech-derived digital biomarker"[Title/Abstract])',
        'abs:"voice biomarker" OR abs:"vocal biomarker" OR abs:"speech biomarker" OR '
        'abs:"speech-based digital biomarker" OR abs:"voice-derived digital biomarker" OR '
        'abs:"speech-derived digital biomarker"',
        "speech|voice|vocal|acoustic biomarker",
    ),
    QueryFamily(
        "clinical_validation",
        "Clinical validation",
        '(voice OR vocal OR speech OR acoustic) AND ("digital biomarker" OR biomarker OR '
        '"digital phenotype") AND ("clinical validation" OR "analytical validation" OR '
        '"external validation" OR "longitudinal validation" OR "clinical utility")',
        '(voice[Title/Abstract] OR vocal[Title/Abstract] OR speech[Title/Abstract] OR acoustic[Title/Abstract]) '
        'AND (biomarker[Title/Abstract] OR "digital biomarker"[Title/Abstract] OR '
        '"digital phenotype"[Title/Abstract]) AND ("clinical validation"[Title/Abstract] OR '
        '"analytical validation"[Title/Abstract] OR "external validation"[Title/Abstract] OR '
        '"longitudinal validation"[Title/Abstract] OR "clinical utility"[Title/Abstract])',
        '(abs:"digital biomarker" OR abs:"digital phenotype" OR abs:"voice biomarker" OR '
        'abs:"speech biomarker" OR abs:"acoustic biomarker") AND (abs:"clinical validation" OR '
        'abs:"analytical validation" OR abs:"external validation" OR abs:"clinical utility")',
        "speech|voice|vocal|acoustic biomarker validation|generalization",
    ),
    QueryFamily(
        "aging_biological_age",
        "Aging and biological age",
        '"voice age" OR "vocal aging" OR "speech aging" OR "voice-based biological clock" OR '
        '"voice-predicted age" OR "vocal age acceleration"',
        '("voice age"[Title/Abstract] OR "vocal aging"[Title/Abstract] OR '
        '"speech aging"[Title/Abstract] OR "voice-based biological clock"[Title/Abstract] OR '
        '"voice-predicted age"[Title/Abstract] OR "vocal age acceleration"[Title/Abstract])',
        'abs:"vocal aging" OR abs:"voice aging" OR abs:"speech aging" OR '
        'abs:"voice-based biological clock" OR abs:"speaker age estimation" OR '
        'abs:"age estimation from speech" OR abs:"age estimation from voice"',
        "speaker|voice|speech age|aging estimation|prediction|recognition",
    ),
    _disease_family(
        "disease_neuro",
        "Neurological and cognitive disease",
        'Parkinson OR Alzheimer OR dementia OR "mild cognitive impairment" OR '
        '"cognitive decline" OR ALS OR "motor neuron disease" OR Huntington OR '
        '"multiple sclerosis" OR aphasia OR dysarthria OR apraxia',
        'Parkinson*[Title/Abstract] OR Alzheimer*[Title/Abstract] OR dementia[Title/Abstract] OR '
        '"mild cognitive impairment"[Title/Abstract] OR "cognitive decline"[Title/Abstract] OR '
        'ALS[Title/Abstract] OR "motor neuron disease"[Title/Abstract] OR Huntington*[Title/Abstract] OR '
        '"multiple sclerosis"[Title/Abstract] OR aphasia[Title/Abstract] OR dysarthria[Title/Abstract] OR '
        'apraxia[Title/Abstract]',
        'abs:Parkinson OR abs:Alzheimer OR abs:dementia OR abs:"cognitive impairment" OR '
        'abs:ALS OR abs:aphasia OR abs:dysarthria',
        "speech|voice|acoustic Parkinson|Alzheimer|dementia|aphasia|dysarthria",
    ),
    _disease_family(
        "disease_psych",
        "Mental health and affective state",
        'depression OR "depressive disorder" OR anxiety OR schizophrenia OR psychosis OR '
        'bipolar OR suicidality OR "post-traumatic stress" OR "mental health"',
        'depression[Title/Abstract] OR "depressive disorder"[Title/Abstract] OR anxiety[Title/Abstract] OR '
        'schizophrenia[Title/Abstract] OR psychosis[Title/Abstract] OR bipolar[Title/Abstract] OR '
        'suicidal*[Title/Abstract] OR "post-traumatic stress"[Title/Abstract] OR "mental health"[Title/Abstract]',
        'abs:depression OR abs:anxiety OR abs:schizophrenia OR abs:psychosis OR '
        'abs:bipolar OR abs:"mental health"',
        "speech|voice|acoustic depression|schizophrenia|psychosis|bipolar|suicidality",
    ),
    _disease_family(
        "disease_respiratory",
        "Respiratory and laryngeal disease",
        'asthma OR COPD OR "chronic obstructive pulmonary" OR respiratory OR cough OR '
        'dyspnea OR COVID OR "pulmonary hypertension" OR laryngeal OR dysphonia OR '
        '"voice disorder" OR "vocal fold" OR "head and neck cancer"',
        'asthma[Title/Abstract] OR COPD[Title/Abstract] OR "chronic obstructive pulmonary"[Title/Abstract] OR '
        'respiratory[Title/Abstract] OR cough[Title/Abstract] OR dyspnea[Title/Abstract] OR '
        'COVID*[Title/Abstract] OR "pulmonary hypertension"[Title/Abstract] OR laryngeal[Title/Abstract] OR '
        'dysphonia[Title/Abstract] OR "voice disorder"[Title/Abstract] OR "vocal fold"[Title/Abstract] OR '
        '"head and neck cancer"[Title/Abstract]',
        'abs:asthma OR abs:COPD OR abs:respiratory OR abs:cough OR abs:COVID OR '
        'abs:dysphonia OR abs:"voice disorder"',
        "speech|voice|vocal|cough asthma|COPD|respiratory|dysphonia|laryngeal",
    ),
    _disease_family(
        "disease_cardiometabolic",
        "Cardiovascular, metabolic, and frailty",
        '"heart failure" OR "coronary artery" OR cardiovascular OR cardiometabolic OR '
        'diabetes OR obesity OR adiposity OR frailty OR sarcopenia OR "sleep apnea"',
        '"heart failure"[Title/Abstract] OR "coronary artery"[Title/Abstract] OR '
        'cardiovascular[Title/Abstract] OR cardiometabolic[Title/Abstract] OR diabetes[Title/Abstract] OR '
        'obesity[Title/Abstract] OR adiposity[Title/Abstract] OR frailty[Title/Abstract] OR '
        'sarcopenia[Title/Abstract] OR "sleep apnea"[Title/Abstract]',
        'abs:"heart failure" OR abs:cardiovascular OR abs:diabetes OR abs:frailty OR '
        'abs:"sleep apnea"',
        "speech|voice|vocal|acoustic cardiac|cardiovascular|diabetes|frailty|apnea",
    ),
    QueryFamily(
        "datasets_foundation_models",
        "Tasks, datasets, and foundation models",
        '"clinical voice" OR "health voice" OR "medical speech" OR "speech health" OR '
        '"voice foundation model" OR "speech foundation model"',
        '("clinical voice"[Title/Abstract] OR "health voice"[Title/Abstract] OR '
        '"medical speech"[Title/Abstract] OR "speech health"[Title/Abstract] OR '
        '"voice foundation model"[Title/Abstract] OR "speech foundation model"[Title/Abstract])',
        'abs:"speech foundation model" OR abs:"voice foundation model" OR abs:"clinical speech" OR '
        'abs:"medical speech" OR abs:"pathological speech" OR abs:"health speech dataset"',
        "speech|voice corpus|dataset|benchmark clinical|medical|pathological|health",
    ),
]


def _fetch(url: str, errors: str) -> str:
    """Fetch with bounded retries.

    A single transient DNS or rate-limit failure used to abort a whole
    query family, which silently changed what the search covered. Retry a
    fixed number of times with linear backoff, then let the caller record
    the failure in the counts CSV.
    """
    last: Exception | None = None
    for attempt in range(FETCH_RETRIES):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read().decode("utf-8", errors=errors)
        except Exception as exc:  # noqa: BLE001 - retried, then reported
            last = exc
            if attempt < FETCH_RETRIES - 1:
                time.sleep(FETCH_BACKOFF_SECONDS * (attempt + 1))
    raise last  # type: ignore[misc]


def fetch_json(url: str, out: Path) -> dict[str, Any]:
    text = _fetch(url, "strict")
    out.write_text(text, encoding="utf-8")
    return json.loads(text)


def fetch_text(url: str, out: Path) -> str:
    text = _fetch(url, "replace")
    out.write_text(text, encoding="utf-8")
    return text


def normalize_title(title: str) -> str:
    return re.sub(r"\W+", " ", title.lower()).strip()


def add_candidate(candidates: list[dict[str, Any]], **row: Any) -> None:
    title = (row.get("title") or "").strip()
    if not title:
        return
    row["title_key"] = normalize_title(title)
    candidates.append(row)


def europe_pmc_title_abs(query: str) -> str:
    """Scope a plain query to Europe PMC's title and abstract fields.

    Europe PMC searches full text by default, while the PubMed queries are
    scoped with [Title/Abstract] and the OpenAlex queries use the
    title_and_abstract filter. Without this transform the three sources answer
    different questions and their counts are not comparable. Every quoted
    phrase and every bare search term is prefixed with TITLE_ABS:, leaving
    boolean operators and parentheses untouched.
    """
    out: list[str] = []
    index = 0
    token = re.compile(r'"[^"]*"|[A-Za-z][A-Za-z0-9*\-]*')
    while index < len(query):
        match = token.search(query, index)
        if not match:
            out.append(query[index:])
            break
        out.append(query[index : match.start()])
        text = match.group(0)
        if text.upper() in {"AND", "OR", "NOT"}:
            out.append(text)
        else:
            out.append(f"TITLE_ABS:{text}")
        index = match.end()
    return "".join(out)


def run_pubmed(family: QueryFamily, candidates: list[dict[str, Any]]) -> tuple[int, bool]:
    term = f"({family.pubmed}) AND (Humans[MeSH Terms] OR human[Title/Abstract] OR clinical[Title/Abstract] OR health[Title/Abstract] OR disease[Title/Abstract] OR aging[Title/Abstract])"
    ids: list[str] = []
    count = 0
    for page, retstart in enumerate(range(0, MAX_RECORDS, PAGE_SIZE)):
        params = {
            "db": "pubmed",
            "retmode": "json",
            "retmax": str(PAGE_SIZE),
            "retstart": str(retstart),
            "sort": SORT_PUBMED,
            "term": term,
        }
        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + urllib.parse.urlencode(params)
        esearch = fetch_json(url, RAW / f"pubmed_{family.key}_esearch_p{page:02d}.json")
        result = esearch.get("esearchresult", {})
        count = int(result.get("count", 0))
        page_ids = result.get("idlist", [])
        ids.extend(page_ids)
        if len(page_ids) < PAGE_SIZE or len(ids) >= count:
            break
        time.sleep(0.4)
    for chunk, start in enumerate(range(0, len(ids), PAGE_SIZE)):
        batch = ids[start : start + PAGE_SIZE]
        params = {"db": "pubmed", "retmode": "json", "id": ",".join(batch)}
        summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?" + urllib.parse.urlencode(params)
        summary = fetch_json(summary_url, RAW / f"pubmed_{family.key}_esummary_p{chunk:02d}.json")
        for uid in summary.get("result", {}).get("uids", []):
            item = summary["result"][uid]
            add_candidate(
                candidates,
                source="PubMed",
                query_family=family.key,
                id=f"PMID:{uid}",
                year=(item.get("pubdate") or "")[:4],
                title=item.get("title", ""),
                venue=item.get("fulljournalname", ""),
                doi="",
                url=f"https://pubmed.ncbi.nlm.nih.gov/{uid}/",
            )
        time.sleep(0.4)
    return count, count > len(ids)


def run_europe_pmc(
    family: QueryFamily, candidates: list[dict[str, Any]], preprints_only: bool
) -> tuple[int, bool]:
    query = f"({europe_pmc_title_abs(family.plain)})"
    if preprints_only:
        query = f"({query}) AND SRC:PPR"
    tag = "preprints" if preprints_only else "all"
    cursor = "*"
    retrieved = 0
    count = 0
    for page in range(MAX_RECORDS // PAGE_SIZE):
        params = {
            "query": query,
            "format": "json",
            "pageSize": str(PAGE_SIZE),
            "resultType": "core",
            "sort": SORT_EUROPE_PMC,
            "cursorMark": cursor,
        }
        url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urllib.parse.urlencode(params)
        data = fetch_json(url, RAW / f"europepmc_{tag}_{family.key}_p{page:02d}.json")
        count = int(data.get("hitCount", 0))
        results = data.get("resultList", {}).get("result", [])
        for item in results:
            add_candidate(
                candidates,
                source="EuropePMC-PPR" if preprints_only else "EuropePMC",
                query_family=family.key,
                id=item.get("id", ""),
                year=item.get("pubYear", ""),
                title=item.get("title", ""),
                venue=item.get("journalTitle", item.get("source", "")),
                doi=item.get("doi", ""),
                url=item.get("doiUrl")
                or item.get("fullTextUrlList", {}).get("fullTextUrl", [{}])[0].get("url", ""),
            )
        retrieved += len(results)
        next_cursor = data.get("nextCursorMark")
        if not results or not next_cursor or next_cursor == cursor or retrieved >= count:
            break
        cursor = next_cursor
        time.sleep(0.4)
    return count, count > retrieved


def run_openalex(family: QueryFamily, candidates: list[dict[str, Any]]) -> tuple[int, bool]:
    cursor = "*"
    retrieved = 0
    count = 0
    for page in range(MAX_RECORDS // OPENALEX_PAGE_SIZE + 1):
        # The bare "search" parameter runs a relevance search over full text
        # and treats the query largely as a bag of words: it returned 38,473
        # records for "voice biomarker" against 232 for the scoped filter.
        # title_and_abstract.search honours quoted phrases and booleans and
        # matches the field scope used for PubMed and Europe PMC.
        params = {
            "filter": f"title_and_abstract.search:{family.plain}",
            "per-page": str(OPENALEX_PAGE_SIZE),
            "sort": SORT_OPENALEX,
            "cursor": cursor,
        }
        if POLITE_MAILTO:
            params["mailto"] = POLITE_MAILTO
        url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
        data = fetch_json(url, RAW / f"openalex_{family.key}_p{page:02d}.json")
        meta = data.get("meta", {})
        count = int(meta.get("count", 0))
        results = data.get("results", [])
        for item in results:
            primary = item.get("primary_location") or {}
            source = primary.get("source") or {}
            add_candidate(
                candidates,
                source="OpenAlex",
                query_family=family.key,
                id=item.get("id", ""),
                year=item.get("publication_year", ""),
                title=item.get("display_name", ""),
                venue=source.get("display_name", ""),
                doi=item.get("doi", ""),
                url=item.get("doi") or item.get("id", ""),
                cited_by_count=item.get("cited_by_count", ""),
            )
        retrieved += len(results)
        next_cursor = meta.get("next_cursor")
        if not results or not next_cursor or retrieved >= count:
            break
        cursor = next_cursor
        time.sleep(0.4)
    return count, count > retrieved


def run_arxiv(family: QueryFamily, candidates: list[dict[str, Any]]) -> tuple[int, bool]:
    query = family.arxiv
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    retrieved = 0
    total = 0
    for page, start in enumerate(range(0, MAX_RECORDS, PAGE_SIZE)):
        params = {
            "search_query": query,
            "start": str(start),
            "max_results": str(PAGE_SIZE),
            "sortBy": SORT_ARXIV,
            "sortOrder": "descending",
        }
        url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
        text = fetch_text(url, RAW / f"arxiv_{family.key}_p{page:02d}.xml")
        if text.lstrip().startswith("<!DOCTYPE html>") or "<feed" not in text:
            return retrieved, False
        root = ET.fromstring(text)
        total_text = root.findtext("{http://a9.com/-/spec/opensearch/1.1/}totalResults", "0")
        total = int(total_text or 0)
        entries = root.findall("atom:entry", ns)
        for entry in entries:
            title = " ".join((entry.findtext("atom:title", "", ns) or "").split())
            published = entry.findtext("atom:published", "", ns)
            link = entry.findtext("atom:id", "", ns)
            add_candidate(
                candidates,
                source="arXiv",
                query_family=family.key,
                id=link.rsplit("/", 1)[-1],
                year=published[:4],
                title=title,
                venue="arXiv",
                doi="",
                url=link,
            )
        retrieved += len(entries)
        if len(entries) < PAGE_SIZE or retrieved >= total:
            break
        time.sleep(3.2)
    return total or retrieved, bool(total) and total > retrieved


def run_dblp(family: QueryFamily, candidates: list[dict[str, Any]]) -> tuple[int, bool]:
    """Search DBLP, the free bibliographic index for computer science venues.

    IEEE Xplore, the ACM Digital Library, the ACL Anthology, and the ISCA
    Archive all require subscriptions or offer no usable search API. DBLP
    indexes their metadata (ICASSP, Interspeech, ACL, ACM conferences and the
    speech journals) and is free, so it serves as the engineering-index layer
    that biomedical databases do not cover. It is a metadata index: it carries
    no abstracts, so records retrieved here need title-level screening and a
    separate metadata lookup before extraction.

    DBLP exposes no sort parameter, so retrieval order is not guaranteed
    stable. The queries are scoped to return complete result sets well under
    MAX_RECORDS, which makes ordering irrelevant to reproducibility; a
    truncated DBLP family would not be reproducible and is reported as such.
    """
    retrieved = 0
    total = 0
    for page, first in enumerate(range(0, MAX_RECORDS, PAGE_SIZE)):
        params = {
            "q": family.dblp,
            "format": "json",
            "h": str(PAGE_SIZE),
            "f": str(first),
        }
        url = "https://dblp.org/search/publ/api?" + urllib.parse.urlencode(params)
        data = fetch_json(url, RAW / f"dblp_{family.key}_p{page:02d}.json")
        hits = data.get("result", {}).get("hits", {})
        total = int(hits.get("@total", 0) or 0)
        records = hits.get("hit", []) or []
        for record in records:
            info = record.get("info", {}) or {}
            venue = info.get("venue", "")
            if isinstance(venue, list):
                venue = "; ".join(str(v) for v in venue)
            add_candidate(
                candidates,
                source="DBLP",
                query_family=family.key,
                id=info.get("key", ""),
                year=info.get("year", ""),
                title=(info.get("title", "") or "").replace("&apos;", "'"),
                venue=venue,
                doi=(info.get("doi", "") or ""),
                url=info.get("ee") or info.get("url", ""),
            )
        retrieved += len(records)
        if len(records) < PAGE_SIZE or retrieved >= total:
            break
        time.sleep(0.6)
    return total, total > retrieved


def dedupe(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    deduped: list[dict[str, Any]] = []
    for row in candidates:
        doi = (row.get("doi") or "").lower().replace("https://doi.org/", "").strip()
        key = doi or row.get("title_key") or ""
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    return deduped


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    fieldnames = [
        "source",
        "query_family",
        "id",
        "year",
        "title",
        "venue",
        "doi",
        "url",
        "cited_by_count",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    candidates: list[dict[str, Any]] = []
    counts: list[dict[str, Any]] = []
    for family in FAMILIES:
        print(f"Running {family.key}")
        for source, fn in [
            ("PubMed", lambda: run_pubmed(family, candidates)),
            ("EuropePMC", lambda: run_europe_pmc(family, candidates, False)),
            ("EuropePMC-PPR", lambda: run_europe_pmc(family, candidates, True)),
            ("OpenAlex", lambda: run_openalex(family, candidates)),
            ("arXiv", lambda: run_arxiv(family, candidates)),
            ("DBLP", lambda: run_dblp(family, candidates)),
        ]:
            try:
                count, truncated = fn()
                status = "ok_truncated_at_max_records" if truncated else "ok"
                counts.append(
                    {"source": source, "query_family": family.key, "count": count, "status": status}
                )
                print(f"  {source}: {count}{' (truncated)' if truncated else ''}")
            except Exception as exc:  # noqa: BLE001
                counts.append(
                    {
                        "source": source,
                        "query_family": family.key,
                        "count": "",
                        "status": f"error: {type(exc).__name__}: {exc}",
                    }
                )
                print(f"  {source}: error {exc}")
            if source == "arXiv":
                time.sleep(3.2)
    deduped = dedupe(candidates)
    write_csv(deduped, ROOT / "sources" / "formal-candidates.csv")
    with (ROOT / "sources" / "formal-search-counts.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "query_family", "count", "status"])
        writer.writeheader()
        writer.writerows(counts)
    print(f"Candidates: {len(candidates)} raw, {len(deduped)} deduplicated")


if __name__ == "__main__":
    main()

