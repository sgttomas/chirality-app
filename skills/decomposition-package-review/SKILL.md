---
name: decomposition-package-review
description: Review one DOMAIN decomposition package as a closed system for derivative parity, active snapshot completeness, and handoff-state readiness. Use when a root-level remediation or scope-change run needs package-level closure evidence before downstream work or phase advancement.
compatibility: Chirality TASK in generic shell mode (no profile); reasoning-first package review with optional bounded repair.
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL — decomposition-package-review

## Purpose

Review one bounded `DOMAIN` root as a closed decomposition package:

- `_Decomposition/`
- `_ScopeChange/_LATEST.md`
- the active `_ScopeChange/SCA-*` snapshot

The skill checks whether duplicated decomposition-local truth surfaces agree,
whether the active snapshot satisfies the current `SCOPE_CHANGE` contract, and
whether the recorded handoff state is consistent with the actual package state.

This skill supports two modes:

- `REVIEW_ONLY` — inspect and report only
- `REVIEW_AND_REPAIR` — perform only bounded, decomposition-local repairs that
  are explicitly authorized by `AllowedWriteTargets` and mechanically derivable
  from already authoritative package truth

This skill never repairs KTY-local content, hypergraph outputs, audit outputs,
or publication artifacts.

## Suitable agent shells

- `TASK` (generic shell mode, no profile)

Typical dispatchers:

- `SCOPE_CHANGE` closeout
- root remediation closure steps
- follow-on review loops before Phase 7 / publication gating

## Inputs

### Required

- `ScopePath` — absolute path to one DOMAIN root
- `AllowedWriteTargets` — explicit list of report paths and any
  decomposition-local files authorized for repair in this run
- `RuntimeOverrides.ROOT_PATH` — normally equal to `ScopePath`
- `RuntimeOverrides.DECOMPOSITION_ROOT` — absolute path to the root's
  `_Decomposition/`
- `RuntimeOverrides.SCOPE_CHANGE_ROOT` — absolute path to the root's
  `_ScopeChange/`
- `RuntimeOverrides.REVIEW_OUTPUT_PATH` — markdown review report path
- `RuntimeOverrides.MODE` — `REVIEW_ONLY` or `REVIEW_AND_REPAIR`

### Optional

- `RuntimeOverrides.FINDINGS_CSV_PATH` — optional structured findings log
- `RuntimeOverrides.PARITY_MATRIX_PATH` — optional structured parity matrix
- `RuntimeOverrides.ACTIVE_SNAPSHOT_PATH` — explicit snapshot path; autodetect
  from `_LATEST.md` when omitted
- `RuntimeOverrides.MAX_FINDINGS` — soft cap on reported findings; default `80`

## Runtime overrides

| Key | Meaning | Default | Allowed values |
|---|---|---|---|
| `ROOT_PATH` | DOMAIN root under review | **Required** | Absolute directory path |
| `DECOMPOSITION_ROOT` | `_Decomposition/` path | **Required** | Absolute directory path |
| `SCOPE_CHANGE_ROOT` | `_ScopeChange/` path | **Required** | Absolute directory path |
| `REVIEW_OUTPUT_PATH` | Markdown report path | **Required** | Path inside `AllowedWriteTargets` |
| `MODE` | Review or bounded repair mode | **Required** | `REVIEW_ONLY`, `REVIEW_AND_REPAIR` |
| `FINDINGS_CSV_PATH` | Optional structured findings log | omitted | Path inside `AllowedWriteTargets` |
| `PARITY_MATRIX_PATH` | Optional structured parity matrix | omitted | Path inside `AllowedWriteTargets` |
| `ACTIVE_SNAPSHOT_PATH` | Explicit active snapshot path | autodetect | Absolute directory path |
| `MAX_FINDINGS` | Soft cap on findings | `80` | Positive integer |

## Read boundary

Reads are limited to:

- `{DECOMPOSITION_ROOT}/`
- `{SCOPE_CHANGE_ROOT}/_LATEST.md`
- the active snapshot under `{SCOPE_CHANGE_ROOT}/`

The skill must not widen to KTY-local folders, `_Aggregation/`,
`_Reconciliation/`, hypergraph outputs, or publication outputs.

## Write boundary

Writes are limited to:

- `{REVIEW_OUTPUT_PATH}`
- optional `{FINDINGS_CSV_PATH}`
- optional `{PARITY_MATRIX_PATH}`
- in `REVIEW_AND_REPAIR` mode only: explicitly authorized files under
  `{DECOMPOSITION_ROOT}/` or `{SCOPE_CHANGE_ROOT}/`

The skill must never write:

- KTY-local folders
- `_Aggregation/`
- `_Reconciliation/`
- hypergraph outputs
- publication outputs

## Tool usage

- Reasoning-first only.
- The `allowed-tools` frontmatter field is intentionally omitted.

Disallowed behavior:

- No use of this skill for cross-root conformity review.
- No KTY-local metadata repair; use `kty-metadata-align` for that.
- No silent repair of ambiguous truth conflicts.
- No invention of missing snapshot artifacts, missing decomposition rows, or
  phase-completion claims that are not supported by package evidence.

## Method

### Step 0 — Preconditions

1. Validate `ROOT_PATH`, `DECOMPOSITION_ROOT`, and `SCOPE_CHANGE_ROOT`.
2. Resolve the active snapshot:
   - use `ACTIVE_SNAPSHOT_PATH` when provided, otherwise read `_LATEST.md`
   - if `_LATEST.md` is missing, empty, or resolves ambiguously, report it
3. Validate `REVIEW_OUTPUT_PATH` is inside `AllowedWriteTargets`.
4. If `MODE = REVIEW_AND_REPAIR`, validate every non-report write target is
   inside `_Decomposition/` or `_ScopeChange/`.

### Step 1 — Inventory the active decomposition package

Inventory, at minimum:

- the main decomposition markdown
- decomposition-local derivatives and annexes under `_Decomposition/`
- `_ScopeChange/_LATEST.md`
- active snapshot artifacts

Treat the package as a closed system. If a local derivative surface carries
duplicated counts, mappings, status, open-issue state, validation evidence, or
handoff state, it is in scope for comparison.

### Step 2 — Classify package roles

Before building the parity matrix, classify every major surface by package role:

| Label | Meaning |
|---|---|
| `working surface` | The main decomposition document; the primary human-facing control surface |
| `authoritative companion register` | A companion file holding heavy machine-truth as the primary working surface for that data |
| `snapshot / handoff artifact` | An immutable amendment snapshot or handoff-state record |
| `derived publication artifact` | A render, bundle, or review document assembled from the modular package; not the amendment surface |

For each reviewed surface, record:

- the assigned package-role label
- whether the main decomposition document is overly monolithic relative to companion truth (heavy ledger/telemetry embedded inline when companion registers already carry the same truth)
- whether any companion register should be promoted (it carries authoritative truth not reflected in the main doc) or demoted (it duplicates main-doc truth without adding value)
- whether any artifact is ambiguously labeled or unlabeled

Package-role classification findings feed into Step 3.

### Step 3 — Build the package parity matrix

Compare the authoritative surfaces for:

- top-level telemetry and counts
- category / knowledge-type / subject parity
- objective support parity
- open-issue parity
- mapping-table parity
- validation-check parity
- active snapshot artifact completeness
- handoff-state consistency

For each reviewed surface, classify package state as:

- `MATCH`
- `DRIFT`
- `MISSING`
- `NOT_APPLICABLE`

### Step 4 — Classify findings

Every finding must land in exactly one class:

- `DECOMP_LOCAL_REPAIR`
- `SNAPSHOT_REPAIR`
- `DOWNSTREAM_RERUN`
- `HUMAN_DECISION_REQUIRED`

Typical examples:

- stale duplicated annex rows -> `DECOMP_LOCAL_REPAIR`
- wrong `_LATEST.md` or incomplete active snapshot -> `SNAPSHOT_REPAIR`
- KTY-local content drift implied by package truth -> `DOWNSTREAM_RERUN`
- contradictory authoritative package surfaces with no clear winner ->
  `HUMAN_DECISION_REQUIRED`

### Step 5 — Optional bounded repair

Only when `MODE = REVIEW_AND_REPAIR`:

1. Repair only files explicitly authorized by `AllowedWriteTargets`.
2. Repair only when the fix is mechanically derivable from already accepted
   package truth.
3. Allowed repair classes:
   - duplicated decomposition-local derivative parity
   - active snapshot pointer parity
   - handoff-state or run-summary state fields that are stale relative to the
     already accepted artifact state
4. Disallowed repair classes:
   - substantive decomposition truth changes requiring human judgment
   - missing snapshot artifacts whose contents would need to be invented
   - KTY-local metadata or content repair

### Step 6 — Write outputs

Write `{REVIEW_OUTPUT_PATH}` containing, in order:

1. Title: `# Decomposition Package Review — {ROOT_NAME}`
2. Metadata block: root path, active snapshot, mode, review date
3. Package verdict:
   - `READY`
   - `READY_WITH_GAPS`
   - `BLOCKED`
4. Package-role classification per reviewed surface
5. Parity summary
6. Findings grouped by the four required classes
7. Repairs applied in this run, if any
8. Required downstream reruns, if any
9. Explicit `RUN_STATUS`

Decomposition-local drift repair (classes `DECOMP_LOCAL_REPAIR` and
`SNAPSHOT_REPAIR`) is authoritative work: this skill may fix it directly when
`MODE = REVIEW_AND_REPAIR`. Observations about derived publication artifacts
(e.g., stale monolithic renders or publication bundles) are for reporting only
and must not be repaired by this skill.

If `PARITY_MATRIX_PATH` is provided, write a structured matrix with at least:

- `SurfacePath`
- `SurfaceType`
- `ComparisonBasis`
- `ParityStatus`
- `AuthorityBasis`
- `RequiredAction`

If `FINDINGS_CSV_PATH` is provided, write a CSV with minimum columns:

- `FindingID`
- `Severity`
- `FindingClass`
- `SurfacePath`
- `Summary`
- `AuthorityBasis`
- `RecommendedAction`

## Outputs

- `Decomposition_Package_Review.md` at `REVIEW_OUTPUT_PATH`
- optional findings CSV at `FINDINGS_CSV_PATH`
- optional parity matrix at `PARITY_MATRIX_PATH`

## Non-negotiable constraints

- **One root per run.** Review exactly one DOMAIN root.
- **Package-bounded.** Treat `_Decomposition/` + active `_ScopeChange/` as the
  full scope; do not widen into KTY folders.
- **No silent truth selection.** If authoritative surfaces disagree and no
  clear authority basis exists, escalate instead of repairing.
- **Repair is opt-in.** `REVIEW_AND_REPAIR` may repair only explicitly approved,
  mechanically derivable package-local drift.
- **Evidence-backed findings.** Every material finding cites a local surface.

## QA expectations

- The reviewed root and active snapshot are explicit.
- The report states one of `READY`, `READY_WITH_GAPS`, or `BLOCKED`.
- Findings distinguish decomposition-local repair, snapshot repair, downstream
  rerun, and human-decision classes.
- `REVIEW_ONLY` runs modify no package-local truth.
- `REVIEW_AND_REPAIR` runs list every repaired file explicitly.
