# Search Strategy

Date: 2026-06-05
Status: protocol component, pre-formal-search
Method basis: K-Dense `literature-review`, `paper-lookup`, `citation-management`; Mohamed-style reproducibility pattern; AI-scientist governance critique.
Tooling basis: see `tooling-assessment.md`; prefer ToolUniverse literature tools for execution when available.

## Review Aim

Systematically map evidence for voice-derived biomarkers across populations, elicitation tasks, modeled outcomes, and validation maturity.

## Formal Review Conditions

The formal search must be reproducible enough for another reviewer to re-run it from the repository. A search pass is formal only if all of the following are recorded:

- database or index name
- exact query string in database-specific syntax
- date and timezone of search
- filters, language constraints, document-type constraints, and date window
- raw result count before deduplication
- raw export filename
- parsed candidate filename
- deduplication rule
- operator/tool and script hash or git SHA
- known-relevant seed retrieval result

Broad web search, Google Scholar-style discovery, and AI-agent browsing can be used for sensitivity checks and citation chasing, but they are not formal PRISMA-count sources unless result pages, queries, dates, and candidate exports are preserved.

Formal screening decisions cannot be delegated to an agent. Automated labels can only pre-sort records; final title/abstract/full-text decisions require manual confirmation or documented adjudication.

## Core Search Concepts

The search combines three concept blocks:

1. Audio signal: voice, vocal, speech, speech-language, acoustic, cough, breathing.
2. Biomarker framing: biomarker, digital biomarker, vocal biomarker, speech biomarker, voice-derived biomarker, digital phenotype.
3. Health/aging task: aging, biological age, clinical, disease, diagnosis, screening, monitoring, prognosis, severity, treatment response, risk.

## Databases To Search

| Source | Include in formal search? | Why |
|---|---:|---|
| PubMed | Yes | Main biomedical index; best for clinical populations, disease biomarkers, validation studies, reviews. Execute via PubMed E-utilities or ToolUniverse `PubMed_search_articles`. |
| Europe PMC | Yes | Best route for biomedical full text and keyword search over medRxiv/bioRxiv preprints. Execute via ToolUniverse `EuropePMC_search_articles`. |
| PubMed Central / PMC | Yes | Full-text biomedical access; useful for reference mining and extracting methods/limitations. Access through Europe PMC/PMC links. |
| medRxiv | Yes | Captures recent clinical preprints, especially 2025-2026 vocal biomarker work. Discover through Europe PMC `source:PPR` or web search; retrieve exact DOI metadata after discovery. |
| bioRxiv | Yes | Captures biology/neuroscience preprints and speech/cognition biomarker studies. Discover through Europe PMC `source:PPR` or web search; retrieve exact DOI metadata after discovery. |
| arXiv | Yes | Captures speech processing, ML, dataset, foundation-model, and benchmark papers. Execute via arXiv API or ToolUniverse `ArXiv_search_papers`. |
| OpenAlex | Yes | Broad scholarly index; useful for deduplication, citation counts, and cross-domain discovery. Execute via OpenAlex API or ToolUniverse `openalex_literature_search`. |
| Semantic Scholar | Yes, if API permits | Useful for citation graph, influential papers, and cross-disciplinary retrieval. Prefer API key to avoid rate limits. |
| Crossref | Verification only | Too noisy for broad discovery; use for DOI/title metadata verification and published-version checks. |
| Unpaywall | Verification only | Use for open-access full text after candidate set is built. |
| Google Scholar-style broad web search | Supplementary | Helps catch missed preprints, reports, and newly indexed pages; not sole source for PRISMA counts unless exportable. |

Minimum acceptable formal search set:

- PubMed
- Europe PMC with preprint filter for medRxiv/bioRxiv discovery
- arXiv
- OpenAlex or Semantic Scholar

Crossref and Unpaywall are downstream verification tools, not primary discovery databases.

## Database Execution Status Categories

Every database must be assigned one of these statuses in the final Methods and in `sources/search-log.md`:

- `pending`: required source not yet searched or resolved.
- `searched_exported`: searched directly and raw export saved.
- `searched_no_export`: searched directly but no export function was available; screenshots or result-page logs required.
- `supplementary_only`: used for sensitivity search or citation chasing, not PRISMA counts.
- `access_unavailable`: not searched because institutional/subscription access was unavailable.
- `api_failed`: attempted but blocked by API error, rate limit, or timeout.
- `not_applicable`: excluded with explicit methodological reason.

Databases that are important for field coverage, especially Embase, Scopus, Web of Science, IEEE Xplore, ACM Digital Library, ACL Anthology, ISCA Archive, CNKI, Wanfang, VIP, SinoMed, ClinicalTrials.gov, WHO ICTRP, and EU Clinical Trials Register, cannot disappear from reporting. They must be searched or logged as unavailable/failed.

## Eligibility Conditions

### Inclusion

- Human participants or human voice/speech/audio datasets.
- Audio-derived feature, representation, model, or score is used as a biomarker, digital biomarker, clinical marker, proxy marker, screening marker, monitoring marker, prognostic marker, or aging marker.
- Study reports at least one extractable empirical element: sample, task, feature/model, outcome, comparator/reference standard, association, benchmark, or validation result.
- Accepted study types:
  - observational studies
  - diagnostic/prognostic modeling studies
  - longitudinal monitoring studies
  - clinical validation or analytical validation studies
  - dataset/benchmark papers with biomarker-relevant tasks
  - systematic/scoping reviews for background and citation chaining
  - preprints, clearly labeled as not peer-reviewed
- Any age group, sex/gender, language, country, recording device, or recording environment.
- English-language records for the formal first pass. Non-English records can be logged as `awaiting translation` if title/abstract suggests high relevance.

### Exclusion

- Pure ASR, speaker identification, speech enhancement, diarization, or NLP papers with no health, aging, disease, or biomarker claim.
- Voice pedagogy, singing technique, theater voice, vocal training, or generic speech communication papers without health biomarker relevance.
- Animal vocalization studies.
- Commercial product pages or marketing claims without methods/results.
- Opinion/editorial pieces without definitions, framework, or usable references.
- Studies where voice is only an interface channel and not analyzed as the signal.

## Time Window

Primary search: no date restriction.

Rationale: older speech/acoustic biomarker studies, Parkinson's disease voice studies, depression voice markers, and acoustic feature sets may be foundational.

Sensitivity analysis/reporting:

- Mark records from 2020 onward as `modern ML/digital biomarker era`.
- Mark records before 2020 as `foundational/pre-modern`.

## Query Families

Do not rely on one broad query. Run separate query families and deduplicate.

### Family A: Core Terminology

Purpose: capture papers explicitly naming the field.

```text
("voice biomarker" OR "vocal biomarker" OR "speech biomarker" OR "speech-based digital biomarker" OR "voice-derived digital biomarker" OR "speech-derived digital biomarker")
```

### Family B: Clinical Validation

Purpose: capture validation and clinical-translation papers.

```text
("voice" OR "vocal" OR "speech" OR "acoustic")
AND ("digital biomarker" OR biomarker OR "digital phenotype")
AND ("clinical validation" OR "analytical validation" OR "external validation" OR "longitudinal validation" OR "clinical utility")
```

### Family C: Aging and Biological Age

Purpose: capture the two seed papers' neighborhood.

```text
("voice age" OR "vocal aging" OR "speech aging" OR "voice-based biological clock" OR "voice-predicted age" OR "vocal age acceleration")
AND (biomarker OR "biological age" OR aging OR longitudinal)
```

### Family D: Disease Detection and Monitoring

Purpose: capture condition-specific biomarker models.

```text
("voice" OR "vocal" OR "speech" OR "acoustic")
AND (biomarker OR "digital biomarker" OR screening OR monitoring OR diagnosis OR prognosis OR severity)
AND (Parkinson* OR Alzheimer* OR dementia OR depression OR anxiety OR schizophrenia OR "heart failure" OR asthma OR COPD OR respiratory OR ALS OR "motor neuron disease" OR frailty OR cardiometabolic)
```

Formal-search note, 2026-06-05: this broad query is too noisy for direct screening. Use it only as a sensitivity layer. The primary disease search should be split into domain-specific subqueries and should require both a voice/speech term and a biomarker term.

Refined disease-domain template:

```text
(voice OR vocal OR speech OR acoustic)
AND (biomarker OR "digital biomarker" OR "vocal biomarker" OR "speech biomarker" OR "voice biomarker")
AND (<domain terms>)
```

Domain term sets:

- neurological: Parkinson* OR Alzheimer* OR dementia OR ALS OR "motor neuron disease"
- psychiatric: depression OR anxiety OR schizophrenia OR psychosis
- cardiovascular: "heart failure" OR "coronary artery disease" OR "pulmonary hypertension"
- respiratory: asthma OR COPD OR respiratory OR cough OR tuberculosis
- aging/metabolic: frailty OR cardiometabolic OR diabetes OR "biological age"

### Family E: Tasks, Datasets, and Foundation Models

Purpose: capture ML/speech-processing work that may not use clinical indexing terms.

```text
("clinical voice" OR "health voice" OR "medical speech" OR "speech health" OR "voice foundation model" OR "speech foundation model")
AND (biomarker OR disease OR aging OR clinical OR health OR dataset OR benchmark)
```

## PubMed Search Syntax

Use title/abstract for specificity, then optionally expand with MeSH terms.

```text
("voice biomarker"[Title/Abstract] OR "vocal biomarker"[Title/Abstract] OR "speech biomarker"[Title/Abstract] OR "speech-based digital biomarker"[Title/Abstract] OR "voice-derived digital biomarker"[Title/Abstract])
AND
(human[Title/Abstract] OR clinical[Title/Abstract] OR health[Title/Abstract] OR disease[Title/Abstract] OR aging[Title/Abstract] OR Humans[MeSH Terms])
```

Expanded clinical query:

```text
(voice[Title/Abstract] OR vocal[Title/Abstract] OR speech[Title/Abstract] OR acoustic[Title/Abstract])
AND
(biomarker[Title/Abstract] OR "digital biomarker"[Title/Abstract] OR "digital phenotype"[Title/Abstract])
AND
(diagnosis[Title/Abstract] OR screening[Title/Abstract] OR monitoring[Title/Abstract] OR prognosis[Title/Abstract] OR validation[Title/Abstract] OR aging[Title/Abstract] OR disease[Title/Abstract])
AND
Humans[MeSH Terms]
```

## arXiv Search Syntax

Run narrower searches because broad `voice AND biomarker` can fail or return unrelated speech papers.

```text
ti:"voice biomarker" OR abs:"voice biomarker"
```

```text
ti:"vocal biomarker" OR abs:"vocal biomarker"
```

```text
("clinical voice" OR "medical speech" OR "voice foundation model")
AND (biomarker OR health OR disease OR aging)
```

Relevant arXiv categories:

- eess.AS
- eess.SP
- cs.CL
- cs.LG
- cs.SD
- stat.ML
- q-bio.QM

## medRxiv/bioRxiv Strategy

Because official bioRxiv/medRxiv APIs do not support keyword search, use:

- DOI lookup for known seed papers.
- Europe PMC keyword search with preprint filter for discovery.
- Date-window browsing for recent preprints only as a supplementary check.
- Broad academic web queries restricted to `medrxiv.org` and `biorxiv.org`.
- Crossref exact-title lookup to check later publication status.

ToolUniverse-recommended query pattern:

```python
EuropePMC_search_articles(query="<query family>", source="PPR", pageSize=100)
```

After DOI discovery:

```python
BioRxiv_get_preprint(doi="<doi>", server="medrxiv" or "biorxiv")
```

Example web-restricted queries:

```text
site:medrxiv.org ("voice biomarker" OR "vocal biomarker" OR "speech biomarker")
```

```text
site:medrxiv.org ("voice age" OR "voice-based biological clock" OR "clinical voice biomarkers")
```

## OpenAlex / Semantic Scholar Strategy

Use them as broad discovery and citation graph sources, but not with one unfiltered query.

Recommended approach:

- Run each query family separately.
- Export top 100 per family.
- Keep citation counts and publication year.
- Deduplicate before screening.
- Use citation chaining from included reviews and seed papers.

## Deduplication Rules

Deduplicate in this order:

1. DOI.
2. PMID/PMCID.
3. arXiv ID.
4. medRxiv/bioRxiv DOI.
5. Normalized title.

If a preprint has a peer-reviewed version:

- Keep both records during screening.
- Prefer the peer-reviewed version for synthesis.
- Record the preprint as linked prior version.

## Screening Rules

Stage 1: title screening.

- Include if clearly voice/speech/audio + health/aging/biomarker.
- Exclude if clearly pedagogy, singing, theater, pure ASR, or non-health.
- Mark `maybe` if only one concept block is obvious.

Stage 2: abstract screening.

- Require human data or human-relevant dataset.
- Require audio-derived signal as the object of analysis.
- Require extractable outcome/comparator/validation information.

Stage 3: full-text screening.

- Confirm population, task, model/feature, outcome, comparator, validation type.
- Record exclusion reason if dropped.

## Data Extraction Priorities

Extract:

- Population/domain.
- Language/country.
- Sample size and demographics.
- Recording task.
- Recording setting/device.
- Feature/model family.
- Outcome.
- Reference standard/comparator.
- Validation design.
- External validation.
- Subgroup/fairness analysis.
- Main metric/effect.
- Limitations and risk of bias.

## Full-Text Extraction Conditions

Use full-text snippets for records marked `include` or `maybe` after abstract screening, especially when the abstract does not report validation details.

Priority terms for snippet extraction:

```text
"external validation", "held-out", "test set", "subject-level", "participant-level",
"cross-validation", "prospective", "longitudinal", "recording", "microphone",
"device", "language", "sex", "gender", "age", "race", "ethnicity",
"clinical utility", "reference standard", "diagnosis", "severity", "AUROC",
"sensitivity", "specificity", "calibration", "generalization"
```

Preferred tools:

- Europe PMC full-text XML snippets for OA biomedical papers.
- Semantic Scholar OA PDF snippets when available.
- arXiv PDF snippets for preprints.

## Formal Search Output Requirements

For each source, record in `sources/search-log.md`:

- Database/source.
- Exact query.
- Date searched.
- Filters.
- Result count.
- Export filename.
- Notes on API failures or rate limits.

For each candidate, add to a deduplicated screening table:

- ID.
- Title.
- Authors.
- Year.
- Source database.
- DOI/PMID/arXiv/URL.
- Screening decision.
- Exclusion reason if excluded.

## Multilingual and Extended Database Layer

The completed formal search is Stage 1: English/open-index search. Before claiming exhaustive systematic coverage, add the multilingual and extended database layer described in `sources/multilingual-and-extended-database-plan.md`.

Required additions:

- Chinese databases: CNKI, Wanfang, VIP, SinoMed.
- Technical databases: IEEE Xplore, ACM Digital Library, ISCA Archive / ACL Anthology where relevant.
- Clinical/citation indexes: Embase, Scopus, Web of Science.
- Trial registries: ClinicalTrials.gov, WHO ICTRP, EU Clinical Trials Register.

Chinese query seed:

```text
(语音 OR 声音 OR 声学 OR 言语 OR 说话 OR 发声)
AND
(生物标志物 OR 生物标记物 OR 数字生物标志物 OR 数字标志物)
```

Additional Chinese sensitivity queries:

```text
(语音 OR 声音 OR 声学 OR 言语)
AND
(疾病 OR 诊断 OR 筛查 OR 监测 OR 预测)
AND
(生物标志物 OR 生物标记物 OR 数字生物标志物)
```

```text
(语音 OR 声音 OR 言语)
AND
(帕金森 OR 阿尔茨海默 OR 痴呆 OR 认知障碍 OR 抑郁 OR 焦虑 OR 精神分裂症 OR 心力衰竭 OR 哮喘 OR 慢阻肺)
```

```text
(语音 OR 声音 OR 声学)
AND
(衰老 OR 老龄 OR 老年人 OR 生物年龄 OR 衰弱)
```

Non-English records should be retained as `translation_needed` when title/abstract suggests relevance. Do not silently exclude them for language.

## Reproducibility and Governance Requirements

Every formal search and extraction run must be logged in `governance/tool-run-log.csv` and connected to a candidate file through `governance/search-trajectory-log.csv`.

Before final synthesis:

- all known-relevant seed papers must be checked against search outputs
- missed seeds must be logged in `governance/false-negative-audit.csv`
- AI-assisted screening labels must be manually adjudicated
- any protocol changes after formal search start must be logged in `governance/protocol-deviation-log.csv`
