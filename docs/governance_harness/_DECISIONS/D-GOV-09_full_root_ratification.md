# D-GOV-09 — Full root governance ratification

Status:       RULED
HumanRuling:  Full ratification of the root `docs/` governance documents by owner (Ryan Tufts), 2026-07-11 — in-session direction
Ruling SHA:   73a0cb79b566eff4cf6102108814a308001217c2 (the `main` merge commit of PR #173, 2026-07-11 — the commit at which the ratified status blocks landed)
Date:         2026-07-11
FramedBy:     owner in-session direction, 2026-07-11; session provenance is Receipt 9 in projects/chirality-app-dev/loop/LOOP_RECEIPTS.md — this register directory is the durable decision home

Publication note: this record transcribes an already-received owner act,
backfill-style (the D-GOV pattern of `f1549afb1`); it was published later than
the act it records, by the ratification-propagation tranche (branch
`claude/ratification-propagation-2026-07-11`), and its own publication is
bound by that tranche's PR merge commit per K-AUTH-2. The Ruling SHA above
binds the ruling's execution, not this record's publication.

## Ruling basis

Owner direction of record (2026-07-11, in-session, Ryan Tufts), verbatim:

> "You can now take all the `docs/` out of the DRAFT state, making them
> authoritative.  And then merge PR #173."

Given 2026-07-11 in-session; executed the same day in PR #173 (merge
`73a0cb79b`): the status blocks of `docs/CONTRACT.md`, `docs/DIRECTIVE.md`,
`docs/SPEC.md`, and `docs/TYPES.md` flipped DRAFT → RATIFIED;
`docs/DELIVERABLE_CONCORDANCE_METHOD.md` ratified; `docs/PLAN.md` was already
ACTIVE (maintainer-adopted 2026-07-01) — no change.

## Recorded outcome

The D-GOV-05 "full ratification on its own track" track is **COMPLETE**: all
root governance documents are accepted governance in full. D-GOV-05
(docs/governance_harness/_DECISIONS/D-GOV-05_minimal_governance_basis.md)
remains the immutable record of the earlier partial basis — subsumed by this
ruling, not amended.

## Consequences recorded

1. **Harness ratification-label propagation** executed in PR #174: all 27
   K-* invariants labeled RATIFIED in
   `tools/practitioner_harness/harness_common.py`; the GEN-4 fact repointed
   to docs/CONTRACT.md; D-GOV-05 retained as the historical basis; a
   fail-closed DRAFT fallback stands for future uncataloged invariants.
2. **Severity posture deliberately reassessed:** ratification removes the
   automatic DRAFT advisory cap, but severity remains governed by the
   D-GOV-02 taxonomy and each check's own observation boundary. Verified: no
   live severity or exit-code change (no BLOCK-emitting check used a
   formerly-DRAFT invariant).
3. **The DRAFT_BASIS_* detectors remain in force.** They police stale or
   improper draft-artifact use generally and are not obsoleted by root
   ratification.
4. **Subsequent lifecycle-semantics amendment** of the ratified SPEC/TYPES
   executed under a separate owner direction (PR #174; app-dev corpus v6;
   piping D-39/DEC-071).

## Scope not granted

Nothing beyond transcription: no severity policy change; no new checks.
