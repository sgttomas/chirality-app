"""Mock keeper/binding tests; optional harmless compiled CF fixture, never live AX."""
import ctypes as C
import hashlib,importlib.util,json,os,tempfile,time,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock,patch
spec=importlib.util.spec_from_file_location('typed_reader_test',Path(__file__).with_name('native_b_typed_ax.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class TypedBinding(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(prefix='typed-binding-test-');self.addCleanup(self.tmp.cleanup)
  self.root=Path(self.tmp.name).resolve();self.exe=self.root/'invented';self.exe.write_bytes(b'not executed')
  self.binding={'version':'chirality.typed-ax-build/v1','manifest':str(self.root/'typed-ax-build.json'),'sha256':'1'*64}
  self.value={'candidate_key':'invented','executable':str(self.exe),'executable_sha256':m.sha(self.exe),'typed_ax_comparison':self.binding}
  policy=self.root/'phase-B.sb';policy.write_text('(deny file-read* file-write* (subpath '+json.dumps(str(self.root))+'))')
  (self.root/'admission.json').write_text(json.dumps({'inputs':self.value,'policy_sha256':m.sha(policy)}))
  self.run=SimpleNamespace(root=self.root,reservation=SimpleNamespace(reaped=False,observe=lambda:None,child=SimpleNamespace(pid=123)),
                           value=self.value,reason=None,log_errors=[],cleanup_end=time.monotonic()+200,admission_sha=m.sha(self.root/'admission.json'))
  self.identity={'pid':123,'ppid':os.getpid(),'uid':os.getuid(),'ruid':os.getuid(),'start_sec':1,'start_usec':2,'executable':str(self.exe)}
  self.backend=SimpleNamespace(identity=lambda pid:self.identity,app=lambda pid:777,owner=lambda ref:(0,123),close=Mock())
  def native(app,out):
   self.assertEqual(app,777);v=C.cast(out,C.POINTER(m.Result)).contents
   v.abi_version=1;v.byte_size=C.sizeof(m.Result);v.application_pid=123;v.application_owner_rc=0;v.completed=1
   return 0
  self.library=SimpleNamespace(chirality_ax_compare_v1=native)
  self.loader=Mock(return_value=(self.library,{'library':{'sha256':'2'*64}}))
 def capture(self):
  with patch.object(m.reference,'ax_inventory',return_value={'attributes':[]}) as reader:
   result=m.capture(self.run,lambda:self.backend,self.loader)
   self.assertEqual(reader.call_args.kwargs['application'],777)
   return result
 def test_same_retained_app_reference_and_independent_sections(self):
  result=self.capture();self.assertEqual(result['typed_c']['application_pid'],123);self.assertIn('python',result)
  self.assertTrue(self.backend.close.called)
 def test_missing_child_stop_or_headroom_refuses_before_backend(self):
  for key,value in [('reservation',None),('reason','exclusive pending'),('cleanup_end',time.monotonic()+5)]:
   old=getattr(self.run,key);setattr(self.run,key,value);factory=Mock()
   with self.assertRaises(RuntimeError):m.capture(self.run,factory,self.loader)
   factory.assert_not_called();setattr(self.run,key,old)
 def test_unbound_or_changed_manifest_admission_refuses(self):
  self.binding['sha256']='3'*64
  with self.assertRaisesRegex(RuntimeError,'admission changed'):self.capture()
  self.loader.assert_not_called()
 def test_changed_identity_after_c_refuses_before_python(self):
  self.backend.identity=Mock(side_effect=[self.identity,dict(self.identity,start_usec=3)])
  with self.assertRaisesRegex(RuntimeError,'across C reader'):self.capture()
 def test_python_refusal_keeps_independent_c_observation(self):
  with patch.object(m.reference,'ax_inventory',side_effect=RuntimeError('AX refusal')):
   result=m.capture(self.run,lambda:self.backend,self.loader)
  self.assertEqual(result['typed_c']['application_pid'],123);self.assertEqual(len(result['python']['attributes']),4);self.assertTrue(all(not a['available'] for a in result['python']['attributes']))
 def test_manifest_hash_or_fixture_standing_refuses_before_loading(self):
  manifest=self.root/'typed-ax-build.json';manifest.write_text(json.dumps({'format':'chirality.typed-ax-build/v1','fixture_build':True}))
  with patch.object(m.C,'CDLL',side_effect=AssertionError('must not load')):
   with self.assertRaisesRegex(RuntimeError,'manifest changed'):m.load(manifest,'0'*64)
   with self.assertRaisesRegex(RuntimeError,'test library'):m.load(manifest,m.sha(manifest))
 def test_checked_library_staged_privately_before_admission_and_never_overwrites(self):
  source=self.root/'source';source.mkdir();lib=source/'reader.dylib';lib.write_bytes(b'invented library never loaded')
  manifest=source/'reader-build.json';manifest.write_text(json.dumps({'format':'chirality.typed-ax-build/v1','fixture_build':False,'sources':{p:m.sha(p) for p in m.production_sources()},'library':{'path':str(lib),'sha256':m.sha(lib)}}))
  target=self.root/'future';target.mkdir(mode=0o700)
  with patch.object(m.C,'CDLL',side_effect=AssertionError('no native load during staging')):
   binding=m.stage_build(target,manifest,m.sha(manifest))
  self.assertEqual(Path(binding['manifest']).parent,target)
  self.assertEqual((target/'typed-ax-reader.dylib').read_bytes(),lib.read_bytes())
  self.assertEqual((target/'typed-ax-reader.dylib').stat().st_mode&0o777,0o600)
  with self.assertRaises(FileExistsError):m.stage_build(target,manifest,m.sha(manifest))
  (target/'admission.json').write_text('{}')
  with self.assertRaisesRegex(RuntimeError,'pre-admission'):m.stage_build(target,manifest,m.sha(manifest))
 def test_unprotected_control_root_refuses_before_backend(self):
  (self.root/'phase-B.sb').write_text('(allow default)')
  factory=Mock()
  with self.assertRaisesRegex(RuntimeError,'sandbox binding'):m.capture(self.run,factory,self.loader)
  factory.assert_not_called()
 def test_result_array_bounds_refuse(self):
  value=m.Result();value.abi_version=1;value.byte_size=C.sizeof(value);value.attribute_count=5
  with self.assertRaisesRegex(RuntimeError,'bounds'):m.decode(value)

 def test_reviewed_manifest_hash_and_exact_source_set_required_before_staging(self):
  source=self.root/'untrusted';source.mkdir();lib=source/'reader.dylib';lib.write_bytes(b'invented')
  manifest=source/'reader-build.json'
  record={'format':'chirality.typed-ax-build/v1','fixture_build':False,'sources':{},'library':{'path':str(lib),'sha256':m.sha(lib)}}
  manifest.write_text(json.dumps(record));target=self.root/'new-root';target.mkdir(mode=0o700)
  with self.assertRaisesRegex(RuntimeError,'reviewed build manifest'):m.stage_build(target,manifest,'0'*64)
  with self.assertRaisesRegex(RuntimeError,'production source set'):m.stage_build(target,manifest,m.sha(manifest))
  self.assertEqual(list(target.iterdir()),[])
 def test_output_exception_keeps_c_header_and_python_attribute_refusals(self):
  with patch.object(m,'decode',side_effect=ValueError('decode refused')),patch.object(m.reference,'ax_inventory',side_effect=ValueError('attribute refused')):
   result=m.capture(self.run,lambda:self.backend,self.loader)
  self.assertEqual(result['typed_c']['application_pid'],123)
  self.assertEqual(result['typed_c']['decode_error'],'decode refused')
  self.assertEqual(len(result['python']['attributes']),4)
 def test_raw_role_decode_never_raises_on_invalid_utf8(self):
  out=m.Result();out.abi_version=1;out.byte_size=C.sizeof(out);out.attribute_count=1
  out.attributes[0].reference_count=1;out.attributes[0].references[0].role=b'bad\xff'
  self.assertIn('\ufffd',m.decode(out)['attributes'][0]['references'][0]['role'])
 def test_exited_reaped_or_log_failure_refuses_before_backend(self):
  for change in ('exited','reaped','logging'):
   factory=Mock();old=self.run.reservation.observe
   if change=='exited':self.run.reservation.observe=lambda:{'code':1,'status':0}
   elif change=='reaped':self.run.reservation.reaped=True
   else:self.run.log_errors=['disk failure']
   with self.assertRaises(RuntimeError):m.capture(self.run,factory,self.loader)
   factory.assert_not_called();self.run.reservation.observe=old;self.run.reservation.reaped=False;self.run.log_errors=[]
 def test_manifest_outside_root_or_output_filename_refuses(self):
  self.binding['manifest']=str(self.root.parent/'typed-ax-build.json')
  admission=json.loads((self.root/'admission.json').read_text());admission['inputs']['typed_ax_comparison']=self.binding
  (self.root/'admission.json').write_text(json.dumps(admission));self.run.admission_sha=m.sha(self.root/'admission.json')
  with self.assertRaisesRegex(RuntimeError,'protected control'):self.capture()
  bad=self.root/'stdout.log';bad.write_text('{}')
  with patch.object(m.C,'CDLL',side_effect=AssertionError('no load')):
   with self.assertRaisesRegex(RuntimeError,'manifest filename'):m.load(bad,m.sha(bad))

@unittest.skipUnless(os.environ.get('TYPED_AX_FIXTURE_BUILD'),'compiled harmless fixture not selected')
class CompiledFixture(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  p=Path(os.environ['TYPED_AX_FIXTURE_BUILD']);record=json.loads(p.read_text());assert record['fixture_build'] is True
  lib=Path(record['library']['path']);assert m.sha(lib)==record['library']['sha256']
  cls.lib=C.CDLL(str(lib),mode=os.RTLD_LOCAL)
  for name,result,args in [('fixture_start',C.c_void_p,[C.c_int]),('fixture_finish',None,[]),('fixture_foreign_role_reads',C.c_int,[]),('fixture_timeout_calls',C.c_int,[]),('fixture_copy_calls',C.c_int,[]),('fixture_app_retain_count',C.c_long,[]),('chirality_ax_compare_size_v1',C.c_uint32,[]),('chirality_ax_compare_v1',C.c_int,[C.c_void_p,C.POINTER(m.Result)])]:
   f=getattr(cls.lib,name);f.restype=result;f.argtypes=args
  assert cls.lib.chirality_ax_compare_size_v1()==C.sizeof(m.Result)
 def inspect(self,mode):
  app=self.lib.fixture_start(mode);before=self.lib.fixture_app_retain_count()
  try:
   result=m.Result();rc=self.lib.chirality_ax_compare_v1(app,C.byref(result))
   self.assertEqual(self.lib.fixture_app_retain_count(),before)
   self.assertEqual(self.lib.fixture_foreign_role_reads(),0)
   self.assertGreater(self.lib.fixture_timeout_calls(),0)
   return rc,m.decode(result)
  finally:self.lib.fixture_finish()
 def test_owned_roles_self_cycle_duplicate_and_foreign_refusal(self):
  rc,result=self.inspect(0);self.assertEqual(rc,0);refs=result['attributes'][0]['references']
  self.assertTrue(refs[0]['application_self_reference']);self.assertEqual(refs[0]['role'],'AXApplication')
  self.assertEqual(refs[1]['role'],'AXWindow');self.assertTrue(refs[2]['duplicate_reference'])
  self.assertEqual(refs[3]['status'],2);self.assertEqual(refs[3]['role'],'');self.assertNotIn('SECRET',str(result));self.assertNotIn('456',str(result))
 def test_raw_errors_wrong_types_reference_bound_and_timeout_refusal(self):
  for mode,status in [(1,6),(2,1),(3,3)]:
   with self.subTest(mode=mode):
    rc,result=self.inspect(mode);self.assertEqual(result['attributes'][0]['status'],status)
    if mode==1:self.assertEqual(result['attributes'][0]['return_code'],-25204)
  rc,result=self.inspect(4);self.assertEqual(result['attributes'][0]['references'][1]['status'],6)
 def test_deadline_wrong_null_or_oversize_role(self):
  rc,result=self.inspect(6);self.assertEqual(rc,4);self.assertFalse(result['completed'])
  for mode,status in [(5,1),(7,1),(8,5)]:
   with self.subTest(mode=mode):
    rc,result=self.inspect(mode);ref=result['attributes'][0]['references'][1]
    self.assertEqual(ref['status'],status);self.assertEqual(ref['role'],'')
 def test_null_reference_is_not_a_pid_interface(self):
  result=m.Result();self.assertEqual(self.lib.chirality_ax_compare_v1(None,C.byref(result)),7)
  self.assertEqual(result.application_owner_rc,-2147483648)

if __name__=='__main__':unittest.main()
