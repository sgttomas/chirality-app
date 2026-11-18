#!/usr/bin/env python3
"""Notices for every package the supplier's Codex and ripgrep lockfiles lock at the declared pin, or an explicit gap.

The set is a superset: a lockfile locks packages for every platform and feature, so some of these packages may not be
compiled into the macOS executables. Which are is not established here beyond the packages recorded absent from the macOS
target by declared target condition (`not_in_macos_package`, below); no resolver, Cargo or Bazel is run.

Inputs, all committed under `crates/`: the two lockfiles as the supplier's source holds them, `associations.json` (the
reviewed bindings of each lockfile to its source revision, the Git-sourced packages' licence files, the workspace
texts, and the texts the App already holds for the same crate archive) and `index.json`, which `index` makes from the held archives. `texts/` holds each shipped crate text once,
named by its SHA-256.

- `index --archives MAP.json` reads each locked archive through `crate_notices` (checksum before opening, header
  inventory, selected notice members only) and writes `index.json`. It writes no text.
- `extract --archives MAP.json --received DIR` repeats the read, requires every archive to equal its index row, copies
  the Git-sourced licence files from DIR after checking each against its recorded blob, and writes `texts/`.
- `generate` writes `packages.json`, the shipped per-package account derived from the committed inputs.

A registry package with no archive notice may take its text through exactly one reviewed association in
`associations.json`: `app_texts` (the App's copy of the same archive) or `registry_sources` (the publisher's licence
files at the revision the archive's VCS record names, each bound to the blob and size a saved listing gives and held in
the store through another route). The owner-reading requirement is applied after the route is resolved. A package with no
text route may instead carry `not_in_macos_package` (absence from the macOS target by declared target condition, checked
here against the lockfile's reverse dependencies), `no_publisher_text` (a licence is stated and no publisher text was
found; open), or a specific gap reason in `gap_reasons`. An association naming a package it cannot apply to refuses.
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
FORMAT = 'supplier-crate-notices/1'
GIT_SOURCE = re.compile(r'^git\+(https://[^?#]+?)(?:\.git)?\?rev=([0-9a-f]{40})#([0-9a-f]{40})$')
HEX64 = re.compile('[0-9a-f]{64}')
# Owner readings are needed, as for the App's own copies, for texts from these repositories (coverage.py's rule).
READING_REPOSITORIES = {'https://github.com/madsmtm/objc2'}
# The macOS package's one target. A package is absent from it only when every lockfile edge to it is declared under a
# target condition that is false for this target, in one of the closed forms of `target_holds`.
MACOS_TARGET = 'aarch64-apple-darwin'
STANDINGS = {'text': 'its texts ship (the basis says on what footing; adequacy is not decided here)',
             'held': 'a text ships; it awaits an owner licence reading',
             'gap': 'no text ships; the reason and what would close it are given',
             'no-publisher-text': 'no text ships: a licence is stated and no publisher text was found at the examined revision; '
                                  'open until a text exists or the owner decides what may serve as its notice',
             'not-in-macos-package': 'no text ships: absent from the macOS target by declared target condition (the evidence '
                                     'is given); not part of what the package carries'}
# Standings that leave a compiled-dependencies component open: everything but text and recorded absence.
OPEN = ('held', 'gap', 'no-publisher-text')
HEX40 = re.compile('[0-9a-f]{40}')

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


def app_texts(associations):
    """Reviewed reuse of texts the App holds, by (name, version, checksum), for crates whose archive names no notice.

    Each text is copied into the crate store by `extract` and checked there by digest; `check` reads no App file, so a
    change to the App's own notices cannot change this group."""
    found = {}
    for entry in associations.get('app_texts', []):
        for package in entry['packages']:
            name, version = package.split(' ')
            require((name, version, entry['checksum']) not in found, 'two App-text associations for ' + package)
            found[(name, version, entry['checksum'])] = entry
    return found


def registry_sources(associations):
    """Reviewed publisher-text associations for registry packages, by (name, version, checksum); shape checked."""
    found = {}
    for entry in associations.get('registry_sources', []):
        require(set(entry) <= {'packages', 'repository', 'repository_basis', 'revision', 'listing', 'basis', 'texts'}
                and {'packages', 'repository', 'revision', 'listing', 'basis', 'texts'} <= set(entry),
                'unknown registry-source association shape')
        require(entry['repository'].startswith('https://github.com/') and HEX40.fullmatch(entry['revision'] or '')
                and isinstance(entry['basis'], str) and entry['basis'].strip(), 'a registry-source association needs its '
                'publisher repository, revision and basis: ' + str(entry.get('repository')))
        require(entry['packages'], 'a registry-source association names no package: ' + entry['repository'])
        require(entry['texts'], 'a registry-source association must have at least one text: ' + entry['repository'])
        for text in entry['texts']:
            require(set(text) == {'source_path', 'size_bytes', 'sha256', 'git_blob_sha1', 'listing_blob', 'listing_size'},
                    'unknown registry-source text shape: ' + entry['repository'])
            require(text['git_blob_sha1'] == text['listing_blob'] and text['size_bytes'] == text['listing_size'],
                    'a registry-source text is not the blob and size its listing names: ' + entry['repository'] + ' '
                    + text['source_path'])
        for package in entry['packages']:
            key = (package['name'], package['version'], package['checksum'])
            require(key not in found, 'two registry-source associations for ' + ' '.join(key[:2]))
            found[key] = entry
    return found


def keyed(associations, collection):
    """{(name, version, checksum): entry} for a per-package collection; a repeated package refuses."""
    found = {}
    for entry in associations.get(collection, []):
        for package in entry.get('packages', [entry]):
            key = (package['name'], package['version'], package['checksum'])
            require(key not in found, f'{collection} names {key[0]} {key[1]} twice')
            found[key] = entry
    return found


TARGET_TABLE = re.compile(r"^\[target\.(?:'(?P<cfg>[^']*)'|(?P<triple>[A-Za-z0-9_-]+))\."
                          r"(?P<table>dependencies|dev-dependencies|build-dependencies)(?:\.(?P<dependency>[A-Za-z0-9_-]+))?\]$")
TABLE_KIND = {'dependencies': 'normal', 'dev-dependencies': 'dev', 'build-dependencies': 'build'}


def target_holds(table, target=MACOS_TARGET):
    """(holds for target, edge kind, dependency named by a dotted table) for a target dependency table header.

    The closed forms: cfg(target_os = "..."), cfg(windows), and a literal target triple. Any other form, or a table
    that is not target-specific, refuses: absence is never inferred from a name or from an unknown condition."""
    match = TARGET_TABLE.fullmatch(table)
    require(match is not None, 'not a target-specific dependency table: ' + table)
    os_name = {'aarch64-apple-darwin': 'macos'}[target]
    if match.group('triple') is not None:
        holds = match.group('triple') == target
    else:
        cfg = match.group('cfg')
        os_match = re.fullmatch(r'cfg\(target_os = "([a-z0-9_]+)"\)', cfg)
        if os_match is not None:
            holds = os_match.group(1) == os_name
        elif cfg == 'cfg(windows)':
            holds = False
        else:
            raise ValueError('a target condition outside the closed forms: ' + cfg)
    return holds, TABLE_KIND[match.group('table')], match.group('dependency')


def reverse_dependencies(packages):
    """{(name, version): {(name, version) of each package whose lockfile dependencies name it}}."""
    by_name = {}
    for key in packages:
        by_name.setdefault(key[0], []).append(key)
    found = {}
    for key, package in packages.items():
        for dependency in package.get('dependencies', []):
            name, *rest = dependency.split(' ')
            candidates = [k for k in by_name.get(name, []) if not rest or k[1] == rest[0]]
            require(len(candidates) == 1, 'a lockfile dependency does not resolve to one package: ' + dependency)
            found.setdefault(candidates[0], set()).add(key)
    return found


def absence(entry, lock, packages, reverse):
    """The recorded evidence that a package is absent from the macOS target, checked against the lockfile.

    The reverse dependencies must be exactly the lockfile's; each must carry the manifest declaring its edge and every
    edge line naming the package, each under a target table whose condition is false for the macOS target."""
    require(set(entry) == {'lock', 'name', 'version', 'checksum', 'target', 'reverse_dependencies'} and entry['target'] == MACOS_TARGET,
            'unknown not-in-macOS-package shape: ' + str(entry.get('name')))
    key = (entry['name'], entry['version'])
    require(key in packages and packages[key].get('checksum') == entry['checksum'], 'not-in-macOS-package names no locked '
            'package with that checksum: ' + ' '.join(key))
    recorded = [(r['name'], r['version']) for r in entry['reverse_dependencies']]
    require(len(recorded) == len(set(recorded)) and set(recorded) == reverse.get(key, set()) and recorded,
            'the recorded reverse dependencies of ' + ' '.join(key) + ' differ from the lockfile\'s: recorded '
            + str(sorted(recorded)) + ', lockfile ' + str(sorted(reverse.get(key, set()))))
    for dependent in entry['reverse_dependencies']:
        source = packages[(dependent['name'], dependent['version'])]
        if kind(source) == 'registry':
            require(set(dependent) == {'name', 'version', 'archive_manifest', 'edges'}, 'a registry reverse dependency needs '
                    'its archive manifest: ' + dependent['name'])
            manifest = dependent['archive_manifest']
            require(set(manifest) == {'checksum', 'member', 'size_bytes', 'sha256'} and manifest['checksum'] == source['checksum']
                    and manifest['member'] == 'Cargo.toml' and HEX64.fullmatch(manifest['sha256']),
                    'the archive manifest is not the locked archive\'s Cargo.toml: ' + dependent['name'])
        else:
            require(kind(source) == 'path' and set(dependent) == {'name', 'version', 'workspace_manifest', 'edges'},
                    'a workspace reverse dependency needs its pinned manifest: ' + dependent['name'])
            manifest = dependent['workspace_manifest']
            require(set(manifest) == {'repository', 'revision', 'path', 'size_bytes', 'git_blob_sha1', 'sha256'}
                    and (manifest['repository'], manifest['revision']) == (lock['repository'], lock['revision'])
                    and manifest['path'].endswith('Cargo.toml') and HEX40.fullmatch(manifest['git_blob_sha1']),
                    'the workspace manifest is not at the lockfile\'s repository and revision: ' + dependent['name'])
        require(dependent['edges'], 'a reverse dependency records no edge: ' + dependent['name'])
        for edge in dependent['edges']:
            require(set(edge) == {'table', 'table_line', 'line', 'text', 'kind'} and edge['line'] >= edge['table_line'] >= 1,
                    'unknown edge shape: ' + dependent['name'])
            holds, edge_kind, named = target_holds(edge['table'])
            require(edge['kind'] == edge_kind, 'the edge kind differs from its table: ' + dependent['name'])
            name = re.escape(entry['name'])
            if named is not None:
                require(named == entry['name'] and edge['line'] == edge['table_line'] and edge['text'] == edge['table'],
                        'a dotted dependency table names another package: ' + edge['table'])
            else:
                require(edge['line'] > edge['table_line'] and (re.match(r'^"?' + name + r'"?\s*=', edge['text'])
                        or re.search(r'package\s*=\s*"' + name + '"', edge['text'])),
                        'the edge line does not name the package: ' + edge['text'])
            require(not holds, f'{entry["name"]} {entry["version"]} is declared for {MACOS_TARGET} by {dependent["name"]}: '
                    + edge['table'])
    return {'target': MACOS_TARGET, 'reverse_dependencies': entry['reverse_dependencies']}


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
    reused = app_texts(associations)
    for row in index['registry']:
        if not row['notices'] and (entry := reused.get((row['package'], row['version'], row['checksum']))) is not None:
            for text in entry['texts']:
                want(text['sha256'], text['size_bytes'], ('file', text['app_path']))
    for source in associations['git_sources']:
        for text in source['texts']:
            want(text['sha256'], text['size_bytes'], ('received', source['repository'], source['revision'], text['source_path']))
    # Nothing is received for a registry-source text: its bytes are ones the store already holds through another route.
    for entry in associations.get('registry_sources', []):
        for text in entry['texts']:
            require(wanted.get(text['sha256'], (None,))[0] == text['size_bytes'], 'a registry-source text is not held through '
                    'another route: ' + entry['repository'] + ' ' + text['source_path'])
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
    reused = app_texts(associations)
    published = registry_sources(associations)
    unresolved = {name: keyed(associations, name) for name in ('not_in_macos_package', 'no_publisher_text', 'gap_reasons')}
    for name, collection in unresolved.items():
        for other, entries_ in unresolved.items():
            both = set(collection) & set(entries_) if other != name else set()
            require(not both, f'{name} and {other} both name ' + str(sorted(both)[:3]))
    used_app, used = set(), set()
    git = {}
    for source in associations['git_sources']:
        for package in source['packages']:
            require(package not in git, 'two Git associations for ' + package)
            git[package] = source
    workspaces = {w['lock']: w for w in associations['workspaces']}
    rows = []
    used_git = set()
    for lock in associations['locks']:
        packages_ = locked(repo, lock)
        reverse = reverse_dependencies(packages_)
        for (name, version), package in sorted(packages_.items()):
            row = {'lock': lock['id'], 'name': name, 'version': version, 'source_kind': kind(package)}
            if row['source_kind'] == 'registry':
                key = (name, version, package['checksum'])
                entry = by_key[key]
                row['checksum'] = package['checksum']
                routes = [r for r, found in (('archive', entry['notices']), ('app', key in reused), ('publisher', key in published)) if found]
                require(len(routes) <= 1, f'{name} {version} has more than one text route: ' + ', '.join(routes))
                marks = [n for n, collection in unresolved.items() if key in collection]
                require(not (routes and marks), f'{name} {version} has a text route and is also named in ' + ', '.join(marks))
                used.update((n, key) for n in marks)
                repository = None
                if routes == ['archive']:
                    row.update(standing=None, basis='licence files of the locked crate archive, selected by name',
                               texts=[{'member': n['path'], 'sha256': n['sha256'], 'size_bytes': n['size_bytes']} for n in entry['notices']])
                elif routes == ['app']:
                    app = reused[key]
                    used_app.add(key)
                    require(app['reading_required'] == (app['repository'] in READING_REPOSITORIES),
                            'an App-text association states another reading requirement than the rule: ' + name)
                    repository = app['repository']
                    row.update(texts=[{'app_text': t['app_path'], 'sha256': t['sha256'], 'size_bytes': t['size_bytes']} for t in app['texts']],
                               standing=None, basis=app['basis'])
                elif routes == ['publisher']:
                    source = published[key]
                    repository = source['repository']
                    row.update(standing=None, repository=source['repository'], revision=source['revision'],
                               texts=[{'publisher_text': t['source_path'], 'sha256': t['sha256'], 'size_bytes': t['size_bytes']}
                                      for t in source['texts']],
                               basis=source['basis'] + f' ({source["repository"]} at {source["revision"][:8]}; each text is the blob '
                                     'and size the saved listing of that revision names, and its bytes are held in the store)')
                elif 'not_in_macos_package' in marks:
                    row.update(standing='not-in-macos-package', texts=[],
                               absence=absence(unresolved['not_in_macos_package'][key], lock, packages_, reverse))
                elif 'no_publisher_text' in marks:
                    item = unresolved['no_publisher_text'][key]
                    row.update(standing='no-publisher-text', texts=[], declared_license=item['declared_license'],
                               repository=item['repository'], revision=item['revision'],
                               reason='a licence is stated and no publisher text was found: ' + item['examined'],
                               would_close=item['would_close'])
                elif 'gap_reasons' in marks:
                    item = unresolved['gap_reasons'][key]
                    row.update(standing='gap', texts=[], reason=item['reason'], would_close=item['would_close'])
                else:
                    row.update(standing='gap', texts=[], reason='the locked archive has no member named as a notice and no '
                               'text is held for this crate version',
                               would_close=f'an owner-permitted acquisition of the licence text {name} {version} names')
                if routes:
                    # The reading requirement follows the resolved route's repository, whichever route that is.
                    reading = repository in READING_REPOSITORIES
                    row['standing'] = 'held' if reading else 'text'
                    if reading:
                        row['reason'] = ('the text from ' + repository + ' awaits an owner licence reading for this supplier '
                                         'crate; no reading of the supplier\'s copy is recorded, and the App\'s reading of '
                                         '2026-11-12 is not extended to it')
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
            require(row['standing'] not in ('text', 'held') or row['texts'],
                    'a text or held package must have at least one text: ' + name + ' ' + version)
            rows.append(row)
    require(used_app == set(reused), 'an App-text association names no locked package without archive notices: '
            + str(sorted(set(reused) - used_app)))
    for name, collection in unresolved.items():
        unused = sorted(set(collection) - {key for n, key in used if n == name})
        require(not unused, f'{name} names a package no lockfile locks with that checksum: ' + str(unused[:3]))
    seen_publisher = {(r['name'], r['version'], r['checksum']) for r in rows if r.get('texts') and 'publisher_text' in r['texts'][0]}
    require(seen_publisher == set(published), 'a registry-source association names no locked package without another text '
            'route: ' + str(sorted(set(published) - seen_publisher)[:3]))
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
    for entry in associations.get('registry_sources', []):
        for text in entry['texts']:
            require(git_blob(held[text['sha256']]) == text['git_blob_sha1'], 'a registry-source text differs from the blob its '
                    'listing names: ' + entry['repository'] + ' ' + text['source_path'])
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
        item['texts'] = [{**{k: t[k] for k in t if k in ('member', 'received', 'app_text', 'publisher_text')}, 'sha256': t['sha256'], 'size_bytes': t['size_bytes'],
                          'package_path': package_path(repo, t, store)} for t in row['texts']]
        rows.append(item)
    return {'format': 'supplier-crate-packages/1', 'pin': associations['pin'], 'superset': associations['superset'],
            'selection': load(repo, INDEX)['selection'],
            'standings': STANDINGS,
            'macos_target': 'packages standing not-in-macos-package are absent from ' + MACOS_TARGET + ' by the target condition '
                            'their reverse dependencies declare, checked against the lockfile; no resolver was run and nothing '
                            'was read from the binaries',
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
        counts = by_lock.setdefault(row['lock'], {'packages': 0, 'registry': 0, 'git': 0, 'path': 0, **{k: 0 for k in STANDINGS}})
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
            raw = regular(repo, source[1])
            require(sha256(raw) == digest and len(raw) == size, 'an App-held text differs from its association: ' + source[1])
            put(raw)
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
