# Dependencies: DEL-03-03 Local external-agent receiving adapter

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
- **Register:** `Dependencies.csv` v3.1, 29 columns; 20 ACTIVE / 0 RETIRED; ACTIVE origin: 20 EXTRACTED.
- **Classes (ACTIVE):** 5 ANCHOR (1 parent + 3 scope + 1 objective), 15 EXECUTION.
- **Execution targets (ACTIVE):** 12 DELIVERABLE, 3 EXTERNAL; direction 4 DOWNSTREAM, 11 UPSTREAM; types 4 HANDOVER, 6 INTERFACE, 5 PREREQUISITE.
- **This run:** 6 added (015, 016, 017, 018, 019, 020), 4 updated in place (008, 009, 013, 014), 0 retired (none); every other ACTIVE row re-observed (LastSeen only).

| DependencyID | Class / type | Direction | Target | Closure | Status |
|---|---|---|---|---|---|
| DEP-03-03-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-03 | NOT_APPLICABLE | ACTIVE |
| DEP-03-03-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-148 | NOT_APPLICABLE | ACTIVE |
| DEP-03-03-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-183 | NOT_APPLICABLE | ACTIVE |
| DEP-03-03-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-184 | NOT_APPLICABLE | ACTIVE |
| DEP-03-03-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-004 | NOT_APPLICABLE | ACTIVE |
| DEP-03-03-006 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-03-01 | PENDING | ACTIVE |
| DEP-03-03-007 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-03-02 | PENDING | ACTIVE |
| DEP-03-03-008 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-04-01 | PENDING | ACTIVE |
| DEP-03-03-009 | EXECUTION / PREREQUISITE | UPSTREAM | Codex native-tool capability for the selected local MCP or CLI boundary | PENDING | ACTIVE |
| DEP-03-03-010 | EXECUTION / INTERFACE | UPSTREAM | External host owner: catalog-derived local MCP/CLI endpoint contract | PENDING | ACTIVE |
| DEP-03-03-011 | EXECUTION / PREREQUISITE | UPSTREAM | SWBPIPE | PENDING | ACTIVE |
| DEP-03-03-012 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-09 | PENDING | ACTIVE |
| DEP-03-03-013 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-01 | PENDING | ACTIVE |
| DEP-03-03-014 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-03 | PENDING | ACTIVE |
| DEP-03-03-015 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-02 | PENDING | ACTIVE |
| DEP-03-03-016 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-02 | PENDING | ACTIVE |
| DEP-03-03-017 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-01 | PENDING | ACTIVE |
| DEP-03-03-018 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-04 | PENDING | ACTIVE |
| DEP-03-03-019 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-04-03 | PENDING | ACTIVE |
| DEP-03-03-020 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-06 | PENDING | ACTIVE |

## Lifecycle Summary

- ACTIVE: 20; RETIRED: 0. Closure (ACTIVE): NOT_APPLICABLE 5, PENDING 15, TBD 0, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-03-03; brief: run APP-V4-SCA003-20261002 `BRIEFS.md` section "DX — dependency-extract UPDATE for the 20 registers" and the DX dispatch message (SCA-V4-003, accepted by DECISION-1 and DECISION-2; register row per `_ScopeChange/SCA-V4-003_2026-10-03_1827/Amendment_Actions.csv`, sha256 `9b7c2ce8…6d1c`); selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (brief). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (located, SHA256 `983199cc22c84398000612cd95308c840ad011d302fe31ca110a5aa97e64a70d`). Companion CSVs in the same folder (Deliverables, Packages, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE deliverable target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (brief: "from the revised ScopeOfWork text only"); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/`, MEMORY.md, _CONTEXT.md, _SEMANTIC.md and _REFERENCES.md were not read as extraction sources. Where a row carries an owner-accepted register item whose content the ScopeOfWork does not restate (ledger annotations), the row says so in Notes and names its source.
- Source ScopeOfWork.md SHA256 `d76b053f4e97a466429e568a80b911b40550e4d8b97e634488d4aaf7de1e2e7a` (revised by SCA-V4-003 G-0303-01…05 (CLM-002, CLM-003, REQ-003, VER-002, AX-006); commit 2d5e6845c5); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table (all anchor quotes verbatim after this run) before Pass 2 examined execution statements.
- Match/merge (UPDATE): all prior ACTIVE EXTRACTED rows matched by DependencyID and kept their identities; LastSeen refreshed to 2026-10-04T01:14:27+00:00. New rows take the next DEP-03-03-SEQ numbers; FirstSeen = LastSeen = run time.
- Added 3 UPSTREAM INTERFACE rows in the revised CLM-002 consumption sentence: DEL-01-02 (NR-02, new admitted arc), DEL-04-02 and DEL-02-01 (R-03-4, existing held arcs).
- Added 3 DOWNSTREAM HANDOVER rows from the new CLM-003 receivers sentence: DEL-03-04, DEL-04-03, DEL-09-06 (R-03-1).
- Updated in place: DEP-03-03-008 RequiredMaturity TBD → INITIALIZED (R-03-2); DEP-03-03-013 and -014 Statement and quote (R-03-6, R-03-3); DEP-03-03-009 Notes (R-03-5 accepted annotation).
- Not extracted: the DOWNSTREAM row to DEL-02-03 (one of the ledger's 4 R-03-1 rows; mirror of DEP-02-03-026, N-24, held). The ScopeOfWork names DEL-02-03 only as a supplier (CLM-002) and as owner of the governance-phase definition (REQ-003); no sentence states that DEL-02-03 receives this adapter's observations. The arc exists through DEP-02-03-026, so the arc set is unaffected. Returned to the coordinator.
- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged except the two owner-accepted RequiredMaturity/SatisfactionStatus normalizations named above where they apply.
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream). The human-owned prefix of this file is byte-identical.
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, every ACTIVE quote an exact substring of the current ScopeOfWork and at most 30 words, target placement). Schema validator VALID (20 rows). enum invocations=21, id invocations=38, all_ok=True.
- `validate_decomposition_registers.py projects/chirality-app-v4/execution --families EVQ,DRB` after all 20 updates: 41 registers, 929 rows, 0 ERROR, 0 WARNING.
- Warnings: none.
- Comparison with `AMENDMENT_PACKET/ARC_EFFECT.md` and the closure recomputation were performed after extraction as separate coordinator checks and are reported in the run folder `DX/`; they were not extraction inputs.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:20:59+00:00 — TASK `/root/renewal_research_strategy/dep_del_03_03`; UPDATE / CONSERVATIVE; decomposition `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` and accepted companion identity rows available. ACTIVE=12 (ANCHOR=5; EXECUTION=7); RETIRED=0. Mandatory local checks passed; no integrity warnings. Actual external availability/receipt/adoption and unresolved interface choices remain unclaimed.
- 2026-09-28T04:25:33+00:00 — TASK `/root/renewal_research_strategy/resolve_dep_03_03`; bounded R3 UPDATE / CONSERVATIVE using accepted G3 companion rows and the supplied target-resolution report. `DEP-03-03-008` now targets `DEL-04-01`; ACTIVE=12 (ANCHOR=5; EXECUTION=7), RETIRED=0, EXTERNAL=3, UNKNOWN=0. RequiredMaturity=TBD, ProposedMaturity blank and SatisfactionStatus=PENDING preserved; mandatory local checks passed, no global check or graph change.
- 2026-09-29T14:38:50+00:00 — TASK DX-3 (APP-V4-BASIS-ALIGN-20260928); UPDATE / CONSERVATIVE; SOURCE_DOCS=ScopeOfWork.md; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` available. Added 2 (DEL-01-01, DEL-02-03 UPSTREAM INTERFACE), refreshed 1 (DEP-03-03-008), retired 0. ACTIVE=14 (ANCHOR=5; EXECUTION=9), RETIRED=0. Mandatory local checks passed; no integrity warnings.
- 2026-09-30T02:37:21+00:00 — TASK DX (run APP-V4-SCA002-20260929); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 14 ACTIVE (5 ANCHOR / 9 EXECUTION), 0 RETIRED; 0 added, 1 updated (008), 0 retired; warnings none; dependency closure unclaimed.
- 2026-10-04T01:14:27+00:00 — TASK DX (run APP-V4-SCA003-20261002); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (revised under SCA-V4-003); decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 20 ACTIVE (5 ANCHOR / 15 EXECUTION), 0 RETIRED; 6 added, 4 updated, 0 retired; warnings none; dependency closure unclaimed.
