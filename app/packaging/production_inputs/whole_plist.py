"""The one reader of a property-list FILE whose value is the whole document, the event reading it shares, and the
refusal every file reader of the release tools raises.

Refusals. A `Refused` carries only fixed text from closed lists this code defines, and integers: the part of the file
(`PARTS`), the kind of refusal (`KINDS`), the field, the shape expected, what was found, and where (a byte offset into
the file, an item number in a set, a tag's class and number). It never carries a byte or a value read from the file.
There are three kinds, kept apart:
- 'unsupported': a form the governing standard allows that this reader does not read (for a property list, XML 1.0
  and the property-list DTD; for the profile's envelope, BER). Nothing was read, so the identity comparison is not
  established: this is neither a mismatch nor a malformed file, and it never counts as agreement.
- 'malformed': a form the governing standard does not allow, or a field not of its declared shape.
- 'mismatch': the file was read whole, and a value is not what the release requires.
The rule where one input could be read either way: a form the standard allows (including one DER forbids but BER
allows, or one another property-list reader might accept) is 'unsupported'; a form the standard does not allow is
'malformed'. The first problem met in reading order is the one reported.

`load` reads an XML property list twice, by two readers that do not share their reading of the structure, and returns
the value only when the two agree and the first has accounted for every byte of the document:

1. A structural reading of the document's own bytes from the XML parser's events (`events`), independent of plistlib.
   The admitted form, and nothing else:
   - the first bytes are the XML declaration, version 1.0, encoding UTF-8 (in any case) or not given, no standalone
     declaration; optionally the property-list document type (name `plist`, public identifier
     `-//Apple//DTD PLIST 1.0//EN`, system identifier `http://www.apple.com/DTDs/PropertyList-1.0.dtd`, no internal
     subset). They are compared by what they declare, not by how they are spelled;
   - one `plist` root, whose only attribute may be `version="1.0"`, holding exactly one value;
   - only the property-list elements (`dict`, `array`, `key`, `string`, `integer`, `real`, `true`, `false`, `date`,
     `data`) inside it, with no attribute, nested at most MAX_DEPTH arrays and dictionaries deep;
   - inside `plist`, `dict` and `array`, and before and after the root, nothing but whitespace bytes (space, tab,
     carriage return, line feed) between elements: no other text, no character reference, no CDATA section;
   - inside `dict`, `key` and a value strictly alternating, no key twice and no key without its value;
   - no comment and no processing instruction anywhere; no entity declaration, no undefined or external entity,
     nothing fetched; no byte after the root element other than whitespace;
   - the leaf values: `string` and `key` hold text (character and entity references and CDATA sections in them are
     the characters XML says they denote); `integer` is `0|-?[1-9][0-9]*` (no `+`, no `-0`, no leading zero,
     no hexadecimal); `real` is a decimal number with an optional exponent that converts to a finite double, and to zero
     only when its digits are all zero; `date` is `YYYY-MM-DDTHH:MM:SSZ` naming a real date and time; `data` is padded
     base64 whose unused bits are zero, with whitespace anywhere in it (any wrapping); `true` and `false` are empty
     (`<true/>` or `<true></true>`).
   Valid XML or a valid property list that is refused as 'unsupported': a byte-order mark, UTF-16 or another
   encoding, no XML declaration, a standalone declaration, another document type or an internal subset, a comment, a
   processing instruction, an entity declaration, whitespace inside an `integer`, `real` or `date`, a character or
   entity reference or a CDATA section inside an `integer`, `real`, `date` or `data`, an integer with `+`, `-0`, leading zeros, hexadecimal or more than 64 characters, a real
   that overflows or underflows a double, a date with a fraction or an offset, base64 with non-zero unused bits,
   nesting deeper than MAX_DEPTH, and a binary property list.
2. plistlib's reading of the same bytes, with a dictionary that refuses a key given twice.
3. The two values must be equal, with the same types (a boolean is not an integer) and the same dictionary key order.

The normalizations, exhaustively: the document header compared by its declaration and document type; the root's
`version` attribute absent or `1.0`; whitespace bytes between elements; line ends in text as the XML parser reports them to both readers (CR LF and a lone CR become LF: XML
1.0 section 2.11); character and entity references and CDATA sections in a `string` or `key` read as the characters
they denote, and an empty element read the same as its start and end tags (XML 1.0); whitespace removed from inside `data` before decoding; and
one conversion: a decimal `real` is read as the nearest double, so two spellings can give the same value. Each other
admitted leaf spelling has exactly one value and each value exactly one spelling. Whitespace inside a `string` or
`key` is part of the value and is kept.

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
    'unsupported': 'an encoding or form this reader does not read; the identity comparison is not established',
    'malformed': 'malformed: not well formed, or a field not of its declared shape',
    'mismatch': 'read whole, and not what the release requires',
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
BASE64 = re.compile(r'(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?')

U, M = 'unsupported', 'malformed'
SPELLING = 'a spelling this reader does not read'
# What was found -> (kind, shape expected). The kind follows the rule in the module docstring.
PLIST_REASONS = {
    'a binary property list': (U, 'an XML property list'),
    'no XML declaration as the first bytes (a byte order mark, another encoding, or none)': (U, 'an XML declaration as the first bytes'),
    'an XML declaration other than version 1.0 in UTF-8 without standalone': (U, 'version 1.0, encoding UTF-8 or none, no standalone'),
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
    'a reference or CDATA section in a leaf that is not text': (U, 'the characters as written in integer, real, date and data'),
    'the standard parser does not read the document': (U, 'a document the standard parser reads'),
    'the standard parser reads another value': (U, 'the same value from both readers'),
}
# For SPELLING, the shape expected is the leaf's admitted form.
LEAF_FORMS = {
    'integer': 'a decimal integer 0|-?[1-9][0-9]*: no +, no -0, no leading zero, no hexadecimal',
    'real': 'a decimal number with an optional exponent, converting to a finite double, and to zero only from zero digits',
    'date': 'YYYY-MM-DDTHH:MM:SSZ naming a real date and time',
    'data': 'padded base64 with unused bits zero, whitespace allowed anywhere',
}
PLACES = ('document header', 'document', 'after the root element', 'plist', 'dict', 'array', *sorted(LEAVES))
declare(fields=PLACES, expected={e for _, e in PLIST_REASONS.values()} | set(LEAF_FORMS.values()),
        found=set(PLIST_REASONS) | {SPELLING})


class NotWhole(Refused):
    """The document is not one property list whose value is the whole document, in the admitted form; `why` names what
    was found, `field` where (the document header, the document, after the root element, or the property-list element
    it was found in), and `offset` the byte where it begins, when known."""

    def __init__(self, why, field='document', offset=None):
        kind, expected = PLIST_REASONS[why] if why != SPELLING else (U, LEAF_FORMS[field])
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
        raise NotWhole('no XML declaration as the first bytes (a byte order mark, another encoding, or none)', 'document header', 0)
    for n in range(root):
        offset, kind, values, _ = found[n]
        if kind == 'xml declaration':
            version, encoding, standalone = values
            if n != 0 or version != '1.0' or (encoding is not None and encoding.lower() != 'utf-8') or standalone != -1:
                raise NotWhole('an XML declaration other than version 1.0 in UTF-8 without standalone', 'document header', offset)
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
    def spelling():
        return NotWhole(SPELLING, name, offset)
    if name in ('string', 'key'):
        return text
    if name in ('true', 'false'):
        if text:
            raise NotWhole('content inside true or false', name, offset)
        return name == 'true'
    if name == 'integer':
        if not INTEGER.fullmatch(text) or len(text) > 64:
            raise spelling()
        return int(text)
    if name == 'real':
        match = REAL.fullmatch(text)
        if not match:
            raise spelling()
        value = float(text)
        if math.isinf(value) or (value == 0 and re.search('[1-9]', match.group(1))):
            raise spelling()  # overflows or underflows a double: the value would not be what is written
        return value
    if name == 'date':
        match = DATE.fullmatch(text)
        if not match:
            raise spelling()
        try:
            return datetime.datetime(*map(int, match.groups()))
        except ValueError:
            raise spelling() from None
    # data: base64, padded, with whitespace allowed anywhere (wrapping at any width), and unused bits zero, so that the
    # text is the one base64 spelling of its bytes.
    compact = re.sub(r'[ \t\r\n]', '', text)
    if not BASE64.fullmatch(compact):
        raise spelling()
    value = base64.b64decode(compact, validate=True)
    if base64.b64encode(value).decode() != compact:
        raise spelling()
    return value


def structure_value(raw):
    """The value of an XML property list built from its own events, without plistlib; raises NotWhole on anything the
    admitted form does not account for."""
    if raw.startswith(b'bplist'):
        raise NotWhole('a binary property list', 'document', 0)
    if not raw.startswith(b'<?xml'):
        raise NotWhole('no XML declaration as the first bytes (a byte order mark, another encoding, or none)', 'document header', 0)
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
                    raise NotWhole('a reference or CDATA section in a leaf that is not text', top[0], offset)
            top[1].append(values[0])
        elif kind in ('cdata start', 'cdata end') and top is not None and top[0] in ('string', 'key'):
            pass  # a CDATA section's text is reported as text; it is a spelling of the string's text
        elif kind in ('cdata start', 'cdata end') and top is not None and top[0] in ('true', 'false'):
            raise NotWhole('content inside true or false', top[0], offset)
        elif kind in ('cdata start', 'cdata end') and top is not None and top[0] in LEAVES:
            raise NotWhole('a reference or CDATA section in a leaf that is not text', top[0], offset)
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
    """The value of one XML property list file, returned only when that value is the whole document; else NotWhole."""
    value = structure_value(raw)
    try:
        standard = plistlib.loads(raw, fmt=plistlib.FMT_XML, dict_type=_UniqueDict)
    except (ValueError, ExpatError, AttributeError, TypeError, IndexError, OverflowError, RecursionError):
        raise NotWhole('the standard parser does not read the document', 'document') from None
    if not _same(value, standard):
        raise NotWhole('the standard parser reads another value', 'document')
    return value
