import csv, glob, os, json, sys
ROOT='projects/chirality-app-v4/execution'
def regs():
    out={}
    for p in sorted(glob.glob(ROOT+'/PKG-*/1_Working/DEL-*/Dependencies.csv')):
        d=os.path.basename(os.path.dirname(p)).split('_')[0]
        with open(p,newline='') as f:
            rows=list(csv.DictReader(f))
        out[d]=(p,rows)
    return out
def arc(r):
    f=r['FromDeliverableID']; t=r['TargetDeliverableID']
    return (f,t) if r['Direction']=='UPSTREAM' else (t,f)
def topo(rows):
    return [r for r in rows if r['Status']=='ACTIVE' and r['DependencyClass']=='EXECUTION' and r['TargetType']=='DELIVERABLE' and r['TargetDeliverableID']]
