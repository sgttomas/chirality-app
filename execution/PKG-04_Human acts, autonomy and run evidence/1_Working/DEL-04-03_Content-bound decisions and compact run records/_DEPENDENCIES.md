# Dependencies: DEL-04-03 Content-bound decisions and compact run records

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
- **Register:** `Dependencies.csv` v3.1, 29 columns; 45 ACTIVE / 0 RETIRED; ACTIVE origin: 45 EXTRACTED.
- **Classes (ACTIVE):** 10 ANCHOR (1 parent + 7 scope + 2 objective), 35 EXECUTION.
- **Execution targets (ACTIVE):** 26 DELIVERABLE, 6 EXTERNAL, 3 PACKAGE; direction 19 DOWNSTREAM, 16 UPSTREAM; types 3 CONSTRAINT, 2 HANDOVER, 30 INTERFACE.
- **This run:** 12 added (034, 035, 036, 037, 038, 039, 040, 041, 042, 043, 044, 045), 5 updated in place (019, 020, 025, 031, 033), 0 retired (none); every other ACTIVE row re-observed (LastSeen only).

| DependencyID | Class / type | Direction | Target | Closure | Status |
|---|---|---|---|---|---|
| DEP-04-03-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-04 | NOT_APPLICABLE | ACTIVE |
| DEP-04-03-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-092 | NOT_APPLICABLE | ACTIVE |
| DEP-04-03-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-093 | NOT_APPLICABLE | ACTIVE |
| DEP-04-03-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-094 | NOT_APPLICABLE | ACTIVE |
| DEP-04-03-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-095 | NOT_APPLICABLE | ACTIVE |
| DEP-04-03-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-096 | NOT_APPLICABLE | ACTIVE |
| DEP-04-03-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-143 | NOT_APPLICABLE | ACTIVE |
| DEP-04-03-008 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-186 | NOT_APPLICABLE | ACTIVE |
| DEP-04-03-009 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-004 | NOT_APPLICABLE | ACTIVE |
| DEP-04-03-010 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-005 | NOT_APPLICABLE | ACTIVE |
| DEP-04-03-011 | EXECUTION / INTERFACE | DOWNSTREAM | PKG-02 | PENDING | ACTIVE |
| DEP-04-03-012 | EXECUTION / INTERFACE | DOWNSTREAM | PKG-03 | PENDING | ACTIVE |
| DEP-04-03-013 | EXECUTION / INTERFACE | DOWNSTREAM | PKG-06 | PENDING | ACTIVE |
| DEP-04-03-014 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-04-02 | PENDING | ACTIVE |
| DEP-04-03-015 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-11 | PENDING | ACTIVE |
| DEP-04-03-016 | EXECUTION / INTERFACE | DOWNSTREAM | Responsible host implementation owner — host-agent run recording | PENDING | ACTIVE |
| DEP-04-03-017 | EXECUTION / INTERFACE | UPSTREAM | DEP-001 | PENDING | ACTIVE |
| DEP-04-03-018 | EXECUTION / INTERFACE | UPSTREAM | Supplied evidence of an actually performed human act | PENDING | ACTIVE |
| DEP-04-03-019 | EXECUTION / CONSTRAINT | UPSTREAM | Owner with affected App/SWB contract owners — OI-001/OI-002 rulings for the first increment (APP-V4-FIRST-INCREMENT-20260928-DECISION-1 D2/D3), carried by App DEL-04-01 | PENDING | ACTIVE |
| DEP-04-03-020 | EXECUTION / CONSTRAINT | UPSTREAM | Shared contract, SWB implementation and App/shared contract owners — affected implementation allocation | PENDING | ACTIVE |
| DEP-04-03-021 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-01 | PENDING | ACTIVE |
| DEP-04-03-022 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-02 | PENDING | ACTIVE |
| DEP-04-03-023 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-01 | PENDING | ACTIVE |
| DEP-04-03-024 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-02 | PENDING | ACTIVE |
| DEP-04-03-025 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-03 | PENDING | ACTIVE |
| DEP-04-03-026 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-03 | PENDING | ACTIVE |
| DEP-04-03-027 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-01 | PENDING | ACTIVE |
| DEP-04-03-028 | EXECUTION / INTERFACE | UPSTREAM | DEL-05-01 | PENDING | ACTIVE |
| DEP-04-03-029 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-05-01 | PENDING | ACTIVE |
| DEP-04-03-030 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-05-02 | PENDING | ACTIVE |
| DEP-04-03-031 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-09-06 | PENDING | ACTIVE |
| DEP-04-03-032 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-09-09 | PENDING | ACTIVE |
| DEP-04-03-033 | EXECUTION / CONSTRAINT | UPSTREAM | OI-021 | PENDING | ACTIVE |
| DEP-04-03-034 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-01 | PENDING | ACTIVE |
| DEP-04-03-035 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-02 | PENDING | ACTIVE |
| DEP-04-03-036 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-04 | PENDING | ACTIVE |
| DEP-04-03-037 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-02-01 | PENDING | ACTIVE |
| DEP-04-03-038 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-02-03 | PENDING | ACTIVE |
| DEP-04-03-039 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-03-01 | PENDING | ACTIVE |
| DEP-04-03-040 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-03-04 | PENDING | ACTIVE |
| DEP-04-03-041 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-01-04 | PENDING | ACTIVE |
| DEP-04-03-042 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-02-02 | PENDING | ACTIVE |
| DEP-04-03-043 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-09-02 | PENDING | ACTIVE |
| DEP-04-03-044 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-09-05 | PENDING | ACTIVE |
| DEP-04-03-045 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-10-03 | PENDING | ACTIVE |

## Lifecycle Summary

- ACTIVE: 45; RETIRED: 0. Closure (ACTIVE): NOT_APPLICABLE 10, PENDING 35, TBD 0, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-04-03; brief: run APP-V4-SCA003-20261002 `BRIEFS.md` section "DX — dependency-extract UPDATE for the 20 registers" and the DX dispatch message (SCA-V4-003, accepted by DECISION-1 and DECISION-2; register row per `_ScopeChange/SCA-V4-003_2026-10-03_1827/Amendment_Actions.csv`, sha256 `9b7c2ce8…6d1c`); selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (brief). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (located, SHA256 `983199cc22c84398000612cd95308c840ad011d302fe31ca110a5aa97e64a70d`). Companion CSVs in the same folder (Deliverables, Packages, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE deliverable target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (brief: "from the revised ScopeOfWork text only"); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/`, MEMORY.md, _CONTEXT.md, _SEMANTIC.md and _REFERENCES.md were not read as extraction sources. Where a row carries an owner-accepted register item whose content the ScopeOfWork does not restate (ledger annotations), the row says so in Notes and names its source.
- Source ScopeOfWork.md SHA256 `b8b58d674e3ac2d86c53005951ca7182dcdeb810964901191afe14cec07afc66` (revised by SCA-V4-003 G-0403-01…06 (CLM-004, REQ-003, REQ-005, AX-005); commit 2d5e6845c5); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table (all anchor quotes verbatim after this run) before Pass 2 examined execution statements.
- Match/merge (UPDATE): all prior ACTIVE EXTRACTED rows matched by DependencyID and kept their identities; LastSeen refreshed to 2026-10-04T01:14:27+00:00. New rows take the next DEP-04-03-SEQ numbers; FirstSeen = LastSeen = run time.
- Added 3 UPSTREAM INTERFACE rows in the revised CLM-004 receives clause: DEL-02-01 (R2-04-03-e, new held arc K-8), DEL-02-02 (R20-10, new held arc) and DEL-02-04 (R22-7-reg, existing held arc).
- Added 9 DOWNSTREAM INTERFACE rows from the revised REQ-005: DEL-02-01, 02-03, 03-01, 03-04 (R2-04-03-a…d) and DEL-01-04, 02-02, 09-02, 09-05, 10-03 (RP1-MX-0403). The package rows DEP-04-03-011/-012 stay.
- Updated in place: DEP-04-03-025 Statement and quote (R2-04-03-f); DEP-04-03-031 noted for R2-04-03-g (stays INITIALIZED; DEP-09-06-015 set to INITIALIZED); SourceRef line numbers of DEP-04-03-019, -020, -033 (TBD lines moved by AX-005).
- R2-04-03-h: the earlier Run Notes label "DEP-04-03-031 (DEL-09-06 consuming this record contract, N-08, …)" is corrected: N-08 is DEL-09-06 → DEL-04-02; DEP-04-03-031 lies on the arc of DEP-09-06-015 (DEL-09-06 consuming this record contract).
- Not extracted: DEL-11-02's counterpart for DEP-02-04-013 (R22-7-open, DEFER). No UPSTREAM row to DEL-09-06; no DOWNSTREAM row to DEL-03-02 or DEL-03-03 is needed by the text (N-12 and N-B8 concern those deliverables consuming this one and stay absent).
- Guards (brief; SOW_REVISIONS_A/B "Extraction guards"; Handoff_State next-workflow row; ARC_EFFECT §3), checked graph-wide after the run: R17-10 holds (DEL-01-02 reaches only DEL-01-01, DEL-01-05, DEL-04-01; DEL-01-03 those and DEL-01-02); DEL-04-01 has no supplier; no SCC-002 member depends on DEL-09-06; N-12, N-B8, NR-03, NR-06 and NR-10 are absent; nothing names DEL-11-02.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged except the two owner-accepted RequiredMaturity/SatisfactionStatus normalizations named above where they apply.
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream). The human-owned prefix of this file is byte-identical.
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, every ACTIVE quote an exact substring of the current ScopeOfWork and at most 30 words, target placement). Schema validator VALID (45 rows). enum invocations=22, id invocations=74, all_ok=True.
- `validate_decomposition_registers.py projects/chirality-app-v4/execution --families EVQ,DRB` after all 20 updates: 41 registers, 929 rows, 0 ERROR, 0 WARNING.
- Warnings: none.
- Comparison with `AMENDMENT_PACKET/ARC_EFFECT.md` and the closure recomputation were performed after extraction as separate coordinator checks and are reported in the run folder `DX/`; they were not extraction inputs.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:26:48+00:00 — TASK dependency-extract; UPDATE / CONSERVATIVE; accepted Group3 decomposition resolved at `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md`. ACTIVE 20 (ANCHOR 10, EXECUTION 10); no integrity warnings; conditional/external input limitations retained.
- 2026-09-29T14:34:59Z — TASK dependency-extract (APP-V4-BASIS-ALIGN-20260928 DX-1); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (revised under SCA-V4-001); decomposition projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md available; +13 / refreshed 2 / retired 0; ACTIVE 33 (ANCHOR 10 / EXECUTION 23), RETIRED 0; warnings none.
- 2026-09-30T02:46:53+00:00 — TASK DX (run APP-V4-SCA002-20260929); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 33 ACTIVE (10 ANCHOR / 23 EXECUTION), 0 RETIRED; 0 added, 13 updated (re-quoted: 019, 021–032), 0 retired; warnings none; dependency closure unclaimed.
- 2026-10-04T01:14:27+00:00 — TASK DX (run APP-V4-SCA003-20261002); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (revised under SCA-V4-003); decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 45 ACTIVE (10 ANCHOR / 35 EXECUTION), 0 RETIRED; 12 added, 5 updated, 0 retired; warnings none; dependency closure unclaimed.
