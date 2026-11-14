"""The stub provider, run as its own process, against invented requests. No
Codex, no App and no model: each case sends what the case names and reads the
stream and the request log back."""
import http.client
import json
import os
import signal
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

STUB = Path(__file__).resolve().parent / 'stub_provider.py'


def request(text, role='user', extra=()):
    return {'model': 'invented-model', 'stream': True, 'input': [
        {'type': 'message', 'role': 'developer', 'content': [{'type': 'input_text', 'text': 'invented guidance'}]},
        {'type': 'message', 'role': 'user', 'content': [{'type': 'input_text', 'text': '<environment_context>x</environment_context>'}]},
        *extra,
        {'type': 'message', 'role': role, 'content': [{'type': 'input_text', 'text': text}]}]}


def events(raw):
    out = []
    for block in raw.decode().split('\n\n'):
        lines = dict(l.split(': ', 1) for l in block.splitlines() if ': ' in l)
        if 'event' in lines:
            out.append((lines['event'], json.loads(lines['data'])))
    return out


class StubProvider(unittest.TestCase):
    def start(self, *args):
        self.tmp = tempfile.TemporaryDirectory()
        self.record = Path(self.tmp.name) / 'record'
        self.record.mkdir()
        self.ready = self.record / 'stub-ready.json'
        self.proc = subprocess.Popen([sys.executable, '-I', str(STUB), '--record', str(self.record), '--ready', str(self.ready), *args],
                                     start_new_session=True, stderr=subprocess.PIPE)
        deadline = time.monotonic() + 10
        while not self.ready.exists():
            self.assertIsNone(self.proc.poll(), 'the stub exited before it was ready')
            self.assertLess(time.monotonic(), deadline, 'the stub was not ready in 10 s')
            time.sleep(0.02)
        self.info = json.loads(self.ready.read_text())
        self.addCleanup(self.finish)

    def finish(self):
        if self.proc.poll() is None:
            self.proc.kill()
            self.proc.wait()
        self.proc.stderr.close()
        self.tmp.cleanup()

    def stop(self):
        self.proc.send_signal(signal.SIGTERM)
        self.assertEqual(self.proc.wait(timeout=10), 0)

    def log(self):
        return [json.loads(l) for l in (self.record / 'stub-requests.jsonl').read_text().splitlines()]

    def post(self, body, path='/v1/responses'):
        conn = http.client.HTTPConnection('127.0.0.1', self.info['port'], timeout=10)
        conn.request('POST', path, json.dumps(body), {'Content-Type': 'application/json', 'Authorization': 'invented-not-a-key'})
        return conn, conn.getresponse()

    def test_ready_file_names_the_address_the_app_is_given(self):
        self.start()
        self.assertEqual(self.info['pid'], self.proc.pid)
        self.assertEqual(self.info['base_url'], 'http://127.0.0.1:%d/v1' % self.info['port'])
        self.assertEqual(list(self.record.glob('*.tmp')), [])

    def test_a_turn_completes_with_the_fixed_reply_and_no_tool_call(self):
        self.start()
        conn, resp = self.post(request('first message'))
        self.assertEqual((resp.status, resp.getheader('Content-Type')), (200, 'text/event-stream'))
        got = events(resp.read())
        conn.close()
        self.assertEqual([e for e, _ in got], ['response.created', 'response.output_item.added', 'response.output_text.delta',
                                               'response.output_item.done', 'response.completed'])
        self.assertEqual(got[2][1]['delta'], 'Invented reply from the stub provider.')
        self.assertTrue(all(d.get('item', {}).get('type', 'message') == 'message' for _, d in got))
        self.stop()
        self.assertEqual([(l['method'], l['path'], l['disposition']) for l in self.log()], [('POST', '/v1/responses', 'completed')])

    def test_a_hold_is_keyed_by_the_last_user_message_only(self):
        self.start('--hold-bound', '0.5')
        earlier = ({'type': 'message', 'role': 'user', 'content': [{'type': 'input_text', 'text': 'STUB-HOLD earlier'}]},
                   {'type': 'message', 'role': 'assistant', 'content': [{'type': 'output_text', 'text': 'x'}]})
        conn, resp = self.post(request('later, no marker', extra=earlier))
        self.assertEqual(events(resp.read())[-1][0], 'response.completed')
        conn.close()
        conn, resp = self.post(request('please STUB-HOLD this'))
        self.assertEqual([e for e, _ in events(resp.read())], ['response.created'])
        conn.close()
        self.stop()
        self.assertEqual([l['disposition'] for l in self.log()], ['completed', 'held-bound-reached'])

    def test_a_held_turn_ends_when_the_client_closes_it(self):
        self.start()
        sock = socket.create_connection(('127.0.0.1', self.info['port']), timeout=10)
        body = json.dumps(request('STUB-HOLD')).encode()
        sock.sendall(b'POST /v1/responses HTTP/1.1\r\nHost: x\r\nContent-Type: application/json\r\nContent-Length: %d\r\n\r\n' % len(body) + body)
        seen = b''
        while b'response.created' not in seen:
            seen += sock.recv(4096)
        sock.close()
        deadline = time.monotonic() + 5
        while not (self.record / 'stub-requests.jsonl').exists():
            self.assertLess(time.monotonic(), deadline, 'the hold did not end when the client closed')
            time.sleep(0.05)
        self.assertEqual([l['disposition'] for l in self.log()], ['held-ended-by-client'])
        self.stop()

    def test_stopping_ends_a_held_turn_and_writes_its_line(self):
        self.start()
        conn, resp = self.post(request('STUB-HOLD'))
        self.assertEqual(resp.status, 200)
        time.sleep(0.3)
        self.stop()
        self.assertEqual([l['disposition'] for l in self.log()], ['held-ended-by-stop'])
        conn.close()

    def test_a_websocket_upgrade_is_refused_with_the_chosen_status(self):
        self.start('--websocket-status', '426')
        conn = http.client.HTTPConnection('127.0.0.1', self.info['port'], timeout=10)
        conn.request('GET', '/v1/responses', headers={'Upgrade': 'websocket', 'Connection': 'Upgrade'})
        self.assertEqual(conn.getresponse().status, 426)
        conn.close()
        self.stop()
        self.assertEqual([l['disposition'] for l in self.log()], ['websocket-refused'])

    def test_anything_else_is_404_and_logged_as_unexpected(self):
        self.start()
        for method, path in (('GET', '/v1/models'), ('POST', '/v1/chat/completions'), ('GET', '/v1/responses')):
            conn = http.client.HTTPConnection('127.0.0.1', self.info['port'], timeout=10)
            conn.request(method, path, body='{}' if method == 'POST' else None)
            self.assertEqual(conn.getresponse().status, 404)
            conn.close()
        self.stop()
        self.assertEqual([l['disposition'] for l in self.log()], ['unexpected'] * 3)

    def test_the_log_carries_no_body_prompt_or_header_value(self):
        self.start('--hold-bound', '0.2')
        for text in ('INVENTED-PROMPT-TEXT', 'INVENTED-PROMPT-TEXT STUB-HOLD'):
            conn, resp = self.post(request(text))
            resp.read()
            conn.close()
        self.stop()
        raw = (self.record / 'stub-requests.jsonl').read_text()
        self.assertNotIn('INVENTED-PROMPT-TEXT', raw)
        self.assertNotIn('invented-not-a-key', raw)
        self.assertIn('authorization', raw, 'header names are kept')
        self.assertEqual({tuple(sorted(l)) for l in self.log()}, {('disposition', 'header_names', 'method', 'path', 't')})

    def test_it_listens_on_loopback_only(self):
        self.start()
        listening = subprocess.run(['lsof', '-nP', '-a', '-p', str(self.proc.pid), '-iTCP', '-sTCP:LISTEN'],
                                   capture_output=True, text=True).stdout if os.path.exists('/usr/sbin/lsof') else None
        if listening is not None:
            self.assertIn('127.0.0.1:%d' % self.info['port'], listening)
            self.assertNotIn('*:%d' % self.info['port'], listening)
        self.stop()

    def test_a_record_that_is_not_a_folder_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            done = subprocess.run([sys.executable, '-I', str(STUB), '--record', str(Path(tmp) / 'absent'), '--ready', str(Path(tmp) / 'r')],
                                  capture_output=True, text=True, timeout=10)
            self.assertEqual(done.returncode, 2)
            self.assertFalse((Path(tmp) / 'r').exists())


if __name__ == '__main__':
    unittest.main()
