#!/usr/bin/env python3
"""AK1 stage 2: Intake_Actions.csv for the SCA-V4-003 candidate (transcription after the act).

The 23 rows of the accepted register (group-2 snapshot, sha256 9b7c2ce8...6d1c) with ScopeChanging left blank and a
trailing Status column PROPOSED, as the contract allows for intake evidence and as SCA-V4-002 did. It is group-1 intake
evidence only, not bound in the group-1 manifest (which binds the ledger and IMPACT_ASSESSMENT section 3 instead).
Usage: gen_intake.py REPO CANDIDATE_REL
"""
import csv, hashlib, io, os, sys
REPO, CAND = sys.argv[1:3]
REG = "projects/chirality-app-v4/execution/_ScopeChange/checkpoint_snapshots/SCA-V4-003_GROUP-2_2026-10-03/Amendment_Actions.csv"
b = open(os.path.join(REPO, REG), "rb").read()
if hashlib.sha256(b).hexdigest() != "9b7c2ce8fbf97ec0cf829c5024e03d19b4117c1ca50abaea4ec0b2c340346d1c":
    raise SystemExit("FAIL: register is not the bound bytes")
rdr = csv.DictReader(io.StringIO(b.decode("utf-8"), newline=""))
cols = rdr.fieldnames + ["Status"]
out = io.StringIO(newline="")
w = csv.DictWriter(out, fieldnames=cols, lineterminator="\n")
w.writeheader()
for r in rdr:
    r["ScopeChanging"] = ""
    r["Status"] = "PROPOSED"
    w.writerow(r)
data = out.getvalue().encode("utf-8")
open(os.path.join(REPO, CAND, "Intake_Actions.csv"), "wb").write(data)
print(hashlib.sha256(data).hexdigest())
