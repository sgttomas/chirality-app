#!/usr/bin/env python3
"""Currency audit scratch re-application of DAG-001's accepted selection rules.

project-dag currency.md step 4. Reads the live local registers named by
DAG-001's SOURCE_MANIFEST.sha256, re-applies the confirmed SR-1..SR-7 exactly as
DAG-001 applied them, and compares the resulting admitted arcs, candidate arcs,
SCCs and inventory with the accepted DAG-001 files. Writes only into this
Evidence/ folder. It is a scratch assembly, not a graph version; it edits no
accepted version, local file or case.

Run from the repository root:
  python3 projects/chirality-app-v4/execution/_Evaluation/DAGCurrency/<snapshot>/Evidence/reapply_selection.py
"""
from __future__ import annotations
import ast, csv, hashlib, json, re, subprocess, sys
from collections import Counter, defaultdict
from pathlib import Path

EVIDENCE = Path(__file__).resolve().parent
EXECUTION = EVIDENCE.parents[3]
ROOT = EXECUTION.parents[2]
DAG1 = EXECUTION / '_DAG/DAG-001'
TOOL = ROOT / 'tools/coordination/audit_dag.py'
P2 = EXECUTION / '_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/DAG_PREP/ARC_ANALYSIS.md'
PROVENANCE = ['SourceRegister', 'SourceRegisterSHA256', 'SourceRecord', 'SelectionRule']


def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rel(p): return str(Path(p).resolve().relative_to(ROOT))


def read(p):
    with Path(p).open(encoding='utf-8-sig', newline='') as f:
        r = csv.DictReader(f); rows = list(r)
    assert all(None not in x and None not in x.values() for x in rows), f'ragged {p}'
    return r.fieldnames, rows


def write(p, cols, rows):
    with Path(p).open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore', lineterminator='\n')
        w.writeheader(); w.writerows(rows)


def arc(r):
    a = (r['FromDeliverableID'], r['TargetDeliverableID'])
    return a if r['Direction'] == 'UPSTREAM' else a[::-1]


def rank(r): return (r['Direction'] != 'UPSTREAM', r['Origin'] != 'DECLARED', r['DependencyID'])


def main():
    tree = ast.parse(TOOL.read_text())
    core = [ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
            and isinstance(n.targets[0], ast.Name) and n.targets[0].id == 'REQUIRED_COLUMNS'][0]
    assert len(core) == 29
    _, nodes = read(DAG1 / 'DeliverableNodes.csv')
    ids = {n['DeliverableID'] for n in nodes}
    # Inventory: the accepted decomposition pointer and register are unchanged.
    inv = '_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv'
    manifest = {l.split('  ', 1)[1]: l.split('  ', 1)[0] for l in (DAG1 / 'SOURCE_MANIFEST.sha256').read_text().splitlines()}
    inventory_unchanged = (sha(EXECUTION / inv) == manifest[inv]
                           and sha(EXECUTION / '_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md') == manifest['_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md'])
    _, invrows = read(EXECUTION / inv)
    assert {x['DeliverableID'] for x in invrows} == ids and len(ids) == 41

    active = []; groups = defaultdict(list); nontopo = 0
    for n in nodes:
        src = n['DependenciesPath']; p = EXECUTION / src; _, rows = read(p)
        for i, r in enumerate(rows, 1):
            if r['Status'] != 'ACTIVE' or r['DependencyClass'] != 'EXECUTION':
                continue
            out = {k: r[k] for k in core}
            out.update(SourceRegister=src, SourceRegisterSHA256=sha(p), SourceRecord=str(i), SelectionRule='')
            active.append(out)
            if r['TargetType'] != 'DELIVERABLE':
                nontopo += 1; continue
            assert r['TargetDeliverableID'] in ids
            groups[arc(out)].append(out)
    admissible = []; rep_of = {}
    for pair, rows in sorted(groups.items()):
        rep = sorted(rows, key=rank)[0]
        rep['SelectionRule'] = 'SR-1;SR-2;SR-3;SR-4;SR-5(not applied);SR-6'
        admissible.append(rep); rep_of[pair] = rep
    write(EVIDENCE / 'scratch_admissible_edges.csv', core + PROVENANCE, admissible)
    argv = ['python3', rel(TOOL), '--edges', rel(EVIDENCE / 'scratch_admissible_edges.csv'),
            '--nodes', rel(DAG1 / 'DeliverableNodes.csv'), '--canonical',
            '--json-out', rel(EVIDENCE / 'scratch_admissible_audit.json')]
    p = subprocess.run(argv, cwd=ROOT, text=True, capture_output=True)
    (EVIDENCE / 'scratch_admissible_audit.stdout.txt').write_text(p.stdout)
    (EVIDENCE / 'scratch_admissible_audit.stderr.txt').write_text(p.stderr)
    assert p.returncode == 0, p.stdout + p.stderr
    audit = json.loads((EVIDENCE / 'scratch_admissible_audit.json').read_text())
    sccs = sorted([sorted(s) for s in audit['active_graph']['sccs']], key=lambda s: (-len(s), s))
    member = {m: i for i, s in enumerate(sccs) for m in s}
    admitted = {a for a in rep_of if not (a[0] in member and member[a[0]] == member.get(a[1]))}
    candidate = set(rep_of) - admitted

    _, e1 = read(DAG1 / 'DependencyEdges.csv'); _, c1 = read(DAG1 / 'CandidateEdges.csv')
    a1 = {arc(r): r for r in e1}; k1 = {arc(r): r for r in c1}
    scc1 = json.loads((DAG1 / 'Evidence/SCC_Accounting.json').read_text())
    sccs1 = {frozenset(x['Members']) for x in scc1}
    old = set(a1) | set(k1); new = set(rep_of)
    added = sorted(new - old); removed = sorted(old - new)
    layer_changes = sorted(a for a in old & new if (a in a1) != (a in admitted))
    rep_changes = []
    for a in sorted(old & new):
        r_old = a1.get(a) or k1.get(a); r_new = rep_of[a]
        if (r_old['SourceRegister'], r_old['DependencyID']) != (r_new['SourceRegister'], r_new['DependencyID']):
            rep_changes.append({'arc': f'{a[0]} -> {a[1]}', 'dag001_representative': f"{r_old['SourceRegister']}#{r_old['DependencyID']}",
                                'current_representative': f"{r_new['SourceRegister']}#{r_new['DependencyID']}",
                                'layer': 'admitted' if a in admitted else 'candidate'})
    # P2 labels (read-only) for the added arcs.
    labels = {}
    for line in P2.read_text().splitlines():
        # Only the ARC_ANALYSIS §2.2 arc table (N-*, R8-*, X-1); E-*/K-* are the kept-out guards.
        m = re.match(r'\|\s*((?:N|R8|X)-[A-Z0-9]+)\s*\|\s*(DEL-\d\d-\d\d)\s*→\s*(DEL-\d\d-\d\d)\s*\|', line)
        if m: labels.setdefault((m.group(2), m.group(3)), m.group(1))
    added_rows = []
    for a in added:
        r = rep_of[a]
        added_rows.append({'Consumer': a[0], 'Supplier': a[1], 'P2Label': labels.get(a, 'UNLABELLED'),
                           'Layer': 'admitted' if a in admitted else 'candidate',
                           'SCC': ('SCC with ' + ';'.join(sccs[member[a[0]]])) if a in candidate else '',
                           'Representative': f"{r['SourceRegister']}#{r['DependencyID']}",
                           'Direction': r['Direction'], 'DependencyType': r['DependencyType']})
    write(EVIDENCE / 'added_arcs.csv', list(added_rows[0]) if added_rows else ['Consumer'], added_rows)
    accepted41 = {k for k, v in labels.items() if v not in ('N-12', 'N-B8')}
    assert len(accepted41) == 41, len(accepted41)
    guards_present = []
    for line in P2.read_text().splitlines():
        m = re.match(r'\|\s*((?:E|K)-\d+)\s*\|\s*(DEL-\d\d-\d\d)\s*→\s*(DEL-\d\d-\d\d)\s*\|', line)
        if m and (m.group(2), m.group(3)) in new: guards_present.append(m.group(1))
    pending = sorted({x for a in added + removed for x in a})
    result = {
        'classification': 'DEPARTURE' if (added or removed or {frozenset(s) for s in sccs} != sccs1 or not inventory_unchanged) else 'CURRENT_WITH_EVIDENCE_DRIFT',
        'inventory_unchanged': inventory_unchanged,
        'active_execution_rows': len(active), 'non_topological_rows': nontopo,
        'deliverable_target_rows': sum(len(v) for v in groups.values()),
        'arcs': {'dag001_admitted': len(a1), 'dag001_candidate': len(k1), 'dag001_total': len(old),
                 'current_admitted': len(admitted), 'current_candidate': len(candidate), 'current_total': len(new),
                 'added': len(added), 'removed': len(removed),
                 'added_admitted': sum(a in admitted for a in added), 'added_candidate': sum(a in candidate for a in added),
                 'existing_arcs_changing_layer': [f'{a[0]} -> {a[1]}' for a in layer_changes]},
        'sccs_current': sccs, 'sccs_unchanged': {frozenset(s) for s in sccs} == sccs1,
        'representative_changes': rep_changes,
        'p2_accepted_arc_set_size': len(accepted41),
        'p2_accepted_arcs_not_produced': sorted(f'{labels[a]} {a[0]} -> {a[1]}' for a in accepted41 - new),
        'arcs_added_outside_p2_set': [f'{a[0]} -> {a[1]}' for a in added if a not in accepted41],
        'withheld_arcs_absent': {lab: (a not in new) for a, lab in labels.items() if lab in ('N-12', 'N-B8')},
        'kept_out_guard_arcs_present': guards_present,
        'dag_pending': pending,
        'scratch_audit': {'tool': rel(TOOL), 'sha256': sha(TOOL), 'argv': argv, 'exit_code': p.returncode,
                          'edge_count': audit['active_graph']['edge_count'], 'scc_count': audit['active_graph']['scc_count'],
                          'canonical_finding_count': audit['canonical_finding_count']},
        'script': {'path': rel(Path(__file__)), 'sha256': sha(Path(__file__))},
    }
    (EVIDENCE / 'reapplication_result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('representative_changes',)}, indent=2))


if __name__ == '__main__':
    main()
