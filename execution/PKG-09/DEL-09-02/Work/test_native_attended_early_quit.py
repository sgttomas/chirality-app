"""Real early-menu traversal/intent/exit path, invented AX and original Child only."""
import json,tempfile
from pathlib import Path
from types import SimpleNamespace as N
from unittest.mock import patch
import unittest
from native_attended_ports import NativePorts
import native_b_window as w

class EarlyQuitTests(unittest.TestCase):
    def fixture(self,root,case='ok'):
        from test_native_attended_ports import Tests
        root=root.resolve()
        run,events=Tests().run_fixture();run.root=root;run.reservation.child=N(pid=10)
        run.ax=N(app='app',quit_ui=lambda:(_ for _ in ()).throw(AssertionError('no key Quit')))
        run.autonomous_owned_focus=True;run.foreground_verified=False
        run.setup_started=False;run.ordinary_input_attempted=False;run.stop_phase_started=False
        run.focus_helper_started=False;run.early_quit_consumed=False;run.quit_posted=False
        value={'bundle':'/invented/App.app','executable':'/invented/App','executable_sha256':'e'*64,'candidate_key':'invented'}
        path=root/'admission.json';path.write_text(json.dumps({'inputs':value}));path.chmod(0o600);run.admission_sha=w.sha(path)
        reads=[];births=[];presses=[];adapter_closed=[];app_reads=[0]
        if case=='latehelper':run.extra_cleanup_ready=lambda:app_reads[0]<2
        def birth(label,r):
            births.append(label)
            if case=='identity' and len(births)>2:raise RuntimeError('original identity changed')
        admissions=N(value=value,check_birth=birth,births={'A':{'pid':10,'birth':'original'}},
                     receipts={'A':{'admission_sha256':run.admission_sha}})
        b=Tests().ports(run).b;b.screen_support=N(w=w)
        p=NativePorts(b,root,value,admissions,lambda event:events.append(event),lambda *a:None,clock=lambda:0)
        p.runs['A']=run
        p.cleanup_original_main=lambda *a:(_ for _ in ()).throw(AssertionError('main AX must not be required'))
        def record(name,value):
            events.append(name)
            with (root/name).open('x') as f:json.dump(value,f)
        run.act_record=record
        class Adapter:
            app='app'
            def __init__(self,ax):pass
            def same(self,a,b):return a==b
            def timeout(self,e,t):return 0
            def owner(self,e):return 99 if case=='pid' and e=='quit' else 10
            def actions(self,e):return [] if case=='action' else ['AXPress']
            def read(self,e,key):
                reads.append((e,key))
                if (e,key)==('app','AXRole'):
                    app_reads[0]+=1
                    if case=='latestage' and app_reads[0]>1:run.setup_started=True
                target='replacement' if case=='target' and app_reads[0]>1 else 'quit'
                targets=[] if case=='missing' else [target,'duplicate'] if case=='ambiguous' else [target]
                rows={'app':{'AXRole':'AXApplication','AXTitle':'App','AXMenuBar':'bar','AXWindows':['app']},
                      'bar':{'AXRole':'AXMenuBar','AXChildren':['top']},
                      'top':{'AXRole':'AXMenuBarItem','AXTitle':'App','AXChildren':['menu']},
                      'menu':{'AXRole':'AXMenu','AXChildren':targets}}
                for item in ('quit','replacement','duplicate'):
                    rows[item]={'AXRole':'AXMenuItem','AXTitle':'Quit App','AXEnabled':case!='disabled'}
                if key in ('AXWindows','AXFrontmost'):raise AssertionError('no main/foreground prerequisite')
                return 0,rows[e][key]
            def press(self,e):
                self_intent=json.loads((root/'early-owned-menu-quit-intent.json').read_text())
                assert self_intent['admission_sha256']==run.admission_sha
                assert self_intent['modal_state'].startswith('UNKNOWN')
                presses.append(e)
                return -25204 if case=='uncertain' else 0
            def close(self):adapter_closed.append(True)
        return p,run,Adapter,events,reads,presses,adapter_closed
    def test_selfreference_early_recovery_uses_real_menu_and_normal_closure(self):
        with tempfile.TemporaryDirectory() as d:
            p,r,A,e,reads,presses,closed=self.fixture(Path(d))
            with patch('native_attended_ports.NativeAdapter',A):result=p.quit_normal('A',295)
            self.assertTrue(result['released']);self.assertEqual(presses,['quit']);self.assertEqual(closed,[True])
            self.assertFalse(any(k in ('AXWindows','AXFrontmost') for _,k in reads))
            self.assertIn('reap',e)
            self.assertEqual(json.loads((r.root/'early-owned-menu-quit-result.json').read_text())['return_code'],0)
    def test_actual_menu_refusals_never_press_or_reap(self):
        for case in ['pid','ambiguous','missing','disabled','action','identity','target','latestage','latehelper']:
            with self.subTest(case=case),tempfile.TemporaryDirectory() as d:
                p,r,A,e,reads,presses,closed=self.fixture(Path(d),case)
                with patch('native_attended_ports.NativeAdapter',A),self.assertRaises(RuntimeError):p.quit_normal('A',295)
                self.assertFalse(presses);self.assertNotIn('reap',e)
                self.assertTrue(r.early_quit_consumed)
    def test_ineligible_stage_or_helper_unknown_refuses_before_menu(self):
        for case in ['setup_started','ordinary_input_attempted','stop_phase_started','stop_requested','helpers','B','missing_stage']:
            with self.subTest(case=case),tempfile.TemporaryDirectory() as d:
                p,r,A,e,reads,presses,closed=self.fixture(Path(d));label='A'
                if case=='helpers':r.extra_cleanup_ready=lambda:False
                elif case=='B':p.runs['B']=r;label='B'
                elif case=='missing_stage':del r.setup_started
                else:setattr(r,case,True)
                with patch('native_attended_ports.NativeAdapter',A),self.assertRaises(RuntimeError):p.quit_normal(label,295)
                self.assertFalse(reads);self.assertFalse(presses);self.assertNotIn('reap',e)
    def test_uncertain_dispatch_is_consumed_and_never_repeated(self):
        with tempfile.TemporaryDirectory() as d:
            p,r,A,e,reads,presses,closed=self.fixture(Path(d),'uncertain')
            with patch('native_attended_ports.NativeAdapter',A):
                for _ in range(2):
                    with self.assertRaises(RuntimeError):p.quit_normal('A',295)
            self.assertEqual(presses,['quit']);self.assertNotIn('reap',e)
            self.assertEqual(json.loads((r.root/'early-owned-menu-quit-result.json').read_text())['return_code'],-25204)
    def test_focus_dispatch_or_unknown_trace_prevents_early_route(self):
        for case in ['no-actions','attempted','missing','intent']:
            with self.subTest(case=case),tempfile.TemporaryDirectory() as d:
                p,r,A,e,reads,presses,closed=self.fixture(Path(d));r.focus_helper_started=True;r.focus_helper_sequence=2
                if case!='missing':
                    trace=r.root/'window-helper-002.focus.json';trace.write_text(json.dumps({'mechanism':'AXRaise+AXFrontmost','raise_attempted':case=='attempted','frontmost_attempted':False}));trace.chmod(0o600)
                if case=='intent':(r.root/'window-helper-002.raise-intent.json').write_text('{}')
                with patch('native_attended_ports.NativeAdapter',A):
                    if case=='no-actions':self.assertTrue(p.quit_normal('A',295)['released'])
                    else:
                        with self.assertRaises((RuntimeError,FileNotFoundError)):p.quit_normal('A',295)
                        self.assertFalse(presses)

    def test_no_exit_after_successful_menu_request_never_reaps(self):
        with tempfile.TemporaryDirectory() as d:
            p,r,A,e,reads,presses,closed=self.fixture(Path(d));now=[0]
            p.clock=lambda:now[0];r.reservation.observe=lambda:None
            with patch('native_attended_ports.NativeAdapter',A),patch('native_attended_ports.time.sleep',side_effect=lambda _:now.__setitem__(0,296)):
                with self.assertRaisesRegex(RuntimeError,'exit unavailable'):p.quit_normal('A',295)
            self.assertEqual(presses,['quit']);self.assertNotIn('reap',e);self.assertNotIn('A',p.closures)

    def test_intent_sync_failure_prevents_press_and_consumes_attempt(self):
        with tempfile.TemporaryDirectory() as d:
            p,r,A,e,reads,presses,closed=self.fixture(Path(d))
            with patch('native_attended_ports.NativeAdapter',A),patch('native_attended_ports.os.fsync',side_effect=OSError('sync failed')):
                with self.assertRaises(OSError):p.quit_normal('A',295)
            self.assertFalse(presses);self.assertTrue(r.early_quit_consumed);self.assertNotIn('reap',e)
