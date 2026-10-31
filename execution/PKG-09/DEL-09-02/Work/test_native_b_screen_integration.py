"""ScreenRun integration and phase reserves; no App/native API calls."""
from pathlib import Path
import importlib.util,json,os,tempfile,time,unittest
from types import SimpleNamespace
from unittest.mock import Mock,patch
s=importlib.util.spec_from_file_location('screen_integration_controller',Path(__file__).with_name('native_successor_relaunch.py'));b=importlib.util.module_from_spec(s);s.loader.exec_module(b);m=b.screen_support
class Integration(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(dir=b.T3/'scratch',prefix='screen-integration-');self.addCleanup(self.tmp.cleanup)
  self.root=Path(self.tmp.name).resolve();self.run=m.make_run(b)(self.root,{'candidate_key':'invented','expected_generation_home':'home'},time.monotonic()+295,'a'*64)
  self.run.record=Mock();self.run.safe_log=Mock();self.run.alive=Mock()
 def test_helper_unknown_blocks_quit_reap_and_held_status_reports_it(self):
  self.run.supplier_settled=self.run.quit_requested=True
  self.run.reservation=SimpleNamespace(observe=lambda:{'code':1,'status':0},reap=Mock())
  self.run.screen.window.helpers_settled=lambda:False;self.run.screen.window.helper=SimpleNamespace(pid=123)
  with self.assertRaisesRegex(RuntimeError,'helper unsettled'):self.run.wait_for_quit_exit()
  self.run.reservation.reap.assert_not_called()
  status=self.run.held_status('fixture');self.assertEqual(status['window_helper']['pid'],123)
  self.assertIsNone(status['administrative_release_request'])
 def test_unexpected_quit_question_never_confirms(self):
  self.run.supplier_settled=self.run.quit_requested=True
  self.run.reservation=SimpleNamespace(observe=lambda:None,reap=Mock())
  self.run.dialog=Mock(return_value=([],object()));self.run.ax=SimpleNamespace(text=lambda rows:'unexpected live work',press=Mock())
  with self.assertRaisesRegex(RuntimeError,'unexpected Quit'):self.run.wait_for_quit_exit()
  self.run.ax.press.assert_not_called()
 def test_owned_menu_quit_is_exact_and_cycle_pruned(self):
  tree={'app':{'AXTitle':'Invented','AXMenuBar':'bar'},'bar':{'AXChildren':['item']},'item':{'AXRole':'AXMenuBarItem','AXTitle':'Invented','AXChildren':['menu','app']},
        'menu':{'AXRole':'AXMenu','AXChildren':['quit','other']},'quit':{'AXRole':'AXMenuItem','AXTitle':'Quit Invented','AXEnabled':True},'other':{'AXRole':'AXMenuItem','AXTitle':'Other','AXEnabled':True}}
  self.run.ax=SimpleNamespace(app='app',attr=lambda e,k:tree[e].get(k),own=Mock(),c=SimpleNamespace(CFEqual=lambda a,c:a==c),press=Mock())
  backend=SimpleNamespace(close=Mock())
  with patch.object(m.w.d,'NativeBackend',return_value=backend),patch.object(m.w.d,'bound_identity',return_value={'pid':1}):self.run.request_quit_ui()
  self.run.ax.press.assert_called_once_with('quit')
 def test_initial_window_wait_has_15second_limit(self):
  self.run.screen.window.capture=Mock(side_effect=m.w.WindowUnavailable('not yet'))
  with patch.object(m.time,'monotonic',side_effect=[0,16]),patch.object(m.time,'sleep'):
   with self.assertRaises(m.w.WindowUnavailable):self.run.observe_ready()
  self.assertEqual(self.run.screen.window.failure,'not yet')
 def test_phase_caps_preserve_downstream_reserve(self):
  expected={'ready':(60,205),'recheck':(35,170),'cleanup-source':(35,135),'stop':(20,115),'stop-confirmation':(30,85),'settlement':(45,40)}
  self.assertEqual(m.PHASE_BUDGETS,expected)
  self.assertEqual(15+15+sum(v[0] for v in expected.values())+40,295)
  for phase,(duration,reserve) in expected.items():
   self.run.screen.active_phase=None
   self.run.cleanup_end=100+duration+reserve
   with patch.object(m.time,'monotonic',return_value=100):self.run.screen.begin_phase(phase)
   self.assertEqual(self.run.ui_deadline,100+duration)
   self.run.cleanup_end-=0.1;self.run.screen.active_phase=None
   with patch.object(m.time,'monotonic',return_value=100):
    with self.assertRaisesRegex(RuntimeError,'full phase'):self.run.screen.begin_phase(phase)
 def test_repeated_phase_cannot_extend_deadline(self):
  self.run.cleanup_end=395
  with patch.object(m.time,'monotonic',return_value=100):self.run.screen.begin_phase('ready')
  with patch.object(m.time,'monotonic',return_value=120):self.run.screen.begin_phase('ready')
  self.assertEqual(self.run.screen.phase_deadline,160)
  with patch.object(m.time,'monotonic',return_value=161):
   with self.assertRaisesRegex(RuntimeError,'budget exhausted'):self.run.screen.begin_phase('ready')
 def test_stop_reobserve_unsets_only_proven_unsent_stop(self):
  screen=self.run.screen;frame={'sha256':'f','sequence':1};screen.window=SimpleNamespace(sequence=0,last=frame,frames={1:frame},capture=Mock(return_value=frame),input=Mock(side_effect=m.w.Reobserve('changed')))
  self.run.generation={'appSession':'s','home':'home','spawnCounter':1}
  screen.next_control=Mock(side_effect=[({'action':'click-stop','point':[50,150]},frame),({'action':'refuse','reason':'test stop'},frame)])
  with self.assertRaisesRegex(RuntimeError,'test stop'):screen.observe('stop',stop=True)
  self.assertFalse(self.run.stop_requested);self.assertFalse(screen.pending_effect)
 def test_controller_slot_binding_checks_pid_parent_hash_and_fixed_end(self):
  from datetime import datetime,timedelta,timezone
  (self.root/'admission.json').write_text('{}');(self.root/b.SLOT_SOURCE.name).write_text('invented')
  admitted={'slot_entry_sha256':b.setup.digest(self.root/b.SLOT_SOURCE.name)}
  at=datetime(2026,10,31,12,0,0,tzinfo=timezone.utc);end=at+timedelta(seconds=295)
  record={'controller_pid':os.getpid(),'slot_parent_pid':os.getppid(),'admission_sha256':b.setup.digest(self.root/'admission.json'),
          'slot_entry_sha256':admitted['slot_entry_sha256'],'at':at.isoformat(),'fixed_window_end':end.isoformat()}
  path=self.root/'slot-entry.json'
  def write(value):path.write_text(json.dumps(value));path.chmod(0o600)
  write(record);b.validate_v2_slot_entry(self.root,admitted,end.timestamp())
  for key,value in [('controller_pid',os.getpid()+1),('slot_parent_pid',os.getppid()+1),('admission_sha256','bad'),('slot_entry_sha256','bad'),('fixed_window_end',(end+timedelta(seconds=1)).isoformat())]:
   with self.subTest(key=key):
    write({**record,key:value})
    with self.assertRaisesRegex(RuntimeError,'acquired-slot'):b.validate_v2_slot_entry(self.root,admitted,end.timestamp())
if __name__=='__main__':unittest.main()
