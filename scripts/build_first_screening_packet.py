#!/usr/bin/env python
"""Build the screening packet for the review by stratified sampling.

The previous version of this script drew records only from a hard-coded set of
PubMed and Europe PMC preprint buckets, in retrieval order, and then assigned a
`title_screen_decision` from a keyword list. Three consequences followed:

1. OpenAlex, arXiv, and DBLP records could never reach screening at all, so the
   engineering literature was excluded downstream even when the search
   retrieved it.
2. Taking the first N rows of each bucket inherited whatever order the API
   returned, which is a sampling decision disguised as an implementation
   detail.
3. The keyword list decided inclusion. Because it named specific diseases
   (Parkinson, Alzheimer, heart failure, ...), the resulting disease mix partly
   reflected the keyword list rather than the literature.

This version samples every (source, query_family) bucket proportionally, picks
records within a bucket deterministically but without reference to API order,
and reduces the keyword list to an advisory annotation. Screening decisions are
left empty for a human to make.
"""

from __future__ import annotations

import csv
import hashlib
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources"
SCREENING = ROOT / "screening"

PACKET_SIZE = 400

# Advisory only. These flag records whose title names a construct the review
# cares about. They annotate; they never decide. Screening decisions are made
# by a human against the eligibility criteria in protocol.md.
TOPIC_HINTS = [
    "biomarker",
    "digital biomarker",
    "voice",
    "vocal",
    "speech",
    "acoustic",
    "dysarthria",
    "dysphonia",
    "cough",
    "phonation",
    "prosody",
    "articulation",
    "speaker",
    "aging",
    "biological age",
    "validation",
    "external validation",
    "generalization",
    "dataset",
    "corpus",
    "benchmark",
    "foundation model",
]

# Titles matching these are almost certainly out of scope: the signal is not
# human audio analysed as a health marker. Flagged, never auto-excluded.
OFF_SCOPE_HINTS = [
    "speech recognition",
    "text-to-speech",
    "speech synthesis",
    "speaker verification",
    "voice conversion",
    "speech enhancement",
    "voice assistant",
]


def norm_title(title: str) -> str:
    return re.sub(r"\W+", " ", title.lower()).strip()


def load_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def record_key(row: dict[str, str]) -> str:
    doi = (row.get("doi") or "").lower().replace("https://doi.org/", "").strip()
    return doi or norm_title(row.get("title", ""))


def hint_flags(title: str) -> tuple[str, str]:
    lowered = title.lower()
    topic = [h for h in TOPIC_HINTS if h in lowered]
    off = [h for h in OFF_SCOPE_HINTS if h in lowered]
    return "; ".join(topic), "; ".join(off)


def stratified_quotas(buckets: dict[tuple[str, str], list], target: int) -> dict:
    """Allocate the packet across buckets proportionally, with a floor.

    Every bucket gets at least one record so that no source or query family is
    silently absent from screening; the remainder is allocated in proportion to
    bucket size using largest-remainder, which is deterministic.
    """
    sizes = {k: len(v) for k, v in buckets.items() if v}
    if not sizes:
        return {}
    total = sum(sizes.values())
    floor_each = 1
    if len(sizes) * floor_each >= target:
        return {k: floor_each for k in sizes}

    remaining = target - len(sizes) * floor_each
    exact = {k: remaining * n / total for k, n in sizes.items()}
    quotas = {k: floor_each + int(math.floor(v)) for k, v in exact.items()}
    leftover = target - sum(quotas.values())
    for key, _ in sorted(exact.items(), key=lambda kv: (-(kv[1] % 1), kv[0])):
        if leftover <= 0:
            break
        quotas[key] += 1
        leftover -= 1
    return {k: min(v, sizes[k]) for k, v in quotas.items()}


def spread(rows: list[dict[str, str]], n: int) -> list[dict[str, str]]:
    """Take n records from a bucket without inheriting API return order.

    Records are ordered by a hash of their identity, which is stable across
    runs and independent of how any database chose to rank them. Taking the
    first n of that order is a reproducible pseudo-random sample rather than a
    relevance- or recency-weighted one.
    """
    ordered = sorted(rows, key=lambda r: hashlib.sha256(record_key(r).encode("utf-8")).hexdigest())
    return ordered[:n]


def main() -> None:
    pools = [
        SOURCES / "formal-candidates.csv",
        SOURCES / "formal-candidates-disease-refined.csv",
    ]
    rows: list[dict[str, str]] = []
    for path in pools:
        rows.extend(load_csv(path))

    seen: set[str] = set()
    buckets: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in rows:
        key = record_key(row)
        if not key or key in seen:
            continue
        seen.add(key)
        buckets.setdefault((row.get("source", ""), row.get("query_family", "")), []).append(row)

    quotas = stratified_quotas(buckets, PACKET_SIZE)

    selected: list[dict[str, str]] = []
    for bucket in sorted(quotas):
        for row in spread(buckets[bucket], quotas[bucket]):
            title = row.get("title", "")
            topic, off = hint_flags(title)
            selected.append(
                {
                    "screening_id": f"FS{len(selected) + 1:04d}",
                    "source": row.get("source", ""),
                    "query_family": row.get("query_family", ""),
                    "year": row.get("year", ""),
                    "title": title,
                    "venue": row.get("venue", ""),
                    "doi": row.get("doi", ""),
                    "url": row.get("url", ""),
                    "topic_hint_flags": topic,
                    "off_scope_hint_flags": off,
                    "title_screen_decision": "",
                    "title_screen_reason": "",
                    "abstract_screen_decision": "",
                    "abstract_screen_reason": "",
                    "full_text_decision": "",
                    "full_text_reason": "",
                    "screened_by": "",
                    "adjudication_status": "",
                }
            )

    out = SCREENING / "screening-packet-stratified.csv"
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(selected[0].keys()))
        writer.writeheader()
        writer.writerows(selected)

    by_source: dict[str, int] = {}
    by_family: dict[str, int] = {}
    for row in selected:
        by_source[row["source"]] = by_source.get(row["source"], 0) + 1
        by_family[row["query_family"]] = by_family.get(row["query_family"], 0) + 1

    summary = (
        "# Stratified Screening Packet\n\n"
        f"Records in packet: {len(selected)} of {len(seen)} deduplicated candidates "
        f"across {len(buckets)} (source, query family) buckets.\n\n"
        "## Sampling\n\n"
        "Every bucket receives at least one record; the remainder is allocated in "
        "proportion to bucket size by largest remainder. Within a bucket, records are "
        "ordered by a SHA-256 hash of their DOI or normalised title and the first n are "
        "taken. That order is stable across runs and independent of how any database "
        "ranked its results, so the packet is a reproducible sample rather than a "
        "relevance- or recency-weighted one.\n\n"
        "## Screening decisions\n\n"
        "`title_screen_decision` is intentionally empty. The keyword list in this script "
        "populates `topic_hint_flags` and `off_scope_hint_flags` only; it is advisory "
        "annotation and does not decide inclusion. Decisions are made by a human against "
        "the eligibility criteria in `protocol.md`, and recorded with `screened_by`.\n\n"
        "## By source\n\n"
        + "\n".join(f"- {k}: {v}" for k, v in sorted(by_source.items()))
        + "\n\n## By query family\n\n"
        + "\n".join(f"- {k}: {v}" for k, v in sorted(by_family.items()))
        + "\n"
    )
    (SCREENING / "screening-packet-stratified-summary.md").write_text(summary, encoding="utf-8")

    print(f"packet: {len(selected)} records from {len(buckets)} buckets -> {out}")
    for k, v in sorted(by_source.items()):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
