"""Check DEL-11-02's adoption account AA-1 (AA-v0.3 rules; record format AA-v0.2). Prototype, not product code. Reads only.

K-1..K-11 check the real account against its schema and against git at the recorded commit. Every rule the
Design says this file enforces is a function of the account (rule_errors); each N-case breaks the real account
in memory and runs those same functions, naming the rule that must refuse it (a negative never re-derives
the rule). ADOPTION_ACCOUNT.md §7 lists which claimed rules have a negative case and which do not.
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


WHITELIST = {  # AA-v0.2 §3: the evidence kinds each fact accepts when established (also in the schema)
    "prepared_notice": {"manifest_statement"},
    "delivered": {"file_at_commit"},
    "published": {"file_at_commit", "git_commit"},
    "resolved": {"candidate_record", "observation_record"},
    "supplied": {"candidate_record", "observation_record"},
    "provider_adopted": {"candidate_record", "observation_record"},
    "observed_behavior": {"candidate_record", "observation_record"},
    "consumer_adopted": {"act", "file_at_commit"},
}
ADOPT_RE = re.compile(r"\badopt(s|ed|ion)?\b", re.I)
NEGATION_RE = re.compile(r"\b(not|no|never|without)\b", re.I)


def in_lane(path, lane):
    """A path lies in a consumer's lane (a lane may list several roots, e.g. Root's 'AGENTS.md, docs/')."""
    return any(path == root.rstrip("/") or path.startswith(root.rstrip("/") + "/") for root in lane.split(", "))


def adoption_text(text):
    """SR-4: the act's own words state an adoption, and do not negate it."""
    t = B.norm(text)
    return bool(ADOPT_RE.search(t)) and not NEGATION_RE.search(t)


ENTRY_HEAD_RE = re.compile(r"^(#{1,6} |- \*\*)")
ID_RE = re.compile(r"\b[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+\b")


def renewal_names(rn):
    """AA2-R1: what names a renewal: the identifiers in its `what`, and its change record's file stem."""
    names = set(ID_RE.findall(rn["what"]))
    if rn.get("change_record"):
        names.add(os.path.splitext(os.path.basename(rn["change_record"]))[0])
    return names


def routed_notices(acct, rn):
    """AA2-R1: the notice paths the renewal's own change record (a tranche manifest) routes; none without one."""
    if not rn.get("change_record"):
        return set()
    man = blob_or_none(acct["at_commit"], rn["change_record"])[1]
    return set(re.findall(r"^    - (projects/\S+NOTICE_\S+\.md)$", man, flags=re.M))


def entry_of(text, quote):
    """The record entry holding a quote: from the last heading or top-level bold item ('- **') before it."""
    lines = text.split("\n")
    nq = B.norm(quote)
    for i in range(len(lines)):
        if nq in B.norm("\n".join(lines[i:i + 12])):
            start = max([j for j in range(i + 1) if ENTRY_HEAD_RE.match(lines[j])], default=0)
            return "\n".join(lines[start:i + 12])
    return ""


def separation_errors(acct):
    """The separation rules (ADOPTION_ACCOUNT.md §3, SR-1..SR-4), enforced, not only stated (RV3 AA1-R1)."""
    errs = []
    acts = {a["act_id"]: a for a in acct["acts"]}
    lanes = {c["consumer_id"]: c["lane"] for c in acct["consumers"]}
    renewals = {rn["renewal_id"]: rn for rn in acct["renewals"]}
    for r in acct["rows"]:
        cid = r["consumer_id"]
        rn = renewals[r["renewal_id"]]
        for f, fact in r["facts"].items():
            if fact["state"] != "established":
                continue
            bad = {e["kind"] for e in fact["evidence"]} - WHITELIST[f]
            if bad:
                errs.append("SR-1 %s/%s: evidence of kind %s is not evidence of this fact" % (cid, f, sorted(bad)))
        dl = r["facts"]["delivered"]
        if dl["state"] == "established" and not all(e["kind"] == "file_at_commit" and in_lane(e["ref"], lanes[cid]) for e in dl["evidence"]):
            errs.append("SR-2 %s/delivered: delivery is shown only by a file inside the receiving lane (%s)" % (cid, lanes[cid]))
        if dl["state"] == "established" and not all(e["ref"] in routed_notices(acct, rn) for e in dl["evidence"]):
            errs.append("SR-2 %s/%s delivered: the file is not a notice that %s's change record routes" % (cid, r["renewal_id"], r["renewal_id"]))
        ca = r["facts"]["consumer_adopted"]
        if ca["state"] == "established":
            cited = [acts.get(e["ref"]) for e in ca["evidence"] if e["kind"] == "act"]
            if not cited or any(a is None for a in cited):
                errs.append("SR-3 %s: adoption cites no recorded act" % cid)
                continue
            for a in cited:
                record = a["record_ref"].split(", ")[0]
                if a["kind"] != "agent_act" or a.get("act_class") != "adoption" or a.get("consumer_id") != cid or not in_lane(record, lanes[cid]):
                    errs.append("SR-3 %s: %s is not %s's own loop's adoption act recorded in its own lane (kind %s, class %s, consumer %s, record %s)"
                                % (cid, a["act_id"], cid, a["kind"], a.get("act_class"), a.get("consumer_id"), record))
                if not adoption_text(a["exact_text"]):
                    errs.append("SR-4 %s: %s's text does not state an adoption" % (cid, a["act_id"]))
                entry = entry_of(blob_or_none(acct["at_commit"], record)[1], a["exact_text"])
                if not any(n in entry for n in renewal_names(rn)):
                    errs.append("SR-3 %s: %s's record entry does not name %s (%s)" % (cid, a["act_id"], r["renewal_id"], ", ".join(sorted(renewal_names(rn)))))
            records = {a["record_ref"].split(", ")[0] for a in cited if a}
            if any(e["kind"] == "file_at_commit" and e["ref"] not in records for e in ca["evidence"]):
                errs.append("SR-3 %s: a file cited for adoption is not the adoption act's record" % cid)
    return errs


def blob_or_none(at, path):
    """A file's (sha256, text) at the commit, or (None, "") when it does not exist there (a refusal, not a crash)."""
    try:
        return B.blob(at, path)
    except subprocess.CalledProcessError:
        return None, ""


def evidence_errors(acct):
    at, errs = acct["at_commit"], []
    for r in acct["rows"]:
        for f, fact in r["facts"].items():
            for e in fact["evidence"]:
                if e["kind"] == "file_at_commit":
                    sha, text = blob_or_none(at, e["ref"])
                    if sha != e["sha256"] or ("quote" in e and B.norm(e["quote"]) not in B.norm(text)):
                        errs.append("%s/%s: %s" % (r["consumer_id"], f, e["ref"]))
                elif e["kind"] == "manifest_statement":
                    text = blob_or_none(at, e["ref"])[1]
                    if "quote" in e and B.norm(e["quote"]) not in B.norm(text):
                        errs.append("%s/%s: quote not in %s" % (r["consumer_id"], f, e["ref"]))
                elif e["kind"] == "git_commit":
                    if B.git("cat-file", "-t", e["ref"], check=False) != "commit":
                        errs.append("%s/%s: no commit %s" % (r["consumer_id"], f, e["ref"]))
    for p in acct["packaging"]:
        for e in p["evidence"]:
            text = blob_or_none(at, e["ref"])[1]
            if "quote" in e and B.norm(e["quote"]) not in B.norm(text):
                errs.append("packaging: quote not in %s" % e["ref"])
    return errs


def act_errors(acct):
    errs = []
    for a in acct["acts"]:
        path = a["record_ref"].split(", ")[0]
        if B.norm(a["exact_text"]) not in B.norm(blob_or_none(acct["at_commit"], path)[1]):
            errs.append("%s: exact text not in its record" % a["act_id"])
    return errs


def coverage_errors(acct, x1):
    """K-7: DEL-10-03's X-1 consumers each have an RN-2 row (F-R11)."""
    want = {"Root": "ROOT", "Runtime": "RUNTIME", "App v3": "APP-V3", "Piping": "PIPING"}
    have = {r["consumer_id"] for r in acct["rows"] if r["renewal_id"] == "RN-2"}
    return ["K-7 X-1 consumer %s has no RN-2 row" % n for n, cid in want.items() if n not in x1 or cid not in have]


def routing_errors(acct):
    """K-8: exactly the notices the tranche manifest routes are 'delivered'; the others are not."""
    man = B.blob(acct["at_commit"], B.TRANCHE)[1]
    routed = set(re.findall(r"^    - (projects/\S+NOTICE_\S+\.md)$", man, flags=re.M))
    lanes = {c["consumer_id"]: c["lane"] for c in acct["consumers"]}
    errs = [] if len(routed) == 3 else ["K-8 the manifest routes %d notices, not 3" % len(routed)]
    for r in acct["rows"]:
        if r["renewal_id"] == "RN-1" and ((lanes[r["consumer_id"]] + "/" + B.NOTICE) in routed) != (r["facts"]["delivered"]["state"] == "established"):
            errs.append("K-8 %s: delivered state differs from the manifest's routing" % r["consumer_id"])
    return errs


def status_errors(acct, status):
    """K-9: the status hand-over says exactly what the rows establish."""
    def adopted(rn):
        return sorted(r["consumer_id"] for r in acct["rows"] if r["renewal_id"] == rn and r["facts"]["consumer_adopted"]["state"] == "established")
    errs = []
    if status != acct["status"]:
        errs.append("K-9 the status file differs from the account's status")
    if status["instruction_changes"][0]["adopted_by"] != adopted("RN-1"):
        errs.append("K-9 RN-1 adopted_by differs from the rows")
    if status["renewed_basis"]["consumers_adopted"] != adopted("RN-2"):
        errs.append("K-9 RN-2 consumers_adopted differs from the rows")
    return errs


def trace_errors(acct):
    """K-10: each derivative's 'applied' state recomputes from its Design file at the commit."""
    return ["K-10 %s" % t["evidence"][0]["ref"] for t in acct["promise_trace"]
            if (t["change_state"] == "applied") != any(k in B.blob(acct["at_commit"], t["evidence"][0]["ref"])[1] for k in ("D-GOV-52", "R23-30"))]


def home_errors(texts):
    """K-11: no home path."""
    return ["K-11 home path in %s" % n for n, t in texts.items() if re.search(r"/Users/|/home/", t)]


def manifest_errors(files, manifest):
    """K-2: every file named in MANIFEST.sha256 has its hash."""
    return ["K-2 %s" % f for h, f in (l.split("  ", 1) for l in manifest.splitlines()) if hashlib.sha256(files[f]).hexdigest() != h]


def rule_errors(acct, status, V, x1):
    """Every rule the Design claims is enforced, by name, on one account."""
    sep = separation_errors(acct)
    return {
        "schema": [e.message for e in V.iter_errors(acct)] + ["status: " + e.message for e in V.evolve(schema={"$ref": "#/$defs/adoption_status", **{k: V.schema[k] for k in ("$defs",)}}).iter_errors(status)],
        "evidence": evidence_errors(acct),
        "acts": act_errors(acct),
        "SR-1": [e for e in sep if e.startswith("SR-1")],
        "SR-2": [e for e in sep if e.startswith("SR-2")],
        "SR-3": [e for e in sep if e.startswith("SR-3")],
        "SR-4": [e for e in sep if e.startswith("SR-4")],
        "coverage": coverage_errors(acct, x1),
        "routing": routing_errors(acct),
        "status": status_errors(acct, status),
        "trace": trace_errors(acct),
    }


def main():
    rec = os.path.join(HERE, "records")
    files = {f: open(os.path.join(rec, f), "rb").read() for f in os.listdir(rec)}
    acct = json.loads(files["AA-1.adoption-account.json"])
    status = json.loads(files["AA-1.status.json"])
    V = Draft202012Validator(json.load(open(SCHEMA, encoding="utf-8")))
    at = acct["at_commit"]
    x1 = [l for l in open(VENDORED_RA, encoding="utf-8").read().splitlines() if l.startswith("| X-1 ")][0]
    real = rule_errors(acct, status, V, x1)

    expect("K-1 AA-1 and its status hand-over are valid against aa.adoption-account.schema.json", not real["schema"], real["schema"])
    expect("K-2 records/MANIFEST.sha256 holds", not manifest_errors(files, files["MANIFEST.sha256"].decode()))
    expect("K-3 rebuilding at the recorded commit reproduces the account exactly", lambda: B.build(at) == acct)
    expect("K-4 every evidence item resolves at the commit: file sha256, quotes in their files, commits exist", not real["evidence"], real["evidence"])
    expect("K-5 every act's exact text is in its record; a human act's actor is the owner and its recorder is someone else (schema; a string comparison: it cannot tell whether the named recorder is true)",
           not real["acts"], real["acts"])
    expect("K-6 the separation rules SR-1..SR-4 hold", not any(real[k] for k in ("SR-1", "SR-2", "SR-3", "SR-4")))
    expect("K-7 DEL-10-03's X-1 consumers (Root, Runtime, App v3, Piping) each have an RN-2 row (F-R11)", not real["coverage"], real["coverage"])
    expect("K-8 notices: exactly the three routed by the tranche manifest are 'delivered'; the others are not", not real["routing"], real["routing"])
    expect("K-9 the status hand-over says exactly what the rows establish", not real["status"], real["status"])
    expect("K-10 promise trace: each derivative's 'applied' state recomputes from the Design file at the commit", not real["trace"], real["trace"])
    expect("K-11 no home path in the records", not home_errors({f: b.decode() for f, b in files.items()}))

    # --- Negatives: break the real account in memory; the named rule must refuse it ---------------------
    def row(a, cid, rn="RN-1"):
        return [r for r in a["rows"] if r["consumer_id"] == cid and r["renewal_id"] == rn][0]

    def act(a, aid):
        return [x for x in a["acts"] if x["act_id"] == aid][0]

    def neg(name, mutate, *rules, st=None):
        v, s = copy.deepcopy(acct), copy.deepcopy(status)
        mutate(v, s)
        errs = rule_errors(v, s, V, x1)
        missing = [k for k in rules if not errs[k]]
        expect(name + " [refused by: %s]" % ", ".join(rules), not missing, "not refused by %s" % missing)

    def n1(v, s):
        r = row(v, "APP-V3")
        r["facts"]["consumer_adopted"] = copy.deepcopy(r["facts"]["delivered"])
        r["adoption_point"] = "the notice"
    neg("N-1 a delivered notice offered as App v3's adoption", n1, "schema", "SR-3")

    def n2(v, s):
        r = row(v, "APP-V4")
        r["facts"]["supplied"] = copy.deepcopy(r["facts"]["published"])
    neg("N-2 publication evidence offered as App v4's supply", n2, "SR-1")

    def n3(v, s):
        r = row(v, "RUNTIME")
        r["facts"]["consumer_adopted"] = copy.deepcopy(row(acct, "APP-V4")["facts"]["consumer_adopted"])
        r["adoption_point"] = "R23-30"
    neg("N-3 App v4's adoption AD-1 offered as Runtime's", n3, "SR-3")

    def n4(v, s):
        v["acts"].append({"act_id": "AD-X", "kind": "agent_act", "act_class": "adoption", "recording_mode": "faithful recording", "consumer_id": "APP-V3",
                          "actor": "App v3 loop", "recorder": "O-F", "recorder_stated_by_record": False, "subject": "App v3 adopts D-GOV-52",
                          "record_ref": "projects/chirality-app-dev/" + B.NOTICE, "exact_text": "App v3 adopts the changed Root text.", "custody": "INVENTED"})
    neg("N-4 a fabricated act whose text is not in its record", n4, "acts")

    def n5(v, s):
        act(v, "A-1")["recorder"] = "the owner"
    neg("N-5 a human act recorded by its own actor", n5, "schema")

    def n6(v, s):
        row(v, "APP-V3")["facts"]["supplied"] = {"state": "established", "evidence": []}
    neg("N-6 an 'unknown' turned 'established' without evidence", n6, "schema")

    def n7(v, s):
        s["instruction_changes"][0]["adopted_by"] = ["APP-V3", "APP-V4"]
    neg("N-7 a status hand-over claiming an adopter the rows do not establish", n7, "status")

    def n8(v, s):
        r = row(v, "PIPING")
        r["facts"]["consumer_adopted"] = {"state": "established", "evidence": copy.deepcopy(r["facts"]["prepared_notice"]["evidence"])}
        r["adoption_point"] = "reads Root live"
    neg("N-8 the manifest's 'reads Root AGENTS.md live' offered as Piping's adoption", n8, "schema", "SR-1", "SR-3")

    # RV3 AA1-R1's five constructions (reviews/RV3-AA1.md), reproduced as RV3 built them
    def n9(v, s):
        r = row(v, "APP-V3")
        r["facts"]["supplied"] = {"state": "established", "evidence": copy.deepcopy(r["facts"]["delivered"]["evidence"])}
    neg("N-9 RV3 variant 1: App v3 'supplied' established by the delivered notice file", n9, "schema", "SR-1")

    def n10(v, s):
        r = row(v, "APP-V3")
        r["facts"]["observed_behavior"] = {"state": "established", "evidence": copy.deepcopy(r["facts"]["consumer_adopted"]["evidence"])}
    neg("N-10 RV3 variant 2: App v3 'observed behaviour' established by an absence search", n10, "schema", "SR-1")

    def n11(v, s):
        row(v, "PIPING")["facts"]["delivered"] = {"state": "established", "evidence": [{"kind": "manifest_statement", "ref": B.TRANCHE}]}
    neg("N-11 RV3 variant 3: Piping 'delivered' established by the tranche manifest's statement alone", n11, "schema", "SR-1", "SR-2", "routing")

    def n12(v, s):
        v["acts"].append({"act_id": "AD-X", "kind": "agent_act", "act_class": "adoption", "recording_mode": "direct capture", "consumer_id": "APP-V3",
                          "actor": "HELP_HUMAN", "recorder": "HELP_HUMAN", "recorder_stated_by_record": True,
                          "subject": "App v3's receiving decision on D-GOV-52", "record_ref": B.RUN + "/R23_RESOLUTIONS.md, R23-32",
                          "exact_text": "notice delivered; receiving decision not recorded", "custody": "R23-32 F-R16"})
        r = row(v, "APP-V3")
        r["facts"]["consumer_adopted"] = {"state": "established", "evidence": [{"kind": "act", "ref": "AD-X"}]}
        r["adoption_point"] = "R23-32"
    neg("N-12 RV3 variant 4: App v3 'consumer adopted' from an agent act whose text is F-R16's status statement (its text is in its record, so K-5 passes)",
        n12, "SR-3", "SR-4")

    def n13(v, s):
        a1 = copy.deepcopy(act(v, "A-1"))
        a1.update({"act_id": "A-1-RUNTIME", "consumer_id": "RUNTIME"})
        v["acts"].append(a1)
        r = row(v, "RUNTIME")
        r["facts"]["consumer_adopted"] = {"state": "established", "evidence": [{"kind": "act", "ref": "A-1-RUNTIME"}]}
        r["adoption_point"] = "A-1"
    neg("N-13 RV3 variant 5: Runtime 'consumer adopted' from the owner's approval A-1 copied with consumer_id RUNTIME", n13, "SR-3", "SR-4")

    def n14(v, s):
        n13(v, s)
        act(v, "A-1-RUNTIME")["act_class"] = "adoption"
    neg("N-14 variant 5 with act_class relabelled 'adoption'", n14, "SR-3", "SR-4")

    def n15(v, s):
        n14(v, s)
        act(v, "A-1-RUNTIME").update({"record_ref": "projects/chirality-runtime/execution/_Coordination/ADOPTION.md",
                                      "exact_text": "Runtime adopts the changed Root text."})
    neg("N-15 variant 5 with adoption class, Runtime's own lane and adoption text: still a person's act (human_act), never a loop's adoption (F-R10)",
        n15, "SR-3")

    # Each claimed rule broken on its own in the real account (coordinator's audit, 2026-10-04)
    def n16(v, s):
        act(v, "AD-1")["exact_text"] = "App v4 does not adopt the changed Root text."
    neg("N-16 App v4's own act AD-1 with a negated text", n16, "SR-4", "acts")

    def n17(v, s):
        row(v, "APP-V3")["facts"]["delivered"]["evidence"] = copy.deepcopy(row(acct, "APP-V4")["facts"]["delivered"]["evidence"])
    neg("N-17 App v3 'delivered' shown by App v4's notice file (a file, but outside App v3's lane)", n17, "SR-2")

    def n18(v, s):
        row(v, "APP-V4")["facts"]["consumer_adopted"]["evidence"].append(copy.deepcopy(row(acct, "APP-V3")["facts"]["delivered"]["evidence"][0]))
    neg("N-18 App v4's adoption also citing a file that is not the adoption act's record", n18, "SR-3")

    def n19(v, s):
        row(v, "APP-V4")["adoption_point"] = ""
    neg("N-19 an established adoption without an adoption point", n19, "schema")

    def n20(v, s):
        row(v, "APP-V3")["facts"]["delivered"]["evidence"][0]["sha256"] = "0" * 64
    neg("N-20 a delivered notice cited with a wrong sha256", n20, "evidence")

    def n21(v, s):
        row(v, "PIPING")["facts"]["prepared_notice"]["evidence"][0]["quote"] = "Piping reads Root AGENTS.md live and adopts it"
    neg("N-21 a manifest quote that is not in the manifest", n21, "evidence")

    def n22(v, s):
        e = [e for e in row(v, "APP-V4")["facts"]["published"]["evidence"] if e["kind"] == "git_commit"][0]
        e["ref"] = "0" * 40
    neg("N-22 publication citing a commit that does not exist", n22, "evidence")

    def n23(v, s):
        v["rows"] = [r for r in v["rows"] if not (r["renewal_id"] == "RN-2" and r["consumer_id"] == "RUNTIME")]
    neg("N-23 the RN-2 row for X-1 consumer Runtime removed", n23, "coverage")

    def n24(v, s):
        row(v, "APP-V3")["facts"]["delivered"].update({"state": "not_established", "evidence": []})
    neg("N-24 App v3's routed notice marked not delivered", n24, "routing")

    def n25(v, s):
        v["promise_trace"][0]["change_state"] = "applied"
    neg("N-25 a derivative marked 'applied' whose Design file does not mention the change", n25, "trace")

    def n26(v, s):
        s["renewed_basis"]["consumers_adopted"] = ["ROOT"]
        v["status"] = copy.deepcopy(s)
    neg("N-26 the renewed basis's status claiming an adopter that no RN-2 row establishes", n26, "status")

    bad = dict(files)
    bad["AA-1.status.json"] = files["AA-1.status.json"].replace(b"no receiving decision", b"a receiving decision")
    expect("N-27 a record byte changed after the manifest was written [refused by: K-2]", manifest_errors(bad, files["MANIFEST.sha256"].decode()))
    v = copy.deepcopy(acct)
    v["limits"] = v["limits"] + ["edited"]
    expect("N-28 an account edited after its build [refused by: K-3]", lambda: B.build(at) != v)
    expect("N-29 a home path in a record [refused by: K-11]", home_errors({"x": "see /" + "Users/someone/notes"}))

    # RV3 AA2-R1's two constructions (reviews/RV3-AA1.md addendum), reproduced as RV3 built them
    def n30(v, s):
        readme = "projects/chirality-app-dev/README.md"
        row(v, "APP-V3")["facts"]["delivered"]["evidence"] = [{"kind": "file_at_commit", "ref": readme, "sha256": B.blob(at, readme)[0],
                                                              "note": "AA2-R1 construction 1"}]
    neg("N-30 RV3 AA2-R1 construction 1: App v3 'delivered' shown by App v3's README (a real in-lane file, not the routed notice)", n30, "SR-2")

    upd = ("projects/chirality-app-dev/execution/PKG-07_Filesystem_Execution_Lifecycle_and_Dependencies/1_Working/"
           "DEL-07-05_Dependencies_csv_v3_1_Reader_Writer_and_Linter/ScopeOfWork.md")

    def n31(v, s):
        v["acts"].append({"act_id": "AD-X", "kind": "agent_act", "act_class": "adoption", "recording_mode": "direct capture", "consumer_id": "APP-V3",
                          "actor": "App v3 loop", "recorder": "App v3 loop", "recorder_stated_by_record": True,
                          "subject": "App v3 adopts D-GOV-52", "record_ref": upd + ", CLM-017",
                          "exact_text": "UPD-133 adopts the stricter live rule: every ACTIVE dependency row requires both `EvidenceFile` and `SourceRef`.",
                          "custody": "AA2-R1 construction 2"})
        r = row(v, "APP-V3")
        r["facts"]["consumer_adopted"] = {"state": "established", "evidence": [{"kind": "act", "ref": "AD-X"}]}
        r["adoption_point"] = "CLM-017"
        s["instruction_changes"][0]["adopted_by"] = ["APP-V3", "APP-V4"]
        v["status"] = copy.deepcopy(s)
    neg("N-31 RV3 AA2-R1 construction 2: App v3 'consumer adopted' by a real, unrelated App v3 sentence ('UPD-133 adopts …'), status updated to match",
        n31, "SR-3")
    expect("P-4 the real adoption AD-1's entry names RN-1 (R23-30's head names D-GOV-52); the UPD-133 entry does not",
           any(n in entry_of(B.blob(at, B.RUN + "/R23_RESOLUTIONS.md")[1], "App v4 adopts the changed Root text.")
               for n in renewal_names(acct["renewals"][0]))
           and not any(n in entry_of(B.blob(at, upd)[1], "UPD-133 adopts the stricter live rule")
                       for n in renewal_names(acct["renewals"][0])))

    expect("P-1 positive control: App v4's real adoption AD-1 passes SR-3 and SR-4; F-R16's statement is not adoption text",
           not [e for e in real["SR-3"] + real["SR-4"] if "APP-V4" in e]
           and adoption_text("App v4 adopts the changed Root text.") and not adoption_text("notice delivered; receiving decision not recorded"))
    expect("P-2 the status hand-over says 'delivered', not 'received', for App v3 and Runtime (AA1-R2; F-R16)",
           "received a notice" not in status["statement"] and "delivered to App v3's and Runtime's coordination folders" in status["statement"])
    rootrow = row(acct, "ROOT", "RN-2")
    expect("P-3 RN-2's Root search covers the whole repository outside App v4, and RV3's search is cited as a second one (AA1-R3)",
           ":(exclude)projects/chirality-app-v4" in rootrow["facts"]["consumer_adopted"]["evidence"][0]["ref"]
           and any("RV3" in e["ref"] for e in rootrow["facts"]["consumer_adopted"]["evidence"]))

    for name, ok, detail in results:
        print(("HOLDS " if ok else "FAILS ") + name + ("" if ok or not detail else "  -> %s" % (detail,)))
    failed = sum(1 for _, ok, _ in results if not ok)
    print("%d/%d expectations held" % (len(results) - failed, len(results)))
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
