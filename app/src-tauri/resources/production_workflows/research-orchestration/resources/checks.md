# QA_CHECKS — research-orchestration

Minimum output validity checks. The fan-out is not `RESEARCH_PACKET_READY` unless all of
these hold; otherwise report the lower verdict with the specific failing check.

## Required checks

1. **Load-bearing claims are verified against live or accepted sources.** This applies
   whatever `CRITIC_REQUIRED` is set to. Every load-bearing claim that entered authority
   (`R3+`) has a distinct `Evidence_Map.csv` row with `VerificationSource = LIVE_TREE` or
   `ACCEPTED_SNAPSHOT` — *not* the original anchor, *not* `INHERITED_BRIEF`, and *not*
   `RETRIEVAL_INDEX`. A second retrieval query, including one in another `--mode`, is not
   such support. Do not report PASS for a load-bearing claim whose only support is an
   inherited brief fact or a retrieval hit.
2. **Critic actually ran, when required.** When `CRITIC_REQUIRED = true`, each load-bearing
   claim also shows a recorded critic re-verification step (a second source-read, query, or
   stream). Record what that step actually was; a repeat query or re-read by the same agent
   is not a separate reviewer, isolated context, or independent primary source, and must not
   be described as one. When `CRITIC_REQUIRED = false`, this check is not applicable and
   check 1 still applies.
3. **No silent stream loss or coverage inflation.** Every planned `StreamPlan` stream has a
   terminal status (`COMPLETED` / `RETRIED-COMPLETED` / `FAILED-WITH-PARTIAL` /
   `FAILED-NO-OUTPUT`). Every stream whose required coverage remains unresolved — a
   `FAILED-NO-OUTPUT` stream, or a `FAILED-WITH-PARTIAL` stream whose `CoverageGaps[]` were
   not closed by later work — is surfaced as a coverage gap in `HANDOFF_STATE.md`, never
   omitted. A preserved partial packet does not by itself count as complete coverage.
4. **Recovery records are truthful.** Per-stream retries ≤ `MAX_RETRIES`. Each attempt
   records its attempt number, its parent attempt, and the recovery mechanism actually used:
   `RESUME` with the identifier the host's resume facility actually returned, only when such a
   resume actually executed, otherwise `NEW_ATTEMPT` with the preserved packets and
   evidence it builds on. Never describe a newly launched attempt as a resume. A
   `FAILED_INPUTS` return is not a transient failure and does not consume retries. Record a
   corrected-brief attempt as `NEW_ATTEMPT` with its parent; route a missing input that needs
   a human decision (for example the accepted snapshot) to the human; otherwise, when the brief cannot be
   corrected, close the stream as `FAILED-NO-OUTPUT` or `FAILED-WITH-PARTIAL` with a coverage gap.
5. **Freshness recorded.** The `check_snapshot_freshness.py` verdict is in `HANDOFF_STATE.md`;
   if `STALE`, the caveat is explicit and no rebuild/refresh was performed.
6. **Conflicts surfaced.** Disagreements found during verification or the critic stage are
   rows in `Conflicts.csv`, not silently reconciled.
7. **Packet integrity.** The packet contains the canonical files with correct headers (the
   scaffolder guarantees this) and the queries in `Query_Log.csv` are tool-emitted, not
   hand-written.
8. **Write boundary held.** Writes stay within the allocated packet directories and the run
   record. Every scaffolder invocation passed `--no-update-latest`, and
   `{ResearchRoot}/_LATEST.md` was not modified by this run.

## Failure reporting

- Required planned coverage is the `StreamPlan` coverage frozen at `WORKFLOW.md` Method step 1, unless the
  human narrows it on record. Do not reclassify planned coverage as optional to reach a
  higher verdict.
- Report a single readiness verdict, determined by the applicable checks and the required
  planned coverage that remains unresolved — not merely by whether every stream terminated
  or produced a packet:
  - `RESEARCH_PACKET_READY` — all applicable checks pass and no required planned coverage
    remains unresolved.
  - `READY_WITH_COVERAGE_GAPS` — the findings being returned satisfy all applicable validity
    and verification checks, but required planned coverage remains incomplete; the gaps are
    surfaced in `HANDOFF_STATE.md`.
  - `BLOCKED` — a mandatory validity or verification requirement remains unsatisfied; in
    particular, a load-bearing claim proposed for reliance lacks the verification check 1
    (and, when required, check 2) demands.
- A gap closed by a later attempt no longer forces a gapped verdict; keep the earlier
  attempt in the retry trail either way.
- When an unresolved gap undermines a load-bearing conclusion, withdraw that conclusion from
  reliance or report `BLOCKED`; never present it as ready with a minor caveat.
- On `BLOCKED` or `READY_WITH_COVERAGE_GAPS`, name the specific claims/streams and what is
  missing. Never upgrade the verdict to hide a gap.

## Required evidence / logs

- `Query_Log.csv` (tool-emitted) — the executed query trail.
- The per-stream status ledger (in `HANDOFF_STATE.md` or the run record), including the attempt
  trail with parentage and actual recovery mechanism.
- `Evidence_Map.csv` with `VerificationSource` / `AssertionMode` / `LoadBearing` populated.
