# Dependencies: DEL-01-01 Stock Codex hosting and supplier contract

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

- **Status:** EXTRACTED (UPDATE 2026-09-29, SCA-V4-002 propagation); local checks recorded in `_run_records/dependency-extract-20260929-sca002.md`.
- **Register:** `Dependencies.csv` v3.1, 29 columns; 24 ACTIVE / 0 RETIRED; ACTIVE origin: 24 EXTRACTED.
- **Classes (ACTIVE):** 15 ANCHOR (1 parent + 11 scope + 3 objective), 9 EXECUTION.
- **Execution targets (ACTIVE):** 6 DELIVERABLE, 3 EXTERNAL; direction 5 DOWNSTREAM, 4 UPSTREAM; types 2 CONSTRAINT, 5 HANDOVER, 1 INTERFACE, 1 PREREQUISITE.
- **This run:** 0 added, 2 updated in place (017, 018: SourceRef/Notes for the revised [N] source line), 0 retired

| DependencyID | Class / type | Direction | Target | Closure | Status |
|---|---|---|---|---|---|
| DEP-01-01-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-01 | NOT_APPLICABLE | ACTIVE |
| DEP-01-01-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-097 | NOT_APPLICABLE | ACTIVE |
| DEP-01-01-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-099 | NOT_APPLICABLE | ACTIVE |
| DEP-01-01-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-100 | NOT_APPLICABLE | ACTIVE |
| DEP-01-01-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-101 | NOT_APPLICABLE | ACTIVE |
| DEP-01-01-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-118 | NOT_APPLICABLE | ACTIVE |
| DEP-01-01-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-119 | NOT_APPLICABLE | ACTIVE |
| DEP-01-01-008 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-121 | NOT_APPLICABLE | ACTIVE |
| DEP-01-01-009 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-128 | NOT_APPLICABLE | ACTIVE |
| DEP-01-01-010 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-131 | NOT_APPLICABLE | ACTIVE |
| DEP-01-01-011 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-135 | NOT_APPLICABLE | ACTIVE |
| DEP-01-01-012 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-149 | NOT_APPLICABLE | ACTIVE |
| DEP-01-01-013 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-001 | NOT_APPLICABLE | ACTIVE |
| DEP-01-01-014 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-002 | NOT_APPLICABLE | ACTIVE |
| DEP-01-01-015 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-004 | NOT_APPLICABLE | ACTIVE |
| DEP-01-01-016 | EXECUTION / CONSTRAINT | UPSTREAM | chirality-app-v4:OI-008 | TBD | ACTIVE |
| DEP-01-01-017 | EXECUTION / CONSTRAINT | UPSTREAM | chirality-app-v4:OI-012 | TBD | ACTIVE |
| DEP-01-01-018 | EXECUTION / PREREQUISITE | UPSTREAM | chirality-app-v4:DEP-005 | TBD | ACTIVE |
| DEP-01-01-019 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-01-02 | TBD | ACTIVE |
| DEP-01-01-020 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-01-03 | TBD | ACTIVE |
| DEP-01-01-021 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-01-04 | TBD | ACTIVE |
| DEP-01-01-022 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-01-05 | TBD | ACTIVE |
| DEP-01-01-023 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-01-06 | TBD | ACTIVE |
| DEP-01-01-024 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-05 | TBD | ACTIVE |

## Lifecycle Summary

- ACTIVE: 24; RETIRED: 0. Closure (ACTIVE): NOT_APPLICABLE 15, PENDING 0, TBD 9, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-01-01; brief: run APP-V4-SCA002-20260929 node DX dispatch message, reusing run APP-V4-BASIS-ALIGN-20260928 `BRIEFS.md` section "DX — dependency-extract UPDATE" shared overrides; selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (both brief overrides). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (brief override; located, SHA256 `ea3388bcb05b2280d8bb10db2578aec9818f40c559b4214e1732da754d9bd7d5`). Companion CSVs in the same folder (Packages, Deliverables, ScopeLedger, Objectives, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (explicit brief override); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/` files, MEMORY.md, _CONTEXT.md and _SEMANTIC.md were not read as extraction sources. `_REFERENCES.md` was read for pointer resolution only.
- Source ScopeOfWork.md SHA256 `9945e72b04b4f45c4c641a5248cca8bc2ac40bf4897d1018c5ab59eba307cc75` (as revised under SCA-V4-002 at commit 1efd4bcda where in scope); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table before Pass 2 examined execution statements. Existing anchor TargetLocation pointers to the GROUP3 frozen snapshot are retained (the IDs are unchanged and resolve in both).
- Match/merge (UPDATE): all 24 prior EXTRACTED rows re-observed with verbatim evidence and kept ACTIVE with their DependencyIDs; LastSeen refreshed. Updated in place: DEP-01-01-017 (OI-012) and DEP-01-01-018 (DEP-005), SourceRef/Notes only, to cite the revised [N] source line. No row added. No row retired.
- SCA-V4-002 edits to this SoW (F-0101-01 source line [N]; F-0101-02 AX-006; Q-6 accepted) name no deliverable and add no consumption statement; [N] now agrees with CLM-003, REQ-006 and TBD-002 (0.158.0 definition/generation pin by APP-V4-FIRST-INCREMENT-20260928-DECISION-1 D4; no implementation or qualification version or environment). No new row, no new arc.
- Considered, not extracted (CONSERVATIVE, information flow only): CLM-004/CLM-005/REQ-007/REQ-008 ownership and exclusion lists alone create no edges beyond the existing CLM-004 consumer handovers (019–023) and the VER-005 receipt (024); OI-008 and OI-012 remain the two owner-held constraints (016, 017); DEP-005 remains the external supplier prerequisite (018).
- Guards (brief): no row makes an SCC-002 member depend on DEL-09-06 and DEL-09-06 has no DOWNSTREAM row to an SCC-002 member; nothing grounds N-12 or N-B8; DEL-04-01 gains no supplier row from an SCC-002 member. Checked against this register after the run: not triggered.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged.
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream).
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, verbatim quotes <=30 words, non-placeholder SourceRefs, target placement, no duplicate typed-target keys); target IDs unresolved: none. Schema validator PASS. enum invocations=22, id invocations=45, all_ok=True
- Optional `validate_decomposition_registers.py` whole-execution EVQ/DRB scan not run per deliverable (the brief bounds reads to the deliverable and decomposition); the equivalent local EVQ-003/EVQ-004/DRB-006 conditions were checked and are absent.
- Warnings: none.
- Comparison with the run folder's `AMENDMENT_PACKET/ARC_EFFECT.md` expectations was performed after extraction as a separate coordinator check and is reported in the run-folder return `DX/DX_DEL-01-01.md`; it was not an extraction input.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:06:28+00:00 — TASK `/root/renewal_research_strategy/dep_del_01_01`, UPDATE / CONSERVATIVE; explicit accepted decomposition `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` resolved; no integrity warnings; ACTIVE 24 (ANCHOR 15, EXECUTION 9); source unchanged; local checks PASS; fulfilment unclaimed.
- 2026-09-29T14:34:59Z — TASK dependency-extract (APP-V4-BASIS-ALIGN-20260928 DX-1); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (revised under SCA-V4-001); decomposition projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md available; +0 / refreshed 2 / retired 0; ACTIVE 24 (ANCHOR 15 / EXECUTION 9), RETIRED 0; warnings none.
- 2026-09-30T02:39:58+00:00 — TASK DX (run APP-V4-SCA002-20260929); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 24 ACTIVE (15 ANCHOR / 9 EXECUTION), 0 RETIRED; 0 added, 2 updated (017, 018), 0 retired; warnings none; dependency closure unclaimed.
