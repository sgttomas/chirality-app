"""Explicit package/S4 witness receiving; no legacy downcast or live authority."""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import stat
import sys
import tempfile

from jsonschema import Draft202012Validator
from referencing import Registry

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
PROFILE = 'exp-package-s4-receiving/1'
PINS_SHA256 = '9ee18c539e92098a3d6bc17cf3f065ab83ccd06bed4b3fca8a0cb665554bd9d3'
LIMITS = [
    'Exact selected package/terms/S4 evidence consistency only; actual custody and producer use are not authenticated.',
    'The outer witness record is the EXP/SQ citation; its inner static package ID remains a separate joined identity.',
    'No actual signing, installation, native run, supplier qualification, human act, release or live-start authority is established.',
    'Publisher trust is supplied separately by an explicitly selected receiving configuration, never selected by request evidence.',
    'Missing inputs and reported failures remain gaps; consistency is not qualification or current reliance.',
]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def parse(raw):
    def unique(pairs):
        value = {}
        for key, item in pairs:
            require(key not in value, 'duplicate JSON field')
            value[key] = item
        return value
    def invalid(_):
        raise ValueError('nonfinite JSON')
    return json.loads(raw, object_pairs_hook=unique, parse_constant=invalid)


def exact(value, keys, label):
    require(isinstance(value, dict) and set(value) == set(keys), 'invalid ' + label + ' fields')


def digest(value):
    require(isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value), 'invalid digest')


def read(root, relative):
    require(isinstance(relative, str) and relative and not relative.startswith('/')
            and '\\' not in relative and all(p not in ('', '.', '..') for p in relative.split('/')),
            'invalid relative source/evidence path')
    target = Path(root)
    for part in relative.split('/'):
        target = target / part
        require(not target.is_symlink(), 'source/evidence link refused')
    require(stat.S_ISREG(target.stat().st_mode), 'ordinary source/evidence file required')
    return target.read_bytes()


def module(name, path, raw):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(path), 'exec'), value.__dict__)
    return value


class Receiver:
    def __init__(self, canonical=None):
        raw = (HERE / 'sources.package-v1.json').read_bytes()
        require(sha(raw) == PINS_SHA256, 'package receiving source profile changed')
        self.pins = parse(raw)
        require(self.pins['format'] == PROFILE, 'unknown package receiving profile')
        self.sources = {}
        for path, expected in self.pins['sources'].items():
            payload = read(PROJECT, path)
            require(sha(payload) == expected, 'package receiving source changed: ' + path)
            self.sources[path] = payload
        source = 'app/examination/support_identity/canonical.py'
        self.canonical = canonical or module('_package_canonical', PROJECT / source, self.sources[source]).CanonicalSupport()
        # Packaging resolves its maintained Work closure independently from the
        # EXP worker's historical Design snapshot. Mixing those roots would
        # falsely make the legacy resolver select a partial Design directory.
        self.producer_snapshot = tempfile.TemporaryDirectory(prefix='exp-package-producer-')
        producer_root = Path(self.producer_snapshot.name)
        for path in self.pins['producer_sources']:
            target = producer_root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(self.sources[path])
        source = 'app/packaging/successor/check.py'
        self.producer = module('_selected_packaged_s4_check', producer_root / source, self.sources[source])
        # The exact original EXP validators remain original support, not a new
        # package schema masquerading as PKG-v0.2.
        frozen = self.canonical.support.sources
        source = 'app/examination/rules.py'
        self.rules = module('_package_original_exp_rules', PROJECT / source, frozen[source])
        schemas = [parse(data) for path, data in frozen.items() if path.endswith('/exam.result-record.schema.json')]
        require(len(schemas) == 1, 'missing original EXP result schema')
        self.result_validator = Draft202012Validator(schemas[0], registry=Registry())

    def configuration(self, path, expected):
        digest(expected)
        path = Path(path).absolute()
        raw = read(path.parent, path.name)
        require(sha(raw) == expected, 'receiving configuration digest mismatch')
        value = parse(raw)
        exact(value, ('format', 'trusted_publisher_sha256'), 'receiving configuration')
        require(value['format'] == 'exp-package-receiving-config/1', 'unknown receiving configuration')
        if value['trusted_publisher_sha256'] is not None:
            digest(value['trusted_publisher_sha256'])
        return value

    def receive(self, request_path, evidence_root, config_path, config_sha256):
        config = self.configuration(config_path, config_sha256)
        request_path = Path(request_path).absolute()
        raw = read(request_path.parent, request_path.name)
        request = parse(raw)
        require(request.get('format') == 'packaged-s4-binding/1', 'unsupported package witness version')
        require(isinstance(request.get('record_id'), str) and request['record_id'].strip(), 'missing wrapper identity')
        report = self.producer.check(request_path, evidence_root=Path(evidence_root),
                                     trusted_publisher_sha256=config['trusted_publisher_sha256'])
        exact(report, ('format', 'record_id', 'request_sha256', 'candidate', 'errors', 'missing',
                       'artifacts', 'source_dependencies', 'standing', 'release_authorized',
                       'live_authority', 'limits'), 'package producer report')
        exact(report['candidate'], ('revision', 'build_identity', 'codex_pin', 'package_record_id'), 'package candidate')
        require(report['format'] == 'packaged-s4-check/1' and report['standing'] == 'evidence-consistency-only',
                'unknown package producer report')
        require(report['record_id'] == request['record_id'] and report['request_sha256'] == sha(raw),
                'package wrapper/report identity mismatch')
        require(report['candidate'] == request['candidate'], 'package candidate/report mismatch')
        require(report['record_id'] != report['candidate']['package_record_id'],
                'outer witness and inner static package IDs must differ')
        require(isinstance(report['errors'], list) and isinstance(report['missing'], list), 'invalid package findings')
        require(report['release_authorized'] is False and report['live_authority'] is False,
                'package report cannot grant authority')
        for path, expected in report['source_dependencies'].items():
            require(self.pins['sources'].get(path) == expected, 'unselected package producer dependency: ' + path)
        require(read(request_path.parent, request_path.name) == raw, 'package wrapper changed during read')
        return report

    def binding(self, raw, report, config_sha256):
        digest(config_sha256)
        require(report['request_sha256'] == sha(raw), 'binding package digest mismatch')
        request = parse(raw)
        require(request['format'] == 'packaged-s4-binding/1' and request['record_id'] == report['record_id'],
                'binding package identity mismatch')
        _, condition = self.canonical.source_condition('current_producer_declaration')
        return {'format': 'exp-package-witness-binding/1', 'method': PROFILE,
                'purpose': 'current_producer_declaration', 'source_profile_sha256': PINS_SHA256,
                'receiver_sha256': sha(Path(__file__).read_bytes()),
                'configuration_sha256': config_sha256,
                'artifact': {'kind': 'package_witness', 'record_id': request['record_id'], 'sha256': sha(raw)},
                'candidate': copy.deepcopy(report['candidate']),
                'exp_receiving_support': {'declaration_sha256': self.canonical.declaration_sha256,
                                          'support_identity': copy.deepcopy(self.canonical.identity)},
                'documentary_selection': {key: condition[key] for key in ('method', 'manifest_sha256')}}

    def verify_binding(self, raw, sidecar_raw, report, config_sha256):
        require(parse(sidecar_raw) == self.binding(raw, report, config_sha256),
                'package witness binding or source/configuration selection mismatch')

    def package_link(self, result, report, revision, build, pin, wrapper_ref):
        errors = [{'code': 'SCHEMA', 'path': list(error.path), 'message': error.message}
                  for error in self.result_validator.iter_errors(result)]
        if errors:
            return errors, ['invalid EXP result; package witness join not evaluated']
        errors.extend({'code': code} for code in self.rules.rule_violations(result))
        candidate = report['candidate']
        subject = result['subject'].get('app_candidate', {})
        def equal(condition, code):
            if not condition:
                errors.append({'code': code})
        equal(result['run_basis'] == 'candidate', 'LINK-CANDIDATE-BASIS')
        equal(result['configuration']['route']['kind'] == 'native_packaged', 'LINK-PACKAGED-ROUTE')
        equal(subject.get('packaged') is True, 'LINK-PACKAGED-SUBJECT')
        equal(subject.get('package_record') == wrapper_ref == report['record_id'], 'LINK-WITNESS-REFERENCE')
        equal(subject.get('revision') == candidate['revision'] == revision, 'LINK-REVISION')
        equal(subject.get('build_identity') == candidate['build_identity'] == build, 'LINK-BUILD')
        equal(result['configuration']['codex_pin'] == candidate['codex_pin'] == pin, 'LINK-PIN')
        expected_support = {'exp_version': self.canonical.identity['exp_version'],
                            'schema_id': self.canonical.identity['schema_ids']['result'],
                            'prototype_digest': 'sha256:' + self.canonical.identity['prototype_sha256']}
        equal(result['support_revision'] == expected_support, 'LINK-SUPPORT-IDENTITY')
        equal(result['currency']['state'] == 'current', 'LINK-HISTORICAL-RESULT')
        errors.extend({'code': 'PACKAGE-S4', 'detail': item} for item in report['errors'])
        missing = copy.deepcopy(report['missing'])
        if result['outcome'] != 'pass':
            missing.append('linked native result reported ' + result['outcome'])
        return errors, missing


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('bind', 'package-link'))
    parser.add_argument('--request', required=True); parser.add_argument('--evidence-root', required=True)
    parser.add_argument('--configuration', required=True); parser.add_argument('--configuration-sha256', required=True)
    parser.add_argument('--result'); parser.add_argument('--revision'); parser.add_argument('--build')
    parser.add_argument('--pin'); parser.add_argument('--package-ref')
    args = parser.parse_args(argv)
    try:
        receiver = Receiver()
        report = receiver.receive(args.request, args.evidence_root, args.configuration, args.configuration_sha256)
        if args.command == 'bind':
            require(not report['errors'], 'invalid selected package witness')
            output = receiver.binding(Path(args.request).read_bytes(), report, args.configuration_sha256)
            code = 0
        else:
            require(all((args.result, args.revision, args.build, args.pin, args.package_ref)), 'complete package-link selection required')
            result_bytes = Path(args.result).read_bytes()
            errors, missing = receiver.package_link(parse(result_bytes), report,
                                                     args.revision, args.build, args.pin, args.package_ref)
            output = {'format': 'exp-package-s4-link/1', 'file_checks_passed': not errors,
                      'errors': errors, 'missing': missing, 'package_report': report,
                      'result_input': {'path': args.result, 'sha256': sha(result_bytes)},
                      'source_profile_sha256': PINS_SHA256, 'configuration_sha256': args.configuration_sha256,
                      'qualification_established': False, 'release_authorized': False,
                      'live_authority': False, 'limits': LIMITS}
            code = 1 if errors or missing else 0
        print(json.dumps(output, indent=2)); return code
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(json.dumps({'file_checks_passed': False, 'input_error': str(error),
                          'qualification_established': False, 'release_authorized': False,
                          'live_authority': False, 'limits': LIMITS}, indent=2)); return 2


if __name__ == '__main__':
    sys.exit(main())
