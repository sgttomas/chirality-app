# D-GOV-28 Candidate Handoff

## State

- Candidate status: `ADOPTION_READY_ONLY_THROUGH_D_GOV_28`
- Authority status: `NON_AUTHORITATIVE_PROPOSAL`
- Accepted upstream basis:
  `main@918bb48b8fcee66c031d0d6d4040a46089f96067`
- Current accepted PRD remains: Rev 5 via D-GOV-22
- Candidate PRD: `PRD_ROOT_REV6_CANDIDATE.md`
- Root authority transcribed: D-GOV-20
- Tier-0 counterpart: D-T0-23, coordination only

## What is complete

- D-GOV-28 verified as the next unused root governance identifier.
- One new stable PRD commitment, O-11, is staged but inert.
- Every exact-source sentence introduced or changed by Rev 6 and labeled
  TRANSCRIBED — both O-1 sentences and all ten D-GOV-20 ruled architecture
  statements — is copied verbatim and declared in `TRANSCRIPTION_SPEC.json`.
  Inherited Rev 5 synthesis is explicitly outside this verbatim check.
- Source files are read from the declared Git basis and matched to expected
  full-file SHA-256 identities; mutable working-tree sources are not accepted
  as substitutes.
- Uncovered seams are recorded with stable IDs in `OPEN_ITEMS.csv`.
- A runnable deterministic concordance validator and frozen output are
  included.
- Package files are hash-listed in `ARTIFACT_HASHES.sha256`; the hash list
  excludes itself by convention.

## What is not authorized or complete

- No PRD byte is adopted.
- No D-GOV-28 decision record or register row exists.
- No accepted decomposition, register, pointer, SOW, App, PEC, runtime,
  instruction, or product file is changed.
- No SCOPE_CHANGE gate is approved.
- No package, deliverable, estimate, dependency, or implementation is created.
- No contract is repinned.

## Owner gates

1. Review the exact candidate and concordance report.
2. Choose D-GOV-28 O-A (adopt), O-B (revise), or O-C (decline/defer).
3. If O-A is ruled against an exact candidate SHA, publish the decision record
   and apply the PRD amendment through its own M2/CHANGE closeout.
4. Only after adoption may Root SCOPE_CHANGE advance beyond its contingent
   Gate 1 intake, and then only through each explicit owner gate.

## Rerun requirement

Rerun `validate_transcriptions.py` and regenerate both
`CONCORDANCE_REPORT.json` and `ARTIFACT_HASHES.sha256` after any candidate,
specification, or open-item change. Any transcription mismatch blocks the
candidate gate; a PASS is structural evidence, not owner acceptance.
