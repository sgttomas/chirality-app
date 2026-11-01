import unittest
from native_attended_sequence import AttendedSequence, Refusal

class Ports:
    def __init__(self):self.events=[];self.now=0;self.fail=None;self.slow=None;self.reports=[];self.records={};self.quits=[]
    def event(self,name):
        self.events.append(name)
        if self.slow==name:self.now=161
        if self.fail==name:raise Refusal(name)
    def record(self,n,v):self.records[n]=dict(v)
    def admit_empty_namespace(self,end):self.event('admitA');return {'admission_id':'a'}
    def launch(self,label,a,end):self.event('launch'+label);return label
    def ordinary_setup_save(self,a,end):self.event('setup');return {'performed_through_native_ui':True,'applies_next_launch_only':True,'incarnation':a,'generation':None}
    def quit_normal(self,i,end):
        self.quits.append(i);self.event('quit'+i)
        return {'incarnation':i,'normal_exit':0,'helpers_settled':True,'reaped':True,'released':True,'release_id':i+'-release','helper_custody_id':i+'-helpers'}
    def readmit_saved_state(self,a,s,c,end):self.event('readmit');return {'admission_id':'b','fresh_after_closure':True,'a_release_id':c['release_id']}
    def observe_ready(self,b,end):
        self.event('ready');return {'incarnation':b,'full_source_gate':True,'ready':True,'zero_observed_work':True,'generation':{'appSession':'B','home':'invented','spawnCounter':1}}
    def sheet_preflight(self,*args):self.event('preflight')
    def post_stop_once(self,*args):self.event('Stop')
    def discover_cancel(self,*args):self.event('discover');return {'exact':'cancel'}
    def observe_question_if_budget(self,*args):self.event('question')
    def cancel_once(self,*args):self.event('Cancel')
    def owner_cancel_now(self,*args):self.events.append('owner-needed');self.reports.append(args)
    def verify_dismissal_and_source(self,b,ready,end):self.event('dismiss');return {'incarnation':b,'same_source':True,'ready':True,'sheet_absent':True}
    def retain_and_report(self,*args):self.events.append('held')

class Tests(unittest.TestCase):
    def run_case(self,fail=None,slow=None):
        p=Ports();p.fail=fail;p.slow=slow;r=AttendedSequence(p,lambda:p.now);return p,r,r.run(0)
    def test_complete_two_incarnations_one_cancel_never_qualification(self):
        p,r,out=self.run_case();self.assertTrue(out['witness_complete']);self.assertFalse(out['qualification_success'])
        self.assertFalse(out['Stop_confirmed']);self.assertFalse(out['LT23_observed'])
        self.assertLess(p.events.index('quitA'),p.events.index('readmit'));self.assertLess(p.events.index('readmit'),p.events.index('launchB'))
        self.assertEqual(p.events.count('Stop'),1);self.assertEqual(p.events.count('Cancel'),1)
        with self.assertRaises(Refusal):r.run(0)
    def test_first_closure_failure_blocks_second_launch(self):
        p,r,out=self.run_case(fail='quitA');self.assertNotIn('launchB',p.events);self.assertTrue(out['custody_held']);self.assertEqual(p.quits,['A'])
    def test_fresh_admission_failure_has_no_second_launch_or_retry(self):
        p,r,out=self.run_case(fail='readmit');self.assertEqual(p.quits,['A']);self.assertNotIn('launchB',p.events)
    def test_cutoff_after_setup_closes_A_and_never_launches_B(self):
        p,r,out=self.run_case(slow='setup');self.assertEqual(p.quits,['A']);self.assertNotIn('launchB',p.events)
    def test_cutoff_at_ready_closes_B_without_Stop(self):
        p,r,out=self.run_case(slow='ready');self.assertEqual(p.quits,['A','B']);self.assertNotIn('Stop',p.events)
    def test_failed_image_preserves_cancel_but_not_witness_success(self):
        p,r,out=self.run_case(fail='question');self.assertIn('Cancel',p.events);self.assertFalse(out['witness_complete']);self.assertFalse(p.reports)
    def test_unknown_binding_reports_before_readback_without_agent_cancel(self):
        p,r,out=self.run_case(fail='discover');self.assertNotIn('Cancel',p.events)
        self.assertLess(p.events.index('owner-needed'),p.events.index('dismiss'))
    def test_ambiguous_cancel_never_repeated(self):
        p,r,out=self.run_case(fail='Cancel');self.assertEqual(p.events.count('Cancel'),1);self.assertEqual(p.quits,['A','B'])
    def test_dismissal_failure_retains_custody_no_Quit(self):
        p,r,out=self.run_case(fail='dismiss');self.assertEqual(p.quits,['A']);self.assertTrue(out['custody_held'])
    def test_reused_child_and_generation_refuse(self):
        p=Ports();old=p.launch
        p.launch=lambda label,a,end: old('A',a,end)
        out=AttendedSequence(p,lambda:p.now).run(0);self.assertFalse(out['witness_complete']);self.assertNotIn('Stop',p.events)
