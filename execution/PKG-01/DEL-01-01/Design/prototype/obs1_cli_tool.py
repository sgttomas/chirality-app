#!/usr/bin/env python3
"""OBS-1 test tool, command-line path: prints one invented JSON result.

Prototype only (DEL-01-01, Wave B node B6); a test double for OBS-1's
optional command-line part (OBS-1 brief, O-7). Not product code. Python 3
standard library only. No network.

It writes nothing to disk (a read-only sandbox may deny writes), so its own
start time travels in its output: OBS-1 compares `toolStartedAtMs` with the
supplier's `item/started` `startedAtMs` for the `commandExecution` item.
If --probe-socket PATH is given, it tries to connect to a local Unix-domain
socket that the observation harness listens on, and reports whether the
connection was allowed (ADAPTER OC-5: the sandbox effect on a local-socket
CLI). It never opens an IP socket.

Usage: obs1_cli_tool.py --key EX-1 [--probe-socket PATH]
Exit status 0 for a found key, 3 for "EX-ERR" (invented not-found).
"""
import argparse
import json
import socket
import sys
import time


def main():
    started = int(time.time() * 1000)
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", required=True)
    ap.add_argument("--probe-socket")
    args = ap.parse_args()
    out = {"outcome": "queued" if args.key != "EX-ERR" else "not-found",
           "proposal": "P-EX-1" if args.key != "EX-ERR" else None, "key": args.key,
           "note": "invented example material", "toolStartedAtMs": started}
    if args.probe_socket:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            s.settimeout(2)
            s.connect(args.probe_socket)
            out["localSocket"] = "connected"
        except OSError as exc:
            out["localSocket"] = "refused: %s" % exc.__class__.__name__
        finally:
            s.close()
    sys.stdout.write(json.dumps(out) + "\n")
    return 0 if args.key != "EX-ERR" else 3


if __name__ == "__main__":
    sys.exit(main())
