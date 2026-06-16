#!/usr/bin/env python
"""Fetch PubMed abstracts for the first screening packet and add abstract decisions."""

from __future__ import annotations

import csv
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCREENING = ROOT / "screening"
RAW = ROOT / "sources" / "raw" / "formal"


EMPIRICAL_HINTS = [
    "participants",
    "patients",
    "cohort",
    "study",
    "model",
    "machine learning",
    "validation",
    "prospective",
    "retrospective",
    "auc",
    "auroc",
    "sensitivity",
    "specificity",
    "correlation",
]

BACKGROUND_HINTS = [
    "systematic review",
    "narrative review",
    "review and recommendations",
    "consensus",
    "workshop",
]

EXCLUDE_HINTS = [
    "singing voice",
    "vocal training",
    "voice pedagogy",
    "theater",
]


def load_packet(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def row_pmid(row: dict[str, str]) -> str:
    if row.get("id", "").startswith("PMID:"):
        return row["id"].replace("PMID:", "")
    match = re.search(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)", row.get("url", ""))
    return match.group(1) if match else ""


def fetch_pubmed_xml(pmids: list[str]) -> ET.Element:
    params = {"db": "pubmed", "retmode": "xml", "id": ",".join(pmids)}
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=90) as response:
        text = response.read().decode("utf-8", errors="replace")
    (RAW / "first_packet_pubmed_efetch.xml").write_text(text, encoding="utf-8")
    return ET.fromstring(text)


def abstract_text(article: ET.Element) -> str:
    parts: list[str] = []
    for node in article.findall(".//AbstractText"):
        label = node.attrib.get("Label")
        text = "".join(node.itertext()).strip()
        if not text:
            continue
        parts.append(f"{label}: {text}" if label else text)
    return " ".join(parts)


def pmid_from_article(article: ET.Element) -> str:
    pmid = article.findtext(".//PMID")
    return pmid or ""


def abstract_decision(title_decision: str, title: str, abstract: str) -> tuple[str, str]:
    text = f"{title} {abstract}".lower()
    if not abstract:
        return "", ""
    if any(h in text for h in EXCLUDE_HINTS):
        return "exclude", "Abstract/title suggests non-biomarker voice domain."
    if any(h in text for h in BACKGROUND_HINTS):
        return "background", "Review/consensus/framework source; use for framing or citation chaining."
    has_voice = any(x in text for x in ["voice", "vocal", "speech", "acoustic", "cough"])
    has_biomarker = any(x in text for x in ["biomarker", "digital biomarker", "marker", "phenotype"])
    has_health = any(
        x in text
        for x in [
            "patient",
            "clinical",
            "disease",
            "diagnosis",
            "screening",
            "monitoring",
            "aging",
            "heart failure",
            "parkinson",
            "depression",
            "asthma",
            "frailty",
        ]
    )
    has_empirical = any(h in text for h in EMPIRICAL_HINTS)
    if has_voice and has_biomarker and has_health and has_empirical:
        return "include", "Abstract supports audio-derived biomarker/health evidence with extractable empirical details."
    if title_decision == "include" and has_voice and has_health:
        return "maybe", "Likely relevant but abstract needs manual check for biomarker outcome and validation detail."
    return "maybe", "Abstract does not clearly satisfy all inclusion criteria; manual screening needed."


def main() -> None:
    path = SCREENING / "first-screening-packet.csv"
    rows = load_packet(path)
    pmids = []
    for row in rows:
        pmid = row_pmid(row)
        if pmid:
            pmids.append(pmid)

    abstracts: dict[str, str] = {}
    if pmids:
        root = fetch_pubmed_xml(pmids)
        for article in root.findall(".//PubmedArticle"):
            pmid = pmid_from_article(article)
            if pmid:
                abstracts[pmid] = abstract_text(article)

    for row in rows:
        row.setdefault("abstract", "")
        pmid = row_pmid(row)
        if pmid:
            if not row.get("id"):
                row["id"] = f"PMID:{pmid}"
            row["abstract"] = re.sub(r"\s+", " ", abstracts.get(pmid, "")).strip()
            decision, reason = abstract_decision(
                row.get("title_screen_decision", ""),
                row.get("title", ""),
                row["abstract"],
            )
            if decision:
                row["abstract_screen_decision"] = decision
                row["abstract_screen_reason"] = reason

    out = SCREENING / "first-screening-packet-with-abstracts.csv"
    fieldnames = list(rows[0].keys())
    if "abstract" not in fieldnames:
        fieldnames.append("abstract")
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    counts: dict[str, int] = {}
    abstract_count = 0
    for row in rows:
        if row.get("abstract"):
            abstract_count += 1
        decision = row.get("abstract_screen_decision") or "not_screened"
        counts[decision] = counts.get(decision, 0) + 1

    print(f"Wrote {out}")
    print(f"PubMed abstracts fetched: {abstract_count}")
    print(counts)


if __name__ == "__main__":
    main()
