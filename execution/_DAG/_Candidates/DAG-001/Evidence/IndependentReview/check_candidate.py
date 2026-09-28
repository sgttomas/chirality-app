#!/usr/bin/env python3
"""Independent checks; writes only this review's own evidence directory."""
import csv
import hashlib
import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[8]
EX = ROOT / 'projects/chirality-app-v4/execution'
C = EX / '_DAG/_Candidates/DAG-001'
OUT = C / 'Evidence/IndependentReview'
failures = []
def check(ok, detail):
    if not ok:
        failures.append(detail)
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):
    with p.open(encoding='utf-8-sig', newline='') as f:
        r = csv.DictReader(f)
        result = list(r)
        check(all(None not in x and None not in x.values() for x in result), 'ragged CSV: '+str(p))
        return r.fieldnames, result
def key(r):
    return (r['SourceRegister'], r['DependencyID'], int(r['SourceRecord']))
def arc(r):
    a, b = r['FromDeliverableID'], r['TargetDeliverableID']
    return (a,b) if r['Direction']=='UPSTREAM' else (b,a)
def loc(r):
    return f"{r['SourceRegister']}#{r['DependencyID']}@{r['SourceRecord']}"
def gitbytes(rev, path):
    return subprocess.check_output(['git','show',f'{rev}:{path}'],cwd=ROOT)

basis=json.loads((C/'SOURCE_BASIS.json').read_text())
source_revision=basis['source_revision']
source_entries=[]
for line in (C/'SOURCE_MANIFEST.sha256').read_text().splitlines():
    digest, rel=line.split('  ',1)
    p=EX/rel
    check(sha(p)==digest, 'working source manifest mismatch: '+rel)
    check(hashlib.sha256(gitbytes(source_revision,p.relative_to(ROOT))).hexdigest()==digest, 'committed source mismatch: '+rel)
    source_entries.append((rel,digest))
assembly=json.loads((C/'Evidence/ASSEMBLY_OUTPUT_MANIFEST.json').read_text())
for x in assembly['files']:
    check(sha(ROOT/x['path'])==x['sha256'],'assembly manifest mismatch: '+x['path'])
historical=json.loads((C/'BASIS_MANIFEST.json').read_text())
for x in historical['files']:
    check(hashlib.sha256(gitbytes(basis['presentation']['revision'],x['path'])).hexdigest()==x['sha256'],'historical CP1 mismatch: '+x['path'])
check(hashlib.sha256(gitbytes(basis['decision_applied_revision'],basis['basis_decision']['path'])).hexdigest()==basis['basis_decision']['sha256'],'actual CP1 decision commit mismatch')
check(sha(ROOT/basis['basis_decision']['path'])==basis['basis_decision']['sha256'],'actual CP1 decision working mismatch')

_, inv=rows(ROOT/basis['inventory_source']['path'])
node_header,nodes=rows(C/'DeliverableNodes.csv')
expected_ids={r['DeliverableID'] for r in inv}
check(len(nodes)==len(expected_ids)==len(inv),'node inventory count or duplicate mismatch')
check({r['DeliverableID'] for r in nodes}==expected_ids,'node inventory identity mismatch')
byid={r['DeliverableID']:r for r in inv}
src={}; totals=Counter(); per_register={}; core=None
for n in nodes:
    i=byid[n['DeliverableID']]
    check(n['PackageID']==i['PackageID'] and n['DeliverableName']==i['Name'],'node identity fields mismatch '+n['DeliverableID'])
    check(n['RegisterState']=='PRESENT' and n['TrackingMode']=='FULL_GRAPH','node state mismatch '+n['DeliverableID'])
    check(n['InventorySource']==str((ROOT/basis['inventory_source']['path']).relative_to(EX)),'node source mismatch '+n['DeliverableID'])
    reg=EX/n['DependenciesPath']; directory=EX/n['ExecutionPath']
    check(reg==directory/'Dependencies.csv' and directory.is_dir(),'node path mismatch '+n['DeliverableID'])
    check(directory.name.startswith(n['DeliverableID']+'_') and directory.parent.parent.name.startswith(n['PackageID']+'_'),'node folder identity mismatch '+n['DeliverableID'])
    check('FULL_GRAPH' in (directory/'_DEPENDENCIES.md').read_text(),'local mode mismatch '+n['DeliverableID'])
    header,records=rows(reg)
    if core is None: core=header[:29]
    check(header[:29]==core,'core column order mismatch '+str(reg))
    cnt=Counter(TotalRows=len(records),AnchorRows=0,RetiredRows=0,ActiveExecution=0)
    ids=[]
    for idx,r in enumerate(records,1):
        ids.append(r['DependencyID'])
        if r['DependencyClass']=='ANCHOR' and r['Status']=='ACTIVE': cnt['AnchorRows']+=1
        if r['Status']=='RETIRED': cnt['RetiredRows']+=1
        if r['DependencyClass']=='EXECUTION' and r['Status']=='ACTIVE':
            cnt['ActiveExecution']+=1
            r.update(SourceRegister=n['DependenciesPath'],SourceRegisterSHA256=sha(reg),SourceRecord=str(idx))
            src[key(r)]=r
    check(len(ids)==len(set(ids)),'duplicate source ID '+n['DependenciesPath'])
    per_register[n['DependenciesPath']]=cnt
    totals.update(cnt)

layer={}; all_output=[]
for name in ['DependencyEdges.csv','CandidateEdges.csv','ExcludedRows.csv']:
    header,rr=rows(C/name);layer[name]=rr;all_output.extend(rr)
    if name!='ExcludedRows.csv': check(header[:29]==core,'graph core order '+name)
    for r in rr:
        k=key(r);check(k in src,'unknown graph source '+str(k))
        if k not in src: continue
        s=src[k]
        fields=core if name!='ExcludedRows.csv' else ['DependencyID','FromDeliverableID','Direction','DependencyType','TargetType','TargetDeliverableID','TargetRefID']
        for field in fields+['SourceRegisterSHA256']:
            check(r[field].encode('utf-8')==s[field].encode('utf-8'),'field fidelity '+str(k)+' '+field)
        per_register[r['SourceRegister']][name]+=1
        check(bool(r.get('SelectionRule') if name!='ExcludedRows.csv' else r.get('RuleOrRuling')),'missing selection rule '+str(k))
outputkeys=Counter(key(r) for r in all_output)
check(set(outputkeys)==set(src),'missing/extra execution accounting keys')
check(all(v==1 for v in outputkeys.values()),'overlapping output accounting keys')
_,existing_account=rows(C/'Evidence/RegisterAccounting.csv')
for r in existing_account:
    cnt=per_register[r['SourceRegister']]
    for k,v in cnt.items(): check(int(r[k])==v,'per-register count mismatch '+r['SourceRegister']+' '+k)
    check(cnt['ActiveExecution']==sum(cnt[n] for n in layer),'per-register balance '+r['SourceRegister'])
for name, expected in [('Evidence/all_execution_rows.csv',set(src)),('Evidence/NonTopologicalInputs.csv',{k for k,r in src.items() if r['TargetType']!='DELIVERABLE'})]:
    _,rr=rows(C/name)
    check(len(rr)==len(expected) and {key(r) for r in rr}==expected,'derived full row coverage '+name)
    for r in rr:
        for f in core+['SourceRegisterSHA256']:
            check(r[f]==src[key(r)][f],'derived row field fidelity '+name+' '+str(key(r))+' '+f)

groups=defaultdict(list);nontopo=[]
for r in src.values():
    check(r['Direction'] in {'UPSTREAM','DOWNSTREAM'},'noncanonical direction '+loc(r))
    if r['TargetType']!='DELIVERABLE': nontopo.append(r);continue
    check(r['FromDeliverableID'] in expected_ids and r['TargetDeliverableID'] in expected_ids,'outside inventory target '+loc(r))
    groups[arc(r)].append(r)
reps={};duplicates={}
for a,rr in groups.items():
    rr.sort(key=lambda r:(0 if r['Direction']=='UPSTREAM' and r['FromDeliverableID']==a[0] else 1,0 if r['Origin']=='DECLARED' else 1,r['DependencyID']))
    reps[a]=rr[0]
    for r in rr[1:]: duplicates[key(r)]=rr[0]

# Independent reachability partition, not the assembler's SCC implementation.
adj={n:set() for n in expected_ids}
for a,b in reps: adj[a].add(b)
reach={}
for n in expected_ids:
    seen={n};todo=[n]
    while todo:
        for v in adj[todo.pop()]:
            if v not in seen: seen.add(v);todo.append(v)
    reach[n]=seen
components={frozenset(v for v in expected_ids if v in reach[n] and n in reach[v]) for n in expected_ids}
cycles=sorted((sorted(s) for s in components if len(s)>1),key=lambda s:s[0])
membership={n:tuple(s) for s in cycles for n in s}
held={key(r) for a,r in reps.items() if a[0]==a[1] or a[0] in membership and membership[a[0]]==membership.get(a[1])}
admitted={key(r) for r in reps.values()}-held
check({key(r) for r in layer['DependencyEdges.csv']}==admitted,'SR-1..7 admitted selection mismatch')
check({key(r) for r in layer['CandidateEdges.csv']}==held,'SR-1..7 candidate selection mismatch')
for r in layer['ExcludedRows.csv']:
    k=key(r)
    if src[k]['TargetType']!='DELIVERABLE':
        check(r['Disposition']=='NOT_TOPOLOGICAL' and r['RuleOrRuling']=='SR-2' and not r['RepresentedBy'],'SR-2 exclusion mismatch '+str(k))
    else:
        check(k in duplicates,'SR-6 unexpected exclusion '+str(k))
        rep=duplicates[k]
        check(r['RepresentedBy']==loc(rep),'SR-6 representative mismatch '+str(k))
        expected='SAME_ARC' if r['SourceRegister']==rep['SourceRegister'] else 'MIRROR'
        check(r['Disposition']==expected and r['RuleOrRuling']=='SR-6','SR-6 disposition mismatch '+str(k))
closure=EX/'_Evaluation/DepClosure/CLOSURE_APP_V4_TARGETS_2026-09-27_2237'
_,closure_scc=rows(closure/'Evidence/scc_summary.csv')
check(cycles==[r['Nodes'].split(';') for r in closure_scc],'closure SCC membership mismatch')
sccbyid={r['SCC_ID']:r['Nodes'].split(';') for r in closure_scc}
casemap={'SCC-001':'SCC-CASE-001','SCC-002':'SCC-CASE-002','SCC-003':'SCC-CASE-003','SCC-004':'SCC-CASE-005','SCC-005':'SCC-CASE-006','SCC-006':'SCC-CASE-007'}
for r in layer['CandidateEdges.csv']:
    check(r['CandidateReason']=='SCC_UNRESOLVED' and bool(r['OpenQuestion']),'candidate reason/question mismatch '+loc(r))
    check(set(arc(r))<=set(sccbyid[r['SCCRef']]),'candidate SCC mismatch '+loc(r))
    check(r['CaseRef']=='_DAG/cases/'+casemap[r['SCCRef']] and (EX/r['CaseRef']/'Case_Datasheet.md').is_file(),'candidate case mismatch '+loc(r))
account=json.loads((C/'Evidence/SCC_Accounting.json').read_text())
for x in account:
    members=set(x['Members'])
    relevant=[r for r in src.values() if r['TargetType']=='DELIVERABLE' and set(arc(r))<=members]
    arcs=[a for a in reps if set(a)<=members]
    check(x['Members']==sccbyid[x['SCCRef']] and x['HeldArcs']==len(arcs) and x['SourceRows']==len(relevant) and x['ExcludedIntraSCCRows']==len(relevant)-len(arcs),'SCC accounting mismatch '+x['SCCRef'])

_,comparisons=rows(C/'Evidence/MirrorComparisons.csv')
check(len(comparisons)==len(duplicates),'mirror comparison count')
byloc={loc(r):r for r in src.values()};compkeys=set()
for x in comparisons:
    r=byloc[x['Other']];rep=byloc[x['Representative']];compkeys.add(key(r))
    check(key(r) in duplicates and key(rep)==key(duplicates[key(r)]),'mirror pairing mismatch '+x['Other'])
    for prefix,source in [('Representative',rep),('Other',r)]:
        for f in ['DependencyType','RequiredMaturity','ProposedMaturity','Statement','EvidenceQuote','SourceRef','SatisfactionStatus']:
            check(x[prefix+f]==source[f],'mirror field mismatch '+x['Other']+' '+prefix+f)
check(compkeys==set(duplicates),'mirror source coverage')
touched={v for a,r in reps.items() if key(r) in admitted for v in a}
degrees={n:sum(n in a for a in reps) for n in expected_ids}
statuses=[]
for n in nodes:
    text=(EX/n['ExecutionPath']/'_STATUS.md').read_text()
    import re
    match=re.search(r'^\*\*Current State:\*\*\s*(\S+)',text,re.M)
    statuses.append(match.group(1) if match else 'UNPARSED')
check(Counter(statuses)==Counter(INITIALIZED=len(nodes)), 'current lifecycle census does not match INITIALIZED definition account')

result={
    'subject_status':'PASS' if not failures else 'FAIL', 'failures':failures,
    'assembly_manifest_members':len(assembly['files']), 'source_manifest_members':len(source_entries),'historical_presentation_members':len(historical['files']),
    'source_revision':source_revision,'reviewed_current_revision':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
    'nodes':len(nodes),'packages':len({n['PackageID'] for n in nodes}),'source_counts':dict(totals),
    'layers':{n:len(rr) for n,rr in layer.items()},'topological_source_rows':sum(map(len,groups.values())),'representative_arcs':len(reps),
    'exclusions':dict(Counter(r['Disposition'] for r in layer['ExcludedRows.csv'])),
    'non_topological_targets':dict(Counter(r['TargetType'] for r in nontopo)),
    'satisfaction':dict(Counter(r['SatisfactionStatus'] for r in src.values())),
    'required_maturity':dict(Counter(r['RequiredMaturity'] for r in src.values())),
    'source_core_field_count':len(core),'representative_core_comparisons':len(reps)*len(core),
    'sccs':cycles,'self_loops':[a for a in reps if a[0]==a[1]],'admitted_isolated_nodes':sorted(expected_ids-touched),
    'raw_hubs':{n:d for n,d in degrees.items() if d>=20},
    'mirror_differences':{f:sum(src[k][f]!=rep[f] for k,rep in duplicates.items()) for f in ['Statement','DependencyType','RequiredMaturity','ProposedMaturity','SatisfactionStatus']},
    'status_counts':dict(Counter(statuses)),
    'accepted_pointer_exists':(EX/'_DAG/_LATEST.md').exists(),
    'per_register':{k:dict(v) for k,v in per_register.items()}
}
(OUT/'IndependentChecks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='per_register'},indent=2))
raise SystemExit(bool(failures))
