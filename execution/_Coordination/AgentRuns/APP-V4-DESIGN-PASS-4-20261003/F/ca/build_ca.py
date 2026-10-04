"""Build DEL-11-01's continuity account CA-1 (CA-v0.1) as a linked view at one commit. Prototype, not product code.

Design: DEL-11-01 Design/CONTINUITY_ACCOUNT.md. Rulings: R23-32 (F-R6, F-R7, F-R8), R23-43, R23-44.

Everything that can be is read from git at the commit named (read-only: rev-parse, show, cat-file,
merge-base, rev-list), so a rebuild at the same commit gives the same bytes. The one input git cannot
hold is the Git-ignored archives: with --archives the builder runs the existing
`reference/archives/archive_digests.py verify` (read-only, ~20 s) and records only its summary; it never
records a path below an archive location or the archive root (a home path). Without --archives the
archive check is `not_run`. No network. Writes only F/ca/records/.

Usage: python3 -B build_ca.py --at <commit> [--archives]
"""

import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = subprocess.run(["git", "-C", HERE, "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
OUT = os.path.join(HERE, "records")  # not "out": the root .gitignore ignores **/out/ (R23-48)
DATE = "2026-10-04"
V4 = "projects/chirality-app-v4"
REFS = V4 + "/reference/REFERENCES.md"
ARCH = V4 + "/reference/archives/ARCHIVES.md"
DIGESTS = V4 + "/reference/archives/archive_digests.json"
TOOL = V4 + "/reference/archives/archive_digests.py"
INV = V4 + "/reference/SOURCE_INVENTORY.md"
PRD = V4 + "/docs/PRD.md"
DECISIONS = V4 + "/conceptual/DECISIONS.md"
OWNER_DEC = V4 + "/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/OWNER_DECISIONS.md"
HANDOFF30 = V4 + "/execution/_Coordination/HANDOFF_30_PERCENT.md"
THESIS = V4 + "/foundation/thesis"
THESIS_TREE = "47fc49e96c2931ba18090f1a82d56a49f230b3ee"  # docs/PRD.md §11
V301_SOURCE = "485051eac923c759238948a54cd7bb094eee4899"   # REFERENCES.md §2
V301_PREP = "cf4653526d2aa24976069275878f4fd4bedd0b9c"
INVESTIGATION = "2b0572fe049c8ffaa02d61b7dbbc3ae41bc589f6"  # REFERENCES.md §1
RUNS_TAG = "archive/agent-runs-2026-09-25"


def git(*a, check=True):
    return subprocess.run(["git", "-C", REPO] + list(a), capture_output=True, text=True, check=check).stdout.strip()


def blob_sha256(commit, path):
    data = subprocess.run(["git", "-C", REPO, "show", "%s:%s" % (commit, path)], capture_output=True, check=True).stdout
    return hashlib.sha256(data).hexdigest()


def text_at(commit, path):
    return git("show", "%s:%s" % (commit, path))


def is_ancestor(a, b):
    return subprocess.run(["git", "-C", REPO, "merge-base", "--is-ancestor", a, b]).returncode == 0


def build(at, run_archives):
    at = git("rev-parse", at)
    # --- C-1 fallback release (REFERENCES §2), local facts only -------------------------------
    pkg_version = json.loads(text_at(V301_SOURCE, "projects/chirality-app-dev/frontend/package.json"))["version"]
    refs = text_at(at, REFS)
    c1_ok = (pkg_version == "3.0.1" and is_ancestor(V301_PREP, V301_SOURCE) and is_ancestor(V301_SOURCE, at)
             and V301_SOURCE in refs and "eea43a0d973d1cd401da58cfd7a7156d9e932503fbb0c469a799e3cec73fd2e3" in refs)
    # --- C-2 App v3 lane -------------------------------------------------------------------------
    v3_tree = git("rev-parse", "%s:projects/chirality-app-dev" % at)
    v3_after = int(git("rev-list", "--count", "%s..%s" % (V301_SOURCE, at), "--", "projects/chirality-app-dev"))
    # --- C-4 thesis ------------------------------------------------------------------------------
    t_obs = git("rev-parse", "%s:%s" % (at, THESIS))
    t_files = len(git("ls-tree", "-r", "--name-only", at, "--", THESIS).splitlines())
    # --- C-5 investigation revision; C-6 archived run records ------------------------------------
    inv_type = git("cat-file", "-t", INVESTIGATION)
    tag_target = git("rev-parse", RUNS_TAG + "^{}")
    # --- C-3 archives (outside git) --------------------------------------------------------------
    if run_archives:
        r = subprocess.run([sys.executable, "-B", os.path.join(REPO, TOOL), "verify"], capture_output=True, text=True)
        lines = r.stdout.splitlines()
        ok_lines = [l for l in lines if l.startswith("OK")]
        if r.returncode == 0 and "All recorded archives unchanged." in r.stdout and len(ok_lines) == 19:
            arch_result = "passed"
        elif r.returncode == 1:
            arch_result = "changed"
        else:  # the tool did not run to a verdict: that is not a change (never report one)
            arch_result = "not_run"
        arch_observed = "%d of 19 locations OK; tool exit %d" % (len(ok_lines), r.returncode)
    else:
        arch_result, arch_observed = "not_run", "not run in this build"

    def link(path, kind="git_blob_sha256", locus=""):
        if kind == "git_blob_sha256":
            ident = {"kind": kind, "value": blob_sha256(at, path)}
        elif kind == "git_tree":
            ident = {"kind": kind, "value": git("rev-parse", "%s:%s" % (at, path))}
        else:
            raise ValueError(kind)
        d = {"path": path, "identity": ident}
        if locus:
            d["locus"] = locus
        return d

    classes = [
        {"class_id": "C-1", "name": "Fallback release Chirality v3.0.1",
         "what": "The published product that stays in place until the owner decides v4 has replaced it",
         "linked_records": [link(REFS, locus="§2 Fallback release (v3.0.1)"),
                            {"path": "sgttomas/chirality@" + V301_SOURCE, "identity": {"kind": "git_commit", "value": V301_SOURCE},
                             "locus": "desktop application source named by the release notes"}],
         "identity_check": {"method": "local git facts: the source commit exists, its frontend/package.json reads 3.0.1, the release-preparation commit is its ancestor, it is an ancestor of the account's commit, and REFERENCES §2 names it and the installer digest",
                            "result": "matches" if c1_ok else "differs", "expected": "all five facts hold",
                            "observed": "package.json version %s at %s" % (pkg_version, V301_SOURCE[:10]),
                            "limits": ["the published release and installer digest were not re-checked against the remote (no network); REFERENCES §2 is the record"]},
         "current_selector": "REFERENCES.md §2 (release, tag target, desktop source, installer digest)",
         "standing": "current_fallback",
         "recovery_route": "the published release named in REFERENCES §2; its source at the commit above, in this repository's history",
         "retained": True, "owner": "the owner (P-1 replacement; P-5 public release)",
         "point_of_need": "kept until the owner's replacement act (PRD §8; OD-09); never retired by this account"},
        {"class_id": "C-2", "name": "App v3 project lane",
         "what": "projects/chirality-app-dev: the v3 line's design, code, run records and coordination, still active",
         "linked_records": [link("projects/chirality-app-dev", "git_tree"), link("projects/chirality-app-dev/AGENTS.md")],
         "identity_check": {"method": "git tree id of the lane at the account's commit; commits touching it after the v3.0.1 source",
                            "result": "passed" if v3_tree and is_ancestor(V301_SOURCE, at) else "not_checked",
                            "observed": "tree %s; %d commits touch it after the v3.0.1 source" % (v3_tree[:12], v3_after),
                            "limits": ["the lane is active, so its identity changes with each commit; the account records it at one commit and does not freeze it (REQ-005)"]},
         "current_selector": "the lane's own entry (projects/chirality-app-dev/AGENTS.md) and _Coordination records; v4 citations treat it as historical evidence only",
         "standing": "active_lane",
         "recovery_route": "git history of this repository",
         "retained": True, "owner": "the App v3 loop's owner",
         "point_of_need": "its own scope; any retirement only by the owner with affected consumers (OI-024)"},
        {"class_id": "C-3", "name": "Git-ignored archives in the original checkout (19 locations)",
         "what": "Earlier App generations, domain corpora, plans, PEC and SWBPIPE planning records kept outside git",
         "linked_records": [link(ARCH), link(DIGESTS), link(TOOL)],
         "identity_check": {"method": "reference/archives/archive_digests.py verify (read-only; recomputes every recorded location and subtree digest)",
                            "result": arch_result, "observed": arch_observed,
                            "limits": ["runs only where the original checkout is present; worktrees do not carry the archives",
                                       "the committed digest file names nothing below the 19 locations (the repository is public)"]},
         "current_selector": "ARCHIVES.md (inventory, access rule, hazard: never run git clean -x or -X in the original checkout)",
         "standing": "preserved_evidence",
         "recovery_route": "read-only access in the original checkout, as ARCHIVES.md states; no other copy is recorded",
         "retained": True, "owner": "the owner (OD-09)",
         "point_of_need": "kept until the owner decides v4 has replaced the fallback (OD-09)"},
        {"class_id": "C-4", "name": "The complete thesis",
         "what": "foundation/thesis, kept unchanged with attribution and its nonbinding standing",
         "linked_records": [link(THESIS, "git_tree"), link(PRD, locus="§11")],
         "identity_check": {"method": "git tree id of foundation/thesis at the account's commit compared with the tree PRD §11 names",
                            "result": "matches" if t_obs == THESIS_TREE else "differs", "expected": THESIS_TREE, "observed": "%s (%d files)" % (t_obs, t_files),
                            "limits": ["committed-tree identity at the commit; working bytes are compared separately by check_ca.py",
                                       "attribution and nonbinding standing are inspected in CONTINUITY_ACCOUNT.md §4.3, not by this check"]},
         "current_selector": "PRD §11 (byte-identical to the named tree; purpose-level citation creates no v4 requirement)",
         "standing": "preserved_basis",
         "recovery_route": "git history; the tree id above",
         "retained": True, "owner": "the owner",
         "point_of_need": "always (REQ-003); never edited to conform"},
        {"class_id": "C-5", "name": "Investigation revision and source inventory",
         "what": "The repository revision the v4 conceptual undertaking read, and what each source can support",
         "linked_records": [link(REFS, locus="§1 Investigation revision"), link(INV),
                            {"path": "commit " + INVESTIGATION, "identity": {"kind": "git_commit", "value": INVESTIGATION}}],
         "identity_check": {"method": "the investigation commit exists in this repository", "result": "passed" if inv_type == "commit" else "changed",
                            "observed": "git cat-file -t: %s" % inv_type, "limits": []},
         "current_selector": "REFERENCES.md §1 and SOURCE_INVENTORY.md",
         "standing": "preserved_basis",
         "recovery_route": "git show <commit>:<path>",
         "retained": True, "owner": "the owner", "point_of_need": "kept with the accepted basis"},
        {"class_id": "C-6", "name": "Archived agent-run records",
         "what": "Closed run records moved out of the working tree and held at an annotated tag (D-GOV-45)",
         "linked_records": [{"path": "tag " + RUNS_TAG, "identity": {"kind": "git_tag_target", "value": tag_target}}, link(REFS, locus="§4")],
         "identity_check": {"method": "the annotated tag resolves to the commit REFERENCES §4 names",
                            "result": "matches" if tag_target.startswith("8007c592") else "differs", "expected": "8007c592…", "observed": tag_target, "limits": []},
         "current_selector": "the tag; REFERENCES §4",
         "standing": "preserved_evidence",
         "recovery_route": "git show <tag>:<path>",
         "retained": True, "owner": "Root governance owner", "point_of_need": "kept; no retirement proposed"},
        {"class_id": "C-7", "name": "External read-only archive named at the 30% gate",
         "what": "A read-only archive outside the repository, named in HANDOFF_30_PERCENT.md line 18 (its path is a home path and is not repeated here)",
         "linked_records": [link(HANDOFF30, locus="line 18"),
                            {"path": "outside the repository", "identity": {"kind": "outside_repository", "reason": "no digest record exists for it"}}],
         "identity_check": {"method": "none recorded", "result": "not_checked",
                            "limits": ["no inventory or digest of this archive exists in the repository; an identity check needs one (open item U-CA-2)"]},
         "current_selector": "HANDOFF_30_PERCENT.md line 18",
         "standing": "preserved_evidence",
         "recovery_route": "read-only access where it lives",
         "retained": True, "owner": "the owner", "point_of_need": "kept until the owner's replacement and retirement decisions"},
    ]

    lanes = [("App v3 (projects/chirality-app-dev)", "the App v3 loop's owner"),
             ("Chirality Runtime (projects/chirality-runtime)", "the Runtime loop's owner"),
             ("SWBPIPE (projects/chirality-piping)", "the SWBPIPE owner (outside session)"),
             ("Root governance and shared guidance", "the Root governance owner")]
    obligations = [{"lane": l, "lane_owner": o, "retirement_intended": False, "continuing_obligations": "not_supplied",
                    "disposition": None, "retirement_eligible": False,
                    "why": "no retirement is intended or proposed, and the lane owner has supplied no continuing-obligation disposition (DEP-006)",
                    "owner_of_decision": "Owner with affected consumers (OI-024)",
                    "point_of_need": "Before each adoption/retirement decision"} for l, o in lanes]

    od = text_at(at, DECISIONS)
    od09 = "Preserve the old projects and archives until I decide v4 has replaced the fallback."
    owner = text_at(at, OWNER_DEC)
    od2 = "1 yes, 2 no rewrite, 3 go, 4 A+C"
    if od09 not in od or od2 not in owner:
        sys.exit("an owner act's exact text is not in its record")
    acts = [
        {"act_id": "OD-09", "actor": "the owner", "recorder": "the v4 conceptual undertaking's recorder (conceptual/DECISIONS.md)",
         "subject": "preserve the old projects and archives until the owner decides v4 has replaced the fallback",
         "record_ref": DECISIONS + " row OD-09", "exact_text": od09,
         "custody": "the owner's direction as transcribed in DECISIONS.md; no platform timestamp",
         "bears_on": "C-1, C-2, C-3, C-7: all retained"},
        {"act_id": "APP-V4-DESIGN-PASS-4-20261003 direction item 2", "actor": "the owner", "recorder": "HELP_HUMAN",
         "subject": "git history is not rewritten for the home-path cleanup",
         "record_ref": OWNER_DEC + ", 'Direction'", "exact_text": od2,
         "custody": "the session transcript; recorded by HELP_HUMAN (its effect list reads: '2: git history is not rewritten')",
         "bears_on": "C-2, C-4, C-5, C-6: history recoverable from git as recorded"},
    ]

    handoff = {
        "record_kind": "continuity_handoff", "format": "CA-v0.1", "account_id": "CA-1", "account_version": 1,
        "at_commit": at,
        "account_sha256_note": "the account file's sha256 is in records/MANIFEST.sha256 (a record cannot hold its own hash)",
        "thesis_check": classes[3]["identity_check"],
        "fallback_identity": {"source": "projects/chirality-app-v4/reference/REFERENCES.md §2", "retained": True, "remote_rechecked": False},
        "archives": {"verify": arch_result, "source": ARCH},
        "continuing_obligations": {"status": "not_supplied", "owner": "Owner with affected consumers (OI-024)",
                                   "point_of_need": "Before each adoption/retirement decision"},
        "adoption_status": "not_supplied",
        "replacement_standing": "replacement pending; v3.0.1 retained",
        "disposition_ref": None,
    }
    return {
        "record_kind": "continuity_account", "format": "CA-v0.1", "account_id": "CA-1", "version": 1, "date": DATE,
        "at_commit": at, "classes": classes, "obligations": obligations, "owner_acts": acts,
        "adoption_status": {"status": "not_supplied", "supplier": "DEL-11-02",
                            "ref": "DEL-11-02's adoption account is not yet written; its first real entry (D-GOV-52) concerns Root guidance, not the renewed v4 basis's staged adoption"},
        "replacement_standing": {"state": "pending", "fallback": "v3.0.1 retained", "disposition_ref": None},
        "handoff": handoff,
        "limits": ["a linked view: it adds standing, selector, recovery route, owner and point of need to existing records and opens no archival audit (AX-003)",
                   "lane obligations are the lane owners' to supply; none is supplied yet",
                   "the archive check depends on the original checkout being present"],
    }


def main():
    args = sys.argv[1:]
    if "--at" not in args:
        sys.exit(__doc__)
    at = args[args.index("--at") + 1]
    acct = build(at, "--archives" in args)
    os.makedirs(OUT, exist_ok=True)
    data = (json.dumps(acct, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
    if re.search(rb"/Users/|/home/", data):
        sys.exit("refusing to write a home path")
    p = os.path.join(OUT, "CA-1.continuity-account.json")
    with open(p, "wb") as fh:
        fh.write(data)
    h = os.path.join(OUT, "CA-1.handoff.json")
    with open(h, "wb") as fh:
        fh.write((json.dumps(acct["handoff"], indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8"))
    with open(os.path.join(OUT, "MANIFEST.sha256"), "w", encoding="utf-8", newline="\n") as fh:
        for f in sorted(["CA-1.continuity-account.json", "CA-1.handoff.json"]):
            fh.write("%s  %s\n" % (hashlib.sha256(open(os.path.join(OUT, f), "rb").read()).hexdigest(), f))
    print("CA-1 written at %s; archives %s" % (acct["at_commit"][:10], acct["handoff"]["archives"]["verify"]))


if __name__ == "__main__":
    main()
