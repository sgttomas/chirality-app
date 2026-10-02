#!/usr/bin/env python3
"""Run the ROLE-v0.2 prototype cases (ROLE §10). Python 3 standard library only.

    python3 run_cases.py                    # run the cases
    python3 run_cases.py --write-examples   # also (re)write the schema examples beside ROLE_SUPPLY.md

Scratch files go to a fresh folder under $TMPDIR. Nothing is sent anywhere; the
supplier is a test double. Output is also written to results/run-<date>.txt
when --record is given.
"""
import copy
import inspect
import datetime
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import role_supply as rs          # noqa: E402
from jsonschema_lite import errors  # noqa: E402

FIX = os.path.join(HERE, "fixtures")
SUPPLY_SCHEMA = json.load(open(os.path.join(DESIGN, "role-supply-record.schema.json")))
LIMIT_SCHEMA = json.load(open(os.path.join(DESIGN, "role-limit-account.schema.json")))
OUT = []
RESULTS = {"pass": 0, "fail": 0}


def say(s=""):
    OUT.append(s)
    print(s)


def check(case, cond, detail=""):
    RESULTS["pass" if cond else "fail"] += 1
    say("%s %s%s" % ("PASS" if cond else "FAIL", case, (" — " + detail) if detail else ""))


def fresh(tmp, name):
    d = os.path.join(tmp, name)
    os.makedirs(d)
    return d


def main():
    write_examples = "--write-examples" in sys.argv
    record = "--record" in sys.argv
    tmp = tempfile.mkdtemp(prefix="chirality-d6-role-", dir=os.environ.get("TMPDIR"))
    say("ROLE-v0.2 prototype run %s; python %s; scratch under $TMPDIR (%s)" % (
        datetime.date.today().isoformat(), sys.version.split()[0], os.path.basename(tmp)))
    bundled = os.path.join(FIX, "bundled")
    roleset = rs.RoleSet(bundled)

    # RC-01 role set and preselection
    conv = rs.Conversation(roleset)
    ok1 = (conv.role == "HELP_HUMAN" and conv.preselected)
    conv.on("clear")
    check("RC-01 four roles; preselection from role-set data is shown and clearable",
          ok1 and conv.role == "none" and not conv.preselected and sorted(roleset.by_role) == sorted(rs.ROLES),
          "default=%s; after clear role=%s" % (roleset.default, conv.role))

    # RC-02 seeding
    app = fresh(tmp, "appdata")
    store = rs.GuidanceStore(bundled, app, "app-fixture-1")
    first, second = store.seed(), store.seed()
    check("RC-02 seed copies five files once, never overwrites",
          len(first) == 5 and second == [] and all(store.state(p) == "default" for p in rs.GUIDANCE_FILES),
          "first=%d second=%d" % (len(first), len(second)))

    # RC-03 composition per role, additive, verifiable
    sup = rs.SupplierDouble()
    child_dir = os.path.join(app, "child-roles")
    allok, detail, by_role = True, [], {}
    for role in rs.ROLES:
        rec, composed = rs.start(sup, "conv-%s" % role, store, roleset, role, child_dir=child_dir)
        by_role[role] = rec
        parts = rec["carried"]["developerInstructions"]["parts"]
        role_file = open(os.path.join(store.root, roleset.by_role[role]["guidance"]), "rb").read()
        sent = sup.sent[-1][1]
        ok = (rec["outcome"] == "supplied" and [p["kind"] for p in parts] == ["product-guidance", "role-guidance"]
              and composed[parts[1]["offset"]:parts[1]["offset"] + parts[1]["length"]] == role_file
              and not rs.verify_composition(composed, parts, rec["carried"]["developerInstructions"]["content"])
              and "baseInstructions" not in sent and not errors(rec, SUPPLY_SCHEMA))
        allok &= ok
        detail.append("%s:%dB" % (role, len(composed)))
    check("RC-03 each role composed at thread/start as product guidance + role, parts recomputable, no baseInstructions, record valid",
          allok, " ".join(detail))

    # RC-04 untyped
    rec, composed = rs.start(sup, "conv-none", store, roleset, "none")
    parts = rec["carried"]["developerInstructions"]["parts"]
    check("RC-04 untyped conversation: product guidance only, record valid",
          [p["kind"] for p in parts] == ["product-guidance"] and not errors(rec, SUPPLY_SCHEMA))

    # RC-05 no workflow part (R19-1, R19-7)
    params = list(inspect.signature(rs.compose).parameters)
    check("RC-05 role supply composes no workflow: compose(store, roleset, role) only; a workflow part is refused by the schema (IS-8)",
          params == ["store", "roleset", "role"], "compose%s" % tuple(params).__repr__())

    # RC-06 fork keeps the source's role (OBS-3 W-6; R19-8)
    src = by_role["WORKING_ITEMS"]
    n_before = len(sup.sent)
    frk = rs.fork(sup, src)
    sent_m, sent_p = sup.sent[-1]
    check("RC-06 fork sends no instructions, keeps the source's guidance, records 'inherited' with inheritedFrom; valid",
          sent_m == "thread/fork" and set(sent_p) == {"threadId"} and frk["outcome"] == "inherited"
          and frk["inheritedFrom"] == src["supplyId"] and frk["selection"]["role"] == "WORKING_ITEMS"
          and sup.in_force[frk["thread"]] == sup.in_force[src["thread"]] and len(sup.sent) == n_before + 1
          and not errors(frk, SUPPLY_SCHEMA), "fork=%s forkedFrom=%s" % (frk["thread"], frk["supplierReported"]["forkedFromId"]))

    # RC-07 relaunch: resume without instructions, no new supply
    c = rs.Conversation(roleset, role="TASK", preselected=False)
    c.on("send"); c.on("ok")
    rs.resume(sup, by_role["TASK"]["thread"])
    c.on("relaunch")
    m, p = sup.sent[-1]
    refused = 0
    for meth in ("thread/resume", "thread/fork"):
        try:
            rs.check_request({"threadId": "t", "developerInstructions": "x"}, meth)
        except rs.SupplyRefused:
            refused += 1
    check("RC-07 relaunch resumes with threadId only (instructions on resume/fork are refused by the check: ignored at 0.158.0, OBS-2 O-5); state stays 'supplied'",
          m == "thread/resume" and set(p) == {"threadId"} and c.state == "supplied" and refused == 2)

    # RC-08 missing role file; restore
    os.remove(os.path.join(store.root, "agents/AGENT_HELPS_HUMANS.md"))
    rec, _ = rs.start(sup, "conv-miss", store, roleset, "HELPS_HUMANS", child_dir=child_dir)
    st = store.state("agents/AGENT_HELPS_HUMANS.md")
    store.restore("agents/AGENT_HELPS_HUMANS.md")
    rec2, _ = rs.start(sup, "conv-miss", store, roleset, "HELPS_HUMANS", child_dir=child_dir)
    check("RC-08 missing role file refuses supply (no silent fallback); restore default, then supplied",
          rec.get("refusal") == "guidance-file-missing" and st == "missing" and rec2["outcome"] == "supplied"
          and not errors(rec, SUPPLY_SCHEMA))

    # RC-09 non-UTF-8 guidance
    p9 = os.path.join(store.root, "agents/AGENT_WORKING_ITEMS.md")
    with open(p9, "wb") as fh:
        fh.write(b"\xff\xfe invented bytes")
    rec, _ = rs.start(sup, "conv-utf", store, roleset, "WORKING_ITEMS", child_dir=child_dir)
    store.restore("agents/AGENT_WORKING_ITEMS.md")
    check("RC-09 guidance that is not UTF-8 text is refused 'guidance-not-utf8'", rec.get("refusal") == "guidance-not-utf8")

    # RC-10 modified TASK guidance: limit standing becomes unknown
    tp = os.path.join(store.root, "agents/AGENT_TASK.md")
    with open(tp, "ab") as fh:
        fh.write(b"\nAn invented local edit.\n")
    acc_mod = rs.limit_account(store, roleset, "app-fixture-1")
    task = [r for r in acc_mod["roles"] if r["role"] == "TASK"][0]
    rec_mod, _ = rs.start(sup, "conv-mod", store, roleset, "TASK", child_dir=child_dir)
    check("RC-10 edited TASK guidance: a new conversation is supplied it as 'modified'; L-TASK-1 standing 'unknown'; both valid",
          task["guidanceState"] == "modified" and task["limits"][0]["standing"] == "unknown"
          and rec_mod["carried"]["developerInstructions"]["parts"][1]["source"]["state"] == "modified"
          and not errors(acc_mod, LIMIT_SCHEMA) and not errors(rec_mod, SUPPLY_SCHEMA))
    store.restore("agents/AGENT_TASK.md")

    # RC-11 forbidden request inputs
    bad = []
    for extra in ({"baseInstructions": "x"}, {"sandbox": "read-only"}, {"personality": "friendly"},
                  {"config": {"features.multi_agent": False}}, {"config": {"agents.max_depth": 1}},
                  {"config": {"developer_instructions": "x"}}):
        try:
            rs.check_request(dict({"developerInstructions": "x"}, **extra))
            bad.append(extra)
        except rs.SupplyRefused as e:
            if e.reason != "forbidden-input-in-request":
                bad.append(extra)
    check("RC-11 role supply never sets baseInstructions, personality, approval, sandbox, features.*, agents.max_depth or config instructions",
          not bad, "not refused: %r" % bad if bad else "6 of 6 refused")

    # RC-12 native child roles, additive only; the file carries product guidance + role
    cfg, entries = rs.child_roles(store, roleset, "HELP_HUMAN", {"TASK"}, os.path.join(app, "child2"))
    by = {e["role"]: e for e in entries}
    keys_ok = all(k.split(".")[0] == "agents" and k.split(".")[2] in ("description", "config_file") for k in cfg)
    agents_bytes = open(os.path.join(store.root, "AGENTS.md"), "rb").read()
    full = all(e["_text"].startswith(agents_bytes) for e in entries if e["status"] == "supplied")
    again, _ = rs.child_roles(store, roleset, "HELP_HUMAN", {"TASK"}, os.path.join(app, "child2"))
    f = cfg["agents.WORKING_ITEMS.config_file"]
    with open(f, "ab") as fh:
        fh.write(b"# altered\n")
    try:
        rs.child_roles(store, roleset, "HELP_HUMAN", {"TASK"}, os.path.join(app, "child2"))
        altered_refused = False
    except rs.SupplyRefused:
        altered_refused = True
    cfg_none, ent_none = rs.child_roles(store, roleset, "WORKING_ITEMS", None, os.path.join(app, "child3"))
    check("RC-12 child roles: offered set only; each file = product guidance + role (it replaces the parent's, O-4a); user-defined TASK kept; config unread -> none; content-named files reused; altered file refused; no features/max_depth keys",
          by["TASK"]["reason"] == "user-configuration-defines-role" and by["HELPS_HUMANS"]["status"] == "supplied"
          and by["HELP_HUMAN"]["reason"] == "not-offered-by-role" and keys_ok and full and again == cfg and altered_refused
          and cfg_none == {} and [e["reason"] for e in ent_none if e["role"] == "TASK"] == ["user-configuration-not-read"],
          "keys=%d" % len(cfg))

    # RC-13 default limit account
    acc = rs.limit_account(store, roleset, "app-fixture-1")
    t = [r for r in acc["roles"] if r["role"] == "TASK"][0]["limits"][0]
    check("RC-13 default limit account: TASK 'Stated, not enforced'; valid",
          t["standing"] == "stated-not-enforced" and t["presentedAs"] == "Stated, not enforced" and not errors(acc, LIMIT_SCHEMA))

    # RC-14 children and delegation observations (no thread/started for a child; OBS-2 O-4)
    notes = [json.loads(l) for l in open(os.path.join(FIX, "items", "task-delegation.jsonl")) if l.strip()]
    kids = rs.children(notes)
    inforce = rs.role_in_force({"thr-task-1": "TASK", "thr-wi-1": "WORKING_ITEMS"}, kids,
                               {"thr-child-3": "TASK", "thr-child-7": "default", "thr-child-9": None},
                               {"thr-wi-1": {"TASK"}})
    obs = rs.observe(notes, inforce, {"thr-task-1": by_role["TASK"]["supplyId"]})
    acc["observations"] = obs
    got = sorted((o["item"]["id"], o["roleBasis"]) for o in obs)
    check("RC-14 children found from completed spawnAgent receivers; a task agent's spawn recorded once; a TASK child (agentRole read, role supplied) recorded; a 'default'-type child's spawn not attributed; valid",
          sorted(kids) == ["thr-child-3", "thr-child-4", "thr-child-7", "thr-child-8", "thr-child-9"]
          and got == [("call-1", "supplied-to-thread"), ("call-3", "native-child-role-reported")]
          and "thr-child-7" not in inforce and not errors(acc, LIMIT_SCHEMA), "observations=%s" % got)

    # RC-15 role fixed for the conversation's life; "Continue as <role>"
    c = rs.Conversation(roleset)
    c.on("select", role="WORKING_ITEMS"); c.on("send")
    rec_a, _ = rs.start(sup, "conv-c", store, roleset, c.role, child_dir=child_dir)
    c.on("ok")
    try:
        c.on("select", role="TASK"); fixed = False
    except rs.IllegalTransition:
        fixed = True
    n_before = len(sup.sent)
    nc = c.continue_as(roleset, "TASK", "Invented handoff summary: the task is X; done so far Y.")
    unsent = len(sup.sent) == n_before and nc.state == "draft" and nc.prefill.startswith("Invented handoff")
    nc.on("send")
    rec_b, _ = rs.start(sup, "conv-c2", store, roleset, nc.role, child_dir=child_dir,
                        continued_from={"thread": rec_a["thread"], "supplyRef": rec_a["supplyId"]})
    nc.on("ok")
    check("RC-15 a supplied conversation's role cannot change; 'Continue as TASK' opens a new conversation with the summary pre-filled and unsent; its start records continuedFrom; valid",
          fixed and unsent and c.role == "WORKING_ITEMS" and nc.role == "TASK" and rec_b["continuedFrom"]["supplyRef"] == rec_a["supplyId"]
          and not errors(rec_b, SUPPLY_SCHEMA))

    # RC-16 guidance edited after a conversation started
    with open(os.path.join(store.root, "agents/AGENT_WORKING_ITEMS.md"), "ab") as fh:
        fh.write(b"\nAn invented edit after the conversation started.\n")
    changed = rs.changed_since_start(store, roleset, rec_a)
    c.on("guidance-changed", parts=changed)
    rec_new, _ = rs.start(sup, "conv-new", store, roleset, "WORKING_ITEMS", child_dir=child_dir)
    new_role_part = rec_new["carried"]["developerInstructions"]["parts"][1]
    old_role_part = rec_a["carried"]["developerInstructions"]["parts"][1]
    store.restore("agents/AGENT_WORKING_ITEMS.md")
    check("RC-16 an edit does not reach an open conversation: it shows 'guidance changed since this conversation started' naming the file; a new conversation gets the edit",
          changed == ["agents/AGENT_WORKING_ITEMS.md"] and c.state == "supplied" and c.guidance_changed == changed
          and new_role_part["content"] != old_role_part["content"] and new_role_part["source"]["state"] == "modified")

    # RC-17 no response at start
    rec_u, _ = rs.start(rs.SupplierDouble(mode="no-response"), "conv-u", store, roleset, "TASK", child_dir=child_dir)
    c3 = rs.Conversation(roleset); c3.on("send"); c3.on("no-response")
    check("RC-17 no response to thread/start: outcome 'unknown-no-response', state 'start-unknown'; valid",
          rec_u["outcome"] == "unknown-no-response" and c3.state == "start-unknown" and not errors(rec_u, SUPPLY_SCHEMA))

    # RC-18 release upgrade
    newb = os.path.join(tmp, "bundled-2")
    shutil.copytree(bundled, newb)
    for rel in ("AGENTS.md", "agents/AGENT_TASK.md"):
        with open(os.path.join(newb, rel), "ab") as fh:
            fh.write(b"\nInvented release-2 default text.\n")
    with open(os.path.join(store.root, "AGENTS.md"), "ab") as fh:
        fh.write(b"\nThe person's own edit.\n")
    acts = dict(store.upgrade(newb, "app-fixture-2"))
    check("RC-18 new release: unmodified TASK copy takes the new default (new conversations only); the person's edited AGENTS.md is kept and flagged",
          acts["agents/AGENT_TASK.md"] == "release-default-applied" and acts["AGENTS.md"].startswith("kept-modified")
          and acts["agents/AGENT_HELP_HUMAN.md"] == "unchanged-default", json.dumps(acts, sort_keys=True))

    # RC-19 illegal transitions
    c4 = rs.Conversation(roleset); c4.on("send")
    try:
        c4.on("send"); illegal = False
    except rs.IllegalTransition:
        illegal = True
    check("RC-19 no second message while the start is in flight (illegal transition refused)", illegal)

    # Examples
    valid_supply = by_role["WORKING_ITEMS"]
    acc_valid = acc
    inv_supply = []

    def mut(base, case, expect, fn):
        inst = copy.deepcopy(base)
        fn(inst)
        return {"case": case, "expect": expect, "instance": inst}

    def parts_of(i):
        return i["carried"]["developerInstructions"]["parts"]

    inv_supply.append(mut(valid_supply, "IS-1 baseInstructions carried", "not-set",
                          lambda i: i["carried"].__setitem__("baseInstructions", "replacement base text")))
    inv_supply.append(mut(valid_supply, "IS-2 refused supply that claims carried content", "matches a 'not' schema",
                          lambda i: i.update({"outcome": "refused-before-send", "refusal": "guidance-file-missing"})))
    inv_supply.append(mut(valid_supply, "IS-3 untyped conversation with a role part", "matches a 'not' schema",
                          lambda i: i["selection"].__setitem__("role", "none")))
    inv_supply.append(mut(valid_supply, "IS-4 adoption claimed", "is not const 'unknown'",
                          lambda i: i.__setitem__("adoption", "adopted")))
    inv_supply.append(mut(valid_supply, "IS-5 fork that claims to carry new guidance", "matches a 'not' schema",
                          lambda i: i.update({"trigger": "fork", "request": {"method": "thread/fork"}, "outcome": "inherited",
                                              "inheritedFrom": "sup:0001"})))

    def bad_child(i):
        i["carried"]["nativeChildRoles"].append({"role": "TASK", "status": "supplied", "configKeys": ["features.multi_agent"],
                                                 "composed": i["carried"]["developerInstructions"]["content"],
                                                 "file": i["carried"]["developerInstructions"]["content"]})
    inv_supply.append(mut(valid_supply, "IS-6 child-role entry that sets a features key", "does not match", bad_child))
    inv_supply.append(mut(valid_supply, "IS-7 a fifth role", "not in enum",
                          lambda i: i["selection"].__setitem__("role", "SWB_PIPING_DESIGNER")))
    inv_supply.append(mut(valid_supply, "IS-8 a workflow part in role supply (R19-7)", "'workflow' not in enum",
                          lambda i: parts_of(i).append(dict(parts_of(i)[0], kind="workflow"))))
    inv_supply.append(mut(valid_supply, "IS-9 role guidance sent on thread/resume", "'thread/resume' not in enum",
                          lambda i: i["request"].__setitem__("method", "thread/resume")))

    inv_limit = []

    def task_limits(i):
        return [r for r in i["roles"] if r["role"] == "TASK"][0]

    inv_limit.append(mut(acc_valid, "IL-1 TASK limit claimed enforced without a mechanism", "required mechanism missing",
                         lambda i: task_limits(i)["limits"][0].update({"standing": "enforced-by-supplier", "presentedAs": "Enforced by Codex"})))
    inv_limit.append(mut(acc_valid, "IL-2 modified guidance still presented as stating the limit", "matches a 'not' schema",
                         lambda i: task_limits(i).__setitem__("guidanceState", "modified")))
    inv_limit.append(mut(acc_valid, "IL-3 observation attributed to a role that may delegate", "is not const 'TASK'",
                         lambda i: i["observations"][0].__setitem__("roleInForce", "WORKING_ITEMS")))
    inv_limit.append(mut(acc_valid, "IL-4 TASK marked as may-delegate", "is not const 'does-not-delegate'",
                         lambda i: task_limits(i).__setitem__("delegation", "may-delegate")))
    inv_limit.append(mut(acc_valid, "IL-5 three roles only", "fewer than 4 items",
                         lambda i: i.__setitem__("roles", i["roles"][:3])))
    inv_limit.append(mut(acc_valid, "IL-6 a child's role inferred from its parent (R18-4)", "not in enum",
                         lambda i: i["observations"][0].__setitem__("roleBasis", "inherited-from-parent (inference)")))

    paths = {
        "role-supply-record.valid.example.json": valid_supply,
        "role-supply-record.invalid.examples.json": inv_supply,
        "role-limit-account.valid.example.json": acc_valid,
        "role-limit-account.invalid.examples.json": inv_limit,
    }
    if write_examples:
        for name, data in paths.items():
            with open(os.path.join(DESIGN, name), "w", encoding="utf-8") as fh:
                json.dump(data, fh, indent=2, ensure_ascii=False)
                fh.write("\n")
        say("examples written: %s" % ", ".join(sorted(paths)))

    # RC-20 example files against the schemas
    for schema, vname, iname in ((SUPPLY_SCHEMA, "role-supply-record.valid.example.json", "role-supply-record.invalid.examples.json"),
                                 (LIMIT_SCHEMA, "role-limit-account.valid.example.json", "role-limit-account.invalid.examples.json")):
        v = json.load(open(os.path.join(DESIGN, vname)))
        ev = errors(v, schema)
        check("RC-20 %s valid" % vname, not ev, "; ".join(ev[:3]))
        for c in json.load(open(os.path.join(DESIGN, iname))):
            e = errors(c["instance"], schema)
            hit = [x for x in e if c["expect"] in x]
            check("RC-20 %s rejected" % c["case"], bool(e) and bool(hit), (hit or e or ["accepted"])[0])

    say("TOTAL pass=%d fail=%d" % (RESULTS["pass"], RESULTS["fail"]))
    shutil.rmtree(tmp)
    if record:
        rd = os.path.join(HERE, "results")
        os.makedirs(rd, exist_ok=True)
        with open(os.path.join(rd, "run-%s.txt" % datetime.date.today().isoformat()), "w", encoding="utf-8") as fh:
            fh.write("\n".join(OUT) + "\n")
    return 0 if RESULTS["fail"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
