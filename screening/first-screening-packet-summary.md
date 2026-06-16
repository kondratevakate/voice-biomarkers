# First Screening Packet Summary

Date: 2026-06-05

## Packet Construction

High-signal sources selected before broad/noisy sources:

- PubMed core terminology
- PubMed clinical validation
- PubMed aging / biological age
- Europe PMC preprints for core, validation, and dataset/foundation-model queries
- PubMed refined disease-domain query

Total records in packet: 200

## Title Screening Counts

- background: 16
- include: 105
- maybe: 79

## Notes

Title screening is preliminary. Records marked `include` or `maybe` still need abstract screening. Records marked `background` are not counted as empirical evidence unless full-text review later shows extractable empirical data.

## Abstract Enrichment

PubMed abstracts were fetched into `first-screening-packet-with-abstracts.csv`.

- PubMed abstracts fetched: 166
- Abstract-screen include: 94
- Abstract-screen maybe: 50
- Abstract-screen background: 20
- Abstract-screen exclude: 2
- Not screened yet, mostly non-PubMed/preprint rows without fetched abstract: 34

Next screening move: manually review the 94 `include` rows for extraction readiness and the 50 `maybe` rows for inclusion/exclusion. Keep `background` rows for definitions, validation frameworks, and citation chaining, but do not count them as empirical evidence unless reclassified after full text.
