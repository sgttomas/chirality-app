#!/usr/bin/env python3
"""EU-D1 builder: the source-file route (DEL-07-02 CFB-v0.2), PEC receiving
(DEL-07-01 PRC-v0.2), Domains receiving (DEL-08-01 DRC-v0.1) and the
connector witness's rehearsal records (DEL-09-10 CW-v0.2), from FX-EUD1 only.

Bounded prototype (owner O-D; R23-34, R23-40). Not product code. Python 3
standard library; no network; reads the fixture folder and the Design files,
writes only into OUTDIR.

Repair round 1 (RV2-EUD1; R23-40; owner findings OD-F1, OD-F2):
- EUD1-R1: CS-R2 restated; case P7 (Q1 asked at S, adopted and current,
  O-B1/O-C1 recorded READY) shows a relied report of the record that
  establishes no readiness to start, completion or permission.
- EUD1-R4: PR-5 compares content at the claim's citation, not revisions.
- OD-F1: PR-7, a record-tier citation must resolve (path, revision, anchor)
  or the claim's condition is `unknown`; case P8.
- EUD1-R5: BUILD_TIME and BUILD_DATE are constants of this deterministic
  build, labelled as such in every record, never as clock observations.
- EUD1-R6/R7: per-source fixture standing in EXP evidence; QC stays visibly
  a rehearsal.

Usage: python3 eud1.py FIXTURE_DIR OUTDIR
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXEC = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
PKG07 = os.path.join(EXEC, "PKG-07_PEC receiving and connector fallback", "1_Working")
D0701 = os.path.join(PKG07, "DEL-07-01_PEC first-consumer contract and adoption evidence", "Design")
D0702 = os.path.join(PKG07, "DEL-07-02_Connector limitation and source-file recovery paths", "Design")
D0801 = os.path.join(EXEC, "PKG-08_Domains research receiving", "1_Working",
                     "DEL-08-01_Domains query, admission and freshness contract", "Design")
D0910 = os.path.join(EXEC, "PKG-09_Candidate examination and connected journeys", "1_Working",
                     "DEL-09-10_Optional connector consumption witness")

S = "e4a0c2c4c369c9f85c3be4417e5815a4b4cb0abc"
R = "e086dfff32c0ddc5f3236dadf2dcb5795a518734"
WG = "projects/chirality-app-v4/execution/_Coordination/WorkGraphs/APP-V4-DESIGN-PASS-4-20261003/WORK_GRAPH.md"
# Constants of this deterministic build (EUD1-R5): never presented as clock observations.
BUILD_TIME = "2026-10-04T09:00:00Z"
BUILD_DATE = "2026-10-04"
PROHIBITED = ["no_work", "ready", "permitted", "correct_by_presence"]
CONDITION_ORDER = ["absent", "failing", "partial", "stale", "unknown", "current"]
RECORDER = {"kind": "tool", "identity": "O-D prototype eud1.py (EU-D1)"}
DELTA_IDS = ["c2", "c3", "c4", "c5", "c6", "c7"]
NOT_ESTABLISHED = {"conclusion": "Any item is ready to start, complete or permitted because of this connector material",
                   "why": "CS-R2: absence or limitation implies none of these, and a relied record-tier claim only reports what its cited record states at its pin"}

Q1 = {"id": "Q1",
      "text": ("For undertaking APP-V4-DESIGN-PASS-4-20261003 at revision e086dfff32: (a) which work-graph "
               "nodes are READY, ACTIVE or BLOCKED; (b) which other nodes are open (any state other than "
               "COMPLETE); (c) which nodes changed state or were added since revision e4a0c2c4c3?"),
      "scope": "loop/undertaking APP-V4-DESIGN-PASS-4-20261003 (PEC-ORI-001/002/005; R23-34 item 2)",
      "at_revision": R, "since_revision": S}
Q1S = {"id": "Q1-S",
       "text": ("For undertaking APP-V4-DESIGN-PASS-4-20261003 at revision e4a0c2c4c3: (a) which work-graph "
                "nodes are READY, ACTIVE or BLOCKED; (b) which other nodes are open (any state other than COMPLETE)?"),
       "scope": "as Q1, asked at the earlier revision (RV2 EUD1-R1; R23-40)",
       "at_revision": S}
QD = {"id": "QD",
      "text": ("Which admitted source supports the (invented) statement 'line EX-L1 support spacing is "
               "3.0 m', and does that support hold for the source as it stands now?"),
      "scope": "invented research material (EU-D1)",
      "at_revision": "sources as read at build time"}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def rd(path):
    with open(path, "rb") as f:
        return f.read()


def jload(path):
    return json.loads(rd(path))


def dump(obj):
    return (json.dumps(obj, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


# ------------------------------------------------------------ work graph
def parse_nodes(md_bytes):
    """Node rows of the '## Nodes' table: id, state token, state as written."""
    text = md_bytes.decode("utf-8")
    sec = text.split("## Nodes", 1)[1]
    nodes = []
    for line in sec.splitlines():
        if not line.startswith("| ") or line.startswith("| ID") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        node_id = cells[0].split()[0]
        state_written = cells[-1]
        nodes.append({"id": node_id, "state": state_written.split()[0], "state_written": state_written})
    return nodes


def wg_sources(fx):
    """The receiver's view of the cited file: revision -> bytes (only revisions it can read)."""
    srcs = jload(os.path.join(fx, "sources", "SOURCES.json"))["sources"]
    return srcs, {s["revision"]: rd(os.path.join(fx, s["file"])) for s in srcs}


def slug(heading):
    return "#" + re.sub(r"[^a-z0-9 -]", "", heading.lower()).strip().replace(" ", "-")


def resolve(citation, content):
    """PR-7: does a citation resolve in the receiver's sources? -> (status, why)."""
    path, rev, anchor = citation.get("path"), citation.get("sha"), citation.get("anchor")
    if not path or ":" in path.split("/")[0]:
        return "not_a_file", f"cites {path}, not a project file"
    if path != WG or rev not in content:
        return "not_comparable", f"revision {str(rev)[:10]} of {path} is not readable by the receiver"
    if anchor:
        heads = {slug(l.lstrip("#").strip()) for l in content[rev].decode("utf-8").splitlines() if l.startswith("#")}
        if anchor not in heads:
            return "anchor_missing", f"anchor {anchor} is not in {path} at {rev[:10]}"
    return "ok", "resolves"


def route_q1(fx, at=R, since=S):
    srcs, content = wg_sources(fx)
    by = {s["revision"]: s for s in srcs}
    nAt = parse_nodes(content[at])
    rab = [n for n in nAt if n["state"] in ("READY", "ACTIVE", "BLOCKED")]
    other_open = [n for n in nAt if n["state"] not in ("READY", "ACTIVE", "BLOCKED", "COMPLETE")]
    changes, removed = [], []
    if since:
        nS = parse_nodes(content[since])
        mS = {n["id"]: n for n in nS}
        for n in nAt:
            old = mS.get(n["id"])
            if old is None:
                changes.append({"node": n["id"], "from": None, "to": n["state_written"]})
            elif old["state_written"] != n["state_written"]:
                changes.append({"node": n["id"], "from": old["state_written"], "to": n["state_written"]})
        removed = [n["id"] for n in nS if n["id"] not in {m["id"] for m in nAt}]
    sid_at = "WG@R" if at == R else "WG@S"
    facts = [
        {"fact_id": "f-a", "statement": (f"The work graph at {at[:10]} marks no node READY, ACTIVE or BLOCKED" if not rab else
                                         f"The work graph at {at[:10]} marks: " + ", ".join(f"{n['id']} {n['state']}" for n in rab)),
         "source_id": sid_at, "anchor": "## Nodes", "data": {"nodes": [n["id"] for n in rab]}},
        {"fact_id": "f-b", "statement": f"Other open nodes at {at[:10]}: " + (", ".join(f"{n['id']} {n['state_written']}" for n in other_open) or "none"),
         "source_id": sid_at, "anchor": "## Nodes", "data": {"nodes": [n["id"] for n in other_open]}},
    ]
    if since:
        facts.append({"fact_id": "f-c", "statement": f"Changed or added since {since[:10]}: " + "; ".join(
            (f"{c['node']} added as {c['to']}" if c["from"] is None else f"{c['node']} {c['from']} -> {c['to']}") for c in changes)
            + ("; removed: " + ", ".join(removed) if removed else ""),
            "source_id": "WG@S", "anchor": "## Nodes (compared with WG@R)", "data": {"changes": changes, "removed": removed}})
    used = [by[r] for r in ([since, at] if since else [at])]
    unsupported = []
    if not rab and other_open:
        unsupported.append({"conclusion": "No work remains in the undertaking",
                            "why": f"{', '.join(n['id'] + ' ' + n['state'] for n in other_open)} at {at[:10]}; the absence of READY/ACTIVE/BLOCKED nodes is not empty work"})
    unsupported.append({"conclusion": "A node this file marks READY or PLANNED may be started, dispatched or treated as complete now",
                        "why": "this account reports what the work graph records at the asked revision; readiness to start, completion and permission are the coordinating role's, from current records (FV), not this account's"})
    account = {
        "format": "chirality.connector.route-account", "formatVersion": "0.1",
        "account_id": "ra:EUD1-Q1" if at == R else "ra:EUD1-Q1S",
        "question": Q1 if at == R else Q1S,
        "trigger": {"connector": "pec",
                    "why": ("PEC material did not support reliance for every part of Q1 (each condition P1-P6 and P8; for P1, part (b) is outside the declared coverage)"
                            if at == R else "Part (b) of Q1-S is outside PEC's orientation coverage (P7)"),
                    "receiving_records": ([f"pr:EUD1-P{i}" for i in (1, 2, 3, 4, 5, 6, 8)] if at == R else ["pr:EUD1-P7"])},
        "sources": [{"source_id": s["source_id"], "path": s["path"], "revision": s["revision"], "sha256": s["sha256"],
                     "role": "work graph at the asked revision" if s["revision"] == at else "work graph at the since-revision"} for s in used],
        "facts": facts,
        "gaps": [
            {"gap": "The node table names no owner per node; owners appear only in the 'Owners' table by deliverable", "effect": "Q1 does not ask for per-node owners; none is inferred", "responsible": "none needed for Q1"},
            {"gap": "The working tree may hold later, uncommitted bytes of the same file", "effect": f"answered at committed revision {at[:10]} only; nothing is said about uncommitted state", "responsible": "the asker, if a later revision is wanted"}],
        "conclusions": {
            "supported": [{"statement": f["statement"], "basis": "source_route", "refs": [f["source_id"]]} for f in facts],
            "unsupported": unsupported,
            "prohibited": list(PROHIBITED)},
        "duties": [
            {"duty": "locate_compare", "actor_role": "agent", "actor": "O-D (agent) running eud1.py", "standing": "performed",
             "evidence": "RUN_LOG.json", "reason": "located the committed revision(s) and read or compared the node tables"},
            {"duty": "review_integrate", "actor_role": "manager", "standing": "outstanding",
             "reason": "no manager (HELP_HUMAN in the WORKING_ITEMS function) has reviewed or integrated this account"},
            {"duty": "cross_undertaking_coordination", "actor_role": "person", "standing": "not_required",
             "reason": "the question concerns one undertaking in one repository"}],
        "recorder": RECORDER, "written_at": BUILD_TIME, "written_at_source": "build_constant"}
    truth = {"rab": [n["id"] for n in rab], "other_open": [n["id"] for n in other_open], "changes": changes, "removed": removed}
    return account, truth


# ------------------------------------------------------------ PEC receiving
def pec_record(fx, name, truth, asked=R, qid="Q1", route_ref="ra:EUD1-Q1"):
    raw = rd(os.path.join(fx, "pec", f"{name}.json"))
    inp = json.loads(raw)
    acct = jload(os.path.join(fx, "pec", "ADOPTION_ACCOUNT.json"))
    adopted = {a["release"]: a["feeds"] for a in acct["adopted"]}
    _, content = wg_sources(fx)
    terms = ["PEC response elements constructed from PEC-ORI-003/004/007 and DEL-04-03 CLM-003/019 (FX-EUD1)",
             "release identities and the adoption account are constructed; no PEC release or App adoption exists"]
    rec = {"format": "chirality.pec.receiving-record", "formatVersion": "0.1", "record_id": f"pr:EUD1-{name}",
           "question_id": qid, "simulated": True, "simulated_terms": terms,
           "input": {"kind": "no_response" if inp.get("observation") == "no_response" else "response",
                     "ref": f"FX-EUD1 pec/{name}.json", "sha256": sha(raw), "fixture_standing": "constructed"},
           "adoption": {"account_ref": "pec/ADOPTION_ACCOUNT.json (constructed OUT-004 account)", "release_adopted": False, "feeds_adopted": []},
           "recorder": RECORDER}
    if rec["input"]["kind"] == "no_response":
        rec.update({"release": {"identity": None, "stated_qualification": "not_stated"}, "stamp": None, "envelope_elements": None,
                    "response_standing": {"connector": "pec", "envelope": "unknown", "condition": "absent", "supports_reliance": False,
                                          "reasons": [{"facet": "condition", "value": "absent", "basis": inp["detail"]},
                                                      {"facet": "envelope", "value": "unknown", "basis": "no response, so no release or envelope to assess"}]},
                    "claims": []})
    else:
        rel = inp["release"]
        feeds_needed = ["work_graphs"]
        env = inp["envelope"]
        is_adopted = rel["identity"] in adopted and all(f in adopted[rel["identity"]] for f in feeds_needed)
        rec["adoption"].update({"release_adopted": rel["identity"] in adopted, "feeds_adopted": adopted.get(rel["identity"], [])})
        reasons = []
        envelope = "adopted" if is_adopted else "not_adopted"
        reasons.append({"facet": "envelope", "value": envelope,
                        "basis": (f"release {rel['identity']} and feed work_graphs are adopted in the OUT-004 account" if is_adopted
                                  else f"release {rel['identity']} ({rel['stated_qualification']}) is not adopted in the OUT-004 account")})
        conds = []
        if env["fallback_signal"] == "set":
            conds.append(("failing", "file-fallback signal set: " + "; ".join(f["limitation"] for f in env["feeds"] if f["limitation"])))
        if env["fallback_signal"] == "not_stated":
            conds.append(("unknown", "file-fallback signal not stated"))
        for f in env["feeds"]:
            if f["feed"] in feeds_needed and env["fallback_signal"] != "set" and (f["limitation"] or (f["coverage"] or "").startswith("partial")):
                conds.append(("partial", f"feed {f['feed']}: {f['limitation'] or f['coverage']}"))
        pin = env["pin"]
        if pin is None or pin not in content:
            conds.append(("unknown", "pin missing or not a revision the receiver can read"))
        elif content[pin] != content[asked]:
            conds.append(("stale", f"the cited file {WG} has different content at the pin {pin[:10]} than at the asked revision {asked[:10]}"))
        if not conds:
            conds.append(("current", f"the cited file has the same content at the pin {pin[:10]} as at the asked revision; no limitation; fallback signal clear"))
        condition = sorted(conds, key=lambda c: CONDITION_ORDER.index(c[0]))[0][0]
        for c, b in conds:
            reasons.append({"facet": "condition", "value": c, "basis": b})
        rec.update({"release": rel, "stamp": inp["stamp"],
                    "envelope_elements": {"pin": pin, "feeds": env["feeds"], "fallback_signal": env["fallback_signal"]},
                    "response_standing": {"connector": "pec", "envelope": envelope, "condition": condition,
                                          "supports_reliance": False, "reasons": reasons}})
        claims = []
        for c in inp["claims"]:
            tier = {"record": "record", "presence": "presence_advisory"}.get(c.get("tier"), "unknown")
            c_cond, why = condition, "response condition"
            if tier == "record" and condition == "current":
                status, rwhy = resolve(c["citation"], content)
                if status != "ok":
                    c_cond, why = "unknown", f"PR-7: {rwhy}"
                elif content[c["citation"]["sha"]] != content[asked]:
                    c_cond, why = "stale", "PR-5: the cited file's content at the citation differs from the asked revision"
            c_reasons = [{"facet": "envelope", "value": envelope, "basis": "response envelope"},
                         {"facet": "claim_tier", "value": tier, "basis": f"stated tier '{c.get('tier')}'"},
                         {"facet": "condition", "value": c_cond, "basis": why}]
            ok = envelope == "adopted" and c_cond == "current" and tier == "record"
            cl = {"claim_id": c["claim_id"], "statement": c["statement"], "citation": c["citation"], "stated_tier": c.get("tier"),
                  "standing": {"connector": "pec", "envelope": envelope, "condition": c_cond, "claim_tier": tier,
                               "supports_reliance": ok, "reasons": c_reasons}}
            if "heartbeat_age_s" in c:
                cl["heartbeat_age_s"] = c["heartbeat_age_s"]
            claims.append(cl)
        rec["claims"] = claims
        rec["response_standing"]["supports_reliance"] = any(c["standing"]["supports_reliance"] for c in claims) and condition == "current" and envelope == "adopted"
        if rec["response_standing"]["supports_reliance"]:
            rec["response_standing"]["claim_tier"] = "record"
    rec["conclusions"] = pec_conclusions(rec, truth, qid, route_ref)
    rec["route"] = {"needed": True, "account_ref": route_ref}
    return rec


def pec_conclusions(rec, truth, qid, route_ref):
    relied = {c["claim_id"]: c for c in rec["claims"] if c["standing"]["supports_reliance"]}
    sup, uns = [], []
    rs = rec["response_standing"]
    if "c1" in relied:
        pin = rec["envelope_elements"]["pin"][:10]
        sup.append({"statement": f"(a) PEC reports, from the work graph recorded at {pin}: {relied['c1']['statement']}",
                    "basis": "connector_reliance", "refs": [rec["record_id"] + "#c1"]})
    else:
        sup.append({"statement": f"(a) answered from the route account ({route_ref} f-a)", "basis": "source_route", "refs": [route_ref + "#f-a"]})
    sup.append({"statement": f"(b) answered from the route account ({route_ref} f-b): PEC orientation covers READY/ACTIVE/BLOCKED nodes only, so other open nodes are outside its coverage",
                "basis": "source_route", "refs": [route_ref + "#f-b"]})
    if qid == "Q1":
        deltas = [c for c in rec["claims"] if c["claim_id"] in DELTA_IDS]
        if deltas and all(c["standing"]["supports_reliance"] for c in deltas) and len(deltas) == len(truth["changes"]):
            sup.append({"statement": "(c) " + "; ".join(c["statement"] for c in deltas), "basis": "connector_reliance",
                        "refs": [rec["record_id"] + "#" + c["claim_id"] for c in deltas]})
        else:
            sup.append({"statement": f"(c) answered from the route account ({route_ref} f-c)", "basis": "source_route", "refs": [route_ref + "#f-c"]})
    if truth["other_open"] and not truth["rab"]:
        uns.append({"conclusion": "No work remains in the undertaking", "why": "no connector state or its absence establishes empty work; the route shows " + ", ".join(truth["other_open"]) + " open"})
    uns.append(dict(NOT_ESTABLISHED))
    if qid == "Q1-S" and "c1" in relied:
        uns.append({"conclusion": "O-B1 or O-C1 may be started or dispatched now because PEC reports them READY",
                    "why": "the relied claim reports what the work graph records at its pin (CS-R2 ii); readiness to start is decided by the coordinating role's rules from current project files (FV), not by a connector"})
    for c in rec["claims"]:
        if c["standing"]["claim_tier"] == "presence_advisory":
            uns.append({"conclusion": "Owner O-A is working on this undertaking, or any work state is correct because a session was active",
                        "why": f"claim {c['claim_id']} is a presence fact, advisory at its stated heartbeat age ({c.get('heartbeat_age_s')} s); presence is never correctness"})
        if c["standing"]["claim_tier"] == "record" and c["standing"]["condition"] == "unknown" and rs["condition"] == "current":
            uns.append({"conclusion": f"Claim {c['claim_id']} can be relied on", "why": c["standing"]["reasons"][-1]["basis"]})
    cond, env = rs["condition"], rs["envelope"]
    if env == "not_adopted":
        uns.append({"conclusion": "Any claim of this response can be relied on", "why": f"release {rec['release']['identity']} is not adopted by the App (OUT-004 account)"})
    if cond == "stale":
        uns.append({"conclusion": "The node states these claims report (for example VC or E ACTIVE, O-B1 or O-C1 READY) hold now",
                    "why": "the pin precedes a change to the cited work graph; the claims describe the earlier revision"})
    if cond == "partial":
        uns.append({"conclusion": "PEC's open-node statement or change list is complete", "why": "the work-graph feed states unparsed rows; claims cover the parsed rows only"})
    if cond == "failing":
        uns.append({"conclusion": "Any claim of this response can be relied on", "why": "the file-fallback signal is set: PEC reports it is failing its own checks"})
    if cond == "absent":
        uns.append({"conclusion": "Anything about the work graph from PEC", "why": "no response; total absence is handled by the receiver and the question goes to the route"})
    return {"supported": sup, "unsupported": uns, "prohibited": list(PROHIBITED)}


# ------------------------------------------------------------ Domains receiving
def src_revision(path):
    m = re.search(r"^revision:\s*(\S+)", rd(path).decode("utf-8"), re.M)
    return m.group(1) if m else None


def domains_record(fx, name):
    """Domains standing depends on Domains inputs only (independence, REQ-005 of DEL-07-02)."""
    raw = rd(os.path.join(fx, "domains", f"{name}.json"))
    inp = json.loads(raw)
    adm = jload(os.path.join(fx, "domains", "ADMISSION.json"))
    rec = {"format": "chirality.domains.receiving-record", "formatVersion": "0.1", "record_id": f"dr:EUD1-{name}",
           "question_id": "QD", "simulated": True,
           "simulated_terms": ["research sources, query contract DQC-EX-1 and admission ADM-1 are invented (FX-EUD1); no Domains provider exists (OI-023, OI-026)"],
           "input": {"kind": "no_response" if inp.get("observation") == "no_response" else "response",
                     "ref": f"FX-EUD1 domains/{name}.json", "sha256": sha(raw), "fixture_standing": "constructed"},
           "recorder": RECORDER}
    if rec["input"]["kind"] == "no_response":
        rec.update({"contract": {"identity": adm["contract"]["identity"], "established": adm["contract"]["established"]},
                    "index_basis": None, "results": [],
                    "response_standing": {"connector": "domains", "envelope": "unknown", "condition": "absent", "supports_reliance": False,
                                          "reasons": [{"facet": "condition", "value": "absent", "basis": inp["detail"]},
                                                      {"facet": "envelope", "value": "unknown", "basis": "no response"}]}})
        uns = [{"conclusion": "Any research context from Domains", "why": "no response; nothing is fabricated in its place (HOST §8.1)"}]
        sup = []
    else:
        envelope = "adopted" if adm["contract"]["established"] and inp["contract"] == adm["contract"]["identity"] else "not_adopted"
        admitted = {a["source_ref"]: a for a in adm["admitted"]}
        results, conds = [], []
        for r in inp["results"]:
            cur = src_revision(os.path.join(fx, r["source_ref"]))
            a = admitted.get(r["source_ref"])
            if a and r["admission"].get("state") == "admitted":
                tier = "admitted"
            elif r["admission"].get("state") == "not_admitted":
                tier = "located_not_admitted"
            else:
                tier = "unknown"
            cond = "unknown" if cur is None else ("current" if cur == r["indexed_revision"] else "stale")
            conds.append(cond)
            ok = envelope == "adopted" and cond == "current" and tier == "admitted"
            results.append({"result_id": r["result_id"], "source_ref": r["source_ref"], "indexed_revision": r["indexed_revision"],
                            "current_revision": cur, "admission": r["admission"],
                            "standing": {"connector": "domains", "envelope": envelope, "condition": cond, "claim_tier": tier,
                                         "supports_reliance": ok,
                                         "reasons": [{"facet": "condition", "value": cond, "basis": f"indexed {r['indexed_revision']}, source now {cur}"},
                                                     {"facet": "claim_tier", "value": tier, "basis": "admission as supplied and in the admission basis" if tier == "admitted" else "search hit without admission" if tier == "located_not_admitted" else "admission not stated"},
                                                     {"facet": "envelope", "value": envelope, "basis": "query contract established (constructed DQC-EX-1)" if envelope == "adopted" else "query contract not established"}]}})
        condition = sorted(conds, key=CONDITION_ORDER.index)[0] if conds else "unknown"
        rec.update({"contract": {"identity": inp["contract"], "established": envelope == "adopted"}, "index_basis": inp["index_basis"],
                    "results": results,
                    "response_standing": {"connector": "domains", "envelope": envelope, "condition": condition,
                                          "supports_reliance": any(r["standing"]["supports_reliance"] for r in results) and condition == "current",
                                          "reasons": [{"facet": "condition", "value": condition, "basis": "worst result condition"},
                                                      {"facet": "envelope", "value": envelope, "basis": "contract and admission basis"}]}})
        sup = [{"statement": "SRC-1 as it stands now (rev-B) states 2.4 m; that revision's admission is not established, so this is a source reading, not admitted research context",
                "basis": "source_route", "refs": ["ra:EUD1-QD#f-1"]}]
        uns = [{"conclusion": "An admitted source supports 'line EX-L1 support spacing is 3.0 m'",
                "why": "r1 (SRC-1) was admitted and indexed at rev-A, but SRC-1 is now rev-B and states 2.4 m (stale); r2 (SRC-2) is a search hit that was never admitted"},
               {"conclusion": "SRC-1 rev-B is admitted evidence", "why": "the admission basis ADM-1 covers rev-A only"}]
    rec["conclusions"] = {"supported": sup, "unsupported": uns, "prohibited": list(PROHIBITED)}
    rec["route"] = {"needed": True, "account_ref": "ra:EUD1-QD"}
    return rec


def route_qd(fx):
    def s(rel, role, sid):
        b = rd(os.path.join(fx, rel))
        return {"source_id": sid, "path": rel, "revision": src_revision(os.path.join(fx, rel)) or "not stated", "sha256": sha(b), "role": role}
    srcs = [s("domains/sources/SRC-1.md", "the source as it stands now", "SRC-1@now"),
            s("domains/sources/SRC-1@rev-A.md", "the revision the result set was built from", "SRC-1@rev-A"),
            s("domains/sources/SRC-2.md", "located, not admitted", "SRC-2@now")]
    adm = rd(os.path.join(fx, "domains", "ADMISSION.json"))
    srcs.append({"source_id": "ADM", "path": "domains/ADMISSION.json", "revision": "constructed", "sha256": sha(adm), "role": "admission basis (constructed)"})
    return {
        "format": "chirality.connector.route-account", "formatVersion": "0.1", "account_id": "ra:EUD1-QD", "question": QD,
        "trigger": {"connector": "domains", "why": "Domains result r1 is stale (indexed rev-A, source now rev-B) and r2 is not admitted; or Domains gave no response (DM-2)",
                    "receiving_records": ["dr:EUD1-DM-1", "dr:EUD1-DM-2"]},
        "sources": srcs,
        "facts": [
            {"fact_id": "f-1", "statement": "SRC-1 at rev-B states 'Line EX-L1 support spacing: 2.4 m (revised after the rev-A check)'", "source_id": "SRC-1@now", "anchor": "line 4"},
            {"fact_id": "f-2", "statement": "SRC-1 at rev-A stated 3.0 m", "source_id": "SRC-1@rev-A", "anchor": "line 4"},
            {"fact_id": "f-3", "statement": "The admission basis ADM-1 admits SRC-1 at rev-A only", "source_id": "ADM", "anchor": "admitted[0]"},
            {"fact_id": "f-4", "statement": "SRC-2 states 3.0 m and has no admission", "source_id": "SRC-2@now", "anchor": "line 4"}],
        "gaps": [{"gap": "No admission of SRC-1 rev-B", "effect": "no admitted source currently supports any spacing value for line EX-L1",
                  "responsible": "the admitting party for Domains sources, which is unallocated (OI-023, OI-026)"}],
        "conclusions": {
            "supported": [{"statement": "SRC-1 now (rev-B) states 2.4 m, read from the source; not admitted research context", "basis": "source_route", "refs": ["SRC-1@now"]}],
            "unsupported": [{"conclusion": "An admitted source supports 3.0 m", "why": "the admitted revision rev-A is superseded by rev-B, which says 2.4 m; SRC-2 is not admitted"},
                            {"conclusion": "2.4 m is admitted research context", "why": "rev-B's admission is not established"}],
            "prohibited": list(PROHIBITED)},
        "duties": [
            {"duty": "locate_compare", "actor_role": "agent", "actor": "O-D (agent) running eud1.py", "standing": "performed", "evidence": "RUN_LOG.json",
             "reason": "read SRC-1 at rev-A and rev-B, SRC-2 and the admission basis, and compared them"},
            {"duty": "review_integrate", "actor_role": "manager", "standing": "outstanding", "reason": "no manager has reviewed this account"},
            {"duty": "cross_undertaking_coordination", "actor_role": "person", "standing": "outstanding",
             "reason": "re-admission of SRC-1 rev-B lies with an admitting party outside this undertaking (unallocated); relaying that need is the person's"}],
        "recorder": RECORDER, "written_at": BUILD_TIME, "written_at_source": "build_constant"}



# ------------------------------------------------------------ DEL-09-10 rehearsal records
def criterion_identity(ac_id):
    text = rd(os.path.join(D0910, "ScopeOfWork.md")).decode("utf-8")
    line = next(l for l in text.splitlines() if l.startswith(f"- **{ac_id}**"))
    return "sha256:" + sha(line.encode("utf-8"))


REHEARSAL_LIMITS = [
    {"label": "rehearsal on constructed connector inputs; stands for no scenario or VER criterion (EXP-R3)", "vocabulary": "EXP"},
    {"label": "date is the build constant BUILD_DATE of eud1.py (deterministic build), not a clock observation", "vocabulary": "EXP"},
]


def exp_records(fx, out_files, check_results, date_value=BUILD_DATE):
    man = rd(os.path.join(fx, "MANIFEST.sha256")).decode().splitlines()
    digests = [f"sha256:{l.split()[0]} FX-EUD1 {l.split()[1]}" for l in man]
    subject = {"kind": "double", "double": "EU-D1 constructed connector inputs and real work-graph sources (FX-EUD1)", "file_digests": digests}
    srcs = {s["source_id"]: s for s in jload(os.path.join(fx, "sources", "SOURCES.json"))["sources"]}
    base = {"record_kind": "exam_result", "format": "EXP-v0.2",
            "support_revision": {"exp_version": "EXP-v0.2", "schema_id": "urn:chirality:app-v4:del-09-01:exam-result-record:0.2"},
            "activity": "verification", "run_basis": "rehearsal", "subject": subject,
            "configuration": {"codex_pin": "not_applicable", "route": {"kind": "model_only"}},
            "date": {"value": date_value, "source": "record_timestamp"}, "currency": {"state": "current"}}

    def ev(ref):
        """Per-source standing (EUD1-R6): connector records are built from constructed input; route
        accounts are derived from real committed bytes; the work graphs themselves are recorded."""
        if ref.startswith("sources/"):
            s = srcs[ref.split("/", 1)[1]]
            return {"ref": f"{s['path']} @ {s['revision'][:10]} (git show)", "digest": "sha256:" + s["sha256"],
                    "provenance": "static_inspection", "fixture_standing": "recorded"}
        e = {"ref": ref, "digest": "sha256:" + sha(out_files[ref]), "provenance": "test_definition"}
        if ref not in ("records/RA-Q1.json", "records/RA-Q1S.json"):
            e["fixture_standing"] = "constructed"
        return e

    def part(pid, expectation, ok, refs):
        return {"part": pid, "expectation": expectation, "outcome": "pass" if ok else "fail", "evidence": [ev(r) for r in refs]}

    q1src = ["sources/WG@S", "sources/WG@R"]
    cr = check_results
    r1 = dict(base, record_id="CW-EUD1-LC", case={"case_id": "CW-LC", "owner_deliverable": "DEL-09-10"},
              criterion={"source": "DEL-09-10 ScopeOfWork AC-002", "identity": criterion_identity("AC-002")},
              parts=[part("LC-1 absent (no response)", "PEC P6: condition absent, envelope unknown; no PEC conclusion; Q1 answered by the route; no prohibited conclusion", cr["P6"], ["records/PR-P6.json", "records/RA-Q1.json"] + q1src),
                     part("LC-2 stale", "PEC P3: condition stale; no claim relied on; the earlier node states named unsupported; Q1 answered by the route", cr["P3"], ["records/PR-P3.json", "records/RA-Q1.json"] + q1src),
                     part("LC-3 partial", "PEC P4: condition partial; completeness named unsupported; Q1 answered by the route", cr["P4"], ["records/PR-P4.json", "records/RA-Q1.json"] + q1src),
                     part("LC-4 failing", "PEC P5: condition failing; no claim relied on; Q1 answered by the route", cr["P5"], ["records/PR-P5.json", "records/RA-Q1.json"] + q1src),
                     part("LC-5 citation does not resolve", "PEC P8: claim c3's anchor is not in the cited file; c3 condition unknown, not relied on; (c) answered by the route", cr["P8"], ["records/PR-P8.json", "records/RA-Q1.json"] + q1src)],
              evidence=[{"ref": "RUN/D run_d.py output", "provenance": "test_definition"}],
              limits=list(REHEARSAL_LIMITS))
    r2 = dict(base, record_id="CW-EUD1-OC", case={"case_id": "CW-OC", "owner_deliverable": "DEL-09-10"},
              criterion={"source": "DEL-09-10 ScopeOfWork AC-003", "identity": criterion_identity("AC-003")},
              parts=[part("OC-1 PEC absent + Domains stale", "P6 absent and DM-1 stale each keep their own standing; DM-1's standing equals its standing with PEC present; both routes are followed", cr["OC-1"], ["records/PR-P6.json", "records/DR-DM-1.json", "records/RA-QD.json"]),
                     part("IA-2 PEC adopted-current + Domains absent", "P1 keeps its reliance; DM-2 absent gives no research context; neither changes the other", cr["IA-2"], ["records/PR-P1.json", "records/DR-DM-2.json"])],
              evidence=[{"ref": "RUN/D run_d.py output", "provenance": "test_definition"}],
              limits=list(REHEARSAL_LIMITS))
    r3 = dict(base, record_id="CW-EUD1-QC", case={"case_id": "CW-QC", "owner_deliverable": "DEL-09-10"},
              criterion={"source": "DEL-09-10 ScopeOfWork AC-001", "identity": criterion_identity("AC-001")},
              parts=[{"part": "QC-1 qualified joined trace", "expectation": "one actual source pin through qualified PEC extraction/response to the permitted App receiving action",
                      "outcome": "not-run", "not_run_because": "no qualified PEC release and no App adoption exist (DEP-002 unestablished at ffb2b6289; D108)"},
                     part("UQ-1 unqualified delivery reported as such", "PEC P2: envelope not_adopted; no claim relied on; reported as unqualified, not as a failed product demonstration", cr["P2"], ["records/PR-P2.json"]),
                     part("QA-1 adopted-current rehearsal", "PEC P1: claims c1-c7 relied on; presence claim c8 advisory; part (b) from the route", cr["P1"], ["records/PR-P1.json", "records/RA-Q1.json"] + q1src),
                     part("QA-2 relied report establishes no readiness", "PEC P7 (Q1 asked at S): c1 relied as a report of the work graph at its pin (O-B1, O-C1 READY); 'may be started now' and the CS-R2 conclusions listed unsupported", cr["P7"], ["records/PR-P7.json", "records/RA-Q1S.json", "sources/WG@S"])],
              missing_inputs=[{"input": "qualified, released PEC response for the selected question", "supplier": "PEC owning project (DEP-002)", "point_of_need": "before operational consumer reliance (OI-022)"},
                              {"input": "App release-level adoption of that release", "supplier": "App receiving owner (DEL-07-01 OUT-004; R23-34 item 7)", "point_of_need": "after a qualified PEC release exists"}],
              evidence=[{"ref": "RUN/D run_d.py output", "provenance": "test_definition"}],
              limits=list(REHEARSAL_LIMITS) + [{"label": "AC-001 is not examined: the joined witness is not run; the rehearsed parts show only the receiving rules on constructed input; do not read this record as a candidate result (EUD1-R7)", "vocabulary": "EXP"}])
    return [r1, r2, r3]


# ------------------------------------------------------------ build
def build(fx, out, date_value=BUILD_DATE):
    os.makedirs(out, exist_ok=True)
    files = {}
    ra1, truth = route_q1(fx)
    ras, truth_s = route_q1(fx, at=S, since=None)
    files["records/RA-Q1.json"] = dump(ra1)
    files["records/RA-Q1S.json"] = dump(ras)
    files["records/RA-QD.json"] = dump(route_qd(fx))
    recs = {}
    for i in (1, 2, 3, 4, 5, 6, 8):
        recs[f"P{i}"] = pec_record(fx, f"P{i}", truth)
        files[f"records/PR-P{i}.json"] = dump(recs[f"P{i}"])
    recs["P7"] = pec_record(fx, "P7", truth_s, asked=S, qid="Q1-S", route_ref="ra:EUD1-Q1S")
    files["records/PR-P7.json"] = dump(recs["P7"])
    for n in ("DM-1", "DM-2"):
        recs[n] = domains_record(fx, n)
        files[f"records/DR-{n}.json"] = dump(recs[n])
    files["RUN_LOG.json"] = dump({"tool": "eud1.py", "fixture_manifest_sha256": sha(rd(os.path.join(fx, "MANIFEST.sha256"))),
                                  "inputs_read": sorted(l.split()[1] for l in rd(os.path.join(fx, "MANIFEST.sha256")).decode().splitlines()),
                                  "build_time": BUILD_TIME, "build_time_source": "build constant (deterministic build; EUD1-R5)",
                                  "note": "Evidence that the locate_compare duty of ra:EUD1-Q1, ra:EUD1-Q1S and ra:EUD1-QD was performed by this tool run"})
    for rel, data in files.items():
        p = os.path.join(out, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as f:
            f.write(data)
    return files, recs, {"Q1": truth, "Q1-S": truth_s}


if __name__ == "__main__":
    fx, out = sys.argv[1], sys.argv[2]
    build(fx, out)
    print("EU-D1 records written to", out)
