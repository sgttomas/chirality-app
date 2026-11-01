"""Explicit post-095 retained-state/v7 admission, separate from A-only, v1, v2, v3, v4, v5 and v6.

Supplier/account/project/skills contents stay opaque. Typed App-ledger history
and exact metadata admit only the recorded twenty-one-row state, not live custody.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sqlite3

HERE = Path(__file__).resolve()
V1_SOURCE = HERE.with_name('native_b_retained.py')
spec = importlib.util.spec_from_file_location('native_B_retained_v1_helpers', V1_SOURCE)
v1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v1)
require, digest = v1.require, v1.digest
VERSION = 'chirality.native-B.retained-state/v7'
CANDIDATE = v1.CANDIDATE
REQUEST_SHA = v1.REQUEST_SHA
SCHEMA_SHA = v1.SCHEMA_SHA
DATABASE_SHA = '3b1a3d6934e43143e716042b522df25789e7bae8c60fb5603a1210acb1ba2135'
ASSESSMENT_SHA = 'ebd3fb85711d54b31b19385d90314962d7823179c4e6c30fc383da283f732cdf'
ASSESSMENT_RELATIVE = Path('scratch/app-post-095-assessment-t2elat1e/assessment.json')
A_RELATIVE = Path('scratch/app-successor-native-A-irf2swd9')
SUPPLIER_NAMES = v1.SUPPLIER_NAMES | {'state_5.sqlite-shm', 'state_5.sqlite-wal'}
LIMIT = (v1.LIMIT + ' This v7 basis preserves seven recorded quit-ended sessions and actual '
         'post-095 metadata; it does not reuse or replace earlier three/six/nine/twelve/fifteen/eighteen-row bases.')


def _stamp(info):
    return tuple(getattr(info, key) for key in ('st_dev', 'st_ino', 'st_mode', 'st_uid',
                 'st_nlink', 'st_size', 'st_mtime_ns', 'st_ctime_ns'))


def summarize_rows(rows):
    """Validate the selected twenty-one-row chronology independently of source hashing."""
    require(len(rows) == 21 and [r['kind'] for r in rows] ==
            ['session_started', 'quit_requested', 'session_ended'] * 7,
            'unexpected v7 retained ledger history')
    sessions = [rows[n]['session'] for n in (0, 3, 6, 9, 12, 15, 18)]
    require(all(isinstance(s, str) and s for s in sessions) and len(set(sessions)) == 7,
            'v7 requires seven distinct recorded sessions')
    require(rows[0]['previousSessionEnd'] == 'none'
            and rows[3]['previousSessionEnd'] == 'clean'
            and rows[3].get('previousSession') == sessions[0]
            and rows[6]['previousSessionEnd'] == 'clean'
            and rows[6].get('previousSession') == sessions[1]
            and rows[9]['previousSessionEnd'] == 'clean'
            and rows[9].get('previousSession') == sessions[2]
            and rows[12]['previousSessionEnd'] == 'clean'
            and rows[12].get('previousSession') == sessions[3]
            and rows[15]['previousSessionEnd'] == 'clean'
            and rows[15].get('previousSession') == sessions[4]
            and rows[18]['previousSessionEnd'] == 'clean'
            and rows[18].get('previousSession') == sessions[5],
            'v7 prior-session linkage/end differs')
    safe = []
    for start in (0, 3, 6, 9, 12, 15, 18):
        group = rows[start:start + 3]
        require(all(row['session'] == group[0]['session'] for row in group),
                'v7 start/quit/end session binding differs')
        require(all(group[1][key] == [] for key in
                    ('liveTurns', 'outstandingEntries', 'activeDescendants')),
                'v7 retained ledger lists work')
        require(group[2]['how'] == 'quit' and group[2]['stopRequests'] == [],
                'v7 recorded quit end/stop requests differ')
        for row in group:
            item = {key: row[key] for key in ('kind', 'session', 'at')}
            if row['kind'] == 'session_started':
                item['previousSessionEnd'] = row['previousSessionEnd']
            elif row['kind'] == 'quit_requested':
                item['work_counts'] = {key: len(row[key]) for key in
                                      ('liveTurns', 'outstandingEntries', 'activeDescendants')}
            else:
                item.update(how=row['how'], stopRequests_count=len(row['stopRequests']))
            safe.append(item)
    return safe


def ledger_projection(database, schema_path):
    import jsonschema
    v1.require_quiescent(database)
    before = v1.owned_plain(database)
    require(before.st_size <= 2 * 1024 * 1024, 'v7 App ledger too large')
    v1.owned_plain(schema_path)
    require(digest(schema_path) == SCHEMA_SHA, 'v7 reviewed ledger schema changed')
    require(digest(database) == DATABASE_SHA, 'v7 retained App database changed')
    validator = jsonschema.Draft202012Validator(json.loads(Path(schema_path).read_text()))
    connection = sqlite3.connect(Path(database).as_uri() + '?mode=ro&immutable=1', uri=True)
    try:
        connection.execute('PRAGMA query_only=ON')
        require(connection.execute("SELECT value FROM ledger_meta WHERE key='schema'").fetchone() == ('1',),
                'v7 App ledger schema changed')
        require(connection.execute('SELECT count(*) FROM ledger_entry').fetchone() == (21,),
                'v7 retained App ledger row count changed')
        rows = [json.loads(raw) for raw, in connection.execute('SELECT entry FROM ledger_entry ORDER BY seq')]
        for row in rows:
            validator.validate(row)
    finally:
        connection.close()
    safe = summarize_rows(rows)
    v1.require_quiescent(database)
    require(_stamp(v1.owned_plain(database)) == _stamp(before) and digest(database) == DATABASE_SHA,
            'v7 App ledger changed during immutable read')
    return {'database_sha256': DATABASE_SHA, 'schema_sha256': SCHEMA_SHA,
            'schema_valid_rows': safe, 'counts': [['quit_requested', 7], ['session_ended', 7], ['session_started', 7]],
            'read_conditions': 'ro immutable query_only; no App WAL/SHM/journal or observed open DB descriptor before/after; stable hash/metadata',
            'limits': LIMIT}


def assessment(b, assessment_path):
    assessment_path = Path(assessment_path)
    require(assessment_path == b.setup.T3 / ASSESSMENT_RELATIVE, 'unreviewed v7 assessment source')
    v1.owned_plain(assessment_path)
    require(assessment_path.stat().st_size <= 4 * 1024 * 1024, 'v7 assessment too large')
    require(digest(assessment_path) == ASSESSMENT_SHA, 'v7 assessment changed')
    observed = json.loads(assessment_path.read_text())
    require(observed['current_database_sha256'] == DATABASE_SHA
            and observed['schema_sha256'] == SCHEMA_SHA
            and observed['saved_request_sha256'] == REQUEST_SHA,
            'v7 assessment ledger/schema/request identity differs')
    return observed


def account_layout(account):
    require({p.name for p in account.iterdir()} == SUPPLIER_NAMES | set(v1.LINKS),
            'v7 unexpected supplier/auth state addition or missing state')
    temporary = account / 'tmp'
    v1.owned_plain(temporary, True)
    require({p.name for p in temporary.iterdir()} == {'arg0'}, 'v7 supplier tmp metadata changed')
    v1.owned_plain(temporary / 'arg0', True)
    require(not list((temporary / 'arg0').iterdir()), 'v7 supplier arg0 metadata changed')


def _metadata_gate(roots, links, observed):
    current = v1.metadata(roots, links)
    require(current == observed['metadata'], 'v7 current metadata differs from exact post-095 assessment')
    return current


def observation(b, a_root, assessment_path=None):
    a_root = Path(a_root)
    require(a_root == b.setup.T3 / A_RELATIVE, 'unreviewed v7 A source')
    assessment_path = Path(assessment_path) if assessment_path is not None else b.setup.T3 / ASSESSMENT_RELATIVE
    assessed = assessment(b, assessment_path)
    paths = [a_root / name for name in ('admission.json', 'result.json', 'saved-bindings.json', 'namespace-after.json')]
    for path in paths:
        v1.owned_plain(path)
    admitted, result, bindings, after = [json.loads(path.read_text()) for path in paths]
    context = b.setup.Context.restore(admitted['context'])
    value = v1.retained_inputs(context)
    require(value['candidate_key'] == CANDIDATE and result['candidate'] == CANDIDATE
            and result['normal_setup_save_quit'] is True and result['saved'] is True
            and result['phase'] == 'A only' and result['exit_code'] == 0 and result['forced'] is False
            and not result['guard_reason'] and not result['logging_errors'] and result['error'] is None,
            'successful A basis unavailable to v7')
    data = Path(value['expected_app_data'])
    account = Path(bindings['account'])
    request = data / 'desktop-startup/request.json'
    for path in (data, account):
        v1.owned_plain(path, True)
    v1.owned_plain(request)
    require(account.parent == data / 'account-homes' and list(account.parent.iterdir()) == [account],
            'v7 account ownership boundary changed')
    require(bindings['request_path'] == str(request) and bindings['expected_inputs'] == value['native_input_paths'],
            'v7 A path binding changed')
    raw, record = b.base.validate_request(request, account, value)
    v1.saved_request_gate(raw, record, bindings)
    require({p.name for p in data.iterdir()} == {'account-homes', 'desktop-startup', 'instructions', 'records', 'runtime'},
            'v7 unexpected App namespace')
    require({p.name for p in request.parent.iterdir()} == {'request.json'}, 'v7 unexpected startup state')
    account_layout(account)
    links = v1.required_links(account, value['native_input_paths'])
    namespaces = context.namespaces(require_absent=False)
    require(set(namespaces) == {'AppData', 'WebKit', 'Caches'}, 'v7 namespace set differs')
    for name, entry in namespaces.items():
        require(entry['present'] and after[name]['present'] and entry['root'][:3] == after[name]['root'][:3],
                'v7 original namespace root changed')
    roots = {name: entry['path'] for name, entry in namespaces.items()}
    roots.update({key: value['native_input_paths'][key] for key in ('project', 'shared_skills')})
    before = _metadata_gate(roots, links, assessed)
    database = data / 'runtime/recovery.ledger.sqlite'
    require(assessed['database'] == str(database), 'v7 assessed App database path differs')
    schema = b.setup.REPO / 'execution/PKG-01/DEL-01-02/Work/recovery.app-ledger-entry.v0.3.schema.json'
    projection = ledger_projection(database, schema)
    require(projection['schema_valid_rows'] == assessed['schema_valid_rows']
            and projection['counts'] == assessed['counts'], 'v7 typed ledger differs from retained assessment')
    require(_metadata_gate(roots, links, assessed) == before, 'v7 metadata changed during admission')
    observed = {'version': VERSION, 'candidate': CANDIDATE, 'a_root': str(a_root),
                'a_files': {str(p): digest(p) for p in paths}, 'request_sha256': REQUEST_SHA,
                'assessment_path': str(assessment_path), 'assessment_sha256': digest(assessment_path),
                'ledger': projection, 'metadata': before,
                'sources': {**b.dependencies(), str(HERE): digest(HERE), str(V1_SOURCE): digest(V1_SOURCE)},
                'limits': LIMIT}
    value['expected_generation_home'] = 'app-home:' + hashlib.sha256(os.fsencode(account)).hexdigest()
    return context, value, bindings, observed


def capture(b, a_root, assessment_path, destination):
    """Write one new v7 basis; does not touch state or any earlier admission."""
    destination = Path(destination)
    require(destination.is_relative_to(b.setup.T3 / 'scratch') and destination.parent.resolve() == destination.parent,
            'v7 basis destination outside plain task scratch')
    _, _, _, observed = observation(b, a_root, assessment_path)
    b.write_once(destination, observed)
    return observed


def admit(b, basis_path):
    basis_path = Path(basis_path)
    require(basis_path.is_relative_to(b.setup.T3 / 'scratch'), 'v7 basis outside task scratch')
    v1.owned_plain(basis_path)
    require(basis_path.stat().st_size <= 4 * 1024 * 1024, 'v7 basis too large')
    basis = json.loads(basis_path.read_text())
    require(basis['version'] == VERSION, 'v7 admission version differs')
    context, value, bindings, observed = observation(b, Path(basis['a_root']), Path(basis['assessment_path']))
    require(observed == basis, 'v7 retained state/source/assessment changed since explicit basis')
    value['retained_state_admission'] = {'version': VERSION, 'path': str(basis_path), 'sha256': digest(basis_path)}
    return context, value, bindings, basis['a_files']
