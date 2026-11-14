#!/usr/bin/env python3
"""The operator's runtime, the route's processes, and what recovery may end (DEL-09-02 examination tooling).

    python3 -B route.py record <evidence folder> <identities|look|after-import|end>
    python3 -B route.py recover <evidence folder> [--dry-run]

Every process read goes through proc_read.py, within App Agent 0's bound (14 November 2026): nothing a process was
started with (its arguments, its environment) and nothing it has open is read, for any process.

WHAT IS OURS, FOR THE BOUNDED DETAILS (App Agent 0's ruling), and nothing beside it:
- the operator's own runtime: the process whose number and parent the walk's runtime wrote itself, from node's own
  process.pid and process.ppid, into runtime.json in the evidence folder (no process is searched for it);
- its parent, the host, for RECORDING ONLY;
- the processes descended from that runtime by parent links read at that moment.
For each: its number, parent, start time, accounting name and the restricted program text path. The window service
is read by its accounting name, as a candidate, and is the service only when its executable is the supplier's path.

record writes route-<label>.json in the evidence folder:
- identities: the runtime and host as expected (ChatGPT's node and node_repl), the runtime's parent the host; otherwise
  exit 3, no walk;
- look: the same runtime and host by start time, and neither an app-server nor a window service running; otherwise
  exit 3, no walk;
- after-import and end: the same runtime and host by start time (otherwise exit 3: at after-import, no walk), and
  what is there, recorded.

THE APP-SERVER is identified only when all three hold: it descends from the runtime, its accounting name is "codex",
and its executable is under the supplier's CodexCLI application.

recover ends, with an ordinary termination and nothing stronger, ONLY:
- an app-server that, at the moment of signalling, (a) descends from the operator's own runtime by parent links just
  read, the runtime being the same process by start time as recorded; (b) is the same process by start time as one
  recorded during the session (route-after-import.json or route-end.json); and (c) started no earlier than the look;
- a window service that the session caused to start: the look recorded that none was running, this one started after
  the look, and its executable is the supplier's path; checked again immediately before the signal.
It NEVER signals the host, the runtime itself, a process identified by name or path alone, or anything outside that
descent. A window service that was already running before the session is never ended (the go refuses to start then);
one recovery cannot show the session caused is reported and left. Whatever recovery leaves, it reports.
"""
import json
import os
from pathlib import Path
import signal
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
import proc_read  # noqa: E402

RUNTIME_EXE = '/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node'
HOST_EXE = '/Applications/ChatGPT.app/Contents/Resources/cua_node/bin/node_repl'
APP_SERVER_UNDER = '/Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/'
APP_SERVER_NAME = 'codex'
LABELS = ('identities', 'look', 'after-import', 'end')


class Reads:
    """The reads route.py makes, all through proc_read. Tests give another."""
    parents = staticmethod(proc_read.parents)
    details = staticmethod(proc_read.details)
    window_service = staticmethod(proc_read.window_service)


def utc_epoch(iso):
    return proc_read.calendar_utc(iso)


def descends(pid, root, table):
    """Whether pid descends from root by the parent links in table (root itself is not its own descendant)."""
    seen = set()
    while pid in table and pid not in seen:
        seen.add(pid)
        pid = table[pid]
        if pid == root:
            return True
    return False


def descendants(root, table):
    return sorted(pid for pid in table if descends(pid, root, table))


def is_app_server(entry):
    return bool(entry) and entry.get('ucomm') == APP_SERVER_NAME and isinstance(entry.get('executable'), str) \
        and entry['executable'].startswith(APP_SERVER_UNDER)


def snapshot(runtime_pid, reads):
    """The runtime, its host, its descendants and any window service, as read now."""
    table = reads.parents()
    if table is None:
        return None
    runtime = reads.details(runtime_pid) if runtime_pid in table else None
    host = reads.details(runtime['ppid']) if runtime else None
    below = [entry for entry in (reads.details(pid) for pid in descendants(runtime_pid, table)) if entry] if runtime else []
    service = reads.window_service()
    return {'at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'runtime': runtime, 'host': host, 'descendants': below,
            'app_servers': [entry for entry in below if is_app_server(entry)], 'window_services': service}


def load(folder, name):
    try:
        return json.loads((Path(folder) / name).read_text())
    except (OSError, ValueError):
        return None


def same(a, b):
    return bool(a) and bool(b) and a.get('pid') == b.get('pid') and a.get('started_epoch') == b.get('started_epoch')


def record(folder, label, reads=Reads):
    """Write route-<label>.json; return (exit status, what was found)."""
    own = load(folder, 'runtime.json')
    if not own or not isinstance(own.get('pid'), int) or not isinstance(own.get('ppid'), int):
        return 3, 'the runtime did not record its number and parent (runtime.json), so it is not identified'
    seen = snapshot(own['pid'], reads)
    if seen is None:
        return 3, 'the process table could not be read'
    (Path(folder) / f'route-{label}.json').write_text(json.dumps(seen, indent=1) + '\n')
    runtime, host = seen['runtime'], seen['host']
    if label == 'identities':
        if not runtime or runtime['ppid'] != own['ppid'] or runtime['executable'] != RUNTIME_EXE or not host or host['executable'] != HOST_EXE:
            return 3, 'the runtime or its host is not the one expected (ChatGPT\'s node, whose parent is its node_repl)'
        return 0, 'the runtime and its host are identified'
    first = load(folder, 'route-identities.json')
    if not first or not same(first.get('runtime'), runtime) or not same(first.get('host'), host):
        return 3, 'the runtime or its host is not the same process as identified'
    if label == 'look' and (seen['app_servers'] or seen['window_services']):
        return 3, 'an app-server or a window service is running before the import'
    return 0, 'the same runtime and host' + ('; no app-server and no window service' if label == 'look' else '; recorded')


def gone(pid, reads, waits=3, pause=5.0, sleep=time.sleep):
    """Ended: not listed, or exited (state Z). Checked again after five seconds, up to three times."""
    for attempt in range(waits + 1):
        if pid not in (reads.parents() or {}):
            return True
        if attempt < waits:
            sleep(pause)
    return False


def recover(folder, dry_run=False, reads=Reads, send=os.kill, sleep=time.sleep):
    """End only what the rules allow; report everything else. Returns the report."""
    report = {'ended': [], 'not_ended': [], 'left': []}
    own, first, look = load(folder, 'runtime.json'), load(folder, 'route-identities.json'), load(folder, 'route-look.json')
    session = [entry for name in ('route-after-import.json', 'route-end.json') for entry in ((load(folder, name) or {}).get('app_servers') or [])]
    table = reads.parents()
    if table is None:
        report['left'].append('the process table could not be read: nothing was signalled')
        return report
    host_pid = (first or {}).get('host', {}).get('pid') if first else None
    runtime_recorded = (first or {}).get('runtime')
    look_epoch = utc_epoch(look['at']) if look and isinstance(look.get('at'), str) else None

    def end(entry, why):
        if entry['pid'] in (1, os.getpid(), host_pid, (runtime_recorded or {}).get('pid')):
            report['not_ended'].append({**entry, 'why': 'never signalled: the host, the runtime, launchd or this process'})
            return
        if dry_run:
            report['ended'].append({**entry, 'why': why, 'dry_run': True})
            return
        send(entry['pid'], signal.SIGTERM)
        report['ended'].append({**entry, 'why': why, 'confirmed_gone': gone(entry['pid'], reads, sleep=sleep)})

    # The app-servers: descendants of the operator's own runtime, recorded in the session, and no older than the look.
    runtime_now = reads.details(own['pid']) if own and isinstance(own.get('pid'), int) else None
    if not same(runtime_recorded, runtime_now):
        report['left'].append('the operator\'s runtime is not the same process as identified (or is gone), so no descendant of it can be shown: no app-server was signalled')
    else:
        for pid in descendants(runtime_now['pid'], table):
            entry = reads.details(pid)
            if not is_app_server(entry):
                continue
            recorded = next((r for r in session if same(r, entry)), None)
            if recorded is None:
                report['not_ended'].append({**entry, 'why': 'not recorded during the session with this start time'})
                continue
            if look_epoch is None or entry['started_epoch'] < look_epoch:
                report['not_ended'].append({**entry, 'why': 'it started before the look, or the look is not recorded'})
                continue
            # Immediately before the signal: still a descendant by links just read, and still the same process.
            again, fresh = reads.details(pid), reads.parents() or {}
            if not same(again, recorded) or not descends(pid, runtime_now['pid'], fresh) or not is_app_server(again):
                report['not_ended'].append({**entry, 'why': 'not shown, immediately before the signal, to be the same descendant'})
                continue
            end(again, "the walk's app-server: a descendant of the operator's runtime, recorded in the session")
    # The window service: only one the session caused to start.
    for entry in reads.window_service() or []:
        if not look or look.get('window_services') != []:
            report['left'].append({**entry, 'why': 'the look did not record that none was running: not shown to be the session\'s; left'})
            continue
        if look_epoch is None or entry['started_epoch'] <= look_epoch:
            report['left'].append({**entry, 'why': 'it started at or before the look: not shown to be the session\'s; left'})
            continue
        again = reads.details(entry['pid'])
        if not same(again, entry) or again.get('executable') != proc_read.SERVICE_PATH:
            report['left'].append({**entry, 'why': 'not shown, immediately before the signal, to be the same window service; left'})
            continue
        end(again, 'the window service the session caused to start: none at the look, started after it, the supplier\'s path')
    return report


def main(argv):
    if len(argv) == 4 and argv[1] == 'record' and argv[3] in LABELS:
        code, said = record(argv[2], argv[3])
        print(said)
        return code
    if len(argv) in (3, 4) and argv[1] == 'recover' and (len(argv) == 3 or argv[3] == '--dry-run'):
        result = recover(argv[2], dry_run=len(argv) == 4)
        print(json.dumps(result, indent=1))
        return 0 if not result['left'] and all(e.get('confirmed_gone', True) for e in result['ended']) else 1
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv))
