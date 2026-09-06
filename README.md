# Voice Biomarkers Systematic Review

Created: 2026-06-05
Last substantive update: 2026-09-01
Search date of record: 2026-09-01

## 1. Current State

This project is a systematic review workspace for voice-derived biomarkers across populations and tasks. The seed topic comes from two 2026 preprints:

- VoxKnesset: longitudinal Hebrew parliamentary speech for aging speaker modeling.
- Sound of Aging: large-scale evidence for a voice-based biological clock.

The working research question is:

> Across human populations and recording tasks, what evidence supports voice, speech, or vocal features as scalable biomarkers for aging, disease state, risk stratification, or longitudinal monitoring?

## 2. Source Basis

| Source | Type | Location | Authority | Freshness | Notes |
|---|---|---|---|---|---|
| VoxKnesset | preprint | https://arxiv.org/abs/2603.01270 | working | tentative | Seed source for longitudinal speech, age prediction, speaker verification drift. |
| Sound of Aging | preprint | https://www.medrxiv.org/content/10.64898/2026.04.05.26350190v1.full-text | working | tentative | Seed source for voice-predicted biological age and cardiometabolic associations. |
| International VOCAL Initiative definitions | preprint | https://www.medrxiv.org/content/10.1101/2025.10.23.25338518.abstract | working | tentative | Candidate terminology anchor for "vocal biomarker". |
| Evaluation of Speech-Based Digital Biomarkers | review/recommendations | https://pmc.ncbi.nlm.nih.gov/articles/PMC7670321/ | authoritative | confirmed | Candidate validation framework: verification, analytical validation, clinical validation. |
| Literature-review skill | local method | K-Dense literature-review skill | authoritative | confirmed | Review workflow: search, screening, extraction, quality assessment, synthesis, citation verification. |
| Task-design skill | local execution method | D:/projects/knowledge-vault/07_skills/task-design.md | authoritative | confirmed | Applied to task card in TASKS.md. |
| V3 / V3+ | reporting framework | doi:10.1038/s41746-020-0260-4 | authoritative | confirmed | Validation lens of record: verification, analytical validation, clinical validation, usability. |
| PROBAST | risk-of-bias tool | doi:10.7326/M18-1376 | authoritative | confirmed | Risk-of-bias structure for prediction-model studies, which is what most voice-biomarker papers are. |
| TRIPOD+AI | reporting guideline | doi:10.1136/bmj-2023-078378 | authoritative | confirmed | Reporting expectations for machine-learning prediction models. |
| PRISMA-ScR / PRISMA-S / JBI | reporting guidelines | doi:10.7326/M18-0850; doi:10.1186/s13643-020-01542-z; doi:10.11124/JBIES-20-00167 | authoritative | confirmed | Reporting and conduct standards for a mapping review and its search. |
| Abdalla Z. Mohamed method pattern | author-style note | `sources/author-style-abdalla-mohamed.md` | worked example only | confirmed | Illustration of reporting style while drafting the extraction schema. Superseded as a methodological standard by V3, PROBAST and TRIPOD+AI (DEV-014). |

## 3. Uncertainty

- The final review type is not locked: systematic review, scoping review, or systematic mapping review are all plausible.
- Inclusion boundaries are open: purely clinical voice biomarkers, aging clocks, disease detection, monitoring, and speech foundation models may be too broad for one manuscript.
- Preprints are not confirmed peer-reviewed evidence; they can seed the search but cannot be treated as settled findings.
- The formal search still needs query-family decomposition because one broad search is either too narrow in PubMed or too noisy in broad metadata indexes.

## 4. Search State

The formal search is complete for five of six sources as of 2026-09-01. Eight
query families run across PubMed, Europe PMC, Europe PMC preprints, arXiv and
DBLP, yielding **8,499 deduplicated candidates** with **zero truncated result
sets**: every completed family retrieved in full, so the date-sorted retrieval
does not over-sample recent work.

Eight OpenAlex source-family combinations remain outstanding, blocked by a
rate limit applied to the client IP. They are tracked in `TASKS.md` and reported
as errors in `sources/formal-search-counts.csv` rather than dropped.

Superseded outputs are preserved rather than overwritten:
`sources/formal-candidates-stage1-superseded.csv` and the matching
`-stage2-superseded` pair.

## 5. Recommended Next Action

Human title screening of `screening/screening-packet-stratified.csv`. The packet
holds 400 records sampled proportionally across all 35 (source, query family)
buckets, with screening decisions deliberately left empty; the SOP requires
calibration on 50 records and at least 20% double screening before the
concentration and validation figures can be recomputed.

## 6. Why This Is Next

Every remaining conclusion depends on screening decisions that no human has yet
made. The abstract-level figures currently reported in the manuscript come from
an earlier packet built by a procedure that drew only from PubMed and Europe PMC
and used a disease-naming keyword list to decide inclusion, so they carry a
known and documented bias.

## Workspace

- `main.tex` - Overleaf-ready manuscript draft for GitHub import.
- `references.bib` - BibTeX file with verified seed and framework citations.
- `protocol.md` - review question, eligibility criteria, databases, search strings, and synthesis plan.
- `sources/seed-papers.md` - verified metadata and extraction notes for the two seed papers.
- `sources/search-log.md` - reproducible search log to fill during database searches.
- `screening/extraction-template.csv` - structured extraction schema.
- `screening/full-text-extraction-template.csv` - full-text extraction schema for reproducibility maturity and risk-of-bias scoring.
- `screening/full-text-calibration-packet-20.csv` - first 20 records selected for full-text extraction calibration.
- `screening/full-text-calibration-availability.csv` - PubMed/Europe PMC DOI/PMCID availability for the calibration packet.
- `screening/full-text-calibration-term-precheck.csv` - automated PMC term-presence precheck for validation, split/leakage, recording protocol, demographics, metrics, data/code availability, and limitations.
- `screening/decisions.md` - inclusion/exclusion decisions and reasons.
- `draft/review.md` - manuscript skeleton.
- `figures/figure-plan.md` - planned PRISMA and concept figures.
- `governance/reproducibility-risk-of-bias-rubric.md` - rubric for R0-R4 reproducibility levels and risk-of-bias domains, each mapped to V3, PROBAST or TRIPOD+AI.
- `governance/protocol-deviation-log.csv` - every change made after the formal search began, with reason and impact (DEV-001 to DEV-018).
- `governance/tool-run-log.csv` - one row per automated run: tool, endpoint, exact input, filters, outputs, status.
- `scripts/run_formal_search.py` - formal search across six sources, deterministic date sorting, complete pagination.
- `scripts/test_search_api_contract.py` - nine live contract checks; run before trusting any new search output.
- `scripts/build_first_screening_packet.py` - stratified screening packet across all source and query-family buckets.
- `screening/screening-packet-stratified.csv` - the current screening packet, awaiting human decisions.

## Overleaf / GitHub Sync

This folder is prepared as a root-level LaTeX project. In Overleaf, import the private GitHub repository and set `main.tex` as the main document.

The manuscript is a **reproducible snapshot** of the literature as of its stated search date, not a living review: it carries no update commitment, and currency is traded for the ability to re-execute the identical search from the preserved queries and raw exports. It is not yet a reporting-complete article; full-text screening, risk-of-bias coding, and the outstanding OpenAlex combinations remain open.

Local LaTeX is not required for GitHub sync; Overleaf can compile the project after import.
