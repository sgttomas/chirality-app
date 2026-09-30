# Dependencies: DEL-01-04 Native requests, outcomes and attachments

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
- **Register:** `Dependencies.csv` v3.1, 29 columns; 18 ACTIVE / 1 RETIRED; ACTIVE origin: 18 EXTRACTED.
- **Classes (ACTIVE):** 6 ANCHOR (1 parent + 3 scope + 2 objective), 12 EXECUTION.
- **Execution targets (ACTIVE):** 6 DELIVERABLE, 6 EXTERNAL; direction 1 DOWNSTREAM, 11 UPSTREAM; types 4 CONSTRAINT, 1 HANDOVER, 4 INTERFACE, 3 PREREQUISITE.
- **This run:** 0 added, 4 updated in place (013 and 016 re-quoted against revised TBD-001/TBD-004; 011 and 018 notes), 1 retired (014 OI-002, source_revised; successor 011)

| DependencyID | Class / type | Direction | Target | Closure | Status |
|---|---|---|---|---|---|
| DEP-01-04-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-01 | NOT_APPLICABLE | ACTIVE |
| DEP-01-04-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-005 | NOT_APPLICABLE | ACTIVE |
| DEP-01-04-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-014 | NOT_APPLICABLE | ACTIVE |
| DEP-01-04-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-129 | NOT_APPLICABLE | ACTIVE |
| DEP-01-04-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-001 | NOT_APPLICABLE | ACTIVE |
| DEP-01-04-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-002 | NOT_APPLICABLE | ACTIVE |
| DEP-01-04-007 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-01-01 | TBD | ACTIVE |
| DEP-01-04-008 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-02 | TBD | ACTIVE |
| DEP-01-04-009 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-02 | TBD | ACTIVE |
| DEP-01-04-010 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-02-02 | TBD | ACTIVE |
| DEP-01-04-011 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-01 | TBD | ACTIVE |
| DEP-01-04-012 | EXECUTION / INTERFACE | UPSTREAM | DEL-04-03 | TBD | ACTIVE |
| DEP-01-04-013 | EXECUTION / CONSTRAINT | UPSTREAM | OI-001 | TBD | ACTIVE |
| DEP-01-04-014 | EXECUTION / CONSTRAINT | UPSTREAM | OI-002 | TBD | RETIRED |
| DEP-01-04-015 | EXECUTION / CONSTRAINT | UPSTREAM | OI-008 | TBD | ACTIVE |
| DEP-01-04-016 | EXECUTION / CONSTRAINT | UPSTREAM | OI-012 | TBD | ACTIVE |
| DEP-01-04-017 | EXECUTION / CONSTRAINT | UPSTREAM | OI-014 | TBD | ACTIVE |
| DEP-01-04-018 | EXECUTION / PREREQUISITE | UPSTREAM | DEP-005 | TBD | ACTIVE |
| DEP-01-04-019 | EXECUTION / PREREQUISITE | UPSTREAM | Person performing the positive human-act case and separate faithful recorder | TBD | ACTIVE |

## Lifecycle Summary

- ACTIVE: 18; RETIRED: 1. Closure (ACTIVE): NOT_APPLICABLE 6, PENDING 0, TBD 12, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-01-04; brief: run APP-V4-SCA002-20260929 node DX dispatch message, reusing run APP-V4-BASIS-ALIGN-20260928 `BRIEFS.md` section "DX — dependency-extract UPDATE" shared overrides; selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (both brief overrides). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (brief override; located, SHA256 `ea3388bcb05b2280d8bb10db2578aec9818f40c559b4214e1732da754d9bd7d5`). Companion CSVs in the same folder (Packages, Deliverables, ScopeLedger, Objectives, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (explicit brief override); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/` files, MEMORY.md, _CONTEXT.md and _SEMANTIC.md were not read as extraction sources. `_REFERENCES.md` was read for pointer resolution only.
- Source ScopeOfWork.md SHA256 `0cdb44e297010b70deb479ab647a165023846aa0943c3f9fc200407c708469cd` (as revised under SCA-V4-002 at commit 1efd4bcda where in scope); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table before Pass 2 examined execution statements. Existing anchor TargetLocation pointers to the GROUP3 frozen snapshot are retained (the IDs are unchanged and resolve in both).
- Match/merge (UPDATE): 18 of 19 prior EXTRACTED rows re-observed and kept ACTIVE with their DependencyIDs; LastSeen refreshed. Updated in place: DEP-01-04-013 (OI-001; Statement/TargetName/EvidenceQuote/Notes re-quoted against revised TBD-001, narrowed to matters the D2 ruling does not cover), DEP-01-04-016 (OI-012; Statement/TargetName/EvidenceQuote/Notes re-quoted against revised TBD-004, narrowed to the implementation/qualification pin), DEP-01-04-011 (DEL-04-01; SourceRef/Notes for revised CLM-005/VER-005) and DEP-01-04-018 (DEP-005; Notes). No row added.
- Retired (retired_by=source_revised, never deleted): DEP-01-04-014 OI-002 owner-decision constraint. Revised TBD-002 records OI-002 as ruled by APP-V4-FIRST-INCREMENT-20260928-DECISION-1 D3 with no residual open part stated in this SoW; successor: the adopted result is received through DEL-04-01 (DEP-01-04-011). Treatment follows DEP-02-03-016 under SCA-V4-001.
- SCA-V4-002 edits to this SoW (F-0104-01 CLM-005; F-0104-02 VER-005; F-0104-03 TBD-001; F-0104-04 TBD-002; F-0104-05 TBD-004; F-0104-06 AX-004) name no deliverable that the SoW did not already name and add no consumption statement. No new arc. The prior run's observation that TBD-001/TBD-002/TBD-004 still described OI-001/OI-002/OI-012 as open is now resolved by the source revision.
- Considered, not extracted (CONSERVATIVE, information flow only): OI-021 (operation-specific reserved-act additions) is named in CLM-005 and TBD-001 without an owner or point of need in this SoW, so it is carried in DEP-01-04-013's Statement/Notes rather than as a separate EXTERNAL row (unlike DEL-04-02 TBD-001, which states both). The CLM-002 through CLM-006 and REQ-006 ownership/exclusion lists alone create no edges beyond the existing consumer/supplier rows. This register is the supplier endpoint of arc X-1 (DEL-02-03 → DEL-01-04), whose row belongs to DEL-02-03 (DEP-02-03-027); no source sentence here names DEL-02-03, so no row was added.
- Guards (brief): no row makes an SCC-002 member depend on DEL-09-06 and DEL-09-06 has no DOWNSTREAM row to an SCC-002 member; nothing grounds N-12 or N-B8; DEL-04-01 gains no supplier row from an SCC-002 member. Checked against this register after the run: not triggered.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged.
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream).
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, verbatim quotes <=30 words, non-placeholder SourceRefs, target placement, no duplicate typed-target keys); target IDs unresolved: none. Schema validator PASS. enum invocations=23, id invocations=33, all_ok=True
- Optional `validate_decomposition_registers.py` whole-execution EVQ/DRB scan not run per deliverable (the brief bounds reads to the deliverable and decomposition); the equivalent local EVQ-003/EVQ-004/DRB-006 conditions were checked and are absent.
- Warnings: none.
- Comparison with the run folder's `AMENDMENT_PACKET/ARC_EFFECT.md` expectations was performed after extraction as a separate coordinator check and is reported in the run-folder return `DX/DX_DEL-01-04.md`; it was not an extraction input.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:14:57+00:00 — TASK dependency-extract; UPDATE / CONSERVATIVE; accepted GROUP3-20260928T001055Z canonical SOFTWARE_DECOMP.md available; warnings 0; ACTIVE 19 (ANCHOR 6 / EXECUTION 13), RETIRED 0; no lifecycle act.
- 2026-09-29T14:34:59Z — TASK dependency-extract (APP-V4-BASIS-ALIGN-20260928 DX-1); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only (unchanged source); decomposition projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md available; +0 / refreshed 0 / retired 0; ACTIVE 19 (ANCHOR 6 / EXECUTION 13), RETIRED 0; warnings none.
- 2026-09-30T02:41:42+00:00 — TASK DX (run APP-V4-SCA002-20260929); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 18 ACTIVE (6 ANCHOR / 12 EXECUTION), 1 RETIRED; 0 added, 4 updated (013, 016, 011, 018), 1 retired (014 source_revised); warnings none; dependency closure unclaimed.
