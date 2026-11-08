"""Fixed diagnostic helper. Only this disposable process loads typed AX FFI."""
# Load standard-library dependencies while isolated sys.path excludes this phase.
import ctypes as C
import hashlib,json,os,sys,time,stat,types,datetime,subprocess,argparse,math,binascii,selectors,signal,struct,importlib.util
from pathlib import Path
typed=None
w=None

def require(ok,reason):
    if not ok:raise RuntimeError(reason)

def private_bytes(path,limit,expected=None):
    path=Path(path);require(path.is_absolute() and path.resolve()==path,'bootstrap path alias')
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    try:
        before=os.fstat(fd)
        require(stat.S_ISREG(before.st_mode) and before.st_uid==os.getuid() and before.st_nlink==1
                and stat.S_IMODE(before.st_mode)==0o600 and 0<before.st_size<=limit,'bootstrap private file invalid')
        raw=os.read(fd,limit+1)
        stamp=lambda v:(v.st_dev,v.st_ino,v.st_mode,v.st_uid,v.st_nlink,v.st_size,v.st_mtime_ns,v.st_ctime_ns)
        require(len(raw)==before.st_size and stamp(before)==stamp(os.fstat(fd))==stamp(path.lstat()),'bootstrap file changed')
        if expected is not None:require(hashlib.sha256(raw).hexdigest()==expected,'bootstrap digest differs')
        return raw
    finally:os.close(fd)

def private_json(path,limit,expected=None):
    def unique(pairs):
        out={}
        for k,v in pairs:
            require(k not in out,'duplicate bootstrap key');out[k]=v
        return out
    return json.loads(private_bytes(path,limit,expected),object_pairs_hook=unique)

def verified_modules(root,buffers):
    # Execute the already verified bytes; no phase sys.path insertion or second
    # file read. Companion readers receive the same verified reference module.
    def load(name,filename,reference=None):
        module=types.ModuleType(name);module.__file__=str(root/filename)
        if reference is not None:module.__dict__['_verified_reference']=reference
        exec(compile(buffers[filename],module.__file__,'exec'),module.__dict__)
        return module
    reference=load('verified_ax_reference','native_b_diagnostic.py')
    return load('verified_typed_ax','native_b_typed_ax.py',reference),load('verified_ax_window','native_b_window.py',reference)

ACTION='same-original-ax-reference/v1'

def publish(path,value):
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
    with os.fdopen(fd,'w') as stream:
        json.dump(value,stream,indent=2);stream.flush();os.fsync(stream.fileno())
    directory=os.open(path.parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:os.fsync(directory)
    finally:os.close(directory)

def admitted(request_path,digest,with_sources=False):
    root=Path(__file__).resolve().parent;info=root.lstat()
    require(root.resolve()==root and stat.S_ISDIR(info.st_mode) and info.st_uid==os.getuid() and stat.S_IMODE(info.st_mode)==0o700,'bootstrap root not private')
    path=Path(request_path);require(path==root/'typed-ax-request.json','diagnostic request path differs')
    request=private_json(path,32768,digest)
    admission=private_json(root/'admission.json',2*1024*1024,request['admission_sha256'])
    value=admission['inputs'];binding=value['typed_ax_comparison'];facts=admission['facts']
    require(facts.get('diagnostic_only') is True and facts.get('launch_limit')==1
              and all(facts.get(k) is False for k in ('setup_allowed','focus_allowed','Stop_allowed')),
              'diagnostic-only authority unavailable')
    require(admission['incarnation']=='A' and binding['action']==ACTION and request['action']==ACTION
              and request['candidate']==admission['candidate'] and request['binding']==binding,
              'diagnostic admission/action differs')
    require(binding['helper_seconds']==10 and binding['helper_reap_seconds']==1,'diagnostic budget differs')
    policy=private_bytes(root/'phase.sb',1024*1024,admission['policy_sha256']).decode()
    require('(deny file-read* file-write* (subpath '+json.dumps(str(root.parent))+'))' in policy,
              'diagnostic private channel not denied to App')
    buffers={}
    for relative,expected in binding['helper_sources'].items():
        p=root/relative;require(p.resolve()==p and p.is_relative_to(root),'diagnostic source alias')
        buffers[relative]=private_bytes(p,2*1024*1024,expected)
    require(set(binding['helper_sources'])=={'native_ax_comparison_helper.py','native_b_typed_ax.py','native_b_diagnostic.py','native_b_window.py','typed_ax/reader.c','typed_ax/reader.h','typed_ax/build.py'},'diagnostic source set differs')
    require(binding['manifest']==str(root/'typed-ax-build.json') and hashlib.sha256(private_bytes(root/'typed-ax-build.json',2*1024*1024)).hexdigest()==binding['sha256'],
              'diagnostic library manifest differs')
    keeper=os.getppid();require(keeper>1 and keeper==request['keeper_pid'],'diagnostic orphan/parent mismatch')
    identity=request['identity']
    require(identity['ppid']==keeper and identity['executable']==value['executable'],'App parent/executable differs')
    age=time.time()-datetime.datetime.fromisoformat(request['recorded_at']).timestamp()
    require(0<=age<5,'diagnostic request stale')
    require(os.environ.get('TMPDIR')==str(root/'helper-tmp'),'diagnostic private temp differs')
    result=(root,request,value,keeper)
    return (*result,buffers) if with_sources else result

def compare(root,request,value,keeper,backend_factory=None,loader=None,clock=time.monotonic):
    backend_factory=backend_factory or w.d.NativeBackend;loader=loader or typed.load
    started=clock();end=started+9 # outer supervisor10s; includes no extension
    backend=backend_factory();identity=request['identity'];binding=value['typed_ax_comparison']
    def check():
        w.require(clock()<end,'diagnostic internal deadline')
        w.require(os.getppid()==keeper,'diagnostic helper reparented')
        w.require(backend.identity(identity['pid'])==identity and identity['ppid']==keeper,'original birth/parent changed')
        w.require(w.sha(value['executable'])==value['executable_sha256'],'original executable bytes changed')
    try:
        check();library,manifest=loader(binding['manifest'],binding['sha256'])
        check();app=backend.app(identity['pid']);rc,owner=backend.owner(app)
        w.require(rc==0 and owner==identity['pid'],'diagnostic AX original owner differs')
        out=typed.Result();c_started=w.d.now()
        rc=library.chirality_ax_compare_v1(app,C.byref(out))
        # Do not publish foreign-root facts. Partial diagnostic status is not
        # readiness, qualification or authority to act.
        w.require(out.application_owner_rc==0 and out.application_pid==identity['pid'],'typed original owner unavailable/different')
        try:decoded=typed.decode(out)
        except Exception as error:
            decoded={'available':False,'decode_error':str(error),'raw_sha256':hashlib.sha256(bytes(out)).hexdigest()}
        c_record={'action':ACTION,'identity':identity,'admission_sha256':request['admission_sha256'],
                  'started_at':c_started,'finished_at':w.d.now(),'return_code':rc,'typed_c':decoded,
                  'library_sha256':manifest['library']['sha256'],
                  'identity_check_after_call':'pending; only a final bound result establishes completion','limits':'same local reference; sequential observation only'}
        publish(root/'typed-ax-c.json',c_record) # durable before Python or later identity refusal
        check();python={'attributes':[],'started_at':w.d.now()};python_end=min(end,clock()+4)
        def python_check():
            w.require(clock()<python_end,'Python comparison deadline')
            w.require(os.getppid()==keeper and backend.identity(identity['pid'])==identity,'original changed during Python comparison')
        for index,name in enumerate(w.d.AX_ATTRIBUTES):
            python_check()
            try:part=typed.reference.ax_inventory(backend,identity['pid'],python_check,application=app,attributes=(name,))
            except Exception as error:part={'attributes':[{'attribute':name,'available':False,'error':str(error)}]}
            publish(root/f'typed-ax-python-{index+1}.json',part)
            python['attributes'].extend(part['attributes']);python_check()
        python_check();check();python['finished_at']=w.d.now();publish(root/'typed-ax-python.json',python)
        result={'action':ACTION,'identity_before':identity,'identity_after':backend.identity(identity['pid']),
                'admission_sha256':request['admission_sha256'],'request_sha256':w.sha(root/'typed-ax-request.json'),
                'c_sha256':w.sha(root/'typed-ax-c.json'),'python_sha256':w.sha(root/'typed-ax-python.json'),
                'elapsed':clock()-started,'comparison_recorded':True,'readiness_promoted':False,'qualification_success':False,
                'limits':'Raw observations may be errors; neither agreement nor disagreement identifies an OS/App cause.'}
        w.require(result['identity_after']==identity and clock()<end,'diagnostic final identity/deadline differs')
        publish(root/'typed-ax-result.json',result);return result
    finally:backend.close()

def main(path,digest):
    global typed,w
    root,request,value,keeper,buffers=admitted(path,digest,with_sources=True)
    typed,w=verified_modules(root,buffers)
    return compare(root,request,value,keeper)

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--request',required=True);p.add_argument('--sha256',required=True)
    a=p.parse_args();main(a.request,a.sha256)
