"""Counted, read-only dismissal/source verification for the attended Cancel scope.

No launch, action, activation, alternate observation path or public endpoint.
"""
import time


def require(ok, message):
    if not ok:raise RuntimeError(message)


class CountedFunction:
    def __init__(self, owner, fn, name):
        object.__setattr__(self, 'owner', owner);object.__setattr__(self, 'fn', fn);object.__setattr__(self,'name',name)
    def __setattr__(self, name, value):setattr(self.fn, name, value)
    def __getattr__(self, name):return getattr(self.fn, name)
    def __call__(self, *args):
        budget=self.owner
        require(budget.calls < budget.cap and budget.clock()+.2 < budget.end,
                'attended AX readback budget exhausted')
        if self.name == "CGEventPostToPid":
            require(args and args[0] == budget.setup_pid, "keyboard target differs from original Child")
        budget.calls+=1
        result=self.fn(*args)
        require(budget.clock() < budget.end, 'attended AX readback returned late')
        return result


class CountedAXLibrary:
    """Instance-only wrapper counts even ownership/timeout calls in old helpers.

    CF conversions are local and consume the same cumulative deadline. The
    count bound is a maximum, not a worst-case timing-fit claim: 0.2s timeouts
    may exhaust the deadline long before the allowed node/call bound.
    """
    def __init__(self, library, end, cap=20000, clock=time.monotonic, setup_pid=None):
        self.library,self.end,self.cap,self.clock=library,end,cap,clock
        self.calls=0;self.functions={};self.setup_pid=setup_pid
    def __getattr__(self, name):
        setup_names={'CGEventCreateKeyboardEvent','CGEventSetFlags','CGEventKeyboardSetUnicodeString','CGEventPostToPid'}
        require(name.startswith(('AX','_AX')) or (self.setup_pid is not None and name in setup_names),
                'non-AX operation not allowed outside exact setup keyboard path')
        if name not in self.functions:self.functions[name]=CountedFunction(self,getattr(self.library,name),name)
        return self.functions[name]


def source_after_cancel(run, context, selected, end, b, route, w, clock=time.monotonic):
    """Use only original keeper/context and actual main AX/protocol text.

    `selected` is the retained identity/main/sheet tuple or None after actual
    owner fallback. No known-state booleans are supplied by an operator.
    """
    require(context.get('posted') is True and run.stop_requested and not run.stop_confirmed,
            'not an unconfirmed source-bound Stop context')
    require(run.generation==context['generation'], 'original Stop generation changed')
    backend=w.d.NativeBackend()
    try:
        identity=w.d.bound_identity(run,backend)
        require(identity==context['identity'],'original Child changed')
        inventory=w.owned_inventory(backend,identity['pid'])
        before={r['window_id'] for r in context['before_inventory'] if r['on_screen'] is True}
        visible={r['window_id'] for r in inventory if r['on_screen'] is True}
        require(not visible-before,'new owned window remains after reported cancellation')
        if selected is not None:require(selected[2]['window_id'] not in visible,'selected sheet still visible')
        main=w.select_main(backend,identity['pid'])
        require((identity,main)==run.ax_binding,'original main changed after cancellation')
        require(clock()<end,'dismissal identity/inventory exceeded deadline')
        original_library=run.ax.a
        budget=CountedAXLibrary(original_library,end,clock=clock)
        run.ax.a=budget
        try:
            rows=run.main_rows()
            observed=b.decode_diagnostics(route.web_strings(rows),protocol=True)
            generation=b.source_gate(observed,run.value,context['generation'])
            b.ready_gate(observed,run.value)
            route.web_control(rows,'AXButton','Stop Codex…')
        finally:
            run.ax.a=original_library
        require(clock()<end,'source decode exceeded deadline')
        relevant=[row for row in observed['lifecycle'] if row.get('generation')==generation]
        stopping=[row for row in relevant if row.get('toState')=='stopping']
        terminal=[row for row in relevant if row.get('transitionId')=='LT-23']
        require(not stopping and not terminal,'Stop effects observed; Cancel witness refused')
        require(w.d.bound_identity(run,backend)==identity,'Child changed during source readback')
        require(w.owned_inventory(backend,identity['pid'])==inventory,'owned inventory changed during source readback')
        require(clock()<end,'readback final validation exceeded deadline')
        proof={'generation':generation,'state':observed['rendered_state'],'stop_enabled':True,
               'sheet_row_absent':True,'no_new_owned_windows':True,'source_gate_passed':True,
               'stopping_rows':stopping,'LT23_rows':terminal,'AX_calls':budget.calls,
               'identity':identity,'main':main,'raw_observation':observed}
        run.act_record('attended-cancel-source-readback.json',proof)
        require(clock()<end,'readback evidence exceeded deadline')
        return proof
    finally:
        backend.close()
