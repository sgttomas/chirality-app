#!/usr/bin/env python3
"""The supplier's own records of its voice bundle, compared with the declared pin's distribution record and the voice rows.

`voice_records/<pin>/` holds byte-faithful copies of two members of the supplier tree, read once from the held
distribution archive: `codex-resources/voice/sources.json` (each library's version and source archive URL) and
`codex-resources/voice/manifest.json` (the build commit, version and target, and the digest of each bundled file).
`notices/coverage.py` calls `establish` on every generate and check:

- each copy is a regular non-link file whose size and SHA-256 equal its member in the distribution record;
- a repeated JSON key or any shape other than the one below refuses;
- the manifest's build commit, version and targets equal the record's source commit, the pin and the supported target,
  and every digest it lists equals that member's digest in the record;
- every voice row (a component with any member or text in the voice library, plugin or licence folders) is established by exactly one native-library entry of
  sources.json with its URL and version, every native-library entry establishes exactly one row, and each row's members
  and texts are files the manifest lists. A repeated or conflicting entry, or two rows for one entry, refuses; nothing is
  collapsed.

Neither record states which licence file belongs to which library, so which tree text is a voice row's notice is the
curated, reviewed association in components.json; it is not checked here.

These are the supplier's statements about its own bundle; the libraries' contents are not inspected, and no source
archive is read. `coverage.py --vendor DIR` applies the same comparison to an extracted tree's two files.
"""
import hashlib
import json
import re
import stat
from pathlib import Path

RECORDS = 'app/packaging/supplier_notices/voice_records'
# The copy in voice_records/<pin>/ -> the member of the supplier tree it is a copy of.
MEMBERS = {'sources.json': 'codex-resources/voice/sources.json', 'manifest.json': 'codex-resources/voice/manifest.json'}
SUPPORTED_TARGET = 'aarch64-apple-darwin'
# Where the bundled voice libraries sit in the supplier tree: their libraries, plugins and licence texts. A component with
# any member or text in these folders is a voice component, however its row is written: it is covered only through this
# comparison, with its source statement (notices/coverage.py). The voice folder's other files (the voice host, NOTICE.md
# and the two records) are the supplier's own and belong to its Codex row.
FOLDERS = ('codex-resources/voice/lib/', 'codex-resources/voice/plugins/', 'codex-resources/voice/licenses/')


def is_voice(component):
    return any(m.startswith(FOLDERS) for m in component['members'] + component['supplier_tree_texts'])
SOURCE_FIELDS = {'name', 'version', 'role', 'archive', 'root', 'url', 'sha256', 'provenance'}
ROLES = {'build-tool', 'native-library'}
HEX64 = re.compile('[0-9a-f]{64}')
HEX40 = re.compile('[0-9a-f]{40}')


def require(condition, message):
    if not condition:
        raise ValueError('voice records: ' + message)


def strict_json(raw, what):
    """JSON with no repeated key at any level."""
    def pairs(items):
        keys = [k for k, _ in items]
        require(len(keys) == len(set(keys)), what + ' repeats a key: ' + ', '.join(sorted({k for k in keys if keys.count(k) > 1})))
        return dict(items)
    try:
        return json.loads(raw, object_pairs_hook=pairs)
    except json.JSONDecodeError as error:
        raise ValueError('voice records: ' + what + ' is not JSON: ' + str(error)) from None


def text(value):
    return type(value) is str and value.strip() != ''


def digest(value, pattern):
    return type(value) is str and pattern.fullmatch(value) is not None


def parse_sources(raw):
    value = strict_json(raw, 'sources.json')
    require(type(value) is dict and set(value) == {'schema_version', 'sources', 'bundled_sources'}
            and type(value['schema_version']) is int and value['schema_version'] == 1 and type(value['sources']) is list
            and type(value['bundled_sources']) is list,
            'sources.json has an unsupported shape')
    for entry in value['sources']:
        require(type(entry) is dict and set(entry) == SOURCE_FIELDS and all(text(entry[k]) for k in SOURCE_FIELDS)
                and entry['role'] in ROLES and entry['url'].startswith('https://') and digest(entry['sha256'], HEX64),
                'sources.json has an unsupported source entry: ' + str(entry.get('name') if isinstance(entry, dict) else entry))
    for entry in value['bundled_sources']:
        require(type(entry) is dict and set(entry) == {'name', 'included_by', 'revision', 'path', 'provenance'}
                and all(text(entry[k]) for k in entry), 'sources.json has an unsupported bundled source entry')
    for field, entries in (('name', value['sources']), ('url', value['sources']), ('name', value['bundled_sources'])):
        values = [e[field] for e in entries]
        require(len(values) == len(set(values)), 'sources.json repeats an entry ' + field + ': '
                + ', '.join(sorted({v for v in values if values.count(v) > 1})))
    return value


def parse_manifest(raw):
    value = strict_json(raw, 'manifest.json')
    require(type(value) is dict and set(value) == {'schemaVersion', 'buildCommit', 'appTarget', 'voiceTarget', 'appVersion', 'sha256'}
            and type(value['schemaVersion']) is int and value['schemaVersion'] == 1 and digest(value['buildCommit'], HEX40)
            and all(text(value[k]) for k in ('appTarget', 'voiceTarget', 'appVersion')) and type(value['sha256']) is dict
            and value['sha256'] and all(text(k) and digest(v, HEX64) for k, v in value['sha256'].items()),
            'manifest.json has an unsupported shape')
    return value


def compare(sources_raw, manifest_raw, pin, record, rows):
    """{row id: {version, url, sources_entry}} for the voice rows, after every comparison passes; refuses otherwise."""
    sources, manifest = parse_sources(sources_raw), parse_manifest(manifest_raw)
    tree = {e['path']: e for e in record['inventory']['entries'] if e['kind'] == 'file'}
    require(record['pin'] == pin and record['package_metadata']['target'] == SUPPORTED_TARGET,
            'the distribution record is not for the declared pin and supported target')
    require(manifest['buildCommit'] == record['source_commit'], 'manifest.json names build commit ' + manifest['buildCommit']
            + ', not the distribution record\'s source commit')
    require(manifest['appVersion'] == pin, 'manifest.json names version ' + manifest['appVersion'] + ', not the pin ' + pin)
    require(manifest['appTarget'] == SUPPORTED_TARGET and manifest['voiceTarget'] == SUPPORTED_TARGET,
            'manifest.json names another target than ' + SUPPORTED_TARGET)
    for path, digest in manifest['sha256'].items():
        require(path in tree and tree[path]['sha256'] == digest, 'manifest.json lists a digest the distribution record does not '
                'have: ' + path)
    native = [e for e in sources['sources'] if e['role'] == 'native-library']
    for field in ('name', 'url'):
        values = [e[field] for e in native]
        require(len(values) == len(set(values)), 'sources.json names one native library ' + field + ' twice')
    established = {}
    used = {}
    for row in rows:
        matches = [e for e in native if e['url'] == row['repository']]
        require(len(matches) == 1, 'no single native-library entry of sources.json states the source of ' + row['id'])
        entry = matches[0]
        require(entry['version'] == row['version'], f'sources.json states {entry["name"]} {entry["version"]}, the table '
                f'{row["id"]} {row["version"]}')
        require(entry['name'] not in used, f'one native-library entry of sources.json ({entry["name"]}) would establish two voice '
                f'rows: {used.get(entry["name"])} and {row["id"]}')
        listed = [m for m in row['members'] + row['supplier_tree_texts'] if m not in manifest['sha256']]
        require(not listed, 'a voice row names files the supplier manifest does not list: ' + ', '.join(listed))
        used[entry['name']] = row['id']
        established[row['id']] = {'version': entry['version'], 'url': entry['url'], 'sources_entry': entry['name']}
    unused = sorted(e['name'] for e in native if e['name'] not in used)
    require(not unused, 'sources.json names native libraries no voice row accounts for: ' + ', '.join(unused))
    return established


def regular(path):
    require(stat.S_ISREG(path.lstat().st_mode), 'not a regular non-link file: ' + str(path))
    return path.read_bytes()


def establish(repo, pin, record, rows):
    """The committed copies for the pin, bound to the distribution record, then compared; None when none are held."""
    folder = Path(repo) / RECORDS / pin
    if not folder.exists():
        return None
    require(stat.S_ISDIR(folder.lstat().st_mode), 'the voice records folder is not a directory')
    names = sorted(p.name for p in folder.iterdir())
    require(names == sorted(MEMBERS), 'the voice records folder holds other files than ' + ', '.join(sorted(MEMBERS)))
    tree = {e['path']: e for e in record['inventory']['entries'] if e['kind'] == 'file'}
    raw = {}
    for name, member in MEMBERS.items():
        data = regular(folder / name)
        entry = tree.get(member)
        require(entry is not None and len(data) == entry['size'] and hashlib.sha256(data).hexdigest() == entry['sha256'],
                name + ' differs from ' + member + ' in the distribution record')
        raw[name] = data
    return {'records': {name: f'{RECORDS}/{pin}/{name}' for name in MEMBERS},
            'rows': compare(raw['sources.json'], raw['manifest.json'], pin, record, rows)}
