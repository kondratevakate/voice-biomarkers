# Tooling Assessment

Date: 2026-06-05
Question: Which local `ai-scientist` tools help define and execute a rigorous systematic review for a strong academic article?

## Current State

The local `ai-scientist` folder contains multiple AI-for-science repositories and notes. For this voice biomarkers review, the most useful tooling is not the autonomous paper-generation stack, but the literature-search and evidence-extraction stack in ToolUniverse.

## Source Basis

Inspected local sources:

- `D:/projects/knowledge-vault/04_projects/02_academia/ai-scientist/README.md`
- `D:/projects/knowledge-vault/04_projects/02_academia/ai-scientist/source-inventory.md`
- `D:/projects/knowledge-vault/04_projects/02_academia/ai-scientist/review-matrix.md`
- `D:/projects/knowledge-vault/04_projects/02_academia/ai-scientist/open-source/ToolUniverse/docs/dev_docs/FULLTEXT_ACCESS_GUIDE.md`
- `D:/projects/knowledge-vault/04_projects/02_academia/ai-scientist/open-source/ToolUniverse/docs/dev_docs/SEARCHING_BIORXIV.md`
- `D:/projects/knowledge-vault/04_projects/02_academia/ai-scientist/open-source/AI-Scientist-v2/README.md`
- `D:/projects/knowledge-vault/04_projects/02_academia/ai-scientist/open-source/agent-baselines/agent_baselines/solvers/search/paper_finder.py`

## Tool Assessment

| Tool / repo | Useful for this review? | Role | Assessment |
|---|---:|---|---|
| K-Dense `literature-review` skill | Yes | Systematic review method | Keep as protocol backbone: PRISMA-style search, inclusion/exclusion, screening, extraction, synthesis, citation verification. |
| K-Dense `paper-lookup` skill | Yes | Database API method | Keep for source-specific API strategy across PubMed, arXiv, OpenAlex, Crossref, Semantic Scholar. |
| ToolUniverse | Yes, high value | Literature discovery + full-text snippets | Best local upgrade. It has PubMed, Europe PMC, OpenAlex, Semantic Scholar, arXiv, Crossref, bioRxiv/medRxiv DOI retrieval, and full-text snippet extraction. |
| ToolUniverse Europe PMC | Yes, high value | Preprint and biomedical search | Use as primary search route for medRxiv/bioRxiv because official bioRxiv API does not support keyword search. |
| ToolUniverse full-text snippets | Yes | Full-text eligibility/extraction support | Use for methods/validation terms such as `external validation`, `subject-level split`, `recording device`, `language`, `clinical utility`. |
| AI-Scientist-v2 | No for protocol; maybe later | Paper generation / ideation | Not appropriate for setting systematic-review conditions. Uses Semantic Scholar for novelty/citations, but not a systematic-review engine. |
| agent-baselines paper_finder | Maybe | Paper retrieval benchmark/API wrapper | Interesting if its AI2I paper finder service is available, but it depends on external service/HF token and is less transparent than direct database searches. |
| Paper2Agent | No | Turn a paper/codebase into an agent | Useful for reproducibility of a specific method, not for systematic search protocol. |

## Recommended Tooling Stack

Use a two-layer workflow:

1. Protocol layer: K-Dense `literature-review` + PRISMA logic.
2. Execution layer: ToolUniverse literature tools where available.

Recommended formal search order:

1. PubMed for peer-reviewed biomedical literature.
2. Europe PMC for biomedical + medRxiv/bioRxiv preprints and full-text snippets.
3. arXiv for speech processing, ML, dataset, and foundation-model papers.
4. OpenAlex for broad scholarly discovery, citation counts, and deduplication.
5. Semantic Scholar for citation graph and influential paper expansion, preferably with API key.
6. Crossref for exact DOI/title verification only.
7. Unpaywall/OA links for full-text access after candidate selection.

## Why ToolUniverse Changes The Search Conditions

ToolUniverse documents an important constraint: bioRxiv/medRxiv public APIs do not support keyword search. Therefore, formal preprint discovery should not rely on direct bioRxiv API keyword queries. Use Europe PMC `source: PPR` or web-restricted searches for discovery, then use DOI-based bioRxiv/medRxiv retrieval for metadata.

ToolUniverse also separates metadata search from full-text extraction. That is useful for a strong article because title/abstract screening is not enough to judge:

- leakage and subject-level split
- external validation
- recording task/device/environment
- demographic and language generalization
- clinical reference standard
- analytical vs clinical validation
- prospective vs retrospective design

## Uncertainty

- ToolUniverse has not been installed/executed in this workspace yet.
- Semantic Scholar may still need an API key to avoid 429 rate limits.
- Full-text snippet extraction only works for open-access articles or accessible PDFs/XML.

## Recommended Next Action

Use ToolUniverse documentation to harden `search-strategy.md`, then run formal searches with exact database-specific queries and export files. If ToolUniverse imports cleanly, use it directly; otherwise reproduce the same strategy with REST APIs and curl/Python.

