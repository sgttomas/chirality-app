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
- **Status:** EXTRACTED
- **Register:** `Dependencies.csv` (v3.1; 29 columns)
- **ACTIVE:** 25 — ANCHOR 10 (parent 1; scope 5; objective 4), EXECUTION 15 (UPSTREAM 14; DOWNSTREAM 1). EXTERNAL 9; UNKNOWN 0. DECLARED 0; RETIRED 0.

| DependencyID | Class | Direction | Type | Target |
|---|---|---|---|---|
| DEP-09-07-001 | ANCHOR | UPSTREAM | OTHER | PKG-09 |
| DEP-09-07-002 | ANCHOR | UPSTREAM | OTHER | SOW-199 |
| DEP-09-07-003 | ANCHOR | UPSTREAM | OTHER | SOW-200 |
| DEP-09-07-004 | ANCHOR | UPSTREAM | OTHER | SOW-201 |
| DEP-09-07-005 | ANCHOR | UPSTREAM | OTHER | SOW-202 |
| DEP-09-07-006 | ANCHOR | UPSTREAM | OTHER | SOW-239 |
| DEP-09-07-007 | ANCHOR | UPSTREAM | OTHER | OBJ-004 |
| DEP-09-07-008 | ANCHOR | UPSTREAM | OTHER | OBJ-005 |
| DEP-09-07-009 | ANCHOR | UPSTREAM | OTHER | OBJ-008 |
| DEP-09-07-010 | ANCHOR | UPSTREAM | OTHER | OBJ-009 |
| DEP-09-07-011 | EXECUTION | UPSTREAM | PREREQUISITE | DEL-09-06 |
| DEP-09-07-012 | EXECUTION | UPSTREAM | INTERFACE | PKG-02 |
| DEP-09-07-013 | EXECUTION | UPSTREAM | INTERFACE | PKG-03 |
| DEP-09-07-014 | EXECUTION | UPSTREAM | INTERFACE | PKG-04 |
| DEP-09-07-015 | EXECUTION | UPSTREAM | INTERFACE | PKG-05 |
| DEP-09-07-016 | EXECUTION | UPSTREAM | PREREQUISITE | DEP-001 |
| DEP-09-07-017 | EXECUTION | UPSTREAM | PREREQUISITE | Actual App/SWBPIPE candidate and local-model runtime configuration |
| DEP-09-07-018 | EXECUTION | UPSTREAM | PREREQUISITE | Person/engineer — scoped V4-EXM-20 row decisions |
| DEP-09-07-019 | EXECUTION | UPSTREAM | PREREQUISITE | Engineer-edited model and agent checking request for V4-EXM-21 |
| DEP-09-07-020 | EXECUTION | UPSTREAM | PREREQUISITE | Person-adopted per-operation autonomy policy and actual run setting |
| DEP-09-07-021 | EXECUTION | UPSTREAM | PREREQUISITE | Person's actual declared workflow-checkpoint act for V4-EXM-22 |
| DEP-09-07-022 | EXECUTION | UPSTREAM | CONSTRAINT | OI-001 |
| DEP-09-07-023 | EXECUTION | UPSTREAM | CONSTRAINT | OI-002 |
| DEP-09-07-024 | EXECUTION | UPSTREAM | INTERFACE | Independent examiner — joined local qualification dossier examination |
| DEP-09-07-025 | EXECUTION | DOWNSTREAM | HANDOVER | DEL-11-03 |

---

## Lifecycle Summary
- INITIALIZED: source-grounded SOW_V1 exists and independent INIT verification passed; manager recorded the separate status act under the approved policy. No dependency availability or product-readiness verdict.
- Register lifecycle: ACTIVE 25; RETIRED 0. Closure: NOT_APPLICABLE 10 (anchors); TBD 15 (execution); PENDING 0; IN_PROGRESS 0; SATISFIED 0; WAIVED 0.

---

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

## Run History
- 2026-09-27 — WORKING_ITEMS applied preparation; extraction not run.
- 2026-09-28T03:38:14+00:00 — TASK `/root/renewal_research_strategy/dep_del_09_07`; UPDATE / CONSERVATIVE; decomposition `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/SOFTWARE_DECOMP.md` present, canonical labels resolved; warnings 0; ACTIVE 25 (ANCHOR 10, EXECUTION 15), RETIRED 0; source unchanged and local checks PASS. No closure or lifecycle advancement.
