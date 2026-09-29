# Dependencies: DEL-05-02 Host panel and shared interaction receiving

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

- **Status:** EXTRACTED (UPDATE 2026-09-29, SCA-V4-001 alignment); local checks recorded in `_run_records/dependency-extract-20260929.md`.
- **Register:** `Dependencies.csv` v3.1, 29 columns; 18 ACTIVE / 2 RETIRED; ACTIVE origin: 18 EXTRACTED.
- **Classes (ACTIVE):** 4 ANCHOR (1 parent + 2 scope + 1 objective), 14 EXECUTION.
- **Execution targets (ACTIVE):** 8 DELIVERABLE, 6 EXTERNAL; direction 1 DOWNSTREAM, 13 UPSTREAM; types 3 CONSTRAINT, 1 HANDOVER, 10 PREREQUISITE.
- **This run:** 2 added (DEL-04-02, DEL-02-03), 6 updated in place (008, 011, 012, 013, 016, 018), 2 retired (014 OI-001, 015 OI-002)

| DependencyID | Class / type | Direction | Target | Closure | Status |
|---|---|---|---|---|---|
| DEP-05-02-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-05 | NOT_APPLICABLE | ACTIVE |
| DEP-05-02-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-019 | NOT_APPLICABLE | ACTIVE |
| DEP-05-02-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-020 | NOT_APPLICABLE | ACTIVE |
| DEP-05-02-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-004 | NOT_APPLICABLE | ACTIVE |
| DEP-05-02-005 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-02-01 | PENDING | ACTIVE |
| DEP-05-02-006 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-03-01 | PENDING | ACTIVE |
| DEP-05-02-007 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-03-02 | PENDING | ACTIVE |
| DEP-05-02-008 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-04-01 | PENDING | ACTIVE |
| DEP-05-02-009 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-04-03 | PENDING | ACTIVE |
| DEP-05-02-010 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-05-01 | PENDING | ACTIVE |
| DEP-05-02-011 | EXECUTION / PREREQUISITE | UPSTREAM | DEP-001 | PENDING | ACTIVE |
| DEP-05-02-012 | EXECUTION / CONSTRAINT | UPSTREAM | OI-013 | PENDING | ACTIVE |
| DEP-05-02-013 | EXECUTION / CONSTRAINT | UPSTREAM | OI-014 | PENDING | ACTIVE |
| DEP-05-02-014 | EXECUTION / CONSTRAINT | UPSTREAM | OI-001 | PENDING | RETIRED |
| DEP-05-02-015 | EXECUTION / CONSTRAINT | UPSTREAM | OI-002 | PENDING | RETIRED |
| DEP-05-02-016 | EXECUTION / CONSTRAINT | UPSTREAM | OI-021 | PENDING | ACTIVE |
| DEP-05-02-017 | EXECUTION / PREREQUISITE | UPSTREAM | Person performing the actual human act for the VER-003 positive evidence case | PENDING | ACTIVE |
| DEP-05-02-018 | EXECUTION / HANDOVER | DOWNSTREAM | DEP-001 | PENDING | ACTIVE |
| DEP-05-02-019 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-04-02 | PENDING | ACTIVE |
| DEP-05-02-020 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-02-03 | PENDING | ACTIVE |

## Lifecycle Summary

- ACTIVE: 18; RETIRED: 2. Closure (ACTIVE): NOT_APPLICABLE 4, PENDING 14, TBD 0, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-05-02; brief: run APP-V4-BASIS-ALIGN-20260928 `BRIEFS.md` section "DX — dependency-extract UPDATE for 18 deliverables" (group DX-2, node DX-2); selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (both brief overrides). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (brief override; located, SHA256 `7434058164f9e53f146793b85c38845a562fbc9ffd46f2b97de18e8d597e5747`; post-SCA-V4-001 working surface). Companion CSVs in the same folder (Packages, Deliverables, ScopeLedger, Objectives, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (explicit brief override); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/` DRAFT files, MEMORY.md, _CONTEXT.md and _SEMANTIC.md were not read as extraction sources. `_REFERENCES.md` was read for pointer resolution only.
- Source ScopeOfWork.md SHA256 `beb9c66c38161cbb00d1040e294aa9dfd04af953f9bf539121fcda44356dc82c` (revised under SCA-V4-001, commit 340ecf341); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table before Pass 2 examined execution statements. Existing anchor TargetLocation pointers to the GROUP3 frozen snapshot are retained (the IDs are unchanged by SCA-V4-001 and resolve in both).
- Match/merge (UPDATE): 16 of 18 prior EXTRACTED rows re-observed and kept ACTIVE with their DependencyIDs; LastSeen refreshed. Updated in place: DEP-05-02-008 (SourceRef/Notes: DEL-04-01 carries the first-increment OI-001/OI-002 rulings, consumed via REQ-003/TBD-004); DEP-05-02-011 (SourceRef line; Notes: revised TBD-003 evidence items SQ-01/SQ-02 and host-join deferral per DECISION-3); DEP-05-02-012/013 (SourceRef line numbers); DEP-05-02-016 (TargetRefID OQ-11 -> OI-021, as the revised paragraph states "tracked as OI-021"; legacy value kept in Notes); DEP-05-02-018 (Notes only).
- Retired (retired_by=source_revised, never deleted): DEP-05-02-014 OI-001 and DEP-05-02-015 OI-002 constraints. Revised TBD-004/TBD-005 record both as ruled for the first increment (APP-V4-FIRST-INCREMENT-20260928-DECISION-1 D2/D3); their quoted points of need no longer appear. The adopted result is consumed through DEL-04-01 (DEP-05-02-008); residual operation-specific additions are carried by DEP-05-02-016 (OI-021).
- Added: DEP-05-02-019 UPSTREAM PREREQUISITE DEL-04-02 (autonomy-grant display states and active scope) and DEP-05-02-020 UPSTREAM PREREQUISITE DEL-02-03 (current-phase checkpoint recording meanings; governance-phase hold-support values and hold-machine meanings). Both are explicit CLM-002 consumption statements; PREREQUISITE follows this register's existing typing of CLM-002 consumed definitions.
- GUARD (brief): TBD-003 names DEL-09-06 `Design/RELAY_QUESTIONS_SWBPIPE.md` as "a coordination route, not an input this deliverable consumes" and `Design/RELAY_ANSWERS_SWBPIPE.md` as current-state answers. No input or prerequisite row on DEL-09-06 was extracted; the relay files were not read. The DOWNSTREAM HANDOVER row DEP-05-02-018 targets the external SWBPIPE owner (DEP-001), not DEL-09-06.
- Considered, not extracted: the SWB default proposal mode in TBD-005 is a stated first-increment fact, not an input; DECISION-3/DECISION-4 and FIRST-INCREMENT DECISION-1 are decided sources.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged (execution rows PENDING).
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream).
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, verbatim quotes <=30 words, non-placeholder SourceRefs, target placement, no duplicate typed-target keys); target IDs unresolved: none. Schema validator PASS. enum invocations=22, id invocations=36, all_ok=True
- Optional `validate_decomposition_registers.py` whole-execution EVQ/DRB scan not run (the brief bounds reads to the deliverable and decomposition); the equivalent local EVQ-003/EVQ-004/DRB-006 conditions were checked and are absent.
- Warnings: none.
- Coordinator comparison against DAG_PREP proposed rows and REGISTER_CHANGES.md was performed after extraction as a separate check and is reported in the run-folder return `DX/DX-2_DEL-05-02.md`; it was not an extraction input.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:27:25Z — TASK `/root/renewal_research_strategy/dep_del_05_02`; UPDATE / CONSERVATIVE; decomposition `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` available and identifiers resolved; 18 ACTIVE (4 ANCHOR, 14 EXECUTION), 0 RETIRED; no structural warnings; actual inputs and point-of-need decisions remain pending. Local checks passed.
- 2026-09-29T14:41:27+00:00 — TASK DX-2 (run APP-V4-BASIS-ALIGN-20260928); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 18 ACTIVE (4 ANCHOR / 14 EXECUTION), 2 RETIRED; 2 added (DEL-04-02, DEL-02-03), 6 updated in place (008, 011, 012, 013, 016, 018), 2 retired (014 OI-001, 015 OI-002); warnings none; dependency closure unclaimed.
