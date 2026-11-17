#!/usr/bin/env python3
"""Start one command so that it outlives the shell that started it.

    python3 -B detached.py <folder for its output> <name> -- <command> [arguments...]
    python3 -B detached.py --recheck <name>.started.json

An agent's shell tool ends the processes it started when a call returns, so a launcher or a watch started with
`&` is gone before the next call. This starts the command in a session of its own, with no input, and its output
in <name>.out and <name>.err in the folder (which must exist; none of its files may exist). It writes
<name>.started.json there with the process number, the command exactly as given, the time and the process's
identity, prints the same, and returns, within about five seconds.

The identity is what the system says of the process it started: its start time (`ps -o lstart=`, to the second),
its parent, its process group and its executable (the system's path for it, and that file's device and inode). It is
read while this starter is still the parent and has not collected the command, so the number cannot yet belong to
any other process, even if the command has already ended: what is read is the process it started. A command started
through a stand-in that replaces itself (a Python found through a shim runs another executable a moment later) is
read until two looks a quarter of a second apart agree, for at most five seconds. Where that is not reached, or the
system could not be asked, or this is not macOS, the started file says "identity_not_established" with the reason,
and nothing may later be signalled by that file.

The recheck, made immediately before a later signal to the recorded number (README.md, steps 8, 10 and 11): it asks
the system again, for that one number only, and exits 0 only when the process with that number now has the recorded
start time, process group and executable file, and its parent is the system's process 1. The parent cannot still be
this starter, which has returned; a process whose parent exits is given to process 1 on macOS, so the parent shows
only that, not which process it is. Exit status 1 when the system says no process has the number (its "no such
process" for the executable's path, ESRCH; a failed listing is never taken for that): nothing is left to signal. 2
when a process has the number but is not the one recorded, which a new process given the number and the recorded
one having run another executable look the same as here; when the file records no identity; or when the system
could not be asked. Only 0 lets a signal follow; 2 is an unresolved process, reported, never signalled. What it does not close: a
number given again within the same second to a process running the same executable in a process group of its own,
which needs the system's process numbers to come round within that second; and the moment between its answer and
the signal, which it narrows to one shell command. It signals nothing.

What it does and does not do. It starts exactly the one command it is given, as a list of arguments: no shell
reads it, nothing is expanded, and nothing else is started. It passes its own environment on to the command and
puts no replacement in its place. It
does not wait for the command, watch it or end it: ending it later is a signal sent to the recorded process
number, and whoever started it is answerable for that. The started file is the record by which something left
running is found.

If the started file cannot be written whole after the command has started, it sends a termination to the command's
process group, and a kill five seconds later if the command itself has not gone; it says whether the command itself
is gone, and the exit status is 3. That is all it can say. A process the command started that left its process
group is not reached, and the App the launcher starts runs in a session of its own; one that outlived the command
is not seen here either. So after exit 3 the operator stops and tells the lane at once, and the lane runs the
stray search (README.md, step 11).
"""
import json
import os
import signal
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stray  # noqa: E402  the system's path for a process's executable, asked of one number (proc_pidpath)

LOOK_APART, LOOKS = 0.25, 20


def look(pid):
    """(start time, parent, process group) of one number. Raises on any result but a listing of it: a failed or
    empty query is not known to mean the number is free, so it is never taken for "gone"."""
    done = subprocess.run(['/bin/ps', '-o', 'lstart=,ppid=,pgid=', '-p', str(pid)],
                          capture_output=True, text=True, env={'PATH': '/bin:/usr/bin'})
    words = done.stdout.split()
    if done.returncode != 0 or len(words) != 7 or not words[5].isdigit() or not words[6].isdigit():
        raise OSError(f'process {pid} could not be asked for its start time, parent and group')
    return ' '.join(words[:5]), int(words[5]), int(words[6])


def identity_now(pid, look_of=None, path_of=None):
    """The process's identity as the system gives it now, or None when the system says no process has the number
    (proc_pidpath: ESRCH). Raises when it could not be asked or gives no path for the executable."""
    look_of, path_of = look_of or look, path_of or stray.executable_of
    path = path_of(pid)  # first: the system's "no such process" (ESRCH) is the one answer taken for gone
    if path is None:
        return None
    seen = look_of(pid)
    if path is stray.NO_PATH:
        raise OSError(f'the system gives no path for the executable of process {pid}')
    info = os.stat(path)
    started, parent, group = seen
    return {'started': started, 'parent': parent, 'group': group, 'executable': path,
            'device': info.st_dev, 'inode': info.st_ino}


def capture(pid, look_of=None, path_of=None, sleep=time.sleep, on_mac=None):
    """The identity of the process this starter has just started and not collected: (identity, None) once two looks
    agree, or (None, the reason)."""
    if not (on_mac if on_mac is not None else sys.platform == 'darwin'):
        return None, 'this is asked on macOS only'
    before = None
    for _ in range(LOOKS):
        try:
            now = identity_now(pid, look_of, path_of)
        except OSError as error:
            return None, f'{type(error).__name__}: {error}'
        if now is None:
            return None, 'the system gave no executable for that number (the command had already ended)'
        if now['parent'] != os.getpid() or now['group'] != pid:
            return None, 'the process was not this starter\'s child leading its own process group'
        if now == before:
            return now, None
        before = now
        sleep(LOOK_APART)
    return None, 'its executable did not stay the same for two looks within five seconds'


def recheck(started, look_of=None, path_of=None):
    """'same', 'gone' or 'not the same', with the reason, for a started file's record. Raises OSError when it could
    not look, and ValueError when the record holds no identity."""
    then = started.get('identity')
    if not isinstance(then, dict) or not isinstance(started.get('pid'), int):
        raise ValueError(started.get('identity_not_established') or 'the started file records no identity')
    now = identity_now(started['pid'], look_of, path_of)
    if now is None:
        return 'gone', 'no process has that number now'
    for field in ('started', 'group', 'device', 'inode'):
        if now[field] != then[field]:
            return 'not the same', f'its {field} is not the one recorded'
    if now['parent'] != 1:
        return 'not the same', 'its parent is not the system\'s process 1, as the starter has returned'
    again = (look_of or look)(started['pid'])
    if again[0] != then['started'] or again[1:] != (1, then['group']):
        return 'not the same', 'it changed while it was asked'
    return 'same', None


def main_recheck(argv, look_of=None, path_of=None):
    try:
        with open(argv[2], encoding='utf-8') as stream:
            started = json.load(stream)
        if not on_macos():
            raise OSError('this is asked on macOS only')
        answer, reason = recheck(started, look_of, path_of)
    except (OSError, ValueError, json.JSONDecodeError, AttributeError) as error:
        print(json.dumps({'answer': 'could not be established', 'reason': f'{type(error).__name__}: {error}'}),
              file=sys.stderr)
        return 2
    print(json.dumps({'pid': started['pid'], 'answer': answer, 'reason': reason}))
    return {'same': 0, 'gone': 1}.get(answer, 2)


def on_macos():
    return sys.platform == 'darwin'


def main(argv):
    if len(argv) == 3 and argv[1] == '--recheck':
        return main_recheck(argv)
    if len(argv) < 5 or argv[3] != '--' or not argv[2] or '/' in argv[2] or argv[2].startswith('.'):
        print('usage: detached.py <folder for its output> <name> -- <command> [arguments...]', file=sys.stderr)
        return 2
    folder, name, command = argv[1], argv[2], argv[4:]
    try:
        paths = [os.path.join(folder, f'{name}.{kind}') for kind in ('out', 'err', 'started.json')]
        handles = [os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600) for path in paths]
    except OSError as error:
        print(json.dumps({'error': f'{type(error).__name__}: the output files could not be created in {folder}'}), file=sys.stderr)
        return 2
    try:
        process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=handles[0], stderr=handles[1],
                                   start_new_session=True, close_fds=True)
    except OSError as error:
        os.write(handles[2], (json.dumps({'not_started': type(error).__name__, 'command': command}) + '\n').encode())
        print(json.dumps({'error': f'{type(error).__name__}: the command could not be started'}), file=sys.stderr)
        return 2
    finally:
        for handle in handles[:2]:
            os.close(handle)
    started = {'pid': process.pid, 'command': command, 'started_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
               'out': paths[0], 'err': paths[1]}
    identity, reason = capture(process.pid)  # before this starter collects it or returns: see the docstring
    if identity is None:
        started['identity_not_established'] = reason
    else:
        started['identity'] = identity
    try:
        publish(handles[2], (json.dumps(started, indent=1) + '\n').encode())
    except OSError as error:  # the command is ended; what it started outside its group is for the stray search
        gone = end_command(process)
        print(json.dumps({'error': f'{type(error).__name__}: the started file could not be written whole',
                          'pid': process.pid, 'command_gone': gone,
                          'next': 'stop, and tell the lane now: it runs the stray search (README.md, step 11)'}), file=sys.stderr)
        return 3
    print(json.dumps(started))
    return 0


def publish(handle, data):
    """All of the data, synced, or an error; never part of it taken for the whole."""
    try:
        view = memoryview(data)
        while view:
            written = os.write(handle, view)
            if written <= 0:
                raise OSError('nothing was written')
            view = view[written:]
        os.fsync(handle)
    finally:
        os.close(handle)


def end_command(process):
    """Signal the command's process group; True when the command itself is known to have gone. Says nothing of any
    other process."""
    for sent in (signal.SIGTERM, signal.SIGKILL):
        try:
            os.killpg(process.pid, sent)
        except ProcessLookupError:
            pass
        try:
            process.wait(timeout=5)
            return True
        except subprocess.TimeoutExpired:
            continue
    return False


if __name__ == '__main__':
    sys.exit(main(sys.argv))
