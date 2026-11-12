"""Candidate v3's bounded, read-only macOS arm64 archive correspondence.

No extraction, supplier execution, signature verification or custody issuance.
The bundle inventory retains directory metadata; tar correspondence compares
the complete regular-file set, bytes and modes, plus explicit tar directories.

Two supplier accounts are accepted. The npm platform tarball is bound by its
acquisition authorization record (supplier-acquisition.json). The supplier's
release package is bound by the committed canonical distribution record
(supplier-canonical-distribution.json), which states the locator, size, digest
and inventory but records no acquirer or authorization; the identification
states those two as not recorded and also compares the bundled tree with that
record's inventory.
"""
import contextlib
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tarfile

ROOT = 'Contents/Resources/codex'
TAR_ROOT = 'package/vendor/aarch64-apple-darwin'
METHOD = 'codex-platform-tar-files/v1'
PACKAGE_METHOD = 'codex-package-tar-files/v1'
NPM_FORM = 'supplier-acquisition-authorization/1'
DISTRIBUTION_FORM = 'chirality.supplier-canonical-assessment/1'
INVENTORY_METHOD = 'codex-vendor-tree-v1'
ACQUISITION_FILE = 'supplier-acquisition.json'
DISTRIBUTION_FILE = 'supplier-canonical-distribution.json'
PACKAGE_SOURCE = re.compile(r'https://github\.com/openai/codex/releases/download/rust-v(\d+\.\d+\.\d+)/'
                            r'(codex-package-aarch64-apple-darwin\.tar\.gz)')
NOT_RECORDED = 'not recorded'
HEX = re.compile('[0-9a-f]{64}')
BINDING = 'Archive correspondence only; each examination binds actual supplier configuration and runtime standing.'


def has_supplier(inv):
    return any(e['path'] == ROOT or e['path'].startswith(ROOT + '/') for e in inv['entries'])


def supplier_entries(inv):
    entries = {e['path']: e for e in inv['entries']}
    if entries.get(ROOT, {}).get('kind') != 'dir':
        raise ValueError('bundled supplier root is not a directory')
    subtree = {p[len(ROOT) + 1:]: e for p, e in entries.items() if p.startswith(ROOT + '/')}
    if not subtree or any(e['kind'] not in ('file', 'dir') for e in subtree.values()):
        raise ValueError('supplier links, special files or empty tree refused')
    if subtree.get('bin/codex', {}).get('kind') != 'file' or not subtree['bin/codex']['mode'] & 0o111:
        raise ValueError('bundled supplier entrypoint missing or nonexecutable')
    return subtree


def manifest(entries):
    return hashlib.sha256(b''.join(
        f"{e['sha256']}  {p}\n".encode() for p, e in sorted(entries.items(), key=lambda x: x[0].encode())
        if e['kind'] == 'file')).hexdigest()


@contextlib.contextmanager
def selected_file(path):
    # Reuse the live identification reader's ancestor, stat and metadata rules.
    import identify
    path = Path(os.path.abspath(path))
    with identify._open_directory(path.parent) as parent:
        info = os.stat(path.name, dir_fd=parent, follow_symlinks=False)
        fd = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
        with os.fdopen(fd, 'rb') as stream:
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or identify._stamp(info) != identify._stamp(os.fstat(fd)):
                raise ValueError('supplier input is not one stable regular file')
            meta = identify._observed_meta(info, str(path), fd=fd)
            yield stream
            if identify._stamp(info) != identify._stamp(os.fstat(fd)) or identify._stamp(info) != identify._stamp(os.stat(path.name, dir_fd=parent, follow_symlinks=False)) \
                    or meta != identify._observed_meta(os.fstat(fd), str(path), fd=fd):
                raise ValueError('supplier input changed during identification')


def _load(raw):
    def unique(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError('duplicate supplier account field')
            value[key] = item
        return value
    record = json.loads(raw, object_pairs_hook=unique)
    if not isinstance(record, dict):
        raise ValueError('supplier account is not an object')
    return record


def _archive_identity(digest, size):
    if not isinstance(digest, str) or not HEX.fullmatch(digest) or type(size) is not int or size <= 0:
        raise ValueError('invalid acquisition size or digest')


def _npm_facts(record):
    subject, acquisition = record['subject'], record['acquisition']
    match = re.fullmatch(r'codex-(\d+\.\d+\.\d+)-darwin-arm64\.tgz', subject['file'])
    if not match or subject['official_source_locator'] != 'https://registry.npmjs.org/@openai/codex/-/' + subject['file']:
        raise ValueError('unsupported supplier archive source or platform')
    digest, size = acquisition['sha256'], acquisition['size_bytes']
    _archive_identity(digest, size)
    return {'pin': match[1], 'archive': {'file': subject['file'], 'source': subject['official_source_locator'],
                                         'size_bytes': size, 'sha256': digest}}


def _relative(path):
    if not isinstance(path, str) or any(c in path for c in '\\\r\n\0') \
            or any(p in ('', '.', '..') for p in path.split('/')):
        raise ValueError('invalid distribution inventory path: ' + repr(path))
    return path


def _distribution_facts(record):
    """Locator, archive identity and inventory, read only from the committed record."""
    pin, archive, inventory = record['pin'], record['archive'], record['inventory']
    match = PACKAGE_SOURCE.fullmatch(archive['url']) if isinstance(archive.get('url'), str) else None
    if not isinstance(pin, str) or not match or match[1] != pin:
        raise ValueError('unsupported supplier release package source, platform or pin')
    metadata = record['package_metadata']
    if metadata.get('version') != pin or metadata.get('target') != 'aarch64-apple-darwin':
        raise ValueError('distribution package metadata differs from its pin or platform')
    _archive_identity(archive['sha256'], archive['size'])
    if inventory['method'] != INVENTORY_METHOD or inventory['algorithm'] != 'sha-256' \
            or not isinstance(inventory['entries'], list) or not inventory['entries']:
        raise ValueError('unsupported distribution inventory method')
    expected = {}
    for e in inventory['entries']:
        if not isinstance(e, dict):
            raise ValueError('invalid distribution inventory entry')
        path = _relative(e.get('path'))
        fields = {'dir': {'path', 'kind', 'mode'}, 'file': {'path', 'kind', 'mode', 'size', 'sha256'}}.get(e.get('kind'))
        if fields is None or set(e) != fields or path in expected or type(e['mode']) is not int or not 0 <= e['mode'] <= 0o777:
            raise ValueError('invalid distribution inventory entry: ' + path)
        if e['kind'] == 'file' and (type(e['size']) is not int or e['size'] < 0
                                    or not isinstance(e['sha256'], str) or not HEX.fullmatch(e['sha256'])):
            raise ValueError('invalid distribution inventory file: ' + path)
        expected[path] = {k: v for k, v in e.items() if k != 'path'}
    for path in expected:
        if '/' in path and expected.get(path.rsplit('/', 1)[0], {}).get('kind') != 'dir':
            raise ValueError('distribution inventory parent is not a listed directory: ' + path)
    files = sum(e['kind'] == 'file' for e in expected.values())
    if manifest(expected) != inventory['manifest_sha256'] or record.get('files', files) != files:
        raise ValueError('distribution inventory does not yield its recorded manifest')
    return {'pin': pin, 'archive': {'file': match[2], 'source': archive['url'], 'size_bytes': archive['size'],
                                    'sha256': archive['sha256']},
            'inventory': expected,
            'summary': {'method': INVENTORY_METHOD, 'entries': len(expected), 'manifest_sha256': inventory['manifest_sha256']}}


def supplier_account(raw):
    """Dispatch on the account's format: the npm acquisition authorization or the canonical distribution record."""
    record = _load(raw)
    form = record.get('format', NPM_FORM)  # earlier npm acquisition fixtures carry no format field
    if form == NPM_FORM:
        return NPM_FORM, _npm_facts(record)
    if form == DISTRIBUTION_FORM:
        return DISTRIBUTION_FORM, _distribution_facts(record)
    raise ValueError('unsupported supplier account format: ' + repr(form))


def distribution_facts(raw):
    """The canonical distribution record's facts; refuses any other account form."""
    form, facts = supplier_account(raw)
    if form != DISTRIBUTION_FORM:
        raise ValueError('not a canonical distribution record')
    return facts


def comparable(entries):
    """Bundle inventory entries reduced to what the distribution inventory states."""
    return {p: {'kind': e['kind'], 'mode': e['mode'], **({'size': e['size'], 'sha256': e['sha256']} if e['kind'] == 'file' else {})}
            for p, e in entries.items()}


def _check_inventory(entries, expected):
    observed = comparable(entries)
    differing = sorted(p for p in observed.keys() | expected.keys() if observed.get(p) != expected.get(p))
    if differing:
        raise ValueError('bundled supplier differs from the distribution record inventory: ' + differing[0])


def _account(form, raw, facts):
    if form == NPM_FORM:
        return {'path': ACQUISITION_FILE, 'sha256': hashlib.sha256(raw).hexdigest()}
    return {'path': DISTRIBUTION_FILE, 'sha256': hashlib.sha256(raw).hexdigest(), 'form': DISTRIBUTION_FORM,
            'acquirer': NOT_RECORDED, 'authorization': NOT_RECORDED}


def _correspondence(form, entries, facts):
    files = sum(e['kind'] == 'file' for e in entries.values())
    if form == NPM_FORM:
        return {'method': METHOD, 'files': files, 'file_manifest_sha256': manifest(entries)}
    return {'method': PACKAGE_METHOD, 'files': files, 'file_manifest_sha256': manifest(entries),
            'inventory': facts['summary']}


def _read_account(path):
    with selected_file(path) as stream:
        raw = stream.read(1_048_577)
    if len(raw) > 1_048_576:
        raise ValueError('supplier account record too large')
    return raw


def identify_supplier(inv, archive, account):
    entries = supplier_entries(inv)
    raw = _read_account(account)
    form, facts = supplier_account(raw)
    # npm: the tree sits under the package's vendor directory, whose member mode is compared with
    # the bundled root. Release package: the tree is at the archive root with no root member; the
    # record states the container mode is not a supplier member, so it is not compared.
    prefix = TAR_ROOT if form == NPM_FORM else ''
    with selected_file(archive) as stream:
        size, digest = 0, hashlib.sha256()
        while chunk := stream.read(1 << 20):
            digest.update(chunk); size += len(chunk)
        if (size, digest.hexdigest()) != (facts['archive']['size_bytes'], facts['archive']['sha256']):
            raise ValueError('supplier archive contradicts acquisition record')
        stream.seek(0)
        files, directories, seen = {}, set(), set()
        with tarfile.open(fileobj=stream, mode='r:gz') as tar:
            for member in tar:
                name = member.name.rstrip('/') if prefix else member.name
                if prefix:
                    if name != prefix and not name.startswith(prefix + '/'):
                        continue  # platform package metadata outside the vendor tree
                    relative = '' if name == prefix else name[len(prefix) + 1:]
                else:
                    relative = name[:-1] if member.isdir() and name.endswith('/') else name
                    if not relative:
                        raise ValueError('duplicate or invalid vendor archive path')
                if relative in seen or relative and any(p in ('', '.', '..') for p in relative.split('/')):
                    raise ValueError('duplicate or invalid vendor archive path')
                seen.add(relative)
                if not member.isfile() and not member.isdir():
                    raise ValueError('supplier archive link or special file refused')
                if not relative:
                    if not member.isdir():
                        raise ValueError('archive supplier root is not a directory')
                    root = next(e for e in inv['entries'] if e['path'] == ROOT)
                    if root['mode'] != member.mode:
                        raise ValueError('supplier root mode differs from archive')
                    continue
                observed = entries.get(relative)
                if observed is None or observed['mode'] != member.mode:
                    raise ValueError('supplier archive path or mode differs: ' + relative)
                if member.isdir():
                    if observed['kind'] != 'dir':
                        raise ValueError('supplier archive directory differs: ' + relative)
                    directories.add(relative)
                    continue
                source = tar.extractfile(member)
                h = hashlib.sha256()
                with source:
                    while chunk := source.read(1 << 20):
                        h.update(chunk)
                if observed['kind'] != 'file' or (observed['size'], observed['sha256']) != (member.size, h.hexdigest()):
                    raise ValueError('supplier bytes differ from archive: ' + relative)
                files[relative] = observed
        required_dirs = {p.rsplit('/', 1)[0] for p in files if '/' in p}
        for p in list(required_dirs):
            while '/' in p:
                p = p.rsplit('/', 1)[0]; required_dirs.add(p)
        if set(files) != {p for p, e in entries.items() if e['kind'] == 'file'} or directories | required_dirs != {p for p, e in entries.items() if e['kind'] == 'dir'}:
            raise ValueError('bundled supplier has extra or missing archive content')
    if form == DISTRIBUTION_FORM:
        _check_inventory(entries, facts['inventory'])
    result = {'pin': facts['pin'], 'archive': facts['archive']}
    result.update(bundled=True, root=ROOT, standing='unqualified-development',
                  acquisition=_account(form, raw, facts),
                  correspondence=_correspondence(form, entries, facts), binding=BINDING)
    return result, raw


def check_supplier(supplier, inv, folder):
    entries = supplier_entries(inv)
    path = supplier['acquisition']['path']
    if path not in (ACQUISITION_FILE, DISTRIBUTION_FILE):
        raise ValueError('unknown retained supplier account')
    raw = _read_account(folder / path)
    if hashlib.sha256(raw).hexdigest() != supplier['acquisition']['sha256']:
        raise ValueError('stored supplier acquisition digest differs')
    form, facts = supplier_account(raw)
    if supplier['acquisition'] != _account(form, raw, facts):
        raise ValueError('retained supplier account differs from its recorded form')
    if any(supplier[k] != facts[k] for k in ('pin', 'archive')):
        raise ValueError('supplier provenance differs from stored acquisition')
    if form == DISTRIBUTION_FORM:
        _check_inventory(entries, facts['inventory'])
    if supplier['correspondence'] != _correspondence(form, entries, facts):
        raise ValueError('supplier correspondence differs from inventoried bundle')
