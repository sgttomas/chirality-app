# Dependencies: DEL-09-09 External control and catalog-extension trace

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
- **Register:** `Dependencies.csv` v3.1, 29 columns; 24 ACTIVE / 0 RETIRED; ACTIVE origin: 24 EXTRACTED.
- **Classes (ACTIVE):** 6 ANCHOR (1 parent + 3 scope + 2 objective), 18 EXECUTION.
- **Execution targets (ACTIVE):** 9 DELIVERABLE, 9 EXTERNAL; direction 1 DOWNSTREAM, 17 UPSTREAM; types 5 CONSTRAINT, 1 HANDOVER, 12 PREREQUISITE.
- **This run:** 0 added (none), 3 updated in place (007, 010, 014), 0 retired (none); every other ACTIVE row re-observed (LastSeen only).

| DependencyID | Class / type | Direction | Target | Closure | Status |
|---|---|---|---|---|---|
| DEP-09-09-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-09 | NOT_APPLICABLE | ACTIVE |
| DEP-09-09-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-073 | NOT_APPLICABLE | ACTIVE |
| DEP-09-09-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-203 | NOT_APPLICABLE | ACTIVE |
| DEP-09-09-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-204 | NOT_APPLICABLE | ACTIVE |
| DEP-09-09-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-004 | NOT_APPLICABLE | ACTIVE |
| DEP-09-09-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-008 | NOT_APPLICABLE | ACTIVE |
| DEP-09-09-007 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-03-01 | PENDING | ACTIVE |
| DEP-09-09-008 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-03-02 | PENDING | ACTIVE |
| DEP-09-09-009 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-03-03 | PENDING | ACTIVE |
| DEP-09-09-010 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-04-01 | PENDING | ACTIVE |
| DEP-09-09-011 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-04-03 | PENDING | ACTIVE |
| DEP-09-09-012 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-09-01 | PENDING | ACTIVE |
| DEP-09-09-013 | EXECUTION / PREREQUISITE | UPSTREAM | Identified App and SWBPIPE candidates, configuration and model basis | PENDING | ACTIVE |
| DEP-09-09-014 | EXECUTION / PREREQUISITE | UPSTREAM | DEP-001 | PENDING | ACTIVE |
| DEP-09-09-015 | EXECUTION / CONSTRAINT | UPSTREAM | Person — actual machine-local external-access enablement | PENDING | ACTIVE |
| DEP-09-09-016 | EXECUTION / PREREQUISITE | UPSTREAM | Engineer — actual proposal acceptance in SWBPIPE | PENDING | ACTIVE |
| DEP-09-09-017 | EXECUTION / CONSTRAINT | UPSTREAM | OI-003 | PENDING | ACTIVE |
| DEP-09-09-018 | EXECUTION / CONSTRAINT | UPSTREAM | OI-021 | PENDING | ACTIVE |
| DEP-09-09-019 | EXECUTION / CONSTRAINT | UPSTREAM | OI-005 | PENDING | ACTIVE |
| DEP-09-09-020 | EXECUTION / HANDOVER | DOWNSTREAM | OI-003 | PENDING | ACTIVE |
| DEP-09-09-021 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-05-01 | PENDING | ACTIVE |
| DEP-09-09-022 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-04-02 | PENDING | ACTIVE |
| DEP-09-09-023 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-02-03 | PENDING | ACTIVE |
| DEP-09-09-024 | EXECUTION / CONSTRAINT | UPSTREAM | APP-V4-SWBPIPE-INTAKE-20260928-DECISION-3 | PENDING | ACTIVE |

## Lifecycle Summary

- ACTIVE: 24; RETIRED: 0. Closure (ACTIVE): NOT_APPLICABLE 6, PENDING 18, TBD 0, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-09-09; brief: run APP-V4-SCA003-20261002 `BRIEFS.md` section "DX — dependency-extract UPDATE for the 20 registers" and the DX dispatch message (SCA-V4-003, accepted by DECISION-1 and DECISION-2; register row per `_ScopeChange/SCA-V4-003_2026-10-03_1827/Amendment_Actions.csv`, sha256 `9b7c2ce8…6d1c`); selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (brief). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (located, SHA256 `983199cc22c84398000612cd95308c840ad011d302fe31ca110a5aa97e64a70d`). Companion CSVs in the same folder (Deliverables, Packages, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE deliverable target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (brief: "from the revised ScopeOfWork text only"); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/`, MEMORY.md, _CONTEXT.md, _SEMANTIC.md and _REFERENCES.md were not read as extraction sources. Where a row carries an owner-accepted register item whose content the ScopeOfWork does not restate (ledger annotations), the row says so in Notes and names its source.
- Source ScopeOfWork.md SHA256 `fafd126f1743c18a3d9e79bef6023cbb94ddab0914634e052fb0114b8468786f` (revised by SCA-V4-003 G-0909-01…04 (OUT-001, OUT-003, REQ-001, AX-006); commit 2d5e6845c5); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table (all anchor quotes verbatim after this run) before Pass 2 examined execution statements.
- Match/merge (UPDATE): all prior ACTIVE EXTRACTED rows matched by DependencyID and kept their identities; LastSeen refreshed to 2026-10-04T01:14:27+00:00. New rows take the next DEP-09-09-SEQ numbers; FirstSeen = LastSeen = run time.
- Updated in place: DEP-09-09-014 Statement (R-0909-1; host fixture set-up and reset per the accepted ledger, noted as not restated in the SoW); DEP-09-09-007 Notes (R-0909-2); DEP-09-09-010 Notes (R-0909-3; D2/D3 rulings replace the pre-ruling owner text).
- Not extracted: NR-03 (DEL-09-09 → DEL-01-02, DROP); the revised ScopeOfWork names DEL-01-02 0 times.
- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged except the two owner-accepted RequiredMaturity/SatisfactionStatus normalizations named above where they apply.
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream). The human-owned prefix of this file is byte-identical.
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, every ACTIVE quote an exact substring of the current ScopeOfWork and at most 30 words, target placement). Schema validator VALID (24 rows). enum invocations=21, id invocations=39, all_ok=True.
- `validate_decomposition_registers.py projects/chirality-app-v4/execution --families EVQ,DRB` after all 20 updates: 41 registers, 929 rows, 0 ERROR, 0 WARNING.
- Warnings: none.
- Comparison with `AMENDMENT_PACKET/ARC_EFFECT.md` and the closure recomputation were performed after extraction as separate coordinator checks and are reported in the run folder `DX/`; they were not extraction inputs.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:37:19+00:00 — TASK dependency-extract; UPDATE / CONSERVATIVE; accepted snapshot `GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` available; local validation passed; ACTIVE=20 (ANCHOR=6; EXECUTION=14), EXTERNAL=8, UNKNOWN=0, RETIRED=0. Actual inputs/acts/decisions unverified; global checks deferred.
- 2026-09-29T14:38:50+00:00 — TASK DX-3 (APP-V4-BASIS-ALIGN-20260928); UPDATE / CONSERVATIVE; SOURCE_DOCS=ScopeOfWork.md; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` available. Added 4 (DEL-05-01, DEL-04-02, DEL-02-03 UPSTREAM PREREQUISITE; DECISION-3 EXTERNAL CONSTRAINT), refreshed 2 (DEP-09-09-014, -015), retired 0. ACTIVE=24 (ANCHOR=6; EXECUTION=18), RETIRED=0. Coordination-route guard held (no DEL-09-06 or DEL-03-04 row). Mandatory local checks passed; no integrity warnings.
- 2026-10-04T01:14:27+00:00 — TASK DX (run APP-V4-SCA003-20261002); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (revised under SCA-V4-003); decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 24 ACTIVE (6 ANCHOR / 18 EXECUTION), 0 RETIRED; 0 added, 3 updated, 0 retired; warnings none; dependency closure unclaimed.
