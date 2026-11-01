"""Once-only two-incarnation attended sequence; no implicit native implementation.

Ports are private keeper operations, not an IPC/control endpoint. Their native
implementation must enforce the same exact identity/source/evidence contracts.
This module neither loads AppKit nor launches via an arbitrary command.
"""
import time
import re


class Refusal(RuntimeError):
    pass


def require(ok, why):
    if not ok:
        raise Refusal(why)


def closed(receipt, incarnation, prior=()):
    require(isinstance(receipt, dict) and receipt.get('incarnation') == incarnation,
            'closure belongs to another incarnation')
    require(receipt.get('normal_exit') == 0 and receipt.get('helpers_settled') is True
            and receipt.get('reaped') is True and receipt.get('released') is True,
            'original Child/helper custody not fully closed')
    require(isinstance(receipt.get('release_id'), str) and receipt['release_id'], 'release identity missing')
    require(isinstance(receipt.get('helper_custody_id'), str) and receipt['helper_custody_id'],
            'helper custody identity missing')
    require(all(receipt['release_id'] != old['release_id'] and
                receipt['helper_custody_id'] != old['helper_custody_id'] for old in prior),
            'release/helper custody identity reused')
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
        self.custody_unknown = False
        self.sheet_pending = False
        self.fallback_attempted = False
        self.closures = []
        self.delivery_errors = []
        self.result = {'scope': 'attended ordinary setup/relaunch/Stop-Cancel only',
                       'Stop_confirmed': False, 'LT23_observed': False, 'qualification_success': False}

    def before(self, reserve, why):
        require(self.clock() + reserve < self.deadline, why)

    def closure(self, receipt):
        checked = closed(receipt, self.current, self.closures)
        self.p.record('closure-' + self.current, checked)
        self.current = None
        self.closures.append(checked)
        return checked

    def quit_current(self):
        require(self.current not in self.quit_attempted, 'Quit already attempted; retain custody')
        self.quit_attempted.add(self.current)
        return self.p.quit_normal(self.current, self.deadline)

    def safe_record(self, name, value):
        try:self.p.record(name, value)
        except BaseException as error:self.delivery_errors.append('record '+name+': '+repr(error))

    def retain(self, reason):
        try:self.p.retain_and_report(self.current, self.deadline, failure={
            'original_error':self.result.get('error'),'cleanup_error':self.result.get('cleanup_error'),
            'custody_reason':str(reason)})
        except BaseException as error:self.delivery_errors.append('retain/report: '+repr(error))
        self.safe_record('custody-retained', {'incarnation':self.current,'unknown':self.custody_unknown,
                                            'reason':str(reason)})

    def fallback(self, reason):
        if not self.sheet_pending or self.fallback_attempted:return False
        self.fallback_attempted = True
        try:
            self.p.owner_cancel_now(self.current, str(reason), self.deadline, self.cancel_attempted)
            return True
        except BaseException as error:
            self.delivery_errors.append('owner delivery: '+repr(error))
            self.retain(error)
            return False

    def launch(self, label, admission):
        # Unknown custody begins before calling a port that may spawn then fail.
        self.custody_unknown = True
        try:incarnation = self.p.launch(label, admission, self.deadline)
        except BaseException as error:
            self.result.setdefault('error',str(error))
            self.retain('launch '+label+' failed; original Child custody unknown')
            raise
        self.current = incarnation
        self.identity_unsupported = not isinstance(incarnation,str) or not incarnation or incarnation in self.incarnations
        require(not self.identity_unsupported,'launch incarnation unavailable or reused')
        self.custody_unknown = False
        self.incarnations.append(incarnation)
        return incarnation

    def run(self, slot_acquired):
        require(not self.started, 'sequence already used; no rearm')
        self.started = True
        require(type(slot_acquired) in (float, int) and slot_acquired <= self.clock(), 'invalid acquisition time')
        self.deadline = slot_acquired + 295
        try:
            self.before(135, 'not enough setup/readiness budget')
            admission_a = self.p.admit_empty_namespace(self.deadline)
            self.before(135, 'empty namespace admission exceeded budget')
            self.launch('A', admission_a)
            saved = self.p.ordinary_setup_save(self.current, self.deadline - 135)
            require(saved.get('performed_through_native_ui') is True
                    and saved.get('applies_next_launch_only') is True
                    and saved.get('incarnation') == self.current
                    and re.fullmatch('[0-9a-f]{64}',saved.get('request_sha256',''))
                    and isinstance(saved.get('account'),str) and saved['account'],
                    'setup not actually saved/bound by original A')
            a = self.closure(self.quit_current())
            self.before(135, 'A closure missed setup/readiness cutoff; no B')
            admission_b = self.p.readmit_saved_state(admission_a, saved, a, self.deadline - 135)
            require(admission_b.get('fresh_after_closure') is True
                    and admission_b.get('a_release_id') == a['release_id']
                    and admission_b.get('admission_id') != admission_a.get('admission_id')
                    and admission_b.get('request_sha256') == saved['request_sha256']
                    and admission_b.get('account') == saved['account']
                    and admission_b.get('ledger_standing') == 'absent setup-only',
                    'fresh B admission unavailable')
            self.before(135, 'readmission missed cutoff; no B')
            b = self.launch('B', admission_b)
            ready = self.p.observe_ready(b, self.deadline - 135)
            require(ready.get('incarnation') == b and ready.get('full_source_gate') is True
                    and ready.get('ready') is True and ready.get('zero_observed_work') is True
                    and isinstance(ready.get('generation'),dict)
                    and set(ready['generation']) == {'appSession','home','spawnCounter'}
                    and isinstance(ready['generation']['appSession'],str) and ready['generation']['appSession']
                    and isinstance(ready['generation']['home'],str) and ready['generation']['home']
                    and type(ready['generation']['spawnCounter']) is int and ready['generation']['spawnCounter'] == 1
                    and ready.get('request_sha256') == saved['request_sha256']
                    and ready.get('account') == saved['account'], 'actual B ready/source unavailable')
            self.result['generation'] = ready['generation']
            self.before(135, '160s setup/readiness cutoff; no Stop')
            self.p.sheet_preflight(b, ready, min(self.clock() + 5, self.deadline - 135))
            self.before(135, 'preflight missed cutoff; no Stop')
            # Intent consumed before dispatch, even if delivery is uncertain.
            self.stop_posted = True
            self.sheet_pending = True
            self.p.post_stop_once(b, ready, min(self.clock() + 20, self.deadline - 115))
            modal_end = min(self.clock() + 30, self.deadline - 85)
            try:
                cancel = self.p.discover_cancel(b, ready, min(self.clock() + 15, modal_end - 15))
                # Question/capture witness failures cannot invalidate separate
                # valid Cancel proof; ports retain them as failed evidence.
                try:
                    self.p.observe_question_if_budget(b, ready, cancel, modal_end - 10)
                except BaseException as observation_error:
                    self.result['observation_failure'] = str(observation_error)
                    self.safe_record('question-observation-failed', {'reason': str(observation_error), 'cancel_bound': True})
                try:self.p.cancel_once(b, cancel, min(self.clock() + 10, modal_end))
                finally:self.cancel_attempted = self.p.cancel_dispatch_attempted(b) is True
            except BaseException as error:
                self.result['automated_cancel_failure'] = str(error)
                delivered = self.fallback(error)
                require(delivered, 'owner fallback not delivered; retain custody')
                completion = self.p.wait_owner_completion(b, self.deadline - 40)
                require(completion == 'Cancelled', 'actual owner Cancel completion unavailable')
                self.p.record_owner_completion(b, completion)
                # Do not repeat agent Cancel. Owner fallback was explicitly
                # selected; report immediately, not at the fixed deadline.
            dismissal = self.p.verify_dismissal_and_source(b, ready, self.deadline - 40)
            require(dismissal.get('same_source') is True and dismissal.get('sheet_absent') is True
                    and dismissal.get('ready') is True and dismissal.get('incarnation') == b,
                    'actual dismissal/source unavailable; no Quit')
            self.sheet_pending = False
            self.before(40, 'dismissal exceeded Quit-entry reserve')
            b_closed = self.closure(self.quit_current())
            self.result['witness_complete'] = not any(k in self.result for k in ('observation_failure','automated_cancel_failure'))
        except BaseException as error:
            self.result.update(witness_complete=False, error=str(error))
            if self.current is not None or self.custody_unknown:
                if self.sheet_pending or self.identity_unsupported or self.custody_unknown:
                    self.fallback(error)
                    self.retain(error)
                else:
                    try:self.closure(self.quit_current())
                    except BaseException as cleanup_error:
                        self.result['cleanup_error'] = str(cleanup_error)
                        self.retain(cleanup_error)
        self.result.update(incarnations=list(self.incarnations), custody_held=self.current is not None or self.custody_unknown,
                           custody_unknown=self.custody_unknown, delivery_errors=self.delivery_errors,
                           elapsed=self.clock() - slot_acquired, overrun=max(0, self.clock() - self.deadline))
        self.safe_record('attended-result', self.result)
        if self.delivery_errors:self.result['witness_complete']=False
        return dict(self.result)
