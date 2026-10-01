#!/usr/bin/env python3
"""Run the ROLE-v0.1 prototype cases (ROLE §10). Python 3 standard library only.

    python3 run_cases.py                    # run the cases
    python3 run_cases.py --write-examples   # also (re)write the schema examples beside ROLE_SUPPLY.md

Scratch files go to a fresh folder under $TMPDIR. Nothing is sent anywhere; the
supplier is a test double. Output is also written to results/run-<date>.txt
when --record is given.
"""
import copy
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


def workflow_fixture(tmp, registered=True):
    pkg = os.path.join(tmp, "wf-lib", "demo-check")
    if not os.path.exists(pkg):
        shutil.copytree(os.path.join(FIX, "workflows", "demo-check"), pkg)
    rev = rs.package_revision(pkg)
    return {"tuple": {"kind": "workflow", "origin": "project", "sourceRoot": "project:fixture",
                      "name": "demo-check", "revision": rev},
            "package_dir": pkg, "registered": registered, "runRef": "run:fixture-1"}


def main():
    write_examples = "--write-examples" in sys.argv
    record = "--record" in sys.argv
    tmp = tempfile.mkdtemp(prefix="chirality-d6-role-", dir=os.environ.get("TMPDIR"))
    say("ROLE-v0.1 prototype run %s; python %s; scratch under $TMPDIR (%s)" % (
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
    allok, detail = True, []
    for role in rs.ROLES:
        rec, composed = rs.supply(sup, "thread/start", "conv-%s" % role, store, roleset, role, child_dir=child_dir)
        parts = rec["carried"]["developerInstructions"]["parts"]
        role_file = open(os.path.join(store.root, roleset.by_role[role]["guidance"]), "rb").read()
        sent = sup.sent[-1][1]
        ok = (rec["outcome"] == "supplied" and [p["kind"] for p in parts] == ["product-guidance", "role-guidance"]
              and composed[parts[1]["offset"]:parts[1]["offset"] + parts[1]["length"]] == role_file
              and not rs.verify_composition(composed, parts, rec["carried"]["developerInstructions"]["content"])
              and "baseInstructions" not in sent and not errors(rec, SUPPLY_SCHEMA))
        allok &= ok
        detail.append("%s:%dB" % (role, len(composed)))
    check("RC-03 each role composed as product guidance + role, parts recomputable, no baseInstructions, record valid",
          allok, " ".join(detail))

    # RC-04 untyped
    rec, composed = rs.supply(sup, "thread/start", "conv-none", store, roleset, "none")
    parts = rec["carried"]["developerInstructions"]["parts"]
    check("RC-04 untyped conversation: product guidance only, record valid",
          [p["kind"] for p in parts] == ["product-guidance"] and not errors(rec, SUPPLY_SCHEMA))

    # RC-05 workflow composed (registered revision)
    wf = workflow_fixture(tmp)
    rec_wf, composed_wf = rs.supply(sup, "thread/start", "conv-wf", store, roleset, "TASK", workflow=wf, child_dir=child_dir)
    kinds = [p["kind"] for p in rec_wf["carried"]["developerInstructions"]["parts"]]
    check("RC-05 workflow entrypoint composed third, revision verified, record valid",
          kinds == ["product-guidance", "role-guidance", "workflow"] and not errors(rec_wf, SUPPLY_SCHEMA),
          "parts=%s" % kinds)

    # RC-06 revision mismatch
    with open(os.path.join(wf["package_dir"], "WORKFLOW.md"), "ab") as fh:
        fh.write(b"\nEdited after selection.\n")
    rec, _ = rs.supply(sup, "thread/start", "conv-wf2", store, roleset, "TASK", workflow=wf, child_dir=child_dir)
    check("RC-06 workflow bytes changed after selection: refused 'revision-not-verified', nothing sent",
          rec["outcome"] == "refused-before-send" and rec["refusal"] == "revision-not-verified" and not errors(rec, SUPPLY_SCHEMA))

    # RC-07 draft workflow (K-7)
    wf2 = dict(workflow_fixture(fresh(tmp, "wf2")), registered=False)
    rec, _ = rs.supply(sup, "thread/start", "conv-draft", store, roleset, "WORKING_ITEMS", workflow=wf2, child_dir=child_dir)
    check("RC-07 a draft is never supplied as a workflow (K-7): 'workflow-not-registered'",
          rec["outcome"] == "refused-before-send" and rec["refusal"] == "workflow-not-registered")

    # RC-08 missing role file; restore
    os.remove(os.path.join(store.root, "agents/AGENT_HELPS_HUMANS.md"))
    rec, _ = rs.supply(sup, "thread/start", "conv-miss", store, roleset, "HELPS_HUMANS", child_dir=child_dir)
    st = store.state("agents/AGENT_HELPS_HUMANS.md")
    store.restore("agents/AGENT_HELPS_HUMANS.md")
    rec2, _ = rs.supply(sup, "thread/start", "conv-miss", store, roleset, "HELPS_HUMANS", child_dir=child_dir)
    check("RC-08 missing role file refuses supply (no silent fallback); restore default, then supplied",
          rec.get("refusal") == "guidance-file-missing" and st == "missing" and rec2["outcome"] == "supplied")

    # RC-09 non-UTF-8 guidance
    p = os.path.join(store.root, "agents/AGENT_WORKING_ITEMS.md")
    with open(p, "wb") as fh:
        fh.write(b"\xff\xfe invented bytes")
    rec, _ = rs.supply(sup, "thread/start", "conv-utf", store, roleset, "WORKING_ITEMS", child_dir=child_dir)
    store.restore("agents/AGENT_WORKING_ITEMS.md")
    check("RC-09 guidance that is not UTF-8 text is refused 'guidance-not-utf8'", rec.get("refusal") == "guidance-not-utf8")

    # RC-10 modified TASK guidance: limit standing becomes unknown
    tp = os.path.join(store.root, "agents/AGENT_TASK.md")
    with open(tp, "ab") as fh:
        fh.write(b"\nAn invented local edit.\n")
    acc_mod = rs.limit_account(store, roleset, "app-fixture-1")
    task = [r for r in acc_mod["roles"] if r["role"] == "TASK"][0]
    rec_mod, _ = rs.supply(sup, "thread/start", "conv-mod", store, roleset, "TASK", child_dir=child_dir)
    check("RC-10 edited TASK guidance: supplied as 'modified'; L-TASK-1 standing 'unknown'; both valid",
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

    # RC-12 native child roles, additive only
    cfg, entries = rs.child_roles(store, roleset, "HELP_HUMAN", {"TASK"}, os.path.join(app, "child2"))
    by = {e["role"]: e for e in entries}
    keys_ok = all(k.split(".")[0] == "agents" and k.split(".")[2] in ("description", "config_file") for k in cfg)
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
    check("RC-12 child roles: offered set only; user-defined TASK kept (not supplied); config unread -> none supplied; content-named files reused; altered file refused; no features/max_depth keys",
          by["TASK"]["reason"] == "user-configuration-defines-role" and by["HELPS_HUMANS"]["status"] == "supplied"
          and by["HELP_HUMAN"]["reason"] == "not-offered-by-role" and keys_ok and again == cfg and altered_refused
          and cfg_none == {} and [e["reason"] for e in ent_none if e["role"] == "TASK"] == ["user-configuration-not-read"],
          "keys=%d" % len(cfg))

    # RC-13 default limit account
    acc = rs.limit_account(store, roleset, "app-fixture-1")
    t = [r for r in acc["roles"] if r["role"] == "TASK"][0]["limits"][0]
    check("RC-13 default limit account: TASK 'Stated, not enforced'; valid",
          t["standing"] == "stated-not-enforced" and t["presentedAs"] == "Stated, not enforced" and not errors(acc, LIMIT_SCHEMA))

    # RC-14 delegation observation
    notes = [json.loads(l) for l in open(os.path.join(FIX, "items", "task-delegation.jsonl")) if l.strip()]
    obs = rs.observe(notes, {"thr-task-1": ("TASK", "supplied-to-thread"), "thr-wi-1": ("WORKING_ITEMS", "supplied-to-thread")},
                     {"thr-task-1": rec_wf["supplyId"]})
    acc["observations"] = obs
    check("RC-14 a task agent's spawnAgent is recorded once (started+completed), a manager's is not; nothing prevented; valid",
          len(obs) == 1 and obs[0]["thread"] == "thr-task-1" and not errors(acc, LIMIT_SCHEMA), "observations=%d" % len(obs))

    # RC-15 role change at the idle point (route A: resume overrides adopted; OBS-2 O-5 pending)
    c = rs.Conversation(roleset)
    c.on("select", role="WORKING_ITEMS")
    c.on("send")
    rec_a, _ = rs.supply(sup, "thread/start", "conv-c", store, roleset, c.role, child_dir=child_dir)
    c.on("ok")
    c.on("select", role="TASK")           # pending, nothing sent
    pending_state, sent_before = c.state, len(sup.sent)
    c.on("send")                          # the person's next message at an idle point
    rec_b, _ = rs.supply(sup, "thread/resume", rec_a["thread"], store, roleset, c.pending, trigger="idle-change",
                         change_cause=["role-selected"], previous=rec_a["supplyId"], child_dir=child_dir)
    c.on("ok")
    check("RC-15 role change waits as 'change-pending' (nothing sent), applies by thread/resume before the next turn; record valid",
          pending_state == "change-pending" and sent_before == len(sup.sent) - 1 and c.state == "supplied" and c.role == "TASK"
          and rec_b["request"]["method"] == "thread/resume" and not errors(rec_b, SUPPLY_SCHEMA),
          "trace=%s" % " > ".join(s for _, s, _ in c.trace))

    # RC-16 route B (resume overrides not adopted on a loaded thread; OBS-2 O-5 pending)
    c2 = rs.Conversation(roleset)
    c2.on("send"); c2.on("ok"); c2.on("select", role="TASK"); c2.on("send"); c2.on("ok-not-adopted-route")
    offered = sorted(rs.T2["change-not-applied"])
    check("RC-16 if O-5 shows resume overrides are not taken up, the change is shown 'not applied' with explicit choices",
          c2.state == "change-not-applied" and c2.role == "HELP_HUMAN" and "new-conversation" in offered and "send-anyway" in offered,
          "offered=%s" % offered)

    # RC-17 no response at start
    rec_u, _ = rs.supply(rs.SupplierDouble(mode="no-response"), "thread/start", "conv-u", store, roleset, "TASK", child_dir=child_dir)
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
    check("RC-18 new release: unmodified TASK copy takes the new default; the person's edited AGENTS.md is kept and flagged",
          acts["agents/AGENT_TASK.md"] == "release-default-applied" and acts["AGENTS.md"].startswith("kept-modified")
          and acts["agents/AGENT_HELP_HUMAN.md"] == "unchanged-default", json.dumps(acts, sort_keys=True))

    # RC-19 illegal transitions
    c4 = rs.Conversation(roleset); c4.on("send"); c4.on("ok"); c4.on("select", role="TASK"); c4.on("send")
    try:
        c4.on("send"); illegal = False
    except rs.IllegalTransition:
        illegal = True
    check("RC-19 no second turn while a re-supply is in flight (illegal transition refused)", illegal)

    # Examples
    valid_supply = rec_wf
    acc_valid = acc
    inv_supply = []

    def mut(base, case, expect, fn):
        inst = copy.deepcopy(base)
        fn(inst)
        return {"case": case, "expect": expect, "instance": inst}

    inv_supply.append(mut(valid_supply, "IS-1 baseInstructions carried", "not-set",
                          lambda i: i["carried"].__setitem__("baseInstructions", "replacement base text")))
    inv_supply.append(mut(valid_supply, "IS-2 refused supply that claims carried content", "matches a 'not' schema",
                          lambda i: i.update({"outcome": "refused-before-send", "refusal": "revision-not-verified"})))
    inv_supply.append(mut(valid_supply, "IS-3 untyped conversation with a role part", "matches a 'not' schema",
                          lambda i: i["selection"].__setitem__("role", "none")))
    inv_supply.append(mut(valid_supply, "IS-4 adoption claimed", "is not const 'unknown'",
                          lambda i: i.__setitem__("adoption", "adopted")))
    inv_supply.append(mut(valid_supply, "IS-5 idle change sent as thread/start without previous supply", "required previousSupply missing",
                          lambda i: i.update({"trigger": "idle-change", "changeCause": ["role-selected"]})))

    def bad_child(i):
        e = [x for x in i["carried"]["nativeChildRoles"] if x["status"] == "supplied"]
        i["carried"]["nativeChildRoles"].append({"role": "TASK", "status": "supplied", "configKeys": ["features.multi_agent"],
                                                 "composed": i["carried"]["developerInstructions"]["content"],
                                                 "file": i["carried"]["developerInstructions"]["content"]})
    inv_supply.append(mut(valid_supply, "IS-6 child-role entry that sets a features key", "does not match", bad_child))
    inv_supply.append(mut(valid_supply, "IS-7 a fifth role", "not in enum",
                          lambda i: i["selection"].__setitem__("role", "SWB_PIPING_DESIGNER")))

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
