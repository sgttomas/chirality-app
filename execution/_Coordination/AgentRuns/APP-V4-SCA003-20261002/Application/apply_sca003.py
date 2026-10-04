#!/usr/bin/env python3
"""AK1 stage 2 (run APP-V4-SCA003-20261002): apply the accepted SCA-V4-003 candidate edits to Open_Issues.csv.

Authority: group-2 decision snapshot checkpoint_snapshots/SCA-V4-003_GROUP-2_2026-10-03/ (DECISION-1), which binds
AMENDMENT_PACKET/BASIS_AMENDMENT.md at sha256 151bc6ff...35bf. Source of every byte: that file's B-02/B-03 table.
Applied: B-02 option B (OI-009 Status and Consequence) and B-03 (OI-018 Consequence; Q-11).
Not applied here: B-01 (Decision Log) and C-01 (_LATEST.md), acceptance-conditional; every ScopeOfWork block (REVISE
after group 3).

Usage: apply_sca003.py REPO OUTPATH LOG.json
  OUTPATH is where the edited Open_Issues.csv is written (the working file for the real run, a scratch path for a dry run).

Rules: the packet and the group-2 manifest are the accepted bytes; the target equals its blob at the basis commit and
the hash the group-2 manifest binds; the CSV writer reproduces the unedited file byte for byte; each old whole-field
value equals the current field; only the three named fields change; the result equals the packet's stated hash.
Any failure aborts before anything is written.
"""
import csv, hashlib, io, json, re, subprocess, sys

REPO, OUTPATH, LOG = sys.argv[1], sys.argv[2], sys.argv[3]
BASIS_COMMIT = "ec267bdb9f"
EX = "projects/chirality-app-v4/execution"
OI = f"{EX}/_Decomposition/Open_Issues.csv"
PK = f"{EX}/_Coordination/AgentRuns/APP-V4-SCA003-20261002/AMENDMENT_PACKET/BASIS_AMENDMENT.md"
G2M = f"{EX}/_ScopeChange/checkpoint_snapshots/SCA-V4-003_GROUP-2_2026-10-03/ACCEPTED_MANIFEST.csv"
PACKET_SHA = "151bc6fffcac482f6f8e77bf3d7b2822ec65f94012e0b66720f14644efbe35bf"
PRE_SHA = "a11782181531ce77e564b774787537d3e11cc1d4304123cba0d83f539bb280f0"
POST_SHA = "9c2d916c277f8ce4b847c9c532822d0566e59517ba9e0a86b650fe0450f3515d"  # Q-10 B with the OI-018 pointer


def fail(msg):
    raise SystemExit("FAIL: " + msg)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git(*a):
    return subprocess.run(["git", "-C", REPO, *a], capture_output=True, check=True).stdout


def rb(rel):
    return open(f"{REPO}/{rel}", "rb").read()


man = {r["Path"]: r["SHA256"] for r in csv.DictReader(io.StringIO(rb(G2M).decode("utf-8"), newline=""))}
if man.get(PK) != PACKET_SHA or sha(rb(PK)) != PACKET_SHA:
    fail("BASIS_AMENDMENT.md is not the bytes the group-2 manifest binds")
if man.get(OI) != PRE_SHA:
    fail("group-2 manifest does not bind the expected pre-change Open_Issues.csv")
ba = rb(PK).decode("utf-8")

# Parse the B-02/B-03 whole-field table: | <row> · `<col>` (<label>) | `old` | `new` |
cells = {}
for line in ba.splitlines():
    m = re.fullmatch(r"\| (OI-\d{3}) · `(\w+)` \(([^|]*)\) \| (`.*?`|same) \| `(.*)` \|", line)
    if m:
        cells[(m.group(1), m.group(2), m.group(3))] = (m.group(4), m.group(5))
want = [("OI-009", "Status", "option B"), ("OI-009", "Consequence", "option B"), ("OI-018", "Consequence", "Q-11")]
edits = []
for k in want:
    if k not in cells:
        fail(f"packet row {k} not found")
    old, new = cells[k]
    if not (old.startswith("`") and old.endswith("`")):
        fail(f"packet row {k} has no whole old value")
    edits.append({"row": k[0], "column": k[1], "label": k[2], "old": old[1:-1], "new": new})

pre = rb(OI)
if sha(pre) != PRE_SHA:
    fail("working Open_Issues.csv is not the bound pre-change bytes")
if pre != git("show", f"{BASIS_COMMIT}:{OI}"):
    fail("working Open_Issues.csv differs from its blob at the basis commit")


def parse(b):
    rdr = csv.reader(io.StringIO(b.decode("utf-8"), newline=""))
    return [r for r in rdr]


def write(rows):
    out = io.StringIO(newline="")
    csv.writer(out, lineterminator="\r\n").writerows(rows)
    return out.getvalue().encode("utf-8")


rows = parse(pre)
if write(rows) != pre:
    fail("CSV writer does not reproduce the unedited file byte for byte")
hdr = rows[0]
idx = {r[0]: i for i, r in enumerate(rows) if i}
for e in edits:
    r, c = idx[e["row"]], hdr.index(e["column"])
    if rows[r][c] != e["old"]:
        fail(f"{e['row']} {e['column']}: current value is not the packet's old value")
    if rows[r][c] == e["new"]:
        fail(f"{e['row']} {e['column']}: already applied")
    rows[r][c] = e["new"]
post = write(rows)

# only the named fields differ
a, b = parse(pre), parse(post)
diff = [(a[i][0], hdr[j]) for i in range(len(a)) for j in range(len(hdr)) if a[i][j] != b[i][j]]
if sorted(diff) != sorted((e["row"], e["column"]) for e in edits) or len(a) != len(b):
    fail(f"unexpected field differences {diff}")
if sha(post) != POST_SHA:
    fail(f"result {sha(post)} is not the packet's stated hash {POST_SHA}")
open_count = sum(1 for r in b[1:] if r[hdr.index("Status")] == "OPEN")

open(OUTPATH, "wb").write(post)
json.dump({"basis_commit": BASIS_COMMIT, "packet": PK, "packet_sha256": PACKET_SHA, "target": OI,
           "pre_sha256": PRE_SHA, "post_sha256": sha(post), "expected_post_sha256": POST_SHA,
           "open_count_before": sum(1 for r in a[1:] if r[hdr.index("Status")] == "OPEN"), "open_count_after": open_count,
           "edits": [{k: v for k, v in e.items() if k in ("row", "column", "label")} | {"old_len": len(e["old"]), "new_len": len(e["new"])} for e in edits],
           "fields_changed": [list(x) for x in diff], "writer_roundtrip_exact": True, "output": OUTPATH},
          open(LOG, "w"), indent=2)
print("OK", sha(post), "OPEN", open_count)
