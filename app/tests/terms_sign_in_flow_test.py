"""Candidate sign-in flow against the flow the retained terms record covers (DEL-01-06 AC-004).

Invented candidate source trees and invented readings; the retained record and the 0.160.0 schema
are copied read-only. No test writes a reading into the repository."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('terms_sign_in_flow', ROOT / 'app/packaging/terms/flow.py')
flow = importlib.util.module_from_spec(spec); spec.loader.exec_module(flow)

HOSTING = 'pub const DECLARED_PIN: &str = "9.9.9";\nfn start(){ self.request_begin_scoped("account/login/start",json!({"type":kind})); }\n'


class SignInFlow(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.base = Path(temp.name).resolve()
        self.source = self.base / 'candidate'
        self.src = self.source / flow.SOURCE_DIR
        (self.src / 'nested').mkdir(parents=True)
        (self.src / 'hosting.rs').write_text(HOSTING)
        (self.src / 'auth_rpc.rs').write_text('fn guard(){ if method == "account/login/start" {} }\n')
        (self.src / 'nested/mod.rs').write_text('// invented\nfn other(){}\n')
        self.schema = self.source / flow.SCHEMA.format(pin='9.9.9')
        self.schema.parent.mkdir(parents=True)
        shutil.copyfile(ROOT / flow.SCHEMA.format(pin='0.160.0'), self.schema)
        for relative in (flow.RETAINED_RECORD, flow.SCHEMA.format(pin='0.160.0')):
            (self.source / relative).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, self.source / relative)
        self.readings = self.source / flow.READINGS_DIR
        self.readings.mkdir(parents=True)
        shutil.copyfile(ROOT / flow.READINGS_DIR / 'README.md', self.readings / 'README.md')

    def digest(self):
        return flow.tree_digest(flow.Tree(self.source).files(flow.SOURCE_DIR))

    def reading(self, name='invented-reading.json', **changes):
        value = {'format': flow.READING_FORMAT, 'source_tree_sha256': self.digest(), 'pin': '9.9.9',
                 'reader': {'name': 'Invented Reviewer', 'role': 'reviewer', 'did_not_write_the_sign_in_change': True},
                 'date': '2026-11-12', 'account_sign_in_types': ['chatgpt', 'chatgptDeviceCode'],
                 'separate_credential_logins': [{'type': 'apiKey', 'home': 'invented key home',
                                                 'sent_from': [{'file': 'hosting.rs', 'line': 2}]}],
                 'relied_on': [{'file': 'hosting.rs', 'line': 2}, {'file': 'auth_rpc.rs', 'line': 1}]}
        value.update(changes)
        (self.readings / name).write_text(json.dumps(value))
        return value

    def run_flow(self):
        return flow.compare(self.source)

    def assertConditions(self, expected):
        report = self.run_flow()
        self.assertEqual(report['status'], 'unresolved' if expected else 'unchanged', report)
        self.assertEqual(report['conditions_failed'], expected)
        return report

    def test_no_reading_is_unresolved(self):
        report = self.assertConditions(['no reading for this source tree'])
        self.assertEqual(flow.main(['--source-root', str(self.source)]), 1)
        self.assertEqual(report['source']['files'], 3)

    def test_matching_reading_is_unchanged(self):
        self.reading()
        report = self.assertConditions([])
        self.assertEqual(report['readings']['bound'], ['invented-reading.json'])
        self.assertEqual(report['readings']['account_sign_in_types'], ['chatgpt', 'chatgptDeviceCode'])
        self.assertEqual(flow.main(['--source-root', str(self.source)]), 0)
        self.assertTrue(report['establishes'])

    def test_one_byte_change_anywhere_in_host_source_makes_the_reading_stale(self):
        self.reading()
        for path in ('nested/mod.rs', 'hosting.rs', 'new.rs'):
            with self.subTest(path=path):
                target = self.src / path
                original = target.read_bytes() if target.exists() else None
                target.write_bytes((original or b'') + b' ')
                self.assertConditions(['reading made for another tree or pin'])
                target.write_bytes(original) if original is not None else target.unlink()
        self.assertConditions([])

    def test_reading_for_another_pin_is_unresolved(self):
        self.reading(pin='9.9.8')
        self.assertConditions(['reading made for another tree or pin'])

    def test_types_differing_from_the_baseline_are_unresolved(self):
        self.reading(account_sign_in_types=['chatgpt', 'chatgptDeviceCode', 'chatgptAuthTokens'])
        self.assertConditions(['types differ'])

    def test_more_than_one_reading_for_the_tree_is_unresolved(self):
        self.reading(); self.reading(name='second.json')
        self.assertConditions(['more than one reading for this source tree'])

    def test_malformed_readings_are_unresolved(self):
        digest = self.digest()
        cases = {
            'missing field': lambda v: v.pop('relied_on'),
            'extra field': lambda v: v.update(note='x'),
            'unknown format': lambda v: v.update(format='other'),
            'author reading': lambda v: v['reader'].update(did_not_write_the_sign_in_change=False),
            'unnamed reader': lambda v: v['reader'].update(name=' '),
            'bad date': lambda v: v.update(date='12/11/2026'),
            'empty types': lambda v: v.update(account_sign_in_types=[]),
            'duplicate types': lambda v: v.update(account_sign_in_types=['chatgpt', 'chatgpt']),
            'bad digest': lambda v: v.update(source_tree_sha256='ABC'),
            'file not in tree': lambda v: v.update(relied_on=[{'file': 'absent.rs', 'line': 1}]),
            'line beyond end': lambda v: v.update(relied_on=[{'file': 'hosting.rs', 'line': 99}]),
            'empty relied_on': lambda v: v.update(relied_on=[]),
            'login without place': lambda v: v['separate_credential_logins'][0].update(sent_from=[]),
        }
        for label, change in cases.items():
            with self.subTest(case=label):
                for p in self.readings.glob('*.json'):
                    p.unlink()
                value = self.reading()
                change(value)
                (self.readings / 'invented-reading.json').write_text(json.dumps(value))
                report = self.run_flow()
                self.assertEqual(report['status'], 'unresolved')
                self.assertIn('malformed reading', report['conditions_failed'])
        for p in self.readings.glob('*.json'):
            p.unlink()
        (self.readings / 'truncated.json').write_text('{"format":')
        self.assertIn('malformed reading', self.run_flow()['conditions_failed'])
        (self.readings / 'truncated.json').unlink()
        (self.readings / 'notes.txt').write_text('x')
        self.assertIn('malformed reading', self.run_flow()['conditions_failed'])
        self.assertEqual(digest, self.digest())

    def test_changed_definitions_are_unresolved(self):
        self.reading()
        value = json.loads(self.schema.read_bytes())
        value['definitions']['PlanType']['enum'].append('invented')   # reached only by reference
        self.schema.write_text(json.dumps(value))
        report = self.assertConditions(['schema differs'])
        self.assertEqual([d['definition'] for d in report['schema']['differences']], ['PlanType'])
        self.assertTrue(report['schema']['named_set_equal'])
        value['definitions']['LoginAccountParams']['oneOf'].append({'title': 'Invented'})
        self.schema.write_text(json.dumps(value))
        self.assertEqual(len(self.assertConditions(['schema differs'])['schema']['differences']), 2)

    def test_definition_outside_the_flow_does_not_count(self):
        self.reading()
        value = json.loads(self.schema.read_bytes())
        value['definitions']['ThreadStartParams'].setdefault('properties', {})['invented'] = {'type': 'string'}
        self.schema.write_text(json.dumps(value))
        self.assertConditions([])

    def test_unreadable_inputs_are_unresolved(self):
        self.reading()
        cases = []
        def missing_schema():
            self.schema.unlink()
        def missing_definition():
            value = json.loads(self.schema.read_bytes()); del value['definitions']['LoginAppBrand']
            self.schema.write_text(json.dumps(value))
        def linked_source():
            os.symlink(self.base, self.src / 'escape')
        def special_source():
            os.mkfifo(self.src / 'pipe')
        def no_pin():
            (self.src / 'hosting.rs').write_text('fn start(){}\n')
        def changed_baseline():
            path = self.source / flow.SCHEMA.format(pin='0.160.0'); path.write_bytes(path.read_bytes() + b'\n')
        def linked_reading():
            os.symlink(self.readings / 'invented-reading.json', self.readings / 'linked.json')
        for label, act in (('missing schema', missing_schema), ('missing definition', missing_definition),
                           ('linked source', linked_source), ('special source', special_source),
                           ('no pin', no_pin), ('changed baseline schema', changed_baseline)):
            with self.subTest(case=label):
                self.setUp(); self.reading(); act()
                report = self.run_flow()
                self.assertEqual((report['status'], report['conditions_failed']), ('unresolved', ['input unreadable']), report)
        self.setUp(); self.reading(); linked_reading()
        self.assertIn('malformed reading', self.run_flow()['conditions_failed'])

    @unittest.skipIf(os.geteuid() == 0, 'root reads everything')
    def test_unreadable_source_file_is_unresolved(self):
        self.reading()
        target = self.src / 'nested/mod.rs'; target.chmod(0o000); self.addCleanup(target.chmod, 0o644)
        self.assertEqual(self.run_flow()['conditions_failed'], ['input unreadable'])

    def test_evidence_is_a_plain_search_without_exclusions(self):
        # Review probes: spellings a parser missed are still evidence lines, and decide nothing.
        (self.src / 'nested/hosting_tests.rs').write_text(
            '#[cfg(test)]\nfn t(){ x("account/login/\\\n    start"); concat!("account/", "login/start"); LoginAccountParams; }\n')
        found = {(e['file'], e['line']) for e in self.run_flow()['source']['evidence']}
        self.assertEqual(found, {('hosting.rs', 2), ('auth_rpc.rs', 1), ('nested/hosting_tests.rs', 2), ('nested/hosting_tests.rs', 3)})

    def test_tree_digest_is_the_stated_canonical_form(self):
        files = {'b.rs': b'two', 'a/z.rs': b'one'}
        preimage = flow.TREE_METHOD.encode() + b'\0' + (2).to_bytes(8, 'big')
        for path in ('a/z.rs', 'b.rs'):
            preimage += len(path).to_bytes(8, 'big') + path.encode() + len(files[path]).to_bytes(8, 'big') + files[path]
        self.assertEqual(flow.tree_digest(files), hashlib.sha256(preimage).hexdigest())

    def test_retained_record_is_never_written(self):
        retained = ROOT / 'app/packaging/terms/retained'
        def state():
            return {str(p): (p.stat().st_mtime_ns, hashlib.sha256(p.read_bytes()).hexdigest())
                    for p in sorted(retained.rglob('*')) if p.is_file()}
        before = state()
        flow.compare(ROOT)
        flow.compare(self.source, record_root=ROOT)
        self.assertEqual(state(), before)
        self.assertNotIn('applicability', flow.compare(self.source))

    def test_baseline_pin_and_schema_derive_from_the_recorded_revision(self):
        revision = flow.BASELINE['revision']
        if subprocess.run(['git', '-C', str(ROOT), 'cat-file', '-e', revision + '^{commit}'], capture_output=True).returncode:
            self.skipTest('recorded revision not in this clone\'s history')
        git = flow.GitRevision(ROOT, revision)
        self.assertEqual(flow.declared_pin(git), flow.BASELINE['pin'])
        self.assertEqual(hashlib.sha256(git.read(flow.SCHEMA.format(pin=flow.BASELINE['pin']))).hexdigest(),
                         flow.BASELINE['schema_file_sha256'])


if __name__ == '__main__':
    unittest.main()
