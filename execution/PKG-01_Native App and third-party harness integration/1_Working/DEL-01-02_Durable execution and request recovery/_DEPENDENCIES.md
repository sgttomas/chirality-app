# Dependencies: DEL-01-02 Durable execution and request recovery

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
- **Register:** `Dependencies.csv` v3.1, 29 columns; 26 ACTIVE / 0 RETIRED; ACTIVE origin: 26 EXTRACTED.
- **Classes (ACTIVE):** 17 ANCHOR (1 parent + 13 scope + 3 objective), 9 EXECUTION.
- **Execution targets (ACTIVE):** 9 DELIVERABLE; direction 7 DOWNSTREAM, 2 UPSTREAM; types 1 CONSTRAINT, 2 HANDOVER, 6 INTERFACE.
- **This run:** 5 added (022, 023, 024, 025, 026), 3 updated in place (018, 020, 021), 0 retired (none); every other ACTIVE row re-observed (LastSeen only).

| DependencyID | Class / type | Direction | Target | Closure | Status |
|---|---|---|---|---|---|
| DEP-01-02-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-01 | NOT_APPLICABLE | ACTIVE |
| DEP-01-02-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-007 | NOT_APPLICABLE | ACTIVE |
| DEP-01-02-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-008 | NOT_APPLICABLE | ACTIVE |
| DEP-01-02-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-060 | NOT_APPLICABLE | ACTIVE |
| DEP-01-02-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-061 | NOT_APPLICABLE | ACTIVE |
| DEP-01-02-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-062 | NOT_APPLICABLE | ACTIVE |
| DEP-01-02-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-063 | NOT_APPLICABLE | ACTIVE |
| DEP-01-02-008 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-064 | NOT_APPLICABLE | ACTIVE |
| DEP-01-02-009 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-065 | NOT_APPLICABLE | ACTIVE |
| DEP-01-02-010 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-066 | NOT_APPLICABLE | ACTIVE |
| DEP-01-02-011 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-122 | NOT_APPLICABLE | ACTIVE |
| DEP-01-02-012 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-123 | NOT_APPLICABLE | ACTIVE |
| DEP-01-02-013 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-124 | NOT_APPLICABLE | ACTIVE |
| DEP-01-02-014 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-125 | NOT_APPLICABLE | ACTIVE |
| DEP-01-02-015 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-001 | NOT_APPLICABLE | ACTIVE |
| DEP-01-02-016 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-002 | NOT_APPLICABLE | ACTIVE |
| DEP-01-02-017 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-005 | NOT_APPLICABLE | ACTIVE |
| DEP-01-02-018 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-01 | TBD | ACTIVE |
| DEP-01-02-019 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-01-04 | TBD | ACTIVE |
| DEP-01-02-020 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-04-03 | TBD | ACTIVE |
| DEP-01-02-021 | EXECUTION / CONSTRAINT | UPSTREAM | DEL-04-01 | TBD | ACTIVE |
| DEP-01-02-022 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-01-03 | TBD | ACTIVE |
| DEP-01-02-023 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-02 | TBD | ACTIVE |
| DEP-01-02-024 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-02-03 | TBD | ACTIVE |
| DEP-01-02-025 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-03-03 | TBD | ACTIVE |
| DEP-01-02-026 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-02-02 | TBD | ACTIVE |

## Lifecycle Summary

- ACTIVE: 26; RETIRED: 0. Closure (ACTIVE): NOT_APPLICABLE 17, PENDING 0, TBD 9, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-01-02; brief: run APP-V4-SCA003-20261002 `BRIEFS.md` section "DX — dependency-extract UPDATE for the 20 registers" and the DX dispatch message (SCA-V4-003, accepted by DECISION-1 and DECISION-2; register row per `_ScopeChange/SCA-V4-003_2026-10-03_1827/Amendment_Actions.csv`, sha256 `9b7c2ce8…6d1c`); selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (brief). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (located, SHA256 `983199cc22c84398000612cd95308c840ad011d302fe31ca110a5aa97e64a70d`). Companion CSVs in the same folder (Deliverables, Packages, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE deliverable target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (brief: "from the revised ScopeOfWork text only"); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/`, MEMORY.md, _CONTEXT.md, _SEMANTIC.md and _REFERENCES.md were not read as extraction sources. Where a row carries an owner-accepted register item whose content the ScopeOfWork does not restate (ledger annotations), the row says so in Notes and names its source.
- Source ScopeOfWork.md SHA256 `6c62de1d749022a388d9a2c466655a35e06b0b9fa7779a7912f9df4424226a07` (revised by SCA-V4-003 G-0102-01…18 (16 definitions and AX-004); commit 2d5e6845c5); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table (all anchor quotes verbatim after this run) before Pass 2 examined execution statements.
- Match/merge (UPDATE): all prior ACTIVE EXTRACTED rows matched by DependencyID and kept their identities; LastSeen refreshed to 2026-10-04T01:14:27+00:00. New rows take the next DEP-01-02-SEQ numbers; FirstSeen = LastSeen = run time.
- Added 5 DOWNSTREAM rows from the revised CLM-001 interfaces sentence: DEL-01-03 (R3-01-02-a) and DEL-09-02 (R3-01-02-b) on existing admitted arcs; DEL-02-03, DEL-03-03 and DEL-02-02, the supplier-side mirrors of the new admitted arcs NR-01, NR-02 and NR-04 (R3-01-02-e, -f, -h).
- Updated in place: DEP-01-02-021 Statement/SourceRef (R3-01-02-c; D2/D3 for this scope, OI-001/OI-002 open beyond it); DEP-01-02-018 Notes (R3-01-02-d; D4 definition pin, qualification pin open); DEP-01-02-020 Notes (OUT-004/REQ-006 narrow the handoff to this slice's own custody observations).
- Not extracted: any UPSTREAM row to DEL-01-04, DEL-02-02, DEL-02-03, DEL-04-02, DEL-04-03 or DEL-06-01 (R17-10; the revised text names them only as receivers or owners); any row to DEL-09-09 (NR-03 dropped; R3-01-02-g DROP).
- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged except the two owner-accepted RequiredMaturity/SatisfactionStatus normalizations named above where they apply.
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream). The human-owned prefix of this file is byte-identical.
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, every ACTIVE quote an exact substring of the current ScopeOfWork and at most 30 words, target placement). Schema validator VALID (26 rows). enum invocations=20, id invocations=41, all_ok=True.
- `validate_decomposition_registers.py projects/chirality-app-v4/execution --families EVQ,DRB` after all 20 updates: 41 registers, 929 rows, 0 ERROR, 0 WARNING.
- Warnings: none.
- Comparison with `AMENDMENT_PACKET/ARC_EFFECT.md` and the closure recomputation were performed after extraction as separate coordinator checks and are reported in the run folder `DX/`; they were not extraction inputs.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:11:19Z — TASK /root/renewal_research_strategy/dep_del_01_02; UPDATE / CONSERVATIVE; decomposition `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` available; 21 ACTIVE (17 ANCHOR, 4 EXECUTION), 0 RETIRED; integrity warnings none; actual fulfilment unclaimed.
- 2026-10-04T01:14:27+00:00 — TASK DX (run APP-V4-SCA003-20261002); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (revised under SCA-V4-003); decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 26 ACTIVE (17 ANCHOR / 9 EXECUTION), 0 RETIRED; 5 added, 3 updated, 0 retired; warnings none; dependency closure unclaimed.
