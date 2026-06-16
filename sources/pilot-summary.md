# Pilot Search Summary

Date: 2026-06-05
Method basis: K-Dense `literature-review`, `paper-lookup`, `citation-management`

## Current State

The pilot search supports treating the project as a systematic mapping review of the field rather than a narrow disease-specific systematic review. The evidence base is distributed across cardiovascular/heart failure, respiratory disease, neurodegeneration, psychiatry, aging/frailty, smoking/behavioral health, pediatric health, and dataset/model infrastructure.

Raw exports are in `sources/raw/`. A first candidate table is in `sources/pilot-candidates.csv`.

## Source Basis

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

## Uncertainty

- PubMed alone misses important arXiv/medRxiv model and dataset papers.
- OpenAlex broad search requires stricter query decomposition before formal screening.
- Crossref broad counts are not meaningful for PRISMA identification unless query is narrowed heavily.
- Current candidate list is pilot-only and should not be treated as final included studies.

## Candidate Next Actions

1. Split formal search into four query families: `terminology/validation`, `aging/frailty`, `clinical disease domains`, and `datasets/foundation models`.
2. Re-run arXiv and Semantic Scholar with narrower queries and save raw exports.
3. Begin title/abstract screening from `pilot-candidates.csv`, marking each as `include`, `exclude`, `maybe`, or `background`.

## Recommended Next Action

Run a formal multi-query search rather than one broad query. The pilot shows that a single broad query is either too narrow in PubMed or too noisy in Crossref/OpenAlex.

## Why This Is Next

The field is heterogeneous. Query families will preserve sensitivity while allowing transparent screening by population, task, outcome, and validation maturity.

