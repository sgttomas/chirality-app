#!/usr/bin/env python3
"""Build one unsigned debug development App candidate for identification (DEL-09-01).

Exports a named revision into a new private output root and verifies the export;
when given a supplier release package and its canonical distribution record,
verifies the archive and extracts its tree for bundling; builds offline by the
route in app/packaging/unsigned/README.md with a fresh development identifier;
and writes the build facts that identify.py record consumes. It does not run the
identification, launch, sign or download anything, and never executes the supplier.

It writes only inside the caller's new output root, and every place it creates
or writes is checked to lie inside that root by device and inode ancestry, with
no symlink on the way. The build runs with a private HOME (npm's cache, logs
and configuration inside it, update notifier off), a private CARGO_HOME, TMPDIR,
CODEX_HOME and target. The caller's prepared offline caches (an npm cache and a
cargo home) are read-only inputs copied into the root; the toolchain is reached
through the node and Rust toolchain bin folders, never rustup's shims. Nothing
is written under the repository, /Applications, /Library, /System or the user's
Library or Applications folders.

The 4.0.0 package installs as Chirality.app with identifier com.chirality.app
in place of the owner's v3.0.1, so a development build may only carry an
identifier under dev.chirality.app-v4.candidate. and a product name of the form
"Chirality App v4 (development <tag>)"; anything else refuses.
"""
import argparse
import contextlib
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import pwd
import re
import secrets
import shlex
import shutil
import stat
import subprocess
import sys
import tarfile
import tomllib

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import bundled_supplier  # noqa: E402
import identify  # noqa: E402

DEV_OVERLAY = 'packaging/unsigned/tauri.development.conf.json'
INSTALL = ['npm', 'install', '--offline', '--no-audit', '--no-fund', '--ignore-scripts']
LOCKFILES = ('app/package-lock.json', 'app/src-tauri/Cargo.lock')
PASSED = ('LANG', 'LC_ALL', 'USER', 'LOGNAME')  # never signing variables, never the caller's home or caches
SYSTEM_PATH = '/usr/bin:/bin:/usr/sbin:/sbin'
FORBIDDEN = ('/Applications', '/Library', '/System')
INPUTS = ('node_bin', 'rust_bin', 'npm_cache', 'cargo_home')
TAG = re.compile(r'[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*')  # no dots, spaces or parentheses
PREFIX = 'dev.chirality.app-v4.candidate.'
RELEASED = ('com.chirality.app', 'Chirality')  # the 4.0.0 package's identifier and product name


def check_names(identifier, product):
    """Refuse anything that could collide with the installed release App."""
    tag = identifier[len(PREFIX):] if identifier.startswith(PREFIX) else ''
    if not TAG.fullmatch(tag) or identifier.lower() == RELEASED[0]:
        raise ValueError('development identifier must be ' + PREFIX + '<tag>: ' + repr(identifier))
    if product.strip().lower() in (RELEASED[1].lower(), RELEASED[1].lower() + '.app') \
            or product != f'Chirality App v4 (development {tag})':
        raise ValueError('development product name must be "Chirality App v4 (development <tag>)": ' + repr(product))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def _ident(path):
    info = os.stat(path)
    return info.st_dev, info.st_ino


def _ancestry(path):
    """(device, inode) of an existing path and each of its ancestors."""
    path = Path(path)
    return [(_ident(p), p) for p in (path, *path.parents)]


def _forbidden(repo_top):
    homes = sorted({os.path.expanduser('~'), pwd.getpwuid(os.getuid()).pw_dir})
    found = {}
    for place in (repo_top, *FORBIDDEN, *(os.path.join(h, n) for h in homes for n in ('Library', 'Applications'))):
        with contextlib.suppress(FileNotFoundError):
            found.setdefault(_ident(place), place)
    return found


def output_root(out, repo_top):
    """A new path whose ancestry has no symlink and, by identity, no forbidden place."""
    root = Path(os.path.abspath(out))
    for ancestor in reversed(root.parents):
        if os.path.islink(ancestor):
            raise ValueError('symlink in output root ancestry: ' + str(ancestor))
    if os.path.lexists(root):
        raise ValueError('output root already exists: ' + str(root))
    if not root.parent.is_dir():
        raise ValueError('output root parent is not a directory: ' + str(root.parent))
    forbidden = _forbidden(repo_top)
    for ident, place in _ancestry(root.parent):
        if ident in forbidden:
            raise ValueError(f'output root is inside {forbidden[ident]} (reached as {place})')
    return root


def contained(root, root_id, path):
    """path lies inside the output root by device and inode ancestry, with no symlink or shared file on the way."""
    root, path = Path(root), Path(os.path.abspath(path))
    if _ident(root) != root_id:
        raise ValueError('output root replaced')
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        raise ValueError('outside the output root: ' + str(path)) from None
    if not parts or '..' in parts:
        raise ValueError('not a path inside the output root: ' + str(path))
    deepest = current = root
    for part in parts:
        current = current / part
        if not os.path.lexists(current):
            break
        info = os.lstat(current)
        if stat.S_ISLNK(info.st_mode):
            raise ValueError('symlink inside the output root: ' + str(current))
        if not stat.S_ISDIR(info.st_mode) and info.st_nlink != 1:
            raise ValueError('hard-linked file inside the output root: ' + str(current))
        deepest = current
    if root_id not in {i for i, _ in _ancestry(os.path.realpath(deepest))}:
        raise ValueError('outside the output root: ' + str(path))
    return path


def _which(name, search):
    found = shutil.which(name, path=search)
    if not found:
        raise ValueError(f'{name} is not on PATH; name its folder explicitly')
    return found


def default_inputs(environ):
    """The caller's toolchain folders and standard offline caches, found without running anything."""
    home = environ.get('HOME') or os.path.expanduser('~')
    search = environ.get('PATH', '')
    node = _which('node', search)
    if not os.path.basename(os.path.realpath(node)).startswith('node'):
        raise ValueError('node on PATH is a shim; pass --node-bin')
    cargo = _which('cargo', search)
    if os.path.basename(os.path.realpath(cargo)).startswith('rustup'):
        rustup_home = environ.get('RUSTUP_HOME') or os.path.join(home, '.rustup')
        toolchain = tomllib.loads(Path(rustup_home, 'settings.toml').read_text()).get('default_toolchain')
        if not isinstance(toolchain, str) or not TAG.fullmatch(toolchain.replace('.', '-')):
            raise ValueError('no usable rustup default toolchain; pass --rust-bin')
        rust_bin = os.path.join(rustup_home, 'toolchains', toolchain, 'bin')
    else:
        rust_bin = os.path.dirname(cargo)
    return {'node_bin': os.path.dirname(node), 'rust_bin': rust_bin,
            'npm_cache': environ.get('NPM_CONFIG_CACHE') or environ.get('npm_config_cache') or os.path.join(home, '.npm'),
            'cargo_home': environ.get('CARGO_HOME') or os.path.join(home, '.cargo')}


def _check_inputs(inputs):
    inputs = {k: os.path.abspath(inputs[k]) for k in INPUTS}
    for folder, tools in (('node_bin', ('node', 'npm')), ('rust_bin', ('cargo', 'rustc'))):
        for tool in tools:
            path = os.path.join(inputs[folder], tool)
            if not os.path.isfile(path) or os.path.basename(os.path.realpath(path)).startswith('rustup'):
                raise ValueError(f'{tool} is not a toolchain file in {inputs[folder]}')
    if not os.path.isdir(os.path.join(inputs['npm_cache'], '_cacache')):
        raise ValueError('npm cache input has no _cacache: ' + inputs['npm_cache'])
    if not os.path.isdir(os.path.join(inputs['cargo_home'], 'registry')):
        raise ValueError('cargo home input has no registry: ' + inputs['cargo_home'])
    return inputs


def plan(repo, revision, out, supplier_archive=None, supplier_record=None, tag=None, environ=None, today=None, inputs=None):
    """Everything the build will do, computed without writing or building."""
    if bool(supplier_archive) != bool(supplier_record):
        raise ValueError('a supplier needs both its archive and its canonical distribution record')
    environ = os.environ if environ is None else environ
    given = {k: v for k, v in (inputs or {}).items() if v}
    if set(INPUTS) - set(given):
        given = {**default_inputs(environ), **given}
    inputs = _check_inputs(given)
    repo = Path(os.path.abspath(repo))
    top = identify.git(repo, 'rev-parse', '--show-toplevel').decode().strip()
    commit = identify.git(repo, 'rev-parse', '--verify', revision + '^{commit}').decode().strip()
    root = output_root(out, top)
    tag = tag or f"{(today or datetime.now(timezone.utc)):%Y%m%d}-{commit[:8]}-{secrets.token_hex(3)}"
    if not isinstance(tag, str) or not TAG.fullmatch(tag):
        raise ValueError('tag must be letters and digits, optionally joined by single hyphens')
    identifier = PREFIX + tag
    product = f'Chirality App v4 (development {tag})'
    check_names(identifier, product)
    overlay = {'identifier': identifier, 'productName': product}
    supplier = None
    if supplier_archive:
        supplier = {'archive': os.path.abspath(supplier_archive), 'record': os.path.abspath(supplier_record),
                    'tree': str(root / 'codex-package')}
        overlay['bundle'] = {'resources': {supplier['tree'] + '/': 'codex/'}}
    overlay_path = root / 'tauri.candidate.conf.json'
    home = root / 'home'
    env = {k: environ[k] for k in PASSED if k in environ}
    env.update(HOME=str(home), PATH=f"{inputs['node_bin']}:{inputs['rust_bin']}:{SYSTEM_PATH}",
               TMPDIR=str(root / 'tmp'), XDG_CACHE_HOME=str(home / '.cache'), XDG_CONFIG_HOME=str(home / '.config'),
               CARGO_HOME=str(root / 'cargo-home'), CARGO_TARGET_DIR=str(root / 'target'), CARGO_NET_OFFLINE='true',
               CODEX_HOME=str(root / 'codex-home'),
               NPM_CONFIG_CACHE=str(root / 'npm-cache'), NPM_CONFIG_USERCONFIG=str(home / '.npmrc'),
               NPM_CONFIG_GLOBALCONFIG=str(home / 'npmrc-global'), NPM_CONFIG_PREFIX=str(home / 'npm-prefix'),
               NPM_CONFIG_LOGS_DIR=str(home / 'npm-logs'), NPM_CONFIG_UPDATE_NOTIFIER='false', NPM_CONFIG_OFFLINE='true')
    build = ['node', 'node_modules/@tauri-apps/cli/tauri.js', 'build', '--debug', '--no-sign', '--bundles', 'app',
             '--features', 'custom-protocol', '--config', DEV_OVERLAY, '--config', str(overlay_path),
             '--', '--offline', '--locked']
    return {'repo': str(repo), 'commit': commit, 'root': str(root), 'source': str(root / 'source'),
            'tag': tag, 'identifier': identifier, 'product': product, 'supplier': supplier, 'inputs': inputs,
            'overlay': overlay, 'overlay_bytes': json.dumps(overlay, indent=2).encode() + b'\n',
            'overlay_path': str(overlay_path), 'env': env, 'install': INSTALL, 'build': build,
            'bundle': str(root / 'target/debug/bundle/macos' / (product + '.app'))}


def facts(p, dev_overlay_sha256, toolchain, lockfiles, started_at, finished_at, phases):
    """The build object of candidate identification v2/v3."""
    steps = [f"export {p['commit']} and verify it against the revision",
             'copy the npm cache and cargo registry inputs into the output root for a private HOME and CARGO_HOME']
    if p['supplier']:
        steps.append('verify the supplier release package against its canonical distribution record and extract it')
    steps += [' '.join(p['install']) + ' in app/', 'then the command in app/']
    return {
        'procedure': f"app/examination/candidate_identity/build_candidate.py (sha256 {sha(Path(__file__).read_bytes())}), "
                     f"unsigned debug route of app/packaging/unsigned/README.md: " + '; '.join(steps),
        'profile': 'debug', 'signing': 'none', 'features': ['custom-protocol'], 'command': p['build'],
        'config_overlays': [{'path': 'app/' + DEV_OVERLAY, 'sha256': dev_overlay_sha256},
                            {'path': p['overlay_path'], 'sha256': sha(p['overlay_bytes']), 'content': p['overlay']}],
        'toolchain': toolchain, 'lockfiles': lockfiles, 'offline': True, 'environment': p['env'],
        'started_at': started_at, 'finished_at': finished_at, 'phases': phases,
    }


def export(repo, commit, source):
    """git archive of the revision, extracted with the data filter, then verified blob by blob."""
    os.mkdir(source, 0o700)
    archive = subprocess.Popen(['git', '-C', repo, 'archive', '--format=tar', commit], stdout=subprocess.PIPE,
                               env=dict(os.environ, GIT_NO_LAZY_FETCH='1', GIT_NO_REPLACE_OBJECTS='1'))
    with archive.stdout, tarfile.open(fileobj=archive.stdout, mode='r|') as tar:
        tar.extractall(source, filter='data')
    if archive.wait():
        raise ValueError('git archive failed')
    exported = identify.verify_export(repo, commit, '.', source)
    if exported['tracked_files_verified'] < 1:
        raise ValueError('export verified no tracked files')
    return exported


def copy_input(source, target, root, root_id):
    """A writable copy (clone where the filesystem offers it) of a read-only input; links refuse."""
    contained(root, root_id, target)
    if subprocess.run(['cp', '-c', '-R', str(source), str(target)], capture_output=True).returncode:
        shutil.rmtree(target, ignore_errors=True)
        shutil.copytree(source, target, symlinks=True)
    for current, dirs, files in os.walk(target):
        for name in dirs + files:
            if os.path.islink(os.path.join(current, name)):
                raise ValueError('link in a copied input refused: ' + os.path.join(current, name))
    contained(root, root_id, target)


def create_root(p):
    root = Path(p['root'])
    os.mkdir(root, 0o700)
    os.chmod(root, 0o700)
    return _ident(root)


def prepare_environment(p, root_id):
    """The private home, temporary folder, Codex home, npm cache and cargo home, all inside the root."""
    root, home, inputs = Path(p['root']), Path(p['env']['HOME']), p['inputs']
    for folder in (home, root / 'tmp', root / 'codex-home', root / 'npm-cache', root / 'cargo-home'):
        contained(root, root_id, folder)
        os.mkdir(folder, 0o700)
    for name in ('.npmrc', 'npmrc-global'):
        contained(root, root_id, home / name)
        with open(home / name, 'xb'):
            pass
    copy_input(Path(inputs['npm_cache'], '_cacache'), root / 'npm-cache/_cacache', root, root_id)
    copied = []
    for name in ('registry', 'git'):
        if Path(inputs['cargo_home'], name).is_dir():
            copy_input(Path(inputs['cargo_home'], name), root / 'cargo-home' / name, root, root_id)
            copied.append(name)
    contained(root, root_id, root / 'cargo-home/config.toml')
    with open(root / 'cargo-home/config.toml', 'xb') as config:
        config.write(b'[net]\noffline = true\n')
    return {'node_bin': inputs['node_bin'], 'rust_bin': inputs['rust_bin'],
            'npm_cache_input': os.path.join(inputs['npm_cache'], '_cacache') + ' (read only; copied into the output root)',
            'cargo_home_input': f"{inputs['cargo_home']}: {', '.join(copied)} (read only; copied into the output root)"}


def _regular(path):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    stream = os.fdopen(fd, 'rb')
    if not stat.S_ISREG(os.fstat(fd).st_mode):
        stream.close()
        raise ValueError('not a regular file: ' + str(path))
    return stream


def tree_entries(root):
    """Files and directories under root, as the distribution inventory states them; links refuse."""
    found = {}
    for current, dirs, files in os.walk(root):
        for name in sorted(dirs + files):
            path = os.path.join(current, name)
            relative = os.path.relpath(path, root).replace(os.sep, '/')
            info = os.lstat(path)
            if stat.S_ISDIR(info.st_mode):
                found[relative] = {'kind': 'dir', 'mode': stat.S_IMODE(info.st_mode)}
            elif stat.S_ISREG(info.st_mode):
                with _regular(path) as stream:
                    digest = hashlib.sha256()
                    while chunk := stream.read(1 << 20):
                        digest.update(chunk)
                found[relative] = {'kind': 'file', 'mode': stat.S_IMODE(info.st_mode), 'size': info.st_size,
                                   'sha256': digest.hexdigest()}
            else:
                raise ValueError('extracted supplier link or special file: ' + relative)
    return found


def prepare_supplier(archive, record, tree):
    """Verify the archive and every member header against the record, then extract into tree; never executed."""
    with _regular(record) as stream:
        raw = stream.read(1_048_577)
    if len(raw) > 1_048_576:
        raise ValueError('distribution record too large')
    account = bundled_supplier.distribution_facts(raw)
    inventory = account['inventory']
    with _regular(archive) as stream:
        before = os.fstat(stream.fileno())
        size, digest = 0, hashlib.sha256()
        while chunk := stream.read(1 << 20):
            digest.update(chunk); size += len(chunk)
        if (size, digest.hexdigest()) != (account['archive']['size_bytes'], account['archive']['sha256']):
            raise ValueError('supplier archive differs from its distribution record')
        stream.seek(0)
        with tarfile.open(fileobj=stream, mode='r:gz') as tar:
            members = {}
            for member in tar:  # every header is checked before anything is extracted
                name = member.name[:-1] if member.isdir() and member.name.endswith('/') else member.name
                if not name or name in members or any(p in ('', '.', '..') for p in name.split('/')):
                    raise ValueError('duplicate or invalid supplier archive path: ' + repr(member.name))
                kind = 'dir' if member.isdir() else 'file' if member.isfile() else None
                if kind is None:
                    raise ValueError('supplier archive link or special file refused: ' + name)
                expected = inventory.get(name)
                if expected is None or (expected['kind'], expected['mode']) != (kind, member.mode) \
                        or kind == 'file' and expected['size'] != member.size:
                    raise ValueError('supplier archive member differs from the distribution record inventory: ' + name)
                members[name] = member
            if set(members) != set(inventory):
                raise ValueError('supplier archive members differ from the distribution record inventory')
            # The bundled container mode is not a supplier member (the record's root_mode); 0755 matches
            # every directory the package declares, and the private output root bounds access to it.
            os.mkdir(tree)
            os.chmod(tree, 0o755)
            for member in members.values():
                tar.extract(member, tree, filter='data')
        after = os.fstat(stream.fileno())
        if (before.st_ino, before.st_size, before.st_mtime_ns) != (after.st_ino, after.st_size, after.st_mtime_ns):
            raise ValueError('supplier archive changed during extraction')
    for name, member in members.items():  # the data filter leaves directory modes to the umask
        if member.isdir():
            os.chmod(os.path.join(tree, name), member.mode)
    found = tree_entries(tree)
    differing = sorted(p for p in found.keys() | inventory.keys() if found.get(p) != inventory.get(p))
    if differing:
        raise ValueError('extracted supplier differs from the distribution record inventory: ' + differing[0])
    return account


def _version(command, env, cwd):
    return subprocess.run(command, env=env, cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()


def _run(command, env, cwd, log):
    log.write(f"$ {shlex.join(command)}  (in {cwd}, started {now()})\n".encode()); log.flush()
    result = subprocess.run(command, env=env, cwd=cwd, stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
    log.write(f"exit {result.returncode} at {now()}\n".encode()); log.flush()
    if result.returncode:
        raise ValueError(f'{command[0]} failed (exit {result.returncode}); see build.log')


def run(p):
    """Build facts are written only after both steps exit 0, the lockfiles are unchanged and the bundle exists."""
    root, source = Path(p['root']), Path(p['source'])
    check_names(p['overlay']['identifier'], p['overlay']['productName'])
    if json.loads(p['overlay_bytes']) != p['overlay']:
        raise ValueError('overlay bytes differ from the planned overlay')
    started, phases = now(), {}
    root_id = create_root(p)
    toolchain = prepare_environment(p, root_id)
    phases['environment'] = f'{started}/{now()}'
    mark = now()
    contained(root, root_id, source)
    exported = export(p['repo'], p['commit'], source)
    phases['export'] = f"{mark}/{now()}: {exported['tracked_files_verified']} tracked files verified"
    if p['supplier']:
        mark = now()
        contained(root, root_id, p['supplier']['tree'])
        prepare_supplier(p['supplier']['archive'], p['supplier']['record'], p['supplier']['tree'])
        phases['supplier'] = f'{mark}/{now()}'
    contained(root, root_id, p['overlay_path'])
    with open(p['overlay_path'], 'xb') as overlay:
        overlay.write(p['overlay_bytes'])
    app = source / 'app'
    lockfiles = {name: sha((source / name).read_bytes()) for name in LOCKFILES}
    env = p['env']
    for tool in ('node', 'npm', 'cargo', 'rustc'):
        toolchain[tool] = _version([tool, '--version'], env, app / 'src-tauri')
    contained(root, root_id, root / 'target')
    contained(root, root_id, root / 'build.log')
    with open(root / 'build.log', 'xb') as log:
        mark = now()
        _run(p['install'], env, app, log)
        phases['npm_install'] = f'{mark}/{now()}'
        toolchain['tauri_cli'] = json.loads((app / 'node_modules/@tauri-apps/cli/package.json').read_bytes())['version']
        mark = now()
        _run(p['build'], env, app, log)
        phases['tauri_build'] = f'{mark}/{now()}'
    if {name: sha((source / name).read_bytes()) for name in LOCKFILES} != lockfiles:
        raise ValueError('a lockfile changed during the build')
    if not os.path.isdir(p['bundle']):
        raise ValueError('expected bundle not produced: ' + p['bundle'])
    contained(root, root_id, p['bundle'])
    result = facts(p, sha((app / DEV_OVERLAY).read_bytes()), toolchain, lockfiles, started, now(), phases)
    contained(root, root_id, root / 'build-facts.json')
    with open(root / 'build-facts.json', 'xb') as out:
        out.write(json.dumps(result, indent=2, ensure_ascii=False).encode() + b'\n')
    return result


def next_command(p):
    command = ['python3', str(HERE / 'identify.py'), 'record', '--app', p['bundle'], '--repo', p['repo'],
               '--revision', p['commit'], '--prefix', '.', '--export-root', p['source'],
               '--build-facts', str(Path(p['root']) / 'build-facts.json'),
               '--out-dir', str(Path(p['root']) / 'identification')]
    if p['supplier']:
        command += ['--supplier-archive', p['supplier']['archive'], '--supplier-acquisition', p['supplier']['record']]
    return shlex.join(command) + ' --identified-at "$(date -u +%Y-%m-%dT%H:%M:%SZ)"'


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--repo', required=True, help='this repository')
    parser.add_argument('--revision', required=True, help='revision to build, resolved to a full commit')
    parser.add_argument('--out', required=True, help='new output root outside the repository; created private')
    parser.add_argument('--supplier-archive', help='existing supplier release package; never downloaded or executed')
    parser.add_argument('--supplier-record', help='its committed canonical distribution record')
    parser.add_argument('--tag', help='identifier tag (default: UTC date, short commit and random suffix)')
    parser.add_argument('--node-bin', help='folder holding node and npm (default: from PATH)')
    parser.add_argument('--rust-bin', help="Rust toolchain bin folder (default: from PATH or rustup's default toolchain)")
    parser.add_argument('--npm-cache', help='prepared npm cache, read only and copied (default: $NPM_CONFIG_CACHE or ~/.npm)')
    parser.add_argument('--cargo-home', help='prepared cargo home, read only; registry copied (default: $CARGO_HOME or ~/.cargo)')
    args = parser.parse_args(argv)
    try:
        p = plan(args.repo, args.revision, args.out, args.supplier_archive, args.supplier_record, args.tag,
                 inputs={k: getattr(args, k) for k in INPUTS})
        run(p)
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError, tarfile.TarError) as error:
        print(json.dumps({'error': f'{type(error).__name__}: {error}'}), file=sys.stderr)
        return 2
    print(json.dumps({'root': p['root'], 'commit': p['commit'], 'identifier': p['identifier'], 'bundle': p['bundle']}, indent=2))
    print('Identify it next with:\n' + next_command(p))
    return 0


if __name__ == '__main__':
    sys.exit(main())
