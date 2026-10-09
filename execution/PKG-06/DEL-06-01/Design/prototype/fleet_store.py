"""DEL-06-01 fleet records: writer and reader (FLEET_RECORDS.md FR-v0.1 §6, §7). Prototype, not product code.

Python 3 standard library, plus the installed `jsonschema` for RF-5a only (DEL-07-02's standing schema uses
`if`/`then`, which the subset validator does not read). Validates records with DEL-04-03's subset validator
(minischema.py, read-only).
Layout of a fleet folder (PROPOSED for the prototype only; no placement is selected, FR §2 FR-D3):
  briefs/<briefId>.json          one brief per file, never edited (a changed brief is a new brief that supersedes)
  graphs/<undertaking>/r<n>.json  one work-graph revision per file, never edited
  coordination.fleet.jsonl       append-only: current_graph selectors and every coordination event
The writer refuses a record that does not validate (W-1) and never overwrites a file (exclusive create, W-2).
The reader derives per-item record facts with their sources (FR §6); it writes nothing. It reports every line it could
not read (RF-10, RF-11) and orphaned observations (RF-12), so that no consumer derives completeness from a partial log.
"""

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(HERE)
EXECUTION = os.path.normpath(os.path.join(DESIGN, "..", "..", ".."))
RS_PROTO = os.path.join(EXECUTION, "PKG-04",
                        "DEL-04-03", "Design", "prototype")
sys.path.insert(0, RS_PROTO)
from minischema import Registry, validate  # noqa: E402

VENDORED = os.path.join(HERE, "fixtures", "vendored", "EU-D1")


class VendoredInputChanged(Exception):
    pass


# FV10-R8: VENDOR.json is itself pinned, so a vendored file and its entry cannot be edited together unnoticed.
# Changing a vendored input is a deliberate re-pin: update VENDOR.json and this constant together.
VENDOR_SHA256 = "d02ffe5d90c2a96292f085194860313cbeb33e3fe26fa0a4355b8846d1ebe811"


def vendored(name):
    """R23-44: a vendored input's path, after checking VENDOR.json against VENDOR_SHA256 and the input's bytes against
    VENDOR.json (raises VendoredInputChanged if either differs)."""
    vpath = os.path.join(VENDORED, "VENDOR.json")
    with open(vpath, "rb") as fh:
        raw = fh.read()
    if hashlib.sha256(raw).hexdigest() != VENDOR_SHA256:
        raise VendoredInputChanged(f"VENDOR.json: sha256 {hashlib.sha256(raw).hexdigest()} differs from the pinned {VENDOR_SHA256}")
    pins = {f["file"]: f["sha256"] for f in json.loads(raw.decode("utf-8"))["files"]}
    path = os.path.join(VENDORED, name)
    with open(path, "rb") as fh:
        got = hashlib.sha256(fh.read()).hexdigest()
    if got != pins[name]:
        raise VendoredInputChanged(f"{name}: sha256 {got} differs from the pinned {pins[name]}")
    return path


def _standing_validator():
    import jsonschema
    with open(vendored("connector.standing.schema.json"), encoding="utf-8") as fh:
        s = json.load(fh)
    return jsonschema.Draft202012Validator({"$ref": "#/$defs/standing", "$defs": s["$defs"]})


def looks_like_connector_record(path):
    try:
        with open(path, encoding="utf-8") as fh:
            rec = json.load(fh)
        return isinstance(rec, dict) and "response_standing" in rec
    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        return False


def connector_need(root, need):
    """RF-5a (R23-39; RV2 FV10-R1, FV10-R3): a DECLARED connector need (kind 'connector', with its connector) is read
    from its receiving record's standing under DEL-07-02's vocabulary (vendored, R23-44), never by presence:
    missing record -> outstanding; unreadable, standing-less, nonconformant or other-connector record -> unknown;
    reliance supported -> satisfied (naming the source-file route where the record says one is still needed);
    condition unknown -> unknown (CS-R5); otherwise outstanding, with the route account."""
    ref, declared = need["ref"], need["connector"]
    base = {"connectorNeed": True, "connector": declared, "record": ref, "route": None}
    path = os.path.join(root, ref)
    if not os.path.isfile(path):
        return dict(base, state="outstanding", why=f"connector {declared}: receiving record {ref} not present")
    try:
        with open(path, encoding="utf-8") as fh:
            rec = json.load(fh)
    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        return dict(base, state="unknown", why=f"connector {declared}: receiving record {ref} unreadable (torn or not JSON)")
    if not isinstance(rec, dict) or not isinstance(rec.get("response_standing"), dict):
        return dict(base, state="unknown", why=f"connector {declared}: receiving record {ref} has no standing")
    st, rid = rec["response_standing"], rec.get("record_id", ref)
    route = rec.get("route") if isinstance(rec.get("route"), dict) else {}
    base.update(record=rid, route=route.get("account_ref"))
    errs = sorted(_standing_validator().iter_errors(st), key=str)
    if errs:
        return dict(base, state="unknown", why=f"connector record {rid}: standing does not conform to DEL-07-02's "
                                                  f"vocabulary ({errs[0].message[:80]}); not used")
    if st["connector"] != declared:
        return dict(base, state="unknown", why=f"connector record {rid} is from {st['connector']}, not the declared {declared}")
    facets = f"envelope {st['envelope']}, condition {st['condition']}" + \
        (f", claim tier {st['claim_tier']}" if "claim_tier" in st else "")
    reasons = "; ".join(f"{r['facet']} {r['value']}: {r['basis']}" for r in st["reasons"])
    if st["supports_reliance"]:
        # FV10-R7 (EUD1-R12): record-level reliance must not hide an unrelied claim. Each claim's own standing is read;
        # a record- or admitted-tier claim (or one whose tier is unknown) that does not support reliance is listed.
        # Without a route covering it, the need is unknown, not satisfied; presence-advisory claims are listed as advisory.
        validator = _standing_validator()
        unrelied, advisory = [], []
        for c in rec.get("claims") or []:
            cs = c.get("standing") if isinstance(c, dict) else None
            cid = c.get("claim_id", "?") if isinstance(c, dict) else "?"
            if not isinstance(cs, dict) or list(validator.iter_errors(cs)):
                unrelied.append(f"{cid} standing not readable or nonconformant")
            elif cs["connector"] != declared:
                # FV10-R9 (offered for closeout): a claim tagged with another connector is never counted as relied.
                unrelied.append(f"{cid} tagged {cs['connector']}, not the declared {declared}")
            elif not cs["supports_reliance"]:
                why = next((r["basis"] for r in cs["reasons"] if r["facet"] == "condition" and cs["condition"] != "current"), None) \
                    or next((r["basis"] for r in cs["reasons"] if r["facet"] == "claim_tier"), "")
                if cs.get("claim_tier") == "presence_advisory":
                    advisory.append(f"{cid} presence advisory")
                else:
                    unrelied.append(f"{cid} {cs['condition']}" + (f": {why}" if why else ""))
        notes = ""
        if unrelied and not route.get("needed"):
            return dict(base, state="unknown", unreliedClaims=unrelied, advisoryClaims=advisory,
                        why=f"connector record {rid} supports reliance at record level ({facets}), but claim(s) "
                            f"{'; '.join(unrelied)} do not, and the record names no source-file route for them")
        if unrelied:
            notes += f"; claim(s) not relied: {'; '.join(unrelied)}"
        if advisory:
            notes += f"; advisory only: {'; '.join(advisory)}"
        part = (f"; reliance covers only the record's covered parts: the source-file route {route.get('account_ref')} "
                f"is still needed for the rest" if route.get("needed") else "")
        return dict(base, state="satisfied", why=f"connector reliance supported ({st['connector']}: {facets}; {rid}){notes}{part}",
                    routeNeeded=bool(route.get("needed")), unreliedClaims=unrelied, advisoryClaims=advisory)
    state = "unknown" if st["condition"] == "unknown" else "outstanding"
    return dict(base, state=state,
                why=f"connector {st['connector']} does not support reliance ({facets}; {rid}): {reasons}"
                    + (f"; the source-file route is {route.get('account_ref')}" if route.get("account_ref") else "; no route account named"))


METHOD = "file content identity (method unselected; TEST VALUE: sha-256 of the file bytes)"


def schema():
    reg = Registry()
    sid = reg.load(os.path.join(DESIGN, "fleet.record.schema.json"))
    return reg, reg.by_id[sid]


def file_identity(path):
    if not os.path.isfile(path):
        return {"notObtainable": True, "reason": "file absent"}
    with open(path, "rb") as fh:
        return {"method": METHOD, "value": "sha256:" + hashlib.sha256(fh.read()).hexdigest()}


def dump(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=False)


class Refused(Exception):
    pass


class Writer:
    def __init__(self, root):
        self.root = root
        self.reg, self.schema = schema()
        os.makedirs(root, exist_ok=True)

    def _check(self, rec):
        errs = validate(rec, self.schema, self.reg)
        if errs:
            raise Refused(f"{rec.get('recordId')}: {errs[0]}")

    def _create(self, rel, data):
        path = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "x", encoding="utf-8") as fh:  # W-2: exclusive create, never overwrite
            fh.write(data)
        return path

    def brief(self, rec):
        self._check(rec)
        return self._create(f"briefs/{rec['body']['briefId'].split(':', 1)[1]}.json", dump(rec) + "\n")

    def graph(self, rec):
        self._check(rec)
        return self._create(f"graphs/{rec['undertaking']}/r{rec['body']['revision']}.json", dump(rec) + "\n")

    def log(self, rec):
        self._check(rec)
        with open(os.path.join(self.root, "coordination.fleet.jsonl"), "a", encoding="utf-8") as fh:
            fh.write(dump(rec) + "\n")


class Reader:
    """Derives record facts; never writes (FR §6 RF-9)."""

    def __init__(self, root, rs_records=None, rs_root=None):
        self.root = root
        self.reg, self.schema = schema()
        self.limits = []
        self.briefs, self.graphs, self.log = {}, {}, []
        self.unread_log = []      # RF-10: line numbers of coordination-log lines not read (torn or nonconformant)
        self.unread_rs = []       # RF-11: line numbers of RS lines not read
        for d, _, fs in os.walk(os.path.join(root, "briefs")):
            for f in sorted(fs):
                rec = self._read(os.path.join(d, f))
                if rec:
                    self.briefs[rec["body"]["briefId"]] = (rec, os.path.join(d, f))
        for d, _, fs in os.walk(os.path.join(root, "graphs")):
            for f in sorted(fs):
                rec = self._read(os.path.join(d, f))
                if rec:
                    self.graphs[rec["recordId"]] = (rec, os.path.join(d, f))
        lp = os.path.join(root, "coordination.fleet.jsonl")
        if os.path.exists(lp):
            with open(lp, encoding="utf-8") as fh:
                for n, line in enumerate(fh, 1):
                    if not line.strip():
                        continue
                    try:
                        rec = json.loads(line)
                    except json.JSONDecodeError:
                        self.limits.append(f"coordination log line {n}: partial entry (not read)")
                        self.unread_log.append(n)
                        continue
                    errs = validate(rec, self.schema, self.reg)
                    if errs:
                        self.limits.append(f"coordination log line {n}: nonconformant ({errs[0][:80]}); not used")
                        self.unread_log.append(n)
                        continue
                    self.log.append(rec)
        self.rs = []
        if rs_records:
            with open(rs_records, encoding="utf-8") as fh:
                for n, line in enumerate(fh, 1):
                    if not line.strip():
                        continue
                    try:
                        self.rs.append(json.loads(line))
                    except json.JSONDecodeError:
                        # RF-11 (RV E2-R2): a torn RS line is a limit; decisions it could hold become unknown.
                        self.limits.append(f"RS records line {n}: partial entry (not read)")
                        self.unread_rs.append(n)
        self.rs_root = rs_root

    def _read(self, path):
        try:
            with open(path, encoding="utf-8") as fh:
                rec = json.load(fh)
        except (json.JSONDecodeError, OSError):
            self.limits.append(f"{os.path.relpath(path, self.root)}: unreadable (not used)")
            return None
        errs = validate(rec, self.schema, self.reg)
        if errs:
            self.limits.append(f"{os.path.relpath(path, self.root)}: nonconformant ({errs[0][:80]}); not used")
            return None
        return rec

    def current_graph(self, undertaking):
        """RF-1: the latest current_graph selector in written order; its content must match the revision file."""
        sel = [r for r in self.log if r["kind"] == "current_graph" and r["undertaking"] == undertaking]
        if not sel:
            return None, ["no current graph selected"]
        s = sel[-1]["body"]
        rec_path = self.graphs.get(s["graph"])
        if not rec_path:
            return None, [f"selected graph {s['graph']} not found"]
        rec, path = rec_path
        notes = []
        if file_identity(path) != s["graphContent"]:
            notes.append("selected graph's content differs from the selector's: not used")
            return None, notes
        return rec, notes

    def events(self, kind, **match):
        return [r for r in self.log if r["kind"] == kind and all(r["body"].get(k) == v for k, v in match.items())]

    def _decision_state(self, request_id):
        """RF-6: a decision need, read from RS records (DEL-04-03): the act the package names, citing it."""
        req = next((e for e in self.rs if e.get("recordId") == request_id and e.get("kind") == "act_request"), None)
        if req is None:
            return "unknown", "request not in the supplied records" + (f" (RS line(s) {self.unread_rs} not read)" if self.unread_rs else "")
        kind = req["body"]["actKind"]
        alts = [a["id"] for a in req["body"].get("alternatives", [])]
        found = []
        for e in self.rs:
            b = e.get("body", {})
            if e.get("kind") == "human_act" and b.get("relations", {}).get("requestRef") == request_id and b.get("actKind") == kind:
                chosen = b["relations"].get("alternativeChosen")
                if kind == "A16" and chosen not in alts:
                    continue
                found.append(e)
        corrected = {e.get("corrects") for e in found if e.get("corrects")}
        current = [e for e in found if e["recordId"] not in corrected]
        if current:
            # R23-25: the latest act of the named kind on the package holds; earlier ones are superseded, not erased.
            e = current[-1]
            chosen = e["body"]["relations"].get("alternativeChosen")
            return "satisfied", f"{e['recordId']} ({kind}{', ' + chosen if chosen else ''})"
        if self.unread_rs:
            return "unknown", f"no decision found on {request_id}, but RS line(s) {self.unread_rs} were not read"
        return "outstanding", f"decision pending on {request_id}"

    def item_facts(self, undertaking):
        graph, notes = self.current_graph(undertaking)
        if graph is None:
            return {"undertaking": undertaking, "items": [], "notes": notes, "limits": self.limits}
        items = {i["itemId"]: i for i in graph["body"]["items"]}
        out = []
        for iid, it in items.items():
            f = {"itemId": iid, "outcome": it["outcome"], "selected": it["selected"], "owner": it["owner"],
                 "brief": None, "dispatch": None, "observed": [], "return": None, "review": None,
                 "integration": None, "related": [], "external": None, "needs": []}
            # RF-2 brief: prepared is never dispatched.
            if it.get("brief"):
                b = self.briefs.get(it["brief"])
                f["brief"] = {"state": "prepared" if b else "named in graph, not found", "brief": it["brief"]}
            # RF-3 dispatch: only from an App-written dispatch_observed associating this brief.
            disp = [e for e in self.events("dispatch_observed") if e["body"]["association"].get("brief") == it.get("brief")] if it.get("brief") else []
            if disp:
                d = disp[-1]["body"]
                f["dispatch"] = {"state": "dispatch observed", "child": d["childThread"], "parent": d["parentThread"],
                                 "association": d["association"]["state"], "source": disp[-1]["recordId"]}
                for c in [d["childThread"]]:
                    obs = self.events("child_observed", childThread=c)
                    end = self.events("observation_ended", childThread=c)
                    f["observed"] = [{"status": o["body"]["status"], "source": o["body"]["observation"]["source"]} for o in obs]
                    if end:
                        f["observed"].append({"ended": end[-1]["body"]["cause"], "lastObserved": end[-1]["body"]["lastObserved"]})
            elif it.get("brief"):
                f["dispatch"] = {"state": "no dispatch observed"}
            # RF-4 return, review, integration: each only from its own record.
            rets = self.events("return_recorded", workItem=iid)
            if rets:
                r = rets[-1]
                f["return"] = {"state": "returned", "by": r["body"]["returnedBy"]["identity"],
                               "recordedBy": r["recorder"]["identity"], "source": r["recordId"]}
                revs = [e for e in self.events("review_recorded", workItem=iid) if e["body"]["returnRef"] == r["recordId"]]
                if revs:
                    f["review"] = {"verdict": revs[-1]["body"]["verdict"], "by": revs[-1]["body"]["reviewer"]["identity"], "source": revs[-1]["recordId"]}
                ints = [e for e in self.events("integration_recorded", workItem=iid) if e["body"]["returnRef"] == r["recordId"]]
                if ints:
                    f["integration"] = {"state": "integrated", "by": ints[-1]["body"]["integrator"]["identity"], "source": ints[-1]["recordId"]}
            ext = self.events("external_result", workItem=iid)
            if ext:
                f["external"] = {"owner": ext[-1]["body"]["owner"]["identity"], "result": [x["ref"] for x in ext[-1]["body"]["result"]],
                                 "mechanism": ext[-1]["body"].get("mechanism", "not stated")}
            f["related"] = [{"thread": e["body"]["thread"], "relation": e["body"]["relation"], "source": e["body"]["source"]}
                            for e in self.events("related_conversation", workItem=iid)]
            # RF-5/RF-6 needs, each with the state its source supports.
            for n in it["needs"]:
                if n["kind"] == "item":
                    other = items.get(n["ref"])
                    ints = [e for e in self.log if e["kind"] == "integration_recorded" and e["body"]["workItem"] == n["ref"]]
                    exts = [e for e in self.log if e["kind"] == "external_result" and e["body"]["workItem"] == n["ref"]]
                    state = ("satisfied", "integrated") if ints else ("satisfied", "external result") if exts else \
                        ("outstanding", "not integrated") if other else ("unknown", "item not in the current graph")
                elif n["kind"] == "decision":
                    state = self._decision_state(n["ref"])
                elif n["kind"] == "connector":
                    # RF-5a (R23-39; FV10-R1): a declared connector need, read from its standing, never by presence.
                    f["needs"].append(dict({"need": n}, **connector_need(self.root, n)))
                    continue
                else:
                    p = os.path.join(self.root, n["ref"])
                    if os.path.exists(p) and looks_like_connector_record(p):
                        # RF-5b (FV10-R1): a connector record named as a plain input is not read by presence.
                        state = ("unknown", f"{n['ref']} is a connector receiving record named as a plain input; "
                                            f"declare it as a connector need")
                    else:
                        state = ("satisfied", "input present") if os.path.exists(p) else ("outstanding", "input not present")
                f["needs"].append({"need": n, "state": state[0], "why": state[1]})
            # RF-7 basis changes naming this item.
            f["basisChanged"] = [e["recordId"] for e in self.log if e["kind"] == "basis_changed" and iid in e["body"]["affectedItems"]]
            out.append(f)
        # RF-8 the child index (R23-4): every child the log observed, associated or not.
        index = [{"child": e["body"]["childThread"], "parent": e["body"]["parentThread"],
                  "association": e["body"]["association"]["state"], "brief": e["body"]["association"].get("brief")}
                 for e in self.events("dispatch_observed")]
        # RF-12 (RV E2-R1): orphans, an observation of a child whose dispatch the log does not hold, are limits.
        dispatched = {e["body"]["childThread"] for e in self.events("dispatch_observed")}
        orphans = sorted({e["body"]["childThread"] for e in self.log
                          if e["kind"] in ("child_observed", "observation_ended") and e["body"]["childThread"] not in dispatched})
        for c in orphans:
            self.limits.append(f"child {c} observed with no dispatch_observed in the log: a dispatch record may be missing")
        return {"undertaking": undertaking, "graph": graph["recordId"], "revision": graph["body"]["revision"],
                "logIncomplete": list(self.unread_log), "orphanChildren": orphans,
                "items": out, "childIndex": index, "notes": notes, "limits": self.limits}
