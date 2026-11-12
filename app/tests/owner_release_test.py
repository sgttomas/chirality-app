"""The owner's signing procedure and the package identity record, on invented material.

No signing, notarization, stapling, Gatekeeper or keychain tool runs: every
Apple command goes to release_fixtures.FakeApple.
"""
import argparse
import datetime
import json
import os
from pathlib import Path
import plistlib
import shutil
import tempfile
import unittest
from unittest.mock import patch

import importlib.util
import sys

_spec = importlib.util.spec_from_file_location('release_fixtures', Path(__file__).resolve().parent / 'release_fixtures.py')
fx = importlib.util.module_from_spec(_spec); sys.modules['release_fixtures'] = fx; _spec.loader.exec_module(fx)
owner, record, common = fx.release('owner_sign'), fx.release('record'), fx.common
Result = common.Result
HOST = ('Darwin', 'arm64')
ENV = {'HOME': '/invented-home', 'PATH': '/usr/bin'}


class OwnerSign(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.candidate = fx.candidate(self.root)
        private = self.root / 'owner-private'; private.mkdir()
        self.profile = private / 'invented.provisionprofile'
        self.profile.write_bytes(fx.profile_bytes())
        self.limitations = self.root / 'RELEASE_LIMITATIONS_4.0.0.md'
        self.limitations.write_bytes(fx.LIMITATIONS)
        self.out = self.root / 'signed'
        self.fake = fx.FakeApple()

    def args(self, **changes):
        values = dict(identity=fx.IDENTITY, notary_profile=fx.NOTARY, candidate=str(self.candidate), profile=str(self.profile),
                      profile_sha256=fx.sha(self.profile.read_bytes()), limitations=str(self.limitations), out=str(self.out), dry_run=False)
        values.update(changes)
        return argparse.Namespace(**values)

    def sign(self, environ=ENV, host=HOST, **changes):
        return owner.sign(self.args(**changes), runner=self.fake, environ=environ, host=host,
                          now=datetime.datetime(2026, 11, 12))

    def log(self):
        return [json.loads(line) for line in (self.out / 'log.jsonl').read_text().splitlines()]

    @staticmethod
    def signing_calls(argvs):
        return [a for a in argvs if a[0] == owner.CODESIGN and '--sign' in a]

    def assert_signing_shape(self, argvs):
        signing = self.signing_calls(argvs)
        self.assertEqual(len(signing), 2)
        self.assertTrue(signing[0][-1].endswith('/staging/' + common.APP_NAME))
        self.assertTrue(signing[1][-1].endswith('.dmg'))
        for argv in signing:
            self.assertFalse({'--deep', '--force', '-f'} & set(argv))
            self.assertNotIn('Resources/codex', argv[-1])
        self.assertEqual(signing[0][1:8], ['--sign', fx.IDENTITY, '--options', 'runtime', '--timestamp', '--entitlements',
                                           str(self.out / 'entitlements.plist')])
        self.assertFalse(any('Resources/codex' in a[-1] and a[0] == owner.CODESIGN and '--sign' in a for a in argvs))

    def test_dry_run_prints_the_exact_plan_and_runs_nothing(self):
        result = self.sign(dry_run=True)
        self.assertEqual(self.fake.calls, [])
        self.assertFalse(self.out.exists())
        argvs = [step['argv'] for step in result['plan']]
        self.assert_signing_shape(argvs)
        self.assertIn([owner.XCRUN, 'stapler', 'staple', str(self.out / 'Chirality-4.0.0.dmg')], argvs)
        self.assertFalse(any(a[0] == owner.XCRUN and a[1] == 'stapler' and a[-1].endswith('.app') for a in argvs))
        self.assertFalse(any('/Applications' in ' '.join(a) or '/Library/' in ' '.join(a) for a in argvs))

    def test_full_run_follows_the_plan_and_writes_a_record_that_checks(self):
        plan = [step['argv'] for step in self.sign(dry_run=True)['plan']]
        result = self.sign()
        executed = [entry['argv'] for entry in self.log()]
        expected = [[('01234567-89ab-cdef-0123-456789abcdef' if w == '<submission-id>' else w) for w in a] for a in plan]
        self.assertEqual(executed, expected)
        self.assert_signing_shape(executed)
        self.assertFalse(result['installed'])
        app = self.out / 'staging' / common.APP_NAME
        placed = app / 'Contents/embedded.provisionprofile'
        self.assertEqual(os.stat(placed).st_mode & 0o7777, 0o644)
        self.assertEqual(fx.sha(placed.read_bytes()), fx.sha(self.profile.read_bytes()))
        self.assertEqual(plistlib.loads((self.out / 'entitlements.plist').read_bytes()),
                         {'com.apple.application-identifier': fx.TEAM + '.com.chirality.app', 'com.apple.developer.team-identifier': fx.TEAM})
        self.assertEqual((self.out / 'staging' / 'Release Limitations.md').read_bytes(), fx.LIMITATIONS)
        identity = json.loads((self.out / 'PACKAGE_IDENTITY.json').read_text())
        self.assertEqual(identity['package']['sha256'], fx.sha((self.out / 'Chirality-4.0.0.dmg').read_bytes()))
        self.assertEqual(identity['observed']['bundle']['name'], 'Chirality.app')
        self.assertEqual(identity['observed']['limitations']['disk_image'], {'sha256': fx.sha(fx.LIMITATIONS), 'equal_to_candidate_source': True})
        self.assertEqual(identity['observed']['limitations']['bundle'], {'sha256': fx.sha(fx.LIMITATIONS), 'equal_to_candidate_source': True})
        self.assertEqual(identity['observed']['provisioning_profile']['app_id'], fx.TEAM + '.com.chirality.app')
        self.assertEqual(identity['notarization']['status'], 'Accepted')
        self.assertIn('not_observed', identity)
        mounted = fx.make_mount_copy(self.out / 'staging', self.root / 'mounted')
        self.assertEqual(record.check(identity, dmg=self.out / 'Chirality-4.0.0.dmg', app=mounted / common.APP_NAME, run=self.fake), [])
        self.assertFalse((self.out / 'mount' / common.APP_NAME).exists())

    def test_refusals_run_no_command(self):
        cases = {
            'malformed identity': dict(identity='Invented Publisher'),
            'path-like identity': dict(identity='/Users/someone/cert.p12'),
            'hash identity': dict(identity='0123456789abcdef0123456789abcdef01234567'),
            'other team': dict(identity='Developer ID Application: Invented Publisher (OTHER00001)'),
            'credential notary profile': dict(notary_profile='abcd-efgh-ijkl-mnop'),
            'e-mail notary profile': dict(notary_profile='someone@example.com'),
            'key file path': dict(profile=str(self.root / 'key.p12')),
            'output in Applications': dict(out='/Applications/Chirality-signing'),
            'profile digest': dict(profile_sha256='0' * 64),
            'limitations differ': dict(limitations=str(self.candidate / 'publisher/publisher-requirement.txt')),
        }
        for name, changes in cases.items():
            with self.subTest(name), self.assertRaises(owner.Stop) as stop:
                self.sign(**changes)
            self.assertEqual(stop.exception.step, 'refused')
        for name, environ in {'Apple variable': ENV | {'APPLE_ID': 'x'}, 'notary variable': ENV | {'NOTARY_PASSWORD': 'x'},
                              'Tauri signing': ENV | {'TAURI_SIGNING_PRIVATE_KEY': 'x'}}.items():
            with self.subTest(name), self.assertRaises(owner.Stop):
                self.sign(environ=environ)
        with self.assertRaises(owner.Stop):
            self.sign(host=('Darwin', 'x86_64'))
        self.out.mkdir()
        with self.assertRaisesRegex(owner.Stop, 'already exists'):
            self.sign()
        self.out.rmdir()
        vendor_file = self.candidate / 'target/release/bundle/macos' / common.APP_NAME / 'Contents/Resources/codex/codex-resources/input.txt'
        vendor_file.write_bytes(b'changed')
        with self.assertRaisesRegex(owner.Stop, 'candidate description does not verify'):
            self.sign()
        self.assertEqual(self.fake.calls, [])
        self.assertFalse(self.out.exists())

    def failing(self, words, result, step, **fake):
        for key, value in fake.items():
            setattr(self.fake, key, value)
        if words:
            self.fake.override[words] = result
        with self.assertRaises(owner.Stop) as stop:
            self.sign()
        self.assertTrue(stop.exception.step.startswith(step), stop.exception)
        return stop.exception, [entry['argv'] for entry in self.log()]

    def test_each_failing_step_stops_with_no_later_command(self):
        cases = [
            (('--sign', '--entitlements'), Result(1), '4', None),
            (('--verify', '--deep'), Result(1), '5', None),
            (('-R',), Result(3), '5', None),
            (('create',), Result(1), '6', None),
            (('--verify', 'DMG'), Result(1), '6', None),
            (('notarytool', 'submit'), Result(1), '7', None),
            (('stapler', 'staple'), Result(1), '8', None),
            (('-t', 'open'), Result(3, b'', b'rejected\n'), '9', None),
            (('-t', 'exec'), Result(3, b'', b'rejected\n'), '9', 'detach'),
        ]
        for words, result, step, after in cases:
            with self.subTest(words=words):
                self.setUp()
                words = tuple(str(self.out / 'Chirality-4.0.0.dmg') if w == 'DMG' else w for w in words)
                _, executed = self.failing(words, result, step)
                failing = max(i for i, a in enumerate(executed) if all(w in a for w in words))
                rest = executed[failing + 1:]
                if after:
                    self.assertEqual([a[1] for a in rest], ['detach'])
                else:
                    self.assertEqual(rest, [])

    def test_supplier_signature_problems_stop_with_the_clm_002_question(self):
        for problem in ({'flags': '0x0(none)'}, {'timestamp': 'Signed Time=Jan 1, 2026'}, {'team': 'OTHER00001'},
                        {'entitlements': {'com.apple.security.get-task-allow': True}}):
            with self.subTest(problem=problem):
                self.setUp()
                stop, executed = self.failing(None, None, '0', supplier={'rg': problem})
                self.assertIn('CLM-002', stop.reason)
                self.assertTrue(all(a[0] == owner.CODESIGN and '--sign' not in a for a in executed))
                self.assertFalse((self.out / 'staging').exists())

    def test_notarization_rejected_with_issues_or_other_digest_is_never_stapled(self):
        for name, fake in {'rejected': dict(submit_extra={'status': 'Invalid'}),
                           'issues': dict(log_changes={'issues': [{'severity': 'error', 'path': 'x'}]}),
                           'digest': dict(log_changes={'sha256': '0' * 64}),
                           'other job': dict(log_changes={'jobId': 'ffffffff-89ab-cdef-0123-456789abcdef'})}.items():
            with self.subTest(name):
                self.setUp()
                stop, executed = self.failing(None, None, '7', **fake)
                self.assertIn('nothing is stapled', stop.reason)
                self.assertFalse(any(a[0] == owner.XCRUN and a[1] == 'stapler' for a in executed))
                self.assertEqual(executed[-1][1], 'notarytool')

    def test_signed_entitlements_other_than_the_two_keys_stop(self):
        self.fake.app_entitlements_override = plistlib.dumps({'com.apple.application-identifier': fx.TEAM + '.com.chirality.app',
                                                              'com.apple.developer.team-identifier': fx.TEAM,
                                                              'com.apple.security.get-task-allow': True})
        stop, _ = self.failing(None, None, '5')
        self.assertIn('exactly the two', stop.reason)

    def test_profile_for_another_app_id_stops_before_signing(self):
        self.profile.write_bytes(fx.profile_bytes(identifier='com.example.other'))
        with self.assertRaises(owner.Stop) as stop:
            self.sign(profile_sha256=fx.sha(self.profile.read_bytes()))
        self.assertEqual(stop.exception.step, '2 profile')
        self.assertEqual(self.signing_calls([e['argv'] for e in self.log()]), [])

    def test_copy_check_catches_changed_modes(self):
        real = shutil.copytree
        def careless(src, dst, *args, **kw):
            done = real(src, dst, *args, **kw)
            if Path(dst).name == common.APP_NAME:
                os.chmod(Path(dst) / 'Contents/Resources/codex/bin', 0o700)
            return done
        with patch.object(owner.shutil, 'copytree', careless):
            with self.assertRaises(owner.Stop) as stop:
                self.sign()
        self.assertEqual(stop.exception.step, '1 copy')
        self.assertIn('codex/bin', stop.exception.reason)

    def test_guard_refuses_forbidden_signing_calls(self):
        app, dmg = self.root / 'x' / common.APP_NAME, self.root / 'x.dmg'
        for argv in ([owner.CODESIGN, '--sign', 'n', '--deep', str(app)], [owner.CODESIGN, '--sign', 'n', '--force', str(app)],
                     [owner.CODESIGN, '--sign', 'n', str(app / 'Contents/Resources/codex/bin/codex')],
                     [owner.CODESIGN, '--sign', 'n', str(app / 'Contents/MacOS/chirality-app-v4')]):
            with self.subTest(argv=argv), self.assertRaises(owner.Stop):
                owner.guard(argv, app, dmg, [])
        signed = []
        owner.guard([owner.CODESIGN, '--sign', 'n', str(app)], app, dmg, signed)
        with self.assertRaises(owner.Stop):
            owner.guard([owner.CODESIGN, '--sign', 'n', str(app)], app, dmg, signed)

    def test_no_credential_looking_value_reaches_the_log(self):
        secrets = ['abcd-efgh-ijkl-mnop', '-----BEGIN PRIVATE KEY-----\nMIIEvQ\n-----END PRIVATE KEY-----', 'someone@example.com',
                   'password=hunter2hunter2']
        self.fake.submit_extra = {'message': ' '.join(secrets)}
        self.sign()
        text = (self.out / 'log.jsonl').read_text() + (self.out / 'PACKAGE_IDENTITY.json').read_text() + (self.out / 'RESULT.json').read_text()
        for secret in secrets:
            self.assertNotIn(secret.splitlines()[0], text)
        self.assertNotIn('hunter2', text)
        self.assertIn(fx.IDENTITY, text)
        self.assertIn(fx.NOTARY, text)

    def test_main_prints_stop_and_writes_no_package_after_failure(self):
        self.fake.override[('stapler', 'staple')] = Result(1)
        argv = ['--identity', fx.IDENTITY, '--notary-profile', fx.NOTARY, '--candidate', str(self.candidate), '--profile', str(self.profile),
                '--profile-sha256', fx.sha(self.profile.read_bytes()), '--limitations', str(self.limitations), '--out', str(self.out)]
        with patch('sys.stderr') as stderr:
            code = owner.main(argv, runner=self.fake, environ=ENV, host=HOST, now=datetime.datetime(2026, 11, 12))
        self.assertEqual(code, 3)
        self.assertIn('STOP: 8 staple:', ''.join(c.args[0] for c in stderr.write.call_args_list))
        self.assertEqual(json.loads((self.out / 'STOPPED.json').read_text())['step'], '8 staple')
        self.assertFalse((self.out / 'RESULT.json').exists())


class RecordCheck(unittest.TestCase):
    """`check` reports each kind of difference between a package and its record."""

    def setUp(self):
        self.case = OwnerSign('test_full_run_follows_the_plan_and_writes_a_record_that_checks')
        self.case.setUp(); self.addCleanup(self.case.temp.cleanup)
        self.case.sign()
        self.out = self.case.out
        self.identity = json.loads((self.out / 'PACKAGE_IDENTITY.json').read_text())
        self.dmg = self.out / 'Chirality-4.0.0.dmg'
        self.mounted = fx.make_mount_copy(self.out / 'staging', self.case.root / 'mounted')
        self.app = self.mounted / common.APP_NAME

    def differences(self, run=None):
        return record.check(self.identity, dmg=self.dmg, app=self.app, run=run or self.case.fake)

    def assert_found(self, prefix, run=None):
        found = self.differences(run)
        self.assertTrue(found and all(any(f.startswith(p) for p in ([prefix] if isinstance(prefix, str) else prefix)) for f in found), found)

    def test_unchanged_package_has_no_difference(self):
        self.assertEqual(self.differences(), [])

    def test_package_bytes(self):
        with open(self.dmg, 'ab') as handle: handle.write(b'x')
        self.assert_found('package.s')

    def test_vendor_file(self):
        (self.app / 'Contents/Resources/codex/codex-resources/input.txt').write_bytes(b'changed')
        self.assert_found('observed.vendor.')

    def test_bundled_resource(self):
        (self.app / 'Contents/Resources/instructions/roles.json').write_text('{"roles": ["x"]}')
        self.assert_found(['observed.resources.instructions', 'observed.roles_sha256'])

    def test_bundle_identity(self):
        (self.app / 'Contents/Info.plist').write_bytes(fx.info_plist(CFBundleShortVersionString='4.0.1'))
        self.assert_found('observed.bundle.')

    def test_signer_entitlements(self):
        self.case.fake.app_entitlements_override = plistlib.dumps({'com.apple.security.get-task-allow': True})
        self.assert_found('observed.signatures..')

    def test_supplier_signer(self):
        self.case.fake.supplier = {'codex': {'team': 'OTHER00001'}}
        self.assert_found('observed.signatures.Contents/Resources/codex/bin/codex')

    def test_profile(self):
        (self.app / 'Contents/embedded.provisionprofile').write_bytes(fx.profile_bytes(team='OTHER00001', prefix='OTHER00001'))
        self.assert_found('observed.provisioning_profile.')

    def test_limitations_copies(self):
        (self.mounted / 'Release Limitations.md').unlink()
        (self.app / 'Contents/Resources/release/LIMITATIONS.md').write_bytes(b'other text')
        found = self.differences()
        self.assertTrue(any(f.startswith('observed.limitations.disk_image') for f in found))
        self.assertTrue(any(f.startswith('observed.limitations.bundle') for f in found))
        self.assertTrue(any(f.startswith('observed.resources.release') for f in found))

    def test_stapled_ticket_and_gatekeeper(self):
        fake = self.case.fake
        fake.override[('stapler', 'validate')] = Result(65)
        fake.override[('-t', 'open')] = Result(3, b'', b'rejected\nsource=Unnotarized Developer ID\n')
        found = self.differences()
        self.assertTrue(any(f.startswith('observed.stapled_ticket') for f in found))
        self.assertTrue(any(f.startswith('observed.gatekeeper_disk_image') for f in found))

    def test_absent_limitations_are_recorded_as_not_observed(self):
        (self.app / 'Contents/Resources/release/LIMITATIONS.md').unlink()
        (self.mounted / 'Release Limitations.md').unlink()
        facts = record.observe(self.dmg, self.app, self.case.fake, fx.sha(fx.LIMITATIONS))
        self.assertEqual(facts['limitations'], {'bundle': 'not observed: absent', 'disk_image': 'not observed: absent'})


if __name__ == '__main__':
    unittest.main()
