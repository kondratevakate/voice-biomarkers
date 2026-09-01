# Stratified Screening Packet

Records in packet: 400 of 10549 deduplicated candidates across 27 (source, query family) buckets.

## Sampling

Every bucket receives at least one record; the remainder is allocated in proportion to bucket size by largest remainder. Within a bucket, records are ordered by a SHA-256 hash of their DOI or normalised title and the first n are taken. That order is stable across runs and independent of how any database ranked its results, so the packet is a reproducible sample rather than a relevance- or recency-weighted one.

## Screening decisions

`title_screen_decision` is intentionally empty. The keyword list in this script populates `topic_hint_flags` and `off_scope_hint_flags` only; it is advisory annotation and does not decide inclusion. Decisions are made by a human against the eligibility criteria in `protocol.md`, and recorded with `screened_by`.

## By source

- EuropePMC: 118
- EuropePMC-PPR: 41
- OpenAlex: 169
- PubMed: 57
- arXiv: 15

## By query family

- aging_biological_age: 41
- clinical_validation: 73
- core_terminology: 48
- datasets_foundation_models: 86
- disease_monitoring: 140
- disease_monitoring_refined: 12
