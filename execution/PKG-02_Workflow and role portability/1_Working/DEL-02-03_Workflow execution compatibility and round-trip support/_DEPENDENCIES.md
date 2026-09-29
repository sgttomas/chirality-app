# Dependencies: DEL-02-03 Workflow execution compatibility and round-trip support

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
- **Register:** `Dependencies.csv` v3.1, 29 columns; 22 ACTIVE / 2 RETIRED; ACTIVE origin: 22 EXTRACTED.
- **Classes (ACTIVE):** 8 ANCHOR (1 parent + 5 scope + 2 objective), 14 EXECUTION.
- **Execution targets (ACTIVE):** 8 DELIVERABLE, 6 EXTERNAL; direction 1 DOWNSTREAM, 13 UPSTREAM; types 5 CONSTRAINT, 1 HANDOVER, 7 INTERFACE, 1 PREREQUISITE.
- **This run:** 3 added (DEL-05-01, DEL-01-01, TBD-006 owner decision), 2 updated in place (003, 012), 2 retired (015 OI-001, 016 OI-002)

| DependencyID | Class / type | Direction | Target | Closure | Status |
|---|---|---|---|---|---|
| DEP-02-03-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-02 | NOT_APPLICABLE | ACTIVE |
| DEP-02-03-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-051 | NOT_APPLICABLE | ACTIVE |
| DEP-02-03-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-052 | NOT_APPLICABLE | ACTIVE |
| DEP-02-03-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-053 | NOT_APPLICABLE | ACTIVE |
| DEP-02-03-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-054 | NOT_APPLICABLE | ACTIVE |
| DEP-02-03-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-055 | NOT_APPLICABLE | ACTIVE |
| DEP-02-03-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-003 | NOT_APPLICABLE | ACTIVE |
| DEP-02-03-008 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-005 | NOT_APPLICABLE | ACTIVE |
| DEP-02-03-009 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-01 | TBD | ACTIVE |
| DEP-02-03-010 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-02 | TBD | ACTIVE |
| DEP-02-03-011 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-01 | TBD | ACTIVE |
| DEP-02-03-012 | EXECUTION / CONSTRAINT | UPSTREAM | DEL-04-01 | TBD | ACTIVE |
| DEP-02-03-013 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-03 | TBD | ACTIVE |
| DEP-02-03-014 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-06 | TBD | ACTIVE |
| DEP-02-03-015 | EXECUTION / CONSTRAINT | UPSTREAM | OI-001 | TBD | RETIRED |
| DEP-02-03-016 | EXECUTION / CONSTRAINT | UPSTREAM | OI-002 | TBD | RETIRED |
| DEP-02-03-017 | EXECUTION / CONSTRAINT | UPSTREAM | OI-013 | TBD | ACTIVE |
| DEP-02-03-018 | EXECUTION / CONSTRAINT | UPSTREAM | OI-014 | TBD | ACTIVE |
| DEP-02-03-019 | EXECUTION / CONSTRAINT | UPSTREAM | OI-021 | TBD | ACTIVE |
| DEP-02-03-020 | EXECUTION / INTERFACE | UPSTREAM | DEP-001 | TBD | ACTIVE |
| DEP-02-03-021 | EXECUTION / PREREQUISITE | UPSTREAM | Human checkpoint actor and separate recorder — positive fixture evidence | TBD | ACTIVE |
| DEP-02-03-022 | EXECUTION / INTERFACE | UPSTREAM | DEL-05-01 | TBD | ACTIVE |
| DEP-02-03-023 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-01 | TBD | ACTIVE |
| DEP-02-03-024 | EXECUTION / CONSTRAINT | UPSTREAM | Owner — governance-phase enforced-checkpoint decision (TBD-006) | TBD | ACTIVE |

## Lifecycle Summary

- ACTIVE: 22; RETIRED: 2. Closure (ACTIVE): NOT_APPLICABLE 8, PENDING 0, TBD 14, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-02-03; brief: run APP-V4-BASIS-ALIGN-20260928 `BRIEFS.md` section "DX — dependency-extract UPDATE for 18 deliverables" (group DX-2, node DX-2); selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (both brief overrides). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (brief override; located, SHA256 `7434058164f9e53f146793b85c38845a562fbc9ffd46f2b97de18e8d597e5747`; post-SCA-V4-001 working surface). Companion CSVs in the same folder (Packages, Deliverables, ScopeLedger, Objectives, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (explicit brief override); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/` DRAFT files, MEMORY.md, _CONTEXT.md and _SEMANTIC.md were not read as extraction sources. `_REFERENCES.md` was read for pointer resolution only.
- Source ScopeOfWork.md SHA256 `a4ffcd8711ad0ee50d9ca6876d0b19972f9f3ba9a7a129578068c4a918c24c0e` (revised under SCA-V4-001, commit 340ecf341); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table before Pass 2 examined execution statements. Existing anchor TargetLocation pointers to the GROUP3 frozen snapshot are retained (the IDs are unchanged by SCA-V4-001 and resolve in both).
- Match/merge (UPDATE): 19 of 21 prior EXTRACTED rows re-observed and kept ACTIVE with their DependencyIDs; LastSeen refreshed. Updated in place: DEP-02-03-003 (SOW-052 amended by SCA-V4-001: EvidenceQuote, TargetName and TargetLocation now cite the current ScopeLedger row) and DEP-02-03-012 (SourceRef/Notes: DEL-04-01 carries the first-increment OI-001/OI-002 rulings).
- Retired (retired_by=source_revised, never deleted): DEP-02-03-015 OI-001 and DEP-02-03-016 OI-002 owner-decision constraints. Revised TBD-001/TBD-002 record both as ruled for the first increment (APP-V4-FIRST-INCREMENT-20260928-DECISION-1 D2/D3); the residual operation-specific additions stay under OI-021 (DEP-02-03-019, ACTIVE) and the adopted result is received via DEL-04-01 (DEP-02-03-012).
- Added: DEP-02-03-022 UPSTREAM INTERFACE DEL-05-01 (CLM-002: arrival observation, subject binding and loop events from host loops; IMPLICIT/MEDIUM); DEP-02-03-023 UPSTREAM INTERFACE DEL-01-01 (CLM-002: observed supplier facts; IMPLICIT/MEDIUM); DEP-02-03-024 UPSTREAM CONSTRAINT EXTERNAL owner governance-phase enforced-checkpoint decision (TBD-006; EXPLICIT/HIGH).
- Considered, not extracted (CONSERVATIVE, information flow only): DEL-03-02 (proposal item dispositions, item-left events, governance-phase governing checkpoint constraint), DEL-04-02 (grant display states), DEL-03-03 (external-channel receiving and governance-phase carriage assurance) and DEL-01-04 (App act control construction) are stated as owned responsibilities in CLM-002/REQ-006 with no statement that this slice consumes or supplies them. The SWBPIPE relay SQ-02 answer in TBD-006 is an input to the future owner decision, not to this deliverable.
- Prior-run position superseded: the 2026-09-28 note that DEL-05-01 was named only as an owner no longer holds, because revised CLM-002 states what DEL-05-01 supplies.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged (all execution rows TBD).
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream).
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, verbatim quotes <=30 words, non-placeholder SourceRefs, target placement, no duplicate typed-target keys); target IDs unresolved: none. Schema validator PASS. enum invocations=25, id invocations=46, all_ok=True
- Optional `validate_decomposition_registers.py` whole-execution EVQ/DRB scan not run (the brief bounds reads to the deliverable and decomposition); the equivalent local EVQ-003/EVQ-004/DRB-006 conditions were checked and are absent.
- Warnings: none.
- Coordinator comparison against DAG_PREP proposed rows and REGISTER_CHANGES.md was performed after extraction as a separate check and is reported in the run-folder return `DX/DX-2_DEL-02-03.md`; it was not an extraction input.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:18:01+00:00 — TASK dependency-extract; UPDATE / CONSERVATIVE; accepted decomposition `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` resolved; 21 ACTIVE (8 ANCHOR, 13 EXECUTION), 0 RETIRED; no local integrity warnings; execution satisfaction remains TBD.
- 2026-09-29T14:38:40+00:00 — TASK DX-2 (run APP-V4-BASIS-ALIGN-20260928); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 22 ACTIVE (8 ANCHOR / 14 EXECUTION), 2 RETIRED; 3 added (DEL-05-01, DEL-01-01, TBD-006 owner decision), 2 updated in place (003, 012), 2 retired (015 OI-001, 016 OI-002); warnings none; dependency closure unclaimed.
