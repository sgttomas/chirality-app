# domain-decomp — method

## Method

### Operational — "How to do?"

This section defines the orchestrator procedure for handbook/domain decomposition. WORKING_ITEMS operates as a conversation-shell orchestrator; heavy lifting moves to deterministic tools and bounded TASK dispatches.

### Output Target

The agent maintains a **canonical working package** during the conversation (a living draft consisting of the main decomposition document, per-source HTML review surfaces, and companion registers), and repeatedly revises it after user feedback until it passes the combined source checkpoint and three grouped decomposition checkpoints in SPEC.

For the combined source checkpoint and each accepted group, finalize
`checkpoint_snapshots/<checkpoint>-<UTC>/{DECISION.md,ACCEPTED_MANIFEST.csv,HANDOFF_STATE.md}`
and then update `_LATEST_SOURCE.md`, `_LATEST_GROUP1.md`, `_LATEST_GROUP2.md`,
or `_LATEST_ACCEPTED.md` as applicable. Each later stage begins by resolving
and consuming the preceding accepted snapshot. A reopened decision produces a
successor snapshot and never overwrites accepted history.

### Phases

#### Source-basis preparation — intake and initial rendering

**Goal:** Receive the handbook(s) and constraints and reflect them back faithfully. Lift each source's TOC skeleton and produce a Phase-1.5 review surface.

**Source-corpus location (binding convention):**

Working source materials live under `_Sources/` within the domain's package root. The agent reads all subfolders of `_Sources/` **except `_Sources/_Archive/`**.

- `_Sources/<subfolder>/` — active source materials (handbook text, manuals, derived markdown, asset manifests). These are the admitted basis for the decomposition. Atomic Handbook Units anchor their `SourceRef` to these files per the AOP-08 source-fidelity invariant.
- `_Sources/_Archive/` — upstream / original material used to produce the active source files (e.g., the PDFs that were extracted into the working markdown). **Not part of the working corpus.** Consult this folder only when an active source appears wrong and needs upstream confirmation; anything found here is evidence-only and is never the primary admission.
- `_Sources/<subfolder>/audit/` — the per-source audit folder. All five per-kind audit surfaces (`equations.html`, `figures.html`, `tables.html`, `images.html`) plus the reduced `<book>.html` (section + atom review) live here as siblings, along with their kind-prefixed sidecars (`equations_verified.json` / `equations_flagged.json` / `equations_backcheck.json` and analogous `<kind>_verified.json` / `<kind>_flagged.json` for figures/tables/images). **Existing review state MUST be preserved**; `audit_equations.py` reads legacy bare `verified.json` / `flagged.json` and the legacy nested `audit/equations/working/` layout as fallbacks.

**Actions:**

1. Discover the proposed source corpus by listing `_Sources/` subfolders (excluding `_Archive/`). Record the discovered set for the combined source-admission/fidelity checkpoint.
2. For each admitted source:
   - Run `tools/decomp/build_source_skeleton.py --md <book>.md --asset-manifest <book>_assets_manifest.json --output-skeleton <book>_skeleton.json --output-dispatch-plan <book>_dispatch_plan.json` to produce the raw skeleton and dispatch plan.
   - Render the **section+atom** review surface: `tools/decomp/render_source_html.py --md <book>.md --asset-manifest <book>_assets_manifest.json --skeleton <book>_skeleton.json --audit-dir _Sources/<book>/audit --output-html _Sources/<book>/audit/<book>.html --output-section-nodes <book>_section_nodes.csv --mode structure`.
   - Render the **per-kind audit surfaces** used for the combined checkpoint:
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

#### Source-fidelity preparation — structure, assets, and reproducibility

**Goal:** Prepare a consolidated assessment of each proposed source's parsed
structure, prose reproducibility, equations, figures, tables, images, and
folios before atomization. Review tracks isolate failure modes, but they feed
one source-admission/fidelity decision. Folio review is required when folio
extraction ran and otherwise records `NOT_APPLICABLE`.

**Review tracks** (each surface persists state in its own `<kind>_verified.json` / `<kind>_flagged.json` sidecar; all required tracks are complete before the combined checkpoint):

| Track | Driver | Surface | What the reviewer (or machine) does |
|---|---|---|---|
| **S** Skeleton | Human review | `<book>.html` (section+atom, structure mode) | Confirm section outline, depth, page-range mapping; tag front/back-matter as OUT |
| **E** Equations | Human review | `equations.html` | Per-equation accept/flag with LaTeX correction notes |
| **F** Figures | Human review | `figures.html` | Per-figure accept/flag (caption + crop quality) |
| **T** Tables | Human review | `tables.html` | Per-table accept/flag (structure + caption + `needs_extraction` triage) |
| **I** Images | Human review | `images.html` | Per-image accept/flag (real asset vs. false positive) |
| **Fo** Folios | Human review (conditional) | `folios.html` | Per-page accept/flag of the printed folio label emitted by `pdf2md-folio-extract`. Required only when the source has VLM-extracted folios |
| **P** Extraction reproducibility | **Machine** (prefilter) | `prose_validation.json` sidecar + proposals into `equations_backcheck.json` | Independent VLM re-extraction of each page; deterministic comparator vs. the original `<book>.md`. Strict on prose, structural on equations/asset refs, with canonicalized-LaTeX content compare emitting proposals for review in track E. Pages with structural fails are auto-flagged for `pdf2md-page-assets` re-dispatch before the combined checkpoint |

**Actions (track S, human review):**

1. Open `_Sources/<book>/audit/<book>.html` in the browser.
2. Filter by `Sections only` and walk the TOC at depth ≤ 3.
3. Mark each section's review status:
   - **Verified** — correctly classified in-scope / out-of-scope.
   - **Flagged** — `is_front_matter` / `is_back_matter` flag is wrong, OR the section's content doesn't match the heuristic (chapter-internal `## REFERENCES` mis-flagged as back matter, in-scope appendix mis-classified, etc.). Use the flag-note textarea to describe the correction.
4. Export sidecars; user moves them into `_Sources/<book>/audit/`.
5. Apply review overrides to the dispatch plan: extract front-matter and back-matter overrides, then re-run `build_source_skeleton.py --front-matter-overrides <JSON> --back-matter-overrides <JSON> --output-skeleton <book>_skeleton.reviewed.json --output-dispatch-plan <book>_dispatch_plan.json` (overwrite). The reviewed skeleton replaces the raw one as the input to Phase 2.

**Actions (tracks E / F / T / I, human review):**

1. Open each per-kind HTML surface in the browser, one at a time.
2. Walk the page-grouped chunks. For each chunk pick `Verified` / `Flagged`; for flagged, describe the defect in the note (wrong bbox, mis-bound caption, false-positive asset, table structure or value error, equation LaTeX correction, etc.).
3. Export the per-kind sidecars (`<source_prefix>_<kind>_verified_<TS>.json` / `<source_prefix>_<kind>_flagged_<TS>.json`). Move the latest of each into `_Sources/<book>/audit/` (rename to canonical `<kind>_verified.json` / `<kind>_flagged.json` for the next render to pick them up automatically; the renderer also auto-detects the most recent `*_<role>_*.json` if you leave the timestamped names).
4. WORKING_ITEMS drains flagged buckets iteratively. Asset-level corrections (re-cropping a figure, re-dispatching a table for structural re-extraction, fixing an equation LaTeX) are applied by the appropriate downstream tool — `pdf2md-page-assets` re-dispatch for assets, `WORKING_ITEMS (workflow: equation-audit)` Phase 3 for equations — and the surface is re-rendered.

**Contract (track P extraction reproducibility prefilter, machine):**

Track P is a three-stage pipeline that runs before the human review tracks. Its
job is to detect pages where the pdf2md extract is not reproducible, route those
pages for re-dispatch, and surface machine-generated equation-fix proposals for
review during track E.

**Stage 1 — Skill: independent re-extraction (perception, nondeterministic).**

- **Input**: page raster `_Sources/<book>_pdf2md_work/page_NNNN.png`, plus the asset bbox manifest for that page (so the workflow knows where figures/tables/images sit).
- **Process**: one `TASK + domain-prose-validate` (model: as specified by the user at dispatch time; requires a a vision-capable model selected for this run) per page. The workflow is given the raster **only**, not the original `<book>.md`, to break confirmation bias. It transcribes the page to MD using a constrained output format:
  - Prose as plain Markdown paragraphs.
  - Display equations as `$$<latex>$$` (same convention as `pdf2md-page-assets`).
  - Asset regions as placeholder syntax — `[FIGURE: <caption text as printed>]`, `[TABLE: <caption text as printed>]`, `[IMAGE: <one-line description>]` — at the position the asset appears in reading order. The workflow does **not** emit asset paths or link syntax (it has no asset IDs to bind to).
- **Output**: `_Sources/<book>/audit/prose_validation_extracts/page_NNNN.reextract.md`. One file per page. Independent re-extracts are themselves R5 provenance evidence and stay on disk.

**Stage 2 — Comparator: deterministic three-class compare.**

- **Input**: `_Sources/<book>_pdf2md_work/page_NNNN.md` (original) and `prose_validation_extracts/page_NNNN.reextract.md` (re-extract).
- **Process**: tokenize both into a typed stream (prose lines / equation blocks / asset placeholders), align on structural position, then compare class-by-class:
  - **Prose** — strict. Normalize (Unicode NFKC, collapse whitespace, de-hyphenate line-break hyphens, normalize smart quotes / dashes / ligatures), then byte-equal. Any divergence is a hunk.
  - **Equations** — two passes. **(2a) Presence + position match**: every `$$…$$` in the original must align with a `$$…$$` in the re-extract at roughly the same paragraph offset (and vice versa). Missing or extra equation slots are structural fails. **(2b) Canonicalize + strict-compare**: for each aligned equation pair, canonicalize the LaTeX (v1: textual normalization — `\frac` ≡ `\dfrac`, `\mathrm{}` ≡ `\rm`, `\,` spacing, brace-around-single-token, `\tag{…}` stripped; v2 if v1.x FP rate stays high after textual patches: AST canonicalization) and strict-compare the canonical forms. Differences become **proposals**, not fails — see Stage 3. **Escalation rule:** if a sample of proposals shows >30% cosmetic content **and** the cosmetic class is *not* dominated by a single fixable pattern, escalate to v2 AST. If one pattern accounts for ≥50% of cosmetic proposals (as `\tag{…}` did on the PSE pilot), write the v1.x textual rule first and re-measure before considering AST.
  - **Asset references** — every original `![alt](figures/…)` / `[XLSX](tables/…)` / `![](images/…)` must align with a `[FIGURE: …]` / `[TABLE: …]` / `[IMAGE: …]` placeholder at the same position. Missing or extra placeholders are structural fails. Caption-text divergence between original `alt` text and placeholder caption is **reported only** (1.5-F/T/I owns caption correctness with a human reviewer).
- **Output**: `_Sources/<book>/audit/prose_validation.json` keyed by `page`, schema-versioned `pdf2md-prose-validate/v1`. Each page entry carries `prose_hunks`, `equation_structural_fails`, `equation_content_proposals` (with original + re-extract + canonicalized forms), `asset_structural_fails`, `caption_notes`, and a per-class summary.

**Stage 3 — Agent: interpretation and action.**

- WORKING_ITEMS reads `prose_validation.json` and consolidates findings:
  - **Page-level structural fails** (prose divergence above noise floor, dropped/extra equations, dropped/extra asset placeholders) → enumerate pages for **`pdf2md-page-assets` re-dispatch**. The page is re-extracted upstream; the per-kind asset manifests, `<book>.md`, and renders regenerate. 1.5-P then re-runs on the affected pages only.
  - **Equation content proposals** (canonicalized-LaTeX mismatches) → WORKING_ITEMS dispatches `equation-flag-interpret` for each proposal to evaluate whether the re-extract's LaTeX is a likely improvement, then writes the surviving proposals into `_Sources/<book>/audit/equations_backcheck.json` with a `source: "1.5-P-machine"` field. `audit_equations.py` renders these in the existing **Backcheck** slot of `equations.html` with the proposed LaTeX visible alongside the original, badged so the human knows the proposal came from machine re-extraction (vs. a Phase-3 fix from a prior human flag).
  - **Caption notes** → recorded for context only. The 1.5-F/T/I human reviewer sees them as annotations on the figure/table/image chunk in the respective surface, but they don't pre-flag the chunk.

**Adoption / rejection of equation proposals (sticky-per-proposal):**

When the 1.5-E human reviewer picks **Verified** on a Backcheck entry, the equation moves to `equations_verified.json` as today. When they pick **Flagged**, the original is marked as needing further correction (existing pipeline).

A third action is needed: **Reject proposal** — the human is saying "this specific machine fix is wrong, but I am not yet attesting the original is correct." This writes `(equation_hash, proposal_hash)` to `_Sources/<book>/audit/equations_rejected.json`. On subsequent 1.5-P runs, the comparator suppresses any proposal whose `(equation_hash, proposal_hash)` is in the rejected sidecar — but if the canonicalizer evolves or the re-extract produces a *different* proposal (different `proposal_hash`) for the same equation, it surfaces again. Rejection is scoped to the proposal, never silently upgraded into verification of the equation. `audit_equations.py` adds a `Reject proposal` action visible only on Backcheck entries with `source: "1.5-P-machine"`.

**1.5-P is purely additive — never verification, never exemption.**

The comparator can route human attention **TO** content (via proposals, structural fails, page-level pre-flags) but cannot route attention **AWAY** from any content. This applies symmetrically across all three classes:

- **Equation content match between extracts is silent but NOT verification.** Both VLM extracts can canonicalize-equal because they both made the same error against the printed equation. 1.5-P never writes to `equations_verified.json` or `equations_flagged.json`. The only equation-state sidecar it writes is `equations_backcheck.json` (proposals). The human at 1.5-E remains the sole authority that can verify any equation.
- **Prose-line match between extracts is silent but NOT verification.** 1.5-P never marks any prose region as reviewed; it only flags divergences.
- **Asset-placeholder structural match is silent but NOT verification.** Presence and position of a placeholder in both extracts does not attest that the asset's caption or crop is correct. 1.5-F/T/I remain the sole authorities.
- **Page-level "no track-P findings" status is silent but NOT exemption.** Atoms inheriting from such a page proceed through normal normalized-scope review with no machine-induced pre-flags and no machine-induced exemption from review.

**Effect on the remaining review tracks and normalized-scope review:**

- 1.5-S / 1.5-F / 1.5-T / 1.5-I run on pages that have cleared 1.5-P structural checks. Reviewers see fewer obviously-broken pages, but every chunk still requires human attestation.
- 1.5-E inherits machine proposals as pre-populated Backcheck entries (no new surface required).
- During normalized-scope review, atoms inheriting from a page that has unresolved track-P findings (open proposals or pending re-dispatch) are auto-pre-flagged in the atom review sidecar. Atoms from pages with no track-P findings proceed through normal review with neither pre-flag nor exemption — machine silence is never an attestation.

**Status**: implemented. `tools/source_audit/{tokenize_md,normalize_prose,canonicalize_latex,compare_extracts,validate_prose}.py` are the deterministic Stage 2 modules. `workflows/domain-prose-validate/` is the Stage 1 workflow. `tools/decomp/build_prose_validate_brief.py` + `tools/source_audit/run_prose_validation.py` are the dispatch/aggregation helpers for Stage 3. `audit_equations.py` renders the 1.5-P-machine source badge and the Reject-proposal action on Backcheck entries, with `equations_rejected.json` suppression sticky per `(equation_hash, proposal_hash)`.

**Output (in draft):**

- `<book>_skeleton.reviewed.json` per source
- Updated `<book>_dispatch_plan.json` per source (excludes reviewer-confirmed out-of-scope sections)
- Six sidecar JSON families under `_Sources/<book>/audit/`: `sections_*`, `equations_*` (legacy `verified.json` / `flagged.json` honored; `equations_backcheck.json` populated by both WORKING_ITEMS (workflow: equation-audit) Phase 3 fixes and 1.5-P machine proposals; `equations_rejected.json` for sticky-per-proposal rejections), `figures_*`, `tables_*`, `images_*`, plus the 1.5-P artifacts: `prose_validation.json` and the per-page re-extracts under `prose_validation_extracts/`

**Combined source-admission and fidelity checkpoint:** Run track P first and
drain structural repairs. Then complete track S and the applicable asset tracks,
iterating repairs and re-renders as needed. Present the proposed admitted corpus,
skeleton/dispatch scope, unresolved fidelity exceptions, and all track evidence
as one reviewable package. The human accepts or revises source admission and
fidelity in one decision. Asset-quality evidence informs this checkpoint and
routes repair work; it never creates a separate workflow prompt. Atomization
may begin only after this checkpoint is accepted.

After acceptance, finalize the source-admission/fidelity snapshot, update
`_LATEST_SOURCE.md`, and consume it as the atomization basis.

---

#### Checkpoint group 1 preparation — normalized scope and meaning

**Goal:** Convert each in-scope dispatch unit into a per-unit atomic-unit CSV via a bounded `TASK + domain-source-atomize` invocation, then merge across all units of all sources into the consolidated Domain Ledger. Checkpoint group 1 decides the merged ledger through browser-mediated review.

**Chunking strategy (delegated to the workflow):**

Per-unit atomization is performed by `workflows/domain-source-atomize/`. The workflow applies the same **semantic-bounded chunking** rules previously documented inline — each atom corresponds to one instruction, one concept, or one requirement; the smallest standalone unit of meaning. The workflow's `WORKFLOW.md` is the authoritative specification of the chunking and classification rules; this doctrine retains them for orchestrator-side awareness:

- atomic-unit text MUST contain semantic instructional content only — page numbers, running headers, orphan reference markers, OCR/extraction artifacts, and standalone boilerplate are stripped from `UnitStatement` and (when retained as anchors) live in the dual `SourceRef`;
- a chunk whose entire content is boilerplate (only a page number, only a running header, only a publisher slug) MUST NOT be promoted to its own atom;
- every chunk is classified IN / OUT / TBD per the binding rules in `WORKFLOW.md` (front/back-matter rules subsumed by the Phase-1.5 reviewed skeleton; WORKING_ITEMS's reviewed skeleton determines the in-scope line range fed to the workflow).

**Dispatch flow (per source):**

1. For each source's `<book>_dispatch_plan.json`:
   1. For each `unit_id` in the plan's `units` list:
      1. Render the INIT-TASK brief: `python3 tools/decomp/build_atomization_brief.py --dispatch-plan <book>_dispatch_plan.json --unit-id <unit_id> --md <book>.md --skeleton <book>_skeleton.reviewed.json --asset-manifest <book>_assets_manifest.json --output-ledger-path _Decomposition/_atomization_work/<book>/dispatch_<unit_id>_atoms.csv --output-vocab-seed-path _Decomposition/_atomization_work/<book>/dispatch_<unit_id>_vocab.csv`.
      2. Dispatch the brief to `TASK` with `Workflow: domain-source-atomize`. TASK loads the workflow and the worker reads ONLY the assigned line range.
      3. Capture `RUN_STATUS` and per-unit counts; record in the dispatch log.
   2. Batches of 4–8 units MAY run in parallel; the per-unit CSVs are written to disjoint paths.
   3. Failed units (`RUN_STATUS=FAILED` / `FAILED_INPUTS`) are re-dispatched in isolation after WORKING_ITEMS diagnoses the input issue.
2. When all dispatch units for a source have produced per-unit CSVs:
   - Run `tools/decomp/merge_source_atomizations.py per-source --dispatch-plan <book>_dispatch_plan.json --unit-csv-glob '<work>/<book>_dispatch_*_atoms.csv' --source-prefix <PREFIX> --source-name <book> --output <book>_atomic_units.csv --strict-coverage`. The merge assigns stable `HBA-<PREFIX>-NNNNN` IDs in skeleton order, validates `LocalSeq` monotonicity per unit, re-derives `ContentHash` to verify integrity, dedupes by hash, and fails fast on missing units.
3. When all sources have per-source CSVs:
   - Run `tools/decomp/merge_source_atomizations.py cross-source --per-source <book1>_atomic_units.csv --per-source <book2>_atomic_units.csv ... --output Atomic_Domain_Ledger.csv`. The cross-source merge concatenates, validates ID-prefix uniqueness, surfaces unresolved cross-source `Corrects` references, and adds `SourceDoc` + `SourcePrefix` columns.
4. Consolidate vocabulary:
   - Run `tools/decomp/merge_vocabulary_seeds.py --seed <book1>_vocabulary_seed.csv --source-doc <book1> --seed <book2>_vocabulary_seed.csv --source-doc <book2> ... --output Vocabulary_Map.csv`. (Per-source vocab seeds are produced by merging each source's per-unit `<book>_dispatch_<unit_id>_vocab.csv` outputs ahead of this step — typically by simple concat, since the per-unit outputs are already source-local.)
5. Re-render each source's `<book>.html` in `atom-review` mode (sections + atoms):
   - Run `tools/decomp/render_source_html.py --md <book>.md --asset-manifest <book>_assets_manifest.json --skeleton <book>_skeleton.reviewed.json --audit-dir _Sources/<book>/audit --output-html _Sources/<book>/audit/<book>.html --output-section-nodes <book>_section_nodes.csv --mode atom-review --atomic-units-csv <book>_atomic_units.csv`. Each in-scope section now carries its mapped atoms as a reviewable list next to the source-page image. Per-asset review state from the source-fidelity preparation stays where it is; those surfaces do not need re-rendering for checkpoint group 1.

**Checkpoint-group-1 review preparation (browser-mediated):**

The user opens each source's regenerated `<book>.html` and reviews atoms via filter chips:

- **`Only TBD`** — chase down every TBD atom; WORKING_ITEMS reviews the user's flag notes and re-classifies via per-source bounded TASK dispatch or manual edit.
- **`Only flagged`** — atoms flagged for content drift, mis-atomization, or boundary issues.
- **`Only OUT`** — verify boilerplate is correctly classified out.
- **`Only IN`** — spot-check substantive atoms by section.

Sidecar exports from each browser session land in `_Sources/<book>/audit/`. WORKING_ITEMS drains the flagged buckets iteratively until `flagged_count = 0` (or all flags resolved with resolution notes).

**Output (in draft):**

- Per-unit atom CSVs (`_Decomposition/_atomization_work/<book>/dispatch_*_atoms.csv`) — immutable after merge closes
- Per-unit vocab seed CSVs (`_Decomposition/_atomization_work/<book>/dispatch_*_vocab.csv`)
- Per-source ledger (`<book>_atomic_units.csv`)
- Merged Domain Ledger (`Atomic_Domain_Ledger.csv`)
- Merged Vocabulary Map (`Vocabulary_Map.csv`)
- Updated per-source HTML in `atom-review` mode
- Sidecar exports under `_Sources/<book>/audit/`

**Checkpoint group 1 — normalized scope and meaning:** Present the merged
Domain Ledger, Handbook Units, `IN | OUT | TBD` classifications, dual source
bindings, vocabulary, resolved flags, and remaining meaning conflicts together.
The human confirms or revises this normalized representation of the admitted
corpus.

After acceptance, finalize the group-1 snapshot, update `_LATEST_GROUP1.md`,
and consume it as the structural-retrieval basis.

---

#### Structural retrieval preparation (deterministic, not a checkpoint)

**Goal:** Build the V2 source database and retrieval index needed for the Category and Knowledge Type checks before checkpoint group 2.

**Actions:**

1. Run `tools/source_catalog/build_source_database.py --domain-root <domain-root>`. This builds the domain-local source catalog snapshot under `<domain-root>/_LocalIndexes/` from `_Sources/`, audit sidecars, section nodes, and decomposition CSVs. Source files are referenced in place by path and SHA-256; they are not copied into the database.
2. Run `tools/retrieval/build_source_index.py --snapshot <domain-root>/_LocalIndexes/_LATEST.md`. This builds BM25 + dense retrieval sidecars inside the same source database snapshot.
3. Build the cross-source TOC reconciliation prior: `tools/decomp/build_toc_priors.py --skeleton <book1>_skeleton.reviewed.json --skeleton <book2>_skeleton.reviewed.json ... --output-md cross_source_toc_matrix.md --output-csv cross_source_toc_matrix.csv`.

The source database, retrieval sidecars, and TOC matrix MUST refresh whenever source files, audit sidecars, section nodes, or the Domain Ledger change (for example after a checkpoint-group-1 repair).

This step is deterministic and non-conversational; it creates no human checkpoint.

**Output:**

- `<domain-root>/_LocalIndexes/_LATEST.md` (pointer to current source database snapshot)
- `<domain-root>/_LocalIndexes/snapshots/SRCIDX_<UTC>/` (catalog + retrieval sidecars)
- `cross_source_toc_matrix.{md,csv}`

---

#### Checkpoint group 2 preparation, part A — define Categories

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

**Index-refresh trigger:** If Category work admits any unit splits, the source database and source retrieval index MUST be rebuilt before scope ratification opens.

**Category check — retrieval-driven scope ratification (binding):**

Before checkpoint group 2 may be presented, every proposed Category MUST pass a retrieval-driven scope ratification check. Catching scope-vs-content drift at the Category level prevents it from propagating into Knowledge Type proposals. The check has the same five-verdict shape as KTY ratification.

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

Blocking Category-level verdicts route back to Category refinement (rename, rewrite ScopeDescription, split, merge, or reassign atoms). Misassignment candidates route to per-atom review. Checkpoint group 2 is not ready while any Category carries a blocking verdict or unresolved misassignment candidates remain.

The full per-Category verdict set is recorded as a companion register (`Category_Scope_Ratification.csv`); the misassignment candidate list is recorded as `Category_Assignment_Findings.csv`. Both surface in the Decision Log.

**Output (in draft):**

- Category list with `SourceAlignment` citations
- Unit→Category assignment (in the Domain Ledger)
- `Category_Scope_Ratification.csv` (per-Category verdicts)
- `Category_Assignment_Findings.csv` (per-atom misassignment candidates, if any)

Continue directly into the Knowledge Type and Knowledge Subject proposal. The
Category proposal and its findings are decided with the rest of the domain
structure at checkpoint group 2.

#### Checkpoint group 2 preparation, part B — define Knowledge Types and Subjects

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

**Knowledge Type check — retrieval-driven scope ratification (binding):**

Before checkpoint group 2 may be presented, every proposed Knowledge Type MUST pass a retrieval-driven scope ratification check. This verifies that a KTY's declared scope (Name + Description) matches the atomic content actually mapped to it.

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

**Blocking verdicts route back to KTY refinement** (rename, rewrite Description, split, merge, or re-cluster atoms) and the ratification check is re-run. Checkpoint group 2 is not ready while any KTY carries a blocking verdict.

The full per-KTY verdict set is recorded as a companion register (`KTY_Scope_Ratification.csv`) and surfaced in the Decision Log.

**Checkpoint group 2 — Category, Knowledge Type, and Knowledge Subject
structure:** Present the Categories, Knowledge Types, Knowledge Subjects,
schemas, mappings, Category and KTY ratification registers, coverage findings,
and exceptions as one reviewable structure. The human confirms or revises the
domain structure and the recorded treatment of advisory findings.

After acceptance, finalize the group-2 snapshot, update `_LATEST_GROUP2.md`,
and consume it as the final-coverage and audit basis.

---

#### Checkpoint group 3 preparation, part A — verify coverage

**Goal:** Prove that decomposition covers the handbook's IN-scope content and make gaps visible and trackable. Section-level coverage findings and proposed scaffold-for-fill dispositions are prepared for the final grouped decision.

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
   - `tools/decomp/render_source_html.py ... --mode coverage-review --atomic-units-csv <book>_atomic_units.csv`. Each section is color-coded by atom-coverage density (cov-empty / cov-low / cov-mid / cov-high). Per-kind asset surfaces remain source-basis evidence; final coverage is a section-level property.
5. Inspect `cov-empty` sections and prepare one of these proposed dispositions
   for the final checkpoint:
   - zero coverage is acceptable because the section is true preamble or
     boilerplate;
   - zero coverage is an explicit scaffold-for-fill candidate under AOP-08;
   - zero coverage is an atomization gap that requires re-dispatch before the
     final checkpoint.
6. Produce **Coverage & Telemetry** summary (required).

**Output (in draft):**

- Coverage & Telemetry section with counts and open issues, including section coverage density
- Open Issues list referencing stable IDs (`HBA-<PREFIX>-NNNNN`, `CAT-###`, `KTY-CC-TT_*`, `SUB-CC-TT-SS_*`, `SEC-<PREFIX>-NNNN`)
- Updated per-source HTML in `coverage-review` mode
- Section coverage sidecar exports under `_Sources/<book>/audit/` (`<source_prefix>_sections_coverage_<TS>.json`)

Do not ask for a separate coverage decision. Carry the coverage package and
proposed dispositions into checkpoint group 3.

#### Checkpoint group 3 preparation, part B — independent audit and final package

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
- Dispatch a separate review instance that did not author the candidate. Audit
  the complete package against the accepted source checkpoint and checkpoint
  groups 1 and 2. Resolve mechanical defects and expose substantive findings.

**Checkpoint group 3 — audited final acceptance:** Present the audited final
package, coverage evidence, scaffold-for-fill proposals, open issues, and
independent review findings. The human accepts the domain decomposition as the
basis for downstream use or returns affected parts for repair. Publication or
output writing occurs around the accepted state and does not add a checkpoint.

After acceptance, finalize the group-3 immutable snapshot under
`{DECOMP_ROOT}/checkpoint_snapshots/<snapshot>/`. Write
`ACCEPTED_MANIFEST.csv` with the accepted artifact paths, package roles, and
hashes, and write `HANDOFF_STATE.md` with the accepted source and checkpoint
basis, derivative status, closure verdict, rerun requirements, and remaining
blockers. Update `{DECOMP_ROOT}/checkpoint_snapshots/_LATEST_ACCEPTED.md` only
after those members are complete. This finalization records checkpoint group 3;
it does not create another human checkpoint. Historical `gate_snapshots/`
packages and pointers remain valid legacy evidence and are not renamed.

If admitted material changes after a checkpoint, identify the affected source
bindings and reopen only the decisions whose meaning, structure, mappings, or
consequences depend on that material. Refresh the source database, retrieval
evidence, coverage, and independent audit only where affected.

---
