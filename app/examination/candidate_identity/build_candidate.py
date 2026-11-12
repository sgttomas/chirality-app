#!/usr/bin/env python3
"""Build one unsigned debug development App candidate for identification (DEL-09-01).

Exports a named revision into a new private output root and verifies the export;
when given a supplier release package and its canonical distribution record,
verifies the archive and extracts its tree for bundling; builds offline by the
route in app/packaging/unsigned/README.md with a fresh development identifier;
and writes the build facts that identify.py record consumes. It does not run the
identification, launch, sign or download anything, and never executes the supplier.

It writes only under the caller's new output root, never under /Applications or
the user's Library. The 4.0.0 package installs as Chirality.app with identifier
com.chirality.app in place of the owner's v3.0.1, so a development build may
only carry an identifier under dev.chirality.app-v4.candidate. and a product
name of the form "Chirality App v4 (development <tag>)"; anything else refuses.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import shlex
import stat
import subprocess
import sys
import tarfile

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import bundled_supplier  # noqa: E402
import identify  # noqa: E402

DEV_OVERLAY = 'packaging/unsigned/tauri.development.conf.json'
INSTALL = ['npm', 'install', '--offline', '--no-audit', '--no-fund', '--ignore-scripts']
LOCKFILES = ('app/package-lock.json', 'app/src-tauri/Cargo.lock')
PASSED = ('HOME', 'PATH', 'LANG', 'LC_ALL', 'USER', 'LOGNAME', 'CARGO_HOME', 'RUSTUP_HOME')  # never signing variables
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


def output_root(out, repo_top):
    """A new path outside the repository whose existing ancestry has no symlink."""
    root = Path(os.path.abspath(out))
    for ancestor in reversed(root.parents):
        if os.path.islink(ancestor):
            raise ValueError('symlink in output root ancestry: ' + str(ancestor))
    if os.path.lexists(root):
        raise ValueError('output root already exists: ' + str(root))
    if not root.parent.is_dir():
        raise ValueError('output root parent is not a directory: ' + str(root.parent))
    top = Path(os.path.realpath(repo_top))
    if root == top or top in root.parents:
        raise ValueError('output root is inside the repository')
    for reserved in (Path('/Applications'), Path(os.path.expanduser('~')) / 'Library', Path('/Library')):
        if root == reserved or reserved in root.parents:
            raise ValueError('output root is under ' + str(reserved))
    return root


def plan(repo, revision, out, supplier_archive=None, supplier_record=None, tag=None, environ=None, today=None):
    """Everything the build will do, computed without writing or building."""
    if bool(supplier_archive) != bool(supplier_record):
        raise ValueError('a supplier needs both its archive and its canonical distribution record')
    environ = os.environ if environ is None else environ
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
    env = {k: environ[k] for k in PASSED if k in environ}
    if 'PATH' not in env or 'HOME' not in env:
        raise ValueError('PATH and HOME are required to find the toolchain and its offline caches')
    env.update(TMPDIR=str(root / 'tmp'), CARGO_TARGET_DIR=str(root / 'target'), CODEX_HOME=str(root / 'codex-home'),
               CARGO_NET_OFFLINE='true', NPM_CONFIG_OFFLINE='true')
    build = ['node', 'node_modules/@tauri-apps/cli/tauri.js', 'build', '--debug', '--no-sign', '--bundles', 'app',
             '--features', 'custom-protocol', '--config', DEV_OVERLAY, '--config', str(overlay_path),
             '--', '--offline', '--locked']
    return {'repo': str(repo), 'commit': commit, 'root': str(root), 'source': str(root / 'source'),
            'tag': tag, 'identifier': identifier, 'product': product, 'supplier': supplier,
            'overlay': overlay, 'overlay_bytes': json.dumps(overlay, indent=2).encode() + b'\n',
            'overlay_path': str(overlay_path), 'env': env, 'install': INSTALL, 'build': build,
            'bundle': str(root / 'target/debug/bundle/macos' / (product + '.app'))}


def facts(p, dev_overlay_sha256, toolchain, lockfiles, started_at, finished_at, phases):
    """The build object of candidate identification v2/v3."""
    steps = [f"export {p['commit']} and verify it against the revision"]
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
    return identify.verify_export(repo, commit, '.', source)


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
    """Verify the archive against the record and extract it into tree; never executed."""
    with _regular(record) as stream:
        raw = stream.read(1_048_577)
    if len(raw) > 1_048_576:
        raise ValueError('distribution record too large')
    account = bundled_supplier.distribution_facts(raw)
    # The bundled container mode is not a supplier member (the record's root_mode); 0755 matches
    # every directory the package declares, and the private output root bounds access to it.
    os.mkdir(tree)
    os.chmod(tree, 0o755)
    with _regular(archive) as stream:
        before = os.fstat(stream.fileno())
        size, digest = 0, hashlib.sha256()
        while chunk := stream.read(1 << 20):
            digest.update(chunk); size += len(chunk)
        if (size, digest.hexdigest()) != (account['archive']['size_bytes'], account['archive']['sha256']):
            raise ValueError('supplier archive differs from its distribution record')
        stream.seek(0)
        directories, seen = {}, set()
        with tarfile.open(fileobj=stream, mode='r:gz') as tar:
            for member in tar:
                name = member.name[:-1] if member.isdir() and member.name.endswith('/') else member.name
                if not name or name in seen or any(p in ('', '.', '..') for p in name.split('/')):
                    raise ValueError('duplicate or invalid supplier archive path: ' + repr(member.name))
                seen.add(name)
                if member.isdir():
                    if member.mode & ~0o755:
                        raise ValueError('supplier archive directory mode refused: ' + name)
                    directories[name] = member.mode
                elif not member.isfile():
                    raise ValueError('supplier archive link or special file refused: ' + name)
                tar.extract(member, tree, filter='data')
        after = os.fstat(stream.fileno())
        if (before.st_ino, before.st_size, before.st_mtime_ns) != (after.st_ino, after.st_size, after.st_mtime_ns):
            raise ValueError('supplier archive changed during extraction')
    for name, mode in directories.items():  # the data filter leaves directory modes to the umask
        os.chmod(os.path.join(tree, name), mode)
    found = tree_entries(tree)
    differing = sorted(p for p in found.keys() | account['inventory'].keys() if found.get(p) != account['inventory'].get(p))
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
    root, source = Path(p['root']), Path(p['source'])
    check_names(p['overlay']['identifier'], p['overlay']['productName'])
    if json.loads(p['overlay_bytes']) != p['overlay']:
        raise ValueError('overlay bytes differ from the planned overlay')
    started, phases = now(), {}
    os.mkdir(root, 0o700)
    os.chmod(root, 0o700)
    for name in ('tmp', 'codex-home'):
        os.mkdir(root / name, 0o700)
    exported = export(p['repo'], p['commit'], source)
    phases['export'] = f"{started}/{now()}: {exported['tracked_files_verified']} tracked files verified"
    if p['supplier']:
        mark = now()
        prepare_supplier(p['supplier']['archive'], p['supplier']['record'], p['supplier']['tree'])
        phases['supplier'] = f'{mark}/{now()}'
    Path(p['overlay_path']).write_bytes(p['overlay_bytes'])
    app = source / 'app'
    lockfiles = {name: sha((source / name).read_bytes()) for name in LOCKFILES}
    env = p['env']
    toolchain = {}
    for tool in ('node', 'npm', 'cargo', 'rustc'):
        toolchain[tool] = _version([tool, '--version'], env, app / 'src-tauri')
        toolchain[tool + '_path'] = _version(['/usr/bin/which', tool], env, app)
    with open(root / 'build.log', 'ab') as log:
        mark = now()
        _run(p['install'], env, app, log)
        phases['npm_install'] = f'{mark}/{now()}'
        toolchain['tauri_cli'] = json.loads((app / 'node_modules/@tauri-apps/cli/package.json').read_bytes())['version']
        mark = now()
        _run(p['build'], env, app, log)
        phases['tauri_build'] = f'{mark}/{now()}'
    if {name: sha((source / name).read_bytes()) for name in LOCKFILES} != lockfiles:
        raise ValueError('a lockfile changed during the build')
    if not Path(p['bundle']).is_dir():
        raise ValueError('expected bundle not produced: ' + p['bundle'])
    result = facts(p, sha((app / DEV_OVERLAY).read_bytes()), toolchain, lockfiles, started, now(), phases)
    (root / 'build-facts.json').write_bytes(json.dumps(result, indent=2, ensure_ascii=False).encode() + b'\n')
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
    args = parser.parse_args(argv)
    try:
        p = plan(args.repo, args.revision, args.out, args.supplier_archive, args.supplier_record, args.tag)
        run(p)
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError, tarfile.TarError, json.JSONDecodeError) as error:
        print(json.dumps({'error': f'{type(error).__name__}: {error}'}), file=sys.stderr)
        return 2
    print(json.dumps({'root': p['root'], 'commit': p['commit'], 'identifier': p['identifier'], 'bundle': p['bundle']}, indent=2))
    print('Identify it next with:\n' + next_command(p))
    return 0


if __name__ == '__main__':
    sys.exit(main())
