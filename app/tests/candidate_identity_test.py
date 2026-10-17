"""candidate-identity-v1: bundle tree identity and candidate identification record."""
import contextlib
import io
import json
import os
from pathlib import Path
import plistlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'examination' / 'candidate_identity'))
import identify  # noqa: E402


def write_bundle(root, identifier='dev.example.test-candidate', extra=None):
    app = Path(root) / 'Test.app'
    (app / 'Contents/MacOS').mkdir(parents=True)
    (app / 'Contents/Resources/instructions').mkdir(parents=True)
    (app / 'Contents/Info.plist').write_bytes(plistlib.dumps({
        'CFBundleExecutable': 'app', 'CFBundleIdentifier': identifier, 'CFBundleShortVersionString': '0.0.0'}))
    exe = app / 'Contents/MacOS/app'
    exe.write_bytes(b'\xcf\xfa\xed\xfe binary')
    exe.chmod(0o755)
    (app / 'Contents/Resources/instructions/AGENTS.md').write_text('guidance\n')
    os.symlink('instructions/AGENTS.md', app / 'Contents/Resources/link')
    for name, data in (extra or {}).items():
        (app / name).write_bytes(data)
    return app


class BundleIdentity(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp()).resolve()
        self.addCleanup(shutil.rmtree, self.tmp)

    def ident(self, app):
        return identify.identity(identify.inventory(app))

    def test_identity_excludes_location_and_is_stable(self):
        a = write_bundle(self.tmp / 'a'); b = write_bundle(self.tmp / 'b')
        self.assertEqual(self.ident(a), self.ident(b))
        self.assertRegex(self.ident(a), r'^chirality\.app\.bundle-tree\.sha256/v1:[0-9a-f]{64}$')

    def test_every_content_mode_and_structure_change_changes_identity(self):
        base = self.ident(write_bundle(self.tmp / 'base'))
        mutations = {
            'byte': lambda app: (app / 'Contents/MacOS/app').write_bytes(b'\xcf\xfa\xed\xfe binarY'),
            'mode': lambda app: (app / 'Contents/MacOS/app').chmod(0o744),
            'dir_mode': lambda app: (app / 'Contents/Resources').chmod(0o700),
            'root_mode': lambda app: app.chmod(0o700),
            'link_target': lambda app: (os.unlink(app / 'Contents/Resources/link'), os.symlink('elsewhere', app / 'Contents/Resources/link')),
            'extra_file': lambda app: (app / 'Contents/Resources/new.txt').write_text('x'),
            'missing_file': lambda app: (app / 'Contents/Resources/instructions/AGENTS.md').unlink(),
            'empty_dir': lambda app: (app / 'Contents/Resources/empty').mkdir(),
        }
        for name, mutate in mutations.items():
            with self.subTest(name):
                app = write_bundle(self.tmp / name)
                mutate(app)
                self.assertNotEqual(self.ident(app), base)

    def test_unrepresentable_or_unsafe_entries_refuse(self):
        app = write_bundle(self.tmp / 'fifo'); os.mkfifo(app / 'Contents/pipe')
        with self.assertRaisesRegex(ValueError, 'special file'): identify.inventory(app)
        app = write_bundle(self.tmp / 'hard'); os.link(app / 'Contents/MacOS/app', app / 'Contents/MacOS/twin')
        with self.assertRaisesRegex(ValueError, 'hard-linked'): identify.inventory(app)
        real = write_bundle(self.tmp / 'real'); os.symlink(real, self.tmp / 'Alias.app')
        with self.assertRaisesRegex(ValueError, 'symlink in bundle root'): identify.inventory(self.tmp / 'Alias.app')
        with self.assertRaisesRegex(ValueError, r'\.app'): identify.inventory(self.tmp / 'real')

    def test_inventory_values_are_validated_before_identity(self):
        inv = identify.inventory(write_bundle(self.tmp / 'v'))
        broken = {
            'unsorted': lambda i: i['entries'].reverse(),
            'missing_parent': lambda i: i['entries'].pop(0),
            'extra_key': lambda i: i['entries'][-1].update(owner='me'),
            'bad_digest': lambda i: next(e for e in i['entries'] if e['kind'] == 'file').update(sha256='0' * 63),
            'other_method': lambda i: i.update(method='other/v1'),
            'absolute': lambda i: i['entries'].insert(0, {'path': '/x', 'kind': 'dir', 'mode': 0o755}),
        }
        for name, change in broken.items():
            with self.subTest(name):
                value = json.loads(json.dumps(inv)); change(value)
                with self.assertRaises(ValueError): identify.identity(value)


class CandidateRecord(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp()).resolve()
        self.addCleanup(shutil.rmtree, self.tmp)
        self.repo = self.tmp / 'repo'
        (self.repo / 'proj/app').mkdir(parents=True)
        (self.repo / 'proj/app/main.rs').write_text('fn main() {}\n')
        (self.repo / 'proj/README.md').write_text('readme\n')
        env = dict(os.environ, GIT_AUTHOR_NAME='t', GIT_AUTHOR_EMAIL='t@example.invalid',
                   GIT_COMMITTER_NAME='t', GIT_COMMITTER_EMAIL='t@example.invalid')
        for cmd in (['init', '-q'], ['add', '.'], ['commit', '-q', '-m', 'c']):
            subprocess.run(['git', '-C', str(self.repo), *cmd], check=True, env=env)
        self.export = self.tmp / 'export'; self.export.mkdir()
        archive = subprocess.run(['git', '-C', str(self.repo), 'archive', 'HEAD', 'proj'], check=True, capture_output=True).stdout
        subprocess.run(['tar', '-x', '-C', str(self.export)], input=archive, check=True)
        self.app = write_bundle(self.tmp / 'build')
        self.facts = self.tmp / 'facts.json'
        self.facts.write_text(json.dumps({
            'procedure': 'test', 'profile': 'debug', 'signing': 'none', 'features': [], 'command': ['build'],
            'config_overlays': [], 'toolchain': {}, 'lockfiles': {}, 'offline': True, 'environment': {},
            'started_at': '2026-10-17T00:00:00Z', 'finished_at': '2026-10-17T00:01:00Z'}))
        self.home = self.tmp / 'home'; (self.home / 'Library/Application Support').mkdir(parents=True)

    def run_tool(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.dict(os.environ, {'HOME': str(self.home)}), contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = identify.main(list(argv))
        return code, out.getvalue(), err.getvalue()

    def record(self, out='rec'):
        return self.run_tool('record', '--app', str(self.app), '--repo', str(self.repo), '--revision', 'HEAD',
                             '--prefix', 'proj', '--export-root', str(self.export), '--build-facts', str(self.facts),
                             '--identified-at', '2026-10-17T00:02:00Z', '--out-dir', str(self.tmp / out))

    def test_record_binds_revision_source_and_bundle_and_check_recomputes(self):
        code, out, err = self.record()
        self.assertEqual(code, 0, err)
        record = json.loads((self.tmp / 'rec/candidate-identification.json').read_text())
        head = subprocess.run(['git', '-C', str(self.repo), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
        self.assertEqual(record['app_candidate']['revision'], head)
        self.assertEqual(record['source']['tracked_files_verified'], 2)
        self.assertFalse(record['app_candidate']['packaged'])
        self.assertTrue(record['candidate_key'].startswith(head[:10] + '-'))
        self.assertNotRegex(record['app_candidate']['build_identity'], '(?i)illustrative|invented|example|placeholder')
        code, out, err = self.run_tool('check', '--record', str(self.tmp / 'rec/candidate-identification.json'), '--app', str(self.app))
        self.assertEqual(code, 0, out + err)
        (self.app / 'Contents/Resources/instructions/AGENTS.md').write_text('changed\n')
        code, out, _ = self.run_tool('check', '--record', str(self.tmp / 'rec/candidate-identification.json'), '--app', str(self.app))
        self.assertEqual(code, 1)
        self.assertIn('Contents/Resources/instructions/AGENTS.md', json.loads(out)['changed'])

    def test_tampered_record_or_inventory_refuses(self):
        self.assertEqual(self.record()[0], 0)
        path = self.tmp / 'rec/candidate-identification.json'
        original = path.read_text()
        record = json.loads(original); record['candidate_key'] = '0' * 10 + '-' + '0' * 12
        path.write_text(json.dumps(record))
        self.assertEqual(self.run_tool('check', '--record', str(path), '--app', str(self.app))[0], 2)
        path.write_text(original)
        inv = self.tmp / 'rec/bundle-inventory.json'; inv.write_bytes(inv.read_bytes().replace(b'"mode":493', b'"mode":511', 1))
        self.assertEqual(self.run_tool('check', '--record', str(path), '--app', str(self.app))[0], 2)

    def test_changed_export_or_existing_app_data_refuses(self):
        (self.export / 'proj/app/main.rs').write_text('fn main() { changed(); }\n')
        code, _, err = self.record('r1')
        self.assertEqual(code, 2); self.assertIn('differs from revision', err)
        (self.export / 'proj/app/main.rs').write_text('fn main() {}\n')
        (self.home / 'Library/Application Support/dev.example.test-candidate').mkdir()
        code, _, err = self.record('r2')
        self.assertEqual(code, 2); self.assertFalse((self.tmp / 'r2').exists())


if __name__ == '__main__':
    unittest.main()
