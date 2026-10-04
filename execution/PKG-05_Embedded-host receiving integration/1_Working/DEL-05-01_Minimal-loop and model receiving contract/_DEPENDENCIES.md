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

- **Status:** EXTRACTED (UPDATE 2026-10-03, SCA-V4-003 propagation); local checks recorded in `_run_records/dependency-extract-20261003-sca003.md`.
- **Register:** `Dependencies.csv` v3.1, 29 columns; 27 ACTIVE / 0 RETIRED; ACTIVE origin: 27 EXTRACTED.
- **Classes (ACTIVE):** 13 ANCHOR (1 parent + 11 scope + 1 objective), 14 EXECUTION.
- **Execution targets (ACTIVE):** 9 DELIVERABLE, 4 EXTERNAL, 1 UNKNOWN; direction 1 DOWNSTREAM, 13 UPSTREAM; types 2 CONSTRAINT, 1 HANDOVER, 9 INTERFACE, 2 PREREQUISITE.
- **This run:** 2 added (026, 027), 3 updated in place (014, 024, 025), 0 retired (none); every other ACTIVE row re-observed (LastSeen only).

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
| DEP-05-01-026 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-05 | PENDING | ACTIVE |
| DEP-05-01-027 | EXECUTION / HANDOVER | DOWNSTREAM | DEP-001 | PENDING | ACTIVE |

## Lifecycle Summary

- ACTIVE: 27; RETIRED: 0. Closure (ACTIVE): NOT_APPLICABLE 13, PENDING 14, TBD 0, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-05-01; brief: run APP-V4-SCA003-20261002 `BRIEFS.md` section "DX — dependency-extract UPDATE for the 20 registers" and the DX dispatch message (SCA-V4-003, accepted by DECISION-1 and DECISION-2; register row per `_ScopeChange/SCA-V4-003_2026-10-03_1827/Amendment_Actions.csv`, sha256 `9b7c2ce8…6d1c`); selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (brief). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (located, SHA256 `983199cc22c84398000612cd95308c840ad011d302fe31ca110a5aa97e64a70d`). Companion CSVs in the same folder (Deliverables, Packages, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE deliverable target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (brief: "from the revised ScopeOfWork text only"); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/`, MEMORY.md, _CONTEXT.md, _SEMANTIC.md and _REFERENCES.md were not read as extraction sources. Where a row carries an owner-accepted register item whose content the ScopeOfWork does not restate (ledger annotations), the row says so in Notes and names its source.
- Source ScopeOfWork.md SHA256 `6fdf4d59e91c0f2ccc91f71950e60f0e2cd5d9549b5fffdfc01eacadab094fa1` (revised by SCA-V4-003 G-0501-01…04 (OUT-002, CLM-002, TBD-003, AX-005); commit 2d5e6845c5); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table (all anchor quotes verbatim after this run) before Pass 2 examined execution statements.
- Match/merge (UPDATE): all prior ACTIVE EXTRACTED rows matched by DependencyID and kept their identities; LastSeen refreshed to 2026-10-04T01:14:27+00:00. New rows take the next DEP-05-01-SEQ numbers; FirstSeen = LastSeen = run time.
- Added 1 UPSTREAM INTERFACE row to DEL-01-05 (R-0501-4; CLM-002 capability handoff received "as information"; existing admitted arc) and 1 DOWNSTREAM HANDOVER EXTERNAL row to DEP-001 (R-0501-5; host questions via the human-relayed file path; Confidence MEDIUM).
- Updated in place: DEP-05-01-024 re-quoted (R-0501-1; FB-CC-1 is a fixture basis, target stays UNKNOWN, PENDING); DEP-05-01-014 and -025 Notes (R-0501-2, R-0501-3 accepted annotations).
- Not extracted: any row to DEL-09-06 (TBD-003 names its relay files as a coordination route).
- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged except the two owner-accepted RequiredMaturity/SatisfactionStatus normalizations named above where they apply.
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream). The human-owned prefix of this file is byte-identical.
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, every ACTIVE quote an exact substring of the current ScopeOfWork and at most 30 words, target placement). Schema validator VALID (27 rows). enum invocations=24, id invocations=42, all_ok=True.
- `validate_decomposition_registers.py projects/chirality-app-v4/execution --families EVQ,DRB` after all 20 updates: 41 registers, 929 rows, 0 ERROR, 0 WARNING.
- Warnings: none.
- Comparison with `AMENDMENT_PACKET/ARC_EFFECT.md` and the closure recomputation were performed after extraction as separate coordinator checks and are reported in the run folder `DX/`; they were not extraction inputs.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:11:20.190351+00:00 — TASK native child `/root/renewal_research_strategy/dep_del_05_01`; dependency-extract UPDATE / CONSERVATIVE; explicit accepted decomposition available; 24 ACTIVE (13 ANCHOR / 11 EXECUTION), 0 RETIRED; one parent; source/declared sections preserved; unresolved model-interface basis and owner/external conditions retained.
- 2026-09-29T14:40:03+00:00 — TASK DX-2 (run APP-V4-BASIS-ALIGN-20260928); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 25 ACTIVE (13 ANCHOR / 12 EXECUTION), 0 RETIRED; 1 added (DEL-04-02), 9 updated in place (002, 003, 004, 006, 007, 017, 018, 021, 024), 0 retired; warnings none; dependency closure unclaimed.
- 2026-10-04T01:14:27+00:00 — TASK DX (run APP-V4-SCA003-20261002); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (revised under SCA-V4-003); decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 27 ACTIVE (13 ANCHOR / 14 EXECUTION), 0 RETIRED; 2 added, 3 updated, 0 retired; warnings none; dependency closure unclaimed.
