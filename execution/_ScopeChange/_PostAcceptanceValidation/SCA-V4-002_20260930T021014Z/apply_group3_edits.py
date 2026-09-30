#!/usr/bin/env python3
"""AK2: apply the SCA-V4-002 acceptance-conditional edits after checkpoint group 3 (owner DECISION-3).

H-1 B-04 (SOFTWARE_DECOMP.md Decision Log entry) from the accepted BASIS_AMENDMENT.md text with the slots
filled from the accepted group-3 record; H-2 C-01 (_ScopeChange/_LATEST.md in SPEC 11.2 form) from the
Part C text with its slots filled; H-3, the Consolidated_Coverage.csv recompute check for the rows H-1 shifts.

Usage: apply_group3_edits.py REPO OUTROOT LOG.json
  OUTROOT == REPO -> writes in place; otherwise writes mirrored copies under OUTROOT (dry run).

Rules:
- the packet must be the accepted bytes (sha256 091871fd...4238);
- every target must still carry its accepted candidate bytes (the blob at the basis commit 851ec3d88);
- the filled B-04 "old" block must occur exactly once and its filled "new" block zero times before, once after;
- no token may remain unfilled in any written file;
- H-3: the B8 rule (SHA256, ReadSnapshot = git blob, SourceLine = first definition line) is recomputed for every
  row of Consolidated_Coverage.csv against the post-H-1 working documents; the register carries no
  SOFTWARE_DECOMP.md row, so any changed row aborts the run (nothing is expected to shift);
- nothing else is touched: any failure aborts before writing.
"""
import csv, hashlib, io, json, os, re, subprocess, sys

REPO, OUTROOT, LOG = sys.argv[1], sys.argv[2], sys.argv[3]
BASIS_COMMIT = "851ec3d88bb090f0bc63ad7075b1668ad65afb39"
AID = "SCA-V4-002"
DATE = "2026-09-29"
SNAP = "SCA-V4-002_2026-09-29_1901"
UTC = "20260930T021014Z"
P = "projects/chirality-app-v4"
EX = f"{P}/execution"
DEC = f"{EX}/_Decomposition"
SC = f"{EX}/_ScopeChange"
PK = f"{EX}/_Coordination/AgentRuns/APP-V4-SCA002-20260929/AMENDMENT_PACKET"
PACKET_SHA = "091871fd90283b27b2d067c1eeb3137e3cf8f9d50dab87ad92a9b871cc634238"
SD = f"{DEC}/SOFTWARE_DECOMP.md"
LATEST = f"{SC}/_LATEST.md"
CC = f"{DEC}/Consolidated_Coverage.csv"
C02 = "execution/_ScopeChange/_PostAcceptanceValidation/SCA-V4-001_20260930T010520Z_EFFECTIVE_STATE/EFFECTIVE_STATE.md"

# B-04 slot values (DECISION-2: no item declined; Q-5 option A)
B04_FILL = {
    "{ACCEPT_DATE}": DATE,
    "{AMENDMENT_SNAPSHOT}": SNAP,
    "{Q6_CLAUSE}": ", DEL-04-02 and DEL-01-01",
    "{Q7_CLAUSE}": "; the OI-012 pointer in Open_Issues.csv",
    "{Q11_CLAUSE}": "; Deliverables DEL-04-01 (checkpoint clause) with its _CONTEXT.md mirror",
    "{Q12_CLAUSE}": '; a reading-rule note ("GROUP3 as amended by the active _ScopeChange/_LATEST.md") on _LATEST.md, checkpoint_snapshots/_LATEST_ACCEPTED.md and five _CONTEXT.md basis lines',
    "{Q10_CLAUSE}": "; and path-level Supersession_Delta rows for SCA-V4-001 actions 18–25, 36, 42 and 46",
}
# C-01 slot values
OPEN_LIST = ("the 9 ScopeOfWork REVISEs (`scope-of-work` MODE=REVISE, `STATUS_POLICY` `NO_STATUS_TOUCH`) with the "
             "B-06a reading-rule note on `_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md`; the "
             "dependency-register UPDATE (`dependency-extract`); the DAG-002 departure and the DAG-003 candidate "
             "(owner checkpoint C); `_Decomposition/Coverage_Telemetry.json` (`STALE_REBUILD_REQUIRED`, owned by "
             "the decomposition owner; carried from SCA-V4-001); the 17 Design re-pins (carried from SCA-V4-001); "
             "the confirmation of ASC-ISS-001's closure by a superseding `audit-scope-closure` snapshot for "
             f"SCA-V4-001 (the SCA-V4-001 effective-state record is `{C02}`); `audit-scope-closure` for SCA-V4-002")
C01_FILL = {
    "{AMENDMENT_SNAPSHOT}": SNAP,
    "{ACCEPT_DATE}": DATE,
    "{AMENDMENT_ID}": AID,
    "{CLOSURE_VERDICT}": "OPEN_PENDING_DERIVATIVE_CLOSURE",
    "{GROUP12_REFS}": "`execution/_ScopeChange/checkpoint_snapshots/SCA-V4-002_GROUP-1_2026-09-29/`, `execution/_ScopeChange/checkpoint_snapshots/SCA-V4-002_GROUP-2_2026-09-29/`",
    "{SCA001_CLOSURE}": f"`OPEN_PENDING_DERIVATIVE_CLOSURE` per `{C02}`",
    "{UTC}": UTC,
    "{ARC_LIST}": "N-18, N-21, N-24 and X-1",
    "{OPEN_LIST}": OPEN_LIST,
}


def fail(msg):
    raise SystemExit("FAIL: " + msg)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git(*a, inp=None):
    return subprocess.run(["git", "-C", REPO, *a], input=inp, capture_output=True, check=True).stdout


pkt = open(os.path.join(REPO, PK, "BASIS_AMENDMENT.md"), "rb").read()
if sha(pkt) != PACKET_SHA:
    fail("BASIS_AMENDMENT.md is not the accepted bytes")
ba = pkt.decode("utf-8")

log = {"basis_commit": BASIS_COMMIT, "packet_sha256": PACKET_SHA, "b04_fill": B04_FILL, "c01_fill": C01_FILL, "edits": [], "consolidated": {}, "files": {}}
orig, texts = {}, {}


def rd(rel):
    if rel not in texts:
        b = open(os.path.join(REPO, rel), "rb").read()
        at_basis = git("show", f"{BASIS_COMMIT}:{rel}")
        if b != at_basis:
            fail(f"{rel} differs from its bytes at the basis commit")
        orig[rel] = b
        texts[rel] = b.decode("utf-8")
    return texts[rel]


TOKEN = re.compile(r"\{[A-Z_0-9]+\}")

# ---------- H-1: B-04 ----------
sec = ba.split("### B-04 · ", 1)[1].split("\n### ", 1)[0]
blocks = re.findall(r"^```(old|new)\n(.*?)\n```$", sec, flags=re.M | re.S)
if [b[0] for b in blocks] != ["old", "new"]:
    fail(f"B-04 blocks {[b[0] for b in blocks]}")
old, new = blocks[0][1], blocks[1][1]
tokens = sorted(set(TOKEN.findall(new)))
if set(tokens) != set(B04_FILL):
    fail(f"B-04 tokens {tokens} != fill keys")
for k, v in B04_FILL.items():
    new = new.replace(k, v)
if TOKEN.search(new) or TOKEN.search(old):
    fail("B-04 unfilled token")
t = rd(SD)
c_old, c_new = t.count(old), t.count(new)
if c_old != 1 or c_new != 0:
    fail(f"B-04 {SD}: old count {c_old}, new count {c_new}")
t2 = t.replace(old, new)
if t2.count(new) != 1:
    fail("B-04 new count after")
texts[SD] = t2
log["edits"].append(dict(item="H-1", edit="B-04", target=SD, tokens=tokens, old_count_before=c_old, new_count_before=c_new,
                         new_count_after=1, old_sha256=sha(old.encode()), new_filled_sha256=sha(new.encode()), new_filled=new))

# ---------- H-2: C-01 ----------
secc = ba.split("## Part C — ", 1)[1].split("\n### C-02", 1)[0]
tb = re.findall(r"^```text\n(.*?)\n```$", secc, flags=re.M | re.S)
if len(tb) != 1:
    fail(f"C-01 text blocks {len(tb)}")
tmpl = tb[0]
ctokens = sorted(set(TOKEN.findall(tmpl)))
if set(ctokens) != set(C01_FILL):
    fail(f"C-01 tokens {ctokens} != fill keys {sorted(C01_FILL)}")
out = tmpl
for k, v in C01_FILL.items():
    out = out.replace(k, v)
if TOKEN.search(out):
    fail("C-01 unfilled token")
out += "\n"
lt = rd(LATEST)
if sha(orig[LATEST]) != "a9a7cdc8c50a36fbdd25fc53c72322972ba4f9b4d301d811e1a9c1381966339d":
    fail("_LATEST.md is not the pre-act pointer")
if "SCA-V4-001_2026-09-28_2155" not in lt:
    fail("_LATEST.md does not name the predecessor")
lines = [l.strip() for l in out.splitlines() if l.strip()]
if lines[0] != f"Latest: {SNAP}" or lines[1] != f"Updated: {DATE}":
    fail("C-01 first two lines")
# registered parser
sys.path.insert(0, os.path.join(REPO, "tools/validation"))
from pathlib import Path as _P
import validate_domain_decomposition_integrity as _vdi
tmp = os.path.join(os.path.dirname(LOG), "_LATEST.probe.md")
open(tmp, "w", encoding="utf-8").write(out)
tgt = _vdi._latest_pointer_target(_P(tmp), allow_legacy_single_line=False)
match = _vdi._pointer_matches(tgt, _P(os.path.join(REPO, SC, SNAP)), _P(os.path.join(REPO, SC)))
os.remove(tmp)
if tgt != SNAP or not match:
    fail(f"registered parser: target {tgt!r} match {match}")
texts[LATEST] = out
log["edits"].append(dict(item="H-2", edit="C-01", target=LATEST, tokens=ctokens, template_sha256=sha(tmpl.encode()),
                         parser_target=tgt, pointer_matches=match, new_sha256=sha(out.encode())))

# ---------- H-3: recompute check ----------
def csv_rows(t):
    return list(csv.reader(io.StringIO(t, newline="")))


def csv_text(rows):
    o = io.StringIO(newline="")
    csv.writer(o, lineterminator="\r\n").writerows(rows)
    return o.getvalue()


cc = rd(CC)
rows = csv_rows(cc)
if csv_text(rows) != cc:
    fail("Consolidated_Coverage.csv round-trip not byte-exact")
hdr = rows[0]
ix = {c: hdr.index(c) for c in hdr}
docs = sorted({r[ix["Document"]] for r in rows[1:]})
if SD in docs:
    fail("Consolidated_Coverage.csv carries SOFTWARE_DECOMP.md rows; H-3 needs a real recompute")
info, changed = {}, []
for r in rows[1:]:
    doc = r[ix["Document"]]
    if doc not in info:
        data = texts[doc].encode("utf-8") if doc in texts else open(os.path.join(REPO, doc), "rb").read()
        blob = subprocess.run(["git", "hash-object", "--stdin"], input=data, capture_output=True, check=True).stdout.decode().strip()
        info[doc] = (sha(data), "git-blob:" + blob, data.decode("utf-8").splitlines())
    s, gb, L = info[doc]
    rid = r[ix["ConsolidatedRequirementID"]]
    pat = re.compile(r"^(- \*\*|\*\*|\| )" + re.escape(rid) + r"(?![0-9A-Za-z])")
    hits = [n + 1 for n, l in enumerate(L) if pat.search(l)]
    if not hits:
        fail(f"B8 {rid}: no definition line")
    want = (s, gb, str(hits[0]))
    have = (r[ix["SHA256"]], r[ix["ReadSnapshot"]], r[ix["SourceLine"]])
    if want != have:
        changed.append((rid, have, want))
if changed:
    fail(f"H-3: {len(changed)} rows would change: {changed[:5]}")
log["consolidated"] = dict(rows_checked=len(rows) - 1, rows_changed=0, documents=docs, software_decomp_rows=0,
                           doc_sha256={d: v[0] for d, v in info.items()}, sha256_unchanged=sha(orig[CC]))

# ---------- write ----------
for rel, t in texts.items():
    b = t.encode("utf-8")
    if b == orig[rel]:
        log["files"][rel] = dict(pre=sha(orig[rel]), post=sha(b), written=False)
        continue
    dst = os.path.join(OUTROOT, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, "wb").write(b)
    log["files"][rel] = dict(pre=sha(orig[rel]), post=sha(b), written=True)
json.dump(log, open(LOG, "w"), indent=1, ensure_ascii=False)
print("edits", len(log["edits"]), "consolidated", {k: log["consolidated"][k] for k in ("rows_checked", "rows_changed")})
for rel, h in log["files"].items():
    print(h["post"], h["written"], rel)
