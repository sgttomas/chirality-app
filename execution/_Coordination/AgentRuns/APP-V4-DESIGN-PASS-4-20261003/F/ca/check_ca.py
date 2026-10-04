"""Check DEL-11-01's continuity account CA-1 (CA-v0.2). Prototype, not product code. Reads only.

K-1..K-12 check the account as written against the schema, git at the recorded commit, the working tree,
the owner records and DEL-10-03's consumer list. N-1..N-8 are negative cases on in-memory variants:
each must be refused. Usage: python3 -B check_ca.py [--no-archives]
"""

import copy
import hashlib
import json
import os
import re
import subprocess
import sys

from jsonschema import Draft202012Validator

import build_ca as B

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA = os.path.join(B.REPO, "projects/chirality-app-v4/execution/PKG-11_Adoption and replacement continuity/1_Working/"
                      "DEL-11-01_Preserved history and coexistence account/Design/ca.continuity-account.schema.json")
results, notices = [], []


def expect(name, fn, detail=""):
    try:
        ok, err = bool(fn() if callable(fn) else fn), ""
    except Exception as exc:
        ok, err = False, "%s: %s" % (type(exc).__name__, exc)
    results.append((name, ok, err or ("" if ok else detail)))


def git(*a):
    return subprocess.run(["git", "-C", B.REPO] + list(a), capture_output=True, text=True).stdout.strip()


def tree_listing(commit, path):
    """[(mode, type, object id, path)] for every file below path at commit."""
    out = []
    for line in git("ls-tree", "-r", commit, "--", path).splitlines():
        meta, p = line.split("\t", 1)
        mode, typ, oid = meta.split()
        out.append((mode, typ, oid, p))
    return out


def compare_listing(expected, observed):
    """VER-003's detector: names every omitted, added or changed file. Empty means equal."""
    e = {p: oid for _, _, oid, p in expected}
    o = {p: oid for _, _, oid, p in observed}
    return ([("omitted", p) for p in sorted(set(e) - set(o))] + [("added", p) for p in sorted(set(o) - set(e))]
            + [("changed", p) for p in sorted(set(e) & set(o)) if e[p] != o[p]])


def retirement_eligible(ob, replacement_disposition=None):
    """REQ-004 / VER-005: a lane is eligible only with retirement intended, obligations supplied and an
    evidenced disposition by its accountable owner. The fallback replacement disposition is not an input."""
    del replacement_disposition  # never consulted: a fallback replacement retires nothing
    d = ob.get("disposition") or {}
    return bool(ob["retirement_intended"] and ob["continuing_obligations"] == "supplied" and d.get("by") and d.get("record_ref") and d.get("evidence"))


def main():
    run_archives = "--no-archives" not in sys.argv
    acct = json.load(open(os.path.join(HERE, "records", "CA-1.continuity-account.json"), encoding="utf-8"))
    handoff = json.load(open(os.path.join(HERE, "records", "CA-1.handoff.json"), encoding="utf-8"))
    at = acct["at_commit"]
    V = Draft202012Validator(json.load(open(SCHEMA, encoding="utf-8")))

    expect("K-1 CA-1 is valid against ca.continuity-account.schema.json", lambda: not list(V.iter_errors(acct)))
    expect("K-2 records/MANIFEST.sha256 holds for both output files", lambda: all(
        hashlib.sha256(open(os.path.join(HERE, "records", f), "rb").read()).hexdigest() == h
        for h, f in (l.split("  ", 1) for l in open(os.path.join(HERE, "records", "MANIFEST.sha256")).read().splitlines())))
    expect("K-3 rebuilding at the recorded commit reproduces the account exactly%s" % ("" if run_archives else " (archive check excluded)"),
           lambda: (lambda b: b == acct if run_archives else
                    {k: v for k, v in b.items() if k not in ("classes", "handoff")} == {k: v for k, v in acct.items() if k not in ("classes", "handoff")})
           (B.build(at, run_archives)))

    def links():
        for c in acct["classes"]:
            for l in c["linked_records"]:
                k, v = l["identity"]["kind"], l["identity"].get("value")
                if k == "git_blob_sha256" and B.blob_sha256(at, l["path"]) != v:
                    return False
                if k == "git_tree" and git("rev-parse", "%s:%s" % (at, l["path"])) != v:
                    return False
                if k in ("git_commit", "git_tag_target") and git("cat-file", "-t", v) != "commit":
                    return False
        return True
    expect("K-4 every linked record's identity recomputes at the recorded commit", links)

    exp = tree_listing(at, B.THESIS)
    expect("K-5 thesis: tree at the recorded commit equals PRD §11's, and so does HEAD's",
           lambda: git("rev-parse", "%s:%s" % (at, B.THESIS)) == B.THESIS_TREE == git("rev-parse", "HEAD:%s" % B.THESIS))
    expect("K-6 thesis: working tree clean (no modified, deleted or untracked file under it)",
           lambda: git("status", "--porcelain", "--untracked-files=all", "--", B.THESIS) == "")
    expect("K-7 thesis attribution and standing as PRD §11 states them: 'retaining attribution and its nonbinding stated standing'",
           lambda: "retaining attribution and its" in B.text_at(at, B.PRD) and "nonbinding stated standing" in B.text_at(at, B.PRD))

    def ver003_negatives():
        omitted, added, changed = exp[1:], exp + [("100644", "blob", "0" * 40, B.THESIS + "/zz_extra.md")], \
            [exp[0][:2] + ("f" * 40,) + exp[0][3:]] + exp[1:]
        return (compare_listing(exp, exp) == [] and [k for k, _ in compare_listing(exp, omitted)] == ["omitted"]
                and [k for k, _ in compare_listing(exp, added)] == ["added"] and [k for k, _ in compare_listing(exp, changed)] == ["changed"])
    expect("K-8 VER-003 in memory: the detector names an omitted, an added and a changed thesis file, and nothing when equal (the thesis is not touched)",
           ver003_negatives)

    def acts():
        for a in acct["owner_acts"]:
            path = a["record_ref"].split(" row ")[0].split(", '")[0]
            if not B.matches_redacted(a["exact_text"], B.text_at(at, path)) or a["actor"] == a["recorder"]:
                return False
            if a["act_id"] == "OD-09" and not (all(B.matches_redacted(p["text"], B.text_at(at, B.OPENING_BRIEF)) for p in a.get("parts", []))
                                                and len(a.get("parts", [])) == 3 and a["recorder_stated_by_record"] is False):
                return False
        return True
    expect("K-9 VER-006 positive: each owner act's exact text is in its record at the commit (OD-09: all three sentences, also in OPENING_BRIEF.md, the "
           "archive-root path redacted; no recorder named where the record names none). Limit: actor-not-recorder is a string comparison and cannot "
           "tell whether a named recorder is true", acts)

    ra = open(os.path.join(HERE, "vendor", "RESPONSIBILITY_ACCOUNT.md"), encoding="utf-8").read()
    x1 = [l for l in ra.splitlines() if l.startswith("| X-1 ")][0]
    expect("K-10 VER-002: the obligation lanes cover DEL-10-03's DEP-006 consumers (Root, Runtime, App v3, Piping; F-R11)",
           lambda: all(n in x1 for n in ("Root", "Runtime", "App v3", "Piping"))
           and all(any(k in o["lane"] for o in acct["obligations"]) for k in ("Root", "Runtime", "App v3", "SWBPIPE")))
    aa = json.load(open(B.AA_STATUS))
    expect("K-13 adoption status is DEL-11-02's AA-1 status, recorded as supplied with its statement",
           lambda: acct["adoption_status"]["status"] == "supplied" and aa["statement"] in acct["adoption_status"]["ref"] and acct["handoff"]["adoption_status"] == "supplied")
    expect("K-11 the hand-over to DEL-11-03 repeats the account's own checks and standing, and no lane is eligible for retirement",
           lambda: handoff == acct["handoff"] and handoff["thesis_check"] == acct["classes"][3]["identity_check"]
           and handoff["archives"]["verify"] == acct["classes"][2]["identity_check"]["result"]
           and not any(retirement_eligible(o) for o in acct["obligations"]))
    expect("K-12 no home path in any output", lambda: not any(re.search(r"/Users/|/home/", open(os.path.join(HERE, "records", f)).read())
                                                         for f in os.listdir(os.path.join(HERE, "records"))))

    # --- Negatives: each must be refused ---------------------------------------------------------
    replaced = {"state": "decided", "chosen_alternative": "ALT-PUBLISHED", "record_ref": "OWNER_DECISIONS_n.md (INVENTED)"}
    expect("N-1 VER-005: a decided fallback replacement makes no lane eligible for retirement",
           not any(retirement_eligible(o, replaced) for o in acct["obligations"]))
    v = copy.deepcopy(acct)
    v["obligations"][0]["retirement_eligible"] = True
    expect("N-2 a lane marked eligible with no supplied obligations and no disposition is refused by the schema", list(V.iter_errors(v)))
    v = copy.deepcopy(acct)
    v["obligations"][0].update({"retirement_intended": True, "continuing_obligations": "supplied", "retirement_eligible": True, "disposition": {}})
    expect("N-3 an 'empty record' disposition does not establish closure (REQ-004)", list(V.iter_errors(v)) and not retirement_eligible(v["obligations"][0]))
    v = copy.deepcopy(acct)
    v["owner_acts"][0]["recorder"] = "the owner"
    expect("N-4 an owner act recorded by its own actor is refused", list(V.iter_errors(v)))
    v = copy.deepcopy(acct)
    v["owner_acts"].append(dict(v["owner_acts"][1], act_id="INVENTED", exact_text="retire App v3 now"))
    expect("N-5 a fabricated act whose exact text is not in its record fails K-9's rule",
           any(not B.matches_redacted(a["exact_text"], B.text_at(at, a["record_ref"].split(" row ")[0].split(", '")[0])) for a in v["owner_acts"]))
    v = copy.deepcopy(acct)
    v["owner_acts"][0]["exact_text"] = v["owner_acts"][0]["exact_text"].replace("Preserve both references.", "Retire both references.")
    expect("N-9 an OD-09 sentence altered behind the redaction placeholder still fails the exact-text rule (the placeholder matches one token only)",
           not B.matches_redacted(v["owner_acts"][0]["exact_text"], B.text_at(at, B.DECISIONS)))
    v = copy.deepcopy(acct)
    v["classes"][1]["retained"] = False
    expect("N-6 a class marked not retained (deletion, migration or freeze by implication) is refused (REQ-001, REQ-005)", list(V.iter_errors(v)))
    v = copy.deepcopy(acct)
    v["replacement_standing"] = {"state": "pending", "fallback": "v4 in use", "disposition_ref": None}
    expect("N-7 a pending replacement that drops v3.0.1 is refused", list(V.iter_errors(v)))
    v = copy.deepcopy(acct)
    v["classes"][1]["standing"] = "v4_authority"
    expect("N-8 historical material presented as v4 authority is refused (CLM-001)", list(V.iter_errors(v)))

    # --- Vendored input drift (R23-44) -----------------------------------------------------------------
    ven = json.load(open(os.path.join(HERE, "vendor", "VENDOR.json")))
    for f in ven["files"]:
        live = os.path.join(B.REPO, "projects/chirality-app-v4/execution", f["source"])
        now = hashlib.sha256(open(live, "rb").read()).hexdigest() if os.path.exists(live) else "missing"
        expect("V-1 vendored %s equals the sha256 recorded at vendoring" % f["key"],
               hashlib.sha256(open(os.path.join(HERE, f["vendored"]), "rb").read()).hexdigest() == f["sha256"])
        if now != f["sha256"]:
            notices.append("NOTICE live %s moved since vendoring (%s -> %s); re-pin deliberately" % (f["key"], f["sha256"][:12], now[:12]))

    for name, ok, detail in results:
        print(("HOLDS " if ok else "FAILS ") + name + ("" if ok or not detail else "  -> %s" % detail))
    for n in notices:
        print(n)
    failed = sum(1 for _, ok, _ in results if not ok)
    print("%d/%d expectations held" % (len(results) - failed, len(results)))
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
