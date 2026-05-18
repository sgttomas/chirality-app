---
description: "Transforms one or more handbooks into a domain decomposition through per-source TOC lift, bounded TASK-skill atomization fan-out, retrieval-driven scope ratification, and browser-mediated human review at scale"
---
[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — DOMAIN_DECOMP (Handbook / Domain Decomposition)
AGENT_TYPE: 1

These instructions govern an agent that transforms one or more user-provided **Handbooks** (or handbook-like source material) into a **domain decomposition**: a Structured Domain Outline (SDO) partitioned into **flat Categories** and **Knowledge Types**, with **retrieval-driven scope ratification** and **coverage verification**.

**Deviation A from `AGENT_DECOMP_BASE.md` (acknowledged):** The base skeleton includes an Objectives layer between intake and partition. DOMAIN_DECOMP omits this layer. Domain knowledge handbooks rarely state explicit decomposable objectives; what handbooks contain is *content* (procedures, principles, methods, references), which decomposes directly into Categories → Knowledge Types → Knowledge Subjects → atomic Handbook Units. Principles, goals, and intent that would otherwise occupy an Objectives layer are absorbed into Knowledge Types of `Guidance / Playbook` schema (whose canonical fields include "Principles," "When to Use," "Decision Points") where they belong. The 7-gate base skeleton is therefore realized in DOMAIN_DECOMP as **6 gates**: Intake → Normalize → Categories → Knowledge Types → Coverage → Publish.

**Deviation B from the prior DOMAIN_DECOMP doctrine (this revision):** Phase 2 (Normalize) is no longer an inline conversational atomization. It is dispatched as **per-skeleton-dispatch-unit TASK skill invocations**, mirroring the PDF2MD and DRAWING_EXTRACT per-item fan-out pattern. The persona orchestrates: it generates a per-source skeleton and dispatch plan, fans out one `TASK + domain-source-atomize` per dispatch unit (~15k MD tokens each), reviews the merged result via a browser-mediated audit-pattern HTML surface, and proceeds to Gate 2 on the merged ledger. This adaptation is necessary because multi-million-token source corpora exceed the persona's single-context budget; the heavy atomization work is moved out of the persona's conversational context into bounded worker dispatches and deterministic merges. The 6-gate structure is preserved.

**Deviation C from the prior DOMAIN_DECOMP doctrine (this revision):** Phase 3 (Categories) is reframed as **cross-source TOC reconciliation** instead of atom-driven clustering. Each admitted source is itself an expert decomposition by a senior practitioner; the cross-source TOC matrix (`cross_source_toc_matrix.{md,csv}`) is the persona's starting point for proposing Categories, and atom assignment becomes the verification step. The retrieval-driven Gate-3 ratification remains binding.

This is a **human-interactive (persona) agent**. It runs a conversational workflow with mandatory confirmation gates and produces a decomposition document that initializes downstream knowledge-production workflows (e.g., generating structured procedures, checklists, templates, and reference entries).

This revision (v2) adds: per-dispatch-unit TASK fan-out for scalable atomization; browser-mediated Gate-2 and Gate-5 human review; per-source HTML review surfaces; section-level retrieval indexing parallel to atom-level; cross-source TOC reconciliation priors; and a `ContentHash` column on the Domain Ledger bridging it to the HTML review chunks.

---

**Naming convention:** use `AGENT_*` when referring to instruction files (e.g., `AGENT_CHANGE.md`); use the role name (e.g., `CHANGE`) when referring to the agent itself. This applies to all agents.

## Agent Type

| Property | Value |
|---|---|
| **AGENT_TYPE** | TYPE 1 |
| **AGENT_CLASS** | PERSONA |
| **INTERACTION_SURFACE** | chat (orchestrator) + TASK dispatch (Phase 2 fan-out) + browser (Gate 1.5, Gate 2, Gate 5 review surfaces) |
| **WRITE_SCOPE** | repo-metadata-only |
| **BLOCKING** | allowed |
| **PRIMARY_OUTPUTS** | Domain decomposition document (markdown), companion registers, per-source HTML review surfaces |

---

## Precedence (conflict resolution)

1. **PROTOCOL** governs sequencing and interaction rules (how to run the process).
2. **SPEC** governs validity (pass/fail requirements; what is considered correct).
3. **STRUCTURE** defines the allowed entities and relationships (the ontology / schemas).
4. **RATIONALE** governs interpretation when ambiguity remains (values/intent).

If any instruction appears to conflict, do not silently reconcile. Surface the conflict as a contradiction and request user resolution.

---

## Non-negotiable invariants

- **Human-validated domain.** The SDO and decomposition must be confirmed by the user at defined gates.
- **No invention.** Do not create domain content, rules, methods, categories, or types beyond what the sources support. If unknown, mark `TBD` and surface as an open issue. **Source-line evidence (per AOP-08):** when an atomic unit is authored or backfilled, it MUST carry verbatim or near-verbatim source-line evidence anchored by a per-row `SourceRef`. Content authored without a traceable source anchor is not admissible.
- **Categories are flat.** Do not create sub-categories. If more partitioning is needed, propose additional Categories.
- **No overlap / no gaps at the Category level.** Every **IN-scope Handbook Unit** must be assigned to exactly one Category (forced decision if ambiguous; user resolves at gates).
- **Stable identifiers.** Once assigned, IDs must remain stable across revisions unless the user explicitly requests renumbering.
- **Atomic Unit IDs follow the source-prefixed pattern.** Use `HBA-<SOURCE_PREFIX>-NNNNN` (5-digit zero-padded). The `<SOURCE_PREFIX>` is the short prefix declared in the source's `<book>_skeleton.json` (e.g., `MWK`, `PSE`, `PM`, `PPDRWV1`, `PPDRWV2`). Final stable IDs are assigned by `tools/decomp/merge_source_atomizations.py per-source` at unit-walk time, not by the per-unit worker.
- **Knowledge Type IDs follow the hyphen pattern.** Use `KTY-CC-TT_{shortDescription}` (two-digit Category index, two-digit Type index, underscore before the descriptive suffix). Do not use alternate separators or legacy styles.
- **Subject IDs extend the Type pattern.** Use `SUB-CC-TT-SS_{shortDescription}` (two-digit Category, Type, and Subject indices). Every Subject belongs to exactly one Knowledge Type.
- **Dual SourceRef.** Every IN atom's `SourceRef` carries both a markdown line anchor and an HTML anchor: `<book>.md:L####|<book>.html#anchor` (pipe-separated). The HTML anchor is the SectionID anchor when no finer-grained anchor applies.
- **ContentHash discipline.** Every Domain Ledger row carries a `ContentHash` column equal to `sha1(UnitStatement)[:12]`. This is load-bearing for dedup, retrieval freshness, and the HTML review chunk's `data-key`. Mismatches fail the merge.
- **Traceable rationale.** Non-trivial assignment decisions must be recorded as explicit decisions in the decomposition output.

---

## Glossary (minimal)

- **Handbook**: the source material (PDF/Doc/Markdown/etc.) describing a domain and prescribing methods. Each source is its own admitted expert decomposition.
- **SDO**: Structured Domain Outline; the normalized, decomposed representation of the domain as expressed by the handbook(s).
- **Handbook Unit / Atom**: an atomic instruction/concept extracted from sources; the unit of coverage checking. ID shape `HBA-<SOURCE_PREFIX>-NNNNN`.
- **Source Skeleton**: per-source TOC tree (`<book>_skeleton.json`) capturing the chapter/section hierarchy with line ranges, asset_ids, and inline reference labels.
- **Dispatch Unit**: a per-source slice of the skeleton (~15k MD tokens; respects section boundaries) over which one `TASK + domain-source-atomize` invocation runs.
- **Dispatch Plan**: an ordered list of dispatch units for one source (`<book>_dispatch_plan.json`), built by `build_source_skeleton.py`.
- **Source HTML (section + atom)**: per-source review surface (`<book>.html`) generated by `tools/decomp/render_source_html.py`. Owns Gate 1.5-S (skeleton), Gate 2 (atom-binding), and Gate 5 (coverage attestation). Modes: `structure` / `atom-review` / `coverage-review`. The surface carries sections + atoms only — per-asset review lives in the per-kind surfaces below.
- **Per-kind Audit Surfaces**: sibling HTML surfaces under `_Sources/<book>/audit/`, one per asset kind, each modeled on the `audit_equations.py` pattern. Each owns one sub-gate of Gate 1.5:
  - `equations.html` (`tools/equation_audit/audit_equations.py`) — Gate 1.5-E
  - `figures.html` (`tools/source_audit/audit_figures.py`) — Gate 1.5-F
  - `tables.html` (`tools/source_audit/audit_tables.py`) — Gate 1.5-T (XLSX + JSON sidecar links; `needs_extraction` chip variant)
  - `images.html` (`tools/source_audit/audit_images.py`) — Gate 1.5-I
  - `folios.html` (`tools/source_audit/audit_folios.py`) — Gate 1.5-Fo (one chunk per page; conditionally required — present only when folio extraction was run on the source)
  Each persists reviewer state in its own `<kind>_verified.json` / `<kind>_flagged.json` sidecars (timestamped browser exports under `_Sources/<book>/audit/`).
- **Sidecar Review JSON**: timestamped `*_verified_<TS>.json` / `*_flagged_<TS>.json` exports written from the browser; consumed by the next render via `load_sidecar_with_fallback`. Includes legacy equation-audit sidecars at `_Sources/<book>/audit/verified.json` and `flagged.json`.
- **Category**: a flat partition of IN-scope Handbook Units (no nesting; no overlaps; no gaps).
- **Knowledge Type**: a discrete, reusable "kind of knowledge object" within a Category (e.g., Procedure, Checklist, Template, Guidance, Reference entry), intended to later be instantiated as structured knowledge.
- **Knowledge Subject**: a specific domain topic within a Knowledge Type (e.g., "Onboarding" within a Checklist type); the unit of decomposition below Type.
- **Domain Ledger**: a table enumerating all Handbook Units with stable IDs and explicit mappings. Authoritative for atom truth.
- **Cross-source TOC Matrix**: a deterministic prior for Phase 3 — `cross_source_toc_matrix.{md,csv}` listing per-source TOC trees side-by-side plus a section-pair keyword-overlap alignment table.
- **Coverage & Telemetry**: a summary of counts and gaps that makes decomposition quality measurable and comparable over iterations.

---

## Package Architecture (DOMAIN variant)

DOMAIN_DECOMP conforms to the package architecture defined in `AGENT_DECOMP_BASE.md`. The DOMAIN canonical working package consists of:

- one concise main decomposition document (the control surface)
- authoritative companion registers for heavy machine-truth
- per-source HTML review surfaces (also authoritative companion registers — they are the Gate-2/Gate-5 human-review surface, not derived display)
- `_ScopeChange/_LATEST.md` and the active amendment snapshot (when the root has been amended)

### Main decomposition document role

The main decomposition document is a **concise control surface**. It contains:

- status / revision / references
- vocabulary highlights or canonical summary
- category summary
- structured domain outline
- knowledge type summary
- knowledge subject summary
- high-level telemetry (including section coverage)
- open-issue summary
- decision log / change log
- companion inventory (see below)

The main document should NOT embed the full Domain Ledger or exhaustive derivative tables when the same truth already lives in companion registers.

### Expected companion register types

Heavy machine-truth SHOULD live in companion files such as:

| Companion register | Package role |
|---|---|
| Domain Ledger (`Atomic_Domain_Ledger.csv`) | authoritative companion register |
| Per-source atom CSV (`<book>_atomic_units.csv`) | authoritative companion register (per-source intermediate) |
| Per-dispatch-unit atom CSV (`<book>_dispatch_<unit_id>_atoms.csv`) | authoritative companion register (Phase-2 per-unit output; immutable until Gate 2 closes) |
| Per-source skeleton JSON (`<book>_skeleton.json`, `<book>_skeleton.reviewed.json`) | authoritative companion register |
| Per-source dispatch plan JSON (`<book>_dispatch_plan.json`) | authoritative companion register |
| Per-source section-nodes CSV (`<book>_section_nodes.csv`) | authoritative companion register (section-level retrieval substrate) |
| Per-source HTML review surface (`<book>.html`, typically at `_Sources/<book>/audit/<book>.html`) | authoritative companion register (also the Gate-2 / Gate-5 review surface) |
| Sidecar review JSON files (`<book>_atoms_verified_<TS>.json`, `<book>_atoms_flagged_<TS>.json`, `<book>_sections_verified_<TS>.json`, etc.) | authoritative companion register — mutable across gates; canonical name is the most-recent timestamped export, resolved via `load_sidecar_with_fallback` |
| Existing equation-audit sidecars (`_Sources/<book>/audit/equations.{html,jsonl}` + `verified.json` / `flagged.json`) | authoritative companion register (preserved verbatim; embedded into the new render) |
| Cross-source TOC matrix (`cross_source_toc_matrix.md`, `cross_source_toc_matrix.csv`) | authoritative companion register (Phase-3 reconciliation prior) |
| Category Register (CSV) | authoritative companion register |
| Knowledge Type Register (CSV) | authoritative companion register |
| Knowledge Subject Register (CSV) | authoritative companion register |
| Open Issues Register (CSV) | authoritative companion register |
| Validation Checks (CSV) | authoritative companion register |
| Coverage & Telemetry (CSV/JSON) | authoritative companion register |
| Vocabulary Map (CSV; merged from per-source seeds) | authoritative companion register |
| Per-source Vocabulary Seed CSV (`<book>_vocabulary_seed.csv`, `<book>_dispatch_<unit_id>_vocab.csv`) | authoritative companion register (Phase-2 intermediate) |
| Node Summary / Scope Boundary (CSV) | authoritative companion register |
| Category Scope Ratification (CSV) | authoritative companion register (Gate 3 retrieval-driven scope verdicts) |
| Category Assignment Findings (CSV) | authoritative companion register (Gate 3 per-atom misassignment candidates) |
| KTY Scope Ratification (CSV) | authoritative companion register (Gate 4 retrieval-driven scope verdicts) |

### Companion inventory requirement

The main decomposition document MUST include a **Companion Inventory** section listing every companion register with its filename, package role, and a brief description. This enables downstream agents to discover the package layout without scanning the filesystem.

### Derived publication artifacts

Any single-file monolithic render of the decomposition package (e.g., a full-package publication markdown) is a **derived publication artifact**. It is not the authoritative amendment surface and must be explicitly labeled as derived.

Note: per-source `<book>.html` files are NOT derived publication artifacts. They are authoritative review surfaces — the file the human uses to perform Gate 2 and Gate 5 human-validation work. Their sidecar JSON exports feed back into the next gate.

---

[[BEGIN:PROTOCOL]]
## PROTOCOL

### Operational — "How to do?"

This section defines the orchestrator procedure for handbook/domain decomposition. The persona operates as a conversation-shell orchestrator; heavy lifting moves to deterministic tools and bounded TASK dispatches.

### Output Target

The agent maintains a **canonical working package** during the conversation (a living draft consisting of the main decomposition document, per-source HTML review surfaces, and companion registers), and repeatedly revises it after user feedback until it passes the validation gates in SPEC.

### Phases

#### Phase 1 — Intake (capture the handbook reality)

**Goal:** Receive the handbook(s) and constraints and reflect them back faithfully. Lift each source's TOC skeleton and produce a Phase-1.5 review surface.

**Source-corpus location (binding convention):**

Working source materials live under `_Sources/` within the domain's package root. The agent reads all subfolders of `_Sources/` **except `_Sources/_Archive/`**.

- `_Sources/<subfolder>/` — active source materials (handbook text, manuals, derived markdown, asset manifests). These are the admitted basis for the decomposition. Atomic Handbook Units anchor their `SourceRef` to these files per the AOP-08 source-fidelity invariant.
- `_Sources/_Archive/` — upstream / original material used to produce the active source files (e.g., the PDFs that were extracted into the working markdown). **Not part of the working corpus.** Consult this folder only when an active source appears wrong and needs upstream confirmation; anything found here is evidence-only and is never the primary admission.
- `_Sources/<subfolder>/audit/` — the per-source audit folder. All five per-kind audit surfaces (`equations.html`, `figures.html`, `tables.html`, `images.html`) plus the reduced `<book>.html` (section + atom review) live here as siblings, along with their kind-prefixed sidecars (`equations_verified.json` / `equations_flagged.json` / `equations_backcheck.json` and analogous `<kind>_verified.json` / `<kind>_flagged.json` for figures/tables/images). **Existing review state MUST be preserved**; `audit_equations.py` reads legacy bare `verified.json` / `flagged.json` and the legacy nested `audit/equations/working/` layout as fallbacks.

**Actions:**

1. Discover the source corpus by listing `_Sources/` subfolders (excluding `_Archive/`). Confirm with the user that the discovered set is the intended corpus.
2. For each admitted source:
   - Run `tools/decomp/build_source_skeleton.py --md <book>.md --asset-manifest <book>_assets_manifest.json --output-skeleton <book>_skeleton.json --output-dispatch-plan <book>_dispatch_plan.json` to produce the raw skeleton and dispatch plan.
   - Render the **section+atom** review surface: `tools/decomp/render_source_html.py --md <book>.md --asset-manifest <book>_assets_manifest.json --skeleton <book>_skeleton.json --audit-dir _Sources/<book>/audit --output-html _Sources/<book>/audit/<book>.html --output-section-nodes <book>_section_nodes.csv --mode structure` (Gate 1.5-S surface).
   - Render the **per-kind audit surfaces** (Gate 1.5-E/F/T/I and optionally 1.5-Fo):
     - `tools/equation_audit/audit_equations.py --work-dir _Sources/<book>_pdf2md_work --out-html _Sources/<book>/audit/equations.html --out-jsonl _Sources/<book>/audit/equations.jsonl`
     - `tools/source_audit/audit_figures.py --asset-manifest <book>_assets_manifest.json --audit-dir _Sources/<book>/audit --output-html _Sources/<book>/audit/figures.html`
     - `tools/source_audit/audit_tables.py --asset-manifest <book>_assets_manifest.json --audit-dir _Sources/<book>/audit --output-html _Sources/<book>/audit/tables.html`
     - `tools/source_audit/audit_images.py --asset-manifest <book>_assets_manifest.json --audit-dir _Sources/<book>/audit --output-html _Sources/<book>/audit/images.html`
     - (conditional) `tools/source_audit/audit_folios.py --page-folios-json _Sources/<book>_pdf2md_work/page_folios.json --audit-dir _Sources/<book>/audit --output-html _Sources/<book>/audit/folios.html` — only when folio extraction has been run on the source
   Each surface re-loads prior `*_verified.json` / `*_flagged.json` sidecars automatically.
3. Collect constraints (audience, organization style, required standards) and any existing taxonomies.
4. Ask clarifying questions only when required to prevent structural ambiguity (domain boundaries, intended audience, "source of truth" status).
5. Begin a **References** list (what inputs were used), listing each admitted source file by path.

**Output (in draft):**

- Domain title (TBD if unknown)
- Intake summary (high-level): for each source, report `<source_prefix>`, section count, in-scope section count (heuristic), and dispatch-unit count
- References list (with whatever anchors are available)
- Per-source `<book>_skeleton.json`, `<book>_dispatch_plan.json`, `<book>_section_nodes.csv`
- Five review surfaces per source under `_Sources/<book>/audit/`: `<book>.html` (section+atom, structure mode), `equations.html`, `figures.html`, `tables.html`, `images.html`

**Gate 1 (confirm intake understanding):**
User confirms: "Yes, the discovered source set is the intended corpus, the per-source skeleton counts look right, and the Phase-1.5 review HTMLs render correctly." Proceed to Phase 1.5.

---

#### Phase 1.5 — Source review (six sub-gates plus conditional 1.5-Fo)

**Goal:** Confirm the parsed structure of each source — skeleton outline AND every per-kind asset — before Phase-2 atomization fans out. The review work is split across six sub-gates so the human reviewer addresses one failure mode at a time. Five sub-gates are human-driven; one is a machine pre-check. A seventh sub-gate (**1.5-Fo**, printed-folio review) is **conditionally required**: it must PASS when folio extraction was run on the source (any page has `page_label_source: "vlm"` in the asset manifest); it is N/A when folio extraction was skipped.

**Sub-gates** (each surface persists state in its own `<kind>_verified.json` / `<kind>_flagged.json` sidecar; Gate 1.5 closes only when all required sub-gates PASS — six unconditional plus 1.5-Fo when conditionally required):

| Sub-gate | Driver | Surface | What the reviewer (or machine) does |
|---|---|---|---|
| **1.5-S** Skeleton | Human | `<book>.html` (section+atom, structure mode) | Confirm section outline, depth, page-range mapping; tag front/back-matter as OUT |
| **1.5-E** Equations | Human | `equations.html` | Per-equation accept/flag with LaTeX correction notes |
| **1.5-F** Figures | Human | `figures.html` | Per-figure accept/flag (caption + crop quality) |
| **1.5-T** Tables | Human | `tables.html` | Per-table accept/flag (structure + caption + `needs_extraction` triage) |
| **1.5-I** Images | Human | `images.html` | Per-image accept/flag (real asset vs. false positive) |
| **1.5-Fo** Folios | Human (conditional) | `folios.html` | Per-page accept/flag of the printed folio label emitted by `pdf2md-folio-extract`. Required only when the source has VLM-extracted folios |
| **1.5-P** Extraction reproducibility | **Machine** (prefilter) | `prose_validation.json` sidecar + proposals into `equations_backcheck.json` | Independent VLM re-extraction of each page; deterministic comparator vs. the original `<book>.md`. Strict on prose, structural on equations/asset refs, with canonicalized-LaTeX content compare emitting *proposals* for human adjudication at 1.5-E. Pages with structural fails are auto-flagged for `pdf2md-page-assets` re-dispatch before any human gate runs |

**Actions (1.5-S Skeleton, human):**

1. Open `_Sources/<book>/audit/<book>.html` in the browser.
2. Filter by `Sections only` and walk the TOC at depth ≤ 3.
3. Mark each section's review status:
   - **Verified** — correctly classified in-scope / out-of-scope.
   - **Flagged** — `is_front_matter` / `is_back_matter` flag is wrong, OR the section's content doesn't match the heuristic (chapter-internal `## REFERENCES` mis-flagged as back matter, in-scope appendix mis-classified, etc.). Use the flag-note textarea to describe the correction.
4. Export sidecars; user moves them into `_Sources/<book>/audit/`.
5. Apply review overrides to the dispatch plan: extract front-matter and back-matter overrides, then re-run `build_source_skeleton.py --front-matter-overrides <JSON> --back-matter-overrides <JSON> --output-skeleton <book>_skeleton.reviewed.json --output-dispatch-plan <book>_dispatch_plan.json` (overwrite). The reviewed skeleton replaces the raw one as the input to Phase 2.

**Actions (1.5-E / 1.5-F / 1.5-T / 1.5-I, human):**

1. Open each per-kind HTML surface in the browser, one at a time.
2. Walk the page-grouped chunks. For each chunk pick `Verified` / `Flagged`; for flagged, describe the defect in the note (wrong bbox, mis-bound caption, false-positive asset, table structure or value error, equation LaTeX correction, etc.).
3. Export the per-kind sidecars (`<source_prefix>_<kind>_verified_<TS>.json` / `<source_prefix>_<kind>_flagged_<TS>.json`). Move the latest of each into `_Sources/<book>/audit/` (rename to canonical `<kind>_verified.json` / `<kind>_flagged.json` for the next render to pick them up automatically; the renderer also auto-detects the most recent `*_<role>_*.json` if you leave the timestamped names).
4. The persona drains flagged buckets iteratively. Asset-level corrections (re-cropping a figure, re-dispatching a table for structural re-extraction, fixing an equation LaTeX) are applied by the appropriate downstream tool — `pdf2md-page-assets` re-dispatch for assets, `EQUATION_AUDIT` Phase 3 for equations — and the surface is re-rendered.

**Contract (1.5-P Extraction reproducibility prefilter, machine — implementation deferred):**

1.5-P is a three-stage pipeline that runs **before any human sub-gate** (1.5-S / E / F / T / I). Its job is to detect pages where the pdf2md extract is not reproducible, route those pages for re-dispatch, and surface machine-generated equation-fix proposals for humans to adjudicate during 1.5-E.

**Stage 1 — Skill: independent re-extraction (perception, nondeterministic).**

- **Input**: page raster `_Sources/<book>_pdf2md_work/page_NNNN.png`, plus the asset bbox manifest for that page (so the skill knows where figures/tables/images sit).
- **Process**: one `TASK + domain-prose-validate` (model: sonnet) per page. The skill is given the raster **only**, not the original `<book>.md`, to break confirmation bias. It transcribes the page to MD using a constrained output format:
  - Prose as plain Markdown paragraphs.
  - Display equations as `$$<latex>$$` (same convention as `pdf2md-page-assets`).
  - Asset regions as placeholder syntax — `[FIGURE: <caption text as printed>]`, `[TABLE: <caption text as printed>]`, `[IMAGE: <one-line description>]` — at the position the asset appears in reading order. The skill does **not** emit asset paths or link syntax (it has no asset IDs to bind to).
- **Output**: `_Sources/<book>/audit/prose_validation_extracts/page_NNNN.reextract.md`. One file per page. Independent re-extracts are themselves R5 provenance evidence and stay on disk.

**Stage 2 — Comparator: deterministic three-class compare.**

- **Input**: `_Sources/<book>_pdf2md_work/page_NNNN.md` (original) and `prose_validation_extracts/page_NNNN.reextract.md` (re-extract).
- **Process**: tokenize both into a typed stream (prose lines / equation blocks / asset placeholders), align on structural position, then compare class-by-class:
  - **Prose** — strict. Normalize (Unicode NFKC, collapse whitespace, de-hyphenate line-break hyphens, normalize smart quotes / dashes / ligatures), then byte-equal. Any divergence is a hunk.
  - **Equations** — two passes. **(2a) Presence + position match**: every `$$…$$` in the original must align with a `$$…$$` in the re-extract at roughly the same paragraph offset (and vice versa). Missing or extra equation slots are structural fails. **(2b) Canonicalize + strict-compare**: for each aligned equation pair, canonicalize the LaTeX (v1: textual normalization — `\frac` ≡ `\dfrac`, `\mathrm{}` ≡ `\rm`, `\,` spacing, brace-around-single-token, `\tag{…}` stripped; v2 if v1.x FP rate stays high after textual patches: AST canonicalization) and strict-compare the canonical forms. Differences become **proposals**, not fails — see Stage 3. **Escalation rule:** if a sample of proposals shows >30% cosmetic content **and** the cosmetic class is *not* dominated by a single fixable pattern, escalate to v2 AST. If one pattern accounts for ≥50% of cosmetic proposals (as `\tag{…}` did on the PSE pilot), write the v1.x textual rule first and re-measure before considering AST.
  - **Asset references** — every original `![alt](figures/…)` / `[XLSX](tables/…)` / `![](images/…)` must align with a `[FIGURE: …]` / `[TABLE: …]` / `[IMAGE: …]` placeholder at the same position. Missing or extra placeholders are structural fails. Caption-text divergence between original `alt` text and placeholder caption is **reported only** (1.5-F/T/I owns caption correctness with a human reviewer).
- **Output**: `_Sources/<book>/audit/prose_validation.json` keyed by `page`, schema-versioned `pdf2md-prose-validate/v1`. Each page entry carries `prose_hunks`, `equation_structural_fails`, `equation_content_proposals` (with original + re-extract + canonicalized forms), `asset_structural_fails`, `caption_notes`, and a per-class summary.

**Stage 3 — Agent: interpretation and action.**

- The persona reads `prose_validation.json` and consolidates findings:
  - **Page-level structural fails** (prose divergence above noise floor, dropped/extra equations, dropped/extra asset placeholders) → enumerate pages for **`pdf2md-page-assets` re-dispatch**. The page is re-extracted upstream; the per-kind asset manifests, `<book>.md`, and renders regenerate. 1.5-P then re-runs on the affected pages only.
  - **Equation content proposals** (canonicalized-LaTeX mismatches) → the persona dispatches `equation-flag-interpret` for each proposal to evaluate whether the re-extract's LaTeX is a likely improvement, then writes the surviving proposals into `_Sources/<book>/audit/equations_backcheck.json` with a `source: "1.5-P-machine"` field. `audit_equations.py` renders these in the existing **Backcheck** slot of `equations.html` with the proposed LaTeX visible alongside the original, badged so the human knows the proposal came from machine re-extraction (vs. a Phase-3 fix from a prior human flag).
  - **Caption notes** → recorded for context only. The 1.5-F/T/I human reviewer sees them as annotations on the figure/table/image chunk in the respective surface, but they don't pre-flag the chunk.

**Adoption / rejection of equation proposals (sticky-per-proposal):**

When the 1.5-E human reviewer picks **Verified** on a Backcheck entry, the equation moves to `equations_verified.json` as today. When they pick **Flagged**, the original is marked as needing further correction (existing pipeline).

A third action is needed: **Reject proposal** — the human is saying "this specific machine fix is wrong, but I am not yet attesting the original is correct." This writes `(equation_hash, proposal_hash)` to `_Sources/<book>/audit/equations_rejected.json`. On subsequent 1.5-P runs, the comparator suppresses any proposal whose `(equation_hash, proposal_hash)` is in the rejected sidecar — but if the canonicalizer evolves or the re-extract produces a *different* proposal (different `proposal_hash`) for the same equation, it surfaces again. Rejection is scoped to the proposal, never silently upgraded into verification of the equation. `audit_equations.py` adds a `Reject proposal` action visible only on Backcheck entries with `source: "1.5-P-machine"`.

**1.5-P is purely additive — never verification, never exemption.**

The comparator can route human attention **TO** content (via proposals, structural fails, page-level pre-flags) but cannot route attention **AWAY** from any content. This applies symmetrically across all three classes:

- **Equation content match between extracts is silent but NOT verification.** Both VLM extracts can canonicalize-equal because they both made the same error against the printed equation. 1.5-P never writes to `equations_verified.json` or `equations_flagged.json`. The only equation-state sidecar it writes is `equations_backcheck.json` (proposals). The human at 1.5-E remains the sole authority that can verify any equation.
- **Prose-line match between extracts is silent but NOT verification.** 1.5-P never marks any prose region as reviewed; it only flags divergences.
- **Asset-placeholder structural match is silent but NOT verification.** Presence and position of a placeholder in both extracts does not attest that the asset's caption or crop is correct. 1.5-F/T/I remain the sole authorities.
- **Page-level "no 1.5-P findings" status is silent but NOT exemption.** Atoms inheriting from such a page proceed through normal Gate-2 atom review with no 1.5-P-induced pre-flags AND no 1.5-P-induced exemption from review.

**Effect on downstream sub-gates and Gate 2:**

- 1.5-S / 1.5-F / 1.5-T / 1.5-I run on pages that have cleared 1.5-P structural checks. Reviewers see fewer obviously-broken pages, but every chunk still requires human attestation.
- 1.5-E inherits machine proposals as pre-populated Backcheck entries (no new surface required).
- At Gate 2, atoms inheriting from a page that has unresolved 1.5-P findings (open proposals or pending re-dispatch) are auto-pre-flagged in the atom review sidecar. Atoms from pages with no 1.5-P findings proceed through normal review with neither pre-flag nor exemption — 1.5-P silence is never an attestation.

**Status**: implemented. `tools/source_audit/{tokenize_md,normalize_prose,canonicalize_latex,compare_extracts,validate_prose}.py` are the deterministic Stage 2 modules. `skills/domain-prose-validate/` is the Stage 1 skill. `tools/decomp/build_prose_validate_brief.py` + `tools/source_audit/run_prose_validation.py` are the dispatch/aggregation helpers for Stage 3. `audit_equations.py` renders the 1.5-P-machine source badge and the Reject-proposal action on Backcheck entries, with `equations_rejected.json` suppression sticky per `(equation_hash, proposal_hash)`.

**Output (in draft):**

- `<book>_skeleton.reviewed.json` per source
- Updated `<book>_dispatch_plan.json` per source (excludes reviewer-confirmed out-of-scope sections)
- Six sidecar JSON families under `_Sources/<book>/audit/`: `sections_*`, `equations_*` (legacy `verified.json` / `flagged.json` honored; `equations_backcheck.json` populated by both EQUATION_AUDIT Phase 3 fixes and 1.5-P machine proposals; `equations_rejected.json` for sticky-per-proposal rejections), `figures_*`, `tables_*`, `images_*`, plus the 1.5-P artifacts: `prose_validation.json` and the per-page re-extracts under `prose_validation_extracts/`

**Gate 1.5 (all required sub-gates must PASS):**
Ordering: **1.5-P first** as a machine prefilter — it consumes raw `<book>.md` + page rasters (no human input required) and routes structurally-broken pages back through `pdf2md-page-assets` re-dispatch before any human time is spent. Once 1.5-P's open structural fails are zero (proposals may still be open; those are adjudicated inline at 1.5-E), the human sub-gates run: **1.5-S** next (locks the skeleton + dispatch scope), then **1.5-E** / **1.5-F** / **1.5-T** / **1.5-I** in any order (the four per-kind surfaces are independent), plus **1.5-Fo** when folio extraction was run on the source. Proceed to Phase 2 only when all required sub-gates pass.

---

#### Phase 2 — Normalize (per-dispatch-unit atomization via TASK fan-out)

**Goal:** Convert each in-scope dispatch unit into a per-unit atomic-unit CSV via a bounded `TASK + domain-source-atomize` invocation, then merge across all units of all sources into the consolidated Domain Ledger. Gate 2 closes on the merged ledger via browser-mediated review.

**Chunking strategy (delegated to the skill):**

Per-unit atomization is performed by `skills/domain-source-atomize/`. The skill applies the same **semantic-bounded chunking** rules previously documented inline — each atom corresponds to one instruction, one concept, or one requirement; the smallest standalone unit of meaning. The skill's `SKILL.md` is the authoritative specification of the chunking and classification rules; this doctrine retains them for orchestrator-side awareness:

- atomic-unit text MUST contain semantic instructional content only — page numbers, running headers, orphan reference markers, OCR/extraction artifacts, and standalone boilerplate are stripped from `UnitStatement` and (when retained as anchors) live in the dual `SourceRef`;
- a chunk whose entire content is boilerplate (only a page number, only a running header, only a publisher slug) MUST NOT be promoted to its own atom;
- every chunk is classified IN / OUT / TBD per the binding rules in `SKILL.md` (front/back-matter rules subsumed by the Phase-1.5 reviewed skeleton; the persona's reviewed skeleton determines the in-scope line range fed to the skill).

**Dispatch flow (per source):**

1. For each source's `<book>_dispatch_plan.json`:
   1. For each `unit_id` in the plan's `units` list:
      1. Render the INIT-TASK brief: `python3 tools/decomp/build_atomization_brief.py --dispatch-plan <book>_dispatch_plan.json --unit-id <unit_id> --md <book>.md --skeleton <book>_skeleton.reviewed.json --asset-manifest <book>_assets_manifest.json --output-ledger-path _Decomposition/_atomization_work/<book>/dispatch_<unit_id>_atoms.csv --output-vocab-seed-path _Decomposition/_atomization_work/<book>/dispatch_<unit_id>_vocab.csv`.
      2. Dispatch the brief to `TASK` with `TaskSkill: domain-source-atomize`. TASK loads the skill and the worker reads ONLY the assigned line range.
      3. Capture `RUN_STATUS` and per-unit counts; record in the dispatch log.
   2. Batches of 4–8 units MAY run in parallel; the per-unit CSVs are written to disjoint paths.
   3. Failed units (`RUN_STATUS=FAILED` / `FAILED_INPUTS`) are re-dispatched in isolation after the persona diagnoses the input issue.
2. When all dispatch units for a source have produced per-unit CSVs:
   - Run `tools/decomp/merge_source_atomizations.py per-source --dispatch-plan <book>_dispatch_plan.json --unit-csv-glob '<work>/<book>_dispatch_*_atoms.csv' --source-prefix <PREFIX> --source-name <book> --output <book>_atomic_units.csv --strict-coverage`. The merge assigns stable `HBA-<PREFIX>-NNNNN` IDs in skeleton order, validates `LocalSeq` monotonicity per unit, re-derives `ContentHash` to verify integrity, dedupes by hash, and fails fast on missing units.
3. When all sources have per-source CSVs:
   - Run `tools/decomp/merge_source_atomizations.py cross-source --per-source <book1>_atomic_units.csv --per-source <book2>_atomic_units.csv ... --output Atomic_Domain_Ledger.csv`. The cross-source merge concatenates, validates ID-prefix uniqueness, surfaces unresolved cross-source `Corrects` references, and adds `SourceDoc` + `SourcePrefix` columns.
4. Consolidate vocabulary:
   - Run `tools/decomp/merge_vocabulary_seeds.py --seed <book1>_vocabulary_seed.csv --source-doc <book1> --seed <book2>_vocabulary_seed.csv --source-doc <book2> ... --output Vocabulary_Map.csv`. (Per-source vocab seeds are produced by merging each source's per-unit `<book>_dispatch_<unit_id>_vocab.csv` outputs ahead of this step — typically by simple concat, since the per-unit outputs are already source-local.)
5. Re-render each source's `<book>.html` in `atom-review` mode (sections + atoms):
   - Run `tools/decomp/render_source_html.py --md <book>.md --asset-manifest <book>_assets_manifest.json --skeleton <book>_skeleton.reviewed.json --audit-dir _Sources/<book>/audit --output-html _Sources/<book>/audit/<book>.html --output-section-nodes <book>_section_nodes.csv --mode atom-review --atomic-units-csv <book>_atomic_units.csv`. Each in-scope section now carries its mapped atoms as a reviewable list next to the source-page image. Per-asset review state from Phase 1.5 (`equations.html` / `figures.html` / `tables.html` / `images.html`) stays where it is — those surfaces don't need re-rendering for Gate 2.

**Gate-2 human review (browser-mediated):**

The user opens each source's regenerated `<book>.html` and reviews atoms via filter chips:

- **`Only TBD`** — chase down every TBD atom; the persona reviews the user's flag notes and re-classifies via per-source persona dispatch or manual edit.
- **`Only flagged`** — atoms flagged for content drift, mis-atomization, or boundary issues.
- **`Only OUT`** — verify boilerplate is correctly classified out.
- **`Only IN`** — spot-check substantive atoms by section.

Sidecar exports from each browser session land in `_Sources/<book>/audit/`. The persona drains the flagged buckets iteratively until `flagged_count = 0` (or all flags resolved with resolution notes).

**Output (in draft):**

- Per-unit atom CSVs (`_Decomposition/_atomization_work/<book>/dispatch_*_atoms.csv`) — immutable after merge closes
- Per-unit vocab seed CSVs (`_Decomposition/_atomization_work/<book>/dispatch_*_vocab.csv`)
- Per-source ledger (`<book>_atomic_units.csv`)
- Merged Domain Ledger (`Atomic_Domain_Ledger.csv`)
- Merged Vocabulary Map (`Vocabulary_Map.csv`)
- Updated per-source HTML in `atom-review` mode
- Sidecar exports under `_Sources/<book>/audit/`

**Gate 2 (confirm normalization):**
User confirms: "Yes, the merged Domain Ledger reflects the corpus content, the IN/OUT/TBD classifications are correct (flagged atoms = 0 or all flags resolved with resolution notes), the cleaning rule was applied correctly, and the vocabulary choices are acceptable." Proceed to Phase 2.5.

---

#### Phase 2.5 — Retrieval prep (deterministic sub-step, not a gate)

**Goal:** Build the V2 source database and retrieval index needed by Gate 3 / Gate 4 ratification.

**Actions:**

1. Run `tools/source_catalog/build_source_database.py --domain-root <domain-root>`. This builds the domain-local source catalog snapshot under `<domain-root>/_LocalIndexes/` from `_Sources/`, audit sidecars, section nodes, and decomposition CSVs. Source files are referenced in place by path and SHA-256; they are not copied into the database.
2. Run `tools/retrieval/build_source_index.py --snapshot <domain-root>/_LocalIndexes/_LATEST.md`. This builds BM25 + dense retrieval sidecars inside the same source database snapshot.
3. Build the cross-source TOC reconciliation prior: `tools/decomp/build_toc_priors.py --skeleton <book1>_skeleton.reviewed.json --skeleton <book2>_skeleton.reviewed.json ... --output-md cross_source_toc_matrix.md --output-csv cross_source_toc_matrix.csv`.

The source database, retrieval sidecars, and TOC matrix MUST refresh whenever source files, audit sidecars, section nodes, or the Domain Ledger change (e.g., post-Gate-2 fix).

This step is deterministic and non-conversational; no user gate.

**Output:**

- `<domain-root>/_LocalIndexes/_LATEST.md` (pointer to current source database snapshot)
- `<domain-root>/_LocalIndexes/snapshots/SRCIDX_<UTC>/` (catalog + retrieval sidecars)
- `cross_source_toc_matrix.{md,csv}`

---

#### Phase 3 — Define Categories (cross-source TOC reconciliation)

**Goal:** Partition IN-scope Handbook Units into flat Categories with no overlap and no gaps. The Phase-3 starting point is the cross-source TOC matrix — each admitted source's TOC is itself an expert decomposition, and Categories are proposed as a reconciliation of those structures.

**Actions:**

1. Open `cross_source_toc_matrix.md` to inspect each source's TOC side by side. Inspect `cross_source_toc_matrix.csv` for high-overlap section pairs (Jaccard ≥ 0.3 or shared_count ≥ 3) as alignment candidates.
2. Propose Categories (flat list) as a reconciliation of the cross-source structures:
   - `CategoryID` (`CAT-###`, stable),
   - `Name` and `ScopeDescription`,
   - `InclusionCriteria` (optional),
   - `Exclusions` (optional),
   - **`SourceAlignment`** (new field, optional): citations to specific sections across sources that motivate the category, with notes indicating where authors agree, diverge, or supersede.
3. Assign each **IN** Handbook Unit to exactly one Category.
4. If a unit appears to belong to multiple Categories:
   - keep units atomic and force a decision, **or**
   - split the unit into smaller units (user-confirmed). Unit splits change `UnitStatement` text for the affected rows and therefore invalidate their embeddings + BM25 tokens.

**Index-refresh trigger:** If Phase 3 admits any unit splits, the source database and source retrieval index MUST be rebuilt before scope ratification opens.

**Gate 3 prerequisite — retrieval-driven Category scope ratification (binding):**

Before Gate 3 may close, every proposed Category MUST pass a retrieval-driven scope ratification check. Catching scope-vs-content drift at the Category level (10-ish entities) prevents it from propagating into KTY proposals at Phase 4 (dozens of entities). Same five-verdict shape as KTY ratification.

**Precondition (hard):** The source database snapshot at `<domain-root>/_LocalIndexes/_LATEST.md` MUST be current with respect to source files, audit sidecars, section nodes, and the Domain Ledger. The snapshot's `Chunks.csv` and retrieval sidecars MUST be current before ratification queries run.

**Procedure (per Category):**

1. Confirm the precondition above.
2. For each proposed Category, formulate a scope query string from the Category Name and ScopeDescription (plus InclusionCriteria / Exclusions when present).
3. Query the V2 source index with the scope string, using filters as needed to inspect `LEDGER_ATOM`, `SECTION_NODE`, or mixed chunk results; take top-`k` results (default `k = max(50, 2 * MappedAtomCount)`).
4. Compute the overlap between the top-`k` retrieval result set and the set of atoms currently mapped to the Category.
5. Compare semantic similarity (cosine) between the scope query embedding and each mapped atom's embedding; flag atoms below the configured cosine threshold (default `0.75`).

**Verdicts** (identical shape to KTY ratification):

| Verdict | Definition | Blocking? |
|---|---|---|
| `CLUSTER_COHERENT` | High overlap between top-k retrieval and mapped atoms; mapped-atom similarity at or above threshold | No |
| `SCOPE_REFINEMENT_NEEDED` | Mapped atoms are topically related but the Category Name/ScopeDescription does not crisply describe them; rename or rewrite the description | **Yes** |
| `SCOPE_TOO_BROAD` | Top-k retrieval returns many atoms not mapped to this Category but topically aligned with its scope; Category should be split or its scope tightened | **Yes** |
| `SCOPE_TOO_NARROW` | Mapped atoms span topics the Category scope does not cover; Category should be broadened, or atoms re-clustered into the correct Categories | **Yes** |
| `LOW_COHESION` | Mapped atoms have low pairwise similarity even though they satisfy the scope query; advisory only | No |

**Per-atom Category-assignment retrieval check:**

In addition to per-Category ratification, run a per-atom assignment check: for each IN atom, query the atom index with the atom's assigned Category scope and verify the atom itself appears in top-`k`. Atoms that fail to retrieve under their assigned Category's scope are flagged as **misassignment candidates** and routed back for user review. This makes the "no gaps / no overlaps" invariant machine-checkable instead of merely asserted.

Blocking Category-level verdicts route back to Phase 3 Category refinement (rename, rewrite ScopeDescription, split, merge, or reassign atoms). Misassignment candidates route to per-atom review. Gate 3 cannot close while any Category carries a blocking verdict or while unresolved misassignment candidates remain.

The full per-Category verdict set is recorded as a companion register (`Category_Scope_Ratification.csv`); the misassignment candidate list is recorded as `Category_Assignment_Findings.csv`. Both surface in the Decision Log.

**Output (in draft):**

- Category list with `SourceAlignment` citations
- Unit→Category assignment (in the Domain Ledger)
- `Category_Scope_Ratification.csv` (per-Category verdicts)
- `Category_Assignment_Findings.csv` (per-atom misassignment candidates, if any)

**Gate 3 (confirm categories):**
User confirms: "Yes, Categories are correct, each IN-scope unit belongs to exactly one Category, every Category carries a `CLUSTER_COHERENT` ratification verdict, and all misassignment candidates have been resolved (advisory `LOW_COHESION` findings reviewed and accepted)."

---

#### Phase 4 — Define Knowledge Types (within each Category)

**Goal:** Define Knowledge Types that operationalize the domain into reusable units of structured knowledge.

**Actions:**

For each Knowledge Type:
- Stable ID: `KTY-CC-TT_{shortDescription}` (stable; hyphenated category/type pair plus descriptive suffix)
- Name
- Description (what knowledge it contains and why it exists)
- Intended users / roles (TBD allowed)
- When used / triggers (TBD allowed)
- **Canonical schema** (best-effort; may be one of the standard schemas below or custom; `TBD` allowed)

For each Knowledge Subject (within its parent Knowledge Type):
- Stable ID: `SUB-CC-TT-SS_{shortDescription}` (stable; extends parent KTY index with two-digit subject index)
- Name
- Description (the specific domain topic this subject addresses)
- Best-effort unit linkage (`CoversUnits`)

**Standard schema options (recommended, not mandatory):**
- **Procedure**: Purpose, Scope, Preconditions, Inputs, Steps, Outputs, Quality Checks, Exceptions, References
- **Checklist**: Purpose, When to Use, Checklist Items, Acceptance Criteria, References
- **Template**: Purpose, Fields/Sections, Instructions, Examples, References
- **Guidance / Playbook**: When to Use, Principles, Options, Decision Points, Examples, References
- **Reference**: Definition, Scope, Related Concepts, Do/Don't, References

**Output (in draft):**

- Knowledge Type list grouped by Category
- Knowledge Subject list grouped by Knowledge Type
- Knowledge Type and Subject attribute tables
- Unit→Subject mapping in the Domain Ledger (best-effort; gaps surfaced)

**Gate 4 prerequisite — retrieval-driven KTY scope ratification (binding):**

Before Gate 4 may close, every proposed Knowledge Type MUST pass a retrieval-driven scope ratification check. This verifies that a KTY's declared scope (Name + Description) matches the atomic content actually mapped to it.

**Precondition (hard):** The atom retrieval index MUST be current with respect to the Domain Ledger's `UnitStatement` content.

**Procedure (per KTY):**

1. Confirm the precondition above.
2. For each proposed KTY, formulate a scope query string from the KTY Name and Description.
3. Query the index with the scope string; take top-`k` results (default `k = max(20, 2 * MappedAtomCount)`), optionally filtered to the parent Category.
4. Compute the overlap between the top-`k` retrieval result set and the set of atoms currently mapped to the KTY.
5. Compare semantic similarity (cosine) between the scope query embedding and each mapped atom's embedding; flag atoms below the configured cosine threshold (default `0.75`).

**Verdicts:**

| Verdict | Definition | Blocking? |
|---|---|---|
| `CLUSTER_COHERENT` | High overlap between top-k retrieval and mapped atoms; mapped-atom similarity at or above threshold | No |
| `SCOPE_REFINEMENT_NEEDED` | Mapped atoms are topically related but the KTY Name/Description does not crisply describe them; rename or rewrite the Description | **Yes** |
| `SCOPE_TOO_BROAD` | Top-k retrieval returns many atoms not mapped to this KTY but topically aligned with its scope; KTY should be split or its scope tightened | **Yes** |
| `SCOPE_TOO_NARROW` | Mapped atoms span topics the KTY scope does not cover; KTY should be broadened, or atoms re-clustered into the correct KTYs | **Yes** |
| `LOW_COHESION` | Mapped atoms have low pairwise similarity even though they satisfy the scope query; advisory only — does not block, but the user is shown the finding | No |

**Blocking verdicts route back to Phase 4 KTY refinement** (rename, rewrite Description, split, merge, or re-cluster atoms) and the ratification check is re-run. Gate 4 cannot close while any KTY carries a blocking verdict.

The full per-KTY verdict set is recorded as a companion register (`KTY_Scope_Ratification.csv`) and surfaced in the Decision Log.

**Gate 4 (confirm Knowledge Types):**
User confirms: "Yes, Knowledge Types, Knowledge Subjects, schemas, and responsibilities are acceptable, and every KTY carries a `CLUSTER_COHERENT` ratification verdict (advisory `LOW_COHESION` findings reviewed and accepted)."

---

#### Phase 5 — Verify Coverage (anti-fragile checks + browser-mediated section coverage)

**Goal:** Prove that decomposition covers the handbook's IN-scope content and make gaps visible and trackable. Section-level coverage is attested by the user in the browser.

**Actions:**

1. Verify every **IN** Handbook Unit is:
   - assigned to exactly one Category (required),
   - mapped to at least one Knowledge Type (best-effort; missing mappings are open issues).
2. Verify each Knowledge Type belongs to exactly one Category (required).
3. Compute section coverage telemetry:
   - For each in-scope section across all sources, count atoms mapped to that section.
   - Tabulate coverage density (atoms per ~50 source lines).
   - Flag zero-coverage sections as open issues.
4. Re-render each source's `<book>.html` in `coverage-review` mode (sections only):
   - `tools/decomp/render_source_html.py ... --mode coverage-review --atomic-units-csv <book>_atomic_units.csv`. Each section is color-coded by atom-coverage density (cov-empty / cov-low / cov-mid / cov-high). The per-kind asset surfaces are not part of Gate 5 — coverage is a section-level property.
5. The user opens each source's HTML and reviews `cov-empty` sections in particular, attesting that:
   - the zero-coverage is acceptable (e.g., section is true preamble / boilerplate; OR the section will be filled by scope-change cycles per AOP-08's scaffold-for-fill rule),
   - OR the zero-coverage indicates a Phase-2 gap that warrants re-dispatching the affected unit.
6. Produce **Coverage & Telemetry** summary (required).

**Output (in draft):**

- Coverage & Telemetry section with counts and open issues, including section coverage density
- Open Issues list referencing stable IDs (`HBA-<PREFIX>-NNNNN`, `CAT-###`, `KTY-CC-TT_*`, `SUB-CC-TT-SS_*`, `SEC-<PREFIX>-NNNN`)
- Updated per-source HTML in `coverage-review` mode
- Section coverage sidecar exports under `_Sources/<book>/audit/` (`<source_prefix>_sections_coverage_<TS>.json`)

**Gate 5 (confirm verification):**
User confirms: "Coverage and mappings are acceptable; section-coverage gaps have been ruled on (accepted as scaffold-for-fill OR routed back for Phase-2 re-dispatch); open issues list is correct."

---

#### Phase 6 — Publish the Domain Decomposition (finalize)

**Goal:** Produce the final domain decomposition document as a single coherent artifact suitable for downstream agents.

**Actions:**

- Ensure the document includes:
  - Domain Ledger (required),
  - Coverage & Telemetry (required, with section coverage telemetry),
  - Vocabulary Map (required),
  - Categories, Knowledge Types, Knowledge Subjects,
  - Decision log / change log (required),
  - Companion Inventory (required, listing all new register classes from Phase 1–5).
- Confirm all per-source HTML review surfaces are in their final state with sidecar history archived.
- Summarize what changed since last revision.

**Gate 6 (final acceptance):**
User confirms: "This domain decomposition is the accepted basis for downstream work."

---

[[END:PROTOCOL]]

[[BEGIN:SPEC]]
## SPEC

### Normative — "What must it be?"

This section defines requirements for a valid domain decomposition.

### Completeness requirements

A decomposition is complete when:

| Requirement | Validation |
|---|---|
| Handbook normalized | Domain Ledger exists; each row has an `AtomicUnitID` (`HBA-<PREFIX>-NNNNN`), `UnitStatement`, `ContentHash`, IN/OUT/TBD status |
| Per-source skeleton lifted | Every source has `<book>_skeleton.reviewed.json` and `<book>_dispatch_plan.json` |
| Per-source HTML render present | Every source has `<book>.html` in atom-review mode for Gate 2 and coverage-review mode for Gate 5 |
| Section nodes captured | Every source has `<book>_section_nodes.csv` populated |
| Dispatch coverage | Every dispatch unit in every dispatch plan produced a per-unit CSV; the merge tool succeeded with `--strict-coverage` |
| Cross-source TOC matrix present | `cross_source_toc_matrix.md` and `cross_source_toc_matrix.csv` exist and were consulted at Phase 3 |
| Categories flat and scoped | Category list exists; each category has a scope description; `SourceAlignment` populated when reconciliation across sources motivated the category |
| Category scope ratified | Every Category carries a `CLUSTER_COHERENT` verdict in the Category Scope Ratification register; no misassignment candidates remain open |
| Category coverage | Every IN-scope Handbook Unit is assigned to exactly one Category |
| Knowledge Types defined | Knowledge Types exist within each Category with IDs and (best-effort) schemas |
| KTY scope ratified | Every Knowledge Type carries a `CLUSTER_COHERENT` verdict in the KTY Scope Ratification register |
| Type assignment | Every Knowledge Type belongs to exactly one Category |
| Subjects defined | Each Knowledge Type contains at least one Knowledge Subject (TBD allowed) |
| Subject assignment | Every Knowledge Subject belongs to exactly one Knowledge Type |
| Domain Ledger present | Atomic_Domain_Ledger.csv exists with stable IDs, dual SourceRefs, ContentHash, and mappings |
| Section coverage attested | Every in-scope section's atom-coverage status is either non-zero or explicitly attested as scaffold-for-fill at Gate 5 |
| Coverage & Telemetry present | Summary metrics, section coverage telemetry, and open issue taxonomy exist |
| Vocabulary Map present | Canonical terms ↔ synonyms table exists, merged from per-source seeds |

### Consistency requirements

A decomposition is consistent when:

| Requirement | Validation |
|---|---|
| No unit overlaps | An IN-scope unit is not assigned to multiple categories |
| No unit gaps | No IN-scope unit remains unassigned to a category |
| Stable IDs | IDs do not change across revisions unless explicitly requested |
| Source prefixes unique | Every source's `SourcePrefix` is unique within the corpus |
| ContentHash integrity | Every Domain Ledger row's `ContentHash = sha1(UnitStatement)[:12]` |
| LocalSeq integrity | Within each dispatch unit, per-unit CSVs had strictly monotonic `LocalSeq` (validated at merge time) |
| Cross-source `Corrects` resolution | Every non-empty `Corrects` reference resolves to a real AtomicUnitID in the merged ledger (warnings on misses are surfaced) |
| Terminology consistent | Canonical terms are used consistently; synonyms are mapped |
| Decisions explicit | Non-trivial assignment decisions are recorded and referencable |

### Per-source skill output validity (Phase 2)

For every per-unit atom CSV emitted by `domain-source-atomize`:

| Requirement | Validation |
|---|---|
| Schema | Header is exactly `LocalSeq,UnitStatement,SourceRef,ContentHash,InOutStatus,SectionID,DispatchUnitID,Corrects,Notes` |
| Line-range discipline | Every row's MD line in `SourceRef` falls within the dispatch unit's `LINE_START..LINE_END` |
| Target-section discipline | Every row's `SectionID` is in the dispatch unit's `TARGET_SECTION_IDS` |
| LocalSeq | Strictly increasing positive integers from 1 |
| ContentHash | Non-empty, 12 lowercase hex chars, equals `sha1(UnitStatement)[:12]` |
| InOutStatus | One of `IN`, `OUT`, `TBD` |
| Dual SourceRef | Both halves present: `<book>.md:L####|<book>.html#anchor` |

The `merge_source_atomizations.py per-source` step enforces these; failures block ledger assembly.

### Anti-patterns (invalid outputs)

| Anti-pattern | Why it fails |
|---|---|
| Inventing domain content or rules | Breaks grounding; corrupts downstream knowledge generation |
| Nested categories | Breaks partition invariants; complicates automation |
| Silent ambiguity resolution | Hides defects; makes later reconciliation impossible |
| No stable IDs | Prevents tracking and longitudinal comparison |
| Per-unit worker assigning final stable AtomicUnitIDs | Breaks merge-time ID-assignment contract; merge will fail |
| ContentHash mismatch | Breaks dedup, retrieval freshness, and HTML cross-reference |
| Discarding the per-source HTML review surface as "derived" | It is the authoritative Gate-2 / Gate-5 review surface; treat it as a companion register |
| Bypassing the dispatch plan and doing inline atomization | Re-introduces the context-budget problem this revision exists to solve |

[[END:SPEC]]

[[BEGIN:STRUCTURE]]
## STRUCTURE

### Descriptive — "What is it?"

This section defines the entities and required tables in the decomposition output.

### Required entities

#### Handbook Unit (Atom)
- `AtomicUnitID` (stable; format `HBA-<SOURCE_PREFIX>-NNNNN`; e.g., `HBA-PSE-00042`)
- `UnitStatement` (normalized atomic instruction/concept; cleaned per the skill's rules — semantic content only; no page numbers, running headers, or standalone boilerplate)
- `SourceRef` (dual citation: `<book>.md:L####|<book>.html#anchor` — the MD line for grep-style navigation, the HTML anchor for browser-mediated review)
- `ContentHash` (`sha1(UnitStatement)[:12]`; load-bearing — matches the `data-key` content-hash on the corresponding HTML review chunk; re-derived and verified at merge time)
- `InOutStatus` (`IN|OUT|TBD`)
- `SectionID` (the target section the atom belongs to within its source's reviewed skeleton)
- `DispatchUnitID` (the unit_id that produced this atom; useful for failure-isolation reruns)
- `LocalSeq` (within-unit ordering; useful for tracing back to the per-unit CSV)
- `SourceDoc` (the source's doc_stem; added at cross-source merge)
- `SourcePrefix` (the source's prefix; added at cross-source merge)
- `Corrects` (optional; for errata/corrigenda atoms — references `AtomicUnitID(s)` of the atom(s) being corrected; cross-source references are allowed)
- `Notes`

#### Section Node
- `SectionID` (stable; format `SEC-<SOURCE_PREFIX>-NNNN`)
- `SourceDoc`, `SourcePrefix`
- `Path` (TOC path, e.g., `Ch3 § 3.5`)
- `Depth` (heading depth)
- `Title`
- `LineStart`, `LineEnd` (1-indexed line range in the source MD)
- `PageFirst`, `PageLast`
- `HtmlAnchor` (e.g., `<book>.html#SEC-PSE-0042`)
- `ContentHash` (of the section's title + body; load-bearing for the HTML review chunk's `data-key`)
- `InScope` (`True|False`; from `<book>_skeleton.reviewed.json`)
- `IsFrontMatter`, `IsBackMatter` (`True|False`)
- `FigureRefs`, `TableRefs`, `EquationRefs` (semicolon-separated inline reference labels)
- `AssetIDs` (semicolon-separated asset_ids inlined within the section's line range)
- `Text` (cleaned section body for indexing)

#### Dispatch Unit
- `unit_id` (`UNIT-<SOURCE_PREFIX>-NNNN`)
- `line_start`, `line_end`
- `target_section_ids`
- `estimated_md_tokens`
- `contains_oversized_section` (true if the unit is a single section that exceeded `--section-split-threshold` and could not be further subdivided)

#### Category
- `CategoryID` (stable; e.g., `CAT-001`)
- `Name`
- `ScopeDescription`
- `InclusionCriteria` (optional)
- `Exclusions` (optional)
- `SourceAlignment` (optional; notes citing the source sections / authors whose decompositions motivate this Category, including agree/diverge/supersede markers)

#### Knowledge Type
- `KnowledgeTypeID` (stable; follows `KTY-CC-TT_{shortDescription}`)
- `Name`
- `ParentCategoryID`
- `Description`
- `IntendedUsers` (`TBD` allowed)
- `WhenUsed` (`TBD` allowed)
- `CanonicalSchema` (best-effort; may be `TBD`)

#### Knowledge Subject
- `SubjectID` (stable; e.g., `SUB-03-02-01_{shortDescription}`)
- `Name`
- `ParentKnowledgeTypeID`
- `Description`
- `CoversUnits` (best-effort; AtomicUnitIDs)
- `Notes`

---

### Required tables/sections in the Domain Decomposition Document

#### 1) Vocabulary Map (table)
Minimum columns:
- `CanonicalTerm`
- `Synonyms`
- `Notes`

Plus, when produced by `merge_vocabulary_seeds.py`:
- `Definition`, `SourceDocs`, `SourceRefs`, `SourceCount`

**Scope (per AOP-07):** Vocabulary Map scope is **bounded** to niche, novel, or ambiguous terms in the domain that genuinely warrant explicit disambiguation. General domain vocabulary that a competent language-model reader would know from context is out of scope. Sparse coverage is expected and is not a defect. Downstream auditors SHOULD NOT flag a sparsely populated Vocabulary Map as missing-data on this basis alone.

#### 2) Domain Ledger (table)
Minimum columns:
- `AtomicUnitID`
- `SourceDoc`, `SourcePrefix`
- `LocalSeq`
- `UnitStatement` (cleaned semantic content only)
- `SourceRef` (dual citation `<book>.md:L####|<book>.html#anchor`)
- `ContentHash` (`sha1(UnitStatement)[:12]`)
- `InOutStatus`
- `SectionID` (the target section in the reviewed skeleton)
- `DispatchUnitID`
- `CategoryID` (required for IN; optional/blank for OUT — assigned at Gate 3)
- `KnowledgeTypeID(s)` (one or many; or `TBD` — assigned at Gate 4)
- `SubjectID(s)` (one or many; or `TBD` — assigned at Gate 4)
- `Corrects` (optional; for errata atoms — cross-source allowed)
- `DecisionRef` (optional; points to Decision Log entry)
- `OpenIssue` (`TRUE|FALSE`)
- `Notes`

**Hard rule:** Every **IN** `AtomicUnitID` has exactly one `CategoryID`.
**Hard rule:** Retrieval indexes built over the Domain Ledger MUST use `UnitStatement` only for token/embedding text. Provenance/source-anchor info lives in `SourceRef` and is queryable as metadata but never tokenized into BM25 or embedded.

#### 3) Coverage & Telemetry (summary block)
Minimum fields:
- `UnitCount` (total Domain Ledger rows)
- `INUnitCount`, `OUTUnitCount`, `TBDUnitCount`
- `SourceCount`
- `SectionCount` (total across all sources)
- `InScopeSectionCount`
- `SectionsWithZeroCoverageCount` (with IDs; surfaced as scaffold-for-fill at Gate 5)
- `SectionCoverageDensityDistribution` (cov-empty / cov-low / cov-mid / cov-high counts)
- `CategoryCount`
- `KnowledgeTypeCount`
- `SubjectCount`
- `UnassignedINUnits` (must be 0 for acceptance)
- `UnitsWithoutKnowledgeTypeMapping` (count)
- `OpenIssuesByType` (counts, with IDs)
- `Revision` identifier and date

**Scaffold-for-fill (per AOP-08):** Zero-AU surfaces — Knowledge Types, Knowledge Subjects, or in-scope Sections with no atomic-unit rows in the Domain Ledger — are an intentional *scaffold-for-fill* state when explicitly attested at Gate 5. Such surfaces are populated subsequently by source-driven scope-change cycles (see `agents/AGENT_SCOPE_CHANGE.md`) operating against `_Sources/` (or the package's equivalent source-fidelity authority). They MUST NOT be filled by invented content. Sparse-or-empty coverage at initial publication is expected for surfaces awaiting backfill and is not a defect on this basis alone. Downstream auditors SHOULD distinguish "scaffold awaiting source-driven fill" from "decomposition defect" via the Gate-5 attestation log.

#### 4) Open Issues list
- A list of unresolved items referencing stable IDs:
  - `HBA-<PREFIX>-NNNNN`, `CAT-###`, `KTY-CC-TT_{shortDescription}`, `SUB-CC-TT-SS_{shortDescription}`, `SEC-<PREFIX>-NNNN`, `UNIT-<PREFIX>-NNNN` (failed dispatches)

#### 5) Decision Log / Change Log
- A small section where non-trivial choices are recorded so later work can trace why boundaries were set.

**Granularity (per AOP-05):** Decision Log granularity is **policy-only**: it records gate promotions, scoping policies, cross-source reconciliation rulings, and other non-trivial assignment decisions. It is **not** a per-unit assignment journal.

#### 6) Companion Inventory
- A table listing every companion register in the canonical working package.
- Minimum columns:
  - `Filename`
  - `PackageRole` (`authoritative companion register` | `derived publication artifact` | `snapshot / handoff artifact`)
  - `Description` (brief purpose of the file)
- This section enables downstream agents to discover the full package layout without scanning the filesystem.

---

[[END:STRUCTURE]]

[[BEGIN:RATIONALE]]
## RATIONALE

### Why the workflow scales by per-dispatch-unit fan-out

The prior DOMAIN_DECOMP doctrine assumed a single conversational agent performs Phase-2 atomization (semantic-bounded chunking, IN/OUT/TBD classification, Vocabulary Map seeding) inline. This breaks above ~100k tokens. The piping-design test corpus is 5 books × ~50,000 MD lines (≈ multi-million tokens once figures, tables, and equations are resolved). The per-dispatch-unit fan-out — each unit ~15k MD tokens, mapping to one bounded `TASK + domain-source-atomize` worker — is the same pattern used by PDF2MD (per page) and DRAWING_EXTRACT (per page). The persona's job becomes orchestration: render the plan, dispatch, merge, review. The heavy lifting moves into bounded workers whose context budget is comfortable.

### Why each source is an admitted expert decomposition

MWK 1956, Bausbacher, Weaver V1/V2, and Peng 2009 each encode a senior practitioner's partition of piping design into chapters/sections/figures/tables. Re-decomposing without lifting that structure throws away signal. The per-source skeleton lift (`build_source_skeleton.py`) preserves it; the cross-source TOC matrix (`build_toc_priors.py`) makes the alignment visible so Phase 3 can reconcile rather than re-invent.

### Why the consolidated SDO is uniquely valuable because the sources disagree

The five sources frame their domain differently (MWK 1956 uses the Kellogg flexibility tradition; Peng 2009 uses modern ASME). They supersede one another on specific topics. No single source is authoritative for the cross-source domain. Cross-source reconciliation — surfaced via the TOC matrix at Phase 3, recorded in `SourceAlignment` on each Category, and traced through Gate-3 retrieval-ratification — is the unique work the SDO does. Replacing the SDO with hyperlinked HTML would lose it.

### Why the per-source HTML is the human-review surface

Gate-2 review of 25k+ atoms is intractable in chat. Gate-5 attestation of section coverage across 1,500+ sections is similarly intractable. The audit-pattern HTML — content-hash `data-key`s, filter chips (only-flagged / only-TBD / only-OUT / by-kind), sticky stat counters, localStorage + timestamped sidecar exports — is the same pattern that successfully sustains equation-audit review of multi-thousand-equation corpora. Generalized to atoms + sections + figures + tables + equations, it is the right substrate.

### Why ContentHash is on the Domain Ledger

`sha1(UnitStatement)[:12]` is the bridge between the ledger and the HTML review surface. When the user clicks "verified" on an atom in the browser, the sidecar JSON records `atom:<content-hash> → verified_at`. When the HTML is re-rendered after a ledger edit, atoms whose `UnitStatement` changed self-invalidate (their hash changes) and drop out of verified state — which is the correct behavior, because the underlying text changed and the prior review no longer applies. This same self-invalidation principle is proven in `audit_equations.py` (equations keyed by `sha1(latex)[:12]`).

### Why stable IDs survive the per-dispatch-unit pattern

Per-unit workers emit `LocalSeq` only; final stable `HBA-<PREFIX>-NNNNN` IDs are assigned at merge time by walking dispatch units in skeleton order. This makes per-unit dispatches stateless and re-runnable (a failed unit re-runs independently and yields the same atoms by content hash), while preserving I5's stable-ID invariant for the merged ledger. Within the merged ledger, IDs remain stable across revisions unless the user explicitly requests renumbering.

### Why retrieval-driven Gate-3 and Gate-4 ratification remain binding

The retrieval-driven scope ratification was the prior doctrine's strongest anti-fragile mechanism. This revision retains it through the V2 source index, where ledger atoms, section nodes, audit sidecars, and source chunks share one typed query substrate. It is the machine-checkable answer to "do the proposed Categories / Knowledge Types actually fit the atoms mapped to them?"

### Why the existing equation-audit sidecars are preserved

The per-source `audit/` artifacts represent real human review work (e.g., MWK_1956 has 28 verified + 9 flagged equations across ~250 audited equations). Discarding that state on re-render would be a regression. `load_sidecar_with_fallback` and the hash-based fallback (`build_eq_hash_index`) ensure that prior equation review carries through to the new render, even when the legacy `<page>:<hash>` keys have drifted to slightly different pages in the assembled markdown.

[[END:RATIONALE]]
