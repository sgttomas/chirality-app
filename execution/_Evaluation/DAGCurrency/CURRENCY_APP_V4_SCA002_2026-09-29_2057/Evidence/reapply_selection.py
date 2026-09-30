#!/usr/bin/env python3
"""Currency audit scratch re-application of DAG-002's accepted selection rules.

project-dag currency.md step 4. Reads the live local registers named by
DAG-002's SOURCE_MANIFEST.sha256, re-applies the confirmed SR-1..SR-7 exactly as
DAG-002 applied them (carried unchanged from DAG-001), and compares the resulting
admitted arcs, candidate arcs, SCCs and inventory with the accepted DAG-002 files.
Writes only into this Evidence/ folder. It is a scratch assembly, not a graph
version; it edits no accepted version, local file or case.

Adapted from CURRENCY_APP_V4_BASISALIGN_2026-09-29_0856/Evidence/reapply_selection.py
(sha256 dcb6cf7f8942f0df1bb18bf7321cd670e04dd87fa013dcd8e07d5c65ea6caed5).

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
DAG2 = EXECUTION / '_DAG/DAG-002'
TOOL = ROOT / 'tools/coordination/audit_dag.py'
P2 = EXECUTION / '_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/DAG_PREP/ARC_ANALYSIS.md'
# The arcs SCA-V4-002 was accepted to add (OWNER_ITEMS Q-4; DECISION-2; ARC_EFFECT §1).
EXPECTED = {('DEL-02-01', 'DEL-03-02'): 'N-18', ('DEL-02-03', 'DEL-03-02'): 'N-21',
            ('DEL-02-03', 'DEL-03-03'): 'N-24', ('DEL-02-03', 'DEL-01-04'): 'X-1'}
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
    _, nodes = read(DAG2 / 'DeliverableNodes.csv')
    ids = {n['DeliverableID'] for n in nodes}
    # Inventory: the accepted decomposition register is unchanged; the pointer file's bytes changed (B-06a note)
    # but it still names the same snapshot.
    inv = '_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv'
    manifest = {l.split('  ', 1)[1]: l.split('  ', 1)[0] for l in (DAG2 / 'SOURCE_MANIFEST.sha256').read_text().splitlines()}
    register_unchanged = sha(EXECUTION / inv) == manifest[inv]
    pointer_text = (EXECUTION / '_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md').read_text()
    pointer_bytes_changed = sha(EXECUTION / '_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md') != manifest['_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md']
    pointer_names_same_snapshot = 'GROUP3-20260928T001055Z' in pointer_text
    _, invrows = read(EXECUTION / inv)
    assert {x['DeliverableID'] for x in invrows} == ids and len(ids) == 41
    inventory_unchanged = register_unchanged and pointer_names_same_snapshot

    active = []; groups = defaultdict(list); nontopo = 0; retired = 0
    for n in nodes:
        src = n['DependenciesPath']; p = EXECUTION / src; _, rows = read(p)
        for i, r in enumerate(rows, 1):
            if r['DependencyClass'] == 'EXECUTION' and r['Status'] == 'RETIRED': retired += 1
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
            '--nodes', rel(DAG2 / 'DeliverableNodes.csv'), '--canonical',
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

    _, e2 = read(DAG2 / 'DependencyEdges.csv'); _, c2 = read(DAG2 / 'CandidateEdges.csv')
    a2 = {arc(r): r for r in e2}; k2 = {arc(r): r for r in c2}
    scc2 = json.loads((DAG2 / 'Evidence/SCC_Accounting.json').read_text())
    sccs2 = {frozenset(x['Members']) for x in scc2}
    old = set(a2) | set(k2); new = set(rep_of)
    added = sorted(new - old); removed = sorted(old - new)
    layer_changes = sorted(a for a in old & new if (a in a2) != (a in admitted))
    rep_changes = []
    for a in sorted(old & new):
        r_old = a2.get(a) or k2.get(a); r_new = rep_of[a]
        if (r_old['SourceRegister'], r_old['DependencyID']) != (r_new['SourceRegister'], r_new['DependencyID']):
            rep_changes.append({'arc': f'{a[0]} -> {a[1]}', 'dag002_representative': f"{r_old['SourceRegister']}#{r_old['DependencyID']}",
                                'current_representative': f"{r_new['SourceRegister']}#{r_new['DependencyID']}",
                                'layer': 'admitted' if a in admitted else 'candidate'})
    # Field drift on arcs already in DAG-002: representative rows whose 29 core columns changed.
    core_drift = []
    for a in sorted(old & new):
        r_old = a2.get(a) or k2.get(a); r_new = rep_of[a]
        if (r_old['SourceRegister'], r_old['DependencyID']) == (r_new['SourceRegister'], r_new['DependencyID']):
            diff = [f for f in core if r_old[f] != r_new[f]]
            if diff: core_drift.append({'arc': f'{a[0]} -> {a[1]}', 'row': f"{r_new['SourceRegister'].split('/')[2].split('_')[0]}#{r_new['DependencyID']}", 'fields': diff})
    # Labels (read-only) from ARC_ANALYSIS for any added arc; E-*/K-* are the kept-out guards.
    labels = {}
    for line in P2.read_text().splitlines():
        m = re.match(r'\|\s*((?:N|R8|X)-[A-Z0-9]+)\s*\|\s*(DEL-\d\d-\d\d)\s*→\s*(DEL-\d\d-\d\d)\s*\|', line)
        if m: labels.setdefault((m.group(2), m.group(3)), m.group(1))
    added_rows = []
    for a in added:
        r = rep_of[a]
        added_rows.append({'Consumer': a[0], 'Supplier': a[1], 'Label': EXPECTED.get(a, labels.get(a, 'UNLABELLED')),
                           'Layer': 'admitted' if a in admitted else 'candidate',
                           'SCC': ('SCC with ' + ';'.join(sccs[member[a[0]]])) if a in candidate else '',
                           'Representative': f"{r['SourceRegister']}#{r['DependencyID']}",
                           'Direction': r['Direction'], 'DependencyType': r['DependencyType'],
                           'RequiredMaturity': r['RequiredMaturity'], 'SatisfactionStatus': r['SatisfactionStatus'],
                           'ReverseArcPresent': 'Y' if (a[1], a[0]) in new else 'N'})
    write(EVIDENCE / 'added_arcs.csv', list(added_rows[0]) if added_rows else ['Consumer'], added_rows)
    guards_present = []
    for line in P2.read_text().splitlines():
        m = re.match(r'\|\s*((?:E|K)-\d+)\s*\|\s*(DEL-\d\d-\d\d)\s*→\s*(DEL-\d\d-\d\d)\s*\|', line)
        if m and (m.group(2), m.group(3)) in new: guards_present.append(m.group(1))
    pending = sorted({x for a in added + removed for x in a})
    sccs_unchanged = {frozenset(s) for s in sccs} == sccs2
    result = {
        'classification': 'DEPARTURE' if (added or removed or not sccs_unchanged or not inventory_unchanged) else 'CURRENT_WITH_EVIDENCE_DRIFT',
        'inventory_unchanged': inventory_unchanged,
        'inventory_detail': {'register_unchanged': register_unchanged, 'pointer_bytes_changed': pointer_bytes_changed,
                             'pointer_names_same_snapshot': pointer_names_same_snapshot},
        'active_execution_rows': len(active), 'retired_execution_rows': retired, 'non_topological_rows': nontopo,
        'deliverable_target_rows': sum(len(v) for v in groups.values()),
        'arcs': {'dag002_admitted': len(a2), 'dag002_candidate': len(k2), 'dag002_total': len(old),
                 'current_admitted': len(admitted), 'current_candidate': len(candidate), 'current_total': len(new),
                 'added': len(added), 'removed': len(removed),
                 'added_admitted': sum(a in admitted for a in added), 'added_candidate': sum(a in candidate for a in added),
                 'existing_arcs_changing_layer': [f'{a[0]} -> {a[1]}' for a in layer_changes]},
        'sccs_current': sccs, 'sccs_unchanged': sccs_unchanged,
        'representative_changes': rep_changes,
        'core_field_drift_on_existing_representatives': core_drift,
        'expected_arcs': {f'{k[0]} -> {k[1]}': v for k, v in EXPECTED.items()},
        'expected_arcs_present': sorted(f'{EXPECTED[a]} {a[0]} -> {a[1]}' for a in EXPECTED if a in new),
        'expected_arcs_missing': sorted(f'{EXPECTED[a]} {a[0]} -> {a[1]}' for a in EXPECTED if a not in new),
        'arcs_added_outside_expected': [f'{a[0]} -> {a[1]}' for a in added if a not in EXPECTED],
        'withheld_arcs_absent': {'N-12': ('DEL-03-02', 'DEL-04-03') not in new, 'N-B8': ('DEL-03-03', 'DEL-04-03') not in new},
        'kept_out_guard_arcs_present': guards_present,
        'del_04_01_suppliers': sorted(a[1] for a in new if a[0] == 'DEL-04-01'),
        'scc002_members_consuming_del_09_06': sorted(a[0] for a in new if a[1] == 'DEL-09-06' and a[0] in sccs[0]),
        'dag_pending': pending,
        'scratch_audit': {'tool': rel(TOOL), 'sha256': sha(TOOL), 'argv': argv, 'exit_code': p.returncode,
                          'edge_count': audit['active_graph']['edge_count'], 'scc_count': audit['active_graph']['scc_count'],
                          'canonical_finding_count': audit['canonical_finding_count']},
        'script': {'path': rel(Path(__file__)), 'sha256': sha(Path(__file__))},
    }
    (EVIDENCE / 'reapplication_result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('representative_changes', 'sccs_current')}, indent=2))


if __name__ == '__main__':
    main()
