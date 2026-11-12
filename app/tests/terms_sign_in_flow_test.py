"""Candidate sign-in flow against the flow the retained terms record covers (DEL-01-06 AC-004).

Each test builds an invented Git repository in a temporary folder; the retained record and the
0.160.0 schema are copied in read-only. No test writes a reading into this repository."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('terms_sign_in_flow', ROOT / 'app/packaging/terms/flow.py')
flow = importlib.util.module_from_spec(spec); spec.loader.exec_module(flow)

ENV = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull, GIT_CONFIG_NOSYSTEM='1')
HOSTING = 'pub const DECLARED_PIN: &str = "9.9.9";\nfn start(){ self.request_begin_scoped("account/login/start",json!({"type":kind})); }\n'


class SignInFlow(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.repo = Path(temp.name).resolve() / 'candidate'
        files = {
            'app/src-tauri/src/hosting.rs': HOSTING,
            'app/src-tauri/src/nested/auth_rpc.rs': 'fn guard(){ if method == "account/login/start" {} }\n',
            'app/src/login.ts': 'invoke("oauth_start"); // LoginAccount view\n',
            'app/packaging/other/included.rs': 'const X: &str = "account/login/start";\n',
            'app/.gitignore': 'build-output/\n',
        }
        for path, text in files.items():
            (self.repo / path).parent.mkdir(parents=True, exist_ok=True)
            (self.repo / path).write_text(text)
        for relative in (flow.RETAINED_RECORD, flow.SCHEMA.format(pin='0.160.0'), flow.READINGS_DIR + 'README.md'):
            (self.repo / relative).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, self.repo / relative)
        self.schema = self.repo / flow.SCHEMA.format(pin='9.9.9')
        self.schema.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / flow.SCHEMA.format(pin='0.160.0'), self.schema)
        self.git('init', '-q', '-b', 'main')
        self.commit('invented candidate')

    def git(self, *args):
        return subprocess.run(['git', '-C', str(self.repo), '-c', 'user.name=Invented', '-c', 'user.email=invented@example.invalid',
                               '-c', 'commit.gpgsign=false', *args], check=True, capture_output=True, env=ENV).stdout.decode().strip()

    def commit(self, message='change'):
        self.git('add', '-A'); self.git('commit', '-q', '--allow-empty', '-m', message)
        return self.git('rev-parse', 'HEAD')

    def head(self):
        return self.git('rev-parse', 'HEAD')

    def reading_value(self, **changes):
        commit = self.head()
        value = {'format': flow.READING_FORMAT, 'commit': commit,
                 'bound_set_sha256': flow.bound_set(flow.Repository(self.repo).entries(commit)), 'pin': '9.9.9',
                 'reader': {'name': 'Invented Reviewer', 'role': 'independent reviewer'}, 'date': '2026-11-12',
                 'how_read': 'Read the invented commit; searched for account/login and read each sender.',
                 'account_sign_in_types': ['chatgpt', 'chatgptDeviceCode'],
                 'separate_credential_logins': [{'type': 'apiKey', 'home': 'invented key home',
                                                 'sent_from': [{'file': 'app/src-tauri/src/hosting.rs', 'line': 2}]}],
                 'relied_on': [{'file': 'app/src-tauri/src/hosting.rs', 'line': 2},
                               {'file': 'app/src-tauri/src/nested/auth_rpc.rs', 'line': 1}]}
        value.update(changes)
        return value

    def add_reading(self, name='invented.json', raw=None, **changes):
        path = self.repo / flow.READINGS_DIR / name
        path.write_text(raw if raw is not None else json.dumps(self.reading_value(**changes)))
        return self.commit('reading')

    def run_flow(self, revision='HEAD'):
        return flow.compare(self.repo, revision)

    def assertConditions(self, expected, revision='HEAD'):
        report = self.run_flow(revision)
        self.assertEqual(report['status'], 'unresolved' if expected else 'unchanged', report)
        self.assertEqual(report['conditions_failed'], expected, report)
        return report

    def test_no_reading_is_unresolved(self):
        report = self.assertConditions(['no reading for this bound set'])
        self.assertEqual(report['commit'], self.head())
        self.assertTrue(report['limits'] and report['bound_set_form'])
        self.assertEqual(flow.main(['--repository', str(self.repo)]), 1)

    def test_matching_reading_is_unchanged(self):
        read_against = self.head()
        self.add_reading()
        report = self.assertConditions([])
        self.assertEqual(report['readings']['reading_commit'], read_against)
        self.assertNotEqual(report['commit'], read_against)   # committing the reading leaves the bound set alone
        self.assertEqual(flow.main(['--repository', str(self.repo)]), 0)

    def test_any_tracked_change_under_app_outside_readings_makes_the_reading_stale(self):
        self.add_reading()
        for path in ('app/packaging/other/included.rs', 'app/src-tauri/src/nested/auth_rpc.rs', 'app/new-file.txt'):
            with self.subTest(path=path):
                target = self.repo / path
                original = target.read_bytes() if target.exists() else None
                target.write_bytes((original or b'') + b' ')
                self.commit()
                self.assertConditions(['reading made for another bound set or pin'])
                target.write_bytes(original) if original is not None else target.unlink()
                self.commit()
        self.assertConditions([])
        (self.repo / 'outside-app.txt').write_text('not bound'); self.commit()
        self.assertConditions([])

    def test_working_tree_differing_from_the_commit_is_refused(self):
        self.add_reading()
        cases = {
            'modified': lambda: (self.repo / 'app/src/login.ts').write_text('changed\n'),
            'untracked': lambda: (self.repo / 'app/src/new.ts').write_text('new\n'),
            'staged': lambda: ((self.repo / 'app/src/login.ts').write_text('staged\n'), self.git('add', 'app/src/login.ts')),
            'untracked reading': lambda: (self.repo / flow.READINGS_DIR / 'late.json').write_text('{}'),
        }
        for label, act in cases.items():
            with self.subTest(case=label):
                act()
                self.assertConditions(['working tree differs from the commit under app/'])
                self.git('reset', '-q', '--hard'); self.git('clean', '-qfd')
        (self.repo / 'app/build-output').mkdir(); (self.repo / 'app/build-output/x.o').write_text('ignored')
        self.assertConditions([])

    def test_named_revision_must_match_the_working_tree(self):
        first = self.head()
        self.add_reading()
        self.assertConditions(['working tree differs from the commit under app/'], revision=first)

    def test_without_a_checkout_of_the_revision_it_is_unresolved(self):
        empty = self.repo.parent / 'not-a-checkout'; empty.mkdir()
        report = flow.compare(empty)
        self.assertEqual((report['status'], report['conditions_failed']), ('unresolved', ['no git checkout of the revision']))
        self.assertEqual(self.run_flow('0' * 40)['conditions_failed'], ['no git checkout of the revision'])

    def test_malformed_readings_are_unresolved(self):
        older = self.head()
        (self.repo / 'app/src/login.ts').write_text('moved on\n'); self.commit()
        good = json.dumps(self.reading_value())
        cases = {
            'duplicated field': good[:-1] + ', "pin": "9.9.9"}',
            'duplicated nested field': good.replace('"role": "independent reviewer"', '"role": "independent reviewer", "role": "owner"'),
            'missing how_read': self.reading_value(), 'extra field': self.reading_value(note='x'),
            'role outside the set': self.reading_value(reader={'name': 'Someone', 'role': 'author'}),
            'tool as reader': self.reading_value(reader={'name': 'flow.py', 'role': 'independent reviewer'}),
            'empty name': self.reading_value(reader={'name': ' ', 'role': 'owner'}),
            'old independence flag': self.reading_value(reader={'name': 'X', 'role': 'owner', 'did_not_write_the_sign_in_change': True}),
            'unknown commit': self.reading_value(commit='1' * 40),
            'commit with another bound set': self.reading_value(commit=older),
            'file not in bound set': self.reading_value(relied_on=[{'file': 'app/absent.rs', 'line': 1}]),
            'reading cited as a place': self.reading_value(relied_on=[{'file': flow.READINGS_DIR + 'README.md', 'line': 1}]),
            'line beyond end': self.reading_value(relied_on=[{'file': 'app/src/login.ts', 'line': 9}]),
            'short how_read': self.reading_value(how_read='read it'),
            'bad date': self.reading_value(date='2026-13-40'),
            'truncated': '{"format":',
        }
        cases['missing how_read'].pop('how_read')
        for label, value in cases.items():
            with self.subTest(case=label):
                self.add_reading(raw=value if isinstance(value, str) else json.dumps(value))
                report = self.run_flow()
                self.assertEqual(report['status'], 'unresolved')
                self.assertIn('malformed reading', report['conditions_failed'])
                (self.repo / flow.READINGS_DIR / 'invented.json').unlink(); self.commit()
        (self.repo / flow.READINGS_DIR / 'notes.txt').write_text('x'); self.commit()
        self.assertIn('malformed reading', self.run_flow()['conditions_failed'])

    def test_types_pin_and_count_conditions(self):
        self.add_reading(account_sign_in_types=['chatgpt', 'chatgptDeviceCode', 'chatgptAuthTokens'])
        self.assertConditions(['types differ'])
        (self.repo / flow.READINGS_DIR / 'invented.json').unlink()
        self.add_reading(pin='9.9.8')
        self.assertConditions(['reading made for another bound set or pin'])
        self.add_reading(); self.add_reading(name='second.json')
        self.assertConditions(['more than one reading for this bound set'])

    def test_changed_definitions_are_unresolved(self):
        value = json.loads(self.schema.read_bytes())
        value['definitions']['PlanType']['enum'].append('invented')
        self.schema.write_text(json.dumps(value)); self.commit()
        self.add_reading()
        report = self.assertConditions(['schema differs'])
        self.assertEqual([d['definition'] for d in report['schema']['differences']], ['PlanType'])
        self.assertTrue(report['schema']['named_set_equal'])

    def test_unreadable_inputs_are_unresolved(self):
        self.schema.unlink(); self.commit()
        self.assertEqual(self.run_flow()['conditions_failed'], ['input unreadable'])
        self.setUp()
        (self.repo / 'app/src-tauri/src/hosting.rs').write_text('fn start(){}\n'); self.commit()
        self.assertEqual(self.run_flow()['conditions_failed'], ['input unreadable'])

    # Review round 3 probes: a working file changed, or a reading created, after the tool started
    # reading. The tool reads only the commit's objects, so neither reaches the result.
    def test_working_changes_during_the_run_do_not_reach_the_result(self):
        self.add_reading()
        original = flow.Repository.show
        def show(repo, commit, path):
            (self.repo / 'app/src-tauri/src/nested/auth_rpc.rs').write_text('chatgptAuthTokens\n')
            (self.repo / flow.READINGS_DIR / 'second.json').write_text(json.dumps(self.reading_value()))
            return original(repo, commit, path)
        with patch.object(flow.Repository, 'show', show):
            report = self.run_flow()
        self.assertEqual((report['status'], report['readings']['bound']), ('unchanged', ['invented.json']))
        self.assertEqual(self.run_flow()['conditions_failed'], ['working tree differs from the commit under app/'])

    def test_evidence_is_a_plain_search_of_tracked_files(self):
        (self.repo / 'app/src-tauri/src/spelled.rs').write_text('x("account/login/\\\n    start"); concat!("account/", "login/start");\n')
        self.commit()
        found = self.run_flow()['evidence']['lines']
        self.assertTrue(any(e['file'].startswith('app/src-tauri/resources/') for e in found))   # schemas are searched too
        lines = {(e['file'], e['line']) for e in found if not e['file'].startswith('app/src-tauri/resources/')}
        self.assertEqual(lines, {('app/src-tauri/src/hosting.rs', 2), ('app/src-tauri/src/nested/auth_rpc.rs', 1),
                                 ('app/src/login.ts', 1), ('app/src-tauri/src/spelled.rs', 1), ('app/src-tauri/src/spelled.rs', 2)})

    def test_bound_set_is_the_stated_listing(self):
        raw = subprocess.run(['git', '-C', str(self.repo), 'ls-tree', '-r', '-z', 'HEAD', '--', 'app/'],
                             capture_output=True, check=True, env=ENV).stdout
        listing = b''.join(item + b'\n' for item in raw.split(b'\0') if item and not item.split(b'\t', 1)[1].startswith(b'app/packaging/terms/readings/'))
        self.assertEqual(flow.bound_set(flow.Repository(self.repo).entries(self.head())), hashlib.sha256(listing).hexdigest())

    def test_retained_record_is_never_written(self):
        retained = ROOT / 'app/packaging/terms/retained'
        def state():
            return {str(p): (p.stat().st_mtime_ns, hashlib.sha256(p.read_bytes()).hexdigest())
                    for p in sorted(retained.rglob('*')) if p.is_file()}
        before = state()
        self.add_reading(); flow.compare(self.repo)
        self.assertEqual(state(), before)
        self.assertNotIn('applicability', flow.compare(self.repo))

    def test_baseline_pin_and_schema_derive_from_the_recorded_revision(self):
        revision = flow.BASELINE['revision']
        if subprocess.run(['git', '-C', str(ROOT), 'cat-file', '-e', revision + '^{commit}'], capture_output=True).returncode:
            self.skipTest('recorded revision not in this clone\'s history')
        repo = flow.Repository(ROOT)
        self.assertEqual(flow.declared_pin(repo, revision), flow.BASELINE['pin'])
        self.assertEqual(hashlib.sha256(repo.show(revision, flow.SCHEMA.format(pin=flow.BASELINE['pin']))).hexdigest(),
                         flow.BASELINE['schema_file_sha256'])


if __name__ == '__main__':
    unittest.main()
