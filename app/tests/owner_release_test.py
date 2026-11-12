"""The owner's signing procedure and the package identity record, on invented material.

No signing, notarization, stapling, Gatekeeper or keychain tool runs: every
Apple command goes to owner_fixtures.FakeApple, whose outputs are the forms
declared in app/packaging/release/observations.py. No test opens, lists, walks
or stats anything in the private folder: the tools are given an in-memory
writer, and the one test of the real writer takes the modes it reports.
"""
import argparse
import ast
import datetime
import importlib.util
import io
import json
import os
from pathlib import Path
import plistlib
import shutil
import stat
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location('owner_fixtures', HERE / 'owner_fixtures.py')
fx = importlib.util.module_from_spec(_spec); sys.modules['owner_fixtures'] = fx; _spec.loader.exec_module(fx)
owner, record, obs, common = fx.release('owner_sign'), fx.release('record'), fx.release('observations'), fx.common
Result = common.Result
HOST = ('Darwin', 'arm64')
ENV = {'HOME': '/invented-home', 'PATH': '/usr/bin'}
NOW = datetime.datetime(2026, 11, 12)
APP_ID, DMG_ID = fx.submission_id(1), fx.submission_id(2)
RELEASE_DIR = HERE.parent / 'packaging/release'
# Secret-looking values, assembled at run time so that no credential-shaped literal sits in the source.
PEM = '-----' + 'BEGIN PRIVATE KEY' + '-----\nMIIEinvented\n-----' + 'END PRIVATE KEY' + '-----'
SECRETS = ['abcd-efgh-ijkl-mnop', 'MIIEinvented', 'someone@example.com', 'invented-secret', 'QQQQ11111Q', 'invented-owner-account',
           'other-notary-profile', 'ABCDEFGHIJ', 'invented-owner-alias', 'invented-owner@example.invalid', 'Apple ID']


# A display of the declared forms only (observations.FORMS['signature']).
DISPLAY = (b'Identifier=com.chirality.app\nFormat=app bundle with Mach-O thin (arm64)\n'
           b'CodeDirectory v=20500 size=1 flags=0x10000(runtime) hashes=1+1 location=embedded\nHash type=sha256 size=32\n'
           b'CDHash=' + b'd' * 40 + b'\nAuthority=Developer ID Application: Invented Publisher (8A7JL35U4S)\n'
           b'Authority=Developer ID Certification Authority\nAuthority=Apple Root CA\nTimestamp=1 Jan 2026 at 00:00:00\n'
           b'TeamIdentifier=8A7JL35U4S\n')
ENTITLEMENTS_XML = plistlib.dumps({'com.apple.application-identifier': '8A7JL35U4S.com.chirality.app',
                                   'com.apple.developer.team-identifier': '8A7JL35U4S'})
SUBMIT = ('Successfully uploaded file.\n id: 00000001-89ab-cdef-0123-456789abcdef\n path: /invented/asked\n'
          'createdDate: 2026-01-01T00:00:00.000Z\nid: 00000001-89ab-cdef-0123-456789abcdef\nname: asked\nstatus: Accepted\n')
LOG = 'Successfully downloaded submission log\n id: 00000001-89ab-cdef-0123-456789abcdef\n location: /invented/asked\n'



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
        return owner.sign(self.args(**changes), runner=self.fake, environ=environ, host=host, now=NOW, private=fx.MemoryWriter)[0]

    def argv(self, notary_profile=fx.NOTARY):
        return ['--identity', fx.IDENTITY, '--notary-profile', notary_profile, '--candidate', str(self.candidate), '--profile',
                str(self.profile), '--profile-sha256', fx.sha(self.profile.read_bytes()), '--limitations', str(self.limitations),
                '--out', str(self.out)]

    def main(self, *extra, runner=None, notary_profile=fx.NOTARY):
        stdout, stderr = io.StringIO(), io.StringIO()
        self.private = []
        def private(root):
            writer = fx.MemoryWriter(root); self.private.append(writer); return writer
        code = owner.main(self.argv(notary_profile) + list(extra), stdout=stdout, stderr=stderr, runner=runner or self.fake,
                          environ=ENV, host=HOST, now=NOW, private=private)
        return code, stdout.getvalue(), stderr.getvalue()

    def with_line(self, argv_filter, line, stream='stderr'):
        """An override that keeps the stand-in's own answer and adds one line to a stream."""
        def override(argv):
            if not argv_filter(argv):
                return None
            real = self.fake.answer(argv)
            add = line(argv) if callable(line) else line
            if stream == 'stdout':
                return Result(real.returncode, real.stdout + add, real.stderr)
            return Result(real.returncode, real.stdout, real.stderr + add)
        return override

    def log(self):
        return [json.loads(line) for line in (self.out / 'log.jsonl').read_text().splitlines()]

    def executed(self):
        return [entry['argv'] for entry in self.log()]

    def failing(self, words, result, code, **fake):
        for key, value in fake.items():
            setattr(self.fake, key, value)
        if words:
            self.fake.override[words] = result
        status, stdout, stderr = self.main()
        self.assertEqual(status, 3, stderr)
        stopped = json.loads((self.out / 'STOPPED.json').read_text())
        self.assertEqual(stopped['reason_code'], code, stopped)
        self.assertEqual(stopped['reason'], common.REASONS[code])
        self.assertEqual(stderr, 'STOP: ' + common.REASONS[code] + '\n')
        self.assertFalse((self.out / 'RESULT.json').exists())
        self.assertEqual(stdout, '')
        return stopped, self.executed()


class Assessment(Base):
    """The most serious finding of round 2: an assessment saying "not accepted" with return code 0 was recorded as accepted."""

    def test_a_negative_assessment_with_return_code_zero_is_never_accepted(self):
        negative = lambda argv: Result(0, b'', f'{argv[-1]}: not accepted\nsource=Notarized Developer ID\n'.encode())
        for text in (b'/x: rejected\nsource=Notarized Developer ID\n', b'/x: accepted\nsource=Unnotarized Developer ID\n',
                     b'/x: not accepted\nsource=Notarized Developer ID\n', b'/x: accepted\n', b'', b'accepted\nsource=Notarized Developer ID\n',
                     # an origin line no source shows is an undeclared form, so this is no observation either
                     b'/x: accepted\nsource=Notarized Developer ID\norigin=Developer ID Application: Errorless (8A7JL35U4S)\n'):
            with self.subTest(text=text), self.assertRaises(obs.ObservationFailed):
                obs.observe('assessment', Result(0, b'', text), subject='/x')
        obs.observe('assessment', Result(0, b'', b'/x: accepted\nsource=Notarized Developer ID\n'), subject='/x')
        self.failing(('-t', 'open'), negative, 'S12_OPEN')
        self.setUp()
        self.failing(('-t', 'exec'), negative, 'S12_EXEC')
        self.setUp()
        stopped, _ = self.failing(('-t', 'exec'), lambda argv: negative(argv) if sum(c[1] == 'detach' for c in self.fake.calls) == 1 else None,
                                  'S13_OBSERVATION')
        self.assertIn({'observation': 'gatekeeper', 'subject': 'app'}, stopped['failed_observations'])


class Binding(Base):
    """Round 3 finding 3: an observation counts only when it names the object asked about and is unambiguous."""

    def test_the_rule_refuses_other_objects_and_ambiguity(self):
        asked = '/invented/asked'
        refused = {
            'assessment of another path': ('assessment', Result(0, b'', b'/invented/other: accepted\nsource=Notarized Developer ID\n')),
            'two assessment sources': ('assessment', Result(0, b'', b'/invented/asked: accepted\nsource=Notarized Developer ID\nsource=Developer ID\n')),
            'verify of another path': ('verify', Result(0, b'', b'/invented/other: valid on disk\n')),
            'requirement of another path': ('requirement', Result(0, b'', b'/invented/other: valid on disk\n/invented/other: explicit requirement satisfied\n')),
            'conflicting identifiers': ('signature', Result(0, b'', DISPLAY + b'Identifier=other\n')),
            'conflicting teams': ('signature', Result(0, b'', DISPLAY + b'TeamIdentifier=OTHER00001\n')),
            'two submission identifiers': ('submit', Result(0, SUBMIT.replace('id: 00000001', 'id: 00000002', 1).encode())),
            'submission of another file': ('submit', Result(0, SUBMIT.replace('path: /invented/asked', 'path: /invented/other').encode())),
            'log written elsewhere': ('log', Result(0, LOG.replace('/invented/asked', '/invented/other').encode())),
            'no object asked about': ('verify', Result(0, b'', b'/invented/asked: valid on disk\n')),
        }
        for name, (kind, result) in refused.items():
            with self.subTest(name), self.assertRaises(obs.ObservationFailed):
                obs.observe(kind, result, subject=None if name == 'no object asked about' else asked)
        self.assertEqual(obs.observe('signature', Result(0, b'', DISPLAY), subject=asked)['identifier'], 'com.chirality.app')
        obs.observe('verify', Result(0, b'', b'/invented/x.app: valid on disk\n\n/invented/x.app: satisfies its Designated Requirement\n'),
                    subject='/invented/x.app')
        self.assertEqual(obs.observe('submit', Result(0, SUBMIT.encode()), subject=asked)['status'], 'Accepted')
        obs.observe('log', Result(0, LOG.encode()), subject=asked)
        self.assertEqual(obs.observe('entitlements', Result(0, ENTITLEMENTS_XML), subject=asked)['com.apple.developer.team-identifier'], fx.TEAM)

    def test_round_4_an_output_is_an_observation_only_when_every_line_is_declared(self):
        """Round 4 findings 1 and 2: failure text, another executable, a second leaf authority or a duplicate key
        completed an observation because only wanted fields were read. Each is now no observation."""
        asked = '/invented/asked'
        duplicate = ENTITLEMENTS_XML.replace(b'<key>com.apple.developer.team-identifier</key>',
                                             b'<key>com.apple.application-identifier</key><string>OTHER00001.com.example.other</string>'
                                             b'<key>com.apple.developer.team-identifier</key>')
        self.assertEqual(duplicate.count(b'com.apple.application-identifier'), 2)
        refused = {
            'entitlements with the App identifier key twice': ('entitlements', Result(0, duplicate)),
            'entitlements with an error on standard error': ('entitlements', Result(0, ENTITLEMENTS_XML, b'failed to read entitlements\n')),
            'entitlements naming another executable': ('entitlements', Result(0, ENTITLEMENTS_XML, b'Executable=/invented/other\n')),
            'entitlements in binary form': ('entitlements', Result(0, plistlib.dumps({}, fmt=plistlib.FMT_BINARY))),
            'entitlements that are not a dictionary': ('entitlements', Result(0, plistlib.dumps(['x']))),
            'display naming another executable': ('signature', Result(0, b'', b'Executable=/invented/other\n' + DISPLAY)),
            'display with failure text': ('signature', Result(0, b'', DISPLAY + b'/invented/asked: code object is not signed at all\n')),
            'display on standard output': ('signature', Result(0, b'Identifier=com.chirality.app\n', DISPLAY)),
            'a second leaf authority': ('signature', Result(0, b'', DISPLAY.replace(
                b'Authority=Apple Root CA\n', b'Authority=Apple Root CA\nAuthority=Developer ID Application: Other (OTHER00001)\n'))),
            'the leaf not first': ('signature', Result(0, b'', DISPLAY.replace(
                b'Authority=Developer ID Application: Invented Publisher (8A7JL35U4S)\nAuthority=Developer ID Certification Authority\n',
                b'Authority=Developer ID Certification Authority\nAuthority=Developer ID Application: Invented Publisher (8A7JL35U4S)\n'))),
            'a chain authority twice': ('signature', Result(0, b'', DISPLAY + b'Authority=Apple Root CA\n')),
            'signed time instead of a timestamp': ('signature', Result(0, b'', DISPLAY.replace(
                b'Timestamp=1 Jan 2026 at 00:00:00', b'Signed Time=1 Jan 2026 at 00:00:00'))),
            'a timestamp of another form': ('signature', Result(0, b'', DISPLAY.replace(b'Timestamp=1 Jan 2026', b'Timestamp=Jan 1, 2026'))),
            'a code directory not embedded': ('signature', Result(0, b'', DISPLAY.replace(b' location=embedded', b''))),
            'verify with failure text': ('verify', Result(0, b'', b'/invented/asked: valid on disk\n/invented/asked: a sealed resource is missing or invalid\n')),
            'verify with a line naming a nested object': ('verify', Result(0, b'', b'--prepared:/invented/asked/Contents/x\n/invented/asked: valid on disk\n')),
            'staple with a line no source shows': ('staple', Result(0, b'Processing: /invented/asked\nThe staple and validate action worked!\n')),
            'validate with failure text': ('validate', Result(0, b'The validate action worked!\nCloudKit query failed\n')),
            'submit with failure text': ('submit', Result(0, (SUBMIT + 'Error: failed to submit\n').encode())),
            'submit with a progress line': ('submit', Result(0, ('Conducting pre-submission checks for asked\n' + SUBMIT).encode())),
            'submit in JSON': ('submit', Result(0, b'{"id":"00000001-89ab-cdef-0123-456789abcdef","status":"Accepted"}')),
            'a status line twice': ('submit', Result(0, (SUBMIT + 'status: Invalid\n').encode())),
            'log with failure text': ('log', Result(0, (LOG + 'Error: failed to fetch log\n').encode())),
            'assessment with failure text': ('assessment', Result(0, b'', b'/invented/asked: accepted\nsource=Notarized Developer ID\n'
                                                                   b'/invented/asked: rejected\n')),
        }
        for name, (kind, result) in refused.items():
            with self.subTest(name), self.assertRaises(obs.ObservationFailed):
                obs.observe(kind, result, subject=asked)
        with self.assertRaises(ValueError):
            obs.load_xml_plist(duplicate)
        log = {'jobId': '00000001-89AB-cdef-0123-456789abcdef', 'status': 'Accepted', 'issues': None, 'sha256': '0' * 64}
        self.assertEqual(obs.observe_log_file(json.dumps(log).encode(), None, None)['job'], '00000001-89ab-cdef-0123-456789abcdef')
        for raw in (json.dumps(log)[:-1] + ', "status": "Invalid"}', json.dumps(log | {'undeclared': 1}),
                    json.dumps(log | {'issues': [{'severity': 'error', 'note': 'x'}]}), json.dumps({k: v for k, v in log.items() if k != 'sha256'})):
            with self.subTest(raw=raw), self.assertRaises(obs.ObservationFailed):
                obs.observe_log_file(raw.encode(), None, None)

    def test_every_declared_form_names_its_source(self):
        sources = {'TN3126', 'TN3127', 'TN3161', 'TN3125', 'NOTARY', 'WITNESS', 'ADVANCE', 'RUN1103'}
        for name, spec in obs.FORMS.items():
            forms = [f for key in ('either', 'stdout', 'stderr') if isinstance(spec.get(key), list) for f in spec[key]]
            for form in forms:
                with self.subTest(command=name, form=form[0]):
                    self.assertIn(form[2], ('fact', 'known', 'noise'))
                    self.assertTrue(any(source in form[4] for source in sources), form)
            if spec.get('stdout') == 'xml-plist':
                self.assertIn(spec['source'], sources)
        for key, (_, source) in obs.LOG_KEYS.items():
            self.assertIn(source, sources)

    def test_a_run_whose_tools_report_another_object_stops(self):
        """The reviewer's whole-run probe: every reported path replaced with another object's."""
        real = self.fake.__call__
        def elsewhere(argv, **kw):
            result = real(argv, **kw)
            target = argv[-1].encode()
            swap = lambda raw: raw.replace(target, b'/invented/different-object')
            return Result(result.returncode, swap(result.stdout), swap(result.stderr))
        code, stdout, stderr = self.main(runner=elsewhere)
        self.assertEqual(code, 3)
        self.assertFalse((self.out / 'RESULT.json').exists())
        self.assertFalse((self.out / 'PACKAGE_IDENTITY.json').exists())

    def test_hardened_runtime_off_at_record_time_stops(self):
        """Round 3 finding 4: a reading at record time without hardened runtime stops; it is never recorded as false."""
        for target, failed in (('.app', 'hardened runtime'), ('codex', 'supplier signature changed')):
            with self.subTest(target=target):
                self.setUp()
                real = self.fake.codesign
                def display(rest, target=target, real=real):
                    result = real(rest)
                    if rest[:2] == ['-d', '--verbose=3'] and '/mount/' in rest[-1] and rest[-1].endswith(target):
                        return Result(0, b'', result.stderr.replace(b'flags=0x10000(runtime)', b'flags=0x0(none)'))
                    return result
                self.fake.codesign = display
                stopped, _ = self.failing(None, None, 'S13_OBSERVATION')
                self.assertIn(failed, [f['observation'] for f in stopped['failed_observations']])
                self.assertFalse((self.out / 'PACKAGE_IDENTITY.json').exists())


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
                                           '<out>/entitlements.plist'])
        submits = [Path(a[3]).name for a in argvs if a[:3] == [owner.XCRUN, 'notarytool', 'submit']]
        self.assertEqual(submits, ['Chirality-4.0.0-app.zip', 'Chirality-4.0.0.dmg'])
        staples = [Path(a[-1]).name for a in argvs if a[1:3] == ['stapler', 'staple']]
        self.assertEqual(staples, ['Chirality.app', 'Chirality-4.0.0.dmg'])
        app = '<out>/staging/' + common.APP_NAME
        after = argvs[[i for i, a in enumerate(argvs) if a[1:3] == ['stapler', 'staple']][0] + 1:]
        self.assertFalse([a for a in after if a[-1] == app and ('--sign' in a or 'staple' in a)])
        # The identity and profile names appear only as the values of their two arguments.
        for argv in argvs:
            for index, value in enumerate(argv):
                if value == fx.IDENTITY:
                    self.assertEqual(argv[index - 1], '--sign')
                if value == fx.NOTARY:
                    self.assertEqual(argv[index - 1], '--keychain-profile')
            self.assertFalse(any(str(self.root) in a for a in argv))

    def test_dry_run_prints_the_exact_plan_and_runs_nothing(self):
        code, stdout, _ = self.main('--dry-run')
        self.assertEqual(code, 0)
        self.assertEqual(self.fake.calls, [])
        self.assertFalse(self.out.exists())
        self.assert_shape([step['argv'] for step in json.loads(stdout)['plan']])

    def test_full_run_follows_the_plan_and_writes_a_record_that_checks(self):
        plan = [step['argv'] for step in self.sign(dry_run=True)['plan']]
        result = self.sign()
        ids = {'<app-submission-id>': APP_ID, '<disk-image-submission-id>': DMG_ID}
        self.assertEqual(self.executed(), [[ids.get(w, w) for w in a] for a in plan])
        self.assert_shape(self.executed())
        self.assertEqual((result['installed'], result['result']), (False, 'complete'))
        for entry in self.log():
            self.assertEqual(set(entry), {'step', 'argv', 'returncode', 'stdout', 'stderr'})
            self.assertEqual(set(entry['stdout']), {'length', 'sha256'})
        app = self.out / 'staging' / common.APP_NAME
        self.assertTrue((app / 'Contents/CodeResources').is_file())
        placed = app / 'Contents/embedded.provisionprofile'
        self.assertEqual(os.stat(placed).st_mode & 0o7777, 0o644)
        self.assertEqual(plistlib.loads((self.out / 'entitlements.plist').read_bytes()),
                         {'com.apple.application-identifier': fx.TEAM + '.com.chirality.app', 'com.apple.developer.team-identifier': fx.TEAM})
        identity = json.loads((self.out / 'PACKAGE_IDENTITY.json').read_text())
        observed = identity['observed']
        self.assertEqual(identity['package']['sha256'], fx.sha((self.out / 'Chirality-4.0.0.dmg').read_bytes()))
        self.assertEqual(set(observed['app_as_stapled']['inventory']['entries']) - set(observed['app_as_signed']['inventory']['entries']),
                         {'Contents/CodeResources'})
        self.assertEqual(observed['stapled_tickets']['app']['validated'], True)
        self.assertEqual(observed['gatekeeper'], {'disk_image': {'accepted': True, 'source': 'Notarized Developer ID'},
                                                  'app': {'accepted': True, 'source': 'Notarized Developer ID'}})
        self.assertEqual({k: v['submission_id'] for k, v in identity['notarization'].items()}, {'app': APP_ID, 'disk_image': DMG_ID})
        self.assertEqual(identity['notarization']['app']['submitted'], 'notary/Chirality-4.0.0-app.zip')
        mounted = fx.make_mount_copy(self.out / 'staging', self.root / 'mounted')
        result = record.check(identity, dmg=self.out / 'Chirality-4.0.0.dmg', app=mounted / common.APP_NAME,
                              run=self.fake, record_dir=self.out)
        self.assertTrue(result['equal'], result)
        self.assertIn(record.NOT_CHECKED_LOGS, result['not_checked'])
        self.assertFalse((self.out / common.PRIVATE_FOLDER).exists())  # the injected writer kept the raw output in memory

    def test_raw_output_is_handed_to_the_private_writer_only(self):
        self.inject = 'invented-owner-account'
        self.fake.log_changes = {'statusSummary': 'note ' + self.inject}  # a declared free-text field of the log
        code, stdout, stderr = self.main()
        self.assertEqual(code, 0, stderr)
        handed = [raw for writer in self.private for _, raw in writer.handed]
        self.assertTrue(any(self.inject.encode() in raw for raw in handed))
        for name in ('log.jsonl', 'notary/app-notarization.json', 'PACKAGE_IDENTITY.json', 'RESULT.json'):
            self.assertNotIn(self.inject, (self.out / name).read_text())

    def test_the_real_private_writer_uses_private_modes(self):
        """The modes come from the writer's own descriptor and folder; the test stats, lists and reads nothing there."""
        out = self.root / 'writer-out'; out.mkdir()
        writer = common.PrivateWriter(out)
        written = [writer.write('first', b'invented raw'), writer.write('second', b'more')]
        for path, file_mode, folder_mode in written:
            self.assertEqual((file_mode, folder_mode), (0o600, 0o700))
        for path, _, _ in written:  # clean-up by the returned names: removal, not a look inside
            os.unlink(path)
        os.rmdir(writer.folder)

    def test_refusals_run_no_command(self):
        cases = {
            'malformed identity': (dict(identity='Invented Publisher'), 'REFUSED_IDENTITY_FORM'),
            'path-like identity': (dict(identity='/Users/someone/cert.p12'), 'REFUSED_IDENTITY_PATH'),
            'other team': (dict(identity='Developer ID Application: Invented Publisher (OTHER00001)'), 'REFUSED_TEAM'),
            'credential notary profile': (dict(notary_profile='abcd-efgh-ijkl-mnop'), 'REFUSED_NOTARY_PROFILE'),
            'e-mail notary profile': (dict(notary_profile='someone@example.com'), 'REFUSED_NOTARY_PROFILE'),
            'key file path': (dict(profile=str(self.root / 'key.p12')), 'REFUSED_ARGUMENT_CREDENTIAL'),
            'profile digest': (dict(profile_sha256='0' * 64), 'REFUSED_PROFILE_BYTES'),
            'limitations differ': (dict(limitations=str(self.candidate / 'publisher/publisher-requirement.txt')), 'REFUSED_LIMITATIONS'),
        }
        private = self.root / common.PRIVATE_FOLDER
        for name in ('candidate', 'profile', 'limitations', 'out'):  # round 4 finding 3: refused by name, before anything is opened
            cases[f'{name} inside the private folder'] = ({name: str(private / 'x')}, 'REFUSED_PRIVATE_INPUT')
            cases[f'{name} inside the private folder, by bytes'] = ({name: os.fsencode(private / 'x')}, 'REFUSED_PRIVATE_INPUT')
        for name, (changes, code) in cases.items():
            with self.subTest(name), self.assertRaises(common.Failure) as raised:
                self.sign(**changes)
            self.assertEqual(raised.exception.code, code)
        for environ in (ENV | {'APPLE_ID': 'x'}, ENV | {'NOTARY_PASSWORD': 'x'}, ENV | {'TAURI_SIGNING_PRIVATE_KEY': 'x'}):
            with self.assertRaises(common.Failure):
                self.sign(environ=environ)
        with self.assertRaises(common.Failure):
            self.sign(host=('Darwin', 'x86_64'))
        self.out.mkdir()
        with self.assertRaises(common.Failure):
            self.sign()
        self.out.rmdir()
        vendor_file = self.candidate / 'target/release/bundle/macos' / common.APP_NAME / 'Contents/Resources/codex/codex-resources/input.txt'
        vendor_file.write_bytes(b'changed')
        with self.assertRaises(common.Failure) as raised:
            self.sign()
        self.assertEqual(raised.exception.code, 'REFUSED_CANDIDATE')
        self.assertEqual(self.fake.calls, [])
        self.assertFalse(self.out.exists())

    def test_installed_locations_are_refused_by_filesystem_identity(self):
        protected = self.root / 'Applications'; protected.mkdir()
        alias = self.root / 'apps-link'; alias.symlink_to(protected)
        cases = {'symlink to the place': alias / 'release', 'inside the place': protected / 'release'}
        (self.root / 'CaseProbe').mkdir()
        if (self.root / 'caseprobe').exists():
            cases['case alias'] = self.root / 'APPLICATIONS' / 'release'
        with patch.object(common, 'protected_places', lambda: [protected]):
            for name, out in cases.items():
                with self.subTest(name), self.assertRaises(common.Failure) as raised:
                    self.sign(out=str(out))
                self.assertEqual(raised.exception.code, 'REFUSED_LOCATION')
        self.assertEqual(self.fake.calls, [])

    def test_writes_refuse_existing_links_and_paths_outside(self):
        out = self.root / 'out-a'; out.mkdir()
        outside = self.root / 'outside.txt'; outside.write_text('before')
        (out / 'log.jsonl').symlink_to(outside)
        os.link(outside, out / 'hard.json')
        for path in (out / 'log.jsonl', out / 'hard.json', self.root / 'elsewhere.json'):
            with self.subTest(path=path.name), self.assertRaises(ValueError):
                common.write_returnable(path, {'result': 'complete'}, out, set(), append=True)
        self.assertEqual(outside.read_text(), 'before')
        # an allowed argument pair is still bounded in length
        long = 'x' * (common.MAX_LENGTH + 1)
        with self.assertRaises(ValueError):
            common.validate_returnable({'argv': ['-R', long]}, set(), argv_allowed={('-R', long)})

    def test_each_failing_step_stops_with_its_fixed_reason_and_no_later_command(self):
        dmg_only = lambda r: (lambda argv: r if argv[-1].endswith('.dmg') else None)
        after_staple = lambda r: (lambda argv: r if is_app(argv) and (Path(argv[-1]) / 'Contents/CodeResources').exists() else None)
        no_line = lambda prefix: (lambda argv: Result(0, b'', b'\n'.join(l for l in self.fake.answer(argv).stderr.splitlines()
                                                                          if not l.startswith(prefix))) if is_app(argv) else None)
        app_only, zip_only = (lambda argv: is_app(argv)), (lambda argv: argv[3].endswith('.zip'))
        line = self.with_line
        cases = [
            (('--sign', '--entitlements'), Result(1), 'S4_SIGN', None),
            (('--verify', '--deep'), Result(1), 'S5_DEEP', None),
            (('--verify', '--deep'), Result(0, b'', b'x: invalid signature (code or signature have been modified)\n'), 'S5_DEEP', None),
            (('-R',), Result(3), 'S5_REQUIREMENT', None),
            (('--verify', '--deep'), line(app_only, lambda a: f'{a[-1]}: a sealed resource is missing or invalid\n'.encode()), 'S5_DEEP', None),
            (('-R',), line(app_only, b'test-requirement: failed\n'), 'S5_REQUIREMENT', None),
            (('-d', '--verbose=3'), lambda argv: Result(1) if is_app(argv) else None, 'S5_DISPLAY', None),
            (('-d', '--verbose=3'), no_line(b'Timestamp='), 'S5_DISPLAY', None),
            (('-d', '--verbose=3'), no_line(b'CodeDirectory '), 'S5_DISPLAY', None),
            (('-d', '--verbose=3'), line(app_only, b'Executable=/invented/other/Contents/MacOS/other\n'), 'S5_DISPLAY', None),
            (('-d', '--verbose=3'), line(app_only, b'Authority=Developer ID Application: Other (OTHER00001)\n'), 'S5_DISPLAY', None),
            (('-d', '--entitlements'), lambda argv: Result(0, b'') if is_app(argv) else None, 'S5_ENTITLEMENTS', None),
            (('-d', '--entitlements'), line(app_only, b'failed to read entitlements\n'), 'S5_ENTITLEMENTS', None),
            ((owner.DITTO,), Result(1), 'S6_ARCHIVE', None),
            (('submit',), lambda argv: Result(1) if argv[3].endswith('.zip') else None, 'S6_SUBMIT', None),
            (('submit',), lambda argv: Result(0, b'invented unexpected text') if argv[3].endswith('.zip') else None, 'S6_SUBMIT', None),
            (('submit',), line(zip_only, b'Error: failed to submit\n', 'stdout'), 'S6_SUBMIT', None),
            (('notarytool', 'log'), Result(0, b'[]'), 'S6_LOG', None),
            (('notarytool', 'log'), line(lambda a: True, b'Error: failed to fetch log\n', 'stdout'), 'S6_LOG', None),
            (('stapler', 'staple'), line(app_only, lambda a: f'Processing: {a[-1]}\n'.encode(), 'stdout'), 'S7_STAPLE', None),
            (('stapler', 'staple'), lambda argv: Result(1) if is_app(argv) else None, 'S7_STAPLE', None),
            (('stapler', 'validate'), lambda argv: Result(65) if is_app(argv) else None, 'S7_VALIDATE', None),
            (('--verify', '--deep'), after_staple(Result(1)), 'S8_DEEP', None),
            (('create',), Result(1), 'S9_CREATE', None),
            (('--verify', '--strict', '--verbose=1'), dmg_only(Result(1)), 'S9_VERIFY', None),
            (('-d', '--verbose=3'), dmg_only(Result(1)), 'S9_DISPLAY', None),
            (('submit',), lambda argv: Result(1) if argv[3].endswith('.dmg') else None, 'S10_SUBMIT', None),
            (('stapler', 'staple'), dmg_only(Result(1)), 'S11_STAPLE', None),
            (('stapler', 'validate'), dmg_only(Result(65)), 'S11_VALIDATE', None),
            (('-t', 'open'), Result(3, b'', b'rejected\n'), 'S12_OPEN', None),
            (('-t', 'open'), line(lambda a: True, b'origin=Developer ID Application: Invented Publisher (8A7JL35U4S)\n'), 'S12_OPEN', None),
            (('attach',), Result(1), 'S12_ATTACH', None),
            (('-t', 'exec'), Result(3, b'', b'rejected\n'), 'S12_EXEC', 'detach'),
            (('detach',), Result(16), 'S12_DETACH', None),
        ]
        for words, result, code, after in cases:
            with self.subTest(code=code, words=words):
                self.setUp()
                _, executed = self.failing(words, result, code)
                answer = lambda a: (result(a) if callable(result) else result)
                shown_words = tuple(w for w in words)
                failing = max(i for i, a in enumerate(executed) if all(w in a for w in shown_words))
                self.assertEqual([a[1] for a in executed[failing + 1:]], ['detach'] if after else [])
                if code < 'S11':
                    self.assertFalse(any(a[1:3] == ['stapler', 'staple'] and a[-1].endswith('.dmg') for a in executed))

    def test_a_failed_observation_in_the_record_stops_with_no_record(self):
        in_record = lambda r: (lambda argv: r if '/mount/' in argv[-1] else None)
        for words, result, failed in ((('stapler', 'validate'), in_record(Result(65)), 'ticket validation'),
                                      (('-d', '--entitlements'), in_record(Result(1)), 'entitlements'),
                                      (('-d', '--verbose=3'), in_record(Result(0, b'', b'Identifier=x\n')), 'signature'),
                                      (('-d', '--verbose=3'), lambda argv: Result(0, b'', b'Executable=/invented/other\n' + self.fake.answer(argv).stderr)
                                       if '/mount/' in argv[-1] else None, 'signature')):
            with self.subTest(failed=failed):
                self.setUp()
                stopped, executed = self.failing(words, result, 'S13_OBSERVATION')
                self.assertIn(failed, [f['observation'] for f in stopped['failed_observations']])
                self.assertEqual(executed[-1][1], 'detach')
                self.assertFalse((self.out / 'PACKAGE_IDENTITY.json').exists())
        self.setUp()
        second_detach = lambda argv: Result(16) if sum(c[1] == 'detach' for c in self.fake.calls) == 2 else None
        self.failing(('detach',), second_detach, 'S13_DETACH')
        self.assertFalse((self.out / 'PACKAGE_IDENTITY.json').exists())
        # a detach that returns zero but leaves the image mounted: the action's output is not read, its effect is
        for count, code in ((1, 'S12_DETACH'), (2, 'S13_DETACH')):
            with self.subTest(code=code):
                self.setUp()
                still_mounted = lambda argv, count=count: Result(0, b'', b'hdiutil: detach failed - invented\n') \
                    if sum(c[1] == 'detach' for c in self.fake.calls) == count else None
                self.failing(('detach',), still_mounted, code)
                self.assertFalse((self.out / 'PACKAGE_IDENTITY.json').exists())

    def test_supplier_signature_problems_stop_with_the_clm_002_question(self):
        for problem, code in (({'flags': '0x0(none)'}, 'S0_SIGNATURE'), ({'timestamp': 'Signed Time=Jan 1, 2026'}, 'S0_SIGNATURE'),
                              ({'team': 'OTHER00001'}, 'S0_SIGNATURE'), ({'cdhash': 'CDHash-unavailable'}, 'S0_SIGNATURE'),
                              ({'entitlements': {'com.apple.security.get-task-allow': True}}, 'S0_ENTITLEMENTS')):
            with self.subTest(problem=problem):
                self.setUp()
                _, executed = self.failing(None, None, code, supplier={'rg': problem})
                self.assertIn('CLM-002', common.REASONS[code])
                self.assertTrue(all(a[0] == owner.CODESIGN and '--sign' not in a for a in executed))
        self.setUp()
        self.failing(('-d', '--entitlements'), lambda argv: Result(0, b'') if 'Resources/codex' in argv[-1] else None, 'S0_ENTITLEMENTS')

    def test_notarization_answers_that_are_not_clean_are_never_stapled(self):
        cases = {'rejected': (dict(submit_extra={'status': 'Invalid'}), 'S6_STATUS'),
                 'issues': (dict(log_changes={'issues': [{'severity': 'error'}]}), 'S6_ISSUES'),
                 'no issues field': (dict(log_changes={'issues': fx.DELETE}), 'S6_LOG'),
                 'digest': (dict(log_changes={'sha256': '0' * 64}), 'S6_DIGEST'),
                 'other job': (dict(log_changes={'jobId': 'ffffffff-89ab-cdef-0123-456789abcdef'}), 'S6_JOB')}
        for name, (fake, code) in cases.items():
            with self.subTest(name):
                self.setUp()
                _, executed = self.failing(None, None, code, **fake)
                self.assertFalse(any(a[0] == owner.XCRUN and a[1] == 'stapler' for a in executed))
        self.setUp()
        # the disk image's log names another digest: the override changes the log the stand-in writes, then lets it answer
        second_log = lambda argv: setattr(self.fake, 'log_changes', {'sha256': '0' * 64}) if len(self.fake.submissions) == 2 else None
        _, executed = self.failing(('notarytool', 'log'), second_log, 'S10_DIGEST')
        self.assertFalse(any(a[1:3] == ['stapler', 'staple'] and a[-1].endswith('.dmg') for a in executed))
        # a log fetched with output that is no observation still leaves the output folder for the private writer
        self.setUp()
        self.failing(('notarytool', 'log'), self.with_line(lambda a: True, b'Error: failed to fetch log\n', 'stdout'), 'S6_LOG')
        self.assertFalse(os.path.lexists(self.out / 'tmp' / 'app-notarization-log.json'))
        self.assertTrue(any(label == 'step 6 notarization log' for writer in self.private for label, _ in writer.handed))

    def test_staple_may_add_only_the_ticket(self):
        def careless(argv):
            app = Path(argv[-1])
            if app.suffix == '.app':
                (app / 'Contents/CodeResources').write_bytes(b'ticket')
                (app / 'Contents/Resources/codex/codex-resources/input.txt').write_bytes(b'changed by stapling')
                return Result(0, b'The staple and validate action worked!\n')
        self.failing(('stapler', 'staple'), careless, 'S7_ONLY_TICKET')

    def test_archiving_for_submission_may_not_change_the_app(self):
        self.fake.ditto_effect = lambda app: os.chmod(app / 'Contents/Resources/codex/bin', 0o700)
        _, executed = self.failing(None, None, 'S6_ARCHIVE_CHANGED')
        self.assertFalse(any(a[1:3] == ['notarytool', 'submit'] for a in executed))

    def test_signed_entitlements_other_than_the_two_keys_stop(self):
        self.fake.app_entitlements_override = plistlib.dumps({'com.apple.application-identifier': fx.TEAM + '.com.chirality.app',
                                                              'com.apple.developer.team-identifier': fx.TEAM,
                                                              'com.apple.security.get-task-allow': True})
        self.failing(None, None, 'S5_ENTITLEMENTS')

    def test_profile_for_another_app_id_stops_before_signing(self):
        self.profile.write_bytes(fx.profile_bytes(identifier='com.example.other'))
        _, executed = self.failing(None, None, 'S2_PROFILE')
        self.assertEqual(self.signing_calls(executed), [])

    def test_copy_check_catches_changed_modes(self):
        real = shutil.copytree
        def careless(src, dst, *args, **kw):
            done = real(src, dst, *args, **kw)
            if Path(dst).name == common.APP_NAME:
                os.chmod(Path(dst) / 'Contents/Resources/codex/bin', 0o700)
            return done
        with patch.object(owner.shutil, 'copytree', careless):
            self.failing(None, None, 'S1_COPY')

    def test_interruption_and_timeout_stop_with_a_record(self):
        for error, code in ((KeyboardInterrupt(), 'INTERRUPTED'), (TimeoutError('invented-owner-alias QQQQ11111Q'), 'S6_UNEXPECTED')):
            with self.subTest(code=code):
                self.setUp()
                def run(argv, **kw):
                    if argv[1:3] == ['notarytool', 'submit']:
                        raise error
                    return self.fake(argv, **kw)
                status, stdout, stderr = self.main(runner=run)
                self.assertEqual(status, 3)
                self.assertEqual(stderr, 'STOP: ' + common.REASONS[code] + '\n')
                self.assertEqual(json.loads((self.out / 'STOPPED.json').read_text())['reason_code'], code)

    def test_guard_refuses_forbidden_signing_calls(self):
        app, dmg = self.root / 'x' / common.APP_NAME, self.root / 'x.dmg'
        for argv in ([owner.CODESIGN, '--sign', 'n', '--deep', str(app)], [owner.CODESIGN, '--sign', 'n', '--force', str(app)],
                     [owner.CODESIGN, '--sign', 'n', str(app / 'Contents/Resources/codex/bin/codex')],
                     [owner.CODESIGN, '--sign', 'n', str(app / 'Contents/MacOS/chirality-app-v4')]):
            with self.subTest(argv=argv), self.assertRaises(common.Failure):
                owner.guard(argv, app, dmg, [])
        signed = []
        owner.guard([owner.CODESIGN, '--sign', 'n', str(app)], app, dmg, signed)
        with self.assertRaises(common.Failure):
            owner.guard([owner.CODESIGN, '--sign', 'n', str(app)], app, dmg, signed)


class Reasons(unittest.TestCase):
    """Every STOP and build failure uses a reason from the one closed list; each names its step and observation."""

    def test_every_reason_names_its_step_and_observation(self):
        for code, text in common.REASONS.items():
            with self.subTest(code=code):
                prefix = text.split(':', 1)[0]
                self.assertRegex(prefix, r'^(step \d{1,2}|refused|guard|unexpected|interrupted|build)$')
                if code.startswith('S'):
                    self.assertEqual(prefix, 'step ' + code[1:].split('_', 1)[0])
                self.assertGreater(len(text.split(':', 1)[1].split()), 4)
        with self.assertRaises(ValueError):
            common.Failure('NOT_A_LISTED_REASON')

    def test_every_code_raised_in_the_tools_is_listed(self):
        for name in ('owner_sign.py', 'build.py', 'common.py', 'observations.py', 'record.py'):
            tree = ast.parse((RELEASE_DIR / name).read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and getattr(node.func, 'id', getattr(node.func, 'attr', None)) in ('Failure', 'check', 'act', 'observe'):
                    for arg in node.args:
                        if isinstance(arg, ast.Constant) and isinstance(arg.value, str) and arg.value.isupper():
                            self.assertIn(arg.value, common.REASONS, (name, arg.value))
                        if isinstance(arg, ast.JoinedStr):
                            suffix = ''.join(v.value for v in arg.values if isinstance(v, ast.Constant))
                            self.assertTrue(any(k.endswith(suffix.lstrip('S')) for k in common.REASONS), (name, suffix))


class NoPrivateReader(unittest.TestCase):
    """No code path reads the private folder: only PrivateWriter writes there, it has no read method, and every
    path the tools accept is refused by name when it lies inside such a folder. The suite guard, a convention
    with the limits its docstring states, is tested in release_build_test.py."""

    def test_only_the_writer_touches_the_private_folder(self):
        for path in sorted(RELEASE_DIR.glob('*.py')):
            text = path.read_text()
            uses = [line for line in text.splitlines() if 'PRIVATE_FOLDER' in line and not line.lstrip().startswith('#')]
            if path.name == 'common.py':
                self.assertEqual(len([u for u in uses if 'self.folder' in u]), 1)
                self.assertEqual(len([u for u in uses if 'in parts' in u]), 1)  # is_private_path: by name only
            else:
                self.assertTrue(all("'private_folder': common.PRIVATE_FOLDER" in u for u in uses), (path.name, uses))
        writer = common.PrivateWriter
        self.assertEqual([n for n in vars(writer) if not n.startswith('_')], ['write'])


class Secrets(Base):
    """Nothing a tool did not construct or select reaches a returnable file or an output stream."""

    RETURNABLE = ('log.jsonl', 'notary/app-notarization.json', 'notary/disk-image-notarization.json', 'PACKAGE_IDENTITY.json',
                  'RESULT.json', 'STOPPED.json')

    def returnable(self, *streams):
        texts = list(streams)
        for name in self.RETURNABLE:  # the named returnable files; the output folder is never walked
            path = self.out / name
            if path.is_file():
                text = path.read_text()
                texts.append(text)
                values = [json.loads(line) for line in text.splitlines()] if path.suffix == '.jsonl' else [json.loads(text)]
                for value in values:
                    allowed = {('--sign', fx.IDENTITY), ('--keychain-profile', fx.NOTARY), ('-R', '=' + fx.REQUIREMENT)}
                    common.validate_returnable(value, {fx.TEAM, common.SUPPLIER_TEAM}, argv_allowed=allowed)
        return '\n'.join(texts)

    def assert_clean(self, text):
        for secret in SECRETS:
            self.assertNotIn(secret, text)

    def inject_everywhere(self):
        """Secret-looking values in every field a declared form leaves free: they reach the private writer only."""
        self.fake.display_format = 'password=invented-secret someone@example.com QQQQ11111Q abcd-efgh-ijkl-mnop Apple ID'
        self.fake.log_changes = {'ticketContents': [{'password': 'invented-secret', 'developerAccount': 'invented-owner-account',
                                                     'teamId': 'ABCDEFGHIJ', 'keychainProfile': 'other-notary-profile',
                                                     'message': 'Apple ID: invented-owner-alias ' + PEM}],
                                 'statusSummary': 'note abcd-efgh-ijkl-mnop someone@example.com',
                                 'archiveFilename': 'invented-owner@example.invalid.zip'}
        self.fake.supplier = {'codex': {'entitlements': {'account': 'invented-owner-account', 'password': 'invented-secret',
                                                         'keychainProfile': 'other-notary-profile',
                                                         'com.apple.security.cs.allow-jit': True}}}

    def test_completed_run(self):
        self.inject_everywhere()
        code, stdout, stderr = self.main()
        self.assertEqual(code, 0, stderr)
        self.assert_clean(self.returnable(stdout, stderr))
        identity = json.loads((self.out / 'PACKAGE_IDENTITY.json').read_text())
        codex = identity['observed']['signatures']['Contents/Resources/codex/bin/codex']
        self.assertEqual(codex['entitlements'], {'com.apple.security.cs.allow-jit': True})
        self.assertEqual(codex['unexpected_entitlements'], 3)

    def test_profile_name_that_is_a_substring_of_a_secret(self):
        for profile, summary in (('abcd', 'abcd-efgh-ijkl-mnop'), ('password', 'password invented-secret')):
            with self.subTest(profile=profile):
                self.setUp()
                self.fake.log_changes = {'statusSummary': summary}
                code, stdout, stderr = self.main(notary_profile=profile)
                self.assertEqual(code, 0, stderr)
                text = self.returnable(stdout, stderr)
                self.assertNotIn('abcd-efgh-ijkl-mnop', text)
                self.assertNotIn('invented-secret', text)

    def test_stop_text_exception_text_and_stopped_json(self):
        # undeclared lines carrying secrets: no observation, and the stop names nothing from them
        cases = [dict(submit_extra={'status': 'password=invented-secret someone@example.com QQQQ11111Q'}),
                 dict(submit_extra={'message': PEM, 'password': 'invented-secret', 'developerAccount': 'invented-owner-account',
                                    'keychainProfile': 'other-notary-profile', 'teamId': 'ABCDEFGHIJ'}),
                 dict(spctl_extra='origin=Apple ID someone@example.com QQQQ11111Q\n'),
                 dict(display_extra='Note=password=invented-secret someone@example.com QQQQ11111Q abcd-efgh-ijkl-mnop Apple ID\n')]
        for fake in cases:
            self.setUp()
            self.inject_everywhere()
            for key, value in fake.items():
                setattr(self.fake, key, value)
            code, stdout, stderr = self.main()
            self.assertEqual(code, 3)
            self.assert_clean(self.returnable(stdout, stderr))
        for error in (RuntimeError('Apple ID: invented-owner-alias; keychain profile other-notary-profile ' + PEM),
                      OSError(2, 'No such file', '/private/tmp/invented-owner@example.invalid.dmg')):
            with self.subTest(error=type(error).__name__):
                self.setUp()
                def explode(argv, **kw):
                    if argv[0] == owner.DITTO:
                        raise error
                    return self.fake(argv, **kw)
                code, stdout, stderr = self.main(runner=explode)
                self.assertEqual(stderr, 'STOP: ' + common.REASONS['S6_UNEXPECTED'] + '\n')
                self.assert_clean(self.returnable(stdout, stderr))

    def test_unknown_arguments_are_not_echoed(self):
        err = io.StringIO()
        with patch('sys.stderr', err), self.assertRaises(SystemExit):
            owner.main(self.argv() + ['--password', 'invented-secret'], runner=self.fake, environ=ENV, host=HOST, now=NOW)
        self.assertNotIn('invented-secret', err.getvalue())
        self.assertIn('usage error', err.getvalue())

    def test_refusal_text(self):
        code, stdout, stderr = self.main(notary_profile='someone@example.com')
        self.assertEqual((code, stdout), (3, ''))
        self.assertEqual(stderr, 'STOP: ' + common.REASONS['REFUSED_NOTARY_PROFILE'] + '\n')
        self.assertFalse(self.out.exists())


class RecordCheck(unittest.TestCase):
    """`check` validates the record's structure and reports differences by fixed category."""

    def setUp(self):
        self.case = OwnerSign('test_full_run_follows_the_plan_and_writes_a_record_that_checks')
        self.case.setUp(); self.addCleanup(self.case.temp.cleanup)
        self.case.sign()
        self.out = self.case.out
        self.identity = json.loads((self.out / 'PACKAGE_IDENTITY.json').read_text())
        self.dmg = self.out / 'Chirality-4.0.0.dmg'
        self.mounted = fx.make_mount_copy(self.out / 'staging', self.case.root / 'mounted')
        self.app = self.mounted / common.APP_NAME

    def result(self, **kw):
        return record.check(self.identity, dmg=self.dmg, app=self.app, run=self.case.fake, record_dir=self.out, **kw)

    def assert_found(self, *prefixes, failed=(), **kw):
        result = self.result(**kw)
        self.assertFalse(result['equal'])
        for prefix in prefixes:
            self.assertTrue(any(k.startswith(prefix) for k in result['differences']), (prefix, result['differences']))
        for name in failed:
            self.assertIn(name, result['failed_observations'])
        return result

    def test_unchanged_package_is_equal_and_names_what_it_did_not_check(self):
        result = self.result()
        self.assertEqual((result['equal'], result['differences'], result['failed_observations']), (True, {}, {}))
        self.assertEqual(result['not_checked'], [record.NOT_CHECKED_LOGS, record.NOT_CHECKED_CANDIDATE])
        self.assertEqual(self.result(candidate_dir=self.case.candidate)['not_checked'], [record.NOT_CHECKED_LOGS])

    def test_package_bytes(self):
        with open(self.dmg, 'ab') as handle: handle.write(b'x')
        self.assert_found('package.s')

    def test_vendor_file(self):
        (self.app / 'Contents/Resources/codex/codex-resources/input.txt').write_bytes(b'changed')
        self.assert_found('observed.vendor', 'observed.app_as_signed', 'observed.app_as_stapled')

    def test_app_ticket(self):
        (self.app / 'Contents/CodeResources').write_bytes(b'another ticket')
        self.assert_found('observed.app_as_stapled', 'observed.stapled_tickets.app.ticket_sha256')
        (self.app / 'Contents/CodeResources').unlink()
        self.assert_found(failed=('ticket validation', 'stapled ticket absent'))

    def test_signer_and_profile(self):
        self.case.fake.app_entitlements_override = plistlib.dumps({'com.apple.security.get-task-allow': True})
        self.assert_found('observed.signatures..', failed=('entitlements', 'debugging entitlement'))
        self.case.fake.app_entitlements_override = None
        (self.app / 'Contents/embedded.provisionprofile').write_bytes(fx.profile_bytes(team='OTHER00001', prefix='OTHER00001'))
        self.assert_found('observed.provisioning_profile')

    def test_a_profile_with_a_key_twice_is_a_failure(self):
        """Of the same kind as round 4 finding 1: the profile's App identifier twice is not read as the last one."""
        twice = lambda xml: xml.replace(b'<key>com.apple.developer.team-identifier</key>',
                                        b'<key>com.apple.application-identifier</key><string>8A7JL35U4S.com.chirality.app</string>'
                                        b'<key>com.apple.developer.team-identifier</key>', 1)
        (self.app / 'Contents/embedded.provisionprofile').write_bytes(fx.profile_bytes(identifier='com.example.other', content=twice))
        failures = []
        facts = record.profile_facts(self.app, {fx.TEAM}, failures)
        self.assertEqual((facts['decoded'], [f['observation'] for f in failures]), (False, ['provisioning profile']))

    def test_incomplete_display_and_negative_assessment_are_failures(self):
        fake = self.case.fake
        fake.override[('-d', '--verbose=3')] = Result(0, b'', b'Identifier=com.chirality.app\nTeamIdentifier=8A7JL35U4S\n')
        fake.override[('-t', 'open')] = lambda argv: Result(0, b'', f'{argv[-1]}: not accepted\nsource=Notarized Developer ID\n'.encode())
        self.assert_found('observed.gatekeeper', failed=('signature', 'gatekeeper'))

    def test_hardened_runtime_off_at_reading_is_a_failure_not_a_fact(self):
        """Round 3 finding 4, at check time: runtime false is never reported as equal or recorded beside success."""
        fake = self.case.fake
        real = fake.codesign
        fake.codesign = lambda rest: Result(0, b'', real(rest).stderr.replace(b'flags=0x10000(runtime)', b'flags=0x0(none)')) \
            if rest[:2] == ['-d', '--verbose=3'] else real(rest)
        self.assert_found(failed=('hardened runtime',))

    def test_record_structure_is_required_and_the_archive_always_compared(self):
        broken = json.loads(json.dumps(self.identity))
        del broken['notarization']['app']['submitted']
        result = record.check(broken, dmg=self.dmg, app=self.app, run=self.case.fake, record_dir=self.out)
        self.assertEqual(result['record_structure_missing'], ['notarization.app.submitted'])
        self.assertFalse(result['equal'])
        (self.out / 'notary/Chirality-4.0.0-app.zip').write_bytes(b'wrong archive')
        self.assert_found(failed=('submitted file',))

    def test_notarization_fields_and_provenance(self):
        for key, field, value in (('app', 'status', 'Invalid'), ('app', 'submission_id', 'x'), ('disk_image', 'submitted_sha256', '0' * 64),
                                  ('disk_image', 'summary_sha256', '0' * 64), ('app', 'original_log_sha256', '0' * 64)):
            with self.subTest(key=key, field=field):
                original = self.identity['notarization'][key][field]
                self.identity['notarization'][key][field] = value
                self.assert_found(f'notarization.{key}.{field}')
                self.identity['notarization'][key][field] = original
        self.identity['candidate']['source_revision'] = '0' * 40
        self.assertTrue(self.result()['equal'])  # without --candidate, provenance is listed as not checked
        self.assert_found('candidate.source_revision', candidate_dir=self.case.candidate)

    def run_cli(self, record_path):
        out, err = io.StringIO(), io.StringIO()
        code = record.main(['check', str(record_path), '--dmg', str(self.dmg), '--app', str(self.app)], run=self.case.fake, stdout=out, stderr=err)
        return code, out.getvalue(), err.getvalue()

    def test_names_read_from_files_never_reach_the_output(self):
        """Round 3 finding 2: a vendor file or a record key named like a secret is counted, not named."""
        secret = 'password=invented-secret someone@example.invalid'
        (self.app / 'Contents/Resources/codex/codex-resources' / secret).write_bytes(b'x')
        tampered = json.loads(json.dumps(self.identity))
        tampered['observed'][secret] = 'x'
        tampered['notarization']['app'][secret] = 'x'
        path = self.case.root / 'tampered.json'
        path.write_text(json.dumps(tampered))
        code, out, err = self.run_cli(path)
        self.assertEqual(code, 1)
        self.assertNotIn('invented-secret', out + err)
        self.assertNotIn('someone@example.invalid', out + err)
        result = json.loads(out)
        self.assertTrue(any('(an entry not named)' in k for k in result['differences']))
        vendor_paths = record.committed_vendor_paths('9.9.9')
        for key in result['differences']:
            location = key.rsplit(': ', 1)[0].replace(' (an entry not named)', '')
            for segment in location.split('.'):
                self.assertTrue(segment in record.FIELD_NAMES or segment in vendor_paths or segment == '', (segment, key))

    def test_command_line_reports_a_fixed_message_without_a_traceback(self):
        out, err = io.StringIO(), io.StringIO()
        code = record.main(['check', str(self.out / 'PACKAGE_IDENTITY.json'), '--dmg', str(self.case.root / 'invented-owner@example.invalid.dmg'),
                            '--app', str(self.app)], run=self.case.fake, stdout=out, stderr=err)
        self.assertEqual(code, 2)
        self.assertNotIn('invented-owner', err.getvalue())
        self.assertNotIn('Traceback', err.getvalue())
        self.assertNotIn(str(self.case.root), err.getvalue())

    def test_round_4_paths_inside_the_private_folder_are_refused_before_reading(self):
        """Round 4 finding 3: a record path, a summary or a submitted file inside the private folder is never read."""
        private = self.case.root / common.PRIVATE_FOLDER
        real_read = Path.read_bytes
        read = []
        def spy(path):
            read.append(str(path))
            return real_read(path)
        with patch.object(Path, 'read_bytes', spy):
            for argv in (['check', str(private / 'PACKAGE_IDENTITY.json'), '--dmg', str(self.dmg), '--app', str(self.app)],
                         ['check', str(self.out / 'PACKAGE_IDENTITY.json'), '--dmg', str(private / 'x.dmg'), '--app', str(self.app)],
                         ['check', str(self.out / 'PACKAGE_IDENTITY.json'), '--dmg', str(self.dmg), '--app', str(self.app),
                          '--candidate', str(private)]):
                with self.subTest(argv=argv[1:3]):
                    out, err = io.StringIO(), io.StringIO()
                    self.assertEqual(record.main(argv, run=self.case.fake, stdout=out, stderr=err), 2)
            entry = dict(self.identity['notarization']['app'])
            for record_dir, changes in ((private, {}), (self.out, {'summary': common.PRIVATE_FOLDER + '/app-notarization.json'})):
                with self.subTest(record_dir=record_dir.name, changes=changes):
                    _, failures = record.notarization_facts(record_dir, entry | changes)
                    self.assertEqual([f['observation'] for f in failures], ['notarization summary'])
            _, failures = record.notarization_facts(self.out, entry | {'submitted': common.PRIVATE_FOLDER + '/Chirality-4.0.0-app.zip'})
            self.assertEqual([f['observation'] for f in failures], ['submitted file'])
        self.assertFalse([path for path in read if common.PRIVATE_FOLDER in path], read)

    def test_the_original_log_options_are_gone(self):
        err = io.StringIO()
        with patch('sys.stderr', err), self.assertRaises(SystemExit):
            record.main(['check', str(self.out / 'PACKAGE_IDENTITY.json'), '--dmg', str(self.dmg), '--app', str(self.app),
                         '--app-original-log', str(self.case.root / 'any.json')], run=self.case.fake)
        self.assertIn('usage error', err.getvalue())


if __name__ == '__main__':
    unittest.main()
