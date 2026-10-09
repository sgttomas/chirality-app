#!/usr/bin/env python3
"""ADAPTER-v0.6 §4.6 (observation-to-record mapping, both native paths),
§7.7 (checkpoint observations for DEL-02-03, CO-1…CO-11) and §3.6
(channel-state transitions), as executable rules over an SH-1 run
(C-v0.8 §10.8); each dispatch record is also written as an RS-v0.8 §5
operation entry with its R11 evidence-limit entries and validated against
DEL-04-03's `RS_RECORD.schema.json` (R14-3).

Prototype only (R12-3); Python 3 standard library; not product code.

  python3 observe_map.py --run DIR [--write-examples]

Reads DIR/native_items.jsonl and DIR/channel_events.jsonl written by
DEL-03-01's run_fixture.py, maps every item to an external dispatch record,
derives the checkpoint observations and channel statuses, validates all three
against the ADAPTER PROPOSED schemas (with DEL-03-01's subset validator) and
prints the mapping. The items it reads imitate supplier item shapes observed in
generated types at pin 0.158.0; they are not observations of Codex.
"""

import argparse
import copy
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORKING = HERE.parents[2]
C_PROTO = next(WORKING.glob("DEL-03-01")) / "Design" / "prototype"
sys.path.insert(0, str(C_PROTO))
from schema_subset import load_registry, validate  # noqa: E402

SCHEMAS = sorted(f for d in WORKING.glob("DEL-03-0[123]") for f in (d / "Design").glob("*.schema.json"))
DISPATCH = "urn:chirality:app-v4:proposed:external-dispatch-record"
CHECKPOINT = "urn:chirality:app-v4:proposed:checkpoint-observation"
CHANNEL = "urn:chirality:app-v4:proposed:channel-status"

STATUS = {"inProgress": "in_progress", "completed": "completed", "failed": "failed", "declined": "declined"}
ROUTE = {"read-catalog": "discovery", "catalog": "discovery", "read-edition-events": "discovery", "events": "discovery",
         "submit-proposal": "submission", "submit": "submission", "observe-proposal": "observation", "observe": "observation"}
UNIFORM = {"queued", "refused_stale", "refused_invalid", "refused_not_permitted", "applied"}
# OM-1 (R14-4; OBS-1b): Codex wraps a model-issued command once in the login shell; that one wrapper is removed.
WRAPPER = re.compile(r"^(?:/bin/|/usr/bin/)?(?:zsh|bash|sh) -lc '(.*)'$", re.S)
COMPOUND = (" && ", " || ", "; ", " | ")


def unwrap(command):
    m = WRAPPER.match(command)
    return (m.group(1), True) if m else (command, False)


def safe(x):
    return re.sub(r"[^A-Za-z0-9._:-]", "-", str(x))


class Mapper:
    """OM-1..OM-10 (ADAPTER §4.6)."""

    def __init__(self):
        self.tool_map = {}          # N-MCP tool name -> operation (host-supplied via discovery)
        self.catalog = {}           # operation identity -> entry
        self.seen_bases = {}        # run -> [basis descriptors observed in read results]
        self.last_state = {}        # (run, proposal) -> last observed derived summary
        self.unknown = set()        # (run, proposal) with an outcome unknown not yet followed by observation

    # -- native reference and request kind (OM-1, OM-2)
    def classify(self, path, item):
        if path == "N-MCP":
            name = item.get("tool") or "tools/list"
            ref = {"server": item.get("server") or item.get("name"), "tool": name}
        else:
            cmd, _ = unwrap(item["command"])
            words = cmd.split()
            name = words[3] if words[2] == "call" else words[2]
            ref = {"command_form": " ".join(words[:4] if words[2] == "call" else words[:3])}
        if item["type"] == "mcpServerStatus":
            return ref, "discovery", {"not_established": "not_a_catalog_operation"}, name
        if name in ROUTE:
            return ref, ROUTE[name], {"not_established": "not_a_catalog_operation"}, name
        op = self.tool_map.get(name) if path == "N-MCP" else (name if name in self.catalog else None)
        if op is None:
            return ref, "unrecognized", {"not_established": "no_mapping"}, name
        e = self.catalog[op]
        if e["effects"]["kind"] == "change":
            kind = "change_call"
        elif e["result"]["content_kinds"] == ["host_check"]:
            kind = "host_check"
        elif e["result"]["content_kinds"] == ["finding"]:
            kind = "examination"
        else:
            kind = "read"
        return ref, kind, {"operation_identity": op, "operation_version": e["operation_version"]}, name

    # -- host result isolation (OM-3, OM-4)
    @staticmethod
    def host_result(path, item):
        if path == "N-MCP":
            res = item.get("result") or {}
            if isinstance(res.get("structuredContent"), dict):
                return res["structuredContent"], None
            if item["type"] == "mcpServerStatus":
                return item.get("hostRefusal"), None
            return None, None
        out = item.get("aggregatedOutput")
        if not out:
            return None, None
        try:
            return json.loads(out), None
        except json.JSONDecodeError:
            # OM-4: only a completed command can carry a host result; a failed one carries none.
            return None, ("host_result_not_isolated" if item.get("status") == "completed" else None)

    def learn(self, doc):
        if isinstance(doc, dict) and "entries" in doc:
            self.catalog = {e["operation_identity"]: e for e in doc["entries"]}

    def map(self, rec):
        """One external dispatch record, or None when OM-1 says the item is not a dispatch."""
        path, item = rec["path"], rec["item"]
        start_source = (rec.get("started") or {}).get("source", item.get("source", "agent"))
        if path == "N-CLI" and start_source != "agent":
            return None                 # OM-1: read at item/started; the person's own shell is never a dispatch
        if item["type"] == "mcpServerStatus":
            for t in (item.get("tools") or {}).values():
                m = t.get("_meta", {}).get("sh1/catalog")
                if m:
                    self.tool_map[t["name"]] = m["operation_identity"]
        ref, kind, op, name = self.classify(path, item)
        status = STATUS.get(item.get("status"), "completed")
        doc, iso = self.host_result(path, item)
        self.learn(doc)
        limits = []
        if iso:
            limits.append(iso)
        if path == "N-CLI" and any(op in unwrap(item["command"])[0] for op in COMPOUND):
            limits.append("dispatch_recognized_from_compound_command")
        r = {"record_kind": "external_dispatch", "path": path,
             "correlation": {"thread": rec["thread"], "turn": rec["turn"], "native_item": item.get("id", f"status-{rec['step']}")},
             "native_reference": ref, "request_kind": kind, "operation": op, "native_status": status,
             "transport": {"exit_status": item.get("exitCode"), "duration_ms": item.get("durationMs")} if path == "N-CLI"
             else {"duration_ms": item.get("durationMs")},
             "observed_at": rec["step"]}
        if path == "N-CLI":
            r["native_source"] = {"at_start": start_source}
            if item.get("source"):
                r["native_source"]["at_completion"] = item["source"]
        if item.get("error"):
            r["transport"]["supplier_error"] = item["error"]["message"]
        if doc and isinstance(doc, dict) and "edition" in doc:
            r["edition"] = doc["edition"]
        key = None
        args = item.get("arguments") or {}
        if kind in ("submission", "observation"):
            if path == "N-MCP":
                pid = args.get("proposal", {}).get("proposal_identity", {}).get("value") if kind == "submission" else args.get("proposal_identity")
            else:
                w = item["command"]
                pid = (json.loads(w.split("--json ", 1)[1].strip("'"))["proposal_identity"]["value"]
                       if kind == "submission" else w.split()[3])
            r["proposal_identity"] = pid
            r["proposal_minted_by"] = "not_observed"
            key = (rec["run"], pid)
            if kind == "submission":
                req = args.get("proposal") if path == "N-MCP" else json.loads(item["command"].split("--json ", 1)[1].strip("'"))
                r["requested_mode"] = req["requested_mode"]
                r["proposal_minted_by"] = req["proposal_identity"].get("minted_by", "not_observed")
                r["origin_observed"] = {"author_identity": "unverified", "channel": "external_agent"}
                limits.append("unverified_caller_identity")
                cited = req["relied_on_basis"][0]
                r["relied_on_basis_check"] = ("observed_in_prior_read" if cited in self.seen_bases.get(rec["run"], [])
                                              else "cited_basis_not_observed")
                if r["relied_on_basis_check"] == "cited_basis_not_observed":
                    limits.append("cited_basis_not_observed")
                if key in self.unknown:
                    limits.append("resubmission_without_prior_observation")
        # outcome (OM-5..OM-9; M-1..M-7)
        if item["type"] == "mcpServerStatus" and doc is None:
            if item.get("toolsError"):
                out = {"value": "not_established", "reporter": "app_via_supplier", "reason": item["toolsError"]}
            else:
                out = {"value": "success", "reporter": "app_via_supplier",
                       "reason": f"{item.get('runtimeStatus')}; {len(item.get('tools') or {})} tools; mapping host-supplied"}
        elif status == "declined":
            out = {"value": "tool_execution_declined", "reporter": "app", "reason": "A14 declined; no host request (M-6)"}
            r["a14_record_reference"] = f"R13-{r['correlation']['native_item']}"
        elif doc is None:
            text = (item.get("aggregatedOutput") or (item.get("error") or {}).get("message") or "no output").strip()
            if kind in ("submission", "observation") and (status == "failed" or iso):
                out = {"value": "outcome_unknown", "reporter": "app", "observer": "app",
                       "last_observed_state": self.last_state.get(key, "submitted"), "reason": text[:120]}
                if kind == "submission":
                    self.unknown.add(key)
                    limits.append("lost_acknowledgement")
            elif iso:
                out = {"value": "error", "reporter": "app", "reason": "no host result isolated (M-3)"}
            else:
                out = {"value": "endpoint_unavailable", "reporter": "app_via_supplier", "reason": text[:120]}
        elif "entries" in doc or "events" in doc:
            out = {"value": "success", "reporter": "host"}
        elif "kind" in doc:
            k = doc["kind"]
            if k == "identity_conflict":
                out = {"value": "refused_identity_conflict", "reporter": "host"}
            elif k == "not_known_to_host":
                out = {"value": "not_known_to_host", "reporter": "host"}
            else:
                s = doc["derived_state"]["summary"]
                first = kind == "submission" and not doc.get("answered_from_recorded_state")
                out = {"value": s if first and s in UNIFORM else "recorded_state", "reporter": "host",
                       "reason": f"derived state: {s}"}
                self.last_state[key] = s
                self.unknown.discard(key)
        else:
            out = {"value": doc["outcome"], "reporter": doc.get("reporter", "host")}
            if doc["outcome"] == "success":
                self.seen_bases.setdefault(rec["run"], []).append(doc["basis"])
                if any(isinstance(v, dict) for v in doc["basis"].values()):
                    limits.append("basis_lineage_not_supplied")
        r["outcome"] = out
        if doc is not None:
            r["host_result"] = doc
        r["evidence_limits"] = sorted(set(limits))
        return r


def checkpoint_observations(records):
    """CO-1..CO-9 (ADAPTER §7.7): what the adapter passes to DEL-02-03."""
    obs, seen, decided = [], {}, set()
    for r in records:
        pid = r.get("proposal_identity")
        run = r["correlation"]["thread"]
        src = r["correlation"]["native_item"]
        if r["outcome"]["value"] == "outcome_unknown":
            obs.append({"observation_kind": "observation_lost", "exec_event": "CE-13",
                        "source_record": src, "proposal_identity": pid, "lost_what": "result of a submission",
                        "last_observed_state": r["outcome"]["last_observed_state"], "observed_at": r["observed_at"]})
            seen[(run, pid, "lost")] = True
            continue
        doc = r.get("host_result") or {}
        if doc.get("kind") != "recorded_state":
            continue
        if seen.pop((run, pid, "lost"), None):
            obs.append({"observation_kind": "observation_recovered", "exec_event": "CE-14",
                        "source_record": src, "proposal_identity": pid, "lost_what": "result of a submission",
                        "last_observed_state": doc["derived_state"]["summary"], "observed_at": r["observed_at"]})
        queued_now = [i["item_identity"] for i in doc["items"] if i["state"] == "queued" and (run, pid, i["item_identity"]) not in seen]
        if queued_now:
            ids = [{"item_identity": i["item_identity"], "content_identity": i["change_item_content_identity"],
                    "identity_method": i.get("identity_method", "unknown")}
                   for i in doc["items"] if i["item_identity"] in queued_now]
            obs.append({"observation_kind": "proposal_queued", "exec_event": "CE-3", "source_record": src,
                        "proposal_identity": pid, "items": queued_now, "item_content_identities": ids,
                        "evidence_time": doc["observed_at"], "evidence_time_source": "host_outcome_time",
                        "observed_at": r["observed_at"]})
        for it in doc["items"]:
            k = (run, pid, it["item_identity"])
            prev = seen.get(k)
            if prev == it["state"]:
                continue
            seen[k] = it["state"]
            d = it.get("decision")
            if d and (prev is None or prev == "queued"):
                cap = d.get("capture_evidence_reference", "not_supplied")
                ref = d.get("act_reference", "not_supplied_by_host")
                # §7.6: the App writes a faithful RS §6 record only with a capture-evidence reference
                faithful = ("not_written" if cap == "not_supplied" else
                            "rec:app:%s:%s" % (safe(run), safe(ref if ref != "not_supplied_by_host"
                                                               else f"{pid}-{it['item_identity']}-{d['act_kind']}")))
                obs.append({"observation_kind": "act_observed", "exec_event": "CE-7",
                            "source_record": src, "proposal_identity": pid, "item_identity": it["item_identity"],
                            "act": {"act_kind": d["act_kind"], "decision_actor": d["actor"], "recorder": "app",
                                    "recording_mode": "faithful_recording",
                                    "bound_content_identity": it["change_item_content_identity"],
                                    "identity_method": it.get("identity_method", "unknown"),
                                    "capture_evidence": cap, "act_reference": ref,
                                    "capture_time": d.get("captured_at", "not_supplied_by_host"),
                                    "faithful_record": faithful},
                            "evidence_time": doc["observed_at"], "evidence_time_source": "host_outcome_time",
                            "observed_at": r["observed_at"]})
            if d and d["act_kind"] == "A5" and it["state"] in ("refused_stale", "application_error", "outcome_unknown") \
                    and prev in (None, "queued", "accepted"):
                na = {"accepted_by": d.get("act_reference", "not_supplied_by_host"), "result": it["state"]}
                if it["state"] == "outcome_unknown":
                    na["observer"] = it.get("observer", "host") if it.get("observer") in ("app", "host") else "host"
                obs.append({"observation_kind": "decided_item_not_applied", "exec_event": "CE-7", "source_record": src,
                            "proposal_identity": pid, "item_identity": it["item_identity"], "not_applied": na,
                            "observed_at": r["observed_at"]})
            if it["state"] in ("refused_stale", "refused_invalid", "refused_not_permitted", "withdrawn", "left_queue") \
                    and prev in (None, "queued") and not d:
                left = it.get("item_left") or {}
                o = {"observation_kind": "item_left", "exec_event": "CE-7",
                     "source_record": src, "proposal_identity": pid, "item_identity": it["item_identity"],
                     "left_cause": left.get("cause") or it.get("left_cause", it["state"]), "observed_at": r["observed_at"]}
                if left.get("time"):
                    o["left_time"] = left["time"]
                obs.append(o)
            if it["state"] == "applied":
                a = it["applied"]
                obs.append({"observation_kind": "applied_outcome", "exec_event": "CE-3",
                            "source_record": src, "proposal_identity": pid, "item_identity": it["item_identity"],
                            "applied": {"receipt_reference": a["receipt_reference"], "resulting_revision": a["resulting_revision"],
                                        "resulting_objects": [o["object_identity"] for o in a["resulting_objects"]]
                                        if isinstance(a["resulting_objects"], list) else "not_supplied"},
                            "observed_at": r["observed_at"]})
        if doc["derived_state"]["all_items_decided"] and (run, pid) not in decided:
            decided.add((run, pid))
            obs.append({"observation_kind": "all_items_decided", "exec_event": "CE-7",
                        "source_record": src, "proposal_identity": pid, "observed_at": r["observed_at"]})
    return obs


def channel_statuses(events):
    """CT-1..CT-12 (ADAPTER §3.6): the channel status after each event, per run."""
    out = []
    facts = {}
    for ev in events:
        f = facts.setdefault(ev["run"], {"config": None, "enablement": "never_observed", "capture": None,
                                         "endpoint": "not_observed", "reason": None, "limits": set()})
        e = ev["event"]
        if e == "app_configuration_added":
            f["config"] = (ev["path"], ev["locus"], ev["directed_by"])
            if ev["directed_by"] != "person":
                f["limits"].add("agent_written_configuration")
        elif e == "app_configuration_removed":
            f["config"] = None
        elif e == "endpoint_ready":
            f["endpoint"], f["reason"] = "yes", None
        elif e in ("endpoint_failed", "endpoint_auth_required", "tools_discovery_failed"):
            f["endpoint"], f["reason"] = "no", ev.get("reason", e)
        elif e == "host_enablement_observed":
            f["enablement"], f["capture"] = ev["record"], ev.get("capture")
        elif e == "host_refusal_channel_not_enabled":
            f["enablement"], f["capture"] = "host_reports_off", None
        elif e == "host_answer_without_A13":
            f["limits"].add("host_reachable_without_evidenced_A13")
        elif e == "app_relaunch":
            f["enablement"], f["capture"], f["endpoint"], f["reason"] = "not_reobserved", None, "not_observed", None
        st = {"host_identity": "SH-1", "reporter": "app", "since": f"{ev['run']}:{len(out) + 1}:{e}",
              "host_enablement": {"record": {"in_force": "in_force", "no_facility": "no_facility",
                                             "not_readable": "not_readable"}.get(f["enablement"], "not_in_force")},
              "app_side_configuration": {"present": f["config"] is not None,
                                         "directed_by": f["config"][2] if f["config"] else "none"},
              "endpoint": {"reachable": f["endpoint"], "locality": "local_process" if f["endpoint"] == "yes" else "not_observed"},
              "model_destination": {"requested": "user-selected model", "effective": "unknown", "destination_class": "unknown"},
              "evidence_limits": sorted(f["limits"])}
        if f["config"]:
            st["app_side_configuration"] |= {"path": f["config"][0], "locus": f["config"][1]}
        if f["capture"]:
            st["host_enablement"]["capture_evidence_reference"] = f["capture"]
        if f["endpoint"] == "no" and f["reason"]:
            st["endpoint"]["observed_reason"] = f["reason"]
        if not f["config"]:
            st |= {"channel_state": "disabled", "disabled_sub_case": "app_side_not_configured"}
        elif f["enablement"] != "in_force":
            sub = {"host_reports_off": "host_reports_off", "not_in_force": "disabled_by_A13",
                   "no_facility": "host_has_no_A13_facility",
                   "not_reobserved": "enablement_not_reobserved"}.get(f["enablement"], "never_enabled")
            st |= {"channel_state": "disabled", "disabled_sub_case": sub}
            if f["enablement"] in ("not_readable", "not_reobserved"):
                st["enablement_unconfirmed"] = True
            if sub == "host_reports_off":
                st["reporter"] = "host"
        elif f["endpoint"] != "yes":
            st |= {"channel_state": "endpoint_unavailable", "reason": f["reason"] or "endpoint not observed"}
        else:
            st |= {"channel_state": "enabled", "reporter": "host"}
        out.append((ev["run"], e, st))
    return out


# -- RS-v0.8 §5 receiving (R14-3): ADAPTER tokens -> RS record values, stated once in RS §5
RS_OUTCOME = {"applied": "applied (receipt)", "refused_invalid": "refused — invalid", "refused_stale": "refused — stale",
              "refused_not_permitted": "not permitted", "refused_identity_conflict": "refused — identity conflict"}
# Every token the underscore rule does not produce is listed (RS §5; RQ, V19-A M-1); vocabulary_check() maps every
# outcome, request-kind and evidence-limit value of this file's schema through the chain.
RS_LIMIT = {"host_reachable_without_evidenced_A13": "host reachable without evidenced A13",
            "app_restart_interruption": "App-restart interruption", "dedup_scope_exceeded": "de-duplication scope exceeded",
            "agent_written_configuration": "agent-written configuration"}
RS_ROUTE = {"submission": "proposal", "observation": "proposal", "examination": "examination", "change_call": "direct"}


def rs_entries(r, n):
    """One RS operation_entry (RS §5) and one evidence_limit entry per limit (RS R11) for a dispatch record."""
    op = r["operation"]
    o = r["outcome"]
    body = {"operation": {"id": op.get("operation_identity", "not established (%s)" % op.get("not_established")),
                          **({"version": op["operation_version"]} if "operation_version" in op else {})},
            "authorType": "agent", "authorIdentity": {"value": "app-agent-seat:1", "verified": False},
            "channel": "external channel", "route": RS_ROUTE.get(r["request_kind"], "read"),
            "requestKind": r["request_kind"].replace("_", " "),
            "outcome": RS_OUTCOME.get(o["value"], o["value"].replace("_", " "))}
    if r.get("proposal_identity"):
        body["proposalId"] = r["proposal_identity"]
    if o["value"] == "outcome_unknown":
        body["observer"] = "App"
        body["lastObservedState"] = o["last_observed_state"]
    if o.get("reason"):
        body["reason"] = o["reason"]
    rid = "rec:app:sh1:%04d" % n
    out = [("operation_entry", body, rid)]
    for i, lim in enumerate(r["evidence_limits"], start=1):
        out.append(("evidence_limit", {"label": RS_LIMIT.get(lim, lim.replace("_", " ")), "subjectRef": rid}, f"{rid}.{i}"))
    return out


def rs_chain(recs):
    """Validate every dispatch record as RS entries with DEL-04-03's own validator and schema."""
    rs_proto = next(WORKING.parent.glob("PKG-04/DEL-04-03/Design/prototype"))
    sys.path.insert(0, str(rs_proto))
    import minischema                                           # noqa: E402  (DEL-04-03 prototype)
    import record_store                                          # noqa: E402
    reg = minischema.Registry()
    w4 = rs_proto.parents[2]
    for d, f in (("DEL-04-01", "ACT_POLICY_CLASS_RECORD.schema.json"), ("DEL-04-02", "AS_SETTINGS_IN.schema.json"),
                 ("DEL-04-03", "RS_RECORD.schema.json")):
        reg.load(str(next(w4.glob(d)) / "Design" / f))
    ref = {"$ref": record_store.RS_ID + "#/$defs/entry"}
    n_ok = n_all = 0
    errs = []
    seq = 0
    for i, r in enumerate(recs, start=1):
        for kind, body, rid in rs_entries(r, i):
            seq += 1
            e = {"format": "chirality.rs.record", "formatVersion": "0.1", "recordId": rid, "kind": kind,
                 "recorder": {"role": "App writer", "identity": "app-writer:local"}, "context": {"surface": "App"},
                 "runId": "run:sh1", "seq": seq, "writtenAt": f"w{seq:03d}", "observedAt": r["observed_at"], "body": body}
            v = minischema.validate(e, ref, reg)
            n_all += 1
            n_ok += not v
            if v:
                errs.append(f"{r['observed_at']} {kind}: {v[:1]}")
    return n_ok, n_all, errs


def vocabulary_check(ids, base):
    """RQ (V19-A M-1): every outcome value, request kind and evidence limit of external_dispatch_record.schema.json,
    not only those SH-1 emits, goes through rs_entries() and is validated as RS entries (rs_chain). The records are
    built from one SH-1 record with one value changed each; they test the vocabulary map, not ADAPTER's own rules."""
    props = ids[DISPATCH]["properties"]
    outcomes = props["outcome"]["properties"]["value"]["enum"]
    kinds = props["request_kind"]["enum"]
    limits = props["evidence_limits"]["items"]["enum"]
    recs = []
    for v in outcomes:
        r = copy.deepcopy(base)
        r["outcome"] = {"value": v, "reporter": "host", **({"last_observed_state": "queued"} if v == "outcome_unknown" else {})}
        r["evidence_limits"] = []
        r["observed_at"] = "VOC-outcome-" + v
        recs.append(r)
    for k in kinds:
        r = copy.deepcopy(base)
        r["request_kind"] = k
        r["evidence_limits"] = []
        r["observed_at"] = "VOC-kind-" + k
        recs.append(r)
    r = copy.deepcopy(base)
    r["evidence_limits"] = list(limits)
    r["observed_at"] = "VOC-limits"
    recs.append(r)
    n_ok, n_all, errs = rs_chain(recs)
    return len(outcomes), len(kinds), len(limits), n_ok, n_all, errs


def self_checks(reg, ids):
    """OBS-1b's item shape (R14-4) and CO-10/CO-11 shapes (no SH-1 step produces them)."""
    out = []
    m = Mapper()
    m.catalog = {"OP-C1": {"effects": {"kind": "none"}, "result": {"content_kinds": ["row"]}, "operation_version": "v1"}}
    base = {"run": "obs1b", "step": "OBS-1b", "path": "N-CLI", "thread": "th", "turn": "tu"}
    item = {"type": "commandExecution", "id": "call_1", "command": "/bin/zsh -lc 'sh1 cli call OP-C1 --json {}'",
            "source": "unifiedExecStartup", "status": "completed", "exitCode": 0, "aggregatedOutput": "not json\n"}
    r = m.map(dict(base, item=item, started={"source": "agent"}))
    out.append(("OBS-1b item: source agent at start, unifiedExecStartup at completion, wrapped once -> a dispatch, "
                "no compound-command limit",
                r is not None and r["native_source"] == {"at_start": "agent", "at_completion": "unifiedExecStartup"}
                and "dispatch_recognized_from_compound_command" not in r["evidence_limits"]
                and not validate(r, ids[DISPATCH], reg)))
    r2 = m.map(dict(base, item=dict(item, command="/bin/zsh -lc 'sh1 cli call OP-C1 --json {} ; echo x'"),
                    started={"source": "agent"}))
    out.append(("compound command keeps the limit", r2 is not None and "dispatch_recognized_from_compound_command" in r2["evidence_limits"]))
    out.append(("userShell at start is never a dispatch", m.map(dict(base, item=item, started={"source": "userShell"})) is None))
    co10 = {"observation_kind": "decided_item_not_applied", "exec_event": "CE-7", "source_record": "x", "proposal_identity": "PR-2",
            "item_identity": "1", "not_applied": {"accepted_by": "ACT-2", "result": "refused_stale", "relied_on_basis": "B1",
                                                  "current_basis": "B2"}, "observed_at": "T12x"}
    co11 = {"observation_kind": "request_recorded", "exec_event": "CE-4", "source_record": "x",
            "request": {"host_request_reference": "REQ-7", "act_kind": "A5", "subject": ["PR-2/1"], "purpose": "accept"},
            "observed_at": "T10r"}
    out.append(("CO-10 and CO-11 shapes validate", not validate(co10, ids[CHECKPOINT], reg) and not validate(co11, ids[CHECKPOINT], reg)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--write-examples", action="store_true")
    a = ap.parse_args()
    run = Path(a.run)
    reg, schemas = load_registry(SCHEMAS)
    ids = {s["$id"]: s for s in schemas.values()}
    m = Mapper()
    recs = [x for x in (m.map(json.loads(l)) for l in (run / "native_items.jsonl").read_text().splitlines()) if x]
    bad = 0
    print(f"{'step':10} {'path':5} {'kind':12} {'operation':10} {'status':10} {'outcome':26} {'reporter':16} limits")
    for r in recs:
        errs = validate(r, ids[DISPATCH], reg)
        bad += bool(errs)
        op = r["operation"].get("operation_identity", "-")
        print(f"{r['observed_at']:10} {r['path']:5} {r['request_kind']:12} {op:10} {r['native_status']:10} "
              f"{r['outcome']['value']:26} {r['outcome']['reporter']:16} {','.join(r['evidence_limits']) or '-'}"
              + (f"  SCHEMA FAIL {errs[:2]}" if errs else ""))
    obs = checkpoint_observations(recs)
    print(f"\nCheckpoint observations passed to DEL-02-03 ({len(obs)}):")
    for o in obs:
        errs = validate(o, ids[CHECKPOINT], reg)
        bad += bool(errs)
        detail = o.get("items") or o.get("item_identity") or o.get("last_observed_state") or ""
        print(f"  {o['observed_at']:8} {o['observation_kind']:22} -> {o['exec_event']:38} {o.get('proposal_identity', '')} {detail}"
              + (f"  SCHEMA FAIL {errs[:2]}" if errs else ""))
    chans = channel_statuses([json.loads(l) for l in (run / "channel_events.jsonl").read_text().splitlines()])
    print(f"\nChannel states ({len(chans)} events):")
    for runname, e, st in chans:
        errs = validate(st, ids[CHANNEL], reg)
        bad += bool(errs)
        print(f"  {runname:6} {e:36} -> {st['channel_state']:20} {st.get('disabled_sub_case', st.get('reason', ''))}"
              f"{' (unconfirmed)' if st.get('enablement_unconfirmed') else ''}" + (f"  SCHEMA FAIL {errs[:2]}" if errs else ""))
    expect = [("T10", "queued"), ("T13", "outcome_unknown"), ("T13o", "recorded_state"), ("PM-3", "refused_identity_conflict"),
              ("XF-34", "tool_execution_declined"), ("OM-CLI-2", "error"), ("XF-06", "endpoint_unavailable"),
              ("CH-0", "channel_not_enabled"), ("V-R1", "not_permitted")]
    got = {(r["observed_at"], r["outcome"]["value"]) for r in recs}
    for step, val in expect:
        ok = (step, val) in got
        bad += not ok
        print(f"{'PASS' if ok else 'FAIL'} mapping {step} -> {val}")
    for label, ok in self_checks(reg, ids):
        bad += not ok
        print(f"{'PASS' if ok else 'FAIL'} {label}")
    n_ok, n_all, errs = rs_chain(recs)
    bad += bool(errs)
    print(f"{'PASS' if not errs else 'FAIL'} RS-v0.8 receiving (R14-3): {len(recs)} dispatch records -> {n_ok} of {n_all} RS entries "
          f"(operation entries and R11 evidence limits) valid against RS_RECORD.schema.json" + (f"  {errs[:3]}" if errs else ""))
    n_o, n_k, n_l, v_ok, v_all, v_errs = vocabulary_check(ids, next(r for r in recs if r["observed_at"] == "T10"))
    bad += bool(v_errs)
    print(f"{'PASS' if not v_errs else 'FAIL'} RS-v0.8 §5 token map (RQ): every schema value -- {n_o} outcomes, {n_k} request "
          f"kinds, {n_l} evidence limits -> {v_ok} of {v_all} RS entries valid" + (f"  {v_errs[:3]}" if v_errs else ""))
    if a.write_examples:
        d = HERE.parent
        valid = next(r for r in recs if r["observed_at"] == "T10")
        (d / "external_dispatch_record.example-valid.json").write_text(json.dumps(valid, indent=2) + "\n")
        (d / "external_dispatch_record.example-valid-2.json").write_text(
            json.dumps(next(r for r in recs if r["observed_at"] == "T13"), indent=2) + "\n")
        inv = copy.deepcopy(next(r for r in recs if r["observed_at"] == "XF-34"))
        del inv["a14_record_reference"]
        (d / "external_dispatch_record.example-invalid.json").write_text(json.dumps(inv, indent=2) + "\n")
        q = next(o for o in obs if o["observation_kind"] == "proposal_queued")
        (d / "checkpoint_observation.example-valid.json").write_text(json.dumps(q, indent=2) + "\n")
        (d / "checkpoint_observation.example-valid-2.json").write_text(
            json.dumps(next(o for o in obs if o["observation_kind"] == "act_observed"), indent=2) + "\n")
        (d / "checkpoint_observation.example-invalid.json").write_text(json.dumps(q | {"exec_event": "CE-10"}, indent=2) + "\n")
        en = next(st for _, _, st in chans if st["channel_state"] == "enabled")
        (d / "channel_status.example-valid.json").write_text(json.dumps(en, indent=2) + "\n")
        inv = copy.deepcopy(en)
        del inv["host_enablement"]["capture_evidence_reference"]
        (d / "channel_status.example-invalid.json").write_text(json.dumps(inv, indent=2) + "\n")
        print("examples written")
    print(f"\nRecords: {len(recs)} dispatch, {len(obs)} checkpoint observations, {len(chans)} channel statuses")
    print("RESULT:", "all checks passed" if bad == 0 else f"{bad} failure(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
