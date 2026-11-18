"""The one reader of a property-list FILE whose value is the whole document, the event reading it shares, and the
refusal every file reader of the release tools raises.

Refusals. A `Refused` carries only fixed text from closed lists this code defines, and integers: the part of the file
(`PARTS`), the kind of refusal (`KINDS`), the field, the shape expected, what was found, and where (a byte offset into
the file, an item number in a set, a tag's class and number). It never carries a byte or a value read from the file.
There are three kinds, kept apart, and each says only what the reader knows:
- 'unsupported' (shown as "not established"): the reader met a named form outside the subset it reads, at a named
  field, and did not read the file. It asserts nothing about whether the file is otherwise valid. The identity
  comparison is not established: this is never a mismatch, never malformed, and never agreement.
- 'malformed': asserted only where the reader is certain within its subset: not well-formed XML in the admitted
  header, a second value, stray text, a key twice, an empty file, an envelope element past its parent or bytes left
  over, a field of the envelope not of its declared shape, and the like.
- 'mismatch': the file was read whole, and a value the tools read is not of its type or not what the release
  requires.
Where several rules fail at once, one is reported: the first met in reading order. Others may exist.

`load` reads an XML property list twice, by two readers that do not share their reading of the structure, and returns
the value only when the two agree and the first has accounted for every byte of the document:

1. A structural reading of the document's own bytes from the XML parser's events (`events`), independent of plistlib.
   The admitted form, and nothing else:
   - the document is not empty (an empty file is malformed);
   - the first bytes are the XML declaration, version 1.0, encoding UTF-8 (in any case) or not given, no standalone
     declaration; optionally the property-list document type (name `plist`, public identifier
     `-//Apple//DTD PLIST 1.0//EN`, system identifier `http://www.apple.com/DTDs/PropertyList-1.0.dtd`, no internal
     subset). They are compared by what they declare, not by how they are spelled;
   - one `plist` root, whose only attribute may be `version="1.0"` (written with no reference), holding exactly one
     value;
   - only the property-list elements (`dict`, `array`, `key`, `string`, `integer`, `real`, `true`, `false`, `date`,
     `data`) inside it, with no attribute, nested at most MAX_DEPTH arrays and dictionaries deep;
   - inside `plist`, `dict` and `array`, and before and after the root, nothing but whitespace bytes (space, tab,
     carriage return, line feed) between elements: no other text, no character reference, no CDATA section;
   - inside `dict`, `key` and a value strictly alternating, no key twice and no key without its value;
   - no comment and no processing instruction anywhere; no entity declaration, no undefined or external entity,
     nothing fetched; no byte after the root element other than whitespace;
   - the leaf values: `string` and `key` hold text (character and entity references and CDATA sections in them are
     the characters XML says they denote); `integer` is `0|-?[1-9][0-9]*` of at most 64 characters (no `+`, no
     `-0`, no leading zero, no hexadecimal); `real` is a decimal number with an optional exponent that converts to a finite double, and to zero
     only when its digits are all zero; `date` is `YYYY-MM-DDTHH:MM:SSZ` naming a real date and time; `data` is padded
     base64 whose unused bits are zero, with whitespace anywhere in it (any wrapping); `true` and `false` are empty
     (`<true/>` or `<true></true>`). `integer`, `real`, `date` and `data` hold their characters as written, with no
     character or entity reference and no CDATA section.
   Forms outside this subset, refused as not established (whether or not another reader would accept them): a
   byte-order mark or anything else before the XML declaration, a declared encoding other than UTF-8, another XML
   version, a standalone declaration, another document type or an internal subset, a comment, a processing
   instruction, an entity declaration, a reference in the root's attribute, a leaf value outside its admitted form
   (each named with its type and that form), nesting deeper than MAX_DEPTH, a binary property list, a document the
   XML parser or the standard parser does not read, and a disagreement between the two readers.
2. plistlib's reading of the same bytes, with a dictionary that refuses a key given twice.
3. The two values must be equal, with the same types (a boolean is not an integer) and the same dictionary key order.

The normalizations, exhaustively:
- the document header compared by what its declaration and document type declare, not by how they are spelled (either
  quote, whitespace inside them, the encoding name in any case);
- the root's `version` attribute absent or `1.0`, in either quote, with whitespace around `=`;
- whitespace inside a tag (before `>` or `/>`, and in an end tag before `>`), and an empty element read the same as
  its start and end tags (XML 1.0);
- whitespace bytes between elements and after the root element;
- line ends in text as the XML parser reports them to both readers (CR LF and a lone CR become LF: XML 1.0 section
  2.11);
- character and entity references and CDATA sections in a `string` or `key` read as the characters they denote;
- space, tab, CR and LF removed from inside `data` before decoding (any wrapping);
- one conversion: a decimal `real` is read as the nearest double, so two spellings can give the same value.
Each other admitted leaf spelling has exactly one value and each value exactly one spelling. Whitespace inside a
`string` or `key` is part of the value and is kept.

What this establishes is that the value returned is the whole document; it does not authenticate the document or say
who wrote it.

`xml_structure` is the reading the entitlement command-output reader (release/observations.load_xml_plist) compares;
it is built on the same `events`, and its behaviour, exceptions and messages included, is as it was before `load`.
"""
import base64
import datetime
import math
import plistlib
import re
from xml.parsers import expat
from xml.parsers.expat import ExpatError

# --- Refusals: fixed text from closed lists, and integers ------------------------------------------------------------

PARTS = ('property list', 'Info.plist', 'profile envelope', 'profile property list', 'profile grants', 'profile file')
KINDS = {
    'unsupported': ('not established: a form outside the subset this reader reads; the file was not read, nothing is asserted '
                    'about whether it is valid, and the identity comparison is not established'),
    'malformed': 'malformed: certain within the subset this reader reads (not well formed, or a field not of its declared shape)',
    'mismatch': 'read whole, and a value the tools read is not of its type or not what the release requires',
}
TAG_CLASSES = ('universal', 'application', 'context-specific', 'private')
# Every field, expected shape and finding a refusal may name; each module declares its own with `declare`.
FIELDS, EXPECTED, FOUND = set(), set(), set()


def declare(fields=(), expected=(), found=()):
    FIELDS.update(fields); EXPECTED.update(expected); FOUND.update(found)


def vocabulary():
    """Every text a refusal's detail may hold."""
    return set(PARTS) | set(KINDS) | set(KINDS.values()) | set(TAG_CLASSES) | FIELDS | EXPECTED | FOUND


class Refused(ValueError):
    """A refusal by a file reader; `detail()` is what may be shown and returned (fixed text and integers only)."""

    def __init__(self, message, *, part, kind, field, expected, found, offset=None, item=None, tag=None):
        if not (part in PARTS and kind in KINDS and field in FIELDS and expected in EXPECTED and found in FOUND):
            raise AssertionError('a refusal text outside the closed lists')
        if tag is not None and not (tag[0] in TAG_CLASSES and (tag[1] is None or isinstance(tag[1], int))
                                    and isinstance(tag[2], bool)):
            raise AssertionError('a tag outside the closed form')
        super().__init__(message)
        self.part, self.kind, self.field, self.expected, self.found = part, kind, field, expected, found
        self.offset, self.item, self.tag = offset, item, tag

    def detail(self):
        value = {'part': self.part, 'kind': self.kind, 'field': self.field, 'expected': self.expected, 'found': self.found}
        if self.item is not None:
            value['item'] = self.item
        if self.tag is not None:
            value['tag'] = {'class': self.tag[0], 'constructed': self.tag[2], **({'number': self.tag[1]} if self.tag[1] is not None else {})}
        if self.offset is not None:
            value['offset'] = self.offset
        return value

    def moved(self, part, by=0):
        """The same refusal named as part of a larger file, its offset moved by the bytes before this document."""
        return Refused(str(self), part=part, kind=self.kind, field=self.field, expected=self.expected, found=self.found,
                       offset=None if self.offset is None else self.offset + by, item=self.item, tag=self.tag)


def describe(detail):
    """One line for a person, built only from a refusal's detail: fixed text and integers."""
    text = f"{detail['part']}: {KINDS[detail['kind']]}. Field {detail['field']}"
    if 'item' in detail:
        text += f" (item {detail['item']})"
    text += f": expected {detail['expected']}; found {detail['found']}"
    if 'tag' in detail:
        tag = detail['tag']
        text += f" (tag {tag['class']}{' ' + str(tag['number']) if 'number' in tag else ''}, {'constructed' if tag['constructed'] else 'primitive'})"
    if 'offset' in detail:
        text += f" at byte {detail['offset']}"
    return text + '.'


# --- The property list ----------------------------------------------------------------------------------------------

# Elements whose content is other elements: text directly inside them only separates elements.
CONTAINERS = {'plist', 'dict', 'array'}
LEAVES = {'key', 'string', 'integer', 'real', 'date', 'data', 'true', 'false'}
XML_WHITESPACE = b' \t\r\n'
PUBLIC_ID = '-//Apple//DTD PLIST 1.0//EN'
SYSTEM_ID = 'http://www.apple.com/DTDs/PropertyList-1.0.dtd'
# Real Info.plist files and profiles nest a few levels (a profile: plist, dict, Entitlements, an array). Thirty-two is
# far above that and far below where a recursive reading or comparison could fail.
MAX_DEPTH = 32
INTEGER = re.compile(r'0|-?[1-9][0-9]*')
REAL = re.compile(r'([+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+))(?:[eE][+-]?[0-9]+)?')
DATE = re.compile(r'([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2})Z')
# The XML declaration's encoding, read before the parser decodes the document (XML 1.0 section 2.8 and 4.3.3).
DECLARED_ENCODING = re.compile(rb'<\?xml[ \t\r\n]+version[ \t\r\n]*=[ \t\r\n]*(["\'])[^"\']*\1'
                               rb'(?:[ \t\r\n]+encoding[ \t\r\n]*=[ \t\r\n]*(["\'])([^"\']*)\2)?')
BASE64 = re.compile(r'(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?')

U, M = 'unsupported', 'malformed'
# What was found -> (kind, shape expected). The kind follows the rule in the module docstring.
PLIST_REASONS = {
    'a binary property list': (U, 'an XML property list'),
    'an empty document': (M, 'one XML property list'),
    'content that does not begin with an XML declaration': (U, 'an XML declaration as the first bytes'),
    'a declared encoding other than UTF-8': (U, 'encoding UTF-8, or no encoding declared'),
    'an XML declaration other than version 1.0, or with a standalone declaration': (U, 'version 1.0, no standalone declaration'),
    'a reference in the root version attribute': (U, 'the root version attribute written as 1.0, with no reference'),
    'a document type other than the property-list one': (U, 'the property-list document type, or none'),
    'a document type with an internal subset': (U, 'the property-list document type, or none'),
    'an entity declaration': (U, 'no entity declaration'),
    'an undefined or external entity reference': (M, 'only the predefined entities and character references'),
    'a comment': (U, 'no comment'),
    'a processing instruction': (U, 'no processing instruction'),
    'not well-formed XML': (M, 'well-formed XML'),
    'bytes after the document element': (M, 'nothing after the root element but whitespace'),
    'no root element': (M, 'one plist root element'),
    'a root element other than plist': (M, 'one plist root element'),
    'an attribute other than the root version': (M, 'no attribute but version="1.0" on the root'),
    'an element that is not a property-list element': (M, 'only property-list elements'),
    'an element inside a leaf value': (M, 'text only inside a leaf value'),
    'content inside true or false': (M, 'an empty true or false element'),
    'a second value under plist': (M, 'exactly one value under plist'),
    'no value under plist': (M, 'exactly one value under plist'),
    'a key with no value': (M, 'key and value alternating in a dictionary'),
    'a value with no key': (M, 'key and value alternating in a dictionary'),
    'a key outside a dictionary': (M, 'keys only inside a dictionary'),
    'a key twice in one dictionary': (M, 'each key once in a dictionary'),
    'text outside a value': (M, 'only whitespace bytes between elements'),
    f'nesting deeper than {MAX_DEPTH} arrays and dictionaries': (U, f'at most {MAX_DEPTH} nested arrays and dictionaries'),
    'the XML parser does not read the document': (U, 'a document the XML parser reads'),
    'the standard parser does not read the document': (U, 'a document the standard parser reads'),
    'the standard parser reads another value': (U, 'the same value from both readers'),
}
# A leaf value outside its admitted form: not established, with the leaf's admitted form in full as the shape expected,
# and what was found named by the rule it fails.
AS_WRITTEN = 'as plain characters, with no character or entity reference and no CDATA section'
LEAF_FORMS = {
    'integer': ('an integer: 0, or an optional minus sign, a digit 1 to 9 and further digits; at most 64 characters; '
                'no +, no -0, no leading zero, no hexadecimal; ' + AS_WRITTEN),
    'real': ('a real: an optional sign, digits with an optional decimal point and digits (or a decimal point and digits), '
             'an optional exponent (e or E, an optional sign, digits); converting to a finite double, and to zero only '
             'from all-zero digits; ' + AS_WRITTEN),
    'date': 'a date: YYYY-MM-DDTHH:MM:SSZ naming a real date and time; ' + AS_WRITTEN,
    'data': ('data: base64 from A-Z, a-z, 0-9, + and /, in groups of four, the last padded with = to four, unused bits '
             'zero; space, tab, CR and LF allowed anywhere; ' + AS_WRITTEN),
}
LEAF_FOUND = {
    'integer': ('an integer outside the admitted grammar', 'an integer longer than 64 characters'),
    'real': ('a real outside the admitted grammar', 'a real that converts to an infinity',
             'a real that converts to zero from non-zero digits'),
    'date': ('a date outside the admitted grammar', 'a date naming no real date or time'),
    'data': ('a character outside base64 and whitespace', 'base64 padding outside the admitted form',
             'base64 with unused bits not zero'),
}
REFERENCE_IN_LEAF = 'a reference or CDATA section in a leaf that is not text'
PLACES = ('document header', 'document', 'after the root element', 'plist', 'dict', 'array', *sorted(LEAVES))
declare(fields=PLACES, expected={e for _, e in PLIST_REASONS.values()} | set(LEAF_FORMS.values()),
        found=set(PLIST_REASONS) | {f for found in LEAF_FOUND.values() for f in found} | {REFERENCE_IN_LEAF})

# --- The size of a file, refused by name before it is parsed ----------------------------------------------------------

FILE_FOUND = {'an empty file': M, 'a file larger than the size limit': U}
declare(fields={'the file'}, found=set(FILE_FOUND))


def within_limit(raw, part, limit, expected):
    """Refuse an empty file (malformed) or one larger than `limit` bytes (not established) by name, before parsing."""
    found = 'an empty file' if not raw else 'a file larger than the size limit' if len(raw) > limit else None
    if found:
        raise Refused(f'{part}: {found}', part=part, kind=FILE_FOUND[found], field='the file', expected=expected, found=found)


class NotWhole(Refused):
    """The document is not one property list whose value is the whole document, in the admitted form; `why` names what
    was found, `field` where (the document header, the document, after the root element, or the property-list element
    it was found in), and `offset` the byte where it begins, when known."""

    def __init__(self, why, field='document', offset=None):
        kind, expected = PLIST_REASONS[why] if why in PLIST_REASONS else (U, LEAF_FORMS[field])
        super().__init__('the property list is not the whole document: ' + why, part='property list', kind=kind, field=field,
                         expected=expected, found=why, offset=offset)
        self.why = why


def events(raw, *, everything=False):
    """[(byte offset, kind, values, directly inside a container)] for an XML document, read with expat.

    The parser reports every event with the byte offset where it starts, so the events partition the document's
    bytes: an event's bytes run to the next event's offset. With `everything`, the default handler reports, as
    'other', with its text, every character no other handler reports (whitespace in the header and after the root),
    and the end of a document type is its own event, so that no construct passes without an event. The document
    type's event is reported at the offset where its declaration ends, so the bytes of the declaration fall in the
    span of the event before it; that is why the header is read by its events' values, not by byte spans. Entity
    declarations raise NotWhole('an entity declaration'); skipped (undefined) entity references and external entities
    raise NotWhole('an undefined or external entity reference'); nothing is fetched. An ExpatError carries the byte
    where it was found as `byte_index`."""
    parser = expat.ParserCreate()
    parser.SetParamEntityParsing(expat.XML_PARAM_ENTITY_PARSING_NEVER)
    found, stack = [], []

    def record(kind, effect=None):
        def handler(*values):
            found.append((parser.CurrentByteIndex, kind, values, bool(stack) and stack[-1] in CONTAINERS))
            if effect:
                effect(*values)
        return handler

    def declared(*_):
        raise NotWhole('an entity declaration', 'document header', parser.CurrentByteIndex)

    def undefined(*_):
        raise NotWhole('an undefined or external entity reference', 'document', parser.CurrentByteIndex)
    parser.XmlDeclHandler = record('xml declaration')
    parser.StartDoctypeDeclHandler = record('document type')
    parser.StartElementHandler = record('start', lambda name, _: stack.append(name))
    parser.EndElementHandler = record('end', lambda _: stack.pop())
    parser.CharacterDataHandler = record('text')
    parser.CommentHandler = record('comment')
    parser.ProcessingInstructionHandler = record('processing instruction')
    parser.StartCdataSectionHandler, parser.EndCdataSectionHandler = record('cdata start'), record('cdata end')
    parser.EntityDeclHandler = parser.UnparsedEntityDeclHandler = parser.NotationDeclHandler = declared
    parser.SkippedEntityHandler = parser.ExternalEntityRefHandler = undefined
    if everything:
        parser.EndDoctypeDeclHandler = record('document type end')
        parser.DefaultHandlerExpand = record('other')
    try:
        parser.Parse(raw, True)
    except ExpatError as error:
        error.byte_index = parser.ErrorByteIndex
        raise
    return found


def span(raw, found, n):
    """The bytes of event n as written: from its offset to the next event's offset (or the end)."""
    return raw[found[n][0]:found[n + 1][0] if n + 1 < len(found) else len(raw)]


def xml_structure(raw):
    """(header, body): what an XML property list document is, read without plistlib and without discarding anything.

    Two normalizations are made, and no others:
    - Document header. Everything before the root element is reduced to its XML declaration (version, encoding,
      standalone) and its document type (name, system and public identifier, whether an internal subset is present).
      Any other event there (a comment, a processing instruction) is kept in `header` as an event.
    - Whitespace between elements. A run of bytes that is only space, tab, carriage return or line feed, directly
      inside `plist`, `dict` or `array`, is left out, and so is such whitespace after the root element.
    `body` is every other byte of the root element exactly as written: every element, attribute, repeated entry,
    piece of text (in a value or between elements), comment, processing instruction and CDATA section, with each
    character and entity reference as spelled. Entity declarations, skipped (undefined) entity references and external
    entities raise ValueError('an entity is declared, skipped or external'); nothing is fetched."""
    try:
        found = events(raw)
    except NotWhole:
        raise ValueError('an entity is declared, skipped or external') from None
    root = next(n for n, event in enumerate(found) if event[1] == 'start')
    header = [(kind, values) for _, kind, values, _ in found[:root]]
    body = []
    for n in range(root, len(found)):
        _, kind, _, in_container = found[n]
        piece = span(raw, found, n)
        if not (kind == 'text' and in_container and not piece.strip(XML_WHITESPACE)):
            body.append(piece)
    return header, b''.join(body).rstrip(XML_WHITESPACE)


def _blank(text):
    """Text that is only XML whitespace (space, tab, carriage return, line feed), as the parser reports it."""
    return not text.strip(' \t\r\n')


def _header(raw, found, root):
    if not found or found[0][1] != 'xml declaration':
        raise NotWhole('content that does not begin with an XML declaration', 'document header', 0)
    for n in range(root):
        offset, kind, values, _ = found[n]
        if kind == 'xml declaration':
            version, encoding, standalone = values
            if encoding is not None and encoding.lower() != 'utf-8':
                raise NotWhole('a declared encoding other than UTF-8', 'document header', offset)
            if n != 0 or version != '1.0' or standalone != -1:
                raise NotWhole('an XML declaration other than version 1.0, or with a standalone declaration', 'document header', offset)
        elif kind == 'document type':
            name, system, public, internal = values
            if (name, system, public) != ('plist', SYSTEM_ID, PUBLIC_ID):
                raise NotWhole('a document type other than the property-list one', 'document header', offset)
            if internal:
                raise NotWhole('a document type with an internal subset', 'document header', offset)
        elif kind == 'document type end' or (kind == 'other' and _blank(values[0])):
            pass
        elif kind in ('comment', 'processing instruction'):
            raise NotWhole('a ' + kind, 'document header', offset)
        else:
            raise NotWhole('text outside a value', 'document header', offset)


def _leaf(name, text, offset):
    """The value of a leaf element from its text (entity and character references already resolved by the parser)."""
    def outside(found):
        return NotWhole(found, name, offset)
    if name in ('string', 'key'):
        return text
    if name in ('true', 'false'):
        if text:
            raise NotWhole('content inside true or false', name, offset)
        return name == 'true'
    if name == 'integer':
        if not INTEGER.fullmatch(text):
            raise outside('an integer outside the admitted grammar')
        if len(text) > 64:
            raise outside('an integer longer than 64 characters')
        return int(text)
    if name == 'real':
        match = REAL.fullmatch(text)
        if not match:
            raise outside('a real outside the admitted grammar')
        value = float(text)
        if math.isinf(value):
            raise outside('a real that converts to an infinity')
        if value == 0 and re.search('[1-9]', match.group(1)):
            raise outside('a real that converts to zero from non-zero digits')
        return value
    if name == 'date':
        match = DATE.fullmatch(text)
        if not match:
            raise outside('a date outside the admitted grammar')
        try:
            return datetime.datetime(*map(int, match.groups()))
        except ValueError:
            raise outside('a date naming no real date or time') from None
    # data: base64, padded, with whitespace allowed anywhere (wrapping at any width), and unused bits zero, so that the
    # text is the one base64 spelling of its bytes.
    compact = re.sub(r'[ \t\r\n]', '', text)
    if not re.fullmatch(r'[A-Za-z0-9+/=]*', compact):
        raise outside('a character outside base64 and whitespace')
    if not BASE64.fullmatch(compact):
        raise outside('base64 padding outside the admitted form')
    value = base64.b64decode(compact, validate=True)
    if base64.b64encode(value).decode() != compact:
        raise outside('base64 with unused bits not zero')
    return value


def structure_value(raw):
    """The value of an XML property list built from its own events, without plistlib; raises NotWhole on anything the
    admitted form does not account for."""
    if not raw:
        raise NotWhole('an empty document', 'document', 0)
    if raw.startswith(b'bplist'):
        raise NotWhole('a binary property list', 'document', 0)
    if not raw.startswith(b'<?xml'):
        raise NotWhole('content that does not begin with an XML declaration', 'document header', 0)
    declared = DECLARED_ENCODING.match(raw)
    if declared and declared.group(3) and declared.group(3).lower() != b'utf-8':
        raise NotWhole('a declared encoding other than UTF-8', 'document header', 0)  # before the parser decodes anything
    try:
        found = events(raw, everything=True)
    except ExpatError as error:
        if error.code == expat.errors.codes[expat.errors.XML_ERROR_JUNK_AFTER_DOC_ELEMENT]:
            raise NotWhole('bytes after the document element', 'after the root element', error.byte_index) from None
        raise NotWhole('not well-formed XML', 'document', error.byte_index) from None
    starts = [n for n, event in enumerate(found) if event[1] == 'start']
    if not starts:
        raise NotWhole('no root element', 'document')
    root = starts[0]
    _header(raw, found, root)
    # Stack frames: [element name, collected value or text pieces, pending key, keys seen, start offset].
    stack, result, closed, depth = [], [], False, 0
    for n in range(root, len(found)):
        offset, kind, values, in_container = found[n]
        top = stack[-1] if stack else None
        here = top[0] if top else ('after the root element' if closed else 'document')
        if kind == 'start':
            name, attributes = values
            if top is None:
                if name != 'plist':
                    raise NotWhole('a root element other than plist', 'document', offset)
                if set(attributes) - {'version'} or attributes.get('version', '1.0') != '1.0':
                    raise NotWhole('an attribute other than the root version', 'plist', offset)
                if b'&' in span(raw, found, n):  # the start tag as written: a reference can only be in an attribute value
                    raise NotWhole('a reference in the root version attribute', 'plist', offset)
            else:
                if top[0] in ('true', 'false'):
                    raise NotWhole('content inside true or false', top[0], offset)
                if top[0] in LEAVES:
                    raise NotWhole('an element inside a leaf value', top[0], offset)
                if name not in LEAVES and name not in ('dict', 'array'):
                    raise NotWhole('an element that is not a property-list element', top[0], offset)
                if attributes:
                    raise NotWhole('an attribute other than the root version', name, offset)
                if top[0] == 'plist' and top[1]:
                    raise NotWhole('a second value under plist', 'plist', offset)
                if top[0] == 'dict':
                    if name == 'key' and top[2] is not None:
                        raise NotWhole('a key with no value', 'dict', offset)
                    if name != 'key' and top[2] is None:
                        raise NotWhole('a value with no key', 'dict', offset)
                elif name == 'key':
                    raise NotWhole('a key outside a dictionary', top[0], offset)
                if name in ('dict', 'array'):
                    depth += 1
                    if depth > MAX_DEPTH:
                        raise NotWhole(f'nesting deeper than {MAX_DEPTH} arrays and dictionaries', name, offset)
            stack.append([name, [] if name != 'dict' else {}, None, set(), offset])
        elif kind == 'end':
            name, value, pending, _, start = stack.pop()
            if name == 'plist':
                if len(value) != 1:
                    raise NotWhole('no value under plist', 'plist', start)
                result, closed = value, True
                continue
            if name in ('dict', 'array'):
                depth -= 1
            if name == 'dict':
                if pending is not None:
                    raise NotWhole('a key with no value', 'dict', start)
            elif name in LEAVES:
                value = _leaf(name, ''.join(value), start)
            parent = stack[-1]
            if name == 'key':
                if value in parent[3]:
                    raise NotWhole('a key twice in one dictionary', 'dict', start)
                parent[3].add(value)
                parent[2] = value
            elif parent[0] == 'dict':
                parent[1][parent[2]] = value
                parent[2] = None
            else:
                parent[1].append(value)
        elif kind == 'text' and top is not None and top[0] in ('true', 'false'):
            raise NotWhole('content inside true or false', top[0], offset)
        elif kind == 'text' and top is not None and top[0] in LEAVES:
            if top[0] not in ('string', 'key'):
                # integer, real, date, data: the characters as written (line ends as XML reads them), no reference
                written = span(raw, found, n).replace(b'\r\n', b'\n').replace(b'\r', b'\n')
                if written != values[0].encode():
                    raise NotWhole(REFERENCE_IN_LEAF, top[0], offset)
            top[1].append(values[0])
        elif kind in ('cdata start', 'cdata end') and top is not None and top[0] in ('string', 'key'):
            pass  # a CDATA section's text is reported as text; it is a spelling of the string's text
        elif kind in ('cdata start', 'cdata end') and top is not None and top[0] in ('true', 'false'):
            raise NotWhole('content inside true or false', top[0], offset)
        elif kind in ('cdata start', 'cdata end') and top is not None and top[0] in LEAVES:
            raise NotWhole(REFERENCE_IN_LEAF, top[0], offset)
        elif kind == 'other' and top is None and closed and _blank(values[0]):
            pass  # whitespace after the root element
        elif kind == 'text' and in_container and _blank(values[0]) and not span(raw, found, n).strip(XML_WHITESPACE):
            pass  # whitespace between elements, written as whitespace bytes (not a character reference)
        elif kind in ('comment', 'processing instruction'):
            raise NotWhole('a ' + kind, here, offset)
        else:
            raise NotWhole('text outside a value', here, offset)
    if not closed or stack:
        raise NotWhole('not well-formed XML', 'document')
    return result[0]


class _UniqueDict(dict):
    def __setitem__(self, key, value):
        if key in self:
            raise ValueError('a key appears twice')
        super().__setitem__(key, value)


def _same(a, b):
    """Equal values with equal types (a dictionary of any class is a dictionary), in the same key order. The structural
    reading bounds the nesting at MAX_DEPTH before this is called, so the recursion here is bounded."""
    kind = lambda v: dict if isinstance(v, dict) else type(v)
    if kind(a) is not kind(b):
        return False
    if isinstance(a, dict):
        return list(a) == list(b) and all(_same(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(_same(x, y) for x, y in zip(a, b))
    return a == b


def load(raw):
    """The value of one XML property list file, returned only when that value is the whole document; else NotWhole.

    No exception from either parser leaves this function untyped: anything either raises that is not already a named
    refusal is the named refusal that the parser does not read the document (not established)."""
    try:
        value = structure_value(raw)
    except Refused:
        raise
    except Exception:  # an exception of the XML parser no rule above names (an encoding it cannot decode, and the like)
        raise NotWhole('the XML parser does not read the document', 'document') from None
    try:
        standard = plistlib.loads(raw, fmt=plistlib.FMT_XML, dict_type=_UniqueDict)
    except Exception:
        raise NotWhole('the standard parser does not read the document', 'document') from None
    if not _same(value, standard):
        raise NotWhole('the standard parser reads another value', 'document')
    return value
