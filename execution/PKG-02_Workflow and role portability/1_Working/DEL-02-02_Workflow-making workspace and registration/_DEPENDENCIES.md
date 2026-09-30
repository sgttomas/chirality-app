# Dependencies: DEL-02-02 Workflow-making workspace and registration

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
- **Register:** `Dependencies.csv` v3.1, 29 columns; 18 ACTIVE / 1 RETIRED; ACTIVE origin: 18 EXTRACTED.
- **Classes (ACTIVE):** 11 ANCHOR (1 parent + 7 scope + 3 objective), 7 EXECUTION.
- **Execution targets (ACTIVE):** 7 DELIVERABLE; direction 1 DOWNSTREAM, 6 UPSTREAM; types 1 HANDOVER, 6 INTERFACE.
- **This run:** 0 added, 1 updated in place (016: Notes for revised TBD-001), 0 retired

| DependencyID | Class / type | Direction | Target | Closure | Status |
|---|---|---|---|---|---|
| DEP-02-02-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-02 | NOT_APPLICABLE | ACTIVE |
| DEP-02-02-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-002 | NOT_APPLICABLE | ACTIVE |
| DEP-02-02-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-046 | NOT_APPLICABLE | ACTIVE |
| DEP-02-02-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-047 | NOT_APPLICABLE | ACTIVE |
| DEP-02-02-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-048 | NOT_APPLICABLE | ACTIVE |
| DEP-02-02-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-049 | NOT_APPLICABLE | ACTIVE |
| DEP-02-02-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-050 | NOT_APPLICABLE | ACTIVE |
| DEP-02-02-008 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-127 | NOT_APPLICABLE | ACTIVE |
| DEP-02-02-009 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-001 | NOT_APPLICABLE | ACTIVE |
| DEP-02-02-010 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-002 | NOT_APPLICABLE | ACTIVE |
| DEP-02-02-011 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-003 | NOT_APPLICABLE | ACTIVE |
| DEP-02-02-012 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-03 | TBD | ACTIVE |
| DEP-02-02-013 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-04 | TBD | ACTIVE |
| DEP-02-02-014 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-01 | TBD | ACTIVE |
| DEP-02-02-015 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-03 | TBD | ACTIVE |
| DEP-02-02-016 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-01 | TBD | ACTIVE |
| DEP-02-02-017 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-03 | TBD | ACTIVE |
| DEP-02-02-018 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-02 | TBD | ACTIVE |
| DEP-02-02-019 | EXECUTION / CONSTRAINT | UPSTREAM | Person performing workflow review and explicit registration | TBD | RETIRED |

## Lifecycle Summary

- ACTIVE: 18; RETIRED: 1. Closure (ACTIVE): NOT_APPLICABLE 11, PENDING 0, TBD 7, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-02-02; brief: run APP-V4-SCA002-20260929 node DX dispatch message, reusing run APP-V4-BASIS-ALIGN-20260928 `BRIEFS.md` section "DX — dependency-extract UPDATE" shared overrides; selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (both brief overrides). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (brief override; located, SHA256 `ea3388bcb05b2280d8bb10db2578aec9818f40c559b4214e1732da754d9bd7d5`). Companion CSVs in the same folder (Packages, Deliverables, ScopeLedger, Objectives, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (explicit brief override); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/` files, MEMORY.md, _CONTEXT.md and _SEMANTIC.md were not read as extraction sources. `_REFERENCES.md` was read for pointer resolution only.
- Source ScopeOfWork.md SHA256 `5814116909db8120c1fe888ba021ca60ad139ea0b36cc89fe7e93ed00235924a` (as revised under SCA-V4-002 at commit 1efd4bcda where in scope); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table before Pass 2 examined execution statements. Existing anchor TargetLocation pointers to the GROUP3 frozen snapshot are retained (the IDs are unchanged and resolve in both).
- Match/merge (UPDATE): all 18 prior ACTIVE EXTRACTED rows re-observed with verbatim evidence and kept ACTIVE with their DependencyIDs; LastSeen refreshed; the 1 RETIRED row (019, retired_by=source_extraction_fidelity_repair) remains RETIRED unchanged. Updated in place: DEP-02-02-016 (DEL-04-01; Notes only, for revised TBD-001). No row added. No row retired by this run.
- SCA-V4-002 edits to this SoW (F-0202-01 TBD-001; F-0202-02 TBD-002 OI-012 clause; F-0202-03 AX-004) name no deliverable that the SoW did not already name and add no consumption statement. The prior run's observation that TBD-001/TBD-002 still described OI-001/OI-002/OI-012 as open is resolved by the source revision. No new arc.
- Considered, not extracted (CONSERVATIVE, information flow only): as in the prior runs, OI-001/OI-002 (now ruled, TBD-001), OI-008 and OI-012 (TBD-002; 0.158.0 definition/generation pin by D4, remaining pin decisions with the App implementation owner), OI-014 (TBD-003) and OI-021 (operation-specific additions) are points of need for their owners rather than inputs this workspace consumes, so this register carries no EXTERNAL OI rows; the adopted policy result is consumed through DEL-04-01 (DEP-02-02-016). Ownership/exclusion lists in CLM-002 through CLM-006 and REQ-008 alone create no edges beyond the existing rows.
- Guards (brief): no row makes an SCC-002 member depend on DEL-09-06 and DEL-09-06 has no DOWNSTREAM row to an SCC-002 member; nothing grounds N-12 or N-B8; DEL-04-01 gains no supplier row from an SCC-002 member. Checked against this register after the run: not triggered.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged.
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream).
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, verbatim quotes <=30 words, non-placeholder SourceRefs, target placement, no duplicate typed-target keys); target IDs unresolved: none. Schema validator PASS. enum invocations=22, id invocations=41, all_ok=True
- Optional `validate_decomposition_registers.py` whole-execution EVQ/DRB scan not run per deliverable (the brief bounds reads to the deliverable and decomposition); the equivalent local EVQ-003/EVQ-004/DRB-006 conditions were checked and are absent.
- Warnings: none.
- Comparison with the run folder's `AMENDMENT_PACKET/ARC_EFFECT.md` expectations was performed after extraction as a separate coordinator check and is reported in the run-folder return `DX/DX_DEL-02-02.md`; it was not an extraction input.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-27T21:05:38-06:00 — TASK dependency-extract UPDATE / CONSERVATIVE; accepted snapshot available; 19 ACTIVE (11 ANCHOR / 8 EXECUTION), 0 RETIRED; local checks PASS; no extraction integrity warnings.
- 2026-09-27T21:08:32-06:00 — Bounded source-extraction fidelity repair: DEP-02-02-019 RETIRED as runtime product behavior without a separately established production input; 18 ACTIVE (11 ANCHOR / 7 EXECUTION), 1 RETIRED. ID/history/source/declared sections preserved; affected checks PASS. No scope, policy or graph-cut decision.
- 2026-09-29T14:34:59Z — TASK dependency-extract (APP-V4-BASIS-ALIGN-20260928 DX-1); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (unchanged source); decomposition projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md available; +0 / refreshed 0 / retired 0; ACTIVE 18 (ANCHOR 11 / EXECUTION 7), RETIRED 1; warnings none.
- 2026-09-30T02:42:47+00:00 — TASK DX (run APP-V4-SCA002-20260929); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 18 ACTIVE (11 ANCHOR / 7 EXECUTION), 1 RETIRED; 0 added, 1 updated (016), 0 retired; warnings none; dependency closure unclaimed.
