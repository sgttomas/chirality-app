#!/usr/bin/env python3
"""CC-H-RT-LATE focused offline boundary model checks; no supplier/process/network."""
import copy
import json
from pathlib import Path
import boundary_model as BM
import jsonschema_subset as V


EXERCISED = set()


class Writer:
    def __init__(self, result):
        self.result, self.frames = result, []

    def write(self, frame):
        if self.result == "written":
            self.frames.append(copy.deepcopy(frame))
        return self.result


def setup(result="written", classification="known-answerable"):
    b = BM.Boundary()
    b.state, b.generation = "ready", 1
    b.child = Writer(result)
    original_reg = b._reg
    def observed_reg(*args):
        original_reg(*args)
        EXERCISED.add(args[1])
    b._reg = observed_reg
    b.register[(1, json.dumps("late-1"))] = {
        "recordKind": "server-request-entry", "requestIdentity": "late-1", "generation": 1,
        "method": "item/tool/requestUserInput", "classification": classification,
        "originClass": "person-input" if classification == "known-answerable" else "none",
        "receiptPosition": 1, "state": "outstanding", "replyWriteResult": "not-attempted",
        "acknowledgmentObservation": {"status": "not-observed"}}
    return b, b.register[(1, json.dumps("late-1"))]


def resolve(b, counter=1):
    b._observe_notification({"generation": counter, "position": 2, "obj": {
        "method": "serverRequest/resolved", "params": {"requestId": "late-1", "threadId": "fixture-thread"}}})


def main():
    EXERCISED.clear()
    design = Path(__file__).resolve().parents[1]
    schema = json.loads((design / "hosting.server-request-entry.schema.json").read_text())
    native = {"code": -32000, "message": "named fixture later error", "data": {"fixture": True}}
    for origin in ({"class": "app-rule", "ruleName": "fixture-on-stop"}, {"class": "app-explicit-error"}):
        b, e = setup()
        generation = b.generation_identity(1)
        assert b.protocol_error("late-1", native, origin, generation=generation) == "accepted-for-write"
        assert e["state"] == "errored" and e["replyWriteResult"] == "written"
        assert e["settlement"] == {"kind": "error", "nativeContent": native, "origin": origin}
        assert e["acknowledgmentObservation"]["status"] == "not-observed"
        assert b.child.frames == [{"jsonrpc": "2.0", "id": "late-1", "error": native}]
        resolve(b, 2)
        assert e["acknowledgmentObservation"]["status"] == "not-observed"
        resolve(b)
        assert e["acknowledgmentObservation"]["status"] == "observed"
        assert {"RT-06", "RT-14", "RT-15"} <= b.register_transitions_used
        record = b.records()[0]
        assert record["generation"] == generation and not V.errors(record, schema, schema)
        assert not any(r.get("recordKind") == "human_act" for r in b.records())
    print("PASS named/boundary later error: RT06/14 write, matching RT15 ack, native origin/full H5 preserved; no human_act")
    for result in ("written", "write-failed"):
        b, e = setup(result)
        b.protocol_error("late-1", native, {"class": "app-rule", "ruleName": "fixture-rule"})
        if result == "write-failed":
            resolve(b)
            assert e["state"] == "settle-write-failed" and not b.child.frames
            assert "RT-09" in b.register_transitions_used and "RT-15" not in b.register_transitions_used
        assert e["acknowledgmentObservation"]["status"] == "not-observed"
        b._close_generation()
        b.state = "stopped"
        resolve(b)
        assert e["acknowledgmentObservation"]["status"] == "not-observed"
        assert not V.errors(b.records()[0], schema, schema)
    print("PASS written/no-ack close retains lack of ack; failed write RT09 stays unknown/no frame/no ack, even after resolution or close")
    for origin, error, generation in [
            ({"class": "person-via-interaction", "actorRef": "person:fixture (identity not verified)"}, native, None),
            ({"class": "app-rule", "ruleName": ""}, native, None),
            ({"class": "app-rule", "ruleName": "fixture"}, {"code": True, "message": "invalid"}, None),
            ({"class": "app-rule", "ruleName": "fixture"}, {"code": -32000, "message": "invalid", "data": float("nan")}, None),
            ({"class": "app-rule", "ruleName": "fixture"}, native, 1),
            ({"class": "app-rule", "ruleName": "fixture"}, native, {"appSession": "wrong", "home": "wrong", "spawnCounter": 1})]:
        b, e = setup()
        before = copy.deepcopy(e)
        assert b.protocol_error("late-1", error, origin, generation=generation).startswith("refused(")
        assert e == before and not b.child.frames
    print("PASS person/empty-rule/invalid native/full namespace mismatch refuse without state or transport mutation")
    # The receipt helper remains intentionally unchanged, including failed-write receipt accounting.
    for classification, row, origin in [("unfamiliar", "RT-02", {"class": "app-explicit-error"}),
            ("known-app-unsupported", "RT-03", {"class": "app-rule", "ruleName": "unsupported-kind"})]:
        for result in ("written", "write-failed"):
            b, e = setup(result, classification)
            e["state"] = "received"
            event = "classified-unfamiliar" if row == "RT-02" else "classified-known-app-unsupported"
            b._write_error(e, -32000, "receipt fixture", row, event, origin)
            resolve(b)
            assert e["state"] == "errored" and e["replyWriteResult"] == result
            assert e["acknowledgmentObservation"]["status"] == "not-observed"
            assert row in b.register_transitions_used and "RT-15" not in b.register_transitions_used
            assert not V.errors(b.records()[0], schema, schema)
    print("PASS RT02/03 receipt-time written/write-failed outcomes unchanged; no late-error ack routing")
    assert {"RT-14", "RT-15"} <= EXERCISED
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
