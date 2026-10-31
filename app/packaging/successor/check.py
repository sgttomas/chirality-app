"""Versioned static package/S4 evidence joins; no execution or live authority."""
import argparse
import importlib.util
import json
import re
from pathlib import Path, PurePosixPath
import tempfile

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parents[3]
WORK = 'execution/PKG-01/DEL-01-06/Work/package-successor-v1'


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


legacy = module('package_static_legacy', 'app/packaging/static_distribution/check.py')
terms = module('package_terms_v1', 'app/packaging/terms/check.py')
sha, parse, require = legacy.sha, legacy.parse, legacy.require


def source_dependencies():
    """Complete maintained offline code/schema closure; no fixture or scanner."""
    paths = {'AGENTS.md', 'app/packaging/successor/check.py',
             'app/packaging/static_distribution/check.py', 'app/packaging/static_distribution/sources.json',
             'app/packaging/terms/check.py', 'execution/PKG-01/DEL-01-06/Work/terms-position-v1/schema.json',
             WORK + '/static-package-input.v2.schema.json', WORK + '/packaged-s4-binding.v1.schema.json',
             'app/src-tauri/src/installed_custody.rs', 'app/src-tauri/build.rs',
             'app/src-tauri/Cargo.toml', 'app/src-tauri/Cargo.lock',
             'app/src-tauri/build_support/publisher_selection.rs',
             'app/src-tauri/build_support/developer-id-application.s1.requirement-template.txt'}
    paths.update('app/src-tauri/schemas/publisher-build-' + name + '.s1.schema.json'
                 for name in ('selection', 'binding', 'public-projection'))
    paths.update('app/src-tauri/resources/distribution-successor/' + name + '.schema.json'
                 for name in ('observed-verification.s4', 'installed-custody-observation.s4', 'distribution-preflight-facts.s3'))
    pins = parse(legacy.transfer(ROOT / 'app/packaging/static_distribution/sources.json', retain=True)[0])
    paths.update(legacy.deliverable_path(ROOT, path) for path in pins['sources'])
    return {path: legacy.transfer(ROOT / path)[1] for path in sorted(paths)}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


class Context:
    def __init__(self, root, scratch):
        self.root, self.scratch = root, scratch
        self.frozen = legacy.Frozen(scratch / 'artifacts')
        self.errors, self.missing = [], []
        self.source_dependencies = {}
        self.model, _ = legacy.source_model(self.frozen, scratch)
        for path, digest in source_dependencies().items():
            require(sha(self.source(path)) == digest, 'source changed during reader capture')

    def source(self, path):
        raw = self.frozen.file(ROOT / path, self.scratch / 'reader' / path)
        self.source_dependencies[path] = sha(raw)
        return raw

    def shape(self, value, path):
        try:
            Draft202012Validator(parse(self.source(path))).validate(value)
        except ValidationError as error:
            raise ValueError('schema refusal: ' + path + ' / ' + '/'.join(map(str, error.path))) from error

    def get(self, reference, typed=True):
        self.frozen.artifact(reference, self.root)
        path = self.frozen.destination / reference['path']
        if not path.exists():
            self.missing.append('artifact:' + reference['path'])
            return None
        if not typed:
            return reference['sha256']
        require(path.stat().st_size <= 2 * 1024 * 1024, 'typed artifact exceeds 2 MiB')
        return parse(path.read_bytes())

    def raw(self, reference):
        if self.get(reference, typed=False) is None:
            return None
        path = self.frozen.destination / reference['path']
        require(path.stat().st_size <= 2 * 1024 * 1024, 'typed artifact exceeds 2 MiB')
        return path.read_bytes()

    def same(self, label, a, b):
        if a != b:
            self.errors.append(label)

    def term_account(self, reference):
        record = self.get(reference)
        if record is None:
            return
        terms.validate(record, parse(self.source(str(terms.SCHEMA.relative_to(ROOT)))))
        position, owner = record['position'], record['owner_disposition']
        if position:
            self.get(position['content'])
        if owner:
            approval = self.get(owner['approval'])
            if approval:
                terms.validate(approval, parse(terms.SCHEMA.read_bytes()), 'approval')
                self.get(approval['approved_proposal']['artifact'], typed=False)
                self.get(approval['owner_answer'])
        if record['distribution_decision'] != 'not_made':
            release = self.get(record['distribution_decision']['evidence'])
            if release:
                terms.validate(release, parse(terms.SCHEMA.read_bytes()), 'release')
                self.get(release['owner_answer'])
        try:
            result = terms.check(reference['path'], self.frozen.destination)
            if result['recorded_state'] != 'applicable_position_retained':
                self.missing.append('applicable terms position')
        except FileNotFoundError:
            self.missing.append('terms evidence closure')

    def static(self, request):
        self.shape(request, WORK + '/static-package-input.v2.schema.json')
        values = {k: self.get(request[k]) for k in ('build_selection', 's1_package', 'legacy_package')}
        self.get(request['installer'], typed=False)
        self.term_account(request['terms'])
        if any(v is None for v in values.values()):
            return None
        selection, package, old = (values[k] for k in ('build_selection', 's1_package', 'legacy_package'))
        legacy.exact(selection, ('format', 'method', 'schema_ids', 'expected', 'attestation'), 'supplier selection')
        require(selection['format'] == 'build-selection.s2' and selection['method'] == 'codex-vendor-tree-v1'
                and selection['schema_ids'] == ['expected-reference.s1', 'adoption-attestation.s1'], 'unsupported supplier selection')
        self.model.shape(package, 'pkg-identity.s1')
        require(package['verification_artifact'] is None, 'static S1 verification_artifact must remain null')
        self.model.legacy_pkg.Draft202012Validator(self.model.legacy_pkg.load('pkg.identity-record.schema.json')).validate(old)
        self.same('embedded legacy package', package['legacy_package'], old)
        self.same('static expected reference', package['expected_reference'], selection['expected'])
        self.same('static attestation', package['adoption_attestation'], selection['attestation'])
        self.same('static candidate', request['candidate'], {'revision': old['app']['revision'],
                  'build_identity': old['app']['build_identity'], 'codex_pin': old['codex']['pin'], 'package_record_id': old['record_id']})
        self.same('pre-notary installer digest', request['installer']['sha256'], old['app']['installer']['sha256_before_notarisation'])
        for key in ('published_inventory', 'packaged_inventory'):
            if package[key] is not None:
                self.get(package[key])
            else:
                self.missing.append(key)
        expected = self.get(selection['expected'])
        attestation = self.get(selection['attestation'])
        if expected:
            self.model.shape(expected, 'expected-reference.s1')
            for edge in [expected['label_evidence'], expected['generation_correspondence'],
                         expected['generated']['provenance'], expected['generated']['version_advance'],
                         *[expected['archive'][k] for k in ('acquisition_authorization', 'custody', 'extraction_procedure')]]:
                self.get(edge, typed=False)
        if attestation:
            self.model.shape(attestation, 'adoption-attestation.s1')
            for edge in (attestation['review_evidence'], attestation['adoption']['through_help_human'], attestation['adoption']['evidence']):
                self.get(edge, typed=False)
        violations = self.model.legacy_pkg.identity_violations(old)
        if violations:
            self.errors.append('legacy package rules: ' + ','.join(violations))
        try:
            self.model.reference(selection['expected'], selection['attestation'], self.frozen.destination, selection['attestation']['sha256'])
            self.model.package(package, self.frozen.destination, selection['attestation']['sha256'])
        except FileNotFoundError:
            self.missing.append('static supplier closure')
        except ValueError as error:
            self.errors.append('static supplier values: ' + str(error))
        return old, package, selection, expected

    def publisher(self, request, trust):
        values = {k: self.get(request[k]) for k in ('publisher_binding', 'publisher_projection', 'publisher_input', 'tauri_config')}
        requirement = self.raw(request['publisher_requirement'])
        if trust is None:
            self.missing.append('independently selected publisher binding digest')
        else:
            require(isinstance(trust, str) and __import__('re').fullmatch('[0-9a-f]{64}', trust), 'invalid trusted publisher digest')
            self.same('trusted publisher digest', trust, request['publisher_binding']['sha256'])
        if any(v is None for v in values.values()) or requirement is None:
            return None
        binding, projection, selected, config = (values[k] for k in ('publisher_binding', 'publisher_projection', 'publisher_input', 'tauri_config'))
        for value, name in ((binding, 'binding'), (projection, 'public-projection'), (selected, 'selection')):
            self.shape(value, 'app/src-tauri/schemas/publisher-build-' + name + '.s1.schema.json')
        self.same('publisher input digest', binding['input_sha256'], request['publisher_input']['sha256'])
        for key in ('production_bundle_identifier', 'developer_id_team_identifier'):
            self.same('publisher selected ' + key, selected[key], binding[key])
        recipes = {'template_sha256': 'build_support/developer-id-application.s1.requirement-template.txt',
                   'generator_sha256': 'build_support/publisher_selection.rs', 'recipe_sha256': 'build.rs',
                   'input_schema_sha256': 'schemas/publisher-build-selection.s1.schema.json',
                   'binding_schema_sha256': 'schemas/publisher-build-binding.s1.schema.json',
                   'public_projection_schema_sha256': 'schemas/publisher-build-public-projection.s1.schema.json',
                   'cargo_manifest_sha256': 'Cargo.toml', 'cargo_lock_sha256': 'Cargo.lock'}
        for key, path in recipes.items():
            self.same('publisher recipe ' + key, binding[key], sha(self.source('app/src-tauri/' + path)))
        template = self.source('app/src-tauri/' + recipes['template_sha256']).decode()
        for key in ('production_bundle_identifier', 'developer_id_team_identifier'):
            template = template.replace('{{' + key + '}}', json.dumps(binding[key], ensure_ascii=False))
        self.same('independent publisher requirement', requirement, template.encode())
        self.same('requirement digest', binding['requirement_sha256'], sha(requirement))
        context = binding['build_context']
        self.same('publisher build context digest', binding['build_context_sha256'], sha(canonical(context)))
        self.same('effective Tauri config digest', context['tauri_config_sha256'], sha(canonical(config)))
        self.same('effective identifier', context['application_identifier'], config.get('identifier'))
        self.same('effective version', context['application_version'], config.get('version'))
        self.same('selected effective identifier', binding['production_bundle_identifier'], context['application_identifier'])
        self.same('projection original digest', projection['original_binding_sha256'], request['publisher_binding']['sha256'])
        for key in binding:
            if key.endswith('_sha256'):
                self.same('projection ' + key, projection.get(key), binding[key])
        return binding

    def binding(self, request, trust):
        self.shape(request, WORK + '/packaged-s4-binding.v1.schema.json')
        static_request = self.get(request['static_package'])
        static = self.static(static_request) if static_request is not None else None
        publisher = self.publisher(request, trust)
        observation, custody = self.get(request['observation']), self.get(request['custody'])
        self.get(request['app']['executable'], typed=False)
        self.get(request['installer_after_stapling'], typed=False)
        if static_request:
            self.same('binding/static candidate', request['candidate'], static_request['candidate'])
        if static is None or publisher is None or observation is None or custody is None:
            return
        old, package, selection, expected = static
        if not old['complete']:
            self.missing.append('complete package content')
        if old['signing']['option'] != 'B_supplier_signatures_kept':
            self.missing.append('selected Option B or separately adopted fallback')
        for key in ('fp0', 'fp1a', 'fp1b', 'fp3'):
            if old.get('first_package_checks', {}).get(key, {}).get('outcome') != 'pass':
                self.missing.append('reported package ' + key + ' pass')
        if old['notarisation']['state'] != 'accepted' or not old['notarisation'].get('stapled'):
            self.missing.append('reported accepted/stapled notarisation')
        app = request['app']
        for a, b in [('revision', 'revision'), ('build_identity', 'build_identity'), ('version', 'version'), ('identifier', 'bundle_id'), ('cdhash', 'cdhash')]:
            self.same('App/' + a, app[a], old['app'].get(b))
        self.same('App publisher binding', app['publisher_binding_sha256'], request['publisher_binding']['sha256'])
        self.same('App publisher projection', app['public_projection_sha256'], request['publisher_projection']['sha256'])
        self.same('App supplier selection', app['supplier_selection_sha256'], static_request['build_selection']['sha256'])
        self.same('App publisher identifier', app['identifier'], publisher['production_bundle_identifier'])
        self.same('App publisher version', app['version'], publisher['build_context']['application_version'])
        self.same('post-staple installer digest', request['installer_after_stapling']['sha256'], old['app']['installer'].get('sha256_after_staple'))
        self.s4(request, observation, custody, selection, expected, old, publisher)

    def s4(self, request, observation, custody, selection, expected, old, publisher):
        for value, name in ((observation, 'observed-verification.s4'), (custody, 'installed-custody-observation.s4')):
            self.shape(value, 'app/src-tauri/resources/distribution-successor/' + name + '.schema.json')
        self.same('S4 custody reference', observation['checks']['custody']['evidence'], request['custody'])
        self.same('S4 generation', custody['generation'], observation['generation'])
        self.same('S4 full inventory', custody['inventory'], observation['inventory'])
        self.same('S4 selection association', custody['selection'], request['supplier_selection'])
        association = request['supplier_selection']
        self.same('S4 selection anchor', association['compiledAnchor'], self.get(request['static_package'])['build_selection'])
        self.same('S4 selected reference', association['expectedReference'], selection['expected'])
        self.same('S4 selected attestation', association['adoptionAttestation'], selection['attestation'])
        for key, ref in [('expected_reference', 'expected'), ('adoption_attestation', 'attestation')]:
            self.same('observed ' + key, observation[key], selection[ref])
        # Runtime may leave candidate_subject null; the separate binding supplies
        # the package identity. A supplied subject must agree, never be ignored.
        if observation['candidate_subject'] is not None:
            self.same('optional runtime candidate', observation['candidate_subject'],
                      {'app_revision': old['app']['revision'], 'build_identity': old['app']['build_identity'],
                       'package_record_id': old['record_id'], 'installer_sha256_before_notarisation': old['app']['installer']['sha256_before_notarisation']})
        require(not self.model.inventory.validate(observation['inventory']), 'invalid S4 inventory')
        if expected:
            for key in ('pin', 'platform', 'generated', 'launcher', 'inventory'):
                self.same('S4 expected ' + key, observation[key], expected[key])
        for name, check in observation['checks'].items():
            if check['outcome'] == 'mismatch':
                self.errors.append('S4 ' + name + ' mismatch')
            elif check['outcome'] != 'pass':
                self.missing.append('S4 ' + name + ' pass')
            if check['evidence'] is None:
                self.missing.append('S4 ' + name + ' evidence')
            elif name != 'custody':
                facts = self.get(check['evidence'])
                if facts:
                    self.shape(facts, 'app/src-tauri/resources/distribution-successor/distribution-preflight-facts.s3.schema.json')
                    for key in ('generation', 'inventory', 'raw_version_label', 'configuration'):
                        self.same('preflight ' + key, facts[key], observation[key])
        self.same('S4 recorded outcome', observation['outcome'], 'verified')
        if any(c['outcome'] != 'pass' or c['evidence'] is None for c in observation['checks'].values()):
            self.errors.append('verified S4 claim lacks all passing checks/evidence')
        self.same('S4 pre-spawn phase', observation['phase'], 'pre-spawn')
        self.same('S4 observed label', observation['observed_label'], observation['pin'])
        self.same('S4 raw label', observation['raw_version_label'].removesuffix('\n') if observation['raw_version_label'] else None, 'codex-cli ' + observation['pin'])
        actual = custody['app']
        installed_source = self.source('app/src-tauri/src/installed_custody.rs').decode()
        limits_block = re.search(r'const LIMITS:.*?= \[(.*?)\];', installed_source, re.S)
        require(limits_block is not None, 'unsupported installed observer limits source')
        expected_limits = [json.loads(s) for s in re.findall(r'"(?:[^"\\]|\\.)*"', limits_block[1])]
        self.same('S4 residual limits', actual['limits'], expected_limits)
        self.same('S4 envelope limits', custody['limits'], ['No live authority from serialized evidence',
                  'No package, installer, quarantine or notarization qualification'])
        self.same('S4 installed standing', actual['standing'], 'installed-observation')
        self.same('S4 publisher requirement', actual['requirement_sha256'], publisher['requirement_sha256'])
        self.same('S4 static/dynamic facts', actual['static'], actual['dynamic'])
        signing = actual['static']
        self.same('S4 signing identifier', signing['identifier'], publisher['production_bundle_identifier'])
        self.same('S4 signing team', signing['team_identifier'], publisher['developer_id_team_identifier'])
        self.same('S4 package signing team', signing['team_identifier'], old['app']['signature'].get('team'))
        self.same('S4 signing cdhash', signing['cdhash'], request['app']['cdhash'])
        if signing['signature_flags'] & 2 or not signing['signature_flags'] & 0x10000:
            self.errors.append('S4 ad-hoc or unhardened signature')
        loc, config = actual['location'], observation['configuration']
        bundle = PurePosixPath(loc['bundle'])
        require(bundle.is_absolute() and bundle.suffix == '.app'
                and not any(p in ('.', '..') for p in loc['bundle'].split('/')),
                'invalid installed bundle location')
        self.same('installed parent', str(bundle.parent), loc['parent'])
        self.same('installed resources', str(bundle / 'Contents/Resources'), loc['resources'])
        self.same('installed executable parent', str(PurePosixPath(loc['executable']).parent), str(bundle / 'Contents/MacOS'))
        self.same('translocation indicator', 'AppTranslocation' in bundle.parts, loc['app_translocation_path_component'])
        self.same('supplier resource root', config['resolved_root'], loc['resources'] + '/codex')
        self.same('supplier executable', config['resolved_executable'], config['resolved_root'] + '/bin/codex')
        self.same('supplier path', config['path_prefix'], config['resolved_root'] + '/codex-path')
        if config['probe_home'] == config['account_home']:
            self.errors.append('probe/account home collision')
        for name in observation['launcher']['removed_wrapper_variables']:
            if name not in config['removed_environment_names']:
                self.errors.append('wrapper environment not removed: ' + name)


def check(request_path, *, evidence_root=None, trusted_publisher_sha256=None):
    """All artifact refs are relative to one selected root, including nested refs."""
    request_path = Path(request_path).absolute()
    root = Path(evidence_root).absolute() if evidence_root is not None else request_path.parent
    relative = request_path.relative_to(root).as_posix()
    legacy.relative(relative)
    try:
        with tempfile.TemporaryDirectory(prefix='chirality-package-successor-') as directory:
            context = Context(root, Path(directory).resolve())
            raw = context.frozen.file(request_path, context.scratch / 'request.json')
            request = parse(raw)
            require(isinstance(request, dict), 'request must be an object')
            if request.get('format') == 'static-package-input/2':
                context.static(request)
                record_id = request['candidate']['package_record_id']
            elif request.get('format') == 'packaged-s4-binding/1':
                context.binding(request, trusted_publisher_sha256)
                record_id = request['record_id']
            else:
                raise ValueError('unsupported package request version')
            context.frozen.recheck()
            return {'format': 'packaged-s4-check/1', 'record_id': record_id, 'request_sha256': sha(raw),
                    'candidate': request['candidate'], 'errors': sorted(set(context.errors)),
                    'missing': sorted(set(context.missing)), 'artifacts': context.frozen.artifacts,
                    'source_dependencies': context.source_dependencies, 'standing': 'evidence-consistency-only',
                    'release_authorized': False, 'live_authority': False,
                    'limits': ['No signatures, runtime, installer, OS support, qualification or owner authority authenticated.',
                               'No supplier tree measured and no scanner executed; inventories are checked retained evidence.',
                               'Private publisher selection is an independent caller trust input, not authority from the packet.']}
    except ValidationError as error:
        raise ValueError('schema refusal: ' + str(error.validator)) from error


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('request')
    parser.add_argument('--evidence-root')
    parser.add_argument('--trusted-publisher-sha256')
    args = parser.parse_args()
    try:
        report = check(args.request, evidence_root=args.evidence_root, trusted_publisher_sha256=args.trusted_publisher_sha256)
        print(json.dumps(report, indent=2))
        return 2 if report['errors'] else 1 if report['missing'] else 0
    except (ValueError, OSError, TypeError, KeyError, RecursionError) as error:
        print(json.dumps({'format': 'packaged-s4-check/1', 'standing': 'refused', 'errors': [str(error)],
                          'release_authorized': False, 'live_authority': False}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
