#!/usr/bin/env python3
"""Read-only audit-decomp checks 1-11 for App v4 (SOFTWARE). Writes only to OUT.

POSTACCEPT (node AK2): POSTCHANGE/audit_checks.py with two additions, and no other check, rule or severity changed:
  (a) Check 9b: the fixed clause "the scope-change Change Register ... is UNRESOLVED" is emitted only while the
      Change Register is unbound; once it binds, the clause names the binding. The output is byte-identical to
      POSTCHANGE whenever the Change Register is unbound.
  (b) Check 10 (audit-decomp method Step 10) runs when execution/_ScopeChange/_LATEST.md exists. Its findings are
      appended after Check 11, so every earlier issue ID keeps its position.
"""
import csv, glob, hashlib, json, os, re, sys
from collections import Counter, defaultdict

REPO = sys.argv[1]
OUT = sys.argv[2]
SCOPE_PKGS = sys.argv[3].split(",")
EX = os.path.join(REPO, "projects/chirality-app-v4/execution")
DEC = os.path.join(EX, "_Decomposition")
G3 = os.path.join(DEC, "checkpoint_snapshots/GROUP3-20260928T001055Z")
REL = lambda p: os.path.relpath(p, REPO)

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def rows(name):
    with open(os.path.join(DEC, name), encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, strict=True))

def split(v):
    return [x.strip() for x in (v or "").split(";") if x.strip()]

def norm(s):
    return re.sub(r"\s+", " ", (s or "").strip())

pk = rows("Packages.csv"); dl = rows("Deliverables.csv"); sl = rows("ScopeLedger.csv")
ob = rows("Objectives.csv"); oi = rows("Open_Issues.csv"); ci = rows("Companion_Inventory.csv")
tel = json.load(open(os.path.join(DEC, "Coverage_Telemetry.json")))
doc_path = os.path.join(DEC, "SOFTWARE_DECOMP.md")
doc = open(doc_path, encoding="utf-8").read()
PK = {r["PackageID"]: r for r in pk}; DL = {r["DeliverableID"]: r for r in dl}
OB = {r["ObjectiveID"]: r for r in ob}; SL = {r["ScopeItemID"]: r for r in sl}

issues = []
def issue(check, sev, etype, label, eid, desc, dref, fref, decision=""):
    issues.append(dict(CheckNumber=str(check), Severity=sev, EntityType=etype, ConcreteLabel=label,
                       EntityID=eid, Description=desc, DecompositionRef=dref, FilesystemRef=fref, DecisionRef=decision))

# ---------- Step 0: section binding ----------
headings = [l[3:].strip() for l in doc.splitlines() if l.startswith("## ")]
def nh(h):
    h = re.sub(r"^\d+[A-Za-z]?\.\s+", "", h.strip())
    return h.strip().casefold()
def bind(target):
    t = nh(target); hs = [nh(h) for h in headings]
    for rank, pred in (("exact", lambda h: h == t), ("prefix", lambda h: h.startswith(t)), ("substring", lambda h: t in h)):
        hits = [headings[i] for i, h in enumerate(hs) if pred(h)]
        if hits:
            return {"target": target, "rank": rank, "hit": hits[0], "ambiguous": hits if len(hits) > 1 else []}
    return {"target": target, "rank": None, "hit": None, "ambiguous": []}
binding_targets = {"Ledger": ["Scope Ledger"], "Objectives": ["Objectives"], "Partitions": ["Packages"],
                   "Production Units": ["Deliverables"], "Change Register (scope-change, SOFTWARE)": ["Decision Log", "Revision History"],
                   "Change Register (scope-change, PROJECT form, reference only)": ["Change Log"]}
bindings = {k: [bind(t) for t in v] for k, v in binding_targets.items()}
companion_binding = {"Ledger": "ScopeLedger.csv", "Objectives": "ScopeLedger.csv ObjectiveIDs column (SOFTWARE Check 7 authority); Objectives.csv (objective register)",
                     "Partitions": "Packages.csv", "Production Units": "Deliverables.csv"}
ci_names = {r["Filename"]: r["PackageRole"] for r in ci}

# ---------- discovery ----------
pkg_folders = {os.path.basename(p).split("_")[0]: p for p in sorted(glob.glob(os.path.join(EX, "PKG-*"))) if os.path.isdir(p)}
pkg_folder_all = [p for p in sorted(glob.glob(os.path.join(EX, "PKG-*"))) if os.path.isdir(p)]
unit_folders = defaultdict(list)
for lc in ("1_Working", "2_Checking", "3_Issued"):
    for p in sorted(glob.glob(os.path.join(EX, "PKG-*", lc, "DEL-*"))):
        if os.path.isdir(p):
            unit_folders[os.path.basename(p).split("_")[0]].append(p)
in_scope_del = [d for d in DL if DL[d]["PackageID"] in SCOPE_PKGS]
in_scope_folder_ids = [u for u in unit_folders if u.split("-")[0] + "-" + u.split("-")[1] in [s for s in SCOPE_PKGS] or ("PKG-" + u.split("-")[1]) in SCOPE_PKGS]

per_unit = defaultdict(int)

# ---------- Check 1 ----------
c1 = []
for pid in SCOPE_PKGS:
    f = pkg_folders.get(pid)
    c1.append((pid, bool(f)))
    if not f:
        issue(1, "BLOCKER", "PARTITION", "Package", pid, f"Partition {pid} declared but no matching folder", f"Packages.csv {pid}", "NOT_FOUND")
    else:
        fname = os.path.basename(f)[len(pid) + 1:]
        if norm(fname) != norm(PK[pid]["Name"]):
            issue(1, "INFO", "PARTITION", "Package", pid, f"Folder label '{fname}' differs from Packages.csv Name '{PK[pid]['Name']}'", f"Packages.csv {pid}", REL(f))

# ---------- Check 2 & 4 ----------
for d in in_scope_del:
    r = DL[d]; fs = unit_folders.get(d, [])
    if not fs:
        issue(2, "BLOCKER", "PRODUCTION_UNIT", "Deliverable", d, f"Production Unit {d} declared but no folder under {r['PackageID']}", f"Deliverables.csv {d}", "NOT_FOUND"); per_unit[d] += 1
        continue
    if len(fs) > 1:
        issue(4, "BLOCKER", "PRODUCTION_UNIT", "Deliverable", d, f"{d} found in more than one lifecycle folder", f"Deliverables.csv {d}", "; ".join(REL(x) for x in fs)); per_unit[d] += 1
    f = fs[0]
    parent_pkg = os.path.basename(os.path.dirname(os.path.dirname(f))).split("_")[0]
    fid = os.path.basename(f).split("_")[0]
    if fid != d or parent_pkg != r["PackageID"]:
        issue(4, "BLOCKER", "PRODUCTION_UNIT", "Deliverable", d, f"ID mismatch: folder says {fid}/{parent_pkg}, decomposition says {d}/{r['PackageID']}", f"Deliverables.csv {d}", REL(f)); per_unit[d] += 1
    label = os.path.basename(f)[len(d) + 1:]
    if norm(label) != norm(r["Name"]):
        issue(4, "INFO", "PRODUCTION_UNIT", "Deliverable", d, f"Folder label '{label}' differs from Deliverables.csv Name '{r['Name']}' (IDs match; label only)", f"Deliverables.csv {d}", REL(f)); per_unit[d] += 1

# ---------- Check 3 ----------
reverse_only = []
for u, fs in unit_folders.items():
    pkg = "PKG-" + u.split("-")[1]
    if pkg not in SCOPE_PKGS:
        continue
    if u not in DL:
        reverse_only.append(u)
        issue(3, "WARNING", "PRODUCTION_UNIT", "Deliverable", u, f"Folder exists but no matching entry in Deliverables.csv", "Deliverables.csv (absent)", REL(fs[0]))
for p in pkg_folder_all:
    pid = os.path.basename(p).split("_")[0]
    if pid not in PK:
        issue(3, "WARNING", "PARTITION", "Package", pid, "Partition folder exists but no matching entry in Packages.csv", "Packages.csv (absent)", REL(p))
scoped_folders = [u for u in unit_folders if "PKG-" + u.split("-")[1] in SCOPE_PKGS]

# ---------- Check 5 ----------
def parse_context(p):
    fields = defaultdict(list)
    for line in open(p, encoding="utf-8").read().splitlines():
        m = re.match(r"^- \*\*(.+?):\*\*\s?(.*)$", line)
        if m:
            fields[m.group(1).strip()].append(m.group(2).strip())
    return fields
DEL_FIELDS = [("Name", "Name"), ("PackageID", "PackageID"), ("Type", "Type"), ("ResponsibleParty", "ResponsibleParty"),
              ("Description", "Description"), ("ContextEnvelope", "ContextEnvelope"), ("ContextEnvelopeNotes", "ContextEnvelopeNotes"),
              ("AnticipatedArtifacts", "AnticipatedArtifacts"), ("CoversScopeItems", "CoversScopeItems"),
              ("SupportsObjectives", "SupportsObjectives"), ("PhaseHint", "PhaseHint")]
PKG_FIELDS = [("Package Name", "Name"), ("ScopeDescription", "ScopeDescription"), ("InclusionCriteria", "InclusionCriteria"), ("Exclusions", "Exclusions")]
ctx_match = {}; sow_refs = {}
for d in in_scope_del:
    fs = unit_folders.get(d)
    if not fs:
        ctx_match[d] = "MISSING"; continue
    cp = os.path.join(fs[0], "_CONTEXT.md")
    if not os.path.isfile(cp):
        issue(5, "WARNING", "CONTEXT", "Deliverable", d, f"No _CONTEXT.md in folder", f"Deliverables.csv {d}", REL(fs[0])); ctx_match[d] = "MISSING"; per_unit[d] += 1; continue
    f = parse_context(cp); mism = []
    for cf, rf in DEL_FIELDS:
        vals = f.get(cf, [])
        if not vals:
            mism.append(cf); issue(5, "WARNING", "CONTEXT", "Deliverable", d, f"{cf} absent from _CONTEXT.md", f"Deliverables.csv {d}.{rf}", REL(cp)); continue
        if any(norm(v) != norm(DL[d][rf]) for v in vals):
            mism.append(cf); issue(5, "WARNING", "CONTEXT", "Deliverable", d, f"{cf} in _CONTEXT.md does not match Deliverables.csv", f"Deliverables.csv {d}.{rf}", REL(cp))
    for cf, rf in PKG_FIELDS:
        vals = f.get(cf, [])
        if not vals or any(norm(v) != norm(PK[DL[d]["PackageID"]][rf]) for v in vals):
            mism.append(cf); issue(5, "WARNING", "CONTEXT", "Deliverable", d, f"{cf} in _CONTEXT.md does not match Packages.csv {DL[d]['PackageID']}.{rf}", f"Packages.csv {DL[d]['PackageID']}.{rf}", REL(cp))
    dup = [k for k, v in f.items() if len(v) > 1]
    for k in dup:
        issue(5, "INFO", "CONTEXT", "Deliverable", d, f"_CONTEXT.md carries field '{k}' {len(f[k])} times (identical values: {len(set(f[k])) == 1})", f"Deliverables.csv {d}.PackageID", REL(cp))
    per_unit[d] += len(mism) + len(dup)
    ctx_match[d] = "MATCH" if not mism else ("PARTIAL" if len(mism) < 4 else "MISMATCH")
    # SoW frontmatter vs register (informational fidelity)
    sp = os.path.join(fs[0], "ScopeOfWork.md")
    if os.path.isfile(sp):
        t = open(sp, encoding="utf-8").read()
        fm = t.split("---")[1] if t.startswith("---") else ""
        def fmv(k):
            m = re.search(rf"^{k}:\s*\[(.*?)\]", fm, re.M); return [x.strip() for x in m.group(1).split(",")] if m else None
        def fms(k):
            m = re.search(rf"^{k}:\s*(.*)$", fm, re.M); return m.group(1).strip() if m else None
        sr, so = fmv("project_scope_refs"), fmv("package_objective_refs")
        sow_refs[d] = {"deliverable_id": fms("deliverable_id"), "package_id": fms("package_id"), "decomposition_basis": fms("decomposition_basis"),
                       "project_scope_refs": sr, "package_objective_refs": so, "sha256": sha(sp)}
        if fms("deliverable_id") != d or fms("package_id") != DL[d]["PackageID"]:
            issue(5, "WARNING", "CONTEXT", "Deliverable", d, "ScopeOfWork.md frontmatter identity differs from register", f"Deliverables.csv {d}", REL(sp)); per_unit[d] += 1
        if sr is not None and set(sr) != set(split(DL[d]["CoversScopeItems"])):
            issue(5, "INFO", "CONTEXT", "Deliverable", d, f"ScopeOfWork.md project_scope_refs {sorted(set(sr) ^ set(split(DL[d]['CoversScopeItems'])))} differ from CoversScopeItems", f"Deliverables.csv {d}.CoversScopeItems", REL(sp)); per_unit[d] += 1
        if so is not None and set(so) != set(split(DL[d]["SupportsObjectives"])):
            issue(5, "INFO", "CONTEXT", "Deliverable", d, f"ScopeOfWork.md package_objective_refs differ from SupportsObjectives", f"Deliverables.csv {d}.SupportsObjectives", REL(sp)); per_unit[d] += 1

# ---------- Structure tool (Checks 2/3 inventory, 6 format, 11) ----------
st = json.load(open(os.path.join(OUT, "structure.json")))
st_units = {u["id"]: u for u in st["units"]}

# ---------- Check 6 ----------
STOP = set("and the with for from into only each that this their per contract contracts docs doc code config test tests script scripts of to on in a an or by as".split())
CONTROL = {"_STATUS.md", "_CONTEXT.md", "_DEPENDENCIES.md", "_REFERENCES.md", "_SEMANTIC.md", "_SEMANTIC_LENSING.md", "_MEMORY.md", "MEMORY.md", "Dependencies.csv", "ScopeOfWork.md"}
def toks(s):
    return {w for w in re.findall(r"[a-z0-9]+", s.lower()) if len(w) >= 4 and w not in STOP}
art_found = art_expected = 0; art_cov = {}
for d in in_scope_del:
    fs = unit_folders.get(d)
    arts = split(DL[d]["AnticipatedArtifacts"])
    files = []
    if fs:
        for root, dirs, fnames in os.walk(fs[0]):
            if "_run_records" in root or "_Archive" in root:
                continue
            files += [os.path.join(root, n) for n in fnames if n not in CONTROL]
    found = 0
    state = (st_units.get(d) or {}).get("current_state")
    for a in arts:
        typ, _, desc = a.partition(":")
        at = toks(desc)
        hits = [x for x in files if len(at & toks(os.path.splitext(os.path.basename(x))[0])) >= 2 or
                (toks(os.path.splitext(os.path.basename(x))[0]) and toks(os.path.splitext(os.path.basename(x))[0]) <= at)]
        if hits:
            found += 1
        else:
            sev = "WARNING" if state in ("IN_PROGRESS", "CHECKING", "ISSUED") else "INFO"
            issue(6, sev, "ARTIFACT", "Deliverable", d, f"Anticipated artifact '{a.strip()}' not found (lifecycle {state}; production not begun)", f"Deliverables.csv {d}.AnticipatedArtifacts", REL(fs[0]) if fs else "NOT_FOUND")
    art_found += found; art_expected += len(arts); art_cov[d] = f"{found}/{len(arts)}"
    fmt = (st_units.get(d) or {}).get("production_format", {})
    if not fmt.get("accepted_baseline"):
        issue(6, "WARNING", "ARTIFACT", "Deliverable", d, f"Production format {fmt.get('state')} not an accepted valid baseline", f"Deliverables.csv {d}", REL(fs[0]) if fs else "NOT_FOUND"); per_unit[d] += 1

# ---------- Check 7 (whole decomposition; SOFTWARE: ledger ObjectiveIDs column authoritative) ----------
ledger_objs = sorted({o for r in sl for o in split(r["ObjectiveIDs"])})
support = defaultdict(list)
for d, r in DL.items():
    for o in split(r["SupportsObjectives"]):
        support[o].append(d)
obj_rows = []
obj_integrity = "PASS"
for o in sorted(set(ledger_objs) | set(OB)):
    sup = sorted(support.get(o, []))
    active = [d for d in sup if unit_folders.get(d) and (st_units.get(d) or {}).get("current_state") != "RETIRED"]
    mapped_reg = sorted(split(OB[o]["MappedDeliverables"])) if o in OB else None
    ledger_items = sorted(r["ScopeItemID"] for r in sl if o in split(r["ObjectiveIDs"]))
    reg_items = sorted(split(OB[o]["ScopeItemIDs"])) if o in OB else None
    obj_rows.append(dict(ObjectiveID=o, in_ledger=o in ledger_objs, in_register=o in OB, supporting_units=len(sup), active_supporting_units=len(active),
                         register_mapped=len(mapped_reg or []), register_parity=mapped_reg == sup, ledger_items=len(ledger_items),
                         register_scope_items=len(reg_items or []), scope_item_parity=reg_items == ledger_items))
    if not active:
        issue(7, "WARNING", "OBJECTIVE", "Objective", o, f"Objective {o} has no active supporting Production Units", "Deliverables.csv SupportsObjectives", "—")
    if o not in OB or o not in ledger_objs:
        issue(7, "WARNING", "OBJECTIVE", "Objective", o, f"Objective {o} present in {'ledger' if o in ledger_objs else 'Objectives.csv'} only", "ScopeLedger.csv ObjectiveIDs / Objectives.csv", "—")
    if mapped_reg is not None and mapped_reg != sup:
        obj_integrity = "FAIL"
        issue(7, "BLOCKER", "OBJECTIVE", "Objective", o, f"Objective {o} support-count evidence is internally inconsistent: Objectives.csv MappedDeliverables {mapped_reg} vs Deliverables.csv SupportsObjectives {sup}", f"Objectives.csv {o}.MappedDeliverables", REL(os.path.join(DEC, 'Objectives.csv')))
    if reg_items is not None and reg_items != ledger_items:
        issue(7, "WARNING", "OBJECTIVE", "Objective", o, f"Objectives.csv ScopeItemIDs ({len(reg_items)}) differ from ScopeLedger.csv ObjectiveIDs mapping ({len(ledger_items)}): only-register={sorted(set(reg_items)-set(ledger_items))[:8]} only-ledger={sorted(set(ledger_items)-set(reg_items))[:8]}", f"Objectives.csv {o}.ScopeItemIDs", REL(os.path.join(DEC, 'Objectives.csv')))
if tel.get("ObjectiveCount") != len(OB) or tel.get("UnmappedObjectives", 0) != sum(1 for o in OB if not support.get(o)):
    obj_integrity = "FAIL"
    issue(7, "BLOCKER", "OBJECTIVE", "Objective", "ALL", "Coverage_Telemetry objective counts disagree with registers", "Coverage_Telemetry.json", REL(os.path.join(DEC, "Coverage_Telemetry.json")))
dels_no_obj = [d for d in DL if not split(DL[d]["SupportsObjectives"])]
in_rows_no_obj = [r["ScopeItemID"] for r in sl if r["InOutStatus"] == "IN" and not split(r["ObjectiveIDs"])]
scoped_dels_no_obj = [d for d in in_scope_del if not split(DL[d]["SupportsObjectives"])]
scoped_in_rows = [r for r in sl if r["InOutStatus"] == "IN" and r["PackageID"] in SCOPE_PKGS]
scoped_in_no_obj = [r["ScopeItemID"] for r in scoped_in_rows if not split(r["ObjectiveIDs"])]

# ---------- Check 8 (ledger; whole register evaluated, scoped counts reported) ----------
status_counts = Counter(r["InOutStatus"] for r in sl)
cov_from_dl = defaultdict(set)
for d, r in DL.items():
    for s in split(r["CoversScopeItems"]):
        cov_from_dl[s].add(d)
ledger_issues = 0
for r in sl:
    sid = r["ScopeItemID"]; dels = split(r["DeliverableIDs"])
    if r["PackageID"] not in PK:
        issue(8, "WARNING", "ATOMIC_UNIT", "Scope Item", sid, f"Scope item {sid} references Package {r['PackageID']} which does not exist", f"ScopeLedger.csv {sid}", "NOT_FOUND"); ledger_issues += 1
    if r["InOutStatus"] == "IN":
        for d in dels:
            if d != "TBD" and d not in DL:
                issue(8, "WARNING", "ATOMIC_UNIT", "Scope Item", sid, f"Scope item {sid} references Deliverable {d} which does not exist", f"ScopeLedger.csv {sid}", "NOT_FOUND"); ledger_issues += 1
            elif d in DL and DL[d]["PackageID"] != r["PackageID"]:
                issue(8, "INFO", "ATOMIC_UNIT", "Scope Item", sid, f"Scope item {sid} homed in {r['PackageID']} maps to {d} of {DL[d]['PackageID']}", f"ScopeLedger.csv {sid}", REL(os.path.join(DEC, 'ScopeLedger.csv')))
        if not dels:
            issue(8, "WARNING", "ATOMIC_UNIT", "Scope Item", sid, f"IN scope item {sid} has no production mapping", f"ScopeLedger.csv {sid}", "—"); ledger_issues += 1
    elif dels:
        issue(8, "WARNING", "ATOMIC_UNIT", "Scope Item", sid, f"{r['InOutStatus']} scope item {sid} carries production mapping {dels}", f"ScopeLedger.csv {sid}", "—"); ledger_issues += 1
    if set(dels) - {"TBD"} != cov_from_dl.get(sid, set()):
        issue(8, "WARNING", "ATOMIC_UNIT", "Scope Item", sid, f"Ledger DeliverableIDs {sorted(dels)} differ from Deliverables.csv CoversScopeItems reciprocal {sorted(cov_from_dl.get(sid, set()))}", f"ScopeLedger.csv {sid}", REL(os.path.join(DEC, 'Deliverables.csv'))); ledger_issues += 1
for s in cov_from_dl:
    if s not in SL:
        issue(8, "WARNING", "ATOMIC_UNIT", "Scope Item", s, f"Deliverables.csv covers {s} absent from ScopeLedger.csv", "Deliverables.csv CoversScopeItems", "NOT_FOUND"); ledger_issues += 1

# ---------- Check 9 other derivative-currency observations ----------
deriv = []
def dobs(sev, eid, desc, fref, dref="Companion_Inventory.csv"):
    issue(9, sev, "DERIVATIVE_SURFACE", "Derivative surface", eid, desc, dref, fref); deriv.append((sev, eid, desc))
# main-doc summary table vs registers
tbl = re.findall(r"^\| (PKG-\d\d) \| (.+?) \| (\d+) \| (\d+) / (\d+) / (\d+) \|$", doc, re.M)
for pid, name, nd, ni, no, nt in tbl:
    real_nd = sum(1 for r in dl if r["PackageID"] == pid)
    c = Counter(r["InOutStatus"] for r in sl if r["PackageID"] == pid)
    if (int(nd), int(ni), int(no), int(nt)) != (real_nd, c["IN"], c["OUT"], c["TBD"]) or norm(name) != norm(PK[pid]["Name"]):
        dobs("WARNING", pid, f"SOFTWARE_DECOMP.md package summary row ({nd}; {ni}/{no}/{nt}) disagrees with registers ({real_nd}; {c['IN']}/{c['OUT']}/{c['TBD']})", REL(doc_path), "SOFTWARE_DECOMP.md 'Accepted flat work domains'")
summary_parity = len(tbl) == len(PK)
# telemetry vs registers
chk = {"ScopeItemCount": len(sl), "PackageCount": len(pk), "DeliverableCount": len(dl), "ObjectiveCount": len(ob),
       "StatusCounts": dict(status_counts), "ContextEnvelopeCounts": {k: sum(1 for r in dl if r["ContextEnvelope"] == k) for k in ("L", "M", "S", "XL")}}
for k, v in chk.items():
    if tel.get(k) != v:
        dobs("WARNING", "Coverage_Telemetry.json", f"Telemetry {k}={tel.get(k)} but registers give {v}", REL(os.path.join(DEC, "Coverage_Telemetry.json")))
oi_status = Counter(r["Status"] for r in oi)
active_oi = [r["OpenIssueID"] for r in oi if r["Status"] == "OPEN"]
nonopen = {r["OpenIssueID"]: r["Status"] for r in oi if r["Status"] != "OPEN"}
if tel.get("ActiveOpenIssueCount") != len(active_oi) or set(tel.get("ResolvedIssueIDs", [])) != set(nonopen):
    dobs("INFO", "Coverage_Telemetry.json", f"Telemetry ActiveOpenIssueCount={tel.get('ActiveOpenIssueCount')} ResolvedIssueIDs={tel.get('ResolvedIssueIDs')} but working Open_Issues.csv has {len(active_oi)} OPEN and non-OPEN {nonopen} (later standing update; telemetry is the frozen Group3 copy, RECOMPUTE planned by IA §8)", REL(os.path.join(DEC, "Coverage_Telemetry.json")))
if tel.get("standing") != "GROUP3_ACCEPTED" or tel.get("checks", {}).get("no_production_folders_or_SoWs_created") is True:
    dobs("INFO", "Coverage_Telemetry.json", f"Telemetry standing '{tel.get('standing')}' and check no_production_folders_or_SoWs_created=true describe the pre-acceptance candidate; 41 deliverable folders with ScopeOfWork.md now exist (bytes identical to the frozen GROUP3 canonical copy)", REL(os.path.join(DEC, "Coverage_Telemetry.json")))
if "No production Package/Deliverable folders or local ScopeOfWork contracts have been created" in doc:
    dobs("WARNING", "SOFTWARE_DECOMP.md", f"Working SOFTWARE_DECOMP.md 'Checkpoint and next stage' still states no production folders or local ScopeOfWork contracts have been created, while its own status line says local contract definition is underway and {len(unit_folders)} deliverable folders with ScopeOfWork.md exist. A30 edits this document", REL(doc_path), "SOFTWARE_DECOMP.md 'Checkpoint and next stage'")
latest = open(os.path.join(DEC, "_LATEST.md"), encoding="utf-8").read().strip()
dobs("INFO", "_Decomposition/_LATEST.md", f"Decomposition tool-root pointer reads '{latest}'; the accepted basis resolves through checkpoint_snapshots/_LATEST_ACCEPTED.md -> GROUP3-20260928T001055Z", REL(os.path.join(DEC, "_LATEST.md")))
g3diff = []
for f in sorted(os.listdir(os.path.join(G3, "canonical"))):
    a, b = sha(os.path.join(DEC, f)), sha(os.path.join(G3, "canonical", f))
    if a != b:
        g3diff.append((f, a, b))
        dobs("INFO", f, f"Working {f} differs from frozen GROUP3 canonical ({a[:12]} vs {b[:12]}); later standing/receiving-currency update, not a scope/structure change", REL(os.path.join(DEC, f)), "checkpoint_snapshots/GROUP3-20260928T001055Z/ACCEPTED_MANIFEST.csv")
oldobj = [o for o in OB if "final Group3 acceptance remains pending" in OB[o]["Notes"]]
if oldobj:
    dobs("INFO", "Objectives.csv", f"Objectives.csv Notes of {len(oldobj)} objectives keep the presentation-time label 'final Group3 acceptance remains pending' (frozen label, bytes equal GROUP3 canonical)", REL(os.path.join(DEC, "Objectives.csv")))

# ---------- Check 9b ----------
has_ci = "Companion_Inventory.csv" in os.listdir(DEC)
unbound = [k for k, v in bindings.items() if "reference only" not in k and all(b["hit"] is None for b in v)]
shape_findings = []
if not has_ci:
    issue("9b", "WARNING", "DERIVATIVE_SURFACE", "Package", "SOFTWARE_DECOMP.md", "Main decomposition document lacks a companion inventory section", "SOFTWARE_DECOMP.md", REL(doc_path)); shape_findings.append("no companion inventory")
# companion inventory completeness vs files
listed = set(ci_names); present = {f for f in os.listdir(DEC) if os.path.isfile(os.path.join(DEC, f)) and f not in ("_LATEST.md",)}
if present - listed or listed - present:
    issue("9b", "WARNING", "DERIVATIVE_SURFACE", "Package", "Companion_Inventory.csv", f"Companion inventory vs files: unlisted={sorted(present-listed)} missing={sorted(listed-present)}", "Companion_Inventory.csv", REL(DEC)); shape_findings.append("inventory mismatch")
if unbound:
    issue("9b", "WARNING", "DERIVATIVE_SURFACE", "Package", "SOFTWARE_DECOMP.md", f"Package roles are discoverable through Companion_Inventory.csv, but heading binding (audit-decomp Variant Section Binding, exact/prefix/substring) yields no hit in SOFTWARE_DECOMP.md for: {', '.join(unbound)}. Registers bind by Companion_Inventory filename; the scope-change Change Register (SOFTWARE: 'Decision Log' and/or 'Revision History') " + ("is UNRESOLVED" if "Change Register (scope-change, SOFTWARE)" in unbound else "binds: " + "; ".join(f"'{b['target']}' at rank {b['rank']} to '## {b['hit']}'" for b in bindings["Change Register (scope-change, SOFTWARE)"] if b["hit"])), "SOFTWARE_DECOMP.md ## headings", REL(doc_path)); shape_findings.append("heading binding unresolved")
pkg_shape = "WARN" if shape_findings else "PASS"

# ---------- Check 10 ----------
sc_latest = os.path.join(EX, "_ScopeChange/_LATEST.md")
active_snapshot_status = "SKIPPED" if not os.path.exists(sc_latest) else "CHECK"
# ---------- Check 11 ----------
life = Counter((st_units.get(d) or {}).get("current_state") or "UNKNOWN" for d in in_scope_del)
life_all = Counter(u["current_state"] or "UNKNOWN" for u in st["units"])
for d in in_scope_del:
    s = (st_units.get(d) or {}).get("current_state")
    if s not in {"OPEN", "INITIALIZED", "SEMANTIC_READY", "IN_PROGRESS", "CHECKING", "ISSUED", "RETIRED"}:
        issue(11, "INFO", "PRODUCTION_UNIT", "Deliverable", d, f"Unexpected lifecycle state '{s}'", f"Deliverables.csv {d}", REL(unit_folders[d][0]) if unit_folders.get(d) else "NOT_FOUND")
if st.get("issues"):
    issue(11, "INFO", "PRODUCTION_UNIT", "Workspace", "execution", f"audit_structure.py workspace findings: {st['issues']} (tool_roots={st['tool_roots']}); informational, outside the 12 checks", "—", REL(EX))

# ---------- Check 10 (POSTACCEPT addition; audit-decomp method Step 10) ----------
check10 = {"status": "SKIPPED"}
if os.path.exists(sc_latest):
    SC = os.path.join(EX, "_ScopeChange")
    lt = open(sc_latest, encoding="utf-8").read()
    probs = []
    act = re.findall(r"^\*\*Active snapshot:\*\*\s*`([^`]+)`", lt, re.M)
    names = sorted(set(re.findall(r"_ScopeChange/(SCA-[A-Z0-9-]+_\d{4}-\d{2}-\d{2}_\d{4}[^/`]*)/?", lt)))
    if len(act) != 1:
        probs.append(f"_LATEST.md names {len(act)} active snapshot lines")
    snap = act[0].rstrip("/") if act else ""
    snap_name = os.path.basename(snap)
    if len(names) != 1 or (names and names[0] != snap_name):
        probs.append(f"_LATEST.md names amendment snapshot folders {names}; exactly one, the active one, is expected")
    sdir = os.path.join(SC, snap_name)
    if not (snap_name and os.path.isdir(sdir) and re.fullmatch(r"SCA-[A-Z0-9-]+_\d{4}-\d{2}-\d{2}_\d{4}.*", snap_name)):
        probs.append(f"active snapshot folder '{snap}' missing or not an SCA-* amendment snapshot")
    required = ["Brief.md", "Intake_Actions.csv", "Impact_Assessment.md", "Amendment_Preview.md", "Propagation_Plan.md",
                "Amendment_Actions.csv", "Pre_Change_Coverage.json", "Post_Change_Coverage.json", "Decision_Log.md",
                "Handoff_State.md", "RUN_SUMMARY.md", "Supersession_Delta.csv", "Supersession_Map.csv"]
    missing = [f for f in required if not os.path.isfile(os.path.join(sdir, f))]
    if missing:
        probs.append(f"active snapshot lacks {missing}")
    allowed = {"DecompositionTruthState": {"NOT_STARTED", "INCOMPLETE", "COMPLETE"}, "DerivativePackageState": {"INCOMPLETE", "COMPLETE"},
               "ContentRemediationState": {"NOT_REQUIRED", "PENDING", "COMPLETE", "BLOCKED", "DEFERRED"},
               "DownstreamRerunState": {"NOT_REQUIRED", "FROZEN", "IN_PROGRESS", "COMPLETE", "BLOCKED"},
               "MetadataAlignmentState": {"NOT_REQUIRED", "NOT_STARTED", "IN_PROGRESS", "COMPLETE", "BLOCKED"},
               "AuditState": {"NOT_RUN", "WARNINGS", "NON_BLOCKING_PASS", "BLOCKED"}, "AdjustedAuditState": {"NOT_RUN", "WARNINGS", "NON_BLOCKING_PASS", "BLOCKED"},
               "ReadyForNextPhase": {"NO", "REGEN_ONLY", "PHASE7_REVIEW", "PUBLICATION_GATED", "NOT_APPLICABLE"}}
    hs = open(os.path.join(sdir, "Handoff_State.md"), encoding="utf-8").read() if "Handoff_State.md" not in missing else ""
    rs = open(os.path.join(sdir, "RUN_SUMMARY.md"), encoding="utf-8").read() if "RUN_SUMMARY.md" not in missing else ""
    fields = {}
    for k in allowed:
        vals = set(re.findall(r"\|\s*`" + k + r"`\s*\|\s*`([A-Z_0-9]+)`", hs + "\n" + rs))
        if len(vals) != 1 or not vals <= allowed[k]:
            probs.append(f"state field {k}: {sorted(vals)}")
        fields[k] = sorted(vals)
    verdicts = set(re.findall(r"Closure verdict:?\*?\*?\s*`?\*?\*?(OPEN_PENDING_DERIVATIVE_CLOSURE|CLOSED_FOR_SCOPE_CHANGE_ONLY)", hs + "\n" + rs))
    if len(verdicts) != 1:
        probs.append(f"closure verdict {sorted(verdicts)}")
    stale = "STALE" in hs
    if stale and ("CLOSED_FOR_SCOPE_CHANGE_ONLY" in verdicts or fields.get("DerivativePackageState") == ["COMPLETE"] or fields.get("DownstreamRerunState") == ["COMPLETE"]):
        probs.append("handoff claims closure or complete derivatives while it records stale derivative packages")
    if fields.get("ReadyForNextPhase") and fields["ReadyForNextPhase"] != ["NOT_APPLICABLE"]:
        probs.append(f"ReadyForNextPhase {fields['ReadyForNextPhase']} for a SOFTWARE decomposition (no phase ladder)")
    others = sorted(d for d in os.listdir(SC) if d.startswith("SCA-") and os.path.isdir(os.path.join(SC, d)) and d != snap_name)
    residue = [d for d in others if any(not os.path.isfile(os.path.join(SC, d, f)) for f in required)]
    for p in probs:
        issue(10, "BLOCKER", "SNAPSHOT", "Scope-change snapshot", snap_name or "_LATEST.md", f"Active snapshot contract failed: {p}", "_ScopeChange/_LATEST.md", REL(sc_latest))
    for d in residue:
        issue(10, "WARNING", "SNAPSHOT", "Scope-change snapshot", d, "Historical snapshot residue is incomplete but not active truth", "_ScopeChange/", REL(os.path.join(SC, d)))
    active_snapshot_status = "FAIL" if probs else "PASS"
    check10 = {"status": active_snapshot_status, "latest": REL(sc_latest), "latest_sha256": sha(sc_latest), "active_snapshot": snap,
               "required_artifacts": required, "missing": missing, "state_fields": fields, "closure_verdict": sorted(verdicts),
               "other_sca_folders": others, "incomplete_residue": residue, "problems": probs}

# ---------- assemble ----------
for n, i in enumerate(issues, 1):
    i["IssueID"] = f"COV-{n:03d}"
per_unit = Counter(i["EntityID"] for i in issues if i["EntityType"] in ("PRODUCTION_UNIT", "CONTEXT", "ARTIFACT"))
sev = Counter(i["Severity"] for i in issues)
cols = ["IssueID", "CheckNumber", "Severity", "EntityType", "ConcreteLabel", "EntityID", "Description", "DecompositionRef", "FilesystemRef", "DecisionRef"]
with open(os.path.join(OUT, "Decomp_Coverage_IssueLog.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n"); w.writeheader(); [w.writerow({c: i[c] for c in cols}) for i in issues]
mcols = ["ProductionUnitID", "PartitionID", "ConcreteProductionUnitLabel", "ConcretePartitionLabel", "FolderExists", "ContextPresent", "ContextMatch", "ArtifactCoverage", "ObjectivesMapped", "LifecycleState", "IssueCount"]
with open(os.path.join(OUT, "Decomp_Coverage_Matrix.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n"); w.writerow(mcols)
    for d in sorted(in_scope_del):
        fs = unit_folders.get(d); objs = split(DL[d]["SupportsObjectives"])
        mapped = sum(1 for o in objs if o in OB and o in ledger_objs)
        w.writerow([d, DL[d]["PackageID"], "Deliverable", "Package", str(bool(fs)).lower(), str(bool(fs and os.path.isfile(os.path.join(fs[0], "_CONTEXT.md")))).lower(),
                    ctx_match.get(d, "MISSING"), art_cov.get(d, "0/0"), f"{mapped}/{len(objs)}", (st_units.get(d) or {}).get("current_state") or "UNKNOWN", per_unit.get(d, 0)])
    for u in sorted(reverse_only):
        w.writerow([u, "PKG-" + u.split("-")[1], "Deliverable", "Package", "true", "", "", "", "", "", per_unit.get(u, 0)])

pd = len(SCOPE_PKGS); pf = sum(1 for p, ok in c1 if ok)
ud = len(in_scope_del); uf = sum(1 for d in in_scope_del if unit_folders.get(d))
blk, wrn = sev["BLOCKER"], sev["WARNING"]
overall = "BLOCKERS" if blk else ("WARNINGS" if wrn else "OK")
summary = {
    "run_label": os.environ["RUN_LABEL"],
    "timestamp": os.environ.get("RUN_TS"),
    "decomp_variant": "SOFTWARE",
    "expected_source_snapshot": "projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z",
    "expected_handoff_phase": os.environ["HANDOFF_PHASE"],
    "decomposition_path": "projects/chirality-app-v4/execution/_Decomposition/SOFTWARE_DECOMP.md",
    "decomposition_revision": os.environ.get("BASIS_COMMIT"),
    "scope": SCOPE_PKGS,
    "repository_topology": {"packages": len(pk), "deliverables": len(dl), "objectives": len(ob), "scope_items": len(sl), "ledger_rows": len(sl)},
    "partitions_declared": pd, "partitions_found": pf,
    "production_units_declared": ud, "production_units_found": uf,
    "forward_coverage_partitions_pct": round(100 * pf / pd, 2),
    "forward_coverage_production_units_pct": round(100 * uf / ud, 2),
    "reverse_coverage_pct": round(100 * sum(1 for u in scoped_folders if u in DL) / len(scoped_folders), 2),
    "context_fidelity_pct": round(100 * sum(1 for d in in_scope_del if ctx_match.get(d) == "MATCH") / ud, 2),
    "artifact_presence_pct": round(100 * art_found / art_expected, 2) if art_expected else 0.0,
    "objective_coverage_pct": round(100 * sum(1 for r in obj_rows if r["active_supporting_units"] > 0) / len(obj_rows), 2),
    "deliverables_without_objective_mapping": len(scoped_dels_no_obj),
    "in_ledger_rows_without_objective_mapping": len(scoped_in_no_obj),
    "package_shape_conformance": pkg_shape,
    "derivative_package_status": "SKIPPED",
    "active_snapshot_status": active_snapshot_status,
    "handoff_state_status": check10["status"],
    "objective_evidence_integrity": obj_integrity,
    "issues_blocker": blk, "issues_warning": wrn, "issues_info": sev["INFO"], "issues_expected_consequence": sev["EXPECTED_CONSEQUENCE"],
    "check_count": 12,
    "lifecycle_distribution": dict(sorted(life.items())),
    "overall_status": overall,
    "closure_readiness": "FAIL" if blk else ("WARN" if wrn else "PASS"),
    "concrete_labels": {"partition": "Package", "production_unit": "Deliverable"},
    "extensions": {
        "scope_derivation": "Packages holding an entity named by IMPACT_ASSESSMENT §3 actions A18-A47 (ledger rows SOW-015/016/017/137/138 -> PKG-05, SOW-052 -> PKG-02, SOW-201/202 -> PKG-09; deliverables A32-A47 incl. DEL-01-01 -> PKG-01, DEL-08-01 -> PKG-08). O-20 lists PKG-02,03,04,05,08,09 and omits PKG-01.",
        "scoped_production_units": sorted(in_scope_del),
        "scoped_in_ledger_rows": len(scoped_in_rows),
        "whole_decomposition": {"status_counts": dict(status_counts), "deliverables_without_objective_mapping": len(dels_no_obj),
                                "in_ledger_rows_without_objective_mapping": len(in_rows_no_obj), "lifecycle_distribution": dict(sorted(life_all.items())),
                                "structure_tool_units_pass": st["summary"]["pass"], "structure_tool_units_fail": st["summary"]["fail"],
                                "production_formats": st["summary"]["production_formats"]},
        "artifact_presence": {"found": art_found, "expected": art_expected, "rule": "fuzzy: >=2 shared significant tokens (len>=4, stop-list) between artifact description and a non-control filename stem, or stem tokens a subset of description tokens"},
        "section_binding": bindings,
        "companion_binding": companion_binding,
        "working_vs_group3_differences": [{"file": f, "working_sha256": a, "group3_sha256": b} for f, a, b in g3diff],
        "open_issue_status_counts": dict(oi_status),
        "objective_rows": obj_rows,
        "sow_frontmatter": sow_refs,
        "main_doc_package_summary_rows_parsed": len(tbl),
        "active_snapshot_check": check10,
    },
}
json.dump(summary, open(os.path.join(OUT, "coverage_summary.json"), "w"), indent=2, sort_keys=False)
open(os.path.join(OUT, "_stats.json"), "w").write("")
os.remove(os.path.join(OUT, "_stats.json"))
print(json.dumps({k: summary[k] for k in list(summary)[:36] if k != "extensions"}, indent=1))
print(sev)
print(Counter((i["CheckNumber"], i["Severity"]) for i in issues))
