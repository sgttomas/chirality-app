"""DEL-06-02 prototype check (FLEET_VIEWS.md FV-v0.1 §7): VER-001, VER-002, VER-005, VER-006 over DEL-06-01's
fixture FX-FL1 and the early-path fixture FX-DP1. Prototype only; invented subject matter; no act was performed.
Usage: python3 -B run_views.py [scratch]. Exit 0 only if every expectation held. Writes only into scratch.
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fleet_views import build  # noqa: E402

EXECUTION = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", ".."))
FX_FL1 = os.path.normpath(os.path.join(HERE, "..", "..", "..", "DEL-06-01_Bounded delegation and current work-graph records",
                                       "Design", "prototype", "fixtures", "FX-FL1"))
RS_LOG = os.path.join(EXECUTION, "_Coordination", "AgentRuns", "APP-V4-DESIGN-PASS-4-20261003", "E", "fixtures", "FX-DP1",
                      "records", "coordination.rs.jsonl")
RESULTS = []


def check(cond, label):
    RESULTS.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + label)


def tree(root):
    out = {}
    for d, _, fs in os.walk(root):
        for f in fs:
            with open(os.path.join(d, f), "rb") as fh:
                out[os.path.relpath(os.path.join(d, f), root)] = hashlib.sha256(fh.read()).hexdigest()
    return out


def main():
    scratch = sys.argv[1] if len(sys.argv) > 1 else tempfile.mkdtemp(prefix="views-")
    os.makedirs(scratch, exist_ok=True)
    before = tree(FX_FL1)
    v = build(FX_FL1, RS_LOG)
    with open(os.path.join(scratch, "views.FX-FL1.json"), "w", encoding="utf-8") as fh:
        json.dump(v, fh, ensure_ascii=False, indent=2)
    Q = {r["item"]: r for r in v["queue"]}
    W = {r["item"]: r for r in v["waiting"]}

    print("== VER-001 return-review queue ==")
    check(set(Q) == {"W8"} and Q["W8"]["state"] == "awaiting review" and Q["W8"]["returnedBy"] == "thr-c8"
          and "thread:fx-u1-manager" in Q["W8"]["examines"],
          "VER-001 W8's return is queued awaiting review, with who returned it and who examines it (the brief's preparer)")
    check("W7" not in Q and any("no return recorded" in c for c in W["W7"]["causes"]) and W["W7"]["category"] == "unknown",
          "VER-001 W7: Codex reports the child completed and an agent's message claims it done; it is not queued and not promoted")
    check("W1" not in Q and W["W1"]["category"] == "done", "VER-001 W1 left the queue only on its integration record")

    nb = os.path.join(scratch, "FX-FL1-no-brief")
    if os.path.exists(nb):
        shutil.rmtree(nb)
    shutil.copytree(FX_FL1, nb)
    with open(os.path.join(nb, "coordination.fleet.jsonl"), "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"format": "chirality.fleet.record", "formatVersion": "0.1", "recordId": "fl:log:0099",
                             "kind": "return_recorded", "undertaking": "FX-U1",
                             "recorder": {"kind": "agent", "identity": "thread:fx-u1-manager", "role": "WORKING_ITEMS"},
                             "writtenAt": "r99", "body": {"workItem": "W9",
                             "returnedBy": {"kind": "agent", "identity": "thread:fx-u1-manager", "role": "WORKING_ITEMS"},
                             "returned": [{"kind": "file", "ref": "REPORT.md"}],
                             "evidence": [{"kind": "file", "ref": "REPORT.md"}]}}) + "\n")
    nq = {r["item"]: r for r in build(nb, RS_LOG)["queue"]}
    check(nq.get("W9", {}).get("examines") == "examiner not established",
          "VER-001 FV-2a a return on an item with no brief shows 'examiner not established'; the graph owner is not used as the examiner")

    print("\n== VER-002 waiting by cause ==")
    check(W["W3"]["category"] == "waiting" and any("waits for W2" in c for c in W["W3"]["causes"])
          and any("related conversation" in c for c in W["W3"]["causes"]) and any("basis changed" in c for c in W["W3"]["causes"]),
          "VER-002 W3 waits for W2, with its basis change and a related conversation shown (not a dispatch)")
    check(W["W5"]["category"] == "waiting" and any("person's decision" in c and "rec:app:coord:0002" in c for c in W["W5"]["causes"]),
          "VER-002 W5 waits for the person's decision on PKG-2")
    check(W["W4"]["category"] == "ready (qualified)" and any("decision recorded" in c and "A16, ALT-2" in c for c in W["W4"]["causes"]),
          "VER-002 W4 is ready: its decision is recorded (A16 on PKG-1, ALT-2 shown, not interpreted)")
    check(W["W2"]["category"] == "unknown" and any("observation ended" in c and "outcome unknown" in c for c in W["W2"]["causes"]),
          "VER-002 W2: observation ended at quit; outcome unknown, never 'in progress' or 'done'")
    check(W["W9"]["category"] == "ready (qualified)" and W["W6"]["category"] == "done",
          "VER-002 W9 ready once W6's external result and its input exist; W6 done by its external result")
    check(W["W9"]["readinessQualified"] and any("thr-cx" in c and "may be unrecorded" in c for c in W["W9"]["causes"])
          and W["W4"]["readinessQualified"],
          "VER-002 FV-4a (E2-R3) ready rows say a child without a brief reference (thr-cx) exists; a dispatch may be unrecorded")
    check(v["queueComplete"], "VER-002 with every log line read and no orphan, the queue is complete")
    def renders_bare_ready(view):
        """E2-R4: a row 'renders as bare ready' if its label is 'ready' or its label and first cause carry no qualifier."""
        bad = []
        for r in view["waiting"]:
            if r["readinessQualified"] and (r["category"] == "ready" or "may be unrecorded" not in r["causes"][0]):
                bad.append(r["item"])
        return bad
    check(not renders_bare_ready(v) and all(r["readinessQualified"] == (r["category"] == "ready (qualified)") for r in v["waiting"]),
          "VER-002 FV-4a (E2-R4) no qualified row renders as bare 'ready': the label says 'ready (qualified)' and the qualifier is the first cause")
    check(all(r["causes"] for r in v["waiting"]), "VER-002 every selected item shows a cause or state; none is blank")

    print("\n== VER-005 cross-session reconstruction ==")
    code = ("import sys, json; sys.path.insert(0, %r); from fleet_views import build; "
            "print(json.dumps(build(%r, %r), ensure_ascii=False, sort_keys=True))") % (HERE, FX_FL1, RS_LOG)
    other = subprocess.run([sys.executable, "-B", "-c", code], capture_output=True, text=True, check=True).stdout
    check(json.loads(other) == json.loads(json.dumps(v)), "VER-005 a separate process rebuilds identical views from the same files")
    check(tree(FX_FL1) == before, "VER-005 input hashes are unchanged by both rebuilds (FV-9)")

    print("\n== VER-006 PEC absent; limited inputs ==")
    no_rs = build(FX_FL1, None)
    W2 = {r["item"]: r for r in no_rs["waiting"]}
    check(W2["W4"]["category"] == "unknown" and W2["W5"]["category"] == "unknown"
          and any("cause not established" in c for c in W2["W4"]["causes"]),
          "VER-006 without the RS records, decision waits are 'cause not established', never ready")
    lim = os.path.join(scratch, "FX-FL1-limited")
    if os.path.exists(lim):
        shutil.rmtree(lim)
    shutil.copytree(FX_FL1, lim)
    with open(os.path.join(lim, "coordination.fleet.jsonl"), "a", encoding="utf-8") as fh:
        fh.write('{"format": "chirality.fleet.record", "kind": "return_rec')
    lv = build(lim, RS_LOG)
    check(any("partial" in l for l in lv["limits"]) and {r["item"] for r in lv["queue"]} == {"W8"},
          "VER-006 a torn log line is listed as a limit; it adds no return and removes none")
    os.remove(os.path.join(lim, "coordination.fleet.jsonl"))
    gone = build(lim, RS_LOG)
    check(gone["queue"] == [] and gone["waiting"] == [] and gone["notes"] == ["no current graph selected"],
          "VER-006 with the log missing there is no current graph: the views say so and show no empty-work conclusion")
    check(not any("PEC" in json.dumps(x) for x in (v["queue"], v["waiting"])), "VER-006 no PEC input exists in the views")
    def lose(name, line_no, rs=False):
        """RV-E2's probes: truncate an EXISTING record line, so a real record is lost (not an extra torn line)."""
        root = os.path.join(scratch, name)
        if os.path.exists(root):
            shutil.rmtree(root)
        shutil.copytree(FX_FL1, root)
        path = os.path.join(root, "coordination.fleet.jsonl")
        rs_path = RS_LOG
        if rs:
            rs_path = os.path.join(root, "rs.jsonl")
            shutil.copyfile(RS_LOG, rs_path)
            path = rs_path
        with open(path, encoding="utf-8") as fh:
            lines = fh.readlines()
        lines[line_no - 1] = lines[line_no - 1][:40] + "\n"
        with open(path, "w", encoding="utf-8") as fh:
            fh.writelines(lines)
        return build(root, rs_path)

    p1 = lose("P1-lost-W8-return", 16)
    P1 = {r["item"]: r for r in p1["waiting"]}
    check(not p1["queueComplete"] and P1["W8"]["category"] == "unknown"
          and P1["W8"]["causes"][0].startswith("coordination log incomplete: line(s) [16]"),
          "VER-006 P1 (E2-R1) W8's return line truncated: the queue is marked incomplete and W8 is unknown, never 'in progress'")
    check(all(r["category"] in ("unknown", "done") for r in p1["waiting"]) and not any(r["category"].startswith("ready") for r in p1["waiting"]),
          "VER-006 P1 no item is ready while a log line is unread; done items stay done")
    p2 = lose("P2-lost-W2-dispatch", 4)
    P2 = {r["item"]: r for r in p2["waiting"]}
    check(P2["W2"]["category"] == "unknown" and any("thr-c2" in l and "dispatch record may be missing" in l for l in p2["limits"])
          and not p2["queueComplete"],
          "VER-006 P2 (E2-R1) W2's dispatch line truncated: W2 is unknown, never 'ready … no dispatch observed'; the orphaned observation is a limit")
    p3 = lose("P3-lost-RS-A16", 3, rs=True)
    P3 = {r["item"]: r for r in p3["waiting"]}
    check(any("RS records line 3" in l for l in p3["limits"]) and P3["W4"]["category"] == "unknown"
          and any("were not read" in c for c in P3["W4"]["causes"]),
          "VER-006 P3 (E2-R2) the A16's RS line truncated: no crash; a limit; W4's decision need is unknown, not outstanding or ready")

    ok = all(RESULTS)
    print(f"\nscratch: {scratch}\nRESULT: {'all expectations held' if ok else 'SOME EXPECTATIONS FAILED'} ({sum(RESULTS)}/{len(RESULTS)})")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
