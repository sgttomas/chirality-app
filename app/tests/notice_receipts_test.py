"""Invented local receipts only; no supplier/network execution."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('notice_receipts', ROOT / 'app/packaging/notices/receipts.py')
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)


def fixture(repo, intake):
    work = repo / r.WORK; work.mkdir(parents=True, exist_ok=True)
    for name in ('public-metadata.json', 'macos-runtime-license-metadata.json'):
        shutil.copyfile(ROOT / r.WORK / name, work / name)
    index = repo / 'app/packaging/notices/index.json'
    index.parent.mkdir(parents=True, exist_ok=True)
    if not index.exists(): shutil.copyfile(ROOT / 'app/packaging/notices/index.json', index)
    codex = json.loads((work / 'public-metadata.json').read_bytes())
    for row in codex['proposed_file_retrieval']:
        raw = ('INVENTED inspection ' + row['path']).encode()
        row.update(size_bytes=len(raw), git_blob_sha1=r.blob(raw))
        path = intake / 'codex' / row['path']; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(raw)
    (work / 'public-metadata.json').write_bytes(r.encode(codex))
    mac = json.loads((work / 'macos-runtime-license-metadata.json').read_bytes())
    raw = b'INVENTED upstream text; not a license grant\n'
    for row in [mac['deduplicated_retrieval_proposal'], *mac['crate_associations']]:
        row.update(size_bytes=len(raw), git_blob_sha1=r.blob(raw))
    (work / 'macos-runtime-license-metadata.json').write_bytes(r.encode(mac))
    (intake / 'objc2').mkdir(parents=True); (intake / 'objc2/LICENSE.md').write_bytes(raw)


class Receipts(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve(); self.repo = self.root / 'repo'; self.intake = self.root / 'intake'
        fixture(self.repo, self.intake)
        private = self.root / 'private'; private.mkdir()
        self.selection = private / 'selection.json'; self.output = self.root / 'output'
        self.choose()

    def choose(self, **changes):
        self.selection.write_bytes(r.encode(dict(format='upstream-notice-selection/1', plan_sha256=r.files.sha(r.encode(r.plan(self.repo))),
                                                components=['objc2', 'dispatch2'], basis='INVENTED scope examination') | changes))

    def stage(self): return r.stage(self.intake, self.selection, self.output, self.repo)

    def test_real_plan_exact_proposal(self):
        p = r.plan(); self.assertEqual(len(p['entries']), 11)
        self.assertEqual(sum(e['size_bytes'] for e in p['entries']), 130005)
        self.assertEqual(len(p['associations']), 5)

    def test_complete_and_partial_receipts(self):
        report = r.verify(self.intake, self.repo)
        self.assertEqual(len(report['verified']), 11); self.assertFalse(report['errors'] or report['missing'])
        (self.intake / 'objc2/LICENSE.md').unlink()
        self.assertEqual(r.verify(self.intake, self.repo)['missing'], ['objc2/LICENSE.md'])

    def test_wrong_size_and_same_size_wrong_blob(self):
        path = self.intake / 'objc2/LICENSE.md'; original = path.read_bytes()
        for raw in (b'wrong', b'X' * len(original)):
            with self.subTest(raw=raw):
                path.write_bytes(raw)
                self.assertEqual(r.verify(self.intake, self.repo)['errors'], ['objc2/LICENSE.md'])
                with self.assertRaises(ValueError): self.stage()

    def test_links_refused(self):
        path = self.intake / 'objc2/LICENSE.md'; other = self.root / 'body'; path.rename(other)
        for link in ('symbolic', 'hard'):
            with self.subTest(link=link):
                if link == 'symbolic': path.symlink_to(other)
                else: os.link(other, path)
                self.assertEqual(r.verify(self.intake, self.repo)['errors'], ['objc2/LICENSE.md'])
                path.unlink()

    def test_selection_closed_explicit_current_scope(self):
        for change in ({'components': []}, {'components': ['objc2', 'objc2']}, {'components': ['codex']},
                       {'components': ['../objc2']}, {'basis': ''}, {'plan_sha256': '0'*64}, {'extra': True}):
            with self.subTest(change=change):
                self.choose(**change)
                with self.assertRaises(ValueError): self.stage()
        self.selection.write_text('{"format":1,"format":2}')
        with self.assertRaises(ValueError): self.stage()

    def test_supplement_preserves_provenance_and_no_private_basis(self):
        result = self.stage(); manifest = result['manifest']
        self.assertEqual([a['package'] for a in manifest['associations']], ['dispatch2', 'objc2'])
        self.assertNotIn(b'INVENTED scope examination', (self.output / 'manifest.json').read_bytes())
        self.assertNotIn(str(self.root), json.dumps(manifest))
        self.assertIn('not an archive member', ' '.join(manifest['limits']))
        self.assertEqual(r.check_stage(self.output, self.repo), result)
        self.assertEqual(r.plan(self.repo)['index_sha256'], manifest['index_sha256'])
        with self.assertRaises(FileExistsError): self.stage()

    def test_incomplete_and_tamper_refused_even_rehashed(self):
        self.stage()
        (self.output / 'INCOMPLETE.txt').write_text('interrupted')
        with self.assertRaises(ValueError): r.check_stage(self.output, self.repo)
        (self.output / 'INCOMPLETE.txt').unlink()
        (self.output / 'LICENSE.md').write_bytes(b'bad')
        marker = json.loads((self.output / 'COMPLETE.json').read_bytes()); marker['files']['LICENSE.md'] = r.files.sha(b'bad')
        (self.output / 'COMPLETE.json').write_bytes(r.encode(marker))
        with self.assertRaises(ValueError): r.check_stage(self.output, self.repo)

    def test_failure_retains_incomplete_marker(self):
        original = r.io.write_new
        def fail(path, raw):
            if path.name == 'manifest.json': raise OSError('invented failure')
            original(path, raw)
        with patch.object(r.io, 'write_new', side_effect=fail):
            with self.assertRaises(OSError): self.stage()
        self.assertTrue((self.output / 'INCOMPLETE.txt').exists())
        with self.assertRaises(ValueError): r.check_stage(self.output, self.repo)

    def test_overlap_and_changed_input_refused(self):
        for parent in (self.intake, self.repo, self.selection.parent):
            with self.subTest(parent=parent):
                self.output = parent / 'output'
                with self.assertRaises(ValueError): self.stage()
        self.output = self.root / 'output'
        original = r.read; count = 0
        def changed(path):
            nonlocal count
            raw = original(path)
            if path == self.selection:
                count += 1
                if count == 2: return raw + b' '
            return raw
        with patch.object(r, 'read', side_effect=changed):
            with self.assertRaises(ValueError): self.stage()
        self.assertFalse(self.output.exists())

    def test_current_association_drift_refused(self):
        path = self.repo / 'app/packaging/notices/index.json'; index = json.loads(path.read_bytes())
        next(c for c in index['components'] if c['package'] == 'objc2')['version'] = '99.0.0'
        path.write_bytes(r.encode(index))
        with self.assertRaises(ValueError): r.plan(self.repo)


if __name__ == '__main__': unittest.main()
