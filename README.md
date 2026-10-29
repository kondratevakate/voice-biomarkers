# Voice biomarkers: a systematic mapping review

What evidence is there that voice, speech or other vocal features can work as
biomarkers for aging, disease, risk or longitudinal monitoring, across human
populations and recording tasks? This repository holds the protocol, the search,
the raw exports and the manuscript for a systematic mapping review that tries
to answer that, reported against PRISMA-ScR.

The review is a dated snapshot, not a living review. The search date of record
is 2026-09-01, and everything needed to re-run the identical search is here:
queries, scripts and the raw API responses.

## Status

Done:

- Protocol and search strategy, with the eligibility framed as PCC (population,
  concept, context).
- Formal search of PubMed, Europe PMC, Europe PMC preprints, arXiv, DBLP and
  OpenAlex: 8,499 deduplicated candidates, and no result set was truncated.
- A stratified screening packet of 400 records drawn from all 35 source and
  query-family buckets.

Open:

- Human title screening of `screening/screening-packet-stratified.csv`, with
  calibration on 50 records and at least 20% double screening.
- 8 OpenAlex source and query-family combinations failed with HTTP 429. They
  are kept as error rows in `sources/formal-search-counts.csv`, not dropped.
- Full-text extraction and risk-of-bias coding (R0 to R4 scale, PROBAST
  domains) on the 20-record calibration set.
- Databases without an open API (Embase, Scopus, Web of Science, IEEE Xplore,
  ACM, ISCA, CNKI and others): each needs a searched or not-accessible status in
  `sources/search-log.md`.
- eGeMAPS and COUGHVID return zero hits; still to explain.

The abstract-level figures currently in `main.tex` come from an earlier,
narrower packet (PubMed and Europe PMC only, keyword-based inclusion). The
manuscript says so, and they will be recomputed after screening.

## What is where

| Path | What it is |
|---|---|
| `main.tex`, `references.bib` | The manuscript. Import the repository into Overleaf and set `main.tex` as the main file. |
| `protocol.md` | Review question, eligibility, databases, synthesis plan. |
| `search-strategy.md` | Query families and the exact search strings. |
| `sources/` | Search outputs: deduplicated candidates, per-source counts, search log, seed papers. Files marked `-superseded` are earlier runs, kept so the deviation log can point at them. |
| `sources/raw/` | Raw API responses, as returned, with author email addresses redacted. |
| `screening/` | Screening packets, extraction templates, decisions. |
| `governance/` | Protocol deviation log, tool-run log, false-negative audit against a seed set, screening reliability, risk-of-bias rubric. |
| `figures/` | Planned figures (PRISMA flow, evidence map). Not generated yet. |
| `scripts/` | Search, packet building, redaction and the tests. |

The validation and bias lens is fixed by three published instruments: V3 for
validation, PROBAST for risk of bias, TRIPOD+AI for reporting. The rubric in
`governance/` maps every item to one of them.

## Re-running the search

The scripts use the Python standard library only.

Check that the APIs still honour the sort and pagination parameters the search
depends on. If a provider changes them, results silently stop being
reproducible, so run this first:

```bash
python scripts/test_search_api_contract.py
```

Run the search. Setting `OPENALEX_MAILTO` to your address puts OpenAlex requests
in its polite pool:

```bash
python scripts/run_formal_search.py
```

Rebuild the screening packet:

```bash
python scripts/build_first_screening_packet.py
```

A fresh run writes author email addresses back into `sources/raw/`. Redact them
and check before committing:

```bash
python scripts/redact_emails.py
```

```bash
python scripts/test_no_raw_emails.py
```

## Licence and citation

- Documents, data and logs: CC BY 4.0, see `LICENSE`.
- Code under `scripts/`: MIT, see `scripts/LICENSE`.

The bibliographic metadata in `sources/raw/` comes from PubMed, Europe PMC,
OpenAlex, arXiv and DBLP and stays under those providers' terms. The licence
covers this project's selection, arrangement and annotation of it. The SHA-256
of every original file is recorded in `sources/raw/MANIFEST.emails-redacted.csv`.

Please cite a tagged release rather than the branch, using `CITATION.cff`. The
DOI is added there once the release is minted.
