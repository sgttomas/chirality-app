import copy
import unittest
from native_sheet_cancel import SheetCancel, Refusal

class AX:
    app='app'
    def __init__(self):
        self.props={'main':{'AXChildren':['sheet'],'AXMain':True},
            'app':{'AXFrontmost':True,'AXFocusedWindow':'sheet'},
            'sheet':{'AXRole':'AXSheet','AXParent':'main','AXModal':True,'AXChildren':['keep','stop','cancel']}}
        for e,t in [('keep','Keep Codex running'),('stop','Stop Codex'),('cancel','Cancel')]:
            self.props[e]={'AXRole':'AXButton','AXTitle':t,'AXEnabled':True,'AXParent':'sheet'}
        self.pressed=[];self.rc=0;self.pid=3;self.late=None
    def same(self,a,b):return a==b
    def timeout(self,e,t):return 0
    def owner(self,e):return self.pid
    def read(self,e,n):return (0,self.props[e][n]) if n in self.props.get(e,{}) else (-1,None)
    def number(self,e):return 1 if e=='main' else 2
    def actions(self,e):return ['AXPress']
    def press(self,e):
        self.pressed.append(e)
        if self.late:self.late()
        return self.rc

class Tests(unittest.TestCase):
    def setUp(self):
        self.ax=AX();self.now=0;self.facts=({'pid':3,'birth':4},{'window_id':1},{'window_id':2})
        self.records={};self.reports=[]
        def record(n,v):
            if n in self.records:raise RuntimeError('duplicate evidence')
            self.records[n]=copy.deepcopy(v)
        self.c=SheetCancel(self.ax,'main',3,lambda:copy.deepcopy(self.facts),record,self.reports.append,lambda:self.now,generation={'session':'B'},main_binding=lambda:{'window_id':1})
    def test_cancel_once_no_stop_or_effect_claim(self):
        self.c.observe(15);self.c.cancel(10)
        self.assertEqual(self.ax.pressed,['cancel']);self.assertFalse(self.records['sheet-cancel-posted']['effect_verified'])
        with self.assertRaises(Refusal):self.c.cancel(20)
    def test_independent_observation_failure_keeps_valid_cancel(self):
        self.c.observe(15);self.c.note_observation_failure('capture failed');self.c.cancel(10)
        self.assertEqual(self.ax.pressed,['cancel']);self.assertEqual(self.c.observation_failure,'capture failed')
    def test_changed_identity_parent_focus_cancel_refuse(self):
        for mutation in ['identity','parent','focus','title','disabled','duplicate']:
            with self.subTest(mutation=mutation):
                self.setUp();self.c.observe(15)
                if mutation=='identity':self.facts[0]['birth']=5
                if mutation=='parent':self.ax.props['sheet']['AXParent']='other'
                if mutation=='focus':self.ax.props['app']['AXFocusedWindow']='main'
                if mutation=='title':self.ax.props['cancel']['AXTitle']='Stop Codex'
                if mutation=='disabled':self.ax.props['cancel']['AXEnabled']=False
                if mutation=='duplicate':self.ax.props['keep']['AXTitle']='Cancel'
                with self.assertRaises(Refusal):self.c.cancel(10)
                self.assertEqual(self.ax.pressed,[])
    def test_unsupported_discovery_does_not_select_or_press(self):
        self.ax.props['main']['AXChildren']=['sheet','sheet2'];self.ax.props['sheet2']={'AXRole':'AXSheet'}
        with self.assertRaises(Refusal):self.c.observe(15)
        self.assertIsNone(self.c.selected);self.assertFalse(self.ax.pressed)
    def test_failed_evidence_never_dispatches(self):
        self.c.observe(15)
        self.c.record=lambda *args:(_ for _ in ()).throw(OSError('disk'))
        with self.assertRaises(OSError):self.c.cancel(10)
        self.assertFalse(self.ax.pressed)
    def test_late_or_uncertain_press_consumes_attempt(self):
        for late in [False,True]:
            self.setUp();self.c.observe(15)
            if late:self.ax.late=lambda:setattr(self,'now',11)
            else:self.ax.rc=-1
            with self.assertRaises(Refusal):self.c.cancel(10)
            with self.assertRaises(Refusal):self.c.cancel(30)
            self.assertEqual(self.ax.pressed,['cancel'])
    def test_native_call_and_cumulative_caps(self):
        with self.assertRaises(Refusal):self.c.observe(15,cap=2)
        self.setUp();self.c.observe(15);self.now=10
        with self.assertRaises(Refusal):self.c.cancel(10)
        self.assertFalse(self.ax.pressed)
    def test_fallback_delivered_immediately_with_custody(self):
        self.c.unsupported('AXParent unavailable','fixed end')
        self.assertEqual(self.reports[0]['event'],'owner-cancel-needed-now')
        self.assertIn('keeper retained',self.reports[0]['custody'])

    def test_preflight_refuses_existing_sheet(self):
        with self.assertRaises(Refusal):self.c.preflight(10)
        self.assertFalse(self.ax.pressed)
    def proof(self):return {'generation':{'session':'B'},'state':'ready','stop_enabled':True,
        'sheet_row_absent':True,'source_gate_passed':True,'stopping_rows':[],'LT23_rows':[]}
    def detach(self):
        self.ax.props['main']['AXChildren']=[];self.ax.props['app']['AXFocusedWindow']='main'
    def test_dismissal_requires_both_hierarchy_and_fresh_source(self):
        self.c.observe(15);self.c.cancel(10)
        with self.assertRaises(Refusal):self.c.dismissed(15,lambda _: self.proof())
        self.setUp();self.c.observe(15);self.c.cancel(10);self.detach()
        with self.assertRaises(Refusal):self.c.dismissed(15,lambda _: {'state':'stopping'})
        self.assertNotIn('sheet-dismissed',self.records)
    def test_valid_dismissal_and_uncertain_actor(self):
        self.c.observe(15);self.ax.rc=-25204
        with self.assertRaises(Refusal):self.c.cancel(10)
        self.c.unsupported('uncertain','fixed');self.detach()
        self.c.dismissed(15,lambda _:self.proof())
        self.assertEqual(self.records['sheet-dismissed']['actor'],'undetermined')
    def test_discovery_failure_is_single_shot(self):
        self.ax.props['main']['AXChildren']=[]
        with self.assertRaises(Refusal):self.c.observe(15)
        count=self.c.total_calls
        with self.assertRaises(Refusal):self.c.observe(15)
        self.assertEqual(count,self.c.total_calls)
    def test_cancel_only_sheet_is_not_Stop(self):
        self.ax.props['sheet']['AXChildren']=['cancel']
        with self.assertRaises(Refusal):self.c.observe(15)
        self.assertFalse(self.ax.pressed)
    def test_late_press_still_retains_return_code(self):
        self.c.observe(15);self.ax.late=lambda:setattr(self,'now',11)
        with self.assertRaises(Refusal):self.c.cancel(10)
        self.assertEqual(self.records['sheet-cancel-posted']['return_code'],0)
        self.assertTrue(self.records['sheet-cancel-posted']['late'])
    def test_max_admitted_layout_fits_count(self):
        self.ax.props['main']['AXChildren']=['sheet']+['g'+str(i) for i in range(4)]
        for i in range(4):self.ax.props['g'+str(i)]={'AXRole':'AXGroup'}
        self.ax.props['sheet']['AXChildren'] += ['icon','text','text2']
        for e in ['icon','text','text2']:self.ax.props[e]={'AXRole':'AXStaticText'}
        self.c.observe(15);self.assertLessEqual(self.c.calls,60)
        self.c.cancel(10);self.assertLessEqual(self.c.calls,46)
    def test_wrong_preflight_main_refuses(self):
        self.c.main_binding=lambda:{'window_id':999}
        with self.assertRaises(Refusal):self.c.preflight(10)

    def test_owner_completion_without_selected_sheet_requires_inventory_and_source(self):
        self.c.unsupported('no sheet binding','end');self.c.record_owner_completion('Cancelled');self.detach()
        proof=self.proof();proof['no_new_owned_windows']=True
        self.c.dismissed(15,lambda _:proof)
        self.assertEqual(self.records['sheet-dismissed']['actor'],'owner-reported-and-verified')
