"""The owner's signing procedure and the package identity record, on invented material.

No signing, notarization, stapling, Gatekeeper or keychain tool runs: every
Apple command goes to owner_fixtures.FakeApple, whose outputs are the forms
declared in app/packaging/release/observations.py. No test opens, lists, walks
or stats anything in the private folder: the tools are given an in-memory
writer, and the one test of the real writer takes the modes it reports.
"""
import argparse
import ast
import base64
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
        # the reason, then one line for each refusal STOPPED.json holds (fixed text and integers), and nothing else
        details = stopped['refusals'] + [f['detail'] for f in stopped['failed_observations'] if 'detail' in f]
        self.assertEqual(stderr, 'STOP: ' + common.REASONS[code] + '\n' + ''.join('  ' + common.describe(d) + '\n' for d in details))
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
        # OWNER: the owner's report of a line's form with its values removed, only where no published source shows it.
        sources = {'TN3126', 'TN3127', 'TN3161', 'TN3125', 'NOTARY', 'WITNESS', 'ADVANCE', 'RUN1103', 'OWNER report'}
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


def whole_document_probes():
    """The fifth reading's three probes, built from the expected entitlements at run time: values plistlib would have
    read as the expected dictionary, while the document also holds something else."""
    right = ENTITLEMENTS_XML
    wrong = plistlib.dumps({'com.apple.application-identifier': 'OTHER00001.com.example.other', 'com.apple.security.get-task-allow': True})
    wrong_dict = wrong[wrong.index(b'<dict>'):wrong.index(b'</dict>') + len(b'</dict>')]
    return {
        'two conflicting dictionaries': right.replace(b'<dict>', wrong_dict + b'\n<dict>', 1),
        'undeclared text before the dictionary': right.replace(b'<dict>', b'failed to read entitlements\n<dict>', 1),
        'a sibling string before the dictionary': right.replace(b'<dict>', b'<string>failed to read entitlements</string>\n<dict>', 1),
    }


class WholeEntitlementDocument(Base):
    """Round 5 finding: the entitlement reader returned a value that was not the whole document. A value is now
    returned only when the original document, read by its own bytes without plistlib, equals plistlib's writing of
    that value, apart from the document header and whitespace between elements."""

    CONTROLS = {
        'the expected entitlements': ENTITLEMENTS_XML,
        'keys in their own order, a boolean and a list': plistlib.dumps(
            {'keychain-access-groups': ['8A7JL35U4S.com.chirality.app'], 'com.apple.security.cs.allow-jit': True,
             'com.apple.application-identifier': '8A7JL35U4S.com.chirality.app'}, sort_keys=False),
        'CRLF line ends and spaces between elements': ENTITLEMENTS_XML.replace(b'\n', b'\r\n').replace(b'\t', b'    '),
        'no entitlements': plistlib.dumps({}),
        'whitespace inside a value kept': plistlib.dumps({'com.apple.application-identifier': ' 8A7JL35U4S.x '}),
    }

    def test_ordinary_entitlements_are_read_and_the_fifth_probes_refuse(self):
        for name, raw in self.CONTROLS.items():
            with self.subTest(control=name):
                self.assertEqual(obs.observe('entitlements', Result(0, raw), subject='/invented/asked'),
                                 plistlib.loads(raw))
        for name, raw in whole_document_probes().items():
            with self.subTest(probe=name):
                self.assertIsInstance(plistlib.loads(raw), dict)  # what plistlib alone accepted
                with self.assertRaises(obs.ObservationFailed):
                    obs.observe('entitlements', Result(0, raw), subject='/invented/asked')

    def test_the_original_is_read_without_discarding_what_plistlib_dropped(self):
        """The comparison's basis: the original's own reading keeps what plistlib's value lost, so the two differ."""
        for name, raw in whole_document_probes().items():
            with self.subTest(probe=name):
                header, body = obs.xml_structure(raw)
                _, emitted = obs.xml_structure(plistlib.dumps(plistlib.loads(raw), sort_keys=False))
                self.assertEqual(header, obs.xml_structure(ENTITLEMENTS_XML)[0])
                kept = {'two conflicting dictionaries': b'OTHER00001.com.example.other'}.get(name, b'failed to read entitlements')
                self.assertIn(kept, body)
                self.assertNotIn(kept, emitted)
        # The two normalizations, and no others: the header by its declaration and type, whitespace between elements.
        header, body = obs.xml_structure(ENTITLEMENTS_XML)
        self.assertEqual([kind for kind, _ in header], ['xml declaration', 'document type'])
        self.assertEqual(body, b''.join(line.strip(b'\t') for line in ENTITLEMENTS_XML.split(b'\n')[2:]))
        spelled = {'a comment': (b'<dict>', b'<!-- x --><dict>'), 'a processing instruction': (b'<dict>', b'<?x y?><dict>'),
                   'an attribute': (b'<dict>', b'<dict id="x">'), 'an unknown element': (b'<dict>', b'<dict><x/>'),
                   'a character reference': (b'>8A7JL35U4S<', b'>&#56;A7JL35U4S<'),
                   'no document type': (ENTITLEMENTS_XML.split(b'\n')[1] + b'\n', b''),
                   'a comment in the header': (b'<plist', b'<!-- x -->\n<plist')}
        for name, (old, new) in spelled.items():
            with self.subTest(spelled=name), self.assertRaises(ValueError):
                obs.load_xml_plist(ENTITLEMENTS_XML.replace(old, new, 1))
        for name, raw in {'an entity declared': ENTITLEMENTS_XML.replace(b'.dtd">', b'.dtd" [<!ENTITY e "z">]>'),
                          'an undefined entity': ENTITLEMENTS_XML.replace(b'8A7JL35U4S</string>', b'8A7JL35U4S&e;</string>', 1)}.items():
            with self.subTest(entity=name), self.assertRaises(ValueError):
                obs.load_xml_plist(raw)

    def assert_stops(self, override, reason, *, supplier=False):
        self.fake = fx.FakeApple()
        if supplier:
            self.fake.override[('--entitlements',)] = lambda argv: Result(0, override) if '/Contents/Resources/codex/' in argv[-1] else None
        else:
            self.fake.app_entitlements_override = override
        code, stdout, stderr = self.main()
        self.assertEqual(code, 3, stderr)
        self.assertEqual(json.loads((self.out / 'STOPPED.json').read_text())['reason_code'], reason)
        self.assertFalse((self.out / 'PACKAGE_IDENTITY.json').exists())
        self.assertFalse((self.out / 'RESULT.json').exists())
        last = self.fake.calls[-1]
        self.assertEqual((last[0], last[1:4]), (owner.CODESIGN, ['-d', '--entitlements', '-']))
        self.assertFalse([a for a in self.fake.calls if '--sign' in a and a[-1].endswith('.dmg')])

    def test_a_full_run_stops_on_each_probe_and_writes_no_record(self):
        """The fifth reading's full run: the App's entitlements as two conflicting dictionaries completed a record that
        then checked equal. Each probe now stops at the App's verification (S5) or, for a supplier executable, at the
        reading before signing (S0); and a truthful run beside them completes."""
        runs = 0
        for name, raw in whole_document_probes().items():
            for supplier, reason in ((False, 'S5_ENTITLEMENTS'), (True, 'S0_ENTITLEMENTS')):
                with self.subTest(probe=name, supplier=supplier):
                    runs += 1
                    self.out = self.root / f'signed-{runs}'
                    self.assert_stops(raw, reason, supplier=supplier)
        self.out = self.root / 'signed-control'
        self.fake = fx.FakeApple()
        code, stdout, stderr = self.main()
        self.assertEqual(code, 0, stderr)
        self.assertTrue((self.out / 'PACKAGE_IDENTITY.json').is_file())


# --- The whole-document FILE reader (app/packaging/production_inputs/whole_plist.py), on invented documents. ---
# Every value here is invented: the team identifiers, App IDs, UUID and dates name nothing real, and the profile
# envelopes are built from invented bytes and are never Apple-signed. Beside each refusal is a control that reads.
WHOLE = common.prepare.whole_plist
PLIST_HEADER = (b'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" '
          b'"http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n')
READER_TEAM, READER_OTHER = 'ZZINVENT01', 'QQOTHER001'
READER_EXPECTED = {'com.apple.application-identifier': READER_TEAM + '.invalid.example.reader', 'com.apple.developer.team-identifier': READER_TEAM}
READER_DICT = (b'<dict>\n\t<key>com.apple.application-identifier</key>\n\t<string>ZZINVENT01.invalid.example.reader</string>\n'
                 b'\t<key>com.apple.developer.team-identifier</key>\n\t<string>ZZINVENT01</string>\n</dict>')
# Another team's App ID with get-task-allow: the first of the conflicting pair.
OTHER_READER_DICT = (b'<dict>\n\t<key>com.apple.application-identifier</key>\n\t<string>QQOTHER001.invalid.example.other</string>\n'
              b'\t<key>com.apple.developer.team-identifier</key>\n\t<string>QQOTHER001</string>\n'
              b'\t<key>com.apple.security.get-task-allow</key>\n\t<true/>\n</dict>')


def plist_document(body, header=PLIST_HEADER, after=b''):
    return header + b'<plist version="1.0">\n' + body + b'\n</plist>\n' + after


def inside_reader_dict(extra, at=b'\t<key>com.apple.developer.team-identifier</key>'):
    """The expected dictionary with `extra` placed before its second key."""
    return plist_document(READER_DICT.replace(at, extra + at, 1))


READER_CONTROL = plist_document(READER_DICT)
READER_REFUSED = {
    # name: (document, (what was found, kind, field where it was found))
    'conflicting pair: two sibling dictionaries': (plist_document(OTHER_READER_DICT + b'\n' + READER_DICT), ('a second value under plist', 'malformed', 'plist')),
    'text before the expected dictionary': (plist_document(b'stray text' + READER_DICT), ('text outside a value', 'malformed', 'plist')),
    'a sibling string': (plist_document(READER_DICT + b'\n<string>' + READER_OTHER.encode() + b'</string>'), ('a second value under plist', 'malformed', 'plist')),
    'an unknown element in the dictionary': (inside_reader_dict(b'<note>' + READER_OTHER.encode() + b'</note>\n'),
                                             ('an element that is not a property-list element', 'malformed', 'dict')),
    'an unknown element under plist': (plist_document(b'<note/>' + READER_DICT), ('an element that is not a property-list element', 'malformed', 'plist')),
    'an attribute': (plist_document(READER_DICT.replace(b'<dict>', b'<dict team="' + READER_OTHER.encode() + b'">', 1)),
                     ('an attribute other than the root version', 'malformed', 'dict')),
    'an attribute on the root other than version': (READER_CONTROL.replace(b'<plist version="1.0">', b'<plist version="1.0" team="x">'),
                                                    ('an attribute other than the root version', 'malformed', 'plist')),
    'a comment': (inside_reader_dict(b'<!-- ' + READER_OTHER.encode() + b' -->\n'), ('a comment', 'unsupported', 'dict')),
    'a comment in the header': (plist_document(READER_DICT, header=PLIST_HEADER + b'<!-- invented -->\n'), ('a comment', 'unsupported', 'document header')),
    'a processing instruction': (inside_reader_dict(b'<?invented ' + READER_OTHER.encode() + b'?>\n'), ('a processing instruction', 'unsupported', 'dict')),
    'a key twice': (inside_reader_dict(b'<key>com.apple.application-identifier</key><string>QQOTHER001.invalid.example.other</string>\n'),
                    ('a key twice in one dictionary', 'malformed', 'dict')),
    'a dictionary with a key and no value': (plist_document(b'<dict><key>com.apple.application-identifier</key></dict>'), ('a key with no value', 'malformed', 'dict')),
    'a key followed by a key': (inside_reader_dict(b'<key>invented</key>\n'), ('a key with no value', 'malformed', 'dict')),
    'a value with no key': (inside_reader_dict(b'<string>' + READER_OTHER.encode() + b'</string>\n'), ('a value with no key', 'malformed', 'dict')),
    'an entity declaration': (plist_document(READER_DICT.replace(b'ZZINVENT01</string>\n</dict>', b'&team;</string>\n</dict>'),
                                       header=b'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist [<!ENTITY team "QQOTHER001">]>\n'),
                              ('an entity declaration', 'unsupported', 'document header')),
    'an undefined entity': (plist_document(READER_DICT.replace(b'ZZINVENT01</string>\n</dict>', b'&team;</string>\n</dict>')),
                            ('an undefined or external entity reference', 'malformed', 'document')),
    'trailing bytes after the document': (plist_document(READER_DICT, after=b'<plist version="1.0"><dict/></plist>'),
                                          ('bytes after the document element', 'malformed', 'after the root element')),
    'trailing text after the document': (plist_document(READER_DICT, after=b'QQOTHER001'), ('bytes after the document element', 'malformed', 'after the root element')),
    'a comment after the document': (plist_document(READER_DICT, after=b'<!-- invented -->'), ('a comment', 'unsupported', 'after the root element')),
    'a character reference between elements': (plist_document(b'&#32;' + READER_DICT), ('text outside a value', 'malformed', 'plist')),
    'a CDATA section between elements': (plist_document(b'<![CDATA[ ]]>' + READER_DICT), ('text outside a value', 'malformed', 'plist')),
    'no value under plist': (plist_document(b''), ('no value under plist', 'malformed', 'plist')),
    'a key outside a dictionary': (plist_document(b'<array><key>a</key></array>'), ('a key outside a dictionary', 'malformed', 'array')),
    'an element inside a string': (plist_document(b'<string>a<string>b</string></string>'), ('an element inside a leaf value', 'malformed', 'string')),
    'a binary property list': (plistlib.dumps(READER_EXPECTED, fmt=plistlib.FMT_BINARY),
                               ('a binary property list', 'unsupported', 'document')),
    'another document type': (plist_document(READER_DICT, header=b'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE invented>\n'),
                              ('a document type other than the property-list one', 'unsupported', 'document header')),
    'another encoding': (plist_document(READER_DICT, header=PLIST_HEADER.replace(b'UTF-8', b'ISO-8859-1')),
                         ('a declared encoding other than UTF-8', 'unsupported', 'document header')),
    'review: Shift_JIS declared (the parser raised ValueError)': (plist_document(READER_DICT, header=PLIST_HEADER.replace(b'UTF-8', b'Shift_JIS')),
                                                                 ('a declared encoding other than UTF-8', 'unsupported', 'document header')),
    'review: an unknown encoding declared (the parser raised LookupError)': (
        plist_document(READER_DICT, header=PLIST_HEADER.replace(b'UTF-8', b'x-invented-encoding')),
        ('a declared encoding other than UTF-8', 'unsupported', 'document header')),
    'UTF-16 declared in single quotes': (plist_document(READER_DICT, header=b"<?xml version='1.0' encoding='UTF-16'?>\n"),
                                         ('a declared encoding other than UTF-8', 'unsupported', 'document header')),
    'a standalone declaration': (plist_document(READER_DICT, header=b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'),
                                 ('an XML declaration other than version 1.0, or with a standalone declaration', 'unsupported', 'document header')),
    'review: a character reference in the root version attribute': (READER_CONTROL.replace(b'version="1.0">', b'version="&#49;.0">'),
                                                                     ('a reference in the root version attribute', 'unsupported', 'plist')),
    'an empty document': (b'', ('an empty document', 'malformed', 'document')),
    'review: XML 1.1 with a character reference XML 1.1 permits': (plist_document(b'<string>&#x1;</string>', header=b'<?xml version="1.1" encoding="UTF-8"?>\n'),
                                                                  ('a declared XML version other than 1.0', 'unsupported', 'document header')),
    'XML 1.1 with an ordinary string': (plist_document(b'<string>x</string>', header=b"<?xml version='1.1'?>\n"),
                                       ('a declared XML version other than 1.0', 'unsupported', 'document header')),
    'review: a reference to another root version': (READER_CONTROL.replace(b'version="1.0">', b'version="&#50;.0">'),
                                                    ('a reference in the root version attribute', 'unsupported', 'plist')),
    'review: a root version 2.0': (READER_CONTROL.replace(b'version="1.0">', b'version="2.0">'),
                                   ('a root version attribute other than 1.0', 'unsupported', 'plist')),
    'whitespace only': (b' \n', ('content that does not begin with an XML declaration', 'unsupported', 'document header')),
    'no XML declaration': (b'<plist version="1.0">' + READER_DICT + b'</plist>', ('content that does not begin with an XML declaration', 'unsupported', 'document header')),
    'a byte order mark': (b'\xef\xbb\xbf' + READER_CONTROL, ('content that does not begin with an XML declaration', 'unsupported', 'document header')),
    # Each leaf value outside its admitted form names its type and the rule it fails (not established).
    'an integer spelled with an underscore': (plist_document(b'<integer>1_0</integer>'), ('an integer outside the admitted grammar', 'unsupported', 'integer')),
    'review: an integer of 65 digits': (plist_document(b'<integer>' + b'1' * 65 + b'</integer>'),
                                        ('an integer longer than 64 characters', 'unsupported', 'integer')),
    'a negative integer of 65 characters': (plist_document(b'<integer>-' + b'1' * 64 + b'</integer>'),
                                            ('an integer longer than 64 characters', 'unsupported', 'integer')),
    'a real spelled as nan': (plist_document(b'<real>nan</real>'), ('a real outside the admitted grammar', 'unsupported', 'real')),
    'a real that overflows': (plist_document(b'<real>1.7976931348623159e308</real>'), ('a real that converts to an infinity', 'unsupported', 'real')),
    'a real that underflows': (plist_document(b'<real>2.4703282292062327e-324</real>'),
                               ('a real that converts to zero from non-zero digits', 'unsupported', 'real')),
    'a partial date': (plist_document(b'<date>2026Z</date>'), ('a date outside the admitted grammar', 'unsupported', 'date')),
    'a date with trailing text': (plist_document(b'<date>2026-01-01T00:00:00Zjunk</date>'), ('a date outside the admitted grammar', 'unsupported', 'date')),
    'review: an impossible date': (plist_document(b'<date>2099-02-29T00:00:00Z</date>'), ('a date naming no real date or time', 'unsupported', 'date')),
    'data with a character outside base64': (plist_document(b'<data>AAAA!!!!</data>'), ('a character outside base64 and whitespace', 'unsupported', 'data')),
    'review: data with @': (plist_document(b'<data>Z@==</data>'), ('a character outside base64 and whitespace', 'unsupported', 'data')),
    'data missing its padding': (plist_document(b'<data>Zg</data>'), ('base64 padding outside the admitted form', 'unsupported', 'data')),
    'data with three pads': (plist_document(b'<data>Zg===</data>'), ('base64 padding outside the admitted form', 'unsupported', 'data')),
    'data padded in the middle': (plist_document(b'<data>Zg==Zg==</data>'), ('base64 padding outside the admitted form', 'unsupported', 'data')),
    'data with unused bits set': (plist_document(b'<data>Zh==</data>'), ('base64 with unused bits not zero', 'unsupported', 'data')),
    'a reference inside an integer': (plist_document(b'<integer>&#49;</integer>'),
                                      ('a reference or CDATA section in a leaf that is not text', 'unsupported', 'integer')),
    'text inside true': (plist_document(b'<true>no</true>'), ('content inside true or false', 'malformed', 'true')),
    'not well-formed': (READER_CONTROL.replace(b'</dict>', b'</array>'), ('not well-formed XML', 'malformed', 'document')),
}


class WholeFileRefusals(unittest.TestCase):
    def test_the_control_reads_the_expected_values(self):
        self.assertEqual(WHOLE.load(READER_CONTROL), READER_EXPECTED)

    def test_each_refusal_names_what_was_found_its_kind_and_where(self):
        for name, (raw, (found, kind, field)) in READER_REFUSED.items():
            with self.subTest(name):
                with self.assertRaises(WHOLE.NotWhole) as raised:
                    WHOLE.load(raw)
                detail = raised.exception.detail()
                self.assertEqual((detail['found'], detail['kind'], detail['field']), (found, kind, field))
                self.assertIsInstance(raised.exception, ValueError)  # every caller already stops on ValueError
                self.assertLessEqual(detail.get('offset', 0), max(len(raw) - 1, 0))
                self.assertEqual(WHOLE.load(READER_CONTROL), READER_EXPECTED)

    def test_the_standard_parser_alone_reads_part_of_the_conflicting_pair(self):
        """What the file readers did before: plistlib keeps the last of two sibling values and ignores the rest."""
        raw = READER_REFUSED['conflicting pair: two sibling dictionaries'][0]
        self.assertEqual(plistlib.loads(raw), READER_EXPECTED)
        for name in ('text before the expected dictionary', 'a comment', 'a processing instruction', 'an attribute',
                     'an unknown element in the dictionary'):
            with self.subTest(name):
                self.assertEqual(plistlib.loads(READER_REFUSED[name][0]), READER_EXPECTED)

    def test_nothing_is_fetched(self):
        external = plist_document(READER_DICT.replace(b'ZZINVENT01</string>\n</dict>', b'&team;</string>\n</dict>'),
                                  header=b'<?xml version="1.0"?>\n<!DOCTYPE plist [<!ENTITY team SYSTEM "http://invalid.example/x">]>\n')
        with patch('urllib.request.urlopen', side_effect=AssertionError('fetched')), self.assertRaises(WHOLE.NotWhole):
            WHOLE.load(external)

    def test_the_two_readers_must_agree(self):
        """The structural reading is not plistlib's: when plistlib reads another value, or refuses, the document refuses
        as not established (the readers disagree; nothing shows which is right)."""
        with patch.object(WHOLE.plistlib, 'loads', return_value=plistlib.loads(plist_document(OTHER_READER_DICT))):
            with self.assertRaises(WHOLE.NotWhole) as raised:
                WHOLE.load(READER_CONTROL)
            self.assertEqual((raised.exception.why, raised.exception.kind), ('the standard parser reads another value', 'unsupported'))
        for error in (plistlib.InvalidFileException(), RecursionError()):
            with self.subTest(error=type(error).__name__), patch.object(WHOLE.plistlib, 'loads', side_effect=error):
                with self.assertRaises(WHOLE.NotWhole) as raised:
                    WHOLE.load(READER_CONTROL)
                self.assertEqual(raised.exception.why, 'the standard parser does not read the document')
        # Types count: a boolean is not the integer 1, though Python compares them equal.
        with patch.object(WHOLE.plistlib, 'loads', return_value={'a': 1}), self.assertRaises(WHOLE.NotWhole):
            WHOLE.load(plist_document(b'<dict><key>a</key><true/></dict>'))
        self.assertEqual(WHOLE.load(READER_CONTROL), READER_EXPECTED)

    def test_nesting_is_refused_by_name_before_any_recursion_can_fail(self):
        """Review round 1, finding 2: a 500-level array raised RecursionError. The limit is MAX_DEPTH arrays and
        dictionaries; deeper is refused by name, however deep."""
        nest = lambda depth: plist_document(b'<array>' * depth + b'<true/>' + b'</array>' * depth)
        self.assertEqual(WHOLE.MAX_DEPTH, 32)
        value = WHOLE.load(nest(32))
        for _ in range(31):
            value = value[0]
        self.assertEqual(value, [True])
        for depth in (33, 500, 6000):
            with self.subTest(depth=depth), self.assertRaises(WHOLE.NotWhole) as raised:
                WHOLE.load(nest(depth))
            self.assertEqual((raised.exception.why, raised.exception.kind, raised.exception.field),
                             ('nesting deeper than 32 arrays and dictionaries', 'unsupported', 'array'))

    def test_a_leaf_is_refused_when_its_conversion_would_lose_what_is_written(self):
        """Review round 1, finding 3: non-zero unused base64 bits, and reals that overflow or underflow a double, read as
        another value. Each is now refused; each control has exactly one spelling of its value."""
        cases = {
            'data with non-zero unused bits (Zh==)': (b'<data>Zh==</data>', b'<data>Zg==</data>', b'f'),
            'data with non-zero unused bits (Zm9=)': (b'<data>Zm9=</data>', b'<data>Zm8=</data>', b'fo'),
            'a real that overflows a double': (b'<real>1e999</real>', b'<real>1e308</real>', 1e308),
            'a negative real that overflows': (b'<real>-1e999</real>', b'<real>-1e308</real>', -1e308),
            'a real that underflows to zero': (b'<real>1e-999</real>', b'<real>0e-999</real>', 0.0),
            'a real that underflows to zero (2e-324)': (b'<real>2e-324</real>', b'<real>5e-324</real>', 5e-324),
            'an integer with +': (b'<integer>+42</integer>', b'<integer>42</integer>', 42),
            'an integer with a leading zero': (b'<integer>0042</integer>', b'<integer>42</integer>', 42),
            'an integer -0': (b'<integer>-0</integer>', b'<integer>0</integer>', 0),
            'a hexadecimal integer': (b'<integer>0x2A</integer>', b'<integer>-42</integer>', -42),
            'an integer of 4500 digits': (b'<integer>' + b'9' * 4500 + b'</integer>', b'<integer>' + b'9' * 64 + b'</integer>', int('9' * 64)),
            'whitespace inside an integer': (b'<integer> 42 </integer>', b'<integer>42</integer>', 42),
            'a CDATA section inside an integer': (b'<integer><![CDATA[42]]></integer>', b'<integer>42</integer>', 42),
            'a character reference inside an integer': (b'<integer>&#52;2</integer>', b'<integer>42</integer>', 42),
            'a character reference inside data': (b'<data>Zg&#32;==</data>', b'<data>Zg ==</data>', b'f'),
            'a CDATA section inside data': (b'<data><![CDATA[Zg==]]></data>', b'<data>\r\nZg==\r\n</data>', b'f'),
            'a fractional date': (b'<date>2099-01-01T00:00:00.1Z</date>', b'<date>2099-01-01T00:00:00Z</date>', datetime.datetime(2099, 1, 1)),
            'a date that is no date': (b'<date>2025-02-29T00:00:00Z</date>', b'<date>2024-02-29T00:00:00Z</date>', datetime.datetime(2024, 2, 29)),
        }
        for name, (refused, control, value) in cases.items():
            with self.subTest(name):
                with self.assertRaises(WHOLE.NotWhole) as raised:
                    WHOLE.load(plist_document(refused))
                self.assertEqual(raised.exception.kind, 'unsupported')
                self.assertEqual(WHOLE.load(plist_document(control)), value)

    def test_the_entitlement_reader_raises_as_it_did(self):
        """Review round 1: the shared event reading changed the exception the entitlement helper raised for an entity.
        Each case raises the class and text it raised on main before this change (plistlib refuses a declared entity
        before the structure is read, so load_xml_plist names that)."""
        undefined = ENTITLEMENTS_XML.replace(b'8A7JL35U4S</string>', b'8A7JL35U4S&e;</string>', 1)
        declared = ENTITLEMENTS_XML.replace(b'.dtd">', b'.dtd" [<!ENTITY e "z">]>')
        for raw, reader, message in ((undefined, obs.xml_structure, 'an entity is declared, skipped or external'),
                                     (undefined, obs.load_xml_plist, 'an entity is declared, skipped or external'),
                                     (declared, obs.xml_structure, 'an entity is declared, skipped or external'),
                                     (declared, obs.load_xml_plist, 'not one XML property list')):
            with self.subTest(reader=reader.__name__, message=message), self.assertRaises(ValueError) as raised:
                reader(raw)
            self.assertIs(type(raised.exception), ValueError)
            self.assertEqual(str(raised.exception), message)


class WholeFileControls(unittest.TestCase):
    """Valid spellings that plistlib would not write, and that a real file may hold, read as their values."""

    def test_data_wrapped_at_several_widths(self):
        payload = bytes(range(256)) * 3
        encoded = base64.b64encode(payload).decode()
        for width in (len(encoded), 76, 68, 60, 52, 4, 1):
            lines = [encoded[i:i + width] for i in range(0, len(encoded), width)]
            for joiner in ('\n', '\n\t', '\r\n\t\t', ' '):
                with self.subTest(width=width, joiner=joiner):
                    raw = plist_document(b'<dict><key>DeveloperCertificates</key><array><data>\n' + joiner.join(lines).encode()
                                         + b'\n</data></array></dict>')
                    self.assertEqual(WHOLE.load(raw), {'DeveloperCertificates': [payload]})

    def test_a_date(self):
        raw = plist_document(b'<dict><key>ExpirationDate</key><date>2099-01-02T03:04:05Z</date></dict>')
        self.assertEqual(WHOLE.load(raw), {'ExpirationDate': datetime.datetime(2099, 1, 2, 3, 4, 5)})

    def test_crlf_line_endings(self):
        self.assertEqual(WHOLE.load(READER_CONTROL.replace(b'\n', b'\r\n')), READER_EXPECTED)

    def test_empty_dictionaries(self):
        for spelling in (b'<dict/>', b'<dict></dict>', b'<dict>\n\t</dict>'):
            with self.subTest(spelling=spelling):
                self.assertEqual(WHOLE.load(plist_document(spelling)), {})
                self.assertEqual(WHOLE.load(plist_document(b'<dict><key>Entitlements</key>' + spelling + b'</dict>')), {'Entitlements': {}})
        self.assertEqual(WHOLE.load(plist_document(b'<array/>')), [])

    def test_whitespace_inside_a_string_is_kept(self):
        raw = plist_document(b'<dict><key> invented key </key><string>  two  spaces\n\tand a tab </string></dict>')
        self.assertEqual(WHOLE.load(raw), {' invented key ': '  two  spaces\n\tand a tab '})

    def test_other_admitted_spellings_of_values(self):
        raw = plist_document(b'<array><true></true><false/><integer>-7</integer><integer>0</integer>'
                             b'<real>1.5e3</real><real>.5</real><real>0.0</real><string>a &amp; b &#x41; <![CDATA[<c>]]></string>'
                             b'<string/></array>')
        self.assertEqual(WHOLE.load(raw), [True, False, -7, 0, 1500.0, 0.5, 0.0, 'a & b A <c>', ''])

    def test_header_spellings(self):
        for header in (b"<?xml version='1.0' encoding='utf-8'?>\n", b'<?xml version="1.0"?>',
                       b"<?xml version='1.0'?>\n<!DOCTYPE plist PUBLIC '-//Apple//DTD PLIST 1.0//EN' "
                       b"'http://www.apple.com/DTDs/PropertyList-1.0.dtd'>\n"):
            with self.subTest(header=header):
                self.assertEqual(WHOLE.load(plist_document(READER_DICT, header=header)), READER_EXPECTED)
        self.assertEqual(WHOLE.load(READER_CONTROL.replace(b'<plist version="1.0">', b'<plist>')), READER_EXPECTED)

    def test_prolog_whitespace_and_a_public_identifier_with_whitespace(self):
        """Review round 3, finding 7: named normalizations (_header)."""
        doctype = b'<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">'
        header = b'<?xml version="1.0" encoding="UTF-8"?>'
        for name, prolog in (('whitespace between declaration, document type and root', header + b'\t\r\n  ' + doctype + b'\r\t'),
                             ('none', header + doctype),
                             ('a public identifier with leading, trailing and inner whitespace',
                              header + doctype.replace(b'-//Apple//DTD PLIST 1.0//EN', b' \r\n-//Apple//DTD  \r\n PLIST 1.0//EN  \n '))):
            with self.subTest(name):
                self.assertEqual(WHOLE.load(prolog + b'<plist version="1.0"><string>x</string></plist>'), 'x')

    def test_what_plistlib_writes_reads(self):
        value = {'CFBundleIdentifier': 'invalid.example.reader', 'Nested': {'List': [1, 2.5, True, b'\x00\xff', 'x']},
                 'When': datetime.datetime(2026, 1, 1)}
        for sort_keys in (True, False):
            self.assertEqual(WHOLE.load(plistlib.dumps(value, sort_keys=sort_keys)), value)


# --- The envelope: each field and each rule, broken alone, beside a control ----------------------------------------
T = fx.tlv
PREPARE = common.prepare
ENVELOPE_CONTENT = plistlib.dumps(fx.profile_value())
RIVAL_CONTENT = plistlib.dumps(fx.profile_value(team='QQOTHER001', prefix='QQOTHER001', identifier='com.example.other'))
SIGNED_OID, DATA_OID_TLV = T(0x06, PREPARE.SIGNED_DATA_OID), T(0x06, PREPARE.DATA_OID)


def signed_data(*fields):
    return T(0x30, SIGNED_OID + T(0xa0, T(0x30, b''.join(fields))))


VERSION, CERTIFICATES, SIGNERS = T(0x02, b'\x01'), T(0xa0, fx.CERTIFICATE), T(0x31, fx.SIGNER_INFO)
ENCAP = T(0x30, DATA_OID_TLV + T(0xa0, T(0x04, ENVELOPE_CONTENT)))
SIGNED_FIELDS = VERSION + fx.DIGEST_ALGORITHMS + ENCAP + CERTIFICATES + SIGNERS  # the control's SignedData fields
CONTROL_ENVELOPE = fx.envelope(ENVELOPE_CONTENT)


def certificate(tbs=T(0x30, T(0x02, b'\x01')), algorithm=fx.SIGNATURE_ALGORITHM, bits=T(0x03, b'\x00INVENTED')):
    return T(0x30, tbs + algorithm + bits)


def with_certificate(cert):
    return fx.envelope(ENVELOPE_CONTENT, after=T(0xa0, cert) + SIGNERS)


def deep(levels):
    inner = T(0x05, b'')
    for _ in range(levels):
        inner = T(0x30, inner)
    return inner


U, MF = 'unsupported', 'malformed'
# name: (envelope, (kind, field, found, item or None)). Each breaks exactly one rule and leaves every other field as the
# control, except where its name says it breaks more (a SignedData cut short omits every field after the first missing
# one, which is the one named). A reason is true of the file; no order between defects is promised. A rival property
# list inside a SET is refused where its bytes cannot be an element within the SET (here its twelfth).
ENVELOPE_CASES = {
    # ContentInfo
    'ContentInfo is not a SEQUENCE': (b'\x31' + CONTROL_ENVELOPE[1:], (MF, 'ContentInfo', 'another tag', None)),
    'a byte after ContentInfo': (CONTROL_ENVELOPE + b'\x00', (MF, 'ContentInfo', 'bytes left over after the last element', None)),
    'a third element in ContentInfo': (T(0x30, SIGNED_OID + T(0xa0, T(0x30, VERSION + fx.DIGEST_ALGORITHMS + ENCAP + CERTIFICATES + SIGNERS))
                                         + T(0x05, b'')), (MF, 'ContentInfo', 'more elements than declared', None)),
    'contentType is not an OBJECT IDENTIFIER': (T(0x30, T(0x04, PREPARE.SIGNED_DATA_OID) + T(0xa0, T(0x30, SIGNED_FIELDS))),
                                                (MF, 'ContentInfo.contentType', 'another tag', None)),
    'contentType is id-data': (T(0x30, DATA_OID_TLV + T(0xa0, T(0x30, SIGNED_FIELDS))), (MF, 'ContentInfo.contentType', 'another object identifier', None)),
    'content is [1]': (T(0x30, SIGNED_OID + T(0xa1, T(0x30, SIGNED_FIELDS))), (MF, 'ContentInfo.content', 'another tag', None)),
    'content holds two elements': (T(0x30, SIGNED_OID + T(0xa0, T(0x30, SIGNED_FIELDS) + T(0x05, b''))),
                                   (MF, 'ContentInfo.content', 'more elements than declared', None)),
    'SignedData is a SET': (T(0x30, SIGNED_OID + T(0xa0, T(0x31, SIGNED_FIELDS))), (MF, 'SignedData', 'another tag', None)),
    # version
    'version is an OCTET STRING': (fx.envelope(ENVELOPE_CONTENT, version=T(0x04, b'\x01')), (MF, 'SignedData.version', 'another tag', None)),
    'version is an empty INTEGER': (fx.envelope(ENVELOPE_CONTENT, version=T(0x02, b'')),
                                    (MF, 'SignedData.version', 'an INTEGER that is empty or has a redundant leading octet', None)),
    'version has a redundant leading octet': (fx.envelope(ENVELOPE_CONTENT, version=T(0x02, b'\x00\x01')),
                                              (MF, 'SignedData.version', 'an INTEGER that is empty or has a redundant leading octet', None)),
    'version length in more octets than needed': (fx.envelope(ENVELOPE_CONTENT, version=b'\x02\x81\x01\x01'),
                                                  (U, 'SignedData.version', 'a length in more octets than needed', None)),
    'version is a constructed INTEGER': (fx.envelope(ENVELOPE_CONTENT, version=T(0x22, T(0x02, b'\x01'))),
                                         (MF, 'SignedData.version', 'another tag', None)),
    'review: a rival property list inside version': (fx.envelope(ENVELOPE_CONTENT, version=T(0x02, RIVAL_CONTENT)),
                                                     (MF, 'SignedData.version', 'another version', None)),
    'version 6': (fx.envelope(ENVELOPE_CONTENT, version=T(0x02, b'\x06')), (MF, 'SignedData.version', 'another version', None)),
    'version of two octets': (fx.envelope(ENVELOPE_CONTENT, version=T(0x02, b'\x01\x00')), (MF, 'SignedData.version', 'another version', None)),
    'a negative version': (fx.envelope(ENVELOPE_CONTENT, version=T(0x02, b'\xff')), (MF, 'SignedData.version', 'another version', None)),
    # digestAlgorithms
    'SignedData cut short after its version (omits three required fields: digestAlgorithms is named)': (
        signed_data(VERSION), (MF, 'SignedData.digestAlgorithms', 'a missing element', None)),
    'digestAlgorithms is a SEQUENCE': (fx.envelope(ENVELOPE_CONTENT, digests=T(0x30, T(0x30, fx.SHA256))),
                                       (MF, 'SignedData.digestAlgorithms', 'another tag', None)),
    'a digest algorithm that is not a SEQUENCE': (fx.envelope(ENVELOPE_CONTENT, digests=T(0x31, T(0x04, b'x'))),
                                                  (MF, 'SignedData.digestAlgorithms', 'another tag', 1)),
    'a digest algorithm with nothing in it': (fx.envelope(ENVELOPE_CONTENT, digests=T(0x31, T(0x30, b''))),
                                              (MF, 'SignedData.digestAlgorithms', 'a missing element', 1)),
    'a digest algorithm beginning with NULL': (fx.envelope(ENVELOPE_CONTENT, digests=T(0x31, T(0x30, T(0x05, b'')))),
                                               (MF, 'SignedData.digestAlgorithms', 'another tag', 1)),
    'review: a rival property list inside digestAlgorithms': (fx.envelope(ENVELOPE_CONTENT, digests=T(0x31, RIVAL_CONTENT)),
                                                              (MF, 'SignedData.digestAlgorithms', 'an element that runs past its parent', 12)),
    'a malformed OBJECT IDENTIFIER in a digest algorithm': (fx.envelope(ENVELOPE_CONTENT, digests=T(0x31, T(0x30, T(0x06, b'\x80\x01')))),
                                                            (MF, 'SignedData.digestAlgorithms', 'an OBJECT IDENTIFIER that is not well formed', 1)),
    'an element cut off in a digest algorithm': (fx.envelope(ENVELOPE_CONTENT, digests=T(0x31, T(0x30, fx.SHA256 + b'\x05'))),
                                                 (MF, 'SignedData.digestAlgorithms', 'an element cut off at the end of its parent', 1)),
    'an end-of-contents marker in a digest algorithm': (fx.envelope(ENVELOPE_CONTENT, digests=T(0x31, T(0x30, fx.SHA256 + b'\x00\x00'))),
                                                        (MF, 'SignedData.digestAlgorithms', 'an end-of-contents marker outside an indefinite length', 1)),
    'a high tag number in a digest algorithm': (fx.envelope(ENVELOPE_CONTENT, digests=T(0x31, T(0x30, fx.SHA256 + b'\x1f\x81\x00\x00'))),
                                                (U, 'SignedData.digestAlgorithms', 'a tag number in the high-tag-number form', 1)),
    'a NULL with content in a digest algorithm': (fx.envelope(ENVELOPE_CONTENT, digests=T(0x31, T(0x30, fx.SHA256 + T(0x05, b'x')))),
                                                  (MF, 'SignedData.digestAlgorithms', 'a NULL with content', 1)),
    # encapContentInfo
    'encapContentInfo is a SET': (fx.envelope(ENVELOPE_CONTENT, encap=T(0x31, DATA_OID_TLV + T(0xa0, T(0x04, ENVELOPE_CONTENT)))),
                                  (MF, 'SignedData.encapContentInfo', 'another tag', None)),
    'no eContent': (fx.envelope(ENVELOPE_CONTENT, encap=T(0x30, DATA_OID_TLV)), (MF, 'SignedData.encapContentInfo', 'a missing element', None)),
    'eContentType is an OCTET STRING': (fx.envelope(ENVELOPE_CONTENT, encap=T(0x30, T(0x04, PREPARE.DATA_OID) + T(0xa0, T(0x04, ENVELOPE_CONTENT)))),
                                        (MF, 'EncapsulatedContentInfo.eContentType', 'another tag', None)),
    'eContentType is id-signedData': (fx.envelope(ENVELOPE_CONTENT, encap=T(0x30, SIGNED_OID + T(0xa0, T(0x04, ENVELOPE_CONTENT)))),
                                      (MF, 'EncapsulatedContentInfo.eContentType', 'another object identifier', None)),
    'eContent is [1]': (fx.envelope(ENVELOPE_CONTENT, encap=T(0x30, DATA_OID_TLV + T(0xa1, T(0x04, ENVELOPE_CONTENT)))),
                        (MF, 'EncapsulatedContentInfo.eContent', 'another tag', None)),
    'eContent holds a SEQUENCE': (fx.envelope(ENVELOPE_CONTENT, encap=T(0x30, DATA_OID_TLV + T(0xa0, T(0x30, b'')))),
                                  (MF, 'EncapsulatedContentInfo.eContent', 'another tag', None)),
    'eContent holds two OCTET STRINGs': (fx.envelope(ENVELOPE_CONTENT, encap=T(0x30, DATA_OID_TLV + T(0xa0, T(0x04, ENVELOPE_CONTENT) + T(0x04, RIVAL_CONTENT)))),
                                         (MF, 'EncapsulatedContentInfo.eContent', 'more elements than declared', None)),
    'eContent is a constructed OCTET STRING': (fx.envelope(ENVELOPE_CONTENT, encap=T(0x30, DATA_OID_TLV + T(0xa0, T(0x24, T(0x04, ENVELOPE_CONTENT))))),
                                               (U, 'EncapsulatedContentInfo.eContent', 'a constructed string', None)),
    'eContent with an indefinite length': (fx.envelope(ENVELOPE_CONTENT, encap=T(0x30, DATA_OID_TLV + b'\xa0\x80' + T(0x04, ENVELOPE_CONTENT) + b'\x00\x00')),
                                           (U, 'EncapsulatedContentInfo.eContent', 'an indefinite length', None)),
    'an OCTET STRING with an indefinite length': (fx.envelope(ENVELOPE_CONTENT, encap=T(0x30, DATA_OID_TLV + T(0xa0, b'\x04\x80' + ENVELOPE_CONTENT + b'\x00\x00'))),
                                                  (MF, 'EncapsulatedContentInfo.eContent', 'an indefinite length on a primitive element', None)),
    # certificates
    'review: a second SignedData in certificates': (fx.envelope(ENVELOPE_CONTENT, after=T(0xa0, fx.envelope(RIVAL_CONTENT)) + SIGNERS),
                                                    (MF, 'SignedData.certificates', 'a missing element', 1)),
    'review: an indefinite-length child in certificates': (fx.envelope(ENVELOPE_CONTENT, after=T(0xa0, b'\x30\x80\x00\x00') + SIGNERS),
                                                           (U, 'SignedData.certificates', 'an indefinite length', 1)),
    'a certificate that is an OCTET STRING': (with_certificate(T(0x04, RIVAL_CONTENT)), (MF, 'SignedData.certificates', 'another tag', 1)),
    'a certificate of two parts': (with_certificate(T(0x30, T(0x30, b'') + fx.SIGNATURE_ALGORITHM)), (MF, 'SignedData.certificates', 'a missing element', 1)),
    'a certificate of four parts': (with_certificate(T(0x30, T(0x30, b'') + fx.SIGNATURE_ALGORITHM + T(0x03, b'\x00') + T(0x04, RIVAL_CONTENT))),
                                    (MF, 'SignedData.certificates', 'more elements than declared', 1)),
    'a certificate signature that is an OCTET STRING': (with_certificate(certificate(bits=T(0x04, b'x'))), (MF, 'SignedData.certificates', 'another tag', 1)),
    'a certificate signature as a constructed BIT STRING': (with_certificate(certificate(bits=T(0x23, T(0x03, b'\x00x')))),
                                                            (U, 'SignedData.certificates', 'a constructed string', 1)),
    'an empty BIT STRING in a certificate': (with_certificate(certificate(bits=T(0x03, b''))), (MF, 'SignedData.certificates', 'a BIT STRING that is not well formed', 1)),
    'a BOOLEAN other than 00 or FF in a certificate': (with_certificate(certificate(tbs=T(0x30, T(0x01, b'\x01')))),
                                                       (U, 'SignedData.certificates', 'a BOOLEAN other than 00 or FF', 1)),
    'a BOOLEAN of two octets in a certificate': (with_certificate(certificate(tbs=T(0x30, T(0x01, b'\xff\xff')))),
                                                 (MF, 'SignedData.certificates', 'a BOOLEAN that is not one octet', 1)),
    'a primitive SEQUENCE in a certificate': (with_certificate(certificate(tbs=T(0x30, b'\x10\x00'))), (MF, 'SignedData.certificates', 'a primitive SEQUENCE or SET', 1)),
    'a constructed OBJECT IDENTIFIER in a certificate': (with_certificate(certificate(tbs=T(0x30, T(0x26, T(0x06, b'\x2a'))))),
                                                         (MF, 'SignedData.certificates', 'a constructed element of a type that is always primitive', 1)),
    'a reserved length octet in a certificate': (with_certificate(certificate(tbs=T(0x30, b'\x04\xff'))), (MF, 'SignedData.certificates', 'a reserved length octet', 1)),
    # The walk counts from the certificate: deep(n) puts its innermost element n + 1 levels below it.
    'review: an element 65 levels below a certificate': (with_certificate(certificate(tbs=deep(64))),
                                                         (U, 'SignedData.certificates', 'nesting deeper than 64 elements', 1)),
    'the second certificate is not one': (fx.envelope(ENVELOPE_CONTENT, after=T(0xa0, fx.CERTIFICATE + T(0x04, b'x')) + SIGNERS),
                                          (MF, 'SignedData.certificates', 'another tag', 2)),
    'certificates as a primitive [0]': (fx.envelope(ENVELOPE_CONTENT, after=T(0x80, b'x') + SIGNERS), (MF, 'SignedData.certificates', 'another tag', None)),
    # crls
    'a revocation list that is an OCTET STRING': (fx.envelope(ENVELOPE_CONTENT, after=CERTIFICATES + T(0xa1, T(0x04, RIVAL_CONTENT)) + SIGNERS),
                                                  (MF, 'SignedData.crls', 'another tag', 1)),
    # signerInfos
    'no signerInfos': (fx.envelope(ENVELOPE_CONTENT, after=CERTIFICATES), (MF, 'SignedData.signerInfos', 'a missing element', None)),
    'signerInfos is a SEQUENCE': (fx.envelope(ENVELOPE_CONTENT, after=CERTIFICATES + T(0x30, fx.SIGNER_INFO)), (MF, 'SignedData.signerInfos', 'another tag', None)),
    'a signer that is an OCTET STRING': (fx.envelope(ENVELOPE_CONTENT, after=CERTIFICATES + T(0x31, T(0x04, RIVAL_CONTENT))),
                                         (MF, 'SignedData.signerInfos', 'another tag', 1)),
    'a signer with nothing in it': (fx.envelope(ENVELOPE_CONTENT, after=CERTIFICATES + T(0x31, T(0x30, b''))), (MF, 'SignedData.signerInfos', 'a missing element', 1)),
    'a signer beginning with an OCTET STRING': (fx.envelope(ENVELOPE_CONTENT, after=CERTIFICATES + T(0x31, T(0x30, T(0x04, b'x')))),
                                                (MF, 'SignedData.signerInfos', 'another tag', 1)),
    'a signer whose version is a rival property list': (fx.envelope(ENVELOPE_CONTENT, after=CERTIFICATES + T(0x31, T(0x30, T(0x02, RIVAL_CONTENT)))),
                                                        (MF, 'SignedData.signerInfos', 'another version', 1)),
    'a signer of version 6': (fx.envelope(ENVELOPE_CONTENT, after=CERTIFICATES + T(0x31, T(0x30, T(0x02, b'\x06')))),
                              (MF, 'SignedData.signerInfos', 'another version', 1)),
    'a signer version of two octets': (fx.envelope(ENVELOPE_CONTENT, after=CERTIFICATES + T(0x31, T(0x30, T(0x02, b'\x01\x00')))),
                                       (MF, 'SignedData.signerInfos', 'another version', 1)),
    'a negative signer version': (fx.envelope(ENVELOPE_CONTENT, after=CERTIFICATES + T(0x31, T(0x30, T(0x02, b'\xff')))),
                                  (MF, 'SignedData.signerInfos', 'another version', 1)),
    'review: the second signer of version 6': (fx.envelope(ENVELOPE_CONTENT, after=CERTIFICATES + T(0x31, fx.SIGNER_INFO + T(0x30, T(0x02, b'\x06')))),
                                               (MF, 'SignedData.signerInfos', 'another version', 2)),
    'review: a rival property list inside signerInfos': (fx.envelope(ENVELOPE_CONTENT, after=CERTIFICATES + T(0x31, RIVAL_CONTENT)),
                                                         (MF, 'SignedData.signerInfos', 'an element that runs past its parent', 12)),
    'signerInfos twice': (fx.envelope(ENVELOPE_CONTENT, after=CERTIFICATES + SIGNERS + SIGNERS),
                          (MF, 'SignedData (after encapContentInfo)', 'more elements than declared', None)),
    'certificates after signerInfos': (fx.envelope(ENVELOPE_CONTENT, after=SIGNERS + CERTIFICATES),
                                       (MF, 'SignedData (after encapContentInfo)', 'more elements than declared', None)),
    # the outer length
    'the outer length in more octets than needed': (b'\x30\x84' + len(CONTROL_ENVELOPE[4:]).to_bytes(4, 'big') + CONTROL_ENVELOPE[4:],
                                                    (U, 'ContentInfo', 'a length in more octets than needed', None)),
    'the outer element with an indefinite length': (b'\x30\x80' + CONTROL_ENVELOPE[4:] + b'\x00\x00', (U, 'ContentInfo', 'an indefinite length', None)),
    'a file cut off inside its length': (b'\x30\x85\x01', (MF, 'ContentInfo', 'an element cut off at the end of its parent', None)),
    'review: an outer length past the end of the file': (b'\x30\xfe' + b'\xff' * 126, (MF, 'ContentInfo', 'an element that runs past its parent', None)),
    # the property list: the whole of the one content string, read by the whole-document reader
    'review: an empty eContent': (fx.envelope(b''), (MF, 'document', 'an empty document', None)),
    'review: a second envelope as the content': (fx.envelope(CONTROL_ENVELOPE),
                                                 (U, 'document header', 'content that does not begin with an XML declaration', None)),
    # the file: one element of 1 byte to 256 KiB
    'review: an empty profile file': (b'', (MF, 'the file', 'an empty file', None)),
    'a profile larger than 256 KiB': (fx.envelope(ENVELOPE_CONTENT, digests=T(0x31, T(0x30, fx.SHA256 + T(0x04, b'x' * (256 * 1024))))),
                                      (U, 'the file', 'a file larger than the size limit', None)),
}
# The cases whose refusal names another part than the envelope: the content string's property list, and the file.
CASE_PART = {'review: an empty eContent': 'profile property list', 'review: a second envelope as the content': 'profile property list',
             'review: an empty profile file': 'profile file', 'a profile larger than 256 KiB': 'profile file'}


def case_part(name):
    return CASE_PART.get(name, 'profile envelope')


def case_expected(name, kind, field, found):
    if case_part(name) == 'profile property list':
        return WHOLE.PLIST_REASONS[found][1]
    if case_part(name) == 'profile file':
        return PREPARE.PROFILE_SIZE
    return (PREPARE.DEFINITE_DER if kind == 'unsupported' else PREPARE.WITHIN_PARENT if found in PREPARE.ENVELOPE_MALFORMED
            else PREPARE.TYPE_RULE if found in PREPARE.ENVELOPE_TYPE_RULES else PREPARE.ENVELOPE_SHAPES[field])
ENVELOPE_CONTROLS = {
    'the control': CONTROL_ENVELOPE,
    'no certificates': fx.envelope(ENVELOPE_CONTENT, after=SIGNERS),
    'two certificates and a revocation list': fx.envelope(ENVELOPE_CONTENT, after=T(0xa0, fx.CERTIFICATE * 2) + T(0xa1, certificate()) + SIGNERS),
    'an empty digestAlgorithms and signerInfos': fx.envelope(ENVELOPE_CONTENT, digests=T(0x31, b''), after=T(0x31, b'')),
    'a certificate holding a property list in an OCTET STRING': with_certificate(certificate(tbs=T(0x30, T(0x04, RIVAL_CONTENT)))),
    'a long-form length where needed': fx.envelope(ENVELOPE_CONTENT, version=T(0x02, b'\x01'), digests=T(0x31, T(0x30, fx.SHA256 + T(0x04, b'x' * 200)))),
    'review: an element exactly 64 levels below a certificate (the walk boundary)': with_certificate(certificate(tbs=deep(63))),
    'a profile of exactly 256 KiB (the size cap)': fx.envelope(ENVELOPE_CONTENT, digests=T(0x31, T(0x30, fx.SHA256 + T(0x04, b'x' * (
        256 * 1024 - len(fx.envelope(ENVELOPE_CONTENT, digests=T(0x31, T(0x30, fx.SHA256 + T(0x04, b'x' * 200000))))) + 200000))))),
    'versions 0, 3 and 5 (the CMSVersion bounds)': fx.envelope(ENVELOPE_CONTENT, version=T(0x02, b'\x05'), after=CERTIFICATES + T(
        0x31, fx.SIGNER_INFO.replace(T(0x02, b'\x01'), T(0x02, b'\x00'), 1) + fx.SIGNER_INFO.replace(T(0x02, b'\x01'), T(0x02, b'\x03'), 1))),
}
CONSISTENT = {'developer_id_team_identifier': fx.TEAM, 'production_bundle_identifier': 'com.chirality.app'}


class EnvelopeShapes(unittest.TestCase):
    """Review round 1, finding 1: the envelope reader skipped the contents of the fields around the content. Each field
    and each rule is now read, and a fixture that breaks one rule alone is refused with exactly that field and rule."""

    def detail(self, raw):
        with self.assertRaises(common.Refused) as raised:
            PREPARE.profile_consistency(raw, fx.sha(raw), CONSISTENT, now=NOW)
        return raised.exception.detail()

    def test_each_field_and_rule(self):
        for name, (raw, (kind, field, found, item)) in ENVELOPE_CASES.items():
            with self.subTest(name):
                detail = self.detail(raw)
                self.assertEqual((detail['part'], detail['kind'], detail['field'], detail['found'], detail.get('item')),
                                 (case_part(name), kind, field, found, item))
                self.assertEqual(detail['expected'], case_expected(name, kind, field, found))
                self.assertLessEqual(detail.get('offset', 0), len(raw))
                common.validate_returnable(detail, set())  # fixed text and integers only

    def test_each_control_reads(self):
        for name, raw in ENVELOPE_CONTROLS.items():
            with self.subTest(name):
                self.assertEqual(PREPARE.profile_consistency(raw, fx.sha(raw), CONSISTENT, now=NOW)['application_identifier'],
                                 fx.TEAM + '.com.chirality.app')
                content, offset = PREPARE.profile_envelope(raw)
                self.assertEqual((content, raw[offset:offset + len(content)]), (ENVELOPE_CONTENT, ENVELOPE_CONTENT))

    def test_each_item_of_the_enforced_list_has_its_cases(self):
        """The claim is exactly the enforced list in prepare.py; each item names the cases above that test it."""
        enforced = {
            '1. one definite-length element of 1 byte to 256 KiB, no byte after it': (
                'a byte after ContentInfo', 'the outer element with an indefinite length', 'the outer length in more octets than needed',
                'a file cut off inside its length', 'review: an empty profile file', 'a profile larger than 256 KiB'),
            '2. the declared structure from the outside down to the content, in order': (
                'ContentInfo is not a SEQUENCE', 'contentType is id-data', 'content is [1]', 'SignedData is a SET', 'version 6',
                'digestAlgorithms is a SEQUENCE', 'encapContentInfo is a SET', 'eContentType is id-signedData',
                'eContent holds two OCTET STRINGs', 'eContent is a constructed OCTET STRING', 'certificates as a primitive [0]',
                'no signerInfos', 'signerInfos twice', 'certificates after signerInfos'),
            '3. every length inside its parent at every level walked': (
                'review: an outer length past the end of the file', 'an element cut off in a digest algorithm',
                'review: a rival property list inside digestAlgorithms', 'review: a rival property list inside signerInfos',
                'a reserved length octet in a certificate'),
            '4. the property list is the whole of the one content string': (
                'review: an empty eContent', 'review: a second envelope as the content'),
        }
        for item, names in enforced.items():
            with self.subTest(item):
                self.assertEqual([n for n in names if n not in ENVELOPE_CASES], [])
        # and item 4 inside the content string: the conflicting pair (test_the_property_list_refusal_names_its_byte_in_the_file)

    def test_a_version_out_of_range_beside_a_later_indefinite_length(self):
        """Review round 2 asked for the version to be reported here, and the code reads the top-level fields in order, so
        it is. No order is promised (review round 3): each reason is true of the file, and the control has the later
        defect alone."""
        raw = fx.envelope(ENVELOPE_CONTENT, version=T(0x02, b'\x06'), after=CERTIFICATES + b'\x31\x80\x00\x00')
        detail = self.detail(raw)
        self.assertEqual((detail['kind'], detail['field'], detail['found']), ('malformed', 'SignedData.version', 'another version'))
        raw = fx.envelope(ENVELOPE_CONTENT, after=CERTIFICATES + b'\x31\x80\x00\x00')  # the later field alone
        detail = self.detail(raw)
        self.assertEqual((detail['kind'], detail['field'], detail['found']),
                         ('unsupported', 'SignedData (after encapContentInfo)', 'an indefinite length'))

    def test_stated_limit_the_inside_of_other_fields_is_length_walked_not_validated(self):
        """Review round 2, finding 1, decided as outside the claim: some universal-type rules inside a digest algorithm's
        parameters, a certificate, a revocation list or a signer information are not refused (these three here). They
        are length-walked only; nothing authenticates the envelope, so validating them adds no assurance about the content.
        This test keeps the behaviour deliberate and visible (README: the envelope's enforced list)."""
        inside = {'reserved universal tag 15': b'\x0f\x00', 'primitive EXTERNAL': b'\x08\x00', 'primitive EMBEDDED PDV': b'\x0b\x00'}
        for name, element in inside.items():
            for where, raw in (('digest algorithm parameters', fx.envelope(ENVELOPE_CONTENT, digests=T(0x31, T(0x30, fx.SHA256 + element)))),
                               ('a certificate', with_certificate(certificate(tbs=T(0x30, element)))),
                               ('a signer information', fx.envelope(ENVELOPE_CONTENT, after=CERTIFICATES + T(0x31, T(0x30, VERSION + element))))):
                with self.subTest(name=name, where=where):
                    self.assertEqual(PREPARE.profile_consistency(raw, fx.sha(raw), CONSISTENT, now=NOW)['application_identifier'],
                                     fx.TEAM + '.com.chirality.app')

    def test_the_property_list_refusal_names_its_byte_in_the_file(self):
        raw = fx.envelope(fx.two_values(RIVAL_CONTENT, ENVELOPE_CONTENT))
        detail = self.detail(raw)
        content, offset = PREPARE.profile_envelope(raw)
        self.assertEqual((detail['part'], detail['kind'], detail['field'], detail['found']),
                         ('profile property list', 'malformed', 'plist', 'a second value under plist'))
        self.assertEqual(raw[detail['offset']:detail['offset'] + 6], b'<dict>')
        self.assertGreater(detail['offset'], offset)


# A property list in a form outside the subset the reader reads (a comment directly inside plist), for the
# not-established kind.
def with_comment(raw):
    return raw.replace(b'<dict>', b'<!-- invented comment --><dict>', 1)


UNREAD_INFO_PLIST = with_comment(fx.info_plist())
UNREAD_PROFILE = fx.profile_bytes(content=with_comment)
OTHER_TEAM_PROFILE = fx.profile_bytes(team='OTHER00001', prefix='OTHER00001')
S2_CODES = {'unsupported': 'S2_PROFILE_NOT_ESTABLISHED', 'malformed': 'S2_PROFILE_MALFORMED', 'mismatch': 'S2_PROFILE'}


class WholeFileDocuments(Base):
    """The file readers (the provisioning profile's property list and the App's Info.plist) return a value only when it
    is the whole document (production_inputs/whole_plist.py). The conflicting pair is another team's values with
    get-task-allow, then the expected ones, as two sibling values; plistlib alone reads the expected ones.

    Where the owner reads a refusal (the STOP line, STOPPED.json, the build's named check, record.py check), it names
    the part, the kind, the field, the shape expected, what was found and the byte, in fixed text and integers. A form
    the reader does not read is 'not established': never a mismatch, never a difference, never agreement."""

    def stopped(self, code):
        """The STOP line, its refusal lines and STOPPED.json, for a run that stopped with `code`; returns STOPPED.json."""
        self.assertFalse((self.out / 'PACKAGE_IDENTITY.json').exists())
        self.assertFalse((self.out / 'RESULT.json').exists())
        stopped = json.loads((self.out / 'STOPPED.json').read_text())
        self.assertEqual(stopped['reason_code'], code)
        return stopped

    def run_stopping(self, code):
        """A signing run that stops with `code`: (stderr lines after the reason, STOPPED.json or None)."""
        status, stdout, stderr = self.main()
        self.assertEqual((status, stdout), (3, ''), stderr)
        lines = stderr.splitlines()
        self.assertEqual(lines[0], 'STOP: ' + common.REASONS[code])
        stopped = self.stopped(code) if (self.out / 'STOPPED.json').exists() else None
        return lines[1:], stopped

    def assert_truthful_run_completes(self, name):
        self.out = self.root / name
        self.fake = fx.FakeApple()
        code, _, stderr = self.main()
        self.assertEqual(code, 0, stderr)
        self.assertTrue((self.out / 'PACKAGE_IDENTITY.json').is_file())
        self.assertTrue((self.out / 'RESULT.json').is_file())

    def test_the_readers_refuse_the_conflicting_pair_and_read_the_control(self):
        selected = {'developer_id_team_identifier': fx.TEAM, 'production_bundle_identifier': 'com.chirality.app'}
        conflicting = fx.conflicting_profile_bytes()
        self.assertEqual(plistlib.loads(common.prepare.profile_content(conflicting))['TeamIdentifier'], [fx.TEAM])  # plistlib alone
        with self.assertRaisesRegex(ValueError, 'a second value under plist'):
            common.prepare.profile_consistency(conflicting, fx.sha(conflicting), selected, now=NOW)
        control = fx.profile_bytes()
        self.assertEqual(common.prepare.profile_consistency(control, fx.sha(control), selected, now=NOW)['application_identifier'],
                         fx.TEAM + '.com.chirality.app')
        app = self.root / 'reader' / common.APP_NAME
        (app / 'Contents').mkdir(parents=True)
        (app / 'Contents/embedded.provisionprofile').write_bytes(conflicting)
        (app / 'Contents/Info.plist').write_bytes(fx.conflicting_info_plist())
        self.assertEqual(plistlib.loads(fx.conflicting_info_plist())['CFBundleIdentifier'], 'com.chirality.app')  # plistlib alone
        failures = []
        self.assertEqual(record.profile_facts(app, {fx.TEAM}, failures)['decoded'], False)
        self.assertEqual([f['observation'] for f in failures], ['provisioning profile'])
        self.assertEqual(failures[0]['detail']['found'], 'a second value under plist')
        with self.assertRaisesRegex(ValueError, 'a second value under plist'):
            common.read_info_plist(app)
        (app / 'Contents/embedded.provisionprofile').write_bytes(control)
        (app / 'Contents/Info.plist').write_bytes(fx.info_plist())
        failures = []
        facts = record.profile_facts(app, {fx.TEAM}, failures)
        self.assertEqual((failures, facts['decoded'], facts['team'], facts['app_id']), ([], True, [fx.TEAM], fx.TEAM + '.com.chirality.app'))
        self.assertEqual(common.read_info_plist(app)[1]['CFBundleIdentifier'], 'com.chirality.app')

    def test_each_envelope_rule_stops_step_2_with_exactly_its_field_and_shape(self):
        """Every envelope case, through the full injected signing run: the STOP code by kind, one refusal line, and
        STOPPED.json holding exactly that refusal; nothing signed. A truthful run beside them completes."""
        for n, (name, (raw, (kind, field, found, item))) in enumerate(ENVELOPE_CASES.items()):
            with self.subTest(name):
                self.out, self.fake = self.root / f'signed-envelope-{n}', fx.FakeApple()
                self.profile.write_bytes(raw)
                lines, stopped = self.run_stopping(S2_CODES[kind])
                if case_part(name) == 'profile file':
                    # refused by its size before any byte is read: nothing ran and no output folder exists
                    self.assertIsNone(stopped)
                    self.assertEqual(self.fake.calls, [])
                    detail = common.Refused('x', part='profile file', kind=kind, field=field, expected=PREPARE.PROFILE_SIZE,
                                            found=found).detail()
                else:
                    [detail] = stopped['refusals']
                self.assertEqual((detail['part'], detail['kind'], detail['field'], detail['found'], detail.get('item')),
                                 (case_part(name), kind, field, found, item))
                self.assertEqual(lines, ['  ' + common.describe(detail)])
                self.assertFalse([a for a in self.fake.calls if '--sign' in a])
        self.profile.write_bytes(fx.profile_bytes())
        self.assert_truthful_run_completes('signed-control')

    def test_step_2_names_the_kind_unread_malformed_or_mismatch(self):
        cases = {'a comment in the property list (not read)': (UNREAD_PROFILE, 'unsupported', 'profile property list', 'plist', 'a comment'),
                 'the conflicting pair (malformed)': (fx.conflicting_profile_bytes(), 'malformed', 'profile property list', 'plist',
                                                      'a second value under plist'),
                 'another team (read whole, a mismatch)': (OTHER_TEAM_PROFILE, 'mismatch', 'profile grants',
                                                           'TeamIdentifier and Entitlements com.apple.developer.team-identifier', 'another value')}
        for n, (name, (raw, kind, part, field, found)) in enumerate(cases.items()):
            with self.subTest(name):
                self.out, self.fake = self.root / f'signed-kind-{n}', fx.FakeApple()
                self.profile.write_bytes(raw)
                lines, stopped = self.run_stopping(S2_CODES[kind])
                [detail] = stopped['refusals']
                self.assertEqual((detail['part'], detail['kind'], detail['field'], detail['found']), (part, kind, field, found))
                self.assertEqual(lines, ['  ' + common.describe(detail)])
                if kind == 'unsupported':
                    self.assertIn('the identity comparison is not established', common.REASONS[stopped['reason_code']])
                    self.assertIn('the identity comparison is not established', lines[0])
                    self.assertNotIn('not a current Developer ID profile', lines[0] + common.REASONS[stopped['reason_code']])
        self.profile.write_bytes(fx.profile_bytes())
        self.assert_truthful_run_completes('signed-control')

    def test_a_candidate_whose_info_plist_is_not_whole_or_not_read_is_refused_before_anything_runs(self):
        for n, (maker, code, kind, field, found) in enumerate((
                (fx.conflicting_info_plist, 'REFUSED_INFO_PLIST_MALFORMED', 'malformed', 'plist', 'a second value under plist'),
                (lambda: UNREAD_INFO_PLIST, 'REFUSED_INFO_PLIST_NOT_ESTABLISHED', 'unsupported', 'plist', 'a comment'))):
            with self.subTest(code):
                folder = self.root / f'candidate-{n}'
                folder.mkdir()
                with patch.object(fx, 'info_plist', maker):
                    self.candidate = fx.candidate(folder) / ''
                self.out, self.fake = self.root / f'signed-candidate-{n}', fx.FakeApple()
                lines, stopped = self.run_stopping(code)
                self.assertIsNone(stopped)  # a refusal before anything runs leaves no output folder
                self.assertEqual(self.fake.calls, [])
                detail = common.Refused('x', part='Info.plist', kind=kind, field=field, found=found, offset=None,
                                        expected=common.prepare.whole_plist.PLIST_REASONS[found][1]).detail()
                self.assertEqual(len(lines), 1)
                self.assertTrue(lines[0].startswith('  ' + common.describe(detail)[:-1] + ' at byte '), lines[0])
        self.candidate = self.root / 'candidate'
        self.assert_truthful_run_completes('signed-control')

    def test_a_package_not_whole_at_the_record_reading_stops_with_no_record(self):
        """Step 13 reads the Info.plist and the profile again from the mounted disk image."""
        def at_record(relative, raw):
            def attach(argv):
                if sum(c[1] == 'attach' for c in self.fake.calls) != 2:
                    return None
                answer = self.fake.answer(argv)
                (Path(argv[argv.index('-mountpoint') + 1]) / common.APP_NAME / relative).write_bytes(raw)
                return answer
            return attach
        for relative, raw, observation in (('Contents/Info.plist', fx.conflicting_info_plist(), 'bundle identity'),
                                           ('Contents/Info.plist', UNREAD_INFO_PLIST, 'bundle identity not established'),
                                           ('Contents/embedded.provisionprofile', fx.conflicting_profile_bytes(), 'provisioning profile'),
                                           ('Contents/embedded.provisionprofile', UNREAD_PROFILE, 'provisioning profile not established')):
            with self.subTest(observation):
                self.out = self.root / ('signed-' + observation.replace(' ', '-'))
                self.fake = fx.FakeApple()
                self.fake.override[('attach',)] = at_record(relative, raw)
                lines, stopped = self.run_stopping('S13_OBSERVATION')
                # the changed file also makes the App differ from the App as signed; the reader's own failure is named
                named = [f for f in stopped['failed_observations'] if f['observation'] == observation]
                self.assertEqual(len(named), 1)
                self.assertEqual(lines, ['  ' + common.describe(named[0]['detail'])])
        self.assert_truthful_run_completes('signed-control')


def profile_with(**fields):
    """An invented profile whose property list has `fields` replaced (a value of None removes the key)."""
    value = fx.profile_value()
    for key, item in fields.items():
        holder, name = (value['Entitlements'], key.split(' ', 1)[1]) if key.startswith('Entitlements ') else (value, key)
        if item is None:
            holder.pop(name, None)
        else:
            holder[name] = item
    return fx.envelope(plistlib.dumps(value))


def info_with(**fields):
    """An invented Info.plist with `fields` replaced (a value of None removes the key)."""
    value = plistlib.loads(fx.info_plist())
    for key, item in fields.items():
        if item is None:
            value.pop(key)
        else:
            value[key] = item
    return plistlib.dumps(value)


# Review round 2, finding 5: one typed check of exactly the fields the tools read, after the whole read, for every consumer.
WRONG_PROFILE_TYPES = {
    'review: TeamIdentifier 42': ('TeamIdentifier', 42), 'review: TeamIdentifier a nested array': ('TeamIdentifier', [[fx.TEAM]]),
    'review: TeamIdentifier a dictionary keyed by the team': ('TeamIdentifier', {fx.TEAM: 'invented'}),
    'UUID an integer': ('UUID', 42), 'ApplicationIdentifierPrefix a string': ('ApplicationIdentifierPrefix', fx.TEAM),
    'Platform a string': ('Platform', 'OSX'), 'ProvisionedDevices an array of integers': ('ProvisionedDevices', [1]),
    'ProvisionsAllDevices the integer 1': ('ProvisionsAllDevices', 1), 'CreationDate a string': ('CreationDate', '2026-01-01T00:00:00Z'),
    'ExpirationDate a string': ('ExpirationDate', '2099-01-01T00:00:00Z'), 'Entitlements an array': ('Entitlements', []),
    'the App ID entitlement an array': ('Entitlements com.apple.application-identifier', [fx.TEAM + '.com.chirality.app']),
    'the team entitlement an array': ('Entitlements com.apple.developer.team-identifier', [fx.TEAM]),
    'get-task-allow a string': ('Entitlements get-task-allow', 'false'),
    'the hardened get-task-allow the integer 0': ('Entitlements com.apple.security.get-task-allow', 0),
}
WRONG_INFO_TYPES = {f'{key} {why}': (key, item, found) for key in ('CFBundleIdentifier', 'CFBundleShortVersionString', 'CFBundleVersion',
                                                                   'LSMinimumSystemVersion', 'CFBundleExecutable')
                    for why, item, found in (('an integer', 4, 'a value of another type'), ('missing', None, 'a missing key'))}


def hostile_documents():
    """Hostile property-list documents, all invented: name -> bytes. Deterministic."""
    import random
    rng = random.Random(387)
    base = READER_CONTROL
    found = {
        'empty': b'', 'whitespace': b'\n\t ', 'NUL bytes': b'\x00' * 32, 'random bytes': bytes(rng.randrange(256) for _ in range(200)),
        'a lone declaration': PLIST_HEADER, 'binary': plistlib.dumps(READER_EXPECTED, fmt=plistlib.FMT_BINARY),
        'binary cut short': plistlib.dumps(READER_EXPECTED, fmt=plistlib.FMT_BINARY)[:20], 'bplist then XML': b'bplist00' + base,
        'UTF-16 bytes': base.decode().encode('utf-16'), 'UTF-32 bytes': base.decode().encode('utf-32'),
        'UTF-16 declared, UTF-16 bytes': base.replace(b'UTF-8', b'UTF-16').decode().encode('utf-16'),
        'XML 1.1': base.replace(b'version="1.0" encoding', b'version="1.1" encoding'),
        'invalid UTF-8': base.replace(b'ZZINVENT01</string>', b'\xff\xfe\xc0</string>'),
        'a NUL character reference': base.replace(b'ZZINVENT01</string>', b'&#0;</string>'),
        'a surrogate character reference': base.replace(b'ZZINVENT01</string>', b'&#xD800;</string>'),
        'a parameter entity': plist_document(READER_DICT, header=b'<?xml version="1.0"?>\n<!DOCTYPE plist [<!ENTITY % p "x"> %p;]>\n'),
        'nested entities': plist_document(READER_DICT.replace(b'ZZINVENT01</string>', b'&b;</string>'),
                                          header=b'<?xml version="1.0"?>\n<!DOCTYPE plist [<!ENTITY a "aaaa"><!ENTITY b "&a;&a;&a;">]>\n'),
        'an external DTD': plist_document(READER_DICT, header=b'<?xml version="1.0"?>\n<!DOCTYPE plist SYSTEM "file:///invented/x.dtd">\n'),
        'deep arrays': plist_document(b'<array>' * 5000 + b'</array>' * 5000),
        'deep dictionaries': plist_document(b'<dict><key>k</key>' * 3000 + b'<true/>' + b'</dict>' * 3000),
        'a huge integer': plist_document(b'<integer>' + b'9' * 100000 + b'</integer>'),
        'an unclosed root': base[:-12],
        'a namespace prefix': base.replace(b'<dict>', b'<x:dict xmlns:x="urn:invented">', 1),
    }
    for encoding in (b'Shift_JIS', b'EUC-JP', b'ISO-2022-JP', b'UTF-16', b'UTF-16LE', b'UTF-32', b'x-invented', b'', b'utf8',
                     b'US-ASCII', b'windows-1252', b'UTF-8"'):
        found[f'declared encoding {encoding!r}'] = base.replace(b'UTF-8', encoding, 1)
    for n in range(0, len(base), 4):
        found[f'cut at {n}'] = base[:n]
    for n in range(0, len(base), 6):
        found[f'byte {n} flipped'] = base[:n] + bytes([base[n] ^ 0xff]) + base[n + 1:]
    for n in range(40):
        raw = bytearray(base)
        for _ in range(rng.randrange(1, 6)):
            raw[rng.randrange(len(raw))] = rng.randrange(256)
        found[f'random mutation {n}'] = bytes(raw)
    return found


def hostile_profiles():
    """Hostile provisioning profiles, all invented: name -> bytes. Deterministic."""
    found = {'content ' + name: fx.envelope(raw) for name, raw in hostile_documents().items()
             if not name.startswith(('cut at', 'byte', 'random mutation'))}
    base = CONTROL_ENVELOPE
    for n in range(0, len(base), 5):
        found[f'cut at {n}'] = base[:n]
        found[f'byte {n} flipped'] = base[:n] + bytes([base[n] ^ 0xff]) + base[n + 1:]
    found.update({name: profile_with(**{field: item}) for name, (field, item) in WRONG_PROFILE_TYPES.items()})
    return found


class TypedAndHostile(Base):
    """Review round 2, findings 3 and 5. The only outcomes of reading a file are a value or a refusal named from the closed
    lists; a field the tools read is of its type or a named mismatch. No other exception class, no generic stop code
    (S2_UNEXPECTED, REFUSED_CANDIDATE, a code without a refusal), and no exit 2 from record.py check."""

    def typed(self, call):
        """call(), or its refusal's detail checked against the closed lists; any other exception fails the test."""
        try:
            return call()
        except common.Refused as refused:
            detail = refused.detail()
            common.validate_returnable(detail, set())
            self.assertIn(detail['kind'], WHOLE.KINDS)
            return detail

    def test_hostile_documents_give_a_value_or_a_typed_refusal(self):
        app = self.root / 'hostile' / common.APP_NAME
        (app / 'Contents').mkdir(parents=True)
        for name, raw in hostile_documents().items():
            with self.subTest(name):
                self.typed(lambda: WHOLE.load(raw))
                (app / 'Contents/Info.plist').write_bytes(raw)
                self.typed(lambda: common.read_info_plist(app))
        for name, raw in hostile_profiles().items():
            with self.subTest(name):
                self.typed(lambda: PREPARE.profile_consistency(raw, fx.sha(raw), CONSISTENT, now=NOW))
                (app / 'Contents/embedded.provisionprofile').write_bytes(raw)
                failures = []
                record.profile_facts(app, {fx.TEAM}, failures)
                for failed in failures:
                    common.validate_returnable(failed, {fx.TEAM})
                    self.assertIn('detail', failed, name)

    def test_each_profile_field_the_tools_read_is_of_its_type_or_a_named_mismatch(self):
        for name, (field, item) in WRONG_PROFILE_TYPES.items():
            with self.subTest(name):
                raw = profile_with(**{field: item})
                detail = self.typed(lambda: PREPARE.profile_consistency(raw, fx.sha(raw), CONSISTENT, now=NOW))
                expected = (PREPARE.ENTITLEMENT_TYPES[field.split(' ', 1)[1]] if field.startswith('Entitlements ')
                            else PREPARE.PROFILE_TYPES[field])[0]
                self.assertEqual((detail['part'], detail['kind'], detail['field'], detail['expected'], detail['found']),
                                 ('profile property list', 'mismatch', field, expected, PREPARE.OTHER_TYPE))
        raw = profile_with(TeamIdentifier=[fx.TEAM])  # the control
        self.assertEqual(PREPARE.profile_consistency(raw, fx.sha(raw), CONSISTENT, now=NOW)['application_identifier'], fx.TEAM + '.com.chirality.app')

    def test_each_info_plist_identity_field_is_present_and_a_string_or_a_named_mismatch(self):
        app = self.root / 'typed' / common.APP_NAME
        (app / 'Contents').mkdir(parents=True)
        for name, (key, item, found) in WRONG_INFO_TYPES.items():
            with self.subTest(name):
                (app / 'Contents/Info.plist').write_bytes(info_with(**{key: item}))
                detail = self.typed(lambda: common.read_info_plist(app))
                self.assertEqual((detail['part'], detail['kind'], detail['field'], detail['expected'], detail['found']),
                                 ('Info.plist', 'mismatch', key, 'a string', found))
        (app / 'Contents/Info.plist').write_bytes(fx.info_plist())
        self.assertEqual(common.read_info_plist(app)[1]['CFBundleVersion'], '4.0.0')

    def test_hostile_and_mistyped_profiles_stop_step_2_with_a_named_reason(self):
        cases = {name: hostile_profiles()[name] for name in (
            'content declared encoding b\'Shift_JIS\'', 'content declared encoding b\'x-invented\'', 'content UTF-16 bytes',
            'content invalid UTF-8', 'content random bytes', 'content empty', 'cut at 40', 'byte 0 flipped')}
        cases.update({'review: an empty profile file': b'', 'review: an envelope as the content': fx.envelope(CONTROL_ENVELOPE)})
        cases.update({name: profile_with(**{field: item}) for name, (field, item) in WRONG_PROFILE_TYPES.items() if name.startswith('review')})
        for n, (name, raw) in enumerate(cases.items()):
            with self.subTest(name):
                self.out, self.fake = self.root / f'hostile-profile-{n}', fx.FakeApple()
                self.profile.write_bytes(raw)
                status, stdout, stderr = self.main()
                lines = stderr.splitlines()
                code = next(c for c, text in common.REASONS.items() if lines[0] == 'STOP: ' + text)
                self.assertIn(code, set(S2_CODES.values()))
                if (self.out / 'STOPPED.json').exists():
                    [detail] = json.loads((self.out / 'STOPPED.json').read_text())['refusals']
                    self.assertEqual(S2_CODES[detail['kind']], code)
                    self.assertEqual((status, lines[1:]), (3, ['  ' + common.describe(detail)]))
                else:  # refused by its size before any byte was read
                    self.assertEqual((status, len(lines), self.fake.calls), (3, 2, []))
                self.assertFalse([a for a in self.fake.calls if '--sign' in a])
        self.profile.write_bytes(fx.profile_bytes())
        self.out, self.fake = self.root / 'hostile-control', fx.FakeApple()
        self.assertEqual(self.main()[0], 0)

    def test_hostile_and_mistyped_candidate_info_plists_are_refused_by_name_before_anything_runs(self):
        codes = {'unsupported': 'REFUSED_INFO_PLIST_NOT_ESTABLISHED', 'malformed': 'REFUSED_INFO_PLIST_MALFORMED',
                 'mismatch': 'REFUSED_INFO_PLIST_MISMATCH'}
        cases = {'review: Shift_JIS declared': (fx.info_plist().replace(b'UTF-8', b'Shift_JIS'), 'unsupported'),
                 'review: an unknown encoding declared': (fx.info_plist().replace(b'UTF-8', b'x-invented-encoding'), 'unsupported'),
                 'an empty Info.plist': (b'', 'malformed'),
                 'review: a whole Info.plist of version 9.9.9': (fx.info_plist(CFBundleShortVersionString='9.9.9'), 'mismatch'),
                 'review: an integer bundle version': (fx.info_plist(CFBundleVersion=4), 'mismatch'),
                 'no executable key': (info_with(CFBundleExecutable=None), 'mismatch')}
        for n, (name, (raw, kind)) in enumerate(cases.items()):
            with self.subTest(name):
                folder = self.root / f'hostile-candidate-{n}'
                folder.mkdir()
                with patch.object(fx, 'info_plist', lambda **_: raw):
                    self.candidate = fx.candidate(folder) / ''
                self.out, self.fake = self.root / f'hostile-candidate-out-{n}', fx.FakeApple()
                status, stdout, stderr = self.main()
                lines = stderr.splitlines()
                self.assertEqual((status, lines[0]), (3, 'STOP: ' + common.REASONS[codes[kind]]))
                self.assertEqual(len(lines), 2)
                self.assertIn(': ' + WHOLE.KINDS[kind] + '. Field ', lines[1])
                self.assertEqual(self.fake.calls, [])
        self.candidate = self.root / 'candidate'
        self.out, self.fake = self.root / 'hostile-candidate-control', fx.FakeApple()
        self.assertEqual(self.main()[0], 0)


class ThirdReview(Base):
    """Review round 3: each finding reproduced, beside a control."""

    def sparse(self, path, size):
        """A file of `size` bytes made by extending an empty one: nothing large is committed or written."""
        path.write_bytes(b'')
        with path.open('r+b') as handle:
            handle.truncate(size)

    def test_finding_1_a_profile_over_the_cap_is_refused_by_name_before_any_read_on_every_path(self):
        cap = CONTROLS_AT_CAP = ENVELOPE_CONTROLS['a profile of exactly 256 KiB (the size cap)']
        self.assertEqual(len(CONTROLS_AT_CAP), PREPARE.PROFILE_LIMIT)
        self.assertEqual(PREPARE.profile_consistency(cap, fx.sha(cap), CONSISTENT, now=NOW)['size'], PREPARE.PROFILE_LIMIT)
        app = self.root / 'sized' / common.APP_NAME
        (app / 'Contents').mkdir(parents=True)
        # above the cap, and above the 32 MiB bound of the generic file transfer that once refused first, untyped
        for n, size in enumerate((PREPARE.PROFILE_LIMIT + 1, 32 * 1024 * 1024 + 1)):
            with self.subTest(size=size):
                self.sparse(app / 'Contents/embedded.provisionprofile', size)
                failures = []
                with patch.object(record.Path, 'read_bytes', side_effect=AssertionError('read before its size was refused')):
                    self.assertEqual(record.profile_facts(app, {fx.TEAM}, failures), {'decoded': False})
                [failed] = failures
                self.assertEqual((failed['observation'], failed['detail']['found']),
                                 ('provisioning profile not established', 'a file larger than the size limit'))
                self.sparse(self.profile, size)
                self.out, self.fake = self.root / f'sized-{n}', fx.FakeApple()
                status, stdout, stderr = self.main()
                lines = stderr.splitlines()
                self.assertEqual((status, lines[0], self.fake.calls), (3, 'STOP: ' + common.REASONS['S2_PROFILE_NOT_ESTABLISHED'], []))
                self.assertEqual(lines[1:], ['  ' + common.describe(failed['detail'])])
        self.profile.write_bytes(cap)
        self.out, self.fake = self.root / 'sized-cap', fx.FakeApple()
        self.assertEqual(self.main()[0], 0)

    def test_finding_2_xml_1_1_is_not_established_at_every_consumer(self):
        xml11 = ENVELOPE_CONTENT.replace(b'<?xml version="1.0"', b'<?xml version="1.1"').replace(
            b'</dict>\n</plist>', b'<key>Invented</key><string>&#x1;</string></dict>\n</plist>')
        self.profile.write_bytes(fx.envelope(xml11))
        status, stdout, stderr = self.main()
        stopped = json.loads((self.out / 'STOPPED.json').read_text())
        self.assertEqual((stopped['reason_code'], stopped['refusals'][0]['found']),
                         ('S2_PROFILE_NOT_ESTABLISHED', 'a declared XML version other than 1.0'))
        info = fx.info_plist().replace(b'<?xml version="1.0"', b'<?xml version="1.1"')
        folder = self.root / 'xml11-candidate'
        folder.mkdir()
        with patch.object(fx, 'info_plist', lambda **_: info):
            self.candidate = fx.candidate(folder) / ''
        self.profile.write_bytes(fx.profile_bytes())
        self.out, self.fake = self.root / 'xml11-out', fx.FakeApple()
        status, stdout, stderr = self.main()
        self.assertEqual(stderr.splitlines()[0], 'STOP: ' + common.REASONS['REFUSED_INFO_PLIST_NOT_ESTABLISHED'])
        self.assertIn('found a declared XML version other than 1.0', stderr)
        self.candidate = self.root / 'candidate'
        self.out, self.fake = self.root / 'xml11-control', fx.FakeApple()
        self.assertEqual(self.main()[0], 0)

    def test_finding_3_and_2_a_reason_is_true_of_the_file_and_need_not_be_the_first(self):
        """No order is promised. With two defects, the one reported is true of the file (its form or shape was met at its
        field); a not-established report says nothing about the other. Each control has the earlier defect alone."""
        late = b'\xa0\x80' + T(0x04, ENVELOPE_CONTENT) + b'\x00\x00'
        signed = T(0x30, VERSION + fx.DIGEST_ALGORITHMS + ENCAP + CERTIFICATES + SIGNERS)
        cases = {
            'review: a wrong eContentType and a later indefinite eContent': (
                fx.envelope(ENVELOPE_CONTENT, encap=T(0x30, SIGNED_OID + late)),
                ('unsupported', 'EncapsulatedContentInfo.eContent', 'an indefinite length'),
                fx.envelope(ENVELOPE_CONTENT, encap=T(0x30, SIGNED_OID + T(0xa0, T(0x04, ENVELOPE_CONTENT)))),
                ('malformed', 'EncapsulatedContentInfo.eContentType', 'another object identifier')),
            'review: SignedData as a SET and a later indefinite element in ContentInfo': (
                T(0x30, SIGNED_OID + T(0xa0, b'\x31' + signed[1:]) + b'\x30\x80\x00\x00'),
                ('unsupported', 'ContentInfo', 'an indefinite length'),
                T(0x30, SIGNED_OID + T(0xa0, b'\x31' + signed[1:])), ('malformed', 'SignedData', 'another tag')),
        }
        for name, (raw, reported, control, alone) in cases.items():
            with self.subTest(name):
                for envelope, expected in ((raw, reported), (control, alone)):
                    with self.assertRaises(common.Refused) as raised:
                        PREPARE.profile_consistency(envelope, fx.sha(envelope), CONSISTENT, now=NOW)
                    detail = raised.exception.detail()
                    self.assertEqual((detail['kind'], detail['field'], detail['found']), expected)
        documents = {
            'review: a comment, then a later syntax error': (plist_document(b'<!--invented--><string></key>'), plist_document(b'<!--invented--><string/>'),
                                                            ('malformed', 'not well-formed XML'), ('unsupported', 'a comment')),
            'review: a standalone declaration, then a later syntax error': (
                plist_document(b'<string></key>', header=b'<?xml version="1.0" standalone="yes"?>\n'),
                plist_document(b'<string/>', header=b'<?xml version="1.0" standalone="yes"?>\n'),
                ('malformed', 'not well-formed XML'), ('unsupported', 'an XML declaration other than version 1.0, or with a standalone declaration')),
        }
        for name, (raw, control, reported, alone) in documents.items():
            with self.subTest(name):
                for document, expected in ((raw, reported), (control, alone)):
                    with self.assertRaises(WHOLE.NotWhole) as raised:
                        WHOLE.load(document)
                    self.assertEqual((raised.exception.kind, raised.exception.found), expected)

    def test_finding_5_a_digest_refusal_says_the_file_was_not_read(self):
        raw = fx.profile_bytes()
        with self.assertRaises(common.Refused) as raised:
            PREPARE.profile_consistency(raw, '7' * 64, CONSISTENT, now=NOW)
        detail = raised.exception.detail()
        self.assertEqual((detail['kind'], detail['found']), ('digest', 'other bytes'))
        line = common.describe(detail)
        self.assertIn('not read', line)
        self.assertNotIn('read whole', line)
        self.assertEqual(PREPARE.profile_consistency(raw, fx.sha(raw), CONSISTENT, now=NOW)['size'], len(raw))
        # every other reason that says "read whole" is a mismatch, reached only after the whole read
        self.assertEqual([k for k, text in WHOLE.KINDS.items() if 'read whole' in text], ['mismatch'])


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

    def test_the_candidate_standing_is_carried_never_inferred(self):
        """An examination candidate signs like any other; its standing reaches the plan, RESULT.json and the record unchanged.
        A candidate whose standing is missing or differs from its plan is refused before any command."""
        examination = fx.standing()['standing']
        self.assertEqual(self.sign(dry_run=True)['release_standing'], examination)
        self.assertEqual(self.sign()['release_standing'], examination)
        self.assertEqual(json.loads((self.out / 'PACKAGE_IDENTITY.json').read_text())['release_standing'], fx.standing())
        for public in (fx.standing(not_for_public_release=False, complete=True), fx.standing(complete=True)):
            with self.subTest(standing=public['standing']):
                root = self.root / ('public' if not public['not_for_public_release'] else 'complete'); root.mkdir()
                result = self.sign(candidate=str(fx.candidate(root, release_standing=public)), out=str(root / 'signed'))
                self.assertEqual(result['release_standing'], public['standing'])
                self.assertEqual(json.loads((root / 'signed/PACKAGE_IDENTITY.json').read_text())['release_standing'], public)
        calls = len(self.fake.calls)
        description_path = self.candidate / common.CANDIDATE_FILE
        original = description_path.read_bytes()
        for name, change in (('missing', None), ('reads as public', {'not_for_public_release': False}),
                             ('other gap count', {'notice_gaps': 4}), ('other coverage digest', {'notice_coverage_sha256': '0' * 64})):
            with self.subTest(name), self.assertRaises(common.Failure) as raised:
                value = json.loads(original)
                if change is None:
                    value.pop('release_standing')
                else:
                    value['release_standing'].update(change)
                description_path.write_text(json.dumps(value))
                self.sign(out=str(self.root / ('signed-' + name.replace(' ', '-'))))
            self.assertEqual(raised.exception.code, 'REFUSED_CANDIDATE')
        description_path.write_bytes(original)
        self.assertEqual(len(self.fake.calls), calls)
        for malformed in (None, fx.standing() | {'notice_gaps': 0}, fx.standing() | {'standing': 'notice coverage complete'}):
            with self.subTest(record_standing=malformed), self.assertRaises(record.RecordFailed) as raised:
                candidate = json.loads(original)
                candidate['release_standing'] = malformed
                record.build_record(dmg=self.out / 'Chirality-4.0.0.dmg', app=self.out / 'staging' / common.APP_NAME, run=self.fake,
                                    candidate=candidate, notarizations={}, signed_tree=None, record_dir=self.out,
                                    public_teams={fx.TEAM, common.SUPPLIER_TEAM}, publisher_team=fx.TEAM, supplier_expected=None)
            self.assertIn('release standing', [f['observation'] for f in raised.exception.failures])

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
            # common.is_private_path compares whole components with case folded (from main): an alias is refused too
            cases[f'{name} inside a case alias of the private folder'] = ({name: str(self.root / common.PRIVATE_FOLDER.upper() / 'x')},
                                                                          'REFUSED_PRIVATE_INPUT')
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
                # is_private_component: by whole name, case aliases included; is_private_path applies it to every part
                self.assertEqual(len([u for u in uses if 'PRIVATE_FOLDER.casefold()' in u]), 1)
                self.assertEqual(len(uses), 3, uses)
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
        # Review round 3, finding 6: a refused profile's fields are named once, under the refusal, and not compared.
        result = self.assert_found('observed.app_as_signed.inventory', failed=('provisioning profile',))
        self.assertFalse([k for k in result['differences'] if k.startswith('observed.provisioning_profile')])
        [refusal] = result['refusals']
        self.assertEqual((refusal['detail']['kind'], refusal['detail']['field']), ('mismatch', 'Entitlements com.apple.application-identifier'))

    def test_a_profile_with_a_key_twice_is_a_failure(self):
        """Of the same kind as round 4 finding 1: the profile's App identifier twice is not read as the last one."""
        twice = lambda xml: xml.replace(b'<key>com.apple.developer.team-identifier</key>',
                                        b'<key>com.apple.application-identifier</key><string>8A7JL35U4S.com.chirality.app</string>'
                                        b'<key>com.apple.developer.team-identifier</key>', 1)
        (self.app / 'Contents/embedded.provisionprofile').write_bytes(fx.profile_bytes(identifier='com.example.other', content=twice))
        failures = []
        facts = record.profile_facts(self.app, {fx.TEAM}, failures)
        self.assertEqual((facts['decoded'], [f['observation'] for f in failures]), (False, ['provisioning profile']))

    def check_main(self):
        out, err = io.StringIO(), io.StringIO()
        code = record.main(['check', str(self.out / 'PACKAGE_IDENTITY.json'), '--dmg', str(self.dmg), '--app', str(self.app),
                            '--candidate', str(self.case.candidate)], run=self.case.fake, stdout=out, stderr=err)
        return code, json.loads(out.getvalue() or err.getvalue())

    def test_a_package_whose_info_plist_or_profile_is_not_whole_is_not_equal(self):
        for relative, raw, control, observation in (
                ('Contents/Info.plist', fx.conflicting_info_plist(), fx.info_plist(), 'bundle identity'),
                ('Contents/embedded.provisionprofile', fx.conflicting_profile_bytes(), fx.profile_bytes(), 'provisioning profile')):
            with self.subTest(relative):
                (self.app / relative).write_bytes(raw)
                result = self.assert_found(failed=(observation,))
                self.assertEqual(result['failed_observations'], {observation: 1})
                self.assertEqual([(r['observation'], r['detail']['found'], r['line']) for r in result['refusals']],
                                 [(observation, 'a second value under plist', common.describe(result['refusals'][0]['detail']))])
                self.assertEqual(result['not_established'], [])
                code, printed = self.check_main()
                self.assertEqual((code, printed['equal']), (1, False))
                (self.app / relative).write_bytes(control)
                self.assertTrue(self.result()['equal'])

    def test_a_file_in_a_form_not_read_is_not_established_not_a_difference(self):
        """A form the reader does not read: a failed observation named 'not established', no difference for the fields
        it would have shown, those fields listed as not established, not equal, and exit 1 (a result), not 2 (unread)."""
        for relative, raw, control, observation, fields in (
                ('Contents/embedded.provisionprofile', UNREAD_PROFILE, fx.profile_bytes(), 'provisioning profile not established',
                 ['observed.provisioning_profile']),
                ('Contents/Info.plist', UNREAD_INFO_PLIST, fx.info_plist(), 'bundle identity not established',
                 ['observed.bundle.bundle_version', 'observed.bundle.executable', 'observed.bundle.identifier',
                  'observed.bundle.minimum_system_version', 'observed.bundle.version'])):
            with self.subTest(observation):
                (self.app / relative).write_bytes(raw)
                result = self.result()
                self.assertFalse(result['equal'])
                self.assertEqual(result['failed_observations'], {observation: 1})
                self.assertEqual(result['not_established'], fields)
                self.assertFalse([k for k in result['differences'] if any(k.startswith(f + ':') or k.startswith(f + '.') for f in fields)],
                                 result['differences'])
                [refusal] = result['refusals']
                self.assertEqual((refusal['detail']['kind'], refusal['detail']['found']), ('unsupported', 'a comment'))
                self.assertIn('the identity comparison is not established', refusal['line'])
                code, printed = self.check_main()
                self.assertEqual((code, printed['equal'], printed['not_established']), (1, False, fields))
                (self.app / relative).write_bytes(control)
                self.assertTrue(self.result()['equal'])

    def test_each_envelope_rule_at_record_check(self):
        """Every envelope case, as the profile in the package: the failed observation by kind, with exactly that refusal."""
        for name, (raw, (kind, field, found, item)) in ENVELOPE_CASES.items():
            with self.subTest(name):
                (self.app / 'Contents/embedded.provisionprofile').write_bytes(raw)
                result = self.result()
                observation = 'provisioning profile' + (' not established' if kind == 'unsupported' else '')
                self.assertEqual((result['equal'], result['failed_observations']), (False, {observation: 1}))
                [refusal] = result['refusals']
                detail = refusal['detail']
                self.assertEqual((detail['part'], detail['kind'], detail['field'], detail['found'], detail.get('item')),
                                 (case_part(name), kind, field, found, item))
                self.assertEqual(result['not_established'], ['observed.provisioning_profile'] if kind == 'unsupported' else [])
        (self.app / 'Contents/embedded.provisionprofile').write_bytes(fx.profile_bytes())
        self.assertTrue(self.result()['equal'])

    def test_typed_and_hostile_files_are_named_failures_never_exit_2(self):
        """Review round 2, finding 5: a profile whose TeamIdentifier was 42 or a nested array made record.py check exit 2,
        one keyed by the team passed unobserved, and an integer bundle version gave 'bundle identity' with no detail."""
        profiles = {name: profile_with(**{field: item}) for name, (field, item) in WRONG_PROFILE_TYPES.items()}
        profiles.update({'review: Shift_JIS content': fx.envelope(ENVELOPE_CONTENT.replace(b'UTF-8', b'Shift_JIS')),
                         'review: an empty profile file': b''})
        infos = {name: info_with(**{key: item}) for name, (key, item, _) in WRONG_INFO_TYPES.items()}
        infos.update({'review: Shift_JIS declared': fx.info_plist().replace(b'UTF-8', b'Shift_JIS'), 'an empty Info.plist': b''})
        for relative, cases, observation in (('Contents/embedded.provisionprofile', profiles, 'provisioning profile'),
                                             ('Contents/Info.plist', infos, 'bundle identity')):
            control = (self.app / relative).read_bytes()
            for name, raw in cases.items():
                with self.subTest(name):
                    (self.app / relative).write_bytes(raw)
                    code, result = self.check_main()
                    self.assertEqual((code, result['equal'], result.get('error')), (1, False, None))
                    named = [r for r in result['refusals'] if r['observation'].startswith(observation)]
                    self.assertEqual(len(named), 1, result['refusals'])
                    kind = named[0]['detail']['kind']
                    self.assertEqual(named[0]['observation'], observation + (' not established' if kind == 'unsupported' else ''))
            (self.app / relative).write_bytes(control)
        self.assertEqual(self.check_main()[0], 0)

    def test_review_3_finding_2_xml_1_1_is_not_established_at_record_check(self):
        for relative, raw, fields in (
                ('Contents/Info.plist', fx.info_plist().replace(b'<?xml version="1.0"', b'<?xml version="1.1"'),
                 ['observed.bundle.' + k for k in ('bundle_version', 'executable', 'identifier', 'minimum_system_version', 'version')]),
                ('Contents/embedded.provisionprofile', fx.envelope(ENVELOPE_CONTENT.replace(b'<?xml version="1.0"', b'<?xml version="1.1"')),
                 ['observed.provisioning_profile'])):
            with self.subTest(relative):
                control = (self.app / relative).read_bytes()
                (self.app / relative).write_bytes(raw)
                code, result = self.check_main()
                self.assertEqual((code, result['not_established']), (1, fields))
                [refusal] = result['refusals']
                self.assertEqual(refusal['detail']['found'], 'a declared XML version other than 1.0')
                (self.app / relative).write_bytes(control)
        self.assertEqual(self.check_main()[0], 0)

    def test_review_3_finding_6_a_refused_identity_is_not_compared(self):
        """Only CFBundleExecutable mistyped: the other identity fields were reported as differing, because the refusal
        replaced the whole identity with empty values. A refused file's fields are now named once, under the refusal;
        byte and inventory differences stay."""
        identity = ['observed.bundle.' + key for key in ('identifier', 'version', 'bundle_version', 'minimum_system_version', 'executable')]
        (self.app / 'Contents/Info.plist').write_bytes(info_with(CFBundleExecutable=5))
        code, result = self.check_main()
        self.assertEqual((code, result['failed_observations']), (1, {'bundle identity': 1}))
        self.assertFalse([k for k in result['differences'] if any(k.startswith(f + ':') for f in identity)], result['differences'])
        self.assertIn('observed.bundle.info_plist_sha256: differs', result['differences'])  # the bytes did change
        [refusal] = result['refusals']
        self.assertEqual((refusal['detail']['field'], refusal['detail']['kind']), ('CFBundleExecutable', 'mismatch'))
        self.assertEqual(result['not_established'], [])
        (self.app / 'Contents/Info.plist').write_bytes(fx.info_plist())
        self.assertEqual(self.check_main()[0], 0)

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

    def test_an_entitlement_document_that_is_not_whole_is_never_equal(self):
        """The fifth reading's check result: equal=true with the candidate given. With every other fact truthful, the App's
        or one supplier executable's entitlements read as a probe are a failed observation, and nothing else is."""
        truthful = self.result(candidate_dir=self.case.candidate)
        self.assertEqual((truthful['equal'], truthful['failed_observations']), (True, {}))
        vendor = str(self.app / 'Contents/Resources/codex/codex-path/rg')
        for name, raw in whole_document_probes().items():
            for where in ('app', 'supplier'):
                with self.subTest(probe=name, where=where):
                    fake = self.case.fake
                    fake.app_entitlements_override = raw if where == 'app' else None
                    fake.override = {('--entitlements', vendor): Result(0, raw)} if where == 'supplier' else {}
                    result = self.result(candidate_dir=self.case.candidate)
                    self.assertFalse(result['equal'])
                    self.assertEqual(result['failed_observations'], {'entitlements': 1})
                    # An invented vendor path is not in the committed inventory, so its location is counted, not named.
                    prefix = 'observed.signatures..' if where == 'app' else 'observed.signatures'
                    self.assertTrue(result['differences'] and all(k.startswith(prefix) for k in result['differences']), result['differences'])
        self.case.fake.app_entitlements_override, self.case.fake.override = None, {}
        self.assertTrue(self.result(candidate_dir=self.case.candidate)['equal'])

    def test_the_release_standing_is_stated_and_checked_only_against_the_candidate(self):
        """App Agent 0's standing decision: the record copies the candidate's standing; check states it, compares it with
        the candidate only when given one, and a missing or mismatched value is never equal."""
        examination = fx.standing()
        self.assertEqual(self.identity['release_standing'], examination)
        self.assertTrue(self.identity['release_standing']['not_for_public_release'])
        unchecked = self.result()
        self.assertTrue(unchecked['equal'])
        self.assertEqual(unchecked['release_standing'], {'stated_by_record': examination['standing'], 'checked_against_candidate': False})
        self.assertIn(record.NOT_CHECKED_CANDIDATE, unchecked['not_checked'])
        checked = self.result(candidate_dir=self.case.candidate)
        self.assertTrue(checked['equal'], checked)
        self.assertEqual(checked['release_standing'], {'stated_by_record': examination['standing'], 'checked_against_candidate': True})
        # A record whose standing reads as public while its candidate was named not for public release differs.
        public = fx.standing(not_for_public_release=False, complete=True)
        self.identity['release_standing'] = public
        self.assertTrue(self.result()['equal'])  # without --candidate only the record's own words, listed as not checked
        self.assert_found('release_standing.not_for_public_release', 'release_standing.standing', 'release_standing.notice_gaps',
                          candidate_dir=self.case.candidate)
        # Missing or malformed in the record: refused as structure, never equal, whether or not a candidate is given.
        for change in ({}, {'standing': 'notice coverage complete'}, {'notice_gaps': 0}, {'notice_gaps': True},
                       {'not_for_public_release': 'yes'}, {'notice_coverage_sha256': 'x'}, {'extra': 1}):
            for candidate_dir in (None, self.case.candidate):
                with self.subTest(change=change, candidate=candidate_dir is not None):
                    broken = json.loads(json.dumps(self.identity)) | {'release_standing': examination | change}
                    if not change:
                        del broken['release_standing']
                    result = record.check(broken, dmg=self.dmg, app=self.app, run=self.case.fake, record_dir=self.out,
                                          candidate_dir=candidate_dir)
                    self.assertFalse(result['equal'])
                    self.assertTrue(any(m.startswith('release_standing') for m in result['record_structure_missing']), result)
                    self.assertEqual(result['release_standing'], {'stated_by_record': 'not observed', 'checked_against_candidate': False})
        self.identity['release_standing'] = examination
        # The candidate's own standing must agree with its bound plan, or the check fails instead of comparing.
        description_path = self.case.candidate / common.CANDIDATE_FILE
        original = description_path.read_bytes()
        for change in ({'notice_gaps': 4}, None):
            with self.subTest(candidate_change=change):
                value = json.loads(original)
                if change is None:
                    value.pop('release_standing')
                else:
                    value['release_standing'].update(change)
                description_path.write_text(json.dumps(value))
                result = self.assert_found(failed=('candidate release standing',), candidate_dir=self.case.candidate)
                self.assertFalse(result['release_standing']['checked_against_candidate'])
        description_path.write_bytes(original)

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
                          '--candidate', str(private)],
                         ['check', str(self.case.root / common.PRIVATE_FOLDER.lower() / 'PACKAGE_IDENTITY.json'), '--dmg', str(self.dmg),
                          '--app', str(self.app)]):
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
        self.assertFalse([path for path in read if common.PRIVATE_FOLDER.casefold() in path.casefold()], read)

    def test_the_original_log_options_are_gone(self):
        err = io.StringIO()
        with patch('sys.stderr', err), self.assertRaises(SystemExit):
            record.main(['check', str(self.out / 'PACKAGE_IDENTITY.json'), '--dmg', str(self.dmg), '--app', str(self.app),
                         '--app-original-log', str(self.case.root / 'any.json')], run=self.case.fake)
        self.assertIn('usage error', err.getvalue())


if __name__ == '__main__':
    unittest.main()
