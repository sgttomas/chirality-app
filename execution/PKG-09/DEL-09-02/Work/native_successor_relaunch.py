"""Phase B only: native saved-request relaunch, diagnosis, Stop and Quit.

Never signal supplier numbers or inherit A's emergency App termination.
Unresolved process settlement retains the original App reservation, slot and observer.
A held observer is an overrun/unknown result, not a bounded settlement claim.
"""
import argparse
import ctypes
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile
import threading
import time
from datetime import datetime, timezone

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve()
spec = importlib.util.spec_from_file_location('successor_A_admission', HERE.with_name('native_successor_setup.py'))
setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)
base = setup.load_base()
require = setup.require
write_once = setup.write_once
T3 = setup.T3
ACTOR = base.ACTOR
LIMIT = 'Original owned groups only; detached/escaped helpers unobserved. Process census is corroboration, never custody.'


def now():
    return datetime.now(timezone.utc).isoformat()


def check_observation_capabilities():
    require(sys.platform == 'darwin' and sys.version_info >= (3, 13)
            and all(hasattr(os, name) for name in ('waitid', 'P_PID', 'WEXITED', 'WNOHANG', 'WNOWAIT')),
            'macOS Python 3.13+ nonreaping observation unavailable')
    library = ctypes.CDLL('/System/Library/Frameworks/ApplicationServices.framework/ApplicationServices')
    trusted = library.AXIsProcessTrusted
    trusted.restype, trusted.argtypes = ctypes.c_bool, []
    require(trusted(), 'Accessibility unavailable before launch; no permission prompt or fallback')


def dependencies():
    return {**setup.dependency_digests(), str(setup.HERE): setup.digest(setup.HERE), str(HERE): setup.digest(HERE)}


def policy(value):
    supplier = str(Path(value['bundle']) / 'Contents/Resources/codex/bin/codex')
    return ('(version 1)\n(allow default)\n(deny network*)\n'
            '(deny file-read* (subpath ' + json.dumps(str(Path.home() / '.codex')) + '))\n'
            '(deny file-write* (subpath ' + json.dumps(str(Path.home() / '.codex')) + '))\n'
            '(allow process-fork)\n(deny process-exec)\n'
            '(allow process-exec (literal ' + json.dumps(value['executable']) + ') '
            '(literal ' + json.dumps(supplier) + '))\n')


def saved_input(a_root):
    setup.plain(a_root, directory=True)
    require(a_root.is_relative_to(T3 / 'scratch'), 'A attempt outside task scratch')
    paths = [a_root / name for name in ('admission.json', 'result.json', 'saved-bindings.json', 'namespace-after.json')]
    for path in paths:
        setup.plain(path)
    admitted, result, bindings, after = [json.loads(path.read_text()) for path in paths]
    context = setup.Context.restore(admitted['context'])
    value = context.inputs()
    require(context.namespaces(require_absent=False) == after, 'namespace differs from preserved A settlement')
    require(result['candidate'] == value['candidate_key'] and result['normal_setup_save_quit'] is True
            and result['saved'] is True and result['phase'] == 'A only'
            and result['exit_code'] == 0 and result['forced'] is False and not result['guard_reason']
            and not result['logging_errors'] and result['error'] is None, 'A did not settle successfully')
    app_data = Path(value['expected_app_data'])
    account = Path(bindings['account'])
    request = app_data / 'desktop-startup/request.json'
    require(bindings['request_path'] == str(request) and bindings['expected_inputs'] == value['native_input_paths'],
            'A binding paths differ')
    setup.plain(account, directory=True)
    require(account.parent == app_data / 'account-homes', 'account not in selected App data')
    raw, record = base.validate_request(request, account, value)
    require(base.sha(raw) == bindings['request_sha256'] and record == bindings['request'], 'saved A request changed')
    # A-only namespace: no existing recovery store or credential contents are
    # read. An extra account file, home or runtime directory refuses admission.
    require(set(p.name for p in app_data.iterdir()) == {'account-homes', 'desktop-startup'},
            'App data has unadmitted recovery/other state')
    require(list(account.parent.iterdir()) == [account], 'additional account home')
    require(set(p.name for p in request.parent.iterdir()) == {'request.json'}, 'extra startup state')
    require(set(p.name for p in account.iterdir()) == {'config.toml', 'AGENTS.md', 'skills'},
            'account has unadmitted recovery/credential/other state')
    for name, key in [('config.toml', 'shared_config'), ('AGENTS.md', 'shared_agents'), ('skills', 'shared_skills')]:
        link = account / name
        require(link.is_symlink() and link.resolve() == Path(value['native_input_paths'][key]), 'shared link changed')
    value['expected_generation_home'] = 'app-home:' + hashlib.sha256(os.fsencode(account)).hexdigest()
    return context, value, bindings, {str(path): setup.digest(path) for path in paths}


def prepare(a_root):
    context, value, bindings, a_files = saved_input(a_root)
    root = Path(tempfile.mkdtemp(prefix='app-successor-native-B-', dir=T3 / 'scratch')).resolve()
    for name in ('codex-home', 'tmp'):
        (root / name).mkdir(mode=0o700)
    value['environment']['CODEX_HOME'] = str(root / 'codex-home')
    value['environment']['TMPDIR'] = str(root / 'tmp')
    (root / 'phase-B.sb').write_text(policy(value))
    (root / 'controller.py.txt').write_bytes(HERE.read_bytes())
    write_once(root / 'admission.json', {'a_root': str(a_root), 'a_files': a_files,
        'context': context.descriptor(), 'inputs': value, 'bindings': bindings,
        'namespaces': context.namespaces(require_absent=False), 'dependencies': dependencies(),
        'policy_sha256': setup.digest(root / 'phase-B.sb'), 'prepared_at': now(), 'limits': LIMIT})
    print(root)
    return root


def generation(value):
    require(isinstance(value, dict) and set(value) == {'appSession', 'home', 'spawnCounter'}
            and all(isinstance(value[k], str) and value[k] for k in ('appSession', 'home'))
            and type(value['spawnCounter']) is int and value['spawnCounter'] > 0, 'full generation unavailable')
    return value


def decode_diagnostics(strings, protocol=True):
    """Parse only observed rendered text and the actual two JSON sections.

    AX may split inline text across nodes. Adjacent duplicate AX values are
    collapsed, but no state/generation is inferred from lifecycle events.
    """
    lifecycle, envelopes, header = [], [], []
    for string in strings:
        if not isinstance(string, str) or not string:
            continue
        try:
            value = json.loads(string)
        except (ValueError, TypeError):
            value = None
        if isinstance(value, dict) and set(value) == {'lifecycle', 'clientRequests'}:
            if value not in lifecycle:
                lifecycle.append(value)
            continue
        if isinstance(value, list) and value and all(isinstance(row, dict) for row in value) and any('frame' in row for row in value):
            if value not in envelopes:
                envelopes.append(value)
            continue
        if not header or header[-1] != string:
            header.append(string)
    text = '\n'.join(header)
    matches = list(re.finditer(r'State:\s*(\S+)\s*·\s*generation\s*(\{[^\n]*?\})\s*·\s*version\s*([^·]+)', text))
    require(len(matches) == 1, 'rendered state/generation header unavailable or ambiguous')
    match = matches[0]
    gen = generation(json.loads(match.group(2)))
    require(len(lifecycle) == 1, 'owned lifecycle section unavailable or ambiguous')
    require(not protocol or len(envelopes) == 1, 'owned envelope section unavailable or ambiguous')
    require(isinstance(lifecycle[0]['lifecycle'], list), 'lifecycle array unavailable')
    return {'rendered_state': match.group(1), 'generation': gen, 'rendered_version': match.group(3).strip(),
            **lifecycle[0], 'envelopes': envelopes[0] if len(envelopes) == 1 else None}


def check_requests(observed, gen):
    requests = observed['clientRequests']
    require(isinstance(requests, list) and isinstance(observed['envelopes'], list), 'protocol observations unavailable')
    require(requests and all(isinstance(r, dict) and r.get('method') == 'initialize'
                            and r.get('generation') == gen for r in requests),
            'unexpected/prohibited or foreign-generation request')
    require(len(requests) == 1, 'initialize request count differs')
    request = requests[0]
    require(type(request.get('requestIdentity')) in (str, int) and request['requestIdentity'] != '', 'initialize request identity unavailable')
    require(request.get('writeResult') == 'written' and request.get('outcome') == 'response-observed-result',
            'initialize write/result not observed')
    replies = [r for r in observed['envelopes'] if r.get('generation') == gen
               and isinstance(r.get('frame'), dict) and type(r['frame'].get('id')) is type(request.get('requestIdentity'))
               and r['frame'].get('id') == request.get('requestIdentity')
               and 'result' in r['frame'] and 'error' not in r['frame']
               and r.get('position') == request.get('responseReceiptPosition')
               and type(r.get('position')) is int]
    require(len(replies) == 1, 'correlated initialize response unavailable or ambiguous')
    return replies[0]['frame']['result']


def source_gate(observed, value, expected=None):
    """Cleanup authority comes from the held App's actual native source, not a pass.

    LT-06 is emitted only after the checked App spawns its admitted bundled
    executable and binds the generation. Before LT-09 that construction, the
    exact two-executable sandbox and saved account binding identify the source.
    If LT-09 exposes a launcher, it must corroborate that same path.
    """
    gen = generation(observed['generation'])
    require(gen['home'] == value['expected_generation_home'], 'generation does not bind saved A account')
    require(expected is None or gen == expected, 'cleanup source generation changed')
    spawned = [r for r in observed['lifecycle'] if r.get('transitionId') == 'LT-06'
               and r.get('generation') == gen and r.get('toState') == 'handshaking']
    require(len(spawned) == 1, 'actual same-generation spawn observation unavailable')
    supplier = str(Path(value['bundle']) / 'Contents/Resources/codex/bin/codex')
    for row in observed['lifecycle']:
        if row.get('transitionId') == 'LT-09' and row.get('generation') == gen:
            require(row.get('versionIdentity', {}).get('configurationIdentity', {}).get('launcher') == supplier,
                    'cleanup executable source differs')
    require(observed['rendered_state'] in ('ready', 'handshaking', 'halted-after-repeated-failure',
            'exited-unexpectedly', 'stopping', 'stopped'), 'cleanup source state is unavailable')
    return gen


def ready_gate(observed, value):
    gen = source_gate(observed, value)
    require(gen['home'] == value['expected_generation_home'], 'generation does not bind saved A account')
    require(observed['rendered_state'] == 'ready' and observed['rendered_version'] == 'codex-cli 0.160.0',
            'native ready/version not observed')
    rows = [r for r in observed['lifecycle'] if r.get('transitionId') == 'LT-09' and r.get('generation') == gen]
    require(len(rows) == 1 and rows[0].get('toState') == 'ready', 'same-generation LT-09 unavailable')
    row = rows[0]
    vi = row.get('versionIdentity', {})
    require(row.get('supplierStanding') == 'unverified-development'
            and vi.get('observedVersionLabel') == 'codex-cli 0.160.0', 'development source standing differs')
    supplier = Path(value['bundle']) / 'Contents/Resources/codex/bin/codex'
    require(vi.get('configurationIdentity', {}).get('launcher') == str(supplier), 'actual supplier launcher differs')
    require(any(r.get('path') == 'bin/codex' and r.get('identity') == {'algorithm': 'sha-256', 'value': setup.digest(supplier)}
                for r in vi.get('distributionContentIdentity', [])), 'supplier content identity differs')
    reply = check_requests(observed, gen)
    require(isinstance(reply, dict) and isinstance(reply.get('userAgent'), str) and reply['userAgent'],
            'initialize identity result unavailable')
    require(reply == vi.get('handshakeReportedIdentity'), 'initialize/LT-09 identity differs')
    return gen


def settlement_gate(observed, gen):
    require(observed['generation'] == gen and observed['rendered_state'] == 'stopped', 'Stop generation/state differs')
    rows = [r for r in observed['lifecycle'] if r.get('transitionId') == 'LT-23' and r.get('generation') == gen]
    require(len(rows) == 1 and rows[0].get('toState') == 'stopped', 'same-generation LT-23 unavailable')
    row = rows[0]
    exit_facts, descendants = row.get('exitFacts', {}), row.get('descendants', {})
    code, ended_signal = exit_facts.get('exitCode'), exit_facts.get('signal')
    require((type(code) is int and 0 <= code <= 255)
            or (type(ended_signal) is int and ended_signal > 0)
            or (isinstance(ended_signal, str) and ended_signal.isdigit() and int(ended_signal) > 0),
            'supplier leader exit unknown')
    require(descendants.get('checked') is True and type(descendants.get('surviving')) is int
            and descendants['surviving'] == 0, 'owned supplier group settlement unknown/nonempty')
    return row


class AppReservation:
    """Strong reference to the actual created child; no numeric ingress/signals."""
    def __init__(self, child):
        self.child = child
        self.reaped = False
        self.lost = None

    def observe(self):
        require(not self.reaped and self.lost is None, 'original App reservation unavailable')
        try:
            result = os.waitid(os.P_PID, self.child.pid, os.WEXITED | os.WNOHANG | os.WNOWAIT)
        except ChildProcessError as error:
            self.lost = str(error)
            raise RuntimeError('original App reservation lost; no numeric action') from error
        if result is None or result.si_pid == 0:
            return None
        require(result.si_pid == self.child.pid, 'foreign exit observation')
        return {'code': result.si_code, 'status': result.si_status}

    def reap(self, supplier_settled, quit_requested):
        require(supplier_settled and quit_requested, 'no settlement/quit permission to reap App')
        require(self.observe() is not None, 'original App has not exited')
        code = self.child.wait()  # Only after WNOWAIT exit + native Stop/Quit gates.
        self.reaped = True
        return code


class Run:
    dialog = base.Supervisor.dialog  # This method only traverses own AX; no poll/kill.

    def __init__(self, root, value, resource_end):
        self.root, self.value, self.resource_end = root, value, resource_end
        self.work_end = min(time.monotonic() + 180, resource_end - 45)
        self.cleanup_end = resource_end
        self.cleanup = False
        self.reservation = None
        self.ax = None
        self.reason = None
        self.log_errors = []
        self.stop = threading.Event()
        self.thread = None
        self.last_sample = 0.0
        self.generation = None
        self.stop_requested = False
        self.stop_confirmed = False
        self.quit_confirmed = False
        self.supplier_settled = False
        self.quit_requested = False
        self.observed_processes = []
        self.last_diagnostics = None
        self.stop_observation = None
        self.log_lock = threading.Lock()

    def note_log_error(self, error):
        text = str(error)[:512]
        if text not in self.log_errors and len(self.log_errors) < 20:
            self.log_errors.append(text)

    def log(self, event, **facts):
        try:
            with self.log_lock:
                with (self.root / 'actions.jsonl').open('a') as stream:
                    stream.write(json.dumps({'at': now(), 'event': event, **facts}) + '\n')
        except BaseException as error:
            if not self.cleanup:
                raise
            self.note_log_error(error)
            self.reason = self.reason or 'evidence logging failed'

    def record(self, name, value):
        try:
            write_once(self.root / name, value)
        except BaseException as error:
            self.note_log_error(error)
            self.reason = self.reason or 'evidence recording failed'
            if not self.cleanup:
                raise

    def safe_log(self, event, **facts):
        try:
            self.log(event, **facts)
        except BaseException as error:
            self.note_log_error(error)
            self.reason = self.reason or 'evidence logging failed'

    def sample(self, admission=False):
        require(not (T3 / 'guard/exclusive.pending').exists(), 'exclusive pending')
        subprocess.run(['/usr/bin/pgrep', '-f', str(T3 / 'guard/memguard.sh')], stdout=subprocess.DEVNULL, check=True, timeout=2)
        output = subprocess.check_output(['/bin/ps', '-axo', 'pid=,ppid=,rss=,command='], text=True, timeout=2)
        rows = []
        for line in output.splitlines():
            fields = line.strip().split(None, 3)
            if len(fields) == 4:
                rows.append((int(fields[0]), int(fields[1]), int(fields[2]), fields[3]))
        own = {os.getpid()}
        if self.reservation is not None:
            own.add(self.reservation.child.pid)
        while True:
            before = len(own)
            own.update(pid for pid, parent, _, _ in rows if parent in own)
            if len(own) == before:
                break
        supplier_root = str(Path(self.value['bundle']) / 'Contents/Resources/codex/')
        found = [{'pid': pid, 'parent': parent, 'under_controller_ancestry': pid in own}
                 for pid, parent, _, command in rows if command.startswith(supplier_root)
                 or command == self.value['executable'] or command.startswith(self.value['executable'] + ' ')]
        self.observed_processes = found
        if admission:
            require(not found, 'existing successor App/supplier observation; no overlapping launch')
        total = sum(rss for pid, _, rss, command in rows if pid in own or str(T3) + '/' in command)
        free = int(subprocess.check_output(['/usr/sbin/sysctl', '-n', 'kern.memorystatus_level'], text=True, timeout=2))
        require(total < (52 if admission else 64) * 1024 * 1024 and free >= (30 if admission else 22), 'resource cap/floor')
        self.last_sample = time.monotonic()

    def monitor(self):
        while not self.stop.wait(0.5):
            try:
                self.sample()
                if time.monotonic() >= self.work_end and not self.cleanup:
                    self.reason = self.reason or 'work deadline'
            except BaseException as error:
                self.reason = self.reason or str(error)
                # Keep the observer/guard alive, including during held overruns.

    def alive(self):
        require(self.reservation is not None and self.reservation.observe() is None, 'original App ended before expected native settlement')
        require(time.monotonic() < (self.cleanup_end if self.cleanup else self.work_end), 'native operation deadline')
        if not self.cleanup:
            require(self.reason is None and not self.log_errors, 'guard/evidence failure: ' + str(self.reason))
            require(self.thread is not None and self.thread.is_alive() and time.monotonic() - self.last_sample < 8, 'guard heartbeat unavailable')

    def wait_for(self, predicate, seconds, reason):
        end = min(time.monotonic() + seconds, self.cleanup_end if self.cleanup else self.work_end)
        while time.monotonic() < end:
            self.alive()
            value = predicate()
            if value:
                return value
            time.sleep(0.1)
        raise RuntimeError(reason)

    def open_disclosure(self, title, prefix=False):
        def find():
            matches = [e for e, p, _ in self.ax.walk(self.ax.main()) if p['AXRole'] == 'AXDisclosureTriangle'
                       and isinstance(p['AXTitle'], str) and (p['AXTitle'].startswith(title) if prefix else p['AXTitle'] == title)]
            require(len(matches) <= 1, 'ambiguous disclosure: ' + title)
            return matches[0] if matches else None
        element = self.wait_for(find, 5, 'disclosure unavailable: ' + title)
        value = self.ax.attr(element, 'AXValue')
        require(value in (True, False, 0, 1), 'disclosure state unavailable: ' + title)
        if value not in (True, 1):
            self.ax.press(element)
            self.wait_for(lambda: self.ax.attr(element, 'AXValue') in (True, 1), 5,
                          'disclosure did not open: ' + title)

    def diagnostics(self):
        rows = self.ax.walk(self.ax.main())
        strings = [p['AXValue'] if isinstance(p.get('AXValue'), str) else p.get('AXTitle') for _, p, _ in rows
                   if p['AXRole'] in ('AXStaticText', 'AXTextArea', 'AXTextField')]
        self.last_diagnostics = {'at': now(), 'strings': strings}
        return decode_diagnostics(strings, protocol=False)

    def observe_ready(self, qualification=True):
        self.wait_for(lambda: self.ax.windows(), 10, 'main window unavailable')
        self.wait_for(lambda: any(p['AXRole'] == 'AXDisclosureTriangle' and str(p['AXTitle']).startswith('Host diagnostics')
                                 for _, p, _ in self.ax.walk(self.ax.main())), 20, 'diagnostics control unavailable')
        self.open_disclosure('Host diagnostics', prefix=True)
        self.open_disclosure('Lifecycle events (', prefix=True)
        self.open_disclosure('Raw native envelopes (including unknown fields)')
        last_error = None
        end = min(time.monotonic() + 45, self.cleanup_end if self.cleanup else self.work_end)
        while time.monotonic() < end:
            self.alive()
            try:
                observed = self.diagnostics()
                gen = ready_gate(observed, self.value) if qualification else source_gate(observed, self.value)
                self.generation = gen
                self.record('ready-observation.json' if qualification else 'cleanup-source-observation.json', observed)
                if not self.cleanup:
                    self.ax.snapshot(self.root / 'ready-AX.json')
                return gen
            except (RuntimeError, ValueError) as error:
                last_error = str(error)
            time.sleep(0.1)
        raise RuntimeError('native ready gate unavailable: ' + str(last_error))

    def stop_and_quit(self, gen):
        self.cleanup = True
        observed = self.diagnostics()
        source_gate(observed, self.value, gen)
        require(self.generation is None or self.generation == gen, 'captured cleanup generation changed')
        self.generation = gen
        if observed['rendered_state'] == 'stopped':
            row = settlement_gate(observed, gen)
            self.supplier_settled = True
            self.stop_observation = observed
            self.record('stop-observation.json', observed)
            self.safe_log('owned_group_settled', generation=gen, actual=row, limits=LIMIT)
        elif not self.stop_confirmed and observed['rendered_state'] != 'stopping':
            if not self.stop_requested:
                self.open_disclosure('Connection and access', prefix=True)
                self.stop_requested = True  # An ambiguous AX delivery is never silently repeated.
                self.ax.press(self.ax.find('AXButton', 'Stop Codex…'))
            rows, button = self.wait_for(lambda: self.dialog('Stop Codex', 'Stop Codex'), 8, 'Stop confirmation unavailable')
            statement = self.ax.text([(e, p, w) for e, p, w in rows if not w])
            require('Home: account' in statement and 'App session ' + gen['appSession'] in statement
                    and re.search(r'Codex process start ' + re.escape(str(gen['spawnCounter'])) + r'(?=\s*·|\s*$)', statement), 'Stop confirmation source differs')
            self.record('stop-confirmation.json', {'generation': gen, 'statement': statement, 'actor': ACTOR})
            self.stop_confirmed = True
            self.ax.press(button)
            self.safe_log('native_stop_confirmed', generation=gen, actor=ACTOR)
        end = min(time.monotonic() + 25, self.cleanup_end)
        last_error = None
        while not self.supplier_settled and time.monotonic() < end:
            self.alive()
            try:
                observed = self.diagnostics()
                source_gate(observed, self.value, gen)
                row = settlement_gate(observed, gen)
                self.stop_observation = observed
                self.record('stop-observation.json', observed)
                self.safe_log('owned_group_settled', generation=gen, actual=row, limits=LIMIT)
                self.supplier_settled = True
            except (RuntimeError, ValueError) as error:
                last_error = str(error)
            if not self.supplier_settled:
                time.sleep(0.1)
        require(self.supplier_settled, 'native supplier settlement unavailable: ' + str(last_error))
        if not self.quit_requested:
            self.quit_requested = True
            self.ax.quit_ui()
            self.safe_log('native_quit_requested', actor=ACTOR)
        return self.wait_for_quit_exit()

    def wait_for_quit_exit(self):
        require(self.supplier_settled and self.quit_requested, 'Quit exit lacks settlement gates')
        while time.monotonic() < self.cleanup_end:
            if self.reservation.observe() is not None:
                return self.reservation.reap(True, True)
            if not self.quit_confirmed:
                try:
                    self.alive()
                    question = self.dialog('Quit Chirality', 'Quit')
                    if question:
                        rows, button = question
                        self.record('quit-confirmation.json', {'statement': self.ax.text(rows), 'actor': ACTOR})
                        self.quit_confirmed = True
                        self.ax.press(button)
                except BaseException:
                    # The App may exit during any AX read after native Quit.
                    # Only this already-settled, Quit-requested path accepts it.
                    if self.reservation.observe() is not None:
                        return self.reservation.reap(True, True)
                    raise
            time.sleep(0.1)
        raise RuntimeError('native Quit did not settle by deadline')

    def settlement_facts(self):
        if self.stop_observation is None:
            return {'supplier_exit_facts': None, 'supplier_cleanup_limits': None}
        row = settlement_gate(self.stop_observation, self.generation)
        envelopes = self.stop_observation.get('envelopes')
        return {'supplier_exit_facts': row['exitFacts'], 'supplier_descendants': row['descendants'],
                'supplier_cleanup_limits': [r for r in envelopes if r.get('class') == 'process-cleanup-unavailable'
                    and r.get('generation') == self.generation] if isinstance(envelopes, list) else None}

    def cleanup_attempt(self):
        self.cleanup = True
        require(time.monotonic() < self.cleanup_end, 'reserved native cleanup deadline expired')
        if self.supplier_settled and self.quit_requested:
            return self.wait_for_quit_exit()
        require(self.reservation.observe() is None, 'App exited before required cleanup proof')
        if self.generation is None:
            self.generation = self.observe_ready(qualification=False)
        return self.stop_and_quit(self.generation)

    def report(self, value):
        try:
            print(json.dumps(value), flush=True)
        except BaseException as error:
            # Losing the tool/stdout consumer is not permission to release
            # the still-owned App or stop its guard/observer.
            self.note_log_error(error)

    def held_status(self, error):
        try:
            app = self.reservation.observe()
        except BaseException as observed_error:
            app = {'unknown': str(observed_error)}
        return {'candidate': self.value['candidate_key'], 'phase': 'B', 'state': 'held-unknown',
                'error': error, 'app_exit_observation': app, 'original_app_reaped': False,
                'supplier_settled_observed': self.supplier_settled, 'quit_requested': self.quit_requested,
                'generation': self.generation, 'recovery_limit': 'Permanent AX/parser loss cannot be repaired inside this frozen controller; retain supervision and report the exact missing observation. No numeric escalation or automatic duplicate UI action.', 'recovery_control': 'write retry-native-cleanup.json with {action:retry-native-cleanup,candidate:<this candidate>}; same source is reobserved, no numeric inputs or repeated UI actions',
                'guard_reason': self.reason, 'logging_errors': self.log_errors,
                'observed_executable_processes': self.observed_processes,
                'overrun': time.monotonic() >= self.resource_end, 'at': now(), 'limits': LIMIT}

    def hold(self, error):
        status = self.held_status(error)
        try:
            write_once(self.root / 'held-result.json', status)
        except BaseException as problem:
            self.note_log_error(problem)
        self.report(status)
        handled_retry = False
        while True:
            retry = self.root / 'retry-native-cleanup.json'
            if not handled_retry and os.path.lexists(retry):
                try:
                    setup.plain(retry)
                    require(retry.stat().st_size <= 4096, 'cleanup request too large')
                    request = json.loads(retry.read_text())
                    require(request == {'action': 'retry-native-cleanup', 'candidate': self.value['candidate_key']}, 'invalid explicit cleanup request')
                    handled_retry = True
                    self.cleanup_end = time.monotonic() + 45
                    self.safe_log('explicit_cleanup_retry', request=request, overrun=time.monotonic() >= self.resource_end)
                    code = self.cleanup_attempt()
                    self.stop.set()
                    if self.thread is not None:
                        self.thread.join(timeout=8)
                    result = {'state': 'settled-after-held-failure', 'success': False, 'original_app_reaped': True,
                              'exit_code': code, 'original_error': error, **self.settlement_facts(), 'limits': LIMIT}
                    self.record('recovery-result.json', result)
                    self.report(result)
                    return 1
                except BaseException as recovery_error:
                    self.safe_log('explicit_cleanup_unavailable', error=str(recovery_error))
            status = self.held_status(error)
            try:
                with (self.root / 'held-heartbeat.jsonl').open('a') as stream:
                    stream.write(json.dumps(status) + '\n')
            except BaseException as problem:
                self.note_log_error(problem)
            self.report(status)
            time.sleep(2)


def execute(root, window_end):
    setup.plain(root, directory=True)
    require(root.is_relative_to(T3 / 'scratch'), 'B attempt outside task scratch')
    require(not any(os.path.lexists(root / name) for name in ('execution-started.json', 'actions.jsonl', 'result.json', 'held-result.json')),
            'B attempt already used; preserve evidence')
    admitted = json.loads((root / 'admission.json').read_text())
    require(admitted['dependencies'] == dependencies(), 'controller dependency changed')
    context, value, bindings, a_files = saved_input(Path(admitted['a_root']))
    require(context.descriptor() == admitted['context'] and bindings == admitted['bindings']
            and a_files == admitted['a_files'], 'A admission/bindings changed')
    require(context.namespaces(require_absent=False) == admitted['namespaces'], 'saved namespace changed since B preparation')
    value['environment']['CODEX_HOME'] = str(root / 'codex-home')
    value['environment']['TMPDIR'] = str(root / 'tmp')
    require(value == admitted['inputs'] and (root / 'phase-B.sb').read_text() == policy(value)
            and setup.digest(root / 'phase-B.sb') == admitted['policy_sha256'], 'B launch inputs/policy changed')
    for name in ('codex-home', 'tmp'):
        setup.plain(root / name, directory=True)
        require(not list((root / name).iterdir()), 'fallback/tmp not fresh')
    require(90 < window_end - time.time() <= 300, 'invalid B interval')
    parent = subprocess.check_output(['/bin/ps', '-p', str(os.getppid()), '-o', 'command='], text=True, timeout=2)
    require(str(T3 / 'tools/t3_slot_run.sh') in parent, 'slot wrapper missing')
    checked = subprocess.run([sys.executable, '-B', str(setup.REPO / 'app/examination/candidate_identity/identify.py'), 'check',
                              '--record', str(context.record_path), '--app', value['bundle']],
                             env={'HOME': str(Path.home()), 'PATH': '/usr/bin:/bin', 'CODEX_HOME': str(root / 'codex-home'),
                                  'PYTHONDONTWRITEBYTECODE': '1'}, capture_output=True, text=True, timeout=45)
    write_once(root / 'artifact-check.json', {'exit_code': checked.returncode, 'stdout': checked.stdout, 'stderr': checked.stderr})
    require(checked.returncode == 0, 'complete candidate inventory refused')
    run = Run(root, value, time.monotonic() + window_end - time.time())
    check_observation_capabilities()
    run.sample(admission=True)
    write_once(root / 'execution-started.json', {'at': now(), 'candidate': value['candidate_key']})
    run.thread = threading.Thread(target=run.monitor, daemon=True)
    run.thread.start()
    def interrupted(number, _frame):
        run.reason = run.reason or 'controller interruption signal ' + str(number)
    for number in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
        signal.signal(number, interrupted)
    try:
        with (root / 'stdout.log').open('xb') as out, (root / 'stderr.log').open('xb') as err:
            require(run.resource_end - time.monotonic() > 90 and run.reason is None, 'work/cleanup allowance unavailable after admission')
            child = subprocess.Popen(['/usr/bin/sandbox-exec', '-f', str(root / 'phase-B.sb'), value['executable']],
                cwd=value['native_input_paths']['project'], env=value['environment'], stdout=out, stderr=err, start_new_session=True)
            run.reservation = AppReservation(child)  # Before any later IO can fail.
        run.log('native_B_started', pid=child.pid, actor=ACTOR, limits=LIMIT)
        run.ax = base.load_ax()(child.pid, run.alive, run.log)
        run.ax.output = root
        gen = run.observe_ready()
        require(ready_gate(run.diagnostics(), value) == gen, 'qualification changed before Stop')
        code = run.stop_and_quit(gen)
        qualification_error = None
        try:
            check_requests(run.stop_observation, gen)
        except (RuntimeError, ValueError, TypeError) as error:
            qualification_error = str(error)
        run.stop.set()
        run.thread.join(timeout=8)
        result = {'candidate': value['candidate_key'], 'phase': 'B', 'generation': gen,
                  'initialize_reply_and_ready_observed': True, 'owned_group_settlement_observed': True,
                  'native_quit_exit_code': code, 'success': code == 0 and not qualification_error and not run.reason and not run.log_errors,
                  'qualification_error': qualification_error, **run.settlement_facts(),
                  'actor': ACTOR, 'guard_reason': run.reason, 'logging_errors': run.log_errors,
                  'limits': LIMIT + ' LT-09 does not prove initialized notification delivery; no model/auth/workflow qualification.'}
        write_once(root / 'result.json', result)
        run.report(result)
        return 0 if result['success'] else 1
    except BaseException as error:
        if run.reservation is None:
            run.stop.set()
            run.thread.join(timeout=8)
            raise
        if run.reservation.reaped:
            run.stop.set()
            run.thread.join(timeout=8)
            run.report({'candidate': value['candidate_key'], 'state': 'settled-with-evidence-failure',
                        'success': False, 'original_app_reaped': True, 'error': str(error), 'limits': LIMIT})
            return 1
        original_error = str(error)
        run.safe_log('work_failed', error=original_error)
        try:
            code = run.cleanup_attempt()
            run.stop.set()
            run.thread.join(timeout=8)
            result = {'candidate': value['candidate_key'], 'phase': 'B', 'success': False,
                      'state': 'settled-after-work-failure', 'original_error': original_error,
                      'native_quit_exit_code': code, 'original_app_reaped': True,
                      'guard_reason': run.reason, 'logging_errors': run.log_errors, **run.settlement_facts(), 'limits': LIMIT}
            run.record('result.json', result)
            run.report(result)
            return 1
        except BaseException as cleanup_error:
            run.safe_log('normal_cleanup_unavailable', error=str(cleanup_error))
        run.safe_log('held_unknown', error=original_error)
        run.record('last-diagnostics.json', run.last_diagnostics)
        if run.ax is not None:
            try:
                run.ax.snapshot(root / 'held-AX.json')
            except BaseException:
                pass
        return run.hold(original_error)  # Retains custody until actual proved native recovery.


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare', type=Path, metavar='SUCCESSFUL_A_ATTEMPT')
    parser.add_argument('--execute', type=Path)
    parser.add_argument('--window-end')
    args = parser.parse_args()
    if args.prepare and not args.execute and not args.window_end:
        prepare(args.prepare.absolute())
    elif args.execute and args.window_end and not args.prepare:
        sys.exit(execute(args.execute.absolute(), datetime.fromisoformat(args.window_end).timestamp()))
    else:
        parser.error('choose --prepare SUCCESSFUL_A_ATTEMPT or --execute ATTEMPT --window-end UTC')
