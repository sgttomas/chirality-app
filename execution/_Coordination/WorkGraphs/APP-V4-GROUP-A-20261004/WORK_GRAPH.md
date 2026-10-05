# Work graph — Group A runtime and contract core toward 90%

## Intent and selected route

- Stable run: `APP-V4-GROUP-A-20261004`; current branch `codex/app-v4-group-a-90`, base `e916ad1789`.
- Owner steering: resolve CI-1…CI-9 by named reviewed change control with affected design owners first; replace macOS temp paths; then grow walking skeleton into tested Group A code toward 90%. Owner assesses gate.
- Methods: `chirality-root:bundled:workflow:coordinated-knowledge-work` and `chirality-root:bundled:workflow:construct-local-work-graph`.
- Route: recover design contracts → reviewed CI changes → propagate/test skeleton → implement ready Group A contract slices → independent review/repair/integration → bounded reconciliation, receipt/MEMORY and final PR.
- Scope: DEL-01-01/02/03/04/05, DEL-02-01/02/03/04, DEL-03-01/02/03, DEL-04-01/02/03, DEL-05-01/02, DEL-09-09. Basis is accepted DAG-004; currency CURRENT_WITH_EVIDENCE_DRIFT, no DAG-pending deliverables. Held rows stay SCC_UNRESOLVED and non-gating; no acceptance or regrouping inferred.
- Limits: offline default; no downloads until exact file/source/size owner yes. Scratch mktemp Codex home only. Parent coordinates newly authorized sign-in; no children use credentials or live turns. SWBPIPE joins remain deferred DECISION-3. Placement OI-013/014 awaits owner when blocking.

## Work

| ID / outcome | Deliverable, writes and owner | Needs | Completion check | State |
|---|---|---|---|---|
| G0 recover graph and sources | This graph/run; WORKING_ITEMS | Steering, current graph/records | Route and relationship recovery, source hashes | COMPLETE initial graph; detailed I1–5 route recovery ACTIVE with group_a_route |
| CC-H hosting/access CI2,7,8 | DEL-01-01/05 Design; design_hosting_access | Frozen prior contracts and observations | Named changes, source/consumer analysis and review | ACTIVE candidate; V0 review then app propagation |
| CC-R RS/EXEC CI1,3,4,9; D07/U08 | DEL-04-03/02-03 Design; design_records_exec | Frozen contracts; CI9 dependency need | Named changes preserve scope, validated schemas, consumer analysis/review | ACTIVE CI1/3/D07/U08; CI4 owner fallback choice pending; CI9 validator download inventory |
| CC-A AAC CI5,6 | DEL-01-04 Design; design_aac | Frozen AAC/package/RS semantics | Named changes, binding/atomicity checks, independent review | ACTIVE candidate; CI4 fallback proposed only |
| CC-X D49 | DEL-09-09 Design; group_a_route TASK | GROUP_SORT and SoW OUT-004 | Correct citation preserves contribution ladder; independent review | ACTIVE frozen candidate; V0-RX dispatched; GUIDE pin adoption pending |
| V0 contract independent review | Run reviews only; contract_reviewer TASK | CC outputs fixed | Requirements/source comparison, consumer adoption findings | ACTIVE basis assessment saved reviews/V0-BASIS.md; exact-candidate review awaits owners |
| T0 portable temp paths | app tests/docs; portable_temp TASK | Current tests | Unique platform temp dirs; offline tests pass | COMPLETE reviewed V0-T0; integrated current schema tests wait P0 |
| D0 dependency inventory | Run inventory only; dependency_inventory TASK | Cache/lockfile inspection | Missing files, sources, sizes; no downloads | ACTIVE inventory saved; native npm cache complete; exact validator metadata still sought |
| SUP1 latest stock supplier adoption | DEL-01-01 Design/app maintained pin; manager single app writer | Owner latest authorization, parent0.160 evidence, CC-H frozen | Named consumer adoption and affected offline replay; no qualification implied | PLANNED |
| CP0 Design consumer propagation | affected GroupA and downstream Design pins/registries; one TASK owner | V0-H/A/RX ready definitions | Affected consumers triaged including DEL09-02/10-03, GUIDE/CA/DV; warranted adoption checked | PLANNED |
| P0 propagate accepted named CI changes | app code/tests/docs; implementation TASK | V0 disposition and CI9 authority | Existing path passes without schema rewrite or unvalidated writes | PLANNED |
| I1 hosting/recovery core | app hosting and recovery slice | CI2/7/8, provider/version choice where needed | Contract mapped offline lifecycle/request/recovery tests | PLANNED |
| I2 workflow/role/context supply | app workflow registration/execution supply slice | CC contracts | Tested source identity, parsing/supply failure behavior | PLANNED |
| I3 records/acts/standing | app records/act/capture slice | CI1/3/4/5/6/9 and placement choice | Schema refusal, capture binding/recovery, tested policy/standing | PLANNED |
| I4 catalog/proposal/adapter and LOOP/PANEL | app receiving slices | I2/I3 and frozen C/P/ADAPTER/LOOP/PANEL | Offline connected consumer route; host joins held | PLANNED |
| I5 external trace | app trace/test evidence | I1–4 and B examination protocol | Own-code witness distinguished from deferred joins | PLANNED |
| V1 review/repair/integrate each slice | app/run; fresh TASK reviewer; manager integrates | Frozen implementation candidate | Independent software-code-review, meaningful offline tests | PLANNED |
| C1 bounded reconciliation | affected Design, run, graph; manager | Integrated slices | Obligations mapped to produced code/evidence; residuals truthful | PLANNED |
| M1 receipt/MEMORY | Run receipt, affected MEMORY | C1 | One receipt, terse local references | PLANNED |
| F1 final PR | Parent Git authority | Review/required CI and decisions | Final PR merged; no gate acceptance implied | PLANNED |

## Relationships and readiness

GC-8 entry recovery inspected all pre-existing WorkGraphs; there are no active B/C/D/E development graphs. Historical graphs remain at original locations. Carry these relationships when those loops construct graphs:
- DEP-09-09-012: A external trace consumes B DEL-09-01 examination protocol; real acyclic exception to A→{B,C}→D→E. Protocol already exists; no qualification claim before candidate examination. O-1 A–B cycle depends on P16 cut; held rows unchanged.
- D07 EXEC→CA wording, D49 XT→CA ladder citation, U08 RS→CA CAF-24 citation: reviewed rewordings assigned above, no invented dependence reversal.
- Group A within-group design needs from G2b/GROUP_SORT: D01,D02,D03,D05,D06,D08,D09,D15–D24,D47,D48,U01,U02,U03,U04,U07. Survey classifications guide local sequencing; do not establish satisfaction. Concrete deciding sentences, supplier contributions and18 module acceptance rows recovered in [IMPLEMENTATION_ROUTE.md](../../AgentRuns/APP-V4-GROUP-A-20261004/IMPLEMENTATION_ROUTE.md); read these before I1–5 dispatch.
- B→A packaging reads AAC entitlement/WR/ROLE inputs (D04,U05,U06); A→B supply remains downstream. U10 optional B→C rehearsal retained for those loops.
- Ready now: contract recovery/design changes, portable temp fixes, dependency inventory. Dependent product expansion waits for contract review. Live model paths wait for coordinated parent sign-in.

## Current state and recovery

Maintainer: `/root/group_a_execution` WORKING_ITEMS under parent `/root` HELP_HUMAN. Native descendant mechanism, full launches/returns and hashes belong in this run. Shared app implementation and issue registry remain single-owner integration writes until reviewed contract changes release bounded scopes. Parent owns human decision interface and Git publication coordination; manager records relayed actual decisions in OWNER_DECISIONS. No downloads, qualification, lifecycle changes or final gate acceptance.

Cross-group consumer propagation identified: CC-X changes XT hash pinned by D DEL-03-04 GUIDE; CC-R supplies changed RS/EXEC definitions/refs to D DEL-06-02/09-06/09-05/09-11 and GUIDE. CC-A capture/backlink semantics affect D decision view/standing reader and B conditional SEAL-2 packaging. No active receiving group graphs yet; carry these notices when formed (GC8). Definition change proposals do not make finished consumer work wrong silently; exact affected source pin/semantic reconciliation is a node before claiming ready consumption.

CI4 owner chose explicit label; pending only independent check/propagation. Parent OI014 preparation requires consumer review of multi-log standing/outside-run and portable library A15 ownership before path choice; host OI013 stays external/deferred. Full route readiness is contribution-specific in IMPLEMENTATION_ROUTE.md.
