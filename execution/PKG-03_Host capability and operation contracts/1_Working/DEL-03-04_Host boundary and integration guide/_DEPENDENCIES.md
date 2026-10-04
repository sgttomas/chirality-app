# Dependencies: DEL-03-04 Host boundary and integration guide

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
- **Register:** `Dependencies.csv` v3.1, 29 columns; 23 ACTIVE / 0 RETIRED; ACTIVE origin: 23 EXTRACTED.
- **Classes (ACTIVE):** 4 ANCHOR (1 parent + 2 scope + 1 objective), 19 EXECUTION.
- **Execution targets (ACTIVE):** 18 DELIVERABLE, 1 DOCUMENT; direction 19 UPSTREAM; types 18 INTERFACE, 1 PREREQUISITE.
- **This run:** 0 added (none), 3 updated in place (021, 022, 023), 0 retired (none); every other ACTIVE row re-observed (LastSeen only).

| DependencyID | Class / type | Direction | Target | Closure | Status |
|---|---|---|---|---|---|
| DEP-03-04-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-03 | NOT_APPLICABLE | ACTIVE |
| DEP-03-04-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-156 | NOT_APPLICABLE | ACTIVE |
| DEP-03-04-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-187 | NOT_APPLICABLE | ACTIVE |
| DEP-03-04-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-004 | NOT_APPLICABLE | ACTIVE |
| DEP-03-04-005 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-01 | TBD | ACTIVE |
| DEP-03-04-006 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-02 | TBD | ACTIVE |
| DEP-03-04-007 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-03 | TBD | ACTIVE |
| DEP-03-04-008 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-01 | TBD | ACTIVE |
| DEP-03-04-009 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-03 | TBD | ACTIVE |
| DEP-03-04-010 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-04 | TBD | ACTIVE |
| DEP-03-04-011 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-01 | TBD | ACTIVE |
| DEP-03-04-012 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-02 | TBD | ACTIVE |
| DEP-03-04-013 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-03 | TBD | ACTIVE |
| DEP-03-04-014 | EXECUTION / INTERFACE | UPSTREAM | DEL-05-01 | TBD | ACTIVE |
| DEP-03-04-015 | EXECUTION / INTERFACE | UPSTREAM | DEL-05-02 | TBD | ACTIVE |
| DEP-03-04-016 | EXECUTION / INTERFACE | UPSTREAM | DEL-07-01 | TBD | ACTIVE |
| DEP-03-04-017 | EXECUTION / INTERFACE | UPSTREAM | DEL-07-02 | TBD | ACTIVE |
| DEP-03-04-018 | EXECUTION / INTERFACE | UPSTREAM | DEL-08-01 | TBD | ACTIVE |
| DEP-03-04-019 | EXECUTION / INTERFACE | UPSTREAM | DEL-08-02 | TBD | ACTIVE |
| DEP-03-04-020 | EXECUTION / PREREQUISITE | UPSTREAM | App v4 host integration basis — HOST_INTEGRATION.md §10 | TBD | ACTIVE |
| DEP-03-04-021 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-01 | TBD | ACTIVE |
| DEP-03-04-022 | EXECUTION / INTERFACE | UPSTREAM | DEL-09-06 | TBD | ACTIVE |
| DEP-03-04-023 | EXECUTION / INTERFACE | UPSTREAM | DEL-09-09 | TBD | ACTIVE |

## Lifecycle Summary

- ACTIVE: 23; RETIRED: 0. Closure (ACTIVE): NOT_APPLICABLE 4, PENDING 0, TBD 19, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-03-04; brief: run APP-V4-SCA003-20261002 `BRIEFS.md` section "DX — dependency-extract UPDATE for the 20 registers" and the DX dispatch message (SCA-V4-003, accepted by DECISION-1 and DECISION-2; register row per `_ScopeChange/SCA-V4-003_2026-10-03_1827/Amendment_Actions.csv`, sha256 `9b7c2ce8…6d1c`); selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (brief). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (located, SHA256 `983199cc22c84398000612cd95308c840ad011d302fe31ca110a5aa97e64a70d`). Companion CSVs in the same folder (Deliverables, Packages, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE deliverable target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (brief: "from the revised ScopeOfWork text only"); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/`, MEMORY.md, _CONTEXT.md, _SEMANTIC.md and _REFERENCES.md were not read as extraction sources. Where a row carries an owner-accepted register item whose content the ScopeOfWork does not restate (ledger annotations), the row says so in Notes and names its source.
- Source ScopeOfWork.md SHA256 `aac10af880945a88cf514fcb07d13544800fb3785a550b1b6660062f0d65761d` (revised by SCA-V4-003 G-0304-01…04 (CLM-003, receiving-map row "Autonomy", AX-005); commit 2d5e6845c5); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table (all anchor quotes verbatim after this run) before Pass 2 examined execution statements.
- Match/merge (UPDATE): all prior ACTIVE EXTRACTED rows matched by DependencyID and kept their identities; LastSeen refreshed to 2026-10-04T01:14:27+00:00. New rows take the next DEP-03-04-SEQ numbers; FirstSeen = LastSeen = run time.
- Updated in place: DEP-03-04-021 and -022 Statement and quote (R-04-1, R-04-2); DEP-03-04-023 re-quoted only (its clause moved within the extended sentence).
- No new row: the revised text adds no supplier or receiver. This deliverable is not an SCC-002 member, so its existing DEL-09-06 row (DEP-03-04-022) does not engage the DEL-09-06 guard.
- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged except the two owner-accepted RequiredMaturity/SatisfactionStatus normalizations named above where they apply.
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream). The human-owned prefix of this file is byte-identical.
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, every ACTIVE quote an exact substring of the current ScopeOfWork and at most 30 words, target placement). Schema validator VALID (23 rows). enum invocations=19, id invocations=50, all_ok=True.
- `validate_decomposition_registers.py projects/chirality-app-v4/execution --families EVQ,DRB` after all 20 updates: 41 registers, 929 rows, 0 ERROR, 0 WARNING.
- Warnings: none.
- Comparison with `AMENDMENT_PACKET/ARC_EFFECT.md` and the closure recomputation were performed after extraction as separate coordinator checks and are reported in the run folder `DX/`; they were not extraction inputs.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:20:20+00:00 — TASK `/root/renewal_research_strategy/dep_del_03_04`; UPDATE / CONSERVATIVE; accepted GROUP3 canonical decomposition resolved; 20 ACTIVE (4 ANCHOR / 16 EXECUTION), 0 RETIRED, 0 declared mirrors; one parent; no floating/ambiguous/missing-decomposition warnings; all execution satisfaction TBD.
- 2026-09-29T14:38:50+00:00 — TASK DX-3 (APP-V4-BASIS-ALIGN-20260928); UPDATE / CONSERVATIVE; SOURCE_DOCS=ScopeOfWork.md; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` available. Added 3 (DEL-01-01, DEL-09-06, DEL-09-09 UPSTREAM INTERFACE), refreshed 1 (DEP-03-04-011), retired 0. ACTIVE=23 (ANCHOR=4; EXECUTION=19), RETIRED=0. Mandatory local checks passed; no integrity warnings.
- 2026-10-04T01:14:27+00:00 — TASK DX (run APP-V4-SCA003-20261002); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (revised under SCA-V4-003); decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 23 ACTIVE (4 ANCHOR / 19 EXECUTION), 0 RETIRED; 0 added, 3 updated, 0 retired; warnings none; dependency closure unclaimed.
