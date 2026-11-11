"""Illustrative PKG-v0.2 identity and terms records; no package, signature or terms answer is examined."""
import importlib.util
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator

APP = Path(__file__).resolve().parents[1]
STATIC = APP / 'packaging/static_distribution'
EXAMPLES = APP / 'tests/group_b_fixtures'


def load_rules():
    spec = importlib.util.spec_from_file_location('group_b_legacy_pkg_rules', STATIC / 'legacy_pkg_rules.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


class LegacyPkgRules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = load_rules()

    def run_examples(self, prefix, rules, valid_ids, invalid_count, expected_rules):
        schema = self.rules.load(prefix + '.schema.json')
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        valid = read(EXAMPLES / (prefix + '.valid.examples.json'))
        self.assertEqual([record['record_id'] for record in valid], valid_ids)
        for record in valid:
            with self.subTest(prefix=prefix, valid=record['record_id']):
                self.assertEqual([e.message for e in validator.iter_errors(record)], [])
                self.assertEqual(rules(record), [])
        invalid = read(EXAMPLES / (prefix + '.invalid.examples.json'))
        self.assertEqual(len(invalid), invalid_count)
        for item in invalid:
            with self.subTest(prefix=prefix, invalid=item['record']['record_id'], why=item['why']):
                self.assertTrue(list(validator.iter_errors(item['record'])))
        violations = read(EXAMPLES / (prefix + '.rule-violations.examples.json'))
        self.assertEqual({item['rule'] for item in violations}, expected_rules)
        for item in violations:
            with self.subTest(prefix=prefix, record=item['record']['record_id'], rule=item['rule']):
                self.assertEqual([e.message for e in validator.iter_errors(item['record'])], [])
                self.assertIn(item['rule'], rules(item['record']))

    def test_identity_examples_and_rule_violations(self):
        self.run_examples('pkg.identity-record', self.rules.identity_violations,
                          ['PKG-EX-01', 'PKG-EX-02', 'PKG-EX-03', 'PKG-EX-04'], 10,
                          {'PK-R1', 'PK-R2', 'PK-R3', 'PK-R5', 'PK-R6', 'PK-R7', 'PK-R8', 'PK-R9'})

    def test_terms_examples_and_rule_violations(self):
        self.run_examples('pkg.terms-record', self.rules.terms_violations,
                          ['PKG-TX-01', 'PKG-TX-02'], 3, {'PK-R4'})


if __name__ == '__main__':
    unittest.main(verbosity=2)
