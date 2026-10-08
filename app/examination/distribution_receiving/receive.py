#!/usr/bin/env python3
"""Check an explicitly selected synthetic Host export against EXP/PKG files.

This is a file-correspondence consumer, not an offline native S1 reader.
"""
import argparse
import hashlib
import importlib.util
import json
import os
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
PINS_SHA256 = 'dca0be539ada665272eb8654ef43a1f5dcce07fdec039517acae61f8cde9fdc6'
FORMAT = 'group-b-s1-reader-exchange.v1'
MAX_BYTES = 32 * 1024 * 1024
LIMITS = [
    'Exact exported file correspondence only; native S1 semantics are not reexecuted.',
    'Serialized readback is a producer report, not authenticated history or a native-held reference capability.',
    'Synthetic Host executable identity and invented application candidate identity are separate; no actual App build is established.',
    'Selected source copies do not establish original source custody, compiled production selection, S3 qualification or adoption.',
    'No native examination, installed custody, signing, supplier qualification or release is established.',
    'No-follow reads and private snapshots are bounded observations, not atomic isolation against a hostile concurrent filesystem.',
]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def parse(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON field: ' + key)
            result[key] = value
        return result
    def invalid(value):
        raise ValueError('nonfinite JSON number: ' + value)
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=invalid)


def exact(value, keys, label):
    require(isinstance(value, dict) and set(value) == set(keys), label + ' fields differ')


def digest(value):
    require(isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value), 'invalid SHA256')


def contained(value):
    require(isinstance(value, str) and value and not value.startswith('/')
            and all(p not in ('', '.', '..') for p in value.split('/'))
            and not any(c in value for c in '\\\x00\n\r'), 'noncontained path')
    return value.split('/')


def read_file(path):
    """Open every absolute component without following symbolic links."""
    path = Path(os.path.abspath(path))
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
    try:
        for component in path.parts[1:-1]:
            child = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd); fd = child
        child = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
        try:
            info = os.fstat(child)
            require(stat.S_ISREG(info.st_mode) and info.st_size <= MAX_BYTES, 'unsupported file kind/size')
            with os.fdopen(child, 'rb', closefd=False) as stream:
                raw = stream.read(MAX_BYTES + 1)
            require(len(raw) <= MAX_BYTES, 'file size limit')
            return raw
        finally:
            os.close(child)
    finally:
        os.close(fd)


def relative(root, path):
    contained(path)
    return read_file(root / path)


def members(root, manifest):
    require(isinstance(manifest, list) and manifest and len(manifest) <= 1024, 'invalid member manifest')
    result = {}; total = 0
    for entry in manifest:
        exact(entry, ('path', 'sha256', 'size'), 'member')
        name = entry['path']; contained(name); digest(entry['sha256'])
        require(name not in result, 'duplicate member')
        require(type(entry['size']) is int and entry['size'] >= 0, 'invalid member size')
        raw = relative(root, name)
        require(len(raw) == entry['size'] and sha(raw) == entry['sha256'], 'member bytes differ: ' + name)
        total += len(raw); require(total <= MAX_BYTES, 'closure size limit'); result[name] = raw
    require(list(result) == sorted(result), 'manifest is not sorted')
    expected_dirs = {'.'}
    for name in result:
        expected_dirs.update(str(p) for p in PurePosixPath(name).parents)
    actual_files = set(); actual_dirs = {'.'}
    require(not root.is_symlink() and root.is_dir(), 'invalid member root')
    for directory, dirs, files in os.walk(root, followlinks=False):
        for name in dirs + files:
            path = Path(directory) / name; info = path.lstat()
            rel = path.relative_to(root).as_posix()
            require(not stat.S_ISLNK(info.st_mode), 'symbolic link in closure')
            if stat.S_ISDIR(info.st_mode):
                actual_dirs.add(rel)
            else:
                require(stat.S_ISREG(info.st_mode), 'unsupported closure entry')
                actual_files.add(rel)
    require(actual_files == set(result) and actual_dirs == expected_dirs, 'closure inventory differs')
    return result


def referenced(files, ref):
    exact(ref, ('path', 'sha256'), 'artifact reference')
    contained(ref['path']); digest(ref['sha256'])
    require(ref['path'] in files and sha(files[ref['path']]) == ref['sha256'], 'unresolved artifact reference')
    return files[ref['path']]


class Receiver:
    def __init__(self):
        raw = read_file(HERE / 'pins.lt12-source-lt09-v1.json')
        require(sha(raw) == PINS_SHA256, 'receiver pins changed')
        self.pins = parse(raw)
        require(sha(read_file(HERE / 'pins.terminal-source-lt09-v1.json')) == self.pins['predecessor_pins_sha256'],
                'historical predecessor pins changed')
        require(self.pins['reader']['namespaceAuthoritySourceSha256'] ==
                self.pins['sources']['app/src-tauri/src/attachment_custody.rs'],
                'namespace authority source identity differs')
        self.schemas = {}
        for path, expected in self.pins['sources'].items():
            require(sha(relative(PROJECT, path)) == expected, 'selected source changed: ' + path)
        for name in ('observed-verification.s1', 'lifecycle-event.s1', 'distribution-closure-transport.s3'):
            schema = parse(relative(PROJECT, 'app/src-tauri/resources/distribution-successor/' + name + '.schema.json'))
            self.schemas[name] = Draft202012Validator(schema, registry=Registry())
        path = PROJECT / 'app/examination/support_identity/canonical.py'
        spec = importlib.util.spec_from_file_location('_s4_canonical', path)
        module = importlib.util.module_from_spec(spec)
        exec(compile(read_file(path), str(path), 'exec'), module.__dict__)
        self.canonical = module.CanonicalSupport()

    def check(self, exchange_path, exchange_sha256, selection_path, selection_sha256):
        digest(exchange_sha256); digest(selection_sha256)
        exchange_path = Path(exchange_path); selection_path = Path(selection_path)
        raw = read_file(exchange_path)
        require(sha(raw) == exchange_sha256, 'exchange digest mismatch')
        exchange = parse(raw)
        exact(exchange, ('format', 'case', 'readback', 'actualLt09', 'members', 'selectedSourceMembers',
                         'producer', 'applicationCandidate'), 'exchange')
        require(exchange['format'] == FORMAT and exchange['case'] in ('selected', 'unselected'), 'unsupported exchange')
        producer = exchange['producer']
        exact(producer, ('sourceRevision', 'harnessExecutableSha256', 'command', 'features', 'kind'), 'producer')
        require(producer['kind'] == 'synthetic-host-test', 'unsupported producer')
        require(isinstance(producer['sourceRevision'], str) and re.fullmatch('[0-9a-f]{40}', producer['sourceRevision']), 'invalid source revision')
        require(producer['sourceRevision'] == self.pins['producer_source_revision'], 'producer source revision differs')
        digest(producer['harnessExecutableSha256'])
        require(isinstance(producer['command'], list) and producer['command']
                and all(isinstance(s, str) and s for s in producer['command']), 'invalid producer command')
        features = producer['features']
        require(isinstance(features, list) and all(isinstance(s, str) and s for s in features)
                and features == sorted(set(features)), 'invalid producer features')
        candidate = exchange['applicationCandidate']
        exact(candidate, ('revision', 'buildIdentity', 'standing'), 'candidate')
        require(candidate['standing'] == 'invented-consumer-fixture'
                and all(isinstance(candidate[k], str) and candidate[k] for k in ('revision', 'buildIdentity')), 'unsupported candidate')
        readback = exchange['readback']
        exact(readback, ('state', 'evidence', 'generation'), 'readback')
        require(readback['state'] == 'read', 'native read unavailable')
        evidence = readback['evidence']
        exact(evidence, ('reference', 'artifact', 'lifecycle', 'transport', 'outcome', 'standing',
                         'readStanding', 'unsupportedEnvelopes'), 'readback evidence')
        require(evidence['outcome'] == 'unverifiable' and evidence['standing'] == 'unverified-development',
                'verified or unsupported standing refused')
        require(evidence['readStanding'] == self.pins['read_standing']
                and evidence['unsupportedEnvelopes'] == self.pins['unsupported_envelopes'], 'read boundary differs')
        ref = evidence['reference']
        exact(ref, ('format', 'publication', 'generation', 'observed', 'lifecycle', 'transport', 'reader'), 'native reference projection')
        require(ref['format'] == 'distribution-s1-reference.s3', 'unsupported reference')
        contained(ref['publication'])
        require(ref['reader'] == self.pins['reader'], 'reader identity differs')
        files = members(exchange_path.parent / 'publication', exchange['members'])
        transport = parse(referenced(files, ref['transport']))
        observation = parse(referenced(files, ref['observed']))
        require(ref['lifecycle'] is not None and evidence['lifecycle'] is not None, 'actual LT09 envelope missing')
        lifecycle = parse(referenced(files, ref['lifecycle']))
        for name, value in [('observed-verification.s1', observation), ('lifecycle-event.s1', lifecycle),
                            ('distribution-closure-transport.s3', transport)]:
            require(not list(self.schemas[name].iter_errors(value)), 'artifact shape differs: ' + name)
        require(transport == evidence['transport'] and observation == evidence['artifact']
                and lifecycle == evidence['lifecycle'], 'readback projection differs from raw bytes')
        exact(transport, ('format', 'method', 'sourceAssociation', 'mirrorLocator', 'generation', 'entries', 'reader', 'limit'), 'transport')
        require(transport['format'] == 'distribution-closure-transport.s3'
                and transport['method'] == 'selected-s1-contract-closure.s3', 'unsupported transport')
        require(transport['reader'] == self.pins['reader'] and transport['limit'] == self.pins['transport_limit'], 'transport reader/boundary differs')
        # Only exported file correspondence is checked here. Native shape, label,
        # inventory, actor, phase and outcome derivation stay in the Host reader.
        require(isinstance(transport['entries'], list), 'invalid transport entries')
        entries = {}
        for entry in transport['entries']:
            referenced(files, entry)
            require(entry['path'] not in entries, 'duplicate transport member')
            entries[entry['path']] = entry['sha256']
        require(entries == {p: sha(b) for p, b in files.items() if p != ref['transport']['path']}, 'transport closure differs')
        require(isinstance(transport['mirrorLocator'], str)
                and transport['mirrorLocator'].endswith('/' + ref['publication']), 'publication locator differs')
        generation = ref['generation']
        exact(generation, ('appSession', 'home', 'spawnCounter'), 'generation')
        require(all(isinstance(generation[k], str) and generation[k] for k in ('appSession', 'home'))
                and type(generation['spawnCounter']) is int and generation['spawnCounter'] >= 1, 'invalid generation')
        require(all(value == generation for value in (readback['generation'], transport['generation'], observation.get('generation'),
                    lifecycle.get('verification_generation'), exchange['actualLt09'].get('generation'))), 'mixed generation')
        require(observation.get('format') == 'observed-verification.s1' and lifecycle.get('format') == 'lifecycle-event.s1', 'mixed artifact versions')
        require(lifecycle.get('verification_artifact') == ref['observed'], 'lifecycle observation reference differs')
        require(lifecycle.get('legacy_event') == exchange['actualLt09']
                and exchange['actualLt09'].get('transitionId') == 'LT-09', 'actual LT09 differs or unsupported envelope')
        require(observation.get('outcome') == 'unverifiable'
                and observation.get('checks', {}).get('custody', {}).get('outcome') != 'pass'
                and exchange['actualLt09'].get('supplierStanding') == 'unverified-development'
                and exchange['actualLt09'].get('verificationResult', {}).get('result') != 'verified', 'verified/custody claim refused')
        require(exchange['actualLt09'].get('versionIdentity', {}).get('declaredPin') == observation.get('pin'),
                'LT09 observation pin differs')
        for check in observation.get('checks', {}).values():
            if check.get('evidence') is not None:
                referenced(files, check['evidence'])
        association = transport['sourceAssociation']
        source_root = exchange_path.parent / 'selected-source'
        if exchange['case'] == 'unselected':
            require(association is None and exchange['selectedSourceMembers'] is None
                    and not os.path.lexists(source_root), 'unselected source association differs')
            require(observation.get('expected_reference') is None and observation.get('adoption_attestation') is None,
                    'nonnull reference without selected source')
            require(all(p.startswith('.chirality-s1/') for p in files), 'unexpected unselected member')
        else:
            exact(association, ('method', 'originalSource', 'compiledAnchor', 'expectedReference', 'adoptionAttestation'), 'source association')
            require(association['method'] == 'selected-s1-contract-closure.s3', 'unsupported source association')
            require(isinstance(association['originalSource'], str) and association['originalSource']
                    and association['originalSource'] != transport['mirrorLocator'], 'source/mirror locator differs')
            source = members(source_root, exchange['selectedSourceMembers'])
            require(source == {p: b for p, b in files.items() if not p.startswith('.chirality-s1/')}, 'selected source/mirror bytes differ')
            anchor = parse(referenced(source, association['compiledAnchor']))
            require(anchor.get('format') == 'build-selection.s2'
                    and anchor.get('expected') == association['expectedReference']
                    and anchor.get('attestation') == association['adoptionAttestation'], 'selection anchor refs differ')
            expected = parse(referenced(source, association['expectedReference']))
            attestation = parse(referenced(source, association['adoptionAttestation']))
            # Follow only the explicitly declared closure edges. Opaque evidence
            # content, native review/selection semantics and authority stay outside.
            declared = {association[k]['path'] for k in ('compiledAnchor', 'expectedReference', 'adoptionAttestation')}
            for value, paths in [(expected, ('label_evidence', 'generation_correspondence', 'generated/provenance',
                                            'generated/version_advance', 'archive/acquisition_authorization',
                                            'archive/custody', 'archive/extraction_procedure')),
                                 (attestation, ('review_evidence', 'adoption/through_help_human', 'adoption/evidence'))]:
                for path in paths:
                    artifact = value
                    for part in path.split('/'):
                        require(isinstance(artifact, dict) and part in artifact, 'declared closure reference missing')
                        artifact = artifact[part]
                    referenced(source, artifact); declared.add(artifact['path'])
            require(declared == set(source), 'declared selected closure differs')
            require(observation.get('expected_reference') == association['expectedReference']
                    and observation.get('adoption_attestation') == association['adoptionAttestation'], 'selected observation refs differ')
        selected_raw = read_file(selection_path)
        require(sha(selected_raw) == selection_sha256, 'support selection digest mismatch')
        selected = parse(selected_raw)
        # Snapshot each original record/binding with no-follow reads before the
        # unchanged canonical engine reads them; do not mint any record sidecar.
        with tempfile.TemporaryDirectory(prefix='chirality-s4-records-') as temp:
            root = Path(temp); seen = set()
            for pair in selected['artifacts'].values():
                for reference in pair.values():
                    name = reference['path']; contained(name)
                    require(name not in seen and name != 'selection.json', 'duplicate support path')
                    seen.add(name); payload = relative(selection_path.parent, name)
                    target = root / name; target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(payload)
            (root / 'selection.json').write_bytes(selected_raw)
            report = self.canonical.check(root / 'selection.json', selection_sha256)
        require(report['canonical_consistency_passed'], 'canonical support join refused: ' + json.dumps(report['errors']))
        package = selected['package_selection']
        require(package['revision'] == candidate['revision'] and package['build'] == candidate['buildIdentity'], 'application candidate/support join differs')
        require(package['pin'] == observation.get('pin'), 'supplier pin/support join differs')
        return {'file_correspondence_passed': True, 'exchange_sha256': exchange_sha256,
                'selection_sha256': selection_sha256, 'receiving_adoption': self.pins['adoption'], 'case': exchange['case'], 'producer': producer,
                'application_candidate': candidate, 'reader': ref['reader'], 'generation': generation,
                'canonical_support': report, 'native_reference_authority': False,
                'terminal_evidence_received': False, 'terminal_authority_authenticated': False,
                'namespace_authority_authenticated': False, 'semantic_reader_reexecuted': False, 'producer_history_authenticated': False,
                'application_build_authenticated': False, 'qualification_established': False, 'limits': LIMITS}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('exchange'); parser.add_argument('--exchange-sha256', required=True)
    parser.add_argument('--selection', required=True); parser.add_argument('--selection-sha256', required=True)
    args = parser.parse_args(argv)
    try:
        report = Receiver().check(args.exchange, args.exchange_sha256, args.selection, args.selection_sha256)
        print(json.dumps(report, indent=2)); return 0
    except (OSError, ValueError, TypeError, KeyError, AttributeError, subprocess.TimeoutExpired) as error:
        print(json.dumps({'file_correspondence_passed': False, 'input_error': str(error),
                          'native_reference_authority': False, 'terminal_evidence_received': False, 'terminal_authority_authenticated': False,
                'namespace_authority_authenticated': False, 'semantic_reader_reexecuted': False,
                          'producer_history_authenticated': False, 'application_build_authenticated': False,
                          'qualification_established': False,
                          'limits': LIMITS}, indent=2)); return 2


if __name__ == '__main__':
    sys.exit(main())
