"""Actual diagnostic algorithms with invented OS effects. No native calls."""
import ctypes as C
import runpy
from contextlib import contextmanager, ExitStack
from copy import deepcopy
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import j1_picker_diagnostic as d
from j1_stage_a_phase import Subject, NativeSession, View, Control, Refusal

S = Subject('invented-source', '/invented/App.app', 'dev.invented.test', '/invented/App.app/Contents/MacOS/app',
            'a' * 64, '/invented/packet/session/project', '/invented/app-data')
ORIGINAL = {'pid': 17, 'ppid': 1, 'uid': 501, 'ruid': 501,
            'start_sec': 10, 'start_usec': 20, 'executable': S.executable}


class Fn:
    def __init__(self, call):
        self.call = call
    def __call__(self, *args):
        return self.call(*args)


class Backend:
    def __init__(self):
        self.nodes = {
            1: {'role': 'AXApplication', 'AXWindows': [2, 3], 'AXFocusedUIElement': 4},
            2: {'role': 'AXWindow', 'AXParent': 1, 'AXSheets': [3], 'AXChildren': []},
            3: {'role': 'AXSheet', 'AXParent': 2, 'AXChildren': [5], 'AXSheets': []},
            4: {'role': 'AXTextField', 'AXParent': 5},
            5: {'role': 'AXGroup', 'AXParent': 3, 'AXChildren': [4, 6, 7]},
            6: {'role': 'owner-filename-SECRET', 'AXParent': 5, 'AXChildren': [8]},
            7: {'role': 'AXList', 'AXParent': 5, 'AXChildren': [8]},
            8: {'role': 'AXRow', 'AXParent': 7},
        }
        self.log, self.held, self.arrays, self.scalars = [], [], {}, {}
        self.on_count = None
        self.a = SimpleNamespace(AXUIElementGetAttributeValueCount=Fn(self.count),
                                 AXUIElementCopyAttributeValues=Fn(self.range),
                                 AXUIElementCopyAttributeValue=Fn(self.value_call))
        self.closed = False
    def equal(self, a, b):
        return a == b
    def kind(self, ref):
        return {'name': 'CFArray' if ref in self.arrays else
                self.scalars[ref][0] if ref in self.scalars else 'AXUIElement' if ref in self.nodes else 'null'}
    def owner(self, ref):
        self.log.append(('owner', ref))
        return 0, self.nodes[ref].get('owner', 17)
    def string(self, name):
        return name
    def attribute(self, ref, name):
        self.log.append(('attribute', ref, name))
        assert name in ('AXRole', 'AXParent', 'AXModal', 'AXFocusedUIElement'), name
        node = self.nodes[ref]
        value = node.get('role') if name == 'AXRole' else node.get(name)
        if value is None:
            return {'return_code': -25212, 'type': {'name': 'null'}, 'value': None}, []
        if name in ('AXParent', 'AXFocusedUIElement'):
            return {'return_code': 0, 'type': {'name': 'AXUIElement'}, 'value': None}, [value]
        return {'return_code': 0, 'type': {'name': 'CFString' if name == 'AXRole' else 'CFBoolean'}, 'value': value}, []
    def value_call(self, ref, name, out):
        row, refs = self.attribute(ref, name)
        if row['return_code'] != 0: return row['return_code']
        if refs: pointer = refs[0]
        else:
            pointer = 2000 + len(self.scalars)
            self.scalars[pointer] = (row['type']['name'], row['value'])
        C.cast(out,C.POINTER(C.c_void_p))[0] = pointer
        return 0
    def scalar(self, pointer):
        return self.scalars[pointer][1]
    def count(self, ref, name, out):
        self.log.append(('count', ref, name))
        if self.on_count:
            self.on_count(ref, name)
        value = self.nodes[ref].get(name)
        if value is None:
            return -25212
        C.cast(out, C.POINTER(C.c_long))[0] = len(value)
        return 0
    def range(self, ref, name, start, count, out):
        self.log.append(('range', ref, name, start, count))
        assert start == 0 and 0 < count <= 12
        pointer = 1000 + len(self.arrays)
        self.arrays[pointer] = self.nodes[ref][name][:count]
        C.cast(out, C.POINTER(C.c_void_p))[0] = pointer
        return 0
    def array(self, ref, bound):
        self.log.append(('decode-array',ref))
        assert len(self.arrays[ref]) <= bound
        return self.arrays[ref]
    def close(self):
        self.closed = True
        self.held.clear()


class Posting:
    def __init__(self):
        self.calls, self.freed, self.posts = [], [], []
        self.allowed, self.allocate_fail = True, None
        self.post_error, self.on_down = False, None
    def preflight(self):
        self.calls.append(('preflight',))
        return self.allowed
    def source(self):
        self.calls.append(('source', -1))
        return None if self.allocate_fail == 0 else 101
    def event(self, source, down):
        self.calls.append(('event', source, 0x05, down))
        number = 102 if down else 103
        return None if self.allocate_fail == (1 if down else 2) else number
    def flags(self, event):
        self.calls.append(('flags', event, 0x00120000))
    def post(self, original, event):
        self.posts.append((deepcopy(original), event))
        if event == 102 and self.on_down:
            self.on_down()
        if event == 102 and self.post_error:
            raise OSError('invented unknown native return')
    def release(self, value):
        self.freed.append(value)


def context():
    now, backend = [0.0], Backend()
    identity = deepcopy(ORIGINAL)
    def check(value):
        if value != identity:
            raise Refusal('invented original changed')
    io = SimpleNamespace(backend=backend, identity=identity, ax=SimpleNamespace(app=1, main=2),
                         clock=lambda: now[0], check=check, project_pending=True)
    io.structural_calls = d.StructuralCalls(backend)
    return d.Structure(io, 2, 2), io, backend, now


class StructuralTests(unittest.TestCase):
    def test_real_bind_route_snapshot_privacy_and_range_order(self):
        structure, io, b, now = context()
        picker = structure.picker()
        self.assertEqual(structure.routing(picker), [3, 4, 2])  # local ordinals, no addresses
        result = structure.snapshot(picker, False)
        self.assertTrue(result['complete'])
        self.assertEqual(result['label'], 'retained-picker-no-command')
        self.assertFalse(result['readiness'])
        self.assertNotIn('SECRET', repr(result))
        self.assertEqual(next(row for row in result['nodes'] if row['ordinal'] == structure.touch_ordinal(6))['role'], 'unknown')
        self.assertFalse(any(row[:3] in (('count', 6, 'AXChildren'), ('count', 7, 'AXChildren')) for row in b.log))
        self.assertFalse(any(row[0] == 'attribute' and row[2] in ('AXTitle', 'AXDescription', 'AXValue') for row in b.log))
        for index, row in enumerate(b.log):
            if row[0] == 'range':
                self.assertIn(('count', row[1], row[2]), b.log[:index])

    def test_missing_foreign_cycle_unrelated_and_depth_routes_refuse(self):
        for case in ('missing', 'foreign', 'cycle', 'unrelated', 'deep'):
            with self.subTest(case=case):
                s, io, b, now = context(); picker = s.picker()
                if case == 'missing': b.nodes[1].pop('AXFocusedUIElement')
                if case == 'foreign': b.nodes[4]['owner'] = 999
                if case == 'cycle': b.nodes[5]['AXParent'] = 4
                if case == 'unrelated': b.nodes[4]['AXParent'] = 1
                if case == 'deep':
                    for n in range(10, 17): b.nodes[n] = {'role': 'AXGroup', 'AXParent': n + 1 if n < 16 else 3}
                    b.nodes[4]['AXParent'] = 10
                with self.assertRaises(Refusal): s.routing(picker)
                if case == 'foreign':
                    self.assertFalse(any(row[0] == 'attribute' and row[1] == 4 for row in b.log))

    def test_routing_refusal_still_allows_safe_bound_picker_snapshot(self):
        s, io, b, now = context(); picker = s.picker()
        b.nodes[1].pop('AXFocusedUIElement')
        with self.assertRaises(Refusal): s.routing(picker)
        self.assertTrue(s.snapshot(picker, False)['complete'])

    def test_new_related_sheet_or_unchanged_picker_only(self):
        s, io, b, now = context(); picker = s.picker()
        b.nodes[9] = {'role': 'AXSheet', 'AXParent': 3, 'AXChildren': []}
        b.nodes[3]['AXSheets'] = [9]
        result = s.snapshot(picker, True)
        self.assertTrue(result['complete'])
        self.assertEqual(result['label'], 'new-related-subtree-semantics-unknown')
        self.assertEqual(result['semantic_handling'], 'unknown')

    def test_unrelated_or_ambiguous_windows_fail_before_post(self):
        for extra in ([9], [9, 10]):
            s, io, b, now = context()
            for n in extra: b.nodes[n] = {'role': 'AXSheet', 'AXParent': 1}
            b.nodes[1]['AXWindows'] += extra
            with self.assertRaises(Refusal): s.picker()

    def test_count_cap_refuses_before_range_and_no_full_array_fetch(self):
        s, io, b, now = context(); picker = s.picker()
        b.nodes[3]['AXChildren'] = list(range(20, 33))
        result = s.snapshot(picker, False)
        self.assertFalse(result['complete'])
        self.assertFalse(any(row[0] == 'range' and row[1:3] == (3, 'AXChildren') for row in b.log))

    def test_distinct_budget_is_shared_and_prevents_large_fetch(self):
        s, io, b, now = context(); picker = s.picker()
        for n in range(20, 47):
            b.nodes[n] = {'role': 'AXButton', 'AXParent': 3}
            s.touch(n)
        self.assertLessEqual(len(s.rows), 32)
        result = s.snapshot(picker, False)
        self.assertFalse(result['complete'])
        self.assertLessEqual(result['distinct_refs'], 32)

    def test_depth_cap_and_private_leaf_classes(self):
        s, io, b, now = context(); picker = s.picker()
        b.nodes[5]['AXChildren'] = [10]
        for n in (10, 11, 12): b.nodes[n] = {'role': 'AXGroup', 'AXParent': n - 1 if n > 10 else 5, 'AXChildren': [n + 1]}
        result = s.snapshot(picker, False)
        self.assertTrue(result['complete'])
        self.assertFalse(any(row[:3] == ('count', 11, 'AXChildren') for row in b.log))
        for role in ('AXBrowser', 'AXTable', 'AXOutline', 'AXList', 'AXRow', 'AXCell', 'AXScrollArea',
                     'AXPathControl', 'AXPopUpButton', 'AXMenu', 'AXMenuBar', 'AXToolbar', 'AXTextField'):
            s, io, b, now = context(); b.nodes[7]['role'] = role
            s.snapshot(s.picker(), False)
            self.assertFalse(any(row[:3] == ('count', 7, 'AXChildren') for row in b.log), role)

    def test_cutoff_and_partial_range_error_never_promote(self):
        s, io, b, now = context(); picker = s.picker()
        b.on_count = lambda *args: now.__setitem__(0, 1.1)
        result = s.snapshot(picker, False)
        self.assertFalse(result['complete'])
        self.assertFalse(result['readiness'])
        with self.assertRaises(Refusal): s.snapshot(picker, False)

    def test_range_error_records_partial_and_foreign_child_is_not_followed(self):
        s, io, b, now = context(); picker = s.picker()
        b.a.AXUIElementCopyAttributeValues = Fn(lambda *a:-25204)
        io.structural_calls = d.StructuralCalls(b); s.calls = io.structural_calls
        result = s.snapshot(picker, False)
        self.assertFalse(result['complete'])
        self.assertNotIn('SECRET', repr(result))
        s, io, b, now = context(); picker = s.picker(); b.nodes[7]['owner'] = 999
        result = s.snapshot(picker, False)
        self.assertFalse(result['complete'])
        self.assertFalse(any(row[0] in ('count','range','attribute') and row[1] == 7 for row in b.log))

    def test_new_sheet_ambiguity_and_parent_cycle_remain_partial(self):
        s, io, b, now = context(); picker = s.picker()
        for n in (9,10): b.nodes[n] = {'role':'AXSheet','AXParent':3,'AXChildren':[]}
        b.nodes[3]['AXSheets'] = [9,10]
        self.assertFalse(s.snapshot(picker, True)['complete'])
        s, io, b, now = context(); picker = s.picker()
        b.nodes[5]['AXParent'] = 5
        self.assertFalse(s.snapshot(picker, False)['complete'])

    def test_wrong_scalar_array_type_is_not_decoded(self):
        s, io, b, now = context()
        b.arrays[9000] = list(range(100))
        def wrong(ref,name,out):
            C.cast(out,C.POINTER(C.c_void_p))[0] = 9000
            return 0
        b.a.AXUIElementCopyAttributeValue = Fn(wrong)
        s.calls = d.StructuralCalls(b)
        with self.assertRaises(Refusal): s.role(3)
        self.assertFalse(any(row[0] == 'decode-array' for row in b.log))


class GestureTests(unittest.TestCase):
    def test_private_fixed_pair_original_pid_and_release(self):
        s, io, b, now = context(); picker = s.picker(); api = Posting(); records = []
        gesture = d.FixedGesture(api)
        result = gesture.run(s, picker, lambda k, v: records.append((k, v)))
        self.assertEqual(api.calls, [('source', -1), ('event', 101, 5, True), ('flags', 102, 0x120000),
                                     ('event', 101, 5, False), ('flags', 103, 0x120000)])
        self.assertEqual([p[0] for p in api.posts], [ORIGINAL, ORIGINAL])
        self.assertEqual([p[1] for p in api.posts], [102, 103])
        self.assertEqual(api.freed, [103, 102, 101])
        self.assertEqual(result['handling'], 'unknown')
        self.assertEqual(records[0][1]['event_count'], 2)
        with self.assertRaises(Refusal): gesture.run(s, picker, lambda *a: None)
        self.assertEqual(len(api.posts), 2)

    def test_wrong_identity_stale_ref_and_route_send_zero_posts(self):
        for case in ('identity', 'main', 'app', 'picker', 'purpose', 'routing', 'cutoff'):
            s, io, b, now = context(); picker = s.picker(); api = Posting()
            if case == 'identity': io.identity['start_usec'] += 1
            if case == 'main': io.ax.main = 90
            if case == 'app': io.ax.app = 90
            if case == 'picker': b.nodes[2]['AXSheets'] = [] ; b.nodes[1]['AXWindows'] = [2]
            if case == 'purpose': io.project_pending = False
            if case == 'routing': b.nodes[4]['AXParent'] = 1
            if case == 'cutoff': now[0] = 2
            with self.assertRaises(Refusal): d.FixedGesture(api).run(s, picker, lambda *a: None)
            self.assertEqual(api.posts, [], case)
            self.assertEqual(sorted(api.freed), [101, 102, 103])

    def test_final_recheck_after_intent_and_callback_cannot_rebind(self):
        s, io, b, now = context(); picker = s.picker(); api = Posting()
        def receipt(kind, value):
            value['original']['pid'] = 999
            b.nodes[4]['AXParent'] = 1
        with self.assertRaises(Refusal): d.FixedGesture(api).run(s, picker, receipt)
        self.assertEqual(api.posts, [])
        self.assertEqual(s.original, ORIGINAL)

    def test_receipt_failure_before_dispatch_consumes_and_releases(self):
        s, io, b, now = context(); picker = s.picker(); api = Posting(); g = d.FixedGesture(api)
        def fail(*args): raise OSError('invented receipt failure')
        with self.assertRaises(OSError): g.run(s, picker, fail)
        self.assertEqual(api.posts, [])
        self.assertTrue(g.used)
        self.assertEqual(api.freed, [103, 102, 101])
        with self.assertRaises(Refusal): g.run(s, picker, lambda *a: None)

    def test_unknown_down_gets_one_paired_up_but_never_a_retry(self):
        s, io, b, now = context(); picker = s.picker(); api = Posting(); api.post_error = True
        g = d.FixedGesture(api)
        with self.assertRaises(OSError): g.run(s, picker, lambda *a: None)
        self.assertEqual([p[1] for p in api.posts], [102, 103])
        with self.assertRaises(Refusal): g.run(s, picker, lambda *a: None)
        self.assertEqual(g.status()['handling'], 'unknown')

    def test_identity_drift_skips_up_and_never_targets_replacement(self):
        s, io, b, now = context(); picker = s.picker(); api = Posting()
        api.on_down = lambda: io.identity.update(start_usec=21)
        with self.assertRaises(Refusal): d.FixedGesture(api).run(s, picker, lambda *a: None)
        self.assertEqual(api.posts, [(ORIGINAL, 102)])
        self.assertEqual(api.freed, [103, 102, 101])

    def test_null_allocations_free_every_successful_allocation(self):
        for which, expected in ((0, []), (1, [101]), (2, [102, 101])):
            s, io, b, now = context(); api = Posting(); api.allocate_fail = which
            with self.assertRaises(Refusal): d.FixedGesture(api).run(s, s.picker(), lambda *a: None)
            self.assertEqual(api.freed, expected)
            self.assertEqual(api.posts, [])

    def test_flags_and_release_exceptions_release_remaining_objects(self):
        s, io, b, now = context(); api = Posting()
        def flags(event): raise OSError('invented flags failure')
        api.flags = flags
        with self.assertRaises(OSError): d.FixedGesture(api).run(s,s.picker(),lambda *a:None)
        self.assertEqual(api.freed,[102,101]); self.assertEqual(api.posts,[])
        s, io, b, now = context(); api = Posting(); old_release = api.release
        def release(value):
            old_release(value)
            if value == 103: raise OSError('invented release failure')
        api.release = release; g = d.FixedGesture(api)
        with self.assertRaises(Refusal): g.run(s,s.picker(),lambda *a:None)
        self.assertEqual(api.freed,[103,102,101]); self.assertTrue(g.used)
        self.assertEqual(g.status()['release_errors'],['OSError'])

    def test_event_allocation_exception_still_releases_private_source(self):
        s, io, b, now = context(); api = Posting()
        def event(*a): raise OSError('invented allocation error')
        api.event = event
        with self.assertRaises(OSError): d.FixedGesture(api).run(s,s.picker(),lambda *a:None)
        self.assertEqual(api.freed,[101]); self.assertEqual(api.posts,[])


class AdmissionAndRunTests(unittest.TestCase):
    def full(self, allowed=True, unavailable=False, fail_record=None, configure=None):
        now, backend, api, records = [0.0], Backend(), Posting(), []
        api.allowed = allowed
        appkit = SimpleNamespace(closed=False, terminations=0)
        @contextmanager
        def target(pid):
            self.assertEqual(pid, 17)
            yield 'exact-original'
        appkit.target = target
        appkit.describe = lambda t: {'pid': 17, 'bundle_identifier': S.identifier, 'executable': S.executable}
        def terminate(t):
            appkit.terminations += 1
            appkit.closed = not hasattr(backend,'late_close_at')
            return appkit.closed
        appkit.terminate = terminate
        counts = {'launches': 0, 'admit': 0}
        def admit(io, subject):
            counts['admit'] += 1
            io.backend, io.appkit = backend, appkit
            io.record('admitted', {'mocked': True})
        def launch(io, subject):
            counts['launches'] += 1
            io.identity = deepcopy(ORIGINAL)
            return deepcopy(io.identity)
        def check(io, identity):
            if io.identity != identity: raise Refusal('invented identity mismatch')
        def main(io, subject, end):
            io.ax = SimpleNamespace(app=1, main=2, last_phase='main')
            return 2
        def observe(io, main, phase, end):
            assert phase == 'main'
            return View(2, 2, [Control(4, 'AXButton', 'Choose project folder…', True),
                Control(10, 'AXRadioButton', 'Start with new settings', True),
                Control(11, 'AXButton', 'Review setup', False)], '', True)
        def record(kind, value):
            if kind == fail_record: raise OSError('invented receipt failure')
            records.append((kind, deepcopy(value)))
        def factory():
            if unavailable: raise AttributeError('invented missing API')
            return api
        if configure: configure(backend, api, now)
        with ExitStack() as stack:
            for name, fn in {'admit': admit, 'launch_once': launch, 'check': check,
                'original_main': main, 'startup_facts': lambda io: {'root_count':1,'self_reference_count':0,'match_count':1,'transient_return_category':'ready'},
                'observe': observe, 'revalidate': lambda io,v,c,end:c, 'press':lambda io,c,end:0,
                'supplier_started':lambda io:False,
                'absent':lambda io,i:appkit.closed or now[0] >= getattr(backend,'late_close_at',float('inf'))}.items():
                stack.enter_context(patch.object(NativeSession, name, fn))
            stack.enter_context(patch.object(d, 'NativePosting', factory))
            result = d.run_prepared(S, {}, record, lambda:now[0], lambda n:now.__setitem__(0,now[0]+n))
        return result, counts, api, backend, appkit, records

    def test_false_or_unavailable_preflight_zero_launches(self):
        for options in ({'allowed':False}, {'unavailable':True}):
            result, counts, api, b, app, records = self.full(**options)
            self.assertEqual(counts, {'launches':0,'admit':0})
            self.assertEqual(api.posts, [])
            self.assertFalse(result['setup_saved'])
            self.assertTrue(result['original_absent'])
            preflight = next(v for k,v in records if k == 'diagnostic-posting-preflight')
            self.assertGreater(preflight['caller']['pid'],0)
            self.assertEqual(len(preflight['caller']['sha256']),64)

    def test_actual_diagnostic_run_cleanup_and_no_readiness_promotion(self):
        result, counts, api, b, app, records = self.full()
        self.assertEqual(counts['launches'], 1)
        self.assertEqual(app.terminations, 1)
        self.assertTrue(b.closed)
        self.assertTrue(result['original_absent'])
        for key in ('setup_saved','J1_complete','qualification','flow_complete'): self.assertFalse(result[key])
        self.assertEqual(result['actions'], ['open project picker'])
        self.assertTrue(result['diagnostic']['snapshot']['complete'])
        self.assertEqual(len(api.posts), 2)
        self.assertIn('final-closure', [k for k,v in records])

    def test_receipt_failures_do_not_skip_autonomous_cleanup(self):
        for kind in ('diagnostic-navigation-intent','diagnostic-structure','cleanup-intent','normal-terminate-intent'):
            result, counts, api, b, app, records = self.full(fail_record=kind)
            self.assertEqual(app.terminations, 1, kind)
            self.assertTrue(result['original_absent'])
            if kind == 'diagnostic-navigation-intent': self.assertEqual(api.posts, [])

    def test_routing_refusal_zero_posts_but_snapshot_and_cleanup(self):
        def configure(b, api, now): b.nodes[1].pop('AXFocusedUIElement')
        result, counts, api, b, app, records = self.full(configure=configure)
        self.assertEqual(api.posts, [])
        self.assertTrue(result['diagnostic']['snapshot']['complete'])
        self.assertEqual(app.terminations, 1)

    def test_cutoff_after_pair_returns_partial_and_starts_cleanup(self):
        def configure(b, api, now): api.on_down = lambda:now.__setitem__(0,110)
        result, counts, api, b, app, records = self.full(configure=configure)
        self.assertEqual(result['cleanup_started'], 110)
        self.assertFalse(result['diagnostic']['snapshot']['complete'])
        self.assertTrue(result['cleanup_within_reserved_interval'])
        self.assertEqual(app.terminations, 1)

    def test_diagnostic_path_write_and_save_always_refuse(self):
        session = d.DiagnosticSession(S, {}, lambda *a:None)
        with self.assertRaises(Refusal): session.enter_path(None,S.project,0)
        with self.assertRaises(Refusal): session.verify_saved(S,{})
        session.experiment_used = True
        with self.assertRaises(Refusal): session.experiment(2,110)

    def test_late_absence_retains_custody_without_second_termination(self):
        def configure(b,api,now): b.late_close_at = 182
        result, counts, api, b, app, records = self.full(configure=configure)
        self.assertEqual(app.terminations,1)
        self.assertTrue(result['initial_held'])
        self.assertGreaterEqual(result['final_overrun'],2)
        self.assertTrue(result['original_absent'])
        self.assertFalse(result['slot_must_remain_held'])
        self.assertIn('held',[k for k,v in records]); self.assertIn('late-absence',[k for k,v in records])


class ABIOnlyTests(unittest.TestCase):
    def test_module_import_is_inert(self):
        with patch.object(d.C,'CDLL',side_effect=AssertionError('no native loader on import')):
            runpy.run_path(d.__file__)

    def test_real_abi_initializer_uses_fixed_symbols_without_native_load(self):
        seen = []
        def symbol(name):
            def call(*args):
                seen.append((name,args))
                return True if name == 'CGPreflightPostEventAccess' else 123
            return Fn(call)
        cg = SimpleNamespace(**{name:symbol(name) for name in ('CGPreflightPostEventAccess','CGEventSourceCreate',
            'CGEventCreateKeyboardEvent','CGEventSetFlags','CGEventPostToPid')})
        cf = SimpleNamespace(CFRelease=symbol('CFRelease'))
        with patch.object(d.C,'CDLL',side_effect=[cg,cf]): api = d.NativePosting()
        self.assertEqual(seen, [])
        self.assertEqual(cg.CGEventPostToPid.argtypes,[C.c_int32,C.c_void_p])
        self.assertIsNone(cg.CGEventPostToPid.restype)
        self.assertEqual(cg.CGEventSetFlags.argtypes,[C.c_void_p,C.c_uint64])
        self.assertEqual(cg.CGEventCreateKeyboardEvent.argtypes,[C.c_void_p,C.c_uint16,C.c_bool])
        self.assertTrue(api.preflight()); api.source(); api.event(123,True); api.flags(123); api.post(ORIGINAL,123); api.release(123)
        self.assertIn(('CGEventSourceCreate',(-1,)),seen)
        self.assertIn(('CGEventPostToPid',(17,123)),seen)


if __name__ == '__main__':
    unittest.main()
