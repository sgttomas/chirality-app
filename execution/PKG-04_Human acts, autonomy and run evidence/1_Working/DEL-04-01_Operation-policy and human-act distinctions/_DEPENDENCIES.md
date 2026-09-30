# Dependencies: DEL-04-01 Operation-policy and human-act distinctions

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
- **Register:** `Dependencies.csv` v3.1, 29 columns; 29 ACTIVE / 0 RETIRED; ACTIVE origin: 29 EXTRACTED.
- **Classes (ACTIVE):** 11 ANCHOR (1 parent + 8 scope + 2 objective), 18 EXECUTION.
- **Execution targets (ACTIVE):** 11 DELIVERABLE, 7 EXTERNAL; direction 11 DOWNSTREAM, 7 UPSTREAM; types 4 CONSTRAINT, 11 HANDOVER, 3 PREREQUISITE.
- **This run:** 0 added, 9 updated in place (re-quoted exactly per ASC-ISS-008: 017, 018, 022–027, 029), 0 retired

| DependencyID | Class / type | Direction | Target | Closure | Status |
|---|---|---|---|---|---|
| DEP-04-01-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-04 | NOT_APPLICABLE | ACTIVE |
| DEP-04-01-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-074 | NOT_APPLICABLE | ACTIVE |
| DEP-04-01-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-079 | NOT_APPLICABLE | ACTIVE |
| DEP-04-01-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-082 | NOT_APPLICABLE | ACTIVE |
| DEP-04-01-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-179 | NOT_APPLICABLE | ACTIVE |
| DEP-04-01-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-180 | NOT_APPLICABLE | ACTIVE |
| DEP-04-01-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-181 | NOT_APPLICABLE | ACTIVE |
| DEP-04-01-008 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-182 | NOT_APPLICABLE | ACTIVE |
| DEP-04-01-009 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-235 | NOT_APPLICABLE | ACTIVE |
| DEP-04-01-010 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-004 | NOT_APPLICABLE | ACTIVE |
| DEP-04-01-011 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-005 | NOT_APPLICABLE | ACTIVE |
| DEP-04-01-012 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-01 | TBD | ACTIVE |
| DEP-04-01-013 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-03 | TBD | ACTIVE |
| DEP-04-01-014 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-01 | TBD | ACTIVE |
| DEP-04-01-015 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-04-02 | TBD | ACTIVE |
| DEP-04-01-016 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-04-03 | TBD | ACTIVE |
| DEP-04-01-017 | EXECUTION / CONSTRAINT | UPSTREAM | OI-001 | TBD | ACTIVE |
| DEP-04-01-018 | EXECUTION / CONSTRAINT | UPSTREAM | OI-002 | TBD | ACTIVE |
| DEP-04-01-019 | EXECUTION / PREREQUISITE | UPSTREAM | projects/chirality-app-v4/execution/_Decomposition/External_Dependencies.csv#DEP-001 | TBD | ACTIVE |
| DEP-04-01-020 | EXECUTION / PREREQUISITE | UPSTREAM | Person setting operation/consequence scope — recorded grant | TBD | ACTIVE |
| DEP-04-01-021 | EXECUTION / PREREQUISITE | UPSTREAM | Person performing the human act — attributable evidence for faithful-recording case | TBD | ACTIVE |
| DEP-04-01-022 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-02 | TBD | ACTIVE |
| DEP-04-01-023 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-03 | TBD | ACTIVE |
| DEP-04-01-024 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-04 | TBD | ACTIVE |
| DEP-04-01-025 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-05-01 | TBD | ACTIVE |
| DEP-04-01-026 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-05-02 | TBD | ACTIVE |
| DEP-04-01-027 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-09 | TBD | ACTIVE |
| DEP-04-01-028 | EXECUTION / CONSTRAINT | UPSTREAM | OI-021 | TBD | ACTIVE |
| DEP-04-01-029 | EXECUTION / CONSTRAINT | UPSTREAM | APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4 | TBD | ACTIVE |

## Lifecycle Summary

- ACTIVE: 29; RETIRED: 0. Closure (ACTIVE): NOT_APPLICABLE 11, PENDING 0, TBD 18, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-04-01; brief: run APP-V4-SCA002-20260929 node DX dispatch message, reusing run APP-V4-BASIS-ALIGN-20260928 `BRIEFS.md` section "DX — dependency-extract UPDATE" shared overrides; selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (both brief overrides). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (brief override; located, SHA256 `ea3388bcb05b2280d8bb10db2578aec9818f40c559b4214e1732da754d9bd7d5`). Companion CSVs in the same folder (Packages, Deliverables, ScopeLedger, Objectives, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (explicit brief override); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/` files, MEMORY.md, _CONTEXT.md and _SEMANTIC.md were not read as extraction sources. `_REFERENCES.md` was read for pointer resolution only.
- Source ScopeOfWork.md SHA256 `ac043e54e396f9155e3d1b02d61ca7333350a812c7db3d5bb26c80d6fc3bb875` (as revised under SCA-V4-002 at commit 1efd4bcda where in scope); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table before Pass 2 examined execution statements. Existing anchor TargetLocation pointers to the GROUP3 frozen snapshot are retained (the IDs are unchanged and resolve in both).
- Source status: ScopeOfWork.md is unchanged since SCA-V4-001 (commit 340ecf341; not in the SCA-V4-002 revision set). The full source was re-read and every ACTIVE row re-checked against it.
- Match/merge (UPDATE): all 29 prior EXTRACTED rows re-observed and kept ACTIVE with their DependencyIDs; LastSeen refreshed. No row added. No row retired.
- Re-quoted exactly (ASC-ISS-008; V12 F1), EvidenceQuote and Notes only: DEP-04-01-017, -018, -022, -023, -024, -025, -026, -027, -029 (inline-code backticks restored, for example App v4 `DEL-03-02`). All 9 are now exact substrings of the SoW and at most 30 words. No identity, direction, type, target, maturity or closure change; no arc change.
- Guard (brief): DEL-04-01 gains no supplier row from an SCC-002 member. After the run this register has no ACTIVE UPSTREAM row with a DELIVERABLE target (its inputs are EXTERNAL: OI-001/OI-002 rulings, OI-021, DEP-001, the person's grant and act, the governance-layer decision); DEL-04-01 keeps 0 deliverable suppliers.
- Considered, not extracted (CONSERVATIVE, information flow only): as in the prior run, the CLM-002 supply sentences carry the DOWNSTREAM handovers (012–016, 022–027); ownership/exclusion lists alone create no edges; no consumption statement names any deliverable as a supplier to DEL-04-01.
- Guards (brief): no row makes an SCC-002 member depend on DEL-09-06 and DEL-09-06 has no DOWNSTREAM row to an SCC-002 member; nothing grounds N-12 or N-B8; DEL-04-01 gains no supplier row from an SCC-002 member. Checked against this register after the run: not triggered.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged.
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream).
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, verbatim quotes <=30 words, non-placeholder SourceRefs, target placement, no duplicate typed-target keys); target IDs unresolved: none. Schema validator PASS. enum invocations=21, id invocations=56, all_ok=True
- Optional `validate_decomposition_registers.py` whole-execution EVQ/DRB scan not run per deliverable (the brief bounds reads to the deliverable and decomposition); the equivalent local EVQ-003/EVQ-004/DRB-006 conditions were checked and are absent.
- Warnings: none.
- Comparison with the run folder's `AMENDMENT_PACKET/ARC_EFFECT.md` expectations was performed after extraction as a separate coordinator check and is reported in the run-folder return `DX/DX_DEL-04-01.md`; it was not an extraction input.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:25:20Z — TASK dependency-extract; UPDATE / CONSERVATIVE; decomposition projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md available; ACTIVE 21 (ANCHOR 11 / EXECUTION 10), RETIRED 0; structural warnings none; external/point-of-need inputs remain unassessed.
- 2026-09-29T14:34:59Z — TASK dependency-extract (APP-V4-BASIS-ALIGN-20260928 DX-1); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (revised under SCA-V4-001); decomposition projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md available; +8 / refreshed 2 / retired 0; ACTIVE 29 (ANCHOR 11 / EXECUTION 18), RETIRED 0; warnings none.
- 2026-09-30T02:46:02+00:00 — TASK DX (run APP-V4-SCA002-20260929); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 29 ACTIVE (11 ANCHOR / 18 EXECUTION), 0 RETIRED; 0 added, 9 updated (re-quoted: 017, 018, 022–027, 029), 0 retired; warnings none; dependency closure unclaimed.
