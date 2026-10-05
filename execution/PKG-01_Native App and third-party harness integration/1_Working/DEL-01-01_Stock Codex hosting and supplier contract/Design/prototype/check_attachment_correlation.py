#!/usr/bin/env python3
"""Focused lean attachment-pointer custody model, no process/network/native/provider use."""
import copy
import json
from pathlib import Path
import boundary_model as BM
import jsonschema_subset as V


class Pipe:
    def __init__(self, result="written"):
        self.result, self.frames = result, []

    def write(self, frame):
        if self.result == "written":
            self.frames.append(copy.deepcopy(frame))
        return self.result


def host(result="written"):
    b = BM.Boundary()
    b.generation, b.state, b.child = 1, "ready", Pipe(result)
    return b


def association(token, steer=False):
    a = {"submissionRef": "submission:" + token, "threadId": "thread-fixture",
         "supplyRefs": ["attachment:" + token + ":first", "attachment:" + token + ":second"]}
    if steer:
        a["expectedTurnId"] = "turn-live"
    return a


def params(steer=False):
    p = {"threadId": "thread-fixture", "input": [{"type": "text", "text": "person text", "text_elements": []},
        {"type": "text", "text": "attached BOM/CRLF \ufeff\r\n", "text_elements": []}], "model": "person-selected"}
    if steer:
        p["expectedTurnId"] = "turn-live"
    return p


def reply(b, rec, result, counter=1, position=1):
    return b._correlate({"generation": counter, "position": position,
                        "obj": {"id": rec["requestIdentity"], "result": result}})


def main():
    schema = json.loads((Path(__file__).resolve().parents[1] / "hosting.client-request-record.schema.json").read_text())
    persisted = []
    b = host()
    a, payload = association("one"), params()
    def preserve(record):
        assert not b.child.frames
        assert record["outcome"] == "prepared-not-sent" and record["writeResult"] == "not-attempted"
        assert record["generation"] == b.generation_identity(1)
        assert record["submissionAssociation"] == a
        assert "params" not in record and "input" not in record and not V.errors(record, schema, schema)
        persisted.append(copy.deepcopy(record))
        return True
    rec = b.send("turn/start", payload, {"kind": "person-directed"}, a, preserve)
    assert rec["writeResult"] == "written" and rec["outcome"] == "pending"
    assert b.child.frames[0]["params"] == payload and "submissionAssociation" not in b.child.frames[0]
    assert "nativeTurnRef" not in b.resolve_submission(a["submissionRef"])
    original_assoc = copy.deepcopy(a)
    assert not reply(b, rec, {"turn": {"id": "wrong"}}, counter=2)
    assert reply(b, rec, {"turn": {"id": "turn-native"}})
    view = b.resolve_submission(a["submissionRef"])
    assert view["nativeTurnRef"] == "turn-native" and view["supplyRefs"] == a["supplyRefs"]
    assert rec["submissionAssociation"] == original_assoc
    assert not V.errors(b.records()[0], schema, schema)
    print("PASS before-write persistence/full namespace/ordered pointers, original native input and later exact RPC native turn; no synthetic wire field or immutable-ref rewrite")
    # Persistence is the owning source's exact complete-list validation barrier, not list syntax alone.
    for suffix, refs in [("missing", ["attachment:list:first"]), ("reordered", ["attachment:list:second", "attachment:list:first"]),
                         ("extra", ["attachment:list:first", "attachment:list:second", "attachment:list:third"])]:
        x = host()
        assoc = association("list")
        canonical = copy.deepcopy(assoc["supplyRefs"])
        assoc["supplyRefs"] = refs
        out = x.send("turn/start", params(), {"kind": "person-directed"}, assoc,
                     lambda r: r["submissionAssociation"]["supplyRefs"] == canonical)
        assert out["outcome"] == "prepared-not-sent" and not x.child.frames
    for persist in (lambda _: False, lambda _: (_ for _ in ()).throw(OSError("fixture persistence failure"))):
        x = host()
        out = x.send("turn/start", params(), {"kind": "person-directed"}, association("failure"), persist)
        assert out["writeResult"] == "not-attempted" and not x.child.frames
        assert x.resolve_submission("submission:failure")["dispatchStatus"] == "not-sent"
    x = host()
    duplicate = association("duplicate")
    duplicate["supplyRefs"] = ["attachment:duplicate:first", "attachment:duplicate:first"]
    try:
        x.send("turn/start", params(), {"kind": "person-directed"}, duplicate, lambda _: True)
        raise AssertionError("duplicate supply reference admitted")
    except ValueError:
        assert not x.child.frames
    # Owning source also checks original token, not just token syntax or filenames.
    x = host()
    assoc = association("wrong-owner-token")
    owning_facts = {r: {"turnRef": "submission:other"} for r in assoc["supplyRefs"]}
    out = x.send("turn/start", params(), {"kind": "person-directed"}, assoc,
                 lambda record: all(owning_facts[r]["turnRef"] == record["submissionAssociation"]["submissionRef"]
                                    for r in record["submissionAssociation"]["supplyRefs"]))
    assert out["outcome"] == "prepared-not-sent" and not x.child.frames
    print("PASS incomplete/reordered/extra owning list or failed/partial association persistence sends nothing")
    x = host()
    out = x.send("turn/start", params(), {"kind": "person-directed"}, association("cancel"), lambda _: True, lambda: True)
    assert not x.child.frames and out["outcome"] == "prepared-not-sent"
    for change in ("home", "session", "counter", "pipe"):
        x = host()
        original = x.generation_identity(1)
        original_pipe = x.child
        def change_scope(_):
            if change == "home": x.home = "other-home"
            elif change == "session": x.app_session = "other-session"
            elif change == "counter": x.generation += 1
            else: x.child = Pipe()
            return True
        out = x.send("turn/start", params(), {"kind": "person-directed"}, association("changed"), change_scope)
        assert not x.child.frames and not original_pipe.frames and out["outcome"] == "prepared-not-sent"
        assert x.records()[0]["generation"] == original
    print("PASS pre-send cancel and session/home/counter/pipe drift send nothing and preserve original namespace")
    x = host("write-failed")
    out = x.send("turn/start", params(), {"kind": "person-directed"}, association("uncertain"), lambda _: True)
    assert out["outcome"] == "unknown-no-response" and not x.child.frames
    assert not reply(x, out, {"turn": {"id": "not-inferred"}})
    assert "nativeTurnRef" not in x.resolve_submission("submission:uncertain")
    assert not V.errors(x.records()[0], schema, schema)
    try:
        x.send("turn/start", params(), {"kind": "person-directed"}, association("uncertain"), lambda _: True)
        raise AssertionError("duplicate token reused")
    except ValueError:
        pass
    # Cold metadata has original outer identity but no later source evidence or live noattempt observation.
    cold = host()
    saved = copy.deepcopy(persisted[0])
    cold.client[(1, saved["requestIdentity"])] = saved
    view = cold.resolve_submission("submission:one")
    assert view["generation"] == saved["generation"] and view["dispatchStatus"] == "prepared"
    assert "nativeTurnRef" not in view and not cold.child.frames
    saved["outcome"], saved["writeResult"] = "pending", "written"
    assert not reply(cold, saved, {"turn": {"id": "foreign-same-counter"}})
    print("PASS failed-write uncertainty, duplicate token no-resend and cold prepared crash gap/foreign same-counter response")
    x = host()
    first = x.send("turn/start", params(), {"kind": "person-directed"}, association("a"), lambda _: True)
    second = x.send("turn/start", params(), {"kind": "person-directed"}, association("b"), lambda _: True)
    assert reply(x, second, {"turn": {"id": "turn-b"}}, position=2)
    assert reply(x, first, {"turn": {"id": "turn-a"}}, position=3)
    assert x.resolve_submission("submission:a")["nativeTurnRef"] == "turn-a"
    assert x.resolve_submission("submission:b")["nativeTurnRef"] == "turn-b"
    for malformed in ([], "not-an-object", {}, {"turn": "invalid"}, {"turnId": "not-a-turn-start-result"}):
        z = host()
        r = z.send("turn/start", params(), {"kind": "person-directed"}, association("malformed"), lambda _: True)
        assert reply(z, r, malformed)
        assert "nativeTurnRef" not in z.resolve_submission("submission:malformed")
        assert not z.destination["turns"]
    for result in ({"turnId": "wrong-target"}, {"threadId": "foreign-thread", "turnId": "turn-live"}, {}):
        y = host()
        r = y.send("turn/steer", params(True), {"kind": "person-directed"}, association("steer", True), lambda _: True)
        assert reply(y, r, result)
        assert "nativeTurnRef" not in y.resolve_submission("submission:steer")
    y = host()
    r = y.send("turn/steer", params(True), {"kind": "person-directed"}, association("steer-ok", True), lambda _: True)
    reply(y, r, {"turnId": "turn-live"})
    assert y.resolve_submission("submission:steer-ok")["nativeTurnRef"] == "turn-live"
    plain = host()
    assert plain.send("turn/steer", params(True), {"kind": "person-directed"})["writeResult"] == "written"
    print("PASS out-of-order RPC response correlation; steer exact target/thread/missing-result checks; plain text steer independent")
    for owner in (x, y, b):
        assert all(not V.errors(r, schema, schema) for r in owner.records())
    control = persisted[0]
    assert not V.errors(control, schema, schema)
    for mutation in (lambda r: r.update(generation=None), lambda r: r.update(requestIdentity=None),
                     lambda r: r.update(outcome="pending"),
                     lambda r: r["submissionAssociation"].update(expectedTurnId="guessed-turn"),
                     lambda r: r["submissionAssociation"].update(supplyRefs=[])):
        bad = copy.deepcopy(control)
        mutation(bad)
        assert V.errors(bad, schema, schema)
    print("PASS all exported associated/generic records and prepared control validate; incomplete/null/pending/guessed-target negative cases rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
