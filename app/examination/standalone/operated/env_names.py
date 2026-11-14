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
- the executable path, ending in NUL, then NUL padding up to the next offset that is 4 plus a multiple of 8 (an empty
  argv[0] is a NUL too, so the padding's end is found by that alignment, never by skipping every NUL);
- argc arguments, each ending in NUL, any of them possibly empty;
- the environment entries, each name=value ending in NUL, closed by an empty string;
- the kernel's own "apple" strings.
The apple strings are not the environment and are not read as names.

The alignment is a fact about this kernel, measured (xnu pads the path so the string area stays pointer-aligned), not
one the system promises. So the read does not rest on it alone:
- CALIBRATION, at every run, before the real read. The script starts its own children from its own interpreter, each
  sleeping, with an invented environment, and reads each back by the same code: one with an empty argv[0], one with
  a non-empty argv[0] and an empty later argument, and one with an empty environment. Each must read back exactly as
  started. If any does not, the real read is not made.
- CONSISTENCY, on the real read. Exactly argc arguments are parsed; every entry after them, up to the empty string,
  is name=value with a non-empty name; and the empty string is followed by more of the block. Anything else is not
  read as an environment.
- An empty list is reported only when the calibration passed and the empty string that closes the environment comes
  straight after the arguments, with the block going on after it.

It exits 2 and prints nothing to standard output when the calibration fails, or when the block cannot be read (no such
process, another user's, or a refusal) or is not of that layout. The kernel gives no environment for an Apple platform
binary (seen with /bin/sleep on this Mac): its block ends exactly after the arguments. That is reported as not
observed, never as an empty environment.
"""
import ctypes
import ctypes.util
import struct
import subprocess
import sys
import time

CTL_KERN, KERN_ARGMAX, KERN_PROCARGS2 = 1, 8, 49

# The calibration's children: (argv, environment). Invented, and read back by the same code as the real read.
CALIBRATION = [
    (['', '-c', 'import time; time.sleep(30)'], {'INVENTED_CALIBRATION_ONE': 'one', 'INVENTED_CALIBRATION_TWO': 'a=b c'}),
    (['invented-argv0', '-c', 'import time; time.sleep(30)', ''], {'INVENTED_CALIBRATION_THREE': ''}),
    (['invented-argv0', '-c', 'import time; time.sleep(30)'], {}),
]


def _sysctl(libc, mib, size):
    mib_array = (ctypes.c_int * len(mib))(*mib)
    buffer = ctypes.create_string_buffer(size)
    length = ctypes.c_size_t(size)
    if libc.sysctl(mib_array, len(mib), buffer, ctypes.byref(length), None, 0) != 0:
        return None
    return buffer.raw[:length.value]


def read_block(pid):
    """The process's KERN_PROCARGS2 block, or None if it cannot be read."""
    libc = ctypes.CDLL(ctypes.util.find_library('c'), use_errno=True)
    argmax = _sysctl(libc, [CTL_KERN, KERN_ARGMAX], ctypes.sizeof(ctypes.c_int))
    if argmax is None:
        return None
    return _sysctl(libc, [CTL_KERN, KERN_PROCARGS2, pid], struct.unpack('i', argmax)[0])


def parse(block):
    """(arguments, sorted environment names) from a block, or None if it is not of the layout above."""
    if block is None or len(block) < 4:
        return None
    argc = struct.unpack('i', block[:4])[0]
    end = block.find(b'\0', 4)                   # the end of the executable path
    if end < 0 or argc < 0:
        return None
    at = end + 1
    while (at - 4) % 8:
        at += 1
    if at > len(block) or any(block[end:at]):    # the padding must be all NUL
        return None
    arguments = []
    for _ in range(argc):
        nul = block.find(b'\0', at)
        if nul < 0:
            return None
        arguments.append(block[at:nul])
        at = nul + 1
    if len(arguments) != argc:
        return None
    found = []
    while True:
        nul = block.find(b'\0', at)
        if nul < 0:
            return None                          # no empty string closes it: withheld, or a layout this does not know
        entry = block[at:nul]
        at = nul + 1
        if not entry:
            # The empty string that closes the environment. The block must go on (the kernel's own strings): a block
            # that ends here is not one whose environment was seen.
            return (arguments, sorted(found)) if at < len(block) else None
        name, equals, _ = entry.partition(b'=')
        if not equals or not name:
            return None
        found.append(name.decode('utf-8', 'backslashreplace'))


def names(pid):
    """The sorted environment names of process pid, or None if its argument block cannot be read as above."""
    parsed = parse(read_block(pid))
    return None if parsed is None else parsed[1]


def calibrated(timeout=5.0):
    """Whether each calibration child reads back exactly as it was started, by the same code as the real read."""
    for argv, environment in CALIBRATION:
        child = subprocess.Popen(argv, executable=sys.executable, env=environment,
                                 stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            wanted = ([arg.encode() for arg in argv], sorted(environment))
            deadline, seen = time.monotonic() + timeout, None
            while time.monotonic() < deadline:   # until the child has replaced the fork's copy of this process
                seen = parse(read_block(child.pid))
                if seen == wanted:
                    break
                time.sleep(0.05)
            if seen != wanted:
                return False
        finally:
            child.kill()
            child.wait()
    return True


def main(argv):
    if len(argv) != 1 or not argv[0].isdigit():
        print('usage: env_names.py <pid>', file=sys.stderr)
        return 2
    if not calibrated():
        print('the calibration did not read back exactly: not observed', file=sys.stderr)
        return 2
    found = names(int(argv[0]))
    if found is None:
        return 2
    if found:  # an empty environment, seen as above, prints nothing and exits 0
        print('\n'.join(found))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
