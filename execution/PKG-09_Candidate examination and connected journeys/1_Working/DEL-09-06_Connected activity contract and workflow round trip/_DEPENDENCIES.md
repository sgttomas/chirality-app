# Dependencies: DEL-09-06 Connected activity contract and workflow round trip

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
- **Register:** `Dependencies.csv` v3.1, 29 columns; 35 ACTIVE / 0 RETIRED; ACTIVE origin: 35 EXTRACTED.
- **Classes (ACTIVE):** 11 ANCHOR (1 parent + 7 scope + 3 objective), 24 EXECUTION.
- **Execution targets (ACTIVE):** 13 DELIVERABLE, 9 EXTERNAL, 2 PACKAGE; direction 2 DOWNSTREAM, 22 UPSTREAM; types 4 CONSTRAINT, 2 HANDOVER, 15 INTERFACE, 3 PREREQUISITE.
- **This run:** 1 added (035), 3 updated in place (015, 019, 027), 0 retired (none); every other ACTIVE row re-observed (LastSeen only).

| DependencyID | Class / type | Direction | Target | Closure | Status |
|---|---|---|---|---|---|
| DEP-09-06-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-09 | NOT_APPLICABLE | ACTIVE |
| DEP-09-06-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-040 | NOT_APPLICABLE | ACTIVE |
| DEP-09-06-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-041 | NOT_APPLICABLE | ACTIVE |
| DEP-09-06-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-236 | NOT_APPLICABLE | ACTIVE |
| DEP-09-06-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-237 | NOT_APPLICABLE | ACTIVE |
| DEP-09-06-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-238 | NOT_APPLICABLE | ACTIVE |
| DEP-09-06-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-240 | NOT_APPLICABLE | ACTIVE |
| DEP-09-06-008 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-241 | NOT_APPLICABLE | ACTIVE |
| DEP-09-06-009 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-001 | NOT_APPLICABLE | ACTIVE |
| DEP-09-06-010 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-004 | NOT_APPLICABLE | ACTIVE |
| DEP-09-06-011 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-008 | NOT_APPLICABLE | ACTIVE |
| DEP-09-06-012 | EXECUTION / INTERFACE | UPSTREAM | PKG-02 | TBD | ACTIVE |
| DEP-09-06-013 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-03 | TBD | ACTIVE |
| DEP-09-06-014 | EXECUTION / INTERFACE | UPSTREAM | PKG-03 | TBD | ACTIVE |
| DEP-09-06-015 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-03 | TBD | ACTIVE |
| DEP-09-06-016 | EXECUTION / INTERFACE | UPSTREAM | DEL-05-01 | TBD | ACTIVE |
| DEP-09-06-017 | EXECUTION / INTERFACE | UPSTREAM | DEL-05-02 | TBD | ACTIVE |
| DEP-09-06-018 | EXECUTION / PREREQUISITE | UPSTREAM | DEP-001 | TBD | ACTIVE |
| DEP-09-06-019 | EXECUTION / PREREQUISITE | UPSTREAM | DEP-001 | TBD | ACTIVE |
| DEP-09-06-020 | EXECUTION / HANDOVER | DOWNSTREAM | DEP-001 | TBD | ACTIVE |
| DEP-09-06-021 | EXECUTION / CONSTRAINT | UPSTREAM | OI-021 | TBD | ACTIVE |
| DEP-09-06-022 | EXECUTION / CONSTRAINT | UPSTREAM | OI-001 | TBD | ACTIVE |
| DEP-09-06-023 | EXECUTION / CONSTRAINT | UPSTREAM | OI-002 | TBD | ACTIVE |
| DEP-09-06-024 | EXECUTION / PREREQUISITE | UPSTREAM | Accountable person — actual content-bound human act in V4-EXM-14 | TBD | ACTIVE |
| DEP-09-06-025 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-01 | TBD | ACTIVE |
| DEP-09-06-026 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-02 | TBD | ACTIVE |
| DEP-09-06-027 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-01 | TBD | ACTIVE |
| DEP-09-06-028 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-02 | TBD | ACTIVE |
| DEP-09-06-029 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-03 | TBD | ACTIVE |
| DEP-09-06-030 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-01 | TBD | ACTIVE |
| DEP-09-06-031 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-02 | TBD | ACTIVE |
| DEP-09-06-032 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-01 | TBD | ACTIVE |
| DEP-09-06-033 | EXECUTION / HANDOVER | DOWNSTREAM | DEP-001 | TBD | ACTIVE |
| DEP-09-06-034 | EXECUTION / CONSTRAINT | UPSTREAM | APP-V4-SWBPIPE-INTAKE-20260928-DECISION-3 | TBD | ACTIVE |
| DEP-09-06-035 | EXECUTION / INTERFACE | UPSTREAM | DEL-09-01 | TBD | ACTIVE |

## Lifecycle Summary

- ACTIVE: 35; RETIRED: 0. Closure (ACTIVE): NOT_APPLICABLE 11, PENDING 0, TBD 24, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-09-06; brief: run APP-V4-SCA003-20261002 `BRIEFS.md` section "DX — dependency-extract UPDATE for the 20 registers" and the DX dispatch message (SCA-V4-003, accepted by DECISION-1 and DECISION-2; register row per `_ScopeChange/SCA-V4-003_2026-10-03_1827/Amendment_Actions.csv`, sha256 `9b7c2ce8…6d1c`); selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (brief). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (located, SHA256 `983199cc22c84398000612cd95308c840ad011d302fe31ca110a5aa97e64a70d`). Companion CSVs in the same folder (Deliverables, Packages, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE deliverable target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (brief: "from the revised ScopeOfWork text only"); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/`, MEMORY.md, _CONTEXT.md, _SEMANTIC.md and _REFERENCES.md were not read as extraction sources. Where a row carries an owner-accepted register item whose content the ScopeOfWork does not restate (ledger annotations), the row says so in Notes and names its source.
- Source ScopeOfWork.md SHA256 `8edc7b3cfedb7c0bf645805650bea42a6f7dddd15b87f5293189210f5cb361a3` (revised by SCA-V4-003 G-0906-01…05 (CLM-003, OUT-003, REQ-008, TBD-003, AX-005); commit 2d5e6845c5); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table (all anchor quotes verbatim after this run) before Pass 2 examined execution statements.
- Match/merge (UPDATE): all prior ACTIVE EXTRACTED rows matched by DependencyID and kept their identities; LastSeen refreshed to 2026-10-04T01:14:27+00:00. New rows take the next DEP-09-06-SEQ numbers; FirstSeen = LastSeen = run time.
- Added 1 UPSTREAM INTERFACE row to DEL-09-01 (R-0906-3; CLM-003 examination support and evidence protocol; existing admitted arc).
- Updated in place: DEP-09-06-015 RequiredMaturity TBD → INITIALIZED (R2-04-03-g, one value with DEP-04-03-031); DEP-09-06-019 Notes/SourceRef (R-0906-1, no step examinable against SWBPIPE); DEP-09-06-027 Notes (R-0906-2 accepted annotation).
- Not extracted: R-0906-4 (DROP, duplicate of R2-04-03-g). No row makes an SCC-002 member depend on this deliverable.
- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged except the two owner-accepted RequiredMaturity/SatisfactionStatus normalizations named above where they apply.
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream). The human-owned prefix of this file is byte-identical.
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, every ACTIVE quote an exact substring of the current ScopeOfWork and at most 30 words, target placement). Schema validator VALID (35 rows). enum invocations=23, id invocations=55, all_ok=True.
- `validate_decomposition_registers.py projects/chirality-app-v4/execution --families EVQ,DRB` after all 20 updates: 41 registers, 929 rows, 0 ERROR, 0 WARNING.
- Warnings: none.
- Comparison with `AMENDMENT_PACKET/ARC_EFFECT.md` and the closure recomputation were performed after extraction as separate coordinator checks and are reported in the run folder `DX/`; they were not extraction inputs.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:35:55+00:00 — UPDATE / CONSERVATIVE; accepted snapshot `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` available; warnings none; ACTIVE 24 (ANCHOR 11, EXECUTION 13), RETIRED 0; actual inputs unclaimed.
- 2026-09-28T04:24:05+00:00 — UPDATE / CONSERVATIVE, R5 only; DEP-09-06-015 target PKG-04 → DEL-04-03, accepted G3 allocation and local CLM-003 verified; ACTIVE 24 (ANCHOR 11, EXECUTION 13), RETIRED 0, local Deliverable inputs 4, Package inputs 2, EXTERNAL 7, UNKNOWN 0; warnings none; maturity, satisfaction and actual-input conditions preserved. See `_run_records/dependency-target-resolution-20260928.md`.
- 2026-09-29T14:38:50+00:00 — TASK DX-3 (APP-V4-BASIS-ALIGN-20260928); UPDATE / CONSERVATIVE; SOURCE_DOCS=ScopeOfWork.md; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` available. First stopped on the literal guard, then applied after the integrator clarified it. Added 10 (8 UPSTREAM INTERFACE deliverable rows; DEP-001 HANDOVER; DECISION-3 CONSTRAINT), refreshed 5 (016, 017, 022, 023, 024), retired 0. ACTIVE=34 (ANCHOR=11; EXECUTION=23), RETIRED=0. Mandatory local checks passed; no integrity warnings.
- 2026-10-04T01:14:27+00:00 — TASK DX (run APP-V4-SCA003-20261002); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (revised under SCA-V4-003); decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 35 ACTIVE (11 ANCHOR / 24 EXECUTION), 0 RETIRED; 1 added, 3 updated, 0 retired; warnings none; dependency closure unclaimed.
