"""Early path E: one decision package decided by the person, checked end to end.

Prototype only (LOOP_INIT "bounded implementation and connected tests"). Python 3
standard library. Reuses DEL-04-03's subset validator (prototype/minischema.py) read-only.
Writes only to the scratch folder given as the first argument (default: a new temp folder).

Parts:
  A  the fixture against the schema files as they are (RS, EXEC CE-4/CE-10, AAC), now that
     PR-1...PR-13 are applied in those files (R23-18): each row present, every record and
     object valid, the capture/offer/record agreement, and invalid cases INV-E-1...7;
  C  RS's own A16 cases (INV-RS-25...28) and the A16 act-log entry;
  D  the decision view derived from the input set (decision_view.py), its expected rows,
     reader-rule cases RV-1...RV-7 on mutated copies in scratch, and input hashes unchanged.
"""

import copy
import hashlib
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
EXECUTION = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
REPO = os.path.normpath(os.path.join(EXECUTION, "..", "..", ".."))
RS_DIR = os.path.join(EXECUTION, "PKG-04_Human acts, autonomy and run evidence", "1_Working",
                      "DEL-04-03_Content-bound decisions and compact run records", "Design")
sys.path.insert(0, os.path.join(RS_DIR, "prototype"))
sys.path.insert(0, HERE)
from minischema import Registry, validate, check_supported  # noqa: E402
import decision_view  # noqa: E402
sys.path.insert(0, os.path.join(EXECUTION, "PKG-02_Workflow and role portability", "1_Working",
                                "DEL-02-03_Workflow execution compatibility and round-trip support", "Design", "prototype"))
from run_all import request_from_file  # noqa: E402

FX = os.path.join(HERE, "fixtures", "FX-DP1")
RESULTS = []


def check(cond, label):
    RESULTS.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + label)


def load_json(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def log(p):
    with open(p, encoding="utf-8") as fh:
        return [json.loads(l) for l in fh if l.strip()]


def tree_hashes(root):
    out = {}
    for d, _, fs in os.walk(root):
        for f in fs:
            p = os.path.join(d, f)
            with open(p, "rb") as fh:
                out[os.path.relpath(p, root)] = hashlib.sha256(fh.read()).hexdigest()
    return out


def pointer(doc, ptr):
    node = doc
    for part in [p for p in ptr.split("/") if p]:
        node = node[int(part)] if isinstance(node, list) else node[part.replace("~1", "/").replace("~0", "~")]
    return node


def registry():
    reg = Registry()
    rs_id = reg.load(os.path.join(RS_DIR, "RS_RECORD.schema.json"))
    rs = reg.by_id[rs_id]
    ref = rs["$defs"]["actRequest"]["$ref"].partition("#")[0]
    exec_schema = reg.resolve_file(ref, rs)
    as_dir = os.path.join(EXECUTION, "PKG-04_Human acts, autonomy and run evidence", "1_Working",
                          "DEL-04-02_Visible autonomy and result standing", "Design")
    reg.load(os.path.join(as_dir, "AS_SETTINGS_IN.schema.json"))
    rows = load_json(os.path.join(HERE, "proposed_rows.json"))
    aac_offer = reg.by_id[reg.load(os.path.join(REPO, rows["files"]["AAC_OFFER"]))]
    aac_cap = reg.by_id[reg.load(os.path.join(REPO, rows["files"]["AAC_CAPTURE"]))]
    return reg, rs, {"EXEC": exec_schema, "AAC_OFFER": aac_offer, "AAC_CAPTURE": aac_cap}, rows


def a16_lapsed(act):
    """The act_lapsed entry the writer records when PKG-1 changes after the decision (RS §7 L-6; RV-2)."""
    return {"format": "chirality.rs.record", "formatVersion": "0.1", "recordId": "rec:app:coord:0006",
            "kind": "act_lapsed", "recorder": {"role": "App writer", "identity": "app-writer:local"},
            "context": {"surface": "App"}, "seq": 6, "writtenAt": "w006",
            "body": {"act": {"recordId": act["recordId"], "actKind": "A16", "capturedAt": act["body"]["captureTime"],
                             "capturingSurface": "app_act_control"},
                     "state": "lapsed", "referents": [act["body"]["boundSubject"][0]],
                     "c0": act["body"]["boundContent"][0],
                     "c1": {"method": act["body"]["boundContent"][0]["method"], "value": "sha256:changed (TEST VALUE)"},
                     "time": "t6"}}


def canon_independent(v):
    """AAC-v0.3 §5.1 aac-offer-digest/0.1 written from its text, not from Python's json module (RV E1-R4)."""
    if isinstance(v, dict):
        return "{" + ",".join(canon_independent(k) + ":" + canon_independent(v[k]) for k in sorted(v)) + "}"
    if isinstance(v, list):
        return "[" + ",".join(canon_independent(x) for x in v) + "]"
    if isinstance(v, bool):
        return "true" if v else "false"
    if v is None:
        return "null"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        raise ValueError("aac-offer-digest/0.1 is not defined over a non-integer number")
    short = {'"': '\\"', "\\": "\\\\", "\b": "\\b", "\f": "\\f", "\n": "\\n", "\r": "\\r", "\t": "\\t"}
    out = []
    for ch in v:
        if ch in short:
            out.append(short[ch])
        elif ord(ch) < 0x20:
            out.append("\\u%04x" % ord(ch))
        else:
            out.append(ch)
    return '"' + "".join(out) + '"'


def digest_independent(offer):
    body = {k: x for k, x in offer.items() if k != "offerDigest"}
    return hashlib.sha256(canon_independent(body).encode("utf-8")).hexdigest()


def main():
    scratch = sys.argv[1] if len(sys.argv) > 1 else tempfile.mkdtemp(prefix="early-path-")
    os.makedirs(scratch, exist_ok=True)
    before = tree_hashes(FX)
    records = log(os.path.join(FX, "records", "coordination.rs.jsonl"))
    offer = load_json(os.path.join(FX, "aac", "offer-PKG-1.json"))
    cap = load_json(os.path.join(FX, "aac", "cap-decide-PKG-1.json"))

    # ---- A: the schema files as they are (PR-1...PR-13 applied in the files under R23-18)
    print("== A: the fixture against the schema files as they are ==")
    reg, rs, sch, rows = registry()
    for name, s in sch.items():
        check_supported(s, name)
    check(True, "A the RS, EXEC CE-4/CE-10 and AAC schemas load within the validator's keyword subset")
    for r in rows["rows"]:
        node = pointer(sch[r["file"]], r["pointer"] if r["op"] != "add-property" else r["pointer"] + "/" + r["name"])
        if r["op"] == "append-enum":
            present = r["value"] in node
        elif r["op"] == "add-property":
            # Descriptions may carry later notes (R23-24 added the file mapping to PR-3/PR-4's); the constraints must match.
            strip = lambda x: {k: v for k, v in x.items() if k != "description"}
            present = strip(node) == strip(r["value"]) and node.get("description", "").startswith(r["value"].get("description", ""))
        else:  # a rule: PR-5 is written as anyOf for EXEC's subset checker; PR-9, PR-12 as allOf entries
            present = any(("A16" in (x.get("description") or "")) or ("PR-5" in (x.get("description") or ""))
                          for x in node.get("allOf", []) + node.get("anyOf", []))
        check(present, f"A {r['id']} present in the file ({r['op']} at {r['pointer']})")
    for e in records:
        errs = validate(e, rs, reg)
        check(not errs, f"A {e['recordId']} {e['kind']} valid {errs[:1]}")
    check(not validate(a16_lapsed(records[2]), rs, reg), f"A act_lapsed of the A16 valid {validate(a16_lapsed(records[2]), rs, reg)[:1]}")
    check(not validate(offer, sch["AAC_OFFER"], reg), f"A offer-PKG-1 valid {validate(offer, sch['AAC_OFFER'], reg)[:1]}")
    check(not validate(cap, sch["AAC_CAPTURE"], reg), f"A cap-decide-PKG-1 valid {validate(cap, sch['AAC_CAPTURE'], reg)[:1]}")
    od = {k: v for k, v in offer.items() if k != "offerDigest"}
    recomputed = hashlib.sha256(json.dumps(od, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
                                .encode("utf-8")).hexdigest()
    check(offer["offerDigest"] == {"method": "aac-offer-digest/0.1", "value": recomputed} and cap["offerDigest"] == offer["offerDigest"],
          "A offerDigest recomputes from the offer file alone under AAC-v0.3 §5.1 (aac-offer-digest/0.1), and the capture carries it")
    check(digest_independent(offer) == offer["offerDigest"]["value"] and "\u2028" in json.dumps(offer, ensure_ascii=False)
          and "Prüfung" in json.dumps(offer, ensure_ascii=False),
          "A E1-R4 an implementation written from §5.1's text (not Python's json) gives the same digest over an offer with ü, ≈ and U+2028")
    aac_a4 = load_json(os.path.join(REPO, rows["files"]["AAC_OFFER"].replace("aac.offer.schema.json", "aac.offer.example.valid.json")))["instances"][0]
    check(canon_independent({k: x for k, x in aac_a4.items() if k != "offerDigest"}).encode("utf-8")
          == json.dumps({k: x for k, x in aac_a4.items() if k != "offerDigest"}, sort_keys=True, separators=(",", ":"),
                        ensure_ascii=False).encode("utf-8") and isinstance(aac_a4["answers"]["arrival"]["arrivalOrdinal"], int),
          "A E1-R4 integers (the A4 example's arrivalOrdinal) serialize identically under both implementations")
    exec_s = sch["EXEC"]
    pkg_def = exec_s["$defs"]["decisionPackageFile"]
    for name in ("PKG-1", "PKG-2"):
        path = os.path.join(FX, "project", "decisions", name + ".json")
        pkg = load_json(path)
        errs = validate(pkg, pkg_def, reg, exec_s)
        check(not errs, f"A R23-24 {name}.json validates against DEL-02-03 $defs/decisionPackageFile {errs[:1]}")
        req = next(e for e in records if e["kind"] == "act_request" and e["body"]["evidence"]["ref"] == f"project/decisions/{name}.json")
        with open(path, "rb") as fh:
            ident = "sha256:" + hashlib.sha256(fh.read()).hexdigest()
        rebuilt = request_from_file(pkg, req["body"]["evidence"]["ref"], ident, req["body"]["requester"], req["body"]["time"])
        check(rebuilt == req["body"], f"A R23-24 {name}: the act_request is the stated mapping of the file, and its evidence is the file's identity")
    bad = load_json(os.path.join(FX, "project", "decisions", "PKG-1.json")); bad["evidence"] = req["body"]["evidence"]
    check(validate(bad, pkg_def, reg, exec_s), "A R23-24 a package file carrying a recorder element (evidence) is refused")
    # cross-object agreement the schemas cannot see
    act = records[2]
    check(cap["recordId"] == act["recordId"] and cap["captureId"] == act["body"]["captureEvidence"][0]["ref"]
          and cap["alternativeChosen"] == act["body"]["relations"]["alternativeChosen"]
          and cap["boundContent"] == act["body"]["boundContent"] and cap["requestRef"] == offer["requestRef"]
          == act["body"]["relations"]["requestRef"],
          "A capture evidence, offer and A16 record agree (record id, capture ref, request, chosen alternative, bound content)")
    # invalid cases, each must fail for its stated reason
    pkg_req = records[0]
    inv = []
    x = copy.deepcopy(pkg_req); del x["body"]["consequences"]; inv.append(("INV-E-1 package without consequences", x, rs))
    x = copy.deepcopy(pkg_req); x["body"]["form"] = "supplier person-input request"; inv.append(("INV-E-2 alternatives on a request that is not a package", x, rs))
    x = copy.deepcopy(pkg_req); x["body"]["alternatives"] = x["body"]["alternatives"][:1]; inv.append(("INV-E-3 package with one alternative", x, rs))
    x = copy.deepcopy(cap); del x["alternativeChosen"]; inv.append(("INV-E-4 A16 capture without the chosen alternative", x, sch["AAC_CAPTURE"]))
    x = copy.deepcopy(offer); x["declineAvailable"] = True; inv.append(("INV-E-5 A16 offer offering a decline", x, sch["AAC_OFFER"]))
    x = copy.deepcopy(cap); x["choice"] = "decline"; inv.append(("INV-E-6 A16 capture with choice decline", x, sch["AAC_CAPTURE"]))
    x = copy.deepcopy(offer); x["actKind"] = "A4"; x["wording"] = "mark checked"; x["declineAvailable"] = True; inv.append(("INV-E-7 alternatives on an A4 offer", x, sch["AAC_OFFER"]))
    for name, inst, schema in inv:
        errs = validate(inst, schema, reg)
        check(errs, f"A {name}: invalid as expected -> {errs[0][:110] if errs else 'VALID (unexpected)'}")

    # ---- C: RS's own A16 cases on the files as they are
    print("\n== C: RS A16 rows on the files as they are ==")
    reg, rs, sch, rows = registry()
    for c in load_json(os.path.join(RS_DIR, "RS_RECORD.invalid.examples.json")):
        if c["case"] in ("INV-RS-25", "INV-RS-26", "INV-RS-27", "INV-RS-28"):
            errs = validate(c["instance"], rs, reg)
            check(errs, f"C {c['case']} invalid as expected -> {errs[0][:90] if errs else ''}")
    a16 = [e for e in log(os.path.join(RS_DIR, "RS_RECORD.valid.act-log.example.jsonl")) if e["body"].get("actKind") == "A16"]
    check(len(a16) == 1 and not validate(a16[0], rs, reg), "C the act-log example's A16 entry is valid")

    # ---- D: the decision view
    print("\n== D: the decision view, derived from the input set ==")
    view = decision_view.derive(FX, ["records/coordination.rs.jsonl"])
    with open(os.path.join(scratch, "decision-view.FX-DP1.json"), "w", encoding="utf-8") as fh:
        json.dump(view, fh, ensure_ascii=False, indent=2)
    r = {row["package"]: row for row in view["rows"]}
    p1, p2 = r.get("rec:app:coord:0001"), r.get("rec:app:coord:0002")
    check(len(view["rows"]) == 2 and not view["limits"], "D two package rows, no read limits")
    check(p1 and p1["state"] == "decided" and p1["decision"]["alternativeChosen"] == "ALT-2"
          and p1["decision"]["lapse"] == "not lapsed" and not p1["limits"],
          "D PKG-1 decided: ALT-2, not lapsed, no limits")
    check(p1 and "identity not verified" in p1["decision"]["decidedBy"]
          and p1["decision"]["recordedBy"].startswith("App interface (capturing surface)"),
          "D PKG-1 shows the decision actor (identity not verified) apart from the recorder")
    check(p1 and all(a["consequences"] for a in p1["alternatives"]), "D PKG-1 shows each alternative with its consequences")
    check(p2 and p2["state"].startswith("pending") and p2["decision"] is None,
          "D PKG-2 pending: the agent's message claiming a decision is not a record and changes nothing (RV-4)")

    def variant(name, mutate):
        root = os.path.join(scratch, name)
        if os.path.exists(root):
            shutil.rmtree(root)
        shutil.copytree(FX, root)
        mutate(root)
        return {row["package"]: row for row in decision_view.derive(root, ["records/coordination.rs.jsonl"])["rows"]}

    def add_act(root, alt, kind="A16", rid="rec:app:coord:0004"):
        p = os.path.join(root, "records", "coordination.rs.jsonl")
        e = copy.deepcopy(records[2])
        e.update(recordId=rid, seq=4, writtenAt="w004")
        e["body"]["actKind"] = kind
        e["body"]["relations"] = {"requestRef": "rec:app:coord:0002", "alternativeChosen": alt} if kind == "A16" \
            else {"requestRef": "rec:app:coord:0002"}
        if kind != "A16":
            e["body"]["actClass"] = {"value": "reserved to the person"}
        with open(p, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(e, ensure_ascii=False) + "\n")

    v = variant("RV-1", lambda root: add_act(root, "ALT-9"))
    check(v["rec:app:coord:0002"]["state"].startswith("pending")
          and any("not one the package names" in l for l in v["rec:app:coord:0002"]["limits"]),
          "RV-1 an A16 choosing an alternative the package does not name is not counted; shown with its rule")

    def edit_pkg(root):
        with open(os.path.join(root, "project", "decisions", "PKG-1.json"), "a", encoding="utf-8") as fh:
            fh.write(" ")
    v = variant("RV-2", edit_pkg)
    check(v["rec:app:coord:0001"]["decision"]["lapse"].startswith("lapsed")
          and any("differs" in l for l in v["rec:app:coord:0001"]["limits"]),
          "RV-2 the package file changed after the decision: the decision shows lapsed (RS §7 L-6)")
    v = variant("RV-3", lambda root: os.remove(os.path.join(root, "project", "decisions", "PKG-1.json")))
    check(v["rec:app:coord:0001"]["decision"]["lapse"] == "unknown (unavailable)",
          "RV-3 the package file is absent: lapse unknown (unavailable), the decision still shown from its record")
    v = variant("RV-5", lambda root: add_act(root, None, kind="A4"))
    check(v["rec:app:coord:0002"]["state"].startswith("pending")
          and any("not the A16" in l for l in v["rec:app:coord:0002"]["limits"]),
          "RV-5 an act of another kind citing the package is not its decision")
    v = variant("RV-6", lambda root: add_act(root, "ALT-1"))
    check(v["rec:app:coord:0002"]["state"] == "decided" and v["rec:app:coord:0002"]["decision"]["alternativeChosen"] == "ALT-1",
          "RV-6 a recorded A16 on PKG-2 decides it (positive control for RV-1 and RV-5)")

    def second_a16(root, corrects=False):
        p = os.path.join(root, "records", "coordination.rs.jsonl")
        e = copy.deepcopy(records[2])
        e.update(recordId="rec:app:coord:0007", seq=4, writtenAt="w004")
        e["body"]["relations"]["alternativeChosen"] = "ALT-1"
        if corrects:
            e["corrects"] = records[2]["recordId"]; e["correctionReason"] = "recorded the wrong alternative (invented)"
        with open(p, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(e, ensure_ascii=False) + "\n")
    v = variant("RV-8", lambda root: second_a16(root))
    d8 = v["rec:app:coord:0001"]["decision"]
    check(d8["alternativeChosen"] == "ALT-1" and d8["earlierActs"] == [{"act": "rec:app:coord:0003", "relation": "superseded by rec:app:coord:0007", "alternativeChosen": "ALT-2"}],
          "RV-8 (R23-25) a second A16 on the same package is a new decision that supersedes the first; the first stays listed")
    v = variant("RV-9", lambda root: second_a16(root, corrects=True))
    d9 = v["rec:app:coord:0001"]["decision"]
    check(d9["alternativeChosen"] == "ALT-1" and d9["earlierActs"][0]["relation"] == "corrected by rec:app:coord:0007",
          "RV-9 (R23-25) a correction (RS OF-5) is shown as correcting the earlier record, not as a new decision")

    def orphan(root):
        p = os.path.join(root, "records", "coordination.rs.jsonl")
        e = copy.deepcopy(records[2])
        e.update(recordId="rec:app:coord:0005", seq=4, writtenAt="w004")
        e["body"]["relations"]["requestRef"] = "rec:app:coord:0099"
        with open(p, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(e, ensure_ascii=False) + "\n")
    root7 = os.path.join(scratch, "RV-7")
    if os.path.exists(root7):
        shutil.rmtree(root7)
    shutil.copytree(FX, root7)
    orphan(root7)
    v7 = decision_view.derive(root7, ["records/coordination.rs.jsonl"])
    check(any("rec:app:coord:0099" in l for l in v7["limits"])
          and {r["package"]: r["state"] for r in v7["rows"]} == {"rec:app:coord:0001": "decided", "rec:app:coord:0002": "pending — awaiting the person's decision"},
          "RV-7 an act citing a request the records do not hold is a view limit, on no row")

    after = tree_hashes(FX)
    check(before == after, f"D input set unchanged by every derivation ({len(before)} files, hashes equal)")
    with open(os.path.join(FX, "MANIFEST.sha256"), encoding="utf-8") as fh:
        man = dict((l.split("  ", 1)[1].strip(), l.split("  ", 1)[0]) for l in fh if l.strip())
    check(all(after.get(k) == h for k, h in man.items()) and set(man) == set(after) - {"MANIFEST.sha256"},
          "D MANIFEST.sha256 matches the input set")

    print(f"\nscratch: {scratch}")
    ok = all(RESULTS)
    print(f"RESULT: {'all expectations held' if ok else 'SOME EXPECTATIONS FAILED'} ({sum(RESULTS)}/{len(RESULTS)})")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
