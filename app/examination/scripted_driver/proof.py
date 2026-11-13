#!/usr/bin/env python3
"""The scripted driver's first step: build a test build, launch it once, and report whether its window loaded the
page and ran a script. See README.md beside this file.

  proof.py build --out <folder>            build the test bundle into <folder>/target (from app/, node_modules present)
  proof.py run --bundle <.app> --out <folder> [--timeout seconds]
                                           launch it once with HOME a new folder inside <folder>, read its stages,
                                           write <folder>/report.json; exit 0 only when the script ran and read the page
  proof.py scenario --bundle <.app> --out <folder> [--timeout seconds]
                                           launch it once more, have it walk the first-use setup scenario in its page,
                                           write <folder>/scenario-report.json; exit 0 only on a pass
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
IDENTIFIER = 'dev.chirality.app-v4.scripted-driver'  # the overlay's identifier
SCENARIO = APP / 'examination/standalone/operated/first-use-setup.scenario.json'
STAGES = ('process started', 'page load started', 'page load finished', 'script evaluated')
LIMITS = [
    'Development evidence about a test build. It satisfies nothing in release criteria 1 and 2, is not an operator\'s or '
    'a person\'s observation, and does not replace the owner\'s own use.',
    'A script inside the page sees the page only: native sheets, alerts, the window\'s own buttons and the menu bar are '
    'unseen. There is no second reading through the accessibility tree.',
    'Windows and web views are counted in Tauri\'s creation notifications, in the one process the runner launched, '
    'from before its first window: a second of either ends the run at once, and the final count, stage and exit are '
    'made on the main thread after any notification already queued. A window made outside Tauri (a native sheet, '
    'alert or dialog) passes through no such notification and is not counted; it is unseen. An open in-page dialog '
    'is counted by the script at each step of the scenario.',
    'Other processes: the App is exactly the launched process; every process below it, and every other member of its '
    'process group, is recorded at each census, about every half second (each census followed by a half-second '
    'pause), in both runs, and none is allowed. A process that starts and ends between two censuses, or that leaves '
    'the App\'s process group for another session, is not seen. The run is held awake by a separate caffeinate that '
    'waits on the App\'s number and is in neither.',
    'Exactly one process start is accepted: a run whose stages show the build started more than once does not pass.',
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


def launch(bundle, run_dir, timeout, scenario_input=None, hold_awake=None):
    """Launch the bundle once in a new home; return what happened. The App is exactly the launched process. Throughout
    the run, every other process below it or in its process group is recorded: in both runs, none is allowed. With
    scenario_input ({scenario, values}), the build walks the scenario."""
    executable = bundle / 'Contents/MacOS' / EXECUTABLE
    run_dir.mkdir(parents=True)  # new: an existing run folder is refused
    home, tmp = run_dir / 'home', run_dir / 'tmp'
    (home / 'scripted-driver').mkdir(parents=True)
    tmp.mkdir()
    if scenario_input is not None:
        (home / 'scripted-driver/scenario.json').write_text(json.dumps(scenario_input))
    # An environment built from nothing: no CHIRALITY_ configuration variable, no inherited home.
    env = {'HOME': str(home), 'TMPDIR': str(tmp), 'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'LANG': 'en_US.UTF-8'}
    command = [str(executable)]
    # On macOS the run is held awake by a separate caffeinate that waits on the App's number: it is not in the App's
    # tree or group, so nothing in them is exempted. Elsewhere, as in this file's tests, the run is not held awake.
    awake = Path('/usr/bin/caffeinate').is_file() if hold_awake is None else hold_awake
    started, others_seen, samples = time.time(), set(), 0

    def numbers(*args):
        found = subprocess.run(['pgrep', *args], capture_output=True, text=True).stdout.split()
        return {int(p) for p in found}

    def census(app):
        """Every process below the App, and every other member of its process group (the App leads its own group and
        session), with its command."""
        found, queue = set(), list(numbers('-P', str(app)))
        while queue:
            child = queue.pop()
            if child not in found:
                found.add(child)
                queue += numbers('-P', str(child))
        found |= numbers('-g', str(app))
        found.discard(app)
        named = {}
        for pid in sorted(found):
            command_line = subprocess.run(['ps', '-o', 'command=', '-p', str(pid)], capture_output=True, text=True).stdout.strip()
            named[pid] = command_line or '(ended before it could be named)'
        return named

    with open(run_dir / 'app.out', 'wb') as stdout, open(run_dir / 'app.err', 'wb') as stderr:
        process = subprocess.Popen(command, env=env, stdout=stdout, stderr=stderr, start_new_session=True)
        holder = (subprocess.Popen(['/usr/bin/caffeinate', '-di', '-w', str(process.pid)],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) if awake else None)
        deadline, timed_out = started + timeout, False
        while process.poll() is None:
            if time.time() > deadline:
                timed_out = True
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
                break
            others_seen.update(f'{pid} {command_line}' for pid, command_line in census(process.pid).items())
            samples += 1
            time.sleep(0.5)
        code = process.returncode
        if holder is not None:
            try:
                holder.wait(timeout=10)
            except subprocess.TimeoutExpired:
                holder.terminate()
                holder.wait()
    stages = read_stages(home / 'scripted-driver/stages.jsonl')
    return {'command': command, 'held_awake_by': ['/usr/bin/caffeinate', '-di', '-w', '<the App\'s number>'] if awake else None,
            'environment': env, 'seconds': round(time.time() - started, 1), 'exit_code': code, 'timed_out': timed_out,
            'stages': stages, 'app_pid': process.pid, 'census_samples': samples, 'other_processes_seen': sorted(others_seen),
            'process_started_stages': sum(1 for s in stages if s.get('stage') == 'process started'),
            'app_stderr_tail': (run_dir / 'app.err').read_bytes()[-4000:].decode('utf-8', 'replace')}


def run(bundle, out, timeout):
    bundle = bundle.resolve()
    if not (bundle / 'Contents/MacOS' / EXECUTABLE).is_file():
        print(f'refused: no {EXECUTABLE} in {bundle}', file=sys.stderr)
        return 2
    ran = launch(bundle, out / 'run', timeout)
    stages, code, timed_out = ran['stages'], ran['exit_code'], ran['timed_out']
    names = [s.get('stage') for s in stages]
    evaluated = next((s for s in stages if s.get('stage') == 'script evaluated'), None)
    returned = (evaluated or {}).get('detail', {}).get('returned') or {}
    windows = (evaluated or {}).get('detail', {}).get('windows')
    created = (evaluated or {}).get('detail', {}).get('created') or {}
    finished = next((s for s in stages if s.get('stage') == 'proof finished'), None)
    shown = (bool(evaluated) and returned.get('heading') == EXPECTED_HEADING and windows == 1
             and created.get('windows_ever_created') == 1 and created.get('webviews_ever_created') == 1
             and bool(finished) and finished.get('detail', {}).get('exactly_one_each') is True
             and returned.get('open_dialogs') == 0 and code == 0 and not timed_out
             and ran['process_started_stages'] == 1 and not ran['other_processes_seen']
             and all(s.get('marker') == MARKER.decode() for s in stages))
    reached = [name for name in STAGES if name in names]
    report = {
        'marker': MARKER.decode(), 'bundle': str(bundle), 'command': ran['command'], 'environment': ran['environment'],
        'seconds': ran['seconds'], 'exit_code': code, 'timed_out': timed_out,
        'stages': stages, 'reached': reached,
        'stopped_after': reached[-1] if reached else 'nothing: no stage was written',
        'result': 'shown' if shown else 'not shown',
        'expected': {'heading': EXPECTED_HEADING, 'windows': 1, 'windows_ever_created': 1, 'webviews_ever_created': 1,
                     'open_dialogs': 0, 'exit_code': 0, 'process_started_stages': 1, 'other_processes': 0},
        'app_pid': ran['app_pid'], 'held_awake_by': ran['held_awake_by'], 'census_samples': ran['census_samples'],
        'other_processes_seen': ran['other_processes_seen'], 'process_started_stages': ran['process_started_stages'],
        'app_stderr_tail': ran['app_stderr_tail'],
        'limits': LIMITS,
    }
    (out / 'report.json').write_text(json.dumps(report, indent=1) + '\n')
    print(json.dumps({k: report[k] for k in ('result', 'stopped_after', 'exit_code', 'timed_out', 'seconds')}, indent=1))
    if evaluated:
        print(json.dumps(returned, indent=1))
    return 0 if shown else 1


def scenario(bundle, out, timeout, scenario_path, hold_awake=None):
    """Walk the scenario in the test build and report its verdict. A pass needs: the walk's own verdict pass; exactly
    one window and one web view created; one process start; no other process at any sample; the build ending itself
    with status 0."""
    bundle = bundle.resolve()
    if not (bundle / 'Contents/MacOS' / EXECUTABLE).is_file():
        print(f'refused: no {EXECUTABLE} in {bundle}', file=sys.stderr)
        return 2
    walked = json.loads(Path(scenario_path).read_text())
    run_dir = out / 'scenario-run'
    home = run_dir / 'home'
    values = {'identifier': IDENTIFIER, 'home': str(home),
              'app_data': f'{home}/Library/Application Support/{IDENTIFIER}'}
    ran = launch(bundle, run_dir, timeout, {'scenario': walked, 'values': values}, hold_awake)
    stages = ran['stages']
    finished = next((s for s in stages if s.get('stage') == 'scenario finished'), None)
    result = (finished or {}).get('detail', {}).get('result') or {}
    most_windows = (finished or {}).get('detail', {}).get('most_windows')
    created = (finished or {}).get('detail', {}).get('created') or {}
    one_window = (created.get('windows_ever_created') == 1 and created.get('webviews_ever_created') == 1
                  and most_windows == 1)
    verdict = result.get('verdict') if finished else None
    one_window = one_window and (finished or {}).get('detail', {}).get('exactly_one_each') is True
    passed = (verdict == 'pass' and one_window and ran['process_started_stages'] == 1 and not ran['other_processes_seen']
              and ran['exit_code'] == 0 and not ran['timed_out'] and all(s.get('marker') == MARKER.decode() for s in stages))
    second = any(s.get('stage', '').startswith('run ended: a second') for s in stages)
    if passed:
        overall = 'pass'
    elif verdict == 'fail' or ran['other_processes_seen'] or second or ran['process_started_stages'] > 1 or (finished and not one_window):
        overall = 'fail'
    else:
        overall = 'inconclusive'
    report = {
        'marker': MARKER.decode(), 'scenario': walked.get('scenario'), 'version': walked.get('version'),
        'bundle': str(bundle), 'values': values, 'command': ran['command'], 'environment': ran['environment'],
        'seconds': ran['seconds'], 'exit_code': ran['exit_code'], 'timed_out': ran['timed_out'],
        'verdict': overall, 'walk_verdict': verdict, 'stopped': result.get('stopped'),
        'outcomes': result.get('outcomes'), 'steps': result.get('steps'),
        'census_at_start': result.get('census_at_start'), 'census_at_end': result.get('census_at_end'),
        'most_windows': most_windows, 'created': created, 'app_pid': ran['app_pid'], 'held_awake_by': ran['held_awake_by'],
        'census_samples': ran['census_samples'], 'other_processes_seen': ran['other_processes_seen'],
        'process_started_stages': ran['process_started_stages'],
        'stages': [{k: v for k, v in s.items() if k != 'detail' or s.get('stage') != 'scenario finished'} for s in stages],
        'app_stderr_tail': ran['app_stderr_tail'],
        'limits': LIMITS + [
            'The scenario is judged from its own file against a model of the page built by stated rules (judge.js), '
            'not against the supplier\'s accessibility text; whether the two readings agree is not established.',
            'Every click is element.click() on the page\'s own element, not input from the system.'],
    }
    (out / 'scenario-report.json').write_text(json.dumps(report, indent=1) + '\n')
    lines = [f"{report['scenario']} (version {report['version']}): {overall.upper()}"]
    lines += [f'  {name}: {state}' for name, state in (report['outcomes'] or {}).items()]
    if report['stopped']:
        lines.append(f"  {report['stopped']}")
    for step in report['steps'] or []:
        for check in step.get('checks', []):
            if not check['pass']:
                lines.append(f"  {step['id']} expected {json.dumps(check['expectation'])}, found: {json.dumps(check['found'])}")
    lines.append(f"  windows ever created {created.get('windows_ever_created')}, web views {created.get('webviews_ever_created')}; "
                 f"other processes seen {len(ran['other_processes_seen'])} in {ran['census_samples']} samples; "
                 f"process starts {ran['process_started_stages']}; exit {ran['exit_code']}")
    print('\n'.join(lines))
    return 0 if overall == 'pass' else 1


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
    sc = sub.add_parser('scenario')
    sc.add_argument('--bundle', type=Path, required=True)
    sc.add_argument('--out', type=Path, required=True)
    sc.add_argument('--timeout', type=int, default=300)
    sc.add_argument('--scenario', type=Path, default=SCENARIO)
    sub.add_parser('release-free').add_argument('--out', type=Path, required=True)
    args = parser.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)
    if args.command == 'build':
        return build(args.out.resolve())
    if args.command == 'run':
        return run(args.bundle, args.out.resolve(), args.timeout)
    if args.command == 'scenario':
        return scenario(args.bundle, args.out.resolve(), args.timeout, args.scenario)
    return release_free(args.out.resolve())


if __name__ == '__main__':
    sys.exit(main())
