"""Offline tests of invented terms/owner evidence; no authority follows from fixtures."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location('terms_position', ROOT / 'app/packaging/terms/check.py')
reader = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(reader)


class TermsPosition(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.scope = {'offering': 'INVENTED local free app', 'platform': 'test macOS',
                      'sign_in_flow': 'INVENTED managed login', 'implementation_revision': 'a' * 40,
                      'includes_first_public_distribution': True}
        self.capture = {'supplier': 'Example supplier', 'sha256': 'b' * 64,
                        'requested_url': 'https://learn.chatgpt.com/example',
                        'resolved_url': 'https://learn.chatgpt.com/example', 'http_status': 200,
                        'content_type': 'text/html', 'last_modified': None, 'bytes': 100,
                        'publication_date_note': 'INVENTED unknown date', 'capture_method': 'INVENTED',
                        'full_response_custody': 'INVENTED path never read', 'standing': 'INVENTED',
                        'retrieved_at': '2026-10-30T10:00:00Z', 'publication_date': None,
                        'capture_actor': 'Example recorder',
                        'excerpts': [{'section': 'INVENTED section', 'html': '<p>INVENTED statement</p>', 'text': 'INVENTED statement',
                                      'html_sha256': reader.digest(b'<p>INVENTED statement</p>')}]}
        self.write('capture.json', self.capture)
        (self.root / 'proposal.md').write_text('INVENTED proposal; not an owner act')
        self.answer = {'format': 'chirality.terms-owner-answer/v1', 'created_by': 'user',
                       'recorded_timestamp': '2026-10-30T11:00:00Z', 'thread': 'invented-thread',
                       'message_id': 'invented-owner-message',
                       'content': 'INVENTED proposal ' + 'c' * 40 + '\nApprove example applicability'}
        self.write('answer.json', self.answer)
        self.approval = {'format': 'chirality.terms-applicability-disposition/v1',
                         'purpose': 'terms_applicability_only', 'actor': 'Example owner',
                         'actor_role': 'owner', 'act': 'received_adopted_retained_evidence',
                         'decided_at': self.answer['recorded_timestamp'], 'source_kind': 'official_publication',
                         'supplier': 'Example supplier', 'content': self.ref('capture.json'),
                         'full_content_sha256': 'b' * 64, 'scope': copy.deepcopy(self.scope),
                         'conditions': ['INVENTED condition'], 'exclusions': ['INVENTED exclusion'],
                         'approved_proposal': {'revision': 'c' * 40, 'artifact': self.ref('proposal.md')},
                         'owner_answer': self.ref('answer.json'), 'answer': 'Approve example applicability',
                         'applicability': 'accepted', 'release_authorized': False}
        self.write('approval.json', self.approval)
        self.record = {'format': 'chirality.distribution-terms-position/v1', 'record_id': 'INVENTED',
                       'supplier': 'Example supplier', 'state': 'applicable_position_retained',
                       'scope': copy.deepcopy(self.scope),
                       'position': {'kind': 'official_publication', 'supplier': 'Example supplier',
                                    'source_url': self.capture['requested_url'], 'publication_or_response_date': None,
                                    'retrieved_or_received_at': self.capture['retrieved_at'],
                                    'captured_by': 'Example recorder', 'content': self.ref('capture.json'),
                                    'full_content_sha256': 'b' * 64, 'conditions': ['INVENTED condition'],
                                    'exclusions': ['INVENTED exclusion'], 'custody': 'INVENTED fixture only'},
                       'owner_disposition': {'actor': 'Example owner', 'act': 'received_adopted_retained_evidence',
                                             'approval': self.ref('approval.json')},
                       'distribution_decision': 'not_made', 'recorded_by': 'Example recorder',
                       'recorded_at': '2026-10-30T12:00:00Z', 'limits': ['Synthetic, no authority']}

    def write(self, name, value):
        (self.root / name).write_text(json.dumps(value) + '\n')

    def ref(self, name):
        return {'path': name, 'sha256': reader.digest((self.root / name).read_bytes())}

    def save_approval(self):
        self.write('approval.json', self.approval)
        self.record['owner_disposition']['approval'] = self.ref('approval.json')

    def check(self):
        self.write('record.json', self.record)
        return reader.check('record.json', self.root)

    def refuses(self):
        with self.assertRaises((ValueError, ValidationError, KeyError, OSError)):
            self.check()

    def test_publication_and_unresolved_are_separate_from_release(self):
        result = self.check()
        self.assertEqual(result['recorded_state'], 'applicable_position_retained')
        self.assertFalse(result['release_authorized'])
        self.assertFalse(result['distribution_decision_recorded'])
        self.record.update(state='unresolved', owner_disposition=None)
        self.assertEqual(self.check()['recorded_state'], 'unresolved')
        self.record['position'] = None
        self.assertEqual(self.check()['source_kind'], None)

    def test_direct_response_is_explicit_and_does_not_change_publication(self):
        response = {'format': 'chirality.supplier-response-capture/v1', 'supplier': 'Example supplier',
                    'source_url': 'https://example.invalid/invented-response', 'received_at': '2026-10-30T10:00:00Z',
                    'response_date': '2026-10-29', 'captured_by': 'Example recorder',
                    'response_text': 'INVENTED direct response', 'sha256': reader.digest(b'INVENTED direct response')}
        self.write('response.json', response)
        self.record['position'].update(kind='direct_response', source_url=response['source_url'],
                                       publication_or_response_date=response['response_date'],
                                       content=self.ref('response.json'), full_content_sha256=response['sha256'])
        self.approval.update(source_kind='direct_response', content=self.ref('response.json'),
                             full_content_sha256=response['sha256'])
        self.save_approval()
        self.assertEqual(self.check()['source_kind'], 'direct_response')
        self.record['position']['kind'] = 'official_publication'
        self.refuses()

    def test_approved_state_requires_owner_event_and_content(self):
        for field in ('owner_disposition', 'position'):
            with self.subTest(field=field):
                original = self.record[field]
                self.record[field] = None
                self.refuses()
                self.record[field] = original

    def test_recorder_cannot_be_owner_even_with_case_or_whitespace(self):
        self.record['owner_disposition']['actor'] = ' EXAMPLE RECORDER '
        self.approval['actor'] = ' EXAMPLE RECORDER '
        self.save_approval()
        self.refuses()

    def test_supplier_cannot_capture_or_record(self):
        self.record['position']['captured_by'] = 'Example supplier'
        self.refuses()

    def test_future_owner_capture_is_not_forbidden_or_inferred_for_current_input(self):
        self.record['position']['captured_by'] = 'Example owner'
        self.refuses()  # current captured evidence names the recorder, not the owner
        self.capture['capture_actor'] = 'Example owner'
        self.write('capture.json', self.capture)
        self.record['position']['content'] = self.ref('capture.json')
        self.approval['content'] = self.ref('capture.json')
        self.save_approval()
        self.assertFalse(self.check()['release_authorized'])

    def test_scope_cannot_be_widened_from_selected_offering(self):
        for key, value in [('offering', 'paid hosted service'), ('includes_first_public_distribution', False),
                           ('implementation_revision', 'd' * 40)]:
            with self.subTest(key=key):
                original = self.record['scope'][key]
                self.record['scope'][key] = value
                self.refuses()
                self.record['scope'][key] = original

    def test_conditions_exclusions_supplier_kind_and_hash_must_join(self):
        for key, value in [('conditions', ['altered']), ('exclusions', ['removed exclusion']),
                           ('supplier', 'Different supplier'), ('source_kind', 'direct_response'),
                           ('full_content_sha256', '0' * 64)]:
            with self.subTest(key=key):
                old = self.approval[key]
                self.approval[key] = value
                self.save_approval()
                self.refuses()
                self.approval[key] = old
        self.save_approval()

    def test_capture_tamper_and_malformed_excerpt_refuse(self):
        self.capture['excerpts'][0]['text'] = 'Different statement'
        self.write('capture.json', self.capture)
        self.refuses()  # digest mismatch
        self.record['position']['content'] = self.ref('capture.json')
        self.approval['content'] = self.ref('capture.json')
        self.save_approval()
        self.refuses()  # even with fresh hashes, HTML/text mismatch

    def test_dates_and_owner_event_are_not_inferred(self):
        self.approval['decided_at'] = '2026-10-30T09:00:00Z'
        self.answer['recorded_timestamp'] = self.approval['decided_at']
        self.write('answer.json', self.answer)
        self.approval['owner_answer'] = self.ref('answer.json')
        self.save_approval()
        self.refuses()  # adoption before capture
        self.record['recorded_at'] = '2026-02-30T12:00:00Z'
        self.refuses()

    def test_agent_message_cannot_replace_owner_answer(self):
        self.answer['created_by'] = 'agent'
        self.write('answer.json', self.answer)
        self.approval['owner_answer'] = self.ref('answer.json')
        self.save_approval()
        self.refuses()

    def test_different_answer_or_proposal_cannot_satisfy_approval(self):
        self.approval['answer'] = 'Approve public release'
        self.save_approval()
        self.refuses()
        self.approval['answer'] = 'Approve example applicability'
        self.approval['approved_proposal']['revision'] = 'd' * 40
        self.save_approval()
        self.refuses()

    def test_release_requires_distinct_event_and_never_grants_authority(self):
        self.record['distribution_decision'] = {'actor': 'Example owner', 'evidence': self.ref('approval.json')}
        self.refuses()
        release = {'format': 'chirality.public-distribution-decision/v1', 'purpose': 'public_distribution_decision',
                   'actor': 'Example owner', 'actor_role': 'owner', 'decided_at': '2026-10-30T11:00:00Z',
                   'scope': self.scope, 'decision': 'approved', 'owner_answer': self.ref('answer.json'),
                   'answer': 'Approve example applicability'}
        self.write('release.json', release)
        self.record['distribution_decision']['evidence'] = self.ref('release.json')
        self.refuses()  # same answer cannot serve both acts
        other = dict(self.answer, content='INVENTED release question\nApprove example release')
        self.write('release-answer.json', other)
        release['owner_answer'] = self.ref('release-answer.json')
        release['answer'] = 'Approve example release'
        self.write('release.json', release)
        self.record['distribution_decision']['evidence'] = self.ref('release.json')
        self.refuses()  # different bytes do not make the same message a separate act
        other['message_id'] = 'different-owner-message'
        self.write('release-answer.json', other)
        release['owner_answer'] = self.ref('release-answer.json')
        self.write('release.json', release)
        self.record['distribution_decision']['evidence'] = self.ref('release.json')
        result = self.check()
        self.assertTrue(result['distribution_decision_recorded'])
        self.assertFalse(result['release_authorized'])

    def test_paths_symlinks_hardlinks_special_and_bounds_refuse(self):
        for path in ('../capture.json', '/capture.json', './capture.json', 'x//capture.json'):
            self.record['position']['content']['path'] = path
            self.refuses()
        self.record['position']['content']['path'] = 'link.json'
        (self.root / 'link.json').symlink_to('capture.json')
        self.refuses()
        os.link(self.root / 'capture.json', self.root / 'hard.json')
        self.record['position']['content']['path'] = 'hard.json'
        self.refuses()
        os.mkfifo(self.root / 'pipe')
        self.record['position']['content']['path'] = 'pipe'
        self.refuses()
        (self.root / 'large').write_bytes(b'x' * (reader.MAX_BYTES + 1))
        self.record['position']['content']['path'] = 'large'
        self.refuses()

    def test_duplicate_unknown_fields_versions_and_legacy_refuse(self):
        self.record['format'] = 'PKG-v0.2'
        self.refuses()
        self.record['format'] = 'chirality.distribution-terms-position/v2'
        self.refuses()
        self.record['format'] = 'chirality.distribution-terms-position/v1'
        self.record['qualified'] = True
        self.refuses()
        with self.assertRaises(ValueError):
            reader.parse(b'{"state":"unresolved","state":"applicable_position_retained"}')

    def test_schema_itself_and_real_record_consistency(self):
        schema = reader.parse(reader.SCHEMA.read_bytes())
        reader.Draft202012Validator.check_schema(schema)
        result = reader.check('execution/PKG-01/DEL-01-06/Work/terms-position-v1/OpenAI.json', ROOT)
        self.assertFalse(result['release_authorized'])
        self.assertFalse(result['distribution_decision_recorded'])

    def test_legacy_reader_keeps_original_closed_meaning(self):
        work = ROOT / 'execution/PKG-01/DEL-01-06/Work'
        legacy_schema = reader.parse((work / 'pkg.terms-record.schema.json').read_bytes())
        legacy_record = reader.parse((work.parent / 'Evidence/PKG/terms/OpenAI.json').read_bytes())
        validator = reader.Draft202012Validator(legacy_schema)
        validator.validate(legacy_record)
        self.assertEqual(legacy_record['state'], 'unresolved')
        with self.assertRaises(ValidationError):
            validator.validate(self.record)

    def test_cli_invalid_record_exits_nonzero(self):
        self.record['state'] = 'approved_for_release'
        self.write('record.json', self.record)
        run = subprocess.run([sys.executable, str(ROOT / 'app/packaging/terms/check.py'),
                              '--record', 'record.json', '--evidence-root', str(self.root)],
                             capture_output=True, text=True)
        self.assertEqual(run.returncode, 2, run.stderr)
        self.assertEqual(json.loads(run.stdout)['standing'], 'refused')


if __name__ == '__main__':
    unittest.main()
