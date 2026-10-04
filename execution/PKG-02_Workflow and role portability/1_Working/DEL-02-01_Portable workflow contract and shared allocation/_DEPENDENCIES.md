# Dependencies: DEL-02-01 Portable workflow contract and shared allocation

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
- **Register:** `Dependencies.csv` v3.1, 29 columns; 40 ACTIVE / 0 RETIRED; ACTIVE origin: 40 EXTRACTED.
- **Classes (ACTIVE):** 16 ANCHOR (1 parent + 12 scope + 3 objective), 24 EXECUTION.
- **Execution targets (ACTIVE):** 20 DELIVERABLE, 4 EXTERNAL; direction 12 DOWNSTREAM, 12 UPSTREAM; types 3 CONSTRAINT, 11 HANDOVER, 10 INTERFACE.
- **This run:** 11 added (030, 031, 032, 033, 034, 035, 036, 037, 038, 039, 040), 2 updated in place (025, 027), 0 retired (none); every other ACTIVE row re-observed (LastSeen only).

| DependencyID | Class / type | Direction | Target | Closure | Status |
|---|---|---|---|---|---|
| DEP-02-01-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-02 | NOT_APPLICABLE | ACTIVE |
| DEP-02-01-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-021 | NOT_APPLICABLE | ACTIVE |
| DEP-02-01-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-022 | NOT_APPLICABLE | ACTIVE |
| DEP-02-01-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-037 | NOT_APPLICABLE | ACTIVE |
| DEP-02-01-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-038 | NOT_APPLICABLE | ACTIVE |
| DEP-02-01-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-039 | NOT_APPLICABLE | ACTIVE |
| DEP-02-01-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-042 | NOT_APPLICABLE | ACTIVE |
| DEP-02-01-008 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-043 | NOT_APPLICABLE | ACTIVE |
| DEP-02-01-009 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-044 | NOT_APPLICABLE | ACTIVE |
| DEP-02-01-010 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-045 | NOT_APPLICABLE | ACTIVE |
| DEP-02-01-011 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-145 | NOT_APPLICABLE | ACTIVE |
| DEP-02-01-012 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-146 | NOT_APPLICABLE | ACTIVE |
| DEP-02-01-013 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-147 | NOT_APPLICABLE | ACTIVE |
| DEP-02-01-014 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-003 | NOT_APPLICABLE | ACTIVE |
| DEP-02-01-015 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-004 | NOT_APPLICABLE | ACTIVE |
| DEP-02-01-016 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-005 | NOT_APPLICABLE | ACTIVE |
| DEP-02-01-017 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-01 | PENDING | ACTIVE |
| DEP-02-01-018 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-01 | PENDING | ACTIVE |
| DEP-02-01-019 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-03 | PENDING | ACTIVE |
| DEP-02-01-020 | EXECUTION / INTERFACE | UPSTREAM | DEL-05-01 | PENDING | ACTIVE |
| DEP-02-01-021 | EXECUTION / INTERFACE | UPSTREAM | DEL-05-02 | PENDING | ACTIVE |
| DEP-02-01-022 | EXECUTION / INTERFACE | UPSTREAM | SWBPIPE | PENDING | ACTIVE |
| DEP-02-01-023 | EXECUTION / CONSTRAINT | UPSTREAM | OI-014 | PENDING | ACTIVE |
| DEP-02-01-024 | EXECUTION / CONSTRAINT | UPSTREAM | OI-013 | PENDING | ACTIVE |
| DEP-02-01-025 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-01 | PENDING | ACTIVE |
| DEP-02-01-026 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-03 | PENDING | ACTIVE |
| DEP-02-01-027 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-03-03 | PENDING | ACTIVE |
| DEP-02-01-028 | EXECUTION / CONSTRAINT | UPSTREAM | Owner — governance-phase enforced-checkpoint decision (TBD-004) | PENDING | ACTIVE |
| DEP-02-01-029 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-02 | PENDING | ACTIVE |
| DEP-02-01-030 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-02 | PENDING | ACTIVE |
| DEP-02-01-031 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-03 | PENDING | ACTIVE |
| DEP-02-01-032 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-04 | PENDING | ACTIVE |
| DEP-02-01-033 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-02 | PENDING | ACTIVE |
| DEP-02-01-034 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-04 | PENDING | ACTIVE |
| DEP-02-01-035 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-05-01 | PENDING | ACTIVE |
| DEP-02-01-036 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-05-02 | PENDING | ACTIVE |
| DEP-02-01-037 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-08-02 | PENDING | ACTIVE |
| DEP-02-01-038 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-02 | PENDING | ACTIVE |
| DEP-02-01-039 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-06 | PENDING | ACTIVE |
| DEP-02-01-040 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-10-03 | PENDING | ACTIVE |

## Lifecycle Summary

- ACTIVE: 40; RETIRED: 0. Closure (ACTIVE): NOT_APPLICABLE 16, PENDING 24, TBD 0, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-02-01; brief: run APP-V4-SCA003-20261002 `BRIEFS.md` section "DX — dependency-extract UPDATE for the 20 registers" and the DX dispatch message (SCA-V4-003, accepted by DECISION-1 and DECISION-2; register row per `_ScopeChange/SCA-V4-003_2026-10-03_1827/Amendment_Actions.csv`, sha256 `9b7c2ce8…6d1c`); selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (brief). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (located, SHA256 `983199cc22c84398000612cd95308c840ad011d302fe31ca110a5aa97e64a70d`). Companion CSVs in the same folder (Deliverables, Packages, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE deliverable target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (brief: "from the revised ScopeOfWork text only"); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/`, MEMORY.md, _CONTEXT.md, _SEMANTIC.md and _REFERENCES.md were not read as extraction sources. Where a row carries an owner-accepted register item whose content the ScopeOfWork does not restate (ledger annotations), the row says so in Notes and names its source.
- Source ScopeOfWork.md SHA256 `9479fc882decd3721a346ff5723751091db9965a65d6078baf6562ed1779bd49` (revised by SCA-V4-003 G-0201-01…03 (CLM-002, AX-007); commit 2d5e6845c5); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table (all anchor quotes verbatim after this run) before Pass 2 examined execution statements.
- Match/merge (UPDATE): all prior ACTIVE EXTRACTED rows matched by DependencyID and kept their identities; LastSeen refreshed to 2026-10-04T01:14:27+00:00. New rows take the next DEP-02-01-SEQ numbers; FirstSeen = LastSeen = run time.
- Added 11 DOWNSTREAM HANDOVER rows from the new CLM-002 receivers sentence (DEL-02-02, 02-03, 02-04, 03-02, 03-04, 05-01, 05-02, 08-02, 09-02, 09-06, 10-03): R2-02-01-a…f (6) and RP1-MX-0201 (5), each mirroring an existing consumer row on an existing arc.
- Updated in place: DEP-02-01-025 Statement (R2-02-01-g; inventory, capability-group meanings, availability signals); DEP-02-01-027 RequiredMaturity TBD → INITIALIZED and SatisfactionStatus TBD → PENDING (R2-02-01-h, local normalization).
- No receivers-sentence target is left unextracted.
- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged except the two owner-accepted RequiredMaturity/SatisfactionStatus normalizations named above where they apply.
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream). The human-owned prefix of this file is byte-identical.
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, every ACTIVE quote an exact substring of the current ScopeOfWork and at most 30 words, target placement). Schema validator VALID (40 rows). enum invocations=23, id invocations=65, all_ok=True.
- `validate_decomposition_registers.py projects/chirality-app-v4/execution --families EVQ,DRB` after all 20 updates: 41 registers, 929 rows, 0 ERROR, 0 WARNING.
- Warnings: none.
- Comparison with `AMENDMENT_PACKET/ARC_EFFECT.md` and the closure recomputation were performed after extraction as separate coordinator checks and are reported in the run folder `DX/`; they were not extraction inputs.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:09:04+00:00 — TASK `/root/renewal_research_strategy/dep_del_02_01`; UPDATE / CONSERVATIVE; accepted decomposition `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` resolved; 24 ACTIVE (16 ANCHOR / 8 EXECUTION), 0 RETIRED; warnings 0; dependency closure unclaimed.
- 2026-09-29T14:35:26+00:00 — TASK DX-2 (run APP-V4-BASIS-ALIGN-20260928); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 28 ACTIVE (16 ANCHOR / 12 EXECUTION), 0 RETIRED; 4 added (DEL-01-01, DEL-02-03, DEL-03-03, TBD-004 owner decision), 2 updated in place (017, 018), 0 retired; warnings none; dependency closure unclaimed.
- 2026-09-30T02:33:47+00:00 — TASK DX (run APP-V4-SCA002-20260929); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 29 ACTIVE (16 ANCHOR / 13 EXECUTION), 0 RETIRED; 1 added (DEL-03-02), 0 updated, 0 retired; warnings none; dependency closure unclaimed.
- 2026-10-04T01:14:27+00:00 — TASK DX (run APP-V4-SCA003-20261002); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (revised under SCA-V4-003); decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 40 ACTIVE (16 ANCHOR / 24 EXECUTION), 0 RETIRED; 11 added, 2 updated, 0 retired; warnings none; dependency closure unclaimed.
