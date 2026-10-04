# Dependencies: DEL-04-02 Visible autonomy and result standing

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
- **Register:** `Dependencies.csv` v3.1, 29 columns; 28 ACTIVE / 0 RETIRED; ACTIVE origin: 28 EXTRACTED.
- **Classes (ACTIVE):** 6 ANCHOR (1 parent + 4 scope + 1 objective), 22 EXECUTION.
- **Execution targets (ACTIVE):** 15 DELIVERABLE, 7 EXTERNAL; direction 9 DOWNSTREAM, 13 UPSTREAM; types 6 CONSTRAINT, 8 HANDOVER, 7 INTERFACE, 1 PREREQUISITE.
- **This run:** 3 added (026, 027, 028), 0 updated in place (none), 0 retired (none); every other ACTIVE row re-observed (LastSeen only).

| DependencyID | Class / type | Direction | Target | Closure | Status |
|---|---|---|---|---|---|
| DEP-04-02-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-04 | NOT_APPLICABLE | ACTIVE |
| DEP-04-02-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-075 | NOT_APPLICABLE | ACTIVE |
| DEP-04-02-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-076 | NOT_APPLICABLE | ACTIVE |
| DEP-04-02-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-077 | NOT_APPLICABLE | ACTIVE |
| DEP-04-02-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-078 | NOT_APPLICABLE | ACTIVE |
| DEP-04-02-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-005 | NOT_APPLICABLE | ACTIVE |
| DEP-04-02-007 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-04-01 | PENDING | ACTIVE |
| DEP-04-02-008 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-03 | PENDING | ACTIVE |
| DEP-04-02-009 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-04-03 | PENDING | ACTIVE |
| DEP-04-02-010 | EXECUTION / INTERFACE | UPSTREAM | App-v4:DEP-001:SWBPIPE | PENDING | ACTIVE |
| DEP-04-02-011 | EXECUTION / CONSTRAINT | UPSTREAM | App-v4:OI-001 | PENDING | ACTIVE |
| DEP-04-02-012 | EXECUTION / CONSTRAINT | UPSTREAM | App-v4:OI-002 | PENDING | ACTIVE |
| DEP-04-02-013 | EXECUTION / CONSTRAINT | UPSTREAM | App-v4:OI-013 | PENDING | ACTIVE |
| DEP-04-02-014 | EXECUTION / CONSTRAINT | UPSTREAM | App-v4:OI-014 | PENDING | ACTIVE |
| DEP-04-02-015 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-02 | PENDING | ACTIVE |
| DEP-04-02-016 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-01 | PENDING | ACTIVE |
| DEP-04-02-017 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-03 | PENDING | ACTIVE |
| DEP-04-02-018 | EXECUTION / INTERFACE | UPSTREAM | DEL-05-01 | PENDING | ACTIVE |
| DEP-04-02-019 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-05-01 | PENDING | ACTIVE |
| DEP-04-02-020 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-05-02 | PENDING | ACTIVE |
| DEP-04-02-021 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-02 | PENDING | ACTIVE |
| DEP-04-02-022 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-03 | PENDING | ACTIVE |
| DEP-04-02-023 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-03 | PENDING | ACTIVE |
| DEP-04-02-024 | EXECUTION / CONSTRAINT | UPSTREAM | App-v4:OI-021 | PENDING | ACTIVE |
| DEP-04-02-025 | EXECUTION / CONSTRAINT | UPSTREAM | APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4 | PENDING | ACTIVE |
| DEP-04-02-026 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-04 | PENDING | ACTIVE |
| DEP-04-02-027 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-06 | PENDING | ACTIVE |
| DEP-04-02-028 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-09 | PENDING | ACTIVE |

## Lifecycle Summary

- ACTIVE: 28; RETIRED: 0. Closure (ACTIVE): NOT_APPLICABLE 6, PENDING 22, TBD 0, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-04-02; brief: run APP-V4-SCA003-20261002 `BRIEFS.md` section "DX — dependency-extract UPDATE for the 20 registers" and the DX dispatch message (SCA-V4-003, accepted by DECISION-1 and DECISION-2; register row per `_ScopeChange/SCA-V4-003_2026-10-03_1827/Amendment_Actions.csv`, sha256 `9b7c2ce8…6d1c`); selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (brief). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (located, SHA256 `983199cc22c84398000612cd95308c840ad011d302fe31ca110a5aa97e64a70d`). Companion CSVs in the same folder (Deliverables, Packages, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE deliverable target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (brief: "from the revised ScopeOfWork text only"); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/`, MEMORY.md, _CONTEXT.md, _SEMANTIC.md and _REFERENCES.md were not read as extraction sources. Where a row carries an owner-accepted register item whose content the ScopeOfWork does not restate (ledger annotations), the row says so in Notes and names its source.
- Source ScopeOfWork.md SHA256 `e130ef7dc92ac865631002a9ab77fc2aedb16d6b0e0a568d7c62f8a8bb1c3fc5` (revised by SCA-V4-003 G-0402-01…02 (CLM-002, AX-006); commit 2d5e6845c5); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table (all anchor quotes verbatim after this run) before Pass 2 examined execution statements.
- Match/merge (UPDATE): all prior ACTIVE EXTRACTED rows matched by DependencyID and kept their identities; LastSeen refreshed to 2026-10-04T01:14:27+00:00. New rows take the next DEP-04-02-SEQ numbers; FirstSeen = LastSeen = run time.
- Added 3 DOWNSTREAM HANDOVER rows from the new CLM-002 sentence: DEL-03-04, DEL-09-06, DEL-09-09 (R2-04-02-a…c).
- No receivers-sentence target is left unextracted.
- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged except the two owner-accepted RequiredMaturity/SatisfactionStatus normalizations named above where they apply.
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream). The human-owned prefix of this file is byte-identical.
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, every ACTIVE quote an exact substring of the current ScopeOfWork and at most 30 words, target placement). Schema validator VALID (28 rows). enum invocations=22, id invocations=45, all_ok=True.
- `validate_decomposition_registers.py projects/chirality-app-v4/execution --families EVQ,DRB` after all 20 updates: 41 registers, 929 rows, 0 ERROR, 0 WARNING.
- Warnings: none.
- Comparison with `AMENDMENT_PACKET/ARC_EFFECT.md` and the closure recomputation were performed after extraction as separate coordinator checks and are reported in the run folder `DX/`; they were not extraction inputs.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:25:20+00:00 — TASK `/root/renewal_research_strategy/dep_del_04_02`; UPDATE / CONSERVATIVE; accepted decomposition available at `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md`; 14 ACTIVE (6 ANCHOR, 8 EXECUTION), 0 RETIRED; local checks passed; unresolved input/owner/host conditions retained without floating or ambiguous anchors.
- 2026-09-29T14:34:59Z — TASK dependency-extract (APP-V4-BASIS-ALIGN-20260928 DX-1); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (revised under SCA-V4-001); decomposition projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md available; +11 / refreshed 2 / retired 0; ACTIVE 25 (ANCHOR 6 / EXECUTION 19), RETIRED 0; warnings none.
- 2026-09-30T02:39:02+00:00 — TASK DX (run APP-V4-SCA002-20260929); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 25 ACTIVE (6 ANCHOR / 19 EXECUTION), 0 RETIRED; 0 added, 13 updated (12 re-quoted: 011, 012, 015–023, 025; 007 notes), 0 retired; warnings none; dependency closure unclaimed.
- 2026-10-04T01:14:27+00:00 — TASK DX (run APP-V4-SCA003-20261002); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (revised under SCA-V4-003); decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 28 ACTIVE (6 ANCHOR / 22 EXECUTION), 0 RETIRED; 3 added, 0 updated, 0 retired; warnings none; dependency closure unclaimed.
