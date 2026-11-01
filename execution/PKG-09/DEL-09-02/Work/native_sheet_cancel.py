"""Attended ordinary-sheet observation/Cancel primitive; not wired to a launcher.

The caller retains original Child, admission, source and phase deadlines. This
module never discovers a PID, confirms Stop, launches, or releases custody.
"""
import time


class Refusal(RuntimeError):
    pass


def require(ok, reason):
    if not ok:
        raise Refusal(reason)


class SheetCancel:
    """Adapter contract: every native call has a 0.2s messaging timeout.

    `binding` freshly checks original kernel/executable/main/owned inventory and
    returns (original_identity, main_facts, derived_sheet_facts). `read` returns
    (AXError, decoded_value); it must not erase unsupported/errors into None.
    `same`, `owner`, `number`, `actions` and `press` operate only on passed refs.
    `record` is a mandatory write-once durable evidence operation. `report` must
    immediately deliver fallback instructions to the supervising parent.
    """
    def __init__(self, ax, main, pid, binding, record, report, clock=time.monotonic):
        self.ax, self.main, self.pid = ax, main, pid
        self.binding, self.record, self.report, self.clock = binding, record, report, clock
        self.selected = None
        self.attempted = False
        self.calls = 0
        self.total_calls = 0
        self.prepared = []
        self.observation_failure = None

    def call(self, fn, *args):
        require(self.calls < self.cap, 'sheet native-call cap exhausted')
        require(self.clock() + .2 < self.end, 'sheet time reserve exhausted')
        self.calls += 1
        self.total_calls += 1
        result = fn(*args)
        require(self.clock() < self.end, 'sheet call completed after deadline')
        return result

    def prepare(self, ref):
        if not any(self.ax.same(ref, old) for old in self.prepared):
            require(self.call(self.ax.timeout, ref, .2) == 0, 'sheet AX timeout unavailable')
            require(self.call(self.ax.owner, ref) == self.pid, 'sheet AX owner changed')
            self.prepared.append(ref)

    def read(self, ref, name):
        self.prepare(ref)
        rc, value = self.call(self.ax.read, ref, name)
        require(rc == 0, 'sheet attribute unavailable: ' + name + ' rc=' + str(rc))
        return value

    def preflight(self, end):
        require(self.selected is None and not self.attempted, 'preflight after sheet transaction')
        self.end, self.cap, self.calls, self.prepared = end, 40, 0, []
        children = self.read(self.main, 'AXChildren')
        require(isinstance(children, list) and len(children) <= 8, 'main child list unsupported')
        require(all(self.read(child, 'AXRole') != 'AXSheet' for child in children), 'preexisting sheet')
        self.record('sheet-preflight', {'calls': self.calls, 'sheet_present': False})
        require(self.clock() < end, 'preflight evidence exceeded deadline')

    def observe(self, end, cap=60):
        require(self.selected is None and not self.attempted, "initial discovery cannot repeat")
        self.end, self.cap, self.calls = end, cap, 0
        self.prepared = []
        facts = self.binding()  # caller bounds non-AX identity/inventory cost
        require(self.clock() < end, 'binding exceeded sheet deadline')
        self.prepare(self.main)
        require(self.call(self.ax.number, self.main) == facts[1]['window_id'], 'AX main mapping differs')
        children = self.read(self.main, 'AXChildren')
        require(isinstance(children, list) and len(children) <= 8, 'sheet child list unsupported')
        sheets = []
        for child in children:
            if any(self.ax.same(child, old) for old in sheets):
                continue
            if self.read(child, 'AXRole') == 'AXSheet':
                sheets.append(child)
        require(len(sheets) == 1, 'unique original-main sheet unavailable')
        sheet = sheets[0]
        parent = self.read(sheet, 'AXParent')
        require(self.ax.same(parent, self.main), 'sheet parent is not original main')
        require(self.call(self.ax.number, sheet) == facts[2]['window_id'], 'sheet window mapping differs')
        require(facts[2]['window_id'] != facts[1]['window_id'], 'sheet has no distinct owned row')
        require(self.read(self.ax.app, 'AXFrontmost') is True, 'App is not frontmost')
        require(self.read(self.main, 'AXMain') is True, 'original window is not main')
        focused = self.read(self.ax.app, 'AXFocusedWindow')
        require(self.ax.same(focused, sheet), 'sheet is not focused')
        require(self.read(sheet, 'AXModal') is True, 'sheet modality unavailable')
        # Deliberately bounded direct native controls. A different native layout
        # is reported, not searched with a broader traversal or guessed target.
        controls = self.read(sheet, 'AXChildren')
        require(isinstance(controls, list) and len(controls) <= 6, 'sheet control layout unsupported')
        cancel = []
        for control in controls:
            if self.read(control, 'AXRole') != 'AXButton':
                continue
            if self.read(control, 'AXTitle') == 'Cancel':
                require(self.read(control, 'AXEnabled') is True, 'Cancel disabled or unknown')
                cancel.append(control)
        require(len(cancel) == 1, 'unique enabled Cancel unavailable')
        require(self.ax.same(self.read(cancel[0], 'AXParent'), sheet), 'Cancel parent differs')
        require('AXPress' in self.call(self.ax.actions, cancel[0]), 'Cancel has no AXPress')
        selected = (facts, sheet, cancel[0])
        if self.selected is not None:
            old = self.selected
            require(facts == old[0] and self.ax.same(sheet, old[1]) and self.ax.same(cancel[0], old[2]),
                    'sheet/Cancel changed; no replacement')
        self.record('sheet-cancel-observation', {'binding': facts, 'calls': self.calls})
        require(self.clock() < end, 'sheet evidence exceeded deadline')
        self.selected = selected
        return selected

    def cancel(self, end):
        require(not self.attempted, 'Cancel already attempted; no repeat')
        require(self.selected is not None, 'Cancel has no original observation')
        self.end, self.cap, self.calls = end, 42, 0
        self.prepared = []
        selected = self.selected
        facts, sheet, button = selected
        require(self.binding() == facts, 'original identity/window binding changed')
        require(self.clock() < end, 'binding exceeded Cancel deadline')
        require(self.ax.same(self.read(sheet, 'AXParent'), self.main), 'sheet parent changed')
        require(self.call(self.ax.number, sheet) == facts[2]['window_id'], 'sheet row changed')
        require(self.read(sheet, 'AXRole') == 'AXSheet' and self.read(sheet, 'AXModal') is True,
                'sheet role/modality changed')
        controls = self.read(sheet, 'AXChildren')
        require(isinstance(controls, list) and len(controls) <= 6, 'sheet controls changed')
        require(sum(self.ax.same(e, button) for e in controls) == 1, 'original Cancel absent/duplicated')
        matches=[]
        for e in controls:
            if self.read(e, 'AXRole') == 'AXButton' and self.read(e, 'AXTitle') == 'Cancel':
                matches.append(e)
        require(len(matches)==1 and self.ax.same(matches[0],button), 'Cancel is no longer unique')
        require(self.read(button, 'AXRole') == 'AXButton' and self.read(button, 'AXTitle') == 'Cancel'
                and self.read(button, 'AXEnabled') is True, 'original Cancel changed')
        require(self.ax.same(self.read(button, 'AXParent'), sheet), 'Cancel parent changed')
        require(self.read(self.ax.app, 'AXFrontmost') is True, 'App lost focus')
        require(self.ax.same(self.read(self.ax.app, 'AXFocusedWindow'), sheet), 'sheet lost focus')
        require('AXPress' in self.call(self.ax.actions, button), 'Cancel action unavailable')
        self.record('sheet-cancel-intent', {'binding': selected[0], 'action': 'Cancel',
                                          'actor': 'agent', 'qualification': False})
        require(self.clock() + .2 < end, 'Cancel dispatch reserve unavailable')
        self.attempted = True  # consumed before native dispatch, including errors
        rc = self.call(self.ax.press, selected[2])
        self.record('sheet-cancel-posted', {'return_code': rc, 'effect_verified': False})
        require(rc == 0, 'Cancel delivery uncertain; do not repeat')
        return rc

    def dismissed(self, end, readback):
        require(self.selected is not None, 'no bound sheet to observe dismissal')
        self.end, self.cap, self.calls, self.prepared = end, 40, 0, []
        children = self.read(self.main, 'AXChildren')
        require(isinstance(children, list) and len(children) <= 8, 'dismissal children unsupported')
        require(not any(self.ax.same(e, self.selected[1]) for e in children), 'sheet still attached')
        require(all(self.read(e, 'AXRole') != 'AXSheet' for e in children), 'another sheet present')
        require(self.read(self.main, 'AXMain') is True, 'original main changed')
        require(self.read(self.ax.app, 'AXFrontmost') is True, 'App focus not restored')
        require(self.ax.same(self.read(self.ax.app, 'AXFocusedWindow'), self.main), 'main focus not restored')
        # Caller freshly verifies kernel/executable/main, absence of the exact
        # sheet WS row, full source/generation ready and restored enabled Stop.
        observation = readback(self.selected[0])
        require(self.clock() < end, 'dismissal/source readback exceeded deadline')
        self.record('sheet-dismissed', {'readback': observation, 'cancel_attempted': self.attempted,
                                       'actor': 'agent' if self.attempted else 'owner-reported-and-verified',
                                       'stop_confirmed': False, 'LT23_observed': False})
        require(self.clock() < end, 'dismissal evidence exceeded deadline')
        return observation

    def note_observation_failure(self, reason):
        # Screenshot/question failure is not missing ownership/Cancel evidence.
        self.observation_failure = str(reason)
        self.record('sheet-witness-failed', {'reason': str(reason), 'cancel_bound': self.selected is not None})

    def unsupported(self, reason, fixed_end):
        self.report({'event': 'owner-cancel-needed-now', 'reason': str(reason),
                     'instruction': 'Please click Cancel on the ordinary Stop Codex sheet now; do not click Stop.',
                     'fixed_end': fixed_end, 'cancel_attempted': self.attempted,
                     'custody': 'original keeper retained; no release or success inferred'})


class NativeAdapter:
    """Explicit adapter over the existing retained AX object; no native loading.

    The caller owns/closes that AX object's CF references. Calls are individually
    counted by SheetCancel; no hidden traversal or fallible attribute fallback.
    """
    def __init__(self, ax):
        import ctypes as C
        self.C, self.raw, self.app = C, ax, ax.app
        self.a, self.c = ax.a, ax.c
        self.held = []
        self.c.CFRelease.restype = None
        self.c.CFRelease.argtypes = [C.c_void_p]
        for name, result, args in [
            ('AXUIElementCopyActionNames', C.c_int, [C.c_void_p, C.POINTER(C.c_void_p)]),
            ('AXUIElementPerformAction', C.c_int, [C.c_void_p, C.c_void_p]),
            ('_AXUIElementGetWindow', C.c_int, [C.c_void_p, C.POINTER(C.c_uint32)]),
        ]:
            fn = getattr(self.a, name); fn.restype = result; fn.argtypes = args

    def same(self, a, b):
        return bool(a and b and self.c.CFEqual(a, b))

    def timeout(self, e, seconds):
        return self.a.AXUIElementSetMessagingTimeout(e, seconds)

    def owner(self, e):
        pid = self.C.c_int()
        rc = self.a.AXUIElementGetPid(e, self.C.byref(pid))
        require(rc == 0, 'AX owner unavailable rc=' + str(rc))
        return pid.value

    def read(self, e, name):
        value = self.C.c_void_p()
        key = self.raw.string(name)
        try:
            rc = self.a.AXUIElementCopyAttributeValue(e, key, self.C.byref(value))
        finally:
            self.c.CFRelease(key)
        if value.value:
            self.held.append(value.value)  # retain parent arrays for borrowed AX refs
        return rc, self.raw.value(value.value) if rc == 0 else None

    def number(self, e):
        number = self.C.c_uint32()
        rc = self.a._AXUIElementGetWindow(e, self.C.byref(number))
        require(rc == 0 and number.value > 0, 'sheet window number unavailable')
        return number.value

    def actions(self, e):
        value = self.C.c_void_p()
        rc = self.a.AXUIElementCopyActionNames(e, self.C.byref(value))
        require(rc == 0, 'Cancel action names unavailable')
        if value.value:
            self.held.append(value.value)
        refs = self.raw.value(value.value)
        require(isinstance(refs, list) and len(refs) <= 8, 'Cancel action array unsupported')
        result = [self.raw.value(ref) for ref in refs]
        require(all(isinstance(s, str) for s in result),
                'Cancel action list unsupported')
        return result

    def press(self, e):
        action = self.raw.string('AXPress')
        try:
            return self.a.AXUIElementPerformAction(e, action)
        finally:
            self.c.CFRelease(action)

    def close(self):
        # Only after the keeper has finished action/readback; selected references
        # become invalid after this explicit custody end.
        while self.held:
            self.c.CFRelease(self.held.pop())


def for_owned_run(run, main, fixed_end, window_module):
    """Bind to the keeper's posted Stop context, never caller PID/window IDs.

    This does not alter the existing B execute route. An attended-only runner
    must select it explicitly and must never call confirm_stop_ui afterwards.
    """
    w = window_module
    context = run.stop_context
    require(context and context.get('posted') is True and run.stop_requested
            and not run.stop_confirmed, 'no original unconfirmed Stop transaction')
    require(context['generation'] == run.generation, 'Stop generation changed')
    def binding():
        run.alive()
        require(run.extra_cleanup_ready(), 'helper custody unsettled')
        backend = w.d.NativeBackend()
        try:
            identity = w.d.bound_identity(run, backend)
            require(identity == context['identity'], 'original Child identity changed')
            modal = w.select_modal(backend, identity['pid'], context)
            original = next((r for r in w.owned_inventory(backend, identity['pid'])
                             if r['window_id'] == context['main']['window_id']), None)
            require(original is not None, 'original main unavailable')
            require(all(original[k] == context['main'][k] for k in original), 'original main facts changed')
            require(w.d.bound_identity(run, backend) == identity, 'Child changed during modal inventory')
            return identity, original, modal
        finally:
            backend.close()
    def record(name, value):
        run.act_record(name + '.json', value)
    def report(value):
        run.record('owner-cancel-needed.json', value)
        run.report(value)  # manager must forward immediately on this supervised session
    adapter = NativeAdapter(run.ax)
    return SheetCancel(adapter, main, context['identity']['pid'], binding, record, report)
