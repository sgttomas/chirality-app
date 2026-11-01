"""Fresh candidate/invented-input preflight. Never makes saved state or a ledger.

A passing A preflight is not B admission or permission to launch. B requires
actual ordinary setup and original A closure, followed by read-only state checks.
"""
import hashlib
import json
import os
from pathlib import Path
import stat


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        while chunk := stream.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def plain(path, directory=False):
    path = Path(path)
    require(path.is_absolute() and path.resolve() == path, 'linked/nonabsolute admission path')
    info = path.lstat()
    require(info.st_uid == os.getuid() and (stat.S_ISDIR(info.st_mode) if directory else
            stat.S_ISREG(info.st_mode) and info.st_nlink == 1), 'foreign/nonplain admission input')
    return info


def preflight_a(root, expected_plan_sha, identify):
    root = Path(root); plain(root, True)
    plan_path = root / 'witness-inputs/input-plan.json'; plain(plan_path)
    require(sha(plan_path) == expected_plan_sha, 'invented input plan changed')
    plan = json.loads(plan_path.read_bytes())
    require(plan['format'] == 'attended-invented-input-plan/v1' and plan['launch_ready'] is False
            and plan['saved_A'] is None and plan['ledger'] is None and plan['launch_limit'] == 2
            and plan['total_seconds'] == 295 and plan['minimum_remaining_before_Stop'] == 135
            and plan['Stop_confirmation_allowed'] is False and plan['PR69_active'] is False,
            'unexpected attended input scope')
    observed = json.loads((root / 'build-observation.json').read_bytes())
    require(observed['candidate_key'] == plan['candidate'] and observed['source_revision'] == plan['source_revision']
            and observed['build_identity'] == plan['build_identity'] and observed['identifier'] == plan['identifier'],
            'candidate/input identities differ')
    bundle = Path(observed['bundle']); plain(bundle, True)
    require(bundle.is_relative_to(root / 'target/release/bundle/macos'), 'bundle outside exact prepared root')
    require(identify.identity(identify.inventory(bundle)) == plan['build_identity'], 'fresh full bundle inventory differs')
    executable = Path(plan['executable']); plain(executable)
    require(executable.is_relative_to(bundle / 'Contents/MacOS') and sha(executable) == plan['executable_sha256'],
            'candidate executable differs')
    expected = {'shared_config':'shared/config.toml','shared_agents':'shared/AGENTS.md',
                'shared_skills':'shared/skills','project':'project'}
    require(plan['input_paths'] == {k:str(root/'witness-inputs'/v) for k,v in expected.items()}, 'invented paths differ')
    require(set(plan['files']) == {'shared/config.toml','shared/AGENTS.md'}, 'unexpected fixture files')
    for relative,digest in plan['files'].items():
        path=root/'witness-inputs'/relative;plain(path)
        require(sha(path)==digest, 'invented input bytes changed')
    for key in ('shared_skills','project'):
        path=Path(plan['input_paths'][key]);plain(path,True)
        require(not list(path.iterdir()), 'invented input directory not empty')
    namespaces=identify.app_data_state(plan['identifier'])
    require(not namespaces['present_at_identification'], 'candidate namespace no longer empty; preserve and reassess')
    return {'kind':'empty-candidate-A-preflight','candidate':plan['candidate'],'plan_sha256':expected_plan_sha,
            'namespace':namespaces,'B_admitted':False,'saved_A':None,'launch_authorized':False,
            'limits':'Guard/slot/current review and actual setup/closure still required; no native observation.'}


def three_row_setup_end(rows, original_session):
    require(len(rows) == 3 and [r.get('kind') for r in rows] ==
            ['session_started', 'quit_requested', 'session_ended'], 'unexpected post-setup activity')
    require(original_session and all(r.get('session') == original_session for r in rows),
            'post-setup session differs from original A')
    require(rows[0].get('previousSessionEnd') == 'none', 'new namespace has prior session')
    require(all(rows[1].get(k) == [] for k in ('liveTurns','outstandingEntries','activeDescendants')),
            'post-setup ledger names live work')
    require(rows[2].get('how') == 'quit' and rows[2].get('stopRequests') == [],
            'post-setup end is not normal empty Quit')
    return {'session':original_session,'row_count':3,'recorded_end':'quit','Stop_requests':0}


def read_setup_ledger(database, schema_path, original_session, retained):
    """Read only after actual A closure; never accept arbitrary future rows.

    retained supplies reviewed owned_plain/require_quiescent primitives. No
    supplier content is read. Current-user lsof is corroboration, not global
    exclusion; stable metadata+hash before/after is additionally required.
    """
    import sqlite3
    import jsonschema
    database=Path(database)
    retained.require_quiescent(database)
    before=retained.owned_plain(database);digest=sha(database)
    validator=jsonschema.Draft202012Validator(json.loads(Path(schema_path).read_bytes()))
    with sqlite3.connect(database.as_uri()+'?mode=ro&immutable=1',uri=True) as connection:
        connection.execute('PRAGMA query_only=ON')
        require(connection.execute("SELECT value FROM ledger_meta WHERE key='schema'").fetchone()==('1',),
                'post-setup schema differs')
        require(connection.execute('SELECT count(*) FROM ledger_entry').fetchone()==(3,),
                'post-setup row count differs')
        rows=[json.loads(raw) for raw, in connection.execute('SELECT entry FROM ledger_entry ORDER BY seq')]
        for row in rows:validator.validate(row)
    summary=three_row_setup_end(rows,original_session)
    retained.require_quiescent(database);after=retained.owned_plain(database)
    stamp=lambda s:tuple(getattr(s,k) for k in ('st_dev','st_ino','st_mode','st_uid','st_nlink','st_size','st_mtime_ns','st_ctime_ns'))
    require(stamp(before)==stamp(after) and sha(database)==digest,'post-setup ledger changed during read')
    return {**summary,'database_sha256':digest,'schema_sha256':sha(schema_path),
            'limits':'current-user descriptor corroboration, no App sidecars, stable readonly immutable snapshot; no supplier internals claim'}
