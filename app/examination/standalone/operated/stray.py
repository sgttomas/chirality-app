#!/usr/bin/env python3
"""Look for a start of the candidate that the launcher did not make. It ends nothing and opens nothing.

    python3 -B stray.py <the bundle, the path of the .app folder> <bundle identifier>

A view of an application that is not running starts it through the system's launch service, outside the launcher.
If the build ends by itself during a walk, the next view can do that. The lane runs this from its own shell after
a run, once the launcher's App is confirmed gone (README.md, steps 10 and 11), so any process it finds is one the
launcher did not leave. It prints, as JSON:

- every process of this user running the bundle's executable (Contents/MacOS/<CFBundleExecutable>, which is what
  the launch service starts), with its parent and start time. That is decided by the file, not by how its path is
  spelled: the system is asked for each process's executable path, and that file's device and inode are compared
  with the bundle executable's, so a link, another letter case or a relative path does not hide it;
- by name only, every entry the launcher's own comparison would watch for this build (launch.py, WATCHED and
  watched_name) in the real Library's places.

It reads the bundle's Info.plist for the executable's name, lists those places, and reads nothing in them. Exit
status 0 when it looked everywhere and found neither; 1 when it found either; 2 when it could not look, including
when one of those places could not be listed or a process of this user that was still there could not be asked
for its executable.

What it does not see: a process that started and ended before it listed; a process of another user. It says
nothing of the environment or home a process it finds was started with.
"""
import ctypes
import errno
import json
import os
from pathlib import Path
import plistlib
import pwd
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import launch  # noqa: E402  (the launcher's watched places and its rule for a name)

_PROC = None


def executable_of(pid):
    """The system's path for a process's executable, or None when the process has gone. Other failures raise."""
    global _PROC
    if _PROC is None:
        _PROC = ctypes.CDLL('/usr/lib/libproc.dylib', use_errno=True)
    buffer = ctypes.create_string_buffer(4096)
    if _PROC.proc_pidpath(ctypes.c_int(pid), buffer, ctypes.c_uint32(len(buffer))) <= 0:
        code = ctypes.get_errno()
        if code == errno.ESRCH:
            return None
        raise OSError(code, f'the executable of process {pid} could not be asked for')
    return os.fsdecode(buffer.value)


def listing():
    """One line for each process of this user: number, parent, start time (five words)."""
    done = subprocess.run(['/bin/ps', '-U', str(os.getuid()), '-o', 'pid=,ppid=,lstart='],
                          capture_output=True, text=True, env={'PATH': '/bin:/usr/bin'})
    if done.returncode != 0:
        raise OSError('the process listing failed')
    return done.stdout.splitlines()


def processes(executable, lines=None, path_of=executable_of):
    """Every process of this user whose executable is the same file as the given one."""
    target, found = os.stat(executable), []
    for line in listing() if lines is None else lines:
        parts = line.split()
        if len(parts) != 7 or not parts[0].isdigit():
            continue
        path = path_of(int(parts[0]))
        if path is None:
            continue  # gone since the listing
        try:
            info = os.stat(path)
        except FileNotFoundError:
            continue  # its executable has been removed; it is not a file of the bundle now
        if (info.st_dev, info.st_ino) == (target.st_dev, target.st_ino):
            found.append({'pid': int(parts[0]), 'parent': int(parts[1]), 'started': ' '.join(parts[2:7]), 'executable': path})
    return found


def library_entries(identifier, executable, library):
    found, not_listed = [], []
    for place in ('',) + launch.WATCHED:
        folder = library / place if place else library
        try:
            names = sorted(os.listdir(folder))
        except FileNotFoundError:
            continue
        except OSError as error:
            not_listed.append(f'{folder} ({type(error).__name__})')
            continue
        found += [str(folder / name) for name in names if launch.watched_name(name, identifier, executable)]
    return found, not_listed


def real_library():
    """The account's real Library, from the account database, never from HOME."""
    return Path(os.path.realpath(pwd.getpwuid(os.getuid()).pw_dir)) / 'Library'


def main(argv):
    if len(argv) != 3 or not argv[1].startswith('/') or not argv[1].endswith('.app'):
        print('usage: stray.py <bundle .app path> <bundle identifier>', file=sys.stderr)
        return 2
    bundle, identifier = argv[1], argv[2]
    library = real_library()
    try:
        with open(os.path.join(bundle, 'Contents', 'Info.plist'), 'rb') as stream:
            executable = plistlib.load(stream)['CFBundleExecutable']
        if not isinstance(executable, str) or not executable or '/' in executable:
            raise KeyError('CFBundleExecutable is not a plain name')
        running = processes(os.path.join(bundle, 'Contents', 'MacOS', executable))
        entries, not_listed = library_entries(identifier, executable, library)
    except (OSError, KeyError, plistlib.InvalidFileException) as error:
        print(json.dumps({'error': f'{type(error).__name__}: {error}'}), file=sys.stderr)
        return 2
    print(json.dumps({'processes_running_the_bundle_executable': running, 'entries_named_for_the_build_in_the_real_library': entries,
                      'places_that_could_not_be_listed': not_listed}, indent=1))
    if running or entries:
        return 1
    return 2 if not_listed else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
