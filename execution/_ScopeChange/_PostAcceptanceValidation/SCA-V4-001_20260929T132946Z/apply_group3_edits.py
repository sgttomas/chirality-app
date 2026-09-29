#!/usr/bin/env python3
"""AK2: apply the SCA-V4-001 acceptance-conditional edits after checkpoint group 3 (owner DECISION-8).

H-1 A07 (3 pairs, PRD.md), H-2 A17a-c (ARCHITECTURE, HOST_INTEGRATION, EXAMINATION), H-3 D-15
(SOFTWARE_DECOMP.md), from the accepted BASIS_AMENDMENT.md text, with the tokens filled from the
accepted group-3 record; then H-4, the second B8 recompute of Consolidated_Coverage.csv.

Usage: apply_group3_edits.py REPO OUTROOT LOG.json
  OUTROOT == REPO -> writes in place; otherwise writes mirrored copies under OUTROOT (dry run).

Rules:
- the packet must be the accepted bytes (sha256 04bdc916...24cf);
- every target must still carry its accepted candidate bytes (the blob at the basis commit);
- every filled "old" block must occur exactly once and its filled "new" block zero times before, once after;
- no token may remain unfilled;
- B8 second pass: SHA256, ReadSnapshot (git blob) and SourceLine of the 126 rows of the four amended
  documents take the post-edit values by the same rule as the first pass; Standing already carries
  "amended by SCA-V4-001" on the nine amended IDs from the first pass and is not appended again
  (recorder's reading of B8: "recompute after the Part A edits", applied once more after A07/A17);
- nothing else is touched: any failure aborts before writing.
"""
import csv, hashlib, io, json, os, re, subprocess, sys

REPO, OUTROOT, LOG = sys.argv[1], sys.argv[2], sys.argv[3]
BASIS_COMMIT = "3d006a909d722606b2f69f8c71a7020e5c86a619"
FILL = {"{AMENDMENT_ID}": "SCA-V4-001", "{ACCEPT_DATE}": "2026-09-29",
        "{AMENDMENT_SNAPSHOT}": "SCA-V4-001_2026-09-28_2155"}
AID = FILL["{AMENDMENT_ID}"]
P = "projects/chirality-app-v4"
EX = f"{P}/execution"
DEC = f"{EX}/_Decomposition"
PK = f"{EX}/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/AMENDMENT_PACKET"
PACKET_SHA = "04bdc91622223510870ac8fe3994d708641c5e07a7853c5abc75ac59c0ed24cf"
DOCS = {"PRD.md": f"{P}/docs/PRD.md", "ARCHITECTURE.md": f"{P}/docs/ARCHITECTURE.md",
        "HOST_INTEGRATION.md": f"{P}/docs/HOST_INTEGRATION.md", "EXAMINATION.md": f"{P}/docs/EXAMINATION.md",
        "_Decomposition/SOFTWARE_DECOMP.md": f"{DEC}/SOFTWARE_DECOMP.md"}
HELD = ["A07", "A17a", "A17b", "A17c", "D-15"]
H_OF = {"A07": "H-1", "A17a": "H-2", "A17b": "H-2", "A17c": "H-2", "D-15": "H-3"}
CC = f"{DEC}/Consolidated_Coverage.csv"


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

log = {"basis_commit": BASIS_COMMIT, "fill": FILL, "packet_sha256": PACKET_SHA, "edits": [], "consolidated": {}, "files": {}}
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


# ---------- H-1, H-2, H-3 ----------
found = []
for s in re.split(r"^#### ", ba, flags=re.M)[1:]:
    eid = s.splitlines()[0].split(" ")[0]
    if eid not in HELD:
        continue
    tgt = DOCS[re.search(r"^Target: (\S+)", s, re.M).group(1)]
    blocks = re.findall(r"^```(old|new)\n(.*?)\n```$", s, flags=re.M | re.S)
    if len(blocks) % 2:
        fail(f"{eid} unpaired blocks")
    for i in range(0, len(blocks), 2):
        if (blocks[i][0], blocks[i + 1][0]) != ("old", "new"):
            fail(f"{eid} block order")
        found.append((eid, i // 2 + 1, tgt, blocks[i][1], blocks[i + 1][1]))
if [f[0] for f in found] != ["A07", "A07", "A07", "A17a", "A17b", "A17c", "D-15"]:
    fail(f"held edit list {[f[0] for f in found]}")

for eid, pair, rel, old, new_t in found:
    new = new_t
    tokens = sorted(set(re.findall(r"\{[A-Z_]+\}", new_t)))
    for k, v in FILL.items():
        new = new.replace(k, v)
    if re.search(r"\{[A-Z_]+\}", new) or re.search(r"\{[A-Z_]+\}", old):
        fail(f"{eid}.{pair} unfilled token")
    t = rd(rel)
    c_old, c_new = t.count(old), t.count(new)
    if c_old != 1 or c_new != 0:
        fail(f"{eid}.{pair} {rel}: old count {c_old}, new count {c_new}")
    t2 = t.replace(old, new)
    if t2.count(new) != 1:
        fail(f"{eid}.{pair} new count after {t2.count(new)}")
    texts[rel] = t2
    log["edits"].append(dict(item=H_OF[eid], edit=eid, pair=pair, target=rel, tokens=tokens,
                             old_count_before=c_old, new_count_before=c_new, new_count_after=1,
                             old_sha256=sha(old.encode()), new_filled_sha256=sha(new.encode()), new_filled=new))

# ---------- H-4: second B8 recompute ----------
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
AMENDED = {"V4-WF-05", "V4-HOST-01", "V4-HOST-02", "V4-ARC-11", "V4-ARC-12", "V4-HI-42", "V4-HI-70", "V4-EXM-22", "V4-EXM-23"}
SUFFIX = " amended by " + AID
doc4 = [v for k, v in DOCS.items() if not k.endswith("SOFTWARE_DECOMP.md")]
info, per_doc, changed_cols, changed_rows, untouched = {}, {}, {}, 0, 0
before_rows = [list(r) for r in rows]
for r in rows[1:]:
    doc = r[ix["Document"]]
    if doc not in doc4:
        untouched += 1
        continue
    if doc not in info:
        data = rd(doc).encode("utf-8")
        blob = subprocess.run(["git", "hash-object", "--stdin"], input=data, capture_output=True, check=True).stdout.decode().strip()
        info[doc] = (sha(data), "git-blob:" + blob, rd(doc).splitlines())
    s, gb, L = info[doc]
    rid = r[ix["ConsolidatedRequirementID"]]
    pat = re.compile(r"^(- \*\*|\*\*|\| )" + re.escape(rid) + r"(?![0-9A-Za-z])")
    hits = [n + 1 for n, l in enumerate(L) if pat.search(l)]
    if not hits:
        fail(f"B8 {rid}: no definition line")
    has = r[ix["Standing"]].endswith(SUFFIX)
    if has != (rid in AMENDED) or r[ix["Standing"]].count("amended by") > 1:
        fail(f"B8 {rid}: Standing suffix state unexpected")
    old = list(r)
    r[ix["SHA256"]], r[ix["ReadSnapshot"]], r[ix["SourceLine"]] = s, gb, str(hits[0])
    for c in hdr:
        if old[ix[c]] != r[ix[c]]:
            changed_cols[c] = changed_cols.get(c, 0) + 1
    changed_rows += old != r
    per_doc[doc] = per_doc.get(doc, 0) + 1
if sorted(per_doc.values()) != [13, 22, 31, 60]:
    fail(f"B8 row counts {per_doc}")
if set(changed_cols) - {"SHA256", "ReadSnapshot", "SourceLine"}:
    fail(f"B8 changed other columns {changed_cols}")
texts[CC] = csv_text(rows)
log["consolidated"] = dict(rows_recomputed=sum(per_doc.values()), rows_changed=changed_rows, rows_untouched_other_documents=untouched,
                           changed_columns=changed_cols, per_doc=per_doc, standing_rows_with_suffix=sum(1 for r in rows[1:] if r[ix["Standing"]].endswith(SUFFIX)),
                           doc_sha256={d: v[0] for d, v in info.items()}, doc_blob={d: v[1] for d, v in info.items()})

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
print("edits", len(log["edits"]), "consolidated", {k: log["consolidated"][k] for k in ("rows_recomputed", "rows_changed", "changed_columns", "standing_rows_with_suffix")})
for rel, h in log["files"].items():
    print(h["post"], rel)
