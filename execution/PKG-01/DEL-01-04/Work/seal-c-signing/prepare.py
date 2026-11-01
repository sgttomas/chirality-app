#!/usr/bin/env python3
"""Offline SEAL-C signing preparation. Never signs, activates, or calls SecItem.

Consumes explicit digest-bound metadata and an existing completed packaging plan.
The output is a proposal and metadata-consistency report, not profile authentication.
"""
import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import plistlib
import re
import tempfile

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent


def module(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    value = importlib.util.module_from_spec(spec); spec.loader.exec_module(value)
    return value


package = module('seal_c_package_inputs', 'app/packaging/production_inputs/prepare.py')
successor = module('seal_c_publisher_join', 'app/packaging/successor/check.py')
sha, parse, require = successor.sha, successor.parse, successor.require
exact = successor.legacy.exact
APP_ID = 'com.apple.application-identifier'
TEAM = 'com.apple.developer.team-identifier'
GROUPS = 'keychain-access-groups'

class StrictPlistDict(dict):
    def __setitem__(self, key, value):
        require(key not in self, 'duplicate profile dictionary key')
        super().__setitem__(key, value)

FORMAT = 'seal-c-signing-preparation/1'


def capture(path):
    return successor.legacy.transfer(Path(path), retain=True)[0]


def timestamp(value):
    require(isinstance(value, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z', value), 'explicit UTC assessment time required')
    return dt.datetime.fromisoformat(value[:-1] + '+00:00').replace(tzinfo=None)


def pattern_allows(grant, value):
    """Only exact values or a single terminal component wildcard, never globbing."""
    return isinstance(grant, str) and (grant == value or
        (grant.endswith('.*') and grant.count('*') == 1 and value.startswith(grant[:-1])
         and len(value) > len(grant) - 1))


def metadata_entitlements(profile, certificate, publisher, namespace, at):
    """Conservative Developer ID profile-backed route; no CMS/certificate trust claim."""
    require(isinstance(profile, dict), 'decoded profile must be a plist dictionary')
    require(profile.get('Platform') == ['OSX'], 'macOS-only profile metadata required')
    require(profile.get('ProvisionsAllDevices') is True and not profile.get('ProvisionedDevices'),
            'device-bound/development profile is not this distribution route')
    creation, expiry = profile.get('CreationDate'), profile.get('ExpirationDate')
    require(isinstance(creation, dt.datetime) and isinstance(expiry, dt.datetime)
            and creation <= at < expiry, 'profile metadata outside assessed validity interval')
    require(isinstance(profile.get('UUID'), str) and profile['UUID'], 'profile UUID metadata required')
    team = publisher['developer_id_team_identifier']
    require(profile.get('TeamIdentifier') == [team], 'profile team does not match publisher')
    prefixes = profile.get('ApplicationIdentifierPrefix')
    require(isinstance(prefixes, list) and len(prefixes) == 1 and isinstance(prefixes[0], str)
            and re.fullmatch('[A-Z0-9]{10}', prefixes[0]), 'one explicit profile AppIdentifierPrefix required')
    # This is obtained from profile metadata, not assumed equal to TeamIdentifier.
    app_id = prefixes[0] + '.' + publisher['production_bundle_identifier']
    entitlements = profile.get('Entitlements')
    require(isinstance(entitlements, dict), 'profile entitlement grants absent')
    require(entitlements.get(APP_ID) == app_id, 'explicit macOS App ID profile grant required')
    require(entitlements.get(TEAM) == team, 'profile entitlement team differs')
    require(all(entitlements.get(k, False) is False for k in
                ('get-task-allow', 'com.apple.security.get-task-allow')), 'development grant refused')
    group = app_id if namespace['access_group'] is None else namespace['access_group']
    require(isinstance(group, str) and re.fullmatch('[A-Za-z0-9._-]{1,255}', group), 'exact group syntax invalid')
    # Own-App group is the smallest proposed namespace; a different group needs
    # its own explicit sharing/ownership disposition, outside this preparation.
    require(group == app_id, 'this route prepares the own-application access group only')
    grants = entitlements.get(GROUPS)
    if grants is not None:
        require(isinstance(grants, list) and any(pattern_allows(g, group) for g in grants),
                'profile metadata does not grant the exact own-App access group')
    certificates = profile.get('DeveloperCertificates')
    require(isinstance(certificates, list) and certificates and all(isinstance(c, bytes) and c for c in certificates)
            and (certificate is None or certificate in certificates),
            'selected public certificate is not among profile-authorized certificate bytes')
    proposed = {APP_ID: app_id, TEAM: team}
    # SecItem's documented default group is the application identifier when no
    # keychain-access-groups entitlement is signed. No cross-App sharing needed.
    if grants is not None: proposed[GROUPS] = [group]
    return proposed


def prepare(request_path, *, evidence_root, package_plan, output, trusted_signer_sha1,
            assessed_at, trusted_publisher_sha256=None):
    """Write private proposal outputs only. No subprocess, network, keychain or build."""
    root, plan, out = map(package.inventory.anchored, (evidence_root, package_plan, output))
    request_path = package.inventory.anchored(request_path)
    require(request_path.is_relative_to(root), 'request must be inside its evidence root')
    require(re.fullmatch('[0-9a-fA-F]{40}', trusted_signer_sha1) is not None,
            'independently selected public signer fingerprint required')
    if trusted_publisher_sha256 is not None:
        require(re.fullmatch('[0-9a-f]{64}', trusted_publisher_sha256) is not None, 'invalid independent publisher digest')
    package.no_overlap(root, [ROOT])
    package.no_overlap(plan, [ROOT])
    package.no_overlap(request_path.parent, [ROOT])
    at = timestamp(assessed_at)
    request_raw = capture(request_path); request = parse(request_raw)
    exact(request, ('format', 'namespace', 'publisher_input', 'publisher_artifacts',
                    'profile_plist', 'profile_cms', 'signer_certificate'), 'SEAL-C request')
    require(request['format'] == FORMAT, 'unknown preparation format')
    require(trusted_publisher_sha256 is None or request['publisher_artifacts'] is not None,
            'publisher trust digest cannot be checked without publisher artifacts')
    supplied = [request[k] for k in ('profile_plist', 'profile_cms', 'signer_certificate') if request[k] is not None]
    require(len({r['sha256'] for r in supplied}) == len(supplied), 'profile CMS, decoded plist and certificate must be distinct artifacts')
    namespace = request['namespace']
    exact(namespace, ('service', 'account', 'access_group'), 'namespace proposal')
    require(all(isinstance(namespace[k], str) and re.fullmatch('[A-Za-z0-9._-]{1,255}', namespace[k])
                for k in ('service', 'account')), 'namespace proposal invalid')
    require(namespace['access_group'] is None or isinstance(namespace['access_group'], str), 'group proposal invalid')
    completion = package.check_plan(plan)
    plan_raw = {name: capture(plan / name) for name in (*completion['files'], 'PLAN_COMPLETE.json')}
    require(all(sha(plan_raw[name]) == digest for name, digest in completion['files'].items()), 'plan changed during capture')
    config = parse(plan_raw['tauri.package-inputs.conf.json'])
    account = parse(plan_raw['input-inventory.json'])
    require(config.get('version') == '4.0.0' and config.get('bundle', {}).get('macOS', {}).get('minimumSystemVersion') == '15.0',
            'selected version/minimum do not match completed packaging plan')
    require(config['bundle']['macOS'].get('signingIdentity') is None, 'preparation requires unsigned plan')
    require(not os.path.lexists(out), 'new output directory required')
    package.no_overlap(out.parent, [ROOT, root, plan, request_path])
    # Context reuses existing no-follow/digest-bounded closure and publisher checks.
    with tempfile.TemporaryDirectory(prefix='seal-c-check-') as temporary:
        ctx = successor.Context(root, Path(temporary).resolve())
        selected = ctx.get(request['publisher_input'])
        require(selected is not None, 'exact publisher input absent')
        ctx.shape(selected, 'app/src-tauri/schemas/publisher-build-selection.s1.schema.json')
        require(selected['production_bundle_identifier'] == config['identifier'], 'plan and publisher identifier differ')
        require(isinstance(account.get('publisher_input'), dict) and
                account['publisher_input'].get('sha256') == request['publisher_input']['sha256'],
                'completed plan does not bind this publisher input; default-None input-test is not production')
        missing = []
        certificate = ctx.raw(request['signer_certificate']) if request['signer_certificate'] is not None else None
        if certificate is None:
            missing.append('selected public DER certificate bytes for profile certificate membership check; never a private key')
        else:
            require(certificate and hashlib.sha1(certificate).hexdigest() == trusted_signer_sha1.lower(),
                    'public certificate differs from independently selected signer fingerprint')
        publisher = None
        publisher_state = 'missing'
        artifacts = request['publisher_artifacts']
        if artifacts is None:
            missing.append('selector original/public binding, requirement and exact effective configuration after authorized build')
        else:
            exact(artifacts, ('publisher_binding', 'publisher_projection', 'publisher_requirement', 'tauri_config'), 'publisher artifacts')
            before_publisher_missing = len(ctx.missing)
            publisher = ctx.publisher(dict(artifacts, publisher_input=request['publisher_input']), trusted_publisher_sha256)
            effective = ctx.get(artifacts['tauri_config'])
            require(effective is not None, 'effective configuration absent')
            require(effective.get('version') == config['version'] and effective.get('identifier') == config['identifier'],
                    'effective version/identifier differs from packaging plan')
            require(effective.get('bundle', {}).get('macOS', {}).get('minimumSystemVersion') == '15.0', 'effective minimum differs')
            require(effective.get('bundle', {}).get('resources') == config['bundle']['resources'], 'effective resource mappings differ')
            require(not ctx.errors, 'existing publisher checker rejected exact closure')
            publisher_missing = ctx.missing[before_publisher_missing:]
            missing.extend(publisher_missing)
            publisher_state = 'gaps' if publisher_missing else 'consistent-exact-byte-joins'
        proposal, profile_summary = None, None
        cms = ctx.raw(request['profile_cms']) if request['profile_cms'] is not None else None
        if request['profile_cms'] is not None: require(cms, 'profile CMS bytes absent or empty')
        if request['profile_plist'] is None or cms is None:
            missing.append('Apple-issued Developer ID profile CMS and explicitly decoded metadata for exact App ID/group/certificate')
        if request['profile_plist'] is not None:
            profile_raw = ctx.raw(request['profile_plist'])
            require(profile_raw is not None and len(profile_raw) <= 2 * 1024 * 1024, 'profile metadata absent or too large')
            profile = plistlib.loads(profile_raw, dict_type=StrictPlistDict)
            # Evaluate available contradictions even when a companion artifact is missing.
            checked = metadata_entitlements(profile, certificate, selected, namespace, at)
            profile_summary = {'uuid': profile['UUID'], 'prefix': profile['ApplicationIdentifierPrefix'][0],
                               'creation': profile['CreationDate'].isoformat() + 'Z',
                               'expiration': profile['ExpirationDate'].isoformat() + 'Z'}
            if certificate is not None and cms: proposal = checked
        # No metadata is authentication, and no proposal is a captured owner act.
        remaining = missing + [
            'owner confirms proposed production bundle/service/account and exact profile-derived own-App group',
            'signer authenticates Apple CMS/profile provenance, decoded-to-CMS correspondence, certificate class/chain/validity',
            'review and admit exact KEYCHAIN_SELECTION for the source-wired native-menu caller; gate remains None until the actual signing stage',
            'authorized signing then actual signed entitlements/embedded profile/cdhash/effective config and publisher binding joins',
            'authorized fresh-namespace signed witness: no-UI, enrollment/readback/restart, locked/denied/missing and pending recovery',
        ]
        facts = {'format': 'seal-c-signing-plan/1', 'standing': 'offline-proposal-metadata-only',
                 'metadata_state': ('profile-proposal-publisher-gaps' if missing else 'consistent-profile-proposal') if proposal else 'required-metadata-missing',
                 'metadata_gaps_remaining': bool(missing), 'metadata_gaps': missing,
                 'publisher_closure': publisher_state,
                 'activation_gaps_remaining': True,
                 'assessed_at': assessed_at, 'request_sha256': sha(request_raw),
                 'evidence_root_locator': str(root), 'packaging_plan_locator': str(plan),
                 'locator_limit': 'private resolution hints only, never authority or future-integrity proof',
                 'packaging_plan_files': {name: sha(raw) for name, raw in plan_raw.items()},
                 'publisher_input': request['publisher_input'], 'publisher_artifacts': artifacts,
                 'profile_plist': request['profile_plist'], 'profile_cms': request['profile_cms'], 'profile_metadata': profile_summary,
                 'signer_certificate': request['signer_certificate'], 'trusted_signer_sha1': trusted_signer_sha1.lower(),
                 'independent_publisher_digest': trusted_publisher_sha256,
                 'namespace_proposal': dict(namespace, access_group=proposal[APP_ID] if proposal else None),
                 'group_route': ('explicit-own-app-group' if GROUPS in proposal else 'default-application-identifier-group') if proposal else None,
                 'profile_metadata_authenticated': False, 'owner_selection_authenticated': False,
                 'keychain_activation_authorized': False, 'signing_executed': False, 'secitem_executed': False,
                 'provider_source_sha256': sha(capture(ROOT / 'app/src-tauri/src/capture_seal_keychain.rs')),
                 'platform_source_sha256': sha(capture(ROOT / 'app/src-tauri/src/capture_seal_keychain_macos.rs')),
                 'tool_sha256': sha(Path(__file__).read_bytes()),
                 'packaging_plan_checker_sha256': sha(capture(ROOT / 'app/packaging/production_inputs/prepare.py')),
                 'packaging_inventory_helper_sha256': sha(capture(ROOT / 'app/packaging/inventory.py')),
                 'sdk_basis_sha256': sha((HERE / 'sdk-basis.json').read_bytes()),
                 'invocation_design_sha256': sha((HERE / 'ENROLLMENT_INVOCATION.md').read_bytes()),
                 'reader_sources': ctx.source_dependencies,
                 'remaining': remaining,
                 'limits': ['Profile metadata and unsigned entitlements do not authenticate Apple authorization or prove OS acceptance.',
                            'Private originals and public publisher projections retain different exact digests.',
                            'No keychain sharing grant is inferred from recovered team or old v3 entitlement absence.',
                            'No SEAL-2 exclusive-agent, entry-seal, native-origin or personal-act guarantee.']}
        outputs = {'signing-plan.json': (json.dumps(facts, indent=2) + '\n').encode(),
                   'witness-sequence.json': (HERE / 'witness-sequence.json').read_bytes()}
        if proposal:
            outputs['entitlements.proposed.plist'] = plistlib.dumps(proposal, sort_keys=True)
        ctx.frozen.recheck()
        require(capture(request_path) == request_raw, 'request changed')
        require(package.check_plan(plan) == completion, 'plan completion changed')
        out.mkdir(mode=0o700)
        package.write_new(out / 'INCOMPLETE.txt', b'Offline proposal only; require completion hashes before review.\n')
        for name, raw in outputs.items(): package.write_new(out / name, raw)
        manifest = {'format': 'seal-c-preparation-complete/1', 'files': {name: sha(raw) for name, raw in outputs.items()}}
        package.write_new(out / 'COMPLETE.json', (json.dumps(manifest, indent=2) + '\n').encode())
        fd = os.open(out, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            os.fsync(fd); (out / 'INCOMPLETE.txt').unlink(); os.fsync(fd)
        finally: os.close(fd)
        return {'format': manifest['format'], 'files': manifest['files'], 'metadata_state': facts['metadata_state'],
                'activation_authorized': False, 'signing_executed': False, 'secitem_executed': False}


def check_output(directory):
    directory = package.inventory.anchored(directory)
    require(not os.path.lexists(directory / 'INCOMPLETE.txt'), 'incomplete preparation')
    value = parse(capture(directory / 'COMPLETE.json'))
    exact(value, ('format', 'files'), 'completion')
    require(value['format'] == 'seal-c-preparation-complete/1' and set(value['files']) in
            ({'signing-plan.json', 'witness-sequence.json'}, {'signing-plan.json', 'witness-sequence.json', 'entitlements.proposed.plist'}), 'unsupported output closure')
    require({p.name for p in directory.iterdir()} == set(value['files']) | {'COMPLETE.json'}, 'unexpected output member')
    for name, digest in value['files'].items(): require(sha(capture(directory / name)) == digest, 'output byte digest differs')
    return value


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('request_path')
    for name in ('evidence-root', 'package-plan', 'output', 'trusted-signer-sha1', 'assessed-at'):
        parser.add_argument('--' + name, required=True)
    parser.add_argument('--trusted-publisher-sha256')
    try:
        print(json.dumps(prepare(**vars(parser.parse_args())), indent=2))
    except Exception as error:
        # All actual values and artifact locators stay in the caller's private closure.
        print(json.dumps({'preparation_complete': False, 'error_type': type(error).__name__}))
        raise SystemExit(2)
