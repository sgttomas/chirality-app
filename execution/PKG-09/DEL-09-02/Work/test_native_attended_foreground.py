"""Owner handoff→read-only gates→capture order; no native APIs or activation."""
import contextlib,io,tempfile
from pathlib import Path
from types import SimpleNamespace as N
import unittest
from native_attended_ports import NativePorts
from native_attended_bridge import ReceiptBridge,delivery_receipt,owner_completion,publish

class GateTests(unittest.TestCase):
    def fixture(self):
        events=[];now=[0];frame={'identity':{'pid':10},'window':{'window_id':20},'path':'/invented/image.png','sha256':'a'*64}
        route=N(initial_binding=(frame['identity'],frame['window']),capture=lambda **kw:events.append('capture') or dict(frame))
        run=N(screen=N(window=route),foreground_verified=False,activation_spent=True,resource_end=295,
              ax=N(app='app',attr=lambda e,k:events.append('read-frontmost') or True),
              act_record=lambda name,value:events.append(name),safe_log=lambda *a,**k:None)
        value={'bundle':'/invented/Exact App.app'};admissions=N(value=value,check_birth=lambda *args:events.append('birth'))
        def deliver(event):events.append(event['event'])
        def completion(label,end,kind):events.append('actual-completion');return 'Foreground'
        ports=NativePorts(N(),'/invented',value,admissions,deliver,completion,clock=lambda:now[0]);ports.runs['A']=run
        ports.cleanup_original_main=lambda run,end:events.append('distinct-main-no-modal')
        ports.owned_menu_quit=lambda run,end,post=True:events.append('menu-read-only' if not post else 'BAD-PRESS')
        return ports,run,frame,events,now
    def test_delivery_and_actual_completion_precede_all_preflight_no_input(self):
        p,r,frame,events,now=self.fixture()
        self.assertEqual(p.foreground_start('A',r,frame,30),frame)
        self.assertTrue(r.foreground_verified)
        self.assertLess(events.index('owner-foreground-needed-now'),events.index('actual-completion'))
        self.assertLess(events.index('actual-completion'),events.index('read-frontmost'))
        self.assertLess(events.index('menu-read-only'),events.index('capture'))
        self.assertNotIn('BAD-PRESS',events)
        with self.assertRaises(RuntimeError):p.foreground_start('A',r,frame,60)
    def test_no_completion_wrong_reply_or_false_frontmost_has_no_input(self):
        for case in ['missing','wrong','frontmost','main','menu','late']:
            with self.subTest(case=case):
                p,r,frame,events,now=self.fixture()
                def fail(*args,**kwargs):raise RuntimeError(case)
                if case=='missing':p.owner_completion=fail
                if case=='wrong':p.owner_completion=lambda *args:'Cancelled'
                if case=='frontmost':r.ax.attr=lambda *args:False
                if case=='main':p.cleanup_original_main=fail
                if case=='menu':p.owned_menu_quit=fail
                if case=='late':p.owner_completion=lambda *args:now.__setitem__(0,19) or 'Foreground'
                with self.assertRaises(RuntimeError):p.foreground_start('A',r,frame,30)
                self.assertFalse(r.foreground_verified);self.assertNotIn('capture',events);self.assertNotIn('BAD-PRESS',events)
                self.assertEqual(events.count('owner-normal-quit-needed-now'),1)
    def test_delivery_failure_does_not_count_as_owner_completion(self):
        p,r,frame,events,now=self.fixture()
        def fail(event):events.append(event['event']);raise RuntimeError('delivery failed')
        p.deliver=fail
        with self.assertRaises(RuntimeError):p.foreground_start('A',r,frame,30)
        self.assertNotIn('actual-completion',events);self.assertNotIn('capture',events)
    def test_both_incarnations_get_distinct_foreground_gate(self):
        p,a,frame,events,now=self.fixture();_,b,_,_,_=self.fixture();p.runs['B']=b
        p.foreground_start('A',a,frame,30);p.foreground_start('B',b,frame,30)
        self.assertEqual(events.count('owner-foreground-needed-now'),2)

    def test_cutoff_before_handoff_requests_only_normal_quit(self):
        p,r,frame,events,now=self.fixture();now[0]=145
        with self.assertRaises(RuntimeError):p.foreground_start('A',r,frame,160)
        self.assertNotIn('owner-foreground-needed-now',events)
        self.assertNotIn('actual-completion',events);self.assertNotIn('capture',events)
        self.assertEqual(events.count('owner-normal-quit-needed-now'),1)

class ReceiptTests(unittest.TestCase):
    def test_actual_foreground_offer_and_cancel_are_distinct_and_once_only(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d).resolve();root.chmod(0o700);(root/'bridge').mkdir(mode=0o700)
            bridge=ReceiptBridge(root,'invented','run',N(receipts={'B':{'admission_sha256':'b'*64}}),clock=lambda:0,simulation=True)
            with contextlib.redirect_stdout(io.StringIO()):event=bridge.emit({'event':'owner-foreground-needed-now','incarnation':'B'})
            delivery_receipt(root,event,{'run_id':'run','event_id':event,'parent_thread':'0f35714c-46fb-45d8-9c97-c927c6587c1e',
                'transport':'t3_thread_send','accepted':True,'message_id':'invented-delivery','simulation':True})
            with self.assertRaises(RuntimeError):owner_completion(root,event,'Cancelled','invented-owner')
            owner_completion(root,event,'Foreground','invented-owner')
            self.assertEqual(bridge.completion('B',10,'foreground'),'Foreground')
            with self.assertRaises(RuntimeError):bridge.completion('B',10,'foreground')
            with contextlib.redirect_stdout(io.StringIO()):bridge.emit({'event':'owner-cancel-needed-now','incarnation':'B'})
            self.assertEqual(bridge.offers['B']['actual_owner_reply'],'Cancelled')

class EarlyQuitTests(unittest.TestCase):
    def test_failed_foreground_never_uses_agent_menu_input(self):
        from test_native_attended_ports import Tests as Existing
        run,events=Existing().run_fixture();ports=Existing().ports(run)
        ports.value['bundle']='/invented/Exact App.app';reports=[];ports.deliver=reports.append
        run.attended_owner_foreground=True;run.foreground_verified=False;run.resource_end=295
        for _ in range(2):
            with self.assertRaisesRegex(RuntimeError,'owner normal Quit requested'):ports.quit_normal('A',295)
        self.assertEqual(len(reports),1);self.assertEqual(reports[0]['event'],'owner-normal-quit-needed-now')
        self.assertFalse(events);self.assertFalse(run.quit_requested)
