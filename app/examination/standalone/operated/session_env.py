#!/usr/bin/env python3
"""Say whether a start of the build by the system's launch service would be given any of the App's configuration
variables. It prints names and states, never a value, and changes nothing.

    python3 -B session_env.py <the bundle, the path of the .app folder>

Why. When any of these variables is present, empty included, the App takes its configuration from the environment
and never looks for a saved request, and with a usable configuration it starts Codex (app/src-tauri/src/lib.rs,
explicit_environment_launch; desktop_startup.rs, resolve). A build the launch service starts has the login
session's environment and any LSEnvironment its own Info.plist declares.

What it asks. The login session's launch domain, through `launchctl print gui/<this user>`, whose block
`environment = { ... }` lists one `NAME => value` line for each variable it holds; and the bundle's Info.plist. For
each name it says one of three things: "absent", "present" (empty included), or "could not be established", with
the reason. Exit status 0 only when every name is absent from both; 1 when any is present; 2 when any could not be
established. Anything but 0 refuses the walk.

Limits. That an application the launch service starts takes its environment from that domain is the system's
documented behaviour, not something this observed; the block's format is what `launchctl` printed on this host,
and output it cannot read is "could not be established", never "absent". It is one look, at one moment.
"""
import json
import os
import plistlib
import subprocess
import sys

NAMES = ('CHIRALITY_CODEX_BIN', 'CHIRALITY_CODEX_HOME', 'CHIRALITY_WORKSPACE', 'CHIRALITY_KEY_HOME',
         'CHIRALITY_SHARED_CONFIG', 'CHIRALITY_SHARED_AGENTS', 'CHIRALITY_SHARED_SKILLS',
         'CHIRALITY_CODEX_EXPECTED_SHA256', 'CHIRALITY_ALLOW_UNVERIFIED', 'CHIRALITY_DISTRIBUTION_SUCCESSOR')
UNKNOWN = 'could not be established'


def session_names(text):
    """The names in the domain's one environment block, or a reason it could not be read. Values are dropped here."""
    blocks = [i for i, line in enumerate(text.splitlines()) if line.strip() == 'environment = {']
    lines = text.splitlines()
    if len(blocks) != 1:
        return None, f'the launch domain printed {len(blocks)} environment blocks, not one'
    names = set()
    for line in lines[blocks[0] + 1:]:
        entry = line.strip()
        if entry == '}':
            return names, None
        name, separator, _ = entry.partition(' =>')
        if not separator or not name or ' ' in name:
            return None, 'a line of the environment block could not be read'
        names.add(name)
    return None, 'the environment block does not end'


def bundle_names(bundle):
    with open(os.path.join(bundle, 'Contents', 'Info.plist'), 'rb') as stream:
        declared = plistlib.load(stream).get('LSEnvironment', {})
    if not isinstance(declared, dict):
        raise ValueError('LSEnvironment is not a dictionary')
    return set(declared)


def states(session, session_reason, bundle, bundle_reason):
    out = {}
    for name in NAMES:
        if (session is not None and name in session) or (bundle is not None and name in bundle):
            out[name] = 'present'
        elif session is None or bundle is None:
            out[name] = f'{UNKNOWN}: {session_reason or bundle_reason}'
        else:
            out[name] = 'absent'
    return out


def status(result):
    values = result.values()
    return 1 if 'present' in values else 2 if any(v.startswith(UNKNOWN) for v in values) else 0


def on_macos():
    return sys.platform == 'darwin'


def main(argv):
    if len(argv) != 2 or not argv[1].startswith('/') or not argv[1].endswith('.app'):
        print('usage: session_env.py <bundle .app path>', file=sys.stderr)
        return 2
    session = bundle = None
    session_reason = bundle_reason = None
    if not on_macos():
        session_reason = 'this is asked on macOS only'
    else:
        done = subprocess.run(['/bin/launchctl', 'print', f'gui/{os.getuid()}'], capture_output=True, text=True,
                              env={'PATH': '/bin:/usr/bin'})
        if done.returncode != 0:
            session_reason = f'launchctl print exited {done.returncode}'
        else:
            session, session_reason = session_names(done.stdout)
    try:
        bundle = bundle_names(argv[1])
    except (OSError, ValueError, plistlib.InvalidFileException) as error:
        bundle_reason = f"the bundle's Info.plist could not be read ({type(error).__name__})"
    result = states(session, session_reason, bundle, bundle_reason)
    print(json.dumps(result, indent=1))
    return status(result)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
