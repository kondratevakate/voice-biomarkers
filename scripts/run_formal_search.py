#!/usr/bin/env python
"""Run formal multi-database searches for the voice biomarkers review.

No third-party dependencies. Saves raw API outputs and a deduplicated candidate CSV.
"""

from __future__ import annotations

import csv
import json
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


@dataclass(frozen=True)
class QueryFamily:
    key: str
    label: str
    plain: str
    pubmed: str


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
    ),
    QueryFamily(
        "aging_biological_age",
        "Aging and biological age",
        '"voice age" OR "vocal aging" OR "speech aging" OR "voice-based biological clock" OR '
        '"voice-predicted age" OR "vocal age acceleration"',
        '("voice age"[Title/Abstract] OR "vocal aging"[Title/Abstract] OR '
        '"speech aging"[Title/Abstract] OR "voice-based biological clock"[Title/Abstract] OR '
        '"voice-predicted age"[Title/Abstract] OR "vocal age acceleration"[Title/Abstract])',
    ),
    QueryFamily(
        "disease_monitoring",
        "Disease detection and monitoring",
        '(voice OR vocal OR speech OR acoustic) AND (biomarker OR "digital biomarker" OR '
        'screening OR monitoring OR diagnosis OR prognosis OR severity) AND '
        '(Parkinson OR Alzheimer OR dementia OR depression OR anxiety OR schizophrenia OR '
        '"heart failure" OR asthma OR COPD OR respiratory OR ALS OR "motor neuron disease" OR '
        'frailty OR cardiometabolic)',
        '(voice[Title/Abstract] OR vocal[Title/Abstract] OR speech[Title/Abstract] OR acoustic[Title/Abstract]) '
        'AND (biomarker[Title/Abstract] OR "digital biomarker"[Title/Abstract] OR '
        'screening[Title/Abstract] OR monitoring[Title/Abstract] OR diagnosis[Title/Abstract] OR '
        'prognosis[Title/Abstract] OR severity[Title/Abstract]) AND '
        '(Parkinson*[Title/Abstract] OR Alzheimer*[Title/Abstract] OR dementia[Title/Abstract] OR '
        'depression[Title/Abstract] OR anxiety[Title/Abstract] OR schizophrenia[Title/Abstract] OR '
        '"heart failure"[Title/Abstract] OR asthma[Title/Abstract] OR COPD[Title/Abstract] OR '
        'respiratory[Title/Abstract] OR ALS[Title/Abstract] OR "motor neuron disease"[Title/Abstract] OR '
        'frailty[Title/Abstract] OR cardiometabolic[Title/Abstract])',
    ),
    QueryFamily(
        "datasets_foundation_models",
        "Tasks, datasets, and foundation models",
        '"clinical voice" OR "health voice" OR "medical speech" OR "speech health" OR '
        '"voice foundation model" OR "speech foundation model"',
        '("clinical voice"[Title/Abstract] OR "health voice"[Title/Abstract] OR '
        '"medical speech"[Title/Abstract] OR "speech health"[Title/Abstract] OR '
        '"voice foundation model"[Title/Abstract] OR "speech foundation model"[Title/Abstract])',
    ),
]


def fetch_json(url: str, out: Path) -> dict[str, Any]:
    with urllib.request.urlopen(url, timeout=60) as response:
        text = response.read().decode("utf-8")
    out.write_text(text, encoding="utf-8")
    return json.loads(text)


def fetch_text(url: str, out: Path) -> str:
    with urllib.request.urlopen(url, timeout=60) as response:
        text = response.read().decode("utf-8", errors="replace")
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


def run_pubmed(family: QueryFamily, candidates: list[dict[str, Any]]) -> int:
    term = f"({family.pubmed}) AND (Humans[MeSH Terms] OR human[Title/Abstract] OR clinical[Title/Abstract] OR health[Title/Abstract] OR disease[Title/Abstract] OR aging[Title/Abstract])"
    params = {
        "db": "pubmed",
        "retmode": "json",
        "retmax": "100",
        "sort": "relevance",
        "term": term,
    }
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + urllib.parse.urlencode(params)
    esearch = fetch_json(url, RAW / f"pubmed_{family.key}_esearch.json")
    ids = esearch.get("esearchresult", {}).get("idlist", [])
    count = int(esearch.get("esearchresult", {}).get("count", 0))
    if not ids:
        return count
    params = {"db": "pubmed", "retmode": "json", "id": ",".join(ids)}
    summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?" + urllib.parse.urlencode(params)
    summary = fetch_json(summary_url, RAW / f"pubmed_{family.key}_esummary.json")
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
    return count


def run_europe_pmc(family: QueryFamily, candidates: list[dict[str, Any]], preprints_only: bool) -> int:
    query = f"({family.plain})"
    if preprints_only:
        query = f"({query}) AND SRC:PPR"
    params = {"query": query, "format": "json", "pageSize": "100", "resultType": "core"}
    tag = "preprints" if preprints_only else "all"
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urllib.parse.urlencode(params)
    data = fetch_json(url, RAW / f"europepmc_{tag}_{family.key}.json")
    count = int(data.get("hitCount", 0))
    for item in data.get("resultList", {}).get("result", []):
        add_candidate(
            candidates,
            source="EuropePMC-PPR" if preprints_only else "EuropePMC",
            query_family=family.key,
            id=item.get("id", ""),
            year=item.get("pubYear", ""),
            title=item.get("title", ""),
            venue=item.get("journalTitle", item.get("source", "")),
            doi=item.get("doi", ""),
            url=item.get("doiUrl") or item.get("fullTextUrlList", {}).get("fullTextUrl", [{}])[0].get("url", ""),
        )
    return count


def run_openalex(family: QueryFamily, candidates: list[dict[str, Any]]) -> int:
    params = {"search": family.plain, "per-page": "100", "sort": "relevance_score:desc"}
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
    data = fetch_json(url, RAW / f"openalex_{family.key}.json")
    count = int(data.get("meta", {}).get("count", 0))
    for item in data.get("results", []):
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
    return count


def run_arxiv(family: QueryFamily, candidates: list[dict[str, Any]]) -> int:
    query = f'all:"{family.label}" OR all:"{family.plain[:80]}"'
    params = {
        "search_query": query,
        "start": "0",
        "max_results": "50",
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
    text = fetch_text(url, RAW / f"arxiv_{family.key}.xml")
    if text.lstrip().startswith("<!DOCTYPE html>") or "<feed" not in text:
        return 0
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(text)
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
    return len(entries)


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
        ]:
            try:
                count = fn()
                counts.append({"source": source, "query_family": family.key, "count": count, "status": "ok"})
                print(f"  {source}: {count}")
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

