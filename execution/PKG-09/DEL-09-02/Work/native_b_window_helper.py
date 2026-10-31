"""Fixed private helper request. No arbitrary PID/command or global input route."""
from pathlib import Path
import argparse,ctypes as C,hashlib,json,os,stat,sys,time
sys.path.insert(0,str(Path(__file__).resolve().parent)) # protected sibling copies under -I -S
import native_b_window as w

def write_result(path,value):
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,'w') as f:json.dump(value,f,indent=2)

def require_same_window(root,request,actual,comparison):
    expected=request['window']
    if actual==expected:return
    differences=[]
    for key in sorted(set(expected)|set(actual)):
        left,right=expected.get(key),actual.get(key)
        if left==right and (key in expected)==(key in actual):continue
        if key=='bounds' and isinstance(left,dict) and isinstance(right,dict):
            for field in sorted(set(left)|set(right)):
                if left.get(field)!=right.get(field) or (field in left)!=(field in right):
                    differences.append('bounds.'+field)
        else:differences.append(key)
    # These are the already selected, owner-filtered facts. No fresh native call,
    # selection, screenshot or retry is added by failure reporting.
    record={'at':w.d.now(),'comparison':comparison,'sequence':request['sequence'],
            'target':request.get('target','main'),'admission_sha256':request['admission_sha256'],
            'expected_window':expected,'actual_owned_window':actual,'different_fields':differences,
            'limits':'Nonatomic samples; mismatch still refuses. No image or input accepted.'}
    try:write_result(root/f"window-helper-{request['sequence']:03d}.window-mismatch.json",record)
    except Exception as error:
        raise RuntimeError('helper owned window changed; mismatch diagnostic unavailable: '+type(error).__name__) from error
    raise RuntimeError('helper owned window changed')


def main(request_path,expected_sha):
    root=Path(__file__).resolve().parent;info=root.lstat()
    w.require(root.resolve()==root and info.st_uid==os.getuid() and stat.S_IMODE(info.st_mode)==0o700,'helper root not private')
    request_path=Path(request_path);w.require(request_path.parent==root,'helper request outside root')
    info=w.private_file(request_path,0o600);w.require(info.st_size<=16384,'helper request oversized')
    request=w.private_json(request_path,16384,expected_sha);admission=root/'admission.json'
    w.require(w.sha(admission)==request['admission_sha256'],'helper admission changed')
    value=json.loads(admission.read_text())['inputs']
    for name,digest in value['window_route']['helper_sources'].items():w.require(w.sha(w.private_path(root,name))==digest,'helper source changed')
    w.require(w.tools_identity()==value['window_route']['tools'] and set(w.python_prefixes())<=set(value['window_route']['python_prefixes']),'helper tool/runtime prefix changed')
    helper_tmp=root/'helper-tmp'
    w.require(os.environ.get('TMPDIR')==str(helper_tmp) and helper_tmp.is_dir() and not helper_tmp.is_symlink(),'private helper temp binding unavailable')
    age=time.time()-__import__('datetime').datetime.fromisoformat(request['recorded_at']).timestamp()
    w.require(0<=age<5,'helper request stale')
    expected=request['identity'];pid=expected['pid'];w.require(expected['executable']==value['executable'],'helper target is not candidate')
    target=request.get('target','main');w.require(target in ('main','stop-modal'),'unsupported helper target')
    context=None
    if target=='stop-modal':
        context=w.private_json(root/'stop-modal-context.json',256*1024,request['stop_context_sha256'])
        w.require(context['identity']==expected and context['posted'] is True
                  and context['generation']['home']==value['expected_generation_home'],'modal Stop context/account binding differs')
    backend=w.d.NativeBackend()
    def bound(comparison):
        w.require(backend.identity(pid)==expected and w.sha(value['executable'])==value['executable_sha256'],'helper original App identity changed')
        window=w.select_modal(backend,pid,context) if context else w.select_main(backend,pid)
        require_same_window(root,request,window,comparison)
        return window
    try:
        action=request['action'];w.require(action in ('capture','focus','click','scroll'),'unsupported helper action')
        w.require(type(request['sequence']) is int and 0<request['sequence']<=w.MAX_OPERATIONS,'helper sequence outside bound')
        if action=='capture':w.require(backend.screen_access(),'capture helper preflight denied; no request or fallback')
        window=bound('initial')
        if context:
            relation=w.modal_relation(backend,pid,window['window_id'],context['main']['window_id'])
            write_result(root/f"window-helper-{request['sequence']:03d}.modal.json",relation)
        if action=='capture':
            name=f"capture-{request['sequence']:03d}.unverified.png"
            w.require(request['image_name']==name and not os.path.lexists(root/name),'capture destination differs/used')
            bound('before-capture-exec');backend.close()
            command=[str(w.CAPTURE),'-x','-a','-o','-t','png','-l',str(window['window_id']),str(root/name)]
            os.execve(str(w.CAPTURE),command,dict(os.environ))
        app=backend.app(pid)
        owner_rc,owner=backend.owner(app);w.require(owner_rc==0 and owner==pid,'helper AX App ownership unavailable')
        if action=='focus':
            if not w.frontmost(backend,app):
                setter=backend.a.AXUIElementSetAttributeValue;setter.restype=C.c_int;setter.argtypes=[C.c_void_p,C.c_void_p,C.c_void_p]
                true=C.c_void_p.in_dll(backend.c,'kCFBooleanTrue').value
                rc=setter(app,backend.string('AXFrontmost'),true);w.require(rc==0,'owned App focus request refused')
                end=time.monotonic()+0.6
                while time.monotonic()<end and not w.frontmost(backend,app):time.sleep(0.05)
            w.require(w.frontmost(backend,app),'owned App did not become frontmost')
        else:
            if context:w.require(action=='click','modal admits confirmation click only')
            w.require(w.frontmost(backend,app) and (context is not None or window['own_visible_layer0_count']==1),'own main-window focus unavailable')
            x,y=request['point'];b=window['bounds']
            w.require(all(type(v) in (int,float) for v in (x,y)) and b['X']+8<x<b['X']+b['Width']-8 and b['Y']+40<y<b['Y']+b['Height']-8,'helper point outside owned content band')
            class Point(C.Structure):_fields_=[('x',C.c_double),('y',C.c_double)]
            create=backend.a.CGEventCreateMouseEvent;create.restype=C.c_void_p;create.argtypes=[C.c_void_p,C.c_uint32,Point,C.c_uint32]
            post=backend.a.CGEventPostToPid;post.restype=None;post.argtypes=[C.c_int,C.c_void_p]
            flags=backend.a.CGEventSetFlags;flags.restype=None;flags.argtypes=[C.c_void_p,C.c_uint64]
            field=backend.a.CGEventSetIntegerValueField;field.restype=None;field.argtypes=[C.c_void_p,C.c_uint32,C.c_int64]
            events=[]
            try:
                if action=='click':
                    for kind in (1,2): # left down/up, no arbitrary keyboard/text command
                        e=create(None,kind,Point(x,y),0);w.require(e,'mouse event unavailable');events.append(e)
                else:
                    delta=request['delta'];w.require(type(delta) is int and 0<abs(delta)<=min(600,int(window['bounds']['Height'])-200),'helper scroll exceeds bound')
                    # Fixed one-axis wheel, no variadic arguments beyond wheel1.
                    scroll=backend.a.CGEventCreateScrollWheelEvent;scroll.restype=C.c_void_p;scroll.argtypes=[C.c_void_p,C.c_uint32,C.c_uint32,C.c_int32]
                    location=backend.a.CGEventSetLocation;location.restype=None;location.argtypes=[C.c_void_p,Point]
                    e=scroll(None,0,1,delta);w.require(e,'scroll event unavailable');location(e,Point(x,y));events.append(e)
                bound('before-input-post');w.require(w.frontmost(backend,app),'focus changed before input')
                for e in events:
                    flags(e,0)
                    if action=='click':field(e,1,1) # kCGMouseEventClickState: one click
                    post(pid,e)
            finally:
                for e in events:backend.c.CFRelease(e)
        w.require(backend.identity(pid)==expected,'App identity changed after input')
        # Posting/AX return codes are not effect proof. Keeper captures and agent
        # must read the actual effect before accepting a subsequent action.
        result={'at':w.d.now(),'action':action,'sequence':request['sequence'],'posted_or_focus_observed':True,'effect_requires_fresh_capture_read':True}
        write_result(root/f"window-helper-{request['sequence']:03d}.result.json",result)
    finally:backend.close()
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--request',type=Path,required=True);p.add_argument('--sha256',required=True);a=p.parse_args();main(a.request,a.sha256)
