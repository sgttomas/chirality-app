import sys,json
S=sys.argv[1]; sys.path.insert(0,S)
from load import regs
R=regs(); recs=json.load(open(S+'/out/p2_records.json'))
ORDER=['DEL-04-01','DEL-04-02','DEL-04-03','DEL-02-01','DEL-02-03','DEL-03-01','DEL-03-02','DEL-03-03','DEL-03-04','DEL-01-01','DEL-05-01','DEL-05-02','DEL-09-06','DEL-09-09']
out=[]
for d in ORDER:
    rows=R[d][1]; act=[r for r in rows if r['Status']=='ACTIVE']
    anc=sum(1 for r in act if r['DependencyClass']=='ANCHOR'); exe=len(act)-anc
    add=[r for r in recs if r['host']==d and r.get('csvrow')]
    g=[r for r in add if r['route']=='EXTRACT']; s=[r for r in add if r['route']=='EXTRACT*']
    ed=[r for r in recs if r['host']==d and r['kind'] in('EDIT','PKG') and r['disp'] in('AMEND','KEEP')]
    out.append(f'#### {d}\n')
    out.append(f'- **Human-owned sections** (Mode, Declared Upstream, Declared Downstream): unchanged by the extraction route.' + (f' Fallback if P1 adds no SoW sentence and the owner declares instead ({len(s)} entr{"y" if len(s)==1 else "ies"}):' if s else ''))
    for r in s:
        x=r['csvrow']; t=x['TargetDeliverableID'] or x['TargetRefID']
        sec='Declared Upstream (I need these before I can proceed)' if x['Direction']=='UPSTREAM' else 'Declared Downstream (These need me)'
        if x['TargetType']=='DELIVERABLE':
            out.append(f'  - under `## {sec}`: `- {t} {x["TargetName"]} — Reason: {x["Statement"]}` / `  - Required maturity: INITIALIZED` / `  - Location: {x["TargetLocation"]}`. Mirrored by dependency-extract as an `Origin=DECLARED` row typed `{"PREREQUISITE" if x["Direction"]=="UPSTREAM" else "ENABLES"}` from the heading. If the owner wants `{x["DependencyType"]}` kept, record a direct `Origin=DECLARED` CSV row instead.')
        else:
            out.append(f'  - `{t}` is not a deliverable. Record it as a direct `Origin=DECLARED` CSV row (`{x["Direction"]} {x["DependencyType"]}`), because the §5.2 entry form takes deliverable IDs.')
    out.append(f'- **Extracted Dependency Register** after application: ACTIVE {len(act)} → {len(act)+len(g)} with grounded rows only, or {len(act)+len(g)+len(s)} with the P1-dependent rows too; ANCHOR {anc} unchanged; EXECUTION {exe} → {exe+len(g)} / {exe+len(g)+len(s)}; RETIRED 0 unless a SoW revision removes a stated relationship.')
    if add:
        out.append('- Append to the EXECUTION summary table:')
        for r in add:
            x=r['csvrow']; out.append(f'  - `| {x["DependencyID"]} | EXECUTION | {x["Direction"]} | {x["TargetDeliverableID"] or x["TargetRefID"]} | {x["DependencyType"]} |`' + (' (P1-dependent)' if r['route']=='EXTRACT*' else ''))
    if ed:
        out.append('- Refreshed in place (same DependencyID; Statement/Notes only; SatisfactionStatus unchanged): ' + ', '.join(sorted({x for r in ed for x in r['row'].split(';')})) + '.')
    drops=[r for r in recs if r['host']==d and r['disp'] in('DROP','DEFER') and r['kind'] in ('MIRROR','NEWREP','NEWMIR')]
    rn=[f'SOURCE_DOCS=ScopeOfWork.md (as revised by scope-of-work REVISE under the accepted amendment); MODE=UPDATE; STRICTNESS=CONSERVATIVE',
        'record the grounding C1 SoW correction ID for each new row, and the Design corroboration line, in Notes']
    if d=='DEL-04-03': rn.append('record that no DOWNSTREAM row to DEL-03-02 is written: the disputed arc N-12 is withheld per the K1 ruling, and the RS §10 "DEL-03-02 consumes §5 evidence rules" cell goes to the owner as a wording finding')
    if d=='DEL-03-03': rn.append('record that no UPSTREAM row to DEL-04-03 (N-B8) is written: it is withheld per the K1 ruling, because RS is read "for joins only" as the destination of the adapter\'s evidence, and N-14 carries the relationship')
    if d=='DEL-04-01': rn.append('do not take the ACT §5.1 runtime resolution inputs, or the ACT §2.7 citation of LOOP §5.1.1, as production inputs: each would pull DEL-04-01 into SCC-002 (ARC_ANALYSIS §4)')
    if drops: rn.append('record the deferred optional mirrors (' + ', '.join(r['c1'] for r in drops) + ') as "not extracted: no SoW ground; consumer row represents the arc"')
    out.append('- **Run Notes / Run History** (agent-owned): append one run entry. ' + '; '.join(rn) + '.')
    out.append('')
open(S+'/out/depmd.md','w').write('\n'.join(out)); print(len(out))
