#!/usr/bin/env python3
"""Redaction of kept probe captures (RV2 EUD1-R11; R23-48 item 3), by the
categories HOSTING-v0.9 §9.1 lists for a captured provider exchange.

Applied in place to every file of a results folder, and recorded in that
folder's REDACTION.json (categories, counts, method). Idempotent.

Categories handled here (those present in P-H1/P-H1b captures):
- installation identifier, and the session, thread, turn, window and
  context-window identifiers: every UUID-shaped value is replaced by a
  marker `<ID-n>` numbered in order of first appearance across the folder,
  so that equal identifiers stay equal and the observations stay readable
  (e.g. "the call and the next turn are on the same thread");
- the host's time zone: the `<timezone>` element's content and any IANA
  zone name it held;
- user name, home path and host name were already removed at capture
  (probe scripts' own check); this script re-checks them and fails if found.

Not redacted, with reason: the client identity text in `userAgent` is the
probe's own invented client name; the OS version is not a personal
identifier; timestamps are kept for ordering.

Usage: redact.py RESULTS_DIR [RESULTS_DIR ...]
"""
import json
import os
import re
import socket
import sys

UUID = re.compile(r"(?<![0-9a-f])[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}(?![0-9a-f])")  # also inside msg_… ids
TZ_ELEM = re.compile(r"<timezone>([^<]*)</timezone>")
MARK = re.compile(r"<ID-\d+>")


def redact_dir(d):
    files = sorted(f for f in os.listdir(d) if f != "REDACTION.json")
    texts = {f: open(os.path.join(d, f), encoding="utf-8").read() for f in files}
    ids, zones = {}, set()
    base = max([int(x[4:-1]) for t in texts.values() for x in MARK.findall(t)] or [0])  # never reuse a marker
    for f in files:
        for m in UUID.findall(texts[f]):
            ids.setdefault(m, f"<ID-{base + len(ids) + 1}>")
        zones.update(z for z in TZ_ELEM.findall(texts[f]) if z and z != "<REDACTED-TZ>")
    counts = {"identifiers": 0, "time_zone": 0}
    for f in files:
        t = texts[f]
        for raw, mark in ids.items():
            counts["identifiers"] += t.count(raw)
            t = t.replace(raw, mark)
        for z in zones:
            counts["time_zone"] += t.count(z)
            t = t.replace(z, "<REDACTED-TZ>")
        texts[f] = t
    user = os.environ.get("USER", "")
    host = socket.gethostname()
    leaks = [n for n in (os.path.expanduser("~"), host, host.split(".")[0], user, user.capitalize())
             if n and any(n in t for t in texts.values())]
    if leaks:
        raise SystemExit(f"{d}: user or host name present; not written")
    left = [f for f, t in texts.items() if UUID.search(t) or TZ_ELEM.search(t) and "<REDACTED-TZ>" not in TZ_ELEM.search(t).group(1)]
    if left:
        raise SystemExit(f"{d}: identifiers remain in {left}")
    for f, t in texts.items():
        with open(os.path.join(d, f), "w", encoding="utf-8") as h:
            h.write(t)
    prev = {}
    rp = os.path.join(d, "REDACTION.json")
    if os.path.exists(rp):
        prev = json.load(open(rp))
        if not any(counts.values()):
            return counts, len(ids)  # idempotent: nothing replaced, record unchanged
    rec = {"basis": "HOSTING-v0.9 §9.1 redaction categories; RV2 EUD1-R11; R23-48 item 3",
           "method": "redact.py: UUID-shaped identifiers -> <ID-n> (consistent within the folder); <timezone> content -> <REDACTED-TZ>; user, home and host names re-checked absent",
           "categories": ["installation identifier", "session, thread, turn, window and context-window identifiers", "host time zone"],
           "replaced_this_run": counts,
           "distinct_identifiers_this_run": len(ids),
           "kept_with_reason": {"userAgent client text": "the probe's own invented client name", "OS version": "not a personal identifier", "timestamps": "kept for ordering"},
           "earlier_runs": prev.get("earlier_runs", []) + ([{k: prev[k] for k in ("replaced_this_run", "distinct_identifiers_this_run") if k in prev}] if prev and any(prev.get("replaced_this_run", {}).values()) else [])}
    with open(rp, "w", encoding="utf-8") as h:
        h.write(json.dumps(rec, indent=2, ensure_ascii=False) + "\n")
    return counts, len(ids)


if __name__ == "__main__":
    for d in sys.argv[1:]:
        c, n = redact_dir(d)
        print(d, c, f"{n} distinct identifiers")
