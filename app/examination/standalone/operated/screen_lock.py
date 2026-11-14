#!/usr/bin/env python3
"""Say whether the login session's screen is locked. It reads and changes nothing else.

    python3 -B screen_lock.py

Why. The supplier's window service cannot see a window behind the lock screen. On 14 November 2026 a walk's first
view failed with "Computer Use server error -10005: cgWindowNotFound" while the screen was locked, and a launch was
spent finding that out. No agent dismisses the lock screen or holds it off; unlocking it is the owner's act.

What it asks. The login session's own dictionary, through CoreGraphics' CGSessionCopyCurrentDictionary, looked up by
CoreFoundation for two keys, kCGSSessionOnConsoleKey and CGSSessionScreenIsLocked. Each value is read as what it is:
absent, a number or a boolean (read as 1 or 0), or anything else. No text is parsed. As read on this Mac on 14 November
2026, the lock key is present, at 1, while the screen is locked, and absent while it is not. So:
- on the console (kCGSSessionOnConsoleKey 1), with the lock key absent or 0: not locked, exit 0;
- the lock key a number or boolean that is not 0: locked, exit 3;
- anything else (no session, not on the console, either key of another type, or not macOS): could not be
  established, exit 2.
Anything but 0 means no walk.

Limits. It is one look, at one moment: the screen can lock after it. The keys are the session's own and are not
documented by Apple. A number that does not convert exactly to a 64-bit integer (a fraction, say) is not established.
"""
import ctypes
import ctypes.util
import sys

KEY, CONSOLE = 'CGSSessionScreenIsLocked', 'kCGSSessionOnConsoleKey'
OTHER = 'a value that is neither a number nor a boolean'


def locked_from(values):
    """True (locked), False (not locked) or None (not established), from the two keys' values by the rule above. Each
    value is None (absent), an int, or OTHER."""
    lock, console = values.get(KEY), values.get(CONSOLE)
    if lock == OTHER or console == OTHER:
        return None
    if lock is not None and lock != 0:
        return True
    if console == 1:
        return False
    return None


def session_values():
    """The two keys' values from the session's dictionary, or raises with the reason."""
    if sys.platform != 'darwin':
        raise OSError('not macOS')
    core = ctypes.CDLL(ctypes.util.find_library('CoreFoundation'))
    graphics = ctypes.CDLL(ctypes.util.find_library('CoreGraphics'))
    graphics.CGSessionCopyCurrentDictionary.restype = ctypes.c_void_p
    core.CFStringCreateWithCString.restype = ctypes.c_void_p
    core.CFStringCreateWithCString.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint32]
    core.CFDictionaryGetValue.restype = ctypes.c_void_p
    core.CFDictionaryGetValue.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    core.CFGetTypeID.restype = ctypes.c_ulong
    core.CFGetTypeID.argtypes = [ctypes.c_void_p]
    core.CFNumberGetTypeID.restype = ctypes.c_ulong
    core.CFBooleanGetTypeID.restype = ctypes.c_ulong
    core.CFDictionaryGetTypeID.restype = ctypes.c_ulong
    core.CFNumberGetValue.restype = ctypes.c_bool
    core.CFNumberGetValue.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p]
    core.CFBooleanGetValue.restype = ctypes.c_bool
    core.CFBooleanGetValue.argtypes = [ctypes.c_void_p]
    core.CFRelease.argtypes = [ctypes.c_void_p]
    session = graphics.CGSessionCopyCurrentDictionary()
    if not session:
        raise OSError('there is no login session dictionary')
    try:
        if core.CFGetTypeID(session) != core.CFDictionaryGetTypeID():
            raise OSError('the session description is not a dictionary')
        values = {}
        for name in (KEY, CONSOLE):
            key = core.CFStringCreateWithCString(None, name.encode(), 0x08000100)  # kCFStringEncodingUTF8
            if not key:
                raise OSError('a key could not be made')
            try:
                value = core.CFDictionaryGetValue(session, key)  # not owned: not released
            finally:
                core.CFRelease(key)
            if not value:
                values[name] = None
            elif core.CFGetTypeID(value) == core.CFBooleanGetTypeID():
                values[name] = 1 if core.CFBooleanGetValue(value) else 0
            elif core.CFGetTypeID(value) == core.CFNumberGetTypeID():
                number = ctypes.c_int64()
                # kCFNumberSInt64Type; false when the value does not convert exactly
                values[name] = number.value if core.CFNumberGetValue(value, 4, ctypes.byref(number)) else OTHER
            else:
                values[name] = OTHER
        return values
    finally:
        core.CFRelease(session)


def main():
    try:
        values = session_values()
    except OSError as error:
        print(f'screen lock: could not be established ({error})')
        return 2
    locked = locked_from(values)
    if locked is None:
        print(f'screen lock: could not be established (the session is not on the console, or {KEY} or {CONSOLE} '
              'holds a value that is neither a number nor a boolean)')
        return 2
    print('screen lock: LOCKED; no walk' if locked else 'screen lock: not locked')
    return 3 if locked else 0


if __name__ == '__main__':
    sys.exit(main())
