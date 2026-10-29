# Formal Search Summary

Date: 2026-06-05
Method basis: K-Dense `literature-review` + ToolUniverse-informed database strategy

This is a record of the first formal pass (Stage 1). It is superseded by the
2026-09-01 run and kept for the audit trail.

## Summary

A formal multi-query search pass has been executed across PubMed, Europe PMC, Europe PMC preprints, OpenAlex, and arXiv API attempts. Raw API outputs are saved under `sources/raw/formal/`.

Outputs:

- `sources/formal-search-counts.csv`
- `sources/formal-candidates.csv`
- `sources/formal-search-counts-disease-refined.csv`
- `sources/formal-candidates-disease-refined.csv`

## Results

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

## Problems found

- arXiv API did not complete successfully in this run due to 429, timeout, and 503 errors. arXiv should be retried later with narrower exact-title/abstract queries and 3+ second spacing.
- OpenAlex and Europe PMC counts can be very broad; their top returned records are useful for discovery, but total counts are not equivalent to screened records.
- The disease-domain search remains too large as one family. It should be split into separate subqueries by clinical domain.
- Semantic Scholar was not included in this formal run because the prior pilot returned 429 without an API key.

## What happened next

- Ranking and truncation: this run kept the top relevance-ranked records per
  source, so its candidate counts depend on ranking. All sources were switched to
  deterministic date sorting with full pagination (DEV-007).
- Disease family: split into four subfamilies (neurological, psychiatric,
  respiratory, cardiometabolic), each pairing a named voice construct with disease
  terms (DEV-010).
- arXiv: rebuilt with a hand-written query per family (DEV-008).
- DBLP was added as an engineering index for ICASSP, Interspeech, ACL and ACM
  (DEV-011).
- The first screening packet of 200 PubMed and Europe PMC preprint records was
  built from this run (`screening/first-screening-packet.csv`). It was later
  replaced by a stratified packet across every source and query family (DEV-013).

The 2026-09-01 run gave 8,499 deduplicated candidates
(`sources/formal-candidates.csv`). The outputs of this run are kept as
`*-stage1-superseded.csv`.
