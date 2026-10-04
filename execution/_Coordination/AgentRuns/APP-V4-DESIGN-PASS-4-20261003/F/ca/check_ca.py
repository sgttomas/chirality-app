"""Check DEL-11-01's continuity account CA-1 (CA-v0.4 checks; CA-1 v3). Prototype, not product code. Reads only.

K-1..K-13 check the account as written against the schema, git at the recorded commit, the working tree,
the owner records and DEL-10-03's consumer list. Each rule about the account is one function of the account
(rule_errors); each N-case breaks the real account in memory and runs those same functions, naming the
rule that must refuse it. CONTINUITY_ACCOUNT.md §8 lists which claimed rules have a negative case and which
do not. Usage: python3 -B check_ca.py [--no-archives]
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


def link_errors(acct):
    """K-4: every linked record's identity recomputes at the recorded commit."""
    at, errs = acct["at_commit"], []
    for c in acct["classes"]:
        for l in c["linked_records"]:
            k, v = l["identity"]["kind"], l["identity"].get("value")
            if k == "git_blob_sha256" and B.blob_sha256(at, l["path"]) != v:
                errs.append("K-4 %s %s" % (c["class_id"], l["path"]))
            if k == "git_tree" and git("rev-parse", "%s:%s" % (at, l["path"])) != v:
                errs.append("K-4 %s %s" % (c["class_id"], l["path"]))
            if k in ("git_commit", "git_tag_target") and git("cat-file", "-t", v) != "commit":
                errs.append("K-4 %s %s" % (c["class_id"], v))
    return errs


def act_errors(acct):
    """K-9: each owner act's exact text is in its record at the commit; actor is not recorder; OD-09 in full."""
    at, errs = acct["at_commit"], []
    for a in acct["owner_acts"]:
        path = a["record_ref"].split(" row ")[0].split(", '")[0]
        if not B.matches_redacted(a["exact_text"], B.text_at(at, path)):
            errs.append("K-9 %s: exact text not in its record" % a["act_id"])
        if a["actor"] == a["recorder"]:
            errs.append("K-9 %s: recorded by its own actor" % a["act_id"])
        if a["act_id"] == "OD-09" and not (len(a.get("parts", [])) == 3 and a["recorder_stated_by_record"] is False
                                           and all(B.matches_redacted(p["text"], B.text_at(at, B.OPENING_BRIEF)) for p in a.get("parts", []))):
            errs.append("K-9 OD-09: not its three sentences, or a recorder claimed the record does not name")
    return errs


def thesis_statement_errors(prd_text):
    """K-7: PRD §11's statement of the thesis's attribution and standing."""
    return [] if "retaining attribution and its" in prd_text and "nonbinding stated standing" in prd_text else ["K-7 PRD statement missing"]


def coverage_errors(acct, x1):
    """K-10: the obligation lanes cover DEL-10-03's DEP-006 consumers (F-R11)."""
    return ["K-10 %s" % k for n, k in (("Root", "Root"), ("Runtime", "Runtime"), ("App v3", "App v3"), ("Piping", "SWBPIPE"))
            if n not in x1 or not any(k in o["lane"] for o in acct["obligations"])]


def handoff_errors(acct, handoff):
    """K-11: the hand-over repeats the account's own checks and standing; no lane is eligible for retirement."""
    errs = []
    if handoff != acct["handoff"]:
        errs.append("K-11 the hand-over file differs from the account's hand-over")
    if handoff["thesis_check"] != acct["classes"][3]["identity_check"] or handoff["archives"]["verify"] != acct["classes"][2]["identity_check"]["result"]:
        errs.append("K-11 the hand-over's checks differ from the account's")
    if any(o["retirement_eligible"] for o in acct["obligations"]):
        errs.append("K-11 a lane is recorded eligible for retirement")  # whether the record agrees with RE-1 is K-14's
    return errs


def adoption_errors(acct, aa):
    """K-13: adoption status is DEL-11-02's AA-1 status, recorded as supplied with its statement."""
    ok = acct["adoption_status"]["status"] == "supplied" and aa["statement"] in acct["adoption_status"]["ref"] and acct["handoff"]["adoption_status"] == "supplied"
    return [] if ok else ["K-13 adoption status is not AA-1's statement as supplied"]


def re1_errors(acct):
    """RE-1: a lane's recorded retirement_eligible equals the rule's result."""
    return ["RE-1 %s: recorded %s, rule %s" % (o["lane"], o["retirement_eligible"], retirement_eligible(o))
            for o in acct["obligations"] if bool(o["retirement_eligible"]) != retirement_eligible(o)]


def home_errors(texts):
    return ["K-12 home path in %s" % n for n, t in texts.items() if re.search(r"/Users/|/home/", t)]


def manifest_errors(files, manifest):
    return ["K-2 %s" % f for h, f in (l.split("  ", 1) for l in manifest.splitlines()) if hashlib.sha256(files[f]).hexdigest() != h]


def rule_errors(acct, handoff, V, x1, aa):
    return {"schema": [e.message for e in V.iter_errors(acct)], "links": link_errors(acct), "acts": act_errors(acct),
            "coverage": coverage_errors(acct, x1), "handoff": handoff_errors(acct, handoff), "adoption": adoption_errors(acct, aa), "RE-1": re1_errors(acct)}


def main():
    run_archives = "--no-archives" not in sys.argv
    rec = os.path.join(HERE, "records")
    files = {f: open(os.path.join(rec, f), "rb").read() for f in os.listdir(rec)}
    acct = json.loads(files["CA-1.continuity-account.json"])
    handoff = json.loads(files["CA-1.handoff.json"])
    at = acct["at_commit"]
    V = Draft202012Validator(json.load(open(SCHEMA, encoding="utf-8")))
    ra = open(os.path.join(HERE, "vendor", "RESPONSIBILITY_ACCOUNT.md"), encoding="utf-8").read()
    x1 = [l for l in ra.splitlines() if l.startswith("| X-1 ")][0]
    aa = json.load(open(B.AA_STATUS))
    real = rule_errors(acct, handoff, V, x1, aa)

    expect("K-1 CA-1 is valid against ca.continuity-account.schema.json", not real["schema"], real["schema"])
    expect("K-2 records/MANIFEST.sha256 holds for both output files", not manifest_errors(files, files["MANIFEST.sha256"].decode()))
    expect("K-3 rebuilding at the recorded commit reproduces the account exactly%s" % ("" if run_archives else " (archive check excluded)"),
           lambda: (lambda b: b == acct if run_archives else
                    {k: v for k, v in b.items() if k not in ("classes", "handoff")} == {k: v for k, v in acct.items() if k not in ("classes", "handoff")})
           (B.build(at, run_archives)))
    expect("K-4 every linked record's identity recomputes at the recorded commit", not real["links"], real["links"])

    exp = tree_listing(at, B.THESIS)
    expect("K-5 thesis: tree at the recorded commit equals PRD §11's, and so does HEAD's",
           lambda: git("rev-parse", "%s:%s" % (at, B.THESIS)) == B.THESIS_TREE == git("rev-parse", "HEAD:%s" % B.THESIS))
    expect("K-6 thesis: working tree clean (no modified, deleted or untracked file under it)",
           lambda: git("status", "--porcelain", "--untracked-files=all", "--", B.THESIS) == "")
    expect("K-7 thesis attribution and standing as PRD §11 states them: 'retaining attribution and its nonbinding stated standing'",
           lambda: not thesis_statement_errors(B.text_at(at, B.PRD)))

    def ver003_negatives():
        omitted, added, changed = exp[1:], exp + [("100644", "blob", "0" * 40, B.THESIS + "/zz_extra.md")], \
            [exp[0][:2] + ("f" * 40,) + exp[0][3:]] + exp[1:]
        return (compare_listing(exp, exp) == [] and [k for k, _ in compare_listing(exp, omitted)] == ["omitted"]
                and [k for k, _ in compare_listing(exp, added)] == ["added"] and [k for k, _ in compare_listing(exp, changed)] == ["changed"])
    expect("K-8 VER-003 in memory: the detector names an omitted, an added and a changed thesis file, and nothing when equal (the thesis is not touched)",
           ver003_negatives)
    expect("K-9 VER-006 positive: each owner act's exact text is in its record at the commit (OD-09: all three sentences, also in OPENING_BRIEF.md, the "
           "archive-root path redacted; no recorder named where the record names none). Limit: actor-not-recorder is a string comparison and cannot "
           "tell whether a named recorder is true", not real["acts"], real["acts"])
    expect("K-10 VER-002: the obligation lanes cover DEL-10-03's DEP-006 consumers (Root, Runtime, App v3, Piping; F-R11)", not real["coverage"], real["coverage"])
    expect("K-11 the hand-over to DEL-11-03 repeats the account's own checks and standing, and no lane is eligible for retirement", not real["handoff"], real["handoff"])
    expect("K-14 RE-1: each lane's recorded retirement eligibility is the rule's result (none eligible today)", not real["RE-1"], real["RE-1"])
    expect("K-12 no home path in any output", not home_errors({f: b.decode() for f, b in files.items()}))
    expect("K-13 adoption status is DEL-11-02's AA-1 status, recorded as supplied with its statement", not real["adoption"], real["adoption"])

    # --- Negatives: break the real account in memory; the named rule must refuse it ---------------------
    def neg(name, mutate, *rules):
        v, h = copy.deepcopy(acct), copy.deepcopy(handoff)
        mutate(v, h)
        errs = rule_errors(v, h, V, x1, aa)
        missing = [k for k in rules if not errs[k]]
        expect(name + " [refused by: %s]" % ", ".join(rules), not missing, "not refused by %s" % missing)

    replaced = {"state": "decided", "chosen_alternative": "ALT-PUBLISHED", "record_ref": "OWNER_DECISIONS_n.md (INVENTED)"}
    expect("N-1 VER-005: a decided fallback replacement makes no lane eligible for retirement [refused by: RE-1 rule]",
           not any(retirement_eligible(o, replaced) for o in acct["obligations"]))

    def n2(v, h):
        v["obligations"][0]["retirement_eligible"] = True
    neg("N-2 a lane marked eligible with no supplied obligations and no disposition", n2, "schema", "RE-1")

    def n3(v, h):
        v["obligations"][0].update({"retirement_intended": True, "continuing_obligations": "supplied", "retirement_eligible": True, "disposition": {}})
    neg("N-3 an 'empty record' disposition does not establish closure (REQ-004)", n3, "schema", "RE-1")

    def n4(v, h):
        v["owner_acts"][0]["recorder"] = "the owner"
    neg("N-4 an owner act recorded by its own actor", n4, "schema", "acts")

    def n5(v, h):
        v["owner_acts"].append(dict(v["owner_acts"][1], act_id="INVENTED", exact_text="retire App v3 now"))
    neg("N-5 a fabricated act whose exact text is not in its record", n5, "acts")

    def n6(v, h):
        v["classes"][1]["retained"] = False
    neg("N-6 a class marked not retained (deletion, migration or freeze by implication) (REQ-001, REQ-005)", n6, "schema")

    def n7(v, h):
        v["replacement_standing"] = {"state": "pending", "fallback": "v4 in use", "disposition_ref": None}
    neg("N-7 a pending replacement that drops v3.0.1", n7, "schema")

    def n8(v, h):
        v["classes"][1]["standing"] = "v4_authority"
    neg("N-8 historical material presented as v4 authority (CLM-001)", n8, "schema")

    def n9(v, h):
        v["owner_acts"][0]["exact_text"] = v["owner_acts"][0]["exact_text"].replace("Preserve both references.", "Retire both references.")
    neg("N-9 an OD-09 sentence altered behind the redaction placeholder (the placeholder matches one token only)", n9, "acts")

    # Each remaining claimed rule broken on its own in the real account (coordinator's audit, 2026-10-04)
    def n10(v, h):
        v["owner_acts"][0]["parts"] = v["owner_acts"][0]["parts"][:2]
    neg("N-10 OD-09 recorded with two of its three sentences", n10, "acts")

    def n11(v, h):
        v["owner_acts"][0]["recorder_stated_by_record"] = True
    neg("N-11 OD-09 claiming a recorder its record does not name", n11, "acts")

    def n12(v, h):
        l = [l for l in v["classes"][0]["linked_records"] if l["identity"]["kind"] == "git_blob_sha256"][0]
        l["identity"]["value"] = "0" * 64
    neg("N-12 a linked record cited with a wrong sha256", n12, "links")

    def n13(v, h):
        l = [l for c in v["classes"] for l in c["linked_records"] if l["identity"]["kind"] == "git_commit"][0]
        l["identity"]["value"] = "0" * 40
    neg("N-13 a linked commit that does not exist", n13, "links")

    def n14(v, h):
        v["obligations"] = [o for o in v["obligations"] if "Runtime" not in o["lane"]]
    neg("N-14 the Runtime obligation lane removed", n14, "coverage")

    def n15(v, h):
        h["replacement_standing"] = "replaced; v3.0.1 retired"
    neg("N-15 a hand-over stating a standing the account does not", n15, "handoff")

    def n16(v, h):
        v["adoption_status"]["ref"] = v["adoption_status"]["ref"].replace("a notice was delivered to", "a notice was received by")
    neg("N-16 an adoption status that is not AA-1's statement (AA1-R2's 'received' wording)", n16, "adoption")

    def n21(v, h):
        v["obligations"][0].update({"retirement_intended": True, "continuing_obligations": "supplied", "retirement_eligible": False,
                                    "disposition": {"by": "INVENTED lane owner", "record_ref": "INVENTED record", "evidence": ["INVENTED evidence"]}})
    v = copy.deepcopy(acct)
    n21(v, None)
    only = {k for k, e in rule_errors(v, handoff, V, x1, aa).items() if e}
    expect("N-21 RV3 CA2-N1: every RE-1 condition met but eligibility recorded false (understated) [refused by: RE-1 (K-14) only]",
           only == {"RE-1"}, sorted(only))

    expect("N-17 PRD text without the thesis standing statement [refused by: K-7]",
           thesis_statement_errors(B.text_at(at, B.PRD).replace("nonbinding stated standing", "binding standing")))
    bad = dict(files)
    bad["CA-1.handoff.json"] = files["CA-1.handoff.json"].replace(b"pending", b"decided")
    expect("N-18 a record byte changed after the manifest was written [refused by: K-2]", manifest_errors(bad, files["MANIFEST.sha256"].decode()))
    v = copy.deepcopy(acct)
    v["limits"] = v["limits"] + ["edited"]
    expect("N-19 an account edited after its build [refused by: K-3]", lambda: B.build(at, run_archives) != v)
    expect("N-20 a home path in a record [refused by: K-12]", home_errors({"x": "see /" + "Users/someone/notes"}))
    expect("P-1 the adoption status carries AA-v0.2's delivery wording, not 'received' (AA1-R2)",
           "received a notice" not in acct["adoption_status"]["ref"] and "a notice was delivered to App v3's and Runtime's coordination folders" in acct["adoption_status"]["ref"])

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
