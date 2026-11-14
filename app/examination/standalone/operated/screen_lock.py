#!/usr/bin/env python3
"""Say whether the login session's screen is locked. It reads and changes nothing else.

    python3 -B screen_lock.py

Why. The supplier's window service cannot see a window behind the lock screen. On 14 November 2026 a walk's first
view failed with "Computer Use server error -10005: cgWindowNotFound" while the screen was locked, and a launch was
spent finding that out. No agent dismisses the lock screen or holds it off; unlocking it is the owner's act.

What it asks. The login session's own description, through CoreGraphics' CGSessionCopyCurrentDictionary, and in it
two keys: kCGSSessionOnConsoleKey and CGSSessionScreenIsLocked. As read on this Mac on 14 November 2026, the lock key
is present, at 1, while the screen is locked, and absent while it is not. So:
- on the console (kCGSSessionOnConsoleKey 1), with the lock key absent or 0: not locked, exit 0;
- the lock key present and not 0: locked, exit 3;
- no session, not on the console, a key given twice or with a value that is not plain digits, or the description
  unreadable (or not macOS): could not be established, exit 2.
Anything but 0 means no walk.

Limits. It is one look, at one moment: the screen can lock after it. The keys are the session's own and are not
documented by Apple.
"""
import ctypes
import ctypes.util
import re
import sys

KEY, CONSOLE = 'CGSSessionScreenIsLocked', 'kCGSSessionOnConsoleKey'


def locked_from(description):
    """True (locked), False (not locked) or None (not established), from the session's description by the rule
    above. A key present more than once is not established."""
    # Only the dictionary's own keys count: at its top level, outside any quoted value, and as a whole name. Each key's
    # name is also counted wherever it appears in the text, and every appearance must be such a key reading
    # "<name> = <digits>;". A second copy, a value of any other form, or the name anywhere else is not established.
    top = top_level(description)
    if top is None:
        return None
    lock = re.findall(r'(?<![\w"])' + KEY + r'\s*=\s*(\d+)\s*;', top)
    console = re.findall(r'(?<![\w"])' + CONSOLE + r'\s*=\s*(\d+)\s*;', top)
    if description.count(KEY) != len(lock) or description.count(CONSOLE) != len(console):
        return None
    if len(lock) > 1 or len(console) > 1:
        return None
    if lock and int(lock[0]) != 0:
        return True
    if console == ['1']:
        return False
    return None


def top_level(description):
    """The description with everything but its outermost dictionary's own text blanked: quoted values and nested
    dictionaries or arrays become spaces. None if it is not one dictionary with balanced braces and quotes."""
    text = description.strip()
    if not (text.startswith('{') and text.endswith('}')):
        return None
    out, depth, quoted, escaped = [], 0, False, False
    for char in text:
        if quoted:
            out.append(' ')
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
            out.append(' ')
            continue
        if char in '{(':
            depth += 1
            out.append(char if depth == 1 else ' ')
            continue
        if char in '})':
            out.append(char if depth == 1 else ' ')
            depth -= 1
            if depth < 0:
                return None
            continue
        out.append(char if depth == 1 else ' ')
    return ''.join(out) if depth == 0 and not quoted else None


def session_description():
    """The session's description as text, or raises with the reason."""
    if sys.platform != 'darwin':
        raise OSError('not macOS')
    core = ctypes.CDLL(ctypes.util.find_library('CoreFoundation'))
    graphics = ctypes.CDLL(ctypes.util.find_library('CoreGraphics'))
    graphics.CGSessionCopyCurrentDictionary.restype = ctypes.c_void_p
    core.CFCopyDescription.restype = ctypes.c_void_p
    core.CFCopyDescription.argtypes = [ctypes.c_void_p]
    core.CFStringGetCString.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_long, ctypes.c_uint32]
    core.CFStringGetCString.restype = ctypes.c_bool
    core.CFRelease.argtypes = [ctypes.c_void_p]
    session = graphics.CGSessionCopyCurrentDictionary()
    if not session:
        raise OSError('there is no login session description')
    text = core.CFCopyDescription(session)
    try:
        buffer = ctypes.create_string_buffer(65536)
        if not core.CFStringGetCString(text, buffer, len(buffer), 0x08000100):  # kCFStringEncodingUTF8
            raise OSError('the description could not be read')
        return buffer.value.decode('utf-8')
    finally:
        core.CFRelease(text)
        core.CFRelease(session)


def main():
    try:
        locked = locked_from(session_description())
    except OSError as error:
        print(f'screen lock: could not be established ({error})')
        return 2
    if locked is None:
        print(f'screen lock: could not be established (the session is not on the console, or {KEY} or {CONSOLE} '
              'is in its description more than once)')
        return 2
    print('screen lock: LOCKED; no walk' if locked else 'screen lock: not locked')
    return 3 if locked else 0


if __name__ == '__main__':
    sys.exit(main())
