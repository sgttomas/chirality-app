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
  proof.py setup --bundle <.app> --out <folder> [--timeout seconds]
                                           three launches in one throwaway home: first-use setup with a typed project,
                                           desktop setup's confirmation answered by the test build's stand-in (leave,
                                           then create), and a relaunch; write <folder>/setup-report.json; exit 0 only
                                           on a pass. The App's native confirmation is not exercised.
  proof.py release-free --out <folder>     build with the release features and no driver, and require the marker absent
                                           from that binary and present in the test binary; and require the driver
                                           refused with the release feature

Nothing is clicked or typed. The process is ended by the build itself, or by this script on timeout.
"""
import argparse
import json
import re
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
SETUP_SCENARIO = Path(__file__).resolve().with_name('setup-complete.scenario.json')
STAND_IN_MARKER = b'chirality-setup-confirmation-stand-in-v1'  # scripted_driver.rs STAND_IN_MARKER
CODEX = 'Contents/Resources/codex/bin/codex'  # the copy of Codex the bundle ships; the App starts it
SIGN_IN_FILE = 'auth.json'  # the name of Codex's sign-in file in a home; never opened
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
    'pause) while the App runs, in both runs, and none is allowed. A process that starts and ends between two '
    'censuses, that starts after the last census before the App ends, or that leaves the App\'s process group for '
    'another session, is not seen. A census that cannot be taken (a listing command that fails), or a run with no '
    'census at all, prevents a pass. The run is held awake by a separate caffeinate that waits on the App\'s number '
    'and is in neither.',
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


def launch(bundle, run_dir, timeout, scenario_input=None, hold_awake=None, home=None, allowed=None, frameworks_home=False):
    """Launch the bundle once; return what happened. The App is exactly the launched process. Throughout the run, every
    other process below it or in its process group is recorded: none is allowed, except a process `allowed(pid)` says
    is the App's own Codex (the setup scenario's relaunch), which is recorded apart with the network connections it
    held at each census. With scenario_input ({scenario, values}), the build walks the scenario. A new home is made in
    run_dir unless `home` names one to keep (the setup scenario's launches share one); the stages file is moved into
    run_dir afterwards, so each launch reads only its own."""
    executable = bundle / 'Contents/MacOS' / EXECUTABLE
    run_dir.mkdir(parents=True)  # new: an existing run folder is refused
    home, tmp = (run_dir / 'home' if home is None else home), run_dir / 'tmp'
    (home / 'scripted-driver').mkdir(parents=True, exist_ok=True)
    tmp.mkdir()
    (home / 'scripted-driver/scenario.json').unlink(missing_ok=True)
    if scenario_input is not None:
        (home / 'scripted-driver/scenario.json').write_text(json.dumps(scenario_input))
    # An environment built from nothing: no CHIRALITY_ configuration variable, no inherited home. The setup scenario
    # also points the system frameworks at the home (CFFIXED_USER_HOME), as the launcher does, so what they write is
    # inside it and in its inventory.
    env = {'HOME': str(home), 'TMPDIR': str(tmp), 'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'LANG': 'en_US.UTF-8'}
    if frameworks_home:
        env['CFFIXED_USER_HOME'] = str(home)
    allowed_seen, network = set(), {}
    command = [str(executable)]
    # On macOS the run is held awake by a separate caffeinate that waits on the App's number: it is not in the App's
    # tree or group, so nothing in them is exempted. Elsewhere, as in this file's tests, the run is not held awake.
    awake = Path('/usr/bin/caffeinate').is_file() if hold_awake is None else hold_awake
    started, others_seen, samples, census_failures = time.time(), set(), 0, []

    def numbers(*args):
        """pgrep exits 0 when it lists processes and 1 when there are none; anything else is a census that could not be
        taken, kept with its status and error, and it prevents a pass. It is never read as "no process"."""
        listed = subprocess.run(['pgrep', *args], capture_output=True, text=True)
        if listed.returncode not in (0, 1):
            census_failures.append({'census': samples + 1, 'command': ['pgrep', *args], 'exit_code': listed.returncode,
                                    'stderr': listed.stderr.strip()[-500:]})
        return {int(p) for p in listed.stdout.split()}

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
            for pid, command_line in census(process.pid).items():
                if allowed is not None and allowed(pid):
                    allowed_seen.add(f'{pid} {command_line}')
                    held = subprocess.run(['lsof', '-a', '-p', str(pid), '-i', '-n', '-P', '-F', 'n'], capture_output=True, text=True)
                    # A fact only, never a gate: the network connections the App's own Codex held at this census.
                    network.setdefault(str(pid), set()).update(line[1:] for line in held.stdout.split() if line.startswith('n'))
                else:
                    others_seen.add(f'{pid} {command_line}')
            samples += 1
            time.sleep(0.5)
        code = process.returncode
        # What the App left in its group after it ended is seen too: the App's own Codex (where allowed) is recorded
        # apart, anything else counts as another process; then each is ended, and said.
        left = numbers('-g', str(process.pid)) - {process.pid}
        for pid in sorted(left):
            if allowed is not None and allowed(pid):
                allowed_seen.add(f'{pid} (left in the App\'s group after it ended)')
            else:
                others_seen.add(f'{pid} (left in the App\'s group after it ended)')
            try:
                os.kill(pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
        if holder is not None:
            try:
                holder.wait(timeout=10)
            except subprocess.TimeoutExpired:
                holder.terminate()
                holder.wait()
    stages = read_stages(home / 'scripted-driver/stages.jsonl')
    if (home / 'scripted-driver/stages.jsonl').exists():
        (home / 'scripted-driver/stages.jsonl').rename(run_dir / 'stages.jsonl')
    return {'command': command, 'held_awake_by': ['/usr/bin/caffeinate', '-di', '-w', '<the App\'s number>'] if awake else None,
            'environment': env, 'seconds': round(time.time() - started, 1), 'exit_code': code, 'timed_out': timed_out,
            'stages': stages, 'app_pid': process.pid, 'census_samples': samples, 'other_processes_seen': sorted(others_seen),
            'census_failures': census_failures, 'census_taken': samples > 0 and not census_failures,
            'allowed_codex_seen': sorted(allowed_seen), 'codex_network_connections': {k: sorted(v) for k, v in network.items()},
            'left_in_group_and_ended': sorted(left),
            'process_started_stages': sum(1 for s in stages if s.get('stage') == 'process started'),
            'app_stderr_tail': (run_dir / 'app.err').read_bytes()[-4000:].decode('utf-8', 'replace')}


def heading_wait(stages):
    """How the wait for the expected heading went: the tries made, whether the heading came, every distinct heading
    read in order (None for none), and the last. A wrong page and a slow one read differently here."""
    evaluated = next((s for s in stages if s.get('stage') == 'script evaluated'), None)
    if evaluated is None:
        return None
    detail = evaluated.get('detail') or {}
    return {'expected': detail.get('expected_heading'), 'seen': detail.get('expected_seen'),
            'tries_made': detail.get('attempt'), 'tries_allowed': detail.get('tries'),
            'headings_seen': detail.get('headings_seen'), 'last_heading': (detail.get('returned') or {}).get('heading')}


def census_said(ran):
    if ran['census_failures']:
        return f"a census could not be taken ({len(ran['census_failures'])} failed listing commands)"
    return 'every census was taken' if ran['census_samples'] else 'a census could not be taken (none was made)'


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
             and ran['process_started_stages'] == 1 and not ran['other_processes_seen'] and ran['census_taken']
             and all(s.get('marker') == MARKER.decode() for s in stages))
    reached = [name for name in STAGES if name in names]
    report = {
        'marker': MARKER.decode(), 'bundle': str(bundle), 'command': ran['command'], 'environment': ran['environment'],
        'seconds': ran['seconds'], 'exit_code': code, 'timed_out': timed_out,
        'stages': stages, 'reached': reached,
        'stopped_after': reached[-1] if reached else 'nothing: no stage was written',
        'result': 'shown' if shown else 'not shown',
        'heading_wait': heading_wait(stages),
        'expected': {'heading': EXPECTED_HEADING, 'windows': 1, 'windows_ever_created': 1, 'webviews_ever_created': 1,
                     'open_dialogs': 0, 'exit_code': 0, 'process_started_stages': 1, 'other_processes': 0},
        'app_pid': ran['app_pid'], 'held_awake_by': ran['held_awake_by'], 'census_samples': ran['census_samples'],
        'census': census_said(ran), 'census_failures': ran['census_failures'],
        'other_processes_seen': ran['other_processes_seen'], 'process_started_stages': ran['process_started_stages'],
        'app_stderr_tail': ran['app_stderr_tail'],
        'limits': LIMITS,
    }
    (out / 'report.json').write_text(json.dumps(report, indent=1) + '\n')
    print(json.dumps({k: report[k] for k in ('result', 'stopped_after', 'heading_wait', 'exit_code', 'timed_out', 'seconds')}, indent=1))
    if evaluated:
        print(json.dumps(returned, indent=1))
    return 0 if shown else 1


def scenario(bundle, out, timeout, scenario_path, hold_awake=None):
    """Walk the scenario in the test build and report its verdict. A pass needs: the walk's own verdict pass; exactly
    one window and one web view created; one process start; no other process at any census, and every census taken;
    the build ending itself with status 0."""
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
              and ran['census_taken'] and ran['exit_code'] == 0 and not ran['timed_out'] and all(s.get('marker') == MARKER.decode() for s in stages))
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
        'heading_wait': heading_wait(stages),
        'most_windows': most_windows, 'created': created, 'app_pid': ran['app_pid'], 'held_awake_by': ran['held_awake_by'],
        'census_samples': ran['census_samples'], 'census': census_said(ran), 'census_failures': ran['census_failures'],
        'other_processes_seen': ran['other_processes_seen'],
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
                 f"process starts {ran['process_started_stages']}; exit {ran['exit_code']}; {census_said(ran)}")
    print('\n'.join(lines))
    return 0 if overall == 'pass' else 1


def same_file(path, other):
    try:
        a, b = os.stat(path), os.stat(other)
    except OSError:
        return False
    return (a.st_dev, a.st_ino) == (b.st_dev, b.st_ino)


def executable_of(pid):
    """The process's executable path as macOS gives it (proc_pidpath, as stray.py asks), or None when it cannot be
    asked (the process has gone, or this is not macOS): then the process is not the App's own Codex."""
    import ctypes
    try:
        proc = ctypes.CDLL('/usr/lib/libproc.dylib', use_errno=True)
    except OSError:
        return None
    buffer = ctypes.create_string_buffer(4096)
    if proc.proc_pidpath(ctypes.c_int(int(pid)), buffer, ctypes.c_uint32(len(buffer))) <= 0:
        return None
    return os.fsdecode(buffer.value)


def inventory(home, app_data, project):
    """Every name under the throwaway home, relative to it (names only; no file is opened), and those outside what
    the App and the system may write for this build: the App data folder, the project folder, the driver's own folder
    and the system's folders named for this bundle (its WebKit, Caches and HTTP storage, its preferences and saved
    window state)."""
    names, errors = [], []
    for root, dirs, files in os.walk(home, followlinks=False, onerror=lambda error: errors.append(f'{error.filename}: {error.strerror}')):
        for name in dirs + files:
            names.append(str((Path(root) / name).relative_to(home)))
    names.sort()
    lib = 'Library'
    allowed_roots = [str(Path(app_data).relative_to(home)), str(Path(project).relative_to(home)), 'scripted-driver']
    allowed_roots += [f'{lib}/{place}/{name}' for place in ('WebKit', 'Caches', 'HTTPStorages') for name in (IDENTIFIER, EXECUTABLE)]
    allowed_roots += [f'{lib}/Preferences/{IDENTIFIER}.plist', f'{lib}/Saved Application State/{IDENTIFIER}.savedState']
    def allowed(name):
        return any(name == root or name.startswith(root + '/') or root.startswith(name + '/') for root in allowed_roots)
    return {'names': names, 'outside': [name for name in names if not allowed(name)], 'allowed_roots': allowed_roots,
            'errors': errors}


UUID = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'


def judge_sheet(stage, sheet, values, answer):
    """The stand-in's record of desktop setup's sheet against the scenario's words: the title, the buttons, the answer,
    and the complete statement, line for line, equal to the scenario's statement with its values filled in. The two
    generated paths (the new settings folder and account directory) must each have the form the scenario gives, a
    fresh identity under the App data folder; the paths found are returned so that the inventory can bind them to
    what was saved."""
    detail = stage.get('detail') or {}
    statement = detail.get('statement') or ''
    fill = lambda text, given: re.sub(r'\{(\w+)\}', lambda m: given.get(m.group(1), m.group(0)), text)
    generated = {}
    for name, form in sheet['generated'].items():
        pattern = re.escape(fill(form, values)).replace(re.escape('<uuid>'), UUID)
        found = re.findall(f'(?m)(?<=: )({pattern})$', statement)
        generated[name] = found[0] if len(found) == 1 else None
    wanted = fill('\n'.join(sheet['statement']), {**values, **{k: v for k, v in generated.items() if v}})
    checks = [
        ('title', detail.get('title') == sheet['title'], detail.get('title')),
        ('buttons', detail.get('buttons') == sheet['buttons'], detail.get('buttons')),
        *[(f'generated path: {name}', path is not None, path) for name, path in generated.items()],
        ('the complete statement', statement == wanted, statement if statement != wanted else None),
        ('answer', detail.get('answer') == answer, detail.get('answer')),
    ]
    return [{'check': name, 'pass': ok, 'found': found} for name, ok, found in checks], generated


def setup(bundle, out, timeout, scenario_path, hold_awake=None):
    """Three launches in one throwaway home, as setup-complete.scenario.json says. A pass needs, for every launch: the
    walk's own verdict pass; exactly one window and one web view; one process start; no other process at any census
    (on the relaunch, apart from the bundle's own Codex, by file identity), and every census taken; the build ending
    itself with status 0; its stand-in records judged right; and its inventory as the scenario says. The App's native
    confirmation is not exercised: the test build's stand-in answers it."""
    bundle = bundle.resolve()
    if not (bundle / 'Contents/MacOS' / EXECUTABLE).is_file():
        print(f'refused: no {EXECUTABLE} in {bundle}', file=sys.stderr)
        return 2
    walked = json.loads(Path(scenario_path).read_text())
    run = out / 'setup-run'
    home = run / 'home'
    project = home / 'Projects/setup-scenario-project'
    project.mkdir(parents=True)
    app_data = home / 'Library/Application Support' / IDENTIFIER
    values = {'identifier': IDENTIFIER, 'home': str(home), 'project': str(project), 'app_data': str(app_data)}
    codex = bundle / CODEX
    common = {k: v for k, v in walked.items() if k not in ('launches', 'sheet', 'scenario', 'version')}
    launches, passed_all = [], True
    for spec in walked['launches']:
        part = {**common, **{k: spec[k] for k in ('steps', 'outcomes')}}
        allowed = (lambda pid: same_file(executable_of(pid) or '', codex)) if spec['children'] != 'none' else None
        ran = launch(bundle, run / spec['id'], timeout,
                     {'scenario': part, 'values': values, 'expected_heading': spec['expected_heading'],
                      'setup_answers': spec['setup_answers']}, hold_awake, home=home, allowed=allowed, frameworks_home=True)
        stages = ran['stages']
        finished = next((s for s in stages if s.get('stage') == 'scenario finished'), None)
        result = (finished or {}).get('detail', {}).get('result') or {}
        created = (finished or {}).get('detail', {}).get('created') or {}
        one = ((finished or {}).get('detail', {}).get('exactly_one_each') is True and created.get('windows_ever_created') == 1
               and created.get('webviews_ever_created') == 1 and (finished or {}).get('detail', {}).get('most_windows') == 1)
        sheets = [s for s in stages if s.get('stage') == 'setup confirmation stand-in']
        judged = [judge_sheet(s, walked['sheet'], values, answer) for s, answer in zip(sheets, spec['setup_answers'])]
        sheet_checks = [checks for checks, _ in judged]
        sheets_right = len(sheets) == len(spec['setup_answers']) and all(c['pass'] for checks in sheet_checks for c in checks)
        listed = inventory(home, app_data, project)
        want = spec['inventory']
        request = (app_data / 'desktop-startup/request.json').exists()
        homes = sorted(p.name for p in (app_data / 'account-homes').iterdir()) if (app_data / 'account-homes').is_dir() else []
        settings = sorted(p.name for p in (app_data / 'shared-settings').iterdir()) if (app_data / 'shared-settings').is_dir() else []
        inventory_checks = [{'check': 'saved request', 'pass': request == want['saved_request'], 'found': request},
                            {'check': 'account homes', 'pass': len(homes) == want['account_homes'], 'found': len(homes)},
                            {'check': 'settings folders', 'pass': len(settings) == want['settings_folders'], 'found': settings},
                            {'check': 'every name under the throwaway home was listed', 'pass': not listed['errors'],
                             'found': listed['errors']},
                            {'check': 'no name under the throwaway home outside the allowed places (allowed_roots: the App '
                                      'data folder, the project, the driver\'s folder and the system\'s folders named for '
                                      'this bundle)', 'pass': not listed['outside'], 'found': listed['outside']}]
        if want.get('settings_named_in_the_sheet'):
            named = judged[-1][1] if judged else {}
            saved = {'settings': [str(app_data / 'shared-settings' / s) for s in settings],
                     'account': [str(app_data / 'account-homes' / h) for h in homes]}
            inventory_checks.append({'check': 'the settings folder and account directory saved are the ones the sheet named',
                                     'pass': all(saved[k] == [named.get(k)] for k in saved), 'found': saved})
        if 'sign_in_file_absent' in want:
            present = [h for h in homes if (app_data / 'account-homes' / h / want['sign_in_file_absent']).exists()]
            inventory_checks.append({'check': f"no {want['sign_in_file_absent']} in the account home (by name, never opened)",
                                     'pass': not present, 'found': present})
        visible = [s for s in (result.get('steps') or []) if 'app_state' not in s]
        state = [s for s in (result.get('steps') or []) if 'app_state' in s]
        verdict = result.get('verdict') if finished else None
        passed = (verdict == 'pass' and one and ran['process_started_stages'] == 1 and not ran['other_processes_seen']
                  and ran['census_taken'] and ran['exit_code'] == 0 and not ran['timed_out'] and sheets_right
                  and all(c['pass'] for c in inventory_checks) and all(s.get('marker') == MARKER.decode() for s in stages))
        passed_all = passed_all and passed
        launches.append({
            'id': spec['id'], 'says': spec['says'], 'verdict': 'pass' if passed else 'not passed', 'walk_verdict': verdict,
            'stopped': result.get('stopped'), 'outcomes': result.get('outcomes'),
            'visible_elements': visible,
            'app_state_read': {'standing': "the App's state as the page's own status read gave it; no person-visible element "
                                           'was judged for these facts', 'steps': state},
            'stand_in_sheets': {'standing': 'the test build\'s stand-in for desktop setup\'s native confirmation; the native '
                                            'confirmation itself was not exercised', 'records': [s.get('detail') for s in sheets],
                                'checks': sheet_checks},
            'inventory': {'checks': inventory_checks, 'names': listed['names'], 'allowed_roots': listed['allowed_roots'],
                          'account_homes': homes},
            'heading_wait': heading_wait(stages), 'created': created, 'exit_code': ran['exit_code'], 'timed_out': ran['timed_out'],
            'census_samples': ran['census_samples'], 'census': census_said(ran), 'census_failures': ran['census_failures'],
            'other_processes_seen': ran['other_processes_seen'], 'allowed_codex_seen': ran['allowed_codex_seen'],
            'codex_network_connections': ran['codex_network_connections'], 'left_in_group_and_ended': ran['left_in_group_and_ended'],
            'process_started_stages': ran['process_started_stages'], 'seconds': ran['seconds'],
            'census_at_start': result.get('census_at_start'), 'census_at_end': result.get('census_at_end'),
            'app_stderr_tail': ran['app_stderr_tail']})
        if not passed:
            break  # a later launch rests on this one
    overall = 'pass' if passed_all and len(launches) == len(walked['launches']) else 'not passed'
    report = {
        'marker': MARKER.decode(), 'scenario': walked['scenario'], 'version': walked['version'], 'verdict': overall,
        'bundle': str(bundle), 'values': values, 'launches': launches,
        'first_launch_after_setup': {
            'standing': 'a fact for another lane, not a judgment: what a person sees on the first launch after setup '
                        'without pressing anything, and how many presses it takes to learn which project the App holds '
                        'and whether they are signed in, as read in the App\'s source for this revision',
            'seen_without_pressing': 'the workspace heading "Chirality" and its connection line ("Codex is connected", '
                                     '"Codex is starting…" or "Codex could not stay connected", with guidance)',
            'project': 'shown as "Project folder: …" under "Project" in "Run a workflow", the task view shown first: no '
                       'press, unless that guide is withheld',
            'signed_in': 'shown only after "Check account status", inside "Connection and access" in the "Settings & tools" '
                         'view: the view\'s link, then the disclosure when Codex is ready (it is open otherwise), then the '
                         'button: two or three presses',
            'launch_state': '"Current launch: saved-request. …" is in "Setup details and source status", inside "Desktop '
                            'setup" (closed after setup), in the "Settings & tools" view: three presses'},
        'limits': LIMITS + [
            'The App\'s native confirmation for desktop setup is not exercised by this scenario: the test build\'s stand-in '
            'records the sheet\'s words and answers it. The real sheet is exercised by the operator rehearsal and by the '
            'owner.',
            'The relaunch\'s project, launch state and Codex state are the App\'s state as the page\'s own status read gave '
            'it; no person-visible element was judged for those facts. Sign-in is judged by the sign-in file\'s name being '
            'absent from the account home; nothing there is opened.',
            'On the relaunch the App starts the copy of Codex it ships, signed out, with nothing typed to it and no turn '
            'sent, so it makes no model request. Whether it makes a start-up request of its own on the runner, which has '
            'outbound network, is not established; the network connections it held at each census are recorded as a fact.',
            'The inventory lists names under the throwaway home only; what the system writes elsewhere on the runner is '
            'not seen.',
            'Typing sets the field\'s value as a script does and fires the page\'s input event; it is not input from the '
            'system.'],
    }
    (out / 'setup-report.json').write_text(json.dumps(report, indent=1) + '\n')
    print(f"{walked['scenario']} (version {walked['version']}): {overall.upper()}")
    print('  The App\'s native confirmation was not exercised: the test build\'s stand-in answered it. Development '
          'evidence only; it satisfies nothing in release criteria 1 and 2.')
    for entry in launches:
        print(f"  {entry['id']}: {entry['verdict']} (walk {entry['walk_verdict']}; exit {entry['exit_code']}; "
              f"other processes {len(entry['other_processes_seen'])}; codex seen {len(entry['allowed_codex_seen'])}; {entry['census']})")
        if entry['stopped']:
            print(f"    {entry['stopped']}")
        for c in [c for checks in entry['stand_in_sheets']['checks'] for c in checks] + entry['inventory']['checks']:
            if not c['pass']:
                print(f"    {c['check']}: found {json.dumps(c['found'])}")
    return 0 if overall == 'pass' else 1


def release_free(out):
    """Marker present in the test build, absent from a release-features build of the same revision, and the driver
    refused with the release feature. Every part must run and say so; a part that did not run is a failure."""
    results = {}
    tests = sorted((out / 'target/debug/bundle/macos').glob('*.app'))
    test_binary = tests[0] / 'Contents/MacOS' / EXECUTABLE if len(tests) == 1 else None
    test_bytes = test_binary.read_bytes() if test_binary and test_binary.is_file() else b''
    results['marker in the test build'] = MARKER in test_bytes
    results['setup stand-in in the test build'] = STAND_IN_MARKER in test_bytes
    release_target = out / 'release-features-target'
    cargo = ['cargo', 'build', '--locked', '--manifest-path', str(APP / 'src-tauri/Cargo.toml'),
             '--features', 'custom-protocol,distribution-successor']
    clean = {k: v for k, v in os.environ.items() if k != 'CHIRALITY_SCRIPTED_DRIVER_BUILD'}
    built = subprocess.run(cargo, env={**clean, 'CARGO_TARGET_DIR': str(release_target)})
    release_binary = release_target / 'debug' / EXECUTABLE
    results['release-features build made'] = built.returncode == 0 and release_binary.is_file()
    release_bytes = release_binary.read_bytes() if results['release-features build made'] else None
    results['marker absent from the release-features build'] = release_bytes is not None and MARKER not in release_bytes
    results['setup stand-in absent from the release-features build'] = (release_bytes is not None
                                                                        and STAND_IN_MARKER not in release_bytes)
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
    return 0 if len(results) == 6 and all(results.values()) else 1


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
    st = sub.add_parser('setup')
    st.add_argument('--bundle', type=Path, required=True)
    st.add_argument('--out', type=Path, required=True)
    st.add_argument('--timeout', type=int, default=300)
    st.add_argument('--scenario', type=Path, default=SETUP_SCENARIO)
    sub.add_parser('release-free').add_argument('--out', type=Path, required=True)
    args = parser.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)
    if args.command == 'build':
        return build(args.out.resolve())
    if args.command == 'run':
        return run(args.bundle, args.out.resolve(), args.timeout)
    if args.command == 'scenario':
        return scenario(args.bundle, args.out.resolve(), args.timeout, args.scenario)
    if args.command == 'setup':
        return setup(args.bundle, args.out.resolve(), args.timeout, args.scenario)
    return release_free(args.out.resolve())


if __name__ == '__main__':
    sys.exit(main())
