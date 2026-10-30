"""CC-REC-R9 local boundary-double settlement and acknowledgment checks."""
import run_cases as C
import recovery_model as M

for mode in ["ack", "boundary", "no-ack", "write-fail"]:
    store, ledger, variant = C.new_world({})
    app = M.AppSession(store, ledger, 1, variant); app.start_supplier()
    tid = app.new_conversation(); app.send_message(tid)
    turn = app.convs[tid]["liveTurn"]; sup = app.supplier()
    rid = sup.raise_request(tid, turn, sup.add_item(tid, turn, "dynamicToolCall"), "item/tool/requestUserInput")
    origin = "app-explicit-error" if mode == "boundary" else "app-rule:test-later-error"
    original_generation = app.g()
    assert app.register[rid]["state"] == "listed"
    assert app.protocol_error(rid, {"code": -32603, "message": "scripted error"}, "person-via-interaction") == "refused: origin-not-permitted"
    assert app.register[rid]["state"] == "listed"
    assert app.protocol_error(rid, {"code": -32603, "message": "scripted error"}, "app-rule:") == "refused: origin-not-permitted"
    assert app.register[rid]["state"] == "listed"
    if mode == "no-ack": sup._on_reply = lambda frame: None
    if mode == "write-fail": app._write = lambda home, frame: False
    assert app.protocol_error(rid, {"code": -32603, "message": "scripted error"}, origin) == "accepted-for-write"
    entry = app.register[rid]
    assert entry["g"] == original_generation and entry["origin"] == origin
    assert ("RQ-08", rid) not in app.trace and ("RQ-03", rid) in app.trace
    assert entry["replyWrite"] == ("write-failed" if mode == "write-fail" else "written")
    assert entry["endedAs"] == ("settle-write-failed" if mode == "write-fail" else "errored")
    if mode in ("ack", "boundary"): assert entry["ack"] == "observed" and ("RQ-09", rid) in app.trace
    if mode == "write-fail":
        app._on_notification(M.DEFAULT_HOME, "serverRequest/resolved", {"threadId": tid, "requestId": rid})
        assert "ack" not in entry and entry["endedAs"] == "settle-write-failed"
    # RT-15 requires the original full tuple, not only the same spawn counter.
    if mode == "no-ack":
        wrong = M.generation_ref("different-session", M.DEFAULT_HOME, 1)
        app._sink(M.DEFAULT_HOME, wrong, {"method": "serverRequest/resolved", "params": {"threadId": tid, "requestId": rid}})
        assert "ack" not in entry
    app.supplier_exits()
    if mode == "no-ack":
        app._on_notification(M.DEFAULT_HOME, "serverRequest/resolved", {"threadId": tid, "requestId": rid})
        assert entry["ack"] == "not-observed"  # closed generation cannot gain RT-15

    if mode == "no-ack": assert entry["ack"] == "not-observed" and ("RQ-05", rid) in app.trace
    if mode == "write-fail":
        assert "ack" not in entry and ("RQ-05", rid) not in app.trace
        assert not any(f.get("id") == rid and "error" in f for f in sup.writes)
    assert not C.check_records(app)
    summaries = [e for e in app.ledger_written if e["kind"] == "register_entry_summary" and e["requestIdentity"] == rid]
    assert all(e["generation"] == original_generation for e in summaries)
    assert not any(e.get("kind") == "human_act" for e in app.events + app.ledger_written)
    print("PASS later protocol error:", mode)
print("CC-REC-R9: named later settlement, failed-write uncertainty and distinct acknowledgment pass")
