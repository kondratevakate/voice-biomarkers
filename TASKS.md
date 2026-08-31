# Tasks

## Pending From Me

- [x] High (voice-biomarkers) Kate K. :: In VS Code, open `protocol.md` and confirm the review type line says "systematic mapping review of the field" :: DONE = review type line saved in `protocol.md` :: context=Lock review type before pilot search. Confirmed 2026-08-31; PRISMA-ScR/PRISMA-S/JBI adopted as reporting standards (DEV-006).
- [x] High (voice-biomarkers) :: Populate and audit `governance/known-relevant-seed-set.csv` against `sources/formal-candidates*.csv` :: DONE = every seed has retrieved/missed status and miss reason where applicable.
- [ ] High (voice-biomarkers) :: Apply `screening/full-text-extraction-template.csv` to the first 20 full texts for calibration :: DONE = extraction provenance rows exist and risk-of-bias disagreements are logged. Packet created: `screening/full-text-calibration-packet-20.csv`.
- [ ] High (voice-biomarkers) :: Execute or log access failure for CNKI, Wanfang, VIP, SinoMed, Embase, Scopus, Web of Science, IEEE Xplore, ACM, ACL/ISCA, and trial registries :: DONE = each database has `searched_exported`, `searched_no_export`, `access_unavailable`, `api_failed`, or `supplementary_only` status in `sources/search-log.md`.

- [ ] High (voice-biomarkers) :: Re-run `scripts/run_formal_search.py` with deterministic sorting and pagination, preserving the superseded Stage 1 counts in `sources/search-log.md` :: DONE = new counts CSV written, prior counts preserved, and any `ok_truncated_at_max_records` status resolved or reported (DEV-007).
- [ ] Medium (voice-biomarkers) :: Restate the eligibility framing as PCC (Population, Concept, Context) per PRISMA-ScR instead of PECO/PICOS :: DONE = `protocol.md` PICO table replaced by a PCC table and `main.tex` methods updated.
