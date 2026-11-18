"""The one reader of a property-list FILE whose value is the whole document, and the event reading it shares.

`load` reads an XML property list twice, by two readers that do not share their reading of the structure, and returns
the value only when the two agree and the first has accounted for every byte of the document:

1. A structural reading of the document's own bytes from the XML parser's events (`events`), independent of plistlib.
   It requires the property-list grammar exactly and builds the value itself:
   - the document header is the XML declaration (version 1.0; encoding UTF-8, in any case, or not given; no standalone
     declaration) and, optionally, the property-list document type (name `plist`, public identifier
     `-//Apple//DTD PLIST 1.0//EN`, system identifier `http://www.apple.com/DTDs/PropertyList-1.0.dtd`, no internal
     subset); they are compared by what they declare, not by how they are spelled;
   - one `plist` root, whose only attribute may be `version="1.0"`, holding exactly one value;
   - only the property-list elements (`dict`, `array`, `key`, `string`, `integer`, `real`, `true`, `false`, `date`,
     `data`) inside it, with no attribute;
   - inside `plist`, `dict` and `array`, and before and after the root, nothing but whitespace bytes (space, tab,
     carriage return, line feed) between elements: no other text, no character reference, no CDATA section;
   - inside `dict`, `key` and a value strictly alternating, no key twice and no key without its value;
   - no comment and no processing instruction anywhere (no genuine property-list file we know of carries one);
   - no entity declaration, no undefined or external entity, nothing fetched; no byte after the root element other
     than whitespace;
   - each leaf value in a spelling of its declared form: `string` and `key` hold text only (entity, character
     references and CDATA in them are part of the text, as XML defines them); `integer` is `[+-]?[0-9]+` or
     `0x` followed by hexadecimal digits; `real` is a decimal number with an optional exponent; `date` is
     `YYYY-MM-DDTHH:MM:SSZ`; `data` is padded base64 with whitespace allowed anywhere in it (any wrapping width);
     `true` and `false` are empty (`<true/>` or `<true></true>`).
2. plistlib's reading of the same bytes, with a dictionary that refuses a key given twice.
3. The two values must be equal, with the same types (a boolean is not an integer) and the same dictionary key order.

The normalizations allowed, and no others: the document header compared by its declaration and document type, as
above; whitespace bytes between elements; line ends in text as the XML parser reports them to both readers (carriage
return and line feed, or a lone carriage return, become a line feed: XML 1.0 section 2.11). Whitespace inside a
`string` or `key` is part of the value and is kept.

A binary property list is refused: the files read with this (the App's Info.plist, the provisioning profile's
encapsulated content) are read as XML only. What this establishes is that the value returned is the whole document; it
does not authenticate the document or say who wrote it.

`xml_structure` is the reading the entitlement command-output reader (release/observations.load_xml_plist) compares;
it is built on the same `events`, and its behaviour is unchanged by `load`.
"""
import base64
import binascii
import datetime
import plistlib
import re
from xml.parsers import expat
from xml.parsers.expat import ExpatError

# Elements whose content is other elements: text directly inside them only separates elements.
CONTAINERS = {'plist', 'dict', 'array'}
LEAVES = {'key', 'string', 'integer', 'real', 'date', 'data', 'true', 'false'}
VALUES = (LEAVES - {'key'}) | {'dict', 'array'}
XML_WHITESPACE = b' \t\r\n'
PUBLIC_ID = '-//Apple//DTD PLIST 1.0//EN'
SYSTEM_ID = 'http://www.apple.com/DTDs/PropertyList-1.0.dtd'
INTEGER = re.compile(r'[+-]?[0-9]+|0[xX][0-9a-fA-F]+')
REAL = re.compile(r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?')
DATE = re.compile(r'([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2})Z')
BASE64 = re.compile(r'(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?')


class NotWhole(ValueError):
    """The document is not one property list whose value is the whole document; `why` names what was left over."""

    def __init__(self, why):
        super().__init__('the property list is not the whole document: ' + why)
        self.why = why


def _refuse(*_):
    raise NotWhole('an entity declaration, an undefined entity or an external entity')


def events(raw, *, everything=False):
    """[(byte offset, kind, values, directly inside a container)] for an XML document, read with expat.

    The parser reports every event with the byte offset where it starts, so the events partition the document's
    bytes: an event's bytes run to the next event's offset. With `everything`, the default handler reports, as
    'other', with its text, every character no other handler reports (whitespace in the header and after the root),
    and the end of a document type is its own event, so that no construct passes without an event. The document
    type's event is reported at the offset where its declaration ends, so the bytes of the declaration fall in the
    span of the event before it; that is why the header is read by its events' values, not by byte spans. Entity declarations, skipped (undefined) entity references
    and external entities raise; nothing is fetched."""
    parser = expat.ParserCreate()
    parser.SetParamEntityParsing(expat.XML_PARAM_ENTITY_PARSING_NEVER)
    found, stack = [], []

    def record(kind, effect=None):
        def handler(*values):
            found.append((parser.CurrentByteIndex, kind, values, bool(stack) and stack[-1] in CONTAINERS))
            if effect:
                effect(*values)
        return handler
    parser.XmlDeclHandler = record('xml declaration')
    parser.StartDoctypeDeclHandler = record('document type')
    parser.StartElementHandler = record('start', lambda name, _: stack.append(name))
    parser.EndElementHandler = record('end', lambda _: stack.pop())
    parser.CharacterDataHandler = record('text')
    parser.CommentHandler = record('comment')
    parser.ProcessingInstructionHandler = record('processing instruction')
    parser.StartCdataSectionHandler, parser.EndCdataSectionHandler = record('cdata start'), record('cdata end')
    parser.EntityDeclHandler = parser.UnparsedEntityDeclHandler = parser.NotationDeclHandler = _refuse
    parser.SkippedEntityHandler = parser.ExternalEntityRefHandler = _refuse
    if everything:
        parser.EndDoctypeDeclHandler = record('document type end')
        parser.DefaultHandlerExpand = record('other')
    parser.Parse(raw, True)
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
    entities raise; nothing is fetched."""
    found = events(raw)
    root = next(n for n, event in enumerate(found) if event[1] == 'start')
    header = [(kind, values) for _, kind, values, _ in found[:root]]
    body = []
    for n in range(root, len(found)):
        _, kind, _, in_container = found[n]
        piece = span(raw, found, n)
        if not (kind == 'text' and in_container and not piece.strip(XML_WHITESPACE)):
            body.append(piece)
    return header, b''.join(body).rstrip(XML_WHITESPACE)


def _header(raw, found, root):
    for n in range(root):
        _, kind, values, _ = found[n]
        if kind == 'xml declaration':
            version, encoding, standalone = values
            if n != 0 or version != '1.0' or (encoding is not None and encoding.lower() != 'utf-8') or standalone != -1:
                raise NotWhole('a document header other than the XML declaration and the property-list document type')
        elif kind == 'document type':
            name, system, public, internal = values
            if (name, system, public) != ('plist', SYSTEM_ID, PUBLIC_ID):
                raise NotWhole('a document header other than the XML declaration and the property-list document type')
            if internal:
                raise NotWhole('a document type with an internal subset')
        elif kind == 'document type end':
            pass
        elif kind == 'other' and _blank(values[0]):
            pass
        else:
            raise NotWhole(_named(kind))
    if not found or found[0][1] != 'xml declaration':
        raise NotWhole('a document header other than the XML declaration and the property-list document type')


def _blank(text):
    """Text that is only XML whitespace (space, tab, carriage return, line feed), as the parser reports it."""
    return not text.strip(' \t\r\n')


def _named(kind):
    return {'comment': 'a comment', 'processing instruction': 'a processing instruction'}.get(
        kind, 'text outside a value')


def _leaf(name, text):
    """The value of a leaf element from its text (entity and character references already resolved by the parser)."""
    if name in ('string', 'key'):
        return text
    if name in ('true', 'false'):
        if text:
            raise NotWhole('a leaf value of an undeclared spelling: ' + name)
        return name == 'true'
    if name == 'integer':
        if not INTEGER.fullmatch(text):
            raise NotWhole('a leaf value of an undeclared spelling: integer')
        return int(text, 16) if text[:2] in ('0x', '0X') else int(text)
    if name == 'real':
        if not REAL.fullmatch(text):
            raise NotWhole('a leaf value of an undeclared spelling: real')
        return float(text)
    if name == 'date':
        match = DATE.fullmatch(text)
        if not match:
            raise NotWhole('a leaf value of an undeclared spelling: date')
        try:
            return datetime.datetime(*map(int, match.groups()))
        except ValueError:
            raise NotWhole('a leaf value of an undeclared spelling: date') from None
    # data: base64, padded, with whitespace allowed anywhere (wrapping at any width).
    compact = re.sub(r'[ \t\r\n]', '', text)
    if not BASE64.fullmatch(compact):
        raise NotWhole('a leaf value of an undeclared spelling: data')
    return base64.b64decode(compact, validate=True)


def structure_value(raw):
    """The value of an XML property list built from its own events, without plistlib; raises NotWhole on anything the
    property-list grammar does not account for."""
    if raw.startswith(b'bplist'):
        raise NotWhole('a binary property list; only an XML property list is read as a whole document')
    if not raw.startswith(b'<?xml'):
        raise NotWhole('not an XML document beginning with its XML declaration')
    try:
        found = events(raw, everything=True)
    except ExpatError as error:
        if error.code == expat.errors.codes[expat.errors.XML_ERROR_JUNK_AFTER_DOC_ELEMENT]:
            raise NotWhole('bytes after the document element') from None
        raise NotWhole('not well-formed XML') from None
    starts = [n for n, event in enumerate(found) if event[1] == 'start']
    if not starts:
        raise NotWhole('no root element')
    root = starts[0]
    _header(raw, found, root)
    # Stack frames: [element name, collected value or text pieces, pending key, keys seen].
    stack, result, closed = [], [], False
    for n in range(root, len(found)):
        _, kind, values, in_container = found[n]
        top = stack[-1] if stack else None
        if kind == 'start':
            name, attributes = values
            if closed:
                raise NotWhole('a second root element')
            if top is None:
                if name != 'plist':
                    raise NotWhole('the root is not a plist element')
                if set(attributes) - {'version'} or attributes.get('version', '1.0') != '1.0':
                    raise NotWhole('an attribute other than the root version')
            else:
                if name not in LEAVES and name not in CONTAINERS - {'plist'}:
                    raise NotWhole('an element that is not a property-list element')
                if attributes:
                    raise NotWhole('an attribute other than the root version')
                if top[0] in LEAVES:
                    raise NotWhole('an element inside a leaf value')
                if top[0] == 'plist' and top[1]:
                    raise NotWhole('a second value under plist')
                if top[0] == 'dict':
                    if name == 'key' and top[2] is not None:
                        raise NotWhole('a key with no value')
                    if name != 'key' and top[2] is None:
                        raise NotWhole('a value with no key in a dictionary')
                elif name == 'key':
                    raise NotWhole('a key outside a dictionary')
            stack.append([name, [] if name != 'dict' else {}, None, set()])
        elif kind == 'end':
            name, value, pending, _ = stack.pop()
            if name == 'plist':
                if len(value) != 1:
                    raise NotWhole('no value under plist')
                result, closed = value, True
                continue
            if name == 'dict':
                if pending is not None:
                    raise NotWhole('a key with no value')
            elif name in LEAVES:
                value = _leaf(name, ''.join(value))
            parent = stack[-1]
            if name == 'key':
                if value in parent[3]:
                    raise NotWhole('a key twice in one dictionary')
                parent[3].add(value)
                parent[2] = value
            elif parent[0] == 'dict':
                parent[1][parent[2]] = value
                parent[2] = None
            else:
                parent[1].append(value)
        elif kind == 'text' and top is not None and top[0] in LEAVES:
            top[1].append(values[0])
        elif kind in ('cdata start', 'cdata end') and top is not None and top[0] in ('string', 'key'):
            pass  # a CDATA section's text is reported as text; it is a spelling of the string's text
        elif kind == 'other' and top is None and closed and _blank(values[0]):
            pass  # whitespace after the root element
        elif kind == 'text' and in_container and _blank(values[0]) and not span(raw, found, n).strip(XML_WHITESPACE):
            pass  # whitespace between elements, written as whitespace bytes (not a character reference)
        elif kind in ('cdata start', 'cdata end') and top is not None and top[0] in LEAVES:
            raise NotWhole('a leaf value of an undeclared spelling: ' + top[0])
        else:
            raise NotWhole(_named(kind) if kind in ('comment', 'processing instruction')
                           else 'text outside a value' if kind in ('text', 'cdata start', 'cdata end')
                           else 'a construct the property-list grammar does not include')
    if not closed or stack:
        raise NotWhole('the root element is not closed')
    return result[0]


class _UniqueDict(dict):
    def __setitem__(self, key, value):
        if key in self:
            raise ValueError('a key appears twice')
        super().__setitem__(key, value)


def _same(a, b):
    """Equal values with equal types (a dictionary of any class is a dictionary), in the same key order."""
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
    except (ValueError, ExpatError, AttributeError, TypeError, IndexError, OverflowError, binascii.Error):
        raise NotWhole('the standard parser refuses the document') from None
    if not _same(value, standard):
        raise NotWhole('the standard parser reads another value')
    return value
