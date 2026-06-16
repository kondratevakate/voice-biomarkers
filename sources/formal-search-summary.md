# Formal Search Summary

Date: 2026-06-05
Method basis: K-Dense `literature-review` + ToolUniverse-informed database strategy

## Current State

A formal multi-query search pass has been executed across PubMed, Europe PMC, Europe PMC preprints, OpenAlex, and arXiv API attempts. Raw API outputs are saved under `sources/raw/formal/`.

Outputs:

- `sources/formal-search-counts.csv`
- `sources/formal-candidates.csv`
- `sources/formal-search-counts-disease-refined.csv`
- `sources/formal-candidates-disease-refined.csv`

## Source Basis

### Main Formal Search Counts

| Query family | PubMed | Europe PMC | Europe PMC preprints | OpenAlex | arXiv |
|---|---:|---:|---:|---:|---|
| Core terminology | 57 | 200 | 10 | 1,833 | failed: 429 |
| Clinical validation | 41 | 5,024 | 30 | 12,723 | failed: 429 |
| Aging / biological age | 28 | 90 | 1 | 1,291 | failed: timeout |
| Disease detection / monitoring, broad | 6,580 | 248,465 | 3,021 | 749,203 | failed: 503 |
| Datasets / foundation models | 278 | 1,074 | 22 | 5,926 | failed: 429 |

Candidate output from main search:

- Raw candidate rows gathered from top API returns: 1,478
- Deduplicated candidates: 1,246

### Disease Query Refinement

The broad disease query was too noisy because it included generic terms such as `screening`, `monitoring`, `diagnosis`, `prognosis`, and `severity`. A refined disease query was run requiring voice/vocal/speech/acoustic terms plus biomarker terms plus disease-domain terms.

| Query family | PubMed | Europe PMC | Europe PMC preprints | OpenAlex |
|---|---:|---:|---:|---:|
| Disease detection / monitoring, refined | 352 | 21,638 | 195 | 74,586 |

Candidate output from refined disease search:

- Deduplicated candidates from top API returns: 390

## Uncertainty

- arXiv API did not complete successfully in this run due to 429, timeout, and 503 errors. arXiv should be retried later with narrower exact-title/abstract queries and 3+ second spacing.
- OpenAlex and Europe PMC counts can be very broad; their top returned records are useful for discovery, but total counts are not equivalent to screened records.
- The disease-domain search remains too large as one family. It should be split into separate subqueries by clinical domain.
- Semantic Scholar was not included in this formal run because the prior pilot returned 429 without an API key.

## Candidate Next Actions

1. Split disease search into domain subqueries:
   - neurological: Parkinson, ALS, motor neuron disease, Alzheimer, dementia
   - psychiatric: depression, anxiety, schizophrenia, psychosis
   - cardiovascular: heart failure, coronary disease, pulmonary hypertension
   - respiratory: asthma, COPD, respiratory, cough, tuberculosis
   - aging/frailty/cardiometabolic: frailty, cardiometabolic, diabetes, biological age
2. Retry arXiv with exact phrase queries:
   - `"voice biomarker"`
   - `"vocal biomarker"`
   - `"speech biomarker"`
   - `"clinical voice"`
   - `"voice foundation model"`
3. Start title/abstract screening from high-signal sources first:
   - PubMed core terminology
   - Europe PMC preprints core terminology
   - PubMed aging
   - PubMed clinical validation
   - refined disease PubMed top 100

## Recommended Next Action

Begin screening with the high-signal subset rather than screening all 1,246 candidates immediately. The first screening packet should be approximately 200 records drawn from PubMed and Europe PMC preprints.

## Why This Is Next

The formal search confirms the topic is broad and heterogeneous. A strong systematic article needs a transparent staged strategy: sensitive search, honest noise accounting, then prioritized screening by database/source quality and query specificity.

