"""Explicit App-specific picker experiment. Import performs no native operation.

This is not a fallback in Stage A: no path input, setup/save or qualification.
The existing full-setup module and its defaults are unchanged.
"""
import ctypes as C
import hashlib
import os
from pathlib import Path
import sys
import time
from copy import deepcopy

from j1_stage_a_phase import (StageA, NativeSession, Refusal, phase_root)


class DiagnosticStop(Refusal):
    def __init__(self, code):
        super().__init__(code)
        self.code = code  # fixed source literals only, never UI/exception text


def require(ok, code):
    if not ok:
        raise DiagnosticStop(code)


class NativePosting:
    """SDK ABI, prepared only in the selected runner's pre-launch admission."""
    def __init__(self):
        self.cg = C.CDLL('/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics')
        self.cf = C.CDLL('/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation')
        for lib, name, result, args in (
            (self.cg, 'CGPreflightPostEventAccess', C.c_bool, []),
            (self.cg, 'CGEventSourceCreate', C.c_void_p, [C.c_int32]),
            (self.cg, 'CGEventCreateKeyboardEvent', C.c_void_p, [C.c_void_p, C.c_uint16, C.c_bool]),
            (self.cg, 'CGEventSetFlags', None, [C.c_void_p, C.c_uint64]),
            (self.cg, 'CGEventPostToPid', None, [C.c_int32, C.c_void_p]),
            (self.cf, 'CFRelease', None, [C.c_void_p]),
        ):
            fn = getattr(lib, name)
            fn.restype, fn.argtypes = result, args

    def preflight(self):
        return bool(self.cg.CGPreflightPostEventAccess())

    def source(self):
        return self.cg.CGEventSourceCreate(-1)  # independent PRIVATE state

    def event(self, source, down):
        return self.cg.CGEventCreateKeyboardEvent(source, 0x05, down)

    def flags(self, event):
        self.cg.CGEventSetFlags(event, 0x00120000)

    def post(self, original, event):
        self.cg.CGEventPostToPid(original['pid'], event)  # void, not handling proof

    def release(self, value):
        self.cf.CFRelease(value)


class StructuralCalls:
    """Count/range reads, never full AXChildren array fetches or content reads."""
    def __init__(self, backend):
        self.b = backend
        self.count_fn = backend.a.AXUIElementGetAttributeValueCount
        self.count_fn.restype, self.count_fn.argtypes = C.c_int, [C.c_void_p, C.c_void_p, C.POINTER(C.c_long)]
        self.range_fn = backend.a.AXUIElementCopyAttributeValues
        self.range_fn.restype, self.range_fn.argtypes = C.c_int, [C.c_void_p, C.c_void_p, C.c_long, C.c_long, C.POINTER(C.c_void_p)]
        self.value_fn = backend.a.AXUIElementCopyAttributeValue
        self.value_fn.restype, self.value_fn.argtypes = C.c_int, [C.c_void_p, C.c_void_p, C.POINTER(C.c_void_p)]

    def value(self, ref, attribute):
        value = C.c_void_p()
        rc = self.value_fn(ref, self.b.string(attribute), C.byref(value))
        if value.value:
            self.b.held.append(value.value)
        kind = self.b.kind(value.value)['name']
        scalar, refs = None, []
        if rc == 0:
            if attribute in ('AXParent', 'AXFocusedUIElement') and kind == 'AXUIElement':
                refs = [value.value]
            elif (attribute == 'AXRole' and kind == 'CFString') or (attribute == 'AXModal' and kind == 'CFBoolean'):
                scalar = self.b.scalar(value.value)  # reviewed CF scalar conversion
        # Unexpected arrays/types are classified, NEVER decoded as references.
        return {'return_code': rc, 'type': {'name': kind}, 'value': scalar}, refs

    def count(self, ref, attribute):
        count = C.c_long()
        rc = self.count_fn(ref, self.b.string(attribute), C.byref(count))
        return rc, count.value

    def refs(self, ref, attribute, count):
        value = C.c_void_p()
        rc = self.range_fn(ref, self.b.string(attribute), 0, count, C.byref(value))
        if value.value:
            self.b.held.append(value.value)  # range returns retained CFArray
        kind = self.b.kind(value.value)['name']
        if rc != 0 or kind != 'CFArray':
            return rc, kind, []
        return rc, kind, self.b.array(value.value, 12)


KNOWN_ROLES = frozenset({
    'AXApplication', 'AXWindow', 'AXSheet', 'AXDialog', 'AXGroup', 'AXSplitGroup',
    'AXButton', 'AXTextField', 'AXComboBox', 'AXStaticText', 'AXTextArea',
    'AXTable', 'AXOutline', 'AXBrowser', 'AXList', 'AXRow', 'AXCell', 'AXScrollArea',
    'AXPathControl', 'AXPopUpButton', 'AXMenu', 'AXMenuBar', 'AXToolbar',
})


class Structure:
    """One shared 32-ref budget for binding, routing and the one snapshot."""
    def __init__(self, session, main, phase_end):
        self.io, self.b, self.calls = session, session.backend, session.structural_calls
        self.app, self.main = session.ax.app, main
        self.original = deepcopy(session.identity)
        self.end, self.refs_seen, self.rows = phase_end, [], []
        self.snapshot_used = False
        self.command_picker = None
        self.io.check(self.original)
        self.touch(self.app)
        self.touch(main)

    def check(self):
        require(self.io.clock() < self.end, 'diagnostic phase cutoff')
        require(self.same(self.app, self.io.ax.app) and self.same(self.main, self.io.ax.main),
                'diagnostic original AX binding changed')

    def same(self, a, b):
        if a is None or b is None:
            return a is b
        return self.b.equal(a, b)

    def owner(self, ref, row):
        rc, owner = self.b.owner(ref)
        row['owner_match'] = rc == 0 and owner == self.original['pid']
        require(row['owner_match'], 'diagnostic owner changed')

    def touch(self, ref):
        self.check()
        for index, previous in enumerate(self.refs_seen):
            if self.same(ref, previous):
                return self.rows[index]
        require(len(self.refs_seen) < 32, 'diagnostic distinct-reference cap')
        kind = self.b.kind(ref)['name']
        row = {'ordinal': len(self.rows), 'cf_type': kind if kind == 'AXUIElement' else 'other',
               'owner_match': None, 'role': None, 'parent_ordinal': None, 'reads': []}
        self.refs_seen.append(ref)
        self.rows.append(row)
        require(kind == 'AXUIElement', 'diagnostic non-element reference')
        rc, owner = self.b.owner(ref)
        row['reads'].append({'attribute': 'owner', 'return_code': rc, 'cf_type': 'pid'})
        row['owner_match'] = rc == 0 and owner == self.original['pid']
        require(row['owner_match'], 'diagnostic foreign/unknown owner')
        return row

    def value(self, ref, name):
        require(name in ('AXRole', 'AXParent', 'AXModal', 'AXFocusedUIElement'), 'diagnostic attribute forbidden')
        row = self.touch(ref)
        self.owner(ref, row)
        if name in ('AXParent', 'AXFocusedUIElement'):
            require(len(self.refs_seen) < 32, 'diagnostic scalar-reference budget exhausted')
        value, refs = self.calls.value(ref, name)
        rc, kind = value['return_code'], value['type']['name']
        row['reads'].append({'attribute': name, 'return_code': rc,
                             'cf_type': kind if kind in ('AXUIElement', 'CFString', 'CFBoolean', 'null') else 'other'})
        require(rc in (0, -25205, -25212), 'diagnostic structural read failed')
        if rc != 0:
            return None
        if name in ('AXParent', 'AXFocusedUIElement'):
            require(kind == 'AXUIElement' and len(refs) == 1, 'diagnostic scalar-reference type')
            target = refs[0]
            parent = self.touch(target)
            if name == 'AXParent':
                row['parent_ordinal'] = parent['ordinal']
            return target
        if name == 'AXRole':
            require(kind == 'CFString' and isinstance(value['value'], str), 'diagnostic role type')
            role = value['value'] if value['value'] in KNOWN_ROLES else 'unknown'
            row['role'] = role  # never retain a custom role string
            return role
        require(kind == 'CFBoolean' and type(value['value']) is bool, 'diagnostic modal type')
        return value['value']

    def role(self, ref):
        role = self.value(ref, 'AXRole')
        require(role is not None, 'diagnostic mandatory role absent')
        return role

    def ref(self, ref, name):
        return self.value(ref, name)

    def refs(self, ref, name, optional=True):
        require(name in ('AXChildren', 'AXSheets', 'AXWindows'), 'diagnostic array forbidden')
        row = self.touch(ref)
        self.owner(ref, row)
        rc, count = self.calls.count(ref, name)
        row['reads'].append({'attribute': name, 'return_code': rc, 'cf_type': 'count',
                             'count': count if rc == 0 and 0 <= count <= 12 else None,
                             'over_limit': rc == 0 and count > 12})
        if optional and rc in (-25205, -25212):
            return []
        require(rc == 0 and 0 <= count <= 12, 'diagnostic child/count cap or read failed')
        self.check()
        if count == 0:
            return []
        require(count <= 32 - len(self.refs_seen), 'diagnostic prospective reference cap')
        self.owner(ref, row)
        rc, kind, refs = self.calls.refs(ref, name, count)
        row['reads'].append({'attribute': name, 'return_code': rc,
                             'cf_type': 'CFArray' if kind == 'CFArray' else 'other'})
        require(rc == 0 and kind == 'CFArray' and len(refs) == count, 'diagnostic bounded range failed')
        for child in refs:
            self.touch(child)
        return refs

    def picker(self):
        self.check()
        self.io.check(self.original)
        root = phase_root(self, self.app, self.main, 'picker')
        self.io.check(self.original)
        self.check()
        return root

    def routing(self, picker):
        current = self.ref(self.app, 'AXFocusedUIElement')
        seen, path = [], []
        for _ in range(7):  # focused ref plus at most six parent links
            require(current is not None, 'diagnostic focused ancestry absent')
            role = self.role(current)
            path.append(self.touch_ordinal(current))
            if self.same(current, picker):
                self.routing_path = path
                return path
            require(role not in ('AXWindow', 'AXSheet', 'AXDialog'),
                    'diagnostic focused ancestry crosses another modal')
            require(not any(self.same(current, old) for old in seen), 'diagnostic focused ancestry cycle')
            seen.append(current)
            if len(seen) <= 6:
                current = self.ref(current, 'AXParent')
        raise Refusal('diagnostic focused ancestry unrelated/too deep')

    def recheck(self, picker):
        self.command_picker = None
        self.check()
        require(self.io.project_pending is True and self.same(self.picker(), picker),
                'diagnostic project purpose/picker changed')
        require(self.same(self.ref(picker, 'AXParent'), self.main),
                'diagnostic command requires direct original-main picker')
        # A first-observed post-command sheet is not a pre-command baseline.
        # Missing/unsupported AXSheets cannot prove an empty published relation.
        require(not self.refs(picker, 'AXSheets', optional=False),
                'diagnostic nested sheet already exposed before command')
        self.routing(picker)
        self.io.check(self.original)  # final full birth/UID/PGID/path/hash bracket
        self.check()
        self.command_picker = picker

    def snapshot(self, picker, after_post):
        require(not self.snapshot_used, 'diagnostic snapshot already consumed')
        self.snapshot_used = True
        self.end = min(self.end, self.io.clock() + 1)
        label = ('unchanged-picker-effect-unknown-possibly-inline' if after_post else 'retained-picker-no-command')
        root, complete = picker, False
        error = None
        try:
            self.check()
            require(not after_post or self.same(self.command_picker, picker),
                    'diagnostic pre-command empty sheet relation unavailable')
            current = self.picker()
            nested = self.refs(picker, 'AXSheets') if after_post else []
            require(len(nested) <= 1, 'diagnostic ambiguous nested sheets')
            if nested:
                child = nested[0]
                require(self.role(child) in ('AXSheet', 'AXDialog')
                        and self.same(self.ref(child, 'AXParent'), picker),
                        'diagnostic new sheet relationship differs')
                require(self.same(current, picker) or self.same(current, child),
                        'diagnostic unexpected modal after command')
                current = child
            if not self.same(current, picker):
                require(after_post, 'diagnostic unexpected new panel before command')
                ancestor, seen = current, []
                for _ in range(6):
                    if self.same(ancestor, picker):
                        break
                    require(not any(self.same(ancestor, old) for old in seen), 'diagnostic new subtree cycle')
                    seen.append(ancestor)
                    ancestor = self.ref(ancestor, 'AXParent')
                    require(ancestor is not None, 'diagnostic new subtree relationship absent')
                require(self.same(ancestor, picker), 'diagnostic new subtree not through retained picker')
                root, label = current, 'newly-exposed-related-subtree-semantics-unknown'
            # A direct modal can contain wrappers. Only those wrappers expand.
            queue, expanded = [(root, 0)], []
            while queue:
                ref, depth = queue.pop(0)
                require(not any(self.same(ref, old) for old in expanded), 'diagnostic structural cycle')
                expanded.append(ref)
                role = self.role(ref)
                parent = self.ref(ref, 'AXParent')
                if parent is not None:
                    self.touch(parent)
                if depth == 0 or role in ('AXGroup', 'AXSplitGroup'):
                    if depth >= 3:
                        continue
                    for child in self.refs(ref, 'AXChildren', optional=False):
                        child_role = self.role(child)
                        require(self.same(self.ref(child, 'AXParent'), ref), 'diagnostic child/parent mismatch')
                        if child_role in ('AXGroup', 'AXSplitGroup'):
                            queue.append((child, depth + 1))
                        # Every other known/unknown role is a private leaf.
            self.check()
            self.io.check(self.original)
            self.check()
            complete = True
        except BaseException as exc:
            error = exc.code if isinstance(exc, DiagnosticStop) else type(exc).__name__
        return {'label': label, 'complete': complete, 'error_category': error,
                'pre_command_empty_sheet_relation': self.same(self.command_picker, picker),
                'root_ordinal': self.touch_ordinal(root), 'nodes': deepcopy(self.rows),
                'distinct_refs': len(self.rows), 'depth_cap': 3, 'reference_cap': 32,
                'child_cap': 12, 'semantic_handling': 'unknown', 'readiness': False}

    def touch_ordinal(self, ref):
        return next((i for i, old in enumerate(self.refs_seen) if self.same(old, ref)), None)


class FixedGesture:
    def __init__(self, posting):
        self.api, self.used = posting, False
        self.down_attempted, self.up_attempted = False, False
        self.allocated_count, self.release_errors = 0, []

    def status(self):
        return {'consumed': self.used, 'down_attempted': self.down_attempted,
                'up_attempted': self.up_attempted, 'allocated_count': self.allocated_count,
                'release_errors': list(self.release_errors), 'handling': 'unknown'}

    def run(self, structure, picker, record):
        require(not self.used, 'diagnostic command already consumed')
        self.used = True
        allocated = []
        try:
            source = self.api.source()
            require(source, 'diagnostic private source allocation failed')
            allocated.append(source)
            self.allocated_count += 1
            for down in (True, False):
                event = self.api.event(source, down)
                require(event, 'diagnostic fixed event allocation failed')
                allocated.append(event)
                self.allocated_count += 1
                self.api.flags(event)
            structure.recheck(picker)
            intent = {'original': deepcopy(structure.original), 'purpose': 'PROJECT-picker-structural-diagnostic',
                      'private_source_state': -1, 'virtual_key': 0x05, 'flags': 0x00120000,
                      'event_count': 2, 'picker_ordinal': structure.touch_ordinal(picker),
                      'app_ordinal': structure.touch_ordinal(structure.app),
                      'main_ordinal': structure.touch_ordinal(structure.main),
                      'pre_command_empty_sheet_relation': True,
                      'focused_ancestry_ordinals': list(structure.routing_path),
                      'handling': 'unknown', 'no_repeat': True}
            record('diagnostic-navigation-intent', intent)  # failure sends no input
            structure.recheck(picker)
            self.down_attempted = True  # void dispatch may have an unknown outcome
            try:
                self.api.post(structure.original, allocated[1])
            finally:
                # Pair release even after a post exception, only to the SAME birth.
                structure.io.check(structure.original)
                self.up_attempted = True
                self.api.post(structure.original, allocated[2])
            return {'dispatch_attempted': True, 'handling': 'unknown'}
        finally:
            errors = []
            for value in reversed(allocated):
                try:
                    self.api.release(value)
                except BaseException as exc:
                    errors.append(type(exc).__name__)
            self.release_errors = errors
            if errors:
                raise Refusal('diagnostic CF release failed')


class DiagnosticSession(NativeSession):
    def admit(self, subject):
        self.project_pending, self.chooser_used = False, False
        self.experiment_used = False
        self.diagnostic = {'diagnostic_only': True, 'semantic_handling': 'unknown', 'snapshot': None}
        executable = Path(sys.executable).resolve()
        caller = {'pid': os.getpid(), 'uid': os.getuid(), 'executable': str(executable),
                  'sha256': hashlib.sha256(executable.read_bytes()).hexdigest()}
        try:
            self.posting = NativePosting()
            allowed = self.posting.preflight()
        except BaseException:
            self.record('diagnostic-posting-preflight', {'available': False, 'posting_access': False, 'caller': caller})
            raise Refusal('diagnostic posting preflight unavailable; no App launch')
        self.record('diagnostic-posting-preflight', {'available': True, 'posting_access': allowed, 'caller': caller})
        require(allowed, 'diagnostic posting access false; no request or App launch')
        super().admit(subject)
        self.structural_calls = StructuralCalls(self.backend)  # signatures before launch
        self.gesture = FixedGesture(self.posting)

    def observe(self, main, phase, deadline):
        require(phase == 'main', 'diagnostic forbids setup/confirmation observation')
        return super().observe(main, phase, deadline)

    def press(self, control, deadline):
        require(not self.chooser_used and self.ax.last_phase == 'main'
                and control.label == 'Choose project folder…', 'diagnostic permits only one project picker press')
        self.chooser_used = True
        rc = super().press(control, deadline)
        self.project_pending = rc == 0
        return rc

    def enter_path(self, *args):
        raise Refusal('diagnostic forbids all path writes')

    def verify_saved(self, *args):
        raise Refusal('diagnostic cannot save or qualify setup')

    def experiment(self, main, work_end):
        require(not self.experiment_used, 'diagnostic experiment already consumed')
        self.experiment_used = True
        require(self.project_pending is True, 'diagnostic project purpose missing')
        structure = Structure(self, main, min(work_end, self.clock() + 2))
        picker = structure.picker()  # common binding without the content classifier
        dispatched = False
        try:
            structure.routing(picker)
            try:
                self.diagnostic['gesture'] = self.gesture.run(structure, picker, self.record)
                dispatched = True
            except BaseException:
                dispatched = self.gesture.down_attempted
                raise
        except BaseException as exc:
            self.diagnostic['refusal_category'] = exc.code if isinstance(exc, DiagnosticStop) else type(exc).__name__
        finally:
            self.diagnostic['gesture_state'] = self.gesture.status()
            snapshot = structure.snapshot(picker, dispatched)
            self.diagnostic['snapshot'] = snapshot
            self.record('diagnostic-structure', snapshot)
        self.record('diagnostic-outcome', deepcopy(self.diagnostic))
        return False


class DiagnosticStage(StageA):
    def setup(self):
        self.startup()
        view = self.ready()
        self.press(view, view.one('Choose project folder…'), 'open project picker')
        self.io.experiment(self.main, self.work_end)
        return False  # diagnostics NEVER save setup or promote J1/qualification


def run_prepared(subject, preflight, record, clock=time.monotonic, sleep=time.sleep):
    """Explicit diagnostic constructors; same original-absence custody as core.

    No factory injection, monkeypatch or replacement of the full-setup defaults.
    The finalizer below mirrors the checked core's finalizer; it sends no input.
    """
    entered = clock()
    io = DiagnosticSession(subject, preflight, record, clock, sleep)
    controller = DiagnosticStage(subject, io, clock, sleep, record)
    result = None
    try:
        result = controller.run()  # unchanged core run owns one normal termination
        result = dict(result, diagnostic_only=True, diagnostic=deepcopy(getattr(io, 'diagnostic', {})))
    finally:
        if result is None:
            try:
                live = io.launch_unknown() if io.identity is None else not io.absent(io.identity)
            except BaseException:
                live = True
            held = {'slot_must_remain_held': live}
        else:
            held = result
        try:
            io.hold_until_absent(held)
            if io.identity is not None:
                require(io.absent(io.identity), 'slot entry cannot return without original absence')
                origin = getattr(controller, 'started_at', entered)
                end = getattr(controller, 'end', origin + 180)
                closure = {'original': deepcopy(io.identity), 'original_absent': True,
                           'final_elapsed': clock() - origin, 'final_overrun': max(0, clock() - end),
                           'exit_status': None, 'exit_status_limit': 'LaunchServices-owned; no wait/reap status',
                           'initial_held': held['slot_must_remain_held']}
                record('final-closure', deepcopy(closure))
                if result is not None:
                    result = dict(result, **closure, slot_must_remain_held=False)
        finally:
            if io.backend is not None:
                io.backend.close()
    return result
