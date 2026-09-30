#!/usr/bin/env python3
"""Run the HOSTING-BOUNDARY-v0.8 cases that the file marks runnable with a
supplier double (Verification cases, "Runnable now?"), plus the checks on the
double itself, the three PROPOSED schemas and their conformance fixtures.

Prototype only (DEL-01-01, Wave B node B6); not product code. Python 3
standard library only. No network. It never starts the Codex binary.

Usage:  python3 run_cases.py [--keep-logs DIR]
Exit status 0 when every case and check gives its expected result.

Result words (HOSTING §9.3 labels, bound to the candidate): here the
candidate is the boundary *model* in boundary_model.py, so a "pass" means
"the rules run as written against the double" and never a VER pass.
"""
import argparse
import glob
import json
import os
import signal
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import boundary_model as BM  # noqa: E402
import jsonschema_subset as V  # noqa: E402

DESIGN = os.path.dirname(HERE)
HOSTING = os.path.join(DESIGN, "HOSTING_BOUNDARY.md")
SCHEMAS = {k: json.load(open(os.path.join(DESIGN, "hosting.%s.schema.json" % k), encoding="utf-8"))
           for k in ("lifecycle-event", "client-request-record", "server-request-entry")}
KIND_TO_SCHEMA = {"lifecycle-event": "lifecycle-event", "client-request": "client-request-record",
                  "server-request-entry": "server-request-entry"}
ROOT = json.load(open(BM.BUNDLE, encoding="utf-8"))
RESP = {"initialize": "#/definitions/InitializeResponse",
        "thread/start": "#/definitions/v2/ThreadStartResponse",
        "turn/start": "#/definitions/v2/TurnStartResponse",
        "turn/interrupt": "#/definitions/v2/TurnInterruptResponse",
        "mcpServerStatus/list": "#/definitions/v2/ListMcpServerStatusResponse",
        "mcpServer/tool/call": "#/definitions/v2/McpServerToolCallResponse"}

RESULTS, ALL_RECORDS, LOG_DIRS = [], [], []
LT_USED, RT_USED = set(), set()


def result(case, ok, detail):
    RESULTS.append((case, "pass (model)" if ok else "FAIL", detail))


def new_boundary(**kw):
    d = tempfile.mkdtemp(prefix="b6-", dir=os.environ.get("TMPDIR"))
    LOG_DIRS.append(d)
    return BM.Boundary(log_dir=d, **kw)


def finish(b):
    if b.state == "ready":
        b.stop()
    ALL_RECORDS.extend(b.records())
    LT_USED.update(b.transitions_used)
    RT_USED.update(b.register_transitions_used)


def entry(b, rid, g=None):
    return b.register[(g or b.generation, json.dumps(rid))]


def double_log(b, g=None):
    path = os.path.join(b.log_dir, "double-g%d.jsonl" % (g or b.generation))
    return [json.loads(line) for line in open(path, encoding="utf-8")] if os.path.exists(path) else []


def app_frames(b, g=None):
    return [json.loads(ev["raw"]) for ev in double_log(b, g) if ev["dir"] == "recv-from-app"]


# ---------------------------------------------------------------------------
def seed_fidelity():
    """SEED-n: seeded from transcript n and driven with its own `send` frames,
    the double must emit exactly the recorded supplier frames, byte for byte,
    in order, and exit with code 0 (end of input, or SIGTERM for runs D)."""
    for path in sorted(glob.glob(os.path.join(BM.SEED_DIR, "*.jsonl"))):
        name = os.path.basename(path)[:-6]
        evs = [json.loads(line) for line in open(path, encoding="utf-8")]
        p = subprocess.Popen([sys.executable, os.path.join(HERE, "supplier_double.py"),
                              "--seed-dir", BM.SEED_DIR, "--seed", name],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        for ev in evs:
            if ev["kind"] == "send":
                p.stdin.write((ev["raw"] + "\n").encode())
                p.stdin.flush()
                time.sleep(0.05)
            elif ev["kind"] == "close-stdin":
                p.stdin.close()
            elif ev["kind"] == "signal-sent":
                time.sleep(0.1)
                p.send_signal(signal.SIGTERM)
        out = p.stdout.read()
        p.wait(timeout=10)
        got = out.decode().splitlines()
        want = [ev["raw"] for ev in evs if ev["kind"] == "recv"]
        rec_exit = [ev for ev in evs if ev["kind"] == "exit"][0]
        ok = got == want and p.returncode == rec_exit["code"] == 0
        result("SEED-" + name, ok, "%d/%d frames byte-identical; exit %s (recorded %s)" % (
            sum(1 for a, b in zip(got, want) if a == b), len(want), p.returncode, rec_exit["code"]))


def seed_cross():
    """SEED-X: seeded from A-bin-freshhome and driven with every other
    transcript's sends; equal to each recording except `emittedAtMs`."""
    diffs = []
    for path in sorted(glob.glob(os.path.join(BM.SEED_DIR, "*.jsonl"))):
        evs = [json.loads(line) for line in open(path, encoding="utf-8")]
        p = subprocess.Popen([sys.executable, os.path.join(HERE, "supplier_double.py"),
                              "--seed-dir", BM.SEED_DIR], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        for ev in evs:
            if ev["kind"] == "send":
                p.stdin.write((ev["raw"] + "\n").encode())
                p.stdin.flush()
                time.sleep(0.03)
        p.stdin.close()
        out = p.stdout.read()
        p.wait(timeout=10)

        def norm(line):
            o = json.loads(line)
            o.pop("emittedAtMs", None)
            return o
        got = [norm(x) for x in out.decode().splitlines()]
        want = [norm(ev["raw"]) for ev in evs if ev["kind"] == "recv"]
        if got != want:
            diffs.append(os.path.basename(path))
    result("SEED-X", not diffs, "8 transcripts equal except emittedAtMs" if not diffs else "differ: %s" % diffs)


def vc16_vc08():
    b = new_boundary()
    ok_start = b.start()
    b.pump(0.2)
    ready_idx = next(i for i, d in enumerate(b.delivered) if d.get("announcement") == "ready")
    note = [d for d in b.delivered if d.get("meta", {}).get("class") == "notification"]
    seed = [json.loads(line) for line in open(os.path.join(BM.SEED_DIR, "A-bin-freshhome.jsonl"))]
    rec_note = [ev["raw"] for ev in seed if ev["kind"] == "recv" and "remoteControl" in ev["raw"]][0]
    held_ok = (ok_start and len(note) == 1 and b.delivered.index(note[0]) == ready_idx + 1
               and note[0]["meta"]["generation"] == b.generation and note[0]["meta"]["position"] == 2)
    result("VC-16", held_ok, "notification received before `initialized` (position 2 of g%d) was held "
           "and delivered right after ready(g%d); not dropped" % (b.generation, b.generation))
    native_ok = note[0]["native"] == rec_note and "generation" not in json.loads(note[0]["native"])
    vi = b.version_identity
    result("VC-08 (part: X-01 side)", native_ok and vi["handshakeConsistency"] == "consistent",
           "delivered frame byte-identical to the recording incl. emittedAtMs; metadata beside; "
           "handshake identity %s, userAgent parse %s" % (sorted(vi["handshakeReportedIdentity"]),
                                                           vi["handshakeConsistency"]))
    finish(b)
    e = new_boundary(scenario="early-request")
    e.start()
    e.pump(0.2)
    p1, p2 = entry(e, "srv-p1"), entry(e, "srv-p2")
    order = [d["meta"]["position"] for d in e.delivered if "meta" in d]
    err = [f for f in app_frames(e) if f.get("id") == "srv-p2"]
    ok_b = (p1["receiptPosition"] == 3 and p1["state"] == "outstanding"
            and p2["receiptPosition"] == 4 and p2["state"] == "errored" and err
            and order[:3] == [2, 3, 4])
    result("VC-16 (b: requests while handshaking)", ok_b, "two server requests sent before "
           "`initialized`: entries created at receipt (R1; positions 3, 4), the unfamiliar one "
           "errored at once (R2), the known one outstanding; all held frames delivered after "
           "ready in received order")
    finish(e)


def vc21():
    b = new_boundary()
    b.start()
    r1 = b.wait_for(b.send("chirality/b6UnknownMethod", {}, {"kind": "receiver", "name": "DEL-01-03"}), 2)
    r2 = b.wait_for(b.send("chirality/b6UnknownMethod2", {}, {"kind": "receiver", "name": "DEL-01-03"}), 2)
    log = double_log(b)
    mutated = [ev for ev in log if ev["dir"] == "emit" and ev.get("note") == "seed:unknown_method"]
    ok = (r1["outcome"] == r2["outcome"] == "response-observed-error" and r1["error"]["code"] == -32600
          and b.state == "ready" and all(ev["standing"] == "mutated" for ev in mutated))
    result("VC-21", ok, "unknown client method -> response-observed(error) -32600 (recorded message, "
           "name substituted: mutated), not unknown; connection continued (second request answered)")
    finish(b)


def vc03():
    b = new_boundary(scenario="unfamiliar")
    b.start()
    b.pump(0.4)
    e = entry(b, "srv-u1")
    sent = [f for f in app_frames(b) if f.get("id") == "srv-u1"]
    ok = (e["classification"] == "unfamiliar" and e["state"] == "errored" and len(sent) == 1
          and "error" in sent[0] and "result" not in sent[0])
    result("VC-03", ok, "entry created (R1), classified unfamiliar, explicit error written (R2, code %s "
           "TEST VALUE); no affirmative answer" % sent[0]["error"]["code"] if sent else "no reply")
    finish(b)


def vc20():
    a = new_boundary(scenario="capabilities")
    a.start()
    a.pump(0.4)
    ea, eb = entry(a, "srv-c1"), entry(a, "srv-c2")
    ok_a = ea["classification"] == eb["classification"] == "unfamiliar" and ea["state"] == eb["state"] == "errored"
    finish(a)
    b = new_boundary(scenario="capabilities", declared={"experimentalApi": True, "requestAttestation": False})
    b.start()
    b.pump(0.4)
    eb1, eb2 = entry(b, "srv-c1"), entry(b, "srv-c2")
    r = b.answer("srv-c1", {"currentTimeAt": 1790000000}, {"class": "app-rule", "ruleName": "clock"})
    ok_b = (eb1["classification"] == "known-answerable" and eb1["originClass"] == "named-service"
            and r == "accepted-for-write" and eb1["state"] == "answered"
            and eb2["classification"] == "unfamiliar")
    finish(b)
    c = new_boundary(scenario="capabilities", declared={"experimentalApi": False, "requestAttestation": True})
    c.start()
    c.pump(0.4)
    ec1, ec2 = entry(c, "srv-c1"), entry(c, "srv-c2")
    ok_c = (ec1["classification"] == "unfamiliar" and ec2["classification"] == "known-app-unsupported"
            and ec2["state"] == "errored" and ec2["settlement"]["origin"]["ruleName"] == "unsupported-kind")
    result("VC-20", ok_a and ok_b and ok_c, "opt-in false: currentTime/read and attestation/generate "
           "unfamiliar -> explicit errors; experimentalApi true: currentTime/read familiar, answered by "
           "app-rule:clock, attestation/generate still unfamiliar; requestAttestation true: "
           "attestation/generate familiar, known-app-unsupported -> explicit error by named rule")
    finish(c)


def vc22():
    b = new_boundary(scenario="origin", declared={"experimentalApi": True, "requestAttestation": False})
    b.start()
    b.pump(0.4)
    rule = {"class": "app-rule", "ruleName": "b6-test-rule"}
    r1 = b.answer("srv-o1", {"answers": {"q-ex-1": {"answers": ["invented"]}}}, rule)
    r2 = b.answer("srv-o2", {"decision": "accept"}, rule)
    r3 = b.answer("srv-o3", {"action": "decline"}, rule)
    r4 = b.answer("srv-o4", {"currentTimeAt": 1790000000}, rule)
    ok = (r1 == r2 == "refused(origin-not-permitted)" and r3 == r4 == "accepted-for-write"
          and entry(b, "srv-o3")["state"] == "declined" and entry(b, "srv-o4")["state"] == "answered"
          and entry(b, "srv-o1")["state"] == entry(b, "srv-o2")["state"] == "outstanding")
    result("VC-22", ok, "app-rule content answer to requestUserInput and affirmative to fileChange "
           "refused origin-not-permitted (entries stay outstanding); app-rule decline of elicitation "
           "recorded declined app-rule:b6-test-rule; currentTime/read answered app-rule; no act record")
    finish(b)


def vc23():
    b = new_boundary(scenario="elicitation")
    b.start()
    b.pump(0.4)
    r = b.answer("srv-e1", {"action": "accept", "content": {"answer": "yes, accepted"}},
                 {"class": "person-via-interaction", "actorRef": "person:ex-1 (identity not verified)"})
    e = entry(b, "srv-e1")
    kinds = {rec["recordKind"] for rec in b.records()}
    ok = (r == "accepted-for-write" and e["state"] == "answered"
          and e["settlement"]["origin"]["class"] == "person-via-interaction"
          and kinds <= {"lifecycle-event", "client-request", "server-request-entry"})
    result("VC-23", ok, "person's 'yes, accepted' settles the elicitation (person-via-interaction) and "
           "is written to the supplier as conversation input; the boundary emits no human-act record "
           "and no checkpoint satisfaction (record kinds: %s)" % sorted(kinds))
    finish(b)


def vc14():
    b = new_boundary(scenario="settlement")
    b.start()
    b.pump(0.5)
    person = {"class": "person-via-interaction", "actorRef": "person:ex-1 (identity not verified)"}
    rule = {"class": "app-rule", "ruleName": "b6-test-rule"}
    steps = [
        ("invalid form", b.answer("srv-s1", {"decision": "approve"}, person), "refused(invalid-answer)"),
        ("app-rule affirmative A14", b.answer("srv-s2", {"decision": "accept"}, rule), "refused(origin-not-permitted)"),
        ("person accept", b.answer("srv-s1", {"decision": "accept"}, person), "accepted-for-write"),
        ("second answer", b.answer("srv-s1", {"decision": "decline"}, person), "refused(already-settled)"),
        ("app-rule decline", b.answer("srv-s2", {"decision": "decline"}, rule), "accepted-for-write"),
        ("resolved before answer", b.answer("srv-s3", {"decision": "accept"}, person), "refused(already-resolved)"),
        ("unknown identity", b.answer("srv-zz", {"decision": "accept"}, person), "refused(no-such-request)"),
    ]
    b.pump(0.3)
    s1 = entry(b, "srv-s1")
    ok = (all(got == want for _, got, want in steps) and s1["state"] == "answered"
          and s1["acknowledgmentObservation"]["status"] == "observed"
          and entry(b, "srv-s2")["state"] == "declined"
          and entry(b, "srv-s3")["state"] == "resolved-by-supplier")
    detail = "; ".join("%s -> %s" % (n, got) for n, got, _ in steps)
    finish(b)
    w = new_boundary(scenario="writefail")
    w.start()
    w.pump(0.5)
    rw = w.answer("srv-w1", {"decision": "accept"}, person)
    ew1 = entry(w, "srv-w1")
    g_old = w.generation
    w.pump(1.5)
    closed = w.answer("srv-w1", {"decision": "decline"}, person, generation=g_old)
    ew2 = w.register[(g_old, json.dumps("srv-w2"))]
    ok_w = (rw == "accepted-for-write" and ew1["state"] == "settle-write-failed"
            and closed == "refused(generation-closed)" and ew2["state"] == "ended-unanswered")
    result("VC-14 (part: X-12 with double)", ok and ok_w, detail + "; write to a closed input -> "
           "settle-write-failed (outcome unknown); after exit: answer -> refused(generation-closed); "
           "unanswered entry -> ended-unanswered(process-exit)")
    if w.state == "restart-waiting":
        w.pump(0.5)
    finish(w)


def vc04():
    b = new_boundary(scenario="malformed")
    b.start()
    b.pump(0.8)
    mal = [d["meta"] for d in b.delivered if d.get("meta", {}).get("class") == "malformed"]
    notes = [d for d in b.delivered if d.get("meta", {}).get("class") == "notification"]
    ok = ([m["reason"] for m in mal] == ["not-json", "not-an-object", "unclassifiable", "oversize"]
          and all("generation" in m and "position" in m for m in mal)
          and b.malformed == 4 and len(notes) == 3 and b.state == "ready")
    result("VC-04", ok, "4 malformed frames counted and surfaced with generation and position "
           "(not-json, not-an-object, unclassifiable, oversize > %d B TEST VALUE); valid frames "
           "without the version member accepted; boundary stayed ready" % BM.FRAME_LIMIT)
    finish(b)


def vc06():
    b = new_boundary(scenario="exit-on-initialize")
    b.start()
    b.pump(1.0)
    halted = b.state == "halted-after-repeated-failure"
    gens = b.generation
    fails = [e["failure"] for e in b.events if e["event"] == "handshake-failed"]
    b.scenario = "default"
    b.start(actor="person:ex-1", explicit=True)
    ok = halted and fails == ["child-ended"] * 3 and gens == 3 and b.state == "ready"
    result("VC-06", ok, "handshake failed 3 times (child ended, exit code 0) -> restart-waiting twice, "
           "then halted-after-repeated-failure (bound %d in %ds TEST VALUE); no automatic start; "
           "explicit person restart -> ready in g%d; each attempt re-verified" % (
               BM.MAX_FAILURES, BM.FAILURE_WINDOW_S, b.generation))
    finish(b)
    x = new_boundary(scenario="exit-after-ready")
    x.start()
    x.pump(0.2)
    rec = x.send("thread/list", {}, {"kind": "receiver", "name": "DEL-01-02"})
    g1 = x.generation
    x.scenario = "default"  # the restarted double runs the recorded handshake only
    x.pump(1.2)
    ev = [e for e in x.events if e["event"] == "child-ended-without-stop-record"]
    ok_x = (ev and ev[0]["exitFacts"]["exitCode"] == 0 and rec["outcome"] == "unknown-no-response"
            and x.register[(g1, json.dumps("srv-x1"))]["state"] == "ended-unanswered"
            and x.generation == 2 and x.state == "ready")
    result("VC-06 (b: unexpected exit)", ok_x, "exit code 0 with no stop record -> exited-unexpectedly "
           "(S-F-07); pending client request -> unknown-no-response; outstanding entry -> "
           "ended-unanswered(process-exit); automatic restart -> ready in g2")
    finish(x)


def vc24():
    b = new_boundary(scenario="mcp")
    b.start()
    b.pump(0.3)
    st = b.wait_for(b.send("mcpServerStatus/list", {}, {"kind": "receiver", "name": "DEL-03-03"}), 2)
    call = b.wait_for(b.send("mcpServer/tool/call", {"server": "example-host", "threadId": "thr-ex-1",
                                                     "tool": "example_lookup", "arguments": {"key": "EX-1"}},
                             {"kind": "receiver", "name": "DEL-03-03"}), 2)
    items = [json.loads(d["native"]) for d in b.delivered
             if d.get("meta", {}).get("class") == "notification" and "item/" in d["native"]]
    status = st.get("_result", {}).get("data", [{}])[0].get("runtimeStatus")
    kinds = {r["recordKind"] for r in b.records()}
    ok = (status == "disabled" and call["outcome"] == "response-observed-result"
          and call["initiator"] == {"kind": "receiver", "name": "DEL-03-03"}
          and [i["params"]["item"]["status"] for i in items] == ["inProgress", "completed"]
          and not b.register and kinds <= {"lifecycle-event", "client-request", "server-request-entry"})
    result("VC-24", ok, "status list delivered natively (runtimeStatus 'disabled' passed through as "
           "App-side configuration; no act record); agent's mcpToolCall items delivered natively, "
           "never answered or altered, no register entry; App-initiated mcpServer/tool/call recorded "
           "with initiator receiver:DEL-03-03, not as the agent's call")
    finish(b)


def vc25():
    b = new_boundary(scenario="hold")
    b.start()
    b.pump(0.4)
    call = b.wait_for(b.send("mcpServer/tool/call", {"server": "example-host", "threadId": "thr-ex-1",
                                                     "tool": "example_lookup"},
                             {"kind": "receiver", "name": "DEL-03-03"}), 2)
    sent = [f.get("method") for f in app_frames(b)]
    e = entry(b, "srv-h1")
    ok1 = (call["outcome"] == "response-observed-result" and "turn/interrupt" not in sent
           and e["state"] == "outstanding" and "settlement" not in e
           and any('"item-ex-8"' in d["native"] and "item/completed" in d["native"]
                   for d in b.delivered if "native" in d))
    finish(b)
    g = new_boundary(scenario="hold", phase="governance")
    g.holding_threads.add("thr-ex-1")  # DEL-02-03 reports the run holding (governance phase)
    g.start()
    g.pump(0.4)
    d = g.answer("srv-h1", {"decision": "decline"}, {"class": "app-rule", "ruleName": "hold-decline"})
    gcall = g.send("mcpServer/tool/call", {"server": "example-host", "threadId": "thr-ex-1",
                                           "tool": "example_lookup"}, {"kind": "receiver", "name": "DEL-03-03"})
    pturn = g.wait_for(g.send("turn/start", {"threadId": "thr-ex-1", "input": [
        {"type": "text", "text": "invented example message"}]},
        {"kind": "person-directed", "actorRef": "person:ex-1"}), 2)
    gsent = [f.get("method") for f in app_frames(g)]
    ok2 = (d == "accepted-for-write" and entry(g, "srv-h1")["state"] == "declined"
           and gcall["outcome"] == "refused-not-sent" and gcall["refusalReason"] == "run-holding"
           and "mcpServer/tool/call" not in gsent and "turn/interrupt" not in gsent
           and pturn["outcome"] == "response-observed-result")
    result("VC-25", ok1 and ok2, "Phase 1: no run holding; no named-rule decline, no run-holding "
           "refusal, no turn/interrupt; App-initiated call handled by §6.8 rules; tool-permission entry "
           "stays outstanding for the person; auto-reviewed tool delivered natively. Governance phase: "
           "decline recorded app-rule:hold-decline; App-initiated call refused run-holding (not sent); "
           "person-directed turn carried; no turn/interrupt; no hold claim")
    finish(g)


def vc26():
    b = new_boundary(scenario="destination")
    b.start()
    b.wait_for(b.send("thread/start", {"modelProvider": "example-local", "model": "example-model-a",
                                       "developerInstructions": "Invented example guidance."},
                      {"kind": "person-directed", "actorRef": "person:ex-1"}), 2)
    for _ in range(2):
        b.wait_for(b.send("turn/start", {"threadId": "thr-ex-1", "model": "example-model-a",
                                         "input": [{"type": "text", "text": "invented example"}]},
                          {"kind": "person-directed", "actorRef": "person:ex-1"}), 2)
    b.pump(0.3)
    f = b.destination_facts()
    t1, t2 = f["turns"]["turn-ex-1"], f["turns"]["turn-ex-2"]
    ts = [r for r in b.client.values() if r["method"] == "thread/start"][0]
    ok = (t1["requested"]["model"] == "example-model-a" and t1["effective"]["model"] == "example-model-b"
          and t2["requested"]["model"] == "example-model-a" and t2["effective"] == "unknown"
          and f["thread"]["effective"]["model"] == "example-model-a"
          and len(ts.get("carriedGuidance", [])) == 1)
    result("VC-26 (part: constructed re-route)", ok, "requested and effective kept apart per turn; "
           "re-route recorded on turn-ex-1 (effective example-model-b); turn-ex-2 has no report -> "
           "unknown, not filled from turn-ex-1 or the thread-level report; thread-level effective kept "
           "at thread scope; carried guidance identity recorded on thread/start; no gate")
    finish(b)


def vc10():
    b = new_boundary(distribution={"label": "codex-cli 0.158.0", "content": "double-tree-2",
                                   "outputPin": "0.158.0"})
    ok_start = b.start()
    ev = b.events[-1]
    ok = (not ok_start and b.state == "refused" and b.child is None
          and ev["verificationResult"] == {"result": "mismatch", "element": "distribution content identity"})
    result("VC-10 (constructed identity)", ok, "same label, different content identity -> refused "
           "mismatch(distribution content identity); no child started")
    b.distribution = dict(b.expected)
    b.start(actor="person:ex-1")
    finish(b)


def stops():
    for means in ("close-input", "termination-signal"):
        b = new_boundary()
        b.start()
        b.pump(0.2)
        b.stop(means=means)
        ev = b.events[-1]
        ok = (b.state == "stopped" and ev["event"] == "tree-ended" and ev["exitFacts"]["exitCode"] == 0
              and ev["descendants"] == {"checked": True, "surviving": 0,
                                        "handling": "recorded; none to handle"}
              and b.events[-2]["stopRecord"]["endingMeans"] == means)
        result("STOP-%s" % means, ok, "stop record written first; exit code 0 (recorded behaviour) not "
               "used to classify; deliberate from the stop record; descendants checked (0)")
        b.start(actor="person:ex-1")
        b.stop(outstanding="declined-by-app-rule-on-stop")
        ALL_RECORDS.extend(b.records())
        LT_USED.update(b.transitions_used)
        RT_USED.update(b.register_transitions_used)


def more_transitions():
    """Rows not reached by the VC cases: stop from restart-waiting, halted and
    verifying-before-spawn; spawn failure; stop while handshaking."""
    b = new_boundary(scenario="exit-on-initialize")
    b.start()
    b.stop(actor="person:ex-1")            # LT-21 from restart-waiting
    h = new_boundary(scenario="exit-on-initialize")
    h.start()
    h.pump(1.0)
    h.stop(actor="person:ex-1")            # LT-22 from halted
    u = new_boundary(scenario="exit-after-ready")
    u.start()
    u.pump(3.5)                            # three unexpected exits in the window -> LT-14
    ok_u = u.state == "halted-after-repeated-failure" and u.events[-1]["transitionId"] == "LT-14"
    ALL_RECORDS.extend(u.records())
    LT_USED.update(u.transitions_used)
    RT_USED.update(u.register_transitions_used)
    inj = []
    for st in ("verifying", "spawning", "handshaking"):
        k = new_boundary()
        k.inject_stop_in = st
        k.start()
        inj.append((st, k.state, [e["transitionId"] for e in k.events][-2:]))
        ALL_RECORDS.extend(k.records())
        LT_USED.update(k.transitions_used)
    s = new_boundary(spawn_argv=["/nonexistent/b6-no-such-supplier"])
    s.start()                              # LT-07 spawn-failed
    s.pump(0.5)                            # LT-15 -> LT-04 -> spawn-failed again ... LT-08
    ok = ok_u and (inj == [("verifying", "stopped", ["LT-01", "LT-20"]),
                  ("spawning", "stopped", ["LT-19", "LT-23"]),
                  ("handshaking", "stopped", ["LT-18", "LT-23"])]
          and b.state == "stopped" and h.state == "stopped"
          and s.state == "halted-after-repeated-failure"
          and [e["transitionId"] for e in s.events if e["event"] == "spawn-failed"] == ["LT-07", "LT-07", "LT-08"])
    result("LT-extra", ok, "stop injected while verifying (LT-20), spawning (LT-19, LT-23) and "
           "handshaking (LT-18, LT-23) -> stopped; stop from restart-waiting and from halted -> "
           "stopped (no child); spawn failure counted toward the bound: LT-07, LT-07, LT-08; three "
           "unexpected exits in the window -> halted (LT-14)")
    for x in (b, h, s):
        ALL_RECORDS.extend(x.records())
        LT_USED.update(x.transitions_used)


def coverage():
    lt = sorted(set(BM.TRANSITIONS) - LT_USED)
    rt = sorted(set(BM.REGISTER_TRANSITIONS) - RT_USED)
    result("TT-coverage", not lt and not rt,
           "lifecycle rows exercised %d/%d (not exercised: %s); register rows %d/%d%s" % (
               len(LT_USED), len(BM.TRANSITIONS), ", ".join(lt) or "none",
               len(RT_USED), len(BM.REGISTER_TRANSITIONS), "" if not rt else " missing " + ", ".join(rt)))


def schema_checks():
    bad = []
    for rec in ALL_RECORDS:
        errs = V.errors(rec, SCHEMAS[KIND_TO_SCHEMA[rec["recordKind"]]])
        if errs:
            bad.append((rec["recordKind"], errs[:2]))
    result("SCHEMA-records", not bad, "%d records emitted by the model validated against the 3 PROPOSED "
           "schemas%s" % (len(ALL_RECORDS), "" if not bad else "; failures: %s" % bad[:3]))
    fx = os.path.join(HERE, "fixtures")
    lines = []
    ok = True
    for k in SCHEMAS:
        for kind in ("valid", "invalid"):
            inst = json.load(open(os.path.join(fx, "%s.%s.json" % (k, kind)), encoding="utf-8"))
            errs = V.errors(inst["instance"], SCHEMAS[k])
            good = (not errs) if kind == "valid" else bool(errs)
            ok &= good
            lines.append("%s.%s: %s" % (k, kind, "valid" if not errs else "invalid (%s)" % errs[0]))
    result("SCHEMA-fixtures", ok, " | ".join(lines))


def double_conformance():
    n, bad = 0, []
    for d in LOG_DIRS:
        for path in glob.glob(os.path.join(d, "double-g*.jsonl")):
            for line in open(path, encoding="utf-8"):
                ev = json.loads(line)
                if ev.get("dir") != "emit" or ev["standing"] == "recorded":
                    continue
                note = ev.get("note") or ""
                if "by design" in note or "no scripted response" in ev["raw"]:
                    continue
                f = json.loads(ev["raw"])
                if "method" in f and "id" in f:
                    errs = V.validate_against(f, ROOT, "#/definitions/ServerRequest")
                elif "method" in f:
                    errs = V.validate_against(f, ROOT, "#/definitions/ServerNotification")
                elif "error" in f:
                    errs = [] if isinstance(f["error"].get("code"), int) else ["error.code"]
                else:
                    errs = V.validate_against(f["result"], ROOT, RESP[ev["responds_to"]])
                n += 1
                if errs:
                    bad.append((f.get("method") or ev.get("responds_to"), errs[:1]))
    result("DOUBLE-conformance", not bad, "%d constructed or mutated frames emitted by the double "
           "valid against the committed 0.158.0 bundle%s" % (n, "" if not bad else "; %s" % bad[:3]))


def hosting_tables():
    """VC-27 (tables): the §4.7 and §6.2.1 tables in HOSTING equal the model's."""
    text = open(HOSTING, encoding="utf-8").read()

    def rows(prefix):
        out = {}
        for line in text.splitlines():
            if line.startswith("| %s-" % prefix):
                c = [x.strip().strip("`") for x in line.strip("|").split("|")]
                out[c[0]] = c
        return out
    lt = rows("LT")
    lt_model = {k: (v[0], v[1], v[2]) for k, v in BM.TRANSITIONS.items()}
    lt_doc = {k: (c[1], c[2], c[4]) for k, c in lt.items()}
    rt = rows("RT")
    rt_model = {k: (v[0] or "—", v[1], v[2]) for k, v in BM.REGISTER_TRANSITIONS.items()}
    rt_doc = {k: (c[1], c[2], c[4]) for k, c in rt.items()}
    ok = lt_doc == lt_model and rt_doc == rt_model
    diff = [k for k in lt_model if lt_doc.get(k) != lt_model[k]] + \
        [k for k in rt_model if rt_doc.get(k) != rt_model[k]]
    result("VC-27 (tables in HOSTING)", ok, "HOSTING §4.7 (%d rows) and §6.2.1 (%d rows) equal the model's "
           "tables%s" % (len(lt_doc), len(rt_doc), "" if ok else "; differ: %s" % diff))


def capability_account():
    """VC-30: every generated surface in exactly one §8.4 group, marks right."""
    import re
    text = open(HOSTING, encoding="utf-8").read()
    sec = text.split("### 8.4 ", 1)[1].split("\n## 9. ", 1)[0]
    inv = open(os.path.join(DESIGN, "generated", "0.158.0", "_spike", "inventory.txt")).read()

    def inv_list(name, which):
        m = re.search(r"## %s:.*?\nstable: (.*?)\n(?:experimental-only: (.*?)\n)?" % name, inv, re.S)
        return (m.group(1) if which == "stable" else (m.group(2) or "")).split(", ")
    v2 = json.load(open(BM.BUNDLE.replace("schemas.json", "v2.schemas.json"), encoding="utf-8"))
    items = [b["properties"]["type"]["enum"][0] for b in v2["definitions"]["ThreadItem"]["oneOf"]]
    seed = [json.loads(x) for x in open(os.path.join(BM.SEED_DIR, "A-bin-freshhome.jsonl"))]
    msg = [json.loads(e["raw"])["error"]["message"] for e in seed
           if e["kind"] == "recv" and "unknown variant" in e["raw"]][0]
    accepted = re.findall(r"`([^`]+)`", msg)[1:]
    root = ROOT["definitions"]
    notes_js = [b["properties"]["method"]["enum"][0] for b in root["ServerNotification"]["oneOf"]]
    ts_c = ["getAuthStatus", "getConversationSummary", "gitDiffToRemote"]
    ts_n = ["rawResponse/completed", "rawResponseItem/completed"]
    universe = {"i": items, "s": [b["properties"]["method"]["enum"][0] for b in root["ServerRequest"]["oneOf"]],
                "c": accepted, "n": notes_js + ts_n}
    exp = {"c": set(inv_list("ClientRequest", "exp")), "s": set(inv_list("ServerRequest", "exp"))}
    obs = {"initialize", "remoteControl/status/changed"}
    seen = {k: [] for k in universe}
    bad = []
    for line in sec.splitlines():
        if not line.startswith("| **HCG-"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        for col, key in ((1, "i"), (2, "s"), (3, "c"), (4, "n")):
            for name, marks in re.findall(r"`([^`]+)`(?: \(([^)]*)\))?", cells[col]):
                seen[key].append(name)
                m = set(x.strip() for x in marks.split(",")) if marks else set()
                want = set()
                if key in exp and name in exp[key]:
                    want.add("exp")
                if (key == "c" and name in ts_c) or (key == "n" and name in ts_n):
                    want.add("TS")
                if name in obs:
                    want.add("obs")
                if m != want:
                    bad.append((name, sorted(m), sorted(want)))
    counts = {}
    for k in universe:
        dup = sorted({x for x in seen[k] if seen[k].count(x) > 1})
        missing = sorted(set(universe[k]) - set(seen[k]))
        extra = sorted(set(seen[k]) - set(universe[k]))
        counts[k] = len(set(seen[k]))
        if dup or missing or extra:
            bad.append((k, "dup", dup, "missing", missing, "extra", extra))
    ok = not bad and counts == {"i": 19, "s": 11, "c": 170, "n": 85} and \
        set(accepted) - set(c for b in root["ClientRequest"]["oneOf"]
                            for c in b["properties"]["method"]["enum"]) == set(ts_c)
    result("VC-30 (capability account)", ok, "§8.4 places %(i)d item kinds, %(s)d server-request kinds, "
           "%(c)d client methods and %(n)d notifications each in exactly one group; variant and (obs) "
           "marks match the bundles, inventory, TS-only list and recorded accepted-method list" % counts
           + ("" if not bad else "; problems: %s" % bad[:4]))


def obs1_doubles():
    """The OBS-1 test tools answer as their briefs say (no Codex involved)."""
    import socket
    d = tempfile.mkdtemp(prefix="b6-obs1-", dir=os.environ.get("TMPDIR"))
    LOG_DIRS.append(d)
    log = os.path.join(d, "mcp.jsonl")
    p = subprocess.Popen([sys.executable, os.path.join(HERE, "obs1_mcp_double.py"), "--log", log],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    msgs = [{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
                "protocolVersion": "2025-06-18", "capabilities": {},
                "clientInfo": {"name": "b6-check", "version": "0"}}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {
                "name": "example_lookup", "arguments": {"key": "EX-1"}, "_meta": {"x": 1}}},
            {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {
                "name": "example_lookup", "arguments": {"key": "EX-ERR"}}},
            {"jsonrpc": "2.0", "id": 5, "method": "resources/list"}]
    p.stdin.write(("\n".join(json.dumps(m) for m in msgs) + "\n").encode())
    p.stdin.close()
    out = [json.loads(x) for x in p.stdout.read().decode().splitlines()]
    p.wait(timeout=5)
    by = {o["id"]: o for o in out}
    sc = by[3]["result"]["structuredContent"]
    ok_m = (by[1]["result"]["protocolVersion"] == "2025-06-18"
            and by[2]["result"]["tools"][0]["name"] == "example_lookup"
            and by[3]["result"]["isError"] is False and sc["outcome"] == "queued" and sc["metaReceived"]
            and by[4]["result"]["isError"] is True and by[5]["error"]["code"] == -32601
            and len(out) == 5 and sum(1 for _ in open(log)) >= 11)
    sock_path = os.path.join(d, "probe.sock")
    srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    srv.bind(sock_path)
    srv.listen(1)
    r1 = subprocess.run([sys.executable, os.path.join(HERE, "obs1_cli_tool.py"), "--key", "EX-1",
                         "--probe-socket", sock_path], capture_output=True, timeout=5)
    r2 = subprocess.run([sys.executable, os.path.join(HERE, "obs1_cli_tool.py"), "--key", "EX-ERR"],
                        capture_output=True, timeout=5)
    srv.close()
    j1, j2 = json.loads(r1.stdout), json.loads(r2.stdout)
    ok_c = (r1.returncode == 0 and j1["outcome"] == "queued" and j1["localSocket"] == "connected"
            and r2.returncode == 3 and j2["outcome"] == "not-found")
    result("OBS1-test-doubles", ok_m and ok_c, "MCP test double: initialize (version echoed), tools/list, "
           "tools/call EX-1 (structured result, _meta seen) and EX-ERR (isError), -32601 for other "
           "methods, receipt log written; CLI tool: JSON result exit 0, EX-ERR exit 3, local-socket "
           "probe connected (outside any sandbox)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keep-logs", action="store_true")
    args = ap.parse_args()
    started = time.strftime("%Y-%m-%d %H:%M:%S %Z")
    for fn in (seed_fidelity, seed_cross, vc16_vc08, vc21, vc03, vc20, vc22, vc23, vc14, vc04,
               vc06, vc24, vc25, vc26, vc10, stops, more_transitions, hosting_tables,
               capability_account, obs1_doubles):
        try:
            fn()
        except Exception as exc:  # a crash is a failure of that case, reported
            result(fn.__name__, False, "exception: %r" % exc)
    coverage()
    schema_checks()
    double_conformance()
    print("B6 supplier-double run — started %s — python %s" % (started, sys.version.split()[0]))
    width = max(len(c) for c, _, _ in RESULTS)
    for case, res, detail in RESULTS:
        print("%-*s  %-12s  %s" % (width, case, res, detail))
    fails = [c for c, r, _ in RESULTS if r != "pass (model)"]
    print("TOTAL %d, pass (model) %d, FAIL %d" % (len(RESULTS), len(RESULTS) - len(fails), len(fails)))
    if args.keep_logs:
        print("logs: " + " ".join(LOG_DIRS))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
