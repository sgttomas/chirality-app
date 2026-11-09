"""Current source-bound destination closure; scripted evidence, never a host witness."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
INPUTS = ROOT / 'app/contract_inputs'
LOOP = INPUTS / 'PKG-05/DEL-05-01/Work'
RS = INPUTS / 'PKG-04/DEL-04-03/Work'
AS = INPUTS / 'PKG-04/DEL-04-02/Work'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


flow = load('current_destination_flow', LOOP / 'prototype/destination_flow.py')
panel = load('current_destination_panel', INPUTS / 'PKG-05/DEL-05-02/Work/prototype/panel_double.py')
TURN = dict(hostIdentity='FX-PIPE-01', conversationId='conversation:one', runId='run:one', turnId='turn:one')


def run():
    return flow.Run(TURN['runId'], flow.base_settings(), conversation_id=TURN['conversationId'])


def request(r, call='call:one', turn=TURN):
    return r.request(call, {'category': 'other APIs', 'destination': 'A-1'}, 'invented read',
                     'once', carried=('OP-A1', 'other APIs', 'A-1'), turn_ref=turn)


def validator(path, pointer=None):
    schema = json.loads(path.read_bytes())
    if pointer:
        schema['$ref'] = pointer
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


class FailedTurnPermissionsTest(unittest.TestCase):
    def test_only_unanswered_requests_of_the_exact_failed_turn_close(self):
        r = run()
        other = {**TURN, 'turnId': 'turn:other'}
        request(r)
        request(r, 'call:other', other)
        request(r, 'call:second')
        request(r, 'call:done')
        r.answer('call:done', 'grant', 'once')
        # A dispatched call whose outcome is unknown must not be recast as unsent.
        unknown = {'class': 4, 'label': 'outcome unknown', 'reporter': 'loop', 'deferred': True}
        r.requests['call:done']['result'] = copy.deepcopy(unknown)
        r.results['call:done'] = copy.deepcopy(unknown)
        done = copy.deepcopy((r.requests['call:done'], r.results['call:done']))
        before_grants = copy.deepcopy(r.nl.grants)
        before_contacts = [e for e in r.entries if e['kind'] == 'destination_contacted']
        self.assertEqual(r.fail_turn(TURN), ['call:one', 'call:second'])
        self.assertEqual(r.requests['call:other']['state'], 'pending')
        self.assertEqual(done, (r.requests['call:done'], r.results['call:done']))
        self.assertEqual(r.nl.grants, before_grants)
        self.assertEqual([e for e in r.entries if e['kind'] == 'destination_contacted'], before_contacts)
        closed = [e for e in r.entries if e['kind'] == 'destination_request_closed']
        self.assertEqual(len(closed), 2)
        for e in closed:
            self.assertEqual(e['body']['cause'], 'turn failed')
            self.assertFalse(e['body']['carriedCallSent'])
            self.assertEqual(e['body']['turnRef'], TURN)
            self.assertEqual(e['runId'], TURN['runId'])
            self.assertEqual(e['context']['hostIdentity'], TURN['hostIdentity'])
        self.assertNotIn('call:one', r.results)
        self.assertEqual(r.fail_turn(TURN), [])  # idempotence, no duplicate closure

    def test_late_answer_or_request_cannot_reopen_failed_turn(self):
        r = run()
        request(r)
        r.fail_turn(TURN)
        original = copy.deepcopy((r.requests, r.entries, r.nl.grants, r.results))
        for answer in ['grant', 'decline', 'confirmation lost', 'control refuses']:
            with self.subTest(answer=answer), self.assertRaises(ValueError):
                r.answer('call:one', answer, 'once')
        with self.assertRaises(ValueError):
            request(r, 'call:late')
        self.assertEqual(original, (r.requests, r.entries, r.nl.grants, r.results))

    def test_wrong_source_conversation_run_and_ambiguous_binding_fail_closed(self):
        for field in TURN:
            with self.subTest(field=field):
                r = run()
                request(r)
                before = copy.deepcopy((r.requests, r.entries, r.results))
                altered = {**TURN, field: 'other'}
                if field == 'turnId':
                    self.assertEqual(r.fail_turn(altered), [])
                else:
                    with self.assertRaises(ValueError):
                        r.fail_turn(altered)
                self.assertEqual(before, (r.requests, r.entries, r.results))
        r = run()
        request(r, turn=None)  # historical, source/turn not established
        self.assertEqual(r.fail_turn(TURN), [])
        self.assertEqual(r.requests['call:one']['state'], 'pending')
        with self.assertRaises(ValueError):
            r.answer('call:one', 'grant', 'once')
        self.assertFalse(r.results)
        self.assertFalse(r.nl.grants)

    def test_new_unbound_request_and_late_answer_after_failure_are_withheld(self):
        r = run()
        r.fail_turn(TURN)
        before = copy.deepcopy((r.requests, r.entries, r.nl.grants, r.results))
        with self.assertRaises(ValueError):
            request(r, 'call:unbound', turn=None)
        with self.assertRaises(ValueError):
            r.answer('call:unbound', 'grant', 'once')
        self.assertEqual(before, (r.requests, r.entries, r.nl.grants, r.results))
        # A demonstrably different turn remains able to request and act.
        request(r, 'call:other', turn={**TURN, 'turnId': 'turn:other'})
        self.assertEqual(r.answer('call:other', 'grant', 'once'), 'granted')
        self.assertEqual(r.results['call:other']['label'], 'success (ran)')

    def test_original_turn_binding_is_frozen_and_duplicate_call_cannot_replace_it(self):
        r = run()
        binding = copy.deepcopy(TURN)
        request(r, turn=binding)
        binding['turnId'] = 'mutated'
        self.assertEqual(r.requests['call:one']['turnRef'], TURN)
        with self.assertRaises(ValueError):
            request(r, turn={**TURN, 'turnId': 'other'})
        self.assertEqual(r.fail_turn(TURN), ['call:one'])

    def test_current_loop_rs_and_settings_schemas_carry_truthful_cause_and_binding(self):
        r = run()
        request(r)
        r.fail_turn(TURN)
        loop = r.loop_record('call:one')
        closed = next(e for e in r.entries if e['kind'] == 'destination_request_closed')['body']
        settings = dict(requestRef='rec:request', target=loop['target'], scopeSought='once',
                        state='unanswered at end', stateReason='turn failed', turnRef=TURN)
        samples = [(validator(LOOP / 'LOOP_DESTINATION_REQUEST.schema.json'), loop, 'endCause'),
                   (validator(RS / 'RS_RECORD.schema.json', '#/$defs/destinationRequestClosed'), closed, 'cause'),
                   (validator(AS / 'AS_SETTINGS_IN.schema.json', '#/$defs/destinationSettings/properties/agentRequests/items'), settings, 'stateReason')]
        for check, good, cause in samples:
            with self.subTest(cause=cause):
                check.validate(good)
                missing = copy.deepcopy(good); missing.pop('turnRef')
                self.assertFalse(check.is_valid(missing))
                for field in TURN:
                    incomplete = copy.deepcopy(good); incomplete['turnRef'].pop(field)
                    self.assertFalse(check.is_valid(incomplete))
                wrong = {**good, cause: 'timed out; granted'}
                self.assertFalse(check.is_valid(wrong))
        for field, value in [('grantScope', 'once'), ('result', {'class': 3, 'label': 'granted', 'reporter': 'host control'}),
                             ('interimNotice', "waiting for the person's answer")]:
            self.assertFalse(samples[0][0].is_valid({**loop, field: value}))
        self.assertFalse(flow.schema_subset.validate(loop, json.loads((LOOP / 'LOOP_DESTINATION_REQUEST.schema.json').read_bytes())))

    def test_subset_validator_enforces_new_conditional_keywords(self):
        schema = {'allOf': [{'if': {'required': ['failed']}, 'then': {'required': ['turn']},
                             'else': {'not': {'required': ['turn']}}}]}
        for value, accepted in [({}, True), ({'turn': 'one'}, False), ({'failed': True}, False),
                                ({'failed': True, 'turn': 'one'}, True)]:
            self.assertEqual(not flow.schema_subset.validate(value, schema), accepted)
            self.assertEqual(Draft202012Validator(schema).is_valid(value), accepted)
        with self.assertRaises(flow.schema_subset.UnsupportedKeyword):
            flow.schema_subset.validate({}, {'unknownKeyword': True})

    def test_panel_closes_matching_prompt_and_withholds_late_answer(self):
        def issued(n, req, turn):
            return dict(ordinal=n, kind='destination request issued', request=req, destination='A-1', turnRef=turn)
        failure = dict(ordinal=3, kind='turn failed', turn=TURN['turnId'], cause='model interface failure',
                       message_standing='interrupted', turnRef=copy.deepcopy(TURN))
        events = [issued(1, 'one', TURN), issued(2, 'other', {**TURN, 'turnId': 'other'}), failure,
                  dict(ordinal=4, kind='destination grant observed', request='one', turnRef=TURN),
                  issued(5, 'late', TURN)]
        shown = panel.reduce(events, set())
        self.assertIn('FD-4 destination request one for A-1: not answered, turn failed; no grant shown; requesting call not sent', shown)
        self.assertFalse(any('request other for A-1: not answered' in line for line in shown))
        self.assertFalse(any(line == 'destination grant observed for request one' for line in shown))
        self.assertIn('FD-4 late request late withheld: turn failed; no choices or grant', shown)

    def test_panel_new_unbound_prompt_and_late_answers_after_failure_are_withheld(self):
        for failed_binding in [TURN, None]:
            with self.subTest(failed_binding=failed_binding):
                other = {**TURN, 'turnId': 'turn:other'}
                events = [dict(ordinal=1, kind='turn failed', turn=TURN['turnId'],
                               cause='model interface failure', message_standing='interrupted', turnRef=failed_binding),
                          dict(ordinal=2, kind='destination request issued', request='unbound', destination='A-1'),
                          dict(ordinal=3, kind='destination grant observed', request='unbound'),
                          dict(ordinal=4, kind='destination grant observed', request='unseen'),
                          dict(ordinal=5, kind='destination request issued', request='other', destination='A-1', turnRef=other),
                          dict(ordinal=6, kind='destination grant observed', request='other', turnRef=other)]
                shown = panel.reduce(events, set())
                self.assertIn('FD-4 request unbound: source/turn binding unavailable; choices withheld; no closure inferred', shown)
                self.assertNotIn('destination request unbound for A-1 shown (ND-2)', shown)
                for req in ['unbound', 'unseen']:
                    self.assertNotIn(f'destination grant observed for request {req}', shown)
                    self.assertIn(f'FD-4 late or ambiguous answer for request {req} withheld; no grant inferred', shown)
                self.assertIn('destination grant observed for request other', shown)

    def test_panel_retains_ambiguous_failure_for_later_bound_requests(self):
        conflicting = {**TURN, 'turnId': 'turn:conflicting'}
        for failure_binding, affected in [(None, [TURN]), (conflicting, [TURN, conflicting])]:
            for request_binding in affected:
                with self.subTest(failure_binding=failure_binding, request_binding=request_binding):
                    other = {**TURN, 'turnId': 'turn:unaffected'}
                    for pending_before_failure in [False, True]:
                        events = []
                        def event(kind, **fields):
                            events.append(dict(ordinal=len(events)+1, kind=kind, **fields))
                        if pending_before_failure:
                            event('destination request issued', request='affected', destination='A-1', turnRef=request_binding)
                            event('destination request issued', request='other', destination='A-1', turnRef=other)
                        event('turn failed', turn=TURN['turnId'], cause='model interface failure',
                              message_standing='interrupted', turnRef=failure_binding)
                        if not pending_before_failure:
                            event('destination request issued', request='affected', destination='A-1', turnRef=request_binding)
                            event('destination request issued', request='other', destination='A-1', turnRef=other)
                        event('destination grant observed', request='affected', turnRef=request_binding)
                        event('destination grant observed', request='other', turnRef=other)
                        shown = panel.reduce(events, set())
                        if not pending_before_failure:
                            self.assertNotIn('destination request affected for A-1 shown (ND-2)', shown)
                            self.assertIn('FD-4 request affected: failed-turn correlation unresolved; choices withheld; no closure inferred', shown)
                        self.assertNotIn('destination grant observed for request affected', shown)
                        self.assertFalse(any('request affected for A-1: not answered, turn failed' in line for line in shown))
                        self.assertIn('destination grant observed for request other', shown)

    def test_panel_mismatched_or_missing_provenance_never_infers_grant(self):
        for turn in [None, {**TURN, 'hostIdentity': 'other-host'}, {**TURN, 'conversationId': 'other-conversation'}]:
            with self.subTest(turn=turn):
                events = [dict(ordinal=1, kind='destination request issued', request='one', destination='A-1', turnRef=TURN),
                          dict(ordinal=2, kind='destination grant observed', request='one', turnRef=turn)]
                shown = panel.reduce(events, set())
                self.assertNotIn('destination grant observed for request one', shown)
                self.assertTrue(any('withheld; no grant inferred' in line for line in shown))


if __name__ == '__main__':
    unittest.main()
