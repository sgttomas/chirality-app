# Dependencies: DEL-03-02 Proposal, validation and outcome contract

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
- **Register:** `Dependencies.csv` v3.1, 29 columns; 34 ACTIVE / 0 RETIRED; ACTIVE origin: 34 EXTRACTED.
- **Classes (ACTIVE):** 15 ANCHOR (1 parent + 12 scope + 2 objective), 19 EXECUTION.
- **Execution targets (ACTIVE):** 15 DELIVERABLE, 4 EXTERNAL; direction 12 DOWNSTREAM, 7 UPSTREAM; types 2 CONSTRAINT, 12 HANDOVER, 2 INTERFACE, 3 PREREQUISITE.
- **This run:** 7 added (028, 029, 030, 031, 032, 033, 034), 0 updated in place (none), 0 retired (none); every other ACTIVE row re-observed (LastSeen only).

| DependencyID | Class / type | Direction | Target | Closure | Status |
|---|---|---|---|---|---|
| DEP-03-02-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-03 | NOT_APPLICABLE | ACTIVE |
| DEP-03-02-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-070 | NOT_APPLICABLE | ACTIVE |
| DEP-03-02-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-090 | NOT_APPLICABLE | ACTIVE |
| DEP-03-02-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-091 | NOT_APPLICABLE | ACTIVE |
| DEP-03-02-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-170 | NOT_APPLICABLE | ACTIVE |
| DEP-03-02-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-171 | NOT_APPLICABLE | ACTIVE |
| DEP-03-02-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-172 | NOT_APPLICABLE | ACTIVE |
| DEP-03-02-008 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-173 | NOT_APPLICABLE | ACTIVE |
| DEP-03-02-009 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-174 | NOT_APPLICABLE | ACTIVE |
| DEP-03-02-010 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-175 | NOT_APPLICABLE | ACTIVE |
| DEP-03-02-011 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-176 | NOT_APPLICABLE | ACTIVE |
| DEP-03-02-012 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-177 | NOT_APPLICABLE | ACTIVE |
| DEP-03-02-013 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-178 | NOT_APPLICABLE | ACTIVE |
| DEP-03-02-014 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-004 | NOT_APPLICABLE | ACTIVE |
| DEP-03-02-015 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-005 | NOT_APPLICABLE | ACTIVE |
| DEP-03-02-016 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-03-01 | TBD | ACTIVE |
| DEP-03-02-017 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-04-01 | TBD | ACTIVE |
| DEP-03-02-018 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-04-02 | TBD | ACTIVE |
| DEP-03-02-019 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-04-03 | TBD | ACTIVE |
| DEP-03-02-020 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-03 | TBD | ACTIVE |
| DEP-03-02-021 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-04 | TBD | ACTIVE |
| DEP-03-02-022 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-09 | TBD | ACTIVE |
| DEP-03-02-023 | EXECUTION / PREREQUISITE | UPSTREAM | EXTERNAL DEP-001 | TBD | ACTIVE |
| DEP-03-02-024 | EXECUTION / HANDOVER | DOWNSTREAM | EXTERNAL DEP-001 | TBD | ACTIVE |
| DEP-03-02-025 | EXECUTION / CONSTRAINT | UPSTREAM | ISSUES OI-014 | TBD | ACTIVE |
| DEP-03-02-026 | EXECUTION / CONSTRAINT | UPSTREAM | Relevant contract and host owners: agreement on proposal representation and mechanics | TBD | ACTIVE |
| DEP-03-02-027 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-01 | TBD | ACTIVE |
| DEP-03-02-028 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-01 | TBD | ACTIVE |
| DEP-03-02-029 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-03 | TBD | ACTIVE |
| DEP-03-02-030 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-05-01 | TBD | ACTIVE |
| DEP-03-02-031 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-05-02 | TBD | ACTIVE |
| DEP-03-02-032 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-06 | TBD | ACTIVE |
| DEP-03-02-033 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-10-03 | TBD | ACTIVE |
| DEP-03-02-034 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-02 | TBD | ACTIVE |

## Lifecycle Summary

- ACTIVE: 34; RETIRED: 0. Closure (ACTIVE): NOT_APPLICABLE 15, PENDING 0, TBD 19, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-03-02; brief: run APP-V4-SCA003-20261002 `BRIEFS.md` section "DX — dependency-extract UPDATE for the 20 registers" and the DX dispatch message (SCA-V4-003, accepted by DECISION-1 and DECISION-2; register row per `_ScopeChange/SCA-V4-003_2026-10-03_1827/Amendment_Actions.csv`, sha256 `9b7c2ce8…6d1c`); selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (brief). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (located, SHA256 `983199cc22c84398000612cd95308c840ad011d302fe31ca110a5aa97e64a70d`). Companion CSVs in the same folder (Deliverables, Packages, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE deliverable target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (brief: "from the revised ScopeOfWork text only"); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/`, MEMORY.md, _CONTEXT.md, _SEMANTIC.md and _REFERENCES.md were not read as extraction sources. Where a row carries an owner-accepted register item whose content the ScopeOfWork does not restate (ledger annotations), the row says so in Notes and names its source.
- Source ScopeOfWork.md SHA256 `e2f8d49de699fd661988cdbe73c340d7b8aaef0dc14d1b8d5732a57e1be5a21f` (revised by SCA-V4-003 G-0302-01…04 (OUT-001, CLM-004, AX-005); commit 2d5e6845c5); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table (all anchor quotes verbatim after this run) before Pass 2 examined execution statements.
- Match/merge (UPDATE): all prior ACTIVE EXTRACTED rows matched by DependencyID and kept their identities; LastSeen refreshed to 2026-10-04T01:14:27+00:00. New rows take the next DEP-03-02-SEQ numbers; FirstSeen = LastSeen = run time.
- Added 6 DOWNSTREAM HANDOVER rows from the new CLM-004 receivers sentence (R-02-2: DEL-02-01, 02-03, 05-01, 05-02, 09-06, 10-03) and 1 UPSTREAM INTERFACE row to DEL-04-02 (R-02-3, consumer side of the held arc N-05).
- Not extracted: the DOWNSTREAM row to DEL-03-01 (ledger R-02-1, mirror of DEP-03-01-026, held). The ScopeOfWork names DEL-03-01 only as the supplier of the catalog (CLM-003, the required-interfaces paragraph, REQ-013); no sentence states that DEL-03-01 receives proposal refusal/application behaviour from this deliverable. The arc exists through DEP-03-01-026, so the arc set is unaffected. Returned to the coordinator.
- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged except the two owner-accepted RequiredMaturity/SatisfactionStatus normalizations named above where they apply.
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream). The human-owned prefix of this file is byte-identical.
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, every ACTIVE quote an exact substring of the current ScopeOfWork and at most 30 words, target placement). Schema validator VALID (34 rows). enum invocations=22, id invocations=54, all_ok=True.
- `validate_decomposition_registers.py projects/chirality-app-v4/execution --families EVQ,DRB` after all 20 updates: 41 registers, 929 rows, 0 ERROR, 0 WARNING.
- Warnings: none.
- Comparison with `AMENDMENT_PACKET/ARC_EFFECT.md` and the closure recomputation were performed after extraction as separate coordinator checks and are reported in the run folder `DX/`; they were not extraction inputs.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:05:57.943525+00:00 — TASK `/root/renewal_research_strategy/dep_del_03_02`; UPDATE / CONSERVATIVE; explicit accepted decomposition path above; 26 ACTIVE (15 ANCHOR / 11 EXECUTION), 0 RETIRED; no floating/multiple-parent warning; conditional external inputs and open agreements retained.
- 2026-09-29T14:43:26+00:00 — TASK DX-2 (run APP-V4-BASIS-ALIGN-20260928); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 27 ACTIVE (15 ANCHOR / 12 EXECUTION), 0 RETIRED; 1 added (DEL-02-01), 2 updated in place (016, 017), 0 retired; warnings none; dependency closure unclaimed.
- 2026-10-04T01:14:27+00:00 — TASK DX (run APP-V4-SCA003-20261002); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (revised under SCA-V4-003); decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 34 ACTIVE (15 ANCHOR / 19 EXECUTION), 0 RETIRED; 7 added, 0 updated, 0 retired; warnings none; dependency closure unclaimed.
