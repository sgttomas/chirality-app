"""Validate the PROPOSED settings-in examples and check the AS §3.1 transitions (R12-3).

  python3 -B validate_settings_in.py

Prototype only; not product code. Uses the subset validator kept in
DEL-04-03's prototype folder (minischema.py). Besides the schema check, it
walks the in-work destination-grant transition table of AS-v0.8 §3.1 as a
small state machine and checks that every listed event sequence ends in the
state the table gives and that forbidden transitions are refused.
"""

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(HERE)
WORKING = os.path.dirname(os.path.dirname(DESIGN))
sys.path.insert(0, glob.glob(os.path.join(WORKING, "DEL-04-03_*", "Design", "prototype"))[0])
from minischema import Registry, validate  # noqa: E402

reg = Registry()
sid = reg.load(os.path.join(DESIGN, "AS_SETTINGS_IN.schema.json"))
schema = reg.by_id[sid]
ok = True
for name, expect in (("AS_SETTINGS_IN.valid.examples.json", True), ("AS_SETTINGS_IN.invalid.examples.json", False)):
    for c in json.load(open(os.path.join(DESIGN, name), encoding="utf-8")):
        e = validate(c["instance"], schema, reg)
        good = (not e) if expect else bool(e)
        ok &= good
        print(f"{c['case']} {'valid' if expect else 'invalid'}:", "PASS" if good else "FAIL", "-", (e[0][:100] if e and not expect else ""))

# AS §3.1 transition table (DG-1…DG-13), as (state, event) -> next state
T = {
    ("requested", "person grants"): "pending control confirmation",
    ("requested", "person declines"): "declined (no grant)",
    ("requested", "run ends"): "ended unanswered (no grant)",
    ("pending control confirmation", "control establishes"): "in force",
    ("pending control confirmation", "control refuses"): "refused",
    ("pending control confirmation", "confirmation lost"): "unconfirmed",
    ("unconfirmed", "control establishes"): "in force",
    ("in force", "requesting call contacts (once)"): "consumed",
    ("in force", "requesting call withdrawn (once)"): "consumed",
    ("in force", "run ends"): "ended with run",
    ("in force", "listed (always)"): "listed",
    ("in force", "confirmation lost"): "unconfirmed",
    ("listed", "later established list edit removes or narrows"): "superseded",
}
FORBIDDEN = [("requested", "timeout"), ("requested", "agent writes entry"), ("consumed", "requesting call contacts (once)"),
             ("ended with run", "new run starts"), ("refused", "control establishes"), ("declined (no grant)", "person grants")]
walks = [
    (["person grants", "control establishes", "requesting call contacts (once)"], "consumed"),
    (["person grants", "control establishes", "run ends"], "ended with run"),
    (["person grants", "control establishes", "requesting call withdrawn (once)"], "consumed"),
    (["person grants", "control establishes", "listed (always)", "later established list edit removes or narrows"], "superseded"),
    (["person grants", "control refuses"], "refused"),
    (["person grants", "confirmation lost", "control establishes"], "in force"),
    (["person declines"], "declined (no grant)"),
    (["run ends"], "ended unanswered (no grant)"),
]
for events, end in walks:
    s = "requested"
    for ev in events:
        s = T.get((s, ev), "REFUSED")
    good = s == end
    ok &= good
    print("walk", " -> ".join(events), "=", s, "PASS" if good else f"FAIL (expected {end})")
for s, ev in FORBIDDEN:
    good = (s, ev) not in T
    ok &= good
    print(f"forbidden: {s} + {ev}:", "PASS (no transition)" if good else "FAIL")
print("RESULT:", "all expectations held" if ok else "failures")
sys.exit(0 if ok else 1)
