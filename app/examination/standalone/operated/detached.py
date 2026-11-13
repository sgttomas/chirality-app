#!/usr/bin/env python3
"""Start one command so that it outlives the shell that started it.

    python3 -B detached.py <folder for its output> <name> -- <command> [arguments...]

An agent's shell tool ends the processes it started when a call returns, so a launcher or a watch started with
`&` is gone before the next call. This starts the command in a session of its own, with no input, and its output
in <name>.out and <name>.err in the folder (which must exist; none of its files may exist). It writes
<name>.started.json there with the process number, the command exactly as given and the time, prints the same,
and returns at once.

What it does and does not do. It starts exactly the one command it is given, as a list of arguments: no shell
reads it, nothing is expanded, and nothing else is started. It changes nothing in the command's environment. It
does not wait for the command, watch it or end it: ending it later is a signal sent to the recorded process
number, and whoever started it is answerable for that. The started file is the record by which something left
running is found.
"""
import json
import os
import subprocess
import sys
import time


def main(argv):
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
    os.write(handles[2], (json.dumps(started, indent=1) + '\n').encode())
    os.close(handles[2])
    print(json.dumps(started))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
