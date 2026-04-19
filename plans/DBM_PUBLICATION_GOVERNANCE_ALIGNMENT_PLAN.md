# DBM Publication Governance Alignment Plan

## Summary

This plan defines the corrective work needed to bring the DBM publication
workflow into alignment with the stricter governance model established during
the West Doe post-Phase-6 remediation work.

The current DBM publication architecture remains valid:
- one execution root -> one rewritten DBM
- frozen publication planning artifacts
- section-level publication workers
- typed concordance register plus package-level concordance gate

The corrective work is about **admission, closure, and authority discipline**,
not about replacing the workflow.

The implementing agent must preserve `plans/DBM_PUBLICATION_WORKFLOW_PLAN.md` as
the original architecture/design record. This plan is the **corrective
implementation plan** that takes precedence where the two documents conflict.

Target new relationship:
- `plans/DBM_PUBLICATION_WORKFLOW_PLAN.md` = original workflow design
- `plans/DBM_PUBLICATION_GOVERNANCE_ALIGNMENT_PLAN.md` = corrective governance
  implementation plan

## Core Governance Change

### Publication may start only from fully closed upstream root state

The publication workflow must no longer admit a root merely because:
- `_ScopeChange/_LATEST.md` points to an accepted snapshot, and
- the root is described as “accepted post-SCA”.

Instead, publication admission must require **full accepted upstream closure**
for the publication boundary. For a `DOMAIN` root, that means the frozen
publication input manifest must prove that:

- the active `_ScopeChange/_LATEST.md` points to exactly one accepted active
  snapshot
- the active scope-change snapshot exists and is complete
- the active `Handoff_State.md` exists
- the active handoff state shows that derivative closure required for
  publication has been completed or explicitly accepted for publication
- the most recent relevant `AUDIT_DECOMP` output is identified and non-blocking
- the root is actually ready for publication-phase consumption, rather than
  merely ready for downstream regeneration

Publication authority remains:
1. approved publication schema
2. approved publication rules
3. approved merged decomposition/package truth
4. accepted scope-change state
5. KTY-local `Scoping.md` and `KA-*.md`
6. original DBM source as provenance only

But publication **admission evidence** must separately include:
- active `Handoff_State.md`
- latest relevant audit evidence
- explicit publication-entry readiness

Those admission artifacts are not section-content authority. They are workflow
gating evidence only.

## Required Contract Revisions

### 1. `agents/AGENT_DBM_PUBLISHER.md`

Revise the publisher contract in these exact ways:

- Gate 1 must become a true **publication admission gate**, not only a path
  freeze.
- Replace the implicit current-state basis
  `accepted post-SCA state` with:
  - accepted decomposition/package truth
  - accepted scope-change state
  - derivative closure state sufficient for publication
  - non-blocking audit state
  - handoff state that permits publication-phase entry
- `Publication_Input_Manifest.md` must explicitly freeze:
  - exact `_Decomposition` inputs
  - exact `_ScopeChange/_LATEST.md`
  - active scope-change snapshot directory
  - active `Handoff_State.md`
  - latest relevant audit snapshot path(s) and verdict(s)
  - exact source DBM/TOC inputs
  - explicitly banned authority inputs
- Gate 5 wording must no longer allow package publication when the section set
  is merely “complete enough to assemble”. It must require that every required
  section has one current section output bundle before Gate 6 begins.
- Gate 7 must emit a fixed publication closeout artifact:
  `Publication_Handoff_State.md`
- Gate 7 must update `_LATEST.md` only after:
  - human acceptance of the package snapshot
  - `Publication_Handoff_State.md` exists

Add `Publication_Handoff_State.md` as a required publication artifact with at
least these fields:
- `UpstreamRoot`
- `AcceptedUpstreamSnapshot`
- `AcceptedUpstreamHandoffState`
- `LatestAuditSnapshot`
- `LatestAuditVerdict`
- `SectionSetState`
- `ConcordanceState`
- `ExpansionCandidateState`
- `PublicationReadinessState`
- `RemainingBlockers`
- `ReadyForChangeHandoff`

Allowed values should be fixed and enumerated in the agent contract so the
implementer does not invent them.

Recommended enums:
- `SectionSetState`: `INCOMPLETE | COMPLETE`
- `ConcordanceState`: `BLOCKED | NON_BLOCKING_PASS`
- `ExpansionCandidateState`: `BLOCKED_HIGH | OPEN_NORMAL | COMPLETE`
- `PublicationReadinessState`: `BLOCKED | READY_WITH_MAJOR_NOTES | READY`
- `ReadyForChangeHandoff`: `NO | YES`

### 2. `plans/DBM_PUBLICATION_WORKFLOW_PLAN.md`

Update the workflow plan so it matches the corrected publisher contract without
rewriting the whole design.

Required corrections:
- Add a clear note near the top that this plan is the original workflow design
  and must be read together with the governance alignment plan.
- Update the publication admission language so “approved post-SCA state” is no
  longer sufficient by itself.
- Expand `Publication_Input_Manifest.md` requirements to include:
  - active `Handoff_State.md`
  - latest relevant audit evidence
  - explicit publication-entry basis
- Update the authority/banned-input section to distinguish:
  - not authoritative for section prose
  - may still be required as admission or closure evidence
- Update the package-entry wording so missing required sections are a pre-Gate-6
  block, not just a package-stage discovery
- Add the required publication closeout artifact
  `Publication_Handoff_State.md`

The plan must continue to describe:
- one execution root -> one DBM
- frozen planning artifacts
- section workers plus package gate
- hard concordance blocking in v1

### 3. `skills/dbm-section-publish/*`

Revise the section worker so freshness is not judged mainly by
`_STATUS.md >= INITIALIZED`.

Required changes:
- The skill must treat the frozen publication manifest as the primary freshness
  and admissibility boundary.
- The skill must assume its mapped KTY inputs were admitted by a root already
  cleared for publication by `DBM_PUBLISHER`.
- `_STATUS.md` remains a local sanity check, but not the main publication
  readiness proxy.
- If local `_STATUS.md` evidence conflicts with the frozen publication manifest
  or root admission state, the skill must fail conservatively and surface the
  conflict in `SEC-##_QA.md`.

Do not widen the section worker’s write scope.

### 4. `skills/dbm-concordance-seed/*`

Keep the concordance-seeding method and agent-owned candidate loop.

Required adjustments:
- Align the skill docs with the corrected publication admission model:
  the skill reads only from a frozen manifest built from a publication-admitted
  root.
- No change to the scope model:
  - one approved section or bounded section group
  - writes only scope-local candidate outputs

No change is required to the core concordance philosophy. The stack is still
appropriate for the job.

### 5. `skills/dbm-publish/*`

Keep `dbm-publish` as the bounded package-level gate.

Required changes:
- Update the brief schema and QA checks so package runs explicitly rely on a
  publication-admitted manifest.
- Add validation that `Publication_Handoff_State.md` is emitted during accepted
  package closeout.
- Keep the current package-level blocking rules:
  - missing required sections block
  - approved-register concordance mismatches block
  - unresolved `HIGH` expansion candidates block

Do not turn `dbm-publish` into a dispatcher.

## Concordance And Toolchain Alignment

### Keep the current concordance architecture

The current concordance design remains appropriate:
- deterministic candidate harvest:
  `tools/publication/build_concordance_candidates.py`
- reasoning-based candidate refinement:
  `skills/dbm-concordance-seed`
- per-section assertion emission:
  `skills/dbm-section-publish`
- deterministic register checking:
  `tools/publication/check_concordance.py`
- package-level readiness judgment:
  `skills/dbm-publish`

That architecture still matches the quality bar established during remediation:
- deterministic structure where possible
- reasoning only where deterministic harvesting cannot safely infer enough
- hard package gate on approved-register mismatches
- separate hard gate on unresolved `HIGH` discovery candidates

### Required concordance contract upgrades

The under-specified part is the candidate artifact contract, not the overall
method.

Update the agent and plan contracts so
`Publication_Concordance_Candidates.csv` explicitly includes:
- `CandidateValueExample`
- `ResolutionStatus`

This must match the richer schema already used by the skill contract.

Required `ResolutionStatus` values:
- `READY_FOR_FREEZE`
- `NEEDS_REVIEW`
- `DUPLICATE_CANDIDATE`
- `OUT_OF_SCOPE`

No redesign is needed in:
- `build_concordance_candidates.py`
- `check_concordance.py`
- `assemble_publication.py`

unless implementation review shows a missing output or a contract mismatch with
the revised docs.

### Admission-evidence distinction for concordance

The corrected workflow must make this distinction explicit:

- concordance checks publication **internal consistency**
- concordance does **not** prove that the upstream root was ready to publish

Upstream root closure remains a separate publisher admission requirement.

## Required Artifact And Interface Changes

### New or expanded artifacts

1. `Publication_Input_Manifest.md`
   Add required sections/fields for:
   - active snapshot pointer
   - active snapshot path
   - active `Handoff_State.md`
   - latest relevant audit snapshot path
   - latest relevant audit verdict
   - publication admission basis

2. `Publication_Handoff_State.md`
   New required package closeout artifact under the accepted package snapshot.

3. `Publication_Concordance_Candidates.csv`
   Ensure the agent/plan docs include:
   - `CandidateValueExample`
   - `ResolutionStatus`

### No new top-level agent

Do not introduce a new publication agent.
Keep `DBM_PUBLISHER` as the runtime publication persona.

## Test Plan

### Admission-control tests

- A root with accepted `_ScopeChange/_LATEST.md` but unresolved derivative
  closure is rejected at publisher Gate 1.
- A root with accepted handoff state, non-blocking latest audit, and explicit
  publication-ready admission evidence is accepted.
- A manifest missing `Handoff_State.md` or latest audit evidence fails
  admission.

### Section-entry tests

- A section run with all mapped outputs present but a root not admitted for
  publication fails conservatively.
- A section run from a publication-admitted root succeeds when mapped KTYs are
  otherwise valid.
- A mismatch between manifest/root closure evidence and local `_STATUS.md`
  appears in section QA and fails the run rather than being silently ignored.

### Package-gate tests

- Package publication cannot begin when any required section bundle is missing.
- `dbm-publish` still blocks on:
  - missing required sections
  - approved-register concordance mismatches
  - unresolved `HIGH` expansion candidates

### Closeout tests

- Human-accepted package snapshots produce `Publication_Handoff_State.md`.
- `_LATEST.md` updates only after the accepted package snapshot and the new
  closeout artifact both exist.
- Publication closeout remains auditable back to:
  - decomposition/package truth
  - accepted scope-change state
  - active handoff state
  - latest relevant audit evidence

### Contract consistency tests

- `AGENT_DBM_PUBLISHER.md`, `DBM_PUBLICATION_WORKFLOW_PLAN.md`, and this
  corrective plan agree on:
  - publisher admission rule
  - package closeout artifact
  - required section completeness before package gate
  - concordance candidate schema
- `dbm-section-publish`, `dbm-concordance-seed`, and `dbm-publish` agree with
  the corrected publisher contract.

## Assumptions And Defaults

- This is a standalone corrective plan, not a replacement for the original DBM
  publication architecture plan.
- The concordance stack is retained; only its governance alignment is revised.
- Publication remains one root -> one rewritten DBM in v1.
- `_Reconciliation/*` remains non-authoritative for DBM prose, but selected
  audit/handoff artifacts may be required as publication admission evidence.
- The implementing agent should update the relevant DBM publication docs and
  skills so another user can run Phase 8 against the stricter governance model
  without inventing policy.
