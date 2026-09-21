"""Synthetic evidence-chain tests; no production override or supplier execution."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import root_runtime_successors as s
from root_governance_state import GovernanceError, digest


class SuccessorRecognitionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='root-successor-tests-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.decomp = 'projects/chirality-runtime/execution/_Decomposition/decomp.md'
        self.ledger = 'projects/chirality-runtime/execution/_Decomposition/ledger.csv'
        self.sow = 'projects/chirality-runtime/execution/PKG-01/ScopeOfWork.md'
        self.old = {self.decomp: b'old decomposition', self.ledger: b'old ledger',
                    self.sow: b'accepted migration SOW'}
        self.baseline = {p: hashlib.sha256(b).hexdigest() for p, b in self.old.items()}
        for p, b in self.old.items():
            self.put(p, b)
        self.changes = []
        for p, b in [(s.SUPPLEMENT, b'D36 disposition'), (self.decomp, b'new decomposition'),
                     (self.ledger, b'new ledger')]:
            self.put(p, b)
            self.changes.append({'path': p, 'before': self.baseline.get(p),
                                 'after': digest(self.root / p)})
        self.index_path = 'accepted/POSTIMAGE_INDEX.json'
        self.index = [{'target': c['path'], 'preimageSha256': c['before'],
                       'postimageSha256': c['after']} for c in self.changes]
        self.put_json(self.index_path, self.index)
        self.members = [self.ref(self.index_path)]
        # A full multi-file subject: a distant, non-index member is also mandatory.
        for i in range(60):
            p = f'accepted/evidence/{i:02}.md'
            self.put(p, f'bounded evidence {i}')
            self.members.append(self.ref(p))
        self.subject_path = 'accepted/SUBJECT.json'
        self.acceptance_path = 'accepted/OWNER_ACCEPTANCE.md'
        self.owner_path = 'root/OWNER_ACT.md'
        self.put(self.owner_path, 'Root owner accepts this exact bounded recognition policy')
        self.adoption = {'id': 'D36_STAGE1', 'changes': copy.deepcopy(self.changes),
                         'postimage_index': self.ref(self.index_path)}
        self.refresh_subject()
        self.policy_path = 'root/POLICY.json'
        self.policy = {'schema': 'root-runtime-successor-adoptions/v1',
                       'root_owner_act': self.ref(self.owner_path), 'adoptions': [self.adoption]}
        self.policy_patch = patch.object(s, 'POLICY', self.policy_path)
        self.policy_patch.start()
        self.addCleanup(self.policy_patch.stop)
        self.seal_policy()

    def put(self, path, data):
        out = self.root / path
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data if isinstance(data, bytes) else data.encode())

    def put_json(self, path, value):
        self.put(path, json.dumps(value, sort_keys=True))

    def ref(self, path):
        return {'path': path, 'sha256': digest(self.root / path)}

    def refresh_subject(self):
        self.put_json(self.subject_path, {'pathBase': 'repository root', 'files': self.members})
        self.adoption['subject'] = self.ref(self.subject_path)
        self.put(self.acceptance_path, 'Owner accepts subject ' + self.adoption['subject']['sha256'])
        self.adoption['acceptance'] = self.ref(self.acceptance_path)

    def seal_policy(self):
        # Only this unittest fixture changes the fixed policy pin; production has no input flag.
        self.put_json(self.policy_path, self.policy)
        p = patch.object(s, 'POLICY_SHA', digest(self.root / self.policy_path))
        p.start()
        self.addCleanup(p.stop)

    def recognize(self):
        return s.recognize(self.root, self.baseline)

    def test_exact_baseline_needs_no_successor_evidence(self):
        for p, b in self.old.items():
            self.put(p, b)
        (self.root / s.SUPPLEMENT).unlink()
        (self.root / self.policy_path).unlink()
        result = self.recognize()
        self.assertEqual(result['state'], 'migration-baseline')
        self.assertEqual(result['current_bindings'], self.baseline)
        self.assertEqual(result['adoptions'], [])
        self.assertIs(result['execution_authority'], False)

    def test_baseline_rejects_injected_account_supplement_without_policy(self):
        account = self.root / s.ACCOUNT_SUPPLEMENT
        for kind in ['file', 'directory', 'dangling-symlink']:
            with self.subTest(kind=kind):
                for p, b in self.old.items():
                    self.put(p, b)
                custody = self.root / s.SUPPLEMENT
                if custody.exists():
                    custody.unlink()
                policy = self.root / self.policy_path
                if policy.exists():
                    policy.unlink()
                if account.is_symlink() or account.is_file():
                    account.unlink()
                elif account.is_dir():
                    account.rmdir()
                if kind == 'file':
                    self.put(s.ACCOUNT_SUPPLEMENT, 'unaccepted account authority')
                elif kind == 'directory':
                    account.mkdir(parents=True)
                else:
                    account.parent.mkdir(parents=True, exist_ok=True)
                    account.symlink_to(account.parent / 'missing-target')
                with self.assertRaises(GovernanceError):
                    self.recognize()

    def test_exact_accepted_revision_without_main_is_not_published_or_authorized(self):
        self.assertFalse((self.root / '.git').exists())
        self.assertIs(s._verify_adoption(self.root, self.adoption), False)
        result = self.recognize()
        self.assertEqual(result['state'], 'accepted-pending-publication')
        self.assertIs(result['published'], False)
        self.assertIs(result['execution_authority'], False)
        self.assertEqual(result['adoptions'], ['D36_STAGE1'])
        self.assertEqual(result['current_bindings'][self.sow], self.baseline[self.sow])
        for c in self.changes:
            self.assertEqual(result['current_bindings'][c['path']], c['after'])

    def test_missing_or_tampered_evidence_fails(self):
        paths = [self.policy_path, self.owner_path, self.acceptance_path, self.subject_path,
                 self.index_path, 'accepted/evidence/59.md']
        for path in paths:
            original = (self.root / path).read_bytes()
            for missing in [True, False]:
                with self.subTest(path=path, missing=missing):
                    if missing:
                        (self.root / path).unlink()
                    else:
                        self.put(path, original + b' changed')
                    with self.assertRaises(GovernanceError):
                        self.recognize()
                    self.put(path, original)

    def test_changed_or_missing_live_file_and_mixed_revision_fail(self):
        for c in self.changes:
            path = c['path']
            original = (self.root / path).read_bytes()
            for data in [None, b'unaccepted revision', self.old.get(path, b'old supplement')]:
                with self.subTest(path=path, data=data):
                    if data is None:
                        (self.root / path).unlink()
                    else:
                        self.put(path, data)
                    with self.assertRaises(GovernanceError):
                        self.recognize()
                    self.put(path, original)

    def test_unaccepted_sow_is_not_hidden_by_accepted_decomposition(self):
        self.put(self.sow, 'future Stage 2 SOW without owning acceptance')
        with self.assertRaises(GovernanceError):
            self.recognize()

    def test_acceptance_must_name_exact_subject_even_when_rehashed(self):
        self.put(self.acceptance_path, 'Owner accepts another subject ' + '0' * 64)
        self.adoption['acceptance'] = self.ref(self.acceptance_path)
        self.seal_policy()
        with self.assertRaises(GovernanceError):
            self.recognize()

    def test_index_membership_and_exact_projection_are_required(self):
        for fault in ['unlisted', 'wrong-member-hash', 'wrong-before', 'wrong-after', 'wrong-target']:
            with self.subTest(fault=fault):
                adoption = copy.deepcopy(self.adoption)
                if fault == 'unlisted':
                    adoption['postimage_index']['path'] = 'accepted/not-in-subject.json'
                    self.put_json(adoption['postimage_index']['path'], self.index)
                elif fault == 'wrong-member-hash':
                    adoption['postimage_index']['sha256'] = '0' * 64
                else:
                    field = {'wrong-before': 'before', 'wrong-after': 'after',
                             'wrong-target': 'path'}[fault]
                    adoption['changes'][0][field] = 'different'
                with self.assertRaises(GovernanceError):
                    s._verify_adoption(self.root, adoption)

    def test_duplicate_and_escaping_subject_members_are_rejected(self):
        original = copy.deepcopy(self.members)
        for path in [self.members[0]['path'], '../outside.md', '/tmp/outside.md',
                     'accepted/../outside.md']:
            with self.subTest(path=path):
                self.members = original + [{'path': path, 'sha256': self.members[0]['sha256']}]
                self.refresh_subject()
                self.seal_policy()
                with self.assertRaises(GovernanceError):
                    self.recognize()

    def test_unknown_or_escaping_change_scope_is_rejected(self):
        for path in ['projects/chirality-app-dev/unknown.md', '../outside.md',
                     '/tmp/outside.md', 'projects/chirality-runtime/execution/new-unaccepted-SOW.md']:
            with self.subTest(path=path):
                self.adoption['changes'] = copy.deepcopy(self.changes) + [
                    {'path': path, 'before': None, 'after': 'a' * 64}]
                self.seal_policy()
                with self.assertRaises(GovernanceError):
                    self.recognize()

    def test_wrong_predecessor_and_duplicate_change_are_rejected(self):
        for fault in ['predecessor', 'duplicate']:
            with self.subTest(fault=fault):
                self.adoption['changes'] = copy.deepcopy(self.changes)
                if fault == 'predecessor':
                    self.adoption['changes'][0]['before'] = 'a' * 64
                else:
                    self.adoption['changes'].append(copy.deepcopy(self.changes[0]))
                self.seal_policy()
                with self.assertRaises(GovernanceError):
                    self.recognize()

    def test_subject_member_symlink_is_rejected(self):
        path = self.root / 'accepted/evidence/59.md'
        data = path.read_bytes()
        self.put('accepted/sibling.md', data)
        path.unlink()
        path.symlink_to(self.root / 'accepted/sibling.md')
        with self.assertRaises(GovernanceError):
            self.recognize()

    def test_selected_policy_preserves_prior_objects_and_verifies_account_chain(self):
        repo = Path(__file__).resolve().parents[2]
        current = json.loads((repo / ('execution/_Coordination/AgentRuns/'
                                      'ROOT_RUNTIME_ACCOUNT_AUTHORITY_ADOPTION_2026-09-07/'
                                      'SUCCESSOR_ADOPTIONS.json')).read_text())
        prior = json.loads((repo / ('execution/_Coordination/AgentRuns/'
                                     'ROOT_RUNTIME_STAGE2_ADOPTION_2026-09-07/'
                                     'SUCCESSOR_ADOPTIONS.json')).read_text())
        self.assertEqual(current['adoptions'][:2], prior['adoptions'])
        account = current['adoptions'][2]
        self.assertEqual(account['id'], 'D36_ACCOUNT_AUTHORITY')
        self.assertIsInstance(s._verify_adoption(repo, account), bool)
        self.assertEqual(
            {Path(item['path']).name: item['after'] for item in account['changes']},
            {
                'ACCOUNT_CONTROL_AUTHORITY_DISPOSITION.md':
                    '19baaea22ba3a5b2dc465c30f7e8273db7b1833fd4a9bf6c2de0fc6056dcdd9d',
                'Chirality_Runtime_SOFTWARE_DECOMP_v1_0.md':
                    '413687ca6a857f5464a3205e9f9c4b29ace512c8d2b67dfa095ef3640fab883e',
                'RUNTIME_SCOPE_LEDGER.csv':
                    'bffda2701dea3667a63f72194404db72b20520802a7d840af13ac456fb1f149d',
            })

    def test_sow_policy_preserves_prior_objects_and_verifies_runtime_pair(self):
        repo = Path(__file__).resolve().parents[2]
        current = json.loads((repo / ('execution/_Coordination/AgentRuns/'
                                      'ROOT_RUNTIME_SOW_SUCCESSOR_ADOPTION_2026-09-07/'
                                      'SUCCESSOR_ADOPTIONS.json')).read_text())
        prior = json.loads((repo / ('execution/_Coordination/AgentRuns/'
                                     'ROOT_RUNTIME_ACCOUNT_AUTHORITY_ADOPTION_2026-09-07/'
                                     'SUCCESSOR_ADOPTIONS.json')).read_text())
        self.assertEqual(current['adoptions'][:3], prior['adoptions'])
        sow = current['adoptions'][3]
        self.assertEqual(sow['id'], 'D36_RUNTIME_SOW_PROPAGATION')
        self.assertIsInstance(s._verify_adoption(repo, sow), bool)
        self.assertEqual([item['path'] for item in sow['changes']], [
            'projects/chirality-runtime/execution/PKG-02_Runtime_Product/1_Working/'
            'DEL-02-06_Generic_Runtime_Stewardship_and_Release_Assurance/ScopeOfWork.md',
            'projects/chirality-runtime/execution/PKG-02_Runtime_Product/1_Working/'
            'DEL-02-09_Hosted_Account_and_Consent_Boundary/ScopeOfWork.md',
        ])


if __name__ == '__main__':
    unittest.main()
