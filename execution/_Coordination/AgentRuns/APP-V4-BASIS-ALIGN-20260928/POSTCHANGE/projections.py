#!/usr/bin/env python3
"""Read-only projections for the SCA-V4-001 group-3 package (node AK1). Writes only OUT/projections.json.

1. Acceptance-conditional edits (A07, A17a-c, D-15), simulated in memory with a placeholder date:
   does each still apply exactly once, does 'Decision Log' then bind (audit-decomp rule), and how many
   Consolidated_Coverage rows would take a new SourceLine/SHA256 on the post-acceptance recompute.
2. Coverage_Telemetry.json: the register-derivable fields recomputed from the candidate registers,
   compared with the file as it stands (the file itself is not written).
Usage: projections.py REPO OUT
"""
import csv, glob, hashlib, io, json, os, re, sys

REPO, OUT = sys.argv[1], sys.argv[2]
P = "projects/chirality-app-v4"
EX = f"{P}/execution"
DEC = f"{EX}/_Decomposition"
PK = f"{EX}/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/AMENDMENT_PACKET"
ba = open(os.path.join(REPO, PK, "BASIS_AMENDMENT.md"), encoding="utf-8").read()
DOCS = {"PRD.md": f"{P}/docs/PRD.md", "ARCHITECTURE.md": f"{P}/docs/ARCHITECTURE.md",
        "HOST_INTEGRATION.md": f"{P}/docs/HOST_INTEGRATION.md", "EXAMINATION.md": f"{P}/docs/EXAMINATION.md",
        "_Decomposition/SOFTWARE_DECOMP.md": f"{DEC}/SOFTWARE_DECOMP.md"}
FILL = {"{AMENDMENT_ID}": "SCA-V4-001", "{ACCEPT_DATE}": "YYYY-MM-DD", "{AMENDMENT_SNAPSHOT}": "SCA-V4-001_2026-09-28_2155"}
res = {"placeholders": FILL}

texts = {}
def rd(rel):
    if rel not in texts:
        texts[rel] = open(os.path.join(REPO, rel), encoding="utf-8").read()
    return texts[rel]

held = []
for s in re.split(r"^#### ", ba, flags=re.M)[1:]:
    eid = s.splitlines()[0].split(" ")[0]
    if eid not in ("A07", "A17a", "A17b", "A17c", "D-15"):
        continue
    tgt = DOCS[re.search(r"^Target: (\S+)", s, re.M).group(1)]
    b = re.findall(r"^```(old|new)\n(.*?)\n```$", s, flags=re.M | re.S)
    for i in range(0, len(b), 2):
        old, new = b[i][1], b[i + 1][1]
        for k, v in FILL.items():
            new = new.replace(k, v)
        c = rd(tgt).count(old)
        held.append({"edit": eid, "pair": i // 2 + 1, "target": tgt, "old_count_in_candidate": c})
        if c == 1:
            texts[tgt] = texts[tgt].replace(old, new)
res["held_edits"] = held

doc = texts[DOCS["_Decomposition/SOFTWARE_DECOMP.md"]]
headings = [l[3:].strip() for l in doc.splitlines() if l.startswith("## ")]
def nh(h):
    return re.sub(r"^\d+[A-Za-z]?\.\s+", "", h.strip()).strip().casefold()
def bind(t):
    t = nh(t); hs = [nh(h) for h in headings]
    for rank, pred in (("exact", lambda h: h == t), ("prefix", lambda h: h.startswith(t)), ("substring", lambda h: t in h)):
        hits = [headings[i] for i, h in enumerate(hs) if pred(h)]
        if hits:
            return {"rank": rank, "hit": hits[0], "hits": len(hits)}
    return {"rank": None, "hit": None, "hits": 0}
res["change_register_binding_after_D15"] = {"Decision Log": bind("Decision Log"), "Revision History": bind("Revision History")}

rows = list(csv.DictReader(open(os.path.join(REPO, DEC, "Consolidated_Coverage.csv"), encoding="utf-8", newline="")))
moved = {}
for r in rows:
    d = r["Document"]
    if d not in texts:
        continue
    L = texts[d].splitlines()
    pat = re.compile(r"^(- \*\*|\*\*|\| )" + re.escape(r["ConsolidatedRequirementID"]) + r"(?![0-9A-Za-z])")
    ln = [n + 1 for n, l in enumerate(L) if pat.search(l)][0]
    sha = hashlib.sha256(texts[d].encode()).hexdigest()
    m = moved.setdefault(d, {"rows": 0, "sha_changes": 0, "line_changes": 0})
    m["rows"] += 1
    m["sha_changes"] += sha != r["SHA256"]
    m["line_changes"] += str(ln) != r["SourceLine"]
res["consolidated_coverage_after_acceptance_conditional_edits"] = moved

# ---- telemetry: register-derivable fields ----
def rows_of(f):
    return list(csv.DictReader(open(os.path.join(REPO, DEC, f), encoding="utf-8-sig", newline="")))
sl, pk, dl, ob, oi = (rows_of(f) for f in ("ScopeLedger.csv", "Packages.csv", "Deliverables.csv", "Objectives.csv", "Open_Issues.csv"))
tel = json.load(open(os.path.join(REPO, DEC, "Coverage_Telemetry.json")))
split = lambda v: [x.strip() for x in (v or "").split(";") if x.strip()]
by_type = {}
for r in oi:
    if r["Status"] == "OPEN":
        by_type.setdefault(r["Type"], []).append(r["OpenIssueID"])
sow_folders = [p for p in glob.glob(os.path.join(REPO, EX, "PKG-*", "*_*", "DEL-*")) if os.path.isfile(os.path.join(p, "ScopeOfWork.md"))]
derived = {
    "ScopeItemCount": len(sl),
    "StatusCounts": {k: sum(1 for r in sl if r["InOutStatus"] == k) for k in ("IN", "OUT", "TBD")},
    "PackageCount": len(pk), "DeliverableCount": len(dl), "ObjectiveCount": len(ob),
    "UnassignedScopeItems": sum(1 for r in sl if not r["PackageID"]),
    "InScopeItemsWithoutDeliverableMapping": sum(1 for r in sl if r["InOutStatus"] == "IN" and not split(r["DeliverableIDs"])),
    "OutOrTbdWithDeliverableMapping": sum(1 for r in sl if r["InOutStatus"] != "IN" and split(r["DeliverableIDs"])),
    "UnmappedObjectives": sum(1 for o in ob if not any(o["ObjectiveID"] in split(d["SupportsObjectives"]) for d in dl)),
    "ContextEnvelopeCounts": {k: sum(1 for r in dl if r["ContextEnvelope"] == k) for k in ("L", "M", "S", "XL")},
    "OpenIssuesByType": {t: {"count": len(v), "ids": sorted(v)} for t, v in sorted(by_type.items())},
    "ActiveOpenIssueCount": sum(len(v) for v in by_type.values()),
    "ResolvedIssueIDs": sorted(r["OpenIssueID"] for r in oi if r["Status"] != "OPEN"),
    "checks.no_production_folders_or_SoWs_created": len(sow_folders) == 0,
    "inputs": [{"path": i["path"], "sha256": hashlib.sha256(open(os.path.join(REPO, i["path"]), "rb").read()).hexdigest()} for i in tel["inputs"]],
}
current = dict(tel)
current["checks.no_production_folders_or_SoWs_created"] = tel["checks"]["no_production_folders_or_SoWs_created"]
res["telemetry"] = {
    "file_sha256": hashlib.sha256(open(os.path.join(REPO, DEC, "Coverage_Telemetry.json"), "rb").read()).hexdigest(),
    "deliverable_folders_with_ScopeOfWork": len(sow_folders),
    "derived_fields": {k: {"current": current.get(k), "recomputed": v, "differs": current.get(k) != v} for k, v in derived.items()},
    "not_derivable_unchanged": {k: tel[k] for k in ("standing", "Revision", "Date") if k in tel},
}
json.dump(res, open(os.path.join(OUT, "projections.json"), "w"), indent=1, ensure_ascii=False)
print(json.dumps({"binding": res["change_register_binding_after_D15"], "held": [(h["edit"], h["old_count_in_candidate"]) for h in held],
                  "cc": moved, "tel_differs": [k for k, v in res["telemetry"]["derived_fields"].items() if v["differs"]]}, indent=1))
