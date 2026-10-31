"""Approved terms receiving, with invented mutations and no external operations."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
APP = ROOT / 'app'
BASE = ROOT / 'execution/PKG-09/DEL-09-01/Work/support-identity-v1'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load('terms_canonical_tests', APP / 'examination/support_identity/canonical.py')
condition = load('terms_condition_tests', APP / 'examination/support_identity/terms_condition.py')
old = load('terms_old_projection_tests', APP / 'examination/documentary_condition.py')
fixtures = load('terms_binding_fixtures', APP / 'tests/group_b_support_identity_canonical_test.py')


def encoded(value):
    return (json.dumps(value, indent=2)+'\n').encode()


class TermsSuccessorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.manifest = json.loads((BASE / 'documentary-condition.v3.json').read_bytes())
        for source in self.manifest['sources']:
            self.copy(source['path'])
        for path in self.manifest['terms_adoption']['artifacts']:
            self.copy(path)
        self.support = canonical.CanonicalSupport(documentary_root=self.root)

    def copy(self, name):
        target = self.root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / canonical.deliverable_path(ROOT, name)).read_bytes())

    def read(self, root, name):
        return (root / name).read_bytes()

    def capture(self, manifest=None):
        return condition.Condition(self.root, encoded(manifest or self.manifest), self.read).capture('sq')

    def test_current_explicit_identity_and_no_release_inference(self):
        _, report = self.capture()
        self.assertEqual(report['method'], condition.METHOD)
        self.assertEqual(report['terms_adoption']['recorded_applicability'], 'accepted')
        self.assertEqual(report['terms_adoption']['distribution_decision'], 'not_made')
        self.assertFalse(report['terms_adoption']['release_authorized'])
        self.assertFalse(report['authority_authenticated'])
        records, _ = fixtures.selection_for(self.support)
        binding = self.support.binding('result', encoded(records['before']), 'current_producer_declaration')
        self.assertEqual(binding['format'], 'exp-support-binding.canonical.terms-v1')
        self.assertEqual(binding['documentary_selection']['manifest_sha256'], canonical.sha((BASE/'documentary-condition.v3.json').read_bytes()))

    def test_every_terms_input_missing_or_tampered_refuses(self):
        for name in self.manifest['terms_adoption']['artifacts']:
            path=self.root/name; raw=path.read_bytes()
            with self.subTest(path=name):
                path.unlink()
                with self.assertRaises(FileNotFoundError): self.capture()
                path.write_bytes(raw+b'\n')
                with self.assertRaisesRegex(ValueError, 'terms adoption source changed'): self.capture()
                path.write_bytes(raw)

    def test_wrong_actor_scope_unapproved_and_release_claim_refuse(self):
        name=self.manifest['terms_adoption']['record']
        raw=(self.root/name).read_bytes()
        for mutate in (lambda r:r.update(state='unresolved'),
                       lambda r:r.update(distribution_decision={'decision':'release'}),
                       lambda r:r['scope'].update(offering='hosted commercial fixture'),
                       lambda r:r['owner_disposition'].update(actor='agent fixture'),
                       lambda r:r.update(format='chirality.distribution-terms-position/v99')):
            value=json.loads(raw);mutate(value);(self.root/name).write_bytes(encoded(value))
            with self.assertRaisesRegex(ValueError,'terms adoption source changed'):self.capture()
        (self.root/name).write_bytes(raw)
        # Even an artificial test-only rehash does not waive the actor/scope rules.
        approval_name=json.loads(raw)['owner_disposition']['approval']['path']
        original_approval=json.loads((self.root/approval_name).read_bytes())
        for mutate in (lambda a:a.update(actor_role='agent'),
                       lambda a:a['scope'].update(offering='hosted commercial fixture'),
                       lambda a:a.update(release_authorized=True),
                       lambda a:a['approved_proposal'].update(revision='0'*40)):
            approval=copy.deepcopy(original_approval);mutate(approval)
            altered=encoded(approval);(self.root/approval_name).write_bytes(altered)
            record=json.loads(raw);record['owner_disposition']['approval']['sha256']=canonical.sha(altered)
            altered_record=encoded(record);(self.root/name).write_bytes(altered_record)
            manifest=copy.deepcopy(self.manifest)
            manifest['terms_adoption']['artifacts'][name]=canonical.sha(altered_record)
            manifest['terms_adoption']['artifacts'][approval_name]=canonical.sha(altered)
            with self.subTest(approval=approval):
                with self.assertRaisesRegex(ValueError,'actor, scope or applicability'):self.capture(manifest)

    def test_unknown_missing_or_old_manifest_refuses(self):
        for key,value in [('method','selected-documentary-source-condition/v99'),('format','documentary-source-condition/2')]:
            manifest=copy.deepcopy(self.manifest);manifest[key]=value
            with self.assertRaisesRegex(ValueError,'unknown documentary'):self.capture(manifest)
        manifest=copy.deepcopy(self.manifest);manifest.pop('terms_adoption')
        with self.assertRaises(KeyError):self.capture(manifest)
        with self.assertRaisesRegex(ValueError,'unknown documentary'):
            condition.Condition(self.root,(BASE/'documentary-condition.v2.json').read_bytes(),self.read)

    def test_selected_manifest_missing_or_modified_refuses_before_receiving(self):
        for name, data in self.support.captured.items():
            target=self.root/name; target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
        manifest_path=next(name for name in self.support.captured if name.endswith('documentary-condition.v3.json'))
        target=self.root/manifest_path; raw=target.read_bytes()
        for altered in (None, raw+b'\n'):
            if altered is None:target.unlink()
            else:target.write_bytes(altered)
            with patch.object(canonical,'PROJECT',self.root):
                # Missing files retain the existing OSError refusal; altered
                # bytes raise the selected-source ValueError. Both fail closed.
                with self.assertRaises((OSError, ValueError)):
                    canonical.CanonicalSupport()

    def test_retained_reader_bytes_match_their_recorded_identities(self):
        archive=APP/'examination/support_identity/frozen/documentary-v2'
        index=json.loads((archive/'index.json').read_bytes())
        for name,digest in index['sources'].items():
            with self.subTest(path=name):
                self.assertEqual(canonical.sha((archive/name).read_bytes()),digest)

    def test_old_projection_has_its_own_truthful_subject(self):
        manifest=json.loads((BASE/'documentary-condition.v2.json').read_bytes())
        source=next(s for s in manifest['sources'] if s['path'].endswith('/PACKAGING_AND_DISTRIBUTION.md'))
        historical=(APP/'examination/support_identity/frozen/documentary-v2/packaging-before-terms.md').read_bytes()
        self.assertEqual(canonical.sha(old.project(historical,source['selectors'])),source['sha256'])
        with self.assertRaisesRegex(ValueError,'documentary meaning changed'):
            old.Condition(self.root,encoded(manifest),self.read).capture('sq')
        (self.root/source['path']).write_bytes(historical)
        old.Condition(self.root,encoded(manifest),self.read).capture('sq')
        with self.assertRaisesRegex(ValueError,'documentary meaning changed'):self.capture()

    def test_cross_version_sidecars_cannot_claim_current_meaning(self):
        records,selected=fixtures.selection_for(self.support)
        path=fixtures.write_bundle(self.root,self.support,records,selected)
        role=selected['artifacts']['review']['binding'];binding_path=self.root/role['path']
        current=json.loads(binding_path.read_bytes())
        for mutate in (lambda b:b.update(format='exp-support-binding.canonical.v1'),
                       lambda b:b.pop('documentary_selection'),
                       lambda b:b['documentary_selection'].update(manifest_sha256='0'*64),
                       lambda b:b['documentary_selection'].update(method=old.METHOD)):
            value=copy.deepcopy(current);mutate(value);binding_path.write_bytes(encoded(value));role['sha256']=canonical.sha(binding_path.read_bytes());path.write_bytes(encoded(selected))
            with self.assertRaisesRegex(ValueError,'invalid canonical binding'):
                self.support.check(path,canonical.sha(path.read_bytes()))
        historical=self.support.binding('review',encoded(records['review']),'historical_correspondence')
        self.assertEqual(historical['format'],'exp-support-binding.canonical.v1')
        self.assertNotIn('documentary_selection',historical)
        for name in self.manifest['terms_adoption']['artifacts']:(self.root/name).unlink()
        self.support.binding('review',encoded(records['review']),'historical_correspondence')
        with self.assertRaises(FileNotFoundError):
            self.support.binding('review',encoded(records['review']),'current_producer_declaration')
