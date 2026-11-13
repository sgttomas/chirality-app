#!/usr/bin/env python3
"""Start one command so that it outlives the shell that started it.

    python3 -B detached.py <folder for its output> <name> -- <command> [arguments...]

An agent's shell tool ends the processes it started when a call returns, so a launcher or a watch started with
`&` is gone before the next call. This starts the command in a session of its own, with no input, and its output
in <name>.out and <name>.err in the folder (which must exist; neither file may exist). It prints the process
number and returns at once. It changes nothing in the command's environment. Ending the command later is a signal
sent to that process number.
"""
import json
import os
import subprocess
import sys


def main(argv):
    if len(argv) < 5 or argv[3] != '--' or not argv[2] or '/' in argv[2] or argv[2].startswith('.'):
        print('usage: detached.py <folder for its output> <name> -- <command> [arguments...]', file=sys.stderr)
        return 2
    folder, name, command = argv[1], argv[2], argv[4:]
    try:
        paths = [os.path.join(folder, f'{name}.{kind}') for kind in ('out', 'err')]
        handles = [os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600) for path in paths]
    except OSError as error:
        print(json.dumps({'error': f'{type(error).__name__}: the output files could not be created in {folder}'}), file=sys.stderr)
        return 2
    try:
        process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=handles[0], stderr=handles[1],
                                   start_new_session=True, close_fds=True)
    except OSError as error:
        print(json.dumps({'error': f'{type(error).__name__}: the command could not be started'}), file=sys.stderr)
        return 2
    finally:
        for handle in handles:
            os.close(handle)
    print(json.dumps({'pid': process.pid, 'out': paths[0], 'err': paths[1]}))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
