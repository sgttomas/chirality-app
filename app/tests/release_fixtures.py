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


class MemoryWriter:
    """An injected private writer for tests: it keeps what it was handed in memory, so no test needs
    the private folder at all. Tests assert through `handed`."""

    instances = []

    def __init__(self, root):
        self.root, self.handed = root, []
        MemoryWriter.instances.append(self)

    def write(self, label, raw):
        self.handed.append((label, raw if isinstance(raw, bytes) else str(raw).encode()))
        return None, None, None


def install_private_folder_guard(folder_name):
    """A convention for this test suite, not an enforcement: in this test process, refuse the common ways
    of looking inside a folder named as the private output folder.

    What it catches, for any path (text or bytes, as given or resolved) with a component of that name:
    listing (os.listdir, os.scandir, os.walk, pathlib iteration, glob.glob, glob.iglob, Path.glob and
    Path.rglob),
    every os.open other than a create-only write (O_WRONLY with O_CREAT and O_EXCL), every built-in
    or io open that can read (any mode without w, a or x, and any mode with +), and starting a
    subprocess whose arguments name the folder.

    What it does not catch: a descriptor-relative open (dir_fd) whose name alone does not contain the
    folder, code holding a reference to one of these functions taken before the guard was installed,
    C extensions and other processes started without these functions, and a path that reaches the
    folder through a name that resolves to it only after a later rename. The rule it supports is
    unchanged: no tool, test or agent of ours opens, lists or walks that folder.
    """
    import builtins, io, subprocess
    if getattr(os, '_chirality_private_guard', False):
        return
    def private(path):
        if isinstance(path, int):
            return False
        try:
            text = os.fsdecode(os.fspath(path))
        except TypeError:
            return False
        return folder_name in Path(text).parts or folder_name in Path(os.path.realpath(text)).parts
    def refuse(path):
        raise PermissionError('test guard: the private folder is never read or listed')
    real = {'listdir': os.listdir, 'scandir': os.scandir, 'open': os.open, 'io_open': io.open, 'walk': os.walk,
            'popen_init': subprocess.Popen.__init__}
    def listdir(path='.'):
        if private(path): refuse(path)
        return real['listdir'](path)
    def scandir(path='.'):
        if private(path): refuse(path)
        return real['scandir'](path)
    def os_open(path, flags, *args, **kw):
        create_only = (flags & os.O_WRONLY) and (flags & os.O_CREAT) and (flags & os.O_EXCL) and not (flags & os.O_RDWR)
        if private(path) and not create_only: refuse(path)
        return real['open'](path, flags, *args, **kw)
    def io_open(file, mode='r', *args, **kw):
        reading = '+' in mode or not any(c in mode for c in 'wax')
        if private(file) and reading: refuse(file)
        return real['io_open'](file, mode, *args, **kw)
    def walk(top, *args, **kw):
        if private(top): refuse(top)
        return real['walk'](top, *args, **kw)
    def popen_init(self, args, *rest, **kw):
        items = [args] if isinstance(args, (str, bytes, os.PathLike)) else list(args)
        if any(isinstance(a, (str, bytes, os.PathLike)) and folder_name in os.fsdecode(os.fspath(a)) for a in items): refuse(args)
        return real['popen_init'](self, args, *rest, **kw)
    # glob and pathlib's glob may hold their own reference to os.scandir, so they are wrapped by name too.
    import glob as glob_module
    real.update({'glob': glob_module.glob, 'iglob': glob_module.iglob, 'path_glob': Path.glob, 'path_rglob': Path.rglob})
    def globbed(name):
        def wrapper(pathname, *args, root_dir=None, **kw):
            if private(pathname) or (root_dir is not None and private(root_dir)): refuse(pathname)
            return real[name](pathname, *args, root_dir=root_dir, **kw)
        return wrapper
    def path_globbed(name):
        def wrapper(self, pattern, *args, **kw):
            if private(self) or private(self / pattern): refuse(self)
            return real[name](self, pattern, *args, **kw)
        return wrapper
    glob_module.glob, glob_module.iglob = globbed('glob'), globbed('iglob')
    Path.glob, Path.rglob = path_globbed('path_glob'), path_globbed('path_rglob')
    os.listdir, os.scandir, os.open, io.open, builtins.open, os.walk = listdir, scandir, os_open, io_open, io_open, walk
    subprocess.Popen.__init__ = popen_init
    os._chirality_private_guard = True


def release(name):
    key = 'chirality_release_' + name
    if key not in sys.modules:
        spec = importlib.util.spec_from_file_location(key, ROOT / 'app/packaging/release' / (name + '.py'))
        module = importlib.util.module_from_spec(spec); sys.modules[key] = module; spec.loader.exec_module(module)
    return sys.modules[key]


common = release('common')
install_private_folder_guard(common.PRIVATE_FOLDER)
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


