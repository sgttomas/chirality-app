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
 def test_retry_offer_only_after_settlement_and_quit(self):
  self.run.reservation=SimpleNamespace(observe=lambda:None)
  for settled,quit_requested in ((False,False),(True,False),(False,True),(True,True)):
   self.run.supplier_settled=settled;self.run.quit_requested=quit_requested
   status=self.run.held_status('fixture')
   self.assertEqual(status['recovery_control'] is not None,settled and quit_requested)
 def test_settlement_and_already_stopped_cleanup_require_protocol(self):
  self.run.screen.observe=Mock(return_value={'envelopes':[]})
  self.run.cleanup=True
  for confirmed,phase in ((False,'cleanup-source'),(True,'settlement')):
   self.run.stop_confirmed=confirmed
   self.run.diagnostics()
   self.run.screen.observe.assert_called_with(phase,protocol=True)
 def test_settlement_uses_nonextending_45second_phase(self):
  self.run.cleanup_end=200
  with patch.object(m.time,'monotonic',return_value=100):
   self.assertEqual(self.run.settlement_deadline(),145)
  with patch.object(m.time,'monotonic',return_value=130):
   self.assertEqual(self.run.settlement_deadline(),145)
  self.run.cleanup=True;self.run.stop_confirmed=False
  self.run.screen.observe=Mock(return_value={})
  self.run.diagnostics();self.run.screen.observe.assert_called_once_with('settlement',protocol=True)
  self.run.supplier_settled=True
  with patch.object(m.time,'monotonic',return_value=146):
   self.assertEqual(self.run.settlement_deadline(),146)
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
 def test_initial_stability_runs_once_inside_15second_limit(self):
  self.run.screen.window.acquire_initial_window=Mock(side_effect=RuntimeError('not stable'))
  self.run.screen.window.capture=Mock()
  with patch.object(m.time,'monotonic',return_value=100):
   with self.assertRaisesRegex(RuntimeError,'not stable'):self.run.observe_ready()
  self.assertEqual(self.run.ui_deadline,115)
  self.run.screen.window.acquire_initial_window.assert_called_once()
  self.run.screen.window.capture.assert_not_called()
 def test_initial_capture_disappearance_blocks_cleanup_capture_retry(self):
  self.run.screen.window.acquire_initial_window=Mock()
  self.run.screen.window.capture=Mock(side_effect=m.w.WindowUnavailable('selected window disappeared'))
  with self.assertRaisesRegex(m.w.WindowUnavailable,'disappeared'):self.run.observe_ready()
  self.assertEqual(self.run.screen.window.failure,'selected window disappeared')
  with patch.object(b.Run,'cleanup_attempt') as inherited:
   with self.assertRaisesRegex(RuntimeError,'no capture retry'):self.run.cleanup_attempt()
  inherited.assert_not_called();self.run.screen.window.capture.assert_called_once()
 def test_initial_acquisition_capture_then_observation_order(self):
  events=[];frame={'fixture':'verified'};observed={'fixture':'source'};gen={'home':'home','appSession':'s','spawnCounter':1}
  self.run.screen.window.acquire_initial_window=Mock(side_effect=lambda:events.append('acquire'))
  self.run.screen.window.capture=Mock(side_effect=lambda:events.append('capture') or frame)
  self.run.screen.observe=Mock(side_effect=lambda *a,**k:events.append('observe') or observed)
  with patch.object(b,'source_gate',return_value=gen),patch.object(b,'ready_gate'),patch.object(b,'reject_permanent_witness_failure'):
   self.assertEqual(self.run.observe_ready(),gen)
  self.assertEqual(events,['acquire','capture','observe'])
  self.run.screen.observe.assert_called_once_with('ready',protocol=True,initial_frame=frame)
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
