"""Joined synthetic package/terms/S4 -> EXP -> SQ receiving; no native witness."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from package_successor_receiving_fixtures import JoinedFixture, adapter, canonical, encoded, load, APP

sq = load('joined_package_sq', APP / 'examination/sq_receiving/receive_packages.py')


class PackageSuccessorReceivingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sq = sq.Receiver()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.f = JoinedFixture(self.root)

    def receive(self):
        return self.f.receiver.receive(self.f.packet / 'binding.json', self.f.packet, self.f.config, self.f.config_sha)

    def check(self):
        self.f.write_selection()
        return self.sq.check(self.f.path, self.f.sha, self.f.config, self.f.config_sha)

    def test_complete_selected_package_exp_sq_join_is_not_qualification(self):
        report = self.check()
        self.assertTrue(report['selection_consistent'], report)
        self.assertEqual(report['coverage'], 'complete', report)
        package = report['package_reports']['package-witness']
        self.assertEqual(package['errors'], [])
        self.assertEqual(package['missing'], [])
        self.assertEqual(package['record_id'], self.f.package.request['record_id'])
        self.assertNotEqual(package['record_id'], package['candidate']['package_record_id'])
        self.assertEqual(report['package_routes']['package-witness'], {
            'input_format': 'packaged-s4-binding/1', 's4_witness_selected': True,
            'evidence_consistency': 'consistent'})
        self.assertTrue(any(c['scope'] == 'package/' + self.f.linked_slot for c in report['existing_checks']))
        self.assertEqual(len([c for c in report['existing_checks'] if c['scope'].startswith('review/')]), 23)
        self.assertFalse(package['release_authorized'])
        self.assertFalse(package['live_authority'])
        for key in ('qualification_established', 'current_reliance', 'actual_producer_use_verified',
                    'native_observation_verified', 'publication_authority_authenticated', 'method_adoption_authenticated'):
            self.assertIs(report[key], False)
        self.assertTrue(report['unresolved_external_references'])

    def test_publisher_trust_is_external_and_missing_trust_stays_missing(self):
        self.f.set_trust(None); self.f.save()
        report = self.check()
        self.assertTrue(report['selection_consistent'], report)
        self.assertEqual(report['coverage'], 'incomplete')
        self.assertIn('independently selected publisher', str(report['missing_selected_inputs']))
        self.f.set_trust('f' * 64); self.f.save()
        report = self.check()
        self.assertFalse(report['selection_consistent'])
        self.assertIn('trusted publisher digest', str(report))
        # A request cannot turn its own evidence digest into receiving authority.
        self.f.package.request['trusted_publisher_sha256'] = self.f.package.trusted_publisher_sha256
        self.f.package.save()
        with self.assertRaises(ValueError): self.receive()

    def test_changed_configuration_requires_exact_selection_and_sidecar(self):
        self.f.set_trust(None)
        with self.assertRaisesRegex(ValueError, 'configuration digest'):
            self.f.receiver.receive(self.f.packet / 'binding.json', self.f.packet, self.f.config, '0' * 64)
        self.f.selection['configuration_sha256'] = self.f.config_sha
        report = self.check()
        self.assertFalse(report['selection_consistent'])
        self.assertIn('binding or source/configuration', str(report))

    def test_wrapper_and_inner_static_package_id_never_substitute(self):
        report = self.receive()
        result = copy.deepcopy(self.f.records[self.f.linked_slot])
        inner = report['candidate']['package_record_id']
        result['subject']['app_candidate']['package_record'] = inner
        errors, _ = self.f.receiver.package_link(result, report, report['candidate']['revision'],
            report['candidate']['build_identity'], report['candidate']['codex_pin'], inner)
        self.assertIn('LINK-WITNESS-REFERENCE', [e['code'] for e in errors])
        self.f.package.request['candidate']['package_record_id'] = 'INVENTED-WRONG-INNER'
        self.f.save()
        self.assertFalse(self.check()['selection_consistent'])

    def test_equal_outer_and_inner_ids_are_refused_even_with_rebound_citations(self):
        same = self.f.package.request['candidate']['package_record_id']
        self.f.package.request['record_id'] = same
        self.f.dossier['candidate']['package_record'] = same
        self.f.records[self.f.linked_slot]['subject']['app_candidate']['package_record'] = same
        self.f.selection['packages'][0]['ref'] = same
        self.f.save(rebind_package=False)
        report = self.check()
        self.assertFalse(report['selection_consistent'])
        self.assertIn('outer witness and inner static package IDs must differ', report.get('input_error', ''))

    def test_legacy_package_route_is_explicit_and_does_not_claim_s4(self):
        artifact = self.f.selection['artifacts'][-1]
        legacy = self.f.package.values['legacy.json']
        raw = encoded(legacy)
        sidecar = encoded(self.f.canonical.binding('package', raw, 'current_producer_declaration'))
        (self.f.packet / 'legacy-receiving.json').write_bytes(raw)
        (self.f.packet / 'legacy-receiving.binding.json').write_bytes(sidecar)
        artifact.update(kind='package', record={'path': 'legacy-receiving.json', 'sha256': adapter.sha(raw)},
                        binding={'path': 'legacy-receiving.binding.json', 'sha256': adapter.sha(sidecar)})
        ref = legacy['record_id']
        self.f.dossier['candidate']['package_record'] = ref
        self.f.records[self.f.linked_slot]['subject']['app_candidate']['package_record'] = ref
        self.f.selection['packages'][0]['ref'] = ref
        # Rebind only EXP inputs; the separately selected legacy package stays legacy.
        saved = self.f.selection['artifacts'].pop()
        self.f.save()
        self.f.selection['artifacts'].append(saved)
        report = self.check()
        self.assertTrue(report['selection_consistent'], report.get('errors', report.get('input_error')))
        self.assertEqual(report['coverage'], 'complete')
        self.assertEqual(report['package_routes']['package-witness'], {
            'input_format': 'PKG-v0.2', 's4_witness_selected': False,
            'evidence_consistency': 'legacy_checks_only'})
        self.assertEqual(report['package_reports'], {})
        self.assertFalse(report['qualification_established'])

    def test_exact_exp_candidate_pin_support_currency_and_route_guards(self):
        report = self.receive(); original = self.f.records[self.f.linked_slot]
        cases = [(lambda r: r['subject']['app_candidate'].update(revision='other'), 'LINK-REVISION'),
                 (lambda r: r['subject']['app_candidate'].update(build_identity='other'), 'LINK-BUILD'),
                 (lambda r: r['configuration'].update(codex_pin='0.158.0'), 'LINK-PIN'),
                 (lambda r: r['support_revision'].update(prototype_digest='sha256:' + '0' * 64), 'LINK-SUPPORT-IDENTITY'),
                 (lambda r: r['currency'].update(state='historical', change_ref='INVENTED-HISTORICAL-CHANGE'), 'LINK-HISTORICAL-RESULT'),
                 (lambda r: r['configuration']['route'].update(kind='native_development'), 'LINK-PACKAGED-ROUTE')]
        for mutate, expected in cases:
            value = copy.deepcopy(original); mutate(value)
            errors, _ = self.f.receiver.package_link(value, report, report['candidate']['revision'],
                report['candidate']['build_identity'], report['candidate']['codex_pin'], report['record_id'])
            with self.subTest(expected=expected):
                self.assertIn(expected, [e['code'] for e in errors])

    def test_missing_s4_artifact_is_incomplete_not_legacy_success(self):
        (self.f.packet / self.f.package.request['custody']['path']).unlink()
        # Existing binding continues to identify the same exact wrapper, but its
        # missing closure must not be hidden behind a consistent static record.
        report = self.check()
        self.assertEqual(report['coverage'], 'incomplete', report)
        self.assertIn('custody.json', str(report))
        self.assertFalse(report['qualification_established'])

    def test_rehashed_s4_generation_contradiction_survives_exp_sq_receiving(self):
        name = self.f.package.request['observation']['path']
        observation = copy.deepcopy(self.f.package.values[name])
        observation['generation']['spawnCounter'] += 1
        self.f.package.request['observation'] = self.f.package.put(name, observation)
        self.f.save()
        report = self.check()
        self.assertFalse(report['selection_consistent'])
        self.assertIn('S4 generation', str(report))

    def test_missing_terms_and_installer_closure_remain_gaps(self):
        for key in ('terms', 'installer'):
            static = self.f.package.values['static.json']
            target = self.f.packet / static[key]['path']
            raw = target.read_bytes(); target.unlink()
            report = self.check()
            with self.subTest(key=key):
                self.assertEqual(report['coverage'], 'incomplete')
                self.assertIn(static[key]['path'], str(report))
            target.write_bytes(raw)

    def test_legacy_and_unknown_versions_do_not_downcast(self):
        raw = (self.f.packet / 'binding.json').read_bytes()
        with self.assertRaises(ValueError):
            self.f.canonical.binding('package', raw, 'current_producer_declaration')
        for version in ('PKG-v0.2', 'pkg-identity.s1', 'packaged-s4-binding/99', 'static-package-input/2'):
            request = copy.deepcopy(self.f.package.request); request['format'] = version
            (self.f.packet / 'binding.json').write_bytes(encoded(request))
            with self.subTest(version=version), self.assertRaisesRegex(ValueError, 'unsupported package witness'):
                self.receive()
        (self.f.packet / 'binding.json').write_bytes(raw)
        self.f.selection['format'] = 'sq-exp-receiving-selection.v1'
        report = self.check()
        self.assertFalse(report['selection_consistent'])
        self.assertIn('unsupported selection format', str(report))

    def test_mixed_legacy_sidecar_and_missing_profile_refuse(self):
        artifact = self.f.selection['artifacts'][-1]
        old = encoded(self.f.canonical.binding('package', encoded(self.f.package.values['legacy.json']),
                                              'current_producer_declaration'))
        (self.f.packet / artifact['binding']['path']).write_bytes(old)
        artifact['binding']['sha256'] = adapter.sha(old)
        report = self.check()
        self.assertFalse(report['selection_consistent'])
        self.assertIn('binding or source/configuration', str(report))
        self.f.selection.pop('package_source_profile_sha256')
        self.assertFalse(self.check()['selection_consistent'])
        with patch.object(adapter, 'PINS_SHA256', '0' * 64):
            with self.assertRaisesRegex(ValueError, 'profile changed'): adapter.Receiver()

    def test_exact_wrapper_bytes_and_citation_coverage_cannot_be_hidden(self):
        path = self.f.packet / 'binding.json'; path.write_bytes(path.read_bytes() + b'\n')
        report = self.check()
        self.assertFalse(report['selection_consistent'])
        self.assertIn('exact-byte mismatch', report.get('input_error', ''))
        self.f.save()
        self.f.selection['packages'] = []
        report = self.check()
        self.assertIn('unreferenced selected artifacts', report.get('input_error', ''))
        self.f.selection['artifacts'] = [a for a in self.f.selection['artifacts'] if a['kind'] != 'package_witness']
        report = self.check()
        self.assertEqual(report['coverage'], 'incomplete')
        self.assertIn('cited package selection missing', str(report['missing_selected_inputs']))

    def test_reported_native_failure_remains_gap_not_package_qualification(self):
        self.f.records[self.f.linked_slot]['outcome'] = 'fail'
        self.f.dossier['scenarios'][0]['steps'][0]['outcome'] = 'fail'
        self.f.save()
        report = self.check()
        self.assertTrue(report['selection_consistent'], report)
        self.assertEqual(report['coverage'], 'incomplete')
        self.assertIn('linked native result reported fail', str(report))

    def test_rehashed_typed_null_closure_is_refused_through_sq(self):
        for name in ('static.json', 'custody.json', 'terms.json'):
            self.f = JoinedFixture(self.root / name.replace('.', '-'))
            self.f.replace_package_artifact(name, b'null\n')
            self.f.save(rebind_package=False)
            report = self.check()
            with self.subTest(artifact=name):
                self.assertFalse(report['selection_consistent'])
                self.assertIn('typed artifact must be an object', report.get('input_error', ''))

    def test_derived_unverifiable_is_missing_in_joined_receiving(self):
        package = copy.deepcopy(self.f.package.values['package.json'])
        package.update(packaged_inventory=None, distribution_status='unverifiable')
        self.f.replace_package_artifact('package.json', encoded(package))
        self.f.save()
        report = self.check()
        self.assertTrue(report['selection_consistent'], report.get('errors'))
        self.assertEqual(report['coverage'], 'incomplete')
        self.assertIn('static package distribution reference equality', str(report['missing_selected_inputs']))

    def test_derived_mismatch_survives_missing_reference_evidence(self):
        package = copy.deepcopy(self.f.package.values['package.json'])
        inventory = copy.deepcopy(self.f.package.values['inventory.json'])
        inventory['inventory']['entries'][0]['mode'] = 448
        package['packaged_inventory'] = self.f.package.put('different-inventory.json', inventory)
        package['distribution_status'] = 'mismatch'
        self.f.replace_package_artifact('package.json', encoded(package))
        (self.f.packet / 'evidence.json').unlink()
        self.f.save()
        report = self.check()
        self.assertFalse(report['selection_consistent'])
        self.assertIn('static package distribution mismatch', str(report['errors']))
        self.assertIn('static supplier closure', str(report['missing_selected_inputs']))

    def test_staged_producer_never_falls_back_to_ambient_repository(self):
        source = 'execution/PKG-01/DEL-01-06/Work/package-successor-v1/packaged-s4-binding.v1.schema.json'
        self.assertTrue((APP.parent / source).is_file())
        staged = Path(self.f.receiver.producer_snapshot.name) / source
        staged.unlink()
        with self.assertRaises((ValueError, OSError)):
            self.receive()

    def test_actual_cli_connects_package_exp_without_ambient_scanner(self):
        result_path = self.f.packet / next(a['record']['path'] for a in self.f.selection['artifacts'] if a['slot'] == self.f.linked_slot)
        candidate = self.f.package.request['candidate']
        command = [sys.executable, '-B', str(APP / 'examination/package_receiving/adapter.py'), 'package-link',
                   '--request', str(self.f.packet / 'binding.json'), '--evidence-root', str(self.f.packet),
                   '--configuration', str(self.f.config), '--configuration-sha256', self.f.config_sha,
                   '--result', str(result_path), '--revision', candidate['revision'], '--build', candidate['build_identity'],
                   '--pin', candidate['codex_pin'], '--package-ref', self.f.package.request['record_id']]
        job = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(job.returncode, 0, job.stdout + job.stderr)
        report = json.loads(job.stdout)
        self.assertTrue(report['file_checks_passed'])
        self.assertEqual(report['missing'], [])
        for key in ('qualification_established', 'release_authorized', 'live_authority'):
            self.assertFalse(report[key])


if __name__ == '__main__': unittest.main()
