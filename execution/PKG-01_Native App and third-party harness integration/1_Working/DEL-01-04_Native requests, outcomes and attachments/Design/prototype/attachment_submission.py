"""CC-NIR-ATTACHMENT-REF candidate model; invented snapshots, no native IO.

Existing HOSTING client custody owns outer generation/RPC/method and its
pointer-only submissionAssociation. No companion schema/store/transcript.
Durable persistence is modeled by callbacks; real filesystem checks remain.
"""
from copy import deepcopy
import hashlib
import json
import nir_model as nm


def native_path(raw):
    """Byte-path host identity is lossless; display is never a dispatch path."""
    identity = {"encoding": "native-bytes-hex", "value": raw.hex()}
    try:
        exact = raw.decode("utf-8")
    except UnicodeDecodeError:
        exact = None
    return {"identity": identity, "display": raw.decode("utf-8", errors="backslashreplace"),
            "supplierPath": exact}


def exact_path_for_supplier(selection):
    path = selection["supplierPath"]
    if path is None or path.encode("utf-8").hex() != selection["identity"]["value"]:
        raise ValueError("selected native path unavailable in supplier string; no lossy dispatch")
    return path


def attachment_ref(record):
    return "attachment:" + record["attachmentId"]


def resolve_list(association, records):
    refs = association["supplyRefs"]
    if len(refs) != len(set(refs)) or not refs:
        raise ValueError("ordered supply references empty or repeat")
    by_id = {}
    for record in records:
        ref = attachment_ref(record)
        if ref in by_id:
            raise ValueError("attachment identity repeats")
        by_id[ref] = record
    if [attachment_ref(r) for r in records] != refs:
        raise ValueError("supply list missing, extra or reordered")
    for ref in refs:
        if not ref.startswith("attachment:") or ref not in by_id:
            raise ValueError("owning attachment reference unavailable")
        r = by_id[ref]
        if r["turnRef"] != association["submissionRef"]:
            raise ValueError("foreign submission record")
        if r["identityAtSelection"] != r["identityAtSubmission"]:
            raise ValueError("changed or unavailable content; confirmation required")
    return [deepcopy(by_id[ref]) for ref in refs]


class Submission:
    def __init__(self, records, generation, rpc_id, thread, method="turn/start", expected_turn=None):
        if method not in ("turn/start", "turn/steer") or not records:
            raise ValueError("supported method and supply list required")
        token = records[0]["turnRef"]
        if not token.startswith("submission:"):
            raise ValueError("new pre-send submission needs explicit App token")
        association = {"submissionRef": token, "threadId": thread,
                       "supplyRefs": [attachment_ref(r) for r in records]}
        if method == "turn/steer":
            if not expected_turn:
                raise ValueError("observed expectedTurnId required")
            association["expectedTurnId"] = expected_turn
        elif expected_turn is not None:
            raise ValueError("expected turn belongs to steering only")
        resolve_list(association, records)
        self.records = deepcopy(records)
        self.custody = {"recordKind": "client-request", "generation": deepcopy(generation),
                       "requestIdentity": rpc_id, "method": method,
                       "initiator": {"kind": "person-directed"},
                       "writeResult": "not-attempted", "outcome": "prepared-not-sent",
                       "submissionAssociation": association}
        if rpc_id is None or set(generation) != {"appSession", "home", "spawnCounter"}:
            raise ValueError("allocated RPC and full generation required")
        self.ready = False
        self.hot = True
        self.cancelled = False
        self.native_turn = None
        self.native_response_source = None  # reference to existing hosting observation, never a payload copy/store
        self.observation_limit = None
        self.sent = False

    def persist_before_send(self, write_supply, write_custody):
        for record in self.records:
            if not write_supply(deepcopy(record)):
                return "held: supply persistence failed; no dispatch"
        if not write_custody(deepcopy(self.custody)):
            return "held: client custody persistence failed; no dispatch"
        self.ready = True
        return "prepared; not sent"

    def dispatch(self, write_native):
        if not self.ready or not self.hot or self.cancelled or self.sent:
            raise ValueError("dispatch refused: not ready/hot, cancelled or already attempted")
        resolve_list(self.custody["submissionAssociation"], self.records)
        self.sent = True
        outcome = write_native()
        self.custody["writeResult"] = outcome
        self.custody["outcome"] = "pending" if outcome == "written" else "unknown-no-response"
        return self.custody["outcome"]

    def observe_response(self, generation, frame, receipt_position):
        # Existing HOSTING owns the original frame. This model retains only a
        # reference to its admitted observation and source metadata in custody.
        if (not isinstance(frame, dict) or generation != self.custody["generation"]
                or frame.get("id") != self.custody["requestIdentity"]):
            return "uncorrelated identity; original frame retained by hosting source"
        if self.custody["outcome"] != "pending" or self.custody["writeResult"] != "written":
            self.observation_limit = "uncorrelated repeat or request not pending/written; first settled source preserved"
            return self.observation_limit
        if not isinstance(receipt_position, int) or isinstance(receipt_position, bool) or receipt_position < 1:
            return "invalid source receipt position; native turn unknown"
        self.native_response_source = frame
        self.custody["responseReceiptPosition"] = receipt_position
        if "error" in frame:
            error = frame["error"]
            if ("result" not in frame and isinstance(error, dict) and isinstance(error.get("code"), int)
                    and not isinstance(error["code"], bool) and isinstance(error.get("message"), str)):
                self.custody.update(outcome="response-observed-error", error=deepcopy(error))
                self.observation_limit = "native refusal; no native turn or resend"
            else:
                self.custody["outcome"] = "unknown-no-response"
                self.observation_limit = "malformed native error/result envelope; source retained, native turn unknown"
            return self.observation_limit
        # One owning RPC reply settles source observation even if its result
        # cannot establish a turn. A later same-RPC reply cannot replace it.
        self.custody["outcome"] = "response-observed-result"
        result = frame.get("result")
        if not isinstance(result, dict):
            self.observation_limit = "malformed result; source retained, native turn unknown"
            return self.observation_limit
        association = self.custody["submissionAssociation"]
        if result.get("threadId", association["threadId"]) != association["threadId"]:
            self.observation_limit = "foreign result thread; source retained, native turn unknown"
            return self.observation_limit
        method = self.custody["method"]
        native = result.get("turn")
        turn = native.get("id") if method == "turn/start" and isinstance(native, dict) else None
        if method == "turn/steer":
            turn = result.get("turnId")
        if not isinstance(turn, str) or not turn:
            self.observation_limit = "native turn missing/malformed; source retained"
            return self.observation_limit
        if method == "turn/steer" and turn != association["expectedTurnId"]:
            self.observation_limit = "result differs from explicit steer target; unknown"
            return self.observation_limit
        self.native_turn = turn
        self.observation_limit = None
        return "native turn correlated; provider adoption not observed"

    def reload(self):
        new = deepcopy(self)
        new.hot = False
        new.ready = False
        return new

    def dispatch_observation(self):
        if not self.hot and self.custody["writeResult"] == "not-attempted":
            return "dispatch unknown/unavailable after restart"
        if self.cancelled and not self.sent:
            return "not sent: cancellation/no-attempt observed in current process"
        return self.custody["writeResult"]


def main():
    count = 0
    def check(condition, label):
        nonlocal count
        count += 1
        if not condition:
            raise AssertionError(label)
        print("PASS " + label)
    def refuses(fn):
        try:
            fn()
        except ValueError:
            return True
        return False
    gen = {"appSession": "submission-fixture", "home": "account", "spawnCounter": 1}
    def rec(aid, data=b"alpha\r\n", selected=None, token="submission:fixture-one"):
        element, text = nm.attachment_input("text-element", "f.md", "/fixture/f.md", data)
        r, why = nm.supply_record(aid, "f.md", "text-element", "/fixture/f.md", data if selected is None else selected,
                                  data, token, "fixture-time", element_text=text)
        return r, why, element
    r, why, element = rec("att-one")
    check(why == "prepared; not sent", "AS-1 App token produces prepared supply, never sent claim")
    check(element["text"].endswith("alpha\r\n"), "AS-2 file text preserves CRLF and exact trailing bytes")
    for size in (262143, 262144, 262145):
        check(nm.carrier_for("f.txt", b"x" * size) == ("text-element" if size <= 262144 else "path-named"),
              f"AS-3 file-byte boundary {size}")
    _, wrapped = nm.attachment_input("text-element", "long" * 200, "/long/" * 200, b"x" * 262144)
    check(len(wrapped.encode("utf-8")) > 262144 and nm.carrier_for("f.txt", b"x" * 262144) == "text-element",
          "AS-4 wrapper overhead does not change per-file eligibility")
    check(nm.carrier_for("f.txt", b"x\x00") == "path-named" and nm.carrier_for("f.txt", b"\xff") == "path-named",
          "AS-5 NUL/non-UTF8 content uses existing named carrier")
    check(nm.carrier_for("f.png", b"invented-image") == "localImage", "AS-6 image route preserved; no provider witness")
    selected = native_path(b"/fixture/\xff.md")
    check(bytes.fromhex(selected["identity"]["value"]) == b"/fixture/\xff.md" and selected["supplierPath"] is None,
          "AS-7 native path identity lossless and display separate")
    check(refuses(lambda: exact_path_for_supplier(selected)), "AS-8 non-UTF8 path never dispatches lossy display")
    good = native_path("/fixture/ü.md".encode("utf-8"))
    check(exact_path_for_supplier(good) == "/fixture/ü.md", "AS-9 exact UTF8 path round-trips original bytes")
    r2, _, _ = rec("att-two", b"second")
    sub = Submission([r, r2], gen, "rpc-one", "thread-one")
    check(sub.custody["submissionAssociation"]["supplyRefs"] == ["attachment:att-one", "attachment:att-two"],
          "AS-10 immutable ordered owning supply refs; no outer fields duplicated")
    check(refuses(lambda: resolve_list(sub.custody["submissionAssociation"], [r2, r])), "AS-11 reordered list refused")
    bad = deepcopy(r); bad["turnRef"] = "submission:other"
    check(refuses(lambda: Submission([r, bad], gen, "rpc", "thread")), "AS-12 duplicate identity/foreign list refused")
    foreign_record = deepcopy(r2); foreign_record["turnRef"] = "submission:other"
    check(refuses(lambda: resolve_list(sub.custody["submissionAssociation"], [r, foreign_record])),
          "AS-12a distinct record from foreign submission refused")
    check(refuses(lambda: resolve_list(sub.custody["submissionAssociation"], [r])), "AS-12b missing record refused")
    extra, _, _ = rec("att-extra")
    check(refuses(lambda: resolve_list(sub.custody["submissionAssociation"], [r, r2, extra])), "AS-12c extra record refused")
    changed, _, _ = rec("att-changed", b"changed", selected=b"selected")
    check(refuses(lambda: Submission([changed], gen, "rpc", "thread")), "AS-13 changed bytes held before send")
    failed = Submission([r, r2], gen, "rpc", "thread")
    calls = []
    failed.persist_before_send(lambda x: calls.append(x) or len(calls) < 2, lambda x: True)
    check(refuses(lambda: failed.dispatch(lambda: "written")), "AS-14 any member persistence failure prevents dispatch")
    failed = Submission([r], gen, "rpc", "thread")
    failed.persist_before_send(lambda x: True, lambda x: False)
    check(refuses(lambda: failed.dispatch(lambda: "written")), "AS-15 custody association persistence failure prevents dispatch")
    sub.persist_before_send(lambda x: True, lambda x: True)
    cold = sub.reload()
    check(cold.dispatch_observation().startswith("dispatch unknown") and refuses(lambda: cold.dispatch(lambda: "written")),
          "AS-16 cold prepared record neither proves no write nor resends")
    sub.cancelled = True
    check(refuses(lambda: sub.dispatch(lambda: "written")), "AS-17 observed pre-dispatch cancellation sends nothing")
    sub = Submission([r], gen, "rpc-one", "thread-one"); sub.persist_before_send(lambda x: True, lambda x: True)
    sub.dispatch(lambda: "written")
    check(refuses(lambda: sub.dispatch(lambda: "written")), "AS-18 pending written input never auto-resends")
    foreign = dict(gen, home="other")
    check(sub.observe_response(foreign, {"id": "rpc-one", "result": {"turn": {"id": "turn-one"}}}, 1).startswith("uncorrelated"),
          "AS-19 equal counter in foreign home cannot correlate")
    check(sub.observe_response(gen, {"method": "turn/started", "params": {"turn": {"id": "nearby"}}}, 2).startswith("uncorrelated"),
          "AS-20 nearby native event cannot substitute RPC correlation")
    check(sub.observe_response(gen, {"id": "rpc-one", "result": {"turn": {"id": "turn-one"}}}, 3).startswith("native turn correlated")
          and sub.records[0]["turnRef"] == "submission:fixture-one", "AS-21 exact native result joins without rewriting original token")
    steer = Submission([r], gen, "rpc-steer", "thread-one", "turn/steer", "turn-live")
    steer.persist_before_send(lambda x: True, lambda x: True); steer.dispatch(lambda: "written")
    check(steer.observe_response(gen, {"id": "rpc-steer", "result": {"turnId": "other"}}, 4).startswith("result differs"),
          "AS-22 wrong steer target remains unknown")
    check(steer.observe_response(gen, {"id": "rpc-steer", "result": {"turnId": "turn-live"}}, 5).startswith("uncorrelated repeat")
          and steer.native_turn is None, "AS-22a settled wrong-target reply cannot be replaced by repeat")
    steer = Submission([r], gen, "rpc-steer-good", "thread-one", "turn/steer", "turn-live")
    steer.persist_before_send(lambda x: True, lambda x: True); steer.dispatch(lambda: "written")
    check(steer.observe_response(gen, {"id": "rpc-steer-good", "result": {"turnId": "turn-live"}}, 6).startswith("native turn correlated"),
          "AS-23 actual expected steer result correlates on owning pending request; no fallback start")
    check("input" not in steer.custody and "text" not in json.dumps(steer.custody), "AS-24 custody contains pointers only, no raw transcript")
    def pending(rpc="rpc-review", method="turn/start", target=None):
        candidate = Submission([r], gen, rpc, "thread-one", method, target)
        candidate.persist_before_send(lambda x: True, lambda x: True); candidate.dispatch(lambda: "written")
        return candidate
    foreign = pending()
    raw = {"id": "rpc-review", "result": {"threadId": "foreign", "turn": {"id": "foreign-native-turn"}}}
    check(foreign.observe_response(gen, raw, 7).startswith("foreign result thread") and foreign.native_turn is None
          and foreign.native_response_source is raw, "AR-1 contradictory reported thread cannot establish native turn; source preserved")
    for payload in ({"turn": None}, {"turn": []}, {"turn": "invalid"}, {"turn": {}}, None, []):
        malformed = pending()
        raw = {"id": "rpc-review", "result": payload}
        response = malformed.observe_response(gen, raw, 8)
        check(malformed.native_turn is None and malformed.native_response_source is raw
              and malformed.custody["outcome"] == "response-observed-result",
              f"AR-2 malformed/null turn safely retains source with native turn unknown: {payload!r}")
    settled = pending()
    original = {"id": "rpc-review", "result": {"turn": {"id": "first"}}}
    settled.observe_response(gen, original, 9)
    result = settled.observe_response(gen, {"id": "rpc-review", "result": {"turn": {"id": "second"}}}, 10)
    check(result.startswith("uncorrelated repeat") and settled.native_turn == "first"
          and settled.native_response_source is original and settled.custody["responseReceiptPosition"] == 9,
          "AR-3 conflicting settled RPC repeat preserves first native turn/source/receipt")
    prepared = Submission([r], gen, "rpc-review", "thread-one")
    prepared.persist_before_send(lambda x: True, lambda x: True)
    check(prepared.observe_response(gen, original, 11).startswith("uncorrelated repeat") and prepared.native_turn is None
          and prepared.native_response_source is None, "AR-4 unsent prepared request cannot accept a native turn reply")
    failed_write = Submission([r], gen, "rpc-review", "thread-one")
    failed_write.persist_before_send(lambda x: True, lambda x: True); failed_write.dispatch(lambda: "write-failed")
    check(failed_write.observe_response(gen, original, 12).startswith("uncorrelated repeat") and failed_write.native_turn is None,
          "AR-5 uncertain failed write cannot become a correlated native turn")
    refused = pending(); error = {"id": "rpc-review", "error": {"code": -32000, "message": "fixture refusal"}}
    check(refused.observe_response(gen, error, 13).startswith("native refusal") and refused.native_turn is None
          and refused.native_response_source is error, "AR-6 actual native error remains refusal/source, never accepted")
    check(refused.observe_response(gen, original, 14).startswith("uncorrelated repeat") and refused.native_response_source is error
          and refused.custody["outcome"] == "response-observed-error", "AR-7 error-settled RPC cannot later acquire a turn")
    foreign_steer = pending("rpc-review", "turn/steer", "turn-live")
    check(foreign_steer.observe_response(gen, {"id": "rpc-review", "result": {"threadId": "foreign", "turnId": "turn-live"}}, 15)
          .startswith("foreign result thread") and foreign_steer.native_turn is None,
          "AR-8 steering also refuses contradictory reported thread")
    malformed_error = pending()
    source_error = {"id": "rpc-review", "error": None}
    check(malformed_error.observe_response(gen, source_error, 16).startswith("malformed native error")
          and malformed_error.native_turn is None and malformed_error.native_response_source is source_error,
          "AR-9 malformed error retains raw source with native turn unknown")
    # Actual co-owner successor schema, not a copied/reworded acceptance oracle.
    import importlib.util
    from pathlib import Path
    host_design = next(Path(__file__).resolve().parents[3].glob("DEL-01-01*/Design"))
    spec = importlib.util.spec_from_file_location("attachment_host_schema_validator", host_design / "prototype/jsonschema_subset.py")
    validator = importlib.util.module_from_spec(spec); spec.loader.exec_module(validator)
    schema = json.loads((host_design / "hosting.client-request-record.schema.json").read_text())
    check(schema["$id"] == "urn:chirality:del-01-01:hosting-boundary:v0.10:client-request-record",
          "AR-10 joined validator uses exact owning HOSTING v0.10 successor")
    for name, candidate in [("prepared", prepared), ("written-pending", pending()), ("settled", settled),
                             ("native-error", refused), ("failed-write", failed_write),
                             ("foreign-thread", foreign), ("malformed-result", malformed),
                             ("malformed-error", malformed_error), ("steer", steer)]:
        check(not validator.errors(candidate.custody, schema, schema), f"AR-11 actual HOSTING schema accepts {name} source state")
    print(f"{count} checks, 0 failed; model only, no native/durable filesystem/provider witness")

if __name__ == "__main__":
    main()
