"""Versioned retained-state admission; opaque supplier files are metadata only.

This does not relax saved_input's A-only predicate. A separately reviewed basis
binds actual post-B state and typed App ledger history, never supplier custody.
"""
from pathlib import Path
import hashlib
import json
import os
import sqlite3
import stat
import subprocess

VERSION = 'chirality.native-B.retained-state/v1'
REQUEST_SHA = 'ef606ee5cf6dfe3bcd9b6c2b150a89e7a2710c6289c56d180c8e6ea5dd7705de'
DATABASE_SHA = 'ff9576caf48a302d4e3b5a2a993842bee13e8ce365a51a7817365fdb522c9417'
CANDIDATE = 'fdcf608fb5-23c6c3f22f5e'
PROJECTION_SHA = '60f1b54d3242f66a7ebe9b4d658bd150c127aca800f1481e0cd7d7577e0584e2'
SCHEMA_SHA = '8a400991244e6dc389f4159bafb65f6486d4b2609ba0a92d030469c434e0a81b'
SUPPLIER_NAMES = {'.sqlite-maintenance.lock', 'goals_1.sqlite', 'installation_id',
    'logs_2.sqlite', 'logs_2.sqlite-shm', 'logs_2.sqlite-wal', 'memories_1.sqlite',
    'queue_1.sqlite', 'queue_1.sqlite-shm', 'queue_1.sqlite-wal', 'state_5.sqlite', 'tmp'}
LINKS = {'AGENTS.md': 'shared_agents', 'config.toml': 'shared_config', 'skills': 'shared_skills'}
LIMIT = ('Typed historical App ledger and exact metadata only. Empty recorded work is not '
         'proof of no unrecorded supplier state, live generation, LT23 or exhaustive settlement.')


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def owned_plain(path, directory=False):
    path = Path(path)
    require(path.is_absolute() and path.parent.resolve() == path.parent, 'linked/relative ancestry')
    info = path.lstat()
    require(info.st_uid == os.getuid() and not stat.S_ISLNK(info.st_mode), 'ownership/symlink violation')
    require(stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode), 'unexpected object type')
    if not directory:
        require(info.st_nlink == 1, 'file has additional links')
    return info


def metadata(roots, allowed_links):
    """No file content reads; no link traversal. UID included unlike old namespace view."""
    result = {}
    for name, root in sorted(roots.items()):
        root = Path(root); owned_plain(root, True)
        rows = []
        def visit(path):
            info = path.lstat(); require(info.st_uid == os.getuid(), 'foreign namespace ownership')
            row = [str(path.relative_to(root)), info.st_dev, info.st_ino, info.st_mode,
                   info.st_uid, info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns]
            if stat.S_ISLNK(info.st_mode):
                require(str(path) in allowed_links and str(path.resolve(strict=True)) == allowed_links[str(path)], 'unadmitted namespace symlink')
                row.append(os.readlink(path))
            else:
                require(stat.S_ISDIR(info.st_mode) or stat.S_ISREG(info.st_mode), 'unadmitted namespace object')
                if stat.S_ISREG(info.st_mode): require(info.st_nlink == 1, 'linked namespace file')
            rows.append(row); require(len(rows) <= 4000, 'metadata bound exceeded')
            if stat.S_ISDIR(info.st_mode):
                for child in sorted(path.iterdir()): visit(child)
        visit(root); result[name] = {'path':str(root),'rows':rows}
    return result


def require_quiescent(database):
    """No mutable SQLite sidecars and no observed open descriptor to this exact DB.

    lsof under the current user is corroboration, not an atomic global writer
    exclusion. Stable before/after hash/metadata and repeated checks are required.
    """
    owned_plain(database)
    for suffix in ('-wal', '-shm', '-journal'):
        require(not os.path.lexists(str(database)+suffix), 'App ledger sidecar present; immutable read refused')
    result = subprocess.run(['/usr/sbin/lsof', '-nP', '-F', 'p', '--', str(database)],
                            capture_output=True, text=True, timeout=3)
    require(result.returncode == 1 and not result.stdout.strip() and not result.stderr.strip(),
            'App ledger open-descriptor observation unavailable or writer/reader present')


def ledger_projection(database, schema_path):
    import jsonschema
    require_quiescent(database)
    before = owned_plain(database); require(before.st_size <= 2*1024*1024, 'App ledger too large')
    require(digest(database) == DATABASE_SHA, 'retained App database changed')
    schema = json.loads(Path(schema_path).read_text())
    validator = jsonschema.Draft202012Validator(schema)
    connection = sqlite3.connect(Path(database).as_uri()+'?mode=ro&immutable=1', uri=True)
    try:
        connection.execute('PRAGMA query_only=ON')
        require(connection.execute("SELECT value FROM ledger_meta WHERE key='schema'").fetchone() == ('1',), 'App ledger schema changed')
        require(connection.execute('SELECT count(*) FROM ledger_entry').fetchone() == (3,), 'retained App ledger row count changed')
        rows = [json.loads(raw) for raw, in connection.execute('SELECT entry FROM ledger_entry ORDER BY seq')]
        for row in rows: validator.validate(row)
    finally:
        connection.close()
    require([r['kind'] for r in rows] == ['session_started','quit_requested','session_ended'], 'unexpected retained ledger history')
    require(len({r['session'] for r in rows}) == 1, 'retained ledger sessions differ')
    require(all(rows[1][k] == [] for k in ('liveTurns','outstandingEntries','activeDescendants')),
            'retained ledger lists work')
    require(rows[2]['how'] == 'quit' and rows[2]['stopRequests'] == [], 'retained end facts differ')
    require_quiescent(database)
    require(tuple(getattr(owned_plain(database), k) for k in ('st_dev','st_ino','st_mode','st_uid','st_nlink','st_size','st_mtime_ns','st_ctime_ns')) == tuple(getattr(before,k) for k in ('st_dev','st_ino','st_mode','st_uid','st_nlink','st_size','st_mtime_ns','st_ctime_ns')) and digest(database) == DATABASE_SHA, 'App ledger changed during immutable read')
    return {'database_sha256':DATABASE_SHA,'schema_sha256':digest(schema_path),
            'session':rows[0]['session'],'kinds':[r['kind'] for r in rows],
            'times':[r['at'] for r in rows],'recorded_end':'quit','listed_work_counts':[0,0,0],
            'stop_requests_count':0,'read_mode':'ro immutable query_only; no App WAL/SHM/journal or observed open DB descriptor before/after',
            'limits':LIMIT}


def retained_inputs(context):
    # Explicit post-B input semantics. Context.inputs remains the A-only path.
    for name, expected in context.file_digests.items():
        owned_plain(Path(name)); require(digest(name)==expected, 'candidate input source changed')
    value=json.loads(context.inputs_path.read_text()); identified=context.identified
    bundle=context.build_root/'target/debug/bundle/macos'/identified['bundle']['name']
    executable=bundle/identified['bundle']['executable']['path']
    require(value['candidate_key']==identified['candidate_key']==CANDIDATE
            and value['bundle_identifier']==context.identifier and value['bundle']==str(bundle)
            and value['executable']==str(executable)
            and value['executable_sha256']==identified['bundle']['executable']['sha256'], 'retained candidate manifest changed')
    require(value['expected_app_data']==str(Path.home()/'Library/Application Support'/context.identifier), 'retained namespace path changed')
    fixture=context.inputs_path.parent
    expected={'shared_config':fixture/'shared/config.toml','shared_agents':fixture/'shared/AGENTS.md',
              'shared_skills':fixture/'shared/skills','project':fixture/'project'}
    require(value['native_input_paths']=={k:str(v) for k,v in expected.items()}, 'retained input paths changed')
    for key,path in expected.items(): owned_plain(path,key in ('shared_skills','project'))
    for name, expected_sha in value['files'].items():
        path=fixture/name
        require(path.is_relative_to(fixture) and '..' not in Path(name).parts, 'fixture path escapes')
        owned_plain(path);require(digest(path)==expected_sha,'original fixture file changed')
    require({p.name for p in expected['project'].iterdir()}=={'.chirality'}, 'unexplained project entries')
    require({str(p.relative_to(expected['project'])) for p in expected['project'].rglob('*')}=={'.chirality','.chirality/project.json'}, 'unexplained project metadata')
    require({p.name for p in expected['shared_skills'].iterdir()}=={'.system'}, 'unexplained shared-skills entries')
    environment={'HOME':str(Path.home()),'PATH':str(bundle/'Contents/Resources/codex/codex-path')+':/usr/bin:/bin:/usr/sbin:/sbin',
                 'LANG':'en_US.UTF-8','CODEX_HOME':str(fixture/'fallback-codex-home'),'TMPDIR':str(fixture/'tmp')}
    require(value['environment']==environment,'retained launch environment changed')
    return value


def saved_request_gate(raw, record, bindings):
    require(hashlib.sha256(raw).hexdigest()==REQUEST_SHA==bindings['request_sha256']
            and record==bindings['request'], 'exact saved A request changed')


def account_layout(account):
    require({p.name for p in account.iterdir()}==SUPPLIER_NAMES|set(LINKS), 'unexpected supplier/auth state addition or missing state')
    require({str(p.relative_to(account/'tmp')) for p in (account/'tmp').rglob('*')}=={'arg0'}, 'supplier tmp metadata changed')


def required_links(account, paths):
    links={str(account/name):str(Path(paths[key])) for name,key in LINKS.items()}
    for path,target in links.items():
        info=Path(path).lstat()
        require(stat.S_ISLNK(info.st_mode) and info.st_uid==os.getuid()
                and str(Path(path).resolve(strict=True))==target, 'required account link changed')
    return links


def observation(b, a_root, projection_path):
    """Versioned alternative; unchanged A-only saved_input() is not called/relaxed."""
    require(a_root == b.setup.T3/'scratch/app-successor-native-A-irf2swd9', 'unreviewed A source')
    require(Path(projection_path) == b.setup.T3/'scratch/app-native-next-admission-35viga7p/retained-runtime-projection.json', 'unreviewed projection source')
    owned_plain(projection_path); require(digest(projection_path)==PROJECTION_SHA, 'historical projection changed')
    paths = [a_root/name for name in ('admission.json','result.json','saved-bindings.json','namespace-after.json')]
    for path in paths: owned_plain(path)
    admitted, result, bindings, after = [json.loads(p.read_text()) for p in paths]
    context = b.setup.Context.restore(admitted['context']); value = retained_inputs(context)
    require(value['candidate_key'] == CANDIDATE, 'retained candidate differs')
    require(result['candidate'] == CANDIDATE and result['normal_setup_save_quit'] is True
            and result['saved'] is True and result['phase'] == 'A only' and result['exit_code']==0
            and result['forced'] is False and not result['guard_reason'] and not result['logging_errors']
            and result['error'] is None, 'successful A basis unavailable')
    data=Path(value['expected_app_data']);account=Path(bindings['account']);request=data/'desktop-startup/request.json'
    owned_plain(data,True);owned_plain(account,True);owned_plain(request)
    require(account.parent == data/'account-homes' and list(account.parent.iterdir())==[account], 'account ownership boundary changed')
    require(bindings['request_path']==str(request) and bindings['expected_inputs']==value['native_input_paths'], 'A path binding changed')
    raw, record=b.base.validate_request(request,account,value)
    saved_request_gate(raw,record,bindings)
    require({p.name for p in data.iterdir()}=={'account-homes','desktop-startup','instructions','records','runtime'}, 'unexpected App namespace')
    require({p.name for p in request.parent.iterdir()}=={'request.json'}, 'unexpected startup state')
    account_layout(account)  # Exact observed names only; contents stay opaque.
    links=required_links(account,value['native_input_paths'])
    namespaces=context.namespaces(require_absent=False)
    for name, entry in namespaces.items():
        require(entry['present'] and after[name]['present'] and entry['root'][:3]==after[name]['root'][:3], 'original namespace root changed')
    roots={name:entry['path'] for name,entry in namespaces.items()}
    roots.update({key:value['native_input_paths'][key] for key in ('project','shared_skills')})
    before=metadata(roots,links)
    schema=b.setup.REPO/'execution/PKG-01/DEL-01-02/Work/recovery.app-ledger-entry.v0.3.schema.json'
    require(digest(schema)==SCHEMA_SHA, 'reviewed ledger schema changed')
    projection=ledger_projection(data/'runtime/recovery.ledger.sqlite',schema)
    owned_plain(projection_path); historical=json.loads(Path(projection_path).read_text())
    require(historical['database_sha256']==DATABASE_SHA and historical['saved_request_sha256']==REQUEST_SHA
            and historical['rows_schema_valid'] is True and historical['session']==projection['session'], 'projection provenance differs')
    require(metadata(roots,links)==before, 'namespace metadata changed during admission')
    result={'version':VERSION,'candidate':CANDIDATE,'a_root':str(a_root),
            'a_files':{str(p):digest(p) for p in paths},'request_sha256':REQUEST_SHA,
            'projection_path':str(projection_path),'projection_sha256':digest(projection_path),
            'ledger':projection,'metadata':before,'sources':b.dependencies(),'limits':LIMIT}
    value['expected_generation_home']='app-home:'+hashlib.sha256(os.fsencode(account)).hexdigest()
    return context,value,bindings,result


def capture(b, a_root, projection_path, destination):
    context,value,bindings,observed=observation(b,a_root,projection_path)
    b.write_once(destination,observed)
    return observed


def admit(b, basis_path):
    require(Path(basis_path).is_relative_to(b.setup.T3/'scratch'), 'basis outside task scratch')
    owned_plain(basis_path);require(Path(basis_path).stat().st_size<=4*1024*1024,'retained basis too large')
    basis=json.loads(Path(basis_path).read_text());require(basis['version']==VERSION,'retained admission version differs')
    context,value,bindings,observed=observation(b,Path(basis['a_root']),Path(basis['projection_path']))
    require(observed==basis,'retained state/source/projection changed since explicit basis')
    value['retained_state_admission']={'version':VERSION,'path':str(basis_path),'sha256':digest(basis_path)}
    return context,value,bindings,basis['a_files']
