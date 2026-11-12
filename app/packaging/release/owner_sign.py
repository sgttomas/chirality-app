"""Sign, notarize and staple the 4.0.0 package from a built candidate. Only the owner runs this.

Arguments are names and paths only. The signing identity and the notary
profile are names of items already in the owner's keychain; no credential is
an argument, an environment variable, a log entry or a record. Each step is
verified before the next; any failure prints `STOP: <step>: <reason>` and no
later command runs. Nothing is installed: the package is left in --out.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import platform
import plistlib
import re
import shutil
import sys


def sibling(name):
    key = 'chirality_release_' + name
    if key not in sys.modules:
        spec = importlib.util.spec_from_file_location(key, Path(__file__).resolve().parent / (name + '.py'))
        module = importlib.util.module_from_spec(spec); sys.modules[key] = module; spec.loader.exec_module(module)
    return sys.modules[key]


common, record = sibling('common'), sibling('record')
prepare, inventory, sha = common.prepare, common.inventory, common.sha

CODESIGN, XCRUN, HDIUTIL, SPCTL = '/usr/bin/codesign', '/usr/bin/xcrun', '/usr/bin/hdiutil', '/usr/sbin/spctl'
IDENTITY = re.compile(r'Developer ID Application: (?P<name>[^/\\\x00-\x1f]{1,200}) \((?P<team>[A-Z0-9]{10})\)')
PROFILE_NAME = re.compile(r'[A-Za-z0-9][A-Za-z0-9._-]{0,63}')
SUBMISSION_ID = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')
CREDENTIAL = [re.compile(p) for p in (
    r'\b[a-z]{4}-[a-z]{4}-[a-z]{4}-[a-z]{4}\b',          # app-specific password shape
    r'-----BEGIN [A-Z0-9 ]+-----[\s\S]*?(-----END [A-Z0-9 ]+-----|$)',  # PEM material
    r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',   # Apple ID e-mail
    r'\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]+\.?[A-Za-z0-9_-]*',  # JSON web token
    r'(?i)(password|passwd|secret|api[_-]?key|token)\s*[=:]\s*\S+',
)]
LONG_TOKEN = re.compile(r'[A-Za-z0-9+/=_-]{32,}')
KEY_FILES = ('.p12', '.p8', '.pem', '.cer', '.key', '.keychain', '.keychain-db', '.pfx')
CREDENTIAL_ENVIRONMENT = re.compile(r'^(APPLE_|TAURI_SIGNING_|NOTARY|NOTARYTOOL|ALTOOL|AC_(PASSWORD|USERNAME|PROVIDER))|NOTARY')
CLM_002 = ('a supplier executable lacks the supplier\'s Developer ID signature, hardened runtime or timestamp, or carries '
           'get-task-allow; re-signing the supplier\'s files is not part of the signing arrangement (DEL-01-06 CLM-002), '
           'so whether this pin can be notarised returns to the owner')


class Stop(Exception):
    def __init__(self, step, reason):
        super().__init__(f'STOP: {step}: {reason}')
        self.step, self.reason = step, reason


def redact(text):
    for pattern in CREDENTIAL:
        text = pattern.sub('[redacted]', text)
    return text


def looks_like_credential(value):
    return any(p.search(value) for p in CREDENTIAL)


def refusals(args, environ, host):
    """Every refusal that needs no command; returns the identity's team."""
    def refuse(reason): raise Stop('refused', reason)
    if host != ('Darwin', 'arm64'):
        refuse('signing runs on arm64 macOS only')
    bad = sorted(k for k in environ if CREDENTIAL_ENVIRONMENT.search(k))
    if bad:
        refuse('credential variables are set in the environment: ' + ', '.join(bad) + '; unset them, the keychain supplies everything')
    identity = args.identity
    if '/' in identity or identity.startswith(('~', '.')) or identity.lower().endswith(KEY_FILES):
        refuse('--identity must be the name of a signing identity, not a path')
    match = IDENTITY.fullmatch(identity)
    if not match:
        refuse('--identity must read exactly "Developer ID Application: <name> (<TEAMID>)"')
    if looks_like_credential(match['name']) or LONG_TOKEN.search(match['name']):
        refuse('--identity looks like a credential')
    profile = args.notary_profile
    if not PROFILE_NAME.fullmatch(profile) or looks_like_credential(profile) or LONG_TOKEN.fullmatch(profile):
        refuse('--notary-profile must be a keychain profile name (letters, digits, . _ -), not a credential')
    if not re.fullmatch('[0-9a-f]{64}', args.profile_sha256):
        refuse('--profile-sha256 must be 64 lowercase hex digits')
    for name in ('candidate', 'profile', 'limitations', 'out'):
        value = getattr(args, name)
        if looks_like_credential(value) or value.lower().endswith(KEY_FILES):
            refuse(f'--{name} looks like a credential or key file')
    for name in ('candidate', 'out'):
        try:
            common.refuse_installed_location(getattr(args, name), name)
        except ValueError as error:
            refuse(str(error))
    if os.path.lexists(args.out):
        refuse('--out already exists; give a new directory')
    if not Path(args.out).parent.is_dir():
        refuse('the parent of --out must exist')
    return match['team']


class Session:
    """Runs and logs commands; enforces the signing invariants on every call."""

    def __init__(self, out, runner, environ, app, dmg):
        self.out, self.runner, self.app, self.dmg = out, runner, Path(app), Path(dmg)
        self.env = {'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'HOME': environ.get('HOME', '/'), 'LANG': 'en_US.UTF-8',
                    'TMPDIR': str(out / 'tmp')}
        self.signed = []
        self.log = out / 'log.jsonl'

    def run(self, step, argv):
        argv = [str(a) for a in argv]
        guard(argv, self.app, self.dmg, self.signed)
        result = self.runner(argv, env=self.env)
        entry = {'step': step, 'argv': [redact(a) for a in argv], 'returncode': result.returncode,
                 'stdout': redact(result.stdout.decode('utf-8', 'replace')), 'stderr': redact(result.stderr.decode('utf-8', 'replace'))}
        with open(self.log, 'a', encoding='utf-8') as handle:
            handle.write(json.dumps(entry) + '\n')
        return result


def guard(argv, app, dmg, signed):
    """One signing call on the App bundle and one on the disk image; never --deep or --force; never into the vendor tree."""
    if argv[0] == CODESIGN and ('--sign' in argv or '-s' in argv):
        if any(a in ('--deep', '--force', '-f') or a.startswith('--deep') for a in argv):
            raise Stop('guard', 'refusing to sign with --deep or --force')
        target = Path(argv[-1])
        vendor = app / common.VENDOR_DESTINATION
        if target == vendor or target.is_relative_to(vendor) or 'Resources/codex' in argv[-1]:
            raise Stop('guard', 'refusing to sign inside the supplier\'s vendor tree')
        if target not in (app, dmg) or target in signed:
            raise Stop('guard', 'refusing a signing call other than one on the App bundle and one on the disk image')
        signed.append(target)


def sign_app_argv(identity, entitlements, app):
    return [CODESIGN, '--sign', identity, '--options', 'runtime', '--timestamp', '--entitlements', str(entitlements), str(app)]


def sign_dmg_argv(identity, dmg):
    return [CODESIGN, '--sign', identity, '--timestamp', str(dmg)]


def submit_argv(dmg, profile):
    return [XCRUN, 'notarytool', 'submit', str(dmg), '--keychain-profile', profile, '--wait', '--output-format', 'json']


def log_argv(submission, profile):
    return [XCRUN, 'notarytool', 'log', submission, '--keychain-profile', profile]


def attach_argv(dmg, mount):
    return [HDIUTIL, 'attach', '-readonly', '-nobrowse', '-noautoopen', '-mountpoint', str(mount), str(dmg)]


def record_argvs(app, dmg, vendor_paths):
    argvs = [common.display_argv(app), common.entitlements_argv(app)]
    for relative in vendor_paths:
        path = app / common.VENDOR_DESTINATION / relative
        argvs += [common.display_argv(path), common.entitlements_argv(path)]
    return argvs + [[XCRUN, 'stapler', 'validate', str(dmg)],
                    [SPCTL, '-a', '-t', 'open', '--context', 'context:primary-signature', '-vv', str(dmg)]]


def plan(identity, profile, paths, candidate_app, vendor_paths, requirement):
    """The exact commands, in order. `<submission-id>` is filled from the submission's own output."""
    app, dmg, mount, ent = paths['app'], paths['dmg'], paths['mount'], paths['entitlements']
    mounted = mount / common.APP_NAME
    steps = []
    for relative in vendor_paths:
        path = candidate_app / common.VENDOR_DESTINATION / relative
        steps += [('0', common.display_argv(path)), ('0', common.entitlements_argv(path))]
    steps.append(('4', sign_app_argv(identity, ent, app)))
    steps += [('5', [CODESIGN, '--verify', '--deep', '--strict', '--verbose=4', str(app)]),
              ('5', [CODESIGN, '--verify', '--strict', '--verbose=4', '-R', '=' + requirement, str(app)]),
              ('5', common.display_argv(app)), ('5', common.entitlements_argv(app))]
    steps += [('5', common.display_argv(app / common.VENDOR_DESTINATION / r)) for r in vendor_paths]
    steps += [('6', [HDIUTIL, 'create', '-volname', common.VOLUME_NAME, '-srcfolder', str(paths['staging']), '-format', 'UDZO', str(dmg)]),
              ('6', sign_dmg_argv(identity, dmg)),
              ('6', [CODESIGN, '--verify', '--strict', '--verbose=4', str(dmg)]), ('6', common.display_argv(dmg)),
              ('7', submit_argv(dmg, profile)), ('7', log_argv('<submission-id>', profile)),
              ('8', [XCRUN, 'stapler', 'staple', str(dmg)]), ('8', [XCRUN, 'stapler', 'validate', str(dmg)]),
              ('9', [SPCTL, '-a', '-t', 'open', '--context', 'context:primary-signature', '-vv', str(dmg)]),
              ('9', attach_argv(dmg, mount)), ('9', [SPCTL, '-a', '-t', 'exec', '-vv', str(mounted)]),
              ('9', [HDIUTIL, 'detach', str(mount)]), ('10', attach_argv(dmg, mount))]
    steps += [('10', a) for a in record_argvs(mounted, dmg, vendor_paths)]
    steps.append(('10', [HDIUTIL, 'detach', str(mount)]))
    return steps


def supplier_ok(display, entitlements):
    return (display['returncode'] == 0 and not display['unsigned'] and display['team'] == common.SUPPLIER_TEAM
            and bool(display['authorities']) and display['authorities'][0].startswith('Developer ID Application:')
            and display['authorities'][0].endswith(f'({common.SUPPLIER_TEAM})') and display['runtime'] and not display['adhoc']
            and display['timestamp'] is not None and entitlements is not None
            and not entitlements.get('com.apple.security.get-task-allow') and not entitlements.get('get-task-allow'))


def sign(args, *, runner=common.system_runner, environ=None, host=None, now=None):
    environ = dict(os.environ if environ is None else environ)
    host = host or (platform.system(), platform.machine())
    team = refusals(args, environ, host)
    try:
        candidate, candidate_app, binding, requirement = common.load_candidate(args.candidate)
    except (ValueError, OSError, KeyError) as error:
        raise Stop('refused', 'candidate description does not verify: ' + str(error))
    if binding['developer_id_team_identifier'] != team:
        raise Stop('refused', 'the identity names a team other than the candidate\'s compiled publisher team')
    limitations = Path(args.limitations).read_bytes()
    if sha(limitations) != candidate['limitations']['sha256']:
        raise Stop('refused', '--limitations is not the candidate source\'s ' + common.LIMITATIONS_SOURCE)
    profile_raw = Path(args.profile).read_bytes()
    if sha(profile_raw) != args.profile_sha256:
        raise Stop('refused', 'the provisioning profile bytes differ from --profile-sha256')
    out = inventory.anchored(args.out)
    paths = {'staging': out / 'staging', 'app': out / 'staging' / common.APP_NAME, 'dmg': out / f'{common.PRODUCT_NAME}-{common.RELEASE["version"]}.dmg',
             'mount': out / 'mount', 'entitlements': out / 'entitlements.plist'}
    vendor_paths = common.macho_paths(candidate['vendor']['inventory'])
    if args.dry_run:
        return {'dry_run': True, 'plan': [{'step': s, 'argv': a} for s, a in plan(args.identity, args.notary_profile, paths, candidate_app, vendor_paths, requirement)]}

    out.mkdir(mode=0o700)
    (out / 'tmp').mkdir(mode=0o700)
    app, dmg, mount = paths['app'], paths['dmg'], paths['mount']
    session = Session(out, runner, environ, app, dmg)
    run = session.run
    facts = {'identity_name': args.identity, 'notary_profile_name': args.notary_profile, 'candidate': str(candidate_app)}

    # 0. The supplier's signatures, read before anything is copied.
    supplier = {}
    for relative in vendor_paths:
        path = candidate_app / common.VENDOR_DESTINATION / relative
        display = common.parse_display(run('0', common.display_argv(path)))
        entitlements = common.parse_entitlements(run('0', common.entitlements_argv(path)))
        if not supplier_ok(display, entitlements):
            raise Stop('0 supplier signatures', relative + ': ' + CLM_002)
        supplier[relative] = display['cdhash']
    if not vendor_paths:
        raise Stop('0 supplier signatures', 'the vendor tree holds no Mach-O file')

    # 1. Copy with modes preserved under umask 022, and check the copy equal.
    previous = os.umask(0o022)
    try:
        paths['staging'].mkdir(mode=0o755)
        shutil.copytree(candidate_app, app, symlinks=True, copy_function=shutil.copy2)
    finally:
        os.umask(previous)
    compared = inventory.compare(inventory.scan(app), candidate['bundle']['inventory'])
    if not compared['equal']:
        raise Stop('1 copy', 'the copy differs from the candidate (modes or bytes): ' + json.dumps(
            {k: compared[k][:5] for k in ('differing', 'missing', 'extra')} | {'root_mode_equal': compared['root_mode_equal']}))

    # 2. The provisioning profile at Contents/embedded.provisionprofile, mode 0644.
    selected = {'developer_id_team_identifier': team, 'production_bundle_identifier': binding['production_bundle_identifier']}
    try:
        profile = prepare.profile_consistency(profile_raw, args.profile_sha256, selected, now=now)
    except ValueError as error:
        raise Stop('2 profile', str(error))
    destination = app / 'Contents/embedded.provisionprofile'
    fd = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
    with os.fdopen(fd, 'wb') as handle:
        handle.write(profile_raw)
    os.chmod(destination, 0o644)
    if os.stat(destination).st_mode & 0o7777 != 0o644 or sha(destination.read_bytes()) != args.profile_sha256:
        raise Stop('2 profile', 'the placed profile is not mode 0644 with the selected digest')

    # 3. Entitlements from the binding: exactly the two keys.
    entitlements = {common.APP_ID_KEY: team + '.' + binding['production_bundle_identifier'], common.TEAM_KEY: team}
    if profile['application_identifier'] != entitlements[common.APP_ID_KEY]:
        raise Stop('3 entitlements', 'the profile grants another application identifier than the publisher binding derives')
    paths['entitlements'].write_bytes(plistlib.dumps(entitlements, sort_keys=True))

    # 4. One signing call, on the bundle path.
    if run('4', sign_app_argv(args.identity, paths['entitlements'], app)).returncode != 0:
        raise Stop('4 sign App', 'codesign failed; see log.jsonl')

    # 5. Verify the signed App.
    if run('5', [CODESIGN, '--verify', '--deep', '--strict', '--verbose=4', app]).returncode != 0:
        raise Stop('5 verify App', 'deep strict verification failed')
    if run('5', [CODESIGN, '--verify', '--strict', '--verbose=4', '-R', '=' + requirement, app]).returncode != 0:
        raise Stop('5 verify App', 'the signed App does not satisfy the compiled publisher requirement')
    display = common.parse_display(run('5', common.display_argv(app)))
    signed_entitlements = common.parse_entitlements(run('5', common.entitlements_argv(app)))
    if signed_entitlements != entitlements:
        raise Stop('5 verify App', 'the signed entitlements are not exactly the two publisher keys')
    if not (display['runtime'] and not display['adhoc'] and display['timestamp'] and display['team'] == team
            and display['identifier'] == binding['production_bundle_identifier'] and display['authorities'][:1] == [args.identity]):
        raise Stop('5 verify App', 'the App signature lacks hardened runtime, timestamp, the identity or the identifier')
    after = inventory.scan(app)
    compared = inventory.compare(after, candidate['bundle']['inventory'])
    allowed_extra = {'Contents/_CodeSignature', 'Contents/_CodeSignature/CodeResources', 'Contents/embedded.provisionprofile'}
    if (compared['differing'] != ['Contents/MacOS/' + common.MAIN_EXECUTABLE] or compared['missing']
            or set(compared['extra']) != allowed_extra or not compared['root_mode_equal']):
        raise Stop('5 verify App', 'signing changed more than the main executable, _CodeSignature and the profile: ' + json.dumps(
            {k: compared[k][:5] for k in ('differing', 'missing', 'extra')}))
    if not inventory.compare(inventory.scan(app / common.VENDOR_DESTINATION), candidate['vendor']['inventory'])['equal']:
        raise Stop('5 verify App', 'the vendor tree changed during signing')
    for relative in vendor_paths:
        cdhash = common.parse_display(run('5', common.display_argv(app / common.VENDOR_DESTINATION / relative)))['cdhash']
        if cdhash is None or cdhash != supplier[relative]:
            raise Stop('5 verify App', 'a supplier code-directory hash changed: ' + relative)
    facts['app'] = {'cdhash': display['cdhash'], 'timestamp': display['timestamp'], 'entitlements': entitlements,
                    'profile': {k: profile[k] for k in ('sha256', 'uuid', 'application_identifier', 'expiration')}}
    signed_tree = inventory.scan(app)

    # 6. The disk image: the App and the limitations, signed with a timestamp.
    beside = paths['staging'] / common.LIMITATIONS_IN_IMAGE
    fd = os.open(beside, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
    with os.fdopen(fd, 'wb') as handle:
        handle.write(limitations)
    os.chmod(beside, 0o644)
    if run('6', [HDIUTIL, 'create', '-volname', common.VOLUME_NAME, '-srcfolder', paths['staging'], '-format', 'UDZO', dmg]).returncode != 0 or not dmg.is_file():
        raise Stop('6 disk image', 'hdiutil create failed')
    if run('6', sign_dmg_argv(args.identity, dmg)).returncode != 0:
        raise Stop('6 disk image', 'codesign of the disk image failed')
    if run('6', [CODESIGN, '--verify', '--strict', '--verbose=4', dmg]).returncode != 0:
        raise Stop('6 disk image', 'disk image signature does not verify')
    image = common.parse_display(run('6', common.display_argv(dmg)))
    if not (image['timestamp'] and image['team'] == team and image['authorities'][:1] == [args.identity]):
        raise Stop('6 disk image', 'disk image signature lacks the identity or a timestamp')
    submitted_sha256 = sha(dmg.read_bytes())

    # 7. Notarize: Accepted, no issues, and the log names this exact disk image.
    submission = run('7', submit_argv(dmg, args.notary_profile))
    try:
        result = json.loads(submission.stdout)
    except ValueError:
        result = {}
    submission_id = result.get('id') if isinstance(result, dict) else None
    if submission.returncode != 0 or not isinstance(submission_id, str) or not SUBMISSION_ID.fullmatch(submission_id):
        raise Stop('7 notarize', 'notarytool submit did not return a submission')
    if result.get('status') != 'Accepted':
        raise Stop('7 notarize', f'notarization status is {result.get("status")!r}, not Accepted; nothing is stapled')
    fetched = run('7', log_argv(submission_id, args.notary_profile))
    try:
        notary_log = json.loads(fetched.stdout)
    except ValueError:
        notary_log = None
    if fetched.returncode != 0 or not isinstance(notary_log, dict):
        raise Stop('7 notarize', 'the notarization log could not be fetched')
    if notary_log.get('status') != 'Accepted' or notary_log.get('issues') not in (None, []):
        raise Stop('7 notarize', 'the notarization log is not Accepted without issues; nothing is stapled')
    if notary_log.get('sha256') != submitted_sha256 or notary_log.get('jobId') != submission_id or sha(dmg.read_bytes()) != submitted_sha256:
        raise Stop('7 notarize', 'the notarization log does not name this exact disk image; nothing is stapled')
    (out / 'notarization-log.json').write_bytes(fetched.stdout)
    notarization = {'submission_id': submission_id, 'status': 'Accepted', 'issues': notary_log.get('issues'),
                    'submitted_sha256': submitted_sha256, 'log_sha256': sha(fetched.stdout)}

    # 8. Staple and validate the disk image only; the signed App is never written to.
    if run('8', [XCRUN, 'stapler', 'staple', dmg]).returncode != 0:
        raise Stop('8 staple', 'stapling the disk image failed')
    if run('8', [XCRUN, 'stapler', 'validate', dmg]).returncode != 0:
        raise Stop('8 staple', 'the stapled ticket does not validate')
    notarization['stapled_sha256'] = sha(dmg.read_bytes())

    # 9. Gatekeeper on the disk image, and on the App from a read-only mount.
    assessed = run('9', [SPCTL, '-a', '-t', 'open', '--context', 'context:primary-signature', '-vv', dmg])
    if assessed.returncode != 0 or 'accepted' not in assessed.text() or 'Notarized Developer ID' not in assessed.text():
        raise Stop('9 Gatekeeper', 'the disk image is not accepted as Notarized Developer ID')
    mount.mkdir(mode=0o700)
    if run('9', attach_argv(dmg, mount)).returncode != 0:
        raise Stop('9 Gatekeeper', 'the disk image did not mount read-only')
    try:
        mounted = mount / common.APP_NAME
        if not inventory.compare(inventory.scan(mounted), signed_tree)['equal']:
            raise Stop('9 Gatekeeper', 'the App in the disk image differs from the signed App')
        if (mount / common.LIMITATIONS_IN_IMAGE).read_bytes() != limitations:
            raise Stop('9 Gatekeeper', 'the limitations in the disk image differ from the candidate source')
        executed = run('9', [SPCTL, '-a', '-t', 'exec', '-vv', mounted])
        if executed.returncode != 0 or 'accepted' not in executed.text():
            raise Stop('9 Gatekeeper', 'the App on the mounted disk image is not accepted')
    finally:
        run('9', [HDIUTIL, 'detach', mount])

    # 10. The package identity record, read from the package itself.
    if run('10', attach_argv(dmg, mount)).returncode != 0:
        raise Stop('10 record', 'the disk image did not mount read-only')
    try:
        digest = record.write(out / 'PACKAGE_IDENTITY.json', dmg=dmg, app=mount / common.APP_NAME,
                              run=lambda argv: run('10', argv), candidate=candidate, notarization=notarization)
    finally:
        run('10', [HDIUTIL, 'detach', mount])
    shutil.rmtree(out / 'tmp', ignore_errors=True)
    summary = facts | {'package': dmg.name, 'package_sha256': sha(dmg.read_bytes()), 'notarization': notarization,
                       'record': 'PACKAGE_IDENTITY.json', 'record_sha256': digest, 'installed': False}
    common.write_json_new(out / 'RESULT.json', summary)
    return summary


def parser():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--identity', required=True, help='"Developer ID Application: <name> (<TEAMID>)" as in your keychain')
    p.add_argument('--notary-profile', required=True, help='the notarytool keychain profile name you stored')
    p.add_argument('--candidate', required=True, help='the build output directory holding CANDIDATE.json')
    p.add_argument('--profile', required=True, help='the Developer ID provisioning profile file')
    p.add_argument('--profile-sha256', required=True)
    p.add_argument('--limitations', required=True, help='docs/RELEASE_LIMITATIONS_4.0.0.md of the candidate source')
    p.add_argument('--out', required=True, help='a new directory for the package, its record and the log')
    p.add_argument('--dry-run', action='store_true', help='print the exact plan and run nothing')
    return p


def main(argv=None, **kw):
    args = parser().parse_args(argv)
    try:
        result = sign(args, **kw)
    except Exception as error:  # every failure is a STOP with no later command
        stop = error if isinstance(error, Stop) else Stop('unexpected', f'{type(error).__name__}: {redact(str(error))}')
        print(str(stop), file=sys.stderr)
        if stop.step != 'refused' and os.path.isdir(args.out) and not os.path.lexists(Path(args.out) / 'STOPPED.json'):
            common.write_json_new(Path(args.out) / 'STOPPED.json', {'step': stop.step, 'reason': stop.reason})
        return 3
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
