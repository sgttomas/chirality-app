"""DEL-06-01 prototype check (FLEET_RECORDS.md FR-v0.1 §9): designed cases for VER-001...VER-005 and VER-007.

Prototype only, not product code; invented subject matter; no act was performed. Python 3 standard library.
Usage: python3 -B run_fleet.py [scratch] [--write-fixture]
  Builds fixture FX-FL1 in scratch through the writer, checks it, and (with --write-fixture) copies it to
  fixtures/FX-FL1/ beside this file, with MANIFEST.sha256. Exit 0 only if every expectation held.
Decision needs read the RS records of the early-path fixture FX-DP1 (run APP-V4-DESIGN-PASS-4-20261003, E/).
"""

import copy
import hashlib
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fleet_store import Writer, Reader, Refused, file_identity, schema, validate, EXECUTION  # noqa: E402

FX_DP1 = os.path.join(EXECUTION, "_Coordination", "AgentRuns", "APP-V4-DESIGN-PASS-4-20261003", "E", "fixtures", "FX-DP1")
RS_LOG = os.path.join(FX_DP1, "records", "coordination.rs.jsonl")
U = "FX-U1"
PIN = "0.158.0 (definition pin; same at 0.160.0 for these surfaces: VC F16 types unchanged)"
RESULTS = []


def check(cond, label):
    RESULTS.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + label)


def hdr(rid, kind, recorder, t, body):
    return {"format": "chirality.fleet.record", "formatVersion": "0.1", "recordId": rid, "kind": kind,
            "undertaking": U, "recorder": recorder, "writtenAt": t, "body": body}


APP = {"kind": "App", "identity": "app-writer:local"}
MGR = {"kind": "agent", "identity": "thread:fx-u1-manager", "role": "WORKING_ITEMS"}
PERSON = {"kind": "person", "identity": "Engineer A", "identityVerified": False}


def brief(bid, item, purpose, target, ret):
    return hdr(f"fl:brief:{bid}", "brief", MGR, f"b-{bid}", {
        "briefId": f"brief:{bid}", "workItem": item, "purpose": purpose,
        "basis": [{"kind": "file", "ref": "basis/FX-U1-SCOPE.md"}],
        "context": [{"kind": "file", "ref": "basis/FX-U1-NOTES.md"}],
        "authority": {"mayDecide": ["wording and structure within the section"],
                      "escalate": ["any change outside the write scope", "any reserved act"],
                      "reservedToPerson": ["choosing the stage-2 route (PKG-1)"]},
        "tools": [{"tool": "shell commands", "limit": {"statement": "within the person's Codex sandbox setting",
                   "standing": "enforced-by-supplier", "mechanism": "Codex sandbox mode workspace-write (the person's own setting, D3)"}},
                  {"tool": "network", "limit": {"statement": "no network use", "standing": "stated-not-enforced"}}],
        "writeScope": [{"target": target, "limit": {"statement": f"write only {target}", "limitId": "L-ALL-1",
                        "standing": "stated-not-enforced"}}],
        "expectedReturn": {"description": ret, "form": "file and message", "returnPath": "the parent conversation; the file in the write scope",
                           "artifacts": [target]},
        "preparedBy": MGR, "delegateRole": "TASK",
        "limits": [{"statement": "a task agent does not delegate", "limitId": "L-TASK-1", "standing": "stated-not-enforced",
                    "source": {"kind": "external", "ref": "ROLE-v0.2 §6.2 limit account (runtime value, no register row)"}}]})


def item(iid, outcome, owner, needs=(), brief_id=None, selected=True, results=None):
    it = {"itemId": iid, "outcome": outcome, "owner": owner, "needs": list(needs), "selected": selected}
    if brief_id:
        it["brief"] = brief_id
    if results:
        it["results"] = results
    return it


def obs(src, at, standing="observed through an adapter, not stock behaviour"):
    return {"source": src, "at": at, "pin": PIN, "standing": standing}


def build(root):
    w = Writer(root)
    for b in (brief("W1", "W1", "Survey section A of the FX-U1 scope", "SURVEY/A.md", "SURVEY/A.md and a one-paragraph summary"),
              brief("W2", "W2", "Survey section B of the FX-U1 scope", "SURVEY/B.md", "SURVEY/B.md and a summary"),
              brief("W3", "W3", "Combine sections A and B", "SURVEY/AB.md", "SURVEY/AB.md"),
              brief("W7", "W7", "Draft the glossary", "GLOSSARY.md", "GLOSSARY.md"),
              brief("W8", "W8", "Survey section C", "SURVEY/C.md", "SURVEY/C.md")):
        w.brief(b)
    task = {"kind": "agent", "identity": "child (thread observed)", "role": "TASK"}
    r1_items = [item("W1", "Section A surveyed", task, brief_id="brief:W1"),
                item("W2", "Section B surveyed", task, brief_id="brief:W2"),
                item("W3", "A and B combined", MGR, needs=[{"kind": "item", "ref": "W1"}, {"kind": "item", "ref": "W2"}], brief_id="brief:W3")]
    p1 = w.graph(hdr("fl:graph:FX-U1:r1", "work_graph", MGR, "g1", {"revision": 1, "projectDagRef": "none (invented undertaking)", "items": r1_items}))
    w.log(hdr("fl:log:0001", "current_graph", MGR, "s1", {"graph": "fl:graph:FX-U1:r1", "graphContent": file_identity(p1)}))
    ext_owner = {"kind": "external", "identity": "host session (human-relayed)", "role": "not known"}
    r2_items = r1_items + [
        item("W4", "Stage 2 started", MGR, needs=[{"kind": "decision", "ref": "rec:app:coord:0001", "condition": "the person decides PKG-1"}]),
        item("W5", "Stage 2 reviewer engaged", MGR, needs=[{"kind": "decision", "ref": "rec:app:coord:0002"}]),
        item("W6", "Host-side check result", ext_owner),
        item("W7", "Glossary drafted", task, brief_id="brief:W7"),
        item("W8", "Section C surveyed", task, brief_id="brief:W8"),
        item("W9", "Report assembled", MGR, needs=[{"kind": "item", "ref": "W6"}, {"kind": "input", "ref": "inputs/STYLE.md"}])]
    p2 = w.graph(hdr("fl:graph:FX-U1:r2", "work_graph", MGR, "g2", {"revision": 2, "supersedes": "fl:graph:FX-U1:r1",
                                                                   "projectDagRef": "none (invented undertaking)", "items": r2_items}))
    w.log(hdr("fl:log:0002", "current_graph", MGR, "s2", {"graph": "fl:graph:FX-U1:r2", "graphContent": file_identity(p2)}))
    for n, (bid, child) in enumerate((("W1", "thr-c1"), ("W2", "thr-c2"), ("W7", "thr-c7"), ("W8", "thr-c8")), start=3):
        bpath = os.path.join(root, "briefs", f"{bid}.json")
        w.log(hdr(f"fl:log:{n:04d}", "dispatch_observed", APP, f"d{n}", {
            "mechanism": "Codex native subagent", "childThread": child, "parentThread": "thr-mgr",
            "parentSource": "thread/read", "agentRole": "fx_task", "spawnItem": f"item-spawn-{bid}",
            "association": {"state": "brief reference in spawn prompt", "brief": f"brief:{bid}", "briefContent": file_identity(bpath)},
            "delegatingRoleLimit": {"statement": "a task agent does not delegate", "limitId": "L-TASK-1", "standing": "stated-not-enforced"},
            "observation": obs(f"collabAgentToolCall spawnAgent item-spawn-{bid} (completed)", f"t{n}")}))
    w.log(hdr("fl:log:0007", "dispatch_observed", APP, "d7", {
        "mechanism": "Codex native subagent", "childThread": "thr-cx", "parentThread": "thr-mgr", "parentSource": "thread/read",
        "agentRole": None, "spawnItem": "item-spawn-x", "association": {"state": "no brief reference"},
        "observation": obs("collabAgentToolCall spawnAgent item-spawn-x (completed)", "t7")}))
    w.log(hdr("fl:log:0008", "child_observed", APP, "o8", {"childThread": "thr-c1", "status": "completed", "observation": obs("agentsStates at wait", "t8")}))
    w.log(hdr("fl:log:0009", "child_observed", APP, "o9", {"childThread": "thr-c2", "status": "running", "observation": obs("agentsStates", "t9")}))
    w.log(hdr("fl:log:0010", "child_observed", APP, "o10", {"childThread": "thr-c7", "status": "completed", "observation": obs("agentsStates at wait", "t10")}))
    w.log(hdr("fl:log:0011", "return_recorded", MGR, "r11", {
        "workItem": "W1", "brief": "brief:W1", "returnedBy": {"kind": "agent", "identity": "thr-c1", "role": "TASK"},
        "returned": [{"kind": "file", "ref": "SURVEY/A.md", "contentIdentity": {"method": "TEST VALUE", "value": "a1"}}],
        "evidence": [{"kind": "supplier item", "ref": "thr-mgr wait item (child's final message)"}]}))
    w.log(hdr("fl:log:0012", "review_recorded", MGR, "v12", {
        "workItem": "W1", "returnRef": "fl:log:0011", "reviewer": {"kind": "agent", "identity": "thread:fx-u1-reviewer", "role": "TASK"},
        "verdict": "no blocking findings", "findings": [{"kind": "file", "ref": "reviews/W1.md"}],
        "reviewedContent": [{"kind": "file", "ref": "SURVEY/A.md", "contentIdentity": {"method": "TEST VALUE", "value": "a1"}}]}))
    w.log(hdr("fl:log:0013", "integration_recorded", MGR, "i13", {
        "workItem": "W1", "returnRef": "fl:log:0011", "reviewRef": "fl:log:0012", "integrator": MGR,
        "evidence": [{"kind": "commit", "ref": "commit 0000a1 (invented)"}]}))
    w.log(hdr("fl:log:0014", "basis_changed", MGR, "c14", {
        "changed": {"kind": "file", "ref": "basis/FX-U1-SCOPE.md"}, "previous": {"method": "TEST VALUE", "value": "s1"},
        "affectedItems": ["W2", "W3"], "note": "section B's scope narrowed"}))
    w.log(hdr("fl:log:0015", "observation_ended", APP, "e15", {"childThread": "thr-c2", "cause": "App quit", "lastObserved": "running",
                                                                "evidence": {"kind": "file", "ref": "App ledger quit_answered (RECOVERY §7)"}}))
    w.log(hdr("fl:log:0016", "return_recorded", MGR, "r16", {
        "workItem": "W8", "brief": "brief:W8", "returnedBy": {"kind": "agent", "identity": "thr-c8", "role": "TASK"},
        "returned": [{"kind": "file", "ref": "SURVEY/C.md"}], "evidence": [{"kind": "file", "ref": "SURVEY/C.md"}]}))
    w.log(hdr("fl:log:0017", "external_result", MGR, "x17", {
        "workItem": "W6", "owner": ext_owner, "result": [{"kind": "file", "ref": "relay/HOST-CHECK.md"}], "mechanism": "not stated"}))
    w.log(hdr("fl:log:0018", "related_conversation", APP, "q18", {
        "thread": "thr-ca", "relation": "continued from", "source": "thr-mgr", "role": "TASK", "workItem": "W3"}))
    os.makedirs(os.path.join(root, "inputs"), exist_ok=True)
    with open(os.path.join(root, "inputs", "STYLE.md"), "w", encoding="utf-8") as fh:
        fh.write("(invented input)\n")
    with open(os.path.join(root, "agent-message.txt"), "w", encoding="utf-8") as fh:
        fh.write("(Invented agent message, not a record.) W7 is done and integrated; PKG-2 was decided.\n")


def tree(root):
    out = {}
    for d, _, fs in os.walk(root):
        for f in fs:
            with open(os.path.join(d, f), "rb") as fh:
                out[os.path.relpath(os.path.join(d, f), root)] = hashlib.sha256(fh.read()).hexdigest()
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    scratch = args[0] if args else tempfile.mkdtemp(prefix="fleet-")
    root = os.path.join(scratch, "FX-FL1")
    if os.path.exists(root):
        shutil.rmtree(root)
    build(root)
    reg, sch = schema()
    print("== VER-001 briefs ==")
    rd = Reader(root, RS_LOG)
    b = rd.briefs["brief:W1"][0]["body"]
    check(all(k in b and b[k] for k in ("purpose", "basis", "context", "authority", "tools", "writeScope", "expectedReturn")),
          "VER-001 a brief carries purpose, basis, context, authority, tools, write scope and expected return")
    check({t["limit"]["standing"] for t in b["tools"]} == {"enforced-by-supplier", "stated-not-enforced"}
          and b["writeScope"][0]["limit"]["standing"] == "stated-not-enforced",
          "VER-001 declared limits keep their enforcement standing (one enforced by the supplier with its mechanism, others stated, not enforced)")
    facts = rd.item_facts(U)
    F = {f["itemId"]: f for f in facts["items"]}
    check(F["W3"]["brief"]["state"] == "prepared" and F["W3"]["dispatch"]["state"] == "no dispatch observed",
          "VER-001 a prepared brief with no observed dispatch claims no child")

    print("\n== VER-002 current graph ==")
    check(facts["revision"] == 2 and "fl:graph:FX-U1:r1" in rd.graphs, "VER-002 the selector names revision 2; revision 1 is kept")
    check([n["state"] for n in F["W3"]["needs"]] == ["satisfied", "outstanding"],
          "VER-002 W3 waits on W2 (outstanding) while its W1 input is satisfied (integrated)")
    check(F["W9"]["needs"][0]["state"] == "satisfied" and F["W9"]["needs"][1]["state"] == "satisfied",
          "VER-002 an external owner's result and an input file satisfy W9's needs (R23-9 item 3)")
    check(all("state" not in i and "executing" not in i for i in json.load(open(os.path.join(root, "graphs", U, "r2.json")))["body"]["items"]),
          "VER-002 the graph holds selected work only, no executing state")
    re_read = Reader(root, RS_LOG).item_facts(U)
    check(re_read == facts, "VER-002 recovering from the files again gives the same facts")

    print("\n== VER-003 association ==")
    check(F["W1"]["dispatch"]["child"] == "thr-c1" and F["W1"]["dispatch"]["parent"] == "thr-mgr"
          and F["W1"]["dispatch"]["association"] == "brief reference in spawn prompt",
          "VER-003 W1's child and parent identities are kept, with how the brief was associated")
    check(any(c["association"] == "no brief reference" and c["brief"] is None for c in facts["childIndex"]),
          "VER-003 a child spawned without a brief reference is indexed, associated with no brief (R23-4)")
    check(F["W2"]["observed"][-1].get("ended") == "App quit" and F["W2"]["return"] is None,
          "VER-003 unknown outcome: W2's observation ended at quit with 'running' last; no return is inferred")

    print("\n== VER-004 changed basis, interruption, returns ==")
    check(F["W7"]["observed"][0]["status"] == "completed" and F["W7"]["return"] is None,
          "VER-004 W7's child completed (Codex's status) and the agent's message claims it done: no return recorded, none inferred")
    check(F["W8"]["return"]["state"] == "returned" and F["W8"]["review"] is None and F["W8"]["integration"] is None,
          "VER-004 W8 returned and awaits review: not promoted")
    check(F["W1"]["return"] and F["W1"]["review"]["verdict"] == "no blocking findings" and F["W1"]["integration"]["state"] == "integrated"
          and len({F["W1"]["return"]["source"], F["W1"]["review"]["source"], F["W1"]["integration"]["source"]}) == 3,
          "VER-004 W1's return, review and integration each rest on their own record")
    check(F["W2"]["basisChanged"] == ["fl:log:0014"] and F["W3"]["basisChanged"] == ["fl:log:0014"],
          "VER-004 the basis change names W2 and W3 and reopens nothing by itself")
    check(F["W3"]["related"] == [{"thread": "thr-ca", "relation": "continued from", "source": "thr-mgr"}] and F["W3"]["dispatch"]["state"] == "no dispatch observed",
          "VER-004 a 'Continue as' conversation is a related conversation, not a dispatch (R23-9 item 2)")

    print("\n== VER-005 decisions and human acts ==")
    check(F["W4"]["needs"][0]["state"] == "satisfied" and "A16" in F["W4"]["needs"][0]["why"],
          "VER-005 W4's decision need is satisfied by the person's recorded A16 on PKG-1 (FX-DP1)")
    check(F["W5"]["needs"][0]["state"] == "outstanding",
          "VER-005 W5's decision on PKG-2 stays outstanding: the agent's message is not a record")
    rd_none = Reader(root)
    check(Reader(root).item_facts(U)["items"][3]["needs"][0]["state"] == "unknown",
          "VER-005 without the RS records the decision need is unknown, never satisfied")

    print("\n== VER-007 PEC absent; writer and reader limits ==")
    check(not any("PEC" in json.dumps(f) for f in facts["items"]) and facts["items"],
          "VER-007 the facts derive from files alone; no PEC input exists in the reader")
    before = tree(root)
    Reader(root, RS_LOG).item_facts(U)
    check(tree(root) == before, "RF-9 reading writes nothing")
    w = Writer(root)
    bad = copy.deepcopy(rd.briefs["brief:W1"][0]); del bad["body"]["writeScope"]; bad["body"]["briefId"] = "brief:WX"
    try:
        w.brief(bad); refused = False
    except Refused:
        refused = True
    check(refused and not os.path.exists(os.path.join(root, "briefs", "WX.json")), "W-1 a brief without a write scope is refused and not written")
    try:
        w.brief(rd.briefs["brief:W1"][0]); overwrote = True
    except FileExistsError:
        overwrote = False
    check(not overwrote, "W-2 a brief file is never overwritten (a changed brief is a new brief)")
    tam = os.path.join(scratch, "FX-FL1-tampered")
    if os.path.exists(tam):
        shutil.rmtree(tam)
    shutil.copytree(root, tam)
    with open(os.path.join(tam, "graphs", U, "r2.json"), "a", encoding="utf-8") as fh:
        fh.write(" ")
    with open(os.path.join(tam, "coordination.fleet.jsonl"), "a", encoding="utf-8") as fh:
        fh.write('{"format": "chirality.fleet.record", "kind": "child_obs')
    t = Reader(tam, RS_LOG).item_facts(U)
    check(t["items"] == [] and any("differs" in n for n in t["notes"]) and any("partial" in l for l in t["limits"]),
          "RF-1 a graph changed after selection is not used; a torn log line is a limit")

    # RV E2-R1 / E2-R2: lost records are reported, not silently dropped.
    lost = os.path.join(scratch, "FX-FL1-lost")
    if os.path.exists(lost):
        shutil.rmtree(lost)
    shutil.copytree(root, lost)
    lp = os.path.join(lost, "coordination.fleet.jsonl")
    with open(lp, encoding="utf-8") as fh:
        lines = fh.readlines()
    lines[3] = lines[3][:40] + "\n"          # W2's dispatch_observed, truncated
    with open(lp, "w", encoding="utf-8") as fh:
        fh.writelines(lines)
    lf = Reader(lost, RS_LOG).item_facts(U)
    check(lf["logIncomplete"] == [4] and lf["orphanChildren"] == ["thr-c2"],
          "RF-10/RF-12 a truncated dispatch line is reported as unread, and its child's later observations as orphans")
    rs_torn = os.path.join(scratch, "rs-torn.jsonl")
    with open(RS_LOG, encoding="utf-8") as fh:
        rl = fh.readlines()
    rl[2] = rl[2][:40] + "\n"                 # the A16 on PKG-1, truncated
    with open(rs_torn, "w", encoding="utf-8") as fh:
        fh.writelines(rl)
    rf = Reader(root, rs_torn)
    tf = {f["itemId"]: f for f in rf.item_facts(U)["items"]}
    check(any("RS records line 3" in l for l in rf.limits) and tf["W4"]["needs"][0]["state"] == "unknown"
          and tf["W5"]["needs"][0]["state"] == "unknown",
          "RF-11 (E2-R2) a torn RS line is a limit, not a crash; decision needs it could hold are unknown")

    # RF-5a (R23-39; RV2 FV10-R1, FV10-R3): declared connector needs, read from vendored inputs (R23-44).
    import fleet_store
    croot = os.path.join(scratch, "FX-FL1-connectors")
    if os.path.exists(croot):
        shutil.rmtree(croot)
    shutil.copytree(root, croot)
    os.makedirs(os.path.join(croot, "connectors"))
    for name in ("PR-P6", "PR-P3", "PR-P1"):
        shutil.copyfile(fleet_store.vendored(name + ".json"), os.path.join(croot, "connectors", name + ".json"))
    with open(fleet_store.vendored("PR-P3.json"), encoding="utf-8") as fh:
        forged = json.load(fh)
    forged["response_standing"]["supports_reliance"] = True
    with open(os.path.join(croot, "connectors", "PR-P3-forged.json"), "w", encoding="utf-8") as fh:
        json.dump(forged, fh)
    with open(fleet_store.vendored("PR-P6.json"), "rb") as fh:
        p6 = fh.read()
    with open(os.path.join(croot, "connectors", "PR-P6-half.json"), "wb") as fh:
        fh.write(p6[: len(p6) // 2])
    with open(os.path.join(croot, "connectors", "PR-P6-renamed.json"), "wb") as fh:
        fh.write(p6.replace(b'"response_standing"', b'"standing_v2"'))
    cw = Writer(croot)
    r2 = Reader(croot, RS_LOG).graphs["fl:graph:FX-U1:r2"][0]

    def cneed(n, c="pec"):
        return {"kind": "connector", "connector": c, "ref": f"connectors/{n}.json"}
    extra = [item("C2", "stale connector", MGR, needs=[cneed("PR-P3")]), item("C5", "forged standing", MGR, needs=[cneed("PR-P3-forged")]),
             item("C8a", "absent connector", MGR, needs=[cneed("PR-P6")]), item("C8b", "adopted, current", MGR, needs=[cneed("PR-P1")]),
             item("C8c", "plain input", MGR, needs=[{"kind": "input", "ref": "inputs/STYLE.md"}]),
             item("H1", "half-truncated", MGR, needs=[cneed("PR-P6-half")]), item("H2", "renamed key", MGR, needs=[cneed("PR-P6-renamed")]),
             item("H3", "missing", MGR, needs=[cneed("PR-P9")]), item("H4", "undeclared", MGR, needs=[{"kind": "input", "ref": "connectors/PR-P1.json"}])]
    gp = cw.graph(hdr("fl:graph:FX-U1:r3", "work_graph", MGR, "g3", {"revision": 3, "supersedes": "fl:graph:FX-U1:r2",
                                                                     "projectDagRef": r2["body"]["projectDagRef"],
                                                                     "items": r2["body"]["items"] + extra}))
    cw.log(hdr("fl:log:0019", "current_graph", MGR, "s3", {"graph": "fl:graph:FX-U1:r3", "graphContent": file_identity(gp)}))
    cf = {f["itemId"]: f["needs"][0] for f in Reader(croot, RS_LOG).item_facts(U)["items"] if f["itemId"] in [x["itemId"] for x in extra]}
    check(cf["C2"]["state"] == "outstanding" and cf["C2"].get("connectorNeed") and cf["C2"]["route"] == "ra:EUD1-Q1"
          and "condition stale" in cf["C2"]["why"],
          "RF-5a C2 an adopted but stale connector record is present yet outstanding (CS-R1), with its route account")
    check(cf["C5"]["state"] == "unknown" and "does not conform" in cf["C5"]["why"],
          "RF-5a C5 a stale standing altered to claim reliance is nonconformant to DEL-07-02's schema: unknown, never satisfied")
    check(cf["C8a"]["state"] == "outstanding" and cf["C8b"]["state"] == "satisfied" and cf["C8c"]["state"] == "satisfied"
          and cf["C8c"]["why"] == "input present" and not cf["C8c"].get("connectorNeed"),
          "RF-5a C8 presence never satisfies a connector need (absent: outstanding; adopted and current: satisfied); a plain input still reads by presence")
    check(cf["C8b"].get("routeNeeded") and "ra:EUD1-Q1 is still needed" in cf["C8b"]["why"],
          "RF-5a (FV10-R3) a satisfied connector need names the source-file route the record says is still needed")
    check(cf["H1"]["state"] == "unknown" and cf["H2"]["state"] == "unknown" and cf["H3"]["state"] == "outstanding"
          and "not present" in cf["H3"]["why"] and cf["H4"]["state"] == "unknown",
          "RF-5a/RF-5b (FV10-R1) half-truncated or renamed-key record: unknown; missing: outstanding; undeclared connector record as input: unknown")
    saved = fleet_store.VENDORED
    tam = os.path.join(scratch, "vendored-tampered")
    if os.path.exists(tam):
        shutil.rmtree(tam)
    shutil.copytree(saved, tam)
    with open(os.path.join(tam, "connector.standing.schema.json"), "a", encoding="utf-8") as fh:
        fh.write(" ")
    fleet_store.VENDORED = tam
    try:
        fleet_store.connector_need(croot, cneed("PR-P1")); refused = False
    except fleet_store.VendoredInputChanged:
        refused = True
    finally:
        fleet_store.VENDORED = saved
    check(refused, "R23-44 a vendored input whose bytes differ from VENDOR.json is refused before use")

    print("\n== invalid records (schema) ==")
    disp = next(e for e in rd.log if e["kind"] == "dispatch_observed")
    inv = []
    x = copy.deepcopy(rd.briefs["brief:W1"][0]); x["body"]["tools"][0]["limit"].pop("mechanism"); inv.append(("INV-FL-1 an 'enforced' limit without its mechanism", x))
    x = copy.deepcopy(disp); x["recorder"] = MGR; inv.append(("INV-FL-2 a dispatch recorded by an agent (only the App's observation records one)", x))
    x = copy.deepcopy(disp); x["body"]["association"] = {"state": "no brief reference", "brief": "brief:W1"}; inv.append(("INV-FL-3 'no brief reference' naming a brief", x))
    g = copy.deepcopy(rd.graphs["fl:graph:FX-U1:r2"][0]); g["body"]["items"][0]["state"] = "executing"; inv.append(("INV-FL-4 an executing state in the graph", g))
    x = copy.deepcopy(next(e for e in rd.log if e["kind"] == "return_recorded")); x["body"]["evidence"] = []; inv.append(("INV-FL-5 a return without evidence", x))
    x = copy.deepcopy(next(e for e in rd.log if e["kind"] == "related_conversation")); x["body"]["relation"] = "delegated to"; inv.append(("INV-FL-6 a related conversation called a delegation", x))
    x = copy.deepcopy(disp); x["body"]["mechanism"] = "brief written"; inv.append(("INV-FL-7 a dispatch whose mechanism is a written brief", x))
    g = copy.deepcopy(rd.graphs["fl:graph:FX-U1:r2"][0]); g["body"]["items"][0]["needs"] = [{"kind": "connector", "ref": "connectors/PR-P1.json"}]
    inv.append(("INV-FL-8 a connector need that does not name its connector (RF-5a)", g))
    g = copy.deepcopy(rd.graphs["fl:graph:FX-U1:r2"][0]); g["body"]["items"][0]["needs"] = [{"kind": "input", "ref": "x", "connector": "pec"}]
    inv.append(("INV-FL-9 a connector named on a plain input need (declare kind 'connector')", g))
    for name, inst in inv:
        errs = validate(inst, sch, reg)
        check(errs, f"{name}: invalid as expected -> {errs[0][:90] if errs else 'VALID (unexpected)'}")

    if "--write-fixture" in sys.argv:
        dst = os.path.join(HERE, "fixtures", "FX-FL1")
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(root, dst)
        rows = sorted(tree(dst).items())
        with open(os.path.join(dst, "MANIFEST.sha256"), "w", encoding="utf-8") as fh:
            for rel, h in rows:
                fh.write(f"{h}  {rel}\n")
        print(f"\nwrote fixture {dst}")
    else:
        dst = os.path.join(HERE, "fixtures", "FX-FL1")
        if os.path.exists(dst):
            committed = tree(dst)
            committed.pop("MANIFEST.sha256", None)
            check(committed == tree(root), "the committed fixture FX-FL1 equals the one built now")
    ok = all(RESULTS)
    print(f"\nRESULT: {'all expectations held' if ok else 'SOME EXPECTATIONS FAILED'} ({sum(RESULTS)}/{len(RESULTS)})")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
