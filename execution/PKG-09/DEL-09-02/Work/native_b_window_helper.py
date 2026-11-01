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


def activate_original_app(pid):
    # System AppKit only, inside this separately supervised helper. No list of
    # applications, bundle lookup, ignore-other-apps flag or new executable.
    appkit=C.CDLL('/System/Library/Frameworks/AppKit.framework/AppKit')
    objc=C.CDLL('/usr/lib/libobjc.A.dylib')
    objc.objc_getClass.restype=C.c_void_p;objc.objc_getClass.argtypes=[C.c_char_p]
    objc.sel_registerName.restype=C.c_void_p;objc.sel_registerName.argtypes=[C.c_char_p]
    sel=objc.sel_registerName
    object_call=C.CFUNCTYPE(C.c_void_p,C.c_void_p,C.c_void_p)(('objc_msgSend',objc))
    object_pid_call=C.CFUNCTYPE(C.c_void_p,C.c_void_p,C.c_void_p,C.c_int)(('objc_msgSend',objc))
    pid_call=C.CFUNCTYPE(C.c_int,C.c_void_p,C.c_void_p)(('objc_msgSend',objc))
    policy_call=C.CFUNCTYPE(C.c_long,C.c_void_p,C.c_void_p)(('objc_msgSend',objc))
    activate_call=C.CFUNCTYPE(C.c_bool,C.c_void_p,C.c_void_p,C.c_ulong)(('objc_msgSend',objc))
    void_call=C.CFUNCTYPE(None,C.c_void_p,C.c_void_p)(('objc_msgSend',objc))
    pool=object_call(objc.objc_getClass(b'NSAutoreleasePool'),sel(b'new'))
    w.require(pool,'activation autorelease pool unavailable')
    try:
        target=object_pid_call(objc.objc_getClass(b'NSRunningApplication'),sel(b'runningApplicationWithProcessIdentifier:'),pid)
        w.require(target,'original App not registered for activation')
        actual=pid_call(target,sel(b'processIdentifier'))
        w.require(actual==pid,'activation receiver differs from original App')
        policy=policy_call(target,sel(b'activationPolicy'))
        w.require(policy in (0,1),'original App activation policy prohibits activation')
        sent=bool(activate_call(target,sel(b'activateWithOptions:'),0))
        return {'receiver_pid':actual,'activation_policy':policy,'options':0,'request_sent':sent,
                'limits':'Request dispatch only, not actual frontmost/effect proof.'}
    finally:void_call(pool,sel(b'drain'))


class NativeFocus:
    """One supervised AX transaction. All AX/CG/libproc calls share one cap.

    CF decoding is local; identity hashes share the same wall deadline. The
    outer original-helper custody still enforces its existing4s wait/1s reap.
    """
    def __init__(self,backend,pid,app,trace,clock=time.monotonic):
        self.b,self.pid,self.app,self.trace,self.clock=backend,pid,app,trace,clock
        self.end=clock()+3;self.calls=0
        declarations=[('AXUIElementCopyActionNames',C.c_int,[C.c_void_p,C.POINTER(C.c_void_p)]),
            ('AXUIElementIsAttributeSettable',C.c_int,[C.c_void_p,C.c_void_p,C.POINTER(C.c_bool)]),
            ('AXUIElementSetAttributeValue',C.c_int,[C.c_void_p,C.c_void_p,C.c_void_p]),
            ('AXUIElementPerformAction',C.c_int,[C.c_void_p,C.c_void_p]),
            ('_AXUIElementGetWindow',C.c_int,[C.c_void_p,C.POINTER(C.c_uint32)])]
        for name,result,args in declarations:
            fn=getattr(backend.a,name);fn.restype=result;fn.argtypes=args
        self.original_a,self.original_p=backend.a,backend.p
        owner=self
        class Function:
            def __init__(self,fn,name):object.__setattr__(self,'fn',fn);object.__setattr__(self,'name',name)
            def __setattr__(self,k,v):setattr(self.fn,k,v)
            def __getattr__(self,k):return getattr(self.fn,k)
            def __call__(self,*args):
                w.require(owner.calls<200 and clock()+.2<owner.end,'autonomous focus call/deadline bound')
                if self.name=='AXUIElementSetMessagingTimeout':args=(args[0],.2)
                owner.calls+=1
                if self.name=='AXUIElementPerformAction':owner.trace['raise_attempted']=True
                if self.name=='AXUIElementSetAttributeValue':owner.trace['frontmost_attempted']=True
                return self.fn(*args) # action rc must be retained even if late
        class Library:
            def __init__(self,lib):self.lib=lib
            def __getattr__(self,name):return Function(getattr(self.lib,name),name)
        backend.a,backend.p=Library(backend.a),Library(backend.p)
    def close(self):
        self.trace.update(native_calls=self.calls,native_call_cap=200,deadline=self.end)
        self.b.a,self.b.p=self.original_a,self.original_p
    def check_time(self):w.require(self.clock()<self.end,'autonomous focus returned late')
    def read(self,e,name):
        rc,owner=self.b.owner(e);w.require(rc==0 and owner==self.pid,'focus AX owner differs')
        row,refs=self.b.attribute(e,name)
        w.require(row['return_code']==0,'focus AX attribute unavailable: '+name)
        self.check_time();return row,refs
    def scalar(self,e,name):
        row,refs=self.read(e,name);w.require(not refs,'focus scalar is reference');return row['value']
    def main(self,expected):
        row,refs=self.read(self.app,'AXWindows')
        w.require(row['type']['name']=='CFArray' and 0<len(refs)<=8,'focus window roots unavailable')
        roots=[]
        for e in refs:
            w.require(not self.b.equal(e,self.app),'focus self-reference is not a window')
            if any(self.b.equal(e,old) for old in roots):continue
            w.require(self.scalar(e,'AXRole')=='AXWindow','ambiguous/unknown focus window root')
            roots.append(e)
        w.require(len(roots)==1,'focus requires one distinct owned main')
        main=roots[0];number=C.c_uint32()
        w.require(self.b.a._AXUIElementGetWindow(main,C.byref(number))==0 and number.value==expected['window_id'],
                  'focus AX main number differs')
        w.require(self.scalar(main,'AXTitle')==expected['title'],'focus AX main title differs')
        # Missing modal/hierarchy observations refuse; never infer no modal.
        w.require(self.scalar(main,'AXModal') is False,'focus main modal state unavailable/blocked')
        row,children=self.read(main,'AXChildren')
        w.require(row['type']['name']=='CFArray' and len(children)<=8,'focus main children unavailable')
        for child in children:
            role=self.scalar(child,'AXRole')
            w.require(isinstance(role,str) and role.startswith('AX') and role not in
                      ('AXSheet','AXDialog','AXWindow','AXUnknown','AXPopover','AXMenu'),
                      'focus blocked by modal/unknown child')
        self.check_time();return main
    def supports(self,main):
        value=C.c_void_p();rc=self.b.a.AXUIElementCopyActionNames(main,C.byref(value))
        if value.value:self.b.held.append(value.value)
        w.require(rc==0 and value.value,'focus action list unavailable')
        actions=[self.b.scalar(e) for e in self.b.array(value.value,32)]
        settable=C.c_bool();rc=self.b.a.AXUIElementIsAttributeSettable(self.app,self.b.string('AXFrontmost'),C.byref(settable))
        self.check_time();return 'AXRaise' in actions and rc==0 and settable.value
    def raise_main(self,main):return self.b.a.AXUIElementPerformAction(main,self.b.string('AXRaise'))
    def front(self):return self.scalar(self.app,'AXFrontmost') is True
    def set_front(self):return self.b.a.AXUIElementSetAttributeValue(self.app,self.b.string('AXFrontmost'),C.c_void_p.in_dll(self.b.c,'kCFBooleanTrue').value)

def autonomous_focus(ops,bound,expected,trace,sleep=time.sleep):
    main=ops.main(expected);trace['observations']=[{'at':w.d.now(),'frontmost':ops.front()}]
    if not trace['observations'][-1]['frontmost']:
        w.require(ops.supports(main),'AXRaise or settable AXFrontmost unavailable')
        bound('before-autonomous-raise');ops.check_time()
        trace['raise_rc']=ops.raise_main(main)
        ops.check_time();w.require(trace['raise_rc']==0,'owned AXRaise refused')
        bound('before-autonomous-frontmost');ops.check_time()
        # Revalidate the same retained AX window after Raise before second act.
        again=ops.main(expected)
        w.require(ops.b.equal(main,again),'focus main reference changed after Raise')
        trace['frontmost_rc']=ops.set_front()
        ops.check_time();w.require(trace['frontmost_rc']==0,'owned AXFrontmost write refused')
        for _ in range(10):
            actual=ops.front();trace['observations'].append({'at':w.d.now(),'frontmost':actual})
            if actual:break
            ops.check_time();sleep(.05)
        w.require(trace['observations'][-1]['frontmost'],'original App did not become frontmost')
    bound('after-autonomous-focus');ops.check_time()
    again=ops.main(expected)
    w.require(ops.b.equal(main,again) and ops.front(),'focus final original main/frontmost changed')
    ops.check_time()


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
        if action=='focus' and value.get('autonomous_focus_route') is not None:
            w.require(value['autonomous_focus_route']=={'version':'autonomous-owned-focus/v1','per_incarnation_cap_seconds':45,'mechanism':'AXRaise+AXFrontmost'},'unselected autonomous focus route')
            w.require(context is None,'autonomous focus only before main journey')
            trace={'mechanism':'AXRaise+AXFrontmost','raise_attempted':False,'frontmost_attempted':False,'observations':[]}
            ops=None
            try:
                ops=NativeFocus(backend,pid,app,trace)
                autonomous_focus(ops,bound,window,trace)
            except BaseException as error:trace['error']=str(error);raise
            finally:
                if ops is not None:ops.close()
                write_result(root/f"window-helper-{request['sequence']:03d}.focus.json",trace)
        elif action=='focus':
            trace={'activation':None,'observations':[]}
            def focused():
                value=w.frontmost(backend,app)
                trace['observations'].append({'at':w.d.now(),'frontmost':value})
                return value
            try:
                if not focused():
                    bound('before-focus-activation')
                    trace['activation']=activate_original_app(pid)
                    w.require(trace['activation']['request_sent'],'owned App activation request refused')
                    end=time.monotonic()+0.6
                    while True:
                        if focused():break
                        w.require(time.monotonic()<end,'owned App did not become frontmost')
                        time.sleep(0.05)
            except BaseException as error:
                trace['error']=str(error);raise
            finally:
                write_result(root/f"window-helper-{request['sequence']:03d}.focus.json",trace)
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
            events=[];event_routes=[]
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
                    if action=='click':
                        # CGEventPostToPid routes to the process; carry only the
                        # already verified window ID in both SDK mouse-window fields.
                        field(e,91,window['window_id']) # kCGMouseEventWindowUnderMousePointer
                        field(e,92,window['window_id']) # ...ThatCanHandleThisEvent
                        event_routes.append({'pid':pid,'window_under_pointer':window['window_id'],
                                             'window_that_can_handle_event':window['window_id']})
                    post(pid,e)
            finally:
                for e in events:backend.c.CFRelease(e)
        w.require(backend.identity(pid)==expected,'App identity changed after input')
        # Posting/AX return codes are not effect proof. Keeper captures and agent
        # must read the actual effect before accepting a subsequent action.
        result={'at':w.d.now(),'action':action,'sequence':request['sequence'],'posted_or_focus_observed':True,'effect_requires_fresh_capture_read':True,
                'event_routes':event_routes if action!='focus' else [],
                'routing_limits':'Explicit owned-window annotation is delivery intent, not proof the target received or acted on the event.'}
        write_result(root/f"window-helper-{request['sequence']:03d}.result.json",result)
    finally:backend.close()
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--request',type=Path,required=True);p.add_argument('--sha256',required=True);a=p.parse_args();main(a.request,a.sha256)
