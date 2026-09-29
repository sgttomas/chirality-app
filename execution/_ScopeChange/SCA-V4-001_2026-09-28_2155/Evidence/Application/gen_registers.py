#!/usr/bin/env python3
"""AK1: transcribe the accepted SCA-V4-001 packet into the _ScopeChange CSV artifacts.

Sources (read-only): AMENDMENT_PACKET/IMPACT_ASSESSMENT.md §3 and §3.1, §7;
BASIS_AMENDMENT.md (new blocks, B2 table); original-seed files.
Writes: Intake_Actions.csv, Amendment_Actions.csv, Supersession_Delta.csv into OUT.
"""
import csv, glob, io, os, re, sys

REPO = sys.argv[1]
OUT = sys.argv[2]
AID = "SCA-V4-001"
P = "projects/chirality-app-v4"
EX = f"{P}/execution"
PK = f"{EX}/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/AMENDMENT_PACKET"
SEED = f"{EX}/_Coordination/Acceptances/APP-V4-BASIS-20260926/original-seed"
ia = open(os.path.join(REPO, PK, "IMPACT_ASSESSMENT.md"), encoding="utf-8").read()
ba = open(os.path.join(REPO, PK, "BASIS_AMENDMENT.md"), encoding="utf-8").read()

def norm(s):
    return re.sub(r"\s+", " ", s).strip()

def delfolder(d):
    hits = glob.glob(os.path.join(REPO, EX, "PKG-*", "1_Working", d + "_*"))
    assert len(hits) == 1, (d, hits)
    return os.path.relpath(hits[0], REPO)

# ---- register (IA §3.1) ----
m = re.search(r"### 3\.1 .*?```csv\n(.*?)\n```", ia, re.S)
reg = list(csv.DictReader(io.StringIO(m.group(1))))
assert len(reg) == 47, len(reg)
cols = list(reg[0].keys())
assert cols == ["AmendmentID", "ActionSeq", "ActionType", "EntityType", "EntityID", "Description", "AffectedFiles",
                "DownstreamReruns", "SupersessionBindingPresent", "ScopeChanging"], cols
DEC = f"{EX}/_Decomposition"
for r in reg:
    assert r["AmendmentID"] == "{AMENDMENT_ID}"
    r["AmendmentID"] = AID
    if r["EntityType"] == "DELIVERABLE":
        folder = delfolder(r["EntityID"])
        full = []
        for f in r["AffectedFiles"].split(";"):
            f = f.strip()
            if f == "ScopeOfWork.md":
                full.append(f"{folder}/ScopeOfWork.md")
            elif f == "_CONTEXT.md":
                full.append(f"{folder}/_CONTEXT.md")
            elif f == "Deliverables.csv":
                full.append(f"{DEC}/Deliverables.csv")
            else:
                raise SystemExit(f"unexpected AffectedFiles token {f!r}")
        r["AffectedFiles"] = ";".join(full)
    for k in cols:
        assert r[k] == r[k].strip(), (r["ActionSeq"], k)

def write(path, rows, fields):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})

write(os.path.join(OUT, "Amendment_Actions.csv"), reg, cols)

# ---- intake (IA §3 table) ----
sec3 = ia.split("## 3. Atomic actions", 1)[1].split("### 3.1", 1)[0]
trows = [l for l in sec3.splitlines() if re.match(r"^\| A\d\d \|", l)]
assert len(trows) == 47, len(trows)
intake = []
for line, r in zip(trows, reg):
    c = [x.strip() for x in line.strip().strip("|").split(" | ")]
    assert len(c) == 6, c
    num, at, et, eid, req, sec = c
    eid = eid.strip("`")
    assert int(num[1:]) == int(r["ActionSeq"]) and at == r["ActionType"] and et == r["EntityType"], (num, at, et)
    if eid != r["EntityID"]:
        print("intake EntityID (IA §3) differs from register (IA §3.1):", num, repr(eid), "->", repr(r["EntityID"]))
    req = req.replace("**", "").replace("`", "")
    intake.append(dict(r, EntityID=eid, Description=f"{req} [AffectedSections: {sec.replace('`', '')}]", ScopeChanging="", Status="PROPOSED"))
write(os.path.join(OUT, "Intake_Actions.csv"), intake, cols + ["Status"])

# ---- supersession delta (IA §7) ----
def block_new(eid_heading, idx=0):
    sec = re.split(r"^#### ", ba, flags=re.M)
    s = [x for x in sec if x.startswith(eid_heading)]
    assert len(s) == 1, eid_heading
    news = re.findall(r"^```new\n(.*?)\n```$", s[0], flags=re.M | re.S)
    return news[idx]

def seed(doc, a, b):
    L = open(os.path.join(REPO, SEED, doc), encoding="utf-8").read().splitlines()
    return norm(" ".join(L[a - 1:b]))

def tbl_row(text, rid):
    return [x for x in text.splitlines() if x.startswith(f"| {rid} |")]

a0203 = block_new("A02 and A03")
host01 = norm(a0203.split("- **V4-HOST-02**")[0])
host02 = norm("- **V4-HOST-02**" + a0203.split("- **V4-HOST-02**")[1])
a0809 = block_new("A08 and A09")
arc11 = norm(tbl_row(a0809, "V4-ARC-11")[0]); arc12 = norm(tbl_row(a0809, "V4-ARC-12")[0])
# the D-09 vocabulary Notes (B2 table)
b2 = [l for l in ba.splitlines() if l.startswith("| D-09 |")][0]
b2c = [x.strip() for x in b2.strip().strip("|").split(" | ")]
seed_arc = open(os.path.join(REPO, SEED, "ARCHITECTURE.md"), encoding="utf-8").read()
vocab_g3 = f"{DEC}/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Vocabulary_Map.csv"
vg = {r["CanonicalTerm"]: r for r in csv.DictReader(open(os.path.join(REPO, vocab_g3), encoding="utf-8", newline=""))}
assert vg["Declared checkpoint"]["Notes"] == b2c[1], "B2 old Notes differs from GROUP3 canonical"

GOV = "Owner record: execution/_Coordination/AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md"
rows = [
 ("D-001", f"{SEED}/PRD.md", "V4-WF-05 (lines 159-161); also ScopeLedger SOW-052 (GROUP3 canonical)", "V4_WF_05_CHECKPOINT_HOLD",
  seed("PRD.md", 159, 161), norm(block_new("A01")),
  "DECISION-4 D4-1. Phased, not withdrawn: the superseded hold holds again for workflows that take up the governance phase (O-21). Also covers register actions 21 (SOW-052) and 36 (DEL-02-03 Deliverables.csv text D-10a/b)."),
 ("D-002", f"{SEED}/PRD.md", "V4-HOST-01 (lines 84-86); also ScopeLedger SOW-015, SOW-016 (GROUP3 canonical)", "V4_HOST_01_MODEL_DEFAULT",
  seed("PRD.md", 84, 86), host01,
  "DECISION-4 D4-3. Also covers register actions 18-19 (SOW-015, SOW-016) and 42 (DEL-05-01 Deliverables.csv text D-11a)."),
 ("D-003", f"{SEED}/PRD.md", "V4-HOST-02 (lines 87-88); also ScopeLedger SOW-017 (GROUP3 canonical)", "V4_HOST_02_DESTINATIONS",
  seed("PRD.md", 87, 88), host02,
  "DECISION-5 revised V4-HOST-02, verbatim. Also covers register actions 20 (SOW-017), 42 (DEL-05-01 D-11b/c/d) and 46 (DEL-09-07 D-12a/c)."),
 ("D-008", f"{SEED}/ARCHITECTURE.md", "V4-ARC-11 (line 113)", "V4_ARC_11_MODEL_DEFAULT",
  norm(tbl_row(seed_arc, "V4-ARC-11")[0]), arc11, "DECISION-4 D4-3; as D-002."),
 ("D-009", f"{SEED}/ARCHITECTURE.md", "V4-ARC-12 (line 114); also ScopeLedger SOW-137, SOW-138 (GROUP3 canonical)", "V4_ARC_12_NETWORK",
  norm(tbl_row(seed_arc, "V4-ARC-12")[0]), arc12,
  "DECISION-4 D4-3; DECISION-5. Also covers register actions 22-23 (SOW-137, SOW-138)."),
 ("D-010", f"{SEED}/ARCHITECTURE.md", "Properties the host agent must hold, first bullet (lines 120-121)", "HOST_AGENT_LOCAL_ONLY_PROPERTY",
  seed("ARCHITECTURE.md", 120, 121), norm(block_new("A10")), "DECISION-5 effects, point by point."),
 ("D-012", f"{SEED}/HOST_INTEGRATION.md", "V4-HI-42 (lines 112-113)", "V4_HI_42_CHECKPOINT_OVERRIDE",
  seed("HOST_INTEGRATION.md", 112, 113), norm(block_new("A12")),
  "DECISION-4 D4-1; as D-001. Phased, not withdrawn: the superseded wait holds again for workflows that take up the governance phase (O-21)."),
 ("D-015", f"{SEED}/EXAMINATION.md", "V4-EXM-22 (line 84, final sentence); also ScopeLedger SOW-201 (GROUP3 canonical)", "V4_EXM_22_CHECKPOINT_STOPS_RUN",
  "A workflow checkpoint stops the run for a human act.", norm(block_new("A15")).split("proposes the second. ", 1)[1],
  "DECISION-4 D4-1; as D-001, for the examination. Also covers register actions 24 (SOW-201) and 46 (DEL-09-07 D-12b)."),
 ("D-016", f"{SEED}/EXAMINATION.md", "V4-EXM-23 (lines 87-89); also ScopeLedger SOW-202 (GROUP3 canonical)", "V4_EXM_23_ENDPOINT_ONLY",
  seed("EXAMINATION.md", 87, 89), norm(block_new("A16")),
  "DECISION-5. Also covers register action 25 (SOW-202)."),
 ("D-006", f"{SEED}/PRD.md", "Section 1 purpose quotation (lines 28-30; blockquote markers removed)", "PURPOSE_LOCAL_FIRST",
  "In host applications the agent runs local-first, on a model server the user controls.",
  "In host applications the agent runs on a model the person chooses — a model server the user controls or a cloud model — with no default.",
  "DECISION-4 D4-3; owner item O-8 (accepted, DECISION-7)."),
 ("D-026", vocab_g3, "CanonicalTerm 'Declared checkpoint', column Notes", "VOCAB_DECLARED_CHECKPOINT",
  b2c[1], b2c[2], "DECISION-4 D4-1; phased reading of the vocabulary term (register action 26)."),
]
# sanity: seed quotes for D-006 and D-015 are verbatim substrings of the normalized seed text
assert "In host applications the agent runs local-first, on a model server the user controls." in norm(seed("PRD.md", 28, 30).replace("> ", " "))
assert "A workflow checkpoint stops the run for a human act." in seed("EXAMINATION.md", 84, 84)
assert norm(rows[9][5]) in norm(block_new("A06").replace("> ", " "))
SUP = ["AmendmentID", "DecisionID", "SupersededAuthorityRole", "SupersededAuthorityPath", "SupersededAuthorityRef", "SupersededFactKey",
       "SupersededFactTextOrValue", "OverrideType", "ReplacementFactTextOrValue", "AppliesToRoots", "AppliesToFacilities",
       "AppliesToSections", "Notes"]
out = []
for did, path, ref, key, old, new, note in rows:
    assert os.path.exists(os.path.join(REPO, path)), path
    out.append(dict(AmendmentID=AID, DecisionID=did, SupersededAuthorityRole="OTHER", SupersededAuthorityPath=path,
                    SupersededAuthorityRef=ref, SupersededFactKey=key, SupersededFactTextOrValue=old, OverrideType="SUPERSESSION",
                    ReplacementFactTextOrValue=new, AppliesToRoots="", AppliesToFacilities="", AppliesToSections="",
                    Notes=note + " Transcribed from IMPACT_ASSESSMENT §7 (accepted, DECISION-7); original and replacement text quoted in full from the seed and BASIS_AMENDMENT, whitespace-normalized."))
write(os.path.join(OUT, "Supersession_Delta.csv"), out, SUP)
yes = sorted(int(r["ActionSeq"]) for r in reg if r["SupersessionBindingPresent"] == "YES")
print("register rows", len(reg), "intake rows", len(intake), "delta rows", len(out), "YES rows", yes)
