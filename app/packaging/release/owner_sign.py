"""Sign, notarize and staple the 4.0.0 package from a built candidate. Only the owner runs this.

Arguments are names and paths only. The signing identity and the notary
profile are names of items already in the owner's keychain; no credential is
an argument or an environment variable.

Each step is verified before the next. Every observation goes through the one
rule in common.observe. Any failure prints `STOP: <fixed reason>` (a reason
from common.REASONS, naming the step and the observation), writes STOPPED.json,
runs no later command and writes no success result. Nothing is installed.

What is written, and where:
- Returnable files (sent back): log.jsonl, the notarization summaries in
  notary/, the App archive, PACKAGE_IDENTITY.json, RESULT.json or STOPPED.json.
  They hold only values this tool constructs or selects and validates
  (common.write_returnable); the command log holds the argv the tool built,
  return codes, and the length and SHA-256 of each output stream, never
  their content.
- The private folder (its name is defined in common.py): raw command output, raw
  notarization logs and traces, for the owner's own diagnosis. It may hold
  account details, stays on the owner's machine and is not sent back. It is
  written only through common.PrivateWriter and never read by this tool, by
  record.py or by any test.

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
import traceback


def sibling(name):
    key = 'chirality_release_' + name
    if key not in sys.modules:
        spec = importlib.util.spec_from_file_location(key, Path(__file__).resolve().parent / (name + '.py'))
        module = importlib.util.module_from_spec(spec); sys.modules[key] = module; spec.loader.exec_module(module)
    return sys.modules[key]


common, record = sibling('common'), sibling('record')
prepare, inventory, sha = common.prepare, common.inventory, common.sha
Failure, check, observe, ObservationFailed = common.Failure, common.check, common.observe, common.ObservationFailed

CODESIGN, XCRUN, HDIUTIL, SPCTL, DITTO = '/usr/bin/codesign', '/usr/bin/xcrun', '/usr/bin/hdiutil', '/usr/sbin/spctl', '/usr/bin/ditto'
IDENTITY = re.compile(r'Developer ID Application: (?P<name>[^/\\\x00-\x1f]{1,200}) \((?P<team>[A-Z0-9]{10})\)')
PROFILE_NAME = re.compile(r'[A-Za-z0-9][A-Za-z0-9._-]{0,63}')
LONG_TOKEN = re.compile(r'[A-Za-z0-9+/=_-]{32,}')
KEY_FILES = ('.p12', '.p8', '.pem', '.cer', '.key', '.keychain', '.keychain-db', '.pfx')
CREDENTIAL_ENVIRONMENT = re.compile(r'^(APPLE_|TAURI_SIGNING_|ALTOOL|AC_(PASSWORD|USERNAME|PROVIDER))|NOTARY')
# Shapes refused in arguments (input validation only; output is protected by selection, not by patterns).
ARGUMENT_CREDENTIAL = [re.compile(p) for p in (
    r'\b[a-z]{4}-[a-z]{4}-[a-z]{4}-[a-z]{4}\b', r'-----BEGIN', r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', r'\beyJ[A-Za-z0-9_-]{8,}\.',
    r'(?i)\b(?:password|passwd|secret|token|api[_-]?key)\b\s*[=:]')]
# Apple's stapler writes a bundle's ticket at Contents/CodeResources, outside what the signature
# seals (the expected Apple layout). What this tool itself establishes is narrower: after stapling,
# the only inventory change is that file, and the App is then verified again (step 8).
SIGNED_EXTRA = {'Contents/_CodeSignature', 'Contents/_CodeSignature/CodeResources', 'Contents/embedded.provisionprofile'}
STAPLED_EXTRA = SIGNED_EXTRA | {record.STAPLED_TICKET}
STEP_NAMES = {0: 'supplier signatures', 1: 'copy', 2: 'profile', 3: 'entitlements', 4: 'sign App', 5: 'verify App',
              6: 'notarize App', 7: 'staple App', 8: 'verify stapled App', 9: 'disk image', 10: 'notarize disk image',
              11: 'staple disk image', 12: 'Gatekeeper', 13: 'record'}
common.VOCABULARY.update({'-R', '-c', '-k', '--sequesterRsrc', '--keepParent', '--deep', '--strict', '--verify', '-vv'})


def looks_like_credential(value):
    return any(p.search(value) for p in ARGUMENT_CREDENTIAL)


def refusals(args, environ, host):
    """Every refusal that needs no command; returns the identity's team."""
    check(host == ('Darwin', 'arm64'), 'REFUSED_HOST')
    check(not any(CREDENTIAL_ENVIRONMENT.search(k) for k in environ), 'REFUSED_ENVIRONMENT')
    identity = args.identity
    check(not ('/' in identity or identity.startswith(('~', '.')) or identity.lower().endswith(KEY_FILES)), 'REFUSED_IDENTITY_PATH')
    match = IDENTITY.fullmatch(identity)
    check(match is not None, 'REFUSED_IDENTITY_FORM')
    check(not (looks_like_credential(match['name']) or LONG_TOKEN.search(match['name'])), 'REFUSED_IDENTITY_CREDENTIAL')
    profile = args.notary_profile
    check(PROFILE_NAME.fullmatch(profile) and not looks_like_credential(profile) and not LONG_TOKEN.fullmatch(profile), 'REFUSED_NOTARY_PROFILE')
    check(re.fullmatch('[0-9a-f]{64}', args.profile_sha256) is not None, 'REFUSED_PROFILE_DIGEST_FORM')
    for name in ('candidate', 'profile', 'limitations', 'out'):
        value = getattr(args, name)
        check(not (looks_like_credential(value) or value.lower().endswith(KEY_FILES)), 'REFUSED_ARGUMENT_CREDENTIAL')
    # The candidate and every written path: never physically inside /Applications or ~/Library.
    # The profile and the limitations file are only read and may be wherever the owner keeps them.
    for name in ('candidate', 'out'):
        try:
            common.refuse_installed_location(getattr(args, name), '--' + name)
        except ValueError:
            raise Failure('REFUSED_LOCATION')
    check(not os.path.lexists(args.out), 'REFUSED_OUT_EXISTS')
    check(Path(args.out).parent.is_dir(), 'REFUSED_OUT_PARENT')
    return match['team']


def guard(argv, app, dmg, signed):
    """One signing call on the App bundle and one on the disk image; never --deep or --force; never into the vendor tree."""
    if argv[0] == CODESIGN and ('--sign' in argv or '-s' in argv):
        target = Path(argv[-1])
        vendor = app / common.VENDOR_DESTINATION
        check(not any(a in ('--deep', '--force', '-f') or a.startswith('--deep') for a in argv), 'GUARD_SIGNING')
        check(not (target == vendor or target.is_relative_to(vendor) or 'Resources/codex' in argv[-1]), 'GUARD_SIGNING')
        check(target in (app, dmg) and target not in signed, 'GUARD_SIGNING')
        signed.append(target)


def shown(argv, out, candidate):
    """The argv as recorded: paths inside the output or the candidate folder as <out>/... or <candidate>/..."""
    result = []
    for arg in argv:
        arg = str(arg)
        if arg.startswith('/') and not common.is_shape(arg, 'tool_path'):
            path = Path(arg)
            if path == out or path.is_relative_to(out):
                arg = '<out>' + ('/' + str(path.relative_to(out)) if path != out else '')
            elif path == candidate or path.is_relative_to(candidate):
                arg = '<candidate>' + ('/' + str(path.relative_to(candidate)) if path != candidate else '')
            else:
                arg = '<elsewhere>'
        result.append(arg)
    return result


class Session:
    """Runs and logs commands. The command log is returnable; raw output goes only to the private folder."""

    def __init__(self, out, runner, environ, paths, candidate, argv_allowed, public_teams):
        self.out, self.runner, self.paths, self.candidate = out, runner, paths, candidate
        self.argv_allowed, self.public_teams = argv_allowed, public_teams
        self.env = {'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'HOME': environ.get('HOME', '/'), 'LANG': 'en_US.UTF-8',
                    'TMPDIR': str(out / 'tmp')}
        self.signed = []
        self.private = common.PrivateWriter(out)

    def run(self, step, argv):
        argv = [str(a) for a in argv]
        guard(argv, self.paths['app'], self.paths['dmg'], self.signed)
        result = self.runner(argv, env=self.env)
        self.private.write(f'step {step} {Path(argv[0]).name} {argv[1] if len(argv) > 1 else ""}',
                           b'argv: ' + json.dumps(argv).encode() + f'\nreturn code: {result.returncode}\n--- stdout\n'.encode()
                           + result.stdout + b'\n--- stderr\n' + result.stderr)
        entry = {'step': str(step), 'argv': shown(argv, self.out, self.candidate), 'returncode': int(result.returncode),
                 'stdout': {'length': len(result.stdout), 'sha256': sha(result.stdout)},
                 'stderr': {'length': len(result.stderr), 'sha256': sha(result.stderr)}}
        common.write_returnable(self.out / 'log.jsonl', entry, self.out, self.public_teams, argv_allowed=self.argv_allowed, append=True)
        return result

    def observe(self, step, name, argv, code, subjects=()):
        """Run one command and apply the one observation rule; a failure stops with `code`."""
        try:
            return observe(name, self.run(step, argv), subjects=subjects)
        except ObservationFailed:
            raise Failure(code)

    def act(self, step, argv, code):
        """An action (no output to read): it counts only when its command returned zero."""
        if self.run(step, argv).returncode != 0:
            raise Failure(code)


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


def open_argv(dmg):
    return [SPCTL, '-a', '-t', 'open', '--context', 'context:primary-signature', '-vv', str(dmg)]


def exec_argv(app):
    return [SPCTL, '-a', '-t', 'exec', '-vv', str(app)]


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
    return argvs + [[XCRUN, 'stapler', 'validate', str(app)], [XCRUN, 'stapler', 'validate', str(dmg)], open_argv(dmg), exec_argv(app)]


def plan(identity, profile, paths, candidate_app, vendor_paths, requirement):
    """The exact commands, in order. Submission ids are filled from each submission's own output."""
    app, dmg, mount = paths['app'], paths['dmg'], paths['mount']
    mounted = mount / common.APP_NAME
    steps = []
    for relative in vendor_paths:
        path = candidate_app / common.VENDOR_DESTINATION / relative
        steps += [(0, common.display_argv(path)), (0, common.entitlements_argv(path))]
    steps.append((4, sign_app_argv(identity, paths['entitlements'], app)))
    steps += [(5, a) for a in verify_app_argvs(app, requirement, vendor_paths)]
    steps.append((6, archive_argv(app, paths['archive'])))
    steps += [(6, a) for a in notarize_argvs(paths['archive'], profile, '<app-submission-id>')]
    steps += [(7, a) for a in staple_argvs(app)]
    steps += [(8, a) for a in verify_app_argvs(app, requirement, vendor_paths)]
    steps += [(9, [HDIUTIL, 'create', '-volname', common.VOLUME_NAME, '-srcfolder', str(paths['staging']), '-format', 'UDZO', str(dmg)]),
              (9, sign_dmg_argv(identity, dmg)), (9, [CODESIGN, '--verify', '--strict', '--verbose=4', str(dmg)]), (9, common.display_argv(dmg))]
    steps += [(10, a) for a in notarize_argvs(dmg, profile, '<disk-image-submission-id>')]
    steps += [(11, a) for a in staple_argvs(dmg)]
    steps += [(12, open_argv(dmg)), (12, attach_argv(dmg, mount)), (12, exec_argv(mounted)), (12, [HDIUTIL, 'detach', str(mount)]),
              (13, attach_argv(dmg, mount))]
    steps += [(13, a) for a in record_argvs(mounted, dmg, vendor_paths)]
    steps.append((13, [HDIUTIL, 'detach', str(mount)]))
    return steps


def sign(args, *, runner=common.system_runner, environ=None, host=None, now=None):
    """The signing run. Raises Failure (a fixed reason) on any failed step; returns the result written."""
    environ = dict(os.environ if environ is None else environ)
    host = host or (platform.system(), platform.machine())
    team = refusals(args, environ, host)
    try:
        candidate, candidate_app, binding, requirement = common.load_candidate(args.candidate)
    except (ValueError, OSError, KeyError):
        raise Failure('REFUSED_CANDIDATE')
    check(binding['developer_id_team_identifier'] == team, 'REFUSED_TEAM')
    limitations = Path(args.limitations).read_bytes()
    check(sha(limitations) == candidate['limitations']['sha256'], 'REFUSED_LIMITATIONS')
    profile_raw = Path(args.profile).read_bytes()
    check(sha(profile_raw) == args.profile_sha256, 'REFUSED_PROFILE_BYTES')
    out = Path(os.path.abspath(args.out))
    candidate_dir = inventory.anchored(args.candidate)
    public_teams = {team, common.SUPPLIER_TEAM}
    paths = {'staging': out / 'staging', 'app': out / 'staging' / common.APP_NAME,
             'dmg': out / f'{common.PRODUCT_NAME}-{common.RELEASE["version"]}.dmg', 'mount': out / 'mount',
             'entitlements': out / 'entitlements.plist', 'notary': out / 'notary',
             'archive': out / 'notary' / f'{common.PRODUCT_NAME}-{common.RELEASE["version"]}-app.zip'}
    argv_allowed = {('--sign', args.identity), ('--keychain-profile', args.notary_profile), ('-R', '=' + requirement)}
    vendor_paths = common.macho_paths(candidate['vendor']['inventory'])
    commands = plan(args.identity, args.notary_profile, paths, candidate_app, vendor_paths, requirement)
    if args.dry_run:
        value = {'dry_run': True, 'plan': [{'step': str(s), 'argv': shown(a, out, candidate_dir)} for s, a in commands]}
        common.validate_returnable(value, public_teams, argv_allowed=argv_allowed)
        return value, None

    out.mkdir(mode=0o700)
    session = Session(out, runner, environ, paths, candidate_dir, argv_allowed, public_teams)
    for name in ('tmp', 'notary'):
        common.require_inside(out / name, out, name)
        (out / name).mkdir(mode=0o700)
    app, dmg, mount = paths['app'], paths['dmg'], paths['mount']
    run = session.run

    def write_bytes(path, raw, mode=0o644):
        common.require_inside(path, out, 'a written file')
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, mode)
        with os.fdopen(fd, 'wb') as handle:
            handle.write(raw)
        os.chmod(path, mode)

    # 0. The supplier's signature metadata, read before anything is copied.
    check(vendor_paths, 'S0_NO_MACHO')
    supplier = {}
    for relative in vendor_paths:
        path = candidate_app / common.VENDOR_DESTINATION / relative
        fields = session.observe(0, 'signature', common.display_argv(path), 'S0_SIGNATURE')
        check(fields['team'] == common.SUPPLIER_TEAM and fields['signer_team'] == common.SUPPLIER_TEAM
              and fields['signer_kind'] == 'Developer ID Application' and fields['runtime'] and not fields['adhoc'], 'S0_SIGNATURE')
        entitlements = session.observe(0, 'entitlements', common.entitlements_argv(path), 'S0_ENTITLEMENTS')
        check(not entitlements.get('com.apple.security.get-task-allow') and not entitlements.get('get-task-allow'), 'S0_ENTITLEMENTS')
        supplier[relative] = fields['cdhash']

    # 1. Copy with modes preserved under umask 022, and check the copy equal.
    previous = os.umask(0o022)
    try:
        common.require_inside(paths['staging'], out, 'the staging folder')
        paths['staging'].mkdir(mode=0o755)
        shutil.copytree(candidate_app, app, symlinks=True, copy_function=shutil.copy2)
    finally:
        os.umask(previous)
    check(inventory.compare(inventory.scan(app), candidate['bundle']['inventory'])['equal'], 'S1_COPY')

    # 2. The provisioning profile at Contents/embedded.provisionprofile, mode 0644.
    selected = {'developer_id_team_identifier': team, 'production_bundle_identifier': binding['production_bundle_identifier']}
    try:
        profile = prepare.profile_consistency(profile_raw, args.profile_sha256, selected, now=now)
    except ValueError:
        raise Failure('S2_PROFILE')
    destination = app / 'Contents/embedded.provisionprofile'
    write_bytes(destination, profile_raw)
    check(os.stat(destination).st_mode & 0o7777 == 0o644 and sha(destination.read_bytes()) == args.profile_sha256, 'S2_PLACED')

    # 3. Entitlements from the binding: exactly the two keys.
    entitlements = {common.APP_ID_KEY: team + '.' + binding['production_bundle_identifier'], common.TEAM_KEY: team}
    check(profile['application_identifier'] == entitlements[common.APP_ID_KEY], 'S3_APP_ID')
    write_bytes(paths['entitlements'], plistlib.dumps(entitlements, sort_keys=True))

    # 4. One signing call, on the bundle path.
    session.act(4, sign_app_argv(args.identity, paths['entitlements'], app), 'S4_SIGN')

    def verify_app(n, allowed_extra):
        session.observe(n, 'verify', [CODESIGN, '--verify', '--deep', '--strict', '--verbose=4', app], f'S{n}_DEEP', [app])
        session.observe(n, 'requirement', [CODESIGN, '--verify', '--strict', '--verbose=4', '-R', '=' + requirement, app],
                        f'S{n}_REQUIREMENT', [app])
        fields = session.observe(n, 'signature', common.display_argv(app), f'S{n}_DISPLAY')
        check(fields['runtime'] and not fields['adhoc'] and fields['team'] == team and fields['signer_team'] == team
              and fields['identifier'] == binding['production_bundle_identifier'] and fields['leaf_authority'] == args.identity, f'S{n}_SIGNER')
        signed_entitlements = session.observe(n, 'entitlements', common.entitlements_argv(app), f'S{n}_ENTITLEMENTS')
        check(signed_entitlements == entitlements, f'S{n}_ENTITLEMENTS')
        compared = inventory.compare(inventory.scan(app), candidate['bundle']['inventory'])
        check(compared['differing'] == ['Contents/MacOS/' + common.MAIN_EXECUTABLE] and not compared['missing']
              and set(compared['extra']) == allowed_extra and compared['root_mode_equal'], f'S{n}_INVENTORY')
        check(inventory.compare(inventory.scan(app / common.VENDOR_DESTINATION), candidate['vendor']['inventory'])['equal'], f'S{n}_VENDOR')
        for relative in vendor_paths:
            shown_fields = session.observe(n, 'signature', common.display_argv(app / common.VENDOR_DESTINATION / relative), f'S{n}_CDHASH')
            check(shown_fields['cdhash'] == supplier[relative], f'S{n}_CDHASH')

    def notarize(n, submitted, kind):
        """Submit, wait, fetch the log; require Accepted, an explicit issues list that is empty and this exact digest."""
        submitted_sha256 = sha(submitted.read_bytes())
        result = session.observe(n, 'submit', submit_argv(submitted, args.notary_profile), f'S{n}_SUBMIT')
        check(result['status'] == 'Accepted', f'S{n}_STATUS')
        fetched = session.run(n, log_argv(result['id'], args.notary_profile))
        try:
            log = observe('notary_log', fetched)
        except ObservationFailed:
            raise Failure(f'S{n}_LOG')
        check(log['status'] == 'Accepted', f'S{n}_LOG_STATUS')
        check(log['issue_count'] == 0, f'S{n}_ISSUES')
        check(log['job'] == result['id'], f'S{n}_JOB')
        check(log['sha256'] == submitted_sha256 and sha(submitted.read_bytes()) == submitted_sha256, f'S{n}_DIGEST')
        # The raw log went to the private folder with the command's output; the returnable summary
        # holds only selected, validated fields, and the raw log's digest computed in memory.
        summary = {'job': log['job'], 'status': log['status'], 'sha256': log['sha256'], 'issue_count': log['issue_count'],
                   'original_log_sha256': sha(fetched.stdout)}
        name = f'notary/{kind}-notarization.json'
        common.write_returnable(out / name, summary, out, public_teams)
        entry = {'summary': name, 'submitted_sha256': submitted_sha256}
        if submitted.is_relative_to(paths['notary']):
            entry['submitted'] = str(submitted.relative_to(out))
        return entry

    def staple(n, target):
        session.observe(n, 'staple', [XCRUN, 'stapler', 'staple', target], f'S{n}_STAPLE', [target])
        session.observe(n, 'validate', [XCRUN, 'stapler', 'validate', target], f'S{n}_VALIDATE', [target])

    def detach(n, code):
        session.act(n, [HDIUTIL, 'detach', mount], code)

    # 5. Verify the signed App, and keep its inventory: the App as signed.
    verify_app(5, SIGNED_EXTRA)
    signed_tree = inventory.scan(app)
    signed_vendor = inventory.scan(app / common.VENDOR_DESTINATION)

    # 6. Notarize the App: an archive of it in the output; the bundle must not change.
    before = inventory.scan(app)
    common.require_inside(paths['archive'], out, 'the App archive')
    session.act(6, archive_argv(app, paths['archive']), 'S6_ARCHIVE')
    check(paths['archive'].is_file() and not paths['archive'].is_symlink(), 'S6_ARCHIVE')
    check(inventory.compare(inventory.scan(app), before)['equal'], 'S6_ARCHIVE_CHANGED')
    notarizations = {'app': notarize(6, paths['archive'], 'app')}

    # 7. Staple and validate the App: the ticket is the only difference from the App as signed.
    staple(7, app)
    compared = inventory.compare(inventory.scan(app), signed_tree)
    check(not compared['differing'] and not compared['missing'] and compared['extra'] == [record.STAPLED_TICKET]
          and compared['root_mode_equal'], 'S7_ONLY_TICKET')
    check(inventory.compare(inventory.scan(app / common.VENDOR_DESTINATION), signed_vendor)['equal'], 'S7_VENDOR')
    # 8. Verify the stapled App again. Nothing writes into the bundle after this.
    verify_app(8, STAPLED_EXTRA)
    stapled_tree = inventory.scan(app)

    # 9. The disk image: the stapled App and the limitations, signed with a timestamp.
    write_bytes(paths['staging'] / common.LIMITATIONS_IN_IMAGE, limitations)
    common.require_inside(dmg, out, 'the disk image')
    session.act(9, [HDIUTIL, 'create', '-volname', common.VOLUME_NAME, '-srcfolder', paths['staging'], '-format', 'UDZO', dmg], 'S9_CREATE')
    check(dmg.is_file() and not dmg.is_symlink(), 'S9_CREATE')
    session.act(9, sign_dmg_argv(args.identity, dmg), 'S9_SIGN')
    session.observe(9, 'verify', [CODESIGN, '--verify', '--strict', '--verbose=4', dmg], 'S9_VERIFY', [dmg])
    image = session.observe(9, 'signature', common.display_argv(dmg), 'S9_DISPLAY')
    check(image['team'] == team and image['signer_team'] == team and image['leaf_authority'] == args.identity, 'S9_DISPLAY')
    check(inventory.compare(inventory.scan(app), stapled_tree)['equal'], 'S9_APP_CHANGED')

    # 10. Notarize the disk image; 11. staple and validate it.
    notarizations['disk_image'] = notarize(10, dmg, 'disk-image')
    staple(11, dmg)

    # 12. Gatekeeper on the disk image, and on the App from a read-only mount.
    session.observe(12, 'assessment', open_argv(dmg), 'S12_OPEN', [dmg])
    common.require_inside(mount, out, 'the mount point')
    mount.mkdir(mode=0o700)
    session.act(12, attach_argv(dmg, mount), 'S12_ATTACH')
    try:
        mounted = mount / common.APP_NAME
        check(inventory.compare(inventory.scan(mounted), stapled_tree)['equal'], 'S12_MOUNTED')
        check((mount / common.LIMITATIONS_IN_IMAGE).read_bytes() == limitations, 'S12_LIMITATIONS')
        session.observe(12, 'assessment', exec_argv(mounted), 'S12_EXEC', [mounted])
    except BaseException:
        run(12, [HDIUTIL, 'detach', mount])  # clean-up while already stopping; its output is in the command log
        raise
    detach(12, 'S12_DETACH')

    # 13. The record, read from the package itself, built in memory; written only after the last
    # observation succeeded and the disk image detached.
    session.act(13, attach_argv(dmg, mount), 'S13_ATTACH')
    try:
        identity_record = record.build_record(dmg=dmg, app=mount / common.APP_NAME, run=lambda argv: run(13, argv), candidate=candidate,
                                              notarizations=notarizations, signed_tree=signed_tree, record_dir=out,
                                              public_teams=public_teams, publisher_team=team)
    except record.RecordFailed as failed:
        run(13, [HDIUTIL, 'detach', mount])
        error = Failure('S13_OBSERVATION')
        error.failures = failed.failures
        raise error
    except BaseException:
        run(13, [HDIUTIL, 'detach', mount])
        raise
    detach(13, 'S13_DETACH')
    digest = common.write_returnable(out / 'PACKAGE_IDENTITY.json', identity_record, out, public_teams)
    shutil.rmtree(out / 'tmp', ignore_errors=True)
    summary = {'result': 'complete', 'package': dmg.name, 'package_sha256': sha(dmg.read_bytes()), 'record': 'PACKAGE_IDENTITY.json',
               'record_sha256': digest, 'installed': False,
               'notarization': {k: {'summary': v['summary'], 'submitted_sha256': v['submitted_sha256']} for k, v in notarizations.items()}}
    common.write_returnable(out / 'RESULT.json', summary, out, public_teams)
    return summary, public_teams


def parser():
    p = common.FixedParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--identity', required=True, help='"Developer ID Application: <name> (<TEAMID>)" as in your keychain')
    p.add_argument('--notary-profile', required=True, help='the notarytool keychain profile name you stored')
    p.add_argument('--candidate', required=True, help='the build output folder holding CANDIDATE.json (not in /Applications or ~/Library)')
    p.add_argument('--profile', required=True, help='the Developer ID provisioning profile file; only read, it may be wherever you keep it')
    p.add_argument('--profile-sha256', required=True)
    p.add_argument('--limitations', required=True,
                   help='docs/RELEASE_LIMITATIONS_4.0.0.md of the candidate source; only read, it may be wherever you keep it')
    p.add_argument('--out', required=True, help='a new folder, not in /Applications or ~/Library, for everything this run writes')
    p.add_argument('--dry-run', action='store_true', help='print the exact plan and run nothing')
    return p


def main(argv=None, *, stdout=None, stderr=None, **kw):
    stdout, stderr = stdout or sys.stdout, stderr or sys.stderr
    args = parser().parse_args(argv)
    out = Path(os.path.abspath(args.out))
    existed = os.path.lexists(out)
    try:
        result, public_teams = sign(args, **kw)
    except BaseException as error:  # every failure, interruption included, is a STOP with a fixed reason
        if isinstance(error, SystemExit):
            raise
        stop = error if isinstance(error, Failure) else Failure('INTERRUPTED' if isinstance(error, KeyboardInterrupt) else 'UNEXPECTED')
        print('STOP: ' + stop.reason, file=stderr)
        if not existed and out.is_dir():
            try:
                if not isinstance(error, Failure):
                    common.PrivateWriter(out).write('trace', ''.join(traceback.format_exception(error)))
                value = {'result': 'stopped', 'reason_code': stop.code, 'reason': stop.reason,
                         'failed_observations': getattr(stop, 'failures', []),
                         'private_folder': common.PRIVATE_FOLDER}  # named only; never opened or examined
                common.write_returnable(out / 'STOPPED.json', value, out, set())
            except BaseException:
                pass
        return 3
    print(json.dumps(result, indent=2), file=stdout)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
