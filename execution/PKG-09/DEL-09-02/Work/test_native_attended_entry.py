"""Full offline entry/supervision exercise. No NativePorts, Child or native API."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace as N
import unittest

from native_attended_entry import run_sequence,original_custody
from native_attended_bridge import ReceiptBridge,publish,read,delivery_receipt,owner_completion
from test_native_attended_sequence import Ports

class SimulatedPorts(Ports):
    def __init__(self,root,bridge):
        super().__init__();self.root=root;self.bridge=bridge;self.runs={};self.pending_launch=None
        self.late_exit=False;self.messages=[]
        self.admissions=N(births={})
        self.b=N(release_support=N(normal_exit=lambda value:value=={'code':1,'status':0},
                request_for=lambda run:{'expected_app_exit':{'code':1,'status':0},'simulation':True}))
    def record(self,name,value):
        self.records[name]=dict(value);publish(self.root/(name+'.json'),dict(value,simulation=True))
    def launch(self,label,admission,end):
        self.pending_launch=label;value=super().launch(label,admission,end)
        reservation=N(reaped=False,exited=False,lost=None,status=0)
        reservation.child=N(pid=100+len(self.runs),wait=lambda:reservation.status)
        reservation.observe=lambda: {'code':1,'status':reservation.status} if reservation.exited else None
        def reap(expected):reservation.reaped=True;return 0
        reservation.administrative_reap=reap
        run=N(admission_sha=label.lower()*64,sample=lambda:None,observed_processes=[],reservation=reservation,thread=N(is_alive=lambda:not reservation.reaped),
              extra_cleanup_ready=lambda:True,stop=N(set=lambda:None),
              act_record=lambda name,value:self.record(label+'-'+name,value),safe_log=lambda *a,**k:None)
        self.runs[label]=run;self.pending_launch=None
        self.admissions.births[label]={'pid':reservation.child.pid,'ppid':1,'start_sec':len(self.runs),'start_usec':0,'executable':'invented'}
        self.bridge.admissions.receipts[label]={'admission_sha256':label.lower()*64}
        return value
    def quit_normal(self,label,end):
        value=super().quit_normal(label,end)
        self.runs[label].reservation.exited=True;self.runs[label].reservation.reaped=True
        return value
    def owner_cancel_now(self,label,reason,end,attempted):
        self.reports.append((label,reason));self.bridge.deliver({'event':'owner-cancel-needed-now',
            'incarnation':label,'fixed_end':end,'reason':reason,'cancel_attempted':attempted})
    def wait_owner_completion(self,label,end):return self.bridge.completion(label,end)
    def record_owner_completion(self,label,value):self.messages.append((label,value))
    def retain_and_report(self,label,end,**kwargs):self.events.append('held')

class EntryTests(unittest.TestCase):
    def exercise(self,mode):
        with tempfile.TemporaryDirectory(prefix='attended-simulation-') as directory:
            root=Path(directory).resolve();root.chmod(0o700);(root/'bridge').mkdir(mode=0o700)
            now=[0];handled=set();clock=lambda:now[0]
            bridge=ReceiptBridge(root,'invented-candidate','invented-run',N(receipts={}),clock=clock,simulation=True)
            ports=SimulatedPorts(root,bridge)
            def tick(delay):
                now[0]+=delay;ports.now=now[0]
                for event in sorted((root/'bridge').glob('*.event.json')):
                    value=read(event);event_id=value['event_id']
                    if event_id in handled:continue
                    handled.add(event_id)
                    accepted=mode!='delivery-failure'
                    delivery_receipt(root,event_id,{'run_id':'invented-run','event_id':event_id,
                        'parent_thread':value['parent_thread'],'transport':'t3_thread_send',
                        'message_id':'invented-tool-result','accepted':accepted,'simulation':True})
                    if accepted and 'administrative_disposition_offer' in value:
                        from native_attended_disposition import publish_disposition
                        publish_disposition(root,event_id,'invented-Agent0-explicit-disposition')
                    if accepted and 'completion_offer' in value and (mode!='late-owner' or value['completion_offer']['action']=='owner-foreground-completed'):
                        owner_completion(root,event_id,value['completion_offer']['actual_owner_reply'],'invented-owner-message')
                if mode=='nonzero-exit':
                    ports.runs['B'].reservation.status=7;ports.runs['B'].reservation.exited=True
                if mode in ('delivery-failure','late-owner') and now[0]>295:
                    if mode=='late-owner':
                        for label,offer in bridge.offers.items():
                            path=root/'bridge'/(offer['event_id']+'.completion.json')
                            if not path.exists():owner_completion(root,offer['event_id'],'Cancelled','invented-late-owner-message')
                    for run in ports.runs.values():run.reservation.exited=True
                if now[0]>310:raise AssertionError('offline supervision failed to close within fixture')
            bridge.sleep=tick
            if mode=='autonomous-flow':
                from test_native_attended_autonomous import AutonomousGateTests
                original_setup,original_ready=ports.ordinary_setup_save,ports.observe_ready
                def gate(label):
                    native,run,frame,events,_=AutonomousGateTests().fixture()
                    native.runs={label:run};native.clock=clock
                    native.deliver=bridge.deliver;native.owner_completion=bridge.completion
                    run.act_record=lambda name,value:ports.record(label+'-'+name,value)
                    native.autonomous_start(label,run,frame,min(clock()+45,160))
                def setup(label,end):gate(label);return original_setup(label,end)
                def ready(label,end):gate(label);return original_ready(label,end)
                ports.ordinary_setup_save=setup;ports.observe_ready=ready
            if mode=='nonzero-exit':ports.fail='quitB'
            elif mode not in ('normal','autonomous-flow'):ports.fail='discover'
            with contextlib.redirect_stdout(io.StringIO()) as output:
                result=run_sequence(ports,bridge,0,clock=clock,sleep=tick)
            self.assertFalse(original_custody(ports));self.assertFalse(result['qualification_success'])
            self.assertFalse(result['Stop_confirmed']);self.assertFalse(result['LT23_observed'])
            self.assertTrue(result['resource_custody_closed'])
            self.assertTrue((root/'attended-resource-closure.json').exists())
            if mode in ('normal','autonomous-flow'):
                self.assertTrue(result['witness_complete'])
                if mode=='autonomous-flow':self.assertEqual(bridge.offers,{})
            else:
                self.assertFalse(result['witness_complete']);self.assertEqual(len(ports.reports),0 if mode=='nonzero-exit' else 1)
                self.assertIn('attended-manager-forward',output.getvalue())
            if mode in ('delivery-failure','late-owner'):self.assertGreater(result['final_overrun'],0)
            return result
    def test_complete_two_incarnation_entrypoint(self):self.exercise('normal')
    def test_both_autonomous_gates_run_without_owner_completion(self):self.exercise('autonomous-flow')
    def test_actual_completion_ingress_simulated_without_native_actions(self):self.exercise('owner')
    def test_transport_failure_keeps_custody_until_observed_exit(self):self.exercise('delivery-failure')
    def test_late_owner_completion_records_overrun_without_rearming(self):self.exercise('late-owner')
    def test_nonzero_original_exit_waits_for_explicit_disposition(self):self.exercise('nonzero-exit')

class BridgeFailureTests(unittest.TestCase):
    def test_flushed_event_is_not_delivery(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d).resolve();root.chmod(0o700);(root/'bridge').mkdir(mode=0o700)
            now=[0]
            bridge=ReceiptBridge(root,'invented','run',N(receipts={}),clock=lambda:now[0],sleep=lambda delta:now.__setitem__(0,now[0]+delta),simulation=True)
            with contextlib.redirect_stdout(io.StringIO()),self.assertRaisesRegex(RuntimeError,'not acknowledged'):
                bridge.deliver({'event':'custody-held','fixed_end':295})
            self.assertTrue((root/'bridge/0001.event.json').exists())
            self.assertFalse((root/'bridge/0001.delivery.json').exists())
    def test_completion_before_delivery_and_partial_receipt_refuse(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d).resolve();root.chmod(0o700);(root/'bridge').mkdir(mode=0o700)
            bridge=ReceiptBridge(root,'invented','run',N(receipts={'B':{'admission_sha256':'a'*64}}),simulation=True)
            with contextlib.redirect_stdout(io.StringIO()):event_id=bridge.emit({'event':'owner-cancel-needed-now','incarnation':'B'})
            with self.assertRaises(FileNotFoundError):owner_completion(root,event_id,'Cancelled','invented-message')
            path=root/'bridge'/('0001.delivery.json');path.write_text('');path.chmod(0o600)
            with self.assertRaises(RuntimeError):owner_completion(root,event_id,'Cancelled','invented-message')
    def test_transport_receipt_cannot_replace_an_existing_receipt(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d).resolve();root.chmod(0o700)
            path=root/'receipt.json';publish(path,{'first':True})
            with self.assertRaises(RuntimeError):publish(path,{'first':False})
            self.assertEqual(read(path),{'first':True})

class LateTransportTests(unittest.TestCase):
    def test_after_deadline_notice_has_transport_only_allowance(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d).resolve();root.chmod(0o700);(root/'bridge').mkdir(mode=0o700)
            now=[300];count=[0]
            def tick(delay):
                now[0]+=delay;count[0]+=1
                event=read(root/'bridge/0001.event.json')
                delivery_receipt(root,'0001',{'run_id':'run','event_id':'0001','parent_thread':event['parent_thread'],
                    'transport':'t3_thread_send','accepted':True,'message_id':'invented','simulation':True})
            bridge=ReceiptBridge(root,'invented','run',N(receipts={}),clock=lambda:now[0],sleep=tick,simulation=True)
            with contextlib.redirect_stdout(io.StringIO()):bridge.deliver({'event':'custody-held','fixed_end':295})
            self.assertEqual(count[0],1);self.assertGreater(now[0],295)

class PublicationFailureTests(unittest.TestCase):
    def test_temp_creation_failure_does_not_leave_publication_lock_held(self):
        from unittest.mock import patch
        import os
        with tempfile.TemporaryDirectory() as d:
            root=Path(d).resolve();root.chmod(0o700);path=root/'receipt.json'
            original=os.open
            def fail_temp(name,*args,**kwargs):
                if Path(name).name.startswith('.receipt.json.'):raise OSError('invented disk failure')
                return original(name,*args,**kwargs)
            with patch('native_attended_bridge.os.open',side_effect=fail_temp),self.assertRaises(OSError):publish(path,{'first':True})
            publish(path,{'second':True});self.assertEqual(read(path),{'second':True})
