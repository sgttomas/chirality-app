"""Fixed owned-AX B journey after verified activation; no image-operator fallback."""
import ctypes as C
import hashlib,json,time

CONTRACT={'version':'chirality.owned-AX-journey/v1','operator_control_files':False,
 'commands':['activate-original-app','open-host-diagnostics','open-lifecycle','open-raw-envelopes',
             'read-complete-diagnostics','open-connection','request-stop-once','confirm-exact-native-stop-once','owned-menu-quit'],
 'limits':'Only fixed role/title controls in the bound owned main/native Stop window. No caller PID, arbitrary selector, text injection or internal App command.'}
TEXT_ROLES=('AXStaticText','AXTextArea','AXTextField')

def require(ok,message):
    if not ok:raise RuntimeError(message)

def bounded_ax(Base):
    class OwnedAX(Base):
        def own(self,e):
            super().own(e)
            require(self.a.AXUIElementSetMessagingTimeout(e,0.2)==0,'owned AX element timeout unavailable')
        def attr(self,e,name):
            self.own(e)
            return super().attr(e,name)
        def value(self,p):
            if p:
                kind=self.c.CFGetTypeID(p)
                if kind==self.c.CFStringGetTypeID():
                    require(0<=self.c.CFStringGetLength(p)<=200000,'owned AX string exceeds bound')
                if kind==self.c.CFArrayGetTypeID():
                    require(0<=self.c.CFArrayGetCount(p)<900,'owned AX array exceeds bound')
            return super().value(p)
    return OwnedAX

def window_number(ax,element):
    ax.own(element)
    fn=ax.a._AXUIElementGetWindow
    fn.restype=C.c_int;fn.argtypes=[C.c_void_p,C.POINTER(C.c_uint32)]
    number=C.c_uint32();rc=fn(element,C.byref(number))
    require(rc==0 and number.value>0,'owned AX window number unavailable')
    return number.value

def web_control(rows,role,title,prefix=False):
    require(any(p['AXRole']=='AXWebArea' for _,p,_ in rows),'actual owned WebKit AXWebArea unavailable')
    matches=[e for e,p,web in rows if web and p['AXRole']==role and isinstance(p.get('AXTitle'),str)
             and (p['AXTitle'].startswith(title) if prefix else p['AXTitle']==title)
             and p.get('AXEnabled') is True]
    require(len(matches)==1,'owned enabled WebKit control unavailable/ambiguous: '+title)
    return matches[0]

def web_strings(rows):
    require(any(p['AXRole']=='AXWebArea' for _,p,_ in rows),'actual owned WebKit AXWebArea unavailable')
    strings=[]
    for _,p,web in rows:
        if web and p['AXRole'] in TEXT_ROLES:
            value=p.get('AXValue') if isinstance(p.get('AXValue'),str) else p.get('AXTitle')
            if isinstance(value,str) and value:strings.append(value)
    require(strings and sum(map(len,strings))<=200000,'complete owned WebKit text unavailable/oversize')
    return strings

def native_question(rows):
    require(rows and not any(web for _,_,web in rows),'Stop question is not a native subtree')
    title_present=any(p['AXRole'] in ('AXWindow','AXDialog','AXSheet','AXStaticText')
                      and 'Stop Codex' in (p.get('AXTitle'),p.get('AXValue')) for _,p,_ in rows)
    require(title_present,'actual native Stop title unavailable')
    strings=[]
    for _,p,_ in rows:
        if p['AXRole'] not in TEXT_ROLES:continue
        value=next((p.get(k) for k in ('AXValue','AXTitle','AXDescription') if isinstance(p.get(k),str) and p[k]),None)
        if value and value!='Stop Codex' and (not strings or strings[-1]!=value):strings.append(value)
    require(strings and sum(map(len,strings))<=16384,'actual complete Stop question unavailable')
    buttons=[e for e,p,_ in rows if p['AXRole']=='AXButton' and p.get('AXTitle')=='Stop Codex' and p.get('AXEnabled') is True]
    require(len(buttons)==1,'native enabled Stop confirmation unavailable/ambiguous')
    return '\n'.join(strings),buttons[0]

def make_run(b):
    screen=b.screen_support;w=screen.w
    class AXRun(screen.make_run(b)):
        def __init__(self,*args,**kwargs):
            super().__init__(*args,**kwargs)
            self.ax_binding=None;self.ax_reads=0;self.ax_actions=set();self.ax_failed=False;self.stop_context=None
        def alive(self):
            super().alive()
            require(time.monotonic()<getattr(self,'ui_deadline',self.cleanup_end),'owned AX phase deadline')
        def note_refusal(self,error):
            self.ax_failed=True
            self.safe_log('owned_AX_boundary_refusal',error=str(error),windows=getattr(self.ax,'last_window_observation',None))
        def bound_main(self):
            require(self.ax_binding is not None,'owned AX journey not initialized')
            backend=w.d.NativeBackend()
            try:
                identity=w.d.bound_identity(self,backend);window=w.select_main(backend,identity['pid'])
                require((identity,window)==self.ax_binding,'owned AX main identity/window facts changed')
            finally:backend.close()
            require(self.ax.attr(self.ax.app,'AXFrontmost') is True,'original App no longer frontmost')
            element=self.ax.main()
            require(window_number(self.ax,element)==window['window_id'],'distinct AX main does not match owned WindowServer ID')
            return element
        def main_rows(self):
            try:
                self.ax_reads+=1;require(self.ax_reads<=64,'owned AX read bound exhausted')
                element=self.bound_main();rows=self.ax.walk(element);self.bound_main()
                require(sum(len(v) for _,p,_ in rows for v in p.values() if isinstance(v,str))<=400000,'owned AX text expansion exceeds bound')
                self.record(f'owned-AX-{self.ax_reads:03d}.json',{'at':b.now(),'window_id':self.ax_binding[1]['window_id'],
                    'rows':[dict(p,in_web_area=web) for _,p,web in rows],'walk':self.ax.last_walk_observation,
                    'provenance':'actual owned native AX attributes, not screenshot transcription/internal App commands'})
                require(any(p['AXRole']=='AXWebArea' for _,p,_ in rows),'actual owned WebKit AXWebArea unavailable')
                return rows
            except BaseException as error:self.note_refusal(error);raise
        def open_disclosure(self,title,prefix=False):
            rows=self.main_rows();element=web_control(rows,'AXDisclosureTriangle',title,prefix)
            state=self.ax.attr(element,'AXValue')
            require(state in (True,False,0,1),'owned disclosure state unavailable: '+title)
            if state in (True,1):return
            require(title not in self.ax_actions,'owned disclosure already pressed; no repeat: '+title)
            self.bound_main();self.ax_actions.add(title)
            self.safe_log('owned_AX_disclosure_intent',title=title,actor=b.ACTOR)
            self.ax.press(element)
            self.wait_for(lambda:self.ax.attr(element,'AXValue') in (True,1),3,'owned disclosure effect unavailable: '+title)
            self.bound_main();self.safe_log('owned_AX_disclosure_open',title=title)
        def read_diagnostics(self):
            strings=web_strings(self.main_rows())
            observed=b.decode_diagnostics(strings,protocol=True)
            observed['observation_provenance']={'kind':'owned-native-AX-text','window_id':self.ax_binding[1]['window_id'],'read_sequence':self.ax_reads}
            self.last_diagnostics=observed
            return observed
        def observe_ready(self,qualification=True):
            try:
                if qualification:
                    self.ui_deadline=min(time.monotonic()+15,self.work_end)
                    self.record('owned-AX-contract.json',CONTRACT)
                    route=self.screen.window;route.acquire_initial_window();frame=route.capture()
                    frame=route.input('focus',frame) # Existing isolated AppKit helper; actual AXFrontmost required.
                    require(frame is not None and frame['identity']==route.initial_binding[0]
                            and frame['window']==route.initial_binding[1],'activation changed initial owned window')
                    self.ax_binding=(frame['identity'],frame['window'])
                require(not self.ax_failed and self.ax_binding is not None,'owned AX unavailable; no image-operator fallback')
                self.screen.begin_phase('ready' if qualification else 'cleanup-source')
                self.wait_for(self.distinct_main,5,'distinct owned AX main unavailable after activation')
                self.open_disclosure('Host diagnostics',True)
                self.open_disclosure('Lifecycle events (',True)
                self.open_disclosure('Raw native envelopes (including unknown fields)')
                last=None
                while True:
                    self.alive()
                    try:
                        observed=self.read_diagnostics();gen=b.source_gate(observed,self.value)
                        self.generation=gen
                        if qualification:b.reject_permanent_witness_failure(observed,gen);b.ready_gate(observed,self.value)
                        self.record('ready-observation.json' if qualification else 'cleanup-source-observation.json',observed)
                        self.screen.window.capture() # Corroboration, never a source substitute.
                        return gen
                    except b.PermanentWitnessFailure:raise
                    except (RuntimeError,ValueError) as error:
                        if self.ax_failed:raise
                        last=str(error);self.safe_log('owned_AX_ready_wait',error=last)
                    time.sleep(.25)
            except BaseException as error:self.note_refusal(error);raise
        def diagnostics(self):
            phase='settlement' if self.stop_confirmed or self.screen.active_phase=='settlement' else ('cleanup-source' if self.cleanup else 'recheck')
            self.screen.begin_phase(phase)
            require(not self.ax_failed,'owned AX boundary failed; no alternate observation route')
            return self.read_diagnostics()
        def request_stop_ui(self):
            try:
                self.screen.begin_phase('stop')
                b.source_gate(self.last_diagnostics,self.value,self.generation)
                self.open_disclosure('Connection and access',True)
                rows=self.main_rows()
                current=b.decode_diagnostics(web_strings(rows),protocol=True)
                b.source_gate(current,self.value,self.generation);self.last_diagnostics=current
                button=web_control(rows,'AXButton','Stop Codex…')
                self.bound_main();backend=w.d.NativeBackend()
                try:
                    identity=w.d.bound_identity(self,backend);window=w.select_main(backend,identity['pid'])
                    require((identity,window)==self.ax_binding,'Stop main binding changed')
                    context={'identity':identity,'main':window,'before_inventory':w.owned_inventory(backend,identity['pid']),
                        'generation':self.generation,'source_observation_sha256':hashlib.sha256(json.dumps(self.last_diagnostics,sort_keys=True).encode()).hexdigest(),
                        'at':b.now(),'posted':False}
                finally:backend.close()
                self.record('owned-AX-stop-intent.json',context)
                require(not self.stop_requested,'Stop already requested')
                self.stop_requested=True;self.ax.press(button)
                context['posted']=True;self.stop_context=context
                self.record('owned-AX-stop-posted.json',context)
            except BaseException as error:self.note_refusal(error);raise
        def modal_rows(self):
            require(self.stop_context is not None and self.stop_context['posted'],'no bound Stop modal derivation')
            backend=w.d.NativeBackend()
            try:
                identity=w.d.bound_identity(self,backend)
                require(identity==self.stop_context['identity'],'original App changed before modal')
                modal=w.select_modal(backend,identity['pid'],self.stop_context)
                require(self.ax.attr(self.ax.app,'AXFrontmost') is True,'App lost focus before modal')
                roots=[e for e in self.ax.windows() if window_number(self.ax,e)==modal['window_id']]
                require(len(roots)<=1,'derived native Stop AX window ambiguous; no main substitution')
                if not roots:raise b.ax_support.MainWindowUnavailable('derived native Stop AX window unavailable')
                flag=self.ax.attr(roots[0],'AXModal')
                require(flag is not False,'exposed AX Stop window is not modal')
                parent=self.ax.attr(roots[0],'AXParent');relation='unavailable'
                if parent is not None:
                    self.ax.own(parent)
                    if self.ax.c.CFEqual(parent,self.ax.app):relation='owned-application-parent'
                    else:
                        require(window_number(self.ax,parent)==self.ax_binding[1]['window_id'],'native Stop parent is not original main')
                        relation='original-main-window-parent'
                self.ax_reads+=1;require(self.ax_reads<=64,'owned AX read bound exhausted')
                rows=self.ax.walk(roots[0])
                self.record(f'owned-AX-modal-{self.ax_reads:03d}.json',{'at':b.now(),'modal':modal,'AXModal':flag,'parent_relation':relation,'rows':[dict(p,in_web_area=web) for _,p,web in rows]})
                require(w.d.bound_identity(self,backend)==identity and w.select_modal(backend,identity['pid'],self.stop_context)==modal,'modal changed while reading')
                return rows,modal
            finally:backend.close()
        def confirm_stop_ui(self,gen):
            try:
                self.screen.begin_phase('stop-confirmation')
                require(not self.stop_confirmed and self.stop_context['generation']==gen,'Stop confirmation repeated/source changed')
                def available():
                    try:return self.modal_rows()
                    except (w.WindowUnavailable,b.ax_support.MainWindowUnavailable):return None
                rows,modal=self.wait_for(available,5,'derived native Stop question unavailable')
                statement,button=native_question(rows)
                normalized=screen.validate_stop_question('Stop Codex',statement,gen,self.value['expected_generation_home'])
                self.record('stop-confirmation.json',{'at':b.now(),'generation':gen,'statement':normalized,'modal':modal,
                    'rows':[dict(p,in_web_area=web) for _,p,web in rows],'actor':b.ACTOR,'provenance':'actual owned native AX question'})
                current,current_modal=self.modal_rows();current_statement,current_button=native_question(current)
                require(current_modal==modal and screen.validate_stop_question('Stop Codex',current_statement,gen,self.value['expected_generation_home'])==normalized,
                        'native Stop question changed before confirmation')
                self.stop_confirmed=True;self.ax.press(current_button)
                self.safe_log('owned_AX_stop_confirmed',generation=gen,actor=b.ACTOR)
            except BaseException as error:self.note_refusal(error);raise
        def request_quit_ui(self):
            self.ui_deadline=self.cleanup_end
            require(self.extra_cleanup_ready(),'helper unsettled before Quit')
            self.bound_main()
            self.screen.window.capture() # settled main-window corroboration
            return super().request_quit_ui()
        def held_status(self,error):
            status=super().held_status(error)
            status['owned_AX_journey']={'version':CONTRACT['version'],'boundary_failed':self.ax_failed,
                'reads':self.ax_reads,'stop_requested':self.stop_requested,'stop_confirmed':self.stop_confirmed,
                'stop_posted_observed':bool(self.stop_context and self.stop_context['posted']),
                'limits':'No screenshot-only fallback. If Stop was requested, flags do not prove modal dismissal; inspect actual question/state before any external cleanup action.'}
            return status
        def cleanup_attempt(self):
            if self.ax_failed and not (self.supplier_settled and self.quit_requested):
                raise RuntimeError('owned AX boundary unavailable; retain custody, no screenshot-only fallback')
            return super().cleanup_attempt()
    return AXRun
