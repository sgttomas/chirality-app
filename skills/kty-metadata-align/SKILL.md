---
name: kty-metadata-align
description: Review and optionally align one DOMAIN Knowledge Type folder's metadata surfaces to approved decomposition truth without rewriting Scoping.md or KA content. Use after regeneration or scope change when `_CONTEXT.md`, `_STATUS.md`, or `_REFERENCES.md` may have drifted.
compatibility: Chirality TASK in generic shell mode (no profile); reasoning-first KTY-local metadata review and bounded repair.
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL — kty-metadata-align

## Purpose

Review and optionally align the metadata surface of one DOMAIN Knowledge Type
folder to approved decomposition truth and current lifecycle evidence.

In package-role terms: this skill aligns KTY-local derived metadata
(`_CONTEXT.md`, `_STATUS.md`, `_REFERENCES.md`) to the authoritative
decomposition truth in the canonical working package, not the reverse. The
decomposition package (main document + authoritative companion registers +
`_ScopeChange` state) is the source of truth; KTY-local metadata is a
downstream consumer of that truth.

When this skill reads `_STATUS.md`, it also reads sibling `_MEMORY.md` or
`MEMORY.md` when present. Memory is non-authoritative operational context only:
it can explain prior local runs or caveats, but it must not override approved
decomposition truth or SCA state.

This skill supports two modes:

- `REPORT_ONLY` — inspect and report only
- `ALIGN_METADATA` — repair metadata-safe drift

Metadata-safe writes are limited to:

- `_CONTEXT.md`
- `_STATUS.md`
- `_REFERENCES.md`

This skill never rewrites:

- `Scoping.md`
- `KA-*.md`
- `_DEPENDENCIES.md`
- `_MEMORY.md`
- publication artifacts

If content files appear stale after metadata alignment, the skill reports a
follow-on rerun rather than widening scope.

## Suitable agent shells

- `TASK` (generic shell mode, no profile)

Typical dispatchers:

- root remediation loops after `domain-documents`
- `SCOPE_CHANGE` follow-on closure work
- targeted KTY metadata cleanup after audit findings

## Inputs

### Required

- `ScopePath` — absolute path to one `KTY-*` folder
- `AllowedWriteTargets` — report path plus any metadata files explicitly
  authorized for alignment in this run
- `RuntimeOverrides.KTY_PATH` — normally equal to `ScopePath`
- `RuntimeOverrides.DECOMPOSITION_REF` — decomposition root or document used as
  truth source
- `RuntimeOverrides.MODE` — `REPORT_ONLY` or `ALIGN_METADATA`

### Optional

- `RuntimeOverrides.SOURCES_ROOT` — shared source/reference root for resolving
  authoritative source pointers
- `RuntimeOverrides.REVIEW_OUTPUT_PATH` — optional markdown report path
- `RuntimeOverrides.REWRITE_REFERENCES` — `true` | `false`; default `true`
- `RuntimeOverrides.ALLOW_STATUS_APPEND` — `true` | `false`; default `true`
- `RuntimeOverrides.AUTHORITATIVE_STATUS_STATE` — optional lifecycle state to
  append when the invoking workflow owns the state transition

## Runtime overrides

| Key | Meaning | Default | Allowed values |
|---|---|---|---|
| `KTY_PATH` | Knowledge Type folder to review/align | **Required** | Absolute path to one `KTY-*` folder |
| `DECOMPOSITION_REF` | Decomposition truth source | **Required** | Absolute path |
| `MODE` | Report or metadata alignment mode | **Required** | `REPORT_ONLY`, `ALIGN_METADATA` |
| `SOURCES_ROOT` | Source-material root for reference-path resolution | omitted | Absolute path |
| `REVIEW_OUTPUT_PATH` | Optional report path | omitted | Path inside `AllowedWriteTargets` |
| `REWRITE_REFERENCES` | Rewrite `_REFERENCES.md` | `true` | `true`, `false` |
| `ALLOW_STATUS_APPEND` | Permit append-only `_STATUS.md` corrections | `true` | `true`, `false` |
| `AUTHORITATIVE_STATUS_STATE` | Explicit lifecycle state supplied by caller | omitted | `OPEN`, `INITIALIZED`, `SEMANTIC_READY`, `IN_PROGRESS`, `CHECKING`, `ISSUED`, `RETIRED` |

## Read boundary

Reads are limited to:

- `{KTY_PATH}/_CONTEXT.md`
- `{KTY_PATH}/_STATUS.md`
- `{KTY_PATH}/_MEMORY.md` or `{KTY_PATH}/MEMORY.md` when present, paired with
  `_STATUS.md` as non-authoritative operational context only
- `{KTY_PATH}/_REFERENCES.md`
- optional `{KTY_PATH}/Scoping.md` and `{KTY_PATH}/KA-*.md` for drift
  observation only
- decomposition materials under `{DECOMPOSITION_REF}`
- source pointers under `{SOURCES_ROOT}` only when needed

This skill must not scan sibling KTY folders or infer truth from unrelated
roots.

## Write boundary

Writes are limited to:

- optional `{REVIEW_OUTPUT_PATH}`
- `{KTY_PATH}/_CONTEXT.md`
- `{KTY_PATH}/_STATUS.md`
- `{KTY_PATH}/_REFERENCES.md`

Only files explicitly authorized in `AllowedWriteTargets` may be modified.

## Tool usage

- Reasoning-first only.
- The `allowed-tools` frontmatter field is intentionally omitted.

Disallowed behavior:

- No edits to `Scoping.md`, `KA-*.md`, `_DEPENDENCIES.md`, `_MEMORY.md`, or any
  decomposition file.
- No invention of source paths, lifecycle state, or decomposition fields.
- No silent deletion of human-authored reference notes unless the brief
  explicitly authorizes replacement.

## Method

### Step 0 — Preconditions

1. Validate `KTY_PATH` exists and resolves to exactly one `KTY-*` folder.
2. Resolve the matching KTY row from `DECOMPOSITION_REF`.
3. Validate every repair target is explicitly authorized by
   `AllowedWriteTargets`.
4. If the KTY row cannot be identified uniquely: `RUN_STATUS=FAILED_INPUTS`.

### Step 1 — Derive canonical metadata

Extract from decomposition truth, without invention:

- `KnowledgeTypeID`
- `Knowledge Type Name`
- `Category ID`
- `Category Name`
- `Discipline`
- `Type`
- `Responsible`
- `Description`
- `AnticipatedArtifacts`
- `CanonicalSchema`
- `IntendedUsers`
- `WhenUsed`
- decomposition reference path
- any authoritative source pointer or `SourceSpan` available for the KTY

If a field is absent in decomposition truth, use `TBD` rather than inferring it.

### Step 2 — Review current metadata state

Review:

- `_CONTEXT.md` for identity / category / description drift
- `_STATUS.md` for append-only lifecycle validity and any obvious contradiction
  with `AUTHORITATIVE_STATUS_STATE`, when provided
- `_MEMORY.md` / `MEMORY.md`, when present, for non-authoritative operational
  caveats paired with `_STATUS.md`
- `_REFERENCES.md` for stale or contradictory authoritative pointers
- `Scoping.md` / `KA-*.md` only to decide whether content regeneration follow-up
  is still needed

Classify each observed issue as:

- `REPAIRED_NOW`
- `RERUN_LATER`
- `UNRESOLVED`

### Step 3 — Optional metadata alignment

Only when `MODE = ALIGN_METADATA`:

1. Rewrite `_CONTEXT.md` to aligned decomposition truth.
2. If `REWRITE_REFERENCES=true`, normalize `_REFERENCES.md` so authoritative
   pointers are current and preserved notes stay clearly non-authoritative.
3. If `ALLOW_STATUS_APPEND=true` and a status correction is unambiguous:
   - append a correction line to `_STATUS.md`
   - never invent a new lifecycle state
   - if `AUTHORITATIVE_STATUS_STATE` is absent and the correction would require
     judgment, do not edit `_STATUS.md`; report it instead

### Step 4 — Surface follow-on work

If `Scoping.md` or any `KA-*.md` appear inconsistent with aligned metadata:

- do not edit them
- report the exact files
- classify them as `RERUN_LATER`

### Step 5 — Write outputs

If `REVIEW_OUTPUT_PATH` is provided, write a report containing:

1. Title: `# KTY Metadata Alignment — {KTY-ID}`
2. Metadata block: KTY path, decomposition ref, mode, review date
3. Summary sections:
   - repaired now
   - rerun later
   - unresolved
4. Files modified in this run, if any
5. Explicit `RUN_STATUS`

## Outputs

- optional report at `REVIEW_OUTPUT_PATH`
- optionally updated `_CONTEXT.md`
- optionally updated `_STATUS.md`
- optionally updated `_REFERENCES.md`

## Non-negotiable constraints

- **Single-KTY scope.** One invocation aligns one KTY folder only.
- **Metadata-only writes.** No `Scoping.md` or `KA-*` edits.
- **Decomposition authority.** `_CONTEXT.md` aligns to approved decomposition
  truth (the canonical working package), not existing draft prose. The
  direction of truth flow is always: authoritative decomposition package ->
  KTY-local metadata, never the reverse.
- **Append-only lifecycle safety.** `_STATUS.md` changes must be append-only and
  authority-backed.
- **No invention.** Missing source pointers or lifecycle evidence remain
  reported, not guessed.
- **Downstream scope only.** This skill operates on KTY-local metadata surfaces
  only. It must not modify the canonical working package, authoritative
  companion registers, `_ScopeChange` state, or any derived publication
  artifacts. It must not become a loophole for compensating for poor
  decomposition package structure upstream.

## QA expectations

- The target KTY ID is explicit.
- The run separates `REPAIRED_NOW`, `RERUN_LATER`, and `UNRESOLVED`.
- Any `_STATUS.md` modification is append-only and evidence-backed.
- Any stale `Scoping.md` or `KA-*` content is surfaced as follow-on work, not
  silently rewritten.
