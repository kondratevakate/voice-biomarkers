# Voice Biomarkers Systematic Review

Created: 2026-06-05
Mode: act

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
| Abdalla Z. Mohamed method pattern | author-style note | `sources/author-style-abdalla-mohamed.md` | methodological analogy | confirmed | Used to harden reproducibility, benchmarking, and data-infrastructure requirements. |

## 3. Uncertainty

- The final review type is not locked: systematic review, scoping review, or systematic mapping review are all plausible.
- Inclusion boundaries are open: purely clinical voice biomarkers, aging clocks, disease detection, monitoring, and speech foundation models may be too broad for one manuscript.
- Preprints are not confirmed peer-reviewed evidence; they can seed the search but cannot be treated as settled findings.
- The formal search still needs query-family decomposition because one broad search is either too narrow in PubMed or too noisy in broad metadata indexes.

## 4. Candidate Next Actions

1. Run formal query-family searches for terminology/validation, aging/frailty, clinical disease domains, and datasets/foundation models.
2. Re-run arXiv and Semantic Scholar with narrower queries or API access after the pilot failures.
3. Screen `sources/pilot-candidates.csv`, then revise inclusion/exclusion criteria before full extraction.

## 5. Recommended Next Action

Use a systematic mapping review frame first, then narrow to a full systematic review after pilot search counts are visible.

## 6. Why This Is Next

The topic crosses clinical domains, age modeling, speech processing, datasets, and foundation models. A mapping frame prevents premature narrowing while still producing a reproducible evidence map: populations, tasks, recording protocols, model families, validation type, external validation, and clinical readiness.

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
- `governance/reproducibility-risk-of-bias-rubric.md` - rubric for R0-R4 reproducibility levels and ML/diagnostic risk-of-bias domains.

## Overleaf / GitHub Sync

This folder is prepared as a root-level LaTeX project. In Overleaf, import the private GitHub repository and set `main.tex` as the main document. The current manuscript is a living systematic mapping review draft, not a final PRISMA-complete article.

Local LaTeX is not required for GitHub sync; Overleaf can compile the project after import.
