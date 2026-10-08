#!/usr/bin/env python3
"""Freeze/check exact B7 preparation inputs; creates no result, dossier or registration."""
import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
PINS_SHA256 = 'e12b994ce886c7fae13fd162a68a841e7875a51692a494f889ffb4b30d87f9d0'
LIMITS = [
    'Technical preparation and exact selected-source correspondence only; no examination opened or result recorded.',
    'Fixture files are invented unregistered inputs; no workflow authoring, execution, registration or origin installation performed.',
    'J-1 starts empty; fixtures are later examiner drafting examples, not substitutes for the person plan, draft trial, review or A15. Changed actual drafts require a fresh exact binding.',
    'Selected EXP support is preparation, not verified producer use or SQ/native result-consumer adoption.',
    'Candidate/configuration and existing missing inputs remain unassigned; no native observation, qualification or acceptance.',
    'Descriptor-based no-follow reads reject symbolic links; digests do not establish external provenance or authenticated custody.',
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def parse(data):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result: raise ValueError('duplicate JSON key')
            result[key] = value
        return result
    def invalid(_): raise ValueError('non-JSON numeric constant')
    return json.loads(data, object_pairs_hook=unique, parse_constant=invalid)


def require(test, message):
    if not test: raise ValueError(message)


def digest_value(value):
    require(isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value), 'invalid SHA-256')


def read_file(path):
    """Open every component without following links; refuse special files."""
    path = Path(path)
    require('..' not in path.parts, 'path traversal refused')
    if not path.is_absolute(): path = Path.cwd() / path
    fd = os.open(path.anchor, os.O_RDONLY | os.O_DIRECTORY)
    try:
        for index, part in enumerate(path.parts[1:]):
            flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
            if index < len(path.parts[1:]) - 1: flags |= os.O_DIRECTORY
            child = os.open(part, flags, dir_fd=fd)
            os.close(fd); fd = child
        require(stat.S_ISREG(os.fstat(fd).st_mode), 'not a regular file')
        with os.fdopen(fd, 'rb', closefd=False) as stream: return stream.read()
    finally:
        os.close(fd)


def relative_file(root, relative):
    require(isinstance(relative, str) and relative, 'empty source path')
    require(not PurePosixPath(relative).is_absolute() and '\\' not in relative
            and all(x not in ('', '.', '..') for x in relative.split('/')), 'invalid relative source path')
    return read_file(Path(root) / relative)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    exec(compile(read_file(path), str(path), 'exec'), module.__dict__)
    return module


class PreRunInputs:
    def __init__(self):
        pins_bytes = read_file(HERE / 'pre_run_inputs.pins.json')
        require(sha(pins_bytes) == PINS_SHA256, 'pre-run source pins changed')
        self.pins = parse(pins_bytes)
        self.captured = {}
        for relative, expected in self.pins['sources'].items():
            data = relative_file(ROOT, relative)
            require(sha(data) == expected, 'pre-run source drift: ' + relative)
            self.captured[relative] = data
        # Each selected package is exactly the maintained two-file fixture;
        # additional companion files or directories are not silently omitted.
        fixture_root = 'projects/chirality-app-v4/app/examination/standalone/fixtures'
        expected_files = {item['path'] for item in self.pins['fixture_roles'].values()}
        expected_files.add(fixture_root + '/README.md')
        expected_dirs = set()
        for relative in expected_files:
            parent = PurePosixPath(relative).parent
            while str(parent).startswith(fixture_root):
                expected_dirs.add(str(parent)); parent = parent.parent
        def inventory(relative):
            with os.scandir(Path(ROOT) / relative) as entries:
                for entry in entries:
                    name = relative + '/' + entry.name
                    require(not entry.is_symlink(), 'fixture link refused')
                    if entry.is_dir(follow_symlinks=False):
                        require(name in expected_dirs, 'unexpected fixture directory')
                        inventory(name)
                    else:
                        require(entry.is_file(follow_symlinks=False) and name in expected_files,
                                'unexpected fixture file')
        inventory(fixture_root)
        for item in self.pins['fixture_roles'].values():
            data = relative_file(ROOT, item['path'])
            require(sha(data) == item['sha256'], 'selected fixture drift: ' + item['path'])
            self.captured[item['path']] = data
        # Existing producers run only from the checked snapshot. Fixture scripts
        # are captured as data and are never imported or executed.
        self.temp = tempfile.TemporaryDirectory(prefix='chirality-pre-run-inputs-')
        self.snapshot = Path(self.temp.name).resolve()
        try:
            for relative, data in self.captured.items():
                target = self.snapshot / relative
                target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(data)
            app = self.snapshot / 'projects/chirality-app-v4/app'
            self.producer = load_module('_b7_pre_run_producer', app / 'examination/standalone/prepare.py')
            self.forms = load_module('_b7_pre_run_blank_forms', app / 'examination/native_forms/native_form.py')
            canonical = load_module('_b7_pre_run_support', app / 'examination/support_identity/canonical.py')
            self.support = canonical.CanonicalSupport()
        except Exception:
            self.close(); raise

    def close(self):
        self.temp.cleanup()

    def __enter__(self): return self
    def __exit__(self, *_): self.close()

    def freeze(self, plan_bytes, expected_plan_sha256):
        digest_value(expected_plan_sha256)
        require(sha(plan_bytes) == expected_plan_sha256, 'exact plan digest mismatch')
        plan = parse(plan_bytes)
        require(not self.producer.validate(plan), 'plan differs from preserved B7 preparation')
        return {
            'artifact_kind': 'standalone_pre_run_inputs', 'preparation_version': 1,
            'standing': 'preparation_only', 'plan_sha256': expected_plan_sha256,
            'source_pins_sha256': PINS_SHA256, 'producer_sha256': sha(read_file(Path(__file__))),
            'source_files': copy.deepcopy(self.pins['sources']),
            'fixture_roles': copy.deepcopy(self.pins['fixture_roles']),
            'support_selection': {
                'purpose': 'preparation_source_correspondence_only',
                'method': self.support.declaration['binding_method'],
                'reader_pins_sha256': sha(self.captured['projects/chirality-app-v4/app/examination/support_identity/canonical-pins.v1.json']),
                'declaration_sha256': self.support.declaration_sha256,
                'publication_reference': copy.deepcopy(self.support.declaration['publication_reference']),
                'support_identity': copy.deepcopy(self.support.identity),
                'producer_use_verified': False, 'result_consumer_adoption': False},
            'candidate_slot': copy.deepcopy(plan['candidate_slot']),
            'missing_inputs': copy.deepcopy(plan['missing_inputs']), 'limits': LIMITS,
        }

    def check(self, selection_bytes, expected_selection_sha256, plan_bytes):
        digest_value(expected_selection_sha256)
        require(sha(selection_bytes) == expected_selection_sha256, 'exact selection digest mismatch')
        selection = parse(selection_bytes)
        require(isinstance(selection, dict) and 'plan_sha256' in selection, 'invalid pre-run selection')
        expected = self.freeze(plan_bytes, selection['plan_sha256'])
        require(not self.producer.differences(selection, expected), 'selection differs from complete fixed preparation')
        return selection


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    freeze = sub.add_parser('freeze'); freeze.add_argument('--plan', required=True)
    freeze.add_argument('--plan-sha256', required=True)
    check = sub.add_parser('check'); check.add_argument('--plan', required=True)
    check.add_argument('--selection', required=True); check.add_argument('--selection-sha256', required=True)
    args = parser.parse_args(argv)
    try:
        with PreRunInputs() as inputs:
            plan = read_file(args.plan)
            if args.command == 'freeze': report = inputs.freeze(plan, args.plan_sha256)
            else:
                inputs.check(read_file(args.selection), args.selection_sha256, plan)
                report = {'preparation_inputs_match': True, 'selection_sha256': args.selection_sha256,
                          'examination_opened': False, 'result_recorded': False,
                          'qualification_claim': False, 'limits': LIMITS}
        print(json.dumps(report, indent=2)); return 0
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(json.dumps({'preparation_inputs_match': False, 'input_error': str(error),
                          'examination_opened': False, 'result_recorded': False,
                          'qualification_claim': False, 'limits': LIMITS}, indent=2)); return 2


if __name__ == '__main__': sys.exit(main())
