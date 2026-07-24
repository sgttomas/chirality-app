---
name: deliverable-consistency
description: Run a deliverable-local consistency sweep across production documents in one deliverable. Use when checking for unresolved markers, missing core artifacts, identity-label mismatches, or candidate unsourced numeric statements.
compatibility: Chirality TASK generic shell; local repo tools only.
allowed-tools: python3 tools/validation/scan_deliverable_consistency.py:*
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL — deliverable-consistency

## Purpose

Run a deliverable-local consistency sweep across the production documents in one deliverable.

This skill is meant to work with generic `TASK` briefs that identify exactly one deliverable folder.

It helps the agent:
- surface contradictions,
- find unresolved `TBD` / `ASSUMPTION` / `CONFLICT:` markers,
- identify unsourced numeric parameters,
- spot identity mismatches across the document set,
- and propose minimal corrective edits when authorized.

## Suitable agent shells

- `TASK` (generic shell, no profile)

## Inputs

### Required

- `ScopePath`
- `RuntimeOverrides.DELIVERABLE_PATH`

### Optional

- `Tasks`
- `RuntimeOverrides.FocusDocs`
- `RuntimeOverrides.Strictness`
- `RuntimeOverrides.MaxFindings`
- `RuntimeOverrides.CheckIdentity`
- `RuntimeOverrides.CheckUnsourcedNumerics`

## Runtime overrides

| Key | Meaning | Default |
|---|---|---|
| `FocusDocs` | Limit the sweep to named production docs | all production docs |
| `Strictness` | `conservative` or `aggressive` finding posture | `conservative` |
| `MaxFindings` | Soft cap on reported findings | `10` |
| `CheckIdentity` | Check folder/document naming consistency | `true` |
| `CheckUnsourcedNumerics` | Flag numeric statements needing evidence review | `true` |
| `ProductionFormat` | resolver-selected `LEGACY_FOUR_DOC`, `SOW_V1`, or authorized `MIGRATION_DUAL` | resolver result |

## Tool usage

Preferred deterministic helper:
- `tools/validation/scan_deliverable_consistency.py`

Preferred method:
- run the deterministic scan first
- read only the flagged deliverable-local files and nearby context
- compare files directly where the deterministic scan cannot decide
- produce recommendation-first output unless edits are explicitly authorized by the brief

Disallowed behavior:
- no widening scope beyond the single deliverable
- no edits outside the effective bounded task brief's write authorization
- no silent conflict resolution
- `SOW_V1` validates cross-section/ID consistency in `ScopeOfWork.md`;
  `MIGRATION_DUAL` additionally requires exact path-scoped accepted authority
- missing, partial, invalid, ambiguous, and unauthorized dual input fail closed

## Outputs

- `PROPOSAL:` blocks for consistency issues
- `MISSING:` items where files or references are absent
- `NEEDS_HUMAN_RULING:` items for true contradictions
- optional applied minimal edits if `ApplyEdits: true`
- optional `MEMORY.md` update only when the brief explicitly authorizes it

## Non-negotiable constraints

- Every finding must cite a file and best-effort section/heading.
- Unknowns remain `TBD`.
- Conflicts must be surfaced, not reconciled silently.
- Proposed edits should be minimal and reversible.

## QA expectations

- Findings are scoped to one deliverable.
- The deterministic scan should be run first unless the brief explicitly forbids tool use.
- Findings are grouped by issue type where practical.
- Identity mismatches and unresolved markers are explicitly reported when found.
- If no meaningful issues are found, the run should say so explicitly rather than padding output.
