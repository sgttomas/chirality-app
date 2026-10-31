"""Fixed helper command/focus refusal tests, no actual native framework calls."""
import hashlib,importlib.util,json,os,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock,patch
s=importlib.util.spec_from_file_location('window_helper_test',Path(__file__).with_name('native_b_window_helper.py'));h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
class Executed(BaseException):pass
class HelperTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(dir='/Users/ryan/dev/chirality-t3/scratch',prefix='window-helper-fixture-');self.addCleanup(self.tmp.cleanup)
  self.root=Path(self.tmp.name).resolve();(self.root/'helper-tmp').mkdir(mode=0o700);self.exe=self.root/'invented';self.exe.write_bytes(b'not executed')
  self.identity={'pid':123,'ppid':456,'uid':os.getuid(),'ruid':os.getuid(),'start_sec':1,'start_usec':2,'executable':str(self.exe)}
  self.window={'window_id':42,'title':h.w.TITLE,'bounds':{'X':0,'Y':0,'Width':100,'Height':100},'own_visible_layer0_count':1}
  self.admission=self.root/'admission.json';self.admission.write_text(json.dumps({'inputs':{'executable':str(self.exe),'executable_sha256':h.w.sha(self.exe),'window_route':{'helper_sources':{},'tools':{},'python_prefixes':h.w.python_prefixes()}}}))
  self.path=self.root/'window-helper-001.json';self.request={'action':'capture','sequence':1,'identity':self.identity,'window':self.window,'image_name':'capture-001.unverified.png','recorded_at':h.w.d.now(),'admission_sha256':h.w.sha(self.admission)}
  self.backend=SimpleNamespace(identity=lambda pid:self.identity,screen_access=lambda:True,close=Mock())
 def run_request(self,**changes):
  self.request.update(changes);self.path.write_text(json.dumps(self.request));self.path.chmod(0o600)
  with patch.dict(os.environ,{'TMPDIR':str(self.root/'helper-tmp')}):return h.main(self.path,h.w.sha(self.path))
 def patches(self):
  return patch.multiple(h,__file__=str(self.root/'native_b_window_helper.py'))
 def test_exact_window_capture_never_uses_desktop_clipboard_or_interactive_flags(self):
  with self.patches(),patch.object(h.w,'tools_identity',return_value={}),patch.object(h.w.d,'NativeBackend',return_value=self.backend),patch.object(h.w,'select_main',return_value=self.window),patch.object(h.os,'execve',side_effect=Executed) as execute:
   with self.assertRaises(Executed):self.run_request()
  command=execute.call_args.args[1]
  self.assertEqual(command,[str(h.w.CAPTURE),'-x','-a','-o','-t','png','-l','42',str(self.root/'capture-001.unverified.png')])
 def test_permission_refusal_does_not_capture_or_request_permissions(self):
  self.backend.screen_access=lambda:False
  with self.patches(),patch.object(h.w,'tools_identity',return_value={}),patch.object(h.w.d,'NativeBackend',return_value=self.backend),patch.object(h.os,'execve') as execute:
   with self.assertRaisesRegex(RuntimeError,'preflight denied'):self.run_request()
  execute.assert_not_called()
 def test_identity_or_window_change_refuses_before_capture(self):
  with self.patches(),patch.object(h.w,'tools_identity',return_value={}),patch.object(h.w.d,'NativeBackend',return_value=self.backend),patch.object(h.w,'select_main',return_value={**self.window,'window_id':99}),patch.object(h.os,'execve') as execute:
   with self.assertRaisesRegex(RuntimeError,'owned window changed'):self.run_request()
  execute.assert_not_called()
 def test_mismatch_records_exact_owned_facts_and_field_without_capture(self):
  for field,actual in [('window_id',{**self.window,'window_id':99}),('bounds.X',{**self.window,'bounds':{**self.window['bounds'],'X':5}}),('own_visible_layer0_count',{**self.window,'own_visible_layer0_count':2})]:
   path=self.root/'window-helper-001.window-mismatch.json'
   if path.exists():path.unlink() # independent invented test case only
   with self.patches(),patch.object(h.w,'tools_identity',return_value={}),patch.object(h.w.d,'NativeBackend',return_value=self.backend),patch.object(h.w,'select_main',return_value=actual),patch.object(h.os,'execve') as execute:
    with self.assertRaisesRegex(RuntimeError,'owned window changed'):self.run_request()
   execute.assert_not_called();record=json.loads(path.read_text())
   self.assertEqual(record['actual_owned_window'],actual);self.assertEqual(record['expected_window'],self.window)
   self.assertEqual(record['different_fields'],[field]);self.assertEqual(record['comparison'],'initial')
   self.assertEqual(path.stat().st_mode&0o777,0o600);self.assertEqual(path.stat().st_nlink,1)
 def test_second_comparison_failure_is_recorded_before_exec(self):
  actual={**self.window,'window_id':99}
  with self.patches(),patch.object(h.w,'tools_identity',return_value={}),patch.object(h.w.d,'NativeBackend',return_value=self.backend),patch.object(h.w,'select_main',side_effect=[self.window,actual]),patch.object(h.os,'execve') as execute:
   with self.assertRaisesRegex(RuntimeError,'owned window changed'):self.run_request()
  execute.assert_not_called()
  self.assertEqual(json.loads((self.root/'window-helper-001.window-mismatch.json').read_text())['comparison'],'before-capture-exec')
 def test_identity_change_never_selects_or_records_window(self):
  self.backend.identity=lambda pid:{**self.identity,'start_usec':3}
  with self.patches(),patch.object(h.w,'tools_identity',return_value={}),patch.object(h.w.d,'NativeBackend',return_value=self.backend),patch.object(h.w,'select_main') as select,patch.object(h.os,'execve') as execute:
   with self.assertRaisesRegex(RuntimeError,'App identity changed'):self.run_request()
  select.assert_not_called();execute.assert_not_called()
  self.assertFalse((self.root/'window-helper-001.window-mismatch.json').exists())
 def test_equal_json_numeric_serialization_does_not_create_mismatch(self):
  actual=json.loads(json.dumps({**self.window,'window_id':42.0}))
  h.require_same_window(self.root,self.request,actual,'initial')
  self.assertFalse((self.root/'window-helper-001.window-mismatch.json').exists())
 def test_existing_diagnostic_is_not_overwritten_and_failure_still_refuses(self):
  path=self.root/'window-helper-001.window-mismatch.json';path.write_text('preserve')
  with self.assertRaisesRegex(RuntimeError,'mismatch diagnostic unavailable'):
   h.require_same_window(self.root,self.request,{**self.window,'window_id':99},'initial')
  self.assertEqual(path.read_text(),'preserve')
 def test_unsafe_destination_and_nonprivate_control_refuse(self):
  with self.patches(),patch.object(h.w,'tools_identity',return_value={}),patch.object(h.w.d,'NativeBackend',return_value=self.backend),patch.object(h.w,'select_main',return_value=self.window),patch.object(h.os,'execve') as execute:
   with self.assertRaisesRegex(RuntimeError,'destination'):self.run_request(image_name='../foreign.png')
   self.path.chmod(0o644)
   with self.assertRaisesRegex(RuntimeError,'mode'):h.main(self.path,h.w.sha(self.path))
  execute.assert_not_called()
 def test_click_posts_only_to_original_app_and_needs_effect_readback(self):
  events=[]
  self.backend.app=lambda pid:'app';self.backend.owner=lambda app:(0,123)
  self.backend.attribute=lambda app,name:({'return_code':0,'type':{'name':'CFBoolean'},'value':True},[])
  self.backend.a=SimpleNamespace(CGEventCreateMouseEvent=Mock(side_effect=lambda source,kind,point,button: events.append((kind,point.x,point.y)) or 100+kind),
       CGEventPostToPid=Mock(),CGEventSetFlags=Mock(),CGEventSetIntegerValueField=Mock())
  self.backend.c=SimpleNamespace(CFRelease=Mock())
  with self.patches(),patch.object(h.w,'tools_identity',return_value={}),patch.object(h.w.d,'NativeBackend',return_value=self.backend),patch.object(h.w,'select_main',return_value=self.window):
   self.run_request(action='click',point=[20,60])
  self.assertEqual(events,[(1,20,60),(2,20,60)])
  self.assertEqual([call.args[0] for call in self.backend.a.CGEventPostToPid.call_args_list],[123,123])
  self.assertEqual(self.backend.c.CFRelease.call_count,2)
  routes=[call.args for call in self.backend.a.CGEventSetIntegerValueField.call_args_list if call.args[1] in (91,92)]
  self.assertEqual(routes,[(101,91,42),(101,92,42),(102,91,42),(102,92,42)])
  result=json.loads((self.root/'window-helper-001.result.json').read_text())
  self.assertTrue(result['effect_requires_fresh_capture_read'])
  self.assertEqual(result['event_routes'],[{'pid':123,'window_under_pointer':42,'window_that_can_handle_event':42}]*2)
 def test_late_window_change_prevents_annotation_and_post(self):
  self.backend.app=lambda pid:'app';self.backend.owner=lambda app:(0,123)
  self.backend.attribute=lambda app,name:({'return_code':0,'type':{'name':'CFBoolean'},'value':True},[])
  self.backend.a=SimpleNamespace(CGEventCreateMouseEvent=Mock(side_effect=[101,102]),CGEventPostToPid=Mock(),CGEventSetFlags=Mock(),CGEventSetIntegerValueField=Mock())
  self.backend.c=SimpleNamespace(CFRelease=Mock())
  with self.patches(),patch.object(h.w,'tools_identity',return_value={}),patch.object(h.w.d,'NativeBackend',return_value=self.backend),patch.object(h.w,'select_main',side_effect=[self.window,{**self.window,'window_id':99}]):
   with self.assertRaisesRegex(RuntimeError,'owned window changed'):self.run_request(action='click',point=[20,60])
  self.backend.a.CGEventPostToPid.assert_not_called();self.backend.a.CGEventSetIntegerValueField.assert_not_called()
  self.assertEqual(self.backend.c.CFRelease.call_count,2)
 def test_focus_uses_one_owned_activation_then_actual_frontmost_readback(self):
  self.backend.app=lambda pid:'app';self.backend.owner=lambda app:(0,123)
  with self.patches(),patch.object(h.w,'tools_identity',return_value={}),patch.object(h.w.d,'NativeBackend',return_value=self.backend),patch.object(h.w,'select_main',return_value=self.window),patch.object(h.w,'frontmost',side_effect=[False,False,True]),patch.object(h,'activate_original_app',return_value={'request_sent':True,'receiver_pid':123,'options':0}) as activate,patch.object(h.time,'sleep'):
   self.run_request(action='focus')
  activate.assert_called_once_with(123)
  trace=json.loads((self.root/'window-helper-001.focus.json').read_text())
  self.assertEqual([x['frontmost'] for x in trace['observations']],[False,False,True])
  self.assertTrue((self.root/'window-helper-001.result.json').exists())
 def test_focus_dispatch_refusal_retains_trace_and_never_claims_effect(self):
  self.backend.app=lambda pid:'app';self.backend.owner=lambda app:(0,123)
  with self.patches(),patch.object(h.w,'tools_identity',return_value={}),patch.object(h.w.d,'NativeBackend',return_value=self.backend),patch.object(h.w,'select_main',return_value=self.window),patch.object(h.w,'frontmost',return_value=False),patch.object(h,'activate_original_app',return_value={'request_sent':False}) as activate:
   with self.assertRaisesRegex(RuntimeError,'activation request refused'):self.run_request(action='focus')
  activate.assert_called_once_with(123);self.assertFalse((self.root/'window-helper-001.result.json').exists())
  self.assertIn('error',json.loads((self.root/'window-helper-001.focus.json').read_text()))
 def test_focus_sent_but_not_frontmost_refuses_without_second_activation(self):
  self.backend.app=lambda pid:'app';self.backend.owner=lambda app:(0,123)
  with self.patches(),patch.object(h.w,'tools_identity',return_value={}),patch.object(h.w.d,'NativeBackend',return_value=self.backend),patch.object(h.w,'select_main',return_value=self.window),patch.object(h.w,'frontmost',return_value=False),patch.object(h,'activate_original_app',return_value={'request_sent':True}) as activate,patch.object(h.time,'monotonic',side_effect=[0,1]):
   with self.assertRaisesRegex(RuntimeError,'did not become frontmost'):self.run_request(action='focus')
  activate.assert_called_once_with(123);self.assertFalse((self.root/'window-helper-001.result.json').exists())
 def test_window_change_prevents_focus_activation(self):
  self.backend.app=lambda pid:'app';self.backend.owner=lambda app:(0,123)
  with self.patches(),patch.object(h.w,'tools_identity',return_value={}),patch.object(h.w.d,'NativeBackend',return_value=self.backend),patch.object(h.w,'select_main',side_effect=[self.window,{**self.window,'window_id':99}]),patch.object(h.w,'frontmost',return_value=False),patch.object(h,'activate_original_app') as activate:
   with self.assertRaisesRegex(RuntimeError,'owned window changed'):self.run_request(action='focus')
  activate.assert_not_called()
 def test_already_frontmost_does_not_activate(self):
  self.backend.app=lambda pid:'app';self.backend.owner=lambda app:(0,123)
  with self.patches(),patch.object(h.w,'tools_identity',return_value={}),patch.object(h.w.d,'NativeBackend',return_value=self.backend),patch.object(h.w,'select_main',return_value=self.window),patch.object(h.w,'frontmost',return_value=True),patch.object(h,'activate_original_app') as activate:
   self.run_request(action='focus')
  activate.assert_not_called()
 def test_activation_exact_selectors_receiver_and_pool_lifetime_without_native_load(self):
  objc=SimpleNamespace(objc_getClass=Mock(side_effect=lambda x:x),sel_registerName=Mock(side_effect=lambda x:x))
  calls=[];actual=123;policy=0
  def send(receiver,selector,*args):
   calls.append((receiver,selector,args))
   if selector==b'new':return 'pool'
   if selector==b'runningApplicationWithProcessIdentifier:':return 'target'
   if selector==b'processIdentifier':return actual
   if selector==b'activationPolicy':return policy
   if selector==b'activateWithOptions:':return True
  with patch.object(h.C,'CDLL',return_value=objc) as load,patch.object(h.C,'CFUNCTYPE',side_effect=lambda *signature:lambda symbol:send):
   result=h.activate_original_app(123)
   self.assertTrue(result['request_sent'])
   self.assertIn(('target',b'activateWithOptions:',(0,)),calls)
   self.assertEqual(calls[-1],('pool',b'drain',()))
   self.assertEqual([c.args[0] for c in load.call_args_list],['/System/Library/Frameworks/AppKit.framework/AppKit','/usr/lib/libobjc.A.dylib'])
   calls.clear();actual=999
   with self.assertRaisesRegex(RuntimeError,'receiver differs'):h.activate_original_app(123)
   self.assertFalse(any(c[1]==b'activateWithOptions:' for c in calls));self.assertEqual(calls[-1][1],b'drain')
   calls.clear();actual=123;policy=2
   with self.assertRaisesRegex(RuntimeError,'policy prohibits'):h.activate_original_app(123)
   self.assertFalse(any(c[1]==b'activateWithOptions:' for c in calls))
 def test_unfocused_or_foreign_app_never_posts(self):
  self.backend.app=lambda pid:'app';self.backend.owner=lambda app:(0,999)
  with self.patches(),patch.object(h.w,'tools_identity',return_value={}),patch.object(h.w.d,'NativeBackend',return_value=self.backend),patch.object(h.w,'select_main',return_value=self.window):
   with self.assertRaisesRegex(RuntimeError,'AX App ownership'):self.run_request(action='click',point=[20,60])
  self.assertFalse((self.root/'window-helper-001.result.json').exists())
if __name__=='__main__':unittest.main()
