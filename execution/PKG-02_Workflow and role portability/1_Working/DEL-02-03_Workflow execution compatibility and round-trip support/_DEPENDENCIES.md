# Dependencies: DEL-02-03 Workflow execution compatibility and round-trip support

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
- **Register:** `Dependencies.csv` v3.1, 29 columns; 38 ACTIVE / 2 RETIRED; ACTIVE origin: 38 EXTRACTED.
- **Classes (ACTIVE):** 8 ANCHOR (1 parent + 5 scope + 2 objective), 30 EXECUTION.
- **Execution targets (ACTIVE):** 24 DELIVERABLE, 6 EXTERNAL; direction 12 DOWNSTREAM, 18 UPSTREAM; types 5 CONSTRAINT, 12 HANDOVER, 12 INTERFACE, 1 PREREQUISITE.
- **This run:** 13 added (028, 029, 030, 031, 032, 033, 034, 035, 036, 037, 038, 039, 040), 4 updated in place (003, 010, 025, 027), 0 retired (none); every other ACTIVE row re-observed (LastSeen only).

| DependencyID | Class / type | Direction | Target | Closure | Status |
|---|---|---|---|---|---|
| DEP-02-03-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-02 | NOT_APPLICABLE | ACTIVE |
| DEP-02-03-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-051 | NOT_APPLICABLE | ACTIVE |
| DEP-02-03-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-052 | NOT_APPLICABLE | ACTIVE |
| DEP-02-03-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-053 | NOT_APPLICABLE | ACTIVE |
| DEP-02-03-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-054 | NOT_APPLICABLE | ACTIVE |
| DEP-02-03-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-055 | NOT_APPLICABLE | ACTIVE |
| DEP-02-03-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-003 | NOT_APPLICABLE | ACTIVE |
| DEP-02-03-008 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-005 | NOT_APPLICABLE | ACTIVE |
| DEP-02-03-009 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-01 | TBD | ACTIVE |
| DEP-02-03-010 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-02 | TBD | ACTIVE |
| DEP-02-03-011 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-01 | TBD | ACTIVE |
| DEP-02-03-012 | EXECUTION / CONSTRAINT | UPSTREAM | DEL-04-01 | TBD | ACTIVE |
| DEP-02-03-013 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-03 | TBD | ACTIVE |
| DEP-02-03-014 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-06 | TBD | ACTIVE |
| DEP-02-03-015 | EXECUTION / CONSTRAINT | UPSTREAM | OI-001 | TBD | RETIRED |
| DEP-02-03-016 | EXECUTION / CONSTRAINT | UPSTREAM | OI-002 | TBD | RETIRED |
| DEP-02-03-017 | EXECUTION / CONSTRAINT | UPSTREAM | OI-013 | TBD | ACTIVE |
| DEP-02-03-018 | EXECUTION / CONSTRAINT | UPSTREAM | OI-014 | TBD | ACTIVE |
| DEP-02-03-019 | EXECUTION / CONSTRAINT | UPSTREAM | OI-021 | TBD | ACTIVE |
| DEP-02-03-020 | EXECUTION / INTERFACE | UPSTREAM | DEP-001 | TBD | ACTIVE |
| DEP-02-03-021 | EXECUTION / PREREQUISITE | UPSTREAM | Human checkpoint actor and separate recorder — positive fixture evidence | TBD | ACTIVE |
| DEP-02-03-022 | EXECUTION / INTERFACE | UPSTREAM | DEL-05-01 | TBD | ACTIVE |
| DEP-02-03-023 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-01 | TBD | ACTIVE |
| DEP-02-03-024 | EXECUTION / CONSTRAINT | UPSTREAM | Owner — governance-phase enforced-checkpoint decision (TBD-006) | TBD | ACTIVE |
| DEP-02-03-025 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-02 | TBD | ACTIVE |
| DEP-02-03-026 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-03 | TBD | ACTIVE |
| DEP-02-03-027 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-04 | TBD | ACTIVE |
| DEP-02-03-028 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-02 | TBD | ACTIVE |
| DEP-02-03-029 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-02 | TBD | ACTIVE |
| DEP-02-03-030 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-01 | TBD | ACTIVE |
| DEP-02-03-031 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-02 | TBD | ACTIVE |
| DEP-02-03-032 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-03 | TBD | ACTIVE |
| DEP-02-03-033 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-04 | TBD | ACTIVE |
| DEP-02-03-034 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-04-02 | TBD | ACTIVE |
| DEP-02-03-035 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-04-03 | TBD | ACTIVE |
| DEP-02-03-036 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-05-01 | TBD | ACTIVE |
| DEP-02-03-037 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-05-02 | TBD | ACTIVE |
| DEP-02-03-038 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-02 | TBD | ACTIVE |
| DEP-02-03-039 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-09 | TBD | ACTIVE |
| DEP-02-03-040 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-10-03 | TBD | ACTIVE |

## Lifecycle Summary

- ACTIVE: 38; RETIRED: 2. Closure (ACTIVE): NOT_APPLICABLE 8, PENDING 0, TBD 30, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-02-03; brief: run APP-V4-SCA003-20261002 `BRIEFS.md` section "DX — dependency-extract UPDATE for the 20 registers" and the DX dispatch message (SCA-V4-003, accepted by DECISION-1 and DECISION-2; register row per `_ScopeChange/SCA-V4-003_2026-10-03_1827/Amendment_Actions.csv`, sha256 `9b7c2ce8…6d1c`); selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (brief). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (located, SHA256 `983199cc22c84398000612cd95308c840ad011d302fe31ca110a5aa97e64a70d`). Companion CSVs in the same folder (Deliverables, Packages, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE deliverable target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (brief: "from the revised ScopeOfWork text only"); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/`, MEMORY.md, _CONTEXT.md, _SEMANTIC.md and _REFERENCES.md were not read as extraction sources. Where a row carries an owner-accepted register item whose content the ScopeOfWork does not restate (ledger annotations), the row says so in Notes and names its source.
- Source ScopeOfWork.md SHA256 `625b299ec1d48de1b80dff74796774cc95ee466870bec06a196e16b840af6e5f` (revised by SCA-V4-003 G-0203-01…13 (Purpose first sentence, SOW-052 row, CLM-002, CLM-003, REQ-002, REQ-007, AC-002, VER-002, VER-006, TBD-006, AX-006); commit 2d5e6845c5); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table (all anchor quotes verbatim after this run) before Pass 2 examined execution statements.
- Match/merge (UPDATE): all prior ACTIVE EXTRACTED rows matched by DependencyID and kept their identities; LastSeen refreshed to 2026-10-04T01:14:27+00:00. New rows take the next DEP-02-03-SEQ numbers; FirstSeen = LastSeen = run time.
- Added 2 UPSTREAM INTERFACE rows in the CLM-002 consumption list: DEL-01-02 (NR-01, new admitted arc) and DEL-04-02 (R2-02-03-a, existing held arc).
- Added 11 DOWNSTREAM HANDOVER rows from the new CLM-003 receivers sentence (DEL-02-01, 02-02, 03-03, 03-04, 04-02, 04-03, 05-01, 05-02, 09-02, 09-09, 10-03): R2-02-03-b…i (8) and RP1-MX-0203 (3). DEL-09-06, also named, already has DEP-02-03-014.
- Updated in place: DEP-02-03-027 Statement and quote (R2-02-03-j; K1-4); DEP-02-03-025 re-quoted (clause unchanged, sentence opening moved); DEP-02-03-003 anchor re-quoted (SOW-052 row reworded; ScopeLedger unchanged); DEP-02-03-010 Statement (SC3-02-02-9, a paired register action grounded by DEL-02-02's revised CLM-003; this SoW does not restate the run-start text, noted in the row).
- Not extracted: any row making this deliverable depend on DEL-09-06 (guard); DEL-09-06 appears only as a receiver.
- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged except the two owner-accepted RequiredMaturity/SatisfactionStatus normalizations named above where they apply.
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream). The human-owned prefix of this file is byte-identical.
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, every ACTIVE quote an exact substring of the current ScopeOfWork and at most 30 words, target placement). Schema validator VALID (40 rows). enum invocations=25, id invocations=66, all_ok=True.
- `validate_decomposition_registers.py projects/chirality-app-v4/execution --families EVQ,DRB` after all 20 updates: 41 registers, 929 rows, 0 ERROR, 0 WARNING.
- Warnings: none.
- Comparison with `AMENDMENT_PACKET/ARC_EFFECT.md` and the closure recomputation were performed after extraction as separate coordinator checks and are reported in the run folder `DX/`; they were not extraction inputs.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:18:01+00:00 — TASK dependency-extract; UPDATE / CONSERVATIVE; accepted decomposition `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` resolved; 21 ACTIVE (8 ANCHOR, 13 EXECUTION), 0 RETIRED; no local integrity warnings; execution satisfaction remains TBD.
- 2026-09-29T14:38:40+00:00 — TASK DX-2 (run APP-V4-BASIS-ALIGN-20260928); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 22 ACTIVE (8 ANCHOR / 14 EXECUTION), 2 RETIRED; 3 added (DEL-05-01, DEL-01-01, TBD-006 owner decision), 2 updated in place (003, 012), 2 retired (015 OI-001, 016 OI-002); warnings none; dependency closure unclaimed.
- 2026-09-30T02:35:46+00:00 — TASK DX (run APP-V4-SCA002-20260929); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 25 ACTIVE (8 ANCHOR / 17 EXECUTION), 2 RETIRED; 3 added (DEL-03-02, DEL-03-03, DEL-01-04), 0 updated, 0 retired; warnings none; dependency closure unclaimed.
- 2026-10-04T01:14:27+00:00 — TASK DX (run APP-V4-SCA003-20261002); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (revised under SCA-V4-003); decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 38 ACTIVE (8 ANCHOR / 30 EXECUTION), 2 RETIRED; 13 added, 4 updated, 0 retired; warnings none; dependency closure unclaimed.
