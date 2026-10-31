"""Generate invented, non-executable package evidence. No build/signing/network."""
import copy
import importlib.util
import json
from pathlib import Path
import sys

_spec = importlib.util.spec_from_file_location('package_successor_fixture_reader', Path(__file__).with_name('check.py'))
checker = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(checker)


class Fixture:
    def __init__(self, root):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.values = {}
        self.make()

    def put_raw(self, name, raw):
        (self.root / name).write_bytes(raw)
        return {'path': name, 'sha256': checker.sha(raw)}

    def put(self, name, value):
        self.values[name] = copy.deepcopy(value)
        return self.put_raw(name, (json.dumps(value, indent=2) + '\n').encode())

    def make_terms(self):
        capture = {'supplier': 'Example supplier', 'requested_url': 'https://example.invalid/publication',
                   'resolved_url': 'https://example.invalid/publication', 'retrieved_at': '2026-10-30T10:00:00Z',
                   'http_status': 200, 'content_type': 'text/html', 'last_modified': None, 'bytes': 16,
                   'sha256': checker.sha(b'<p>INVENTED</p>'), 'publication_date': None,
                   'publication_date_note': 'INVENTED unknown', 'capture_actor': 'Example recorder',
                   'capture_method': 'INVENTED', 'full_response_custody': 'INVENTED; never read',
                   'excerpts': [{'section': 'INVENTED', 'html': '<p>INVENTED</p>', 'text': 'INVENTED',
                                 'html_sha256': checker.sha(b'<p>INVENTED</p>')}], 'standing': 'INVENTED'}
        content = self.put('terms-capture.json', capture)
        scope = {'offering': 'INVENTED local free App', 'platform': 'macOS', 'sign_in_flow': 'INVENTED managed login',
                 'implementation_revision': 'a' * 40, 'includes_first_public_distribution': True}
        answer = self.put('terms-answer.json', {'format': 'chirality.terms-owner-answer/v1', 'created_by': 'user',
                         'thread': 'INVENTED thread', 'message_id': 'INVENTED message', 'recorded_timestamp': '2026-10-30T11:00:00Z',
                         'content': 'INVENTED question ' + 'b' * 40 + '\nApprove invented applicability'})
        proposal = self.put_raw('terms-proposal.md', b'INVENTED proposal only')
        approval = self.put('terms-approval.json', {'format': 'chirality.terms-applicability-disposition/v1',
                         'purpose': 'terms_applicability_only', 'actor': 'Example owner', 'actor_role': 'owner',
                         'act': 'received_adopted_retained_evidence', 'decided_at': '2026-10-30T11:00:00Z',
                         'source_kind': 'official_publication', 'supplier': 'Example supplier', 'content': content,
                         'full_content_sha256': capture['sha256'], 'scope': scope, 'conditions': ['INVENTED condition'],
                         'exclusions': ['INVENTED exclusion'], 'approved_proposal': {'revision': 'b' * 40, 'artifact': proposal},
                         'owner_answer': answer, 'answer': 'Approve invented applicability', 'applicability': 'accepted', 'release_authorized': False})
        return self.put('terms.json', {'format': 'chirality.distribution-terms-position/v1', 'record_id': 'INVENTED-TERMS',
                        'supplier': 'Example supplier', 'state': 'applicable_position_retained', 'scope': scope,
                        'position': {'kind': 'official_publication', 'supplier': 'Example supplier', 'source_url': capture['requested_url'],
                         'publication_or_response_date': None, 'retrieved_or_received_at': capture['retrieved_at'],
                         'captured_by': 'Example recorder', 'content': content, 'full_content_sha256': capture['sha256'],
                         'conditions': ['INVENTED condition'], 'exclusions': ['INVENTED exclusion'], 'custody': 'INVENTED'},
                        'owner_disposition': {'actor': 'Example owner', 'act': 'received_adopted_retained_evidence', 'approval': approval},
                        'distribution_decision': 'not_made', 'recorded_by': 'Example recorder', 'recorded_at': '2026-10-30T12:00:00Z',
                        'limits': ['INVENTED test bytes only; no actual authority']})

    def make(self):
        evidence = self.put('evidence.json', {'standing': 'INVENTED opaque evidence, no supplier/owner/qualification act'})
        entries = [{'path': p, 'kind': 'dir', 'mode': 493} for p in ('.', 'bin', 'codex-path', 'codex-resources')]
        entries += [{'path': p, 'kind': 'file', 'mode': 493 if p == 'bin/codex' else 420,
                     'size': len(p), 'sha256': checker.sha(p.encode())} for p in ('bin/codex', 'codex-package.json')]
        inventory = {'method': 'codex-vendor-tree-v1', 'algorithm': 'sha-256', 'entries': entries,
                     'manifest_sha256': checker.sha(''.join(f"{e['sha256']}  {e['path']}\n" for e in entries if e['kind'] == 'file').encode())}
        launcher = {'kind': 'direct-vendor', 'relative_executable': 'bin/codex', 'path_prefix_relative': 'codex-path',
                    'removed_wrapper_variables': ['CODEX_MANAGED_PACKAGE_ROOT', 'CODEX_MANAGED_BY_NPM']}
        generated = {'pin': '9.9.9', 'kind': 'json-schema', 'variant': 'experimental', 'formatter_policy': 'INVENTED',
                     'manifest_sha256': '1' * 64, 'provenance': evidence, 'version_advance': evidence}
        expected = self.put('expected.json', {'format': 'expected-reference.s1', 'method': 'codex-vendor-tree-v1',
                         'pin': '9.9.9', 'platform': 'macOS arm64', 'archive': {'official_source_locator': 'INVENTED',
                         'sha256': '2' * 64, 'acquisition_authorization': evidence, 'custody': evidence,
                         'extraction_procedure': evidence, 'source_subtree': 'vendor/INVENTED'},
                         'inventory': inventory, 'launcher': launcher, 'generated': generated,
                         'label_evidence': evidence, 'generation_correspondence': evidence, 'author': 'Example author'})
        attestation = self.put('attestation.json', {'format': 'adoption-attestation.s1', 'expected_reference': expected,
                            'author': 'Example author', 'independent_reviewer': 'Example reviewer', 'reviewed_revision': 'INVENTED',
                            'review_evidence': evidence, 'adoption': {'actor': 'Example owner', 'through_help_human': evidence,
                            'decision': 'adopt-for-supplier-reference', 'evidence': evidence}, 'limits': ['INVENTED']})
        selection = self.put('selection.json', {'format': 'build-selection.s2', 'method': 'codex-vendor-tree-v1',
                            'schema_ids': ['expected-reference.s1', 'adoption-attestation.s1'], 'expected': expected, 'attestation': attestation})
        old = json.loads((checker.ROOT / 'app/packaging/static_distribution/fixtures/legacy-template.json').read_text())
        old['app'].update(revision='a' * 40, build_identity='INVENTED-BUILD', version='4.0.0', bundle_id='invalid.example.app', cdhash='c' * 40)
        old['app']['signature'].update(team='EXAMPLE001', authority='Developer ID Application: INVENTED (EXAMPLE001)')
        old['first_package_checks'] = {k: {'outcome': 'pass', 'evidence': 'INVENTED value claim only'} for k in ('fp0', 'fp1a', 'fp1b', 'fp3')}
        old['notarisation'] = {'state': 'accepted', 'submission_id': 'INVENTED', 'log_ref': 'INVENTED',
                              'submitted_by': 'Example owner', 'stapled': True, 'issues': []}
        before = self.put_raw('before.dmg', b'INVENTED before notarisation, not a disk image')
        after = self.put_raw('after.dmg', b'INVENTED after staple, not a disk image')
        old['app']['installer'].update(sha256_before_notarisation=before['sha256'], sha256_after_staple=after['sha256'])
        for side in ('published', 'packaged'):
            old['codex'][side] = {'manifest_sha256': inventory['manifest_sha256'], 'files': 2, 'macho_files': 1}
        old['codex']['executables'] = old['codex']['executables'][:1]
        for key in ('sha256_published', 'sha256_packaged'):
            old['codex']['executables'][0][key] = entries[4]['sha256']
        oldref = self.put('legacy.json', old)
        ir = self.put('inventory.json', {'format': 'inventory-artifact.s1', 'inventory': inventory})
        package = self.put('package.json', {'format': 'pkg-identity.s1', 'distribution_status': 'reference-equal',
                           'legacy_package': old, 'expected_reference': expected, 'adoption_attestation': attestation,
                           'published_inventory': ir, 'packaged_inventory': ir, 'verification_artifact': None, 'mach_o_paths': ['bin/codex']})
        candidate = {'revision': old['app']['revision'], 'build_identity': old['app']['build_identity'],
                     'codex_pin': old['codex']['pin'], 'package_record_id': old['record_id']}
        static = self.put('static.json', {'format': 'static-package-input/2', 'candidate': candidate,
                          'build_selection': selection, 's1_package': package, 'legacy_package': oldref,
                          'terms': self.make_terms(), 'installer': before})
        identity = {'format': 'publisher-build-selection.s1', 'production_bundle_identifier': old['app']['bundle_id'],
                    'developer_id_team_identifier': 'EXAMPLE001'}
        identity_ref = self.put('publisher-input.json', identity)
        config = {'identifier': old['app']['bundle_id'], 'version': '4.0.0'}
        config_ref = self.put('tauri.json', config)
        template = (checker.ROOT / 'app/src-tauri/build_support/developer-id-application.s1.requirement-template.txt').read_text()
        for key in ('production_bundle_identifier', 'developer_id_team_identifier'):
            template = template.replace('{{' + key + '}}', json.dumps(identity[key]))
        requirement = self.put_raw('requirement.txt', template.encode())
        context = {'target': 'aarch64-apple-darwin', 'profile': 'release', 'debug_assertions': False,
                   'development': False, 'successor': True, 'synthetic_anchor': False, 'package_name': 'chirality-app-v4',
                   'package_version': '0.0.0-skeleton', 'features': ['custom-protocol', 'distribution-successor'],
                   'application_identifier': identity['production_bundle_identifier'], 'application_version': '4.0.0',
                   'tauri_config_sha256': checker.sha(checker.canonical(config))}
        binding = {'format': 'publisher-build-binding.s1', 'state': 'selected-production', **{k: identity[k] for k in identity if k != 'format'},
                   'input_sha256': identity_ref['sha256'], 'requirement_sha256': requirement['sha256'],
                   'build_context': context, 'build_context_sha256': checker.sha(checker.canonical(context))}
        for key, path in {'template': 'build_support/developer-id-application.s1.requirement-template.txt',
                          'generator': 'build_support/publisher_selection.rs', 'recipe': 'build.rs',
                          'input_schema': 'schemas/publisher-build-selection.s1.schema.json',
                          'binding_schema': 'schemas/publisher-build-binding.s1.schema.json',
                          'public_projection_schema': 'schemas/publisher-build-public-projection.s1.schema.json',
                          'cargo_manifest': 'Cargo.toml', 'cargo_lock': 'Cargo.lock'}.items():
            binding[key + '_sha256'] = checker.sha((checker.ROOT / 'app/src-tauri' / path).read_bytes())
        publisher = self.put('publisher.json', binding)
        projection = self.put('public.json', {'format': 'publisher-build-public-projection.s1', 'original_binding_sha256': publisher['sha256'],
                              **{k: v for k, v in binding.items() if k.endswith('_sha256')},
                              'redacted_fields': ['production_bundle_identifier', 'developer_id_team_identifier', 'build_context.application_identifier'],
                              'standing': 'redacted-derivative-not-selection-authority'})
        app = {'revision': candidate['revision'], 'build_identity': candidate['build_identity'], 'version': '4.0.0',
               'identifier': old['app']['bundle_id'], 'cdhash': old['app']['cdhash'], 'executable': self.put_raw('app.bin', b'INVENTED non-executable App'),
               'publisher_binding_sha256': publisher['sha256'], 'public_projection_sha256': projection['sha256'], 'supplier_selection_sha256': selection['sha256']}
        location = {'bundle': '/INVENTED/App.app', 'executable': '/INVENTED/App.app/Contents/MacOS/app',
                    'resources': '/INVENTED/App.app/Contents/Resources', 'parent': '/INVENTED',
                    'translocation': 'not-established', 'app_translocation_path_component': False}
        config = {'resolved_root': location['resources'] + '/codex', 'resolved_executable': location['resources'] + '/codex/bin/codex',
                  'working_directory': '/INVENTED/project', 'argv': ['app-server'], 'path_prefix': location['resources'] + '/codex/codex-path',
                  'path_remainder_provenance': 'INVENTED', 'app_supplied_nonsecret': {}, 'removed_environment_names': launcher['removed_wrapper_variables'],
                  'probe_home': '/INVENTED/probe', 'account_home': '/INVENTED/account', 'home_link_states': 'INVENTED', 'k12_flags': ['INVENTED'], 'secret_redactions': []}
        generation = {'appSession': 'INVENTED-session', 'home': config['account_home'], 'spawnCounter': 1}
        association = {'method': 'selected-s1-contract-closure.s3', 'originalSource': '/INVENTED/closure', 'compiledAnchor': selection,
                       'expectedReference': expected, 'adoptionAttestation': attestation}
        signing = {'cdhash': app['cdhash'], 'identifier': app['identifier'], 'team_identifier': 'EXAMPLE001', 'signature_flags': 0x10000, 'get_task_allow': False}
        limits = ['Validation assumes a trusted stable installed bundle and parent path; parent writability is not checked and hostile same-user or administrator mutation remains possible',
                  'Checks are bounded observations, not an atomic snapshot or an immutable check-to-exec guarantee',
                  'No App Management protection, quarantine, notarization, Gatekeeper, revocation or installation witness is established',
                  'Nested code is checked in Security.framework standard locations; other sealed resources are checked as resources',
                  'Signing information including dynamic signature flags is disk-backed; running-process assurance comes from SecCodeCheckValidity against the compiled requirement']
        custody = self.put('custody.json', {'format': 'installed-custody-observation.s4', 'generation': generation, 'inventory': inventory,
                          'selection': association, 'app': {'observer': 'macos-security-framework.s4.v1', 'standing': 'installed-observation',
                          'requirement_sha256': requirement['sha256'], 'static_validation_flags': 536870937, 'dynamic_validation_flags': 536870912,
                          'static': signing, 'dynamic': signing, 'location': location, 'custody_assumption': 'trusted-stable-installed-bundle-and-parent-path', 'limits': limits},
                          'standing': 'process-observation-evidence-only', 'limits': ['No live authority from serialized evidence', 'No package, installer, quarantine or notarization qualification']})
        facts = self.put('facts.json', {'format': 'distribution-preflight-facts.s3', 'generation': generation, 'inventory': inventory,
                        'raw_version_label': 'codex-cli 9.9.9', 'configuration': config, 'limit': 'Bounded source observations; no installed integrity/custody issuer or qualification'})
        observation = self.put('observation.json', {'format': 'observed-verification.s4', 'expected_reference': expected,
                              'adoption_attestation': attestation, 'pin': '9.9.9', 'platform': 'macOS arm64', 'observed_label': '9.9.9',
                              'raw_version_label': 'codex-cli 9.9.9', 'generated': generated, 'inventory': inventory, 'launcher': launcher,
                              'configuration': config, 'generation': generation, 'at': 'INVENTED', 'phase': 'pre-spawn',
                              'checks': {k: {'outcome': 'pass', 'evidence': custody if k == 'custody' else facts, 'reason': 'INVENTED'}
                                         for k in ('tree', 'label', 'generated', 'custody', 'reference')},
                              'outcome': 'verified', 'limits': ['INVENTED claims only'], 'candidate_subject': None})
        self.request = {'format': 'packaged-s4-binding/1', 'record_id': 'INVENTED-PACKAGE-WITNESS', 'candidate': candidate,
                        'app': app, 'static_package': static, 'observation': observation, 'custody': custody,
                        'publisher_binding': publisher, 'publisher_projection': projection, 'publisher_input': identity_ref,
                        'publisher_requirement': requirement, 'tauri_config': config_ref, 'installer_after_stapling': after,
                        'supplier_selection': association, 'reader': 'observed-lifecycle-reader.s4.publisher-v1'}
        self.trusted_publisher_sha256 = publisher['sha256']  # explicit invented trust seam; never an actual owner selection
        self.save()

    def save(self):
        self.put('binding.json', self.request)

    def check(self, trust=True):
        self.save()
        return checker.check(self.root / 'binding.json', trusted_publisher_sha256=self.trusted_publisher_sha256 if trust else None)


if __name__ == '__main__':
    Fixture(sys.argv[1])
