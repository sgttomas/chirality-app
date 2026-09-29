import csv,json,sys
sys.path.insert(0,sys.argv[1])
import importlib.util
spec=importlib.util.spec_from_file_location('sr',sys.argv[1]+'/scc_recompute.py'); sr=importlib.util.module_from_spec(spec); spec.loader.exec_module(sr)
src='projects/chirality-app-v4/execution/_DAG/DAG-001/Evidence/admissible_edges.csv'
rows=list(csv.DictReader(open(src,newline=''))); cols=list(rows[0].keys())
kept={k:v for k,v in sr.C1.items() if k not in sr.DROP}; kept.update(sr.ADD)
tmpl=rows[0]
for i,(k,(a,b)) in enumerate(sorted(kept.items()),1):
    r=dict(tmpl); r.update({'DependencyID':f'DEP-{a[4:6]}-{a[7:9]}-9{i:02d}','FromDeliverableID':a,'FromPackageID':'PKG-'+a[4:6],'Direction':'UPSTREAM','TargetType':'DELIVERABLE','TargetDeliverableID':b,'TargetPackageID':'PKG-'+b[4:6],'Statement':'P2 scratch arc '+k,'Status':'ACTIVE','DependencyClass':'EXECUTION','SourceRecord':'0','SelectionRule':'P2-SCRATCH'})
    rows.append(r)
w=csv.DictWriter(open(sys.argv[1]+'/scratch_admissible_S2.csv','w',newline=''),fieldnames=cols); w.writeheader(); w.writerows(rows)
print(len(rows))
