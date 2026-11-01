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
    def __init__(self, ax, main, pid, binding, record, report, clock=time.monotonic, generation=None, main_binding=None):
        self.ax, self.main, self.pid = ax, main, pid
        self.binding, self.record, self.report, self.clock = binding, record, report, clock
        self.generation, self.main_binding = generation, main_binding
        self.discovery_started = False
        self.preflight_started = False
        self.cancel_started = False
        self.dismissal_started = False
        self.posted_rc = None
        self.fallback_sent = False
        self.owner_completion = None
        self.selected = None
        self.attempted = False
        self.calls = 0
        self.total_calls = 0
        self.prepared = []
        self.observation_failure = None

    def call(self, fn, *args):
        require(self.calls < self.cap and self.total_calls < 190, 'sheet native-call cap exhausted')
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
        require(not self.preflight_started and not self.discovery_started, 'preflight cannot repeat')
        self.preflight_started = True
        require(self.main_binding is not None, 'preflight needs original keeper main binding')
        self.end, self.cap, self.calls, self.prepared = end, 40, 0, []
        expected = self.main_binding()
        self.prepare(self.main)
        require(self.call(self.ax.number, self.main) == expected['window_id'], 'preflight main differs')
        children = self.read(self.main, 'AXChildren')
        require(isinstance(children, list) and len(children) <= 5, 'main child list unsupported')
        require(all(self.read(child, 'AXRole') != 'AXSheet' for child in children), 'preexisting sheet')
        self.record('sheet-preflight', {'calls': self.calls, 'sheet_present': False})
        require(self.clock() < end, 'preflight evidence exceeded deadline')

    def observe(self, end, cap=60):
        require(not self.discovery_started, "initial discovery cannot repeat")
        self.discovery_started = True
        self.end, self.cap, self.calls = end, cap, 0
        self.prepared = []
        facts = self.binding()  # caller bounds non-AX identity/inventory cost
        require(self.clock() < end, 'binding exceeded sheet deadline')
        self.prepare(self.main)
        require(self.call(self.ax.number, self.main) == facts[1]['window_id'], 'AX main mapping differs')
        children = self.read(self.main, 'AXChildren')
        require(isinstance(children, list) and len(children) <= 5, 'sheet child list unsupported')
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
        titles = []
        for control in controls:
            if self.read(control, 'AXRole') != 'AXButton':
                continue
            title = self.read(control, 'AXTitle')
            titles.append(title)
            if title == 'Cancel':
                require(self.read(control, 'AXEnabled') is True, 'Cancel disabled or unknown')
                cancel.append(control)
        require(sorted(titles) == ['Cancel','Keep Codex running','Stop Codex'], 'not the exact Stop question button set')
        require(len(cancel) == 1, 'unique enabled Cancel unavailable')
        require(self.ax.same(self.read(cancel[0], 'AXParent'), sheet), 'Cancel parent differs')
        require('AXPress' in self.call(self.ax.actions, cancel[0]), 'Cancel has no AXPress')
        selected = (facts, sheet, cancel[0])
        self.record('sheet-cancel-observation', {'binding': facts, 'calls': self.calls, 'buttons': titles})
        require(self.clock() < end, 'sheet evidence exceeded deadline')
        self.selected = selected
        return selected

    def cancel(self, end):
        require(not self.cancel_started, 'Cancel phase already used; no repeat')
        self.cancel_started = True
        require(self.selected is not None, 'Cancel has no original observation')
        self.end, self.cap, self.calls = end, 46, 0
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
        titles=[]
        for e in controls:
            if self.read(e, 'AXRole') == 'AXButton':
                title=self.read(e, 'AXTitle');titles.append(title)
                if title == 'Cancel':matches.append(e)
        require(sorted(titles) == ['Cancel','Keep Codex running','Stop Codex'], 'Stop question buttons changed')
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
        require(self.calls < self.cap and self.total_calls < 190, 'Cancel call cap exhausted')
        started = self.clock()
        require(started + .2 < end, 'Cancel dispatch reserve exhausted before native call')
        self.calls += 1; self.total_calls += 1
        self.attempted = True
        rc = None; error = None
        try:
            rc = self.ax.press(button)
            self.posted_rc = rc
        except BaseException as exc:
            error = repr(exc)
            raise
        finally:
            self.record('sheet-cancel-posted', {'return_code': rc, 'error': error,
                'started': started, 'finished': self.clock(), 'late': self.clock() >= end,
                'effect_verified': False})
        require(self.clock() < end, 'Cancel returned after deadline; do not repeat')
        require(rc == 0, 'Cancel delivery uncertain; do not repeat')
        return rc

    def dismissed(self, end, readback):
        require(not self.dismissal_started, 'dismissal phase already used')
        self.dismissal_started = True
        require(self.selected is not None or self.owner_completion == 'Cancelled',
                'unbound dismissal needs actual owner Cancel completion')
        self.end, self.cap, self.calls, self.prepared = end, 40, 0, []
        children = self.read(self.main, 'AXChildren')
        require(isinstance(children, list) and len(children) <= 8, 'dismissal children unsupported')
        if self.selected is not None:
            require(not any(self.ax.same(e, self.selected[1]) for e in children), 'sheet still attached')
        require(all(self.read(e, 'AXRole') != 'AXSheet' for e in children), 'another sheet present')
        require(self.read(self.main, 'AXMain') is True, 'original main changed')
        require(self.read(self.ax.app, 'AXFrontmost') is True, 'App focus not restored')
        require(self.ax.same(self.read(self.ax.app, 'AXFocusedWindow'), self.main), 'main focus not restored')
        # Caller freshly verifies kernel/executable/main, absence of the exact
        # sheet WS row, full source/generation ready and restored enabled Stop.
        observation = readback(self.selected[0] if self.selected else None)
        if self.selected is None:
            require(observation.get('no_new_owned_windows') is True, 'unbound owner dismissal inventory unavailable')
        require(self.clock() < end, 'dismissal/source readback exceeded deadline')
        self.validate_readback(observation)
        actor = ('owner-reported-and-verified' if self.owner_completion == 'Cancelled' else
                 'agent' if self.posted_rc == 0 and not self.fallback_sent else 'undetermined')
        self.record('sheet-dismissed', {'readback': observation, 'cancel_attempted': self.attempted,
                                      'actor': actor, 'Stop_action_authorized_by_controller': False})
        require(self.clock() < end, 'dismissal evidence exceeded deadline')
        return observation

    def validate_readback(self, observation):
        require(isinstance(observation, dict) and self.generation is not None
                and observation.get('generation') == self.generation
                and observation.get('state') == 'ready'
                and observation.get('stop_enabled') is True
                and observation.get('sheet_row_absent') is True
                and observation.get('source_gate_passed') is True
                and observation.get('stopping_rows') == []
                and observation.get('LT23_rows') == [], 'dismissal source/effect proof unavailable')

    def record_owner_completion(self, actual_message):
        require(actual_message == 'Cancelled', 'actual owner completion required')
        self.owner_completion = actual_message

    def note_observation_failure(self, reason):
        # Screenshot/question failure is not missing ownership/Cancel evidence.
        self.observation_failure = str(reason)
        self.record('sheet-witness-failed', {'reason': str(reason), 'cancel_bound': self.selected is not None})

    def unsupported(self, reason, fixed_end):
        self.fallback_sent = True
        self.report({'event': 'owner-cancel-needed-now', 'reason': str(reason),
                     'instruction': 'If the ordinary Stop Codex sheet is still visible, please click Cancel now; do not click Stop. Report what you actually observe.',
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
    require(run.ax_binding is not None and run.generation is not None and not run.stop_confirmed,
            'original ready binding unavailable')
    original_binding = run.ax_binding
    generation = run.generation
    def main_binding():
        run.alive()
        backend = w.d.NativeBackend()
        try:
            identity = w.d.bound_identity(run, backend)
            main_facts = w.select_main(backend, identity['pid'])
            require((identity, main_facts) == original_binding, 'preflight original main changed')
            return main_facts
        finally:
            backend.close()
    def binding():
        context = run.stop_context
        require(context and context.get('posted') is True and run.stop_requested
                and not run.stop_confirmed and context['generation'] == generation == run.generation,
                'no original unconfirmed Stop transaction')
        require(context['identity'] == original_binding[0] and context['main'] == original_binding[1],
                'Stop context differs from original ready main')
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
    reports = [0]
    def report(value):
        value['fixed_end'] = fixed_end
        run.report(value)  # delivery must not depend on evidence disk writes
        reports[0] += 1
        try:run.record('owner-cancel-needed-%03d.json' % reports[0], value)
        except Exception as error:run.safe_log('fallback_record_failed', error=str(error))
    adapter = NativeAdapter(run.ax)
    return SheetCancel(adapter, main, original_binding[0]['pid'], binding, record, report,
                       generation=generation, main_binding=main_binding)
