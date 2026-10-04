#!/usr/bin/env python3
"""AK1 stage 2 (run APP-V4-SCA003-20261002): byte copies and the supersession delta for the SCA-V4-003 candidate.

Usage: gen_candidate.py REPO CANDIDATE_REL LOG.json

- Amendment_Actions.csv, Impact_Assessment.md and Pre_Change_Coverage.json are byte copies of files bound in the
  group-1 or group-2 ACCEPTED_MANIFEST.csv; each source is checked against its bound hash first.
- Supersession_Delta.csv is the ```csv block of BASIS_AMENDMENT.md Part D (Q-10 option B), byte for byte, LF line
  endings and a final newline, as SCA-V4-002's delta. It has no token to fill.
Writes only inside CANDIDATE_REL; refuses to overwrite a file whose bytes differ.
"""
import csv, hashlib, io, json, os, re, sys

REPO, CAND, LOG = sys.argv[1], sys.argv[2], sys.argv[3]
EX = "projects/chirality-app-v4/execution"
RUN = f"{EX}/_Coordination/AgentRuns/APP-V4-SCA003-20261002"
G1M = f"{EX}/_ScopeChange/checkpoint_snapshots/SCA-V4-003_GROUP-1_2026-10-03/ACCEPTED_MANIFEST.csv"
G2M = f"{EX}/_ScopeChange/checkpoint_snapshots/SCA-V4-003_GROUP-2_2026-10-03/ACCEPTED_MANIFEST.csv"
COPIES = {
    "Amendment_Actions.csv": (G2M, f"{EX}/_ScopeChange/checkpoint_snapshots/SCA-V4-003_GROUP-2_2026-10-03/Amendment_Actions.csv"),
    "Impact_Assessment.md": (G1M, f"{RUN}/AMENDMENT_PACKET/IMPACT_ASSESSMENT.md"),
    "Pre_Change_Coverage.json": (G1M, f"{RUN}/BASELINE/coverage_summary.json"),
}
BA = f"{RUN}/AMENDMENT_PACKET/BASIS_AMENDMENT.md"


def fail(m):
    raise SystemExit("FAIL: " + m)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def rb(rel):
    return open(os.path.join(REPO, rel), "rb").read()


def manifest(rel):
    return {r["Path"]: r["SHA256"] for r in csv.DictReader(io.StringIO(rb(rel).decode("utf-8"), newline=""))}


def put(name, data):
    p = os.path.join(REPO, CAND, name)
    if os.path.exists(p) and open(p, "rb").read() != data:
        fail(f"{name} exists with other bytes")
    open(p, "wb").write(data)
    return sha(data)


log = {"candidate": CAND, "files": {}}
for name, (man, src) in COPIES.items():
    bound = manifest(man).get(src)
    data = rb(src)
    if bound is None or sha(data) != bound:
        fail(f"{src} is not bound at its hash in {man}")
    log["files"][name] = {"source": src, "bound_in": man, "sha256": put(name, data), "kind": "byte copy"}

ba = rb(BA)
if sha(ba) != manifest(G2M).get(BA):
    fail("BASIS_AMENDMENT.md is not the bound bytes")
text = ba.decode("utf-8")
part_d = text[text.index("## D. Supersession"):]
blocks = re.findall(r"```csv\n(.*?)```", part_d, re.S)
if len(blocks) != 1:
    fail(f"expected one csv block in Part D, found {len(blocks)}")
delta = blocks[0].encode("utf-8")
rows = list(csv.DictReader(io.StringIO(blocks[0], newline="")))
if len(rows) != 1 or rows[0]["DecisionID"] != "D-021" or rows[0]["AmendmentID"] != "SCA-V4-003" or "{" in blocks[0]:
    fail("Part D block is not the single filled D-021 row")
log["files"]["Supersession_Delta.csv"] = {"source": BA + " Part D csv block", "sha256": put("Supersession_Delta.csv", delta),
                                          "rows": len(rows), "kind": "exact packet block"}
json.dump(log, open(LOG, "w"), indent=2)
print(json.dumps(log, indent=2))
