"""Prepare exact unsigned release-build inputs; never build, sign or launch."""
import argparse
import datetime
import importlib.util
import importlib.metadata
import json
import os
from pathlib import Path
import re
import tomllib

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[3]

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    value = importlib.util.module_from_spec(spec); spec.loader.exec_module(value)
    return value

inventory = load_module('production_input_inventory', 'app/packaging/inventory.py')
files = load_module('production_input_files', 'app/packaging/static_distribution/check.py')
# The one reader of a property-list file whose value is the whole document (the profile here; Info.plist in release/).
whole_plist = load_module('production_input_whole_plist', 'app/packaging/production_inputs/whole_plist.py')
sha, parse, require = files.sha, files.parse, files.require


class NoticeCoverageIncomplete(ValueError):
    """The notice gate's refusal of a production plan not named as not for public release.

    `open_components` are the names of the account's open components (repository content); `other_gaps` counts
    the gaps that are not account rows (another supplier described, or a plan mapping the account does not name).
    """

    def __init__(self, open_components, other_gaps, message):
        super().__init__(message)
        self.open_components, self.other_gaps = list(open_components), other_gaps


def identity(path):
    value = os.stat(path, follow_symlinks=False)
    return value.st_dev, value.st_ino


def ancestors(path):
    return {identity(p) for p in (path, *path.parents)}


def no_overlap(parent, protected):
    """Case aliases and macOS firmlinks must not hide an input ancestor."""
    require(parent.is_dir(), 'existing physical output parent required')
    require(not ancestors(parent).intersection(identity(p) for p in protected),
            'output and selected input overlap by filesystem identity')


def require_nonempty(tree):
    for directory in [''] + [e['path'] for e in tree['entries'] if e['kind'] == 'dir']:
        prefix = directory + '/' if directory else ''
        require(any(e['kind'] == 'file' and e['path'].startswith(prefix) for e in tree['entries']),
                'empty resource directory would be omitted by the bundler')


def write_new(path, raw):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'wb') as output:
        output.write(raw)
        output.flush()
        os.fsync(output.fileno())


def check_plan(output):
    output = inventory.anchored(output)
    require(not os.path.lexists(output / 'INCOMPLETE.txt'), 'plan is incomplete')
    marker = parse(files.transfer(output / 'PLAN_COMPLETE.json', retain=True)[0])
    require(set(marker) == {'files'} and set(marker['files']) ==
            {'tauri.package-inputs.conf.json', 'build-recipe.json', 'input-inventory.json'}, 'invalid completion marker')
    for name, digest in marker['files'].items():
        require(files.transfer(output / name)[1] == digest, 'completed plan file changed')
    recipe = parse(files.transfer(output / 'build-recipe.json', retain=True)[0])
    if 'cargo_build_input' in recipe:
        contract = recipe['cargo_build_input']
        require(contract == cargo_build_input_contract(contract.get('preset')), 'invalid Cargo build input contract')
    return marker


CARGO_BUILD_PRESET = 'macos-arm64-rust-1.97.1-no-strip'


def cargo_build_input_contract(preset):
    """Explicit opt-in for the measured toolchain; never a global Cargo default."""
    require(preset == CARGO_BUILD_PRESET, 'unsupported Cargo build input preset')
    text = ('[net]\noffline = true\n[build]\njobs = 2\n\n'
            '[profile.release.build-override]\nstrip = "none"\n\n'
            '[profile.release]\nstrip = "none"\n')
    return {'preset': preset, 'destination': 'CARGO_HOME/config.toml', 'text': text, 'sha256': sha(text.encode()),
            'scope': {'host': 'aarch64-apple-darwin', 'target': 'aarch64-apple-darwin', 'macos': '27.2', 'sdk': '27.2'},
            'tool_sha256': {
                'rustc': '210df6794001b73ec3d453878707fa1e0bdcb63c427024a6e6574bbe5615a4da',
                'cargo': '7672ead309d505577c018fff2cafb3433601f073e38cbe87359ac1f7b944bbf5',
                'clang': 'fc5e3cbba6ad54059295cad716aacb05ace8235f5f7a6031f1d8c15d24bd6d66',
                'ld': '7f7041b1bb30e5e6a815a55edf374065d5c82e1ab93f84d5b6ed5656ded24bcf'},
            'release_opt_level': 3,
            'standing': 'host build dependencies/proc-macros AND shipped release targets are unstripped; '
                        'no bit-identical output claim; require Apple dyld_info -validate_only on actual bundled Mach-Os'}


def verify_cargo_build_input(output, cargo_home, scope, tool_paths):
    """Read-only pre-build check; caller supplies observed scope and resolved tool paths."""
    check_plan(output)
    recipe = parse(files.transfer(Path(output) / 'build-recipe.json', retain=True)[0])
    require('cargo_build_input' in recipe, 'plan has no selected Cargo build input')
    contract = recipe['cargo_build_input']
    require(scope == contract['scope'], 'Cargo build input platform scope mismatch')
    require(set(tool_paths) == set(contract['tool_sha256']), 'exact resolved Cargo tool paths required')
    for name, digest in contract['tool_sha256'].items():
        require(files.transfer(tool_paths[name])[1] == digest, 'Cargo build input toolchain mismatch: ' + name)
    raw, digest, _ = files.transfer(inventory.anchored(cargo_home) / 'config.toml', retain=True)
    require(digest == contract['sha256'] and raw == contract['text'].encode(), 'Cargo build config mismatch')
    return contract['sha256']


SIGNED_DATA_OID = bytes.fromhex('2a864886f70d010702')
DATA_OID = bytes.fromhex('2a864886f70d010701')

# --- The provisioning profile's envelope: RFC 5652 ContentInfo / SignedData, read as definite-length DER -------------
#
# What the envelope reading is for: the identity facts come only from the property list in the envelope's content, and
# nothing authenticates the envelope. So the reading claims exactly this enforced list, and no more:
#   1. The file is one definite-length element, of 1 byte to PROFILE_LIMIT, with no byte after it.
#   2. From the outside down to the content, the structure is the declared one: ContentInfo (a SEQUENCE of id-signedData
#      and [0]), SignedData with its version (an INTEGER of one octet, 0 to 5), digestAlgorithms, encapContentInfo (id-data
#      and [0] holding one primitive OCTET STRING), then optional certificates [0] and revocation lists [1], then
#      signerInfos, and nothing after.
#   3. Every element's length lies inside its parent at every level walked, with no byte unaccounted for at any level.
#   4. The property list is the whole of that one content string, read by the whole-document reader (whole_plist.load).
# Further refusals, not validation: the outer shapes of the other fields (each digest algorithm a SEQUENCE beginning with
# an OBJECT IDENTIFIER; each certificate and revocation list a SEQUENCE of a SEQUENCE, a SEQUENCE and a BIT STRING; each
# signer information a SEQUENCE beginning with its version), and the universal-type rules in ENVELOPE_TYPE_RULES where
# the walk meets them. The contents of digest algorithm parameters, certificates, revocation lists and signer
# information are length-walked but not validated as ASN.1: some universal-type rules met there are refused (those in
# ENVELOPE_TYPE_RULES, such as a constructed OBJECT IDENTIFIER) and others are not (a reserved universal tag, a primitive
# EXTERNAL or EMBEDDED PDV, the contents of strings and times, among others). Validating them would add no assurance
# about who wrote the content, since nothing authenticates the envelope. A certificate can
# legitimately carry arbitrary bytes inside its own fields, so "no other property list anywhere in the file" is not
# claimed. Nothing is authenticated.
#
# The kinds (whole_plist): a form outside the subset this reader reads (an indefinite length, a length in more octets
# than needed, a constructed string, a tag number in the high-tag-number form, a BOOLEAN other than 00 or FF, an element
# more than ENVELOPE_DEPTH levels below the element its walk starts from, a file larger than PROFILE_LIMIT) is
# 'unsupported', shown as not established: the reader
# names the form and the field and did not read the file; it asserts nothing about whether the file is otherwise valid.
# 'malformed' is asserted only where the reader is certain within its subset (an element past its parent or cut off,
# bytes left over, a reserved length octet, an indefinite length on a primitive element, an empty file, a field not of
# its declared shape, a version out of range, ...). A refusal's reason is true of the file: the named form or shape was
# met at the named field. Where a file has more than one defect, the one reported need not be the first, and a "not
# established" report says nothing about defects elsewhere.

PROFILE_LIMIT = 256 * 1024  # a profile is a short property list and a few certificates; this bounds the reader's memory
# Counted from the element each walk starts from (each digest algorithm, certificate, revocation list and signer
# information, the version and the two object identifiers), not from ContentInfo: an element 64 levels below it reads,
# 65 is refused. Real profiles nest about a dozen levels (certificate extensions); BER allows any depth.
ENVELOPE_DEPTH = 64
ENVELOPE_SHAPES = {
    'ContentInfo': 'a SEQUENCE of contentType and content spanning the whole file',
    'ContentInfo.contentType': 'OBJECT IDENTIFIER id-signedData (1.2.840.113549.1.7.2)',
    'ContentInfo.content': '[0] EXPLICIT holding one SignedData',
    'SignedData': 'a SEQUENCE of version, digestAlgorithms, encapContentInfo, optional certificates [0], optional crls [1], signerInfos',
    'SignedData.version': 'an INTEGER of one content octet, a CMSVersion from 0 to 5',
    'SignedData.digestAlgorithms': 'a SET of SEQUENCEs, each beginning with an OBJECT IDENTIFIER',
    'SignedData.encapContentInfo': 'a SEQUENCE of eContentType and eContent',
    'EncapsulatedContentInfo.eContentType': 'OBJECT IDENTIFIER id-data (1.2.840.113549.1.7.1)',
    'EncapsulatedContentInfo.eContent': '[0] EXPLICIT holding one primitive OCTET STRING',
    'SignedData.certificates': '[0] IMPLICIT SET of X.509 Certificates, each a SEQUENCE of exactly a SEQUENCE, a SEQUENCE and a BIT STRING',
    'SignedData.crls': '[1] IMPLICIT SET of X.509 CertificateLists, each a SEQUENCE of exactly a SEQUENCE, a SEQUENCE and a BIT STRING',
    'SignedData.signerInfos': 'a SET of SignerInfos, each a SEQUENCE beginning with an INTEGER version of one content octet, 0 to 5',
    'SignedData (after encapContentInfo)': 'optional certificates [0], optional crls [1], then signerInfos, then nothing',
}
DEFINITE_DER = 'definite-length DER'
WITHIN_PARENT = 'every element within its parent, no byte left over'
TYPE_RULE = "the encoding rule of the element's universal type"
PROFILE_SIZE = 'a profile of 1 byte to 256 KiB'
ENVELOPE_UNSUPPORTED = ('an indefinite length', 'a length in more octets than needed', 'a constructed string',
                        'a tag number in the high-tag-number form', 'a BOOLEAN other than 00 or FF',
                        f'nesting deeper than {ENVELOPE_DEPTH} elements')
ENVELOPE_MALFORMED = ('an element cut off at the end of its parent', 'an element that runs past its parent',
                      'bytes left over after the last element', 'an indefinite length on a primitive element',
                      'a reserved length octet')
ENVELOPE_TYPE_RULES = ('an end-of-contents marker outside an indefinite length',
                       'a primitive SEQUENCE or SET', 'a constructed element of a type that is always primitive',
                       'an INTEGER that is empty or has a redundant leading octet', 'an OBJECT IDENTIFIER that is not well formed',
                       'a BOOLEAN that is not one octet', 'a NULL with content', 'a BIT STRING that is not well formed')
ENVELOPE_SHAPE_FOUND = ('another tag', 'another object identifier', 'a missing element', 'more elements than declared',
                        'another version')
whole_plist.declare(fields=ENVELOPE_SHAPES, expected={*ENVELOPE_SHAPES.values(), DEFINITE_DER, WITHIN_PARENT, TYPE_RULE, PROFILE_SIZE},
                    found={*ENVELOPE_UNSUPPORTED, *ENVELOPE_MALFORMED, *ENVELOPE_TYPE_RULES, *ENVELOPE_SHAPE_FOUND})
_STRINGS = {3, 4, 12, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30}  # types BER allows constructed, DER does not
_ALWAYS_PRIMITIVE = {1, 2, 5, 6, 9, 10, 13}


class _Element:
    def __init__(self, at, byte, content, end):
        self.at, self.content, self.end = at, content, end
        self.cls, self.constructed, self.number = whole_plist.TAG_CLASSES[byte >> 6], bool(byte & 0x20), byte & 0x1f

    def tag(self):
        return (self.cls, self.number, self.constructed)

    def is_(self, number, constructed, cls='universal'):
        """This tag. For a string type, BER allows either form: the shape is the type, and the walk names a constructed
        string as a form this reader does not read."""
        if cls == 'universal' and number in _STRINGS:
            return (self.cls, self.number) == (cls, number)
        return (self.cls, self.number, self.constructed) == (cls, number, constructed)


def _refused(found, field, at, item=None, tag=None):
    if found in ENVELOPE_UNSUPPORTED:
        kind, expected = 'unsupported', DEFINITE_DER
    elif found in ENVELOPE_MALFORMED:
        kind, expected = 'malformed', WITHIN_PARENT
    elif found in ENVELOPE_TYPE_RULES:
        kind, expected = 'malformed', TYPE_RULE
    else:
        kind, expected = 'malformed', ENVELOPE_SHAPES[field]
    return whole_plist.Refused(f'profile envelope {kind}: {field}: {found}', part='profile envelope', kind=kind, field=field,
                               expected=expected, found=found, offset=at, item=item, tag=tag)


def _element(raw, at, end, field, item=None):
    """The header of the element at `at`, which must end by `end`."""
    if at + 2 > end:
        raise _refused('an element cut off at the end of its parent', field, at, item)
    byte, first = raw[at], raw[at + 1]
    cls, constructed = whole_plist.TAG_CLASSES[byte >> 6], bool(byte & 0x20)
    if byte & 0x1f == 0x1f:
        raise _refused('a tag number in the high-tag-number form', field, at, item, (cls, None, constructed))
    tag = (cls, byte & 0x1f, constructed)
    start = at + 2
    if first == 0x80:
        raise _refused('an indefinite length' if constructed else 'an indefinite length on a primitive element', field, at, item, tag)
    if first == 0xff:
        raise _refused('a reserved length octet', field, at, item, tag)
    if first & 0x80:
        count = first & 0x7f
        if start + count > end:
            raise _refused('an element cut off at the end of its parent', field, at, item, tag)
        length = int.from_bytes(raw[start:start + count], 'big')
        start += count
        if start + length > end:
            raise _refused('an element that runs past its parent', field, at, item, tag)
        if raw[at + 2] == 0 or length < 0x80:
            raise _refused('a length in more octets than needed', field, at, item, tag)
    else:
        length = first
        if start + length > end:
            raise _refused('an element that runs past its parent', field, at, item, tag)
    return _Element(at, byte, start, start + length)


def _each(raw, node, name):
    """The elements that exactly fill a constructed element, each read when it is asked for; `name(index)` gives
    (field, item) for each."""
    at, index = node.content, 0
    while at < node.end:
        field, item = name(index)
        child = _element(raw, at, node.end, field, item)
        yield child
        at, index = child.end, index + 1


def _children(raw, node, name):
    """The elements that exactly fill a constructed element, all headers read first."""
    return list(_each(raw, node, name))


def _walk(raw, node, field, item=None, depth=0):
    """Every element under `node` length-walked: within its parent, nothing left over, and the universal types' rules
    in ENVELOPE_TYPE_RULES where met; reserved or other universal tags are not refused."""
    if depth > ENVELOPE_DEPTH:
        raise _refused(f'nesting deeper than {ENVELOPE_DEPTH} elements', field, node.at, item, node.tag())
    if node.cls == 'universal':
        number, content = node.number, raw[node.content:node.end]
        rule = None
        if number == 0:
            rule = 'an end-of-contents marker outside an indefinite length'
        elif number in (16, 17) and not node.constructed:
            rule = 'a primitive SEQUENCE or SET'
        elif number in _ALWAYS_PRIMITIVE and node.constructed:
            rule = 'a constructed element of a type that is always primitive'
        elif number in _STRINGS and node.constructed:
            rule = 'a constructed string'
        elif number in (2, 10) and (not content or (len(content) > 1 and (content[0], content[1] >> 7) in ((0, 0), (0xff, 1)))):
            rule = 'an INTEGER that is empty or has a redundant leading octet'
        elif number in (6, 13) and (not content or content[-1] & 0x80
                                    or any(c == 0x80 and (i == 0 or not content[i - 1] & 0x80) for i, c in enumerate(content))):
            rule = 'an OBJECT IDENTIFIER that is not well formed'
        elif number == 1 and len(content) != 1:
            rule = 'a BOOLEAN that is not one octet'
        elif number == 1 and content[0] not in (0, 0xff):
            rule = 'a BOOLEAN other than 00 or FF'
        elif number == 5 and content:
            rule = 'a NULL with content'
        elif number == 3 and (not content or content[0] > 7 or (len(content) == 1 and content[0] != 0)):
            rule = 'a BIT STRING that is not well formed'
        if rule:
            raise _refused(rule, field, node.at, item, node.tag())
    if node.constructed:
        for child in _children(raw, node, lambda _: (field, item)):
            _walk(raw, child, field, item, depth + 1)


def _shape(condition, found, field, node, item=None):
    if not condition:
        raise _refused(found, field, node.at if node is not None else None, item, node.tag() if node is not None else None)


def _count(nodes, wanted, field, parent):
    """Exactly `wanted` elements: fewer is a missing element, more is more elements than declared."""
    if len(nodes) < wanted:
        raise _refused('a missing element', field, parent.end, tag=None)
    if len(nodes) > wanted:
        raise _refused('more elements than declared', field, nodes[wanted].at, tag=nodes[wanted].tag())


def _cms_version(raw, node, field, item=None):
    """A CMSVersion (RFC 5652): an INTEGER of exactly one content octet, 0 to 5; anything else is a wrong shape. Checked
    after the INTEGER's own well-formedness."""
    _walk(raw, node, field, item)
    _shape(node.end - node.content == 1 and raw[node.content] <= 5, 'another version', field, node, item)


def _signed_outer(raw, node, field, item):
    """An X.509 Certificate or CertificateList outer shape (RFC 5280): a SEQUENCE of exactly SEQUENCE, SEQUENCE, BIT STRING."""
    _shape(node.is_(16, True), 'another tag', field, node, item)
    parts = _children(raw, node, lambda _: (field, item))
    if len(parts) != 3:
        raise _refused('a missing element' if len(parts) < 3 else 'more elements than declared', field,
                       node.at if len(parts) < 3 else parts[3].at, item)
    for part, (number, constructed) in zip(parts, ((16, True), (16, True), (3, False))):
        _shape(part.is_(number, constructed), 'another tag', field, part, item)


def _reader(raw, parent, names, rest):
    """The next element of `parent` when asked for, and the refusal for a missing one; names[i] names the i-th field."""
    elements = _each(raw, parent, lambda i: (names[i] if i < len(names) else rest, None))

    def take(field):
        node = next(elements, None)
        if node is None:
            raise _refused('a missing element', field, parent.end)
        return node
    return take, lambda: next(elements, None)


def profile_envelope(raw):
    """(content, offset): the bytes of the one property list the envelope defines as its content, and where they start.

    The content extractor of the enforced list in the comment above; it checks the size of `raw` before it reads any
    element. Raises whole_plist.Refused (a ValueError) naming a real field, the shape or encoding expected, and what was
    found there; which of several defects is reported follows the rule stated there, not an order."""
    whole_plist.within_limit(raw, 'profile file', PROFILE_LIMIT, PROFILE_SIZE)
    top = _element(raw, 0, len(raw), 'ContentInfo')
    if top.end != len(raw):
        raise _refused('bytes left over after the last element', 'ContentInfo', top.end)
    _shape(top.is_(16, True), 'another tag', 'ContentInfo', top)
    take, extra = _reader(raw, top, ('ContentInfo.contentType', 'ContentInfo.content'), 'ContentInfo')
    kind = take('ContentInfo.contentType')
    _shape(kind.is_(6, False), 'another tag', 'ContentInfo.contentType', kind)
    _walk(raw, kind, 'ContentInfo.contentType')
    _shape(raw[kind.content:kind.end] == SIGNED_DATA_OID, 'another object identifier', 'ContentInfo.contentType', kind)
    wrapper = take('ContentInfo.content')
    _shape(wrapper.is_(0, True, 'context-specific'), 'another tag', 'ContentInfo.content', wrapper)
    more = extra()
    _shape(more is None, 'more elements than declared', 'ContentInfo', more)
    inner = _children(raw, wrapper, lambda _: ('ContentInfo.content', None))
    _count(inner, 1, 'ContentInfo.content', wrapper)
    signed = inner[0]
    _shape(signed.is_(16, True), 'another tag', 'SignedData', signed)
    names = ('SignedData.version', 'SignedData.digestAlgorithms', 'SignedData.encapContentInfo')
    take, extra = _reader(raw, signed, names, 'SignedData (after encapContentInfo)')
    version = take('SignedData.version')
    _shape(version.is_(2, False), 'another tag', 'SignedData.version', version)
    _cms_version(raw, version, 'SignedData.version')
    field = 'SignedData.digestAlgorithms'
    digests = take(field)
    _shape(digests.is_(17, True), 'another tag', field, digests)
    for number, algorithm in enumerate(_children(raw, digests, lambda i: (field, i + 1)), 1):
        _shape(algorithm.is_(16, True), 'another tag', field, algorithm, number)
        first = _children(raw, algorithm, lambda _: (field, number))
        _shape(bool(first), 'a missing element', field, algorithm, number)
        _shape(first[0].is_(6, False), 'another tag', field, first[0], number)
        _walk(raw, algorithm, field, number)
    field = 'SignedData.encapContentInfo'
    encap = take(field)
    _shape(encap.is_(16, True), 'another tag', field, encap)
    parts = _children(raw, encap, lambda i: (('EncapsulatedContentInfo.eContentType', 'EncapsulatedContentInfo.eContent')[i]
                                             if i < 2 else field, None))
    _count(parts, 2, field, encap)
    kind, wrapper = parts
    _shape(kind.is_(6, False), 'another tag', 'EncapsulatedContentInfo.eContentType', kind)
    _walk(raw, kind, 'EncapsulatedContentInfo.eContentType')
    _shape(raw[kind.content:kind.end] == DATA_OID, 'another object identifier', 'EncapsulatedContentInfo.eContentType', kind)
    field = 'EncapsulatedContentInfo.eContent'
    _shape(wrapper.is_(0, True, 'context-specific'), 'another tag', field, wrapper)
    octets = _children(raw, wrapper, lambda _: (field, None))
    _count(octets, 1, field, wrapper)
    content = octets[0]
    _shape(content.is_(4, False), 'another tag', field, content)
    if content.constructed:
        raise _refused('a constructed string', field, content.at, tag=content.tag())
    # After encapContentInfo: optional certificates [0], optional crls [1], then signerInfos, then nothing.
    node = extra()
    for tag_number, field in ((0, 'SignedData.certificates'), (1, 'SignedData.crls')):
        if node is not None and node.cls == 'context-specific' and node.number == tag_number:
            _shape(node.constructed, 'another tag', field, node)
            for number, item in enumerate(_children(raw, node, lambda i, field=field: (field, i + 1)), 1):
                _signed_outer(raw, item, field, number)
                _walk(raw, item, field, number)
            node = extra()
    field = 'SignedData.signerInfos'
    if node is None:
        raise _refused('a missing element', field, signed.end)
    _shape(node.is_(17, True), 'another tag', field, node)
    for number, signer in enumerate(_children(raw, node, lambda i: (field, i + 1)), 1):
        _shape(signer.is_(16, True), 'another tag', field, signer, number)
        first = _children(raw, signer, lambda _: (field, number))
        _shape(bool(first), 'a missing element', field, signer, number)
        _shape(first[0].is_(2, False), 'another tag', field, first[0], number)
        _cms_version(raw, first[0], field, number)
        _walk(raw, signer, field, number)
    more = extra()
    if more is not None:
        raise _refused('more elements than declared', 'SignedData (after encapContentInfo)', more.at, tag=more.tag())
    return raw[content.content:content.end], content.content


def profile_content(raw):
    """The bytes of the profile's one encapsulated property list (profile_envelope); no signature/authentication check."""
    return profile_envelope(raw)[0]


# --- The profile's property list and grants ---------------------------------------------------------------------------

NOT_A_DICTIONARY = 'another value under plist'
whole_plist.declare(expected={'a dictionary under plist'}, found={NOT_A_DICTIONARY, 'another value', 'other bytes'})

# The one typed check of exactly the fields the release tools read from a profile, applied once after the whole read
# (profile_plist), so that every consumer reads a value of its type or a named mismatch. Each may be absent: a missing
# field is refused by the rule that needs it. Entitlement values other than these four are classified by the record's
# entitlement selection (release/observations.select_entitlements), which counts a value of another type as an
# unexpected entitlement and never records it.
STRINGS, DATE = 'an array of strings, or absent', 'a date, or absent'
PROFILE_TYPES = {
    'UUID': ('a string, or absent', lambda v: isinstance(v, str)),
    'TeamIdentifier': (STRINGS, lambda v: isinstance(v, list) and all(isinstance(i, str) for i in v)),
    'ApplicationIdentifierPrefix': (STRINGS, lambda v: isinstance(v, list) and all(isinstance(i, str) for i in v)),
    'Platform': (STRINGS, lambda v: isinstance(v, list) and all(isinstance(i, str) for i in v)),
    'ProvisionedDevices': (STRINGS, lambda v: isinstance(v, list) and all(isinstance(i, str) for i in v)),
    'ProvisionsAllDevices': ('a boolean, or absent', lambda v: isinstance(v, bool)),
    'CreationDate': (DATE, lambda v: isinstance(v, datetime.datetime)),
    'ExpirationDate': (DATE, lambda v: isinstance(v, datetime.datetime)),
    'Entitlements': ('a dictionary, or absent', lambda v: isinstance(v, dict)),
}
ENTITLEMENT_TYPES = {
    'com.apple.application-identifier': ('a string, or absent', lambda v: isinstance(v, str)),
    'com.apple.developer.team-identifier': ('a string, or absent', lambda v: isinstance(v, str)),
    'get-task-allow': ('a boolean, or absent', lambda v: isinstance(v, bool)),
    'com.apple.security.get-task-allow': ('a boolean, or absent', lambda v: isinstance(v, bool)),
}
OTHER_TYPE = 'a value of another type'
whole_plist.declare(fields={*PROFILE_TYPES, *('Entitlements ' + k for k in ENTITLEMENT_TYPES)},
                    expected={e for e, _ in (*PROFILE_TYPES.values(), *ENTITLEMENT_TYPES.values())}, found={OTHER_TYPE})


def profile_types(profile):
    """Refuse (a mismatch: the property list was read whole) the first field the tools read that is not of its type."""
    fields = [(key, profile, key, PROFILE_TYPES[key]) for key in PROFILE_TYPES]
    entitlements = profile.get('Entitlements')
    if isinstance(entitlements, dict):
        fields += [('Entitlements ' + key, entitlements, key, ENTITLEMENT_TYPES[key]) for key in ENTITLEMENT_TYPES]
    for name, holder, key, (expected, typed) in fields:
        if key in holder and not typed(holder[key]):
            raise whole_plist.Refused(f'profile field {name} is not of its type', part='profile property list', kind='mismatch',
                                      field=name, expected=expected, found=OTHER_TYPE)


def profile_plist(raw):
    """The profile's encapsulated property list, a dictionary whose value is the whole document (whole_plist.load), with
    each field the tools read of its type (profile_types).

    Raises whole_plist.Refused (a ValueError) naming the part (file, envelope or property list), the field, the shape and
    what was found. Not CMS authentication."""
    content, offset = profile_envelope(raw)
    try:
        profile = whole_plist.load(content)
    except whole_plist.Refused as refused:
        raise refused.moved('profile property list', offset) from None
    if not isinstance(profile, dict):
        raise whole_plist.Refused('profile property list must be a dictionary', part='profile property list', kind='malformed',
                                  field='plist', expected='a dictionary under plist', found=NOT_A_DICTIONARY, offset=offset)
    profile_types(profile)
    return profile


# The consistency rules: (part, field, expected, found, message). The message keeps the words earlier callers matched.
GRANTS = {
    'digest': ('profile file', 'the file', 'the bytes of the selected digest', 'other bytes', 'provisioning profile bytes differ from selected digest'),
    'prefix': ('profile grants', 'ApplicationIdentifierPrefix', 'one string', 'another value', 'one profile AppIdentifierPrefix required'),
    'entitlements': ('profile grants', 'Entitlements', 'a dictionary', 'another value', 'profile entitlement grants absent'),
    'platform': ('profile grants', 'Platform, ProvisionsAllDevices and ProvisionedDevices',
                 'Platform exactly OSX, ProvisionsAllDevices true, no ProvisionedDevices', 'another value',
                 'macOS Developer ID distribution profile required'),
    'team': ('profile grants', 'TeamIdentifier and Entitlements com.apple.developer.team-identifier',
             'the publisher team, alone, in both', 'another value', 'profile team differs from publisher input'),
    'app_id': ('profile grants', 'Entitlements com.apple.application-identifier', 'the prefix, a dot and the publisher bundle identifier',
               'another value', 'profile does not grant the selected application identifier'),
    'debugging': ('profile grants', 'Entitlements get-task-allow', 'absent or false, under either name', 'another value',
                  'development profile grant refused'),
    'dates': ('profile grants', 'CreationDate and ExpirationDate', 'dates, created at or before now, expiring after now',
              'another value', 'profile not valid at preparation time'),
}
whole_plist.declare(fields={g[1] for g in GRANTS.values()}, expected={g[2] for g in GRANTS.values()},
                    found={g[3] for g in GRANTS.values()})


def grant(condition, rule):
    """Refuse with the named consistency rule: a mismatch (the profile was read whole), except the digest, which is
    checked before the profile is read and so says only that its bytes are not the selected digest's."""
    if not condition:
        part, field, expected, found, message = GRANTS[rule]
        raise whole_plist.Refused(message, part=part, kind='digest' if rule == 'digest' else 'mismatch', field=field,
                                  expected=expected, found=found)


def profile_size(path):
    """Refuse the profile at `path` by its size, from the file system, before the caller reads it for the reader (and, in
    prepare, before the transfer's own larger bound); profile_envelope checks the size of the bytes it is given again."""
    whole_plist.check_size(os.stat(path).st_size, 'profile file', PROFILE_LIMIT, PROFILE_SIZE)


def profile_consistency(raw, expected_sha256, selected, now=None):
    """Consistency only: exact bytes and encapsulated grants match the publisher input. Not CMS authentication.

    The grants are read by profile_plist: the encapsulated property list is read only when its value is the whole
    document, so no fact below comes from part of it. Every refusal is a whole_plist.Refused naming its rule."""
    grant(isinstance(expected_sha256, str) and re.fullmatch('[0-9a-f]{64}', expected_sha256) is not None
          and sha(raw) == expected_sha256, 'digest')
    profile = profile_plist(raw)  # its size, envelope, property list and field types, each refused by name
    team, identifier = selected['developer_id_team_identifier'], selected['production_bundle_identifier']
    prefixes = profile.get('ApplicationIdentifierPrefix')
    grant(isinstance(prefixes, list) and len(prefixes) == 1 and isinstance(prefixes[0], str), 'prefix')
    entitlements = profile.get('Entitlements')
    grant(isinstance(entitlements, dict), 'entitlements')
    grant(profile.get('Platform') == ['OSX'] and profile.get('ProvisionsAllDevices') is True
          and not profile.get('ProvisionedDevices'), 'platform')
    grant(profile.get('TeamIdentifier') == [team] and entitlements.get('com.apple.developer.team-identifier') == team, 'team')
    grant(entitlements.get('com.apple.application-identifier') == prefixes[0] + '.' + identifier, 'app_id')
    grant(not entitlements.get('get-task-allow') and not entitlements.get('com.apple.security.get-task-allow'), 'debugging')
    creation, expiry = profile.get('CreationDate'), profile.get('ExpirationDate')
    checked = now or datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None, microsecond=0)
    grant(isinstance(creation, datetime.datetime) and isinstance(expiry, datetime.datetime) and creation <= checked < expiry, 'dates')
    return {'sha256': expected_sha256, 'size': len(raw), 'uuid': profile.get('UUID'),
            'application_identifier': entitlements['com.apple.application-identifier'],
            'expiration': expiry.isoformat() + 'Z', 'validity_checked_at': checked.isoformat() + 'Z',
            'destination': 'Contents/embedded.provisionprofile',
            'standing': 'structural CMS content and metadata consistency only; signature/Apple authentication is a separate intake; placement unverified until build'}


def prepare(source_root, vendor, expected_manifest, pin, revision, output, *,
            test_identifier=None, publisher_input=None, publisher_sha256=None, upstream_notices=None,
            provisioning_profile=None, provisioning_profile_sha256=None, cargo_build_input=None,
            not_for_public_release=False):
    cargo_contract = cargo_build_input_contract(cargo_build_input) if cargo_build_input is not None else None
    source_root, vendor, output = map(inventory.anchored, (source_root, vendor, output))
    require(not os.path.lexists(source_root / '.git'), 'source must be a disposable frozen export, not a checkout')
    require('*' not in str(vendor), 'glob characters in vendor source refused')
    require(identity(source_root) not in ancestors(vendor) and identity(vendor) not in ancestors(source_root),
            'vendor and source export must be disjoint')
    require(output.parent.is_dir(), 'existing physical output parent required')
    require(re.fullmatch('[0-9a-f]{40}', revision) is not None, 'exact source revision required')
    require(re.fullmatch('[0-9a-f]{64}', expected_manifest) is not None, 'expected vendor manifest required')
    require(bool(test_identifier) != bool(publisher_input), 'select exactly one explicit test namespace or private publisher input')
    inspected = {}
    def read(path):
        path = inventory.anchored(path)
        raw, digest, _ = files.transfer(path, retain=True)
        inspected[str(path)] = digest
        return raw
    publisher_ref = None
    if test_identifier:
        require(publisher_sha256 is None, 'test mode cannot select publisher trust')
        require(re.fullmatch(r'dev\.chirality\.app-v4\.package-test\.[A-Za-z0-9-]+', test_identifier) is not None,
                'explicit isolated package-test identifier required')
        identifier = test_identifier
        mode = 'unqualified-input-test'
        product = 'Chirality App v4 (package input test ' + test_identifier.rsplit('.', 1)[1] + ')'
    else:
        require(isinstance(publisher_sha256, str) and re.fullmatch('[0-9a-f]{64}', publisher_sha256), 'exact selected publisher input digest required')
        publisher_path = inventory.anchored(publisher_input)
        require(not ancestors(publisher_path.parent).intersection({identity(source_root), identity(vendor)}),
                'private publisher input must be outside source and vendor')
        raw = read(publisher_path)
        require(sha(raw) == publisher_sha256, 'publisher input bytes differ from selected digest')
        selected = parse(raw)
        schema = parse(read(source_root / 'app/src-tauri/schemas/publisher-build-selection.s1.schema.json'))
        Draft202012Validator(schema).validate(selected)
        identifier = selected['production_bundle_identifier']
        require(not identifier.startswith('dev.chirality.app-v4.package-test.'), 'test namespace cannot select production inputs')
        mode, product = 'selected-production-inputs', 'Chirality'
        publisher_ref = {'path': str(inventory.anchored(publisher_input)), 'sha256': publisher_sha256}
    profile_ref = None
    if provisioning_profile is not None or provisioning_profile_sha256 is not None:
        require(publisher_ref is not None, 'test mode cannot embed a production provisioning profile')
        profile_path = inventory.anchored(provisioning_profile)
        require(not ancestors(profile_path.parent).intersection({identity(source_root), identity(vendor)}),
                'private provisioning profile must be outside source and vendor')
        profile_size(profile_path)  # by name, before the transfer reads it for the reader (and before its own, larger, bound)
        profile_raw = read(profile_path)
        profile_ref = profile_consistency(profile_raw, provisioning_profile_sha256, selected)
        profile_ref['path'] = str(profile_path)
    app = source_root / 'app'
    # Bundle-visible copies of the frontend IBM Plex notices; refuse a stale index for this source.
    font_notice = load_module('production_font_notice', 'app/packaging/font_notice/check.py')
    fonts = font_notice.check(source_root)
    # The source-selected mappings (base configuration resources, overlays, SQLite and font notices), shared with the
    # notice coverage account; a platform or alternate configuration or any other copy route refuses there.
    bundle = load_module('production_bundle_resources', 'app/packaging/production_inputs/bundle_resources.py')
    resources = bundle.selected(app, [l['path'] for l in fonts['licenses']], load=lambda path: parse(read(path)))
    plan_pairs = bundle.pairs(resources)
    supplement_sources = set()
    supplement = None
    if upstream_notices is not None:
        receipts = load_module('production_notice_receipts', 'app/packaging/notices/receipts.py')
        upstream_notices = inventory.anchored(upstream_notices)
        supplement = receipts.check_stage(upstream_notices, source_root)
        for name in supplement['files']:
            src = str(upstream_notices / name)
            require('*' not in src and src not in resources, 'supplement source conflict')
            resources[src] = bundle.SUPPLEMENT_DESTINATION + name
            supplement_sources.add(src)
            plan_pairs.append((bundle.SUPPLEMENT_SOURCE + name, bundle.SUPPLEMENT_DESTINATION + name))
    resource_inputs = {}
    for src, dst in resources.items():
        require('*' not in src and '*' not in dst, 'glob resource mapping refused')
        require(not Path(src).is_absolute() or src in supplement_sources, 'source resource mapping must be repository-relative')
        files.relative(dst.rstrip('/'))
        path = inventory.anchored(os.path.abspath(app / 'src-tauri' / src))
        require(path.is_relative_to(source_root) or src in supplement_sources, 'source resource mapping escapes selected source')
        if path.is_dir():
            tree = inventory.scan(path)
            require(all(e['kind'] in ('file', 'dir') for e in tree['entries']), 'resource tree contains link/special input')
            require_nonempty(tree)
            resource_inputs[src] = {'destination': dst, 'tree': tree}
        else:
            raw = read(path)
            resource_inputs[src] = {'destination': dst, 'sha256': sha(raw), 'size': len(raw)}
    destinations = [(info['destination'].rstrip('/'), 'tree' in info) for info in resource_inputs.values()]
    require(len({p for p, _ in destinations}) == len(destinations), 'duplicate resource destination')
    for parent, directory in destinations:
        if directory:
            require(not any(p != parent and p.startswith(parent + '/') for p, _ in destinations), 'overlapping resource destinations')
    supplier = inventory.scan(vendor)
    require(supplier['manifest_sha256'] == expected_manifest and supplier['files'] > 0, 'vendor manifest mismatch')
    require(all(e['kind'] in ('file', 'dir') for e in supplier['entries']), 'vendor links/special files refused')
    require_nonempty(supplier)
    metadata = parse(read(vendor / 'codex-package.json'))
    inventory.validate_package_layout(metadata, supplier, pin)
    require('codex' not in {p for p, _ in destinations}
            and not any(p.startswith('codex/') for p, _ in destinations), 'vendor destination collision')
    by_destination = {info['destination']: src for src, info in resource_inputs.items() if 'tree' not in info}
    def reference_file(reference):
        files.ref(reference)
        destination = 'distribution-reference/' + reference['path']
        require(destination in by_destination, 'supplier reference is not explicitly mapped')
        raw = read(app / 'src-tauri' / by_destination[destination])
        require(sha(raw) == reference['sha256'], 'mapped supplier reference digest mismatch')
        return parse(raw)
    selection_key = by_destination['distribution-reference/build-selection.s2.json']
    selection = parse(read(app / 'src-tauri' / selection_key))
    require(selection['format'] == 'build-selection.s2', 'unknown supplier selection')
    expected = reference_file(selection['expected'])
    attestation = reference_file(selection['attestation'])
    require(attestation['expected_reference'] == selection['expected'], 'supplier attestation subject mismatch')
    require(expected['pin'] == pin and expected['inventory']['manifest_sha256'] == expected_manifest,
            'selected vendor does not match mapped supplier reference')
    observed_entries = [{'path': '.', 'kind': 'dir', 'mode': int(supplier['root_mode'], 8)}]
    for entry in supplier['entries']:
        item = {'path': entry['path'], 'kind': entry['kind'], 'mode': int(entry['mode'], 8)}
        if entry['kind'] == 'file': item.update(size=entry['size'], sha256=entry['sha256'])
        observed_entries.append(item)
    require(sorted(observed_entries, key=lambda e: e['path']) == sorted(expected['inventory']['entries'], key=lambda e: e['path']),
            'vendor full tree differs from mapped supplier reference')
    resources[str(vendor) + '/'] = bundle.VENDOR_DESTINATION
    plan_pairs.append((bundle.VENDOR_SOURCE, bundle.VENDOR_DESTINATION))
    # Read relevant recipe inputs without selecting a new supplier pin or changing source.
    for relative in ('app/package-lock.json', 'app/src-tauri/Cargo.lock', 'app/src-tauri/Cargo.toml', 'app/src-tauri/tauri.conf.json'):
        read(source_root / relative)
    if cargo_contract is not None:
        manifest = tomllib.loads(read(source_root / 'app/src-tauri/Cargo.toml').decode())
        require(manifest.get('profile', {}).get('release', {}).get('opt-level', 3) == 3,
                'Cargo build input requires release opt-level 3')
    # One account of every shipped component's notice; a public-release plan refuses while any is open.
    coverage = load_module('production_notice_coverage', 'app/packaging/notices/coverage.py')
    notice_coverage = coverage.check(source_root)
    # The account counts only for the supplier it describes: the selected pin and vendor manifest.
    describes_vendor = (notice_coverage['supplier_pin'] == pin
                        and notice_coverage['supplier_distribution']['manifest_sha256'] == expected_manifest)
    gaps = [f"{o['name']} {o['version']}" for o in notice_coverage['open']]
    # Every mapping this plan gives the bundler, including the vendor tree and any supplement, must be named in the
    # account by its exact source and destination.
    unnamed = coverage.unaccounted(notice_coverage['mappings'], plan_pairs)
    gaps += [f'bundle mapping not named in the notice coverage account: {src} -> {dst}' for src, dst in unnamed]
    if not describes_vendor:
        gaps.insert(0, f"the account describes supplier {notice_coverage['supplier_pin']}, not the selected vendor")
    require(not_for_public_release is True or not_for_public_release is False, 'not_for_public_release must be given as true or false')
    if gaps and publisher_ref is not None and not not_for_public_release:
        raise NoticeCoverageIncomplete([o['name'] for o in notice_coverage['open']], len(gaps) - len(notice_coverage['open']),
                                       'notice coverage is incomplete; a production plan needs --not-for-public-release: ' + ', '.join(gaps))
    release_standing = ('not for public release: notice coverage is incomplete' if gaps
                        else 'not for public release: package input test' if publisher_ref is None
                        else 'notice coverage complete')
    if not_for_public_release:
        release_standing = 'not for public release (named by the caller)' + ('; notice coverage is incomplete' if gaps else '')
    tool_paths = [__file__, inventory.__file__, files.__file__, whole_plist.__file__, font_notice.__file__, bundle.__file__, coverage.__file__]
    if supplement is not None: tool_paths.append(receipts.__file__)
    tool_hashes = {str(inventory.anchored(p)): sha(read(Path(p))) for p in tool_paths}
    no_overlap(output.parent, [source_root, vendor, *{Path(p).parent for p in inspected}])
    config = {'productName': product, 'version': '4.0.0', 'identifier': identifier,
              'bundle': {'active': True, 'targets': ['app'], 'resources': resources,
                         'macOS': {'minimumSystemVersion': '15.0', 'signingIdentity': None}}}
    if profile_ref:
        # Tauri copies macOS.files relative to Contents/; placement is verified only by a later build inventory.
        config['bundle']['macOS']['files'] = {bundle.PROFILE_FILE: profile_ref['path']}
    # The configuration the bundler will use is the base merged with this plan: its copy routes must be exactly the
    # plan's resources, the base icon and, in a production plan, the validated profile.
    effective = bundle.merge_patch({'bundle': bundle.base_bundle(app, load=lambda path: parse(read(path)))}, config)['bundle']
    bundle.check_routes(effective, profile=profile_ref['path'] if profile_ref else None)
    require(effective['resources'] == resources, 'effective bundle resources differ from the plan')
    env = {'CARGO_NET_OFFLINE': 'true', 'NPM_CONFIG_OFFLINE': 'true', 'CARGO_BUILD_JOBS': '2', 'MACOSX_DEPLOYMENT_TARGET': '15.0',
           'NPM_CONFIG_UPDATE_NOTIFIER': 'false'}
    if publisher_ref:
        env.update(CHIRALITY_PUBLISHER_SELECTION='production-v1', CHIRALITY_PUBLISHER_INPUT_FILE=publisher_ref['path'],
                   CHIRALITY_PUBLISHER_INPUT_SHA256=publisher_ref['sha256'])
    required_env = {'PATH': 'prepared toolchain PATH', 'HOME': 'explicit build HOME, not a Codex home',
                    'LANG': 'explicit locale', 'TMPDIR': 'private build temporary directory',
                    'CARGO_HOME': 'prepared offline cache view', 'CARGO_TARGET_DIR': 'new isolated absolute target outside inputs',
                    'CODEX_HOME': 'fresh private scratch Codex home', 'NPM_CONFIG_CACHE': 'prepared offline npm cache',
                    'NPM_CONFIG_USERCONFIG': 'empty task-owned config', 'NPM_CONFIG_GLOBALCONFIG': 'empty task-owned config',
                    'RUSTUP_HOME': 'task-owned rustup home inside the run folder', 'NPM_CONFIG_PREFIX': 'task-owned npm prefix inside the run folder',
                    'NPM_CONFIG_LOGS_DIR': 'task-owned npm logs folder inside the run folder'}
    recipe = {'working_directory': str(app), 'inherit_environment': False,
              'environment_allowlist': sorted(set(env) | set(required_env)), 'required_environment': required_env, 'environment': env,
              'unset_environment': ['APPLE_SIGNING_IDENTITY', 'APPLE_CERTIFICATE', 'APPLE_CERTIFICATE_PASSWORD', 'APPLE_ID',
                                    'APPLE_PASSWORD', 'APPLE_TEAM_ID', 'APPLE_API_KEY', 'APPLE_API_ISSUER', 'APPLE_API_KEY_PATH',
                                    'TAURI_CONFIG', 'TAURI_SIGNING_PRIVATE_KEY', 'TAURI_SIGNING_PRIVATE_KEY_PASSWORD', 'RUSTFLAGS', 'CARGO_ENCODED_RUSTFLAGS']
                                    + ([] if publisher_ref else ['CHIRALITY_PUBLISHER_SELECTION', 'CHIRALITY_PUBLISHER_INPUT_FILE', 'CHIRALITY_PUBLISHER_INPUT_SHA256']),
              'argv': ['node', 'node_modules/@tauri-apps/cli/tauri.js', 'build', '--no-sign', '--bundles', 'app',
                       '--features', 'custom-protocol,distribution-successor', '--config', str(output / 'tauri.package-inputs.conf.json'), '--', '--offline', '--locked'],
              'required_host_controls': ['prepared offline caches and isolated target', 'fresh scratch CODEX_HOME',
                                         'current owner-selected host admission; no shared-script changes', 'jobs2',
                                         'coordinate one fresh candidate; never mutate retained native artifacts'],
              'signing': 'disabled; no signing or build executed', 'profile': 'release', 'mode': mode}
    if cargo_contract is not None:
        recipe['cargo_build_input'] = cargo_contract
    # Ensure all inspected files/trees are still the same before publishing inputs.
    for name, digest in inspected.items():
        require(files.transfer(name)[1] == digest, 'input file changed during preparation')
    require(inventory.compare(inventory.scan(vendor), supplier)['equal'], 'vendor changed during preparation')
    for info in resource_inputs.values():
        if 'tree' in info:
            require(inventory.compare(inventory.scan(info['tree']['root']), info['tree'])['equal'], 'resource tree changed during preparation')
    if supplement is not None:
        require(receipts.check_stage(upstream_notices, source_root) == supplement, 'supplement changed during preparation')
    require(font_notice.check(source_root) == fonts, 'font notice changed during preparation')
    require(coverage.check(source_root) == notice_coverage, 'notice coverage changed during preparation')
    output.mkdir(exist_ok=False, mode=0o700)
    write_new(output / 'INCOMPLETE.txt', b'Not usable until PLAN_COMPLETE.json validates and this marker is absent.\n')
    try:
        account = {'tool_sha256': tool_hashes, 'jsonschema_version': importlib.metadata.version('jsonschema'),
                   'source_revision': revision, 'source_root': str(source_root), 'source_claim': 'caller-selected disposable export; hashes below, not Git export authentication',
                   'mode': mode, 'resource_inputs': resource_inputs, 'supplier': supplier, 'inspected_files': inspected,
                   'publisher_input': publisher_ref, 'limits': ['input preparation only; no App build or resource mapper executed',
                   'stock cache selection does not qualify supplier pin', 'no signed package, S4 installed observation, OS qualification or release',
                   'notice coverage is as notice_coverage states; open components are named there'],
                   'release_standing': release_standing, 'not_for_public_release': not_for_public_release,
                   'notice_coverage': {'account': 'app/packaging/notices/coverage.json', 'sha256': notice_coverage['sha256'],
                                       'complete': not gaps, 'gaps': len(gaps),
                                       'counts': notice_coverage['counts'],
                                       'supplier_pin': notice_coverage['supplier_pin'], 'describes_selected_vendor': describes_vendor,
                                       'open': [f"{o['name']} {o['version']} ({o['standing']})" for o in notice_coverage['open']]}}
        if supplement is not None: account['upstream_notice_supplement'] = supplement
        if profile_ref: account['provisioning_profile'] = profile_ref
        completed = {}
        for name, value in [('tauri.package-inputs.conf.json', config), ('build-recipe.json', recipe), ('input-inventory.json', account)]:
            raw = (json.dumps(value, indent=2) + '\n').encode()
            write_new(output / name, raw)
            completed[name] = sha(raw)
        write_new(output / 'PLAN_COMPLETE.json', (json.dumps({'files': completed}, indent=2) + '\n').encode())
        fd = os.open(output, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            os.fsync(fd)
            (output / 'INCOMPLETE.txt').unlink()
            os.fsync(fd)
        finally:
            os.close(fd)
    except Exception:
        # The initial marker remains even if killed between writes; no incomplete
        # output is made runnable by the presence of only config and recipe.
        raise
    # Do not print production identifier/team or private input bytes.
    return {'mode': mode, 'output': str(output), 'files': check_plan(output)['files'],
            'build_executed': False, 'signing_executed': False, 'package_complete': False, 'release_standing': release_standing,
            'not_for_public_release': not_for_public_release}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ('source-root', 'vendor', 'expected-manifest', 'pin', 'revision', 'output'):
        parser.add_argument('--' + key, required=True)
    parser.add_argument('--test-identifier')
    parser.add_argument('--publisher-input')
    parser.add_argument('--publisher-sha256')
    parser.add_argument('--upstream-notices', help='Explicit completed upstream notice supplement; default omitted')
    parser.add_argument('--provisioning-profile', help='Private Developer ID profile embedded at Contents/; production only')
    parser.add_argument('--provisioning-profile-sha256')
    parser.add_argument('--not-for-public-release', action='store_true',
                        help='Name the plan as not for public release; required for a production plan while notice coverage is open')
    parser.add_argument('--cargo-build-input', choices=[CARGO_BUILD_PRESET],
                        help='Explicit platform/toolchain-scoped host and shipped release strip override; default omitted')
    args = vars(parser.parse_args())
    try:
        print(json.dumps(prepare(**args), indent=2))
    except Exception as error:
        # Source/identity values belong to private output evidence, not diagnostics.
        # A file reader's refusal carries only fixed text and integers (whole_plist.Refused.detail), so it is printed.
        refusal = {'refusal': error.detail(), 'reason': whole_plist.describe(error.detail())} if isinstance(error, whole_plist.Refused) else {}
        print(json.dumps({'preparation_complete': False, 'error_type': type(error).__name__, **refusal}))
        raise SystemExit(2)
