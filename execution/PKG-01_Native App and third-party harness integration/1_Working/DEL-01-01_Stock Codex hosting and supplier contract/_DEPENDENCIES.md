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

- **Status:** EXTRACTED (UPDATE 2026-10-03, SCA-V4-003 propagation); local checks recorded in `_run_records/dependency-extract-20261003-sca003.md`.
- **Register:** `Dependencies.csv` v3.1, 29 columns; 32 ACTIVE / 0 RETIRED; ACTIVE origin: 32 EXTRACTED.
- **Classes (ACTIVE):** 15 ANCHOR (1 parent + 11 scope + 3 objective), 17 EXECUTION.
- **Execution targets (ACTIVE):** 14 DELIVERABLE, 3 EXTERNAL; direction 13 DOWNSTREAM, 4 UPSTREAM; types 2 CONSTRAINT, 13 HANDOVER, 1 INTERFACE, 1 PREREQUISITE.
- **This run:** 8 added (025, 026, 027, 028, 029, 030, 031, 032), 3 updated in place (017, 018, 022), 0 retired (none); every other ACTIVE row re-observed (LastSeen only).

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
| DEP-01-01-025 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-01 | TBD | ACTIVE |
| DEP-01-01-026 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-03 | TBD | ACTIVE |
| DEP-01-01-027 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-03 | TBD | ACTIVE |
| DEP-01-01-028 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-04 | TBD | ACTIVE |
| DEP-01-01-029 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-06 | TBD | ACTIVE |
| DEP-01-01-030 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-06-01 | TBD | ACTIVE |
| DEP-01-01-031 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-01 | TBD | ACTIVE |
| DEP-01-01-032 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-02 | TBD | ACTIVE |

## Lifecycle Summary

- ACTIVE: 32; RETIRED: 0. Closure (ACTIVE): NOT_APPLICABLE 15, PENDING 0, TBD 17, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-01-01; brief: run APP-V4-SCA003-20261002 `BRIEFS.md` section "DX — dependency-extract UPDATE for the 20 registers" and the DX dispatch message (SCA-V4-003, accepted by DECISION-1 and DECISION-2; register row per `_ScopeChange/SCA-V4-003_2026-10-03_1827/Amendment_Actions.csv`, sha256 `9b7c2ce8…6d1c`); selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (brief). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (located, SHA256 `983199cc22c84398000612cd95308c840ad011d302fe31ca110a5aa97e64a70d`). Companion CSVs in the same folder (Deliverables, Packages, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE deliverable target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (brief: "from the revised ScopeOfWork text only"); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/`, MEMORY.md, _CONTEXT.md, _SEMANTIC.md and _REFERENCES.md were not read as extraction sources. Where a row carries an owner-accepted register item whose content the ScopeOfWork does not restate (ledger annotations), the row says so in Notes and names its source.
- Source ScopeOfWork.md SHA256 `bbc81a8d31eeacab3497acf297c8c6eeac7b2f6febda5381f332ec14b8f65d02` (revised by SCA-V4-003 G-0101-01…04 (CLM-004 receivers sentence P1-09, CLM-005 harness-capability supply S-11-1, TBD-002 observation pointers S-11-2, AX-007); commit 2d5e6845c5); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table (all anchor quotes verbatim after this run) before Pass 2 examined execution statements.
- Match/merge (UPDATE): all prior ACTIVE EXTRACTED rows matched by DependencyID and kept their identities; LastSeen refreshed to 2026-10-04T01:14:27+00:00. New rows take the next DEP-01-01-SEQ numbers; FirstSeen = LastSeen = run time.
- Added 8 DOWNSTREAM HANDOVER rows grounded by the new CLM-004 receivers sentence (DEL-02-03, DEL-03-03, DEL-03-04, DEL-09-06, DEL-06-01, DEL-09-01, DEL-09-02) and the new CLM-005 supply sentence (DEL-02-01); each mirrors an existing consumer row on an existing admitted arc (ledger R-11-1). No arc change.
- Updated in place (Notes/SourceRef only): DEP-01-01-017 (TBD-002 pointer), DEP-01-01-018 (R-11-2 observation pointer), DEP-01-01-022 (R-11-3 accepted annotation, labelled as not restated in the ScopeOfWork).
- Not extracted: DOWNSTREAM rows to DEL-02-04 and DEL-04-03 (2 of the ledger's 10 R-11-1 rows). The revised ScopeOfWork names both only as owners in CLM-005 ("owns additive role supply", "owns content-bound records") and in the REQ-008 exclusion list; no sentence states that either receives this supplier boundary. Ownership/exclusion lists create no edges here (CONSERVATIVE). The arcs exist through the consumer rows DEP-02-04-010 and DEP-04-03-027, so the arc set is unaffected. Returned to the coordinator.
- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged except the two owner-accepted RequiredMaturity/SatisfactionStatus normalizations named above where they apply.
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream). The human-owned prefix of this file is byte-identical.
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, every ACTIVE quote an exact substring of the current ScopeOfWork and at most 30 words, target placement). Schema validator VALID (32 rows). enum invocations=22, id invocations=51, all_ok=True.
- `validate_decomposition_registers.py projects/chirality-app-v4/execution --families EVQ,DRB` after all 20 updates: 41 registers, 929 rows, 0 ERROR, 0 WARNING.
- Warnings: none.
- Comparison with `AMENDMENT_PACKET/ARC_EFFECT.md` and the closure recomputation were performed after extraction as separate coordinator checks and are reported in the run folder `DX/`; they were not extraction inputs.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:06:28+00:00 — TASK `/root/renewal_research_strategy/dep_del_01_01`, UPDATE / CONSERVATIVE; explicit accepted decomposition `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` resolved; no integrity warnings; ACTIVE 24 (ANCHOR 15, EXECUTION 9); source unchanged; local checks PASS; fulfilment unclaimed.
- 2026-09-29T14:34:59Z — TASK dependency-extract (APP-V4-BASIS-ALIGN-20260928 DX-1); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (revised under SCA-V4-001); decomposition projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md available; +0 / refreshed 2 / retired 0; ACTIVE 24 (ANCHOR 15 / EXECUTION 9), RETIRED 0; warnings none.
- 2026-09-30T02:39:58+00:00 — TASK DX (run APP-V4-SCA002-20260929); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 24 ACTIVE (15 ANCHOR / 9 EXECUTION), 0 RETIRED; 0 added, 2 updated (017, 018), 0 retired; warnings none; dependency closure unclaimed.
- 2026-10-04T01:14:27+00:00 — TASK DX (run APP-V4-SCA003-20261002); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (revised under SCA-V4-003); decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 32 ACTIVE (15 ANCHOR / 17 EXECUTION), 0 RETIRED; 8 added, 3 updated, 0 retired; warnings none; dependency closure unclaimed.
