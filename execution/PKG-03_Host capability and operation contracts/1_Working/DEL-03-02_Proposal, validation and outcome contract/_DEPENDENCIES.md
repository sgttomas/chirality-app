# Dependencies: DEL-03-02 Proposal, validation and outcome contract

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
- **Register:** `Dependencies.csv` v3.1, 29 columns; 27 ACTIVE / 0 RETIRED; ACTIVE origin: 27 EXTRACTED.
- **Classes (ACTIVE):** 15 ANCHOR (1 parent + 12 scope + 2 objective), 12 EXECUTION.
- **Execution targets (ACTIVE):** 8 DELIVERABLE, 4 EXTERNAL; direction 6 DOWNSTREAM, 6 UPSTREAM; types 2 CONSTRAINT, 6 HANDOVER, 1 INTERFACE, 3 PREREQUISITE.
- **This run:** 1 added (DEL-02-01), 2 updated in place (016, 017), 0 retired

| DependencyID | Class / type | Direction | Target | Closure | Status |
|---|---|---|---|---|---|
| DEP-03-02-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-03 | NOT_APPLICABLE | ACTIVE |
| DEP-03-02-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-070 | NOT_APPLICABLE | ACTIVE |
| DEP-03-02-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-090 | NOT_APPLICABLE | ACTIVE |
| DEP-03-02-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-091 | NOT_APPLICABLE | ACTIVE |
| DEP-03-02-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-170 | NOT_APPLICABLE | ACTIVE |
| DEP-03-02-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-171 | NOT_APPLICABLE | ACTIVE |
| DEP-03-02-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-172 | NOT_APPLICABLE | ACTIVE |
| DEP-03-02-008 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-173 | NOT_APPLICABLE | ACTIVE |
| DEP-03-02-009 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-174 | NOT_APPLICABLE | ACTIVE |
| DEP-03-02-010 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-175 | NOT_APPLICABLE | ACTIVE |
| DEP-03-02-011 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-176 | NOT_APPLICABLE | ACTIVE |
| DEP-03-02-012 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-177 | NOT_APPLICABLE | ACTIVE |
| DEP-03-02-013 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-178 | NOT_APPLICABLE | ACTIVE |
| DEP-03-02-014 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-004 | NOT_APPLICABLE | ACTIVE |
| DEP-03-02-015 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-005 | NOT_APPLICABLE | ACTIVE |
| DEP-03-02-016 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-03-01 | TBD | ACTIVE |
| DEP-03-02-017 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-04-01 | TBD | ACTIVE |
| DEP-03-02-018 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-04-02 | TBD | ACTIVE |
| DEP-03-02-019 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-04-03 | TBD | ACTIVE |
| DEP-03-02-020 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-03 | TBD | ACTIVE |
| DEP-03-02-021 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-04 | TBD | ACTIVE |
| DEP-03-02-022 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-09 | TBD | ACTIVE |
| DEP-03-02-023 | EXECUTION / PREREQUISITE | UPSTREAM | EXTERNAL DEP-001 | TBD | ACTIVE |
| DEP-03-02-024 | EXECUTION / HANDOVER | DOWNSTREAM | EXTERNAL DEP-001 | TBD | ACTIVE |
| DEP-03-02-025 | EXECUTION / CONSTRAINT | UPSTREAM | ISSUES OI-014 | TBD | ACTIVE |
| DEP-03-02-026 | EXECUTION / CONSTRAINT | UPSTREAM | Relevant contract and host owners: agreement on proposal representation and mechanics | TBD | ACTIVE |
| DEP-03-02-027 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-01 | TBD | ACTIVE |

## Lifecycle Summary

- ACTIVE: 27; RETIRED: 0. Closure (ACTIVE): NOT_APPLICABLE 15, PENDING 0, TBD 12, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-03-02; brief: run APP-V4-BASIS-ALIGN-20260928 `BRIEFS.md` section "DX — dependency-extract UPDATE for 18 deliverables" (group DX-2, node DX-2); selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (both brief overrides). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (brief override; located, SHA256 `7434058164f9e53f146793b85c38845a562fbc9ffd46f2b97de18e8d597e5747`; post-SCA-V4-001 working surface). Companion CSVs in the same folder (Packages, Deliverables, ScopeLedger, Objectives, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (explicit brief override); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/` DRAFT files, MEMORY.md, _CONTEXT.md and _SEMANTIC.md were not read as extraction sources. `_REFERENCES.md` was read for pointer resolution only.
- Source ScopeOfWork.md SHA256 `3560915142ebfbf3fa7197008ea3b0660584665c9d86260b22b550c5c2354d0f` (revised under SCA-V4-001, commit 340ecf341); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table before Pass 2 examined execution statements. Existing anchor TargetLocation pointers to the GROUP3 frozen snapshot are retained (the IDs are unchanged by SCA-V4-001 and resolve in both).
- Match/merge (UPDATE): all 26 prior EXTRACTED rows re-observed with verbatim evidence and kept ACTIVE with their DependencyIDs; LastSeen refreshed. Updated in place: DEP-03-02-016 (Notes: content identity with identity-method designation and subject content identities under revised CLM-003) and DEP-03-02-017 (SourceRef/Notes: REQ-012/TBD-001 first-increment D2/D3 rulings carried by DEL-04-01; OI-021 and DEP-001 still open). No row retired.
- Added: DEP-03-02-027 UPSTREAM INTERFACE DEL-02-01 (revised CLM-003 explicitly consumes DEL-02-01 workflow identity for proposal origin and its checkpoint declarations; the derived governing checkpoint constraint is governance phase only).
- Considered, not extracted (CONSERVATIVE; register convention): OI-021 residual operation-specific additions named in TBD-001/TBD-003 are received through DEL-04-01 as the 2026-09-28 run treated OI-001/OI-002, and OI-003 (TBD-004) remains an extension decision owned elsewhere; neither creates a new local edge. The governance-phase carriage assurance in OUT-001 flows to DEL-03-03 under the existing DEP-03-02-020.
- Anomaly (not repaired under MODE=UPDATE): DEP-03-02-023/024 carry TargetRefID `EXTERNAL DEP-001` and DEP-03-02-025 carries `ISSUES OI-014`, i.e. the SoW source-key prefix is part of the reference. The identities are unambiguous and the rows are EXTERNAL, so they are preserved; a CANONICALIZE_EXISTING pass could normalize them to `DEP-001`/`OI-014`.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged (execution rows TBD).
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream).
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, verbatim quotes <=30 words, non-placeholder SourceRefs, target placement, no duplicate typed-target keys); target IDs unresolved: none. Schema validator PASS. enum invocations=22, id invocations=54, all_ok=True
- Optional `validate_decomposition_registers.py` whole-execution EVQ/DRB scan not run (the brief bounds reads to the deliverable and decomposition); the equivalent local EVQ-003/EVQ-004/DRB-006 conditions were checked and are absent.
- Warnings: none.
- Coordinator comparison against DAG_PREP proposed rows and REGISTER_CHANGES.md was performed after extraction as a separate check and is reported in the run-folder return `DX/DX-2_DEL-03-02.md`; it was not an extraction input.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:05:57.943525+00:00 — TASK `/root/renewal_research_strategy/dep_del_03_02`; UPDATE / CONSERVATIVE; explicit accepted decomposition path above; 26 ACTIVE (15 ANCHOR / 11 EXECUTION), 0 RETIRED; no floating/multiple-parent warning; conditional external inputs and open agreements retained.
- 2026-09-29T14:43:26+00:00 — TASK DX-2 (run APP-V4-BASIS-ALIGN-20260928); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 27 ACTIVE (15 ANCHOR / 12 EXECUTION), 0 RETIRED; 1 added (DEL-02-01), 2 updated in place (016, 017), 0 retired; warnings none; dependency closure unclaimed.
