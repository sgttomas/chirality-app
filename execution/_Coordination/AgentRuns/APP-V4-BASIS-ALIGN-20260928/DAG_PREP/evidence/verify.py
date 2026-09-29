import sys,re,os,glob,json; sys.path.insert(0,sys.argv[1])
from load import *
from proposals import P
R=regs()
dag=json.load(open(sys.argv[1]+'/dag001_arcs.json'))
A=set(map(tuple,dag['admitted'])); C=set(map(tuple,dag['candidate'])); ALL=A|C
KEY={'ACT':'ACT_AND_POLICY_CONTRACT.md','AS':'AUTONOMY_AND_STANDING_EXCHANGE.md','RS':'RECORD_SEMANTICS.md','WD':'WORKFLOW_DECLARATION.md','EXEC':'EXECUTION_COMPATIBILITY.md','C':'CATALOG_AND_READ_BASIS.md','P':'PROPOSAL_LIFECYCLE_AND_OUTCOMES.md','ADAPTER':'ADAPTER_ENABLEMENT_AND_RECEIVING.md','GUIDE':'HOST_INTEGRATION_GUIDE.md','HOSTING':'HOSTING_BOUNDARY.md','LOOP':'LOOP_RECEIVING_CONTRACT.md','PANEL':'PANEL_RECEIVING_CONTRACT.md','CA':'CONNECTED_ACTIVITY_CONTRACT.md','XT':'EXTERNAL_TRACE_CASES.md'}
def ddir(d): return os.path.dirname(R[d][0])
def quote(line):
    s=line.strip().lstrip('|').strip()
    s=re.sub(r'\s+',' ',s)
    w=s.split(' ')
    return ' '.join(w[:30])
out=[];bad=[]
rowsById={d:{r['DependencyID']:r for r in R[d][1]} for d in R}
for p in P:
    rec=dict(p)
    h=p['host']
    if p.get('ev'):
        k,pat=p['ev']
        f=os.path.join(ddir(h),'ScopeOfWork.md') if k=='SOW' else os.path.join(ddir(h),'Design',KEY[k])
        hit=None
        L=open(f).read().splitlines()
        for i,l in enumerate(L,1):
            if re.search(pat,l): hit=(i,' '.join(L[i-1:i-1+p.get('evn',1)])); break
        if not hit: bad.append((p['c1'],'NO EVIDENCE',pat)); rec['evfile']=None
        else:
            rec['evfile']=os.path.relpath(f,ddir(h)); rec['evline']=hit[0]; rec['quote']=quote(hit[1])
            # target mention check for deliverable rows
            t=p.get('tgt','')
            if t.startswith('DEL-') and p['kind'] in('MIRROR','NEWREP','NEWMIR'):
                rec['tgt_on_line']= (t in hit[1])
    t=p.get('tgt','')
    if p['kind'] in ('MIRROR','NEWREP','NEWMIR'):
        arc=(h,t) if p['dir']=='UPSTREAM' else (t,h)
        rec['arcpair']=arc
        rec['in_dag001']='admitted' if arc in A else ('candidate' if arc in C else None)
        if p['kind']=='MIRROR':
            cp=rowsById.get(t if p['host']!=t else h,{}).get(p['cp'])
            # counterpart lives in the other endpoint's register
            other = t
            cp=rowsById[other].get(p['cp'])
            if not cp: bad.append((p['c1'],'CP MISSING',p['cp']))
            else:
                ca=arc_of=( (cp['FromDeliverableID'],cp['TargetDeliverableID']) if cp['Direction']=='UPSTREAM' else (cp['TargetDeliverableID'],cp['FromDeliverableID']))
                rec['cp_ok']= cp['Status']=='ACTIVE' and ca==arc and cp['TargetDeliverableID']==h
                rec['cp_dir']=cp['Direction']
                if not rec['cp_ok']: bad.append((p['c1'],'CP MISMATCH',p['cp'],ca,arc))
            if rec['in_dag001'] is None: bad.append((p['c1'],'MIRROR BUT ARC ABSENT',arc))
        else:
            if rec['in_dag001']: bad.append((p['c1'],'NEW BUT ARC EXISTS',arc,rec['in_dag001']))
    if p['kind'] in('EDIT','PKG'):
        for rid in p['row'].split(';'):
            if rid not in rowsById[h]: bad.append((p['c1'],'EDIT ROW MISSING',rid))
    out.append(rec)
json.dump(out,open(sys.argv[1]+'/verified.json','w'),indent=1,default=list)
print('proposals',len(P)); print('problems',len(bad))
for b in bad: print(b)
for r in out:
    if r.get('tgt_on_line') is False: print('TARGET NOT ON EVIDENCE LINE',r['c1'],r['host'],r['tgt'],r.get('evline'),r.get('quote')[:120])
