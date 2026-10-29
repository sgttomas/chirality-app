"""Candidate v3's bounded, read-only macOS arm64 archive correspondence.

No extraction, supplier execution, signature verification or custody issuance.
The bundle inventory retains directory metadata; tar correspondence compares
the complete regular-file set, bytes and modes, plus explicit tar directories.
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


def acquisition_facts(raw):
    def unique(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError('duplicate acquisition field')
            value[key] = item
        return value
    record = json.loads(raw, object_pairs_hook=unique)
    subject, acquisition = record['subject'], record['acquisition']
    match = re.fullmatch(r'codex-(\d+\.\d+\.\d+)-darwin-arm64\.tgz', subject['file'])
    if not match or subject['official_source_locator'] != 'https://registry.npmjs.org/@openai/codex/-/' + subject['file']:
        raise ValueError('unsupported supplier archive source or platform')
    digest, size = acquisition['sha256'], acquisition['size_bytes']
    if not isinstance(digest, str) or not re.fullmatch('[0-9a-f]{64}', digest) or type(size) is not int or size <= 0:
        raise ValueError('invalid acquisition size or digest')
    return {'pin': match[1], 'archive': {'file': subject['file'], 'source': subject['official_source_locator'],
                                     'size_bytes': size, 'sha256': digest}}


def identify_supplier(inv, archive, acquisition):
    entries = supplier_entries(inv)
    with selected_file(acquisition) as stream:
        raw = stream.read(1_048_577)
    if len(raw) > 1_048_576:
        raise ValueError('acquisition record too large')
    result = acquisition_facts(raw)
    with selected_file(archive) as stream:
        size, digest = 0, hashlib.sha256()
        while chunk := stream.read(1 << 20):
            digest.update(chunk); size += len(chunk)
        if (size, digest.hexdigest()) != (result['archive']['size_bytes'], result['archive']['sha256']):
            raise ValueError('supplier archive contradicts acquisition record')
        stream.seek(0)
        files, directories, seen = {}, set(), set()
        with tarfile.open(fileobj=stream, mode='r:gz') as tar:
            for member in tar:
                name = member.name.rstrip('/')
                if name != TAR_ROOT and not name.startswith(TAR_ROOT + '/'):
                    continue  # platform package metadata outside the vendor tree
                relative = '' if name == TAR_ROOT else name[len(TAR_ROOT) + 1:]
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
    result.update(bundled=True, root=ROOT, standing='unqualified-development',
                  acquisition={'path': 'supplier-acquisition.json', 'sha256': hashlib.sha256(raw).hexdigest()},
                  correspondence={'method': METHOD, 'files': len(files), 'file_manifest_sha256': manifest(entries)},
                  binding='Archive correspondence only; each examination binds actual supplier configuration and runtime standing.')
    return result, raw


def check_supplier(supplier, inv, folder):
    entries = supplier_entries(inv)
    with selected_file(folder / 'supplier-acquisition.json') as stream:
        raw = stream.read(1_048_577)
    if hashlib.sha256(raw).hexdigest() != supplier['acquisition']['sha256']:
        raise ValueError('stored supplier acquisition digest differs')
    facts = acquisition_facts(raw)
    if any(supplier[k] != facts[k] for k in ('pin', 'archive')):
        raise ValueError('supplier provenance differs from stored acquisition')
    if supplier['correspondence'] != {'method': METHOD, 'files': sum(e['kind'] == 'file' for e in entries.values()),
                                      'file_manifest_sha256': manifest(entries)}:
        raise ValueError('supplier correspondence differs from inventoried bundle')
