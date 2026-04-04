---
name: proposal-format
description: Structured recommendation output using PROPOSAL blocks with evidence, change, risk, and status fields. Use for any deliverable-local task that surfaces actionable findings.
compatibility: Chirality TASK with DELIVERABLE_TASK profile; reasoning-only (no deterministic tools).
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: DELIVERABLE_TASK
---

# SKILL — proposal-format

## Purpose

Produce structured, evidence-grounded recommendations for deliverable-local work using the PROPOSAL: block format. This skill standardizes how findings are expressed so they are reviewable, actionable, and traceable.

The PROPOSAL: pattern is the canonical recommendation format for deliverable-local tasks. It separates evidence from judgment, makes risk explicit, and preserves human authority over acceptance.

## Suitable agent shells

- `TASK` with `TaskProfile: DELIVERABLE_TASK`

## Inputs

### Required

- `DeliverablePath` via `DELIVERABLE_TASK`

### Optional

- `Tasks` — specific asks; if omitted, the skill produces a baseline scan (see Method: baseline scan)
- `RuntimeOverrides.MaxProposals` — soft cap on proposals generated
- `RuntimeOverrides.FocusDocs` — restrict analysis to named production docs
- `RuntimeOverrides.IncludeLensTags` — whether to include `Lens:` tags (default: only when `UseSemanticLensing: true`)

## Runtime overrides

| Key | Meaning | Default |
|---|---|---|
| `MaxProposals` | Soft cap on proposals returned | `10` |
| `FocusDocs` | Limit analysis to named docs (e.g., `Specification.md,Guidance.md`) | all production docs |
| `IncludeLensTags` | Add `Lens:` tags even when semantic lensing is not active | `false` |
| `ProposalDepth` | `summary` (title + status only) or `full` (all fields) | `full` |

## Tool usage

This is a reasoning-only skill. No deterministic tools are required.

When combined with other skills that use deterministic tools (e.g., deliverable-consistency), the tool output provides the evidence base; this skill provides the output structure.

Disallowed behavior:
- no inventing evidence to justify a proposal
- no widening scope beyond the single deliverable
- no edits outside the files permitted by `DELIVERABLE_TASK`
- no silent conflict resolution — contradictions go in `NEEDS_HUMAN_RULING`

## Method: PROPOSAL block format

Every recommendation MUST be expressed as a PROPOSAL: block with these fields:

```
- PROPOSAL: <short title>
  - Evidence: <_REFERENCES.md item(s) and/or Source: <Doc> §<Heading>>
  - Change: <precise change — what to add, modify, or remove>
  - Why: <what it improves — clarity, completeness, verification, consistency, etc.>
  - Risk: <downstream impact, dependency impacts, or conflicts>
  - Status: <PROPOSED | APPLIED | NEEDS_HUMAN_RULING>
```

Optional field (when semantic lensing is active or `IncludeLensTags: true`):
```
  - Lens: <Matrix.Row.Column> (or Lens: UNKNOWN if _SEMANTIC.md is missing)
```

### Field rules

- **Evidence** must cite a file and best-effort section/heading. If exact location is unknown, use `location TBD`. Never cite `_SEMANTIC_LENSING.md` as evidence — it is a worklist, not authority.
- **Change** must be precise enough to apply without further interpretation. "Improve the specification" is not acceptable; "Add REQ-12: minimum wall thickness per CSA Z662 §7.1" is.
- **Why** must name the improvement category (clarity, completeness, verification, consistency, source fidelity, etc.), not just restate the change.
- **Risk** must name concrete downstream effects. "Low risk" without explanation is not acceptable; "Low — additive requirement; no existing content contradicted" is.
- **Status** rules:
  - `PROPOSED` — default; the human has not yet decided
  - `APPLIED` — only when `ApplyEdits: true` and the edit was made
  - `NEEDS_HUMAN_RULING` — when the proposal involves a genuine trade-off, contradiction, or scope decision

### Grouping

When practical, group proposals by issue type:
- Completeness gaps (missing content)
- Consistency issues (cross-document conflicts)
- Verification gaps (requirements without verification methods)
- Source fidelity issues (content that may not match source)
- Identity/terminology issues

## Method: decision interface

After all PROPOSAL: blocks, always include:

```
- MISSING: <items where files or references are absent>
- NEEDS_HUMAN_RULING: <items requiring human decision — contradictions, trade-offs, scope questions>
- DEPENDENCY_NOTES: <cross-deliverable interfaces, blockers, mismatches>
```

Each section may be `none` if empty.

## Method: baseline scan

When `Tasks` is omitted from the brief, produce a baseline assessment:
- Top proposals (up to `MaxProposals`) — the highest-value recommendations based on a sweep of the production documents
- Top `TBD` items — the most impactful unresolved markers
- Top dependency notes — cross-deliverable issues visible from this deliverable's content

This baseline scan is the default behavior, not a separate mode. It is what the skill does when given no specific direction.

## Outputs

- `PROPOSAL:` blocks (structured per the format above)
- `MISSING:` items
- `NEEDS_HUMAN_RULING:` items
- `DEPENDENCY_NOTES:` items
- Optional applied edits (when `ApplyEdits: true`)
- Updated `MEMORY.md` through DELIVERABLE_TASK closeout

## Non-negotiable constraints

- Every proposal must cite evidence from production documents or accessible sources
- Unknowns remain `TBD` — do not invent content to fill gaps
- Conflicts must be surfaced in `NEEDS_HUMAN_RULING`, not reconciled silently
- Proposed changes must be minimal and reversible
- The human decides acceptance — proposals are recommendations, not directives

## QA expectations

- Every PROPOSAL: block contains all required fields (Evidence, Change, Why, Risk, Status)
- Evidence fields cite file + section/heading (or `location TBD`)
- No proposal is unsupported by evidence
- Change descriptions are specific enough to apply without interpretation
- Status is correctly assigned (PROPOSED unless edits were applied or human ruling is needed)
- If no meaningful issues are found, the run says so explicitly rather than padding output
