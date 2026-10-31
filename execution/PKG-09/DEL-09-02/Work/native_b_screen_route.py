"""Fixed B-only operator-assisted native UI route; no fabricated AX/source rows."""
import hashlib,importlib.util,json,os,re,time
from pathlib import Path
HERE=Path(__file__).resolve()
s=importlib.util.spec_from_file_location('owned_B_window',HERE.with_name('native_b_window.py'));w=importlib.util.module_from_spec(s);s.loader.exec_module(w)
TARGETS={'host-diagnostics','lifecycle','raw-envelopes','connection-access'}

def read_control(path,root):
    require=w.require;info=w.private_file(path,0o600)
    require(path.parent==root and info.st_size<=256*1024,'screen control outside root/oversize')
    return w.private_json(path,256*1024)

class ScreenSession:
    def __init__(self,run,b):self.run=run;self.b=b;self.window=w.WindowRoute(run);self.step=0;self.pending_effect=False
    def next_control(self,phase,extra=None):
        self.run.alive();self.step+=1;w.require(self.step<=48,'B UI step bound exhausted')
        frame=self.window.last or self.window.capture();name=f'screen-control-{self.step:03d}.json'
        prompt={'at':self.b.now(),'phase':phase,'control_file':str(self.run.root/name),'candidate':self.run.value['candidate_key'],
                'admission_sha256':self.run.admission_sha,'frame':frame,'effect_readback_required':self.pending_effect,
                'allowed_actions':['observe','capture','focus','click-disclosure','scroll','refuse']+(['click-stop'] if phase=='stop' else []),
                'limits':'Read ONLY verified owned-window image. Transcribe actual complete displayed strings/JSON; never fill missing source/generation/requests from expected values. Agent act, not personal human act.',**(extra or {})}
        path=self.run.root/name
        w.require(not os.path.lexists(path),'prequeued screen input refused; read this effect first')
        self.run.record(f'screen-prompt-{self.step:03d}.json',prompt);self.run.report({'event':'native_screen_operator_step','prompt':prompt})
        while not os.path.lexists(path):
            self.run.alive();time.sleep(0.1)
        control=read_control(path,self.run.root)
        w.require(control.get('candidate')==self.run.value['candidate_key'] and control.get('admission_sha256')==self.run.admission_sha
                  and control.get('capture_sha256')==frame['sha256'],'screen control binding differs')
        if self.pending_effect and control.get('action')!='refuse':
            effect=control.get('previous_effect')
            w.require(isinstance(effect,dict) and effect.get('expected') is True and isinstance(effect.get('observed'),str) and 0<len(effect['observed'])<=2048,'actual expected effect must be read from this capture; unknown means refuse')
            self.run.safe_log('screen_effect_readback',capture_sha256=frame['sha256'],operator_observation=effect)
            self.pending_effect=False
        return control,frame
    def observe(self,phase='diagnostics',stop=False):
        # Every call begins with a fresh bound capture; earlier frame references
        # remain evidence only, never authority for another input.
        minimum_frame=self.window.sequence+1
        self.window.capture()
        while True:
            c,frame=self.next_control(phase);action=c.get('action')
            if action=='refuse':raise RuntimeError('operator cannot establish native observation/effect: '+str(c.get('reason','unspecified'))[:2048])
            if action=='capture':self.window.capture();continue
            if action=='observe':
                w.require(not stop,'Stop action not observed/sent')
                refs=c.get('frames');strings=c.get('strings')
                w.require(isinstance(refs,list) and refs and all(type(n) is int and minimum_frame<=n and n in self.window.frames for n in refs),'transcript capture references unavailable')
                w.require(frame['sequence'] in refs,'current capture missing from observation')
                w.require(isinstance(strings,list) and strings and all(isinstance(x,str) for x in strings)
                          and sum(map(len,strings))<=200000,'complete displayed text required')
                w.require(c.get('complete_sections')==['state-generation','lifecycle-clientRequests','raw-envelopes'] and c.get('unreadable') is False, 'do not infer missing/unclear displayed diagnostics')
                observed=self.b.decode_diagnostics(strings)
                observed['observation_provenance']={'kind':'agent-transcribed-owned-native-UI','frames':[self.window.frames[n] for n in refs],
                    'limits':'Displayed text transcribed by agent; no machine-native snapshot or personal-human-act claim.'}
                self.run.record(f'screen-observation-{self.step:03d}.json',{'strings':strings,'decoded':observed})
                return observed
            if action=='focus':input_action='focus';position=None;delta=None
            elif action=='scroll':input_action='scroll';position=c.get('point');delta=c.get('delta')
            elif action=='click-disclosure':
                w.require(c.get('target') in TARGETS,'non-B UI target refused');input_action='click';position=c.get('point');delta=None
            elif action=='click-stop':
                w.require(stop and phase=='stop' and self.run.generation is not None and not self.run.stop_requested,'Stop click unavailable/repeated')
                input_action='click';position=c.get('point');delta=None
            else:raise RuntimeError('screen action outside fixed B route')
            if input_action!='focus':w.require(isinstance(position,list) and len(position)==2,'current image point required')
            try:
                if action=='click-stop':self.run.stop_requested=True # no ambiguous repeated Stop
                self.pending_effect=True # ambiguous helper failure still requires effect readback
                self.window.input(input_action,frame,position,delta)
                self.pending_effect=True
                self.run.safe_log('screen_input_attempt',action=action,target=c.get('target'),actor=self.b.ACTOR)
                if action=='click-stop':return
            except w.Reobserve:
                self.pending_effect=False # reobserve proves no input event was posted
                if action=='click-stop':self.run.stop_requested=False # proven no event posted
                self.run.safe_log('screen_reobserve_before_input',action=action)
                continue


def make_run(b):
    class ScreenRun(b.Run):
        def __init__(self,*args,**kwargs):
            super().__init__(*args,**kwargs);self.screen=ScreenSession(self,b)
        def extra_cleanup_ready(self):return self.screen.window.helpers_settled()
        def held_status(self,error):
            status=super().held_status(error)
            helper=self.screen.window.helper
            status['window_helper']={'pid':helper.pid,'settlement':'unknown; retained Child'} if helper is not None else {'settlement':'no live held helper'}
            status['screen_step']=self.screen.step
            status['last_verified_capture']=self.screen.window.last
            return status
        def diagnostics(self):
            observed=self.screen.observe('cleanup-diagnostics' if self.cleanup else 'diagnostics')
            self.last_diagnostics=observed;return observed
        def observe_ready(self,qualification=True):
            end=min(time.monotonic()+15,self.cleanup_end if self.cleanup else self.work_end)
            while True:
                try:
                    observed=self.diagnostics();break
                except w.WindowUnavailable as error:
                    if self.screen.window.frames or time.monotonic()>=end:
                        self.screen.window.failure=str(error);raise
                    self.alive();time.sleep(0.1)
            gen=b.source_gate(observed,self.value);self.generation=gen
            if qualification:
                b.reject_permanent_witness_failure(observed,gen);b.ready_gate(observed,self.value)
            self.record('ready-observation.json' if qualification else 'cleanup-source-observation.json',observed)
            return gen
        def cleanup_attempt(self):
            if self.screen.window.failure and self.generation is None:
                raise RuntimeError('owned-window observation unavailable with no source binding; no capture retry: '+self.screen.window.failure)
            return super().cleanup_attempt()
        def request_stop_ui(self):
            self.screen.observe('stop',stop=True)
        def request_quit_ui(self):
            # Native owned-menu address, not keyboard focus or cached coordinates.
            self.alive()
            backend=w.d.NativeBackend()
            try:before=w.d.bound_identity(self,backend)
            finally:backend.close()
            app=self.ax.app;title=self.ax.attr(app,'AXTitle');bar=self.ax.attr(app,'AXMenuBar')
            b.require(bar is not None,'owned menu unavailable')
            items=self.ax.attr(bar,'AXChildren') or []
            b.require(len(items)<=32,'menu root bound')
            own=[e for e in items if self.ax.attr(e,'AXRole')=='AXMenuBarItem' and self.ax.attr(e,'AXTitle')==title]
            b.require(len(own)==1,'owned App menu ambiguous')
            stack=[(own[0],0)];seen=[];matches=[];count=0
            while stack:
                e,depth=stack.pop();count+=1;b.require(count<=150,'menu traversal bound')
                self.ax.own(e)
                if any(self.ax.c.CFEqual(e,old) for old in seen):continue
                seen.append(e);role=self.ax.attr(e,'AXRole')
                if self.ax.c.CFEqual(e,app) or role not in ('AXMenuBarItem','AXMenu','AXMenuItem'):continue
                b.require(depth<=6,'menu depth bound')
                if role=='AXMenuItem':
                    if self.ax.attr(e,'AXTitle')=='Quit '+title and self.ax.attr(e,'AXEnabled') is True:matches.append(e)
                    continue
                children=self.ax.attr(e,'AXChildren') or [];b.require(len(children)<=64,'menu child bound')
                stack.extend((child,depth+1) for child in children)
            b.require(len(matches)==1,'owned Quit unavailable/ambiguous')
            self.record('screen-route-native-menu-quit.json',{'at':b.now(),'title':'Quit '+title,'actor':b.ACTOR})
            backend=w.d.NativeBackend()
            try:b.require(w.d.bound_identity(self,backend)==before,'App identity changed before native Quit')
            finally:backend.close()
            self.ax.press(matches[0])
        def wait_for_quit_exit(self):
            # No automatic acceptance of unexpected live-work effects. Preserve
            # the genuine statement for a concrete owner/operator disposition.
            b.require(self.supplier_settled and self.quit_requested,'Quit lacks settlement gates')
            while time.monotonic()<self.cleanup_end:
                if self.reservation.observe() is not None:
                    b.require(self.extra_cleanup_ready(),'window helper unsettled; retain original App reservation')
                    return self.reservation.reap(True,True)
                try:
                    question=self.dialog('Quit Chirality','Quit')
                    if question:
                        rows,_=question;statement=self.ax.text(rows)
                        self.record('unexpected-quit-question.json',{'statement':statement,'actor':b.ACTOR})
                        raise RuntimeError('unexpected Quit question requires explicit confined-effects disposition; no automatic confirmation')
                except BaseException:
                    if self.reservation.observe() is not None:continue
                    raise
                time.sleep(0.1)
            raise RuntimeError('native Quit did not exit by deadline')
    return ScreenRun
