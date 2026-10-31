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
  self.root=Path(self.tmp.name).resolve();self.exe=self.root/'invented';self.exe.write_bytes(b'not executed')
  self.identity={'pid':123,'ppid':456,'uid':os.getuid(),'ruid':os.getuid(),'start_sec':1,'start_usec':2,'executable':str(self.exe)}
  self.window={'window_id':42,'title':h.w.TITLE,'bounds':{'X':0,'Y':0,'Width':100,'Height':100},'own_visible_layer0_count':1}
  self.admission=self.root/'admission.json';self.admission.write_text(json.dumps({'inputs':{'executable':str(self.exe),'executable_sha256':h.w.sha(self.exe),'window_route':{'helper_sources':{},'tools':{}}}}))
  self.path=self.root/'window-helper-001.json';self.request={'action':'capture','sequence':1,'identity':self.identity,'window':self.window,'image_name':'capture-001.unverified.png','recorded_at':h.w.d.now(),'admission_sha256':h.w.sha(self.admission)}
  self.backend=SimpleNamespace(identity=lambda pid:self.identity,screen_access=lambda:True,close=Mock())
 def run_request(self,**changes):
  self.request.update(changes);self.path.write_text(json.dumps(self.request));self.path.chmod(0o600)
  return h.main(self.path,h.w.sha(self.path))
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
   self.run_request(action='click',point=[20,40])
  self.assertEqual(events,[(1,20,40),(2,20,40)])
  self.assertEqual([call.args[0] for call in self.backend.a.CGEventPostToPid.call_args_list],[123,123])
  self.assertEqual(self.backend.c.CFRelease.call_count,2)
  result=json.loads((self.root/'window-helper-001.result.json').read_text())
  self.assertTrue(result['effect_requires_fresh_capture_read'])
 def test_unfocused_or_foreign_app_never_posts(self):
  self.backend.app=lambda pid:'app';self.backend.owner=lambda app:(0,999)
  with self.patches(),patch.object(h.w,'tools_identity',return_value={}),patch.object(h.w.d,'NativeBackend',return_value=self.backend),patch.object(h.w,'select_main',return_value=self.window):
   with self.assertRaisesRegex(RuntimeError,'AX App ownership'):self.run_request(action='click',point=[20,40])
  self.assertFalse((self.root/'window-helper-001.result.json').exists())
if __name__=='__main__':unittest.main()
