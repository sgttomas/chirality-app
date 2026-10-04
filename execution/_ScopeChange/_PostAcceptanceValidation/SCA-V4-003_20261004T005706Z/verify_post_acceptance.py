#!/usr/bin/env python3
"""AK2 part 1 (run APP-V4-SCA003-20261002): H-3, the SCA-V4-003 post-acceptance validation.

Recomputes the applied bytes from the accepted basis independently of apply_group3_edits.py and the finalize scripts,
and checks custody, pointer, boundary, snapshot completeness, the audit rerun (RUN/POSTACCEPT/), the supersession map
and DAG-003 currency. Writes POST_ACCEPTANCE_VALIDATION.md, post_acceptance_checks.json, DAG_CURRENCY.txt and
Supersession_Findings.csv into this folder. Read-only elsewhere (the accumulator check writes its map to SCRATCH).
Usage: verify_post_acceptance.py REPO SCRATCH [SIM_OUT_DIR]
"""
import csv, hashlib, io, json, os, re, subprocess, sys
from pathlib import Path

REPO, SCR = sys.argv[1], os.path.normpath(sys.argv[2])
SIM = os.path.normpath(sys.argv[3]) if len(sys.argv) > 3 else None
ACT, PRES = "84b520742d", "388fc730b9"
E = "projects/chirality-app-v4/execution"
RUN = f"{E}/_Coordination/AgentRuns/APP-V4-SCA003-20261002"
SC = f"{E}/_ScopeChange"
SNAP = "SCA-V4-003_2026-10-03_1827"
C = f"{SC}/{SNAP}"
G3 = f"{SC}/checkpoint_snapshots/SCA-V4-003_GROUP-3_2026-10-03"
PAV = f"{SC}/_PostAcceptanceValidation/SCA-V4-003_20261004T005706Z"
BA = f"{RUN}/AMENDMENT_PACKET/BASIS_AMENDMENT.md"
OD = f"{RUN}/OWNER_DECISIONS.md"
SD, LT = f"{E}/_Decomposition/SOFTWARE_DECOMP.md", f"{SC}/_LATEST.md"
ACT_TEXT = "I accept the audited result."
sha = lambda b: hashlib.sha256(b).hexdigest()
rb = lambda p: open(os.path.join(REPO, p), "rb").read()
def git(*a):
    return subprocess.run(["git", "-C", REPO, *a], capture_output=True, check=True).stdout
blob = lambda p, c=ACT: git("show", f"{c}:{p}")
checks, files = [], {}
def chk(cid, desc, ok, detail=""):
    checks.append({"id": cid, "check": desc, "result": "PASS" if ok else "FAIL", "detail": detail})

# ---- 1 custody and the group-3 snapshot ----
sys.path.insert(0, os.path.join(REPO, "tools/validation"))
import check_amendment_reopen as car
dec = rb(f"{G3}/DECISION.md").decode()
first = car._first_line(dec)
chk("1a", "group-3 DECISION.md first line is the accepted heading (check_amendment_reopen.py form)", bool(car._heading_re("SCA-V4-003").match(first)), first)
od = rb(OD).decode()
sec = od[od.index("## DECISION-2"):]
chk("1b", "the act text is quoted in DECISION.md and in the DECISION-2 section of OWNER_DECISIONS.md", f"> {ACT_TEXT}" in dec and f"> {ACT_TEXT}" in sec, ACT_TEXT)
chk("1c", "OWNER_DECISIONS.md custody hash equals the cited hash and its blob at 84b520742d",
    sha(rb(OD)) == "29c0a07b50d695a15bbff52b36d5925725cc7f3e78d0caf997ee9fd3c3b28c2e" == sha(blob(OD)), sha(rb(OD)))
changed = git("diff", "--name-only", PRES, ACT).decode().split()
chk("1d", "commit 84b520742d changes only OWNER_DECISIONS.md over the presentation commit 388fc730b9", changed == [OD], ";".join(changed))
man = list(csv.DictReader(io.StringIO(rb(f"{G3}/ACCEPTED_MANIFEST.csv").decode(), newline="")))
mm = [r["Path"] for r in man if sha(blob(r["Path"])) != r["SHA256"]]
chk("1e", "group-3 ACCEPTED_MANIFEST.csv binds the presented bytes (every row equals its blob at 84b520742d)", not mm, f"{len(man)} rows; mismatches {mm}")
chk("1f", "group-3 folder holds DECISION.md, ACCEPTED_MANIFEST.csv, Handoff_State.md",
    sorted(os.listdir(os.path.join(REPO, G3))) == ["ACCEPTED_MANIFEST.csv", "DECISION.md", "Handoff_State.md"], sorted(os.listdir(os.path.join(REPO, G3))))
store = car._WorkTree(Path(REPO).resolve())
try:
    g3path, _ = car._accepted_group3(store, SC, "SCA-V4-003", None)
    ent, lex, bsha, gman = car._bound_register(store, SC, "SCA-V4-003")
    ok = ent is not None and sha(rb(ent.path)) == bsha == "9b7c2ce8fbf97ec0cf829c5024e03d19b4117c1ca50abaea4ec0b2c340346d1c"
    chk("1g", "check_amendment_reopen.py (unanchored, read-only) finds the group-3 acceptance and the group-2 register at its bound hash", ok, f"{g3path}; {lex}; {bsha}")
except car._Refusal as e:
    chk("1g", "check_amendment_reopen.py finds the group-3 acceptance and the group-2 register", False, f"{e.code}: {e}")

# ---- 2 H-1 recomputed ----
ba_b = rb(BA)
chk("2a", "BASIS_AMENDMENT.md is the accepted bytes", sha(ba_b) == "151bc6fffcac482f6f8e77bf3d7b2822ec65f94012e0b66720f14644efbe35bf", sha(ba_b))
ba = ba_b.decode()
b01 = ba[ba.index("### B-01"):ba.index("### B-02")]
old = b01.split("```old\n", 1)[1].split("```", 1)[0]
new = b01.split("```new\n", 1)[1].split("```", 1)[0]
slot_rows = dict(re.findall(r"^\| `(\{\w+\})` \| (.*?) \|", b01, re.M))
vals = {"{ACCEPT_DATE}": "2026-10-03", "{AMENDMENT_SNAPSHOT}": SNAP}
for k in ("{Q5_CLAUSE}", "{OI018_CLAUSE}", "{D021_CLAUSE}"):
    vals[k] = re.search(r"`([^`]*)`", slot_rows[k]).group(1)
vals["{OI009_CLAUSE}"] = re.search(r"Q-10 B: `([^`]*)`", slot_rows["{OI009_CLAUSE}"]).group(1)
filled = new
for k, v in vals.items():
    filled = filled.replace(k, v)
pre_sd = blob(SD).decode()
exp_sd = pre_sd.replace(old, filled, 1).encode()
chk("2b", "B-01 old block occurs exactly once in the accepted state, the new block zero times", pre_sd.count(old) == 1 and pre_sd.count(filled) == 0, f"old {pre_sd.count(old)}, new {pre_sd.count(filled)}")
chk("2c", "SOFTWARE_DECOMP.md equals the accepted state + filled B-01, and the expected hash 983199cc...", rb(SD) == exp_sd and sha(exp_sd) == "983199cc22c84398000612cd95308c840ad011d302fe31ca110a5aa97e64a70d", sha(rb(SD)))
chk("2d", "SOFTWARE_DECOMP.md carries no unfilled slot and gained exactly two lines", not re.search(r"\{[A-Z0-9_]+\}", rb(SD).decode()) and len(rb(SD).decode().splitlines()) - len(pre_sd.splitlines()) == 2, json.dumps(vals))

# ---- 3 H-2 recomputed ----
chk("3a", "pre-act _LATEST.md (blob at 84b520742d) is 2b7938bc... naming SCA-V4-002", sha(blob(LT)) == "2b7938bc82aa9b08a2bd26d7f2c0169c538edb1e6ae5423d5757def968f0c2e1", sha(blob(LT)))
c01 = ba[ba.index("### C-01"):ba.index("### C-02")]
tmpl = c01.split("```text\n", 1)[1].split("```", 1)[0]
fills = {"{AMENDMENT_SNAPSHOT}": SNAP, "{ACCEPT_DATE}": "2026-10-03", "{CLOSURE_VERDICT}": "OPEN_PENDING_DERIVATIVE_CLOSURE",
         "{G1_DATE}": "2026-10-03", "{G2_DATE}": "2026-10-03", "{C02_UTC}": "20261004T002903Z", "{UTC}": "20261004T005706Z"}
for k, v in fills.items():
    tmpl = tmpl.replace(k, v)
lt = rb(LT)
chk("3b", "_LATEST.md equals the C-01 text with every slot filled and nothing else", lt == tmpl.encode(), sha(lt))
import validate_domain_decomposition_integrity as vdi
tgt = vdi._latest_pointer_target(Path(REPO, LT), allow_legacy_single_line=False)
match = vdi._pointer_matches(tgt, Path(REPO, C), Path(REPO, LT).parent)
chk("3c", "registered parser _latest_pointer_target resolves the pointer to the accepted snapshot and _pointer_matches is True", tgt == SNAP and match, f"target {tgt!r} match {match}")
ltl = lt.decode().splitlines()
chk("3d", "first two lines are 'Latest:' and 'Updated:' (SPEC 11.2 form)", ltl[0] == f"Latest: {SNAP}" and ltl[1] == "Updated: 2026-10-03", " / ".join(ltl[:2]))
act_lines = re.findall(r"^\*\*Active snapshot:\*\*\s*`([^`]+)`", lt.decode(), re.M)
chk("3e", "exactly one '**Active snapshot:**' line, naming the accepted snapshot", act_lines == [f"execution/_ScopeChange/{SNAP}/"], act_lines)
named = re.findall(r"`(execution/[^`]+)`", lt.decode())
missing = [p for p in named if not os.path.exists(os.path.join(REPO, "projects/chirality-app-v4", p))]
chk("3f", "every path _LATEST.md names exists", not missing, f"{len(named)} paths; missing {missing}")
chk("3g", "no unfilled slot in _LATEST.md", not re.search(r"\{[A-Z0-9_]+\}", lt.decode()), "")

# ---- 4 Consolidated_Coverage ----
cc = f"{E}/_Decomposition/Consolidated_Coverage.csv"
ccrows = list(csv.DictReader(io.StringIO(rb(cc).decode("utf-8-sig"), newline="")))
cols = [c for c in ccrows[0] if "path" in c.lower() or "source" in c.lower() or "doc" in c.lower()]
names_sd = [r for r in ccrows if any("SOFTWARE_DECOMP.md" in (r.get(c) or "") for c in ccrows[0])]
chk("4a", "Consolidated_Coverage.csv unchanged (no basis text changed) and no row names SOFTWARE_DECOMP.md", rb(cc) == blob(cc) and not names_sd, f"{sha(rb(cc))}; {len(ccrows)} rows")

# ---- 5 boundary ----
st = git("status", "--porcelain", "--untracked-files=all", "-z").decode().split("\0")
paths = sorted({l[3:] for l in st if l})
allowed = (f"{G3}/", f"{PAV}/", f"{RUN}/POSTACCEPT/", f"{RUN}/Application/")
allowed_files = {SD, LT, f"{C}/Decision_Log.md", f"{C}/Handoff_State.md", f"{C}/RUN_SUMMARY.md"}
outside = [p for p in paths if p not in allowed_files and not p.startswith(allowed)]
chk("5a", "every changed path since 84b520742d is inside the acceptance-time write boundary", not outside, f"{len(paths)} paths; outside {outside}")
forb = [p for p in paths if re.search(r"(ScopeOfWork\.md|Dependencies\.csv|_DEPENDENCIES\.md|/_DAG/|_STATUS\.md|_CONTEXT\.md|Coverage_Telemetry\.json|_LATEST_ACCEPTED\.md|Open_Issues\.csv)$|/_DAG/", p)]
chk("5b", "no ScopeOfWork, register, _DEPENDENCIES, _DAG, _STATUS, _CONTEXT, Coverage_Telemetry, _LATEST_ACCEPTED or Open_Issues byte changed", not forb, forb)
prior = [p for p in paths if "SCA-V4-001" in p or "SCA-V4-002" in p]
chk("5c", "no SCA-V4-001 or SCA-V4-002 byte changed", not prior, prior)
for g in ("GROUP-1", "GROUP-2"):
    rows = list(csv.DictReader(io.StringIO(rb(f"{SC}/checkpoint_snapshots/SCA-V4-003_{g}_2026-10-03/ACCEPTED_MANIFEST.csv").decode(), newline="")))
    mis = [r["Path"] for r in rows if sha(rb(r["Path"])) != r["SHA256"]]
    expected = {OD, f"{E}/_Decomposition/Open_Issues.csv"} if g == "GROUP-2" else {OD}
    chk(f"5d-{g}", f"{g} ACCEPTED_MANIFEST.csv rows still match (append-only custody record and, for group 2, the by-design pre-change Open_Issues row excepted)", set(mis) <= expected, f"{len(rows)} rows; mismatches {mis}")
art = {}
for line in rb(f"{RUN}/Application/CANDIDATE_ARTIFACTS.sha256").decode().splitlines():
    h, p = line.split("  ", 1); art[p] = h
diff_art = sorted(os.path.basename(p) for p, h in art.items() if sha(rb(p)) != h)
chk("5e", "of the 13 artifacts only the three status records changed (F-2..F-4); the other ten equal their presented hashes", diff_art == ["Decision_Log.md", "Handoff_State.md", "RUN_SUMMARY.md"], diff_art)
# F-2: reversing the two replacements and removing the appended section gives the presented bytes
dl = rb(f"{C}/Decision_Log.md").decode()
dl_pre = blob(f"{C}/Decision_Log.md").decode()
sec_start = dl.find("\n## Execution-stage records (node AK2 part 1, after DECISION-2)")
rev = dl[:sec_start] if sec_start >= 0 else dl
rev = rev.replace("**Standing: ACCEPTED amendment snapshot (posture `ACCEPTED_PREDECESSOR`);\ncheckpoint group 3 accepted by DECISION-2 on 2026-10-03.**",
                  "**Standing: CANDIDATE amendment folder (posture `ACCEPTED_PREDECESSOR`);\ncheckpoint group 3 not yet presented.**", 1)
rev = re.sub(r"\| DECISION-2 \| 2026-10-03 \| K2: scope-change group 3 \|[^\n]*\n", "", rev, count=1)
chk("5f", "F-2 changed only the standing lines, added the DECISION-2 row and appended the AK2 section", rev == dl_pre, "")
# F-3/F-4: the edits are the listed ones (verified by reproducing them from the presented bytes)
sys.path.insert(0, os.path.join(REPO, RUN, "Application"))
fs_src = open(os.path.join(REPO, RUN, "Application/finalize_status.py")).read()
ns = {}
exec(compile(fs_src.split("log = {}")[0], "finalize_status", "exec"), ns)
ok34 = True
for p, reps in ns["edits"].items():
    t = blob(p).decode()
    for o, n in reps:
        ok34 &= t.count(o) == 1
        t = t.replace(o, n, 1)
    ok34 &= t.encode() == rb(p)
chk("5g", "F-3 and F-4: reproducing the listed status-line replacements on the presented bytes gives the working files", ok34, "")

# ---- 6 snapshot completeness ----
req = ["Brief.md", "Intake_Actions.csv", "Impact_Assessment.md", "Amendment_Preview.md", "Propagation_Plan.md", "Amendment_Actions.csv",
       "Pre_Change_Coverage.json", "Post_Change_Coverage.json", "Decision_Log.md", "Handoff_State.md", "RUN_SUMMARY.md",
       "Supersession_Delta.csv", "Supersession_Map.csv"]
chk("6a", "active snapshot holds every required artifact", all(os.path.isfile(os.path.join(REPO, C, f)) for f in req), "13")
sca = sorted(d for d in os.listdir(os.path.join(REPO, SC)) if d.startswith("SCA-") and os.path.isdir(os.path.join(REPO, SC, d)))
complete = [d for d in sca if all(os.path.isfile(os.path.join(REPO, SC, d, f)) for f in req)]
chk("6b", "exactly three SCA-* amendment snapshot folders exist (two predecessors and the active one), all complete", sca == complete and len(sca) == 3, sca)

# ---- 7 audit ----
pa = f"{RUN}/POSTACCEPT"
s = json.load(open(os.path.join(REPO, pa, "coverage_summary.json")))
x = s["extensions"]
chk("7a", "audit-decomp rerun (unchanged baseline script): 0 BLOCKER", s["issues_blocker"] == 0, f"{s['issues_blocker']}/{s['issues_warning']}/{s['issues_info']}")
chk("7b", "the audit script is byte-identical to BASELINE/audit_checks.py", rb(f"{pa}/audit_checks.py") == rb(f"{RUN}/BASELINE/audit_checks.py"), sha(rb(f"{pa}/audit_checks.py")))
il = list(csv.DictReader(open(os.path.join(REPO, pa, "Decomp_Coverage_IssueLog.csv"), newline="")))
chk("7c", "no 'Historical snapshot residue' finding (COV-129 closed)", not [r for r in il if "residue" in r["Description"]], "")
chk("7d", "Check 10 active snapshot and handoff state PASS; active snapshot is SCA-V4-003; registered parser matches",
    s["active_snapshot_status"] == "PASS" and s["handoff_state_status"] == "PASS" and x["active_snapshot_check"]["active_snapshot"] == f"execution/_ScopeChange/{SNAP}"
    and x["registered_pointer_parser"].get("pointer_matches_active") is True, json.dumps(x["registered_pointer_parser"]))
chk("7e", "topology unchanged (11 packages, 41 deliverables, 10 objectives, 262 scope items)", s["repository_topology"] == {"packages": 11, "deliverables": 41, "objectives": 10, "scope_items": 262, "ledger_rows": 262}, json.dumps(s["repository_topology"]))
sim = json.load(open(os.path.join(REPO, RUN, "Application/simulated_postaccept.json")))
chk("7f", "counts equal the recorded simulation (0/51/77)", (sim["blocker"], sim["warning"], sim["info"]) == (s["issues_blocker"], s["issues_warning"], s["issues_info"]), f"simulation {sim['blocker']}/{sim['warning']}/{sim['info']}")
if SIM:
    same = all(open(os.path.join(SIM, f), "rb").read() == rb(f"{pa}/{f}") for f in ("Decomp_Coverage_IssueLog.csv", "Decomp_Coverage_Matrix.csv"))
    chk("7g", "IssueLog and Matrix byte-identical to the simulation's outputs (scratch copy of AK1-R's run)", same, "<scratch>/ak1r_sim/out")

# ---- 8 supersession ----
os.makedirs(SCR, exist_ok=True)
r = subprocess.run([sys.executable, os.path.join(REPO, "tools/coordination/accumulate_supersession_map.py"),
                    "--prior-map", os.path.join(REPO, SC, "SCA-V4-002_2026-09-29_1901/Supersession_Map.csv"),
                    "--delta", os.path.join(REPO, C, "Supersession_Delta.csv"),
                    "--output-map", os.path.join(SCR, "Supersession_Map.regen.csv"),
                    "--check-map", os.path.join(REPO, C, "Supersession_Map.csv"),
                    "--output-findings", os.path.join(REPO, PAV, "Supersession_Findings.csv")], capture_output=True, text=True)
chk("8", "accumulate_supersession_map.py --check-map on the active snapshot (prior = SCA-V4-002 map, delta = SCA-V4-003)", r.returncode == 0,
    " ".join(r.stdout.split()).replace(SCR, "<scratch>"))

# ---- 9 DAG and lifecycle ----
d = subprocess.run(["shasum", "-a", "256", "-c", "_DAG/DAG-003/SOURCE_MANIFEST.sha256"], cwd=os.path.join(REPO, E), capture_output=True, text=True)
d2 = subprocess.run(["shasum", "-a", "256", "-c", "MANIFEST.sha256"], cwd=os.path.join(REPO, E, "_DAG/DAG-003"), capture_output=True, text=True)
ok1 = d.stdout.count(": OK\n"); ok2 = d2.stdout.count(": OK\n")
open(os.path.join(REPO, PAV, "DAG_CURRENCY.txt"), "w").write(
    "# DAG-003 currency after SCA-V4-003 H-1/H-2 (AK2 part 1)\n# from projects/chirality-app-v4/execution: shasum -a 256 -c _DAG/DAG-003/SOURCE_MANIFEST.sha256\n"
    + d.stdout + d.stderr + f"exit {d.returncode}\n# from _DAG/DAG-003: shasum -a 256 -c MANIFEST.sha256\n" + d2.stdout + d2.stderr + f"exit {d2.returncode}\n")
chk("9a", "DAG-003 currency: SOURCE_MANIFEST (from the execution root) and MANIFEST all OK", d.returncode == 0 and d2.returncode == 0, f"{ok1} and {ok2} OK")
states = {}
for p in Path(REPO, E).glob("PKG-*/1_Working/*/_STATUS.md"):
    m = re.search(r"^\*\*Current State:\*\*\s*(\S+)", p.read_text(), re.M)
    states[m.group(1) if m else "?"] = states.get(m.group(1) if m else "?", 0) + 1
chk("9b", "no deliverable is ISSUED or CHECKING (the ISSUED-reopen rule does not apply)", not ({"ISSUED", "CHECKING"} & set(states)), json.dumps(states))

# ---- outputs ----
for p in (SD, LT, f"{C}/Decision_Log.md", f"{C}/Handoff_State.md", f"{C}/RUN_SUMMARY.md", f"{G3}/DECISION.md", f"{G3}/ACCEPTED_MANIFEST.csv", f"{G3}/Handoff_State.md"):
    files[p] = sha(rb(p))
res = "PASS" if all(c["result"] == "PASS" for c in checks) else "FAIL"
json.dump({"result": res, "checks": checks, "files": files}, open(os.path.join(REPO, PAV, "post_acceptance_checks.json"), "w"), indent=2)
md = ["# SCA-V4-003 post-acceptance validation", "",
      "Owner act: DECISION-2, 2026-10-03, America/Denver (\"I accept the audited result.\"; `checkpoint_snapshots/SCA-V4-003_GROUP-3_2026-10-03/`). "
      "Accepted basis `84b520742d` (candidate `fa16393978`, records `388fc730b9`). Applied state: uncommitted working tree over `84b520742d`. "
      "Record `SCA-V4-003_20261004T005706Z`, written by `verify_post_acceptance.py`, which recomputes the applied bytes from the accepted basis "
      "independently of `apply_group3_edits.py`. The candidate evidence reviewed at group 3 (POSTCHANGE/, V24) is not modified. No `ScopeOfWork.md`, "
      "register or DAG file is changed under this record: the 19 REVISEs, the register UPDATE and DAG-004 follow as propagation.", "",
      "| Check | Result | Detail |", "|---|---|---|"]
for c in checks:
    det = str(c["detail"]).replace("|", "\\|").replace("\n", " ")
    md.append(f"| {c['id']} {c['check']} | {c['result']} | {det} |")
md += ["", "## Applied and finalized files (sha256)", "", "| File | sha256 |", "|---|---|"]
md += [f"| `{p}` | `{h}` |" for p, h in files.items()]
md += ["", f"Result: {res}", ""]
open(os.path.join(REPO, PAV, "POST_ACCEPTANCE_VALIDATION.md"), "w").write("\n".join(md))
print(res, sum(c["result"] == "PASS" for c in checks), "/", len(checks))
for c in checks:
    if c["result"] != "PASS":
        print("FAIL", c["id"], c["detail"])
