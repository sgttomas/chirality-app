"""Invented files/SQLite only; no actual candidate, supplier or native execution."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sqlite3
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('retained_v4_tests', Path(__file__).with_name('native_b_retained_v4.py'))
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


def rows():
    result = []
    for index, session in enumerate(('fixture-session-one', 'fixture-session-two', 'fixture-session-three', 'fixture-session-four')):
        start = {'kind': 'session_started', 'session': session, 'at': '2026-10-31T00:00:00Z',
                 'previousSessionEnd': 'none' if not index else 'clean'}
        if index:
            start['previousSession'] = ('fixture-session-one', 'fixture-session-two', 'fixture-session-three')[index-1]
        result.extend([start, {'kind': 'quit_requested', 'session': session, 'at': '2026-10-31T00:00:01Z',
                              'liveTurns': [], 'outstandingEntries': [], 'activeDescendants': []},
                       {'kind': 'session_ended', 'session': session, 'at': '2026-10-31T00:00:02Z',
                        'how': 'quit', 'stopRequests': []}])
    return result


def database(path, entries):
    connection = sqlite3.connect(path)
    connection.executescript('CREATE TABLE ledger_meta(key,value); INSERT INTO ledger_meta VALUES ("schema","1"); CREATE TABLE ledger_entry(seq INTEGER PRIMARY KEY,entry TEXT);')
    connection.executemany('INSERT INTO ledger_entry VALUES (?,?)', [(i, json.dumps(row)) for i, row in enumerate(entries)])
    connection.commit()
    connection.close()


class V4(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='retained-v4-test-', dir='/Users/ryan/dev/chirality-t3/scratch')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.db = self.root / 'ledger.sqlite'
        self.rows = rows()
        database(self.db, self.rows)
        self.schema = self.root / 'schema.json'
        self.schema.write_text('{"type":"object"}')
        self.addCleanup(patch.stopall)
        patch.object(r, 'DATABASE_SHA', r.digest(self.db)).start()
        patch.object(r, 'SCHEMA_SHA', r.digest(self.schema)).start()
        self.lsof = patch.object(r.v1.subprocess, 'run', return_value=SimpleNamespace(returncode=1, stdout='', stderr='')).start()
        self.b = SimpleNamespace(setup=SimpleNamespace(T3=self.root))

    def test_exact_twelve_rows_readonly_and_v1_constants_unchanged(self):
        old = (r.v1.VERSION, r.v1.DATABASE_SHA, r.v1.PROJECTION_SHA, r.v1.SCHEMA_SHA)
        before = r.digest(self.db)
        observed = r.ledger_projection(self.db, self.schema)
        self.assertEqual(observed['schema_valid_rows'], r.summarize_rows(self.rows))
        self.assertEqual(observed['counts'], [['quit_requested', 4], ['session_ended', 4], ['session_started', 4]])
        self.assertEqual(r.digest(self.db), before)
        self.assertEqual(self.lsof.call_count, 2)
        self.assertEqual(old, (r.v1.VERSION, r.v1.DATABASE_SHA, r.v1.PROJECTION_SHA, r.v1.SCHEMA_SHA))

    def test_ledger_fact_mutations_refuse(self):
        for mutate in [lambda v: v[10].update(liveTurns=['invented']), lambda v: v[11].update(how='system-terminated'), lambda v: v[9].update(previousSession='foreign'), lambda v: v[7].update(outstandingEntries=['invented']),
                       lambda v: v[8].update(how='system-terminated'),
                       lambda v: v[8].update(stopRequests=['invented']),
                       lambda v: v[6].update(previousSession='foreign'),
                       lambda v: v.append(copy.deepcopy(v[-1])), lambda v: v[4].update(liveTurns=['invented']),
                       lambda v: v[5].update(stopRequests=['invented']),
                       lambda v: v[5].update(how='system-terminated'),
                       lambda v: v[3].update(previousSessionEnd='ended-without-record'),
                       lambda v: v[3].update(previousSession='foreign'),
                       lambda v: v[4].update(session='foreign'),
                       lambda v: v[3].update(session=v[0]['session'])]:
            changed = copy.deepcopy(self.rows)
            mutate(changed)
            with self.assertRaises(RuntimeError):
                r.summarize_rows(changed)
        with self.assertRaisesRegex(RuntimeError, 'history'):
            r.summarize_rows(self.rows[:3])

    def test_row_count_database_and_schema_drift_refuse(self):
        changed = self.root / 'changed.sqlite'
        database(changed, self.rows[:3])
        with self.assertRaisesRegex(RuntimeError, 'database changed'):
            r.ledger_projection(changed, self.schema)
        with patch.object(r, 'DATABASE_SHA', r.digest(changed)):
            with self.assertRaisesRegex(RuntimeError, 'row count'):
                r.ledger_projection(changed, self.schema)
        self.schema.write_text('{}')
        with self.assertRaisesRegex(RuntimeError, 'schema changed'):
            r.ledger_projection(self.db, self.schema)

    def test_sidecars_observed_user_and_unavailable_query_refuse(self):
        for suffix in ('-wal', '-shm', '-journal'):
            path = Path(str(self.db) + suffix)
            path.touch()
            with self.assertRaisesRegex(RuntimeError, 'sidecar'):
                r.ledger_projection(self.db, self.schema)
            path.unlink()
        for outcome in (SimpleNamespace(returncode=0, stdout='p123', stderr=''),
                        SimpleNamespace(returncode=1, stdout='', stderr='not observable')):
            self.lsof.return_value = outcome
            with self.assertRaisesRegex(RuntimeError, 'descriptor'):
                r.ledger_projection(self.db, self.schema)
        self.lsof.side_effect = r.v1.subprocess.TimeoutExpired('lsof', 3)
        with self.assertRaises(r.v1.subprocess.TimeoutExpired):
            r.ledger_projection(self.db, self.schema)

    def test_after_read_sidecar_or_changed_metadata_refuses(self):
        self.lsof.side_effect = [SimpleNamespace(returncode=1, stdout='', stderr=''),
                                SimpleNamespace(returncode=0, stdout='p123', stderr='')]
        with self.assertRaisesRegex(RuntimeError, 'descriptor'):
            r.ledger_projection(self.db, self.schema)
        self.lsof.side_effect = None
        original = r.v1.require_quiescent
        calls = []
        def change_after(path):
            original(path)
            calls.append(1)
            if len(calls) == 2:
                info = path.stat()
                os.utime(path, ns=(info.st_atime_ns, info.st_mtime_ns + 1000000))
        with patch.object(r.v1, 'require_quiescent', side_effect=change_after):
            with self.assertRaisesRegex(RuntimeError, 'changed during'):
                r.ledger_projection(self.db, self.schema)

    def test_explicit_assessment_path_hash_and_v4_identity(self):
        with self.assertRaisesRegex(RuntimeError, 'assessment source'):
            r.assessment(self.b, self.schema)
        assessment = self.root / r.ASSESSMENT_RELATIVE
        assessment.parent.mkdir(parents=True)
        assessment.write_text('{}')
        with self.assertRaisesRegex(RuntimeError, 'assessment changed'):
            r.assessment(self.b, assessment)
        basis = self.root / 'scratch/basis.json'
        basis.write_text(json.dumps({'version': r.v1.VERSION}))
        with self.assertRaisesRegex(RuntimeError, 'version'):
            r.admit(self.b, basis)

    def test_only_exact_supplier_names_and_arg0_are_allowed(self):
        account = self.root / 'account'
        account.mkdir()
        for name in r.SUPPLIER_NAMES | set(r.v1.LINKS):
            if name == 'tmp':
                (account / name / 'arg0').mkdir(parents=True)
            else:
                (account / name).touch()
        r.account_layout(account)
        for extra in ('auth.json', 'unexpected.sqlite'):
            path = account / extra
            path.touch()
            with self.assertRaisesRegex(RuntimeError, 'supplier/auth'):
                r.account_layout(account)
            path.unlink()
        (account / 'tmp/extra').touch()
        with self.assertRaisesRegex(RuntimeError, 'tmp metadata'):
            r.account_layout(account)
        (account / 'tmp/extra').unlink()
        (account / 'tmp/arg0').rmdir()
        (account / 'tmp/arg0').symlink_to(self.root)
        with self.assertRaisesRegex(RuntimeError, 'symlink'):
            r.account_layout(account)

    def test_metadata_is_exact_and_never_opens_opaque_file(self):
        root = self.root / 'opaque'
        root.mkdir()
        file = root / 'supplier.sqlite'
        file.write_bytes(b'opaque invented contents')
        roots = {'AppData': str(root)}
        observed = {'metadata': r.v1.metadata(roots, {})}
        with patch.object(Path, 'read_bytes', side_effect=AssertionError('contents not allowed')), \
             patch.object(Path, 'read_text', side_effect=AssertionError('contents not allowed')):
            self.assertEqual(r._metadata_gate(roots, {}, observed), observed['metadata'])
        file.write_bytes(b'changed length')
        with self.assertRaisesRegex(RuntimeError, 'current metadata'):
            r._metadata_gate(roots, {}, observed)
        link = root / 'foreign'
        link.symlink_to('/tmp')
        with self.assertRaisesRegex(RuntimeError, 'symlink'):
            r._metadata_gate(roots, {}, observed)

    def test_admit_requires_exact_source_assessment_and_state_then_binds_v4(self):
        basis_path = self.root / 'scratch/basis.json'
        basis_path.parent.mkdir()
        basis = {'version': r.VERSION, 'a_root': str(self.root), 'assessment_path': str(self.schema),
                 'a_files': {'invented': 'hash'}, 'sources': {'source': 'hash'}}
        basis_path.write_text(json.dumps(basis))
        with patch.object(r, 'observation', return_value=('context', {}, 'bindings', basis)):
            context, value, bindings, files = r.admit(self.b, basis_path)
        self.assertEqual(value['retained_state_admission'], {'version': r.VERSION, 'path': str(basis_path), 'sha256': r.digest(basis_path)})
        for key in ('sources', 'a_files'):
            changed = {**basis, key: {'changed': 'hash'}}
            with patch.object(r, 'observation', return_value=('context', {}, 'bindings', changed)):
                with self.assertRaisesRegex(RuntimeError, 'state/source/assessment'):
                    r.admit(self.b, basis_path)

    def test_capture_refuses_overwrite_and_unreviewed_a_without_state_reads(self):
        destination = self.root / 'scratch/basis.json'
        destination.parent.mkdir()
        def write_once(path, value):
            with path.open('x') as stream:
                json.dump(value, stream)
        self.b.write_once = write_once
        with patch.object(r, 'observation', return_value=(None, None, None, {'version': r.VERSION})):
            r.capture(self.b, self.root, self.schema, destination)
            with self.assertRaises(FileExistsError):
                r.capture(self.b, self.root, self.schema, destination)
        with self.assertRaisesRegex(RuntimeError, 'A source'):
            r.observation(self.b, self.root, self.schema)

    def test_full_observation_binds_exact_assessment_and_refuses_state_drift(self):
        fake_t3 = self.root / 't3'
        a_root = fake_t3 / r.A_RELATIVE
        a_root.mkdir(parents=True)
        app = self.root / 'app-data'
        for name in ('account-homes', 'desktop-startup', 'instructions', 'records', 'runtime'):
            (app / name).mkdir(parents=True)
        account = app / 'account-homes/fixture-account'
        account.mkdir()
        shared = self.root / 'shared'
        shared.mkdir()
        native_paths = {}
        for name, key in r.v1.LINKS.items():
            target = shared / name
            if name == 'skills':
                target.mkdir()
            else:
                target.write_text('invented original fixture')
            native_paths[key] = str(target)
            (account / name).symlink_to(target)
        project = self.root / 'project'
        project.mkdir()
        native_paths['project'] = str(project)
        for name in r.SUPPLIER_NAMES:
            if name == 'tmp':
                (account / name / 'arg0').mkdir(parents=True)
            else:
                (account / name).write_bytes(b'opaque fixture')
        request = app / 'desktop-startup/request.json'
        request.write_text('{"invented":"saved request"}')
        db = app / 'runtime/recovery.ledger.sqlite'
        db.write_bytes(self.db.read_bytes())
        repo = self.root / 'repo'
        schema = repo / 'execution/PKG-01/DEL-01-02/Work/recovery.app-ledger-entry.v0.3.schema.json'
        schema.parent.mkdir(parents=True)
        schema.write_bytes(self.schema.read_bytes())
        roots = {'AppData': str(app), 'WebKit': str(self.root / 'webkit'), 'Caches': str(self.root / 'caches')}
        for key in ('WebKit', 'Caches'):
            Path(roots[key]).mkdir()
        def namespaces(require_absent=False):
            return {key: {'path': path, 'present': True, 'root': [Path(path).stat().st_dev, Path(path).stat().st_ino, Path(path).stat().st_mode]}
                    for key, path in roots.items()}
        value = {'candidate_key': r.CANDIDATE, 'expected_app_data': str(app), 'native_input_paths': native_paths}
        bindings = {'account': str(account), 'request_path': str(request), 'expected_inputs': native_paths,
                    'request_sha256': r.REQUEST_SHA, 'request': {'invented': 'saved request'}}
        result = {'candidate': r.CANDIDATE, 'normal_setup_save_quit': True, 'saved': True, 'phase': 'A only',
                  'exit_code': 0, 'forced': False, 'guard_reason': None, 'logging_errors': [], 'error': None}
        for name, content in [('admission.json', {'context': 'fixture'}), ('result.json', result),
                              ('saved-bindings.json', bindings), ('namespace-after.json', namespaces())]:
            (a_root / name).write_text(json.dumps(content))
        links = r.v1.required_links(account, native_paths)
        all_roots = {**roots, 'project': str(project), 'shared_skills': native_paths['shared_skills']}
        observed = {'current_database_sha256': r.DATABASE_SHA, 'schema_sha256': r.SCHEMA_SHA,
                    'saved_request_sha256': r.REQUEST_SHA, 'database': str(db),
                    'metadata': r.v1.metadata(all_roots, links), 'schema_valid_rows': r.summarize_rows(self.rows),
                    'counts': [['quit_requested', 4], ['session_ended', 4], ['session_started', 4]]}
        assessment = fake_t3 / r.ASSESSMENT_RELATIVE
        assessment.parent.mkdir(parents=True)
        assessment.write_text(json.dumps(observed))
        context = SimpleNamespace(namespaces=namespaces)
        b = SimpleNamespace(setup=SimpleNamespace(T3=fake_t3, REPO=repo,
                            Context=SimpleNamespace(restore=lambda descriptor: context)),
                            base=SimpleNamespace(validate_request=lambda *args: (request.read_bytes(), bindings['request'])),
                            dependencies=lambda: {'fixture-controller': 'source-hash'})
        with patch.object(r, 'ASSESSMENT_SHA', r.digest(assessment)), \
             patch.object(r.v1, 'retained_inputs', return_value=value), \
             patch.object(r.v1, 'saved_request_gate') as saved_gate:
            result = r.observation(b, a_root, assessment)
            self.assertEqual(result[3]['version'], r.VERSION)
            self.assertEqual(result[3]['metadata'], observed['metadata'])
            self.assertIn(str(r.HERE), result[3]['sources'])
            saved_gate.assert_called_once_with(request.read_bytes(), bindings['request'], bindings)
            # Known filename with unexplained metadata drift must fail before
            # another database read; no new snapshot silently accepts it.
            (account / 'installation_id').write_bytes(b'changed opaque length')
            with patch.object(r, 'ledger_projection', side_effect=AssertionError('must refuse metadata first')):
                with self.assertRaisesRegex(RuntimeError, 'current metadata'):
                    r.observation(b, a_root, assessment)
            # A regular file cannot substitute for a required original link.
            (account / 'AGENTS.md').unlink()
            (account / 'AGENTS.md').write_text('replacement')
            with self.assertRaisesRegex(RuntimeError, 'required account link'):
                r.observation(b, a_root, assessment)


if __name__ == '__main__':
    unittest.main()
