#!/usr/bin/env python3
"""AK1-R (run APP-V4-SCA003-20261002): simulate the SCA-V4-003 post-acceptance state on a scratch copy and audit it.

Usage: simulate_postaccept.py REPO SCRATCH OUT.json
  REPO     the worktree (read only)
  SCRATCH  an empty scratch directory; receives copies of projects/chirality-app-v4 and tools/, then the H-1 and H-2
           edits, then the audit outputs under SCRATCH/out/
Nothing is written under REPO except OUT.json (which should be RUN/Application/...).

H-1: BASIS_AMENDMENT B-01 old -> new with the group-2 clause slots, {ACCEPT_DATE} = TEST_DATE and
     {AMENDMENT_SNAPSHOT} = SCA-V4-003_2026-10-03_1827. The expected result hash is also computed for each date in DATES.
H-2: BASIS_AMENDMENT C-01 text with {CLOSURE_VERDICT} = OPEN_PENDING_DERIVATIVE_CLOSURE, {G1_DATE} = {G2_DATE} =
     2026-10-03, {C02_UTC} = 20261004T002903Z, {UTC} = TEST_UTC (a placeholder stamp; the real one is taken at H-3).
F-1..F-4 are not simulated: they write records the unchanged audit reads only for Check 10 file presence, the closure
verdict and the state fields, which the candidate records already carry in parsable form.
Then: tools/evaluation/audit_structure.py and RUN/BASELINE/audit_checks.py (unchanged), scope PKG-01,02,03,04,05,09,10.
"""
import hashlib, json, os, re, shutil, subprocess, sys

REPO, SCR, OUTJ = sys.argv[1:4]
EX = "projects/chirality-app-v4/execution"
RUN = f"{EX}/_Coordination/AgentRuns/APP-V4-SCA003-20261002"
BA = f"{RUN}/AMENDMENT_PACKET/BASIS_AMENDMENT.md"
BA_SHA = "151bc6fffcac482f6f8e77bf3d7b2822ec65f94012e0b66720f14644efbe35bf"
SNAP = "SCA-V4-003_2026-10-03_1827"
TEST_DATE = "2026-10-03"
DATES = ["2026-10-03", "2026-10-04"]
TEST_UTC = "20261004T120000Z"
CLAUSES = {
    "{Q5_CLAUSE}": ", including the App act control in DEL-01-04",
    "{OI009_CLAUSE}": "Open_Issues OI-009 Status (RESOLVED_BY_OWNER_DECISION) and Consequence",
    "{OI018_CLAUSE}": " and the OI-018 Consequence pointer",
    "{D021_CLAUSE}": "; and a Supersession_Delta row binding the GROUP3 OI-009 Status",
}
sha = lambda b: hashlib.sha256(b).hexdigest()


def fail(m):
    raise SystemExit("FAIL: " + m)


ba_raw = open(os.path.join(REPO, BA), "rb").read()
if sha(ba_raw) != BA_SHA:
    fail("BASIS_AMENDMENT.md is not the accepted bytes")
ba = ba_raw.decode("utf-8")

if os.listdir(SCR):
    fail("scratch directory is not empty")
repo = os.path.join(SCR, "repo")
for d in ("projects/chirality-app-v4", "tools"):
    shutil.copytree(os.path.join(REPO, d), os.path.join(repo, d), symlinks=True,
                    ignore=shutil.ignore_patterns("__pycache__"))

# ---- H-1 ----
b01 = ba[ba.index("### B-01"):ba.index("**Slot rules**")]
old = re.search(r"```old\n(.*?)```", b01, re.S).group(1)
new_t = re.search(r"```new\n(.*?)```", b01, re.S).group(1)
sd_rel = f"{EX}/_Decomposition/SOFTWARE_DECOMP.md"
sd = open(os.path.join(repo, sd_rel), "rb").read().decode("utf-8")
if sd.count(old) != 1:
    fail(f"B-01 old block occurs {sd.count(old)} times")


def fill_b01(date):
    t = new_t.replace("{ACCEPT_DATE}", date).replace("{AMENDMENT_SNAPSHOT}", SNAP)
    for k, v in CLAUSES.items():
        t = t.replace(k, v)
    if "{" in t:
        fail("B-01 slot left unfilled")
    return t


h1 = {"before_sha256": sha(sd.encode()), "old_block_count": 1, "expected_by_date": {}}
for dt in DATES:
    t = fill_b01(dt)
    res = sd.replace(old, t, 1)
    added = len(res.splitlines()) - len(sd.splitlines())
    if res.count(t) != 1 or added != 2:
        fail(f"B-01 result for {dt}: added {added} lines")
    h1["expected_by_date"][dt] = {"sha256": sha(res.encode()), "lines_added": added}
res = sd.replace(old, fill_b01(TEST_DATE), 1)
open(os.path.join(repo, sd_rel), "wb").write(res.encode("utf-8"))
h1["applied_date"] = TEST_DATE
h1["applied_sha256"] = sha(res.encode())

# ---- H-2 ----
c01 = ba[ba.index("### C-01"):ba.index("### C-02")]
ptxt = re.search(r"```text\n(.*?)```", c01, re.S).group(1)
fills = {"{AMENDMENT_SNAPSHOT}": SNAP, "{ACCEPT_DATE}": TEST_DATE, "{CLOSURE_VERDICT}": "OPEN_PENDING_DERIVATIVE_CLOSURE",
         "{G1_DATE}": "2026-10-03", "{G2_DATE}": "2026-10-03", "{C02_UTC}": "20261004T002903Z", "{UTC}": TEST_UTC}
for k, v in fills.items():
    ptxt = ptxt.replace(k, v)
if "{" in ptxt:
    fail("C-01 slot left unfilled")
lt_rel = f"{EX}/_ScopeChange/_LATEST.md"
before = open(os.path.join(repo, lt_rel), "rb").read()
open(os.path.join(repo, lt_rel), "wb").write(ptxt.encode("utf-8"))
sys.path.insert(0, os.path.join(repo, "tools/validation"))
from pathlib import Path
import validate_domain_decomposition_integrity as vdi
tgt = vdi._latest_pointer_target(Path(repo, lt_rel), allow_legacy_single_line=False)
match = vdi._pointer_matches(tgt, Path(repo, EX, "_ScopeChange", SNAP), Path(repo, lt_rel).parent)
h2 = {"before_sha256": sha(before), "applied_sha256": sha(ptxt.encode()), "fills": fills,
      "parser_target": tgt, "pointer_matches": match}

# ---- audit ----
out = os.path.join(SCR, "out")
os.makedirs(out)
shutil.copy(os.path.join(REPO, RUN, "POSTCHANGE/inventory.json"), os.path.join(out, "inventory.json"))
r1 = subprocess.run([sys.executable, "audit_structure.py", "--root", "../../projects/chirality-app-v4/execution", "--variant",
                     "SOFTWARE", "--output", os.path.join(out, "structure.json"), "--inventory", os.path.join(out, "inventory.json")],
                    cwd=os.path.join(repo, "tools/evaluation"), capture_output=True, text=True)
script = os.path.join(REPO, RUN, "BASELINE/audit_checks.py")
env = dict(os.environ, RUN_LABEL="APP_V4_SCA_V4_003_SIMULATED_POSTACCEPT", HANDOFF_PHASE="simulation of SCA-V4-003 after group-3 acceptance (H-1, H-2 applied to a scratch copy)",
           RUN_TS="simulation", BASIS_COMMIT="scratch")
r2 = subprocess.run([sys.executable, script, repo, out, "PKG-01,PKG-02,PKG-03,PKG-04,PKG-05,PKG-09,PKG-10"], env=env,
                    capture_output=True, text=True)
summ = json.load(open(os.path.join(out, "coverage_summary.json")))
ext = summ["extensions"]
import csv
issues = list(csv.DictReader(open(os.path.join(out, "Decomp_Coverage_IssueLog.csv"), newline="")))
pc = list(csv.DictReader(open(os.path.join(REPO, RUN, "POSTCHANGE/Decomp_Coverage_IssueLog.csv"), newline="")))
key = lambda r: tuple(v for c, v in r.items() if c != "IssueID")
only_post = [r["IssueID"] + " " + r["Severity"] + " " + r["Description"][:160] for r in pc if key(r) not in {key(x) for x in issues}]
only_sim = [r["IssueID"] + " " + r["Severity"] + " " + r["Description"][:160] for r in issues if key(r) not in {key(x) for x in pc}]
result = {
    "script_sha256": sha(open(script, "rb").read()), "audit_structure_exit": r1.returncode, "audit_checks_exit": r2.returncode,
    "H1": h1, "H2": h2,
    "blocker": summ["issues_blocker"], "warning": summ["issues_warning"], "info": summ["issues_info"],
    "active_snapshot_status": summ["active_snapshot_status"], "handoff_state_status": summ["handoff_state_status"],
    "check10": {k: ext.get("active_snapshot_check", {}).get(k) for k in ("status", "active_snapshot", "closure_verdict", "state_fields", "missing", "incomplete_residue", "problems")},
    "registered_pointer_parser": ext.get("registered_pointer_parser"),
    "expected_source_unequal": [f["path"] for f in ext.get("expected_source", {}).get("files", []) if not f.get("equal")],
    "issues_only_in_POSTCHANGE": only_post, "issues_only_in_simulation": only_sim,
    "matrix_identical_to_POSTCHANGE": open(os.path.join(out, "Decomp_Coverage_Matrix.csv"), "rb").read() == open(os.path.join(REPO, RUN, "POSTCHANGE/Decomp_Coverage_Matrix.csv"), "rb").read(),
}
json.dump(result, open(OUTJ, "w"), indent=2)
print(json.dumps({k: result[k] for k in ("blocker", "warning", "info", "active_snapshot_status", "handoff_state_status")}, indent=1))
