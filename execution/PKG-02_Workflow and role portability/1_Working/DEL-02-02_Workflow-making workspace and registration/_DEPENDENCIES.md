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

- **Status:** EXTRACTED (UPDATE 2026-10-03, SCA-V4-003 propagation); local checks recorded in `_run_records/dependency-extract-20261003-sca003.md`.
- **Register:** `Dependencies.csv` v3.1, 29 columns; 23 ACTIVE / 1 RETIRED; ACTIVE origin: 23 EXTRACTED.
- **Classes (ACTIVE):** 11 ANCHOR (1 parent + 7 scope + 3 objective), 12 EXECUTION.
- **Execution targets (ACTIVE):** 12 DELIVERABLE; direction 5 DOWNSTREAM, 7 UPSTREAM; types 5 HANDOVER, 7 INTERFACE.
- **This run:** 5 added (020, 021, 022, 023, 024), 4 updated in place (013, 015, 016, 017), 0 retired (none); every other ACTIVE row re-observed (LastSeen only).

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
| DEP-02-02-020 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-02 | TBD | ACTIVE |
| DEP-02-02-021 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-01-04 | TBD | ACTIVE |
| DEP-02-02-022 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-03 | TBD | ACTIVE |
| DEP-02-02-023 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-06 | TBD | ACTIVE |
| DEP-02-02-024 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-04-03 | TBD | ACTIVE |

## Lifecycle Summary

- ACTIVE: 23; RETIRED: 1. Closure (ACTIVE): NOT_APPLICABLE 11, PENDING 0, TBD 12, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-02-02; brief: run APP-V4-SCA003-20261002 `BRIEFS.md` section "DX — dependency-extract UPDATE for the 20 registers" and the DX dispatch message (SCA-V4-003, accepted by DECISION-1 and DECISION-2; register row per `_ScopeChange/SCA-V4-003_2026-10-03_1827/Amendment_Actions.csv`, sha256 `9b7c2ce8…6d1c`); selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (brief). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (located, SHA256 `983199cc22c84398000612cd95308c840ad011d302fe31ca110a5aa97e64a70d`). Companion CSVs in the same folder (Deliverables, Packages, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE deliverable target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (brief: "from the revised ScopeOfWork text only"); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/`, MEMORY.md, _CONTEXT.md, _SEMANTIC.md and _REFERENCES.md were not read as extraction sources. Where a row carries an owner-accepted register item whose content the ScopeOfWork does not restate (ledger annotations), the row says so in Notes and names its source.
- Source ScopeOfWork.md SHA256 `fe9f9bd923f94ed314aba054d5d04e4e803ca4ec0456bd5d11d94df355198d51` (revised by SCA-V4-003 G-0202-01…09 (CLM-002, CLM-003, REQ-001, REQ-002, REQ-003, REQ-008, AX-005); commit 2d5e6845c5); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table (all anchor quotes verbatim after this run) before Pass 2 examined execution statements.
- Match/merge (UPDATE): all prior ACTIVE EXTRACTED rows matched by DependencyID and kept their identities; LastSeen refreshed to 2026-10-04T01:14:27+00:00. New rows take the next DEP-02-02-SEQ numbers; FirstSeen = LastSeen = run time.
- Added 1 UPSTREAM INTERFACE row to DEL-01-02 (NR-04, new admitted arc; REQ-001 "A run in the chain ends only as `DEL-01-02` defines ending a run").
- Added 4 DOWNSTREAM HANDOVER rows from the new CLM-003 receivers sentence: DEL-01-04, DEL-02-03, DEL-09-06 (R3-02-02-a…c, existing arcs) and DEL-04-03 (R3-02-02-d, mirror of the new held arc R20-10).
- Updated in place: DEP-02-02-013 (SC3-02-02-6), DEP-02-02-015 (SC3-02-02-9), DEP-02-02-016 and -017 (SC3-02-02-7; the "A15" label is the ledger's and DEL-01-04's, noted) Statements.
- No receivers-sentence target is left unextracted.
- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged except the two owner-accepted RequiredMaturity/SatisfactionStatus normalizations named above where they apply.
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream). The human-owned prefix of this file is byte-identical.
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, every ACTIVE quote an exact substring of the current ScopeOfWork and at most 30 words, target placement). Schema validator VALID (24 rows). enum invocations=22, id invocations=38, all_ok=True.
- `validate_decomposition_registers.py projects/chirality-app-v4/execution --families EVQ,DRB` after all 20 updates: 41 registers, 929 rows, 0 ERROR, 0 WARNING.
- Warnings: none.
- Comparison with `AMENDMENT_PACKET/ARC_EFFECT.md` and the closure recomputation were performed after extraction as separate coordinator checks and are reported in the run folder `DX/`; they were not extraction inputs.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-27T21:05:38-06:00 — TASK dependency-extract UPDATE / CONSERVATIVE; accepted snapshot available; 19 ACTIVE (11 ANCHOR / 8 EXECUTION), 0 RETIRED; local checks PASS; no extraction integrity warnings.
- 2026-09-27T21:08:32-06:00 — Bounded source-extraction fidelity repair: DEP-02-02-019 RETIRED as runtime product behavior without a separately established production input; 18 ACTIVE (11 ANCHOR / 7 EXECUTION), 1 RETIRED. ID/history/source/declared sections preserved; affected checks PASS. No scope, policy or graph-cut decision.
- 2026-09-29T14:34:59Z — TASK dependency-extract (APP-V4-BASIS-ALIGN-20260928 DX-1); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (unchanged source); decomposition projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md available; +0 / refreshed 0 / retired 0; ACTIVE 18 (ANCHOR 11 / EXECUTION 7), RETIRED 1; warnings none.
- 2026-09-30T02:42:47+00:00 — TASK DX (run APP-V4-SCA002-20260929); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 18 ACTIVE (11 ANCHOR / 7 EXECUTION), 1 RETIRED; 0 added, 1 updated (016), 0 retired; warnings none; dependency closure unclaimed.
- 2026-10-04T01:14:27+00:00 — TASK DX (run APP-V4-SCA003-20261002); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (revised under SCA-V4-003); decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 23 ACTIVE (11 ANCHOR / 12 EXECUTION), 1 RETIRED; 5 added, 4 updated, 0 retired; warnings none; dependency closure unclaimed.
