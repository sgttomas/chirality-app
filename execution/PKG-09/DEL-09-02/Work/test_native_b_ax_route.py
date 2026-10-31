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
  self.run=m.make_run(b)(self.root,self.value,time.monotonic()+295,'a'*64);self.run.alive=Mock();self.run.safe_log=Mock();self.run.report=Mock()
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
   if e==100:return [(100,prop('AXWindow','Stop Codex'),False),(101,prop('AXStaticText','Stop Codex'),False),(102,prop('AXStaticText',value=self.question),False),(103,prop('AXButton','Stop Codex'),False)]
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
  with self.assertRaisesRegex(RuntimeError,'WebKit AXWebArea unavailable'):self.run.observe_ready()
  with self.assertRaisesRegex(RuntimeError,'no screenshot-only fallback'):self.run.cleanup_attempt()
  self.run.screen.observe.assert_not_called();self.assertEqual(self.pressed,[])
  self.assertTrue(list(self.root.glob('owned-AX-*.json')))
 def test_wrong_window_number_or_focus_refuses_before_control(self):
  self.run.ax_binding=(self.identity,self.window);self.mapping[2]=99
  with self.assertRaisesRegex(RuntimeError,'does not match'):self.run.open_disclosure('Host diagnostics')
  self.assertEqual(self.pressed,[])
  self.mapping[2]=10;self.front=False
  with self.assertRaisesRegex(RuntimeError,'no longer frontmost'):self.run.bound_main()
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
   with self.assertRaisesRegex(RuntimeError,'unavailable/ambiguous'):m.web_control(rows,'AXButton','Stop Codex…')
 def test_web_question_cannot_be_native_confirmation(self):
  with self.assertRaisesRegex(RuntimeError,'not a native subtree'):m.native_question([(1,prop('AXStaticText',value=self.question),True)])
 def test_record_failure_prevents_control_and_preserves_custody(self):
  self.run.ax_binding=(self.identity,self.window);self.run.record=Mock(side_effect=OSError('fixture disk failure'))
  with self.assertRaises(OSError):self.run.open_disclosure('Host diagnostics')
  self.assertEqual(self.pressed,[]);self.assertTrue(self.run.ax_failed)
 def test_guard_phase_deadline_remains_enforced(self):
  self.run.ui_deadline=time.monotonic()-1
  with patch.object(b.Run,'alive'):
   with self.assertRaisesRegex(RuntimeError,'AX phase deadline'):type(self.run).alive(self.run)

class Bounds(unittest.TestCase):
 def test_per_element_timeout_and_owner_refusal(self):
  class Base:
   def own(self,e):
    if e=='foreign':raise RuntimeError('foreign')
   def attr(self,e,n):return 'value'
  ax=m.bounded_ax(Base)();ax.a=SimpleNamespace(AXUIElementSetMessagingTimeout=Mock(return_value=0))
  self.assertEqual(ax.attr('own','AXRole'),'value');ax.a.AXUIElementSetMessagingTimeout.assert_called_once_with('own',.2)
  with self.assertRaisesRegex(RuntimeError,'foreign'):ax.attr('foreign','AXRole')
  self.assertEqual(ax.a.AXUIElementSetMessagingTimeout.call_count,1)
 def test_string_array_expansion_refuses_before_base_conversion(self):
  class Base:
   def value(self,p):raise AssertionError('oversized value reached base converter')
  ax=m.bounded_ax(Base)();ax.c=SimpleNamespace(CFGetTypeID=lambda p:p,CFStringGetTypeID=lambda:1,CFArrayGetTypeID=lambda:2,CFStringGetLength=lambda p:200001,CFArrayGetCount=lambda p:900)
  with self.assertRaisesRegex(RuntimeError,'string exceeds'):ax.value(1)
  with self.assertRaisesRegex(RuntimeError,'array exceeds'):ax.value(2)
 def test_question_button_must_be_unique_enabled_native(self):
  rows=[(1,prop('AXWindow','Stop Codex'),False),(2,prop('AXStaticText',value=q.question()),False),(3,prop('AXButton','Stop Codex'),False)]
  self.assertEqual(m.native_question(rows)[1],3)
  with self.assertRaisesRegex(RuntimeError,'ambiguous'):m.native_question(rows+[rows[-1]])
if __name__=='__main__':unittest.main()
