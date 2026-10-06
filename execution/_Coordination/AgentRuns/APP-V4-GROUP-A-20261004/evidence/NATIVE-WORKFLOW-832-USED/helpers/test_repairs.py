#!/usr/bin/env python3
"""Synthetic-only checks: no HTTP listener, supplier, Cargo, auth or native page mint."""
import json,pathlib,tempfile,subprocess,os,signal,sys,time,unittest,struct
from witness_common import *
from owned_processes import Ownership
HERE=pathlib.Path(__file__).resolve().parent
ROOT=pathlib.Path(tempfile.mkdtemp(prefix='chirality-wf-synthetic-',dir='/private/tmp'))
class Checks(unittest.TestCase):
    def test_original_zero_result_success_and_repaired_rejection(self):
        # The original launcher's final standing uses returncode only. A no-test
        # inert executable is the precise acceptance condition, no provider starts.
        process=subprocess.run(['/usr/bin/true',TEST,'--ignored','--exact'],capture_output=True,text=True)
        self.assertEqual(process.returncode,0)
        with self.assertRaisesRegex(ValueError,'exactly one'):validate_result(ROOT,{},process.returncode,'running 0 tests\n\ntest result: ok. 0 passed; 0 failed; 0 ignored;')
    def test_missing_stale_and_foreign_result_rejected(self):
        root=ROOT/'results';root.mkdir();binding={'id':'fresh','providerMarker':'unique'};out='running 1 test\ntest result: ok. 1 passed; 0 failed; 0 ignored;'
        with self.assertRaises(FileNotFoundError):validate_result(root,binding,0,out)
        save(root/'witness-result.json',{'invocation':{'id':'stale'}})
        with self.assertRaisesRegex(ValueError,'unique invocation'):validate_result(root,binding,0,out)
    def test_http_cause_unknown_until_both_correlated(self):
        root=ROOT/'cause';root.mkdir();binding={'id':'fresh','providerMarker':'unique'};out='running 1 test\ntest result: ok. 1 passed; 0 failed; 0 ignored;'
        r={'invocation':binding,'adoption':'unknown','thread':'t','turn':'v','sourceGeneration':'g','supply':{'comparison':{'state':'equal_claimed_text'}},'nativeFailedTurn':[{'threadId':'t','turnId':'v','generation':'g','nativeTurn':{'status':'failed','error':{'message':'unrelated failure'}}}]}
        save(root/'witness-result.json',r)
        self.assertFalse(validate_result(root,binding,0,out)['http400CauseEstablished'])
        (root/'provider-observations.jsonl').write_text(json.dumps({'responseSent':True,'status':400,'marker':'unique'})+'\n')
        self.assertFalse(validate_result(root,binding,0,out)['http400CauseEstablished'])
        r['nativeFailedTurn'][0]['nativeTurn']['error']={'message':'400 unique'};save(root/'witness-result.json',r)
        self.assertTrue(validate_result(root,binding,0,out)['http400CauseEstablished'])
        # These JSON dictionaries exercise validator logic only, not native authority.
    def test_original_timeout_leaves_separate_group(self):
        root=ROOT/'original-timeout';root.mkdir();script=root/'inert.py'
        script.write_text('import subprocess,time,pathlib\np=subprocess.Popen(["/bin/sleep","20"],start_new_session=True)\npathlib.Path("pid").write_text(str(p.pid))\ntime.sleep(20)\n')
        harness=subprocess.Popen([sys.executable,str(script)],cwd=root)
        pid=None
        try:
            deadline=time.monotonic()+3
            while not (root/'pid').exists() and time.monotonic()<deadline:time.sleep(.01)
            pid=int((root/'pid').read_text())
            # Exact original timeout handler, entered with a shortened inert wait.
            try:harness.wait(timeout=.05)
            except subprocess.TimeoutExpired:harness.terminate();harness.wait(timeout=10);code=124
            self.assertEqual(code,124);os.killpg(pid,0)
            save(root/'observation.json',{'originalLauncherSha256':sha(pathlib.Path('/private/tmp/chirality-parent-workflow-witness-lncXTF/parent_launch.py')),'harnessReaped':True,'supplierGroupSurvived':pid,'standing':'synthetic negative; wait shortened, timeout handler unchanged'})
        finally:
            if pid:
                try:os.killpg(pid,signal.SIGKILL)
                except ProcessLookupError:pass
            if harness.poll() is None:harness.kill();harness.wait()
            deadline=time.monotonic()+3
            while pid and time.monotonic()<deadline:
                try:os.killpg(pid,0);time.sleep(.02)
                except ProcessLookupError:pid=None
            self.assertIsNone(pid,'synthetic original-negative group cleanup incomplete')
    def run_owned(self,stage,ack=True,stubborn=False):
        root=ROOT/('owned-'+str(stage)+'-'+str(ack)+'-'+str(stubborn));root.mkdir();owner=Ownership(root);owner.start()
        if not ack:owner.closing=True
        # Python represents the pre-exec packet in a synthetic owned child only.
        # The actual Rust pre_exec implementation still requires compile/backcheck.
        code='''import os,subprocess,sys,struct,time,pathlib,signal
r=int(sys.argv[1]);a=int(sys.argv[2]);stage=int(sys.argv[3])
child=os.fork()
if child==0:
 os.setpgid(0,0);os.write(r,struct.pack('=ii',os.getpid(),stage));ack=os.read(a,1);os.close(r);os.close(a)
 if ack!=b'A':os._exit(125)
 pathlib.Path('exec-marker').write_text('owned before inert exec')
 if sys.argv[4]=='True':
  signal.signal(signal.SIGTERM,signal.SIG_IGN);subprocess.Popen(['/bin/sleep','20']);time.sleep(20);os._exit(0)
 os.execl('/bin/sleep','sleep','20')
os.close(r);os.close(a);os.waitpid(child,0)
'''
        harness=subprocess.Popen([sys.executable,'-c',code,str(owner.register_write),str(owner.ack_read),str(stage),str(stubborn)],cwd=root,env={'PATH':'/usr/bin:/bin'},pass_fds=owner.inherited(),start_new_session=True);owner.handed_off()
        deadline=time.monotonic()+3
        while not owner.entries and time.monotonic()<deadline:time.sleep(.01)
        if ack:
            while not (root/'exec-marker').exists() and time.monotonic()<deadline:time.sleep(.01)
            self.assertTrue((root/'exec-marker').exists())
        outcome=owner.cleanup(harness,.3);self.assertTrue(outcome['clean'],outcome)
        if not ack:self.assertFalse((root/'exec-marker').exists())
    def test_owned_version_timeout_cleanup(self):self.run_owned(1)
    def test_owned_app_timeout_cleanup(self):self.run_owned(2)
    def test_incomplete_handshake_cannot_exec(self):self.run_owned(1,False)
    def test_owned_stubborn_group_and_descendant_cleanup(self):self.run_owned(2,True,True)
    def test_copy_injection_is_bounded(self):
        import prepare_compile
        app=ROOT/'injection/app';(app/'src-tauri/src').mkdir(parents=True)
        repo=pathlib.Path('/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/app')
        for name in ('hosting.rs','runtime_session.rs'):(app/'src-tauri/src'/name).write_bytes((repo/'src-tauri/src'/name).read_bytes())
        before=manifest(app);patch=prepare_compile.inject(app,HERE);after=manifest(app);(ROOT/'injection/injection.diff').write_text(patch)
        changed={p for p in set(before)|set(after) if before.get(p)!=after.get(p)}
        self.assertEqual(changed,{'src-tauri/src/hosting.rs','src-tauri/src/runtime_session.rs','src-tauri/src/parent_stock_workflow_witness.rs'})
        self.assertIn('probe.process_group(0)',patch);self.assertEqual(patch.count('+        parent_witness_own_spawn'),2)
        save(ROOT/'injection/bindings.json',{'before':before,'after':after,'diffSha256':sha(ROOT/'injection/injection.diff')})
if __name__=='__main__':
    print('SYNTHETIC_ROOT='+str(ROOT),flush=True)
    unittest.main(verbosity=2)
