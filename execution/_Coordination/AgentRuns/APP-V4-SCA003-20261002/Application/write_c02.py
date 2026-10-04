#!/usr/bin/env python3
"""AK1 stage 2: write the SCA-V4-002 effective-state note (BASIS_AMENDMENT C-02, as corrected for V23b n-1 before K1).

Usage: write_c02.py REPO C02_UTC HEAD LOG.json
Source: the ```text block of BASIS_AMENDMENT.md section C-02 at the bound hash; slots {C02_UTC} and {HEAD} filled.
Writes a new folder _ScopeChange/_PostAcceptanceValidation/SCA-V4-002_{C02_UTC}_EFFECTIVE_STATE/; refuses if it exists.
"""
import csv, hashlib, io, json, os, re, sys
REPO, UTC, HEAD, LOG = sys.argv[1:5]
EX = "projects/chirality-app-v4/execution"
BA = f"{EX}/_Coordination/AgentRuns/APP-V4-SCA003-20261002/AMENDMENT_PACKET/BASIS_AMENDMENT.md"
G2M = f"{EX}/_ScopeChange/checkpoint_snapshots/SCA-V4-003_GROUP-2_2026-10-03/ACCEPTED_MANIFEST.csv"
sha = lambda b: hashlib.sha256(b).hexdigest()
bound = {r["Path"]: r["SHA256"] for r in csv.DictReader(io.StringIO(open(os.path.join(REPO, G2M)).read(), newline=""))}[BA]
raw = open(os.path.join(REPO, BA), "rb").read()
if sha(raw) != bound:
    raise SystemExit("FAIL: BASIS_AMENDMENT.md is not the bound bytes")
t = raw.decode("utf-8")
sec = t[t.index("### C-02"):t.index("## D. Supersession")]
blocks = re.findall(r"```text\n(.*?)```", sec, re.S)
if len(blocks) != 1:
    raise SystemExit("FAIL: C-02 block not unique")
body = blocks[0]
for slot in ("{C02_UTC}", "{HEAD}"):
    if body.count(slot) != 1:
        raise SystemExit(f"FAIL: slot {slot} count {body.count(slot)}")
body = body.replace("{C02_UTC}", UTC).replace("{HEAD}", HEAD)
if "{" in body:
    raise SystemExit("FAIL: unfilled slot remains")
folder = os.path.join(REPO, EX, "_ScopeChange/_PostAcceptanceValidation", f"SCA-V4-002_{UTC}_EFFECTIVE_STATE")
os.makedirs(folder)
out = os.path.join(folder, "EFFECTIVE_STATE.md")
open(out, "wb").write(body.encode("utf-8"))
json.dump({"source": BA, "source_sha256": bound, "C02_UTC": UTC, "HEAD": HEAD,
           "output": os.path.relpath(out, REPO), "output_sha256": sha(body.encode("utf-8"))}, open(LOG, "w"), indent=2)
print(os.path.relpath(out, REPO), sha(body.encode("utf-8")))
