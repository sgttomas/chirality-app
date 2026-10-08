#!/usr/bin/env python3
"""EXP-SUPPORT-BINDING-v1: fixed canonical support selection, not origin authentication."""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import subprocess
import tempfile

from jsonschema import Draft202012Validator
from referencing import Registry

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
PINS_SHA256 = '9ad24d5d6fa38afbeaa39b532f9a10d9550f964f463a8a49356ef254caba35b4'
METHOD = 'EXP-SUPPORT-BINDING-v1'
PURPOSES = ('current_producer_declaration', 'historical_correspondence')
LIMITS = [
    'Fixed canonical support selection and exact-byte consistency only; runtime does not authenticate publication or method adoption.',
    'Current producer binding is a declaration, not verified use; historical correspondence never establishes the basis actually used.',
    'No actual observation, reviewer independence, repair, native run, signing, qualification, acceptance or release established.',
    'Only the supplied current package and bounded result/review/change pair are joined; omitted history and prior package custody remain outside scope.',
    'Filesystem link checks are best effort, not hostile concurrent-filesystem isolation or authenticated custody.',
    'SQ, native-form and S4 receiving adoption and M1 runner/native qualification remain separate.',
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


class CanonicalSupport:
    def __init__(self):
        pins_bytes = (HERE / 'canonical-pins.v1.json').read_bytes()
        if sha(pins_bytes) != PINS_SHA256:
            raise ValueError('canonical reader pins changed')
        self.pins = json.loads(pins_bytes)
        self.captured = {}
        for path, expected in self.pins['sources'].items():
            data = (PROJECT / path).read_bytes()
            if sha(data) != expected:
                raise ValueError('canonical selected source changed: ' + path)
            self.captured[path] = data
        # Load the captured, pinned legacy module without executing an unrelated
        # module from sys.path and without changing its bytes or historical API.
        path = 'app/examination/support_identity/support_identity.py'
        spec = importlib.util.spec_from_file_location('_exp_support_canonical_adapter', PROJECT / path)
        self.legacy = importlib.util.module_from_spec(spec)
        exec(compile(self.captured[path], str(PROJECT / path), 'exec'), self.legacy.__dict__)
        self.support = self.legacy.SupportIdentity()
        self.declaration_bytes = self.captured[self.pins['declaration']]
        self.declaration = self.legacy.parse(self.declaration_bytes)
        self.declaration_sha256 = sha(self.declaration_bytes)
        self.identity = self.declaration['support_identity']
        require = self.legacy.require
        require(self.declaration['binding_method'] == METHOD and self.identity == self.support.identity,
                'canonical support tuple differs from selected published sources')
        # Independently compare all publication source hashes with actual captured
        # source bytes, not just sidecar/declaration equality. Legacy construction
        # also verifies the actual three schema IDs/formats and prototype digest.
        expected = {p: sha(d) for p, d in self.support.sources.items() if p.startswith('execution/')}
        require(self.declaration['sources'] == expected, 'canonical publication sources differ')
        schema = self.legacy.parse(self.captured[self.pins['schema']])
        Draft202012Validator.check_schema(schema)
        self.validator = Draft202012Validator(schema, registry=Registry())

    def binding(self, kind, data, purpose):
        self.legacy.require(purpose in PURPOSES, 'unknown binding purpose')
        binding = self.support.binding(kind, data)
        binding.pop('standing')
        binding.update(format='exp-support-binding.canonical.v1', binding_method=METHOD,
                       binding_purpose=purpose, declaration_sha256=self.declaration_sha256)
        # A caller changing its returned dict must not mutate the reader's basis.
        return copy.deepcopy(binding)

    def check(self, selection_path, expected_sha256):
        legacy = self.legacy
        legacy.checked_digest(expected_sha256)
        selection_path = Path(selection_path)
        data = selection_path.read_bytes()
        legacy.require(sha(data) == expected_sha256, 'canonical selection digest mismatch')
        selected = legacy.parse(data)
        legacy.exact(selected, ('format', 'binding_method', 'binding_purpose', 'declaration_sha256',
                                'artifacts', 'package_selection', 'review_selection', 'change_selection'),
                     'canonical selection')
        legacy.require(selected['format'] == 'exp-support-selection.canonical.v1'
                       and selected['binding_method'] == METHOD, 'unknown canonical method/selection version')
        purpose = selected['binding_purpose']
        legacy.require(purpose in PURPOSES, 'unknown binding purpose')
        legacy.require(selected['declaration_sha256'] == self.declaration_sha256,
                       'caller-selected publication refused')
        legacy.exact(selected['artifacts'], legacy.KINDS, 'canonical artifacts')
        raw = {}; seen = set()
        for role, kind in legacy.KINDS.items():
            pair = selected['artifacts'][role]
            legacy.exact(pair, ('record', 'binding'), 'canonical artifact pair')
            for part in ('record', 'binding'):
                ref = pair[part]
                legacy.exact(ref, ('path', 'sha256'), 'canonical artifact reference')
                legacy.checked_digest(ref['sha256'])
                legacy.require(isinstance(ref['path'], str), 'invalid artifact path')
                legacy.require(ref['path'] not in seen, 'duplicate canonical artifact path')
                seen.add(ref['path'])
                payload = legacy.relative_file(selection_path.parent, ref['path'])
                legacy.require(sha(payload) == ref['sha256'], 'canonical artifact digest mismatch')
                raw[(role, part)] = payload
            binding = legacy.parse(raw[(role, 'binding')])
            legacy.require(not list(self.validator.iter_errors(binding)), 'invalid canonical binding')
            legacy.require(binding == self.binding(kind, raw[(role, 'record')], purpose),
                           'canonical binding identity or purpose mismatch')
        # This is a representation adapter, not another validator engine. Keep
        # exact original record bytes; derive only internal unpublished sidecars.
        with tempfile.TemporaryDirectory(prefix='chirality-canonical-binding-') as temp:
            root = Path(temp)
            adapted = {k: copy.deepcopy(selected[k]) for k in
                       ('package_selection', 'review_selection', 'change_selection')}
            adapted.update(format='exp-support-selection.v1', standing='frozen_candidate_not_published',
                           declaration_sha256=legacy.DECLARATION_SHA256, artifacts={})
            for role, kind in legacy.KINDS.items():
                pair = {}
                for part, payload in [('record', raw[(role, 'record')]),
                                      ('binding', json.dumps(self.support.binding(kind, raw[(role, 'record')])).encode())]:
                    name = role + '.' + part + '.json'
                    (root / name).write_bytes(payload)
                    pair[part] = {'path': name, 'sha256': sha(payload)}
                adapted['artifacts'][role] = pair
            payload = json.dumps(adapted).encode()
            (root / 'selection.json').write_bytes(payload)
            report = self.support.check(root / 'selection.json', sha(payload))
        # Report original canonical inputs, never internal temporary adapter refs.
        return {'canonical_consistency_passed': report['identity_consistency_passed'],
                'errors': report['errors'], 'binding_method': METHOD, 'binding_purpose': purpose,
                'fixed_support_selection': {'declaration_sha256': self.declaration_sha256,
                                            'publication_reference': self.declaration['publication_reference'],
                                            'support_identity': self.identity, 'reader_pins_sha256': PINS_SHA256},
                'selection_sha256': expected_sha256, 'inputs': selected['artifacts'],
                'existing_checks': report['existing_checks'],
                'adapter': {'tool_sha256': sha(self.captured['app/examination/support_identity/support_identity.py']),
                            'standing': 'internal_unpublished_v1_bindings_only'},
                'producer_use_verified': False, 'publication_authority_authenticated': False,
                'method_adoption_authenticated': False, 'qualification_established': False,
                'tool_sha256': sha(Path(__file__).read_bytes()), 'limits': LIMITS}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    bind = sub.add_parser('bind', help='Emit a canonical binding declaration; no validity or producer-use claim')
    bind.add_argument('kind', choices=('result', 'review', 'change', 'package'))
    bind.add_argument('record'); bind.add_argument('--purpose', choices=PURPOSES, required=True)
    check = sub.add_parser('check', help='Check the externally pinned canonical method and selected exact-byte join')
    check.add_argument('selection'); check.add_argument('--selection-sha256', required=True)
    args = parser.parse_args(argv)
    try:
        support = CanonicalSupport()
        if args.command == 'bind':
            report = support.binding(args.kind, Path(args.record).read_bytes(), args.purpose)
            code = 0
        else:
            report = support.check(args.selection, args.selection_sha256)
            code = 0 if report['canonical_consistency_passed'] else 1
        print(json.dumps(report, indent=2)); return code
    except (OSError, ValueError, TypeError, KeyError, subprocess.TimeoutExpired) as error:
        print(json.dumps({'canonical_consistency_passed': False, 'input_error': str(error),
                          'producer_use_verified': False, 'publication_authority_authenticated': False,
                          'method_adoption_authenticated': False, 'qualification_established': False,
                          'limits': LIMITS}, indent=2))
        return 2


if __name__ == '__main__':
    sys.exit(main())
