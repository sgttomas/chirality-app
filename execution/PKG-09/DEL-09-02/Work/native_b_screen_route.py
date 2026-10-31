"""Fixed B-only operator-assisted native UI route; no fabricated AX/source rows."""
import hashlib,importlib.util,json,os,re,time
from pathlib import Path
HERE=Path(__file__).resolve()
s=importlib.util.spec_from_file_location('owned_B_window',HERE.with_name('native_b_window.py'));w=importlib.util.module_from_spec(s);s.loader.exec_module(w)
TARGETS={'host-diagnostics','lifecycle','raw-envelopes','connection-access','more-tools-link','connection-access-link'}
# Prepared caps, not measured native latency. Work after Stop retains 40s for exit/failure handling.
PHASE_BUDGETS={'ready':(60,205),'recheck':(35,170),'cleanup-source':(35,135),'stop':(20,115),'stop-confirmation':(30,85),'settlement':(45,40)}

def read_control(path,root):
    require=w.require;info=w.private_file(path,0o600)
    require(path.parent==root and info.st_size<=256*1024,'screen control outside root/oversize')
    return w.private_json(path,256*1024)

def validate_stop_question(title,text,generation,expected_home):
    w.require(title=='Stop Codex' and isinstance(text,str) and 0<len(text)<=16384,'actual Stop title/question unavailable')
    w.require(generation['home']==expected_home,'full generation account source differs')
    normalized=' '.join(text.split())
    prefix='Stop Codex for this home? Home: account · App session '+generation['appSession']+' · Codex process start '+str(generation['spawnCounter'])+' · state '
    match=re.match(re.escape(prefix)+r'(ready|handshaking|halted|unexpected-exit)\b',normalized)
    w.require(match is not None,'Stop question source/generation differs')
    state=match.group(1)
    before_time=[prefix+state]
    if state!='ready':before_time.append('Codex is '+state+', not ready: live work cannot be observed and nothing is sent to it; only the process is stopped.')
    before_time.extend(['Observed: no live turns, waiting requests, delegated agents or workflow runs in force.',
                       'Stop Codex stops this Codex process.',
                       'None observed is not none: coverage is not complete.',
                       'This is your operational choice, not a recorded act. If you confirm, the App writes the stop and each interrupt to its recovery ledger before sending; what the ledger accepts can be read after a relaunch.'])
    suffix='Stop Codex proceeds; Keep Codex running (the default) and Cancel change nothing.'
    pattern=re.escape(' '.join(before_time))+r' Observed at ([0-9T:.+Z-]+)\. '+re.escape(suffix)
    whole=re.fullmatch(pattern,normalized)
    w.require(whole is not None,'unexpected/missing/digest-only Stop effects or coverage')
    timestamp=__import__('datetime').datetime.fromisoformat(whole.group(1).replace('Z','+00:00'))
    w.require(timestamp.tzinfo is not None,'Stop observation timestamp unavailable')
    return normalized


class ScreenSession:
    def __init__(self,run,b):self.run=run;self.b=b;self.window=w.WindowRoute(run);self.step=0;self.pending_effect=False;self.phase_deadline=None;self.active_phase=None
    def begin_phase(self,phase):
        if self.active_phase==phase:
            self.phase_alive();return # repeated observations cannot extend this phase
        duration,reserve=PHASE_BUDGETS[phase]
        now=time.monotonic()
        w.require(self.run.cleanup_end-now>=duration+reserve,'insufficient full phase/cleanup budget for '+phase)
        self.phase_deadline=now+duration;self.active_phase=phase
        self.run.ui_deadline=self.phase_deadline
    def phase_alive(self):
        self.run.alive()
        if self.phase_deadline is not None:w.require(time.monotonic()<self.phase_deadline,'native UI phase budget exhausted')
    def next_control(self,phase,extra=None):
        self.phase_alive();self.step+=1;w.require(self.step<=48,'B UI step bound exhausted')
        frame=self.window.last or self.window.capture();name=f'screen-control-{self.step:03d}.json'
        prompt={'at':self.b.now(),'phase':phase,'control_file':str(self.run.root/name),'candidate':self.run.value['candidate_key'],
                'admission_sha256':self.run.admission_sha,'frame':frame,'effect_readback_required':self.pending_effect,'phase_seconds_remaining':None if self.phase_deadline is None else max(0,self.phase_deadline-time.monotonic()),
                'control_publication':'Write a private owned single-link0600 temporary file, then atomically rename to the named control path. Never write the final path in place.',
                'allowed_actions':['observe','capture','focus','click-disclosure','scroll','refuse']+(['click-stop'] if phase=='stop' else []),
                'limits':'Read ONLY verified owned-window image. Transcribe actual complete displayed strings/JSON; never fill missing source/generation/requests from expected values. Agent act, not personal human act.',**(extra or {})}
        path=self.run.root/name
        w.require(not os.path.lexists(path),'prequeued screen input refused; read this effect first')
        self.run.record(f'screen-prompt-{self.step:03d}.json',prompt);self.run.report({'event':'native_screen_operator_step','prompt':prompt})
        while not os.path.lexists(path):
            self.phase_alive();time.sleep(0.1)
        control=read_control(path,self.run.root)
        w.require(control.get('candidate')==self.run.value['candidate_key'] and control.get('admission_sha256')==self.run.admission_sha
                  and control.get('capture_sha256')==frame['sha256'],'screen control binding differs')
        if self.pending_effect and control.get('action') not in ('refuse','capture'):
            effect=control.get('previous_effect')
            w.require(isinstance(effect,dict) and effect.get('expected') is True and isinstance(effect.get('observed'),str) and 0<len(effect['observed'])<=2048,'actual expected effect must be read from this capture; unknown means refuse')
            self.run.safe_log('screen_effect_readback',capture_sha256=frame['sha256'],operator_observation=effect)
            self.pending_effect=False
        return control,frame
    def observe(self,phase='recheck',stop=False,protocol=True,initial_frame=None):
        # Every call begins with a fresh bound capture; earlier frame references
        # remain evidence only, never authority for another input.
        self.begin_phase(phase)
        if initial_frame is None:
            minimum_frame=self.window.sequence+1;self.window.capture()
        else:
            w.require(self.window.last is initial_frame,'initial verified frame no longer current')
            minimum_frame=initial_frame['sequence']
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
                required=['state-generation','lifecycle-clientRequests']
                accepted=[required+['raw-envelopes']] if protocol else [required,required+['raw-envelopes']]
                w.require(c.get('complete_sections') in accepted and c.get('unreadable') is False, 'do not infer missing/unclear displayed diagnostics')
                observed=self.b.decode_diagnostics(strings,protocol=protocol)
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
                self.window.input(input_action,frame,position,delta,stop_generation=self.run.generation if action=='click-stop' else None)
                self.pending_effect=True
                self.run.safe_log('screen_input_attempt',action=action,target=c.get('target'),actor=self.b.ACTOR)
                if action=='click-stop':return
            except w.Reobserve:
                self.pending_effect=False # reobserve proves no input event was posted
                if action=='click-stop':self.run.stop_requested=False # proven no event posted
                self.run.safe_log('screen_reobserve_before_input',action=action)
                continue

    def confirm_stop(self,generation):
        w.require(self.window.modal_active and not self.window.modal_confirm_attempted,'modal confirmation unavailable/already attempted')
        w.require(self.window.stop_context is not None and self.window.stop_context['generation']==generation
                  and self.window.stop_context['posted'] is True,'no posted bound Stop for modal observation')
        self.begin_phase('stop-confirmation')
        end=min(time.monotonic()+8,self.phase_deadline)
        while True:
            try:self.window.capture();break
            except w.WindowUnavailable:
                self.phase_alive()
                if time.monotonic()>=end:raise RuntimeError('distinct owned Stop modal unavailable; unsupported sheet/relationship, no substitution')
                time.sleep(0.1)
        while True:
            c,frame=self.next_control('stop-confirmation',{'allowed_actions':['capture','focus','confirm-stop','refuse'],
                'bound_full_generation':generation,'presentation_limit':'Physical home is bound by prior full generation; actual modal must show matching account/session/spawn and exact effects. Do not infer missing text.'})
            w.require(frame.get('target')=='stop-modal','main-window image cannot substitute for Stop modal')
            action=c.get('action')
            if action=='refuse':raise RuntimeError('Stop modal scope refused: '+str(c.get('reason','unknown'))[:2048])
            if action=='capture':self.window.capture();continue
            if action=='focus':
                self.pending_effect=True;self.window.input('focus',frame);continue
            w.require(action=='confirm-stop' and c.get('complete_question') is True and c.get('unreadable') is False
                      and c.get('button_label')=='Stop Codex','actual complete same-source modal confirmation required')
            statement=validate_stop_question(c.get('question_title'),c.get('question_text'),generation,self.run.value['expected_generation_home'])
            point=c.get('point');w.require(isinstance(point,list) and len(point)==2,'current modal button point required')
            self.run.record(f'stop-modal-question-{self.step:03d}.json',{'generation':generation,'statement':statement,
                'capture':frame,'actor':self.b.ACTOR,'provenance':'agent transcription of actual owned modal; not supplier JSON/personal human act'})
            try:
                self.run.stop_confirmed=True;self.pending_effect=True
                self.window.input('click',frame,point)
                self.run.record('stop-confirmation.json',{'generation':generation,'statement':statement,'capture':frame,'actor':self.b.ACTOR})
                self.run.safe_log('native_stop_confirmation_input_posted',generation=generation,actor=self.b.ACTOR)
                return
            except w.Reobserve:
                self.run.stop_confirmed=False;self.pending_effect=False
                self.run.safe_log('stop_modal_changed_before_input_no_event')



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
            phase='settlement' if self.stop_confirmed else ('cleanup-source' if self.cleanup else 'recheck')
            observed=self.screen.observe(phase,protocol=not self.cleanup)
            self.last_diagnostics=observed;return observed
        def observe_ready(self,qualification=True):
            initial=None
            if qualification:
                end=min(time.monotonic()+15,self.work_end);self.ui_deadline=end
                while True:
                    try:initial=self.screen.window.capture();break
                    except w.WindowUnavailable as error:
                        if time.monotonic()>=end:self.screen.window.failure=str(error);raise
                        self.alive();time.sleep(0.1)
            observed=self.screen.observe('ready' if qualification else 'cleanup-source',protocol=qualification,initial_frame=initial)
            self.last_diagnostics=observed
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
        def confirm_stop_ui(self,gen):
            self.screen.confirm_stop(gen)
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
