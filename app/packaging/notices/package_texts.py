#!/usr/bin/env python3
"""Ship the licence and notice texts of every transitive runtime dependency and of the supplier's components.

`extract` reads each locked .crate archive from a caller-supplied Cargo cache directory (the folder that
holds `<name>-<version>.crate`) and each locked npm tarball from a caller-supplied npm cache, verifies the
archive against Cargo.lock or the lock integrity, takes exactly the notice members transitive-index.json
names, verifies each member's size and SHA-256 against the index, and writes them under
`transitive/<ecosystem>/<package>/<version>/`. Held texts (retained root texts and texts fetched with the
owner's permission) are copied from their committed files after their digests are checked. It reads the
caches as files only: it never runs Cargo or npm and never writes to a cache.

`check` needs no cache: the committed tree must equal exactly the set the indexes name, byte for byte.
`overlay` writes ../unsigned/tauri.notices.conf.json: the development configuration plus every notice
resource (direct, transitive, supplier, coverage account), each mapped under third-party-notices/.
"""
import argparse
import copy
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import sys
import tarfile
import tempfile
import tomllib

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
TEXTS = 'app/packaging/notices/transitive'
SUPPLIER = 'app/packaging/supplier_notices/components.json'
HOSTING = 'app/src-tauri/src/hosting.rs'
INPUTS = 'app/packaging/notices/coverage-inputs.json'
OVERLAY = 'app/packaging/unsigned/tauri.notices.conf.json'
NAMESPACE = 'third-party-notices/'


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


transitive = _load('package_texts_transitive', HERE / 'transitive.py')
require, sha, git_blob = transitive.require, transitive.sha, transitive.git_blob


def load(repo, relative):
    return json.loads((Path(repo) / relative).read_bytes())


def declared_pin(repo=REPO):
    """The supplier pin the App declares (hosting.rs DECLARED_PIN); nothing here hard-codes it."""
    import re
    found = re.findall(r'^pub const DECLARED_PIN: &str = "([0-9A-Za-z.+-]+)";$', (Path(repo) / HOSTING).read_text(), re.M)
    require(len(found) == 1, 'declared supplier pin not found')
    return found[0]


def supplier_record(repo=REPO):
    """(pin, record path, record) for the declared pin's distribution record."""
    pin = declared_pin(repo)
    relative = f'app/src-tauri/resources/supplier/{pin}/CANONICAL_DISTRIBUTION.json'
    record = load(repo, relative)
    require(record.get('pin') == pin, 'distribution record is for another pin')
    return pin, relative, record


def executables(record):
    """The tree's executables: regular files with an execute bit that are neither libraries nor data."""
    return sorted(e['path'] for e in record['inventory']['entries']
                  if e['kind'] == 'file' and e['mode'] & 0o111 and not e['path'].endswith(('.dylib', '.json')))


def refuse_colliding_notices(archive, name, version):
    """Two root notice members that would land on one file (same name, or names equal ignoring case) refuse."""
    prefix, seen = f'{name}-{version}/', {}
    with tarfile.open(archive) as tar:
        for member in tar.getmembers():
            rel = member.name[len(prefix):] if member.name.startswith(prefix) else None
            if rel and '/' not in rel and transitive.NOTICE_NAME.match(rel):
                require(rel.casefold() not in seen, f'archive has two notice members for one name: {seen.get(rel.casefold())} and {rel}')
                seen[rel.casefold()] = rel


def crate_texts(lock_path, cargo_cache, out, select=None):
    """General extraction for any Cargo.lock and folder of .crate archives (no index needed).

    For every registry package in the lock (or only `select`, a set of (name, version)), reads
    `<cargo_cache>/<name>-<version>.crate`, requires its SHA-256 to equal the lock checksum, writes its
    root licence/notice members to `<out>/<name>/<version>/<member>` and returns one row per package:
    notice members with size and SHA-256, or `missing` with the repository and VCS revision the archive
    names. Git- or path-sourced packages have no archive here and are returned as `not-in-registry`.
    """
    packages = tomllib.loads(Path(lock_path).read_text())['package']
    rows = []
    for package in sorted(packages, key=lambda p: (p['name'], p['version'])):
        key = (package['name'], package['version'])
        if select is not None and key not in select:
            continue
        row = {'package': key[0], 'version': key[1], 'source': package.get('source')}
        if 'checksum' not in package:
            rows.append({**row, 'kind': 'not-in-registry'})
            continue
        archive = Path(cargo_cache) / f'{key[0]}-{key[1]}.crate'
        require(sha(archive.read_bytes()) == package['checksum'], 'cached crate differs from the lock: ' + archive.name)
        refuse_colliding_notices(archive, *key)
        notices, _, vcs, manifest, _ = transitive.read_crate(archive, *key)
        with tarfile.open(archive) as tar:
            for notice in notices:
                data = tar.extractfile(f'{key[0]}-{key[1]}/{notice["member"]}').read()
                require(sha(data) == notice['sha256'], 'member changed while reading: ' + archive.name)
                target = Path(out) / safe(key[0]) / safe(key[1]) / safe(notice['member'])
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
        rows.append({**row, 'checksum': package['checksum'], 'declared_license': manifest.get('license'),
                     'kind': 'archive-member' if notices else 'missing', 'notice_members': notices,
                     'repository': manifest.get('repository'), 'vcs_revision': vcs.get('git', {}).get('sha1'),
                     'path_in_vcs': vcs.get('path_in_vcs')})
    return rows


def safe(part):
    require(isinstance(part, str) and part and '\\' not in part and all(p not in ('', '.', '..') for p in part.split('/'))
            and not part.startswith('/'), 'unsafe text path: ' + repr(part))
    return part


def file_digest(repo, relative, expected=None):
    """Bytes of one committed file, refusing links, escapes and (when given) a different identity."""
    target = Path(repo) / safe(relative)
    require(not target.is_symlink() and target.resolve().is_relative_to(Path(repo).resolve()), 'text escapes the repository')
    raw = target.read_bytes()
    found = {'size_bytes': len(raw), 'sha256': sha(raw), 'git_blob_sha1': git_blob(raw)}
    if expected:
        require(all(found[k] == v for k, v in expected.items() if k in found), 'committed text differs: ' + relative)
    return found


def received_subjects(repo, rows):
    """Texts fetched with the owner's permission, each verified against the revision its crates name."""
    by_key = {(r['package'], r['version']): r for r in rows}
    found = {}
    for text in load(repo, INPUTS)['received_texts']:
        file_digest(repo, text['path'], text)
        require(PurePosixPath(text['path']).name == text['name'], 'received text name differs')
        for subject in text['subjects']:
            row = by_key.get((subject['package'], subject['version']))
            require(row is not None and row['source'] == 'registry', 'received text names no indexed crate: ' + subject['package'])
            locator = row['text']
            require(locator.get('repository') == text['repository'], 'received text is from another repository: ' + subject['package'])
            # The crate's own revision, or a root blob the retained root metadata names at that revision.
            require(locator.get('vcs_revision') == text['revision'] or
                    any('blob' + text['git_blob_sha1'] in item for item in locator.get('unresolved', [])),
                    'received text is not at the revision the crate names: ' + subject['package'])
            found.setdefault((subject['package'], subject['version']), []).append(text)
    return found


def planned(repo=REPO):
    """Relative path under TEXTS -> {size_bytes, sha256, source}; source says where extraction reads it."""
    repo = Path(repo)
    index = load(repo, 'app/packaging/notices/transitive-index.json')
    lock = transitive.cargo_lock(repo)
    direct = {c['package']: c for c in load(repo, 'app/packaging/notices/index.json')['components'] if c['ecosystem'] == 'npm'}
    received = received_subjects(repo, index['cargo'])
    plan = {}

    folded = set()

    def add(relative, entry):
        # Case-insensitive file systems would merge names that differ only by case.
        require(relative.casefold() not in folded, 'duplicate shipped text: ' + relative)
        folded.add(relative.casefold())
        plan[relative] = entry

    for row in index['cargo']:
        if row['source'] != 'registry':
            continue
        name, version, text = row['package'], row['version'], row['text']
        base = f'cargo/{safe(name)}/{safe(version)}/'
        if text['kind'] == 'archive-member':
            for member in row['notice_members']:
                add(base + safe(member['member']), {'size_bytes': member['size_bytes'], 'sha256': member['sha256'],
                    'source': {'crate': f'{name}-{version}.crate', 'checksum': lock[(name, version)]['checksum'],
                               'member': f"{name}-{version}/{member['member']}"}})
        elif text['kind'] == 'received-upstream-text':
            found = file_digest(repo, text['path'], {'git_blob_sha1': text['git_blob_sha1']})
            add(base + 'LICENSE.md', {'size_bytes': found['size_bytes'], 'sha256': found['sha256'], 'source': {'file': text['path']}})
        elif text['kind'] == 'retained-root-texts':
            for notice in text['notices']:
                file_digest(repo, notice['retained_path'], notice)
                add(base + safe(notice['root_path']), {'size_bytes': notice['size_bytes'], 'sha256': notice['sha256'],
                                                       'source': {'file': notice['retained_path']}})
        for extra in received.get((name, version), []):
            add(base + extra['name'], {'size_bytes': extra['size_bytes'], 'sha256': extra['sha256'], 'source': {'file': extra['path']}})
    for row in index['npm']:
        base = f"npm/{safe(row['package'])}/{safe(row['version'])}/"
        if row['text']['kind'] == 'direct-index-archive':
            for notice in direct[row['package']]['notices']:
                add(base + safe(notice['source_path']), {'size_bytes': notice['size_bytes'], 'sha256': notice['sha256'],
                    'source': {'integrity': row['integrity'], 'member': notice['source_path']}})
        elif row['text']['kind'] == 'lock-tarball':
            for member in row['text']['notice_members']:
                add(base + safe(member['member']), {'size_bytes': member['size_bytes'], 'sha256': member['sha256'],
                    'source': {'integrity': row['integrity'], 'member': member['member']}})
    return plan


def extract(cargo_cache, npm_cache, repo=REPO):
    """Write TEXTS from the caches and committed held texts; read-only on every input."""
    repo = Path(repo)
    plan = planned(repo)
    crates, tarballs = {}, {}
    staging = Path(tempfile.mkdtemp(prefix='.transitive-', dir=(repo / TEXTS).parent))
    try:
        for relative, entry in sorted(plan.items()):
            source = entry['source']
            if 'crate' in source:
                if source['crate'] not in crates:
                    raw = (Path(cargo_cache) / source['crate']).read_bytes()
                    require(sha(raw) == source['checksum'], 'cached crate differs from Cargo.lock: ' + source['crate'])
                    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
                        files = [m for m in archive.getmembers() if m.isfile()]
                        require(len({m.name for m in files}) == len(files), 'archive repeats a member: ' + source['crate'])
                        crates[source['crate']] = {m.name: archive.extractfile(m).read() for m in files}
                data = crates[source['crate']].get(source['member'])
            elif 'integrity' in source:
                if source['integrity'] not in tarballs:
                    tarballs[source['integrity']] = transitive.npm_notice_members(transitive.npm_tarball(npm_cache, source['integrity']))
                data = tarballs[source['integrity']].get(source['member'])
            else:
                data = (repo / source['file']).read_bytes()
            require(data is not None and len(data) == entry['size_bytes'] and sha(data) == entry['sha256'],
                    'text differs from the index: ' + relative)
            target = staging / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        final = repo / TEXTS
        if final.exists():
            shutil.rmtree(final)
        staging.rename(final)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return check(repo)


def check(repo=REPO):
    """The committed tree equals the planned set exactly; no cache is read."""
    repo = Path(repo)
    plan = planned(repo)
    root = repo / TEXTS
    found = {}
    for directory, folders, names in os.walk(root, followlinks=False):
        for name in folders + names:
            path = Path(directory) / name
            require(not path.is_symlink(), 'linked text refused: ' + str(path.relative_to(root)))
        for name in names:
            path = Path(directory) / name
            found[path.relative_to(root).as_posix()] = path.read_bytes()
    require(set(found) == set(plan), 'shipped texts differ from the indexes: missing ' + str(sorted(set(plan) - set(found))[:5])
            + ', extra ' + str(sorted(set(found) - set(plan))[:5]))
    for relative, entry in plan.items():
        require(len(found[relative]) == entry['size_bytes'] and sha(found[relative]) == entry['sha256'], 'text bytes differ: ' + relative)
    return {'transitive_texts': len(plan), 'bytes': sum(e['size_bytes'] for e in plan.values())}


def supplier_texts(repo=REPO):
    table = load(repo, SUPPLIER)
    prefix = 'app/packaging/supplier_notices/'
    for text in table['texts']:
        require(text['path'].startswith(prefix), 'supplier text outside supplier_notices')
        file_digest(repo, text['path'], text)
    return table['texts']


def resources(repo=REPO):
    """Every notice resource beyond the direct index: source (relative to src-tauri) -> bundle destination."""
    mapped = {'../packaging/notices/transitive-index.json': NAMESPACE + 'transitive-index.json',
              '../packaging/notices/coverage.json': NAMESPACE + 'coverage.json'}
    for relative in sorted(planned(repo)):
        mapped['../packaging/notices/transitive/' + relative] = NAMESPACE + 'transitive/' + relative
    for text in supplier_texts(repo):
        relative = text['path'].removeprefix('app/packaging/supplier_notices/')
        mapped['../packaging/supplier_notices/' + relative] = NAMESPACE + 'supplier/' + relative
    require(len(set(mapped.values())) == len(mapped), 'duplicate notice destination')
    return mapped


def overlay(repo=REPO, notices_root=None):
    """The explicit notice overlay: development base, direct index and assets, then every other notice resource."""
    repo = Path(repo)
    base = load(repo, 'app/packaging/unsigned/tauri.development.conf.json')
    value = copy.deepcopy(base)
    direct = load(notices_root or repo / 'app/packaging/notices', 'index.json')
    paths = ['index.json'] + [n['asset'] for c in direct['components'] for n in c['notices']]
    for path in paths:
        value['bundle']['resources']['../packaging/notices/' + path] = NAMESPACE + path
    value['bundle']['resources'].update(resources(repo))
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    e = sub.add_parser('extract')
    e.add_argument('--cargo-cache', type=Path, required=True, help='folder holding the locked <name>-<version>.crate files')
    e.add_argument('--npm-cache', type=Path, required=True, help='npm cache root holding _cacache')
    sub.add_parser('check')
    sub.add_parser('overlay')
    c = sub.add_parser('crates', help='Extract root notice members for any Cargo.lock from a folder of .crate archives')
    c.add_argument('--lock', type=Path, required=True)
    c.add_argument('--cargo-cache', type=Path, required=True)
    c.add_argument('--out', type=Path, required=True, help='new or empty folder; texts go to <out>/<name>/<version>/')
    c.add_argument('--rows', type=Path, required=True, help='JSON file for the per-package rows')
    args = parser.parse_args()
    try:
        if args.command == 'extract':
            result = extract(args.cargo_cache, args.npm_cache)
        elif args.command == 'crates':
            require(not args.out.exists() or not any(args.out.iterdir()), '--out must be new or empty')
            rows = crate_texts(args.lock, args.cargo_cache, args.out)
            args.rows.write_text(json.dumps(rows, indent=1) + '\n')
            result = {'packages': len(rows), 'kinds': {k: sum(r['kind'] == k for r in rows) for k in sorted({r['kind'] for r in rows})}}
        elif args.command == 'overlay':
            (REPO / OVERLAY).write_text(json.dumps(overlay(), indent=2) + '\n')
            result = {'overlay_resources': len(overlay()['bundle']['resources'])}
        else:
            result = check()
        print(json.dumps(result))
        return 0
    except (ValueError, KeyError, OSError, tarfile.TarError) as error:
        print(json.dumps({'package_texts_match': False, 'error': str(error)}), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
