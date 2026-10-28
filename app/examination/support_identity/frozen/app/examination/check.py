#!/usr/bin/env python3
"""Offline file examination support. Never executes a supplier or claims qualification."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator
from referencing import Registry

from rules import identity_violations, rule_violations

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
SCHEMAS = {'result': 'exam.result-record.schema.json', 'package': 'pkg.identity-record.schema.json'}
LIMITS = [
    'File structure and declared consistency only; observation origin is unverified.',
    'No package bytes, signatures, notarisation, native run, human act or qualification verified.',
    'EXP review/change-impact records, runner admission and SQ dossiers are not checked by this slice.',
    'SIGN-1 Option B remains selected; OI-011 SWB co-owner work remains open.',
]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate JSON key: {key}')
        result[key] = value
    return result


def parse(data):
    def invalid_constant(value):
        raise ValueError(f'non-JSON numeric constant: {value}')
    return json.loads(data, object_pairs_hook=unique_object, parse_constant=invalid_constant)


class Support:
    """Pin-check canonical sources before validating any record; no remote retrieval."""
    def __init__(self, project=PROJECT, manifest=HERE / 'sources.json'):
        self.sources = parse(Path(manifest).read_bytes())
        self.schemas = {}
        self.prototype_digest = None
        for relative, pin in self.sources['sources'].items():
            data = (Path(project) / relative).read_bytes()
            if digest(data) != pin['sha256']:
                raise ValueError(f'canonical source changed; reviewed adoption required: {relative}')
            if relative.endswith('/prototype/check_exp.py'):
                self.prototype_digest = 'sha256:' + digest(data)
            for kind, filename in SCHEMAS.items():
                if relative.endswith('/' + filename):
                    schema = parse(data)
                    Draft202012Validator.check_schema(schema)
                    self.schemas[kind] = schema
        if set(self.schemas) != set(SCHEMAS) or self.prototype_digest is None:
            raise ValueError('source manifest is incomplete')
        # An empty explicit registry fails unresolved external references locally.
        self.validators = {k: Draft202012Validator(s, registry=Registry()) for k, s in self.schemas.items()}

    def validate(self, kind, record):
        errors = sorted(self.validators[kind].iter_errors(record), key=lambda e: str(list(e.path)))
        if errors:
            return [{'code': 'SCHEMA', 'path': list(e.path), 'message': e.message} for e in errors]
        codes = rule_violations(record) if kind == 'result' else identity_violations(record)
        return [{'code': code} for code in sorted(set(codes))]

    def package_link(self, result, package, revision, build, pin, package_ref):
        errors = [{'record': kind, **e} for kind, r in [('result', result), ('package', package)]
                  for e in self.validate(kind, r)]
        blockers = []
        if errors:
            return errors, ['invalid record; package claims not evaluated']
        def require(condition, code):
            if not condition:
                errors.append({'code': code})
        subject = result['subject'].get('app_candidate', {})
        require(result['run_basis'] == 'candidate', 'LINK-CANDIDATE-BASIS')
        require(result['configuration']['route']['kind'] == 'native_packaged', 'LINK-PACKAGED-ROUTE')
        require(subject.get('packaged') is True, 'LINK-PACKAGED-SUBJECT')
        require(subject.get('package_record') == package_ref, 'LINK-PACKAGE-REFERENCE')
        require(subject.get('revision') == package['app']['revision'] == revision, 'LINK-REVISION')
        require(subject.get('build_identity') == package['app']['build_identity'] == build, 'LINK-BUILD')
        require(result['configuration']['codex_pin'] == package['codex']['pin'] == pin, 'LINK-PIN')
        support = result['support_revision']
        require(support['exp_version'] == package['support_revision'] == 'EXP-v0.2', 'LINK-SUPPORT-VERSION')
        require(support['schema_id'] == self.schemas['result']['$id'], 'LINK-SUPPORT-SCHEMA')
        # §4.4 needs prototype identity; the schema only makes it optional. A
        # standalone schema check remains separate from this stronger join check.
        require(support.get('prototype_digest') == self.prototype_digest, 'LINK-SUPPORT-DIGEST')
        require(result['currency']['state'] == 'current', 'LINK-HISTORICAL-RESULT')
        if package['signing']['option'] != 'B_supplier_signatures_kept':
            blockers.append('SIGN-1 Option B selected; Option A requires its separate adopted change')
        for key in ('fp1a', 'fp1b', 'fp3'):
            if package.get('first_package_checks', {}).get(key, {}).get('outcome') != 'pass':
                blockers.append(f'{key} has no reported pass; Option B cannot be relied on')
        if not package['complete']:
            blockers.append('package content reported incomplete')
        if result['outcome'] != 'pass':
            blockers.append(f"linked native result reported {result['outcome']}")
        return errors, blockers


def load_record(path):
    data = Path(path).read_bytes()
    return parse(data), {'path': str(path), 'sha256': digest(data)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    validate = commands.add_parser('validate', help='Check one declared record; does not establish its outcome')
    validate.add_argument('kind', choices=SCHEMAS)
    validate.add_argument('record')
    link = commands.add_parser('package-link', help='Check a selected EXP/PKG pair against an explicit candidate')
    link.add_argument('result')
    link.add_argument('package')
    for name in ('revision', 'build', 'pin', 'package-ref'):
        link.add_argument('--' + name, required=True)
    args = parser.parse_args(argv)
    try:
        support = Support()
        if args.command == 'validate':
            record, identity = load_record(args.record)
            errors = support.validate(args.kind, record)
            report = {'inputs': [identity], 'errors': errors}
        else:
            result, result_identity = load_record(args.result)
            package, package_identity = load_record(args.package)
            errors, blockers = support.package_link(result, package, args.revision, args.build, args.pin, args.package_ref)
            report = {'inputs': [result_identity, package_identity], 'errors': errors,
                      'selected_candidate': {'revision': args.revision, 'build_identity': args.build, 'codex_pin': args.pin},
                      'selected_package_reference': args.package_ref,
                      'reported_prerequisite_gaps': blockers,
                      'option_b_reliance': 'not_established_by_file_check',
                      'native_qualification': 'not_established_by_file_check'}
        report.update({'file_checks_passed': not errors, 'limits': LIMITS,
                       'tool_sha256': digest(Path(__file__).read_bytes()),
                       'rules_sha256': digest((HERE / 'rules.py').read_bytes()),
                       'source_manifest_sha256': digest((HERE / 'sources.json').read_bytes())})
        print(json.dumps(report, indent=2))
        return 1 if errors else 0
    except (OSError, ValueError) as error:
        print(json.dumps({'file_checks_passed': False, 'input_error': str(error), 'limits': LIMITS}, indent=2))
        return 2


if __name__ == '__main__':
    sys.exit(main())
