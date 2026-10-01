#!/usr/bin/env python3
"""P-v0.8 §4.6: the per-item transition table and the derived proposal state,
as executable rules. Prototype only (R12-3); Python 3 standard library.

  python3 proposal_states.py                 # self-test: legal and illegal sequences
  python3 proposal_states.py --check RUN     # check an SH-1 run (C §10.8):
                                             # every observed item-state change is
                                             # reachable in the table, and every
                                             # reported derived state equals DS-1..DS-4

Since the RP-2 repair (R14-8 N-18), --check also verifies that every item
that left the queue carries its explicit item-left event (P §4.3) with the
matching cause and a time, and that no other item carries one.

Nothing here is host behaviour. The table is PROPOSED; the host decides what
it does, and the App receives it (P §4.6).
"""

import argparse
import json
import sys
from collections import deque
from pathlib import Path

# (from, event) -> to ; one row per P §4.6 PT-n. "∅" is "no item yet".
TABLE = {
    ("∅", "draft"): "drafted",                                     # PT-1  proposer (A1)
    ("drafted", "validated"): "validated",                         # PT-2  host
    ("drafted", "queued_on_submit"): "queued",                     # PT-3  host (validation and queueing reported together)
    ("validated", "queued"): "queued",                             # PT-3a host
    ("drafted", "refused_invalid"): "refused_invalid",             # PT-4  host
    ("drafted", "refused_stale"): "refused_stale",                 # PT-5  host
    ("drafted", "refused_not_permitted"): "refused_not_permitted", # PT-6  host
    ("validated", "applied_direct"): "applied",                    # PT-7  host (direct branch)
    ("validated", "application_error"): "application_error",       # PT-8  host (direct branch)
    ("queued", "A5"): "accepted",                                  # PT-9  the person
    ("queued", "A10"): "rejected",                                 # PT-10 the person
    ("queued", "A11"): "withdrawn",                                # PT-11 the proposer
    ("queued", "refused_stale"): "refused_stale",                  # PT-12 host (item left)
    ("queued", "cleared_no_record"): "left_queue",                 # PT-13 host (item left, R8-5)
    ("accepted", "applied_after_acceptance"): "applied",           # PT-14 host
    ("accepted", "refused_stale"): "refused_stale",                # PT-15 host; A5 kept (R2-16)
    ("accepted", "application_error"): "application_error",        # PT-16 host
    ("applied", "reversed"): "applied_then_reversed",              # PT-17 host (undo receipt)
}
TERMINAL = {"applied_then_reversed", "rejected", "withdrawn", "left_queue", "refused_invalid",
            "refused_not_permitted", "refused_stale", "application_error"}
OPEN = {"drafted", "validated", "queued", "accepted"}
LEFT = {"refused_stale", "refused_invalid", "refused_not_permitted", "withdrawn", "left_queue"}
LEFT_CAUSE = {"refused_stale": "refused_stale", "refused_invalid": "refused_invalid",
              "refused_not_permitted": "refused_not_permitted", "withdrawn": "withdrawn",
              "left_queue": "cleared_by_person_no_decision_record"}


def has_left(it):
    """P §4.3: the item left the queue without a person's A5 (an item refused after A5, PT-15, has not)."""
    if it["state"] in ("withdrawn", "left_queue"):
        return True
    return it["state"] in LEFT and "decision" not in it


def item_left_ok(it):
    """RP-2 (R14-8 N-18): the item-left event is explicit, with the matching cause and a time."""
    ev = it.get("item_left")
    if has_left(it):
        return bool(ev) and ev.get("cause") == LEFT_CAUSE[it["state"]] and bool(ev.get("time"))
    return ev is None


def step(state, event):
    """One transition; outcome unknown is an overlay (PT-18/PT-19), not a state change."""
    if event == "observation_lost":
        return state
    key = (state, event)
    if key not in TABLE:
        raise ValueError(f"illegal transition: {state} --{event}-->")
    return TABLE[key]


def reachable(a, b):
    if a == b:
        return True
    seen, q = {a}, deque([a])
    while q:
        s = q.popleft()
        for (f, _), t in TABLE.items():
            if f == s and t not in seen:
                if t == b:
                    return True
                seen.add(t)
                q.append(t)
    return False


def derive(items):
    """DS-1..DS-4."""
    counts = {}
    for it in items:
        counts[it["state"]] = counts.get(it["state"], 0) + 1
    summary = next(iter(counts)) if len(counts) == 1 else "mixed"            # DS-1
    decided = all("decision" in it or "item_left" in it for it in items)     # DS-4 (P §4.3): A5, A10 or an item-left event
    return {"summary": summary, "counts": counts,                             # DS-2
            "open": any(it["state"] in OPEN for it in items),                 # DS-3
            "all_items_decided": decided}


SEQUENCES = {
    "T5-T7 PR-1 (both items refused stale at first receipt)": [("draft", "refused_stale")],
    "T9-T12 PR-2 item 1 (accepted then applied)": [("draft", "queued_on_submit", "A5", "applied_after_acceptance")],
    "T9-T11 PR-2 item 2 (rejected)": [("draft", "queued_on_submit", "A10")],
    "V-S1 (accepted, then refused stale before application)": [("draft", "queued_on_submit", "A5", "refused_stale")],
    "SQ-P1 withdrawal": [("draft", "queued_on_submit", "A11")],
    "SQ-P3 direct branch failure": [("draft", "validated", "application_error")],
    "SQ-P4 partial application error after A5": [("draft", "queued_on_submit", "A5", "application_error")],
    "T16-T17 direct then undone": [("draft", "validated", "applied_direct", "reversed")],
    "V-OU1 lost observation leaves the state": [("draft", "queued_on_submit", "A5", "observation_lost")],
    "R8-5 queue cleared by the person": [("draft", "queued_on_submit", "cleared_no_record")],
}
ILLEGAL = {
    "queued item applied without A5": ("draft", "queued_on_submit", "applied_after_acceptance"),
    "rejected item later applied": ("draft", "queued_on_submit", "A10", "applied_after_acceptance"),
    "refused item re-queued (a re-draft is a new proposal)": ("draft", "refused_stale", "queued_on_submit"),
    "direct application reported as accepted": ("draft", "validated", "A5"),
    "application error becomes applied": ("draft", "queued_on_submit", "A5", "application_error", "applied_after_acceptance"),
}


def run_seq(events):
    s = "∅"
    for e in events:
        s = step(s, e)
    return s


def selftest():
    ok = True
    for name, [events] in SEQUENCES.items():
        try:
            print(f"PASS legal   {name}: ends {run_seq(events)}")
        except ValueError as e:
            ok = False
            print(f"FAIL legal   {name}: {e}")
    for name, events in ILLEGAL.items():
        try:
            run_seq(events)
            ok = False
            print(f"FAIL illegal {name}: accepted")
        except ValueError as e:
            print(f"PASS illegal {name}: {e}")
    for name, it, want in (
            ("T7 item refused stale at first receipt carries its event",
             {"state": "refused_stale", "item_left": {"cause": "refused_stale", "time": "t0003"}}, True),
            ("T7 item refused stale without an event", {"state": "refused_stale"}, False),
            ("V-S1 accepted then refused stale: not an item-left case",
             {"state": "refused_stale", "decision": {"act_kind": "A5"}}, True),
            ("V-S1 item wrongly carrying an item-left event",
             {"state": "refused_stale", "decision": {"act_kind": "A5"},
              "item_left": {"cause": "refused_stale", "time": "t1"}}, False),
            ("R8-5 cleared queue with cause 'cleared by the person'",
             {"state": "left_queue", "item_left": {"cause": "cleared_by_person_no_decision_record", "time": "t1"}}, True)):
        good = item_left_ok(it) == want
        ok &= good
        print(f"{'PASS' if good else 'FAIL'} IL  {name}: {'conforms' if item_left_ok(it) else 'does not conform'}")
    items = [{"state": "applied", "decision": {}}, {"state": "rejected", "decision": {}}]
    d = derive(items)
    good = d["summary"] == "mixed" and not d["open"] and d["all_items_decided"]
    ok &= good
    print(f"{'PASS' if good else 'FAIL'} DS  PR-2 after T12: {d}")
    d = derive([{"state": "queued"}, {"state": "queued"}])
    good = d["summary"] == "queued" and d["open"] and not d["all_items_decided"]
    ok &= good
    print(f"{'PASS' if good else 'FAIL'} DS  PR-2 after T10: {d}")
    return ok


def check_run(run):
    ok = True
    last = {}
    n = 0
    nl = 0
    for line in (Path(run) / "host_docs.jsonl").read_text().splitlines():
        rec = json.loads(line)
        doc = rec["doc"]
        if doc.get("kind") != "recorded_state":
            continue
        n += 1
        key = (rec["run"], doc["proposal_identity"])
        if derive(doc["items"]) != doc["derived_state"]:
            ok = False
            print(f"FAIL derived state {key} at {rec['step']}")
        for it in doc["items"]:
            if not item_left_ok(it):
                ok = False
                print(f"FAIL {key} item {it['item_identity']} ({it['state']}): item-left event missing, misplaced or wrong cause")
            nl += 1 if "item_left" in it else 0
            prev = last.get(key + (it["item_identity"],), "drafted")
            if not reachable(prev, it["state"]):
                ok = False
                print(f"FAIL {key} item {it['item_identity']}: {prev} -> {it['state']} not reachable")
            last[key + (it["item_identity"],)] = it["state"]
    print(f"{'PASS' if ok else 'FAIL'} {n} recorded-state documents: every item-state change reachable in the table; "
          f"every derived state equals DS-1..DS-4; every item that left carries its item-left event "
          f"({nl} item-left events, each with cause and time) and no other item carries one")
    for k, v in sorted(last.items()):
        print(f"      final {k[0]}/{k[1]} item {k[2]}: {v}")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check")
    a = ap.parse_args()
    ok = selftest()
    if a.check:
        ok &= check_run(a.check)
    print("RESULT:", "all checks passed" if ok else "failures")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
