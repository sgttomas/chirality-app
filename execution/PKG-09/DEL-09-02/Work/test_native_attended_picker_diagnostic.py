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
from native_b_diagnostic import NativeBackend as ReviewedBackend

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
            1: {'role': 'AXApplication', 'AXWindows': [2], 'AXFocusedUIElement': 4},
            2: {'role': 'AXWindow', 'AXParent': 1, 'AXSheets': [3], 'AXChildren': [3]},
            3: {'role': 'AXSheet', 'AXParent': 2, 'AXChildren': [5], 'AXSheets': []},
            4: {'role': 'AXTextField', 'AXParent': 5},
            5: {'role': 'AXGroup', 'AXParent': 3, 'AXChildren': [4, 6, 7]},
            6: {'role': 'AXButton', 'AXParent': 5, 'AXChildren': [8]},
            7: {'role': 'AXList', 'AXParent': 5, 'AXChildren': [8]},
            8: {'role': 'AXRow', 'AXParent': 7},
        }
        self.log, self.held, self.arrays, self.scalars = [], [], {}, {}
        self.on_count = None
        self.a = SimpleNamespace(AXUIElementGetAttributeValueCount=Fn(self.count),
                                 AXUIElementCopyAttributeValues=Fn(self.range),
                                 AXUIElementCopyAttributeValue=Fn(self.value_call),
                                 AXUIElementSetMessagingTimeout=Fn(self.timeout),
                                 AXUIElementGetPid=Fn(self.pid_call))
        self.closed = False
    def equal(self, a, b):
        return a == b
    def kind(self, ref):
        return {'name': 'CFArray' if ref in self.arrays else
                self.scalars[ref][0] if ref in self.scalars else 'AXUIElement' if ref in self.nodes else 'null'}
    def owner(self, ref):
        return ReviewedBackend.owner(self,ref)  # actual reviewed helper; fake OS calls below
    def bounded_element(self, ref):
        d.require(self.kind(ref)['name']=='AXUIElement','invented non-element')
        d.require(self.a.AXUIElementSetMessagingTimeout(ref,.2)==0,'invented timeout setup failed')
    def timeout(self, ref, seconds):
        self.log.append(('timeout-exact',ref,seconds))
        return 0
    def pid_call(self, ref, out):
        self.log.append(('owner', ref))
        C.cast(out,C.POINTER(C.c_int))[0]=self.nodes[ref].get('owner',17)
        return 0
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


def context(initial=False):
    now, backend = [0.0], Backend()
    identity = deepcopy(ORIGINAL)
    def check(value):
        if value != identity:
            raise Refusal('invented original changed')
    io = SimpleNamespace(backend=backend, identity=identity, ax=SimpleNamespace(app=1, main=2),
                         clock=lambda: now[0], check=check, project_pending=True,
                         sleep=lambda n:now.__setitem__(0,now[0]+n), record=lambda *a:None)
    io.structural_calls = d.StructuralCalls(backend,io.clock)
    structure=d.Structure(io,2,8 if initial else 2,110)
    return (structure if initial else structure.begin()),io,backend,now


def observed_shape(b):
    """Invented safe roles in the observed six-child/five-link geometry, no UI text."""
    for n,role in zip(range(10,15),('AXGroup','AXButton','AXButton','AXButton','AXStaticText')):
        b.nodes[n]={'role':role,'AXParent':2}
    b.nodes[2]['AXChildren']=[10,11,12,13,14,3]
    b.nodes[4].update(role='AXOutline',AXParent=20)
    b.nodes[20]={'role':'AXScrollArea','AXParent':21}
    b.nodes[21]={'role':'AXSplitGroup','AXParent':22,'AXChildren':[20]}
    b.nodes[22]={'role':'AXSplitGroup','AXParent':3,'AXChildren':[21]}
    b.nodes[3]['AXChildren']=[22]
    b.nodes[2].pop('AXSheets',None);b.nodes[3].pop('AXSheets',None)


def small_positive(b):
    b.nodes[3]['AXChildren']=[4];b.nodes[4]['AXParent']=3


def related_after(b):
    b.nodes[9]={'role':'AXSheet','AXParent':3,'AXChildren':[10]}
    b.nodes[10]={'role':'AXTextField','AXParent':9}
    b.nodes[3]['AXChildren']=[5,9];b.nodes[1]['AXFocusedUIElement']=10


class ReturnedReferenceEvidenceTests(unittest.TestCase):
    def test_foreign_range_ref_retains_actual_return_before_owner_refusal(self):
        s, io, b, now = context(initial=True)
        observed_shape(b)
        b.nodes[22]['AXChildren'] = list(range(24, 36))
        for ref in range(24, 36):
            b.nodes[ref] = {'role': 'SECRET', 'AXParent': 22, 'owner': 999 if ref == 25 else 17}
        with self.assertRaisesRegex(Refusal, 'foreign/unknown owner'):
            s.initial_picker()
        report = s.binding_refusal(s.stopped)
        row = report['nodes'][s.touch_ordinal(25)]
        origin = row['first_return']
        self.assertEqual(origin['source_ordinal'], s.touch_ordinal(22))
        self.assertEqual((origin['attribute'], origin['output_index'], origin['requested_count']),
                         ('AXChildren', 1, 12))
        self.assertEqual(origin['meaning'], 'native-return-only-not-ownership-parent-or-readiness')
        call = next(e for e in report['trace'] if e['op'] == origin['op'])
        self.assertEqual((call['api'], call['attribute'], call['ordinal'], call['return_code']),
                         ('AXUIElementCopyAttributeValues', 'AXChildren', s.touch_ordinal(22), 0))
        self.assertEqual(row['owner_pid'], 999)
        self.assertFalse(row['owner_match'])
        self.assertIsNone(row['role']); self.assertIsNone(row['parent_ordinal'])
        self.assertNotIn('AXChildren', report['nodes'][s.touch_ordinal(22)]['array_observations'])
        self.assertIsNone(s.initial_completed_pass); self.assertEqual(report['target_proofs'], [])
        self.assertFalse(any(e[0] in ('attribute', 'count', 'range') and e[1] == 25 for e in b.log))
        self.assertFalse(any(e[0] == 'owner' and e[1] == 26 for e in b.log))
        self.assertNotIn('SECRET', repr(report))

    def test_foreign_scalar_ref_retains_return_without_publishing_a_proved_edge(self):
        for name, source, target, field in (('AXFocusedUIElement', 1, 4, 'focused_ordinal'),
                                           ('AXParent', 4, 5, 'parent_ordinal')):
            with self.subTest(name=name):
                s, io, b, now = context()
                b.nodes[target]['owner'] = 999
                with self.assertRaisesRegex(Refusal, 'foreign/unknown owner'):
                    s.ref(source, name)
                row = s.rows[s.touch_ordinal(target)]
                origin = row['last_return']
                self.assertEqual(origin['source_ordinal'], s.touch_ordinal(source))
                self.assertEqual((origin['api'], origin['attribute'], origin['output_index'], origin['requested_count']),
                                 ('AXUIElementCopyAttributeValue', name, 0, None))
                self.assertIsNone(s.rows[s.touch_ordinal(source)].get(field))
                self.assertEqual(row['owner_pid'], 999)
                self.assertIsNone(row['role']); self.assertIsNone(row['parent_ordinal'])
                self.assertFalse(any(e[0] in ('attribute', 'count', 'range') and e[1] == target for e in b.log))

    def test_owner_pid_is_only_the_successful_existing_integer_output(self):
        for rc, pid in ((0, 17), (0, 999), (0, 0), (0, -1), (-25202, 999),
                        (None, 999), (0, 'SECRET'), (0, 2**40), (0, True)):
            with self.subTest(rc=rc, pid=pid):
                s, io, b, now = context()
                b.owner = lambda ref: (rc, pid)
                if rc == 0 and pid == 17:
                    s.owner(1, s.rows[0])
                else:
                    with self.assertRaises(Refusal): s.owner(1, s.rows[0])
                expected = pid if rc == 0 and type(pid) is int and -(2**31) <= pid < 2**31 else None
                row, event = s.rows[0], s.trace[-1]
                self.assertEqual(row['owner_pid'], expected)
                self.assertEqual(event['owner_pid'], expected)
                self.assertEqual(row['property_provenance']['owner_pid']['op'], event['op'])
                self.assertNotIn('SECRET', repr(s.binding_refusal(s.stopped)))
        s, io, b, now = context()
        b.a.AXUIElementSetMessagingTimeout = Fn(lambda *a: -25202)
        with self.assertRaises(Refusal): s.owner(1, s.rows[0])
        self.assertIsNone(s.rows[0]['owner_pid']); self.assertIsNone(s.trace[-1]['owner_pid'])

    def test_alias_and_repeated_returns_keep_two_bounded_detached_observations(self):
        s, io, b, now = context()
        s.ref(1, 'AXFocusedUIElement')
        row = s.rows[s.touch_ordinal(4)]
        first = deepcopy(row['first_return'])
        b.nodes[44] = deepcopy(b.nodes[4])
        b.equal = lambda left, right: (4 if left == 44 else left) == (4 if right == 44 else right)
        b.nodes[1]['AXFocusedUIElement'] = 44
        for _ in range(100): s.ref(1, 'AXFocusedUIElement')
        self.assertEqual(row['first_return'], first)
        self.assertGreater(row['last_return']['op'], first['op'])
        self.assertEqual(len(s.rows), 3)
        self.assertLessEqual(sum(r[key] is not None for r in s.rows for key in ('first_return', 'last_return')), 64)
        s.role(44)
        self.assertIn(('timeout-exact', 44, .2), b.log); self.assertIn(('owner', 44), b.log)
        report = s.binding_refusal('invented-report')
        copy = report['nodes'][row['ordinal']]
        copy['first_return']['op'] = -1; copy['last_return']['source_ordinal'] = 31; copy['owner_pid'] = 666
        self.assertEqual(row['first_return'], first)
        self.assertEqual(row['last_return']['source_ordinal'], 0)
        self.assertEqual(row['owner_pid'], 17)

    def test_late_or_failed_range_has_no_return_provenance_or_foreign_follow(self):
        for case in ('late', 'error', 'wrong-type', 'wrong-size'):
            with self.subTest(case=case):
                s, io, b, now = context()
                original = b.a.AXUIElementCopyAttributeValues.call
                def returned(ref, name, start, count, out):
                    rc = original(ref, name, start, count, out)
                    if case == 'late': now[0] = 2.01
                    elif case == 'error': return -25204
                    elif case == 'wrong-type': C.cast(out, C.POINTER(C.c_void_p))[0] = 3
                    elif case == 'wrong-size': b.arrays[C.cast(out, C.POINTER(C.c_void_p))[0]].clear()
                    return rc
                b.a.AXUIElementCopyAttributeValues.call = returned
                with self.assertRaises(Refusal): s.refs(2, 'AXChildren')
                self.assertIsNone(s.touch_ordinal(3))
                self.assertIsNone(s.rows[1]['last_return'])
                self.assertNotIn('AXChildren', s.rows[1]['array_observations'])
                self.assertFalse(any(e == ('owner', 3) for e in b.log))

    def test_owner_receipt_failure_retains_local_provenance_without_more_calls(self):
        s, io, b, now = context()
        b.nodes[4]['owner'] = 999
        def receipt(kind, event):
            if event.get('owner_match') is False: raise OSError('SECRET')
        io.record = receipt
        with self.assertRaises(Refusal): s.ref(1, 'AXFocusedUIElement')
        row = s.rows[s.touch_ordinal(4)]
        self.assertEqual(row['owner_pid'], 999)
        self.assertEqual(row['last_return']['attribute'], 'AXFocusedUIElement')
        before = list(b.log)
        with self.assertRaises(Refusal): s.role(4)
        self.assertEqual(b.log, before)
        self.assertEqual(s.completed_proofs, [])
        self.assertNotIn('SECRET', repr(s.binding_refusal(s.stopped)))


class ExactReturnedAliasAndSnapshotTests(unittest.TestCase):
    def alias(self, backend, actual, canonical, owner=17):
        backend.nodes[actual] = dict(backend.nodes[canonical], owner=owner)
        backend.equal = lambda left, right: (canonical if left == actual else left) == (canonical if right == actual else right)

    def test_app_window_main_alias_cannot_inherit_retained_main_owner(self):
        s, io, b, now = context()
        self.alias(b, 22, 2, 999); b.nodes[1]['AXWindows'] = [22]
        with self.assertRaisesRegex(Refusal, 'foreign/unknown owner'): s.publication()
        self.assertIn(('timeout-exact', 22, .2), b.log); self.assertEqual(b.log[-1], ('owner', 22))
        self.assertNotIn('AXWindows', s.rows[0]['array_observations'])
        self.assertEqual(s.rows[1]['owner_pid'], 999)
        self.assertEqual(s.rows[1]['last_return']['attribute'], 'AXWindows')

    def test_terminal_picker_parent_alias_cannot_inherit_main_owner(self):
        s, io, b, now = context()
        self.alias(b, 22, 2, 999); b.nodes[3]['AXParent'] = 22
        with self.assertRaisesRegex(Refusal, 'foreign/unknown owner'): s.publication()
        self.assertEqual(b.log[-1], ('owner', 22))
        self.assertIsNone(s.rows[s.touch_ordinal(3)]['parent_ordinal'])
        self.assertEqual(s.rows[1]['last_return']['attribute'], 'AXParent')

    def test_cross_source_deduplicated_alias_still_gets_its_own_admission(self):
        s, io, b, now = context()
        self.alias(b, 23, 3, 999)
        b.nodes[1]['AXWindows'] = [2, 3]; b.nodes[2]['AXChildren'] = [23]
        with self.assertRaisesRegex(Refusal, 'foreign/unknown owner'): s.publication()
        self.assertEqual(b.log[-1], ('owner', 23))
        self.assertNotIn('AXChildren', s.rows[1]['array_observations'])
        self.assertEqual(s.rows[s.touch_ordinal(3)]['owner_pid'], 999)
        self.assertFalse(any(e[:2] == ('attribute', 23) for e in b.log))

    def test_valid_main_alias_is_admitted_even_when_publication_skips_its_role(self):
        s, io, b, now = context()
        self.alias(b, 22, 2); b.nodes[1]['AXWindows'] = [22]
        picker, proof = s.publication()
        self.assertEqual(picker, 3)
        self.assertIn(('timeout-exact', 22, .2), b.log); self.assertIn(('owner', 22), b.log)
        self.assertFalse(any(e[:2] == ('attribute', 22) for e in b.log))
        self.assertEqual(proof['app_windows']['members'], [s.touch_ordinal(2)])

    def test_returned_alias_owner_capacity_and_lateness_prevent_edge_acceptance(self):
        for case in ('owner-cap', 'trace-cap', 'late-owner'):
            with self.subTest(case=case):
                s, io, b, now = context(initial=True)
                s.mode = s.phase = 'initial'; s.end = 6; s.begin()
                self.alias(b, 22, 2); b.nodes[1]['AXWindows'] = [22]
                ranged = b.a.AXUIElementCopyAttributeValues.call
                def output(*args):
                    rc = ranged(*args)
                    if case == 'owner-cap': s.initial_owners = 128
                    if case == 'trace-cap': s.op_count = 512
                    return rc
                b.a.AXUIElementCopyAttributeValues.call = output
                if case == 'late-owner':
                    owner = b.owner
                    def late(ref):
                        value = owner(ref)
                        if ref == 22: now[0] = 6.01
                        return value
                    b.owner = late
                with self.assertRaises(Refusal): s.refs(1, 'AXWindows', optional=False)
                self.assertNotIn('AXWindows', s.rows[0]['array_observations'])
                self.assertEqual(s.completed_proofs, [])
                if case != 'late-owner': self.assertNotIn(('owner', 22), b.log)
                else: self.assertTrue(s.trace[-1]['late'])

    def test_retained_picker_extra_modal_or_unknown_child_makes_snapshot_partial(self):
        for role in ('AXSheet', 'AXWindow', 'AXDrawer', 'AXDialog', 'SECRET unknown'):
            with self.subTest(role=role):
                s, io, b, now = context(); picker = s.picker(); api = Posting()
                d.FixedGesture(api).run(s, picker, lambda *args: None)
                b.nodes[9] = {'role': role, 'AXParent': picker}
                b.nodes[picker]['AXChildren'].append(9)
                result = s.snapshot(picker, True)
                self.assertFalse(result['complete']); self.assertFalse(result['selection_complete'])
                self.assertIsNone(result['root_ordinal'])
                self.assertEqual(result['candidate_root_ordinal'], s.touch_ordinal(picker))
                self.assertEqual(result['semantic_handling'], 'unknown'); self.assertEqual(len(api.posts), 2)
                self.assertFalse(any(e[:3] == ('attribute', 9, 'AXParent') for e in b.log))
                self.assertNotIn('SECRET', repr(result))

    def test_related_sheet_extra_modal_or_unknown_child_makes_snapshot_partial(self):
        for role in ('AXSheet', 'AXWindow', 'AXDrawer', 'AXDialog', 'SECRET unknown'):
            with self.subTest(role=role):
                s, io, b, now = context(); picker = s.picker(); api = Posting()
                d.FixedGesture(api).run(s, picker, lambda *args: None)
                related_after(b)
                b.nodes[11] = {'role': role, 'AXParent': 9}; b.nodes[9]['AXChildren'].append(11)
                result = s.snapshot(picker, True)
                self.assertFalse(result['complete']); self.assertFalse(result['selection_complete'])
                self.assertIsNone(result['root_ordinal'])
                self.assertEqual(result['candidate_root_ordinal'], s.touch_ordinal(9))
                self.assertEqual(result['semantic_handling'], 'unknown'); self.assertEqual(len(api.posts), 2)
                self.assertFalse(any(e[:3] == ('attribute', 11, 'AXParent') for e in b.log))
                self.assertNotIn('SECRET', repr(result))

    def test_initial_only_counters_and_sealed_strict_snapshot_deadline_keep_their_scope(self):
        s, io, b, now = context(initial=True)
        picker = s.initial_picker()
        initial = (s.initial_reads, s.initial_owners)
        strict_end, initial_ops = s.end, s.op_count
        api = Posting(); d.FixedGesture(api).run(s, picker, lambda *args: None)
        self.assertEqual((s.initial_reads, s.initial_owners), initial)
        self.assertEqual(s.end, strict_end); self.assertGreater(s.op_count, initial_ops)
        before_snapshot = s.op_count
        result = s.snapshot(picker, True)
        self.assertTrue(result['complete'])
        self.assertEqual((s.initial_reads, s.initial_owners), initial)
        self.assertEqual(s.end, min(strict_end, now[0] + 1))
        self.assertGreater(s.op_count, before_snapshot)
        self.assertEqual([event['op'] for event in s.trace], list(range(1, s.op_count + 1)))
        self.assertLessEqual(s.op_count, 512); self.assertEqual(len(api.posts), 2)


class PositiveTargetTests(unittest.TestCase):
    def gesture(self,s,b,record=lambda *a:None):
        api=Posting();g=d.FixedGesture(api);picker=s.initial_picker() if not s.initial_binding_used and s.experiment_end==8 else s.picker()
        g.run(s,picker,record)
        return picker,api,g

    def test_observed_geometry_proofs_post_but_snapshot_honestly_reaches_shared_cap(self):
        s,io,b,now=context(initial=True);observed_shape(b)
        old=b.a.AXUIElementCopyAttributeValue.call;failed=[0]
        def read(ref,name,out):
            if (ref,name)==(2,'AXRole') and failed[0]<2:failed[0]+=1;return -25204
            return old(ref,name,out)
        b.a.AXUIElementCopyAttributeValue.call=read
        picker,api,g=self.gesture(s,b)
        result=s.snapshot(picker,True)
        self.assertFalse(result['complete']); self.assertEqual(result['error_category'],'diagnostic trace capacity')
        self.assertFalse(result['selection_complete']); self.assertIsNone(result['root_ordinal'])
        self.assertEqual(s.initial_completed_pass,3);self.assertEqual(len(api.posts),2)
        self.assertLessEqual(s.initial_reads,64);self.assertLessEqual(s.initial_owners,128)
        self.assertLessEqual(s.op_count,512);self.assertLessEqual(len(s.rows),32)
        proof=s.after_intent_proof
        self.assertEqual(proof['publication']['app_windows']['members'],[s.touch_ordinal(2)])
        self.assertEqual(proof['publication']['main_children']['members'],[s.touch_ordinal(x) for x in (10,11,12,13,14,3)])
        self.assertEqual(proof['legacy_nested']['state'],'unknown');self.assertIsNone(proof['legacy_nested']['count'])
        self.assertEqual([e['source'] for e in proof['ancestry_edges']],[s.touch_ordinal(x) for x in (4,20,21,22)])
        self.assertEqual(proof['nearest_modal_proof']['nearest_modal'],s.touch_ordinal(3))
        self.assertFalse(any(x[0] in ('count','range') and x[1] in (4,20) for x in b.log))
        self.assertEqual(result['label'],'partial-observed-after-attempt')
        self.assertEqual(s.op_count,512); self.assertEqual(len(s.completed_proofs),3)

    def test_primary_ancestry_never_queries_any_shortcut_regardless_of_provider_values(self):
        for advertised in (None,3,2,{'private':'SECRET'}):
            s,io,b,now=context(initial=True);observed_shape(b)
            b.nodes[4]['AXTopLevelUIElement']=advertised
            p,api,g=self.gesture(s,b);result=s.snapshot(p,True)
            self.assertFalse(result['complete']);self.assertEqual(result['error_category'],'diagnostic trace capacity')
            self.assertEqual(len(api.posts),2);self.assertEqual(len(s.completed_proofs),3)
            self.assertEqual(s.PROOF_MODE,'POSITIVE_FOCUSED_ANCESTRY_DIAGNOSTIC_V1')
            proof=s.after_intent_proof['nearest_modal_proof']
            self.assertEqual(proof['path_ordinals'],[s.touch_ordinal(x) for x in (4,20,21,22,3)])
            self.assertEqual(proof['nearest_modal'],s.touch_ordinal(3))
            self.assertEqual(proof['nearest_modal_role'],'AXSheet')
            self.assertEqual([x['role'] for x in proof['role_observations']],
                             ['AXOutline','AXScrollArea','AXSplitGroup','AXSplitGroup','AXSheet'])
            self.assertFalse(any(x[0]=='attribute' and x[2] in ('AXTopLevelUIElement','AXWindow','AXFocusedWindow') for x in b.log))
            self.assertNotIn('top_level',repr(result));self.assertNotIn('SECRET',repr(result))

    def test_first_intervening_modal_vetoes_before_following_it_even_legacy_zero(self):
        for role in ('AXWindow','AXSheet','AXDrawer','AXDialog'):
            s,io,b,now=context();p=s.picker();api=Posting()
            b.nodes[9]={'role':role,'AXParent':5};b.nodes[4]['AXParent']=9
            with self.assertRaises(Refusal):d.FixedGesture(api).run(s,p,lambda *a:None)
            self.assertEqual(api.posts,[])
            self.assertFalse(any(x[:3]==('attribute',9,'AXParent') for x in b.log))
            self.assertFalse(any(x[:3]==('count',3,'AXChildren') for x in b.log))

    def test_required_parent_role_and_focus_copies_fail_closed_even_legacy_zero(self):
        for attribute,ref in (('AXParent',4),('AXRole',4),('AXFocusedUIElement',1)):
            for case in ('unsupported','no_value','null','array','dictionary','foreign','missing_ref','nonnull_failed'):
                with self.subTest(attribute=attribute,case=case):
                    s,io,b,now=context();p=s.picker();api=Posting()
                    old=b.a.AXUIElementCopyAttributeValue.call
                    b.nodes[9]={'role':'AXButton','AXParent':3,'owner':999}
                    def read(target,name,out):
                        if (target,name)!=(ref,attribute):return old(target,name,out)
                        if case in ('unsupported','no_value','null'):
                            return {'unsupported':-25205,'no_value':-25212,'null':0}[case]
                        pointer=99 if case=='missing_ref' else 9
                        if case=='array':pointer=9000;b.arrays[pointer]=[3]
                        if case=='dictionary':pointer=9000;b.scalars[pointer]=('CFDictionary','SECRET')
                        C.cast(out,C.POINTER(C.c_void_p))[0]=pointer
                        return -25212 if case=='nonnull_failed' else 0
                    b.a.AXUIElementCopyAttributeValue.call=read
                    with self.assertRaises(Refusal):d.FixedGesture(api).run(s,p,lambda *a:None)
                    self.assertEqual(api.posts,[])
                    self.assertFalse(any(x[0]=='decode-array' and x[1]==9000 for x in b.log))
                    self.assertFalse(any(x[0]=='attribute' and x[1]==9 for x in b.log))
                    self.assertNotIn('SECRET',repr(s.binding_refusal('fixed refusal')))

    def test_required_parent_initial_cannot_complete_can_retry_but_strict_never_does(self):
        s,io,b,now=context(initial=True);small_positive(b)
        old=b.a.AXUIElementCopyAttributeValue.call;failed=[0]
        def read(ref,name,out):
            if (ref,name)==(4,'AXParent') and failed[0]==0:failed[0]+=1;return -25204
            return old(ref,name,out)
        b.a.AXUIElementCopyAttributeValue.call=read
        p=s.initial_picker();self.assertEqual(s.initial_completed_pass,2);self.assertAlmostEqual(now[0],.1)
        attempts=[]
        def strict(ref,name,out):
            if (ref,name)==(4,'AXParent'):attempts.append(name);return -25204
            return old(ref,name,out)
        b.a.AXUIElementCopyAttributeValue.call=strict;api=Posting()
        with self.assertRaises(Refusal):d.FixedGesture(api).run(s,p,lambda *a:None)
        self.assertEqual(attempts,['AXParent']);self.assertEqual(api.posts,[])

    def test_focused_self_unknown_modal_or_changed_across_intent_never_posts(self):
        for case in ('app','main','picker','unknown','drawer','another_control'):
            s,io,b,now=context();p=s.picker();api=Posting()
            def receipt(*a):
                if case in ('app','main','picker'):b.nodes[1]['AXFocusedUIElement']={'app':1,'main':2,'picker':3}[case]
                elif case=='another_control':
                    b.nodes[9]={'role':'AXButton','AXParent':5}
                    b.nodes[5]['AXChildren'].append(9);b.nodes[1]['AXFocusedUIElement']=9
                else:b.nodes[4]['role']='SECRET unknown' if case=='unknown' else 'AXDrawer'
            with self.assertRaises(Refusal):d.FixedGesture(api).run(s,p,receipt)
            self.assertEqual(api.posts,[],case)

    def test_same_picker_cannot_be_replaced_reparented_or_foreign_across_intent(self):
        for case in ('replacement','reparent','foreign'):
            s,io,b,now=context();p=s.picker();api=Posting()
            def intent(*a):
                if case=='replacement':
                    b.nodes[9]={'role':'AXSheet','AXParent':2,'AXChildren':[],'AXSheets':[]}
                    b.nodes[2]['AXChildren']=[9]
                    b.nodes[5]['AXParent']=9
                elif case=='reparent':b.nodes[3]['AXParent']=1
                else:b.nodes[3]['owner']=999
            with self.assertRaises(Refusal):d.FixedGesture(api).run(s,p,intent)
            self.assertEqual(api.posts,[],case);self.assertEqual(s.picker_anchor,3)
            self.assertEqual(api.freed,[103,102,101])

    def test_fresh_ancestry_after_catalog_work_and_full_final_identity(self):
        for point in ('legacy','final_identity'):
            s,io,b,now=context();p=s.picker();api=Posting()
            if point=='legacy':
                old=b.a.AXUIElementGetAttributeValueCount.call
                def count(ref,name,out):
                    if (ref,name)==(3,'AXSheets'):b.nodes[4]['AXParent']=2
                    return old(ref,name,out)
                b.a.AXUIElementGetAttributeValueCount.call=count
            else:
                old=io.check;calls=[0]
                def check(identity):
                    old(identity);calls[0]+=1
                    if calls[0]==2:b.nodes[4]['AXParent']=2
                io.check=check
            with self.assertRaises(Refusal):d.FixedGesture(api).run(s,p,lambda *a:None)
            self.assertEqual(api.posts,[])

    def test_active_preexisting_nested_sheet_with_both_legacy_unknown_vetoes(self):
        s,io,b,now=context();p=s.picker();api=Posting();related_after(b)
        b.nodes[2].pop('AXSheets');b.nodes[3].pop('AXSheets')
        self.assertEqual(b.nodes[1]['AXWindows'],[2])
        with self.assertRaises(Refusal):d.FixedGesture(api).run(s,p,lambda *a:None)
        self.assertEqual(api.posts,[])

    def test_known_nonempty_veto_and_expected_main_legacy_does_not_authorize(self):
        for nested in (False,True):
            s,io,b,now=context();p=s.picker();api=Posting()
            if nested:b.nodes[3]['AXSheets']=[99]
            if nested:
                with self.assertRaises(Refusal):d.FixedGesture(api).run(s,p,lambda *a:None)
                self.assertEqual(api.posts,[])
            else:
                d.FixedGesture(api).run(s,p,lambda *a:None)
                self.assertEqual(len(api.posts),2)
            self.assertFalse(any(x[0] in ('count','range') and x[1:3]==(2,'AXSheets') for x in b.log))

    def test_malformed_publication_ambiguous_modal_and_unknown_private_boundaries(self):
        for case in ('duplicate_main','duplicate_picker','alias_duplicate','second_sheet','drawer','dialog','window','foreign','bad_parent','unpublished_main','unpublished_picker','self_child','app_child','unknown','private_unknown_group'):
            s,io,b,now=context(initial=True);api=Posting()
            if case=='duplicate_main':b.nodes[1]['AXWindows']=[2,2]
            if case=='duplicate_picker':b.nodes[2]['AXChildren']=[3,3]
            if case=='alias_duplicate':
                b.nodes[23]=dict(b.nodes[3]);b.equal=lambda a,c:(3 if a==23 else a)==(3 if c==23 else c)
                b.nodes[2]['AXChildren']=[3,23]
            if case in ('second_sheet','drawer','dialog','window'):
                b.nodes[9]={'role':{'second_sheet':'AXSheet','drawer':'AXDrawer','dialog':'AXDialog','window':'AXWindow'}[case],'AXParent':2}
                b.nodes[2]['AXChildren'].append(9)
            if case=='foreign':b.nodes[3]['owner']=999
            if case=='bad_parent':b.nodes[3]['AXParent']=1
            if case=='unpublished_main':b.nodes[1]['AXWindows']=[]
            if case=='unpublished_picker':b.nodes[2]['AXChildren']=[]
            if case=='self_child':b.nodes[2]['AXChildren']=[2,3]
            if case=='app_child':b.nodes[2]['AXChildren']=[1,3]
            if case=='unknown':b.nodes[6]['role']='SECRET unknown'
            if case=='private_unknown_group':b.nodes[7]['role']='SECRET unknown'
            with self.assertRaises(Refusal):
                p=s.initial_picker();d.FixedGesture(api).run(s,p,lambda *a:None)
            self.assertEqual(api.posts,[],case);self.assertEqual(now[0],0)
            self.assertFalse(any(x[:3] in (('count',6,'AXChildren'),('count',7,'AXChildren')) for x in b.log))

    def test_known_candidate_before_partial_failure_is_never_forgotten(self):
        s,io,b,now=context(initial=True)
        old=b.a.AXUIElementCopyAttributeValue.call;failed=[False]
        def read(ref,name,out):
            if (ref,name)==(3,'AXParent') and not failed[0]:failed[0]=True;return -25204
            return old(ref,name,out)
        b.a.AXUIElementCopyAttributeValue.call=read
        def sleep(n):
            now[0]+=n;b.nodes[9]={'role':'AXSheet','AXParent':2,'AXChildren':[]}
            b.nodes[2]['AXChildren']=[9]
        io.sleep=sleep
        with self.assertRaises(Refusal):s.initial_picker()
        self.assertEqual(s.pre_modal_refs,[3,9]);self.assertEqual(s.initial_completed_pass,None)
        self.assertAlmostEqual(now[0],.1)

    def test_proof_edges_are_actual_ops_and_intent_receipt_is_fully_detached(self):
        s,io,b,now=context();api=Posting();p=s.picker();seen=[]
        def mutate(kind,value):
            seen.append(deepcopy(value))
            value['original']['pid']=999;value['positive_target_proof']['publication']['main_children']['members'].clear()
            value['positive_target_proof']['nearest_modal_proof']['nearest_modal']=999
            value['proof_mode']='fabricated';value['focused_ancestry_ordinals'].clear()
        d.FixedGesture(api).run(s,p,mutate)
        self.assertEqual(len(api.posts),2);self.assertEqual(s.original,ORIGINAL)
        proof=s.completed_proofs[0];trace={e['op']:e for e in s.trace}
        self.assertEqual(proof['publication']['main_children']['members'],[s.touch_ordinal(3)])
        for edge in (*proof['ancestry_edges'],proof['picker_parent_edge']):
            self.assertEqual(trace[edge['op']]['ordinal'],edge['source'])
            self.assertEqual(trace[edge['op']]['return_code'],0)
        self.assertEqual(seen[0]['proof_mode'],d.Structure.PROOF_MODE)
        self.assertNotIn('pre_command_empty_sheet_relation',seen[0])
        self.assertNotIn('raw_refs',s.after_intent_proof)

    def test_initial_parent_late_success_failure_or_owner_drift_stops_no_retry(self):
        for case in ('success','failure','owner','birth'):
            s,io,b,now=context(initial=True);small_positive(b)
            old=b.a.AXUIElementCopyAttributeValue.call;attempts=[]
            def read(ref,name,out):
                if (ref,name)==(4,'AXParent'):
                    attempts.append(name)
                    if case in ('success','failure'):now[0]=6.01
                    elif case=='owner':b.nodes[3]['owner']=999
                    else:io.identity['start_usec']+=1
                    return -25204 if case=='failure' else old(ref,name,out)
                return old(ref,name,out)
            b.a.AXUIElementCopyAttributeValue.call=read
            with self.assertRaises(Refusal):s.initial_picker()
            self.assertEqual(len(attempts),2 if case=='birth' else 1)
            self.assertEqual({t['pass'] for t in s.trace if t['api']=='AXUIElementCopyAttributeValue'},{1})
            self.assertEqual(s.mode,'strict');self.assertEqual(now[0],0 if case in ('owner','birth') else 6.01)

    def test_full_identity_after_final_parent_read_and_no_input_after_late_intent(self):
        for case in ('birth','late_intent','trace_capacity'):
            s,io,b,now=context();p=s.picker();api=Posting();parents=[0]
            old=b.a.AXUIElementCopyAttributeValue.call
            def read(ref,name,out):
                if (ref,name)==(4,'AXParent'):
                    parents[0]+=1
                    if case=='birth' and parents[0]==4:io.identity['start_usec']+=1
                return old(ref,name,out)
            b.a.AXUIElementCopyAttributeValue.call=read
            def intent(*a):
                if case=='late_intent':now[0]=2.01
                if case=='trace_capacity':s.op_count=512
            with self.assertRaises(Refusal):d.FixedGesture(api).run(s,p,intent)
            self.assertEqual(api.posts,[],case);self.assertEqual(api.freed,[103,102,101])

    def test_all_receipt_edges_and_memberships_use_real_pass_op_ids(self):
        s,io,b,now=context(initial=True);observed_shape(b)
        p,api,g=self.gesture(s,b)
        proofs=deepcopy(s.completed_proofs);trace={e['op']:e for e in s.trace}
        for proof in proofs:
            for publication in (proof['publication']['app_windows'],proof['publication']['main_children'],
                                *(a['publication'] for a in proof['veto_boundary']['arrays'])):
                self.assertEqual(trace[publication['count_op']]['api'],'AXUIElementGetAttributeValueCount')
                self.assertEqual(trace[publication['count_op']]['pass'],publication['pass'])
                if publication['range_op'] is not None:
                    self.assertEqual(trace[publication['range_op']]['requested_count'],len(publication['members']))
            for edge in (*proof['publication']['parent_edges'],*proof['veto_boundary']['parent_edges'],
                         *proof['ancestry_edges'],proof['focused_edge'],proof['picker_parent_edge']):
                event=trace[edge['op']]
                self.assertEqual(event['ordinal'],edge['source']);self.assertEqual(event['return_code'],0)
                self.assertFalse(event['late']);self.assertEqual(event['pass'],edge['pass'])
            nearest=proof['nearest_modal_proof']
            self.assertEqual(len(nearest['parent_edges']),len(nearest['path_ordinals'])-1)
            for role in nearest['role_observations']:
                event=trace[role['op']]
                self.assertEqual(event['attribute'],'AXRole');self.assertEqual(event['ordinal'],role['ordinal'])
                self.assertEqual(event['return_code'],0);self.assertEqual(event['pass'],role['pass'])
        proofs[0]['veto_boundary']['arrays'].clear()
        self.assertTrue(s.completed_proofs[0]['veto_boundary']['arrays'])

    def test_post_inline_is_retained_picker_and_unknown_effect_even_external_misrouting(self):
        s,io,b,now=context();p=s.picker();api=Posting();ground_truth=[]
        api.on_down=lambda:ground_truth.append({'event':102,'receiver':'outside-retained-picker'})
        d.FixedGesture(api).run(s,p,lambda *a:None)
        result=s.snapshot(p,True)
        self.assertTrue(result['complete']);self.assertEqual(result['root_ordinal'],s.touch_ordinal(p))
        self.assertEqual(result['label'],'retained-picker-observed-after-attempt')
        self.assertEqual(result['semantic_handling'],'unknown');self.assertFalse(result['readiness'])
        # This external invented ground truth falsifies routing fidelity; AX does not detect it.
        self.assertEqual(ground_truth,[{'event':102,'receiver':'outside-retained-picker'}])
        self.assertNotIn('misrouting',repr(result));self.assertEqual(len(api.posts),2)

    def test_post_related_selection_rejects_sibling_private_multiple_missing_or_wrong_parent(self):
        for case in ('sibling','missing_reciprocal','foreign','window','drawer','private','multiple','missing_parent','unsupported_parent','cycle','too_deep'):
            s,io,b,now=context();p,api,g=self.gesture(s,b);related_after(b)
            if case=='sibling':b.nodes[9]['AXParent']=2;b.nodes[3]['AXChildren']=[5]
            if case=='missing_reciprocal':b.nodes[3]['AXChildren']=[5]
            if case=='foreign':b.nodes[9]['owner']=999
            if case in ('window','drawer'):b.nodes[9]['role']='AXWindow' if case=='window' else 'AXDrawer'
            if case in ('private','cycle','too_deep'):
                b.nodes[11]={'role':'AXScrollArea' if case=='private' else 'AXGroup','AXParent':11 if case=='cycle' else 3,'AXChildren':[9]}
                b.nodes[9]['AXParent']=11;b.nodes[3]['AXChildren']=[5,11]
                if case=='too_deep':
                    for n in (12,13):b.nodes[n]={'role':'AXGroup','AXParent':n+1 if n==12 else 3,'AXChildren':[11 if n==12 else 12]}
                    b.nodes[11]['AXParent']=12;b.nodes[3]['AXChildren']=[5,13]
            if case=='multiple':
                b.nodes[11]={'role':'AXSheet','AXParent':3,'AXChildren':[]};b.nodes[3]['AXChildren'].append(11)
            if case in ('missing_parent','unsupported_parent'):
                b.nodes[10].pop('AXParent')
                if case=='unsupported_parent':
                    old=b.a.AXUIElementCopyAttributeValue.call
                    b.a.AXUIElementCopyAttributeValue.call=lambda ref,name,out:-25205 if (ref,name)==(10,'AXParent') else old(ref,name,out)
            result=s.snapshot(p,True)
            self.assertFalse(result['complete'],case);self.assertIsNone(result['root_ordinal'],case)
            self.assertEqual(result['semantic_handling'],'unknown');self.assertEqual(len(api.posts),2)
            if case=='private':self.assertFalse(any(x[:3]==('count',11,'AXChildren') for x in b.log))

    def test_post_selected_root_later_role_or_parent_drift_stays_partial(self):
        for field,value in (('role','AXWindow'),('AXParent',2)):
            s,io,b,now=context();p,api,g=self.gesture(s,b);related_after(b)
            old=b.a.AXUIElementGetAttributeValueCount.call
            def count(ref,name,out):
                if (ref,name)==(1,'AXWindows'):b.nodes[9][field]=value
                return old(ref,name,out)
            b.a.AXUIElementGetAttributeValueCount.call=count
            result=s.snapshot(p,True)
            self.assertFalse(result['complete']);self.assertEqual(result['semantic_handling'],'unknown')
            self.assertEqual(len(api.posts),2)

    def test_post_changed_focus_within_retained_picker_is_not_misrouting_claim(self):
        s,io,b,now=context();p,api,g=self.gesture(s,b)
        b.nodes[9]={'role':'AXButton','AXParent':5}
        b.nodes[5]['AXChildren'].append(9);b.nodes[1]['AXFocusedUIElement']=9
        result=s.snapshot(p,True)
        self.assertTrue(result['complete']);self.assertEqual(result['semantic_handling'],'unknown')
        self.assertNotIn('misrouting',repr(result))

    def test_ancestry_alias_uses_exact_ref_timeout_and_safe_ordinals(self):
        s,io,b,now=context();p=s.picker();api=Posting()
        b.nodes[23]=dict(b.nodes[3]);b.nodes[5]['AXParent']=23
        b.equal=lambda a,c:(3 if a==23 else a)==(3 if c==23 else c)
        d.FixedGesture(api).run(s,p,lambda *a:None)
        self.assertEqual(len(api.posts),2);self.assertEqual(s.touch_ordinal(23),s.touch_ordinal(3))
        self.assertIn(('timeout-exact',23,.2),b.log);self.assertIn(('owner',23),b.log)
        self.assertIn(('attribute',23,'AXRole'),b.log)

    def test_cross_source_cfequal_publication_deduplicates_without_timeout_inheritance(self):
        s,io,b,now=context();b.nodes[23]=dict(b.nodes[3])
        b.equal=lambda a,c:(3 if a==23 else a)==(3 if c==23 else c)
        b.nodes[1]['AXWindows']=[2,23]
        p,api,g=self.gesture(s,b)
        self.assertEqual(len(api.posts),2)
        proof=s.after_intent_proof;ordinal=s.touch_ordinal(3)
        self.assertEqual(proof['publication']['app_windows']['members'],[s.touch_ordinal(2),ordinal])
        self.assertEqual(proof['publication']['main_children']['members'],[ordinal])
        self.assertIn(('timeout-exact',23,.2),b.log)

    def test_failed_nonnull_required_parent_and_focus_never_become_absence(self):
        for attr in ('AXParent','AXFocusedUIElement'):
            s,io,b,now=context(initial=True);old=b.a.AXUIElementCopyAttributeValue.call
            def read(ref,name,out):
                if name==attr:C.cast(out,C.POINTER(C.c_void_p))[0]=3;return -25212
                return old(ref,name,out)
            b.a.AXUIElementCopyAttributeValue.call=read
            with self.assertRaises(Refusal):s.initial_picker()
            self.assertEqual(now[0],0);self.assertEqual(s.mode,'strict')



class StructuralTests(unittest.TestCase):
    def test_optional_relationship_absence_keeps_unknown_count_and_no_range(self):
        for code in (-25205, -25212):
            for name in ('AXSheets', 'AXChildren'):
                with self.subTest(code=code, name=name):
                    s, io, b, now = context()
                    original = b.a.AXUIElementGetAttributeValueCount.call
                    def absent(ref, attr, out):
                        return code if (ref, attr) == (2, name) else original(ref, attr, out)
                    b.a.AXUIElementGetAttributeValueCount.call = absent
                    self.assertEqual(s.refs(2, name, optional=True), [])
                    fact = s.rows[1]['reads'][-1]
                    self.assertEqual(fact['return_code'], code)
                    self.assertIsNone(fact['count'])
                    self.assertFalse(any(row[:3] == ('range', 2, name) for row in b.log))
                    self.assertIsNone(s.stopped)

    def test_optional_scalar_absence_does_not_remove_mandatory_role_or_parent(self):
        for code in (-25205, -25212):
            s, io, b, now = context()
            original = b.a.AXUIElementCopyAttributeValue.call
            def absent(ref, name, out):
                return code if (ref, name) == (3, 'AXParent') else original(ref, name, out)
            b.a.AXUIElementCopyAttributeValue.call = absent
            self.assertIsNone(s.ref(3, 'AXParent'))
            s, io, b, now = context()
            b.a.AXUIElementCopyAttributeValue.call = lambda *args: code
            with self.assertRaises(Refusal):
                s.role(2)
            s, io, b, now = context(); picker = s.picker(); api = Posting()
            original_value = b.a.AXUIElementCopyAttributeValue.call
            def no_parent(ref, name, out):
                return code if (ref,name) == (4,'AXParent') else original_value(ref, name, out)
            b.a.AXUIElementCopyAttributeValue.call = no_parent
            with self.assertRaises(Refusal):
                d.FixedGesture(api).run(s, picker, lambda *args: None)
            self.assertEqual(api.posts, [])

    def test_real_bind_route_snapshot_privacy_and_range_order(self):
        structure, io, b, now = context()
        picker = structure.picker()
        route = structure.routing(picker)
        self.assertEqual(route['path'], [4, 5, 3])
        self.assertEqual([e['source'] for e in route['edges']], [structure.touch_ordinal(x) for x in (4,5)])
        b.nodes[6]['role'] = 'SECRET unknown role'
        result = structure.snapshot(picker, False)
        self.assertFalse(result['complete']); self.assertFalse(result['selection_complete'])
        self.assertEqual(result['error_category'], 'diagnostic snapshot child role unknown')
        self.assertIsNone(result['root_ordinal'])
        self.assertEqual(result['candidate_root_ordinal'], structure.touch_ordinal(picker))
        self.assertEqual(result['label'], 'partial-without-attempt')
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

    def test_fatal_routing_refusal_retains_facts_without_recovery_snapshot(self):
        s, io, b, now = context(); picker = s.picker()
        b.nodes[1].pop('AXFocusedUIElement')
        with self.assertRaises(Refusal): s.routing(picker)
        before=list(b.log)
        self.assertFalse(s.snapshot(picker, False)['complete'])
        self.assertEqual(b.log,before)

    def test_related_sheet_requires_actual_post_ancestry_and_reciprocal_path(self):
        s, io, b, now = context(); picker = s.picker()
        d.FixedGesture(Posting()).run(s, picker, lambda *args: None)
        b.nodes[9] = {'role': 'AXSheet', 'AXParent': 3, 'AXChildren': [10]}
        b.nodes[10] = {'role': 'AXTextField', 'AXParent': 9}
        b.nodes[3]['AXChildren'] = [5,9]
        b.nodes[1]['AXFocusedUIElement'] = 10
        b.nodes[3].pop('AXSheets'); b.nodes[2].pop('AXSheets')
        result = s.snapshot(picker, True)
        self.assertTrue(result['complete'], result['error_category'])
        self.assertEqual(result['label'], 'related-sheet-observed-after-attempt')
        self.assertEqual(result['relation']['path']['arrays'][0]['publication']['members'],
                         [s.touch_ordinal(5),s.touch_ordinal(9)])
        self.assertEqual(result['semantic_handling'], 'unknown')
        self.assertNotIn('newly',repr(result))

    def test_after_post_snapshot_without_baseline_does_not_claim_newness(self):
        s, io, b, now = context(); picker = s.picker()
        b.nodes[9] = {'role': 'AXSheet', 'AXParent': 3, 'AXChildren': []}
        b.nodes[3]['AXSheets'] = [9]
        result = s.snapshot(picker, True)
        self.assertFalse(result['complete'])
        self.assertNotIn('newly-exposed', result['label'])

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
        io.structural_calls = d.StructuralCalls(b,io.clock); s.calls = io.structural_calls
        result = s.snapshot(picker, False)
        self.assertFalse(result['complete'])
        self.assertNotIn('SECRET', repr(result))
        s, io, b, now = context(); picker = s.picker(); b.nodes[7]['owner'] = 999
        result = s.snapshot(picker, False)
        self.assertFalse(result['complete'])
        self.assertFalse(any(row[0] in ('count','range','attribute') and row[1] == 7 for row in b.log))

    def test_new_sheet_ambiguity_and_parent_cycle_remain_partial(self):
        s, io, b, now = context(); picker = s.picker()
        s.recheck(picker)
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
        s.calls = d.StructuralCalls(b,io.clock)
        with self.assertRaises(Refusal): s.role(3)
        self.assertFalse(any(row[0] == 'decode-array' for row in b.log))


class CommunicationPolicyTests(unittest.TestCase):
    def fails(self, backend, count, ref=2, attribute='AXRole', code=-25204, kind='null', hook=None):
        original=backend.a.AXUIElementCopyAttributeValue.call; attempts=[]
        def read(target,name,out):
            if target==ref and name==attribute and len(attempts)<count:
                attempts.append((target,name));backend.log.append(('failed-read',target,name,code))
                if kind!='null':
                    backend.scalars[9000]=(kind,'SECRET output never decoded')
                    C.cast(out,C.POINTER(C.c_void_p))[0]=9000
                if hook:hook()
                return code
            return original(target,name,out)
        backend.a.AXUIElementCopyAttributeValue=Fn(read)
        return attempts

    def install(self,s,io,b):
        io.structural_calls=d.StructuralCalls(b,io.clock);s.calls=io.structural_calls

    def test_recorded_prefix_completes_fourth_pass_not_an_attribute_patch(self):
        s,io,b,now=context(initial=True);original=b.a.AXUIElementCopyAttributeValue.call
        failures=[0];count_failed=[False];sleeps=[]
        def role(ref,name,out):
            if ref==2 and name=='AXRole' and failures[0]<2:
                failures[0]+=1;return -25204
            return original(ref,name,out)
        old_count=b.a.AXUIElementGetAttributeValueCount.call
        def count(ref,name,out):
            if ref==1 and name=='AXWindows' and not count_failed[0]:
                count_failed[0]=True;return -25204
            return old_count(ref,name,out)
        b.a.AXUIElementCopyAttributeValue=Fn(role);b.a.AXUIElementGetAttributeValueCount=Fn(count)
        self.install(s,io,b)
        def sleep(n):sleeps.append(n);now[0]+=n
        io.sleep=sleep
        self.assertEqual(s.initial_picker(),3)
        self.assertEqual(sleeps,[.1,.1,.1]);self.assertEqual(s.initial_completed_pass,4)
        self.assertEqual(s.mode,'strict');self.assertEqual(s.readiness_end,6);self.assertEqual(s.experiment_end,8)
        self.assertAlmostEqual(s.end,2.3)
        failures=[e for e in s.trace if e['return_code']==-25204]
        self.assertEqual([(e['pass'],e['attribute']) for e in failures],[(1,'AXRole'),(2,'AXRole'),(3,'AXWindows')])
        self.assertEqual([r['return_code'] for r in s.rows[1]['reads'] if r['attribute']=='AXRole'],[-25204,-25204,0,0])
        self.assertEqual(s.rows[1]['property_provenance']['role']['pass'],4)
        self.assertTrue(all(abs(e['start_elapsed']+e['phase_remaining_before']-6)<1e-8 for e in s.trace if e['phase']=='initial'))

    def test_persistent_failure_four_passes_and_sealed_on_refusal(self):
        s,io,b,now=context(initial=True);attempts=self.fails(b,10);self.install(s,io,b)
        with self.assertRaises(d.StructuralReadFailure):s.initial_picker()
        self.assertEqual(len(attempts),4);self.assertAlmostEqual(now[0],.3)
        self.assertEqual(s.mode,'strict');self.assertIsNone(s.initial_completed_pass)
        before=list(b.log)
        with self.assertRaises(Refusal):s.initial_picker()
        with self.assertRaises(Refusal):s.role(2)
        self.assertEqual(b.log,before)
        self.assertFalse(any(row[0]=='count' for row in b.log))

    def test_moved_failure_and_failed_range_recount(self):
        s,io,b,now=context(initial=True);original=b.a.AXUIElementCopyAttributeValue.call
        parent_failed=[False]
        def parent(ref,name,out):
            if ref==3 and name=='AXParent' and not parent_failed[0]:parent_failed[0]=True;return -25204
            return original(ref,name,out)
        b.a.AXUIElementCopyAttributeValue=Fn(parent)
        old_range=b.a.AXUIElementCopyAttributeValues.call;range_failed=[False]
        def ranged(ref,name,start,count,out):
            if ref==1 and name=='AXWindows' and not range_failed[0]:range_failed[0]=True;return -25204
            return old_range(ref,name,start,count,out)
        b.a.AXUIElementCopyAttributeValues=Fn(ranged);self.install(s,io,b)
        self.assertEqual(s.initial_picker(),3)
        self.assertEqual(s.initial_completed_pass,3)
        events=[e for e in s.trace if e['attribute']=='AXWindows' and e['api']!='bounded_owner_composite']
        self.assertEqual([(e['pass'],e['api']) for e in events[:4]],[(1,'AXUIElementGetAttributeValueCount'),(1,'AXUIElementCopyAttributeValues'),(2,'AXUIElementGetAttributeValueCount'),(2,'AXUIElementCopyAttributeValues')])

    def test_failed_count_is_unknown_not_zero_and_no_range_follows(self):
        s,io,b,now=context(initial=True)
        old=b.a.AXUIElementGetAttributeValueCount.call
        def count(ref,name,out):
            if ref==1 and name=='AXWindows':C.cast(out,C.POINTER(C.c_long))[0]=0;return -25204
            return old(ref,name,out)
        b.a.AXUIElementGetAttributeValueCount=Fn(count);self.install(s,io,b)
        with self.assertRaises(d.StructuralReadFailure):s.initial_picker()
        failed=[e for e in s.trace if e['attribute']=='AXWindows' and e['api']=='AXUIElementGetAttributeValueCount']
        self.assertEqual(len(failed),4);self.assertTrue(all(e['count'] is None for e in failed))
        self.assertFalse(any(row[0]=='range' and row[1:3]==(1,'AXWindows') for row in b.log))

    def test_nonusable_copies_other_codes_and_types_never_retry(self):
        for code,kind in ((-25204,'CFString'),(-25204,'CFArray'),(-25202,'null'),(-25205,'null'),(-25212,'null'),(0,'null')):
            s,io,b,now=context(initial=True);attempts=self.fails(b,10,code=code,kind=kind);self.install(s,io,b)
            with self.assertRaises(Refusal):s.initial_picker()
            self.assertEqual(len(attempts),1);self.assertEqual(now[0],0);self.assertEqual(s.mode,'strict')
            self.assertNotIn('SECRET',repr(s.trace));self.assertFalse(any(row[0]=='decode-array' for row in b.log))

    def test_wrong_or_drifting_original_and_semantic_failures_are_fatal(self):
        for case in ('role','foreign','birth','main','app','ambiguous','changed-picker'):
            s,io,b,now=context(initial=True)
            if case=='role':b.nodes[2]['role']='AXSheet'
            if case=='foreign':b.nodes[2]['owner']=999
            if case=='birth':io.identity['start_usec']+=1
            if case=='main':io.ax.main=99
            if case=='app':io.ax.app=99
            if case=='ambiguous':
                b.nodes[9]={'role':'AXSheet','AXParent':2};b.nodes[1]['AXWindows'].append(9)
            if case=='changed-picker':
                s.picker_anchor=9
            with self.assertRaises(Refusal):s.initial_picker()
            self.assertEqual(now[0],0,case);self.assertEqual(s.mode,'strict')

    def test_candidate_retained_when_later_routing_pass_changes(self):
        s,io,b,now=context(initial=True)
        original=b.a.AXUIElementCopyAttributeValue.call;failed=[False]
        def read(ref,name,out):
            if ref==1 and name=='AXFocusedUIElement' and not failed[0]:failed[0]=True;return -25204
            return original(ref,name,out)
        b.a.AXUIElementCopyAttributeValue=Fn(read);self.install(s,io,b)
        def sleep(n):
            now[0]+=n;b.nodes[9]={'role':'AXSheet','AXParent':2,'AXChildren':[],'AXSheets':[]}
            b.nodes[1]['AXWindows']=[2,9];b.nodes[2]['AXSheets']=[9]
        io.sleep=sleep
        with self.assertRaises(Refusal):s.initial_picker()
        self.assertEqual(s.picker_anchor,3);self.assertEqual(s.mode,'strict')

    def test_read_owner_trace_and_ref_caps_precede_calls(self):
        s,io,b,now=context(initial=True);s.mode='initial';s.end=6;s.begin();b.log.clear();s.initial_reads=64
        with self.assertRaises(Refusal):s.role(2)
        self.assertEqual(b.log,[])
        s,io,b,now=context(initial=True);s.mode='initial';s.end=6;s.begin();b.log.clear();s.initial_owners=128
        with self.assertRaises(Refusal):s.owner(2,s.rows[1])
        self.assertEqual(b.log,[])
        s,io,b,now=context();b.log.clear();s.op_count=512
        with self.assertRaises(Refusal):s.role(2)
        self.assertEqual(b.log,[])
        s,io,b,now=context()
        for n in range(20,50):b.nodes[n]={'role':'AXButton','AXParent':3};s.touch(n)
        b.log.clear();b.nodes[99]={'role':'AXButton','AXParent':3}
        with self.assertRaises(Refusal):s.touch(99)
        self.assertEqual(b.log,[])

    def test_exact_cfequal_alias_owner_and_read_use_actual_call_ref(self):
        s,io,b,now=context();b.nodes[22]=dict(b.nodes[2]);b.equal=lambda a,c:(2 if a==22 else a)==(2 if c==22 else c)
        b.log.clear();self.assertEqual(s.role(22),'AXWindow')
        self.assertEqual(s.touch_ordinal(22),s.touch_ordinal(2))
        self.assertIn(('owner',22),b.log);self.assertIn(('attribute',22,'AXRole'),b.log)
        self.assertIn(('timeout-exact',22,.2),b.log)
        self.assertNotIn(('timeout-exact',2,.2),b.log)
        self.assertFalse(any(row[0]=='owner' and row[1]==2 for row in b.log))

    def test_native_timing_is_separate_from_decode_and_receipt(self):
        s,io,b,now=context();original=b.a.AXUIElementCopyAttributeValue.call
        def native(ref,name,out):now[0]+=.002;return original(ref,name,out)
        b.a.AXUIElementCopyAttributeValue=Fn(native);self.install(s,io,b)
        scalar=b.scalar
        def decode(pointer):now[0]+=.03;return scalar(pointer)
        b.scalar=decode
        def record(kind,value):now[0]+=.04
        io.record=record
        self.assertEqual(s.role(2),'AXWindow')
        event=next(e for e in reversed(s.trace) if e['api']=='AXUIElementCopyAttributeValue')
        self.assertAlmostEqual(event['native_duration'],.002);self.assertAlmostEqual(event['post_native_processing_duration'],.03)
        self.assertAlmostEqual(event['duration'],.032)
        self.assertIn('composite',next(e for e in s.trace if e['api']=='bounded_owner_composite')['duration_scope'])
        self.assertGreaterEqual(s.receipt_seconds,.08)

    def test_late_native_success_failure_decode_identity_or_sleep_admits_no_more(self):
        for case in ('success','failure','decode','identity','sleep'):
            s,io,b,now=context(initial=True)
            if case in ('success','failure'):
                original=b.a.AXUIElementCopyAttributeValue.call
                def read(ref,name,out):
                    if ref==2 and name=='AXRole':
                        now[0]=6.01
                        return original(ref,name,out) if case=='success' else -25204
                    return original(ref,name,out)
                b.a.AXUIElementCopyAttributeValue=Fn(read);self.install(s,io,b)
            if case=='decode':
                old_scalar=b.scalar
                def scalar(pointer):now[0]=6.01;return old_scalar(pointer)
                b.scalar=scalar
            if case=='identity':io.check=lambda value:now.__setitem__(0,6.01)
            if case=='sleep':
                self.fails(b,10);self.install(s,io,b);io.sleep=lambda n:now.__setitem__(0,6.01)
            with self.assertRaises(Refusal):s.initial_picker()
            self.assertEqual(s.mode,'strict');self.assertEqual(s.experiment_end,8)
            before=list(b.log)
            with self.assertRaises(Refusal):s.role(2)
            self.assertEqual(b.log,before)
            self.assertIsNone(s.initial_completed_pass)

    def test_strict_final_failure_never_returns_to_initial_or_posts(self):
        s,io,b,now=context(initial=True);picker=s.initial_picker();attempts=self.fails(b,10);self.install(s,io,b);api=Posting()
        with self.assertRaises(Refusal):d.FixedGesture(api).run(s,picker,lambda *a:None)
        self.assertEqual(len(attempts),1);self.assertEqual(api.posts,[]);self.assertEqual(now[0],0)
        self.assertEqual(api.freed,[103,102,101]);self.assertEqual(s.mode,'strict')

    def test_late_pause_and_insufficient_read_headroom_do_not_reset_R_E_S(self):
        s,io,b,now=context(initial=True);self.fails(b,10);self.install(s,io,b)
        now[0]=5.75
        with self.assertRaises(Refusal):s.initial_picker()
        self.assertEqual(s.readiness_end,6);self.assertEqual(s.experiment_end,8)
        self.assertEqual(now[0],5.75)
        s,io,b,now=context(initial=True);self.fails(b,10);self.install(s,io,b)
        io.sleep=lambda n:now.__setitem__(0,6.1)
        with self.assertRaises(Refusal):s.initial_picker()
        self.assertEqual(s.readiness_end,6);self.assertEqual(s.experiment_end,8)

    def test_receipt_mutation_cannot_rebind_identity_properties_or_counters(self):
        s,io,b,now=context(initial=True)
        def mutate(kind,value):value.update(op=9999,pass_=9999,ordinal=9999,return_code=0);value['owner_match']=True
        io.record=mutate;self.assertEqual(s.initial_picker(),3)
        self.assertEqual(s.original,ORIGINAL);self.assertTrue(all(e['op']<9999 for e in s.trace))
        self.assertLess(s.initial_reads,64);self.assertLess(s.initial_owners,128)
        self.assertTrue(all(r['ordinal']<32 for r in s.rows))

    def test_unknown_native_RC_is_null_and_fatal(self):
        s,io,b,now=context(initial=True);b.a.AXUIElementCopyAttributeValue=Fn(lambda *a:None);self.install(s,io,b)
        with self.assertRaises(Refusal):s.initial_picker()
        event=next(e for e in s.trace if e['api']=='AXUIElementCopyAttributeValue')
        self.assertIsNone(event['return_code']);self.assertEqual(s.mode,'strict')

    def test_initial_success_near_six_has_strict_two_and_snapshot_one_clipped(self):
        s,io,b,now=context(initial=True);now[0]=5.5
        picker=s.initial_picker();self.assertAlmostEqual(s.end,7.5);self.assertEqual(s.experiment_end,8)
        now[0]=7.1;s.command_picker=picker;s.snapshot(picker,True)
        self.assertLessEqual(s.end,7.5);self.assertEqual(s.mode,'strict')

    def test_late_owner_and_receipt_stop_without_more_observations(self):
        for case in ('owner','receipt'):
            s,io,b,now=context(initial=True)
            if case=='owner':
                original=b.owner
                def owner(ref):
                    result=original(ref)
                    if ref==2:now[0]=6.01
                    return result
                b.owner=owner
            else:
                def receipt(kind,value):
                    if value['api']=='AXUIElementCopyAttributeValue':now[0]=6.01
                io.record=receipt
            with self.assertRaises(Refusal):s.initial_picker()
            before=list(b.log)
            with self.assertRaises(Refusal):s.role(2)
            self.assertEqual(b.log,before);self.assertEqual(s.mode,'strict')
            self.assertIn('late',s.stopped)

    def test_guard_duration_and_missing_RC_are_honestly_labelled(self):
        s,io,b,now=context();original=b.owner
        def owner(ref):now[0]+=.007;return original(ref)
        b.owner=owner;s.role(2)
        event=next(e for e in reversed(s.trace) if e['api']=='bounded_owner_composite')
        self.assertAlmostEqual(event['duration'],.007);self.assertIsNone(event['native_duration'])
        self.assertEqual(event['duration_scope'],'SetMessagingTimeout(.2)+GetPid composite')
        identity=next(e for e in s.trace if e['api']=='identity_guard')
        self.assertIsNone(identity['return_code'])
        self.assertIn('uninstrumented',s.summary()['cleanup_and_paired_release_identity_timing'])

    def test_last_properties_from_failed_earlier_pass_are_not_current_proof(self):
        s,io,b,now=context(initial=True);old_value=b.a.AXUIElementCopyAttributeValue.call
        roles=[0]
        def role(ref,name,out):
            if ref==2 and name=='AXRole':
                roles[0]+=1
                if roles[0]>1:return -25204
            return old_value(ref,name,out)
        old_count=b.a.AXUIElementGetAttributeValueCount.call
        def count(ref,name,out):
            if ref==1 and name=='AXWindows':return -25204
            return old_count(ref,name,out)
        b.a.AXUIElementCopyAttributeValue=Fn(role);b.a.AXUIElementGetAttributeValueCount=Fn(count);self.install(s,io,b)
        with self.assertRaises(Refusal):s.initial_picker()
        self.assertEqual(s.rows[1]['role'],'AXWindow')
        self.assertEqual(s.rows[1]['property_provenance']['role']['pass'],1)
        self.assertEqual(s.rows[1]['property_meaning'],'last_observed_only_not_readiness')
        self.assertIsNone(s.initial_completed_pass)
        self.assertEqual([r['pass'] for r in s.rows[1]['reads'] if r['attribute']=='AXRole'],[1,2,3,4])

    def test_fast_or_wait_length_failure_is_timed_without_cause_claim(self):
        for duration in (.002,.199):
            s,io,b,now=context(initial=True);original=b.a.AXUIElementCopyAttributeValue.call
            def value(ref,name,out):
                if ref==2 and name=='AXRole':now[0]+=duration;return -25204
                return original(ref,name,out)
            b.a.AXUIElementCopyAttributeValue=Fn(value);self.install(s,io,b)
            with self.assertRaises(Refusal):s.initial_picker()
            failed=[e for e in s.trace if e['api']=='AXUIElementCopyAttributeValue']
            self.assertEqual(len(failed),4)
            for event in failed:
                self.assertAlmostEqual(event['native_duration'],duration)
                self.assertEqual(event['requested_timeout'],.2)
                self.assertNotIn('cause',event)

    def test_nonnull_failed_range_and_timeout_setup_failure_are_fatal(self):
        s,io,b,now=context(initial=True);b.arrays[9990]=[2,3]
        def ranged(ref,name,start,count,out):C.cast(out,C.POINTER(C.c_void_p))[0]=9990;return -25204
        b.a.AXUIElementCopyAttributeValues=Fn(ranged);self.install(s,io,b)
        with self.assertRaises(Refusal):s.initial_picker()
        self.assertFalse(any(row[0]=='decode-array' for row in b.log));self.assertEqual(now[0],0)
        s,io,b,now=context(initial=True);b.a.AXUIElementSetMessagingTimeout=Fn(lambda *a:-25202)
        with self.assertRaises(Refusal):s.initial_picker()
        self.assertFalse(any(row[0]=='attribute' for row in b.log));self.assertEqual(s.mode,'strict')
        event=next(e for e in s.trace if e['api']=='bounded_owner_composite')
        self.assertIsNone(event['return_code'])

    def test_input_trace_reserve_refuses_before_dispatch(self):
        s,io,b,now=context();picker=s.picker();api=Posting()
        def intent(*a):s.op_count=511
        with self.assertRaises(Refusal):d.FixedGesture(api).run(s,picker,intent)
        self.assertEqual(api.posts,[]);self.assertEqual(api.freed,[103,102,101])

    def test_failed_range_recounts_changed_size_before_next_range(self):
        s,io,b,now=context(initial=True);original=b.a.AXUIElementCopyAttributeValues.call;failed=[False]
        b.nodes[9]={'role':'AXButton','AXParent':2}
        def ranged(ref,name,start,count,out):
            if ref==2 and name=='AXChildren' and not failed[0]:
                failed[0]=True;b.nodes[2]['AXChildren']=[3,9];return -25204
            return original(ref,name,start,count,out)
        b.a.AXUIElementCopyAttributeValues=Fn(ranged);self.install(s,io,b)
        self.assertEqual(s.initial_picker(),3)
        events=[e for e in s.trace if e['attribute']=='AXChildren' and e['ordinal']==1]
        self.assertEqual(events[0]['count'],1);self.assertEqual(events[1]['requested_count'],1)
        self.assertEqual(events[2]['count'],2);self.assertEqual(events[3]['requested_count'],2)

    def test_caps_and_malformed_success_are_semantic_not_readiness(self):
        for size in (5,13):
            s,io,b,now=context(initial=True);b.nodes[1]['AXWindows']=[2]*size
            with self.assertRaises(Refusal):s.initial_picker()
            self.assertFalse(any(row[0]=='range' for row in b.log));self.assertEqual(now[0],0)
        s,io,b,now=context(initial=True);original=b.a.AXUIElementCopyAttributeValues.call
        def short(ref,name,start,count,out):return original(ref,name,start,1,out)
        b.a.AXUIElementCopyAttributeValues=Fn(short);self.install(s,io,b)
        with self.assertRaises(Refusal):s.initial_picker()
        self.assertEqual(now[0],0);self.assertEqual(s.mode,'strict')

    def test_work_deadline_and_four_pass_limits_never_reset(self):
        s,io,b,now=context(initial=True);s.work_end=5.5;s.experiment_end=5.5
        self.fails(b,20);self.install(s,io,b)
        with self.assertRaises(Refusal):s.initial_picker()
        self.assertEqual(s.readiness_end,3.5);self.assertLessEqual(s.end,5.5)
        self.assertTrue(all(e['phase_remaining_before']<=3.5 for e in s.trace if e['phase']=='initial'))

    def test_late_native_range_does_not_decode_or_follow_returned_refs(self):
        s,io,b,now=context(initial=True);original=b.a.AXUIElementCopyAttributeValues.call
        def late(ref,name,start,count,out):
            result=original(ref,name,start,count,out);now[0]=6.01;return result
        b.a.AXUIElementCopyAttributeValues=Fn(late);self.install(s,io,b)
        with self.assertRaises(Refusal):s.initial_picker()
        self.assertFalse(any(row[0]=='decode-array' for row in b.log))
        self.assertFalse(any(row==('owner',3) for row in b.log))
        self.assertTrue(b.held)  # returned retained array is still owned for final release

    def test_exhausted_read_budget_does_not_issue_retry_provenance_queries(self):
        s,io,b,now=context(initial=True);s.initial_reads=63
        attempts=self.fails(b,10);self.install(s,io,b)
        with self.assertRaises(Refusal):s.initial_picker()
        self.assertEqual(len(attempts),1);self.assertEqual(s.initial_reads,64);self.assertEqual(now[0],0)
        failure_index=next(i for i,row in enumerate(b.log) if row[0]=='failed-read')
        self.assertFalse(any(row[0] in ('owner','attribute','count','range') for row in b.log[failure_index+1:]))


class GestureTests(unittest.TestCase):
    def test_trace_failure_or_cap_after_down_cannot_block_same_original_up(self):
        for case in ('cap','receipt'):
            s,io,b,now=context();picker=s.picker();api=Posting()
            def down():
                if case=='cap':s.op_count=512;s.halt('injected exhausted trace')
                else:io.record=lambda *a:(_ for _ in ()).throw(OSError('injected receipt failure'))
            api.on_down=down
            d.FixedGesture(api).run(s,picker,lambda *a:None)
            self.assertEqual([p[1] for p in api.posts],[102,103])
            self.assertEqual(api.freed,[103,102,101])
    def test_preexisting_nested_sheet_never_receives_navigation(self):
        for published_in_windows in (False, True):
            with self.subTest(published_in_windows=published_in_windows):
                s, io, b, now = context(); api = Posting()
                b.nodes[9] = {'role': 'AXSheet', 'AXParent': 3, 'AXChildren': []}
                b.nodes[3]['AXSheets'] = [9]
                b.nodes[4]['AXParent'] = 9
                if published_in_windows:
                    b.nodes[1]['AXWindows'].append(9)
                with self.assertRaises(Refusal):
                    picker = s.picker()
                    d.FixedGesture(api).run(s, picker, lambda *args: None)
                self.assertEqual(api.posts, [])

    def test_nested_sheet_after_intent_prevents_dispatch(self):
        s, io, b, now = context(); picker = s.picker(); api = Posting()
        def receipt(*args):
            b.nodes[9] = {'role': 'AXSheet', 'AXParent': 3, 'AXChildren': []}
            b.nodes[3]['AXSheets'] = [9]
        with self.assertRaises(Refusal):
            d.FixedGesture(api).run(s, picker, receipt)
        self.assertEqual(api.posts, [])
        self.assertEqual(api.freed, [103, 102, 101])

    def test_missing_parent_or_intermediate_modal_prevents_dispatch(self):
        for case in ('missing-parent', 'intermediate-modal'):
            with self.subTest(case=case):
                s, io, b, now = context(); picker = s.picker(); api = Posting()
                if case == 'missing-parent':
                    b.nodes[4].pop('AXParent')
                else:
                    b.nodes[5]['role'] = 'AXSheet'
                with self.assertRaises(Refusal):
                    d.FixedGesture(api).run(s, picker, lambda *args: None)
                self.assertEqual(api.posts, [])

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
            if case == 'picker': b.nodes[2]['AXChildren'] = []
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
            if getattr(backend,'terminate_error',False):raise OSError('invented unknown normal request')
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
            if (kind == 'diagnostic-call' and getattr(backend, 'fail_focus_pause_receipt', False)
                    and value.get('api') == 'sleep' and value.get('requested_sleep') == .2):
                backend.focus_pause_receipt_failed = True
                raise OSError('invented focus pause receipt failure')
            if (getattr(backend,'receipt_failure_after_down',False) and getattr(backend,'down_started',False)
                    and kind==getattr(backend,'failure_after_down_kind',kind)):
                raise OSError('invented post-down evidence failure')
            if getattr(backend,'mutate_receipts',False) and kind in ('diagnostic-structure','diagnostic-binding-refusal'):
                value['complete']=False
                if value.get('nodes'):value['nodes'][0]['owner_match']=False
            records.append((kind, deepcopy(value)))
        def factory():
            if unavailable: raise AttributeError('invented missing API')
            return api
        if configure: configure(backend, api, now)
        backend.sleep_calls=[]
        def sleep(seconds):
            backend.sleep_calls.append(seconds)
            now[0]+=seconds
            if hasattr(backend,'sleep_hook'):backend.sleep_hook()
        with ExitStack() as stack:
            for name, fn in {'admit': admit, 'launch_once': launch, 'check': check,
                'original_main': main, 'startup_facts': lambda io: {'root_count':1,'self_reference_count':0,'match_count':1,'transient_return_category':'ready'},
                'observe': observe, 'revalidate': lambda io,v,c,end:c, 'press':lambda io,c,end:0,
                'supplier_started':lambda io:False,
                'absent':lambda io,i:appkit.closed or now[0] >= getattr(backend,'late_close_at',float('inf'))}.items():
                stack.enter_context(patch.object(NativeSession, name, fn))
            stack.enter_context(patch.object(d, 'NativePosting', factory))
            self.last_fixture=(counts,api,backend,appkit,records)
            result = d.run_prepared(S, {}, record, lambda:now[0], sleep)
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

    def test_returned_main_alias_owner_refusal_still_cleans_up_without_input(self):
        def configure(b, api, now):
            b.nodes[22] = dict(b.nodes[2], owner=999)
            b.equal = lambda left, right: (2 if left == 22 else left) == (2 if right == 22 else right)
            b.nodes[1]['AXWindows'] = [22]
        result, counts, api, b, app, records = self.full(configure=configure)
        self.assertEqual(api.posts, []); self.assertEqual(app.terminations, 1)
        self.assertTrue(result['original_absent']); self.assertEqual(counts['launches'], 1)
        self.assertFalse(result['diagnostic']['gesture_state']['consumed'])
        self.assertNotIn('diagnostic-navigation-intent', [kind for kind, value in records])
        self.assertFalse(any(e[:2] == ('attribute', 22) for e in b.log))

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

    def test_actual_controller_observed_geometry_cap_stays_partial_and_cleans_up(self):
        def configure(b,api,now):observed_shape(b)
        result,counts,api,b,app,records=self.full(configure=configure)
        self.assertEqual(counts['launches'],1);self.assertEqual(len(api.posts),2)
        self.assertEqual(app.terminations,1);self.assertTrue(result['original_absent'])
        self.assertEqual(result['diagnostic']['proof_mode'],d.Structure.PROOF_MODE)
        self.assertEqual(len(result['diagnostic']['target_proofs']),3)
        self.assertFalse(result['diagnostic']['snapshot']['complete'])
        self.assertEqual(result['diagnostic']['snapshot']['error_category'],'diagnostic trace capacity')
        self.assertEqual(result['diagnostic']['snapshot']['budget']['reserved_operations'],512)
        self.assertFalse(result['diagnostic']['snapshot']['selection_complete'])
        for key in ('setup_saved','J1_complete','qualification','flow_complete'):self.assertFalse(result[key])

    def test_mandatory_parent_refusal_or_strict_drift_always_autonomous_cleanup(self):
        for case in ('unsupported','foreign','changed_during_strict'):
            def configure(b,api,now):
                old=b.a.AXUIElementCopyAttributeValue.call;reads=[0]
                def read(ref,name,out):
                    if (ref,name)==(4,'AXParent'):
                        reads[0]+=1
                        if case=='unsupported':return -25205
                        if case=='foreign':b.nodes[3]['owner']=999
                        if case=='changed_during_strict' and reads[0]==5:b.nodes[4]['AXParent']=2
                    return old(ref,name,out)
                b.a.AXUIElementCopyAttributeValue.call=read
            result,counts,api,b,app,records=self.full(configure=configure)
            self.assertEqual(api.posts,[],case);self.assertEqual(app.terminations,1)
            self.assertTrue(result['original_absent']);self.assertFalse(result['setup_saved'])

    def test_actual_controller_selected_ancestry_has_no_shortcut_even_after_pair(self):
        def configure(b,api,now):
            observed_shape(b);old=b.a.AXUIElementCopyAttributeValue.call
            def value(ref,name,out):
                self.assertNotIn(name,('AXTopLevelUIElement','AXWindow','AXFocusedWindow'))
                return old(ref,name,out)
            b.a.AXUIElementCopyAttributeValue.call=value
        result,counts,api,b,app,records=self.full(configure=configure)
        self.assertEqual(len(api.posts),2);self.assertEqual(app.terminations,1)
        self.assertTrue(result['original_absent']);self.assertFalse(result['setup_saved'])
        proof=result['diagnostic']['target_proofs'][-1]
        self.assertEqual(proof['proof_mode'],'POSITIVE_FOCUSED_ANCESTRY_DIAGNOSTIC_V1')
        self.assertEqual(proof['nearest_modal_proof']['nearest_modal_role'],'AXSheet')
        self.assertNotIn('top_level',repr(result['diagnostic']))

    def test_main_legacy_absence_is_unknown_but_standard_children_required(self):
        for code in (-25205, -25212):
            for required_absent in (False,True):
                with self.subTest(code=code,required_absent=required_absent):
                    def configure(b, api, now):
                        original = b.a.AXUIElementGetAttributeValueCount.call
                        def absent(ref, name, out):
                            if ref == 2 and (name=='AXSheets' or required_absent and name=='AXChildren'):
                                return code
                            return original(ref, name, out)
                        b.a.AXUIElementGetAttributeValueCount.call = absent
                    result, counts, api, b, app, records = self.full(configure=configure)
                    self.assertEqual(len(api.posts), 0 if required_absent else 2)
                    self.assertFalse(b.sleep_calls)
                    if not required_absent:
                        self.assertEqual(result['diagnostic']['snapshot']['budget']['initial_completed_pass'], 1)
                        self.assertTrue(result['diagnostic']['snapshot']['complete'])
                    self.assertTrue(result['original_absent'])
                    self.assertEqual(app.terminations, 1)

    def test_initial_binding_read_failure_retains_only_partial_safe_facts(self):
        for case in ('role', 'count', 'owner'):
            with self.subTest(case=case):
                def configure(b, api, now):
                    if case == 'role':
                        original = b.a.AXUIElementCopyAttributeValue.call
                        def value(ref, name, out):
                            if ref == 2 and name == 'AXRole':
                                b.log.append(('failed-role', ref))
                                b.stopped_log = list(b.log)
                                return -25204
                            return original(ref, name, out)
                        b.a.AXUIElementCopyAttributeValue = Fn(value)
                    elif case == 'count':
                        original = b.a.AXUIElementGetAttributeValueCount.call
                        def count(ref, name, out):
                            if ref == 1 and name == 'AXWindows':
                                b.log.append(('failed-count', ref))
                                b.stopped_log = list(b.log)
                                return -25204
                            return original(ref, name, out)
                        b.a.AXUIElementGetAttributeValueCount = Fn(count)
                    else:
                        b.nodes[2]['owner'] = 999
                result, counts, api, b, app, records = self.full(configure=configure)
                partial = result['diagnostic']['binding_refusal']
                self.assertEqual(partial['stage'], 'binding')
                self.assertFalse(partial['complete'])
                self.assertIsNone(result['diagnostic']['snapshot'])
                self.assertFalse(partial['readiness'])
                self.assertEqual(api.posts, [])
                self.assertEqual(app.terminations, 1)
                self.assertTrue(result['original_absent'])
                self.assertIn('diagnostic-binding-refusal', [k for k,v in records])
                self.assertNotIn('SECRET', repr(partial))
                if case in ('role', 'count'):
                    self.assertEqual(b.log, b.stopped_log)  # no recovery AX query
                    reads = [r for node in partial['nodes'] for r in node['reads']]
                    failed = next(r for r in reads if r['return_code'] == -25204)
                    self.assertEqual(failed['attribute'], 'AXRole' if case == 'role' else 'AXWindows')
                    if case == 'count':
                        self.assertIsNone(failed['count'])
                else:
                    self.assertFalse(partial['nodes'][-1]['owner_match'])

    def test_binding_refusal_receipt_failure_still_cleans_up(self):
        def configure(b, api, now):
            b.nodes[2]['owner'] = 999
        result, counts, api, b, app, records = self.full(
            configure=configure, fail_record='diagnostic-binding-refusal')
        self.assertEqual(app.terminations, 1)
        self.assertTrue(result['original_absent'])
        self.assertEqual(api.posts, [])
        self.assertIsNone(result['diagnostic']['snapshot'])

    def test_returned_foreign_ref_still_vetoes_input_and_cleans_up_with_or_without_receipt(self):
        for failure in (None, 'diagnostic-binding-refusal'):
            with self.subTest(failure=failure):
                def configure(b, api, now):
                    observed_shape(b)
                    b.nodes[22]['AXChildren'] = [21, 25]
                    b.nodes[25] = {'owner': 999, 'role': 'SECRET', 'AXParent': 22}
                result, counts, api, b, app, records = self.full(configure=configure, fail_record=failure)
                self.assertEqual(api.posts, []); self.assertEqual(app.terminations, 1)
                self.assertTrue(result['original_absent']); self.assertEqual(counts['launches'], 1)
                self.assertFalse(any(e[0] in ('attribute', 'count', 'range') and e[1] == 25 for e in b.log))
                self.assertFalse(result['setup_saved']); self.assertFalse(result['J1_complete'])
                self.assertIsNone(result['diagnostic']['snapshot'])
                if failure is None:
                    partial = result['diagnostic']['binding_refusal']
                    row = next(r for r in partial['nodes'] if r['owner_match'] is False)
                    self.assertEqual(row['owner_pid'], 999)
                    self.assertEqual(row['last_return']['attribute'], 'AXChildren')
                    self.assertFalse(partial['readiness']); self.assertEqual(partial['target_proofs'], [])
                    self.assertNotIn('SECRET', repr(partial))
    def test_initial_role_wait_uses_actual_experiment_and_original_cleanup(self):
        for failures in (1,2):
            def configure(b,api,now):CommunicationPolicyTests.fails(self,b,failures)
            result,counts,api,b,app,records=self.full(configure=configure)
            self.assertEqual(b.sleep_calls,[.1]*failures)
            self.assertEqual(len(api.posts),2);self.assertEqual(app.terminations,1)
            self.assertEqual(result['actions'],['open project picker'])
            self.assertTrue(result['diagnostic']['snapshot']['complete'])
            main=result['diagnostic']['snapshot']['nodes'][1]
            role_reads=[r['return_code'] for r in main['reads'] if r['attribute']=='AXRole']
            self.assertEqual(role_reads[:failures],[-25204]*failures)
            self.assertEqual(role_reads[failures],0)
            for key in ('setup_saved','J1_complete','qualification'):self.assertFalse(result[key])

    def test_persistent_initial_communication_and_receipt_failure_cleanup_after_four(self):
        for receipt in (None,'diagnostic-binding-refusal'):
            def configure(b,api,now):CommunicationPolicyTests.fails(self,b,10)
            result,counts,api,b,app,records=self.full(configure=configure,fail_record=receipt)
            partial=result['diagnostic']['binding_refusal']
            reads=[r for node in partial['nodes'] for r in node['reads'] if r['attribute']=='AXRole']
            self.assertEqual([r['return_code'] for r in reads],[-25204]*4)
            self.assertEqual(b.sleep_calls,[.1,.1,.1]);self.assertEqual(api.posts,[])
            self.assertFalse(result['diagnostic']['gesture_state']['consumed'])
            self.assertEqual(app.terminations,1);self.assertTrue(result['original_absent'])
            self.assertFalse(any(row[0] in ('count','range') for row in b.log))

    def test_missing_mandatory_parent_stops_before_extra_child_boundary_reads(self):
        for code in (-25205, -25212):
            with self.subTest(code=code):
                def configure(b,api,now):
                    original=b.a.AXUIElementCopyAttributeValue.call
                    def missing(ref,name,out):
                        if (ref,name)==(4,'AXParent'):
                            b.log.append(('missing-parent',ref,code));return code
                        return original(ref,name,out)
                    b.a.AXUIElementCopyAttributeValue.call=missing
                result,counts,api,b,app,records=self.full(configure=configure)
                self.assertFalse(any(row[:3]==('count',3,'AXChildren') for row in b.log))
                self.assertTrue(any(row[0]=='missing-parent' for row in b.log))
                self.assertEqual(api.posts,[]);self.assertEqual(app.terminations,1)
                self.assertTrue(result['original_absent']);self.assertIsNone(result['diagnostic']['snapshot'])

    def test_late_initial_read_or_sleep_starts_autonomous_cutoff_cleanup(self):
        for case in ('read','sleep'):
            def configure(b,api,now):
                hook=(lambda:now.__setitem__(0,110)) if case=='read' else None
                CommunicationPolicyTests.fails(self,b,10,hook=hook)
                if case=='sleep':b.sleep_hook=lambda:now.__setitem__(0,110)
            result,counts,api,b,app,records=self.full(configure=configure)
            self.assertEqual(result['cleanup_started'],110)
            self.assertEqual(app.terminations,1);self.assertEqual(api.posts,[])
            self.assertEqual(result['actions'],['open project picker'])
            self.assertIsNone(result['diagnostic']['snapshot'])
            self.assertFalse(any(row[0] in ('count','range') for row in b.log))
            self.assertEqual(b.sleep_calls,[] if case=='read' else [.1])

    def test_receipt_failures_do_not_skip_autonomous_cleanup(self):
        for kind in ('diagnostic-navigation-intent','diagnostic-structure','cleanup-intent','normal-terminate-intent'):
            result, counts, api, b, app, records = self.full(fail_record=kind)
            self.assertEqual(app.terminations, 1, kind)
            self.assertTrue(result['original_absent'])
            if kind == 'diagnostic-navigation-intent': self.assertEqual(api.posts, [])

    def test_initial_routing_refusal_zero_posts_partial_binding_and_cleanup(self):
        def configure(b, api, now): b.nodes[1].pop('AXFocusedUIElement')
        result, counts, api, b, app, records = self.full(configure=configure)
        self.assertEqual(api.posts, [])
        self.assertIsNone(result['diagnostic']['snapshot'])
        self.assertFalse(result['diagnostic']['binding_refusal']['complete'])
        self.assertEqual(app.terminations, 1)

    def test_preexisting_nested_modal_zero_posts_and_autonomous_cleanup(self):
        def configure(b, api, now):
            b.nodes[9] = {'role': 'AXSheet', 'AXParent': 3, 'AXChildren': []}
            b.nodes[3]['AXSheets'] = [9]
            b.nodes[4]['AXParent'] = 9
        result, counts, api, b, app, records = self.full(configure=configure)
        self.assertEqual(api.posts, [])
        self.assertEqual(app.terminations, 1)
        self.assertTrue(result['original_absent'])
        self.assertIsNone(result['diagnostic']['snapshot'])
        self.assertFalse(result['diagnostic']['binding_refusal']['complete'])
        self.assertFalse(result['setup_saved'])

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


    def test_recorded_prefix_actual_controller_completes_fourth_pass(self):
        def configure(b,api,now):
            CommunicationPolicyTests.fails(self,b,2)
            old=b.a.AXUIElementGetAttributeValueCount.call;failed=[False]
            def count(ref,name,out):
                if ref==1 and name=='AXWindows' and not failed[0]:failed[0]=True;return -25204
                return old(ref,name,out)
            b.a.AXUIElementGetAttributeValueCount=Fn(count)
        result,counts,api,b,app,records=self.full(configure=configure)
        self.assertEqual(b.sleep_calls,[.1,.1,.1]);self.assertEqual(len(api.posts),2)
        self.assertEqual(result['diagnostic']['snapshot']['budget']['initial_completed_pass'],4)
        self.assertTrue(result['diagnostic']['snapshot']['complete']);self.assertEqual(app.terminations,1)
        self.assertEqual(result['actions'],['open project picker'])
        for key in ('setup_saved','J1_complete','qualification'):self.assertFalse(result[key])

    def test_trace_failure_still_normal_cleanup_and_false_unknown_hold(self):
        for unknown in (False,True):
            def configure(b,api,now):b.late_close_at=182;b.terminate_error=unknown
            result,counts,api,b,app,records=self.full(configure=configure,fail_record='diagnostic-call')
            self.assertEqual(app.terminations,1);self.assertEqual(api.posts,[])
            self.assertTrue(result['initial_held']);self.assertGreaterEqual(result['final_overrun'],2)
            self.assertTrue(result['original_absent']);self.assertFalse(result['slot_must_remain_held'])
            self.assertIn('held',[k for k,v in records]);self.assertIn('late-absence',[k for k,v in records])

    def test_evidence_failure_after_down_preserves_up_and_cleanup(self):
        def configure(b,api,now):
            b.receipt_failure_after_down=True
            b.failure_after_down_kind='diagnostic-call'
            api.on_down=lambda:setattr(b,'down_started',True)
        result,counts,api,b,app,records=self.full(configure=configure)
        self.assertEqual([p[1] for p in api.posts],[102,103])
        self.assertEqual(app.terminations,1);self.assertTrue(result['original_absent'])
        self.assertEqual(api.freed,[103,102,101])

    def test_permanent_receipt_failure_after_down_still_closes_before_raising(self):
        def configure(b,api,now):
            b.receipt_failure_after_down=True
            api.on_down=lambda:setattr(b,'down_started',True)
        with self.assertRaises(OSError):self.full(configure=configure)
        counts,api,b,app,records=self.last_fixture
        self.assertEqual([p[1] for p in api.posts],[102,103])
        self.assertEqual(app.terminations,1);self.assertTrue(app.closed);self.assertTrue(b.closed)
        self.assertEqual(api.freed,[103,102,101])

    def test_snapshot_receipt_is_detached_from_internal_result(self):
        def configure(b,api,now):b.mutate_receipts=True
        result,counts,api,b,app,records=self.full(configure=configure)
        self.assertTrue(result['diagnostic']['snapshot']['complete'])
        self.assertTrue(result['diagnostic']['snapshot']['nodes'][0]['owner_match'])
        self.assertEqual(app.terminations,1)


class FocusAvailabilityTests(unittest.TestCase):
    full = AdmissionAndRunTests.full

    def unavailable_focus(self, b, failures, code=-25212, hook=None):
        original = b.a.AXUIElementCopyAttributeValue.call
        calls = []
        def read(ref, name, out):
            if ref == 1 and name == 'AXFocusedUIElement' and len(calls) < failures:
                calls.append((ref, name))
                if hook: hook()
                return code
            return original(ref, name, out)
        b.a.AXUIElementCopyAttributeValue.call = read
        return calls

    def test_initial_focus_novalue_then_positive_without_publication_replay(self):
        for failures in (1, 2, 3):
            with self.subTest(failures=failures):
                def configure(b, api, now):
                    observed_shape(b)
                    self.unavailable_focus(b, failures)
                result, counts, api, b, app, records = self.full(configure=configure)
                self.assertEqual(b.sleep_calls, [.2] * failures)
                self.assertEqual(len(api.posts), 2)
                self.assertFalse(result['diagnostic']['snapshot']['complete'])
                self.assertEqual(result['diagnostic']['snapshot']['error_category'], 'diagnostic trace capacity')
                budget = result['diagnostic']['snapshot']['budget']
                self.assertEqual(budget['reserved_operations'], 512)
                self.assertEqual(budget['initial_completed_pass'], 1)
                self.assertEqual(budget['initial_focus_pause_reservations'], failures)
                self.assertLessEqual(budget['initial_reads'], 64)
                self.assertLessEqual(budget['initial_owner_composites'], 128)
                self.assertEqual(app.terminations, 1)
                self.assertTrue(result['original_absent'])

    def test_persistent_initial_focus_novalue_is_bounded_and_never_posts(self):
        def configure(b, api, now): self.unavailable_focus(b, 20)
        result, counts, api, b, app, records = self.full(configure=configure)
        reads = [r for n in result['diagnostic']['binding_refusal']['nodes']
                 for r in n['reads'] if r['attribute'] == 'AXFocusedUIElement']
        self.assertEqual([r['return_code'] for r in reads], [-25212] * 4)
        self.assertEqual(b.sleep_calls, [.2] * 3)
        self.assertEqual(api.posts, [])
        self.assertEqual(app.terminations, 1)
        self.assertTrue(result['original_absent'])
        self.assertIsNone(result['diagnostic']['snapshot'])

    def test_unsupported_initial_focus_and_strict_novalue_never_wait(self):
        def configure(b, api, now): self.unavailable_focus(b, 20, code=-25205)
        result, counts, api, b, app, records = self.full(configure=configure)
        self.assertEqual(b.sleep_calls, [])
        self.assertEqual(api.posts, [])
        s, io, b, now = context(); self.unavailable_focus(b, 20)
        sleeps = []; io.sleep = lambda n: sleeps.append(n)
        with self.assertRaises(Refusal): s.nearest_modal()
        self.assertEqual(sleeps, [])

    def test_late_focus_read_or_pause_cannot_extend_initial_deadline(self):
        for case in ('read', 'pause'):
            with self.subTest(case=case):
                def configure(b, api, now):
                    self.unavailable_focus(b, 20, hook=(lambda: now.__setitem__(0, 110)) if case == 'read' else None)
                    if case == 'pause': b.sleep_hook = lambda: now.__setitem__(0, 110)
                result, counts, api, b, app, records = self.full(configure=configure)
                self.assertEqual(result['cleanup_started'], 110)
                self.assertEqual(api.posts, [])
                self.assertEqual(app.terminations, 1)
                self.assertEqual(b.sleep_calls, [] if case == 'read' else [.2])

    def test_focus_pause_identity_or_owner_drift_stops_before_resample(self):
        for case in ('birth', 'picker_owner'):
            with self.subTest(case=case):
                s, io, b, now = context(initial=True)
                calls = self.unavailable_focus(b, 20)
                def sleep(n):
                    now[0] += n
                    if case == 'birth': io.identity['start_usec'] += 1
                    else: b.nodes[3]['owner'] = 999
                io.sleep = sleep
                with self.assertRaises(Refusal): s.initial_picker()
                self.assertEqual(len(calls), 1)

    def test_focus_pause_receipt_failure_still_runs_one_normal_cleanup(self):
        def configure(b, api, now):
            self.unavailable_focus(b, 20)
            b.fail_focus_pause_receipt = True
        result, counts, api, b, app, records = self.full(configure=configure)
        self.assertTrue(b.focus_pause_receipt_failed)
        self.assertEqual(b.sleep_calls, [.2])
        self.assertEqual(api.posts, [])
        self.assertEqual(app.terminations, 1)
        self.assertTrue(result['original_absent'])

    def test_focus_pause_quota_is_shared_across_initial_proof_reads(self):
        def configure(b, api, now):
            original = b.a.AXUIElementCopyAttributeValue.call
            seen = [0]
            def read(ref, name, out):
                if ref == 1 and name == 'AXFocusedUIElement':
                    seen[0] += 1
                    if seen[0] in (1, 3, 4): return -25212
                return original(ref, name, out)
            b.a.AXUIElementCopyAttributeValue.call = read
        result, counts, api, b, app, records = self.full(configure=configure)
        self.assertEqual(b.sleep_calls, [.2] * 3)
        self.assertEqual(result['diagnostic']['snapshot']['budget']['initial_focus_pause_reservations'], 3)
        self.assertEqual(len(api.posts), 2)
        self.assertTrue(result['original_absent'])

    def test_strict_and_post_focus_novalue_do_not_gain_availability_wait(self):
        for stage in ('strict', 'snapshot'):
            def configure(b, api, now):
                original = b.a.AXUIElementCopyAttributeValue.call
                seen = [0]
                def read(ref, name, out):
                    if ref == 1 and name == 'AXFocusedUIElement':
                        seen[0] += 1
                        if (stage == 'strict' and seen[0] >= 3) or getattr(b, 'after_post', False):
                            return -25212
                    return original(ref, name, out)
                b.a.AXUIElementCopyAttributeValue.call = read
                if stage == 'snapshot': api.on_down = lambda: setattr(b, 'after_post', True)
            result, counts, api, b, app, records = self.full(configure=configure)
            self.assertEqual(b.sleep_calls, [])
            self.assertEqual(len(api.posts), 0 if stage == 'strict' else 2)
            self.assertEqual(app.terminations, 1)
            self.assertTrue(result['original_absent'])


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
