#!/usr/bin/env python3
"""Transitive macOS arm64 runtime dependency notice inventory: preparation, not bundled coverage.

`generate` resolves the target/feature-selected dependency INPUT graph with an offline `cargo tree`
(normal edges, no proc-macros, aarch64-apple-darwin) and reads each exact locked .crate archive in a
prepared Cargo home. That graph is what Cargo would compile for these features; it is not an
observation of final linked contents.

`check` (default) needs no Cargo. It cannot re-resolve the graph; it verifies the generation
receipt's canonical member-set digests against the rows (so dropped or added rows fail), every
row against Cargo.lock (version, checksum, source kind), the npm runtime closure recomputed from
package-lock.json, and received/retained upstream-text associations against fixed source allowlists.
`associate-local` joins retained bytes to the already checked graph without running Cargo;
legacy /2 indexes keep their historical interpretation. New /3 rows carry explicit scope limits.
`check --cargo-home` additionally re-resolves the graph and re-reads every archive.
`associate-npm --npm-cache` re-derives only the npm text rows from the locked tarballs (no Cargo run),
and `check --npm-cache` re-reads them. Never fetches, builds or executes dependency code and never
writes to a cache.
"""
import argparse
import base64
import copy
import importlib.util
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
FORMAT = 'chirality.app.transitive-runtime-notices/3'
LEGACY_FORMAT = 'chirality.app.transitive-runtime-notices/2'
TARGET = 'aarch64-apple-darwin'
FEATURES = 'custom-protocol,distribution-successor'
EDGES = 'normal,no-proc-macro'
COMMAND = ['cargo', 'tree', '--offline', '--locked', '--target', TARGET, '--edges', EDGES,
           '--features', FEATURES, '--prefix', 'none', '--format', '{p}|{l}']
BASIS = ('app/src-tauri/Cargo.toml', 'app/src-tauri/Cargo.lock', 'app/package.json', 'app/package-lock.json')
INDEX = HERE / 'transitive-index.json'
OBJC2_METADATA = 'app/packaging/notices/macos-runtime-license-metadata.json'
# The ONLY received upstream text a row may reference, keyed by the repository it belongs to.
RECEIVED_TEXTS = {'https://github.com/madsmtm/objc2': 'app/packaging/notices/retained/objc2-LICENSE.md'}
NOTICE_NAME = re.compile(r'^(licen[cs]e|copying|notice|copyright|unlicense)', re.I)
NATIVE = re.compile(r'\.(c|cc|cpp|cxx|h|hpp|S|s|asm)$')
LOCAL_ASSOCIATIONS = 'app/packaging/notices/retained-root-associations.json'
LOCAL_ASSOCIATIONS_SHA256 = '9b8b93ef107c0dd80a65cfe248dd0fd9323803cbf4b88747dde698dd4f4af260'
_spec = importlib.util.spec_from_file_location('transitive_notice_files', HERE / 'retained_files.py')
files = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(files)
NPM_TEXT_KINDS = {'missing', 'direct-index-archive', 'installed-tree-only', 'lock-tarball'}
HEX64 = re.compile('[0-9a-f]{64}')


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


def npm_tarball(npm_cache, integrity):
    """Locate a locked tarball by its lock integrity in an npm cache (content-addressed); read-only."""
    algorithm, encoded = integrity.split('-', 1)
    require(algorithm == 'sha512', 'unsupported npm integrity algorithm')
    digest = base64.b64decode(encoded, validate=True)
    path = Path(npm_cache) / '_cacache/content-v2/sha512' / digest.hex()[:2] / digest.hex()[2:4] / digest.hex()[4:]
    raw = path.read_bytes()
    require(hashlib.sha512(raw).digest() == digest, 'cached npm tarball differs from the lock integrity')
    return raw


def npm_notice_members(raw):
    """Root-level licence/notice members of one npm tarball: name -> bytes."""
    import io
    found = {}
    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
        for member in archive.getmembers():
            rel = member.name[len('package/'):] if member.name.startswith('package/') else None
            if rel and '/' not in rel and NOTICE_NAME.match(rel):
                require(member.isfile() and rel not in found, 'npm notice member is not one regular file: ' + rel)
                found[rel] = archive.extractfile(member).read()
    return found


def npm_text(row, component, npm_cache=None, node_modules=None):
    if component and component['version'] == row['version'] and component['source']['integrity'] == row['integrity']:
        notices = [n['sha256'] for n in component['notices']]
        if npm_cache:
            members = npm_notice_members(npm_tarball(npm_cache, row['integrity']))
            require(sorted(sha(v) for v in members.values()) == sorted(notices), 'direct npm notices differ from tarball')
        return {'kind': 'direct-index-archive', 'notices': notices}
    if npm_cache:
        members = npm_notice_members(npm_tarball(npm_cache, row['integrity']))
        return {'kind': 'lock-tarball', 'notice_members': [{'member': name, 'size_bytes': len(raw), 'sha256': sha(raw)}
                                                           for name, raw in sorted(members.items())]}
    files = []
    if node_modules:
        folder = Path(node_modules) / row['package']
        files = [{'file': f.name, 'sha256': sha(f.read_bytes())} for f in sorted(folder.iterdir())
                 if f.is_file() and NOTICE_NAME.match(f.name)]
    return {'kind': 'installed-tree-only' if files else 'missing', 'installed_notice_files': files,
            'limit': 'unverified: installed copy only; lock tarball not available locally'}


def direct_npm(repo=REPO):
    return {c['package']: c for c in json.loads((Path(repo) / 'app/packaging/notices/index.json').read_bytes())['components']
            if c['ecosystem'] == 'npm'}


def associate_npm(npm_cache, index_path=INDEX, repo=REPO):
    """Re-derive only the npm text rows from locked tarballs; the checked Cargo graph is kept as is."""
    index = copy.deepcopy(check(index_path, repo))
    direct = direct_npm(repo)
    for row in index['npm']:
        row['text'] = npm_text(row, direct.get(row['package']), npm_cache)
    return index


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


def local_associations(repo):
    """Reviewed fixed associations; disk/index inputs cannot select a new source path."""
    raw = files.transfer(Path(repo).absolute() / LOCAL_ASSOCIATIONS, retain=True)[0]
    require(sha(raw) == LOCAL_ASSOCIATIONS_SHA256, 'retained-root allowlist differs')
    value = files.parse(raw)
    require(value['format'] == 'retained-root-notice-associations/1', 'unknown local association format')
    return {(a['subject']['package'], a['subject']['version']): a for a in value['associations']}


def local_text(repo, entry, associations, *, prior=False):
    selected = associations.get((entry['package'], entry['version']))
    if selected is None:
        return None
    require(all(entry.get(k) == v for k, v in selected['subject'].items()), 'retained-root crate subject differs')
    if prior:
        require(entry['text'] == selected['prior_locator'], 'retained-root original source locator differs')
    else:
        require(entry['text'] == selected['text'], 'retained-root text association differs')
    # Paths and byte expectations are fixed by the source allowlist before any open.
    for notice in selected['text']['notices']:
        raw, digest, size = files.transfer(Path(repo).absolute() / notice['retained_path'], retain=True)
        require((size, digest, git_blob(raw)) == (notice['size_bytes'], notice['sha256'], notice['git_blob_sha1']),
                'retained-root notice bytes differ')
    return copy.deepcopy(selected['text'])


def associate_local(index_path=INDEX, repo=REPO):
    """Derive only local text associations; retain the previously resolved graph and receipt.

    This is not a new Cargo resolution. The checked legacy index supplies the exact
    graph; current lock/basis/member checks still apply before and after the join.
    """
    index = copy.deepcopy(check(index_path, repo))
    associations = local_associations(repo)
    for entry in index['cargo']:
        if (entry['package'], entry['version']) not in associations:
            continue
        prior = index['format'] == LEGACY_FORMAT
        text = local_text(repo, entry, associations, prior=prior)
        entry['text'] = text
    index['format'] = FORMAT
    return index


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


def generate(cargo_home, node_modules=None, repo=REPO, npm_cache=None):
    lock, known = cargo_lock(repo), known_objc2_blobs(repo)
    associations = local_associations(repo)
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
        if entry['text']['kind'] == 'missing':
            local = local_text(repo, entry, associations, prior=True)
            if local is not None: entry['text'] = local
        cargo.append(entry)
    direct = direct_npm(repo)
    npm = []
    for row in npm_runtime(repo):
        row['text'] = npm_text(row, direct.get(row['package']), npm_cache, node_modules)
        npm.append(row)
    cargo_version = subprocess.run(['cargo', '--version'], capture_output=True, text=True, check=True).stdout.strip()
    return {'format': FORMAT, 'target': TARGET, 'features': FEATURES, 'edges': EDGES, 'source_basis': basis(repo),
            'generation': {'command': COMMAND, 'cargo_version': cargo_version, 'member_set_sha256': member_digests(cargo, npm),
                           'limit': 'consistency binding of the generated member set; only `check --cargo-home` re-resolves it'},
            'scope': 'target/feature-selected dependency input graph (build/dev/proc-macro and other-platform crates '
                     'excluded); not an observation of linked contents, bundled coverage, licence election or legal approval',
            'cargo': cargo, 'npm': npm}


def check(index_path=INDEX, repo=REPO, cargo_home=None, npm_cache=None):
    index = json.loads(Path(index_path).read_bytes())
    require(set(index) == {'format', 'target', 'features', 'edges', 'source_basis', 'generation', 'scope', 'cargo', 'npm'}
            and index['format'] in (FORMAT, LEGACY_FORMAT) and index['target'] == TARGET and index['features'] == FEATURES
            and index['edges'] == EDGES and index['generation']['command'] == COMMAND, 'unknown transitive index shape')
    require(index['source_basis'] == basis(repo), 'manifests/locks changed; regenerate with `transitive.py generate`')
    require(index['generation']['member_set_sha256'] == member_digests(index['cargo'], index['npm']),
            'member set differs from the generation receipt (dropped, added or altered rows)')
    lock = cargo_lock(repo)
    associations = local_associations(repo) if index['format'] == FORMAT else {}
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
        require(kind in ('archive-member', 'received-upstream-text', 'missing') or
                (index['format'] == FORMAT and kind == 'retained-root-texts'), 'unknown cargo text kind')
        require((kind == 'archive-member') == bool(entry['notice_members']), 'text kind contradicts members')
        if kind == 'received-upstream-text':
            received_text(repo, entry)
        if index['format'] == FORMAT:
            selected = local_text(repo, entry, associations)
            require(kind != 'retained-root-texts' or selected is not None, 'retained-root subject is not allowed')
    require(lock_reachable(repo, seen) == seen, 'crate row is unreachable from the workspace root through Cargo.lock')
    expected_npm = npm_runtime(repo)
    require([[r['package'], r['version'], r['integrity'], r['declared_license']] for r in expected_npm] ==
            [[r['package'], r['version'], r['integrity'], r['declared_license']] for r in index['npm']],
            'npm runtime closure differs from package-lock.json')
    direct = json.loads((HERE / 'index.json').read_bytes())['components']
    direct_npm = {c['package']: c for c in direct if c['ecosystem'] == 'npm'}
    for row in index['npm']:
        require(row['text']['kind'] in NPM_TEXT_KINDS, 'unknown npm text kind')
        if row['text']['kind'] == 'direct-index-archive':
            component = direct_npm.get(row['package'])
            require(component and component['version'] == row['version'] and component['source']['integrity'] == row['integrity']
                    and row['text']['notices'] == [n['sha256'] for n in component['notices']],
                    'npm row does not match the direct archive-verified index: ' + row['package'])
        if row['text']['kind'] == 'lock-tarball':
            members = row['text'].get('notice_members')
            require(set(row['text']) == {'kind', 'notice_members'} and isinstance(members, list) and members
                    and all(set(m) == {'member', 'size_bytes', 'sha256'} and isinstance(m['member'], str)
                            and '/' not in m['member'] and NOTICE_NAME.match(m['member'])
                            and type(m['size_bytes']) is int and HEX64.fullmatch(m['sha256']) for m in members)
                    and len({m['member'] for m in members}) == len(members), 'invalid npm tarball notice members: ' + row['package'])
        if npm_cache is not None and row['text']['kind'] in ('lock-tarball', 'direct-index-archive'):
            require(npm_text(row, direct_npm.get(row['package']), npm_cache) == row['text'],
                    'npm tarball notice members differ: ' + row['package'])
    for component in direct:
        if component['ecosystem'] == 'cargo':
            require((component['package'], component['version']) in seen, 'direct crate missing: ' + component['package'])
    if cargo_home is not None:
        resolved = cargo_runtime(repo, cargo_home)
        require(set(resolved) == seen, 're-resolved graph differs from the index member set')
        for entry in (e for e in index['cargo'] if e['source'] == 'registry'):
            path = archive_path(cargo_home, entry['package'], entry['version'])
            require(sha(path.read_bytes()) == entry['archive_sha256'], 'cached archive differs: ' + entry['package'])
            notices, _, vcs, manifest, _ = read_crate(path, entry['package'], entry['version'])
            require(notices == entry['notice_members'], 'archive notice members differ: ' + entry['package'])
            if entry['text']['kind'] == 'retained-root-texts':
                text = entry['text']
                require((manifest.get('repository', '').rstrip('/'), vcs.get('git', {}).get('sha1'), vcs.get('path_in_vcs')) ==
                        (text['repository'], text['vcs_revision'], text['path_in_vcs']), 'retained-root archive source locator differs')
    return index


def summary(index):
    registry = [e for e in index['cargo'] if e['source'] == 'registry']
    kinds = {}
    for e in registry + index['npm']:
        kinds[e['text']['kind']] = kinds.get(e['text']['kind'], 0) + 1
    return {'cargo_runtime_crates': len(registry), 'npm_runtime_packages': len(index['npm']), 'text_kinds': kinds,
            'missing_or_unverified': [f"{e['package']} {e['version']} ({e['text']['kind']})" for e in registry + index['npm']
                                      if e['text']['kind'] in ('missing', 'installed-tree-only', 'retained-root-texts',
                                                               'received-upstream-text')],
            'retained_root_associations': [{'package': e['package'], 'version': e['version'],
                                            'unresolved': e['text']['unresolved'], 'standing': e['text']['standing']}
                                           for e in registry if e['text']['kind'] == 'retained-root-texts'],
            'native_source_paths': {e['package']: e['native_source_paths'] for e in registry if e['native_source_paths']},
            'member_set_sha256': index['generation']['member_set_sha256'],
            'standing': 'dependency input inventory; not linked-content observation, bundled coverage or legal approval'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command')
    g = sub.add_parser('generate'); g.add_argument('--cargo-home', required=True, type=Path)
    g.add_argument('--node-modules', type=Path); g.add_argument('--npm-cache', type=Path)
    g.add_argument('--out', type=Path, default=INDEX)
    c = sub.add_parser('check'); c.add_argument('--cargo-home', type=Path); c.add_argument('--npm-cache', type=Path)
    n = sub.add_parser('associate-npm'); n.add_argument('--npm-cache', type=Path, required=True)
    n.add_argument('--input', type=Path, default=INDEX); n.add_argument('--out', type=Path, default=INDEX)
    a = sub.add_parser('associate-local'); a.add_argument('--input', type=Path, default=INDEX)
    a.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == 'generate':
            index = generate(args.cargo_home, args.node_modules, npm_cache=args.npm_cache)
            args.out.write_text(json.dumps(index, indent=1) + '\n')
            check(args.out, cargo_home=args.cargo_home, npm_cache=args.npm_cache)
        elif args.command == 'associate-npm':
            index = associate_npm(args.npm_cache, args.input)
            args.out.write_text(json.dumps(index, indent=1) + '\n')
            check(args.out, npm_cache=args.npm_cache)
        elif args.command == 'associate-local':
            index = associate_local(args.input)
            args.out.write_text(json.dumps(index, indent=1) + '\n')
            check(args.out)
        else:
            index = check(cargo_home=getattr(args, 'cargo_home', None), npm_cache=getattr(args, 'npm_cache', None))
        print(json.dumps(summary(index), indent=1))
        return 0
    except (ValueError, KeyError, OSError, StopIteration, subprocess.CalledProcessError, tarfile.TarError) as error:
        print(json.dumps({'transitive_index_match': False, 'error': str(error)}), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
