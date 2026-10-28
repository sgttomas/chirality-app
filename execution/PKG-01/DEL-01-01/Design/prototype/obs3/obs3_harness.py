#!/usr/bin/env python3
"""OBS-3 observation harness: per-turn workflow supply, chaining and fork at Codex 0.158.0.

Prototype only (DEL-01-01, run APP-V4-DESIGN-PASS-3-20261001, node OBS-3). Not product code;
not an App candidate; nothing here is qualified. Python 3 standard library only. Scope:
R19_RESOLUTIONS.md R19-6 and BRIEFS.md "OBS-3" items W-1...W-6.

It reuses the OBS-2 harness (../obs2/obs2_harness.py) unchanged: its Run (scratch folders, S-9
memory-pressure and S-2 download watch), Session (one `codex app-server` over stdio with frame
log, process and socket snapshots, S-1/S-3/S-5/S-6 checks), the refusal policy for supplier
requests, thread_start and wait_turn_completed. The provider path is obs3_provider_tap.py on
127.0.0.1:12350, a pass-through recorder in front of LM Studio that becomes capture-only (HTTP
400, no model call) while the flag file <obs>/logs/capture.flag exists.

Hard limits honoured by construction (as OBS-2): scratch CODEX_HOMEs under the OBS folder only
(never ~/.codex); no sign-in request answered; no key or token anywhere; the only provider is the
loopback tap in front of the local LM Studio server; every text sent to the model is invented.
Every home sets `[features] plugins = false`, which OBS-2 O-7 found stops both start-up
connections (featured plugins, plugin repository), so no plugin cache is needed.

Scenarios:
  capture  W-1/W-3/W-4 input shapes, capture-only (no model call): skill input with WORKFLOW.md,
           SKILL.md outside any root, a folder, a wrong name, a missing file, no text item;
           mention input; plain text; skills installed in a discovered root and in an extra root
           set by skills/extraRoots/set.
  capture2 the same with canonical (realpath) paths, an installed skill, an extra root holding SKILL.md, an
           extra root holding only WORKFLOW.md, a `$name` text mention, a wrong name, a skill-only input.
  supp     capture-only supplements: W-2b (recorded injection bytes replayed after the file changes and the
           supplier restarts; extra roots not kept across a restart) and W-6b (fork with
           config.developer_instructions; fork then thread/settings/update).
  w12      W-1 then W-2 on one thread with real predictions (skills in an App-set extra root, route
           `extraroot`, the default): run A started by a skill input, a
           follow-up turn, run B started by a skill input with a line saying run A ended, a
           follow-up turn; thread/read and thread/turns/list.
  w34      W-3 (mention, real) and W-4 (B's bytes as plain text, real), each on its own thread.
  w5       W-5 thread/settings/update collaborationMode.settings.developer_instructions = A, then
           B; a turn without update; restart and resume (capture); plan mode interplay (capture).
  w6       W-6 thread/fork with new developerInstructions; fork turn (real); the source's next
           request (capture); a fork with no developerInstructions (capture); fork after restart
           (capture).

Usage:
  obs3_harness.py --obs DIR --binary PATH [--route extraroot|skillmd|workflowmd] SCENARIO
"""
import argparse
import json
import os
import sys
import threading
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "obs2"))
import obs2_harness as H  # noqa: E402  (OBS-2 harness, unchanged)

TAP_PORT = 12350

WF = {
    "A": ("obs3-workflow-a",
          "---\n"
          "name: obs3-workflow-a\n"
          "description: Invented workflow A for the OBS-3 observation (test material only).\n"
          "---\n"
          "# Workflow A (invented, OBS-3)\n\n"
          "This is invented test material. While workflow A is in force:\n\n"
          "- Begin every reply with the exact text [WF-A] followed by a space.\n"
          "- Keep each reply to one short sentence after that marker.\n"),
    "B": ("obs3-workflow-b",
          "---\n"
          "name: obs3-workflow-b\n"
          "description: Invented workflow B for the OBS-3 observation (test material only).\n"
          "---\n"
          "# Workflow B (invented, OBS-3)\n\n"
          "This is invented test material. While workflow B is in force:\n\n"
          "- Begin every reply with the exact text [WF-B] followed by a space.\n"
          "- Keep each reply to one short sentence after that marker.\n"),
}
ROLE_DEV = ("You are running an observation test with invented data. Invented role guidance: you are the "
            "OBS3 HELPER role. Answer briefly.")
ROLE_ONE = ("You are running an observation test with invented data. Invented role line: you are OBS3 ROLE ONE. "
            "End every reply with the word ROLEONE.")
ROLE_TWO = ("You are running an observation test with invented data. Invented role line: you are OBS3 ROLE TWO. "
            "End every reply with the word ROLETWO.")
MARKERS = ["[WF-A]", "[WF-B]", "obs3-workflow-a", "obs3-workflow-b", "Workflow A (invented", "Workflow B (invented",
           "OBS3 HELPER", "ROLE ONE", "ROLE TWO", "Plan Mode", "<skill>", "<collaboration_mode>",
           "run A", "Run A"]


# ---------------- packages ----------------

def write_packages(run):
    """Invented workflow packages A and B: WORKFLOW.md as is, and a SKILL.md-shaped copy (same bytes)."""
    p = {}
    for key, (name, text) in WF.items():
        wdir = os.path.join(run.obs, "pkgs", "workflows", name)
        sdir = os.path.join(run.obs, "pkgs", "skill-copies", name)
        for d, fn in ((wdir, "WORKFLOW.md"), (sdir, "SKILL.md")):
            os.makedirs(d, exist_ok=True)
            with open(os.path.join(d, fn), "w", encoding="utf-8") as f:
                f.write(text)
        p[key] = {"name": name, "workflow_md": os.path.join(wdir, "WORKFLOW.md"),
                  "skill_md": os.path.join(sdir, "SKILL.md"), "skill_dir": sdir, "text": text}
    return p


def config(run):
    return H.provider_config(run.a.model, run.a.ctx) + "\n[features]\nplugins = false\n"


# ---------------- tap helpers ----------------

def tap_log(run):
    return os.path.join(run.logroot, "provider_tap.jsonl")


def flag_path(run):
    return os.path.join(run.logroot, "capture.flag")


def set_capture(run, on):
    fp = flag_path(run)
    if on:
        open(fp, "w").close()
    elif os.path.exists(fp):
        os.remove(fp)


def tap_mark(run):
    try:
        with open(tap_log(run), "r", encoding="utf-8") as f:
            return sum(1 for _ in f)
    except OSError:
        return 0


def tap_since(run, mark):
    try:
        with open(tap_log(run), "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    except OSError:
        return []
    out = []
    for line in lines[mark:]:
        try:
            out.append(json.loads(line))
        except ValueError:
            pass
    return out


def _texts(content):
    if isinstance(content, str):
        return [content]
    out = []
    for c in content or []:
        if isinstance(c, dict):
            out.append(c.get("text") or c.get("output") or json.dumps(c)[:400])
    return out


def summarize_input(body, cut=3000):
    """Model input of one provider request: one row per input item (role, type, texts cut)."""
    rows = []
    for i, it in enumerate((body or {}).get("input") or []):
        typ = it.get("type")
        if typ == "message":
            texts = _texts(it.get("content"))
        elif typ in ("function_call",):
            texts = ["%s(%s)" % (it.get("name"), (it.get("arguments") or "")[:300])]
        elif typ == "function_call_output":
            texts = [str(it.get("output"))[:600]]
        elif typ == "reasoning":
            texts = ["<reasoning %d chars>" % sum(len(t) for t in _texts(it.get("content")))]
        else:
            texts = [json.dumps(it)[:300]]
        rows.append({"i": i, "type": typ, "role": it.get("role"),
                     "texts": [t if len(t) <= cut else t[:cut] + "...<%d chars>" % len(t) for t in texts],
                     "markers": sorted({m for m in MARKERS for t in texts if m in t})})
    return rows


def request_view(rec):
    body = rec.get("body") or {}
    return {"wall_ms": rec.get("wall_ms"), "status": rec.get("status"), "capture_only": rec.get("capture_only", False),
            "instructions_chars": len(body.get("instructions") or ""),
            "instructions_markers": sorted({m for m in MARKERS if m in (body.get("instructions") or "")}),
            "tools": [t.get("name") or t.get("type") for t in body.get("tools") or []],
            "input": summarize_input(body)}


# ---------------- turn helper ----------------

def run_turn(s, run, thread_id, inputs, label, capture=False, extra=None, timeout=None):
    """Start one turn with the given input items; return everything observed for it."""
    set_capture(run, capture)
    mark = tap_mark(run)
    idx = len(s.notes)
    params = {"threadId": thread_id, "input": inputs}
    if extra:
        params.update(extra)
    run.turn_active = not capture
    r = s.request("turn/start", params, timeout=60)
    out = {"label": label, "capture_only": capture, "params": params, "turn/start response": r}
    if r is None or "result" not in r:
        run.turn_active = False
        out["accepted"] = False
        set_capture(run, False)
        return out
    out["accepted"] = True
    turn_id = ((r["result"] or {}).get("turn") or {}).get("id")
    out["turn_id"] = turn_id
    done = H.wait_turn_completed(s, run, turn_id, timeout=timeout or (120 if capture else run.a.turn_timeout),
                                 start_index=idx)
    run.turn_active = False
    time.sleep(1.0)
    set_capture(run, False)
    seg = s.notes[idx:]
    tc = (done[2]["params"]["turn"] if done else None)
    out["turn_completed"] = {"status": (tc or {}).get("status"), "error": (tc or {}).get("error")} if tc else None
    out["methods"] = H.method_counts(seg)
    out["items"] = H.items_summary(seg, thread_id)
    out["user_message_items"] = [m["params"]["item"] for _, m in seg if m.get("method") == "item/completed" and
                                 (m["params"].get("item") or {}).get("type") == "userMessage"]
    out["agent_messages"] = [m["params"]["item"].get("text") for _, m in seg if m.get("method") == "item/completed"
                             and (m["params"].get("item") or {}).get("type") == "agentMessage"
                             and (m["params"].get("threadId") in (None, thread_id))]
    out["other_items"] = [{"type": m["params"]["item"].get("type"), "item": m["params"]["item"]}
                          for _, m in seg if m.get("method") == "item/completed" and
                          (m["params"].get("item") or {}).get("type") not in
                          ("userMessage", "agentMessage", "reasoning")]
    out["errors_warnings"] = [m for _, m in seg if m.get("method") in ("error", "warning", "configWarning",
                                                                       "deprecationNotice")]
    out["settings_notes"] = [m.get("params") for _, m in seg if m.get("method") == "thread/settings/updated"]
    out["provider_requests"] = [request_view(rec) for rec in tap_since(run, mark)]
    out["server_requests"] = [m for t, m in s.server_requests if t >= (seg[0][0] if seg else 0)]
    return out


def compliance(text, want, avoid=None):
    t = (text or "").lstrip()
    return {"begins_with_" + want: t.startswith(want), "contains_" + want: want in (text or ""),
            **({"contains_" + avoid: avoid in (text or "")} if avoid else {})}


def text_item(t):
    return {"type": "text", "text": t, "text_elements": []}


def new_session(run, label, home, experimental=True):
    s = H.Session(run, label, home, run.make_cwd(label), policy=H.policy_refuse)
    s.start()
    init = s.initialize(experimental=experimental, name="chirality-obs3")
    return s, init


def read_thread(s, tid, turns=True):
    return s.request("thread/read", {"threadId": tid, "includeTurns": turns})


def thread_read_items(resp):
    """Compact view of thread/read: per turn, the item types and the userMessage content."""
    th = ((resp or {}).get("result") or {}).get("thread") or {}
    out = {"id": th.get("id"), "status": th.get("status"), "parentThreadId": th.get("parentThreadId"),
           "forkedFromId": th.get("forkedFromId"), "source": th.get("source"), "turns": []}
    for tr in th.get("turns") or []:
        row = {"id": tr.get("id"), "status": tr.get("status"), "items": []}
        for it in tr.get("items") or []:
            if it.get("type") == "userMessage":
                row["items"].append({"type": "userMessage", "content": it.get("content")})
            elif it.get("type") == "agentMessage":
                row["items"].append({"type": "agentMessage", "text": (it.get("text") or "")[:300]})
            else:
                row["items"].append({"type": it.get("type")})
        out["turns"].append(row)
    other = {k: v for k, v in th.items() if k not in ("turns", "preview")}
    out["thread_fields"] = other
    return out


def save(run, name, obj):
    H.write_json(os.path.join(run.logroot, name), obj)


# ---------------- scenarios ----------------

def sc_capture(run):
    pk = write_packages(run)
    out = {"packages": {k: {kk: (vv.replace(run.obs, "<OBS>") if isinstance(vv, str) else vv)
                            for kk, vv in v.items()} for k, v in pk.items()}}
    hello = "This is a test with invented data. Starting workflow A (run 1). Say hello in one short sentence."
    A, B = pk["A"], pk["B"]
    # ---- home without any skill root holding the workflows ----
    home = run.make_home("cap-noroot", config(run), warm=False)
    s, init = new_session(run, "cap-noroot", home)
    try:
        if init is None:
            return
        time.sleep(1.5)
        out["noroot_skills/list"] = s.request("skills/list", {"cwds": [s.cwd], "forceReload": True})
        variants = [
            ("c1-skill-WORKFLOW.md", [text_item(hello), {"type": "skill", "name": A["name"], "path": A["workflow_md"]}]),
            ("c2-skill-SKILL.md-outside-roots", [text_item(hello), {"type": "skill", "name": A["name"], "path": A["skill_md"]}]),
            ("c3-skill-folder", [text_item(hello), {"type": "skill", "name": A["name"], "path": A["skill_dir"]}]),
            ("c4-skill-wrong-name", [text_item(hello), {"type": "skill", "name": "obs3-not-the-name", "path": A["skill_md"]}]),
            ("c5-skill-missing-file", [text_item(hello), {"type": "skill", "name": A["name"],
                                                         "path": os.path.join(run.obs, "pkgs", "missing", "SKILL.md")}]),
            ("c6-skill-only-no-text", [{"type": "skill", "name": A["name"], "path": A["skill_md"]}]),
            ("c7-mention-WORKFLOW.md", [text_item(hello), {"type": "mention", "name": A["name"], "path": A["workflow_md"]}]),
            ("c8-mention-SKILL.md", [text_item(hello), {"type": "mention", "name": A["name"], "path": A["skill_md"]}]),
            ("c9-text-bytes-B", [text_item("This is a test with invented data. Starting workflow B (run 1). The "
                                           "workflow follows.\n\n" + B["text"] + "\nSay hello in one short sentence.")]),
        ]
        for label, inputs in variants:
            if run.stop_reason:
                break
            th = H.thread_start(s, run, ROLE_DEV)
            if th is None:
                break
            tid = th["thread"]["id"]
            res = run_turn(s, run, tid, inputs, label, capture=True)
            res["thread/read"] = thread_read_items(read_thread(s, tid))
            out[label] = res
    finally:
        run.turn_active = False
        set_capture(run, False)
        out["noroot_exit"] = s.stop("stdin")
    if run.stop_reason:
        save(run, "capture_result.json", out)
        return
    # ---- home with A installed in the home's user skill root, B in an extra root ----
    home2 = run.make_home("cap-root", config(run), warm=False)
    sk = os.path.join(home2, "skills", A["name"])
    os.makedirs(sk)
    with open(os.path.join(sk, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(A["text"])
    extra_root = os.path.join(run.obs, "pkgs", "extra-root")
    os.makedirs(os.path.join(extra_root, B["name"]), exist_ok=True)
    with open(os.path.join(extra_root, B["name"], "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(B["text"])
    s, init = new_session(run, "cap-root", home2)
    try:
        if init is None:
            return
        time.sleep(1.5)
        out["root_skills/list_before"] = s.request("skills/list", {"cwds": [s.cwd], "forceReload": True})
        out["root_extraRoots/set"] = s.request("skills/extraRoots/set", {"extraRoots": [extra_root]})
        out["root_skills/list_after"] = s.request("skills/list", {"cwds": [s.cwd], "forceReload": True})
        variants = [
            ("c10-skill-installed-root-A", [text_item(hello), {"type": "skill", "name": A["name"],
                                                               "path": os.path.join(sk, "SKILL.md")}]),
            ("c11-skill-extra-root-B", [text_item(hello.replace("workflow A", "workflow B")),
                                        {"type": "skill", "name": B["name"],
                                         "path": os.path.join(extra_root, B["name"], "SKILL.md")}]),
            ("c12-no-skill-input", [text_item("This is a test with invented data. Say hello in one short sentence.")]),
            ("c13-skill-outside-roots-while-roots-set", [text_item(hello), {"type": "skill", "name": A["name"],
                                                                           "path": A["skill_md"]}]),
        ]
        for label, inputs in variants:
            if run.stop_reason:
                break
            th = H.thread_start(s, run, ROLE_DEV)
            if th is None:
                break
            tid = th["thread"]["id"]
            res = run_turn(s, run, tid, inputs, label, capture=True)
            res["thread/read"] = thread_read_items(read_thread(s, tid))
            out[label] = res
    finally:
        run.turn_active = False
        set_capture(run, False)
        out["root_exit"] = s.stop("stdin")
        save(run, "capture_result.json", out)


def sc_capture2(run):
    """Second capture pass. The first pass gave every path in its /var/folders form while Codex lists skills by
    their canonical /private/var/folders path; here every path is canonical (os.path.realpath)."""
    pk = write_packages(run)
    R = os.path.realpath
    A, B = pk["A"], pk["B"]
    hello = "This is a test with invented data. Starting workflow A (run 1). Say hello in one short sentence."
    out = {}
    home = run.make_home("cap2-noroot", config(run), warm=False)
    s, init = new_session(run, "cap2-noroot", home)
    try:
        if init is None:
            return
        time.sleep(1.5)
        variants = [
            ("r1-skill-WORKFLOW.md-real", [text_item(hello), {"type": "skill", "name": A["name"], "path": R(A["workflow_md"])}]),
            ("r2-skill-SKILL.md-outside-roots-real", [text_item(hello), {"type": "skill", "name": A["name"], "path": R(A["skill_md"])}]),
            ("r3-mention-SKILL.md-real", [text_item(hello), {"type": "mention", "name": A["name"], "path": R(A["skill_md"])}]),
            ("r4-mention-WORKFLOW.md-real", [text_item(hello), {"type": "mention", "name": A["name"], "path": R(A["workflow_md"])}]),
        ]
        for label, inputs in variants:
            if run.stop_reason:
                break
            th = H.thread_start(s, run, ROLE_DEV)
            if th is None:
                break
            tid = th["thread"]["id"]
            res = run_turn(s, run, tid, inputs, label, capture=True)
            res["thread/read"] = thread_read_items(read_thread(s, tid))
            out[label] = res
    finally:
        run.turn_active = False
        set_capture(run, False)
        out["noroot_exit"] = s.stop("stdin")
    if run.stop_reason:
        save(run, "capture2_result.json", out)
        return
    home2 = run.make_home("cap2-root", config(run), warm=False)
    sk = os.path.join(home2, "skills", A["name"])
    os.makedirs(sk)
    with open(os.path.join(sk, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(A["text"])
    extra_root = os.path.join(run.obs, "pkgs", "extra-root")          # B as SKILL.md (from the first pass)
    wf_root = os.path.join(run.obs, "pkgs", "workflow-root")          # B as WORKFLOW.md only
    os.makedirs(os.path.join(wf_root, B["name"]), exist_ok=True)
    with open(os.path.join(wf_root, B["name"], "WORKFLOW.md"), "w", encoding="utf-8") as f:
        f.write(B["text"])
    s, init = new_session(run, "cap2-root", home2)
    try:
        if init is None:
            return
        time.sleep(1.5)
        out["extraRoots/set workflow-root only"] = s.request("skills/extraRoots/set", {"extraRoots": [R(wf_root)]})
        out["skills/list with workflow-root"] = s.request("skills/list", {"cwds": [s.cwd], "forceReload": True})
        out["extraRoots/set extra-root"] = s.request("skills/extraRoots/set", {"extraRoots": [R(extra_root)]})
        out["skills/list with extra-root"] = s.request("skills/list", {"cwds": [s.cwd], "forceReload": True})
        a_inst = R(os.path.join(sk, "SKILL.md"))
        variants = [
            ("r5-skill-installed-A-real", [text_item(hello), {"type": "skill", "name": A["name"], "path": a_inst}]),
            ("r6-skill-extra-root-B-real", [text_item(hello.replace("workflow A", "workflow B")),
                                            {"type": "skill", "name": B["name"],
                                             "path": R(os.path.join(extra_root, B["name"], "SKILL.md"))}]),
            ("r7-text-dollar-mention-A", [text_item("This is a test with invented data. Use $obs3-workflow-a. "
                                                    "Starting workflow A (run 1). Say hello in one short sentence.")]),
            ("r8-skill-installed-A-wrong-name", [text_item(hello), {"type": "skill", "name": "obs3-not-the-name",
                                                                   "path": a_inst}]),
            ("r9-mention-installed-A", [text_item(hello), {"type": "mention", "name": A["name"], "path": a_inst}]),
            ("r10-skill-installed-A-only", [{"type": "skill", "name": A["name"], "path": a_inst}]),
        ]
        for label, inputs in variants:
            if run.stop_reason:
                break
            th = H.thread_start(s, run, ROLE_DEV)
            if th is None:
                break
            tid = th["thread"]["id"]
            res = run_turn(s, run, tid, inputs, label, capture=True)
            res["thread/read"] = thread_read_items(read_thread(s, tid))
            out[label] = res
    finally:
        run.turn_active = False
        set_capture(run, False)
        out["root_exit"] = s.stop("stdin")
        save(run, "capture2_result.json", out)


EXTRA_ROOT_AB = "extra-root-ab"


def make_extra_root(run, pk):
    """An App-owned skill root holding SKILL.md copies of A and B (canonical path), as capture2 found the skill
    input is honoured only for a discovered skill at its canonical path."""
    root = os.path.join(run.obs, "pkgs", EXTRA_ROOT_AB)
    for key in ("A", "B"):
        d = os.path.join(root, pk[key]["name"])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write(pk[key]["text"])
    return os.path.realpath(root)


def skill_path(run, pk, key):
    if run.a.route == "extraroot":
        return os.path.join(os.path.realpath(os.path.join(run.obs, "pkgs", EXTRA_ROOT_AB)), pk[key]["name"], "SKILL.md")
    return os.path.realpath(pk[key]["skill_md"] if run.a.route == "skillmd" else pk[key]["workflow_md"])


def set_roots(s, run, pk, out):
    if run.a.route == "extraroot":
        root = make_extra_root(run, pk)
        out["skills/extraRoots/set"] = s.request("skills/extraRoots/set", {"extraRoots": [root]})
        lst = s.request("skills/list", {"cwds": [s.cwd], "forceReload": True})
        out["skills/list names"] = [(k["name"], k["scope"]) for d in ((lst or {}).get("result") or {}).get("data", [])
                                    for k in d.get("skills", [])]


def sc_w12(run):
    pk = write_packages(run)
    A, B = pk["A"], pk["B"]
    home = run.make_home("w12", config(run), warm=False)
    s, init = new_session(run, "w12", home)
    out = {"route": run.a.route}
    try:
        if init is None:
            return
        time.sleep(1.5)
        set_roots(s, run, pk, out)
        th = H.thread_start(s, run, ROLE_DEV)
        if th is None:
            return
        tid = th["thread"]["id"]
        out["thread"] = tid
        turns = [
            ("t1-W1-start-A", [text_item("This is a test with invented data. Starting workflow A (run 1). "
                                         "Say hello in one short sentence."),
                               {"type": "skill", "name": A["name"], "path": skill_path(run, pk, "A")}], "[WF-A]", None),
            ("t2-W1-followup", [text_item("This is a test with invented data. Name one invented colour in one "
                                          "short sentence.")], "[WF-A]", None),
            ("t3-W2-start-B", [text_item("This is a test with invented data. Run 1 (workflow obs3-workflow-a) has "
                                         "ended; its instructions no longer apply. Starting workflow B (run 2). "
                                         "Say hello in one short sentence."),
                               {"type": "skill", "name": B["name"], "path": skill_path(run, pk, "B")}], "[WF-B]", "[WF-A]"),
            ("t4-W2-followup", [text_item("This is a test with invented data. Name one invented animal in one "
                                          "short sentence.")], "[WF-B]", "[WF-A]"),
        ]
        for label, inputs, want, avoid in turns:
            if run.stop_reason:
                break
            res = run_turn(s, run, tid, inputs, label)
            res["compliance"] = [compliance(t, want, avoid) for t in res["agent_messages"]]
            out[label] = res
        out["thread/read"] = thread_read_items(read_thread(s, tid))
        out["thread/turns/list"] = s.request("thread/turns/list", {"threadId": tid})
    finally:
        run.turn_active = False
        out["exit"] = s.stop("stdin")
        save(run, "w12_result.json", out)


def sc_w34(run):
    pk = write_packages(run)
    A, B = pk["A"], pk["B"]
    home = run.make_home("w34", config(run), warm=False)
    s, init = new_session(run, "w34", home)
    out = {"route": run.a.route}
    try:
        if init is None:
            return
        time.sleep(1.5)
        set_roots(s, run, pk, out)
        cases = [
            ("W3-mention-A", [text_item("This is a test with invented data. Starting workflow A (run 1). Say "
                                        "hello in one short sentence."),
                              {"type": "mention", "name": A["name"], "path": skill_path(run, pk, "A")}], "[WF-A]"),
            ("W4-text-bytes-B", [text_item("This is a test with invented data. Starting workflow B (run 1). The "
                                           "workflow follows.\n\n" + B["text"] + "\nSay hello in one short sentence.")],
             "[WF-B]"),
        ]
        for label, inputs, want in cases:
            if run.stop_reason:
                break
            th = H.thread_start(s, run, ROLE_DEV)
            if th is None:
                break
            tid = th["thread"]["id"]
            res = run_turn(s, run, tid, inputs, label)
            res["compliance"] = [compliance(t, want) for t in res["agent_messages"]]
            res["thread/read"] = thread_read_items(read_thread(s, tid))
            out[label] = res
    finally:
        run.turn_active = False
        out["exit"] = s.stop("stdin")
        save(run, "w34_result.json", out)


def cm(run, mode, dev):
    return {"mode": mode, "settings": {"model": run.a.model, "reasoning_effort": None, "developer_instructions": dev}}


def sc_w5(run):
    pk = write_packages(run)
    A, B = pk["A"], pk["B"]
    home = run.make_home("w5", config(run), warm=False)
    cwd_label = "w5"
    s, init = new_session(run, cwd_label, home)
    out = {}
    tid = None
    say = "This is a test with invented data. Say hello in one short sentence, following your instructions."
    try:
        if init is None:
            return
        time.sleep(1.5)
        th = H.thread_start(s, run, ROLE_DEV)
        if th is None:
            return
        tid = th["thread"]["id"]
        out["thread"] = tid
        steps = [
            ("u1-set-A", cm(run, "default", A["text"])),
            ("t1-after-A", None, "[WF-A]", None, False),
            ("u2-set-B", cm(run, "default", B["text"])),
            ("t2-after-B", None, "[WF-B]", "[WF-A]", False),
            ("t3-no-update", None, "[WF-B]", "[WF-A]", False),
        ]
        for st in steps:
            if run.stop_reason:
                break
            if len(st) == 2:
                label, mode = st
                idx = len(s.notes)
                r = s.request("thread/settings/update", {"threadId": tid, "collaborationMode": mode})
                time.sleep(0.5)
                out[label] = {"params_collaborationMode": mode, "response": r,
                              "settings_notes": [m.get("params") for _, m in s.notes[idx:]
                                                 if m.get("method") == "thread/settings/updated"]}
            else:
                label, _, want, avoid, cap = st
                res = run_turn(s, run, tid, [text_item(say)], label, capture=cap)
                res["compliance"] = [compliance(t, want, avoid) for t in res["agent_messages"]]
                out[label] = res
    finally:
        run.turn_active = False
        out["first_exit"] = s.stop("stdin")
    if tid is None or run.stop_reason:
        save(run, "w5_result.json", out)
        return
    time.sleep(1.5)
    # Persistence across a restart of the supplier: resume and capture the next request.
    s2, init = new_session(run, cwd_label + "-second", home)
    try:
        if init is None:
            return
        time.sleep(1.5)
        r = s2.request("thread/resume", {"threadId": tid, "excludeTurns": True}, timeout=120)
        out["resume"] = {"collaborationMode": ((r or {}).get("result") or {}).get("collaborationMode"),
                         "error": (r or {}).get("error")}
        out["t4-after-restart-capture"] = run_turn(s2, run, tid, [text_item(say)], "t4-after-restart-capture",
                                                   capture=True)
        # Plan mode interplay (capture only): plan with B as developer_instructions; plan with null; default null.
        for label, mode in (("u5-plan-with-B", cm(run, "plan", B["text"])),
                            ("u6-plan-null", cm(run, "plan", None)),
                            ("u7-default-null", cm(run, "default", None))):
            if run.stop_reason:
                break
            idx = len(s2.notes)
            r = s2.request("thread/settings/update", {"threadId": tid, "collaborationMode": mode})
            time.sleep(0.5)
            out[label] = {"params_collaborationMode": mode, "response": r,
                          "settings_notes": [m.get("params") for _, m in s2.notes[idx:]
                                             if m.get("method") == "thread/settings/updated"]}
            out[label]["turn"] = run_turn(s2, run, tid, [text_item(say)], label + "-capture", capture=True)
        out["thread/read"] = thread_read_items(read_thread(s2, tid))
    finally:
        run.turn_active = False
        set_capture(run, False)
        out["second_exit"] = s2.stop("stdin")
        save(run, "w5_result.json", out)


def sc_w6(run):
    home = run.make_home("w6", config(run), warm=False)
    s, init = new_session(run, "w6", home)
    out = {"ROLE_ONE": ROLE_ONE, "ROLE_TWO": ROLE_TWO}
    say1 = "This is a test with invented data. Name one invented fruit in one short sentence."
    say2 = "This is a test with invented data. Name one invented city in one short sentence."
    src = None
    try:
        if init is None:
            return
        time.sleep(1.5)
        th = H.thread_start(s, run, ROLE_ONE)
        if th is None:
            return
        src = th["thread"]["id"]
        out["source"] = src
        res = run_turn(s, run, src, [text_item(say1)], "s1-source-turn")
        res["compliance"] = [compliance(t, "ROLEONE") for t in res["agent_messages"]]
        out["s1-source-turn"] = res
        if run.stop_reason:
            return
        idx = len(s.notes)
        r = s.request("thread/fork", {"threadId": src, "developerInstructions": ROLE_TWO}, timeout=120)
        time.sleep(0.5)
        fres = (r or {}).get("result") or {}
        fork_id = (fres.get("thread") or {}).get("id")
        out["fork"] = {"error": (r or {}).get("error"), "thread_id": fork_id,
                       "instructionSources": fres.get("instructionSources"),
                       "response_keys": sorted(fres.keys()),
                       "thread": thread_read_items({"result": {"thread": fres.get("thread") or {}}}),
                       "notes": [m for _, m in s.notes[idx:] if m.get("method") not in
                                 ("item/agentMessage/delta", "item/reasoning/textDelta")]}
        if not fork_id:
            return
        res = run_turn(s, run, fork_id, [text_item(say2)], "f1-fork-turn")
        res["compliance"] = [{**compliance(t, "ROLETWO"), "contains_ROLEONE": "ROLEONE" in (t or "")}
                             for t in res["agent_messages"]]
        out["f1-fork-turn"] = res
        if run.stop_reason:
            return
        out["s2-source-after-fork-capture"] = run_turn(s, run, src, [text_item(say2)], "s2-source-after-fork-capture",
                                                       capture=True)
        # Control: a fork without developerInstructions (capture).
        r2 = s.request("thread/fork", {"threadId": src, "lastTurnId": out["s1-source-turn"]["turn_id"]}, timeout=120)
        f2 = (((r2 or {}).get("result") or {}).get("thread") or {}).get("id")
        out["fork_control"] = {"error": (r2 or {}).get("error"), "thread_id": f2}
        if f2:
            out["fc1-control-fork-capture"] = run_turn(s, run, f2, [text_item(say2)], "fc1-control-fork-capture",
                                                       capture=True)
        out["thread/read source"] = thread_read_items(read_thread(s, src))
        out["thread/read fork"] = thread_read_items(read_thread(s, fork_id))
        out["thread/list"] = s.request("thread/list", {})
        out["thread/loaded/list"] = s.request("thread/loaded/list", {})
    finally:
        run.turn_active = False
        set_capture(run, False)
        out["first_exit"] = s.stop("stdin")
    if src is None or run.stop_reason:
        save(run, "w6_result.json", out)
        return
    time.sleep(1.5)
    # Fork of a thread that is not loaded (new process), with ROLE_TWO (capture).
    s2, init = new_session(run, "w6-second", home)
    try:
        if init is None:
            return
        time.sleep(1.5)
        r = s2.request("thread/fork", {"threadId": src, "developerInstructions": ROLE_TWO, "excludeTurns": True},
                       timeout=120)
        f3 = (((r or {}).get("result") or {}).get("thread") or {}).get("id")
        out["fork_unloaded"] = {"error": (r or {}).get("error"), "thread_id": f3}
        if f3:
            out["fu1-unloaded-fork-capture"] = run_turn(s2, run, f3, [text_item(say2)], "fu1-unloaded-fork-capture",
                                                        capture=True)
    finally:
        run.turn_active = False
        set_capture(run, False)
        out["second_exit"] = s2.stop("stdin")
        save(run, "w6_result.json", out)


def sc_supp(run):
    """Supplementary, capture-only (no model call).
    W-2b: a skill injection is recorded in the rollout; after the SKILL.md file changes and the supplier
    restarts, does history replay the recorded bytes, is the extra root still set, and what does a new skill
    input inject?  W-6b: does a fork take `config.developer_instructions`; does thread/settings/update on the
    fork add a role text?"""
    import hashlib
    pk = write_packages(run)
    A = pk["A"]
    out = {}
    home = run.make_home("supp-w2b", config(run), warm=False)
    root = make_extra_root(run, pk)
    a_path = os.path.join(root, A["name"], "SKILL.md")
    with open(a_path, "rb") as f:
        out["A_sha256_before"] = hashlib.sha256(f.read()).hexdigest()
    s, init = new_session(run, "supp-w2b", home)
    tid = None
    say = "This is a test with invented data. Say hello in one short sentence."
    try:
        if init is None:
            return
        time.sleep(1.5)
        out["extraRoots/set"] = s.request("skills/extraRoots/set", {"extraRoots": [root]})
        th = H.thread_start(s, run, ROLE_DEV)
        if th is None:
            return
        tid = th["thread"]["id"]
        out["b1-skill-A-capture"] = run_turn(s, run, tid, [text_item(say), {"type": "skill", "name": A["name"],
                                                                             "path": a_path}], "b1", capture=True)
    finally:
        run.turn_active = False
        out["first_exit"] = s.stop("stdin")
    if tid is None or run.stop_reason:
        save(run, "supp_result.json", out)
        return
    with open(a_path, "a", encoding="utf-8") as f:
        f.write("- Invented added line: MODIFIED-AFTER-RUN.\n")
    with open(a_path, "rb") as f:
        out["A_sha256_after_edit"] = hashlib.sha256(f.read()).hexdigest()
    s2, init = new_session(run, "supp-w2b-second", home)
    try:
        if init is None:
            return
        time.sleep(1.5)
        lst = s2.request("skills/list", {"cwds": [s2.cwd], "forceReload": True})
        out["skills/list after restart"] = [k["name"] for d in ((lst or {}).get("result") or {}).get("data", [])
                                            for k in d.get("skills", [])]
        r = s2.request("thread/resume", {"threadId": tid, "excludeTurns": True}, timeout=120)
        out["resume_error"] = (r or {}).get("error")
        out["b2-plain-after-restart-capture"] = run_turn(s2, run, tid, [text_item(say)], "b2", capture=True)
        out["b3-skill-A-roots-not-set-capture"] = run_turn(s2, run, tid, [text_item(say), {
            "type": "skill", "name": A["name"], "path": a_path}], "b3", capture=True)
        out["extraRoots/set again"] = s2.request("skills/extraRoots/set", {"extraRoots": [root]})
        out["b4-skill-A-roots-set-capture"] = run_turn(s2, run, tid, [text_item(say), {
            "type": "skill", "name": A["name"], "path": a_path}], "b4", capture=True)
    finally:
        run.turn_active = False
        out["second_exit"] = s2.stop("stdin")
    if run.stop_reason:
        save(run, "supp_result.json", out)
        return
    home3 = run.make_home("supp-w6b", config(run), warm=False)
    s3, init = new_session(run, "supp-w6b", home3)
    try:
        if init is None:
            return
        time.sleep(1.5)
        th = H.thread_start(s3, run, ROLE_ONE)
        if th is None:
            return
        src = th["thread"]["id"]
        out["c0-source-capture"] = run_turn(s3, run, src, [text_item(say)], "c0", capture=True)
        r = s3.request("thread/fork", {"threadId": src, "config": {"developer_instructions": ROLE_TWO}}, timeout=120)
        f1 = (((r or {}).get("result") or {}).get("thread") or {}).get("id")
        out["fork_config_dev"] = {"error": (r or {}).get("error"), "thread_id": f1}
        if f1:
            out["c1-fork-config-dev-capture"] = run_turn(s3, run, f1, [text_item(say)], "c1", capture=True)
        r = s3.request("thread/fork", {"threadId": src, "developerInstructions": ROLE_TWO}, timeout=120)
        f2 = (((r or {}).get("result") or {}).get("thread") or {}).get("id")
        out["fork_then_settings"] = {"error": (r or {}).get("error"), "thread_id": f2}
        if f2:
            out["fork_then_settings"]["update"] = s3.request("thread/settings/update", {
                "threadId": f2, "collaborationMode": cm(run, "default", ROLE_TWO)})
            out["c2-fork-then-settings-capture"] = run_turn(s3, run, f2, [text_item(say)], "c2", capture=True)
    finally:
        run.turn_active = False
        set_capture(run, False)
        out["third_exit"] = s3.stop("stdin")
        save(run, "supp_result.json", out)


SCENARIOS = {"capture": sc_capture, "capture2": sc_capture2, "w12": sc_w12, "w34": sc_w34, "w5": sc_w5, "w6": sc_w6,
             "supp": sc_supp}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--obs", required=True)
    ap.add_argument("--binary", required=True)
    ap.add_argument("--model", default="qwen/qwen3.5-9b")
    ap.add_argument("--ctx", type=int, default=24576)
    ap.add_argument("--turn-timeout", type=float, default=600.0)
    ap.add_argument("--after-resume", type=float, default=5.0)
    ap.add_argument("--suffix", default="")
    ap.add_argument("--route", default="extraroot", choices=["extraroot", "skillmd", "workflowmd"])
    ap.add_argument("scenario", choices=sorted(SCENARIOS))
    a = ap.parse_args()
    H.LMS_BASE = "http://127.0.0.1:%d/v1" % TAP_PORT
    run = H.Run(a)
    run.event("begin", scenario=a.scenario, pin="0.158.0", model=a.model, ctx=a.ctx, provider_base=H.LMS_BASE,
              suffix=a.suffix, route=a.route, node="OBS-3")
    threading.Thread(target=run.global_watch, daemon=True).start()
    try:
        SCENARIOS[a.scenario](run)
    finally:
        set_capture(run, False)
        for pg in list(H.LIVE_PGIDS):
            try:
                os.killpg(pg, 9)
                run.event("cleanup-killed", pgid=pg)
            except ProcessLookupError:
                pass
        run.watch_done.set()
        run.event("end", scenario=a.scenario, stop=run.stop_reason)
    print(json.dumps({"scenario": a.scenario, "stop": run.stop_reason}))


if __name__ == "__main__":
    main()
