# Dependencies: DEL-01-03 Native plans, tools and delegation views

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
- **Register:** `Dependencies.csv` v3.1, 29 columns; 22 ACTIVE / 0 RETIRED; ACTIVE origin: 22 EXTRACTED.
- **Classes (ACTIVE):** 10 ANCHOR (1 parent + 7 scope + 2 objective), 12 EXECUTION.
- **Execution targets (ACTIVE):** 7 DELIVERABLE, 4 EXTERNAL, 1 PACKAGE; direction 6 DOWNSTREAM, 6 UPSTREAM; types 4 CONSTRAINT, 5 HANDOVER, 1 INTERFACE, 2 PREREQUISITE.
- **This run:** 4 added (019, 020, 021, 022), 2 updated in place (011, 017), 0 retired (none); every other ACTIVE row re-observed (LastSeen only).

| DependencyID | Class / type | Direction | Target | Closure | Status |
|---|---|---|---|---|---|
| DEP-01-03-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-01 | NOT_APPLICABLE | ACTIVE |
| DEP-01-03-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-001 | NOT_APPLICABLE | ACTIVE |
| DEP-01-03-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-003 | NOT_APPLICABLE | ACTIVE |
| DEP-01-03-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-004 | NOT_APPLICABLE | ACTIVE |
| DEP-01-03-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-006 | NOT_APPLICABLE | ACTIVE |
| DEP-01-03-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-014 | NOT_APPLICABLE | ACTIVE |
| DEP-01-03-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-128 | NOT_APPLICABLE | ACTIVE |
| DEP-01-03-008 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-129 | NOT_APPLICABLE | ACTIVE |
| DEP-01-03-009 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-001 | NOT_APPLICABLE | ACTIVE |
| DEP-01-03-010 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-002 | NOT_APPLICABLE | ACTIVE |
| DEP-01-03-011 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-01-01 | TBD | ACTIVE |
| DEP-01-03-012 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-01-02 | TBD | ACTIVE |
| DEP-01-03-013 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-02 | TBD | ACTIVE |
| DEP-01-03-014 | EXECUTION / HANDOVER | DOWNSTREAM | PKG-06 | TBD | ACTIVE |
| DEP-01-03-015 | EXECUTION / CONSTRAINT | UPSTREAM | OI-008 | TBD | ACTIVE |
| DEP-01-03-016 | EXECUTION / CONSTRAINT | UPSTREAM | OI-014 | TBD | ACTIVE |
| DEP-01-03-017 | EXECUTION / CONSTRAINT | UPSTREAM | OI-001;OI-002 | TBD | ACTIVE |
| DEP-01-03-018 | EXECUTION / CONSTRAINT | UPSTREAM | OI-006 | TBD | ACTIVE |
| DEP-01-03-019 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-06-01 | TBD | ACTIVE |
| DEP-01-03-020 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-02 | TBD | ACTIVE |
| DEP-01-03-021 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-05 | TBD | ACTIVE |
| DEP-01-03-022 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-01-04 | TBD | ACTIVE |

## Lifecycle Summary

- ACTIVE: 22; RETIRED: 0. Closure (ACTIVE): NOT_APPLICABLE 10, PENDING 0, TBD 12, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-01-03; brief: run APP-V4-SCA003-20261002 `BRIEFS.md` section "DX — dependency-extract UPDATE for the 20 registers" and the DX dispatch message (SCA-V4-003, accepted by DECISION-1 and DECISION-2; register row per `_ScopeChange/SCA-V4-003_2026-10-03_1827/Amendment_Actions.csv`, sha256 `9b7c2ce8…6d1c`); selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (brief). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (located, SHA256 `983199cc22c84398000612cd95308c840ad011d302fe31ca110a5aa97e64a70d`). Companion CSVs in the same folder (Deliverables, Packages, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE deliverable target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (brief: "from the revised ScopeOfWork text only"); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/`, MEMORY.md, _CONTEXT.md, _SEMANTIC.md and _REFERENCES.md were not read as extraction sources. Where a row carries an owner-accepted register item whose content the ScopeOfWork does not restate (ledger annotations), the row says so in Notes and names its source.
- Source ScopeOfWork.md SHA256 `0056ec198e855080da740e2fb72a3e0a37fcd304c58cca537d4ad56a11c46069` (revised by SCA-V4-003 G-0103-01…11 (10 definitions and AX-004); commit 2d5e6845c5); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table (all anchor quotes verbatim after this run) before Pass 2 examined execution statements.
- Match/merge (UPDATE): all prior ACTIVE EXTRACTED rows matched by DependencyID and kept their identities; LastSeen refreshed to 2026-10-04T01:14:27+00:00. New rows take the next DEP-01-03-SEQ numbers; FirstSeen = LastSeen = run time.
- Added 4 DOWNSTREAM rows from the new CLM-003 receivers sentence: DEL-06-01, DEL-09-02, DEL-09-05 (R3-01-03-a…c, existing admitted arcs) and DEL-01-04 (R3-01-03-d, mirror of the new admitted arc NR-05). The package row DEP-01-03-014 (PKG-06) stays.
- Updated in place: DEP-01-03-017 re-quoted to the revised TBD-003 residue (R3-01-03-e; OI-002 and OI-001 recorded as ruled for this scope by D3/D2 and open beyond it; kept as one combined row and noted, not split or retired); DEP-01-03-011 Notes (R3-01-03-f, D4 pointer).
- Not extracted: any UPSTREAM row to DEL-01-04 or DEL-06-01 (R17-10). Pre-existing, not changed by this run: 14 rows carry an absolute TargetLocation under `/Users/ryan/.codex/worktrees/077c/...` (for example DEP-01-03-011); repairing it is outside this brief and is returned to the coordinator.
- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged except the two owner-accepted RequiredMaturity/SatisfactionStatus normalizations named above where they apply.
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream). The human-owned prefix of this file is byte-identical.
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, every ACTIVE quote an exact substring of the current ScopeOfWork and at most 30 words, target placement). Schema validator VALID (22 rows). enum invocations=23, id invocations=34, all_ok=True.
- `validate_decomposition_registers.py projects/chirality-app-v4/execution --families EVQ,DRB` after all 20 updates: 41 registers, 929 rows, 0 ERROR, 0 WARNING.
- Warnings: none.
- Comparison with `AMENDMENT_PACKET/ARC_EFFECT.md` and the closure recomputation were performed after extraction as separate coordinator checks and are reported in the run folder `DX/`; they were not extraction inputs.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:13:34+00:00 — TASK executed UPDATE / CONSERVATIVE using the accepted Group3 canonical decomposition path above: 18 ACTIVE (10 ANCHOR, 8 EXECUTION), 0 RETIRED; no parent, missing-decomposition or declaration warnings. Point-of-need decision receipts and technical inputs remain unverified.
- 2026-10-04T01:14:27+00:00 — TASK DX (run APP-V4-SCA003-20261002); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (revised under SCA-V4-003); decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 22 ACTIVE (10 ANCHOR / 12 EXECUTION), 0 RETIRED; 4 added, 2 updated, 0 retired; warnings none; dependency closure unclaimed.
