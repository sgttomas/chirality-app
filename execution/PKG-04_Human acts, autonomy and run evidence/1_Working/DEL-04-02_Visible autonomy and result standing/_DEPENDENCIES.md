# Dependencies: DEL-04-02 Visible autonomy and result standing

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
- **Classes (ACTIVE):** 6 ANCHOR (1 parent + 4 scope + 1 objective), 19 EXECUTION.
- **Execution targets (ACTIVE):** 12 DELIVERABLE, 7 EXTERNAL; direction 6 DOWNSTREAM, 13 UPSTREAM; types 6 CONSTRAINT, 5 HANDOVER, 7 INTERFACE, 1 PREREQUISITE.
- **This run:** 0 added, 13 updated in place (12 re-quoted exactly per ASC-ISS-008: 011, 012, 015–023, 025; 007 SourceRef/Notes for revised CLM-004), 0 retired

| DependencyID | Class / type | Direction | Target | Closure | Status |
|---|---|---|---|---|---|
| DEP-04-02-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-04 | NOT_APPLICABLE | ACTIVE |
| DEP-04-02-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-075 | NOT_APPLICABLE | ACTIVE |
| DEP-04-02-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-076 | NOT_APPLICABLE | ACTIVE |
| DEP-04-02-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-077 | NOT_APPLICABLE | ACTIVE |
| DEP-04-02-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-078 | NOT_APPLICABLE | ACTIVE |
| DEP-04-02-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-005 | NOT_APPLICABLE | ACTIVE |
| DEP-04-02-007 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-04-01 | PENDING | ACTIVE |
| DEP-04-02-008 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-03 | PENDING | ACTIVE |
| DEP-04-02-009 | EXECUTION / INTERFACE | DOWNSTREAM | DEL-04-03 | PENDING | ACTIVE |
| DEP-04-02-010 | EXECUTION / INTERFACE | UPSTREAM | App-v4:DEP-001:SWBPIPE | PENDING | ACTIVE |
| DEP-04-02-011 | EXECUTION / CONSTRAINT | UPSTREAM | App-v4:OI-001 | PENDING | ACTIVE |
| DEP-04-02-012 | EXECUTION / CONSTRAINT | UPSTREAM | App-v4:OI-002 | PENDING | ACTIVE |
| DEP-04-02-013 | EXECUTION / CONSTRAINT | UPSTREAM | App-v4:OI-013 | PENDING | ACTIVE |
| DEP-04-02-014 | EXECUTION / CONSTRAINT | UPSTREAM | App-v4:OI-014 | PENDING | ACTIVE |
| DEP-04-02-015 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-02 | PENDING | ACTIVE |
| DEP-04-02-016 | EXECUTION / INTERFACE | UPSTREAM | DEL-03-01 | PENDING | ACTIVE |
| DEP-04-02-017 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-03 | PENDING | ACTIVE |
| DEP-04-02-018 | EXECUTION / INTERFACE | UPSTREAM | DEL-05-01 | PENDING | ACTIVE |
| DEP-04-02-019 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-05-01 | PENDING | ACTIVE |
| DEP-04-02-020 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-05-02 | PENDING | ACTIVE |
| DEP-04-02-021 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-02 | PENDING | ACTIVE |
| DEP-04-02-022 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-03-03 | PENDING | ACTIVE |
| DEP-04-02-023 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-03 | PENDING | ACTIVE |
| DEP-04-02-024 | EXECUTION / CONSTRAINT | UPSTREAM | App-v4:OI-021 | PENDING | ACTIVE |
| DEP-04-02-025 | EXECUTION / CONSTRAINT | UPSTREAM | APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4 | PENDING | ACTIVE |

## Lifecycle Summary

- ACTIVE: 25; RETIRED: 0. Closure (ACTIVE): NOT_APPLICABLE 6, PENDING 19, TBD 0, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-04-02; brief: run APP-V4-SCA002-20260929 node DX dispatch message, reusing run APP-V4-BASIS-ALIGN-20260928 `BRIEFS.md` section "DX — dependency-extract UPDATE" shared overrides; selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (both brief overrides). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (brief override; located, SHA256 `ea3388bcb05b2280d8bb10db2578aec9818f40c559b4214e1732da754d9bd7d5`). Companion CSVs in the same folder (Packages, Deliverables, ScopeLedger, Objectives, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (explicit brief override); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/` files, MEMORY.md, _CONTEXT.md and _SEMANTIC.md were not read as extraction sources. `_REFERENCES.md` was read for pointer resolution only.
- Source ScopeOfWork.md SHA256 `f16ffa8a33cbfb2e78a8e916e90aff9fb44ad20adf94fe61a559a213f5564460` (as revised under SCA-V4-002 at commit 1efd4bcda where in scope); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table before Pass 2 examined execution statements. Existing anchor TargetLocation pointers to the GROUP3 frozen snapshot are retained (the IDs are unchanged and resolve in both).
- Match/merge (UPDATE): all 25 prior EXTRACTED rows re-observed and kept ACTIVE with their DependencyIDs; LastSeen refreshed. No row added. No row retired.
- Re-quoted exactly (ASC-ISS-008; V12 F1), EvidenceQuote and Notes only: DEP-04-02-011, -012, -015, -016, -017, -018, -019, -020, -021, -022, -023 (inline-code backticks restored) and DEP-04-02-025 (bold markers `**Owner:**`/`**Point of need:**` restored). All 12 are now exact substrings of the SoW and at most 30 words (015–017 are exactly 30). No identity, direction, type, target, maturity or closure change; no arc change.
- Updated in place: DEP-04-02-007 (SourceRef/Notes only) for the SCA-V4-002 revision of CLM-004 (F-0402-01): OI-001/OI-002 ruled for the first increment (D2/D3); residual matters with the Owner with App/SWB contract owners; operation-specific additions under OI-021, already carried by DEP-04-02-024.
- SCA-V4-002 edits to this SoW (F-0402-01 CLM-004 first sentence; F-0402-02 AX-005) name no deliverable and add no consumption statement. No new row, no new arc.
- Considered, not extracted (CONSERVATIVE, information flow only): CLM-004 remains an owner/decision-allocation statement; its OI-013/OI-014 and OI-021 references are already carried by DEP-04-02-013/-014/-024. Ownership/exclusion lists in CLM-002/REQ-007 alone create no edges (DEL-03-03 channel-status display, DEL-05-01 host-loop receiving of checkpoint meanings). Consumption and receiver statements in CLM-002 are carried by the existing rows 015–023.
- Guards (brief): no row makes an SCC-002 member depend on DEL-09-06 and DEL-09-06 has no DOWNSTREAM row to an SCC-002 member; nothing grounds N-12 or N-B8; DEL-04-01 gains no supplier row from an SCC-002 member. Checked against this register after the run: not triggered.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged.
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream).
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, verbatim quotes <=30 words, non-placeholder SourceRefs, target placement, no duplicate typed-target keys); target IDs unresolved: none. Schema validator PASS. enum invocations=22, id invocations=43, all_ok=True
- Optional `validate_decomposition_registers.py` whole-execution EVQ/DRB scan not run per deliverable (the brief bounds reads to the deliverable and decomposition); the equivalent local EVQ-003/EVQ-004/DRB-006 conditions were checked and are absent.
- Warnings: none.
- Comparison with the run folder's `AMENDMENT_PACKET/ARC_EFFECT.md` expectations was performed after extraction as a separate coordinator check and is reported in the run-folder return `DX/DX_DEL-04-02.md`; it was not an extraction input.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:25:20+00:00 — TASK `/root/renewal_research_strategy/dep_del_04_02`; UPDATE / CONSERVATIVE; accepted decomposition available at `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md`; 14 ACTIVE (6 ANCHOR, 8 EXECUTION), 0 RETIRED; local checks passed; unresolved input/owner/host conditions retained without floating or ambiguous anchors.
- 2026-09-29T14:34:59Z — TASK dependency-extract (APP-V4-BASIS-ALIGN-20260928 DX-1); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (revised under SCA-V4-001); decomposition projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md available; +11 / refreshed 2 / retired 0; ACTIVE 25 (ANCHOR 6 / EXECUTION 19), RETIRED 0; warnings none.
- 2026-09-30T02:39:02+00:00 — TASK DX (run APP-V4-SCA002-20260929); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 25 ACTIVE (6 ANCHOR / 19 EXECUTION), 0 RETIRED; 0 added, 13 updated (12 re-quoted: 011, 012, 015–023, 025; 007 notes), 0 retired; warnings none; dependency closure unclaimed.
