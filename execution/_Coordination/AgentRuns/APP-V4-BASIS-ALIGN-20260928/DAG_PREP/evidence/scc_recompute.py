#!/usr/bin/env python3
"""SCC recomputation for APP-V4-BASIS-ALIGN-20260928 node P2 (preparation only).
Reads the DAG-001 admissible arc set from the live registers (verified equal to
DAG-001 DependencyEdges+CandidateEdges), adds arc sets, and reports SCC membership.
Writes nothing outside the output path given as argv[2]."""
import csv, glob, os, sys, json
ROOT = 'projects/chirality-app-v4/execution'
def arcs_from_registers():
    out = set()
    for p in glob.glob(ROOT + '/PKG-*/1_Working/DEL-*/Dependencies.csv'):
        for r in csv.DictReader(open(p, newline='')):
            if r['Status'] == 'ACTIVE' and r['DependencyClass'] == 'EXECUTION' and r['TargetType'] == 'DELIVERABLE' and r['TargetDeliverableID']:
                f, t = r['FromDeliverableID'], r['TargetDeliverableID']
                out.add((f, t) if r['Direction'] == 'UPSTREAM' else (t, f))
    return out
def dag001_arcs():
    s = set()
    for fn in ('DependencyEdges.csv', 'CandidateEdges.csv'):
        for r in csv.DictReader(open(ROOT + '/_DAG/DAG-001/' + fn, newline='')):
            f, t = r['FromDeliverableID'], r['TargetDeliverableID']
            s.add((f, t) if r['Direction'] == 'UPSTREAM' else (t, f))
    return s
def nodes():
    return [r['DeliverableID'] for r in csv.DictReader(open(ROOT + '/_DAG/DAG-001/DeliverableNodes.csv'))]
def tarjan(V, E):
    adj = {v: [] for v in V}
    for a, b in E: adj[a].append(b)
    idx, low, st, on, res, c = {}, {}, [], set(), [], [0]
    sys.setrecursionlimit(10000)
    def sc(v):
        idx[v] = low[v] = c[0]; c[0] += 1; st.append(v); on.add(v)
        for w in adj[v]:
            if w not in idx: sc(w); low[v] = min(low[v], low[w])
            elif w in on: low[v] = min(low[v], idx[w])
        if low[v] == idx[v]:
            comp = []
            while True:
                w = st.pop(); on.discard(w); comp.append(w)
                if w == v: break
            res.append(sorted(comp))
    for v in V:
        if v not in idx: sc(v)
    return sorted([c for c in res if len(c) > 1])
C1 = {  # consumer -> supplier, the 40 distinct C1 arcs
 'N-01':('DEL-04-02','DEL-03-01'),'N-02':('DEL-04-02','DEL-02-03'),'N-03':('DEL-05-01','DEL-04-02'),'N-04':('DEL-05-02','DEL-04-02'),
 'N-05':('DEL-03-02','DEL-04-02'),'N-06':('DEL-03-03','DEL-04-02'),'N-07':('DEL-02-03','DEL-04-02'),'N-08':('DEL-09-06','DEL-04-02'),
 'N-09':('DEL-09-09','DEL-04-02'),'N-10':('DEL-04-03','DEL-03-01'),'N-11':('DEL-03-01','DEL-04-03'),'N-12':('DEL-03-02','DEL-04-03'),
 'N-13':('DEL-04-03','DEL-02-03'),'N-14':('DEL-04-03','DEL-03-03'),'N-15':('DEL-04-03','DEL-01-01'),'N-16':('DEL-02-01','DEL-01-01'),
 'N-17':('DEL-02-01','DEL-02-03'),'N-18':('DEL-02-01','DEL-03-02'),'N-19':('DEL-09-06','DEL-02-01'),'N-20':('DEL-03-03','DEL-02-01'),
 'N-21':('DEL-02-03','DEL-03-02'),'N-22':('DEL-02-03','DEL-05-01'),'N-23':('DEL-02-03','DEL-01-01'),'N-24':('DEL-02-03','DEL-03-03'),
 'N-25':('DEL-05-02','DEL-02-03'),'N-26':('DEL-09-09','DEL-02-03'),'N-27':('DEL-03-03','DEL-02-03'),'N-28':('DEL-09-06','DEL-04-01'),
 'N-B3':('DEL-03-02','DEL-02-01'),'N-B4':('DEL-03-03','DEL-01-01'),'N-B8':('DEL-03-03','DEL-04-03'),'N-B9':('DEL-03-04','DEL-01-01'),
 'N-B10':('DEL-03-04','DEL-09-06'),'N-B11':('DEL-03-04','DEL-09-09'),
 'N-C1':('DEL-09-06','DEL-02-02'),'N-C2':('DEL-09-06','DEL-03-01'),'N-C3':('DEL-09-06','DEL-03-02'),'N-C4':('DEL-09-06','DEL-03-03'),
 'N-C5':('DEL-09-06','DEL-01-01'),'N-C6':('DEL-09-09','DEL-05-01')}
DROP = ['N-12', 'N-B8']
ADD = {'R8-A':('DEL-04-02','DEL-05-01'), 'R8-B':('DEL-04-03','DEL-05-01'), 'X-1':('DEL-02-03','DEL-01-04')}
EXCLUDED5 = {'E-1':('DEL-09-09','DEL-09-06'),'E-2':('DEL-09-09','DEL-03-04'),'E-3':('DEL-04-01','DEL-03-01'),'E-4':('DEL-04-01','DEL-03-03'),'E-5':('DEL-09-06','DEL-03-04')}
CONSIDERED = {'K-1':('DEL-04-01','DEL-05-01'),'K-2':('DEL-04-01','DEL-02-01'),'K-3':('DEL-01-01','DEL-03-03'),'K-4':('DEL-01-01','DEL-04-03'),
 'K-5':('DEL-01-01','DEL-05-01'),'K-6':('DEL-09-06','DEL-09-09'),'K-7':('DEL-09-06','DEL-09-07'),'K-8':('DEL-04-03','DEL-02-01'),
 'K-9':('DEL-02-01','DEL-03-03'),'K-10':('DEL-04-02','DEL-05-02'),'K-11':('DEL-03-03','DEL-09-06'),'K-12':('DEL-01-01','DEL-04-01')}
def main():
    V = nodes(); S0 = arcs_from_registers(); D = dag001_arcs()
    rep = {'nodes': len(V), 'S0_arcs': len(S0), 'S0_equals_DAG001': S0 == D}
    base = tarjan(V, S0); rep['S0_sccs'] = base
    assert all(a not in S0 for a in C1.values()), 'a C1 arc already exists'
    S1 = S0 | set(C1.values()); rep['S1_arcs'] = len(S1); rep['S1_sccs'] = tarjan(V, S1)
    kept = {k: v for k, v in C1.items() if k not in DROP}; kept.update(ADD)
    assert all(a not in S0 for a in kept.values())
    S2 = S0 | set(kept.values()); rep['S2_arcs'] = len(S2); s2 = tarjan(V, S2); rep['S2_sccs'] = s2
    rep['S1_membership_changed'] = rep['S1_sccs'] != base
    rep['S2_membership_changed'] = s2 != base
    comp = {v: i for i, c in enumerate(s2) for v in c}
    def layer(a): return 'candidate' if a[0] in comp and comp.get(a[0]) == comp.get(a[1]) else 'admitted'
    rep['S2_layers'] = {k: [v[0], v[1], layer(v)] for k, v in sorted(kept.items())}
    rep['S2_existing_layer_changes'] = [a for a in S0 if (layer(a) == 'candidate') != (a[0] in {x for c in base for x in c} and any(a[0] in c and a[1] in c for c in base))]
    def effect(E, extra):
        s = tarjan(V, E | {extra})
        return 'no membership change' if s == tarjan(V, E) else {'sccs_after': s}
    rep['excluded5_on_S2'] = {k: [v, effect(S2, v)] for k, v in EXCLUDED5.items()}
    rep['excluded5_on_S1'] = {k: [v, effect(S1, v)] for k, v in EXCLUDED5.items()}
    rep['considered_on_S2'] = {k: [v, effect(S2, v), v in S0] for k, v in CONSIDERED.items()}
    rep['dropped_on_S2'] = {k: [C1[k], effect(S2, C1[k])] for k in DROP}
    UNGROUNDED = ['N-11','N-17','N-20','N-22','N-27','N-B3','N-B4','R8-A','R8-B']
    S2g = S0 | {v for k, v in kept.items() if k not in UNGROUNDED}
    s2g = tarjan(V, S2g)
    rep['S2g_arcs'] = len(S2g); rep['S2g_sccs'] = s2g; rep['S2g_membership_changed'] = s2g != base
    rep['S2g_admitted_arcs'] = sum(1 for a in S2g if layer(a) == 'admitted'); rep['S2g_candidate_arcs'] = sum(1 for a in S2g if layer(a) == 'candidate')
    # per-SCC admitted/candidate counts
    rep['S2_candidate_arcs'] = sum(1 for a in S2 if layer(a) == 'candidate')
    rep['S2_admitted_arcs'] = sum(1 for a in S2 if layer(a) == 'admitted')
    # acyclicity of the admitted layer
    adm = {a for a in S2 if layer(a) == 'admitted'}
    rep['S2_admitted_layer_sccs'] = tarjan(V, adm)
    json.dump(rep, open(sys.argv[1], 'w'), indent=1, default=list)
    print(json.dumps({k: rep[k] for k in ['nodes','S0_arcs','S0_equals_DAG001','S1_arcs','S2_arcs','S1_membership_changed','S2_membership_changed','S2_admitted_arcs','S2_candidate_arcs','S2_admitted_layer_sccs','S2_existing_layer_changes','S2g_arcs','S2g_membership_changed','S2g_admitted_arcs','S2g_candidate_arcs']}, default=list))
if __name__ == '__main__':
    main()
