# QA_CHECKS — research-orchestration

Minimum output validity checks. The fan-out is not `RESEARCH_PACKET_READY` unless all of
these hold; otherwise report the lower verdict with the specific failing check.

## Required checks

1. **Load-bearing claims are live-verified.** Every claim that entered authority (`R3+`) has
   a distinct `Evidence_Map.csv` row with `VerificationSource = LIVE_TREE` (or accepted
   snapshot) — *not* the original anchor and *not* `INHERITED_BRIEF`. Do not report PASS for
   a load-bearing claim whose only support is an inherited brief fact or a retrieval hit.
2. **Critic actually ran.** When `CRITIC_REQUIRED = true`, each load-bearing claim shows an
   independent re-verification step (a second query/source-read or stream). A claim with no
   recorded critic step is not authority-ready.
3. **No silent stream loss.** Every planned `StreamPlan` stream has a terminal status
   (`COMPLETED` / `RETRIED-COMPLETED` / `FAILED-WITH-PARTIAL` / `FAILED-NO-OUTPUT`). Any
   `FAILED-NO-OUTPUT` stream is surfaced as a coverage-gap in `HANDOFF_STATE.md`, never omitted.
4. **Retry discipline.** Per-stream retries ≤ `MAX_RETRIES`; each retry records the
   `resumeFromRunId` used and the attempt number.
5. **Freshness recorded.** The `check_snapshot_freshness.py` verdict is in `HANDOFF_STATE.md`;
   if `STALE`, the caveat is explicit and no rebuild/refresh was performed.
6. **Conflicts surfaced.** Disagreements found by the critic stage are rows in
   `Conflicts.csv`, not silently reconciled.
7. **Packet integrity.** The packet contains the canonical files with correct headers (the
   scaffolder guarantees this) and the queries in `Query_Log.csv` are tool-emitted, not
   hand-written.

## Failure reporting

- Report a single readiness verdict:
  - `RESEARCH_PACKET_READY` — all streams resolved, critic ran, no unrecorded gaps.
  - `READY_WITH_COVERAGE_GAPS` — some streams `FAILED-NO-OUTPUT`; gaps surfaced in `HANDOFF_STATE.md`.
  - `BLOCKED` — the critic could not live-verify one or more load-bearing claims.
- On `BLOCKED` or `READY_WITH_COVERAGE_GAPS`, name the specific claims/streams and what is
  missing. Never upgrade the verdict to hide a gap.

## Required evidence / logs

- `Query_Log.csv` (tool-emitted) — the executed query trail.
- The per-stream status ledger (in `HANDOFF_STATE.md` or the run record), including the retry trail.
- `Evidence_Map.csv` with `VerificationSource` / `AssertionMode` / `LoadBearing` populated.
