"""Diagnostic process boundary fixtures: no App/native library/framework calls."""
import ctypes as C
import json,os,tempfile,subprocess
from pathlib import Path
from types import SimpleNamespace as N
from unittest.mock import patch
import unittest
import native_ax_comparison as control
import native_ax_comparison_helper as helper
import native_b_typed_ax, native_b_window
helper.typed=native_b_typed_ax;helper.w=native_b_window # explicit offline dependency injection; no native construction
from native_attended_admission import NativeAdmissions
from native_attended_entry import original_custody

class NativeFault(BaseException):pass

class HelperTests(unittest.TestCase):
    def fixture(self,root):
        root=root.resolve();exe=root/'invented-app';exe.write_text('invented only')
        identity={'pid':10,'ppid':123,'birth':'original','executable':str(exe)}
        binding={'action':helper.ACTION,'manifest':str(root/'typed-ax-build.json'),'sha256':'m'*64}
        value={'executable':str(exe),'executable_sha256':helper.w.sha(exe),'typed_ax_comparison':binding}
        request={'identity':identity,'admission_sha256':'a'*64};(root/'typed-ax-request.json').write_text(json.dumps(request))
        app=object();seen=[]
        backend=N(identity=lambda pid:dict(identity),app=lambda pid:app,owner=lambda e:(0,10),close=lambda:seen.append('closed'))
        def native(ref,out):
            self.assertIs(ref,app);seen.append('C');v=out._obj
            v.abi_version=1;v.byte_size=C.sizeof(helper.typed.Result);v.attribute_count=4;v.completed=1
            v.application_pid=10;v.application_owner_rc=0;return 0
        library=N(chirality_ax_compare_v1=native)
        loader=lambda *a:(library,{'library':{'sha256':'l'*64}})
        def python(backend,pid,check,application,attributes):
            self.assertIs(application,app);self.assertTrue((root/'typed-ax-c.json').exists());check();seen.append('Python')
            return {'attributes':[{'attribute':attributes[0],'return_code':0,'references':[]}]}
        return root,request,value,backend,library,loader,python,seen
    def test_same_local_reference_and_durable_C_before_Python(self):
        with tempfile.TemporaryDirectory() as d:
            root,request,value,b,lib,load,py,seen=self.fixture(Path(d))
            with patch.object(helper.os,'getppid',return_value=123),patch.object(helper.typed.reference,'ax_inventory',side_effect=py):
                result=helper.compare(root,request,value,123,lambda:b,load,clock=lambda:0)
            self.assertEqual(seen,['C']+['Python']*4+['closed'])
            self.assertFalse(result['readiness_promoted']);self.assertFalse(result['qualification_success'])
    def test_C_or_Python_crash_preserves_only_actual_partial_results(self):
        for stage in ('C','Python'):
            with self.subTest(stage=stage),tempfile.TemporaryDirectory() as d:
                root,request,value,b,lib,load,py,seen=self.fixture(Path(d))
                def crash(*a,**kw):raise NativeFault(stage)
                if stage=='C':lib.chirality_ax_compare_v1=crash
                else:py=crash
                with patch.object(helper.os,'getppid',return_value=123),patch.object(helper.typed.reference,'ax_inventory',side_effect=py),self.assertRaises(NativeFault):
                    helper.compare(root,request,value,123,lambda:b,load,clock=lambda:0)
                self.assertEqual((root/'typed-ax-c.json').exists(),stage=='Python')
                self.assertFalse((root/'typed-ax-result.json').exists());self.assertIn('closed',seen)
    def test_parent_birth_and_executable_drift_refuse_before_FFI(self):
        for case in ('parent','birth','executable'):
            with self.subTest(case=case),tempfile.TemporaryDirectory() as d:
                root,request,value,b,lib,load,py,seen=self.fixture(Path(d))
                if case=='birth':b.identity=lambda pid:{'pid':10,'ppid':123,'birth':'replacement'}
                if case=='executable':Path(value['executable']).write_text('changed')
                with patch.object(helper.os,'getppid',return_value=999 if case=='parent' else 123),self.assertRaises(RuntimeError):
                    helper.compare(root,request,value,123,lambda:b,load,clock=lambda:0)
                self.assertNotIn('C',seen);self.assertNotIn('Python',seen)

class AdmissionTests(unittest.TestCase):
    def test_production_emitter_to_actual_helper_decoder(self):
        with tempfile.TemporaryDirectory() as d:
            base=Path(d).resolve();root=base/'A';root.mkdir(mode=0o700);(root/'helper-tmp').mkdir()
            for name in control.SOURCES:
                p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('invented fixture source');p.chmod(0o600)
            manifest=root/'typed-ax-build.json';manifest.write_text('{}');manifest.chmod(0o600)
            binding={'action':helper.ACTION,'helper_seconds':10,'helper_reap_seconds':1,
                     'manifest':str(manifest),'sha256':helper.w.sha(manifest),
                     'helper_sources':{name:helper.w.sha(root/name) for name in control.SOURCES}}
            policy='(deny file-read* file-write* (subpath '+json.dumps(str(base))+'))\n';(root/'phase.sb').write_text(policy);(root/'phase.sb').chmod(0o600)
            a=NativeAdmissions.__new__(NativeAdmissions);a.root=base;a.plan={'candidate':'invented'};a.plan_sha='p'*64
            a.value={'typed_ax_comparison':binding,'executable':'/invented/App'};a.receipts={}
            a.policy=lambda *args:policy
            def write(path,value):path.write_text(json.dumps(value));path.chmod(0o600)
            a.b=N(write_once=write);receipt=a._receipt('A',{'diagnostic_only':True,'launch_limit':1,'setup_allowed':False,'focus_allowed':False,'Stop_allowed':False})
            request={'action':helper.ACTION,'candidate':'invented','binding':binding,'keeper_pid':123,
                     'identity':{'pid':10,'ppid':123,'executable':'/invented/App'},'admission_sha256':receipt['admission_sha256'],
                     'recorded_at':helper.w.d.now()}
            path=root/'typed-ax-request.json';write(path,request)
            with patch.object(helper,'__file__',str(root/'native_ax_comparison_helper.py')),patch.object(helper.os,'getppid',return_value=123),patch.dict(os.environ,{'TMPDIR':str(root/'helper-tmp')}):
                self.assertEqual(helper.admitted(path,helper.w.sha(path))[3],123)
                request['keeper_pid']=999;write(path,request)
                with self.assertRaisesRegex(RuntimeError,'parent mismatch'):helper.admitted(path,helper.w.sha(path))
                request['keeper_pid']=123;request['binding']={**binding,'helper_seconds':20};write(path,request)
                with self.assertRaisesRegex(RuntimeError,'action differs'):helper.admitted(path,helper.w.sha(path))

class SupervisorTests(unittest.TestCase):
    def fixture(self,root,mode):
        root=root.resolve();events=[]
        for name in control.SOURCES:
            p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('invented');p.chmod(0o600)
        library=root/'typed-ax-reader.dylib';library.write_text('not a library');library.chmod(0o600)
        manifest=root/'typed-ax-build.json';manifest.write_text(json.dumps({'library':{'path':str(library),'sha256':helper.w.sha(library)}}));manifest.chmod(0o600)
        binding={'action':control.ACTION,'helper_seconds':10,'helper_reap_seconds':1,'manifest':str(manifest),'sha256':helper.w.sha(manifest),
                 'helper_sources':{name:helper.w.sha(root/name) for name in control.SOURCES}}
        value={'candidate_key':'invented','typed_ax_comparison':binding}
        admission=root/'admission.json';admission.write_text(json.dumps({'inputs':value}));admission.chmod(0o600)
        def record(name,value):
            with (root/name).open('x') as f:json.dump(value,f)
            (root/name).chmod(0o600)
        run=N(root=root,value=value,admission_sha=helper.w.sha(admission),act_record=record,
              extra_cleanup_ready=lambda:True,safe_log=lambda *a,**kw:events.append(a[0]),
              reservation=N(reaped=False,child=N(pid=10),administrative_reap=lambda *a:(_ for _ in ()).throw(AssertionError('never reap App here'))),
              thread=N(is_alive=lambda:True))
        identity={'pid':10,'ppid':os.getpid(),'birth':'original'};original_checks=[]
        def original(label):
            original_checks.append(label)
            if mode=='identity' and len(original_checks)>1:raise RuntimeError('original changed')
        ports=N(_original=original,admissions=N(births={'A':identity}),runs={'A':run},pending_launch=None)
        class Child:
            pid=999
            def __init__(self):self.waits=0;self.ready=False
            def wait(self,timeout):
                self.waits+=1
                if mode=='unknown-helper' and not self.ready:raise subprocess.TimeoutExpired('invented',timeout)
                if mode=='timeout' and self.waits==1:raise subprocess.TimeoutExpired('invented',timeout)
                if mode in ('C-crash','Python-crash'):return -11 if mode=='C-crash' else 1
                if mode in ('timeout','unknown-helper'):return -9
                record('typed-ax-c.json',{'action':control.ACTION,'identity':identity,'admission_sha256':run.admission_sha,'library_sha256':helper.w.sha(library)});record('typed-ax-python.json',{'invented':True})
                record('typed-ax-result.json',{'action':control.ACTION,'identity_before':identity,'identity_after':identity,
                    'admission_sha256':run.admission_sha,'request_sha256':helper.w.sha(root/'typed-ax-request.json'),
                    'c_sha256':helper.w.sha(root/'typed-ax-c.json'),'python_sha256':helper.w.sha(root/'typed-ax-python.json'),
                    'readiness_promoted':False,'qualification_success':False})
                return 0
            def kill(self):events.append('kill-only-helper')
        child=Child()
        def popen(argv,**kw):
            events.append('spawn-only-helper');self.assertEqual(argv[1:4],['-I','-B','-S'])
            self.assertEqual(argv[4],'-c');self.assertIn(str(root/'native_ax_comparison_helper.py'),argv[5]);return child
        return run,ports,child,events,popen
    def test_supervised_crash_timeout_and_identity_never_load_FFI_or_reap_App(self):
        for mode in ('normal','C-crash','Python-crash','timeout','identity','unknown-helper'):
            with self.subTest(mode=mode),tempfile.TemporaryDirectory() as d:
                run,ports,child,events,popen=self.fixture(Path(d),mode)
                supervisor=control.DiagnosticHelper(ports,run,clock=lambda:0,popen=popen)
                with patch.object(helper.typed,'load',side_effect=AssertionError('keeper must not load FFI')):
                    if mode=='normal':self.assertFalse(supervisor.invoke(295)['qualification_success'])
                    else:
                        with self.assertRaises(RuntimeError):supervisor.invoke(295)
                if mode=='unknown-helper':
                    self.assertFalse(run.extra_cleanup_ready());self.assertIn(('A','helper-unknown'),original_custody(ports))
                    child.ready=True;self.assertTrue(run.extra_cleanup_ready())
                else:self.assertTrue(run.extra_cleanup_ready())
                self.assertFalse(run.reservation.reaped)
                with self.assertRaises(RuntimeError):supervisor.invoke(295)
                self.assertEqual(events.count('spawn-only-helper'),1)
                self.assertEqual(events.count('kill-only-helper'),int(mode in ('timeout','unknown-helper')))
    def test_source_drift_refuses_before_helper_spawn(self):
        with tempfile.TemporaryDirectory() as d:
            run,ports,child,events,popen=self.fixture(Path(d),'normal')
            (run.root/'native_ax_comparison_helper.py').write_text('changed')
            supervisor=control.DiagnosticHelper(ports,run,clock=lambda:0,popen=popen)
            with self.assertRaisesRegex(RuntimeError,'source changed'):supervisor.invoke(295)
            self.assertNotIn('spawn-only-helper',events);self.assertTrue(run.extra_cleanup_ready())

class DiagnosticSequenceTests(unittest.TestCase):
    def exercise(self,mode='normal'):
        events=[];records={};run=N(extra_cleanup_ready=lambda:True)
        ports=N(runs={},record=lambda name,value:records.__setitem__(name,value),
                admit_empty_namespace=lambda end:events.append('admit-A') or {'admission':'invented'},
                retain_and_report=lambda *a:events.append('retain'))
        def launch(label,receipt,end):events.append('launch-'+label);ports.runs[label]=run
        ports.launch=launch
        def quit(label,end):
            events.append('Quit-'+label)
            if mode=='unknown-helper':raise RuntimeError('unsettled diagnostic helper')
            return {'incarnation':'A','normal_exit':0,'helpers_settled':True,'reaped':True,'released':True,
                    'release_id':'invented-release','helper_custody_id':'invented-helper'}
        ports.quit_normal=quit
        class FakeHelper:
            def __init__(self,*a):pass
            def invoke(self,end):
                events.append('compare')
                if mode!='normal':raise RuntimeError(mode)
                return {'comparison_recorded':True,'readiness_promoted':False}
        sequence=control.DiagnosticSequence(ports,clock=lambda:0)
        with patch.object(control,'DiagnosticHelper',FakeHelper):result=sequence.run(0)
        self.assertEqual(events[:3],['admit-A','launch-A','compare']);self.assertEqual(events.count('Quit-A'),1)
        self.assertFalse(result['witness_complete']);self.assertFalse(result['qualification_success']);self.assertFalse(result['Stop_confirmed'])
        self.assertEqual(result['custody_held'],mode=='unknown-helper')
        self.assertEqual(result['diagnostic_complete'],mode=='normal')
        return result
    def test_minimal_diagnostic_entry_all_outcomes(self):
        for mode in ('normal','C-crash','Python-crash','timeout','identity','unknown-helper'):
            with self.subTest(mode=mode):self.exercise(mode)

class StagingTests(unittest.TestCase):
    def test_isolated_stage_relocates_exact_reviewed_sources_without_loading_library(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d).resolve();build=root/'build';build.mkdir();phase=root/'A';phase.mkdir(mode=0o700)
            library=build/'reader.dylib';library.write_bytes(b'invented-not-loaded')
            manifest={'format':'chirality.typed-ax-build/v1','fixture_build':False,
                      'sources':{p:helper.w.sha(Path(p)) for p in helper.typed.production_sources()},
                      'library':{'path':str(library),'sha256':helper.w.sha(library)}}
            path=build/'reader-build.json';path.write_text(json.dumps(manifest))
            with patch.object(helper.typed.C,'CDLL',side_effect=AssertionError('no FFI in stage')):
                binding=control.stage(phase,path,helper.w.sha(path))
            staged=json.loads((phase/'typed-ax-build.json').read_text())
            self.assertEqual(staged['original_source_bindings'],manifest['sources'])
            self.assertEqual(set(binding['helper_sources']),control.SOURCES)
            with patch.object(helper.typed,'HERE',phase/'native_b_typed_ax.py'):
                helper.typed.source_binding(staged)
            self.assertEqual((phase/'typed-ax-reader.dylib').read_bytes(),library.read_bytes())

class ActualDisposableProcessTests(unittest.TestCase):
    def test_abrupt_helper_exit_leaves_keeper_and_original_handle_intact(self):
        import sys
        with tempfile.TemporaryDirectory() as d:
            run,ports,child,events,unused=SupervisorTests().fixture(Path(d),'normal')
            keeper=os.getpid()
            def actual_child(argv,**kw):
                # Fault-only disposable Python process, no App/native imports.
                return subprocess.Popen([sys.executable,'-I','-B','-S','-c','import os; os._exit(17)'],**kw)
            supervisor=control.DiagnosticHelper(ports,run,popen=actual_child)
            with self.assertRaisesRegex(RuntimeError,'helper failed'):supervisor.invoke(supervisor.clock()+295)
            self.assertEqual(os.getpid(),keeper);self.assertFalse(run.reservation.reaped)
            self.assertEqual(supervisor.returncode,17);self.assertTrue(run.extra_cleanup_ready())

class UnknownSpawnTests(unittest.TestCase):
    def test_unknown_spawn_outcome_blocks_cleanup_and_original_reap(self):
        with tempfile.TemporaryDirectory() as d:
            run,ports,child,events,popen=SupervisorTests().fixture(Path(d),'normal')
            def unknown(*a,**kw):raise OSError('spawn outcome unavailable')
            supervisor=control.DiagnosticHelper(ports,run,clock=lambda:0,popen=unknown)
            with self.assertRaises(OSError):supervisor.invoke(295)
            self.assertTrue(supervisor.pending);self.assertFalse(run.extra_cleanup_ready())
            self.assertIn(('A','helper-unknown'),original_custody(ports));self.assertFalse(run.reservation.reaped)
            with self.assertRaises(RuntimeError):supervisor.invoke(295)

class DiagnosticEntryTests(unittest.TestCase):
    def exercise(self,mode='normal'):
        import contextlib,io
        from native_attended_entry import run_sequence
        from native_attended_bridge import ReceiptBridge,read,delivery_receipt
        from test_native_attended_entry import SimulatedPorts
        with tempfile.TemporaryDirectory() as d:
            root=Path(d).resolve();root.chmod(0o700);(root/'bridge').mkdir(mode=0o700)
            now=[0];clock=lambda:now[0];handled=set();settled=[mode!='unknown-helper']
            bridge=ReceiptBridge(root,'invented','invented-run',N(receipts={}),clock=clock,simulation=True)
            ports=SimulatedPorts(root,bridge)
            ports.retain_and_report=lambda label,end,failure=None:ports.events.append('held')
            if mode=='unknown-helper':ports.fail='quitA'
            class FakeHelper:
                def __init__(self,p,run,*a):run.extra_cleanup_ready=lambda:settled[0]
                def invoke(self,end):
                    if mode!='normal':raise RuntimeError(mode)
                    return {'comparison_recorded':True,'readiness_promoted':False}
            def tick(delay):
                now[0]+=delay
                for event in (root/'bridge').glob('*.event.json'):
                    eid=event.name[:4]
                    if eid in handled:continue
                    v=read(event);handled.add(eid)
                    delivery_receipt(root,eid,{'run_id':'invented-run','event_id':eid,'parent_thread':v['parent_thread'],
                        'transport':'t3_thread_send','message_id':'invented-delivery','accepted':True,'simulation':True})
                if mode=='unknown-helper' and 'A' in ports.runs:
                    if not settled[0]:self.assertFalse(ports.runs['A'].reservation.reaped)
                    if now[0]>1:settled[0]=True;ports.runs['A'].reservation.exited=True
                if now[0]>20:raise AssertionError('diagnostic simulated custody did not close')
            bridge.sleep=tick
            with patch.object(control,'DiagnosticHelper',FakeHelper),contextlib.redirect_stdout(io.StringIO()):
                result=run_sequence(ports,bridge,0,clock=clock,sleep=tick,diagnostic=True)
            self.assertTrue(result['resource_custody_closed']);self.assertFalse(original_custody(ports))
            self.assertEqual(result['incarnations'],['A']);self.assertFalse(result['witness_complete'])
            self.assertFalse(result['qualification_success']);self.assertFalse(result['Stop_confirmed'])
            self.assertEqual(result['diagnostic_complete'],mode=='normal');self.assertFalse(bridge.offers)
            return result
    def test_full_entry_and_held_helper_supervision(self):
        for mode in ('normal','C-crash','Python-crash','timeout','identity','unknown-helper'):
            with self.subTest(mode=mode):self.exercise(mode)

class DiagnosticAuthorityTests(unittest.TestCase):
    def test_broader_launch_and_ui_ports_refuse_before_native_calls(self):
        from native_attended_ports import NativePorts
        value={'typed_ax_comparison':{'action':control.ACTION}}
        ports=NativePorts(N(),'/invented',value,N(value=value),lambda e:None,lambda *a:None)
        for label,receipt in [('B',{'diagnostic_only':True,'launch_limit':1,'setup_allowed':False,'focus_allowed':False,'Stop_allowed':False}),('A',{'diagnostic_only':True,'launch_limit':2})]:
            with self.assertRaises(RuntimeError):ports.launch(label,receipt,295)
        for operation in (lambda:ports.autonomous_start('A',None,None,295),lambda:ports.ordinary_setup_save('A',295),
                          lambda:ports.observe_ready('A',295),lambda:ports.post_stop_once('A',{},295)):
            with self.assertRaises(RuntimeError):operation()

class ReviewRepairTests(unittest.TestCase):
    def test_real_writer_under_umask022_admits_request_and_early_cleanup(self):
        from native_successor_setup import write_once
        from test_native_attended_early_quit import EarlyQuitTests
        with tempfile.TemporaryDirectory() as d:
            root=Path(d).resolve();run,ports,child,events,popen=SupervisorTests().fixture(root,'normal')
            admitted=json.loads((root/'admission.json').read_text());(root/'admission.json').unlink()
            old=os.umask(0o022)
            try:
                write_once(root/'admission.json',admitted)
                run.admission_sha=helper.w.sha(root/'admission.json')
                run.act_record=lambda name,value:write_once(root/name,value)
                supervisor=control.DiagnosticHelper(ports,run,clock=lambda:0,popen=popen)
                supervisor.invoke(295)
            finally:os.umask(old)
            for name in ('admission.json','typed-ax-request.json'):
                self.assertEqual((root/name).stat().st_mode&0o777,0o600)
                helper.w.private_json(root/name,2*1024*1024)
        with tempfile.TemporaryDirectory() as d:
            p,r,adapter,events,reads,presses,closed=EarlyQuitTests().fixture(Path(d))
            admitted=json.loads((r.root/'admission.json').read_text());(r.root/'admission.json').unlink()
            old=os.umask(0o022)
            try:write_once(r.root/'admission.json',admitted)
            finally:os.umask(old)
            r.admission_sha=helper.w.sha(r.root/'admission.json');p.admissions.receipts['A']['admission_sha256']=r.admission_sha
            with patch('native_attended_ports.NativeAdapter',adapter):self.assertTrue(p.quit_normal('A',295)['released'])
            self.assertEqual(presses,['quit'])
    def test_last_Python_attribute_overrun_preserves_partial_but_no_final_record(self):
        with tempfile.TemporaryDirectory() as d:
            root,req,value,b,lib,load,py,seen=HelperTests().fixture(Path(d));now=[0];calls=[0]
            def late(*args,**kwargs):
                calls[0]+=1
                if calls[0]==4:now[0]=5;raise RuntimeError('late final attribute')
                return py(*args,**kwargs)
            with patch.object(helper.os,'getppid',return_value=123),patch.object(helper.typed.reference,'ax_inventory',side_effect=late),self.assertRaisesRegex(RuntimeError,'Python comparison deadline'):
                helper.compare(root,req,value,123,lambda:b,load,clock=lambda:now[0])
            self.assertTrue((root/'typed-ax-c.json').exists());self.assertTrue((root/'typed-ax-python-4.json').exists())
            self.assertFalse((root/'typed-ax-result.json').exists())
    def test_pre_spawn_refusal_has_no_false_held_or_Quit_report(self):
        calls=[];ports=N(runs={},pending_launch=None,record=lambda *a:None,
                         admit_empty_namespace=lambda end:{},launch=lambda *a:(_ for _ in ()).throw(RuntimeError('admission refused')),
                         quit_normal=lambda *a:calls.append('Quit'),retain_and_report=lambda *a:calls.append('held'))
        result=control.DiagnosticSequence(ports,clock=lambda:0).run(0)
        self.assertEqual(calls,[]);self.assertFalse(result['custody_held']);self.assertTrue(result['launch_not_started'])
    def test_actual_CPython_missing_executable_is_known_settled_failure(self):
        with tempfile.TemporaryDirectory() as d:
            run,ports,child,events,popen=SupervisorTests().fixture(Path(d),'normal')
            supervisor=control.DiagnosticHelper(ports,run,clock=lambda:0)
            with patch.object(control.sys,'executable',str(run.root/'missing-interpreter')):
                with self.assertRaises(FileNotFoundError):supervisor.invoke(295)
            self.assertFalse(supervisor.pending);self.assertTrue(run.extra_cleanup_ready());self.assertFalse(run.reservation.reaped)
            self.assertTrue((run.root/'typed-ax-helper-not-started.json').exists())

class VerifiedBootstrapTests(unittest.TestCase):
    def test_isolated_bootstrap_ignores_unlisted_stdlib_shadow_and_executes_verified_bytes(self):
        import sys
        from native_successor_setup import write_once
        with tempfile.TemporaryDirectory() as d:
            base=Path(d).resolve();root=base/'A';root.mkdir(mode=0o700);build=base/'build';build.mkdir()
            lib=build/'reader.dylib';lib.write_bytes(b'not loaded')
            manifest={'format':'chirality.typed-ax-build/v1','fixture_build':False,
                      'sources':{p:helper.w.sha(Path(p)) for p in helper.typed.production_sources()},
                      'library':{'path':str(lib),'sha256':helper.w.sha(lib)}}
            path=build/'reader-build.json';path.write_text(json.dumps(manifest))
            binding=control.stage(root,path,helper.w.sha(path));(root/'helper-tmp').mkdir()
            policy='(deny file-read* file-write* (subpath '+json.dumps(str(base))+'))\n'
            (root/'phase.sb').write_text(policy);(root/'phase.sb').chmod(0o600)
            a=NativeAdmissions.__new__(NativeAdmissions);a.root=base;a.plan={'candidate':'invented'};a.plan_sha='p'*64
            a.value={'typed_ax_comparison':binding,'executable':'/invented/App'};a.receipts={};a.policy=lambda *args:policy;a.b=N(write_once=write_once)
            old=os.umask(0o022)
            try:receipt=a._receipt('A',{'diagnostic_only':True,'launch_limit':1,'setup_allowed':False,'focus_allowed':False,'Stop_allowed':False})
            finally:os.umask(old)
            # No staged module may be imported by name before source verification.
            (root/'datetime.py').write_text("raise AssertionError('shadow imported')")
            script='''import os,sys,json,hashlib
from pathlib import Path
root=Path(sys.argv[1]);entry=root/'native_ax_comparison_helper.py'
namespace={'__file__':str(entry),'__name__':'offline_bootstrap'}
exec(compile(entry.read_bytes(),str(entry),'exec'),namespace)
admission=json.loads((root/'admission.json').read_text())
request={'action':'same-original-ax-reference/v1','candidate':'invented','binding':admission['inputs']['typed_ax_comparison'],
'identity':{'pid':10,'ppid':os.getppid(),'executable':'/invented/App'},'keeper_pid':os.getppid(),
'admission_sha256':hashlib.sha256((root/'admission.json').read_bytes()).hexdigest(),
'recorded_at':namespace['datetime'].datetime.now(namespace['datetime'].timezone.utc).isoformat()}
namespace['publish'](root/'typed-ax-request.json',request)
digest=hashlib.sha256((root/'typed-ax-request.json').read_bytes()).hexdigest()
r,req,v,p,buffers=namespace['admitted'](root/'typed-ax-request.json',digest,with_sources=True)
(root/'native_b_diagnostic.py').write_text("raise AssertionError('unverified replacement executed')")
typed,window=namespace['verified_modules'](r,buffers)
assert typed.reference is window.d
assert str(root) not in sys.path
print('VERIFIED_BYTES_NO_NATIVE')
'''
            result=subprocess.run([sys.executable,'-I','-B','-S','-c',script,str(root)],env={**os.environ,'TMPDIR':str(root/'helper-tmp')},capture_output=True,text=True,timeout=5)
            self.assertEqual(result.returncode,0,result.stderr);self.assertIn('VERIFIED_BYTES_NO_NATIVE',result.stdout)

class FollowupRepairTests(unittest.TestCase):
    def test_registered_but_unspawned_run_does_not_request_Quit_or_report_App_held(self):
        calls=[];ports=N(runs={},pending_launch=None,record=lambda *a:None,admit_empty_namespace=lambda end:{},
                         quit_normal=lambda *a:calls.append('Quit'),retain_and_report=lambda *a:calls.append('held'))
        def refused(*args):ports.runs['A']=N(reservation=None,thread=None);raise RuntimeError('sample refused')
        ports.launch=refused
        result=control.DiagnosticSequence(ports,clock=lambda:0).run(0)
        self.assertEqual(calls,[]);self.assertFalse(result['custody_held']);self.assertTrue(result['launch_not_started'])
    def test_forged_custom_ENOENT_stays_unknown(self):
        import errno
        with tempfile.TemporaryDirectory() as d:
            run,ports,child,events,unused=SupervisorTests().fixture(Path(d),'normal')
            def forged(argv,**kw):raise FileNotFoundError(errno.ENOENT,'invented',argv[0])
            supervisor=control.DiagnosticHelper(ports,run,clock=lambda:0,popen=forged)
            with self.assertRaises(FileNotFoundError):supervisor.invoke(295)
            self.assertTrue(supervisor.pending);self.assertFalse(run.extra_cleanup_ready());self.assertFalse(run.reservation.reaped)
    def test_known_exec_receipt_failure_preserves_original_errno(self):
        import errno
        with tempfile.TemporaryDirectory() as d:
            run,ports,child,events,unused=SupervisorTests().fixture(Path(d),'normal');record=run.act_record
            def fail(name,value):
                if name=='typed-ax-helper-not-started.json':raise OSError(errno.EIO,'receipt failure')
                record(name,value)
            run.act_record=fail;supervisor=control.DiagnosticHelper(ports,run,clock=lambda:0)
            with patch.object(control.sys,'executable',str(run.root/'missing-interpreter')):
                with self.assertRaisesRegex(RuntimeError,'exec failure errno=2; receipt failed'):supervisor.invoke(295)
            self.assertFalse(supervisor.pending);self.assertTrue(run.extra_cleanup_ready());self.assertFalse(run.reservation.reaped)
    def test_wrong_C_subject_or_action_refuses_even_when_hash_matches(self):
        for key,value in [('identity',{'pid':99}),('admission_sha256','wrong'),('library_sha256','wrong'),('action','wrong')]:
            with self.subTest(key=key),tempfile.TemporaryDirectory() as d:
                run,ports,child,events,popen=SupervisorTests().fixture(Path(d),'normal');wait=child.wait
                def changed(timeout):
                    rc=wait(timeout);c=run.root/'typed-ax-c.json';data=json.loads(c.read_text());data[key]=value;c.write_text(json.dumps(data))
                    result=run.root/'typed-ax-result.json';data=json.loads(result.read_text());data['c_sha256']=helper.w.sha(c);result.write_text(json.dumps(data));return rc
                child.wait=changed
                supervisor=control.DiagnosticHelper(ports,run,clock=lambda:0,popen=popen)
                with self.assertRaisesRegex(RuntimeError,'C record subject'):supervisor.invoke(295)
                self.assertFalse(run.reservation.reaped)
    def test_actual_keeper_c_command_refuses_stale_request_before_native_entry(self):
        import sys
        with tempfile.TemporaryDirectory() as d:
            run,ports,child,events,unused=SupervisorTests().fixture(Path(d),'normal');root=run.root
            here=Path(control.__file__).parent
            for name in control.SOURCES:
                data=(here/name).read_text()
                if name=='native_b_diagnostic.py':data=data.replace('    def __init__(self):','    def __init__(self):\n        raise AssertionError("UNEXPECTED_NATIVE_ENTRY")',1)
                (root/name).write_text(data)
            binding=run.value['typed_ax_comparison'];binding['helper_sources']={name:helper.w.sha(root/name) for name in control.SOURCES}
            run.value['executable']='/invented/App';ports.admissions.births['A']['executable']='/invented/App'
            policy='(deny file-read* file-write* (subpath '+json.dumps(str(root.parent))+'))\n'
            (root/'phase.sb').write_text(policy);(root/'phase.sb').chmod(0o600);(root/'helper-tmp').mkdir()
            admitted={'inputs':run.value,'incarnation':'A','candidate':'invented','policy_sha256':helper.w.sha(root/'phase.sb'),
                      'facts':{'diagnostic_only':True,'launch_limit':1,'setup_allowed':False,'focus_allowed':False,'Stop_allowed':False}}
            (root/'admission.json').write_text(json.dumps(admitted));run.admission_sha=helper.w.sha(root/'admission.json')
            def actual(argv,**kwargs):
                self.assertEqual(argv[4],'-c');self.assertIn('__file__=',argv[5])
                request=root/'typed-ax-request.json';data=json.loads(request.read_text());data['recorded_at']='2000-01-01T00:00:00+00:00';request.write_text(json.dumps(data))
                argv[-1]=helper.w.sha(request)
                return subprocess.Popen(argv,**kwargs)
            supervisor=control.DiagnosticHelper(ports,run,popen=actual)
            with self.assertRaisesRegex(RuntimeError,'helper failed'):supervisor.invoke(supervisor.clock()+295)
            stderr=(root/'typed-ax-helper.stderr').read_text()
            self.assertIn('diagnostic request stale',stderr);self.assertNotIn('UNEXPECTED_NATIVE_ENTRY',stderr)
            self.assertTrue(run.extra_cleanup_ready());self.assertFalse(run.reservation.reaped)

class InterpreterDependencyTests(unittest.TestCase):
    def test_actual_stdlib_and_builtin_or_extension_are_bound(self):
        import sys,sysconfig,_posixsubprocess
        import native_attended_entry as entry
        # Exercise actual interpreter-path selection without requiring local
        # slot-wrapper files or unrelated controller dependencies on hosted CI.
        with patch.dict(sys.modules,{'native_successor_relaunch':N(dependencies=lambda:{})}),patch.object(entry,'sha',return_value='fixture-digest'):
            deps=entry.dependencies()
        self.assertIn(str(Path(sysconfig.get_path('stdlib')).resolve()/'subprocess.py'),deps)
        if getattr(_posixsubprocess,'__file__',None):self.assertIn(str(Path(_posixsubprocess.__file__).resolve()),deps)
        else:self.assertEqual(_posixsubprocess.__spec__.origin,'built-in');self.assertIn('_posixsubprocess',sys.builtin_module_names)
