"""Owned main window and one derived Stop modal; no desktop or C-plugin path."""
import binascii,hashlib,importlib.util,json,math,os,stat,struct,subprocess,sys,time
from pathlib import Path
HERE=Path(__file__).resolve()
spec=importlib.util.spec_from_file_location('window_identity_primitives',HERE.with_name('native_b_diagnostic.py'))
d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
require=d.require
TITLE='Chirality App v4 — walking skeleton'
CAPTURE=Path('/usr/sbin/screencapture')
HELPER=HERE.with_name('native_b_window_helper.py')
MAX_IMAGE=32*1024*1024
MAX_OPERATIONS=96
class Reobserve(RuntimeError):pass
class WindowUnavailable(RuntimeError):pass

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def private_file(path,mode=None):
    path=Path(path);info=path.lstat()
    require(path.is_absolute() and path.parent.resolve()==path.parent and stat.S_ISREG(info.st_mode)
            and info.st_uid==os.getuid() and info.st_nlink==1,'owned plain file required')
    if mode is not None:require(stat.S_IMODE(info.st_mode)==mode,'private file mode differs')
    return info

def private_json(path,limit,expected_sha=None):
    private_file(path,0o600)
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    try:
        before=os.fstat(fd)
        require(stat.S_ISREG(before.st_mode) and before.st_uid==os.getuid() and before.st_nlink==1
                and stat.S_IMODE(before.st_mode)==0o600 and 0<before.st_size<=limit,'private JSON descriptor invalid')
        with os.fdopen(fd,'rb',closefd=False) as stream:raw=stream.read(limit+1)
        after=os.fstat(fd);named=Path(path).lstat()
        stamp=lambda i:(i.st_dev,i.st_ino,i.st_mode,i.st_uid,i.st_nlink,i.st_size,i.st_mtime_ns,i.st_ctime_ns)
        require(len(raw)==before.st_size and stamp(before)==stamp(after)==stamp(named),'private JSON changed while reading')
        if expected_sha is not None:require(hashlib.sha256(raw).hexdigest()==expected_sha,'private JSON digest changed')
        def unique(pairs):
            result={}
            for key,value in pairs:
                require(key not in result,'duplicate JSON control field');result[key]=value
            return result
        return json.loads(raw,object_pairs_hook=unique)
    finally:os.close(fd)


def python_prefixes():
    prefixes=sorted({str(Path(sys.prefix).resolve()),str(Path(sys.base_prefix).resolve())})
    executable=Path(sys.executable).resolve()
    require(all(Path(p).is_absolute() and Path(p).is_dir() and Path(p) not in (Path('/'),Path.home()) for p in prefixes)
            and any(executable.is_relative_to(Path(p)) for p in prefixes),'helper Python prefix unavailable')
    return prefixes


def tools_identity():
    result={}
    for path in (CAPTURE,Path(sys.executable).resolve()):
        info=path.stat();require(path.is_file() and not info.st_mode&(stat.S_ISUID|stat.S_ISGID),'unexpected helper executable')
        if path==CAPTURE:require(info.st_uid==0,'capture tool is not system-owned')
        result[str(path)]={'sha256':sha(path),'device':info.st_dev,'inode':info.st_ino,'mode':info.st_mode,'uid':info.st_uid}
    return result

def owned_inventory(backend,pid):
    result=[];rows=backend.window_rows();require(len(rows)<=d.MAX_WINDOWS,'WindowServer reference bound')
    for row in rows:
        if backend.owner_pid(row)!=pid:continue
        value=backend.decode_owned_window(row,True);number=value['number'];bounds=value['bounds']
        require(type(number) in (int,float) and 0<number<=4294967295 and int(number)==number,'invalid owned window ID')
        require(set(bounds)=={'X','Y','Width','Height'} and all(type(v) in (int,float) and math.isfinite(v) for v in bounds.values()),'invalid own bounds')
        require(len(result)<32,'owned window inventory bound')
        result.append({'window_id':int(number),'title':value['title'],'bounds':bounds,'on_screen':value['on_screen'], 'layer':value['layer']})
    return result

def select_main(backend,pid):
    rows=owned_inventory(backend,pid)
    matches=[r for r in rows if r['title']==TITLE and r['layer']==0 and r['on_screen'] is True]
    if not matches:raise WindowUnavailable('exact owned visible main window unavailable')
    require(len(matches)==1,'exact owned visible main window ambiguous')
    require(100<=matches[0]['bounds']['Width']<=10000 and 100<=matches[0]['bounds']['Height']<=10000,'own window size outside bound')
    return {**matches[0],'own_visible_layer0_count':sum(r['layer']==0 and r['on_screen'] is True for r in rows)}

def modal_relation(backend,pid,candidate_id,main_id):
    # Existing A used this window-number bridge. No capability probe is run in
    # preparation; unavailable AX metadata remains an explicit observation limit.
    import ctypes as C
    try:get_window=backend.a._AXUIElementGetWindow
    except AttributeError:return {'status':'unavailable','reason':'AX window-number bridge unavailable'}
    get_window.restype=C.c_int;get_window.argtypes=[C.c_void_p,C.POINTER(C.c_uint32)]
    app=backend.app(pid);seen=[];matches=[];sheet_without_row=False
    def number(element):
        out=C.c_uint32();rc=get_window(element,C.byref(out));return rc,int(out.value)
    for name in ('AXFocusedWindow','AXWindows','AXChildren'):
        value,refs=backend.attribute(app,name)
        if value['return_code']!=0:continue
        require(len(refs)<=32,'modal AX reference bound')
        for element in refs:
            if backend.equal(element,app) or any(backend.equal(element,e) for e in seen):continue
            seen.append(element);rc,owner=backend.owner(element)
            require(rc==0 and owner==pid,'modal AX ownership unavailable/foreign')
            role,_=backend.attribute(element,'AXRole')
            if role.get('value') not in ('AXWindow','AXDialog','AXSheet'):continue
            map_rc,window_id=number(element)
            if role.get('value')=='AXSheet' and (map_rc!=0 or not window_id or window_id==main_id):sheet_without_row=True
            if map_rc!=0 or window_id!=candidate_id:continue
            modal,_=backend.attribute(element,'AXModal');parent,parents=backend.attribute(element,'AXParent')
            require(not(modal['return_code']==0 and modal.get('value') is False),'exposed AX object is not modal')
            relation='unavailable'
            if parent['return_code']==0 and parents:
                require(len(parents)==1,'modal AX parent ambiguous')
                parent_rc,parent_pid=backend.owner(parents[0]);require(parent_rc==0 and parent_pid==pid,'modal AX parent foreign')
                if backend.equal(parents[0],app):relation='owned-application-parent'
                else:
                    prc,parent_id=number(parents[0]);require(prc==0 and parent_id==main_id,'modal parent is not original main window')
                    relation='original-main-window-parent'
            matches.append({'status':'exposed','role':role,'modal':modal,'parent_relation':relation,'window_id':window_id})
    require(len(matches)<=1,'modal AX relation ambiguous')
    if matches:return matches[0]
    require(not sheet_without_row,'AX sheet mapping does not establish a distinct selected WindowServer row; unsupported')
    return {'status':'unavailable','reason':'no matching AX modal relationship exposed'}

def select_modal(backend,pid,context):
    require(context.get('posted') is True and context['identity']['pid']==pid,'no bound posted Stop context')
    rows=owned_inventory(backend,pid);main_id=context['main']['window_id']
    main=[r for r in rows if r['window_id']==main_id]
    require(len(main)==1 and main[0]['title']==TITLE and main[0]['bounds']==context['main']['bounds'],'original main window changed; no substitution')
    before={r['window_id'] for r in context['before_inventory'] if r['on_screen'] is True}
    new=[r for r in rows if r['on_screen'] is True and r['window_id'] not in before and r['window_id']!=main_id]
    if not new:
        raise WindowUnavailable('no distinct newly visible owned Stop modal; sheets without a separate row are unsupported')
    require(len(new)==1,'new owned modal candidates ambiguous')
    candidate=new[0]
    require(candidate['title'] in ('','Stop Codex') and candidate['layer'] in (0,8),'unexpected modal title/layer')
    require(80<=candidate['bounds']['Width']<=10000 and 80<=candidate['bounds']['Height']<=10000,'modal bounds unsupported')
    visible=[r for r in rows if r['on_screen'] is True]
    require(visible and visible[0]['window_id']==candidate['window_id'],'derived modal is not foremost owned window')
    return {**candidate,'own_visible_layer0_count':sum(r['layer']==0 and r['on_screen'] is True for r in rows),
            'derivation':'unique newly-visible owned window after bound Stop; presentation not yet approved'}


def frontmost(backend,app):
    value,refs=backend.attribute(app,'AXFrontmost')
    require(value['return_code']==0 and value['type']['name']=='CFBoolean' and not refs,'own App focus observation unavailable')
    return value['value'] is True

def png_geometry(path,window):
    info=private_file(path);require(24<=info.st_size<=MAX_IMAGE,'capture image missing/oversize')
    with Path(path).open('rb') as f:header=f.read(24)
    require(header[:8]==b'\x89PNG\r\n\x1a\n' and header[12:16]==b'IHDR','capture is not PNG')
    width,height=struct.unpack('>II',header[16:24]);b=window['bounds']
    sx,sy=width/b['Width'],height/b['Height']
    require(width*height<=40_000_000 and sx in (1,2,3) and abs(sx-sy)<1e-6,'pixel/point mapping unavailable; no guessed offsets')
    raw=Path(path).read_bytes();offset=8;fingerprint=hashlib.sha256();chunks=0;ended=False
    while offset<len(raw):
        require(offset+12<=len(raw),'truncated PNG chunk')
        length=struct.unpack('>I',raw[offset:offset+4])[0];kind=raw[offset+4:offset+8];end=offset+12+length
        require(end<=len(raw) and length<=MAX_IMAGE,'PNG chunk exceeds image')
        data=raw[offset+8:offset+8+length];crc=struct.unpack('>I',raw[offset+8+length:end])[0]
        require(binascii.crc32(kind+data)&0xffffffff==crc,'PNG checksum differs')
        if kind not in (b'tEXt',b'zTXt',b'iTXt',b'tIME'):fingerprint.update(kind+data) # include palettes/color/geometry, ignore nonvisual text/time
        chunks+=1;require(chunks<=4096,'PNG chunk bound')
        offset=end
        if kind==b'IEND':ended=True;break
    require(ended and offset==len(raw),'PNG incomplete/trailing data')
    return {'width':width,'height':height,'scale':sx,'image_data_sha256':fingerprint.hexdigest()}

def point(window,image,x,y):
    require(type(x) in (int,float) and type(y) in (int,float) and math.isfinite(x) and math.isfinite(y),'invalid point')
    require(0<x<image['width'] and 0<y<image['height'],'point outside exact own image')
    local_x,local_y=x/image['scale'],y/image['scale']
    require(8<local_x<window['bounds']['Width']-8 and 40<local_y<window['bounds']['Height']-8,'point in title/resize band; content only')
    return [window['bounds']['X']+local_x,window['bounds']['Y']+local_y]

class WindowRoute:
    def __init__(self,run):
        self.run=run;self.sequence=0;self.frames={};self.helper=None;self.last=None;self.failure=None;self.stop_context=None;self.modal_active=False;self.modal_confirm_attempted=False;self.modal_window=None
    def helpers_settled(self):
        if self.helper is None:return True
        try:
            code=self.helper.wait(timeout=0)
            self.run.safe_log('window_helper_late_exit',return_code=code)
            self.helper=None;return True
        except subprocess.TimeoutExpired:return False
        except BaseException as error:
            self.run.safe_log('window_helper_observation_unknown',error=str(error));return False
    def invoke(self,request):
        require(self.helpers_settled(),'previous window helper settlement unknown; no second helper')
        require(min(self.run.cleanup_end, self.run.cleanup_end if self.run.cleanup else self.run.work_end, getattr(self.run,'ui_deadline',self.run.cleanup_end))-time.monotonic()>6,'window helper lacks bounded completion allowance')
        root=self.run.root;number=request['sequence'];name=f'window-helper-{number:03d}'
        request_path=root/(name+'.json');request['admission_sha256']=self.run.admission_sha
        request['recorded_at']=d.now()
        request['target']='stop-modal' if self.modal_active else 'main'
        if self.modal_active:
            request['stop_context_sha256']=sha(root/'stop-modal-context.json')
        fd=os.open(request_path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        with os.fdopen(fd,'w') as f:json.dump(request,f,indent=2)
        for filename,digest in self.run.value['window_route']['helper_sources'].items():
            require(sha(private_path(root,filename))==digest,'protected window helper source changed')
        require(tools_identity()==self.run.value['window_route']['tools'] and python_prefixes()==self.run.value['window_route']['python_prefixes'],'helper executable/runtime prefix identity changed')
        command=[str(Path(sys.executable).resolve()),'-I','-S','-B',str(root/HELPER.name),'--request',str(request_path),'--sha256',sha(request_path)]
        env={'HOME':str(Path.home()),'PATH':'/usr/bin:/bin:/usr/sbin:/sbin','LANG':'en_US.UTF-8',
             'TMPDIR':str(root/'helper-tmp'),'CODEX_HOME':str(root/'codex-home'),'PYTHONDONTWRITEBYTECODE':'1'}
        with (root/(name+'.stdout')).open('xb') as out,(root/(name+'.stderr')).open('xb') as err:
            self.helper=subprocess.Popen(command,env=env,stdin=subprocess.DEVNULL,stdout=out,stderr=err,close_fds=True,umask=0o077)
            child=self.helper
            try:code=child.wait(timeout=4)
            except subprocess.TimeoutExpired:
                # Only this retained capture/input helper, never the App/supplier.
                child.kill()
                try:code=child.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    self.run.safe_log('window_helper_held_unknown',pid=child.pid)
                    raise RuntimeError('owned window helper did not settle after timeout; retain keeper/slot')
                self.helper=None
                self.run.safe_log('window_helper_timeout',return_code=code)
                raise RuntimeError('window helper timed out; no input retry or capture acceptance')
            self.helper=None
        require(code==0,'window helper refused: inspect its scoped stderr/result')
    def bound_window(self,backend):
        identity=d.bound_identity(self.run,backend)
        window=select_modal(backend,identity['pid'],self.stop_context) if self.modal_active else select_main(backend,identity['pid'])
        if not self.modal_active and self.modal_confirm_attempted and self.modal_window:
            if any(r['window_id']==self.modal_window['window_id'] and r['on_screen'] is True for r in owned_inventory(backend,identity['pid'])):
                raise WindowUnavailable('Stop modal still visible after confirmation attempt; effect unavailable')
        return identity,window
    def capture(self):
        self.run.alive();require(self.sequence<MAX_OPERATIONS,'window operation bound exhausted')
        backend=d.NativeBackend()
        try:
            require(backend.screen_access(),'screen capture unavailable: preflight false; no prompt/fallback')
            identity,window=self.bound_window(backend)
            self.sequence+=1;number=self.sequence
            path=self.run.root/f'capture-{number:03d}.unverified.png'
            require(not os.path.lexists(path),'capture destination used')
            self.invoke({'action':'capture','sequence':number,'identity':identity,'window':window,'image_name':path.name})
            after,after_window=self.bound_window(backend)
            require(after==identity and after_window==window,'capture binding changed; quarantine image, do not view/export')
            image=png_geometry(path,window)
            accepted=self.run.root/f'window-{number:03d}.png'
            require(not os.path.lexists(accepted),'accepted capture destination used')
            path.rename(accepted);path=accepted
            receipt={'at':d.now(),'sequence':number,'path':str(path),'sha256':sha(path),'identity':identity,'window':window,'image':image,
                     'limits':'Exact owned window only, -a excludes attached windows, -o excludes shadow. Before/after checks are not atomic. Pixels are observations, not native source records.'}
            if self.modal_active:
                receipt['target']='stop-modal'
                receipt['modal_relation']=private_json(self.run.root/f'window-helper-{number:03d}.modal.json',32768)
                self.modal_window=window
            else:receipt['target']='main'
            self.run.record(f'window-{number:03d}.json',receipt)
            self.frames[number]=receipt;self.last=receipt;self.failure=None
            self.run.report({'event':'owned_window_ready_for_agent_read','receipt':receipt})
            return receipt
        except WindowUnavailable:
            raise
        except BaseException as error:
            self.failure=str(error);raise
        finally:backend.close()
    def input(self,action,frame,position=None,delta=None,stop_generation=None):
        self.run.alive();require(self.last is frame,'input requires latest captured window')
        require(time.time()-__import__('datetime').datetime.fromisoformat(frame['at']).timestamp()<45,'capture too old for input; reobserve')
        if action!='focus':
            fresh=self.capture()
            if fresh['image']!=frame['image'] or fresh['window']!=frame['window']:
                raise Reobserve('image changed before input; no event sent, reread fresh capture')
            frame=fresh
        backend=d.NativeBackend()
        try:
            identity,window=self.bound_window(backend)
            require(identity==frame['identity'] and window==frame['window'],'input window/geometry changed')
            app=backend.app(identity['pid'])
            owner_rc,owner=backend.owner(app);require(owner_rc==0 and owner==identity['pid'],'own AX App binding unavailable')
            if action!='focus':require(frontmost(backend,app) and (self.modal_active or window['own_visible_layer0_count']==1),'exact owned-window focus unavailable')
            if self.modal_active:require(action in ('focus','click'),'modal admits focus or one confirmed click only')
            require(action in ('focus','click','scroll'),'unsupported ordinary UI action')
            self.sequence+=1;require(self.sequence<=MAX_OPERATIONS,'window operation bound exhausted')
            request={'action':action,'sequence':self.sequence,'identity':identity,'window':window,'capture_sha256':frame['sha256']}
            if action=='click':request['point']=point(window,frame['image'],*position)
            if action=='scroll':
                require(type(delta) is int and 0<abs(delta)<=min(600,int(window['bounds']['Height'])-200),'scroll outside bounded overlapping page')
                request['delta']=delta
                request['point']=point(window,frame['image'],*position)
            context=None
            if stop_generation is not None:
                require(not self.modal_active and self.stop_context is None and stop_generation==self.run.generation,'Stop modal derivation already used/unbound')
                require(stop_generation['home']==self.run.value['expected_generation_home'],'Stop account source changed')
                require(isinstance(self.run.last_diagnostics,dict) and self.run.last_diagnostics.get('generation')==stop_generation,'fresh bound source observation unavailable before Stop')
                context={'identity':identity,'main':window,'before_inventory':owned_inventory(backend,identity['pid']),
                         'generation':stop_generation,'source_observation_sha256':hashlib.sha256(json.dumps(self.run.last_diagnostics,sort_keys=True).encode()).hexdigest(),'capture_sha256':frame['sha256'],
                         'operation_sequence':self.sequence,'at':d.now(),'posted':False}
                fd=os.open(self.run.root/'stop-click-intent.json',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
                with os.fdopen(fd,'w') as f:json.dump(context,f,indent=2)
            if self.modal_active and action=='click':
                require(not self.modal_confirm_attempted,'modal confirmation already attempted')
                self.modal_confirm_attempted=True
            self.invoke(request)
            if context is not None:
                result=private_json(self.run.root/f'window-helper-{self.sequence:03d}.result.json',16384)
                require(result['action']=='click' and result['sequence']==self.sequence and result['posted_or_focus_observed'] is True,'Stop posting result unavailable')
                context['posted']=True
                fd=os.open(self.run.root/'stop-modal-context.json',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
                with os.fdopen(fd,'w') as f:json.dump(context,f,indent=2)
                self.stop_context=context;self.modal_active=True
                return None # next observation is the derived modal, never a main-window substitute
            if self.modal_active and action=='click':
                require(d.bound_identity(self.run,backend)==identity,'App identity changed after modal confirmation')
                self.modal_active=False
                return None # subsequent diagnostics must observe actual dismissal/settlement
            after,after_window=self.bound_window(backend)
            require(after==identity and after_window['window_id']==window['window_id'] and after_window['bounds']==window['bounds'],'post-input binding changed; effect unknown')
        finally:backend.close()
        return self.capture() # Next action requires reading this actual effect.

def private_path(root,filename):
    require(Path(filename).name==filename,'helper path escape')
    path=root/filename;private_file(path,0o600);return path

def configuration():
    sources=(HERE,HELPER,HERE.with_name('native_b_diagnostic.py'))
    return {'version':'chirality.owned-window-ui/v2','modal_scope':'one-derived-stop-confirmation','tools':tools_identity(),'python_prefixes':python_prefixes(),'helper_sources':{p.name:sha(p) for p in sources}}

def stage(root,config):
    for filename,digest in config['helper_sources'].items():
        source=HERE.with_name(filename);require(sha(source)==digest,'window source changed before staging')
        fd=os.open(root/filename,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        with os.fdopen(fd,'wb') as f:f.write(source.read_bytes())
