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
Never fetches, builds, executes supplier code or reads a cache. `--vendor DIR` additionally reads an
extracted supplier tree and checks the voice component versions against its sources.json.
"""
import argparse
import hashlib
import importlib.util
import json
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
# Crates whose held text comes from these repositories, or was received as an upstream text, are covered only by a
# valid owner reading; without one they are pending, never covered through another route.
READING_REQUIRED_REPOSITORIES = {'https://github.com/madsmtm/objc2'}
ROOT_TEXT_BASIS = ('repository root text at the crate\'s named revision (the project\'s Agent 0 accepted these as a '
                   'mechanical match: the text of the crate\'s declared licence from the repository and revision it names)')
# Every executable of the declared pin's tree (a regular file with an execute bit that is neither a .dylib library nor
# .json data; package_texts.executables) is a compiled program. Each must be a member of a component of kind
# compiled-dependencies, covered only with a committed lockfile and texts, or it stands uncovered.
COMPILED = 'compiled-dependencies'
LIMITS = [
    'An account of what the package is built to carry, from committed inputs; it is not read from a built package.',
    'A notice text is the publisher\'s licence or notice text for the component at the named version or revision; '
    'whether it satisfies the licence is not decided here, except where an owner licence reading is recorded.',
    'Supplier components inside an executable are as the supplier\'s build files and package records state; '
    'they are not read from the binaries. Texts in subdirectories of a component\'s repository are not included.',
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
    direct = direct_check.check(repo / 'app/packaging/notices', repo)
    index = transitive.check(repo / 'app/packaging/notices/transitive-index.json', repo)
    texts.check(repo)
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
        add({'class': 'library-content', 'name': content['name'], 'version': content['revision'][:12],
             'source': {'repository': content['repository'], 'revision': content['revision'], 'bundled_at': content['destination']},
             'texts': app_text}, COVERED, basis='LICENSE.md at the source revision equals the App\'s LICENSE.md, which ships')

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
        needs_reading = kind == 'received-upstream-text' or row['text'].get('repository') in READING_REQUIRED_REPOSITORIES
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
        add({'class': 'font', 'name': 'IBM Plex ' + family.capitalize(), 'version': upstream.get('version'),
             'source': {'package': upstream.get('package'), 'integrity': upstream.get('integrity')}, 'files': files,
             'texts': [text_entry(repo, license['path'], FONT_DESTINATION + PurePosixPath(license['path']).name)]},
            COVERED, basis=('the OFL text of the family\'s @fontsource tarball (the tarball members are recorded in the font index)'
                            if fonts['source']['declared_upstream_verified'] else 'the OFL text kept with the fonts; its upstream is not verified'))
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
    reviewed = table['reviewed_for_pin'] == pin
    by_path = {t['path']: t for t in texts.supplier_texts(repo)}
    claimed = {}
    ids = [item['id'] for item in table['components']]
    require(len(ids) == len(set(ids)), 'duplicate supplier component id')
    compiled_members = set()
    for item in table['components']:
        missing = [m for m in item['members'] + item['supplier_tree_texts'] if m not in tree]
        require(not reviewed or not missing, 'supplier component names a path not in the tree: ' + item['id'])
        for member in item['members']:
            claimed.setdefault(member, []).append(item['id'])
        for member in item['supplier_tree_texts']:
            claimed.setdefault(member, [])
        entry = {'class': 'supplier', 'id': item['id'], 'name': item['name'], 'version': item['version'],
                 'source': {'repository': item['repository'], 'revision': item['revision']}, 'members': item['members'],
                 'texts': [{**text_entry(repo, p, mapping[source_key(p)]),
                            **{k: by_path[p][k] for k in ('repository', 'revision', 'source_path', 'git_blob_sha1')},
                            **({'fetched_with_owner_permission': True} if by_path[p].get('fetched_with_owner_permission') else {})}
                           for p in item['texts']]
                          + [{'supplier_member': m, 'package_path': VENDOR_DESTINATION + m, 'size_bytes': tree[m]['size'],
                              'sha256': tree[m]['sha256']} for m in item['supplier_tree_texts'] if m in tree]}
        for key in ('declared_license', 'below_root', 'kind'):
            if key in item:
                entry[key] = item[key]
        if item.get('kind') == COMPILED:
            compiled_members.update(item['members'])
        require(item['standing'] in ('covered', 'uncovered'), 'unknown supplier standing: ' + item['id'])
        if item['standing'] == 'covered' and item.get('kind') == COMPILED:
            lock = item.get('lockfile')
            require(isinstance(lock, dict) and lock.get('path') and sha((repo / lock['path']).read_bytes()) == lock.get('sha256')
                    and item['texts'], 'covered compiled-in dependencies need a committed lockfile and texts: ' + item['id'])
            entry['lockfile'] = lock
            add(entry, COVERED, basis='licence texts of the packages the named lockfile locks')
        elif item['standing'] == 'covered':
            add(entry, COVERED, basis='texts of the repository and revision named' if item['texts']
                else 'licence texts the supplier ships in its tree, identified by the distribution record\'s digests')
        else:
            add(entry, UNCOVERED, reason=item['reason'], would_close=item['would_close'])
    unclaimed = sorted(set(tree) - set(claimed))
    if reviewed:
        require(not unclaimed, 'supplier members claimed by no component: ' + str(unclaimed))
    else:
        add({'class': 'supplier', 'id': 'component-table', 'name': 'Supplier component table', 'version': pin,
             'source': {'table': texts.SUPPLIER}, 'members': unclaimed, 'texts': []}, UNCOVERED,
            reason=f'the supplier component table was reviewed for {table["reviewed_for_pin"]}, not for the declared pin {pin}',
            would_close='review components.json against the declared pin\'s tree and set reviewed_for_pin')
    # The expectation that does not come from the table: every executable has a compiled-in dependency component.
    executables = texts.executables(record)
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
        check_vendor(vendor, table, tree)

    for path in ('app/packaging/notices/index.json', 'app/packaging/notices/transitive-index.json', texts.INPUTS, texts.SUPPLIER,
                 'app/packaging/font_notice/index.json', 'app/packaging/sqlite_notice/index.json', texts.OVERLAY):
        digest(path)
    counts = {s: sum(c['standing'] == s for c in components) for s in (COVERED, HELD, UNCOVERED)}
    keys = [component_key(c) for c in components]
    require(len(keys) == len(set(keys)), 'duplicate component in the account')
    return {'format': FORMAT, 'package': 'Chirality.app, macOS arm64', 'supplier_pin': pin,
            'supplier_distribution': {'record': record_path, 'manifest_sha256': record['inventory']['manifest_sha256']},
            'compiled_program_rule': 'every regular file of the tree with an execute bit that is neither a .dylib library nor .json '
                                     'data is a compiled program; each needs a compiled-dependencies component (covered only with a '
                                     'committed lockfile and texts) or stands uncovered',
            'supplier_table_reviewed_for_pin': table['reviewed_for_pin'], 'supplier_executables': executables,
            'inputs_sha256': dict(sorted(inputs_read.items())), 'counts': {**counts, 'total': len(components)},
            'open': [{'name': c['name'], 'version': c['version'], 'standing': c['standing'], 'reason': c['reason'],
                      **({'would_close': c['would_close']} if 'would_close' in c else {})}
                     for c in components if c['standing'] != COVERED],
            'standings': {COVERED: 'its notice text ships in the package', HELD: 'a text ships; its adequacy awaits the owner\'s licence reading',
                          UNCOVERED: 'no notice text ships'},
            'components': components, 'supplier_members': members, 'limits': LIMITS + table['limits']}


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


def check_vendor(vendor, table, tree):
    """Optional: compare the voice components with the extracted tree's own sources.json."""
    vendor = Path(vendor)
    for path, entry in tree.items():
        if path.endswith(('.json', '.md', '.txt')):
            require(sha((vendor / path).read_bytes()) == entry['sha256'], 'vendor file differs from the record: ' + path)
    sources = json.loads((vendor / table['voice_sources']['path']).read_bytes())
    stated = {s['url']: s['version'] for s in sources['sources'] if s['role'] == 'native-library'}
    for item in table['components']:
        if item['supplier_tree_texts']:
            require(stated.get(item['repository']) == item['version'], 'voice component differs from sources.json: ' + item['id'])


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
            'supplier_distribution': value['supplier_distribution']}


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
