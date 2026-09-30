# Dependencies: DEL-03-03 Local external-agent receiving adapter

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
- **Register:** `Dependencies.csv` v3.1, 29 columns; 14 ACTIVE / 0 RETIRED; ACTIVE origin: 14 EXTRACTED.
- **Classes (ACTIVE):** 5 ANCHOR (1 parent + 3 scope + 1 objective), 9 EXECUTION.
- **Execution targets (ACTIVE):** 6 DELIVERABLE, 3 EXTERNAL; direction 1 DOWNSTREAM, 8 UPSTREAM; types 1 HANDOVER, 3 INTERFACE, 5 PREREQUISITE.
- **This run:** 0 added, 1 updated in place (008: SourceRef/Notes for the revised CLM-002 tail and REQ-005), 0 retired

| DependencyID | Class / type | Direction | Target | Closure | Status |
|---|---|---|---|---|---|
| DEP-03-03-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM | PKG-03 | NOT_APPLICABLE | ACTIVE |
| DEP-03-03-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-148 | NOT_APPLICABLE | ACTIVE |
| DEP-03-03-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-183 | NOT_APPLICABLE | ACTIVE |
| DEP-03-03-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | SOW-184 | NOT_APPLICABLE | ACTIVE |
| DEP-03-03-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM | OBJ-004 | NOT_APPLICABLE | ACTIVE |
| DEP-03-03-006 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-03-01 | PENDING | ACTIVE |
| DEP-03-03-007 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-03-02 | PENDING | ACTIVE |
| DEP-03-03-008 | EXECUTION / PREREQUISITE | UPSTREAM | DEL-04-01 | PENDING | ACTIVE |
| DEP-03-03-009 | EXECUTION / PREREQUISITE | UPSTREAM | Codex native-tool capability for the selected local MCP or CLI boundary | PENDING | ACTIVE |
| DEP-03-03-010 | EXECUTION / INTERFACE | UPSTREAM | External host owner: catalog-derived local MCP/CLI endpoint contract | PENDING | ACTIVE |
| DEP-03-03-011 | EXECUTION / PREREQUISITE | UPSTREAM | SWBPIPE | PENDING | ACTIVE |
| DEP-03-03-012 | EXECUTION / HANDOVER | DOWNSTREAM | DEL-09-09 | PENDING | ACTIVE |
| DEP-03-03-013 | EXECUTION / INTERFACE | UPSTREAM | DEL-01-01 | PENDING | ACTIVE |
| DEP-03-03-014 | EXECUTION / INTERFACE | UPSTREAM | DEL-02-03 | PENDING | ACTIVE |

## Lifecycle Summary

- ACTIVE: 14; RETIRED: 0. Closure (ACTIVE): NOT_APPLICABLE 5, PENDING 9, TBD 0, IN_PROGRESS 0, SATISFIED 0, WAIVED 0.
- Local Deliverable RequiredMaturity INITIALIZED is a checked contract threshold only. No execution row is reported received, compatible, adopted, qualified or complete by this extraction; closure states were not advanced.

## Run Notes

- SCOPE DEL-03-03; brief: run APP-V4-SCA002-20260929 node DX dispatch message, reusing run APP-V4-BASIS-ALIGN-20260928 `BRIEFS.md` section "DX — dependency-extract UPDATE" shared overrides; selected method `chirality-root:bundled:workflow:dependency-extract` (`workflows/dependency-extract/WORKFLOW.md`).
- MODE UPDATE; STRICTNESS CONSERVATIVE (both brief overrides). Defaults applied: CONSUMER_CONTEXT NONE, ARCHITECTURE_BASIS_POLICY NONE, DOC_ROLE_MAP DEFAULT.
- RUN_ROOT `projects/chirality-app-v4/execution`; DECOMPOSITION_PATH `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (brief override; located, SHA256 `ea3388bcb05b2280d8bb10db2578aec9818f40c559b4214e1732da754d9bd7d5`). Companion CSVs in the same folder (Packages, Deliverables, ScopeLedger, Objectives, Open_Issues, External_Dependencies) were used for identity/label resolution only; all ACTIVE target IDs resolve there.
- SOURCE_DOCS `ScopeOfWork.md` only (explicit brief override); ANCHOR_DOC `ScopeOfWork.md`; EXECUTION_DOC_ORDER [`ScopeOfWork.md`]. `Design/` files, MEMORY.md, _CONTEXT.md and _SEMANTIC.md were not read as extraction sources. `_REFERENCES.md` was read for pointer resolution only.
- Source ScopeOfWork.md SHA256 `93faf918ce5d2d4eb14f0ecd1b20831a164a8c55a8b47cad26880818251b1a93` (as revised under SCA-V4-002 at commit 1efd4bcda where in scope); unchanged by this run.
- Two passes in order: Pass 1 re-verified every ANCHOR row against the current frontmatter/traceability table before Pass 2 examined execution statements. Existing anchor TargetLocation pointers to the GROUP3 frozen snapshot are retained (the IDs are unchanged and resolve in both).
- Match/merge (UPDATE): all 14 prior EXTRACTED rows re-observed with verbatim evidence and kept ACTIVE with their DependencyIDs; LastSeen refreshed. Updated in place: DEP-03-03-008 (SourceRef/Notes only, for the SCA-V4-002 revision of the CLM-002 tail and REQ-005; no identity, direction, type, target, quote, maturity or closure change). No row added. No row retired.
- SCA-V4-002 edits to this SoW (F-0303-01 CLM-002 tail; F-0303-02 REQ-005 policy clause; F-0303-03 AX-005) name no deliverable that the SoW did not already name and add no consumption statement; they restate ownership of the residual reserved-act matters (OI-021 additions with the owner via the outside SWB session and the App/shared owner; host adoption and enforcement under DEP-001). No new arc.
- Typing of DEP-03-03-013/-014 (INTERFACE) and the prior-run reading of the Praxeology opening paragraph are unchanged.
- Considered, not extracted (CONSERVATIVE, information flow only): the revised CLM-002 tail and REQ-005 are ownership/retention statements, not inputs this adapter consumes; OI-021 (TBD-006), OI-003 (TBD-003), OI-013 (TBD-004), OI-014 (TBD-005) and TBD-007 retain their source owners and points of need and remain unextracted as in the prior runs; DEP-001 host adoption/enforcement is carried by the existing SWBPIPE row DEP-03-03-011. No UPSTREAM row to DEL-04-03 (N-B8) is written: the SoW names no DEL-04-03 input. No row to DEL-09-06: the SoW does not name it. DEL-03-04, DEL-04-02, DEL-02-01 and the DEL-04-03/DEL-02-03 supplier mirrors remain without SoW ground (the DEL-02-03 → DEL-03-03 arc N-24 is now carried by DEL-02-03's consumer row DEP-02-03-026).
- Guards (brief): no row makes an SCC-002 member depend on DEL-09-06 and DEL-09-06 has no DOWNSTREAM row to an SCC-002 member; nothing grounds N-12 or N-B8; DEL-04-01 gains no supplier row from an SCC-002 member. Checked against this register after the run: not triggered.
- FACT/ASSUMPTION/PROPOSAL separation is recorded per row in Notes. No human act, receipt, compatibility or closure is inferred; closure states unchanged.
- Declared mirrors: 0 added, 0 refreshed, 0 retired; 2 entries skipped ("None declared at initial setup." placeholders in Declared Upstream/Downstream).
- Local checks: PASS (unique IDs, DEP prefix, one parent anchor, verbatim quotes <=30 words, non-placeholder SourceRefs, target placement, no duplicate typed-target keys); target IDs unresolved: none. Schema validator PASS. enum invocations=21, id invocations=30, all_ok=True
- Optional `validate_decomposition_registers.py` whole-execution EVQ/DRB scan not run per deliverable (the brief bounds reads to the deliverable and decomposition); the equivalent local EVQ-003/EVQ-004/DRB-006 conditions were checked and are absent.
- Warnings: none.
- Comparison with the run folder's `AMENDMENT_PACKET/ARC_EFFECT.md` expectations was performed after extraction as a separate coordinator check and is reported in the run-folder return `DX/DX_DEL-03-03.md`; it was not an extraction input.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:20:59+00:00 — TASK `/root/renewal_research_strategy/dep_del_03_03`; UPDATE / CONSERVATIVE; decomposition `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` and accepted companion identity rows available. ACTIVE=12 (ANCHOR=5; EXECUTION=7); RETIRED=0. Mandatory local checks passed; no integrity warnings. Actual external availability/receipt/adoption and unresolved interface choices remain unclaimed.
- 2026-09-28T04:25:33+00:00 — TASK `/root/renewal_research_strategy/resolve_dep_03_03`; bounded R3 UPDATE / CONSERVATIVE using accepted G3 companion rows and the supplied target-resolution report. `DEP-03-03-008` now targets `DEL-04-01`; ACTIVE=12 (ANCHOR=5; EXECUTION=7), RETIRED=0, EXTERNAL=3, UNKNOWN=0. RequiredMaturity=TBD, ProposedMaturity blank and SatisfactionStatus=PENDING preserved; mandatory local checks passed, no global check or graph change.
- 2026-09-29T14:38:50+00:00 — TASK DX-3 (APP-V4-BASIS-ALIGN-20260928); UPDATE / CONSERVATIVE; SOURCE_DOCS=ScopeOfWork.md; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` available. Added 2 (DEL-01-01, DEL-02-03 UPSTREAM INTERFACE), refreshed 1 (DEP-03-03-008), retired 0. ACTIVE=14 (ANCHOR=5; EXECUTION=9), RETIRED=0. Mandatory local checks passed; no integrity warnings.
- 2026-09-30T02:37:21+00:00 — TASK DX (run APP-V4-SCA002-20260929); UPDATE / CONSERVATIVE; SOURCE_DOCS ScopeOfWork.md only; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` resolved; 14 ACTIVE (5 ANCHOR / 9 EXECUTION), 0 RETIRED; 0 added, 1 updated (008), 0 retired; warnings none; dependency closure unclaimed.
