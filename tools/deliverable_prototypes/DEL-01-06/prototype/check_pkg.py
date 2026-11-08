#!/usr/bin/env python3
"""DEL-01-06 PKG-v0.2 design prototype: checks the two PROPOSED schemas, their
example sets and the rules PK-R1...PK-R9 a schema cannot express; checks
read_tree.py's comparison on small synthetic trees (links, directory links,
modes) built in a temporary folder under $TMPDIR and removed afterwards.
With --tree <vendor-tree> it also runs FP-0 of PKG §7 on a published Codex
tree (read only: codesign -d and sha256; nothing in it is executed or
written).

Not product code. A pass shows the rules run as written on illustrative
records; it passes no VER criterion (PKG §11). Needs Python 3 and the
`jsonschema` package (Draft 2020-12).

    python3 check_pkg.py [--tree <codex vendor tree>]
"""
import json
import os
import shutil
import sys
import tempfile

from jsonschema import Draft202012Validator

HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import read_tree  # noqa: E402

SUPPLIER_TEAM = "2DC432GLL2"  # observed signer of every Mach-O at 0.158.0 and 0.160.0 (PKG §2.2)
RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))


def load(n):
    with open(os.path.join(DESIGN, n), encoding="utf-8") as f:
        return json.load(f)


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


def run(prefix, schema, rules):
    s = load(schema)
    Draft202012Validator.check_schema(s)
    val = Draft202012Validator(s)
    check(f"SCHEMA {schema} is valid 2020-12", True)
    for r in load(f"{prefix}.valid.examples.json"):
        errs = list(val.iter_errors(r))
        check(f"VALID {r['record_id']}", not errs, "; ".join(e.message[:120] for e in errs[:2]))
        check(f"RULES {r['record_id']} none violated", not rules(r), str(rules(r)))
    for i in load(f"{prefix}.invalid.examples.json"):
        check(f"INVALID {i['record']['record_id']} ({i['why']})", list(val.iter_errors(i["record"])))
    for i in load(f"{prefix}.rule-violations.examples.json"):
        errs = list(val.iter_errors(i["record"]))
        check(f"RULE-SCHEMA {i['record']['record_id']} schema-valid", not errs, "; ".join(e.message[:120] for e in errs[:2]))
        got = rules(i["record"])
        check(f"RULES {i['record']['record_id']} {i['rule']} detected", i["rule"] in got, str(got))


def fp0(tree_dir):
    """FP-0 (PKG §7): the published tree meets option B's preconditions."""
    t = read_tree.read(tree_dir)
    m = [r for r in t if "macho" in r]
    nf = sum(1 for r in t if r["kind"] == "file")
    nd = sum(1 for r in t if r["kind"] == "dir")
    check(f"FP-0 published tree read ({nf} files, {nd} directories, {len(m)} Mach-O)", m)
    check("FP-0 every Mach-O signed by the supplier team", all(r["macho"]["team"] == SUPPLIER_TEAM for r in m),
          str({r["macho"]["team"] for r in m}))
    check("FP-0 every Mach-O's first Authority is the supplier's Developer ID Application",
          all((r["macho"]["authority"] or "").startswith("Developer ID Application:")
              and (r["macho"]["authority"] or "").endswith(f"({SUPPLIER_TEAM})") for r in m),
          str({r["macho"]["authority"] for r in m}))
    check("FP-0 every Mach-O hardened runtime and timestamped",
          all(r["macho"]["hardened_runtime"] and r["macho"]["timestamp"] for r in m))
    check("FP-0 no Mach-O carries get-task-allow",
          all("com.apple.security.get-task-allow" not in r["macho"]["entitlements"] for r in m))
    check("FP-0 no symbolic links (files or directories) in the tree", not any(r["kind"] == "symlink" for r in t))
    check("FP-0 manifest computed (PKG §5.2)", len(read_tree.manifest(t)) == 64, read_tree.manifest(t))


def tree_compare_cases():
    """RV2 P6-P8: read_tree's comparison sees link targets, directory links and modes."""
    d = tempfile.mkdtemp(dir=os.environ.get("TMPDIR"))
    try:
        def mk(name, target, dirlink=False):
            t = os.path.join(d, name)
            os.makedirs(os.path.join(t, "bin"))
            os.makedirs(os.path.join(t, "real"))
            with open(os.path.join(t, "bin", "f"), "w") as f:
                f.write("same")
            os.chmod(os.path.join(t, "bin", "f"), 0o755)
            os.symlink(target, os.path.join(t, "bin", "link"))
            if dirlink:
                os.symlink("real", os.path.join(t, "dirlink"))
            return t
        a, b = mk("a", "x1", dirlink=True), mk("b", "x2")
        res = read_tree.compare(read_tree.read(a, False), read_tree.read(b, False))
        check("TREE P6 differing file-link targets detected", "bin/link" in res["differing"], str(res))
        check("TREE P7 a directory link is recorded and detected",
              any(r["path"] == "dirlink" and r["kind"] == "symlink" for r in read_tree.read(a, False)) and "dirlink" in res["extra"],
              str(res))
        c = mk("c", "x2")
        os.chmod(os.path.join(c, "bin", "f"), 0o644)
        res2 = read_tree.compare(read_tree.read(c, False), read_tree.read(b, False))
        check("TREE P8 a stripped executable bit is detected", "bin/f" in res2["differing"], str(res2))
        res3 = read_tree.compare(read_tree.read(b, False), read_tree.read(mk("e", "x2"), False))
        check("TREE identical trees compare equal", res3["equal"], str(res3))
    finally:
        shutil.rmtree(d)


def main(argv):
    run("pkg.identity-record", "pkg.identity-record.schema.json", identity_violations)
    run("pkg.terms-record", "pkg.terms-record.schema.json", terms_violations)
    tree_compare_cases()
    if "--tree" in argv:
        fp0(argv[argv.index("--tree") + 1])
    fails = [r for r in RESULTS if not r[1]]
    for n, ok, d in RESULTS:
        print(f"{'PASS' if ok else 'FAIL'}  {n}" + (f"  -- {d}" if d and not ok else ""))
    print(f"TOTAL {len(RESULTS)}, FAIL {len(fails)}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
