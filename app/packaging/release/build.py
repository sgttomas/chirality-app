"""Build the unsigned 4.0.0 release candidate and describe it; signs nothing.

Agents run this. It prepares the plan with production_inputs/prepare.py,
checks it, checks the Cargo build input, installs the npm dependencies
offline, runs the plan's recipe argv from an empty environment holding only
the allowlisted variables, checks the built bundle, and publishes
CANDIDATE.json, which owner_sign.py verifies before it does anything.

The inputs it would write through (the source export, the Cargo home and the
npm cache) are copied into its output folder; every writable location of the
install and the build points inside that folder. Raw tool output and traces go
only to the private folder (common.PrivateWriter, never read back). Files it
returns (CANDIDATE.json, BUILD_REFUSED.json, BUILD_FAILED.json) hold only
values it constructs or selects and validates. A failure carries a fixed
reason from common.REASONS. CANDIDATE.json appears only as the last act, by an
atomic rename after the final check; any failure before that leaves
INCOMPLETE.txt and BUILD_FAILED.json.

No signing, notarization or keychain tool is run, and no credential, signing
identity or provisioning profile is an input.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import platform
import re
import shutil
import sys
import traceback


def sibling(name):
    """Load a module of this directory once per process, by file path."""
    key = 'chirality_release_' + name
    if key not in sys.modules:
        spec = importlib.util.spec_from_file_location(key, Path(__file__).resolve().parent / (name + '.py'))
        module = importlib.util.module_from_spec(spec); sys.modules[key] = module; spec.loader.exec_module(module)
    return sys.modules[key]


common = sibling('common')
prepare, inventory, require, sha = common.prepare, common.inventory, common.require, common.sha
Failure, check = common.Failure, common.check

KEYCHAIN_SOURCE = 'app/src-tauri/src/capture_seal_keychain.rs'
CALLER_ENVIRONMENT = ('PATH', 'LANG')
TOOLS = ('rustc', 'cargo', 'clang', 'ld')
WRITABLE_ENVIRONMENT = ('HOME', 'TMPDIR', 'CARGO_HOME', 'CARGO_TARGET_DIR', 'CODEX_HOME', 'NPM_CONFIG_CACHE', 'NPM_CONFIG_USERCONFIG',
                        'NPM_CONFIG_GLOBALCONFIG', 'RUSTUP_HOME', 'NPM_CONFIG_PREFIX', 'NPM_CONFIG_LOGS_DIR')
INSTALL_ARGV = ['npm', 'ci', '--offline', '--ignore-scripts', '--no-audit', '--no-fund']
CARGO_CACHE_REFUSED = ('config', 'config.toml', 'credentials', 'credentials.toml', 'env')
CHECKS = ['info_plist_identifier', 'info_plist_version', 'info_plist_bundle_version', 'info_plist_minimum_system_version',
          'info_plist_executable', 'dyld_validate', 'executable_signature', 'already_signed', 'vendor_tree', 'resource',
          'publisher_binding', 'limitations']
common.VOCABULARY.update(CHECKS)


def publisher_values(source_root):
    """The bundle identifier and team published in the compiled keychain selection of the source being built."""
    text = (Path(source_root) / KEYCHAIN_SOURCE).read_text()
    blocks = re.findall(r'const KEYCHAIN_SELECTION: Option<Selection> = Some\(Selection \{(.*?)\}\);', text, re.S)
    require(len(blocks) == 1, 'exactly one compiled keychain selection required in ' + KEYCHAIN_SOURCE)
    def field(name):
        found = re.findall(r'^\s*' + name + r':\s*"([^"]*)",\s*$', blocks[0], re.M)
        require(len(found) == 1, 'keychain selection field missing or repeated: ' + name)
        return found[0]
    identifier, team = field('bundle_identifier'), field('team_identifier')
    require(identifier == common.RELEASE['identifier'], 'compiled keychain selection is not the release identifier')
    require(re.fullmatch('[A-Z0-9]{10}', team) is not None, 'compiled keychain selection team is malformed')
    return identifier, team


def write_private_input(path, raw):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'wb') as handle:
        handle.write(raw)


def generate_publisher_input(source_root, directory):
    """Write the two-field publisher-build-selection.s1 file from the source; returns (path, digest)."""
    identifier, team = publisher_values(source_root)
    raw = (json.dumps({'format': 'publisher-build-selection.s1', 'production_bundle_identifier': identifier,
                       'developer_id_team_identifier': team}, indent=2, sort_keys=True) + '\n').encode()
    directory.mkdir(mode=0o700)
    path = directory / 'publisher-build-selection.json'
    write_private_input(path, raw)
    return path, sha(raw)


def isolated_environment(out):
    """Every location the install and the build may write: all inside the run's own folder."""
    return {'HOME': str(out / 'home'), 'TMPDIR': str(out / 'tmp'), 'CARGO_HOME': str(out / 'cargo-home'),
            'CARGO_TARGET_DIR': str(out / 'target'), 'CODEX_HOME': str(out / 'codex-home'),
            'NPM_CONFIG_CACHE': str(out / 'npm-cache'), 'NPM_CONFIG_USERCONFIG': str(out / 'npm-config/userconfig'),
            'NPM_CONFIG_GLOBALCONFIG': str(out / 'npm-config/globalconfig'), 'RUSTUP_HOME': str(out / 'rustup-home'),
            'NPM_CONFIG_PREFIX': str(out / 'npm-prefix'), 'NPM_CONFIG_LOGS_DIR': str(out / 'npm-logs')}


def placeholder(value, out):
    """A path inside the output folder as <out>/...; the description never names a path outside it."""
    if isinstance(value, str) and value.startswith('/'):
        path = Path(value)
        require(path == out or path.is_relative_to(out), 'a path outside the output folder would be described')
        return '<out>' + ('/' + str(path.relative_to(out)) if path != out else '')
    return value


def refuse_links(tree, root, allow_inside):
    """Refuse links in a copied input: any link in the caches, and any link in the export that leaves it."""
    for entry in tree['entries']:
        if entry['kind'] == 'symlink':
            check(allow_inside, 'BUILD_LINK')
            target = Path(os.path.realpath(Path(root) / entry['path']))
            check(target == Path(os.path.realpath(root)) or target.is_relative_to(Path(os.path.realpath(root))), 'BUILD_LINK')


def observe_scope(runner, env, private):
    def one(argv, shape):
        result = runner(argv, env=env)
        private.write('scope ' + Path(argv[0]).name, result.stdout + result.stderr)
        value = result.stdout.decode('utf-8', 'replace').strip()
        check(result.returncode == 0 and common.is_shape(value, shape), 'BUILD_SCOPE')
        return value
    check(one(['/usr/bin/uname', '-m'], 'identifier') == 'arm64', 'BUILD_SCOPE')
    triple = 'aarch64-apple-darwin'
    return {'host': triple, 'target': triple, 'macos': one(['/usr/bin/sw_vers', '-productVersion'], 'version'),
            'sdk': one(['/usr/bin/xcrun', '--sdk', 'macosx', '--show-sdk-version'], 'version')}


def bundle_errors(app, plan, vendor, source_root, runner, env, private):
    """Every post-build check; returns (facts, errors). Errors are named checks with an optional relative path."""
    errors, facts = [], {}
    def error(name, path=None):
        errors.append({'check': name, 'path': path})
    info_raw, info = common.read_info_plist(app)
    for name in common.release_identity_errors(info):
        error(name)
    facts['info_plist_sha256'] = sha(info_raw)
    identity = common.bundle_identity(info)
    facts['identity'] = {k: common.selected(v, 'version' if 'version' in k else 'identifier') for k, v in identity.items()}
    executable = (app / 'Contents/MacOS' / common.MAIN_EXECUTABLE).read_bytes()
    facts['executable_sha256'] = sha(executable)
    tree = inventory.scan(app)
    facts['inventory'] = common.tree_entries(tree)
    # Apple's static validator on the main executable and on every bundled Mach-O, through the one observation rule.
    validated = []
    for relative in sorted(set(['Contents/MacOS/' + common.MAIN_EXECUTABLE] + common.macho_paths(tree))):
        result = runner(['/usr/bin/dyld_info', '-validate_only', str(app / relative)], env=env)
        private.write('dyld_info ' + relative, result.stdout + result.stderr)
        try:
            common.observe('dyld_validate', result, subjects=[app / relative])
            validated.append({'path': relative, 'valid': True})
        except common.ObservationFailed:
            validated.append({'path': relative, 'valid': False})
            error('dyld_validate', relative)
    facts['dyld_validate'] = validated
    # The App's own code carries only the linker's ad hoc signature.
    try:
        adhoc, slices = common.only_linker_adhoc(executable)
    except ValueError:
        adhoc, slices = False, 'not observed'
    facts['executable_signature'] = slices
    if not adhoc:
        error('executable_signature')
    for relative in ('Contents/_CodeSignature', 'Contents/CodeResources', 'Contents/embedded.provisionprofile'):
        if os.path.lexists(app / relative):
            error('already_signed', relative)
    # Vendor tree: bytes, modes and types equal to the vendor input.
    packaged = inventory.scan(app / common.VENDOR_DESTINATION)
    equal = inventory.compare(packaged, inventory.scan(vendor))['equal']
    facts['vendor'] = {'equal': equal, 'inventory': common.tree_entries(packaged)}
    if not equal:
        error('vendor_tree')
    # Every mapped resource equals its source, byte for byte and by type.
    account = prepare.parse((plan / 'input-inventory.json').read_bytes())
    resources = []
    for source, item in sorted(account['resource_inputs'].items()):
        destination = app / 'Contents/Resources' / item['destination'].rstrip('/')
        if 'tree' in item:
            original = inventory.scan(item['tree']['root'])
            if not os.path.isdir(destination):
                error('resource', item['destination']); continue
            placed = inventory.scan(destination)
            def content(t): return {e['path']: (e['kind'], e.get('sha256')) for e in t['entries']}
            same = content(placed) == content(original)
            resources.append({'destination': item['destination'], 'manifest_sha256': placed['manifest_sha256'], 'equal': same,
                              'modes_equal': inventory.compare(placed, original)['equal']})
        else:
            path = Path(source) if Path(source).is_absolute() else Path(os.path.abspath(source_root / 'app/src-tauri' / source))
            same = destination.is_file() and not destination.is_symlink() and sha(destination.read_bytes()) == sha(path.read_bytes())
            resources.append({'destination': item['destination'], 'sha256': item['sha256'], 'equal': same})
        if not same:
            error('resource', item['destination'])
    facts['resources'] = resources
    return facts, errors


def find_publisher_outputs(target):
    found = {}
    for binding in sorted(Path(target).glob('release/build/chirality-app-v4-*/out/publisher-build-binding.s1.json')):
        raw = binding.read_bytes()
        if raw.strip() != b'null':
            found.setdefault(raw, binding.parent)
    return next(iter(found.values())) if len(found) == 1 else None


def build(*, out, **kw):
    """Build and publish a candidate. Any failure leaves INCOMPLETE.txt and BUILD_FAILED.json and no CANDIDATE.json."""
    out = Path(os.path.abspath(out))
    existed = os.path.lexists(out)
    try:
        return _build(out=out, **kw)
    except BaseException as error:
        if isinstance(error, SystemExit):
            raise
        failure = error if isinstance(error, Failure) else Failure('BUILD_INTERRUPTED' if isinstance(error, KeyboardInterrupt) else 'BUILD_UNEXPECTED')
        if not existed and out.is_dir() and not os.path.lexists(out / common.CANDIDATE_FILE):
            try:
                if not isinstance(error, Failure):
                    common.PrivateWriter(out).write('trace', ''.join(traceback.format_exception(error)))
                if not os.path.lexists(out / 'INCOMPLETE.txt'):
                    write_private_input(out / 'INCOMPLETE.txt', b'No candidate: the build failed; see BUILD_FAILED.json.\n')
                if not os.path.lexists(out / 'BUILD_FAILED.json'):
                    common.write_returnable(out / 'BUILD_FAILED.json', {'result': 'failed', 'reason_code': failure.code,
                                                                        'reason': failure.reason}, out, set())
            except BaseException:
                pass
        raise failure from None


def _build(*, source_root, revision, vendor, expected_manifest, pin, out, environment, tools, cargo_cache, npm_cache,
           publisher_input=None, publisher_sha256=None, cargo_build_input=prepare.CARGO_BUILD_PRESET,
           runner=common.system_runner, host=None):
    host = host or (platform.system(), platform.machine())
    check(host == ('Darwin', 'arm64'), 'BUILD_HOST')
    try:
        export, vendor, cargo_cache, npm_cache = map(inventory.anchored, (source_root, vendor, cargo_cache, npm_cache))
        common.refuse_installed_location(out, 'output')
    except ValueError:
        raise Failure('BUILD_OUT')
    check(not os.path.lexists(out) and out.parent.is_dir(), 'BUILD_OUT')
    check(set(environment) == set(CALLER_ENVIRONMENT)
          and all(isinstance(v, str) and v and '\n' not in v for v in environment.values())
          and all(Path(p).is_absolute() for p in environment['PATH'].split(':')), 'BUILD_ENVIRONMENT')
    check(set(tools) == set(TOOLS), 'BUILD_TOOLS')
    for name in ('rustc', 'cargo'):
        resolved = shutil.which(name, path=environment['PATH'])
        check(resolved is not None and os.path.samefile(resolved, tools[name]), 'BUILD_TOOLS')
        proxy = Path(resolved).parent / 'rustup'
        check(not (proxy.exists() and os.path.samefile(proxy, resolved)) and Path(os.path.realpath(resolved)).name != 'rustup', 'BUILD_TOOLS')
    check((publisher_input is None) == (publisher_sha256 is None), 'BUILD_PUBLISHER_PAIR')
    check(not os.path.lexists(export / 'app/node_modules'), 'BUILD_NODE_MODULES')
    check(not any(os.path.lexists(cargo_cache / n) for n in CARGO_CACHE_REFUSED), 'BUILD_CARGO_CACHE')
    # Inputs the build would write through are copied in: no link may lead out of them.
    refuse_links(inventory.scan(cargo_cache), cargo_cache, allow_inside=False)
    refuse_links(inventory.scan(npm_cache), npm_cache, allow_inside=False)
    refuse_links(inventory.scan(export), export, allow_inside=True)
    out.mkdir(mode=0o700)
    write_private_input(out / 'INCOMPLETE.txt', b'No candidate until CANDIDATE.json is published and this marker is removed.\n')
    private = common.PrivateWriter(out)
    source_root = out / 'source'
    shutil.copytree(export, source_root, symlinks=True, copy_function=shutil.copy2)
    shutil.copytree(cargo_cache, out / 'cargo-home', symlinks=True, copy_function=shutil.copy2)
    shutil.copytree(npm_cache, out / 'npm-cache', symlinks=True, copy_function=shutil.copy2)
    for name in ('home', 'tmp', 'codex-home', 'npm-config', 'rustup-home', 'npm-prefix', 'npm-logs'):
        (out / name).mkdir(mode=0o700)
    for name in ('userconfig', 'globalconfig'):
        write_private_input(out / 'npm-config' / name, b'')
    limitations_source = source_root / common.LIMITATIONS_SOURCE
    check(limitations_source.is_file() and not limitations_source.is_symlink(), 'BUILD_LIMITATIONS')
    try:
        if publisher_input is None:
            publisher_input, publisher_sha256 = generate_publisher_input(source_root, out / 'publisher-input')
            publisher_origin = 'publisher-build-selection.s1 generated from the source keychain selection'
        else:
            publisher_origin = 'supplied publisher input file'
    except ValueError:
        raise Failure('BUILD_PUBLISHER_SOURCE')
    plan = out / 'plan'
    try:
        prepare.prepare(source_root, vendor, expected_manifest, pin, revision, plan, publisher_input=publisher_input,
                        publisher_sha256=publisher_sha256, cargo_build_input=cargo_build_input)
        completion = prepare.check_plan(plan)
        team = parse_team(publisher_input)
    except (ValueError, OSError, KeyError):
        raise Failure('BUILD_PLAN')
    public_teams = {team, common.SUPPLIER_TEAM}
    config = prepare.parse((plan / 'tauri.package-inputs.conf.json').read_bytes())
    check(config['productName'] == common.PRODUCT_NAME and config['identifier'] == common.RELEASE['identifier']
          and config['version'] == common.RELEASE['version']
          and config['bundle']['macOS']['minimumSystemVersion'] == common.RELEASE['minimum_system_version']
          and config['bundle']['macOS']['signingIdentity'] is None, 'BUILD_OVERLAY')
    recipe = prepare.parse((plan / 'build-recipe.json').read_bytes())
    env = dict(recipe['environment']) | environment | isolated_environment(out)
    check(recipe['inherit_environment'] is False and '--no-sign' in recipe['argv'] and set(env) == set(recipe['environment_allowlist'])
          and not set(env) & set(recipe['unset_environment']) and Path(recipe['working_directory']) == source_root / 'app', 'BUILD_RECIPE')
    try:
        for name in WRITABLE_ENVIRONMENT:
            common.require_inside(Path(env[name]) / 'probe', out, name)
    except ValueError:
        raise Failure('BUILD_CONTAINED')
    cargo_home = inventory.anchored(env['CARGO_HOME'])
    contract = recipe['cargo_build_input']
    # The run's own Cargo home gets exactly the contract's configuration (the cache input may hold none).
    write_private_input(cargo_home / 'config.toml', contract['text'].encode())
    scope = observe_scope(runner, env, private)
    try:
        cargo_config_sha256 = prepare.verify_cargo_build_input(plan, cargo_home, scope, tools)
    except (ValueError, OSError):
        raise Failure('BUILD_CARGO_INPUT')
    installed = runner(INSTALL_ARGV, env=env, cwd=recipe['working_directory'])
    private.write('install', installed.stdout + b'\n--- stderr\n' + installed.stderr)
    check(installed.returncode == 0, 'BUILD_INSTALL')
    result = runner(recipe['argv'], env=env, cwd=recipe['working_directory'])
    private.write('build', result.stdout + b'\n--- stderr\n' + result.stderr)
    check(result.returncode == 0, 'BUILD_RUN')
    bundles = sorted((out / 'target/release/bundle/macos').glob('*.app'))
    check([b.name for b in bundles] == [common.APP_NAME], 'BUILD_BUNDLE')
    app = bundles[0]
    facts, errors = bundle_errors(app, plan, vendor, source_root, runner, env, private)
    # The publisher binding and requirement the build compiled in.
    produced = find_publisher_outputs(out / 'target')
    executable = (app / 'Contents/MacOS' / common.MAIN_EXECUTABLE).read_bytes()
    if produced is None:
        errors.append({'check': 'publisher_binding', 'path': None})
    else:
        binding_raw = (produced / 'publisher-build-binding.s1.json').read_bytes()
        requirement_raw = (produced / 'publisher-requirement.txt').read_bytes()
        binding = prepare.parse(binding_raw)
        if (binding.get('input_sha256') != publisher_sha256 or binding.get('production_bundle_identifier') != common.RELEASE['identifier']
                or binding.get('build_context', {}).get('application_version') != common.RELEASE['version']
                or binding.get('requirement_sha256') != sha(requirement_raw) or binding_raw not in executable or requirement_raw not in executable):
            errors.append({'check': 'publisher_binding', 'path': None})
    limitations_raw = limitations_source.read_bytes()
    bundled = app / common.LIMITATIONS_IN_BUNDLE
    bundled_state = ({'sha256': sha(bundled.read_bytes()), 'equal_to_source': bundled.read_bytes() == limitations_raw}
                     if bundled.is_file() else 'not observed')
    if isinstance(bundled_state, dict) and not bundled_state['equal_to_source']:
        errors.append({'check': 'limitations', 'path': common.LIMITATIONS_IN_BUNDLE})
    if errors:
        common.write_returnable(out / 'BUILD_REFUSED.json', {'checks': errors}, out, public_teams)
        raise Failure('BUILD_CHECKS')
    publisher_dir = out / 'publisher'; publisher_dir.mkdir(mode=0o700)
    files = {}
    for key, name in (('binding', 'publisher-build-binding.s1.json'), ('requirement', 'publisher-requirement.txt'),
                      ('projection', 'publisher-build-public-projection.s1.json')):
        raw = (produced / name).read_bytes()
        write_private_input(publisher_dir / name, raw)
        files[key] = {'path': 'publisher/' + name, 'sha256': sha(raw)}
    write_private_input(out / 'RELEASE_LIMITATIONS_4.0.0.md', limitations_raw)
    description = {
        'format': common.CANDIDATE_FORMAT, 'source_revision': common.selected(revision, 'revision'), 'pin': common.selected(pin, 'version'),
        'expected_manifest': common.selected(expected_manifest, 'sha256'), 'plan': completion['files'],
        'build': {'install_argv': INSTALL_ARGV, 'argv': [placeholder(a, out) for a in recipe['argv']],
                  'working_directory': placeholder(recipe['working_directory'], out),
                  'writable_environment': {k: placeholder(env[k], out) for k in WRITABLE_ENVIRONMENT},
                  'environment_sha256': sha(json.dumps(env, sort_keys=True).encode()), 'environment_keys': sorted(env),
                  'returncode': result.returncode, 'cargo_config_sha256': cargo_config_sha256, 'observed_scope': scope,
                  'tool_sha256': contract['tool_sha256'], 'publisher_input_origin': publisher_origin, 'publisher_input_sha256': publisher_sha256},
        'bundle': {'path': str(app.relative_to(out)), 'name': common.APP_NAME, 'executable': common.MAIN_EXECUTABLE,
                   'executable_sha256': facts['executable_sha256'], 'info_plist_sha256': facts['info_plist_sha256'],
                   'identity': facts['identity'], 'inventory': facts['inventory'], 'executable_signature': facts['executable_signature'],
                   'dyld_validate': facts['dyld_validate']},
        'vendor': facts['vendor'], 'resources': facts['resources'], 'publisher': files,
        'limitations': {'source': common.LIMITATIONS_SOURCE, 'sha256': sha(limitations_raw), 'copy': 'RELEASE_LIMITATIONS_4.0.0.md',
                        'bundled': bundled_state},
    }
    # Publish last: write the pending description, verify it, remove the marker, then rename atomically.
    digest = common.write_returnable(out / common.CANDIDATE_PENDING, description, out, public_teams)
    try:
        common.load_candidate(out, name=common.CANDIDATE_PENDING, finishing=True)
    except (ValueError, OSError, KeyError):
        raise Failure('BUILD_FINAL')
    os.unlink(out / 'INCOMPLETE.txt')
    os.rename(out / common.CANDIDATE_PENDING, out / common.CANDIDATE_FILE)
    return {'result': 'complete', 'candidate_sha256': digest, 'signing_executed': False}


def parse_team(publisher_input):
    value = prepare.parse(Path(publisher_input).read_bytes())
    team = value['developer_id_team_identifier']
    require(re.fullmatch('[A-Z0-9]{10}', team) is not None, 'malformed team')
    return team


def pairs(values, what):
    result = {}
    for item in values or []:
        key, sep, value = item.partition('=')
        require(sep and key and key not in result, 'malformed or repeated ' + what)
        result[key] = value
    return result


def main(argv=None, *, stdout=None, stderr=None, **kw):
    stdout, stderr = stdout or sys.stdout, stderr or sys.stderr
    parser = common.FixedParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for key in ('source-root', 'revision', 'vendor', 'expected-manifest', 'pin', 'out'):
        parser.add_argument('--' + key, required=True)
    parser.add_argument('--env', action='append', metavar='KEY=VALUE', help='one of ' + ', '.join(CALLER_ENVIRONMENT))
    parser.add_argument('--cargo-cache', required=True, help='prepared offline Cargo home (registry and git, no links); copied in, never written')
    parser.add_argument('--npm-cache', required=True, help='prepared offline npm cache (no links); copied in, never written')
    parser.add_argument('--tool', action='append', metavar='NAME=PATH', help='resolved path of ' + ', '.join(TOOLS))
    parser.add_argument('--publisher-input', help='optional supplied publisher-build-selection.s1 file; default generated from source')
    parser.add_argument('--publisher-sha256')
    parser.add_argument('--cargo-build-input', default=prepare.CARGO_BUILD_PRESET, choices=[prepare.CARGO_BUILD_PRESET])
    args = parser.parse_args(argv)
    try:
        result = build(source_root=args.source_root, revision=args.revision, vendor=args.vendor,
                       expected_manifest=args.expected_manifest, pin=args.pin, out=args.out,
                       environment=pairs(args.env, 'environment entry'), tools=pairs(args.tool, 'tool'),
                       publisher_input=args.publisher_input, publisher_sha256=args.publisher_sha256,
                       cargo_build_input=args.cargo_build_input, cargo_cache=args.cargo_cache, npm_cache=args.npm_cache, **kw)
    except Failure as failure:
        print('FAILED: ' + failure.reason, file=stderr)
        return 2
    except ValueError:
        print('FAILED: ' + common.REASONS['BUILD_ENVIRONMENT'], file=stderr)
        return 2
    print(json.dumps(result, indent=2), file=stdout)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
