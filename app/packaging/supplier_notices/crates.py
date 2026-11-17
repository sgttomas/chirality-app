#!/usr/bin/env python3
"""Notices for every package the supplier's Codex and ripgrep lockfiles lock at the declared pin, or an explicit gap.

The set is a superset: a lockfile locks packages for every platform and feature, so some of these packages may not be
compiled into the macOS executables. Which are is not established here, and no resolver, Cargo or Bazel is run.

Inputs, all committed under `crates/`: the two lockfiles as the supplier's source holds them, `associations.json` (the
reviewed bindings of each lockfile to its source revision, the Git-sourced packages' licence files and the workspace
texts) and `index.json`, which `index` makes from the held archives. `texts/` holds each shipped crate text once,
named by its SHA-256.

- `index --archives MAP.json` reads each locked archive through `crate_notices` (checksum before opening, header
  inventory, selected notice members only) and writes `index.json`. It writes no text.
- `extract --archives MAP.json --received DIR` repeats the read, requires every archive to equal its index row, copies
  the Git-sourced licence files from DIR after checking each against its recorded blob, and writes `texts/`.
- `generate` writes `packages.json`, the shipped per-package account derived from the committed inputs.
- `check` needs no archive: the lockfiles, associations, index, texts and `packages.json` must agree exactly (every
  locked package has one row, every text exists once with its digest, nothing else is held).

MAP.json maps `<name>-<version>.crate` to the absolute path of a held archive. Nothing here writes to a cache,
executes supplier code or opens a network connection. A text selected by its file name is a file named as a notice;
selection by name does not show that no other file in a package carries its own terms.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import stat
import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
BASE = 'app/packaging/supplier_notices/crates'
INDEX = BASE + '/index.json'
ASSOCIATIONS = BASE + '/associations.json'
TEXTS = BASE + '/texts'
APP_INDEX = 'app/packaging/notices/transitive-index.json'
APP_TEXTS = 'app/packaging/notices/transitive'
FORMAT = 'supplier-crate-notices/1'
GIT_SOURCE = re.compile(r'^git\+(https://[^?#]+?)(?:\.git)?\?rev=([0-9a-f]{40})#([0-9a-f]{40})$')
HEX64 = re.compile('[0-9a-f]{64}')
# Owner readings are needed, as for the App's own copies, for texts from these repositories (coverage.py's rule).
READING_REPOSITORIES = {'https://github.com/madsmtm/objc2'}

_spec = importlib.util.spec_from_file_location('supplier_crate_notices_route', HERE / 'crate_notices.py')
route = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(route)
sha256, git_blob = route.sha256, route.git_blob


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(repo, relative):
    return json.loads((Path(repo) / relative).read_bytes())


def regular(repo, relative):
    path = Path(repo) / relative
    require(stat.S_ISREG(path.lstat().st_mode), 'not a regular non-link file: ' + relative)
    require(path.resolve().is_relative_to(Path(repo).resolve()), 'path escapes the repository: ' + relative)
    return path.read_bytes()


def locked(repo, lock):
    """The lockfile's packages as {(name, version): package}, after its bytes equal the association's identity."""
    raw = regular(repo, lock['path'])
    require((len(raw), sha256(raw), git_blob(raw)) == (lock['size_bytes'], lock['sha256'], lock['git_blob_sha1']),
            'lockfile differs from its association: ' + lock['path'])
    packages = {}
    for package in tomllib.loads(raw.decode())['package']:
        key = (package['name'], package['version'])
        require(key not in packages, 'lockfile locks one name and version twice: ' + ' '.join(key))
        packages[key] = package
    return packages


def kind(package):
    source = package.get('source')
    if source is None:
        return 'path'
    if source == 'registry+https://github.com/rust-lang/crates.io-index':
        require(HEX64.fullmatch(package.get('checksum', '')) is not None, 'registry package without checksum: ' + package['name'])
        return 'registry'
    require(GIT_SOURCE.fullmatch(source) is not None, 'unsupported package source: ' + source)
    match = GIT_SOURCE.fullmatch(source)
    require(match.group(2) == match.group(3), 'Git source names two revisions: ' + source)
    return 'git'


def registry_set(repo, associations):
    """{(name, version, checksum): [lock ids]} over both lockfiles."""
    found = {}
    for lock in associations['locks']:
        for key, package in locked(repo, lock).items():
            if kind(package) == 'registry':
                found.setdefault((*key, package['checksum']), []).append(lock['id'])
    return found


def archive_map(path):
    value = json.loads(Path(path).read_bytes())
    require(isinstance(value, dict) and all(isinstance(k, str) and isinstance(v, str) and os.path.isabs(v)
                                            for k, v in value.items()), 'archive map must name absolute paths')
    return value


def build_index(repo, archives):
    """The index rows of every locked registry package, read through the notice-only route."""
    associations = load(repo, ASSOCIATIONS)
    archives = archive_map(archives)
    rows = []
    for (name, version, checksum), locks in sorted(registry_set(repo, associations).items()):
        raw = Path(archives[f'{name}-{version}.crate']).read_bytes()
        rows.append({**route.index_entry(raw, (name, version), checksum), 'locks': sorted(locks)})
    return {'format': FORMAT, 'pin': associations['pin'],
            'selection': 'Each archive verified against its lockfile checksum before opening; its tar headers inventoried; '
                         'the members selected by name (at any depth, see rule) read, and no other payload. A name-based '
                         'selection does not show that no other file carries its own terms.',
            'rule': {'notice_stem': route.NOTICE_STEM.pattern, 'notice_folder': route.NOTICE_FOLDER.pattern,
                     'not_a_notice': route.NOT_A_NOTICE.pattern},
            'registry': rows}


def write_index(repo, archives):
    value = build_index(repo, archives)
    (Path(repo) / INDEX).write_bytes(encode(value, 'registry'))
    return {'registry_packages': len(value['registry']), 'notices': sum(len(r['notices']) for r in value['registry'])}


def app_rows(repo):
    """The App's own transitive index rows, by (name, version, checksum), for crates whose archive names no notice."""
    return {(r['package'], r['version'], r['archive_sha256']): r for r in load(repo, APP_INDEX)['cargo'] if r['source'] == 'registry'}


def app_text_files(repo, row):
    """The App's committed text files for one of its own crate rows (shipped under its transitive texts)."""
    prefix = Path(repo) / APP_TEXTS / 'cargo' / row['package'] / row['version']
    if not prefix.is_dir():
        return []
    return sorted(str(p.relative_to(repo)) for p in prefix.iterdir())


def wanted_texts(repo):
    """sha256 -> (size, where the bytes come from) for every crate text the group ships."""
    associations, index = load(repo, ASSOCIATIONS), load(repo, INDEX)
    wanted = {}

    def want(digest, size, source):
        require(wanted.get(digest, (size, source))[0] == size, 'one digest with two sizes: ' + digest)
        wanted.setdefault(digest, (size, source))

    for row in index['registry']:
        for notice in row['notices']:
            want(notice['sha256'], notice['size_bytes'], ('archive', row['package'], row['version']))
    apps = app_rows(repo)
    for row in index['registry']:
        if not row['notices']:
            app = apps.get((row['package'], row['version'], row['checksum']))
            for path in app_text_files(repo, app) if app else []:
                raw = regular(repo, path)
                want(sha256(raw), len(raw), ('file', path))
    for source in associations['git_sources']:
        for text in source['texts']:
            want(text['sha256'], text['size_bytes'], ('received', source['repository'], source['revision'], text['source_path']))
    return wanted


def entries(repo):
    """Every locked package of both lockfiles, with its texts (by digest or committed path) or its gap."""
    repo = Path(repo)
    associations, index = load(repo, ASSOCIATIONS), load(repo, INDEX)
    require(index.get('format') == FORMAT and index.get('pin') == associations['pin'], 'crate index is for another pin or format')
    by_key = {(r['package'], r['version'], r['checksum']): r for r in index['registry']}
    require(len(by_key) == len(index['registry']), 'crate index repeats a package')
    expected = registry_set(repo, associations)
    require(set(by_key) == set(expected), 'crate index differs from the lockfiles: missing '
            + str(sorted(set(expected) - set(by_key))[:5]) + ', extra ' + str(sorted(set(by_key) - set(expected))[:5]))
    for key, locks in expected.items():
        require(by_key[key]['locks'] == sorted(locks), 'crate index names other lockfiles for ' + ' '.join(key[:2]))
    apps = app_rows(repo)
    git = {}
    for source in associations['git_sources']:
        for package in source['packages']:
            require(package not in git, 'two Git associations for ' + package)
            git[package] = source
    workspaces = {w['lock']: w for w in associations['workspaces']}
    rows = []
    used_git = set()
    for lock in associations['locks']:
        for (name, version), package in sorted(locked(repo, lock).items()):
            row = {'lock': lock['id'], 'name': name, 'version': version, 'source_kind': kind(package)}
            if row['source_kind'] == 'registry':
                entry = by_key[(name, version, package['checksum'])]
                row['checksum'] = package['checksum']
                if entry['notices']:
                    row.update(standing='text', basis='licence files of the locked crate archive, selected by name',
                               texts=[{'member': n['path'], 'sha256': n['sha256'], 'size_bytes': n['size_bytes']} for n in entry['notices']])
                elif (app := apps.get((name, version, package['checksum']))) is not None and app_text_files(repo, app):
                    texts = [{'file': p, 'sha256': sha256(regular(repo, p)), 'size_bytes': len(regular(repo, p))}
                             for p in app_text_files(repo, app)]
                    reading = app['text']['kind'] == 'received-upstream-text' or app['text'].get('repository') in READING_REPOSITORIES
                    row.update(texts=texts, standing='held' if reading else 'text',
                               basis='the text the App holds for the same crate, version and archive checksum '
                                     f'({app["text"]["kind"]} from {app["text"].get("repository")})')
                    if reading:
                        row['reason'] = ('the same text awaits an owner licence reading for this crate as the App\'s own copy does; '
                                         'the App\'s reading of 2026-11-12 is not extended to the supplier\'s copy here')
                else:
                    row.update(standing='gap', texts=[], reason='the locked archive has no member named as a notice and no '
                               'text is held for this crate version',
                               would_close=f'an owner-permitted acquisition of the licence text {name} {version} names')
            elif row['source_kind'] == 'git':
                match = GIT_SOURCE.fullmatch(package['source'])
                source = git.get(f'{name} {version}')
                require(source is not None, 'no Git association for locked package ' + f'{name} {version}')
                require((source['repository'], source['revision']) == (match.group(1), match.group(3)),
                        'Git association names another repository or revision than the lock: ' + name)
                used_git.add(f'{name} {version}')
                row.update(repository=source['repository'], revision=source['revision'],
                           texts=[{'received': t['source_path'], 'sha256': t['sha256'], 'size_bytes': t['size_bytes']}
                                  for t in source['texts'] if f'{name} {version}' in t['for']])
                require(row['texts'], 'Git association ships no text for ' + name)
                row.update(standing='text', basis=source['basis'])
            else:
                workspace = workspaces[lock['id']]
                row.update(repository=workspace['repository'], revision=workspace['revision'],
                           texts=[{'file': t['path'], 'sha256': t['sha256'], 'size_bytes': t['size_bytes']} for t in workspace['texts']],
                           standing='text', basis=workspace['basis'])
            rows.append(row)
    require(used_git == set(git), 'Git association names a package no lockfile locks: ' + str(sorted(set(git) - used_git)))
    return rows


def check_texts(repo):
    """texts/ holds exactly the wanted digests, each once, as regular files with those bytes."""
    repo = Path(repo)
    associations = load(repo, ASSOCIATIONS)
    for workspace in associations['workspaces']:
        for text in workspace['texts']:
            raw = regular(repo, text['path'])
            require((len(raw), sha256(raw), git_blob(raw)) == (text['size_bytes'], text['sha256'], text['git_blob_sha1']),
                    'workspace text differs from its association: ' + text['path'])
            require(text['git_blob_sha1'] in text['listing_blobs'], 'workspace text is not the blob its listing names: ' + text['path'])
    for source in associations['git_sources']:
        for text in source['texts']:
            require(text['git_blob_sha1'] == text['listing_blob'], 'Git-source text is not the blob its listing names: '
                    + source['repository'] + ' ' + text['source_path'])
    wanted = wanted_texts(repo)
    root = repo / TEXTS
    held = {}
    for directory, folders, names in os.walk(root, followlinks=False):
        require(not folders, 'crate texts are one flat folder')
        for name in names:
            held[name] = regular(repo, f'{TEXTS}/{name}')
    require(set(held) == set(wanted), 'crate texts differ from the wanted set: missing ' + str(sorted(set(wanted) - set(held))[:3])
            + ', extra ' + str(sorted(set(held) - set(wanted))[:3]))
    for digest, raw in held.items():
        require(sha256(raw) == digest and len(raw) == wanted[digest][0], 'crate text bytes differ from their name: ' + digest)
    for source in associations['git_sources']:
        for text in source['texts']:
            require(git_blob(held[text['sha256']]) == text['git_blob_sha1'], 'Git-source text differs from its blob: ' + text['source_path'])
    return {'texts': len(held), 'bytes': sum(len(v) for v in held.values())}


PACKAGES = BASE + '/packages.json'
NAMESPACE = 'third-party-notices/supplier/'


def package_path(repo, text, store):
    """Where a package's text ships: the crate store by digest, or a workspace text where the supplier table maps it."""
    if 'file' in text and text['file'].startswith('app/packaging/supplier_notices/') and not text['file'].startswith(TEXTS):
        return NAMESPACE + text['file'].removeprefix('app/packaging/supplier_notices/')
    require(text['sha256'] in store, 'a package text is not in the crate store: ' + text['sha256'])
    return NAMESPACE + 'crates/texts/' + text['sha256']


def packages(repo=REPO):
    """The shipped per-package account: every locked package with its standing and where each text ships (derived)."""
    associations = load(repo, ASSOCIATIONS)
    store = set(wanted_texts(repo))
    rows = []
    for row in entries(repo):
        item = {k: v for k, v in row.items() if k != 'texts'}
        item['texts'] = [{**{k: t[k] for k in t if k in ('member', 'received')}, 'sha256': t['sha256'], 'size_bytes': t['size_bytes'],
                          'package_path': package_path(repo, t, store)} for t in row['texts']]
        rows.append(item)
    return {'format': 'supplier-crate-packages/1', 'pin': associations['pin'], 'superset': associations['superset'],
            'selection': load(repo, INDEX)['selection'],
            'standings': {'text': 'its texts ship (the basis says on what footing; adequacy is not decided here)',
                          'held': 'a text ships; it awaits an owner licence reading',
                          'gap': 'no text ships; the reason and what would close it are given'},
            'locks': [{k: lock[k] for k in ('id', 'component', 'repository', 'revision', 'source_path', 'sha256', 'binding')}
                      for lock in associations['locks']],
            'packages': rows}


def encode(value, rows='packages'):
    """JSON with one line per row of `rows`, so a reviewer's diff shows one package per line."""
    head = json.dumps({k: v for k, v in value.items() if k != rows}, indent=1, ensure_ascii=False)
    body = ',\n'.join('  ' + json.dumps(r, ensure_ascii=False, separators=(',', ':')) for r in value[rows])
    return (head[:-2] + ',\n "' + rows + '": [\n' + body + '\n ]\n}\n').encode()


def check(repo=REPO):
    rows = entries(repo)
    texts = check_texts(repo)
    require(regular(repo, PACKAGES) == encode(packages(repo)), 'crates/packages.json is stale; regenerate with crates.py generate')
    by_lock = {}
    for row in rows:
        counts = by_lock.setdefault(row['lock'], {'packages': 0, 'registry': 0, 'git': 0, 'path': 0, 'text': 0, 'held': 0, 'gap': 0})
        counts['packages'] += 1
        counts[row['source_kind']] += 1
        counts[row['standing']] += 1
    return {'locks': by_lock, **texts}


def group(repo, component):
    """For one compiled-dependencies component: its lockfile association, its packages and the store texts it ships."""
    associations = load(repo, ASSOCIATIONS)
    locks = [lock for lock in associations['locks'] if lock['component'] == component]
    if not locks:
        return None
    require(len(locks) == 1, 'two lockfiles name one component: ' + component)
    value = packages(repo)
    rows = [r for r in value['packages'] if r['lock'] == locks[0]['id']]
    return {'lock': locks[0], 'packages': rows}


def extract(repo, archives, received):
    """Write texts/ from the archives (checked against the index), the App's held files and the received Git texts."""
    repo = Path(repo)
    associations, index = load(repo, ASSOCIATIONS), load(repo, INDEX)
    archives = archive_map(archives)
    entries(repo)
    root = repo / TEXTS
    require(not root.exists() or not any(root.iterdir()), 'crate texts folder must be new or empty')
    root.mkdir(parents=True, exist_ok=True)
    written = {}

    def put(raw):
        digest = sha256(raw)
        if digest not in written:
            (root / digest).write_bytes(raw)
            written[digest] = len(raw)

    for row in index['registry']:
        if row['notices']:
            raw = Path(archives[f'{row["package"]}-{row["version"]}.crate']).read_bytes()
            for data in route.extract_checked(raw, row).values():
                put(data)
    for digest, (size, source) in wanted_texts(repo).items():
        if source[0] == 'file':
            put(regular(repo, source[1]))
    for source in associations['git_sources']:
        for text in source['texts']:
            # A received text comes from DIR; one whose bytes the repository already holds is read from its committed file.
            raw = regular(repo, text['held_at']) if 'held_at' in text else (Path(received) / text['received_as']).read_bytes()
            require((len(raw), sha256(raw), git_blob(raw)) == (text['size_bytes'], text['sha256'], text['git_blob_sha1']),
                    'received text differs from its association: ' + text['source_path'])
            put(raw)
    return check_texts(repo)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='command', required=True)
    i = sub.add_parser('index'); i.add_argument('--archives', type=Path, required=True)
    e = sub.add_parser('extract'); e.add_argument('--archives', type=Path, required=True)
    e.add_argument('--received', type=Path, required=True, help='folder holding the received Git-source licence texts')
    sub.add_parser('check')
    sub.add_parser('generate', help='write crates/packages.json from the committed inputs')
    args = parser.parse_args()
    try:
        if args.command == 'index':
            result = write_index(REPO, args.archives)
        elif args.command == 'extract':
            result = extract(REPO, args.archives, args.received)
        elif args.command == 'generate':
            (REPO / PACKAGES).write_bytes(encode(packages(REPO)))
            result = check(REPO)
        else:
            result = check(REPO)
    except (ValueError, KeyError, OSError) as error:
        print(json.dumps({'supplier_crates_match': False, 'error': str(error)}), file=sys.stderr)
        return 1
    print(json.dumps({'supplier_crates_match': True, **result}, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
