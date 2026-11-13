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

Limits. It is a sample taken once a second, not custody: the process can end between two samples. Its children
are those whose parent is that process at the sample; a process it started that has since been given another
parent, or that came and went between samples, is not seen.
"""
import json
import os
import subprocess
import sys
import time


def listing():
    done = subprocess.run(['/bin/ps', '-axo', 'pid=,ppid=,stat=,comm='], capture_output=True, text=True, env={'PATH': '/bin:/usr/bin'})
    rows = []
    for line in done.stdout.splitlines():
        parts = line.strip().split(None, 3)
        if len(parts) == 4 and parts[0].isdigit() and parts[1].isdigit():
            rows.append((int(parts[0]), int(parts[1]), parts[2], parts[3]))
    return rows


def state(pid, first_seen=None, rows=None):
    rows = listing() if rows is None else rows
    own = [(status, command) for number, _, status, command in rows if number == pid]
    exited = bool(own) and own[0][0].startswith('Z')
    executable = own[0][1] if own and not exited else None
    same = executable is not None and (first_seen is None or executable == first_seen)
    return {'pid': pid, 'at_ms': int(time.time() * 1000), 'at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'running': same, 'executable': executable if same else None,
            'children': [{'pid': number, 'command': command} for number, parent, _, command in rows if parent == pid] if same else []}


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
