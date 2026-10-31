#!/usr/bin/env python3
"""Explicit current EXP source adoption; unchanged legacy rules, no frozen fallback."""
import argparse
import builtins
import copy
import hashlib
import json
from pathlib import Path
import sys
import types

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
PROFILE = 'current-v1'
MANIFEST = HERE / 'sources.current-v1.json'
MANIFEST_SHA256 = '4606dbc82a3eb8c526575070263c0d590eaa2c96cdf1f557a148cd16ef637811'
DEPENDENCIES = {
    'admission_check.py': 'bd9a8ef07bdf0c848f8ba09e14b8c3ef977a7a52140c26e5a58f1cf83e7167cf',
    'admission_rules.py': 'b6cb783561cade47855431f0be33190d8fe287a9f5ff05a2da5bbc7953e694a5',
}
LIMITS = [
    'Explicit current full-document source correspondence and unchanged EXP-v0.2 file/rule/join checks only.',
    'Existing records retain their original subjects and support revisions; current source selection does not establish producer use.',
    'No actual review, independence, repair, human act, native execution, supplier qualification, acceptance or release is established.',
    'Only supplied relationships are checked; other evidence, affectedness and unreadable reliance remain with the examination owner.',
    'Recorded SUP1/D2/D3/R23-22 and terms decisions are received, not newly made or authenticated by this reader.',
    'Current source failure never falls back to frozen history; no hostile concurrent-filesystem custody is claimed.',
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def parse(data):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('duplicate JSON key: ' + key)
            result[key] = value
        return result
    def invalid(value):
        raise ValueError('non-JSON constant: ' + value)
    return json.loads(data, object_pairs_hook=unique, parse_constant=invalid)


def _legacy():
    """Load exact unchanged bytes into a private import namespace.

    The legacy module's named admission_rules import resolves only to the
    captured dependency, never a caller's sys.path/sys.modules substitute.
    No shared module entry is replaced and no legacy source is rewritten.
    """
    captured = {}
    for name, expected in DEPENDENCIES.items():
        raw = (HERE / name).read_bytes()
        if sha(raw) != expected:
            raise ValueError('current reader dependency drift: ' + name)
        captured[name] = raw
    rules = types.ModuleType('_current_exp_admission_rules')
    rules.__file__ = str(HERE / 'admission_rules.py')
    exec(compile(captured['admission_rules.py'], rules.__file__, 'exec'), rules.__dict__)
    api = types.ModuleType('_current_exp_admission_legacy')
    api.__file__ = str(HERE / 'admission_check.py')
    def selected_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == 'admission_rules' and level == 0:
            return rules
        return builtins.__import__(name, globals, locals, fromlist, level)
    api.__dict__['__builtins__'] = dict(vars(builtins), __import__=selected_import)
    exec(compile(captured['admission_check.py'], api.__file__, 'exec'), api.__dict__)
    return api


def deliverable_path(root, relative):
    return _legacy().deliverable_path(root, relative)


class Support:
    def __init__(self, project=PROJECT, manifest=MANIFEST, *, profile=None):
        if profile != PROFILE:
            raise ValueError('missing or unknown current admission source profile')
        raw = Path(manifest).read_bytes()
        if sha(raw) != MANIFEST_SHA256:
            raise ValueError('source drift: current admission profile manifest')
        pins = parse(raw)
        if pins['format'] != 'exp-admission-source-profile/1' or pins['profile'] != profile:
            raise ValueError('mixed current admission profile')
        self._api = _legacy()
        expected_dependencies = {'app/examination/admission/' + name: value
                                 for name, value in DEPENDENCIES.items()}
        if pins['reader_dependencies'] != expected_dependencies:
            raise ValueError('mixed current reader dependencies')
        # Support verifies all six complete sources against this selected lock.
        # It does not look in the frozen publication or silently renew a pin.
        self._support = self._api.Support(project=project, manifest=manifest)
        if self._support.manifest_bytes != raw:
            raise ValueError('current profile changed during read')
        if {kind: validator.schema['$id'] for kind, validator in self._support.validators.items()} != pins['support_revision']['schema_ids']:
            raise ValueError('mixed EXP schema identity')
        self.manifest_bytes = raw
        self._selection = {
            'profile': profile, 'format': pins['format'], 'manifest_sha256': sha(raw),
            'basis_revision': pins['basis_revision'], 'read_extent': pins['read_extent'],
            'sources': copy.deepcopy(pins['sources']),
            'reader_dependencies': copy.deepcopy(pins['reader_dependencies']),
            'support_revision': copy.deepcopy(pins['support_revision']),
            'legacy_source_lock': copy.deepcopy(pins['legacy_source_lock']),
            'producer_use_verified': False, 'authority_authenticated': False,
        }

    @property
    def source_selection(self):
        return copy.deepcopy(self._selection)

    @property
    def validators(self):
        return self._support.validators

    def validate(self, *args, **kwargs):
        return self._support.validate(*args, **kwargs)

    def index_results(self, *args, **kwargs):
        return self._support.index_results(*args, **kwargs)

    def review_join(self, *args, **kwargs):
        return self._support.review_join(*args, **kwargs)

    def change_join(self, *args, **kwargs):
        return self._support.change_join(*args, **kwargs)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile', required=True, choices=(PROFILE,))
    subs = parser.add_subparsers(dest='command', required=True)
    val = subs.add_parser('validate'); val.add_argument('kind', choices=('review', 'change'))
    val.add_argument('record'); val.add_argument('--result', action='append', default=[])
    review = subs.add_parser('review-join')
    for field in ('review', 'result', 'selection'):
        review.add_argument('--' + field, required=True)
    change = subs.add_parser('change-join')
    for field in ('change', 'before', 'after', 'selection'):
        change.add_argument('--' + field, required=True)
    change.add_argument('--rerun')
    args = parser.parse_args(argv)
    inputs = []
    def read(path):
        raw = Path(path).read_bytes()
        inputs.append({'path': str(path), 'sha256': sha(raw)})
        return parse(raw)
    try:
        support = Support(profile=args.profile)
        unresolved = []; pending = False
        if args.command == 'validate':
            record = read(args.record)
            records = [read(path) for path in args.result]
            errors, index = support.index_results(records)
            if not errors:
                errors = support.validate(args.kind, record, index)
        elif args.command == 'review-join':
            errors, unresolved = support.review_join(read(args.review), read(args.result), read(args.selection))
        else:
            ci = read(args.change); before = read(args.before); after = read(args.after)
            selected = read(args.selection); rerun = read(args.rerun) if args.rerun else None
            errors, unresolved = support.change_join(ci, before, after, selected, rerun)
            pending = rerun is None
        report = {'format': 'exp-current-admission-check/1', 'file_checks_passed': not errors,
                  'errors': errors, 'scope': args.command, 'inputs': inputs,
                  'source_selection': support.source_selection,
                  'source_lock_sha256': sha(support.manifest_bytes),
                  'tool_sha256': sha(Path(__file__).read_bytes()),
                  'unresolved_other_references': unresolved, 'rerun_not_supplied': pending,
                  'review_or_repair_verified': False, 'route_admission': 'not_established', 'limits': LIMITS}
        print(json.dumps(report, indent=2)); return 1 if errors else 0
    except (ValueError, OSError) as error:
        print(json.dumps({'format': 'exp-current-admission-check/1', 'file_checks_passed': False,
                          'input_error': str(error), 'requested_profile': args.profile,
                          'inputs': inputs, 'review_or_repair_verified': False,
                          'route_admission': 'not_established', 'limits': LIMITS}, indent=2))
        return 2


if __name__ == '__main__':
    sys.exit(main())
