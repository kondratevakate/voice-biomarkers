# Voice-Derived Biomarkers Across Populations and Tasks: A Systematic Mapping Review

Status: preliminary synthesis of abstract-level includes
Date: 2026-09-01

## Abstract

Voice and speech are increasingly proposed as scalable digital biomarkers across
neurological, psychiatric, respiratory, cardiovascular, and aging phenotypes. We
map this evidence base by population, elicitation task, modeled outcome, and
validation maturity, reporting against PRISMA-ScR with PRISMA-S search
reporting. This document reports a preliminary synthesis of 94 abstract-level
includes drawn from an open-index search; it is not the final included-study
set. Two findings are already stable enough to state. First, the evidence base
is concentrated: 72% of includes concern neurology and cognition, while
metabolic (3%) and pediatric (2%) work is nearly absent. Second, and more
consequentially, external validation is reported in 5 of 94 records (5%), and
all but three of those sit in neurology; psychiatry, respiratory,
cardiovascular, aging, and metabolic work contribute **zero** externally
validated records. A field that is 81% published since 2022 has not yet
demonstrated that its measures transfer.

## Introduction

Voice and speech are low-cost, repeatable signals that may encode information
about aging, neurological function, respiratory physiology, mental health,
laryngeal function, and cardiometabolic state. The field is fragmented across
clinical domains, elicitation tasks, languages, model families, and validation
standards.

This review maps the evidence base across populations and tasks and evaluates
the maturity of voice-derived biomarkers. It positions itself against prior
overlapping syntheses rather than alongside them. Hecker et al. (2022,
doi:10.3389/fdgth.2022.842301) mapped voice analysis for neurological disorder
recognition across PubMed, Web of Science, and IEEE Xplore, cataloguing 43
newly collected datasets and their recording practices. Two systematic reviews
cover machine learning for Parkinson's disease from speech specifically. This
review differs in three ways: it is not restricted to neurological conditions;
it treats validation maturity and reproducibility as mapped outcomes rather
than as quality filters applied at screening; and it covers dataset and
foundation-model infrastructure alongside empirical studies.

## Methods

See `../protocol.md`. Quality and reproducibility assessment follows V3
(Goldsack et al., 2020), PROBAST (Wolff et al., 2019), and TRIPOD+AI (Collins
et al., 2024), adapted for audio-specific failure modes in
`../governance/reproducibility-risk-of-bias-rubric.md`. Full-text extraction
uses `../screening/full-text-extraction-template.csv`.

## Results

### Search and Selection

PRISMA-ScR counts are reported in `../sources/search-log.md` and are not
reproduced here until full-text screening completes. The synthesis below rests
on 94 records that passed abstract-level screening from a stratified but
incomplete search. **These 94 are not a random sample of the field**, and the
direction of their bias is known and documented: they were drawn only from
PubMed and Europe PMC preprint buckets, and abstract-level inclusion was
assisted by a keyword list that named specific diseases. Both defects are
corrected in the current search and screening code, so the numbers below should
be read as a lower bound on concentration and an upper bound on validation
maturity.

### Evidence Map: What the Field Has Studied

| Domain | Records | Share |
|---|---|---|
| Neurology and cognition | 68 | 72% |
| Aging and frailty | 19 | 20% |
| Psychiatry | 18 | 19% |
| Respiratory | 16 | 17% |
| General framework or methods | 15 | 16% |
| Cardiovascular | 13 | 14% |
| Metabolic | 3 | 3% |

Tags are multi-label and do not sum to 94. Pediatric work appears in 2 records.

The concentration in neurology and cognition is the field's dominant structural
feature. It is partly genuine — Parkinson's disease and Alzheimer's disease
offer motor-speech and language-production mechanisms that plausibly link
pathology to acoustics — and partly an artefact of dataset availability, since
the shared benchmarks that let groups compete are overwhelmingly neurological.
The near-absence of metabolic and pediatric work is the clearest gap the map
identifies.

### Validation Maturity: What the Field Has Shown

| Validation tag | Records | Share |
|---|---|---|
| Not determinable from abstract | 37 | 39% |
| Clinical validation | 33 | 35% |
| Longitudinal | 12 | 13% |
| Prospective | 10 | 11% |
| Analytical validation | 8 | 9% |
| **External validation** | **5** | **5%** |
| Retrospective | 2 | 2% |

External validation by domain:

| Domain | Externally validated | Records |
|---|---|---|
| Neurology and cognition | 3 | 68 |
| Psychiatry | 0 | 18 |
| Respiratory | 0 | 16 |
| Cardiovascular | 0 | 13 |
| Aging and frailty | 0 | 19 |
| Metabolic | 0 | 3 |

This is the review's central finding. Ninety-five percent of records carry the
preliminary flag `no_external_validation_mentioned`. Whole clinical domains —
psychiatry, respiratory medicine, cardiology, aging — contribute no record in
which a voice measure was shown to hold on an independent cohort, site,
language, or device. In V3 terms, the field has produced a large volume of
clinical-validation claims resting on very little analytical validation, and
almost no evidence of transportability.

A second observation compounds this. Elicitation task is not recoverable from
the abstract in any of the 94 records: 100% are tagged
`unspecified_voice_audio`, and where a modality is inferable it is usually only
that a smartphone was used (69%). Since the acoustic consequences of a sustained
vowel, read speech, and spontaneous conversation differ substantially, a
literature that does not state its task in the abstract cannot be compared
across studies without full-text extraction — and cannot be replicated at all
where the full text is equally silent.

### Recency

Eighty-one percent of includes were published in 2022 or later (2022: 16, 2023:
17, 2024: 17, 2025: 18, 2026: 8). The field is young enough that the absence of
external validation may reflect immaturity rather than neglect. That reading is
testable: if the 2022 cohort still lacks replication by 2027, the explanation is
not youth.

### Theme 1: Aging and Longitudinal Voice Change

Nineteen records touch aging or frailty, but only two carry an age or aging
construct in the title, and none of the 19 report external validation. The
strongest infrastructure signal comes from outside the screened set: longitudinal
corpora such as VoxKnesset (2,300 hours of Hebrew parliamentary speech, 393
speakers, spans to 15 years) show that cross-sectionally trained age regressors
fail to capture within-speaker aging, and that speaker-verification error rises
from 2.15% to 4.58% across 15 years. This is a direct warning to any
cross-sectional voice-age model that claims to measure biological aging.

### Theme 2: Neurological and Cognitive Biomarkers

The largest and most methodologically developed stratum, and the only one with
any external validation (3 of 68). Full-text calibration material in this
stratum illustrates the field's typical design: a prospective case-control
comparison of 63 Parkinson's patients against 35 controls using sustained
vowels and formant-derived metrics, with the clinically interesting claim being
detection of *subclinical* dysarthria. Such designs are informative about
mechanism but do not establish screening performance in an unselected
population.

### Theme 3: Mental Health and Affective State

Eighteen records, zero externally validated. This stratum carries the field's
sharpest known confound: speaker identity. Recent work explicitly frames the
problem as "who is speaking or who is depressed," and speaker leakage is the
mechanism by which apparently strong within-corpus depression classifiers fail
to transfer.

### Theme 4: Respiratory, Laryngeal, and Cardiometabolic Signals

Respiratory (16) and cardiovascular (13) work is dominated by prospective
cohort designs with plausible physiological mechanisms — a smartphone
respiratory-responsive vocal biomarker tracked daily across 84 asthma patients,
vocal biomarkers in heart failure and in incident coronary artery disease. None
report external validation. A concentration risk applies here: several
cardiovascular records derive from one institutional programme and one
commercial technology, so this stratum's apparent breadth may overstate the
number of independent findings.

### Theme 5: Dataset Infrastructure and Foundation Models

No record among the 94 carries a dataset, corpus, benchmark, or foundation-model
construct in its title, despite this being a declared stratum. This is a
retrieval failure rather than a field-level absence: the layer exists, but lives
at ISCA, IEEE, and ACL venues that the Stage 1 and Stage 2 searches did not
cover. Foundation models for clinical voice are being proposed — one contrastive
model aligning audio embeddings with clinical metadata reports mean AUROC 0.952
across five tasks and 0.99 for Alzheimer's, dementia and MCI on a 138-participant
held-out cohort — and these claims are precisely the ones a validation-focused
map must scrutinise, since a held-out cohort drawn from the same five medical
centres tests generalisation to new participants but not to new sites, devices,
or languages.

### Theme 6: Validation, Generalization, and Equity

Treated as an outcome rather than a theme; see the validation maturity section.
Equity and subgroup reporting could not be assessed from abstracts and is
deferred to full-text extraction.

## Discussion

The field's problem is not whether voice carries health-relevant signal. It
does, across many physiological systems, and the abstract-level literature is
now large and growing quickly. The problem is that the evidence is
overwhelmingly *within-corpus*. Five of 94 records claim external validation,
and outside neurology that count is zero. Meanwhile, the two structural
prerequisites for cross-study comparison — a stated elicitation task and a
stated recording setup — are absent from every abstract screened.

This has a practical consequence for anyone entering the field: published
performance figures are not comparable across studies and should not be pooled.
The correct unit of appraisal is not the reported AUROC but the design that
produced it, and specifically whether speakers, sessions, and sites were
separated.

It also has a consequence for regulators and for anyone planning translation.
None of the screened records reports the kind of evidence that a fit-for-purpose
determination under V3 requires: verification of the measurement chain,
analytical validation across devices and environments, and clinical validation
in the intended-use population. The field currently reports the third without
the first two.

## Limitations

This synthesis rests on abstract-level tags from a non-random subset of an
incomplete search, and the direction of every known bias is documented in
`../sources/search-log.md` and `../governance/protocol-deviation-log.csv`. In
particular: engineering venues were absent from the search that produced these
94 records, so Theme 5 is under-observed by construction; abstract-level
validation tags will change under full-text extraction, and the 39% "not
determinable" category may resolve in either direction; and the disease mix was
partly shaped by a keyword list that named specific diseases, so the 72%
neurology share should be read as an upper bound.

Reproducibility maturity (R0-R4) has not been assigned to any record, because
full-text extraction has not been performed.

## Conclusion

Voice-derived biomarkers are a fast-growing, neurology-dominated literature in
which almost nothing has been shown to transfer. The most useful contribution a
mapping review can make at this moment is not another catalogue of reported
accuracies but an explicit account of what has and has not been validated, and
of the reporting gaps — elicitation task, device, speaker separation — that
prevent the field from checking its own claims.

## References

See `../references.bib`. All 22 entries verified against Crossref and arXiv.
