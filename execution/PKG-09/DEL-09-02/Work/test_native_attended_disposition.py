import contextlib,io,os,tempfile
from pathlib import Path
from types import SimpleNamespace as N
import unittest
from native_attended_bridge import ReceiptBridge,delivery_receipt
from native_attended_disposition import offer,publish_disposition,consume

class Tests(unittest.TestCase):
    def fixture(self,root,observed):
        waits=[];records=[]
        reservation=N(reaped=False,lost=None,observe=lambda:dict(observed))
        reservation.child=N(pid=123,wait=lambda:waits.append(1) or (observed['status'] if observed['code']==os.CLD_EXITED else -observed['status']))
        run=N(reservation=reservation,extra_cleanup_ready=lambda:True,admission_sha='a'*64,
              act_record=lambda name,value:records.append((name,value)))
        ports=N(runs={'B':run},admissions=N(births={'B':{'pid':123,'ppid':456,'start_sec':1,'start_usec':2,'executable':'invented'}}))
        bridge=ReceiptBridge(root,'invented','run',N(receipts={}),simulation=True)
        selected=offer(ports,bridge,'B')
        with contextlib.redirect_stdout(io.StringIO()):event=bridge.emit({'event':'attended-terminal-disposition-needed','incarnation':'B','administrative_disposition_offer':selected})
        delivery_receipt(root,event,{'run_id':'run','event_id':event,'parent_thread':selected['issuer_thread'],
            'transport':'t3_thread_send','accepted':True,'message_id':'invented-delivery','simulation':True})
        return ports,bridge,event,waits,records
    def test_nonzero_and_signal_exact_original_wait_once(self):
        for observed in [{'code':os.CLD_EXITED,'status':7},{'code':os.CLD_KILLED,'status':9}]:
            with tempfile.TemporaryDirectory() as d:
                root=Path(d).resolve();root.chmod(0o700);(root/'bridge').mkdir(mode=0o700)
                ports,bridge,event,waits,records=self.fixture(root,observed)
                self.assertFalse(consume(ports,bridge,'B',event));self.assertFalse(waits)
                publish_disposition(root,event,'actual-parent-fixture-message')
                self.assertTrue(consume(ports,bridge,'B',event));self.assertEqual(waits,[1])
                self.assertFalse(consume(ports,bridge,'B',event));self.assertEqual(waits,[1])
                self.assertFalse(records[-1][1]['success']);self.assertFalse(records[-1][1]['all_resources_closed'])
    def test_changed_exit_or_unknown_helper_refuses_before_wait(self):
        for mutation in ['exit','helper','birth']:
            with tempfile.TemporaryDirectory() as d:
                root=Path(d).resolve();root.chmod(0o700);(root/'bridge').mkdir(mode=0o700)
                ports,bridge,event,waits,_=self.fixture(root,{'code':os.CLD_EXITED,'status':7})
                publish_disposition(root,event,'parent')
                if mutation=='exit':ports.runs['B'].reservation.observe=lambda:{'code':os.CLD_EXITED,'status':8}
                if mutation=='helper':ports.runs['B'].extra_cleanup_ready=lambda:False
                if mutation=='birth':ports.admissions.births['B']['start_sec']=10
                with self.assertRaises(RuntimeError):consume(ports,bridge,'B',event)
                self.assertFalse(waits)
