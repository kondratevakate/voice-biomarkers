# Stratified Screening Packet

Records in packet: 400 of 8724 deduplicated candidates across 35 (source, query family) buckets.

## Sampling

Every bucket receives at least one record; the remainder is allocated in proportion to bucket size by largest remainder. Within a bucket, records are ordered by a SHA-256 hash of their DOI or normalised title and the first n are taken. That order is stable across runs and independent of how any database ranked its results, so the packet is a reproducible sample rather than a relevance- or recency-weighted one.

## Screening decisions

`title_screen_decision` is intentionally empty. The keyword list in this script populates `topic_hint_flags` and `off_scope_hint_flags` only; it is advisory annotation and does not decide inclusion. Decisions are made by a human against the eligibility criteria in `protocol.md`, and recorded with `screened_by`.

## By source

- DBLP: 90
- EuropePMC: 135
- EuropePMC-PPR: 4
- OpenAlex: 3
- PubMed: 144
- arXiv: 24

## By query family

- aging_biological_age: 13
- clinical_validation: 7
- core_terminology: 16
- datasets_foundation_models: 38
- disease_cardiometabolic: 17
- disease_monitoring_refined: 13
- disease_neuro: 116
- disease_psych: 51
- disease_respiratory: 129
