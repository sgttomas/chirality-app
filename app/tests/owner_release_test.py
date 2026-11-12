"""The owner's signing procedure and the package identity record, on invented material.

No signing, notarization, stapling, Gatekeeper or keychain tool runs: every
Apple command goes to release_fixtures.FakeApple.
"""
import argparse
import datetime
import importlib.util
import io
import json
import os
from pathlib import Path
import plistlib
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

_spec = importlib.util.spec_from_file_location('release_fixtures', Path(__file__).resolve().parent / 'release_fixtures.py')
fx = importlib.util.module_from_spec(_spec); sys.modules['release_fixtures'] = fx; _spec.loader.exec_module(fx)
owner, record, common = fx.release('owner_sign'), fx.release('record'), fx.common
Result = common.Result
HOST = ('Darwin', 'arm64')
ENV = {'HOME': '/invented-home', 'PATH': '/usr/bin'}
NOW = datetime.datetime(2026, 11, 12)
APP_ID, DMG_ID = fx.submission_id(1), fx.submission_id(2)
# Secret-looking values, assembled at run time so that no credential-shaped literal sits in the source.
PEM = '-----' + 'BEGIN PRIVATE KEY' + '-----\nMIIEinvented\n-----' + 'END PRIVATE KEY' + '-----'
SECRETS = ['abcd-efgh-ijkl-mnop', 'MIIEinvented', 'someone@example.com', 'invented-secret', 'QQQQ11111Q']


def is_app(argv):
    return argv[-1].endswith('.app')


class Base(unittest.TestCase):
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
        return owner.sign(self.args(**changes), runner=self.fake, environ=environ, host=host, now=NOW)

    def argv(self, notary_profile=fx.NOTARY):
        return ['--identity', fx.IDENTITY, '--notary-profile', notary_profile, '--candidate', str(self.candidate), '--profile',
                str(self.profile), '--profile-sha256', fx.sha(self.profile.read_bytes()), '--limitations', str(self.limitations),
                '--out', str(self.out)]

    def main(self, *extra, runner=None, notary_profile=fx.NOTARY):
        stdout, stderr = io.StringIO(), io.StringIO()
        code = owner.main(self.argv(notary_profile) + list(extra), stdout=stdout, stderr=stderr, runner=runner or self.fake,
                          environ=ENV, host=HOST, now=NOW)
        return code, stdout.getvalue(), stderr.getvalue()

    def log(self):
        return [json.loads(line) for line in (self.out / 'log.jsonl').read_text().splitlines()]

    def executed(self):
        return [entry['argv'] for entry in self.log()]


class OwnerSign(Base):
    @staticmethod
    def signing_calls(argvs):
        return [a for a in argvs if a[0] == owner.CODESIGN and '--sign' in a]

    def assert_shape(self, argvs):
        signing = self.signing_calls(argvs)
        self.assertEqual([Path(a[-1]).name for a in signing], ['Chirality.app', 'Chirality-4.0.0.dmg'])
        for argv in signing:
            self.assertFalse({'--deep', '--force', '-f'} & set(argv))
            self.assertNotIn('Resources/codex', argv[-1])
        self.assertEqual(signing[0][1:8], ['--sign', fx.IDENTITY, '--options', 'runtime', '--timestamp', '--entitlements',
                                           str(self.out / 'entitlements.plist')])
        submits = [Path(a[3]).name for a in argvs if a[:3] == [owner.XCRUN, 'notarytool', 'submit']]
        self.assertEqual(submits, ['Chirality-4.0.0-app.zip', 'Chirality-4.0.0.dmg'])
        staples = [Path(a[-1]).name for a in argvs if a[1:3] == ['stapler', 'staple']]
        self.assertEqual(staples, ['Chirality.app', 'Chirality-4.0.0.dmg'])
        # After the App's staple no command signs or staples the App again.
        app = str(self.out / 'staging' / common.APP_NAME)
        after = argvs[[i for i, a in enumerate(argvs) if a[1:3] == ['stapler', 'staple']][0] + 1:]
        self.assertFalse([a for a in after if a[-1] == app and ('--sign' in a or 'staple' in a)])

    def test_dry_run_prints_the_exact_plan_and_runs_nothing(self):
        code, stdout, _ = self.main('--dry-run')
        self.assertEqual(code, 0)
        self.assertEqual(self.fake.calls, [])
        self.assertFalse(self.out.exists())
        argvs = [step['argv'] for step in json.loads(stdout)['plan']]
        self.assert_shape(argvs)
        self.assertFalse(any('/Applications' in ' '.join(a) or '/Library/' in ' '.join(a) for a in argvs))

    def test_full_run_follows_the_plan_and_writes_a_record_that_checks(self):
        plan = [step['argv'] for step in self.sign(dry_run=True)['plan']]
        result = self.sign()
        ids = {'<app-submission-id>': APP_ID, '<disk-image-submission-id>': DMG_ID}
        self.assertEqual(self.executed(), [[ids.get(w, w) for w in a] for a in plan])
        self.assert_shape(self.executed())
        self.assertEqual((result['installed'], result['result']), (False, 'complete'))
        app = self.out / 'staging' / common.APP_NAME
        self.assertTrue((app / 'Contents/CodeResources').is_file())
        placed = app / 'Contents/embedded.provisionprofile'
        self.assertEqual(os.stat(placed).st_mode & 0o7777, 0o644)
        self.assertEqual(fx.sha(placed.read_bytes()), fx.sha(self.profile.read_bytes()))
        self.assertEqual(plistlib.loads((self.out / 'entitlements.plist').read_bytes()),
                         {'com.apple.application-identifier': fx.TEAM + '.com.chirality.app', 'com.apple.developer.team-identifier': fx.TEAM})
        identity = json.loads((self.out / 'PACKAGE_IDENTITY.json').read_text())
        observed = identity['observed']
        self.assertEqual(identity['package']['sha256'], fx.sha((self.out / 'Chirality-4.0.0.dmg').read_bytes()))
        self.assertEqual(observed['bundle']['name'], 'Chirality.app')
        self.assertEqual(set(observed['app_as_stapled']['inventory']['entries']) - set(observed['app_as_signed']['inventory']['entries']),
                         {'Contents/CodeResources'})
        self.assertNotEqual(observed['app_as_signed']['digest'], observed['app_as_stapled']['digest'])
        self.assertEqual(observed['stapled_tickets']['app']['validated'], True)
        self.assertEqual(observed['stapled_tickets']['disk_image']['validated'], True)
        self.assertEqual({k: v['submission_id'] for k, v in identity['notarization'].items()}, {'app': APP_ID, 'disk_image': DMG_ID})
        self.assertEqual(identity['notarization']['app']['submitted_sha256'], fx.sha((self.out / 'notary/Chirality-4.0.0-app.zip').read_bytes()))
        self.assertEqual(observed['limitations']['disk_image'], {'sha256': fx.sha(fx.LIMITATIONS), 'equal_to_candidate_source': True})
        mounted = fx.make_mount_copy(self.out / 'staging', self.root / 'mounted')
        self.assertEqual(record.check(identity, dmg=self.out / 'Chirality-4.0.0.dmg', app=mounted / common.APP_NAME,
                                      run=self.fake, record_dir=self.out), [])
        self.assertFalse((self.out / 'mount' / common.APP_NAME).exists())
        self.assertFalse((self.out / 'STOPPED.json').exists())

    def test_refusals_run_no_command(self):
        cases = {
            'malformed identity': dict(identity='Invented Publisher'),
            'path-like identity': dict(identity='/Users/someone/cert.p12'),
            'hash identity': dict(identity='0123456789abcdef0123456789abcdef01234567'),
            'other team': dict(identity='Developer ID Application: Invented Publisher (OTHER00001)'),
            'credential notary profile': dict(notary_profile='abcd-efgh-ijkl-mnop'),
            'e-mail notary profile': dict(notary_profile='someone@example.com'),
            'key file path': dict(profile=str(self.root / 'key.p12')),
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

    def test_installed_locations_are_refused_by_filesystem_identity(self):
        protected = self.root / 'Applications'; protected.mkdir()
        alias = self.root / 'apps-link'; alias.symlink_to(protected)
        cases = {'symlink to the place': alias / 'release', 'inside the place': protected / 'release'}
        (self.root / 'CaseProbe').mkdir()
        if (self.root / 'caseprobe').exists():  # case-insensitive volume: a case alias names the same directory
            cases['case alias'] = self.root / 'APPLICATIONS' / 'release'
        with patch.object(common, 'protected_places', lambda: [protected]):
            for name, out in cases.items():
                with self.subTest(name), self.assertRaisesRegex(owner.Stop, 'may not be inside'):
                    self.sign(out=str(out))
            moved = protected / 'candidate'
            shutil.copytree(self.candidate, moved, symlinks=True)
            with self.assertRaisesRegex(owner.Stop, 'may not be inside'):
                self.sign(candidate=str(alias / 'candidate'))
            with self.assertRaisesRegex(ValueError, 'may not be inside'):
                common.load_candidate(moved)
        self.assertEqual(self.fake.calls, [])
        self.assertEqual(sorted(p.name for p in protected.iterdir()), ['candidate'])

    def test_every_write_is_inside_the_output(self):
        (self.root / 'out-a').mkdir()
        session = owner.Session(self.root / 'out-a', self.fake, ENV, {'app': self.root / 'a.app', 'dmg': self.root / 'a.dmg'},
                                owner.make_redactor(fx.IDENTITY, fx.NOTARY))
        session.writable(self.root / 'out-a' / 'x')
        with self.assertRaisesRegex(ValueError, 'not inside the output'):
            session.writable(self.root / 'elsewhere.json')

    def failing(self, words, result, step, **fake):
        for key, value in fake.items():
            setattr(self.fake, key, value)
        if words:
            self.fake.override[words] = result
        code, stdout, stderr = self.main()
        self.assertEqual(code, 3, stderr)
        stopped = json.loads((self.out / 'STOPPED.json').read_text())
        self.assertTrue(stopped['step'].startswith(step + ' '), stopped)
        self.assertEqual(stopped['result'], 'stopped')
        self.assertIn(f'STOP: {stopped["step"]}:', stderr)
        self.assertFalse((self.out / 'RESULT.json').exists())
        self.assertEqual(stdout, '')
        return stopped, self.executed()

    @staticmethod
    def after_staple(result):
        def answer(argv):
            app = Path(argv[-1])
            return result if app.suffix == '.app' and (app / 'Contents/CodeResources').exists() else None
        return answer

    def test_each_failing_step_stops_with_no_later_command_and_no_result(self):
        dmg_only = lambda r: (lambda argv: r if argv[-1].endswith('.dmg') else None)
        cases = [
            (('--sign', '--entitlements'), Result(1), '4', None),
            (('--verify', '--deep'), Result(1), '5', None),
            (('-R',), Result(3), '5', None),
            (('-d', '--verbose=4'), lambda argv: Result(1) if is_app(argv) else None, '5', None),
            (('-d', '--entitlements'), lambda argv: Result(0, b'') if is_app(argv) else None, '5', None),
            ((owner.DITTO,), Result(1), '6', None),
            (('submit',), lambda argv: Result(1) if argv[3].endswith('.zip') else None, '6', None),
            (('stapler', 'staple'), lambda argv: Result(1) if is_app(argv) else None, '7', None),
            (('stapler', 'validate'), lambda argv: Result(65) if is_app(argv) else None, '7', None),
            (('--verify', '--deep'), self.after_staple(Result(1)), '8', None),
            (('create',), Result(1), '9', None),
            (('--verify', '--strict', '--verbose=4'), dmg_only(Result(1)), '9', None),
            (('-d', '--verbose=4'), dmg_only(Result(1)), '9', None),
            (('submit',), lambda argv: Result(1) if argv[3].endswith('.dmg') else None, '10', None),
            (('stapler', 'staple'), dmg_only(Result(1)), '11', None),
            (('stapler', 'validate'), dmg_only(Result(65)), '11', None),
            (('-t', 'open'), Result(3, b'', b'rejected\n'), '12', None),
            (('-t', 'exec'), Result(3, b'', b'rejected\n'), '12', 'detach'),
            (('detach',), Result(16, b'', b'resource busy\n'), '12', None),
        ]
        for words, result, step, after in cases:
            with self.subTest(words=words, step=step):
                self.setUp()
                _, executed = self.failing(words, result, step)
                answer = lambda a: (result(a) if callable(result) else result)
                failing = max(i for i, a in enumerate(executed) if all(w in a for w in words) and answer(a) is not None)
                rest = executed[failing + 1:]
                self.assertEqual([a[1] for a in rest], ['detach'] if after else [])
                if int(step) < 11:
                    self.assertFalse(any(a[1:3] == ['stapler', 'staple'] and a[-1].endswith('.dmg') for a in executed))

    def test_a_failed_observation_in_the_record_stops_with_no_result(self):
        """The reviewer's case: a ticket validation returning 65 while recording must stop, not be recorded as done."""
        in_record = lambda r: (lambda argv: r if '/mount/' in argv[-1] else None)
        for words, result in ((('stapler', 'validate'), in_record(Result(65))), (('-d', '--entitlements'), in_record(Result(1))),
                              (('-d', '--verbose=4'), in_record(Result(1)))):
            with self.subTest(words=words):
                self.setUp()
                stopped, executed = self.failing(words, result, '13')
                self.assertIn('observations failed', stopped['reason'])
                self.assertEqual(executed[-1][1], 'detach')
                self.assertFalse((self.out / 'PACKAGE_IDENTITY.json').exists())
        self.setUp()
        record_exec = lambda argv: Result(3) if sum(c[1] == 'detach' for c in self.fake.calls) == 1 else None
        stopped, _ = self.failing(('-t', 'exec'), record_exec, '13')
        self.assertIn('Gatekeeper did not accept the app', stopped['reason'])
        self.setUp()
        self.fake.override[('stapler', 'validate')] = in_record(Result(65))
        stopped, _ = self.failing(('detach',), lambda argv: Result(16) if sum(c[1] == 'detach' for c in self.fake.calls) == 2 else None, '13')
        self.assertIn('observations failed', stopped['reason'])
        self.assertIn('also did not detach', stopped['reason'])
        self.setUp()
        second_detach = lambda argv: Result(16) if sum(c[1] == 'detach' for c in self.fake.calls) == 2 else None
        stopped, _ = self.failing(('detach',), second_detach, '13')
        self.assertIn('did not detach', stopped['reason'])

    def test_supplier_signature_problems_stop_with_the_clm_002_question(self):
        for problem in ({'flags': '0x0(none)'}, {'timestamp': 'Signed Time=Jan 1, 2026'}, {'team': 'OTHER00001'},
                        {'entitlements': {'com.apple.security.get-task-allow': True}}, {'cdhash': 'CDHash-unavailable'}):
            with self.subTest(problem=problem):
                self.setUp()
                stop, executed = self.failing(None, None, '0', supplier={'rg': problem})
                self.assertIn('CLM-002', stop['reason'])
                self.assertTrue(all(a[0] == owner.CODESIGN and '--sign' not in a for a in executed))
                self.assertFalse((self.out / 'staging').exists())
        self.setUp()
        empty = lambda argv: Result(0, b'') if 'Resources/codex' in argv[-1] else None
        stop, _ = self.failing(('-d', '--entitlements'), empty, '0')
        self.assertIn('CLM-002', stop['reason'])

    def test_notarization_answers_that_are_not_clean_are_never_stapled(self):
        cases = {'rejected': dict(submit_extra={'status': 'Invalid'}),
                 'issues': dict(log_changes={'issues': [{'severity': 'error', 'path': 'x'}]}),
                 'no issues field': dict(log_changes={'issues': fx.DELETE}),
                 'digest': dict(log_changes={'sha256': '0' * 64}),
                 'other job': dict(log_changes={'jobId': 'ffffffff-89ab-cdef-0123-456789abcdef'})}
        for name, fake in cases.items():
            with self.subTest(name):
                self.setUp()
                stop, executed = self.failing(None, None, '6', **fake)
                self.assertIn('nothing is stapled', stop['reason'])
                self.assertFalse(any(a[0] == owner.XCRUN and a[1] == 'stapler' for a in executed))
                self.assertEqual(executed[-1][1], 'notarytool')
        # The same rule for the disk image's submission: a log without an issues field.
        self.setUp()
        no_issues = lambda argv: (Result(0, json.dumps({'jobId': argv[2], 'status': 'Accepted',
                                                        'sha256': fx.sha(self.fake.submissions[-1].read_bytes())}).encode())
                                  if len(self.fake.submissions) == 2 else None)
        stop, executed = self.failing(('notarytool', 'log'), no_issues, '10')
        self.assertFalse(any(a[1:3] == ['stapler', 'staple'] and a[-1].endswith('.dmg') for a in executed))

    def test_staple_may_add_only_the_ticket(self):
        def careless(argv):
            app = Path(argv[-1])
            if app.suffix == '.app':
                (app / 'Contents/CodeResources').write_bytes(b'ticket')
                (app / 'Contents/Resources/codex/codex-resources/input.txt').write_bytes(b'changed by stapling')
                return Result(0)
        stop, _ = self.failing(('stapler', 'staple'), careless, '7')
        self.assertIn('more than adding the ticket', stop['reason'])

    def test_archiving_for_submission_may_not_change_the_app(self):
        self.fake.ditto_effect = lambda app: os.chmod(app / 'Contents/Resources/codex/bin', 0o700)
        stop, executed = self.failing(None, None, '6')
        self.assertIn('archiving changed the App', stop['reason'])
        self.assertFalse(any(a[1:3] == ['notarytool', 'submit'] for a in executed))

    def test_signed_entitlements_other_than_the_two_keys_stop(self):
        self.fake.app_entitlements_override = plistlib.dumps({'com.apple.application-identifier': fx.TEAM + '.com.chirality.app',
                                                              'com.apple.developer.team-identifier': fx.TEAM,
                                                              'com.apple.security.get-task-allow': True})
        stop, _ = self.failing(None, None, '5')
        self.assertIn('exactly the two', stop['reason'])

    def test_profile_for_another_app_id_stops_before_signing(self):
        self.profile.write_bytes(fx.profile_bytes(identifier='com.example.other'))
        _, executed = self.failing(None, None, '2')
        self.assertEqual(self.signing_calls(executed), [])

    def test_copy_check_catches_changed_modes(self):
        real = shutil.copytree
        def careless(src, dst, *args, **kw):
            done = real(src, dst, *args, **kw)
            if Path(dst).name == common.APP_NAME:
                os.chmod(Path(dst) / 'Contents/Resources/codex/bin', 0o700)
            return done
        with patch.object(owner.shutil, 'copytree', careless):
            stop, _ = self.failing(None, None, '1')
        self.assertIn('codex/bin', stop['reason'])

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


class Redaction(Base):
    """No output path holds an account name, a password, a non-public team or other owner-typed value."""

    def written(self, *streams):
        texts = list(streams)
        for path in sorted(self.out.rglob('*')) if self.out.exists() else []:
            if path.is_file() and path.suffix in ('.json', '.jsonl', '.md', '.plist'):
                texts.append(path.read_text(errors='replace'))
        return '\n'.join(texts)

    def assert_clean(self, text):
        for secret in SECRETS:
            self.assertNotIn(secret, text)

    def test_completed_run_command_log_record_saved_logs_and_stdout(self):
        self.fake.display_extra = 'Note=password=invented-secret someone@example.com QQQQ11111Q abcd-efgh-ijkl-mnop\n'
        self.fake.submit_extra = {'message': PEM, 'password': 'invented-secret', 'developerAccount': 'someone@example.com'}
        self.fake.log_changes = {'password': 'invented-secret', 'developerAccount': 'someone@example.com', 'teamId': 'QQQQ11111Q',
                                 'statusSummary': 'note abcd-efgh-ijkl-mnop'}
        self.fake.spctl_extra = ' someone@example.com QQQQ11111Q'
        code, stdout, stderr = self.main()
        self.assertEqual(code, 0, stderr)
        text = self.written(stdout, stderr)
        self.assert_clean(text)
        self.assertIn(fx.IDENTITY, text)
        self.assertIn(fx.NOTARY, text)
        for name in ('app-notarization-log.json', 'disk-image-notarization-log.json'):
            saved = json.loads((self.out / 'notary' / name).read_text())
            self.assertEqual(saved['password'], '[redacted]')
            self.assertEqual(saved['status'], 'Accepted')
        identity = json.loads((self.out / 'PACKAGE_IDENTITY.json').read_text())
        self.assertNotEqual(identity['notarization']['app']['original_log_sha256'], identity['notarization']['app']['log_sha256'])

    def test_stop_text_and_stopped_json(self):
        self.fake.submit_extra = {'status': 'password=invented-secret someone@example.com QQQQ11111Q abcd-efgh-ijkl-mnop'}
        code, stdout, stderr = self.main()
        self.assertEqual(code, 3)
        self.assertIn('STOP: 6 notarize App:', stderr)
        self.assert_clean(self.written(stdout, stderr))

    def test_unexpected_exception_text(self):
        def explode(argv, **kw):
            if argv[0] == owner.DITTO:
                raise RuntimeError('someone@example.com QQQQ11111Q password=invented-secret ' + PEM)
            return self.fake(argv, **kw)
        code, stdout, stderr = self.main(runner=explode)
        self.assertEqual(code, 3)
        self.assertIn('STOP: unexpected: RuntimeError', stderr)
        self.assert_clean(self.written(stdout, stderr))

    def test_refusal_text_with_a_typed_value(self):
        code, stdout, stderr = self.main(notary_profile='someone@example.com')
        self.assertEqual(code, 3)
        self.assert_clean(stdout + stderr)
        self.assertFalse(self.out.exists())

    def test_redactor_is_structural_for_json(self):
        redactor = owner.make_redactor(fx.IDENTITY, fx.NOTARY)
        value = redactor.json({'password': 'invented-secret', 'nested': {'appleId': 'x', 'note': '"password":"invented-secret"'},
                               'teams': ['QQQQ11111Q', fx.TEAM, common.SUPPLIER_TEAM], 'identity': fx.IDENTITY}, structural=True)
        self.assertEqual(value['password'], '[redacted]')
        self.assertEqual(value['nested']['appleId'], '[redacted]')
        self.assertNotIn('invented-secret', json.dumps(value))
        self.assertEqual(value['teams'], ['[redacted]', fx.TEAM, common.SUPPLIER_TEAM])
        self.assertEqual(value['identity'], fx.IDENTITY)


class RecordCheck(unittest.TestCase):
    """`check` reports each kind of difference between a package, its saved logs and its record."""

    def setUp(self):
        self.case = OwnerSign('test_full_run_follows_the_plan_and_writes_a_record_that_checks')
        self.case.setUp(); self.addCleanup(self.case.temp.cleanup)
        self.case.sign()
        self.out = self.case.out
        self.identity = json.loads((self.out / 'PACKAGE_IDENTITY.json').read_text())
        self.dmg = self.out / 'Chirality-4.0.0.dmg'
        self.mounted = fx.make_mount_copy(self.out / 'staging', self.case.root / 'mounted')
        self.app = self.mounted / common.APP_NAME

    def differences(self):
        return record.check(self.identity, dmg=self.dmg, app=self.app, run=self.case.fake, record_dir=self.out)

    def assert_found(self, *prefixes):
        found = self.differences()
        self.assertTrue(found, 'no difference reported')
        for prefix in prefixes:
            self.assertTrue(any(f.startswith(prefix) for f in found), (prefix, found))

    def test_unchanged_package_has_no_difference(self):
        self.assertEqual(self.differences(), [])

    def test_package_bytes(self):
        with open(self.dmg, 'ab') as handle: handle.write(b'x')
        self.assert_found('package.s')

    def test_vendor_file(self):
        (self.app / 'Contents/Resources/codex/codex-resources/input.txt').write_bytes(b'changed')
        self.assert_found('observed.vendor.', 'observed.app_as_signed.', 'observed.app_as_stapled.')

    def test_bundled_resource(self):
        (self.app / 'Contents/Resources/instructions/roles.json').write_text('{"roles": ["x"]}')
        self.assert_found('observed.resources.instructions', 'observed.roles_sha256')

    def test_bundle_identity(self):
        (self.app / 'Contents/Info.plist').write_bytes(fx.info_plist(CFBundleShortVersionString='4.0.1'))
        self.assert_found('observed.bundle.')

    def test_app_ticket(self):
        (self.app / 'Contents/CodeResources').write_bytes(b'another ticket')
        found = self.differences()
        self.assertTrue(any(f.startswith('observed.app_as_stapled.') for f in found))
        self.assertTrue(any(f.startswith('observed.stapled_tickets.app.ticket_sha256') for f in found))
        self.assertFalse(any(f.startswith('observed.app_as_signed.') for f in found))
        (self.app / 'Contents/CodeResources').unlink()
        self.assert_found('observation failed: stapled ticket of the app', 'observation failed: the App holds no stapled ticket')

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
        self.assert_found('observed.limitations.disk_image', 'observed.limitations.bundle', 'observed.resources.release')

    def test_failed_observations_are_reported_not_equal(self):
        fake = self.case.fake
        fake.override[('stapler', 'validate')] = Result(65)
        fake.override[('-t', 'open')] = Result(3, b'', b'rejected\nsource=Unnotarized Developer ID\n')
        fake.override[('-d', '--entitlements')] = Result(1)
        self.assert_found('observation failed: stapled ticket of the app', 'observation failed: stapled ticket of the disk image',
                          'observation failed: Gatekeeper', 'observation failed: entitlements unreadable',
                          'observed.stapled_tickets', 'observed.gatekeeper')

    def test_notarization_fields_in_the_record(self):
        for key, field, value in (('app', 'status', 'Invalid'), ('app', 'submission_id', 'x'), ('disk_image', 'submitted_sha256', '0' * 64),
                                  ('disk_image', 'log_sha256', '0' * 64), ('app', 'issues', [{'severity': 'error'}])):
            with self.subTest(key=key, field=field):
                original = self.identity['notarization'][key][field]
                self.identity['notarization'][key][field] = value
                self.assert_found(f'notarization.{key}')
                self.identity['notarization'][key][field] = original
        self.assertEqual(self.differences(), [])

    def test_saved_logs_and_submitted_archive(self):
        log = self.out / 'notary/disk-image-notarization-log.json'
        value = json.loads(log.read_text()); value['status'] = 'Invalid'
        log.write_text(json.dumps(value))
        self.assert_found('notarization.disk_image: notarization log is not Accepted', 'notarization.disk_image.log_sha256')
        (self.out / 'notary/Chirality-4.0.0-app.zip').write_bytes(b'other archive')
        self.assert_found('notarization.app: submitted file differs')
        (self.out / 'notary/app-notarization-log.json').unlink()
        self.assert_found('notarization.app: notarization log missing')

    def test_write_refuses_a_failed_observation(self):
        self.case.fake.override[('stapler', 'validate')] = Result(65)
        notarizations = {k: {kk: v[kk] for kk in ('log', 'original_log_sha256', 'submitted_sha256', 'submitted') if kk in v}
                         for k, v in self.identity['notarization'].items()}
        candidate = json.loads((self.case.candidate / 'CANDIDATE.json').read_text())
        with self.assertRaises(record.ObservationFailed):
            record.write(self.out / 'second-record.json', dmg=self.dmg, app=self.app, run=self.case.fake, candidate=candidate,
                         notarizations=notarizations, signed_tree=common.inventory.scan(self.app),
                         redactor=owner.make_redactor(fx.IDENTITY, fx.NOTARY))
        self.assertFalse((self.out / 'second-record.json').exists())


if __name__ == '__main__':
    unittest.main()
