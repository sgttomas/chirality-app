#!/usr/bin/env python3
"""Fixtures that establish what the pinned Codex does with sandbox and approval settings.

Development evidence about the supplier at the pin; it qualifies no App candidate and writes no
recording. Each test that uses this module asserts one fact and fails when the pin stops
behaving so.

- `ScriptedStub`: a loopback Responses provider (standard library, 127.0.0.1 only, forwards
  nothing). It scripts the model's tool calls from markers in the request's last user message, so
  the turns are keyed on content, never on request order. It keeps in memory, for the test only,
  the tool names offered and the output Codex returned for each scripted call, and counts every
  connection it accepts. It writes nothing to disk and never logs a body or a header value.
- `Run`: one fresh root (home, user home, project, outside, tmpdir, and where asked a second project) under a scratch folder, removed
  afterwards; with `working_files`, the home and TMPDIR are laid out as the App lays them out. Codex is started with an environment built here and nothing inherited: PATH, HOME,
  TZ, CODEX_HOME, TMPDIR, LANG and the examination launcher's proxy overrides. The App's
  account-home flags point the built-in provider at the stub.
- `Client`: the App side of stdio JSON-RPC. Every approval request it receives is declined and
  noted by method and thread only. A dynamic tool call is held or answered as the test says.

Every command the stub scripts is one of `commands()` below: fixed, harmless, and writing only
under the run's root, or under the run's own /private/tmp/chirality-level-<run>/ folder, which
the run refuses to start if it exists, creates itself, and removes afterwards; and likewise, where a
test asks for it, under its own /private/var/tmp/chirality-level-<run>/ folder.
"""
import hashlib
import json
import os
import queue
import secrets
import shlex
import shutil
import signal
import socket
import socketserver
import stat
import subprocess
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parent.parent
GENERATION = APP / 'src-tauri' / 'resources' / 'supplier' / '0.169.0' / 'GENERATION.json'
PIN = '0.169.0'
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
VAR_TMP = Path('/private/var/tmp')
# The network probe: connects to the stub's own loopback port and asks for the probe path. Unlike curl, it prints
# the system's own reason when the connection is refused, so a sandbox refusal is in evidence, not inferred.
NET_PROBE = ('$SIG{ALRM} = sub { print "timed out\\n"; exit 4 }; alarm 3; '
             'use IO::Socket::INET; my $s = IO::Socket::INET->new(PeerAddr => "127.0.0.1", PeerPort => $ARGV[0], '
             'Proto => "tcp", Timeout => 3); if ($s) { print $s "GET /level-net-probe HTTP/1.0\\r\\n\\r\\n"; '
             '<$s>; print "connected\\n"; exit 0 } print "connect failed: $!\\n"; exit 3')
APP_TOOL = 'level_invented_records_read'
# The relative write's file name: it lands in the folder the command runs in.
RELATIVE_NAME = 'w-relative'


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


def shell_command_of(item):
    """The command a shell call would run, or None for any other item. A shell call whose command cannot be read
    is returned as its raw arguments, so that it never matches the fixed list."""
    if not isinstance(item, dict) or item.get('type') != 'function_call':
        return None
    if item.get('name') not in ('exec_command', 'shell_command', 'shell'):
        return None
    try:
        args = json.loads(item.get('arguments') or '{}')
    except ValueError:
        return item.get('arguments')
    if item['name'] == 'exec_command':
        return args.get('cmd')
    if item['name'] == 'shell_command':
        return args.get('command')
    command = args.get('command')
    if isinstance(command, list) and len(command) == 3 and command[:2] == ['/bin/sh', '-c']:
        return command[2]
    return json.dumps(command)


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


def placements_of(body, markers):
    """For each of `markers` that a request body carries anywhere: where it sits in text the model reads, and how
    much of it lies elsewhere. 'where' lists, in the body's order, 'instructions' (the request's own instructions
    text) and 'input[<index>]:<role>' for each input message whose text carries it; 'count' is how many times it
    appears in those texts; 'elsewhere' is how many more times it appears anywhere else in the serialised body
    (another field of an entry, an entry that is not a message). Nothing else of the body is kept."""
    out = {}
    body = body or {}
    entries = body.get('input') or []
    instructions = body.get('instructions') if isinstance(body.get('instructions'), str) else ''
    for marker in markers:
        places, count = [], instructions.count(marker)
        if count:
            places.append('instructions')
        for index, entry in enumerate(entries):
            if not isinstance(entry, dict) or entry.get('type', 'message') != 'message' or not entry.get('role'):
                continue
            n = text_of(entry.get('content')).count(marker)
            if n:
                places.append('input[%d]:%s' % (index, entry['role']))
                count += n
        total = json.dumps(body).count(marker)
        if total:
            out[marker] = {'count': count, 'where': places, 'elsewhere': total - count}
    return out


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

    def __init__(self, serve=True):
        """With `serve` False the listener is bound but not yet served, so that its owner can register it for
        cleanup first and then call `serve`."""
        self.scripts = {}
        self.lock = threading.Lock()
        self.count = 0
        self.requests = []  # per POST: {'key', 'tools'}; in memory only
        self.outputs = {}   # call id -> output text; in memory only
        self.net_probes = 0
        self.not_offered = set()  # call ids a command script could not call: no shell tool offered
        self.connections = 0  # every connection accepted, whatever it carried (counted before it is read)
        self.active = set()  # the accepted sockets a handler still holds; ended by `close`
        self.serving = False
        self.contacts = []  # (method, path) of every HTTP request read, in order; in memory only
        self.issued = set()  # call ids the stub put into a response as a call
        self.allowed_commands = None  # set by Run: the only commands a shell call may carry
        self.violations = []  # shell calls a script tried to issue with a command off that list
        self.unexpected = []
        self.watched = ()  # set by a test: invented marker lines whose presence in each request is noted
        self.record_model = False  # set by a test: the model each request names is noted too
        # Aligned with `requests` while markers are watched: for each marker carried, how many times and where
        # (`placements_of`). The markers' positions alone are kept, never the text around them.
        self.placements = []
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
                with stub.lock:
                    stub.contacts.append(('GET', path))
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
                with stub.lock:
                    stub.contacts.append(('POST', path))
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

            def process_request(self, request, client_address):
                with stub.lock:  # counted whatever the connection carries, even what is not HTTP/1.1
                    stub.connections += 1
                    stub.active.add(request)
                ThreadingHTTPServer.process_request(self, request, client_address)

            def shutdown_request(self, request):
                with stub.lock:
                    stub.active.discard(request)
                ThreadingHTTPServer.shutdown_request(self, request)

        self.server = Server(('127.0.0.1', 0), Handler)
        self.port = self.server.server_address[1]
        self.base_url = 'http://127.0.0.1:%d/v1' % self.port
        if serve:
            self.serve()

    def serve(self):
        """Start serving; if the serving thread cannot start, the listener is closed before the error is raised."""
        try:
            threading.Thread(target=self.server.serve_forever, daemon=True).start()
        except BaseException:
            self.server.server_close()
            raise
        self.serving = True

    def answer(self, body):
        text, outputs = turn_view(body)
        key = None
        if 'LEVEL[' in text:
            key = text.split('LEVEL[', 1)[1].split(']', 1)[0]
        # Which invented markers the request carries anywhere in its body: the markers alone, never the body.
        raw = json.dumps(body) if self.watched else ''
        placed = placements_of(body, self.watched) if self.watched else {}
        with self.lock:
            self.requests.append({'key': key, 'tools': tool_names(body), 'body_tools': body.get('tools'),
                                  'body_keys': sorted(body), 'markers': [m for m in self.watched if m in raw]})
            if self.record_model:
                self.requests[-1]['model'] = body.get('model')
            self.placements.append(placed)
            self.outputs.update(outputs)
        script = self.scripts.get(key)
        if script is None:
            return [message('No script for this turn.', 'msg_none')]
        items = script(body, outputs, self) or [message('Done.', 'msg_done_%s' % key)]
        for item in items:
            command = shell_command_of(item)
            if command is not None and (self.allowed_commands is None or command not in self.allowed_commands):
                with self.lock:
                    self.violations.append(command)
                return [message('Refused by the fixture: a command off the fixed list.', 'msg_refused')]
        with self.lock:
            self.issued.update(i['call_id'] for i in items if i.get('call_id'))
        return items

    def close(self, wait=2.0):
        """Stop accepting, close the listener, then end every connection a handler still holds (a handler blocked
        reading one would otherwise keep it open): each is shut down, its handler given `wait` seconds to let it
        go, and any still held is closed."""
        if self.serving:  # `shutdown` waits for a serving loop, so it is called only when one was started
            self.server.shutdown()
        self.server.server_close()
        with self.lock:
            held = list(self.active)
        for request in held:
            try:
                request.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
        deadline = time.monotonic() + wait
        while time.monotonic() < deadline:
            with self.lock:
                if not self.active:
                    return
            time.sleep(0.05)
        with self.lock:
            left, self.active = list(self.active), set()
        for request in left:
            try:
                request.close()
            except OSError:
                pass


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


def forced_exec_script(call_id, command, escalate=False):
    """A call to exec_command whether or not the request offers it (a fork's requests carry no tools), keeping the
    escalation request when asked for."""
    def script(body, outputs, stub):
        if call_id in outputs:
            return [message('Done.', 'msg_' + call_id)]
        args = {'cmd': command}
        if escalate:
            args.update({'sandbox_permissions': 'require_escalated', 'justification': 'Invented fixture command.'})
        return [{'type': 'function_call', 'name': 'exec_command', 'call_id': call_id, 'id': 'fc_' + call_id,
                 'arguments': json.dumps(args)}]
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
NETWORK = 'network'  # the target of the network probe


class Lines(frozenset):
    """The exact lines that alone show the sandbox refused a command that is not a shell redirection (a rename,
    a removal, a link), given by the command's own author. Passed as a call's target."""


def refusal_lines(target):
    """The exact lines that show the sandbox refused the expected target, one per shell seen at the pin: zsh's,
    bash's and sh's for a write to `target`, and the network probe's own line; or, for `Lines`, exactly those.
    Nothing else counts."""
    if isinstance(target, Lines):
        return set(target)
    if target == NETWORK:
        return {'connect failed: Operation not permitted'}
    path = str(target)
    return {'zsh:1: operation not permitted: %s' % path,
            '/bin/zsh:1: operation not permitted: %s' % path,
            '/bin/bash: %s: Operation not permitted' % path,
            'bash: %s: Operation not permitted' % path,
            'bash: line 1: %s: Operation not permitted' % path,
            '/bin/sh: %s: Operation not permitted' % path,
            'sh: %s: Operation not permitted' % path}


class Outcome:
    """One observed outcome of one scripted call, with the evidence it rests on."""

    def __init__(self, kind, exit=None, text='', evidence=None):
        self.kind, self.exit, self.text, self.evidence = kind, exit, text, evidence or {}

    def __repr__(self):
        return 'Outcome(%s, exit=%r, text=%r)' % (self.kind, self.exit, self.text[:160])


def classify(output, target=None):
    """The outcome a call's output shows, from Codex's own words at the pin. A failure is a sandbox refusal only
    when its whole output is exactly one of `refusal_lines(target)`; any other failure is FAILED. An output this
    does not recognise refuses: it is never read as an absence."""
    if output is None:
        raise Refused('no output was received for the call')
    if 'Process exited with code ' in output:
        code = int(output.split('Process exited with code ', 1)[1].split()[0])
        text = output.split('Output:', 1)[1].strip() if 'Output:' in output else ''
        if code == 0:
            return Outcome(SUCCEEDED, code, text)
        refused = target is not None and text in refusal_lines(target)
        return Outcome(SANDBOX_REFUSED if refused else FAILED, code, text)
    if 'Process running with session ID' in output:
        return Outcome(RUNNING, text=output)
    if 'rejected by user' in output:
        return Outcome(DECLINED, text=output)
    if 'approval policy is Never' in output:
        return Outcome(REJECTED, text=output)
    if output.startswith('unsupported call') or output.startswith('unsupported custom tool call'):
        return Outcome(UNSUPPORTED, text=output)
    raise Refused('an output this fixture does not recognise: %r' % output[:200])


def judge(call_id, issued, not_offered, output, item_ids, request_item_ids, turn_status, target=None,
          item_status=None, item_exit=None):
    """The outcome of one call, from the protocol stages that outcome has, each tied to the call's id.

    `item_ids` are the ids of commandExecution items started in the call's own turn; `item_status` is the status
    that call's item completed with, if it completed, and `item_exit` the exit code that item carried.
    - not offered: the stub could not make the call; returned as NOT_OFFERED, which `expect` reports as
      inconclusive, never as a pass;
    - otherwise the stub must have issued it, and the turn must have completed;
    - succeeded: the output says exit 0, and a commandExecution item with the call's id started in that turn;
    - refused by the sandbox: a non-zero exit, and the whole output is the refusal line for the expected target; no
      item is required, but an item that completed, or carries another exit code, contradicts it and refuses;
    - declined: an approval request with the call's id reached the fixture, the output says rejected, and the
      call's item, if any, ended declined, not run;
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
    outcome = classify(output, target)
    asked = call_id in request_item_ids
    if outcome.kind == SUCCEEDED and call_id not in item_ids:
        raise Refused('%s reported exit 0 without its command item in its turn' % call_id)
    if outcome.kind == DECLINED:
        if not asked:
            raise Refused('%s was reported rejected without an approval request for it' % call_id)
        if item_status not in (None, 'declined'):
            raise Refused('%s was declined, yet its item ended %s' % (call_id, item_status))
        if item_exit is not None:
            raise Refused('%s was declined, yet its item carries exit code %r' % (call_id, item_exit))
    if outcome.kind == SANDBOX_REFUSED and (item_status == 'completed' or
                                            (item_exit is not None and item_exit != outcome.exit)):
        # No item is required for a refusal (a refused command completes none), but one that is present and says
        # otherwise contradicts it.
        raise Refused('%s printed a refusal, yet its item ended %s with exit code %r' % (call_id, item_status, item_exit))
    if outcome.kind == REJECTED and asked:
        raise Refused('%s was reported rejected by policy, yet a request was raised for it' % call_id)
    outcome.evidence = {'issued': True, 'item': call_id in item_ids, 'request': asked, 'turn': turn_status,
                        'item_status': item_status, 'item_exit': item_exit}
    return outcome


def expect(outcome, kind):
    """Assert one outcome. NOT_OFFERED is inconclusive, and so is a failure where a sandbox refusal was expected
    but the refusal line for the target was not what the command printed: each fails, saying so."""
    if outcome.kind == NOT_OFFERED:
        raise AssertionError('INCONCLUSIVE: the call was never offered, so nothing was observed')
    if kind == SANDBOX_REFUSED and outcome.kind == FAILED:
        raise AssertionError('INCONCLUSIVE: it failed, but not with the refusal line for its target: %r' % outcome)
    if outcome.kind != kind:
        raise AssertionError('expected %s, observed %r' % (kind, outcome))
    return outcome


UNSAFE_PATH_CHARACTERS = '$`"\\'


def checked_scratch(scratch):
    """The resolved scratch base, refused unless it and every ancestor are free of the characters a shell expands
    inside double quotes, so no path the fixture makes can carry them to Codex."""
    base = Path(scratch).resolve()
    if not base.is_dir():
        raise Refused('the scratch folder does not exist')
    for part in (base,) + tuple(base.parents):
        bad = [c for c in UNSAFE_PATH_CHARACTERS if c in part.name]
        if bad:
            raise Refused('the scratch base %s holds %r; choose another' % (part, ''.join(bad)))
    return base


class Unobserved(Exception):
    """A process could not be observed: neither present nor established gone."""


def observe_process(pid, kill=os.kill, run=subprocess.run):
    """The process numbered `pid`, observed alone (a signal 0, then `ps -p` for that one process; no search):
    ('gone', None) only when the signal check reports no such process; ('present', start time) when `ps` succeeds and
    prints a start time. Anything else raises Unobserved. A process that ends between the two observations is
    established gone by the signal check again."""
    def absent():
        try:
            kill(pid, 0)
        except ProcessLookupError:
            return True
        except PermissionError:
            return False
        return False
    if absent():
        return ('gone', None)
    try:
        out = run(['/bin/ps', '-o', 'lstart=', '-p', str(pid)], capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError) as error:
        raise Unobserved('ps for process %d could not run: %s' % (pid, error))
    started = (out.stdout or '').strip()
    if out.returncode == 0 and started:
        return ('present', started)
    if absent():
        return ('gone', None)
    raise Unobserved('ps for process %d answered %d with %r' % (pid, out.returncode, started))


def still_running(pid, at, observe=observe_process):
    """Whether the process numbered `pid` that started at `at` is still the same, running process. False only on
    positive evidence (gone, or the number now names a process with another start time); an observation that fails
    raises Unobserved, so a row relying on it fails rather than claim the process ended."""
    state, started = observe(pid)
    return state == 'present' and started == at


def end_known(known, observe=observe_process, kill=os.kill):
    """Ends each process of `known` ({name: (pid, start time)}) that is still the same process, or that cannot be
    observed: unknown is a reason to try, never a reason to skip."""
    for pid, at in known.values():
        try:
            if not still_running(pid, at, observe):
                continue
        except Unobserved:
            pass
        try:
            kill(pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass


def group_members(pgid, run=subprocess.run):
    result = run(['/bin/ps', '-axo', 'pgid='], capture_output=True, text=True, timeout=20)
    if result.returncode != 0:
        raise Refused('the process list could not be read')
    return result.stdout.split().count(str(pgid))


def group_has_members(pgid, killpg=os.killpg, members=group_members):
    """Whether the process group `pgid` still has a member: a signal 0 to the group. macOS answers a group whose
    members have all exited and await reaping with a permission error, so the group's members are then counted by
    group number (`group_members`)."""
    try:
        killpg(pgid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return members(pgid) > 0
    return True


# ---------- one run ----------

class RecordingRefusal:
    """In place of the closed proxy port: a loopback listener that refuses every request, as the closed port does,
    and first records where it was going. Only the target is kept, in memory: the host and port of a CONNECT, or
    the scheme, host and port of an absolute URL; never a path, a header or a body. Each entry is
    (monotonic time, method, target)."""

    def __init__(self):
        attempts = self.attempts = []
        lock = self.lock = threading.Lock()

        class Handler(socketserver.BaseRequestHandler):
            def handle(self):
                self.request.settimeout(3)
                try:
                    line = self.request.recv(4096).split(b'\r\n', 1)[0].decode('latin-1')
                except OSError:
                    line = ''
                parts = line.split(' ')
                method, target = (parts[0], parts[1]) if len(parts) >= 2 else ('?', '?')
                if '://' in target:
                    scheme, rest = target.split('://', 1)
                    target = scheme + '://' + rest.split('/', 1)[0]
                with lock:
                    attempts.append((time.monotonic(), method, target))
                try:
                    self.request.sendall(b'HTTP/1.1 502 Bad Gateway\r\nContent-Length: 0\r\nConnection: close\r\n\r\n')
                except OSError:
                    pass

        class Server(socketserver.ThreadingTCPServer):
            daemon_threads = True
            allow_reuse_address = True

        self.server = Server(('127.0.0.1', 0), Handler)
        self.url = 'http://127.0.0.1:%d' % self.server.server_address[1]
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def since(self, mark):
        with self.lock:
            return [(method, target) for at, method, target in self.attempts if at >= mark]

    def close(self):
        self.server.shutdown()
        self.server.server_close()


# Names the run's own layout uses in its root (the plain one and the App's, `working_files`), and `.git`, which
# beside the project would be a repository marker above it.
RUN_FOLDERS = ('home', 'userhome', 'outside', 'tmpdir', 'Invented App Data', 'Invented App Data Working Files',
               '.git')
# The relative write's exit when the folder it finds itself in is neither project: nothing is written.
RELATIVE_ELSEWHERE = 97

# ---------- a project's own files (the trusted-project rows) ----------
# The only files a test may write into the project, relative to it.
TRUST_FILES = ('.codex/config.toml', '.codex/hooks.json', '.codex/rules/invented.rules', 'AGENTS.md',
               'sub/AGENTS.md')
# The subfolder a conversation may be given, inside the project (where `sub/AGENTS.md` is written).
SUBFOLDER = 'sub'
# The only files a test may write into the Codex home (the person's own settings), for a positive control.
HOME_FILES = ('config.toml', 'rules/default.rules')
# Hook events that fire in an ordinary turn with one command, each with a marker of its own.
HOOK_MARKERS = {'SessionStart': 'hook-session-start', 'UserPromptSubmit': 'hook-user-prompt',
                'PreToolUse': 'hook-pre-tool', 'PostToolUse': 'hook-post-tool', 'Stop': 'hook-stop'}
# Every marker a program named by a project's file may write; each is one file under the run's `outside` folder.
PROJECT_MARKERS = tuple(HOOK_MARKERS.values()) + ('mcp-stdio', 'notify', 'zdotdir', 'bash-env', 'mcp-person-same',
                                                  'mcp-person-other', 'mcp-headers-helper')
MCP_PERSON = 'level_invented_person'  # a server of the person's own, named in no project file
MCP_HELPER = 'level_invented_helper'  # an HTTP server whose headers come from a helper command
OTHER_PROVIDER = 'level_invented_other'
OTHER_MODEL = 'level-invented-other-model'
MCP_STDIO = 'level_invented_stdio'
MCP_HTTP = 'level_invented_http'
TRUST_ENV = 'LEVEL_TRUST_ENV'
# The keys the public source at rust-v0.169.0 strips from a project's own settings (PROJECT_LOCAL_CONFIG_DENYLIST in
# codex-rs/config/src/loader/mod.rs), as read there; the rows observe it, they do not rely on it.
PROJECT_DENYLIST_READ = ('openai_base_url', 'chatgpt_base_url', 'apps_mcp_product_sku', 'responses_api_metadata',
                         'model_provider', 'model_providers', 'notify', 'profile', 'profiles',
                         'experimental_realtime_webrtc_call_base_url', 'experimental_realtime_ws_base_url', 'otel')


class Run:
    """A fresh root and one stub. Use as a context manager; the root is removed on exit.

    With `second_project` (a folder name), a second project folder B is made beside the project A, in the run's
    root, with the same care: its name checked, 0700, and with `second_git_marker` a `.git` folder inside it. The
    app server is still started in A. `instructions` writes an invented `AGENTS.md` into each of A and B, each
    with its own marker line (`markers`); `project_settings` writes an invented `.codex/config.toml` into each,
    naming a writable root of its own under `outside` (`settings_roots`).

    With `trusted_project`, the project A can be given its own files (`write_trust_file`, one of `TRUST_FILES`),
    whose contents the fixture's builders make (`hooks_json`, `mcp_toml`, ...). Every program those files name is
    the fixture's marker command (`marker_command`): absolute system binaries only, appending one line to its own
    marker file under `outside`, and nothing else. A second loopback listener (`other`, a second stub) is made and
    closed with the run, for the files that name a destination; it counts every connection it accepts."""

    def __init__(self, scratch, binary, slash_tmp=False, git_marker=False, project_name='project',
                 working_files=False, var_tmp=False, proxy=None, second_project=None, second_git_marker=False,
                 instructions=False, project_settings=False, trusted_project=False):
        self.binary = binary
        self.trusted_project = trusted_project
        self.other = None  # with `trusted_project`: the second loopback listener
        self.proxy = proxy  # a RecordingRefusal in place of the closed port, or None for the closed port
        if '/' in project_name or project_name in ('', '.', '..'):
            raise Refused('a project folder name, not a path')
        self.project_name = project_name  # only this folder's name may carry characters the scratch base may not
        if second_project is not None:
            if '/' in second_project or second_project in ('', '.', '..'):
                raise Refused('a second project folder name, not a path')
            if second_project == project_name or second_project in RUN_FOLDERS or second_project.startswith('codex-stderr-'):
                raise Refused('the second project folder needs a name of its own')
            if any(c in second_project for c in UNSAFE_PATH_CHARACTERS):
                raise Refused('only the first project folder name may carry %r' % UNSAFE_PATH_CHARACTERS)
        elif second_git_marker or instructions or project_settings:
            raise Refused('a second project folder is needed for its marker, instructions or settings')
        self.second_project = second_project
        self.second_git_marker = second_git_marker
        self.instructions = instructions
        self.project_settings = project_settings
        tag = secrets.token_hex(4)  # distinct per run, so a marker seen cannot be left from another run
        self.markers = {'a': 'INVENTED-INSTRUCTION-MARKER-A-' + tag,
                        'b': 'INVENTED-INSTRUCTION-MARKER-B-' + tag} if instructions else {}
        # With `trusted_project`: the line the project's own settings give as instructions, and the App's own.
        # And the lines of the project's own `AGENTS.md` and of a nested one in `sub/`.
        self.trust_markers = {'project': 'INVENTED-PROJECT-SETTINGS-MARKER-' + tag,
                              'app': 'INVENTED-APP-INSTRUCTIONS-MARKER-' + tag,
                              'agents-root': 'INVENTED-AGENTS-ROOT-MARKER-' + tag,
                              'agents-sub': 'INVENTED-AGENTS-SUB-MARKER-' + tag} if trusted_project else {}
        self.name = 'level-' + secrets.token_hex(6)
        self.root = checked_scratch(scratch) / self.name
        self.slash_tmp = SLASH_TMP / ('chirality-level-' + self.name) if slash_tmp else None
        self.git_marker = git_marker
        self.made_slash_tmp = False
        self.var_tmp = VAR_TMP / ('chirality-level-' + self.name) if var_tmp else None
        self.made_var_tmp = False
        # With `working_files`, the App's layout (invented names): the Codex home inside an invented data folder,
        # and TMPDIR a folder made inside "codex-tmp" in the "<data folder> Working Files" folder beside it.
        self.working_files = working_files
        if working_files:
            self.data = self.root / 'Invented App Data'
            self.home = self.data / 'homes' / 'account'
            self.working = self.root / 'Invented App Data Working Files'
            self.codex_tmp = self.working / 'codex-tmp'
            self.tmpdir = self.codex_tmp / ('start-' + secrets.token_hex(4))
        else:
            self.data = self.working = self.codex_tmp = None
            self.home = self.root / 'home'
            self.tmpdir = self.root / 'tmpdir'
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
        for shared in (self.slash_tmp, self.var_tmp):
            if shared is not None and os.path.lexists(shared):
                raise Refused('%s already exists' % shared)
        os.mkdir(self.root, 0o700)
        try:
            for child in ('userhome', self.project_name, 'outside'):
                os.mkdir(self.root / child, 0o700)
            if self.second_project is not None:
                os.mkdir(self.project_b, 0o700)
            for folder in (self.home, self.tmpdir):
                os.makedirs(folder, 0o700)
            if self.working_files:
                (self.home / 'config.toml').write_bytes(b'')  # new, empty settings
            if self.git_marker:
                os.mkdir(self.project / '.git', 0o700)
            if self.second_git_marker:
                os.mkdir(self.project_b / '.git', 0o700)
            self.write_project_files()
            if self.slash_tmp is not None:
                os.mkdir(self.slash_tmp, 0o700)  # fails if it appeared since the check
                self.made_slash_tmp = True
            if self.var_tmp is not None:
                os.mkdir(self.var_tmp, 0o700)  # fails if it appeared since the check
                self.made_var_tmp = True
            self.stub = ScriptedStub()
            self.stub.allowed_commands = set(self.commands().values())  # enforced before any call reaches Codex
            if self.trusted_project:
                self.write_shell_files()
                self.other = ScriptedStub(serve=False)  # registered for cleanup before it serves
                self.other.allowed_commands = self.stub.allowed_commands
                self.other.serve()
        except BaseException:
            self.__exit__()
            raise
        return self

    def __exit__(self, *unused):
        """Every step runs even when an earlier one raises; the first error is raised after all have run, so a
        failed removal is never silent."""
        steps = [client.stop for client in self.clients]
        if self.clients:
            steps.append(self.nothing_remains)
        if self.stub is not None:
            steps.append(self.stub.close)
        if self.other is not None:
            steps.append(self.other.close)
        if self.made_slash_tmp:  # only the folder this run made, never one it found
            steps.append(lambda: shutil.rmtree(self.slash_tmp))
        if self.made_var_tmp:  # likewise
            steps.append(lambda: shutil.rmtree(self.var_tmp))
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

    def nothing_remains(self, wait=10.0):
        """After the servers are stopped: wait until none of the Codex servers this run started is still running
        and no member of any of their process groups remains, or fail naming each that does. A server is known by
        its number (the run is its parent) and the start time recorded when it started, so a number used again by
        another process does not count; a group is checked by a signal 0 to it. No process's command line or open
        files are read. A command that Codex ran in a process group of its own is not seen here: the rows that start
        such commands know their numbers and end them themselves (`end_known`). The network probe is not one of the
        run's servers; it ends within its 3 s alarm."""
        deadline = time.monotonic() + wait
        while True:
            left = []
            for client in self.clients:
                pid = client.proc.pid
                try:
                    running = client.proc.poll() is None or (
                        client.started_at is not None and still_running(pid, client.started_at))
                except Unobserved as error:
                    running, why = True, str(error)
                else:
                    why = 'still running'
                if running:
                    left.append('server %d: %s' % (pid, why))
                if group_has_members(client.pgid):
                    left.append('process group %d has a member' % client.pgid)
            if not left:
                return
            if time.monotonic() >= deadline:
                raise Refused('processes of the run remain after %.0f s: %s' % (wait, '; '.join(left)))
            time.sleep(0.25)

    @property
    def project(self):
        return self.root / self.project_name

    @property
    def project_b(self):
        """The second project folder B, or None."""
        return self.root / self.second_project if self.second_project is not None else None

    def settings_roots(self):
        """With `project_settings`: the writable root each project's own settings name, {'a': ..., 'b': ...}."""
        if not self.project_settings:
            return {}
        return {'a': self.root / 'outside' / 'root-a', 'b': self.root / 'outside' / 'root-b'}

    def write_project_files(self):
        """The invented instruction and settings files of A and B, as the run's options ask."""
        folders = {'a': self.project, 'b': self.project_b}
        if self.instructions:
            for side, folder in folders.items():
                (folder / 'AGENTS.md').write_text('# Invented instructions for a fixture\n\n%s\n' % self.markers[side])
        for side, root in self.settings_roots().items():
            os.mkdir(root, 0o700)
            os.mkdir(folders[side] / '.codex', 0o700)
            (folders[side] / '.codex' / 'config.toml').write_text(
                '[sandbox_workspace_write]\nwritable_roots = [%s]\n' % toml_string(root))

    def relative_landings(self):
        """Where the relative write (`commands()['relative']`) lands if it runs in A or in B."""
        if self.second_project is None:
            return {}
        return {'a': self.project / RELATIVE_NAME, 'b': self.project_b / RELATIVE_NAME}

    def environment(self, extra=None):
        package = Path(self.binary).resolve().parent.parent
        env = {'PATH': str(package / 'codex-path') + ':' + SYSTEM_PATH, 'HOME': str(self.root / 'userhome'),
               'TZ': 'UTC', 'LANG': 'en_US.UTF-8', 'CODEX_HOME': str(self.home),
               'TMPDIR': str(self.tmpdir) + '/'}
        env.update({name: (self.proxy.url if self.proxy is not None else PROXY) for name in PROXY_NAMES})
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
               'tmpdir': self.tmpdir / 'w-tmpdir', 'late': self.root / 'outside' / 'w-late',
               'git': self.project / '.git' / 'w-git', 'extra': self.root / 'outside' / 'w-extra'}
        if self.slash_tmp is not None:
            out['slashtmp'] = self.slash_tmp / 'w-slashtmp'
        if self.var_tmp is not None:
            out['vartmp'] = self.var_tmp / 'w-vartmp'
        if self.second_project is not None:
            out['in-b'] = self.project_b / 'w-in-b'
        for side, root in self.settings_roots().items():
            out['root-' + side] = root / ('w-root-' + side)
        if self.trusted_project:  # written by `/usr/bin/touch`, not by a redirection (see `commands`)
            out['touch-out'] = self.root / 'outside' / 'w-touch-out'
            out['touch-in'] = self.project / 'w-touch-in'
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
        if self.second_project is not None:
            # Run in whatever folder the command is given: the folder it prints, and the file it writes there.
            # The relative write checks, in the same shell call, that the folder it is in is one of the two
            # projects, and writes nothing anywhere else: a command given some other folder exits 97.
            cmds['pwd'] = '/bin/pwd -P'
            cmds['relative'] = 'case "$(/bin/pwd -P)" in %s|%s) printf ok > %s;; *) exit %d;; esac' % (
                shlex.quote(os.path.realpath(self.project)), shlex.quote(os.path.realpath(self.project_b)),
                RELATIVE_NAME, RELATIVE_ELSEWHERE)
        if self.working_files:
            cmds.update({key: command for key, (command, _) in self.entry_operations().items()})
        if self.trusted_project:
            # A program a rule can name, with no redirection: a project's exec-policy rule matches its first word.
            for key in ('touch-out', 'touch-in'):
                cmds[key] = '/usr/bin/touch %s' % shlex.quote(str(p[key]))
            # What a command sees of the variable a project's shell environment policy may set; exits 0 either way.
            cmds['env'] = 'printf %%s "${%s-unset}"' % TRUST_ENV
        return cmds

    def touch_refusals(self):
        """With `trusted_project`: the exact line the sandbox's refusal of each `touch` command prints."""
        if not self.trusted_project:
            return {}
        return {key: Lines({'touch: %s: Operation not permitted' % self.paths()[key]})
                for key in ('touch-out', 'touch-in')}

    # ----- a project's own files (`trusted_project`) -----

    def needs_trusted_project(self):
        if not self.trusted_project:
            raise Refused('the project files and their markers need Run(trusted_project=True)')

    def marker(self, name):
        """The marker file of one of `PROJECT_MARKERS`, under the run's `outside` folder."""
        self.needs_trusted_project()
        if name not in PROJECT_MARKERS:
            raise Refused('a marker off the fixed list: %r' % name)
        return self.root / 'outside' / ('m-' + name)

    def marker_command(self, name):
        """The only command a project's file names: appends one line to its marker file, and exits."""
        return "/usr/bin/printf 'ok\\n' >> %s" % shlex.quote(str(self.marker(name)))

    def marker_argv(self, name):
        """`marker_command` as a program and its arguments, for the settings that take a list."""
        return ['/bin/sh', '-c', self.marker_command(name)]

    def marker_runs(self, name):
        """How many times the marker command of `name` ran: its marker file's lines (0 when it is absent)."""
        path = self.marker(name)
        return path.read_text().count('ok\n') if path.exists() else 0

    def clear_markers(self):
        for name in PROJECT_MARKERS:
            path = self.marker(name)
            if path.exists():
                path.unlink()

    def shell_files(self):
        """The two start-up files a shell environment policy can point a command's shell at, under `outside`."""
        self.needs_trusted_project()
        return {'zdotdir': self.root / 'outside' / 'zdotdir', 'bash-env': self.root / 'outside' / 'bash-env.sh'}

    def write_shell_files(self):
        files = self.shell_files()
        os.mkdir(files['zdotdir'], 0o700)
        (files['zdotdir'] / '.zshenv').write_text(self.marker_command('zdotdir') + '\n')
        files['bash-env'].write_text(self.marker_command('bash-env') + '\n')

    def write_trust_file(self, relative, text):
        """Write one of `TRUST_FILES` into the project A, replacing what was there."""
        self.needs_trusted_project()
        if relative not in TRUST_FILES:
            raise Refused('a project file off the fixed list: %r' % relative)
        target = self.project / relative
        target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        target.write_text(text)
        return target

    def write_home_file(self, relative, text):
        """Write one of `HOME_FILES` into the Codex home (the person's own settings), for a positive control."""
        self.needs_trusted_project()
        if relative not in HOME_FILES:
            raise Refused('a home file off the fixed list: %r' % relative)
        target = self.home / relative
        target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        target.write_text(text)
        return target

    def other_origin(self):
        return 'http://127.0.0.1:%d' % self.other.port

    # Each builder returns settings as top-level dotted keys and inline tables only, so any of them can be joined.

    def hooks_json(self):
        """`.codex/hooks.json`: one command hook for each of `HOOK_MARKERS`' events, with no matcher."""
        self.needs_trusted_project()
        return json.dumps({'hooks': {event: [{'hooks': [{'type': 'command', 'command': self.marker_command(name),
                                                          'timeout': 5}]}]
                                     for event, name in HOOK_MARKERS.items()}}, indent=2) + '\n'

    def hook_state_toml(self, states):
        """The person's (or, as a test asks, a project's) approval of hooks: `hooks.state.<key>.trusted_hash` for
        each (key, hash) Codex itself reported in `hooks/list`."""
        self.needs_trusted_project()
        return ''.join('hooks.state.%s = { trusted_hash = %s }\n' % (toml_string(k), toml_string(h)) for k, h in states)

    def mcp_toml(self):
        """Two MCP servers: one started as the marker command, one at the second listener's loopback address."""
        argv = self.marker_argv('mcp-stdio')
        return ('mcp_servers.%s = { command = %s, args = [%s], startup_timeout_sec = 5 }\n'
                'mcp_servers.%s = { url = %s, startup_timeout_sec = 5 }\n'
                % (MCP_STDIO, toml_string(argv[0]), ', '.join(toml_string(a) for a in argv[1:]),
                   MCP_HTTP, toml_string(self.other_origin() + '/mcp')))

    def notify_toml(self):
        return 'notify = [%s]\n' % ', '.join(toml_string(a) for a in self.marker_argv('notify'))

    def policy_toml(self):
        """The widest approval, sandbox, network and review routing a project's own settings can name."""
        self.needs_trusted_project()
        return ('approval_policy = "never"\nsandbox_mode = "danger-full-access"\napprovals_reviewer = "auto_review"\n'
                'sandbox_workspace_write.network_access = true\n')

    def provider_toml(self):
        """Another provider and model, at the second listener's loopback address, and the built-in provider's base
        address moved there too."""
        base = toml_string(self.other.base_url)
        return ('model_provider = %s\nmodel = %s\nopenai_base_url = %s\n'
                'model_providers.%s = { name = "Invented other provider", base_url = %s, wire_api = "responses" }\n'
                % (toml_string(OTHER_PROVIDER), toml_string(OTHER_MODEL), base, OTHER_PROVIDER, base))

    def developer_toml(self):
        self.needs_trusted_project()
        return 'developer_instructions = %s\n' % toml_string(self.trust_markers['project'])

    def shell_env_toml(self):
        """A variable of the fixture's own, and the two start-up files a command's shell would read."""
        files = self.shell_files()
        return ('shell_environment_policy.set = { %s = %s, ZDOTDIR = %s, BASH_ENV = %s }\n'
                % (TRUST_ENV, toml_string(self.trust_markers['project']), toml_string(files['zdotdir']),
                   toml_string(files['bash-env'])))

    def permissions_toml(self):
        self.needs_trusted_project()
        return 'default_permissions = ":danger-full-access"\n'

    def thread_store_toml(self):
        return 'experimental_thread_store_endpoint = %s\n' % toml_string(self.other_origin())

    def rules_text(self):
        """An exec-policy rule allowing the fixture's `touch`, by its path and by its name."""
        self.needs_trusted_project()
        return ('prefix_rule(pattern = ["/usr/bin/touch"], decision = "allow")\n'
                'prefix_rule(pattern = ["touch"], decision = "allow")\n')

    def person_mcp_toml(self):
        """For the person's own settings: a server with the same name as the project's stdio server, and one of
        the person's own, each started as a marker command of its own."""
        same, other = self.marker_argv('mcp-person-same'), self.marker_argv('mcp-person-other')
        return ''.join('mcp_servers.%s = { command = %s, args = [%s], startup_timeout_sec = 5 }\n'
                       % (name, toml_string(argv[0]), ', '.join(toml_string(a) for a in argv[1:]))
                       for name, argv in ((MCP_STDIO, same), (MCP_PERSON, other)))

    def headers_helper_toml(self):
        """An HTTP MCP server at the second listener's loopback address whose headers come from a helper command,
        the marker command (run by Codex as `sh -c <command>`)."""
        return ('mcp_servers.%s = { url = %s, http_headers_helper = %s, startup_timeout_sec = 5 }\n'
                % (MCP_HELPER, toml_string(self.other_origin() + '/mcp-helper'),
                   toml_string(self.marker_command('mcp-headers-helper'))))

    def malformed_toml(self):
        """A settings file that is not TOML at all."""
        self.needs_trusted_project()
        return 'this is = = not toml\n'

    def agents_md(self, which):
        """The text of the project's own `AGENTS.md` ('root') or of the nested `sub/AGENTS.md` ('sub')."""
        self.needs_trusted_project()
        return '# Invented instructions for a fixture\n\n%s\n' % self.trust_markers['agents-' + which]

    def subfolder(self):
        self.needs_trusted_project()
        return self.project / SUBFOLDER

    def denied_read_folder(self):
        """An invented folder under `outside`, made empty on first use, that a permissions profile may deny reading."""
        self.needs_trusted_project()
        folder = self.root / 'outside' / 'denied-read'
        if not folder.exists():
            os.mkdir(folder, 0o700)
        return folder

    def entry_operations(self):
        """With `working_files`: commands that change the directory entry naming Codex's temporary folder, or an
        ancestor's entry, each with the exact line the sandbox's refusal of its first step prints. Each is
        attempted whole; where the first step is refused, the later ones never run. No `rm` is used."""
        if not self.working_files:
            return {}
        q = lambda path: shlex.quote(str(path))  # noqa: E731
        t, p, w = self.tmpdir, self.codex_tmp, self.working
        moved = lambda path, suffix: path.with_name(path.name + suffix)  # noqa: E731

        def mv(src, dst):
            return 'mv %s %s' % (q(src), q(dst)), 'mv: rename %s to %s: Operation not permitted' % (src, dst)

        def rmdir(path):
            return 'rmdir %s' % q(path), 'rmdir: %s: Operation not permitted' % path

        def ln(target, link):
            return 'ln -s %s %s' % (q(target), q(link)), 'ln: %s: Operation not permitted' % link

        ops = {
            'entry-t-rename': mv(t, moved(t, '.moved')),
            'entry-t-remake': (rmdir(t)[0] + ' && mkdir ' + q(t), rmdir(t)[1]),
            'entry-t-link': (mv(t, moved(t, '.aside'))[0] + ' && ln -s %s %s' % (q(moved(t, '.aside')), q(t)),
                             mv(t, moved(t, '.aside'))[1]),
            'entry-p-new-link': ln(t, p / 'x-link'),
            'entry-p-rename': mv(p, moved(p, '.moved')),
            'entry-p-remove': rmdir(p),
            'entry-p-link': (mv(p, moved(p, '.aside'))[0] + ' && ln -s %s %s' % (q(moved(p, '.aside')), q(p)),
                             mv(p, moved(p, '.aside'))[1]),
            'entry-w-rename': mv(w, moved(w, '.moved')),
            'entry-w-new-link': ln(p, w / 'x-link'),
        }
        return {key: (command, Lines({line})) for key, (command, line) in ops.items()}

    def entries(self):
        """Identity of each folder on the temporary folder's path, from the run's root down, and the names each of
        the App's folders holds: what an entry operation would change."""
        folders = [self.root, self.data, self.working, self.codex_tmp, self.tmpdir]
        ident = {}
        for folder in folders:
            st = os.lstat(folder)
            ident[str(folder)] = (st.st_dev, st.st_ino, stat.S_IFMT(st.st_mode))
        names = {str(f): sorted(os.listdir(f)) for f in (self.root, self.working, self.codex_tmp)}
        return ident, names


class Client:
    def __init__(self, run):
        """Start the app server. Until it is returned, nobody holds it to stop it: if anything fails after it has
        started, its whole process group is ended and its pipes closed here before the error is raised."""
        self.run = run
        self.stderr = open(run.root / ('codex-stderr-%d.log' % len(run.clients)), 'wb')
        try:
            self.proc = subprocess.Popen(
                [run.binary, '-c', 'analytics.enabled=false', '-c', 'model_provider="openai"',
                 '-c', 'openai_base_url="%s"' % run.stub.base_url, 'app-server'],
                cwd=str(run.project), env=run.environment(), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=self.stderr, start_new_session=True)
        except BaseException:
            self.stderr.close()
            raise
        self.pgid = self.proc.pid  # its own session, so its own process group
        try:
            try:  # when it started, so that its number is not mistaken for another process's later
                self.started_at = observe_process(self.proc.pid)[1]
            except Unobserved:
                self.started_at = None
            self.lock = threading.Lock()
            self.changed = threading.Condition(self.lock)
            self.next_id = 0
            self.replies = {}
            self.notes = []
            self.server_requests = []  # {'method', 'thread', 'id', 'params'}; params kept in memory only
            self.tool_call_policy = 'answer'  # 'answer' or 'hold'
            self.held = []
            self.writer = threading.Lock()
            self.reader_end = None  # set by read(): 'eof', or the error that stopped it
            self.reader = threading.Thread(target=self.read, daemon=True)
            self.reader.start()
        except BaseException:
            self.abandon()
            raise

    def abandon(self):
        """End a server that failed to be set up: signal its whole process group, reap it, close its pipes. Each
        step is attempted whatever the one before it did."""
        try:
            os.killpg(self.pgid, signal.SIGKILL)
        except OSError:
            pass
        try:
            self.proc.wait(5)
        except Exception:  # noqa: BLE001 - the pipes are closed whatever happened here
            pass
        for stream in (self.proc.stdin, self.proc.stdout, self.stderr):
            try:
                stream.close()
            except (OSError, ValueError, AttributeError):
                pass

    def read(self):
        """Take every frame until the server's output ends. How it ended is kept: 'eof' when the output reached its
        end, or the error that stopped it, so that `drain` can tell the two apart."""
        try:
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
            self.reader_end = 'eof'
        except BaseException as error:  # noqa: BLE001 - kept for drain() to report
            self.reader_end = error
        finally:
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
        self.drain()  # every frame the server wrote is taken before its output is closed
        self.close_pipes()

    def kill_group(self):
        try:
            os.killpg(self.pgid, signal.SIGKILL)
        except ProcessLookupError:  # the group is gone
            pass
        except PermissionError:  # macOS answers so for a group whose members have all exited and await reaping
            if group_members(self.pgid):
                raise
        if self.proc.poll() is None:
            self.proc.wait(5)

    def drain(self, timeout=10):
        """After the server has ended: wait until the reader has taken every frame up to the end of its output, so
        an absence asserted afterwards covers the server's whole life. A reader that stopped for any reason other
        than the end of the output fails, with that reason."""
        self.reader.join(timeout)
        if self.reader.is_alive():
            raise Refused('the reader did not reach the end of the server output')
        if self.reader_end != 'eof':
            raise Refused('the reader stopped before the end of the server output: %r' % (self.reader_end,))

    def close_pipes(self):
        for stream in (self.proc.stdin, self.proc.stdout, self.stderr):
            try:
                stream.close()
            except (OSError, ValueError):
                pass

    def kill(self):
        """End the app server and its group at once, as a quit or crash would."""
        self.kill_group()
