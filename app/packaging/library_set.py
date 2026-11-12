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
packages are missing, extra or differ; 2 when an input is refused. Reads only; writes nothing.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
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


def no_link_ancestry(path):
    path = Path(os.path.abspath(path))
    for parent in (path, *path.parents):
        require(not parent.is_symlink(), f'symbolic link refused: {parent}')
    return path


def read_file(path):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        before = os.fstat(fd)
        require(stat.S_ISREG(before.st_mode), f'not a regular file: {path}')
        chunks = []
        while chunk := os.read(fd, 1 << 20):
            chunks.append(chunk)
        after = os.fstat(fd)
        require((before.st_size, before.st_mtime_ns) == (after.st_size, after.st_mtime_ns), f'changed while read: {path}')
        return b''.join(chunks)
    finally:
        os.close(fd)


def read_package(folder):
    """Every file of one package folder: relative path -> bytes. Links and special files refused."""
    files = {}
    for directory, subdirectories, names in os.walk(folder, followlinks=False):
        for name in subdirectories + names:
            path = Path(directory) / name
            mode = os.lstat(path).st_mode
            require(not stat.S_ISLNK(mode), f'symbolic link refused: {path}')
            require(stat.S_ISDIR(mode) or stat.S_ISREG(mode), f'special file refused: {path}')
            require('\n' not in name and '\r' not in name, f'line break in a name refused: {path}')
            if stat.S_ISREG(mode):
                files[path.relative_to(folder).as_posix()] = read_file(path)
    return dict(sorted(files.items(), key=lambda item: item[0].encode()))


def revision(files):
    """The App's package revision: app/src-tauri/src/workflow_workspace.rs `from_files`."""
    preimage = bytearray(REVISION_METHOD.encode()); preimage.append(0)
    preimage += len(files).to_bytes(8, 'big')
    for path, raw in sorted(files.items(), key=lambda item: item[0].encode()):
        preimage += len(path.encode()).to_bytes(8, 'big') + path.encode() + len(raw).to_bytes(8, 'big') + raw
    return sha(bytes(preimage))


def tree_digest(packages):
    listing = {name: {path: sha(raw) for path, raw in files.items()} for name, files in packages.items()}
    return sha(json.dumps(listing, sort_keys=True, separators=(',', ':')).encode())


def subfolders(root):
    entries = {}
    for name in os.listdir(root):
        mode = os.lstat(root / name).st_mode
        require(not stat.S_ISLNK(mode), f'symbolic link refused: {root / name}')
        entries[name] = mode
    return entries


def library(library_root):
    root = no_link_ancestry(library_root)
    workflows = root / 'workflows'
    raw_index = read_file(workflows / 'index.json')
    index = json.loads(raw_index)
    require(isinstance(index, dict) and index.get('schema') == INDEX_SCHEMA, 'unknown index schema')
    methods = index.get('methods')
    require(isinstance(methods, list), 'index has no methods list')
    names = [m.get('name') for m in methods if isinstance(m, dict) and m.get('kind') == 'workflow']
    require(all(isinstance(n, str) and n and '/' not in n and n not in ('.', '..') for n in names), 'invalid workflow name in index')
    require(len(names) == len(set(names)), 'duplicate workflow name in index')
    # A skill and a workflow may share a name (3.4.0: drawing-titleblock-page); within a kind they may not.
    kinds_names = [(m.get('kind'), m.get('name')) for m in methods if isinstance(m, dict)]
    require(len(kinds_names) == len(set(kinds_names)), 'duplicate method name within a kind in index')
    entries = subfolders(workflows)
    folders = sorted(n for n, mode in entries.items() if stat.S_ISDIR(mode))
    require(all(stat.S_ISDIR(m) or stat.S_ISREG(m) for m in entries.values()), 'special file in workflows/ refused')
    require(set(folders) == set(names), 'index and folders disagree: index only ' + json.dumps(sorted(set(names) - set(folders)))
            + ', folders only ' + json.dumps(sorted(set(folders) - set(names))))
    packages = {n: read_package(workflows / n) for n in sorted(names)}
    listed = {m['name']: sorted(m.get('resources') or []) for m in methods if isinstance(m, dict) and m.get('kind') == 'workflow'}
    resource_mismatch = {n: {'listed_only': sorted(set(listed[n]) - set(packages[n])),
                             'folder_only': sorted(set(packages[n]) - set(listed[n]))}
                         for n in packages if set(listed[n]) != set(packages[n])}
    return {'index_sha256': sha(raw_index), 'packages': packages, 'resource_mismatch': resource_mismatch,
            'other_methods': len(methods) - len(names)}


def shipped(workflows_dir):
    root = no_link_ancestry(workflows_dir)
    raw_manifest = read_file(root / 'MANIFEST.json')
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
    entries = subfolders(root)
    folders = sorted(n for n, mode in entries.items() if stat.S_ISDIR(mode))
    loose = sorted(n for n, mode in entries.items() if not stat.S_ISDIR(mode) and n != 'MANIFEST.json')
    require(not loose, 'unlisted file beside the packages: ' + json.dumps(loose))
    require(set(folders) == set(listed), 'manifest and tree disagree: manifest only ' + json.dumps(sorted(set(listed) - set(folders)))
            + ', tree only ' + json.dumps(sorted(set(folders) - set(listed))))
    packages = {n: read_package(root / n) for n in sorted(listed)}
    for name, package in listed.items():
        recorded = {f.get('path'): (f.get('bytes'), f.get('sha256')) for f in package.get('files') or []}
        require(len(recorded) == len(package.get('files') or []), f'duplicate file in manifest package {name}')
        actual = {p: (len(raw), sha(raw)) for p, raw in packages[name].items()}
        require(recorded == actual, f'manifest and tree disagree in package {name}')
        if package.get('revision_method') == REVISION_METHOD:
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
