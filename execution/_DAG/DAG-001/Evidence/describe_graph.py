#!/usr/bin/env python3
"""Record the assembler's bounded interpretation and provenance after assembly.

Writes only the authorized candidate account and Evidence records. It does not
edit graph rows, source/case/CP1 evidence, an accepted pointer or any status.
"""
import csv
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

C=Path(__file__).resolve().parent.parent
E=C/'Evidence'; X=C.parents[2]; R=X.parents[2]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def fp(p): return {'path':str(p.relative_to(R)), 'sha256':sha(p)}
def save(p,x): p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def read(p):
    with p.open(newline='') as f:return list(csv.DictReader(f))

checks=json.loads((E/'AssemblyChecks.json').read_text())
assert checks['result']=='PASS'
baseline=json.loads((E/'input_baseline.json').read_text())
for p,h in baseline['protected_inputs'].items(): assert sha(R/p)==h,p

# Run the workflow's explicit manifest-check command and keep its actual output.
argv=['sha256sum','-c','_DAG/_Candidates/DAG-001/SOURCE_MANIFEST.sha256']
p=subprocess.run(argv,cwd=X,text=True,capture_output=True)
(E/'manifest_check.stdout.txt').write_text(p.stdout)
(E/'manifest_check.stderr.txt').write_text(p.stderr)
assert p.returncode==0
save(E/'ManifestCheck_Run.json',{'arguments':argv,'cwd':str(X),'exit_code':p.returncode,'run_status':'COMPLETE','subject_status':'PASS','checked_entries':130,'tool':{'path':'/sbin/sha256sum','sha256':sha(Path('/sbin/sha256sum'))},'script':fp(Path(__file__))})

mirrors=read(E/'MirrorComparisons.csv')
findings=[]
for row in mirrors:
    other=row['Other'].split('#')[1].split('@')[0]
    if other=='DEP-01-05-013':
        account='Distinct contributions on one arc: selected pin/protocol and candidate-bound embedding qualification. Both remain required at their separate points of need (CASE-001).'
    elif other=='DEP-07-02-012':
        account='Distinct contributions on one arc: PEC receiving terms versus later exact envelope qualification/release/adoption evidence. Neither substitutes for the other (CASE-005).'
    elif other=='DEP-10-04-014':
        account='CONSTRAINT/HANDOVER describes consumption and supply of an accepted current graph once available. Both statements preserve later-use conditionality; neither requires an accepted graph to define the initial graph (CASE-006).'
    elif other in ['DEP-07-01-015','DEP-08-01-010','DEP-08-01-011']:
        account='Receiving terms/meanings and connector-specific case or question handoff are complementary contributions. Common recovery, case evidence and actual qualified/adopted input retain their separate conditions (CASE-005).'
    else:
        account='Supplier handoff/interface and consumer required-contribution statements are compatible in this bounded comparison. Broader contribution, focused fixtures and actual joined/receiving evidence remain distinct where stated; the representative does not replace the other obligation.'
    if 'SatisfactionStatus' in row['DifferentFields']:
        account+=' The two source satisfaction values are TBD/PENDING; neither states a satisfied input. Preserve both without normalization.'
    findings.append({'Representative':row['Representative'],'Other':row['Other'],'Standing':'NO_MATERIAL_CONTRADICTION_IDENTIFIED_IN_BOUNDED_COMPARISON','Assessment':account})
with (E/'MirrorAssessment.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(findings[0]),lineterminator='\n');w.writeheader();w.writerows(findings)
(E/'MirrorAssessment.md').write_text('''# Mirror and same-arc assessment

The assembler examined all 40 explicit comparisons in `MirrorComparisons.csv`: 38 counterpart-register mirrors and two same-register rows. All 40 have distinct statement text, 37 have different dependency types, and 13 have different satisfaction values. RequiredMaturity and ProposedMaturity match in every pair. The 13 satisfaction differences are TBD versus PENDING; none asserts fulfilment.

No material contradiction was identified in this bounded comparison of statements, types, maturity and status, informed by the supplied case and independent closure accounts. HANDOVER at the supplier and PREREQUISITE/INTERFACE/CONSTRAINT at the receiver usually describe compatible sides of a transfer. Distinct fixture/candidate/contract conditions remain additional obligations, not disposable duplicate text. This is not a new full semantic certification of all source SoWs or all 403 obligations.

The two SAME_ARC cases particularly require both obligations: DEP-01-05-012/013 distinguishes selected pin/protocol from candidate-bound embedding qualification; DEP-07-02-010/012 distinguishes actual PEC receiving terms from a later qualified/released/adopted-envelope account. CASE-005 additionally distinguishes connector meanings from actual case handoffs. DEP-10-02-012 and DEP-10-04-014 preserve the same later accepted/current-graph condition despite CONSTRAINT/HANDOVER types. No bootstrap graph prerequisite is introduced.

`MirrorAssessment.csv` records each compared pair and its assessment. Source paths, record ordinals, hashes, exact statements, evidence quotes and clause references remain in `MirrorComparisons.csv` and `all_execution_rows.csv`. No source repair is prescribed by this bounded assessment; a substantive contradiction found by independent review must remain a finding routed to both endpoint owners. SR-6 representatives remain selected by rule, and a future extra hold requires its actual warrant.
''')

account=['# Execution-row accounting','', 'All 403 ACTIVE EXECUTION rows occur exactly once: **109 admitted + 52 candidate + 242 excluded = 403**. Exclusions are 202 NOT_TOPOLOGICAL, 38 MIRROR and 2 SAME_ARC. The 355 active ANCHOR rows and one RETIRED execution row remain in their local registers, outside this denominator. No row is missing or counted twice.','',
'The 161 admitted/candidate representatives preserve all 29 core field values, including exact UTF-8 field bytes, from their source logical records; serialization/CSV quoting is not claimed identical. `all_execution_rows.csv` independently retains all 403 full core records, including every excluded obligation. Source file hashes and one-based logical record ordinals disambiguate locators. There are no duplicate source DependencyIDs.','',
'The 130-entry source manifest matches working bytes and source commit 85dcc17c3fda4bce82332a40f27aa9b4e849653e. The original 79 presentation members match their own preserved commit 2a461a47adee03bb868e433a73048265cc0be808, not later decision-applied case bytes. All 268 protected source/CP1/case/status/closure inputs remain unchanged. The node file retains its original bytes and all 41 accepted identities/paths.','',
'SCCs computed by the registered auditor on the 161 representative arcs match all six refreshed closure member sets exactly. The 52 held arcs represent 66 source rows, with 14 further intra-SCC mirrors/same-arc rows retained in exclusions. No type filter, SR-5 hold, cut, merge group or endpoint normalization is applied. Raw closure cyclicity remains expected.','',
'| Register owner | Total source | Anchors | Retired | Active execution | Admitted | Candidate | Excluded |','|---|---:|---:|---:|---:|---:|---:|---:|']
for r in read(E/'RegisterAccounting.csv'):
    account.append('| '+' | '.join(r[k] for k in ['DeliverableID','TotalRows','AnchorRows','RetiredRows','ActiveExecution','DependencyEdges.csv','CandidateEdges.csv','ExcludedRows.csv'])+' |')
account+=['| **Total** | **759** | **355** | **1** | **403** | **109** | **52** | **242** |','',
'`RegisterAccounting.csv` adds full register paths. `AssemblyChecks.json`, `SCC_Accounting.json`, `Tool_Run.json`, and `ManifestCheck_Run.json` carry checks and exact invocation/fingerprint evidence. Strict admitted audit exits 0; this is an admitted-topology result only. No acceptance, readiness, lifecycle or input fulfilment follows.']
(E/'Accounting.md').write_text('\n'.join(account)+'\n')

graph='''# DAG-001 — qualified initial graph candidate

**Basis confirmed; version assembled and audited. Independent version review is a separate required record; no graph-version acceptance or 30% passage is inferred.** Trigger: INITIAL. Predecessor: none. Case home: `_DAG/cases/`. No accepted `_DAG/_LATEST.md` exists or is written by this assembly.

The owner confirmed the full required-contribution basis and six characterized unresolved groups in [BASIS_DECISION.md](BASIS_DECISION.md), decision `APP-V4-DAG-BASIS-20260928-DECISION-1`, SHA256 `5a269b838d8e923cd4b9c4911b1128244d4854e33c0f4f1c7ab061d18b2acb60`. The exact 79-member proposal is preserved at `2a461a47adee03bb868e433a73048265cc0be808`; actual decision-applied origin is `0139b067dcc49cb0c90b7a250e4dd09b19250585`. The original reader, BASIS_* records and case history remain unchanged by assembly. Current graph files are derivatives, not bytes claimed previously presented or accepted.

The owner subsequently directed, via HELP_HUMAN and WORKING_ITEMS, that approval after completion and review of the combined final package will also pass the 30% gate. Graph acceptance and the 30% effect must therefore be explicit in that future single act, without inventing a second later approval turn. This assembly supplies only the graph component; WORKING_ITEMS prepares the final readiness/handoff account. That future approval has not occurred.

## Objective, semantics and coverage

The initial project graph accounts for production-order and route-selection relationships in this App project using the full required-contribution semantics: **the consumer requires the supplier's stated contribution, at the stated maturity/condition, before the stated part of its work**. It does not require every part of a supplier to finish before any part of a consumer begins. It is neither a cross-project graph nor a schedule.

Canonical arcs are consumer → supplier (depends on): UPSTREAM is From → Target; DOWNSTREAM is Target → From. Source Direction is preserved. No quotient node or Deliverable merge is used.

TrackingMode is FULL_GRAPH; Completeness is **FULL for the selected semantics, with the explicit unresolved-input/candidate qualifications below**. The accepted Group3 register `_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv` independently supplies 41 nodes in 11 packages, no exemptions. All 41 registers are PRESENT and FULL_GRAPH. [DeliverableNodes.csv](DeliverableNodes.csv) preserves accepted identities and actual paths byte for byte; no node is removed because it has held or unsatisfied inputs.

Dependency evidence is source `85dcc17c3fda4bce82332a40f27aa9b4e849653e`; [SOURCE_MANIFEST.sha256](SOURCE_MANIFEST.sha256) SHA256 `0b60d9a2a9342acf40ac7074876115954d897a7e595ec319b223e7460e0e80a4` binds 130 unchanged files. The refreshed closure is `_Evaluation/DepClosure/CLOSURE_APP_V4_TARGETS_2026-09-27_2237`, report SHA256 `6b0b0268e79315eddb4e2595dffd30e12b5f483bd6c74e2341be03b67d2a1a11`. Its input basis matches; the prior initial observation remains historical. Closure found no schema/orphan/declaration/isolated-node defect and identified six SCCs. Its raw-acyclic BLOCKER/subject FAIL does not demand resolution before 30%.

## Selection and complete row account

The confirmed default SR-1…SR-7 are applied in order from `chirality-root:bundled:workflow:project-dag`:

1. Use included registers at the frozen manifest.
2. Select ACTIVE EXECUTION canonical local-Deliverable target rows for topology; preserve non-Deliverable inputs in exclusions.
3. Admit all canonical dependency types to selection. No type-wide exclusion applies.
4. Apply no cut or graph merge-group ruling; none exists. CP1 case tracking is not such a ruling.
5. Apply no additional confirmation hold.
6. Choose one row per canonical arc: consumer UPSTREAM, then DECLARED before EXTRACTED, then lowest DependencyID. Retain other rows as MIRROR or SAME_ARC, pointing to the exact representative.
7. Hold every intra-SCC representative in the non-gating candidate layer, citing the refreshed SCC and actual continuing case. No arbitrary subset of cycle edges is removed.

| Account | Rows / arcs |
|---|---:|
| ACTIVE EXECUTION source rows | 403 |
| Admitted: DependencyEdges.csv | 109 |
| Held: CandidateEdges.csv | 52 |
| Excluded: NOT_TOPOLOGICAL | 202 |
| Excluded: MIRROR / SAME_ARC | 38 / 2 |
| Active ANCHOR / RETIRED execution, outside denominator | 355 / 1 |

The 201 local-target rows yield 161 representative arcs. Admitted + candidate + excluded is exactly 403, with zero overlap or missing rows. All 29 core fields of all 161 representatives match source values; the complete 403-row core account is additionally preserved in [Evidence/all_execution_rows.csv](Evidence/all_execution_rows.csv). Every exclusion has source identity, disposition and rule; every mirror/same-arc row names its representative. Full per-register balance and closure comparison are in [Evidence/Accounting.md](Evidence/Accounting.md).

## Unresolved groups and actual input conditions

All six current cases are EVIDENCE_ACCUMULATING with actual CP1 basis/case tracking confirmed; no case is closed. Table counts include every source row on held arcs, including excluded duplicates. Exact node sets appear in [Evidence/SCC_Accounting.json](Evidence/SCC_Accounting.json).

| Refreshed SCC / continuing case | Nodes | Held arcs / source rows | Work/input limits and future route under existing owners |
|---|---:|---:|---|
| SCC-001 / [SCC-CASE-001](../../cases/SCC-CASE-001/Case_Datasheet.md) | 2 | 2 / 4 | Supplier and account owners identify the actual selected pin/protocol, embedding contribution and conditional native-sign-in/substitution return. Definition may proceed; affected protocol/account implementation and qualification need their named inputs and observed evidence. |
| SCC-002 / [SCC-CASE-002](../../cases/SCC-CASE-002/Case_Datasheet.md) | 13 | 40 / 46 | Existing owners identify portable/native/workspace, catalog/proposal, policy-record, role and host receiving versions and compare actual contributions. Catalog/adapter definitions can proceed; dependent finalization, conformance and live witness claims need actual versions, policy, host outcomes and person acts. Extension trace production in DEL-09-09 remains distinct from the OI-003 owner ruling. |
| SCC-003 / [SCC-CASE-003](../../cases/SCC-CASE-003/Case_Datasheet.md) | 2 | 2 / 2 | Examination owner supplies reusable support/interfaces; packaging supplies the actual candidate and package/signing/entitlement evidence. Native smoke and packaged-witness claims require actual native evidence. Support/case definition does not require completed future witnesses. Public-release-only terms remain at their separate point of need. |
| SCC-004 / [SCC-CASE-005](../../cases/SCC-CASE-005/Case_Datasheet.md) | 3 | 4 / 8 | Common source-file recovery and connector owners coordinate meanings and cases. Later PEC use requires exact qualification/release/adoption evidence; Domains reliance requires actual admitted sources/query/boundary inputs and preserves unresolved provider allocation. Neither connector's availability gates initial App or ordinary-file recovery. |
| SCC-005 / [SCC-CASE-006](../../cases/SCC-CASE-006/Case_Datasheet.md) | 2 | 2 / 3 | Undertaking/dependency owners identify applicable current control/practice records for initial graph examination. An actual accepted/current graph is needed for later graph-based selection. No already-accepted-graph bootstrap requirement or completed-controls blanket hold is introduced. |
| SCC-006 / [SCC-CASE-007](../../cases/SCC-CASE-007/Case_Datasheet.md) | 2 | 2 / 3 | Continuity and replacement-evidence owners identify current account, baseline and actual candidate dossiers. A later attributable owner disposition returns to continuity when supplied. Recording an act never performs it; favorable replacement, adoption or retirement is not inferred. |

SCC-002 actually continues CASE-002 for all 13 nodes; [CASE-004](../../cases/SCC-CASE-004/Case_Datasheet.md) remains constituent history of its original catalog/proposal inquiry. Original CASE-002 nine-member history also remains. This changes case tracking only, not scope, responsibilities, Deliverable identity or graph merge groups. Historical proposed/pending passages in preserved case bodies are governed by their current confirmed-tracking preface and actual ruling rows, rather than silently rewritten.

The candidate layer is **non-gating**. It supplies no waves, schedules, priorities, blocker queues or dispatch-readiness verdicts. An acyclic admitted layer neither resolves these SCCs nor supplies their missing contributions. Only work that actually needs a missing contribution is limited at that point. No further SCC-resolution or interface-production tranche is inserted as a pre-30% condition.

## Inputs outside topology, mirrors and findings

All 202 non-topological rows remain explicit in [Evidence/NonTopologicalInputs.csv](Evidence/NonTopologicalInputs.csv): 144 EXTERNAL, 26 DOCUMENT, 18 PACKAGE and 14 UNKNOWN. The 32 package/unknown rows retain the independent audit's row-specific A/B/C account: A is established allocation/partial support; B is a future actual candidate, source/value, contract subset or recipient instance; C is a genuine technical/allocation choice with its recorded actor. Mixed classes remain mixed. These are not 32 new human choices. Package membership is not expanded into guessed dependencies, and a known producer does not supply its actual value or contribution.

SWB/PEC/provider construction, receiving qualification/adoption, actual human decisions and source admission remain separately owned/evidenced. The known selected-pin producer remains distinct from its still-open actual value. Existing policy, catalog/schema/encoding, host/model placement/interface and Domains admission/allocation choices keep their existing points of need. INITIALIZED is checked-contract maturity only: 195 execution rows require it; 208 require TBD. Satisfaction remains 278 TBD and 125 PENDING, with none SATISFIED. No field is promoted.

[Evidence/MirrorAssessment.md](Evidence/MirrorAssessment.md) and its 40-row comparison/assessment account preserve all distinct obligations. There are 37 type differences and 13 TBD/PENDING differences, but no maturity difference. No material contradiction was identified in the bounded comparison: supplier HANDOVER and consumer prerequisite/interface/constraint commonly describe complementary contributions. In particular pin versus qualification, PEC terms versus later envelope evidence, and current-graph later-use conditions remain distinct. A representative never erases these obligations. Any contradiction found by separate review must remain a finding routed to both source owners; this account does not certify all source semantics afresh.

## Verification, reproduction and limits

The registered `tools/coordination/audit_dag.py` ran on the 161-arc admissible set, then with `--canonical --strict` on the 109-arc admitted layer, and optionally on candidates. Strict admitted exit is **0 / PASS**: zero canonical, schema, endpoint, ragged-edge, SCC, duplicate-arc or bidirectional-pair findings. Additional checks cover all 41 node rows, node identities/paths, self-loops, source field fidelity and row accounting. All 41 nodes are touched even in the admitted layer; this does not establish input availability. The raw 21-degree record-interface hub and six SCCs remain characterized source observations.

Non-strict admissible/candidate audits exit 0 because their process completed, while cyclic subjects remain FAIL against an acyclic objective. Their six exact SCC member sets agree with refreshed closure. No strictness exception is taken. No DEV-001 markdown is published or relied upon; the tool's project-specific `dev001_projection` JSON and legacy source-docstring authority wording do not govern this graph. Actual tool/script hashes and exact arguments are in [Evidence/Tool_Run.json](Evidence/Tool_Run.json) and [Evidence/ManifestCheck_Run.json](Evidence/ManifestCheck_Run.json).

From repository root, run `python3 projects/chirality-app-v4/execution/_DAG/_Candidates/DAG-001/Evidence/assemble_graph.py`, then the adjacent `describe_graph.py` for this account. These are bounded assembly reruns, not independent review. They preserve protected inputs and write only authorized candidate files. The second script records the explicit `sha256sum -c` invocation from EXECUTION_ROOT. [SOURCE_BASIS.json](SOURCE_BASIS.json) records exact source/decision/history/method/tool origins; [ASSEMBLY_RUN.md](ASSEMBLY_RUN.md) records parentage and the host-versus-brief limit.

The next action is separate independent version review and manager integration into the completed final package for the owner's combined decision. This assembly creates no accepted snapshot/pointer, readiness claim, lifecycle transition, fulfilled input, provider/product activation, release, adoption or professional act.
'''
(C/'GRAPH_BASIS.md').write_text(graph)

run=json.loads((E/'Tool_Run.json').read_text())
cases=json.loads((E/'SCC_Accounting.json').read_text())
for case in cases:
    d=X/case['CaseRef']
    case['basis_ruling_id']='CP1-20260928'
    case['ruling']=fp(d/'Ruling_Register.csv')
    case['current_tracking']=fp(d/'Case_Datasheet.md')
    case['evidence_register']=fp(d/'Evidence_Register.csv')
source_basis={
 'GraphID':'DAG-001','trigger':'INITIAL','predecessor':None,
 'standing':'BASIS_CONFIRMED; VERSION_ASSEMBLED_CHECKED; INDEPENDENT_VERSION_REVIEW_PENDING; VERSION_AND_30_NOT_ACCEPTED',
 'source_revision':'85dcc17c3fda4bce82332a40f27aa9b4e849653e',
 'decision_applied_revision':'0139b067dcc49cb0c90b7a250e4dd09b19250585',
 'working_state':'Assembly derivatives in the current working tree; all 130 source inputs match their frozen commit; all 268 protected inputs unchanged. No Git mutation by assembler.',
 'manifest':fp(C/'SOURCE_MANIFEST.sha256'),'source_members':130,
 'inventory_source':fp(X/'_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv'),
 'node_count':41,'package_count':11,'exempt_units':[],'tracking_mode':'FULL_GRAPH','completeness':'FULL with characterized unresolved candidate/input qualifications',
 'basis_decision':fp(C/'BASIS_DECISION.md'),
 'presentation':{'revision':'2a461a47adee03bb868e433a73048265cc0be808','member_count':79,'manifest':fp(C/'BASIS_MANIFEST.json'),'reader':fp(C/'READER.md'),'all_members_verified_at_presented_revision':True,'scope':'Original CP1 presentation only; current graph/case derivatives are not retrospectively attributed to it.'},
 'future_decision':{'owner_direction':'After the completion of your work you just described I will review and when I approve that is the 30% gate being passed.','custody':'WORKING_ITEMS message to this TASK, relaying HELP_HUMAN and actual owner direction; not a raw platform export','effect':'Future combined final-package approval will explicitly carry graph acceptance and 30% effects; neither has occurred; no second later 30% approval turn prescribed.'},
 'closure_snapshots':[{'path':str((X/'_Evaluation/DepClosure/CLOSURE_APP_V4_TARGETS_2026-09-27_2237').relative_to(X)),'report':fp(X/'_Evaluation/DepClosure/CLOSURE_APP_V4_TARGETS_2026-09-27_2237/Dependency_Closure_Report.md'),'source_revision':'85dcc17c3fda4bce82332a40f27aa9b4e849653e','manifest_sha256':sha(C/'SOURCE_MANIFEST.sha256'),'admissible_scc_member_sets_match':True,'process':'COMPLETE / exit 0','subject':'FAIL raw acyclic objective; characterized unresolved work, no gate verdict'}],
 'source_history':[{'source_revision':'c1038ae5ac5c23a30ea7d3b516cd9033cb47f77b','closure':'_Evaluation/DepClosure/CLOSURE_APP_V4_INITIAL_2026-09-27_2149','standing':'Historical first observation; unaffected semantic audit reused by refreshed independent auditor, not silently rebound.'}],
 'cases':cases,'case_history':{'CaseID':'SCC-CASE-004','path':'_DAG/cases/SCC-CASE-004','current_tracking':fp(X/'_DAG/cases/SCC-CASE-004/Case_Datasheet.md'),'ruling':fp(X/'_DAG/cases/SCC-CASE-004/Ruling_Register.csv'),'standing':'Retained original two-member inquiry/constituent history linked to actual continuing CASE-002; no separate current SCC or closure claim'},
 'selection':{'rules':'SR-1 through SR-7 defaults','canonical_arc':'consumer to supplier; DOWNSTREAM reverses written endpoints','types':'all canonical','extra_confirmation_hold':False,'cut_rulings':[],'graph_merge_groups':[],'identity_normalization':False},
 'counts':checks,'selected_context':run['selected_context'],
 'additional_consultation':[fp(R/'docs/SPEC.md')],
 'tools':[fp(R/'tools/coordination/audit_dag.py'),fp(E/'assemble_graph.py'),fp(E/'describe_graph.py')],
 'tool_runs':'Evidence/Tool_Run.json','manifest_check_run':'Evidence/ManifestCheck_Run.json','protected_input_fingerprints':'Evidence/input_baseline.json',
 'graph_files':[fp(C/name) for name in ['GRAPH_BASIS.md','DeliverableNodes.csv','DependencyEdges.csv','CandidateEdges.csv','ExcludedRows.csv']],
 'authority_limits':'No accepted pointer/snapshot, graph-version acceptance, 30% act, readiness, source satisfaction, lifecycle, SCC closure, scope/Deliverable merge, product/provider activation, release/adoption or professional act.'
}
save(C/'SOURCE_BASIS.json',source_basis)

(C/'ASSEMBLY_RUN.md').write_text('''# DAG-001 bounded assembly return

TASK `/root/renewal_research_strategy/dag_version_assembly` executed under WORKING_ITEMS `/root/renewal_research_strategy`, itself under HELP_HUMAN. Mechanism: actual delegated-harness-native child. The role ceiling and exact `ASSEMBLY_BRIEF.md` bound this assignment. No child delegation, external messaging or Git mutation occurred. No different model family or independent-review identity is claimed. The inherited Codex model is not independently identified beyond the host-supplied context.

Selected method: `chirality-root:bundled:workflow:project-dag`, bounded assembly under Stage 4. Root/TASK, catalog descriptor, entrypoint, contract, method and graph-version rules were read. `Tool_Run.json` fingerprints those exact files and the dispatch brief. `SOURCE_BASIS.json` and `input_baseline.json` bind actual source, case, CP1 and closure inputs; targeted SPEC/tool, case contribution/evidence/ruling records, refreshed closure report/QA and target account informed the assembly. Broader case bodies were consulted selectively; no exhaustive new source semantic certification is claimed.

Host permissions allow broader workspace writes/tools; the brief is narrower and is followed by this TASK rather than enforced by a separate OS sandbox. Writes are only GRAPH_BASIS.md, unchanged-byte DeliverableNodes.csv, DependencyEdges.csv, CandidateEdges.csv, ExcludedRows.csv, SOURCE_BASIS.json, Evidence/ and this run file. All BASIS_* files, original READER, SOURCE_MANIFEST, local registers/indices/SoWs/statuses, cases and closure inputs remain unchanged. No accepted pointer or DAG snapshot was created.

Actual result: **41 nodes; 109 admitted arcs; 52 non-gating held arcs in six groups; 242 exclusions = 202 non-topological + 38 mirrors + 2 same-arc rows.** All 403 active execution rows are accounted exactly once. The 355 active anchors and one retired execution row stay outside the denominator. All 29 core fields match for all 161 representatives and the supplemental 403-row account. All 130 source inputs match frozen working and committed bytes; the 79 historical presentation members match their own preserved revision. All 268 protected inputs remain unchanged.

The registered admissible audit completed (exit 0) and found the expected six SCCs/161 arcs. The registered canonical strict admitted audit exited 0 with no graph/schema/canonical/endpoint findings. Optional candidate audit completed (exit 0) with the same six cyclic groups as expected. Exact arguments, hashes, outputs and process-versus-subject status are retained. Additional checks cover node widths, identities/paths, self-loops, complete accounting/fidelity and exact closure member sets. CASE-002 actually continues the expanded 13-member group; CASE-004 remains history, not a Deliverable or graph merge.

An initial assembly attempt stopped before any auditor invocation because default LF CSV serialization differed from the existing node file bytes. The script now independently regenerates and checks node values/paths, then preserves the original node serialization from the verified presentation revision. Source/case/CP1 files were never changed, and the rerun confirms unchanged node bytes. This was an assembly serialization repair, not a source repair or re-freeze. The successful attempt invoked each of the three graph audits once.

The assembler examined all 40 mirror/same-arc comparisons and identified no material contradiction in that bounded scope. All distinct obligations, 202 non-topological inputs and mixed A/B/C conditions remain visible. Maturity is still 195 INITIALIZED / 208 TBD; satisfaction remains 278 TBD / 125 PENDING. INITIALIZED is checked-contract maturity, not an actual input receipt or performed act.

WORKING_ITEMS relayed the owner's later direction: “After the completion of your work you just described I will review and when I approve that is the 30% gate being passed.” This return therefore does not prescribe a separate subsequent 30% prompt. The manager prepares the completed combined package and records the two effects of the future single approval explicitly. No such approval has occurred here.

Return standing: assembly complete for separate independent version review. Review and final package integration remain with the caller. Candidate edges remain non-gating; no schedule, wave, priority, blocker queue or readiness verdict is produced. No further SCC-resolution/interface-production work is added as a pre-30% condition. Graph acceptance, 30%, input fulfilment, lifecycle, provider/product work and actual human acts are not inferred.
''')

for p,h in baseline['protected_inputs'].items():assert sha(R/p)==h,p
assert sha(C/'DeliverableNodes.csv')==baseline['nodes_before']
# Stable return manifest covers actual output bytes without a self-reference.
files=[C/n for n in ['GRAPH_BASIS.md','DeliverableNodes.csv','DependencyEdges.csv','CandidateEdges.csv','ExcludedRows.csv','SOURCE_BASIS.json','ASSEMBLY_RUN.md']]
files+=sorted(p for p in E.iterdir() if p.is_file() and p.name!='ASSEMBLY_OUTPUT_MANIFEST.json')
save(E/'ASSEMBLY_OUTPUT_MANIFEST.json',{'standing':'ASSEMBLED_UNACCEPTED_REVIEW_SUBJECT','files':[fp(p) for p in files],'self_excluded':'Evidence/ASSEMBLY_OUTPUT_MANIFEST.json','source_manifest_sha256':sha(C/'SOURCE_MANIFEST.sha256')})
print(json.dumps({'result':'PASS','output_files':len(files),'manifest':fp(E/'ASSEMBLY_OUTPUT_MANIFEST.json'),'graph_basis':fp(C/'GRAPH_BASIS.md'),'source_basis':fp(C/'SOURCE_BASIS.json')},indent=2))
