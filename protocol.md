# Protocol: Voice Biomarkers Across Populations and Tasks

Date: 2026-06-05
Status: draft protocol

Method basis: K-Dense `literature-review`, `paper-lookup`, and `citation-management` skills.

## Review Type

Initial design: systematic mapping review with PRISMA-style search reporting.

Escalation path: convert to a systematic review if pilot search yields a manageable and clinically coherent subset.

Working confirmation: this is an academic systematic review of the field, not a venue-driven review.

## Research Questions

RQ1. Which populations have been studied for voice-derived biomarkers?

RQ2. Which tasks are used to elicit signal: sustained vowels, read speech, spontaneous speech, picture description, conversation, cough, breathing, singing, or passive audio?

RQ3. Which outcomes are modeled: chronological age, biological age, disease detection, disease severity, prognosis, treatment response, longitudinal deterioration, or speaker identity drift?

RQ4. What level of validation is reported: technical verification, analytical validation, clinical validation, external validation, longitudinal validation, fairness/generalization, or deployment evaluation?

RQ5. Which model/feature families dominate: hand-crafted acoustic features, linguistic features, self-supervised speech embeddings, multimodal models, clinical foundation models, or hybrid approaches?

## Population, Index, Comparator, Outcome

| Element | Definition |
|---|---|
| Population | Humans of any age group, language, geography, health status, or clinical population. |
| Index signal | Voice, speech, vocalization, cough, breathing, or speech-language features extracted from audio. |
| Comparator | Clinical labels, chronological age, biological/omic/physiologic clocks, standard clinical scores, longitudinal follow-up, healthy controls, or external cohorts. |
| Outcomes | Biomarker performance, association with health/aging measures, generalization, validation evidence, bias/fairness, clinical utility. |

## Inclusion Criteria

- Human data.
- Audio-derived voice, speech, or vocal features used as a biomarker, proxy marker, screening marker, monitoring marker, or risk marker.
- Empirical studies, datasets with benchmark tasks, validation studies, systematic/scoping reviews, and clinically relevant preprints.
- Any population, language, or recording environment.
- Studies reporting at least one modeled outcome, association, benchmark, or validation result.

## Exclusion Criteria

- Pure ASR/NLP papers without health, aging, or biomarker relevance.
- Non-human vocalization studies.
- Opinion pieces without a usable evidence framework, unless used only for background.
- Commercial claims without method/results detail.
- Papers where audio is only a UI channel and not analyzed as a biomarker.

## Databases and Sources

Detailed search conditions and database rationale are specified in `search-strategy.md`.

Minimum search sources:

- PubMed / PMC
- medRxiv / bioRxiv
- arXiv
- Semantic Scholar or OpenAlex
- Crossref
- Google Scholar-style broad academic search

Seed sources:

- arXiv:2603.01270
- medRxiv DOI 10.64898/2026.04.05.26350190

## Pilot Search Strings

### Broad

```text
("voice biomarker" OR "vocal biomarker" OR "speech biomarker" OR "voice-derived digital biomarker")
AND (aging OR disease OR clinical OR diagnosis OR monitoring OR prognosis OR screening)
```

### Aging and Biological Age

```text
("voice age" OR "vocal aging" OR "speech aging" OR "voice-based biological clock")
AND (biomarker OR "digital biomarker" OR "biological age" OR longitudinal)
```

### Clinical Validation

```text
("speech-based digital biomarker" OR "voice-derived biomarker")
AND ("clinical validation" OR "analytical validation" OR "external validation" OR "longitudinal validation")
```

### Populations and Fairness

```text
("voice biomarker" OR "speech biomarker")
AND (population OR language OR sex OR gender OR age OR pediatric OR fairness OR generalization)
```

### Foundation Models

```text
("clinical voice foundation model" OR "speech foundation model")
AND (biomarker OR disease OR health OR clinical metadata)
```

## Screening Workflow

1. Deduplicate by DOI, arXiv ID, medRxiv/bioRxiv DOI, then normalized title.
2. Title/abstract screening against inclusion and exclusion criteria.
3. Full-text screening for model task, population, outcome, and validation evidence.
4. Extract structured data into `screening/extraction-template.csv`.
5. Assign evidence category and quality/risk concerns.

K-Dense workflow checkpoints:

- Use at least three complementary databases before synthesis.
- Preserve exact search strings, dates, filters, and result counts in `sources/search-log.md`.
- Separate title screening, abstract screening, and full-text decisions in `screening/decisions.md`.
- Synthesize thematically, not as a study-by-study annotated bibliography.
- Verify DOI/citation metadata before final manuscript use.

## Extraction Fields

Use `screening/extraction-template.csv`.

Core dimensions:

- Population/domain
- Audio task and recording setting
- Feature/model family
- Outcome/biomarker claim
- Comparator/reference standard
- Validation type
- External validation and fairness/generalization
- Main performance/effect result
- Limitations and risk of bias

## Quality and Validation Framework

Primary validation lens:

- Verification: is the feature/model computed reliably?
- Analytical validation: is the measure robust to recording device, noise, task, language, demographic variation, and repeated measurement?
- Clinical validation: is the measure associated with a meaningful clinical or aging outcome?
- Clinical utility: does it improve decisions, monitoring, triage, or trial endpoints?

Risk concerns to code:

- Small sample size
- Leakage across speakers or sessions
- No subject-level split
- No external validation
- Demographic imbalance
- Language/task confounding
- Device/environment confounding
- Preprint only
- Unclear reference standard

## Synthesis Plan

The final review should synthesize thematically rather than paper-by-paper:

1. Aging and longitudinal voice change
2. Neurological and cognitive biomarkers
3. Mental health and affective state biomarkers
4. Respiratory, laryngeal, and cardiometabolic signals
5. Dataset/model infrastructure and foundation models
6. Validation, generalization, and equity gaps

## Planned Outputs

- Search log and PRISMA-style counts.
- Evidence map table: population x task x outcome x validation type.
- Thematic synthesis manuscript.
- At least one figure: PRISMA flow diagram or evidence-map schematic.

## Coverage Limitation and Required Expansion

The current formal search should be reported as Stage 1, not as exhaustive field coverage. It covers open English-oriented databases and preprint discovery through Europe PMC/OpenAlex/PubMed, with failed arXiv/Semantic Scholar attempts documented.

Before final synthesis, the review needs the multilingual and extended database layer in `sources/multilingual-and-extended-database-plan.md`, especially Chinese databases and engineering indexes. If access to subscription databases is unavailable, this must be reported explicitly as a limitation.

## Reproducibility and Governance Layer

This review uses an AI-scientist-inspired governance layer described in `governance/reproducibility-and-governance.md`.

Required controls before final synthesis:

- known-relevant seed-set retrieval test
- false-negative audit
- tool-run log
- search trajectory log
- protocol deviation log
- screening reliability log
- extraction provenance log
- manual adjudication of AI-assisted screening/extraction labels

Automated labels are provisional and must not be treated as final inclusion/exclusion decisions without manual confirmation or documented adjudication.
