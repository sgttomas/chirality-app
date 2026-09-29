# Dependencies: DEL-03-01 Capability catalog and read-basis contract

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
- **Register:** `Dependencies.csv` v3.1, 29 columns; 31 ACTIVE / 0 RETIRED; ACTIVE origin: 31 EXTRACTED.
- **Classes (ACTIVE):** 21 ANCHOR (1 parent + 18 scope + 2 objective), 10 EXECUTION.
- **Execution targets (ACTIVE):** 5 DELIVERABLE, 3 EXTERNAL, 1 PACKAGE, 1 UNKNOWN; direction 2 DOWNSTREAM, 8 UPSTREAM; types 3 CONSTRAINT, 2 HANDOVER, 3 INTERFACE, 2 PREREQUISITE.
- **This run:** 1 added (DEL-04-03), 3 updated in place (024, 025, 028), 0 retired

| DependencyID | Class / type | Direction | Target | Closure | Status |
|---|---|---|---|---|---|
| DEP-03-01-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-03 | NOT_APPLICABLE | ACTIVE |
| DEP-03-01-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-018 | NOT_APPLICABLE | ACTIVE |
| DEP-03-01-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-067 | NOT_APPLICABLE | ACTIVE |
| DEP-03-01-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-068 | NOT_APPLICABLE | ACTIVE |
| DEP-03-01-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-069 | NOT_APPLICABLE | ACTIVE |
| DEP-03-01-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-072 | NOT_APPLICABLE | ACTIVE |
| DEP-03-01-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-157 | NOT_APPLICABLE | ACTIVE |
| DEP-03-01-008 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-158 | NOT_APPLICABLE | ACTIVE |
| DEP-03-01-009 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-159 | NOT_APPLICABLE | ACTIVE |
| DEP-03-01-010 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-160 | NOT_APPLICABLE | ACTIVE |
| DEP-03-01-011 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-161 | NOT_APPLICABLE | ACTIVE |
| DEP-03-01-012 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-162 | NOT_APPLICABLE | ACTIVE |
| DEP-03-01-013 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-163 | NOT_APPLICABLE | ACTIVE |
| DEP-03-01-014 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-164 | NOT_APPLICABLE | ACTIVE |
| DEP-03-01-015 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-165 | NOT_APPLICABLE | ACTIVE |
| DEP-03-01-016 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-166 | NOT_APPLICABLE | ACTIVE |
| DEP-03-01-017 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-167 | NOT_APPLICABLE | ACTIVE |
| DEP-03-01-018 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-168 | NOT_APPLICABLE | ACTIVE |
| DEP-03-01-019 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-169 | NOT_APPLICABLE | ACTIVE |
| DEP-03-01-020 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-004 | NOT_APPLICABLE | ACTIVE |
| DEP-03-01-021 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-005 | NOT_APPLICABLE | ACTIVE |
| DEP-03-01-022 | EXECUTION / HANDOVER | DOWNSTREAM | PKG-02 | PENDING | ACTIVE |
| DEP-03-01-023 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-02 | PENDING | ACTIVE |
| DEP-03-01-024 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-04-01 | PENDING | ACTIVE |
| DEP-03-01-025 | EXECUTION / PREREQUISITE | UPSTREAM | SWBPIPE | PENDING | ACTIVE |
| DEP-03-01-026 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-02 | PENDING | ACTIVE |
| DEP-03-01-027 | EXECUTION / CONSTRAINT | UPSTREAM | OI-003 | PENDING | ACTIVE |
| DEP-03-01-028 | EXECUTION / CONSTRAINT | UPSTREAM | App/shared and affected host/consumer technical agreement | PENDING | ACTIVE |
| DEP-03-01-029 | EXECUTION / CONSTRAINT | UPSTREAM | SWBPIPE | PENDING | ACTIVE |
| DEP-03-01-030 | EXECUTION / INTERFACE | UPSTREAM | DEL-09-09 | PENDING | ACTIVE |
| DEP-03-01-031 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-03 | PENDING | ACTIVE |

## Lifecycle Summary

- ACTIVE: 31; RETIRED: 0. Closure (ACTIVE): NOT_APPLICABLE 21, PENDING 10, TBD 0, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-03-01; brief: run APP-V4-BASIS-ALIGN-20260928 `BRIEFS.md` section "DX — dependency-extract UPDATE for 18 deliverables" (group DX-2, node DX-2); selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (both brief overrides). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (brief override; located, SHA256 `7434058164f9e53f146793b85c38845a562fbc9ffd46f2b97de18e8d597e5747`; post-SCA-V4-001 working surface). Companion CSVs in the same folder (Packages, Deliverables, ScopeLedger, Objectives, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (explicit brief override); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/` DRAFT files, MEMORY.md, _CONTEXT.md and _SEMANTIC.md were not read as extraction sources. `_REFERENCES.md` was read for pointer resolution only.
- Source ScopeOfWork.md SHA256 `9ada531b59a6efc007c273f131a8d51df390994ef5f379b1d523d635d3849449` (revised under SCA-V4-001, commit 340ecf341); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table before Pass 2 examined execution statements. Existing anchor TargetLocation pointers to the GROUP3 frozen snapshot are retained (the IDs are unchanged by SCA-V4-001 and resolve in both).
- Match/merge (UPDATE): all 30 prior EXTRACTED rows re-observed with verbatim evidence and kept ACTIVE with their DependencyIDs; LastSeen refreshed. Updated in place: DEP-03-01-024 (SourceRef/Notes: TBD-001/REQ-002 record the first-increment OI-001/OI-002 rulings carried by DEL-04-01; OI-021 and DEP-001 still open), DEP-03-01-025 (SourceRef/Notes: host-supplied exposure per surface and content identities under revised REQ-002/REQ-004) and DEP-03-01-028 (Notes: identity-method designation; algorithm unselected under TBD-003). No row retired.
- Added: DEP-03-01-031 UPSTREAM INTERFACE DEL-04-03 (revised CLM-002 explicitly consumes the DEL-04-03 act field set and lapse vocabulary carried as read standing). This supersedes the 2026-09-27 note that the DEL-04-03 exclusion creates no edge; the REQ-007 exclusion itself still creates none.
- Retained with provenance note: DEP-03-01-030 (UPSTREAM INTERFACE DEL-09-09). Its AC-007 evidence is still present verbatim, but the SoW clause does not name the producer; the target was resolved by the 2026-09-28 R6 target-resolution repair (`_run_records/dependency-target-resolution-20260928.md`, report `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-INITIAL-SETUP-20260927/TARGET_RESOLUTION.md`). Under this run's SoW-only read boundary the resolution was preserved (UPDATE match by DependencyID), not re-derived.
- Considered, not extracted (CONSERVATIVE, information flow only): DEL-03-03 remains an ownership statement only; the integration rulings R-6/R-9/R8-4 named in AX-004 are decided sources; host-declared exposure and subject content identities are host-supplied content within DEP-03-01-025, not a separate supplier.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged.
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream).
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, verbatim quotes <=30 words, non-placeholder SourceRefs, target placement, no duplicate typed-target keys); target IDs unresolved: none. Schema validator PASS. enum invocations=24, id invocations=60, all_ok=True
- Optional `validate_decomposition_registers.py` whole-execution EVQ/DRB scan not run (the brief bounds reads to the deliverable and decomposition); the equivalent local EVQ-003/EVQ-004/DRB-006 conditions were checked and are absent.
- Warnings: none.
- Coordinator comparison against DAG_PREP proposed rows and REGISTER_CHANGES.md was performed after extraction as a separate check and is reported in the run-folder return `DX/DX-2_DEL-03-01.md`; it was not an extraction input.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-27 — TASK `/root/renewal_research_strategy/dep_del_03_01` executed UPDATE/CONSERVATIVE from accepted GROUP3-20260928T001055Z canonical decomposition; 29 ACTIVE (21 ANCHOR/8 EXECUTION), 0 RETIRED. No parent-anchor or decomposition warnings; unresolved execution targets and fulfilment remain explicit.
- 2026-09-28 — TASK `/root/renewal_research_strategy/resolve_dep_03_01` executed bounded R6 UPDATE/CONSERVATIVE against accepted GROUP3-20260928T001055Z and target-resolution report: 30 ACTIVE (21 ANCHOR/9 EXECUTION), 0 RETIRED; 3 EXTERNAL/1 UNKNOWN. Parent-anchor and local checks pass; actor ruling and actual trace remain PENDING; global closure refresh is downstream.
- 2026-09-29T14:42:27+00:00 — TASK DX-2 (run APP-V4-BASIS-ALIGN-20260928); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 31 ACTIVE (21 ANCHOR / 10 EXECUTION), 0 RETIRED; 1 added (DEL-04-03), 3 updated in place (024, 025, 028), 0 retired; warnings none; dependency closure unclaimed.
