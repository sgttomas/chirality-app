"""Frozen-input S1 support. Never produces runtime verification or qualification."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import tempfile
from jsonschema.exceptions import ValidationError

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'AGENTS.md').is_file())
LIMIT = 512 * 1024 * 1024


def require(value, message):
    if not value:
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
    def constant(value):
        raise ValueError('non-finite JSON value: ' + value)
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)


def exact(value, fields, label):
    require(isinstance(value, dict) and set(value) == set(fields), 'unknown/missing ' + label + ' fields')


def relative(value):
    require(isinstance(value, str) and value and not value.startswith('/')
            and not any(c in value for c in '\\\x00\n\r')
            and all(p not in ('', '.', '..') for p in value.split('/')), 'noncontained artifact path')
    return value


def ref(value):
    exact(value, ('path', 'sha256'), 'artifact reference')
    relative(value['path'])
    require(isinstance(value['sha256'], str) and re.fullmatch('[0-9a-f]{64}', value['sha256']), 'invalid artifact digest')
    return value


def transfer(path, destination=None, retain=False):
    """Stream a bounded no-follow regular file, checking descriptor stability."""
    path = Path(path)
    require(path.is_absolute() and '..' not in path.parts, 'absolute physical file path required')
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in path.parts[1:-1]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd); fd = child
        child = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
        writer = None
        try:
            before = os.fstat(child)
            limit = 32 * 1024 * 1024 if retain else LIMIT
            require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and before.st_size <= limit,
                    'unsupported linked/special file or explicit size bound exceeded')
            if destination is not None:
                destination.parent.mkdir(parents=True, exist_ok=True)
                writer = destination.open('wb')
            digest, chunks, size = hashlib.sha256(), [], 0
            while True:
                chunk = os.read(child, 1024 * 1024)
                if not chunk: break
                size += len(chunk)
                require(size <= limit, 'explicit file byte limit exceeded')
                digest.update(chunk)
                if writer: writer.write(chunk)
                if retain: chunks.append(chunk)
            after = os.fstat(child)
            stamp = lambda v: (v.st_dev, v.st_ino, v.st_mode, v.st_size, v.st_mtime_ns, v.st_ctime_ns)
            require(stamp(before) == stamp(after), 'input changed during read')
            return (b''.join(chunks) if retain else None), digest.hexdigest(), size
        finally:
            if writer: writer.close()
            os.close(child)
    finally:
        os.close(fd)


class Frozen:
    def __init__(self, destination):
        self.destination = destination
        self.originals = {}
        self.artifacts = {}
        self.missing = set()
        self.total = 0

    def file(self, original, destination, retain=True):
        original = Path(original)
        raw, digest, size = transfer(original, destination, retain)
        require(original not in self.originals or self.originals[original] == digest, 'source changed during capture')
        self.originals[original] = digest
        self.total += size
        require(self.total <= 1024 * 1024 * 1024, 'snapshot total byte limit')
        return raw if retain else digest

    def artifact(self, reference, source):
        ref(reference)
        name, digest = reference['path'], reference['sha256']
        if name in self.artifacts:
            require(self.artifacts[name] == digest, 'conflicting artifact reference digest: ' + name)
            return
        self.artifacts[name] = digest
        try:
            digest_read = self.file(source / name, self.destination / name, retain=False)
        except FileNotFoundError:
            self.missing.add(source / name)
            return
        require(digest_read == digest, 'artifact exact-byte mismatch: ' + name)

    def recheck(self):
        for path, digest in self.originals.items():
            require(transfer(path)[1] == digest, 'stale original input/source/scanner: ' + str(path))
        for path in self.missing:
            try: transfer(path)
            except FileNotFoundError: continue
            raise ValueError('missing artifact changed during check: ' + str(path))


def source_model(frozen, scratch):
    raw = frozen.file(HERE / 'sources.json', scratch / 'source-pins.json')
    pins = parse(raw)
    exact(pins, ('format', 'basis_revision', 'model', 'sources'), 'source manifest')
    require(pins['format'] == 'static-distribution-sources/1', 'unknown source manifest version')
    relative(pins['model'])
    require(pins['model'] in pins['sources'], 'model must be a guarded frozen source')
    for name, digest in pins['sources'].items():
        relative(name)
        actual = frozen.file(ROOT / name, scratch / 'source' / name)
        require(sha(actual) == digest, 'canonical static source changed: ' + name)
    (scratch / 'source/AGENTS.md').write_text('Frozen value-model source root marker.\n')
    spec = importlib.util.spec_from_file_location('static_s1_value_model', scratch / 'source' / pins['model'])
    model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)
    return model, sha(raw)


def check(*args, **kwargs):
    try:
        return _check(*args, **kwargs)
    except ValidationError as error:
        raise ValueError('selected value schema refused: ' + error.message) from error


def _check(request_path, scanner_path, published_tree=None, packaged_tree=None):
    require(published_tree is not None or packaged_tree is not None, 'at least one actual tree required')
    request_path, scanner_path = Path(request_path), Path(scanner_path)
    with tempfile.TemporaryDirectory(prefix='chirality-static-distribution-') as tmp:
        scratch = Path(tmp).resolve()
        artifacts = scratch / 'artifacts'
        frozen = Frozen(artifacts)
        model, source_digest = source_model(frozen, scratch)
        request_raw = frozen.file(request_path, scratch / 'request.json')
        request = parse(request_raw)
        exact(request, ('format', 'build_selection', 's1_package', 'legacy_package', 'terms', 'candidate', 'installer', 'scanner'), 'request')
        require(request['format'] == 'static-distribution-input/1', 'unknown static distribution input version')
        exact(request['scanner'], ('sha256', 'declared_source_revision'), 'scanner selection')
        require(isinstance(request['scanner']['declared_source_revision'], str) and request['scanner']['declared_source_revision'].strip(), 'scanner declared source required')
        scanner_digest = frozen.file(scanner_path, scratch / 'scanner', retain=False)
        require(scanner_digest == request['scanner']['sha256'], 'selected scanner byte digest mismatch')
        (scratch / 'scanner').chmod(0o500)
        for key in ('build_selection', 's1_package', 'legacy_package', 'terms', 'candidate', 'installer'):
            frozen.artifact(request[key], request_path.parent)

        def get(reference):
            ref(reference)
            require((artifacts / reference['path']).stat().st_size <= 32 * 1024 * 1024, 'typed JSON artifact exceeds 32 MiB')
            return model.resolve(reference, artifacts, None)

        def value(key):
            return parse(get(request[key]))

        selection, package, legacy, terms, candidate = [value(k) for k in ('build_selection', 's1_package', 'legacy_package', 'terms', 'candidate')]
        exact(selection, ('format', 'method', 'schema_ids', 'expected', 'attestation'), 'build selection')
        require(selection['format'] == 'build-selection.s2' and selection['method'] == 'codex-vendor-tree-v1'
                and selection['schema_ids'] == ['expected-reference.s1', 'adoption-attestation.s1'], 'unknown build selection cohort')
        model.shape(package, 'pkg-identity.s1')
        require(package['verification_artifact'] is None, 'runtime observation outside static packaging scope')
        # Follow only contract-owned artifact edges. Evidence is opaque bytes;
        # incidental JSON keys inside it are never dependency declarations.
        ref(selection['expected']); ref(selection['attestation'])
        typed = [(selection['expected'], 'expected-reference.s1'),
                 (selection['attestation'], 'adoption-attestation.s1'),
                 (package['expected_reference'], 'expected-reference.s1'),
                 (package['adoption_attestation'], 'adoption-attestation.s1'),
                 (package['published_inventory'], 'inventory-artifact.s1'),
                 (package['packaged_inventory'], 'inventory-artifact.s1')]
        for reference, schema in typed:
            if reference is None: continue
            frozen.artifact(reference, request_path.parent)
            try: body = parse(get(reference))
            except FileNotFoundError: continue
            model.shape(body, schema)
            evidence = []
            if schema == 'expected-reference.s1':
                evidence = [body['label_evidence'], body['generation_correspondence'],
                            body['generated']['provenance'], body['generated']['version_advance']]
                evidence += [body['archive'][key] for key in ('acquisition_authorization', 'custody', 'extraction_procedure')]
            elif schema == 'adoption-attestation.s1':
                evidence = [body['review_evidence'], body['adoption']['through_help_human'], body['adoption']['evidence']]
            for item in evidence: frozen.artifact(item, request_path.parent)
        model.legacy_pkg.Draft202012Validator(model.legacy_pkg.load('pkg.identity-record.schema.json')).validate(legacy)
        model.legacy_pkg.Draft202012Validator(model.legacy_pkg.load('pkg.terms-record.schema.json')).validate(terms)
        exact(candidate, ('app_revision', 'build_identity', 'package_record_id', 'installer_sha256_before_notarisation'), 'candidate')
        mismatches, blockers = [], ['No trusted compiled App selection anchor, signature/build integrity or installed custody established.',
            'No supplier probe, version-label observation, runtime verification, native package checks or qualification performed.',
            'No App binary-content authentication: legacy PKG has no App-binary digest.']
        if terms['state'] == 'unresolved':
            blockers.append('Selected terms obligation remains unresolved; PK-R4 value checks do not settle it.')
        checks = {}
        def same(label, left, right):
            checks[label] = left == right
            if left != right: mismatches.append(label)
        same('selected legacy PKG value', package['legacy_package'], legacy)
        same('selected reference', package['expected_reference'], selection['expected'])
        same('selected attestation', package['adoption_attestation'], selection['attestation'])
        actual_candidate = {'app_revision': legacy['app']['revision'], 'build_identity': legacy['app']['build_identity'],
                            'package_record_id': legacy['record_id'], 'installer_sha256_before_notarisation': legacy['app']['installer']['sha256_before_notarisation']}
        same('candidate identity', candidate, actual_candidate)
        same('installer exact bytes', transfer(artifacts / request['installer']['path'])[1], candidate['installer_sha256_before_notarisation'])
        for label, violations in [('legacy PKG duties', model.legacy_pkg.identity_violations(legacy)), ('terms PK-R4', model.legacy_pkg.terms_violations(terms))]:
            checks[label] = not violations
            if violations: mismatches.append(label + ': ' + ','.join(violations))

        expected = None
        incomplete_comparison = bool(frozen.missing)
        try:
            expected = parse(get(selection['expected']))
            model.shape(expected, 'expected-reference.s1')
            require(not model.inventory.validate(expected['inventory']), 'invalid selected expected inventory')
            same('reference pin', expected['pin'], legacy['codex']['pin'])
            same('reference platform', expected['platform'], legacy['app']['target'])
        except FileNotFoundError:
            blockers.append('Selected expected reference missing.')
            incomplete_comparison = True
        try:
            # This selected-digest argument is a value-check seam, never trust.
            model.reference(selection['expected'], selection['attestation'], artifacts, selection['attestation']['sha256'])
            checks['reference closure values'] = True
        except OSError as error:
            checks['reference closure values'] = False
            blockers.append('Reference closure unavailable: ' + str(error))
        except ValueError as error:
            checks['reference closure values'] = False
            mismatches.append('Reference closure values: ' + str(error))
        try:
            model.package(package, artifacts, selection['attestation']['sha256'])
            checks['S1 package values'] = True
        except OSError as error:
            checks['S1 package values'] = False
            blockers.append('S1 package values unavailable: ' + str(error))
        except ValueError as error:
            checks['S1 package values'] = False
            if 'derived unverifiable' in str(error):
                blockers.append('S1 package declared status lacks available closure; no observed status inferred.')
            else:
                mismatches.append('S1 package values: ' + str(error))

        def scanner(*args):
            result = subprocess.run([str(scratch / 'scanner'), *map(str, args)], capture_output=True, timeout=120, check=False)
            require(result.returncode == 0, 'static scanner refused: ' + result.stderr.decode('utf-8', 'replace')[:1000])
            return parse(result.stdout)

        def equal(left, right):
            a, b = scratch / 'compare-left.json', scratch / 'compare-right.json'
            a.write_text(json.dumps(left)); b.write_text(json.dumps(right))
            result = scanner('compare', a, b)
            exact(result, ('equal',), 'scanner comparison')
            require(type(result['equal']) is bool, 'invalid scanner equality result')
            return result['equal']

        measurements = {}
        for side, tree in [('published', published_tree), ('packaged', packaged_tree)]:
            if tree is None:
                measurements[side] = {'state': 'unmeasured'}
                blockers.append(side + ' tree not measured; selected artifact is a value claim only.')
                incomplete_comparison = True
                continue
            inventory = scanner('scan', tree)
            require(not model.inventory.validate(inventory), 'scanner returned invalid complete inventory')
            measurements[side] = {'state': 'measured', 'inventory': inventory}
            reference = package[side + '_inventory']
            if reference is None:
                blockers.append(side + ' inventory artifact not selected; measured facts retained without that comparison.')
                incomplete_comparison = True
            else:
                try:
                    claimed = parse(get(reference))
                    model.shape(claimed, 'inventory-artifact.s1')
                    require(not model.inventory.validate(claimed['inventory']), 'invalid selected ' + side + ' inventory')
                    same(side + ' selected complete inventory', equal(claimed['inventory'], inventory), True)
                except FileNotFoundError:
                    blockers.append(side + ' inventory artifact missing.')
                    incomplete_comparison = True
            if expected is not None:
                same(side + ' reference complete inventory', equal(expected['inventory'], inventory), True)
            summary = legacy['codex'][side]
            same(side + ' legacy manifest', inventory['manifest_sha256'], summary['manifest_sha256'])
            same(side + ' legacy file count', sum(e['kind'] == 'file' for e in inventory['entries']), summary['files'])
            files = {e['path']: e for e in inventory['entries'] if e['kind'] == 'file'}
            for executable in legacy['codex']['executables']:
                same(side + ' executable ' + executable['path'], files.get(executable['path'], {}).get('sha256'), executable['sha256_' + side])
        if all(v['state'] == 'measured' for v in measurements.values()):
            same('actual published/packaged complete inventories', equal(measurements['published']['inventory'], measurements['packaged']['inventory']), True)
        for side, tree in [('published', published_tree), ('packaged', packaged_tree)]:
            if tree is not None:
                require(equal(measurements[side]['inventory'], scanner('scan', tree)), 'tree changed during static check: ' + side)
        frozen.recheck()
        return {'format': 'chirality.static-distribution-support/1', 'standing': 'development-unverifiable',
            'comparison': 'mismatch' if mismatches else 'incomplete' if incomplete_comparison else 'consistent', 'mismatches': mismatches, 'blockers': blockers,
            'value_checks': checks, 'measurements': measurements, 'candidate': candidate,
            'selected_terms_state': terms['state'],
            'selected_request_sha256': sha(request_raw), 'selected_artifacts': frozen.artifacts,
            'source_manifest_sha256': source_digest,
            'scanner': {'sha256': scanner_digest, 'declared_source_revision': request['scanner']['declared_source_revision'],
                        'contract': 'distribution_preflight::scan/equal; complete Inventory JSON',
                        'standing': 'operator-selected executable bytes; source/build provenance not authenticated'},
            'limits': ['Canonical Design model checks frozen values only; no reviewer/adoption authority authenticated.',
                       'Legacy signing/notary/terms/Mach-O coverage statements remain selected claims, not newly observed facts.',
                       'No S1 observed verification, lifecycle event, selected-store state or production trust created.',
                       'Checks detect changed inputs at recheck, not hostile changes after the report.']}
