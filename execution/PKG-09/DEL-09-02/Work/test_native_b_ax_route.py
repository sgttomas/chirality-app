"""AX-first complete journey/refusal fixtures. No native libraries or App actions."""
from pathlib import Path
import copy,importlib.util,json,tempfile,time,unittest
from types import SimpleNamespace
from unittest.mock import Mock,patch
spec=importlib.util.spec_from_file_location('ax_route_controller_test',Path(__file__).with_name('native_successor_relaunch.py'));b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b);m=b.ax_route_support;w=b.screen_support.w
spec=importlib.util.spec_from_file_location('ax_route_source_fixture',Path(__file__).with_name('test_native_successor_relaunch.py'));t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
spec=importlib.util.spec_from_file_location('ax_route_question_fixture',Path(__file__).with_name('test_native_b_modal.py'));q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)
t.G=q.G

def prop(role,title=None,value=None,enabled=True):return {'AXRole':role,'AXTitle':title,'AXValue':value,'AXDescription':None,'AXEnabled':enabled}
class Route(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(dir=b.T3/'scratch',prefix='owned-AX-route-fixture-');self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name).resolve()
  self.bundle=self.root/'fixture.app';binary=self.bundle/'Contents/Resources/codex/bin/codex';binary.parent.mkdir(parents=True);binary.write_text('invented never executed')
  self.value={'candidate_key':'invented','bundle':str(self.bundle),'expected_generation_home':t.G['home']}
  self.run=m.make_run(b)(self.root,self.value,time.monotonic()+295,'a'*64);self.run.alive=Mock();self.run.safe_log=Mock();self.run.report=Mock();self.run.ui_deadline=self.run.cleanup_end
  self.identity={'pid':123,'ppid':99,'start_sec':1,'start_usec':2,'executable':'fixture'}
  self.window={'window_id':10,'title':w.TITLE,'bounds':{'X':0,'Y':0,'Width':1100,'Height':800},'on_screen':True,'layer':0,'own_visible_layer0_count':1}
  self.modal={**self.window,'window_id':20,'title':'Stop Codex','layer':8}
  self.frame={'identity':self.identity,'window':self.window,'sequence':1,'sha256':'image'}
  self.window_route=self.run.screen.window
  self.window_route.acquire_initial_window=Mock(return_value=(self.identity,self.window));self.window_route.initial_binding=(self.identity,self.window)
  self.window_route.capture=Mock(return_value=self.frame);self.window_route.input=Mock(return_value=self.frame);self.window_route.helpers_settled=Mock(return_value=True)
  self.run.screen.observe=Mock(side_effect=AssertionError('screenshot operator fallback forbidden'))
  self.nodes={2:prop('AXWindow',w.TITLE),3:prop('AXWebArea'),4:prop('AXDisclosureTriangle','Host diagnostics',False),5:prop('AXDisclosureTriangle','Lifecycle events (2)',False),6:prop('AXDisclosureTriangle','Raw native envelopes (including unknown fields)',False),7:prop('AXDisclosureTriangle','Connection and access',False),8:prop('AXButton','Stop Codex…')}
  self.state='ready';self.modal_open=False;self.front=True;self.web=True;self.pressed=[];self.question=q.question();self.mapping={2:10,100:20}
  def press(e):
   self.pressed.append(e)
   if e in (4,5,6,7):self.nodes[e]['AXValue']=True
   elif e==8:self.modal_open=True
   elif e==103:self.modal_open=False;self.state='stopped'
  def walk(e):
   if e==100:return [(100,prop('AXWindow','Stop Codex'),False),(101,prop('AXStaticText','Stop Codex'),False),(102,prop('AXStaticText',value=self.question),False),(103,prop('AXButton','Stop Codex'),False),(104,prop('AXButton','Keep Codex running'),False),(105,prop('AXButton','Cancel'),False)]
   if not self.web:return [(2,self.nodes[2],False)]
   observed=t.observation(self.bundle,self.state);header='State: '+self.state+' · generation '+json.dumps(t.G)+' · version codex-cli 0.160.0 · verification {}'
   return [(i,p,i>=3) for i,p in self.nodes.items()]+[(20,prop('AXStaticText',value=header),True),(21,prop('AXStaticText',value=json.dumps({k:observed[k] for k in ('lifecycle','clientRequests')})),True),(22,prop('AXStaticText',value=json.dumps(observed['envelopes'])),True)]
  def attr(e,k):return self.front if e==1 and k=='AXFrontmost' else self.nodes.get(e,{}).get(k)
  self.ax=SimpleNamespace(app=1,main=lambda:2,main_if_available=lambda:2,windows=lambda:[2,100] if self.modal_open else [2],walk=walk,attr=attr,press=press,own=Mock(),last_walk_observation={'fixture':True},last_window_observation=[])
  self.run.ax=self.ax
  self.run.wait_for=lambda fn,seconds,reason:fn() or (_ for _ in ()).throw(RuntimeError(reason))
  self.addCleanup(patch.stopall)
  patch.object(w.d,'NativeBackend',return_value=SimpleNamespace(close=Mock())).start()
  patch.object(w.d,'bound_identity',return_value=self.identity).start()
  patch.object(w,'select_main',return_value=self.window).start()
  self.focus_receipt=Mock(return_value={'activation':None,'observations':[{'frontmost':True}]});self.focus_result_override=None
  def private_json(path,limit):
   if path.name.endswith('.focus.json'):return self.focus_receipt()
   return self.focus_result_override if self.focus_result_override is not None else {'action':'focus','sequence':int(path.name.split('-')[-1].split('.')[0]),'posted_or_focus_observed':True}
  self.json_reader=patch.object(w,'private_json',side_effect=private_json).start()
  patch.object(w,'owned_inventory',return_value=[self.window]).start()
  patch.object(w,'select_modal',side_effect=lambda *args:self.modal if self.modal_open else (_ for _ in ()).throw(w.WindowUnavailable('no modal'))).start()
  patch.object(m,'window_number',side_effect=lambda ax,e:self.mapping[e]).start()
 def test_complete_mock_journey_preserves_all_real_gates_and_no_operator_fallback(self):
  gen=self.run.observe_ready();self.assertEqual(gen,t.G)
  self.window_route.input.assert_called_once_with('focus',self.frame)
  self.assertEqual(b.ready_gate(self.run.diagnostics(),self.value),gen)
  self.run.request_quit_ui=Mock();self.run.wait_for_quit_exit=Mock(return_value=0)
  self.assertEqual(self.run.stop_and_quit(gen),0)
  b.check_requests(self.run.stop_observation,gen);b.settlement_gate(self.run.stop_observation,gen)
  self.assertEqual(self.pressed,[4,5,6,7,8,103]);self.assertTrue(self.run.supplier_settled)
  self.run.request_quit_ui.assert_called_once();self.run.screen.observe.assert_not_called()
  raw=json.loads((self.root/'ready-observation.json').read_text());self.assertEqual(raw['observation_provenance']['kind'],'owned-native-AX-text')
 def test_missing_webkit_records_exact_refusal_and_never_uses_images_as_source(self):
  self.web=False
  with patch.object(m.time,'sleep'):
   with self.assertRaisesRegex(RuntimeError,'read allowance exhausted'):self.run.observe_ready()
  with self.assertRaisesRegex(RuntimeError,'no screenshot-only fallback'):self.run.cleanup_attempt()
  self.run.screen.observe.assert_not_called();self.assertEqual(self.pressed,[])
  self.assertTrue(list(self.root.glob('owned-AX-*.json')))
 def test_wrong_window_number_or_focus_refuses_before_control(self):
  self.run.ax_binding=(self.identity,self.window);self.mapping[2]=99
  with self.assertRaisesRegex(RuntimeError,'does not match'):self.run.open_disclosure('Host diagnostics')
  self.assertEqual(self.pressed,[])
  self.mapping[2]=10;self.front=False
  with self.assertRaisesRegex(RuntimeError,'no longer frontmost'):self.run.bound_main(press=True)
 def test_disclosure_does_not_repeat_or_accept_missing_effect(self):
  self.run.ax_binding=(self.identity,self.window);self.ax.press=lambda e:self.pressed.append(e)
  with self.assertRaisesRegex(RuntimeError,'effect unavailable'):self.run.open_disclosure('Host diagnostics')
  with self.assertRaisesRegex(RuntimeError,'already pressed'):self.run.open_disclosure('Host diagnostics')
  self.assertEqual(self.pressed,[4])
 def test_native_question_unexpected_effect_refuses_before_confirmation(self):
  gen=self.run.observe_ready();self.run.cleanup=True;self.run.diagnostics();self.run.request_stop_ui()
  self.question+=' Delete another project.'
  with self.assertRaisesRegex(RuntimeError,'unexpected/missing'):self.run.confirm_stop_ui(gen)
  self.assertNotIn(103,self.pressed);self.assertTrue(self.run.ax_failed)
  with self.assertRaisesRegex(RuntimeError,'retain custody'):self.run.cleanup_attempt()
 def test_modal_cannot_use_main_window_or_foreign_generation(self):
  gen=self.run.observe_ready();self.run.cleanup=True;self.run.diagnostics();self.run.request_stop_ui()
  self.mapping[100]=10
  with self.assertRaisesRegex(RuntimeError,'unavailable'):self.run.confirm_stop_ui(gen)
  self.assertNotIn(103,self.pressed)
 def test_explicit_nonmodal_or_wrong_parent_refuses_before_confirmation(self):
  gen=self.run.observe_ready();self.run.cleanup=True;self.run.diagnostics();self.run.request_stop_ui()
  original=self.ax.attr
  self.ax.attr=lambda e,k:False if e==100 and k=='AXModal' else original(e,k)
  with self.assertRaisesRegex(RuntimeError,'not modal'):self.run.confirm_stop_ui(gen)
  self.assertNotIn(103,self.pressed)
  self.ax.attr=lambda e,k:300 if e==100 and k=='AXParent' else original(e,k)
  self.ax.c=SimpleNamespace(CFEqual=lambda a,c:a==c);self.mapping[300]=99
  with self.assertRaisesRegex(RuntimeError,'not original main'):self.run.confirm_stop_ui(gen)
  self.assertNotIn(103,self.pressed)
 def test_foreign_modal_parent_refuses_before_confirmation(self):
  gen=self.run.observe_ready();self.run.cleanup=True;self.run.diagnostics();self.run.request_stop_ui()
  original=self.ax.attr;self.ax.attr=lambda e,k:300 if e==100 and k=='AXParent' else original(e,k)
  self.ax.own=Mock(side_effect=lambda e:(_ for _ in ()).throw(RuntimeError('foreign parent')) if e==300 else None)
  with self.assertRaisesRegex(RuntimeError,'foreign parent'):self.run.confirm_stop_ui(gen)
  self.assertNotIn(103,self.pressed)
 def test_incomplete_protocol_text_does_not_use_saved_expected_values(self):
  self.run.ax_binding=(self.identity,self.window)
  self.ax.walk=lambda e:[(3,prop('AXWebArea'),True),(4,prop('AXStaticText',value='State: ready'),True)]
  with self.assertRaisesRegex(RuntimeError,'header unavailable'):self.run.read_diagnostics()
  self.assertIsNone(self.run.generation);self.run.screen.observe.assert_not_called()
 def test_changed_generation_at_stop_refuses_before_button(self):
  gen=self.run.observe_ready();self.run.cleanup=True;self.run.diagnostics()
  with patch.object(b,'source_gate',side_effect=[gen,RuntimeError('cleanup source generation changed')]):
   with self.assertRaisesRegex(RuntimeError,'generation changed'):self.run.request_stop_ui()
  self.assertNotIn(8,self.pressed)
 def test_ambiguous_or_disabled_or_native_masquerading_web_control_refuses(self):
  web=(3,prop('AXWebArea'),True);button=(8,prop('AXButton','Stop Codex…'),True)
  for rows in ([web,button,button],[web,(8,prop('AXButton','Stop Codex…',enabled=False),True)],[web,(8,button[1],False)]):
   with self.assertRaises(RuntimeError):m.web_control(rows,'AXButton','Stop Codex…')
 def test_web_question_cannot_be_native_confirmation(self):
  with self.assertRaisesRegex(RuntimeError,'not a native subtree'):m.native_question([(1,prop('AXStaticText',value=self.question),True)])
 def test_record_failure_prevents_control_and_preserves_custody(self):
  self.run.ax_binding=(self.identity,self.window);self.run.record=Mock(side_effect=OSError('fixture disk failure'))
  with self.assertRaises(OSError):self.run.open_disclosure('Host diagnostics')
  self.assertEqual(self.pressed,[]);self.assertFalse(self.run.ax_failed)
 def test_webkit_wait_is_read_only_until_tree_and_control_appear(self):
  self.run.ax_binding=(self.identity,self.window);original=self.ax.walk;count=0
  def delayed(e):
   nonlocal count
   count+=1
   if count==1:self.assertEqual(self.pressed,[]);return [(2,self.nodes[2],False)]
   if count==2:self.assertEqual(self.pressed,[]);return [(2,self.nodes[2],False),(3,self.nodes[3],True)]
   return original(e)
  self.ax.walk=delayed
  with patch.object(m.time,'sleep') as sleep:self.run.open_disclosure('Host diagnostics')
  self.assertEqual(self.pressed,[4]);self.assertEqual(sleep.call_count,2)
 def test_stopped_ready_witness_failure_keeps_bound_source_cleanup(self):
  self.state='stopped'
  with self.assertRaises(b.PermanentWitnessFailure):self.run.observe_ready()
  self.assertFalse(self.run.ax_failed);self.assertEqual(self.run.generation,t.G)
  self.run.reservation=SimpleNamespace(observe=lambda:None)
  self.run.request_quit_ui=Mock();self.run.wait_for_quit_exit=Mock(return_value=0)
  self.assertEqual(self.run.cleanup_attempt(),0);self.assertNotIn(8,self.pressed)
 def test_ready_capture_failure_is_terminal_and_not_duplicate_record(self):
  self.window_route.capture.side_effect=[self.frame,RuntimeError('corroboration failed')]
  with self.assertRaisesRegex(RuntimeError,'corroboration failed'):self.run.observe_ready()
  self.assertFalse((self.root/'ready-observation.json').exists());self.assertFalse(self.run.ax_failed)
  self.assertEqual(self.window_route.capture.call_count,2)
 def test_focus_loss_does_not_block_read_only_settlement_or_owned_menu_quit(self):
  self.run.observe_ready();self.run.cleanup=True;self.run.stop_confirmed=True;self.state='stopped';self.front=False
  result=self.run.diagnostics();b.settlement_gate(result,t.G)
  parent=type(self.run).__mro__[1]
  with patch.object(parent,'request_quit_ui') as post:self.run.request_quit_ui()
  post.assert_called_once();self.assertTrue(self.run.quit_posted)
 def test_quit_intent_before_capture_failure_is_not_reported_as_post(self):
  self.run.observe_ready();self.run.cleanup=True;self.run.supplier_settled=True;self.run.quit_requested=True
  self.run.reservation=SimpleNamespace(observe=lambda:None)
  self.window_route.capture.side_effect=RuntimeError('capture failed before Quit')
  with self.assertRaisesRegex(RuntimeError,'capture failed'):self.run.request_quit_ui()
  status=self.run.held_status('fixture');self.assertFalse(status['quit_posted']);self.assertIsNone(status['recovery_control'])
  with self.assertRaisesRegex(RuntimeError,'intent without observed post'):self.run.cleanup_attempt()
 def test_node_or_read_headroom_refuses_before_stop(self):
  self.run.observe_ready();self.run.cleanup=True;self.run.diagnostics();self.run.ax_reads=31
  with self.assertRaisesRegex(RuntimeError,'headroom'):self.run.request_stop_ui()
  self.assertNotIn(8,self.pressed)
  self.run.ax_reads=0;self.run.ax_failed=False;original=self.ax.walk
  self.ax.walk=lambda e:original(e)+[(500+i,prop('AXGroup'),True) for i in range(701)] if e==2 else original(e)
  with self.assertRaisesRegex(RuntimeError,'headroom'):self.run.request_stop_ui()
  self.assertNotIn(8,self.pressed)
 def test_settlement_reads_have_reserved_rate_and_count(self):
  self.run.observe_ready();self.run.cleanup=True;self.run.stop_confirmed=True;self.state='stopped'
  self.run.last_settlement_read=100
  with patch.object(m.time,'monotonic',return_value=100.5),patch.object(m.time,'sleep') as sleep:self.run.diagnostics()
  sleep.assert_called_once_with(1.0)
  self.run.settlement_reads=30;self.run.last_settlement_read=None
  self.run.screen.phase_deadline=time.monotonic()+45;self.run.ui_deadline=self.run.screen.phase_deadline
  with self.assertRaisesRegex(RuntimeError,'settlement read allowance'):self.run.diagnostics()
 def test_cleanup_evidence_failure_prevents_stop_and_confirmation_presses(self):
  self.run.observe_ready();self.run.cleanup=True;self.run.diagnostics();original=b.write_once
  def refuse_stop(path,value):
   if path.name=='owned-AX-stop-intent.json':raise OSError('intent write failed')
   return original(path,value)
  with patch.object(b,'write_once',side_effect=refuse_stop):
   with self.assertRaisesRegex(OSError,'intent write failed'):self.run.request_stop_ui()
  self.assertNotIn(8,self.pressed);self.run.ax_failed=False
  self.run.request_stop_ui()
  def refuse_confirm(path,value):
   if path.name=='stop-confirmation.json':raise OSError('confirmation write failed')
   return original(path,value)
  with patch.object(b,'write_once',side_effect=refuse_confirm):
   with self.assertRaisesRegex(OSError,'confirmation write failed'):self.run.confirm_stop_ui(t.G)
  self.assertNotIn(103,self.pressed)
 def test_unmappable_other_owned_root_does_not_substitute_or_abort_modal(self):
  self.run.observe_ready();self.run.cleanup=True;self.run.diagnostics();self.run.request_stop_ui()
  def number(ax,e):
   if e==2:raise m.WindowNumberUnavailable('fixture unmappable main root')
   return self.mapping[e]
  with patch.object(m,'window_number',side_effect=number):self.run.confirm_stop_ui(t.G)
  self.assertIn(103,self.pressed)
 def test_guard_failure_during_read_is_not_an_ax_boundary_failure(self):
  self.run.ax_binding=(self.identity,self.window)
  self.run.alive=Mock(side_effect=m.AXGateFailure('guard heartbeat unavailable'))
  with self.assertRaisesRegex(m.AXGateFailure,'heartbeat'):self.run.main_rows()
  self.assertFalse(self.run.ax_failed)
 def test_unused_activation_can_be_used_once_before_first_press(self):
  self.run.observe_ready() # initial fixture opens controls, reset to fresh first-control boundary below
  self.run.ax_actions.clear();self.pressed.clear();self.nodes[4]['AXValue']=False;self.front=False
  def focus(action,frame):
   self.front=True
   self.focus_receipt.return_value={'activation':{'receiver_pid':123,'activation_policy':0,'options':0,'request_sent':True},'observations':[{'frontmost':False},{'frontmost':True}]}
   return self.frame
  self.window_route.input.side_effect=focus
  self.run.open_disclosure('Host diagnostics')
  self.assertEqual(self.pressed,[4]);self.assertTrue(self.run.activation_spent);self.assertTrue(self.run.first_press_focus_used)
  self.assertTrue((self.root/'first-press-focus-observed.json').exists())
  self.front=False
  with self.assertRaisesRegex(RuntimeError,'no unused'):self.run.first_press_focus()
  self.assertEqual(self.window_route.input.call_count,2) # initial no-op + one actual request
 def test_ready_journey_recovers_only_initial_noop_focus_drift(self):
  original=self.ax.walk;walks=0
  def walk(e):
   nonlocal walks
   walks+=1
   if walks==1:self.front=False
   return original(e)
  self.ax.walk=walk
  def focus(action,frame):
   self.front=True
   self.focus_receipt.return_value=({'activation':None,'observations':[{'frontmost':True}]} if self.window_route.input.call_count==1 else
     {'activation':{'receiver_pid':123,'activation_policy':0,'options':0,'request_sent':True},'observations':[{'frontmost':True}]})
   return self.frame
  self.window_route.input.side_effect=focus
  self.assertEqual(self.run.observe_ready(),t.G)
  self.assertEqual(self.window_route.input.call_count,2);self.assertEqual(self.pressed,[4,5,6])
  self.assertTrue(self.run.activation_spent)
 def test_focus_receipt_is_for_the_exact_next_helper_operation(self):
  self.window_route.sequence=11
  self.run.focus_receipt(self.frame)
  self.json_reader.assert_any_call(self.root/'window-helper-012.focus.json',32768)
  self.json_reader.assert_any_call(self.root/'window-helper-012.result.json',16384)
  self.assertFalse(self.run.activation_spent)
  self.focus_receipt.side_effect=FileNotFoundError('missing trace')
  with self.assertRaises(FileNotFoundError):self.run.focus_receipt(self.frame)
  self.assertTrue(self.run.activation_spent)
 def test_changed_first_press_capture_never_activates(self):
  self.run.ax_binding=(self.identity,self.window);self.run.activation_spent=False;self.front=False;self.run.screen.active_phase='ready'
  self.window_route.capture.return_value={**self.frame,'window':{**self.window,'window_id':99}}
  with self.assertRaisesRegex(RuntimeError,'capture changed binding'):self.run.first_press_focus()
  self.window_route.input.assert_not_called();self.assertTrue(self.run.activation_spent)
 def test_sent_or_unknown_activation_never_retries(self):
  self.run.ax_binding=(self.identity,self.window);self.front=False;self.run.screen.active_phase='ready'
  for spent,used,actions in ((True,False,set()),(False,True,set()),(False,False,{'Host diagnostics'})):
   self.run.activation_spent=spent;self.run.first_press_focus_used=used;self.run.ax_actions=actions
   with self.assertRaisesRegex(RuntimeError,'no unused'):self.run.first_press_focus()
  self.window_route.input.assert_not_called()
 def test_missing_or_wrong_focus_receipt_cannot_grant_unused_budget(self):
  for trace in ({'observations':[{'frontmost':True}]},{'activation':{'receiver_pid':999,'request_sent':True,'options':0,'activation_policy':0},'observations':[{'frontmost':True}]}):
   self.focus_receipt.return_value=trace
   with self.assertRaises(RuntimeError):self.run.focus_receipt(self.frame)
   self.assertTrue(self.run.activation_spent)
 def test_first_press_focus_discards_pre_activation_control_reference(self):
  self.run.ax_binding=(self.identity,self.window);self.run.activation_spent=False;self.front=False;self.run.screen.active_phase='ready'
  original=self.ax.walk
  def focus(action,frame):
   self.front=True;self.nodes[44]=self.nodes.pop(4)
   self.focus_receipt.return_value={'activation':{'receiver_pid':123,'activation_policy':0,'options':0,'request_sent':True},'observations':[{'frontmost':True}]}
   return self.frame
  self.window_route.input.side_effect=focus
  old_press=self.ax.press
  def press(e):
   if e==44:self.pressed.append(e);self.nodes[e]['AXValue']=True
   else:old_press(e)
  self.ax.press=press
  self.run.open_disclosure('Host diagnostics')
  self.assertEqual(self.pressed,[44])
 def test_first_press_activation_refuses_cleanup_and_stop_phase_disclosures(self):
  self.run.ax_binding=(self.identity,self.window);self.run.activation_spent=False;self.front=False
  for cleanup,phase in ((True,'cleanup-source'),(True,'stop'),(False,'stop'),(True,'ready')):
   self.run.cleanup=cleanup;self.run.screen.active_phase=phase
   with self.assertRaisesRegex(RuntimeError,'no unused'):self.run.open_disclosure('Host diagnostics')
  self.window_route.input.assert_not_called();self.assertEqual(self.pressed,[])
 def test_second_helper_noop_still_consumes_boundary_attempt(self):
  self.run.observe_ready();self.run.ax_actions.clear();self.pressed.clear();self.nodes[4]['AXValue']=False;self.front=False
  def focus(action,frame):self.front=True;return self.frame
  self.window_route.input.side_effect=focus
  self.run.open_disclosure('Host diagnostics')
  self.assertTrue(self.run.activation_spent);self.assertTrue(self.run.first_press_focus_used)
  self.assertEqual(self.window_route.input.call_count,2)
  self.front=False
  with self.assertRaisesRegex(RuntimeError,'no unused'):self.run.first_press_focus()
  self.assertEqual(self.window_route.input.call_count,2)
 def test_focus_result_and_noop_shape_are_required(self):
  for result in ({'action':'click','sequence':1,'posted_or_focus_observed':True},{'action':'focus','sequence':99,'posted_or_focus_observed':True},{'action':'focus','sequence':1,'posted_or_focus_observed':False}):
   self.focus_result_override=result
   with self.assertRaisesRegex(RuntimeError,'result receipt'):self.run.focus_receipt(self.frame)
   self.assertTrue(self.run.activation_spent)
  self.focus_result_override=None
  self.focus_receipt.return_value={'activation':None,'observations':[{'frontmost':False},{'frontmost':True}]}
  with self.assertRaisesRegex(RuntimeError,'no-op receipt'):self.run.focus_receipt(self.frame)
  self.assertTrue(self.run.activation_spent)
 def test_guard_phase_deadline_remains_enforced(self):
  self.run.ui_deadline=time.monotonic()-1
  with patch.object(b.Run,'alive'):
   with self.assertRaisesRegex(RuntimeError,'AX phase deadline'):type(self.run).alive(self.run)

class Bounds(unittest.TestCase):
 def test_per_element_timeout_and_owner_refusal(self):
  class Base:
   def own(self,e):
    if e=='foreign':raise RuntimeError('foreign')
   def string(self,n):return n
   def value(self,p):return 'value'
  ax=m.bounded_ax(Base)();ax.a=SimpleNamespace(AXUIElementSetMessagingTimeout=Mock(return_value=0),AXUIElementCopyAttributeValue=Mock(return_value=0))
  self.assertEqual(ax.attr('own','AXRole'),'value');ax.a.AXUIElementSetMessagingTimeout.assert_called_once_with('own',.2)
  with self.assertRaisesRegex(RuntimeError,'foreign'):ax.attr('foreign','AXRole')
  self.assertEqual(ax.a.AXUIElementSetMessagingTimeout.call_count,1)
 def test_string_array_expansion_refuses_before_base_conversion(self):
  class Base:
   def value(self,p):raise AssertionError('oversized value reached base converter')
  ax=m.bounded_ax(Base)();ax.c=SimpleNamespace(CFGetTypeID=lambda p:p,CFStringGetTypeID=lambda:1,CFArrayGetTypeID=lambda:2,CFStringGetLength=lambda p:200001,CFArrayGetCount=lambda p:900)
  with self.assertRaisesRegex(RuntimeError,'string exceeds'):ax.value(1)
  with self.assertRaisesRegex(RuntimeError,'array exceeds'):ax.value(2)
 def test_walk_records_attribute_errors_instead_of_silent_absence(self):
  class Base:
   def own(self,e):pass
   def string(self,n):return n
   def walk(self,e):self.last_walk_observation={'unique_nodes':1};self.attr(e,'AXChildren');return []
  ax=m.bounded_ax(Base)();ax.a=SimpleNamespace(AXUIElementSetMessagingTimeout=Mock(return_value=0),AXUIElementCopyAttributeValue=Mock(return_value=-25204))
  self.assertEqual(ax.walk('owned'),[])
  self.assertEqual(ax.last_walk_observation['attribute_errors'],{'AXChildren:-25204':1})
 def test_question_button_must_be_unique_enabled_native(self):
  rows=[(1,prop('AXWindow','Stop Codex'),False),(2,prop('AXStaticText',value=q.question()),False),(3,prop('AXButton','Stop Codex'),False),(4,prop('AXButton','Keep Codex running'),False),(5,prop('AXButton','Cancel'),False)]
  self.assertEqual(m.native_question(rows)[1],3)
  with self.assertRaisesRegex(RuntimeError,'button set'):m.native_question(rows+[rows[-1]])
  with self.assertRaisesRegex(RuntimeError,'input control'):m.native_question(rows+[(6,prop('AXCheckBox'),False)])
  with self.assertRaisesRegex(RuntimeError,'input control'):m.native_question(rows+[(6,prop('AXTextField',value='injected'),False)])
if __name__=='__main__':unittest.main()
