"""Invented metadata only: no real profiles, certificates, keychain, signing or builds."""
import datetime as dt
import hashlib
import importlib.util
import json
from pathlib import Path
import plistlib
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec); spec.loader.exec_module(value)
    return value


subject = load('seal_c_preparation', HERE / 'prepare.py')
fixtures = load('seal_c_existing_publisher_fixture', ROOT / 'app/packaging/successor/fixtures.py')


class Preparation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.evidence = self.root / 'evidence'
        self.fixture = fixtures.Fixture(self.evidence)
        self.plan = self.root / 'package-plan'; self.plan.mkdir()
        self.output = self.root / 'output'
        self.wrapper = self.fixture.values['binding.json']
        self.publisher = self.fixture.values[self.wrapper['publisher_input']['path']]
        config = self.fixture.values[self.wrapper['tauri_config']['path']]
        config['version'] = '4.0.0'
        config.setdefault('bundle', {})['macOS'] = {'minimumSystemVersion': '15.0', 'signingIdentity': None}
        config['bundle']['resources'] = {'/synthetic/vendor/': 'codex/'}
        self.config = config
        files = {'tauri.package-inputs.conf.json': config, 'build-recipe.json': {'not_executed': True},
                 'input-inventory.json': {'publisher_input': self.wrapper['publisher_input'], 'source_revision': 'a'*40}}
        complete = {}
        for name, value in files.items():
            raw = (json.dumps(value) + '\n').encode(); (self.plan / name).write_bytes(raw); complete[name] = subject.sha(raw)
        (self.plan / 'PLAN_COMPLETE.json').write_text(json.dumps({'files': complete}))
        self.certificate = b'INVENTED public DER fixture, never a real identity'
        cert = self.fixture.put_raw('signer.der', self.certificate)
        self.profile = {'UUID': 'INVENTED-PROFILE', 'Platform': ['OSX'], 'ProvisionsAllDevices': True,
                        'CreationDate': dt.datetime(2026, 1, 1), 'ExpirationDate': dt.datetime(2027, 1, 1),
                        'TeamIdentifier': [self.publisher['developer_id_team_identifier']],
                        'ApplicationIdentifierPrefix': ['PREFIX0001'],
                        'DeveloperCertificates': [self.certificate],
                        'Entitlements': {'com.apple.application-identifier': 'PREFIX0001.' + self.publisher['production_bundle_identifier'],
                                         'com.apple.developer.team-identifier': self.publisher['developer_id_team_identifier'],
                                         'keychain-access-groups': ['PREFIX0001.*']}}
        self.request = {'format': subject.FORMAT, 'namespace': {'service': 'invalid.example.seal', 'account': 'installation-keyring', 'access_group': None},
                        'publisher_input': self.wrapper['publisher_input'], 'publisher_artifacts': None,
                        'profile_plist': self.fixture.put_raw('profile.plist', plistlib.dumps(self.profile)),
                        'profile_cms': self.fixture.put_raw('profile.cms', b'INVENTED CMS, never authenticated'), 'signer_certificate': cert}
        self.args = {'evidence_root': self.evidence, 'package_plan': self.plan, 'output': self.output,
                     'trusted_signer_sha1': hashlib.sha1(self.certificate).hexdigest(), 'assessed_at': '2026-11-01T00:00:00Z'}

    def run_plan(self):
        self.fixture.put('request.json', self.request)
        return subject.prepare(self.evidence / 'request.json', **self.args)

    def changed_profile(self):
        self.request['profile_plist'] = self.fixture.put_raw('profile.plist', plistlib.dumps(self.profile))

    def test_profile_backed_proposal_uses_prefix_not_team_and_never_grants_authority(self):
        result = self.run_plan(); self.assertFalse(result['activation_authorized'])
        ent = plistlib.loads((self.output / 'entitlements.proposed.plist').read_bytes())
        self.assertEqual(ent[subject.GROUPS], ['PREFIX0001.' + self.publisher['production_bundle_identifier']])
        self.assertNotIn('com.apple.security.cs.allow-jit', ent)
        self.assertNotIn('com.apple.security.get-task-allow', ent)
        report = json.loads((self.output / 'signing-plan.json').read_bytes())
        self.assertFalse(report['profile_metadata_authenticated']); self.assertFalse(report['secitem_executed'])
        self.assertIn('original/public', report['remaining'][0])
        self.assertEqual(subject.check_output(self.output)['files'], result['files'])
        (self.output / 'entitlements.proposed.plist').write_bytes(b'changed')
        with self.assertRaises(ValueError): subject.check_output(self.output)

    def test_default_application_group_needs_no_extra_sharing_entitlement(self):
        del self.profile['Entitlements'][subject.GROUPS]; self.changed_profile()
        self.run_plan()
        proposal = plistlib.loads((self.output / 'entitlements.proposed.plist').read_bytes())
        self.assertEqual(set(proposal), {subject.APP_ID, subject.TEAM})
        report = json.loads((self.output / 'signing-plan.json').read_text())
        self.assertEqual(report['namespace_proposal']['access_group'], proposal[subject.APP_ID])
        self.assertEqual(report['group_route'], 'default-application-identifier-group')
        self.assertFalse(report['keychain_activation_authorized'])

    def test_missing_profile_or_certificate_reports_exact_gap_without_plist(self):
        for field in ('profile_plist', 'profile_cms', 'signer_certificate'):
            with self.subTest(field=field):
                prior = self.request[field]; self.request[field] = None
                self.args['output'] = self.root / ('output-' + field)
                result = self.run_plan()
                self.assertEqual(result['metadata_state'], 'required-metadata-missing')
                self.assertFalse((self.args['output'] / 'entitlements.proposed.plist').exists())
                self.request[field] = prior

    def test_profile_scope_class_validity_development_and_signer_mismatches_refuse(self):
        baseline = plistlib.loads(plistlib.dumps(self.profile))
        cases = [('Platform', ['iOS']), ('ProvisionsAllDevices', False), ('TeamIdentifier', ['OTHER00000']),
                 ('ApplicationIdentifierPrefix', []), ('ExpirationDate', dt.datetime(2025, 1, 1)),
                 ('DeveloperCertificates', [b'other']), ('ProvisionedDevices', ['device'])]
        for key, value in cases:
            with self.subTest(key=key):
                self.profile = dict(baseline, **{key: value}); self.changed_profile()
                with self.assertRaises(ValueError): self.run_plan()
                self.assertFalse(self.output.exists())
        for key, value in [(subject.APP_ID, '*'), (subject.GROUPS, ['OTHER00000.*']),
                           ('com.apple.security.get-task-allow', True), (subject.TEAM, 'OTHER00000')]:
            with self.subTest(entitlement=key):
                self.profile = dict(baseline, Entitlements=dict(baseline['Entitlements'], **{key: value}))
                self.changed_profile()
                with self.assertRaises(ValueError): self.run_plan()

    def test_exact_input_and_plan_digests_refuse_mutation_symlink_and_unknown_fields(self):
        self.request['namespace']['extra'] = 'authority'
        with self.assertRaises(ValueError): self.run_plan()
        del self.request['namespace']['extra']
        profile = self.evidence / 'profile.plist'; original = profile.read_bytes(); profile.write_bytes(original + b' ')
        with self.assertRaises(ValueError): self.run_plan()
        profile.unlink(); (self.evidence / 'aliased.plist').write_bytes(original); profile.symlink_to('aliased.plist')
        with self.assertRaises(OSError): self.run_plan()
        profile.unlink(); profile.write_bytes(original)
        (self.plan / 'INCOMPLETE.txt').write_text('interrupted')
        with self.assertRaises(ValueError): self.run_plan()

    def test_untrusted_fingerprint_and_default_none_plan_cannot_be_promoted(self):
        self.args['trusted_signer_sha1'] = '0'*40
        with self.assertRaises(ValueError): self.run_plan()
        self.args['trusted_signer_sha1'] = hashlib.sha1(self.certificate).hexdigest()
        account = self.plan / 'input-inventory.json'; account.write_text(json.dumps({'publisher_input': None}))
        marker = json.loads((self.plan / 'PLAN_COMPLETE.json').read_text())
        marker['files'][account.name] = subject.sha(account.read_bytes()); (self.plan / 'PLAN_COMPLETE.json').write_text(json.dumps(marker))
        with self.assertRaises(ValueError): self.run_plan()

    def test_explicit_invalid_group_and_empty_cms_do_not_fall_back(self):
        for group in ('', 'OTHER00000.group', 'PREFIX0001.*'):
            self.request['namespace']['access_group'] = group
            with self.assertRaises(ValueError): self.run_plan()
        self.request['namespace']['access_group'] = None
        self.request['profile_cms'] = self.fixture.put_raw('profile.cms', b'')
        with self.assertRaises(ValueError): self.run_plan()

    def test_contradiction_dominates_missing_cms_and_duplicate_plist_refuses(self):
        self.request['profile_cms'] = None
        self.profile['TeamIdentifier'] = ['OTHER00000']; self.changed_profile()
        with self.assertRaises(ValueError): self.run_plan()
        raw = b'<?xml version="1.0"?><plist version="1.0"><dict><key>UUID</key><string>a</string><key>UUID</key><string>b</string></dict></plist>'
        self.request['profile_plist'] = self.fixture.put_raw('profile.plist', raw)
        with self.assertRaises(ValueError): self.run_plan()

    def test_failed_publication_remains_incomplete_and_never_overwrites(self):
        actual = subject.package.write_new
        def fail(path, raw):
            if path.name == 'witness-sequence.json': raise OSError('synthetic disk failure')
            return actual(path, raw)
        with patch.object(subject.package, 'write_new', side_effect=fail):
            with self.assertRaises(OSError): self.run_plan()
        self.assertTrue((self.output / 'INCOMPLETE.txt').exists())
        with self.assertRaises(ValueError): subject.check_output(self.output)
        with self.assertRaises(ValueError): self.run_plan()

    def test_existing_publisher_checker_is_used_with_original_public_and_effective_config(self):
        # Rebind invented existing fixture to the exact planned effective config;
        # no synthetic record is labelled authenticated or used by runtime.
        wrapper = self.wrapper
        config_ref = self.fixture.put(wrapper['tauri_config']['path'], self.config)
        binding = self.fixture.values[wrapper['publisher_binding']['path']]
        binding['build_context']['application_version'] = '4.0.0'
        binding['build_context']['tauri_config_sha256'] = subject.sha(subject.successor.canonical(self.config))
        binding['build_context_sha256'] = subject.sha(subject.successor.canonical(binding['build_context']))
        original = self.fixture.put(wrapper['publisher_binding']['path'], binding)
        projection = self.fixture.values[wrapper['publisher_projection']['path']]
        projection['original_binding_sha256'] = original['sha256']
        for key in binding:
            if key.endswith('_sha256'): projection[key] = binding[key]
        public = self.fixture.put(wrapper['publisher_projection']['path'], projection)
        self.request['publisher_artifacts'] = {'publisher_binding': original, 'publisher_projection': public,
                   'publisher_requirement': wrapper['publisher_requirement'], 'tauri_config': config_ref}
        self.args['trusted_publisher_sha256'] = original['sha256']
        self.run_plan()
        report = json.loads((self.output / 'signing-plan.json').read_text())
        self.assertEqual(report['independent_publisher_digest'], original['sha256'])
        self.assertFalse(report['keychain_activation_authorized'])
        self.args['output'] = self.root / 'wrong-binding'
        self.args['trusted_publisher_sha256'] = public['sha256']
        with self.assertRaises(ValueError): self.run_plan()


if __name__ == '__main__': unittest.main()

