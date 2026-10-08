"""Invented exact-byte joined records; no actual native run or independent review."""
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
TOOL = APP / 'examination/support_identity/support_identity.py'
spec = importlib.util.spec_from_file_location('group_b_support_identity', TOOL)
identity = importlib.util.module_from_spec(spec); spec.loader.exec_module(identity)


def encoded(value):
    return (json.dumps(value, indent=2) + '\n').encode()


def fixture_records(support):
    fixtures = APP / 'tests/group_b_admission_fixtures'
    records = {k: json.loads((fixtures / (k + '.json')).read_text())
               for k in ('before', 'after', 'rerun', 'review', 'change')}
    records['package'] = json.loads((APP / 'tests/group_b_fixtures/package.json').read_text())
    for k in ('before', 'after', 'rerun'):
        r = records[k]
        r['support_revision']['prototype_digest'] = 'sha256:' + support.identity['prototype_sha256']
        r['subject']['app_candidate'].update(packaged=True, package_record='INVENTED-PACKAGE')
        r['configuration']['route'] = copy.deepcopy(json.loads((APP / 'tests/group_b_fixtures/result.json').read_text())['configuration']['route'])
    records['package']['app'].update(revision='INVENTED-REV-B', build_identity='INVENTED-BUILD-B')
    review = json.loads((fixtures / 'review-selection.json').read_text())
    change = json.loads((fixtures / 'change-selection.json').read_text())
    basis = lambda k: {f: copy.deepcopy(records[k][f]) for f in ('subject', 'configuration', 'criterion')}
    review['basis'] = basis('rerun'); change['before_basis'] = basis('before'); change['rerun_basis'] = basis('rerun')
    selection = {'format': 'exp-support-selection.v1', 'standing': 'frozen_candidate_not_published',
                 'declaration_sha256': identity.DECLARATION_SHA256, 'artifacts': {},
                 'package_selection': {'revision': 'INVENTED-REV-B', 'build': 'INVENTED-BUILD-B',
                                       'pin': '0.160.0', 'package_ref': 'INVENTED-PACKAGE'},
                 'review_selection': review, 'change_selection': change}
    return records, selection


def write_bundle(directory, support, records, selection):
    for role, kind in identity.KINDS.items():
        data = encoded(records[role])
        sidecar = encoded(support.binding(kind, data))
        pair = {}
        for label, payload in [('record', data), ('binding', sidecar)]:
            name = role + '.' + label + '.json'
            (directory / name).write_bytes(payload)
            pair[label] = {'path': name, 'sha256': identity.sha(payload)}
        selection['artifacts'][role] = pair
    selection_path = directory / 'selection.json'
    selection_path.write_bytes(encoded(selection))
    return selection_path


class SupportIdentityTests(unittest.TestCase):
    def setUp(self):
        self.support = identity.SupportIdentity()
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.records, self.selection = fixture_records(self.support)
        self.path = write_bundle(self.root, self.support, self.records, self.selection)

    def check(self):
        self.path.write_bytes(encoded(self.selection))
        return self.support.check(self.path, identity.sha(self.path.read_bytes()))

    def rebuild(self):
        write_bundle(self.root, self.support, self.records, self.selection)

    def mutate_binding(self, role, mutate):
        path = self.root / self.selection['artifacts'][role]['binding']['path']
        value = identity.parse(path.read_bytes()); mutate(value); path.write_bytes(encoded(value))
        self.selection['artifacts'][role]['binding']['sha256'] = identity.sha(path.read_bytes())

    def assert_refused(self, pattern=None):
        with self.assertRaisesRegex((ValueError, OSError), pattern or '.'):
            self.check()

    def test_composed_existing_validators_and_truthful_limits(self):
        report = self.check()
        self.assertTrue(report['identity_consistency_passed'], report['errors'])
        self.assertEqual(set(report['existing_checks']), {'package', 'review', 'change'})
        self.assertEqual(len(report['existing_checks']['package']['reported_prerequisite_gaps']), 3)
        for flag in ('publication_established', 'adoption_established', 'qualification_established'):
            self.assertFalse(report[flag])
        self.assertFalse(report['existing_checks']['review']['review_or_repair_verified'])

    def test_missing_schema_ids_and_all_mixed_support_fields_refuse(self):
        mutations = [lambda s: s['support_identity']['schema_ids'].pop('review'),
                     lambda s: s['support_identity']['schema_ids'].update(change='other:0.3'),
                     lambda s: s['support_identity'].update(exp_version='EXP-v0.3'),
                     lambda s: s['support_identity'].update(prototype_sha256='0' * 64),
                     lambda s: s.update(declaration_sha256='0' * 64)]
        for role in identity.KINDS:
            for mutate in mutations:
                with self.subTest(role=role, mutation=mutations.index(mutate)):
                    self.rebuild(); self.mutate_binding(role, mutate); self.assert_refused()

    def test_writer_cannot_publish_or_select_another_declaration(self):
        for mutate in (lambda s: s.update(standing='published'), lambda s: s.update(publication=True)):
            self.rebuild(); self.mutate_binding('review', mutate); self.assert_refused()
        self.rebuild(); self.selection['declaration_sha256'] = '0' * 64; self.assert_refused('self-selected')
        self.selection['declaration_sha256'] = identity.DECLARATION_SHA256
        self.selection['publication'] = {'approved': True}; self.assert_refused('unknown')

    def test_exact_byte_changes_and_false_digests_refuse(self):
        for role in identity.KINDS:
            self.rebuild()
            path = self.root / self.selection['artifacts'][role]['record']['path']
            path.write_bytes(path.read_bytes() + b'\n')
            self.assert_refused('digest mismatch')
            self.selection['artifacts'][role]['record']['sha256'] = identity.sha(path.read_bytes())
            self.assert_refused('artifact identity mismatch')  # Sidecar still binds original exact bytes.
        self.rebuild(); self.selection['artifacts']['review']['binding']['sha256'] = 'f' * 64
        self.assert_refused('digest mismatch')

    def test_missing_record_binding_and_duplicate_paths_refuse(self):
        self.selection['artifacts'].pop('review'); self.assert_refused('missing')
        self.rebuild(); self.selection['artifacts']['review'].pop('binding'); self.assert_refused('missing')
        self.rebuild(); self.selection['artifacts']['review']['record'] = self.selection['artifacts']['change']['record']
        self.assert_refused()

    def test_source_freeze_cannot_be_replaced_by_writer_or_missing_sources(self):
        with patch.object(identity, 'PROJECT', self.root):
            with self.assertRaises(OSError): identity.SupportIdentity()
        for relative, data in self.support.sources.items():
            p = self.root / relative; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(data)
        changed = self.root / 'app/examination/admission/sources.json'
        changed.write_bytes(changed.read_bytes() + b'\n')
        with patch.object(identity, 'PROJECT', self.root):
            with self.assertRaisesRegex(ValueError, 'frozen source changed'): identity.SupportIdentity()
        with patch.object(identity, 'DECLARATION_SHA256', '0' * 64):
            with self.assertRaisesRegex(ValueError, 'declaration changed'): identity.SupportIdentity()

    def test_declared_record_versions_and_result_digest_stay_explicit(self):
        for role in identity.KINDS:
            original = copy.deepcopy(self.records[role]); self.records[role]['format'] = 'EXP-v0.3'
            self.rebuild(); self.assert_refused('mixed record versions'); self.records[role] = original
        self.records['before']['support_revision'].pop('prototype_digest')
        self.rebuild(); self.assert_refused('support identity missing')

    def test_caller_digest_cannot_follow_changed_selection(self):
        digest = identity.sha(self.path.read_bytes())
        self.path.write_bytes(self.path.read_bytes() + b'\n')
        with self.assertRaisesRegex(ValueError, 'selection digest mismatch'):
            self.support.check(self.path, digest)

    def test_repair_history_and_candidate_package_join_remain_enforced(self):
        self.records['after']['outcome'] = 'pass'; self.rebuild()
        report = self.check(); self.assertFalse(report['identity_consistency_passed'])
        self.assertIn('CHANGE-HISTORY-MUTATED', [e['code'] for e in report['errors']])
        self.records, self.selection = fixture_records(self.support)
        self.records['package']['app']['build_identity'] = 'OTHER'; self.rebuild()
        self.assertIn('LINK-BUILD', [e['code'] for e in self.check()['errors']])

    def test_review_actor_and_cross_join_aliases_enforced(self):
        self.records['review']['reviewer']['identity'] = 'OTHER'; self.rebuild()
        self.assertIn('REVIEW-REVIEWER', [e['code'] for e in self.check()['errors']])
        self.selection['review_selection']['subject_alias'] = 'OTHER'
        self.assert_refused('target aliases differ')

    def test_unresolved_references_cannot_pass_complete_join(self):
        self.records['review']['evidence_set'].append('OTHER-UNRESOLVED'); self.rebuild()
        report = self.check(); self.assertFalse(report['identity_consistency_passed'])
        self.assertIn('UNRESOLVED-JOIN-REFERENCES', [e['code'] for e in report['errors']])

    def test_links_traversal_and_duplicate_json_refused(self):
        path = self.root / 'link.json'; path.symlink_to(self.root / 'review.record.json')
        self.selection['artifacts']['review']['record']['path'] = 'link.json'; self.assert_refused('symbolic link')
        self.selection['artifacts']['review']['record']['path'] = '../outside'; self.assert_refused('relative path')
        for data in (b'{"x":1,"x":2}', b'{"x":NaN}'):
            with self.assertRaises(ValueError): identity.parse(data)

    def test_declaration_identity_is_derived_from_actual_pinned_sources(self):
        local = self.root / 'tool'; local.mkdir()
        (local / 'binding.v1.schema.json').write_bytes((identity.HERE / 'binding.v1.schema.json').read_bytes())
        for kind in ('schema', 'prototype', 'version'):
            value = copy.deepcopy(self.support.declaration)
            if kind == 'schema': value['support_identity']['schema_ids']['review'] = 'other'
            elif kind == 'prototype': value['support_identity']['prototype_sha256'] = '0' * 64
            else: value['support_identity']['exp_version'] = 'EXP-v0.3'
            payload = encoded(value); (local / 'declaration.v1.json').write_bytes(payload)
            # Test-only repin exposes the independent source-to-value checks.
            with patch.object(identity, 'HERE', local), patch.object(identity, 'DECLARATION_SHA256', identity.sha(payload)):
                with self.assertRaisesRegex(ValueError, 'disagrees with'):
                    identity.SupportIdentity()

    def test_frozen_source_snapshot_survives_later_filesystem_drift(self):
        # The support object already captured and checked exact source bytes.
        with patch.object(identity, 'PROJECT', self.root / 'missing-project'):
            self.assertTrue(self.check()['identity_consistency_passed'])

    def test_bind_command_emits_only_unpublished_candidate_and_no_pass_claim(self):
        result = subprocess.run([sys.executable, '-B', str(TOOL), 'bind', 'review',
                                 str(self.root / 'review.record.json')], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        value = identity.parse(result.stdout)
        self.assertEqual(value['standing'], 'frozen_candidate_not_published')
        self.assertNotIn('identity_consistency_passed', value)
        self.assertEqual(value['artifact']['sha256'], self.selection['artifacts']['review']['record']['sha256'])

    def test_cli_offline_success_and_stale_selection_exit(self):
        digest = identity.sha(self.path.read_bytes())
        command = [sys.executable, '-B', str(TOOL), 'check', str(self.path), '--selection-sha256', digest]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = identity.parse(result.stdout); self.assertTrue(report['identity_consistency_passed'])
        self.path.write_bytes(self.path.read_bytes() + b'\n')
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 2); self.assertFalse(identity.parse(result.stdout)['identity_consistency_passed'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
