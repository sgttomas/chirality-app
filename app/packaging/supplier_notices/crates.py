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
- `check` needs no archive: the lockfiles, associations, index, texts and `packages.json` must agree exactly (every
  locked package has one row, every text exists once with its digest, nothing else is held).

A registry package with no archive notice may take its text through exactly one reviewed association in
`associations.json`: `app_texts` (the App's copy of the same archive) or `registry_sources` (the publisher's licence
files at the revision the archive's VCS record names, each bound to the blob and size a saved listing gives and held in
the store through another route). The 23 packages awaiting the owner's objc2 reading are a closed list here
(`HELD_FOR_READING`) and stay held whatever their rows say. A package with no text route may instead carry
`not_in_macos_package` (absence from the macOS target, derived by parsing the committed parent manifests under
`manifests/`), `no_publisher_text` (a licence is stated and no publisher text was found; open), or a specific gap reason
in `gap_reasons`. An association naming a package it cannot apply to refuses. `verify-manifests --archives MAP.json`
compares the committed registry parent manifests with their archives.

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
# The open question for these 23 supplier packages is whether the objc2 repository's LICENSE.md, a licensing overview, is
# adequate as the notice for each supplier copy; that reading is the owner's. Each stays held whatever text, repository
# spelling or route its row gives it, and no association can move it to text. The list is the checker's, not the curated
# associations': a listed identity that no lockfile locks refuses, so it cannot go stale unnoticed.
HELD_FOR_READING = frozenset({
    ('block2', '0.6.2', 'cdeb9d870516001442e364c5220d3574d2da8dc765554b4a617230d33fa58ef5'),
    ('dispatch2', '0.3.0', '89a09f22a6c6069a18470eb92d2298acf25463f14256d24778e1230d789a2aec'),
    ('objc2', '0.6.3', 'b7c2599ce0ec54857b29ce62166b0ed9b4f6f1a70ccc9a71165b6154caca8c05'),
    ('objc2-app-kit', '0.3.2', 'd49e936b501e5c5bf01fda3a9452ff86dc3ea98ad5f283e1455153142d97518c'),
    ('objc2-audio-toolbox', '0.3.2', '6948501a91121d6399b79abaa33a8aa4ea7857fe019f341b8c23ad6e81b79b08'),
    ('objc2-avf-audio', '0.3.2', '13a380031deed8e99db00065c45937da434ca987c034e13b87e4441f9e4090be'),
    ('objc2-cloud-kit', '0.3.2', '73ad74d880bb43877038da939b7427bba67e9dd42004a18b809ba7d87cee241c'),
    ('objc2-core-audio', '0.3.2', 'e1eebcea8b0dbff5f7c8504f3107c68fc061a3eb44932051c8cf8a68d969c3b2'),
    ('objc2-core-audio-types', '0.3.2', '5a89f2ec274a0cf4a32642b2991e8b351a404d290da87bb6a9a9d8632490bd1c'),
    ('objc2-core-data', '0.3.2', '0b402a653efbb5e82ce4df10683b6b28027616a2715e90009947d50b8dd298fa'),
    ('objc2-core-foundation', '0.3.2', '2a180dd8642fa45cdb7dd721cd4c11b1cadd4929ce112ebd8b9f5803cc79d536'),
    ('objc2-core-graphics', '0.3.2', 'e022c9d066895efa1345f8e33e584b9f958da2fd4cd116792e15e07e4720a807'),
    ('objc2-core-image', '0.3.2', 'e5d563b38d2b97209f8e861173de434bd0214cf020e3423a52624cd1d989f006'),
    ('objc2-core-location', '0.3.2', 'ca347214e24bc973fc025fd0d36ebb179ff30536ed1f80252706db19ee452009'),
    ('objc2-core-text', '0.3.2', '0cde0dfb48d25d2b4862161a4d5fcc0e3c24367869ad306b0c9ec0073bfed92d'),
    ('objc2-encode', '4.1.0', 'ef25abbcd74fb2609453eb695bd2f860d389e457f67dc17cafc8b8cbc89d0c33'),
    ('objc2-foundation', '0.3.2', 'e3e0adef53c21f888deb4fa59fc59f7eb17404926ee8a6f59f5df0fd7f9f3272'),
    ('objc2-io-surface', '0.3.2', '180788110936d59bab6bd83b6060ffdfffb3b922ba1396b312ae795e1de9d81d'),
    ('objc2-local-authentication', '0.3.2', 'e48e0b8b339e0d9d2ed4416b7f93f9d4daadff7d4dd797f89867cde11aeac607'),
    ('objc2-quartz-core', '0.3.2', '96c1358452b371bf9f104e21ec536d37a650eb10f7ee379fff67d2e08d537f1f'),
    ('objc2-security', '0.3.2', '709fe137109bd1e8b5a99390f77a7d8b2961dafc1a1c5db8f2e60329ad6d895a'),
    ('objc2-ui-kit', '0.3.2', 'd87d638e33c06f577498cbcc50491496a3ed4246998a7fbba7ccb98b1e7eab22'),
    ('objc2-user-notifications', '0.3.2', '9df9128cbbfef73cda168416ccf7f837b62737d748333bfe9ab71c245d76613e'),
})
# The exact text awaiting that reading (the objc2 repository's LICENSE.md, 1,339 bytes, blob 540ae4c8). The digest only
# identifies the text on a row; it never decides which packages are held.
OVERVIEW_TEXT = {'sha256': '7f976f7e9cb2d87df7230606feb932c3f21ac0e664045a775b600046ff850c54', 'size_bytes': 1339,
                 'git_blob_sha1': '540ae4c81adb5f64a9f61e222b688880da24300e'}
OBJC2_REPOSITORY = 'https://github.com/madsmtm/objc2'
# A second, independent guard: a package not on the list whose texts include the overview text, or whose canonical
# repository is the objc2 repository, is held too, so a new objc2 package at a later pin cannot pass as text.
READING_REPOSITORIES = {OBJC2_REPOSITORY}
# Every repository field of every association, in one form: no scheme variant, suffix, path or trailing slash.
CANONICAL_REPOSITORY = re.compile(r'^https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$')
# The macOS package's one target. A package is absent from it only when every declaration of it in every reverse
# dependency's manifest sits under a target condition that is false for this target (`target_holds`).
MACOS_TARGET = 'aarch64-apple-darwin'
# Literal target triples the absence rule knows; any other bare target key refuses.
KNOWN_TRIPLES = frozenset({
    'aarch64-apple-darwin', 'x86_64-apple-darwin', 'aarch64-apple-ios', 'x86_64-apple-ios', 'aarch64-apple-ios-sim',
    'i686-pc-windows-gnu', 'x86_64-pc-windows-gnu', 'i686-pc-windows-msvc', 'x86_64-pc-windows-msvc', 'aarch64-pc-windows-msvc',
    'x86_64-unknown-linux-gnu', 'aarch64-unknown-linux-gnu', 'i686-unknown-linux-gnu', 'x86_64-unknown-linux-musl',
    'aarch64-unknown-linux-musl', 'armv7-unknown-linux-gnueabihf', 'aarch64-linux-android', 'armv7-linux-androideabi',
    'i686-linux-android', 'x86_64-linux-android', 'x86_64-unknown-freebsd', 'wasm32-unknown-unknown', 'wasm32-wasip1',
    'wasm32-wasip2'})
STANDINGS = {'text': 'its texts ship (the basis says on what footing; adequacy is not decided here)',
             'held': 'held open for an owner licence reading (the reason says which text, if any, awaits it)',
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
        require(entry.get('texts'), 'an App-text association must have at least one text: ' + ', '.join(entry['packages']))
        for package in entry['packages']:
            name, version = package.split(' ')
            require((name, version, entry['checksum']) not in found, 'two App-text associations for ' + package)
            found[(name, version, entry['checksum'])] = entry
    return found


def canonical(repository, what):
    """A repository field in its one accepted form; anything else refuses."""
    require(isinstance(repository, str) and CANONICAL_REPOSITORY.fullmatch(repository) is not None
            and not repository.endswith('.git'), f'{what} names a repository not in the form https://github.com/<owner>/<repository>: '
            + repr(repository))
    return repository


def github_identity(url):
    """owner/repository, lower-cased, of a GitHub URL as a crate manifest may spell it (with .git, a path or a slash)."""
    match = re.fullmatch(r'https?://github\.com/([^/]+)/([^/#?]+?)(?:\.git)?(?:/.*)?', url or '')
    return (match.group(1) + '/' + match.group(2)).lower() if match else None


def positive(value):
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def file_identity(value, fields=('size_bytes', 'sha256')):
    """A recorded file identity: a positive size and well-formed digests."""
    return (isinstance(value, dict) and positive(value.get('size_bytes')) and HEX64.fullmatch(str(value.get('sha256'))) is not None
            and ('git_blob_sha1' not in fields or HEX40.fullmatch(str(value.get('git_blob_sha1'))) is not None))


def registry_sources(associations):
    """Reviewed publisher-text associations for registry packages, by (name, version, checksum); provenance checked.

    What the tool cannot see is the review boundary: a well-formed but wrong revision, another held text with consistent
    digests, or a lock identity moved between associations is caught only by the review of associations.json."""
    found = {}
    for entry in associations.get('registry_sources', []):
        require(isinstance(entry, dict) and set(entry) <= {'packages', 'repository', 'repository_basis', 'revision', 'listing', 'basis', 'texts'}
                and {'packages', 'repository', 'revision', 'listing', 'basis', 'texts'} <= set(entry),
                'unknown registry-source association shape')
        canonical(entry['repository'], 'a registry-source association')
        require(HEX40.fullmatch(str(entry['revision'])) is not None and isinstance(entry['basis'], str) and entry['basis'].strip(),
                'a registry-source association needs its publisher revision and basis: ' + entry['repository'])
        listing = entry['listing']
        require(isinstance(listing, dict) and set(listing) == {'read', 'entries', 'response_sha256'} and isinstance(listing['read'], str)
                and listing['read'].strip() and positive(listing['entries']) and HEX64.fullmatch(str(listing['response_sha256'])),
                'a registry-source association needs its listing identity (read, entries, response_sha256): ' + entry['repository'])
        require(entry['packages'], 'a registry-source association names no package: ' + entry['repository'])
        require(entry['texts'], 'a registry-source association must have at least one text: ' + entry['repository'])
        for text in entry['texts']:
            require(set(text) == {'source_path', 'size_bytes', 'sha256', 'git_blob_sha1', 'listing_blob', 'listing_size'}
                    and file_identity(text, ('size_bytes', 'sha256', 'git_blob_sha1')), 'unknown registry-source text shape: ' + entry['repository'])
            require(text['git_blob_sha1'] == text['listing_blob'] and text['size_bytes'] == text['listing_size'],
                    'a registry-source text is not the blob and size its listing names: ' + entry['repository'] + ' '
                    + text['source_path'])
            # The same name rule the archive route uses: a README or source file is not a notice.
            require(route.is_notice(text['source_path']), 'a registry-source text is not named as a notice: ' + text['source_path'])
        inferred = False
        for package in entry['packages']:
            require(isinstance(package, dict) and set(package) == {'name', 'version', 'checksum', 'path_in_vcs', 'archive_metadata',
                                                                   'archive_vcs_revision', 'archive_repository'},
                    'unknown registry-source package shape: ' + str(package.get('name') if isinstance(package, dict) else package))
            metadata = package['archive_metadata']
            require(isinstance(metadata, dict) and set(metadata) == {'Cargo.toml', '.cargo_vcs_info.json'}
                    and all(set(v) == {'size_bytes', 'sha256'} and file_identity(v) for v in metadata.values()),
                    'a registry-source package needs its archive Cargo.toml and .cargo_vcs_info.json identities: ' + package['name'])
            require(package['archive_vcs_revision'] == entry['revision'], 'the archive\'s VCS record names another revision than '
                    'the association: ' + package['name'])
            if package['archive_repository'] is None:
                inferred = True
            else:
                require(github_identity(package['archive_repository']) == github_identity(entry['repository']),
                        'the archive names another repository than the association: ' + package['name'])
            key = (package['name'], package['version'], package['checksum'])
            require(key not in found, 'two registry-source associations for ' + ' '.join(key[:2]))
            found[key] = entry
        require(not inferred or (isinstance(entry.get('repository_basis'), str) and entry['repository_basis'].strip()),
                'an archive that names no repository needs the association\'s stated basis: ' + entry['repository'])
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


TABLE_KIND = {'dependencies': 'normal', 'dev-dependencies': 'dev', 'dev_dependencies': 'dev', 'build-dependencies': 'build',
              'build_dependencies': 'build'}
TARGET_TABLE = re.compile(r"^\[target\.(?:'(?P<quoted>[^']*)'|\"(?P<dquoted>[^\"]*)\"|(?P<bare>[A-Za-z0-9_.-]+?))\."
                          r"(?P<table>dependencies|dev-dependencies|build-dependencies)(?:\.(?P<dependency>[A-Za-z0-9_-]+))?\]$")


def target_holds(spec, target=MACOS_TARGET):
    """Whether a target key holds for the target, over a closed set of forms: cfg(target_os = "..."), cfg(windows), and a
    literal triple from KNOWN_TRIPLES. Any other form refuses: absence is never inferred from a name or an unknown form."""
    os_name = {'aarch64-apple-darwin': 'macos'}[target]
    os_match = re.fullmatch(r'cfg\(target_os = "([a-z0-9_]+)"\)', spec)
    if os_match is not None:
        return os_match.group(1) == os_name
    if spec == 'cfg(windows)':
        return False
    if spec.startswith('cfg('):
        raise ValueError('a target condition outside the closed forms: ' + spec)
    require(spec in KNOWN_TRIPLES, 'a target key that is neither a closed cfg form nor a known triple: ' + spec)
    return spec == target


def header_target(table):
    """(target key, edge kind, dependency named by a dotted table) of a recorded target table header."""
    match = TARGET_TABLE.fullmatch(table)
    require(match is not None, 'not a target-specific dependency table: ' + table)
    spec = next(match.group(g) for g in ('quoted', 'dquoted', 'bare') if match.group(g) is not None)
    return spec, TABLE_KIND[match.group('table')], match.group('dependency')


def declarations(manifest, name):
    """Every declaration of `name` in a parsed manifest: [(target key or None, kind)], by key or by `package =` rename."""
    found = []

    def scan(tables, spec):
        for table_name, kind_ in TABLE_KIND.items():
            table = tables.get(table_name, {})
            require(isinstance(table, dict), 'a dependency table is not a table: ' + table_name)
            for key, value in table.items():
                renamed = value.get('package') if isinstance(value, dict) else None
                if (renamed or key) == name:
                    found.append((spec, kind_))
    scan(manifest, None)
    targets = manifest.get('target', {})
    require(isinstance(targets, dict), 'the manifest\'s target table is not a table')
    for spec, tables in targets.items():
        require(isinstance(tables, dict), 'a target entry is not a table: ' + spec)
        scan(tables, spec)
    return found


def manifests(repo, associations):
    """The committed parent manifests by id, each a regular file equal to its recorded identity."""
    found = {}
    for item in associations.get('manifests', []):
        require(isinstance(item, dict) and set(item) == {'id', 'path', 'size_bytes', 'sha256', 'git_blob_sha1', 'binding',
                                                         'declared_license', 'source', 'notice'}
                and file_identity(item, ('size_bytes', 'sha256', 'git_blob_sha1')) and item['id'] not in found
                and item['path'].startswith(BASE + '/manifests/'), 'unknown or repeated parent manifest entry: ' + str(item.get('id')))
        raw = regular(repo, item['path'])
        require((len(raw), sha256(raw), git_blob(raw)) == (item['size_bytes'], item['sha256'], item['git_blob_sha1']),
                'a committed parent manifest differs from its recorded identity: ' + item['path'])
        source = item['source']
        if source.get('kind') == 'registry-archive-member':
            require(set(source) == {'kind', 'name', 'version', 'checksum', 'member'} and source['member'] == 'Cargo.toml'
                    and HEX64.fullmatch(str(source['checksum'])), 'unknown registry manifest source: ' + item['id'])
        else:
            require(source.get('kind') == 'workspace-file' and set(source) == {'kind', 'repository', 'revision', 'source_path'}
                    and HEX40.fullmatch(str(source['revision'])) and source['source_path'].endswith('Cargo.toml'),
                    'unknown workspace manifest source: ' + item['id'])
            canonical(source['repository'], 'a workspace manifest')
        found[item['id']] = (item, raw)
    return found


def absence(entry, lock, packages, reverse, parents):
    """Absence from the macOS target, derived from the parent manifests themselves.

    The recorded reverse dependencies must equal the lockfile's. Each names its committed manifest, which must be the
    locked archive's Cargo.toml (by checksum) or the workspace file at the lockfile's repository and revision. Every
    declaration of the package in every dependency table of that manifest is found by parsing it, and each must sit under
    a target key that is false for the macOS target. The recorded edge lines are a cross-check that must equal the
    declarations found and the manifest's own lines, not the evidence."""
    require(set(entry) == {'lock', 'name', 'version', 'checksum', 'target', 'reverse_dependencies'} and entry['target'] == MACOS_TARGET,
            'unknown not-in-macOS-package shape: ' + str(entry.get('name')))
    key = (entry['name'], entry['version'])
    require(key in packages and packages[key].get('checksum') == entry['checksum'], 'not-in-macOS-package names no locked '
            'package with that checksum: ' + ' '.join(key))
    recorded = [(r['name'], r['version']) for r in entry['reverse_dependencies']]
    require(len(recorded) == len(set(recorded)) and set(recorded) == reverse.get(key, set()) and recorded,
            'the recorded reverse dependencies of ' + ' '.join(key) + ' differ from the lockfile\'s: recorded '
            + str(sorted(recorded)) + ', lockfile ' + str(sorted(reverse.get(key, set()))))
    evidence = []
    for dependent in entry['reverse_dependencies']:
        require(set(dependent) == {'name', 'version', 'manifest', 'edges'}, 'unknown reverse dependency shape: ' + str(dependent.get('name')))
        require(dependent['manifest'] in parents, 'a reverse dependency names no committed manifest: ' + dependent['name'])
        item, raw = parents[dependent['manifest']]
        source, parent = item['source'], packages[(dependent['name'], dependent['version'])]
        if kind(parent) == 'registry':
            require(source['kind'] == 'registry-archive-member' and (source['name'], source['version'], source['checksum'])
                    == (dependent['name'], dependent['version'], parent['checksum']),
                    'the manifest is not the locked archive\'s Cargo.toml: ' + dependent['name'])
        else:
            require(kind(parent) == 'path' and source['kind'] == 'workspace-file'
                    and (source['repository'], source['revision']) == (lock['repository'], lock['revision']),
                    'the workspace manifest is not at the lockfile\'s repository and revision: ' + dependent['name'])
        text = raw.decode()
        manifest = tomllib.loads(text)
        require(manifest.get('package', {}).get('name') == dependent['name'], 'the manifest is another package\'s: ' + dependent['name'])
        found = declarations(manifest, entry['name'])
        require(found, 'the manifest declares no dependency on ' + entry['name'] + ': ' + dependent['name'])
        for spec, _ in found:
            require(spec is not None, f'{entry["name"]} is declared without a target condition by {dependent["name"]}')
            require(not target_holds(spec), f'{entry["name"]} {entry["version"]} is declared for {MACOS_TARGET} by '
                    f'{dependent["name"]}: target {spec}')
        lines = text.splitlines()
        claimed = []
        for edge in dependent['edges']:
            require(set(edge) == {'table', 'table_line', 'line', 'text', 'kind'} and positive(edge['table_line'])
                    and positive(edge['line']) and edge['line'] >= edge['table_line'] and edge['line'] <= len(lines),
                    'unknown edge shape: ' + dependent['name'])
            require(lines[edge['table_line'] - 1].strip() == edge['table'] and lines[edge['line'] - 1].strip() == edge['text'],
                    'a recorded edge line differs from the manifest: ' + dependent['name'] + ' line ' + str(edge['line']))
            spec, edge_kind, _ = header_target(edge['table'])
            require(edge['kind'] == edge_kind, 'the edge kind differs from its table: ' + dependent['name'])
            claimed.append((spec, edge_kind))
        require(sorted(claimed) == sorted(found), 'the recorded edges differ from the declarations the manifest gives: '
                + dependent['name'] + ' recorded ' + str(sorted(claimed)) + ', manifest ' + str(sorted(found)))
        evidence.append({'name': dependent['name'], 'version': dependent['version'], 'manifest': item['path'],
                         'declarations': [{'target': spec, 'kind': k} for spec, k in sorted(found)]})
    return {'target': MACOS_TARGET, 'reverse_dependencies': evidence}


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


def parent_notices(item, rows_by_key, workspaces):
    """A parent manifest ships under a notice the account already carries: the crate's own row stands text with exactly
    the recorded texts, or, for a workspace file, the workspace texts of its lockfile."""
    notice, source = item['notice'], item['source']
    if source['kind'] == 'registry-archive-member':
        row = rows_by_key.get((source['name'], source['version'], source['checksum']))
        require(row is not None and row['standing'] == 'text' and set(notice) == {'crate_row', 'texts'}
                and [{k: t[k] for k in ('member', 'sha256')} for t in row['texts'] if 'member' in t] == notice['texts']
                and len(notice['texts']) == len(row['texts']),
                'a parent manifest\'s crate does not stand text with the recorded licence texts: ' + item['id'])
    else:
        texts = [t['path'] for w in workspaces if (w['repository'], w['revision']) == (source['repository'], source['revision'])
                 for t in w['texts']]
        require(set(notice) == {'workspace_texts'} and texts and notice['workspace_texts'] == texts,
                'a workspace manifest is not covered by its workspace\'s shipped texts: ' + item['id'])


def verify_manifests(repo, archives):
    """Archive-reading mode: each committed registry manifest equals the Cargo.toml member of its checksum-verified archive."""
    associations = load(repo, ASSOCIATIONS)
    archives = archive_map(archives)
    checked = []
    for item, raw in manifests(repo, associations).values():
        source = item['source']
        if source['kind'] != 'registry-archive-member':
            continue
        archive = Path(archives[f'{source["name"]}-{source["version"]}.crate']).read_bytes()
        member = route.read_member(archive, (source['name'], source['version']), source['checksum'], source['member'])
        require(member == raw, 'a committed manifest differs from its archive\'s Cargo.toml: ' + item['id'])
        checked.append(item['id'])
    return {'manifests_equal_to_archive_members': checked}


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
    # Every repository field of every association is in its one canonical form.
    for lock in associations['locks']:
        canonical(lock['repository'], 'lockfile association ' + lock['id'])
    for collection in ('workspaces', 'git_sources', 'app_texts', 'no_publisher_text'):
        for item in associations.get(collection, []):
            canonical(item['repository'], collection + ' entry')
    reused = app_texts(associations)
    published = registry_sources(associations)
    parents = manifests(repo, associations)
    unresolved = {name: keyed(associations, name) for name in ('not_in_macos_package', 'no_publisher_text', 'gap_reasons')}
    for name, collection in unresolved.items():
        for other, entries_ in unresolved.items():
            both = set(collection) & set(entries_) if other != name else set()
            require(not both, f'{name} and {other} both name ' + str(sorted(both)[:3]))
    used_app, used, listed_seen = set(), set(), set()
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
                               absence=absence(unresolved['not_in_macos_package'][key], lock, packages_, reverse, parents))
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
                    row['standing'] = 'text'
                reading = hold_for_reading(row, key, repository)
                if routes == ['app']:
                    require(reused[key]['reading_required'] == (reading is not None),
                            'an App-text association states another reading requirement than the rule: ' + name)
                if reading is not None:
                    listed_seen.add(key)
                    row.pop('would_close', None)
                    row.update(standing='held', reason=reading['reason'])
                    if reading.get('awaiting'):
                        row['awaiting_reading'] = reading['awaiting']
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
            require(row['standing'] != 'text' or row['texts'], 'a text package must have at least one text: ' + name + ' ' + version)
            require(row['standing'] != 'held' or row['texts'] or (row['name'], row['version'], row.get('checksum')) in HELD_FOR_READING,
                    'a held package must have at least one text: ' + name + ' ' + version)
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
    stale = sorted(HELD_FOR_READING - listed_seen)
    require(not stale, 'a package listed for the owner\'s objc2 reading is locked by no lockfile: ' + str(stale[:3]))
    rows_by_key = {(r['name'], r['version'], r.get('checksum')): r for r in rows}
    for item, _ in parents.values():
        parent_notices(item, rows_by_key, associations['workspaces'])
    return rows


def hold_for_reading(row, key, repository):
    """Whether a registry package is held for the owner's objc2 reading, and why; None when it is not.

    A listed package is held whatever text, spelling or route its row gives it. If its row does not carry the overview text
    it stays open too: no accepted evidence in this change establishes another text for it, and no substitution covers it.
    An unlisted package carrying the overview text, or from the objc2 repository, is held by the independent guard."""
    digests = [t['sha256'] for t in row['texts']]
    carries = OVERVIEW_TEXT['sha256'] in digests
    awaiting = {'sha256': OVERVIEW_TEXT['sha256'], 'size_bytes': OVERVIEW_TEXT['size_bytes'],
                'git_blob_sha1': OVERVIEW_TEXT['git_blob_sha1'],
                'question': 'whether the objc2 repository\'s LICENSE.md, a licensing overview, is adequate as the notice for '
                            'this supplier copy (the owner\'s reading)'}
    if key in HELD_FOR_READING:
        if carries:
            return {'awaiting': awaiting, 'reason': 'listed for the owner\'s reading: the objc2 repository\'s LICENSE.md (a '
                    'licensing overview, sha256 ' + OVERVIEW_TEXT['sha256'][:12] + ') ships and awaits that reading for this '
                    'supplier copy; no reading of the supplier\'s copy is recorded, and the App\'s reading of 2026-11-12 is not '
                    'extended to it'}
        found = ('another text (sha256 ' + ', '.join(d[:12] for d in digests) + ')') if digests else 'no text'
        return {'reason': 'listed for the owner\'s reading of the objc2 overview text, but this row carries ' + found + ' instead '
                'of that text; no accepted evidence establishes another notice for this package, so it stays open'}
    if carries or (repository is not None and repository in READING_REPOSITORIES):
        return {'awaiting': awaiting if carries else None,
                'reason': 'not on the named list for the owner\'s objc2 reading, but its row ' + ('carries the objc2 overview text'
                          if carries else 'comes from ' + OBJC2_REPOSITORY) + '; held until the list and the reading cover it'}
    return None


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
    v = sub.add_parser('verify-manifests', help='require each committed registry parent manifest to equal its checksum-verified '
                                                'archive\'s Cargo.toml member')
    v.add_argument('--archives', type=Path, required=True)
    sub.add_parser('check')
    sub.add_parser('generate', help='write crates/packages.json from the committed inputs')
    args = parser.parse_args()
    try:
        if args.command == 'index':
            result = write_index(REPO, args.archives)
        elif args.command == 'extract':
            result = extract(REPO, args.archives, args.received)
        elif args.command == 'verify-manifests':
            result = verify_manifests(REPO, args.archives)
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
