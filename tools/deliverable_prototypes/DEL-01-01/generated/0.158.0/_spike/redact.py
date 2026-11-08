#!/usr/bin/env python3
"""W11 pin spike — redact raw handshake transcripts for commit.

Usage: redact.py <scratch-root> <out-dir>

Reads <scratch-root>/handshake/*.jsonl (written by handshake.mjs) and writes
redacted copies to <out-dir>. Redactions (labeled placeholders, per
HOSTING_BOUNDARY §9.1): scratch root path -> <SCRATCH>; host name -> <HOSTNAME>;
login user name in lsof/path text -> <USER>; installation id -> <INSTALLATION-ID>;
IP addresses -> <LOCAL-IP>/<REMOTE-IP>; lsof device/inode columns are kept.
The CODEX_HOME listing is collapsed below `.tmp/plugins/` and `skills/.system/`
to per-directory entry counts. A redacted transcript never claims byte identity
with the original exchange; frame content other than the replaced tokens is
unchanged. Spike evidence only.
"""
import json
import re
import sys
from pathlib import Path

scratch, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
user = Path.home().name
host_re = re.compile(r"\bprivate-host\b")
ip6_re = re.compile(r"\[[0-9a-f:]+\]:(\d+)->\[[0-9a-f:]+\]:(\d+)")
uuid_re = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b")


def scrub(s: str) -> str:
    s = s.replace(str(scratch), "<SCRATCH>")
    s = s.replace(str(scratch.resolve()), "<SCRATCH>")
    s = host_re.sub("<HOSTNAME>", s)
    s = ip6_re.sub(r"[<LOCAL-IP>]:\1->[<REMOTE-IP>]:\2", s)
    s = uuid_re.sub("<INSTALLATION-ID>", s)
    s = re.sub(rf"(?<![A-Za-z0-9_-]){re.escape(user)}(?![A-Za-z0-9_])", "<USER>", s)
    s = s.replace(f"-Users-{user}-", "-Users-<USER>-")
    return s


def collapse(entries):
    kept, counts = [], {}
    for e in entries:
        for prefix in (".tmp/plugins/", "skills/.system/"):
            if e.startswith(prefix) and e != prefix:
                counts[prefix] = counts.get(prefix, 0) + 1
                break
        else:
            kept.append(e)
    return kept + [f"{p} ... ({n} entries collapsed by redact.py)" for p, n in counts.items()]


for src in sorted((scratch / "handshake").glob("*.jsonl")):
    lines = []
    for raw in src.read_text().splitlines():
        ev = json.loads(raw)
        if ev.get("kind") == "codex-home-after":
            ev["entries"] = collapse(ev["entries"])
        ev.pop("frame", None)  # parsed copy of `raw`; `raw` is kept
        lines.append(scrub(json.dumps(ev, ensure_ascii=False)))
    (out / src.name).write_text("\n".join(lines) + "\n")
    print(f"{src.name}: {len(lines)} events")
