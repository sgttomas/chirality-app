#!/usr/bin/env python3
"""Currency audit scratch re-application of DAG-004's accepted selection rules.

project-dag currency.md step 4, after the DEL-01-03 TargetLocation repair (run
APP-V4-SCA003-20261002, node FX; DECISION-3 effect 4). Reads the live local
registers named by DAG-004's DeliverableNodes.csv, re-applies the confirmed
SR-1..SR-7 as DAG-004 applied them (carried unchanged from DAG-001), and
compares the admitted arcs, candidate arcs, SCCs, representatives and inventory
with the accepted DAG-004 files. Writes only into this Evidence/ folder. It is a
scratch assembly, not a graph version; it edits no accepted version, local file
or case.

Adapted from _Evaluation/DAGCurrency/CURRENCY_APP_V4_SCA003_2026-10-03_1937/Evidence/reapply_selection.py
(sha256 recorded in ../Tool_Run.json): the comparison base is DAG-004, no arc
is expected to change, and the guards carried in DAG-004's HANDOFF_STATE.md are
re-checked.

Run from the repository root:
  python3 <this file>
"""
from __future__ import annotations
import ast, csv, hashlib, json, re, subprocess
from collections import defaultdict
from pathlib import Path

EVIDENCE = Path(__file__).resolve().parent
ROOT = next(p for p in EVIDENCE.parents if (p / 'tools/coordination/audit_dag.py').is_file())
EXECUTION = ROOT / 'projects/chirality-app-v4/execution'
DAG3 = EXECUTION / '_DAG/DAG-004'  # comparison base (name kept from the adapted script)
TOOL = ROOT / 'tools/coordination/audit_dag.py'
INV = '_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv'
# No arc is expected to change: the repair rewrites TargetLocation cells only.
EXPECTED = {}
EXPECTED_ADMITTED = set()
# Arcs that must stay absent (ARC_EFFECT §1.4, §3; DAG-003 HANDOFF_STATE guards).
ABSENT = {'N-12': ('DEL-03-02', 'DEL-04-03'), 'N-B8': ('DEL-03-03', 'DEL-04-03'), 'NR-03': ('DEL-09-09', 'DEL-01-02'),
          'NR-06': ('DEL-02-04', 'DEL-01-03'), 'NR-10': ('DEL-02-04', 'DEL-02-02'),
          'E-1': ('DEL-09-09', 'DEL-09-06'), 'K-11': ('DEL-03-03', 'DEL-09-06'), 'E-5': ('DEL-09-06', 'DEL-03-04'),
          'K-7': ('DEL-09-06', 'DEL-09-07'), 'K-6': ('DEL-09-06', 'DEL-09-09'),
          'REQ-008 source wording a': ('DEL-04-01', 'DEL-01-04'), 'REQ-008 source wording b': ('DEL-04-03', 'DEL-01-04')}
R17_10_FORBIDDEN = {'DEL-01-04', 'DEL-02-02', 'DEL-02-03', 'DEL-04-02', 'DEL-04-03', 'DEL-06-01'}
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


def reach(start, arcs):
    out = defaultdict(set)
    for a, b in arcs: out[a].add(b)
    seen, stack = set(), [start]
    while stack:
        for n in out[stack.pop()]:
            if n not in seen: seen.add(n); stack.append(n)
    return seen


def main():
    tree = ast.parse(TOOL.read_text())
    core = [ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
            and isinstance(n.targets[0], ast.Name) and n.targets[0].id == 'REQUIRED_COLUMNS'][0]
    assert len(core) == 29
    _, nodes = read(DAG3 / 'DeliverableNodes.csv')
    ids = {n['DeliverableID'] for n in nodes}
    manifest = {l.split('  ', 1)[1]: l.split('  ', 1)[0] for l in (DAG3 / 'SOURCE_MANIFEST.sha256').read_text().splitlines()}
    changed_members = sorted(p for p, h in manifest.items() if sha(EXECUTION / p) != h)
    register_unchanged = sha(EXECUTION / INV) == manifest[INV]
    pointer = '_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md'
    pointer_bytes_changed = sha(EXECUTION / pointer) != manifest[pointer]
    pointer_names_same_snapshot = 'GROUP3-20260928T001055Z' in (EXECUTION / pointer).read_text()
    _, invrows = read(EXECUTION / INV)
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
            '--nodes', rel(DAG3 / 'DeliverableNodes.csv'), '--canonical',
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

    _, e3 = read(DAG3 / 'DependencyEdges.csv'); _, c3 = read(DAG3 / 'CandidateEdges.csv')
    a3 = {arc(r): r for r in e3}; k3 = {arc(r): r for r in c3}
    scc3 = json.loads((DAG3 / 'Evidence/SCC_Accounting.json').read_text())
    sccs3 = {frozenset(x['Members']) for x in scc3}
    old = set(a3) | set(k3); new = set(rep_of)
    added = sorted(new - old); removed = sorted(old - new)
    layer_changes = sorted(a for a in old & new if (a in a3) != (a in admitted))
    rep_changes = []; core_drift = []
    for a in sorted(old & new):
        r_old = a3.get(a) or k3.get(a); r_new = rep_of[a]
        if (r_old['SourceRegister'], r_old['DependencyID']) != (r_new['SourceRegister'], r_new['DependencyID']):
            rep_changes.append({'arc': f'{a[0]} -> {a[1]}', 'dag004_representative': f"{r_old['SourceRegister']}#{r_old['DependencyID']}",
                                'current_representative': f"{r_new['SourceRegister']}#{r_new['DependencyID']}",
                                'layer': 'admitted' if a in admitted else 'candidate'})
        else:
            diff = [f for f in core if r_old[f] != r_new[f]]
            if diff: core_drift.append({'arc': f'{a[0]} -> {a[1]}', 'row': r_new['DependencyID'], 'fields': diff})
    added_rows = []
    for a in added:
        r = rep_of[a]
        added_rows.append({'Consumer': a[0], 'Supplier': a[1], 'Label': EXPECTED.get(a, 'UNLABELLED'),
                           'Layer': 'admitted' if a in admitted else 'candidate',
                           'SCC': ('SCC with ' + ';'.join(sccs[member[a[0]]])) if a in candidate else '',
                           'Representative': f"{r['SourceRegister']}#{r['DependencyID']}",
                           'Direction': r['Direction'], 'DependencyType': r['DependencyType'],
                           'RequiredMaturity': r['RequiredMaturity'], 'SatisfactionStatus': r['SatisfactionStatus'],
                           'RowsOnArc': len(groups[a]),
                           'ReverseArcPresent': 'Y' if (a[1], a[0]) in new else 'N'})
    write(EVIDENCE / 'added_arcs.csv', list(added_rows[0]) if added_rows else ['Consumer'], added_rows)
    pending = sorted({x for a in added + removed for x in a})
    sccs_unchanged = {frozenset(s) for s in sccs} == sccs3
    # Advice (not DAG pending): deliverables whose admitted routes now pass through an added admitted arc,
    # i.e. that reach the consumer of such an arc through admitted arcs (or are that consumer).
    added_admitted = [a for a in added if a in admitted]
    rev_admitted = [(b, a) for a, b in admitted]
    advice = {}
    for a in added_admitted:
        for n in reach(a[0], rev_admitted) | {a[0]}:
            advice.setdefault(n, set()).add(f'{EXPECTED.get(a, "?")} {a[0]} -> {a[1]}')
    advice = {k: sorted(v) for k, v in sorted(advice.items())}
    result = {
        'classification': 'DEPARTURE' if (added or removed or not sccs_unchanged or not inventory_unchanged) else
                          ('CURRENT_WITH_EVIDENCE_DRIFT' if changed_members else 'CURRENT'),
        'source_manifest_members': len(manifest), 'source_manifest_members_changed': len(changed_members),
        'changed_members': changed_members,
        'inventory_unchanged': inventory_unchanged,
        'inventory_detail': {'register_unchanged': register_unchanged, 'pointer_bytes_changed': pointer_bytes_changed,
                             'pointer_names_same_snapshot': pointer_names_same_snapshot},
        'active_execution_rows': len(active), 'retired_execution_rows': retired, 'non_topological_rows': nontopo,
        'deliverable_target_rows': sum(len(v) for v in groups.values()),
        'arcs': {'dag004_admitted': len(a3), 'dag004_candidate': len(k3), 'dag004_total': len(old),
                 'current_admitted': len(admitted), 'current_candidate': len(candidate), 'current_total': len(new),
                 'added': len(added), 'removed': len(removed),
                 'added_admitted': sum(a in admitted for a in added), 'added_candidate': sum(a in candidate for a in added),
                 'existing_arcs_changing_layer': [f'{a[0]} -> {a[1]}' for a in layer_changes],
                 'reciprocal_pairs': len({frozenset(a) for a in new if (a[1], a[0]) in new})},
        'sccs_current': sccs, 'sccs_unchanged': sccs_unchanged,
        'representative_changes': rep_changes,
        'core_field_drift_on_existing_representatives': core_drift,
        'expected_arcs': {f'{k[0]} -> {k[1]}': v for k, v in EXPECTED.items()},
        'expected_arcs_missing': sorted(f'{EXPECTED[a]} {a[0]} -> {a[1]}' for a in EXPECTED if a not in new),
        'arcs_added_outside_expected': [f'{a[0]} -> {a[1]}' for a in added if a not in EXPECTED],
        'expected_layers_hold': all((a in admitted) == (a in EXPECTED_ADMITTED) for a in EXPECTED if a in new),
        'guard_arcs_present': sorted(k for k, a in ABSENT.items() if a in new),
        'del_04_01_suppliers': sorted(a[1] for a in new if a[0] == 'DEL-04-01'),
        'scc002_members_consuming_del_09_06': sorted(a[0] for a in new if a[1] == 'DEL-09-06' and a[0] in sccs[0]),
        'r17_10': {'DEL-01-02_reaches': sorted(reach('DEL-01-02', new)), 'DEL-01-03_reaches': sorted(reach('DEL-01-03', new)),
                   'holds': not ((reach('DEL-01-02', new) | reach('DEL-01-03', new)) & R17_10_FORBIDDEN)},
        'dag_pending': pending,
        'advice_renewed_examination': advice,
        'scratch_audit': {'tool': rel(TOOL), 'sha256': sha(TOOL), 'argv': argv, 'exit_code': p.returncode,
                          'edge_count': audit['active_graph']['edge_count'], 'scc_count': audit['active_graph']['scc_count'],
                          'canonical_finding_count': audit['canonical_finding_count']},
        'script': {'path': rel(Path(__file__)), 'sha256': sha(Path(__file__))},
    }
    (EVIDENCE / 'reapplication_result.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('representative_changes', 'sccs_current', 'changed_members',
                                                                  'core_field_drift_on_existing_representatives')}, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
