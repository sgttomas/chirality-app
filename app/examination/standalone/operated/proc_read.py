#!/usr/bin/env python3
"""The one way this method reads processes (DEL-09-02 examination tooling; App Agent 0's bound, 14 November 2026).

The bound: no tool of ours reads or keeps what a process was started WITH (its arguments, its environment) or what it
has OPEN, for any process, and nothing at all is kept about a process that is neither ours nor the supplier's window
service. Within it, exactly these reads are made, and no other:

- every process's number and parent, numbers only (ps -axo pid=,ppid=), to follow parent links;
- every process's accounting name (ps -axo pid=,ucomm=), compared exactly against the one name wanted. Only matching
  rows are kept; every other row is discarded unprinted. ucomm is the accounting name, cut at 16 characters, and not
  argv[0]: comm is argv[0] on this host, so it is never read;
- for a selected process only: its number, parent, start time and accounting name (ps -o pid=,ppid=,lstart=,ucomm=),
  and its executable, the first program text entry of that one process (lsof -a -p <pid> -d txt -Fn). lsof is never
  run unrestricted, since that would list the files the process has open.

No command line is printed, matched on or kept. pgrep is not used, with its full-argument or its exact-name flag
(the exact-name match reads a name longer than the accounting name, from a source not established).

    python3 -B proc_read.py details <pid>
    python3 -B proc_read.py descendants <pid>       the process and every descendant, each with its details
    python3 -B proc_read.py window-service          the supplier's window service, if it is running
    python3 -B proc_read.py count <accounting name> how many processes have exactly that accounting name
"""
import json
import os
import subprocess
import sys
import time

PS = '/bin/ps'
LSOF = '/usr/sbin/lsof'
ENV = {'PATH': '/bin:/usr/bin:/usr/sbin', 'LC_ALL': 'C'}
# The window service's accounting name, cut at 16 characters, and the path it runs from (README, "Reading processes").
# The path is compared as text against lsof's answer; nothing under it is opened.
SERVICE_NAME = 'SkyComputerUseService'[:16]
SERVICE_PATH = os.path.expanduser('~') + '/.codex/computer-use/Codex Computer Use.app/Contents/MacOS/SkyComputerUseService'


def _run(args):
    done = subprocess.run(args, capture_output=True, text=True, env=ENV)
    return done.returncode, done.stdout


def parents():
    """Every process's number and parent, numbers only."""
    code, out = _run([PS, '-axo', 'pid=,ppid='])
    if code != 0:
        return None
    table = {}
    for line in out.splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            table[int(parts[0])] = int(parts[1])
    return table


def executable(pid):
    """The first program text entry of this one process, or None. Anything but p, f and n lines makes it None."""
    code, out = _run([LSOF, '-a', '-p', str(pid), '-d', 'txt', '-Fn'])
    if code != 0:
        return None
    lines = out.splitlines()
    if any(not line or line[0] not in 'pfn' for line in lines):
        return None
    names = [line[1:] for line in lines if line.startswith('n')]
    return names[0] if names else None


def details(pid):
    """Number, parent, start time (UTC and epoch), accounting name and executable of one selected process, or None."""
    code, out = _run([PS, '-o', 'pid=,ppid=,lstart=,ucomm=', '-p', str(pid)])
    parts = out.split()
    if code != 0 or len(parts) < 7 or not parts[0].isdigit():
        return None
    try:
        started = time.mktime(time.strptime(' '.join(parts[2:7]), '%a %b %d %H:%M:%S %Y'))
    except ValueError:
        return None
    return {'pid': int(parts[0]), 'ppid': int(parts[1]), 'started_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(started)),
            'started_epoch': int(started), 'ucomm': ' '.join(parts[7:]), 'executable': executable(pid)}


def descendants(root):
    """The process and every descendant, by parent links, each with its details; or None when the table is unreadable."""
    table = parents()
    if table is None:
        return None
    found, frontier = [], [root] if root in table else []
    while frontier:
        pid = frontier.pop(0)
        found.append(pid)
        frontier.extend(child for child, parent in table.items() if parent == pid and child not in found)
    return [entry for entry in (details(pid) for pid in found) if entry is not None]


def exact_accounting_name(name):
    """The numbers of the processes whose accounting name is exactly this; every other row is discarded unread."""
    code, out = _run([PS, '-axo', 'pid=,ucomm='])
    if code != 0:
        return None
    matches = []
    for line in out.splitlines():
        head, _, rest = line.strip().partition(' ')
        if head.isdigit() and rest.strip() == name:
            matches.append(int(head))
    return matches


def window_service():
    """The window service, if running: a process whose accounting name is its cut name AND whose executable is its known
    path. A candidate with another path is not the service and nothing about it is kept."""
    candidates = exact_accounting_name(SERVICE_NAME)
    if candidates is None:
        return None
    return [entry for entry in (details(pid) for pid in candidates) if entry and entry['executable'] == SERVICE_PATH]


def same_process(pid, started_at_iso, command_word):
    """Whether this number is still the process we started: running, started within two seconds of our record of its
    start, and executing the program our own record names (resolved). Reads nothing the process was started with."""
    entry = details(pid)
    if entry is None:
        return False, 'not running'
    try:
        recorded = calendar_utc(started_at_iso)
    except (TypeError, ValueError):
        return False, 'our record of its start could not be read'
    if abs(entry['started_epoch'] - recorded) > 2:
        return False, f"process {pid} started at {entry['started_utc']}, not at our record's {started_at_iso}: another process"
    wanted = os.path.realpath(command_word) if command_word else None
    if not wanted or entry['executable'] is None or os.path.realpath(entry['executable']) != wanted:
        return False, f'process {pid} does not execute the program our record names'
    return True, 'the process we started'


def calendar_utc(iso):
    import calendar
    return calendar.timegm(time.strptime(iso, '%Y-%m-%dT%H:%M:%SZ'))


def main(argv):
    if len(argv) >= 2 and argv[1] == 'window-service':
        result = window_service()
    elif len(argv) == 3 and argv[1] == 'details' and argv[2].isdigit():
        result = details(int(argv[2]))
    elif len(argv) == 3 and argv[1] == 'descendants' and argv[2].isdigit():
        result = descendants(int(argv[2]))
    elif len(argv) == 3 and argv[1] == 'count':
        matches = exact_accounting_name(argv[2][:16])
        result = None if matches is None else len(matches)
    else:
        print(__doc__, file=sys.stderr)
        return 2
    print(json.dumps(result))
    return 0 if result is not None else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
