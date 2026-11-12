"""Package identity record (DEL-01-06 OUT-002): write it from a package, or check a package against it.

`write` builds the record that DEL-01-06's "Package identity record" term
defines from the package bytes, the operating system's own reports and the
saved notarization logs. It refuses to write a record when any observation the
record states fails: a failed observation belongs in a STOP, never in a
record of a completed package.

`check` re-reads a package independently and reports every difference from a
record, including the notarization results against the saved logs, for
VER-002's "compare the package identity record with that reading".

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

FORMAT = 'chirality-package-identity/2'
STAPLED_TICKET = 'Contents/CodeResources'
NOTARIZED = ('app', 'disk_image')
NOT_OBSERVED = [
    'install-and-launch witness: not part of this record (DEL-01-06 REQ-003, VER-003)',
    'supplier signatures are recorded as displayed (signature metadata, not cryptographic validity); their identity with the '
    'supplier publication is DEL-01-01\'s expected inventory, and the whole-tree comparison shows them unchanged',
    'provisioning profile decoded structurally; its CMS signature and Apple authentication are not checked here',
    'entitlements needed by each named feature are not re-derived here; the expected set is the two publisher keys',
    'the disk image was changed by stapling after submission; its submitted bytes are tied to the package by the digest '
    'Apple\'s log names and by the validated stapled ticket, not by re-hashing',
    'whether the installed App accepts its own signature and Codex: only the installed observation shows it',
    'notice completeness (REQ-006), v3.0.1 data preservation (REQ-008) and the bundle after a run (AC-001) are not observed',
]


class ObservationFailed(ValueError):
    def __init__(self, failures):
        super().__init__('observations failed: ' + '; '.join(failures))
        self.failures = failures


def inv(tree):
    """Inventory keyed by path, so that differences name paths."""
    entries = {}
    for e in tree['entries']:
        entries[e['path']] = {k: e[k] for k in ('kind', 'mode', 'sha256', 'size', 'target') if k in e}
    return {'root_mode': tree['root_mode'], 'manifest_sha256': tree['manifest_sha256'], 'files': tree['files'], 'entries': entries}


def bundle_state(entries):
    """An App state for the record: its inventory and one digest over paths, types, modes and bytes."""
    return {'digest': sha(json.dumps(entries, sort_keys=True).encode()), 'inventory': entries}


def as_signed(stapled):
    """The App as signed is the App as stapled without its ticket, and nothing else."""
    entries = {k: v for k, v in stapled['entries'].items() if k != STAPLED_TICKET}
    manifest = sha(''.join(f"{v['sha256']}  {k}\n" for k, v in sorted(entries.items(), key=lambda i: i[0].encode())
                           if v['kind'] == 'file').encode())
    return {'root_mode': stapled['root_mode'], 'manifest_sha256': manifest,
            'files': sum(v['kind'] == 'file' for v in entries.values()), 'entries': entries}


def signature(run, path, where, failures):
    display = common.parse_display(run(common.display_argv(path)))
    entitlements = common.parse_entitlements(run(common.entitlements_argv(path)))
    signed = display['returncode'] == 0 and not display['unsigned']
    if not signed:
        failures.append(f'signature display failed for {where}')
    elif not (display['identifier'] and display['team'] and display['cdhash'] and display['authorities']):
        failures.append(f'signature display of {where} lacks its identifier, team, signer or code-directory hash')
    if entitlements is None:
        failures.append(f'entitlements unreadable for {where}')
    return {'signed': signed, 'identifier': display['identifier'], 'team': display['team'], 'authorities': display['authorities'],
            'timestamp': display['timestamp'], 'cdhash': display['cdhash'], 'flags': display['flags'], 'runtime': display['runtime'],
            'adhoc': display['adhoc'], 'entitlements': common.plain(entitlements) if entitlements is not None else 'unreadable'}


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


def assessment(result):
    text = result.text()
    source = next((line.split('=', 1)[1].strip() for line in text.splitlines() if line.strip().startswith('source=')), None)
    return {'accepted': result.returncode == 0 and 'accepted' in text, 'source': source}


def observe(dmg, app, run, limitations_source_sha256=None):
    """Everything the record states that can be read back from the package; returns (facts, failures)."""
    dmg, app = Path(dmg), Path(app)
    failures = []
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
    signatures = {'.': signature(run, app, 'the App', failures)}
    for relative in common.macho_paths(vendor_tree):
        where = common.VENDOR_DESTINATION + '/' + relative
        signatures[where] = signature(run, app / common.VENDOR_DESTINATION / relative, where, failures)
    tickets = {}
    for key, target in (('app', app), ('disk_image', dmg)):
        validated = run(['/usr/bin/xcrun', 'stapler', 'validate', str(target)]).returncode == 0
        if not validated:
            failures.append(f'stapled ticket of the {key.replace("_", " ")} does not validate')
        tickets[key] = {'validated': validated}
    ticket = app / STAPLED_TICKET
    tickets['app']['ticket_sha256'] = sha(ticket.read_bytes()) if ticket.is_file() else 'not observed: absent'
    gatekeeper = {'disk_image': assessment(run(['/usr/sbin/spctl', '-a', '-t', 'open', '--context', 'context:primary-signature', '-vv', str(dmg)])),
                  'app': assessment(run(['/usr/sbin/spctl', '-a', '-t', 'exec', '-vv', str(app)]))}
    for key, value in gatekeeper.items():
        if not value['accepted']:
            failures.append(f'Gatekeeper did not accept the {key.replace("_", " ")}')
    profile = profile_facts(app)
    if profile is None or not profile['decoded']:
        failures.append('the provisioning profile in the App is ' + ('absent' if profile is None else 'not decodable'))
    stapled = inv(inventory.scan(app))
    if STAPLED_TICKET not in stapled['entries']:
        failures.append('the App holds no stapled ticket at ' + STAPLED_TICKET)
    facts = {
        'package': {'file_name': dmg.name, 'sha256': sha(raw), 'size': len(raw)},
        'bundle': {'name': app.name, 'identifier': identity['identifier'], 'version': identity['version'],
                   'bundle_version': identity['bundle_version'], 'minimum_system_version': identity['minimum_system_version'],
                   'executable': identity['executable'], 'info_plist_sha256': sha(info_raw),
                   'executable_sha256': sha((app / 'Contents/MacOS' / str(identity['executable'])).read_bytes())},
        # Two entries: the App as signed (derived by removing the ticket, the only permitted later
        # write) and the App as signed and stapled, as read from the package.
        'app_as_signed': bundle_state(as_signed(stapled)),
        'app_as_stapled': bundle_state(stapled),
        'vendor': inv(vendor_tree),
        'resources': bundled,
        'workflows': workflows,
        'roles_sha256': sha(roles.read_bytes()) if roles.is_file() else 'not observed: absent',
        'limitations': {'bundle': limitation_copy(app / common.LIMITATIONS_IN_BUNDLE, limitations_source_sha256),
                        'disk_image': limitation_copy(app.parent / common.LIMITATIONS_IN_IMAGE, limitations_source_sha256)},
        'signatures': signatures,
        'provisioning_profile': profile,
        'stapled_tickets': tickets,
        'gatekeeper': gatekeeper,
    }
    return facts, failures


def notarization_facts(record_dir, entry):
    """Facts derived from a saved (redacted) notarization log and, where kept, the submitted file."""
    failures = []
    log_path = Path(record_dir) / prepare.files.relative(entry['log'])
    raw = log_path.read_bytes() if log_path.is_file() else None
    try:
        log = json.loads(raw) if raw else {}
    except ValueError:
        log = None
    if not isinstance(log, dict):
        log = {}
        failures.append('notarization log is not a JSON object: ' + entry['log'])
    facts = {'log': entry['log'], 'log_sha256': sha(raw) if raw else 'not observed: absent',
             'original_log_sha256': entry['original_log_sha256'], 'submission_id': log.get('jobId'), 'status': log.get('status'),
             'issues': log.get('issues', 'not stated'), 'submitted_sha256': log.get('sha256')}
    if raw is None:
        failures.append('notarization log missing: ' + entry['log'])
    if facts['status'] != 'Accepted':
        failures.append('notarization log is not Accepted: ' + entry['log'])
    if 'issues' not in log or log['issues'] not in (None, []):
        failures.append('notarization log does not state that there are no issues: ' + entry['log'])
    if facts['submitted_sha256'] != entry['submitted_sha256']:
        failures.append('notarization log names another submitted digest: ' + entry['log'])
    if entry.get('submitted'):
        submitted = Path(record_dir) / prepare.files.relative(entry['submitted'])
        facts['submitted'] = entry['submitted']
        if not submitted.is_file() or sha(submitted.read_bytes()) != entry['submitted_sha256']:
            failures.append('submitted file differs from the digest Apple\'s log names: ' + entry['submitted'])
    return facts, failures


def write(path, *, dmg, app, run, candidate, notarizations, signed_tree, redactor, extra_not_observed=()):
    """Write the record once, exclusively; refuse when any observation it would state failed. Returns its digest.

    `signed_tree` is the App's inventory taken after signing and before stapling; the App read from the
    package without its ticket must equal it exactly.
    """
    path = Path(path)
    facts, failures = observe(dmg, app, run, candidate['limitations']['sha256'])
    if facts['app_as_signed'] != bundle_state(inv(signed_tree)):
        failures.append('the packaged App without its ticket differs from the App as signed')
    notarization = {}
    for key in NOTARIZED:
        notarization[key], more = notarization_facts(path.parent, notarizations[key])
        failures += more
    if failures:
        raise ObservationFailed(failures)
    record = {'format': FORMAT, 'package': facts.pop('package'), 'public_teams': sorted(redactor.public_teams),
              'candidate': {'source_revision': candidate['source_revision'], 'pin': candidate['pin'],
                            'expected_manifest': candidate['expected_manifest'], 'build_environment_sha256': candidate['build']['environment_sha256'],
                            'unsigned_executable_sha256': candidate['bundle']['executable_sha256'],
                            'limitations_source': candidate['limitations']['source'], 'limitations_sha256': candidate['limitations']['sha256']},
              'observed': facts, 'notarization': notarization,
              'not_observed': NOT_OBSERVED + [f'limitations copy in the {k}: absent' for k, v in facts['limitations'].items() if isinstance(v, str)]
              + list(extra_not_observed)}
    return common.write_json_new(path, record, redactor=redactor)


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


def check(record, *, dmg, app, run, record_dir, limitations_source_sha256=None):
    """Every difference between the record and an independent reading of the package and the saved logs."""
    require(record.get('format') == FORMAT, 'not a package identity record')
    redactor = common.Redactor(public_teams=record.get('public_teams', ()))
    source = limitations_source_sha256 or record['candidate']['limitations_sha256']
    facts, failures = observe(dmg, app, run, source)
    found = [f'observation failed: {f}' for f in failures]
    found += differences(record['package'], redactor.json(facts.pop('package')), 'package')
    found += differences(record['observed'], redactor.json(facts), 'observed')
    for key in NOTARIZED:
        entry = record.get('notarization', {}).get(key)
        if not isinstance(entry, dict):
            found.append(f'notarization.{key}: absent from the record'); continue
        observed, more = notarization_facts(record_dir, entry)
        found += [f'notarization.{key}: {f}' for f in more]
        found += differences(entry, redactor.json(observed), f'notarization.{key}')
    return [redactor.text(f) for f in found]


def system_run(argv):
    env = {'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'HOME': os.environ.get('HOME', '/'), 'LANG': 'en_US.UTF-8'}
    return common.system_runner(argv, env=env, timeout=600)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='command', required=True)
    c = sub.add_parser('check', help='compare a package with its record')
    c.add_argument('record', help='PACKAGE_IDENTITY.json, in the folder that also holds notary/')
    c.add_argument('--dmg', required=True)
    c.add_argument('--app', required=True, help='the App on the read-only mounted disk image')
    c.add_argument('--limitations-source', help='docs/RELEASE_LIMITATIONS_4.0.0.md of the candidate source, read independently')
    args = parser.parse_args(argv)
    record = prepare.parse(Path(args.record).read_bytes())
    source = sha(Path(args.limitations_source).read_bytes()) if args.limitations_source else None
    found = check(record, dmg=args.dmg, app=args.app, run=system_run, record_dir=Path(args.record).resolve().parent,
                  limitations_source_sha256=source)
    print(json.dumps({'equal': not found, 'differences': found}, indent=2))
    return 0 if not found else 1


if __name__ == '__main__':
    raise SystemExit(main())
