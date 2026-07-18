# Reproducibility and Risk-of-Bias Rubric

Date: 2026-06-17
Status: required for full-text extraction

## Purpose

This rubric operationalizes the Mohamed-style reproducibility pattern for the voice-biomarkers review. It should be applied during full-text extraction to all empirical studies, dataset papers, benchmark papers, and model papers.

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

| Domain | Low concern signal | High concern signal |
|---|---|---|
| participant_selection | Target population, recruitment, inclusion/exclusion, and case/control comparability are clear. | Convenience sample, unclear recruitment, unmatched controls, or strong spectrum bias. |
| reference_standard | Diagnosis, clinical endpoint, biological-age comparator, or severity scale is clinically meaningful and well described. | Self-report-only label, unclear label source, circular label, or weak proxy treated as ground truth. |
| recording_protocol | Task, device/microphone, environment, language, and collection procedure are documented. | Recording conditions not reported or differ systematically by class/site. |
| leakage_control | Subject/session/site separation and preprocessing fit are explicitly controlled. | Speaker/session overlap, split not reported, or normalization/feature selection done before split. |
| validation_design | Independent test set, nested CV, external validation, or longitudinal validation is appropriate to the claim. | Training performance only, non-independent CV, or no held-out evaluation. |
| statistical_reporting | Effect sizes, uncertainty, calibration, and multiple-testing handling are reported where relevant. | Accuracy-only reporting, no CI, no calibration, no adjustment for multiple comparisons. |
| confounding_control | Age, sex/gender, language/accent, severity, comorbidity, medication, site, and device are considered. | Main claim plausibly explained by one or more uncontrolled confounders. |
| subgroup_generalization | Subgroup, fairness, language, site, or demographic performance is reported when relevant. | No subgroup reporting despite heterogeneous population or deployment claim. |
| missing_data_qc | Missing recordings, excluded samples, QC thresholds, and failed recordings are reported. | Exclusions or recording-quality filters are hidden or post hoc. |
| reproducibility_assets | Data/code/preprocessing/model assets are available or controlled-access route is clear. | No data, no code, no feature definitions, no model details. |
| conflict_of_interest | Funding and conflicts are reported and do not dominate interpretation. | Undisclosed or strong commercial conflict with weak independent validation. |

## Overall Judgment

Assign an overall evidence concern:

- `low_concern`: no high-concern domains and reproducibility level R3/R4, or strong clinical validation with transparent limitations.
- `some_concern`: one or more not-reported domains, no fatal leakage, reproducibility R1/R2.
- `high_concern`: likely leakage, invalid reference standard, severe confounding, or no independent validation for a strong clinical claim.
- `background_only`: useful for terminology, dataset context, or citation chaining but not a direct evidence source.

## Extraction Rule

Facts must be tied to source location. Inferences must be explicitly labeled as reviewer inference. Recommendations must not be mixed with extracted facts.
