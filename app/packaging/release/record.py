"""Package identity record (DEL-01-06 OUT-002): build it from a package, or check a package against it.

`build_record` reads the package and the operating system's reports through
the one observation rule (common.observe) and selects every value it records:
digests, shaped identifiers, public team identifiers, known entitlements, fixed
words. No free text from a tool is recorded. A fact the scope requires is
recorded only as read positive: the App's own code must show the publisher
identity, hardened runtime, a timestamp and no debugging entitlement, and each
supplier executable must equal what was read from the supplier's tree before
signing. When any observation fails, it raises RecordFailed with the failed
observations named by fixed words; owner_sign.py then stops and writes no record.

`check` validates a record's required structure, re-reads a package and the
returnable notarization summaries, and prints fixed messages and counts by
category. It names a differing location only when it is a field of the record's
own stated shape or a path of the committed distribution record's inventory;
anything else is counted, not named. It never compares the original
notarization logs: the record holds their digests, and the owner compares a
refetched log by hand (see the owner's page).

Reading signatures runs `codesign -d`, `xcrun stapler validate` and
`spctl --assess`. Only the owner, or an examiner the owner authorises, runs
this on a real package. It signs nothing, changes nothing in the package,
reads no keychain item and never opens the private folder.

What these tools withstand: they are operator-run tools on stable inputs. They are built so that an
observation that was not made, that failed, or that is incomplete cannot come out as success, and so
that drift and mistakes are caught. They are not a filesystem snapshot and are not built to withstand
a writer changing the inputs during the run, nor someone with write access forging a record: a
completion marker or a recorded digest is not authentication.
"""
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

FORMAT = 'chirality-package-identity/4'
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
NOT_CHECKED_LOGS = ('not checked by this tool: the original notarization logs; the record holds each log\'s digest '
                    '(original_log_sha256), which the owner compares by hand with shasum -a 256')
NOT_CHECKED_CANDIDATE = 'not checked: candidate provenance (give --candidate with the build output folder)'
FAILURES = ['bundle identity', 'signature', 'entitlements', 'unexpected entitlement', 'other team', 'ticket validation',
            'stapled ticket absent', 'gatekeeper', 'provisioning profile', 'notarization summary', 'notarization status',
            'notarization issues', 'notarization digest', 'submitted file', 'app as signed', 'workflow manifest',
            'hardened runtime', 'ad hoc signature', 'signer', 'identifier', 'debugging entitlement', 'supplier signature changed']
# Every field name the record's stated shape uses: the only keys `check` prints by name.
FIELD_NAMES = {
    'format', 'package', 'file_name', 'sha256', 'size', 'public_teams', 'publisher_team', 'candidate', 'source_revision', 'pin',
    'expected_manifest', 'build_environment_sha256', 'unsigned_executable_sha256', 'limitations_source', 'limitations_sha256',
    'observed', 'bundle', 'name', 'identifier', 'version', 'bundle_version', 'minimum_system_version', 'executable',
    'info_plist_sha256', 'executable_sha256', 'app_as_signed', 'app_as_stapled', 'digest', 'inventory', 'root_mode',
    'manifest_sha256', 'files', 'entries', 'vendor', 'resources', 'workflows', 'shipped_revisions',
    'historical_shipped_revision_count', 'roles_sha256', 'limitations', 'disk_image', 'equal_to_candidate_source', 'signatures',
    'team', 'cdhash', 'flags', 'runtime', 'adhoc', 'timestamp', 'signer', 'signer_team', 'entitlements', 'unexpected_entitlements',
    'provisioning_profile', 'decoded', 'uuid', 'app_id', 'allowed_entitlements', 'expiration', 'stapled_tickets', 'app',
    'validated', 'ticket_sha256', 'gatekeeper', 'accepted', 'source', 'notarization', 'summary', 'summary_sha256', 'submission_id',
    'status', 'issue_count', 'submitted_sha256', 'original_log_sha256', 'submitted', 'not_observed', 'mode', 'kind', 'target_sha256',
}
common.VOCABULARY.update(NOT_OBSERVED, FAILURES, {NOT_CHECKED_LOGS, NOT_CHECKED_CANDIDATE})


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


def read_signature(run, path, public_teams):
    """(facts, failure name or None): one signed executable's display and entitlements, through the one observation rule."""
    try:
        fields = common.observe('signature', run(common.display_argv(path)), subject=path)
    except common.ObservationFailed:
        return None, 'signature'
    facts = common.signature_facts(fields, public_teams)
    try:
        raw = common.observe('entitlements', run(common.entitlements_argv(path)), subject=path)
    except common.ObservationFailed:
        return facts, 'entitlements'
    chosen, unexpected = common.select_entitlements(raw, public_teams)
    facts['entitlements'] = chosen
    facts['unexpected_entitlements'] = unexpected
    return facts, None


def app_signature_failures(facts, publisher_team):
    """AC-002 for the App's own code: publisher identity, hardened runtime, a timestamp, exactly the two entitlements."""
    expected = {common.APP_ID_KEY: f'{publisher_team}.{common.RELEASE["identifier"]}', common.TEAM_KEY: publisher_team}
    found = []
    if facts['team'] != publisher_team or facts['signer_team'] != publisher_team:
        found.append('other team')
    if facts['signer'] != 'Developer ID Application':
        found.append('signer')
    if facts['identifier'] != common.RELEASE['identifier']:
        found.append('identifier')
    if not facts['runtime']:
        found.append('hardened runtime')
    if facts['adhoc']:
        found.append('ad hoc signature')
    entitlements = facts.get('entitlements') or {}
    if entitlements.get('com.apple.security.get-task-allow') or entitlements.get('get-task-allow'):
        found.append('debugging entitlement')
    if facts.get('unexpected_entitlements'):
        found.append('unexpected entitlement')
    if entitlements != expected:
        found.append('entitlements')
    return found


def supplier_signature_failures(facts, expected):
    """The supplier's executables: the supplier's signer and team, and equal to what was read before signing."""
    found = []
    if facts['team'] != common.SUPPLIER_TEAM or facts['signer_team'] != common.SUPPLIER_TEAM or facts['signer'] != 'Developer ID Application':
        found.append('other team')
    if expected is not None and facts != expected:
        found.append('supplier signature changed')
    return found


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


def observe_package(dmg, app, run, public_teams, publisher_team, limitations_source_sha256=None, supplier_expected=None):
    """Everything the record states that can be read back from the package; returns (facts, failures).

    `supplier_expected` maps each supplier executable to its signature facts as read before signing;
    when given, each must be equal at this reading.
    """
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
    signatures = {}
    facts, failed = read_signature(run, app, public_teams)
    if failed:
        failures.append(failure(failed, '.'))
    if facts is not None and not failed:
        failures += [failure(name, '.') for name in app_signature_failures(facts, publisher_team)]
    signatures['.'] = facts if facts is not None else 'not observed'
    for relative in common.macho_paths(vendor_tree):
        where = common.VENDOR_DESTINATION + '/' + relative
        facts, failed = read_signature(run, app / common.VENDOR_DESTINATION / relative, public_teams)
        if failed:
            failures.append(failure(failed, where))
        if facts is not None and not failed:
            expected = None if supplier_expected is None else supplier_expected.get(relative)
            failures += [failure(name, where) for name in supplier_signature_failures(facts, expected)]
        signatures[where] = facts if facts is not None else 'not observed'
    tickets = {}
    for key, target in (('app', app), ('disk_image', dmg)):
        try:
            common.observe('validate', run(['/usr/bin/xcrun', 'stapler', 'validate', str(target)]), subject=target)
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
            common.observe('assessment', run(argv), subject=target)
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
    try:
        path = Path(record_dir) / prepare.files.relative(entry.get('summary', 'missing'))
        summary = json.loads(path.read_bytes(), object_pairs_hook=common._unique_json)
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


def build_record(*, dmg, app, run, candidate, notarizations, signed_tree, record_dir, public_teams, publisher_team, supplier_expected):
    """The record, in memory. Raises RecordFailed when any observation it would state failed."""
    facts, failures = observe_package(dmg, app, run, public_teams, publisher_team, candidate['limitations']['sha256'], supplier_expected)
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


def committed_vendor_paths(pin):
    """Paths of the committed distribution record's inventory for `pin` (the repository's own reference files)."""
    paths = set()
    for expected in sorted((common.ROOT / 'app/src-tauri/resources/distribution-reference').rglob('expected.json')):
        try:
            value = json.loads(expected.read_bytes())
            if value.get('pin') == pin:
                paths |= {e['path'] for e in value['inventory']['entries'] if isinstance(e.get('path'), str)}
        except (OSError, ValueError, KeyError, TypeError, AttributeError):
            continue
    return paths


def differences(recorded, observed, where=()):
    """[(location segments, kind)] for every difference; kinds are fixed words."""
    if isinstance(recorded, dict) and isinstance(observed, dict):
        found = []
        for key in set(recorded) | set(observed):
            here = where + (key,)
            if key not in observed:
                found.append((here, 'in the record only'))
            elif key not in recorded:
                found.append((here, 'in the package only'))
            else:
                found += differences(recorded[key], observed[key], here)
        return found
    return [] if recorded == observed else [(where, 'differs')]


def location(segments, vendor_paths):
    """The printable prefix of a difference's location: record field names and committed inventory paths only."""
    shown, previous = [], None
    for segment in segments:
        named = isinstance(segment, str) and (
            segment in FIELD_NAMES
            or (previous == 'entries' and shown[:2] == ['observed', 'vendor'] and segment in vendor_paths)
            or (previous == 'signatures' and (segment == '.' or (segment.startswith(common.VENDOR_DESTINATION + '/')
                                                                 and segment[len(common.VENDOR_DESTINATION) + 1:] in vendor_paths))))
        if not named:
            return '.'.join(shown) + ' (an entry not named)'
        shown.append(segment)
        previous = segment
    return '.'.join(shown)


def check(record, *, dmg, app, run, record_dir, candidate_dir=None):
    """A summary of differences and failed observations by fixed category, and what was not checked."""
    missing = structure_errors(record)
    if missing:
        return {'equal': False, 'record_structure_missing': sorted(missing), 'differences': {}, 'failed_observations': {},
                'not_checked': ['everything else: the record lacks required fields', NOT_CHECKED_LOGS]}
    public_teams = set(record['public_teams'])
    vendor_paths = committed_vendor_paths(record['candidate'].get('pin'))
    facts, failures = observe_package(dmg, app, run, public_teams, record['publisher_team'], record['candidate']['limitations_sha256'])
    found = differences(record['package'], facts.pop('package'), ('package',))
    found += differences(record['observed'], facts, ('observed',))
    for key in NOTARIZED:
        observed, more = notarization_facts(record_dir, record['notarization'][key])
        failures += [failure(f['observation'], key) for f in more]
        found += differences(record['notarization'][key], observed, ('notarization', key))
    not_checked = [NOT_CHECKED_LOGS]
    if candidate_dir is not None:
        description = json.loads((Path(candidate_dir) / common.CANDIDATE_FILE).read_bytes())
        provenance = {'source_revision': description['source_revision'], 'pin': description['pin'],
                      'expected_manifest': description['expected_manifest'], 'build_environment_sha256': description['build']['environment_sha256'],
                      'unsigned_executable_sha256': description['bundle']['executable_sha256'],
                      'limitations_source': description['limitations']['source'], 'limitations_sha256': description['limitations']['sha256']}
        found += differences(record['candidate'], provenance, ('candidate',))
    else:
        not_checked.append(NOT_CHECKED_CANDIDATE)
    summary = {}
    for segments, kind in found:
        key = location(segments, vendor_paths) + ': ' + kind
        summary[key] = summary.get(key, 0) + 1
    observations = {}
    for item in failures:
        observations[item['observation']] = observations.get(item['observation'], 0) + 1
    return {'equal': not found and not failures, 'differences': dict(sorted(summary.items())),
            'failed_observations': dict(sorted(observations.items())), 'not_checked': not_checked}


def system_run(argv):
    env = {'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'HOME': os.environ.get('HOME', '/'), 'LANG': 'en_US.UTF-8'}
    return common.system_runner(argv, env=env, timeout=600)


def main(argv=None, *, run=None, stdout=None, stderr=None):
    stdout, stderr = stdout or sys.stdout, stderr or sys.stderr
    parser = common.FixedParser(description=__doc__, formatter_class=__import__('argparse').RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='command', required=True, parser_class=common.FixedParser)
    c = sub.add_parser('check', help='compare a package with its record')
    c.add_argument('record', help='PACKAGE_IDENTITY.json, in the folder that also holds notary/')
    c.add_argument('--dmg', required=True)
    c.add_argument('--app', required=True, help='the App on the read-only mounted disk image')
    c.add_argument('--candidate', help='the build output folder holding CANDIDATE.json, to check provenance')
    args = parser.parse_args(argv)
    try:
        record = json.loads(Path(args.record).read_bytes(), object_pairs_hook=common._unique_json)
        result = check(record, dmg=args.dmg, app=args.app, run=run or system_run, record_dir=Path(args.record).resolve().parent,
                       candidate_dir=args.candidate)
    except Exception:  # a fixed message: no traceback, no path, no tool text
        print(json.dumps({'equal': False, 'error': 'the record, the package, a saved summary or the candidate could not be read'}), file=stderr)
        return 2
    print(json.dumps(result, indent=2), file=stdout)
    return 0 if result['equal'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
