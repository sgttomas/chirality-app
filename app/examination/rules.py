"""Maintained EXP result and PKG identity rules, transcribed from pinned Design prototypes.

Call only after schema validation. These inspect declared facts, not their truth.
Source hashes and paths are in sources.json. Other EXP record kinds are out of scope.
"""
NATIVE = {"native_development", "native_packaged"}
SUPPLIER_TEAM = "2DC432GLL2"


def aggregate(parts):
    """EXP-R1: same order as CA W-R6, in EXP's labels."""
    outs = [p["outcome"] for p in parts]
    if "fail" in outs:
        return "fail"
    if "blocked" in outs:
        return "blocked"
    if outs and all(o == "pass" for o in outs):
        return "pass"
    if all(o == "not-run" for o in outs):
        return "not-run"
    return "inconclusive"


def rule_violations(rec):
    v = []
    # EXP-R1 aggregation over the applicable parts (R23-19); a declared
    # not-applicable part is listed apart and never also run
    if rec.get("parts"):
        if aggregate(rec["parts"]) != rec["outcome"]:
            v.append("EXP-R1")
    na = {p["part"] for p in rec.get("parts_not_applicable", [])}
    if na & {p["part"] for p in rec.get("parts", [])}:
        v.append("EXP-R1")
    # EXP-R3 only a candidate-basis record stands for a scenario (V4-EXM-nn), whatever its outcome
    if rec["case"].get("scenario") and rec["run_basis"] != "candidate" and rec["outcome"] != "not-run":
        v.append("EXP-R3")
    # EXP-R4 a part or record needing native evidence cannot pass on browser/replay evidence only
    units = rec.get("parts") or []
    for u in units:
        if u.get("needs_native") and u["outcome"] == "pass":
            routes = {e.get("route", rec["configuration"]["route"]["kind"]) for e in u.get("evidence", [])}
            if not routes & NATIVE:
                v.append("EXP-R4")
                break
    # EXP-R5 every cited act names an actor other than its recorder
    for a in rec.get("acts_cited", []):
        if a["actor"].strip().lower() == a["recorder"].strip().lower():
            v.append("EXP-R5")
            break
    return v


def identity_violations(r):
    v = []
    c = r["codex"]
    opt = r["signing"]["option"]
    if opt.startswith("B"):
        same_tree = c["published"]["manifest_sha256"] == c["packaged"]["manifest_sha256"]
        same_files = all(e["sha256_published"] == e["sha256_packaged"] for e in c["executables"])
        supplier_signed = all(e["signature"]["team"] == SUPPLIER_TEAM and e["signature"]["hardened_runtime"]
                              and e["signature"]["timestamp"]
                              and e["signature"]["authority"].startswith("Developer ID Application:")
                              and e["signature"]["authority"].endswith(f"({SUPPLIER_TEAM})")
                              for e in c["executables"])
        fp1_ok = all(r.get("first_package_checks", {}).get(k, {}).get("outcome") != "fail" for k in ("fp1a", "fp1b"))
        if not (same_tree and same_files and supplier_signed and fp1_ok):
            v.append("PK-R1")
    else:
        app_team = r["app"].get("signature", {}).get("team")
        for e in c["executables"]:
            s = e["signature"]
            if (sorted(s["entitlements"]) != sorted(e.get("supplier_entitlements", []))
                    or not s["hardened_runtime"] or not s["timestamp"] or s["team"] != app_team
                    or not s["authority"].startswith("Developer ID Application:")):
                v.append("PK-R2")
                break
        if sorted(r["signing"].get("configuration_space_tried", [])) != ["CS-1", "CS-2", "CS-3", "CS-4"]:
            v.append("PK-R7")
    # PK-R6 every Mach-O of the packaged tree is listed
    if len(c["executables"]) != c["packaged"]["macho_files"] or len({e["path"] for e in c["executables"]}) != len(c["executables"]):
        v.append("PK-R6")
    # PK-R9 option B is not relied on until FP-1(a), FP-1(b) and FP-3 pass (PKG §3)
    if opt.startswith("B") and any(r.get("first_package_checks", {}).get(k, {}).get("outcome") != "pass"
                                   for k in ("fp1a", "fp1b", "fp3")) \
            and "option B not yet relied on: FP-1/FP-3 not passed" not in r.get("limits", []):
        v.append("PK-R9")
    # PK-R8 complete only with no missing bundle item
    if r.get("complete") and any(b.get("state") == "missing" for b in r["bundle_contents"]):
        v.append("PK-R8")
    actors = {r["signing"]["performed_by"].strip().lower()}
    if r["notarisation"].get("submitted_by"):
        actors.add(r["notarisation"]["submitted_by"].strip().lower())
    if r["signing"]["recorded_by"].strip().lower() in actors:
        v.append("PK-R3")
    g = r["gatekeeper"]
    if g.get("assessed") and "Notarized" in g.get("verdict", "") and "Unnotarized" not in g.get("verdict", "") \
            and r["notarisation"]["state"] != "accepted":
        v.append("PK-R5")
    return v
