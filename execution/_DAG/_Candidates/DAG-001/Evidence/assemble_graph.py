#!/usr/bin/env python3
"""Bounded DAG-001 assembly; reruns only the authorized graph/evidence files.

Source registers, cases, CP1 presentation/decision records, and manifest are
read-only.  This does not publish or accept a graph, decide a gate, or schedule.
"""
from __future__ import annotations
import ast
import csv
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

CANDIDATE = Path(__file__).resolve().parent.parent
EVIDENCE = CANDIDATE / 'Evidence'
EXECUTION = CANDIDATE.parents[2]
ROOT = EXECUTION.parents[2]
SOURCE = '85dcc17c3fda4bce82332a40f27aa9b4e849653e'
PRESENTED = '2a461a47adee03bb868e433a73048265cc0be808'
DECISION_REV = '0139b067dcc49cb0c90b7a250e4dd09b19250585'
MANIFEST_HASH = '0b60d9a2a9342acf40ac7074876115954d897a7e595ec319b223e7460e0e80a4'
DECISION_HASH = '5a269b838d8e923cd4b9c4911b1128244d4854e33c0f4f1c7ab061d18b2acb60'
CLOSURE = EXECUTION / '_Evaluation/DepClosure/CLOSURE_APP_V4_TARGETS_2026-09-27_2237'
INVENTORY = '_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv'
TOOL = ROOT / 'tools/coordination/audit_dag.py'
CASE_MAP = {f'SCC-{i:03}': f'SCC-CASE-{j:03}' for i,j in [(1,1),(2,2),(3,3),(4,5),(5,6),(6,7)]}
PROVENANCE = ['SourceRegister','SourceRegisterSHA256','SourceRecord','SelectionRule']
CANDIDATE_COLS = ['CandidateReason','SCCRef','CaseRef','OpenQuestion']
EXCLUDE_COLS = ['SourceRegister','SourceRegisterSHA256','SourceRecord','DependencyID','FromDeliverableID','Direction','DependencyType','TargetType','TargetDeliverableID','TargetRefID','Disposition','RuleOrRuling','RepresentedBy','Notes']
NODE_COLS = ['DeliverableID','PackageID','DeliverableName','ExecutionPath','DependenciesPath','RegisterState','TrackingMode','InventorySource']
QUESTIONS = {
 'SCC-001': 'Identify the selected pin/protocol and embedding contribution, account/provider observations and exact conditional supplier-return criterion; qualify only with actual inputs at their point of need. See case contribution and missing-input account.',
 'SCC-002': 'Identify and compare actual portable/native/workspace, C/P/catalog, policy-record, role and host receiving versions; preserve actual trace production separately from OI-003 owner ruling and host/person acts. Future/post30 input-specific work; see continuing CASE-002 and retained CASE-004 history.',
 'SCC-003': 'Identify usable examination-support interfaces and the actual package/configuration/signing/entitlement evidence for native smoke and packaged-witness reliance; support definition may proceed before actual native evidence.',
 'SCC-004': 'Identify common recovery and connector-specific terms/cases; later PEC qualification/release/adoption and Domains admission/query/boundary evidence remain separate. No connector availability gate for initial App or ordinary-file recovery.',
 'SCC-005': 'Identify applicable current control/practice records for graph examination and actual later accepted/current graph for graph-based selection. Current records support initial definition without an already accepted graph.',
 'SCC-006': 'Identify the current continuity account and actual candidate/baseline dossiers; return a later attributable owner disposition when supplied. Recording never performs the act or implies favorable replacement, adoption or retirement.'
}

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def rel(path): return str(Path(path).relative_to(ROOT))
def read(path):
    with Path(path).open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f); rows = list(reader)
        assert all(None not in row and None not in row.values() for row in rows), f'Ragged {path}'
        return reader.fieldnames, rows
def write(path, columns, rows):
    with Path(path).open('w', encoding='utf-8', newline='') as f:
        w=csv.DictWriter(f, fieldnames=columns, extrasaction='ignore', lineterminator='\n')
        w.writeheader(); w.writerows(rows)
def save(path, value): Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')
def git_bytes(revision, path):
    return subprocess.check_output(['git','show',f'{revision}:{rel(path)}'],cwd=ROOT)
def fingerprint(path): return {'path':rel(path),'sha256':sha(path)}
def key(row): return (row['SourceRegister'], row['DependencyID'], str(row['SourceRecord']))
def locator(row): return f"{row['SourceRegister']}#{row['DependencyID']}@{row['SourceRecord']}"
def arc(row):
    pair=(row['FromDeliverableID'],row['TargetDeliverableID'])
    return pair if row['Direction']=='UPSTREAM' else pair[::-1]
def rank(row): return (row['Direction']!='UPSTREAM',row['Origin']!='DECLARED',row['DependencyID'])

def main():
    EVIDENCE.mkdir(exist_ok=True)
    # Read registered definitions without importing (and without creating pycache).
    tree=ast.parse(TOOL.read_text())
    definitions={n.targets[0].id:ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ['REQUIRED_COLUMNS','CANONICAL_ENUMS']}
    core=definitions['REQUIRED_COLUMNS']; enums=definitions['CANONICAL_ENUMS']; assert len(core)==29
    manifest=CANDIDATE/'SOURCE_MANIFEST.sha256'; assert sha(manifest)==MANIFEST_HASH
    assert sha(CANDIDATE/'BASIS_DECISION.md')==DECISION_HASH
    source_entries=[]
    for line in manifest.read_text().splitlines():
        expected, path=line.split('  ',1); p=EXECUTION/path
        assert sha(p)==expected, f'Manifest moved: {path}'
        assert hashlib.sha256(git_bytes(SOURCE,p)).hexdigest()==expected, f'Committed basis mismatch: {path}'
        source_entries.append({'path':rel(p),'sha256':expected})
    assert len(source_entries)==130
    protected={item['path']:item['sha256'] for item in source_entries}
    protected_paths=[manifest,CANDIDATE/'READER.md',*CANDIDATE.glob('BASIS_*'),*(EXECUTION/'_DAG/cases').rglob('*'),*EXECUTION.glob('PKG*/1_Working/DEL*/_STATUS.md'),*CLOSURE.rglob('*')]
    for p in protected_paths:
        if p.is_file(): protected[rel(p)]=sha(p)
    baseline=EVIDENCE/'input_baseline.json'
    if baseline.exists():
        existing=json.loads(baseline.read_text())
        assert existing['protected_inputs']==protected, 'Protected input changed since initial assembly'
    else:
        save(baseline,{'captured_at':datetime.now(timezone.utc).isoformat(),'protected_inputs':protected,'nodes_before':sha(CANDIDATE/'DeliverableNodes.csv')})
    initial=json.loads(baseline.read_text())
    # Historical presentation is checked against its own commit, never current case bytes.
    presentation=json.loads((CANDIDATE/'BASIS_MANIFEST.json').read_text())
    for item in presentation['files']:
        assert hashlib.sha256(git_bytes(PRESENTED,ROOT/item['path'])).hexdigest()==item['sha256'],item['path']
    assert len(presentation['files'])==79
    assert git_bytes(DECISION_REV,CANDIDATE/'BASIS_DECISION.md')==(CANDIDATE/'BASIS_DECISION.md').read_bytes()
    assert sha(CLOSURE/'Dependency_Closure_Report.md')=='6b0b0268e79315eddb4e2595dffd30e12b5f483bd6c74e2341be03b67d2a1a11'
    closure_tool=json.loads((CLOSURE/'Tool_Run.json').read_text())
    assert closure_tool['source_revision']==SOURCE
    # Inventory is derived from accepted rows; actual folder paths are matched by exact IDs.
    _, inventory=read(EXECUTION/INVENTORY); assert len(inventory)==41
    ids={x['DeliverableID'] for x in inventory}; assert len(ids)==41
    nodes=[]
    for x in sorted(inventory,key=lambda x:x['DeliverableID']):
        paths=list(EXECUTION.glob(f"{x['PackageID']}_*/1_Working/{x['DeliverableID']}_*")); assert len(paths)==1
        p=paths[0]; h,rr=read(p/'Dependencies.csv')
        assert h[:29]==core and len(h)==len(set(h))
        assert 'FULL_GRAPH' in (p/'_DEPENDENCIES.md').read_text()
        nodes.append(dict(zip(NODE_COLS,[x['DeliverableID'],x['PackageID'],x['Name'],str(p.relative_to(EXECUTION)),str((p/'Dependencies.csv').relative_to(EXECUTION)),'PRESENT','FULL_GRAPH',INVENTORY])))
    assert read(CANDIDATE/'DeliverableNodes.csv')[1]==nodes, 'Canonical nodes disagree with prior inventory'
    # The accepted inventory has been independently regenerated and compared.
    # Retain original CSV serialization as well as the same values and paths.
    preserved_nodes=git_bytes(PRESENTED,CANDIDATE/'DeliverableNodes.csv')
    assert hashlib.sha256(preserved_nodes).hexdigest()==initial['nodes_before']
    (CANDIDATE/'DeliverableNodes.csv').write_bytes(preserved_nodes)
    assert sha(CANDIDATE/'DeliverableNodes.csv')==initial['nodes_before'], 'Node bytes changed'
    assert not (EXECUTION/'_DAG/_LATEST.md').exists()
    all_rows=[]; active=[]; per_register={}; groups=defaultdict(list); exclusions=[]
    for node in nodes:
        source=node['DependenciesPath']; p=EXECUTION/source; _, rows=read(p)
        counts=Counter(); counts['TotalRows']=len(rows)
        seen=set()
        for ordinal,r in enumerate(rows,1):
            assert r['DependencyID'] not in seen, f'Duplicate source ID: {p}'; seen.add(r['DependencyID'])
            assert r['FromDeliverableID']==node['DeliverableID']
            assert r['FromPackageID']==node['PackageID']
            assert all(r[field] in values for field,values in enums.items()), f'Invalid enum {p}:{ordinal}'
            assert r['RegisterSchemaVersion']=='v3.1'
            out={k:r[k] for k in core};out.update(SourceRegister=source,SourceRegisterSHA256=sha(p),SourceRecord=str(ordinal),SelectionRule='')
            all_rows.append(out)
            if r['DependencyClass']=='ANCHOR': counts['AnchorRows']+=1
            if r['Status']=='RETIRED': counts['RetiredRows']+=1
            if r['Status']!='ACTIVE' or r['DependencyClass']!='EXECUTION':continue
            active.append(out);counts['ActiveExecution']+=1
            if r['TargetType']!='DELIVERABLE':
                exclusions.append({**out,'Disposition':'NOT_TOPOLOGICAL','RuleOrRuling':'SR-2','RepresentedBy':'','Notes':'Non-deliverable input retained unchanged in source and Evidence/all_execution_rows.csv; exclusion supplies no contribution or readiness.'})
            else:
                assert r['TargetDeliverableID'] in ids and re.fullmatch(r'DEL-\d{2}-\d{2}',r['TargetDeliverableID'])
                assert r['DependencyType'] in enums['DependencyType']
                groups[arc(out)].append(out)
        per_register[source]={'DeliverableID':node['DeliverableID'],**counts}
    assert len(all_rows)==759 and len(active)==403 and len(groups)==161
    admissible=[]; mirror_pairs=[]
    for pair, rows in sorted(groups.items()):
        ordered=sorted(rows,key=rank); representative=ordered[0]
        representative['SelectionRule']='SR-1;SR-2;SR-3(all canonical types);SR-4(no cut/merge ruling);SR-5(not applied);SR-6'
        admissible.append(representative)
        for other in ordered[1:]:
            disposition='MIRROR' if other['SourceRegister']!=representative['SourceRegister'] else 'SAME_ARC'
            exclusions.append({**other,'Disposition':disposition,'RuleOrRuling':'SR-6','RepresentedBy':locator(representative),'Notes':'Topology represented once; original contribution, type, conditions, maturity and satisfaction remain live source obligations. See Evidence/MirrorComparisons.csv.'})
            mirror_pairs.append((pair,representative,other,disposition))
    write(EVIDENCE/'admissible_edges.csv',core+PROVENANCE,admissible)
    runs=[]
    def audit(name, args, subject):
        argv=['python3',rel(TOOL),*args];p=subprocess.run(argv,cwd=ROOT,text=True,capture_output=True)
        (EVIDENCE/(name+'.stdout.txt')).write_text(p.stdout);(EVIDENCE/(name+'.stderr.txt')).write_text(p.stderr)
        runs.append({'name':name,'tool':fingerprint(TOOL),'arguments':argv,'cwd':str(ROOT),'exit_code':p.returncode,'run_status':'COMPLETE' if p.returncode==0 else 'FAILED','subject_status':subject,'stdout':f'{name}.stdout.txt','stderr':f'{name}.stderr.txt'})
        assert p.returncode==0,p.stdout+p.stderr
    audit('admissible_audit',['--edges',rel(EVIDENCE/'admissible_edges.csv'),'--nodes',rel(CANDIDATE/'DeliverableNodes.csv'),'--canonical','--json-out',rel(EVIDENCE/'admissible_audit.json')],'FAIL_RAW_ACYCLIC_OBJECTIVE; CHARACTERIZED_UNRESOLVED_CYCLES')
    raw=json.loads((EVIDENCE/'admissible_audit.json').read_text());_, scc_rows=read(CLOSURE/'Evidence/scc_summary.csv')
    scc_sets={x['SCC_ID']:set(x['Nodes'].split(';')) for x in scc_rows}
    assert {frozenset(s) for s in raw['active_graph']['sccs']}=={frozenset(s) for s in scc_sets.values()}
    assert raw['canonical_finding_count']==0 and raw['endpoint_issue_count']==0
    assert raw['active_graph']['edge_count']==161 and raw['active_graph']['scc_count']==6
    member_to_scc={n:s for s,ns in scc_sets.items() for n in ns}
    admitted=[];candidates=[]
    for row in admissible:
        a,b=arc(row); s=member_to_scc.get(a)
        assert a!=b, 'Unexpected self-loop requires characterized case'
        if s and s==member_to_scc.get(b):
            case='_DAG/cases/'+CASE_MAP[s]
            _, rulings=read(EXECUTION/case/'Ruling_Register.csv')
            assert any(x['RulingID']=='CP1-20260928' and x['Status']=='RECORDED_ACTUAL_BASIS_ONLY' for x in rulings)
            candidates.append({**row,'SelectionRule':row['SelectionRule']+';SR-7(held)','CandidateReason':'SCC_UNRESOLVED','SCCRef':s,'CaseRef':case,'OpenQuestion':QUESTIONS[s]})
        else: admitted.append({**row,'SelectionRule':row['SelectionRule']+';SR-7(admitted)'})
    exclusions.sort(key=key)
    write(CANDIDATE/'DependencyEdges.csv',core+PROVENANCE,admitted)
    write(CANDIDATE/'CandidateEdges.csv',core+PROVENANCE+CANDIDATE_COLS,candidates)
    write(CANDIDATE/'ExcludedRows.csv',EXCLUDE_COLS,exclusions)
    audit('dag_audit',['--dag-dir',rel(CANDIDATE),'--canonical','--strict','--json-out',rel(EVIDENCE/'dag_audit.json')],'PASS_ADMITTED_LAYER_ONLY')
    audit('candidate_audit',['--dag-dir',rel(CANDIDATE),'--edges',rel(CANDIDATE/'CandidateEdges.csv'),'--canonical','--json-out',rel(EVIDENCE/'candidate_audit.json')],'FAIL_ACYCLIC_OBJECTIVE_EXPECTED; NON_GATING_CANDIDATE_LAYER')
    # Verify serialized output rather than just construction data.
    admitted=read(CANDIDATE/'DependencyEdges.csv')[1];candidates=read(CANDIDATE/'CandidateEdges.csv')[1];exclusions=read(CANDIDATE/'ExcludedRows.csv')[1]
    original={key(x):x for x in active};placements={};fidelity=0
    for filename,rows in [('DependencyEdges.csv',admitted),('CandidateEdges.csv',candidates),('ExcludedRows.csv',exclusions)]:
        for x in rows:
            k=key(x);assert k in original and k not in placements;placements[k]=filename
            src=original[k];assert x['SourceRegisterSHA256']==src['SourceRegisterSHA256']
            if filename!='ExcludedRows.csv':
                assert all(x[f]==src[f] and x[f].encode('utf-8')==src[f].encode('utf-8') for f in core)
                fidelity+=1
            else:
                assert all(x[f]==src[f] for f in EXCLUDE_COLS[:10])
    assert set(placements)==set(original)
    assert (len(admitted),len(candidates),len(exclusions))==(109,52,242)
    # Supplemental complete source-core account preserves excluded input obligations.
    evidence_rows=[]
    for x in active:
        y={**x,'AccountingLayer':placements[key(x)]};evidence_rows.append(y)
        per_register[x['SourceRegister']][placements[key(x)]]=per_register[x['SourceRegister']].get(placements[key(x)],0)+1
    write(EVIDENCE/'all_execution_rows.csv',core+PROVENANCE+['AccountingLayer'],evidence_rows)
    for x in read(EVIDENCE/'all_execution_rows.csv')[1]: assert all(x[f]==original[key(x)][f] for f in core)
    # Carry A/B/C descriptions verbatim from the independent refreshed account.
    classification={}
    for line in (CLOSURE/'Dependency_Closure_Report.md').read_text().splitlines():
        cells=[s.strip() for s in line.strip().strip('|').split('|')]
        if len(cells)==4 and re.fullmatch(r'DEP-\d{2}-\d{2}-\d{3}',cells[0]) and cells[1].startswith(('PACKAGE /','UNKNOWN /')):
            classification[cells[0]]=(cells[2],cells[3])
    non_topological=[]
    for x in active:
        if x['TargetType']=='DELIVERABLE':continue
        info=classification.get(x['DependencyID'],('NOT_CLASSIFIED_A_B_C','External/document input retained at its source point of need; no new human-choice classification inferred.'))
        if x['TargetType'] in ['PACKAGE','UNKNOWN']: assert x['DependencyID'] in classification
        non_topological.append({**x,'InputClass':info[0],'InputAccount':info[1],'AccountSource':str((CLOSURE/'Dependency_Closure_Report.md').relative_to(EXECUTION)) if x['DependencyID'] in classification else x['SourceRegister']})
    assert len(classification)==32 and len(non_topological)==202
    write(EVIDENCE/'NonTopologicalInputs.csv',core+PROVENANCE+['InputClass','InputAccount','AccountSource'],non_topological)
    # Keep every comparison explicit for substantive review; do not call text differences contradictions.
    comparisons=[]
    for pair,rep,other,disposition in mirror_pairs:
        diff=[f for f in ['DependencyType','RequiredMaturity','ProposedMaturity','Statement','SatisfactionStatus'] if rep[f]!=other[f]]
        comparisons.append({'Consumer':pair[0],'Supplier':pair[1],'Representative':locator(rep),'Other':locator(other),'Disposition':disposition,'DifferentFields':';'.join(diff),**{f'Representative{f}':rep[f] for f in ['DependencyType','RequiredMaturity','ProposedMaturity','Statement','EvidenceQuote','SourceRef','SatisfactionStatus']},**{f'Other{f}':other[f] for f in ['DependencyType','RequiredMaturity','ProposedMaturity','Statement','EvidenceQuote','SourceRef','SatisfactionStatus']}})
    write(EVIDENCE/'MirrorComparisons.csv',list(comparisons[0]),comparisons)
    scc_account=[]
    for s,ns in scc_sets.items():
        internal=[x for x in active if x['TargetType']=='DELIVERABLE' and set(arc(x))<=ns]
        held=[x for x in candidates if x['SCCRef']==s]
        scc_account.append({'SCCRef':s,'CaseRef':'_DAG/cases/'+CASE_MAP[s],'Members':sorted(ns),'MemberCount':len(ns),'SourceRows':len(internal),'HeldArcs':len(held),'ExcludedIntraSCCRows':len(internal)-len(held),'CaseState':'EVIDENCE_ACCUMULATING; BASIS_CONFIRMED; UNRESOLVED','RetainedHistory':'_DAG/cases/SCC-CASE-004' if s=='SCC-002' else None})
    save(EVIDENCE/'SCC_Accounting.json',scc_account)
    dag=json.loads((EVIDENCE/'dag_audit.json').read_text())
    assert dag['node_row_count']==41 and dag['active_graph']['scc_count']==0
    assert dag['node_row_width_issue_count']==0 and dag['edge_row_width_issue_count']==0
    assert not any(arc(x)[0]==arc(x)[1] for x in admitted)
    assert len({arc(x) for x in admitted})==len(admitted)
    for path,h in protected.items():assert sha(ROOT/path)==h, f'Protected input changed: {path}'
    checks={'result':'PASS','manifest_entries':130,'manifest_matches_source_commit':True,'historical_presentation_members_verified_at_own_revision':79,'protected_input_count':len(protected),'protected_inputs_unchanged':True,'node_count':41,'node_bytes_unchanged':True,'packages':len({n['PackageID'] for n in nodes}),'total_source_rows':len(all_rows),'active_anchors':sum(x['DependencyClass']=='ANCHOR' and x['Status']=='ACTIVE' for x in all_rows),'retired_rows':sum(x['Status']=='RETIRED' for x in all_rows),'active_execution':403,'admissible_arcs':161,'admitted_rows':109,'candidate_rows':52,'excluded_rows':242,'dispositions':dict(Counter(x['Disposition'] for x in exclusions)),'candidate_reasons':dict(Counter(x['CandidateReason'] for x in candidates)),'target_types':dict(Counter(x['TargetType'] for x in active)),'maturity':dict(Counter(x['RequiredMaturity'] for x in active)),'satisfaction':dict(Counter(x['SatisfactionStatus'] for x in active)),'edge_core_fidelity_rows':fidelity,'supplemental_core_fidelity_rows':403,'core_fields_per_row':29,'missing_rows':0,'overlapping_rows':0,'source_duplicate_ids':0,'closure_scc_membership_exact':True,'case_mapping':CASE_MAP,'self_loops':0,'no_accepted_pointer':True,'strict_admitted_exit_code':0,'strict_subject_status':'PASS_ADMITTED_LAYER_ONLY','authority':'UNACCEPTED_VERSION; no lifecycle, satisfaction, readiness, 30% or product activation inferred'}
    save(EVIDENCE/'AssemblyChecks.json',checks)
    write(EVIDENCE/'RegisterAccounting.csv',['SourceRegister','DeliverableID','TotalRows','AnchorRows','RetiredRows','ActiveExecution','DependencyEdges.csv','CandidateEdges.csv','ExcludedRows.csv'],[{'SourceRegister':s,**{k:v.get(k,0) for k in ['DeliverableID','TotalRows','AnchorRows','RetiredRows','ActiveExecution','DependencyEdges.csv','CandidateEdges.csv','ExcludedRows.csv']}} for s,v in per_register.items()])
    context=[ROOT/'AGENTS.md',ROOT/'agents/AGENT_TASK.md',ROOT/'workflows/index.json',ROOT/'workflows/project-dag/WORKFLOW.md',ROOT/'workflows/project-dag/resources/contract.md',ROOT/'workflows/project-dag/resources/method.md',ROOT/'workflows/project-dag/resources/graph-version.md',EXECUTION/'_Coordination/AgentRuns/APP-V4-INITIAL-SETUP-20260927/ASSEMBLY_BRIEF.md']
    save(EVIDENCE/'Tool_Run.json',{'schema_version':1,'workflow':'chirality-root:bundled:workflow:project-dag','actor':'/root/renewal_research_strategy/dag_version_assembly','parent':'/root/renewal_research_strategy','role':'TASK','mechanism':'delegated-harness-native TASK child; no descendants','model':'Inherited Codex model; no model-family change requested or claimed','source_revision':SOURCE,'decision_applied_revision':DECISION_REV,'presented_revision':PRESENTED,'selected_context':[fingerprint(p) for p in context],'assembly_script':fingerprint(Path(__file__)),'python':sys.version,'python_executable':sys.executable,'runs':runs,'script_command':['python3',rel(Path(__file__))],'finished_at':datetime.now(timezone.utc).isoformat(),'process_subject_distinction':'Non-strict audit exits 0 with cyclic subject; strict admitted audit exits 0 and passes only its subject. Neither accepts graph or gate.','tool_limits':'No markdown-out used: report title/front matter are DEV-001-specific. dev001_projection JSON is preserved but not relied on. audit_dag source docstring still says aggregate authority/mirrors; governing D-GOV-49 method controls. Independent checks additionally cover node widths, self-loops, accounting and fidelity.','host_vs_brief':'Host permits wider workspace writes/tools. The brief narrows writes to named candidate files/Evidence/ASSEMBLY_RUN.md; no OS-level per-brief confinement is claimed. No Git mutation or delegation performed.'})
    print(json.dumps(checks,indent=2))

if __name__=='__main__': main()
