"""Initial acquisition policy fixtures; no native API, capture or UI action."""
import copy,importlib.util,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock,patch
spec=importlib.util.spec_from_file_location('initial_window_tests',Path(__file__).with_name('native_b_window.py'));w=importlib.util.module_from_spec(spec);spec.loader.exec_module(w)
class Stability(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(dir='/Users/ryan/dev/chirality-t3/scratch',prefix='initial-window-fixture-');self.addCleanup(self.tmp.cleanup)
  self.root=Path(self.tmp.name).resolve();self.clock=100.;self.records={}
  self.run=SimpleNamespace(root=self.root,alive=Mock(),work_end=280.,cleanup_end=395.,ui_deadline=115.,record=lambda name,value:self.records.setdefault(name,copy.deepcopy(value)),report=Mock())
  self.route=w.WindowRoute(self.run);self.identity={'pid':123,'ppid':99,'start_sec':1,'start_usec':2,'executable':'fixture'}
  self.window={'window_id':42,'title':w.TITLE,'bounds':{'X':106.,'Y':32.,'Width':1100.,'Height':800.},'on_screen':True,'layer':0.,'own_visible_layer0_count':1}
  self.backend=SimpleNamespace(screen_access=lambda:True,close=Mock())
  self.addCleanup(patch.stopall)
  patch.object(w.time,'monotonic',side_effect=lambda:self.clock).start();patch.object(w.time,'sleep',side_effect=self.advance).start()
  self.native=patch.object(w.d,'NativeBackend',return_value=self.backend).start()
  self.identity_reader=patch.object(w.d,'bound_identity',return_value=self.identity).start()
  self.selection=patch.object(w,'select_main',return_value=self.window).start()
 def advance(self,n):self.clock+=n
 def test_geometry_evolves_then_three_complete_samples_match(self):
  changed={**self.window,'bounds':{**self.window['bounds'],'X':105.,'Width':1102.}}
  self.selection.side_effect=[self.window,changed,changed,changed]
  self.assertEqual(self.route.acquire_initial_window(),(self.identity,changed))
  self.assertEqual(self.clock,100.75);self.assertEqual(self.route.sequence,0)
  result=self.records['initial-window-stable.json'];self.assertEqual(result['consecutive_matches'],3)
  self.assertEqual([self.records[f'initial-window-sample-{n:02d}.json']['monotonic'] for n in range(1,5)],[100.,100.25,100.5,100.75])
  self.assertEqual(self.identity_reader.call_count,8)
 def test_absence_before_selection_waits_but_disappearance_after_selection_refuses(self):
  self.selection.side_effect=[w.WindowUnavailable('none'),self.window,self.window,self.window]
  self.route.acquire_initial_window();self.assertIsNone(self.records['initial-window-sample-01.json']['window'])
  self.route=w.WindowRoute(self.run);self.selection.side_effect=[self.window,w.WindowUnavailable('gone')]
  with self.assertRaisesRegex(RuntimeError,'disappeared'):self.route.acquire_initial_window()
 def test_never_stable_refuses_inside_fixed_three_seconds(self):
  self.selection.side_effect=lambda *a:{**self.window,'bounds':{**self.window['bounds'],'X':self.clock}}
  with self.assertRaisesRegex(RuntimeError,'budget'):self.route.acquire_initial_window()
  self.assertLessEqual(self.clock,103.);self.assertIsNone(self.route.initial_binding)
  with self.assertRaisesRegex(RuntimeError,'unavailable after'):self.route.acquire_initial_window()
 def test_changed_incarnation_or_owner_refuses_before_admission(self):
  for field in ('pid','start_usec','executable'):
   self.route=w.WindowRoute(self.run);self.identity_reader.side_effect=[self.identity,{**self.identity,field:'changed'}]
   with self.assertRaisesRegex(RuntimeError,'App identity changed'):self.route.acquire_initial_window()
   self.assertIsNone(self.route.initial_binding)
 def test_changed_window_identity_or_nongeometry_fact_refuses(self):
  for key,value in (('window_id',99),('title','different'),('layer',8),('on_screen',False),('own_visible_layer0_count',2)):
   self.route=w.WindowRoute(self.run);self.selection.side_effect=[self.window,{**self.window,key:value}]
   with self.assertRaisesRegex(RuntimeError,'no replacement'):self.route.acquire_initial_window()
 def test_ambiguous_selection_never_retries(self):
  self.selection.side_effect=RuntimeError('exact owned visible main window ambiguous')
  with self.assertRaisesRegex(RuntimeError,'ambiguous'):self.route.acquire_initial_window()
  self.selection.assert_called_once();self.assertIsNone(self.route.initial_binding)
 def test_insufficient_budget_refuses_before_native_backend(self):
  self.run.ui_deadline=106.5
  with self.assertRaisesRegex(RuntimeError,'helper reserve'):self.route.acquire_initial_window()
  self.native.assert_not_called()
 def test_exact_minimum_budget_refuses_before_native_backend(self):
  self.run.ui_deadline=106.75
  with self.assertRaisesRegex(RuntimeError,'helper reserve'):self.route.acquire_initial_window()
  self.native.assert_not_called()
 def test_matching_admitted_binding_reaches_first_helper(self):
  self.route.acquire_initial_window()
  with patch.object(self.route,'bound_window',return_value=(self.identity,self.window)),patch.object(self.route,'invoke',side_effect=RuntimeError('fixture reached helper')) as invoke:
   with self.assertRaisesRegex(RuntimeError,'fixture reached helper'):self.route.capture()
  request=invoke.call_args.args[0]
  self.assertEqual(request['identity'],self.identity);self.assertEqual(request['window'],self.window)
  self.assertEqual(request['sequence'],1)
 def test_slow_native_sample_cannot_admit_after_deadline(self):
  def slow(*a):self.clock+=3.1;return self.window
  self.selection.side_effect=slow
  with self.assertRaisesRegex(RuntimeError,'exceeded budget'):self.route.acquire_initial_window()
  self.assertIsNone(self.route.initial_binding)
 def test_acquisition_forbidden_after_capture_or_input_transaction(self):
  for attribute,value in (('sequence',1),('last',{}),('input_started',True),('frames',{1:{}}),('helper',object())):
   self.route=w.WindowRoute(self.run);setattr(self.route,attribute,value)
   with self.assertRaisesRegex(RuntimeError,'unavailable after'):self.route.acquire_initial_window()
  self.native.assert_not_called()
 def test_drift_after_stability_refuses_before_new_request(self):
  self.route.acquire_initial_window()
  with patch.object(self.route,'bound_window',return_value=(self.identity,{**self.window,'bounds':{**self.window['bounds'],'Width':1102.}})),patch.object(self.route,'invoke') as invoke:
   with self.assertRaisesRegex(RuntimeError,'no reselection'):self.route.capture()
  invoke.assert_not_called();self.assertEqual(self.route.sequence,0)
 def test_late_helper_refusal_does_not_restart_stability(self):
  self.route.acquire_initial_window()
  with patch.object(self.route,'bound_window',return_value=(self.identity,self.window)),patch.object(self.route,'invoke',side_effect=RuntimeError('helper owned window changed')) as invoke:
   with self.assertRaisesRegex(RuntimeError,'helper owned window changed'):self.route.capture()
  invoke.assert_called_once();self.assertEqual(self.route.sequence,1)
  with self.assertRaisesRegex(RuntimeError,'unavailable after'):self.route.acquire_initial_window()
if __name__=='__main__':unittest.main()
