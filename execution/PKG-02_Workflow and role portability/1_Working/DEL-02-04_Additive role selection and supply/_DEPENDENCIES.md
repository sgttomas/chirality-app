# Dependencies: DEL-02-04 Additive role selection and supply

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
- **Register:** `Dependencies.csv` v3.1, 29 columns; 19 ACTIVE / 0 RETIRED; ACTIVE origin: 19 EXTRACTED.
- **Classes (ACTIVE):** 9 ANCHOR (1 parent + 5 scope + 3 objective), 10 EXECUTION.
- **Execution targets (ACTIVE):** 7 DELIVERABLE, 3 EXTERNAL; direction 5 DOWNSTREAM, 5 UPSTREAM; types 2 CONSTRAINT, 5 HANDOVER, 2 INTERFACE, 1 PREREQUISITE.
- **This run:** 3 added (017, 018, 019), 2 updated in place (010, 016), 0 retired (none); every other ACTIVE row re-observed (LastSeen only).

| DependencyID | Class / type | Direction | Target | Closure | Status |
|---|---|---|---|---|---|
| DEP-02-04-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-02 | NOT_APPLICABLE | ACTIVE |
| DEP-02-04-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-013 | NOT_APPLICABLE | ACTIVE |
| DEP-02-04-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-057 | NOT_APPLICABLE | ACTIVE |
| DEP-02-04-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-058 | NOT_APPLICABLE | ACTIVE |
| DEP-02-04-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-059 | NOT_APPLICABLE | ACTIVE |
| DEP-02-04-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-126 | NOT_APPLICABLE | ACTIVE |
| DEP-02-04-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-001 | NOT_APPLICABLE | ACTIVE |
| DEP-02-04-008 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-002 | NOT_APPLICABLE | ACTIVE |
| DEP-02-04-009 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-003 | NOT_APPLICABLE | ACTIVE |
| DEP-02-04-010 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-01 | PENDING | ACTIVE |
| DEP-02-04-011 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-01 | PENDING | ACTIVE |
| DEP-02-04-012 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-04-03 | PENDING | ACTIVE |
| DEP-02-04-013 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-11-02 | PENDING | ACTIVE |
| DEP-02-04-014 | EXECUTION / PREREQUISITE | UPSTREAM | DEP-006 | PENDING | ACTIVE |
| DEP-02-04-015 | EXECUTION / CONSTRAINT | UPSTREAM | OI-008 | PENDING | ACTIVE |
| DEP-02-04-016 | EXECUTION / CONSTRAINT | UPSTREAM | OI-018 | PENDING | ACTIVE |
| DEP-02-04-017 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-04 | PENDING | ACTIVE |
| DEP-02-04-018 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-10-03 | PENDING | ACTIVE |
| DEP-02-04-019 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-01-04 | PENDING | ACTIVE |

## Lifecycle Summary

- ACTIVE: 19; RETIRED: 0. Closure (ACTIVE): NOT_APPLICABLE 9, PENDING 10, TBD 0, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-02-04; brief: run APP-V4-SCA003-20261002 `BRIEFS.md` section "DX — dependency-extract UPDATE for the 20 registers" and the DX dispatch message (SCA-V4-003, accepted by DECISION-1 and DECISION-2; register row per `_ScopeChange/SCA-V4-003_2026-10-03_1827/Amendment_Actions.csv`, sha256 `9b7c2ce8…6d1c`); selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (brief). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (located, SHA256 `983199cc22c84398000612cd95308c840ad011d302fe31ca110a5aa97e64a70d`). Companion CSVs in the same folder (Deliverables, Packages, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE deliverable target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (brief: "from the revised ScopeOfWork text only"); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/`, MEMORY.md, _CONTEXT.md, _SEMANTIC.md and _REFERENCES.md were not read as extraction sources. Where a row carries an owner-accepted register item whose content the ScopeOfWork does not restate (ledger annotations), the row says so in Notes and names its source.
- Source ScopeOfWork.md SHA256 `2327508f2290e7cf2528950d65bc331d72a80d8413a13fe31ea8f867cce4d176` (revised by SCA-V4-003 G-0204-01…13 (CLM-002, REQ-001/002/003, AC-001, AC-003, open-matter rows, TBD-001, AX-005); commit 2d5e6845c5); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table (all anchor quotes verbatim after this run) before Pass 2 examined execution statements.
- Match/merge (UPDATE): all prior ACTIVE EXTRACTED rows matched by DependencyID and kept their identities; LastSeen refreshed to 2026-10-04T01:14:27+00:00. New rows take the next DEP-02-04-SEQ numbers; FirstSeen = LastSeen = run time.
- Added 3 DOWNSTREAM HANDOVER rows from the new CLM-002 receivers sentence: DEL-03-04 and DEL-10-03 (R3-02-04-a, -b, existing admitted arcs) and DEL-01-04 (R3-02-04-c, mirror of the new held arc NR-4).
- Updated in place: DEP-02-04-010 Statement (SC3-02-04-8; the surface names come from the ledger and are noted as not restated in the SoW); DEP-02-04-016 Notes (R3-02-04-d; OI-018 answered for the App, open for hosts).
- Not extracted: NR-06 (→ DEL-01-03) and NR-10 (→ DEL-02-02), both withdrawn; the revised text adds no consumption of either. DEL-11-02's counterpart for DEP-02-04-013 stays with its owner (R22-7-open).
- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged except the two owner-accepted RequiredMaturity/SatisfactionStatus normalizations named above where they apply.
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream). The human-owned prefix of this file is byte-identical.
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, every ACTIVE quote an exact substring of the current ScopeOfWork and at most 30 words, target placement). Schema validator VALID (19 rows). enum invocations=22, id invocations=33, all_ok=True.
- `validate_decomposition_registers.py projects/chirality-app-v4/execution --families EVQ,DRB` after all 20 updates: 41 registers, 929 rows, 0 ERROR, 0 WARNING.
- Warnings: none.
- Comparison with `AMENDMENT_PACKET/ARC_EFFECT.md` and the closure recomputation were performed after extraction as separate coordinator checks and are reported in the run folder `DX/`; they were not extraction inputs.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-27 — TASK dependency-extract; UPDATE / CONSERVATIVE; explicit GROUP3-20260928T001055Z decomposition present; ACTIVE 16 (ANCHOR 9, EXECUTION 7), RETIRED 0; no mandatory integrity warning. Actual execution timestamp and verification evidence recorded in `_run_records/dependency-extract-20260927.md`.
- 2026-10-04T01:14:27+00:00 — TASK DX (run APP-V4-SCA003-20261002); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (revised under SCA-V4-003); decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 19 ACTIVE (9 ANCHOR / 10 EXECUTION), 0 RETIRED; 3 added, 2 updated, 0 retired; warnings none; dependency closure unclaimed.
