#!/usr/bin/env python3
"""Compare the shipped workflows with the selected Library's whole workflow set.

Release target exit criterion 10: "the workflows it ships are every workflow of the selected
Library"; DEL-01-06 AC-001 for the inventory comparison.

  compare --library-root DIR --workflows DIR

`--library-root` is an extracted Library release (it holds `workflows/index.json`, schema
`chirality-method-index/v1`). `--workflows` is either the source `production_workflows` folder or
a built package's `Contents/Resources/workflows`; both hold `MANIFEST.json` and one folder per
shipped package.

A package is compared as its whole folder, every file byte for byte. That is the structure the
shipped manifest implies: each package lists every file of its folder with size and SHA-256, and
its revision (`chirality.app.workflow-package.sha256/v1`, app/src-tauri/src/workflow_workspace.rs)
is computed over every file the folder holds. The Library index's `resources` list is
cross-checked against each Library folder and any disagreement is reported.

Exit 0 only when the shipped set equals the Library's whole workflow set byte for byte; 1 when
packages are missing, extra or differ; 2 when an input is refused. Every directory it traverses,
from `/` down, is opened without following a link, and every file is read through a descriptor
opened the same way: a link at any level, a special file, a name with a line break and any entry
it cannot list, open or read refuse the comparison; nothing is skipped. Each directory is listed
again after its content is read, and the same names and file identities (device, inode, size,
modification time) are required. A whole-tree identity snapshot of each side, the index and
manifest included, is taken before any content is read and again after all of it, and the two
must be equal. Index entries must have a known kind, a plain name and, for workflows, a list of
plain relative resource paths. Every shipped package must
carry the known revision method and the revision recomputed from its tree; an unknown or missing
method, or another revision, refuses. Reads only; writes nothing.

Limits: this is an operator-run check on stable inputs. It is built so that an observation that was
not made, that failed, or that is incomplete cannot come out as success, and so that drift and
mistakes are caught. It is not built to withstand a writer changing the inputs during the run (the
snapshots catch ordinary changes, not a writer who restores identities), nor someone with write
access forging inputs.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys

INDEX_SCHEMA = 'chirality-method-index/v1'
REVISION_METHOD = 'chirality.app.workflow-package.sha256/v1'


class Refused(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Refused(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


DIR_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
FILE_FLAGS = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK


def _os(what, call, *args, **kwargs):
    """Every filesystem error refuses the comparison; nothing unreadable is skipped."""
    try:
        return call(*args, **kwargs)
    except OSError as error:
        raise Refused(f'{what}: {type(error).__name__} (unreadable, untraversable or linked)') from error


def open_dir(path):
    """Open an absolute directory one component at a time from '/', refusing a link at any level."""
    path = Path(os.path.abspath(path))
    fd = _os(str(path), os.open, '/', DIR_FLAGS)
    try:
        for part in path.parts[1:]:
            child = _os(str(path), os.open, part, DIR_FLAGS, dir_fd=fd)
            os.close(fd)
            fd = child
    except BaseException:
        os.close(fd)
        raise
    return fd


def open_child_dir(fd, name, where):
    info = _os(where, os.stat, name, dir_fd=fd, follow_symlinks=False)
    require(not stat.S_ISLNK(info.st_mode), f'symbolic link refused: {where}')
    require(stat.S_ISDIR(info.st_mode), f'not a directory: {where}')
    child = _os(where, os.open, name, DIR_FLAGS, dir_fd=fd)
    require((os.fstat(child).st_dev, os.fstat(child).st_ino) == (info.st_dev, info.st_ino), f'changed while read: {where}')
    return child


def read_file(fd, name, where, expected=None):
    """One regular file relative to a directory descriptor, never following a link. With
    `expected` (the directory listing's identity), the opened file must be that same file."""
    leaf = _os(where, os.open, name, FILE_FLAGS, dir_fd=fd)
    try:
        before = os.fstat(leaf)
        require(stat.S_ISREG(before.st_mode), f'not a regular file: {where}')
        if expected is not None:
            require((before.st_mode, before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) == expected,
                    f'changed while read: {where}')
        chunks = []
        while chunk := _os(where, os.read, leaf, 1 << 20):
            chunks.append(chunk)
        after = os.fstat(leaf)
        require((before.st_size, before.st_mtime_ns) == (after.st_size, after.st_mtime_ns), f'changed while read: {where}')
        return b''.join(chunks)
    finally:
        os.close(leaf)


def identities(fd, where):
    """Names and identities (mode, device, inode, size, modification time) of one directory's
    entries; a link or special entry refuses."""
    names = sorted(_os(where, os.listdir, fd), key=str.encode)
    entries = {}
    for name in names:
        require('\n' not in name and '\r' not in name, f'line break in a name refused: {where}/{name}')
        info = _os(f'{where}/{name}', os.stat, name, dir_fd=fd, follow_symlinks=False)
        require(not stat.S_ISLNK(info.st_mode), f'symbolic link refused: {where}/{name}')
        require(stat.S_ISDIR(info.st_mode) or stat.S_ISREG(info.st_mode), f'special file refused: {where}/{name}')
        entries[name] = (info.st_mode, info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns)
    return entries


def listing(fd, where):
    return {name: identity[0] for name, identity in identities(fd, where).items()}


def unchanged_since(fd, where, before):
    """Listing a directory again after reading its content must give the same names and identities."""
    require(identities(fd, where) == before, f'changed while read: {where}')


def snapshot(fd, where):
    """One whole-tree identity snapshot: every directory's names and every entry's mode, device,
    inode, size and modification time, keyed by relative path ('.' for the root itself). Taken
    before any content is read and again after all of it; the two must be equal."""
    root = os.fstat(fd)
    found = {'.': (root.st_mode, root.st_dev, root.st_ino, root.st_size, root.st_mtime_ns)}
    def visit(dir_fd, prefix, place):
        for name, identity in identities(dir_fd, place).items():
            found[prefix + name] = identity
            if stat.S_ISDIR(identity[0]):
                child = open_child_dir(dir_fd, name, f'{place}/{name}')
                try:
                    visit(child, prefix + name + '/', f'{place}/{name}')
                finally:
                    os.close(child)
    visit(fd, '', where)
    return found


def same_snapshot(fd, where, before):
    require(snapshot(fd, where) == before, f'changed while read: {where} (whole-tree identities differ)')


NAME = re.compile(r'[A-Za-z0-9][A-Za-z0-9._-]*')
KINDS = ('workflow', 'skill')


def valid_method(m):
    """Kind and name of the expected values; a workflow's resources a list of plain relative paths."""
    if not (isinstance(m, dict) and m.get('kind') in KINDS and isinstance(m.get('name'), str) and NAME.fullmatch(m['name'])):
        return False
    resources = m.get('resources')
    if m['kind'] == 'workflow' or 'resources' in m:
        return (isinstance(resources, list) and all(isinstance(r, str) and r and not r.startswith('/')
                and all(part not in ('', '.', '..') for part in r.split('/')) for r in resources))
    return True


def read_package(parent_fd, name, where):
    """Every file of one package folder: relative path -> bytes. Each directory traversed is
    opened without following links; any error refuses."""
    files = {}
    def visit(fd, prefix, place):
        before = identities(fd, place)
        for entry, identity in before.items():
            if stat.S_ISDIR(identity[0]):
                child = open_child_dir(fd, entry, f'{place}/{entry}')
                try:
                    visit(child, prefix + entry + '/', f'{place}/{entry}')
                finally:
                    os.close(child)
            else:
                files[prefix + entry] = read_file(fd, entry, f'{place}/{entry}', identity)
        unchanged_since(fd, place, before)
    top = open_child_dir(parent_fd, name, where)
    try:
        visit(top, '', where)
    finally:
        os.close(top)
    return dict(sorted(files.items(), key=lambda item: item[0].encode()))


def revision(files):
    """The App's package revision: app/src-tauri/src/workflow_workspace.rs `from_files`."""
    preimage = bytearray(REVISION_METHOD.encode()); preimage.append(0)
    preimage += len(files).to_bytes(8, 'big')
    for path, raw in sorted(files.items(), key=lambda item: item[0].encode()):
        preimage += len(path.encode()).to_bytes(8, 'big') + path.encode() + len(raw).to_bytes(8, 'big') + raw
    return sha(bytes(preimage))


def tree_digest(packages):
    files_by_package = {name: {path: sha(raw) for path, raw in files.items()} for name, files in packages.items()}
    return sha(json.dumps(files_by_package, sort_keys=True, separators=(',', ':')).encode())


def library(library_root):
    root_fd = open_dir(library_root)
    try:
        workflows_fd = open_child_dir(root_fd, 'workflows', 'library workflows/')
    finally:
        os.close(root_fd)
    try:
        before = snapshot(workflows_fd, 'library workflows')
        require('index.json' in before, 'library workflows/index.json missing')
        raw_index = read_file(workflows_fd, 'index.json', 'library workflows/index.json', before['index.json'])
        index = json.loads(raw_index)
        require(isinstance(index, dict) and index.get('schema') == INDEX_SCHEMA, 'unknown index schema')
        methods = index.get('methods')
        require(isinstance(methods, list), 'index has no methods list')
        # No index entry is skipped or loosely accepted.
        require(all(valid_method(m) for m in methods), 'malformed index entry')
        names = [m.get('name') for m in methods if isinstance(m, dict) and m.get('kind') == 'workflow']
        require(all(isinstance(n, str) and n and '/' not in n and n not in ('.', '..') for n in names), 'invalid workflow name in index')
        require(len(names) == len(set(names)), 'duplicate workflow name in index')
        # A skill and a workflow may share a name (3.4.0: drawing-titleblock-page); within a kind they may not.
        kinds_names = [(m.get('kind'), m.get('name')) for m in methods if isinstance(m, dict)]
        require(len(kinds_names) == len(set(kinds_names)), 'duplicate method name within a kind in index')
        top = identities(workflows_fd, 'library workflows')
        entries = {n: i[0] for n, i in top.items()}
        folders = sorted(n for n, mode in entries.items() if stat.S_ISDIR(mode))
        require(set(folders) == set(names), 'index and folders disagree: index only ' + json.dumps(sorted(set(names) - set(folders)))
                + ', folders only ' + json.dumps(sorted(set(folders) - set(names))))
        packages = {n: read_package(workflows_fd, n, f'library workflows/{n}') for n in sorted(names)}
        unchanged_since(workflows_fd, 'library workflows', top)
        same_snapshot(workflows_fd, 'library workflows', before)
    finally:
        os.close(workflows_fd)
    listed = {m['name']: sorted(m['resources']) for m in methods if m['kind'] == 'workflow'}
    resource_mismatch = {n: {'listed_only': sorted(set(listed[n]) - set(packages[n])),
                             'folder_only': sorted(set(packages[n]) - set(listed[n]))}
                         for n in packages if set(listed[n]) != set(packages[n])}
    return {'index_sha256': sha(raw_index), 'packages': packages, 'resource_mismatch': resource_mismatch,
            'other_methods': len(methods) - len(names)}


def shipped(workflows_dir):
    root_fd = open_dir(workflows_dir)
    try:
        before = snapshot(root_fd, 'shipped')
        require('MANIFEST.json' in before, 'shipped MANIFEST.json missing')
        raw_manifest = read_file(root_fd, 'MANIFEST.json', 'shipped MANIFEST.json', before['MANIFEST.json'])
        manifest = json.loads(raw_manifest)
        require(isinstance(manifest, dict) and isinstance(manifest.get('packages'), list), 'manifest has no packages list')
        listed = {}
        for package in manifest['packages']:
            name = package.get('name') if isinstance(package, dict) else None
            require(isinstance(name, str) and name and '/' not in name and name not in ('.', '..'), 'invalid package name in manifest')
            require(name not in listed, 'duplicate package name in manifest')
            source = package.get('source_path')
            require(isinstance(source, str) and PurePosixPath(source).parts == ('workflows', name),
                    f'source path outside workflows/: {source}')
            listed[name] = package
        top = identities(root_fd, 'shipped')
        entries = {n: i[0] for n, i in top.items()}
        folders = sorted(n for n, mode in entries.items() if stat.S_ISDIR(mode))
        loose = sorted(n for n, mode in entries.items() if not stat.S_ISDIR(mode) and n != 'MANIFEST.json')
        require(not loose, 'unlisted file beside the packages: ' + json.dumps(loose))
        require(set(folders) == set(listed), 'manifest and tree disagree: manifest only ' + json.dumps(sorted(set(listed) - set(folders)))
                + ', tree only ' + json.dumps(sorted(set(folders) - set(listed))))
        packages = {n: read_package(root_fd, n, f'shipped {n}') for n in sorted(listed)}
        unchanged_since(root_fd, 'shipped', top)
        same_snapshot(root_fd, 'shipped', before)
    finally:
        os.close(root_fd)
    for name, package in listed.items():
        listed_files = package.get('files')
        require(isinstance(listed_files, list) and all(isinstance(f, dict) and set(f) == {'path', 'bytes', 'sha256'} for f in listed_files),
                f'manifest package {name} has no well-formed file list')
        recorded = {f['path']: (f['bytes'], f['sha256']) for f in listed_files}
        require(len(recorded) == len(listed_files), f'duplicate file in manifest package {name}')
        actual = {p: (len(raw), sha(raw)) for p, raw in packages[name].items()}
        require(recorded == actual, f'manifest and tree disagree in package {name}')
        # Never skipped: an unknown or missing method, or a revision other than the recomputed one, refuses.
        require(package.get('revision_method') == REVISION_METHOD, f'unknown or missing revision method in manifest package {name}')
        require(package.get('revision') == revision(packages[name]), f'manifest revision differs from tree in package {name}')
    return {'manifest_sha256': sha(raw_manifest), 'packages': packages}


def compare(library_root, workflows_dir):
    lib, ship = library(library_root), shipped(workflows_dir)
    a, b = lib['packages'], ship['packages']
    differing = []
    for name in sorted(a.keys() & b.keys()):
        if a[name] != b[name]:
            differing.append({'name': name,
                              'changed': sorted(p for p in a[name].keys() & b[name].keys() if a[name][p] != b[name][p]),
                              'library_only': sorted(a[name].keys() - b[name].keys()),
                              'shipped_only': sorted(b[name].keys() - a[name].keys()),
                              'library_revision': revision(a[name]), 'shipped_revision': revision(b[name])})
    missing, extra = sorted(a.keys() - b.keys()), sorted(b.keys() - a.keys())
    equal = not (missing or extra or differing)
    return {'format': 'chirality-library-workflow-set/v1', 'equal': equal,
            'library': {'index_sha256': lib['index_sha256'], 'tree_sha256': tree_digest(a), 'workflows': len(a),
                        'other_methods_not_compared': lib['other_methods'], 'index_resources_differ_from_folder': lib['resource_mismatch']},
            'shipped': {'manifest_sha256': ship['manifest_sha256'], 'tree_sha256': tree_digest(b), 'packages': len(b)},
            'identical': sorted(n for n in a.keys() & b.keys() if a[n] == b[n]),
            'missing': missing, 'extra': extra, 'differing': differing,
            'comparison': 'whole package folder, every file byte for byte'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest='command', required=True)
    cmp = commands.add_parser('compare')
    cmp.add_argument('--library-root', required=True)
    cmp.add_argument('--workflows', required=True)
    args = parser.parse_args(argv)
    try:
        result = compare(args.library_root, args.workflows)
    except (Refused, OSError, ValueError) as error:
        print(json.dumps({'refused': str(error)}), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result['equal'] else 1


if __name__ == '__main__':
    sys.exit(main())
