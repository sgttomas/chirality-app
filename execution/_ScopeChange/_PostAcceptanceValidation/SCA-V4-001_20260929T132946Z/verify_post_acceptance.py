#!/usr/bin/env python3
"""AK2: post-acceptance validation of SCA-V4-001 (scope-change method, "After acceptance").

Read-only on everything except this record folder. It recomputes the applied state from the accepted
basis (commit 3d006a909) independently of apply_group3_edits.py and compares bytes.

Usage: verify_post_acceptance.py REPO SCRATCH_DIR
Writes: POST_ACCEPTANCE_VALIDATION.md, post_acceptance_checks.json, DAG_CURRENCY.txt,
        Supersession_Findings.csv (in this folder).
"""
import csv, hashlib, io, json, os, re, subprocess, sys

REPO, SCRATCH = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
BASIS = "3d006a909d722606b2f69f8c71a7020e5c86a619"
AID = "SCA-V4-001"
DATE = "2026-09-29"
SNAP = "SCA-V4-001_2026-09-28_2155"
P = "projects/chirality-app-v4"
EX = f"{P}/execution"
DEC = f"{EX}/_Decomposition"
SC = f"{EX}/_ScopeChange"
S = f"{SC}/{SNAP}"
G3 = f"{SC}/checkpoint_snapshots/{AID}_GROUP-3_{DATE}"
RUN = f"{EX}/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928"
PKT = f"{RUN}/AMENDMENT_PACKET/BASIS_AMENDMENT.md"
REC = os.path.relpath(HERE, REPO)
checks = []


def ok(name, cond, detail=""):
    checks.append({"check": name, "result": "PASS" if cond else "FAIL", "detail": detail})


def sha(b):
    return hashlib.sha256(b).hexdigest()


def cur(rel):
    return open(os.path.join(REPO, rel), "rb").read()


def at_basis(rel):
    return subprocess.run(["git", "-C", REPO, "show", f"{BASIS}:{rel}"], capture_output=True, check=True).stdout


def git(*a):
    return subprocess.run(["git", "-C", REPO, *a], capture_output=True, check=True).stdout.decode()


# ---- 1. group-3 decision folder ----
dec = cur(f"{G3}/DECISION.md").decode("utf-8")
first = next(l for l in dec.splitlines() if l.strip())
heading_re = re.compile(rf"^#\s+{re.escape(AID)}\s+checkpoint group 3\s+[—–-]+\s+accepted(?:\s|$|[.,;])", re.I)
ok("1a group-3 DECISION.md first line is the accepted heading (check_amendment_reopen.py form)", bool(heading_re.match(first)), first)
od_rel = f"{RUN}/OWNER_DECISIONS.md"
od = cur(od_rel)
labels = ['"Accept (Recommended)"', '"Record as stale, fix later (Recommended)"', '"Small follow-on amendment (Recommended)"']
ok("1b DECISION-8 labels quoted verbatim in DECISION.md and present in OWNER_DECISIONS.md",
   all(l in dec and l in od.decode("utf-8") for l in labels), "3/3 labels")
ok("1c OWNER_DECISIONS.md custody hash equals the cited hash and its blob at 3d006a909",
   sha(od) == sha(at_basis(od_rel)) == "752876c16f7f96ef5d63609d995596f1ac838152b561bc7b9c0b2aa6e3ddea10" and "752876c16f7f96ef5d63609d995596f1ac838152b561bc7b9c0b2aa6e3ddea10" in dec, sha(od))
man = list(csv.DictReader(io.StringIO(cur(f"{G3}/ACCEPTED_MANIFEST.csv").decode("utf-8"))))
bad = [r["Path"] for r in man if sha(at_basis(r["Path"])) != r["SHA256"]]
ok("1d group-3 ACCEPTED_MANIFEST.csv binds the presented bytes (every row equals its blob at 3d006a909)", not bad, f"{len(man)} rows; mismatches {bad}")
ok("1e group-3 folder holds DECISION.md, ACCEPTED_MANIFEST.csv, Handoff_State.md",
   sorted(os.listdir(os.path.join(REPO, G3))) == ["ACCEPTED_MANIFEST.csv", "DECISION.md", "Handoff_State.md"], str(sorted(os.listdir(os.path.join(REPO, G3)))))

# ---- 2. H-1..H-3 recomputed from the accepted text ----
pkt = cur(PKT)
ok("2a BASIS_AMENDMENT.md is the accepted bytes", sha(pkt) == "04bdc91622223510870ac8fe3994d708641c5e07a7853c5abc75ac59c0ed24cf", sha(pkt))
ba = pkt.decode("utf-8")
DOCS = {"PRD.md": f"{P}/docs/PRD.md", "ARCHITECTURE.md": f"{P}/docs/ARCHITECTURE.md", "HOST_INTEGRATION.md": f"{P}/docs/HOST_INTEGRATION.md",
        "EXAMINATION.md": f"{P}/docs/EXAMINATION.md", "_Decomposition/SOFTWARE_DECOMP.md": f"{DEC}/SOFTWARE_DECOMP.md"}
FILL = {"{AMENDMENT_ID}": AID, "{ACCEPT_DATE}": DATE, "{AMENDMENT_SNAPSHOT}": SNAP}
expect = {rel: at_basis(rel).decode("utf-8") for rel in DOCS.values()}
held = 0
for sec in re.split(r"^#### ", ba, flags=re.M)[1:]:
    eid = sec.splitlines()[0].split(" ")[0]
    if eid not in ("A07", "A17a", "A17b", "A17c", "D-15"):
        continue
    rel = DOCS[re.search(r"^Target: (\S+)", sec, re.M).group(1)]
    bl = re.findall(r"^```(old|new)\n(.*?)\n```$", sec, flags=re.M | re.S)
    for i in range(0, len(bl), 2):
        old, new = bl[i][1], bl[i + 1][1]
        for k, v in FILL.items():
            new = new.replace(k, v)
        c = expect[rel].count(old)
        ok(f"2b {eid} pair {i // 2 + 1}: filled old block occurs exactly once in the accepted candidate", c == 1, f"{rel} count {c}")
        expect[rel] = expect[rel].replace(old, new)
        held += 1
ok("2c seven held pairs found (A07 x3, A17a, A17b, A17c, D-15)", held == 7, str(held))
for rel, t in expect.items():
    got = cur(rel)
    ok(f"2d {rel} equals accepted candidate + filled edits", got == t.encode("utf-8"), sha(got))
    ok(f"2e {rel} carries no unfilled token", not re.search(r"\{(AMENDMENT_ID|ACCEPT_DATE|AMENDMENT_SNAPSHOT)\}", got.decode("utf-8")))

# ---- 3. H-4 recomputed ----
cc_rel = f"{DEC}/Consolidated_Coverage.csv"
b_rows = list(csv.reader(io.StringIO(at_basis(cc_rel).decode("utf-8"), newline="")))
c_rows = list(csv.reader(io.StringIO(cur(cc_rel).decode("utf-8"), newline="")))
hdr = b_rows[0]
ix = {c: hdr.index(c) for c in hdr}
doc4 = [v for k, v in DOCS.items() if "SOFTWARE_DECOMP" not in k]
exp_rows = [list(r) for r in b_rows]
blob = {}
for rel in doc4:
    data = cur(rel)
    h = subprocess.run(["git", "hash-object", "--stdin"], input=data, capture_output=True, check=True).stdout.decode().strip()
    blob[rel] = (sha(data), "git-blob:" + h, data.decode("utf-8").splitlines())
n4 = n_other = 0
for r in exp_rows[1:]:
    d = r[ix["Document"]]
    if d not in blob:
        n_other += 1
        continue
    n4 += 1
    s_, g_, L = blob[d]
    rid = r[ix["ConsolidatedRequirementID"]]
    pat = re.compile(r"^(- \*\*|\*\*|\| )" + re.escape(rid) + r"(?![0-9A-Za-z])")
    r[ix["SHA256"]], r[ix["ReadSnapshot"]] = s_, g_
    r[ix["SourceLine"]] = str(next(n + 1 for n, l in enumerate(L) if pat.search(l)))
o = io.StringIO(newline="")
csv.writer(o, lineterminator="\r\n").writerows(exp_rows)
ok("3a Consolidated_Coverage.csv equals the B8 rule applied to the accepted candidate and the applied documents", cur(cc_rel) == o.getvalue().encode("utf-8"), sha(cur(cc_rel)))
diffcols = {c for rb, rc in zip(b_rows[1:], c_rows[1:]) for c in hdr if rb[ix[c]] != rc[ix[c]]}
ok("3b only SHA256, ReadSnapshot and SourceLine changed; 126 rows recomputed, 18 other rows untouched",
   diffcols <= {"SHA256", "ReadSnapshot", "SourceLine"} and n4 == 126 and n_other == 18 and len(b_rows) == len(c_rows), f"cols {sorted(diffcols)}; {n4}/{n_other}")
suf = sum(1 for r in c_rows[1:] if r[ix["Standing"]].endswith(" amended by " + AID))
dbl = sum(1 for r in c_rows[1:] if r[ix["Standing"]].count("amended by") > 1)
ok("3c Standing: nine rows end 'amended by SCA-V4-001', none doubled", suf == 9 and dbl == 0, f"{suf}; doubled {dbl}")

# ---- 4. write containment ----
changed = [l[3:] for l in git("status", "--porcelain=v1", "-uall", "--", P).splitlines()]
changed = [c.strip('"') for c in changed]
allowed_mod = set(DOCS.values()) | {cc_rel, f"{S}/Handoff_State.md", f"{S}/RUN_SUMMARY.md", f"{S}/Decision_Log.md"}
allowed_new_prefix = (G3 + "/", f"{SC}/_LATEST.md", f"{SC}/_PostAcceptanceValidation/", f"{RUN}/POSTACCEPT/")
outside = [c for c in changed if c not in allowed_mod and not c.startswith(allowed_new_prefix)]
ok("4a every changed path is inside the post-acceptance write boundary", not outside, f"{len(changed)} paths; outside {outside}")
forbidden = [c for c in changed if re.search(r"(ScopeOfWork\.md|Dependencies\.csv|_DEPENDENCIES\.md|/_DAG/|_STATUS\.md|Coverage_Telemetry\.json)$|/_DAG/", c)]
ok("4b no ScopeOfWork.md, Dependencies.csv, _DEPENDENCIES.md, _DAG, _STATUS.md or Coverage_Telemetry.json changed", not forbidden, str(forbidden))
outside_proj = [l for l in git("status", "--porcelain=v1", "-uall").splitlines() if P not in l]
ok("4c nothing outside projects/chirality-app-v4 changed", not outside_proj, str(outside_proj))

# ---- 5. earlier bound records intact ----
for g in ("GROUP-1_2026-09-28", "GROUP-2_2026-09-28"):
    m = list(csv.DictReader(io.StringIO(cur(f"{SC}/checkpoint_snapshots/{AID}_{g}/ACCEPTED_MANIFEST.csv").decode("utf-8"))))
    # OWNER_DECISIONS.md is an append-only custody record bound at the DECISION-7 commit f4ba34c2c; it later gained
    # DECISION-8. It counts as intact when its blob at f4ba34c2c has the bound hash and is a byte prefix of the current file.
    badm, appended = [], []
    for r in m:
        if sha(cur(r["Path"])) == r["SHA256"]:
            continue
        old = subprocess.run(["git", "-C", REPO, "show", f"f4ba34c2c:{r['Path']}"], capture_output=True).stdout
        if r["Path"].endswith("/OWNER_DECISIONS.md") and sha(old) == r["SHA256"] and cur(r["Path"]).startswith(old):
            appended.append(r["Path"])
        else:
            badm.append(r["Path"])
    ok(f"5 {g} ACCEPTED_MANIFEST.csv rows still match the working tree (append-only custody record checked at f4ba34c2c)",
       not badm, f"{len(m)} rows; mismatches {badm}; append-only since binding {[os.path.basename(a) for a in appended]}")

# ---- 6. active pointer and snapshot ----
latest = cur(f"{SC}/_LATEST.md").decode("utf-8")
act = re.findall(r"^\*\*Active snapshot:\*\*\s*`([^`]+)`", latest, re.M)
ok("6a _LATEST.md names exactly one active snapshot, the accepted SCA-V4-001 folder", act == [f"execution/_ScopeChange/{SNAP}/"], str(act))
req = ["Brief.md", "Intake_Actions.csv", "Impact_Assessment.md", "Amendment_Preview.md", "Propagation_Plan.md", "Amendment_Actions.csv",
       "Pre_Change_Coverage.json", "Post_Change_Coverage.json", "Decision_Log.md", "Handoff_State.md", "RUN_SUMMARY.md",
       "Supersession_Delta.csv", "Supersession_Map.csv"]
miss = [f for f in req if not os.path.isfile(os.path.join(REPO, S, f))]
ok("6b active snapshot holds every required PROJECT/SOFTWARE artifact", not miss, f"missing {miss}")
hs = cur(f"{S}/Handoff_State.md").decode("utf-8")
need = ["SCA-V4-001_2026-09-28_2155", "STALE", "scope-of-work", "REVISE", "DAG-002", "STALE_REBUILD_REQUIRED", "decomposition owner",
        "OPEN_PENDING_DERIVATIVE_CLOSURE", "project-setup", "audit-scope-closure", "SCA-V4-002", "REQ-005", "HANDOFF_SWBPIPE_DOMAINS",
        "Allocation_Rationale", "NO_CHANGE", "scan_next_amendment_id.sh", "Crosswalk", "V11 F3"]
lack = [n for n in need if n not in hs]
ok("6c accepted Handoff_State.md names snapshot, derivative status, verdict, next workflows, residuals, crosswalk, F3", not lack, f"missing {lack}")
others = sorted(d for d in os.listdir(os.path.join(REPO, SC)) if d.startswith("SCA-") and os.path.isdir(os.path.join(REPO, SC, d)))
ok("6d exactly one SCA-* amendment snapshot folder exists", others == [SNAP], str(others))

# ---- 7. post-acceptance audit (POSTACCEPT) ----
cs = json.load(open(os.path.join(REPO, RUN, "POSTACCEPT/coverage_summary.json")))
crb = cs["extensions"]["section_binding"]["Change Register (scope-change, SOFTWARE)"]
ok("7a audit-decomp rerun: 0 BLOCKER", cs["issues_blocker"] == 0, f"{cs['issues_blocker']}/{cs['issues_warning']}/{cs['issues_info']}")
ok("7b Change Register binds ('Decision Log', rank exact); the COV-131 Change Register part is closed",
   any(b["target"] == "Decision Log" and b["rank"] == "exact" for b in crb), json.dumps(crb))
ok("7c Check 10 active snapshot and handoff state PASS", cs["active_snapshot_status"] == "PASS" and cs["handoff_state_status"] == "PASS",
   f"{cs['active_snapshot_status']}/{cs['handoff_state_status']}")
ok("7d topology unchanged (11 packages, 41 deliverables, 10 objectives, 262 scope items)",
   cs["repository_topology"] == {"packages": 11, "deliverables": 41, "objectives": 10, "scope_items": 262, "ledger_rows": 262}, json.dumps(cs["repository_topology"]))

# ---- 8. supersession map ----
os.makedirs(SCRATCH, exist_ok=True)
fnd = os.path.join(HERE, "Supersession_Findings.csv")
r = subprocess.run([sys.executable, os.path.join(REPO, "tools/coordination/accumulate_supersession_map.py"), "--delta", os.path.join(REPO, S, "Supersession_Delta.csv"),
                    "--output-map", os.path.join(SCRATCH, "Supersession_Map.regen.csv"), "--check-map", os.path.join(REPO, S, "Supersession_Map.csv"),
                    "--output-findings", fnd], capture_output=True, text=True)
ok("8 accumulate_supersession_map.py --check-map on the active snapshot", r.returncode == 0, (r.stdout + r.stderr).strip().replace(SCRATCH, "<scratch>").replace("\n", " "))

# ---- 9. DAG currency and lifecycle ----
d = subprocess.run(["shasum", "-a", "256", "-c", "_DAG/DAG-001/SOURCE_MANIFEST.sha256"], cwd=os.path.join(REPO, EX), capture_output=True, text=True)
open(os.path.join(HERE, "DAG_CURRENCY.txt"), "w").write(
    f"# cwd: {EX}\n# command: shasum -a 256 -c _DAG/DAG-001/SOURCE_MANIFEST.sha256\n# exit: {d.returncode}\n" + d.stdout + d.stderr)
nok = sum(1 for l in d.stdout.splitlines() if l.endswith(": OK"))
ok("9a DAG-001 currency (run from the execution root)", d.returncode == 0 and nok == 130, f"{nok}/130 OK, exit {d.returncode}")
states = {}
for root, _, files in os.walk(os.path.join(REPO, EX)):
    if "_STATUS.md" in files and "/1_Working/DEL-" in root:
        m = re.search(r"\*\*Current State:\*\*\s*([A-Z_]+)", open(os.path.join(root, "_STATUS.md"), encoding="utf-8").read())
        states[m.group(1) if m else "UNKNOWN"] = states.get(m.group(1) if m else "UNKNOWN", 0) + 1
ok("9b no deliverable is ISSUED (the ISSUED-reopen rule does not apply)", "ISSUED" not in states and sum(states.values()) == 41, json.dumps(states))

# ---- report ----
hashes = {rel: sha(cur(rel)) for rel in sorted(allowed_mod | {f"{SC}/_LATEST.md", f"{G3}/DECISION.md", f"{G3}/ACCEPTED_MANIFEST.csv", f"{G3}/Handoff_State.md"})}
res = "PASS" if all(c["result"] == "PASS" for c in checks) else "FAIL"
json.dump({"amendment": AID, "record": REC, "basis_commit": BASIS, "result": res, "checks": checks, "applied_hashes": hashes},
          open(os.path.join(HERE, "post_acceptance_checks.json"), "w"), indent=1, ensure_ascii=False)
L = [f"# {AID} post-acceptance validation", "",
     f"Owner act: DECISION-8, 2026-09-29 (\"Accept (Recommended)\"; `checkpoint_snapshots/{AID}_GROUP-3_{DATE}/`). Accepted basis `{BASIS[:9]}` "
     f"(candidate `230bf1e64`, presentation `9ae24fc0f`). Applied state: uncommitted working tree over `{BASIS[:9]}`. Record `{os.path.basename(HERE)}`. "
     "Written by `verify_post_acceptance.py`, which recomputes the applied bytes from the accepted basis independently of "
     "`apply_group3_edits.py`. The candidate evidence reviewed at group 3 (POSTCHANGE/, V11) is not modified.", "",
     "| Check | Result | Detail |", "|---|---|---|"]
L += [f"| {c['check']} | {c['result']} | {c['detail'].replace('|', '/')[:400]} |" for c in checks]
L += ["", "## Applied and finalized files (sha256)", "", "| File | sha256 |", "|---|---|"]
L += [f"| `{k}` | `{v}` |" for k, v in hashes.items()]
L += ["", f"Result: {res}", ""]
open(os.path.join(HERE, "POST_ACCEPTANCE_VALIDATION.md"), "w", encoding="utf-8").write("\n".join(L))
print(res, sum(c["result"] == "PASS" for c in checks), "/", len(checks))
for c in checks:
    if c["result"] != "PASS":
        print(c)
