# Dependencies: DEL-10-03 Shared commitments and consumer responsibility account

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
- **Register:** `Dependencies.csv` v3.1, 29 columns; 20 ACTIVE / 0 RETIRED; ACTIVE origin: 20 EXTRACTED.
- **Classes (ACTIVE):** 7 ANCHOR (1 parent + 5 scope + 1 objective), 13 EXECUTION.
- **Execution targets (ACTIVE):** 11 DELIVERABLE, 1 PACKAGE, 1 UNKNOWN; direction 2 DOWNSTREAM, 11 UPSTREAM; types 2 HANDOVER, 9 INTERFACE, 2 PREREQUISITE.
- **This run:** 0 added, 1 updated in place (015: Notes for revised REQ-005), 0 retired

| DependencyID | Class / type | Direction | Target | Closure | Status |
|---|---|---|---|---|---|
| DEP-10-03-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-10 | NOT_APPLICABLE | ACTIVE |
| DEP-10-03-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-230 | NOT_APPLICABLE | ACTIVE |
| DEP-10-03-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-231 | NOT_APPLICABLE | ACTIVE |
| DEP-10-03-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-232 | NOT_APPLICABLE | ACTIVE |
| DEP-10-03-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-233 | NOT_APPLICABLE | ACTIVE |
| DEP-10-03-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-234 | NOT_APPLICABLE | ACTIVE |
| DEP-10-03-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-010 | NOT_APPLICABLE | ACTIVE |
| DEP-10-03-008 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-01 | TBD | ACTIVE |
| DEP-10-03-009 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-03 | TBD | ACTIVE |
| DEP-10-03-010 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-04 | TBD | ACTIVE |
| DEP-10-03-011 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-01 | TBD | ACTIVE |
| DEP-10-03-012 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-02 | TBD | ACTIVE |
| DEP-10-03-013 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-01 | TBD | ACTIVE |
| DEP-10-03-014 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-03 | TBD | ACTIVE |
| DEP-10-03-015 | EXECUTION / INTERFACE | UPSTREAM | DEL-05-01 | TBD | ACTIVE |
| DEP-10-03-016 | EXECUTION / INTERFACE | UPSTREAM | DEL-05-02 | TBD | ACTIVE |
| DEP-10-03-017 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-10-01 | TBD | ACTIVE |
| DEP-10-03-018 | EXECUTION / PREREQUISITE | UPSTREAM | Identified current source for affected packaging selectors, instruction consumers and tool paths | TBD | ACTIVE |
| DEP-10-03-019 | EXECUTION / HANDOVER | DOWNSTREAM | PKG-11 | TBD | ACTIVE |
| DEP-10-03-020 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-10-04 | TBD | ACTIVE |

## Lifecycle Summary

- ACTIVE: 20; RETIRED: 0. Closure (ACTIVE): NOT_APPLICABLE 7, PENDING 0, TBD 13, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-10-03; brief: run APP-V4-SCA002-20260929 node DX dispatch message, reusing run APP-V4-BASIS-ALIGN-20260928 `BRIEFS.md` section "DX — dependency-extract UPDATE" shared overrides; selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (both brief overrides). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (brief override; located, SHA256 `ea3388bcb05b2280d8bb10db2578aec9818f40c559b4214e1732da754d9bd7d5`). Companion CSVs in the same folder (Packages, Deliverables, ScopeLedger, Objectives, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (explicit brief override); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/` files, MEMORY.md, _CONTEXT.md and _SEMANTIC.md were not read as extraction sources. `_REFERENCES.md` was read for pointer resolution only.
- Source ScopeOfWork.md SHA256 `31bc607defa42914520959234f2400858d4c1d5272ac5fa523fcea39d1b94166` (as revised under SCA-V4-002 at commit 1efd4bcda where in scope); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table before Pass 2 examined execution statements. Existing anchor TargetLocation pointers to the GROUP3 frozen snapshot are retained (the IDs are unchanged and resolve in both).
- Match/merge (UPDATE): all 20 prior EXTRACTED rows re-observed with verbatim evidence and kept ACTIVE with their DependencyIDs; LastSeen refreshed (first refresh since the 2026-09-27 extraction; this SoW was not in the SCA-V4-001 set). Updated in place: DEP-10-03-015 (DEL-05-01; Notes only, for revised REQ-005). No row added. No row retired.
- SCA-V4-002 edits to this SoW (F-1003-01 REQ-005 "local-first" replacement, applying D4-3; F-1003-02 AX-005) name no deliverable and add no consumption statement; the first REQ-005 clause quoted by rows 008–016 is unchanged. No new arc.
- Prior-run readings retained: REQ-005 supplies the positive input requirement for the nine compatible-contract rows; CLM ownership lists and REQ-006 exclusions alone create no edges; DEP-10-03-018 stays UNKNOWN (affected source set not fixed by the contract); the PKG-11 handoff (019) stays at package level; OI-017 is carried by the DEL-10-01 record row (017).
- Considered, not extracted (CONSERVATIVE, information flow only): the revised REQ-005 model-choice clause (local or cloud model chosen by the person; OAuth sign-in or API key) names no deliverable and is a person's choice, not an input from DEL-01-05 or another deliverable, so no row; OI-013/014/018 and OI-024/DEP-006 (TBD-001…003) retain their owners and points of need as in the prior run and are not extracted as separate rows.
- Guards (brief): no row makes an SCC-002 member depend on DEL-09-06 and DEL-09-06 has no DOWNSTREAM row to an SCC-002 member; nothing grounds N-12 or N-B8; DEL-04-01 gains no supplier row from an SCC-002 member. Checked against this register after the run: not triggered.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged.
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream).
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, verbatim quotes <=30 words, non-placeholder SourceRefs, target placement, no duplicate typed-target keys); target IDs unresolved: none. Schema validator PASS. enum invocations=22, id invocations=44, all_ok=True
- Optional `validate_decomposition_registers.py` whole-execution EVQ/DRB scan not run per deliverable (the brief bounds reads to the deliverable and decomposition); the equivalent local EVQ-003/EVQ-004/DRB-006 conditions were checked and are absent.
- Warnings: none.
- Comparison with the run folder's `AMENDMENT_PACKET/ARC_EFFECT.md` expectations was performed after extraction as a separate coordinator check and is reported in the run-folder return `DX/DX_DEL-10-03.md`; it was not an extraction input.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-27 — TASK `/root/renewal_research_strategy/dep_del_10_03`; UPDATE / CONSERVATIVE; accepted Group3 decomposition available; 20 ACTIVE (7 ANCHOR, 13 EXECUTION), 0 RETIRED, 1 UNKNOWN target; no integrity warnings; local validation only.
- 2026-09-30T02:45:15+00:00 — TASK DX (run APP-V4-SCA002-20260929); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 20 ACTIVE (7 ANCHOR / 13 EXECUTION), 0 RETIRED; 0 added, 1 updated (015), 0 retired; warnings none; dependency closure unclaimed.
