"""Build DEL-11-02's adoption account AA-1 (AA-v0.2) from git at one commit. Prototype, not product code.

Design: DEL-11-02 Design/ADOPTION_ACCOUNT.md. Rulings: R23-30, R23-32 (F-R9, F-R10, F-R11, F-R16), R23-44.
Every fact cites evidence read from git at the commit (read-only: show, grep, rev-list, ls-tree); a rebuild
at the same commit gives the same bytes. Consumers come from DEL-10-03's X-1 (vendored RA-v0.2). No
network. Writes only F/aa/records/.

Usage: python3 -B build_aa.py --at <commit>
"""

import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = subprocess.run(["git", "-C", HERE, "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
OUT = os.path.join(HERE, "records")
DATE = "2026-10-04"
RUN = "projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003"
TRANCHE = "docs/governance_harness/tranche_manifests/ROOT-DGOV52-APPLICATION-20261004.yaml"
TRANCHE_COMMIT = "7bd2283dbc8de37e7d3c2963a83c81a499ede7fd"
BEFORE, AFTER = "c8ce87ef342902cb081bc659b26fc9a4edda1b6dba513814e5cb1e14e0b1dffd", "f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977"
NOTICE = "execution/_Coordination/NOTICE_2026-10-04_ROOT_D-GOV-52_AGENTS_MD_APP_V4_ALIGNMENT.md"
RESEARCH_PIN = "e548d4cfada4d2105de6231516dc6e5fc4bd4689"
V4 = "projects/chirality-app-v4"
DESIGN = {
    "ROLE-v0.2 F-R9": V4 + "/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-04_Additive role selection and supply/Design/ROLE_SUPPLY.md",
    "HOSTING-v0.9 §2/§8.2": V4 + "/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/HOSTING_BOUNDARY.md",
    "ACCESS-v0.2 §9/U-A9": V4 + "/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-05_Native OAuth-sign-in, API-key and local-provider access/Design/ACCOUNT_AND_PROVIDER_ACCESS.md",
}


def git(*a, check=True):
    return subprocess.run(["git", "-C", REPO] + list(a), capture_output=True, text=True, check=check).stdout.strip()


def blob(at, path):
    data = subprocess.run(["git", "-C", REPO, "show", "%s:%s" % (at, path)], capture_output=True, check=True).stdout
    return hashlib.sha256(data).hexdigest(), data.decode("utf-8")


def exists(at, path):
    return subprocess.run(["git", "-C", REPO, "cat-file", "-e", "%s:%s" % (at, path)], capture_output=True).returncode == 0


def grep_files(at, needle, lane):
    specs = lane if isinstance(lane, list) else [lane]
    out = subprocess.run(["git", "-C", REPO, "grep", "-l", "-F", needle, at, "--"] + specs, capture_output=True, text=True).stdout
    return sorted(l.split(":", 1)[1] for l in out.splitlines() if l)


def norm(t):
    return re.sub(r"\s+", " ", t)


def ev_file(at, path, note=None, quote=None):
    sha, text = blob(at, path)
    if quote is not None and norm(quote) not in norm(text):
        sys.exit("quote not in %s: %s" % (path, quote[:60]))
    e = {"kind": "file_at_commit", "ref": path, "sha256": sha}
    if quote:
        e["quote"] = quote
    if note:
        e["note"] = note
    return e


def F(state, evidence=(), note=None):
    d = {"state": state, "evidence": list(evidence)}
    if note:
        d["note"] = note
    return d


def build(at):
    at = git("rev-parse", at)
    root_sha, _ = blob(at, "AGENTS.md")
    if root_sha != AFTER:
        sys.exit("Root AGENTS.md at %s is not the D-GOV-52 bytes" % at[:10])
    published = F("established", [ev_file(TRANCHE_COMMIT, "AGENTS.md", "Root AGENTS.md after the tranche: sha256 equals the packet's predicted f96feb19…"),
                                  {"kind": "git_commit", "ref": TRANCHE_COMMIT, "note": "tranche ROOT-DGOV52-APPLICATION-20261004"}])
    _, man = blob(at, TRANCHE)
    routed = re.findall(r"^    - (projects/\S+NOTICE_\S+\.md)$", man, flags=re.M)
    lanes = {"APP-V4": "projects/chirality-app-v4", "APP-V3": "projects/chirality-app-dev", "RUNTIME": "projects/chirality-runtime",
             "PIPING": "projects/chirality-piping", "PEC": "projects/pec"}

    acts = [
        {"act_id": "A-1", "kind": "human_act", "act_class": "change_approval", "recording_mode": "faithful recording",
         "actor": "the owner", "recorder": "HELP_HUMAN", "recorder_stated_by_record": True,
         "subject": "apply edits A1 and B1 to Root AGENTS.md (D-GOV-52), on the terms HELP_HUMAN stated: notices to App v4 (substantive), App v3 and Runtime (informational), none to Piping or PEC",
         "record_ref": RUN + "/OWNER_DECISIONS_2.md, 'D-GOV-52 application'", "exact_text": "I approve A1 and B1, go ahead",
         "custody": "the session transcript; recorded by HELP_HUMAN (the file's own custody line)"},
        {"act_id": "AD-1", "kind": "agent_act", "act_class": "adoption", "recording_mode": "direct capture",
         "consumer_id": "APP-V4", "actor": "HELP_HUMAN, as App v4's integrator (R23 rulings)", "recorder": "HELP_HUMAN", "recorder_stated_by_record": True,
         "subject": "App v4 adopts the changed Root text (D-GOV-52)", "record_ref": RUN + "/R23_RESOLUTIONS.md, R23-30",
         "exact_text": "App v4 adopts the changed Root text.",
         "custody": "the ruling as written in R23_RESOLUTIONS.md ('Integrator: HELP_HUMAN'): direct capture, the integrator recording its own ruling; a receiving loop's own adoption, not the owner's act (F-R10)"},
    ]
    for a, path in (("A-1", RUN + "/OWNER_DECISIONS_2.md"), ("AD-1", RUN + "/R23_RESOLUTIONS.md")):
        act = [x for x in acts if x["act_id"] == a][0]
        if norm(act["exact_text"]) not in norm(blob(at, path)[1]):
            sys.exit("act text not in record: " + a)

    def notice_row(cid):
        lane = lanes[cid]
        path = lane + "/" + NOTICE
        routed_here = path in routed
        if not routed_here:
            why = ("The tranche manifest routes no notice here. Its rationale reads: \"Piping and PEC hold no pin or copy of either passage and read "
                   "Root AGENTS.md live\" (the manifest's statement; not observed)")
            return F("not_applicable", [{"kind": "manifest_statement", "ref": TRANCHE, "quote": "Piping and PEC hold no pin or copy of either passage and read Root AGENTS.md live"}], why), \
                F("not_applicable", [], "no notice was routed")
        return (F("established", [{"kind": "manifest_statement", "ref": TRANCHE, "note": "listed under m6_notice.routed_to"}]),
                F("established", [ev_file(at, path, "the notice file is present in the receiving loop's coordination folder; whether the loop read it is not recorded")]))

    def receiving(cid):
        lane = lanes[cid]
        hits = grep_files(at, "D-GOV-52", lane)
        after = int(git("rev-list", "--count", "%s..%s" % (TRANCHE_COMMIT, at), "--", lane))
        notice = lane + "/" + NOTICE
        others = [h for h in hits if h != notice]
        search = {"kind": "absence_search", "ref": "git grep -F 'D-GOV-52' %s -- %s" % (at[:10], lane),
                  "note": "%d file(s) mention D-GOV-52 besides the notice; %d commit(s) touch the lane after the tranche" % (len(others), after)}
        return others, search

    rows = []
    # App v4: adopted by its integrator (AD-1); Design-file updates pending next revision
    pn, dl = notice_row("APP-V4")
    rows.append({"renewal_id": "RN-1", "consumer_id": "APP-V4",
                 "facts": {"prepared_notice": pn, "delivered": dl, "published": published,
                           "resolved": F("not_established", [], "no App v4 build resolves its guidance yet"),
                           "supplied": F("not_established", [], "no App v4 candidate supplies instructions yet (DEL-02-04 O-3 has no supply record)"),
                           "provider_adopted": F("not_established", [], "no provider has been given the text"),
                           "observed_behavior": F("not_established", [], "nothing observed"),
                           "consumer_adopted": F("established", [{"kind": "act", "ref": "AD-1"}, ev_file(at, RUN + "/R23_RESOLUTIONS.md", quote="App v4 adopts the changed Root text.")],
                                                 "adopted by App v4's integrator; its Design files follow at their next revision (promise trace)")},
                 "adoption_point": "R23-30 (App v4 run APP-V4-DESIGN-PASS-4-20261003)", "open": None})
    for cid, owner in (("APP-V3", "the App v3 loop's owner"), ("RUNTIME", "the Runtime loop's owner")):
        pn, dl = notice_row(cid)
        others, search = receiving(cid)
        rows.append({"renewal_id": "RN-1", "consumer_id": cid,
                     "facts": {"prepared_notice": pn, "delivered": dl, "published": published,
                               "resolved": F("unknown", [], "how this lane resolves Root guidance is not observed by this account"),
                               "supplied": F("unknown", []), "provider_adopted": F("unknown", []), "observed_behavior": F("unknown", []),
                               "consumer_adopted": F("not_established" if not others else "unknown", [search],
                                                     "notice delivered; receiving decision not recorded (F-R16). The notice's 'This loop: … No adoption work is "
                                                     "expected' was written by the sending tranche, not by this loop" + ("" if cid == "APP-V3" else
                                                     "; the Runtime copy is byte-identical to App v3's and speaks of 'the v3 idle-boundary path and RB-SETTINGS'"))},
                     "adoption_point": None, "open": {"owner": owner, "point_of_need": "before this loop relies on the changed passages (its own decision)"}})
    for cid, owner in (("PIPING", "the SWBPIPE owner (outside session; human relay)"), ("PEC", "the PEC loop's owner")):
        pn, dl = notice_row(cid)
        others, search = receiving(cid)
        rows.append({"renewal_id": "RN-1", "consumer_id": cid,
                     "facts": {"prepared_notice": pn, "delivered": dl, "published": published,
                               "resolved": F("unknown", [], "the manifest states that it reads Root AGENTS.md live; not observed"),
                               "supplied": F("unknown", []), "provider_adopted": F("unknown", []), "observed_behavior": F("unknown", []),
                               "consumer_adopted": F("not_established", [search], "no adoption record; reading the Root file live is a supply route, not an adoption decision")},
                     "adoption_point": None, "open": {"owner": owner, "point_of_need": "its own; no notice was routed"}})
    # RN-2: the App v4 renewed basis, as staged adoption for the DEP-006 consumers (OI-024)
    basis = V4 + "/execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/ACCEPTANCE.md"
    for cid in ("ROOT", "RUNTIME", "APP-V3", "PIPING"):
        lane = {"ROOT": [".", ":(exclude)" + lanes["APP-V4"]], "RUNTIME": lanes["RUNTIME"], "APP-V3": lanes["APP-V3"], "PIPING": lanes["PIPING"]}[cid]
        hits = grep_files(at, "APP-V4-BASIS-20260926", lane)
        scope = ("the whole repository outside %s (Root's governance, workflows and every other lane)" % lanes["APP-V4"]) if cid == "ROOT" else lane
        searches = [{"kind": "absence_search", "ref": "git grep -F 'APP-V4-BASIS-20260926' %s -- %s" % (at[:10], " ".join("'%s'" % x for x in lane) if isinstance(lane, list) else lane),
                     "note": "scope: %s; %d file(s) mention it" % (scope, len(hits))}]
        if cid == "ROOT":
            searches.append({"kind": "absence_search", "ref": "reviews/RV3-AA1.md, AA1-R3",
                             "note": "a second search, by RV3 (not O-F): the same id over the whole repository outside projects/chirality-app-v4 at 122c5abcf5 found nothing"})
        rows.append({"renewal_id": "RN-2", "consumer_id": cid,
                     "facts": {"prepared_notice": F("not_established", [], "no adoption notice for the renewed v4 basis has been prepared"),
                               "delivered": F("not_established", []),
                               "published": F("established", [ev_file(at, basis, "the accepted App v4 basis is in this repository; publication is not adoption (V4-OPS-14)")]),
                               "resolved": F("not_applicable", []), "supplied": F("not_applicable", []), "provider_adopted": F("not_applicable", []),
                               "observed_behavior": F("not_applicable", []),
                               "consumer_adopted": F("not_established", searches,
                                                     "no first adopter is identified; that is the owner's decision with affected consumers (OI-024; P-4)")},
                     "adoption_point": None, "open": {"owner": "Owner with affected consumers (OI-024)", "point_of_need": "Before each adoption/retirement decision"}})

    export = "exports/chirality-app/export-manifest.csv"
    _, exp_text = blob(at, export)
    packaging = [
        {"item": "public export manifest (exports/chirality-app)", "consequence": "the export pins Root AGENTS.md; regenerated in the tranche to the new bytes",
         "state": "established" if ("AGENTS.md,14481," + AFTER) in exp_text else "not_established",
         "evidence": [ev_file(at, export, quote="AGENTS.md,14481," + AFTER), {"kind": "manifest_statement", "ref": TRANCHE, "quote": "status: regenerated"}]},
        {"item": "public export staging tree and publication", "consequence": "the staging tree is written outside the repository; no publication act is recorded",
         "state": "not_established", "evidence": [{"kind": "manifest_statement", "ref": TRANCHE, "quote": "The staging tree is written outside the repository and is not committed."}]},
    ]
    trace = []
    for label, path in DESIGN.items():
        sha, text = blob(at, path)
        applied = "D-GOV-52" in text or "R23-30" in text
        trace.append({"promise": "Root AGENTS.md's changed passages (A1 idle boundary / new conversations; B1 App-process settings)",
                      "from": "DEL-10-03 RA S-3 (guidance supply); R23-30", "owner": label.split()[0] + " owner",
                      "derivative": "%s (%s)" % (label, path.split("/1_Working/")[1].split("/")[0]),
                      "change_state": "applied" if applied else "pending_next_revision",
                      "evidence": [{"kind": "design_file_state", "ref": path, "sha256": sha,
                                    "note": "mentions D-GOV-52 or R23-30: %s" % ("yes" if applied else "no (R23-30: 'Each file is updated at its next revision')")}]})
    consumers = [
        {"consumer_id": "ROOT", "name": "Root governance and shared guidance", "lane": "AGENTS.md, docs/", "in_dep006": True, "owner": "the Root governance owner"},
        {"consumer_id": "APP-V4", "name": "Chirality App v4 (this project)", "lane": lanes["APP-V4"], "in_dep006": False, "owner": "App v4's integrator (HELP_HUMAN)"},
        {"consumer_id": "APP-V3", "name": "Chirality App v3", "lane": lanes["APP-V3"], "in_dep006": True, "owner": "the App v3 loop's owner"},
        {"consumer_id": "RUNTIME", "name": "Chirality Runtime", "lane": lanes["RUNTIME"], "in_dep006": True, "owner": "the Runtime loop's owner"},
        {"consumer_id": "PIPING", "name": "SWBPIPE", "lane": lanes["PIPING"], "in_dep006": True, "owner": "the SWBPIPE owner (outside session)"},
        {"consumer_id": "PEC", "name": "PEC", "lane": lanes["PEC"], "in_dep006": False, "owner": "the PEC loop's owner"},
    ]
    status = {"record_kind": "adoption_status", "format": "AA-v0.2", "account_id": "AA-1", "account_version": 2, "at_commit": at,
              "renewed_basis": {"consumers_adopted": [], "consumers_not_recorded": ["ROOT", "RUNTIME", "APP-V3", "PIPING"],
                                "owner": "Owner with affected consumers (OI-024)", "point_of_need": "Before each adoption/retirement decision"},
              "instruction_changes": [{"renewal_id": "RN-1", "adopted_by": ["APP-V4"], "not_recorded": ["APP-V3", "RUNTIME"], "no_notice": ["PIPING", "PEC"]}],
              "statement": "No consumer has adopted the renewed App v4 basis; first adopters are the owner's decision with affected consumers (OI-024). Of the one instruction change traced (D-GOV-52), App v4 adopted it; a notice was delivered to App v3's and Runtime's coordination folders, and no receiving decision is recorded (whether either loop read it is not shown); no notice was routed to Piping or PEC, by design."}
    return {
        "record_kind": "adoption_account", "format": "AA-v0.2", "account_id": "AA-1", "version": 2, "date": DATE, "at_commit": at,
        "renewals": [
            {"renewal_id": "RN-1", "kind": "instruction_change", "what": "D-GOV-52: Root AGENTS.md instruction-change timing (A1) and App-process settings (B1)",
             "source": {"path": "AGENTS.md", "before_sha256": BEFORE, "after_sha256": AFTER, "at": TRANCHE_COMMIT}, "change_record": TRANCHE, "approval_act": "A-1"},
            {"renewal_id": "RN-2", "kind": "renewed_basis", "what": "the accepted App v4 basis (APP-V4-BASIS-20260926), as a renewed basis other consumers may adopt in stages",
             "source": {"path": basis}, "change_record": None, "approval_act": None},
        ],
        "consumers": consumers, "rows": rows, "acts": acts, "packaging": packaging,
        "currency": [{"claim": "no consumer relies on the pinned research as a current implementation map in this account", "research_pin": RESEARCH_PIN,
                      "relied_on": False, "comparison": "not run: REQ-003 requires it before such reliance; none occurs here"}],
        "promise_trace": trace, "status": status,
        "limits": ["evidence is what git holds at the commit; whether a loop read a notice is not observable here",
                   "'unknown' facts stay unknown; they are never filled from the manifest's rationale",
                   "consumers come from DEL-10-03 RA-v0.2 X-1 (vendored), plus App v4 and PEC as recipients the tranche names"],
    }


def main():
    a = sys.argv[1:]
    if "--at" not in a:
        sys.exit(__doc__)
    acct = build(a[a.index("--at") + 1])
    os.makedirs(OUT, exist_ok=True)
    files = {"AA-1.adoption-account.json": acct, "AA-1.status.json": acct["status"]}
    for name, obj in files.items():
        data = (json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
        if re.search(rb"/Users/|/home/", data):
            sys.exit("refusing to write a home path")
        with open(os.path.join(OUT, name), "wb") as fh:
            fh.write(data)
    with open(os.path.join(OUT, "MANIFEST.sha256"), "w", encoding="utf-8", newline="\n") as fh:
        for n in sorted(files):
            fh.write("%s  %s\n" % (hashlib.sha256(open(os.path.join(OUT, n), "rb").read()).hexdigest(), n))
    print("AA-1 written at %s" % acct["at_commit"][:10])


if __name__ == "__main__":
    main()
