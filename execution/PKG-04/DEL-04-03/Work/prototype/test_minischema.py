"""Conditional assertion regressions; standard-library runner, optional oracle."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

import minischema as mini

try:
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
except ImportError:
    Draft202012Validator = None


class ConditionalTests(unittest.TestCase):
    def assert_cases(self, schema, cases, resources=()):
        mini.check_supported(schema)
        reg = mini.Registry()
        for source in resources:
            mini.check_supported(source)
            reg.add(source)
        oracle = None
        if Draft202012Validator is not None:
            reference = Registry()
            for source in resources:
                reference = reference.with_resource(source['$id'], Resource.from_contents(
                    dict(source, **{'$schema': 'https://json-schema.org/draft/2020-12/schema'})))
            oracle = Draft202012Validator(schema, registry=reference)
        for instance, expected in cases:
            with self.subTest(schema=schema, instance=instance):
                self.assertEqual(not mini.validate(instance, schema, reg), expected)
                if oracle is not None:
                    self.assertEqual(oracle.is_valid(instance), expected)

    def test_native_turn_requires_workflow_form_thread_and_completed_check(self):
        source = json.loads((Path(__file__).parents[1] / 'RS_RECORD.schema.json').read_text())
        condition = source['$defs']['suppliedGuidance']['allOf'][2]
        good = {'nativeTurn': 'fx-turn', 'supplyForm': 'workflow run start (turn text)',
                'thread': 'fx-thread', 'supplyCheck': 'verified'}
        cases = [(good, True), ({}, True)]
        for key, value in [('supplyForm', 'role guidance at conversation start'),
                           ('thread', ''), ('supplyCheck', 'not checked')]:
            bad = copy.deepcopy(good)
            bad[key] = value
            cases.append((bad, False))
        ended = dict(good, supplyForm='workflow run end notice (turn text)')
        cases.append((ended, True))
        self.assert_cases(condition, cases)
        reg = mini.Registry()
        self.assertEqual(reg.load(Path(__file__).parents[1] / 'RS_RECORD.schema.json'), source['$id'])

    def test_condition_selects_only_its_branch(self):
        self.assert_cases({'if': {'type': 'string'}, 'then': {'minLength': 2},
                           'else': {'type': 'boolean'}},
                          [('ok', True), ('x', False), (True, True), (1, False)])
        for condition, expected in [(True, False), (False, True)]:
            self.assert_cases({'if': condition, 'then': False, 'else': True}, [(None, expected)])

    def test_absent_and_unselected_branches_are_ignored(self):
        missing = {'$ref': 'urn:chirality:prototype:absent'}
        self.assert_cases({'then': missing, 'else': missing}, [(None, True)])
        self.assert_cases({'if': True, 'else': missing}, [(None, True)])
        self.assert_cases({'if': False, 'then': missing}, [(None, True)])
        self.assert_cases({'if': {'type': 'string'}, 'then': {'minLength': 2}},
                          [('x', False), (0, True)])

    def test_nested_and_local_reference_conditions(self):
        schema = {'$defs': {'condition': {'type': 'integer'}},
                  'if': {'$ref': '#/$defs/condition'},
                  'then': {'if': {'minimum': 2}, 'then': True, 'else': False},
                  'else': {'type': 'boolean'}}
        self.assert_cases(schema, [(1.0, False), (2.0, True), (True, True), (1.5, False)])
        self.assert_cases({'allOf': [{'type': 'string'}], 'if': {'$ref': '#/allOf/0'},
                           'then': {'minLength': 2}}, [('ok', True), ('x', False), (1, False)])

    def test_registered_reference_conditions(self):
        target = {'$id': 'urn:chirality:prototype:condition', 'type': 'boolean'}
        self.assert_cases({'if': {'$ref': target['$id']}, 'then': {'const': True},
                           'else': {'const': 'fallback'}},
                          [(True, True), (False, False), ('fallback', True), (0, False)], [target])

    def test_json_equality_does_not_confuse_booleans_and_numbers(self):
        for keyword, value in [('const', 1), ('enum', [1])]:
            schema = {keyword: value}
            self.assert_cases(schema, [(1, True), (1.0, True), (True, False), (False, False)])
        self.assert_cases({'const': {'nested': [False, 1]}},
                          [({'nested': [False, 1.0]}, True), ({'nested': [0, True]}, False)])
        self.assert_cases({'enum': [{'nested': [1]}]},
                          [({'nested': [1.0]}, True), ({'nested': [True]}, False)])
        self.assert_cases({'if': {'const': 1}, 'then': True, 'else': False},
                          [(1.0, True), (True, False)])
        self.assert_cases({'if': {'enum': [False]}, 'then': True, 'else': False},
                          [(False, True), (0, False)])

    def test_integer_predicates_follow_json_numeric_value(self):
        self.assert_cases({'type': 'integer'},
                          [(1, True), (1.0, True), (1.5, False), (True, False), ('1', False)])
        self.assert_cases({'if': {'type': 'integer'}, 'then': True, 'else': False},
                          [(1.0, True), (1.5, False), (True, False)])

    def test_unresolved_predicates_are_schema_errors(self):
        target = {'$id': 'urn:chirality:prototype:known', 'type': 'string'}
        reg = mini.Registry()
        reg.add(target)
        for ref in ['urn:chirality:prototype:absent', '#/absent', target['$id'] + '#/absent']:
            with self.subTest(ref=ref), self.assertRaises(mini.SchemaError):
                mini.validate(None, {'if': {'$ref': ref}, 'else': True}, reg)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'root.json'
            path.write_text(json.dumps({'$id': 'urn:chirality:prototype:relative',
                                        'if': {'$ref': 'missing.json'}, 'else': True}))
            sid = reg.load(path)
            with self.assertRaises(mini.SchemaError):
                mini.validate(None, reg.by_id[sid], reg)

    def test_unknown_keywords_still_refuse_every_conditional_subschema(self):
        for branch in ['if', 'then', 'else']:
            with self.subTest(branch=branch), self.assertRaises(mini.SchemaError):
                mini.check_supported({branch: {'unevaluatedProperties': False}})
        with self.assertRaises(mini.SchemaError):
            mini.check_supported({'if': True, 'else': {'allOf': [{'unknown': True}]}})
        with self.assertRaises(mini.SchemaError):
            mini.check_supported({'if': True, 'then': 0})


if __name__ == '__main__':
    unittest.main()
