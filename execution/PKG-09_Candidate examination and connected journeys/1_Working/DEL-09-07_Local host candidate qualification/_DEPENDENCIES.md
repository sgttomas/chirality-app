# Dependencies: DEL-09-07 Local host candidate qualification

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

- **Status:** EXTRACTED (UPDATE 2026-09-29, SCA-V4-002 propagation); local checks recorded in `_run_records/dependency-extract-20260929-sca002.md`.
- **Register:** `Dependencies.csv` v3.1, 29 columns; 25 ACTIVE / 0 RETIRED; ACTIVE origin: 25 EXTRACTED.
- **Classes (ACTIVE):** 10 ANCHOR (1 parent + 5 scope + 4 objective), 15 EXECUTION.
- **Execution targets (ACTIVE):** 2 DELIVERABLE, 9 EXTERNAL, 4 PACKAGE; direction 1 DOWNSTREAM, 14 UPSTREAM; types 2 CONSTRAINT, 1 HANDOVER, 5 INTERFACE, 7 PREREQUISITE.
- **This run:** 0 added, 4 updated in place (022 and 023 re-quoted against revised TBD-002/TBD-003; 016 Notes restated per ASC-ISS-007; 020 notes), 0 retired

| DependencyID | Class / type | Direction | Target | Closure | Status |
|---|---|---|---|---|---|
| DEP-09-07-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-09 | NOT_APPLICABLE | ACTIVE |
| DEP-09-07-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-199 | NOT_APPLICABLE | ACTIVE |
| DEP-09-07-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-200 | NOT_APPLICABLE | ACTIVE |
| DEP-09-07-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-201 | NOT_APPLICABLE | ACTIVE |
| DEP-09-07-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-202 | NOT_APPLICABLE | ACTIVE |
| DEP-09-07-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-239 | NOT_APPLICABLE | ACTIVE |
| DEP-09-07-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-004 | NOT_APPLICABLE | ACTIVE |
| DEP-09-07-008 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-005 | NOT_APPLICABLE | ACTIVE |
| DEP-09-07-009 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-008 | NOT_APPLICABLE | ACTIVE |
| DEP-09-07-010 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-009 | NOT_APPLICABLE | ACTIVE |
| DEP-09-07-011 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-09-06 | TBD | ACTIVE |
| DEP-09-07-012 | EXECUTION / INTERFACE | UPSTREAM | PKG-02 | TBD | ACTIVE |
| DEP-09-07-013 | EXECUTION / INTERFACE | UPSTREAM | PKG-03 | TBD | ACTIVE |
| DEP-09-07-014 | EXECUTION / INTERFACE | UPSTREAM | PKG-04 | TBD | ACTIVE |
| DEP-09-07-015 | EXECUTION / INTERFACE | UPSTREAM | PKG-05 | TBD | ACTIVE |
| DEP-09-07-016 | EXECUTION / PREREQUISITE | UPSTREAM | DEP-001 | TBD | ACTIVE |
| DEP-09-07-017 | EXECUTION / PREREQUISITE | UPSTREAM | Actual App/SWBPIPE candidate and local-model runtime configuration | TBD | ACTIVE |
| DEP-09-07-018 | EXECUTION / PREREQUISITE | UPSTREAM | Person/engineer — scoped V4-EXM-20 row decisions | TBD | ACTIVE |
| DEP-09-07-019 | EXECUTION / PREREQUISITE | UPSTREAM | Engineer-edited model and agent checking request for V4-EXM-21 | TBD | ACTIVE |
| DEP-09-07-020 | EXECUTION / PREREQUISITE | UPSTREAM | Person-adopted per-operation autonomy policy and actual run setting | TBD | ACTIVE |
| DEP-09-07-021 | EXECUTION / PREREQUISITE | UPSTREAM | Person's actual declared workflow-checkpoint act for V4-EXM-22 | TBD | ACTIVE |
| DEP-09-07-022 | EXECUTION / CONSTRAINT | UPSTREAM | OI-001 | TBD | ACTIVE |
| DEP-09-07-023 | EXECUTION / CONSTRAINT | UPSTREAM | OI-002 | TBD | ACTIVE |
| DEP-09-07-024 | EXECUTION / INTERFACE | UPSTREAM | Independent examiner — joined local qualification dossier examination | TBD | ACTIVE |
| DEP-09-07-025 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-11-03 | TBD | ACTIVE |

## Lifecycle Summary

- ACTIVE: 25; RETIRED: 0. Closure (ACTIVE): NOT_APPLICABLE 10, PENDING 0, TBD 15, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-09-07; brief: run APP-V4-SCA002-20260929 node DX dispatch message, reusing run APP-V4-BASIS-ALIGN-20260928 `BRIEFS.md` section "DX — dependency-extract UPDATE" shared overrides; selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (both brief overrides). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (brief override; located, SHA256 `ea3388bcb05b2280d8bb10db2578aec9818f40c559b4214e1732da754d9bd7d5`). Companion CSVs in the same folder (Packages, Deliverables, ScopeLedger, Objectives, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (explicit brief override); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/` files, MEMORY.md, _CONTEXT.md and _SEMANTIC.md were not read as extraction sources. `_REFERENCES.md` was read for pointer resolution only.
- Source ScopeOfWork.md SHA256 `813ef0f3ebcbc000df3a54093f15a0cfe9b2a75c8f6bb69a6648b1eec8e0395a` (as revised under SCA-V4-002 at commit 1efd4bcda where in scope); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table before Pass 2 examined execution statements. Existing anchor TargetLocation pointers to the GROUP3 frozen snapshot are retained (the IDs are unchanged and resolve in both).
- Match/merge (UPDATE): all 25 prior EXTRACTED rows re-observed and kept ACTIVE with their DependencyIDs; LastSeen refreshed. Updated in place: DEP-09-07-022 (OI-001; Statement/TargetName/EvidenceQuote/Notes re-quoted against revised TBD-002, narrowed to matters the D2 ruling does not cover), DEP-09-07-023 (OI-002; same against revised TBD-003, narrowed to criteria outside the D3 ruling), DEP-09-07-016 (DEP-001; Notes restated against the revised SoW per ASC-ISS-007, superseding the pre-SCA-V4-001 "candidate/run/configured endpoint" sentence) and DEP-09-07-020 (Notes only). No row added. No row retired: both revised TBDs keep a residual owner-held constraint with a stated point of need, so the OI-001/OI-002 rows are re-quoted rather than retired (IMPACT §5 allows either).
- SCA-V4-002 edits to this SoW (F-0907-01 CLM-002 policy clause; F-0907-02 TBD-002; F-0907-03 TBD-003; F-0907-04 AX-005) name no deliverable that the SoW did not already name and add no consumption statement. No new arc.
- Considered, not extracted (CONSERVATIVE, information flow only): OI-021 (TBD-001; useful operation, permitted autonomy and candidate environment) remains carried through the DEL-09-06 agreement row DEP-09-07-011 as in the prior runs, not as a separate EXTERNAL row; the PKG-02/03/04/05 package-level consumption rows (012–015) remain unresolved to per-deliverable edges because CLM-003 names packages. The CLM-002 policy clause is an owner/decision-allocation statement, not an input. No row on DEL-09-06 was added or changed.
- Guards (brief): no row makes an SCC-002 member depend on DEL-09-06 and DEL-09-06 has no DOWNSTREAM row to an SCC-002 member; nothing grounds N-12 or N-B8; DEL-04-01 gains no supplier row from an SCC-002 member. Checked against this register after the run: not triggered.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged.
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream).
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, verbatim quotes <=30 words, non-placeholder SourceRefs, target placement, no duplicate typed-target keys); target IDs unresolved: none. Schema validator PASS. enum invocations=23, id invocations=43, all_ok=True
- Optional `validate_decomposition_registers.py` whole-execution EVQ/DRB scan not run per deliverable (the brief bounds reads to the deliverable and decomposition); the equivalent local EVQ-003/EVQ-004/DRB-006 conditions were checked and are absent.
- Warnings: none.
- Comparison with the run folder's `AMENDMENT_PACKET/ARC_EFFECT.md` expectations was performed after extraction as a separate coordinator check and is reported in the run-folder return `DX/DX_DEL-09-07.md`; it was not an extraction input.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:38:14+00:00 — TASK `/root/renewal_research_strategy/dep_del_09_07`; UPDATE / CONSERVATIVE; decomposition `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` present, canonical labels resolved; warnings 0; ACTIVE 25 (ANCHOR 10, EXECUTION 15), RETIRED 0; source unchanged and local checks PASS. No closure or lifecycle advancement.
- 2026-09-29T14:38:50+00:00 — TASK DX-3 (APP-V4-BASIS-ALIGN-20260928); UPDATE / CONSERVATIVE; SOURCE_DOCS=ScopeOfWork.md; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` available. Added 0, refreshed 4 (anchors DEP-09-07-004/-005 labels; DEP-09-07-016, -021), retired 0. ACTIVE=25 (ANCHOR=10; EXECUTION=15), RETIRED=0. Mandatory local checks passed; no integrity warnings.
- 2026-09-30T02:44:08+00:00 — TASK DX (run APP-V4-SCA002-20260929); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 25 ACTIVE (10 ANCHOR / 15 EXECUTION), 0 RETIRED; 0 added, 4 updated (016, 020, 022, 023), 0 retired; warnings none; dependency closure unclaimed.
