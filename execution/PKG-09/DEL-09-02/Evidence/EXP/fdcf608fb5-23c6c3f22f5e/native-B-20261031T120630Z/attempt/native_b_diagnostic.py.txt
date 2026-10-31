"""Read-only owned-App window inventory. No launch, signal, activation or prompt.

Called only with the keeper's original retained Child. Native APIs are loaded
lazily at capture, never on import. WindowServer rows are filtered by owner PID
before any other field is decoded. This is observation, not supplier custody.
"""
import ctypes as C
from datetime import datetime, timezone
import hashlib
import os
from pathlib import Path
import sys
import time

MAX_WINDOWS = 4096
MAX_OWN_WINDOWS = 32
MAX_AX_REFERENCES = 64
MAX_SECONDS = 8.0
AX_ATTRIBUTES = ('AXWindows', 'AXMainWindow', 'AXFocusedWindow', 'AXChildren')
LIMITS = ('Read-only representations, not window-construction proof or supplier custody. '
          'No listed WindowServer row can also mean a window never ordered in. '
          'Before/after identity checks do not establish an atomic observation snapshot. '
          'Eight-second deadline is checked between native calls; WindowServer calls have no cancellation guarantee.')


def require(ok, reason):
    if not ok:
        raise RuntimeError(reason)


def now():
    return datetime.now(timezone.utc).isoformat()


class Bsd(C.Structure):
    # sys/proc_info.h proc_bsdinfo, macOS arm64, 136 bytes.
    _fields_ = [(k, C.c_uint32) for k in ('flags', 'status', 'xstatus', 'pid', 'ppid', 'uid',
        'gid', 'ruid', 'rgid', 'svuid', 'svgid', 'reserved')] + [('comm', C.c_char * 16),
        ('name', C.c_char * 32)] + [(k, C.c_uint32) for k in ('nfiles', 'pgid', 'pjobc', 'tdev', 'tpgid')] + [
        ('nice', C.c_int32), ('start_sec', C.c_uint64), ('start_usec', C.c_uint64)]


class NativeBackend:
    def __init__(self):
        require(sys.platform == 'darwin', 'macOS diagnostic unavailable')
        self.c = C.CDLL('/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation')
        self.a = C.CDLL('/System/Library/Frameworks/ApplicationServices.framework/ApplicationServices')
        self.p = C.CDLL('/usr/lib/libproc.dylib')
        self.held = []
        declarations = [
            (self.p, 'proc_pidinfo', C.c_int, [C.c_int, C.c_int, C.c_uint64, C.c_void_p, C.c_int]),
            (self.p, 'proc_pidpath', C.c_int, [C.c_int, C.c_void_p, C.c_uint32]),
            (self.c, 'CFRelease', None, [C.c_void_p]),
            (self.c, 'CFGetTypeID', C.c_ulong, [C.c_void_p]),
            (self.c, 'CFStringCreateWithCString', C.c_void_p, [C.c_void_p, C.c_char_p, C.c_uint32]),
            (self.c, 'CFStringGetLength', C.c_long, [C.c_void_p]),
            (self.c, 'CFStringGetCString', C.c_bool, [C.c_void_p, C.c_void_p, C.c_long, C.c_uint32]),
            (self.c, 'CFNumberGetValue', C.c_bool, [C.c_void_p, C.c_long, C.c_void_p]),
            (self.c, 'CFBooleanGetValue', C.c_bool, [C.c_void_p]),
            (self.c, 'CFArrayGetCount', C.c_long, [C.c_void_p]),
            (self.c, 'CFArrayGetValueAtIndex', C.c_void_p, [C.c_void_p, C.c_long]),
            (self.c, 'CFDictionaryGetValue', C.c_void_p, [C.c_void_p, C.c_void_p]),
            (self.c, 'CFEqual', C.c_bool, [C.c_void_p, C.c_void_p]),
            (self.a, 'CGWindowListCopyWindowInfo', C.c_void_p, [C.c_uint32, C.c_uint32]),
            (self.a, 'CGPreflightScreenCaptureAccess', C.c_bool, []),
            (self.a, 'AXUIElementCreateApplication', C.c_void_p, [C.c_int]),
            (self.a, 'AXUIElementSetMessagingTimeout', C.c_int, [C.c_void_p, C.c_float]),
            (self.a, 'AXUIElementCopyAttributeValue', C.c_int, [C.c_void_p, C.c_void_p, C.POINTER(C.c_void_p)]),
            (self.a, 'AXUIElementGetPid', C.c_int, [C.c_void_p, C.POINTER(C.c_int)]),
            (self.a, 'AXUIElementGetTypeID', C.c_ulong, []),
        ]
        for library, name, result, args in declarations:
            f = getattr(library, name)
            f.restype, f.argtypes = result, args
        self.types = {}
        for name in ('String', 'Number', 'Boolean', 'Array', 'Dictionary'):
            f = getattr(self.c, 'CF' + name + 'GetTypeID')
            f.restype, f.argtypes = C.c_ulong, []
            self.types[f()] = 'CF' + name
        self.types[self.a.AXUIElementGetTypeID()] = 'AXUIElement'

    def close(self):
        for reference in reversed(self.held):
            self.c.CFRelease(reference)
        self.held.clear()

    def own_reference(self, reference):
        require(bool(reference), 'native object unavailable')
        self.held.append(reference)
        return reference

    def string(self, value):
        return self.own_reference(self.c.CFStringCreateWithCString(None, value.encode(), 0x08000100))

    def kind(self, value):
        if not value:
            return {'id': None, 'name': 'null'}
        number = self.c.CFGetTypeID(value)
        return {'id': number, 'name': self.types.get(number, 'other')}

    def scalar(self, value):
        kind = self.kind(value)['name']
        if kind == 'null':
            return None
        if kind == 'CFNumber':
            number = C.c_double()
            require(self.c.CFNumberGetValue(value, 13, C.byref(number)), 'native number unavailable')
            return number.value
        if kind == 'CFBoolean':
            return bool(self.c.CFBooleanGetValue(value))
        if kind == 'CFString':
            length = self.c.CFStringGetLength(value)
            require(0 <= length <= 4096, 'native text exceeds bound')
            buffer = C.create_string_buffer(length * 4 + 1)
            require(self.c.CFStringGetCString(value, buffer, len(buffer), 0x08000100), 'native text unavailable')
            return buffer.value.decode('utf-8')
        raise RuntimeError('unexpected scalar native type')

    def array(self, value, bound):
        require(self.kind(value)['name'] == 'CFArray', 'native array unavailable')
        length = self.c.CFArrayGetCount(value)
        require(0 <= length <= bound, 'native reference expansion exceeds bound')
        return [self.c.CFArrayGetValueAtIndex(value, i) for i in range(length)]

    def identity(self, pid):
        info, path = Bsd(), C.create_string_buffer(4096)
        require(C.sizeof(info) == 136 and self.p.proc_pidinfo(pid, 3, 0, C.byref(info), 136) == 136,
                'complete original-child birth/identity unavailable')
        require(self.p.proc_pidpath(pid, path, len(path)) > 0, 'original-child executable unavailable')
        require(info.pid == pid and info.uid == info.ruid == os.getuid()
                and info.status in (2, 3) and not info.flags & 7,
                'original-child identity is foreign, traced, exiting or nonlive')
        return {key: int(getattr(info, key)) for key in ('pid', 'ppid', 'uid', 'ruid', 'start_sec', 'start_usec')} | {
            'executable': os.fsdecode(path.value)}

    def window_rows(self):
        # kCGWindowListOptionAll == 0; kCGNullWindowID == 0. No image APIs.
        rows = self.own_reference(self.a.CGWindowListCopyWindowInfo(0, 0))
        return self.array(rows, MAX_WINDOWS)

    def field(self, row, key):
        require(self.kind(row)['name'] == 'CFDictionary', 'WindowServer row unavailable')
        return self.c.CFDictionaryGetValue(row, self.string(key))

    def owner_pid(self, row):
        value = self.scalar(self.field(row, 'kCGWindowOwnerPID'))
        require(type(value) in (int, float) and value > 0 and int(value) == value, 'WindowServer owner unavailable')
        return int(value)

    def screen_access(self):
        # Preflight only. There is intentionally no request-access symbol.
        return bool(self.a.CGPreflightScreenCaptureAccess())

    def decode_owned_window(self, row, access):
        bounds = self.field(row, 'kCGWindowBounds')
        require(self.kind(bounds)['name'] == 'CFDictionary', 'owned window bounds unavailable')
        title = self.field(row, 'kCGWindowName')
        return {'number': self.scalar(self.field(row, 'kCGWindowNumber')),
                'layer': self.scalar(self.field(row, 'kCGWindowLayer')),
                'bounds': {key: self.scalar(self.field(bounds, key)) for key in ('X', 'Y', 'Width', 'Height')},
                'on_screen': self.scalar(self.field(row, 'kCGWindowIsOnscreen')),
                'title_key_present': bool(title),
                'title': self.scalar(title) if access and title else None}

    def app(self, pid):
        app = self.own_reference(self.a.AXUIElementCreateApplication(pid))
        require(self.a.AXUIElementSetMessagingTimeout(app, 0.5) == 0, 'AX bounded messaging unavailable')
        return app

    def equal(self, left, right):
        return bool(self.c.CFEqual(left, right))

    def element_type(self, element):
        return self.kind(element)

    def bounded_element(self, element):
        require(self.kind(element)['name'] == 'AXUIElement', 'AX reference is not an AX element')
        require(self.a.AXUIElementSetMessagingTimeout(element, 0.5) == 0, 'AX element timeout unavailable')

    def owner(self, element):
        self.bounded_element(element)
        require(self.kind(element)['name'] == 'AXUIElement', 'AX reference is not an AX element')
        pid = C.c_int()
        rc = self.a.AXUIElementGetPid(element, C.byref(pid))
        return rc, pid.value

    def attribute(self, element, name):
        self.bounded_element(element)
        value = C.c_void_p()
        rc = self.a.AXUIElementCopyAttributeValue(element, self.string(name), C.byref(value))
        if value.value:
            self.held.append(value.value)
        kind = self.kind(value.value)
        references, scalar = [], None
        if rc == 0:
            if kind['name'] == 'CFArray':
                references = self.array(value.value, MAX_AX_REFERENCES)
            elif kind['name'] == 'AXUIElement':
                references = [value.value]
            elif kind['name'] in ('CFString', 'CFNumber', 'CFBoolean', 'null'):
                scalar = self.scalar(value.value)
        return {'return_code': rc, 'type': kind, 'value': scalar}, references


def bound_identity(run, backend):
    reservation = run.reservation
    require(reservation is not None and not reservation.reaped and reservation.observe() is None,
            'original retained App is not live/unreaped')
    pid = reservation.child.pid  # No caller-supplied PID ingress.
    identity = backend.identity(pid)
    require(identity['pid'] == pid and identity['ppid'] == os.getpid()
            and identity['uid'] == identity['ruid'] == os.getuid()
            and identity['executable'] == run.value['executable'], 'original App binding differs')
    require(Path(identity['executable']).is_file()
            and hashlib.sha256(Path(identity['executable']).read_bytes()).hexdigest() == run.value['executable_sha256'],
            'original App executable content differs')
    require(reservation.observe() is None, 'original App exited during identity check')
    return identity


def window_inventory(backend, pid, check=lambda: None):
    check()
    access = backend.screen_access()
    result = []
    check()
    rows = backend.window_rows()
    require(len(rows) <= MAX_WINDOWS, 'WindowServer list exceeds bound')
    for row in rows:
        check()
        # The only operation on a foreign row is its owner PID lookup.
        if backend.owner_pid(row) != pid:
            continue
        require(len(result) < MAX_OWN_WINDOWS, 'owned WindowServer rows exceed bound')
        result.append(backend.decode_owned_window(row, access))
    return {'at': now(), 'source': 'CGWindowListCopyWindowInfo(kCGWindowListOptionAll)',
            'screen_capture_preflight_access': access, 'rows': result}


def ax_inventory(backend, pid, check=lambda: None):
    check()
    app = backend.app(pid)
    rc, owner = backend.owner(app)
    require(rc == 0 and owner == pid, 'owned AX application unavailable')
    result = []
    for name in AX_ATTRIBUTES:
        check()
        attribute, references = backend.attribute(app, name)
        require(len(references) <= MAX_AX_REFERENCES, 'AX references exceed bound')
        seen, children = [], []
        for element in references:
            check()
            owner_rc, owner = backend.owner(element)
            require(owner_rc == 0 and owner == pid, 'AX reference ownership unavailable or foreign')
            duplicate = any(backend.equal(element, old) for old in seen)
            self_reference = backend.equal(element, app)
            seen.append(element)
            row = {'type': backend.element_type(element), 'owner_return_code': owner_rc, 'application_self_reference': self_reference,
                   'duplicate_reference': duplicate}
            if not duplicate:
                role, unused = backend.attribute(element, 'AXRole')
                require(not unused, 'AX role unexpectedly references objects')
                row['role'] = role
            children.append(row)
            # Deliberately no recursion. Self/cyclic references are observations.
        result.append({'attribute': name, **attribute, 'references': children})
    return {'at': now(), 'source': 'owned AX attribute calls; nonrecursive children', 'attributes': result}


def capture(run, backend_factory=NativeBackend):
    """Return scoped observations only while original Child identity stays bound.

    The caller must preserve any refusal as unavailable; never infer absence or
    release custody from failure here. No UI action or settlement permission.
    """
    require(run.reservation is not None and not run.reservation.reaped
            and run.reservation.observe() is None, 'original App exited during diagnostic or reservation unavailable')
    require(not getattr(run, 'reason', None), 'diagnostic skipped: ' + str(getattr(run, 'reason', None)))
    backend = backend_factory()
    try:
        started = now()
        deadline = time.monotonic() + MAX_SECONDS
        def check():
            require(not getattr(run, 'reason', None), 'diagnostic stopped: ' + str(getattr(run, 'reason', None)))
            require(time.monotonic() < deadline, 'owned-window diagnostic deadline')
            require(run.reservation is not None and run.reservation.observe() is None,
                    'original App exited during diagnostic')
        check()
        before = bound_identity(run, backend)
        windows = window_inventory(backend, before['pid'], check)
        require(bound_identity(run, backend) == before, 'original App changed across WindowServer observation')
        try:
            accessibility = ax_inventory(backend, before['pid'], check)
        except RuntimeError as error:
            accessibility = {'at': now(), 'source': 'owned AX attribute calls', 'available': False,
                             'error': str(error), 'limits': 'AX refusal does not erase separately bound WindowServer observation.'}
        after = bound_identity(run, backend)
        require(after == before, 'original App changed across AX observation')
        return {'format': 'chirality.native-B.owned-window-diagnostic/v1',
                'diagnostic_source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                'admission_sha256': getattr(run, 'admission_sha', None),
                'started_at': started, 'finished_at': now(), 'candidate': run.value['candidate_key'],
                'binding_source': 'original retained Child + proc_bsdinfo/proc_pidpath + inventoried executable SHA256',
                'identity_before': before, 'identity_after': after,
                'executable_sha256': run.value['executable_sha256'],
                'window_server': windows, 'accessibility': accessibility, 'limits': LIMITS}
    finally:
        backend.close()
