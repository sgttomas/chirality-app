"""Synthetic package/S4 joins; no signing, scanner, supplier or native execution."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'app/packaging/successor'))
from fixtures import Fixture, checker


class PackageSuccessor(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.f = Fixture(self.root)

    def rejected(self):
        try:
            report = self.f.check()
        except ValueError:
            return
        self.assertTrue(report['errors'], report)

    def update(self, filename, value):
        """Refresh declared reference hashes so tests exercise value joins too."""
        ref = self.f.put(filename, value)
        def replace(item):
            if isinstance(item, dict):
                if set(item) == {'path', 'sha256'} and item['path'] == filename:
                    item.update(ref)
                else:
                    for child in item.values(): replace(child)
            elif isinstance(item, list):
                for child in item: replace(child)
        replace(self.f.request)
        return ref

    def test_positive_static_and_binding_never_grant_authority(self):
        r = self.f.check()
        self.assertEqual((r['errors'], r['missing']), ([], []))
        self.assertEqual(r['record_id'], 'INVENTED-PACKAGE-WITNESS')
        self.assertEqual(r['candidate']['package_record_id'], 'PKG-STATIC-SYNTHETIC')
        self.assertFalse(r['live_authority']); self.assertFalse(r['release_authorized'])
        self.assertEqual(r['source_dependencies'], checker.source_dependencies())
        s = checker.check(self.root / 'static.json')
        self.assertEqual((s['errors'], s['missing']), ([], []))
        self.assertEqual(s['source_dependencies'], r['source_dependencies'])

    def test_trust_missing_is_gap_wrong_trust_is_error(self):
        r = self.f.check(False)
        self.assertEqual(r['errors'], [])
        self.assertIn('independently selected publisher binding digest', r['missing'])
        r = checker.check(self.root / 'binding.json', trusted_publisher_sha256='0' * 64)
        self.assertIn('trusted publisher digest', r['errors'])
        self.f.request['trusted_publisher_sha256'] = self.f.trusted_publisher_sha256
        self.rejected()

    def test_all_candidate_axes_and_wrapper_identity_are_separate(self):
        for key in self.f.request['candidate']:
            with self.subTest(key=key):
                prior = self.f.request['candidate'][key]
                self.f.request['candidate'][key] = 'wrong'
                self.rejected()
                self.f.request['candidate'][key] = prior
        self.f.request['record_id'] = 'NEW-CALLER-WRAPPER-ID'
        self.assertEqual(self.f.check()['record_id'], 'NEW-CALLER-WRAPPER-ID')

    def test_app_and_publisher_axes(self):
        for key in ('revision', 'build_identity', 'version', 'identifier', 'cdhash',
                    'publisher_binding_sha256', 'public_projection_sha256', 'supplier_selection_sha256'):
            with self.subTest(key=key):
                original = self.f.request['app'][key]
                self.f.request['app'][key] = 'd' * len(original)
                self.rejected()
                self.f.request['app'][key] = original

    def test_custody_generation_inventory_and_selection_cannot_drift(self):
        for key in ('generation', 'inventory', 'selection'):
            value = copy.deepcopy(self.f.values['custody.json'])
            if key == 'generation': value[key]['spawnCounter'] += 1
            elif key == 'inventory': value[key]['entries'][0]['mode'] = 448
            else: value[key]['compiledAnchor']['sha256'] = 'e' * 64
            with self.subTest(key=key):
                ref = self.update('custody.json', value)
                obs = copy.deepcopy(self.f.values['observation.json']); obs['checks']['custody']['evidence'] = ref
                self.update('observation.json', obs)
                self.rejected()

    def test_signing_flags_limits_and_old_formats_refuse(self):
        baseline = copy.deepcopy(self.f.values['custody.json'])
        for key, value in [('standing', 'synthetic-source-fixture'), ('requirement_sha256', 'f' * 64),
                           ('static_validation_flags', 0), ('limits', ['INVENTED'] * 5)]:
            body = copy.deepcopy(baseline); body['app'][key] = value
            ref = self.update('custody.json', body)
            obs = copy.deepcopy(self.f.values['observation.json']); obs['checks']['custody']['evidence'] = ref
            self.update('observation.json', obs)
            self.rejected()
        obs['format'] = 'observed-verification.s1'; self.update('observation.json', obs); self.rejected()

    def test_preflight_label_and_generation_and_check_standing(self):
        for key in ('raw_version_label', 'generation'):
            facts = copy.deepcopy(self.f.values['facts.json'])
            if key == 'generation': facts[key]['home'] = 'other'
            else: facts[key] = 'codex-cli 0.0.0'
            ref = self.update('facts.json', facts)
            obs = copy.deepcopy(self.f.values['observation.json'])
            for name in ('tree', 'label', 'reference', 'generated'): obs['checks'][name]['evidence'] = ref
            self.update('observation.json', obs); self.rejected()
        obs['checks']['custody']['outcome'] = 'unverifiable'
        self.update('observation.json', obs); self.rejected()

    def test_hash_tamper_missing_file_and_path_refusal(self):
        (self.root / 'app.bin').write_bytes(b'changed')
        self.rejected()
        (self.root / 'app.bin').unlink()
        r = self.f.check(); self.assertIn('artifact:app.bin', r['missing'])
        self.f.request['app']['executable']['path'] = '../outside'
        self.rejected()

    def test_legacy_request_refused_without_downcast(self):
        self.f.request['format'] = 'static-distribution-input/1'
        self.rejected()
        self.assertEqual((ROOT / 'app/packaging/static_distribution/check.py').read_bytes(),
                         subprocess.check_output(['git', 'show', 'c26fb825:app/packaging/static_distribution/check.py'], cwd=ROOT))

    def test_examination_can_replay_entire_reported_closure_without_repo(self):
        report = self.f.check()
        with tempfile.TemporaryDirectory() as other:
            stage = Path(other).resolve()
            for name in report['source_dependencies']:
                target = stage / name; target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / name, target)
            evidence = stage / 'packet'; evidence.mkdir()
            for name in list(report['artifacts']) + ['binding.json']:
                target = evidence / name; target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(self.root / name, target)
            result = subprocess.run([sys.executable, str(stage / 'app/packaging/successor/check.py'),
                                     str(evidence / 'binding.json'), '--evidence-root', str(evidence),
                                     '--trusted-publisher-sha256', self.f.trusted_publisher_sha256], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertEqual(json.loads(result.stdout)['source_dependencies'], report['source_dependencies'])


if __name__ == '__main__':
    unittest.main()
