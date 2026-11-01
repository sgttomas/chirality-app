"""Native keeper adapters for attended setup/relaunch/Cancel; no CLI launch.

Instantiation requires the separately checked admission, explicit two-phase
roots and the supervising manager's delivery/completion callbacks. No product
control endpoint, credentials, model, signal or automatic extra launch.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import threading
import time

from native_sheet_cancel import for_owned_run
from native_attended_readback import source_after_cancel, CountedAXLibrary
from native_attended_admission import validate_saved_setup


def require(ok, message):
    if not ok:raise RuntimeError(message)


class NativePorts:
    def __init__(self, b, root, value, admissions, deliver, owner_completion, clock=time.monotonic):
        self.b,self.root,self.value,self.admissions=b,Path(root),value,admissions
        self.deliver,self.owner_completion,self.clock=deliver,owner_completion,clock
        self.runs={};self.controls={};self.launches=set();self.pending_launch=None
        self.closures={};self.saved=None;self.last_readback={}

    def record(self, name, value):
        self.b.write_once(self.root/(name+'.json'),value)

    def admit_empty_namespace(self, end):
        # The admission verifier is a fixed callback installed by the prepared
        # entrypoint, not a caller-supplied CLI module or bypass flag.
        return self.admissions.empty(end)

    def launch(self, label, admission, end):
        require(label in ('A','B') and label not in self.launches, 'unknown/repeated incarnation')
        require(label=='A' or ('A' in self.closures and self.saved is not None), 'B before complete A closure')
        self.admissions.before_launch(label,admission,end)
        self.launches.add(label);self.pending_launch=label
        phase=self.root/label
        run_type=self.b.ax_route_support.make_run(self.b)
        run=run_type(phase,dict(self.value),end,admission['admission_sha256'])
        run.work_end=end-135 if label=='A' else end-40
        run.ui_deadline=run.work_end
        def begin_phase(phase):
            if run.screen.active_phase==phase:
                run.screen.phase_alive();return
            caps={'ready':60,'recheck':35,'stop':20,'stop-confirmation':30,'settlement':45,'cleanup-source':35}
            require(phase in caps,'unknown attended phase')
            cutoff=end-135 if phase in ('ready','recheck','cleanup-source') else end-40
            limit=min(self.clock()+caps[phase],cutoff)
            require(limit>self.clock(),'attended phase has no remaining shared budget')
            run.screen.active_phase=phase;run.screen.phase_deadline=limit;run.ui_deadline=limit
        run.screen.begin_phase=begin_phase
        self.runs[label]=run  # register before any launch-side failure
        run.sample(admission=True)
        run.thread=threading.Thread(target=run.monitor,daemon=True);run.thread.start()
        policy=phase/'phase.sb'
        require(policy.read_text()==self.admissions.policy(label,phase),'prepared native policy changed')
        with (phase/'stdout.log').open('wb') as out,(phase/'stderr.log').open('wb') as err:
            child=subprocess.Popen(['/usr/bin/sandbox-exec','-f',str(policy),self.value['executable']],
                cwd=self.value['native_input_paths']['project'],env=self.admissions.environment(label),
                stdin=subprocess.DEVNULL,stdout=out,stderr=err,start_new_session=True)
            run.reservation=self.b.AppReservation(child)  # original Child, never cold PID
        self.pending_launch=None
        run.log('attended_incarnation_started',phase=label,pid=child.pid)
        ax=self.b.ax_route_support.bounded_ax(self.b.ax_support.wrap_ax(self.b.base.load_ax()))
        run.ax=ax(child.pid,run.alive,run.log);run.ax.output=phase
        self.admissions.bind_birth(label,run)
        return label

    def _original(self, label):
        require(label in self.runs,'unknown keeper incarnation')
        run=self.runs[label]
        self.admissions.check_birth(label,run)
        return run

    def ordinary_setup_save(self, label, end):
        require(label=='A','setup may run only in A')
        run=self._original(label);run.ui_deadline=min(end,run.work_end)
        route=run.screen.window
        route.acquire_initial_window();frame=route.capture();frame=run.focus_receipt(frame)
        require(frame is not None,'initial App activation unavailable')
        run.ax_binding=(frame['identity'],frame['window'])
        run.bound_main(press=True)
        # Reuse maintained form/input semantics, but replace its root-based
        # modal lookup and unsupervised screenshot with exact owned bindings.
        run.ax.capture_window=lambda element,name: route.capture(expected_binding=run.ax_binding)
        original_dialog=run.dialog
        def dialog(title,button):
            # A sheet legitimately increases owned window count. Keep original
            # identity/title/bounds/ID while deriving this one setup sheet.
            w=self.b.screen_support.w;backend=w.d.NativeBackend()
            try:
                identity=w.d.bound_identity(run,backend)
                require(identity==run.ax_binding[0],'setup original Child changed')
                inventory=w.owned_inventory(backend,identity['pid'])
                expected=run.ax_binding[1]
                original=[r for r in inventory if r['window_id']==expected['window_id']]
                require(len(original)==1 and all(original[0][k]==expected[k] for k in original[0]),'setup main changed')
                main=run.ax.main()
                require(self.b.ax_route_support.window_number(run.ax,main)==expected['window_id'],'setup AX main differs')
            finally:backend.close()
            children=run.ax.attr(main,'AXChildren')
            require(isinstance(children,list) and len(children)<=8,'setup sheet children unsupported')
            sheets=[e for e in children if run.ax.attr(e,'AXRole')=='AXSheet']
            require(len(sheets)<=1,'ambiguous setup sheet')
            if not sheets:return None
            sheet=sheets[0];parent=run.ax.attr(sheet,'AXParent')
            require(parent is not None and run.ax.c.CFEqual(parent,main),'setup sheet parent differs')
            run.ax.own(sheet)
            number=self.b.ax_route_support.window_number(run.ax,sheet)
            candidates=[r for r in inventory if r['on_screen'] is True and r['window_id']!=expected['window_id']]
            require(len(candidates)==1 and candidates[0]['window_id']==number,'setup sheet has no unique owned row')
            require(run.ax.attr(run.ax.app,'AXFrontmost') is True,'setup App lost focus')
            rows=run.ax.walk(sheet)
            require(not any(web for _,_,web in rows),'setup question must be native')
            require(any(title in (p.get('AXTitle'),p.get('AXValue')) for _,p,_ in rows), 'setup title differs')
            matches=[e for e,p,_ in rows if p['AXRole']=='AXButton' and p.get('AXTitle')==button and p.get('AXEnabled') is True]
            require(len(matches)==1,'setup affirmative unavailable/ambiguous')
            return rows,matches[0]
        run.dialog=dialog
        original_library=run.ax.a
        budget=CountedAXLibrary(original_library,end,cap=12000,clock=self.clock)
        run.ax.a=budget
        # base.form's immutable input recheck is rebound only within this owned
        # serialized manager process, to the same exact admission verifier.
        old_inputs=self.b.base.inputs
        self.b.base.inputs=lambda:self.admissions.recheck_inputs()
        try:self.b.base.form(run,self.value)
        finally:
            self.b.base.inputs=old_inputs;run.ax.a=original_library;run.dialog=original_dialog
        saved=json.loads((run.root/'saved-bindings.json').read_text())
        self.saved={**saved,'incarnation':'A','performed_through_native_ui':True,
                    'applies_next_launch_only':True,'generation':None}
        require(self.clock()<end,'setup exceeded first-stage cutoff')
        return self.saved

    def readmit_saved_state(self, a, saved, closure, end):
        require('A' in self.closures and closure==self.closures['A'],'A closure receipt differs')
        require(saved==self.saved,'saved setup receipt differs')
        return self.admissions.saved_after_closure(a,saved,closure,end)

    def observe_ready(self,label,end):
        require(label=='B','ready only in B')
        run=self._original(label)
        run.work_end=min(end,run.resource_end-40)
        gen=run.observe_ready()
        observed=run.diagnostics()
        require(self.b.ready_gate(observed,run.value)==gen,'B source changed before sheet')
        require(self.clock()<end,'B ready exceeded setup/readiness cutoff')
        return {'incarnation':label,'full_source_gate':True,'ready':True,'zero_observed_work':True,
                'generation':gen,'request_sha256':self.saved['request_sha256'],'account':self.saved['account']}

    def sheet_preflight(self,label,ready,end):
        run=self._original(label);run.ui_deadline=end
        control=for_owned_run(run,run.bound_main(),run.resource_end,self.b.screen_support.w)
        self.controls[label]=control;control.preflight(end)

    def post_stop_once(self,label,ready,end):
        run=self._original(label);run.cleanup=True;run.ui_deadline=end
        require(run.generation==ready['generation'],'Stop source changed')
        run.request_stop_ui()
        require(self.clock()<end,'Stop post exceeded phase cap')

    def discover_cancel(self,label,ready,end):
        run=self._original(label);run.ui_deadline=end
        return self.controls[label].observe(end)

    def observe_question_if_budget(self,label,ready,cancel,end):
        run=self._original(label);run.ui_deadline=end
        identity,main,modal=cancel[0]
        require(identity==run.stop_context['identity'],'question identity differs')
        original_library=run.ax.a;budget=CountedAXLibrary(original_library,end,cap=300,clock=self.clock)
        run.ax.a=budget
        try:
            rows=run.ax.walk(cancel[1])
            statement,_=self.b.ax_route_support.native_question(rows)
            normalized=self.b.screen_support.validate_stop_question('Stop Codex',statement,
                ready['generation'],run.value['expected_generation_home'])
            run.act_record('attended-actual-question.json',{'generation':ready['generation'],
                'statement':normalized,'modal':modal,'AX_calls':budget.calls,
                'provenance':'actual owned sheet AX text; no sheet image captured; no confirmation'})
        finally:run.ax.a=original_library
        require(self.clock()<end,'actual question observation exceeded allowance')

    def cancel_once(self,label,cancel,end):
        run=self._original(label);run.ui_deadline=end
        require(cancel is self.controls[label].selected,'Cancel selection differs')
        return self.controls[label].cancel(end)

    def cancel_dispatch_attempted(self,label):
        return label in self.controls and self.controls[label].attempted

    def owner_cancel_now(self,label,reason,end,attempted):
        run=self.runs.get(label)
        self.deliver({'event':'owner-cancel-needed-now','incarnation':label,'reason':reason,
            'instruction':'If the Stop Codex sheet is still visible, click Cancel, never Stop; report the actual result.',
            'fixed_end':end,'cancel_attempted':attempted,'custody':'retained original Child'})
        if label in self.controls:self.controls[label].fallback_sent=True

    def wait_owner_completion(self,label,end):
        return self.owner_completion(label,end)

    def record_owner_completion(self,label,message):
        self.controls[label].record_owner_completion(message)

    def verify_dismissal_and_source(self,label,ready,end):
        run=self._original(label);run.cleanup=True;run.ui_deadline=end
        control=self.controls[label]
        proof=control.dismissed(end,lambda selected:source_after_cancel(run,run.stop_context,selected,end,
            self.b,self.b.ax_route_support,self.b.screen_support.w,clock=self.clock))
        self.last_readback[label]=proof
        control.ax.close()
        return {'incarnation':label,'same_source':True,'sheet_absent':True,'ready':True}

    def quit_normal(self,label,end):
        run=self._original(label);run.cleanup=True;run.ui_deadline=end
        require(run.extra_cleanup_ready(),'helper custody unknown before Quit')
        if label=='B' and run.stop_requested:require(label in self.last_readback,'Stop sheet not verified dismissed')
        run.bound_main()
        require(not run.quit_requested,'Quit already requested')
        run.quit_requested=True;run.ax.quit_ui()  # never confirm a Quit question
        while self.clock()<end:
            exit_fact=run.reservation.observe()
            if exit_fact is not None:break
            time.sleep(.1)
        else:raise RuntimeError('normal Quit exit unavailable; retain keeper')
        require(self.b.release_support.normal_exit(exit_fact),'App exit was not normal0')
        require(run.extra_cleanup_ready(),'helper custody unknown at exit')
        offered=self.b.release_support.request_for(run)
        require(offered is not None,'fresh admission-bound administrative release unavailable')
        run.act_record('attended-admin-release-intent.json',offered)
        code=run.reservation.administrative_reap(offered['expected_app_exit'])
        require(code==0,'original Child wait not0')
        run.stop.set();run.thread.join(timeout=2)
        require(not run.thread.is_alive(),'guard did not settle')
        receipt={'incarnation':label,'normal_exit':code,'helpers_settled':True,'reaped':True,
                 'released':True,'release_id':label+':'+run.admission_sha,
                 'helper_custody_id':str(run.root),'exit_fact':exit_fact,'supplier_settlement':'not claimed'}
        self.closures[label]=receipt
        return receipt

    def retain_and_report(self,label,end):
        held=[key for key,run in self.runs.items() if run.reservation is not None and not run.reservation.reaped]
        self.deliver({'event':'custody-held','requested_incarnation':label,'pending_launch':self.pending_launch,
                      'retained_incarnations':held,'fixed_end':end,'action':'manager retain supervision; no blind input/reap'})
