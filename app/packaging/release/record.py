"""Package identity record (DEL-01-06 OUT-002): build it from a package, or check a package against it.

`build_record` reads the package and the operating system's reports through
the one observation rule (common.observe) and selects every value it records:
digests, shaped identifiers, public team identifiers, known entitlements, fixed
words. No free text from a tool is recorded. When any observation the record
states fails, it raises RecordFailed with the failed observations named by
fixed words; owner_sign.py then stops and writes no record.

`check` validates a record's required structure, re-reads a package and the
returnable notarization summaries, and lists every difference and every
failed observation, together with what it did not check.

Reading signatures runs `codesign -d`, `xcrun stapler validate` and
`spctl --assess`. Only the owner, or an examiner the owner authorises, runs
this on a real package. It signs nothing, changes nothing in the package,
reads no keychain item and never opens the private folder.
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

FORMAT = 'chirality-package-identity/3'
STAPLED_TICKET = 'Contents/CodeResources'
NOTARIZED = ('app', 'disk_image')
NOT_OBSERVED = [
    'install-and-launch witness: not part of this record (DEL-01-06 REQ-003, VER-003)',
    'supplier signatures are recorded as displayed (signature metadata, not cryptographic validity); the whole-tree comparison shows them unchanged',
    'provisioning profile decoded structurally; its CMS signature and Apple authentication are not checked here',
    'entitlements needed by each named feature are not re-derived here; the expected set is the two publisher keys',
    'the disk image was changed by stapling after submission; its submitted bytes are tied to the package by the digest Apple\'s log names and by the validated stapled ticket',
    'whether the installed App accepts its own signature and Codex: only the installed observation shows it',
    'notice completeness (REQ-006), v3.0.1 data preservation (REQ-008) and the bundle after a run (AC-001) are not observed',
]
NOT_CHECKED = {
    'candidate': 'not checked: candidate provenance (give --candidate with the build output folder)',
    'original_logs': 'not checked: the original notarization log digests (fetch each log again and give --app-original-log and --disk-image-original-log)',
}
FAILURES = ['bundle identity', 'signature', 'entitlements', 'unexpected entitlement', 'other team', 'ticket validation',
            'stapled ticket absent', 'gatekeeper', 'provisioning profile', 'notarization summary', 'notarization status',
            'notarization issues', 'notarization digest', 'submitted file', 'app as signed', 'workflow manifest',
            'record structure', 'candidate provenance', 'original log digest']
common.VOCABULARY.update(NOT_OBSERVED, NOT_CHECKED.values(), FAILURES)


class RecordFailed(ValueError):
    def __init__(self, failures):
        super().__init__('observations failed')
        self.failures = failures


def failure(name, subject='.'):
    require(name in FAILURES, 'unlisted record failure')
    return {'observation': name, 'subject': subject}


def inv(tree):
    """Inventory keyed by path, so that differences name paths. A link's target is recorded by digest."""
    entries = {}
    for e in tree['entries']:
        item = {k: e[k] for k in ('kind', 'mode', 'sha256', 'size') if k in e}
        if 'target' in e:
            item['target_sha256'] = sha(e['target'].encode())
        entries[e['path']] = item
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


def signature(run, path, where, failures, public_teams, expect_team, exact_entitlements=None):
    """One signed executable: display and entitlements, each through the one observation rule."""
    try:
        fields = common.observe('signature', run(common.display_argv(path)))
    except common.ObservationFailed:
        failures.append(failure('signature', where))
        return 'not observed'
    facts = common.signature_facts(fields, public_teams)
    if facts['team'] != expect_team or facts['signer_team'] != expect_team:
        failures.append(failure('other team', where))
    try:
        raw = common.observe('entitlements', run(common.entitlements_argv(path)))
        chosen, unexpected = common.select_entitlements(raw, public_teams)
        facts['entitlements'] = chosen
        if unexpected:
            facts['unexpected_entitlements'] = unexpected
            if exact_entitlements is not None:
                failures.append(failure('unexpected entitlement', where))
        if exact_entitlements is not None and chosen != exact_entitlements:
            failures.append(failure('entitlements', where))
    except common.ObservationFailed:
        failures.append(failure('entitlements', where))
        facts['entitlements'] = 'not observed'
    return facts


def profile_facts(app, public_teams, failures):
    path = Path(app) / 'Contents/embedded.provisionprofile'
    if not path.is_file():
        failures.append(failure('provisioning profile'))
        return 'not observed'
    raw = path.read_bytes()
    try:
        value = plistlib.loads(prepare.profile_content(raw), fmt=plistlib.FMT_XML)
        require(isinstance(value, dict), 'profile is not a dictionary')
    except (ValueError, plistlib.InvalidFileException):
        failures.append(failure('provisioning profile'))
        return {'sha256': sha(raw), 'decoded': False}
    chosen, unexpected = common.select_entitlements(value.get('Entitlements'), public_teams)
    teams = [common.select_team(t, public_teams) for t in value.get('TeamIdentifier') or []]
    facts = {'sha256': sha(raw), 'mode': oct(os.stat(path).st_mode & 0o777), 'decoded': True,
             'uuid': common.selected(value.get('UUID'), 'profile_uuid'), 'team': teams,
             'app_id': (chosen or {}).get(common.APP_ID_KEY), 'allowed_entitlements': chosen,
             'unexpected_entitlements': unexpected, 'expiration': common.plain_datetime(value.get('ExpirationDate'))}
    if facts['uuid'] is None or facts['app_id'] is None or not teams or 'other' in teams or facts['expiration'] is None:
        failures.append(failure('provisioning profile'))
    return facts


def limitation_copy(path, source_sha256):
    path = Path(path)
    if not path.is_file() or path.is_symlink():
        return 'not observed'
    raw = path.read_bytes()
    return {'sha256': sha(raw), 'equal_to_candidate_source': source_sha256 is not None and sha(raw) == source_sha256}


def observe_package(dmg, app, run, public_teams, publisher_team, limitations_source_sha256=None):
    """Everything the record states that can be read back from the package; returns (facts, failures)."""
    dmg, app = Path(dmg), Path(app)
    failures = []
    raw = dmg.read_bytes()
    info_raw, info = common.read_info_plist(app)
    identity_fields = common.bundle_identity(info)
    bundle = {'name': common.APP_NAME if app.name == common.APP_NAME else 'other', 'info_plist_sha256': sha(info_raw)}
    for key, shape in (('identifier', 'identifier'), ('version', 'version'), ('bundle_version', 'version'),
                       ('minimum_system_version', 'version'), ('executable', 'identifier')):
        bundle[key] = common.selected(identity_fields[key], shape)
        if bundle[key] is None:
            failures.append(failure('bundle identity'))
    bundle['executable_sha256'] = sha((app / 'Contents/MacOS' / common.MAIN_EXECUTABLE).read_bytes())
    resources = app / 'Contents/Resources'
    vendor_tree = inventory.scan(resources / 'codex')
    bundled = {}
    for child in sorted(resources.iterdir()):
        if child.name == 'codex':
            continue
        bundled[child.name] = inv(inventory.scan(child)) if child.is_dir() and not child.is_symlink() else {'sha256': sha(child.read_bytes())}
    manifest = resources / 'workflows/MANIFEST.json'
    workflows = 'not observed'
    if manifest.is_file():
        try:
            value = prepare.parse(manifest.read_bytes())
            revisions = [{'name': common.selected(p.get('name'), 'identifier'), 'revision': common.selected(p.get('revision'), 'sha256')}
                         for p in value.get('packages', [])]
            require(all(r['name'] and r['revision'] for r in revisions), 'unshaped workflow entry')
            workflows = {'manifest_sha256': sha(manifest.read_bytes()), 'shipped_revisions': revisions,
                         'historical_shipped_revision_count': len(value.get('historical_shipped_revisions') or [])}
        except (ValueError, AttributeError, TypeError):
            failures.append(failure('workflow manifest'))
    stapled = inv(inventory.scan(app))
    if STAPLED_TICKET not in stapled['entries']:
        failures.append(failure('stapled ticket absent'))
    publisher_entitlements = {common.APP_ID_KEY: f'{publisher_team}.{common.RELEASE["identifier"]}', common.TEAM_KEY: publisher_team}
    signatures = {'.': signature(run, app, '.', failures, public_teams, publisher_team, exact_entitlements=publisher_entitlements)}
    for relative in common.macho_paths(vendor_tree):
        where = common.VENDOR_DESTINATION + '/' + relative
        signatures[where] = signature(run, app / common.VENDOR_DESTINATION / relative, where, failures, public_teams, common.SUPPLIER_TEAM)
    tickets = {}
    for key, target in (('app', app), ('disk_image', dmg)):
        try:
            common.observe('validate', run(['/usr/bin/xcrun', 'stapler', 'validate', str(target)]), subjects=[target])
            tickets[key] = {'validated': True}
        except common.ObservationFailed:
            tickets[key] = {'validated': False}
            failures.append(failure('ticket validation', key))
    ticket = app / STAPLED_TICKET
    tickets['app']['ticket_sha256'] = sha(ticket.read_bytes()) if ticket.is_file() else 'not observed'
    gatekeeper = {}
    for key, argv, target in (('disk_image', ['/usr/sbin/spctl', '-a', '-t', 'open', '--context', 'context:primary-signature', '-vv', str(dmg)], dmg),
                              ('app', ['/usr/sbin/spctl', '-a', '-t', 'exec', '-vv', str(app)], app)):
        try:
            common.observe('assessment', run(argv), subjects=[target])
            gatekeeper[key] = {'accepted': True, 'source': 'Notarized Developer ID'}
        except common.ObservationFailed:
            gatekeeper[key] = {'accepted': False}
            failures.append(failure('gatekeeper', key))
    facts = {
        'package': {'file_name': dmg.name, 'sha256': sha(raw), 'size': len(raw)},
        'bundle': bundle,
        'app_as_signed': bundle_state(as_signed(stapled)),
        'app_as_stapled': bundle_state(stapled),
        'vendor': inv(vendor_tree),
        'resources': bundled,
        'workflows': workflows,
        'roles_sha256': sha((resources / 'instructions/roles.json').read_bytes()) if (resources / 'instructions/roles.json').is_file() else 'not observed',
        'limitations': {'bundle': limitation_copy(app / common.LIMITATIONS_IN_BUNDLE, limitations_source_sha256),
                        'disk_image': limitation_copy(app.parent / common.LIMITATIONS_IN_IMAGE, limitations_source_sha256)},
        'signatures': signatures,
        'provisioning_profile': profile_facts(app, public_teams, failures),
        'stapled_tickets': tickets,
        'gatekeeper': gatekeeper,
    }
    return facts, failures


SUMMARY_FIELDS = ('job', 'status', 'sha256', 'issue_count', 'original_log_sha256')


def notarization_facts(record_dir, entry):
    """Facts from a returnable notarization summary (never the raw log) and, for the App, the submitted archive."""
    failures = []
    path = Path(record_dir) / prepare.files.relative(entry.get('summary', 'missing'))
    try:
        summary = json.loads(path.read_bytes())
        require(isinstance(summary, dict) and set(summary) == set(SUMMARY_FIELDS), 'summary shape')
    except (OSError, ValueError):
        failures.append(failure('notarization summary'))
        return {'summary': entry.get('summary')}, failures
    facts = {'summary': entry['summary'], 'summary_sha256': sha(path.read_bytes()), 'submission_id': summary['job'],
             'status': summary['status'], 'issue_count': summary['issue_count'], 'submitted_sha256': summary['sha256'],
             'original_log_sha256': summary['original_log_sha256']}
    if summary['status'] != 'Accepted':
        failures.append(failure('notarization status'))
    if summary['issue_count'] != 0:
        failures.append(failure('notarization issues'))
    if summary['sha256'] != entry.get('submitted_sha256'):
        failures.append(failure('notarization digest'))
    if 'submitted' in entry:
        facts['submitted'] = entry['submitted']
        submitted = Path(record_dir) / prepare.files.relative(entry['submitted'])
        if not submitted.is_file() or sha(submitted.read_bytes()) != summary['sha256']:
            failures.append(failure('submitted file'))
    return facts, failures


def build_record(*, dmg, app, run, candidate, notarizations, signed_tree, record_dir, public_teams, publisher_team):
    """The record, in memory. Raises RecordFailed when any observation it would state failed."""
    facts, failures = observe_package(dmg, app, run, public_teams, publisher_team, candidate['limitations']['sha256'])
    if facts['app_as_signed'] != bundle_state(inv(signed_tree)):
        failures.append(failure('app as signed'))
    notarization = {}
    for key in NOTARIZED:
        notarization[key], more = notarization_facts(record_dir, notarizations[key])
        failures += more
    if failures:
        raise RecordFailed(failures)
    return {'format': FORMAT, 'package': facts.pop('package'), 'public_teams': sorted(public_teams), 'publisher_team': publisher_team,
            'candidate': {'source_revision': candidate['source_revision'], 'pin': candidate['pin'],
                          'expected_manifest': candidate['expected_manifest'], 'build_environment_sha256': candidate['build']['environment_sha256'],
                          'unsigned_executable_sha256': candidate['bundle']['executable_sha256'],
                          'limitations_source': candidate['limitations']['source'], 'limitations_sha256': candidate['limitations']['sha256']},
            'observed': facts, 'notarization': notarization,
            'not_observed': NOT_OBSERVED + [f'limitations copy in the {k}: absent' for k, v in facts['limitations'].items() if isinstance(v, str)]}


REQUIRED = {
    'format': None, 'package': ('file_name', 'sha256', 'size'), 'public_teams': None, 'publisher_team': None,
    'candidate': ('source_revision', 'pin', 'expected_manifest', 'build_environment_sha256', 'unsigned_executable_sha256',
                  'limitations_source', 'limitations_sha256'),
    'observed': ('bundle', 'app_as_signed', 'app_as_stapled', 'vendor', 'resources', 'workflows', 'roles_sha256', 'limitations',
                 'signatures', 'provisioning_profile', 'stapled_tickets', 'gatekeeper'),
    'notarization': ('app', 'disk_image'), 'not_observed': None,
}
NOTARIZATION_REQUIRED = {'app': ('summary', 'summary_sha256', 'submission_id', 'status', 'issue_count', 'submitted_sha256',
                                 'original_log_sha256', 'submitted'),
                         'disk_image': ('summary', 'summary_sha256', 'submission_id', 'status', 'issue_count', 'submitted_sha256',
                                        'original_log_sha256')}


def structure_errors(record):
    missing = []
    if not isinstance(record, dict) or record.get('format') != FORMAT:
        return ['format']
    for key, fields in REQUIRED.items():
        if key not in record:
            missing.append(key); continue
        for field in fields or ():
            if not isinstance(record[key], dict) or field not in record[key]:
                missing.append(f'{key}.{field}')
    for key, fields in NOTARIZATION_REQUIRED.items():
        entry = record.get('notarization', {}).get(key) if isinstance(record.get('notarization'), dict) else None
        for field in fields:
            if not isinstance(entry, dict) or field not in entry:
                missing.append(f'notarization.{key}.{field}')
    return missing


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
        return [f'{where}: differs']
    return []


def check(record, *, dmg, app, run, record_dir, candidate_dir=None, original_logs=None):
    """(differences, not_checked): every difference from the record and every failed observation, and what was not checked."""
    missing = structure_errors(record)
    if missing:
        return [f'record structure: lacks {m}' for m in missing], ['nothing else: the record lacks required fields']
    public_teams = set(record['public_teams'])
    facts, failures = observe_package(dmg, app, run, public_teams, record['publisher_team'], record['candidate']['limitations_sha256'])
    found = [f'observation failed: {f["observation"]} ({f["subject"]})' for f in failures]
    found += differences(record['package'], facts.pop('package'), 'package')
    found += differences(record['observed'], facts, 'observed')
    for key in NOTARIZED:
        observed, more = notarization_facts(record_dir, record['notarization'][key])
        found += [f'notarization.{key}: {f["observation"]}' for f in more]
        found += differences(record['notarization'][key], observed, f'notarization.{key}')
    not_checked = []
    if candidate_dir is not None:
        description = json.loads((Path(candidate_dir) / common.CANDIDATE_FILE).read_bytes())
        provenance = {'source_revision': description['source_revision'], 'pin': description['pin'],
                      'expected_manifest': description['expected_manifest'], 'build_environment_sha256': description['build']['environment_sha256'],
                      'unsigned_executable_sha256': description['bundle']['executable_sha256'],
                      'limitations_source': description['limitations']['source'], 'limitations_sha256': description['limitations']['sha256']}
        found += differences(record['candidate'], provenance, 'candidate')
    else:
        not_checked.append(NOT_CHECKED['candidate'])
    if original_logs:
        for key, path in original_logs.items():
            if sha(Path(path).read_bytes()) != record['notarization'][key]['original_log_sha256']:
                found.append(f'notarization.{key}.original_log_sha256: differs from the log given')
    else:
        not_checked.append(NOT_CHECKED['original_logs'])
    return found, not_checked


def system_run(argv):
    env = {'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'HOME': os.environ.get('HOME', '/'), 'LANG': 'en_US.UTF-8'}
    return common.system_runner(argv, env=env, timeout=600)


def main(argv=None, *, run=None, stdout=None, stderr=None):
    stdout, stderr = stdout or sys.stdout, stderr or sys.stderr
    parser = common.FixedParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='command', required=True, parser_class=common.FixedParser)
    c = sub.add_parser('check', help='compare a package with its record')
    c.add_argument('record', help='PACKAGE_IDENTITY.json, in the folder that also holds notary/')
    c.add_argument('--dmg', required=True)
    c.add_argument('--app', required=True, help='the App on the read-only mounted disk image')
    c.add_argument('--candidate', help='the build output folder holding CANDIDATE.json, to check provenance')
    c.add_argument('--app-original-log', help='the App\'s notarization log fetched again with notarytool log')
    c.add_argument('--disk-image-original-log', help='the disk image\'s notarization log fetched again with notarytool log')
    args = parser.parse_args(argv)
    try:
        record = json.loads(Path(args.record).read_bytes())
        logs = {k: v for k, v in (('app', args.app_original_log), ('disk_image', args.disk_image_original_log)) if v}
        found, not_checked = check(record, dmg=args.dmg, app=args.app, run=run or system_run, record_dir=Path(args.record).resolve().parent,
                                   candidate_dir=args.candidate, original_logs=logs or None)
    except Exception:  # a fixed message: no traceback, no path, no tool text
        print(json.dumps({'equal': False, 'error': 'the record, the package, a saved summary or a given file could not be read'}), file=stderr)
        return 2
    print(json.dumps({'equal': not found, 'differences': found, 'not_checked': not_checked}, indent=2), file=stdout)
    return 0 if not found else 1


if __name__ == '__main__':
    raise SystemExit(main())
