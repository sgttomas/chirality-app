#!/usr/bin/env python3
"""One account of every component the package ships and where its notice ships; a strict check refuses gaps.

`generate` writes coverage.json from committed inputs only: the direct and transitive indexes, the shipped
texts, the font and SQLite indexes, the supplier component table, the declared pin's distribution record and
coverage-inputs.json (owner readings, permitted texts, Library content). Each component gets one standing:

- covered: its notice text ships in the package (`basis` says on what footing);
- held-pending-owner-licence-reading: a text ships but its adequacy is for the owner to read;
- uncovered: no notice ships; `reason` and `would_close` say why and what would close it.

`check` regenerates and requires the committed account to be identical (it runs every underlying check).
`check --strict` also exits non-zero while any component is held or uncovered, naming each.
Never fetches, builds, executes supplier code or reads a cache. When the table is reviewed for the pin and the
supplier's own voice records are held (committed under supplier_notices/voice_records/<pin>/ and bound to the
distribution record; supplier_notices/voice.py), the voice rows' versions and source URLs are compared with them.
`--vendor DIR` additionally reads an extracted supplier tree and applies the same comparison to its own sources.json
and manifest.json.
"""
import argparse
import hashlib
import importlib.util
import json
import stat
from pathlib import Path, PurePosixPath
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
ACCOUNT = 'app/packaging/notices/coverage.json'
FORMAT = 'chirality.app.notice-coverage/1'
COVERED, HELD, UNCOVERED = 'covered', 'held-pending-owner-licence-reading', 'uncovered'
# Bundle destinations production_inputs/prepare.py gives the SQLite and font notices (beside the overlay).
SQLITE_DESTINATION = 'third-party-notices/sqlite-preparation/'
FONT_DESTINATION = 'third-party-notices/fonts/'
VENDOR_DESTINATION = 'codex/'
# An owner licence reading counts only in this closed form: answer -> the exact words of that answer.
READING_ANSWERS = {
    'Adequate as published': 'The App ships the publisher\'s own text as the notice for those nine, and the notices account '
                             'records that this was your reading.',
}
READING_FIELDS = {'ecosystem', 'package', 'version', 'text', 'decided_by', 'date', 'answer', 'statement'}
# Supplier components covered only by an owner licence reading, each in this closed form: the question as put, the
# answer the owner selected and that answer's description, exactly. Without a valid reading the row is pending.
SUPPLIER_READINGS = {
    'icu': {
        'question': 'One licence reading for the App\'s notices, held since 12 November and never put to you as a question '
                    '(my omission). ICU\'s licence text, which the App ships as its notice, mentions GPL terms for two '
                    'build-system files that are not part of the built library. Is the notice complete as published, or '
                    'should the two GPL texts ship as well?',
        'answer': 'ICU\'s licence text as published is complete',
        'answer_description': 'Nothing is added. The two files are build-system files, very likely not compiled into or '
                              'shipped with anything.',
    },
}
SUPPLIER_READING_FIELDS = {'decided_by', 'date', 'relayed_by', 'question', 'answer', 'answer_description'}
# Crates whose held text comes from these repositories, or was received as an upstream text, are covered only by a
# valid owner reading; without one they are pending, never covered through another route.
READING_REQUIRED_REPOSITORIES = {'https://github.com/madsmtm/objc2'}
ROOT_TEXT_BASIS = ('repository root text at the crate\'s named revision (the project\'s Agent 0 accepted these as a '
                   'mechanical match: the text of the crate\'s declared licence from the repository and revision it names)')
# Every executable of the declared pin's tree (a regular file with an execute bit that is neither a .dylib library nor
# .json data; package_texts.executables) is a compiled program. Each must be a member of a component of kind
# compiled-dependencies. Such a component is covered only by the supplier crate group (supplier_notices/crates.py): its
# lockfile is associated with the component's own repository and revision (the Codex one with the distribution record's
# source commit), and every package that lockfile locks has its text (none is held for a reading or a gap); otherwise
# it stands held or uncovered and the account names each open package.
COMPILED = 'compiled-dependencies'
# Rows with no route to covered in this change, whatever the table or the review record says. The change that
# establishes one of them removes its id here. The five ids this list held for 0.167.0 were removed for 0.169.0: the two
# crate groups by the lockfile, index and text correspondence that crates.py checks (they are evaluated by the rule
# above), the two LLVM CREDITS rows by their texts at the listed blobs, and those two and llvm-libc's subdirectory row by
# complete listings that name no licence file below the root.
DEFERRED = ()
LIMITS = [
    'An account of what the package is built to carry, from committed inputs; it is not read from a built package.',
    'A notice text is the publisher\'s licence or notice text for the component at the named version or revision; '
    'whether it satisfies the licence is not decided here, except where an owner licence reading is recorded.',
    'Supplier components inside an executable are as the supplier\'s build files and package records state; '
    'they are not read from the binaries. Below a repository\'s root, only the texts a row lists are included.',
    'Each bundle mapping is named by its exact source and destination; the App\'s own content files are bound by path, not '
    'by bytes. Copy routes other than bundle resources, the icon and a production plan\'s validated provisioning profile '
    'refuse; frontend assets embedded in the executable are not a copy route.',
]


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


texts = _load('coverage_package_texts', HERE / 'package_texts.py')
transitive = texts.transitive
direct_check = _load('coverage_direct_check', HERE / 'check.py')
font_check = _load('coverage_font_check', HERE.parent / 'font_notice/check.py')
bundle = _load('coverage_bundle_resources', HERE.parent / 'production_inputs/bundle_resources.py')
voice_records = _load('coverage_voice_records', HERE.parent / 'supplier_notices/voice.py')
# The repository identity (supplier_notices/crates.py), used only where it makes a check stricter than comparing as
# written: the reading rule and the Codex membership of a compiled row. Curated values are otherwise compared exactly.
same_repository = texts.supplier_crates.same_repository
require, sha = transitive.require, transitive.sha


def encode(value):
    return (json.dumps(value, indent=1, ensure_ascii=False) + '\n').encode()


def source_key(path):
    """Overlay/prepare source key for a repository path under app/ (relative to app/src-tauri)."""
    require(path.startswith('app/'), 'notice text outside app/: ' + path)
    return '../' + path.removeprefix('app/')


def text_entry(repo, path, destination):
    raw = (Path(repo) / path).read_bytes()
    return {'repository_path': path, 'package_path': destination, 'size_bytes': len(raw), 'sha256': sha(raw)}


def build(repo=REPO, vendor=None):
    repo = Path(repo)
    # A voice row's revision key is present (refused by name before anything, the review record's entries included,
    # indexes it); that its value is null is checked with the voice route below.
    for item in texts.load(repo, texts.SUPPLIER)['components']:
        require(not voice_records.is_voice(item) or 'revision' in item,
                'a voice component\'s revision must be present and null: ' + str(item.get('id')))
    # Then: the curated inputs and cache-made indexes must be the content the review record names.
    check_review_record(repo, texts.load(repo, texts.SUPPLIER))
    # Then: no copy route the account cannot name (a platform or alternate configuration, or a bundle key beyond
    # resources and the icon) before anything reads the configuration.
    bundle.base_bundle(repo / 'app')
    direct = direct_check.check(repo / 'app/packaging/notices', repo)
    index = transitive.check(repo / 'app/packaging/notices/transitive-index.json', repo)
    texts.check(repo)
    # The supplier crate group: lockfiles, associations, index, texts and the derived package account agree exactly.
    texts.supplier_crates.check(repo)
    fonts = font_check.check(repo)
    inputs = texts.load(repo, texts.INPUTS)
    mapping = texts.overlay(repo)['bundle']['resources']
    inputs_read = {}

    def digest(path):
        inputs_read[path] = sha((repo / path).read_bytes())

    def shipped(path):
        destination = mapping.get(source_key(path))
        require(destination is not None, 'notice text is not mapped into the package: ' + path)
        return text_entry(repo, path, destination)

    components = []

    def add(row, standing, basis=None, reason=None, would_close=None):
        row['standing'] = standing
        require((standing == COVERED) == (basis is not None) and (standing == COVERED) == (reason is None),
                'standing needs a basis when covered and a reason otherwise: ' + row['name'])
        require(standing != COVERED or row['texts'], 'covered component ships no text: ' + row['name'])
        require(standing != UNCOVERED or would_close, 'uncovered component needs what would close it: ' + row['name'])
        for key, value in (('basis', basis), ('reason', reason), ('would_close', would_close)):
            if value is not None:
                row[key] = value
        components.append(row)

    # The App itself, and the Library content it bundles under the same licence text.
    app = next(c for c in direct['components'] if c['ecosystem'] == 'app')
    app_text = [shipped('app/packaging/notices/' + n['asset']) for n in app['notices']]
    add({'class': 'app', 'name': app['package'], 'version': app['version'], 'declared_license': app['declared_license'],
         'source': {'repository': app['source']['repository'], 'revision': app['source']['revision']}, 'texts': app_text},
        COVERED, basis='the App\'s own LICENSE.md')
    # Every icon the bundle declares needs a provenance entry; one without stands uncovered.
    assets = {a['path']: a for a in inputs['app_assets']}
    icons = texts.load(repo, 'app/src-tauri/tauri.conf.json')['bundle'].get('icon', [])
    for icon in icons:
        path = 'app/src-tauri/' + icon
        asset = assets.pop(path, None)
        row = {'class': 'app-asset', 'name': 'App icon ' + icon, 'version': app['version'],
               'source': {'path': path, **({'added_by_commit': asset['added_by_commit']} if asset else {})}, 'texts': []}
        if asset is not None:
            raw = (repo / path).read_bytes()
            require(sha(raw) == asset['sha256'] and len(raw) == asset['size_bytes'], 'bundled icon differs from its provenance entry: ' + path)
            row.update(texts=app_text, provenance=asset['provenance'])
            add(row, COVERED, basis='the App\'s own asset, by its provenance entry; the App\'s LICENSE.md ships')
        else:
            add(row, UNCOVERED, reason='no provenance entry establishes who made this bundled icon',
                would_close='establish its origin from repository files and record it in coverage-inputs.json app_assets')
    require(not assets, 'provenance entry names no bundled icon: ' + str(sorted(assets)))
    app_license = (repo / 'LICENSE.md').read_bytes()
    for content in inputs['library_content']:
        require(sha(app_license) == content['license_sha256'], 'Library content licence differs from the App\'s LICENSE.md')
        require((repo / content['resource']).is_dir(), 'bundled Library content missing: ' + content['resource'])
        # The source each bundle names in its own record must be the one this entry states, and the record must be the
        # reviewed one (its digest is in this entry), since it is what lists the folder's members.
        record_path = content['source_record']['path']
        require(record_path.startswith(content['resource']), 'source record outside its bundle: ' + content['name'])
        require(sha((repo / record_path).read_bytes()) == content['source_record'].get('sha256'),
                'bundle source record differs from the reviewed one named in coverage-inputs.json: ' + content['name'])
        source = texts.load(repo, record_path)
        if content['source_record']['kind'] == 'workflow-manifest':
            require((source['source']['repository'], source['source']['commit'], source['source']['license']['sha256'])
                    == (content['repository'], content['revision'], content['license_sha256']),
                    'workflow bundle names another source or licence: ' + content['name'])
        else:
            require(content['source_record']['kind'] == 'role-set-binding' and source['basisCommit'] == content['revision'],
                    'instruction bundle names another source revision: ' + content['name'])
        listed, unlisted = folder_membership(repo, content, source)
        row = {'class': 'library-content', 'name': content['name'], 'version': content['revision'][:12],
               'mappings': [{'source': content['resource'], 'destination': content['destination'],
                             'members': {'files': listed, 'listed_by': record_path}}],
               'source': {'repository': content['repository'], 'revision': content['revision'], 'bundled_at': content['destination']},
               'texts': app_text}
        if unlisted:
            row['texts'] = []
            add(row, UNCOVERED, reason='the bundled folder differs from the members its source record lists: ' + ', '.join(unlisted),
                would_close='restore the folder to its source record, or rebundle it with its generator and review the new record')
        else:
            add(row, COVERED, basis='LICENSE.md at the source revision equals the App\'s LICENSE.md, which ships; the folder holds '
                                    'exactly the members its source record lists')

    # Cargo and npm runtime dependencies (direct ones are a subset of the transitive closure).
    plan = texts.planned(repo)
    readings = {}
    for reading in inputs['owner_licence_readings']:
        key = (reading.get('package'), reading.get('version'))
        require(key not in readings, 'duplicate owner reading: ' + str(key))
        readings[key] = reading
    received = {(s['package'], s['version']) for t in inputs['received_texts'] for s in t['subjects']}
    # Joined by ecosystem, name and version: a name alone would give one version's notices to another.
    direct_rows = {(c['ecosystem'], c['package'], c['version']): c for c in direct['components']}
    for row in index['cargo']:
        if row['source'] != 'registry':
            continue
        key = (row['package'], row['version'])
        prefix = f'cargo/{row["package"]}/{row["version"]}/'
        shipped_texts = [shipped(texts.TEXTS + '/' + p) for p in sorted(plan) if p.startswith(prefix)]
        component = direct_rows.get(('cargo', row['package'], row['version']))
        shipped_texts += [shipped('app/packaging/notices/' + n['asset']) for n in (component or {}).get('notices', [])]
        entry = {'class': 'cargo', 'relation': 'direct' if component else 'transitive', 'name': row['package'],
                 'version': row['version'], 'declared_license': row['declared_license'],
                 'source': {'registry': 'crates.io', 'archive_sha256': row['archive_sha256']}, 'texts': shipped_texts}
        kind = row['text']['kind']
        needs_reading = kind == 'received-upstream-text' or any(
            same_repository(row['text'].get('repository'), r) for r in READING_REQUIRED_REPOSITORIES)
        reading = readings.pop(key, None)
        if needs_reading:
            require(shipped_texts, 'a crate awaiting a reading must ship its held text: ' + row['package'])
            if reading is not None and reading_valid(reading, row):
                entry['owner_licence_reading'] = {k: reading[k] for k in ('decided_by', 'date', 'answer', 'statement')}
                add(entry, COVERED, basis='owner licence reading: the publisher\'s repository text ships as the notice')
            else:
                add(entry, HELD, reason='the held text ships; its adequacy awaits the owner\'s licence reading'
                    + ('' if reading is None else ' (the recorded reading is not an affirmative reading in the closed form)'))
        elif reading is not None:
            raise ValueError('owner reading names a crate that needs none: ' + row['package'])
        elif kind == 'archive-member':
            add(entry, COVERED, basis='licence files of the locked crate archive')
        elif shipped_texts and (kind == 'retained-root-texts' or key in received):
            locator = row['text']
            add(entry, COVERED, basis=ROOT_TEXT_BASIS + f': {locator["repository"]} at {locator["vcs_revision"]}')
        else:
            locator = row['text']
            add(entry, UNCOVERED, reason='the locked archive carries no licence text and none is held',
                would_close=f'an owner-permitted fetch of the root licence text of {locator.get("repository")} '
                            f'at {locator.get("vcs_revision")}')
    require(not readings, 'owner reading names no indexed crate: ' + str(sorted(readings)))
    for row in index['npm']:
        prefix = f'npm/{row["package"]}/{row["version"]}/'
        shipped_texts = [shipped(texts.TEXTS + '/' + p) for p in sorted(plan) if p.startswith(prefix)]
        component = direct_rows.get(('npm', row['package'], row['version']))
        shipped_texts += [shipped('app/packaging/notices/' + n['asset']) for n in (component or {}).get('notices', [])]
        entry = {'class': 'npm', 'relation': 'direct' if component else 'transitive', 'name': row['package'],
                 'version': row['version'], 'declared_license': row['declared_license'],
                 'source': {'registry': 'npmjs', 'integrity': row['integrity']}, 'texts': shipped_texts}
        if row['text']['kind'] in ('direct-index-archive', 'lock-tarball'):
            add(entry, COVERED, basis='licence files of the locked tarball')
        else:
            add(entry, UNCOVERED, reason='no licence text verified against the locked tarball',
                would_close='transitive.py associate-npm with a cache holding the locked tarball')

    # Fonts and SQLite (mapped by production_inputs/prepare.py beside the overlay).
    packages = {p['family']: p for p in fonts['upstream_packages']}
    for license in fonts['licenses']:
        family = license['family']
        files = [f['path'] for f in fonts['fonts'] if f['family'] == family]
        upstream = packages.get(family, {})
        row = {'class': 'font', 'name': 'IBM Plex ' + family.capitalize(), 'version': upstream.get('version'),
               'source': {'package': upstream.get('package'), 'integrity': upstream.get('integrity')}, 'files': files,
               'texts': [text_entry(repo, license['path'], FONT_DESTINATION + PurePosixPath(license['path']).name)]}
        # font_notice/check.py has already required, for a verified index, a tarball member for every file and licence.
        evidence = (fonts['source']['declared_upstream_verified'] and upstream.get('package') and upstream.get('integrity')
                    and license.get('upstream') and all(f.get('upstream') for f in fonts['fonts'] if f['family'] == family))
        if evidence:
            add(row, COVERED, basis='the OFL text of the family\'s @fontsource tarball; the font index records the tarball member of '
                                    'every file and of the licence')
        else:
            row['texts'] = []
            add(row, UNCOVERED, reason='no recorded upstream evidence ties the family\'s files and licence text to a published package',
                would_close='record the upstream package, integrity and tarball members with font_notice/check.py --generate --npm-cache')
    sqlite = texts.load(repo, 'app/packaging/sqlite_notice/index.json')
    header = next(a for a in sqlite['assets'] if a['path'] == 'sqlite3-source-header.txt')
    entry = text_entry(repo, 'app/packaging/sqlite_notice/' + header['path'], SQLITE_DESTINATION + header['path'])
    require(entry['sha256'] == header['sha256'], 'SQLite notice bytes differ')
    add({'class': 'sqlite', 'name': 'SQLite', 'version': sqlite['sqlite_version'],
         'source': {'bundled_by': f'{sqlite["crate"]} {sqlite["crate_version"]}', 'archive_sha256': sqlite['archive_sha256']},
         'texts': [entry]}, COVERED, basis='the public-domain dedication in the bundled sqlite3.c header')

    # The supplier tree of the declared pin and the components known inside it.
    pin, record_path, record = texts.supplier_record(repo)
    digest(record_path)
    table = texts.load(repo, texts.SUPPLIER)
    tree = {e['path']: e for e in record['inventory']['entries'] if e['kind'] == 'file'}
    require(len(tree) == sum(e['kind'] == 'file' for e in record['inventory']['entries']), 'the distribution record repeats a file')
    reviewed = table['reviewed_for_pin'] == pin
    supplier_texts = list(texts.supplier_texts(repo))
    by_path = {t['path']: t for t in supplier_texts}
    require(len(by_path) == len(supplier_texts), 'the supplier table repeats a text path')
    executables = texts.executables(record)
    # A component a lockfile association names is a compiled-dependencies component, covered only by its crate group,
    # and has at least one executable member. Which executable is built from which lockfile is the supplier's statement
    # in its source's build files: a review duty (README).
    locked_components = [lock['component'] for lock in texts.supplier_crates.load_associations(repo)['locks']]
    # When the table is reviewed for the pin and the records are held, the voice rows (components with a member or
    # supplier-tree text in the three folders voice.is_voice names) are compared with the supplier's own voice records
    # for this pin; any disagreement refuses. A voice row is covered only
    # when the comparison established its version and source URL and it ships only its texts from the supplier tree.
    require(table['voice_sources']['path'] == voice_records.MEMBERS['sources.json'], 'the table names another voice sources member')
    # Voice membership is decided before anything else: a component with a member or text in the voice library folders
    # takes the voice route and only that route, each voice member belongs to one component, and only a voice component
    # names supplier-tree texts, each under the voice licences folder.
    voice_owner = {}
    for item in table['components']:
        is_voice = voice_records.is_voice(item)
        require(not is_voice or (item.get('kind') != COMPILED and item['id'] not in SUPPLIER_READINGS
                                 and item['id'] not in DEFERRED and 'owner_licence_reading' not in item),
                'a voice component takes only the voice route (not compiled, reading or deferred): ' + item['id'])
        # No revision is recorded for a voice row: its source is the release URL the supplier states, and none is invented.
        require(not is_voice or item['revision'] is None, 'a voice component\'s revision must be present and null: ' + item['id'])
        require(not item['supplier_tree_texts'] or is_voice, 'only a voice component may name supplier-tree texts: ' + item['id'])
        require(all(t.startswith(voice_records.LICENCE_FOLDER) for t in item['supplier_tree_texts']),
                'a supplier-tree text must be a member under ' + voice_records.LICENCE_FOLDER + ': ' + item['id'])
        for member in item['members']:
            if member.startswith(voice_records.FOLDERS):
                require(member not in voice_owner, f'a voice member belongs to two components: {member} '
                        f'({voice_owner.get(member)} and {item["id"]})')
                voice_owner[member] = item['id']
    voice = voice_records.establish(repo, pin, record, [c for c in table['components'] if voice_records.is_voice(c)]) if reviewed else None
    for path in (voice or {}).get('records', {}).values():
        digest(path)
    claimed = {}
    ids = [item['id'] for item in table['components']]
    require(len(ids) == len(set(ids)), 'duplicate supplier component id')
    rows_by_id = {item['id']: item for item in table['components']}
    for component in locked_components:
        row = rows_by_id.get(component)
        require(row is not None and row.get('kind') == COMPILED,
                'a lockfile association names a component that is not a compiled-dependencies row: ' + component)
        require(any(m in executables for m in row['members']),
                'a compiled-dependencies component with a lockfile has no executable member: ' + component)
    require(set(DEFERRED) <= set(ids), 'a deferred supplier row is missing: ' + str(sorted(set(DEFERRED) - set(ids))))
    require(set(SUPPLIER_READINGS) <= set(ids), 'a supplier row awaiting a reading is missing: ' + str(sorted(set(SUPPLIER_READINGS) - set(ids))))
    compiled_members = set()
    for item in table['components']:
        is_voice = voice_records.is_voice(item)
        missing = [m for m in item['members'] + item['supplier_tree_texts'] if m not in tree]
        require(not reviewed or not missing, 'supplier component names a path not in the tree: ' + item['id'])
        for member in item['members']:
            claimed.setdefault(member, []).append(item['id'])
        for member in item['supplier_tree_texts']:
            claimed.setdefault(member, [])
        exceptions = {}
        for exception in item.get('text_exceptions', []):
            require(isinstance(exception.get('reason'), str) and exception['reason'].strip() and exception.get('path'),
                    'a text exception needs a path and a non-empty reason: ' + item['id'])
            exceptions[exception['path']] = exception['reason']
        require(set(exceptions) <= set(item['texts']), 'text exception names a text the component does not ship: ' + item['id'])
        entry = {'class': 'supplier', 'id': item['id'], 'name': item['name'], 'version': item['version'],
                 'source': {'repository': item['repository'], 'revision': item['revision']}, 'members': item['members'],
                 'texts': [{**text_entry(repo, p, mapping[source_key(p)]),
                            **{k: by_path[p][k] for k in ('repository', 'revision', 'source_path', 'git_blob_sha1')},
                            **({'fetched_with_owner_permission': True} if by_path[p].get('fetched_with_owner_permission') else {}),
                            **({'exception': exceptions[p]} if p in exceptions else {})}
                           for p in item['texts']]
                          + [{'supplier_member': m, 'source': 'inside the supplier tree', 'package_path': VENDOR_DESTINATION + m,
                              'size_bytes': tree[m]['size'], 'sha256': tree[m]['sha256']} for m in item['supplier_tree_texts'] if m in tree]}
        for key in ('declared_license', 'below_root', 'kind', 'reading_context'):
            if key in item:
                entry[key] = item[key]
        # The supplier tree is one mapping, the selected vendor tree, whose members are the distribution record's files.
        # Only a reviewed table names it; an unreviewed one leaves it to the open component-table row below.
        require(set(item.get('accounts_for', [])) <= {VENDOR_DESTINATION}, 'a supplier row may name only the vendor tree: ' + item['id'])
        if reviewed and item.get('accounts_for'):
            entry['mappings'] = [vendor_mapping(record_path, tree)]
        require(item['standing'] in ('covered', 'uncovered', 'pending'), 'unknown supplier standing: ' + item['id'])
        reading = item.get('owner_licence_reading')
        require(reading is None or item['id'] in SUPPLIER_READINGS, 'owner reading names a supplier row that needs none: ' + item['id'])
        if reading is not None:
            entry['owner_licence_reading'] = reading
        # Every committed text must come from the component's own repository and revision (its recorded source or an
        # also_at identity for the same blob), or be a named exception.
        foreign = [p for p in item['texts'] if (item['repository'], item['revision']) not in text_identities(by_path[p])
                   and p not in exceptions]
        if item.get('kind') == COMPILED:
            twice = sorted(set(item['members']) & compiled_members & set(executables))
            require(not twice, 'an executable belongs to two compiled-dependencies components: ' + ', '.join(twice))
            compiled_members.update(item['members'])
        if item['id'] in DEFERRED:
            add(entry, UNCOVERED, reason=item.get('reason') or 'deferred: this row has no route to covered in this change',
                would_close=item.get('would_close') or 'the change that establishes this row removes it from coverage.DEFERRED')
        elif item.get('kind') == COMPILED and reviewed:
            compiled_group(repo, item, entry, record, mapping, add)
        elif item.get('kind') == COMPILED:
            add(entry, UNCOVERED, reason=f'the component table associates this row for {table["reviewed_for_pin"]}, not for the declared '
                                         f'pin {pin}; that association is not carried forward',
                would_close='review components.json against the declared pin\'s tree and set reviewed_for_pin')
        elif not reviewed:
            # An association made for another pin is not carried forward, whatever standing it had there.
            add(entry, UNCOVERED, reason=f'the component table associates this row for {table["reviewed_for_pin"]}, not for the declared '
                                         f'pin {pin}; that association is not carried forward',
                would_close='review components.json against the declared pin\'s tree and set reviewed_for_pin')
        elif identity_gaps(item):
            # Checked before any text or exception: a component without its own identity has nothing to match texts to.
            add(entry, UNCOVERED, reason='the component\'s own identity is incomplete: ' + '; '.join(identity_gaps(item)),
                would_close='record the component\'s repository (or, for a supplier-tree text, its source URL) and revision')
        elif is_voice:
            voice_route(item, entry, voice, pin, add)
        elif item['standing'] == 'covered' and foreign:
            add(entry, UNCOVERED, reason='a shipped text records another repository or revision than the component: ' + ', '.join(foreign),
                would_close='ship the component\'s own texts, or name each other text as an exception with its reason')
        elif item['standing'] == 'covered' and not item['texts']:
            raise ValueError('covered supplier component ships no text: ' + item['id'])
        elif item['id'] in SUPPLIER_READINGS and not (item['standing'] == 'covered' and supplier_reading_valid(reading, item['id'])):
            add(entry, HELD, reason=item.get('reason') or 'the held text ships; its adequacy awaits the owner\'s licence reading'
                + ('' if reading is None else ' (the recorded reading is not in the closed form)'))
        elif item['id'] in SUPPLIER_READINGS:
            add(entry, COVERED, basis=f'owner licence reading ({reading["date"]}): {reading["answer"]}; the text recorded at the '
                                      'component\'s own repository and revision ships unchanged')
        elif item['standing'] == 'covered':
            add(entry, COVERED, basis='texts recorded at the component\'s own repository and revision')
        elif item['standing'] == 'pending':
            add(entry, HELD, reason=item['reason'])
        else:
            add(entry, UNCOVERED, reason=item['reason'], would_close=item['would_close'])
    # After the rows, so that each comparison above refuses first with its own message; then the form of the non-voice
    # repository fields (check_repository_forms), an additional refusal.
    check_repository_forms(table)
    unclaimed = sorted(set(tree) - set(claimed))
    if reviewed:
        require(not unclaimed, 'supplier members claimed by no component: ' + str(unclaimed))
    else:
        add({'class': 'supplier', 'id': 'component-table', 'name': 'Supplier component table', 'version': pin,
             'mappings': [vendor_mapping(record_path, tree)],
             'source': {'table': texts.SUPPLIER}, 'members': sorted(tree), 'texts': []}, UNCOVERED,
            reason=f'the supplier component table was reviewed for {table["reviewed_for_pin"]}, not for the declared pin {pin}; '
                   'no row of it counts as covered for this tree',
            would_close='review components.json against the declared pin\'s tree and set reviewed_for_pin')
    # Expectations that do not come from the table. The executable rule fits this distribution record; the record's own
    # Mach-O count must equal executables plus .dylib members, and every one of them must belong to a component.
    machos = executables + sorted(p for p in tree if p.endswith('.dylib'))
    require(len(machos) == record['macho_files'], f'executables and libraries ({len(machos)}) differ from the record\'s '
            f'Mach-O count ({record["macho_files"]}); the executable rule does not fit this record')
    for path in machos:
        require(claimed.get(path) or not reviewed, 'Mach-O member belongs to no component: ' + path)
    for path in executables:
        if path not in compiled_members:
            claimed.setdefault(path, []).append('compiled-in:' + path)
            add({'class': 'supplier', 'id': 'compiled-in:' + path, 'kind': COMPILED, 'name': 'Dependencies compiled into ' + path,
                 'version': pin, 'source': {'distribution_record': record_path}, 'members': [path], 'texts': []}, UNCOVERED,
                reason='the executable is a compiled program and no component states its compiled-in dependencies',
                would_close='a compiled-dependencies component in components.json naming this executable, covered with its lockfile and texts')
    members = [{'path': p, 'size': tree[p]['size'], 'sha256': tree[p]['sha256'], 'package_path': VENDOR_DESTINATION + p,
                'components': claimed.get(p, [])} for p in sorted(tree)]
    if vendor is not None:
        check_vendor(vendor, table, tree, pin, record)

    # Every mapping the bundle is given is named in the account by its exact source and destination: in a row's
    # mappings, or as the repository path and package path of a text a row ships. A folder mapping is named only with
    # a membership record (the Library bundles' own records, the vendor tree's distribution record). The mappings are
    # what a production preparation selects (bundle_resources.selected: the base configuration's resources, the
    # overlays and the SQLite and font notices; any other copy route refuses there), plus the two caller-selected
    # mappings it adds: the vendor tree and an explicitly selected upstream supplement. A claim must name a mapping
    # that exists; a destination prefix names nothing.
    selected = bundle.selected(repo / 'app', [l['path'] for l in fonts['licenses']])
    mapped = set(bundle.pairs(selected)) | {(bundle.VENDOR_SOURCE, VENDOR_DESTINATION)} | set(SUPPLEMENT_PAIRS)
    for item in inputs['app_resources']:
        require(set(item) == {'name', 'mappings', 'note'} and item['mappings'], 'unknown app_resources entry shape: ' + str(item.get('name')))
        for pair in item['mappings']:
            require(set(pair) == {'source', 'destination'} and not pair['source'].endswith('/') and not pair['destination'].endswith('/'),
                    'App content names each file mapping exactly (a folder needs a membership record): ' + item['name'])
            source = repo / texts.safe(pair['source'])
            require(stat.S_ISREG(source.lstat().st_mode),
                    'App content source must be a regular non-link file: ' + pair['source'])
        add({'class': 'app-content', 'name': item['name'], 'version': app['version'], 'mappings': item['mappings'],
             'source': {'repository': app['source']['repository']}, 'texts': app_text}, COVERED,
            basis='the App\'s own content under the App\'s licence; the App\'s LICENSE.md ships as its notice')
    index_pairs = [(src, dst) for dst, src in NOTICE_INDEX_SOURCES.items() if (src, dst) in mapped]
    add({'class': 'notices', 'name': 'Third-party notices and their indexes', 'version': app['version'],
         'mappings': [{'source': src, 'destination': dst} for src, dst in [*index_pairs, *SUPPLEMENT_PAIRS]],
         'source': {'note': 'each licence text is named by the repository and package paths of the component row that ships it'},
         'texts': [text_entry(repo, src, dst) for src, dst in index_pairs if dst != NOTICE_ACCOUNT]},
        COVERED, basis='these are the notices: the licence texts are named by their components\' rows, and the index and '
                       'account files are named here; an explicitly selected upstream supplement (receipts.py check_stage: '
                       'exactly ' + ' and '.join(bundle.SUPPLEMENT_FILES) + ') is placed under ' + bundle.SUPPLEMENT_DESTINATION)
    claims = [(m['source'], m['destination']) for c in components for m in c.get('mappings', [])]
    claims += [(t['repository_path'], t['package_path']) for c in components for t in c['texts'] if 'repository_path' in t]
    for claim in claims:
        require(claim in mapped, 'an account row claims a mapping that does not exist: ' + ' -> '.join(claim))
    for component in components:
        for text in component['texts']:
            # A supplier-tree text is a member of the vendor tree mapping, identified by the distribution record.
            require('repository_path' in text or (text.get('supplier_member') in tree
                                                  and text['package_path'] == VENDOR_DESTINATION + text['supplier_member']),
                    'a shipped text is not in any bundle mapping: ' + str(text.get('package_path')))
    for src, dst in sorted(mapped - set(claims)):
        add({'class': 'resource', 'name': 'Unnamed bundle resource ' + dst, 'version': app['version'],
             'mappings': [{'source': src, 'destination': dst}], 'texts': []}, UNCOVERED,
            reason='the bundle maps this source to this destination and no account row names that mapping',
            would_close='a row naming this exact mapping, with its notice or the basis on which it is the App\'s own content')
    for path in ('app/packaging/notices/index.json', 'app/packaging/notices/transitive-index.json', texts.INPUTS, texts.SUPPLIER,
                 'app/packaging/font_notice/index.json', 'app/packaging/sqlite_notice/index.json', texts.OVERLAY, REVIEW):
        digest(path)
    counts = {s: sum(c['standing'] == s for c in components) for s in (COVERED, HELD, UNCOVERED)}
    keys = [component_key(c) for c in components]
    require(len(keys) == len(set(keys)), 'duplicate component in the account')
    return {'format': FORMAT, 'package': 'Chirality.app, macOS arm64', 'supplier_pin': pin,
            'supplier_distribution': {'record': record_path, 'manifest_sha256': record['inventory']['manifest_sha256']},
            'compiled_program_rule': 'for this distribution record, every regular file with an execute bit that is neither a .dylib '
                                     'library nor .json data is a compiled program (checked against the record\'s Mach-O count); '
                                     'each has a compiled-dependencies component, covered only when every package its associated '
                                     'lockfile locks has its text or is recorded absent from the macOS target by declared target '
                                     'condition (supplier_notices/crates.py)',
            'review_record': REVIEW,
            'supplier_table_reviewed_for_pin': table['reviewed_for_pin'], 'supplier_executables': executables,
            'inputs_sha256': dict(sorted(inputs_read.items())), 'counts': {**counts, 'total': len(components)},
            'open': [{'name': c['name'], 'version': c['version'], 'standing': c['standing'], 'reason': c['reason'],
                      **({'would_close': c['would_close']} if 'would_close' in c else {})}
                     for c in components if c['standing'] != COVERED],
            'standings': {COVERED: 'its notice text ships in the package', HELD: 'a text ships; its adequacy awaits the owner\'s licence reading',
                          UNCOVERED: 'no notice text ships'},
            'components': components, 'supplier_members': members, 'limits': LIMITS + table['limits']}


REVIEW = 'app/packaging/notices/coverage-review.json'
# Curated judgments, and the indexes generators make from caches CI does not hold (their archive claims are rechecked
# only by the cache-reading checks: transitive.py check --cargo-home/--npm-cache, check.py --archives,
# font_notice/check.py --npm-cache, sqlite_notice/check.py --archive). Binding them makes a change to what they
# claim a visible, reviewed change.
REVIEWED_FILES = ('app/packaging/supplier_notices/components.json', 'app/packaging/supplier_notices/crates/associations.json',
                  'app/packaging/supplier_notices/crates/index.json', 'app/packaging/notices/coverage-inputs.json',
                  'app/packaging/notices/index.json', 'app/packaging/notices/transitive-index.json',
                  'app/packaging/font_notice/index.json', 'app/packaging/sqlite_notice/index.json')


def review_entries(table):
    """What the review record must list: each supplier component's identity, standing and exact texts."""
    rows = []
    for item in table['components']:
        rows.append({'id': item['id'], 'standing': item['standing'], 'version': item['version'], 'revision': item['revision'],
                     'texts': item['texts'], 'supplier_tree_texts': item['supplier_tree_texts'], 'accounts_for': item.get('accounts_for', []),
                     'text_exceptions': sorted(e['path'] for e in item.get('text_exceptions', []))})
    return rows


def check_review_record(repo, table):
    """The curated inputs must equal what the review record says was reviewed (a statement, not a proof)."""
    record = texts.load(repo, REVIEW)
    require(set(record) == {'format', 'statement', 'updated_by', 'reviewed_in', 'files_sha256', 'supplier_components'}
            and record['format'] == 'notice-coverage-review/1', 'unknown review record shape')
    for path, expected in record['files_sha256'].items():
        require(sha((Path(repo) / path).read_bytes()) == expected,
                f'{path} differs from the review record; its reviewer must update {REVIEW} after reviewing the change')
    bound = set(REVIEWED_FILES) | {texts.supplier_record(repo)[1]}
    require(set(record['files_sha256']) == bound, 'review record must bind every curated input, cache-made index and the '
            'declared pin\'s distribution record (a pin move changes which record is bound): ' + str(sorted(bound ^ set(record['files_sha256']))))
    require(record['supplier_components'] == review_entries(table),
            'supplier components differ from the review record; its reviewer must update ' + REVIEW)


NOTICE_ACCOUNT = 'third-party-notices/coverage.json'
# The notice index and account files, each from exactly this repository source.
NOTICE_INDEX_SOURCES = {
    'third-party-notices/index.json': 'app/packaging/notices/index.json',
    'third-party-notices/transitive-index.json': 'app/packaging/notices/transitive-index.json',
    NOTICE_ACCOUNT: ACCOUNT,
    'third-party-notices/fonts/index.json': 'app/packaging/font_notice/index.json',
    'third-party-notices/sqlite-preparation/index.json': 'app/packaging/sqlite_notice/index.json',
    'third-party-notices/sqlite-preparation/README.md': 'app/packaging/sqlite_notice/README.md',
    'third-party-notices/sqlite-preparation/libsqlite3-sys.LICENSE': 'app/packaging/sqlite_notice/libsqlite3-sys.LICENSE',
    'third-party-notices/supplier/crates/packages.json': 'app/packaging/supplier_notices/crates/packages.json',
}
SUPPLEMENT_PAIRS = [(bundle.SUPPLEMENT_SOURCE + name, bundle.SUPPLEMENT_DESTINATION + name) for name in bundle.SUPPLEMENT_FILES]


def unaccounted(named, mappings):
    """Mappings (source, destination) that no account entry names exactly."""
    named = {tuple(entry) for entry in named}
    return sorted(tuple(m) for m in set(map(tuple, mappings)) if tuple(m) not in named)


def vendor_mapping(record_path, tree):
    return {'source': bundle.VENDOR_SOURCE, 'destination': VENDOR_DESTINATION,
            'members': {'files': len(tree), 'listed_by': record_path}}


def folder_membership(repo, content, record):
    """(number of listed files, differences) for a bundled Library folder against the members its source record lists."""
    root = Path(repo) / content['resource']
    record_name = content['source_record']['path'].removeprefix(content['resource'])
    listed = {record_name: None}
    if content['source_record']['kind'] == 'workflow-manifest':
        for package in record['packages']:
            for item in package['files']:
                listed[package['name'] + '/' + item['path']] = (item['bytes'], item['sha256'])
    else:
        listed[record['roleSet']['path']] = (None, record['roleSet']['sha256'])
        for item in record['guidance']:
            listed[item['path']] = (item['byteLength'], item['sha256'])
    held, odd = {}, []
    for path in sorted(root.rglob('*')):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink() or not (path.is_file() or path.is_dir()):
            odd.append(relative)
        elif path.is_file():
            held[relative] = path
    differences = [p + ' (link or special file)' for p in odd]
    differences += [p + ' (not listed)' for p in sorted(set(held) - set(listed))]
    differences += [p + ' (listed, not held)' for p in sorted(set(listed) - set(held))]
    for relative, expected in sorted(listed.items()):
        if expected is not None and relative in held:
            raw = held[relative].read_bytes()
            if sha(raw) != expected[1] or (expected[0] is not None and len(raw) != expected[0]):
                differences.append(relative + ' (differs from its listed digest)')
    return len(listed), differences


def text_identities(text):
    """(repository, revision) pairs a committed supplier text is recorded at: its source and each also_at identity."""
    return {(text['repository'], text['revision'])} | {(o['repository'], o['revision']) for o in text.get('also_at', [])}


CODEX_REPOSITORY = 'https://github.com/openai/codex'


def compiled_group(repo, item, entry, record, mapping, add):
    """Standing of a compiled-dependencies component from the supplier crate group (supplier_notices/crates.py)."""
    group = texts.supplier_crates.group(repo, item['id'])
    if group is None:
        add(entry, UNCOVERED, reason='no lockfile in supplier_notices/crates is associated with this component',
            would_close='associate the lockfile that builds this executable, with every locked package\'s text')
        return
    lock = group['lock']
    # Compared as written, as on main: any difference in spelling, suffix or letter case refuses.
    require((lock['repository'], lock['revision']) == (item['repository'], item['revision']),
            'the crate group\'s lockfile is for another repository or revision than the component: ' + item['id'])
    require(not same_repository(item['repository'], CODEX_REPOSITORY) or item['revision'] == record['source_commit'],
            'a Codex compiled-dependencies component must be at the distribution record\'s source commit: ' + item['id'])
    rows = group['packages']
    seen = {}
    for row in rows:
        for text in row['texts']:
            seen.setdefault(text['package_path'], text)
    by_destination = {dst: src for src, dst in mapping.items()}
    shipped = []
    for destination, text in sorted(seen.items()):
        source = by_destination.get(destination)
        require(source is not None, 'a crate text is not mapped into the package: ' + destination)
        found = text_entry(repo, 'app/' + source.removeprefix('../'), destination)
        require(found['sha256'] == text['sha256'], 'a crate text differs from its package account: ' + destination)
        shipped.append(found)
    entry['texts'] = shipped
    standings = texts.supplier_crates.STANDINGS
    require({r['standing'] for r in rows} <= set(standings), 'a crate package has an unknown standing: ' + item['id'])
    counts = {k: sum(r['standing'] == k for r in rows) for k in standings}
    kinds = {k: sum(r['source_kind'] == k for r in rows) for k in ('registry', 'git', 'path')}
    entry['lockfile'] = {k: lock[k] for k in ('path', 'sha256', 'repository', 'revision', 'source_path', 'binding')}
    entry['packages'] = {'total': len(rows), **kinds, **counts, 'account': 'third-party-notices/supplier/crates/packages.json',
                         'superset': 'every package the lockfile locks, on every platform and feature; some may not be compiled '
                                     'into the macOS executables. Only packages standing not-in-macos-package are recorded as '
                                     'absent, by declared target condition'}
    # Recorded absence from the macOS target is the only standing besides text that does not hold the group open, and the
    # account names every such package with its evidence. A package with no publisher text stays open, like a gap.
    excluded = [r for r in rows if r['standing'] == 'not-in-macos-package']
    entry['excluded_packages'] = [{'name': r['name'], 'version': r['version'], 'checksum': r['checksum'], 'absence': r['absence']}
                                  for r in excluded]
    open_rows = [r for r in rows if r['standing'] in texts.supplier_crates.OPEN]
    require(len(open_rows) + len(excluded) + counts['text'] == len(rows), 'a crate package standing is neither open, text nor absent')
    entry['open_packages'] = [{'name': r['name'], 'version': r['version'], 'standing': r['standing'], 'reason': r['reason']}
                              for r in open_rows]
    computed = 'covered' if not open_rows else 'uncovered'
    require(item['standing'] == computed, f'the table says {item["standing"]} for {item["id"]}, and its crate group is {computed}')
    unshipped = counts['gap'] + counts['no-publisher-text']
    if unshipped:
        add(entry, UNCOVERED, reason=f'of the {len(rows)} locked packages, {counts["gap"]} have no text, {counts["no-publisher-text"]} '
                                     f'state a licence with no publisher text found, and {counts["held"]} await an owner licence '
                                     f'reading ({len(excluded)} are recorded absent from the macOS package and named under '
                                     'excluded_packages): ' + ', '.join(f'{r["name"]} {r["version"]}' for r in open_rows),
            would_close='each open package\'s licence text (an owner-permitted acquisition), for one with no publisher text the '
                        'owner\'s decision on what may serve as its notice, and for a held one the owner\'s reading')
    elif counts['held']:
        add(entry, HELD, reason=f'{counts["held"]} locked packages await an owner licence reading: '
                                + ', '.join(f'{r["name"]} {r["version"]}' for r in open_rows))
    else:
        add(entry, COVERED, basis=f'every one of the {len(rows) - len(excluded)} packages the associated lockfile locks for the macOS '
                                  'package has its text in the package (archive notice members selected by name, Git-source licence '
                                  'files at the locked revision, publisher texts at the archive\'s named revision, or the workspace\'s '
                                  f'texts); {len(excluded)} are recorded absent from the macOS target by declared target condition; '
                                  'the set is otherwise a superset of what is compiled, and adequacy is not decided here')


def voice_route(item, entry, voice, pin, add):
    """The only route of a voice component: covered only when the supplier's voice records establish it, with its texts
    from the supplier tree and nothing else, carrying its source statement."""
    if item['standing'] == 'covered' and voice is None:
        add(entry, UNCOVERED, reason=f'the supplier\'s voice records for {pin} are not held, so this row\'s version and source are '
                                     'not established by them',
            would_close=f'commit the pin\'s voice/sources.json and voice/manifest.json under {voice_records.RECORDS}/{pin}/')
    elif item['standing'] == 'covered' and (item['texts'] or item.get('text_exceptions') or not item['supplier_tree_texts']):
        add(entry, UNCOVERED, reason='a voice component is covered only by its licence texts in the supplier tree, with its '
                                     'source established by the voice records; this row names another text or route',
            would_close='name the component\'s licence texts under the voice licences folder (supplier_tree_texts) and no other text')
    elif item['standing'] == 'covered':
        require(item['id'] in voice['rows'], 'a voice row is not established by the voice records: ' + item['id'])
        entry['source_statement'] = {**voice['rows'][item['id']], 'records': sorted(voice['records'].values())}
        add(entry, COVERED, basis='licence texts the supplier ships in its tree, identified by the distribution record\'s digests; '
                                  'the component is identified by its source URL')
    elif item['standing'] == 'pending':
        add(entry, HELD, reason=item['reason'])
    else:
        add(entry, UNCOVERED, reason=item['reason'], would_close=item['would_close'])


# The other hosts a non-voice repository field of the component table may name, as exact prefixes.
OTHER_REPOSITORY_PREFIXES = ('https://chromium.googlesource.com/',)


def check_repository_forms(table):
    """Every non-voice repository field of the component table (components, texts, also_at) is either
    https://github.com/<owner>/<repository> in the form crates.canonical_form checks (each of owner and repository one
    or more letters, digits, `_`, `.` or `-`, neither of them `.` or `..`, no `.git` suffix in any letter case) or
    begins with exactly https://chromium.googlesource.com/; anything else refuses, naming the field. A check of form,
    not that such a repository exists. The googlesource values are compared
    exactly wherever they are compared and are otherwise not constrained in form. A voice row's repository is the source
    URL the supplier's sources.json states and is compared with it exactly. A null or missing field is not a form and
    is left to main's checks: a text's or also_at identity's refuses (package_texts.supplier_texts), a component's null
    repository goes to its identity and lock checks (a row with committed texts stays uncovered), and a component's
    missing key stops the build with a KeyError."""
    canonical = texts.supplier_crates.canonical_form
    fields = [(f'components[{item["id"]}].repository', item.get('repository'))
              for item in table['components'] if not voice_records.is_voice(item)]
    fields += [(f'texts[{text["path"]}].repository', text.get('repository')) for text in table['texts']]
    fields += [(f'texts[{text["path"]}].also_at[{index}].repository', other.get('repository'))
               for text in table['texts'] for index, other in enumerate(text.get('also_at', []))]
    for where, repository in fields:
        require(repository is None or canonical(repository)
                or (type(repository) is str and repository.startswith(OTHER_REPOSITORY_PREFIXES)),
                'a repository field is neither exactly https://github.com/<owner>/<repository> nor under '
                + ' or '.join(OTHER_REPOSITORY_PREFIXES) + ': ' + where)


def identity_gaps(item):
    """What the component's own identity lacks, independently of its texts and exceptions."""
    def present(value):
        return isinstance(value, str) and value.strip() != ''
    gaps = []
    if item['texts'] and not (present(item.get('repository')) and present(item.get('revision'))):
        gaps.append('committed texts need the component\'s own repository and revision')
    if item['supplier_tree_texts'] and not (present(item.get('repository')) and item['repository'].startswith('https://')):
        gaps.append('a supplier-tree text needs the component\'s source URL (as the supplier\'s sources.json states it)')
    if item.get('revision') is not None and not present(item['revision']):
        gaps.append('a revision, when recorded, must be non-empty')
    return gaps


def supplier_reading_valid(reading, component):
    """An owner reading for a supplier row in its closed form: the question, answer and description exactly."""
    import re
    expected = SUPPLIER_READINGS[component]
    return (isinstance(reading, dict) and set(reading) == SUPPLIER_READING_FIELDS and reading['decided_by'] == 'owner'
            and isinstance(reading['date'], str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', reading['date']) is not None
            and isinstance(reading['relayed_by'], str) and reading['relayed_by'].strip() != ''
            and all(reading[key] == value for key, value in expected.items()))


def component_key(component):
    if component['class'] == 'supplier':
        return 'supplier:' + component['id']
    return f"{component['class']}:{component['name']}@{component['version']}"


def removed(previous, value, inputs):
    """Components in the previous account that the new one drops without a reviewed statement in coverage-inputs.json."""
    stated = {r['key'] for r in inputs.get('removed_components', []) if isinstance(r, dict) and r.get('reason')}
    before = {component_key(c) for c in previous.get('components', [])}
    after = {component_key(c) for c in value['components']}
    return sorted(before - after - stated)


def reading_valid(reading, row):
    """An affirmative owner reading in the closed form, for exactly this crate and version."""
    import re
    return (isinstance(reading, dict) and set(reading) == READING_FIELDS and reading['ecosystem'] == 'cargo'
            and (reading['package'], reading['version']) == (row['package'], row['version'])
            and reading['decided_by'] == 'owner' and isinstance(reading['date'], str)
            and re.fullmatch(r'\d{4}-\d{2}-\d{2}', reading['date']) is not None
            and reading['answer'] in READING_ANSWERS and reading['statement'] == READING_ANSWERS[reading['answer']])


def check_vendor(vendor, table, tree, pin, record):
    """Optional: the extracted tree's data files equal the record, and its own voice records give the same comparison."""
    vendor = Path(vendor)
    for path, entry in tree.items():
        if path.endswith(('.json', '.md', '.txt')):
            require(sha((vendor / path).read_bytes()) == entry['sha256'], 'vendor file differs from the record: ' + path)
    sources = json.loads((vendor / table['voice_sources']['path']).read_bytes())
    stated = {s['url']: s['version'] for s in sources['sources'] if s['role'] == 'native-library'}
    for item in table['components']:
        if item['supplier_tree_texts']:
            require(stated.get(item['repository']) == item['version'], 'voice component differs from sources.json: ' + item['id'])
    voice_records.compare((vendor / voice_records.MEMBERS['sources.json']).read_bytes(),
                          (vendor / voice_records.MEMBERS['manifest.json']).read_bytes(), pin, record,
                          [c for c in table['components'] if voice_records.is_voice(c)])


def check(repo=REPO, vendor=None, base_account=None):
    """Regenerate and require the committed account to be identical; returns its digest, counts and open list."""
    repo = Path(repo)
    value = build(repo, vendor)
    committed = (repo / ACCOUNT).read_bytes()
    require(committed == encode(value), 'coverage.json is stale; regenerate with coverage.py generate')
    if base_account is not None:
        dropped = removed(json.loads(Path(base_account).read_bytes()), value, texts.load(repo, texts.INPUTS))
        require(not dropped, 'components dropped from the base account without a reviewed statement: ' + ', '.join(dropped))
    return {'sha256': sha(committed), 'counts': value['counts'], 'open': value['open'], 'supplier_pin': value['supplier_pin'],
            'supplier_distribution': value['supplier_distribution'],
            # Mappings the account's rows name (an "Unnamed bundle resource" row names none; it is in the open list).
            'mappings': sorted({(m['source'], m['destination']) for c in value['components'] if c['class'] != 'resource'
                                for m in c.get('mappings', [])}
                               | {(t['repository_path'], t['package_path']) for c in value['components'] for t in c['texts']
                                  if 'repository_path' in t})}


def generate(repo=REPO, vendor=None):
    """Write the account; refuse to drop a component the committed account has unless coverage-inputs.json states it."""
    repo = Path(repo)
    value = build(repo, vendor)
    target = repo / ACCOUNT
    require(target.exists(), 'no committed account to compare with; restore coverage.json before generating')
    dropped = removed(json.loads(target.read_bytes()), value, texts.load(repo, texts.INPUTS))
    require(not dropped, 'components would be dropped without a reviewed statement in coverage-inputs.json removed_components: '
            + ', '.join(dropped))
    target.write_bytes(encode(value))
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    g = sub.add_parser('generate'); g.add_argument('--vendor', type=Path)
    c = sub.add_parser('check'); c.add_argument('--vendor', type=Path)
    c.add_argument('--base-account', type=Path, help='an earlier coverage.json (for example the base branch\'s); a component '
                                                     'it has that the current account drops must be stated in removed_components')
    c.add_argument('--strict', action='store_true', help='exit non-zero while any component is held or uncovered')
    args = parser.parse_args()
    try:
        if args.command == 'generate':
            generate(vendor=args.vendor)
        result = check(vendor=args.vendor, base_account=getattr(args, 'base_account', None))
    except (ValueError, KeyError, TypeError, OSError, StopIteration) as error:
        print(json.dumps({'coverage_account_match': False, 'error': str(error)}), file=sys.stderr)
        return 1
    print(json.dumps({'coverage_account_match': True, **result}, indent=1))
    if getattr(args, 'strict', False) and result['open']:
        for item in result['open']:
            print(f"not covered: {item['name']} {item['version']} ({item['standing']}): {item['reason']}", file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
