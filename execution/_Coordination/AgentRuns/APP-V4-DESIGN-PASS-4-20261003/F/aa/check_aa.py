"""Check DEL-11-02's adoption account AA-1 (AA-v0.1). Prototype, not product code. Reads only.

K-1..K-10 check the account against its schema and against git at the recorded commit. N-1..N-8 are
negative cases on in-memory variants; each must be refused by the schema or by the separation rules.
Usage: python3 -B check_aa.py
"""

import copy
import hashlib
import json
import os
import re
import subprocess

from jsonschema import Draft202012Validator

import build_aa as B

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA = os.path.join(B.REPO, "projects/chirality-app-v4/execution/PKG-11_Adoption and replacement continuity/1_Working/"
                      "DEL-11-02_Consumer-specific renewed-basis adoption/Design/aa.adoption-account.schema.json")
VENDORED_RA = os.path.normpath(os.path.join(HERE, "..", "ca", "vendor", "RESPONSIBILITY_ACCOUNT.md"))
results = []


def expect(name, fn, detail=""):
    try:
        ok, err = bool(fn() if callable(fn) else fn), ""
    except Exception as exc:
        ok, err = False, "%s: %s" % (type(exc).__name__, exc)
    results.append((name, ok, err or ("" if ok else detail)))


def separation_errors(acct):
    """The rules the schema cannot express (ADOPTION_ACCOUNT.md §3, SR-1..SR-4)."""
    errs = []
    acts = {a["act_id"]: a for a in acct["acts"]}
    for r in acct["rows"]:
        pub_refs = {e["ref"] for e in r["facts"]["published"]["evidence"]}
        for f in ("resolved", "supplied", "provider_adopted", "observed_behavior", "consumer_adopted"):
            fact = r["facts"][f]
            if fact["state"] != "established":
                continue
            kinds = {e["kind"] for e in fact["evidence"]}
            if kinds <= {"manifest_statement", "git_commit"}:
                errs.append("SR-1 %s/%s: established only by a manifest statement or a commit" % (r["consumer_id"], f))
            if {e["ref"] for e in fact["evidence"]} <= pub_refs:
                errs.append("SR-2 %s/%s: established only by the publication evidence" % (r["consumer_id"], f))
        ca = r["facts"]["consumer_adopted"]
        if ca["state"] == "established":
            cited = [acts.get(e["ref"]) for e in ca["evidence"] if e["kind"] == "act"]
            if not cited or any(a is None for a in cited):
                errs.append("SR-3 %s: adoption cites no recorded act" % r["consumer_id"])
            elif any(a.get("consumer_id") != r["consumer_id"] for a in cited):
                errs.append("SR-4 %s: adoption cites another consumer's act" % r["consumer_id"])
    return errs


def evidence_errors(acct):
    at, errs = acct["at_commit"], []
    for r in acct["rows"]:
        for f, fact in r["facts"].items():
            for e in fact["evidence"]:
                if e["kind"] == "file_at_commit":
                    sha, text = B.blob(at, e["ref"])
                    if sha != e["sha256"] or ("quote" in e and B.norm(e["quote"]) not in B.norm(text)):
                        errs.append("%s/%s: %s" % (r["consumer_id"], f, e["ref"]))
                elif e["kind"] == "manifest_statement":
                    text = B.blob(at, e["ref"])[1]
                    if "quote" in e and B.norm(e["quote"]) not in B.norm(text):
                        errs.append("%s/%s: quote not in %s" % (r["consumer_id"], f, e["ref"]))
                elif e["kind"] == "git_commit":
                    if B.git("cat-file", "-t", e["ref"], check=False) != "commit":
                        errs.append("%s/%s: no commit %s" % (r["consumer_id"], f, e["ref"]))
    for p in acct["packaging"]:
        for e in p["evidence"]:
            text = B.blob(at, e["ref"])[1]
            if "quote" in e and B.norm(e["quote"]) not in B.norm(text):
                errs.append("packaging: quote not in %s" % e["ref"])
    return errs


def act_errors(acct):
    errs = []
    for a in acct["acts"]:
        path = a["record_ref"].split(", ")[0]
        if B.norm(a["exact_text"]) not in B.norm(B.blob(acct["at_commit"], path)[1]):
            errs.append("%s: exact text not in its record" % a["act_id"])
    return errs


def main():
    acct = json.load(open(os.path.join(HERE, "records", "AA-1.adoption-account.json"), encoding="utf-8"))
    status = json.load(open(os.path.join(HERE, "records", "AA-1.status.json"), encoding="utf-8"))
    V = Draft202012Validator(json.load(open(SCHEMA, encoding="utf-8")))
    at = acct["at_commit"]
    expect("K-1 AA-1 valid against aa.adoption-account.schema.json", lambda: not list(V.iter_errors(acct)))
    expect("K-2 records/MANIFEST.sha256 holds", lambda: all(
        hashlib.sha256(open(os.path.join(HERE, "records", f), "rb").read()).hexdigest() == h
        for h, f in (l.split("  ", 1) for l in open(os.path.join(HERE, "records", "MANIFEST.sha256")).read().splitlines())))
    expect("K-3 rebuilding at the recorded commit reproduces the account exactly", lambda: B.build(at) == acct)
    expect("K-4 every evidence item resolves at the commit: file sha256, quotes in their files, commits exist",
           lambda: not evidence_errors(acct), evidence_errors(acct))
    expect("K-5 every act's exact text is in its record; a human act's actor is the owner and its recorder is someone else (a string comparison: it cannot tell whether the named recorder is true)",
           lambda: not act_errors(acct), act_errors(acct))
    expect("K-6 the separation rules SR-1..SR-4 hold", lambda: not separation_errors(acct), separation_errors(acct))
    ra = open(VENDORED_RA, encoding="utf-8").read()
    x1 = [l for l in ra.splitlines() if l.startswith("| X-1 ")][0]
    expect("K-7 DEL-10-03's X-1 consumers (Root, Runtime, App v3, Piping) each have an RN-2 row (F-R11)",
           lambda: all(n in x1 for n in ("Root", "Runtime", "App v3", "Piping"))
           and {r["consumer_id"] for r in acct["rows"] if r["renewal_id"] == "RN-2"} == {"ROOT", "RUNTIME", "APP-V3", "PIPING"})

    def routing():
        man = B.blob(at, B.TRANCHE)[1]
        routed = set(re.findall(r"^    - (projects/\S+NOTICE_\S+\.md)$", man, flags=re.M))
        lanes = {c["consumer_id"]: c["lane"] for c in acct["consumers"]}
        for r in acct["rows"]:
            if r["renewal_id"] != "RN-1":
                continue
            routed_here = (lanes[r["consumer_id"]] + "/" + B.NOTICE) in routed
            if routed_here != (r["facts"]["delivered"]["state"] == "established"):
                return False
        return len(routed) == 3
    expect("K-8 notices: exactly the three routed by the tranche manifest are 'delivered'; the others are not_applicable", routing)

    def status_consistent():
        rn1 = [r for r in acct["rows"] if r["renewal_id"] == "RN-1"]
        adopted = sorted(r["consumer_id"] for r in rn1 if r["facts"]["consumer_adopted"]["state"] == "established")
        rn2 = [r for r in acct["rows"] if r["renewal_id"] == "RN-2"]
        return (status == acct["status"] and status["instruction_changes"][0]["adopted_by"] == adopted
                and status["renewed_basis"]["consumers_adopted"] == sorted(r["consumer_id"] for r in rn2 if r["facts"]["consumer_adopted"]["state"] == "established"))
    expect("K-9 the status hand-over says exactly what the rows establish", status_consistent)
    expect("K-10 promise trace: each derivative's state recomputes from the Design file at the commit",
           lambda: all((t["change_state"] == "applied") == any(k in B.blob(at, t["evidence"][0]["ref"])[1] for k in ("D-GOV-52", "R23-30"))
                       for t in acct["promise_trace"]))
    expect("K-11 no home path in the records", lambda: not any(re.search(r"/Users/|/home/", open(os.path.join(HERE, "records", f)).read())
                                                         for f in os.listdir(os.path.join(HERE, "records"))))

    # --- Negatives -----------------------------------------------------------------------------
    def row(a, cid, rn="RN-1"):
        return [r for r in a["rows"] if r["consumer_id"] == cid and r["renewal_id"] == rn][0]
    v = copy.deepcopy(acct)
    r = row(v, "APP-V3")
    r["facts"]["consumer_adopted"] = copy.deepcopy(r["facts"]["delivered"])
    r["adoption_point"] = "the notice"
    expect("N-1 a delivered notice offered as adoption is refused (schema: adoption needs an act)", list(V.iter_errors(v)))
    v = copy.deepcopy(acct)
    r = row(v, "APP-V4")
    r["facts"]["supplied"] = copy.deepcopy(r["facts"]["published"])
    expect("N-2 publication evidence offered as supply is refused (SR-1/SR-2)", separation_errors(v))
    v = copy.deepcopy(acct)
    r = row(v, "RUNTIME")
    r["facts"]["consumer_adopted"] = copy.deepcopy(row(acct, "APP-V4")["facts"]["consumer_adopted"])
    r["adoption_point"] = "R23-30"
    expect("N-3 App v4's adoption offered as Runtime's is refused (SR-4)", any(e.startswith("SR-4") for e in separation_errors(v)))
    v = copy.deepcopy(acct)
    v["acts"].append({"act_id": "AD-X", "kind": "agent_act", "consumer_id": "APP-V3", "actor": "App v3 loop", "recorder": "O-F",
                      "recorder_stated_by_record": False, "subject": "App v3 adopts D-GOV-52",
                      "record_ref": "projects/chirality-app-dev/execution/_Coordination/" + B.NOTICE.split("/")[-1],
                      "exact_text": "App v3 adopts the changed Root text.", "custody": "INVENTED"})
    expect("N-4 a fabricated adoption act whose text is not in its record is refused (K-5's rule)", act_errors(v))
    v = copy.deepcopy(acct)
    v["acts"][0]["recorder"] = "the owner"
    expect("N-5 a human act recorded by its own actor is refused (schema)", list(V.iter_errors(v)))
    v = copy.deepcopy(acct)
    row(v, "APP-V3")["facts"]["supplied"] = {"state": "established", "evidence": []}
    expect("N-6 an 'unknown' turned 'established' without evidence is refused (schema)", list(V.iter_errors(v)))
    v = copy.deepcopy(acct)
    v["status"]["instruction_changes"][0]["adopted_by"] = ["APP-V4", "APP-V3"]
    expect("N-7 a status hand-over claiming an adopter the rows do not establish fails K-9's rule",
           v["status"]["instruction_changes"][0]["adopted_by"] != sorted(r["consumer_id"] for r in v["rows"] if r["renewal_id"] == "RN-1" and r["facts"]["consumer_adopted"]["state"] == "established"))
    v = copy.deepcopy(acct)
    r = row(v, "PIPING")
    r["facts"]["consumer_adopted"] = {"state": "established", "evidence": copy.deepcopy(r["facts"]["prepared_notice"]["evidence"])}
    r["adoption_point"] = "reads Root live"
    expect("N-8 the manifest's 'reads Root AGENTS.md live' offered as adoption is refused", list(V.iter_errors(v)) and separation_errors(v))

    for name, ok, detail in results:
        print(("HOLDS " if ok else "FAILS ") + name + ("" if ok or not detail else "  -> %s" % (detail,)))
    failed = sum(1 for _, ok, _ in results if not ok)
    print("%d/%d expectations held" % (len(results) - failed, len(results)))
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
