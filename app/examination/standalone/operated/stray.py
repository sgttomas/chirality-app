#!/usr/bin/env python3
"""Look for remaining candidate processes after a run. It ends nothing and opens nothing. macOS only.

    python3 -B stray.py <the bundle, the path of the .app folder>

A view of an application that is not running starts it through the system's launch service, outside the launcher.
If the build ends by itself during a walk, the next view can do that. The lane runs this from its own shell after
every run, by whatever path the run ended (README.md, step 11). It prints, as JSON, the remaining candidate
processes: every process of this user running the bundle's executable (Contents/MacOS/<CFBundleExecutable>, which
is what the launch service starts), with its parent and start time. That is decided by the file, not by how its
path is spelled: the system is asked for each process's executable path, and that file's device and inode are
compared with the bundle executable's, so a link, another letter case or a relative path does not hide it.

It reads the bundle's Info.plist for the executable's name and nothing else. Exit status 0 when it found none; 1
when it found one or more; 2 when it could not look, including when a process of this user that was still there
could not be asked for its executable, or gave a path that was gone when it was examined.

One kind of process is listed by number and not counted: one for which the system gives no path at all (ENOENT),
which it does for a file that no longer has a name. That is sound only while the bundle's executable has exactly
one name and stays the same file for the whole search. That is an operating condition the lane keeps (README.md,
"The condition of the exception": the identified bundle is not rebuilt, replaced, renamed or given another link from
identification through recovery), not something this search proves. The search only detects a change it can see:
it refuses unless the link count is 1, and compares device, inode, link count, size and modification and change
times (in nanoseconds) before and after the search, exiting 2 on a difference. A file written anew at the same path
differs at least in its change time, even where the file system gives it the inode number of the one removed (seen
on Linux). Equal values do not show that the file was unchanged in between. While the condition
holds, a process running it is running a file with a name, the bundle's own. That the system gives a path for every file that has a name is how
the call is documented and what the third reviewer saw on this host (a hard link removed: the system gave the
surviving name), not something this search proves.

What it does not say: where a process it finds came from (the launcher's App not yet ended, or a start the launcher
did not make, look the same here), or the environment or home it was started with; anything about Codex, which it
does not look for; anything in the real Library (what changed there in places named for the build while the
launcher ran is in the launcher's record); a process that started and ended before it listed; a process of another
user. On any system but macOS it looks for nothing and exits 2.
"""
import ctypes
import errno
import json
import os
import plistlib
import subprocess
import sys

_PROC = None
NO_PATH = object()


def executable_of(pid):
    """The system's path for a process's executable; None when the process has gone; NO_PATH when the system gives
    none because the file it runs has been removed (ENOENT). Other failures raise."""
    global _PROC
    if _PROC is None:
        _PROC = ctypes.CDLL('/usr/lib/libproc.dylib', use_errno=True)
    buffer = ctypes.create_string_buffer(4096)
    if _PROC.proc_pidpath(ctypes.c_int(pid), buffer, ctypes.c_uint32(len(buffer))) <= 0:
        code = ctypes.get_errno()
        if code == errno.ESRCH:
            return None
        if code == errno.ENOENT:
            return NO_PATH
        raise OSError(code, f'the executable of process {pid} could not be asked for')
    return os.fsdecode(buffer.value)


def listing():
    """One line for each process of this user: number, parent, start time (five words)."""
    done = subprocess.run(['/bin/ps', '-U', str(os.getuid()), '-o', 'pid=,ppid=,lstart='],
                          capture_output=True, text=True, env={'PATH': '/bin:/usr/bin'})
    if done.returncode != 0:
        raise OSError('the process listing failed')
    return done.stdout.splitlines()


def fingerprint(info):
    """What the two looks at the bundle's executable compare. Equal does not prove the same, unchanged file."""
    return (info.st_dev, info.st_ino, info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def processes(executable, lines=None, path_of=None):
    """Every process of this user whose executable is the same file as the given one; and, by number, those for
    which the system gives no path (see the module's docstring for why those are not that file, and when)."""
    path_of, target, found, no_path = path_of or executable_of, os.stat(executable), [], []
    if target.st_nlink != 1:
        raise OSError(f"the bundle's executable has {target.st_nlink} names, not one")
    for line in listing() if lines is None else lines:
        parts = line.split()
        if len(parts) != 7 or not parts[0].isdigit():
            continue
        path = path_of(int(parts[0]))
        if path is None:
            continue  # gone since the listing
        if path is NO_PATH:
            no_path.append(int(parts[0]))
            continue
        try:
            info = os.stat(path)
        except FileNotFoundError:  # a path that is gone by now says nothing of which file the process runs
            raise OSError(f'process {parts[0]} gave an executable path that was gone when it was examined')
        if (info.st_dev, info.st_ino) == (target.st_dev, target.st_ino):
            found.append({'pid': int(parts[0]), 'parent': int(parts[1]), 'started': ' '.join(parts[2:7]), 'executable': path})
    if fingerprint(os.stat(executable)) != fingerprint(target):
        raise OSError("the bundle's executable changed during the search")
    return found, no_path


def on_macos():
    return sys.platform == 'darwin'


def main(argv):
    if len(argv) != 2 or not argv[1].startswith('/') or not argv[1].endswith('.app'):
        print('usage: stray.py <bundle .app path>', file=sys.stderr)
        return 2
    bundle = argv[1]
    if not on_macos():
        print(json.dumps({'error': 'this search is made on macOS only; nothing was looked for'}), file=sys.stderr)
        return 2
    try:
        with open(os.path.join(bundle, 'Contents', 'Info.plist'), 'rb') as stream:
            executable = plistlib.load(stream)['CFBundleExecutable']
        if not isinstance(executable, str) or not executable or '/' in executable:
            raise KeyError('CFBundleExecutable is not a plain name')
        running, no_path = processes(os.path.join(bundle, 'Contents', 'MacOS', executable))
    except (OSError, KeyError, plistlib.InvalidFileException) as error:
        print(json.dumps({'error': f'{type(error).__name__}: {error}'}), file=sys.stderr)
        return 2
    print(json.dumps({'remaining_candidate_processes': running, 'processes_whose_executable_was_removed': no_path}, indent=1))
    return 1 if running else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
