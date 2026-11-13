#!/usr/bin/env python3
"""Build one unsigned debug development App candidate for identification (DEL-09-01).

Exports a named revision, verifies the export, optionally verifies a supplier
release package against its canonical distribution record and extracts it for
bundling, builds offline by the route in app/packaging/unsigned/README.md with a
fresh development identifier, and writes the build facts that identify.py
record consumes. It does not run the identification, launch, sign or download,
and does not execute the supplier.

What it guarantees:
1. It writes into a new directory it creates, disjoint by filesystem identity
   from its inputs (the repository, the npm cache and cargo home inputs, the
   supplier archive and record, the node and Rust toolchain folders): no
   existing ancestor of the output root is an input or inside one, and no input
   is inside the output root.
2. It accepts a build only when the bundle output folder holds exactly the
   planned development bundle and that bundle passes validation against the
   plan; otherwise it writes no build facts and prints nothing.
3. A development bundle's identifier, names and file name are judged by one
   rule shared with identification (identify.judge_development_bundle), which
   refuses the release identity: com.chirality.app, the name Chirality and the
   file name Chirality.app.

It also refuses known reserved locations as the output root (listed in
RESERVED_LOCATIONS, not exhaustive), and it sets every writable location of the
build tools' environment inside the output root (private HOME, npm cache, logs
and configuration, CARGO_HOME, TMPDIR, target), re-checking them by
device and inode between steps. It makes no Codex home and sets no CODEX_HOME:
nothing in the build runs the supplier, and the caller's CODEX_HOME is not
carried. The npm cache and cargo home inputs are copied
in and the build uses the copies; the toolchain is reached through its own bin
folders.

Limit: these checks are not a filesystem snapshot or a hostile concurrent-writer
isolation service. They do not confine npm, cargo or the Tauri command; a
process that replaces a path while one of them runs can redirect that tool's
writes, and system tools that ignore HOME and TMPDIR are not covered. No
operating-system write restriction is applied. Run it only in a location the
caller controls.
"""
import argparse
import contextlib
from datetime import datetime, timezone
from xml.parsers.expat import ExpatError
import hashlib
import json
import os
from pathlib import Path
import plistlib
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
PASSED = ('LANG', 'LC_ALL', 'USER', 'LOGNAME')  # carried from the caller; no signing variables, home or cache locations
SYSTEM_PATH = '/usr/bin:/bin:/usr/sbin:/sbin'
RESERVED_LOCATIONS = ('/Applications', '/Library', '/System')  # a courtesy list, not exhaustive; plus each home's Library and Applications
INPUTS = ('node_bin', 'rust_bin', 'npm_cache', 'cargo_home')
WRITABLE_FILES = ('NPM_CONFIG_USERCONFIG', 'NPM_CONFIG_GLOBALCONFIG')
WRITABLE = ('HOME', 'TMPDIR', 'XDG_CACHE_HOME', 'XDG_CONFIG_HOME', 'CARGO_HOME', 'CARGO_TARGET_DIR',
            'NPM_CONFIG_CACHE', 'NPM_CONFIG_PREFIX', 'NPM_CONFIG_LOGS_DIR') + WRITABLE_FILES
TAG = re.compile(r'[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*')  # no dots, spaces or parentheses
PREFIX = 'dev.chirality.app-v4.candidate.'


def planned_names(tag):
    """The identifier and product name this script plans; judged by identification's shared rule."""
    if not isinstance(tag, str) or not TAG.fullmatch(tag):
        raise ValueError('tag must be letters and digits, optionally joined by single hyphens')
    identifier, product = PREFIX + tag, f'Chirality App v4 (development {tag})'
    identify.judge_development_bundle(identifier, product + '.app', (product, product))
    return identifier, product


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


def reserved_locations():
    homes = sorted({os.path.expanduser('~'), pwd.getpwuid(os.getuid()).pw_dir})
    return [*RESERVED_LOCATIONS, *(os.path.join(h, n) for h in homes for n in ('Library', 'Applications'))]


def refuse_reserved(root, chain):
    """Courtesy refusal of known locations (listed, not exhaustive), whether or not each exists yet."""
    ancestors = {ident for ident, _ in chain}
    planned = os.path.normpath(str(root)).lower()
    for place in reserved_locations():
        try:
            matched = _ident(place) in ancestors
        except FileNotFoundError:  # not there yet: compare the normalised path, case-insensitively
            listed = os.path.normpath(place).lower()
            matched = planned == listed or planned.startswith(listed + '/')
        if matched:
            raise ValueError(f'output root is inside the reserved location {place} (a listed location; the list is not exhaustive)')


def disjoint(root, inputs, chain, root_id=None):
    """Invariant 1: the output root and every input are disjoint by filesystem identity, in both directions."""
    ancestors = {ident for ident, _ in chain}
    root = Path(root)
    root_ids = {tuple(root_id)} if root_id else ({_ident(root)} if os.path.lexists(root) else set())
    for name, path in inputs.items():
        real = os.path.realpath(path)
        if _ident(real) in ancestors:
            raise ValueError(f'output root is inside the {name} input: {path}')
        if root == Path(real) or root in Path(real).parents or root_ids & {ident for ident, _ in _ancestry(real)}:
            raise ValueError(f'the {name} input is inside the output root: {path}')


def output_root(out, inputs):
    """A new path whose ancestry has no symlink, disjoint from the inputs and outside the reserved list."""
    root = Path(os.path.abspath(out))
    for ancestor in reversed(root.parents):
        if os.path.islink(ancestor):
            raise ValueError('symlink in output root ancestry: ' + str(ancestor))
    deepest = root
    while not os.path.lexists(deepest):
        deepest = deepest.parent
    chain = _ancestry(deepest)
    refuse_reserved(root, chain)
    disjoint(root, inputs, chain)
    if os.path.lexists(root):
        raise ValueError('output root already exists: ' + str(root))
    if not root.parent.is_dir():
        raise ValueError('output root parent is not a directory: ' + str(root.parent))
    return root


def contained(root, root_id, path):
    """path lies inside the output root by device and inode ancestry, with no symlink or shared file on the way."""
    root, path = Path(root), Path(os.path.abspath(path))
    info = os.lstat(root)
    if not stat.S_ISDIR(info.st_mode) or (info.st_dev, info.st_ino) != tuple(root_id):
        raise ValueError('output root replaced or not the held directory: ' + str(root))
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


def _default_node(environ, home):
    node = _which('node', environ.get('PATH', ''))
    if not os.path.basename(os.path.realpath(node)).startswith('node'):
        raise ValueError('node on PATH is a shim; pass --node-bin')
    return os.path.dirname(node)


def _default_rust(environ, home):
    cargo = _which('cargo', environ.get('PATH', ''))
    if not os.path.basename(os.path.realpath(cargo)).startswith('rustup'):
        return os.path.dirname(cargo)
    rustup_home = environ.get('RUSTUP_HOME') or os.path.join(home, '.rustup')
    toolchain = tomllib.loads(Path(rustup_home, 'settings.toml').read_text()).get('default_toolchain')
    if not isinstance(toolchain, str) or not TAG.fullmatch(toolchain.replace('.', '-')):
        raise ValueError('no usable rustup default toolchain; pass --rust-bin')
    return os.path.join(rustup_home, 'toolchains', toolchain, 'bin')


DEFAULTS = {
    'node_bin': _default_node,
    'rust_bin': _default_rust,
    'npm_cache': lambda environ, home: environ.get('NPM_CONFIG_CACHE') or environ.get('npm_config_cache') or os.path.join(home, '.npm'),
    'cargo_home': lambda environ, home: environ.get('CARGO_HOME') or os.path.join(home, '.cargo'),
}


def default_inputs(environ, keys=INPUTS):
    """Defaults for the named inputs: toolchain folders and standard offline caches, found without running anything."""
    home = environ.get('HOME') or os.path.expanduser('~')
    return {key: DEFAULTS[key](environ, home) for key in keys}


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
    given.update(default_inputs(environ, [k for k in INPUTS if k not in given]))
    inputs = _check_inputs(given)
    repo = Path(os.path.abspath(repo))
    top = identify.git(repo, 'rev-parse', '--show-toplevel').decode().strip()
    commit = identify.git(repo, 'rev-parse', '--verify', revision + '^{commit}').decode().strip()
    input_paths = {'repository': top, 'npm cache': inputs['npm_cache'], 'cargo home': inputs['cargo_home'],
                   'node toolchain': inputs['node_bin'], 'Rust toolchain': inputs['rust_bin']}
    if supplier_archive:
        input_paths.update({'supplier archive': os.path.abspath(supplier_archive),
                            'supplier record': os.path.abspath(supplier_record)})
    root = output_root(out, input_paths)
    tag = tag or f"{(today or datetime.now(timezone.utc)):%Y%m%d}-{commit[:8]}-{secrets.token_hex(3)}"
    identifier, product = planned_names(tag)
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
               NPM_CONFIG_CACHE=str(root / 'npm-cache'), NPM_CONFIG_USERCONFIG=str(home / '.npmrc'),
               NPM_CONFIG_GLOBALCONFIG=str(home / 'npmrc-global'), NPM_CONFIG_PREFIX=str(home / 'npm-prefix'),
               NPM_CONFIG_LOGS_DIR=str(home / 'npm-logs'), NPM_CONFIG_UPDATE_NOTIFIER='false', NPM_CONFIG_OFFLINE='true')
    build = ['node', 'node_modules/@tauri-apps/cli/tauri.js', 'build', '--debug', '--no-sign', '--bundles', 'app',
             '--features', 'custom-protocol', '--config', DEV_OVERLAY, '--config', str(overlay_path),
             '--', '--offline', '--locked']
    return {'repo': str(repo), 'commit': commit, 'root': str(root), 'parent_id': list(_ident(root.parent)),
            'input_paths': input_paths, 'source': str(root / 'source'),
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
    """A writable copy (clone where the filesystem offers it) of an input; links refuse."""
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
    """Create the root through a held descriptor of the checked parent; return the held root descriptor and identity."""
    root = Path(p['root'])
    parent = os.open(root.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        info = os.fstat(parent)
        if [info.st_dev, info.st_ino] != list(p['parent_id']):
            raise ValueError('output root parent replaced since planning: ' + str(root.parent))
        chain, current = [], os.dup(parent)
        try:
            while True:  # the held parent's real ancestry, walked by '..' from the descriptor
                here = os.fstat(current)
                chain.append(((here.st_dev, here.st_ino), None))
                up = os.open('..', os.O_RDONLY | os.O_DIRECTORY, dir_fd=current)
                above = os.fstat(up)
                os.close(current)
                current = up
                if (above.st_dev, above.st_ino) == (here.st_dev, here.st_ino):
                    break
        finally:
            os.close(current)
        refuse_reserved(root, chain)
        disjoint(root, p['input_paths'], chain)
        os.mkdir(root.name, 0o700, dir_fd=parent)
        fd = os.open(root.name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent)
    finally:
        os.close(parent)
    try:
        os.fchmod(fd, 0o700)
        held = os.fstat(fd)
        disjoint(root, p['input_paths'], chain, root_id=(held.st_dev, held.st_ino))
    except BaseException:
        os.close(fd)
        raise
    return fd, (held.st_dev, held.st_ino)


def create_file(root, root_id, path, data):
    """Exclusive, no-follow creation of a file re-checked inside the held root immediately before opening."""
    contained(root, root_id, path)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
    with os.fdopen(fd, 'wb') as stream:
        stream.write(data)


def make_dir(root, root_id, path, mode=0o700):
    contained(root, root_id, path)
    os.mkdir(path, mode)


def revalidate(p, root_id, required):
    """At a step boundary: every writable place exists as a real directory (or file) inside the held root."""
    root, env = Path(p['root']), p['env']
    for key in WRITABLE:
        path = contained(root, root_id, env[key])
        kind = os.lstat(path).st_mode
        if not (stat.S_ISREG(kind) if key in WRITABLE_FILES else stat.S_ISDIR(kind)):
            raise ValueError(f'{key} is not the expected {"file" if key in WRITABLE_FILES else "directory"}: {path}')
    for path in required:
        path = contained(root, root_id, path)
        if not stat.S_ISDIR(os.lstat(path).st_mode):
            raise ValueError('not a directory inside the output root: ' + str(path))


def prepare_environment(p, root_id):
    """The private home, temporary folder, npm cache and cargo home, all inside the root."""
    root, env, inputs = Path(p['root']), p['env'], p['inputs']
    for key in ('HOME', 'TMPDIR', 'XDG_CACHE_HOME', 'XDG_CONFIG_HOME', 'NPM_CONFIG_CACHE',
                'NPM_CONFIG_PREFIX', 'NPM_CONFIG_LOGS_DIR', 'CARGO_HOME', 'CARGO_TARGET_DIR'):
        make_dir(root, root_id, env[key])
    for key in WRITABLE_FILES:
        create_file(root, root_id, env[key], b'')
    copy_input(Path(inputs['npm_cache'], '_cacache'), root / 'npm-cache/_cacache', root, root_id)
    copied = []
    for name in ('registry', 'git'):
        if Path(inputs['cargo_home'], name).is_dir():
            copy_input(Path(inputs['cargo_home'], name), root / 'cargo-home' / name, root, root_id)
            copied.append(name)
    create_file(root, root_id, root / 'cargo-home/config.toml', b'[net]\noffline = true\n')
    return {'node_bin': inputs['node_bin'], 'rust_bin': inputs['rust_bin'],
            'npm_cache_input': os.path.join(inputs['npm_cache'], '_cacache') + ' (input; the build uses a copy in the output root)',
            'cargo_home_input': f"{inputs['cargo_home']}: {', '.join(copied)} (input; the build uses a copy in the output root)"}


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
    """Verify the archive and every member header against the record, then extract into tree; nothing is executed."""
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


def _part(root, root_id, path, what):
    path = contained(root, root_id, path)
    if not os.path.lexists(path):
        raise ValueError(f'bundle {what} missing: {path}')
    return path, os.lstat(path)


def validate_bundle(p, root_id):
    """Invariant 2: the bundle output folder holds exactly the planned bundle, which matches the plan."""
    root, bundle = Path(p['root']), Path(p['bundle'])
    folder = contained(root, root_id, bundle.parent)
    if not os.path.isdir(folder) or os.path.islink(folder) or sorted(os.listdir(folder)) != [bundle.name]:
        raise ValueError('bundle output folder does not hold exactly the planned bundle: ' + str(folder))
    plist_path, _ = _part(root, root_id, bundle / 'Contents/Info.plist', 'Info.plist')
    with _regular(plist_path) as stream:
        plist = plistlib.loads(stream.read(1 << 20))
    if not isinstance(plist, dict):
        raise ValueError('bundle Info.plist is not a dictionary')
    identifier, name, display = (plist.get(k) for k in ('CFBundleIdentifier', 'CFBundleName', 'CFBundleDisplayName'))
    if not all(isinstance(v, str) for v in (identifier, name, display)):
        raise ValueError('bundle identifier or names missing')
    identify.judge_development_bundle(identifier, bundle.name, (name, display))
    if (identifier, name, display) != (p['identifier'], p['product'], p['product']):
        raise ValueError('bundle identifier or names differ from the plan: ' + identifier)
    executable = plist.get('CFBundleExecutable')
    if not isinstance(executable, str) or not executable or '/' in executable or executable in ('.', '..'):
        raise ValueError('bundle executable name invalid')
    _, info = _part(root, root_id, bundle / 'Contents/MacOS' / executable, 'executable')
    if not stat.S_ISREG(info.st_mode) or info.st_size == 0 or not info.st_mode & 0o111:
        raise ValueError('bundle executable missing, empty or not executable: ' + executable)
    for resource in ('instructions', 'workflows'):
        folder, _ = _part(root, root_id, bundle / 'Contents/Resources' / resource, 'resources ' + resource)
        if not stat.S_ISDIR(os.lstat(folder).st_mode) or not os.listdir(folder):
            raise ValueError('bundle resources missing or empty: ' + resource)
    if p['supplier']:
        _, info = _part(root, root_id, bundle / 'Contents/Resources/codex/bin/codex', 'supplier entrypoint')
        if not stat.S_ISREG(info.st_mode) or not info.st_mode & 0o111:
            raise ValueError('bundled supplier entrypoint missing or not executable')
    return {'identifier': identifier, 'name': name, 'executable': executable}


def run(p):
    """Build facts are written after both steps exit 0, the lockfiles are unchanged and validate_bundle accepts the bundle."""
    root, source = Path(p['root']), Path(p['source'])
    identify.judge_development_bundle(p['overlay']['identifier'], p['overlay']['productName'] + '.app',
                                      (p['overlay']['productName'],))
    if (p['overlay']['identifier'], p['overlay']['productName']) != (p['identifier'], p['product']):
        raise ValueError('overlay identity differs from the plan')
    if json.loads(p['overlay_bytes']) != p['overlay']:
        raise ValueError('overlay bytes differ from the planned overlay')
    started, phases = now(), {}
    fd, root_id = create_root(p)
    try:
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
        create_file(root, root_id, p['overlay_path'], p['overlay_bytes'])
        app = source / 'app'
        lockfiles = {name: sha((source / name).read_bytes()) for name in LOCKFILES}
        env = p['env']
        for tool in ('node', 'npm', 'cargo', 'rustc'):
            toolchain[tool] = _version([tool, '--version'], env, app / 'src-tauri')
        contained(root, root_id, root / 'build.log')
        log_fd = os.open(root / 'build.log', os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
        with os.fdopen(log_fd, 'wb') as log:
            revalidate(p, root_id, [source, app])
            mark = now()
            _run(p['install'], env, app, log)
            phases['npm_install'] = f'{mark}/{now()}'
            revalidate(p, root_id, [source, app, app / 'node_modules'])
            bundle = Path(p['bundle'])
            for path in (bundle.parent, bundle):
                if os.path.lexists(contained(root, root_id, path)):
                    raise ValueError('bundle path exists before the build step: ' + str(path))
            toolchain['tauri_cli'] = json.loads((app / 'node_modules/@tauri-apps/cli/package.json').read_bytes())['version']
            mark = now()
            _run(p['build'], env, app, log)
            phases['tauri_build'] = f'{mark}/{now()}'
            revalidate(p, root_id, [source, app, app / 'node_modules'])
        if {name: sha((source / name).read_bytes()) for name in LOCKFILES} != lockfiles:
            raise ValueError('a lockfile changed during the build')
        validate_bundle(p, root_id)
        result = facts(p, sha((app / DEV_OVERLAY).read_bytes()), toolchain, lockfiles, started, now(), phases)
        create_file(root, root_id, root / 'build-facts.json', json.dumps(result, indent=2, ensure_ascii=False).encode() + b'\n')
        return result
    finally:
        os.close(fd)


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
    parser.add_argument('--out', required=True, help='new output root, created private; disjoint from every input and '
                        'not a listed reserved location (the list is not exhaustive); run only where you control the location')
    parser.add_argument('--supplier-archive', help='existing supplier release package; not downloaded or executed by this script')
    parser.add_argument('--supplier-record', help='its committed canonical distribution record')
    parser.add_argument('--tag', help='identifier tag (default: UTC date, short commit and random suffix)')
    parser.add_argument('--node-bin', help='folder holding node and npm (default: from PATH)')
    parser.add_argument('--rust-bin', help="Rust toolchain bin folder (default: from PATH or rustup's default toolchain)")
    parser.add_argument('--npm-cache', help='prepared npm cache, copied in (default: $NPM_CONFIG_CACHE or ~/.npm)')
    parser.add_argument('--cargo-home', help='prepared cargo home; its registry is copied in (default: $CARGO_HOME or ~/.cargo)')
    args = parser.parse_args(argv)
    try:
        p = plan(args.repo, args.revision, args.out, args.supplier_archive, args.supplier_record, args.tag,
                 inputs={k: getattr(args, k) for k in INPUTS})
        run(p)
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError, tarfile.TarError,
            plistlib.InvalidFileException, ExpatError) as error:
        print(json.dumps({'error': f'{type(error).__name__}: {error}'}), file=sys.stderr)
        return 2
    print(json.dumps({'root': p['root'], 'commit': p['commit'], 'identifier': p['identifier'], 'bundle': p['bundle']}, indent=2))
    print('Identify it next with:\n' + next_command(p))
    return 0


if __name__ == '__main__':
    sys.exit(main())
