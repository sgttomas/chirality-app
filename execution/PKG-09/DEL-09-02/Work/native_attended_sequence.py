"""Once-only two-incarnation attended sequence; no implicit native implementation.

Ports are private keeper operations, not an IPC/control endpoint. Their native
implementation must enforce the same exact identity/source/evidence contracts.
This module neither loads AppKit nor launches via an arbitrary command.
"""
import time


class Refusal(RuntimeError):
    pass


def require(ok, why):
    if not ok:
        raise Refusal(why)


def closed(receipt, incarnation):
    require(isinstance(receipt, dict) and receipt.get('incarnation') == incarnation,
            'closure belongs to another incarnation')
    require(receipt.get('normal_exit') == 0 and receipt.get('helpers_settled') is True
            and receipt.get('reaped') is True and receipt.get('released') is True,
            'original Child/helper custody not fully closed')
    require(isinstance(receipt.get('release_id'), str) and receipt['release_id'], 'release identity missing')
    return receipt


class AttendedSequence:
    def __init__(self, ports, clock=time.monotonic):
        self.p, self.clock = ports, clock
        self.started = False
        self.current = None
        self.deadline = None
        self.stop_posted = False
        self.cancel_attempted = False
        self.incarnations = []
        self.quit_attempted = set()
        self.identity_unsupported = False
        self.result = {'scope': 'attended ordinary setup/relaunch/Stop-Cancel only',
                       'Stop_confirmed': False, 'LT23_observed': False, 'qualification_success': False}

    def before(self, reserve, why):
        require(self.clock() + reserve < self.deadline, why)

    def closure(self, receipt):
        checked = closed(receipt, self.current)
        self.p.record('closure-' + self.current, checked)
        self.current = None
        return checked

    def quit_current(self):
        require(self.current not in self.quit_attempted, 'Quit already attempted; retain custody')
        self.quit_attempted.add(self.current)
        return self.p.quit_normal(self.current, self.deadline)

    def run(self, slot_acquired):
        require(not self.started, 'sequence already used; no rearm')
        self.started = True
        require(type(slot_acquired) in (float, int) and slot_acquired <= self.clock(), 'invalid acquisition time')
        self.deadline = slot_acquired + 295
        try:
            self.before(135, 'not enough setup/readiness budget')
            admission_a = self.p.admit_empty_namespace(self.deadline)
            self.before(135, 'empty namespace admission exceeded budget')
            self.current = self.p.launch('A', admission_a, self.deadline)
            self.incarnations.append(self.current)
            saved = self.p.ordinary_setup_save(self.current, self.deadline - 135)
            require(saved.get('performed_through_native_ui') is True
                    and saved.get('applies_next_launch_only') is True
                    and saved.get('incarnation') == self.current, 'setup not actually saved by original A')
            a = self.closure(self.quit_current())
            self.before(135, 'A closure missed setup/readiness cutoff; no B')
            admission_b = self.p.readmit_saved_state(admission_a, saved, a, self.deadline - 135)
            require(admission_b.get('fresh_after_closure') is True
                    and admission_b.get('a_release_id') == a['release_id']
                    and admission_b.get('admission_id') != admission_a.get('admission_id'),
                    'fresh B admission unavailable')
            self.before(135, 'readmission missed cutoff; no B')
            b = self.p.launch('B', admission_b, self.deadline)
            # Native launch ports must register keeper custody before returning.
            self.current = b
            self.identity_unsupported = b in self.incarnations
            require(not self.identity_unsupported, 'B reused A incarnation identity')
            self.incarnations.append(b)
            ready = self.p.observe_ready(b, self.deadline - 135)
            require(ready.get('incarnation') == b and ready.get('full_source_gate') is True
                    and ready.get('ready') is True and ready.get('zero_observed_work') is True
                    and ready.get('generation') != saved.get('generation'), 'actual B ready/source unavailable')
            self.result['generation'] = ready['generation']
            self.before(135, '160s setup/readiness cutoff; no Stop')
            self.p.sheet_preflight(b, ready, min(self.clock() + 5, self.deadline - 135))
            self.before(135, 'preflight missed cutoff; no Stop')
            # Intent consumed before dispatch, even if delivery is uncertain.
            self.stop_posted = True
            self.p.post_stop_once(b, ready, min(self.clock() + 20, self.deadline - 115))
            modal_end = min(self.clock() + 30, self.deadline - 85)
            try:
                cancel = self.p.discover_cancel(b, ready, min(self.clock() + 15, modal_end - 15))
                # Question/capture witness failures cannot invalidate separate
                # valid Cancel proof; ports retain them as failed evidence.
                try:
                    self.p.observe_question_if_budget(b, ready, cancel, modal_end - 10)
                except Exception as observation_error:
                    self.result['observation_failure'] = str(observation_error)
                    self.p.record('question-observation-failed', {'reason': str(observation_error), 'cancel_bound': True})
                self.cancel_attempted = True
                self.p.cancel_once(b, cancel, min(self.clock() + 10, modal_end))
            except Exception as error:
                self.result['automated_cancel_failure'] = str(error)
                self.p.owner_cancel_now(b, str(error), self.deadline, self.cancel_attempted)
                # Do not repeat agent Cancel. Owner fallback was explicitly
                # selected; report immediately, not at the fixed deadline.
            dismissal = self.p.verify_dismissal_and_source(b, ready, self.deadline - 40)
            require(dismissal.get('same_source') is True and dismissal.get('sheet_absent') is True
                    and dismissal.get('ready') is True and dismissal.get('incarnation') == b,
                    'actual dismissal/source unavailable; no Quit')
            self.before(40, 'dismissal exceeded Quit-entry reserve')
            b_closed = self.closure(self.quit_current())
            require(b_closed['release_id'] != a['release_id'], 'B reused A release token')
            require(b_closed.get('helper_custody_id') and b_closed.get('helper_custody_id') != a.get('helper_custody_id'),
                    'B helper custody identity unavailable/reused')
            self.result['witness_complete'] = not any(k in self.result for k in ('observation_failure','automated_cancel_failure'))
        except Exception as error:
            self.result.update(witness_complete=False, error=str(error))
            if self.current is not None:
                if self.stop_posted or self.identity_unsupported:
                    self.p.owner_cancel_now(self.current, str(error), self.deadline, self.cancel_attempted)
                    self.p.retain_and_report(self.current, self.deadline)
                else:
                    # No sheet was requested; known-safe ordinary Quit only.
                    try:
                        self.closure(self.quit_current())
                    except Exception as cleanup_error:
                        self.result['cleanup_error'] = str(cleanup_error)
                        self.p.retain_and_report(self.current, self.deadline)
        self.result.update(incarnations=list(self.incarnations), custody_held=self.current is not None,
                           elapsed=self.clock() - slot_acquired, overrun=max(0, self.clock() - self.deadline))
        self.p.record('attended-result', self.result)
        return dict(self.result)
