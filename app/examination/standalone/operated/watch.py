#!/usr/bin/env python3
"""Keep a small file that says whether one process is running and what child processes it has.

    python3 -B watch.py <process number> <file to keep>

The operator starts this from the shell once the App's process is confirmed, and leaves it running. Once a second
it rewrites the file, whole, with the process number, the time, whether the process is running, its executable as
the system reports it, and its child processes. When the process has gone it writes that and ends. walk.mjs reads
the file, because the node runtime it runs in cannot ask the system about a process. It signals nothing and starts
nothing but the system's own process listing.

"Running" means: the number is in the listing, the process has not exited (one that has exited and not yet been
collected is not running), and its executable is the one first seen at that number, so another program that later
gets the same number is not taken for it.

What it reads (App Agent 0's bound on reading processes, 14 November 2026: nothing a process was started with, its
arguments or its environment, and nothing it has open, is read for any process, and nothing is kept about a process
that is not the watched one or its child). Every process's number and parent, numbers only, to find the children.
Then, for the watched process and its children only: the process state and the accounting name (ps -o stat=,ucomm=;
ucomm is the accounting name, cut at 16 characters, not argv[0], which comm would give). And for the watched process
only: its executable's path, asked of the system by process number (libproc's proc_pidpath on macOS, the
/proc/<pid>/exe link on Linux), which gives the path and nothing the process was started with.

Limits. It is a sample taken once a second, not custody: the process can end between two samples. Its children
are those whose parent is that process at the sample; a process it started that has since been given another
parent, or that came and went between samples, is not seen.
"""
import ctypes
import json
import os
import subprocess
import sys
import time

ENV = {'PATH': '/bin:/usr/bin', 'LC_ALL': 'C'}
_PROC = None


def parents():
    """Every process's number and parent, numbers only."""
    done = subprocess.run(['/bin/ps', '-axo', 'pid=,ppid='], capture_output=True, text=True, env=ENV)
    table = {}
    for line in done.stdout.splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            table[int(parts[0])] = int(parts[1])
    return table


def executable_of(pid):
    """The system's path for one process's executable, or None."""
    global _PROC
    if sys.platform == 'darwin':
        if _PROC is None:
            _PROC = ctypes.CDLL('/usr/lib/libproc.dylib', use_errno=True)
        buffer = ctypes.create_string_buffer(4096)
        if _PROC.proc_pidpath(ctypes.c_int(pid), buffer, ctypes.c_uint32(len(buffer))) <= 0:
            return None
        return os.fsdecode(buffer.value)
    try:
        return os.readlink(f'/proc/{pid}/exe')
    except OSError:
        return None


def detail(pid):
    """The process state and the accounting name of one selected process, or None when it is not listed."""
    done = subprocess.run(['/bin/ps', '-o', 'stat=,ucomm=', '-p', str(pid)], capture_output=True, text=True, env=ENV)
    parts = done.stdout.strip().split(None, 1)
    if done.returncode != 0 or not parts:
        return None
    return parts[0], (parts[1].strip() if len(parts) > 1 else '')


def state(pid, first_seen=None, table=None, detail_of=None, executable=None):
    table = parents() if table is None else table
    detail_of = detail_of or detail
    executable = executable or executable_of
    own = detail_of(pid) if pid in table else None
    exited = own is not None and own[0].startswith('Z')
    path = executable(pid) if own is not None and not exited else None
    same = path is not None and (first_seen is None or path == first_seen)
    children = []
    if same:
        for number in sorted(child for child, parent in table.items() if parent == pid):
            seen = detail_of(number)
            if seen is not None:
                children.append({'pid': number, 'name': seen[1]})
    return {'pid': pid, 'at_ms': int(time.time() * 1000), 'at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'running': same, 'executable': path if same else None, 'children': children}


def write(path, value):
    partial = f'{path}.partial-{os.getpid()}'
    with open(partial, 'w') as stream:
        stream.write(json.dumps(value) + '\n')
    os.replace(partial, path)


def main(argv):
    if len(argv) != 3 or not argv[1].isdigit() or int(argv[1]) <= 1:
        print('usage: watch.py <process number> <file to keep>', file=sys.stderr)
        return 2
    pid, path = int(argv[1]), argv[2]
    first_seen = None
    while True:
        value = state(pid, first_seen)
        first_seen = first_seen or value['executable']
        write(path, value)
        if not value['running']:
            return 0
        time.sleep(1)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
