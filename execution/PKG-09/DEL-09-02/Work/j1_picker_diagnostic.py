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

from j1_stage_a_phase import (StageA, NativeSession, Refusal)


class DiagnosticStop(Refusal):
    def __init__(self, code):
        super().__init__(code)
        self.code = code  # fixed source literals only, never UI/exception text


class StructuralReadFailure(DiagnosticStop):
    """No-result CannotComplete from an allowlisted initial read only."""
    def __init__(self, api, attribute, ordinal, cf_type):
        require(api in ('value', 'count', 'range')
                and attribute in ('AXRole', 'AXParent', 'AXModal', 'AXFocusedUIElement',
                                  'AXTopLevelUIElement', 'AXWindows', 'AXSheets', 'AXChildren')
                and type(ordinal) is int and 0 <= ordinal < 32
                and cf_type in ('null', 'count'),
                'diagnostic invalid typed read failure')
        super().__init__('diagnostic structural read failed')
        self.api, self.attribute, self.ordinal, self.cf_type = api, attribute, ordinal, cf_type
        self.return_code = -25204


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
    def __init__(self, backend, clock=time.monotonic):
        self.b = backend
        self.clock, self.last_native, self.last_cf_type = clock, None, None
        self.count_fn = backend.a.AXUIElementGetAttributeValueCount
        self.count_fn.restype, self.count_fn.argtypes = C.c_int, [C.c_void_p, C.c_void_p, C.POINTER(C.c_long)]
        self.range_fn = backend.a.AXUIElementCopyAttributeValues
        self.range_fn.restype, self.range_fn.argtypes = C.c_int, [C.c_void_p, C.c_void_p, C.c_long, C.c_long, C.POINTER(C.c_void_p)]
        self.value_fn = backend.a.AXUIElementCopyAttributeValue
        self.value_fn.restype, self.value_fn.argtypes = C.c_int, [C.c_void_p, C.c_void_p, C.POINTER(C.c_void_p)]

    def _invoke(self, api, fn, *args):
        start, rc = self.clock(), None
        try:
            rc = fn(*args)
            return rc
        finally:
            self.last_native = {'api': api, 'start': start, 'end': self.clock(),
                                'rc': rc if type(rc) is int else None}

    def value(self, ref, attribute, deadline=None):
        self.last_native, self.last_cf_type = None, None
        value = C.c_void_p()
        rc = self._invoke('AXUIElementCopyAttributeValue', self.value_fn, ref, self.b.string(attribute), C.byref(value))
        if value.value:
            self.b.held.append(value.value)
        if deadline is not None and self.last_native['end'] >= deadline:
            return {'return_code': rc, 'type': {'name': 'other'}, 'value': None}, []
        kind = self.b.kind(value.value)['name']
        self.last_cf_type = kind
        scalar, refs = None, []
        if rc == 0 and (deadline is None or self.last_native['end'] < deadline):
            if attribute in ('AXParent', 'AXFocusedUIElement', 'AXTopLevelUIElement') and kind == 'AXUIElement':
                refs = [value.value]
            elif (attribute == 'AXRole' and kind == 'CFString') or (attribute == 'AXModal' and kind == 'CFBoolean'):
                scalar = self.b.scalar(value.value)  # reviewed CF scalar conversion
        # Unexpected arrays/types are classified, NEVER decoded as references.
        return {'return_code': rc, 'type': {'name': kind}, 'value': scalar}, refs

    def count(self, ref, attribute, deadline=None):
        self.last_native, self.last_cf_type = None, 'count'
        count = C.c_long()
        rc = self._invoke('AXUIElementGetAttributeValueCount', self.count_fn, ref, self.b.string(attribute), C.byref(count))
        return rc, count.value

    def refs(self, ref, attribute, count, deadline=None):
        self.last_native, self.last_cf_type = None, None
        value = C.c_void_p()
        rc = self._invoke('AXUIElementCopyAttributeValues', self.range_fn, ref, self.b.string(attribute), 0, count, C.byref(value))
        if value.value:
            self.b.held.append(value.value)  # range returns retained CFArray
        if deadline is not None and self.last_native['end'] >= deadline:
            return rc, 'other', []
        kind = self.b.kind(value.value)['name']
        self.last_cf_type = kind
        if rc != 0 or kind != 'CFArray' or (deadline is not None and self.last_native['end'] >= deadline):
            return rc, kind, []
        return rc, kind, self.b.array(value.value, 12)


KNOWN_ROLES = frozenset({
    'AXApplication', 'AXWindow', 'AXSheet', 'AXDialog', 'AXDrawer', 'AXGroup', 'AXSplitGroup',
    'AXButton', 'AXTextField', 'AXComboBox', 'AXStaticText', 'AXTextArea',
    'AXTable', 'AXOutline', 'AXBrowser', 'AXList', 'AXRow', 'AXCell', 'AXScrollArea',
    'AXPathControl', 'AXPopUpButton', 'AXMenu', 'AXMenuBar', 'AXToolbar',
})


class Structure:
    """One App-specific initial communication policy; strict input never retries."""
    PROOF_MODE = 'POSITIVE_FOCUSED_TOP_LEVEL_DIAGNOSTIC_V1'
    MODALS = frozenset(('AXWindow', 'AXSheet', 'AXDrawer', 'AXDialog'))
    VALUE_ATTRS = ('AXRole', 'AXParent', 'AXModal', 'AXFocusedUIElement', 'AXTopLevelUIElement')
    ARRAY_ATTRS = ('AXChildren', 'AXSheets', 'AXWindows')
    APIS = {'value': 'AXUIElementCopyAttributeValue', 'count': 'AXUIElementGetAttributeValueCount',
            'range': 'AXUIElementCopyAttributeValues'}
    TRACE_APIS = frozenset((*APIS.values(), 'bounded_owner_composite', 'identity_guard', 'sleep', 'input_boundary'))
    DETAIL_KEYS = frozenset(('count', 'over_limit', 'range_start', 'requested_count', 'owner_match',
                            'duration_scope', 'guard_completed', 'requested_sleep',
                            'read_capacity_used', 'owner_capacity_used'))

    def __init__(self, session, main, phase_end, work_end=None):
        self.io, self.b, self.calls = session, session.backend, session.structural_calls
        self.app, self.main = session.ax.app, main
        self.original = deepcopy(session.identity)
        self.started = session.clock()
        self.experiment_end = phase_end
        self.work_end = phase_end if work_end is None else work_end
        self.end, self.refs_seen, self.rows = phase_end, [], []
        self.snapshot_used, self.initial_binding_used = False, False
        self.command_picker, self.picker_anchor = None, None
        self.mode, self.phase, self.pass_no = 'strict', 'strict', 0
        self.initial_reads, self.initial_owners, self.op_count = 0, 0, 0
        self.trace, self.receipt_seconds, self.stopped = [], 0.0, None
        self.readiness_end, self.initial_completed_pass = None, None
        self.pre_modal_refs, self.completed_proofs = [], []
        self.proof_count, self.intent_focus, self.intent_proof_id = 0, None, None
        self.after_intent_proof = None

    def halt(self, code):
        if self.stopped is None:
            self.stopped = code

    def guard(self, ok, code):
        if not ok:
            self.halt(code)
            raise DiagnosticStop(code)

    def check(self):
        require(self.stopped is None, self.stopped or 'diagnostic stopped')
        self.guard(self.io.clock() < self.end and self.io.clock() < self.work_end,
                   'diagnostic phase cutoff')
        self.guard(self.op_count < 512, 'diagnostic trace capacity')
        self.guard(self.same(self.app, self.io.ax.app) and self.same(self.main, self.io.ax.main),
                   'diagnostic original AX binding changed')

    def same(self, a, b):
        if a is None or b is None:
            return a is b
        return self.b.equal(a, b)

    def reserve(self, api, attribute=None, ordinal=None, headroom=0):
        self.check()
        self.guard(api in self.TRACE_APIS and attribute in (*self.VALUE_ATTRS,*self.ARRAY_ATTRS,'owner',None)
                   and (ordinal is None or type(ordinal) is int and 0 <= ordinal < 32),
                   'diagnostic trace schema')
        self.guard(self.io.clock() + headroom < self.end, 'diagnostic call headroom')
        self.op_count += 1  # capacity reserved BEFORE the operation/receipt
        return {'op': self.op_count, 'phase': self.phase, 'pass': self.pass_no,
                'api': api, 'attribute': attribute, 'ordinal': ordinal,
                'start': self.io.clock(), 'deadline': self.end,
                'phase_remaining_before': self.end - self.io.clock(),
                'work_remaining_before': self.work_end - self.io.clock()}

    def set_property(self, row, name, value, token=None):
        row[name] = value
        row['property_provenance'][name] = {
            'phase': self.phase if token is None else token['phase'],
            'pass': self.pass_no if token is None else token['pass'],
            'op': None if token is None else token['op'],
            'instrumented': token is not None}

    def finish(self, token, rc=None, kind=None, details=None, native=None, row=None, raised=False):
        self.guard(details is None or set(details) <= self.DETAIL_KEYS, 'diagnostic trace detail schema')
        end = self.io.clock()
        late = end >= token['deadline'] or end >= self.work_end
        if native is not None:
            late = late or native['end'] >= token['deadline'] or native['end'] >= self.work_end
        if late:
            self.halt('diagnostic late operation')
        event = {k: token[k] for k in ('op', 'phase', 'pass', 'api', 'attribute', 'ordinal')}
        event.update(start_elapsed=token['start']-self.started, end_elapsed=end-self.started,
                     duration=end-token['start'], return_code=rc if type(rc) is int else None,
                     cf_type=None if kind is None else kind if kind in ('AXUIElement','CFString','CFBoolean','CFArray','null','count','pid') else 'other',
                     requested_timeout=.2 if token['api'] not in ('identity_guard','sleep','input_boundary') else None,
                     phase_remaining_before=token['phase_remaining_before'],
                     phase_remaining_after=token['deadline']-end,
                     work_remaining_before=token['work_remaining_before'],
                     work_remaining_after=self.work_end-end, late=late, raised=raised,
                     native_start_elapsed=None if native is None else native['start']-self.started,
                     native_end_elapsed=None if native is None else native['end']-self.started,
                     native_duration=None if native is None else native['end']-native['start'],
                     post_native_processing_duration=None if native is None else end-native['end'])
        if details:
            event.update(details)
        if row is not None:
            fact = {'attribute': token['attribute'], 'return_code': event['return_code'],
                    'cf_type': event['cf_type'], 'phase': token['phase'], 'pass': token['pass'],
                    'op': token['op'], 'late': late}
            if details:
                fact.update(details)
            row['reads'].append(deepcopy(fact))
        self.trace.append(deepcopy(event))
        record_start = self.io.clock()
        try:
            self.io.record('diagnostic-call', deepcopy(event))
        except BaseException:
            self.halt('diagnostic trace receipt failed')
            raise DiagnosticStop('diagnostic trace receipt failed') from None
        finally:
            self.receipt_seconds += self.io.clock()-record_start
            if self.io.clock() >= token['deadline'] or self.io.clock() >= self.work_end:
                self.halt('diagnostic late receipt')
        require(self.stopped is None, self.stopped or 'diagnostic stopped')

    def identity_check(self):
        token = self.reserve('identity_guard')
        completed = False
        try:
            self.io.check(self.original)  # NEVER override/instrument NativeSession.check itself
            completed = True
        except BaseException:
            self.halt('diagnostic original identity guard failed')
            raise
        finally:
            self.finish(token, details={'guard_completed': completed}, raised=not completed)

    def begin(self):
        self.identity_check()
        self.touch(self.app)
        self.touch(self.main)
        return self

    def summary(self):
        return {'initial_reads': self.initial_reads, 'initial_owner_composites': self.initial_owners,
                'capacity_counter_meaning': 'reserved attempt slots, not completion or native-call proof',
                'trace_records': len(self.trace), 'reserved_operations': self.op_count,
                'trace_receipt_duration_total': self.receipt_seconds, 'mode': self.mode,
                'phase': self.phase, 'pass': self.pass_no, 'stop_category': self.stopped,
                'experiment_end_elapsed': self.experiment_end-self.started,
                'reported_elapsed': self.io.clock()-self.started,
                'phase_remaining': self.end-self.io.clock(),
                'work_remaining': self.work_end-self.io.clock(),
                'initial_end_elapsed': None if self.readiness_end is None else self.readiness_end-self.started,
                'initial_completed_pass': self.initial_completed_pass,
                'proof_mode': self.PROOF_MODE,
                'phase_end_elapsed': self.end-self.started,
                'local_CF_type_and_equality_timing': 'uninstrumented',
                'non_trace_journal_timing': 'uninstrumented; included in wall/work time',
                'owner_duration_scope': 'SetMessagingTimeout(.2)+GetPid composite',
                'posting_and_event_allocation_timing': 'uninstrumented; fixed NativePosting unchanged',
                'core_startup_content_timing': 'uninstrumented by this trace; existing core receipts retained',
                'cleanup_and_paired_release_identity_timing': 'uninstrumented NativeSession.check'}

    def binding_refusal(self, category):
        return {'stage': 'binding', 'complete': False, 'error_category': category,
                'nodes': deepcopy(self.rows), 'distinct_refs': len(self.rows),
                'depth_cap': 3, 'reference_cap': 32, 'child_cap': 12,
                'semantic_handling': 'unknown', 'readiness': False,
                'trace': deepcopy(self.trace), 'budget': self.summary(),
                'target_proofs': deepcopy(self.completed_proofs)}

    def admit_read(self):
        self.check()
        if self.mode == 'initial':
            self.guard(self.initial_reads < 64, 'diagnostic initial read capacity')
        self.guard(self.io.clock()+.2 < self.end, 'diagnostic read headroom')

    def pass_capacity(self):
        self.admit_read()
        self.guard(self.initial_owners < 128, 'diagnostic initial owner capacity')

    def owner(self, ref, row):
        self.check()
        if self.mode == 'initial':
            self.guard(self.initial_owners < 128, 'diagnostic initial owner capacity')
        token = self.reserve('bounded_owner_composite', 'owner', row['ordinal'], .2)
        if self.mode == 'initial':
            self.initial_owners += 1
        rc, owner, completed = None, None, False
        try:
            rc, owner = self.b.owner(ref)  # existing exact-ref .2 setter + GetPid
            completed = True
        except BaseException:
            self.halt('diagnostic owner composite failed')
            raise
        finally:
            match = (owner == self.original['pid']) if rc == 0 else None
            self.set_property(row, 'owner_match', match, token)
            if completed and match is not True:
                self.halt('diagnostic foreign/unknown owner')
            self.finish(token, rc, 'pid', {'owner_match': match,
                        'duration_scope': 'SetMessagingTimeout(.2)+GetPid composite'},
                        row=row, raised=not completed)

    def touch(self, ref):
        self.check()
        for index, previous in enumerate(self.refs_seen):
            if self.same(ref, previous):
                return self.rows[index]
        self.guard(len(self.refs_seen) < 32, 'diagnostic distinct-reference cap')
        if self.mode == 'initial':
            self.guard(self.initial_owners < 128, 'diagnostic initial owner capacity')
        kind = self.b.kind(ref)['name']
        row = {'ordinal': len(self.rows), 'cf_type': kind if kind == 'AXUIElement' else 'other',
               'owner_match': None, 'role': None, 'parent_ordinal': None, 'reads': [],
               'property_meaning': 'last_observed_only_not_readiness', 'property_provenance': {},
               'array_observations': {}}
        self.refs_seen.append(ref)
        self.rows.append(row)
        self.set_property(row, 'cf_type', row['cf_type'])
        self.guard(kind == 'AXUIElement', 'diagnostic non-element reference')
        self.owner(ref, row)
        return row

    def read(self, ref, name, api, row, count=None):
        self.admit_read()
        token = self.reserve(self.APIS[api], name, row['ordinal'], .2)
        if self.mode == 'initial':
            self.initial_reads += 1
        completed, result = False, None
        try:
            if api == 'value':
                result = self.calls.value(ref, name, self.end)
            elif api == 'count':
                result = self.calls.count(ref, name, self.end)
            else:
                result = self.calls.refs(ref, name, count, self.end)
            completed = True
            return result, token
        except BaseException:
            self.halt('diagnostic structural call or decode failed')
            raise
        finally:
            native = self.calls.last_native
            rc = None if native is None else native['rc']
            details = {}
            if api == 'count':
                value = result[1] if completed and rc == 0 else None
                details = {'count': value if type(value) is int and 0 <= value <= 12 else None,
                           'over_limit': type(value) is int and value > 12}
            elif api == 'range':
                details = {'range_start': 0, 'requested_count': count}
            self.finish(token, rc, self.calls.last_cf_type, details, native, row, not completed)

    def read_status(self, rc, kind, api, name, row, optional=False):
        if rc == -25204 and self.mode == 'initial' and (api == 'count' or kind == 'null'):
            raise StructuralReadFailure(api, name, row['ordinal'], 'count' if api == 'count' else 'null')
        if optional and rc in (-25205, -25212):
            self.guard(api == 'count' or kind == 'null', 'diagnostic failed copy returned nonnull output')
            return False  # prior optional absence, never a successful zero count
        self.guard(rc == 0, 'diagnostic structural read failed')
        return True

    def value(self, ref, name):
        self.guard(name in self.VALUE_ATTRS, 'diagnostic attribute forbidden')
        self.admit_read()
        row = self.touch(ref)
        self.owner(ref, row)
        if name in ('AXParent', 'AXFocusedUIElement', 'AXTopLevelUIElement'):
            self.guard(len(self.refs_seen) < 32, 'diagnostic scalar-reference budget exhausted')
        (value, refs), token = self.read(ref, name, 'value', row)
        rc, kind = value['return_code'], value['type']['name']
        if not self.read_status(rc, kind, 'value', name, row, optional=name!='AXTopLevelUIElement'):
            return None
        if name in ('AXParent', 'AXFocusedUIElement', 'AXTopLevelUIElement'):
            self.guard(kind == 'AXUIElement' and len(refs) == 1, 'diagnostic scalar-reference type')
            target = refs[0]
            parent = self.touch(target)
            field = {'AXParent':'parent_ordinal','AXFocusedUIElement':'focused_ordinal',
                     'AXTopLevelUIElement':'top_level_ordinal'}[name]
            self.set_property(row, field, parent['ordinal'], token)
            return target
        if name == 'AXRole':
            self.guard(kind == 'CFString' and isinstance(value['value'], str), 'diagnostic role type')
            role = value['value'] if value['value'] in KNOWN_ROLES else 'unknown'
            self.set_property(row, 'role', role, token)
            return role
        self.guard(kind == 'CFBoolean' and type(value['value']) is bool, 'diagnostic modal type')
        return value['value']

    def role(self, ref):
        role = self.value(ref, 'AXRole')
        self.guard(role is not None, 'diagnostic mandatory role absent')
        return role

    def ref(self, ref, name):
        return self.value(ref, name)

    def refs(self, ref, name, optional=True):
        self.guard(name in self.ARRAY_ATTRS, 'diagnostic array forbidden')
        self.admit_read()
        row = self.touch(ref)
        self.owner(ref, row)
        (rc, count), count_token = self.read(ref, name, 'count', row)
        if not self.read_status(rc, 'count', 'count', name, row, optional=optional):
            return []
        self.guard(type(count) is int and 0 <= count <= 12, 'diagnostic child/count cap or type')
        if name == 'AXWindows':
            self.guard(count <= 4, 'diagnostic App window cap')
        if count == 0:
            row['array_observations'][name] = {'members': [], 'count': 0, 'count_op': count_token['op'],
                                               'range_op': None, 'phase': self.phase, 'pass': self.pass_no}
            return []
        self.guard(count <= 32-len(self.refs_seen), 'diagnostic prospective reference cap')
        self.admit_read()
        self.owner(ref, row)
        (rc, kind, refs), range_token = self.read(ref, name, 'range', row, count)
        self.read_status(rc, kind, 'range', name, row)
        self.guard(kind == 'CFArray' and len(refs) == count, 'diagnostic bounded range failed')
        seen = []
        for child in refs:
            self.guard(not any(self.same(child,old) for old in seen), 'diagnostic duplicate published reference')
            seen.append(child)
            self.touch(child)
        row['array_observations'][name] = {'members':[self.touch_ordinal(x) for x in refs], 'count':count,
                                           'count_op':count_token['op'],'range_op':range_token['op'],
                                           'phase':self.phase,'pass':self.pass_no}
        return refs

    def array_fact(self, ref, name):
        row = self.rows[self.touch_ordinal(ref)]
        return deepcopy(row['array_observations'][name])

    def edge(self, ref, field):
        row = self.rows[self.touch_ordinal(ref)]
        return {'source': row['ordinal'], 'target': row[field],
                **deepcopy(row['property_provenance'][field])}

    def parent(self, ref):
        target = self.ref(ref, 'AXParent')
        self.guard(target is not None, 'diagnostic mandatory parent absent')
        return target, self.edge(ref, 'parent_ordinal')

    def remember_pre_modal(self, ref):
        if self.same(ref,self.main):return
        if not any(self.same(ref,old) for old in self.pre_modal_refs):self.pre_modal_refs.append(ref)
        self.guard(len(self.pre_modal_refs)==1,'diagnostic additional published modal observed')
        if self.picker_anchor is not None:
            self.guard(self.same(ref,self.picker_anchor),'diagnostic retained picker changed')

    def publication(self, expected=None, post_root=None):
        """Actual standard memberships; AXWindows is not a sheet census."""
        self.check()
        self.guard(self.role(self.main)=='AXWindow','diagnostic original main role changed')
        windows=self.refs(self.app,'AXWindows',optional=False)
        self.guard(any(self.same(x,self.main) for x in windows),'diagnostic main not positively published')
        children=self.refs(self.main,'AXChildren',optional=False)
        self.guard(not any(self.same(x,self.main) or self.same(x,self.app) for x in children),
                   'diagnostic malformed main child root')
        union=[]
        for ref in windows+children:
            if not any(self.same(ref,x) for x in union):union.append(ref)
        candidates=[];edges=[]
        for ref in union:
            if self.same(ref,self.main):continue
            role=self.role(ref)
            self.guard(role!='unknown','diagnostic unknown publication role')
            in_children=any(self.same(ref,x) for x in children)
            in_windows=any(self.same(ref,x) for x in windows)
            if role in self.MODALS:
                if post_root is not None and self.same(ref,post_root):
                    self.guard(not in_children,'diagnostic related post sheet has wrong published parent')
                    continue  # relation through P was independently proved, never chosen here
                self.remember_pre_modal(ref)
                self.guard(role=='AXSheet','diagnostic unexpected published modal role')
                if expected is not None:self.guard(self.same(ref,expected),'diagnostic unexpected published sheet')
                self.guard(in_children,'diagnostic picker not original-main child publication')
                parent,edge=self.parent(ref);edges.append(edge)
                self.guard(self.same(parent,self.main),'diagnostic picker not direct original-main child')
                candidates.append(ref)
            else:
                self.guard(not in_windows,'diagnostic malformed App-window publication')
                if in_children:
                    parent,edge=self.parent(ref);edges.append(edge)
                    self.guard(self.same(parent,self.main),'diagnostic main child/parent mismatch')
        self.guard(len(candidates)==1,'diagnostic unique published PROJECT picker absent')
        candidate=candidates[0]
        if self.picker_anchor is None:self.picker_anchor=candidate
        self.guard(self.same(candidate,self.picker_anchor),'diagnostic retained picker changed')
        return candidate, {'app_windows':self.array_fact(self.app,'AXWindows'),
                           'main_children':self.array_fact(self.main,'AXChildren'),
                           'parent_edges':edges}

    def picker(self):
        self.identity_check()
        candidate,_=self.publication(self.picker_anchor)
        self.identity_check();self.check()
        return candidate

    def routing(self, picker):
        current=self.ref(self.app,'AXFocusedUIElement')
        focused=current;seen=[];path=[];edges=[];wrappers=[]
        self.guard(current is not None and not any(self.same(current,x) for x in (self.app,self.main,picker)),
                   'diagnostic focused element is not a nonmodal descendant')
        for _ in range(7):
            role=self.role(current);path.append(current)
            if self.same(current,picker):
                self.guard(role=='AXSheet','diagnostic picker role changed in ancestry')
                self.routing_path=[self.touch_ordinal(x) for x in path]
                return {'focused':focused,'path':path,'wrappers':wrappers,
                        'edges':edges,'focused_edge':self.edge(self.app,'focused_ordinal')}
            self.guard(role!='unknown' and role!='AXApplication' and role not in self.MODALS,
                       'diagnostic focused ancestry crosses unknown/modal')
            self.guard(not any(self.same(current,x) for x in seen),'diagnostic focused ancestry cycle')
            seen.append(current)
            if role in ('AXGroup','AXSplitGroup'):wrappers.append(current)
            if len(seen)>6:break
            parent,edge=self.parent(current);edges.append(edge)
            self.guard(parent is not None and not any(self.same(parent,x) for x in seen),
                       'diagnostic focused ancestry missing/cyclic')
            self.guard(not any(self.same(parent,x) for x in (self.app,self.main)),
                       'diagnostic focused ancestry misses picker')
            current=parent
        self.guard(False,'diagnostic focused ancestry too deep')

    def top_level(self, focused, picker):
        top=self.ref(focused,'AXTopLevelUIElement')  # MANDATORY, never inferred/fallback
        self.guard(top is not None and self.same(top,picker),'diagnostic focused top-level mismatch')
        self.guard(self.role(top)=='AXSheet','diagnostic top-level is not retained Sheet')
        parent,parent_edge=self.parent(top)
        self.guard(self.same(parent,self.main),'diagnostic top-level direct parent changed')
        return {'top':top,'edge':self.edge(focused,'top_level_ordinal'),'parent_edge':parent_edge}

    def legacy_veto(self, picker):
        """Provider-specific negative observation, never positive authority."""
        self.admit_read();row=self.touch(picker);self.owner(picker,row)
        (rc,count),token=self.read(picker,'AXSheets','count',row)
        if rc in (-25205,-25212):
            return {'state':'unknown','count':None,'op':token['op']}
        self.read_status(rc,'count','count','AXSheets',row)
        self.guard(type(count) is int and 0<=count<=12,'diagnostic malformed legacy nested count')
        self.guard(count==0,'diagnostic known nonempty nested relation veto')
        return {'state':'published_zero_not_authority','count':0,'op':token['op']}

    def veto_boundary(self, picker, route):
        queue=[(picker,0)];seen=[];arrays=[];edges=[];opaque=[]
        while queue:
            ref,depth=queue.pop(0)
            self.guard(not any(self.same(ref,x) for x in seen),'diagnostic boundary cycle')
            seen.append(ref)
            if depth>=3:continue
            children=self.refs(ref,'AXChildren',optional=False)
            arrays.append({'container':self.touch_ordinal(ref),'publication':self.array_fact(ref,'AXChildren')})
            for child in children:
                role=self.role(child)
                self.guard(role!='unknown','diagnostic unknown veto-boundary role')
                if role in self.MODALS:
                    self.remember_pre_modal(child)
                    self.guard(False,'diagnostic published nested modal veto')
                parent,edge=self.parent(child);edges.append(edge)
                self.guard(self.same(parent,ref),'diagnostic boundary child/parent mismatch')
                if role in ('AXGroup','AXSplitGroup') and any(self.same(child,x) for x in route['wrappers']):
                    queue.append((child,depth+1))
                else:opaque.append(self.touch_ordinal(child))
        return {'arrays':arrays,'parent_edges':edges,'opaque_ordinals':opaque,
                'meaning':'bounded published veto boundary, not global empty-modal proof'}

    def positive_proof(self, expected=None):
        self.guard(self.io.project_pending is True,'diagnostic PROJECT purpose missing')
        self.identity_check()
        picker,publication=self.publication(expected)
        early=self.routing(picker)
        boundary=self.veto_boundary(picker,early)
        legacy=self.legacy_veto(picker)
        self.identity_check()
        fresh=self.routing(picker)
        self.guard(self.same(fresh['focused'],early['focused']),'diagnostic focus changed during proof')
        self.top_level(fresh['focused'],picker)
        self.identity_check()
        # Only focused/top-level confirmation follows the final identity guard: no catalog work.
        sealed_focus=self.ref(self.app,'AXFocusedUIElement')
        self.guard(self.same(sealed_focus,fresh['focused']),'diagnostic focus changed at final boundary')
        sealed_top=self.top_level(sealed_focus,picker)
        self.identity_check()  # full birth/path/hash after the final AX reads as well
        self.check()
        self.proof_count+=1
        public={'proof_id':self.proof_count,'proof_mode':self.PROOF_MODE,'phase':self.phase,'pass':self.pass_no,
                'app':self.touch_ordinal(self.app),'main':self.touch_ordinal(self.main),
                'picker':self.touch_ordinal(picker),'focused':self.touch_ordinal(sealed_focus),
                'top_level':self.touch_ordinal(sealed_top['top']),
                'publication':publication,'veto_boundary':boundary,'legacy_nested':legacy,
                'ancestry_edges':deepcopy(fresh['edges']),
                'focused_edge':self.edge(self.app,'focused_ordinal'),
                'top_level_edge':sealed_top['edge'],'picker_parent_edge':sealed_top['parent_edge'],
                'last_observation_op':self.op_count,'semantic_handling':'unknown','readiness':False}
        self.completed_proofs.append(deepcopy(public))
        return {'picker':picker,'focused':sealed_focus,'public':public}

    def initial_picker(self):
        """Four complete initial binding+routing passes; never used by strict reads."""
        self.guard(not self.initial_binding_used, 'diagnostic initial binding already consumed')
        self.initial_binding_used = True
        self.mode, self.phase, self.end = 'initial', 'initial', min(self.started+6, self.experiment_end-2)
        self.readiness_end = self.end
        complete = False
        try:
            self.pass_no = 1
            self.pass_capacity()
            self.begin()
            for attempt in range(1,5):
                self.pass_no = attempt
                self.pass_capacity()
                self.identity_check()
                self.owner(self.app, self.touch(self.app))
                self.owner(self.main, self.touch(self.main))
                try:
                    proof = self.positive_proof(self.picker_anchor)
                    candidate = proof['picker']
                    self.check()
                    complete = True
                    self.initial_completed_pass = attempt
                    return candidate
                except StructuralReadFailure:
                    if attempt == 4:
                        raise
                    self.pass_capacity()  # no provenance probe/pause if another pass cannot read
                    self.identity_check()
                    self.owner(self.app,self.touch(self.app))
                    self.owner(self.main,self.touch(self.main))
                    self.guard(self.io.clock()+.1+.2 < self.end, 'diagnostic initial pause headroom')
                    token = self.reserve('sleep')
                    try:
                        self.io.sleep(.1)
                    except BaseException:
                        self.halt('diagnostic pause failed')
                        raise
                    finally:
                        self.finish(token, details={'requested_sleep': .1})
            raise DiagnosticStop('diagnostic initial passes exhausted')
        finally:
            if not complete:
                self.halt('diagnostic initial observation failed')
            # Sealed on EVERY exit, without extending the single experiment/work ceiling.
            self.mode, self.phase, self.pass_no = 'strict', 'strict', 0
            self.end = min(self.experiment_end,self.work_end,self.io.clock()+2)

    def recheck(self, picker, after_intent=False):
        self.command_picker=None
        self.guard(self.mode=='strict','diagnostic positive proof is not strict')
        proof=self.positive_proof(picker)
        if after_intent:
            self.guard(self.intent_focus is not None and self.same(proof['focused'],self.intent_focus),
                       'diagnostic focused identity changed across intent')
            self.after_intent_proof=dict(deepcopy(proof['public']), before_intent_proof_id=self.intent_proof_id)
            self.command_picker=picker
        else:
            self.guard(self.intent_focus is None,'diagnostic before-intent proof already consumed')
            self.intent_focus=proof['focused'];self.intent_proof_id=proof['public']['proof_id']
        self.guard(self.op_count<511,'diagnostic input trace reserve')
        token=self.reserve('input_boundary')
        self.finish(token,details={'read_capacity_used':self.initial_reads,'owner_capacity_used':self.initial_owners})
        self.check()
        return deepcopy(proof['public'])

    def reciprocal_path(self, child, picker):
        current=child;seen=[];edges=[];arrays=[]
        for _ in range(4):  # at most three reciprocal links through public structural wrappers
            if self.same(current,picker):return {'parent_edges':edges,'arrays':arrays}
            self.guard(not any(self.same(current,x) for x in seen),'diagnostic related subtree cycle')
            self.guard(len(seen)<3,'diagnostic related path depth cap')
            seen.append(current)
            parent,edge=self.parent(current);edges.append(edge)
            self.guard(parent is not None,'diagnostic related parent missing')
            if not self.same(parent,picker):
                self.guard(self.role(parent) in ('AXGroup','AXSplitGroup'),
                           'diagnostic related path crosses private/unrelated root')
            children=self.refs(parent,'AXChildren',optional=False)
            self.guard(any(self.same(current,x) for x in children),'diagnostic related reciprocal edge absent')
            for sibling in children:
                role=self.role(sibling)
                self.guard(role!='unknown','diagnostic related publication has unknown role')
                self.guard(self.same(sibling,current) or role not in self.MODALS,
                           'diagnostic multiple/unrelated post modal')
                actual,sibling_edge=self.parent(sibling);edges.append(sibling_edge)
                self.guard(self.same(actual,parent),'diagnostic related child/parent mismatch')
            arrays.append({'container':self.touch_ordinal(parent),'publication':self.array_fact(parent,'AXChildren')})
            current=parent
        self.guard(False,'diagnostic related path does not reach retained picker')

    def snapshot(self, picker, after_post):
        require(not self.snapshot_used,'diagnostic snapshot already consumed')
        self.snapshot_used=True;self.phase='snapshot'
        self.end=min(self.end,self.experiment_end,self.work_end,self.io.clock()+1)
        root=None;complete=False;error=None;relation=None
        label='partial-observed-after-attempt' if after_post else 'partial-without-attempt'
        try:
            self.check();self.identity_check()
            self.guard(not after_post or self.same(self.command_picker,picker) and self.after_intent_proof is not None,
                       'diagnostic positive after-intent proof unavailable')
            focused=self.ref(self.app,'AXFocusedUIElement')
            self.guard(focused is not None and not any(self.same(focused,x) for x in (self.app,self.main,picker)),
                       'diagnostic post focused descendant absent')
            top=self.ref(focused,'AXTopLevelUIElement')
            self.guard(top is not None and self.role(top)=='AXSheet','diagnostic post top-level is not Sheet')
            if self.same(top,picker):
                candidate=picker
                relation={'kind':'retained-picker','top_level_edge':self.edge(focused,'top_level_ordinal')}
            else:
                self.guard(after_post,'diagnostic different top-level without command attempt')
                relation={'kind':'positively-related-sheet','path':self.reciprocal_path(top,picker),
                          'top_level_edge':self.edge(focused,'top_level_ordinal')}
                candidate=top
            retained,publication=self.publication(picker,None if self.same(candidate,picker) else candidate)
            self.guard(self.same(retained,picker),'diagnostic retained picker publication changed')
            route=self.routing(candidate)  # fresh focused ancestry, not routing/handling ground truth
            confirmed=self.ref(route['focused'],'AXTopLevelUIElement')
            self.guard(confirmed is not None and self.same(confirmed,candidate),
                       'diagnostic post focused top-level changed')
            self.owner(confirmed,self.touch(confirmed))
            relation.update(retained_publication=publication,
                            focused_edge=self.edge(self.app,'focused_ordinal'),
                            top_level_edge=self.edge(route['focused'],'top_level_ordinal'))
            root=candidate
            label=('retained-picker-observed-after-attempt' if after_post else 'retained-picker-observed-without-attempt') if self.same(root,picker) else 'related-sheet-observed-after-attempt'
            queue=[(root,0)];expanded=[]
            while queue:
                ref,depth=queue.pop(0)
                self.guard(not any(self.same(ref,x) for x in expanded),'diagnostic structural cycle')
                expanded.append(ref);role=self.role(ref);parent,edge=self.parent(ref)
                if depth==0:
                    expected_parent=self.main if self.same(root,picker) else self.refs_seen[relation['path']['parent_edges'][0]['target']]
                    self.guard(role=='AXSheet' and self.same(parent,expected_parent),
                               'diagnostic selected post root role/parent drift')
                if depth==0 or role in ('AXGroup','AXSplitGroup'):
                    if depth>=3:continue
                    for child in self.refs(ref,'AXChildren',optional=False):
                        child_role=self.role(child);actual,child_edge=self.parent(child)
                        self.guard(self.same(actual,ref),'diagnostic child/parent mismatch')
                        if child_role in ('AXGroup','AXSplitGroup') and any(self.same(child,x) for x in route['wrappers']):
                            queue.append((child,depth+1))
            self.identity_check();self.check();complete=True
        except BaseException as exc:
            error=exc.code if isinstance(exc,DiagnosticStop) else type(exc).__name__
        return {'label':label,'complete':complete,'error_category':error,'proof_mode':self.PROOF_MODE,
                'after_intent_positive_proof':deepcopy(self.after_intent_proof),
                'root_ordinal':None if root is None else self.touch_ordinal(root),
                'relation':deepcopy(relation),'nodes':deepcopy(self.rows),'distinct_refs':len(self.rows),
                'depth_cap':3,'reference_cap':32,'child_cap':12,'semantic_handling':'unknown','readiness':False,
                'trace':deepcopy(self.trace),'budget':self.summary(),'target_proofs':deepcopy(self.completed_proofs)}

    def touch_ordinal(self, ref):
        return next((i for i,old in enumerate(self.refs_seen) if self.same(old,ref)),None)


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
            before = structure.recheck(picker, after_intent=False)
            intent = {'original': deepcopy(structure.original), 'purpose': 'PROJECT-picker-structural-diagnostic',
                      'private_source_state': -1, 'virtual_key': 0x05, 'flags': 0x00120000,
                      'event_count': 2, 'picker_ordinal': structure.touch_ordinal(picker),
                      'app_ordinal': structure.touch_ordinal(structure.app),
                      'main_ordinal': structure.touch_ordinal(structure.main),
                      'proof_mode': structure.PROOF_MODE,
                      'positive_target_proof': deepcopy(before),
                      'focused_ancestry_ordinals': list(structure.routing_path),
                      'handling': 'unknown', 'no_repeat': True}
            record('diagnostic-navigation-intent', intent)  # failure sends no input
            structure.recheck(picker, after_intent=True)
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
        self.diagnostic = {'diagnostic_only': True, 'proof_mode': Structure.PROOF_MODE,
                           'semantic_handling': 'unknown', 'snapshot': None}
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
        self.structural_calls = StructuralCalls(self.backend, self.clock)  # signatures before launch
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
        structure = Structure(self, main, min(work_end, self.clock() + 8), work_end)
        picker = None
        dispatched = False
        try:
            picker = structure.initial_picker()  # complete initial binding+routing policy
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
            self.diagnostic['target_proofs'] = deepcopy(structure.completed_proofs)
            if picker is None:
                partial = structure.binding_refusal(self.diagnostic['refusal_category'])
                self.diagnostic['binding_refusal'] = partial
                self.record('diagnostic-binding-refusal', deepcopy(partial))
            else:
                snapshot = structure.snapshot(picker, dispatched)
                self.diagnostic['snapshot'] = snapshot
                self.record('diagnostic-structure', deepcopy(snapshot))
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
