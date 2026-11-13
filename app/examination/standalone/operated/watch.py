#!/usr/bin/env python3
"""Keep a small file that says whether one process is running and what child processes it has.

    python3 -B watch.py <process number> <file to keep>

The operator starts this from the shell once the App's process is confirmed, and leaves it running. Once a second
it rewrites the file, whole, with the process number, the time, whether the process exists, its executable as the
system reports it, and its child processes. When the process has gone it writes that and ends. walk.mjs reads the
file, because the node runtime it runs in cannot ask the system about a process. It signals nothing and starts
nothing but the system's own process listing.
"""
import json
import os
import subprocess
import sys
import time


def listing():
    done = subprocess.run(['/bin/ps', '-axo', 'pid=,ppid=,comm='], capture_output=True, text=True, env={'PATH': '/bin:/usr/bin'})
    rows = []
    for line in done.stdout.splitlines():
        parts = line.strip().split(None, 2)
        if len(parts) == 3 and parts[0].isdigit() and parts[1].isdigit():
            rows.append((int(parts[0]), int(parts[1]), parts[2]))
    return rows


def state(pid):
    rows = listing()
    own = [command for number, _, command in rows if number == pid]
    return {'pid': pid, 'at_ms': int(time.time() * 1000), 'at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'running': bool(own), 'executable': own[0] if own else None,
            'children': [{'pid': number, 'command': command} for number, parent, command in rows if parent == pid]}


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
    while True:
        value = state(pid)
        write(path, value)
        if not value['running']:
            return 0
        time.sleep(1)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
