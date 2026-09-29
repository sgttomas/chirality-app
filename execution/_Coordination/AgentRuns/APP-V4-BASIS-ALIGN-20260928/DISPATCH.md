# Dispatch — APP-V4-BASIS-ALIGN-20260928

Mechanism: Claude Code `Agent` subagents (Type 2; they do not delegate).
Parent: HELP_HUMAN, integrating under a recorded WORKING_ITEMS consultation.

| Node | State |
|---|---|
| B0 | Graph, decision record, briefs |
| P1 | Amendment packet RETURNED (AMENDMENT_PACKET/): 47 MODIFY actions; 21 basis replacements; 124 SoW blocks across 16 SoWs; 74 C1 items: 45 kept, 29 amended; 30 owner items. All edits dry-run clean; 16/16 SoWs validate. Fence verified |
| P2 | DAG preparation RETURNED (DAG_PREP/): 41 arcs (38 C1 kept, N-12/N-B8 dropped, 3 added); SCCs unchanged; 69 rows to add (59 grounded, 10 need P1 wording, now drafted); 50 deferred; scratch closure run shows DEPARTURE (16 deliverables). Fence verified |
| K1 | Owner checkpoint A: presented |
| K1 | Accepted by the owner (DECISION-7): scope-change groups 1–2 |
| AK1 | Applied the accepted basis and decomposition edits (15 Markdown replacements, 29 CSV field edits, 11 `_CONTEXT.md` edits); group-1/2 decision snapshots and `_ScopeChange` candidate artifacts; post-change audit (7 packages) vs baseline; DAG-001 currency 130/130. Held until group-3 acceptance: A07, A17a–c and D-15 (need ACCEPT_DATE/snapshot); the Coverage_Telemetry recompute (writer and values to be named at group 3). Fence verified |
| V11 | READY FOR GROUP 3: 0 BLOCKING, 3 minor, 5 notes. F1/F2 closed by the integrator in the candidate Handoff_State.md and RUN_SUMMARY.md (bound files untouched; manifests re-verified); F3 disclosed |
| K2 | Accepted by the owner (DECISION-8, 2026-09-29) |
| AK2 | Group-3 decision snapshot; H-1…H-4 applied (A07, A17a–c, D-15, second coverage recompute); post-acceptance validation 43/43 PASS; audit rerun (COV-131 Change Register part closed); accepted snapshot `SCA-V4-001_2026-09-28_2155`, and `_ScopeChange/_LATEST.md` moved; closure OPEN_PENDING_DERIVATIVE_CLOSURE (Coverage_Telemetry STALE_REBUILD_REQUIRED). DAG-001 130/130. Note: the A17b line join in HOST_INTEGRATION is cosmetic and verbatim; carried to SCA-V4-002. Fence verified |
| RV-1…RV-4 | All 16 SoWs revised under SCA-V4-001: each prior hash matched, every E-block applied exactly, validators and boundary check pass, and MODE=VERIFY passed (by the same TASK; independent review follows in V12). No `_STATUS.md` touched. Findings carried to SCA-V4-002: DEL-03-03 CLM-002's "unresolved reserved-act and classifier decisions" tail; the REVISION_SCOPE header lines omit CLM-002 for DEL-03-01 and DEL-03-03 (edits applied as E-blocks). Fences verified |
| DX-1/2/3 | dependency-extract UPDATE for 18 deliverables (ScopeOfWork.md only), all validators passing. The DEL-09-06 guard wording in the brief was wrong; the integrator ruled on the intended guard (no SCC-002 member depends on DEL-09-06), and the row was then applied. Result: 198 arcs (161 + 37), 124 admitted / 74 candidate; six SCCs unchanged. Missing against the accepted 41: N-18, N-21, N-24, X-1 (the SoWs state ownership, not consumption; no edge under this repo's extraction convention); N-07 is carried by its supplier-side row. For SCA-V4-002: the DEL-09-07 TBD-002/003, DEL-01-04 and DEL-02-02 SoW text still calls OI-001/002/012 open; Open_Issues OI-001/002 are still OPEN; DEL-03-03 CLM-002 tail; A17b line join. Fences verified |
| D1 | Closure: 198 arcs, 6 SCCs unchanged. Currency: DEPARTURE, 15 DAG pending (DEL-01-04 not, since X-1 was not produced). DAG-002 candidate: 41 nodes / 124 admitted / 74 held / 264 excluded; `audit_dag --canonical --strict` exit 0; CASE-002 evidence updated; PROPOSED_LATEST in §11.2 form; CHECKPOINT_C.md written. Nothing accepted; `_DAG/_LATEST.md` untouched. Fence verified |
| V12 | Independent review of the SoW revisions, registers and DAG-002: ACTIVE |
