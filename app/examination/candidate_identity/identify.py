#!/usr/bin/env python3
"""Development App candidate identity (DEL-09-01 candidate-identity-v2: bundle-tree v2).

Reads an already built, unpackaged App bundle without executing it, computes its
tree identity and writes or checks a candidate identification record. It builds
nothing, launches nothing, opens no examination and establishes no qualification.
"""
import argparse
import contextlib
import ctypes
from datetime import datetime
import errno
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import plistlib
import re
import stat
import subprocess
import sys
import tarfile
from xml.parsers.expat import ExpatError

METHOD = 'chirality.app.bundle-tree.sha256/v2'
FORMAT = 'chirality.app-v4.candidate-identification/v2'
BUNDLED_FORMAT = 'chirality.app-v4.candidate-identification/v3'
INVENTORY_FORMAT = 'chirality.app-v4.bundle-inventory/v2'
XATTR_ALLOWLIST = ('com.apple.provenance',)
KINDS = ('dir', 'file', 'symlink')
MAX_LINK_HOPS = 32
HEX = re.compile(r'[0-9a-f]{64}')
TIMESTAMP = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}[Tt][0-9]{2}:[0-9]{2}:[0-5][0-9]'
                       r'(?:\.[0-9]+)?(?:[Zz]|[+-](?:[01][0-9]|2[0-3]):[0-5][0-9])')
LIMITS = [
    'Identifies the exact bundle bytes, structure, modes, ownership and allowlisted extended attributes read at identification; reproducible rebuilding is not claimed.',
    'Unpackaged development build (route native_development): no signing, notarisation, package record or packaged witness.',
    'File times and location are outside the identity: examine this copy in a controlled location without relying on timestamps, launch-registration caches or timestamp-based resource selection; record the actual examination environment separately.',
    'ACLs, non-zero file flags, set-id bits, extended attributes outside the allowlist, absolute or escaping links and special files are refused, not omitted.',
    'Descriptor-relative no-follow reads with two equal passes detect ordinary change during reading; they do not establish custody against a concurrent hostile writer.',
    'The Codex supplier is not part of the bundle; each examination record binds its own supplier pin, distribution identity and configuration.',
    'No examination is opened, no App is launched and no candidate qualification, replacement or acceptance follows from this record.',
    'App-data absence is historical at identification, limited to the three declared identifier-selected locations; it is not a freshness promise after launch or a census of external state.',
]
_AFTER_FILE_READ = None  # test hook: called with the entry path after its bytes are read

XATTR_NOFOLLOW = 0x0001
ACL_TYPE_EXTENDED = 0x00000100
ACL_FIRST_ENTRY = 0
_libc = None
if sys.platform == 'darwin':  # bundle metadata is read through the macOS libc interfaces
    _libc = ctypes.CDLL(None, use_errno=True)
    _libc.flistxattr.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_size_t, ctypes.c_int]
    _libc.flistxattr.restype = ctypes.c_ssize_t
    _libc.listxattr.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_size_t, ctypes.c_int]
    _libc.listxattr.restype = ctypes.c_ssize_t
    _libc.fgetxattr.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_uint32, ctypes.c_int]
    _libc.fgetxattr.restype = ctypes.c_ssize_t
    _libc.getxattr.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_uint32, ctypes.c_int]
    _libc.getxattr.restype = ctypes.c_ssize_t
    _libc.acl_get_fd_np.argtypes = [ctypes.c_int, ctypes.c_int]
    _libc.acl_get_fd_np.restype = ctypes.c_void_p
    _libc.acl_get_link_np.argtypes = [ctypes.c_char_p, ctypes.c_int]
    _libc.acl_get_link_np.restype = ctypes.c_void_p
    _libc.acl_get_entry.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_void_p)]
    _libc.acl_get_entry.restype = ctypes.c_int
    _libc.acl_free.argtypes = [ctypes.c_void_p]
    _libc.acl_valid.argtypes = [ctypes.c_void_p]
    _libc.acl_valid.restype = ctypes.c_int


def _require_macos():
    if _libc is None:
        raise OSError(errno.ENOTSUP, 'bundle identification reads macOS extended attributes and ACLs; this platform is not supported')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def _os_error(what):
    code = ctypes.get_errno()
    return OSError(code, f'{what}: {os.strerror(code)}')


def _xattrs(fd=None, path=None):
    """Every extended attribute (name, size, SHA-256); names outside the allowlist refuse."""
    _require_macos()
    options = 0 if fd is not None else XATTR_NOFOLLOW
    listing = (lambda buf, n: _libc.flistxattr(fd, buf, n, options)) if fd is not None else \
        (lambda buf, n: _libc.listxattr(os.fsencode(path), buf, n, options))
    size = listing(None, 0)
    if size < 0:
        raise _os_error('extended attributes unreadable')
    buf = ctypes.create_string_buffer(size)
    if listing(buf, size) != size:
        raise ValueError('extended attributes changed during identification')
    names = [n for n in buf.raw[:size].split(b'\0') if n]
    out = []
    for raw_name in sorted(names):
        name = raw_name.decode('utf-8', 'strict')
        if name not in XATTR_ALLOWLIST:
            raise ValueError('extended attribute outside the allowlist refused: ' + name)
        getter = (lambda b, n: _libc.fgetxattr(fd, raw_name, b, n, 0, options)) if fd is not None else \
            (lambda b, n: _libc.getxattr(os.fsencode(path), raw_name, b, n, 0, options))
        length = getter(None, 0)
        if length < 0:
            raise _os_error('extended attribute unreadable: ' + name)
        value = ctypes.create_string_buffer(length)
        if getter(value, length) != length:
            raise ValueError('extended attribute changed during identification: ' + name)
        out.append({'name': name, 'size': length, 'sha256': sha(value.raw[:length])})
    return out


def _refuse_acl(fd=None, path=None, where='.'):
    _require_macos()
    ctypes.set_errno(0)
    acl = _libc.acl_get_fd_np(fd, ACL_TYPE_EXTENDED) if fd is not None else \
        _libc.acl_get_link_np(os.fsencode(path), ACL_TYPE_EXTENDED)
    if not acl:
        # Darwin uses ENOENT for an absent extended ACL even on an open fd.
        # Path-based link reads are bracketed by lstat in the scanner.
        if ctypes.get_errno() == errno.ENOENT:
            return
        raise _os_error('ACL unreadable: ' + where)
    try:
        if _libc.acl_valid(acl) != 0:
            raise _os_error('invalid ACL: ' + where)
        entry = ctypes.c_void_p()
        ctypes.set_errno(0)
        result = _libc.acl_get_entry(acl, ACL_FIRST_ENTRY, ctypes.byref(entry))
        if result == 0:
            raise ValueError('ACL refused: ' + where)
        # Darwin returns -1/EINVAL for the first entry of a valid empty ACL.
        if result != -1 or ctypes.get_errno() != errno.EINVAL:
            raise _os_error('ACL entries unreadable: ' + where)
    finally:
        _libc.acl_free(acl)


def _metadata(info, where):
    _require_macos()
    if info.st_mode & (stat.S_ISUID | stat.S_ISGID):
        raise ValueError('set-user-ID or set-group-ID bit refused: ' + where)
    if info.st_flags:
        raise ValueError('non-zero file flags refused: ' + where)
    return {'mode': stat.S_IMODE(info.st_mode), 'uid': info.st_uid, 'gid': info.st_gid}


def _check_name(name):
    if not isinstance(name, str):
        raise ValueError('bundle path is not text')
    try:
        name.encode('utf-8', 'strict')
    except UnicodeError as error:
        raise ValueError('bundle path is not valid UTF-8') from error
    if name in ('', '.', '..') or any(c in name for c in '/\\\r\n\0'):
        raise ValueError('bundle path cannot be represented: ' + repr(name))


def _stamp(info):
    """Ignore atime (our reads change it); include mutable access metadata."""
    return (info.st_dev, info.st_ino, info.st_mode, info.st_uid, info.st_gid,
            info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns,
            getattr(info, 'st_flags', None))


def _binding(info):
    return info.st_dev, info.st_ino, info.st_mode, info.st_uid, info.st_gid


@contextlib.contextmanager
def _open_directory(root, bundle=False):
    """Open every ancestor relative to its held parent, without following links."""
    root = Path(os.path.abspath(root))
    if bundle and root.suffix != '.app':
        raise ValueError('bundle root must be a .app directory')
    _check_name(root.name)
    held = []
    try:
        fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
        held.append(fd)
        bindings = []
        for part in root.parts[1:]:
            info = os.stat(part, dir_fd=fd, follow_symlinks=False)
            if stat.S_ISLNK(info.st_mode):
                raise ValueError('symlink in bundle root ancestry: ' + part)
            child = os.open(part, os.O_RDONLY | os.O_NOFOLLOW | os.O_DIRECTORY, dir_fd=fd)
            held.append(child)
            if _stamp(info) != _stamp(os.fstat(child)):
                raise ValueError('bundle ancestry changed during identification')
            bindings.append((fd, part, child, info))
            fd = child
        yield fd
        for parent, name, child, original in bindings:
            bound = os.stat(name, dir_fd=parent, follow_symlinks=False)
            live = os.fstat(child)
            if _binding(bound) != _binding(live) or _binding(original) != _binding(live):
                raise ValueError('bundle ancestry replaced during identification')
    finally:
        for fd in reversed(held):
            os.close(fd)


def _observed_meta(info, where, **handle):
    _refuse_acl(where=where, **handle)
    return {**_metadata(info, where), 'xattrs': _xattrs(**handle)}


def _read_regular(fd, info, relative, retain=False):
    start = os.fstat(fd)
    if not stat.S_ISREG(start.st_mode) or _stamp(info) != _stamp(start):
        raise ValueError('file replaced during identification: ' + relative)
    if start.st_nlink != 1:
        raise ValueError('hard-linked file refused: ' + relative)
    meta = _observed_meta(start, relative, fd=fd)
    digest = hashlib.sha256()
    chunks = []
    size = 0
    while chunk := os.read(fd, 1 << 20):
        digest.update(chunk)
        size += len(chunk)
        if retain:
            chunks.append(chunk)
    if _AFTER_FILE_READ:
        _AFTER_FILE_READ(relative)
    end = os.fstat(fd)
    if _observed_meta(end, relative, fd=fd) != meta or _stamp(start) != _stamp(os.fstat(fd)) or size != start.st_size:
        raise ValueError('file changed during identification: ' + relative)
    return {'path': relative, 'kind': 'file', **meta, 'size': size, 'sha256': digest.hexdigest()}, b''.join(chunks)


def _scan_once(root):
    _require_macos()
    root = Path(os.path.abspath(root))
    flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
    entries = []

    def visit(fd, prefix):
        before = os.fstat(fd)
        meta = _observed_meta(before, prefix or '.', fd=fd)
        with os.scandir(fd) as listing:
            names = sorted((e.name for e in listing), key=lambda n: n.encode('utf-8', 'surrogateescape'))
        for name in names:
            _check_name(name)
            relative = prefix + name
            info = os.stat(name, dir_fd=fd, follow_symlinks=False)
            if stat.S_ISLNK(info.st_mode):
                if info.st_nlink != 1:
                    raise ValueError('hard-linked symlink refused: ' + relative)
                full = str(root / relative)
                link_meta = _observed_meta(info, relative, path=full)
                target = os.readlink(name, dir_fd=fd)
                entry = {'path': relative, 'kind': 'symlink', **link_meta, 'target': target}
                if _observed_meta(os.stat(name, dir_fd=fd, follow_symlinks=False), relative, path=full) != link_meta:
                    raise ValueError('symlink metadata changed during identification: ' + relative)
                entries.append(entry)
            elif stat.S_ISDIR(info.st_mode):
                child = os.open(name, flags | os.O_DIRECTORY, dir_fd=fd)
                try:
                    if _stamp(os.fstat(child)) != _stamp(info):
                        raise ValueError('directory replaced during identification: ' + relative)
                    child_meta = visit(child, relative + '/')
                    entries.append({'path': relative, 'kind': 'dir', **child_meta})
                finally:
                    os.close(child)
            elif stat.S_ISREG(info.st_mode):
                child = os.open(name, flags, dir_fd=fd)
                try:
                    entry, _ = _read_regular(child, info, relative)
                    entries.append(entry)
                finally:
                    os.close(child)
            else:
                raise ValueError('special file refused: ' + relative)
            if _stamp(info) != _stamp(os.stat(name, dir_fd=fd, follow_symlinks=False)):
                raise ValueError('entry changed during identification: ' + relative)
        after = os.fstat(fd)
        if _observed_meta(after, prefix or '.', fd=fd) != meta or _stamp(before) != _stamp(os.fstat(fd)):
            raise ValueError('directory changed during identification: ' + (prefix or '.'))
        return meta

    with _open_directory(root, bundle=True) as fd:
        top = visit(fd, '')
    entries.sort(key=lambda e: e['path'].encode('utf-8'))
    inv = {'format': INVENTORY_FORMAT, 'method': METHOD, 'root': top, 'entries': entries}
    return validate_inventory(inv)


def inventory(root):
    """Two complete passes must agree; the value excludes the root's location and name."""
    first = _scan_once(root)
    second = _scan_once(root)
    if canonical(first) != canonical(second):
        raise ValueError('bundle changed between identification passes')
    return first


def identity(inv):
    validate_inventory(inv)
    body = {'method': inv['method'], 'root': inv['root'], 'entries': inv['entries']}
    return METHOD + ':' + sha(canonical(body))


def file_manifest(inv):
    """DEL-01-06 PKG §5.2 regular-file manifest; recorded beside the identity, never instead of it."""
    lines = ''.join(f"{e['sha256']}  {e['path']}\n" for e in inv['entries'] if e['kind'] == 'file')
    return sha(lines.encode('utf-8'))


def _int(value, low, high):
    return type(value) is int and low <= value <= high


def _check_meta(e, where):
    if not _int(e.get('mode'), 0, 0o7777) or e['mode'] & 0o6000:
        raise ValueError('invalid mode: ' + where)
    if not _int(e.get('uid'), 0, 2**32 - 1) or not _int(e.get('gid'), 0, 2**32 - 1):
        raise ValueError('invalid owner: ' + where)
    xattrs = e.get('xattrs')
    if not isinstance(xattrs, list):
        raise ValueError('invalid extended attributes: ' + where)
    names = []
    for x in xattrs:
        if not isinstance(x, dict) or set(x) != {'name', 'size', 'sha256'} or x['name'] not in XATTR_ALLOWLIST \
                or not _int(x['size'], 0, 2**63) or not isinstance(x['sha256'], str) or not HEX.fullmatch(x['sha256']):
            raise ValueError('invalid or refused extended attribute: ' + where)
        names.append(x['name'])
    if names != sorted(set(names)):
        raise ValueError('extended attributes not unique and sorted: ' + where)


def resolve_link(by_path, link):
    """Resolve a link (and any chain) within the bundle; absolute, escaping, dangling or cyclic links refuse."""
    current = link.split('/')[:-1]
    pending = list(by_path[link]['target'].split('/'))
    if by_path[link]['target'].startswith('/') or by_path[link]['target'] == '':
        raise ValueError('absolute or empty link target refused: ' + link)
    hops = 1
    while pending:
        part = pending.pop(0)
        if part in ('', '.'):
            continue
        if part == '..':
            if not current:
                raise ValueError('link escapes the bundle root: ' + link)
            current.pop()
            continue
        candidate = '/'.join(current + [part])
        entry = by_path.get(candidate)
        if entry is None:
            raise ValueError('dangling link refused: ' + link)
        if entry['kind'] == 'symlink':
            hops += 1
            if hops > MAX_LINK_HOPS:
                raise ValueError('link cycle or chain too long: ' + link)
            target = entry['target']
            if target.startswith('/') or target == '':
                raise ValueError('absolute or empty link target refused: ' + link)
            pending = target.split('/') + pending
            continue
        if entry['kind'] == 'file' and pending:
            raise ValueError('link passes through a file: ' + link)
        current.append(part)
    return '/'.join(current)


def _check_target(target):
    if not isinstance(target, str):
        raise ValueError('invalid link target')
    try:
        target.encode('utf-8', 'strict')
    except UnicodeError as error:
        raise ValueError('link target is not valid UTF-8') from error
    if any(c in target for c in '\\\r\n\0'):
        raise ValueError('link target cannot be represented')


def validate_inventory(inv):
    if not isinstance(inv, dict) or set(inv) != {'format', 'method', 'root', 'entries'}:
        raise ValueError('inventory fields differ from the method')
    if inv['format'] != INVENTORY_FORMAT or inv['method'] != METHOD:
        raise ValueError('unknown inventory format or method')
    if not isinstance(inv['root'], dict) or set(inv['root']) != {'mode', 'uid', 'gid', 'xattrs'}:
        raise ValueError('invalid root entry')
    _check_meta(inv['root'], '.')
    if not isinstance(inv['entries'], list):
        raise ValueError('inventory entries are not a list')
    by_path = {}
    previous = None
    for e in inv['entries']:
        if not isinstance(e, dict) or e.get('kind') not in KINDS:
            raise ValueError('invalid inventory entry kind')
        extra = {'file': {'size', 'sha256'}, 'symlink': {'target'}, 'dir': set()}[e['kind']]
        if set(e) != {'path', 'kind', 'mode', 'uid', 'gid', 'xattrs'} | extra:
            raise ValueError('invalid inventory entry fields: ' + repr(e.get('path')))
        path = e['path']
        if not isinstance(path, str):
            raise ValueError('invalid path')
        parts = path.split('/')
        for part in parts:
            _check_name(part)
        if PurePosixPath(path).is_absolute() or path in by_path:
            raise ValueError('invalid or duplicate path: ' + repr(path))
        key = path.encode('utf-8')
        if previous is not None and previous >= key:
            raise ValueError('entries are not in UTF-8 byte order')
        previous = key
        parent = '/'.join(parts[:-1])
        if parent and by_path.get(parent, {}).get('kind') != 'dir':
            raise ValueError('parent is not a listed directory: ' + path)
        _check_meta(e, path)
        if e['kind'] == 'file' and (not _int(e['size'], 0, 2**63) or not isinstance(e['sha256'], str) or not HEX.fullmatch(e['sha256'])):
            raise ValueError('invalid file entry: ' + path)
        if e['kind'] == 'symlink':
            _check_target(e['target'])
        by_path[path] = e
    for path, e in by_path.items():
        if e['kind'] == 'symlink':
            resolve_link(by_path, path)
    return inv


def metadata_state(inv):
    """The observed metadata the record shows beside the identity."""
    every = [inv['root'], *inv['entries']]
    xattrs = {}
    for e in every:
        for x in e['xattrs']:
            xattrs[x['name']] = xattrs.get(x['name'], 0) + 1
    owners = sorted({(e['uid'], e['gid']) for e in every})
    return {'entries_including_root': len(every), 'acl_entries': 0, 'nonzero_flags': 0, 'set_id_bits': 0,
            'extended_attributes': xattrs, 'xattr_allowlist': list(XATTR_ALLOWLIST),
            'owners': [{'uid': u, 'gid': g} for u, g in owners],
            'symlinks': sum(e['kind'] == 'symlink' for e in inv['entries'])}


def compare(expected, observed):
    left = {e['path']: e for e in expected['entries']}
    right = {e['path']: e for e in observed['entries']}
    return {'equal': canonical(expected) == canonical(observed),
            'root_equal': expected['root'] == observed['root'],
            'missing': sorted(left.keys() - right.keys()), 'extra': sorted(right.keys() - left.keys()),
            'changed': sorted(p for p in left.keys() & right.keys() if left[p] != right[p])}


def git(repo, *args):
    result = subprocess.run(['git', '-C', str(repo), *args], capture_output=True, check=True,
                            env=dict(os.environ, GIT_NO_LAZY_FETCH='1', GIT_NO_REPLACE_OBJECTS='1'))
    return result.stdout


def verify_export(repo, revision, prefix, export_root):
    """Every tracked file and link under prefix at revision exists unchanged in the export."""
    tree_ref = revision + '^{tree}' if prefix == '.' else f'{revision}:{prefix}'
    tree = git(repo, 'rev-parse', tree_ref).decode().strip()
    listing = git(repo, 'ls-tree', '-r', '-z', '--full-tree', revision, '--', prefix).split(b'\0')
    count = 0
    with _open_directory(export_root) as base:
        for row in filter(None, listing):
            meta, path = row.split(b'\t', 1)
            mode, kind, blob = meta.decode().split()
            if kind != 'blob' or mode not in ('100644', '100755', '120000'):
                raise ValueError('unsupported tracked entry: ' + path.decode())
            parts = path.decode('utf-8', 'strict').split('/')
            for part in parts:
                _check_name(part)
            held = []
            fd = base
            try:
                for part in parts[:-1]:
                    fd = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                    held.append(fd)
                info = os.stat(parts[-1], dir_fd=fd, follow_symlinks=False)
                if mode == '120000':
                    if not stat.S_ISLNK(info.st_mode):
                        raise ValueError('exported link is not a link: ' + path.decode())
                    data = os.fsencode(os.readlink(parts[-1], dir_fd=fd))
                else:
                    if not stat.S_ISREG(info.st_mode):
                        raise ValueError('exported file is not a regular file: ' + path.decode())
                    child = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
                    held.append(child)
                    if _stamp(info) != _stamp(os.fstat(child)):
                        raise ValueError('exported file replaced during verification')
                    chunks = []
                    while chunk := os.read(child, 1 << 20):
                        chunks.append(chunk)
                    data = b''.join(chunks)
                    if _stamp(info) != _stamp(os.fstat(child)):
                        raise ValueError('exported file changed during verification')
                    if bool(info.st_mode & stat.S_IXUSR) != (mode == '100755'):
                        raise ValueError('exported executable mode differs from revision: ' + path.decode())
                if _stamp(info) != _stamp(os.stat(parts[-1], dir_fd=fd, follow_symlinks=False)):
                    raise ValueError('exported entry changed during verification')
                if hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest() != blob:
                    raise ValueError('exported source differs from revision: ' + path.decode())
                count += 1
            finally:
                for child in reversed(held):
                    os.close(child)
    return {'tree': tree, 'tracked_files_verified': count}


APP_DATA_PLACES = ('Library/Application Support/{id}', 'Library/WebKit/{id}', 'Library/Caches/{id}')


def _check_identifier(identifier):
    if not isinstance(identifier, str) or not re.fullmatch(r'[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+', identifier):
        raise ValueError('invalid bundle identifier')


def app_data_declaration(identifier):
    _check_identifier(identifier)
    places = ['~/' + p.format(id=identifier) for p in APP_DATA_PLACES]
    return {'directory': places[0], 'checked': places, 'present_at_identification': []}


def app_data_state(identifier):
    """Observe only the declared Tauri data and WKWebView data/cache locations."""
    result = app_data_declaration(identifier)
    with _open_directory(Path.home()) as home:
        for place in result['checked']:
            parts = PurePosixPath(place[2:]).parts
            fd = home
            held = []
            parents = [(home, os.fstat(home))]
            bindings = []
            try:
                for index, part in enumerate(parts):
                    try:
                        info = os.stat(part, dir_fd=fd, follow_symlinks=False)
                    except FileNotFoundError:
                        break
                    if index == len(parts) - 1:
                        result['present_at_identification'].append(place)
                    else:
                        if not stat.S_ISDIR(info.st_mode):
                            raise ValueError('App data ancestry is not a plain directory: ' + place)
                        child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                        held.append(child)
                        bindings.append((fd, part, info))
                        if _stamp(info) != _stamp(os.fstat(child)):
                            raise ValueError('App data ancestry changed during identification')
                        fd = child
                        parents.append((fd, info))
                for handle, info in parents:
                    if _stamp(info) != _stamp(os.fstat(handle)):
                        raise ValueError('App data ancestry changed during identification')
                for handle, part, info in bindings:
                    if _stamp(info) != _stamp(os.stat(part, dir_fd=handle, follow_symlinks=False)):
                        raise ValueError('App data ancestry replaced during identification')
            finally:
                for child in reversed(held):
                    os.close(child)
    return result


def bundle_metadata(root, inv):
    entries = {e['path']: e for e in inv['entries']}
    plist_entry = entries.get('Contents/Info.plist', {})
    if plist_entry.get('kind') != 'file':
        raise ValueError('Info.plist is not an inventoried regular file')
    # Re-read only through held no-follow descriptors, including Contents.
    with _open_directory(root, bundle=True) as fd:
        directory = os.open('Contents', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
        try:
            child = os.open('Info.plist', os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
            try:
                observed, data = _read_regular(child, os.fstat(child), 'Contents/Info.plist', retain=True)
            finally:
                os.close(child)
            if observed != plist_entry:
                raise ValueError('Info.plist differs from the inventory')
            for handle, expected, where in ((fd, inv['root'], '.'), (directory, entries['Contents'], 'Contents')):
                if _observed_meta(os.fstat(handle), where, fd=handle) != {k: expected[k] for k in ('mode', 'uid', 'gid', 'xattrs')}:
                    raise ValueError('bundle metadata changed during plist read: ' + where)
        finally:
            os.close(directory)
    plist = plistlib.loads(data)
    if not isinstance(plist, dict):
        raise ValueError('Info.plist is not a dictionary')
    name = plist.get('CFBundleExecutable')
    _check_name(name)
    identifier = plist.get('CFBundleIdentifier')
    _check_identifier(identifier)
    for field in ('CFBundleShortVersionString', 'CFBundleVersion'):
        if field in plist:
            value = plist[field]
            if not isinstance(value, str) or not value or any(ord(c) < 32 for c in value):
                raise ValueError('invalid plist version field: ' + field)
            value.encode('utf-8', 'strict')
    executable = 'Contents/MacOS/' + name
    if entries.get(executable, {}).get('kind') != 'file':
        raise ValueError('bundle executable missing: ' + executable)
    return {'name': Path(os.path.abspath(root)).name, 'identifier': identifier,
            'version': str(plist.get('CFBundleShortVersionString') or plist.get('CFBundleVersion') or ''),
            'executable': {'path': executable, 'sha256': entries[executable]['sha256']},
            'info_plist_sha256': plist_entry['sha256'],
            'file_manifest_sha256': file_manifest(inv),
            'counts': {k: sum(e['kind'] == k for e in inv['entries']) for k in KINDS},
            'metadata_state': metadata_state(inv)}


def make_record(args):
    inv = inventory(args.app)
    build_identity = identity(inv)
    revision = git(args.repo, 'rev-parse', '--verify', args.revision + '^{commit}').decode().strip()
    facts = json.loads(Path(args.build_facts).read_bytes())
    meta = bundle_metadata(args.app, inv)
    inventory_bytes = canonical(inv) + b'\n'
    record = {
        'format': FORMAT,
        'candidate_key': revision[:10] + '-' + build_identity.rsplit(':', 1)[1][:12],
        'app_candidate': {'revision': revision, 'build_identity': build_identity, 'packaged': False},
        'route': 'native_development',
        'source': {'repository': args.repository, 'revision': revision,
                   'commit_tree': git(args.repo, 'rev-parse', revision + '^{tree}').decode().strip(),
                   'exported_prefix': args.prefix,
                   **verify_export(args.repo, revision, args.prefix, args.export_root)},
        'build': facts,
        'bundle': {**meta, 'inventory': {'path': 'bundle-inventory.json', 'sha256': sha(inventory_bytes)}},
        'app_data': app_data_state(meta['identifier']),
        'supplier': {'bundled': False, 'binding': 'per examination record configuration (codex_pin, codex_distribution_identity)'},
        'identified_by': {'tool': 'app/examination/candidate_identity/identify.py',
                          'tool_sha256': sha(Path(__file__).read_bytes()), 'method': METHOD},
        'identified_at': args.identified_at,
        'limits': LIMITS,
    }
    acquisition = None
    if bool(args.supplier_archive) != bool(args.supplier_acquisition):
        raise ValueError('bundled supplier requires both archive and acquisition record')
    if args.supplier_archive:
        from bundled_supplier import identify_supplier
        record['supplier'], acquisition = identify_supplier(inv, args.supplier_archive, args.supplier_acquisition)
        record['format'] = BUNDLED_FORMAT
        record['identified_by']['supplier_tool_sha256'] = sha(Path(__file__).with_name('bundled_supplier.py').read_bytes())
        record['limits'] = [s for s in LIMITS if not s.startswith('The Codex supplier is not part')]
        record['limits'] += [
            'Bundled supplier files and modes match the measured official-source archive; acquisition authorization/custody remains the supplied record, not authenticated by this tool.',
            'Unsigned development candidate only: no installed-custody issuer, supplier qualification, signing, notarisation, native launch or release follows from identification.',
        ]
    else:
        from bundled_supplier import has_supplier
        if has_supplier(inv):
            raise ValueError('v2 excludes bundled Codex; supply archive and acquisition record for v3')
    validate_record(record)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=False)
    (out / 'bundle-inventory.json').write_bytes(inventory_bytes)
    if acquisition is not None:
        (out / 'supplier-acquisition.json').write_bytes(acquisition)
    (out / 'candidate-identification.json').write_bytes(json.dumps(record, indent=2, ensure_ascii=False).encode() + b'\n')
    return record


def validate_record(record):
    version = {FORMAT: 'v2', BUNDLED_FORMAT: 'v3'}.get(record.get('format'))
    if version is None:
        raise ValueError('unknown candidate identification format')
    schema_path = Path(__file__).resolve().parents[3] / f'execution/PKG-09/DEL-09-01/Design/candidate-identity-{version}/candidate-identification.schema.json'
    from jsonschema import Draft202012Validator
    errors = sorted(Draft202012Validator(json.loads(schema_path.read_text())).iter_errors(record), key=lambda e: str(list(e.path)))
    if errors:
        raise ValueError('record schema: ' + '; '.join(f"{'/'.join(map(str, e.path))}: {e.message}" for e in errors))
    # jsonschema's optional RFC3339 checker is absent in the prepared offline
    # environment. Enforce these fields with stdlib calendar validation too.
    for where, value in (('identified_at', record['identified_at']),
                         ('build.started_at', record['build']['started_at']),
                         ('build.finished_at', record['build']['finished_at'])):
        try:
            if not TIMESTAMP.fullmatch(value):
                raise ValueError('timestamp requires a date, time and explicit timezone')
            datetime.fromisoformat(value.upper())
        except ValueError as error:
            raise ValueError('invalid timestamp: ' + where) from error
    build = record['app_candidate']['build_identity']
    if record['candidate_key'] != record['app_candidate']['revision'][:10] + '-' + build.rsplit(':', 1)[1][:12]:
        raise ValueError('candidate key does not derive from revision and build identity')
    if record['source']['revision'] != record['app_candidate']['revision']:
        raise ValueError('source and candidate revisions differ')
    if record['app_data']['present_at_identification']:
        raise ValueError('App data already present; the candidate would not start fresh: ' + ', '.join(record['app_data']['present_at_identification']))
    if record['app_data'] != app_data_declaration(record['bundle']['identifier']):
        raise ValueError('App data checked-location declaration differs from the identifier-selected locations')
    return record


def check(args):
    """Recompute every bundle-derived record field from the stored inventory and the bundle."""
    folder = Path(args.record).parent
    record = json.loads(Path(args.record).read_bytes())
    validate_record(record)
    stored = (folder / record['bundle']['inventory']['path']).read_bytes()
    if sha(stored) != record['bundle']['inventory']['sha256']:
        raise ValueError('stored inventory differs from its recorded digest')
    expected = validate_inventory(json.loads(stored))
    from bundled_supplier import check_supplier, has_supplier
    if record['format'] == BUNDLED_FORMAT:
        check_supplier(record['supplier'], expected, folder)
    elif has_supplier(expected):
        raise ValueError('v2 record cannot declare a bundled supplier absent')
    if identity(expected) != record['app_candidate']['build_identity']:
        raise ValueError('stored inventory does not yield the recorded build identity')
    observed = inventory(args.app)
    result = compare(expected, observed)
    result['build_identity'] = identity(observed)
    result['recorded_build_identity'] = record['app_candidate']['build_identity']
    if result['equal']:
        derived = bundle_metadata(args.app, expected)
        mismatched = sorted(k for k, v in derived.items() if record['bundle'].get(k) != v)
        if record['app_data']['directory'] != '~/Library/Application Support/' + derived['identifier']:
            mismatched.append('app_data.directory')
        result['record_fields_mismatched'] = mismatched
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('inventory'); p.add_argument('app')
    p = sub.add_parser('record')
    p.add_argument('--app', required=True); p.add_argument('--repo', required=True)
    p.add_argument('--revision', required=True); p.add_argument('--prefix', default='.')
    p.add_argument('--export-root', required=True); p.add_argument('--build-facts', required=True)
    p.add_argument('--repository', default='sgttomas/chirality-app'); p.add_argument('--identified-at', required=True)
    p.add_argument('--out-dir', required=True)
    p.add_argument('--supplier-archive', help='Existing official macOS arm64 platform tarball; never downloaded or executed')
    p.add_argument('--supplier-acquisition', help='Exact acquisition record for that archive; retained with the v3 record')
    p = sub.add_parser('check'); p.add_argument('--record', required=True); p.add_argument('--app', required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'inventory':
            inv = inventory(args.app)
            print(json.dumps({'build_identity': identity(inv), 'file_manifest_sha256': file_manifest(inv),
                              'entries': len(inv['entries']), 'metadata_state': metadata_state(inv)}, indent=2))
            return 0
        if args.command == 'record':
            record = make_record(args)
            print(json.dumps({'candidate_key': record['candidate_key'], 'build_identity': record['app_candidate']['build_identity']}, indent=2))
            return 0
        result = check(args)
        print(json.dumps(result, indent=2))
        ok = result['equal'] and result['build_identity'] == result['recorded_build_identity'] and not result.get('record_fields_mismatched')
        return 0 if ok else 1
    except (ValueError, TypeError, KeyError, AttributeError, OSError, subprocess.CalledProcessError,
            json.JSONDecodeError, plistlib.InvalidFileException, ExpatError, tarfile.TarError) as error:
        print(json.dumps({'error': f'{type(error).__name__}: {error}'}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
