# Pilot Search Summary

Date: 2026-06-05
Method basis: K-Dense `literature-review`, `paper-lookup`, `citation-management`

This is a record of the first exploratory search. It is kept for the audit trail.
The search of record is the 2026-09-01 run in `sources/formal-search-counts.csv`.

## Summary

The pilot search supports treating the project as a systematic mapping review of the field rather than a narrow disease-specific systematic review. The evidence base is distributed across cardiovascular/heart failure, respiratory disease, neurodegeneration, psychiatry, aging/frailty, smoking/behavioral health, pediatric health, and dataset/model infrastructure.

Raw exports are in `sources/raw/`. A first candidate table is in `sources/pilot-candidates.csv`.

## Results by source

### PubMed

- Search type: Title/Abstract biomedical search.
- Result count: 53.
- Export: `pubmed_pilot_esearch.json`, `pubmed_pilot_esummary.json`.
- Signal quality: high.

Top relevant candidate clusters:

- Heart failure and cardiovascular voice biomarkers.
- Motor neuron disease / ALS digital speech biomarkers.
- Respiratory/asthma/pulmonary hypertension voice biomarkers.
- Frailty and aging-related phenotypes.
- Smoking status and behavioral/mental health voice biomarkers.
- Consensus terminology and validation reviews.

### OpenAlex

- Search type: broad cross-disciplinary search.
- Result count: 1,852.
- Export: `openalex_pilot.json`.
- Signal quality: mixed; useful for influential foundational and cross-domain references.

Notable surfaced references:

- GeMAPS acoustic parameter set.
- Evaluation of Speech-Based Digital Biomarkers: Review and Recommendations.
- Vocal biomarkers of depression based on motor incoordination.
- Digital biomarkers for Alzheimer's disease context.

### Crossref

- Search type: broad metadata search.
- Result count: 6,254,881.
- Export: `crossref_pilot.json`.
- Signal quality: too noisy for discovery because "voice" retrieves pedagogy, humanities, and generic speech literature.
- Recommended use: exact DOI/title verification, not broad discovery.

### arXiv

- Status: attempted, API returned 503.
- Recommended next retry: narrower queries by title/category, for example `ti:"voice biomarker"` and categories `eess.AS`, `cs.CL`, `cs.LG`.

### Semantic Scholar

- Status: attempted, API returned 429.
- Recommended next retry: use API key or query fewer records after delay.

### Broad Academic Web

Recent relevant preprints found by targeted web search:

- Sound of Aging: Large-Scale Evidence for a Voice-Based Biological Clock.
- Towards A Foundation Model for Clinical Voice Biomarkers.
- Consensus-Based Definitions for Vocal Biomarkers.
- Vocal markers of schizophrenia and generalizability.
- Longitudinal normative dataset / Voiceome protocol.
- Digital voice-based biomarker for respiratory quality of life.

## Problems found

- PubMed alone misses important arXiv/medRxiv model and dataset papers.
- OpenAlex broad search requires stricter query decomposition before formal screening.
- Crossref broad counts are not meaningful for PRISMA identification unless query is narrowed heavily.
- Current candidate list is pilot-only and should not be treated as final included studies.

## What happened next

The pilot led to the formal multi-query search described in
`sources/formal-search-summary.md`. Of the follow-ups listed here at the time:

- Query families: the search was split into families, and the disease family
  was later split again into four disease subfamilies (DEV-010).
- arXiv: retried with a hand-written query per family (DEV-008) and completed
  in the 2026-09-01 run.
- Semantic Scholar: not retried. It is recorded as `api_failed` in
  `sources/search-log.md`.
- Screening from `pilot-candidates.csv`: replaced by the stratified packet in
  `screening/screening-packet-stratified.csv` (DEV-013).
