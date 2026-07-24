# QA CHECKS — evaluation-protocol

## Minimum output validity checks

1. `EVALUATION_PROTOCOL.md` exists under the brief's write target and names the
   accepted basis, the accepted toolbelt, the dispatch order, output locations,
   and the decision points (and the scoring rubric if one was accepted).
2. `FINDINGS.csv` rows are schema-complete: every row carries all ten columns —
   `FindingID`, `Concern`, `Classification`, `Severity`, `Scope`, `Claim`,
   `EvidenceRefs`, `Status`, `RecommendedOwner`, `RerunRequirement` — in that
   order.
3. Every findings row is evidence-linked through `EvidenceRefs` (a file,
   immutable snapshot, tool output, or validated Agent 2 return). Unsupported
   rows are labeled `ASSUMPTION`; missing-evidence rows are labeled `UNKNOWN`.
4. `EVALUATION_REPORT.md` contains every section of the report content contract:
   basis, method, coverage, validated-return inventory, findings,
   conflicts/unknowns, optional scorecard, recommendations, decision queue, and
   handoff summary.
5. `HANDOFF.md` names the human decisions, remediation owners, blockers, and
   rerun requirements, and records derivative-package status.
6. Required child returns passed schema and coverage checks before fan-in;
   missing, invalid, or conflicting returns are recorded as visible, not
   averaged away.
7. Any score present is backed by an accepted rubric; no score appears without
   one.
8. No files were written outside the brief's `AllowedWriteTargets`; no subject
   file outside `_Evaluation/` was modified.

## Failure reporting expectations

Use `FAILED_INPUTS` when:

- `EXECUTION_ROOT` is missing or not a directory,
- the accepted basis, evaluation questions, scope, permitted toolbelt, or write
  targets are absent from the brief,
- a required parent directory under the write target does not exist.

Use `BLOCKED` (return to EVALUATION for human routing) when:

- a mandatory child return is missing or invalid and has not been waived by the
  human,
- scoring is requested but no accepted rubric was supplied,
- concurrent fan-out is required but no fan-out authorization was supplied.

A run must not be reported as closed unless every check above passes. Recording
files is not closure: basis, coverage, unresolved conflicts, blockers, and rerun
requirements must be present.

## Required evidence

- The preserved child returns under `returns/<DispatchID>/` as produced.
- Deterministic validator outputs, where the accepted toolbelt used them, cited
  in `EvidenceRefs`.
