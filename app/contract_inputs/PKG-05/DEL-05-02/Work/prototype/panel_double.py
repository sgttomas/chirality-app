"""Scripted loop-event double and failure-display reducer (PANEL-v0.8 §3.10, §7.1).

Prototype only, not product code (R12-3). Python 3 standard library only.

The double replays a scripted list of loop events (LOOP-v0.8 §2.3 meanings,
with the PROPOSED event ordinal of LOOP-v0.8 §2.3 E-6), can drop events to
simulate a delivery gap, and marks references that no longer resolve. The
reducer applies PANEL-v0.8 FD-1…FD-4 and prints what the panel would show,
one line per display item. It chooses no wording or layout (PANEL §0): the
strings are the display meanings the contract names.

Usage: python3 panel_double.py [fixtures/event_script.json]
"""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


TURN_FIELDS = ("hostIdentity", "conversationId", "runId", "turnId")


def valid_turn_ref(value):
    return (isinstance(value, dict) and set(value) == set(TURN_FIELDS)
            and all(isinstance(value[k], str) and value[k].strip() for k in TURN_FIELDS))


def reduce(events, unresolved):
    shown = []
    last = 0
    pending = {}  # request identity -> destination and original turn binding
    ended = set()
    failed = []
    withheld = set()
    for ev in events:
        n = ev["ordinal"]
        if n != last + 1:
            shown.append(f"FD-3 events {last + 1}-{n - 1} not received; nothing inferred for them")
        last = n
        kind = ev["kind"]
        if kind == "model interface failure":
            shown.append(f"FD-1 model interface failure: {ev['termination_reason']} (reported by {ev['reporter']})")
        elif kind == "turn failed":
            shown.append(f"FD-1 turn {ev['turn']} failed: {ev['cause']}; partial message shown as {ev['message_standing']}")
            binding = ev.get("turnRef")
            if not valid_turn_ref(binding) or binding["turnId"] != ev["turn"]:
                if pending:
                    withheld.update(pending)
                    shown.append("FD-4 failed-turn provenance unavailable; choices withheld; no closure or grant inferred")
                continue
            if binding not in failed:
                failed.append(copy.deepcopy(binding))
            for req, (dest, original) in sorted(list(pending.items())):
                if not valid_turn_ref(original):
                    withheld.add(req)
                    shown.append(f"FD-4 request {req}: source/turn binding unavailable; choices withheld; no closure inferred")
                elif original == binding and req not in withheld:
                    shown.append(f"FD-4 destination request {req} for {dest}: not answered, turn failed; no grant shown; requesting call not sent")
                    ended.add(req)
                    pending.pop(req)
        elif kind == "reference":
            ref = ev["reference"]
            if ref in unresolved:
                shown.append(f"FD-2 reference {ref} no longer resolves; last known label '{ev['label']}' kept, marked unresolved")
            else:
                shown.append(f"reference {ref} ('{ev['label']}')")
        elif kind == "destination request issued":
            req, binding = ev["request"], ev.get("turnRef")
            if req in ended or (valid_turn_ref(binding) and binding in failed):
                shown.append(f"FD-4 late request {req} withheld: turn failed; no choices or grant")
                ended.add(req)
                continue
            if req in pending:
                withheld.add(req)
                shown.append(f"FD-4 duplicate request {req}: provenance ambiguous; choices withheld")
                continue
            pending[req] = (ev["destination"], copy.deepcopy(binding))
            shown.append(f"destination request {req} for {ev['destination']} shown (ND-2)")
        elif kind in ("destination grant observed", "destination declined"):
            req = ev["request"]
            original = pending.get(req, (None, None))[1]
            if req in ended or req in withheld:
                shown.append(f"FD-4 late or ambiguous answer for request {req} withheld; no grant inferred")
                continue
            if valid_turn_ref(original) and ev.get("turnRef") != original:
                withheld.add(req)
                shown.append(f"FD-4 mismatched answer for request {req} withheld; no grant inferred")
                continue
            pending.pop(req, None)
            shown.append(f"{kind} for request {req}")
        elif kind == "run ended":
            for req, (dest, _) in sorted(pending.items()):
                shown.append(f"FD-4 destination request {req} for {dest}: not answered, run ended; no grant shown; requesting call not sent")
            pending.clear()
            shown.append(f"run ended ({ev['cause']})")
        else:
            shown.append(kind)
    return shown


def main(argv):
    path = argv[1] if len(argv) > 1 else os.path.join(HERE, "fixtures", "event_script.json")
    with open(path, encoding="utf-8") as fh:
        script = json.load(fh)
    failures = 0
    for case in script["cases"]:
        events = [e for e in case["events"] if e["ordinal"] not in set(case.get("drop", []))]
        got = reduce(events, set(case.get("unresolved", [])))
        ok = got == case["expected"]
        failures += 0 if ok else 1
        print(f"{'PASS' if ok else 'FAIL'} {case['id']}: {case['note']}")
        for line in got:
            print("     " + line)
        if not ok:
            print("     expected:", case["expected"])
    print(f"{len(script['cases']) - failures}/{len(script['cases'])} scripts as expected")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
