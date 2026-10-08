"""Actual synthetic Host exports connected to invented EXP/PKG record fixtures."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

APP = Path(__file__).resolve().parents[1]
HISTORICAL = APP / 'tests/group_b_distribution_receiving_fixtures'
NAMESPACE_HISTORICAL = APP / 'tests/group_b_distribution_receiving_namespace_fixtures'
LT23_SOURCE_HISTORICAL = APP / 'tests/group_b_distribution_receiving_lt23_source_fixtures'
PREVIOUS_CURRENT = APP / 'tests/group_b_distribution_receiving_terminal_source_fixtures'
FIXTURES = APP / 'tests/group_b_lt12_source_lt09_fixtures'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


receiver = load('_s4_receiving_test_subject', APP / 'examination/distribution_receiving/receive.py')
records = load('_s4_invented_record_fixtures', HISTORICAL / 'records.py')


def encoded(value):
    return (json.dumps(value, indent=2) + '\n').encode()


class DistributionReceivingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='s4-consumer-test-', dir=Path(tempfile.gettempdir()).resolve())
        self.addCleanup(self.temp.cleanup); self.root = Path(self.temp.name)
        self.receiver = receiver.Receiver()
        self.exports = Path(os.environ.get('CHIRALITY_S4_TEST_EXPORTS', str(FIXTURES)))
        self.select('selected')

    def select(self, case):
        self.case = self.root / 'case'
        if self.case.exists(): shutil.rmtree(self.case)
        shutil.copytree(self.exports / case, self.case)
        self.path = self.case / 'exchange.json'; self.exchange = receiver.parse(self.path.read_bytes())
        self.record_root = self.root / 'records'; self.record_root.mkdir(exist_ok=True)
        self.selection = records.write(self.record_root, self.receiver.canonical, self.exchange['applicationCandidate'])

    def check(self):
        self.path.write_bytes(encoded(self.exchange))
        return self.receiver.check(self.path, receiver.sha(self.path.read_bytes()),
                                   self.selection, receiver.sha(self.selection.read_bytes()))

    def refused(self, pattern='.'):
        with self.assertRaisesRegex((ValueError, OSError), pattern): self.check()

    def rebind_publication(self):
        """Adversarially rehash a changed projection to reach field-level refusals.

        This mutation never claims another native read occurred.
        """
        e = self.exchange['readback']['evidence']; ref = e['reference']; root = self.case / 'publication'
        def put(artifact, value):
            data = encoded(value); (root / artifact['path']).write_bytes(data); artifact['sha256'] = receiver.sha(data)
        put(ref['observed'], e['artifact'])
        e['lifecycle']['verification_artifact'] = copy.deepcopy(ref['observed'])
        put(ref['lifecycle'], e['lifecycle'])
        entries = []
        for f in sorted(root.rglob('*')):
            if f.is_file() and f.relative_to(root).as_posix() != ref['transport']['path']:
                entries.append({'path': f.relative_to(root).as_posix(), 'sha256': receiver.sha(f.read_bytes())})
        e['transport']['entries'] = entries
        put(ref['transport'], e['transport'])
        self.exchange['members'] = [{'path': f.relative_to(root).as_posix(),
                                      'sha256': receiver.sha(f.read_bytes()), 'size': f.stat().st_size}
                                     for f in sorted(root.rglob('*')) if f.is_file()]

    def test_actual_selected_and_unselected_host_exports_connect_to_full_canonical_join(self):
        for case in ('selected', 'unselected'):
            with self.subTest(case=case):
                self.select(case)
                raw = self.path.read_bytes()
                if self.exports == FIXTURES:
                    provenance = receiver.parse((FIXTURES / 'provenance.json').read_bytes())
                    self.assertEqual(receiver.sha(raw), provenance['exchange_sha256'][case])
                report = self.receiver.check(self.path, receiver.sha(raw), self.selection, receiver.sha(self.selection.read_bytes()))
                self.assertTrue(report['file_correspondence_passed'])
                self.assertEqual(set(report['canonical_support']['existing_checks']), {'package', 'review', 'change'})
                self.assertEqual(len(report['canonical_support']['existing_checks']['package']['reported_prerequisite_gaps']), 3)
                self.assertEqual(report['application_candidate']['standing'], 'invented-consumer-fixture')
                for key in ('native_reference_authority', 'semantic_reader_reexecuted', 'producer_history_authenticated',
                            'application_build_authenticated', 'qualification_established'):
                    self.assertFalse(report[key])
                expected = 17 if case == 'selected' else 4
                self.assertEqual(len(self.exchange['members']), expected)

    def test_original_exchange_and_selection_digests_are_required(self):
        exchange_sha = receiver.sha(self.path.read_bytes()); selection_sha = receiver.sha(self.selection.read_bytes())
        self.path.write_bytes(self.path.read_bytes() + b'\n')
        with self.assertRaisesRegex(ValueError, 'exchange digest'):
            self.receiver.check(self.path, exchange_sha, self.selection, selection_sha)
        self.selection.write_bytes(self.selection.read_bytes() + b'\n')
        with self.assertRaisesRegex(ValueError, 'support selection digest'):
            self.receiver.check(self.path, receiver.sha(self.path.read_bytes()), self.selection, selection_sha)

    def test_every_publication_member_and_selected_source_is_exact(self):
        for area, field in [('publication', 'members'), ('selected-source', 'selectedSourceMembers')]:
            for entry in self.exchange[field]:
                with self.subTest(area=area, member=entry['path']):
                    path = self.case / area / entry['path']; raw = path.read_bytes()
                    path.write_bytes(raw + b'\n'); self.refused('member bytes differ'); path.write_bytes(raw)
        self.exchange['members'][0]['sha256'] = '0' * 64; self.refused('member bytes differ')

    def test_missing_extra_empty_directory_and_special_file_refuse(self):
        root = self.case / 'publication'; path = root / self.exchange['members'][0]['path']
        raw = path.read_bytes(); path.unlink(); self.refused(); path.write_bytes(raw)
        (root / 'extra').write_bytes(b'opaque'); self.refused('inventory differs'); (root / 'extra').unlink()
        (root / 'empty').mkdir(); self.refused('inventory differs'); (root / 'empty').rmdir()
        os.mkfifo(root / 'pipe'); self.refused('unsupported closure entry')

    def test_symlink_component_leaf_and_traversal_refuse(self):
        path = self.case / 'publication' / self.exchange['members'][0]['path']
        raw = path.read_bytes(); other = self.root / 'outside'; other.write_bytes(raw)
        path.unlink(); path.symlink_to(other); self.refused(); path.unlink(); path.write_bytes(raw)
        directory = self.case / 'selected-source'; directory.rename(self.root / 'source')
        directory.symlink_to(self.root / 'source', target_is_directory=True); self.refused()
        directory.unlink(); (self.root / 'source').rename(directory)
        self.exchange['members'][0]['path'] = '../outside'; self.refused('noncontained')

    def test_duplicate_fields_extra_fields_manifest_aliases_and_order_refuse(self):
        raw = self.path.read_bytes(); duplicate = b'{"format":"x",' + raw[1:]
        self.path.write_bytes(duplicate)
        with self.assertRaisesRegex(ValueError, 'duplicate JSON'):
            self.receiver.check(self.path, receiver.sha(duplicate), self.selection, receiver.sha(self.selection.read_bytes()))
        self.exchange['publicationEstablished'] = True; self.refused('fields differ')
        self.exchange.pop('publicationEstablished'); self.exchange['members'].append(self.exchange['members'][0])
        self.refused('duplicate member'); self.exchange['members'].pop()
        self.exchange['members'].reverse(); self.refused('not sorted')

    def test_reader_revision_digest_and_producer_source_refuse(self):
        original = copy.deepcopy(self.exchange)
        for mutate in [lambda x: x['readback']['evidence']['reference']['reader'].update(semanticRevision='other'),
                       lambda x: x['readback']['evidence']['reference']['reader'].update(readerSourceSha256='0'*64),
                       lambda x: x['producer'].update(sourceRevision='0'*40)]:
            self.exchange = copy.deepcopy(original); mutate(self.exchange); self.refused('identity differs|source revision differs')

    def test_missing_unavailable_lifecycle_and_unsupported_event_refuse(self):
        original = copy.deepcopy(self.exchange)
        self.exchange['readback']['state'] = 'unavailable'; self.refused('unavailable')
        self.exchange = copy.deepcopy(original)
        self.exchange['readback']['evidence']['reference']['lifecycle'] = None; self.refused('envelope missing')
        self.exchange = copy.deepcopy(original)
        self.exchange['actualLt09']['transitionId'] = 'LT-08'
        self.exchange['readback']['evidence']['lifecycle']['legacy_event'] = self.exchange['actualLt09']
        self.rebind_publication(); self.refused('unsupported envelope')

    def test_projection_actual_event_and_generation_mismatch_refuse(self):
        original = copy.deepcopy(self.exchange)
        self.exchange['readback']['evidence']['artifact']['at'] = 'other'; self.refused('projection differs')
        self.exchange = copy.deepcopy(original); self.exchange['actualLt09']['at'] = 'other'; self.refused('LT09 differs')
        self.exchange = copy.deepcopy(original); self.exchange['readback']['generation']['spawnCounter'] += 1
        self.refused('mixed generation')

    def test_fully_rehashed_false_verified_and_custody_claims_refuse(self):
        for claim in ('verified', 'custody'):
            self.select('selected'); e = self.exchange['readback']['evidence']
            if claim == 'verified': e['artifact']['outcome'] = 'verified'
            else: e['artifact']['checks']['custody']['outcome'] = 'pass'
            self.rebind_publication(); self.refused('verified/custody claim')
        self.select('selected'); self.exchange['readback']['evidence']['standing'] = 'verified-pin'
        self.refused('verified or unsupported standing')

    def test_transport_member_omission_cannot_hide_existing_closure_member(self):
        e = self.exchange['readback']['evidence']; e['transport']['entries'].pop()
        path = self.case / 'publication' / e['reference']['transport']['path']; path.write_bytes(encoded(e['transport']))
        e['reference']['transport']['sha256'] = receiver.sha(path.read_bytes())
        for member in self.exchange['members']:
            if member['path'] == e['reference']['transport']['path']:
                member.update(sha256=receiver.sha(path.read_bytes()), size=path.stat().st_size)
        self.refused('transport closure differs')

    def test_selected_unselected_source_association_and_false_digest_refuse(self):
        e = self.exchange['readback']['evidence']
        e['transport']['sourceAssociation']['expectedReference']['sha256'] = '0' * 64
        self.rebind_publication(); self.refused('anchor refs differ|unresolved artifact')
        self.select('unselected'); self.exchange['selectedSourceMembers'] = []; self.refused('unselected source association')
        self.select('selected'); self.exchange['case'] = 'unselected'; self.refused('unselected source association')

    def test_candidate_build_pin_and_existing_review_change_negatives(self):
        self.exchange['applicationCandidate']['buildIdentity'] = 'other'; self.refused('candidate/support join')
        self.exchange['applicationCandidate']['buildIdentity'] = 'INVENTED-S4-APP-BUILD'
        self.exchange['applicationCandidate']['revision'] = 'other'; self.refused('candidate/support join')
        self.select('selected'); e = self.exchange['readback']['evidence']; e['artifact']['pin'] = 'OTHER'
        self.rebind_publication(); self.refused('pin differs|pin/support join')
        self.select('selected')
        selected = receiver.parse(self.selection.read_bytes())
        ref = selected['artifacts']['review']['record']; path = self.record_root / ref['path']
        record = receiver.parse(path.read_bytes()); record['reviewer']['identity'] = 'OTHER'
        path.write_bytes(encoded(record)); ref['sha256'] = receiver.sha(path.read_bytes())
        binding_ref = selected['artifacts']['review']['binding']; binding_path = self.record_root / binding_ref['path']
        binding_path.write_bytes(encoded(self.receiver.canonical.binding('review', path.read_bytes(), selected['binding_purpose'])))
        binding_ref['sha256'] = receiver.sha(binding_path.read_bytes()); self.selection.write_bytes(encoded(selected))
        self.refused('REVIEW-REVIEWER')

    def test_resigned_missing_selected_dependency_and_malformed_references_refuse(self):
        # Remove an opaque leaf from BOTH copies and every transport manifest.
        # The retained expected reference still names it, so correspondence fails.
        name = 'evidence/expected/0.json'
        (self.case / 'publication' / name).unlink()
        (self.case / 'selected-source' / name).unlink()
        self.exchange['selectedSourceMembers'] = [m for m in self.exchange['selectedSourceMembers'] if m['path'] != name]
        self.rebind_publication(); self.refused('unresolved artifact reference')
        for malformed in (None, {}, {'path': 'reference/expected.json', 'sha256': '0' * 64}):
            self.select('selected')
            self.exchange['readback']['evidence']['transport']['sourceAssociation']['expectedReference'] = malformed
            self.rebind_publication(); self.refused()

    def test_pinned_sources_and_pin_file_refuse_drift(self):
        with patch.object(receiver, 'PINS_SHA256', '0' * 64):
            with self.assertRaisesRegex(ValueError, 'pins changed'): receiver.Receiver()
        original = receiver.relative
        def changed(root, path):
            raw = original(root, path)
            return raw + b'\n' if path.endswith('distribution_s1.rs') else raw
        with patch.object(receiver, 'relative', changed):
            with self.assertRaisesRegex(ValueError, 'selected source changed'): receiver.Receiver()

    def test_historical_cohort_is_preserved_but_not_active(self):
        provenance = receiver.parse((HISTORICAL / 'provenance.json').read_bytes())
        for case in ('selected', 'unselected'):
            path = HISTORICAL / case / 'exchange.json'
            self.assertEqual(receiver.sha(path.read_bytes()), provenance['exchange_sha256'][case])
            with self.assertRaisesRegex(ValueError, 'producer source revision differs'):
                self.receiver.check(path, receiver.sha(path.read_bytes()), self.selection,
                                    receiver.sha(self.selection.read_bytes()))
        old = receiver.parse((HISTORICAL / 'selected/exchange.json').read_bytes())
        old['producer']['sourceRevision'] = self.receiver.pins['producer_source_revision']
        old['readback']['evidence']['unsupportedEnvelopes'] = self.receiver.pins['unsupported_envelopes']
        self.exchange = old
        self.refused('reader identity differs')

    def test_missing_mixed_and_forged_namespace_receipts_refuse(self):
        historical = receiver.parse((HISTORICAL / 'selected/exchange.json').read_bytes())
        old_reader = historical['readback']['evidence']['reference']['reader']
        for field in ('reference', 'transport'):
            for mutation in ('missing', 'forged', 'old', 'claim'):
                with self.subTest(field=field, mutation=mutation):
                    self.select('selected')
                    value = self.exchange['readback']['evidence'][field]['reader']
                    if mutation == 'missing': value.pop('namespaceAuthoritySourceSha256')
                    elif mutation == 'forged': value['namespaceAuthoritySourceSha256'] = '0' * 64
                    elif mutation == 'old': value.update(old_reader)
                    else: value['namespaceAuthorityAuthenticated'] = True
                    self.rebind_publication()
                    self.refused('reader identity differs|transport reader/boundary differs')
        self.select('selected')
        self.exchange['readback']['evidence']['reference']['namespaceAuthority'] = {'epoch': 1}
        self.refused('fields differ')

    def test_namespace_source_guard_and_non_authority_report(self):
        original = receiver.relative
        def changed(root, path):
            raw = original(root, path)
            return raw + b'\n' if path.endswith('attachment_custody.rs') else raw
        with patch.object(receiver, 'relative', changed):
            with self.assertRaisesRegex(ValueError, 'selected source changed'): receiver.Receiver()
        report = self.check()
        self.assertEqual(report['receiving_adoption'], 'B-S4-LT12-SOURCE-LT09-v1')
        self.assertFalse(report['namespace_authority_authenticated'])
        self.assertFalse(report['qualification_established'])

    def test_namespace_historical_source_and_mixed_store_identity_refuse(self):
        provenance = receiver.parse((NAMESPACE_HISTORICAL / 'provenance.json').read_bytes())
        for case in ('selected', 'unselected'):
            path = NAMESPACE_HISTORICAL / case / 'exchange.json'
            self.assertEqual(receiver.sha(path.read_bytes()), provenance['exchange_sha256'][case])
            with self.assertRaisesRegex(ValueError, 'producer source revision differs'):
                self.receiver.check(path, receiver.sha(path.read_bytes()), self.selection,
                                    receiver.sha(self.selection.read_bytes()))
        old = receiver.parse((NAMESPACE_HISTORICAL / 'selected/exchange.json').read_bytes())
        for field in ('reference', 'transport'):
            self.select('selected')
            self.exchange['readback']['evidence'][field]['reader']['storeReaderSha256'] = old['readback']['evidence'][field]['reader']['storeReaderSha256']
            self.rebind_publication()
            self.refused('reader identity differs|transport reader/boundary differs')

    def test_lt23_substitution_and_terminal_authority_claims_refuse(self):
        self.exchange['actualLt09']['transitionId'] = 'LT-23'
        self.exchange['readback']['evidence']['lifecycle']['legacy_event'] = copy.deepcopy(self.exchange['actualLt09'])
        self.rebind_publication(); self.refused('unsupported envelope|artifact shape differs')
        for target in ('exchange', 'evidence', 'reference'):
            self.select('selected')
            value = self.exchange if target == 'exchange' else self.exchange['readback']['evidence']
            if target == 'reference': value = value['reference']
            value['terminalAuthority'] = {'established': True}
            self.refused('fields differ')
        self.select('selected'); report = self.check()
        self.assertFalse(report['terminal_evidence_received'])
        self.assertFalse(report['terminal_authority_authenticated'])
        self.assertFalse(report['qualification_established'])

    def test_prior_lt23_source_and_terminal_exchange_are_not_standalone_v1(self):
        for case in ('selected', 'unselected'):
            path = LT23_SOURCE_HISTORICAL / case / 'exchange.json'
            with self.assertRaisesRegex(ValueError, 'producer source revision differs'):
                self.receiver.check(path, receiver.sha(path.read_bytes()), self.selection, receiver.sha(self.selection.read_bytes()))
        path = APP / 'tests/group_b_terminal_receiving_fixtures/selected/exchange.json'
        with self.assertRaisesRegex(ValueError, 'exchange fields differ'):
            self.receiver.check(path, receiver.sha(path.read_bytes()), self.selection, receiver.sha(self.selection.read_bytes()))

    def test_lt12_source_adoption_refuses_previous_source_mixed_reader_and_lt12(self):
        path = PREVIOUS_CURRENT / 'selected/exchange.json'
        with self.assertRaisesRegex(ValueError, 'producer source revision differs'):
            self.receiver.check(path, receiver.sha(path.read_bytes()), self.selection, receiver.sha(self.selection.read_bytes()))
        old = receiver.parse(path.read_bytes())
        self.exchange['readback']['evidence']['reference']['reader']['storeReaderSha256'] = old['readback']['evidence']['reference']['reader']['storeReaderSha256']
        self.refused('reader identity differs')
        self.select('selected')
        self.exchange['actualLt09']['transitionId'] = 'LT-12'
        self.exchange['readback']['evidence']['lifecycle']['legacy_event'] = copy.deepcopy(self.exchange['actualLt09'])
        self.rebind_publication(); self.refused('unsupported envelope')

    def test_cli_uses_actual_export_and_preserves_limits(self):
        result = subprocess.run([sys.executable, '-B', str(APP / 'examination/distribution_receiving/receive.py'),
                                 str(self.path), '--exchange-sha256', receiver.sha(self.path.read_bytes()),
                                 '--selection', str(self.selection), '--selection-sha256', receiver.sha(self.selection.read_bytes())],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout); self.assertTrue(report['file_correspondence_passed'])
        self.assertFalse(report['native_reference_authority'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
