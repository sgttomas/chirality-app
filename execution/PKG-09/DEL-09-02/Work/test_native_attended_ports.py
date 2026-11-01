import tempfile
from pathlib import Path
from types import SimpleNamespace as N
from unittest.mock import patch
import unittest
from native_attended_ports import NativePorts

class Tests(unittest.TestCase):
    def ports(self,run):
        value={};a=N(check_birth=lambda label,r:None,value=value)
        b=N(release_support=N(normal_exit=lambda x:x=={'code':1,'status':0},
              request_for=lambda r:{'expected_app_exit':{'code':1,'status':0},'admission':r.admission_sha}))
        p=NativePorts(b,'/invented',value,a,lambda event:None,lambda label,end:'Cancelled',clock=lambda:0)
        p.owned_menu_quit=lambda run,end:run.ax.quit_ui()
        p.runs['A']=run
        return p
    def run_fixture(self):
        events=[]
        run=N(cleanup=False,ui_deadline=0,quit_requested=False,stop_requested=False,admission_sha='a'*64,root=Path('/invented/A'),
            extra_cleanup_ready=lambda:True,bound_main=lambda:events.append('bound'),
            ax=N(quit_ui=lambda:events.append('quit')),act_record=lambda n,v:events.append(n),
            reservation=N(observe=lambda:{'code':1,'status':0},administrative_reap=lambda e:events.append('reap') or 0,reaped=False),
            stop=N(set=lambda:events.append('stop-monitor')),thread=N(join=lambda timeout:None,is_alive=lambda:False))
        return run,events
    def test_quit_original_normal_exit_then_fresh_reap_only(self):
        run,events=self.run_fixture();p=self.ports(run)
        r=p.quit_normal('A',20)
        self.assertEqual(events[:2],['bound','quit']);self.assertLess(events.index('attended-admin-release-intent.json'),events.index('reap'))
        self.assertTrue(r['reaped']);self.assertEqual(r['supplier_settlement'],'not claimed')
        with self.assertRaises(RuntimeError):p.quit_normal('A',20)
    def test_unknown_helper_refuses_before_any_Quit(self):
        run,events=self.run_fixture();run.extra_cleanup_ready=lambda:False;p=self.ports(run)
        with self.assertRaises(RuntimeError):p.quit_normal('A',20)
        self.assertFalse(events)
    def test_nonzero_exit_never_reaped(self):
        run,events=self.run_fixture();run.reservation.observe=lambda:{'code':1,'status':1};p=self.ports(run)
        with self.assertRaises(RuntimeError):p.quit_normal('A',20)
        self.assertNotIn('reap',events)
    def test_unknown_guard_blocks_closure_receipt(self):
        run,events=self.run_fixture();run.thread.is_alive=lambda:True;p=self.ports(run)
        with self.assertRaises(RuntimeError):p.quit_normal('A',20)
        self.assertNotIn('A',p.closures)
    def test_Quit_never_affirms_pending_B_sheet(self):
        run,events=self.run_fixture();run.stop_requested=True;p=self.ports(run);p.runs['B']=run
        with self.assertRaises(RuntimeError):p.quit_normal('B',20)
        self.assertFalse(events)
