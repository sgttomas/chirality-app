"""Transitive runtime notice index: cargo-free check refusals; no fetch, build or Cargo run."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('notice_transitive', ROOT / 'app/packaging/notices/transitive.py')
t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)


class Transitive(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.index = Path(self.tmp.name) / 'index.json'
        shutil.copyfile(t.INDEX, self.index)
        self.value = json.loads(self.index.read_text())

    def write(self):
        self.index.write_text(json.dumps(self.value))

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
        self.setUp(); next(e for e in self.value['cargo'] if e['source'] == 'registry')['version'] = '999.0.0'; self.write()
        with self.assertRaisesRegex(ValueError, 'unlocked'): t.check(self.index)

    def test_missing_direct_component_refuses(self):
        self.value['cargo'] = [e for e in self.value['cargo'] if e['package'] != 'rusqlite']; self.write()
        with self.assertRaisesRegex(ValueError, 'direct crate missing'): t.check(self.index)

    def test_text_kind_must_match_members_and_received_text(self):
        member = next(e for e in self.value['cargo'] if e['source'] == 'registry' and e['notice_members'])
        member['text'] = {'kind': 'missing'}; self.write()
        with self.assertRaisesRegex(ValueError, 'contradicts'): t.check(self.index)
        self.setUp(); received = next(e for e in self.value['cargo'] if e['text']['kind'] == 'received-upstream-text')
        received['text']['git_blob_sha1'] = '0' * 40; self.write()
        with self.assertRaisesRegex(ValueError, 'received upstream text differs'): t.check(self.index)


if __name__ == '__main__':
    unittest.main()
