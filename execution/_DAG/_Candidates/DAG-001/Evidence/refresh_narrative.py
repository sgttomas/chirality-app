#!/usr/bin/env python3
"""Regenerate only authorized narrative/provenance after the header correction.

No graph audit or manifest-check command is rerun; prior evidence is preserved.
"""
import ast
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

C=Path(__file__).resolve().parent.parent
E=C/'Evidence'; R=C.parents[5]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def fp(p): return {'path':str(p.relative_to(R)),'sha256':sha(p)}
def save(p,x): p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
prior_manifest=json.loads((E/'ASSEMBLY_OUTPUT_MANIFEST.json').read_text())
prior_manifest_hash=sha(E/'ASSEMBLY_OUTPUT_MANIFEST.json')
generator=E/'describe_graph.py'
allowed=[C/'GRAPH_BASIS.md',C/'SOURCE_BASIS.json',C/'ASSEMBLY_RUN.md',generator]
unchanged=[]
for item in prior_manifest['files']:
    p=R/item['path']
    if p not in allowed:
        assert sha(p)==item['sha256'],str(p)
        unchanged.append(item)
before=[fp(C/n) for n in ['GRAPH_BASIS.md','SOURCE_BASIS.json','ASSEMBLY_RUN.md']]
tree=ast.parse(generator.read_text())
graph=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='graph' for t in n.targets))
old='**Basis confirmed; version assembled and checked; independent version review pending. No current graph-version acceptance or 30% passage.**'
new='**Basis confirmed; version assembled and audited. Independent version review is a separate required record; no graph-version acceptance or 30% passage is inferred.**'
assert (C/'GRAPH_BASIS.md').read_text().replace(old,new)==graph
(C/'GRAPH_BASIS.md').write_text(graph)
source=json.loads((C/'SOURCE_BASIS.json').read_text())
for item in source['graph_files']:
    if item['path']==str((C/'GRAPH_BASIS.md').relative_to(R)):item['sha256']=sha(C/'GRAPH_BASIS.md')
for item in source['tools']:
    if item['path']==str(generator.relative_to(R)):item['sha256']=sha(generator)
save(C/'SOURCE_BASIS.json',source)
timestamp=datetime.now(timezone.utc).isoformat()
with (C/'ASSEMBLY_RUN.md').open('a') as f:
    f.write('\n## Administrative narrative refresh\n\nAt '+timestamp+', the manager requested a timeless GRAPH_BASIS heading before independent review. The heading and describe_graph.py generation source now state that independent review is a separate required record. This bounded narrative refresh regenerated GRAPH_BASIS.md and its SOURCE_BASIS.json fingerprints, appended this run note and refreshed the output manifest. No graph audit or manifest-check command was rerun; all existing tool-run evidence, graph rows, nodes, exclusions and source/input accounts remain byte-identical. The actual refresh command, prior generator bytes and preservation checks are in Evidence/NarrativeRefresh_Run.json. No source, case, acceptance or gate effect changed.\n')
for item in unchanged: assert sha(R/item['path'])==item['sha256']
baseline=json.loads((E/'input_baseline.json').read_text())
for p,h in baseline['protected_inputs'].items(): assert sha(R/p)==h
save(E/'NarrativeRefresh_Run.json',{'recorded_at':timestamp,'arguments':['python3',str(Path(__file__).relative_to(R))],'cwd':str(R),'script':fp(Path(__file__)),'generator':fp(generator),'prior_generator_preserved':fp(E/'describe_graph_before_header_refresh.py'),'prior_output_manifest_sha256':prior_manifest_hash,'before_narrative':before,'after_narrative':[fp(C/n) for n in ['GRAPH_BASIS.md','SOURCE_BASIS.json','ASSEMBLY_RUN.md']],'unchanged_prior_outputs':unchanged,'protected_inputs_unchanged':len(baseline['protected_inputs']),'graph_auditor_invocations':0,'manifest_check_invocations':0,'run_status':'COMPLETE','subject_status':'PASS_ADMINISTRATIVE_WORDING_ONLY','reason':'Manager-directed timeless header before independent review; no new source or gate decision.'})
files=[C/n for n in ['GRAPH_BASIS.md','DeliverableNodes.csv','DependencyEdges.csv','CandidateEdges.csv','ExcludedRows.csv','SOURCE_BASIS.json','ASSEMBLY_RUN.md']]
files+=sorted(p for p in E.iterdir() if p.is_file() and p.name!='ASSEMBLY_OUTPUT_MANIFEST.json')
save(E/'ASSEMBLY_OUTPUT_MANIFEST.json',{'standing':'ASSEMBLED_UNACCEPTED_REVIEW_SUBJECT','files':[fp(p) for p in files],'self_excluded':'Evidence/ASSEMBLY_OUTPUT_MANIFEST.json','source_manifest_sha256':sha(C/'SOURCE_MANIFEST.sha256')})
print(json.dumps({'result':'PASS','output_count':len(files),'stable_manifest':fp(E/'ASSEMBLY_OUTPUT_MANIFEST.json'),'updated_docs':[fp(C/n) for n in ['GRAPH_BASIS.md','SOURCE_BASIS.json','ASSEMBLY_RUN.md']],'unchanged_prior_outputs':len(unchanged)},indent=2))
