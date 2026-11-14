#!/usr/bin/env python3
"""Fixtures that establish what the pinned Codex does with sandbox and approval settings.

Development evidence about the supplier at the pin; it qualifies no App candidate and writes no
recording. Each test that uses this module asserts one fact and fails when the pin stops
behaving so.

- `ScriptedStub`: a loopback Responses provider (standard library, 127.0.0.1 only, forwards
  nothing). It scripts the model's tool calls from markers in the request's last user message, so
  the turns are keyed on content, never on request order. It keeps in memory, for the test only,
  the tool names offered and the output Codex returned for each scripted call. It writes nothing
  to disk and never logs a body or a header value.
- `Run`: one fresh root (home, user home, project, outside, tmpdir) under a scratch folder, removed
  afterwards. Codex is started with an environment built here and nothing inherited: PATH, HOME,
  TZ, CODEX_HOME, TMPDIR, LANG and the examination launcher's proxy overrides. The App's
  account-home flags point the built-in provider at the stub.
- `Client`: the App side of stdio JSON-RPC. Every approval request it receives is declined and
  noted by method and thread only. A dynamic tool call is held or answered as the test says.

Every command the stub scripts is one of `commands()` below: fixed, harmless, and writing only
under the run's root, or under the run's own /private/tmp/chirality-level-<run>/ folder, which
the run refuses to start if it exists, creates itself, and removes afterwards.
"""
import hashlib
import json
import os
import queue
import secrets
import shlex
import shutil
import signal
import socketserver
import subprocess
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parent.parent
GENERATION = APP / 'src-tauri' / 'resources' / 'supplier' / '0.167.0' / 'GENERATION.json'
PIN = '0.167.0'
SYSTEM_PATH = '/usr/bin:/bin:/usr/sbin:/sbin'
# The examination launcher's proxy values (launch.py, copied here, not read): every outbound attempt
# that is not loopback goes to a closed port.
PROXY = 'http://127.0.0.1:9'
PROXY_NAMES = ('HTTPS_PROXY', 'https_proxy', 'HTTP_PROXY', 'http_proxy', 'ALL_PROXY', 'all_proxy')
EXEMPT = '127.0.0.1,localhost,::1'
MODEL = 'level-invented-model'
CLIENT_INFO = {'name': 'chirality-level-fixture', 'title': 'Chirality level fixture', 'version': '0.0.0'}
CAPABILITIES = {'experimentalApi': True, 'requestAttestation': False, 'explicitGatewayOauth': True}
APPROVAL_METHODS = ('item/commandExecution/requestApproval', 'item/fileChange/requestApproval',
                    'item/permissions/requestApproval', 'execCommandApproval', 'applyPatchApproval')
DECLINE = {'item/commandExecution/requestApproval': {'decision': 'decline'},
           'item/fileChange/requestApproval': {'decision': 'decline'},
           'item/permissions/requestApproval': {'permissions': {}, 'scope': 'turn'},
           'execCommandApproval': {'decision': 'denied'},
           'applyPatchApproval': {'decision': 'denied'}}
SLASH_TMP = Path('/private/tmp')
# The network probe: connects to the stub's own loopback port and asks for the probe path. Unlike curl, it prints
# the system's own reason when the connection is refused, so a sandbox refusal is in evidence, not inferred.
NET_PROBE = ('use IO::Socket::INET; my $s = IO::Socket::INET->new(PeerAddr => "127.0.0.1", PeerPort => $ARGV[0], '
             'Proto => "tcp", Timeout => 3); if ($s) { print $s "GET /level-net-probe HTTP/1.0\\r\\n\\r\\n"; '
             '<$s>; print "connected\\n"; exit 0 } print "connect failed: $!\\n"; exit 3')
APP_TOOL = 'level_invented_records_read'


class Refused(Exception):
    pass


def toml_string(value):
    """A TOML basic string for `value` (JSON's escapes are a subset TOML accepts)."""
    return json.dumps(str(value))


def pinned_sha256():
    return json.loads(GENERATION.read_text())['supplier']['main_sha256']


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b''):
            digest.update(chunk)
    return digest.hexdigest()


def admitted_binary(path):
    """The binary, after its digest is checked against the pin. Checked again before each start."""
    if not path or not os.path.isabs(path) or not os.path.isfile(path):
        raise Refused('CHIRALITY_CODEX_BIN is not an absolute path to a file')
    if sha256_file(path) != pinned_sha256():
        raise Refused('the binary is not the pinned Codex %s' % PIN)
    return path


# ---------- the scripted stub ----------

def sse(event, data):
    return ('event: %s\ndata: %s\n\n' % (event, json.dumps(data, separators=(',', ':')))).encode('utf-8')


def stream(items, response_id):
    out = [sse('response.created', {'type': 'response.created', 'response': {'id': response_id}})]
    for index, item in enumerate(items):
        out.append(sse('response.output_item.added',
                       {'type': 'response.output_item.added', 'output_index': index, 'item': item}))
        if item.get('type') == 'message':
            out.append(sse('response.output_text.delta',
                           {'type': 'response.output_text.delta', 'output_index': index, 'content_index': 0,
                            'delta': item['content'][0]['text'], 'item_id': item.get('id')}))
        out.append(sse('response.output_item.done',
                       {'type': 'response.output_item.done', 'output_index': index, 'item': item}))
    out.append(sse('response.completed', {'type': 'response.completed', 'response': {
        'id': response_id, 'usage': {'input_tokens': 1, 'input_tokens_details': {'cached_tokens': 0},
                                     'output_tokens': 1, 'output_tokens_details': {'reasoning_tokens': 0},
                                     'total_tokens': 2}}}))
    return out


def message(text, message_id):
    return {'type': 'message', 'role': 'assistant', 'id': message_id,
            'content': [{'type': 'output_text', 'text': text, 'annotations': []}]}


def tool_names(body):
    """Offered tools as `name` or `namespace.name`; a tool with no name by its type."""
    names = []
    for tool in (body or {}).get('tools') or []:
        if not isinstance(tool, dict):
            continue
        inner = tool.get('tools')
        if isinstance(inner, list):
            names.extend('%s.%s' % (tool.get('name'), t.get('name')) for t in inner if isinstance(t, dict))
        else:
            names.append(tool.get('name') or tool.get('type'))
    return names


def tool_parameters(body, name):
    """The property names of one offered tool's parameters (names only), or None."""
    for tool in (body or {}).get('tools') or []:
        candidates = tool.get('tools') if isinstance(tool.get('tools'), list) else [tool]
        for t in candidates:
            if isinstance(t, dict) and t.get('name') == name.split('.')[-1]:
                return sorted(((t.get('parameters') or {}).get('properties') or {}))
    return None


def text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return ''.join(p.get('text', '') for p in content if isinstance(p, dict) and isinstance(p.get('text'), str))
    return ''


def last_user_index(entries):
    for index in range(len(entries) - 1, -1, -1):
        entry = entries[index]
        if isinstance(entry, dict) and entry.get('role') == 'user' and entry.get('type', 'message') == 'message':
            return index
    return None


def turn_view(body):
    """(last user text, the outputs that follow it as {call_id: output text})."""
    entries = (body or {}).get('input') or []
    index = last_user_index(entries)
    if index is None:
        return '', {}
    outputs = {}
    for entry in entries[index + 1:]:
        if isinstance(entry, dict) and str(entry.get('type', '')).endswith('_output'):
            output = entry.get('output')
            outputs[entry.get('call_id')] = output if isinstance(output, str) else json.dumps(output)
    return text_of(entries[index].get('content')), outputs


def shell_call(body, call_id, command, escalate=False, background=False):
    """A call to whichever shell tool the request offers."""
    names = [n.split('.')[-1] for n in tool_names(body)]
    call = {'type': 'function_call', 'call_id': call_id, 'id': 'fc_' + call_id}
    extra = {}
    if escalate:
        extra = {'sandbox_permissions': 'require_escalated', 'justification': 'Invented fixture command.'}
    if 'exec_command' in names:
        args = dict({'cmd': command}, **extra)
        if background:
            args['yield_time_ms'] = 250
        return dict(call, name='exec_command', arguments=json.dumps(args))
    if 'shell_command' in names:
        return dict(call, name='shell_command', arguments=json.dumps(dict({'command': command}, **extra)))
    if 'shell' in names:
        return dict(call, name='shell', arguments=json.dumps(dict({'command': ['/bin/sh', '-c', command]}, **extra)))
    return None


class ScriptedStub:
    """Answers POST .../responses from scripts keyed by a marker `LEVEL[key]` in the last user message.

    `scripts[key]` is a function (body, outputs, stub) -> list of output items; `outputs` maps each
    call id that follows the last user message to the output Codex returned for it.
    """

    def __init__(self):
        self.scripts = {}
        self.lock = threading.Lock()
        self.count = 0
        self.requests = []  # per POST: {'key', 'tools'}; in memory only
        self.outputs = {}   # call id -> output text; in memory only
        self.net_probes = 0
        self.not_offered = set()  # call ids a command script could not call: no shell tool offered
        self.issued = set()  # call ids the stub put into a response as a call
        self.unexpected = []
        stub = self

        class Handler(BaseHTTPRequestHandler):
            protocol_version = 'HTTP/1.1'

            def log_message(self, *unused):
                pass

            def plain(self, status, body=b'{}'):
                self.send_response(status)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(body)))
                self.send_header('Connection', 'close')
                self.end_headers()
                self.wfile.write(body)
                self.close_connection = True

            def do_GET(self):
                path = self.path.split('?')[0]
                if path.endswith('/responses') and self.headers.get('Upgrade'):
                    self.plain(426)  # Codex 0.167.0 falls back to HTTP for the session at once
                elif path == '/level-net-probe':
                    with stub.lock:
                        stub.net_probes += 1
                    self.plain(200, b'probe')
                else:
                    with stub.lock:
                        stub.unexpected.append(('GET', path))
                    self.plain(404)

            def do_POST(self):
                path = self.path.split('?')[0]
                if not path.endswith('/responses'):
                    with stub.lock:
                        stub.unexpected.append(('POST', path))
                    self.plain(404)
                    return
                try:
                    body = json.loads(self.rfile.read(int(self.headers.get('Content-Length') or 0)))
                except ValueError:
                    self.plain(400)
                    return
                items = stub.answer(body)
                with stub.lock:
                    stub.count += 1
                    index = stub.count
                self.send_response(200)
                self.send_header('Content-Type', 'text/event-stream')
                self.send_header('Cache-Control', 'no-cache')
                self.send_header('Connection', 'close')
                self.end_headers()
                self.close_connection = True
                try:
                    for chunk in stream(items, 'resp_level_%d' % index):
                        self.wfile.write(chunk)
                    self.wfile.flush()
                except (BrokenPipeError, ConnectionResetError):
                    pass

        class Server(ThreadingHTTPServer):
            daemon_threads = True

            def server_bind(self):
                socketserver.TCPServer.server_bind(self)
                self.server_name, self.server_port = '127.0.0.1', self.server_address[1]

        self.server = Server(('127.0.0.1', 0), Handler)
        self.port = self.server.server_address[1]
        self.base_url = 'http://127.0.0.1:%d/v1' % self.port
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def answer(self, body):
        text, outputs = turn_view(body)
        key = None
        if 'LEVEL[' in text:
            key = text.split('LEVEL[', 1)[1].split(']', 1)[0]
        with self.lock:
            self.requests.append({'key': key, 'tools': tool_names(body), 'body_tools': body.get('tools'),
                                  'body_keys': sorted(body)})
            self.outputs.update(outputs)
        script = self.scripts.get(key)
        if script is None:
            return [message('No script for this turn.', 'msg_none')]
        items = script(body, outputs, self) or [message('Done.', 'msg_done_%s' % key)]
        with self.lock:
            self.issued.update(i['call_id'] for i in items if i.get('call_id'))
        return items

    def close(self):
        self.server.shutdown()
        self.server.server_close()


def command_script(call_id, command, escalate=False, background=False):
    """One scripted command, then a closing message once Codex has returned its output. When the request offers
    no shell tool, no call is made and the call id is noted in `stub.not_offered`, so a test can tell that apart
    from a command that ran."""
    def script(body, outputs, stub):
        if call_id in outputs:
            return [message('Done.', 'msg_' + call_id)]
        call = shell_call(body, call_id, command, escalate=escalate, background=background)
        if call is None:
            with stub.lock:
                stub.not_offered.add(call_id)
            return [message('No shell tool offered.', 'msg_noshell_' + call_id)]
        return [call]
    return script


# ---------- what a call's output shows ----------

SUCCEEDED = 'ran-succeeded'
SANDBOX_REFUSED = 'ran-refused-by-sandbox'   # ran, failed, and the sandbox's own refusal is in the output
FAILED = 'ran-failed'                        # ran and failed, with no refusal in evidence: never a refusal
RUNNING = 'still-running'                    # returned while its process keeps running in the background
DECLINED = 'declined-at-approval'            # an approval request for this call, declined by the fixture
REJECTED = 'rejected-by-policy'              # refused by Codex's approval policy before it ran
UNSUPPORTED = 'unsupported-call'             # Codex has no such tool in this conversation
NOT_OFFERED = 'not-offered'                  # the stub could not make the call: inconclusive, never a pass
SANDBOX_REFUSAL = 'operation not permitted'  # what the shell and the network probe print when the sandbox refuses


class Outcome:
    """One observed outcome of one scripted call, with the evidence it rests on."""

    def __init__(self, kind, exit=None, text='', evidence=None):
        self.kind, self.exit, self.text, self.evidence = kind, exit, text, evidence or {}

    def __repr__(self):
        return 'Outcome(%s, exit=%r, text=%r)' % (self.kind, self.exit, self.text[:160])


def classify(output):
    """The outcome a call's output shows, from Codex's own words at the pin. An output this does not recognise
    refuses: it is never read as an absence."""
    if output is None:
        raise Refused('no output was received for the call')
    if 'Process exited with code ' in output:
        code = int(output.split('Process exited with code ', 1)[1].split()[0])
        text = output.split('Output:', 1)[1].strip() if 'Output:' in output else ''
        if code == 0:
            return Outcome(SUCCEEDED, code, text)
        return Outcome(SANDBOX_REFUSED if SANDBOX_REFUSAL in text.lower() else FAILED, code, text)
    if 'Process running with session ID' in output:
        return Outcome(RUNNING, text=output)
    if 'rejected by user' in output:
        return Outcome(DECLINED, text=output)
    if 'approval policy is Never' in output:
        return Outcome(REJECTED, text=output)
    if output.startswith('unsupported call') or output.startswith('unsupported custom tool call'):
        return Outcome(UNSUPPORTED, text=output)
    raise Refused('an output this fixture does not recognise: %r' % output[:200])


def judge(call_id, issued, not_offered, output, item_ids, request_item_ids, turn_status):
    """The outcome of one call, from the protocol stages that outcome has, each tied to the call's id.

    - not offered: the stub could not make the call; returned as NOT_OFFERED, which `expect` reports as
      inconclusive, never as a pass;
    - otherwise the stub must have issued it, and the turn must have completed;
    - succeeded: the output says exit 0, and Codex started a command item with the call's id;
    - refused by the sandbox: the output says a non-zero exit and carries the refusal's own text;
    - declined: an approval request with the call's id reached the fixture, and the output says rejected;
    - rejected by policy: the output says so, and no approval request with the call's id was raised.
    Anything short of that refuses; nothing is inferred from an absence."""
    if call_id in not_offered:
        return Outcome(NOT_OFFERED)
    if call_id not in issued:
        raise Refused('the stub never issued %s' % call_id)
    if turn_status is None:
        raise Refused('unresolved: the turn carrying %s did not complete in time' % call_id)
    if turn_status != 'completed':
        raise Refused('the turn carrying %s ended %s' % (call_id, turn_status))
    outcome = classify(output)
    asked = call_id in request_item_ids
    if outcome.kind == SUCCEEDED and call_id not in item_ids:
        raise Refused('%s reported exit 0 without its command item' % call_id)
    if outcome.kind == DECLINED and not asked:
        raise Refused('%s was reported rejected without an approval request for it' % call_id)
    if outcome.kind == REJECTED and asked:
        raise Refused('%s was reported rejected by policy, yet a request was raised for it' % call_id)
    outcome.evidence = {'issued': True, 'item': call_id in item_ids, 'request': asked, 'turn': turn_status}
    return outcome


def expect(outcome, kind):
    """Assert one outcome. NOT_OFFERED is inconclusive: it fails, saying so, whatever was expected."""
    if outcome.kind == NOT_OFFERED:
        raise AssertionError('INCONCLUSIVE: the call was never offered, so nothing was observed')
    if outcome.kind != kind:
        raise AssertionError('expected %s, observed %r' % (kind, outcome))
    return outcome


# ---------- one run ----------

class Run:
    """A fresh root and one stub. Use as a context manager; the root is removed on exit."""

    def __init__(self, scratch, binary, slash_tmp=False, git_marker=False, home_name='home'):
        self.binary = binary
        self.home_name = home_name  # the Codex home's folder name under the root
        self.name = 'level-' + secrets.token_hex(6)
        scratch = Path(scratch).resolve()
        if not scratch.is_dir():
            raise Refused('the scratch folder does not exist')
        self.root = scratch / self.name
        self.slash_tmp = SLASH_TMP / ('chirality-level-' + self.name) if slash_tmp else None
        self.git_marker = git_marker
        self.made_slash_tmp = False
        self.stub = None
        self.clients = []

    def __enter__(self):
        if Path('/etc/codex').exists():
            raise Refused('/etc/codex exists, and the supplier reads system configuration from it')
        folder = self.root.parent
        while True:  # as the examination launcher: no .git above the project, so no ancestor's .codex is read
            if os.path.lexists(folder / '.git'):
                raise Refused('%s holds a .git entry above the project' % folder)
            if folder.parent == folder:
                break
            folder = folder.parent
        if self.slash_tmp is not None and os.path.lexists(self.slash_tmp):
            raise Refused('%s already exists' % self.slash_tmp)
        os.mkdir(self.root, 0o700)
        try:
            for child in (self.home_name, 'userhome', 'project', 'outside', 'tmpdir'):
                os.mkdir(self.root / child, 0o700)
            if self.git_marker:
                os.mkdir(self.root / 'project' / '.git', 0o700)
            if self.slash_tmp is not None:
                os.mkdir(self.slash_tmp, 0o700)  # fails if it appeared since the check
                self.made_slash_tmp = True
            self.stub = ScriptedStub()
        except BaseException:
            self.__exit__()
            raise
        return self

    def __exit__(self, *unused):
        """Every step runs even when an earlier one raises; the first error is raised after all have run, so a
        failed removal is never silent."""
        steps = [client.stop for client in self.clients]
        if self.stub is not None:
            steps.append(self.stub.close)
        if self.made_slash_tmp:  # only the folder this run made, never one it found
            steps.append(lambda: shutil.rmtree(self.slash_tmp))
        steps.append(lambda: os.path.lexists(self.root) and shutil.rmtree(self.root))
        errors = []
        for step in steps:
            try:
                step()
            except Exception as error:  # noqa: BLE001 - kept and raised after the remaining steps
                errors.append(error)
        if errors:
            raise Refused('cleanup failed: %s' % '; '.join('%s: %s' % (type(e).__name__, e) for e in errors))
        return False

    @property
    def home(self):
        return self.root / self.home_name

    @property
    def project(self):
        return self.root / 'project'

    def environment(self, extra=None):
        package = Path(self.binary).resolve().parent.parent
        env = {'PATH': str(package / 'codex-path') + ':' + SYSTEM_PATH, 'HOME': str(self.root / 'userhome'),
               'TZ': 'UTC', 'LANG': 'en_US.UTF-8', 'CODEX_HOME': str(self.root / self.home_name),
               'TMPDIR': str(self.root / 'tmpdir') + '/'}
        env.update({name: PROXY for name in PROXY_NAMES})
        env.update({'NO_PROXY': EXEMPT, 'no_proxy': EXEMPT})
        env.update(extra or {})
        return env

    def start(self):
        admitted_binary(self.binary)
        client = Client(self)
        self.clients.append(client)
        client.initialize()
        return client

    def paths(self):
        """The paths the fixed commands write."""
        out = {'in': self.project / 'w-in', 'out': self.root / 'outside' / 'w-out',
               'out2': self.root / 'outside' / 'w-out2',
               'tmpdir': self.root / 'tmpdir' / 'w-tmpdir', 'late': self.root / 'outside' / 'w-late',
               'git': self.project / '.git' / 'w-git', 'extra': self.root / 'outside' / 'w-extra'}
        if self.slash_tmp is not None:
            out['slashtmp'] = self.slash_tmp / 'w-slashtmp'
        return out

    def commands(self):
        """The only commands any fixture scripts. Each writes one file under the run's own folders, or reads the
        project, or asks the stub's own loopback address. Every path is quoted for the shell, so a scratch folder
        whose name holds spaces or shell characters cannot make a command write anywhere else."""
        p = self.paths()
        cmds = {key: 'printf ok > %s' % shlex.quote(str(path)) for key, path in p.items() if key != 'late'}
        cmds['late'] = 'sleep 4; printf ok > %s' % shlex.quote(str(p['late']))
        cmds['read'] = '/bin/ls %s' % shlex.quote(str(self.project))
        cmds['net'] = '/usr/bin/perl -e %s %d' % (shlex.quote(NET_PROBE), self.stub.port)
        return cmds


class Client:
    def __init__(self, run):
        self.run = run
        self.stderr = open(run.root / ('codex-stderr-%d.log' % len(run.clients)), 'wb')
        self.proc = subprocess.Popen(
            [run.binary, '-c', 'analytics.enabled=false', '-c', 'model_provider="openai"',
             '-c', 'openai_base_url="%s"' % run.stub.base_url, 'app-server'],
            cwd=str(run.project), env=run.environment(), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=self.stderr, start_new_session=True)
        self.pgid = self.proc.pid  # its own session, so its own process group
        self.lock = threading.Lock()
        self.changed = threading.Condition(self.lock)
        self.next_id = 0
        self.replies = {}
        self.notes = []
        self.server_requests = []  # {'method', 'thread', 'id', 'params'}; params kept in memory only
        self.tool_call_policy = 'answer'  # 'answer' or 'hold'
        self.held = []
        self.writer = threading.Lock()
        threading.Thread(target=self.read, daemon=True).start()

    def read(self):
        for line in self.proc.stdout:
            try:
                frame = json.loads(line)
            except ValueError:
                continue
            if 'method' in frame and 'id' in frame:
                self.on_request(frame)
            with self.changed:
                if 'method' in frame and 'id' not in frame:
                    self.notes.append(frame)
                elif 'id' in frame and 'method' not in frame:
                    self.replies[frame['id']] = frame
                self.changed.notify_all()
        with self.changed:
            self.changed.notify_all()

    def send(self, frame):
        with self.writer:
            self.proc.stdin.write((json.dumps(frame) + '\n').encode())
            self.proc.stdin.flush()

    def on_request(self, frame):
        method, params = frame['method'], frame.get('params') or {}
        record = {'method': method, 'thread': params.get('threadId') or params.get('conversationId'),
                  'id': frame['id'], 'params': params, 'at': time.monotonic()}
        with self.changed:
            self.server_requests.append(record)
        if method in DECLINE:
            self.send({'jsonrpc': '2.0', 'id': frame['id'], 'result': DECLINE[method]})
        elif method == 'item/tool/call':
            if self.tool_call_policy == 'hold':
                self.held.append(record)
            else:
                self.answer_tool_call(record)
        elif method == 'item/tool/requestUserInput':
            self.send({'jsonrpc': '2.0', 'id': frame['id'], 'result': {'answers': {}}})
        else:
            self.send({'jsonrpc': '2.0', 'id': frame['id'],
                       'error': {'code': -32601, 'message': 'fixture: not answered'}})

    def answer_tool_call(self, record):
        self.send({'jsonrpc': '2.0', 'id': record['id'], 'result': {
            'success': True, 'contentItems': [{'type': 'inputText', 'text': 'Invented records answer.'}]}})

    def call(self, method, params, timeout=30):
        with self.lock:
            self.next_id += 1
            ident = self.next_id
        self.send({'jsonrpc': '2.0', 'id': ident, 'method': method, 'params': params})
        reply = self.wait(lambda: self.replies.get(ident), timeout)
        if reply is None:
            raise Refused('no reply to %s within %ss' % (method, timeout))
        return reply

    def result(self, method, params, timeout=30):
        reply = self.call(method, params, timeout)
        if 'error' in reply:
            raise Refused('%s answered an error: %s' % (method, json.dumps(reply['error'])[:400]))
        return reply['result']

    def wait(self, predicate, timeout):
        deadline = time.monotonic() + timeout
        with self.changed:
            while True:
                value = predicate()
                if value:
                    return value
                left = deadline - time.monotonic()
                if left <= 0 or (self.proc.poll() is not None and not value):
                    return predicate()
                self.changed.wait(min(left, 0.5))

    def initialize(self):
        result = self.result('initialize', {'clientInfo': CLIENT_INFO, 'capabilities': CAPABILITIES})
        self.send({'jsonrpc': '2.0', 'method': 'initialized'})
        return result

    def start_thread(self, **settings):
        params = dict({'cwd': str(self.run.project), 'model': MODEL, 'modelProvider': 'openai'}, **settings)
        return self.result('thread/start', params)

    def notes_for(self, method, thread=None, turn=None):
        out = []
        for n in self.notes:
            if n.get('method') != method:
                continue
            p = n.get('params') or {}
            if thread is not None and p.get('threadId') != thread:
                continue
            if turn is not None and (p.get('turnId') or (p.get('turn') or {}).get('id')) != turn:
                continue
            out.append(n)
        return out

    def turn(self, thread, text, timeout=60, **settings):
        """Start a turn and wait for its completion. Returns (turn id, completed params or None)."""
        params = dict({'threadId': thread, 'input': [{'type': 'text', 'text': text}]}, **settings)
        turn = self.result('turn/start', params)['turn']['id']
        done = self.wait(lambda: self.notes_for('turn/completed', thread, turn), timeout)
        return turn, (done[0]['params'] if done else None)

    def items(self, thread, turn, kind=None):
        out = []
        for n in self.notes_for('item/completed', thread):
            p = n['params']
            if p.get('turnId') == turn and (kind is None or p['item'].get('type') == kind):
                out.append(p['item'])
        return out

    def requests_for(self, thread=None, methods=APPROVAL_METHODS):
        return [r for r in self.server_requests if r['method'] in methods and (thread is None or r['thread'] == thread)]

    def stop(self):
        """Close stdin, give the server a moment, then signal its whole process group, even when the leader has
        already exited, so no process it started outlives the run."""
        if self.proc.poll() is None:
            try:
                self.proc.stdin.close()
            except OSError:
                pass
            try:
                self.proc.wait(5)
            except subprocess.TimeoutExpired:
                pass
        self.kill_group()
        self.close_pipes()

    def kill_group(self):
        try:
            os.killpg(self.pgid, signal.SIGKILL)
        except ProcessLookupError:  # the group is gone
            pass
        except PermissionError:  # macOS: a group whose members have all exited and await reaping
            pass
        if self.proc.poll() is None:
            self.proc.wait(5)

    def close_pipes(self):
        for stream in (self.proc.stdin, self.proc.stdout, self.stderr):
            try:
                stream.close()
            except (OSError, ValueError):
                pass

    def kill(self):
        """End the app server and its group at once, as a quit or crash would."""
        self.kill_group()
