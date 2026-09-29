# Dependencies: DEL-05-01 Minimal-loop and model receiving contract

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
- **Register:** `Dependencies.csv` v3.1, 29 columns; 25 ACTIVE / 0 RETIRED; ACTIVE origin: 25 EXTRACTED.
- **Classes (ACTIVE):** 13 ANCHOR (1 parent + 11 scope + 1 objective), 12 EXECUTION.
- **Execution targets (ACTIVE):** 8 DELIVERABLE, 3 EXTERNAL, 1 UNKNOWN; direction 12 UPSTREAM; types 2 CONSTRAINT, 8 INTERFACE, 2 PREREQUISITE.
- **This run:** 1 added (DEL-04-02), 9 updated in place (002, 003, 004, 006, 007, 017, 018, 021, 024), 0 retired

| DependencyID | Class / type | Direction | Target | Closure | Status |
|---|---|---|---|---|---|
| DEP-05-01-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-05 | NOT_APPLICABLE | ACTIVE |
| DEP-05-01-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-015 | NOT_APPLICABLE | ACTIVE |
| DEP-05-01-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-016 | NOT_APPLICABLE | ACTIVE |
| DEP-05-01-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-017 | NOT_APPLICABLE | ACTIVE |
| DEP-05-01-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-136 | NOT_APPLICABLE | ACTIVE |
| DEP-05-01-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-137 | NOT_APPLICABLE | ACTIVE |
| DEP-05-01-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-138 | NOT_APPLICABLE | ACTIVE |
| DEP-05-01-008 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-139 | NOT_APPLICABLE | ACTIVE |
| DEP-05-01-009 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-140 | NOT_APPLICABLE | ACTIVE |
| DEP-05-01-010 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-141 | NOT_APPLICABLE | ACTIVE |
| DEP-05-01-011 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-142 | NOT_APPLICABLE | ACTIVE |
| DEP-05-01-012 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-144 | NOT_APPLICABLE | ACTIVE |
| DEP-05-01-013 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-004 | NOT_APPLICABLE | ACTIVE |
| DEP-05-01-014 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-01 | PENDING | ACTIVE |
| DEP-05-01-015 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-02 | PENDING | ACTIVE |
| DEP-05-01-016 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-01 | PENDING | ACTIVE |
| DEP-05-01-017 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-03 | PENDING | ACTIVE |
| DEP-05-01-018 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-01 | PENDING | ACTIVE |
| DEP-05-01-019 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-03 | PENDING | ACTIVE |
| DEP-05-01-020 | EXECUTION / INTERFACE | UPSTREAM | DEL-05-02 | PENDING | ACTIVE |
| DEP-05-01-021 | EXECUTION / PREREQUISITE | UPSTREAM | DEP-001 | PENDING | ACTIVE |
| DEP-05-01-022 | EXECUTION / CONSTRAINT | UPSTREAM | OI-013 | PENDING | ACTIVE |
| DEP-05-01-023 | EXECUTION / CONSTRAINT | UPSTREAM | OI-014 | PENDING | ACTIVE |
| DEP-05-01-024 | EXECUTION / PREREQUISITE | UPSTREAM | Adopted host model-interface and detailed protocol/fixture basis | PENDING | ACTIVE |
| DEP-05-01-025 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-02 | PENDING | ACTIVE |

## Lifecycle Summary

- ACTIVE: 25; RETIRED: 0. Closure (ACTIVE): NOT_APPLICABLE 13, PENDING 12, TBD 0, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-05-01; brief: run APP-V4-BASIS-ALIGN-20260928 `BRIEFS.md` section "DX — dependency-extract UPDATE for 18 deliverables" (group DX-2, node DX-2); selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (both brief overrides). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (brief override; located, SHA256 `7434058164f9e53f146793b85c38845a562fbc9ffd46f2b97de18e8d597e5747`; post-SCA-V4-001 working surface). Companion CSVs in the same folder (Packages, Deliverables, ScopeLedger, Objectives, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (explicit brief override); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/` DRAFT files, MEMORY.md, _CONTEXT.md and _SEMANTIC.md were not read as extraction sources. `_REFERENCES.md` was read for pointer resolution only.
- Source ScopeOfWork.md SHA256 `9b2379a14e2c9da4310f62e72d83a6e7506ef37f70c4a38b41d76908bca985ed` (revised under SCA-V4-001, commit 340ecf341); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table before Pass 2 examined execution statements. Existing anchor TargetLocation pointers to the GROUP3 frozen snapshot are retained (the IDs are unchanged by SCA-V4-001 and resolve in both).
- Match/merge (UPDATE): all 24 prior EXTRACTED rows re-observed and kept ACTIVE with their DependencyIDs; LastSeen refreshed. Updated in place: anchors DEP-05-01-002/003/004/006/007 (SOW-015/016/017/137/138 amended by SCA-V4-001; TargetName/TargetLocation now cite the current ScopeLedger rows); DEP-05-01-017 (Statement/SourceRef: revised REQ-006 current-phase observation and governance-phase hold machine/hold-support values of DEL-02-03); DEP-05-01-018 (Notes: CLM-004 first-increment D2/D3); DEP-05-01-021 (EvidenceQuote/Statement: revised VER-002 destination record and credential separation; Notes: host joins deferred per DECISION-3); DEP-05-01-024 (Notes: SQ-29 answer keeps the model-interface basis UNKNOWN).
- Added: DEP-05-01-025 UPSTREAM INTERFACE DEL-04-02 (CLM-002 explicitly consumes the autonomy-grant display states and standing exchange as the grant in force on each dispatch). No row retired.
- GUARD (brief): TBD-003 names DEL-09-06 `Design/RELAY_QUESTIONS_SWBPIPE.md` and `Design/RELAY_ANSWERS_SWBPIPE.md` as "a coordination route, not an input this deliverable consumes". No input or prerequisite row on DEL-09-06 was extracted; the pointer is recorded only in DEP-05-01-021 Notes. The relay files were not read.
- Considered, not extracted (CONSERVATIVE, information flow only): the REQ-001 rule that an MCP server is allowed only under the stateless MCP revision 2026-07-28 is a stated contract content rule, not an input this deliverable must receive; organization-locked allow lists and enforced sandboxing are named as a later governance phase without an owner or point of need; APP-V4-SWBPIPE-INTAKE-20260928-DECISION-3/4/5 and APP-V4-FIRST-INCREMENT-20260928-DECISION-1 are decided sources, not pending inputs; the UI-SUCCESSOR resumption qualifies DEP-001 timing (row 021).
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged (all execution rows PENDING).
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream).
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, verbatim quotes <=30 words, non-placeholder SourceRefs, target placement, no duplicate typed-target keys); target IDs unresolved: none. Schema validator PASS. enum invocations=21, id invocations=50, all_ok=True
- Optional `validate_decomposition_registers.py` whole-execution EVQ/DRB scan not run (the brief bounds reads to the deliverable and decomposition); the equivalent local EVQ-003/EVQ-004/DRB-006 conditions were checked and are absent.
- Warnings: none.
- Coordinator comparison against DAG_PREP proposed rows and REGISTER_CHANGES.md was performed after extraction as a separate check and is reported in the run-folder return `DX/DX-2_DEL-05-01.md`; it was not an extraction input.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:11:20.190351+00:00 — TASK native child `/root/renewal_research_strategy/dep_del_05_01`; dependency-extract UPDATE / CONSERVATIVE; explicit accepted decomposition available; 24 ACTIVE (13 ANCHOR / 11 EXECUTION), 0 RETIRED; one parent; source/declared sections preserved; unresolved model-interface basis and owner/external conditions retained.
- 2026-09-29T14:40:03+00:00 — TASK DX-2 (run APP-V4-BASIS-ALIGN-20260928); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 25 ACTIVE (13 ANCHOR / 12 EXECUTION), 0 RETIRED; 1 added (DEL-04-02), 9 updated in place (002, 003, 004, 006, 007, 017, 018, 021, 024), 0 retired; warnings none; dependency closure unclaimed.
