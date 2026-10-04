# Dependencies: DEL-01-05 Native OAuth/sign-in, API-key and local-provider access

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
- **Register:** `Dependencies.csv` v3.1, 29 columns; 17 ACTIVE / 0 RETIRED; ACTIVE origin: 17 EXTRACTED.
- **Classes (ACTIVE):** 11 ANCHOR (1 parent + 8 scope + 2 objective), 6 EXECUTION.
- **Execution targets (ACTIVE):** 4 DELIVERABLE, 2 DOCUMENT; direction 2 DOWNSTREAM, 4 UPSTREAM; types 2 CONSTRAINT, 2 HANDOVER, 2 PREREQUISITE.
- **This run:** 1 added (017), 3 updated in place (012, 015, 016), 0 retired (none); every other ACTIVE row re-observed (LastSeen only).

| DependencyID | Class / type | Direction | Target | Closure | Status |
|---|---|---|---|---|---|
| DEP-01-05-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-01 | NOT_APPLICABLE | ACTIVE |
| DEP-01-05-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-009 | NOT_APPLICABLE | ACTIVE |
| DEP-01-05-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-010 | NOT_APPLICABLE | ACTIVE |
| DEP-01-05-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-011 | NOT_APPLICABLE | ACTIVE |
| DEP-01-05-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-012 | NOT_APPLICABLE | ACTIVE |
| DEP-01-05-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-132 | NOT_APPLICABLE | ACTIVE |
| DEP-01-05-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-133 | NOT_APPLICABLE | ACTIVE |
| DEP-01-05-008 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-149 | NOT_APPLICABLE | ACTIVE |
| DEP-01-05-009 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-150 | NOT_APPLICABLE | ACTIVE |
| DEP-01-05-010 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-002 | NOT_APPLICABLE | ACTIVE |
| DEP-01-05-011 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-004 | NOT_APPLICABLE | ACTIVE |
| DEP-01-05-012 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-01-01 | PENDING | ACTIVE |
| DEP-01-05-013 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-01-01 | PENDING | ACTIVE |
| DEP-01-05-014 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-05-01 | PENDING | ACTIVE |
| DEP-01-05-015 | EXECUTION / CONSTRAINT | UPSTREAM | OI-009 | PENDING | ACTIVE |
| DEP-01-05-016 | EXECUTION / CONSTRAINT | UPSTREAM | OI-010 | PENDING | ACTIVE |
| DEP-01-05-017 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-02 | PENDING | ACTIVE |

## Lifecycle Summary

- ACTIVE: 17; RETIRED: 0. Closure (ACTIVE): NOT_APPLICABLE 11, PENDING 6, TBD 0, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-01-05; brief: run APP-V4-SCA003-20261002 `BRIEFS.md` section "DX — dependency-extract UPDATE for the 20 registers" and the DX dispatch message (SCA-V4-003, accepted by DECISION-1 and DECISION-2; register row per `_ScopeChange/SCA-V4-003_2026-10-03_1827/Amendment_Actions.csv`, sha256 `9b7c2ce8…6d1c`); selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (brief). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (located, SHA256 `983199cc22c84398000612cd95308c840ad011d302fe31ca110a5aa97e64a70d`). Companion CSVs in the same folder (Deliverables, Packages, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE deliverable target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (brief: "from the revised ScopeOfWork text only"); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/`, MEMORY.md, _CONTEXT.md, _SEMANTIC.md and _REFERENCES.md were not read as extraction sources. Where a row carries an owner-accepted register item whose content the ScopeOfWork does not restate (ledger annotations), the row says so in Notes and names its source.
- Source ScopeOfWork.md SHA256 `2e134b572f2676ed4fe6daa892047e21e53a637f9901cba20f482a6637f7f3d3` (revised by SCA-V4-003 G-0105-01…16 (11 definitions; added REQ-010, AC-011, VER-011, matrix row, AX-006); commit 2d5e6845c5); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table (all anchor quotes verbatim after this run) before Pass 2 examined execution statements.
- Match/merge (UPDATE): all prior ACTIVE EXTRACTED rows matched by DependencyID and kept their identities; LastSeen refreshed to 2026-10-04T01:14:27+00:00. New rows take the next DEP-01-05-SEQ numbers; FirstSeen = LastSeen = run time.
- Added 1 DOWNSTREAM HANDOVER row to DEL-09-02 (R3-01-05-b; new CLM-004 sentence; existing admitted arc).
- Updated in place: DEP-01-05-015 re-quoted, TargetName/TargetLocation set to the account-home decision record and Statement refreshed (R3-01-05-c; K-1 choice level, L-7; OI-009 now RESOLVED_BY_OWNER_DECISION in Open_Issues; SatisfactionStatus kept PENDING); DEP-01-05-016 TargetLocation set to ACCESS §10 (R3-01-05-d; OI-010 open, L-6); DEP-01-05-012 Notes (R3-01-05-e).
- Not extracted: the DOWNSTREAM row to DEL-01-01 (ledger R3-01-05-a, mirror of DEP-01-01-024, held in SCC-001). The ScopeOfWork names DEL-01-01 only as owner/supplier (CLM-003, REQ-009, AC-007, AX-004 "joint scope"); no sentence states that DEL-01-01 receives sign-in or substitution evidence from this deliverable. The arc exists through DEP-01-01-024, so the arc set is unaffected. Returned to the coordinator.
- Not extracted: any row naming DEL-01-04. OUT-002 supplies the Codex account "for the person-identity element of App-captured acts" without naming a receiver; NR-07's supplier-side mirror is not proposed.
- Pre-existing and unchanged: DEP-01-05-012 and -013 share the typed key UPSTREAM/PREREQUISITE/DEL-01-01; their Notes distinguish the pin input from the embedding-qualification input.
- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged except the two owner-accepted RequiredMaturity/SatisfactionStatus normalizations named above where they apply.
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream). The human-owned prefix of this file is byte-identical.
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, every ACTIVE quote an exact substring of the current ScopeOfWork and at most 30 words, target placement). Schema validator VALID (17 rows). enum invocations=21, id invocations=24, all_ok=True.
- `validate_decomposition_registers.py projects/chirality-app-v4/execution --families EVQ,DRB` after all 20 updates: 41 registers, 929 rows, 0 ERROR, 0 WARNING.
- Warnings: none.
- Comparison with `AMENDMENT_PACKET/ARC_EFFECT.md` and the closure recomputation were performed after extraction as separate coordinator checks and are reported in the run folder `DX/`; they were not extraction inputs.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:14:23+00:00 — TASK dependency-extract; UPDATE / CONSERVATIVE; decomposition `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` available and IDs/labels validated; 16 ACTIVE (11 ANCHOR, 5 EXECUTION), 0 RETIRED; no Tree warnings; OI-009/OI-010/OI-012 and technical-input fulfilment remain unresolved.
- 2026-10-04T01:14:27+00:00 — TASK DX (run APP-V4-SCA003-20261002); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (revised under SCA-V4-003); decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 17 ACTIVE (11 ANCHOR / 6 EXECUTION), 0 RETIRED; 1 added, 3 updated, 0 retired; warnings none; dependency closure unclaimed.
