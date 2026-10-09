#!/usr/bin/env python3
"""CI-26 staged exact-byte support bindings; publication is never established."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import tempfile

from jsonschema import Draft202012Validator
from referencing import Registry

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
DECLARATION_SHA256 = 'c41aad04875ad6059e9a20776e7d57dd27b876afc3159cc242bfa3dc6f8dfc92'
SCHEMA_SHA256 = 'aeda3b2d3e98b94ba3823dfadb3bad4f14e5b73c00da62b19c5e32aab8c431b0'
KINDS = {'before': 'result', 'after': 'result', 'rerun': 'result',
         'review': 'review', 'change': 'change', 'package': 'package'}
RECORD_KINDS = {'result': 'exam_result', 'review': 'exam_review',
                'change': 'exam_change_impact', 'package': 'package_identity'}
LIMITS = [
    'Exact-byte identity and supplied file relationships only; origin and actual observations are unverified.',
    'Frozen candidate declaration is not canonical publication or adoption. A record writer cannot publish support.',
    'Caller-selected artifact/basis digest is a technical freeze, not authorization or an authenticated authority.',
    'No actual review independence, repair, native execution, signatures, qualification, acceptance or release established.',
    'Filesystem link checks are best effort; hostile concurrent filesystem isolation and authenticated custody are not established.',
    'CI-26 canonical disposition and consumer adoption remain with the owning Design loops.',
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def parse(data):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('duplicate JSON key')
            result[key] = value
        return result
    def invalid(_):
        raise ValueError('non-JSON numeric constant')
    return json.loads(data, object_pairs_hook=unique, parse_constant=invalid)


def exact(value, fields, label):
    if not isinstance(value, dict) or set(value) != set(fields):
        raise ValueError(label + ': missing or unknown fields')


def require(test, message):
    if not test:
        raise ValueError(message)


def checked_digest(value):
    require(isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value), 'invalid SHA-256')


def relative_file(root, relative):
    """Contain reads and refuse links/special files; no source files are executed here."""
    require(isinstance(relative, str) and relative != '', 'empty artifact path')
    path = PurePosixPath(relative)
    require(not path.is_absolute() and all(p not in ('', '.', '..') for p in relative.split('/'))
            and '\\' not in relative, 'non-canonical relative path')
    current = Path(root)
    for part in path.parts:
        current = current / part
        mode = current.lstat().st_mode
        require(not stat.S_ISLNK(mode), 'symbolic link refused')
    require(stat.S_ISREG(mode), 'not a regular file')
    return current.read_bytes()


class SupportIdentity:
    def __init__(self):
        # No caller-supplied declaration, source manifest, schema or publication flag.
        declaration = (HERE / 'declaration.v1.json').read_bytes()
        require(sha(declaration) == DECLARATION_SHA256, 'frozen declaration changed')
        self.declaration = parse(declaration)
        schema_bytes = (HERE / 'binding.v1.schema.json').read_bytes()
        require(sha(schema_bytes) == SCHEMA_SHA256, 'binding schema changed')
        schema = parse(schema_bytes)
        Draft202012Validator.check_schema(schema)
        self.validator = Draft202012Validator(schema, registry=Registry())
        self.identity = self.declaration['support_identity']
        # Snapshot every frozen source before any record processing. Existing
        # checkers run from these bytes, so rereads cannot select a different basis.
        self.sources = {}
        for path, expected in self.declaration['sources'].items():
            data = relative_file(PROJECT, path)
            require(sha(data) == expected, 'frozen source changed: ' + path)
            self.sources[path] = data
        for kind, filename in [('result', 'exam.result-record.schema.json'),
                               ('review', 'exam.review-record.schema.json'),
                               ('change', 'exam.change-impact.schema.json')]:
            matches = [data for path, data in self.sources.items() if path.endswith('/' + filename)]
            require(len(matches) == 1 and parse(matches[0])['$id'] == self.identity['schema_ids'][kind],
                    'declared schema identity disagrees with source')
        prototypes = [data for path, data in self.sources.items() if path.endswith('/prototype/check_exp.py')]
        require(len(prototypes) == 1 and sha(prototypes[0]) == self.identity['prototype_sha256'],
                'declared prototype identity disagrees with source')
        # Protocol version and schema formats must agree with the frozen declaration.
        versions = [parse(data)['properties']['format']['const'] for path, data in self.sources.items()
                    if any(path.endswith('/' + name) for name in
                           ('exam.result-record.schema.json', 'exam.review-record.schema.json', 'exam.change-impact.schema.json'))]
        require(versions == [self.identity['exp_version']] * 3, 'declared version disagrees with schemas')

    def binding(self, kind, data):
        """Describe candidate bytes; this method never creates published standing."""
        require(kind in RECORD_KINDS, 'unknown record kind')
        record = parse(data)
        require(isinstance(record, dict) and record.get('record_kind') == RECORD_KINDS[kind], 'record kind mismatch')
        record_id = record.get('record_id')
        require(isinstance(record_id, str) and record_id.strip(), 'missing record identity')
        return {'format': 'exp-support-binding.v1', 'standing': 'frozen_candidate_not_published',
                'declaration_sha256': DECLARATION_SHA256, 'support_identity': self.identity,
                'artifact': {'kind': kind, 'record_id': record_id, 'sha256': sha(data)}}

    def bound_record(self, kind, data, sidecar_bytes):
        sidecar = parse(sidecar_bytes)
        require(not list(self.validator.iter_errors(sidecar)), 'invalid support binding')
        require(sidecar == self.binding(kind, data), 'support binding or artifact identity mismatch')
        record = parse(data)
        expected_format = 'PKG-v0.2' if kind == 'package' else self.identity['exp_version']
        require(record.get('format') == expected_format, 'mixed record versions')
        if kind == 'result':
            support = record.get('support_revision')
            require(support == {'exp_version': self.identity['exp_version'],
                               'schema_id': self.identity['schema_ids']['result'],
                               'prototype_digest': 'sha256:' + self.identity['prototype_sha256']},
                    'result support identity missing or different')
        elif kind == 'package':
            require(record.get('support_revision') == self.identity['exp_version'], 'package support version mismatch')
        return record

    def check(self, selection_path, expected_sha256):
        checked_digest(expected_sha256)
        selection_path = Path(selection_path)
        data = selection_path.read_bytes()
        require(sha(data) == expected_sha256, 'selection digest mismatch')
        selected = parse(data)
        exact(selected, ('format', 'standing', 'declaration_sha256', 'artifacts', 'package_selection',
                         'review_selection', 'change_selection'), 'selection')
        require(selected['format'] == 'exp-support-selection.v1'
                and selected['standing'] == 'frozen_candidate_not_published', 'unsupported selection standing or format')
        require(selected['declaration_sha256'] == DECLARATION_SHA256, 'self-selected declaration refused')
        exact(selected['artifacts'], KINDS, 'artifact selection')
        for name in ('review_selection', 'change_selection'):
            require(isinstance(selected[name], dict), 'invalid join selection')
        exact(selected['package_selection'], ('revision', 'build', 'pin', 'package_ref'), 'package selection')
        for value in selected['package_selection'].values():
            require(isinstance(value, str) and value.strip(), 'empty package selection')
        inputs = {}; records = {}; raw = {}; seen = set()
        for role, kind in KINDS.items():
            item = selected['artifacts'][role]
            exact(item, ('record', 'binding'), 'artifact pair')
            for part in ('record', 'binding'):
                ref = item[part]
                exact(ref, ('path', 'sha256'), 'artifact reference')
                checked_digest(ref['sha256'])
                require(isinstance(ref['path'], str), 'invalid artifact path')
                require(ref['path'] not in seen, 'duplicate artifact path')
                seen.add(ref['path'])
                captured = relative_file(selection_path.parent, ref['path'])
                require(sha(captured) == ref['sha256'], 'artifact digest mismatch: ' + role + '/' + part)
                raw[(role, part)] = captured
            records[role] = self.bound_record(kind, raw[(role, 'record')], raw[(role, 'binding')])
            inputs[role] = item
        # The existing checker uses explicit aliases. The frozen selection binds
        # those aliases and the exact bytes here; matching strings are not origin proof.
        require(records['package']['record_id'] == selected['package_selection']['package_ref'],
                'selected package alias does not identify selected record')
        require(selected['review_selection'].get('subject_alias') == selected['change_selection'].get('to_alias'),
                'review/change target aliases differ')
        ids = [records[k]['record_id'] for k in ('before', 'rerun', 'review', 'change', 'package')]
        require(len(ids) == len(set(ids)), 'duplicate record identity')
        reports = self._existing_checks(raw, selected)
        errors = [{'join': name, **error} for name, report in reports.items() for error in report.get('errors', [])]
        for name, report in reports.items():
            if not report['file_checks_passed'] and not report.get('errors'):
                errors.append({'join': name, 'code': 'EXISTING-CHECK-FAILED'})
            if report.get('unresolved_other_references'):
                errors.append({'join': name, 'code': 'UNRESOLVED-JOIN-REFERENCES'})
        return {'identity_consistency_passed': not errors, 'errors': errors,
                'selection_sha256': expected_sha256, 'declaration_sha256': DECLARATION_SHA256,
                'tool_sha256': sha(Path(__file__).read_bytes()), 'binding_schema_sha256': SCHEMA_SHA256,
                'support_identity': self.identity, 'inputs': inputs,
                'existing_checks': reports, 'publication_established': False, 'adoption_established': False,
                'qualification_established': False, 'limits': LIMITS}

    def _existing_checks(self, raw, selection):
        # Execute unchanged accepted maintained validators over captured bytes in
        # an isolated temporary project; no supplier, native or canonical prototype runs.
        with tempfile.TemporaryDirectory(prefix='chirality-support-identity-') as temp:
            root = Path(temp)
            for relative, data in self.sources.items():
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            records = root / 'inputs'; records.mkdir()
            for role in KINDS:
                (records / (role + '.json')).write_bytes(raw[(role, 'record')])
            for name in ('review_selection', 'change_selection'):
                (records / (name + '.json')).write_text(json.dumps(selection[name]))
            path = lambda name: str(records / (name + '.json'))
            pkg = selection['package_selection']
            jobs = {
                'package': ['app/examination/check.py', 'package-link', path('rerun'), path('package'),
                            '--revision', pkg['revision'], '--build', pkg['build'], '--pin', pkg['pin'],
                            '--package-ref', pkg['package_ref']],
                'review': ['app/examination/admission/admission_check.py', 'review-join',
                           '--review', path('review'), '--result', path('rerun'), '--selection', path('review_selection')],
                'change': ['app/examination/admission/admission_check.py', 'change-join',
                           '--change', path('change'), '--before', path('before'), '--after', path('after'),
                           '--rerun', path('rerun'), '--selection', path('change_selection')],
            }
            reports = {}
            for name, args in jobs.items():
                process = subprocess.run([sys.executable, '-B', *args], cwd=root,
                                         capture_output=True, text=True, timeout=60)
                require(process.returncode in (0, 1), 'existing ' + name + ' checker could not run')
                report = parse(process.stdout)
                # Temp paths are implementation detail, not durable identities.
                report.pop('inputs', None)
                reports[name] = report
            return reports


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    bind = sub.add_parser('bind', help='Emit an unpublished candidate binding; no record validation or publication')
    bind.add_argument('kind', choices=RECORD_KINDS); bind.add_argument('record')
    check = sub.add_parser('check', help='Check an exact-byte frozen selection and all joined records')
    check.add_argument('selection'); check.add_argument('--selection-sha256', required=True)
    args = parser.parse_args(argv)
    try:
        support = SupportIdentity()
        if args.command == 'bind':
            report = support.binding(args.kind, Path(args.record).read_bytes())
            code = 0
        else:
            report = support.check(args.selection, args.selection_sha256)
            code = 0 if report['identity_consistency_passed'] else 1
        print(json.dumps(report, indent=2)); return code
    except (OSError, ValueError, TypeError, KeyError, subprocess.TimeoutExpired) as error:
        print(json.dumps({'identity_consistency_passed': False, 'input_error': str(error),
                          'publication_established': False, 'adoption_established': False,
                          'qualification_established': False, 'limits': LIMITS}, indent=2))
        return 2


if __name__ == '__main__':
    sys.exit(main())
