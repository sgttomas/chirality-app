#!/usr/bin/env python3
"""Development App candidate identity (DEL-09-01 candidate-identity-v1).

Reads an already built, unpackaged App bundle without executing it, computes its
tree identity and writes or checks a candidate identification record. It builds
nothing, launches nothing, opens no examination and establishes no qualification.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import plistlib
import re
import stat
import subprocess
import sys

METHOD = 'chirality.app.bundle-tree.sha256/v1'
FORMAT = 'chirality.app-v4.candidate-identification/v1'
INVENTORY_FORMAT = 'chirality.app-v4.bundle-inventory/v1'
HEX = re.compile(r'[0-9a-f]{64}')
REV = re.compile(r'[0-9a-f]{40}')
LIMITS = [
    'Identifies the exact bundle bytes, modes and structure read at identification; reproducible rebuilding is not claimed.',
    'Unpackaged development build (route native_development): no signing, notarisation, package record or packaged witness.',
    'Ownership, timestamps, extended attributes and ACLs are outside the identity; signatures embedded in files are covered by file bytes.',
    'Descriptor-relative no-follow reads with two equal passes detect ordinary change during reading; they do not establish custody against a concurrent hostile writer.',
    'The Codex supplier is not part of the bundle; each examination record binds its own supplier pin, distribution identity and configuration.',
    'No examination is opened, no App is launched and no candidate qualification, replacement or acceptance follows from this record.',
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def _check_name(name):
    try:
        name.encode('utf-8', 'strict')
    except UnicodeError as error:
        raise ValueError('bundle path is not valid UTF-8') from error
    if name in ('.', '..') or any(c in name for c in '/\\\r\n\0'):
        raise ValueError('bundle path cannot be represented: ' + repr(name))


def _scan_once(root):
    root = Path(os.path.abspath(root))
    for parent in reversed((root, *root.parents)):
        if parent.is_symlink():
            raise ValueError(f'symlink in bundle root ancestry: {parent}')
    if root.suffix != '.app':
        raise ValueError('bundle root must be a .app directory')
    flags = os.O_RDONLY | os.O_NOFOLLOW
    entries = []

    def visit(fd, prefix):
        before = os.fstat(fd)
        with os.scandir(fd) as listing:
            names = sorted((e.name for e in listing), key=lambda n: n.encode('utf-8'))
        for name in names:
            _check_name(name)
            relative = prefix + name
            info = os.stat(name, dir_fd=fd, follow_symlinks=False)
            entry = {'path': relative, 'mode': stat.S_IMODE(info.st_mode)}
            if stat.S_ISLNK(info.st_mode):
                entry.update(kind='symlink', target=os.readlink(name, dir_fd=fd))
            elif stat.S_ISDIR(info.st_mode):
                child = os.open(name, flags | os.O_DIRECTORY, dir_fd=fd)
                try:
                    if os.fstat(child).st_ino != info.st_ino:
                        raise ValueError('directory replaced during identification: ' + relative)
                    entry['kind'] = 'dir'
                    entries.append(entry)
                    visit(child, relative + '/')
                    continue
                finally:
                    os.close(child)
            elif stat.S_ISREG(info.st_mode):
                if info.st_nlink != 1:
                    raise ValueError('hard-linked file refused: ' + relative)
                child = os.open(name, flags | os.O_NONBLOCK, dir_fd=fd)
                try:
                    start = os.fstat(child)
                    if (start.st_dev, start.st_ino) != (info.st_dev, info.st_ino):
                        raise ValueError('file replaced during identification: ' + relative)
                    digest = hashlib.sha256()
                    while chunk := os.read(child, 1 << 20):
                        digest.update(chunk)
                    end = os.fstat(child)
                    if (start.st_size, start.st_mtime_ns, start.st_ctime_ns) != (end.st_size, end.st_mtime_ns, end.st_ctime_ns):
                        raise ValueError('file changed during identification: ' + relative)
                    entry.update(kind='file', size=end.st_size, sha256=digest.hexdigest())
                finally:
                    os.close(child)
            else:
                raise ValueError('special file refused: ' + relative)
            entries.append(entry)
        after = os.fstat(fd)
        if (before.st_mtime_ns, before.st_ctime_ns) != (after.st_mtime_ns, after.st_ctime_ns):
            raise ValueError('directory changed during identification: ' + (prefix or '.'))

    fd = os.open(root, flags | os.O_DIRECTORY)
    try:
        root_mode = stat.S_IMODE(os.fstat(fd).st_mode)
        visit(fd, '')
    finally:
        os.close(fd)
    entries.sort(key=lambda e: e['path'].encode('utf-8'))
    return {'format': INVENTORY_FORMAT, 'method': METHOD, 'root_mode': root_mode, 'entries': entries}


def inventory(root):
    """Two complete passes must agree; the value excludes the root's location."""
    first = _scan_once(root)
    second = _scan_once(root)
    if canonical(first) != canonical(second):
        raise ValueError('bundle changed between identification passes')
    return first


def identity(inv):
    validate_inventory(inv)
    body = {'method': inv['method'], 'root_mode': inv['root_mode'], 'entries': inv['entries']}
    return METHOD + ':' + sha(canonical(body))


def file_manifest(inv):
    """DEL-01-06 PKG §5.2 compatible regular-file manifest; never the identity alone."""
    lines = ''.join(f"{e['sha256']}  {e['path']}\n" for e in inv['entries'] if e['kind'] == 'file')
    return sha(lines.encode('utf-8'))


def validate_inventory(inv):
    if not isinstance(inv, dict) or set(inv) != {'format', 'method', 'root_mode', 'entries'}:
        raise ValueError('inventory fields differ from the method')
    if inv['format'] != INVENTORY_FORMAT or inv['method'] != METHOD:
        raise ValueError('unknown inventory format or method')
    if not isinstance(inv['root_mode'], int) or not 0 <= inv['root_mode'] <= 0o7777:
        raise ValueError('invalid root mode')
    seen = set()
    previous = None
    for e in inv['entries']:
        keys = {'path', 'kind', 'mode'} | {'file': {'size', 'sha256'}, 'symlink': {'target'}, 'dir': set()}.get(e.get('kind'), {'?'})
        if set(e) != keys:
            raise ValueError('invalid inventory entry: ' + repr(e.get('path')))
        path = e['path']
        parts = path.split('/')
        for part in parts:
            _check_name(part)
        if PurePosixPath(path).is_absolute() or path in seen:
            raise ValueError('invalid or duplicate path: ' + repr(path))
        if previous is not None and previous >= path.encode('utf-8'):
            raise ValueError('entries are not in UTF-8 byte order')
        previous = path.encode('utf-8')
        parent = '/'.join(parts[:-1])
        if parent and parent not in seen:
            raise ValueError('missing parent directory: ' + parent)
        if not isinstance(e['mode'], int) or not 0 <= e['mode'] <= 0o7777:
            raise ValueError('invalid mode: ' + path)
        if e['kind'] == 'file' and (not HEX.fullmatch(str(e['sha256'])) or not isinstance(e['size'], int) or e['size'] < 0):
            raise ValueError('invalid file entry: ' + path)
        if e['kind'] == 'symlink' and not isinstance(e['target'], str):
            raise ValueError('invalid link target: ' + path)
        seen.add(path)
    dirs = {e['path'] for e in inv['entries'] if e['kind'] == 'dir'}
    for e in inv['entries']:
        parent = e['path'].rpartition('/')[0]
        if parent and parent not in dirs:
            raise ValueError('parent is not a directory: ' + e['path'])
    return inv


def compare(expected, observed):
    left = {e['path']: e for e in expected['entries']}
    right = {e['path']: e for e in observed['entries']}
    return {'equal': canonical(expected) == canonical(observed),
            'root_mode_equal': expected['root_mode'] == observed['root_mode'],
            'missing': sorted(left.keys() - right.keys()), 'extra': sorted(right.keys() - left.keys()),
            'changed': sorted(p for p in left.keys() & right.keys() if left[p] != right[p])}


def git(repo, *args):
    result = subprocess.run(['git', '-C', str(repo), *args], capture_output=True, check=True,
                            env=dict(os.environ, GIT_NO_LAZY_FETCH='1', GIT_NO_REPLACE_OBJECTS='1'))
    return result.stdout


def verify_export(repo, revision, prefix, export_root):
    """Every tracked file under prefix at revision exists unchanged in the export."""
    tree = git(repo, 'rev-parse', f'{revision}:{prefix}').decode().strip()
    listing = git(repo, 'ls-tree', '-r', '-z', '--full-tree', revision, '--', prefix).split(b'\0')
    count = 0
    for row in filter(None, listing):
        meta, path = row.split(b'\t', 1)
        mode, kind, blob = meta.decode().split()
        if kind != 'blob':
            raise ValueError('unsupported tracked entry: ' + path.decode())
        target = Path(export_root) / path.decode()
        if mode == '120000':
            data = os.readlink(target).encode()
        else:
            data = target.read_bytes()
        if hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest() != blob:
            raise ValueError('exported source differs from revision: ' + path.decode())
        count += 1
    return {'tree': tree, 'tracked_files_verified': count}


def bundle_metadata(root, inv):
    plist_path = Path(root) / 'Contents/Info.plist'
    plist = plistlib.loads(plist_path.read_bytes())
    executable = 'Contents/MacOS/' + plist['CFBundleExecutable']
    entries = {e['path']: e for e in inv['entries']}
    if entries.get(executable, {}).get('kind') != 'file':
        raise ValueError('bundle executable missing: ' + executable)
    return {'name': Path(root).name, 'identifier': plist['CFBundleIdentifier'],
            'version': plist.get('CFBundleShortVersionString') or plist.get('CFBundleVersion'),
            'executable': {'path': executable, 'sha256': entries[executable]['sha256']},
            'info_plist_sha256': entries['Contents/Info.plist']['sha256'],
            'file_manifest_sha256': file_manifest(inv),
            'counts': {k: sum(e['kind'] == k for e in inv['entries']) for k in ('dir', 'file', 'symlink')}}


def make_record(args):
    inv = inventory(args.app)
    build_identity = identity(inv)
    revision = git(args.repo, 'rev-parse', '--verify', args.revision + '^{commit}').decode().strip()
    facts = json.loads(Path(args.build_facts).read_bytes())
    meta = bundle_metadata(args.app, inv)
    inventory_bytes = canonical(inv) + b'\n'
    tool = Path(__file__).read_bytes()
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
        'app_data': {'directory': '~/Library/Application Support/' + meta['identifier'],
                     'present_at_identification': (Path.home() / 'Library/Application Support' / meta['identifier']).exists()},
        'supplier': {'bundled': False, 'binding': 'per examination record configuration (codex_pin, codex_distribution_identity)'},
        'identified_by': {'tool': 'projects/chirality-app-v4/app/examination/candidate_identity/identify.py',
                          'tool_sha256': sha(tool), 'method': METHOD},
        'identified_at': args.identified_at,
        'limits': LIMITS,
    }
    validate_record(record)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=False)
    (out / 'bundle-inventory.json').write_bytes(inventory_bytes)
    (out / 'candidate-identification.json').write_bytes(json.dumps(record, indent=2, ensure_ascii=False).encode() + b'\n')
    return record


def validate_record(record):
    schema_path = Path(__file__).resolve().parents[3] / 'execution/PKG-09/DEL-09-01/Design/candidate-identity-v1/candidate-identification.schema.json'
    from jsonschema import Draft202012Validator
    errors = sorted(Draft202012Validator(json.loads(schema_path.read_text())).iter_errors(record), key=lambda e: list(e.path))
    if errors:
        raise ValueError('record schema: ' + '; '.join(f"{'/'.join(map(str, e.path))}: {e.message}" for e in errors))
    build = record['app_candidate']['build_identity']
    if not build.startswith(METHOD + ':') or not HEX.fullmatch(build.rsplit(':', 1)[1]):
        raise ValueError('build identity does not use the method')
    if record['candidate_key'] != record['app_candidate']['revision'][:10] + '-' + build.rsplit(':', 1)[1][:12]:
        raise ValueError('candidate key does not derive from revision and build identity')
    if record['source']['revision'] != record['app_candidate']['revision']:
        raise ValueError('source and candidate revisions differ')
    if record['app_data']['present_at_identification']:
        raise ValueError('App data directory already exists; the candidate would not start fresh')
    return record


def check(args):
    folder = Path(args.record).parent
    record = json.loads(Path(args.record).read_bytes())
    validate_record(record)
    stored = (folder / record['bundle']['inventory']['path']).read_bytes()
    if sha(stored) != record['bundle']['inventory']['sha256']:
        raise ValueError('stored inventory differs from its recorded digest')
    expected = validate_inventory(json.loads(stored))
    if identity(expected) != record['app_candidate']['build_identity']:
        raise ValueError('stored inventory does not yield the recorded build identity')
    observed = inventory(args.app)
    result = compare(expected, observed)
    result['build_identity'] = identity(observed)
    result['recorded_build_identity'] = record['app_candidate']['build_identity']
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('inventory'); p.add_argument('app')
    p = sub.add_parser('record')
    p.add_argument('--app', required=True); p.add_argument('--repo', required=True)
    p.add_argument('--revision', required=True); p.add_argument('--prefix', default='projects/chirality-app-v4')
    p.add_argument('--export-root', required=True); p.add_argument('--build-facts', required=True)
    p.add_argument('--repository', default='sgttomas/chirality'); p.add_argument('--identified-at', required=True)
    p.add_argument('--out-dir', required=True)
    p = sub.add_parser('check'); p.add_argument('--record', required=True); p.add_argument('--app', required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'inventory':
            inv = inventory(args.app)
            print(json.dumps({'build_identity': identity(inv), 'file_manifest_sha256': file_manifest(inv),
                              'entries': len(inv['entries'])}, indent=2))
            return 0
        if args.command == 'record':
            record = make_record(args)
            print(json.dumps({'candidate_key': record['candidate_key'], 'build_identity': record['app_candidate']['build_identity']}, indent=2))
            return 0
        result = check(args)
        print(json.dumps(result, indent=2))
        return 0 if result['equal'] and result['build_identity'] == result['recorded_build_identity'] else 1
    except (ValueError, OSError, subprocess.CalledProcessError, KeyError) as error:
        print(json.dumps({'error': str(error)}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
