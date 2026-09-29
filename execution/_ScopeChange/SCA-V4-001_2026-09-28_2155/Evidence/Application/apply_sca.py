#!/usr/bin/env python3
"""AK1: apply the accepted SCA-V4-001 basis and decomposition edits (BASIS_AMENDMENT Parts A and B).

Usage: apply_sca.py REPO OUTROOT LOG.json
  OUTROOT == REPO  -> writes in place (candidate application);
  otherwise        -> writes mirrored copies under OUTROOT (dry run).

Held (acceptance-conditional, BASIS_AMENDMENT header and method "Acceptance-conditional edits"):
A07 (3 pairs), A17a, A17b, A17c, D-15. Each is verified to still match exactly once in the candidate.
Not touched: any ScopeOfWork.md, Dependencies.csv, _DEPENDENCIES.md, _DAG file, Coverage_Telemetry.json.
Every replacement must match exactly once, or the run aborts before writing anything.
"""
import csv, hashlib, io, json, os, re, subprocess, sys

REPO, OUTROOT, LOG = sys.argv[1], sys.argv[2], sys.argv[3]
AID = "SCA-V4-001"
P = "projects/chirality-app-v4"
EX = f"{P}/execution"
DEC = f"{EX}/_Decomposition"
PK = f"{EX}/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/AMENDMENT_PACKET"
ba = open(os.path.join(REPO, PK, "BASIS_AMENDMENT.md"), encoding="utf-8").read()
HELD = {"A07", "A17a", "A17b", "A17c", "D-15"}
DOCS = {"PRD.md": f"{P}/docs/PRD.md", "ARCHITECTURE.md": f"{P}/docs/ARCHITECTURE.md",
        "HOST_INTEGRATION.md": f"{P}/docs/HOST_INTEGRATION.md", "EXAMINATION.md": f"{P}/docs/EXAMINATION.md",
        "_Decomposition/SOFTWARE_DECOMP.md": f"{DEC}/SOFTWARE_DECOMP.md"}
log = {"edits": [], "held": [], "csv": [], "context": [], "consolidated": {}}
texts, orig = {}, {}

def rd(rel):
    if rel not in texts:
        b = open(os.path.join(REPO, rel), "rb").read()
        orig[rel] = b
        texts[rel] = b.decode("utf-8")
    return texts[rel]

def fail(msg):
    raise SystemExit("FAIL: " + msg)

# ---------- Part A and the SOFTWARE_DECOMP.md blocks (D-15, D-16) ----------
secs = re.split(r"^#### ", ba, flags=re.M)[1:]
md_edits = []
for s in secs:
    title = s.splitlines()[0]
    m = re.search(r"^Target: (\S+)", s, re.M)
    if not m:
        continue
    blocks = re.findall(r"^```(old|new)\n(.*?)\n```$", s, flags=re.M | re.S)
    assert len(blocks) % 2 == 0
    for i in range(0, len(blocks), 2):
        assert blocks[i][0] == "old" and blocks[i + 1][0] == "new", title
        md_edits.append((title.split(" ")[0], i // 2 + 1, DOCS[m.group(1)], blocks[i][1], blocks[i + 1][1]))
ids = [e[0] for e in md_edits]
expected = ["A01", "A02", "A04", "A05", "A06", "A07", "A07", "A07", "A11a", "A11b", "A08", "A10", "A12", "A13", "A14",
            "A15", "A16", "A17a", "A17b", "A17c", "D-15", "D-16"]
if ids != expected:
    fail(f"edit list {ids}")
for eid, k, rel, old, new in md_edits:
    t = rd(rel)
    c_orig = orig[rel].decode("utf-8").count(old)
    if eid in HELD:
        log["held"].append(dict(edit=eid, pair=k, target=rel, count_in_preimage=c_orig, old=old, new_template=new))
        if c_orig != 1:
            fail(f"held {eid}.{k} old count {c_orig} in preimage")
        continue
    if "{AMENDMENT_ID}" in new or "{ACCEPT_DATE}" in new or "{AMENDMENT_SNAPSHOT}" in new:
        fail(f"{eid} carries an acceptance token but is not held")
    c = t.count(old)
    if c != 1 or c_orig != 1:
        fail(f"{eid}.{k} {rel} count now {c}, preimage {c_orig}")
    texts[rel] = t.replace(old, new)
    log["edits"].append(dict(edit=eid, pair=k, target=rel, count_before=c, count_new_after=texts[rel].count(new)))

# ---------- Part B CSV field edits ----------
def csv_load(rel):
    t = rd(rel)
    return list(csv.reader(io.StringIO(t, newline="")))

def csv_dump(rel, rows):
    out = io.StringIO(newline="")
    csv.writer(out, lineterminator="\r\n").writerows(rows)
    s = out.getvalue()
    texts[rel] = s

def tbl(label_regex):
    return [[c.strip() for c in l.strip().strip("|").split(" | ")] for l in ba.splitlines() if re.match(label_regex, l)]

def set_field(rel, key_col, key, col, old, new, eid, substring=False):
    rows = csv_load(rel)
    hdr = rows[0]
    ki, ci = hdr.index(key_col), hdr.index(col)
    hits = [r for r in rows[1:] if r[ki] == key]
    if len(hits) != 1:
        fail(f"{eid}: {rel} key {key} rows {len(hits)}")
    r = hits[0]
    if substring:
        c = r[ci].count(old)
        if c != 1:
            fail(f"{eid}: substring count {c} in {rel} {key}.{col}")
        r[ci] = r[ci].replace(old, new)
    else:
        if r[ci] != old:
            fail(f"{eid}: {rel} {key}.{col} old value differs: {r[ci]!r}")
        r[ci] = new
    csv_dump(rel, rows)
    log["csv"].append(dict(edit=eid, target=rel, key=key, column=col, mode="substring" if substring else "field"))

# round-trip guard: the writer reproduces every CSV target byte-for-byte before any edit
for f in ("ScopeLedger.csv", "Vocabulary_Map.csv", "Deliverables.csv", "Packages.csv", "Open_Issues.csv", "Consolidated_Coverage.csv"):
    rel = f"{DEC}/{f}"
    before = rd(rel)
    csv_dump(rel, csv_load(rel))
    if texts[rel] != before:
        fail(f"CSV round-trip not byte-exact for {f}")

# B1 ScopeLedger
b1 = tbl(r"^\| D-0[1-8] \| SOW-")
assert [r[0] for r in b1] == [f"D-0{i}" for i in range(1, 9)]
for eid, row, old, new, decision in b1:
    set_field(f"{DEC}/ScopeLedger.csv", "ScopeItemID", row, "ScopeItemStatement", old, new, eid)
    set_field(f"{DEC}/ScopeLedger.csv", "ScopeItemID", row, "DecisionRef", "APP-V4-BASIS-20260926",
              f"APP-V4-BASIS-20260926;{decision};{AID}", eid + "/DecisionRef")
# B2 Vocabulary_Map
(b2,) = tbl(r"^\| D-09 \|")
set_field(f"{DEC}/Vocabulary_Map.csv", "CanonicalTerm", "Declared checkpoint", "Notes", b2[1], b2[2], "D-09")
# B3 Deliverables (substrings)
for eid, rowcol, old, new, decision in tbl(r"^\| D-1[012][a-d] \|"):
    key, col = [x.strip() for x in rowcol.split("·")]
    set_field(f"{DEC}/Deliverables.csv", "DeliverableID", key, col, old.strip("`"), new.strip("`"), eid, substring=True)
# B4 Packages (O-8 accepted)
(b4,) = tbl(r"^\| D-13 \|")
assert b4[1] == "PKG-05 · third column (description)"
hdr = csv_load(f"{DEC}/Packages.csv")[0]
set_field(f"{DEC}/Packages.csv", "PackageID", "PKG-05", hdr[2], b4[2].strip("`"), b4[3].strip("`"), "D-13", substring=True)
# B5 Open_Issues (O-17 accepted)
for eid, rowcol, old, new, decision in tbl(r"^\| D-14[ab] \|"):
    key, col = [x.strip() for x in rowcol.split("·")]
    set_field(f"{DEC}/Open_Issues.csv", "OpenIssueID", key, col, old, new, eid)

# ---------- B7 _CONTEXT.md mirrors ----------
sub = {}
for r in tbl(r"^\| D-1[0-3][a-d]? \|"):
    sub[r[0]] = (r[2].strip("`"), r[3].strip("`"))
import glob
def ctx(d):
    h = glob.glob(os.path.join(REPO, EX, "PKG-*", "1_Working", d + "_*", "_CONTEXT.md"))
    assert len(h) == 1
    return os.path.relpath(h[0], REPO)
B7 = {"DEL-02-03": ["D-10a", "D-10b"], "DEL-05-01": ["D-11a", "D-11b", "D-11c", "D-11d", "D-13"],
      "DEL-05-02": ["D-13"], "DEL-09-07": ["D-12a", "D-12b", "D-12c"]}
for d, eids in B7.items():
    rel = ctx(d)
    for eid in eids:
        t = rd(rel)
        old, new = sub[eid]
        c = t.count(old)
        if c != 1:
            fail(f"B7 {d} {eid} count {c}")
        texts[rel] = t.replace(old, new)
        log["context"].append(dict(edit=eid, target=rel, count_before=c))

# ---------- held edits must still apply exactly once to the candidate ----------
for h in log["held"]:
    c = texts[h["target"]].count(h["old"])
    h["count_in_candidate"] = c
    if c != 1:
        fail(f"held {h['edit']}.{h['pair']} would not apply to candidate (count {c})")

# ---------- B8 Consolidated_Coverage RECOMPUTE ----------
AMENDED_IDS = {"V4-WF-05", "V4-HOST-01", "V4-HOST-02", "V4-ARC-11", "V4-ARC-12", "V4-HI-42", "V4-HI-70", "V4-EXM-22", "V4-EXM-23"}
ccrel = f"{DEC}/Consolidated_Coverage.csv"
rows = csv_load(ccrel)
hdr = rows[0]
ix = {c: hdr.index(c) for c in hdr}
def blob(data):
    return subprocess.run(["git", "hash-object", "--stdin"], input=data, capture_output=True, check=True).stdout.decode().strip()
docinfo = {}
changed_rows = 0
per_doc = {}
for r in rows[1:]:
    doc = r[ix["Document"]]
    if doc not in DOCS.values() or doc.endswith("SOFTWARE_DECOMP.md"):
        continue
    data = texts[doc].encode("utf-8")
    if doc not in docinfo:
        docinfo[doc] = (hashlib.sha256(data).hexdigest(), "git-blob:" + blob(data), texts[doc].splitlines())
        # the preimage values must equal the recorded ones (the rule reproduces the current file)
    sha, gb, L = docinfo[doc]
    rid = r[ix["ConsolidatedRequirementID"]]
    pat = re.compile(r"^(- \*\*|\*\*|\| )" + re.escape(rid) + r"(?![0-9A-Za-z])")
    hits = [n + 1 for n, l in enumerate(L) if pat.search(l)]
    if not hits:
        fail(f"B8 {rid} no definition line")
    before = list(r)
    r[ix["SHA256"]] = sha
    r[ix["ReadSnapshot"]] = gb
    r[ix["SourceLine"]] = str(hits[0])
    if rid in AMENDED_IDS:
        r[ix["Standing"]] = r[ix["Standing"]] + " amended by " + AID
    if r != before:
        changed_rows += 1
    per_doc[doc] = per_doc.get(doc, 0) + 1
if sorted(per_doc.values()) != [13, 22, 31, 60]:
    fail(f"B8 row counts {per_doc}")
csv_dump(ccrel, rows)
std = sum(1 for r in rows[1:] if r[ix["Standing"]].endswith(" amended by " + AID))
if std != 9:
    fail(f"B8 standing rows {std}")
log["consolidated"] = dict(rows_recomputed=sum(per_doc.values()), rows_changed=changed_rows, per_doc=per_doc, standing_rows=std,
                           doc_sha256={d: v[0] for d, v in docinfo.items()}, doc_blob={d: v[1] for d, v in docinfo.items()})

# ---------- write ----------
written = {}
for rel, t in texts.items():
    b = t.encode("utf-8")
    if b == orig[rel]:
        continue
    dst = os.path.join(OUTROOT, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, "wb").write(b)
    written[rel] = dict(pre=hashlib.sha256(orig[rel]).hexdigest(), post=hashlib.sha256(b).hexdigest())
log["written"] = written
json.dump(log, open(LOG, "w"), indent=1, ensure_ascii=False)
print("md edits applied", len(log["edits"]), "held", len(log["held"]), "csv edits", len(log["csv"]), "context edits", len(log["context"]))
print("consolidated", {k: v for k, v in log["consolidated"].items() if k in ("rows_recomputed", "rows_changed", "standing_rows")})
for rel, h in written.items():
    print(h["post"], rel)
