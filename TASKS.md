# Tasks

## Pending From Me

- [x] High (voice-biomarkers) Kate K. :: In VS Code, open `protocol.md` and confirm the review type line says "systematic mapping review of the field" :: DONE = review type line saved in `protocol.md` :: context=Lock review type before pilot search. Confirmed 2026-08-31; PRISMA-ScR/PRISMA-S/JBI adopted as reporting standards (DEV-006).
- [x] High (voice-biomarkers) :: Populate and audit `governance/known-relevant-seed-set.csv` against `sources/formal-candidates*.csv` :: DONE = every seed has retrieved/missed status and miss reason where applicable.
- [ ] High (voice-biomarkers) :: Apply `screening/full-text-extraction-template.csv` to the first 20 full texts for calibration :: DONE = extraction provenance rows exist and risk-of-bias disagreements are logged. Packet created: `screening/full-text-calibration-packet-20.csv`.
- [ ] High (voice-biomarkers) :: Execute or log access failure for CNKI, Wanfang, VIP, SinoMed, Embase, Scopus, Web of Science, IEEE Xplore, ACM, ACL/ISCA, and trial registries :: DONE = each database has `searched_exported`, `searched_no_export`, `access_unavailable`, `api_failed`, or `supplementary_only` status in `sources/search-log.md`.

- [x] High (voice-biomarkers) :: Re-run `scripts/run_formal_search.py` once `scripts/test_search_api_contract.py` passes all five checks :: DONE 2026-09-01 = contract test passed 5/5, clean run TR-20260901-001 + completion TR-20260901-002, zero error rows, 10,347 candidates, Stage 1 preserved in *-stage1-superseded.csv, truncation reported per row.
- [x] Medium (voice-biomarkers) :: Restate the eligibility framing as PCC (Population, Concept, Context) per PRISMA-ScR instead of PECO/PICOS :: DONE 2026-08-31 = `protocol.md` PCC table added, `main.tex` eligibility subsection updated, governance doc aligned.
- [ ] High (voice-biomarkers) :: Narrow the `disease_monitoring` query family :: DONE = OpenAlex hit count below the 1000-record retrieval ceiling, or the family split into subfamilies. It currently returns 886,609 OpenAlex and 253,991 Europe PMC hits, so retrieval covers roughly 0.1 percent of the result set and no amount of pagination fixes it.
- [ ] Medium (voice-biomarkers) :: Rewrite the arXiv sentence in the Limitations section of `main.tex` :: DONE = the text says arXiv was never validly queried (DEV-008), not merely that the API failed.
