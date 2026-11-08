"""Bounded development-only visual operator session. Import performs no OS/UI work.

One reviewed 66d39df5/75e953fe development App, launched and cleaned up through
the UNCHANGED j1_stage_a_phase.NativeSession (admit/launch_once/bind_cleanup/
check/normal_terminate/absent/hold_until_absent/verify_saved). The operator (a
parent agent) inspects numbered screenshots and sends one JSON command per line
on stdin; each input command consumes the permission of one fresh frame.

Not a generic automation framework, AX parser, private App IPC or model/API
service. CoreGraphics posting returns void: dispatch is reported as attempted
and handling as unknown. Native calls are cooperative; deadlines are checked
between them and overrun is reported, never hidden. Running this file is a
separately approved live act; tool approval is not desktop availability or GO.
"""
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
import argparse
import ctypes as C
import hashlib
import json
import math
import os
import re
import select
import stat
import sys
import time
import types

WORK = Path(__file__).resolve().parent
CORE_SHA = 'f510d9be6a4e2e8d8eb77f25642e1f16a33f13c8d909898ff7f71ff6f6a3ccdc'
READER_SHA = 'fd37834b301f138963cdfe76f8bf3a146aea373b99ab2c994546ff73c939af19'
RECEIPT_PATH = '/Users/ryan/dev/chirality-t3/scratch/app-native-visual-current-subject-hoamd1ib/preflight-current.json'
RECEIPT_SHA = '5567d97631e281a82c2682c60f73798439534a9a54611ed11655e42e5bb6034b'
EXACT_PROJECT = '/Users/ryan/dev/chirality-t3/scratch/app-j1-owner-reviewed-naw71ke6/session/project'
_CANDIDATE = ('/Users/ryan/dev/chirality-t3/scratch/app-dev-candidate-20261107-75f470c7-kr7swwbe/target/debug/'
              'bundle/macos/Chirality App v4 (development 20261107-75f470c7).app')
REVIEWED_SUBJECT = {
    'source': '66d39df5da20f15b0d706f6813e2a38fee02d81f',
    'bundle': _CANDIDATE,
    'identifier': 'dev.chirality.app-v4.candidate.20261107-75f470c7',
    'executable': _CANDIDATE + '/Contents/MacOS/chirality-app-v4',
    'executable_sha256': '75e953fe235961cea186289bd6112951b1ecbbe1d203858dce8863605463b546',
    'packet': '/Users/ryan/dev/chirality-t3/scratch/app-j1-owner-reviewed-naw71ke6',
}

# New-session caps only. The frozen StageA 180/110 and entry 185 budgets are untouched.
TOTAL_CAP = 600
UI_CAP = 480
CLEANUP_RESERVE = 120
MIN_UI = 180
WAIT_MAX = 10
FRAME_MAX_AGE = 60
CAPTURE_TIMEOUT = 5
MAX_LINE = 4096
MAX_FRAMES = 120
MAX_INPUTS = 60
MAX_PNG = 64 * 1024 * 1024
UTF16_CHUNK = 20  # CGEventKeyboardSetUnicodeString documented practical limit
# Ordinary folder-selection keys only: (virtual key, CGEventFlags).
KEYS = {'go_to_folder': (0x05, 0x120000),  # Cmd+Shift+G
        'select_all': (0x00, 0x100000),    # Cmd+A
        'return': (0x24, 0x0)}
UTC_FORMAT = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z')
LIMITS = ('Frames request the selected original-App window, not a whole display; attached-window '
          'composition is unproved. Frames and AppKit foreground facts are point-in-time observations and do not prove machine '
          'isolation, occlusion freedom, event routing or App handling. CGEventPostToPid is void: dispatch '
          'attempted, handling unknown. Deadlines are cooperative between native calls. Original-birth absence '
          'alone closes the session; terminate BOOL, deadlines and exit status never do.')


class SessionStop(RuntimeError):
    """Fatal: end input and run normal cleanup."""


class ActionRefused(RuntimeError):
    """Non-fatal: this command is refused; the session continues."""


class SessionSignal(BaseException):
    pass


def stop_unless(ok, why):
    if not ok:
        raise SessionStop(why)


def refuse_unless(ok, why):
    if not ok:
        raise ActionRefused(why)


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


# ---------------------------------------------------------------- source binding

def load_core(work=WORK):
    """Load the exact reviewed j1_stage_a_phase bytes; never a substitute."""
    path = Path(work) / 'j1_stage_a_phase.py'
    raw = path.read_bytes()
    stop_unless(sha256(raw) == CORE_SHA, 'reviewed j1_stage_a_phase bytes changed')
    stop_unless(sha256((Path(work) / 'native_b_diagnostic.py').read_bytes()) == READER_SHA,
                'reviewed native_b_diagnostic bytes changed')
    existing = sys.modules.get('j1_stage_a_phase')
    if existing is not None:
        stop_unless(Path(existing.__file__).resolve() == path.resolve(), 'refuse a different loaded core module')
        return existing
    module = types.ModuleType('j1_stage_a_phase')
    module.__file__ = str(path)
    sys.modules['j1_stage_a_phase'] = module  # dataclasses resolve their module here
    exec(compile(raw, str(path), 'exec'), module.__dict__)
    return module


def load_reader(work=WORK):
    """Private copy of the exact owned-window reader, as NativeSession.admit loads it."""
    path = Path(work) / 'native_b_diagnostic.py'
    raw = path.read_bytes()
    stop_unless(sha256(raw) == READER_SHA, 'reviewed native_b_diagnostic bytes changed')
    module = types.ModuleType('visual_reviewed_window_reader')
    module.__file__ = str(path)
    exec(compile(raw, str(path), 'exec'), module.__dict__)
    return module


def parse_owner_end(text):
    stop_unless(isinstance(text, str) and UTC_FORMAT.fullmatch(text), 'explicit UTC owner-window-end ending in Z required')
    try:
        value = datetime.fromisoformat(text)
    except ValueError:
        raise SessionStop('invalid UTC owner-window-end') from None
    stop_unless(value.utcoffset() == timedelta(0), 'owner-window-end must be UTC')
    return value


def reviewed_subject(core, preflight, home=None):
    for key, expected in REVIEWED_SUBJECT.items():
        stop_unless(preflight.get(key) == expected, 'reviewed subject differs: ' + key)
    stop_unless(preflight.get('ready') is True and preflight.get('refusals') == [], 'reviewed receipt not ready')
    project = preflight['packet'] + '/session/project'
    stop_unless(project == EXACT_PROJECT, 'exact invented project differs')
    home = Path.home() if home is None else Path(home)
    return core.Subject(source=preflight['source'], bundle=preflight['bundle'], identifier=preflight['identifier'],
                        executable=preflight['executable'], executable_sha256=preflight['executable_sha256'],
                        project=project, app_data=str(home / 'Library/Application Support' / preflight['identifier']))


# ---------------------------------------------------------------- commands

def _frame(value):
    refuse_unless(type(value) is int and 1 <= value <= MAX_FRAMES, 'frame must be a current frame number')
    return value


def _pixel(value):
    refuse_unless(type(value) is int and 0 <= value < 100000, 'pixel coordinate must be a nonnegative integer')
    return value


def _location(value):
    refuse_unless(isinstance(value, str) and 0 < len(value) <= 1024 and '\x00' not in value
                  and value.startswith('/'), 'location must be an absolute bounded path string')
    return value


def _key(value):
    refuse_unless(isinstance(value, str) and value in KEYS, 'key not allowed')
    return value


def _seconds(value):
    refuse_unless(type(value) in (int, float) and math.isfinite(value) and 0 < value <= WAIT_MAX,
                  'wait seconds must be in (0, 10]')
    return float(value)


SCHEMA = {
    'capture': {},
    'click': {'frame': _frame, 'x': _pixel, 'y': _pixel},
    'key': {'frame': _frame, 'key': _key},
    'type_project': {'frame': _frame},
    'activate': {'frame': _frame},
    'confirm_first_effect': {'frame': _frame},
    'wait': {'seconds': _seconds},
    'expected_effects': {'settings_folder': _location, 'sign_in_folder': _location},
    'verify_saved': {},
    'status': {},
    'quit': {},
}


def parse_command(line):
    """One JSON object; fixed op set; exact keys; no code, shell, PID or free text."""
    refuse_unless(isinstance(line, bytes) and len(line) <= MAX_LINE, 'command exceeds bound')

    def unique(pairs):
        keys = [k for k, _ in pairs]
        refuse_unless(len(keys) == len(set(keys)), 'duplicate command key')
        return dict(pairs)
    try:
        value = json.loads(line.decode('utf-8'), object_pairs_hook=unique)
    except (UnicodeDecodeError, ValueError):
        raise ActionRefused('command is not one UTF-8 JSON object') from None
    refuse_unless(isinstance(value, dict) and isinstance(value.get('op'), str), 'command object with op required')
    fields = SCHEMA.get(value['op'])
    refuse_unless(fields is not None, 'unknown op')
    refuse_unless(set(value) == {'op', *fields}, 'command keys differ from schema')
    return {'op': value['op'], **{k: check(value[k]) for k, check in fields.items()}}


class LineReader:
    """Bounded stdin lines; wakes at the caller's timeout instead of blocking forever."""
    TIMEOUT, EOF = 'timeout', 'eof'

    def __init__(self, fd, limit=MAX_LINE):
        self.fd, self.limit, self.buffer, self.closed = fd, limit, b'', False

    def read(self, timeout):
        end = time.monotonic() + max(0.0, timeout)
        while True:
            if b'\n' in self.buffer:
                line, _, self.buffer = self.buffer.partition(b'\n')
                stop_unless(len(line) <= self.limit, 'command line exceeds bound')
                return line
            stop_unless(len(self.buffer) <= self.limit, 'command line exceeds bound')
            if self.closed:
                return self.EOF  # an unterminated partial line is discarded
            ready, _, _ = select.select([self.fd], [], [], max(0.0, end - time.monotonic()))
            if not ready:
                return self.TIMEOUT
            chunk = os.read(self.fd, 4096)
            if not chunk:
                self.closed = True
            self.buffer += chunk


class LineWriter:
    def __init__(self, stream):
        self.stream = stream

    def write(self, value):
        try:
            self.stream.write(json.dumps(value, sort_keys=True) + '\n')
            self.stream.flush()
        except (OSError, ValueError) as error:
            raise SessionStop('operator output unavailable: ' + type(error).__name__) from None


# ---------------------------------------------------------------- geometry

def png_size(raw):
    stop_unless(len(raw) >= 24 and raw[:8] == b'\x89PNG\r\n\x1a\n' and raw[12:16] == b'IHDR', 'capture is not PNG')
    width, height = int.from_bytes(raw[16:20], 'big'), int.from_bytes(raw[20:24], 'big')
    stop_unless(0 < width <= 20000 and 0 < height <= 20000, 'capture dimensions invalid')
    return width, height


def window_id(number):
    """CGWindowID from a reader row's kCGWindowNumber, or None when not an exact nonzero uint32."""
    if type(number) in (int, float) and math.isfinite(number) and number == int(number) and 0 < number < 2 ** 32:
        return int(number)
    return None


def owned_windows(rows):
    result = []
    for row in rows:
        b = row['bounds']
        rect = [b.get('X'), b.get('Y'), b.get('Width'), b.get('Height')]
        sane = all(type(v) in (int, float) and math.isfinite(v) for v in rect) and rect[2] > 0 and rect[3] > 0
        result.append({'number': row['number'], 'layer': row['layer'], 'bounds': rect, 'on_screen': row['on_screen'],
                       'targetable': bool(sane and row['on_screen'] is True and row['layer'] == 0
                                          and window_id(row['number']) is not None)})
    return result


def capture_plan(windows):
    """The frontmost targetable original-PID window (WindowServer order), or None. Never a fallback."""
    for window in windows:  # rows were filtered to the original PID before decoding
        if window['targetable']:
            return {'window_id': window_id(window['number']), 'number': window['number'],
                    'bounds': list(window['bounds'])}
    return None


def window_geometry(plan, pixels):
    """Selected-window capture pixels -> global CG points from that window's own origin.

    The PNG must be exactly the window's CG bounds at one 1x/2x scale on both axes;
    any other size (shadow, attached overhang, crop, mixed scale) is ambiguous and refuses.
    Origins may be nonzero or negative (any display arrangement).
    """
    x, y, width, height = plan['bounds']
    numbers = [x, y, width, height, *pixels]
    refuse_unless(len(pixels) == 2 and all(type(v) in (int, float) and math.isfinite(v) for v in numbers)
                  and width > 0 and height > 0, 'window capture geometry invalid')
    scale_x, scale_y = pixels[0] / width, pixels[1] / height
    refuse_unless(scale_x == scale_y and scale_x in (1.0, 2.0),
                  'capture size is not the exact original window bounds at one 1x/2x scale')
    return {'basis': 'original-window', 'window_id': plan['window_id'], 'origin_points': [x, y],
            'size_points': [width, height], 'pixels': list(pixels), 'scale': scale_x, 'whole_display': False}


def capture_local(geometry, bounds):
    """Global CG point rectangle -> pixel rectangle local to this window capture (may lie outside it)."""
    s, (ox, oy) = geometry['scale'], geometry['origin_points']
    return [(bounds[0] - ox) * s, (bounds[1] - oy) * s, bounds[2] * s, bounds[3] * s]


def map_target(frame, x, y):
    """Capture-local pixel -> global point inside the captured original-App window only."""
    geometry = frame.geometry
    refuse_unless(geometry is not None, 'frame geometry unavailable')
    refuse_unless(0 <= x < geometry['pixels'][0] and 0 <= y < geometry['pixels'][1],
                  'target outside captured original window pixels')
    gx = geometry['origin_points'][0] + x / geometry['scale']
    gy = geometry['origin_points'][1] + y / geometry['scale']
    plan = capture_plan(frame.windows)
    refuse_unless(plan is not None and plan['window_id'] == geometry['window_id']
                  and plan['bounds'] == geometry['origin_points'] + geometry['size_points'],
                  'captured window is not the frame\'s frontmost original window')
    wx, wy, ww, wh = plan['bounds']
    refuse_unless(wx <= gx < wx + ww and wy <= gy < wy + wh, 'target outside captured original window')
    window = next(w for w in frame.windows if w['targetable'])
    return gx, gy, window


def utf16_chunks(text, limit=UTF16_CHUNK):
    """Literal UTF-16 code units, never splitting a surrogate pair."""
    units = list(memoryview(text.encode('utf-16-le')).cast('H'))
    chunks, start = [], 0
    while start < len(units):
        end = min(start + limit, len(units))
        if end < len(units) and 0xD800 <= units[end - 1] <= 0xDBFF:
            end -= 1
        chunks.append(tuple(units[start:end]))
        start = end
    return chunks


# ---------------------------------------------------------------- input pairing

class Gesture:
    """Paired down/up posting to the original PID with guaranteed CF release."""

    def __init__(self, api):
        self.api = api
        self.state = {'pairs': 0, 'allocated': 0, 'down_attempted': 0, 'up_attempted': 0,
                      'release_errors': [], 'dispatch': 'not attempted', 'handling': 'unknown'}

    def run(self, pid, specs, full_check, birth_check):
        allocated = []
        try:
            source = self.api.source()
            stop_unless(source, 'private event source allocation failed')
            allocated.append(source)
            pairs = []
            for spec in specs:
                pair = []
                for down in (True, False):
                    event = self.api.event(source, spec, down)
                    stop_unless(event, 'event allocation failed')
                    allocated.append(event)
                    pair.append(event)
                pairs.append(pair)
            self.state.update(pairs=len(pairs), allocated=len(allocated))
            for index, (down, up) in enumerate(pairs):
                if index:
                    birth_check()
                full_check()  # after allocation, and before every new down/chunk
                self.state['down_attempted'] += 1
                self.state['dispatch'] = 'attempted'
                try:
                    self.api.post(pid, down)
                finally:
                    # Pair the release even after a post error, but only to the SAME birth.
                    birth_check()
                    self.state['up_attempted'] += 1
                    self.api.post(pid, up)
            return dict(self.state)
        finally:
            errors = []
            for value in reversed(allocated):
                try:
                    self.api.release(value)
                except BaseException as error:
                    errors.append(type(error).__name__)
            self.state['release_errors'] = errors
            if errors:
                raise SessionStop('CF release failed')


# ---------------------------------------------------------------- session

@dataclass
class Frame:
    number: int
    taken: float
    path: str
    sha256: str
    pixels: tuple
    geometry: object
    windows: list
    foreground: bool
    actionable: bool
    reasons: list
    inputs_before: int
    consumed: bool = False
    facts: dict = field(default_factory=dict, repr=False)


class VisualSession:
    def __init__(self, core, subject, io, adapter_factory, window_reader, record, owner_end, commands, output,
                 clock=time.monotonic, utc=lambda: datetime.now(timezone.utc), sleep=time.sleep):
        self.core, self.subject, self.io, self.adapter_factory = core, subject, io, adapter_factory
        self.window_reader, self.record, self.owner_end = window_reader, record, owner_end
        self.commands, self.output, self.clock, self.utc, self.sleep = commands, output, clock, utc, sleep
        self.used, self.closing = False, False
        self.adapter, self.identity, self.t0 = None, None, None
        self.frames, self.actions = [], []
        self.inputs, self.activated, self.first_confirmed = 0, False, False
        self.locations, self.saved_used = None, False
        self.stop_reason = None

    # -- time
    def owner_left(self):
        return (self.owner_end - self.utc()).total_seconds()

    def ui_left(self):
        return min(self.t0 + UI_CAP - self.clock(), self.owner_left() - CLEANUP_RESERVE)

    def total_left(self):
        return min(self.t0 + TOTAL_CAP - self.clock(), self.owner_left())

    def require_time(self):
        stop_unless(self.ui_left() > 0, 'UI cutoff')

    def emit(self, value):
        self.output.write(dict(value, ui_seconds_left=round(self.ui_left(), 3)))

    # -- facts
    def expected_app(self):
        return {'pid': self.identity['pid'], 'bundle_identifier': self.subject.identifier,
                'executable': self.subject.executable}

    def facts(self):
        foreground = self.adapter.foreground(self.identity)
        stop_unless(foreground['correspondence'] == self.expected_app(), 'AppKit correspondence differs from original')
        inventory = self.window_reader.window_inventory(self.io.backend, self.identity['pid'], self.require_time)
        return {'foreground': foreground, 'windows': owned_windows(inventory['rows'])}

    def is_foreground(self, facts):
        f = facts['foreground']
        return f['active'] is True and f['frontmost_pid'] == self.identity['pid']

    def birth_check(self):
        stop_unless(self.io.backend.identity(self.identity['pid']) == self.identity, 'original birth changed; no input')

    # -- lifecycle
    def start(self, result):
        left = self.ui_left()
        if left < MIN_UI:
            self.record('window-refusal', {'owner_window_end': self.owner_end.isoformat(), 'ui_seconds_left': left,
                                           'minimum_ui_seconds': MIN_UI, 'cleanup_reserve': CLEANUP_RESERVE})
            raise SessionStop('stale/insufficient owner window; no App operation')
        self.adapter = self.adapter_factory()
        preflight = dict(self.adapter.preflight())
        self.record('visual-preflight', {'no_prompt': True, **preflight})
        stop_unless(set(preflight) == {'screen_capture', 'post_event', 'ax_trusted'}
                    and all(v is True for v in preflight.values()), 'no-prompt capture/posting/trust preflight false')
        self.io.admit(self.subject)
        stop_unless(self.ui_left() >= MIN_UI, 'insufficient UI time remains before launch')
        self.identity = self.io.launch_once(self.subject)
        result['launches'] = 1
        self.io.bind_cleanup(self.identity, self.subject)  # before any UI operation
        self.emit({'event': 'ready', 'pid': self.identity['pid'], 'ops': sorted(SCHEMA),
                   'frame_max_age': FRAME_MAX_AGE, 'limits': LIMITS})

    def loop(self):
        while True:
            left = self.ui_left()
            if left <= 0:
                self.stop_reason = 'ui-cutoff'
                return
            line = self.commands.read(left)
            if line == LineReader.TIMEOUT:
                continue
            if line == LineReader.EOF:
                self.stop_reason = 'eof'
                return
            op = None
            try:
                command = parse_command(line)
                op = command['op']
                if op == 'quit':
                    self.stop_reason = 'operator-quit'
                    return
                response = getattr(self, 'op_' + command['op'])(command)
                self.emit({'op': command['op'], 'ok': True, **response})
            except ActionRefused as refusal:
                self.emit({'op': op, 'ok': False, 'refused': str(refusal)})

    def run(self):
        stop_unless(not self.used, 'one session only; no rearm or retry')
        self.used = True
        self.t0 = self.clock()
        result = {'format': 'chirality.app.native-visual-session/v1', 'source': self.subject.source,
                  'launches': 0, 'setup_saved': False, 'J1_complete': False, 'qualification': False,
                  'handling': 'unknown', 'limits': LIMITS}
        try:
            self.start(result)
            self.loop()
        except BaseException as error:
            result['session_error'] = repr(error)[:400]
        finally:
            self.cleanup(result)
        return result

    def cleanup(self, result):
        """Normal original cleanup without any parent roundtrip; absence alone closes."""
        self.closing = True
        evidence_errors = []
        try:
            try:
                self.output.write({'event': 'closing', 'reason': self.stop_reason or 'error', 'no_more_input': True})
            except BaseException:
                pass
            if self.identity is None:
                self.identity = getattr(self.io, 'identity', None)
            if self.identity is not None:
                result['launches'] = 1
                result['cleanup_started'] = self.clock() - self.t0
                self.core.cleanup_receipt(self.record, 'cleanup-intent',
                                          {'original': self.identity, 'reason': self.stop_reason,
                                           'mechanism': 'normal NSRunningApplication terminate',
                                           'no_parent_roundtrip': True}, evidence_errors)
                try:
                    self.io.check(self.identity)
                    result['terminate_BOOL'] = self.io.normal_terminate(self.identity, self.subject)
                except BaseException as error:
                    result['cleanup_error'] = repr(error)[:400]
                try:
                    while self.total_left() > 0 and not self.io.absent(self.identity):
                        self.sleep(min(.2, max(0, self.total_left())))
                    result['original_absent'] = self.io.absent(self.identity) is True
                except BaseException as error:
                    result['original_absent'] = False
                    result['absence_error'] = repr(error)[:400]
            else:
                result['original_absent'] = not self.io.launch_unknown()
            elapsed = self.clock() - self.t0
            result.update(stop_reason=self.stop_reason, elapsed=elapsed, overrun=max(0, elapsed - TOTAL_CAP),
                          owner_end_overrun=max(0, -self.owner_left()), actions=list(self.actions),
                          inputs=self.inputs, activated=self.activated,
                          slot_must_remain_held=not result['original_absent'])
            evidence_errors.extend(getattr(self.io, 'evidence_errors', []))
            result['evidence_errors'] = evidence_errors
            self.core.cleanup_receipt(self.record, 'result', result, evidence_errors)
            result['closed_normally'] = bool(result['original_absent'] and result.get('terminate_BOOL') is True
                                             and not result['overrun'] and not result['owner_end_overrun']
                                             and not result.get('cleanup_error') and not evidence_errors)
            if result['slot_must_remain_held']:
                try:
                    self.output.write({'event': 'held', 'no_more_input': True, 'original': self.identity,
                                       'slot_must_remain_held': True})
                except BaseException:
                    pass
                self.io.hold_until_absent(result)  # existing behavior; never forces or repeats termination
                stop_unless(self.identity is not None and self.io.absent(self.identity),
                            'cannot report closure without original absence')
                result.update(original_absent=True, late_absence=True, slot_must_remain_held=False,
                              initial_held=True, final_elapsed=self.clock() - self.t0)
                self.core.cleanup_receipt(self.record, 'final-closure',
                                          {'original': self.identity, 'original_absent': True, 'late': True,
                                           'final_elapsed': result['final_elapsed']}, evidence_errors)
            try:
                self.output.write({'event': 'closed', 'original_absent': result['original_absent'],
                                   'closed_normally': result['closed_normally']})
            except BaseException:
                pass
        finally:
            for closer in (getattr(self.adapter, 'close', None), getattr(getattr(self.io, 'backend', None), 'close', None)):
                if closer is not None:
                    try:
                        closer()
                    except BaseException as error:
                        result.setdefault('close_errors', []).append(type(error).__name__)

    # -- operations
    def op_status(self, command):
        latest = self.frames[-1] if self.frames else None
        return {'total_seconds_left': round(self.total_left(), 3), 'inputs': self.inputs,
                'activated': self.activated, 'first_effect_confirmed': self.first_confirmed,
                'latest_frame': latest and {'number': latest.number, 'consumed': latest.consumed,
                                            'actionable': latest.actionable}}

    def op_wait(self, command):
        end = self.clock() + command['seconds']
        while self.clock() < end and self.ui_left() > 0:
            self.sleep(min(.5, end - self.clock(), max(0, self.ui_left())))
        return {'waited': round(command['seconds'] - max(0, end - self.clock()), 3)}

    def op_capture(self, command):
        refuse_unless(len(self.frames) < MAX_FRAMES, 'frame budget exhausted')
        refuse_unless(self.ui_left() > 1, 'too little UI time for capture')
        number = len(self.frames) + 1
        self.io.check(self.identity)
        before = self.facts()
        plan = capture_plan(before['windows'])  # fresh original-PID row; never operator/stale/foreign/display
        shot = None
        if plan is not None:
            shot = self.adapter.capture(number, plan['window_id'], min(CAPTURE_TIMEOUT, self.ui_left()))
        self.io.check(self.identity)
        after = self.facts()
        reasons, geometry = [], None
        if plan is None:
            reasons.append('no visible original-App window; nothing captured (no display/other-window fallback)')
        else:
            if capture_plan(after['windows']) != plan:
                reasons.append('captured original window changed, moved, disappeared or lost front position')
            try:
                geometry = window_geometry(plan, shot['pixels'])
            except ActionRefused as refusal:
                reasons.append(str(refusal))
        if before != after:
            reasons.append('foreground/window facts changed during capture')
        foreground = self.is_foreground(after)
        if not foreground:
            reasons.append('original App is not foreground')
        frame = Frame(number, self.clock(), shot and shot['path'], shot and shot['sha256'],
                      tuple(shot['pixels']) if shot else None, geometry, after['windows'], foreground,
                      not reasons, reasons, self.inputs, facts=after)
        self.frames.append(frame)
        capture = None if plan is None else {
            'basis': 'original-window', 'window_id': plan['window_id'], 'origin_points': plan['bounds'][:2],
            'size_points': plan['bounds'][2:], 'whole_display': False}
        summary = {'frame': number, 'path': frame.path, 'sha256': frame.sha256,
                   'pixels': list(frame.pixels) if frame.pixels else None, 'capture': capture,
                   'scale': geometry and geometry['scale'], 'foreground': foreground,
                   'actionable': frame.actionable, 'reasons': reasons,
                   'windows_capture_pixels': [dict(w, bounds=capture_local(geometry, w['bounds']))
                                              for w in frame.windows] if geometry else None}
        self.record('frame', dict(summary, windows_global_points=frame.windows))
        return summary

    def current_frame(self, command, actionable=True):
        frame = self.frames[-1] if self.frames else None
        refuse_unless(frame is not None and command['frame'] == frame.number, 'stale, replayed or unknown frame')
        refuse_unless(not frame.consumed, 'frame action permission already consumed')
        refuse_unless(self.clock() - frame.taken <= FRAME_MAX_AGE, 'frame too old; capture again')
        frame.consumed = True  # one attempt per frame, even when a later check refuses
        refuse_unless(not actionable or frame.actionable, 'frame not actionable: ' + '; '.join(frame.reasons))
        return frame

    def verify_unchanged(self, frame):
        self.io.check(self.identity)  # full original birth/UID/path/PGID/hash
        stop_unless(not self.io.supplier_started(), 'unexpected supplier start; stop session')
        now = self.facts()
        refuse_unless(self.is_foreground(now), 'original App not foreground immediately before input')
        refuse_unless(now['windows'] == frame.windows, 'window geometry changed since frame')

    def dispatch_check(self, frame):
        self.require_time()
        self.verify_unchanged(frame)
        self.require_time()  # identity/window/native preparation may have crossed the cutoff
        refuse_unless(self.clock() - frame.taken <= FRAME_MAX_AGE, 'frame too old; capture again')

    def activation_check(self, frame):
        self.require_time()
        self.io.check(self.identity)
        self.require_time()
        refuse_unless(self.clock() - frame.taken <= FRAME_MAX_AGE, 'frame too old; capture again')

    def input(self, command, kind, build):
        """One input per fresh frame: consume, recheck original/foreground/geometry, record, post pairs."""
        refuse_unless(self.inputs < MAX_INPUTS, 'input budget exhausted')
        refuse_unless(self.ui_left() > 1, 'too little UI time for input')
        frame = self.current_frame(command)
        if self.inputs == 0:
            refuse_unless(kind == 'click', 'first input must be one benign visible click')
        else:
            refuse_unless(self.first_confirmed, 'operator has not confirmed the first click effect')
        specs, detail = build(frame)
        self.verify_unchanged(frame)
        intent = {'kind': kind, 'frame': frame.number, 'frame_sha256': frame.sha256, 'original': self.identity,
                  'actor': 'operator via visual session', 'handling': 'unknown', 'no_repeat': True, **detail}
        self.record('input-intent', intent)  # a recording failure sends no input
        self.inputs += 1
        gesture, error = Gesture(self.adapter), None
        try:
            gesture.run(self.identity['pid'], specs, lambda: self.dispatch_check(frame), self.birth_check)
        except BaseException as exc:
            error = repr(exc)[:400]
            raise
        finally:
            row = {'kind': kind, 'frame': frame.number, 'at': self.clock() - self.t0, 'error': error, **gesture.state}
            self.actions.append(row)
            errors = []
            self.core.cleanup_receipt(self.record, 'input-result', row, errors)
            if errors and error is None:
                raise SessionStop('input result evidence failed')
        return {'frame': frame.number, **gesture.state, 'next': 'bounded wait, then fresh capture'}

    def op_click(self, command):
        def build(frame):
            gx, gy, window = map_target(frame, command['x'], command['y'])
            return ([('click', gx, gy, int(window['number']))],
                    {'pixel': [command['x'], command['y']], 'pixel_basis': 'local to captured original window',
                     'global_point': [gx, gy], 'window_number': window['number'],
                     'window_origin_points': frame.geometry['origin_points'], 'scale': frame.geometry['scale']})
        return self.input(command, 'click', build)

    def op_key(self, command):
        code, flags = KEYS[command['key']]
        return self.input(command, 'key', lambda frame: (
            [('key', code, flags)], {'key': command['key'], 'virtual_key': code, 'flags': flags}))

    def op_type_project(self, command):
        stop_unless(self.subject.project == EXACT_PROJECT, 'only the exact invented project text is permitted')
        chunks = utf16_chunks(self.subject.project)
        return self.input(command, 'type_project', lambda frame: (
            [('text', chunk) for chunk in chunks],
            {'text': self.subject.project, 'utf16_units': sum(map(len, chunks)), 'chunks': len(chunks)}))

    def op_activate(self, command):
        refuse_unless(not self.activated, 'one activation of the original App only')
        frame = self.current_frame(command, actionable=False)
        refuse_unless(not frame.foreground, 'original App already foreground')
        self.io.check(self.identity)
        self.record('activation-intent', {'frame': frame.number, 'original': self.identity, 'once': True})
        self.activated = True
        result, error = None, None
        try:
            result = self.adapter.activate(self.identity, self.expected_app(), lambda: self.activation_check(frame))
        except BaseException as exc:
            error = repr(exc)[:400]
            raise
        finally:
            errors = []
            self.core.cleanup_receipt(self.record, 'activation-result',
                                      {'BOOL': result, 'error': error, 'effect_proved': False}, errors)
            if errors and error is None:
                raise SessionStop('activation evidence failed')
        return {'BOOL': result, 'effect': 'unknown until a fresh capture'}

    def op_confirm_first_effect(self, command):
        refuse_unless(self.inputs >= 1 and not self.first_confirmed, 'no unconfirmed first click')
        frame = self.frames[-1] if self.frames else None
        refuse_unless(frame is not None and command['frame'] == frame.number and frame.inputs_before >= 1
                      and frame.path is not None and self.clock() - frame.taken <= FRAME_MAX_AGE,
                      'confirmation needs a fresh captured post-click frame')
        self.record('operator-first-effect', {'frame': frame.number, 'frame_sha256': frame.sha256,
                                              'actor': 'operator visual inspection', 'tool_proof': False})
        self.first_confirmed = True
        return {'frame': frame.number, 'tool_proof': False}

    def checked_locations(self, command):
        return {'Settings folder': command['settings_folder'], 'Sign-in folder': command['sign_in_folder'],
                'Saved choices': str(Path(self.subject.app_data) / 'desktop-startup/request.json')}

    def op_expected_effects(self, command):
        locations = self.checked_locations(command)
        try:
            text = self.core.setup_effects(self.subject, locations)  # includes checked_locations
        except self.core.Refusal as refusal:
            raise ActionRefused(str(refusal)) from None
        self.locations = locations
        self.record('expected-effects', {'locations': locations, 'text': text, 'semantic_proof': False})
        return {'text': text, 'note': 'operator compares visible effects; no coordinate/semantic proof'}

    def op_verify_saved(self, command):
        refuse_unless(not self.saved_used, 'pending-save verification already used')
        refuse_unless(self.locations is not None, 'expected_effects locations required first')
        self.saved_used = True
        try:
            saved = self.io.verify_saved(self.subject, self.locations)
        except (self.core.Refusal, OSError, ValueError) as error:
            self.record('saved-state-refusal', {'error': repr(error)[:400]})
            raise ActionRefused('pending save not verified: ' + str(error)[:200]) from None
        self.record('saved-state', saved)
        return {'path': saved['path'], 'sha256': saved['sha256'], 'checked': saved['checked'], 'pending_only': True}


# ---------------------------------------------------------------- native adapter

class CGPoint(C.Structure):
    _fields_ = [('x', C.c_double), ('y', C.c_double)]


class MacVisual:
    """Public macOS APIs only; constructed by a selected runtime, never on import."""
    CG = '/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics'
    CF = '/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation'
    AS = '/System/Library/Frameworks/ApplicationServices.framework/ApplicationServices'

    def __init__(self, io, frames):
        stop_unless(sys.platform == 'darwin', 'macOS visual session unavailable')
        self.io, self.frames = io, Path(frames)
        self.cg, self.cf, self.ax = C.CDLL(self.CG), C.CDLL(self.CF), C.CDLL(self.AS)
        for lib, name, result, args in (
            (self.cg, 'CGPreflightScreenCaptureAccess', C.c_bool, []),
            (self.cg, 'CGPreflightPostEventAccess', C.c_bool, []),
            (self.ax, 'AXIsProcessTrusted', C.c_bool, []),
            (self.cg, 'CGEventSourceCreate', C.c_void_p, [C.c_int32]),
            (self.cg, 'CGEventCreateMouseEvent', C.c_void_p, [C.c_void_p, C.c_uint32, CGPoint, C.c_uint32]),
            (self.cg, 'CGEventCreateKeyboardEvent', C.c_void_p, [C.c_void_p, C.c_uint16, C.c_bool]),
            (self.cg, 'CGEventSetFlags', None, [C.c_void_p, C.c_uint64]),
            (self.cg, 'CGEventSetIntegerValueField', None, [C.c_void_p, C.c_uint32, C.c_int64]),
            (self.cg, 'CGEventKeyboardSetUnicodeString', None, [C.c_void_p, C.c_ulong, C.POINTER(C.c_uint16)]),
            (self.cg, 'CGEventPostToPid', None, [C.c_int32, C.c_void_p]),
            (self.cf, 'CFRelease', None, [C.c_void_p]),
            (self.cf, 'CFRunLoopRunInMode', C.c_int32, [C.c_void_p, C.c_double, C.c_bool]),
        ):
            fn = getattr(lib, name)
            fn.restype, fn.argtypes = result, args
        self.default_mode = C.c_void_p.in_dll(self.cf, 'kCFRunLoopDefaultMode').value

    def preflight(self):
        # Preflight only: no CGRequest*/AXIsProcessTrustedWithOptions prompt symbols are bound.
        return {'screen_capture': bool(self.cg.CGPreflightScreenCaptureAccess()),
                'post_event': bool(self.cg.CGPreflightPostEventAccess()),
                'ax_trusted': bool(self.ax.AXIsProcessTrusted())}

    def capture(self, number, window, timeout):
        """Capture exactly one CGWindowID chosen by the session from original-PID rows; no display mode."""
        import subprocess
        stop_unless(type(window) is int and 0 < window < 2 ** 32, 'original window id invalid')
        path = self.frames / f'frame-{number:03d}.png'
        stop_unless(not os.path.lexists(path), 'frame path already exists')
        # -l <windowid>: that window only; -o: no window shadow; -x: no sound.
        result = subprocess.run(['/usr/sbin/screencapture', '-x', '-o', '-l', str(window), str(path)],
                                capture_output=True, timeout=max(0.5, timeout))
        stop_unless(result.returncode == 0, 'screencapture failed')
        info = os.lstat(path)
        stop_unless(stat.S_ISREG(info.st_mode) and info.st_uid == os.getuid() and 0 < info.st_size <= MAX_PNG,
                    'capture file invalid')
        os.chmod(path, 0o600)
        raw = path.read_bytes()
        return {'path': str(path), 'sha256': sha256(raw), 'pixels': png_size(raw)}

    def foreground(self, identity):
        appkit = self.io.appkit
        self.cf.CFRunLoopRunInMode(self.default_mode, 0.05, True)  # let NSWorkspace state refresh
        with appkit.target(identity['pid']) as target:
            actual = appkit.describe(target)
            active = bool(appkit.boolean(target, appkit.sel(b'isActive')))
            workspace = appkit.obj(appkit.objc.objc_getClass(b'NSWorkspace'), appkit.sel(b'sharedWorkspace'))
            stop_unless(workspace, 'NSWorkspace unavailable')
            front = appkit.obj(workspace, appkit.sel(b'frontmostApplication'))
            front_pid = appkit.pidcall(front, appkit.sel(b'processIdentifier')) if front else None
        return {'correspondence': actual, 'active': active, 'frontmost_pid': front_pid}

    def activate(self, identity, expected, before_dispatch):
        appkit = self.io.appkit
        send = C.CFUNCTYPE(C.c_bool, C.c_void_p, C.c_void_p, C.c_ulong)(('objc_msgSend', appkit.objc))
        with appkit.target(identity['pid']) as target:
            stop_unless(appkit.describe(target) == expected, 'AppKit activation target differs')
            before_dispatch()  # after AppKit/identity preparation, immediately before activation
            return bool(send(target, appkit.sel(b'activateWithOptions:'), 0))

    def source(self):
        return self.cg.CGEventSourceCreate(-1)  # kCGEventSourceStatePrivate

    def event(self, source, spec, down):
        kind = spec[0]
        if kind == 'click':
            event = self.cg.CGEventCreateMouseEvent(source, 1 if down else 2, CGPoint(spec[1], spec[2]), 0)
        else:
            event = self.cg.CGEventCreateKeyboardEvent(source, spec[1] if kind == 'key' else 0, down)
        if not event:
            return None
        try:
            if kind == 'click':
                self.cg.CGEventSetIntegerValueField(event, 1, 1)  # kCGMouseEventClickState
                for window_field in (91, 92):  # kCGMouseEventWindowUnderMousePointer[ThatCanHandleThisEvent]
                    self.cg.CGEventSetIntegerValueField(event, window_field, spec[3])
            elif kind == 'key':
                self.cg.CGEventSetFlags(event, spec[2])
            elif kind == 'text':
                self.cg.CGEventSetFlags(event, 0)
                units = (C.c_uint16 * len(spec[1]))(*spec[1])
                self.cg.CGEventKeyboardSetUnicodeString(event, len(spec[1]), units)
            else:
                raise SessionStop('unknown event kind')
        except BaseException:
            self.cf.CFRelease(event)
            raise
        return event

    def post(self, pid, event):
        self.cg.CGEventPostToPid(pid, event)  # void: never a handling proof

    def release(self, value):
        self.cf.CFRelease(value)

    def close(self):
        pass  # no retained CF objects; each gesture releases its own


# ---------------------------------------------------------------- entry

def parse_args(argv):
    parser = argparse.ArgumentParser(
        description='Bounded development-only visual session for the reviewed 66d39df5/75e953fe App. '
                    'Running it launches that App and requires a separate fresh owner/Root GO under ordinary t3_slot.',
        epilog='Protocol: one JSON object per stdin line; see NATIVE_VISUAL_SESSION.md. --help performs no OS action.')
    parser.add_argument('--owner-window-end', required=True, help='fresh UTC YYYY-MM-DDTHH:MM:SS[.ffffff]Z')
    parser.add_argument('--preflight', required=True, help='exact reviewed corrected receipt path')
    parser.add_argument('--journal', required=True, help='new empty private 0700 evidence directory')
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    owner_end = parse_owner_end(args.owner_window_end)
    stop_unless(args.preflight == RECEIPT_PATH, 'preflight receipt path differs')
    raw = Path(RECEIPT_PATH).read_bytes()
    stop_unless(sha256(raw) == RECEIPT_SHA, 'reviewed receipt changed')
    core, reader = load_core(), load_reader()
    subject = reviewed_subject(core, json.loads(raw))
    root = Path(args.journal)
    stop_unless(root.is_absolute() and root.is_dir() and not any(root.iterdir()), 'new empty journal directory required')
    record = core.private_journal(root)
    frames = root / 'frames'
    os.mkdir(frames, 0o700)
    io = core.NativeSession(subject, json.loads(raw), record)
    session = VisualSession(core, subject, io, lambda: MacVisual(io, frames), reader, record, owner_end,
                            LineReader(sys.stdin.fileno()), LineWriter(sys.stdout))
    import signal

    def interrupt(signum, frame):
        if not session.closing:
            raise SessionSignal(signum)  # normal cleanup follows; ignored once cleanup/hold began
    for signum in (signal.SIGTERM, signal.SIGHUP, signal.SIGINT):
        signal.signal(signum, interrupt)
    result = session.run()
    print(json.dumps({'event': 'session-result', 'result': result}, sort_keys=True, default=str), flush=True)
    return 0 if result.get('closed_normally') else 1  # rc is not closure evidence; absence is


if __name__ == '__main__':
    raise SystemExit(main())
