#!/usr/bin/env python
"""Build the first high-signal screening packet for the review."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources"
SCREENING = ROOT / "screening"


HIGH_SIGNAL = {
    ("PubMed", "core_terminology"): 80,
    ("PubMed", "clinical_validation"): 60,
    ("PubMed", "aging_biological_age"): 40,
    ("EuropePMC-PPR", "core_terminology"): 30,
    ("EuropePMC-PPR", "clinical_validation"): 30,
    ("EuropePMC-PPR", "datasets_foundation_models"): 30,
    ("PubMed", "disease_monitoring_refined"): 80,
}


INCLUDE_HINTS = [
    "biomarker",
    "digital biomarker",
    "vocal biomarker",
    "voice biomarker",
    "speech biomarker",
    "voice age",
    "vocal aging",
    "speech aging",
    "biological clock",
    "clinical utility",
    "external validation",
    "heart failure",
    "parkinson",
    "alzheimer",
    "dementia",
    "depression",
    "schizophrenia",
    "asthma",
    "frailty",
    "pulmonary hypertension",
]

BACKGROUND_HINTS = [
    "systematic review",
    "review and recommendations",
    "consensus-based definitions",
    "workshop summaries",
    "from research to clinical practice",
]

EXCLUDE_HINTS = [
    "singing",
    "choir",
    "pedagogy",
    "theater",
    "vocal traditions",
    "laryngoscopy",
]


def norm_title(title: str) -> str:
    return re.sub(r"\W+", " ", title.lower()).strip()


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def title_decision(title: str) -> tuple[str, str]:
    t = title.lower()
    if any(h in t for h in EXCLUDE_HINTS):
        return "exclude", "Title suggests voice/vocal topic without biomarker-health relevance."
    if any(h in t for h in BACKGROUND_HINTS):
        return "background", "Review/consensus/framework source; useful for framing or citation chaining."
    if any(h in t for h in INCLUDE_HINTS):
        return "include", "Title contains voice/speech biomarker or target health/aging domain."
    if any(x in t for x in ["voice", "vocal", "speech", "acoustic"]) and any(
        y in t for y in ["clinical", "health", "disease", "monitoring", "diagnosis", "screening"]
    ):
        return "maybe", "Title suggests possible audio-health relevance; abstract needed."
    return "maybe", "Title alone is insufficient; abstract needed."


def main() -> None:
    rows = load_csv(SOURCES / "formal-candidates.csv")
    disease_rows = load_csv(SOURCES / "formal-candidates-disease-refined.csv")
    by_bucket: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in rows + disease_rows:
        bucket = (row.get("source", ""), row.get("query_family", ""))
        by_bucket.setdefault(bucket, []).append(row)

    selected: list[dict[str, str]] = []
    seen: set[str] = set()
    for bucket, limit in HIGH_SIGNAL.items():
        for row in by_bucket.get(bucket, [])[:limit]:
            key = (row.get("doi") or "").lower().replace("https://doi.org/", "").strip()
            key = key or norm_title(row.get("title", ""))
            if not key or key in seen:
                continue
            seen.add(key)
            decision, reason = title_decision(row.get("title", ""))
            selected.append(
                {
                    "screening_id": f"FS{len(selected) + 1:04d}",
                    "source": row.get("source", ""),
                    "query_family": row.get("query_family", ""),
                    "year": row.get("year", ""),
                    "title": row.get("title", ""),
                    "venue": row.get("venue", ""),
                    "doi": row.get("doi", ""),
                    "url": row.get("url", ""),
                    "title_screen_decision": decision,
                    "title_screen_reason": reason,
                    "abstract_screen_decision": "",
                    "abstract_screen_reason": "",
                    "full_text_decision": "",
                    "full_text_reason": "",
                    "extract_now": "yes" if decision == "include" else "no",
                }
            )
            if len(selected) >= 200:
                break
        if len(selected) >= 200:
            break

    out = SCREENING / "first-screening-packet.csv"
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(selected[0].keys()))
        writer.writeheader()
        writer.writerows(selected)

    counts: dict[str, int] = {}
    for row in selected:
        counts[row["title_screen_decision"]] = counts.get(row["title_screen_decision"], 0) + 1

    summary = SCREENING / "first-screening-packet-summary.md"
    summary.write_text(
        "# First Screening Packet Summary\n\n"
        "Date: 2026-06-05\n\n"
        "## Packet Construction\n\n"
        "High-signal sources selected before broad/noisy sources:\n\n"
        "- PubMed core terminology\n"
        "- PubMed clinical validation\n"
        "- PubMed aging / biological age\n"
        "- Europe PMC preprints for core, validation, and dataset/foundation-model queries\n"
        "- PubMed refined disease-domain query\n\n"
        f"Total records in packet: {len(selected)}\n\n"
        "## Title Screening Counts\n\n"
        + "\n".join(f"- {k}: {v}" for k, v in sorted(counts.items()))
        + "\n\n"
        "## Notes\n\n"
        "Title screening is preliminary. Records marked `include` or `maybe` still need abstract screening. "
        "Records marked `background` are not counted as empirical evidence unless full-text review later shows extractable empirical data.\n",
        encoding="utf-8",
    )

    print(f"Wrote {out}")
    print(f"Wrote {summary}")
    print(counts)


if __name__ == "__main__":
    main()

