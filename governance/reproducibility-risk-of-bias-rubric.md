# Reproducibility and Risk-of-Bias Rubric

Date: 2026-06-17
Status: required for full-text extraction

## Purpose

This rubric operationalizes three established instruments for the voice-biomarkers review. It should be applied during full-text extraction to all empirical studies, dataset papers, benchmark papers, and model papers.

The rubric is not a new instrument. It is a domain adaptation, and every element below maps to a published standard so that reviewers can check it against the source:

| This rubric | Established instrument | What the adaptation adds |
|---|---|---|
| Validation lens: verification, analytical validation, clinical validation, clinical utility | **V3 / V3+** (Goldsack et al. 2020, doi:10.1038/s41746-020-0260-4; Bakker et al. 2025) | Names the voice-specific evidence each V3 component requires: recording protocol and device for verification; repeatability across task, microphone, environment and language for analytical validation. |
| Risk-of-bias domains | **PROBAST** (Wolff et al. 2019, doi:10.7326/M18-1376) participants, predictors, outcome, analysis | Splits PROBAST's analysis domain into the failure modes that dominate speech machine learning: speaker/session/site leakage, normalisation before split, and language or accent confounding. |
| Reporting expectations for model papers | **TRIPOD+AI** (Collins et al. 2024, doi:10.1136/bmj-2023-078378) | Adds audio-specific reporting items: elicitation task, sampling rate, device, and preprocessing chain. |
| R0-R4 reproducibility maturity | No single published standard; consistent with TRIPOD+AI items on data and code availability | Provides an ordinal scale so reproducibility can be synthesised as an outcome rather than narrated in limitations. |

Where this rubric and a published instrument disagree, the published instrument governs and the deviation is logged in `protocol-deviation-log.csv`.

## Reproducibility Maturity

| Level | Label | Criteria |
|---|---|---|
| R0 | Not reproducible from report | Missing core information about data, recording task, features/model, split design, or outcome. |
| R1 | Methods described only | Recording protocol, feature/model family, outcome, and validation design are described, but no usable data/code/materials are available. |
| R2 | Partially reproducible | At least one reproducibility asset is available: data, code, model, preprocessing description, supplementary feature definitions, or candidate split details. |
| R3 | Independently rerunnable | Data or controlled-access data, code/toolchain, preprocessing steps, split design, and primary metrics are sufficient for a third party to rerun the main analysis. |
| R4 | Externally validated and reusable | Meets R3 and includes external cohort/site/language/device validation or independent replication, with reuse documentation. |
| R_pending | Pending | Full text or supplement has not yet been checked. |

## Risk-of-Bias Domains

Code each domain as `low_concern`, `some_concern`, `high_concern`, `not_reported`, or `not_applicable`.

Domains are grouped by their PROBAST parent domain, so a reviewer familiar with PROBAST can locate each item.

| Domain | PROBAST parent | Low concern signal | High concern signal |
|---|---|---|---|
| participant_selection | Participants | Target population, recruitment, inclusion/exclusion, and case/control comparability are clear. | Convenience sample, unclear recruitment, unmatched controls, or strong spectrum bias. |
| reference_standard | Outcome | Diagnosis, clinical endpoint, biological-age comparator, or severity scale is clinically meaningful and well described. | Self-report-only label, unclear label source, circular label, or weak proxy treated as ground truth. |
| recording_protocol | Predictors | Task, device/microphone, environment, language, and collection procedure are documented. | Recording conditions not reported or differ systematically by class/site. |
| leakage_control | Analysis | Subject/session/site separation and preprocessing fit are explicitly controlled. | Speaker/session overlap, split not reported, or normalization/feature selection done before split. |
| validation_design | Analysis | Independent test set, nested CV, external validation, or longitudinal validation is appropriate to the claim. | Training performance only, non-independent CV, or no held-out evaluation. |
| statistical_reporting | Analysis | Effect sizes, uncertainty, calibration, and multiple-testing handling are reported where relevant. | Accuracy-only reporting, no CI, no calibration, no adjustment for multiple comparisons. |
| confounding_control | Analysis | Age, sex/gender, language/accent, severity, comorbidity, medication, site, and device are considered. | Main claim plausibly explained by one or more uncontrolled confounders. |
| subgroup_generalization | Analysis | Subgroup, fairness, language, site, or demographic performance is reported when relevant. | No subgroup reporting despite heterogeneous population or deployment claim. |
| missing_data_qc | Analysis | Missing recordings, excluded samples, QC thresholds, and failed recordings are reported. | Exclusions or recording-quality filters are hidden or post hoc. |
| reproducibility_assets | Reporting (TRIPOD+AI) | Data/code/preprocessing/model assets are available or controlled-access route is clear. | No data, no code, no feature definitions, no model details. |
| conflict_of_interest | Reporting (TRIPOD+AI) | Funding and conflicts are reported and do not dominate interpretation. | Undisclosed or strong commercial conflict with weak independent validation. |

## Overall Judgment

Assign an overall evidence concern:

- `low_concern`: no high-concern domains and reproducibility level R3/R4, or strong clinical validation with transparent limitations.
- `some_concern`: one or more not-reported domains, no fatal leakage, reproducibility R1/R2.
- `high_concern`: likely leakage, invalid reference standard, severe confounding, or no independent validation for a strong clinical claim.
- `background_only`: useful for terminology, dataset context, or citation chaining but not a direct evidence source.

## Extraction Rule

Facts must be tied to source location. Inferences must be explicitly labeled as reviewer inference. Recommendations must not be mixed with extracted facts.
