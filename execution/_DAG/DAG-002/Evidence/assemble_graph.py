#!/usr/bin/env python3
"""DAG-002 successor candidate assembly (project-dag TRIGGER=SUCCESSOR).

Adapted from DAG-001/Evidence/assemble_graph.py (sha256 recorded in
Tool_Run.json). Applies DAG-001's confirmed SR-1..SR-7, carried forward
unchanged, to the registers frozen by this candidate's SOURCE_MANIFEST.sha256.

Reads: the frozen local files, the accepted GROUP3 register, DAG-001 (read
only), the closure snapshot, the currency audit and the SCC case rulings.
Writes: only this candidate's graph files and Evidence/. It never writes a
local register, SoW, _STATUS, case, the accepted DAG-001 or _DAG/_LATEST.md,
and asserts that those inputs are unchanged at the end.

Run from the repository root:
  python3 projects/chirality-app-v4/execution/_DAG/_Candidates/DAG-002/Evidence/assemble_graph.py
"""
from __future__ import annotations
import ast, csv, hashlib, json, re, subprocess, sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

CANDIDATE = Path(__file__).resolve().parent.parent
EVIDENCE = CANDIDATE / 'Evidence'
EXECUTION = CANDIDATE.parents[2]
ROOT = EXECUTION.parents[2]
DAG1 = EXECUTION / '_DAG/DAG-001'
SOURCE = 'b585e5ebead38f8ece442c80cd3bec5be8363cf3'
MANIFEST_HASH = '6d1021f1c78fea023c2089aa29a2bc60f5ae498f56068eeddbfa376467793250'
CLOSURE = EXECUTION / '_Evaluation/DepClosure/CLOSURE_APP_V4_BASISALIGN_2026-09-29_0855'
CURRENCY = EXECUTION / '_Evaluation/DAGCurrency/CURRENCY_APP_V4_BASISALIGN_2026-09-29_0856'
RUN = EXECUTION / '_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928'
INVENTORY = '_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv'
TOOL = ROOT / 'tools/coordination/audit_dag.py'
PROVENANCE = ['SourceRegister', 'SourceRegisterSHA256', 'SourceRecord', 'SelectionRule']
CANDIDATE_COLS = ['CandidateReason', 'SCCRef', 'CaseRef', 'OpenQuestion']
EXCLUDE_COLS = ['SourceRegister', 'SourceRegisterSHA256', 'SourceRecord', 'DependencyID', 'FromDeliverableID', 'Direction',
                'DependencyType', 'TargetType', 'TargetDeliverableID', 'TargetRefID', 'Disposition', 'RuleOrRuling',
                'RepresentedBy', 'Notes']
NODE_COLS = ['DeliverableID', 'PackageID', 'DeliverableName', 'ExecutionPath', 'DependenciesPath', 'RegisterState',
             'TrackingMode', 'InventorySource']
SR_BASE = 'SR-1;SR-2;SR-3(all canonical types);SR-4(no cut/merge ruling);SR-5(not applied);SR-6'


def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rel(p): return str(Path(p).resolve().relative_to(ROOT))
def fingerprint(p): return {'path': rel(p), 'sha256': sha(p)}


def read(p):
    with Path(p).open(encoding='utf-8-sig', newline='') as f:
        r = csv.DictReader(f); rows = list(r)
    assert all(None not in x and None not in x.values() for x in rows), f'Ragged {p}'
    return r.fieldnames, rows


def write(p, cols, rows):
    with Path(p).open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore', lineterminator='\n')
        w.writeheader(); w.writerows(rows)


def save(p, v): Path(p).write_text(json.dumps(v, indent=2, ensure_ascii=False) + '\n')
def git_bytes(rev, p): return subprocess.check_output(['git', 'show', f'{rev}:{rel(p)}'], cwd=ROOT)
def key(r): return (r['SourceRegister'], r['DependencyID'], str(r['SourceRecord']))
def locator(r): return f"{r['SourceRegister']}#{r['DependencyID']}@{r['SourceRecord']}"


def arc(r):
    a = (r['FromDeliverableID'], r['TargetDeliverableID'])
    return a if r['Direction'] == 'UPSTREAM' else a[::-1]


def rank(r): return (r['Direction'] != 'UPSTREAM', r['Origin'] != 'DECLARED', r['DependencyID'])


def protected_snapshot():
    paths = [EXECUTION / '_DAG/_LATEST.md', *DAG1.rglob('*'), *(EXECUTION / '_DAG/_Candidates/DAG-001').rglob('*'),
             *EXECUTION.glob('PKG*/1_Working/DEL*/_STATUS.md'), *EXECUTION.glob('PKG*/1_Working/DEL*/Dependencies.csv'),
             *EXECUTION.glob('PKG*/1_Working/DEL*/_DEPENDENCIES.md'), *EXECUTION.glob('PKG*/1_Working/DEL*/ScopeOfWork.md'),
             *CLOSURE.rglob('*')]
    return {rel(p): sha(p) for p in paths if p.is_file()}


def main():
    EVIDENCE.mkdir(exist_ok=True)
    protected = protected_snapshot()
    tree = ast.parse(TOOL.read_text())
    defs = {n.targets[0].id: ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
            and isinstance(n.targets[0], ast.Name) and n.targets[0].id in ['REQUIRED_COLUMNS', 'CANONICAL_ENUMS']}
    core = defs['REQUIRED_COLUMNS']; enums = defs['CANONICAL_ENUMS']; assert len(core) == 29

    # 1. Basis has not moved: every manifest member equals working bytes and the frozen commit.
    manifest = CANDIDATE / 'SOURCE_MANIFEST.sha256'; assert sha(manifest) == MANIFEST_HASH
    entries = []
    for line in manifest.read_text().splitlines():
        h, path = line.split('  ', 1); p = EXECUTION / path
        assert sha(p) == h, f'Manifest moved: {path}'
        assert hashlib.sha256(git_bytes(SOURCE, p)).hexdigest() == h, f'Commit mismatch: {path}'
        entries.append({'path': path, 'sha256': h})
    assert len(entries) == 130
    dag1_manifest = {l.split('  ', 1)[1]: l.split('  ', 1)[0] for l in (DAG1 / 'SOURCE_MANIFEST.sha256').read_text().splitlines()}
    assert [e['path'] for e in entries] == list(dag1_manifest), 'File classes differ from DAG-001'
    changed_members = [e['path'] for e in entries if dag1_manifest[e['path']] != e['sha256']]

    # 2. Inventory from the accepted register; expected byte-equal to DAG-001's node file.
    _, inventory = read(EXECUTION / INVENTORY); assert len(inventory) == 41
    ids = {x['DeliverableID'] for x in inventory}; assert len(ids) == 41
    nodes = []
    for x in sorted(inventory, key=lambda x: x['DeliverableID']):
        paths = list(EXECUTION.glob(f"{x['PackageID']}_*/1_Working/{x['DeliverableID']}_*")); assert len(paths) == 1
        p = paths[0]; h, _ = read(p / 'Dependencies.csv')
        assert h[:29] == core and len(h) == len(set(h))
        assert 'FULL_GRAPH' in (p / '_DEPENDENCIES.md').read_text()
        nodes.append(dict(zip(NODE_COLS, [x['DeliverableID'], x['PackageID'], x['Name'], str(p.relative_to(EXECUTION)),
                                          str((p / 'Dependencies.csv').relative_to(EXECUTION)), 'PRESENT', 'FULL_GRAPH', INVENTORY])))
    assert read(DAG1 / 'DeliverableNodes.csv')[1] == nodes, 'Re-derived inventory differs from DAG-001'
    (CANDIDATE / 'DeliverableNodes.csv').write_bytes((DAG1 / 'DeliverableNodes.csv').read_bytes())
    nodes_byte_equal = sha(CANDIDATE / 'DeliverableNodes.csv') == sha(DAG1 / 'DeliverableNodes.csv')

    # 3. SR-1..SR-6 on the frozen registers.
    all_rows = []; active = []; per_register = {}; groups = defaultdict(list); exclusions = []
    for node in nodes:
        src = node['DependenciesPath']; p = EXECUTION / src; _, rows = read(p)
        counts = Counter(); counts['TotalRows'] = len(rows); seen = set()
        for i, r in enumerate(rows, 1):
            assert r['DependencyID'] not in seen, f'Duplicate ID {p}'; seen.add(r['DependencyID'])
            assert r['FromDeliverableID'] == node['DeliverableID'] and r['FromPackageID'] == node['PackageID']
            assert all(r[f] in v for f, v in enums.items()), f'Invalid enum {p}:{i}'
            assert r['RegisterSchemaVersion'] == 'v3.1'
            out = {k: r[k] for k in core}
            out.update(SourceRegister=src, SourceRegisterSHA256=sha(p), SourceRecord=str(i), SelectionRule='')
            all_rows.append(out)
            if r['DependencyClass'] == 'ANCHOR': counts['AnchorRows'] += 1
            if r['Status'] == 'RETIRED': counts['RetiredRows'] += 1
            if r['Status'] != 'ACTIVE' or r['DependencyClass'] != 'EXECUTION': continue
            active.append(out); counts['ActiveExecution'] += 1
            if r['TargetType'] != 'DELIVERABLE':
                exclusions.append({**out, 'Disposition': 'NOT_TOPOLOGICAL', 'RuleOrRuling': 'SR-2', 'RepresentedBy': '',
                                   'Notes': 'Non-deliverable input retained unchanged in source and Evidence/all_execution_rows.csv; exclusion supplies no contribution or readiness.'})
            else:
                assert r['TargetDeliverableID'] in ids and re.fullmatch(r'DEL-\d{2}-\d{2}', r['TargetDeliverableID'])
                groups[arc(out)].append(out)
        per_register[src] = {'DeliverableID': node['DeliverableID'], **counts}
    admissible = []; mirror_pairs = []
    for pair, rows in sorted(groups.items()):
        ordered = sorted(rows, key=rank); rep = ordered[0]; rep['SelectionRule'] = SR_BASE
        admissible.append(rep)
        for other in ordered[1:]:
            disp = 'MIRROR' if other['SourceRegister'] != rep['SourceRegister'] else 'SAME_ARC'
            exclusions.append({**other, 'Disposition': disp, 'RuleOrRuling': 'SR-6', 'RepresentedBy': locator(rep),
                               'Notes': 'Topology represented once; original contribution, type, conditions, maturity and satisfaction remain live source obligations. See Evidence/MirrorComparisons.csv.'})
            mirror_pairs.append((pair, rep, other, disp))
    write(EVIDENCE / 'admissible_edges.csv', core + PROVENANCE, admissible)

    runs = []
    def audit(name, args, subject, require_zero=True):
        argv = ['python3', rel(TOOL), *args]; p = subprocess.run(argv, cwd=ROOT, text=True, capture_output=True)
        (EVIDENCE / f'{name}.stdout.txt').write_text(p.stdout); (EVIDENCE / f'{name}.stderr.txt').write_text(p.stderr)
        runs.append({'name': name, 'tool': fingerprint(TOOL), 'arguments': argv, 'cwd': '<repository root>',
                     'exit_code': p.returncode, 'run_status': 'COMPLETE' if p.returncode == 0 else 'FAILED',
                     'subject_status': subject, 'stdout': f'{name}.stdout.txt', 'stderr': f'{name}.stderr.txt'})
        if require_zero: assert p.returncode == 0, p.stdout + p.stderr

    # 4. SR-7 on the admissible set; SCCs must equal the closure snapshot's.
    audit('admissible_audit', ['--edges', rel(EVIDENCE / 'admissible_edges.csv'), '--nodes', rel(CANDIDATE / 'DeliverableNodes.csv'),
                               '--canonical', '--json-out', rel(EVIDENCE / 'admissible_audit.json')],
          'FAIL_RAW_ACYCLIC_OBJECTIVE; CHARACTERIZED_UNRESOLVED_CYCLES')
    raw = json.loads((EVIDENCE / 'admissible_audit.json').read_text())
    _, scc_rows = read(CLOSURE / 'Evidence/scc_summary.csv')
    scc_sets = {x['SCC_ID']: set(x['Nodes'].split(';')) for x in scc_rows}
    assert {frozenset(s) for s in raw['active_graph']['sccs']} == {frozenset(s) for s in scc_sets.values()}
    assert raw['canonical_finding_count'] == 0 and raw['endpoint_issue_count'] == 0
    dag1_scc = json.loads((DAG1 / 'Evidence/SCC_Accounting.json').read_text())
    case_by_set = {frozenset(x['Members']): x['CaseRef'] for x in dag1_scc}
    assert set(case_by_set) == {frozenset(s) for s in scc_sets.values()}, 'SCC membership changed from DAG-001'
    case_map = {s: case_by_set[frozenset(ns)] for s, ns in scc_sets.items()}
    _, c1 = read(DAG1 / 'CandidateEdges.csv')
    questions = {}
    for x in c1:
        questions.setdefault(x['CaseRef'], x['OpenQuestion'])
    member_to_scc = {n: s for s, ns in scc_sets.items() for n in ns}
    admitted = []; candidates = []
    for row in admissible:
        a, b = arc(row); s = member_to_scc.get(a); assert a != b, 'Unexpected self-loop'
        if s and s == member_to_scc.get(b):
            case = case_map[s]
            _, rulings = read(EXECUTION / case / 'Ruling_Register.csv')
            assert any(x['RulingID'] == 'CP1-20260928' and x['Status'] == 'RECORDED_ACTUAL_BASIS_ONLY' for x in rulings)
            candidates.append({**row, 'SelectionRule': row['SelectionRule'] + ';SR-7(held)', 'CandidateReason': 'SCC_UNRESOLVED',
                               'SCCRef': s, 'CaseRef': case, 'OpenQuestion': questions[case]})
        else:
            admitted.append({**row, 'SelectionRule': row['SelectionRule'] + ';SR-7(admitted)'})
    exclusions.sort(key=key)
    write(CANDIDATE / 'DependencyEdges.csv', core + PROVENANCE, admitted)
    write(CANDIDATE / 'CandidateEdges.csv', core + PROVENANCE + CANDIDATE_COLS, candidates)
    write(CANDIDATE / 'ExcludedRows.csv', EXCLUDE_COLS, exclusions)

    # 5. Acceptance check on the admitted layer (exit 0 required), then candidate-layer evidence.
    audit('dag_audit', ['--dag-dir', rel(CANDIDATE), '--canonical', '--strict', '--json-out', rel(EVIDENCE / 'dag_audit.json')],
          'PASS_ADMITTED_LAYER_ONLY')
    audit('candidate_audit', ['--dag-dir', rel(CANDIDATE), '--edges', rel(CANDIDATE / 'CandidateEdges.csv'), '--canonical',
                              '--json-out', rel(EVIDENCE / 'candidate_audit.json')],
          'FAIL_ACYCLIC_OBJECTIVE_EXPECTED; NON_GATING_CANDIDATE_LAYER')

    # 6. Accounting and byte fidelity on the serialized files.
    admitted = read(CANDIDATE / 'DependencyEdges.csv')[1]; candidates = read(CANDIDATE / 'CandidateEdges.csv')[1]
    exclusions = read(CANDIDATE / 'ExcludedRows.csv')[1]
    original = {key(x): x for x in active}; placements = {}; fidelity = 0
    for fn, rows in [('DependencyEdges.csv', admitted), ('CandidateEdges.csv', candidates), ('ExcludedRows.csv', exclusions)]:
        for x in rows:
            k = key(x); assert k in original and k not in placements; placements[k] = fn
            src = original[k]; assert x['SourceRegisterSHA256'] == src['SourceRegisterSHA256']
            if fn != 'ExcludedRows.csv':
                assert all(x[f].encode('utf-8') == src[f].encode('utf-8') for f in core); fidelity += 1
            else:
                assert all(x[f] == src[f] for f in EXCLUDE_COLS[:10])
    assert set(placements) == set(original)
    for x in admitted + candidates:
        for f in ('Explicitness', 'SatisfactionStatus', 'Confidence'):
            assert x[f] in enums[f] and x[f] != '', f'Required field blank: {locator(x)} {f}'
    evidence_rows = []
    for x in active:
        evidence_rows.append({**x, 'AccountingLayer': placements[key(x)]})
        reg = per_register[x['SourceRegister']]; reg[placements[key(x)]] = reg.get(placements[key(x)], 0) + 1
    write(EVIDENCE / 'all_execution_rows.csv', core + PROVENANCE + ['AccountingLayer'], evidence_rows)

    # 7. Non-topological inputs: DAG-001's A/B/C account carried forward by row identity.
    _, nt1 = read(DAG1 / 'Evidence/NonTopologicalInputs.csv')
    prior_class = {(x['SourceRegister'], x['DependencyID']): x for x in nt1}
    non_topological = []; nt_status = Counter()
    for x in active:
        if x['TargetType'] == 'DELIVERABLE': continue
        p = prior_class.get((x['SourceRegister'], x['DependencyID']))
        if p:
            edited = [f for f in core if p[f] != x[f] and f != 'LastSeen']
            info = (p['InputClass'], p['InputAccount'], p['AccountSource'] + (f" (carried from DAG-001; fields edited since: {', '.join(edited)}; re-read the live row)" if edited else ''))
            nt_status['carried_row_edited' if edited else 'carried_unchanged_except_LastSeen'] += 1
        else:
            info = ('NOT_CLASSIFIED_A_B_C', 'New since DAG-001. External/document input retained at its source point of need; no new human-choice classification inferred.', x['SourceRegister'])
            nt_status['new'] += 1
        if x['TargetType'] in ('PACKAGE', 'UNKNOWN'): assert p, f'Unclassified PACKAGE/UNKNOWN row {locator(x)}'
        non_topological.append({**x, 'InputClass': info[0], 'InputAccount': info[1], 'AccountSource': info[2]})
    write(EVIDENCE / 'NonTopologicalInputs.csv', core + PROVENANCE + ['InputClass', 'InputAccount', 'AccountSource'], non_topological)

    # 8. Departure account against DAG-001, with P2 labels (read only).
    _, e1 = read(DAG1 / 'DependencyEdges.csv')
    a1 = {arc(r): r for r in e1}; k1 = {arc(r): r for r in c1}; old = set(a1) | set(k1)
    rep_now = {arc(r): r for r in admitted + candidates}; now = set(rep_now)
    added = sorted(now - old); removed = sorted(old - now)
    labels = {}
    for line in (RUN / 'DAG_PREP/ARC_ANALYSIS.md').read_text().splitlines():
        m = re.match(r'\|\s*((?:N|R8|X)-[A-Z0-9]+)\s*\|\s*(DEL-\d\d-\d\d)\s*→\s*(DEL-\d\d-\d\d)\s*\|', line)
        if m: labels.setdefault((m.group(2), m.group(3)), m.group(1))
    accepted_set = {k for k, v in labels.items() if v not in ('N-12', 'N-B8')}; assert len(accepted_set) == 41
    rows_on = defaultdict(list)
    for x in active:
        if x['TargetType'] == 'DELIVERABLE': rows_on[arc(x)].append(x)
    dep = []
    for a in added:
        r = rep_now[a]
        dep.append({'Consumer': a[0], 'Supplier': a[1], 'P2Label': labels.get(a, 'UNLABELLED'),
                    'Layer': 'admitted' if a in {arc(x) for x in admitted} else 'candidate',
                    'SCCRef': r.get('SCCRef', ''), 'CaseRef': r.get('CaseRef', ''),
                    'Representative': locator(r), 'RepresentativeDirection': r['Direction'], 'DependencyType': r['DependencyType'],
                    'RequiredMaturity': r['RequiredMaturity'], 'SatisfactionStatus': r['SatisfactionStatus'],
                    'OtherRowsOnArc': ';'.join(locator(y) for y in rows_on[a] if key(y) != key(r))})
    write(EVIDENCE / 'DepartureAccount.csv', list(dep[0]), dep)
    rep_changes = []
    for a in sorted(old & now):
        o = a1.get(a) or k1.get(a); n = rep_now[a]
        if (o['SourceRegister'], o['DependencyID']) != (n['SourceRegister'], n['DependencyID']):
            rep_changes.append({'arc': f'{a[0]} -> {a[1]}', 'dag001': f"{o['SourceRegister']}#{o['DependencyID']}",
                                'dag002': locator(n), 'layer': 'admitted' if a in a1 else 'candidate'})
    layer_moves = [f'{a[0]} -> {a[1]}' for a in sorted(old & now) if (a in a1) != (a in {arc(x) for x in admitted})]
    departure = {'added': len(added), 'removed': len(removed), 'removed_arcs': [f'{a[0]} -> {a[1]}' for a in removed],
                 'added_admitted': sum(d['Layer'] == 'admitted' for d in dep), 'added_candidate': sum(d['Layer'] == 'candidate' for d in dep),
                 'existing_arcs_changing_layer': layer_moves, 'representative_changes': rep_changes,
                 'accepted_arc_set_size': len(accepted_set),
                 'accepted_arcs_not_produced': [f'{labels[a]} {a[0]} -> {a[1]}' for a in sorted(accepted_set - now)],
                 'added_outside_accepted_set': [f'{a[0]} -> {a[1]}' for a in added if a not in accepted_set],
                 'withheld_absent': {'N-12': ('DEL-03-02', 'DEL-04-03') not in now, 'N-B8': ('DEL-03-03', 'DEL-04-03') not in now},
                 'dag_pending_resolved_by_this_candidate': sorted({x for a in added + removed for x in a})}
    save(EVIDENCE / 'DepartureAccount.json', departure)

    # 9. Mirror comparisons (all) and the pairs new or changed since DAG-001.
    dag1_pairs = set()
    _, m1 = read(DAG1 / 'Evidence/MirrorComparisons.csv')
    for x in m1: dag1_pairs.add((x['Representative'].split('@')[0], x['Other'].split('@')[0]))
    comparisons = []
    for pair, rep, other, disp in mirror_pairs:
        diff = [f for f in ['DependencyType', 'RequiredMaturity', 'ProposedMaturity', 'Statement', 'SatisfactionStatus'] if rep[f] != other[f]]
        is_new = (locator(rep).split('@')[0], locator(other).split('@')[0]) not in dag1_pairs
        comparisons.append({'Consumer': pair[0], 'Supplier': pair[1], 'Representative': locator(rep), 'Other': locator(other),
                            'Disposition': disp, 'NewSinceDAG001': 'Y' if is_new else 'N', 'DifferentFields': ';'.join(diff),
                            **{f'Representative{f}': rep[f] for f in ['DependencyType', 'RequiredMaturity', 'ProposedMaturity', 'Statement', 'EvidenceQuote', 'SourceRef', 'SatisfactionStatus']},
                            **{f'Other{f}': other[f] for f in ['DependencyType', 'RequiredMaturity', 'ProposedMaturity', 'Statement', 'EvidenceQuote', 'SourceRef', 'SatisfactionStatus']}})
    write(EVIDENCE / 'MirrorComparisons.csv', list(comparisons[0]), comparisons)

    # 10. SCC accounting with continuing cases.
    scc_account = []
    for s, ns in scc_sets.items():
        internal = [x for x in active if x['TargetType'] == 'DELIVERABLE' and set(arc(x)) <= ns]
        held = [x for x in candidates if x['SCCRef'] == s]
        prior = next(x for x in dag1_scc if set(x['Members']) == ns)
        scc_account.append({'SCCRef': s, 'CaseRef': case_map[s], 'Members': sorted(ns), 'MemberCount': len(ns),
                            'SourceRows': len(internal), 'HeldArcs': len(held), 'ExcludedIntraSCCRows': len(internal) - len(held),
                            'DAG001': {'SCCRef': prior['SCCRef'], 'SourceRows': prior['SourceRows'], 'HeldArcs': prior['HeldArcs']},
                            'CaseState': 'EVIDENCE_ACCUMULATING; BASIS_CONFIRMED; UNRESOLVED',
                            'RetainedHistory': '_DAG/cases/SCC-CASE-004' if case_map[s].endswith('SCC-CASE-002') else None})
    save(EVIDENCE / 'SCC_Accounting.json', scc_account)

    dag = json.loads((EVIDENCE / 'dag_audit.json').read_text())
    assert dag['node_row_count'] == 41 and dag['active_graph']['scc_count'] == 0 and dag['canonical_finding_count'] == 0
    assert dag['active_graph']['duplicate_edge_count'] == 0 and dag['active_graph']['bidirectional_pair_count'] == 0
    assert dag['node_row_width_issue_count'] == 0 and dag['edge_row_width_issue_count'] == 0 and dag['endpoint_issue_count'] == 0
    assert len({arc(x) for x in admitted}) == len(admitted)
    after = protected_snapshot()
    assert after == protected, 'A protected input changed during assembly'

    dispositions = dict(Counter(x['Disposition'] for x in exclusions))
    checks = {'result': 'PASS', 'source_revision': SOURCE, 'manifest_sha256': MANIFEST_HASH, 'manifest_entries': 130,
              'manifest_matches_source_commit': True, 'manifest_members_changed_since_dag001': len(changed_members),
              'node_count': 41, 'nodes_byte_equal_to_dag001': nodes_byte_equal, 'packages': len({n['PackageID'] for n in nodes}),
              'total_source_rows': len(all_rows), 'active_anchors': sum(x['DependencyClass'] == 'ANCHOR' and x['Status'] == 'ACTIVE' for x in all_rows),
              'retired_rows': sum(x['Status'] == 'RETIRED' for x in all_rows), 'active_execution': len(active),
              'deliverable_target_rows': sum(len(v) for v in groups.values()), 'admissible_arcs': len(admissible),
              'admitted_rows': len(admitted), 'candidate_rows': len(candidates), 'excluded_rows': len(exclusions),
              'dispositions': dispositions, 'candidate_reasons': dict(Counter(x['CandidateReason'] for x in candidates)),
              'target_types': dict(Counter(x['TargetType'] for x in active)), 'maturity': dict(Counter(x['RequiredMaturity'] for x in active)),
              'satisfaction': dict(Counter(x['SatisfactionStatus'] for x in active)), 'edge_core_fidelity_rows': fidelity,
              'core_fields_per_row': 29, 'missing_rows': 0, 'overlapping_rows': 0, 'self_loops': 0,
              'closure_scc_membership_exact': True, 'scc_membership_equal_to_dag001': True, 'case_mapping': case_map,
              'non_topological_account': dict(nt_status), 'mirror_comparisons': len(comparisons),
              'mirror_comparisons_new_since_dag001': sum(c['NewSinceDAG001'] == 'Y' for c in comparisons),
              'departure': {k: departure[k] for k in ('added', 'removed', 'added_admitted', 'added_candidate')},
              'strict_admitted_exit_code': 0, 'protected_inputs_unchanged': True, 'protected_input_count': len(protected),
              'no_accepted_pointer_written': True,
              'authority': 'UNACCEPTED CANDIDATE; no lifecycle, satisfaction, readiness or gate effect inferred'}
    save(EVIDENCE / 'AssemblyChecks.json', checks)
    write(EVIDENCE / 'RegisterAccounting.csv', ['SourceRegister', 'DeliverableID', 'TotalRows', 'AnchorRows', 'RetiredRows', 'ActiveExecution',
                                                'DependencyEdges.csv', 'CandidateEdges.csv', 'ExcludedRows.csv'],
          [{'SourceRegister': s, **{k: v.get(k, 0) for k in ['DeliverableID', 'TotalRows', 'AnchorRows', 'RetiredRows', 'ActiveExecution',
                                                             'DependencyEdges.csv', 'CandidateEdges.csv', 'ExcludedRows.csv']}} for s, v in per_register.items()])
    for s, v in per_register.items():
        assert v.get('ActiveExecution', 0) == v.get('DependencyEdges.csv', 0) + v.get('CandidateEdges.csv', 0) + v.get('ExcludedRows.csv', 0)

    context = [ROOT / 'AGENTS.md', ROOT / 'agents/AGENT_TASK.md', ROOT / 'workflows/project-dag/WORKFLOW.md',
               ROOT / 'workflows/project-dag/resources/contract.md', ROOT / 'workflows/project-dag/resources/method.md',
               ROOT / 'workflows/project-dag/resources/graph-version.md', ROOT / 'workflows/project-dag/resources/currency.md',
               ROOT / 'workflows/audit-dep-closure/WORKFLOW.md', ROOT / 'workflows/scc-resolution-case/WORKFLOW.md',
               RUN / 'OWNER_DECISIONS.md', RUN / 'DISPATCH.md', RUN / 'DAG_PREP/SUCCESSOR_PLAN.md', RUN / 'DAG_PREP/ARC_ANALYSIS.md',
               RUN / 'DAG_PREP/REGISTER_CHANGES.md']
    save(EVIDENCE / 'Tool_Run.json', {
        'schema_version': 1, 'workflow': 'chirality-root:bundled:workflow:project-dag', 'trigger': 'SUCCESSOR',
        'run': 'APP-V4-BASIS-ALIGN-20260928', 'node': 'D1',
        'actor': 'Type 2 TASK executor, Claude Code Agent subagent (node D1)', 'parent': 'HELP_HUMAN integrator under a recorded WORKING_ITEMS consultation',
        'role': 'TASK', 'mechanism': 'Claude Code Agent subagent; no descendants', 'source_revision': SOURCE,
        'selected_context': [fingerprint(p) for p in context], 'assembly_script': fingerprint(Path(__file__)),
        'adapted_from': fingerprint(DAG1 / 'Evidence/assemble_graph.py'), 'python': sys.version, 'runs': runs,
        'script_command': ['python3', rel(Path(__file__))], 'finished_at': datetime.now(timezone.utc).isoformat(),
        'process_subject_distinction': 'Non-strict audits exit 0 with cyclic subjects; the strict admitted audit exits 0 and passes only its subject. Neither accepts the graph.',
        'tool_limits': 'No --markdown-out output is published (its title and front matter are DEV-001-specific). The dev001_projection JSON section is preserved but not relied on.',
        'host_vs_brief': 'The host permits wider workspace writes. The D1 brief narrows writes to _Evaluation/, this candidate, CASE files for evidence updates and DAG_PREP/CHECKPOINT_C.md. No OS-level confinement is claimed. Git is read-only; no delegation.'})
    print(json.dumps(checks, indent=2))


if __name__ == '__main__':
    main()
