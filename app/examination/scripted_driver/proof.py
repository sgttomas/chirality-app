#!/usr/bin/env python3
"""The scripted driver's first step: build a test build, launch it once, and report whether its window loaded the
page and ran a script. See README.md beside this file.

  proof.py build --out <folder>            build the test bundle into <folder>/target (from app/, node_modules present)
  proof.py run --bundle <.app> --out <folder> [--timeout seconds]
                                           launch it once with HOME a new folder inside <folder>, read its stages,
                                           write <folder>/report.json; exit 0 only when the script ran and read the page
  proof.py release-free --out <folder>     build with the release features and no driver, and require the marker absent
                                           from that binary and present in the test binary; and require the driver
                                           refused with the release feature

Nothing is clicked or typed. The process is ended by the build itself, or by this script on timeout.
"""
import argparse
import json
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

APP = Path(__file__).resolve().parents[2]
OVERLAY = Path(__file__).resolve().with_name('tauri.scripted-driver.conf.json')
DEV_OVERLAY = APP / 'packaging/unsigned/tauri.development.conf.json'
MARKER = b'chirality-scripted-driver-test-build-v1'
EXPECTED_HEADING = 'Welcome to Chirality'
EXECUTABLE = 'chirality-app-v4'
STAGES = ('process started', 'page load started', 'page load finished', 'script evaluated')
LIMITS = [
    'Development evidence about a test build. It satisfies nothing in release criteria 1 and 2, is not an operator\'s or '
    'a person\'s observation, and does not replace the owner\'s own use.',
    'A script inside the page sees the page only: native sheets, alerts, the window\'s own buttons and the menu bar are '
    'unseen. There is no second reading through the accessibility tree.',
    'The window count is read from the App itself (it must be 1); an open in-page dialog is counted by the script.',
]


def tauri_build(env, target, features, extra_config=()):
    command = ['node', 'node_modules/@tauri-apps/cli/tauri.js', 'build', '--debug', '--no-sign', '--bundles', 'app',
               '--features', features, '--config', str(DEV_OVERLAY), *[a for c in extra_config for a in ('--config', str(c))],
               '--', '--locked']
    environment = {**os.environ, **env, 'CARGO_TARGET_DIR': str(target)}
    return subprocess.run(command, cwd=APP, env=environment)


def build(out):
    started = time.time()
    done = tauri_build({'CHIRALITY_SCRIPTED_DRIVER_BUILD': '1'}, out / 'target', 'custom-protocol', [OVERLAY])
    bundles = sorted((out / 'target/debug/bundle/macos').glob('*.app')) if done.returncode == 0 else []
    print(json.dumps({'built': done.returncode == 0, 'seconds': round(time.time() - started),
                      'bundle': str(bundles[0]) if len(bundles) == 1 else None}, indent=1))
    return 0 if done.returncode == 0 and len(bundles) == 1 else 1


def read_stages(path):
    stages = []
    if path.exists():
        for line in path.read_text().splitlines():
            try:
                stages.append(json.loads(line))
            except ValueError:
                stages.append({'stage': 'unreadable line', 'detail': line})
    return stages


def run(bundle, out, timeout):
    bundle = bundle.resolve()
    executable = bundle / 'Contents/MacOS' / EXECUTABLE
    if not executable.is_file():
        print(f'refused: no {EXECUTABLE} in {bundle}', file=sys.stderr)
        return 2
    run_dir = out / 'run'
    run_dir.mkdir(parents=True)  # new: an existing run folder is refused
    home, tmp = run_dir / 'home', run_dir / 'tmp'
    home.mkdir()
    tmp.mkdir()
    # An environment built from nothing: no CHIRALITY_ configuration variable, no inherited home.
    env = {'HOME': str(home), 'TMPDIR': str(tmp), 'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'LANG': 'en_US.UTF-8'}
    # On macOS the run is held awake (caffeinate exists there); elsewhere, as in this file's tests, it runs bare.
    caffeinate = Path('/usr/bin/caffeinate').is_file()
    command = (['/usr/bin/caffeinate', '-di'] if caffeinate else []) + [str(executable)]
    started = time.time()
    with open(run_dir / 'app.out', 'wb') as stdout, open(run_dir / 'app.err', 'wb') as stderr:
        process = subprocess.Popen(command, env=env, stdout=stdout, stderr=stderr, start_new_session=True)
        try:
            code, timed_out = process.wait(timeout=timeout), False
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            code = process.returncode
    stages = read_stages(home / 'scripted-driver/stages.jsonl')
    names = [s.get('stage') for s in stages]
    evaluated = next((s for s in stages if s.get('stage') == 'script evaluated'), None)
    returned = (evaluated or {}).get('detail', {}).get('returned') or {}
    windows = (evaluated or {}).get('detail', {}).get('windows')
    shown = (bool(evaluated) and returned.get('heading') == EXPECTED_HEADING and windows == 1
             and returned.get('open_dialogs') == 0 and code == 0 and not timed_out
             and all(s.get('marker') == MARKER.decode() for s in stages))
    reached = [name for name in STAGES if name in names]
    report = {
        'marker': MARKER.decode(), 'bundle': str(bundle), 'command': command, 'environment': env,
        'seconds': round(time.time() - started, 1), 'exit_code': code, 'timed_out': timed_out,
        'stages': stages, 'reached': reached,
        'stopped_after': reached[-1] if reached else 'nothing: no stage was written',
        'result': 'shown' if shown else 'not shown',
        'expected': {'heading': EXPECTED_HEADING, 'windows': 1, 'open_dialogs': 0, 'exit_code': 0},
        'app_stderr_tail': (run_dir / 'app.err').read_bytes()[-4000:].decode('utf-8', 'replace'),
        'limits': LIMITS,
    }
    (out / 'report.json').write_text(json.dumps(report, indent=1) + '\n')
    print(json.dumps({k: report[k] for k in ('result', 'stopped_after', 'exit_code', 'timed_out', 'seconds')}, indent=1))
    if evaluated:
        print(json.dumps(returned, indent=1))
    return 0 if shown else 1


def release_free(out):
    """Marker present in the test build, absent from a release-features build of the same revision, and the driver
    refused with the release feature. Every part must run and say so; a part that did not run is a failure."""
    results = {}
    tests = sorted((out / 'target/debug/bundle/macos').glob('*.app'))
    test_binary = tests[0] / 'Contents/MacOS' / EXECUTABLE if len(tests) == 1 else None
    results['marker in the test build'] = bool(test_binary and test_binary.is_file() and MARKER in test_binary.read_bytes())
    release_target = out / 'release-features-target'
    cargo = ['cargo', 'build', '--locked', '--manifest-path', str(APP / 'src-tauri/Cargo.toml'),
             '--features', 'custom-protocol,distribution-successor']
    clean = {k: v for k, v in os.environ.items() if k != 'CHIRALITY_SCRIPTED_DRIVER_BUILD'}
    built = subprocess.run(cargo, env={**clean, 'CARGO_TARGET_DIR': str(release_target)})
    release_binary = release_target / 'debug' / EXECUTABLE
    results['release-features build made'] = built.returncode == 0 and release_binary.is_file()
    results['marker absent from the release-features build'] = (results['release-features build made']
                                                                and MARKER not in release_binary.read_bytes())
    refused = subprocess.run(['cargo', 'check', '--locked', '--manifest-path', str(APP / 'src-tauri/Cargo.toml'),
                              '--lib', '--features', 'distribution-successor'],
                             env={**clean, 'CHIRALITY_SCRIPTED_DRIVER_BUILD': '1', 'CARGO_TARGET_DIR': str(release_target)},
                             capture_output=True, text=True)
    results['driver refused with the release feature'] = (refused.returncode != 0
                                                          and 'scripted driver build refused' in refused.stderr)
    (out / 'release-free.json').write_text(json.dumps(results, indent=1) + '\n')
    report = out / 'report.json'
    if report.exists():  # the release checks join the one report the job uploads
        joined = json.loads(report.read_text())
        joined['release_free'] = results
        report.write_text(json.dumps(joined, indent=1) + '\n')
    print(json.dumps(results, indent=1))
    return 0 if len(results) == 4 and all(results.values()) else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('build').add_argument('--out', type=Path, required=True)
    r = sub.add_parser('run')
    r.add_argument('--bundle', type=Path, required=True)
    r.add_argument('--out', type=Path, required=True)
    r.add_argument('--timeout', type=int, default=180)
    sub.add_parser('release-free').add_argument('--out', type=Path, required=True)
    args = parser.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)
    if args.command == 'build':
        return build(args.out.resolve())
    if args.command == 'run':
        return run(args.bundle, args.out.resolve(), args.timeout)
    return release_free(args.out.resolve())


if __name__ == '__main__':
    sys.exit(main())
