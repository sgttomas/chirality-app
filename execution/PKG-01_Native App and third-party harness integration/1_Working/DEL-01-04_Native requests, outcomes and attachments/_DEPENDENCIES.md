# Dependencies: DEL-01-04 Native requests, outcomes and attachments

## Dependency Tracking Mode
- **Mode:** FULL_GRAPH
- **Register:** the declared sections of this file together with Dependencies.csv (schema v3.1) when present (docs/SPEC.md §5.3)
- **Notes:** `projects/chirality-app-v4/execution/_Coordination/_COORDINATION.md`; no individual human-declared edge yet. Accepted interface descriptions are sources for later extraction, not declarations inferred by scaffolding.

---

## Declared Upstream (I need these before I can proceed)
- None declared at initial setup.

## Declared Downstream (These need me)
- None declared at initial setup.

---

## Extracted Dependency Register

- **Status:** EXTRACTED (UPDATE 2026-10-03, SCA-V4-003 propagation); local checks recorded in `_run_records/dependency-extract-20261003-sca003.md`.
- **Register:** `Dependencies.csv` v3.1, 29 columns; 25 ACTIVE / 1 RETIRED; ACTIVE origin: 25 EXTRACTED.
- **Classes (ACTIVE):** 6 ANCHOR (1 parent + 3 scope + 2 objective), 19 EXECUTION.
- **Execution targets (ACTIVE):** 13 DELIVERABLE, 6 EXTERNAL; direction 3 DOWNSTREAM, 16 UPSTREAM; types 4 CONSTRAINT, 3 HANDOVER, 9 INTERFACE, 3 PREREQUISITE.
- **This run:** 7 added (020, 021, 022, 023, 024, 025, 026), 5 updated in place (009, 010, 011, 012, 019), 0 retired (none); every other ACTIVE row re-observed (LastSeen only).

| DependencyID | Class / type | Direction | Target | Closure | Status |
|---|---|---|---|---|---|
| DEP-01-04-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-01 | NOT_APPLICABLE | ACTIVE |
| DEP-01-04-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-005 | NOT_APPLICABLE | ACTIVE |
| DEP-01-04-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-014 | NOT_APPLICABLE | ACTIVE |
| DEP-01-04-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-129 | NOT_APPLICABLE | ACTIVE |
| DEP-01-04-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-001 | NOT_APPLICABLE | ACTIVE |
| DEP-01-04-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-002 | NOT_APPLICABLE | ACTIVE |
| DEP-01-04-007 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-01-01 | TBD | ACTIVE |
| DEP-01-04-008 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-02 | TBD | ACTIVE |
| DEP-01-04-009 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-02 | TBD | ACTIVE |
| DEP-01-04-010 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-02 | TBD | ACTIVE |
| DEP-01-04-011 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-01 | TBD | ACTIVE |
| DEP-01-04-012 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-03 | TBD | ACTIVE |
| DEP-01-04-013 | EXECUTION / CONSTRAINT | UPSTREAM | OI-001 | TBD | ACTIVE |
| DEP-01-04-014 | EXECUTION / CONSTRAINT | UPSTREAM | OI-002 | TBD | RETIRED |
| DEP-01-04-015 | EXECUTION / CONSTRAINT | UPSTREAM | OI-008 | TBD | ACTIVE |
| DEP-01-04-016 | EXECUTION / CONSTRAINT | UPSTREAM | OI-012 | TBD | ACTIVE |
| DEP-01-04-017 | EXECUTION / CONSTRAINT | UPSTREAM | OI-014 | TBD | ACTIVE |
| DEP-01-04-018 | EXECUTION / PREREQUISITE | UPSTREAM | DEP-005 | TBD | ACTIVE |
| DEP-01-04-019 | EXECUTION / PREREQUISITE | UPSTREAM | Person performing the positive human-act case and separate faithful recorder | TBD | ACTIVE |
| DEP-01-04-020 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-03 | TBD | ACTIVE |
| DEP-01-04-021 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-05 | TBD | ACTIVE |
| DEP-01-04-022 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-02 | TBD | ACTIVE |
| DEP-01-04-023 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-03 | TBD | ACTIVE |
| DEP-01-04-024 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-04 | TBD | ACTIVE |
| DEP-01-04-025 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-03 | TBD | ACTIVE |
| DEP-01-04-026 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-02 | TBD | ACTIVE |

## Lifecycle Summary

- ACTIVE: 25; RETIRED: 1. Closure (ACTIVE): NOT_APPLICABLE 6, PENDING 0, TBD 19, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-01-04; brief: run APP-V4-SCA003-20261002 `BRIEFS.md` section "DX — dependency-extract UPDATE for the 20 registers" and the DX dispatch message (SCA-V4-003, accepted by DECISION-1 and DECISION-2; register row per `_ScopeChange/SCA-V4-003_2026-10-03_1827/Amendment_Actions.csv`, sha256 `9b7c2ce8…6d1c`); selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (brief). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (located, SHA256 `983199cc22c84398000612cd95308c840ad011d302fe31ca110a5aa97e64a70d`). Companion CSVs in the same folder (Deliverables, Packages, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE deliverable target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (brief: "from the revised ScopeOfWork text only"); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/`, MEMORY.md, _CONTEXT.md, _SEMANTIC.md and _REFERENCES.md were not read as extraction sources. Where a row carries an owner-accepted register item whose content the ScopeOfWork does not restate (ledger annotations), the row says so in Notes and names its source.
- Source ScopeOfWork.md SHA256 `8434cc47ec28e1397e7dae548183543567f0b5fcfdefaebc0b44bc1f709aacf3` (revised by SCA-V4-003 G-0104-01…14 (CLM-001, CLM-004, OUT-002, REQ-001/002/005/006, VER-005; added OUT-005, REQ-008, AC-008, VER-008, matrix row, AX-005); commit 2d5e6845c5); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table (all anchor quotes verbatim after this run) before Pass 2 examined execution statements.
- Match/merge (UPDATE): all prior ACTIVE EXTRACTED rows matched by DependencyID and kept their identities; LastSeen refreshed to 2026-10-04T01:14:27+00:00. New rows take the next DEP-01-04-SEQ numbers; FirstSeen = LastSeen = run time.
- Added 5 UPSTREAM INTERFACE rows for the new arcs: DEL-01-03 (NR-05, admitted; REQ-001 collaboration mode), DEL-01-05 (NR-07, admitted; REQ-002 selection state and Codex account), DEL-04-02 (NR-08, held; OUT-002 overlay and facets), DEL-02-03 (NR-09, held; OUT-002 display meanings) and DEL-02-04 (NR-4, held; REQ-002 role list).
- Added 2 DOWNSTREAM HANDOVER mirrors: DEL-02-03 (R2-01-04-a; REQ-008 "used by … DEL-02-03") and DEL-09-02 (R3-01-04-b; CLM-001).
- Updated in place: DEP-01-04-010 Statement (SC3-01-04-9; App act control capturing A15; REQ-008's DEL-02-02 use is mirrored here, so no new row); DEP-01-04-009 Statement (R3-01-04-a; A15 descriptor, run-start text and run-end line); DEP-01-04-019 re-quoted (VER-005 now "identified App content through the App act control"); DEP-01-04-011 and -012 Notes (REQ-008 names DEL-04-01 and DEL-04-03 as suppliers).
- Not extracted: a DOWNSTREAM row to DEL-04-01 or DEL-04-03 (G-0104-09 guard; REQ-008 states "takes its act wording and kinds from DEL-04-01" and "writes its records through the writer of DEL-04-03", both supplier relations already carried by DEP-01-04-011 and -012).
- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged except the two owner-accepted RequiredMaturity/SatisfactionStatus normalizations named above where they apply.
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream). The human-owned prefix of this file is byte-identical.
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, every ACTIVE quote an exact substring of the current ScopeOfWork and at most 30 words, target placement). Schema validator VALID (26 rows). enum invocations=23, id invocations=42, all_ok=True.
- `validate_decomposition_registers.py projects/chirality-app-v4/execution --families EVQ,DRB` after all 20 updates: 41 registers, 929 rows, 0 ERROR, 0 WARNING.
- Warnings: none.
- Comparison with `AMENDMENT_PACKET/ARC_EFFECT.md` and the closure recomputation were performed after extraction as separate coordinator checks and are reported in the run folder `DX/`; they were not extraction inputs.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:14:57+00:00 — TASK dependency-extract; UPDATE / CONSERVATIVE; accepted GROUP3-20260928T001055Z canonical SOFTWARE_DECOMP.md available; warnings 0; ACTIVE 19 (ANCHOR 6 / EXECUTION 13), RETIRED 0; no lifecycle act.
- 2026-09-29T14:34:59Z — TASK dependency-extract (APP-V4-BASIS-ALIGN-20260928 DX-1); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (unchanged source); decomposition projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md available; +0 / refreshed 0 / retired 0; ACTIVE 19 (ANCHOR 6 / EXECUTION 13), RETIRED 0; warnings none.
- 2026-09-30T02:41:42+00:00 — TASK DX (run APP-V4-SCA002-20260929); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 18 ACTIVE (6 ANCHOR / 12 EXECUTION), 1 RETIRED; 0 added, 4 updated (013, 016, 011, 018), 1 retired (014 source_revised); warnings none; dependency closure unclaimed.
- 2026-10-04T01:14:27+00:00 — TASK DX (run APP-V4-SCA003-20261002); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (revised under SCA-V4-003); decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 25 ACTIVE (6 ANCHOR / 19 EXECUTION), 1 RETIRED; 7 added, 5 updated, 0 retired; warnings none; dependency closure unclaimed.
