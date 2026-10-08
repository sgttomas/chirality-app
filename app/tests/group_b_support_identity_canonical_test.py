"""Canonical additive binding tests; all record events and actors remain invented."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

APP = Path(__file__).resolve().parents[1]

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module

canonical = load('canonical_binding_test_subject', APP / 'examination/support_identity/canonical.py')
fixtures = load('canonical_binding_invented_fixtures', APP / 'tests/group_b_support_identity_test.py')


def write_bundle(root, support, records, selected):
    for role, kind in support.legacy.KINDS.items():
        pair = {}
        data = fixtures.encoded(records[role])
        binding = fixtures.encoded(support.binding(kind, data, selected['binding_purpose']))
        for part, payload in [('record', data), ('binding', binding)]:
            name = role + '.' + part + '.json'; (root / name).write_bytes(payload)
            pair[part] = {'path': name, 'sha256': canonical.sha(payload)}
        selected['artifacts'][role] = pair
    path = root / 'selection.json'; path.write_bytes(fixtures.encoded(selected)); return path


def selection_for(support):
    records, selected = fixtures.fixture_records(support.support)
    selected.pop('standing')
    selected.update(format='exp-support-selection.canonical.v1', binding_method=canonical.METHOD,
                    binding_purpose='current_producer_declaration', declaration_sha256=support.declaration_sha256)
    return records, selected


class CanonicalBindingTests(unittest.TestCase):
    def setUp(self):
        self.support = canonical.CanonicalSupport()
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup); self.root = Path(self.temp.name)
        self.records, self.selected = selection_for(self.support)
        self.rebuild()

    def rebuild(self):
        self.path = write_bundle(self.root, self.support, self.records, self.selected)

    def check(self):
        self.path.write_bytes(fixtures.encoded(self.selected))
        return self.support.check(self.path, canonical.sha(self.path.read_bytes()))

    def binding_change(self, role, mutate):
        ref = self.selected['artifacts'][role]['binding']; path = self.root / ref['path']
        value = json.loads(path.read_bytes()); mutate(value); path.write_bytes(fixtures.encoded(value))
        ref['sha256'] = canonical.sha(path.read_bytes())

    def test_fixed_publication_and_full_connected_existing_checks(self):
        report = self.check()
        self.assertTrue(report['canonical_consistency_passed'], report['errors'])
        self.assertEqual(set(report['existing_checks']), {'package', 'review', 'change'})
        self.assertEqual(report['fixed_support_selection']['publication_reference']['revision'],
                         '09106477e351c6e5bde85259c55a00cc8fc5f7f5')
        self.assertEqual(report['inputs'], self.selected['artifacts'])
        self.assertEqual(len(report['existing_checks']['package']['reported_prerequisite_gaps']), 3)
        for key in ('producer_use_verified', 'publication_authority_authenticated',
                    'method_adoption_authenticated', 'qualification_established'):
            self.assertFalse(report[key])

    def test_historical_correspondence_never_upgrades_to_verified_producer_use(self):
        self.selected['binding_purpose'] = 'historical_correspondence'; self.rebuild()
        report = self.check(); self.assertTrue(report['canonical_consistency_passed'])
        self.assertFalse(report['producer_use_verified'])
        self.assertEqual(report['binding_purpose'], 'historical_correspondence')
        self.selected['binding_purpose'] = 'current_producer_declaration'
        with self.assertRaisesRegex(ValueError, 'purpose mismatch'): self.check()
        self.rebuild(); self.assertFalse(self.check()['producer_use_verified'])
        self.binding_change('before', lambda b: b.update(producer_use_verified=True))
        with self.assertRaisesRegex(ValueError, 'invalid canonical binding'): self.check()

    def test_publication_and_method_cannot_be_selected_by_record_writer(self):
        self.selected['declaration_sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'caller-selected publication'): self.check()
        self.selected['declaration_sha256'] = self.support.declaration_sha256
        for mutate in (lambda b: b.update(publication='published'), lambda b: b.update(adopted=True),
                       lambda b: b.update(binding_method='EXP-SUPPORT-BINDING-v2')):
            self.rebuild(); self.binding_change('review', mutate)
            with self.assertRaises(ValueError): self.check()
        self.rebuild(); self.selected['publication'] = {'approved': True}
        with self.assertRaisesRegex(ValueError, 'unknown fields'): self.check()

    def test_full_tuple_and_digests_are_required_for_every_kind(self):
        mutations = [lambda b: b['support_identity']['schema_ids'].pop('review'),
                     lambda b: b['support_identity']['schema_ids'].update(change='other'),
                     lambda b: b['support_identity'].update(exp_version='EXP-v0.3'),
                     lambda b: b['support_identity'].update(prototype_sha256='0' * 64),
                     lambda b: b['artifact'].update(sha256='0' * 64)]
        for role in self.support.legacy.KINDS:
            for mutate in mutations:
                with self.subTest(role=role):
                    self.rebuild(); self.binding_change(role, mutate)
                    with self.assertRaises(ValueError): self.check()

    def test_canonical_method_sources_and_reader_pins_refuse_drift(self):
        with patch.object(canonical, 'PINS_SHA256', '0' * 64):
            with self.assertRaisesRegex(ValueError, 'pins changed'): canonical.CanonicalSupport()
        for relative, data in self.support.captured.items():
            path = self.root / relative; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
        method = self.root / self.support.pins['method']; method.write_bytes(method.read_bytes() + b'\n')
        with patch.object(canonical, 'PROJECT', self.root):
            with self.assertRaisesRegex(ValueError, 'canonical selected source changed'): canonical.CanonicalSupport()
        method.unlink()
        with patch.object(canonical, 'PROJECT', self.root):
            with self.assertRaises(OSError): canonical.CanonicalSupport()

    def test_source_tuple_cannot_be_repinned_without_semantic_agreement(self):
        local = self.root / 'tool'; local.mkdir()
        declaration = copy.deepcopy(self.support.declaration)
        declaration['support_identity']['schema_ids']['review'] = 'other'
        payload = fixtures.encoded(declaration)
        for relative, data in self.support.captured.items():
            path = self.root / relative; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
        path = self.root / self.support.pins['declaration']; path.write_bytes(payload)
        pins = copy.deepcopy(self.support.pins); pins['sources'][pins['declaration']] = canonical.sha(payload)
        pins_bytes = fixtures.encoded(pins); (local / 'canonical-pins.v1.json').write_bytes(pins_bytes)
        # A test-only artificial repin must still fail source-to-identity checking.
        with patch.object(canonical, 'HERE', local), patch.object(canonical, 'PROJECT', self.root), \
             patch.object(canonical, 'PINS_SHA256', canonical.sha(pins_bytes)):
            # Supply all legacy source inputs to reach the independent tuple check.
            for relative, data in self.support.support.sources.items():
                file = self.root / relative; file.parent.mkdir(parents=True, exist_ok=True); file.write_bytes(data)
            with self.assertRaisesRegex(ValueError, 'tuple differs'): canonical.CanonicalSupport()

    def test_selection_and_original_byte_mutations_refuse(self):
        digest = canonical.sha(self.path.read_bytes()); self.path.write_bytes(self.path.read_bytes() + b'\n')
        with self.assertRaisesRegex(ValueError, 'selection digest mismatch'): self.support.check(self.path, digest)
        record = self.root / self.selected['artifacts']['review']['record']['path']
        record.write_bytes(record.read_bytes() + b'\n')
        with self.assertRaisesRegex(ValueError, 'artifact digest mismatch'): self.check()
        self.selected['artifacts']['review']['record']['sha256'] = canonical.sha(record.read_bytes())
        with self.assertRaisesRegex(ValueError, 'binding identity'): self.check()

    def test_mixed_legacy_and_canonical_bindings_refuse(self):
        data = fixtures.encoded(self.records['review'])
        ref = self.selected['artifacts']['review']['binding']
        payload = fixtures.encoded(self.support.support.binding('review', data))
        (self.root / ref['path']).write_bytes(payload); ref['sha256'] = canonical.sha(payload)
        with self.assertRaisesRegex(ValueError, 'invalid canonical binding'): self.check()

    def test_history_actor_package_and_unresolved_join_failures_remain_enforced(self):
        mutations = [lambda: self.records['after'].update(outcome='pass'),
                     lambda: self.records['review']['reviewer'].update(identity='OTHER'),
                     lambda: self.records['package']['app'].update(build_identity='OTHER'),
                     lambda: self.records['review']['evidence_set'].append('UNRESOLVED')]
        for mutate, code in zip(mutations, ('CHANGE-HISTORY-MUTATED', 'REVIEW-REVIEWER', 'LINK-BUILD', 'UNRESOLVED-JOIN-REFERENCES')):
            self.records, self.selected = selection_for(self.support); mutate(); self.rebuild()
            report = self.check(); self.assertFalse(report['canonical_consistency_passed'])
            self.assertIn(code, [e['code'] for e in report['errors']])

    def test_record_version_missing_binding_and_path_escape_refuse(self):
        self.records['change']['format'] = 'EXP-v0.3'; self.rebuild()
        with self.assertRaisesRegex(ValueError, 'mixed record versions'): self.check()
        self.records['change']['format'] = 'EXP-v0.2'; self.rebuild()
        self.selected['artifacts']['package'].pop('binding')
        with self.assertRaisesRegex(ValueError, 'missing'): self.check()
        self.rebuild(); self.selected['artifacts']['package']['record']['path'] = '../outside'
        with self.assertRaisesRegex(ValueError, 'relative path'): self.check()

    def test_cli_canonical_check_and_binding_limits(self):
        command = [sys.executable, '-B', str(APP / 'examination/support_identity/canonical.py')]
        result = subprocess.run(command + ['check', str(self.path), '--selection-sha256', canonical.sha(self.path.read_bytes())],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(json.loads(result.stdout)['canonical_consistency_passed'])
        result = subprocess.run(command + ['bind', 'review', str(self.root / 'review.record.json'),
                                          '--purpose', 'historical_correspondence'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        binding = json.loads(result.stdout); self.assertEqual(binding['binding_purpose'], 'historical_correspondence')
        self.assertNotIn('canonical_consistency_passed', binding)


if __name__ == '__main__':
    unittest.main(verbosity=2)
