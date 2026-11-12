"""Package identity record (DEL-01-06 OUT-002): write it from a package, or check a package against it.

`write` builds the record that DEL-01-06's "Package identity record" term
defines from the package bytes and the operating system's own reports.
`check` re-reads a package independently and reports every difference from a
record, for VER-002's "compare the package identity record with that reading".

Reading signatures runs `codesign -d` (display), `xcrun stapler validate` and
`spctl --assess`. Only the owner, or an examiner the owner authorises, runs
this on a real package. It signs nothing, changes nothing in the package and
reads no keychain item. The App is read where the disk image is mounted
read-only; the caller mounts it (`hdiutil attach -readonly -nobrowse`).
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import plistlib
import sys


def sibling(name):
    key = 'chirality_release_' + name
    if key not in sys.modules:
        spec = importlib.util.spec_from_file_location(key, Path(__file__).resolve().parent / (name + '.py'))
        module = importlib.util.module_from_spec(spec); sys.modules[key] = module; spec.loader.exec_module(module)
    return sys.modules[key]


common = sibling('common')
prepare, inventory, require, sha = common.prepare, common.inventory, common.require, common.sha

FORMAT = 'chirality-package-identity/1'
NOT_OBSERVED = [
    'install-and-launch witness: not part of this record (DEL-01-06 REQ-003, VER-003)',
    'supplier signatures compared with the candidate vendor tree only; its identity with the supplier publication is DEL-01-01\'s expected inventory',
    'provisioning profile decoded structurally; its CMS signature and Apple authentication are not checked here',
    'entitlements needed by each named feature are not re-derived here; the expected set is the two publisher keys',
    'notice completeness (REQ-006), v3.0.1 data preservation (REQ-008) and the bundle after a run (AC-001) are not observed',
]


def inv(tree):
    """Inventory keyed by path, so that differences name paths."""
    entries = {}
    for e in tree['entries']:
        entries[e['path']] = {k: e[k] for k in ('kind', 'mode', 'sha256', 'size', 'target') if k in e}
    return {'root_mode': tree['root_mode'], 'manifest_sha256': tree['manifest_sha256'], 'files': tree['files'], 'entries': entries}


def signature(run, path):
    display = common.parse_display(run(common.display_argv(path)))
    entitlements = common.parse_entitlements(run(common.entitlements_argv(path)))
    return {'signed': display['returncode'] == 0 and not display['unsigned'], 'identifier': display['identifier'],
            'team': display['team'], 'authorities': display['authorities'], 'timestamp': display['timestamp'],
            'cdhash': display['cdhash'], 'flags': display['flags'], 'runtime': display['runtime'], 'adhoc': display['adhoc'],
            'entitlements': common.plain(entitlements) if entitlements is not None else 'unreadable'}


def profile_facts(app):
    path = Path(app) / 'Contents/embedded.provisionprofile'
    if not path.exists():
        return None
    raw = path.read_bytes()
    try:
        content = prepare.profile_content(raw)
        value = plistlib.loads(content, fmt=plistlib.FMT_XML)
    except (ValueError, plistlib.InvalidFileException) as error:
        return {'sha256': sha(raw), 'mode': oct(os.stat(path).st_mode & 0o777), 'decoded': False, 'error': str(error)}
    entitlements = value.get('Entitlements') if isinstance(value, dict) else None
    return {'sha256': sha(raw), 'mode': oct(os.stat(path).st_mode & 0o777), 'decoded': True,
            'uuid': value.get('UUID'), 'app_id': (entitlements or {}).get(common.APP_ID_KEY),
            'team': value.get('TeamIdentifier'), 'application_identifier_prefix': value.get('ApplicationIdentifierPrefix'),
            'allowed_entitlements': common.plain(entitlements), 'expiration': common.plain(value.get('ExpirationDate'))}


def limitation_copy(path, source_sha256):
    path = Path(path)
    if not path.is_file() or path.is_symlink():
        return 'not observed: absent'
    raw = path.read_bytes()
    return {'sha256': sha(raw), 'equal_to_candidate_source': source_sha256 is not None and sha(raw) == source_sha256}


def observe(dmg, app, run, limitations_source_sha256=None):
    """Everything the record states that can be read back from the package."""
    dmg, app = Path(dmg), Path(app)
    raw = dmg.read_bytes()
    info_raw, info = common.read_info_plist(app)
    identity = common.bundle_identity(info)
    resources = app / 'Contents/Resources'
    vendor_tree = inventory.scan(resources / 'codex')
    bundled = {}
    for child in sorted(resources.iterdir()):
        if child.name == 'codex':
            continue
        bundled[child.name] = inv(inventory.scan(child)) if child.is_dir() and not child.is_symlink() else {'sha256': sha(child.read_bytes())}
    manifest = resources / 'workflows/MANIFEST.json'
    if manifest.is_file():
        value = prepare.parse(manifest.read_bytes())
        workflows = {'manifest_sha256': sha(manifest.read_bytes()), 'release_subject': value.get('release_subject'),
                     'shipped_revisions': [{'name': p.get('name'), 'revision': p.get('revision')} for p in value.get('packages', [])],
                     'historical_shipped_revisions': value.get('historical_shipped_revisions')}
    else:
        workflows = 'not observed: no workflows/MANIFEST.json'
    roles = resources / 'instructions/roles.json'
    signatures = {'.': signature(run, app)}
    for relative in common.macho_paths(vendor_tree):
        signatures[common.VENDOR_DESTINATION + '/' + relative] = signature(run, app / common.VENDOR_DESTINATION / relative)
    staple = run(['/usr/bin/xcrun', 'stapler', 'validate', str(dmg)])
    assessment = run(['/usr/sbin/spctl', '-a', '-t', 'open', '--context', 'context:primary-signature', '-vv', str(dmg)])
    text = assessment.text()
    source = next((line.split('=', 1)[1].strip() for line in text.splitlines() if line.strip().startswith('source=')), None)
    return {
        'package': {'file_name': dmg.name, 'sha256': sha(raw), 'size': len(raw)},
        'bundle': {'name': app.name, 'identifier': identity['identifier'], 'version': identity['version'],
                   'bundle_version': identity['bundle_version'], 'minimum_system_version': identity['minimum_system_version'],
                   'executable': identity['executable'], 'info_plist_sha256': sha(info_raw),
                   'executable_sha256': sha((app / 'Contents/MacOS' / str(identity['executable'])).read_bytes())},
        'vendor': inv(vendor_tree),
        'resources': bundled,
        'workflows': workflows,
        'roles_sha256': sha(roles.read_bytes()) if roles.is_file() else 'not observed: absent',
        'limitations': {'bundle': limitation_copy(app / common.LIMITATIONS_IN_BUNDLE, limitations_source_sha256),
                        'disk_image': limitation_copy(app.parent / common.LIMITATIONS_IN_IMAGE, limitations_source_sha256)},
        'signatures': signatures,
        'provisioning_profile': profile_facts(app),
        'stapled_ticket': {'validated': staple.returncode == 0},
        'gatekeeper_disk_image': {'accepted': assessment.returncode == 0 and 'accepted' in text, 'source': source},
    }


def write(path, *, dmg, app, run, candidate, notarization, extra_not_observed=()):
    """Write the record once, exclusively. Returns its digest."""
    limitations_sha256 = candidate['limitations']['sha256']
    facts = observe(dmg, app, run, limitations_sha256)
    record = {'format': FORMAT, 'package': facts.pop('package'),
              'candidate': {'source_revision': candidate['source_revision'], 'pin': candidate['pin'],
                            'expected_manifest': candidate['expected_manifest'], 'build_environment_sha256': candidate['build']['environment_sha256'],
                            'unsigned_executable_sha256': candidate['bundle']['executable_sha256'],
                            'limitations_source': candidate['limitations']['source'], 'limitations_sha256': limitations_sha256},
              'observed': facts, 'notarization': notarization,
              'not_observed': NOT_OBSERVED + [f'limitations copy in the {k}: absent' for k, v in facts['limitations'].items() if isinstance(v, str)]
              + list(extra_not_observed)}
    return common.write_json_new(path, record)


def differences(recorded, observed, where=''):
    if isinstance(recorded, dict) and isinstance(observed, dict):
        found = []
        for key in sorted(set(recorded) | set(observed), key=str):
            here = f'{where}.{key}' if where else str(key)
            if key not in observed:
                found.append(f'{here}: in the record, not in the package')
            elif key not in recorded:
                found.append(f'{here}: in the package, not in the record')
            else:
                found += differences(recorded[key], observed[key], here)
        return found
    if recorded != observed:
        return [f'{where}: record {json.dumps(recorded)[:160]} != package {json.dumps(observed)[:160]}']
    return []


def check(record, *, dmg, app, run, limitations_source_sha256=None):
    """Every difference between the record and an independent reading of the package."""
    require(record.get('format') == FORMAT, 'not a package identity record')
    source = limitations_source_sha256 or record['candidate']['limitations_sha256']
    facts = observe(dmg, app, run, source)
    found = differences(record['package'], facts.pop('package'), 'package')
    found += differences(record['observed'], facts, 'observed')
    return found


def system_run(argv):
    env = {'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'HOME': os.environ.get('HOME', '/'), 'LANG': 'en_US.UTF-8'}
    return common.system_runner(argv, env=env, timeout=600)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='command', required=True)
    c = sub.add_parser('check', help='compare a package with its record')
    c.add_argument('record'); c.add_argument('--dmg', required=True)
    c.add_argument('--app', required=True, help='the App on the read-only mounted disk image')
    c.add_argument('--limitations-source', help='docs/RELEASE_LIMITATIONS_4.0.0.md of the candidate source, read independently')
    w = sub.add_parser('write', help='write a record (owner_sign.py does this as its last step)')
    w.add_argument('record'); w.add_argument('--dmg', required=True); w.add_argument('--app', required=True)
    w.add_argument('--candidate', required=True, help='the build output holding CANDIDATE.json')
    w.add_argument('--notarization', required=True, help='JSON file with the notarization result as captured')
    args = parser.parse_args(argv)
    if args.command == 'write':
        candidate = prepare.parse((Path(args.candidate) / common.CANDIDATE_FILE).read_bytes())
        notarization = prepare.parse(Path(args.notarization).read_bytes())
        print(write(args.record, dmg=args.dmg, app=args.app, run=system_run, candidate=candidate, notarization=notarization))
        return 0
    record = prepare.parse(Path(args.record).read_bytes())
    source = sha(Path(args.limitations_source).read_bytes()) if args.limitations_source else None
    found = check(record, dmg=args.dmg, app=args.app, run=system_run, limitations_source_sha256=source)
    print(json.dumps({'equal': not found, 'differences': found}, indent=2))
    return 0 if not found else 1


if __name__ == '__main__':
    raise SystemExit(main())
