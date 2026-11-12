"""Prepare exact unsigned release-build inputs; never build, sign or launch."""
import argparse
import datetime
import importlib.util
import importlib.metadata
import json
import os
from pathlib import Path
import plistlib
import re
import tomllib
import xml.parsers.expat

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
    recipe = parse(files.transfer(output / 'build-recipe.json', retain=True)[0])
    if 'cargo_build_input' in recipe:
        contract = recipe['cargo_build_input']
        require(contract == cargo_build_input_contract(contract.get('preset')), 'invalid Cargo build input contract')
    return marker


CARGO_BUILD_PRESET = 'macos-arm64-rust-1.97.1-no-strip'


def cargo_build_input_contract(preset):
    """Explicit opt-in for the measured toolchain; never a global Cargo default."""
    require(preset == CARGO_BUILD_PRESET, 'unsupported Cargo build input preset')
    text = ('[net]\noffline = true\n[build]\njobs = 2\n\n'
            '[profile.release.build-override]\nstrip = "none"\n\n'
            '[profile.release]\nstrip = "none"\n')
    return {'preset': preset, 'destination': 'CARGO_HOME/config.toml', 'text': text, 'sha256': sha(text.encode()),
            'scope': {'host': 'aarch64-apple-darwin', 'target': 'aarch64-apple-darwin', 'macos': '27.2', 'sdk': '27.2'},
            'tool_sha256': {
                'rustc': '210df6794001b73ec3d453878707fa1e0bdcb63c427024a6e6574bbe5615a4da',
                'cargo': '7672ead309d505577c018fff2cafb3433601f073e38cbe87359ac1f7b944bbf5',
                'clang': 'fc5e3cbba6ad54059295cad716aacb05ace8235f5f7a6031f1d8c15d24bd6d66',
                'ld': '7f7041b1bb30e5e6a815a55edf374065d5c82e1ab93f84d5b6ed5656ded24bcf'},
            'release_opt_level': 3,
            'standing': 'host build dependencies/proc-macros AND shipped release targets are unstripped; '
                        'no bit-identical output claim; require Apple dyld_info -validate_only on actual bundled Mach-Os'}


def verify_cargo_build_input(output, cargo_home, scope, tool_paths):
    """Read-only pre-build check; caller supplies observed scope and resolved tool paths."""
    check_plan(output)
    recipe = parse(files.transfer(Path(output) / 'build-recipe.json', retain=True)[0])
    require('cargo_build_input' in recipe, 'plan has no selected Cargo build input')
    contract = recipe['cargo_build_input']
    require(scope == contract['scope'], 'Cargo build input platform scope mismatch')
    require(set(tool_paths) == set(contract['tool_sha256']), 'exact resolved Cargo tool paths required')
    for name, digest in contract['tool_sha256'].items():
        require(files.transfer(tool_paths[name])[1] == digest, 'Cargo build input toolchain mismatch: ' + name)
    raw, digest, _ = files.transfer(inventory.anchored(cargo_home) / 'config.toml', retain=True)
    require(digest == contract['sha256'] and raw == contract['text'].encode(), 'Cargo build config mismatch')
    return contract['sha256']


SIGNED_DATA_OID = bytes.fromhex('2a864886f70d010702')
DATA_OID = bytes.fromhex('2a864886f70d010701')


def der(raw, offset):
    """One definite-length DER element: (tag, content start, end). Indefinite/long tags refused."""
    require(offset + 2 <= len(raw), 'truncated DER element')
    tag, first = raw[offset], raw[offset + 1]
    require(tag & 0x1f != 0x1f and first != 0x80, 'unsupported DER tag or indefinite length')
    start = offset + 2
    if first & 0x80:
        count = first & 0x7f
        require(1 <= count <= 4 and start + count <= len(raw), 'invalid DER length')
        length = int.from_bytes(raw[start:start + count], 'big'); start += count
        require(length >= 0x80 and raw[offset + 2] != 0, 'non-minimal DER length')
    else:
        length = first
    require(start + length <= len(raw), 'DER element exceeds envelope')
    return tag, start, start + length


def profile_content(raw):
    """Structural CMS SignedData path to its single encapsulated plist; no signature/authentication check."""
    tag, start, end = der(raw, 0)
    require(tag == 0x30 and end == len(raw), 'profile must be exactly one DER ContentInfo')
    tag, oid_start, oid_end = der(raw, start)
    require(tag == 0x06 and raw[oid_start:oid_end] == SIGNED_DATA_OID, 'profile is not CMS SignedData')
    tag, explicit, explicit_end = der(raw, oid_end)
    require(tag == 0xa0 and explicit_end == end, 'invalid SignedData wrapper')
    tag, signed, signed_end = der(raw, explicit)
    require(tag == 0x30 and signed_end == explicit_end, 'invalid SignedData')
    tag, _, cursor = der(raw, signed)
    require(tag == 0x02, 'SignedData version missing')
    tag, _, cursor = der(raw, cursor)
    require(tag == 0x31, 'SignedData digest algorithms missing')
    tag, encap, encap_end = der(raw, cursor)
    require(tag == 0x30, 'encapsulated content missing')
    tag, oid_start, oid_end = der(raw, encap)
    require(tag == 0x06 and raw[oid_start:oid_end] == DATA_OID, 'encapsulated content is not id-data')
    tag, wrapper, wrapper_end = der(raw, oid_end)
    require(tag == 0xa0 and wrapper_end == encap_end, 'encapsulated content wrapper invalid')
    tag, content, content_end = der(raw, wrapper)
    require(tag == 0x04 and content_end == wrapper_end, 'encapsulated content must be one primitive OCTET STRING')
    return raw[content:content_end]


class UniquePlistDict(dict):
    def __setitem__(self, key, value):
        require(key not in self, 'duplicate profile dictionary key')
        super().__setitem__(key, value)


def profile_consistency(raw, expected_sha256, selected, now=None):
    """Consistency only: exact bytes and encapsulated grants match the publisher input. Not CMS authentication."""
    require(isinstance(expected_sha256, str) and re.fullmatch('[0-9a-f]{64}', expected_sha256) is not None
            and sha(raw) == expected_sha256, 'provisioning profile bytes differ from selected digest')
    require(0 < len(raw) <= 1024 * 1024, 'provisioning profile size out of bounds')
    content = profile_content(raw)
    require(content.lstrip().startswith(b'<?xml'), 'encapsulated content is not an XML property list')
    try:
        profile = plistlib.loads(content, fmt=plistlib.FMT_XML, dict_type=UniquePlistDict)
    except (plistlib.InvalidFileException, xml.parsers.expat.ExpatError) as error:
        raise ValueError('encapsulated profile content is not exactly one property list') from error
    require(isinstance(profile, dict), 'profile property list must be a dictionary')
    team, identifier = selected['developer_id_team_identifier'], selected['production_bundle_identifier']
    prefixes = profile.get('ApplicationIdentifierPrefix')
    require(isinstance(prefixes, list) and len(prefixes) == 1 and isinstance(prefixes[0], str), 'one profile AppIdentifierPrefix required')
    entitlements = profile.get('Entitlements')
    require(isinstance(entitlements, dict), 'profile entitlement grants absent')
    require(profile.get('Platform') == ['OSX'] and profile.get('ProvisionsAllDevices') is True
            and not profile.get('ProvisionedDevices'), 'macOS Developer ID distribution profile required')
    require(profile.get('TeamIdentifier') == [team] and entitlements.get('com.apple.developer.team-identifier') == team,
            'profile team differs from publisher input')
    require(entitlements.get('com.apple.application-identifier') == prefixes[0] + '.' + identifier,
            'profile does not grant the selected application identifier')
    require(not entitlements.get('get-task-allow') and not entitlements.get('com.apple.security.get-task-allow'),
            'development profile grant refused')
    creation, expiry = profile.get('CreationDate'), profile.get('ExpirationDate')
    checked = now or datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None, microsecond=0)
    require(isinstance(creation, datetime.datetime) and isinstance(expiry, datetime.datetime) and creation <= checked < expiry,
            'profile not valid at preparation time')
    return {'sha256': expected_sha256, 'size': len(raw), 'uuid': profile.get('UUID'),
            'application_identifier': entitlements['com.apple.application-identifier'],
            'expiration': expiry.isoformat() + 'Z', 'validity_checked_at': checked.isoformat() + 'Z',
            'destination': 'Contents/embedded.provisionprofile',
            'standing': 'structural CMS content and metadata consistency only; signature/Apple authentication is a separate intake; placement unverified until build'}

def prepare(source_root, vendor, expected_manifest, pin, revision, output, *,
            test_identifier=None, publisher_input=None, publisher_sha256=None, upstream_notices=None,
            provisioning_profile=None, provisioning_profile_sha256=None, cargo_build_input=None,
            not_for_public_release=False):
    cargo_contract = cargo_build_input_contract(cargo_build_input) if cargo_build_input is not None else None
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
    profile_ref = None
    if provisioning_profile is not None or provisioning_profile_sha256 is not None:
        require(publisher_ref is not None, 'test mode cannot embed a production provisioning profile')
        profile_path = inventory.anchored(provisioning_profile)
        require(not ancestors(profile_path.parent).intersection({identity(source_root), identity(vendor)}),
                'private provisioning profile must be outside source and vendor')
        profile_raw = read(profile_path)
        profile_ref = profile_consistency(profile_raw, provisioning_profile_sha256, selected)
        profile_ref['path'] = str(profile_path)
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
    # Bundle-visible copy of the frontend IBM Plex notice; refuse a stale index for this source.
    font_notice = load_module('production_font_notice', 'app/packaging/font_notice/check.py')
    fonts = font_notice.check(source_root)
    for src, dst in (('../packaging/font_notice/index.json', 'third-party-notices/fonts/index.json'),
                     *(('../' + l['path'].removeprefix('app/'), 'third-party-notices/fonts/' + Path(l['path']).name) for l in fonts['licenses'])):
        require(src not in resources or resources[src] == dst, 'font notice resource mapping conflict')
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
    inventory.validate_package_layout(metadata, supplier, pin)
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
    if cargo_contract is not None:
        manifest = tomllib.loads(read(source_root / 'app/src-tauri/Cargo.toml').decode())
        require(manifest.get('profile', {}).get('release', {}).get('opt-level', 3) == 3,
                'Cargo build input requires release opt-level 3')
    # One account of every shipped component's notice; a public-release plan refuses while any is open.
    coverage = load_module('production_notice_coverage', 'app/packaging/notices/coverage.py')
    notice_coverage = coverage.check(source_root)
    if notice_coverage['open']:
        require(publisher_ref is None or not_for_public_release,
                'notice coverage is incomplete; a production plan needs --not-for-public-release: '
                + ', '.join(f"{o['name']} {o['version']}" for o in notice_coverage['open']))
    release_standing = ('not for public release: notice coverage is incomplete' if notice_coverage['open']
                        else 'not for public release: package input test' if publisher_ref is None
                        else 'notice coverage complete')
    if not_for_public_release:
        release_standing = 'not for public release (named by the caller)' + ('; notice coverage is incomplete' if notice_coverage['open'] else '')
    tool_paths = [__file__, inventory.__file__, files.__file__, font_notice.__file__, coverage.__file__]
    if supplement is not None: tool_paths.append(receipts.__file__)
    tool_hashes = {str(inventory.anchored(p)): sha(read(Path(p))) for p in tool_paths}
    no_overlap(output.parent, [source_root, vendor, *{Path(p).parent for p in inspected}])
    config = {'productName': product, 'version': '4.0.0', 'identifier': identifier,
              'bundle': {'active': True, 'targets': ['app'], 'resources': resources,
                         'macOS': {'minimumSystemVersion': '15.0', 'signingIdentity': None}}}
    if profile_ref:
        # Tauri copies macOS.files relative to Contents/; placement is verified only by a later build inventory.
        config['bundle']['macOS']['files'] = {'embedded.provisionprofile': profile_ref['path']}
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
                                         'current owner-selected host admission; no shared-script changes', 'jobs2',
                                         'coordinate one fresh candidate; never mutate retained native artifacts'],
              'signing': 'disabled; no signing or build executed', 'profile': 'release', 'mode': mode}
    if cargo_contract is not None:
        recipe['cargo_build_input'] = cargo_contract
    # Ensure all inspected files/trees are still the same before publishing inputs.
    for name, digest in inspected.items():
        require(files.transfer(name)[1] == digest, 'input file changed during preparation')
    require(inventory.compare(inventory.scan(vendor), supplier)['equal'], 'vendor changed during preparation')
    for info in resource_inputs.values():
        if 'tree' in info:
            require(inventory.compare(inventory.scan(info['tree']['root']), info['tree'])['equal'], 'resource tree changed during preparation')
    if supplement is not None:
        require(receipts.check_stage(upstream_notices, source_root) == supplement, 'supplement changed during preparation')
    require(font_notice.check(source_root) == fonts, 'font notice changed during preparation')
    require(coverage.check(source_root) == notice_coverage, 'notice coverage changed during preparation')
    output.mkdir(exist_ok=False, mode=0o700)
    write_new(output / 'INCOMPLETE.txt', b'Not usable until PLAN_COMPLETE.json validates and this marker is absent.\n')
    try:
        account = {'tool_sha256': tool_hashes, 'jsonschema_version': importlib.metadata.version('jsonschema'),
                   'source_revision': revision, 'source_root': str(source_root), 'source_claim': 'caller-selected disposable export; hashes below, not Git export authentication',
                   'mode': mode, 'resource_inputs': resource_inputs, 'supplier': supplier, 'inspected_files': inspected,
                   'publisher_input': publisher_ref, 'limits': ['input preparation only; no App build or resource mapper executed',
                   'stock cache selection does not qualify supplier pin', 'no signed package, S4 installed observation, OS qualification or release',
                   'notice coverage is as notice_coverage states; open components are named there'],
                   'release_standing': release_standing,
                   'notice_coverage': {'account': 'app/packaging/notices/coverage.json', 'sha256': notice_coverage['sha256'],
                                       'counts': notice_coverage['counts'],
                                       'open': [f"{o['name']} {o['version']} ({o['standing']})" for o in notice_coverage['open']]}}
        if supplement is not None: account['upstream_notice_supplement'] = supplement
        if profile_ref: account['provisioning_profile'] = profile_ref
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
            'build_executed': False, 'signing_executed': False, 'package_complete': False, 'release_standing': release_standing}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ('source-root', 'vendor', 'expected-manifest', 'pin', 'revision', 'output'):
        parser.add_argument('--' + key, required=True)
    parser.add_argument('--test-identifier')
    parser.add_argument('--publisher-input')
    parser.add_argument('--publisher-sha256')
    parser.add_argument('--upstream-notices', help='Explicit completed upstream notice supplement; default omitted')
    parser.add_argument('--provisioning-profile', help='Private Developer ID profile embedded at Contents/; production only')
    parser.add_argument('--provisioning-profile-sha256')
    parser.add_argument('--not-for-public-release', action='store_true',
                        help='Name the plan as not for public release; required for a production plan while notice coverage is open')
    parser.add_argument('--cargo-build-input', choices=[CARGO_BUILD_PRESET],
                        help='Explicit platform/toolchain-scoped host and shipped release strip override; default omitted')
    args = vars(parser.parse_args())
    try:
        print(json.dumps(prepare(**args), indent=2))
    except Exception as error:
        # Source/identity values belong to private output evidence, not diagnostics.
        print(json.dumps({'preparation_complete': False, 'error_type': type(error).__name__}))
        raise SystemExit(2)
