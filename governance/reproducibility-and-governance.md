# Reproducibility and Governance Layer

Date: 2026-06-06
Status: required before final synthesis

## Purpose

This layer applies lessons from AI-scientist benchmark and tooling systems to the systematic review workflow. It is not a substitute for PRISMA/JBI/Cochrane methods. It adds engineering-grade auditability: every automated search, screen, extraction, and post-processing step must be reproducible and reviewable.

## Source Basis

This governance layer is adapted from local AI-scientist source critiques:

- ScienceAgentBench: false-negative mitigation, SME/manual validation, contamination control, dockerized evaluation.
- AstaBench: solver metadata, cost logging, validation/test split, sandbox execution, reproducibility metadata.
- BixBench: trajectories, postprocessing, replicas, Docker/HF access, cost/time accounting.
- AI-Scientist-v2: sandboxing and uncontrolled web/API risks; Semantic Scholar rate-limit dependency.
- Paper2Agent: benchmark extraction, assessment reports, assumptions/limitations, human review outputs.
- ToolUniverse: tool registry, tool protocol, async/tool composition, literature search coverage.
- K-Dense scientific-agent-skills: permissions, contribution review, manual review; scans do not replace human review.

## Governance Rules

### 1. Known-Relevant Seed Set

Before final search execution, define a seed set of known relevant papers. The formal search must retrieve these records or explicitly explain why not.

Minimum seed categories:

- seed aging / biological age papers
- heart failure / cardiovascular voice biomarker papers
- neurological speech biomarker reviews and empirical studies
- validation-framework papers
- foundation-model or dataset papers
- non-English / Mandarin or Chinese-language candidates where available

Failure to retrieve a seed paper is a protocol event, not a silent miss.

### 2. False-Negative Audit

After each formal search pass:

1. Check whether all seed papers were retrieved.
2. Run backward citation chasing from included reviews.
3. Run forward citation chasing from seed and framework papers.
4. Log every newly discovered eligible paper.
5. Classify each missed record:
   - query vocabulary miss
   - database coverage miss
   - API failure/rate limit
   - language/indexing miss
   - deduplication/postprocessing error

### 3. Tool-Run Log

Every automated search or extraction run must create a row in `governance/tool-run-log.csv`.

Required fields:

- run_id
- date_time
- tool_or_script
- database_or_endpoint
- query_family
- exact_query_or_input
- filters
- output_file
- raw_export_file
- status
- error_or_limitation
- script_git_sha_or_file_hash
- operator

### 4. Search Trajectory Log

Every candidate set should be traceable:

```text
query -> raw export -> parsed candidates -> deduped candidates -> screening packet -> extraction table -> synthesis
```

Use `governance/search-trajectory-log.csv`.

### 5. AI-Assisted Screening Control

Automated labels such as `include`, `maybe`, `background`, or `exclude` are provisional. They are not final screening decisions.

Final decisions require:

- manual confirmation, or
- documented second-pass adjudication, or
- explicit label `ai_prelabel_only`.

Any manuscript must report if AI-assisted screening or extraction was used.

### 6. Screening Reliability SOP

Minimum defensible workflow:

1. Calibrate on 50 records.
2. Record disagreements and update decision rules.
3. Double-screen at least 20% of records, or all records if feasible.
4. Adjudicate conflicts.
5. Report agreement qualitatively or quantitatively.

### 7. Extraction Provenance

Every extracted field must be tied to a source basis:

- title
- abstract
- full text
- table/figure
- supplement
- author/database metadata
- inference by reviewer

Facts, inferences, and recommendations must be separated.

### 8. Protocol Deviation Log

Any change after formal search starts must be logged in `governance/protocol-deviation-log.csv`.

Examples:

- adding a database
- changing a query
- changing inclusion/exclusion criteria
- changing deduplication logic
- changing evidence strata
- adding non-English handling
- excluding a database due to access failure

### 9. Cost, Time, and Access Accounting

For subscription/API-dependent sources, record:

- access available or unavailable
- API key used or not used
- rate-limit failure
- date/time of failure
- retry plan
- whether results are reproducible without institutional access

### 10. Safety Boundary

No uncontrolled autonomous web browsing should be treated as formal search. Web search may be supplementary only if exact queries, dates, result pages, and inclusion decisions are logged.

## Required Files

- `governance/tool-run-log.csv`
- `governance/search-trajectory-log.csv`
- `governance/known-relevant-seed-set.csv`
- `governance/false-negative-audit.csv`
- `governance/protocol-deviation-log.csv`
- `governance/screening-reliability-log.csv`
- `governance/extraction-provenance-log.csv`

## Recommended Next Action

Populate the known-relevant seed set, then audit whether the formal search retrieved each seed record.
