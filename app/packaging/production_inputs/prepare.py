"""Prepare exact unsigned release-build inputs; never build, sign or launch."""
import argparse
import importlib.util
import importlib.metadata
import json
import os
from pathlib import Path
import re

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[3]

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    value = importlib.util.module_from_spec(spec); spec.loader.exec_module(value)
    return value

inventory = load_module('production_input_inventory', 'app/packaging/inventory.py')
files = load_module('production_input_files', 'app/packaging/static_distribution/check.py')
sha, parse, require = files.sha, files.parse, files.require


def identity(path):
    value = os.stat(path, follow_symlinks=False)
    return value.st_dev, value.st_ino


def ancestors(path):
    return {identity(p) for p in (path, *path.parents)}


def no_overlap(parent, protected):
    """Case aliases and macOS firmlinks must not hide an input ancestor."""
    require(parent.is_dir(), 'existing physical output parent required')
    require(not ancestors(parent).intersection(identity(p) for p in protected),
            'output and selected input overlap by filesystem identity')


def require_nonempty(tree):
    for directory in [''] + [e['path'] for e in tree['entries'] if e['kind'] == 'dir']:
        prefix = directory + '/' if directory else ''
        require(any(e['kind'] == 'file' and e['path'].startswith(prefix) for e in tree['entries']),
                'empty resource directory would be omitted by the bundler')


def write_new(path, raw):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'wb') as output:
        output.write(raw)
        output.flush()
        os.fsync(output.fileno())


def check_plan(output):
    output = inventory.anchored(output)
    require(not os.path.lexists(output / 'INCOMPLETE.txt'), 'plan is incomplete')
    marker = parse(files.transfer(output / 'PLAN_COMPLETE.json', retain=True)[0])
    require(set(marker) == {'files'} and set(marker['files']) ==
            {'tauri.package-inputs.conf.json', 'build-recipe.json', 'input-inventory.json'}, 'invalid completion marker')
    for name, digest in marker['files'].items():
        require(files.transfer(output / name)[1] == digest, 'completed plan file changed')
    return marker


def prepare(source_root, vendor, expected_manifest, pin, revision, output, *,
            test_identifier=None, publisher_input=None, publisher_sha256=None, upstream_notices=None):
    source_root, vendor, output = map(inventory.anchored, (source_root, vendor, output))
    require(not os.path.lexists(source_root / '.git'), 'source must be a disposable frozen export, not a checkout')
    require('*' not in str(vendor), 'glob characters in vendor source refused')
    require(identity(source_root) not in ancestors(vendor) and identity(vendor) not in ancestors(source_root),
            'vendor and source export must be disjoint')
    require(output.parent.is_dir(), 'existing physical output parent required')
    require(re.fullmatch('[0-9a-f]{40}', revision) is not None, 'exact source revision required')
    require(re.fullmatch('[0-9a-f]{64}', expected_manifest) is not None, 'expected vendor manifest required')
    require(bool(test_identifier) != bool(publisher_input), 'select exactly one explicit test namespace or private publisher input')
    inspected = {}
    def read(path):
        path = inventory.anchored(path)
        raw, digest, _ = files.transfer(path, retain=True)
        inspected[str(path)] = digest
        return raw
    publisher_ref = None
    if test_identifier:
        require(publisher_sha256 is None, 'test mode cannot select publisher trust')
        require(re.fullmatch(r'dev\.chirality\.app-v4\.package-test\.[A-Za-z0-9-]+', test_identifier) is not None,
                'explicit isolated package-test identifier required')
        identifier = test_identifier
        mode = 'unqualified-input-test'
        product = 'Chirality App v4 (package input test ' + test_identifier.rsplit('.', 1)[1] + ')'
    else:
        require(isinstance(publisher_sha256, str) and re.fullmatch('[0-9a-f]{64}', publisher_sha256), 'exact selected publisher input digest required')
        publisher_path = inventory.anchored(publisher_input)
        require(not ancestors(publisher_path.parent).intersection({identity(source_root), identity(vendor)}),
                'private publisher input must be outside source and vendor')
        raw = read(publisher_path)
        require(sha(raw) == publisher_sha256, 'publisher input bytes differ from selected digest')
        selected = parse(raw)
        schema = parse(read(source_root / 'app/src-tauri/schemas/publisher-build-selection.s1.schema.json'))
        Draft202012Validator(schema).validate(selected)
        identifier = selected['production_bundle_identifier']
        require(not identifier.startswith('dev.chirality.app-v4.package-test.'), 'test namespace cannot select production inputs')
        mode, product = 'selected-production-inputs', 'Chirality App v4'
        publisher_ref = {'path': str(inventory.anchored(publisher_input)), 'sha256': publisher_sha256}
    app = source_root / 'app'
    resources = {}
    for name in ('tauri.attested-reference.conf.json', 'tauri.notices.conf.json'):
        overlay = parse(read(app / 'packaging/unsigned' / name))
        for src, dst in overlay['bundle']['resources'].items():
            require(src not in resources or resources[src] == dst, 'resource mapping conflict')
            resources[src] = dst
    for name in ('index.json', 'libsqlite3-sys.LICENSE', 'sqlite3-source-header.txt', 'README.md'):
        src, dst = '../packaging/sqlite_notice/' + name, 'third-party-notices/sqlite-preparation/' + name
        require(src not in resources or resources[src] == dst, 'SQLite resource mapping conflict')
        resources[src] = dst
    supplement_sources = set()
    supplement = None
    if upstream_notices is not None:
        receipts = load_module('production_notice_receipts', 'app/packaging/notices/receipts.py')
        upstream_notices = inventory.anchored(upstream_notices)
        supplement = receipts.check_stage(upstream_notices, source_root)
        for name in supplement['files']:
            src = str(upstream_notices / name)
            require('*' not in src and src not in resources, 'supplement source conflict')
            resources[src] = 'third-party-notices/upstream/' + name
            supplement_sources.add(src)
    resource_inputs = {}
    for src, dst in resources.items():
        require('*' not in src and '*' not in dst, 'glob resource mapping refused')
        require(not Path(src).is_absolute() or src in supplement_sources, 'source resource mapping must be repository-relative')
        files.relative(dst.rstrip('/'))
        path = inventory.anchored(os.path.abspath(app / 'src-tauri' / src))
        require(path.is_relative_to(source_root) or src in supplement_sources, 'source resource mapping escapes selected source')
        if path.is_dir():
            tree = inventory.scan(path)
            require(all(e['kind'] in ('file', 'dir') for e in tree['entries']), 'resource tree contains link/special input')
            require_nonempty(tree)
            resource_inputs[src] = {'destination': dst, 'tree': tree}
        else:
            raw = read(path)
            resource_inputs[src] = {'destination': dst, 'sha256': sha(raw), 'size': len(raw)}
    destinations = [(info['destination'].rstrip('/'), 'tree' in info) for info in resource_inputs.values()]
    require(len({p for p, _ in destinations}) == len(destinations), 'duplicate resource destination')
    for parent, directory in destinations:
        if directory:
            require(not any(p != parent and p.startswith(parent + '/') for p, _ in destinations), 'overlapping resource destinations')
    supplier = inventory.scan(vendor)
    require(supplier['manifest_sha256'] == expected_manifest and supplier['files'] > 0, 'vendor manifest mismatch')
    require(all(e['kind'] in ('file', 'dir') for e in supplier['entries']), 'vendor links/special files refused')
    require_nonempty(supplier)
    metadata = parse(read(vendor / 'codex-package.json'))
    require(type(metadata.get('layoutVersion')) is int, 'vendor layoutVersion must be an integer')
    require(metadata == {'layoutVersion': 1, 'version': pin, 'target': 'aarch64-apple-darwin', 'variant': 'codex',
                         'entrypoint': 'bin/codex', 'resourcesDir': 'codex-resources', 'pathDir': 'codex-path'}, 'vendor metadata mismatch')
    entries = {e['path']: e for e in supplier['entries']}
    require(entries.get('bin/codex', {}).get('macho') and int(entries['bin/codex']['mode'], 8) & 0o111, 'vendor entrypoint invalid')
    require(all(entries.get(n, {}).get('kind') == 'dir' for n in ('codex-path', 'codex-resources')), 'vendor layout incomplete')
    require('codex' not in {p for p, _ in destinations}
            and not any(p.startswith('codex/') for p, _ in destinations), 'vendor destination collision')
    by_destination = {info['destination']: src for src, info in resource_inputs.items() if 'tree' not in info}
    def reference_file(reference):
        files.ref(reference)
        destination = 'distribution-reference/' + reference['path']
        require(destination in by_destination, 'supplier reference is not explicitly mapped')
        raw = read(app / 'src-tauri' / by_destination[destination])
        require(sha(raw) == reference['sha256'], 'mapped supplier reference digest mismatch')
        return parse(raw)
    selection_key = by_destination['distribution-reference/build-selection.s2.json']
    selection = parse(read(app / 'src-tauri' / selection_key))
    require(selection['format'] == 'build-selection.s2', 'unknown supplier selection')
    expected = reference_file(selection['expected'])
    attestation = reference_file(selection['attestation'])
    require(attestation['expected_reference'] == selection['expected'], 'supplier attestation subject mismatch')
    require(expected['pin'] == pin and expected['inventory']['manifest_sha256'] == expected_manifest,
            'selected vendor does not match mapped supplier reference')
    observed_entries = [{'path': '.', 'kind': 'dir', 'mode': int(supplier['root_mode'], 8)}]
    for entry in supplier['entries']:
        item = {'path': entry['path'], 'kind': entry['kind'], 'mode': int(entry['mode'], 8)}
        if entry['kind'] == 'file': item.update(size=entry['size'], sha256=entry['sha256'])
        observed_entries.append(item)
    require(sorted(observed_entries, key=lambda e: e['path']) == sorted(expected['inventory']['entries'], key=lambda e: e['path']),
            'vendor full tree differs from mapped supplier reference')
    resources[str(vendor) + '/'] = 'codex/'
    # Read relevant recipe inputs without selecting a new supplier pin or changing source.
    for relative in ('app/package-lock.json', 'app/src-tauri/Cargo.lock', 'app/src-tauri/Cargo.toml', 'app/src-tauri/tauri.conf.json'):
        read(source_root / relative)
    tool_paths = [__file__, inventory.__file__, files.__file__]
    if supplement is not None: tool_paths.append(receipts.__file__)
    tool_hashes = {str(inventory.anchored(p)): sha(read(Path(p))) for p in tool_paths}
    no_overlap(output.parent, [source_root, vendor, *{Path(p).parent for p in inspected}])
    config = {'productName': product, 'version': '4.0.0', 'identifier': identifier,
              'bundle': {'active': True, 'targets': ['app'], 'resources': resources,
                         'macOS': {'minimumSystemVersion': '15.0', 'signingIdentity': None}}}
    env = {'CARGO_NET_OFFLINE': 'true', 'NPM_CONFIG_OFFLINE': 'true', 'CARGO_BUILD_JOBS': '2', 'MACOSX_DEPLOYMENT_TARGET': '15.0'}
    if publisher_ref:
        env.update(CHIRALITY_PUBLISHER_SELECTION='production-v1', CHIRALITY_PUBLISHER_INPUT_FILE=publisher_ref['path'],
                   CHIRALITY_PUBLISHER_INPUT_SHA256=publisher_ref['sha256'])
    required_env = {'PATH': 'prepared toolchain PATH', 'HOME': 'explicit build HOME, not a Codex home',
                    'LANG': 'explicit locale', 'TMPDIR': 'private build temporary directory',
                    'CARGO_HOME': 'prepared offline cache view', 'CARGO_TARGET_DIR': 'new isolated absolute target outside inputs',
                    'CODEX_HOME': 'fresh private scratch Codex home', 'NPM_CONFIG_CACHE': 'prepared offline npm cache',
                    'NPM_CONFIG_USERCONFIG': 'empty task-owned config', 'NPM_CONFIG_GLOBALCONFIG': 'empty task-owned config'}
    recipe = {'working_directory': str(app), 'inherit_environment': False,
              'environment_allowlist': sorted(set(env) | set(required_env)), 'required_environment': required_env, 'environment': env,
              'unset_environment': ['APPLE_SIGNING_IDENTITY', 'APPLE_CERTIFICATE', 'APPLE_CERTIFICATE_PASSWORD', 'APPLE_ID',
                                    'APPLE_PASSWORD', 'APPLE_TEAM_ID', 'APPLE_API_KEY', 'APPLE_API_ISSUER', 'APPLE_API_KEY_PATH',
                                    'TAURI_CONFIG', 'TAURI_SIGNING_PRIVATE_KEY', 'TAURI_SIGNING_PRIVATE_KEY_PASSWORD', 'RUSTFLAGS', 'CARGO_ENCODED_RUSTFLAGS']
                                    + ([] if publisher_ref else ['CHIRALITY_PUBLISHER_SELECTION', 'CHIRALITY_PUBLISHER_INPUT_FILE', 'CHIRALITY_PUBLISHER_INPUT_SHA256']),
              'argv': ['node', 'node_modules/@tauri-apps/cli/tauri.js', 'build', '--no-sign', '--bundles', 'app',
                       '--features', 'custom-protocol,distribution-successor', '--config', str(output / 'tauri.package-inputs.conf.json'), '--', '--offline', '--locked'],
              'required_host_controls': ['prepared offline caches and isolated target', 'fresh scratch CODEX_HOME',
                                         'shared t3_slot.sh/t3_cargo.sh and running memguard admission', 'jobs2',
                                         'coordinate one fresh candidate; never mutate retained native artifacts'],
              'signing': 'disabled; no signing or build executed', 'profile': 'release', 'mode': mode}
    # Ensure all inspected files/trees are still the same before publishing inputs.
    for name, digest in inspected.items():
        require(files.transfer(name)[1] == digest, 'input file changed during preparation')
    require(inventory.compare(inventory.scan(vendor), supplier)['equal'], 'vendor changed during preparation')
    for info in resource_inputs.values():
        if 'tree' in info:
            require(inventory.compare(inventory.scan(info['tree']['root']), info['tree'])['equal'], 'resource tree changed during preparation')
    if supplement is not None:
        require(receipts.check_stage(upstream_notices, source_root) == supplement, 'supplement changed during preparation')
    output.mkdir(exist_ok=False, mode=0o700)
    write_new(output / 'INCOMPLETE.txt', b'Not usable until PLAN_COMPLETE.json validates and this marker is absent.\n')
    try:
        account = {'tool_sha256': tool_hashes, 'jsonschema_version': importlib.metadata.version('jsonschema'),
                   'source_revision': revision, 'source_root': str(source_root), 'source_claim': 'caller-selected disposable export; hashes below, not Git export authentication',
                   'mode': mode, 'resource_inputs': resource_inputs, 'supplier': supplier, 'inspected_files': inspected,
                   'publisher_input': publisher_ref, 'upstream_notice_supplement': supplement, 'limits': ['input preparation only; no App build or resource mapper executed',
                   'stock cache selection does not qualify supplier pin', 'no signed package, S4 installed observation, OS qualification or release',
                   'four supplier notice/source associations and transitive completeness remain unresolved']}
        completed = {}
        for name, value in [('tauri.package-inputs.conf.json', config), ('build-recipe.json', recipe), ('input-inventory.json', account)]:
            raw = (json.dumps(value, indent=2) + '\n').encode()
            write_new(output / name, raw)
            completed[name] = sha(raw)
        write_new(output / 'PLAN_COMPLETE.json', (json.dumps({'files': completed}, indent=2) + '\n').encode())
        fd = os.open(output, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            os.fsync(fd)
            (output / 'INCOMPLETE.txt').unlink()
            os.fsync(fd)
        finally:
            os.close(fd)
    except Exception:
        # The initial marker remains even if killed between writes; no incomplete
        # output is made runnable by the presence of only config and recipe.
        raise
    # Do not print production identifier/team or private input bytes.
    return {'mode': mode, 'output': str(output), 'files': check_plan(output)['files'],
            'build_executed': False, 'signing_executed': False, 'package_complete': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ('source-root', 'vendor', 'expected-manifest', 'pin', 'revision', 'output'):
        parser.add_argument('--' + key, required=True)
    parser.add_argument('--test-identifier')
    parser.add_argument('--publisher-input')
    parser.add_argument('--publisher-sha256')
    parser.add_argument('--upstream-notices', help='Explicit completed upstream notice supplement; default omitted')
    args = vars(parser.parse_args())
    try:
        print(json.dumps(prepare(**args), indent=2))
    except Exception as error:
        # Source/identity values belong to private output evidence, not diagnostics.
        print(json.dumps({'preparation_complete': False, 'error_type': type(error).__name__}))
        raise SystemExit(2)
