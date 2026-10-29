"""Bounded notice input and opt-in resource checks; no build, network or supplier run."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

APP = Path(__file__).resolve().parents[1]
ROOT = APP / 'packaging/notices'
OVERLAY = APP / 'packaging/unsigned/tauri.notices.conf.json'
spec = importlib.util.spec_from_file_location('notice_check', ROOT / 'check.py')
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


class NoticeResources(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / 'notices'
        shutil.copytree(ROOT, self.root)
        self.overlay = self.base / 'overlay.json'
        shutil.copyfile(OVERLAY, self.overlay)
        self.index = check.load(self.root / 'index.json')

    def write_index(self):
        (self.root / 'index.json').write_text(json.dumps(self.index))

    def validate(self):
        return check.check(self.root, overlay=self.overlay)

    def test_saved_scope_is_app_and_exact_direct_runtime_set(self):
        index = self.validate()
        self.assertEqual(len(index['components']), 17)
        self.assertEqual(sum(len(c['notices']) for c in index['components']), 30)
        self.assertEqual(sum(n['size_bytes'] for c in index['components'] for n in c['notices']), 133902)
        self.assertNotIn('tauri-build', {c['package'] for c in index['components']})

    def test_changed_notice_bytes_refuse(self):
        path = self.root / self.index['components'][1]['notices'][0]['asset']
        path.write_bytes(path.read_bytes() + b'changed')
        with self.assertRaisesRegex(ValueError, 'notice bytes/size differ'):
            self.validate()

    def test_missing_extra_and_unindexed_assets_refuse(self):
        path = self.root / self.index['components'][0]['notices'][0]['asset']
        raw = path.read_bytes(); path.unlink()
        with self.assertRaisesRegex(ValueError, 'missing or extra notice assets'):
            self.validate()
        path.write_bytes(raw)
        (self.root / 'assets/extra.txt').write_text('unindexed')
        with self.assertRaisesRegex(ValueError, 'missing or extra notice assets'):
            self.validate()

    def test_index_extra_duplicate_wrong_version_and_missing_runtime_refuse(self):
        original = copy.deepcopy(self.index)
        mutations = [lambda: self.index['components'].append(copy.deepcopy(self.index['components'][0])),
                     lambda: self.index['components'][1].update(version='9.9.9'),
                     lambda: self.index['components'].pop()]
        for mutate in mutations:
            self.index = copy.deepcopy(original); mutate(); self.write_index()
            with self.assertRaises(ValueError):
                self.validate()

    def test_extra_asset_reference_and_escaping_path_refuse(self):
        original = copy.deepcopy(self.index)
        extra = copy.deepcopy(self.index['components'][1]['notices'][0])
        extra['asset'] += '.extra'; extra['source_path'] += '.extra'; extra['archive_member'] += '.extra'
        self.index['components'][1]['notices'].append(extra); self.write_index()
        with self.assertRaisesRegex(ValueError, 'missing or extra notice assets'):
            self.validate()
        self.index = original
        self.index['components'][0]['notices'][0]['asset'] = '../outside'
        self.write_index()
        with self.assertRaisesRegex(ValueError, 'relative path'):
            self.validate()

    def test_links_empty_extra_directories_and_unknown_format_refuse(self):
        (self.root / 'assets/link').symlink_to('app/LICENSE.md')
        with self.assertRaisesRegex(ValueError, 'linked or special'):
            self.validate()
        (self.root / 'assets/link').unlink(); (self.root / 'assets/empty').mkdir()
        with self.assertRaisesRegex(ValueError, 'asset directories'):
            self.validate()
        (self.root / 'assets/empty').rmdir()
        self.index['format'] = 'unknown'; self.write_index()
        with self.assertRaisesRegex(ValueError, 'shape/version'):
            self.validate()

    def test_wrong_or_omitted_overlay_resource_refuses(self):
        overlay = check.load(self.overlay)
        key = '../packaging/notices/index.json'
        overlay['bundle']['resources'][key] = 'wrong/index.json'
        self.overlay.write_text(json.dumps(overlay))
        with self.assertRaisesRegex(ValueError, 'overlay differs'):
            self.validate()
        del overlay['bundle']['resources'][key]; self.overlay.write_text(json.dumps(overlay))
        with self.assertRaisesRegex(ValueError, 'overlay differs'):
            self.validate()

    def test_explicit_mapping_stages_exact_saved_namespace_without_claiming_sdk_execution(self):
        overlay = check.load(OVERLAY)
        paths = {s: d for s, d in overlay['bundle']['resources'].items() if d.startswith('third-party-notices/')}
        self.assertEqual(len(paths), 31)
        self.assertEqual(len(set(paths.values())), 31)
        staging = self.base / 'staging'
        for source, destination in paths.items():
            target = staging / destination
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(APP / 'src-tauri' / source, target)
        index = check.check(staging / 'third-party-notices')
        self.assertEqual(index, check.load(ROOT / 'index.json'))
        self.assertEqual({str(p.relative_to(staging / 'third-party-notices')) for p in (staging / 'third-party-notices').rglob('*') if p.is_file()},
                         {'index.json'} | {n['asset'] for c in index['components'] for n in c['notices']})

    def test_source_archive_missing_or_wrong_bytes_refuse_without_fallback(self):
        component = next(c for c in self.index['components'] if c['ecosystem'] == 'npm')
        subset = {'components': [component]}
        cargo_home, npm_cache = self.base / 'cargo', self.base / 'npm'
        with self.assertRaises(FileNotFoundError):
            check.check_archives(subset, APP.parent, cargo_home, npm_cache)
        import base64
        digest = base64.b64decode(component['source']['integrity'].split('-', 1)[1]).hex()
        archive = npm_cache / '_cacache/content-v2/sha512' / digest[:2] / digest[2:4] / digest[4:]
        archive.parent.mkdir(parents=True); archive.write_bytes(b'wrong local archive')
        with self.assertRaisesRegex(ValueError, 'archive digest/size differs'):
            check.check_archives(subset, APP.parent, cargo_home, npm_cache)


if __name__ == '__main__':
    unittest.main()
