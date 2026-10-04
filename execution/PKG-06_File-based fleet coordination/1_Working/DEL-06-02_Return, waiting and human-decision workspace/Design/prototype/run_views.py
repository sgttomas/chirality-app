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
from fleet_store import Writer, file_identity, vendored  # noqa: E402

EXECUTION = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", ".."))
FX_FL1 = os.path.normpath(os.path.join(HERE, "..", "..", "..", "DEL-06-01_Bounded delegation and current work-graph records",
                                       "Design", "prototype", "fixtures", "FX-FL1"))
RS_LOG = os.path.join(EXECUTION, "_Coordination", "AgentRuns", "APP-V4-DESIGN-PASS-4-20261003", "E", "fixtures", "FX-DP1",
                      "records", "coordination.rs.jsonl")
# Connector inputs: DEL-06-01 prototype/fixtures/vendored/EU-D1 (R23-44), hash-checked by fleet_store.vendored().
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

    print("\n== VER-002/VER-006 connector waiting cause (FV-10; S-3; R23-34.10, R23-37.4) ==")
    croot = os.path.join(scratch, "FX-FL1-connectors")
    if os.path.exists(croot):
        shutil.rmtree(croot)
    shutil.copytree(FX_FL1, croot)
    os.makedirs(os.path.join(croot, "connectors"))
    for name in ("PR-P6", "PR-P3", "PR-P1", "PR-P8"):
        shutil.copyfile(vendored(name + ".json"), os.path.join(croot, "connectors", name + ".json"))
    with open(vendored("PR-P8.json"), encoding="utf-8") as fh:
        p8 = json.load(fh)
    p8["route"]["needed"] = False
    with open(os.path.join(croot, "connectors", "PR-P8-noroute.json"), "w", encoding="utf-8") as fh:
        json.dump(p8, fh)
    with open(vendored("PR-P3.json"), encoding="utf-8") as fh:
        p3 = json.load(fh)
    forged = json.loads(json.dumps(p3)); forged["response_standing"]["supports_reliance"] = True
    with open(os.path.join(croot, "connectors", "PR-P3-forged.json"), "w", encoding="utf-8") as fh:
        json.dump(forged, fh)
    unk = json.loads(json.dumps(p3)); unk["response_standing"]["condition"] = "unknown"
    unk["response_standing"]["reasons"] = [{"facet": "condition", "value": "unknown", "basis": "constructed variant of PR-P3 for FV-10's CS-R5 case"}]
    with open(os.path.join(croot, "connectors", "PR-P3-unknown.json"), "w", encoding="utf-8") as fh:
        json.dump(unk, fh)
    with open(os.path.join(croot, "graphs", "FX-U1", "r2.json"), encoding="utf-8") as fh:
        r2 = json.load(fh)
    mgr = {"kind": "agent", "identity": "thread:fx-u1-manager", "role": "WORKING_ITEMS"}

    def need_c(name, connector="pec"):
        return {"kind": "connector", "connector": connector, "ref": f"connectors/{name}.json", "condition": "the PEC answer to Q1"}
    with open(vendored("PR-P6.json"), "rb") as fh:
        p6 = fh.read()
    with open(os.path.join(croot, "connectors", "PR-P6-half.json"), "wb") as fh:
        fh.write(p6[: len(p6) // 2])                                  # RV2 probe: half-truncated
    with open(os.path.join(croot, "connectors", "PR-P6-renamed.json"), "wb") as fh:
        fh.write(p6.replace(b'"response_standing"', b'"standing_v2"'))  # RV2 probe: renamed key (format drift)
    extra = [
        {"itemId": "W10", "outcome": "Q1 answered (PEC absent)", "owner": mgr, "needs": [need_c("PR-P6")], "selected": True},
        {"itemId": "W11", "outcome": "Q1 answered (PEC stale)", "owner": mgr, "needs": [need_c("PR-P3")], "selected": True},
        {"itemId": "W12", "outcome": "Stage plan using Q1", "owner": mgr,
         "needs": [need_c("PR-P1"), {"kind": "item", "ref": "W2"}], "selected": True},
        {"itemId": "W13", "outcome": "Q1 answered (PEC adopted, current)", "owner": mgr, "needs": [need_c("PR-P1")], "selected": True},
        {"itemId": "W14", "outcome": "Q1 answered (forged standing)", "owner": mgr, "needs": [need_c("PR-P3-forged")], "selected": True},
        {"itemId": "W15", "outcome": "Q1 answered (condition unknown)", "owner": mgr, "needs": [need_c("PR-P3-unknown")], "selected": True},
        {"itemId": "W16", "outcome": "Q1 (half-truncated record)", "owner": mgr, "needs": [need_c("PR-P6-half")], "selected": True},
        {"itemId": "W17", "outcome": "Q1 (renamed standing key)", "owner": mgr, "needs": [need_c("PR-P6-renamed")], "selected": True},
        {"itemId": "W18", "outcome": "Q1 (record missing)", "owner": mgr, "needs": [need_c("PR-P9-missing")], "selected": True},
        {"itemId": "W19", "outcome": "Q1 (connector record as plain input)", "owner": mgr,
         "needs": [{"kind": "input", "ref": "connectors/PR-P1.json"}], "selected": True},
        {"itemId": "W20", "outcome": "Q1 (declared domains, record is pec)", "owner": mgr, "needs": [need_c("PR-P1", "domains")], "selected": True},
        {"itemId": "W21", "outcome": "Q1 (P8: claim c3 unknown, route needed)", "owner": mgr, "needs": [need_c("PR-P8")], "selected": True},
        {"itemId": "W22", "outcome": "Q1 (P8: claim c3 unknown, no route)", "owner": mgr, "needs": [need_c("PR-P8-noroute")], "selected": True}]
    r3 = {"format": "chirality.fleet.record", "formatVersion": "0.1", "recordId": "fl:graph:FX-U1:r3", "kind": "work_graph",
          "undertaking": "FX-U1", "recorder": mgr, "writtenAt": "g3",
          "body": {"revision": 3, "supersedes": "fl:graph:FX-U1:r2", "projectDagRef": r2["body"]["projectDagRef"],
                   "items": r2["body"]["items"] + extra}}
    w = Writer(croot)
    p3path = w.graph(r3)
    w.log({"format": "chirality.fleet.record", "formatVersion": "0.1", "recordId": "fl:log:0019", "kind": "current_graph",
           "undertaking": "FX-U1", "recorder": mgr, "writtenAt": "s3",
           "body": {"graph": "fl:graph:FX-U1:r3", "graphContent": file_identity(p3path)}})
    cv = build(croot, RS_LOG)
    C = {r["item"]: r for r in cv["waiting"]}
    check(C["W10"]["category"] == "waiting" and any("condition absent" in c and "envelope unknown" in c and "ra:EUD1-Q1" in c for c in C["W10"]["causes"])
          and "pr:EUD1-P6" in C["W10"]["sources"],
          "FV-10 W10 (PR-P6, PEC absent): waiting on the connector, with its standing and the route account ra:EUD1-Q1; never ready")
    check(C["W11"]["category"] == "waiting" and any("envelope adopted, condition stale" in c and "does not support reliance" in c for c in C["W11"]["causes"]),
          "FV-10 W11 (PR-P3, adopted but stale): waiting; reliance not supported (CS-R1)")
    check(C["W12"]["category"] == "waiting" and any(c.startswith("waits for W2") for c in C["W12"]["causes"])
          and any(c.startswith("connector reliance supported") and "pr:EUD1-P1" in c for c in C["W12"]["causes"]),
          "FV-10 W12 (PR-P1, adopted and current): reliance supported, yet W12 still waits for W2; the connector makes nothing ready")
    check(C["W13"]["category"] == "ready (qualified)" and any("connector reliance supported" in c and "ra:EUD1-Q1 is still needed" in c for c in C["W13"]["causes"]),
          "FV-10 W13 (PR-P1 only): ready, its one need met by connector material that supports reliance (CS-R1), naming the route still needed for Q1(b) (FV10-R3); still qualified by thr-cx (FV-4a)")
    check(C["W14"]["category"] == "unknown" and any("does not conform" in c for c in C["W14"]["causes"]),
          "FV-10 W14 (PR-P3 altered to claim reliance while stale): nonconformant to DEL-07-02's schema, so unknown, never ready")
    check(C["W15"]["category"] == "unknown" and any("condition unknown" in c for c in C["W15"]["causes"]),
          "FV-10 W15 (condition unknown): unknown stays unknown (CS-R5)")
    base = {r["item"]: (r["category"], r["causes"]) for r in v["waiting"]}
    check(all(base[i] == (C[i]["category"], C[i]["causes"]) for i in base),
          "FV-10 C7 (CS-R2 as restated by R23-40) adding connector items and records changes no other item's category or causes")
    check(C["W16"]["category"] == "unknown" and C["W17"]["category"] == "unknown"
          and any("unreadable" in c for c in C["W16"]["causes"]) and any("has no standing" in c for c in C["W17"]["causes"]),
          "FV10-R1 RV2's probes: a half-truncated record and a renamed standing key make the need unknown, never satisfied by presence")
    check(C["W18"]["category"] == "waiting" and any("not present" in c and "connector pec" in c for c in C["W18"]["causes"]),
          "FV10-R1 a missing record for a declared connector need is outstanding, with the connector named")
    check(C["W19"]["category"] == "unknown" and any("named as a plain input" in c for c in C["W19"]["causes"])
          and C["W20"]["category"] == "unknown" and any("not the declared domains" in c for c in C["W20"]["causes"]),
          "FV10-R1 a connector record named as a plain input, or declared under the wrong connector, is unknown; presence never applies")
    check(C["W21"]["category"] == "ready (qualified)" and any("claim(s) not relied: c3 unknown" in c and "ra:EUD1-Q1 is still needed" in c
                                                              for c in C["W21"]["causes"]),
          "FV10-R7 C13 PR-P8 with route.needed true: the row names claim c3 unknown and the route covering it")
    check(C["W22"]["category"] == "unknown" and any("c3 unknown" in c and "names no source-file route" in c for c in C["W22"]["causes"]),
          "FV10-R7 C14 PR-P8 with route.needed false: unknown, never a bare 'reliance supported'")
    from fleet_store import Reader as _R
    raw = {f["itemId"]: f for f in _R(croot, RS_LOG).item_facts("FX-U1")["items"]}
    expect = {"W10": "outstanding", "W11": "outstanding", "W13": "satisfied", "W14": "unknown", "W15": "unknown",
              "W16": "unknown", "W17": "unknown", "W18": "outstanding", "W20": "unknown", "W21": "satisfied", "W22": "unknown"}
    agree = all(raw[i]["needs"][0]["state"] == s and raw[i]["needs"][0].get("connectorNeed") for i, s in expect.items())
    check(agree and C["W10"]["category"] == "waiting",
          "FV-10 C8 (R23-39) DEL-06-01's facts (RF-5a) now read connector needs by CS-R1; FV-10 words them, no override")

    ok = all(RESULTS)
    print(f"\nscratch: {scratch}\nRESULT: {'all expectations held' if ok else 'SOME EXPECTATIONS FAILED'} ({sum(RESULTS)}/{len(RESULTS)})")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
