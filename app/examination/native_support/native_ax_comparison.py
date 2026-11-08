"""Keeper supervision for one isolated typed AX diagnostic. Never loads its DLL."""
import errno,hashlib,json,os,subprocess,sys,time
from pathlib import Path
from native_attended_sequence import AttendedSequence,closed
import native_b_window as w

ACTION='same-original-ax-reference/v1'
SOURCES={'native_ax_comparison_helper.py','native_b_typed_ax.py','native_b_diagnostic.py','native_b_window.py',
         'typed_ax/reader.c','typed_ax/reader.h','typed_ax/build.py'}

def stage(root,manifest,manifest_sha):
    import native_b_typed_ax as typed # import defines FFI types; no library load
    binding=typed.stage_build(root,manifest,manifest_sha,isolated_sources=True)
    root=Path(root);here=Path(__file__).resolve().parent
    for name in ('native_ax_comparison_helper.py','native_b_window.py'):
        data=(here/name).read_bytes();target=root/name
        if target.exists():w.require(target.read_bytes()==data,'diagnostic staging collision')
        else:
            fd=os.open(target,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
            with os.fdopen(fd,'wb') as f:f.write(data)
    return {**binding,'action':ACTION,'helper_seconds':10,'helper_reap_seconds':1,
            'helper_sources':{name:w.sha(root/name) for name in sorted(SOURCES)}}

def check_binding(run):
    value=w.private_json(run.root/'admission.json',2*1024*1024,run.admission_sha)['inputs']
    binding=value['typed_ax_comparison']
    w.require(binding==run.value['typed_ax_comparison'] and binding['action']==ACTION
              and binding['helper_seconds']==10 and binding['helper_reap_seconds']==1,'diagnostic admission/budget differs')
    w.require(set(binding['helper_sources'])==SOURCES,'diagnostic source set differs')
    for name,digest in binding['helper_sources'].items():
        p=run.root/name;w.private_file(p,0o600);w.require(w.sha(p)==digest,'diagnostic staged source changed')
    w.require(binding['manifest']==str(run.root/'typed-ax-build.json') and w.sha(run.root/'typed-ax-build.json')==binding['sha256'],
              'diagnostic manifest binding differs')
    manifest=w.private_json(run.root/'typed-ax-build.json',2*1024*1024,binding['sha256'])
    library=Path(manifest['library']['path'])
    w.require(library==run.root/'typed-ax-reader.dylib','diagnostic library path differs')
    w.private_file(library,0o600);w.require(w.sha(library)==manifest['library']['sha256'],'diagnostic library changed')
    return binding

class DiagnosticHelper:
    def __init__(self,ports,run,clock=time.monotonic,popen=subprocess.Popen):
        self.ports,self.run,self.clock,self.popen=ports,run,clock,popen
        self.child=None;self.pending=False;self.used=False;self.returncode=None;self.timed_out=False
        original_ready=run.extra_cleanup_ready
        run.diagnostic_helper=self
        run.extra_cleanup_ready=lambda:self.settled() and original_ready()
    def settled(self):
        if self.pending:return False
        if self.child is None:return True
        try:
            code=self.child.wait(timeout=0)
            self.returncode=code;self.child=None
            self.run.safe_log('diagnostic_helper_settled',return_code=code,timed_out=self.timed_out)
            return True
        except subprocess.TimeoutExpired:return False
        except BaseException as error:
            self.run.safe_log('diagnostic_helper_settlement_unknown',error=str(error));return False
    def invoke(self,end):
        w.require(not self.used and self.child is None and not self.pending,'diagnostic helper already used/unknown')
        self.used=True
        run=self.run;self.ports._original('A')
        binding=check_binding(run)
        w.require(self.clock()+11<end-57,'diagnostic lacks10s+1s helper and57s cleanup reserve')
        identity=dict(self.ports.admissions.births['A'])
        w.require(identity['ppid']==os.getpid(),'diagnostic original Child parent differs')
        request={'action':ACTION,'candidate':run.value['candidate_key'],'binding':binding,
                 'identity':identity,'keeper_pid':os.getpid(),'admission_sha256':run.admission_sha,'recorded_at':w.d.now()}
        run.act_record('typed-ax-request.json',request)
        entry=run.root/'native_ax_comparison_helper.py';source=entry.read_bytes()
        w.require(hashlib.sha256(source).hexdigest()==binding['helper_sources'][entry.name],'diagnostic entry bytes changed')
        code_source='__file__='+repr(str(entry))+'\n'+source.decode('utf-8')
        command=[str(Path(sys.executable).resolve()),'-I','-B','-S','-c',code_source,
                 '--request',str(run.root/'typed-ax-request.json'),'--sha256',w.sha(run.root/'typed-ax-request.json')]
        env={'HOME':str(Path.home()),'PATH':'/usr/bin:/bin','TMPDIR':str(run.root/'helper-tmp'),
             'CODEX_HOME':str(run.root/'codex-home'),'PYTHONDONTWRITEBYTECODE':'1'}
        with (run.root/'typed-ax-helper.stdout').open('xb') as out,(run.root/'typed-ax-helper.stderr').open('xb') as err:
            started=self.clock();helper_end=started+10
            self.pending=True # failed Popen outcome remains unknown, never original custody release
            try:self.child=self.popen(command,env=env,stdin=subprocess.DEVNULL,stdout=out,stderr=err,close_fds=True,umask=0o077)
            except OSError as error:
                # CPython's errpipe exec-error path waitpids its child before
                # raising these executable-bound errors. Other failures remain
                # unknown; an injected/custom spawner cannot assert this proof.
                known=(self.popen is subprocess.Popen and sys.implementation.name=='cpython'
                       and error.errno in (errno.ENOENT,errno.ENOEXEC,errno.EACCES,errno.EPERM)
                       and error.filename==command[0])
                if known:
                    self.pending=False
                    try:run.act_record('typed-ax-helper-not-started.json',{'errno':error.errno,
                        'executable':command[0],'proof':'CPython executable-error path completed child wait before raising',
                        'original_Child_reaped':False})
                    except BaseException as receipt_error:
                        raise RuntimeError('known helper exec failure errno='+str(error.errno)+'; receipt failed: '+repr(receipt_error)+'; helper settled, original Child not reaped') from error
                raise
            self.pending=False
            try:
                code=self.child.wait(timeout=max(0,helper_end-self.clock()))
                self.timed_out=self.clock()>helper_end
            except subprocess.TimeoutExpired:
                self.timed_out=True
                # Only the retained disposable diagnostic helper, never App/supplier.
                self.child.kill()
                try:code=self.child.wait(timeout=1)
                except subprocess.TimeoutExpired:raise RuntimeError('diagnostic helper settlement unknown; retain all custody')
            self.returncode=code;self.child=None
        run.act_record('typed-ax-helper-exit.json',{'return_code':code,'timed_out':self.timed_out,
            'elapsed':self.clock()-started,'original_Child_reaped':False})
        self.ports._original('A')
        w.require(not self.timed_out and code==0,'diagnostic helper failed; partial files are evidence only')
        result=w.private_json(run.root/'typed-ax-result.json',2*1024*1024)
        w.require(result['action']==ACTION and result['identity_before']==identity and result['identity_after']==identity
                  and result['admission_sha256']==run.admission_sha
                  and result['request_sha256']==w.sha(run.root/'typed-ax-request.json')
                  and result['c_sha256']==w.sha(run.root/'typed-ax-c.json')
                  and result['python_sha256']==w.sha(run.root/'typed-ax-python.json')
                  and result['readiness_promoted'] is False and result['qualification_success'] is False,
                  'diagnostic result binding differs')
        c_record=w.private_json(run.root/'typed-ax-c.json',2*1024*1024,result['c_sha256'])
        manifest=w.private_json(Path(binding['manifest']),2*1024*1024,binding['sha256'])
        w.require(c_record.get('action')==ACTION and c_record['identity']==identity and c_record['admission_sha256']==run.admission_sha
                  and c_record['library_sha256']==manifest['library']['sha256'],'diagnostic C record subject differs')
        return result

class DiagnosticSequence(AttendedSequence):
    def run(self,slot_start):
        w.require(not self.started,'diagnostic sequence already used');self.started=True
        self.deadline=slot_start+295
        self.result.update(scope='one original A typed AX diagnostic and normal Quit only',
                           witness_complete=False,diagnostic_complete=False,Stop_confirmed=False,LT23_observed=False)
        try:
            receipt=self.p.admit_empty_namespace(self.deadline)
            self.current='A' # preserve unknown launch custody if it raises after spawn
            self.p.launch('A',receipt,self.deadline);self.incarnations.append('A')
            run=self.p.runs['A'];helper=DiagnosticHelper(self.p,run,self.clock)
            self.p.record('typed-ax-diagnostic-result',helper.invoke(self.deadline))
            self.result['diagnostic_complete']=True
        except BaseException as error:self.result['error']=repr(error)
        unspawned=(getattr(self.p,'pending_launch',None) is None and
                   ('A' not in self.p.runs or getattr(self.p.runs['A'],'reservation','unknown') is None))
        if self.current=='A' and unspawned:
            self.current=None;self.result['launch_not_started']=True
        # This route never invokes setup, focus, readiness, B, Stop or Cancel.
        if self.current=='A':
            try:
                self.quit_attempted.add('A')
                self.closure(self.p.quit_normal('A',self.deadline))
            except BaseException as error:
                self.result['cleanup_error']=repr(error)
                try:self.p.retain_and_report('A',self.deadline,self.result)
                except BaseException as delivery:self.delivery_errors.append(str(delivery))
        self.result.update(incarnations=list(self.incarnations),custody_held=self.current is not None or any(getattr(r,'thread',None) is not None and r.thread.is_alive() for r in self.p.runs.values()),
                           elapsed=self.clock()-slot_start,overrun=max(0,self.clock()-self.deadline),
                           delivery_errors=self.delivery_errors)
        self.safe_record('typed-ax-sequence-result',self.result)
        return self.result
