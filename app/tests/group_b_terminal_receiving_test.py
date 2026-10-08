"""Real synthetic terminal export pairs; no native or terminal integrity claim."""
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
PREVIOUS_CURRENT = APP / 'tests/group_b_terminal_receiving_fixtures'
COMBINED_PREDECESSOR = APP / 'tests/group_b_lt12_source_terminal_fixtures'
FIXTURES = APP / 'tests/group_b_lt12_combined_terminal_fixtures'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module


subject = load('_terminal_test_subject', APP / 'examination/distribution_receiving/terminal.py')
base = subject.base
records = load('_terminal_invented_records', APP / 'tests/group_b_distribution_receiving_fixtures/records.py')


def encoded(value):
    return (json.dumps(value, indent=2) + '\n').encode()


class TerminalReceivingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=Path(tempfile.gettempdir()).resolve())
        self.addCleanup(self.temp.cleanup); self.root = Path(self.temp.name)
        self.receiver = subject.TerminalReceiver(); self.select('selected')

    def select(self, case):
        self.case = self.root / 'case'
        if self.case.exists(): shutil.rmtree(self.case)
        shutil.copytree(FIXTURES / case, self.case)
        self.path = self.case / 'exchange.json'; self.exchange = base.parse(self.path.read_bytes())
        record_root = self.root / 'records'; record_root.mkdir(exist_ok=True)
        self.selection = records.write(record_root, self.receiver.canonical, self.exchange['applicationCandidate'])

    def check(self):
        self.path.write_bytes(encoded(self.exchange))
        return self.receiver.check(self.path, base.sha(self.path.read_bytes()), self.selection, base.sha(self.selection.read_bytes()))

    def refused(self, pattern='.'):
        with self.assertRaisesRegex((ValueError, OSError), pattern): self.check()

    def rebind(self, role='terminal'):
        value = self.exchange[role]; e = value['readback']['evidence']; ref = e['reference']; root = self.case / role / 'publication'
        def put(artifact, value):
            path = root / artifact['path']; original = path.read_bytes()
            raw = original if base.parse(original) == value else encoded(value)
            path.write_bytes(raw); artifact['sha256'] = base.sha(raw)
        put(ref['observed'], e['artifact'])
        e['lifecycle']['verification_artifact'] = copy.deepcopy(ref['observed'])
        put(ref['lifecycle'], e['lifecycle'])
        e['transport']['entries'] = [{'path': p.relative_to(root).as_posix(), 'sha256': base.sha(p.read_bytes())}
                                     for p in sorted(root.rglob('*')) if p.is_file() and p.relative_to(root).as_posix() != ref['transport']['path']]
        put(ref['transport'], e['transport'])
        value['members'] = [{'path': p.relative_to(root).as_posix(), 'sha256': base.sha(p.read_bytes()), 'size': p.stat().st_size}
                            for p in sorted(root.rglob('*')) if p.is_file()]

    def test_actual_selected_unselected_pairs_and_full_canonical_join(self):
        provenance = base.parse((FIXTURES / 'provenance.json').read_bytes())
        for case in ('selected', 'unselected'):
            self.select(case); raw = self.path.read_bytes()
            self.assertEqual(base.sha(raw), provenance['exchange_sha256'][case])
            report = self.receiver.check(self.path, base.sha(raw), self.selection, base.sha(self.selection.read_bytes()))
            self.assertTrue(report['terminal_pair_file_correspondence_passed'])
            self.assertEqual(report['exported_event_pair'], ['LT-09', 'LT-23'])
            self.assertEqual(set(report['predecessor_canonical_join']['canonical_support']['existing_checks']), {'package', 'review', 'change'})
            for key in ('native_reference_authority', 'namespace_authority_authenticated', 'terminal_integrity_established',
                        'terminal_authority_authenticated', 'semantic_reader_reexecuted', 'producer_history_authenticated',
                        'application_build_authenticated', 'qualification_established'):
                self.assertFalse(report[key])

    def test_every_original_publication_and_source_byte_is_bound(self):
        for role in ('predecessor', 'terminal'):
            for entry in self.exchange[role]['members']:
                p = self.case / role / 'publication' / entry['path']; raw = p.read_bytes()
                p.write_bytes(raw + b'\n'); self.refused('member bytes differ'); p.write_bytes(raw)
        for entry in self.exchange['selectedSourceMembers']:
            p = self.case / 'selected-source' / entry['path']; raw = p.read_bytes()
            p.write_bytes(raw + b'\n'); self.refused('member bytes differ'); p.write_bytes(raw)

    def test_rehashed_observation_reference_and_shared_closure_changes_refuse(self):
        self.exchange['terminal']['readback']['evidence']['artifact']['at'] = 'CHANGED'
        self.rebind(); self.refused('observation bytes/reference differ')
        self.select('selected'); p = self.case / 'terminal/publication/evidence/expected/0.json'
        p.write_bytes(b'changed opaque evidence'); self.rebind(); self.refused('shared closure bytes differ')

    def test_same_generation_event_sequence_and_actual_event_joins(self):
        for field in ('generation', 'sequence', 'transitionId'):
            self.select('selected'); event = self.exchange['terminal']['actualLt23']
            if field == 'generation': event['generation']['spawnCounter'] += 1
            elif field == 'sequence': event['sequence'] = self.exchange['predecessor']['actualLt09']['sequence']
            else: event['transitionId'] = 'LT-22'
            self.exchange['terminal']['readback']['evidence']['lifecycle']['legacy_event'] = copy.deepcopy(event)
            self.rebind(); self.refused('mixed terminal generation|sequence not increasing|unsupported terminal event|shape differs')
        self.select('selected'); self.exchange['terminal']['actualLt23']['at'] = 'different'; self.refused('event/reference differs')

    def test_distinct_publication_source_and_reader_identity(self):
        e = self.exchange['terminal']['readback']['evidence']; old = self.exchange['predecessor']['readback']['evidence']
        e['reference']['publication'] = old['reference']['publication']; self.refused('must be distinct')
        self.select('selected'); e = self.exchange['terminal']['readback']['evidence']
        e['transport']['sourceAssociation']['originalSource'] = 'other'; self.rebind(); self.refused('association differs')
        self.select('selected'); self.exchange['terminal']['readback']['evidence']['reference']['reader']['storeReaderSha256'] = '0'*64
        self.refused('reader identity differs')

    def test_malformed_missing_refs_and_duplicate_manifest(self):
        for ref in (None, {}, {'path':'absent','sha256':'0'*64}):
            self.select('selected'); self.exchange['terminal']['readback']['evidence']['reference']['lifecycle'] = ref; self.refused()
        self.select('selected'); self.exchange['terminal']['members'].append(self.exchange['terminal']['members'][0]); self.refused('duplicate member')
        self.select('selected'); self.exchange['terminal']['members'].pop(); self.refused('inventory differs')

    def test_pending_unavailable_and_diagnostic_markers_refuse(self):
        for state in ('pending', 'queued', 'unavailable'):
            self.select('selected'); self.exchange['terminal']['readback']['state'] = state; self.refused('unavailable or pending')
        self.select('selected'); diagnostic = self.case / 'exchange.diagnostic.json'; self.path.rename(diagnostic)
        with self.assertRaisesRegex(ValueError, 'completed exchange.json'):
            self.receiver.check(diagnostic, base.sha(diagnostic.read_bytes()), self.selection, base.sha(self.selection.read_bytes()))
        diagnostic.rename(self.path); (self.root / 'DIAGNOSTIC_SOURCE.json').write_text('{}'); self.refused('diagnostic marker')
        (self.root / 'DIAGNOSTIC_SOURCE.json').unlink(); (self.case / 'queued.marker').write_text('queued'); self.refused('inventory differs')

    def test_false_terminal_native_and_verified_authority_refuse(self):
        for area in ('top', 'evidence', 'reference'):
            self.select('selected'); value = self.exchange if area == 'top' else self.exchange['terminal']['readback']['evidence']
            if area == 'reference': value = value['reference']
            value['terminalAuthority'] = True; self.refused('fields differ')
        self.select('selected'); e = self.exchange['terminal']['readback']['evidence']; e['standing'] = 'verified-pin'; self.refused('standing/boundary differs')
        self.select('selected'); e = self.exchange['predecessor']['readback']['evidence']; e['artifact']['checks']['custody']['outcome'] = 'pass'; self.rebind('predecessor'); self.refused('verified/custody claim')

    def test_paths_links_extra_members_and_duplicate_json_refuse(self):
        entry = self.exchange['terminal']['members'][0]; entry['path'] = '../outside'; self.refused('noncontained')
        self.select('selected'); p = self.case / 'terminal/publication' / self.exchange['terminal']['members'][0]['path']
        other = self.root / 'outside'; other.write_bytes(p.read_bytes()); p.unlink(); p.symlink_to(other); self.refused()
        self.select('selected'); (self.case / 'terminal/publication/extra').write_text('x'); self.refused('inventory differs')
        self.select('selected'); raw = b'{"format":"duplicate",' + self.path.read_bytes()[1:]; self.path.write_bytes(raw)
        with self.assertRaisesRegex(ValueError, 'duplicate JSON'):
            self.receiver.check(self.path, base.sha(raw), self.selection, base.sha(self.selection.read_bytes()))

    def test_stale_format_source_candidate_and_selection_controls(self):
        self.exchange['format'] = 'group-b-s1-reader-exchange.v1'; self.refused('unsupported terminal')
        self.select('selected'); self.exchange['producer']['sourceRevision'] = '5c9aabcfb400bab3ef1e283362dc378414621da7'; self.refused('source revision differs')
        self.select('selected'); self.exchange['applicationCandidate']['buildIdentity'] = 'OTHER'; self.refused('candidate/support join')
        self.select('selected'); digest = base.sha(self.path.read_bytes()); self.path.write_bytes(self.path.read_bytes()+b'\n')
        with self.assertRaisesRegex(ValueError, 'exchange digest mismatch'):
            self.receiver.check(self.path,digest,self.selection,base.sha(self.selection.read_bytes()))

    def test_standalone_v1_and_cross_source_predecessor_are_not_terminal_pairs(self):
        path = APP / 'tests/group_b_distribution_receiving_terminal_source_fixtures/selected/exchange.json'
        with self.assertRaisesRegex(ValueError, 'terminal exchange fields differ'):
            self.receiver.check(path,base.sha(path.read_bytes()),self.selection,base.sha(self.selection.read_bytes()))
        old = base.parse((APP / 'tests/group_b_distribution_receiving_lt23_source_fixtures/selected/exchange.json').read_bytes())
        self.exchange['predecessor']['readback']['evidence']['reference'] = old['readback']['evidence']['reference']
        self.refused()

    def test_lt12_source_adoption_refuses_previous_source_mixed_reader_and_lt12(self):
        prior = COMBINED_PREDECESSOR / 'selected/exchange.json'
        with self.assertRaisesRegex(ValueError, 'producer source revision differs'):
            self.receiver.check(prior, base.sha(prior.read_bytes()), self.selection, base.sha(self.selection.read_bytes()))
        path = PREVIOUS_CURRENT / 'selected/exchange.json'
        with self.assertRaisesRegex(ValueError, 'producer source revision differs'):
            self.receiver.check(path,base.sha(path.read_bytes()),self.selection,base.sha(self.selection.read_bytes()))
        old = base.parse(path.read_bytes())
        self.exchange['terminal']['readback']['evidence']['reference']['reader']['storeReaderSha256'] = old['terminal']['readback']['evidence']['reference']['reader']['storeReaderSha256']
        self.refused('terminal reader identity differs')
        for role,key in [('predecessor','actualLt09'),('terminal','actualLt23')]:
            self.select('selected'); event = self.exchange[role][key]; event['transitionId'] = 'LT-12'
            self.exchange[role]['readback']['evidence']['lifecycle']['legacy_event'] = copy.deepcopy(event)
            self.rebind(role); self.refused('unsupported envelope|unsupported terminal event')

    def test_terminal_source_guard_and_cli(self):
        original = base.relative
        def changed(root, path):
            raw = original(root,path)
            return raw+b'\n' if path.endswith('hosting_terminal_export.rs') else raw
        with patch.object(base,'relative',changed):
            with self.assertRaisesRegex(ValueError,'terminal selected source changed'):subject.TerminalReceiver()
        result = subprocess.run([sys.executable,'-B',str(APP/'examination/distribution_receiving/terminal.py'),str(self.path),
                                 '--exchange-sha256',base.sha(self.path.read_bytes()),'--selection',str(self.selection),
                                 '--selection-sha256',base.sha(self.selection.read_bytes())],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        self.assertFalse(json.loads(result.stdout)['terminal_integrity_established'])


if __name__ == '__main__': unittest.main(verbosity=2)
