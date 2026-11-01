"""Autonomous helper/gate/cleanup fixtures; no native framework or App."""
from pathlib import Path
from types import SimpleNamespace as N
from unittest.mock import patch
import unittest
import native_b_window_helper as helper
from native_attended_ports import NativePorts

class FocusSequenceTests(unittest.TestCase):
    def fixture(self,case=None):
        calls=[];observations=iter([False,False,True,True])
        ops=N(b=N(equal=lambda a,b:a==b),check_time=lambda:None,
              main=lambda expected:'main',front=lambda:next(observations),
              supports=lambda main:case!='unsupported')
        ops.raise_main=lambda main:calls.append('raise') or (1 if case=='raise' else 0)
        ops.set_front=lambda:calls.append('set') or (1 if case=='set' else 0)
        def bound(stage):
            calls.append(stage)
            if case=='window' and stage=='before-autonomous-frontmost':raise RuntimeError('window changed')
        return ops,bound,calls,{}
    def test_one_raise_set_and_actual_observation(self):
        ops,bound,calls,trace=self.fixture()
        helper.autonomous_focus(ops,bound,{},trace,sleep=lambda _:None)
        self.assertEqual(calls.count('raise'),1);self.assertEqual(calls.count('set'),1)
        self.assertTrue(trace['observations'][-1]['frontmost'])
    def test_failures_never_cycle_or_fallback(self):
        for case in ['unsupported','raise','set','window','frontmost','modal']:
            with self.subTest(case=case):
                ops,bound,calls,trace=self.fixture(case)
                if case=='frontmost':ops.front=lambda:False
                if case=='modal':ops.main=lambda expected:(_ for _ in ()).throw(RuntimeError('modal'))
                with self.assertRaises(RuntimeError):helper.autonomous_focus(ops,bound,{},trace,sleep=lambda _:None)
                self.assertLessEqual(calls.count('raise'),1);self.assertLessEqual(calls.count('set'),1)
                if case in ('unsupported','modal'):self.assertNotIn('raise',calls)
                if case in ('raise','window'):self.assertNotIn('set',calls)
    def test_already_foreground_has_no_raise_or_set(self):
        ops,bound,calls,trace=self.fixture();ops.front=lambda:True
        helper.autonomous_focus(ops,bound,{},trace)
        self.assertNotIn('raise',calls);self.assertNotIn('set',calls)
    def test_late_raise_keeps_rc_and_never_sets_frontmost(self):
        ops,bound,calls,trace=self.fixture()
        ops.check_time=lambda:(_ for _ in ()).throw(RuntimeError('late')) if 'raise' in calls else None
        with self.assertRaisesRegex(RuntimeError,'late'):helper.autonomous_focus(ops,bound,{},trace)
        self.assertEqual(trace['raise_rc'],0);self.assertNotIn('set',calls)

class AutonomousGateTests(unittest.TestCase):
    def fixture(self):
        calls=[];frame={'identity':{'pid':10},'window':{'window_id':20},'sha256':'a'*64}
        route=N(sequence=1,initial_binding=(frame['identity'],frame['window']))
        route.input=lambda action,before:calls.append(('helper',action,before)) or frame
        trace={'mechanism':'AXRaise+AXFrontmost','observations':[{'frontmost':True}]}
        b=N(screen_support=N(w=N(private_json=lambda *a:trace)))
        value={};admissions=N(value=value,check_birth=lambda *a:calls.append('birth'))
        p=NativePorts(b,'/invented',value,admissions,lambda event:(_ for _ in ()).throw(AssertionError('no owner event')),
                      lambda *a:(_ for _ in ()).throw(AssertionError('no completion')),clock=lambda:0)
        r=N(screen=N(window=route),root=Path('/invented/A'),ax=N(attr=lambda *a:True,app='app'),
            act_record=lambda name,value:calls.append(name))
        p.runs['A']=r;p.cleanup_original_main=lambda *a:calls.append('main-no-modal')
        p.owned_menu_quit=lambda *a,**kw:calls.append(('menu',kw['post']))
        return p,r,frame,calls,trace
    def test_actual_gate_needs_no_chat_receipt(self):
        p,r,f,c,t=self.fixture();self.assertEqual(p.autonomous_start('A',r,f,45),f)
        self.assertTrue(r.foreground_verified);self.assertIn(('menu',False),c)
        self.assertLess(c.index('main-no-modal'),c.index('autonomous-focus-verified.json'))
        with self.assertRaises(RuntimeError):p.autonomous_start('A',r,f,45)
    def test_false_focus_changed_window_and_modal_refuse_before_input(self):
        for case in ['trace','capture','modal','menu','focus']:
            p,r,f,c,t=self.fixture()
            def refuse(*a,**kw):raise RuntimeError('unsupported')
            if case=='trace':t['error']='failed raise'
            if case=='capture':r.screen.window.input=lambda *a:{**f,'window':{'window_id':99}}
            if case=='modal':p.cleanup_original_main=refuse
            if case=='menu':p.owned_menu_quit=refuse
            if case=='focus':r.ax.attr=lambda *a:False
            with self.subTest(case=case),self.assertRaises(RuntimeError):p.autonomous_start('A',r,f,45)
            self.assertFalse(r.foreground_verified)
            self.assertNotIn('autonomous-focus-verified.json',c)
    def test_early_focus_failure_cleanup_succeeds_without_foreground(self):
        from test_native_attended_ports import Tests
        r,c=Tests().run_fixture();p=Tests().ports(r)
        r.autonomous_owned_focus=True;r.foreground_verified=False
        self.assertTrue(p.quit_normal('A',295)['released']);self.assertIn('quit',c)
    def test_early_cleanup_refusal_notifies_owner_without_guessing_input(self):
        from test_native_attended_ports import Tests
        r,c=Tests().run_fixture();p=Tests().ports(r);reports=[];p.deliver=reports.append
        r.autonomous_owned_focus=True;r.foreground_verified=False
        p.cleanup_original_main=lambda *a:(_ for _ in ()).throw(RuntimeError('modal unknown'))
        with self.assertRaisesRegex(RuntimeError,'modal unknown'):p.quit_normal('A',295)
        self.assertNotIn('quit',c);self.assertNotIn('reap',c)
        self.assertEqual(reports[0]['event'],'owner-normal-quit-needed-now')

class NativeMainMappingTests(unittest.TestCase):
    def test_actual_mapping_rejects_foreign_window_modal_and_unknown_children(self):
        for case in ['ok','number','title','modal','child','self','extra']:
            with self.subTest(case=case):
                ops=helper.NativeFocus.__new__(helper.NativeFocus)
                ops.pid=10;ops.app='app';ops.check_time=lambda:None
                def number(main,out):out._obj.value=99 if case=='number' else 20;return 0
                ops.b=N(equal=lambda a,b:a==b,a=N(_AXUIElementGetWindow=number))
                def read(e,name):
                    refs=(['app'] if case=='self' else ['main','extra'] if case=='extra' else ['main']) if name=='AXWindows' else ['group']
                    return {'type':{'name':'CFArray'}},refs
                ops.read=read
                def scalar(e,name):
                    if name=='AXRole':return 'AXSheet' if case=='child' and e=='group' else ('AXGroup' if e=='group' else 'AXWindow')
                    if name=='AXTitle':return 'changed' if case=='title' else 'Original'
                    if name=='AXModal':return case=='modal'
                ops.scalar=scalar
                if case=='ok':self.assertEqual(ops.main({'window_id':20,'title':'Original'}),'main')
                else:
                    with self.assertRaises(RuntimeError):ops.main({'window_id':20,'title':'Original'})

class ActualHelperDecodeTests(unittest.TestCase):
    def test_actual_admission_decode_selects_only_explicit_autonomous_route(self):
        import json,os
        from test_native_b_window_helper import HelperTests
        for case in ['valid','wrong','failed']:
            fixture=HelperTests();fixture.setUp()
            try:
                admission=json.loads(fixture.admission.read_text())
                admission['inputs']['autonomous_focus_route']={'version':'autonomous-owned-focus/v1','per_incarnation_cap_seconds':45,'mechanism':'AXRaise+AXFrontmost'}
                if case=='wrong':admission['inputs']['autonomous_focus_route']['mechanism']='other'
                fixture.admission.write_text(json.dumps(admission));fixture.request['admission_sha256']=helper.w.sha(fixture.admission)
                fixture.backend.app=lambda pid:'app';fixture.backend.owner=lambda app:(0,123)
                calls=[]
                class Ops:
                    def __init__(self,*args):calls.append('construct')
                    def close(self):calls.append('close')
                def sequence(ops,bound,window,trace):
                    calls.append('sequence')
                    if case=='failed':raise RuntimeError('failed raise')
                    trace['observations']=[{'frontmost':True}]
                # The fixture uses an independently loaded copy of the real helper.
                import test_native_b_window_helper as module
                h=module.h
                with fixture.patches(),patch.object(h.w,'tools_identity',return_value={}),patch.object(h.w.d,'NativeBackend',return_value=fixture.backend),patch.object(h.w,'select_main',return_value=fixture.window),patch.object(h,'NativeFocus',Ops),patch.object(h,'autonomous_focus',side_effect=sequence),patch.object(h,'activate_original_app',side_effect=AssertionError('no AppKit fallback')):
                    if case=='valid':fixture.run_request(action='focus')
                    else:
                        with self.assertRaises(RuntimeError):fixture.run_request(action='focus')
                if case=='wrong':self.assertEqual(calls,[])
                else:
                    self.assertEqual(calls,['construct','sequence','close'])
                    trace=json.loads((fixture.root/'window-helper-001.focus.json').read_text())
                    self.assertEqual(trace['mechanism'],'AXRaise+AXFrontmost')
                    self.assertEqual('error' in trace,case=='failed')
                self.assertEqual((fixture.root/'window-helper-001.result.json').exists(),case=='valid')
            finally:fixture.doCleanups()

class NativeAdapterBudgetTests(unittest.TestCase):
    def test_actual_support_query_requires_settable(self):
        ops=helper.NativeFocus.__new__(helper.NativeFocus);ops.app='app';ops.check_time=lambda:None
        def actions(e,out):out._obj.value=1;return 0
        def settable(e,key,out):out._obj.value=False;return 0
        ops.b=N(a=N(AXUIElementCopyActionNames=actions,AXUIElementIsAttributeSettable=settable),held=[],
                string=lambda s:s,array=lambda *a:[2],scalar=lambda e:'AXRaise')
        self.assertFalse(ops.supports('main'));self.assertEqual(ops.b.held,[1])
    def test_real_budget_counts_actions_and_refuses_before_unsent_attempt(self):
        now=[0];trace={};calls=[]
        names=['AXUIElementCopyActionNames','AXUIElementIsAttributeSettable','AXUIElementSetAttributeValue',
               'AXUIElementPerformAction','_AXUIElementGetWindow','AXUIElementSetMessagingTimeout']
        a=N(**{name:(lambda *args:0) for name in names});p=N(proc_pidpath=lambda *a:0)
        b=N(a=a,p=p)
        ops=helper.NativeFocus(b,10,'app',trace,clock=lambda:now[0])
        try:
            self.assertEqual(b.a.AXUIElementPerformAction('main','raise'),0)
            self.assertTrue(trace['raise_attempted']);self.assertEqual(ops.calls,1)
            ops.calls=200
            with self.assertRaisesRegex(RuntimeError,'bound'):b.a.AXUIElementSetAttributeValue('app','front',True)
            self.assertNotIn('frontmost_attempted',trace)
        finally:ops.close()
        self.assertIs(b.a,a);self.assertIs(b.p,p);self.assertEqual(trace['native_calls'],200)
