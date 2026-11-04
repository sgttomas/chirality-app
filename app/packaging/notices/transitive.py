#!/usr/bin/env python3
"""Transitive macOS arm64 runtime dependency notice inventory: preparation, not bundled coverage.

`generate` resolves the release-feature runtime graph with an offline `cargo tree` (normal edges,
no proc-macros, aarch64-apple-darwin) and reads each exact locked .crate archive in a prepared
Cargo home. `check` (default) needs no Cargo: it fails closed when manifests/locks moved or the
committed index no longer matches them. Never fetches, builds or executes dependency code.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import tomllib

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
FORMAT = 'chirality.app.transitive-runtime-notices/1'
TARGET = 'aarch64-apple-darwin'
FEATURES = 'custom-protocol,distribution-successor'
EDGES = 'normal,no-proc-macro'
BASIS = ('app/src-tauri/Cargo.toml', 'app/src-tauri/Cargo.lock', 'app/package.json', 'app/package-lock.json')
INDEX = HERE / 'transitive-index.json'
WORK = 'execution/PKG-01/DEL-01-06/Work/supplier-notice-associations'
OBJC2_TEXT = WORK + '/approved-receipt-20261102/sources/objc2/LICENSE.md'
NOTICE_NAME = re.compile(r'^(licen[cs]e|copying|notice|copyright|unlicense)', re.I)
NATIVE = re.compile(r'\.(c|cc|cpp|cxx|h|hpp|S|s|asm)$')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def basis(repo):
    return {p: sha((repo / p).read_bytes()) for p in BASIS}


def cargo_runtime(repo, cargo_home):
    """Exact (name, version) -> declared license for the shipped runtime graph."""
    env = dict(os.environ, CARGO_HOME=str(cargo_home), CARGO_NET_OFFLINE='true')
    out = subprocess.run(['cargo', 'tree', '--offline', '--locked', '--target', TARGET, '--edges', EDGES,
                          '--features', FEATURES, '--prefix', 'none', '--format', '{p}|{l}'],
                         cwd=repo / 'app/src-tauri', env=env, capture_output=True, text=True, check=True).stdout
    found = {}
    for line in out.splitlines():
        line = line.replace(' (*)', '').strip()
        if not line:
            continue
        package, license = line.split('|', 1)
        name, version = package.split()[:2]
        found[(name, version.lstrip('v'))] = license
    return found


def objc2_revisions(repo):
    metadata = json.loads((repo / WORK / 'macos-runtime-license-metadata.json').read_bytes())
    return {a['vcs_revision']: a['git_blob_sha1'] for a in metadata['crate_associations']}


def read_crate(path, name, version):
    with tarfile.open(path) as archive:
        prefix = f'{name}-{version}/'
        members = {m.name: m for m in archive.getmembers()}
        def body(rel):
            member = members.get(prefix + rel)
            return archive.extractfile(member).read() if member is not None and member.isfile() else None
        notices = []
        for full, member in sorted(members.items()):
            rel = full[len(prefix):] if full.startswith(prefix) else None
            if rel and '/' not in rel and member.isfile() and NOTICE_NAME.match(rel):
                raw = archive.extractfile(member).read()
                notices.append({'member': rel, 'size_bytes': len(raw), 'sha256': sha(raw)})
        native = sorted(full[len(prefix):] for full, m in members.items() if m.isfile() and NATIVE.search(full))
        vcs = json.loads(body('.cargo_vcs_info.json') or b'{}')
        manifest = tomllib.loads(body('Cargo.toml').decode())['package']
        readme = body('README.md') or b''
    return notices, native, vcs, manifest, readme


def generate(cargo_home, node_modules=None, repo=REPO):
    cargo_home = Path(cargo_home)
    lock = {(p['name'], p['version']): p for p in tomllib.loads((repo / 'app/src-tauri/Cargo.lock').read_text())['package']}
    caches = sorted((cargo_home / 'registry/cache').iterdir())
    known = objc2_revisions(repo)
    cargo = []
    for (name, version), license in sorted(cargo_runtime(repo, cargo_home).items()):
        locked = lock[(name, version)]
        if 'source' not in locked:
            cargo.append({'package': name, 'version': version, 'source': 'path', 'declared_license': license})
            continue
        path = next(c / f'{name}-{version}.crate' for c in caches if (c / f'{name}-{version}.crate').exists())
        raw = path.read_bytes()
        require(sha(raw) == locked['checksum'], 'cached archive differs from Cargo.lock: ' + name)
        notices, native, vcs, manifest, readme = read_crate(path, name, version)
        entry = {'package': name, 'version': version, 'source': 'registry', 'archive_sha256': locked['checksum'],
                 'declared_license': license, 'notice_members': notices, 'native_source_paths': native}
        revision, repository = vcs.get('git', {}).get('sha1'), manifest.get('repository', '')
        if notices:
            entry['text'] = {'kind': 'archive-member'}
        elif repository.rstrip('/') == 'https://github.com/madsmtm/objc2' and revision in known and b'../../LICENSE.md' in readme:
            entry['text'] = {'kind': 'received-upstream-text', 'path': OBJC2_TEXT, 'git_blob_sha1': known[revision],
                             'vcs_revision': revision, 'path_in_vcs': vcs.get('path_in_vcs')}
        else:
            entry['text'] = {'kind': 'missing', 'repository': repository, 'vcs_revision': revision,
                             'path_in_vcs': vcs.get('path_in_vcs')}
        cargo.append(entry)
    packages = json.loads((repo / 'app/package-lock.json').read_bytes())['packages']
    npm, stack = {}, list(packages['']['dependencies'])
    while stack:
        name = stack.pop(); key = 'node_modules/' + name
        if key in npm or key not in packages:
            continue
        locked = packages[key]; require(not locked.get('dev'), 'runtime walk reached a dev package: ' + name)
        files = []
        if node_modules:
            folder = Path(node_modules) / name
            files = [{'file': f.name, 'sha256': sha(f.read_bytes())} for f in sorted(folder.iterdir())
                     if f.is_file() and NOTICE_NAME.match(f.name)]
        npm[key] = {'package': name, 'version': locked['version'], 'declared_license': locked.get('license'),
                    'integrity': locked['integrity'], 'installed_notice_files': files,
                    'text': {'kind': 'installed-tree-only' if files else 'missing',
                             'limit': 'installed copy; lock tarball integrity not re-verified here'}}
        stack.extend(locked.get('dependencies') or {})
    return {'format': FORMAT, 'target': TARGET, 'features': FEATURES, 'edges': EDGES, 'source_basis': basis(repo),
            'scope': 'shipped runtime graph for the selected release features; build/dev/proc-macro crates excluded; '
                     'preparation inventory, not bundled coverage, licence election or legal approval',
            'cargo': cargo, 'npm': sorted(npm.values(), key=lambda e: e['package'])}


def check(index_path=INDEX, repo=REPO, cargo_home=None):
    index = json.loads(Path(index_path).read_bytes())
    require(set(index) == {'format', 'target', 'features', 'edges', 'source_basis', 'scope', 'cargo', 'npm'}
            and index['format'] == FORMAT and index['target'] == TARGET and index['features'] == FEATURES
            and index['edges'] == EDGES, 'unknown transitive index shape')
    require(index['source_basis'] == basis(repo), 'manifests/locks changed; regenerate with `transitive.py generate`')
    lock = {(p['name'], p['version']): p for p in tomllib.loads((repo / 'app/src-tauri/Cargo.lock').read_text())['package']}
    seen = set()
    for entry in index['cargo']:
        key = (entry['package'], entry['version']); require(key not in seen and key in lock, 'unlocked or duplicate crate')
        seen.add(key)
        if entry['source'] == 'registry':
            require(entry['archive_sha256'] == lock[key]['checksum'], 'crate checksum differs from lock: ' + key[0])
            kind = entry['text']['kind']
            require(kind in ('archive-member', 'received-upstream-text', 'missing'), 'unknown text kind')
            require((kind == 'archive-member') == bool(entry['notice_members']), 'text kind contradicts members')
            if kind == 'received-upstream-text':
                raw = (repo / entry['text']['path']).read_bytes()
                require(hashlib.sha1(b'blob %d\0' % len(raw) + raw).hexdigest() == entry['text']['git_blob_sha1'],
                        'received upstream text differs')
    direct = json.loads((HERE / 'index.json').read_bytes())['components']
    npm = {(e['package'], e['version']) for e in index['npm']}
    for component in direct:
        if component['ecosystem'] == 'cargo':
            require((component['package'], component['version']) in seen, 'direct crate missing: ' + component['package'])
        elif component['ecosystem'] == 'npm':
            require((component['package'], component['version']) in npm, 'direct npm package missing: ' + component['package'])
    if cargo_home is not None:
        caches = sorted((Path(cargo_home) / 'registry/cache').iterdir())
        for entry in (e for e in index['cargo'] if e['source'] == 'registry'):
            path = next(c / f"{entry['package']}-{entry['version']}.crate" for c in caches
                        if (c / f"{entry['package']}-{entry['version']}.crate").exists())
            require(sha(path.read_bytes()) == entry['archive_sha256'], 'cached archive differs: ' + entry['package'])
            require(read_crate(path, entry['package'], entry['version'])[0] == entry['notice_members'],
                    'archive notice members differ: ' + entry['package'])
    return index


def summary(index):
    registry = [e for e in index['cargo'] if e['source'] == 'registry']
    kinds = {}
    for e in registry + index['npm']:
        kinds[e['text']['kind']] = kinds.get(e['text']['kind'], 0) + 1
    return {'cargo_runtime_crates': len(registry), 'npm_runtime_packages': len(index['npm']), 'text_kinds': kinds,
            'missing_text': [f"{e['package']} {e['version']}" for e in registry + index['npm'] if e['text']['kind'] == 'missing'],
            'native_source_paths': {e['package']: e['native_source_paths'] for e in registry if e['native_source_paths']},
            'standing': 'preparation inventory; not bundled coverage, licence election or legal approval'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command')
    g = sub.add_parser('generate'); g.add_argument('--cargo-home', required=True, type=Path)
    g.add_argument('--node-modules', type=Path); g.add_argument('--out', type=Path, default=INDEX)
    c = sub.add_parser('check'); c.add_argument('--cargo-home', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'generate':
            index = generate(args.cargo_home, args.node_modules)
            args.out.write_text(json.dumps(index, indent=1) + '\n')
            check(args.out, cargo_home=args.cargo_home)
        else:
            index = check(cargo_home=getattr(args, 'cargo_home', None))
        print(json.dumps(summary(index), indent=1))
        return 0
    except (ValueError, KeyError, OSError, StopIteration, subprocess.CalledProcessError, tarfile.TarError) as error:
        print(json.dumps({'transitive_index_match': False, 'error': str(error)}), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
