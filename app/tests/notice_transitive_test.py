"""Transitive runtime notice index: cargo-free check refusals; no fetch, build or Cargo run."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import tomllib
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('notice_transitive', ROOT / 'app/packaging/notices/transitive.py')
t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)


class Transitive(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.index = Path(self.tmp.name) / 'index.json'
        shutil.copyfile(t.INDEX, self.index)
        self.value = json.loads(self.index.read_text())

    def write(self, rebind=False):
        if rebind:  # a mutator who also recomputes the receipt digests
            self.value['generation']['member_set_sha256'] = t.member_digests(self.value['cargo'], self.value['npm'])
        self.index.write_text(json.dumps(self.value))

    def refuses(self, pattern):
        with self.assertRaisesRegex(ValueError, pattern): t.check(self.index)

    def test_committed_index_matches_current_manifests_and_direct_index(self):
        index = t.check()
        s = t.summary(index)
        self.assertGreater(s['cargo_runtime_crates'], 0)
        self.assertEqual(sum(s['text_kinds'].values()), s['cargo_runtime_crates'] + s['npm_runtime_packages'])

    def test_moved_basis_refuses(self):
        self.value['source_basis']['app/src-tauri/Cargo.lock'] = '0' * 64; self.write()
        with self.assertRaisesRegex(ValueError, 'regenerate'): t.check(self.index)

    def test_checksum_drift_and_unlocked_crate_refuse(self):
        crate = next(e for e in self.value['cargo'] if e['source'] == 'registry')
        crate['archive_sha256'] = '0' * 64; self.write()
        with self.assertRaisesRegex(ValueError, 'checksum'): t.check(self.index)
        self.setUp(); next(e for e in self.value['cargo'] if e['source'] == 'registry')['version'] = '999.0.0'; self.write(rebind=True)
        with self.assertRaisesRegex(ValueError, 'unlocked'): t.check(self.index)

    def test_missing_direct_component_refuses(self):
        self.value['cargo'] = [e for e in self.value['cargo'] if e['package'] != 'rusqlite']; self.write(rebind=True)
        with self.assertRaisesRegex(ValueError, 'direct crate missing|unreachable'): t.check(self.index)

    def test_text_kind_must_match_members_and_received_text(self):
        member = next(e for e in self.value['cargo'] if e['source'] == 'registry' and e['notice_members'])
        member['text'] = {'kind': 'missing'}; self.write()
        with self.assertRaisesRegex(ValueError, 'contradicts'): t.check(self.index)

    def test_changed_retained_received_text_refuses(self):
        repo = Path(self.tmp.name) / 'repo'
        for rel in (*t.BASIS, t.OBJC2_METADATA, *t.RECEIVED_TEXTS.values()):
            (repo / rel).parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(ROOT / rel, repo / rel)
        t.check(self.index, repo)
        text = repo / t.RECEIVED_TEXTS['https://github.com/madsmtm/objc2']
        text.write_bytes(text.read_bytes() + b'\n')
        with self.assertRaisesRegex(ValueError, 'received upstream text differs'): t.check(self.index, repo)

    def test_dropped_or_altered_rows_break_the_generation_receipt(self):
        for mutate in (lambda v: v.update(cargo=[e for e in v['cargo'] if e['package'] != 'adler2']),
                       lambda v: v.update(npm=[e for e in v['npm'] if e['package'] != 'scheduler']),
                       lambda v: v['npm'][0].update(integrity='sha512-' + 'A' * 86 + '==')):
            self.setUp(); mutate(self.value); self.write()
            self.refuses('generation receipt')

    def test_npm_rows_are_recomputed_from_the_lock_even_when_the_receipt_is_rebound(self):
        self.value['npm'] = [e for e in self.value['npm'] if e['package'] != 'scheduler']; self.write(rebind=True)
        self.refuses('package-lock')
        self.setUp(); self.value['npm'][0]['integrity'] = 'sha512-' + 'A' * 86 + '=='; self.write(rebind=True)
        self.refuses('package-lock')

    def test_cargo_text_kinds_cannot_hide_unverified_npm_packages(self):
        for package in ('scheduler', 'react'):
            row = next(e for e in self.value['npm'] if e['package'] == package)
            original = row['text']
            for kind in ('archive-member', 'received-upstream-text'):
                with self.subTest(package=package, kind=kind):
                    row['text'] = {'kind': kind}; self.write()
                    self.refuses('unknown npm text kind')
            row['text'] = original

    def test_unsupported_npm_lock_lookup_refuses(self):
        lock = json.loads((ROOT / 'app/package-lock.json').read_text())
        repo = Path(self.tmp.name) / 'repo'; (repo / 'app').mkdir(parents=True)
        del lock['packages']['node_modules/scheduler']
        (repo / 'app/package-lock.json').write_text(json.dumps(lock))
        with self.assertRaisesRegex(ValueError, 'unsupported lookup'): t.npm_runtime(repo)

    def test_registry_row_relabelled_as_path_refuses(self):
        crate = next(e for e in self.value['cargo'] if e['package'] == 'adler2')
        crate.update(source='path', archive_sha256='0' * 64); self.write(rebind=True)
        self.refuses('source kind contradicts Cargo.lock')

    def test_extra_locked_but_unreachable_row_refuses(self):
        lock = tomllib.loads((ROOT / 'app/src-tauri/Cargo.lock').read_text())['package']
        members = {(e['package'], e['version']) for e in self.value['cargo']}
        named = {d.split()[0] for p in lock if (p['name'], p['version']) in members for d in p.get('dependencies', [])}
        extra = next(p for p in lock if 'source' in p and p['name'] not in named and (p['name'], p['version']) not in members)
        self.value['cargo'].append({'package': extra['name'], 'version': extra['version'], 'source': 'registry',
                                    'archive_sha256': extra['checksum'], 'declared_license': 'MIT', 'notice_members': [],
                                    'native_source_paths': [], 'text': {'kind': 'missing'}}); self.write(rebind=True)
        self.refuses('unreachable')

    def test_received_text_reads_only_the_allowed_retained_source(self):
        invented = Path(self.tmp.name) / 'invented-LICENSE.md'; invented.write_bytes(b'invented text\n')
        blob = t.git_blob(invented.read_bytes())
        original = Path.read_bytes
        opened = []
        def tracking(path):
            opened.append(Path(path).resolve()); return original(path)
        for path in (str(invented), t.WORK + '/../../../../../' + str(invented).lstrip('/'),
                     t.WORK + '/approved-receipt-20261102/sources/objc2/../../../' + invented.name):
            self.setUp()
            received = next(e for e in self.value['cargo'] if e['text']['kind'] == 'received-upstream-text')
            received['text'].update(path=path, git_blob_sha1=blob); self.write(rebind=True)
            with mock.patch.object(Path, 'read_bytes', tracking):
                self.refuses('allowed retained source')
            self.assertNotIn(invented.resolve(), opened)
        self.setUp()
        received = next(e for e in self.value['cargo'] if e['text']['kind'] == 'received-upstream-text')
        received['text']['git_blob_sha1'] = blob; self.write(rebind=True)
        self.refuses('no known received-text blob')


if __name__ == '__main__':
    unittest.main()
