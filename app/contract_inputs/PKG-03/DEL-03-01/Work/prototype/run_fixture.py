#!/usr/bin/env python3
"""Drive SH-1 (simhost.py) through FX-PIPE-01 steps over both native paths.

Prototype only (R12-3); Python 3 standard library. It plays the part of the
App's Codex and records, for each agent request, an item shaped like the
supplier's thread items at pin 0.158.0: `mcpToolCall` for the MCP-tool path
and `commandExecution` for the command-line path. Those item field names are
supplier facts `observed-in-generated-types` (DEL-01-01 generated v2 schema,
sha256 34f28a48...; ADAPTER §3.5). This driver IMITATES them; it does not run
Codex, and nothing here is an observation of Codex.

Outputs (in --out): native_items.jsonl (for the ADAPTER mapper),
host_docs.jsonl (every host document, for the schema check and the P state
check), channel_events.jsonl (for the ADAPTER channel-state machine) and
summary.json. It prints the M3-CP basis comparison (C VC-C-04 / P §11) and a
PASS/FAIL line per check; the exit status is 1 if any check fails.
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

PROTO = Path(__file__).resolve().parent
SIM = [sys.executable, str(PROTO / "simhost.py")]


class Run:
    def __init__(self, out, name, profile="full", edition="e2"):
        self.out = out
        self.state = out / f"state-{name}"
        self.name = name
        self.n = 0
        self.items, self.docs, self.channel = [], [], []
        self.mcp = None
        self.sim("init", profile=profile, edition=edition)

    # ------------------------------------------------------------ plumbing
    def sim(self, mode, *words, json_arg=None, env=None, profile=None, edition=None):
        cmd = SIM + [mode] + list(words) + ["--state", str(self.state)]
        if json_arg is not None:
            cmd += ["--json", json_arg]
        if profile:
            cmd += ["--profile", profile]
        if edition:
            cmd += ["--edition", edition]
        e = dict(os.environ)
        e.update(env or {})
        return subprocess.run(cmd, capture_output=True, text=True, env=e)

    def person(self, *words):
        p = self.sim("person", *words)
        return json.loads(p.stdout) if p.stdout.strip() else {}

    def host(self, *words):
        return self.sim("host", *words)

    def chan(self, event, **kw):
        self.channel.append({"run": self.name, "event": event, **kw})

    def start_mcp(self):
        self.mcp = subprocess.Popen(SIM + ["mcp", "--state", str(self.state)], stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.rpc_id = 0
        r = self.rpc("initialize", {})
        if r is None:
            err = self.mcp.stderr.read()
            self.mcp = None
            return err.strip()
        return None

    def stop_mcp(self):
        if self.mcp:
            self.mcp.stdin.close()
            self.mcp.wait(timeout=10)
            self.mcp = None

    def rpc(self, method, params):
        self.rpc_id += 1
        try:
            self.mcp.stdin.write(json.dumps({"jsonrpc": "2.0", "id": self.rpc_id, "method": method, "params": params}) + "\n")
            self.mcp.stdin.flush()
        except BrokenPipeError:
            return None
        line = self.mcp.stdout.readline()
        return json.loads(line) if line else None

    def record(self, step, path, item, doc=None, note=None):
        self.items.append({"run": self.name, "step": step, "path": path, "thread": f"th-{self.name}",
                           "turn": f"turn-{step}", "item": item, **({"note": note} if note else {})})
        if doc is not None:
            self.docs.append({"run": self.name, "step": step, "path": path, "doc": doc})
        return doc

    def next_id(self):
        self.n += 1
        return f"item-{self.name}-{self.n}"

    # ------------------------------------------------------------- paths
    def mcp_status(self, step):
        """Imitates the per-server status the App reads (mcpServerStatus/list)."""
        r = self.rpc("tools/list", {})
        if "error" in r:
            item = {"type": "mcpServerStatus", "name": "sh1", "tools": {}, "toolsError": r["error"]["message"],
                    "runtimeStatus": "connected", "httpOrigin": None, "hostRefusal": r["error"].get("data")}
            return self.record(step, "N-MCP", item, r["error"].get("data"))
        item = {"type": "mcpServerStatus", "name": "sh1", "tools": {t["name"]: t for t in r["result"]["tools"]},
                "toolsError": None, "runtimeStatus": "connected", "httpOrigin": None}
        return self.record(step, "N-MCP", item)

    def mcp_call(self, step, tool, args, drop=False, note=None):
        r = self.rpc("tools/call", {"name": tool, "arguments": args})
        doc = r["result"]["structuredContent"]
        item = {"type": "mcpToolCall", "id": self.next_id(), "server": "sh1", "tool": tool, "arguments": args,
                "status": "completed", "result": r["result"], "error": None, "durationMs": 1, "readOnlyHint": None}
        if drop:
            item.update(status="failed", result=None, error={"message": "connection closed before the result was read"})
            self.docs.append({"run": self.name, "step": step, "path": "N-MCP", "doc": doc, "unobserved": True})
            return self.record(step, "N-MCP", item, None, note or "response dropped by the driver (lost acknowledgement)")
        return self.record(step, "N-MCP", item, doc, note)

    def cli(self, step, words, json_arg=None, env=None, declined=False, note=None):
        shown = "sh1 cli " + " ".join(words) + (f" --json '{json_arg}'" if json_arg else "")
        base = {"type": "commandExecution", "id": self.next_id(), "command": shown, "cwd": str(self.state),
                "source": "agent", "commandActions": [], "processId": None}
        if declined:
            item = base | {"status": "declined", "exitCode": None, "aggregatedOutput": None, "durationMs": None}
            return self.record(step, "N-CLI", item, None, note or "tool execution declined (A14); no host request made")
        p = self.sim("cli", *words, json_arg=json_arg, env=env)
        aggregated = (p.stderr or "") + (p.stdout or "")
        item = base | {"status": "completed" if p.returncode == 0 else "failed", "exitCode": p.returncode,
                       "aggregatedOutput": aggregated, "durationMs": 1}
        doc = json.loads(p.stdout) if p.returncode == 0 and p.stdout.strip() else None
        return self.record(step, "N-CLI", item, doc, note)


# ------------------------------------------------------------------ fixture

def rows_of(doc, table_prefix):
    for t in doc["views"][0]["tables"]:
        if t["table_identity"].startswith(table_prefix):
            return {r["subject"]["subject_identity"]: r["subject"] for r in t["rows"]}
    return {}


def target(subjects, sid):
    s = subjects[sid]
    return {"subject_identity": sid, "subject_content_identity": s["subject_content_identity"],
            "identity_method": s["identity_method"]}


def proposal(pid, basis, subjects, items, lineage=None, mode="propose", reason="Span S-2->S-3 exceeds 6 m"):
    p = {"proposal_identity": {"value": pid, "minted_by": "proposer"}, "requested_mode": mode,
         "origin": {"author_type": "agent", "author_identity": "unverified", "seat_role_meaning": "external agent (App Codex)",
                    "channel": "external_agent", "conversation": "K-7",
                    "workflow_identity": {"kind": "workflow", "origin": "host", "source_root": "fx-root",
                                          "name": "supports-adjust", "revision": "rev-3"},
                    "workflow_run": "12", "reason": reason},
         "relied_on_basis": [basis], "items": items}
    if lineage:
        p["lineage"] = {"replaces": lineage, "why": "refused_stale"}
    return p


def items_pr(subjects, run_subjects, s3_old):
    return [
        {"item_identity": "1", "operation_identity": "OP-C4", "operation_version": "v1",
         "affected_object": {"created_description": "guide support on R-100 at 4.2 m"},
         "relied_on_targets": [target(run_subjects, "R-100"), target(subjects, "S-2"), target(subjects, "S-3")],
         "attribute": "created", "old_value": None, "new_value": 4.2},
        {"item_identity": "2", "operation_identity": "OP-C5", "operation_version": "v1",
         "affected_object": {"object_identity": "S-3"},
         "relied_on_targets": [target(subjects, "S-3")],
         "attribute": "stiffness", "old_value": s3_old, "new_value": "2.0e6"},
    ]


def main_timeline(out, checks):
    r = Run(out, "main")
    # Channel off (XF-02): the host refuses on both paths.
    r.chan("app_configuration_added", directed_by="person", path="N-MCP", locus="per_thread_configuration")
    r.chan("app_configuration_added", directed_by="person", path="N-CLI", locus="command_on_path")
    assert r.start_mcp() is None
    r.chan("endpoint_ready", locality="local_process")
    off_mcp = r.mcp_status("CH-0")
    off_cli = r.cli("CH-0", ["call", "OP-C1"], json.dumps({"run": "R-100"}))
    r.chan("host_refusal_channel_not_enabled")
    checks.append(("XF-02 host-reported channel not enabled on both paths",
                   off_mcp["outcome"] == off_cli["outcome"] == "channel_not_enabled" and off_cli["reporter"] == "host"))
    # A13 by the scripted person in the double's own enablement facility (fixture act).
    r.person("enable")
    st = json.loads((r.state / "state.json").read_text())
    r.chan("host_enablement_observed", record="in_force", capture=st["enablement"]["capture_evidence_reference"])
    # Discovery on both paths (C §2.1 CI-1).
    r.mcp_status("D-1")
    cat_m = r.mcp_call("D-1", "read-catalog", {})
    cat_c = r.cli("D-1", ["catalog"])
    checks.append(("CI-1 discovery: same edition and entries on both paths", cat_m == cat_c and cat_m["edition"] == "e2"))
    # T3 read on both paths; parity (VC-C-02 restricted to X's two native paths).
    b1m = r.mcp_call("T3", "OP-C1", {"run": "R-100"})
    b1c = r.cli("T3", ["call", "OP-C1"], json.dumps({"run": "R-100"}))
    checks.append(("VC-C-02 (X paths) T3 read identical on MCP and CLI", b1m == b1c))
    B1 = b1m["basis"]
    subj1, run1 = rows_of(b1m, "supports"), rows_of(b1m, "run")
    r.cli("T4", ["call", "OP-C3"], json.dumps({"run": "R-100", "spacing_limit_m": 6}))
    t4a = r.mcp_call("T4a", "OP-C12", {"run": "R-100"})
    checks.append(("T4a host check failed: support spacing, with basis", t4a["standing"]["host_checks"][0]["verdict"] == "failed"))
    pr1 = proposal("PR-1", B1, subj1, items_pr(subj1, run1, "rigid"))
    r.person("edit", "S-3", "stiffness", "1.5e6")                           # T6
    t7 = r.cli("T7", ["submit"], json.dumps(pr1))
    ok7 = all(i["state"] == "refused_stale" and i["refusal"]["failing_targets"] == ["S-3"]
              and i["refusal"]["relied_on_basis"] == B1 and i["refusal"]["evaluated_basis"]["model_revision"] == "r13"
              for i in t7["items"])
    checks.append(("T7 both PR-1 items refused stale per item: failing S-3, relied B1, current r13", ok7))
    t8 = r.mcp_call("T8", "OP-C2", {"run": "R-100", "load_case": "LC-1"})
    checks.append(("T8 unavailable R-no-current-solve with evaluated basis r13",
                   t8["outcome"] == "unavailable" and t8["unavailable_reason"]["reason_identity"] == "R-no-current-solve"
                   and t8["evaluated_basis"]["model_revision"] == "r13"))
    b2 = r.cli("T9", ["call", "OP-C1"], json.dumps({"run": "R-100"}))
    B2 = b2["basis"]
    subj2, run2 = rows_of(b2, "supports"), rows_of(b2, "run")
    pr2 = proposal("PR-2", B2, subj2, items_pr(subj2, run2, "1.5e6"), lineage="PR-1", reason="Reduce thermal restraint")
    t10 = r.mcp_call("T10", "submit-proposal", {"proposal": pr2})
    checks.append(("T10 PR-2 queued (2 items), lineage PR-1", t10["derived_state"]["summary"] == "queued"
                   and t10.get("lineage_replaces") == "PR-1"))
    r.person("accept", "PR-2", "1")                                          # T11
    r.person("reject", "PR-2", "2")
    t11 = r.cli("T11o", ["observe", "PR-2"])
    checks.append(("T11 observed: item 1 accepted (A5), item 2 rejected (A10), derived 'mixed'",
                   [i["state"] for i in t11["items"]] == ["accepted", "rejected"] and t11["derived_state"]["summary"] == "mixed"))
    r.host("apply", "PR-2")                                                  # T12
    t12 = r.mcp_call("T12o", "observe-proposal", {"proposal_identity": "PR-2"})
    it1 = t12["items"][0]
    checks.append(("T12 item 1 applied RC-1 at r14; S-5 created, R-100 changed; A5 kept",
                   it1["state"] == "applied" and it1["applied"]["receipt_reference"] == "RC-1"
                   and it1["applied"]["resulting_revision"] == "r14"
                   and [(o["object_identity"], o["relation"]) for o in it1["applied"]["resulting_objects"]] == [("S-5", "created"), ("R-100", "changed")]
                   and it1["decision"]["act_kind"] == "A5"))
    # T13: resubmission whose acknowledgement is lost, then observation first, then a retry.
    r.mcp_call("T13", "submit-proposal", {"proposal": pr2}, drop=True)
    t13o = r.cli("T13o", ["observe", "PR-2"])
    t13r = r.cli("T13r", ["submit"], json.dumps(pr2))
    checks.append(("T13 observation by identity after the lost acknowledgement returns recorded state (2 submissions)",
                   t13o["kind"] == "recorded_state" and t13o["submissions_recorded"] == 2))
    checks.append(("T13 retry answered from recorded state before any basis check; never stale (3 submissions, RC-1)",
                   t13r["answered_from_recorded_state"] and t13r["submissions_recorded"] == 3
                   and t13r["items"][0]["applied"]["receipt_reference"] == "RC-1"))
    conflict = dict(pr2, items=[dict(pr2["items"][0], new_value=4.5), pr2["items"][1]])
    ic = r.mcp_call("PM-3", "submit-proposal", {"proposal": conflict})
    checks.append(("PM-3 same identity, different content -> identity conflict, no effect",
                   ic["kind"] == "identity_conflict" and ic["effect"] == "none"))
    nk = r.cli("PM-2", ["observe", "PR-9"])
    checks.append(("PM-2 observation of an identity the host never received -> not known to host", nk["kind"] == "not_known_to_host"))
    vr1 = r.mcp_call("V-R1", "OP-C7", {"proposal": "PR-2", "items": "1"})
    checks.append(("V-R1 reserved entry -> not permitted, A8 offered", vr1["outcome"] == "not_permitted" and vr1["a8_offered"]))
    xf22 = r.cli("XF-22", ["call", "OP-C4"], json.dumps({"run": "R-100", "location_m": 5.0, "type": "guide"}))
    checks.append(("XF-22 direct request under set-1 -> not permitted naming P-03", xf22["outcome"] == "not_permitted"
                   and xf22["governing_treatment"]["reference"].startswith("P-03")))
    hist = r.mcp_call("C-HR", "OP-C1", {"run": "R-100", "requested_basis": B1})
    checks.append(("C §6.4 requested historical read at r12 -> currency historical, basis r12",
                   hist["standing"]["currency"] == "historical" and hist["basis"]["model_revision"] == "r12"))
    r.cli("XF-34", ["call", "OP-C1"], json.dumps({"run": "R-100"}), declined=True)
    ni = r.cli("OM-CLI-2", ["call", "OP-C1"], json.dumps({"run": "R-100"}), env={"SH1_STDERR_NOTE": "1"},
               note="host wrote a note on stderr; aggregated output is not one document")
    # T15-T16 direct branch (XF-23).
    r.person("grant-direct", "S-4")
    t16r = r.mcp_call("T16pre", "OP-C1", {"run": "R-100"})
    s16 = rows_of(t16r, "supports")
    pr3 = proposal("PR-3", t16r["basis"], s16, [{"item_identity": "1", "operation_identity": "OP-C9", "operation_version": "v1",
                                                 "affected_object": {"object_identity": "S-4"},
                                                 "relied_on_targets": [target(s16, "S-4")], "attribute": "label",
                                                 "old_value": "G-4a", "new_value": "G-4"}], mode="apply_directly",
                   reason="Relabel S-4")
    t16 = r.cli("T16", ["submit"], json.dumps(pr3))
    checks.append(("T16 direct under set-2 -> applied RC-2, branch direct, no decision recorded",
                   t16["items"][0]["state"] == "applied" and t16["items"][0]["applied"]["branch"] == "direct_under_grant"
                   and "decision" not in t16["items"][0]))
    # Endpoint stops (XF-06), then App relaunch (S-7).
    r.stop_mcp()
    r.person("stop-endpoint")
    down = r.cli("XF-06", ["call", "OP-C1"], json.dumps({"run": "R-100"}))
    err = r.start_mcp()
    r.chan("endpoint_failed", reason=err or "not observed")
    checks.append(("XF-06 endpoint stopped: CLI exits non-zero with no host document; MCP server fails to start",
                   down is None and err is not None))
    r.chan("app_relaunch")
    r.person("start-endpoint")
    assert r.start_mcp() is None
    r.chan("endpoint_ready", locality="local_process")
    r.mcp_status("S-7")
    r.chan("host_enablement_observed", record="in_force", capture=st["enablement"]["capture_evidence_reference"])
    r.person("disable")
    r.chan("host_enablement_observed", record="not_in_force")
    r.stop_mcp()
    return r, B1, B2, pr1, pr2, t7, t10, t12, t13r


def edition_variant(out, checks):
    r = Run(out, "ved1", edition="e1")
    r.person("enable")
    assert r.start_mcp() is None
    e1 = r.cli("V-ED1-1", ["catalog"])
    missing = "OP-C9" not in [e["operation_identity"] for e in e1["entries"]]
    r.person("publish-edition")
    ev = r.mcp_call("V-ED1-2", "read-edition-events", {})
    e2 = r.mcp_call("V-ED1-3", "read-catalog", {})
    checks.append(("V-ED1 OP-C9 missing on e1; one host-reported event e1->e2 adding OP-C9 v1; rediscovery shows it",
                   missing and len(ev["events"]) == 1 and ev["events"][0]["added"][0]["operation_identity"] == "OP-C9"
                   and "OP-C9" in [e["operation_identity"] for e in e2["entries"]] and e2["previous_edition"] == "e1"))
    r.stop_mcp()
    return r


def lineage_variant(out, checks):
    r = Run(out, "nolineage", profile="no-lineage")
    # Channel facts in the form SWBPIPE's answers describe (SQ-13, SQ-28): no A13 facility, and a host that
    # answers anyway. Synthetic events only: SH-1 has an enablement facility; this is not SH-1 behaviour.
    for ev in ({"event": "app_configuration_added", "directed_by": "person", "path": "N-CLI", "locus": "command_on_path"},
               {"event": "endpoint_ready", "locality": "local_socket"},
               {"event": "host_enablement_observed", "record": "no_facility"},
               {"event": "host_answer_without_A13"}):
        r.channel.append({"run": "swbform", **ev})
    r.person("enable")
    cat = r.cli("R12-9-a", ["catalog"])
    rd = r.cli("R12-9-b", ["call", "OP-C1"], json.dumps({"run": "R-100"}))
    b = rd["basis"]
    absent = sorted(k for k, v in b.items() if isinstance(v, dict))
    checks.append(("R13-1 case: basis profile declares no workspace identity or generation; the read marks both host_declares_none",
                   cat["basis_profile"]["workspace_identity"] == "not_supplied"
                   and absent == ["generation", "workspace_identity"]))
    return r, absent


def classify(basis, profile):
    """R13-1 (B3's option B, ruled; C §5.2 rule 1) as an executable rule."""
    missing = {k: v["not_supplied"] for k, v in basis.items() if isinstance(v, dict)}
    if not missing:
        return "citable"
    declared_none = all(v == "host_declares_none" and profile.get(k) == "not_supplied" for k, v in missing.items())
    lineage_only = set(missing) <= {"workspace_identity", "generation"}
    if declared_none and lineage_only:
        return "citable with limit 'basis lineage not supplied'; comparisons across lineages are unknown (incomparable)"
    return "basis incomplete: not citable"


def m3cp(B1, B2, pr1, pr2, t7, t10, t12, t13r):
    def rev(b):
        return b["model_revision"]
    rows = [
        ("T3 read", rev(B1), "-", "-", "-"),
        ("T5 PR-1 reference", "-", rev(pr1["relied_on_basis"][0]), "-", "-"),
        ("T7 refusal (item 1)", "-", rev(pr1["relied_on_basis"][0]),
         f"relied {rev(t7['items'][0]['refusal']['relied_on_basis'])} / current {rev(t7['items'][0]['refusal']['evaluated_basis'])}", "-"),
        ("T9 read", rev(B2), "-", "-", "-"),
        ("T10 PR-2 reference", "-", rev(pr2["relied_on_basis"][0]), "-", "-"),
        ("T12 applied association", "-", "-", "-",
         f"relied {rev(t12['items'][0]['applied']['relied_on_basis'])} / {t12['items'][0]['applied']['receipt_reference']} / "
         f"{t12['items'][0]['applied']['resulting_revision']}"),
        ("T13 retry (recorded state)", "-", rev(pr2["relied_on_basis"][0]), "no stale refusal",
         t13r["items"][0]["applied"]["receipt_reference"]),
    ]
    same = (pr1["relied_on_basis"][0] == B1 and t7["items"][0]["refusal"]["relied_on_basis"] == B1
            and pr2["relied_on_basis"][0] == B2 and t12["items"][0]["applied"]["relied_on_basis"] == B2)
    return rows, same


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(os.environ.get("TMPDIR", "/tmp"), f"sh1-run-{int(time.time())}"))
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    checks = []
    r, B1, B2, pr1, pr2, t7, t10, t12, t13r = main_timeline(out, checks)
    rows, same = m3cp(B1, B2, pr1, pr2, t7, t10, t12, t13r)
    checks.append(("VC-C-04 / P §11 M3-CP: no step rewrites a relied-on reference (all five basis elements compared)", same))
    v = edition_variant(out, checks)
    nl, absent = lineage_variant(out, checks)
    runs = [r, v, nl]
    with open(out / "native_items.jsonl", "w") as f:
        for x in runs:
            for it in x.items:
                f.write(json.dumps(it) + "\n")
    with open(out / "host_docs.jsonl", "w") as f:
        for x in runs:
            for d in x.docs:
                f.write(json.dumps(d) + "\n")
    with open(out / "channel_events.jsonl", "w") as f:
        for x in runs:
            for c in x.channel:
                f.write(json.dumps(c) + "\n")
    nlb = next(d["doc"]["basis"] for d in nl.docs if d["step"] == "R12-9-b")
    prof = next(d["doc"]["basis_profile"] for d in nl.docs if d["step"] == "R12-9-a")
    full_prof = {"workspace_identity": "supplied", "generation": "supplied"}
    omitted = dict(nlb, workspace_identity={"not_supplied": "omitted"}, generation=B1["generation"])
    r131 = {"no-lineage read on a host declaring none": classify(nlb, prof),
            "read omitting workspace identity on a host that supplies it": classify(omitted, full_prof),
            "T3 read on the full profile": classify(B1, full_prof)}
    checks.append(("R13-1 rule: a no-lineage read is citable with 'basis lineage not supplied'; an omitted "
                   "element stays basis incomplete; a full read is citable",
                   r131["no-lineage read on a host declaring none"].startswith("citable with limit")
                   and r131["read omitting workspace identity on a host that supplies it"].startswith("basis incomplete")
                   and r131["T3 read on the full profile"] == "citable"))
    print("SH-1 run directory:", out)
    print("\nM3-CP basis comparison (revision shown; the full five-element descriptors were compared):")
    print(f"{'step':32} {'read':6} {'proposal ref':13} {'refusal':24} applied")
    for row in rows:
        print(f"{row[0]:32} {row[1]:6} {row[2]:13} {row[3]:24} {row[4]}")
    print("\nR13-1 (ruled; C §5.2 rule 1), reads classified for citation:")
    for k, val in r131.items():
        print(f"  {k}: {val}")
    print("\nChecks:")
    failed = 0
    for name, ok in checks:
        print(("PASS " if ok else "FAIL ") + name)
        failed += 0 if ok else 1
    print(f"\n{len(checks) - failed} of {len(checks)} checks passed; items recorded: "
          f"{sum(len(x.items) for x in runs)}; host documents: {sum(len(x.docs) for x in runs)}")
    (out / "summary.json").write_text(json.dumps({"checks": [[n, ok] for n, ok in checks], "r13_1": r131,
                                                   "m3cp": rows}, indent=1))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
