"""Build the unsigned 4.0.0 release candidate and describe it; signs nothing.

Agents run this. It prepares the plan with production_inputs/prepare.py,
checks it, checks the Cargo build input, runs the plan's recipe argv from an
empty environment holding only the allowlisted variables, then checks the
built bundle and writes CANDIDATE.json, which owner_sign.py verifies before it
does anything. No signing, notarization or keychain tool is run, and no
credential, signing identity or provisioning profile is an input.
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


def sibling(name):
    """Load a module of this directory once per process, by file path."""
    key = 'chirality_release_' + name
    if key not in sys.modules:
        spec = importlib.util.spec_from_file_location(key, Path(__file__).resolve().parent / (name + '.py'))
        module = importlib.util.module_from_spec(spec); sys.modules[key] = module; spec.loader.exec_module(module)
    return sys.modules[key]


common = sibling('common')

prepare, inventory, require, sha = common.prepare, common.inventory, common.require, common.sha

KEYCHAIN_SOURCE = 'app/src-tauri/src/capture_seal_keychain.rs'
CALLER_ENVIRONMENT = ('PATH', 'LANG')
TOOLS = ('rustc', 'cargo', 'clang', 'ld')


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


def generate_publisher_input(source_root, directory):
    """Write the two-field publisher-build-selection.s1 file from the source; returns (path, digest)."""
    identifier, team = publisher_values(source_root)
    value = {'format': 'publisher-build-selection.s1', 'production_bundle_identifier': identifier,
             'developer_id_team_identifier': team}
    directory.mkdir(mode=0o700)
    path = directory / 'publisher-build-selection.json'
    return path, common.write_json_new(path, value, mode=0o600)


def observe_scope(runner, env):
    def one(argv):
        result = runner(argv, env=env)
        require(result.returncode == 0, 'could not observe build scope: ' + ' '.join(argv))
        return result.stdout.decode().strip()
    machine = one(['/usr/bin/uname', '-m'])
    require(machine == 'arm64', 'build host is not arm64')
    triple = 'aarch64-apple-darwin'
    return {'host': triple, 'target': triple, 'macos': one(['/usr/bin/sw_vers', '-productVersion']),
            'sdk': one(['/usr/bin/xcrun', '--sdk', 'macosx', '--show-sdk-version'])}


def bundle_errors(app, plan, vendor, source_root, runner, env):
    """Every post-build check; returns (facts, errors). Nothing is executed from the bundle."""
    errors, facts = [], {}
    info_raw, info = common.read_info_plist(app)
    errors += common.release_identity_errors(info)
    facts['info_plist_sha256'] = sha(info_raw)
    facts['identity'] = common.bundle_identity(info)
    executable_path = app / 'Contents/MacOS' / common.MAIN_EXECUTABLE
    executable = executable_path.read_bytes()
    facts['executable_sha256'] = sha(executable)
    tree = inventory.scan(app)
    facts['inventory'] = common.tree_entries(tree)
    # Apple's static validator on the main executable and on every bundled Mach-O.
    validated = []
    for relative in sorted(set(['Contents/MacOS/' + common.MAIN_EXECUTABLE] + common.macho_paths(tree))):
        result = runner(['/usr/bin/dyld_info', '-validate_only', str(app / relative)], env=env)
        validated.append({'path': relative, 'returncode': result.returncode})
        if result.returncode != 0:
            errors.append('dyld_info -validate_only failed: ' + relative)
    facts['dyld_validate'] = validated
    # The App's own code carries only the linker's ad hoc signature.
    try:
        adhoc, slices = common.only_linker_adhoc(executable)
    except ValueError as error:
        adhoc, slices = False, str(error)
    facts['executable_signature'] = slices
    if not adhoc:
        errors.append('main executable carries a signature other than the linker ad hoc one')
    for relative in ('Contents/_CodeSignature', 'Contents/CodeResources', 'Contents/embedded.provisionprofile'):
        if os.path.lexists(app / relative):
            errors.append('bundle already holds ' + relative)
    # Vendor tree: bytes, modes and types equal to the vendor input.
    packaged = inventory.scan(app / common.VENDOR_DESTINATION)
    compared = inventory.compare(packaged, inventory.scan(vendor))
    facts['vendor'] = {'equal': compared['equal'], 'inventory': common.tree_entries(packaged)}
    if not compared['equal']:
        errors.append('packaged vendor tree differs from the vendor input: ' + json.dumps(
            {k: compared[k][:5] for k in ('differing', 'missing', 'extra')} | {'root_mode_equal': compared['root_mode_equal']}))
    # Every mapped resource equals its source, byte for byte and by type.
    account = prepare.parse((plan / 'input-inventory.json').read_bytes())
    resources = []
    for source, item in sorted(account['resource_inputs'].items()):
        destination = app / 'Contents/Resources' / item['destination'].rstrip('/')
        if 'tree' in item:
            original = inventory.scan(item['tree']['root'])
            if not os.path.isdir(destination):
                errors.append('mapped resource tree missing: ' + item['destination']); continue
            placed = inventory.scan(destination)
            def content(t): return {e['path']: (e['kind'], e.get('sha256')) for e in t['entries']}
            equal = content(placed) == content(original)
            modes_equal = inventory.compare(placed, original)['equal']
            resources.append({'destination': item['destination'], 'manifest_sha256': placed['manifest_sha256'],
                              'equal': equal, 'modes_equal': modes_equal})
        else:
            path = Path(source) if Path(source).is_absolute() else Path(os.path.abspath(source_root / 'app/src-tauri' / source))
            equal = destination.is_file() and not destination.is_symlink() and sha(destination.read_bytes()) == sha(path.read_bytes())
            resources.append({'destination': item['destination'], 'sha256': item['sha256'], 'equal': equal})
        if not equal:
            errors.append('mapped resource differs from its source: ' + item['destination'])
    facts['resources'] = resources
    return facts, errors


def find_publisher_outputs(target):
    found = {}
    for binding in sorted(Path(target).glob('release/build/chirality-app-v4-*/out/publisher-build-binding.s1.json')):
        raw = binding.read_bytes()
        if raw.strip() != b'null':
            found.setdefault(raw, binding.parent)
    require(len(found) == 1, 'exactly one selected publisher binding required in the build output')
    return next(iter(found.values()))


WRITABLE_ENVIRONMENT = ('HOME', 'TMPDIR', 'CARGO_HOME', 'CARGO_TARGET_DIR', 'CODEX_HOME', 'NPM_CONFIG_CACHE',
                        'NPM_CONFIG_USERCONFIG', 'NPM_CONFIG_GLOBALCONFIG')
INSTALL_ARGV = ['npm', 'ci', '--offline', '--ignore-scripts', '--no-audit', '--no-fund']
CARGO_CACHE_REFUSED = ('config', 'config.toml', 'credentials', 'credentials.toml', 'env')


def isolated_environment(out):
    """Every location the install and the build may write: all inside the run's own folder."""
    return {'HOME': str(out / 'home'), 'TMPDIR': str(out / 'tmp'), 'CARGO_HOME': str(out / 'cargo-home'),
            'CARGO_TARGET_DIR': str(out / 'target'), 'CODEX_HOME': str(out / 'codex-home'),
            'NPM_CONFIG_CACHE': str(out / 'npm-cache'), 'NPM_CONFIG_USERCONFIG': str(out / 'npm-config/userconfig'),
            'NPM_CONFIG_GLOBALCONFIG': str(out / 'npm-config/globalconfig')}


def build(*, out, **kw):
    """Build and describe a candidate; any failure leaves BUILD_FAILED.json and INCOMPLETE.txt, never CANDIDATE.json."""
    out = Path(os.path.abspath(out))
    existed = os.path.lexists(out)
    try:
        return _build(out=out, **kw)
    except BaseException as error:
        if not existed and out.is_dir() and not (out / common.CANDIDATE_FILE).exists() and not (out / 'BUILD_FAILED.json').exists():
            (out / 'BUILD_FAILED.json').write_text(json.dumps({'result': 'failed', 'reason': f'{type(error).__name__}: {error}'}, indent=2) + '\n')
        raise


def _build(*, source_root, revision, vendor, expected_manifest, pin, out, environment, tools, cargo_cache, npm_cache,
           publisher_input=None, publisher_sha256=None, cargo_build_input=prepare.CARGO_BUILD_PRESET,
           runner=common.system_runner, host=None):
    host = host or (platform.system(), platform.machine())
    require(host == ('Darwin', 'arm64'), 'the release build runs on arm64 macOS only')
    export, vendor, out, cargo_cache, npm_cache = map(inventory.anchored, (source_root, vendor, out, cargo_cache, npm_cache))
    common.refuse_installed_location(out, 'output')
    require(not os.path.lexists(out) and out.parent.is_dir(), 'a new output directory with an existing parent is required')
    require(set(environment) == set(CALLER_ENVIRONMENT), 'exactly these caller environment entries are required: ' + ', '.join(CALLER_ENVIRONMENT))
    require(all(isinstance(v, str) and v and '\n' not in v for v in environment.values()), 'environment values must be non-empty single lines')
    require(all(Path(p).is_absolute() for p in environment['PATH'].split(':')), 'PATH entries must be absolute')
    require(set(tools) == set(TOOLS), 'exact resolved tool paths required for: ' + ', '.join(TOOLS))
    for name in ('rustc', 'cargo'):
        resolved = shutil.which(name, path=environment['PATH'])
        require(resolved is not None and os.path.samefile(resolved, tools[name]), name + ' on the build PATH is not the selected tool')
        proxy = Path(resolved).parent / 'rustup'
        require(not (proxy.exists() and os.path.samefile(proxy, resolved)) and Path(os.path.realpath(resolved)).name != 'rustup',
                name + ' on the build PATH is a rustup proxy; put the toolchain\'s own bin directory on PATH')
    require((publisher_input is None) == (publisher_sha256 is None), 'supply the publisher input file and its digest together')
    require(not os.path.lexists(export / 'app/node_modules'), 'the source export holds node_modules; dependencies come from the npm cache')
    require(not any(os.path.lexists(cargo_cache / n) for n in CARGO_CACHE_REFUSED), 'the Cargo cache input holds configuration or credentials')
    out.mkdir(mode=0o700)
    (out / 'INCOMPLETE.txt').write_text('No candidate until CANDIDATE.json is written and this marker is removed.\n')
    # Inputs are copied in; nothing the build writes reaches the export, the caches or the caller's home.
    source_root = out / 'source'
    shutil.copytree(export, source_root, symlinks=True, copy_function=shutil.copy2)
    shutil.copytree(cargo_cache, out / 'cargo-home', symlinks=True, copy_function=shutil.copy2)
    shutil.copytree(npm_cache, out / 'npm-cache', symlinks=True, copy_function=shutil.copy2)
    for name in ('home', 'tmp', 'codex-home', 'npm-config'):
        (out / name).mkdir(mode=0o700)
    for name in ('userconfig', 'globalconfig'):
        (out / 'npm-config' / name).write_text('')
    limitations_source = source_root / common.LIMITATIONS_SOURCE
    require(limitations_source.is_file() and not limitations_source.is_symlink(), 'source export lacks ' + common.LIMITATIONS_SOURCE)
    if publisher_input is None:
        publisher_input, publisher_sha256 = generate_publisher_input(source_root, out / 'publisher-input')
        publisher_origin = 'generated from ' + KEYCHAIN_SOURCE + ' of the source export'
    else:
        publisher_origin = 'supplied file'
    plan = out / 'plan'
    prepare.prepare(source_root, vendor, expected_manifest, pin, revision, plan, publisher_input=publisher_input,
                    publisher_sha256=publisher_sha256, cargo_build_input=cargo_build_input)
    completion = prepare.check_plan(plan)
    config = prepare.parse((plan / 'tauri.package-inputs.conf.json').read_bytes())
    require(config['productName'] == common.PRODUCT_NAME and config['identifier'] == common.RELEASE['identifier']
            and config['version'] == common.RELEASE['version']
            and config['bundle']['macOS']['minimumSystemVersion'] == common.RELEASE['minimum_system_version']
            and config['bundle']['macOS']['signingIdentity'] is None, 'plan overlay is not the 4.0.0 release identity')
    recipe = prepare.parse((plan / 'build-recipe.json').read_bytes())
    require(recipe['inherit_environment'] is False and '--no-sign' in recipe['argv'], 'recipe must build unsigned from an empty environment')
    env = dict(recipe['environment']) | environment | isolated_environment(out)
    require(set(env) == set(recipe['environment_allowlist']), 'build environment is not exactly the allowlist')
    require(not set(env) & set(recipe['unset_environment']), 'a refused variable is in the build environment')
    for name in WRITABLE_ENVIRONMENT:
        common.require_inside(env[name], out, name)
    cargo_home = inventory.anchored(env['CARGO_HOME'])
    contract = recipe['cargo_build_input']
    # The run's own Cargo home gets exactly the contract's configuration (the cache input may hold none).
    fd = os.open(cargo_home / 'config.toml', os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
    with os.fdopen(fd, 'wb') as handle: handle.write(contract['text'].encode())
    scope = observe_scope(runner, env)
    cargo_config_sha256 = prepare.verify_cargo_build_input(plan, cargo_home, scope, tools)
    require(Path(recipe['working_directory']) == source_root / 'app', 'the recipe does not build the copied source')
    installed = runner(INSTALL_ARGV, env=env, cwd=recipe['working_directory'])
    (out / 'install-stdout.log').write_bytes(installed.stdout); (out / 'install-stderr.log').write_bytes(installed.stderr)
    require(installed.returncode == 0, 'the offline dependency install failed; see install-stderr.log')
    result = runner(recipe['argv'], env=env, cwd=recipe['working_directory'])
    (out / 'build-stdout.log').write_bytes(result.stdout); (out / 'build-stderr.log').write_bytes(result.stderr)
    require(result.returncode == 0, 'the recipe build failed; see build-stderr.log')
    bundles = sorted((out / 'target/release/bundle/macos').glob('*.app'))
    require([b.name for b in bundles] == [common.APP_NAME], 'exactly one ' + common.APP_NAME + ' bundle expected')
    app = bundles[0]
    facts, errors = bundle_errors(app, plan, vendor, source_root, runner, env)
    # The publisher binding and requirement the build compiled in.
    produced = find_publisher_outputs(out / 'target')
    binding_raw = (produced / 'publisher-build-binding.s1.json').read_bytes()
    requirement_raw = (produced / 'publisher-requirement.txt').read_bytes()
    binding = prepare.parse(binding_raw)
    executable = (app / 'Contents/MacOS' / common.MAIN_EXECUTABLE).read_bytes()
    if binding.get('input_sha256') != publisher_sha256: errors.append('compiled binding names another publisher input')
    if binding.get('production_bundle_identifier') != common.RELEASE['identifier']: errors.append('compiled binding names another identifier')
    if binding.get('build_context', {}).get('application_version') != common.RELEASE['version']: errors.append('compiled binding names another version')
    if binding.get('requirement_sha256') != sha(requirement_raw): errors.append('compiled requirement differs from its binding')
    if binding_raw not in executable or requirement_raw not in executable:
        errors.append('main executable does not hold the produced publisher binding and requirement')
    limitations_raw = limitations_source.read_bytes()
    bundled = app / common.LIMITATIONS_IN_BUNDLE
    bundled_state = ({'sha256': sha(bundled.read_bytes()), 'equal_to_source': bundled.read_bytes() == limitations_raw}
                     if bundled.is_file() else 'not present in the bundle')
    if isinstance(bundled_state, dict) and not bundled_state['equal_to_source']:
        errors.append('bundled limitations differ from ' + common.LIMITATIONS_SOURCE)
    if errors:
        (out / 'BUILD_REFUSED.json').write_text(json.dumps({'errors': errors}, indent=2) + '\n')
        raise ValueError('candidate checks failed:\n- ' + '\n- '.join(errors))
    publisher_dir = out / 'publisher'; publisher_dir.mkdir(mode=0o700)
    files = {}
    for key, name in (('binding', 'publisher-build-binding.s1.json'), ('requirement', 'publisher-requirement.txt'),
                      ('projection', 'publisher-build-public-projection.s1.json')):
        raw = (produced / name).read_bytes()
        (publisher_dir / name).write_bytes(raw)
        files[key] = {'path': 'publisher/' + name, 'sha256': sha(raw)}
    (out / 'RELEASE_LIMITATIONS_4.0.0.md').write_bytes(limitations_raw)
    description = {
        'format': common.CANDIDATE_FORMAT, 'source_revision': revision, 'pin': pin, 'expected_manifest': expected_manifest,
        'plan': completion['files'],
        'build': {'install_argv': INSTALL_ARGV, 'argv': recipe['argv'], 'working_directory': recipe['working_directory'],
                  'writable_environment': {k: env[k] for k in WRITABLE_ENVIRONMENT},
                  'environment_sha256': sha(json.dumps(env, sort_keys=True).encode()), 'environment_keys': sorted(env),
                  'returncode': result.returncode, 'cargo_config_sha256': cargo_config_sha256, 'observed_scope': scope,
                  'tool_sha256': contract['tool_sha256'], 'publisher_input_origin': publisher_origin,
                  'publisher_input_sha256': publisher_sha256},
        'bundle': {'path': str(app.relative_to(out)), 'name': common.APP_NAME, 'executable': common.MAIN_EXECUTABLE,
                   'executable_sha256': facts['executable_sha256'], 'info_plist_sha256': facts['info_plist_sha256'],
                   'identity': facts['identity'], 'inventory': facts['inventory'], 'executable_signature': facts['executable_signature'],
                   'dyld_validate': facts['dyld_validate']},
        'vendor': facts['vendor'], 'resources': facts['resources'], 'publisher': files,
        'limitations': {'source': common.LIMITATIONS_SOURCE, 'sha256': sha(limitations_raw), 'copy': 'RELEASE_LIMITATIONS_4.0.0.md',
                        'bundled': bundled_state},
        'limits': ['unsigned candidate; signing, notarization and the installed observation are the owner\'s acts',
                   'source revision is the caller\'s claim about the export'],
    }
    digest = common.write_json_new(out / common.CANDIDATE_FILE, description)
    (out / 'INCOMPLETE.txt').unlink()
    common.load_candidate(out)
    return {'candidate': str(out), 'candidate_sha256': digest, 'bundle': str(app), 'signing_executed': False}


def pairs(values, what):
    result = {}
    for item in values or []:
        key, sep, value = item.partition('=')
        require(sep and key and key not in result, 'malformed or repeated ' + what + ': ' + key)
        result[key] = value
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for key in ('source-root', 'revision', 'vendor', 'expected-manifest', 'pin', 'out'):
        parser.add_argument('--' + key, required=True)
    parser.add_argument('--env', action='append', metavar='KEY=VALUE', help='one of ' + ', '.join(CALLER_ENVIRONMENT))
    parser.add_argument('--cargo-cache', required=True, help='prepared offline Cargo home (registry and git); copied in, never written')
    parser.add_argument('--npm-cache', required=True, help='prepared offline npm cache; copied in, never written')
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
                       cargo_build_input=args.cargo_build_input, cargo_cache=args.cargo_cache, npm_cache=args.npm_cache)
    except (ValueError, OSError) as error:
        print('FAILED: ' + str(error) + ' (no candidate; the output, if created, holds BUILD_FAILED.json)', file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
