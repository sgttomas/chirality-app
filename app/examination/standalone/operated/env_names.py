#!/usr/bin/env python3
"""The names in one process's environment, and nothing else (DEL-09-02 examination tooling, macOS only).

    python3 -B env_names.py <pid>

It reads the process's argument block once, read-only, with sysctl KERN_PROCARGS2 for that one pid, and prints the
sorted names of its environment entries, one per line. It drives nothing, opens no file, and keeps no value in memory
beyond the read itself. It writes no value anywhere, and prints no value.

Why this block: its entries are separated by NUL bytes, so a name is exactly what precedes the first "=" of an entry.
A value holding spaces, "=" signs or line breaks cannot be taken for a name, as it can in `ps -E`, whose entries are
separated by spaces. The block's layout:
- argc, as an int;
- the executable path, ending in NUL, then NUL padding;
- argc arguments, each ending in NUL;
- the environment entries, each ending in NUL, ended by an empty string;
- the kernel's own "apple" strings.
The apple strings are not the environment and are not read as names.

It exits 2 when the block cannot be read (no such process, another user's, or a refusal) or holds no environment, and
prints nothing then. The kernel gives no environment for an Apple platform binary (seen with /bin/sleep on this Mac); a
block that ends after the arguments, without the empty string that closes an environment, is reported so, never as an
empty environment.
"""
import ctypes
import ctypes.util
import struct
import sys

CTL_KERN, KERN_ARGMAX, KERN_PROCARGS2 = 1, 8, 49


def _sysctl(libc, mib, size):
    mib_array = (ctypes.c_int * len(mib))(*mib)
    buffer = ctypes.create_string_buffer(size)
    length = ctypes.c_size_t(size)
    if libc.sysctl(mib_array, len(mib), buffer, ctypes.byref(length), None, 0) != 0:
        return None
    return buffer.raw[:length.value]


def names(pid):
    """The sorted environment names of process pid, or None if its argument block cannot be read."""
    libc = ctypes.CDLL(ctypes.util.find_library('c'), use_errno=True)
    argmax = _sysctl(libc, [CTL_KERN, KERN_ARGMAX], ctypes.sizeof(ctypes.c_int))
    if argmax is None:
        return None
    block = _sysctl(libc, [CTL_KERN, KERN_PROCARGS2, pid], struct.unpack('i', argmax)[0])
    if block is None or len(block) < 4:
        return None
    argc = struct.unpack('i', block[:4])[0]
    at = block.index(b'\0', 4)                   # the end of the executable path
    while at < len(block) and block[at] == 0:    # its NUL padding
        at += 1
    for _ in range(argc):                        # the arguments
        at = block.index(b'\0', at) + 1
    found = []
    while at < len(block):
        end = block.find(b'\0', at)
        if end < 0:
            return None
        entry = block[at:end]
        if not entry:                            # the empty string that ends the environment
            return sorted(found)
        found.append(entry.split(b'=', 1)[0].decode('utf-8', 'backslashreplace'))
        at = end + 1
    # The block ended with no empty string after the arguments: the kernel gave no environment (as it does for an Apple
    # platform binary). That is not an empty environment, so nothing is reported.
    return None


def main(argv):
    if len(argv) != 1 or not argv[0].isdigit():
        print('usage: env_names.py <pid>', file=sys.stderr)
        return 2
    found = names(int(argv[0]))
    if found is None:
        return 2
    print('\n'.join(found))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
