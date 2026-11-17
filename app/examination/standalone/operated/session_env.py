#!/usr/bin/env python3
"""Say whether a start of the build by the system's launch service would be given any of the App's configuration
variables. It asks for fixed names one at a time, keeps only whether each is set, never a value, and changes nothing.

    python3 -B session_env.py <the bundle, the path of the .app folder>

Why. The launcher builds the App's environment from nothing, so a launch it makes inherits nothing from the login
session. One start of the build does not go through the launcher: a view the computer-use service asks of an App
that is not running can start the build through the system's launch service (README.md, "A view of an application
that is not running"). Such a start is given the login session's launch-domain environment and any LSEnvironment
the bundle's own Info.plist declares. When any of these variables is present, empty included, the App takes its
configuration from the environment and never looks for a saved request, and with a usable configuration it starts
Codex (app/src-tauri/src/lib.rs, explicit_environment_launch; desktop_startup.rs, resolve).

What it asks. For each of the fixed names below, and for no other, one query of the launch domain,
`launchctl getenv <name>`. Whatever the query prints is read into memory only to tell whether it printed anything,
and is then dropped: no value is printed, logged, kept or put in an error. The domain is never printed whole. The
bundle's Info.plist is read for the names its LSEnvironment declares.

What a query can establish. launchctl's documentation says only that `getenv` prints the value of the variable
launchd would set. It says nothing of its exit status, of what it prints for a variable that is not set, or of how a
variable set to the empty value differs from one not set. So:
- exit status 0 with something printed: the variable is set; "present";
- anything else (nothing printed, which an unset variable and one set to empty could both give, a non-zero exit
  status, a query that could not be made): "could not be established", with the reason. Never "absent".
A name declared by the bundle's LSEnvironment is "present". A name is "absent" only when both the bundle and the
launch domain establish that it is not set, and the launch domain never establishes that by this query. Exit status
0 only when every name is absent; 1 when any is present; 2 when any could not be established. Anything but 0
refuses the walk, so this check refuses every walk until the meaning of "not set" is established for this query.

Limits. Which domain `getenv` answers for is the caller's context, as the documentation says; that it is the domain
the launch service would start the build in is not observed. It is one look, at one moment.
"""
import json
import os
import plistlib
import subprocess
import sys

NAMES = ('CHIRALITY_CODEX_BIN', 'CHIRALITY_CODEX_HOME', 'CHIRALITY_WORKSPACE', 'CHIRALITY_KEY_HOME',
         'CHIRALITY_SHARED_CONFIG', 'CHIRALITY_SHARED_AGENTS', 'CHIRALITY_SHARED_SKILLS',
         'CHIRALITY_CODEX_EXPECTED_SHA256', 'CHIRALITY_ALLOW_UNVERIFIED', 'CHIRALITY_DISTRIBUTION_SUCCESSOR',
         'CHIRALITY_APP_DATA')
UNKNOWN = 'could not be established'
EMPTY = ('launchctl getenv printed nothing, which a variable not set and one set to the empty value could both give '
         '(its documentation states neither)')


def query(name, run=None):
    """'present', or a reason it could not be established. Never 'absent'."""
    try:
        code, printed = (run or _run)(name)
    except (OSError, ValueError) as error:
        return f'{UNKNOWN}: launchctl getenv could not be asked ({type(error).__name__})'
    if code == 0 and printed:
        return 'present'
    if code != 0:
        return f'{UNKNOWN}: launchctl getenv exited {code}'
    return f'{UNKNOWN}: {EMPTY}'


def _run(name):
    """One query of the launch domain for one fixed name: (exit status, whether it printed anything). What it printed
    is dropped here and goes nowhere else."""
    if name not in NAMES:
        raise ValueError('only the fixed names are asked for')
    done = subprocess.run(['/bin/launchctl', 'getenv', name], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                          stderr=subprocess.DEVNULL, env={'PATH': '/bin:/usr/bin'})
    code, printed = done.returncode, bool(done.stdout.strip())
    del done
    return code, printed


def bundle_names(bundle):
    with open(os.path.join(bundle, 'Contents', 'Info.plist'), 'rb') as stream:
        declared = plistlib.load(stream).get('LSEnvironment', {})
    if not isinstance(declared, dict):
        raise ValueError('LSEnvironment is not a dictionary')
    return set(declared)


def states(session, bundle, bundle_reason):
    """session: name -> the launch domain's answer for it (query). bundle: the names the bundle declares, or None."""
    out = {}
    for name in NAMES:
        if (bundle is not None and name in bundle) or session.get(name) == 'present':
            out[name] = 'present'
        elif bundle is None:
            out[name] = f'{UNKNOWN}: {bundle_reason}'
        else:
            out[name] = session.get(name, f'{UNKNOWN}: not asked')
    return out


def status(result):
    values = result.values()
    return 1 if 'present' in values else 2 if any(v.startswith(UNKNOWN) for v in values) else 0


def on_macos():
    return sys.platform == 'darwin'


def main(argv, run=None):
    if len(argv) != 2 or not argv[1].startswith('/') or not argv[1].endswith('.app'):
        print('usage: session_env.py <bundle .app path>', file=sys.stderr)
        return 2
    if on_macos():
        session = {name: query(name, run) for name in NAMES}
    else:
        session = {name: f'{UNKNOWN}: this is asked on macOS only' for name in NAMES}
    bundle = bundle_reason = None
    try:
        bundle = bundle_names(argv[1])
    except (OSError, ValueError, plistlib.InvalidFileException) as error:
        bundle_reason = f"the bundle's Info.plist could not be read ({type(error).__name__})"
    result = states(session, bundle, bundle_reason)
    print(json.dumps(result, indent=1))
    return status(result)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
