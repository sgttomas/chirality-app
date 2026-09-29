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

- **Status:** EXTRACTED (UPDATE 2026-09-29, SCA-V4-001 alignment); local checks recorded in `_run_records/dependency-extract-20260929.md`.
- **Register:** `Dependencies.csv` v3.1, 29 columns; 28 ACTIVE / 0 RETIRED; ACTIVE origin: 28 EXTRACTED.
- **Classes (ACTIVE):** 16 ANCHOR (1 parent + 12 scope + 3 objective), 12 EXECUTION.
- **Execution targets (ACTIVE):** 8 DELIVERABLE, 4 EXTERNAL; direction 1 DOWNSTREAM, 11 UPSTREAM; types 3 CONSTRAINT, 9 INTERFACE.
- **This run:** 4 added (DEL-01-01, DEL-02-03, DEL-03-03, TBD-004 owner decision), 2 updated in place (017, 018), 0 retired

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
| DEP-02-01-027 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-03-03 | TBD | ACTIVE |
| DEP-02-01-028 | EXECUTION / CONSTRAINT | UPSTREAM | Owner — governance-phase enforced-checkpoint decision (TBD-004) | PENDING | ACTIVE |

## Lifecycle Summary

- ACTIVE: 28; RETIRED: 0. Closure (ACTIVE): NOT_APPLICABLE 16, PENDING 11, TBD 1, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-02-01; brief: run APP-V4-BASIS-ALIGN-20260928 `BRIEFS.md` section "DX — dependency-extract UPDATE for 18 deliverables" (group DX-2, node DX-2); selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (both brief overrides). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (brief override; located, SHA256 `7434058164f9e53f146793b85c38845a562fbc9ffd46f2b97de18e8d597e5747`; post-SCA-V4-001 working surface). Companion CSVs in the same folder (Packages, Deliverables, ScopeLedger, Objectives, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (explicit brief override); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/` DRAFT files, MEMORY.md, _CONTEXT.md and _SEMANTIC.md were not read as extraction sources. `_REFERENCES.md` was read for pointer resolution only.
- Source ScopeOfWork.md SHA256 `6ccc860ba48aee9392fbf90fef323577c7599655164442e6f3fb0b78fe36f0dc` (revised under SCA-V4-001, commit 340ecf341); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table before Pass 2 examined execution statements. Existing anchor TargetLocation pointers to the GROUP3 frozen snapshot are retained (the IDs are unchanged by SCA-V4-001 and resolve in both).
- Match/merge (UPDATE): all 24 prior EXTRACTED rows re-observed with verbatim evidence and kept ACTIVE with their DependencyIDs; LastSeen refreshed. Updated in place: DEP-02-01-017 (SourceRef/Notes: revised REQ-002 names DEL-03-01 directly) and DEP-02-01-018 (Statement/SourceRef/Notes: DEL-04-01 now carries the first-increment OI-001/OI-002 rulings, APP-V4-FIRST-INCREMENT-20260928-DECISION-1 D2/D3; operation-specific additions with OI-021). No row retired.
- Added: DEP-02-01-025 UPSTREAM INTERFACE DEL-01-01 (REQ-002 harness-capability meaning); DEP-02-01-026 UPSTREAM INTERFACE DEL-02-03 (TBD-004 current-phase statement and governance-phase hold-support values); DEP-02-01-027 DOWNSTREAM INTERFACE DEL-03-03 (CLM-002 receipt of declared checkpoint constraints, governance phase; IMPLICIT/MEDIUM because the clause does not name the producer); DEP-02-01-028 UPSTREAM CONSTRAINT EXTERNAL owner decision on enforced checkpoints (TBD-004 Owner/Point of need; governance-phase hold claims only).
- Considered, not extracted (CONSERVATIVE, information flow only): DEL-03-02 appears in CLM-002/REQ-006 as owner of proposal/outcome semantics and the governance-phase governing checkpoint constraint, with no statement that this contract consumes or supplies it; OI-021 (operation-specific reserved additions) is named in TBD-003 but TBD-003 states the open choices are not used to defer independent definition; OI-018 remains a mechanism matter with its owners; DEL-02-02/DEL-02-04 appear only in ownership/exclusion lists.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged (upstream PENDING; new downstream TBD).
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream).
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, verbatim quotes <=30 words, non-placeholder SourceRefs, target placement, no duplicate typed-target keys); target IDs unresolved: none. Schema validator PASS. enum invocations=23, id invocations=57, all_ok=True
- Optional `validate_decomposition_registers.py` whole-execution EVQ/DRB scan not run (the brief bounds reads to the deliverable and decomposition); the equivalent local EVQ-003/EVQ-004/DRB-006 conditions were checked and are absent.
- Warnings: none.
- Coordinator comparison against DAG_PREP proposed rows and REGISTER_CHANGES.md was performed after extraction as a separate check and is reported in the run-folder return `DX/DX-2_DEL-02-01.md`; it was not an extraction input.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:09:04+00:00 — TASK `/root/renewal_research_strategy/dep_del_02_01`; UPDATE / CONSERVATIVE; accepted decomposition `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` resolved; 24 ACTIVE (16 ANCHOR / 8 EXECUTION), 0 RETIRED; warnings 0; dependency closure unclaimed.
- 2026-09-29T14:35:26+00:00 — TASK DX-2 (run APP-V4-BASIS-ALIGN-20260928); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 28 ACTIVE (16 ANCHOR / 12 EXECUTION), 0 RETIRED; 4 added (DEL-01-01, DEL-02-03, DEL-03-03, TBD-004 owner decision), 2 updated in place (017, 018), 0 retired; warnings none; dependency closure unclaimed.
