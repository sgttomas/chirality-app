"""DEL-09-12 practitioner validation: builder and rules PV-R1..PV-R4 (prototype; not product code).

Design: DEL-09-12 Design/PRACTITIONER_VALIDATION.md (PV-v0.1). Rulings: R23-32 (F-R3, F-R12, F-R13,
F-R14; P-2, P-3, P-6), R23-33. Reads git at a named commit (read-only); writes only F/pv/records/.

Usage: python3 -B pvlib.py --at <commit>      (builds the current real records)
"""

import csv
import hashlib
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = subprocess.run(["git", "-C", HERE, "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
OUT = os.path.join(HERE, "records")
E = "projects/chirality-app-v4/execution"
DESIGN = E + "/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-12_Practitioner validation and feedback disposition/Design"
SCHEMA = DESIGN + "/pv.practitioner-validation.schema.json"
LEDGER = E + "/_Decomposition/ScopeLedger.csv"
OPEN_ISSUES = E + "/_Decomposition/Open_Issues.csv"
UC = E + "/PKG-10_Project definition and manual-led practice/1_Working/DEL-10-02_Proportionate undertaking controls and practice feedback/Design/UNDERTAKING_CONTROLS.md"
DECISION3 = E + "/_Coordination/AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md"
PLACEHOLDER_RE = re.compile(r"illustrative|invented|example|placeholder", re.I)


def git(*a, check=True):
    return subprocess.run(["git", "-C", REPO] + list(a), capture_output=True, text=True, check=check).stdout.strip()


def text_at(at, path):
    return subprocess.run(["git", "-C", REPO, "show", "%s:%s" % (at, path)], capture_output=True, check=True).stdout.decode("utf-8")


def sha_at(at, path):
    return hashlib.sha256(subprocess.run(["git", "-C", REPO, "show", "%s:%s" % (at, path)], capture_output=True, check=True).stdout).hexdigest()


# --- F-R13: routing through the ScopeLedger ---------------------------------------------------------

def route(at, ref, kind):
    """Recipient(s) for an observation's owning commitment. Method feedback goes to DEL-10-02 (UC §9).
    Otherwise: the IN ScopeLedger rows whose SourceRef anchor is the requirement id, or whose ScopeItemID is it.
    No row means 'unresolved': a recipient is never invented (VER-004)."""
    if kind == "method":
        return ["DEL-10-02"], "method_feedback_to_DEL-10-02"
    rows = list(csv.DictReader(io.StringIO(text_at(at, LEDGER))))
    hits = sorted({d for r in rows if r["InOutStatus"] == "IN" and (r["ScopeItemID"] == ref or r["SourceRef"].split("#")[-1] == ref)
                   for d in r["DeliverableIDs"].split(";") if d})
    return (hits, "scope_ledger") if hits else (["unresolved"], "unresolved")


# --- Rules the schema cannot express -----------------------------------------------------------------

def placeholder(cand):
    return cand is None or any(PLACEHOLDER_RE.search(str(cand.get(k, ""))) for k in ("revision", "build_identity"))


def rule_errors(rec, at):
    errs, kind = [], rec.get("record_kind")
    if kind == "pv_observation" and rec.get("standing") == "actual_use" and placeholder(rec.get("candidate")):
        errs.append("PV-R1: actual use on an illustrative or unidentified candidate")
    if kind == "pv_arrangement" and rec.get("state") in ("agreed", "in_use", "ended"):
        if any(a["selected_by"] != "the owner" for e in rec["expressions"] for a in e["activities"]) or \
                any(not e["activities"] for e in rec["expressions"] if e["availability"]["state"] == "available"):
            errs.append("PV-R2: an agreed arrangement whose activities the owner did not select")
    if kind == "pv_disposition":
        want, how = route(at, rec["owning_commitment"]["ref"], rec["kind"])
        if rec["recipient"] != want or rec["routed_by"] != how:
            errs.append("PV-R3: recipient %s / %s differs from routing %s / %s" % (rec["recipient"], rec["routed_by"], want, how))
    return errs


def fr14_violations(text):
    """F-R14: every 'OI-016' is qualified as 'OI-016 (App v4)' or 'SWBPIPE OI-016'."""
    bad = []
    for m in re.finditer(r"OI-016", text):
        before, after = text[max(0, m.start() - 8):m.start()], text[m.end():m.end() + 9]
        if not (after.startswith(" (App v4)") or before.endswith("SWBPIPE ")):
            bad.append(text[max(0, m.start() - 30):m.end() + 12].replace("\n", " "))
    return bad


def uc_fields(at):
    """The field names of DEL-10-02 UC §5's practice-note table, read at the commit."""
    t = text_at(at, UC)
    sec = t[t.index("## 5. Practice-note convention"):t.index("## 6.")]
    return [m.group(1).strip() for m in re.finditer(r"^\| ([A-Z][A-Za-z ,]+?) \|", sec, flags=re.M) if m.group(1).strip() != "Field"]


UC_TO_PV = {"ID, node, date": ["id", "node", "date"], "Observer": ["observer", "recorder"], "Conditions": ["conditions"],
            "Practice exercised": ["practice_exercised"], "Class": ["class"], "Applied": ["applied"], "Consequence": ["consequence"],
            "Evidence": ["evidence"], "Inference": ["inference"], "Proposed treatment": ["proposed_treatment"], "Disposition": ["disposition"]}


# --- The current real records ------------------------------------------------------------------------

def build(at):
    at = git("rev-parse", at)
    oi = {r["OpenIssueID"]: r for r in csv.DictReader(io.StringIO(text_at(at, OPEN_ISSUES)))}
    if not (oi["OI-016"]["Status"] == "OPEN" and oi["OI-016"]["Owner"] == "Owner" and oi["OI-021"]["Status"] == "OPEN"):
        sys.exit("OI-016 (App v4) or OI-021 is no longer open: rebuild the arrangement from its record")
    if "defer the host joins" not in text_at(at, DECISION3):
        sys.exit("DECISION-3's text not found")
    arr = {
        "record_kind": "pv_arrangement", "format": "PV-v0.1", "arrangement_id": "PV-ARR-1", "version": 1,
        "open_issue": "OI-016 (App v4)", "state": "not_agreed",
        "expressions": [
            {"expression": "app", "candidate": None, "activities": [], "material": None,
             "availability": {"state": "blocked", "cause": "no App v4 candidate exists: DEL-09-02's dossier is an illustrative example and nothing is built"}},
            {"expression": "swbpipe", "candidate": None, "activities": [], "material": None,
             "availability": {"state": "blocked", "cause": "no SWBPIPE candidate; the owner deferred the host joins (DECISION-3: 'defer the host joins'); OI-021 is open"}},
        ],
        "period": None, "agreement": None,
        "prepared_by": "DEL-09-12 coordinator (O-F, prototype)",
        "limits": ["OI-016 (App v4) is open: Owner 'Owner', point of need 'Before practitioner validation in use' (Open_Issues.csv at %s)" % at[:10],
                   "no activity is proposed here: the activities are the owner's choice (V4-EXM-40), and none can run before a candidate exists",
                   "no observation exists; none is invented"],
    }
    standing = {"record_kind": "practitioner_standing", "format": "PV-v0.1", "open_issue": "OI-016 (App v4)", "standing": "not_agreed",
                "arrangement_ref": "PV-ARR-1 v1", "agreement_ref": None, "observations": 0, "is_replacement_condition": False,
                "limits": ["no validation period or activities agreed; no practitioner use has occurred",
                           "practitioner validation is not a replacement condition (R23-32 F-R3)"]}
    return {"PV-ARR-1.arrangement.json": arr, "PV-STANDING-1.json": standing}


def main():
    a = sys.argv[1:]
    if "--at" not in a:
        sys.exit(__doc__)
    at = git("rev-parse", a[a.index("--at") + 1])
    os.makedirs(OUT, exist_ok=True)
    files = build(at)
    files["BUILT_AT"] = at
    with open(os.path.join(OUT, "BUILT_AT"), "w") as fh:
        fh.write(at + "\n")
    names = []
    for name, obj in files.items():
        if name == "BUILT_AT":
            continue
        data = (json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
        if re.search(rb"/Users/|/home/", data):
            sys.exit("refusing a home path")
        open(os.path.join(OUT, name), "wb").write(data)
        names.append(name)
    with open(os.path.join(OUT, "MANIFEST.sha256"), "w", encoding="utf-8", newline="\n") as fh:
        for n in sorted(names + ["BUILT_AT"]):
            fh.write("%s  %s\n" % (hashlib.sha256(open(os.path.join(OUT, n), "rb").read()).hexdigest(), n))
    print("PV records built at %s" % at[:10])


if __name__ == "__main__":
    main()
