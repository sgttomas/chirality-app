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

- **Status:** EXTRACTED (UPDATE 2026-10-03, SCA-V4-003 propagation); local checks recorded in `_run_records/dependency-extract-20261003-sca003.md`.
- **Register:** `Dependencies.csv` v3.1, 29 columns; 41 ACTIVE / 1 RETIRED; ACTIVE origin: 41 EXTRACTED.
- **Classes (ACTIVE):** 21 ANCHOR (1 parent + 18 scope + 2 objective), 20 EXECUTION.
- **Execution targets (ACTIVE):** 16 DELIVERABLE, 3 EXTERNAL, 1 UNKNOWN; direction 12 DOWNSTREAM, 8 UPSTREAM; types 3 CONSTRAINT, 12 HANDOVER, 3 INTERFACE, 2 PREREQUISITE.
- **This run:** 11 added (032, 033, 034, 035, 036, 037, 038, 039, 040, 041, 042), 1 updated in place (025), 1 retired (022); every other ACTIVE row re-observed (LastSeen only).

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
| DEP-03-01-022 | EXECUTION / HANDOVER | DOWNSTREAM | PKG-02 | PENDING | RETIRED |
| DEP-03-01-023 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-02 | PENDING | ACTIVE |
| DEP-03-01-024 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-04-01 | PENDING | ACTIVE |
| DEP-03-01-025 | EXECUTION / PREREQUISITE | UPSTREAM | SWBPIPE | PENDING | ACTIVE |
| DEP-03-01-026 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-02 | PENDING | ACTIVE |
| DEP-03-01-027 | EXECUTION / CONSTRAINT | UPSTREAM | OI-003 | PENDING | ACTIVE |
| DEP-03-01-028 | EXECUTION / CONSTRAINT | UPSTREAM | App/shared and affected host/consumer technical agreement | PENDING | ACTIVE |
| DEP-03-01-029 | EXECUTION / CONSTRAINT | UPSTREAM | SWBPIPE | PENDING | ACTIVE |
| DEP-03-01-030 | EXECUTION / INTERFACE | UPSTREAM | DEL-09-09 | PENDING | ACTIVE |
| DEP-03-01-031 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-03 | PENDING | ACTIVE |
| DEP-03-01-032 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-01 | PENDING | ACTIVE |
| DEP-03-01-033 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-03 | PENDING | ACTIVE |
| DEP-03-01-034 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-03 | PENDING | ACTIVE |
| DEP-03-01-035 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-04 | PENDING | ACTIVE |
| DEP-03-01-036 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-04-02 | PENDING | ACTIVE |
| DEP-03-01-037 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-04-03 | PENDING | ACTIVE |
| DEP-03-01-038 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-05-01 | PENDING | ACTIVE |
| DEP-03-01-039 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-05-02 | PENDING | ACTIVE |
| DEP-03-01-040 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-06 | PENDING | ACTIVE |
| DEP-03-01-041 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-09 | PENDING | ACTIVE |
| DEP-03-01-042 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-10-03 | PENDING | ACTIVE |

## Lifecycle Summary

- ACTIVE: 41; RETIRED: 1. Closure (ACTIVE): NOT_APPLICABLE 21, PENDING 20, TBD 0, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-03-01; brief: run APP-V4-SCA003-20261002 `BRIEFS.md` section "DX — dependency-extract UPDATE for the 20 registers" and the DX dispatch message (SCA-V4-003, accepted by DECISION-1 and DECISION-2; register row per `_ScopeChange/SCA-V4-003_2026-10-03_1827/Amendment_Actions.csv`, sha256 `9b7c2ce8…6d1c`); selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (brief). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (located, SHA256 `983199cc22c84398000612cd95308c840ad011d302fe31ca110a5aa97e64a70d`). Companion CSVs in the same folder (Deliverables, Packages, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE deliverable target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (brief: "from the revised ScopeOfWork text only"); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/`, MEMORY.md, _CONTEXT.md, _SEMANTIC.md and _REFERENCES.md were not read as extraction sources. Where a row carries an owner-accepted register item whose content the ScopeOfWork does not restate (ledger annotations), the row says so in Notes and names its source.
- Source ScopeOfWork.md SHA256 `48f0496c88b52a48aa86c606d3879b1bc09b9fd8631e765cf06ab02d168c1b6c` (revised by SCA-V4-003 G-0301-01…08 (CLM-002, OUT-001, OUT-003, REQ-001, REQ-002, AX-005); commit 2d5e6845c5); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table (all anchor quotes verbatim after this run) before Pass 2 examined execution statements.
- Match/merge (UPDATE): all prior ACTIVE EXTRACTED rows matched by DependencyID and kept their identities; LastSeen refreshed to 2026-10-04T01:14:27+00:00. New rows take the next DEP-03-01-SEQ numbers; FirstSeen = LastSeen = run time.
- Added 11 DOWNSTREAM HANDOVER rows from the new CLM-002 receivers sentence (R-01-1: DEL-02-01, 02-03, 03-03, 03-04, 04-02, 04-03, 05-01, 05-02, 09-06, 09-09, 10-03), each mirroring an existing consumer row.
- Retired DEP-03-01-022 (PKG-02 package row; R-01-2; retired_by=superseded_by_deliverable_rows; the sentence still occurs; package target, no arc).
- Updated in place: DEP-03-01-025 Notes/SourceRef (R-01-3 edition part; destination elements of REQ-002 noted).
- Not extracted: the basis-profile part of R-01-3 (S-01-4 held, Q-7). FX-PIPE-01 and SH-1 (OUT-003) are this deliverable's outputs cited by others; no further row.
- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged except the two owner-accepted RequiredMaturity/SatisfactionStatus normalizations named above where they apply.
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream). The human-owned prefix of this file is byte-identical.
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, every ACTIVE quote an exact substring of the current ScopeOfWork and at most 30 words, target placement). Schema validator VALID (42 rows). enum invocations=25, id invocations=62, all_ok=True.
- `validate_decomposition_registers.py projects/chirality-app-v4/execution --families EVQ,DRB` after all 20 updates: 41 registers, 929 rows, 0 ERROR, 0 WARNING.
- Warnings: none.
- Comparison with `AMENDMENT_PACKET/ARC_EFFECT.md` and the closure recomputation were performed after extraction as separate coordinator checks and are reported in the run folder `DX/`; they were not extraction inputs.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-27 — TASK `/root/renewal_research_strategy/dep_del_03_01` executed UPDATE/CONSERVATIVE from accepted GROUP3-20260928T001055Z canonical decomposition; 29 ACTIVE (21 ANCHOR/8 EXECUTION), 0 RETIRED. No parent-anchor or decomposition warnings; unresolved execution targets and fulfilment remain explicit.
- 2026-09-28 — TASK `/root/renewal_research_strategy/resolve_dep_03_01` executed bounded R6 UPDATE/CONSERVATIVE against accepted GROUP3-20260928T001055Z and target-resolution report: 30 ACTIVE (21 ANCHOR/9 EXECUTION), 0 RETIRED; 3 EXTERNAL/1 UNKNOWN. Parent-anchor and local checks pass; actor ruling and actual trace remain PENDING; global closure refresh is downstream.
- 2026-09-29T14:42:27+00:00 — TASK DX-2 (run APP-V4-BASIS-ALIGN-20260928); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 31 ACTIVE (21 ANCHOR / 10 EXECUTION), 0 RETIRED; 1 added (DEL-04-03), 3 updated in place (024, 025, 028), 0 retired; warnings none; dependency closure unclaimed.
- 2026-10-04T01:14:27+00:00 — TASK DX (run APP-V4-SCA003-20261002); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (revised under SCA-V4-003); decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 41 ACTIVE (21 ANCHOR / 20 EXECUTION), 1 RETIRED; 11 added, 1 updated, 1 retired; warnings none; dependency closure unclaimed.
