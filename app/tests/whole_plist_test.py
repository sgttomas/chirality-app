"""The whole-document property-list file reader (app/packaging/production_inputs/whole_plist.py), on invented documents.

Every value here is invented: the team identifiers, App IDs, UUID and dates name nothing real, and the profile
envelopes are built from invented bytes and are never Apple-signed. Beside each refusal is a control that reads.
"""
import base64
import datetime
import importlib.util
from pathlib import Path
import plistlib
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location('whole_plist_test_prepare', ROOT / 'app/packaging/production_inputs/prepare.py')
prepare = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(prepare)
whole = prepare.whole_plist

HEADER = (b'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" '
          b'"http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n')
TEAM, OTHER = 'ZZINVENT01', 'QQOTHER001'
EXPECTED = {'com.apple.application-identifier': TEAM + '.invalid.example.reader', 'com.apple.developer.team-identifier': TEAM}
EXPECTED_DICT = (b'<dict>\n\t<key>com.apple.application-identifier</key>\n\t<string>ZZINVENT01.invalid.example.reader</string>\n'
                 b'\t<key>com.apple.developer.team-identifier</key>\n\t<string>ZZINVENT01</string>\n</dict>')
# Another team's App ID with get-task-allow: the first of the conflicting pair.
OTHER_DICT = (b'<dict>\n\t<key>com.apple.application-identifier</key>\n\t<string>QQOTHER001.invalid.example.other</string>\n'
              b'\t<key>com.apple.developer.team-identifier</key>\n\t<string>QQOTHER001</string>\n'
              b'\t<key>com.apple.security.get-task-allow</key>\n\t<true/>\n</dict>')


def document(body, header=HEADER, after=b''):
    return header + b'<plist version="1.0">\n' + body + b'\n</plist>\n' + after


def inside(extra, at=b'\t<key>com.apple.developer.team-identifier</key>'):
    """The expected dictionary with `extra` placed before its second key."""
    return document(EXPECTED_DICT.replace(at, extra + at, 1))


CONTROL = document(EXPECTED_DICT)
REFUSED = {
    # name: (document, the reason it names)
    'conflicting pair: two sibling dictionaries': (document(OTHER_DICT + b'\n' + EXPECTED_DICT), 'a second value under plist'),
    'text before the expected dictionary': (document(b'stray text' + EXPECTED_DICT), 'text outside a value'),
    'a sibling string': (document(EXPECTED_DICT + b'\n<string>' + OTHER.encode() + b'</string>'), 'a second value under plist'),
    'an unknown element in the dictionary': (inside(b'<note>' + OTHER.encode() + b'</note>\n'),
                                             'an element that is not a property-list element'),
    'an unknown element under plist': (document(b'<note/>' + EXPECTED_DICT), 'an element that is not a property-list element'),
    'an attribute': (document(EXPECTED_DICT.replace(b'<dict>', b'<dict team="' + OTHER.encode() + b'">', 1)),
                     'an attribute other than the root version'),
    'an attribute on the root other than version': (CONTROL.replace(b'<plist version="1.0">', b'<plist version="1.0" team="x">'),
                                                    'an attribute other than the root version'),
    'a comment': (inside(b'<!-- ' + OTHER.encode() + b' -->\n'), 'a comment'),
    'a comment in the header': (document(EXPECTED_DICT, header=HEADER + b'<!-- invented -->\n'), 'a comment'),
    'a processing instruction': (inside(b'<?invented ' + OTHER.encode() + b'?>\n'), 'a processing instruction'),
    'a key twice': (inside(b'<key>com.apple.application-identifier</key><string>QQOTHER001.invalid.example.other</string>\n'),
                    'a key twice in one dictionary'),
    'a dictionary with a key and no value': (document(b'<dict><key>com.apple.application-identifier</key></dict>'), 'a key with no value'),
    'a key followed by a key': (inside(b'<key>invented</key>\n'), 'a key with no value'),
    'a value with no key': (inside(b'<string>' + OTHER.encode() + b'</string>\n'), 'a value with no key in a dictionary'),
    'an entity declaration': (document(EXPECTED_DICT.replace(b'ZZINVENT01</string>\n</dict>', b'&team;</string>\n</dict>'),
                                       header=b'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist [<!ENTITY team "QQOTHER001">]>\n'),
                              'an entity declaration, an undefined entity or an external entity'),
    'an undefined entity': (document(EXPECTED_DICT.replace(b'ZZINVENT01</string>\n</dict>', b'&team;</string>\n</dict>')),
                            'an entity declaration, an undefined entity or an external entity'),
    'trailing bytes after the document': (document(EXPECTED_DICT, after=b'<plist version="1.0"><dict/></plist>'),
                                          'bytes after the document element'),
    'trailing text after the document': (document(EXPECTED_DICT, after=b'QQOTHER001'), 'bytes after the document element'),
    'a comment after the document': (document(EXPECTED_DICT, after=b'<!-- invented -->'), 'a comment'),
    'a character reference between elements': (document(b'&#32;' + EXPECTED_DICT), 'text outside a value'),
    'a CDATA section between elements': (document(b'<![CDATA[ ]]>' + EXPECTED_DICT), 'text outside a value'),
    'no value under plist': (document(b''), 'no value under plist'),
    'a key outside a dictionary': (document(b'<array><key>a</key></array>'), 'a key outside a dictionary'),
    'an element inside a string': (document(b'<string>a<string>b</string></string>'), 'an element inside a leaf value'),
    'a binary property list': (plistlib.dumps(EXPECTED, fmt=plistlib.FMT_BINARY),
                               'a binary property list; only an XML property list is read as a whole document'),
    'another document type': (document(EXPECTED_DICT, header=b'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE invented>\n'),
                              'a document header other than the XML declaration and the property-list document type'),
    'another encoding': (document(EXPECTED_DICT, header=HEADER.replace(b'UTF-8', b'ISO-8859-1')),
                         'a document header other than the XML declaration and the property-list document type'),
    'no XML declaration': (b'<plist version="1.0">' + EXPECTED_DICT + b'</plist>', 'not an XML document beginning with its XML declaration'),
    'a byte order mark': (b'\xef\xbb\xbf' + CONTROL, 'not an XML document beginning with its XML declaration'),
    'an integer spelled with an underscore': (document(b'<integer>1_0</integer>'), 'a leaf value of an undeclared spelling: integer'),
    'a real spelled as nan': (document(b'<real>nan</real>'), 'a leaf value of an undeclared spelling: real'),
    'a partial date': (document(b'<date>2026Z</date>'), 'a leaf value of an undeclared spelling: date'),
    'a date with trailing text': (document(b'<date>2026-01-01T00:00:00Zjunk</date>'), 'a leaf value of an undeclared spelling: date'),
    'data with a character outside base64': (document(b'<data>AAAA!!!!</data>'), 'a leaf value of an undeclared spelling: data'),
    'text inside true': (document(b'<true>no</true>'), 'a leaf value of an undeclared spelling: true'),
    'not well-formed': (CONTROL.replace(b'</dict>', b'</array>'), 'not well-formed XML'),
}


class Refusals(unittest.TestCase):
    def test_the_control_reads_the_expected_values(self):
        self.assertEqual(whole.load(CONTROL), EXPECTED)

    def test_each_refusal_names_what_was_left_over(self):
        for name, (raw, why) in REFUSED.items():
            with self.subTest(name):
                with self.assertRaises(whole.NotWhole) as raised:
                    whole.load(raw)
                self.assertEqual(raised.exception.why, why)
                self.assertIsInstance(raised.exception, ValueError)  # every caller already stops on ValueError
                self.assertEqual(whole.load(CONTROL), EXPECTED)

    def test_the_standard_parser_alone_reads_part_of_the_conflicting_pair(self):
        """What the file readers did before: plistlib keeps the last of two sibling values and ignores the rest."""
        raw = REFUSED['conflicting pair: two sibling dictionaries'][0]
        self.assertEqual(plistlib.loads(raw), EXPECTED)
        for name in ('text before the expected dictionary', 'a comment', 'a processing instruction', 'an attribute',
                     'an unknown element in the dictionary'):
            with self.subTest(name):
                self.assertEqual(plistlib.loads(REFUSED[name][0]), EXPECTED)

    def test_nothing_is_fetched(self):
        external = document(EXPECTED_DICT.replace(b'ZZINVENT01</string>\n</dict>', b'&team;</string>\n</dict>'),
                            header=b'<?xml version="1.0"?>\n<!DOCTYPE plist [<!ENTITY team SYSTEM "http://invalid.example/x">]>\n')
        with patch('urllib.request.urlopen', side_effect=AssertionError('fetched')), self.assertRaises(whole.NotWhole):
            whole.load(external)

    def test_the_two_readers_must_agree(self):
        """The structural reading is not plistlib's: when plistlib reads another value, or refuses, the document refuses."""
        with patch.object(whole.plistlib, 'loads', return_value=plistlib.loads(document(OTHER_DICT))):
            with self.assertRaises(whole.NotWhole) as raised:
                whole.load(CONTROL)
            self.assertEqual(raised.exception.why, 'the standard parser reads another value')
        with patch.object(whole.plistlib, 'loads', side_effect=plistlib.InvalidFileException()):
            with self.assertRaises(whole.NotWhole) as raised:
                whole.load(CONTROL)
            self.assertEqual(raised.exception.why, 'the standard parser refuses the document')
        # Types count: a boolean is not the integer 1, though Python compares them equal.
        with patch.object(whole.plistlib, 'loads', return_value={'a': 1}), self.assertRaises(whole.NotWhole):
            whole.load(document(b'<dict><key>a</key><true/></dict>'))
        self.assertEqual(whole.load(CONTROL), EXPECTED)


class Controls(unittest.TestCase):
    """Valid spellings that plistlib would not write, and that a real file may hold, read as their values."""

    def test_data_wrapped_at_several_widths(self):
        payload = bytes(range(256)) * 3
        encoded = base64.b64encode(payload).decode()
        for width in (len(encoded), 76, 68, 60, 52, 4, 1):
            lines = [encoded[i:i + width] for i in range(0, len(encoded), width)]
            for joiner in ('\n', '\n\t', '\r\n\t\t', ' '):
                with self.subTest(width=width, joiner=joiner):
                    raw = document(b'<dict><key>DeveloperCertificates</key><array><data>\n' + joiner.join(lines).encode()
                                   + b'\n</data></array></dict>')
                    self.assertEqual(whole.load(raw), {'DeveloperCertificates': [payload]})

    def test_a_date(self):
        raw = document(b'<dict><key>ExpirationDate</key><date>2099-01-02T03:04:05Z</date></dict>')
        self.assertEqual(whole.load(raw), {'ExpirationDate': datetime.datetime(2099, 1, 2, 3, 4, 5)})

    def test_crlf_line_endings(self):
        self.assertEqual(whole.load(CONTROL.replace(b'\n', b'\r\n')), EXPECTED)

    def test_empty_dictionaries(self):
        for spelling in (b'<dict/>', b'<dict></dict>', b'<dict>\n\t</dict>'):
            with self.subTest(spelling=spelling):
                self.assertEqual(whole.load(document(spelling)), {})
                self.assertEqual(whole.load(document(b'<dict><key>Entitlements</key>' + spelling + b'</dict>')), {'Entitlements': {}})
        self.assertEqual(whole.load(document(b'<array/>')), [])

    def test_whitespace_inside_a_string_is_kept(self):
        raw = document(b'<dict><key> invented key </key><string>  two  spaces\n\tand a tab </string></dict>')
        self.assertEqual(whole.load(raw), {' invented key ': '  two  spaces\n\tand a tab '})

    def test_other_valid_spellings_of_values(self):
        raw = document(b'<array><true></true><false/><integer>-7</integer><integer>+7</integer><integer>0x1F</integer>'
                       b'<real>1.5e3</real><real>.5</real><string>a &amp; b &#x41; <![CDATA[<c>]]></string><string/></array>')
        self.assertEqual(whole.load(raw), [True, False, -7, 7, 31, 1500.0, 0.5, 'a & b A <c>', ''])

    def test_header_spellings(self):
        for header in (b"<?xml version='1.0' encoding='utf-8'?>\n", b'<?xml version="1.0"?>',
                       b"<?xml version='1.0'?>\n<!DOCTYPE plist PUBLIC '-//Apple//DTD PLIST 1.0//EN' "
                       b"'http://www.apple.com/DTDs/PropertyList-1.0.dtd'>\n"):
            with self.subTest(header=header):
                self.assertEqual(whole.load(document(EXPECTED_DICT, header=header)), EXPECTED)
        self.assertEqual(whole.load(CONTROL.replace(b'<plist version="1.0">', b'<plist>')), EXPECTED)

    def test_what_plistlib_writes_reads(self):
        value = {'CFBundleIdentifier': 'invalid.example.reader', 'Nested': {'List': [1, 2.5, True, b'\x00\xff', 'x']},
                 'When': datetime.datetime(2026, 1, 1)}
        for sort_keys in (True, False):
            self.assertEqual(whole.load(plistlib.dumps(value, sort_keys=sort_keys)), value)


def tlv(tag, body):
    n = len(body)
    length = bytes([n]) if n < 0x80 else bytes([0x80 | ((n.bit_length() + 7) // 8)]) + n.to_bytes((n.bit_length() + 7) // 8, 'big')
    return bytes([tag]) + length + body


def envelope(content, after_content=(tlv(0x31, b'INVENTED signer info; never Apple-signed'),)):
    """An invented CMS-shaped envelope; never Apple-signed."""
    encap = tlv(0x30, tlv(0x06, prepare.DATA_OID) + tlv(0xa0, tlv(0x04, content)))
    signed = tlv(0x30, tlv(0x02, b'\x01') + tlv(0x31, b'') + encap + b''.join(after_content))
    return tlv(0x30, tlv(0x06, prepare.SIGNED_DATA_OID) + tlv(0xa0, signed))


def profile_xml(*dicts):
    return document(b'\n'.join(dicts))


PROFILE_DICT = (b'<dict>\n\t<key>ApplicationIdentifierPrefix</key><array><string>ZZINVENT01</string></array>\n'
                b'\t<key>CreationDate</key><date>2020-01-01T00:00:00Z</date>\n'
                b'\t<key>Entitlements</key>' + EXPECTED_DICT + b'\n'
                b'\t<key>ExpirationDate</key><date>2099-01-01T00:00:00Z</date>\n'
                b'\t<key>Platform</key><array><string>OSX</string></array>\n'
                b'\t<key>ProvisionsAllDevices</key><true/>\n'
                b'\t<key>TeamIdentifier</key><array><string>ZZINVENT01</string></array>\n'
                b'\t<key>UUID</key><string>0A1B2C3D-0000-4000-8000-00000000BEEF</string>\n</dict>')
OTHER_PROFILE_DICT = PROFILE_DICT.replace(EXPECTED_DICT, OTHER_DICT).replace(b'ZZINVENT01', b'QQOTHER001')
SELECTED = {'developer_id_team_identifier': TEAM, 'production_bundle_identifier': 'invalid.example.reader'}
NOW = datetime.datetime(2026, 11, 12)


class ProfileEnvelope(unittest.TestCase):
    def consistency(self, raw):
        return prepare.profile_consistency(raw, prepare.sha(raw), SELECTED, now=NOW)

    def test_the_conflicting_pair_refuses_and_the_control_reads(self):
        control = envelope(profile_xml(PROFILE_DICT))
        self.assertEqual(self.consistency(control)['application_identifier'], TEAM + '.invalid.example.reader')
        pair = envelope(profile_xml(OTHER_PROFILE_DICT, PROFILE_DICT))
        with self.assertRaises(whole.NotWhole) as raised:
            self.consistency(pair)
        self.assertEqual(raised.exception.why, 'a second value under plist')

    def test_the_bytes_around_the_content_are_declared_elements_with_nothing_left_over(self):
        signer = tlv(0x31, b'INVENTED signer info')
        content = profile_xml(PROFILE_DICT)
        for name, after in (('certificates, then signer information', (tlv(0xa0, b'INVENTED certificates'), signer)),
                            ('certificates, revocation lists, signer information', (tlv(0xa0, b'c'), tlv(0xa1, b'r'), signer))):
            with self.subTest(name):
                self.assertEqual(prepare.profile_content(envelope(content, after)), content)
        for name, after in (('no signer information', ()),
                            ('a second property list after the content', (tlv(0x04, profile_xml(OTHER_PROFILE_DICT)), signer)),
                            ('signer information twice', (signer, signer)),
                            ('certificates after signer information', (signer, tlv(0xa0, b'c')))):
            with self.subTest(name):
                with self.assertRaisesRegex(ValueError, 'SignedData after the encapsulated content'):
                    prepare.profile_content(envelope(content, after))
        with self.assertRaises(ValueError):  # a byte that is no element
            prepare.profile_content(envelope(content, (signer, b'\x00')))


if __name__ == '__main__':
    unittest.main()
