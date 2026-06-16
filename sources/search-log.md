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

## Reproducibility Notes

- Record exact query string, database, filters, date searched, number of hits, and export filename.
- Keep raw exports under `sources/raw/` when searches are run.
- Do not update included/excluded counts without preserving the prior count in this log.
