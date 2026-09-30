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

- **Status:** EXTRACTED (UPDATE 2026-09-29, SCA-V4-002 propagation); local checks recorded in `_run_records/dependency-extract-20260929-sca002.md`.
- **Register:** `Dependencies.csv` v3.1, 29 columns; 25 ACTIVE / 2 RETIRED; ACTIVE origin: 25 EXTRACTED.
- **Classes (ACTIVE):** 8 ANCHOR (1 parent + 5 scope + 2 objective), 17 EXECUTION.
- **Execution targets (ACTIVE):** 11 DELIVERABLE, 6 EXTERNAL; direction 1 DOWNSTREAM, 16 UPSTREAM; types 5 CONSTRAINT, 1 HANDOVER, 10 INTERFACE, 1 PREREQUISITE.
- **This run:** 3 added (DEL-03-02, DEL-03-03, DEL-01-04; CLM-002 consumption sentence), 0 updated in place, 0 retired

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

## Lifecycle Summary

- ACTIVE: 25; RETIRED: 2. Closure (ACTIVE): NOT_APPLICABLE 8, PENDING 0, TBD 17, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-02-03; brief: run APP-V4-SCA002-20260929 node DX dispatch message, reusing run APP-V4-BASIS-ALIGN-20260928 `BRIEFS.md` section "DX — dependency-extract UPDATE" shared overrides; selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (both brief overrides). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (brief override; located, SHA256 `ea3388bcb05b2280d8bb10db2578aec9818f40c559b4214e1732da754d9bd7d5`). Companion CSVs in the same folder (Packages, Deliverables, ScopeLedger, Objectives, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (explicit brief override); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/` files, MEMORY.md, _CONTEXT.md and _SEMANTIC.md were not read as extraction sources. `_REFERENCES.md` was read for pointer resolution only.
- Source ScopeOfWork.md SHA256 `0006521b9bd96ea7ec98ecc5d9e6db794ecb331440c276006b444e7ee319726d` (as revised under SCA-V4-002 at commit 1efd4bcda where in scope); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table before Pass 2 examined execution statements. Existing anchor TargetLocation pointers to the GROUP3 frozen snapshot are retained (the IDs are unchanged and resolve in both).
- Match/merge (UPDATE): all 22 prior ACTIVE EXTRACTED rows re-observed with verbatim evidence and kept ACTIVE with their DependencyIDs; LastSeen refreshed; the 2 RETIRED rows (015, 016; retired_by=source_revised under SCA-V4-001) remain RETIRED unchanged. No field of a prior row changed. No row retired by this run.
- Added from the CLM-002 sentence appended by SCA-V4-002 F-0203-01 ("This slice consumes, and does not define: ..."): DEP-02-03-025 UPSTREAM INTERFACE DEL-03-02 (per-item dispositions, item-left events, all-items-decided indication, change-item content identities, applied outcomes with resulting objects; checkpoint recording and interrupted/replayed history); DEP-02-03-026 UPSTREAM INTERFACE DEL-03-03 (observations of checkpoint arrivals and act records on the external channel, which this slice records); DEP-02-03-027 UPSTREAM INTERFACE DEL-01-04 (App act control and person identity, for the App-side positive capture fixtures OUT-003/VER-003 only). All EXPLICIT/HIGH. The new AX-005 line names no deliverable and yields no row.
- Considered, not extracted (CONSERVATIVE, information flow only): the pre-existing CLM-002 ownership clauses (DEL-03-02 owns proposal item dispositions etc.; DEL-03-03 owns external-channel receiving including the governance-phase carriage assurance; DEL-01-04 constructs the App act control; DEL-04-02 owns grant display states) alone remain non-edges; the three new edges rest on the appended consumption sentence. DEL-04-02 has no consumption statement here (its supplier-side rows DEP-04-02-023 carry arc N-07). The governance-phase carriage assurance and hold-support inputs are not current-phase inputs and are not extracted. The SWBPIPE relay SQ-02 answer is an input to the future TBD-006 decision, not to this deliverable.
- Guards (brief): no row makes an SCC-002 member depend on DEL-09-06 and DEL-09-06 has no DOWNSTREAM row to an SCC-002 member; nothing grounds N-12 or N-B8; DEL-04-01 gains no supplier row from an SCC-002 member. Checked against this register after the run: not triggered.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged.
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream).
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, verbatim quotes <=30 words, non-placeholder SourceRefs, target placement, no duplicate typed-target keys); target IDs unresolved: none. Schema validator PASS. enum invocations=25, id invocations=52, all_ok=True
- Optional `validate_decomposition_registers.py` whole-execution EVQ/DRB scan not run per deliverable (the brief bounds reads to the deliverable and decomposition); the equivalent local EVQ-003/EVQ-004/DRB-006 conditions were checked and are absent.
- Warnings: none.
- Comparison with the run folder's `AMENDMENT_PACKET/ARC_EFFECT.md` expectations was performed after extraction as a separate coordinator check and is reported in the run-folder return `DX/DX_DEL-02-03.md`; it was not an extraction input.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:18:01+00:00 — TASK dependency-extract; UPDATE / CONSERVATIVE; accepted decomposition `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` resolved; 21 ACTIVE (8 ANCHOR, 13 EXECUTION), 0 RETIRED; no local integrity warnings; execution satisfaction remains TBD.
- 2026-09-29T14:38:40+00:00 — TASK DX-2 (run APP-V4-BASIS-ALIGN-20260928); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 22 ACTIVE (8 ANCHOR / 14 EXECUTION), 2 RETIRED; 3 added (DEL-05-01, DEL-01-01, TBD-006 owner decision), 2 updated in place (003, 012), 2 retired (015 OI-001, 016 OI-002); warnings none; dependency closure unclaimed.
- 2026-09-30T02:35:46+00:00 — TASK DX (run APP-V4-SCA002-20260929); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 25 ACTIVE (8 ANCHOR / 17 EXECUTION), 2 RETIRED; 3 added (DEL-03-02, DEL-03-03, DEL-01-04), 0 updated, 0 retired; warnings none; dependency closure unclaimed.
