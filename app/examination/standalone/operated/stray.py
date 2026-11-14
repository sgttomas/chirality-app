#!/usr/bin/env python3
"""Look for remaining candidate processes after a run. It ends nothing and opens nothing. macOS only.

    python3 -B stray.py <the bundle, the path of the .app folder> [--also-under <folder>]

A view of an application that is not running starts it through the system's launch service, outside the launcher.
If the build ends by itself during a walk, the next view can do that. The lane runs this from its own shell after
every run, by whatever path the run ended (README.md, step 11). It prints, as JSON, the remaining candidate
processes: every process of this user running the bundle's executable (Contents/MacOS/<CFBundleExecutable>, which
is what the launch service starts), with its parent and start time. That is decided by the file, not by how its
path is spelled: the system is asked for each process's executable path, and that file's device and inode are
compared with the bundle executable's, so a link, another letter case or a relative path does not hide it.

What it reads of processes, and what it keeps (App Agent 0's bound on reading processes, 14 November 2026). A stray
is exactly a process that has lost its parent, so descent cannot find one. It lists only the numbers of this user's
processes (ps -U <user> -o pid=) and asks the system for each one's executable path by number (libproc's
proc_pidpath, which gives the path and nothing the process was started with: no argument, no environment, nothing it
has open). It KEEPS AND PRINTS ONLY the processes whose executable is the bundle's own (remaining_candidate_processes),
or whose path lies under the candidate's folder or a folder given with --also-under (other_processes_of_ours). Every
other process is discarded unprinted and uncounted. For a kept process only, it then reads its parent and start time.
That is the least that can show that no process of ours was left. A process for which the system gives no path is
discarded too: while the operating condition below holds, it is not running the bundle's executable.

It reads the bundle's Info.plist for the executable's name and nothing else. Exit status 0 when it found none; 1
when it found one or more; 2 when it could not look, including when a process of this user that was still there
could not be asked for its executable, or gave a path that was gone when it was examined.

One kind of process is discarded without being examined further: one for which the system gives no path at all
(ENOENT), which it does for a file that no longer has a name. That is sound only while the bundle's executable has exactly
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
    """The numbers of this user's processes, numbers only."""
    done = subprocess.run(['/bin/ps', '-U', str(os.getuid()), '-o', 'pid='],
                          capture_output=True, text=True, env={'PATH': '/bin:/usr/bin'})
    if done.returncode != 0:
        raise OSError('the process listing failed')
    return done.stdout.splitlines()


def started(pid):
    """The parent and start time of one kept process, or None when it has gone."""
    done = subprocess.run(['/bin/ps', '-o', 'ppid=,lstart=', '-p', str(pid)],
                          capture_output=True, text=True, env={'PATH': '/bin:/usr/bin'})
    parts = done.stdout.split()
    if done.returncode != 0 or len(parts) != 6 or not parts[0].isdigit():
        return None
    return int(parts[0]), ' '.join(parts[1:6])


def fingerprint(info):
    """What the two looks at the bundle's executable compare. Equal does not prove the same, unchanged file."""
    return (info.st_dev, info.st_ino, info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def under(path, folder):
    return folder is not None and os.path.realpath(path).startswith(os.path.realpath(folder).rstrip('/') + '/')


def processes(executable, lines=None, path_of=None, folders=(), started_of=None):
    """The processes of this user whose executable is the same file as the given one, and those whose executable lies
    under one of the given folders. Every other process is discarded unprinted and uncounted."""
    path_of, started_of = path_of or executable_of, started_of or started
    target, found, ours = os.stat(executable), [], []
    if target.st_nlink != 1:
        raise OSError(f"the bundle's executable has {target.st_nlink} names, not one")
    for line in listing() if lines is None else lines:
        parts = line.split()
        if len(parts) != 1 or not parts[0].isdigit():
            continue
        pid = int(parts[0])
        path = path_of(pid)
        if path is None or path is NO_PATH:
            continue  # gone since the listing, or running a file with no name: not the bundle's (module docstring)
        try:
            info = os.stat(path)
        except FileNotFoundError:  # a path that is gone by now says nothing of which file the process runs
            raise OSError('a process gave an executable path that was gone when it was examined')
        bundle_file = (info.st_dev, info.st_ino) == (target.st_dev, target.st_ino)
        if not bundle_file and not any(under(path, folder) for folder in folders if folder):
            continue  # not ours: discarded, unprinted and uncounted
        when = started_of(pid)
        if when is None:
            continue  # gone since its path was asked
        (found if bundle_file else ours).append({'pid': pid, 'parent': when[0], 'started': when[1], 'executable': path})
    if fingerprint(os.stat(executable)) != fingerprint(target):
        raise OSError("the bundle's executable changed during the search")
    return found, ours


def on_macos():
    return sys.platform == 'darwin'


def main(argv):
    also = None
    if len(argv) == 4 and argv[2] == '--also-under' and argv[3].startswith('/'):
        also, argv = argv[3], argv[:2]
    if len(argv) != 2 or not argv[1].startswith('/') or not argv[1].endswith('.app'):
        print('usage: stray.py <bundle .app path> [--also-under <folder>]', file=sys.stderr)
        return 2
    bundle = argv[1]
    # The candidate's folder: <candidate>/target/debug/bundle/macos/<name>.app, else the bundle itself.
    marker = '/target/debug/bundle/macos/'
    candidate = bundle[:bundle.index(marker)] if marker in bundle else bundle
    if not on_macos():
        print(json.dumps({'error': 'this search is made on macOS only; nothing was looked for'}), file=sys.stderr)
        return 2
    try:
        with open(os.path.join(bundle, 'Contents', 'Info.plist'), 'rb') as stream:
            executable = plistlib.load(stream)['CFBundleExecutable']
        if not isinstance(executable, str) or not executable or '/' in executable:
            raise KeyError('CFBundleExecutable is not a plain name')
        running, ours = processes(os.path.join(bundle, 'Contents', 'MacOS', executable), folders=[candidate, also])
    except (OSError, KeyError, plistlib.InvalidFileException) as error:
        print(json.dumps({'error': f'{type(error).__name__}: {error}'}), file=sys.stderr)
        return 2
    print(json.dumps({'remaining_candidate_processes': running, 'other_processes_of_ours': ours}, indent=1))
    return 1 if running or ours else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
