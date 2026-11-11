"""PKG-v0.2 identity and terms rules a schema cannot express (PK-R1 to PK-R9).

Used by the static distribution value model and check. Call after schema
validation; these inspect declared facts, not their truth.
"""
import json
from pathlib import Path

from jsonschema import Draft202012Validator  # noqa: F401  (the static check builds its validators from this module)

SCHEMAS = Path(__file__).resolve().parent / "schemas"
SUPPLIER_TEAM = "2DC432GLL2"  # observed signer of every Mach-O at 0.158.0 and 0.160.0


def load(name):
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


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


def terms_violations(t):
    v = []
    rec = t["recorded_by"].strip().lower()
    if t.get("response") and t["response"]["obtained_by"].strip().lower() == rec:
        v.append("PK-R4")
    d = t["distribution_decision"]
    if isinstance(d, dict) and d["decided_by"].strip().lower() == rec:
        v.append("PK-R4")
    return sorted(set(v))
