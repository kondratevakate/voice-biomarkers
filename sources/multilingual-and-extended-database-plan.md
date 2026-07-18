# Multilingual and Extended Database Search Plan

Date: 2026-06-06
Status: required before claiming exhaustive systematic coverage

## Current State

The completed formal search is a strong first pass over open English-oriented scholarly infrastructure, but it is not exhaustive. It should be labeled as Stage 1: English/open-index search.

To support a strong academic systematic review of the field, the search must add multilingual, technical, and subscription-index layers.

## Source Basis

Stage 1 covered:

- PubMed
- Europe PMC
- Europe PMC preprints
- OpenAlex
- attempted arXiv API

Known gaps:

- CNKI / Wanfang / VIP / SinoMed were not searched.
- IEEE Xplore and ACM Digital Library were not searched.
- Embase, Scopus, and Web of Science were not searched.
- Google Scholar was not systematically exported.
- arXiv API failed in the formal run and needs retry.
- Semantic Scholar failed/rate-limited in pilot and needs API key or slow retry.

## Chinese Database Layer

Databases:

- CNKI
- Wanfang Data
- VIP Chinese Journals
- SinoMed / Chinese Biomedical Literature Database

Chinese search concepts:

| Concept | Chinese terms |
|---|---|
| voice/speech/acoustic | 语音, 声音, 声学, 言语, 说话, 发声 |
| biomarker | 生物标志物, 生物标记物, 数字生物标志物, 数字标志物 |
| health/clinical | 医疗, 健康, 临床, 疾病, 诊断, 筛查, 监测, 预测 |
| aging | 衰老, 老龄, 老年人, 生物年龄, 衰弱 |
| neurological | 帕金森, 阿尔茨海默, 痴呆, 认知障碍 |
| psychiatry | 抑郁, 焦虑, 精神分裂症 |
| respiratory/cardiovascular | 哮喘, 慢阻肺, 呼吸, 咳嗽, 心力衰竭, 冠心病 |

Candidate Chinese queries:

```text
(语音 OR 声音 OR 声学 OR 言语 OR 说话 OR 发声)
AND
(生物标志物 OR 生物标记物 OR 数字生物标志物 OR 数字标志物)
```

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
(帕金森 OR 阿尔茨海默 OR 痴呆 OR 认知障碍 OR 抑郁 OR 心力衰竭 OR 哮喘 OR 慢阻肺)
```

```text
(语音 OR 声音 OR 声学)
AND
(衰老 OR 老龄 OR 老年人 OR 生物年龄 OR 衰弱)
```

English-in-Chinese-index queries:

```text
"voice biomarker" OR "vocal biomarker" OR "speech biomarker" OR "digital biomarker"
```

## Technical Database Layer

Databases:

- IEEE Xplore
- ACM Digital Library
- ISCA Archive / ACL Anthology where relevant
- arXiv exact phrase retry

Purpose:

- speech processing methods
- foundation models
- acoustic feature extraction
- datasets and benchmarks
- signal-processing validation

Technical queries:

```text
("voice biomarker" OR "vocal biomarker" OR "speech biomarker")
```

```text
("clinical voice" OR "medical speech" OR "speech health" OR "voice foundation model")
AND (biomarker OR disease OR aging OR clinical OR health)
```

```text
("speech" OR "voice" OR "acoustic")
AND ("digital biomarker" OR "health monitoring" OR "disease detection")
```

## Clinical Index Layer

Databases:

- Embase
- Scopus
- Web of Science Core Collection

Purpose:

- broader biomedical and conference coverage
- citation tracking
- European and non-US indexing
- more complete systematic review defensibility

Use the same query families as `search-strategy.md`, adapted to each database syntax.

## Trial and Regulatory Layer

Databases:

- ClinicalTrials.gov
- WHO ICTRP
- EU Clinical Trials Register
- FDA 510(k) and device databases, if device/product claims become relevant

Trial search terms:

```text
voice biomarker
vocal biomarker
speech biomarker
digital voice
speech digital biomarker
```

## Inclusion Handling for Non-English Records

Do not exclude non-English records at title stage if title/abstract suggests relevance.

Codes:

- `include_translation_needed`
- `maybe_translation_needed`
- `exclude_non_relevant`
- `background_translation_needed`

Minimum extracted fields before translation:

- original title
- translated title
- database
- authors
- year
- journal/source
- abstract if available
- DOI or local database ID
- language
- screening decision

## Reporting Requirement

The final Methods section must explicitly report:

- databases searched
- date searched
- languages included
- translation method
- whether subscription databases were accessible
- whether Chinese databases were searched directly or via secondary web indexes
- limitations for inaccessible databases

## Recommended Next Action

Run Chinese database searches manually or through institutional access, then export RIS/BibTeX/CSV where possible. If direct access is unavailable, record this as a limitation and perform supplementary web-index searches with Chinese search strings.
