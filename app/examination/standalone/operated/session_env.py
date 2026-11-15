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

What it keeps (App Agent 0's conditions, 14 November 2026). It reads the launch DOMAIN, never a process: no
process's arguments or environment are read. It keeps and prints names and their states only. No value is ever
written to a file, a log, a record or an error message, including when the output cannot be parsed: a failure is
reported in this tool's own fixed words ("could not be established" with a fixed reason), never with the line or any
part of the output.

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
         'CHIRALITY_CODEX_EXPECTED_SHA256', 'CHIRALITY_ALLOW_UNVERIFIED', 'CHIRALITY_DISTRIBUTION_SUCCESSOR',
         'CHIRALITY_APP_DATA')
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


def read_domain(run=None):
    """The domain's names, or a fixed reason. Output that cannot be decoded or parsed is never shown."""
    try:
        done = (run or subprocess.run)(['/bin/launchctl', 'print', f'gui/{os.getuid()}'], capture_output=True, env={'PATH': '/bin:/usr/bin'})
        if done.returncode != 0:
            return None, f'launchctl print exited {done.returncode}'
        text = done.stdout.decode('utf-8')
    except Exception:  # noqa: BLE001  any failure, in fixed words: nothing of the output is kept
        return None, 'the launch domain could not be read'
    return session_names(text)


def bundle_names(bundle):
    with open(os.path.join(bundle, 'Contents', 'Info.plist'), 'rb') as stream:
        info = plistlib.load(stream)
    if not isinstance(info, dict):
        raise ValueError('the Info.plist is not a dictionary')
    declared = info.get('LSEnvironment', {})
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
        session, session_reason = read_domain()
    try:
        bundle = bundle_names(argv[1])
    except Exception:  # noqa: BLE001  any failure, in fixed words: nothing of the file or the error is shown
        bundle_reason = "the bundle's Info.plist could not be read"
    result = states(session, session_reason, bundle, bundle_reason)
    print(json.dumps(result, indent=1))
    return status(result)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
