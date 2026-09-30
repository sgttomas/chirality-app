# Dependencies: DEL-04-03 Content-bound decisions and compact run records

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
- **Register:** `Dependencies.csv` v3.1, 29 columns; 33 ACTIVE / 0 RETIRED; ACTIVE origin: 33 EXTRACTED.
- **Classes (ACTIVE):** 10 ANCHOR (1 parent + 7 scope + 2 objective), 23 EXECUTION.
- **Execution targets (ACTIVE):** 14 DELIVERABLE, 6 EXTERNAL, 3 PACKAGE; direction 10 DOWNSTREAM, 13 UPSTREAM; types 3 CONSTRAINT, 2 HANDOVER, 18 INTERFACE.
- **This run:** 0 added, 13 updated in place (re-quoted exactly per ASC-ISS-008: 019, 021–032), 0 retired

| DependencyID | Class / type | Direction | Target | Closure | Status |
|---|---|---|---|---|---|
| DEP-04-03-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-04 | NOT_APPLICABLE | ACTIVE |
| DEP-04-03-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-092 | NOT_APPLICABLE | ACTIVE |
| DEP-04-03-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-093 | NOT_APPLICABLE | ACTIVE |
| DEP-04-03-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-094 | NOT_APPLICABLE | ACTIVE |
| DEP-04-03-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-095 | NOT_APPLICABLE | ACTIVE |
| DEP-04-03-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-096 | NOT_APPLICABLE | ACTIVE |
| DEP-04-03-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-143 | NOT_APPLICABLE | ACTIVE |
| DEP-04-03-008 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-186 | NOT_APPLICABLE | ACTIVE |
| DEP-04-03-009 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-004 | NOT_APPLICABLE | ACTIVE |
| DEP-04-03-010 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-005 | NOT_APPLICABLE | ACTIVE |
| DEP-04-03-011 | EXECUTION / INTERFACE | DOWNSTREAM | PKG-02 | PENDING | ACTIVE |
| DEP-04-03-012 | EXECUTION / INTERFACE | DOWNSTREAM | PKG-03 | PENDING | ACTIVE |
| DEP-04-03-013 | EXECUTION / INTERFACE | DOWNSTREAM | PKG-06 | PENDING | ACTIVE |
| DEP-04-03-014 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-04-02 | PENDING | ACTIVE |
| DEP-04-03-015 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-11 | PENDING | ACTIVE |
| DEP-04-03-016 | EXECUTION / INTERFACE | DOWNSTREAM | Responsible host implementation owner — host-agent run recording | PENDING | ACTIVE |
| DEP-04-03-017 | EXECUTION / INTERFACE | UPSTREAM | DEP-001 | PENDING | ACTIVE |
| DEP-04-03-018 | EXECUTION / INTERFACE | UPSTREAM | Supplied evidence of an actually performed human act | PENDING | ACTIVE |
| DEP-04-03-019 | EXECUTION / CONSTRAINT | UPSTREAM | Owner with affected App/SWB contract owners — OI-001/OI-002 rulings for the first increment (APP-V4-FIRST-INCREMENT-20260928-DECISION-1 D2/D3), carried by App DEL-04-01 | PENDING | ACTIVE |
| DEP-04-03-020 | EXECUTION / CONSTRAINT | UPSTREAM | Shared contract, SWB implementation and App/shared contract owners — affected implementation allocation | PENDING | ACTIVE |
| DEP-04-03-021 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-01 | PENDING | ACTIVE |
| DEP-04-03-022 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-02 | PENDING | ACTIVE |
| DEP-04-03-023 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-01 | PENDING | ACTIVE |
| DEP-04-03-024 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-02 | PENDING | ACTIVE |
| DEP-04-03-025 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-03 | PENDING | ACTIVE |
| DEP-04-03-026 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-03 | PENDING | ACTIVE |
| DEP-04-03-027 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-01 | PENDING | ACTIVE |
| DEP-04-03-028 | EXECUTION / INTERFACE | UPSTREAM | DEL-05-01 | PENDING | ACTIVE |
| DEP-04-03-029 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-05-01 | PENDING | ACTIVE |
| DEP-04-03-030 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-05-02 | PENDING | ACTIVE |
| DEP-04-03-031 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-09-06 | PENDING | ACTIVE |
| DEP-04-03-032 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-09-09 | PENDING | ACTIVE |
| DEP-04-03-033 | EXECUTION / CONSTRAINT | UPSTREAM | OI-021 | PENDING | ACTIVE |

## Lifecycle Summary

- ACTIVE: 33; RETIRED: 0. Closure (ACTIVE): NOT_APPLICABLE 10, PENDING 23, TBD 0, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-04-03; brief: run APP-V4-SCA002-20260929 node DX dispatch message, reusing run APP-V4-BASIS-ALIGN-20260928 `BRIEFS.md` section "DX — dependency-extract UPDATE" shared overrides; selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (both brief overrides). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (brief override; located, SHA256 `ea3388bcb05b2280d8bb10db2578aec9818f40c559b4214e1732da754d9bd7d5`). Companion CSVs in the same folder (Packages, Deliverables, ScopeLedger, Objectives, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (explicit brief override); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/` files, MEMORY.md, _CONTEXT.md and _SEMANTIC.md were not read as extraction sources. `_REFERENCES.md` was read for pointer resolution only.
- Source ScopeOfWork.md SHA256 `ceecddbb67a86f744b413bb08b08c27017a82ebee8500f7600faf8d880fbaa47` (as revised under SCA-V4-002 at commit 1efd4bcda where in scope); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table before Pass 2 examined execution statements. Existing anchor TargetLocation pointers to the GROUP3 frozen snapshot are retained (the IDs are unchanged and resolve in both).
- Source status: ScopeOfWork.md is unchanged since SCA-V4-001 (commit 340ecf341; not in the SCA-V4-002 revision set). The full source was re-read and every ACTIVE row re-checked against it.
- Match/merge (UPDATE): all 33 prior EXTRACTED rows re-observed and kept ACTIVE with their DependencyIDs; LastSeen refreshed. No row added. No row retired.
- Re-quoted exactly (ASC-ISS-008; V12 F1), EvidenceQuote and Notes only: DEP-04-03-019, -021, -022, -023, -024, -025, -026, -027, -028, -029, -030, -031, -032 (inline-code backticks restored, for example `DEL-04-01`, `DEL-05-01` (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5`)). All 13 are now exact substrings of the SoW and at most 30 words. No identity, direction, type, target, maturity or closure change; no arc change.
- Guards (brief), checked after the run: no DOWNSTREAM row to DEL-03-02 or DEL-03-03 (N-12 and N-B8 stay absent); the only DEL-09-06 row is DOWNSTREAM DEP-04-03-031 (DEL-09-06 consuming this record contract, N-08, allowed by the integrator ruling) and there is no UPSTREAM row to DEL-09-06; no DOWNSTREAM row to DEL-04-01 (the DEL-04-01 row DEP-04-03-021 is UPSTREAM).
- Considered, not extracted (CONSERVATIVE, information flow only): as in the prior run, the CLM-002 receiving and consumer sentences carry the UPSTREAM and DOWNSTREAM rows; ownership/exclusion lists alone create no edges; no sentence makes DEL-03-02 or DEL-03-03 a consumer of this record contract.
- Guards (brief): no row makes an SCC-002 member depend on DEL-09-06 and DEL-09-06 has no DOWNSTREAM row to an SCC-002 member; nothing grounds N-12 or N-B8; DEL-04-01 gains no supplier row from an SCC-002 member. Checked against this register after the run: not triggered.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged.
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream).
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, verbatim quotes <=30 words, non-placeholder SourceRefs, target placement, no duplicate typed-target keys); target IDs unresolved: none. Schema validator PASS. enum invocations=22, id invocations=62, all_ok=True
- Optional `validate_decomposition_registers.py` whole-execution EVQ/DRB scan not run per deliverable (the brief bounds reads to the deliverable and decomposition); the equivalent local EVQ-003/EVQ-004/DRB-006 conditions were checked and are absent.
- Warnings: none.
- Comparison with the run folder's `AMENDMENT_PACKET/ARC_EFFECT.md` expectations was performed after extraction as a separate coordinator check and is reported in the run-folder return `DX/DX_DEL-04-03.md`; it was not an extraction input.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:26:48+00:00 — TASK dependency-extract; UPDATE / CONSERVATIVE; accepted Group3 decomposition resolved at `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md`. ACTIVE 20 (ANCHOR 10, EXECUTION 10); no integrity warnings; conditional/external input limitations retained.
- 2026-09-29T14:34:59Z — TASK dependency-extract (APP-V4-BASIS-ALIGN-20260928 DX-1); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (revised under SCA-V4-001); decomposition projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md available; +13 / refreshed 2 / retired 0; ACTIVE 33 (ANCHOR 10 / EXECUTION 23), RETIRED 0; warnings none.
- 2026-09-30T02:46:53+00:00 — TASK DX (run APP-V4-SCA002-20260929); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 33 ACTIVE (10 ANCHOR / 23 EXECUTION), 0 RETIRED; 0 added, 13 updated (re-quoted: 019, 021–032), 0 retired; warnings none; dependency closure unclaimed.
