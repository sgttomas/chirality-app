#!/usr/bin/env python3
"""DAG-004 successor candidate assembly (project-dag TRIGGER=SUCCESSOR).

Adapted from _DAG/DAG-003/Evidence/assemble_graph.py (sha256 recorded in
Tool_Run.json). Applies DAG-003's confirmed SR-1..SR-7, carried forward
unchanged from DAG-001 through DAG-002, to the registers frozen by this
candidate's SOURCE_MANIFEST.sha256.

Staged location: this candidate is prepared in the run folder
(_Coordination/AgentRuns/APP-V4-SCA003-20261002/DAG_PREP/DAG-004/) because the
D1 brief fences writes out of _DAG/. The script is location-independent: the
repository root is found by walking up to tools/coordination/audit_dag.py, and
the closure and currency snapshots are located through RUN_DAG_PREP, so it
reruns unchanged after a byte-for-byte copy to _DAG/_Candidates/DAG-004/ or
_DAG/DAG-004/.

Reads: the frozen local files, the accepted GROUP3 register, DAG-003 (read
only), the closure snapshot, the currency audit and the SCC case rulings.
Writes: only this candidate's graph files and Evidence/. It never writes a
local register, SoW, _STATUS, case, an accepted DAG, or _DAG/_LATEST.md, and
asserts that those inputs are unchanged at the end.

Run from the repository root:
  python3 <candidate>/Evidence/assemble_graph.py
"""
from __future__ import annotations
import ast, csv, hashlib, json, re, subprocess, sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

CANDIDATE = Path(__file__).resolve().parent.parent
EVIDENCE = CANDIDATE / 'Evidence'
ROOT = next(p for p in CANDIDATE.parents if (p / 'tools/coordination/audit_dag.py').is_file())
EXECUTION = ROOT / 'projects/chirality-app-v4/execution'
DAG3 = EXECUTION / '_DAG/DAG-003'
DAG2 = EXECUTION / '_DAG/DAG-002'
DAG1 = EXECUTION / '_DAG/DAG-001'
SOURCE = '75764184b99ab006cd46c1d1c328cf7d5c4d0c8d'
MANIFEST_HASH = '03aa668b88cb1cb32e1d26a15fb64afdf85e0af6fbb61ec89f833eaf5893a8ef'
RUN = EXECUTION / '_Coordination/AgentRuns/APP-V4-SCA003-20261002'
RUN_DAG_PREP = RUN / 'DAG_PREP'
CLOSURE = RUN_DAG_PREP / 'CLOSURE_APP_V4_SCA003_2026-10-03_1936'
CURRENCY = RUN_DAG_PREP / 'CURRENCY_APP_V4_SCA003_2026-10-03_1937'
PRIOR_RUN = EXECUTION / '_Coordination/AgentRuns/APP-V4-SCA002-20260929'
INVENTORY = '_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv'
TOOL = ROOT / 'tools/coordination/audit_dag.py'
# The departure this candidate decides: the 10 arcs SCA-V4-003 was accepted to add
# (OWNER_ITEMS Q-4; OWNER_DECISIONS DECISION-1; ARC_EFFECT §1.1, §4), found by the currency audit.
EXPECTED = {('DEL-01-04', 'DEL-01-03'): 'NR-05', ('DEL-01-04', 'DEL-01-05'): 'NR-07',
            ('DEL-01-04', 'DEL-04-02'): 'NR-08', ('DEL-01-04', 'DEL-02-03'): 'NR-09',
            ('DEL-01-04', 'DEL-02-04'): 'NR-4', ('DEL-02-03', 'DEL-01-02'): 'NR-01',
            ('DEL-03-03', 'DEL-01-02'): 'NR-02', ('DEL-02-02', 'DEL-01-02'): 'NR-04',
            ('DEL-04-03', 'DEL-02-01'): 'R2-04-03-e', ('DEL-04-03', 'DEL-02-02'): 'R20-10'}
EXPECTED_ADMITTED = {('DEL-01-04', 'DEL-01-03'), ('DEL-01-04', 'DEL-01-05'), ('DEL-02-03', 'DEL-01-02'),
                     ('DEL-03-03', 'DEL-01-02'), ('DEL-02-02', 'DEL-01-02')}
# Existing arcs whose SR-6 representative moves to a consumer-side UPSTREAM row that
# SCA-V4-003 added as a mirror (ARC_EFFECT §1.2; ledger IDs from the rows' Notes).
EXPECTED_REP_CHANGES = {('DEL-02-03', 'DEL-04-02'): ('DEP-04-02-023', 'DEP-02-03-029', 'R2-02-03-a (N-07)'),
                        ('DEL-03-02', 'DEL-04-02'): ('DEP-04-02-021', 'DEP-03-02-034', 'R-02-3 (N-05)'),
                        ('DEL-03-03', 'DEL-02-01'): ('DEP-02-01-027', 'DEP-03-03-017', 'R-03-4 (N-20)'),
                        ('DEL-03-03', 'DEL-04-02'): ('DEP-04-02-022', 'DEP-03-03-016', 'R-03-4 (N-06)'),
                        ('DEL-04-03', 'DEL-02-04'): ('DEP-02-04-012', 'DEP-04-03-036', 'R22-7-reg'),
                        ('DEL-05-01', 'DEL-01-05'): ('DEP-01-05-014', 'DEP-05-01-026', 'R-0501-4 (F0 M-5)'),
                        ('DEL-09-06', 'DEL-09-01'): ('DEP-09-01-024', 'DEP-09-06-035', 'R-0906-3')}
ABSENT = {'N-12': ('DEL-03-02', 'DEL-04-03'), 'N-B8': ('DEL-03-03', 'DEL-04-03'), 'NR-03': ('DEL-09-09', 'DEL-01-02'),
          'NR-06': ('DEL-02-04', 'DEL-01-03'), 'NR-10': ('DEL-02-04', 'DEL-02-02'),
          'E-1': ('DEL-09-09', 'DEL-09-06'), 'K-11': ('DEL-03-03', 'DEL-09-06'), 'E-5': ('DEL-09-06', 'DEL-03-04'),
          'K-7': ('DEL-09-06', 'DEL-09-07'), 'K-6': ('DEL-09-06', 'DEL-09-09'),
          'REQ-008 source wording a': ('DEL-04-01', 'DEL-01-04'), 'REQ-008 source wording b': ('DEL-04-03', 'DEL-01-04')}
R17_10_FORBIDDEN = {'DEL-01-04', 'DEL-02-02', 'DEL-02-03', 'DEL-04-02', 'DEL-04-03', 'DEL-06-01'}
PROVENANCE = ['SourceRegister', 'SourceRegisterSHA256', 'SourceRecord', 'SelectionRule']
CANDIDATE_COLS = ['CandidateReason', 'SCCRef', 'CaseRef', 'OpenQuestion']
EXCLUDE_COLS = ['SourceRegister', 'SourceRegisterSHA256', 'SourceRecord', 'DependencyID', 'FromDeliverableID', 'Direction',
                'DependencyType', 'TargetType', 'TargetDeliverableID', 'TargetRefID', 'Disposition', 'RuleOrRuling',
                'RepresentedBy', 'Notes']
NODE_COLS = ['DeliverableID', 'PackageID', 'DeliverableName', 'ExecutionPath', 'DependenciesPath', 'RegisterState',
             'TrackingMode', 'InventorySource']
SR_BASE = 'SR-1;SR-2;SR-3(all canonical types);SR-4(no cut/merge ruling);SR-5(not applied);SR-6'
COMPARE_FIELDS = ['DependencyType', 'RequiredMaturity', 'ProposedMaturity', 'Statement', 'EvidenceQuote', 'SourceRef', 'SatisfactionStatus']
DIFF_FIELDS = ['DependencyType', 'RequiredMaturity', 'ProposedMaturity', 'Statement', 'SatisfactionStatus']


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
def rowid(loc): return loc.split('#', 1)[1].split('@')[0]


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


def protected_snapshot():
    paths = [EXECUTION / '_DAG/_LATEST.md', *(EXECUTION / '_DAG').glob('DAG-00[123]/**/*'),
             *(EXECUTION / '_DAG/_Candidates').rglob('*'), *(EXECUTION / '_DAG/cases').rglob('*'),
             *EXECUTION.glob('PKG*/1_Working/DEL*/_STATUS.md'), *EXECUTION.glob('PKG*/1_Working/DEL*/Dependencies.csv'),
             *EXECUTION.glob('PKG*/1_Working/DEL*/_DEPENDENCIES.md'), *EXECUTION.glob('PKG*/1_Working/DEL*/ScopeOfWork.md'),
             *(EXECUTION / '_Evaluation').rglob('*'), *CLOSURE.rglob('*'), *CURRENCY.rglob('*')]
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
    dag3_manifest = {l.split('  ', 1)[1]: l.split('  ', 1)[0] for l in (DAG3 / 'SOURCE_MANIFEST.sha256').read_text().splitlines()}
    assert [e['path'] for e in entries] == list(dag3_manifest), 'File classes differ from DAG-003'
    changed_members = [e['path'] for e in entries if dag3_manifest[e['path']] != e['sha256']]

    # 2. Inventory from the accepted register; expected byte-equal to DAG-003's (and DAG-001/002's) node file.
    _, inventory = read(EXECUTION / INVENTORY); assert len(inventory) == 41
    ids = {x['DeliverableID'] for x in inventory}; assert len(ids) == 41
    pointer_text = (EXECUTION / '_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md').read_text()
    assert 'GROUP3-20260928T001055Z' in pointer_text, 'Accepted decomposition pointer no longer names GROUP3'
    nodes = []
    for x in sorted(inventory, key=lambda x: x['DeliverableID']):
        paths = list(EXECUTION.glob(f"{x['PackageID']}_*/1_Working/{x['DeliverableID']}_*")); assert len(paths) == 1
        p = paths[0]; h, _ = read(p / 'Dependencies.csv')
        assert h[:29] == core and len(h) == len(set(h))
        assert 'FULL_GRAPH' in (p / '_DEPENDENCIES.md').read_text()
        nodes.append(dict(zip(NODE_COLS, [x['DeliverableID'], x['PackageID'], x['Name'], str(p.relative_to(EXECUTION)),
                                          str((p / 'Dependencies.csv').relative_to(EXECUTION)), 'PRESENT', 'FULL_GRAPH', INVENTORY])))
    assert read(DAG3 / 'DeliverableNodes.csv')[1] == nodes, 'Re-derived inventory differs from DAG-003'
    (CANDIDATE / 'DeliverableNodes.csv').write_bytes((DAG3 / 'DeliverableNodes.csv').read_bytes())
    nodes_byte_equal = sha(CANDIDATE / 'DeliverableNodes.csv') == sha(DAG3 / 'DeliverableNodes.csv')

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

    # 4. SR-7 on the admissible set; SCCs must equal the closure snapshot's and DAG-003's.
    audit('admissible_audit', ['--edges', rel(EVIDENCE / 'admissible_edges.csv'), '--nodes', rel(CANDIDATE / 'DeliverableNodes.csv'),
                               '--canonical', '--json-out', rel(EVIDENCE / 'admissible_audit.json')],
          'FAIL_RAW_ACYCLIC_OBJECTIVE; CHARACTERIZED_UNRESOLVED_CYCLES')
    raw = json.loads((EVIDENCE / 'admissible_audit.json').read_text())
    _, scc_rows = read(CLOSURE / 'Evidence/scc_summary.csv')
    scc_sets = {x['SCC_ID']: set(x['Nodes'].split(';')) for x in scc_rows}
    assert {frozenset(s) for s in raw['active_graph']['sccs']} == {frozenset(s) for s in scc_sets.values()}
    assert raw['canonical_finding_count'] == 0 and raw['endpoint_issue_count'] == 0
    dag3_scc = json.loads((DAG3 / 'Evidence/SCC_Accounting.json').read_text())
    case_by_set = {frozenset(x['Members']): x['CaseRef'] for x in dag3_scc}
    assert set(case_by_set) == {frozenset(s) for s in scc_sets.values()}, 'SCC membership changed from DAG-003'
    case_map = {s: case_by_set[frozenset(ns)] for s, ns in scc_sets.items()}
    _, c3 = read(DAG3 / 'CandidateEdges.csv')
    questions = {}
    for x in c3:
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

    # 7. Non-topological inputs: DAG-001's A/B/C account, as carried by DAG-002 and DAG-003, carried forward by row identity.
    _, nt3 = read(DAG3 / 'Evidence/NonTopologicalInputs.csv')
    prior_class = {(x['SourceRegister'], x['DependencyID']): x for x in nt3}
    non_topological = []; nt_status = Counter(); nt_edited = []; nt_new = []
    for x in active:
        if x['TargetType'] == 'DELIVERABLE': continue
        p = prior_class.get((x['SourceRegister'], x['DependencyID']))
        if p:
            edited = [f for f in core if p[f] != x[f] and f != 'LastSeen']
            src_note = p['AccountSource'].split(' (carried from DAG-00')[0]
            info = (p['InputClass'], p['InputAccount'], src_note + (f" (carried from DAG-003; fields edited since: {', '.join(edited)}; re-read the live row)" if edited else ''))
            nt_status['carried_row_edited' if edited else 'carried_unchanged_except_LastSeen'] += 1
            if edited: nt_edited.append({'row': x['DependencyID'], 'fields': edited})
        else:
            info = ('NOT_CLASSIFIED_A_B_C', 'New since DAG-003. External/document input retained at its source point of need; no new human-choice classification inferred.', x['SourceRegister'])
            nt_status['new'] += 1; nt_new.append({'row': x['DependencyID'], 'TargetType': x['TargetType'], 'TargetRefID': x['TargetRefID']})
        if x['TargetType'] in ('PACKAGE', 'UNKNOWN'): assert p, f'Unclassified PACKAGE/UNKNOWN row {locator(x)}'
        non_topological.append({**x, 'InputClass': info[0], 'InputAccount': info[1], 'AccountSource': info[2]})
    live_nt = {(x['SourceRegister'], x['DependencyID']) for x in non_topological}
    retired_since = [k[1] for k in prior_class if k not in live_nt]
    nt_status['retired_since_dag003'] = len(retired_since)
    write(EVIDENCE / 'NonTopologicalInputs.csv', core + PROVENANCE + ['InputClass', 'InputAccount', 'AccountSource'], non_topological)

    # 8. Departure account against DAG-003 (read only), with the ARC_EFFECT ledger labels.
    _, e3 = read(DAG3 / 'DependencyEdges.csv')
    a3 = {arc(r): r for r in e3}; k3 = {arc(r): r for r in c3}; old = set(a3) | set(k3)
    rep_now = {arc(r): r for r in admitted + candidates}; now = set(rep_now)
    admitted_arcs = {arc(x) for x in admitted}
    added = sorted(now - old); removed = sorted(old - now)
    rows_on = defaultdict(list)
    for x in active:
        if x['TargetType'] == 'DELIVERABLE': rows_on[arc(x)].append(x)
    dep = []
    for a in added:
        r = rep_now[a]
        dep.append({'Consumer': a[0], 'Supplier': a[1], 'Label': EXPECTED.get(a, 'UNLABELLED'),
                    'Layer': 'admitted' if a in admitted_arcs else 'candidate',
                    'SCCRef': r.get('SCCRef', ''), 'CaseRef': r.get('CaseRef', ''),
                    'Representative': locator(r), 'RepresentativeDirection': r['Direction'], 'DependencyType': r['DependencyType'],
                    'RequiredMaturity': r['RequiredMaturity'], 'SatisfactionStatus': r['SatisfactionStatus'],
                    'ReverseArcPresent': 'Y' if (a[1], a[0]) in now else 'N',
                    'ReverseArcRepresentative': locator(rep_now[(a[1], a[0])]) if (a[1], a[0]) in now else '',
                    'OtherRowsOnArc': ';'.join(locator(y) for y in rows_on[a] if key(y) != key(r))})
    write(EVIDENCE / 'DepartureAccount.csv', list(dep[0]), dep)
    rep_changes = []; core_drift = Counter(); drift_rows = []
    for a in sorted(old & now):
        o = a3.get(a) or k3.get(a); n = rep_now[a]
        if (o['SourceRegister'], o['DependencyID']) != (n['SourceRegister'], n['DependencyID']):
            exp = EXPECTED_REP_CHANGES.get(a)
            rep_changes.append({'arc': f'{a[0]} -> {a[1]}', 'dag003': f"{o['SourceRegister']}#{o['DependencyID']} ({o['Direction']})",
                                'dag004': f"{locator(n)} ({n['Direction']})", 'layer': 'admitted' if a in a3 else 'candidate',
                                'ledger': exp[2] if exp else 'UNEXPECTED',
                                'reason': 'SR-6: the consumer register now has an UPSTREAM row on this arc, which ranks before the supplier DOWNSTREAM row; the former representative becomes a MIRROR'})
        else:
            diff = [f for f in core if o[f] != n[f]]
            if diff:
                core_drift[';'.join(diff)] += 1
                drift_rows.append({'arc': f'{a[0]} -> {a[1]}', 'row': n['DependencyID'], 'fields': diff})
    layer_moves = [f'{a[0]} -> {a[1]}' for a in sorted(old & now) if (a in a3) != (a in admitted_arcs)]
    rev_admitted = [(b, a) for a, b in admitted_arcs]
    advice = {}
    for a in added:
        if a not in admitted_arcs: continue
        for n in reach(a[0], rev_admitted) | {a[0]}:
            advice.setdefault(n, set()).add(f'{EXPECTED.get(a, "?")} {a[0]} -> {a[1]}')
    pending = sorted({x for a in added + removed for x in a})
    departure = {'predecessor': 'DAG-003', 'added': len(added), 'removed': len(removed), 'removed_arcs': [f'{a[0]} -> {a[1]}' for a in removed],
                 'added_admitted': sum(d['Layer'] == 'admitted' for d in dep), 'added_candidate': sum(d['Layer'] == 'candidate' for d in dep),
                 'added_arcs': [f"{d['Label']} {d['Consumer']} -> {d['Supplier']} ({d['Layer']}, {d['SCCRef'] or 'no SCC'})" for d in dep],
                 'existing_arcs_changing_layer': layer_moves, 'representative_changes': rep_changes,
                 'existing_representatives_with_changed_core_fields': dict(core_drift),
                 'existing_representatives_with_changed_core_fields_rows': drift_rows,
                 'expected_arc_set': {f'{k[0]} -> {k[1]}': v for k, v in EXPECTED.items()},
                 'accepted_arcs_not_produced': [f'{EXPECTED[a]} {a[0]} -> {a[1]}' for a in sorted(EXPECTED) if a not in now],
                 'added_outside_accepted_set': [f'{a[0]} -> {a[1]}' for a in added if a not in EXPECTED],
                 'expected_layers_hold': all((a in admitted_arcs) == (a in EXPECTED_ADMITTED) for a in EXPECTED),
                 'guard_arcs_present': sorted(k for k, a in ABSENT.items() if a in now),
                 'del_04_01_suppliers': sorted(a[1] for a in now if a[0] == 'DEL-04-01'),
                 'scc002_members_consuming_del_09_06': sorted(a[0] for a in now if a[1] == 'DEL-09-06' and a[0] in scc_sets['SCC-002']),
                 'del_09_06_consumers': sorted(a[0] for a in now if a[1] == 'DEL-09-06'),
                 'r17_10': {'DEL-01-02_reaches': sorted(reach('DEL-01-02', now)), 'DEL-01-03_reaches': sorted(reach('DEL-01-03', now)),
                            'holds': not ((reach('DEL-01-02', now) | reach('DEL-01-03', now)) & R17_10_FORBIDDEN)},
                 'reciprocal_pairs': len({frozenset(a) for a in now if (a[1], a[0]) in now}),
                 'dag_pending_resolved_by_this_candidate': pending,
                 'advice_renewed_examination_not_pending': {k: sorted(v) for k, v in sorted(advice.items()) if k not in pending},
                 'admitted_consumers_gaining_admitted_supplier': {k: sorted(v) for k, v in sorted(advice.items()) if k in pending}}
    assert not departure['accepted_arcs_not_produced'] and not departure['added_outside_accepted_set']
    assert departure['added'] == 10 and departure['removed'] == 0 and not layer_moves and departure['expected_layers_hold']
    assert not departure['guard_arcs_present'] and not departure['del_04_01_suppliers'] and not departure['scc002_members_consuming_del_09_06']
    assert departure['r17_10']['holds']
    assert {tuple(x['arc'].split(' -> ')) for x in rep_changes} == set(EXPECTED_REP_CHANGES)
    for x in rep_changes:
        o_id, n_id, _ = EXPECTED_REP_CHANGES[tuple(x['arc'].split(' -> '))]
        assert f'#{o_id} ' in x['dag003'] and f'#{n_id}@' in x['dag004'] and x['dag004'].endswith('(UPSTREAM)')
    save(EVIDENCE / 'DepartureAccount.json', departure)

    # 9. Mirror comparisons (all), flagged new or changed since DAG-003, and the carried assessments.
    _, m3 = read(DAG3 / 'Evidence/MirrorComparisons.csv')
    dag3_cmp = {frozenset((rowid(x['Representative']), rowid(x['Other']))): x for x in m3}
    _, ma3 = read(DAG3 / 'Evidence/MirrorAssessment.csv')
    dag3_assess = {frozenset((rowid(x['Representative']), rowid(x['Other']))): x for x in ma3}
    comparisons = []; assessments = []
    for pair, rep, other, disp in mirror_pairs:
        diff = [f for f in DIFF_FIELDS if rep[f] != other[f]]
        k = frozenset((rep['DependencyID'], other['DependencyID'])); prior = dag3_cmp.get(k)
        changed = []; swapped = False
        if prior:
            swapped = rowid(prior['Representative']) != rep['DependencyID']
            sides = (('Other', rep), ('Representative', other)) if swapped else (('Representative', rep), ('Other', other))
            changed = [f"{'Representative' if side == ('Other' if swapped else 'Representative') else 'Other'}.{f}"
                       for side, row in sides for f in COMPARE_FIELDS if prior[f'{side}{f}'] != row[f]]
        comparisons.append({'Consumer': pair[0], 'Supplier': pair[1], 'Representative': locator(rep), 'Other': locator(other),
                            'Disposition': disp, 'NewSinceDAG003': 'N' if prior else 'Y',
                            'RepresentativeSwappedSinceDAG003': 'Y' if swapped else 'N',
                            'FieldsChangedSinceDAG003': ';'.join(changed), 'DifferentFields': ';'.join(diff),
                            **{f'Representative{f}': rep[f] for f in COMPARE_FIELDS},
                            **{f'Other{f}': other[f] for f in COMPARE_FIELDS}})
        pa = dag3_assess.get(k)
        prior_diff = set(pa['DifferentFields'].split(';')) - {''} if pa else None
        if pa and prior_diff == set(diff):
            standing, text, assessed = pa['Standing'], pa['Assessment'], pa['AssessedIn']
        elif pa and pa['Standing'] == 'MATURITY_DIFFERENCE_ROUTED_TO_BOTH_OWNERS' and 'RequiredMaturity' not in diff:
            standing = 'MATURITY_DIFFERENCE_RECONCILED_SINCE_DAG003'
            text = (f"DAG-003 routed a RequiredMaturity difference on this arc to both owners. Both rows now state "
                    f"{rep['RequiredMaturity']} (SCA-V4-003 register UPDATE). Remaining differing fields: {';'.join(diff) or 'none'}.")
            assessed = 'DAG-004'
        elif 'RequiredMaturity' in diff:
            standing = 'MATURITY_DIFFERENCE_ROUTED_TO_BOTH_OWNERS'
            text = (f"Representative RequiredMaturity {rep['RequiredMaturity']}; counterpart {other['RequiredMaturity']}. "
                    'Routed to both register owners; read both rows. Mechanical comparison.')
            assessed = 'DAG-004'
        else:
            standing = 'NEW_MECHANICAL_COMPARISON_ONLY' if not pa else 'REASSESSMENT_DUE_FIELDS_CHANGED'
            text = ('Same RequiredMaturity on both rows; differing fields listed. Typical pattern: supplier-side DOWNSTREAM '
                    'HANDOVER/INTERFACE row against the consumer-side UPSTREAM row, statements written from each side. Not a semantic '
                    'certification; the independent review samples these. Both rows remain live obligations.')
            assessed = 'DAG-004'
        assessments.append({'Consumer': pair[0], 'Supplier': pair[1], 'Representative': locator(rep), 'Other': locator(other),
                            'DifferentFields': ';'.join(diff), 'AssessedIn': assessed,
                            'FieldsChangedSinceDAG003': ';'.join(changed), 'NewSinceDAG003': 'N' if pa else 'Y',
                            'Standing': standing, 'Assessment': text})
    write(EVIDENCE / 'MirrorComparisons.csv', list(comparisons[0]), comparisons)
    write(EVIDENCE / 'MirrorAssessment.csv', list(assessments[0]), assessments)

    # 10. SCC accounting with continuing cases.
    scc_account = []
    for s, ns in scc_sets.items():
        internal = [x for x in active if x['TargetType'] == 'DELIVERABLE' and set(arc(x)) <= ns]
        held = [x for x in candidates if x['SCCRef'] == s]
        prior = next(x for x in dag3_scc if set(x['Members']) == ns)
        scc_account.append({'SCCRef': s, 'CaseRef': case_map[s], 'Members': sorted(ns), 'MemberCount': len(ns),
                            'SourceRows': len(internal), 'HeldArcs': len(held), 'ExcludedIntraSCCRows': len(internal) - len(held),
                            'DAG003': {'SCCRef': prior['SCCRef'], 'SourceRows': prior['SourceRows'], 'HeldArcs': prior['HeldArcs']},
                            'DAG002': prior['DAG002'], 'DAG001': prior['DAG001'],
                            'CaseState': 'EVIDENCE_ACCUMULATING; BASIS_CONFIRMED; UNRESOLVED',
                            'RetainedHistory': '_DAG/cases/SCC-CASE-004' if case_map[s].endswith('SCC-CASE-002') else None})
    save(EVIDENCE / 'SCC_Accounting.json', scc_account)

    dag = json.loads((EVIDENCE / 'dag_audit.json').read_text())
    assert dag['node_row_count'] == 41 and dag['active_graph']['scc_count'] == 0 and dag['canonical_finding_count'] == 0
    assert dag['active_graph']['duplicate_edge_count'] == 0 and dag['active_graph']['bidirectional_pair_count'] == 0
    assert dag['node_row_width_issue_count'] == 0 and dag['edge_row_width_issue_count'] == 0 and dag['endpoint_issue_count'] == 0
    assert len(admitted_arcs) == len(admitted)
    assert admitted_arcs == set(a3) | EXPECTED_ADMITTED, 'Admitted arc set is not DAG-003 plus the five expected arcs'
    abs_paths = [locator(x) + f" [{placements[key(x)]}]" for x in active if re.search(r'/Users/|^/', x['TargetLocation'])]
    after = protected_snapshot()
    assert after == protected, 'A protected input changed during assembly'

    dispositions = dict(Counter(x['Disposition'] for x in exclusions))
    checks = {'result': 'PASS', 'source_revision': SOURCE, 'manifest_sha256': MANIFEST_HASH, 'manifest_entries': 130,
              'manifest_matches_source_commit': True, 'manifest_members_changed_since_dag003': len(changed_members),
              'manifest_members_changed_since_dag003_list': changed_members,
              'node_count': 41, 'nodes_byte_equal_to_dag003': nodes_byte_equal, 'packages': len({n['PackageID'] for n in nodes}),
              'total_source_rows': len(all_rows), 'active_anchors': sum(x['DependencyClass'] == 'ANCHOR' and x['Status'] == 'ACTIVE' for x in all_rows),
              'retired_rows': sum(x['Status'] == 'RETIRED' for x in all_rows), 'active_execution': len(active),
              'deliverable_target_rows': sum(len(v) for v in groups.values()), 'admissible_arcs': len(admissible),
              'admitted_rows': len(admitted), 'candidate_rows': len(candidates), 'excluded_rows': len(exclusions),
              'dispositions': dispositions, 'candidate_reasons': dict(Counter(x['CandidateReason'] for x in candidates)),
              'target_types': dict(Counter(x['TargetType'] for x in active)), 'maturity': dict(Counter(x['RequiredMaturity'] for x in active)),
              'satisfaction': dict(Counter(x['SatisfactionStatus'] for x in active)), 'edge_core_fidelity_rows': fidelity,
              'core_fields_per_row': 29, 'missing_rows': 0, 'overlapping_rows': 0, 'self_loops': 0,
              'closure_scc_membership_exact': True, 'scc_membership_equal_to_dag003': True,
              'admitted_arc_set_equal_to_dag003_plus_expected_five': True,
              'case_mapping': case_map,
              'non_topological_account': dict(nt_status), 'non_topological_new_rows': nt_new,
              'non_topological_retired_since_dag003': retired_since, 'non_topological_edited_rows': nt_edited,
              'mirror_comparisons': len(comparisons),
              'mirror_comparisons_new_since_dag003': sum(c['NewSinceDAG003'] == 'Y' for c in comparisons),
              'mirror_comparisons_with_changed_fields_since_dag003': sum(bool(c['FieldsChangedSinceDAG003']) for c in comparisons),
              'mirror_standing': dict(Counter(a['Standing'] for a in assessments)),
              'departure': {k: departure[k] for k in ('added', 'removed', 'added_admitted', 'added_candidate')},
              'representative_changes': len(rep_changes),
              'absolute_target_location_rows': abs_paths,
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

    context = [ROOT / 'AGENTS.md', ROOT / 'workflows/project-dag/WORKFLOW.md',
               ROOT / 'workflows/project-dag/resources/contract.md', ROOT / 'workflows/project-dag/resources/method.md',
               ROOT / 'workflows/project-dag/resources/graph-version.md', ROOT / 'workflows/project-dag/resources/currency.md',
               RUN / 'BRIEFS.md', RUN / 'OWNER_DECISIONS.md', RUN / 'DISPATCH.md', RUN / 'AMENDMENT_PACKET/ARC_EFFECT.md',
               RUN / 'AMENDMENT_PACKET/OWNER_ITEMS.md', RUN / 'DX/DX_SCC-CHECK.md',
               PRIOR_RUN / 'DAG_PREP/CHECKPOINT_C.md', PRIOR_RUN / 'DAG_PREP/REVIEW_PACKET.md', PRIOR_RUN / 'DISPATCH.md',
               DAG3 / 'HANDOFF_STATE.md', DAG3 / 'ACCEPTANCE_RECORD.md', DAG3 / 'GRAPH_BASIS.md', DAG3 / 'MANIFEST.sha256',
               DAG3 / 'SOURCE_MANIFEST.sha256', DAG3 / 'Evidence/assemble_graph.py', EXECUTION / '_DAG/_LATEST.md']
    save(EVIDENCE / 'Tool_Run.json', {
        'schema_version': 1, 'workflow': 'chirality-root:bundled:workflow:project-dag', 'trigger': 'SUCCESSOR',
        'run': 'APP-V4-SCA003-20261002', 'node': 'D1',
        'actor': 'Type 2 TASK executor, Claude Code Agent subagent (node D1)', 'parent': 'HELP_HUMAN integrator under a recorded WORKING_ITEMS consultation',
        'role': 'TASK', 'mechanism': 'Claude Code Agent subagent; no descendants', 'source_revision': SOURCE,
        'selected_context': [fingerprint(p) for p in context], 'assembly_script': fingerprint(Path(__file__)),
        'adapted_from': fingerprint(DAG3 / 'Evidence/assemble_graph.py'), 'python': sys.version, 'runs': runs,
        'script_command': ['python3', rel(Path(__file__))], 'finished_at': datetime.now(timezone.utc).isoformat(),
        'process_subject_distinction': 'Non-strict audits exit 0 with cyclic subjects; the strict admitted audit exits 0 and passes only its subject. Neither accepts the graph.',
        'tool_limits': 'No --markdown-out output is published (its title and front matter are DEV-001-specific). The dev001_projection JSON section is preserved but not relied on.',
        'host_vs_brief': 'The host permits wider workspace writes. The D1 brief narrows writes to the run folder DAG_PREP/ and scratch; the candidate is staged there instead of _DAG/_Candidates/. No OS-level confinement is claimed. Git is read-only; no delegation; no network.'})
    print(json.dumps({k: v for k, v in checks.items() if k not in ('manifest_members_changed_since_dag003_list', 'non_topological_edited_rows')}, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
