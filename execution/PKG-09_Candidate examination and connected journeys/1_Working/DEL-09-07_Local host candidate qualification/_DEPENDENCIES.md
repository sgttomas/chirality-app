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
- **Status:** EXTRACTED_AND_LOCALLY_VALIDATED
- **Register:** `Dependencies.csv` (v3.1; 29 columns).
- **Counts:** 25 ACTIVE rows: 10 ANCHOR (1 parent, 9 scope/objective traces), 15 EXECUTION (14 UPSTREAM, 1 DOWNSTREAM); 0 RETIRED; 0 DECLARED; EXECUTION target types: DELIVERABLE 2, EXTERNAL 9, PACKAGE 4.

| DependencyID | Class / anchor | Direction / type | Target | Satisfaction | Status |
|---|---|---|---|---|---|
| DEP-09-07-001 | ANCHOR / IMPLEMENTS_NODE | UPSTREAM / OTHER | PKG-09 | NOT_APPLICABLE | ACTIVE |
| DEP-09-07-002 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | SOW-199 | NOT_APPLICABLE | ACTIVE |
| DEP-09-07-003 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | SOW-200 | NOT_APPLICABLE | ACTIVE |
| DEP-09-07-004 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | SOW-201 | NOT_APPLICABLE | ACTIVE |
| DEP-09-07-005 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | SOW-202 | NOT_APPLICABLE | ACTIVE |
| DEP-09-07-006 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | SOW-239 | NOT_APPLICABLE | ACTIVE |
| DEP-09-07-007 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | OBJ-004 | NOT_APPLICABLE | ACTIVE |
| DEP-09-07-008 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | OBJ-005 | NOT_APPLICABLE | ACTIVE |
| DEP-09-07-009 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | OBJ-008 | NOT_APPLICABLE | ACTIVE |
| DEP-09-07-010 | ANCHOR / TRACES_TO_REQUIREMENT | UPSTREAM / OTHER | OBJ-009 | NOT_APPLICABLE | ACTIVE |
| DEP-09-07-011 | EXECUTION / NOT_APPLICABLE | UPSTREAM / PREREQUISITE | DEL-09-06 | TBD | ACTIVE |
| DEP-09-07-012 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | PKG-02 | TBD | ACTIVE |
| DEP-09-07-013 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | PKG-03 | TBD | ACTIVE |
| DEP-09-07-014 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | PKG-04 | TBD | ACTIVE |
| DEP-09-07-015 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | PKG-05 | TBD | ACTIVE |
| DEP-09-07-016 | EXECUTION / NOT_APPLICABLE | UPSTREAM / PREREQUISITE | DEP-001 | TBD | ACTIVE |
| DEP-09-07-017 | EXECUTION / NOT_APPLICABLE | UPSTREAM / PREREQUISITE | Actual App/SWBPIPE candidate and local-model runtime configuration | TBD | ACTIVE |
| DEP-09-07-018 | EXECUTION / NOT_APPLICABLE | UPSTREAM / PREREQUISITE | Person/engineer — scoped V4-EXM-20 row decisions | TBD | ACTIVE |
| DEP-09-07-019 | EXECUTION / NOT_APPLICABLE | UPSTREAM / PREREQUISITE | Engineer-edited model and agent checking request for V4-EXM-21 | TBD | ACTIVE |
| DEP-09-07-020 | EXECUTION / NOT_APPLICABLE | UPSTREAM / PREREQUISITE | Person-adopted per-operation autonomy policy and actual run setting | TBD | ACTIVE |
| DEP-09-07-021 | EXECUTION / NOT_APPLICABLE | UPSTREAM / PREREQUISITE | Person's actual declared workflow-checkpoint act for V4-EXM-22 | TBD | ACTIVE |
| DEP-09-07-022 | EXECUTION / NOT_APPLICABLE | UPSTREAM / CONSTRAINT | OI-001 | TBD | ACTIVE |
| DEP-09-07-023 | EXECUTION / NOT_APPLICABLE | UPSTREAM / CONSTRAINT | OI-002 | TBD | ACTIVE |
| DEP-09-07-024 | EXECUTION / NOT_APPLICABLE | UPSTREAM / INTERFACE | Independent examiner — joined local qualification dossier examination | TBD | ACTIVE |
| DEP-09-07-025 | EXECUTION / NOT_APPLICABLE | DOWNSTREAM / HANDOVER | DEL-11-03 | TBD | ACTIVE |

## Lifecycle Summary
- ACTIVE: 25; RETIRED: 0. Satisfaction (ACTIVE): NOT_APPLICABLE 10; TBD 15.
- INITIALIZED: source-grounded contract exists; the SCA-V4-001 REVISE left DEL-09-07 INITIALIZED. No dependency availability or product-readiness verdict. Execution SatisfactionStatus=TBD is the register convention.

## Run Notes
- Workflow: `chirality-root:bundled:workflow:dependency-extract`; SCOPE `DEL-09-07`; MODE `UPDATE`; STRICTNESS `CONSERVATIVE`; CONSUMER_CONTEXT `NONE`; ARCHITECTURE_BASIS_POLICY `NONE`.
- RUN_ROOT: `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution`. DECOMPOSITION_PATH: `/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md`; accepted companion Package/Deliverable/scope/objective rows resolve labels and IDs only. Historical snapshot candidate/pending labels do not reverse the accepted basis specified by the brief.
- SOURCE_DOCS, ANCHOR_DOC and EXECUTION_DOC_ORDER: `ScopeOfWork.md` only; DOC_ROLE_MAP `DEFAULT`. Pass 1 completed with one parent, five scope traces and four objective traces before Pass 2.
- Source SHA256 before/after: `36cc2e24595f0585111929204e27943f68b79bb54001ba52a3356aba9f78c1a0`; matches dispatch. Initial register absent; 25 extracted rows added, none refreshed/retired/deleted. Human-owned sections and prior history preserved exactly. Declaration mirror counts: added 0, refreshed 0, retired 0, skipped 2 initial-setup placeholders.
- RequiredMaturity `INITIALIZED` applies only to local Deliverable contract maturity. Actual agreement, technical contribution, runtime configuration, adopted policy, scoped human acts and examined dossier are separate conditions; all 15 execution rows remain `TBD` for satisfaction. Anchors have `NOT_APPLICABLE` closure. No delivery, qualification, lifecycle advancement, acceptance or adoption is claimed.
- Four consumed package-contract interfaces stay at package level: CLM-003 states positive consumption but does not identify exact contributing Deliverables. No owner/exclusion list was converted into edges; no full-package completion or blanket provider gate. Package/non-Deliverable maturity remains `TBD`.
- External DEP-001 remains SWB-owned and human-relayed; actual candidate/configuration/model/server, complete same-run host traffic/native-boundary evidence and receipts remain necessary. No construction or provider readiness is inferred. OI-001/002 apply only at the stated affected points of need; OI-021 choices arrive with the actual DEL-09-06 agreement. Independent definition and unrelated checks may continue.
- Scoped witness inputs retain the person as actor for row decisions and checkpoint release, and preserve the engineer-edited checking fixture. No synthetic sequence between acceptance, checking, approval and reliance; no favorable professional act demanded. PEC remains optional and Domains later; neither becomes a local-host qualification gate.
- Limits: exact runtime/endpoint/model/provider configuration, actual received external contributions, contract subsets, adopted policy dispositions and human/examiner acts are not established by extraction. `TargetLocation=TBD` names missing execution locations without inventing identifiers. No unresolved source conflict identified. No FLOATING_NODE or AMBIGUOUS_ANCHOR warning.
- Local schema, all used core enums, supported ID formats, one-parent/duplicate/evidence/quote/summary/source/declared-preservation checks: PASS. Optional whole-execution EVQ/DRB scan omitted; local equivalents found no blank quotes, placeholder SourceRef or mismatched dependency prefix. See `_run_records/dependency-extract-20260927.md` for exact verification results and hashes.

- **Run 2026-09-29 (DX-3, APP-V4-BASIS-ALIGN-20260928; dependency-extract UPDATE after SCA-V4-001 SoW revision).** Method `chirality-root:bundled:workflow:dependency-extract` (WORKFLOW.md SHA256 `e5523ebabccf44337ec531280d4d91be2ce7ff1477bd39568a18bb0c4c9f18c3`). Brief: run folder `BRIEFS.md` § DX (group DX-3). Defaults and chosen paths: SCOPE=DEL-09-07; MODE=UPDATE; STRICTNESS=CONSERVATIVE; CONSUMER_CONTEXT=NONE; ARCHITECTURE_BASIS_POLICY=NONE; DOC_ROLE_MAP=DEFAULT; SOURCE_DOCS=ANCHOR_DOC=EXECUTION_DOC_ORDER=`ScopeOfWork.md` only (explicit); RUN_ROOT=`projects/chirality-app-v4/execution`; DECOMPOSITION_PATH=`projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` (current, post-SCA-V4-001; its ScopeLedger companion resolves the amended SOW-201/SOW-202 labels).
- Source `ScopeOfWork.md` SHA256 `53b51d309d060089a6a88dae565867a92348789ee01430927e7464c7c2d3cba0` (commit `340ecf341`), unchanged during the run. The SoW has no `Design/` folder.
- Pass 1: parent PKG-09 and traces SOW-199/200/201/202/239 and OBJ-004/005/008/009 re-confirmed. `DEP-09-07-004` (SOW-201) and `DEP-09-07-005` (SOW-202) TargetName/TargetLocation re-resolved to the current ScopeLedger labels amended by SCA-V4-001 (GROUP3 labels preserved in Notes as `legacy_TargetName`).
- Pass 2: 0 rows added; 2 rows refreshed in place: `DEP-09-07-016` (DEP-001 contribution: native destination-enforcement wording for revised REQ-006/AC-006/VER-006) and `DEP-09-07-021` (checkpoint act: re-quoted from revised VER-005; recorded only when performed, hold/release only in the governance phase, DECISION-4 D4-1). 21 rows re-observed unchanged (LastSeen only). 0 retired. TBD-002/TBD-003 (OI-001/OI-002) are unchanged in this SoW, so `DEP-09-07-022`/`-023` are unchanged. No new deliverable target is named; the destination allow list and in-work grants (VER-006) are part of the runtime configuration already carried by `DEP-09-07-017`.
- Declaration mirrors added/refreshed/retired: 0/0/0; 2 placeholders skipped. Human-owned sections byte-identical.
- Function 5 checks: `validate_dependencies_schema.py` VALID (29 columns, 25 rows); `validate_enum.py` 23 invocations, 0 failures; `validate_id_format.sh` 43 invocations, 0 failures; unique IDs; prefix matches; exactly 1 ACTIVE parent anchor; no blank quote or placeholder locus; no Status=CANDIDATE. Run record: `_run_records/dependency-extract-20260929.md`.

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:38:14+00:00 — TASK `/root/renewal_research_strategy/dep_del_09_07`; UPDATE / CONSERVATIVE; decomposition `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` present, canonical labels resolved; warnings 0; ACTIVE 25 (ANCHOR 10, EXECUTION 15), RETIRED 0; source unchanged and local checks PASS. No closure or lifecycle advancement.
- 2026-09-29T14:38:50+00:00 — TASK DX-3 (APP-V4-BASIS-ALIGN-20260928); UPDATE / CONSERVATIVE; SOURCE_DOCS=ScopeOfWork.md; decomposition `projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md` available. Added 0, refreshed 4 (anchors DEP-09-07-004/-005 labels; DEP-09-07-016, -021), retired 0. ACTIVE=25 (ANCHOR=10; EXECUTION=15), RETIRED=0. Mandatory local checks passed; no integrity warnings.
