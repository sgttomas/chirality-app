"""No native API/screenshots: fixed ownership/image/helper boundaries with fixtures."""
import binascii,hashlib,importlib.util,json,os,struct,subprocess,tempfile,time,unittest,zlib
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock,patch
spec=importlib.util.spec_from_file_location('window_test',Path(__file__).with_name('native_b_window.py'));w=importlib.util.module_from_spec(spec);spec.loader.exec_module(w)
def chunk(kind,data):return struct.pack('>I',len(data))+kind+data+struct.pack('>I',binascii.crc32(kind+data)&0xffffffff)
def png(width=200,height=200,metadata=b''):
 return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',width,height,8,2,0,0,0))+chunk(b'tEXt',metadata)+chunk(b'IDAT',zlib.compress(b'invented pixels fixture, not displayed'))+chunk(b'IEND',b'')
class WindowTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory(dir='/Users/ryan/dev/chirality-t3/scratch',prefix='window-fixture-');self.addCleanup(self.temp.cleanup)
  self.root=Path(self.temp.name).resolve();self.window={'window_id':123,'title':w.TITLE,'bounds':{'X':10,'Y':20,'Width':100,'Height':100},'on_screen':True,'layer':0,'own_visible_layer0_count':1}
 def test_foreign_rows_are_not_decoded_and_ambiguous_own_main_refuses(self):
  value={'number':123,'title':w.TITLE,'bounds':self.window['bounds'],'on_screen':True,'layer':0}
  def decode(row,access):
   self.assertEqual(row,'own');return value
  backend=SimpleNamespace(window_rows=lambda:['foreign','own'],owner_pid=lambda r:7 if r=='own' else 999,decode_owned_window=decode)
  self.assertEqual(w.select_main(backend,7),self.window)
  backend.window_rows=lambda:['own','own']
  with self.assertRaisesRegex(RuntimeError,'ambiguous'):w.select_main(backend,7)
 def test_invalid_or_missing_window_id_never_becomes_desktop_capture(self):
  backend=SimpleNamespace(window_rows=lambda:['own'],owner_pid=lambda r:7,decode_owned_window=lambda r,a:{'number':0,'title':w.TITLE,'bounds':self.window['bounds'],'on_screen':True,'layer':0})
  with self.assertRaisesRegex(RuntimeError,'window ID'):w.select_main(backend,7)
 def test_png_geometry_fingerprint_and_current_coordinates(self):
  path=self.root/'image.png';path.write_bytes(png());image=w.png_geometry(path,self.window)
  self.assertEqual(w.point(self.window,image,20,40),[20,40])
  old=image;path.write_bytes(png(metadata=b'creation timestamp differs'));self.assertEqual(w.png_geometry(path,self.window),old)
  path.write_bytes(png(width=201))
  with self.assertRaisesRegex(RuntimeError,'mapping'):w.png_geometry(path,self.window)
  with self.assertRaisesRegex(RuntimeError,'outside'):w.point(self.window,image,-1,20)
 def run_fixture(self):
  return SimpleNamespace(root=self.root,value={'window_route':{'helper_sources':{},'tools':{}}},admission_sha='a'*64,
       cleanup=False,cleanup_end=time.monotonic()+100,work_end=time.monotonic()+90,safe_log=Mock(),alive=Mock(),record=Mock(),report=Mock())
 def test_helper_timeout_targets_only_retained_helper_and_unknown_remains_held(self):
  run=self.run_fixture();route=w.WindowRoute(run);child=Mock(pid=123);child.wait.side_effect=[subprocess.TimeoutExpired('helper',4),subprocess.TimeoutExpired('helper',1)]
  with patch.object(w,'tools_identity',return_value={}),patch.object(w.subprocess,'Popen',return_value=child):
   with self.assertRaisesRegex(RuntimeError,'retain keeper'):route.invoke({'sequence':1})
  child.kill.assert_called_once();self.assertIs(route.helper,child)
  child.wait.side_effect=subprocess.TimeoutExpired('helper',0)
  with self.assertRaisesRegex(RuntimeError,'previous window helper'):route.invoke({'sequence':2})
 def test_helper_has_fixed_protected_script_and_no_shell(self):
  run=self.run_fixture();route=w.WindowRoute(run);child=Mock();child.wait.return_value=0
  with patch.object(w,'tools_identity',return_value={}),patch.object(w.subprocess,'Popen',return_value=child) as popen:
   route.invoke({'sequence':1})
  command=popen.call_args.args[0];self.assertEqual(command[1:4],['-I','-S','-B'])
  self.assertEqual(command[4],str(self.root/w.HELPER.name));self.assertNotIn('shell',popen.call_args.kwargs)
  self.assertIsNone(route.helper)
 def test_capture_permission_failure_does_not_start_helper(self):
  run=self.run_fixture();route=w.WindowRoute(run);backend=SimpleNamespace(screen_access=lambda:False,close=Mock())
  with patch.object(w.d,'NativeBackend',return_value=backend),patch.object(route,'invoke') as invoke:
   with self.assertRaisesRegex(RuntimeError,'preflight false'):route.capture()
  invoke.assert_not_called();backend.close.assert_called_once()
 def test_geometry_or_image_drift_prevents_input_event(self):
  run=self.run_fixture();route=w.WindowRoute(run);frame={'at':w.d.now(),'image':{'image_data_sha256':'old'},'window':self.window};route.last=frame
  with patch.object(route,'capture',return_value={**frame,'image':{'image_data_sha256':'new'}}),patch.object(route,'invoke') as invoke:
   with self.assertRaises(w.Reobserve):route.input('click',frame,[1,2])
  invoke.assert_not_called()
 def test_capture_post_binding_failure_quarantines_pixels_without_publishing(self):
  run=self.run_fixture();route=w.WindowRoute(run);identity={'pid':123}
  backend=SimpleNamespace(screen_access=lambda:True,close=Mock())
  def capture_helper(request):(self.root/request['image_name']).write_bytes(png())
  with patch.object(w.d,'NativeBackend',return_value=backend),patch.object(route,'bound_window',side_effect=[(identity,self.window),(identity,{**self.window,'window_id':999})]),patch.object(route,'invoke',side_effect=capture_helper):
   with self.assertRaisesRegex(RuntimeError,'quarantine'):route.capture()
  self.assertTrue((self.root/'capture-001.unverified.png').exists());self.assertFalse((self.root/'window-001.png').exists());self.assertEqual(route.frames,{})
  run.report.assert_not_called()
 def test_unfocused_input_never_posts_an_event(self):
  run=self.run_fixture();route=w.WindowRoute(run);identity={'pid':123}
  frame={'at':w.d.now(),'identity':identity,'window':self.window,'image':{'width':200,'height':200,'scale':2,'image_data_sha256':'x'},'sha256':'x'};route.last=frame
  backend=SimpleNamespace(app=lambda pid:'app',owner=lambda app:(0,123),close=Mock())
  with patch.object(route,'capture',return_value=frame),patch.object(w.d,'NativeBackend',return_value=backend),patch.object(route,'bound_window',return_value=(identity,self.window)),patch.object(w,'frontmost',return_value=False),patch.object(route,'invoke') as invoke:
   with self.assertRaisesRegex(RuntimeError,'focus unavailable'):route.input('click',frame,[10,20])
  invoke.assert_not_called()
 def test_external_helper_failure_does_not_reap_original_app_fixture(self):
  original=subprocess.Popen([__import__('sys').executable,'-I','-S','-c','import time;time.sleep(0.3)'],stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  try:
   run=self.run_fixture();run.reservation=SimpleNamespace(child=original)
   (self.root/w.HELPER.name).write_text('raise SystemExit(7)')
   route=w.WindowRoute(run)
   with patch.object(w,'tools_identity',return_value={}):
    with self.assertRaisesRegex(RuntimeError,'helper refused'):route.invoke({'sequence':1})
   self.assertIs(run.reservation.child,original);self.assertIsNone(original.returncode)
   os.waitid(os.P_PID,original.pid,os.WEXITED|os.WNOHANG|os.WNOWAIT)
   self.assertIsNone(original.returncode,'helper completion did not reap original Child')
  finally:original.wait(timeout=3)
if __name__=='__main__':unittest.main()
