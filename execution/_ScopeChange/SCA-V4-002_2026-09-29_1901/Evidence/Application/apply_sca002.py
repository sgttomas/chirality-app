#!/usr/bin/env python3
"""AK1 (run APP-V4-SCA002-20260929): apply the accepted, non-acceptance-conditional SCA-V4-002 edits.

Source of every byte: AMENDMENT_PACKET/BASIS_AMENDMENT.md at the accepted sha256 (DECISION-2).
Applied: A-01, B-02, B-05a, B-05b, B-06b, B-06c (5 files), then B-01 (RECOMPUTE, 31 rows).
Held:    B-04 and C-01 (after group-3 acceptance); B-06a (with the SoW REVISEs; DAG-002-bound file).
None:    B-03 (option A, no edit).

Usage: apply_sca002.py REPO OUTROOT LOG.json
  OUTROOT == REPO -> writes in place; otherwise mirrored copies under OUTROOT (dry run).

Rules: the packet is the accepted bytes; every target equals its blob at the basis commit; every old
block or value matches exactly once and the new one zero times before and once after; any failure
aborts before anything is written.
"""
import csv, hashlib, io, json, os, re, subprocess, sys

REPO, OUTROOT, LOG = sys.argv[1], sys.argv[2], sys.argv[3]
BASIS_COMMIT = "39c97257ba5c354cff31f14487c05b538e806197"
P = "projects/chirality-app-v4"
EX = f"{P}/execution"
DEC = f"{EX}/_Decomposition"
PK = f"{EX}/_Coordination/AgentRuns/APP-V4-SCA002-20260929/AMENDMENT_PACKET"
PACKET_SHA = "091871fd90283b27b2d067c1eeb3137e3cf8f9d50dab87ad92a9b871cc634238"
HI = f"{P}/docs/HOST_INTEGRATION.md"
CC = f"{DEC}/Consolidated_Coverage.csv"
CTX = {
    "DEL-02-03": f"{EX}/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/_CONTEXT.md",
    "DEL-05-01": f"{EX}/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-01_Minimal-loop and model receiving contract/_CONTEXT.md",
    "DEL-05-02": f"{EX}/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-02_Host panel and shared interaction receiving/_CONTEXT.md",
    "DEL-09-07": f"{EX}/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-07_Local host candidate qualification/_CONTEXT.md",
    "DEL-04-01": f"{EX}/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-01_Operation-policy and human-act distinctions/_CONTEXT.md",
}


def fail(msg):
    raise SystemExit("FAIL: " + msg)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git(*a):
    return subprocess.run(["git", "-C", REPO, *a], capture_output=True, check=True).stdout


pkt = open(os.path.join(REPO, PK, "BASIS_AMENDMENT.md"), "rb").read()
if sha(pkt) != PACKET_SHA:
    fail("BASIS_AMENDMENT.md is not the accepted bytes")
ba = pkt.decode("utf-8")
log = {"basis_commit": BASIS_COMMIT, "packet_sha256": PACKET_SHA, "edits": [], "held": [], "consolidated": {}, "files": {}}
orig, texts = {}, {}


def rd(rel):
    if rel not in texts:
        b = open(os.path.join(REPO, rel), "rb").read()
        if b != git("show", f"{BASIS_COMMIT}:{rel}"):
            fail(f"{rel} differs from its bytes at the basis commit")
        orig[rel] = b
        texts[rel] = b.decode("utf-8")
    return texts[rel]


def section(prefix, level):
    """Text of the packet section whose heading starts with `prefix`, up to the next heading of the same or higher level."""
    pat = re.compile(r"^" + "#" * level + r" " + re.escape(prefix) + r".*?$", re.M)
    m = list(pat.finditer(ba))
    if len(m) != 1:
        fail(f"packet heading {prefix!r} found {len(m)} times")
    rest = ba[m[0].end():]
    out, fenced = [], False
    for l in rest.split("\n"):
        if l.startswith("```"):
            fenced = not fenced
        elif not fenced and re.match(r"#{1," + str(level) + r"} ", l):
            break
        out.append(l)
    return "\n".join(out)


def pair(sec, label):
    blocks = re.findall(r"^```(old|new)\n(.*?)\n```$", sec, flags=re.M | re.S)
    if [b[0] for b in blocks] != ["old", "new"]:
        fail(f"{label}: expected one old/new pair, got {[b[0] for b in blocks]}")
    for b in blocks:
        if re.search(r"\{[A-Z0-9_]+\}", b[1]):
            fail(f"{label}: carries a token; it is acceptance-conditional")
    return blocks[0][1], blocks[1][1]


def replace_once(rel, old, new, label):
    t = rd(rel)
    c_old, c_new = t.count(old), t.count(new)
    # the new block may contain the old block as a prefix (append-style edits); count occurrences of new only
    if c_old != 1 or c_new != 0:
        fail(f"{label} {rel}: old count {c_old}, new count {c_new}")
    t2 = t.replace(old, new)
    if t2.count(new) != 1:
        fail(f"{label} {rel}: new count after {t2.count(new)}")
    texts[rel] = t2
    log["edits"].append(dict(edit=label, target=rel, mode="text", old_count_before=c_old, new_count_before=c_new,
                             new_count_after=1, old_sha256=sha(old.encode()), new_sha256=sha(new.encode())))


def csv_rows(t):
    return list(csv.reader(io.StringIO(t, newline="")))


def csv_text(rows):
    o = io.StringIO(newline="")
    csv.writer(o, lineterminator="\r\n").writerows(rows)
    return o.getvalue()


def set_field(rel, key_col, key, col, old, new, label, substring):
    t = rd(rel)
    rows = csv_rows(t)
    if csv_text(rows) != t:
        fail(f"{rel}: CSV round-trip not byte-exact")
    hdr = rows[0]
    ki, ci = hdr.index(key_col), hdr.index(col)
    hits = [r for r in rows[1:] if r[ki] == key]
    if len(hits) != 1:
        fail(f"{label}: {rel} key {key} rows {len(hits)}")
    r = hits[0]
    if substring:
        c, cn = r[ci].count(old), r[ci].count(new)
        if c != 1 or cn != 0:
            fail(f"{label}: substring count {c}, new count {cn} in {rel} {key}.{col}")
        file_count = t.count(old)
        r[ci] = r[ci].replace(old, new)
    else:
        if r[ci] != old:
            fail(f"{label}: {rel} {key}.{col} old value differs")
        file_count = None
        r[ci] = new
    texts[rel] = csv_text(rows)
    log["edits"].append(dict(edit=label, target=rel, mode="csv-substring" if substring else "csv-field", key=key, column=col,
                             old_count_in_field=1, old_count_in_file=file_count, old_sha256=sha(old.encode()),
                             new_sha256=sha(new.encode()), new_field_value=r[ci]))


def table_rows(sec, first_cell_regex):
    out = []
    for l in sec.splitlines():
        if l.startswith("|"):
            cells = [c.strip() for c in l.strip().strip("|").split(" | ")]
            if re.match(first_cell_regex, cells[0]):
                out.append(cells)
    return out


def tick(s):
    if not (s.startswith("`") and s.endswith("`")) or "`" in s[1:-1]:
        fail(f"cell is not one backtick-quoted value: {s[:40]!r}")
    return s[1:-1]


# ---------- A-01 ----------
old, new = pair(section("A-01", 3), "A-01")
replace_once(HI, old, new, "A-01")

# ---------- B-02 (Q-7 accepted) ----------
(b02,) = table_rows(section("B-02", 3), r"^OI-012 · `Consequence`$")
set_field(f"{DEC}/Open_Issues.csv", "OpenIssueID", "OI-012", "Consequence", tick(b02[1]), tick(b02[2]), "B-02", substring=False)

# ---------- B-03: option A, no edit ----------
log["held"].append(dict(edit="B-03", state="NO_EDIT", reason="Q-5 option A accepted: OI-001/OI-002 stay OPEN"))

# ---------- B-04: held ----------
b04_old, b04_new = re.findall(r"^```(?:old|new)\n(.*?)\n```$", section("B-04", 3), flags=re.M | re.S)
c = rd(f"{DEC}/SOFTWARE_DECOMP.md").count(b04_old)
if c != 1:
    fail(f"B-04 old block count {c}")
log["held"].append(dict(edit="B-04", state="HELD_UNTIL_GROUP3_ACCEPTANCE", target=f"{DEC}/SOFTWARE_DECOMP.md",
                        old_count_now=c, tokens=sorted(set(re.findall(r"\{[A-Z0-9_]+\}", b04_new)))))

# ---------- B-05 (Q-11 accepted) ----------
sec = section("B-05", 3)
(a,) = table_rows(sec, r"^B-05a$")
(b,) = table_rows(sec, r"^B-05b$")
o5, n5 = tick(a[2]), tick(a[3])
if (b[2], b[3]) != ("same", "same"):
    fail("B-05b is not 'same'")
if a[1] != "`Deliverables.csv` DEL-04-01 · `Description`":
    fail("B-05a row/column cell")
set_field(f"{DEC}/Deliverables.csv", "DeliverableID", "DEL-04-01", "Description", o5, n5, "B-05a", substring=True)
t = rd(CTX["DEL-04-01"])
L = t.split("\n")
if not L[12].startswith("- **Description:** ") or L[12].count(o5) != 1:
    fail("B-05b: line 13 is not the Description line carrying the old substring once")
replace_once(CTX["DEL-04-01"], o5, n5, "B-05b")

# ---------- B-06 (Q-12 option (a) accepted) ----------
o6a, n6a = pair(section("B-06a", 4), "B-06a")
rel6a = f"{DEC}/checkpoint_snapshots/_LATEST_ACCEPTED.md"
raw6a = open(os.path.join(REPO, rel6a), "rb").read()
if raw6a != git("show", f"{BASIS_COMMIT}:{rel6a}"):
    fail("B-06a target differs from the basis commit")
log["held"].append(dict(edit="B-06a", state="HELD_WITH_SOW_REVISE_STAGE", target=rel6a, old_count_now=raw6a.decode().count(o6a),
                        sha256_unchanged=sha(raw6a), reason="bound in _DAG/DAG-002/SOURCE_MANIFEST.sha256; packet: apply with the SoW REVISEs"))
if raw6a.decode().count(o6a) != 1:
    fail("B-06a old count")
o6b, n6b = pair(section("B-06b", 4), "B-06b")
replace_once(f"{DEC}/_LATEST.md", o6b, n6b, "B-06b")
sec6c = section("B-06c", 4)
if "DEL-02-03, DEL-05-01, DEL-05-02, DEL-09-07 and DEL-04-01" not in ba:
    fail("B-06c target list")
o6c, n6c = pair(sec6c, "B-06c")
for d in ("DEL-02-03", "DEL-05-01", "DEL-05-02", "DEL-09-07", "DEL-04-01"):
    t = rd(CTX[d])
    if t.split("\n")[2].count(o6c) != 1:
        fail(f"B-06c {d}: old string is not on line 3 once")
    replace_once(CTX[d], o6c, n6c, f"B-06c/{d}")

# ---------- C-01: held ----------
log["held"].append(dict(edit="C-01", state="HELD_UNTIL_GROUP3_ACCEPTANCE", target=f"{EX}/_ScopeChange/_LATEST.md"))

# ---------- B-01 RECOMPUTE (SCA-V4-001 B8 rule: SHA256, ReadSnapshot, SourceLine) ----------
b01 = section("B-01", 3)
exp = {}
for cells in table_rows(b01, r"^`(SHA256|ReadSnapshot)`$"):
    exp[tick(cells[0])] = (tick(cells[1]), tick(cells[2]))
cc = rd(CC)
rows = csv_rows(cc)
if csv_text(rows) != cc:
    fail("Consolidated_Coverage.csv round-trip not byte-exact")
hdr = rows[0]
ix = {c: hdr.index(c) for c in hdr}
data = texts[HI].encode("utf-8")
blob = subprocess.run(["git", "hash-object", "--stdin"], input=data, capture_output=True, check=True).stdout.decode().strip()
new_sha, new_blob = sha(data), "git-blob:" + blob
if (new_sha, new_blob) != (exp["SHA256"][1], exp["ReadSnapshot"][1]):
    fail(f"A-01 result {new_sha} {new_blob} differs from the packet's stated result")
Lines = texts[HI].splitlines()
n_rows, changed_cols, deltas, untouched = 0, {}, set(), 0
for r in rows[1:]:
    if r[ix["Document"]] != HI:
        untouched += 1
        continue
    if (r[ix["SHA256"]], r[ix["ReadSnapshot"]]) != (exp["SHA256"][0], exp["ReadSnapshot"][0]):
        fail("B-01: a row does not carry the packet's old SHA256/ReadSnapshot")
    rid = r[ix["ConsolidatedRequirementID"]]
    pat = re.compile(r"^(- \*\*|\*\*|\| )" + re.escape(rid) + r"(?![0-9A-Za-z])")
    hits = [n + 1 for n, l in enumerate(Lines) if pat.search(l)]
    if not hits:
        fail(f"B-01 {rid}: no definition line")
    oldline = int(r[ix["SourceLine"]])
    if oldline < 40 or hits[0] != oldline + 1:
        fail(f"B-01 {rid}: line {oldline} -> {hits[0]} is not n+1 with n >= 40")
    before = list(r)
    r[ix["SHA256"]], r[ix["ReadSnapshot"]], r[ix["SourceLine"]] = new_sha, new_blob, str(hits[0])
    for c_ in hdr:
        if before[ix[c_]] != r[ix[c_]]:
            changed_cols[c_] = changed_cols.get(c_, 0) + 1
    n_rows += 1
if n_rows != 31:
    fail(f"B-01 rows {n_rows}")
if changed_cols != {"SHA256": 31, "ReadSnapshot": 31, "SourceLine": 31}:
    fail(f"B-01 changed columns {changed_cols}")
texts[CC] = csv_text(rows)
log["consolidated"] = dict(rows_recomputed=n_rows, rows_untouched_other_documents=untouched, changed_columns=changed_cols,
                           rule="SCA-V4-001 B8 rule (Decision_Log E-4); every row n -> n+1, n >= 40",
                           doc_sha256=new_sha, doc_blob=new_blob)

# ---------- B-05 mirror consistency ----------
drow = [r for r in csv_rows(texts[f"{DEC}/Deliverables.csv"])[1:] if r[0] == "DEL-04-01"][0]
dhdr = csv_rows(texts[f"{DEC}/Deliverables.csv"])[0]
desc = drow[dhdr.index("Description")]
ctx_line = texts[CTX["DEL-04-01"]].split("\n")[12]
log["b05_mirror"] = dict(context_line_13=ctx_line, deliverables_description=desc,
                         byte_consistent=(ctx_line == "- **Description:** " + desc))
pre_ctx = orig[CTX["DEL-04-01"]].decode().split("\n")[12]
pre_desc = [r for r in csv_rows(orig[f"{DEC}/Deliverables.csv"].decode())[1:] if r[0] == "DEL-04-01"][0][dhdr.index("Description")]
log["b05_mirror"]["byte_consistent_before"] = (pre_ctx == "- **Description:** " + pre_desc)

# ---------- write ----------
for rel, t in texts.items():
    b = t.encode("utf-8")
    written = b != orig[rel]
    if written:
        dst = os.path.join(OUTROOT, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, "wb").write(b)
    log["files"][rel] = dict(pre=sha(orig[rel]), post=sha(b), written=written)
json.dump(log, open(LOG, "w"), indent=1, ensure_ascii=False)
print("edits", len(log["edits"]), "held", [h["edit"] for h in log["held"]], "consolidated", log["consolidated"]["rows_recomputed"])
print("b05 mirror", log["b05_mirror"]["byte_consistent_before"], "->", log["b05_mirror"]["byte_consistent"])
for rel, h in log["files"].items():
    print(h["post"], "W" if h["written"] else "-", rel)
