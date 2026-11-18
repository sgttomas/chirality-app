"""Notice-only reader for locked .crate archives: header inventory first, then only the selected notice bytes.

The route, for one archive and the package a held lockfile names:

1. The archive's bytes are read as one opaque file and their SHA-256 must equal the lockfile checksum before the
   archive is opened. The verified bytes are kept in memory, so what is opened is what was verified.
2. The gzip stream is walked header by header. Each tar header (and each GNU long-name or pax extended header, which
   carries a member's name) is parsed; every other member's payload is skipped by a forward seek. Payload bytes of
   unselected members are never returned to this module: they pass only through the gzip decompressor, which must
   process the stream in order to reach the next header, and are discarded there.
3. The inventory (every member's name, type and size) is checked before any payload is read. The archive is refused
   for a member outside `<name>-<version>/`, an unsafe or traversing path, a repeated name, two names equal ignoring
   case, a symbolic or hard link, or any member type other than a regular file or a directory.
4. Notice members are selected by name alone (`is_notice`), at any depth, and the selection is a list of exact paths.
   A second walk reads only those members' bytes, and each must be a regular file whose length equals its header.
5. `index` records, per package, the lockfile checksum, the member count, the inventory digest, and each selected
   notice's path, size, SHA-256 and Git blob. `extract` repeats steps 1 to 4 and requires every result to equal the
   index before it writes anything.

Nothing here parses a manifest, README or source file, runs a build, a resolver or Cargo, or writes to a cache.
`read_member` returns one named member's bytes after the same checks; crates.py uses it only to compare a committed
parent manifest with its archive's Cargo.toml. A
selection by name finds the files named as notices; it does not show that no other file carries its own terms.
"""
import gzip
import hashlib
import io
import json
import re

BLOCK = 512
# A notice-named file: the name starts with a licence or notice word.
NOTICE_STEM = re.compile(r'^(licen[cs]e|copying|notice|copyright|unlicense|credits|authors|patents|third[-_]?party)', re.I)
# Extensions that make a notice-named file something else (source, data or build files), so it is not selected.
NOT_A_NOTICE = re.compile(
    r'\.(rs|c|cc|cpp|cxx|h|hh|hpp|hxx|inc|s|asm|py|pyi|js|mjs|cjs|ts|go|java|kt|rb|pl|pm|php|sh|bash|zsh|fish|ps1|bat|cmd|'
    r'toml|json|yaml|yml|xml|lock|cfg|ini|mk|cmake|in|am|ac|m4|bzl|bazel|gn|gni|proto|wasm|o|a|so|dylib|dll|exe|'
    r'png|jpg|jpeg|gif|svg|ico|bin|dat|gz|zip|tar|xz|bz2|zst|tmpl|template|tera|hbs|j2|star|snap|stderr|stdout|out|diff|patch)$',
    re.I)
REGULAR, DIRECTORY = 'file', 'dir'
_TYPES = {b'0': REGULAR, b'\0': REGULAR, b'7': REGULAR, b'5': DIRECTORY}


class Refused(ValueError):
    """The archive does not meet the route's conditions; nothing from it is used."""


def require(condition, message):
    if not condition:
        raise Refused(message)


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def git_blob(raw):
    return hashlib.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()


NOTICE_FOLDER = re.compile(r'^licen[cs]es?$', re.I)


def is_notice(path):
    """True for a member path, at any depth, whose file name is a notice name or which sits in a licence folder
    (such as `LICENSES/`), and which is not a source, data or build file."""
    *folders, name = path.split('/')
    named = bool(NOTICE_STEM.match(name)) or any(NOTICE_FOLDER.match(f) for f in folders)
    return named and not NOT_A_NOTICE.search(name)


def _number(field):
    if field and field[0] & 0x80:
        value = int.from_bytes(field, 'big') & ~(1 << (8 * len(field) - 1))
        return value
    text = field.split(b'\0', 1)[0].strip(b' ')
    require(re.fullmatch(rb'[0-7]*', text) is not None, 'malformed numeric header field')
    return int(text or b'0', 8)


def _string(field):
    return field.split(b'\0', 1)[0].decode('utf-8')


def _pax(data):
    records, at = {}, 0
    while at < len(data):
        space = data.index(b' ', at)
        length = int(data[at:space])
        require(length > 0, 'malformed pax record')
        key, _, value = data[space + 1:at + length - 1].partition(b'=')
        records[key.decode('utf-8')] = value.decode('utf-8')
        at += length
    return records


def _walk(stream):
    """Yield (path, kind, size, data_offset) for each member; payloads are skipped, never returned."""
    long_name, pax, offset = None, {}, 0
    while True:
        header = stream.read(BLOCK)
        if not header or header == b'\0' * BLOCK:
            return
        require(len(header) == BLOCK, 'truncated header')
        stored = _number(header[148:156])
        unsigned = sum(header[:148]) + 32 * 8 + sum(header[156:])
        signed = sum(b - 256 if b > 127 else b for b in header[:148] + header[156:]) + 32 * 8
        require(stored in (unsigned, signed), 'header checksum differs')
        offset += BLOCK
        size = _number(header[124:136])
        require(size >= 0, 'negative member size')
        padded = (size + BLOCK - 1) // BLOCK * BLOCK
        flag = header[156:157]
        if flag in (b'L', b'x'):
            # A name-carrying header: its data is header data, read and parsed for the next member's name.
            data = stream.read(padded)
            require(len(data) == padded, 'truncated extended header')
            offset += padded
            if flag == b'L':
                long_name = data[:size].split(b'\0', 1)[0].decode('utf-8')
            else:
                pax = _pax(data[:size])
                require(set(pax) <= {'path', 'size', 'mtime', 'atime', 'ctime', 'uid', 'gid', 'uname', 'gname'},
                        'pax header carries an unsupported record: ' + ','.join(sorted(set(pax))))
            continue
        require(flag not in (b'1', b'2', b'K'), 'archive has a link member')
        kind = _TYPES.get(flag)
        require(kind is not None, 'archive has an unsupported member type: ' + repr(flag))
        magic = header[257:265]
        name = _string(header[0:100])
        if magic[:6] == b'ustar\0':
            prefix = _string(header[345:500])
            name = prefix + '/' + name if prefix else name
        if long_name is not None:
            name = long_name
        if 'path' in pax:
            name = pax['path']
        if 'size' in pax:
            require(re.fullmatch(r'[0-9]+', pax['size']) is not None,
                    'pax size must be a nonnegative decimal')
            size = int(pax['size'])
            padded = (size + BLOCK - 1) // BLOCK * BLOCK
        yield name, kind, size, offset
        long_name, pax = None, {}
        if padded:
            stream.seek(padded, io.SEEK_CUR)
            offset += padded


def _members(raw, package, opener=gzip.GzipFile):
    prefix = f'{package[0]}-{package[1]}/'
    members, folded = [], {}
    with opener(fileobj=io.BytesIO(raw)) as stream:
        for name, kind, size, offset in _walk(stream):
            path = name.rstrip('/') if kind == DIRECTORY else name
            require(path.startswith(prefix) or path + '/' == prefix, 'member outside the package folder: ' + name)
            relative = path[len(prefix):]
            if kind == DIRECTORY and relative == '':
                continue
            parts = relative.split('/')
            require(relative and '\\' not in relative and all(p not in ('', '.', '..') for p in parts),
                    'unsafe member path: ' + name)
            key = relative.casefold()
            require(key not in folded, 'archive repeats a member, or has two names equal ignoring case: '
                    + relative + ' and ' + folded.get(key, relative))
            folded[key] = relative
            members.append({'path': relative, 'kind': kind, 'size': size, 'offset': offset})
    return members


def inventory_digest(members):
    canonical = json.dumps([[m['path'], m['kind'], m['size']] for m in members], separators=(',', ':')).encode()
    return sha256(canonical)


def read_notices(raw, package, checksum, opener=gzip.GzipFile):
    """(inventory, notices) for one verified archive: the header inventory and the selected notice members' bytes."""
    require(sha256(raw) == checksum, f'archive differs from the lockfile checksum: {package[0]} {package[1]}')
    members = _members(raw, package, opener)
    selected = [m for m in members if m['kind'] == REGULAR and is_notice(m['path'])]
    notices = []
    with opener(fileobj=io.BytesIO(raw)) as stream:
        at = 0
        for member in sorted(selected, key=lambda m: m['offset']):
            stream.seek(member['offset'] - at, io.SEEK_CUR)
            data = stream.read(member['size'])
            require(len(data) == member['size'], 'notice member is shorter than its header: ' + member['path'])
            at = member['offset'] + member['size']
            notices.append({'path': member['path'], 'size_bytes': len(data), 'sha256': sha256(data),
                            'git_blob_sha1': git_blob(data), 'data': data})
    inventory = {'members': len(members), 'inventory_sha256': inventory_digest(members)}
    return inventory, sorted(notices, key=lambda n: n['path'])


def index_entry(raw, package, checksum, opener=gzip.GzipFile):
    """The index row for one package, with each selected notice's identity (no bytes)."""
    inventory, notices = read_notices(raw, package, checksum, opener)
    return {'package': package[0], 'version': package[1], 'checksum': checksum, **inventory,
            'notices': [{k: n[k] for k in ('path', 'size_bytes', 'sha256', 'git_blob_sha1')} for n in notices]}


def extract_checked(raw, entry, opener=gzip.GzipFile):
    """The selected notice bytes of one archive, required to equal its index row exactly; nothing else is returned."""
    package = (entry['package'], entry['version'])
    inventory, notices = read_notices(raw, package, entry['checksum'], opener)
    require(inventory == {'members': entry['members'], 'inventory_sha256': entry['inventory_sha256']},
            f'archive inventory differs from the index: {package[0]} {package[1]}')
    found = [{k: n[k] for k in ('path', 'size_bytes', 'sha256', 'git_blob_sha1')} for n in notices]
    require(found == entry['notices'], f'selected notices differ from the index: {package[0]} {package[1]}')
    return {n['path']: n['data'] for n in notices}


def read_member(raw, package, checksum, member, opener=gzip.GzipFile):
    """The bytes of one named regular member of a verified archive (for crates.py verify-manifests), after the same
    checksum and header checks; no other member's payload is returned."""
    require(sha256(raw) == checksum, f'archive differs from the lockfile checksum: {package[0]} {package[1]}')
    found = [m for m in _members(raw, package, opener) if m['path'] == member]
    require(len(found) == 1 and found[0]['kind'] == REGULAR, f'the archive has no single regular member {member}')
    with opener(fileobj=io.BytesIO(raw)) as stream:
        stream.seek(found[0]['offset'], io.SEEK_CUR)
        data = stream.read(found[0]['size'])
    require(len(data) == found[0]['size'], 'member is shorter than its header: ' + member)
    return data
