# Protocol: Voice Biomarkers Across Populations and Tasks

Date: 2026-06-05
Status: draft protocol

Method basis: K-Dense `literature-review`, `paper-lookup`, and `citation-management` skills; AI-scientist governance critique; Abdalla Z. Mohamed-style reproducibility pattern from systematic review, technical benchmarking, and data-descriptor papers.

## Review Type

Confirmed design: **systematic mapping review of the field**. This is the review type of record; earlier drafts also described the work as a "systematic review" and as a "living" review, and both descriptions are superseded here.

Reporting standards:

- **PRISMA-ScR** (Tricco et al., 2018, doi:10.7326/M18-0850) is the reporting guideline of record. PRISMA 2020 governs systematic reviews of effectiveness; mapping and scoping syntheses are reported against the ScR extension.
- **PRISMA-S** (Rethlefsen et al., 2021, doi:10.1186/s13643-020-01542-z) governs search reporting: exact strings, filters, dates, counts, raw exports, and re-runnable queries for every source.
- **JBI scoping-review guidance** (Peters et al., 2020, doi:10.11124/JBIES-20-00167) governs conduct.

Registration: PROSPERO does not accept scoping or mapping reviews. Registration, when made, goes to the Open Science Framework.

**Reproducible snapshot, not a living review.** The review reports the literature as of a stated search date (currently 1 September 2026) and carries no commitment to update. Currency is deliberately traded for reproducibility: every query string, filter, result count, and raw API response is preserved, so any later reader can re-execute the identical search and measure the delta rather than trust a claim of being current. The words "living", "continuously updated", and "rolling" must not be used to describe this review.

Escalation path: convert to a systematic review reported against PRISMA 2020 if full-text screening yields a manageable and clinically coherent subset.

Critical appraisal: optional under PRISMA-ScR. This review performs it anyway, because validation maturity and reproducibility are mapped dimensions (RQ4, RQ6), not eligibility filters.

## Methodological Standards

This review will follow a staged systematic mapping-review design. Quality and reproducibility assessment rests on three established instruments, not on a bespoke rubric:

- **V3 / V3+** (Goldsack et al., 2020, doi:10.1038/s41746-020-0260-4; Bakker et al., 2025) supplies the validation lens: verification, analytical validation, clinical validation, and usability. RQ4 is expressed in these terms.
- **PROBAST** (Wolff et al., 2019, doi:10.7326/M18-1376) supplies the risk-of-bias structure for prediction-model studies, which is what most voice-biomarker papers are.
- **TRIPOD+AI** (Collins et al., 2024, doi:10.1136/bmj-2023-078378) supplies the reporting expectations for machine-learning prediction models.

`governance/reproducibility-risk-of-bias-rubric.md` maps every rubric element to one of these instruments and states what the voice-specific adaptation adds. The adaptation is confined to domain specifics such as elicitation task, microphone and environment, speaker- and session-level leakage, and language or accent confounding.

Three operational disciplines are applied on top of the instruments above:

1. Systematic review discipline: PCC framing per PRISMA-ScR (PECO/PICOS if the review escalates to PRISMA 2020), PRISMA-family reporting, prospective registration when possible, full database-specific search strings, explicit exclusion reasons, and PROBAST-based risk-of-bias assessment.
2. Technical benchmarking discipline: validation claims must be tied to numerical evidence, such as subject-level split, external validation, repeated-measure reliability, calibration, subgroup performance, or robustness to recording protocol.
3. Data-infrastructure discipline: data availability, code availability, preprocessing documentation, quality-control metrics, and standardization of input data must be extracted as first-class outcomes.

The review will not treat reproducibility as a narrative limitation only. Reproducibility is an extraction and synthesis dimension.

The reporting and data-infrastructure style of Abdalla Z. Mohamed's systematic review, technical benchmarking, and data-descriptor papers was used as a worked example of these disciplines while drafting the protocol. It is an illustration of reporting practice, not a methodological standard for this review, and it is not a substitute for V3, PROBAST, or TRIPOD+AI.

## Research Questions

RQ1. Which populations have been studied for voice-derived biomarkers?

RQ2. Which tasks are used to elicit signal: sustained vowels, read speech, spontaneous speech, picture description, conversation, cough, breathing, singing, or passive audio?

RQ3. Which outcomes are modeled: chronological age, biological age, disease detection, disease severity, prognosis, treatment response, longitudinal deterioration, or speaker identity drift?

RQ4. What level of validation is reported: technical verification, analytical validation, clinical validation, external validation, longitudinal validation, fairness/generalization, or deployment evaluation?

RQ5. Which model/feature families dominate: hand-crafted acoustic features, linguistic features, self-supervised speech embeddings, multimodal models, clinical foundation models, or hybrid approaches?

RQ6. How reproducible and transportable are the reported biomarker claims with respect to data access, code access, preprocessing specification, recording protocol, subject-level separation, external validation, language/population generalization, and clinical reference standard?

## Eligibility Framework: Population, Concept, Context (PCC)

PRISMA-ScR and JBI guidance frame eligibility for mapping and scoping reviews as PCC rather than PICO/PECO. PICO presumes a comparator and an effect estimate, which a mapping review does not require: this review characterizes what the field has studied, not whether one intervention outperforms another.

| Element | Definition |
|---|---|
| **Population** | Humans of any age group, language, geography, health status, or clinical population. Non-human vocalization is excluded. |
| **Concept** | Voice, speech, vocalization, cough, breathing, or speech-language features extracted from audio and used as a biomarker, proxy marker, screening marker, monitoring marker, risk marker, or aging marker. The concept explicitly includes the *maturity* of that use: validation level attained (RQ4) and reproducibility/transportability of the claim (RQ6). |
| **Context** | Any recording and deployment setting: clinic, hospital, laboratory, home, remote or telehealth, population cohort, and any elicitation task, device, acoustic environment, or language. Both clinical and non-clinical research contexts are in scope. |

Comparator and outcome are not eligibility criteria in this review, but they remain mandatory *extraction* fields, because the map records what each study compared against and what it reported:

| Extraction dimension | Definition |
|---|---|
| Comparator | Clinical labels, chronological age, biological/omic/physiologic clocks, standard clinical scores, longitudinal follow-up, healthy controls, or external cohorts. |
| Outcomes | Biomarker performance, association with health/aging measures, generalization, validation evidence, bias/fairness, clinical utility. |
| Reproducibility outcome | Data/code availability, recording-protocol completeness, preprocessing transparency, split design, external validation, subgroup reporting, and auditability of the evidence claim. |

If the review escalates to a systematic review of effectiveness under PRISMA 2020, this framework converts back to PECO/PICOS and the comparator becomes an eligibility criterion.

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

Use `screening/extraction-template.csv` for first-pass title/abstract extraction and `screening/full-text-extraction-template.csv` for full-text evidence extraction and risk-of-bias/reproducibility scoring.

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

Risk-of-bias and reproducibility lens:

- Selection bias: recruitment, inclusion/exclusion, target-population match, case/control comparability.
- Measurement bias: recording task, microphone/device, environment, speech language, rater/scorer blinding where relevant.
- Leakage and modeling bias: subject-level split, session-level split, speaker overlap, site overlap, feature normalization leakage, hyperparameter tuning leakage.
- Reference-standard bias: diagnostic criteria, clinical label source, biological-age comparator, severity scale, adjudication method.
- Confounding: age, sex/gender, language, accent, disease severity, comorbidity, medication, site, device, socioeconomic or cultural factors.
- Statistical validity: sample size, calibration, uncertainty intervals, multiple testing, cross-validation design, external validation.
- Reproducibility: data access, code access, preprocessing description, model weights or feature definitions, random seeds where applicable, and availability of supplementary search/extraction material.

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
