"""Fixed diagnostic helper. Only this disposable process loads typed AX FFI."""
import ctypes as C
import hashlib,json,os,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import native_b_typed_ax as typed
import native_b_window as w

ACTION='same-original-ax-reference/v1'

def publish(path,value):
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
    with os.fdopen(fd,'w') as stream:
        json.dump(value,stream,indent=2);stream.flush();os.fsync(stream.fileno())

def admitted(request_path,digest):
    root=Path(__file__).resolve().parent;typed.private_root(root)
    path=Path(request_path);w.require(path==root/'typed-ax-request.json','diagnostic request path differs')
    request=w.private_json(path,32768,digest)
    admission=w.private_json(root/'admission.json',2*1024*1024,request['admission_sha256'])
    value=admission['inputs'];binding=value['typed_ax_comparison'];facts=admission['facts']
    w.require(facts.get('diagnostic_only') is True and facts.get('launch_limit')==1
              and all(facts.get(k) is False for k in ('setup_allowed','focus_allowed','Stop_allowed')),
              'diagnostic-only authority unavailable')
    w.require(admission['incarnation']=='A' and binding['action']==ACTION and request['action']==ACTION
              and request['candidate']==admission['candidate'] and request['binding']==binding,
              'diagnostic admission/action differs')
    w.require(binding['helper_seconds']==10 and binding['helper_reap_seconds']==1,'diagnostic budget differs')
    w.private_file(root/'phase.sb',0o600)
    w.require(w.sha(root/'phase.sb')==admission['policy_sha256'],'diagnostic App policy changed')
    w.require('(deny file-read* file-write* (subpath '+json.dumps(str(root.parent))+'))' in (root/'phase.sb').read_text(),
              'diagnostic private channel not denied to App')
    for relative,expected in binding['helper_sources'].items():
        p=root/relative;w.require(p.resolve()==p and p.is_relative_to(root),'diagnostic source alias')
        w.private_file(p,0o600);w.require(w.sha(p)==expected,'diagnostic helper source changed')
    w.require(set(binding['helper_sources'])=={'native_ax_comparison_helper.py','native_b_typed_ax.py','native_b_diagnostic.py','native_b_window.py','typed_ax/reader.c','typed_ax/reader.h','typed_ax/build.py'},'diagnostic source set differs')
    w.require(binding['manifest']==str(root/'typed-ax-build.json') and w.sha(root/'typed-ax-build.json')==binding['sha256'],
              'diagnostic library manifest differs')
    keeper=os.getppid();w.require(keeper>1 and keeper==request['keeper_pid'],'diagnostic orphan/parent mismatch')
    identity=request['identity']
    w.require(identity['ppid']==keeper and identity['executable']==value['executable'],'App parent/executable differs')
    age=time.time()-__import__('datetime').datetime.fromisoformat(request['recorded_at']).timestamp()
    w.require(0<=age<5,'diagnostic request stale')
    w.require(os.environ.get('TMPDIR')==str(root/'helper-tmp'),'diagnostic private temp differs')
    return root,request,value,keeper

def compare(root,request,value,keeper,backend_factory=w.d.NativeBackend,loader=typed.load,clock=time.monotonic):
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
                  'library_sha256':manifest['library']['sha256'],'limits':'same local reference; sequential observation only'}
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
            python['attributes'].extend(part['attributes'])
        check();python['finished_at']=w.d.now();publish(root/'typed-ax-python.json',python)
        result={'action':ACTION,'identity_before':identity,'identity_after':backend.identity(identity['pid']),
                'admission_sha256':request['admission_sha256'],'request_sha256':w.sha(root/'typed-ax-request.json'),
                'c_sha256':w.sha(root/'typed-ax-c.json'),'python_sha256':w.sha(root/'typed-ax-python.json'),
                'elapsed':clock()-started,'comparison_recorded':True,'readiness_promoted':False,'qualification_success':False,
                'limits':'Raw observations may be errors; neither agreement nor disagreement identifies an OS/App cause.'}
        w.require(result['identity_after']==identity and clock()<end,'diagnostic final identity/deadline differs')
        publish(root/'typed-ax-result.json',result);return result
    finally:backend.close()

def main(path,digest):
    root,request,value,keeper=admitted(path,digest)
    return compare(root,request,value,keeper)

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--request',required=True);p.add_argument('--sha256',required=True)
    a=p.parse_args();main(a.request,a.sha256)
