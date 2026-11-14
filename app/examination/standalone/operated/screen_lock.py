#!/usr/bin/env python3
"""Say whether the login session's screen is locked. It reads and changes nothing else.

    python3 -B screen_lock.py

Why. The supplier's window service cannot see a window behind the lock screen. On 14 November 2026 a walk's first
view failed with "Computer Use server error -10005: cgWindowNotFound" while the screen was locked, and a launch was
spent finding that out. No agent dismisses the lock screen or holds it off; unlocking it is the owner's act.

What it asks. The login session's own description, through CoreGraphics' CGSessionCopyCurrentDictionary, and in it
the key CGSSessionScreenIsLocked. Only that key is read. Exit status 0 when the screen is not locked; 3 when it is
locked; 2 when it could not be established (not macOS, the call failed, or the description could not be read).
Anything but 0 means no walk.

Limits. It is one look, at one moment: the screen can lock after it. The key is the session's own and is not
documented by Apple; its absence is "could not be established", never "not locked".
"""
import ctypes
import ctypes.util
import re
import sys

KEY = 'CGSSessionScreenIsLocked'


def locked_from(description):
    """True or False from the session's description, or None when the key is not in it once."""
    found = re.findall(KEY + r'\s*=\s*(\d+)\s*;', description)
    if len(found) != 1:
        return None
    return found[0] != '0'


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
        print(f'screen lock: could not be established ({KEY} is not in the session description once)')
        return 2
    print('screen lock: LOCKED; no walk' if locked else 'screen lock: not locked')
    return 3 if locked else 0


if __name__ == '__main__':
    sys.exit(main())
