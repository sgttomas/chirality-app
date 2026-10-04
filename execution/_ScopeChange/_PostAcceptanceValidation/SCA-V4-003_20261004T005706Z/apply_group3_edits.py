#!/usr/bin/env python3
"""AK2 part 1 (run APP-V4-SCA003-20261002): apply H-1 (B-01) and H-2 (C-01) after group-3 acceptance (DECISION-2).

Source of every byte: AMENDMENT_PACKET/BASIS_AMENDMENT.md at the accepted sha256 151bc6ff...35bf.
Slots: {ACCEPT_DATE} = 2026-10-03 (DECISION-2 "Effects"); {AMENDMENT_SNAPSHOT} = SCA-V4-003_2026-10-03_1827;
B-01 clause slots as fixed by the group-2 DECISION.md; C-01 {CLOSURE_VERDICT} = OPEN_PENDING_DERIVATIVE_CLOSURE,
{G1_DATE} = {G2_DATE} = 2026-10-03, {C02_UTC} = 20261004T002903Z, {UTC} = 20261004T005706Z (this record's stamp).
Usage: apply_group3_edits.py REPO OUTROOT LOG.json   (OUTROOT == REPO writes in place; else mirrored dry run)
Rules: each target equals its blob at the act commit 84b520742d; the B-01 old block occurs once and the new block zero
times before and once after; no '{' remains; H-1's result equals the expected hash 983199cc...a70d; the registered
parser resolves H-2 to the snapshot. Any failure aborts before anything is written.
"""
import hashlib, json, os, re, subprocess, sys
REPO, OUTROOT, LOG = sys.argv[1:4]
ACT = "84b520742d"
E = "projects/chirality-app-v4/execution"
BA = f"{E}/_Coordination/AgentRuns/APP-V4-SCA003-20261002/AMENDMENT_PACKET/BASIS_AMENDMENT.md"
SD = f"{E}/_Decomposition/SOFTWARE_DECOMP.md"
LT = f"{E}/_ScopeChange/_LATEST.md"
SNAP = "SCA-V4-003_2026-10-03_1827"
DATE, UTC, C02 = "2026-10-03", "20261004T005706Z", "20261004T002903Z"
EXP_H1 = "983199cc22c84398000612cd95308c840ad011d302fe31ca110a5aa97e64a70d"
CL = {"{Q5_CLAUSE}": ", including the App act control in DEL-01-04",
      "{OI009_CLAUSE}": "Open_Issues OI-009 Status (RESOLVED_BY_OWNER_DECISION) and Consequence",
      "{OI018_CLAUSE}": " and the OI-018 Consequence pointer",
      "{D021_CLAUSE}": "; and a Supersession_Delta row binding the GROUP3 OI-009 Status"}
sha = lambda b: hashlib.sha256(b).hexdigest()
def fail(m): raise SystemExit("FAIL: " + m)
def blob(p): return subprocess.run(["git", "-C", REPO, "show", f"{ACT}:{p}"], capture_output=True, check=True).stdout
ba = open(os.path.join(REPO, BA), "rb").read()
if sha(ba) != "151bc6fffcac482f6f8e77bf3d7b2822ec65f94012e0b66720f14644efbe35bf": fail("BASIS_AMENDMENT not accepted bytes")
ba = ba.decode()
pre = {}
for p in (SD, LT):
    b = open(os.path.join(REPO, p), "rb").read()
    if b != blob(p): fail(f"{p} differs from its blob at {ACT}")
    pre[p] = b
# H-1
sec = ba[ba.index("### B-01"):ba.index("**Slot rules**")]
old = re.search(r"```old\n(.*?)```", sec, re.S).group(1)
new = re.search(r"```new\n(.*?)```", sec, re.S).group(1).replace("{ACCEPT_DATE}", DATE).replace("{AMENDMENT_SNAPSHOT}", SNAP)
for k, v in CL.items(): new = new.replace(k, v)
if "{" in new: fail("B-01 slot unfilled")
sd = pre[SD].decode()
if sd.count(old) != 1 or sd.count(new) != 0: fail("B-01 old/new counts before")
sd2 = sd.replace(old, new, 1)
if sd2.count(new) != 1 or "{ACCEPT_DATE}" in sd2: fail("B-01 counts after")
h1 = sd2.encode()
if sha(h1) != EXP_H1: fail(f"H-1 result {sha(h1)} != expected {EXP_H1}")
# H-2
sec = ba[ba.index("### C-01"):ba.index("### C-02")]
lt = re.search(r"```text\n(.*?)```", sec, re.S).group(1)
fills = {"{AMENDMENT_SNAPSHOT}": SNAP, "{ACCEPT_DATE}": DATE, "{CLOSURE_VERDICT}": "OPEN_PENDING_DERIVATIVE_CLOSURE",
         "{G1_DATE}": DATE, "{G2_DATE}": DATE, "{C02_UTC}": C02, "{UTC}": UTC}
for k, v in fills.items(): lt = lt.replace(k, v)
if "{" in lt: fail("C-01 slot unfilled")
h2 = lt.encode()
for p, data in ((SD, h1), (LT, h2)):
    dst = os.path.join(OUTROOT, p)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, "wb").write(data)
sys.path.insert(0, os.path.join(REPO, "tools/validation"))
from pathlib import Path
import validate_domain_decomposition_integrity as v
tgt = v._latest_pointer_target(Path(OUTROOT, LT), allow_legacy_single_line=False)
match = v._pointer_matches(tgt, Path(REPO, E, "_ScopeChange", SNAP), Path(REPO, LT).parent)
if tgt != SNAP or not match: fail(f"parser {tgt} {match}")
json.dump({"act_commit": ACT, "H1": {"target": SD, "before": sha(pre[SD]), "after": sha(h1), "expected": EXP_H1, "accept_date": DATE},
           "H2": {"target": LT, "before": sha(pre[LT]), "after": sha(h2), "fills": fills, "parser_target": tgt, "pointer_matches": match},
           "outroot_is_repo": os.path.realpath(OUTROOT) == os.path.realpath(REPO)}, open(LOG, "w"), indent=2)
print("OK", sha(h1), sha(h2), tgt, match)
