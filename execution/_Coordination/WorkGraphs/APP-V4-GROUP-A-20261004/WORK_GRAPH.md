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
| CC-H hosting/access CI2,7,8 | DEL-01-01/05 Design; design_hosting_access | Frozen prior contracts and observations | Named changes, source/consumer analysis and review | COMPLETE definition review V0-H-R1; product propagation remains |
| CC-R RS/EXEC CI1,3,4,9; D07/U08 | DEL-04-03/02-03 Design; design_records_exec | Frozen contracts; CI9 dependency need | Named changes preserve scope, validated schemas, consumer analysis/review | COMPLETE CC-R definition V0-RX; CI4 chosen; CI9 runtime ACTIVE parameterized W1 with approved29 dependency set |
| CC-A AAC CI5,6 | DEL-01-04 Design; design_aac | Frozen AAC/package/RS semantics | Named changes, binding/atomicity checks, independent review | COMPLETE definition V0-A; owner CI4 adopted; product capture/offer propagation remains |
| CC-X D49 | DEL-09-09 Design; group_a_route TASK | GROUP_SORT and SoW OUT-004 | Correct citation preserves contribution ladder; independent review | COMPLETE definition V0-RX; GUIDE pin adoption pending |
| V0 contract independent review | Run reviews only; contract_reviewer TASK | CC outputs fixed | Requirements/source comparison, consumer adoption findings | COMPLETE initial packages V0-T0/V0-RX/V0-A/V0-H-R1; later supplier/allocation/product slices need own affected review |
| T0 portable temp paths | app tests/docs; portable_temp TASK | Current tests | Unique platform temp dirs; offline tests pass | COMPLETE reviewed V0-T0; integrated current schema tests wait P0 |
| D0 dependency inventory | Run inventory only; dependency_inventory TASK | Cache/lockfile inspection | Missing files, sources, sizes; no downloads | COMPLETE preferred29 approved/retrieved verified, isolated offline cache admitted; see dependencies/DOWNLOAD_RESULT.md |
| SUP1 latest stock supplier adoption | DEL-01-01/05 Design hosting owner; app maintained pin P0 | Owner latest authorization, parent0.160 evidence, CC-H ready | Named consumer adoption and affected offline replay; no qualification implied | COMPLETE Design adoption/review V0-SUP1; P0-H app adoption ACTIVE |
| CC-P storage/native allocation adoption | DEL04-03/02-03 and DEL01-04 Design; original owners | Owner chosen reviewed proposal/native implementation | Named prose adoption, no schema narrowing, affected review | COMPLETE definition V0-P; P1 corrected/V0-ID ready; P0-ACT app adoption ACTIVE |
| CC-NPT-GEN native item generation | DEL01-03 Design; native_items_generation_design | Reviewed full H5 generation and SUP1 | Schema/prototype full tuple and delimiter-safe revision identity; independent review before I1 | COMPLETE definition V0-NPT-GEN, ready only inside explicit receiving-home namespace; standalone cross-home references need consumers |
| CP0 Design consumer propagation | affected GroupA and downstream Design pins/registries; one TASK owner | V0-H/A/RX ready definitions | Affected consumers triaged including DEL09-02/10-03, GUIDE/CA/DV; warranted adoption checked | PLANNED |
| P0-W1 validated writer | records/schema/Cargo/maintainedfixtures; runtime_schema_writer | Reviewed CC-R; approved29 | Completeentry preappend gate, no retrieval/fallback, meaningful refusaltests | COMPLETE bounded W1 V1-W1 reviewed; downstream fullwriter behavior P0-ACT |
| P0-API package/offer/capture validators | schema_validation/assets/tests; runtime_schema_writer | Reviewed CC-R/A | Source/hash sync6, fullshape/setup failures | COMPLETE consumer checks and V1-ACT review; six schema source/hash/ID checks pass |
| P0-ACT decision/capture/storage path | act/recorder/storage/records/readers/util/lib/actUI/selectedtests; act_storage_propagation | V0-A/P/ID/RX plus P0-API | CI3/4/5/6 conform; selected paths/UUID/recovery; no duplicates; offline checks and fresh review | COMPLETE V1-ACT-R2 repaired-scope review; combined offline checks pass; trusted persistent cold replay remains I3-CUST |
| P0-H hosting existing path | hosting/handshake/newhosttests; hosting_propagation | V0-H-R1 + V0-SUP1 | CI2fullidentity, CI7devLT24/nohash-onlyverified, CI8disclosure; actual0160offlinehandshake | COMPLETE V1-HOST-R2 reviewed existing path; combined source validation ahead |
| CC-CUST native-origin prerequisite | AAC/RS prose and app CI-10; original design owners/manager | V1-ACT ACT1, Root source disposition | Named clarification and fail-closed code backcheck, no seal adoption | COMPLETE V0-CUST source and V1-ACT code backchecks; trustworthy persistent replay remains I3-CUST |
| P0-I connected CI integration | Nodevalidation/runtimeUI/docs/issues; WORKING_ITEMS | P0-ACT/H/API ready and reviews | DirectDesignschema registration/no rewrite, wholeconnectedexistingpath passes, truthful issues/docs | COMPLETE PR1-INTEGRATION ready; Rust/Node/frontend/schema checks pass |
| P1 first reviewed code PR | P0 contracts/code/docs/current graph and evidence; manager commit, Root publishes | PR1 integration preservation verdict and existing required CI | First code slice merged; whole Group A stays active | READY all first-slice reviews/checks complete; manager commits and Root publishes |
| I1 hosting/recovery core | app hosting and recovery slice | CI2/7/8, provider/version choice where needed | Contract mapped offline lifecycle/request/recovery tests | PLANNED |
| I2 workflow/role/context supply | app workflow registration/execution supply slice | CC contracts | Tested source identity, parsing/supply failure behavior | PLANNED |
| I3-CUST trustworthy persistent replay | App sealing/provenance code and native evidence; manager/owner choice | Human SEAL-2 choice, explicit staged A/B signed-output join | Trusted cold replay and reader origin proof, tamper negatives; A retains obligation | BLOCKED choice pending; unverified replay remains held, unrelated slices continue |
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
- Initial contract definitions/T0/dependency preparation complete reviewed. Required P0 contract consumer code active; new I1–5 feature expansion waits existing connected path to prove all nine CI repairs. Parent0.160 live gpt-6.1-sol medium synthetic test passed; actual app model paths need bounded connecting-path checks.

## Current state and recovery

Maintainer: `/root/group_a_execution` WORKING_ITEMS under parent `/root` HELP_HUMAN. Native descendant mechanism, full launches/returns and hashes belong in this run. Bounded app scopes now released after initial contract review; disjoint owners above, shared integration/issue registry remain WORKING_ITEMS. Actor owns lib/act UI while hosting owner source-only separate module/tests; manager serializes host UI wiring after actor freeze. Parent owns human decision interface and Git publication coordination; manager records relayed actual decisions in OWNER_DECISIONS. No downloads, qualification, lifecycle changes or final gate acceptance.

Cross-group consumer propagation identified: CC-X changes XT hash pinned by D DEL-03-04 GUIDE; CC-R supplies changed RS/EXEC definitions/refs to D DEL-06-02/09-06/09-05/09-11 and GUIDE. CC-A capture/backlink semantics affect D decision view/standing reader and B conditional SEAL-2 packaging. No active receiving group graphs yet; carry these notices when formed (GC8). Definition change proposals do not make finished consumer work wrong silently; exact affected source pin/semantic reconciliation is a node before claiming ready consumption.

CI4 owner chose explicit label; pending only independent check/propagation. Owner selected reviewed App-local path/native allocation; namedCC-P adoption+product checks ahead. Host OI013 stays external/deferred. Full route readiness is contribution-specific in IMPLEMENTATION_ROUTE.md.

New CI-10 is tracked in app/CONTRACT_ISSUES.md and V1-ACT ACT1. Cold writable files do not establish native origin. Trusted in-memory retries and existing-record backlink repair proceed; trustworthy persisted replay remains required and depends on a concrete SEAL-2 custody choice, not an assumed JSON warrant. A read-only CAPTURE_CUSTODY_DECISION task prepares that choice for Root. No against-order dependency has been decided; any signing/packaging relationship is assessed before readiness.

Before I1 native-items code, adapt NPTD checklist plan-revision integer generation and its revision-ID grammar to the full H5 tuple under named change control (CI2 consumer follow-up). Its current schema/prototype is not a ready consumer of composite generation; this has no current P0 decision-path dependency.

GC-7 immediate source finding: Group B DEL-01-06 PKG I-4 supplies the signed App identity that Group A AAC SEAL-2 needs for native protected-key/replay proof. Code implementation can precede B packaging and qualification, but A native evidence cannot be declared supplied before that signed output exists. This conditional A-consumes-B point of need is brought to Root/human now; no cycle or regrouping decision is inferred. Carry into Group B's graph when it exists (GC-8). CAPTURE_CUSTODY_DECISION.md prepares the staged production/qualification choice; Group A retains its unfinished replay responsibility.

Remote recovery: initial graph checkpoint `cb5a88b29a` is pushed to `origin/codex/app-v4-group-a-90` with upstream configured by Root. No PR or merge yet; current product/review changes are local and uncommitted. First code slice has repaired-source reviews and combined checks; final manager glue/docs integration review is READY. Unrelated proposed CI or sealed replay work does not hold this slice.

Current operation: first-slice Git integration by WORKING_ITEMS/Root. PR1-INTEGRATION independently found no remaining glue/docs or integration findings. All product owners and reviewers returned frozen sources; writes are briefly held for commit/push/PR handling. Subsequent Group A slices continue from the reviewed base. No final receipt or whole-group acceptance is claimed at this boundary.
