# Author Style Note: Abdalla Z. Mohamed

Date checked: 2026-06-17

## Identity

The relevant author appears to be Abdalla Z. Mohamed, not "Abdalla Muhammed".

Source basis:

- UAEU research profile: Abdalla Mohamed, Assistant Professor, Department of Cognitive Sciences. https://research.uaeu.ac.ae/en/persons/abdalla-mohamed/
- NYU Abu Dhabi news item on ASPIRE dataset: names Abdalla Z. Mohamed as lead author and Assistant Professor at UAEU Department of Cognitive Sciences. https://nyuad.nyu.edu/en/news/latest-news/science-and-technology/2026/february/brain-dataset-adds-research-potential.html
- ORCID: 0000-0003-4499-672X.
- Europe PMC confirms NYU Abu Dhabi and UAEU affiliations on the 2026 ASPIRE data paper.

## Review-Relevant Publications

### Systematic Review / Meta-Analysis

Mohamed AZ, Andersen T, Radovic S, Del Fante P, Kwiatek R, Calhoun V, Bhuta S, Hermens DF, Lagopoulos J, Shan ZY. Objective sleep measures in chronic fatigue syndrome patients: A systematic review and meta-analysis. Sleep Medicine Reviews. 2023;69:101771. DOI: 10.1016/j.smrv.2023.101771.

Observed structure:

- Starts from a clinically specific contradiction: ME/CFS patients report sleep disruption, but objective sleep studies are inconsistent.
- Narrows the evidence base to case-control studies with objective sleep measures.
- Searches PubMed, Scopus, Medline, Google Scholar, and PsycInfo.
- Separates adults and adolescents in synthesis rather than pooling heterogeneous populations blindly.
- Reports included counts directly in abstract: 24 studies total; 20 adult studies with 801 adults; 4 adolescent studies with 477 adolescents.
- Uses meta-analysis when measures are comparable.
- Converts heterogeneous sleep measures into interpretable physiological claims: altered sleep architecture and possible sympathetic/parasympathetic nervous-system involvement.
- Publishes in a specialized review journal, Sleep Medicine Reviews.

### Method / Atlas Paper With Review-Like Elements

Mohamed AZ, Kwiatek R, Del Fante P, Calhoun VD, Lagopoulos J, Shan ZY. Functional MRI of the Brainstem for Assessing Its Autonomic Functions: From Imaging Parameters and Analysis to Functional Atlas. Journal of Magnetic Resonance Imaging. 2024;60(5):1880-1891. DOI: 10.1002/jmri.29286.

Observed structure:

- Uses a structured clinical-imaging abstract: Background, Purpose, Study Type, Subjects, Field Strength/Sequence, Assessment, Statistical Tests, Results, Data Conclusion, Evidence Level, Technical Efficacy.
- Frames the paper around a technical bottleneck: brainstem fMRI is hard because protocols, analysis, and interpretation vary.
- Benchmarks protocols and preprocessing pipelines rather than only narrating the field.
- Combines meta-analysis/literature-derived ROI logic with data-driven validation.
- Ends with technical efficacy staging, making translational maturity explicit.

### Dataset / Infrastructure Paper

Mohamed AZ et al. The ASPIRE Research Institute Dataset: Building a Foundation for Brain Health Research in the United Arab Emirates. Scientific Data. 2026;13:186. DOI: 10.1038/s41597-025-06498-0.

Observed structure:

- Opens with a regional evidence gap: UAE/MENA lack large, controlled normative neuroimaging datasets.
- Makes the contribution infrastructural: cohort design, acquisition protocol, data management, preprocessing workflows, documentation, and OSF data access.
- Reports target cohort and released sample concretely: 1000 Emirati citizens, 1000 non-Emirati residents, initial 41 participants.
- Uses reproducibility and reuse as the main selling point.
- The NYUAD public summary emphasizes dataset documentation, preprocessing workflows, and reproducible regional brain-health infrastructure.

## Methods and Reproducibility Pattern

### Systematic review / meta-analysis methods

In the ME/CFS sleep review, Mohamed's group uses a formal systematic-review design rather than a narrative scan:

- PECO framing for Population, Exposure, Comparison, and Outcome.
- PRISMA reporting.
- Prospective registration on PROSPERO: CRD42021262494.
- Database search in PubMed, Scopus, Medline, and PsycInfo for January 1990 to April 2021.
- Supplementary full search terms per database.
- Additional Google Scholar search on 2022-05-10 for "chronic fatigue syndrome" and "objective sleep", limited to 10 result pages.
- Backward checking of prior systematic reviews and relevant original/review article reference lists.
- Deduplication in EndNote.
- Explicit inclusion criteria: English, peer-reviewed, original data, accepted ME/CFS diagnostic criteria, age-matched controls, overnight sleep measurement, objective sleep measures.
- Extraction of study metadata, diagnostic criteria, sample sizes, demographics, sleep measurement tool, analysis method, observations, conclusions, and sleep variables.
- Duplicate-sample protection: studies sharing an author were checked for overlapping samples and excluded if judged similar.

Reproducibility checks in that review:

- PRISMA flow: 2181 identified records, 998 after duplicates, 47 full ME/CFS sleep articles, 24 included in meta-analysis.
- Supplementary tables for included studies and exclusion reasons.
- Risk of bias assessed with an adapted QUADAS-2 tool across patient selection, index test, control standard, and confounding control.
- Random-effects meta-analysis in RevMan 5.4.1.
- Mean difference and standardized mean difference estimates with 95% CI.
- Heterogeneity quantified using I-squared and interpreted by pre-specified thresholds.
- Subgroup analyses split by age group and by measurement method, especially PSG vs actigraphy.
- Publication bias was planned with Egger-style logic, but they explicitly report that it could not be evaluated reliably because of missing information and poor protocol reporting in many primary studies.

### Technical benchmarking / atlas methods

In the brainstem fMRI paper, the method is not a review-only workflow. It is a small prospective technical validation study plus literature-informed atlas construction:

- Prospective cross-sectional design.
- Ten healthy subjects.
- 3T MRI acquisition.
- Comparison of three fMRI protocols: optimized FIBS, HCP, and ABCD.
- Quantitative protocol metric: temporal signal-to-noise ratio (TSNR).
- Comparison of normalization algorithms: FSL-FNIRT, SPM-DARTEL, and ANTs-SyN.
- Quantitative preprocessing metric: RMS error from manually defined reference points.
- Functional brainstem atlas built using meta-analysis and data-driven approaches.
- Statistical comparison with ANOVA and multiple-comparison correction.
- ROI agreement checked with Dice coefficient, with 50% overlap treated as significant.
- Maturity reported as Evidence Level 2 and Technical Efficacy Stage 1.

Reproducibility checks in that paper:

- Competing protocols and competing normalization algorithms are benchmarked explicitly.
- The validation criteria are numerical, not narrative: TSNR, RMS error, Dice overlap.
- The atlas is only accepted where literature-derived and data-driven ROI evidence overlaps.
- The paper states translational maturity with technical-efficacy staging, which prevents overclaiming clinical readiness.

### Dataset / infrastructure methods

In the ASPIRE Scientific Data paper, reproducibility is the main contribution:

- A prospective regional normative dataset design for 1000 Emirati citizens and 1000 non-Emirati residents aged 18-60.
- Initial release of 41 participants.
- Standardized protocol: consent, MRI safety screening, demographic assessment, MRI session, behavioral assessment.
- Single-scanner acquisition to reduce site confounding.
- BIDS data organization.
- XNAT repository and high-performance-computing integration for standardized preprocessing.
- MRIQC for individual and project-level quality reports.
- Visual inspection by trained researchers before preprocessing.
- Structural preprocessing with fMRIPrep anatomical steps, FSL-FAST, FreeSurfer recon-all, Mindboggle, and MNI normalization.
- fMRI preprocessing with fMRIPrep and FSL-topup, motion correction, skull stripping, co-registration, resampling, and denoising strategies.
- Data deposited on OSF: 10.17605/OSF.IO/BNXSJ.
- Code availability is handled through public/open-source processing tools: DCM2BIDS, MRIQC, fMRIPrep, MRtrix3, FSL, FreeSurfer, Tractflow, TractSeg, and XNAT.

Reproducibility checks in that paper:

- Raw data release on OSF.
- BIDS standardization.
- Public toolchain.
- Quality control with MRIQC metrics and human visual inspection.
- Explicit data access and sharing notes under UAE data-sharing constraints.
- Documentation of protocol, acquisition, data management, preprocessing, and usage notes.

## What This Means for Our Voice-Biomarkers Review

The transferable pattern is: define a strict review question, document the search completely, stratify heterogeneity before synthesis, and make reproducibility a measured outcome.

For the voice-biomarkers review, the Mohamed-style method would require:

- PECO/PICOS framing for each clinical/population/task stratum.
- PRISMA reporting and prospective registration if possible.
- Full database-specific search strings in supplementary material.
- Machine-readable screening log with deduplication, exclusion reasons, and seed-paper false-negative audit.
- Extraction of recording protocol, task, language, device, acoustic environment, feature pipeline, model type, training/test split, external validation, data/code availability, and clinical endpoint.
- Risk-of-bias and applicability assessment adapted for diagnostic/prognostic ML, not just generic biomedical study bias.
- Quantitative synthesis only inside narrow comparable strata; otherwise evidence maps and validation-maturity tables.
- Separate reproducibility scoring for data, code, preprocessing, model validation, external validation, and population/language transportability.

## Style Lessons for Voice Biomarkers Review

1. Frame the paper around a precise contradiction or gap, not a broad topic. For voice biomarkers: many voice-health models exist, but validation, task comparability, population coverage, and generalization remain inconsistent.
2. Split heterogeneous populations before synthesis. Do not pool aging, neurological disease, psychiatry, pediatrics, respiratory, and cardiovascular papers as one evidence class.
3. Put search scope and included counts early. Mohamed-style abstracts make numbers visible.
4. Treat protocol and preprocessing choices as evidence, not background. For voice biomarkers this means recording task, device, environment, language, and feature/model family are core extraction variables.
5. Make validation maturity explicit. Use verification, analytical validation, clinical validation, external validation, longitudinal validation, and clinical utility as primary axes.
6. If the field is too heterogeneous for one meta-analysis, present an evidence map plus targeted quantitative summaries where measures are comparable.
7. Use reproducibility as a contribution: search logs, candidate exports, screening decisions, extraction provenance, seed false-negative audit, and machine-readable tables.

## Implication

For our voice-biomarkers manuscript, the closest emulation is not a narrative overview. It is a staged systematic mapping review with domain-stratified synthesis, transparent counts, and technical validation axes. The Abdalla Z. Mohamed model suggests writing the review as a methodologically constrained evidence map that can later support narrower meta-analyses, not as a broad essay on the promise of vocal biomarkers.
