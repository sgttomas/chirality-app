"""Sign, notarize and staple the 4.0.0 package from a built candidate. Only the owner runs this.

Arguments are names and paths only. The signing identity and the notary
profile are names of items already in the owner's keychain; no credential is
an argument, an environment variable, a log entry or a record. Each step is
verified before the next; any failure prints `STOP: <step>: <reason>`, runs no
later command and writes no success result. Nothing is installed: the package
is left in --out.

The App is notarized and its ticket stapled to it; then the disk image built
from the stapled App is notarized and its ticket stapled to the disk image.
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

CODESIGN, XCRUN, HDIUTIL, SPCTL, DITTO = '/usr/bin/codesign', '/usr/bin/xcrun', '/usr/bin/hdiutil', '/usr/sbin/spctl', '/usr/bin/ditto'
IDENTITY = re.compile(r'Developer ID Application: (?P<name>[^/\\\x00-\x1f]{1,200}) \((?P<team>[A-Z0-9]{10})\)')
PROFILE_NAME = re.compile(r'[A-Za-z0-9][A-Za-z0-9._-]{0,63}')
SUBMISSION_ID = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')
LONG_TOKEN = re.compile(r'[A-Za-z0-9+/=_-]{32,}')
KEY_FILES = ('.p12', '.p8', '.pem', '.cer', '.key', '.keychain', '.keychain-db', '.pfx')
CREDENTIAL_ENVIRONMENT = re.compile(r'^(APPLE_|TAURI_SIGNING_|ALTOOL|AC_(PASSWORD|USERNAME|PROVIDER))|NOTARY')
CLM_002 = ('a supplier executable lacks the supplier\'s Developer ID signature, hardened runtime, timestamp or code-directory '
           'hash, or its entitlements are unreadable or include get-task-allow; re-signing the supplier\'s files is not part of '
           'the signing arrangement (DEL-01-06 CLM-002), so whether this pin can be notarised returns to the owner')
# The stapled ticket of a bundle is written by stapler at Contents/CodeResources, outside the signature's seal.
SIGNED_EXTRA = {'Contents/_CodeSignature', 'Contents/_CodeSignature/CodeResources', 'Contents/embedded.provisionprofile'}
STAPLED_EXTRA = SIGNED_EXTRA | {record.STAPLED_TICKET}


class Stop(Exception):
    def __init__(self, step, reason):
        super().__init__(f'STOP: {step}: {reason}')
        self.step, self.reason = step, reason


def looks_like_credential(value):
    return any(p.search(value) for p in common.CREDENTIAL_PATTERNS)


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
    # The candidate and every written path: never physically inside /Applications or ~/Library.
    # The profile and the limitations file are only read and may be wherever the owner keeps them.
    for name in ('candidate', 'out'):
        try:
            common.refuse_installed_location(getattr(args, name), '--' + name)
        except ValueError as error:
            refuse(str(error))
    if os.path.lexists(args.out):
        refuse('--out already exists; give a new directory')
    if not Path(args.out).parent.is_dir():
        refuse('the parent of --out must exist')
    return match['team']


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


class Session:
    """Runs and logs commands, writes files, and redacts everything it writes through one Redactor."""

    def __init__(self, out, runner, environ, paths, redactor):
        self.out, self.runner, self.paths, self.redactor = out, runner, paths, redactor
        self.env = {'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'HOME': environ.get('HOME', '/'), 'LANG': 'en_US.UTF-8',
                    'TMPDIR': str(out / 'tmp')}
        self.signed = []
        self.log = out / 'log.jsonl'

    def writable(self, path, what='a written file'):
        common.require_inside(path, self.out, what)
        return Path(path)

    def run(self, step, argv):
        argv = [str(a) for a in argv]
        guard(argv, self.paths['app'], self.paths['dmg'], self.signed)
        result = self.runner(argv, env=self.env)
        entry = {'step': step, 'argv': argv, 'returncode': result.returncode,
                 'stdout': result.stdout.decode('utf-8', 'replace'), 'stderr': result.stderr.decode('utf-8', 'replace')}
        with open(self.writable(self.log), 'a', encoding='utf-8') as handle:
            handle.write(json.dumps(self.redactor.json(entry)) + '\n')
        return result

    def write_bytes(self, path, raw, mode=0o644):
        fd = os.open(self.writable(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, mode)
        with os.fdopen(fd, 'wb') as handle:
            handle.write(raw)
        os.chmod(path, mode)

    def write_json(self, path, value, structural=False):
        self.writable(path)
        return common.write_json_new(path, self.redactor.json(value, structural=structural))


def sign_app_argv(identity, entitlements, app):
    return [CODESIGN, '--sign', identity, '--options', 'runtime', '--timestamp', '--entitlements', str(entitlements), str(app)]


def sign_dmg_argv(identity, dmg):
    return [CODESIGN, '--sign', identity, '--timestamp', str(dmg)]


def archive_argv(app, archive):
    return [DITTO, '-c', '-k', '--sequesterRsrc', '--keepParent', str(app), str(archive)]


def submit_argv(path, profile):
    return [XCRUN, 'notarytool', 'submit', str(path), '--keychain-profile', profile, '--wait', '--output-format', 'json']


def log_argv(submission, profile):
    return [XCRUN, 'notarytool', 'log', submission, '--keychain-profile', profile]


def attach_argv(dmg, mount):
    return [HDIUTIL, 'attach', '-readonly', '-nobrowse', '-noautoopen', '-mountpoint', str(mount), str(dmg)]


def verify_app_argvs(app, requirement, vendor_paths):
    return ([[CODESIGN, '--verify', '--deep', '--strict', '--verbose=4', str(app)],
             [CODESIGN, '--verify', '--strict', '--verbose=4', '-R', '=' + requirement, str(app)],
             common.display_argv(app), common.entitlements_argv(app)]
            + [common.display_argv(app / common.VENDOR_DESTINATION / r) for r in vendor_paths])


def notarize_argvs(submitted, profile, placeholder):
    return [submit_argv(submitted, profile), log_argv(placeholder, profile)]


def staple_argvs(target):
    return [[XCRUN, 'stapler', 'staple', str(target)], [XCRUN, 'stapler', 'validate', str(target)]]


def record_argvs(app, dmg, vendor_paths):
    argvs = [common.display_argv(app), common.entitlements_argv(app)]
    for relative in vendor_paths:
        path = app / common.VENDOR_DESTINATION / relative
        argvs += [common.display_argv(path), common.entitlements_argv(path)]
    return argvs + [[XCRUN, 'stapler', 'validate', str(app)], [XCRUN, 'stapler', 'validate', str(dmg)],
                    [SPCTL, '-a', '-t', 'open', '--context', 'context:primary-signature', '-vv', str(dmg)],
                    [SPCTL, '-a', '-t', 'exec', '-vv', str(app)]]


# The step list. Each notarized subject is (step names, the file submitted, what is stapled).
STEPS = ['0 supplier signatures', '1 copy', '2 profile', '3 entitlements', '4 sign App', '5 verify App',
         '6 notarize App', '7 staple App', '8 verify stapled App', '9 disk image', '10 notarize disk image',
         '11 staple disk image', '12 Gatekeeper', '13 record']


def plan(identity, profile, paths, candidate_app, vendor_paths, requirement):
    """The exact commands, in order. Submission ids are filled from each submission's own output."""
    app, dmg, mount = paths['app'], paths['dmg'], paths['mount']
    mounted = mount / common.APP_NAME
    steps = []
    for relative in vendor_paths:
        path = candidate_app / common.VENDOR_DESTINATION / relative
        steps += [('0', common.display_argv(path)), ('0', common.entitlements_argv(path))]
    steps.append(('4', sign_app_argv(identity, paths['entitlements'], app)))
    steps += [('5', a) for a in verify_app_argvs(app, requirement, vendor_paths)]
    steps.append(('6', archive_argv(app, paths['archive'])))
    steps += [('6', a) for a in notarize_argvs(paths['archive'], profile, '<app-submission-id>')]
    steps += [('7', a) for a in staple_argvs(app)]
    steps += [('8', a) for a in verify_app_argvs(app, requirement, vendor_paths)]
    steps += [('9', [HDIUTIL, 'create', '-volname', common.VOLUME_NAME, '-srcfolder', str(paths['staging']), '-format', 'UDZO', str(dmg)]),
              ('9', sign_dmg_argv(identity, dmg)),
              ('9', [CODESIGN, '--verify', '--strict', '--verbose=4', str(dmg)]), ('9', common.display_argv(dmg))]
    steps += [('10', a) for a in notarize_argvs(dmg, profile, '<disk-image-submission-id>')]
    steps += [('11', a) for a in staple_argvs(dmg)]
    steps += [('12', [SPCTL, '-a', '-t', 'open', '--context', 'context:primary-signature', '-vv', str(dmg)]),
              ('12', attach_argv(dmg, mount)), ('12', [SPCTL, '-a', '-t', 'exec', '-vv', str(mounted)]),
              ('12', [HDIUTIL, 'detach', str(mount)]), ('13', attach_argv(dmg, mount))]
    steps += [('13', a) for a in record_argvs(mounted, dmg, vendor_paths)]
    steps.append(('13', [HDIUTIL, 'detach', str(mount)]))
    return steps


def supplier_ok(display, entitlements):
    return (display['returncode'] == 0 and not display['unsigned'] and display['team'] == common.SUPPLIER_TEAM
            and bool(display['authorities']) and display['authorities'][0].startswith('Developer ID Application:')
            and display['authorities'][0].endswith(f'({common.SUPPLIER_TEAM})') and display['runtime'] and not display['adhoc']
            and display['timestamp'] is not None and bool(display['cdhash']) and entitlements is not None
            and not entitlements.get('com.apple.security.get-task-allow') and not entitlements.get('get-task-allow'))


def make_redactor(identity, notary_profile):
    """The one redaction path: the two argument names verbatim, the public teams kept, all else credential-shaped removed."""
    return common.Redactor(allowed=(identity, notary_profile), public_teams={common.SUPPLIER_TEAM, public_team()})


def public_team():
    """The publisher team published in this checkout's source (the compiled keychain selection)."""
    return sibling('build').publisher_values(common.ROOT)[1]


def sign(args, *, runner=common.system_runner, environ=None, host=None, now=None):
    if getattr(args, 'redactor', None) is None:
        args.redactor = make_redactor(args.identity, args.notary_profile)
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
    out = Path(os.path.abspath(args.out))
    paths = {'staging': out / 'staging', 'app': out / 'staging' / common.APP_NAME,
             'dmg': out / f'{common.PRODUCT_NAME}-{common.RELEASE["version"]}.dmg', 'mount': out / 'mount',
             'entitlements': out / 'entitlements.plist', 'notary': out / 'notary',
             'archive': out / 'notary' / f'{common.PRODUCT_NAME}-{common.RELEASE["version"]}-app.zip'}
    vendor_paths = common.macho_paths(candidate['vendor']['inventory'])
    commands = plan(args.identity, args.notary_profile, paths, candidate_app, vendor_paths, requirement)
    if args.dry_run:
        return {'dry_run': True, 'plan': [{'step': s, 'argv': a} for s, a in commands]}

    out.mkdir(mode=0o700)
    session = Session(out, runner, environ, paths, args.redactor)
    for name in ('tmp', 'notary'):
        session.writable(out / name).mkdir(mode=0o700)
    app, dmg, mount = paths['app'], paths['dmg'], paths['mount']
    run = session.run

    def display(step, path, what):
        shown = common.parse_display(run(step.split()[0], common.display_argv(path)))
        if shown['returncode'] != 0 or shown['unsigned']:
            raise Stop(step, f'the signature of {what} could not be displayed')
        return shown

    # 0. The supplier's signature metadata, read before anything is copied.
    supplier = {}
    if not vendor_paths:
        raise Stop(STEPS[0], 'the vendor tree holds no Mach-O file')
    for relative in vendor_paths:
        path = candidate_app / common.VENDOR_DESTINATION / relative
        shown = common.parse_display(run('0', common.display_argv(path)))
        entitlements = common.parse_entitlements(run('0', common.entitlements_argv(path)))
        if not supplier_ok(shown, entitlements):
            raise Stop(STEPS[0], relative + ': ' + CLM_002)
        supplier[relative] = shown['cdhash']

    # 1. Copy with modes preserved under umask 022, and check the copy equal.
    previous = os.umask(0o022)
    try:
        session.writable(paths['staging'], 'the staging folder').mkdir(mode=0o755)
        shutil.copytree(candidate_app, session.writable(app, 'the App copy'), symlinks=True, copy_function=shutil.copy2)
    finally:
        os.umask(previous)
    compared = inventory.compare(inventory.scan(app), candidate['bundle']['inventory'])
    if not compared['equal']:
        raise Stop(STEPS[1], 'the copy differs from the candidate (modes or bytes): ' + json.dumps(
            {k: compared[k][:5] for k in ('differing', 'missing', 'extra')} | {'root_mode_equal': compared['root_mode_equal']}))

    # 2. The provisioning profile at Contents/embedded.provisionprofile, mode 0644.
    selected = {'developer_id_team_identifier': team, 'production_bundle_identifier': binding['production_bundle_identifier']}
    try:
        profile = prepare.profile_consistency(profile_raw, args.profile_sha256, selected, now=now)
    except ValueError as error:
        raise Stop(STEPS[2], str(error))
    destination = app / 'Contents/embedded.provisionprofile'
    session.write_bytes(destination, profile_raw)
    if os.stat(destination).st_mode & 0o7777 != 0o644 or sha(destination.read_bytes()) != args.profile_sha256:
        raise Stop(STEPS[2], 'the placed profile is not mode 0644 with the selected digest')

    # 3. Entitlements from the binding: exactly the two keys.
    entitlements = {common.APP_ID_KEY: team + '.' + binding['production_bundle_identifier'], common.TEAM_KEY: team}
    if profile['application_identifier'] != entitlements[common.APP_ID_KEY]:
        raise Stop(STEPS[3], 'the profile grants another application identifier than the publisher binding derives')
    session.write_bytes(paths['entitlements'], plistlib.dumps(entitlements, sort_keys=True))

    # 4. One signing call, on the bundle path.
    if run('4', sign_app_argv(args.identity, paths['entitlements'], app)).returncode != 0:
        raise Stop(STEPS[4], 'codesign failed; see log.jsonl')

    def verify_app(step, allowed_extra):
        number = step.split()[0]
        if run(number, [CODESIGN, '--verify', '--deep', '--strict', '--verbose=4', app]).returncode != 0:
            raise Stop(step, 'deep strict verification failed')
        if run(number, [CODESIGN, '--verify', '--strict', '--verbose=4', '-R', '=' + requirement, app]).returncode != 0:
            raise Stop(step, 'the App does not satisfy the compiled publisher requirement')
        shown = display(step, app, 'the App')
        signed_entitlements = common.parse_entitlements(run(number, common.entitlements_argv(app)))
        if signed_entitlements != entitlements:
            raise Stop(step, 'the signed entitlements are not exactly the two publisher keys')
        if not (shown['runtime'] and not shown['adhoc'] and shown['timestamp'] and shown['team'] == team
                and shown['identifier'] == binding['production_bundle_identifier'] and shown['authorities'][:1] == [args.identity]):
            raise Stop(step, 'the App signature lacks hardened runtime, timestamp, the identity or the identifier')
        compared = inventory.compare(inventory.scan(app), candidate['bundle']['inventory'])
        if (compared['differing'] != ['Contents/MacOS/' + common.MAIN_EXECUTABLE] or compared['missing']
                or set(compared['extra']) != allowed_extra or not compared['root_mode_equal']):
            raise Stop(step, 'the App changed beyond the main executable, _CodeSignature, the profile'
                       + (' and the stapled ticket' if record.STAPLED_TICKET in allowed_extra else '') + ': '
                       + json.dumps({k: compared[k][:5] for k in ('differing', 'missing', 'extra')}))
        if not inventory.compare(inventory.scan(app / common.VENDOR_DESTINATION), candidate['vendor']['inventory'])['equal']:
            raise Stop(step, 'the vendor tree changed')
        for relative in vendor_paths:
            if display(step, app / common.VENDOR_DESTINATION / relative, relative)['cdhash'] != supplier[relative]:
                raise Stop(step, 'a supplier code-directory hash changed: ' + relative)
        return shown

    def notarize(step, submitted, kind):
        """Submit, wait, fetch the log; require Accepted, an explicit empty issues list and this exact digest."""
        number = step.split()[0]
        submitted_sha256 = sha(submitted.read_bytes())
        submission = run(number, submit_argv(submitted, args.notary_profile))
        try:
            result = json.loads(submission.stdout)
        except ValueError:
            result = {}
        submission_id = result.get('id') if isinstance(result, dict) else None
        if submission.returncode != 0 or not isinstance(submission_id, str) or not SUBMISSION_ID.fullmatch(submission_id):
            raise Stop(step, 'notarytool submit did not return a submission')
        if result.get('status') != 'Accepted':
            raise Stop(step, f'notarization status is {result.get("status")!r}, not Accepted; nothing is stapled')
        fetched = run(number, log_argv(submission_id, args.notary_profile))
        try:
            log = json.loads(fetched.stdout)
        except ValueError:
            log = None
        if fetched.returncode != 0 or not isinstance(log, dict):
            raise Stop(step, 'the notarization log could not be fetched')
        if log.get('status') != 'Accepted' or 'issues' not in log or log['issues'] not in (None, []):
            raise Stop(step, 'the notarization log is not Accepted with an explicitly empty issues list; nothing is stapled')
        if log.get('sha256') != submitted_sha256 or log.get('jobId') != submission_id or sha(submitted.read_bytes()) != submitted_sha256:
            raise Stop(step, 'the notarization log does not name this exact submission; nothing is stapled')
        name = f'{kind}-notarization-log.json'
        session.write_json(paths['notary'] / name, log, structural=True)
        entry = {'log': 'notary/' + name, 'original_log_sha256': sha(fetched.stdout), 'submitted_sha256': submitted_sha256}
        if submitted.is_relative_to(paths['notary']):
            entry['submitted'] = str(submitted.relative_to(out))
        return entry

    def staple(step, target):
        number = step.split()[0]
        if run(number, [XCRUN, 'stapler', 'staple', target]).returncode != 0:
            raise Stop(step, 'stapling failed')
        if run(number, [XCRUN, 'stapler', 'validate', target]).returncode != 0:
            raise Stop(step, 'the stapled ticket does not validate')

    def detach(step):
        if run(step.split()[0], [HDIUTIL, 'detach', mount]).returncode != 0:
            raise Stop(step, 'the disk image did not detach; detach it yourself with hdiutil detach')

    def detach_after(step, stop):
        """Detach while already stopping; a failed detach is added to the reason, never hidden."""
        if run(step.split()[0], [HDIUTIL, 'detach', mount]).returncode != 0 and isinstance(stop, Stop):
            stop.reason += '; the disk image also did not detach: detach it yourself with hdiutil detach'
            stop.args = (f'STOP: {stop.step}: {stop.reason}',)

    # 5. Verify the signed App, and keep its inventory: the App as signed.
    verify_app(STEPS[5], SIGNED_EXTRA)
    signed_tree = inventory.scan(app)
    signed_vendor = inventory.scan(app / common.VENDOR_DESTINATION)

    # 6. Notarize the App: an archive of it in the private output; the bundle must not change.
    before = inventory.scan(app)
    if run('6', archive_argv(app, session.writable(paths['archive']))).returncode != 0 or not paths['archive'].is_file():
        raise Stop(STEPS[6], 'archiving the App for submission failed')
    if not inventory.compare(inventory.scan(app), before)['equal']:
        raise Stop(STEPS[6], 'archiving changed the App')
    notarizations = {'app': notarize(STEPS[6], paths['archive'], 'app')}

    # 7. Staple and validate the App: the ticket is the only difference from the App as signed.
    staple(STEPS[7], app)
    compared = inventory.compare(inventory.scan(app), signed_tree)
    if compared['differing'] or compared['missing'] or compared['extra'] != [record.STAPLED_TICKET] or not compared['root_mode_equal']:
        raise Stop(STEPS[7], 'stapling changed more than adding the ticket at ' + record.STAPLED_TICKET + ': '
                   + json.dumps({k: compared[k][:5] for k in ('differing', 'missing', 'extra')}))
    if not inventory.compare(inventory.scan(app / common.VENDOR_DESTINATION), signed_vendor)['equal']:
        raise Stop(STEPS[7], 'the supplier\'s tree changed during stapling')
    # 8. Verify the stapled App again. Nothing writes into the bundle after this.
    verify_app(STEPS[8], STAPLED_EXTRA)
    stapled_tree = inventory.scan(app)

    # 9. The disk image: the stapled App and the limitations, signed with a timestamp.
    session.write_bytes(paths['staging'] / common.LIMITATIONS_IN_IMAGE, limitations)
    if run('9', [HDIUTIL, 'create', '-volname', common.VOLUME_NAME, '-srcfolder', paths['staging'], '-format', 'UDZO',
                 session.writable(dmg)]).returncode != 0 or not dmg.is_file():
        raise Stop(STEPS[9], 'hdiutil create failed')
    if run('9', sign_dmg_argv(args.identity, dmg)).returncode != 0:
        raise Stop(STEPS[9], 'codesign of the disk image failed')
    if run('9', [CODESIGN, '--verify', '--strict', '--verbose=4', dmg]).returncode != 0:
        raise Stop(STEPS[9], 'disk image signature does not verify')
    image = display(STEPS[9], dmg, 'the disk image')
    if not (image['timestamp'] and image['team'] == team and image['authorities'][:1] == [args.identity]):
        raise Stop(STEPS[9], 'disk image signature lacks the identity or a timestamp')
    if not inventory.compare(inventory.scan(app), stapled_tree)['equal']:
        raise Stop(STEPS[9], 'the stapled App changed while the disk image was made')

    # 10. Notarize the disk image; 11. staple and validate it.
    notarizations['disk_image'] = notarize(STEPS[10], dmg, 'disk-image')
    staple(STEPS[11], dmg)

    # 12. Gatekeeper on the disk image, and on the App from a read-only mount.
    assessed = run('12', [SPCTL, '-a', '-t', 'open', '--context', 'context:primary-signature', '-vv', dmg])
    if assessed.returncode != 0 or 'accepted' not in assessed.text() or 'Notarized Developer ID' not in assessed.text():
        raise Stop(STEPS[12], 'the disk image is not accepted as Notarized Developer ID')
    session.writable(mount, 'the mount point').mkdir(mode=0o700)
    if run('12', attach_argv(dmg, mount)).returncode != 0:
        raise Stop(STEPS[12], 'the disk image did not mount read-only')
    try:
        mounted = mount / common.APP_NAME
        if not inventory.compare(inventory.scan(mounted), stapled_tree)['equal']:
            raise Stop(STEPS[12], 'the App in the disk image differs from the stapled App')
        if (mount / common.LIMITATIONS_IN_IMAGE).read_bytes() != limitations:
            raise Stop(STEPS[12], 'the limitations in the disk image differ from the candidate source')
        executed = run('12', [SPCTL, '-a', '-t', 'exec', '-vv', mounted])
        if executed.returncode != 0 or 'accepted' not in executed.text():
            raise Stop(STEPS[12], 'the App on the mounted disk image is not accepted')
    except BaseException as error:
        detach_after(STEPS[12], error)
        raise
    detach(STEPS[12])

    # 13. The package identity record, read from the package itself; every observation must succeed.
    if run('13', attach_argv(dmg, mount)).returncode != 0:
        raise Stop(STEPS[13], 'the disk image did not mount read-only')
    try:
        digest = record.write(session.writable(out / 'PACKAGE_IDENTITY.json'), dmg=dmg, app=mount / common.APP_NAME,
                              run=lambda argv: run('13', argv), candidate=candidate, notarizations=notarizations,
                              signed_tree=signed_tree, redactor=args.redactor)
    except record.ObservationFailed as failed:
        stop = Stop(STEPS[13], str(failed))
        detach_after(STEPS[13], stop)
        raise stop
    except BaseException as error:
        detach_after(STEPS[13], error)
        raise
    detach(STEPS[13])
    shutil.rmtree(out / 'tmp', ignore_errors=True)
    summary = {'identity_name': args.identity, 'notary_profile_name': args.notary_profile, 'package': dmg.name,
               'package_sha256': sha(dmg.read_bytes()), 'notarization': notarizations, 'record': 'PACKAGE_IDENTITY.json',
               'record_sha256': digest, 'installed': False, 'result': 'complete'}
    session.write_json(out / 'RESULT.json', summary)
    return summary


def parser():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--identity', required=True, help='"Developer ID Application: <name> (<TEAMID>)" as in your keychain')
    p.add_argument('--notary-profile', required=True, help='the notarytool keychain profile name you stored')
    p.add_argument('--candidate', required=True, help='the build output directory holding CANDIDATE.json (not in /Applications or ~/Library)')
    p.add_argument('--profile', required=True, help='the Developer ID provisioning profile file; only read, it may be wherever you keep it')
    p.add_argument('--profile-sha256', required=True)
    p.add_argument('--limitations', required=True,
                   help='docs/RELEASE_LIMITATIONS_4.0.0.md of the candidate source; only read, it may be wherever you keep it')
    p.add_argument('--out', required=True, help='a new directory, not in /Applications or ~/Library, for everything this run writes')
    p.add_argument('--dry-run', action='store_true', help='print the exact plan and run nothing')
    return p


def main(argv=None, *, stdout=None, stderr=None, **kw):
    stdout, stderr = stdout or sys.stdout, stderr or sys.stderr
    args = parser().parse_args(argv)
    args.redactor = make_redactor(args.identity, args.notary_profile)
    try:
        result = sign(args, **kw)
    except Exception as error:  # every failure is a STOP with no later command and no success result
        stop = error if isinstance(error, Stop) else Stop('unexpected', f'{type(error).__name__}: {error}')
        text = args.redactor.text(str(stop))
        print(text, file=stderr)
        out = Path(args.out)
        if stop.step != 'refused' and out.is_dir() and not os.path.lexists(out / 'STOPPED.json'):
            try:
                common.require_inside(out / 'STOPPED.json', out, 'STOPPED.json')
                common.write_json_new(out / 'STOPPED.json', {'result': 'stopped', 'step': stop.step, 'reason': stop.reason},
                                      redactor=args.redactor)
            except (OSError, ValueError):
                pass
        return 3
    print(json.dumps(args.redactor.json(result), indent=2), file=stdout)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
