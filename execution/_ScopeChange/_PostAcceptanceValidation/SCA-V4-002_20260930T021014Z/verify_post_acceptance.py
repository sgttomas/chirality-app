#!/usr/bin/env python3
"""AK2: post-acceptance validation of SCA-V4-002 (scope-change method, "After acceptance").

Read-only on everything except this record folder. It recomputes the applied state from the accepted
basis (commit 851ec3d88) independently of apply_group3_edits.py and compares bytes.

Usage: verify_post_acceptance.py REPO SCRATCH_DIR
Writes: POST_ACCEPTANCE_VALIDATION.md, post_acceptance_checks.json, DAG_CURRENCY.txt,
        Supersession_Findings.csv (in this folder).
"""
import csv, hashlib, io, json, os, re, subprocess, sys

REPO, SCRATCH = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
BASIS = "851ec3d88bb090f0bc63ad7075b1668ad65afb39"
PRES = "ffdb56e1a438dfd4014a7b4a4f2a2c5fce2e74fd"
CAND = "70376aff2fb7a46f4731803e7988e42c2e8f2366"
AID = "SCA-V4-002"
DATE = "2026-09-29"
SNAP = "SCA-V4-002_2026-09-29_1901"
PRED = "SCA-V4-001_2026-09-28_2155"
UTC = "20260930T021014Z"
P = "projects/chirality-app-v4"
EX = f"{P}/execution"
DEC = f"{EX}/_Decomposition"
SC = f"{EX}/_ScopeChange"
S = f"{SC}/{SNAP}"
G3 = f"{SC}/checkpoint_snapshots/{AID}_GROUP-3_{DATE}"
RUN = f"{EX}/_Coordination/AgentRuns/APP-V4-SCA002-20260929"
PKT = f"{RUN}/AMENDMENT_PACKET/BASIS_AMENDMENT.md"
PACKET_SHA = "091871fd90283b27b2d067c1eeb3137e3cf8f9d50dab87ad92a9b871cc634238"
OD_SHA = "f2dda563beaadc737c73d897d6801a78332e5a722334dd8ef6d26c0dd0c38ef3"
C02 = "execution/_ScopeChange/_PostAcceptanceValidation/SCA-V4-001_20260930T010520Z_EFFECTIVE_STATE/EFFECTIVE_STATE.md"
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


TOKEN = re.compile(r"\{[A-Z_0-9]+\}")

# ---- 1. group-3 decision folder ----
dec = cur(f"{G3}/DECISION.md").decode("utf-8")
first = next(l for l in dec.splitlines() if l.strip())
heading_re = re.compile(rf"^#\s+{re.escape(AID)}\s+checkpoint group 3\s+[—–-]+\s+accepted(?:\s|$|[.,;])", re.I)
ok("1a group-3 DECISION.md first line is the accepted heading (check_amendment_reopen.py form)", bool(heading_re.match(first)), first)
od_rel = f"{RUN}/OWNER_DECISIONS.md"
od = cur(od_rel)
label = '"Accept (Recommended)"'
ok("1b DECISION-3 label quoted verbatim in DECISION.md and present in the DECISION-3 section of OWNER_DECISIONS.md",
   label in dec and label in od.decode("utf-8").split("DECISION-3", 1)[1], label)
ok("1c OWNER_DECISIONS.md custody hash equals the cited hash and its blob at 851ec3d88",
   sha(od) == sha(at_basis(od_rel)) == OD_SHA and OD_SHA in dec, sha(od))
ok("1d commit 851ec3d88 changes only OWNER_DECISIONS.md over the presentation commit ffdb56e1a",
   git("diff", "--name-only", PRES, BASIS).split() == [od_rel], git("diff", "--name-only", PRES, BASIS).strip())
man = list(csv.DictReader(io.StringIO(cur(f"{G3}/ACCEPTED_MANIFEST.csv").decode("utf-8"))))
bad = [r["Path"] for r in man if sha(at_basis(r["Path"])) != r["SHA256"]]
ok("1e group-3 ACCEPTED_MANIFEST.csv binds the presented bytes (every row equals its blob at 851ec3d88)", not bad, f"{len(man)} rows; mismatches {bad}")
ok("1f group-3 folder holds DECISION.md, ACCEPTED_MANIFEST.csv, Handoff_State.md",
   sorted(os.listdir(os.path.join(REPO, G3))) == ["ACCEPTED_MANIFEST.csv", "DECISION.md", "Handoff_State.md"], str(sorted(os.listdir(os.path.join(REPO, G3)))))
reg_row = [r for r in man if r["Path"].endswith("/Amendment_Actions.csv")]
ok("1g the manifest binds the register at the group-2 hash", len(reg_row) == 1 and reg_row[0]["SHA256"] == "158702bf610777e008e304268fcbd967756f9186ded946942430a391957c579d" and sha(cur(f"{S}/Amendment_Actions.csv")) == "158702bf610777e008e304268fcbd967756f9186ded946942430a391957c579d", reg_row[0]["SHA256"] if reg_row else "")

# ---- 2. H-1 (B-04) recomputed from the accepted text ----
pkt = cur(PKT)
ok("2a BASIS_AMENDMENT.md is the accepted bytes", sha(pkt) == PACKET_SHA, sha(pkt))
ba = pkt.decode("utf-8")
sec = ba.split("### B-04 · ", 1)[1].split("\n### ", 1)[0]
blocks = re.findall(r"^```(old|new)\n(.*?)\n```$", sec, flags=re.M | re.S)
old, new = blocks[0][1], blocks[1][1]
FILL = {"{ACCEPT_DATE}": DATE, "{AMENDMENT_SNAPSHOT}": SNAP,
        "{Q6_CLAUSE}": ", DEL-04-02 and DEL-01-01",
        "{Q7_CLAUSE}": "; the OI-012 pointer in Open_Issues.csv",
        "{Q11_CLAUSE}": "; Deliverables DEL-04-01 (checkpoint clause) with its _CONTEXT.md mirror",
        "{Q12_CLAUSE}": '; a reading-rule note ("GROUP3 as amended by the active _ScopeChange/_LATEST.md") on _LATEST.md, checkpoint_snapshots/_LATEST_ACCEPTED.md and five _CONTEXT.md basis lines',
        "{Q10_CLAUSE}": "; and path-level Supersession_Delta rows for SCA-V4-001 actions 18–25, 36, 42 and 46"}
# the clause texts are taken from the B-04 slot table itself
tbl = dict(re.findall(r"^\| `(\{Q\d+_CLAUSE\})` \| `([^`]*)` if ", sec, re.M))
ok("2b the five clause texts equal the B-04 slot table", all(tbl.get(k) == v for k, v in FILL.items() if k.startswith("{Q")), str(sorted(tbl)))
filled = new
for k, v in FILL.items():
    filled = filled.replace(k, v)
sd_rel = f"{DEC}/SOFTWARE_DECOMP.md"
sd_basis = at_basis(sd_rel).decode("utf-8")
ok("2c B-04 filled old block occurs exactly once in the accepted candidate", sd_basis.count(old) == 1 and sd_basis.count(filled) == 0, f"old {sd_basis.count(old)}, new {sd_basis.count(filled)}")
expect_sd = sd_basis.replace(old, filled)
ok("2d SOFTWARE_DECOMP.md equals accepted candidate + filled B-04", cur(sd_rel).decode("utf-8") == expect_sd, sha(cur(sd_rel)))
ok("2e SOFTWARE_DECOMP.md carries no unfilled token", not TOKEN.search(cur(sd_rel).decode("utf-8")), "")
ok("2f Q-5 option A: no 'OI-001/OI-002 Status' clause in the entry", "; OI-001/OI-002 Status" not in cur(sd_rel).decode("utf-8"), "")

# ---- 3. H-2 (C-01) ----
secc = ba.split("## Part C — ", 1)[1].split("\n### C-02", 1)[0]
tmpl = re.findall(r"^```text\n(.*?)\n```$", secc, flags=re.M | re.S)[0]
lt_rel = f"{SC}/_LATEST.md"
lt = cur(lt_rel).decode("utf-8")
ok("3a pre-act _LATEST.md at the basis named the predecessor (sha a9a7cdc8...)", sha(at_basis(lt_rel)) == "a9a7cdc8c50a36fbdd25fc53c72322972ba4f9b4d301d811e1a9c1381966339d" and PRED in at_basis(lt_rel).decode("utf-8"), sha(at_basis(lt_rel)))
# structural: template with slots -> regex
pat = re.escape(tmpl)
slot_names = sorted(set(TOKEN.findall(tmpl)))
for s in slot_names:
    # first occurrence is a named group; every later occurrence must repeat the same value (backreference)
    pat = pat.replace(re.escape(s), f"(?P<{s[1:-1]}>.+?)", 1).replace(re.escape(s), f"(?P={s[1:-1]})")
m = re.fullmatch(pat, lt.rstrip("\n"), flags=re.S)
ok("3b _LATEST.md equals the C-01 template with every slot filled and nothing else changed", m is not None, str(slot_names))
vals = m.groupdict() if m else {}
consistent = m is not None and all(len(set(vals[k] for k in vals if k == kk)) == 1 for kk in vals)
ok("3c slot values: AMENDMENT_SNAPSHOT, ACCEPT_DATE, AMENDMENT_ID, CLOSURE_VERDICT, UTC, ARC_LIST",
   m is not None and vals.get("AMENDMENT_SNAPSHOT") == SNAP and vals.get("ACCEPT_DATE") == DATE and vals.get("AMENDMENT_ID") == AID
   and vals.get("CLOSURE_VERDICT") == "OPEN_PENDING_DERIVATIVE_CLOSURE" and vals.get("UTC") == UTC and vals.get("ARC_LIST") == "N-18, N-21, N-24 and X-1",
   json.dumps({k: vals.get(k) for k in ("AMENDMENT_SNAPSHOT", "ACCEPT_DATE", "AMENDMENT_ID", "CLOSURE_VERDICT", "UTC", "ARC_LIST")}))
# repeated tokens must agree: check each slot's every occurrence
rep_ok = True
if m:
    filled_t = tmpl
    for k, v in vals.items():
        filled_t = filled_t.replace("{" + k + "}", v)
    rep_ok = filled_t + "\n" == lt
ok("3d every repeated slot carries the same value (template refilled reproduces the file)", rep_ok, "")
ok("3e GROUP12_REFS names the two actual decision folders", m is not None and all(f"checkpoint_snapshots/{AID}_GROUP-{n}_{DATE}/" in vals.get("GROUP12_REFS", "") for n in (1, 2)), vals.get("GROUP12_REFS", ""))
ok("3f SCA001_CLOSURE is OPEN_PENDING_DERIVATIVE_CLOSURE and cites the C-02 record at its committed path", m is not None and "OPEN_PENDING_DERIVATIVE_CLOSURE" in vals.get("SCA001_CLOSURE", "") and C02 in vals.get("SCA001_CLOSURE", "") and os.path.isfile(os.path.join(REPO, P, C02)), vals.get("SCA001_CLOSURE", ""))
open_needed = ["9 ScopeOfWork REVISEs", "B-06a", "dependency-register", "DAG-003", "Coverage_Telemetry.json", "17 Design re-pins", "ASC-ISS-001", "audit-scope-closure"]
ok("3g OPEN_LIST carries the group-3 Handoff_State open items and the carried SCA-V4-001 items", m is not None and all(x in vals.get("OPEN_LIST", "") for x in open_needed), str(open_needed))
lines = [l.strip() for l in lt.splitlines() if l.strip()]
ok("3h first two lines are 'Latest:' and 'Updated:' (SPEC 11.2 form)", lines[0] == f"Latest: {SNAP}" and lines[1] == f"Updated: {DATE}", lines[0] + " / " + lines[1])
sys.path.insert(0, os.path.join(REPO, "tools/validation"))
from pathlib import Path as _P
import validate_domain_decomposition_integrity as _vdi
tgt = _vdi._latest_pointer_target(_P(os.path.join(REPO, lt_rel)), allow_legacy_single_line=False)
match = _vdi._pointer_matches(tgt, _P(os.path.join(REPO, S)), _P(os.path.join(REPO, SC)))
ok("3i registered parser _latest_pointer_target resolves the pointer to the accepted snapshot and _pointer_matches is True", tgt == SNAP and match, f"target {tgt!r} match {match}")
act = re.findall(r"^\*\*Active snapshot:\*\*\s*`([^`]+)`", lt, re.M)
ok("3j exactly one '**Active snapshot:**' line, naming the accepted snapshot", act == [f"execution/_ScopeChange/{SNAP}/"], str(act))
ok("3k no unfilled token in _LATEST.md", not TOKEN.search(lt), "")

# ---- 4. H-3 ----
cc_rel = f"{DEC}/Consolidated_Coverage.csv"
ok("4a Consolidated_Coverage.csv unchanged from the accepted candidate (the register carries no SOFTWARE_DECOMP.md row)", cur(cc_rel) == at_basis(cc_rel), sha(cur(cc_rel)))
rows = list(csv.reader(io.StringIO(cur(cc_rel).decode("utf-8"), newline="")))
hdr = rows[0]; ix = {c: hdr.index(c) for c in hdr}
docs = sorted({r[ix["Document"]] for r in rows[1:]})
ok("4b no Consolidated_Coverage.csv row names SOFTWARE_DECOMP.md", sd_rel not in docs, str(docs))
drift = []
info = {}
for r in rows[1:]:
    doc = r[ix["Document"]]
    if doc not in info:
        data = cur(doc)
        blob = subprocess.run(["git", "hash-object", "--stdin"], input=data, capture_output=True, check=True).stdout.decode().strip()
        info[doc] = (sha(data), "git-blob:" + blob, data.decode("utf-8").splitlines())
    s_, gb, L = info[doc]
    rid = r[ix["ConsolidatedRequirementID"]]
    patt = re.compile(r"^(- \*\*|\*\*|\| )" + re.escape(rid) + r"(?![0-9A-Za-z])")
    hits = [n + 1 for n, l in enumerate(L) if patt.search(l)]
    if (s_, gb, str(hits[0]) if hits else None) != (r[ix["SHA256"]], r[ix["ReadSnapshot"]], r[ix["SourceLine"]]):
        drift.append(rid)
ok("4c the B8 rule recomputed over all rows against the working documents changes no row", not drift, f"{len(rows) - 1} rows; drift {drift}")

# ---- 5. write boundary ----
changed = [l[3:] for l in git("status", "--porcelain", "--untracked-files=all").splitlines()]
allowed_prefix = (f"{SC}/", f"{RUN}/POSTACCEPT/", sd_rel)
outside = [c for c in changed if not c.startswith(allowed_prefix)]
ok("5a every changed path is inside the post-acceptance write boundary (_ScopeChange/, SOFTWARE_DECOMP.md, POSTACCEPT/)", not outside, f"{len(changed)} paths; outside {outside}")
forb = [c for c in changed if re.search(r"ScopeOfWork\.md$|Dependencies\.csv$|_DEPENDENCIES\.md$|/_DAG/|_STATUS\.md$|Coverage_Telemetry\.json$|_LATEST_ACCEPTED\.md$", c)]
ok("5b no ScopeOfWork.md, Dependencies.csv, _DEPENDENCIES.md, _DAG, _STATUS.md, Coverage_Telemetry.json or _LATEST_ACCEPTED.md changed", not forb, str(forb))
sca1_changed = [c for c in changed if "/SCA-V4-001" in c]
ok("5c no SCA-V4-001 byte changed (snapshot, decision folders, validation records)", not sca1_changed, str(sca1_changed))
bound = []
for gname in ("GROUP-1", "GROUP-2"):
    mm = list(csv.DictReader(io.StringIO(cur(f"{SC}/checkpoint_snapshots/{AID}_{gname}_{DATE}/ACCEPTED_MANIFEST.csv").decode("utf-8"))))
    mism = [r["Path"] for r in mm if not os.path.isfile(os.path.join(REPO, r["Path"])) or sha(cur(r["Path"])) != r["SHA256"]]
    exp_mism = [r["Path"] for r in mm if r["Path"].endswith("OWNER_DECISIONS.md")]
    ok(f"5d {gname} ACCEPTED_MANIFEST.csv rows still match the working tree (append-only custody record excepted)", mism == exp_mism, f"{len(mm)} rows; mismatches {mism}")
    bound += [r["Path"] for r in mm]
rewritten = [c for c in changed if c in bound]
ok("5e no group-1- or group-2-bound file was rewritten", not rewritten, str(rewritten))

# ---- 6. active snapshot ----
required = ["Brief.md", "Intake_Actions.csv", "Impact_Assessment.md", "Amendment_Preview.md", "Propagation_Plan.md", "Amendment_Actions.csv",
            "Pre_Change_Coverage.json", "Post_Change_Coverage.json", "Decision_Log.md", "Handoff_State.md", "RUN_SUMMARY.md", "Supersession_Delta.csv", "Supersession_Map.csv"]
missing = [f for f in required if not os.path.isfile(os.path.join(REPO, S, f))]
ok("6a active snapshot holds every required PROJECT/SOFTWARE artifact", not missing, f"missing {missing}")
hs = cur(f"{S}/Handoff_State.md").decode("utf-8")
need = ["ACCEPTED, active snapshot", "OPEN_PENDING_DERIVATIVE_CLOSURE", "`DecompositionTruthState` | `COMPLETE`", "`DownstreamRerunState` | `IN_PROGRESS`", "`AuditState` | `WARNINGS`",
        "158702bf610777e008e304268fcbd967756f9186ded946942430a391957c579d", "Carried from the predecessor", "Dispositions carried from V14", "COV-139", "ASC-ISS-001", "STALE"]
ok("6b accepted Handoff_State.md names the snapshot, register, derivative status, verdict, next workflows, V14 dispositions and carried items", all(x in hs for x in need), f"missing {[x for x in need if x not in hs]}")
folders = sorted(d for d in os.listdir(os.path.join(REPO, SC)) if d.startswith("SCA-") and os.path.isdir(os.path.join(REPO, SC, d)))
ok("6c exactly two SCA-* amendment snapshot folders exist (the predecessor and the active one), both complete", folders == [PRED, SNAP] and all(os.path.isfile(os.path.join(REPO, SC, d, f)) for d in folders for f in required), str(folders))
ok("6d candidate Handoff_State.md and RUN_SUMMARY.md bytes presented at group 3 are bound in the group-3 manifest",
   any(r["Path"] == f"{S}/Handoff_State.md" and r["SHA256"] == sha(at_basis(f"{S}/Handoff_State.md")) for r in man) and any(r["Path"] == f"{S}/RUN_SUMMARY.md" and r["SHA256"] == sha(at_basis(f"{S}/RUN_SUMMARY.md")) for r in man), "")

# ---- 7. audit-decomp rerun (POSTACCEPT) ----
summ = json.load(open(os.path.join(REPO, RUN, "POSTACCEPT/coverage_summary.json")))
ok("7a audit-decomp rerun: 0 BLOCKER", summ["issues_blocker"] == 0, f"{summ['issues_blocker']}/{summ['issues_warning']}/{summ['issues_info']}")
il = list(csv.DictReader(open(os.path.join(REPO, RUN, "POSTACCEPT/Decomp_Coverage_IssueLog.csv"), encoding="utf-8", newline="")))
res = [r for r in il if r["Description"].startswith("Historical snapshot residue")]
ok("7b COV-139 absent: no 'Historical snapshot residue' finding", not res, str([r["IssueID"] for r in res]))
rp = [r for r in il if "Registered pointer parser" in r["Description"]]
ok("7c the registered-parser INFO is absent", not rp and summ["extensions"]["registered_pointer_parser"]["pointer_matches_active"] is True, json.dumps(summ["extensions"]["registered_pointer_parser"]))
ok("7d Check 10 active snapshot and handoff state PASS, active snapshot is the accepted one", summ["active_snapshot_status"] == "PASS" and summ["handoff_state_status"] == "PASS" and summ["extensions"]["active_snapshot_check"]["active_snapshot"].endswith(SNAP), summ["extensions"]["active_snapshot_check"]["active_snapshot"])
ok("7e topology unchanged (11 packages, 41 deliverables, 10 objectives, 262 scope items)", summ["repository_topology"] == {"packages": 11, "deliverables": 41, "objectives": 10, "scope_items": 262, "ledger_rows": 262}, json.dumps(summ["repository_topology"]))
cr = [r for r in il if r["CheckNumber"] == "9b"]
ok("7f Change Register binds ('Decision Log' at rank exact) in the 9b finding", len(cr) == 1 and "'Decision Log' at rank exact" in cr[0]["Description"], cr[0]["IssueID"] if cr else "")
ok("7g the seven-package scope equals the register-derived scope", summ["scope"] == ["PKG-01", "PKG-02", "PKG-03", "PKG-04", "PKG-05", "PKG-09", "PKG-10"] and summ["extensions"]["scope_check"]["scope_equals_register_packages"], str(summ["scope"]))

# ---- 8. supersession map ----
regen = os.path.join(SCRATCH, "Supersession_Map.regen.csv")
r8 = subprocess.run([sys.executable, os.path.join(REPO, "tools/coordination/accumulate_supersession_map.py"), "--prior-map", os.path.join(REPO, SC, PRED, "Supersession_Map.csv"),
                     "--delta", os.path.join(REPO, S, "Supersession_Delta.csv"), "--output-map", regen, "--check-map", os.path.join(REPO, S, "Supersession_Map.csv"),
                     "--output-findings", os.path.join(HERE, "Supersession_Findings.csv")], capture_output=True, text=True)
ok("8 accumulate_supersession_map.py --check-map on the active snapshot (prior = SCA-V4-001 map, delta = SCA-V4-002)", r8.returncode == 0 and open(regen, "rb").read() == cur(f"{S}/Supersession_Map.csv"), (r8.stdout + r8.stderr).strip().replace("\n", " ").replace(SCRATCH, "<scratch>"))

# ---- 9. DAG-002 currency ----
r9 = subprocess.run(["shasum", "-a", "256", "-c", "_DAG/DAG-002/SOURCE_MANIFEST.sha256"], cwd=os.path.join(REPO, EX), capture_output=True, text=True)
okc = r9.stdout.count(": OK"); total = len([l for l in r9.stdout.splitlines() if l.strip()])
open(os.path.join(HERE, "DAG_CURRENCY.txt"), "w").write(f"# cwd: {EX}\n# command: shasum -a 256 -c _DAG/DAG-002/SOURCE_MANIFEST.sha256\n# exit: {r9.returncode}\n" + r9.stdout + r9.stderr)
ok("9a DAG-002 currency (run from the execution root): every bound file OK", r9.returncode == 0 and okc == total == 130, f"{okc}/{total} OK, exit {r9.returncode}")
st = json.load(open(os.path.join(REPO, RUN, "POSTACCEPT/structure.json")))
ok("9b no deliverable is ISSUED or CHECKING (the ISSUED-reopen rule does not apply)", set(st["summary"]["lifecycle_states"]) <= {"INITIALIZED", "IN_PROGRESS"}, json.dumps(st["summary"]["lifecycle_states"]))

# ---- write ----
applied = {}
for rel in [sd_rel, lt_rel, cc_rel, f"{S}/Handoff_State.md", f"{S}/RUN_SUMMARY.md", f"{S}/Decision_Log.md", f"{G3}/DECISION.md", f"{G3}/ACCEPTED_MANIFEST.csv", f"{G3}/Handoff_State.md"]:
    applied[rel] = sha(cur(rel))
result = "PASS" if all(c["result"] == "PASS" for c in checks) else "FAIL"
json.dump({"record": REC, "basis_commit": BASIS, "presentation_commit": PRES, "candidate_commit": CAND, "amendment": AID, "snapshot": SNAP, "result": result, "checks": checks, "applied_hashes": applied},
          open(os.path.join(HERE, "post_acceptance_checks.json"), "w"), indent=1)
md = [f"# {AID} post-acceptance validation", "",
      f"Owner act: DECISION-3, {DATE} (\"Accept (Recommended)\"; `checkpoint_snapshots/{AID}_GROUP-3_{DATE}/`). Accepted basis `{BASIS[:9]}` (candidate `{CAND[:9]}`, presentation `{PRES[:9]}`). Applied state: uncommitted working tree over `{BASIS[:9]}`. Record `{os.path.basename(HERE)}`. Written by `verify_post_acceptance.py`, which recomputes the applied bytes from the accepted basis independently of `apply_group3_edits.py`. The candidate evidence reviewed at group 3 (POSTCHANGE/, V14) is not modified. No `ScopeOfWork.md` is changed under this record: the nine REVISEs and B-06a follow as propagation stage 1.", "",
      "| Check | Result | Detail |", "|---|---|---|"]
for c in checks:
    md.append(f"| {c['check']} | {c['result']} | {c['detail'].replace('|', '\\|')} |")
md += ["", "## Applied and finalized files (sha256)", "", "| File | sha256 |", "|---|---|"]
for rel, h in sorted(applied.items()):
    md.append(f"| `{rel}` | `{h}` |")
md += ["", f"Result: {result}", ""]
open(os.path.join(HERE, "POST_ACCEPTANCE_VALIDATION.md"), "w", encoding="utf-8").write("\n".join(md))
print(result, sum(1 for c in checks if c["result"] == "PASS"), "/", len(checks))
for c in checks:
    if c["result"] != "PASS":
        print("FAIL:", c["check"], c["detail"])
