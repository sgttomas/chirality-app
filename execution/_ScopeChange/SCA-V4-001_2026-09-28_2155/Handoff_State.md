# Handoff state — SCA-V4-001 (CANDIDATE, before group 3)

**Status.** This is a candidate awaiting the owner's checkpoint group 3.
Groups 1 and 2 were accepted (DECISION-7). Group 3 is **not accepted**: there
is no `SCA-*` accepted snapshot and no `_ScopeChange/_LATEST.md`.

**Accepted snapshot:** none yet. The authorized group snapshots are
`checkpoint_snapshots/SCA-V4-001_GROUP-1_2026-09-28/` and `…_GROUP-2_2026-09-28/`.

**Candidate applied at:** `230bf1e64`.
- Basis docs: PRD, ARCHITECTURE, HOST_INTEGRATION, EXAMINATION.
- Decomposition: registers, SOFTWARE_DECOMP D-16, `_CONTEXT.md` mirrors.
- Consolidated_Coverage recompute (first pass).

**Independent review:** `AgentRuns/APP-V4-BASIS-ALIGN-20260928/reviews/V11.md` —
READY FOR GROUP 3. It found 0 BLOCKING items, 3 minor findings and 5 notes.

## Applied only after group-3 acceptance (acceptance-conditional)

| # | Item | Tokens filled at acceptance |
|---|---|---|
| H-1 | A07: PRD status paragraph and §0 source table (three pairs; only the first carries `{ACCEPT_DATE}`) | `SCA-V4-001`; the group-3 act date |
| H-2 | A17a–c: ARCHITECTURE, HOST_INTEGRATION and EXAMINATION status paragraphs | same |
| H-3 | D-15: new `## Decision Log` section with the amendment entry | `SCA-V4-001`; the act date; snapshot `SCA-V4-001_2026-09-28_2155` |
| H-4 | B8: **second** Consolidated_Coverage recompute after H-1…H-3. A separate item (V11 F1) | — |
| H-5 | Post-acceptance validation under `_PostAcceptanceValidation/`, and an audit-decomp rerun with the seven-package scope. COV-131 (Change Register binding) should close | — |

## Derivative packages and propagation (after acceptance)

| Package | State | Next owning workflow |
|---|---|---|
| 16 ScopeOfWork contracts (the 14 IN_PROGRESS plus DEL-09-07 and DEL-08-01) | STALE; revise per SOW_REVISIONS.md | `scope-of-work` MODE=REVISE, one deliverable per brief |
| Dependency registers (69 rows; 50 deferred) | STALE; rows in DAG_PREP/REGISTER_CHANGES.md | `dependency-extract` per deliverable, after REVISE |
| DAG-001 | Will depart; DAG-002 candidate | `project-dag` currency audit, then TRIGGER=SUCCESSOR; owner checkpoint C |
| Coverage_Telemetry.json | **STALE_REBUILD_REQUIRED** (COV-119/120). No tool writes it, and the packet routes it to read-only audit-decomp. The derivable values are in POSTCHANGE/projections.json | Decomposition owner. A bounded brief must name the writer and the exact bytes |
| Design files (17) pinning the basis docs | Re-pin to the amended texts at the next design pass | App v4 design undertaking |

**Closure verdict:** OPEN_PENDING_DERIVATIVE_CLOSURE.

## Crosswalk for inconsistent action IDs (V11 residual 4)

The hash-bound register is not changed. Mapping:

- register row 7 = A07 (held);
- row 11 = A11a+b;
- row 17 = A17a–c (held);
- row 30 = D-16 (applied) + D-15 (held);
- row 31 = B8 (first pass applied; second pass H-4).

## Residuals outside SCA-V4-001

- **DEL-10-03 ScopeOfWork REQ-005.** It still says "the minimal local-first
  host loop". Route it to a follow-on amendment (SCA-V4-002) or a separately
  authorized REVISE. It is not edited here.
- **`_Coordination/HANDOFF_SWBPIPE_DOMAINS.md` l.22** ("local-first host
  operation"). It carries forward with the next DECISION-5 relay to SWBPIPE.
- **`Allocation_Rationale.csv`.** NO_CHANGE, historical. The owner accepted
  that classification.
- **`tools/query/scan_next_amendment_id.sh`.** It is zsh by design and works
  when invoked directly. A bash-invocation fix would be a separately
  authorized Root tooling change.

## Process disclosure (V11 F3)

The group-1 manifest binds a candidate `Brief.md` that already describes the
post-change audit. The group-1 snapshot bytes were finalized after
application, and application landed in the same commit. The snapshots are
not rewritten; this note discloses the sequence.

**Minor notes carried:** V11 F4, F5 (the register uses `;` separators in
DownstreamReruns), F6, F7 and F8.
