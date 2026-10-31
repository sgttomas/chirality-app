"""One owned main-window capture/input boundary; no desktop or C-plugin path."""
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


def tools_identity():
    result={}
    for path in (CAPTURE,Path(sys.executable).resolve()):
        info=path.stat();require(path.is_file() and not info.st_mode&(stat.S_ISUID|stat.S_ISGID),'unexpected helper executable')
        if path==CAPTURE:require(info.st_uid==0,'capture tool is not system-owned')
        result[str(path)]={'sha256':sha(path),'device':info.st_dev,'inode':info.st_ino,'mode':info.st_mode,'uid':info.st_uid}
    return result

def select_main(backend,pid):
    matches=[];visible=0
    rows=backend.window_rows();require(len(rows)<=d.MAX_WINDOWS,'WindowServer reference bound')
    for row in rows:
        if backend.owner_pid(row)!=pid:continue # no foreign data decoded/retained
        value=backend.decode_owned_window(row,True)
        if value['layer']==0 and value['on_screen'] is True:visible+=1
        if value['title']==TITLE and value['layer']==0 and value['on_screen'] is True:
            number=value['number'];bounds=value['bounds']
            require(type(number) in (int,float) and 0<number<=4294967295 and int(number)==number,'invalid owned window ID')
            require(set(bounds)=={'X','Y','Width','Height'} and all(type(v) in (int,float) and math.isfinite(v) for v in bounds.values()),'invalid own bounds')
            require(100<=bounds['Width']<=10000 and 100<=bounds['Height']<=10000,'own window size outside bound')
            matches.append({'window_id':int(number),'title':TITLE,'bounds':bounds,'on_screen':True,'layer':0})
    if not matches:raise WindowUnavailable('exact owned visible main window unavailable')
    require(len(matches)==1,'exact owned visible main window ambiguous')
    return {**matches[0],'own_visible_layer0_count':visible}

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
    return [window['bounds']['X']+x/image['scale'],window['bounds']['Y']+y/image['scale']]

class WindowRoute:
    def __init__(self,run):
        self.run=run;self.sequence=0;self.frames={};self.helper=None;self.last=None;self.failure=None
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
        require(min(self.run.cleanup_end, self.run.cleanup_end if self.run.cleanup else self.run.work_end)-time.monotonic()>6,'window helper lacks bounded completion allowance')
        root=self.run.root;number=request['sequence'];name=f'window-helper-{number:03d}'
        request_path=root/(name+'.json');request['admission_sha256']=self.run.admission_sha
        request['recorded_at']=d.now()
        fd=os.open(request_path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        with os.fdopen(fd,'w') as f:json.dump(request,f,indent=2)
        for filename,digest in self.run.value['window_route']['helper_sources'].items():
            require(sha(private_path(root,filename))==digest,'protected window helper source changed')
        require(tools_identity()==self.run.value['window_route']['tools'],'helper executable identity changed')
        command=[str(Path(sys.executable).resolve()),'-I','-S','-B',str(root/HELPER.name),'--request',str(request_path),'--sha256',sha(request_path)]
        env={'HOME':str(Path.home()),'PATH':'/usr/bin:/bin:/usr/sbin:/sbin','LANG':'en_US.UTF-8',
             'TMPDIR':str(root/'tmp'),'CODEX_HOME':str(root/'codex-home'),'PYTHONDONTWRITEBYTECODE':'1'}
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
        window=select_main(backend,identity['pid'])
        return identity,window
    def capture(self):
        self.run.alive();require(self.sequence<64,'window operation bound exhausted')
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
            self.run.record(f'window-{number:03d}.json',receipt)
            self.frames[number]=receipt;self.last=receipt;self.failure=None
            self.run.report({'event':'owned_window_ready_for_agent_read','receipt':receipt})
            return receipt
        except WindowUnavailable:
            raise
        except BaseException as error:
            self.failure=str(error);raise
        finally:backend.close()
    def input(self,action,frame,position=None,delta=None):
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
            if action!='focus':require(frontmost(backend,app) and window['own_visible_layer0_count']==1,'exact main-window focus unavailable')
            require(action in ('focus','click','scroll'),'unsupported ordinary UI action')
            self.sequence+=1;require(self.sequence<=64,'window operation bound exhausted')
            request={'action':action,'sequence':self.sequence,'identity':identity,'window':window,'capture_sha256':frame['sha256']}
            if action=='click':request['point']=point(window,frame['image'],*position)
            if action=='scroll':
                require(type(delta) is int and 0<abs(delta)<=400,'scroll outside bound')
                request['delta']=delta
                request['point']=point(window,frame['image'],*position)
            self.invoke(request)
            after,after_window=self.bound_window(backend)
            require(after==identity and after_window['window_id']==window['window_id'] and after_window['bounds']==window['bounds'],'post-input binding changed; effect unknown')
        finally:backend.close()
        return self.capture() # Next action requires reading this actual effect.

def private_path(root,filename):
    require(Path(filename).name==filename,'helper path escape')
    path=root/filename;private_file(path,0o600);return path

def configuration():
    sources=(HERE,HELPER,HERE.with_name('native_b_diagnostic.py'))
    return {'version':'chirality.owned-window-ui/v1','tools':tools_identity(),'helper_sources':{p.name:sha(p) for p in sources}}

def stage(root,config):
    for filename,digest in config['helper_sources'].items():
        source=HERE.with_name(filename);require(sha(source)==digest,'window source changed before staging')
        fd=os.open(root/filename,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        with os.fdopen(fd,'wb') as f:f.write(source.read_bytes())
