---
name: domain-source-atomize
description: Per-dispatch-unit bounded atomization of one slice of one DOMAIN source markdown into IN/OUT/TBD atomic units with dual SourceRefs, content hashes, and vocabulary seeds. Invoked by the DOMAIN_DECOMP orchestrator for per-skeleton-dispatch-unit fanout in Phase 2.
compatibility: Chirality TASK; invoked by DOMAIN_DECOMP orchestrator for per-dispatch-unit fanout
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL — domain-source-atomize

## Purpose

Read **one assigned slice** (LINE_START..LINE_END) of **one source's `<book>.md`** and emit two CSVs:

1. **Atomic-unit ledger** (`OUTPUT_LEDGER_PATH`) — one row per atomic unit extracted from the slice, with monotonic `LocalSeq`, dual `SourceRef`, `ContentHash`, IN/OUT/TBD classification, and target `SectionID`.
2. **Vocabulary seed** (`OUTPUT_VOCAB_SEED_PATH`) — candidate canonical terms surfaced from the slice with source attribution.

This is a **bounded extraction** skill, not a full-source analysis skill. One invocation processes one dispatch unit (~15k MD tokens) and writes exactly the two artifacts above. Cross-source reconciliation, ID assignment, and gate decisions are not part of this skill — the orchestrator handles them.

## Suitable agent shells

- `TASK` in generic shell mode, spawned by the `DOMAIN_DECOMP` orchestrator.

Not the best fit for:
- whole-book atomization (use multiple dispatches via the orchestrator)
- cross-source vocabulary reconciliation (orchestrator + `merge_vocabulary_seeds.py`)
- final stable-ID assignment (merge step's responsibility via `merge_source_atomizations.py`)
- IN/OUT ratification across multiple sources (Gate 2 persona responsibility)

## Inputs

### Required (via `RuntimeOverrides`)

- `SOURCE_NAME` — the source's doc_stem (e.g., `Pipe-Stress-Engineering`)
- `SOURCE_PREFIX` — short prefix used downstream for ID assignment (e.g., `PSE`)
- `DISPATCH_UNIT_ID` — the dispatch unit being atomized (e.g., `UNIT-PSE-0007`)
- `MD_PATH` — absolute path to the assembled `<book>.md`
- `LINE_START`, `LINE_END` — 1-indexed line range to read (inclusive); the assigned slice
- `TARGET_SECTION_IDS` — list of `SectionID`s covered by the dispatch unit; every emitted atom must map to one
- `SKELETON_PATH` — absolute path to `<book>_skeleton.json` (read for section metadata only)
- `ASSET_MANIFEST_PATH` — absolute path to `<book>_assets_manifest.json` (for asset-aware references)
- `OUTPUT_LEDGER_PATH` — absolute path for the per-unit atom CSV
- `OUTPUT_VOCAB_SEED_PATH` — absolute path for the per-unit vocabulary seed CSV

### Optional

- `MAX_ATOMS` — bound for smoke testing; halt and write what you have when reached
- `SOURCE_HTML_PATH` — when known, used as the second half of the dual `SourceRef` anchor

## Runtime overrides

| Key | Meaning | Default | Allowed values |
|---|---|---|---|
| `SOURCE_NAME` | Doc stem | **Required** | String |
| `SOURCE_PREFIX` | ID prefix | **Required** | String |
| `DISPATCH_UNIT_ID` | Unit identifier | **Required** | `UNIT-<prefix>-NNNN` |
| `MD_PATH` | Path to `<book>.md` | **Required** | Existing `.md` file |
| `LINE_START` | First line to read | **Required** | Positive integer |
| `LINE_END` | Last line to read | **Required** | Positive integer ≥ `LINE_START` |
| `TARGET_SECTION_IDS` | Section IDs to map atoms into | **Required** | List of `SEC-<prefix>-NNNN` |
| `SKELETON_PATH` | Path to skeleton JSON | **Required** | Existing `.json` file |
| `ASSET_MANIFEST_PATH` | Path to asset manifest | **Required** | Existing `.json` file |
| `OUTPUT_LEDGER_PATH` | Per-unit atom CSV | **Required** | Parent dir exists; `.csv` |
| `OUTPUT_VOCAB_SEED_PATH` | Per-unit vocab CSV | **Required** | Parent dir exists; `.csv` |
| `MAX_ATOMS` | Smoke-test bound | None | Positive integer |
| `SOURCE_HTML_PATH` | `<book>.html` URL or path | None | String |

## Read boundary

Reads are limited to:

- `MD_PATH` — but ONLY lines `LINE_START..LINE_END` inclusive. Lines outside that range MUST NOT be inspected.
- `SKELETON_PATH` — read in full for section metadata (titles, depth, in-scope status).
- `ASSET_MANIFEST_PATH` — read in full for asset metadata (figure/table captions, page numbers).

The skill MUST NOT read any other source files, other sources' MD, the v1.1 archive, prior decomposition ledgers, or cross-source artifacts.

## Write boundary

Writes are limited to:

- `OUTPUT_LEDGER_PATH` — exactly one per-unit atom CSV
- `OUTPUT_VOCAB_SEED_PATH` — exactly one per-unit vocabulary seed CSV

No other files are written. Parent directories must already exist; the skill does not create directories.

## Tool usage

- No deterministic tools are invoked from inside this skill — the surrounding orchestrator pipeline (skeleton lift, dispatch-plan generation, brief building, merge, vocabulary consolidation) is handled by `tools/decomp/*` and `tools/retrieval/*` outside the worker.
- The `allowed-tools` frontmatter field is intentionally omitted — this skill is LLM-reasoning-only over the assigned slice.

Disallowed behavior:
- No deterministic tool invocation from within the worker.
- No writing outside `OUTPUT_LEDGER_PATH` or `OUTPUT_VOCAB_SEED_PATH`.
- No reading outside the declared read boundary.
- No sub-agent fanout.
- No final stable-ID assignment (the merge tool owns that).
- No cross-source reconciliation (Gate 3 persona owns that).

## Atom-CSV output schema

Required columns (in order):

```
LocalSeq, UnitStatement, SourceRef, ContentHash, InOutStatus, SectionID, DispatchUnitID, Corrects, Notes
```

| Column | Meaning |
|---|---|
| `LocalSeq` | 1-indexed monotonic counter within this dispatch unit |
| `UnitStatement` | One normalized atomic statement, one concept per row, ≤ ~50 words preferred |
| `SourceRef` | Dual citation: `<book>.md:L####` plus `<book>.html#anchor` separated by `\|` (e.g., `Pipe-Stress-Engineering.md:L1170\|Pipe-Stress-Engineering.html#SEC-PSE-0024`). Section anchor is acceptable when no finer anchor applies. **Per-kind anchor routing:** atoms sourced from an asset rather than prose anchor into the per-kind surfaces — `figures.html#asset-{asset_id}`, `tables.html#asset-{asset_id}`, `images.html#asset-{asset_id}` (use `equations.html#p{page}` when anchoring an equation). The `<book>.html` anchor remains the default for prose-derived atoms. |
| `ContentHash` | `sha1(UnitStatement)[:12]` — load-bearing for dedup, retrieval, and HTML cross-reference |
| `InOutStatus` | `IN` \| `OUT` \| `TBD` |
| `SectionID` | One of the `TARGET_SECTION_IDS` from `RuntimeOverrides` |
| `DispatchUnitID` | The `DISPATCH_UNIT_ID` from `RuntimeOverrides` |
| `Corrects` | Optional; semicolon-separated list of `HBA-<PREFIX>-NNNNN` IDs the atom corrects (cross-source allowed). Empty when not applicable. |
| `Notes` | Free-form note for ambiguity callouts or rationale. Empty when not applicable. |

`AtomicUnitID` is NOT a column on the per-unit CSV — final stable IDs are assigned by the merge tool (`tools/decomp/merge_source_atomizations.py per-source`) at unit-walk time.

## Vocabulary-seed CSV output schema

Required columns (in order):

```
CandidateTerm, Synonyms, Definition, SourceRefs, Notes
```

| Column | Meaning |
|---|---|
| `CandidateTerm` | The term as it appears in the source (case preserved) |
| `Synonyms` | Semicolon-separated variants observed in this dispatch unit |
| `Definition` | Best-effort definition extracted from the source; empty if not stated |
| `SourceRefs` | Semicolon-separated dual-citation lines where the term appears |
| `Notes` | Free-form notes (e.g., tradition / framing) |

## Method

### Step 1 — Validate inputs

1. Confirm `MD_PATH`, `SKELETON_PATH`, `ASSET_MANIFEST_PATH` exist.
2. Confirm `LINE_END ≥ LINE_START` and both are within the MD's total line count.
3. Confirm every `TARGET_SECTION_IDS` entry exists in the skeleton's `sections` list.
4. Confirm `OUTPUT_LEDGER_PATH` and `OUTPUT_VOCAB_SEED_PATH` parent directories exist.
5. If any input is invalid, return `RUN_STATUS=FAILED_INPUTS` and write empty (header-only) CSVs at the two output paths.

### Step 2 — Read the assigned slice

1. Read ONLY lines `LINE_START..LINE_END` of `MD_PATH`. Do not look outside this range.
2. Read the skeleton's `sections` list, filtering to the entries matching `TARGET_SECTION_IDS` for context.
3. Read the asset manifest's `assets` list, filtering to assets whose `page` falls within the slice's page range as derived from `sections[].page_first` / `page_last`.

### Step 3 — Atomize

For each meaningful technical statement in the slice:

1. Normalize it into a single short atomic statement (one concept, ≤ ~50 words).
2. Assign `SectionID` — the target section whose line range covers the statement's MD line.
3. Compute `SourceRef` — dual citation pinning to MD line and HTML anchor.
4. Compute `ContentHash` — `sha1(UnitStatement)[:12]`.
5. Classify `InOutStatus`:
   - **IN** for substantive technical claims that belong in the domain decomposition: principles, procedures, formulas (referenced from text), rules of thumb, standards-citations with the requirement clearly stated, definitions of canonical terms.
   - **OUT** for boilerplate that should not enter the decomposition: page numbers, running headers, copyright matter, indexed phrase repetitions, table-of-contents fragments, advertising / dust-jacket / dedication text, navigational markers (`<!-- PDF2MD-ASSETS:END page=N -->`), uninterpreted image-caption-only blocks.
   - **TBD** for content the persona must rule on at Gate 2: ambiguous statements, conflicting cross-source claims you cannot resolve from the slice alone, text whose meaning is unclear without external context.
6. If the statement appears to correct an earlier statement in another source (rare; only when explicitly noted in the text — e.g., errata, supersession statement), populate `Corrects` with the target atom's `HBA-…` ID. Leave empty if not applicable.
7. Append to the atom-CSV row buffer with `LocalSeq = previous + 1`.

If `MAX_ATOMS` is set, halt at that count and write what you have.

### Step 4 — Seed vocabulary

In parallel with atomization, surface candidate canonical terms:

1. Identify multi-word noun phrases that appear repeatedly within the slice or are explicitly emphasized (bold, italics, "called …", "known as …", "the term … refers to").
2. Note observed synonyms ("flexibility analysis (also called flexibility study)").
3. Capture an inline definition only when the source provides one explicitly.
4. Append to the vocabulary-seed CSV with dual-citation `SourceRefs` for each occurrence.

Do not invent canonical terms not visible in the text. Do not normalize beyond what the source uses.

### Step 5 — Write outputs

1. Write `OUTPUT_LEDGER_PATH` as CSV with the schema above, header row included. Use `\r\n` or `\n` consistently; UTF-8 encoding; field-quoted via Python `csv` module conventions.
2. Write `OUTPUT_VOCAB_SEED_PATH` likewise.

### Step 6 — Return status

Return one of:

- `RUN_STATUS=SUCCESS` — atoms emitted, `LocalSeq` monotonic, every row passes QA.
- `RUN_STATUS=NO_FINDINGS` — slice read but no IN atoms emitted (rare; valid when the slice was almost entirely OUT-boilerplate).
- `RUN_STATUS=FAILED_INPUTS` — inputs invalid; header-only CSVs written.
- `RUN_STATUS=FAILED` — slice could not be processed (unexpected encoding, malformed skeleton, etc.).

Also return: `DISPATCH_UNIT_ID`, `ATOM_COUNT`, `IN_COUNT`, `OUT_COUNT`, `TBD_COUNT`, `VOCAB_COUNT`.

## Non-negotiable constraints

- **Line-range discipline.** Read only lines `LINE_START..LINE_END`. Any atom whose `SourceRef` MD line falls outside that range is a contract violation.
- **Target-section discipline.** Every emitted atom's `SectionID` must be in `TARGET_SECTION_IDS`. Atoms whose source belongs to a section outside that list are a contract violation.
- **Output-path-only writes.** Exactly two files are written per invocation. No other side effects.
- **No invention (AOP-08).** Extract only what is visible in the assigned slice; if a fact is not present, do not invent — mark `TBD` or omit.
- **Content-hash discipline.** `ContentHash` MUST equal `sha1(UnitStatement)[:12]` — the merge tool re-verifies this and fails if mismatched.
- **LocalSeq monotonicity.** Strictly increasing positive integers starting at 1; no gaps, no reuse.
- **No final stable IDs.** `AtomicUnitID` is not a column in the per-unit CSV; the merge tool owns assignment.
- **Dual SourceRef.** Both halves required; HTML anchor falls back to the section anchor when no finer-grained anchor applies.

## QA expectations

- Exactly two files exist at `OUTPUT_LEDGER_PATH` and `OUTPUT_VOCAB_SEED_PATH` after the run.
- No files other than those two were written.
- Atom CSV header is exactly: `LocalSeq,UnitStatement,SourceRef,ContentHash,InOutStatus,SectionID,DispatchUnitID,Corrects,Notes`.
- Vocab CSV header is exactly: `CandidateTerm,Synonyms,Definition,SourceRefs,Notes`.
- For every IN row: `UnitStatement` non-empty, `SourceRef` non-empty, `ContentHash` non-empty.
- `InOutStatus ∈ {IN, OUT, TBD}`.
- Every row's MD line in `SourceRef` falls within `LINE_START..LINE_END`.
- Every row's `SectionID` is in `TARGET_SECTION_IDS`.
- `LocalSeq` is strictly increasing.
- No row's `UnitStatement` is a bare page number, header line, navigational marker, or boilerplate-only fragment marked `IN`.
- `ContentHash` recomputes correctly from `UnitStatement` (validated by the merge tool).
- `RUN_STATUS` is one of: `SUCCESS`, `NO_FINDINGS`, `FAILED_INPUTS`, `FAILED`.

## Relationship to DOMAIN_DECOMP

This skill is the per-dispatch-unit worker invoked by the `DOMAIN_DECOMP` orchestrator for per-skeleton-dispatch-unit fanout in Phase 2. The orchestrator:

- runs `tools/decomp/build_source_skeleton.py` to produce the dispatch plan,
- runs `tools/decomp/render_source_html.py --mode structure` to produce the HTML review surface for Gate 1.5,
- iterates the dispatch plan and calls `tools/decomp/build_atomization_brief.py` per unit_id to render the INIT-TASK brief,
- dispatches one `TASK + domain-source-atomize` invocation per dispatch unit,
- collects per-unit CSVs and runs `tools/decomp/merge_source_atomizations.py per-source` then `cross-source` to assemble the final ledger,
- runs `tools/decomp/merge_vocabulary_seeds.py` to consolidate vocabulary,
- runs `tools/decomp/render_source_html.py --mode atom-review` to produce the Gate-2 atom-review surface in the browser,
- proceeds to Gate 3 with the merged ledger.

This skill is a sibling of `pdf2md-page` and `drawing-extract-page` — same per-item fanout pattern, but per-MD-slice atomization instead of per-page extraction.
