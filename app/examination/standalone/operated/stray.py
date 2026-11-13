#!/usr/bin/env python3
"""Look for a start of the candidate that the launcher did not make. It ends nothing and opens nothing.

    python3 -B stray.py <the bundle, the path of the .app folder> <bundle identifier> [<process number the launcher started> ...]

A view of an application that is not running starts it through the system's launch service, outside the launcher,
with the account's real home. If the build ends by itself during a walk, the next view can do that. This prints,
as JSON: every running process whose executable is inside the bundle, other than the numbers given, with its
parent and start time; and, by name only, every entry named for the identifier in the real Library's places the
launcher compares. It lists those places and reads nothing in them. Exit status 0 when it found neither, 1 when it
found either, 2 when it could not look.
"""
import json
import os
from pathlib import Path
import pwd
import subprocess
import sys

PLACES = ('', 'Application Support', 'Caches', 'WebKit', 'HTTPStorages', 'Preferences', 'Saved Application State',
          'Logs', 'Application Scripts', 'LaunchAgents')  # the launcher's watched places (launch.py WATCHED)


def listing():
    """One line for each process: number, parent, start time (five words), executable."""
    done = subprocess.run(['/bin/ps', '-axo', 'pid=,ppid=,lstart=,comm='], capture_output=True, text=True, env={'PATH': '/bin:/usr/bin'})
    if done.returncode != 0:
        raise OSError('the process listing failed')
    return done.stdout.splitlines()


def processes(bundle, known, lines=None):
    found = []
    inside = tuple({bundle + '/', os.path.realpath(bundle) + '/'})  # as given, and with any link in the path resolved
    for line in listing() if lines is None else lines:
        parts = line.strip().split(None, 7)  # the executable is last and may hold spaces
        if len(parts) == 8 and parts[0].isdigit() and parts[7].startswith(inside) and int(parts[0]) not in known:
            found.append({'pid': int(parts[0]), 'parent': int(parts[1]), 'started': ' '.join(parts[2:7]), 'executable': parts[7]})
    return found


def library_entries(identifier, library):
    found, not_listed = [], []
    for place in PLACES:
        folder = library / place if place else library
        try:
            names = sorted(os.listdir(folder))
        except FileNotFoundError:
            continue
        except OSError as error:
            not_listed.append(f'{folder} ({type(error).__name__})')
            continue
        found += [str(folder / name) for name in names if name == identifier or name.startswith(identifier + '.')]
    return found, not_listed


def main(argv):
    if len(argv) < 3 or not argv[1].startswith('/') or not argv[1].endswith('.app') or not all(a.isdigit() for a in argv[3:]):
        print('usage: stray.py <bundle .app path> <bundle identifier> [<process number the launcher started> ...]', file=sys.stderr)
        return 2
    bundle, identifier, known = argv[1], argv[2], {int(a) for a in argv[3:]}
    library = Path(os.path.realpath(pwd.getpwuid(os.getuid()).pw_dir)) / 'Library'
    try:
        running = processes(bundle, known)
        entries, not_listed = library_entries(identifier, library)
    except OSError as error:
        print(json.dumps({'error': f'{type(error).__name__}: {error}'}), file=sys.stderr)
        return 2
    print(json.dumps({'processes_not_started_by_the_launcher': running, 'entries_named_for_the_build_in_the_real_library': entries,
                      'places_that_could_not_be_listed': not_listed}, indent=1))
    return 1 if running or entries else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
