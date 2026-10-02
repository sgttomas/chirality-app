#!/usr/bin/env python3
"""Run the prototype cases of DEL-01-05/ACCESS-v0.2 (VC-A11…VC-A17, VC-A19, VC-A20).

Python 3 standard library only; no Codex, no model, no network, no credential.
Prints one line per case; exit status 0 when every result is as expected.
A "pass (model)" is evidence that the rules run as written, never a VER pass.
"""
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import access_model as A  # noqa: E402
import jsonschema_subset as V  # noqa: E402

RESULTS = []


def result(case, ok, detail):
    RESULTS.append(ok)
    print("%-8s %-16s %s" % (case, "pass (model)" if ok else "FAIL", detail))


SCHEMAS = {}
for name in ("access-state", "conversation-selection", "network-observation", "capability-handoff"):
    fn = os.path.join(DESIGN, "access.%s.schema.json" % name.replace("access-", ""))
    SCHEMAS[name] = json.load(open(fn, encoding="utf-8"))
EMITTED = []  # (schema name, record)


def vc_a14_tables():
    doc = A.parse_doc_tables(os.path.join(DESIGN, "ACCOUNT_AND_PROVIDER_ACCESS.md"))
    lines, ok = [], True
    for k, rows in A.TABLES.items():
        same = doc[k] == rows
        ok &= same
        lines.append("%s %d/%d%s" % (k, len(doc[k]), len(rows), "" if same else " DIFFER"))
    # every row reachable by the model machine from its own from-state
    for k, rows in A.TABLES.items():
        for rid, frm, ev, to in rows:
            m = A.Machine(k)
            m.state = frm
            ok &= (m.apply(ev) == rid and m.state == to)
    # an unlisted move is refused
    m = A.Machine("CS")
    try:
        m.apply("start:ok")
        ok = False
    except A.Refused:
        pass
    result("VC-A14", ok, "doc tables = model tables: " + ", ".join(lines) +
           "; every row applies; unlisted move refused")


def vc_a12_selection():
    app = A.App()
    app.read_account("chatgpt")
    app.configure_local("example_lmstudio")
    c1 = app.new_conversation("example-project")
    r1 = c1.message("hello")
    ok = (r1 == "refused" and c1.refusal["text"] == A.NO_MODEL_CONV and c1.drafts == ["hello"]
          and not app.thread_starts and c1.m.state == "no-selection")
    EMITTED.append(("conversation-selection", c1.record()))
    c1.choose("local-provider:example_lmstudio", "example_lmstudio", "example-model")
    r2 = c1.message("hello")
    ok &= (r2 == "started" and app.thread_starts[-1] ==
           ("account", {"modelProvider": "example_lmstudio", "model": "example-model"}))
    EMITTED.append(("conversation-selection", c1.record()))
    # second conversation in the same project: offer shown, never applied
    c2 = app.new_conversation("example-project")
    n_before = len(app.thread_starts)
    r3 = c2.message("again")
    ok &= (c2.m.state == "offer-shown" and r3 == "refused" and c2.selection is None
           and len(app.thread_starts) == n_before and c2.offer["applied"] is False)
    EMITTED.append(("conversation-selection", c2.record()))
    c2.accept_offer()
    ok &= c2.selection["source"] == "offered-last-choice-accepted"
    c2.message("again")
    EMITTED.append(("conversation-selection", c2.record()))
    # no silent switch: the provider disappears; the conversation stays on its entry
    app.local["example_lmstudio"].apply("config:gone")
    c2.entry_changed(False)
    r4 = c2.message("still there?")
    ok &= (r4 == "refused" and c2.m.state == "entry-unavailable"
           and c2.selection["entryId"] == "local-provider:example_lmstudio"
           and len(app.thread_starts) == n_before + 1)
    EMITTED.append(("conversation-selection", c2.record()))
    # change of entry refused (CS-19)
    c1.change_entry("chatgpt-account")
    ok &= c1.m.state == "started" and c1.refusal["reason"] == "entry-change-not-offered"
    trace = c1.m.trace + ["|"] + c2.m.trace
    result("VC-A12", ok, "K-3 walk: refusal '%s'; offer not applied; explicit provider+model on start; "
           "no switch on unavailability; entry change refused; trace %s" % (A.NO_MODEL_CONV, " ".join(trace)))


def vc_a15_routing():
    app = A.App()
    app.read_account("chatgpt", email="person@example.invalid")
    app.configure_local("example_lmstudio")
    ok = "api-key" not in app.children and app.key.state == "unknown"
    app.key.apply("read:null")
    c = app.new_conversation("p")
    c.choose("api-key", "openai", "example-cloud-model")
    r = c.message("x")
    ok &= (r == "refused" and c.m.state == "entry-unavailable")  # no key: not started, no switch
    app.enter_key(A.KEY_CANARY)
    ok &= "api-key" in app.children and app.key.state == "present"
    c.entry_changed(True)
    c.message("x")
    ca = app.new_conversation("q")
    ca.choose("chatgpt-account", "openai", "example-cloud-model")
    ca.message("y")
    cl = app.new_conversation("r")
    cl.choose("local-provider:example_lmstudio", "example_lmstudio", "example-model")
    cl.message("z")
    homes = [h for h, _ in app.thread_starts]
    ok &= homes == ["api-key", "account", "account"]
    snap = A.state_snapshot(app)
    ok &= snap["entries"][0].get("codexAccount") == "person@example.invalid"
    EMITTED.append(("access-state", snap))
    result("VC-A15", ok, "K2-1 routing: api-key -> H-key (created only with a key), chatgpt and local -> "
           "H-acct; homes used %s" % homes)


def vc_a13_custody():
    app = A.App()
    app.read_account("null")
    app.sign_in_browser()
    shown_during = A.URL_CANARY in app.rec.display
    app.login_completed("login-other", True)       # AR-1: not ours, ignored
    ok_ar1 = app.account.state == "signing-in"
    app.login_completed("login-1", True)
    app.account.apply("person:sign-out")
    app.account.apply("logout:ok")
    app.sign_in_device()
    app.account.apply("person:cancel")
    app.rec.release()
    app.key.apply("read:null")
    app.enter_key(A.KEY_CANARY, outcome="error", echo_in_error=True)
    app.enter_key(A.KEY_CANARY, outcome="exit")
    sends_after_exit = sum(1 for w in app.rec.wire if w["params"].get("apiKey"))
    app.key.apply("read:null")
    app.enter_key(A.KEY_CANARY, outcome="ok")
    snap = A.state_snapshot(app)
    EMITTED.append(("access-state", snap))
    durable = app.rec.durable_text(extra=[snap])
    leaked = [c for c in A.CANARIES if c in durable]
    on_wire = any(w["params"].get("apiKey") == A.KEY_CANARY for w in app.rec.wire)
    ok = (not leaked and on_wire and shown_during and ok_ar1 and app.rec.display == []
          and sends_after_exit == 2)  # one per person's entry before the 'ok' entry; never a resend
    result("VC-A13", ok, "canaries in durable records/logs/errors/snapshots: %s; key on the wire only; "
           "auth URL shown during sign-in, display cleared; foreign loginId ignored; no resend after exit "
           "(%d key frames for 2 entries before the third)" % (leaked or "none", sends_after_exit))


def vc_a11_link():
    steps, touched, root = A.link_case()
    tmp = os.path.realpath(os.environ.get("TMPDIR", "/tmp"))
    inside = all(os.path.realpath(p).startswith(os.path.realpath(root)) for p in touched)
    under_tmp = os.path.realpath(root).startswith(tmp)
    codex_home = os.path.realpath(os.path.expanduser("~/.codex"))
    no_codex = all(not os.path.realpath(p).startswith(codex_home) for p in touched)
    expect = [("setup", "CL-1", "linked"), ("guidance-links", True, "linked"), ("read-through-link", True, "linked"),
              ("write-explicit-target", "CL-10", "linked"), ("write-by-replacement", "CL-4", "link-broken"),
              ("diverged-and-both-kept", True, "link-broken"), ("person-relink", "CL-7", "linked"),
              ("backup-kept", True, "linked"), ("probe-home-separate", True, "linked"),
              ("skills-root-untouched", True, "linked")]
    ok = steps == expect and inside and under_tmp and no_codex
    shutil.rmtree(root)
    result("VC-A11", ok, "steps %s; %d paths, all inside a temporary folder under $TMPDIR (removed); "
           "~/.codex untouched; config.toml, AGENTS.md and skills/ linked (R18-6); nothing written into the "
           "linked skills root (R19-7)" % ([(s, r) for s, r, _ in steps], len(touched)))


def vc_a16_network():
    observed = [
        {"address": "2001:db8::1", "port": 443, "process": "codex", "phase": "start-up", "host_hint": "chatgpt.com"},
        {"address": "2001:db8::2", "port": 443, "process": "git", "phase": "start-up", "host_hint": "github.com"},
        {"address": "127.0.0.1", "port": 1234, "process": "codex", "phase": "turn", "model": True},
        {"address": "192.0.2.10", "port": 443, "process": "codex", "phase": "idle"},
    ]
    view = A.network_view(observed, A.plugins_setting({}))
    EMITTED.append(("network-observation", view))
    purposes = [r["purpose"] for r in view["rows"]]
    unlisted = [r for r in view["rows"] if r["purpose"] == "unlisted"]
    rc = [r for r in view["rows"] if r["purpose"] == "remote-control"]
    plug = [r for r in view["rows"] if r["purpose"] in ("plugins-featured", "plugin-sync")]
    versioned = all("@0.158.0" in r["standing"] for r in view["rows"])
    ok = (len(unlisted) == 1 and unlisted[0]["sources"] == ["app-observed"]
          and len(rc) == 1 and rc[0]["sources"] == ["expected-at-pin"] and rc[0]["appSetting"]["state"] == "no-setting"
          and "no socket without sign-in" in rc[0]["standing"]
          and len(plug) == 2 and all(r["appSetting"]["state"] == "follows-person-setting" for r in plug)
          and "model" in purposes and versioned)
    result("VC-A16", ok, "rows %s; unlisted shown, never blocked; remote-control loop listed as observed "
           "(no setting; no socket without sign-in); plugin rows follow the person's setting; every row "
           "names its version" % purposes)


def vc_a19_plugins():
    inherited = {"PATH": "/usr/bin", "OPENAI_API_KEY": "INVENTED-MARKER-NOT-A-KEY",
                 A.INTERNAL_RC: "1", "HOME": "/invented"}
    lines, ok = [], True
    for mode in ("linked", "own-config"):
        for label, cfg in (("on", {"plugins": True}), ("off", {"plugins": False}), ("unset", {})):
            env, flags, plugins = A.spawn_plan(mode, cfg, inherited)
            want_flag = (mode == "own-config" and label == "off")
            ok &= (("features.plugins=false" in flags) == want_flag)
            ok &= "analytics.enabled=false" in flags
            ok &= A.INTERNAL_RC not in env and not any(k in env for k in A.CREDENTIAL_ENV)
            view = A.network_view([], plugins)
            EMITTED.append(("network-observation", view))
            has_plugin_rows = any(r["purpose"] in ("plugins-featured", "plugin-sync") for r in view["rows"])
            ok &= has_plugin_rows == (label != "off")
            ok &= plugins["source"] == ("app-fallback-flag" if want_flag else
                                        "codex-default-observed" if label == "unset" else "person-config")
            lines.append("%s/%s: flags=%s plugins=%s/%s plugin-rows=%s" % (
                mode, label, ",".join(flags), plugins["value"], plugins["source"], has_plugin_rows))
    result("VC-A19", ok, "L-3: " + "; ".join(lines) + "; internal remote-control variable and credential "
           "variables never passed to the child")


def vc_a20_wording():
    app = A.App()
    app.read_account("chatgpt")
    c = app.new_conversation("w")
    c.message("hello")
    t1 = c.refusal["text"]
    EMITTED.append(("conversation-selection", c.record()))
    c.message("start the review workflow", starts_run=True)
    t2 = c.refusal["text"]
    EMITTED.append(("conversation-selection", c.record()))
    ok = t1 == "not started — no model selected" and t2 == "run not started — no model selected"
    bad = c.record()
    bad["refusal"] = {"reason": "no-model-selected", "runRequested": True, "text": t1}
    mismatch_rejected = bool(V.errors(bad, SCHEMAS["conversation-selection"]))
    ok &= mismatch_rejected
    result("VC-A20", ok, "R18-2: ordinary '%s'; workflow run '%s'; a run refusal with the ordinary wording "
           "is rejected by the schema: %s" % (t1, t2, mismatch_rejected))


def vc_a17_schemas():
    lines, ok = [], True
    fx = os.path.join(HERE, "fixtures")
    for name, schema in SCHEMAS.items():
        for kind in ("valid", "invalid"):
            inst = json.load(open(os.path.join(fx, "%s.%s.json" % (name, kind)), encoding="utf-8"))["instance"]
            errs = V.errors(inst, schema)
            good = (not errs) if kind == "valid" else bool(errs)
            ok &= good
            lines.append("%s.%s: %s" % (name, kind, "valid" if not errs else "invalid (%s)" % errs[0]))
    bad = []
    for name, rec in EMITTED:
        errs = V.errors(rec, SCHEMAS[name])
        if errs:
            bad.append((name, errs[:2]))
    ok &= not bad
    result("VC-A17", ok, " | ".join(lines) + " | %d emitted records valid%s" %
           (len(EMITTED) - len(bad), "" if not bad else "; failures %s" % bad))


if __name__ == "__main__":
    vc_a14_tables()
    vc_a12_selection()
    vc_a15_routing()
    vc_a13_custody()
    vc_a11_link()
    vc_a16_network()
    vc_a19_plugins()
    vc_a20_wording()
    vc_a17_schemas()
    total, fails = len(RESULTS), RESULTS.count(False)
    print("TOTAL %d, FAIL %d" % (total, fails))
    sys.exit(0 if fails == 0 else 1)
