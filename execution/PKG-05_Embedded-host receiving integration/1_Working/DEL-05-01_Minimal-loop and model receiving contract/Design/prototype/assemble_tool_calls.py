"""Assemble streamed tool-call fragments into complete calls (V-1, V-2).

Prototype only, not product code (R12-3). Python 3 standard library only.

The input streams are written in the shape of fixture basis FB-CC-1, the
published Chat Completions reference (OpenAI OpenAPI specification,
retrieved 2026-09-30; LOOP-v0.8 §4.1). FB-CC-1 is a fixture basis, not a
product selection (DEL-05-01 REQ-002). The output records use Chirality's
own names and are checked against ../LOOP_TOOL_CALL.schema.json.

Rules applied (LOOP-v0.8 §4.1 and §7; all PROPOSED until OBS-1):
  * fragments of one call are joined by their position ("index", the only
    member FB-CC-1 requires in a streamed tool-call chunk); argument text is
    appended in arrival order and never repaired (MC-9);
  * the correlation identity and the name are taken from the fragment that
    carries them; a later fragment of the same position that carries a
    different one is a conflict (MC-10);
  * the termination reason decides the whole response: stop / tool_calls
    complete; length -> every call truncated (MC-1); content_filter -> every
    call filtered (MC-11); deprecated function_call -> every call MC-4;
    stream ended with no termination reason -> every call interrupted (MC-2);
  * in a complete response each call is judged on its own (R12-7): argument
    text absent or empty -> MC-6; not JSON -> MC-3; JSON but not an object ->
    MC-4; tool type other than "function" -> MC-4; no correlation identity
    -> MC-4; name missing or not in the offered edition -> MC-5 (V-2);
    two positions sharing one correlation identity -> MC-7 for both;
  * a fragment with no position, or a chunk for a second choice, cannot be
    attributed: every call of the response is rejected (MC-13, MC-12).

Usage: python3 assemble_tool_calls.py [fixtures.json]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from schema_subset import validate  # noqa: E402

BASIS = "FB-CC-1"
TERMINATION = {
    "tool_calls": "tool-calls",
    "stop": "stop",
    "length": "length-truncated",
    "content_filter": "content-filtered",
    "function_call": "deprecated-function-call",
    None: "ended-without-reason",
}


def assemble(stream, offered):
    calls = {}          # position -> dict
    order = []
    finish = None
    response_fault = None   # (case, reason) that rejects every call
    for chunk in stream:
        for choice in chunk.get("choices", []):
            if choice.get("index", 0) != 0:
                response_fault = response_fault or ("MC-12", "chunk for a second choice; FB-CC-1 fixtures request one choice")
                continue
            delta = choice.get("delta") or {}
            if "function_call" in delta:
                response_fault = response_fault or ("MC-4", "deprecated function_call form, outside the fixture basis")
            for frag in delta.get("tool_calls") or []:
                pos = frag.get("index")
                if not isinstance(pos, int) or isinstance(pos, bool):
                    response_fault = response_fault or ("MC-13", "fragment without a position cannot be attributed to a call")
                    continue
                if pos not in calls:
                    calls[pos] = {"id": None, "type": None, "name": None, "args": None, "conflict": None}
                    order.append(pos)
                c = calls[pos]
                for key, val in (("id", frag.get("id")), ("type", frag.get("type")),
                                 ("name", (frag.get("function") or {}).get("name"))):
                    if val is None:
                        continue
                    if c[key] is None:
                        c[key] = val
                    elif c[key] != val and c["conflict"] is None:
                        c["conflict"] = f"later fragment carries a different {key}"
                fn = frag.get("function") or {}
                if "arguments" in fn and fn["arguments"] is not None:
                    c["args"] = (c["args"] or "") + fn["arguments"]
            if choice.get("finish_reason") is not None:
                finish = choice["finish_reason"]
    termination = TERMINATION.get(finish, "ended-without-reason")

    id_count = {}
    for pos in order:
        cid = calls[pos]["id"]
        if cid:
            id_count[cid] = id_count.get(cid, 0) + 1

    records = []
    for pos in sorted(order):
        c = calls[pos]
        rec = {
            "model_interface_basis": BASIS,
            "position_in_response": pos,
            "call_correlation_identity": c["id"],
            "operation_reference": c["name"],
            "argument_text": c["args"],
            "argument_value": None,
            "parse_state": "complete",
            "response_termination": termination,
            "rejection": None,
        }

        def reject(state, step, case, reason):
            rec["parse_state"] = state
            rec["rejection"] = {"step": step, "case": case, "reason": reason, "dispatched": False}

        if response_fault:
            reject("malformed", "V-1", response_fault[0], response_fault[1])
        elif finish is None:
            reject("interrupted", "V-1", "MC-2", "stream ended with no termination reason")
        elif finish == "length":
            reject("truncated", "V-1", "MC-1", "response cut off at the token limit")
        elif finish == "content_filter":
            reject("filtered", "V-1", "MC-11", "content omitted by the service's filter")
        elif finish == "function_call":
            reject("malformed", "V-1", "MC-4", "deprecated function_call termination, outside the fixture basis")
        elif c["conflict"]:
            reject("malformed", "V-1", "MC-10", c["conflict"])
        elif c["type"] not in (None, "function"):
            reject("malformed", "V-1", "MC-4", f"tool type {c['type']!r} is outside the fixture basis")
        elif not c["id"]:
            reject("malformed", "V-1", "MC-4", "no call correlation identity")
        elif id_count.get(c["id"], 0) > 1:
            reject("malformed", "V-1", "MC-7", "correlation identity shared with another call")
        elif c["args"] is None or c["args"] == "":
            reject("malformed", "V-1", "MC-6", "argument text absent or empty; never coerced to no arguments")
        else:
            try:
                value = json.loads(c["args"])
            except ValueError:
                reject("malformed", "V-1", "MC-3", "argument text is not JSON")
            else:
                if not isinstance(value, dict):
                    reject("malformed", "V-1", "MC-4", "argument JSON is not an object")
                elif not c["name"] or c["name"] not in offered:
                    rec["argument_value"] = value
                    reject("complete", "V-2", "MC-5", "operation reference missing or not in the offered edition")
                else:
                    rec["argument_value"] = value
        records.append(rec)
    return records, termination


def main(argv):
    path = argv[1] if len(argv) > 1 else os.path.join(HERE, "fixtures", "stream_fixtures.json")
    with open(path, encoding="utf-8") as fh:
        suite = json.load(fh)
    with open(os.path.join(HERE, "..", "LOOP_TOOL_CALL.schema.json"), encoding="utf-8") as fh:
        schema = json.load(fh)
    failures = 0
    for case in suite["cases"]:
        records, termination = assemble(case["chunks"], set(suite["offered_edition"]))
        got = [{"position": r["position_in_response"], "parse_state": r["parse_state"],
                "case": (r["rejection"] or {}).get("case")} for r in records]
        schema_errs = [e for r in records for e in validate(r, schema)]
        ok = got == case["expected"] and not schema_errs
        failures += 0 if ok else 1
        print(f"{'PASS' if ok else 'FAIL'} {case['id']:<8} {case['maps_to']:<14} termination={termination:<22} "
              + "; ".join(f"#{g['position']} {g['parse_state']}{'/' + g['case'] if g['case'] else ''}" for g in got))
        if not ok:
            print("     expected:", case["expected"])
            print("     got:     ", got)
            for e in schema_errs:
                print("     schema:", e)
    print(f"{len(suite['cases']) - failures}/{len(suite['cases'])} cases as expected; every record checked against LOOP_TOOL_CALL.schema.json")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
