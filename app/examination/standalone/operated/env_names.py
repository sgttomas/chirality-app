#!/usr/bin/env python3
"""The names in one process's environment, and nothing else (DEL-09-02 examination tooling, macOS only).

    python3 -B env_names.py <pid> --expect-args '<JSON list of the target's arguments>' --require <NAME> [--require ...]

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
- THE TARGET, checked against what is independently known of it. The arguments parsed for the target must equal,
  exactly and in order, the arguments the caller knows the target was started with (from the source that starts it
  and the launch record), and the names must include each name the caller knows was set. If not, nothing is
  reported. Finding the arguments shows the parser found the boundary between arguments and environment in this
  process, not only in the calibration's children. A result without a required name, the empty result included, is
  not observed, never "nothing there".
- COMPLETENESS of the buffer: a block as long as the size asked for (it may have been cut), or one that does not end
  in NUL, is not observed.

What even this does not show: finding the arguments and a required name shows the framing is right for this process;
it does not by itself prove that no entry was skipped inside the environment area. Each entry is taken from one NUL
to the next, so an entry can be lost only if the block itself lacks it; that is the kernel's copy of what the process
was started with, and it is not checked further here.

The layout, from a supported source: the kernel's own source for the sysctl (xnu, bsd/kern/kern_sysctl.c,
sysctl_procargsx, which copies the string area from the process's stack and prepends argc for KERN_PROCARGS2) and for
the string area (bsd/kern/kern_exec.c: exec_save_path writes the path, exec_extract_strings pads it with NULs until
the remaining space is a multiple of the pointer size, then the arguments, then the environment, then the apple
strings). That source is published by Apple per release. It was not fetched for this change (the lane downloads
nothing): the functions are named so that a reader can check them, and which release this Mac runs, and that its
source reads the same, is not checked here. What remains measured: the alignment, on this Mac (path lengths 1 to 16, each with an
empty and a non-empty argv[0]), and, at every run, the calibration.

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
    """The process's KERN_PROCARGS2 block, or None if it cannot be read whole."""
    libc = ctypes.CDLL(ctypes.util.find_library('c'), use_errno=True)
    argmax = _sysctl(libc, [CTL_KERN, KERN_ARGMAX], ctypes.sizeof(ctypes.c_int))
    if argmax is None:
        return None
    size = struct.unpack('i', argmax)[0]
    block = _sysctl(libc, [CTL_KERN, KERN_PROCARGS2, pid], size)
    if block is None or len(block) >= size or not block.endswith(b'\0'):
        return None                              # it may have been cut, or its last string is not ended
    return block


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


def names(pid, args_match, required):
    """The sorted environment names of process pid, or None unless its block reads as above, its parsed arguments
    satisfy args_match (a list of bytes compared exactly, or a function of the list), and every required name is
    among the names."""
    parsed = parse(read_block(pid))
    if parsed is None or not required:
        return None
    arguments, found = parsed
    if not (args_match(arguments) if callable(args_match) else arguments == list(args_match)):
        return None
    return found if set(required) <= set(found) else None


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


USAGE = "usage: env_names.py <pid> --expect-args '<JSON list>' --require <NAME> [--require <NAME> ...]"


def main(argv):
    import json
    pid, expected, required = None, None, []
    rest = list(argv)
    try:
        pid = int(rest.pop(0)) if rest and rest[0].isdigit() else None
        while rest:
            flag, value = rest.pop(0), rest.pop(0)
            if flag == '--expect-args':
                expected = [item.encode() for item in json.loads(value)]
            elif flag == '--require' and value:
                required.append(value)
            else:
                raise ValueError(flag)
    except (IndexError, ValueError, TypeError, AttributeError):
        pid = None
    if pid is None or expected is None or not required:
        print(USAGE, file=sys.stderr)
        return 2
    if not calibrated():
        print('the calibration did not read back exactly: not observed', file=sys.stderr)
        return 2
    found = names(pid, expected, required)
    if found is None:
        return 2
    print('\n'.join(found))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
