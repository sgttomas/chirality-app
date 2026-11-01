#!/usr/bin/env python3
"""Check this bounded direct-runtime notice input; never build, fetch or execute suppliers."""
import argparse
import base64
import copy
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
sys.path.insert(0, str(HERE.parent))
from inventory import scan

FORMAT = 'chirality.app.direct-runtime-notices/v2'
LEGACY_FORMAT = 'chirality.app.direct-runtime-notices/v1'
TARGET = 'aarch64-apple-darwin'
BASIS = ('app/package.json', 'app/package-lock.json', 'app/src-tauri/Cargo.toml', 'app/src-tauri/Cargo.lock')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(path):
    def unique(pairs):
        value = {}
        for key, item in pairs:
            require(key not in value, 'duplicate JSON field: ' + key)
            value[key] = item
        return value
    return json.loads(Path(path).read_bytes(), object_pairs_hook=unique)


def relative(value):
    require(isinstance(value, str) and '\\' not in value and not any(ord(c) < 32 for c in value), 'invalid relative path')
    require(not PurePosixPath(value).is_absolute() and all(p not in ('', '.', '..') for p in value.split('/')), 'noncanonical relative path')
    return value


def cargo_runtime_declarations(manifest):
    """Explicit macOS arm64 selection, not host auto-detection or a cfg evaluator."""
    selected = {name: ['all'] for name in manifest.get('dependencies', {})}
    predicates = {
        'cfg(target_os = "macos")': True, 'cfg(unix)': True,
        'cfg(target_family = "unix")': True, 'aarch64-apple-darwin': True,
        'cfg(windows)': False, 'cfg(target_os = "windows")': False,
        'cfg(target_family = "windows")': False, 'cfg(target_os = "linux")': False,
        'x86_64-apple-darwin': False, 'x86_64-pc-windows-msvc': False,
        'aarch64-pc-windows-msvc': False,
    }
    for condition, table in manifest.get('target', {}).items():
        dependencies = table.get('dependencies', {})
        if not dependencies:
            continue  # build/dev-only target declarations are outside runtime scope
        require(condition in predicates, 'unsupported runtime target condition; explicit scope adoption needed: ' + condition)
        if predicates[condition]:
            for name in dependencies:
                selected.setdefault(name, []).append(condition)
    for name, selectors in selected.items():
        for selector in selectors:
            definition = manifest['dependencies'][name] if selector == 'all' else manifest['target'][selector]['dependencies'][name]
            require(not isinstance(definition, dict) or definition.get('package', name) == name,
                    'renamed runtime dependency requires explicit package selection: ' + name)
        selected[name] = sorted(selectors)
    return selected


def check(root=HERE, repo=REPO, overlay=None):
    root, repo = Path(root), Path(repo)
    index = load(root / 'index.json')
    version = index.get('format')
    require(version in (FORMAT, LEGACY_FORMAT), 'unknown notice index shape/version')
    fields = {'format', 'scope', 'source_basis', 'components', 'unresolved_supplier_inputs', 'limits'}
    if version == FORMAT:
        fields.add('target')
        require(index.get('target') == TARGET, 'notice target differs')
    require(set(index) == fields, 'unknown notice index shape')
    basis = index['source_basis']
    require(set(basis) == {'app_revision', 'manifest_sha256'} and re.fullmatch('[0-9a-f]{40}', basis['app_revision']), 'invalid source basis')
    require(set(basis['manifest_sha256']) == set(BASIS), 'manifest basis differs')
    for path, digest in basis['manifest_sha256'].items():
        require(sha((repo / path).read_bytes()) == digest, 'manifest/lock changed: ' + path)
    npm = load(repo / 'app/package.json')
    npm_lock = load(repo / 'app/package-lock.json')['packages']
    cargo = cargo_runtime_declarations(tomllib.loads((repo / 'app/src-tauri/Cargo.toml').read_text()))
    if version == LEGACY_FORMAT:
        require(all(selectors == ['all'] for selectors in cargo.values()), 'legacy notice index cannot describe target-specific runtime scope')
    cargo_lock = tomllib.loads((repo / 'app/src-tauri/Cargo.lock').read_text())['package']
    app_lock = next(p for p in cargo_lock if p['name'] == 'chirality-app-v4')
    expected = {('app', 'chirality-app'): npm['version']}
    selected = {}
    for name in cargo:
        parts = next(d.split() for d in app_lock['dependencies'] if d.split()[0] == name)
        matches = [p for p in cargo_lock if p['name'] == name and (len(parts) == 1 or p['version'] == parts[1])]
        require(len(matches) == 1, 'ambiguous locked direct dependency: ' + name)
        selected[name] = matches[0]
        expected['cargo', name] = matches[0]['version']
    expected.update({('npm', name): version for name, version in npm['dependencies'].items()})
    found, assets = set(), {}
    for component in index['components']:
        component_fields = {'ecosystem', 'package', 'version', 'declared_license', 'source', 'notices'}
        if index['format'] == FORMAT:
            component_fields.update(('declaration_targets', 'notice_gap'))
        require(set(component) == component_fields, 'unexpected component fields')
        kind, name, version = component['ecosystem'], component['package'], component['version']
        key = kind, name
        if index['format'] == FORMAT:
            require(component['declaration_targets'] == (cargo.get(name) if kind == 'cargo' else ['all']), 'runtime declaration target differs: ' + name)
        require(key not in found and expected.get(key) == version, 'duplicate, extra or wrong-version runtime component: ' + name)
        found.add(key)
        source = component['source']
        require(source['kind'] == ('git' if kind == 'app' else kind), 'source kind differs')
        if kind == 'cargo':
            locked = selected[name]
            require(set(source) == {'kind', 'registry', 'archive_filename', 'archive_sha256', 'archive_size_bytes', 'manifest_member', 'manifest_sha256'}, 'unexpected Cargo source fields')
            require(source['registry'] == locked['source'] and source['archive_sha256'] == locked['checksum'], 'Cargo lock identity differs')
            require(source['archive_filename'] == name + '-' + version + '.crate' and source['manifest_member'] == name + '-' + version + '/Cargo.toml', 'Cargo archive path differs')
        elif kind == 'npm':
            require(set(source) == {'kind', 'resolved', 'integrity', 'archive_sha256', 'archive_size_bytes', 'manifest_member', 'manifest_sha256'}, 'unexpected npm source fields')
            locked = npm_lock['node_modules/' + name]
            require(source['resolved'] == locked['resolved'] and source['integrity'] == locked['integrity'] and source['manifest_member'] == 'package/package.json', 'npm lock identity differs')
        else:
            require(set(source) == {'kind', 'repository', 'revision', 'blob'} and source['revision'] == basis['app_revision'] and source['repository'] == 'https://github.com/sgttomas/chirality-app', 'App source identity differs')
        if index['format'] == LEGACY_FORMAT:
            require(component['notices'], 'component has no notice inputs')
        elif component['notices']:
            require(component['notice_gap'] is None, 'provided notice component cannot carry a missing-text assertion')
        else:
            gap = component['notice_gap']
            require(kind == 'cargo' and isinstance(gap, dict), 'missing notice requires exact Cargo source gap')
            require(set(gap) == {'reason', 'repository', 'revision', 'path_in_vcs', 'vcs_info_member', 'vcs_info_sha256', 'readme_member', 'readme_sha256', 'readme_license_link'}, 'unknown notice gap fields')
            require(gap['reason'] == 'locked_archive_contains_no_root_notice_text', 'unknown notice gap reason')
            require(re.fullmatch('[0-9a-f]{40}', gap['revision']) and gap['repository'].startswith('https://'), 'invalid notice source locator')
            require(gap['vcs_info_member'] == name + '-' + version + '/.cargo_vcs_info.json' and gap['readme_member'] == name + '-' + version + '/README.md', 'notice provenance member differs')
            require(all(re.fullmatch('[0-9a-f]{64}', gap[k]) for k in ('vcs_info_sha256', 'readme_sha256')), 'invalid notice provenance digest')
            relative(gap['path_in_vcs'])
            require(gap['readme_license_link'] == '../../LICENSE.md', 'unknown notice link')
        for notice in component['notices']:
            require(set(notice) == {'asset', 'source_path', 'archive_member', 'size_bytes', 'sha256'}, 'unexpected notice fields')
            path, origin = relative(notice['asset']), relative(notice['source_path'])
            expected_path = 'assets/app/' + origin if kind == 'app' else f'assets/{kind}/{name}/{version}/{origin}'
            require(path == expected_path and path not in assets, 'duplicate or misplaced notice asset')
            require(type(notice['size_bytes']) is int and notice['size_bytes'] >= 0 and re.fullmatch('[0-9a-f]{64}', notice['sha256']), 'invalid notice digest/size')
            if kind == 'app':
                require(origin == 'LICENSE.md' and notice['archive_member'] is None and component['declared_license'] == 'MIT', 'App notice source differs')
                raw = (repo / origin).read_bytes()
                require(sha(raw) == notice['sha256'] and hashlib.sha1(b'blob %d\0' % len(raw) + raw).hexdigest() == source['blob'], 'App source bytes/blob differ')
            else:
                prefix = name + '-' + version + '/' if kind == 'cargo' else 'package/'
                require(notice['archive_member'] == prefix + origin, 'notice archive member differs')
            assets[path] = notice
    require(found == set(expected), 'missing direct runtime component')
    tree = scan(root / 'assets')
    require(all(e['kind'] in ('dir', 'file') for e in tree['entries']), 'linked or special notice asset refused')
    files = {'assets/' + e['path']: e for e in tree['entries'] if e['kind'] == 'file'}
    require(set(files) == set(assets), 'missing or extra notice assets')
    for path, notice in assets.items():
        require((files[path]['sha256'], files[path]['size']) == (notice['sha256'], notice['size_bytes']), 'notice bytes/size differ: ' + path)
    expected_dirs = {str(p) for path in files for p in PurePosixPath(path).parents if str(p) not in ('.', 'assets')}
    require({'assets/' + e['path'] for e in tree['entries'] if e['kind'] == 'dir'} == expected_dirs, 'extra or missing asset directories')
    base = load(repo / 'app/packaging/unsigned/tauri.development.conf.json')
    expected_overlay = copy.deepcopy(base)
    for path in ['index.json', *assets]:
        expected_overlay['bundle']['resources']['../packaging/notices/' + path] = 'third-party-notices/' + path
    overlay = Path(overlay) if overlay else repo / 'app/packaging/unsigned/tauri.notices.conf.json'
    require(load(overlay) == expected_overlay, 'explicit notice overlay differs from base plus exact indexed resources')
    for ordinary in [base, load(repo / 'app/src-tauri/tauri.conf.json')]:
        require(not any(s.startswith('../packaging/notices/') or d.startswith('third-party-notices/') for s, d in ordinary['bundle']['resources'].items()), 'notices enabled on ordinary route')
    return index


def check_archives(index, repo, cargo_home, npm_cache):
    """Independent read-only comparison to locked local archives; no extraction/fetch."""
    count = 0
    for component in index['components']:
        source = component['source']
        if source['kind'] == 'git':
            raw = subprocess.check_output(['git', '-C', str(repo), 'show', source['revision'] + ':LICENSE.md'],
                                          env=dict(os.environ, GIT_NO_LAZY_FETCH='1', GIT_NO_REPLACE_OBJECTS='1'))
            require(sha(raw) == component['notices'][0]['sha256'], 'selected Git source differs')
            continue
        if source['kind'] == 'cargo':
            matches = list((Path(cargo_home) / 'registry/cache').glob('*/' + source['archive_filename']))
            require(len(matches) == 1, 'exact Cargo archive unavailable/ambiguous: ' + component['package'])
            archive = matches[0]
        else:
            algorithm, encoded = source['integrity'].split('-', 1)
            require(algorithm == 'sha512', 'unsupported npm integrity algorithm')
            digest = base64.b64decode(encoded, validate=True).hex()
            archive = Path(npm_cache) / '_cacache/content-v2' / algorithm / digest[:2] / digest[2:4] / digest[4:]
        raw = archive.read_bytes()
        require(sha(raw) == source['archive_sha256'] and len(raw) == source['archive_size_bytes'], 'cached archive digest/size differs')
        if source['kind'] == 'npm':
            require(hashlib.sha512(raw).digest() == base64.b64decode(source['integrity'].split('-', 1)[1], validate=True), 'npm integrity differs')
        with tarfile.open(archive) as tar:
            members = tar.getmembers()
            names = [m.name for m in members]
            require(len(names) == len(set(names)), 'duplicate archive members')
            def read(member):
                require(tar.getmember(member).isfile(), 'archive input is not a regular file')
                return tar.extractfile(member).read()
            manifest = read(source['manifest_member'])
            require(sha(manifest) == source['manifest_sha256'], 'package manifest differs')
            metadata = tomllib.loads(manifest.decode())['package'] if source['kind'] == 'cargo' else json.loads(manifest)
            require(metadata['name'] == component['package'] and metadata['version'] == component['version'] and metadata.get('license') == component['declared_license'], 'package identity/license metadata differs')
            prefix = source['manifest_member'].rsplit('/', 1)[0] + '/'
            provided = {m.name for m in members if m.name.startswith(prefix) and '/' not in m.name[len(prefix):] and
                        (m.name[len(prefix):].lower().startswith(('license', 'licence', 'notice', 'copying', 'copyright')) or m.name[len(prefix):] == metadata.get('license-file'))}
            require(provided == {n['archive_member'] for n in component['notices']}, 'provided license/notice input omitted or added')
            if component.get('notice_gap'):
                gap = component['notice_gap']
                vcs_raw, readme = read(gap['vcs_info_member']), read(gap['readme_member'])
                vcs = json.loads(vcs_raw)
                require(sha(vcs_raw) == gap['vcs_info_sha256'] and sha(readme) == gap['readme_sha256'], 'notice source gap bytes differ')
                require(vcs['git']['sha1'] == gap['revision'] and vcs['path_in_vcs'] == gap['path_in_vcs'], 'notice source revision differs')
                require(metadata.get('repository') == gap['repository'] and gap['readme_license_link'].encode() in readme, 'notice source link differs')
            for notice in component['notices']:
                data = read(notice['archive_member'])
                require(sha(data) == notice['sha256'] and len(data) == notice['size_bytes'], 'notice contradicts cached archive member')
        count += 1
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archives', action='store_true', help='Also compare every source input with local locked archives/Git')
    parser.add_argument('--cargo-home', type=Path)
    parser.add_argument('--npm-cache', type=Path)
    args = parser.parse_args()
    if args.archives and (args.cargo_home is None or args.npm_cache is None):
        parser.error('--archives requires explicit --cargo-home and --npm-cache; no download/fallback')
    try:
        index = check()
        count = check_archives(index, REPO, args.cargo_home, args.npm_cache) if args.archives else 0
        print(json.dumps({'index_and_assets_match': True, 'components': len(index['components']),
                          'notice_artifacts': sum(len(c['notices']) for c in index['components']),
                          'target': index.get('target'), 'notice_text_coverage': 'incomplete' if any(not c['notices'] for c in index['components']) else 'indexed-direct-inputs-only', 'missing_notice_components': [c['package'] for c in index['components'] if not c['notices']],
                          'source_archives_checked': count, 'tauri_sdk_mapper_executed': False,
                          'standing': 'optional resource preparation only; no built/shipped/qualified candidate'}))
        return 0
    except (ValueError, KeyError, TypeError, StopIteration, OSError, tarfile.TarError, EOFError, subprocess.CalledProcessError) as error:
        print(json.dumps({'index_and_assets_match': False, 'error': str(error)}), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
