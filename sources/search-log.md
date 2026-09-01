# Search Log

Search date: 2026-06-05
Searcher: Codex
Status: pilot search executed using K-Dense literature-review/paper-lookup fallback workflow

## Search Inventory

| Database/source | Query | Filters | Results | Export file | Notes |
|---|---|---|---:|---|---|
| PubMed | `("voice biomarker"[Title/Abstract] OR "vocal biomarker"[Title/Abstract] OR "speech biomarker"[Title/Abstract] OR "speech-based digital biomarker"[Title/Abstract]) AND (humans[MeSH Terms] OR human[Title/Abstract] OR clinical[Title/Abstract] OR health[Title/Abstract])` | retmax 50; relevance sort; no date limit | 53 | `sources/raw/pubmed_pilot_esearch.json`, `sources/raw/pubmed_pilot_esummary.json` | Strong biomedical seed set. |
| OpenAlex | `voice vocal speech biomarker clinical aging digital` | per-page 50; relevance sort | 1,852 | `sources/raw/openalex_pilot.json` | Broad but useful for influential cross-disciplinary papers. |
| Crossref | `voice vocal speech biomarker clinical aging digital` | rows 50; relevance sort | 6,254,881 | `sources/raw/crossref_pilot.json` | Too noisy as a discovery source; use later for DOI verification and exact-title lookup. |
| arXiv | `all:voice AND all:biomarker` | max 50 | failed | `sources/raw/arxiv_voice_biomarker.xml` | API returned 503 in this run; retry later or use arXiv web/API with narrower category terms. |
| Semantic Scholar | `voice vocal speech biomarker clinical aging` | limit 50 | failed | `sources/raw/semantic_scholar_pilot.json` | API returned 429; retry later or use API key. |
| Broad academic web | medRxiv/arXiv/PubMed targeted web queries | scholarly domains | qualitative hits | browser/session results | Used to catch recent medRxiv/arXiv preprints not surfaced by PubMed. |

## Seed Checks Completed

| Date | Source | Result |
|---|---|---|
| 2026-06-05 | arXiv:2603.01270 | Metadata captured in `seed-papers.md`. |
| 2026-06-05 | medRxiv 10.64898/2026.04.05.26350190 | Metadata captured in `seed-papers.md`. |
| 2026-06-05 | K-Dense pilot search | Candidate table created at `sources/pilot-candidates.csv`; summary at `sources/pilot-summary.md`. |
| 2026-06-05 | K-Dense + ToolUniverse-informed formal search | Raw exports saved under `sources/raw/formal/`; deduplicated candidates in `sources/formal-candidates.csv`; counts in `sources/formal-search-counts.csv`; summary in `sources/formal-search-summary.md`. |
| 2026-06-05 | Refined disease-domain search | Broad disease query was too noisy; refined query outputs saved in `sources/formal-candidates-disease-refined.csv` and `sources/formal-search-counts-disease-refined.csv`. |
| 2026-06-17 | Known-relevant seed audit | 6 of 8 seeds retrieved in Stage 1 candidate/screening CSVs. VoxKnesset and Babrak et al. were missed and added to `sources/seed-supplement-candidates.csv`; details in `governance/false-negative-audit.csv`. |

## Extended Database Status

Status vocabulary: `pending`, `searched_exported`, `searched_no_export`, `supplementary_only`, `access_unavailable`, `api_failed`, `not_applicable`.

| Database/source | Status | Date | Export/log file | Notes |
|---|---|---|---|---|
| PubMed | searched_exported | 2026-06-05 | `sources/raw/formal/pubmed_*` | Stage 1 formal search complete. |
| Europe PMC | searched_exported | 2026-06-05 | `sources/raw/formal/europepmc_all_*` | Stage 1 formal search complete. |
| Europe PMC preprints | searched_exported | 2026-06-05 | `sources/raw/formal/europepmc_preprints_*` | Used for medRxiv/bioRxiv discovery. |
| OpenAlex | searched_exported | 2026-06-05 | `sources/raw/formal/openalex_*` | Stage 1 formal search complete; broad counts require careful interpretation. |
| arXiv | api_failed | 2026-06-05 | `sources/formal-search-summary.md` | 429, timeout, and 503 errors; retry required. |
| Semantic Scholar | api_failed | 2026-06-05 | `sources/search-log.md` | Pilot failed with 429; API key or slow retry required. |
| Google Scholar-style broad web | supplementary_only | 2026-06-05 | `sources/search-log.md` | Useful for sensitivity only unless exportable. |
| Consensus (Semantic Scholar/PubMed/Scopus/arXiv) | supplementary_only | 2026-08-31 | `sources/seed-supplement-candidates.csv`; `governance/tool-run-log.csv` TR-20260831-001..004 | Free tier caps results at 3 per query and has no export endpoint. Used only as a false-negative probe; surfaced 4 records (FNA-009..012), 3 of them from IEEE/GSA venues. Must not be used for PRISMA counts. |
| CNKI | pending | TBD | TBD | Must be searched or logged as access unavailable. |
| Wanfang | pending | TBD | TBD | Must be searched or logged as access unavailable. |
| VIP Chinese Journals | pending | TBD | TBD | Must be searched or logged as access unavailable. |
| SinoMed | pending | TBD | TBD | Must be searched or logged as access unavailable. |
| Embase | pending | TBD | TBD | Subscription access required. |
| Scopus | pending | TBD | TBD | Subscription access required. |
| Web of Science | pending | TBD | TBD | Subscription access required. |
| IEEE Xplore | pending | TBD | TBD | Needed for speech-processing and signal-processing coverage. |
| ACM Digital Library | pending | TBD | TBD | Needed for CS/ML coverage. |
| ACL Anthology / ISCA Archive | pending | TBD | TBD | Needed for speech/language conference coverage. |
| ClinicalTrials.gov | pending | TBD | TBD | Needed for clinical deployment/trial claims. |
| WHO ICTRP | pending | TBD | TBD | Needed for trial-registry coverage. |
| EU Clinical Trials Register | pending | TBD | TBD | Needed for trial-registry coverage. |

## Reproducibility Notes

- **Stage 1 counts are not re-runnable and must be regenerated (DEV-007, 2026-08-31).** Every Stage 1 formal search was executed with relevance sorting and a single 100-record page per source. Relevance ranking is not stable over time and single-page retrieval silently truncated large result sets, so `sources/formal-candidates.csv`, `sources/formal-search-counts.csv`, and their disease-refined variants cannot be reproduced by re-running the script. `scripts/run_formal_search.py` now sorts by publication date and paginates, and reports truncation as `ok_truncated_at_max_records`. When the search is re-run, preserve the superseded counts in this log rather than overwriting them.
- Search parameters are contract-tested against the live APIs by `scripts/test_search_api_contract.py`; run it before trusting any new search output.
- **arXiv was never validly queried in Stage 1 (DEV-008, 2026-08-31).** The arXiv query string was assembled from a human-readable family label and a truncated slice of the generic query, producing unbalanced quotes; arXiv parsed it as a disjunction of bare words and matched its entire corpus. Stage 1 recorded this as an API failure, but the query was also malformed. Each family now carries an explicit arXiv query. Corrected hit counts, measured 2026-08-31: core terminology 24, clinical validation 7, aging and biological age 8, disease monitoring 30, datasets and foundation models 254.
- **Stage 2 deterministic re-run completed 2026-09-01 (TR-20260901-001, completed by TR-20260901-002).** All 25 source-family combinations succeeded: zero error rows, arXiv retrieved validly for the first time (24 / 7 / 8 / 30 / 255 topical hits per family). Result: 10,347 deduplicated candidates in `sources/formal-candidates.csv`. Stage 1 outputs are preserved verbatim in `sources/formal-candidates-stage1-superseded.csv` and `sources/formal-search-counts-stage1-superseded.csv`. Twelve source-family combinations report `ok_truncated_at_max_records`; the dominant ones are OpenAlex disease_monitoring (886,668 hits, 1,000 retrieved) and Europe PMC disease_monitoring (254,067 hits, 1,000 retrieved). Because retrieval is date-sorted, truncated families over-sample recent work; the family must be narrowed before its counts can support synthesis.
- **Stage 3 completed 2026-09-01 with the narrowed families and the DBLP layer (TR-20260901-006 to -008).** Eight query families across six sources. Result: 8,499 deduplicated candidates from PubMed (3,161), Europe PMC (2,951), DBLP (1,974) and arXiv (413). **Zero rows report truncation**: every family that completed retrieved its entire result set, so the date-sorted retrieval no longer over-samples recent work and the recency bias introduced alongside the DEV-007 fix is gone. Eight rows remain in error, all OpenAlex, from a rate-limit block that persisted for the whole session and was not lifted by the polite-pool contact address; OpenAlex must be completed separately.
- **The DBLP layer closed the content gap it was added to close (DEV-011 confirmed).** Records that were absent from the 10,347-record Stage 2 corpus and are present now: ADReSS 6, Tsanas 8, DementiaBank 2, Interspeech 258, ICASSP 118. The diagnosis that the field's benchmark and model layer was missing because of index coverage rather than because it does not exist is therefore supported by retrieval, not only by argument.
- Stage 2 outputs are preserved in `sources/formal-candidates-stage2-superseded.csv` and `sources/formal-search-counts-stage2-superseded.csv`; Stage 1 outputs remain in the `-stage1-superseded` pair.

- Record exact query string, database, filters, date searched, number of hits, and export filename.
- Keep raw exports under `sources/raw/` when searches are run.
- Do not update included/excluded counts without preserving the prior count in this log.
