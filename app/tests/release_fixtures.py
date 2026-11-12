"""Invented release material and a stand-in for Apple's tools; nothing here signs, notarizes or reads a keychain."""
import datetime
import importlib.util
import json
import os
from pathlib import Path
import plistlib
import shutil
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]


def release(name):
    key = 'chirality_release_' + name
    if key not in sys.modules:
        spec = importlib.util.spec_from_file_location(key, ROOT / 'app/packaging/release' / (name + '.py'))
        module = importlib.util.module_from_spec(spec); sys.modules[key] = module; spec.loader.exec_module(module)
    return sys.modules[key]


common = release('common')
sha = common.sha
Result = common.Result
TEAM = '8A7JL35U4S'  # the publisher team already public in app/src-tauri/src/capture_seal_keychain.rs
IDENTITY = 'Developer ID Application: Invented Publisher (8A7JL35U4S)'
NOTARY = 'invented-notary-profile'
REQUIREMENT = ('anchor apple generic and identifier com.chirality.app and certificate 1[field.1.2.840.113635.100.6.2.6] '
               'and certificate leaf[field.1.2.840.113635.100.6.1.13] and certificate leaf[subject.OU] = 8A7JL35U4S')
LIMITATIONS = b'# Invented limitations\n\n- LIM-001 key rotation is unavailable.\n'


def macho(flags=common.CS_ADHOC | common.CS_LINKER_SIGNED, cms=False, payload=b''):
    """A thin arm64 Mach-O with one LC_CODE_SIGNATURE; never executable code."""
    header_size, command = 32, 16
    body = b'INVENTED; DO NOT EXECUTE\x00' + payload
    dataoff = header_size + command + len(body)
    dataoff += (-dataoff) % 16
    cd = struct.pack('>IIIIIIIIIBBBBI', 0xfade0c02, 44, 0x20400, flags, 0, 0, 0, 0, 0, 32, 0, 0, 12, 0)[:44]
    blobs = [(0, cd)]
    if cms:
        blobs.append((0x10000, struct.pack('>II', 0xfade0b01, 12) + b'CMS!'))
    index_size = 12 + 8 * len(blobs)
    offsets, cursor = [], index_size
    for _, blob in blobs:
        offsets.append(cursor); cursor += len(blob)
    superblob = struct.pack('>III', 0xfade0cc0, cursor, len(blobs))
    superblob += b''.join(struct.pack('>II', kind, at) for (kind, _), at in zip(blobs, offsets))
    superblob += b''.join(blob for _, blob in blobs)
    header = struct.pack('<IiiIIIII', 0xfeedfacf, 0x0100000c, 0, 2, 1, command, 0, 0)
    load = struct.pack('<IIII', 0x1d, command, dataoff, len(superblob))
    raw = header + load + body
    return raw + b'\x00' * (dataoff - len(raw)) + superblob


def vendor_tree(root, pin='9.9.9'):
    root.mkdir()
    for name in ('bin', 'codex-path', 'codex-resources'):
        (root / name).mkdir()
    (root / 'bin/codex').write_bytes(macho(common.CS_RUNTIME, cms=True, payload=b'codex'))
    (root / 'bin/codex').chmod(0o755)
    (root / 'codex-path/rg').write_bytes(macho(common.CS_RUNTIME, cms=True, payload=b'rg'))
    (root / 'codex-path/rg').chmod(0o755)
    (root / 'codex-resources/input.txt').write_bytes(b'INVENTED resource')
    (root / 'codex-package.json').write_text(json.dumps({
        'layoutVersion': 1, 'version': pin, 'target': 'aarch64-apple-darwin', 'variant': 'codex',
        'entrypoint': 'bin/codex', 'resourcesDir': 'codex-resources', 'pathDir': 'codex-path'}))
    return root


def binding_bytes(input_sha256='0' * 64, team=TEAM, requirement=REQUIREMENT):
    return json.dumps({'format': 'publisher-build-binding.s1', 'state': 'selected-production', 'input_sha256': input_sha256,
                       'requirement_sha256': sha(requirement.encode()), 'production_bundle_identifier': 'com.chirality.app',
                       'developer_id_team_identifier': team, 'build_context': {'application_version': '4.0.0',
                       'application_identifier': 'com.chirality.app'}}, separators=(',', ':')).encode()


def info_plist(**changes):
    value = {'CFBundleIdentifier': 'com.chirality.app', 'CFBundleShortVersionString': '4.0.0', 'CFBundleVersion': '4.0.0',
             'LSMinimumSystemVersion': '15.0', 'CFBundleExecutable': 'chirality-app-v4', 'CFBundleName': 'Chirality'}
    value.update(changes)
    return plistlib.dumps(value)


def app_bundle(app, vendor, binding, requirement=REQUIREMENT, limitations=LIMITATIONS, executable=None):
    contents = app / 'Contents'
    (contents / 'MacOS').mkdir(parents=True)
    (contents / 'Info.plist').write_bytes(info_plist())
    exe = contents / 'MacOS/chirality-app-v4'
    exe.write_bytes(executable or macho(payload=binding + b'\x00' + requirement.encode()))
    exe.chmod(0o755)
    resources = contents / 'Resources'
    resources.mkdir()
    shutil.copytree(vendor, resources / 'codex', symlinks=True, copy_function=shutil.copy2)
    (resources / 'workflows/coordinated-knowledge-work').mkdir(parents=True)
    (resources / 'workflows/MANIFEST.json').write_text(json.dumps({'release_subject': 'invented', 'historical_shipped_revisions': [],
        'packages': [{'name': 'coordinated-knowledge-work', 'revision': 'a' * 64}]}))
    (resources / 'workflows/coordinated-knowledge-work/WORKFLOW.md').write_text('invented workflow\n')
    (resources / 'instructions').mkdir()
    (resources / 'instructions/roles.json').write_text('{"roles": []}\n')
    (resources / 'release').mkdir()
    (resources / 'release/LIMITATIONS.md').write_bytes(limitations)
    return app


def candidate(root, *, team=TEAM, limitations=LIMITATIONS):
    """A candidate output as build.py writes it, made from invented material."""
    vendor = vendor_tree(root / 'vendor-input')
    out = root / 'candidate'
    out.mkdir()
    binding = binding_bytes(team=team)
    app = app_bundle(out / 'target/release/bundle/macos' / common.APP_NAME, vendor, binding)
    (out / 'publisher').mkdir()
    files = {}
    for key, name, raw in (('binding', 'publisher-build-binding.s1.json', binding), ('requirement', 'publisher-requirement.txt', REQUIREMENT.encode()),
                           ('projection', 'publisher-build-public-projection.s1.json', b'{"format":"invented projection"}')):
        (out / 'publisher' / name).write_bytes(raw)
        files[key] = {'path': 'publisher/' + name, 'sha256': sha(raw)}
    (out / 'RELEASE_LIMITATIONS_4.0.0.md').write_bytes(limitations)
    info_raw = (app / 'Contents/Info.plist').read_bytes()
    description = {
        'format': common.CANDIDATE_FORMAT, 'source_revision': 'a' * 40, 'pin': '9.9.9', 'expected_manifest': 'b' * 64,
        'build': {'environment_sha256': 'c' * 64},
        'bundle': {'path': str(app.relative_to(out)), 'info_plist_sha256': sha(info_raw),
                   'executable_sha256': sha((app / 'Contents/MacOS/chirality-app-v4').read_bytes()),
                   'inventory': common.tree_entries(common.inventory.scan(app))},
        'vendor': {'inventory': common.tree_entries(common.inventory.scan(app / common.VENDOR_DESTINATION))},
        'publisher': files,
        'limitations': {'source': common.LIMITATIONS_SOURCE, 'sha256': sha(limitations), 'copy': 'RELEASE_LIMITATIONS_4.0.0.md'},
    }
    common.write_returnable(out / common.CANDIDATE_FILE, description, out, {team, common.SUPPLIER_TEAM})
    return out


def tlv(tag, body):
    n = len(body)
    length = bytes([n]) if n < 0x80 else bytes([0x80 | ((n.bit_length() + 7) // 8)]) + n.to_bytes((n.bit_length() + 7) // 8, 'big')
    return bytes([tag]) + length + body


def profile_bytes(team=TEAM, prefix=TEAM, identifier='com.chirality.app'):
    """An invented CMS-shaped Developer ID profile; never Apple-signed."""
    value = {'UUID': '0A1B2C3D-0000-4000-8000-00000000ABCD', 'Platform': ['OSX'], 'ProvisionsAllDevices': True, 'TeamIdentifier': [team],
             'ApplicationIdentifierPrefix': [prefix], 'CreationDate': datetime.datetime(2020, 1, 1),
             'ExpirationDate': datetime.datetime(2099, 1, 1),
             'Entitlements': {'com.apple.application-identifier': prefix + '.' + identifier, 'com.apple.developer.team-identifier': team,
                              'keychain-access-groups': [prefix + '.*']}}
    prep = common.prepare
    encap = tlv(0x30, tlv(0x06, prep.DATA_OID) + tlv(0xa0, tlv(0x04, plistlib.dumps(value))))
    signed = tlv(0x30, tlv(0x02, b'\x01') + tlv(0x31, b'') + encap + tlv(0x31, b'INVENTED signer info'))
    return tlv(0x30, tlv(0x06, prep.SIGNED_DATA_OID) + tlv(0xa0, signed))


DELETE = object()


def submission_id(n):
    return f'{n:08x}-89ab-cdef-0123-456789abcdef'


class FakeApple:
    """Answers codesign, hdiutil, notarytool, stapler and spctl argv with invented outputs and file effects.

    `override` maps a tuple of argv words (all must appear) to a Result returned instead.
    """

    def __init__(self, identity=IDENTITY, team=TEAM):
        self.calls, self.override, self.identity, self.team = [], {}, identity, team
        self.supplier = {}
        self.app_entitlements = None
        self.submit_extra = {}
        self.log_changes = {}
        self.app_entitlements_override = None
        self.submissions = []
        self.ditto_effect = None
        self.spctl_extra = ''
        self.display_extra = ''

    def __call__(self, argv, *, env=None, cwd=None, timeout=None):
        self.calls.append(list(argv))
        for words, result in self.override.items():
            if all(w in argv for w in words):
                answer = result(argv) if callable(result) else result
                if answer is not None:
                    return answer
        if self.ditto_effect and argv[0] == '/usr/bin/ditto':
            self.ditto_effect(Path(argv[-2]))
        tool, rest = argv[0], argv[1:]
        if tool == '/usr/bin/codesign':
            return self.codesign(rest)
        if tool == '/usr/bin/hdiutil':
            return self.hdiutil(rest)
        if tool == '/usr/bin/xcrun' and rest[0] == 'notarytool':
            return self.notarytool(rest[1:])
        if tool == '/usr/bin/xcrun' and rest[0] == 'stapler':
            target = Path(rest[2])
            if rest[1] == 'staple':
                if target.suffix == '.app':
                    (target / 'Contents/CodeResources').write_bytes(b'INVENTED STAPLED TICKET')
                else:
                    with open(target, 'ab') as handle: handle.write(b'STAPLED-TICKET')
                return Result(0, f'Processing: {target}\nThe staple and validate action worked!\n'.encode())
            if target.suffix == '.app' and not (target / 'Contents/CodeResources').is_file():
                return Result(65, b'', b'does not have a ticket stapled to it\n')
            return Result(0, f'Processing: {target}\nThe validate action worked!\n'.encode())
        if tool == '/usr/bin/ditto':
            app, archive = Path(rest[-2]), Path(rest[-1])
            tree = common.inventory.scan(app)
            archive.write_bytes(b'INVENTED-ZIP:' + json.dumps(tree['entries'], sort_keys=True).encode())
            return Result(0)
        if tool == '/usr/sbin/spctl':
            return Result(0, b'', f'{rest[-1]}: accepted\nsource=Notarized Developer ID\norigin=Developer ID Application: Invented{self.spctl_extra}\n'.encode())
        raise AssertionError('unexpected command ' + repr(argv))

    def kind(self, path):
        text = str(path)
        if '/Contents/Resources/codex/' in text:
            return 'vendor'
        if text.endswith('.dmg'):
            return 'dmg'
        if text.endswith('.app'):
            return 'app'
        raise AssertionError('unexpected codesign target ' + text)

    def codesign(self, rest):
        target = Path(rest[-1])
        if '--sign' in rest:
            if self.kind(target) == 'app':
                exe = target / 'Contents/MacOS/chirality-app-v4'
                exe.write_bytes(exe.read_bytes() + b'DEVELOPER-ID-SIGNATURE')
                (target / 'Contents/_CodeSignature').mkdir()
                (target / 'Contents/_CodeSignature/CodeResources').write_bytes(b'invented seal')
                self.app_entitlements = Path(rest[rest.index('--entitlements') + 1]).read_bytes()
            else:
                with open(target, 'ab') as handle: handle.write(b'DMG-SIGNATURE')
            return Result(0)
        if '--verify' in rest:
            return Result(0, b'', f'{target}: valid on disk\n{target}: satisfies its Designated Requirement\n{target}: explicit requirement satisfied\n'.encode())
        kind = self.kind(target)
        if '--entitlements' in rest:
            if kind == 'vendor':
                return Result(0, plistlib.dumps(self.supplier.get(target.name, {}).get('entitlements', {})))
            if kind == 'app':
                return Result(0, self.app_entitlements_override or self.app_entitlements or b'')
            return Result(0, b'')
        if kind == 'vendor':
            facts = {'team': '2DC432GLL2', 'flags': '0x10000(runtime)', 'timestamp': 'Timestamp=Jan 1, 2026 at 00:00:00'}
            facts.update(self.supplier.get(target.name, {}))
            authority = f'Authority=Developer ID Application: OpenAI, L.L.C. ({facts["team"]})'
            cdhash = sha(target.read_bytes())[:40]
            cdhash = facts.get('cdhash', 'CDHash=' + cdhash)
            text = (f'Executable={target}\nIdentifier={target.name}\nCodeDirectory v=20500 size=1 flags={facts["flags"]} hashes=1+1\n'
                    f'{cdhash}\n{authority}\n{facts["timestamp"]}\nTeamIdentifier={facts["team"]}\n')
            return Result(0, b'', text.encode())
        identifier = 'com.chirality.app' if kind == 'app' else 'Chirality-4.0.0'
        flags = '0x10000(runtime)' if kind == 'app' else '0x0(none)'
        text = (f'Executable={target}\nIdentifier={identifier}\nCodeDirectory v=20500 size=1 flags={flags} hashes=1+1\n'
                f'CDHash={"d" * 40}\nAuthority={self.identity}\nAuthority=Developer ID Certification Authority\n'
                f'Timestamp=Jan 1, 2026 at 00:00:00\nTeamIdentifier={self.team}\n{self.display_extra}')
        return Result(0, b'', text.encode())

    def hdiutil(self, rest):
        if rest[0] == 'create':
            staging = Path(rest[rest.index('-srcfolder') + 1])
            tree = common.inventory.scan(staging)
            Path(rest[-1]).write_bytes(b'INVENTED-DMG:' + json.dumps(tree['entries'], sort_keys=True).encode())
            self.staging = staging
            return Result(0, b'created\n')
        if rest[0] == 'attach':
            mount = Path(rest[rest.index('-mountpoint') + 1])
            for child in self.staging.iterdir():
                if child.is_dir():
                    shutil.copytree(child, mount / child.name, symlinks=True, copy_function=shutil.copy2)
                else:
                    shutil.copy2(child, mount / child.name)
            return Result(0, f'/dev/disk9s1\t{mount}\n'.encode())
        if rest[0] == 'detach':
            mount = Path(rest[1])
            for child in list(mount.iterdir()):
                shutil.rmtree(child) if child.is_dir() and not child.is_symlink() else child.unlink()
            return Result(0, b'detached\n')
        raise AssertionError(rest)

    def notarytool(self, rest):
        if rest[0] == 'submit':
            self.submissions.append(Path(rest[1]))
            value = {'id': submission_id(len(self.submissions)), 'status': 'Accepted', 'message': 'Processing complete'}
            value.update(self.submit_extra)
            return Result(0, json.dumps(value).encode())
        if rest[0] == 'log':
            submitted = self.submissions[-1]
            value = {'logFormatVersion': 1, 'jobId': rest[1], 'status': 'Accepted', 'issues': None,
                     'sha256': sha(submitted.read_bytes()), 'archiveFilename': submitted.name}
            value.update(self.log_changes)
            for key in [k for k, v in value.items() if v is DELETE]:
                del value[key]
            return Result(0, json.dumps(value).encode())
        raise AssertionError(rest)


def make_mount_copy(staging, target):
    """A stand-in for the read-only mounted disk image."""
    shutil.copytree(staging, target, symlinks=True, copy_function=shutil.copy2)
    return target
