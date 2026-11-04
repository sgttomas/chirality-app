#!/usr/bin/env python3
"""Transitive macOS arm64 runtime dependency notice inventory: preparation, not bundled coverage.

`generate` resolves the target/feature-selected dependency INPUT graph with an offline `cargo tree`
(normal edges, no proc-macros, aarch64-apple-darwin) and reads each exact locked .crate archive in a
prepared Cargo home. That graph is what Cargo would compile for these features; it is not an
observation of final linked contents.

`check` (default) needs no Cargo. It cannot re-resolve the graph; it verifies the generation
receipt's canonical member-set digests against the rows (so dropped or added rows fail), every
row against Cargo.lock (version, checksum, source kind), the npm runtime closure recomputed from
package-lock.json, and received-upstream-text associations against a fixed allowlist.
`check --cargo-home` additionally re-resolves the graph and re-reads every archive.
Never fetches, builds or executes dependency code.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tarfile
import tomllib

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
FORMAT = 'chirality.app.transitive-runtime-notices/2'
TARGET = 'aarch64-apple-darwin'
FEATURES = 'custom-protocol,distribution-successor'
EDGES = 'normal,no-proc-macro'
COMMAND = ['cargo', 'tree', '--offline', '--locked', '--target', TARGET, '--edges', EDGES,
           '--features', FEATURES, '--prefix', 'none', '--format', '{p}|{l}']
BASIS = ('app/src-tauri/Cargo.toml', 'app/src-tauri/Cargo.lock', 'app/package.json', 'app/package-lock.json')
INDEX = HERE / 'transitive-index.json'
WORK = 'execution/PKG-01/DEL-01-06/Work/supplier-notice-associations'
OBJC2_METADATA = WORK + '/macos-runtime-license-metadata.json'
# The ONLY received upstream text a row may reference, keyed by the repository it belongs to.
RECEIVED_TEXTS = {'https://github.com/madsmtm/objc2': WORK + '/approved-receipt-20261102/sources/objc2/LICENSE.md'}
NOTICE_NAME = re.compile(r'^(licen[cs]e|copying|notice|copyright|unlicense)', re.I)
NATIVE = re.compile(r'\.(c|cc|cpp|cxx|h|hpp|S|s|asm)$')
TEXT_KINDS = {'archive-member', 'received-upstream-text', 'missing', 'direct-index-archive', 'installed-tree-only'}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git_blob(raw):
    return hashlib.sha1(b'blob %d\0' % len(raw) + raw).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def basis(repo):
    return {p: sha((repo / p).read_bytes()) for p in BASIS}


def member_digests(cargo_rows, npm_rows):
    return {'cargo': sha(canonical(sorted([r['package'], r['version'], r['source']] for r in cargo_rows))),
            'npm': sha(canonical(sorted([r['package'], r['version'], r['integrity']] for r in npm_rows)))}


def cargo_lock(repo):
    return {(p['name'], p['version']): p for p in tomllib.loads((repo / 'app/src-tauri/Cargo.lock').read_text())['package']}


def lock_reachable(repo, members):
    """Members reachable from the workspace root through Cargo.lock edges restricted to `members`.

    Lock edges include every dependency kind and platform, so this rejects unreachable added rows
    but cannot prove target/feature selection; only `check --cargo-home` re-resolves that.
    """
    packages = tomllib.loads((repo / 'app/src-tauri/Cargo.lock').read_text())['package']
    by_name = {}
    for p in packages:
        by_name.setdefault(p['name'], []).append(p['version'])
    def target(dep):
        name, *rest = dep.split()
        return (name, rest[0] if rest else by_name[name][0])
    edges = {(p['name'], p['version']): [target(d) for d in p.get('dependencies', [])] for p in packages}
    roots = [k for k in members if 'source' not in next(p for p in packages if (p['name'], p['version']) == k)]
    seen, stack = set(), list(roots)
    while stack:
        key = stack.pop()
        if key in seen or key not in members:
            continue
        seen.add(key)
        stack.extend(edges[key])
    return seen


def cargo_runtime(repo, cargo_home):
    """Exact (name, version) -> declared license for the target/feature-selected input graph."""
    env = dict(os.environ, CARGO_HOME=str(cargo_home), CARGO_NET_OFFLINE='true')
    out = subprocess.run(COMMAND, cwd=repo / 'app/src-tauri', env=env, capture_output=True, text=True, check=True).stdout
    found = {}
    for line in out.splitlines():
        line = line.replace(' (*)', '').strip()
        if line:
            package, license = line.split('|', 1)
            name, version = package.split()[:2]
            found[(name, version.lstrip('v'))] = license
    return found


def npm_runtime(repo):
    """Non-dev closure from package-lock.json; unsupported or missing lookups refuse."""
    packages = json.loads((repo / 'app/package-lock.json').read_bytes())['packages']
    found, stack = {}, [('', name) for name in packages['']['dependencies']]
    while stack:
        parent, name = stack.pop()
        key = 'node_modules/' + name
        require((parent + '/' if parent else '') + 'node_modules/' + name not in packages or not parent,
                'nested npm lookup is unsupported: ' + parent + ' -> ' + name)
        require(key in packages, 'npm runtime dependency has no flat lock entry (unsupported lookup): ' + name)
        if key in found:
            continue
        locked = packages[key]
        require(not locked.get('dev') and isinstance(locked.get('integrity'), str) and locked.get('version'),
                'npm runtime entry is dev-only or lacks version/integrity: ' + name)
        require(not {'optionalDependencies', 'peerDependenciesMeta', 'bundleDependencies', 'bundledDependencies', 'link'} & set(locked),
                'unsupported npm lock feature: ' + name)
        found[key] = {'package': name, 'version': locked['version'], 'integrity': locked['integrity'],
                      'declared_license': locked.get('license')}
        # Required peers are installed by the lock as well; follow them so none is silently omitted.
        stack.extend((key, dep) for field in ('dependencies', 'peerDependencies') for dep in locked.get(field) or {})
    return sorted(found.values(), key=lambda e: e['package'])


def known_objc2_blobs(repo):
    metadata = json.loads((repo / OBJC2_METADATA).read_bytes())
    return {a['vcs_revision']: a['git_blob_sha1'] for a in metadata['crate_associations']}


def received_text(repo, entry):
    """Validate the association from fixed data BEFORE opening anything; never a caller-chosen path."""
    text = entry['text']
    require(set(text) == {'kind', 'repository', 'path', 'git_blob_sha1', 'vcs_revision', 'path_in_vcs'},
            'unknown received-text fields')
    allowed = RECEIVED_TEXTS.get(text['repository'])
    require(allowed is not None and text['path'] == allowed, 'received text path is not the allowed retained source')
    relative = PurePosixPath(text['path'])
    require(not relative.is_absolute() and '..' not in relative.parts, 'received text path must be repo-relative')
    known = known_objc2_blobs(repo)
    require(known.get(text['vcs_revision']) == text['git_blob_sha1'], 'revision has no known received-text blob')
    target = repo / text['path']
    require(not target.is_symlink() and target.resolve().is_relative_to(repo.resolve()), 'received text escapes the repository')
    require(git_blob(target.read_bytes()) == text['git_blob_sha1'], 'received upstream text differs')


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


def archive_path(cargo_home, name, version):
    hits = [c / f'{name}-{version}.crate' for c in sorted((Path(cargo_home) / 'registry/cache').iterdir())
            if (c / f'{name}-{version}.crate').exists()]
    require(len(hits) == 1, 'exact cached archive unavailable/ambiguous: ' + name)
    return hits[0]


def generate(cargo_home, node_modules=None, repo=REPO):
    lock, known = cargo_lock(repo), known_objc2_blobs(repo)
    cargo = []
    for (name, version), license in sorted(cargo_runtime(repo, cargo_home).items()):
        locked = lock[(name, version)]
        if 'source' not in locked:
            cargo.append({'package': name, 'version': version, 'source': 'path', 'declared_license': license})
            continue
        path = archive_path(cargo_home, name, version)
        require(sha(path.read_bytes()) == locked['checksum'], 'cached archive differs from Cargo.lock: ' + name)
        notices, native, vcs, manifest, readme = read_crate(path, name, version)
        entry = {'package': name, 'version': version, 'source': 'registry', 'archive_sha256': locked['checksum'],
                 'declared_license': license, 'notice_members': notices, 'native_source_paths': native}
        revision, repository = vcs.get('git', {}).get('sha1'), manifest.get('repository', '').rstrip('/')
        if notices:
            entry['text'] = {'kind': 'archive-member'}
        elif repository in RECEIVED_TEXTS and revision in known and b'../../LICENSE.md' in readme:
            entry['text'] = {'kind': 'received-upstream-text', 'repository': repository, 'path': RECEIVED_TEXTS[repository],
                             'git_blob_sha1': known[revision], 'vcs_revision': revision, 'path_in_vcs': vcs.get('path_in_vcs')}
        else:
            entry['text'] = {'kind': 'missing', 'repository': repository, 'vcs_revision': revision,
                             'path_in_vcs': vcs.get('path_in_vcs')}
        cargo.append(entry)
    direct = {c['package']: c for c in json.loads((HERE / 'index.json').read_bytes())['components'] if c['ecosystem'] == 'npm'}
    npm = []
    for row in npm_runtime(repo):
        component = direct.get(row['package'])
        if component and component['version'] == row['version'] and component['source']['integrity'] == row['integrity']:
            row['text'] = {'kind': 'direct-index-archive', 'notices': [n['sha256'] for n in component['notices']]}
        else:
            files = []
            if node_modules:
                folder = Path(node_modules) / row['package']
                files = [{'file': f.name, 'sha256': sha(f.read_bytes())} for f in sorted(folder.iterdir())
                         if f.is_file() and NOTICE_NAME.match(f.name)]
            row['text'] = {'kind': 'installed-tree-only' if files else 'missing', 'installed_notice_files': files,
                           'limit': 'unverified: installed copy only; lock tarball not available locally'}
        npm.append(row)
    cargo_version = subprocess.run(['cargo', '--version'], capture_output=True, text=True, check=True).stdout.strip()
    return {'format': FORMAT, 'target': TARGET, 'features': FEATURES, 'edges': EDGES, 'source_basis': basis(repo),
            'generation': {'command': COMMAND, 'cargo_version': cargo_version, 'member_set_sha256': member_digests(cargo, npm),
                           'limit': 'consistency binding of the generated member set; only `check --cargo-home` re-resolves it'},
            'scope': 'target/feature-selected dependency input graph (build/dev/proc-macro and other-platform crates '
                     'excluded); not an observation of linked contents, bundled coverage, licence election or legal approval',
            'cargo': cargo, 'npm': npm}


def check(index_path=INDEX, repo=REPO, cargo_home=None):
    index = json.loads(Path(index_path).read_bytes())
    require(set(index) == {'format', 'target', 'features', 'edges', 'source_basis', 'generation', 'scope', 'cargo', 'npm'}
            and index['format'] == FORMAT and index['target'] == TARGET and index['features'] == FEATURES
            and index['edges'] == EDGES and index['generation']['command'] == COMMAND, 'unknown transitive index shape')
    require(index['source_basis'] == basis(repo), 'manifests/locks changed; regenerate with `transitive.py generate`')
    require(index['generation']['member_set_sha256'] == member_digests(index['cargo'], index['npm']),
            'member set differs from the generation receipt (dropped, added or altered rows)')
    lock = cargo_lock(repo)
    seen = set()
    for entry in index['cargo']:
        key = (entry['package'], entry['version'])
        require(key not in seen and key in lock, 'unlocked or duplicate crate: ' + key[0])
        seen.add(key)
        locked = lock[key]
        require(entry['source'] == ('registry' if 'source' in locked else 'path'), 'source kind contradicts Cargo.lock: ' + key[0])
        if entry['source'] == 'path':
            require(set(entry) == {'package', 'version', 'source', 'declared_license'}, 'path row carries registry fields')
            continue
        require(entry['archive_sha256'] == locked['checksum'], 'crate checksum differs from lock: ' + key[0])
        kind = entry['text']['kind']
        require(kind in ('archive-member', 'received-upstream-text', 'missing'), 'unknown cargo text kind')
        require((kind == 'archive-member') == bool(entry['notice_members']), 'text kind contradicts members')
        if kind == 'received-upstream-text':
            received_text(repo, entry)
    require(lock_reachable(repo, seen) == seen, 'crate row is unreachable from the workspace root through Cargo.lock')
    expected_npm = npm_runtime(repo)
    require([[r['package'], r['version'], r['integrity'], r['declared_license']] for r in expected_npm] ==
            [[r['package'], r['version'], r['integrity'], r['declared_license']] for r in index['npm']],
            'npm runtime closure differs from package-lock.json')
    direct = json.loads((HERE / 'index.json').read_bytes())['components']
    direct_npm = {c['package']: c for c in direct if c['ecosystem'] == 'npm'}
    for row in index['npm']:
        require(row['text']['kind'] in TEXT_KINDS, 'unknown npm text kind')
        if row['text']['kind'] == 'direct-index-archive':
            component = direct_npm.get(row['package'])
            require(component and component['version'] == row['version'] and component['source']['integrity'] == row['integrity']
                    and row['text']['notices'] == [n['sha256'] for n in component['notices']],
                    'npm row does not match the direct archive-verified index: ' + row['package'])
    for component in direct:
        if component['ecosystem'] == 'cargo':
            require((component['package'], component['version']) in seen, 'direct crate missing: ' + component['package'])
    if cargo_home is not None:
        resolved = cargo_runtime(repo, cargo_home)
        require(set(resolved) == seen, 're-resolved graph differs from the index member set')
        for entry in (e for e in index['cargo'] if e['source'] == 'registry'):
            path = archive_path(cargo_home, entry['package'], entry['version'])
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
            'missing_or_unverified': [f"{e['package']} {e['version']} ({e['text']['kind']})" for e in registry + index['npm']
                                      if e['text']['kind'] in ('missing', 'installed-tree-only')],
            'native_source_paths': {e['package']: e['native_source_paths'] for e in registry if e['native_source_paths']},
            'member_set_sha256': index['generation']['member_set_sha256'],
            'standing': 'dependency input inventory; not linked-content observation, bundled coverage or legal approval'}


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
