# External Tools — Integration with the Chirality Framework

This document describes how external open-source tools integrate with the Chirality Framework. **edgequake-pdf2md** is a pipeline tool used in Step 0 of the DOMAIN pipeline. **synalinks** is the preferred ad hoc utility for human-directed entity extraction work when bridging DOMAIN knowledge into PROJECT or SOFTWARE contexts. **synalinks-memory-python-sdk** provides an optional queryable long-term knowledge layer. **zingg** remains available for fuzzy entity resolution workflows.

All tool directories are gitignored. The framework configures against them as external dependencies, not vendored copies.

For the authoritative pipeline specification — entity type registry, ID namespace rules, canonical CSV schemas, confidence level definitions, validation criteria per stage, execution model, and domain-specific tool configuration — see `PIPELINE_DESIGN.md`.

---

## The Systems

| System | What it does | Role | Maintained by |
|---|---|---|---|
| **chirality-domain-test** | Structured, auditable agent framework for domain knowledge curation. Decomposes handbooks into Categories and Knowledge Types, produces Knowledge Artifacts, builds and audits a structural hypergraph of workspace organization. | Framework | This repo |
| **PDF2MD (native)** | Native PDF-to-Markdown pipeline. Rasterizes pages via pymupdf, dispatches per-page Type 2 agents for multimodal vision conversion, post-processes with 10-rule cleanup + header/footer stripping, assembles into a single Markdown file. Resumable, batch-parallel. | Pipeline agent (Step 0) | This repo (`agents/AGENT_PDF2MD.md`) |
| **edgequake-pdf2md** | High-performance PDF-to-Markdown converter. Rasterizes PDF pages to images and sends them to Vision Language Models (VLMs) for structure-preserving conversion. Rust CLI + library. Superseded by native PDF2MD agent for Step 0; remains available as an alternative. | Pipeline tool (Step 0, legacy) | Edgequake (open source) |
| **zingg** | Scalable ML-based entity resolution. Learns blocking + similarity models from small labeled training sets via active learning, then clusters records that refer to the same real-world entity. Runs on Apache Spark. | Ad hoc utility (legacy) | Zingg (open source) |
| **synalinks** | Neuro-symbolic LM framework (Keras-like). Defines entity types as `DataModel` classes, extracts structured entities via `Generator` with schema-constrained output, and emits deterministic GB.v1.0 extraction CSVs. | Ad hoc utility (extraction) | Synalinks (open source) |
| **synalinks-memory-python-sdk** | Python client for Synalinks Memory — hosted knowledge API. Optional query layer over extracted entities. Derived from extraction outputs, not canonical. | Ad hoc utility (query, optional) | Synalinks (open source) |
| **pdftotext (Poppler)** | Command-line PDF text extractor. Used for deterministic extraction of embedded title-block text, drawing-number verification, and system-name candidate harvesting from PDF pages when present in the text layer. | Supporting utility (verification) | Poppler (open source) |
| **Pillow** | Python imaging library used for ad hoc operator-side image cropping and contact-sheet generation during drawing extraction QA and workflow prototyping. | Supporting utility (operator QA) | Pillow contributors (open source) |

---

## What Each System Produces

**chirality-domain-test agents produce:**
- Structural hypergraph (DOMAIN_HYPERGRAPH): `nodes.csv`, `hyperedges.csv`, `incidence.csv` — Categories, Knowledge Types, Artifacts, Ledger bindings, Objectives and their n-ary relationships
- Knowledge Artifacts (DOMAIN_DOCUMENTS): Reference.md, Standard.md, Procedure.md, Guidance.md per Knowledge Type — the actual domain content
- Semantic matrices (CHIRALITY_FRAMEWORK): `_SEMANTIC.md` — conceptual coordinate system per Knowledge Type
- Semantic lensing (CHIRALITY_LENS): `_SEMANTIC_LENSING.md` — enrichment register identifying gaps and conflicts

**PDF2MD agent produces:**
- Clean, structured Markdown from PDF source documents — preserving tables, headings, lists, formulas, and reading order
- Per-page `.md` files in a work directory (resumable intermediate artifacts)
- `manifest.json` with page metadata (page count, DPI, rendering timestamp)
- Header/footer removal integrated as a pipeline stage (via `clean_pdf2md_output.py`)

**zingg produces (when invoked ad hoc):**
- Entity clusters: input records augmented with `z_cluster` (cluster ID), `z_minScore`, `z_maxScore`
- A trained blocking model (hash functions that reduce the comparison space)
- A trained similarity model (classifier that scores record pairs)

**synalinks produces (when invoked ad hoc):**
- GB.v1.0 compliant extraction CSVs: `nodes.csv` (typed entities with `EXTRACTED_ENTITY` NodeType, `EXT-{EntitySubtype}-{blake2b[:12]}` IDs) and `edges.csv` (typed relationships between extracted entities)
- Entity types defined as `synalinks.DataModel` classes per project (inline in the extraction script)
- Confidence levels constrained to HIGH/MEDIUM/LOW per `PIPELINE_DESIGN.md` §2.1
- Deterministic blake2b identity fingerprinting (same identity fields → same ID)
- Extraction metadata JSON (source document, timestamp, configuration, entity/relationship counts)

**synalinks-memory-python-sdk produces (when invoked optionally):**
- Query results over uploaded extraction data via the Synalinks Memory hosted API
- Not a canonical data store — derived from extraction outputs

---

## The DOMAIN Pipeline

```
_Sources/ (handbooks, reference materials — typically PDFs)
      |
      v
  PDF2MD agent (Step 0)
  (rasterizes pages, dispatches per-page VLM agents, post-processes, assembles)
      |
      v
  Markdown source documents
  (readable text, tables, structure preserved)
      |
      v
  DOMAIN_DECOMP (Step 1) → PREPARATION (Step 2)
      |
      v
  DOMAIN_DOCUMENTS (Step 3)
  (reads source Markdown, produces Knowledge Artifacts per KTY)
      |
      v
  DOMAIN_HYPERGRAPH (Step 4)
      |
      v
  AUDIT_HYPERGRAPH_CLOSURE (Step 5)
```

The pipeline is a single linear path from source documents through to an audited structural hypergraph.

### What runs when

| Step | Tool / Agent | Depends on | Can parallel with |
|---|---|---|---|
| 0 | PDF2MD (native agent) | PDF source documents in `_Sources/` | — |
| 1 | DOMAIN_DECOMP | Human input (+ Markdown sources from step 0) | — |
| 2 | PREPARATION | Decomposition | — |
| 3 | DOMAIN_DOCUMENTS | Preparation + Markdown sources | — |
| 4 | DOMAIN_HYPERGRAPH | PREPARATION (reads folder structure) | — |
| 5 | AUDIT_HYPERGRAPH_CLOSURE | DOMAIN_HYPERGRAPH | — |

Step 0 (PDF2MD agent) runs first when source materials are PDFs — it produces the Markdown that the content path consumes. The native PDF2MD agent replaces edgequake-pdf2md; it uses pymupdf for rasterization and Claude Code's multimodal vision for per-page conversion.

---

## DOMAIN → Human → PROJECT / SOFTWARE

The DOMAIN pipeline produces the knowledge layer — normative rules, trade-off guidance, step-by-step procedures, verification criteria. **The human bridges between DOMAIN knowledge and its application in PROJECT or SOFTWARE contexts.** This bridging is the human's validation and decision-making process, not a pipeline stage.

When working in a PROJECT or SOFTWARE context, the human draws on DOMAIN knowledge case by case:
- A designer routing pump suction piping pulls rules from a KTY and applies them to specific equipment in their project
- A software developer implementing compliance checks references normative statements and encodes them as validation logic
- A project lead reviewing a layout consults trade-off guidance for deviation decisions

Agents assist the human in this bridging work — extracting data from documents on demand, cross-referencing against KTY standards, building case-specific relationship maps — but the human directs what to extract, decides what it means, and validates whether the mapping is correct.

### Entity extraction in bridging context

When the human needs entity-level data for a specific project task, extraction utilities are available:

- **synalinks** (preferred) extracts typed entities from a document the human selects, using `DataModel` classes + `Generator` for schema-constrained structured output. Produces GB.v1.0 compliant CSVs with deterministic blake2b IDs. Entity resolution is handled by deterministic identity fingerprinting — no separate Spark-based resolution step needed.
- **zingg** (legacy) resolves entity identity across multiple extraction outputs using ML-based matching on Apache Spark. Synalinks' deterministic identity fingerprinting handles the common case; zingg remains documented for scenarios requiring fuzzy cross-document matching at scale.

These produce **ad hoc graphs** scoped to the documents the human selects and validated by the human before use. They are not pipeline stages that run automatically.

---

## Agent Interfaces

### DOMAIN_HYPERGRAPH

Reads workspace folder structure and metadata stubs (`_CONTEXT.md`, `_REFERENCES.md`). Produces the structural hypergraph — the terminal data artifact of the DOMAIN pipeline.

### AUDIT_HYPERGRAPH_CLOSURE

Reads the structural hypergraph (produced by DOMAIN_HYPERGRAPH) and validates structural integrity, referential integrity, and completeness.

### ORCHESTRATOR

Coordinates the pipeline. Responsible for invoking the PDF2MD agent at Step 0 and sub-agents at Steps 1–7. May also assist the human with ad hoc entity extraction work when directed.

### PDF2MD

Orchestrates PDF-to-Markdown conversion (Step 0). Rasterizes PDF pages to PNGs via `tools/pdf2md/rasterize_pdf.py`, dispatches PDF2MD_PAGE sub-agents in configurable batches for multimodal vision conversion, runs `tools/pdf2md/postprocess_page.py` (10-rule cleanup) and `tools/reporting/clean_pdf2md_output.py` (header/footer stripping), then assembles the final Markdown via `tools/pdf2md/assemble_markdown.py`.

### DRAWING_EXTRACT

Orchestrates structured extraction from engineering drawing PDFs. Rasterizes pages via `tools/pdf2md/rasterize_pdf.py`, prepares deterministic top-header/titleblock crops plus overlapping top-header slices via `tools/drawing_extract/prepare_header_crops.py`, dispatches `DRAWING_EXTRACT_PAGE` workers for page-scoped extraction, writes deterministic per-page coverage reports via `tools/drawing_extract/report_stub_counts.py`, applies deterministic post-extraction QC via `tools/drawing_extract/sanitize_equipment_stubs.py`, assembles combined Markdown and CSV outputs via `tools/drawing_extract/assemble_equipment_markdown.py` and `tools/drawing_extract/assemble_equipment_csv.py`, flags repeated equipment numbers via `tools/drawing_extract/flag_duplicate_equipment_csv.py`, may optionally cross-check title-block text via `tools/drawing_extract/extract_pdf_titleblock_text.py` when `pdftotext` is available, and can backfill extracted title-block system names into page stubs via `tools/drawing_extract/backfill_stub_system_names.py`. Targeted deterministic family-specific recovery tools such as `tools/drawing_extract/recover_deepcut_multiblock_headers.py` remain available when a repeated layout still undercounts after the default robust path. Deduplication remains available only as an optional/manual downstream utility.

---

## Ad Hoc Entity Extraction — Tool Reference

> **Note:** Synalinks is the preferred extraction path. Zingg remains optional for fuzzy cross-document matching when deterministic identity fingerprinting is insufficient.

The following sections document Synalinks + zingg interfaces, data contracts, and entity resolution patterns. These are reference material for when the human directs entity extraction work in a PROJECT or SOFTWARE context.

### Synalinks → zingg Flattening

**Format:** CSV or Parquet.

When fuzzy resolution is needed across multiple extraction outputs, extracted entities are flattened to flat records for zingg:
- One row per extracted entity
- Columns: `entity_id`, `entity_type`, `label`, identity field columns, `source_kty`, `source_doc`
- zingg `FieldDefinition` maps each column to a match type (`FUZZY`, `EXACT`, `TEXT`, etc.) appropriate for the domain

### zingg Output

**Format:** CSV or Parquet.

Same records as input, augmented with:
- `z_cluster`: integer cluster ID — all entities in the same cluster are resolved as the same real-world entity
- `z_minScore`: lowest match confidence within the cluster
- `z_maxScore`: highest match confidence within the cluster

### Entity Resolution Patterns

Entity resolution when using these tools is divided between two tools based on what each does best:

| Resolution type | Tool | Why |
|---|---|---|
| **Cross-document entity identity** | zingg | Structured record matching with fuzzy fields. Scales via blocking model. Trained model is deterministic — same inputs produce same clusters. Handles typos, abbreviations, naming variations. |
| **Entity-to-knowledge correspondence** | LLM (agent-assisted) | Requires reading production documents and understanding domain semantics. Cannot be reduced to field-level similarity — needs contextual reasoning about whether an extracted entity refers to a concept a KTY covers. |

### How zingg gets its training data

Zingg requires labeled training pairs (match / no-match). The labeling approach:

1. **Deterministic seed**: exact-match entity pairs (identical identity fingerprints across extractions) serve as positive examples. Entity pairs with different entity types serve as negative examples.
2. **LLM-assisted labeling**: zingg's `findTrainingData` phase selects candidate pairs. The LLM evaluates them — grounded in relevant KTY production documents — and provides match/no-match labels.
3. **Active learning iteration**: zingg prioritizes the most informative (uncertain) pairs for labeling, minimizing the number of LLM evaluations needed.

Once trained, zingg's model is deterministic and scalable. The LLM's judgment is used for training, not for every entity pair at inference time.

---

## Installation

**PDF2MD** (native pipeline agent — Step 0):

```
pip install pymupdf
```

No VLM API key required — uses Claude Code's built-in multimodal vision. Invoke with `--agent PDF2MD` or let ORCHESTRATOR spawn it.

**Drawing extraction support utilities**:

```
pip install pillow
```

Optional PDF title-block verification tool requires:

```
pdftotext
```

Typically provided by Poppler packages such as `poppler-utils`.

**edgequake-pdf2md** (legacy pipeline tool, alternative to PDF2MD):

```
cargo install edgequake-pdf2md
```

Requires a VLM API key (OpenAI, Anthropic, Gemini, etc.) set as an environment variable. See the edgequake-pdf2md README for provider configuration.

**zingg** (legacy):

Requires Apache Spark. See the [zingg documentation](https://docs.zingg.ai/) for installation and Spark setup.

**synalinks** (ad hoc utility — preferred extraction path):

```
cd synalinks/ && uv sync
```

Requires an LLM API key (e.g., `ANTHROPIC_API_KEY` for Claude models via LiteLLM). Extraction scripts run via `uv run --project ../../synalinks python run_synalinks_extraction.py` from the workspace directory.

**synalinks-memory-python-sdk** (optional query layer):

```
cd synalinks-memory-python-sdk/ && uv sync
```

Requires `SYNALINKS_API_KEY` for the hosted Memory API. The SDK supports both `list()` and the explicit alias `list_predicates()`.

All tool directories (`edgequake-pdf2md/`, `zingg/`, `synalinks/`, `synalinks-memory-python-sdk/`) are gitignored. If local copies are present for development reference, they are not tracked in this repository.
