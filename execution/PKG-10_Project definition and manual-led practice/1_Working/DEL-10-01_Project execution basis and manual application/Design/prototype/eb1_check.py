#!/usr/bin/env python3
"""EB-1 checks (DEL-10-01 EB-v0.1 §8, VER-002 and the input-set checks).

Design prototype, not product code. Read-only. Exit 0 only if every check passes.

  python3 eb1_check.py                 # pins, manifest schema, manifest hashes
  python3 eb1_check.py --verify-dir D  # also: a copied input folder D matches the manifest
  python3 eb1_check.py --post-dispatch RUN/RR-EB1/SUPPLIED.sha256
                                       # after a read: manifest drift is reported, not failed;
                                       # the supplied folder's record must equal the frozen manifest

Checks:
  P-1  every sha256 in EXECUTION_BASIS.md §3.1/§3.2 equals today's bytes
  P-2  §3.1 rows equal the bytes at Git ffb2b628…; §3.2 rows as the table states
       (coordinated-knowledge-work absent there)
  P-3  CURRENT_EXECUTION_BASIS.md contains all nine §3.1 hashes verbatim (manuals and methods)
  M-1  the manifest validates against DEL-09-11's rrm.input-set-manifest.schema.json (unchanged)
  M-2  every manifest item's sha256 equals today's bytes
  M-3  the account is in the set as project_file; the key, the survey and S2-E are not items
  M-4  every §3 path is a manifest item (the reader can recompute each pin)
  P-4  every sha256 in RUN/BASIS_BINDING.md equals today's bytes and the account's §3 row (R23-35)
  D-1  (--post-dispatch) SUPPLIED.sha256 lists every manifest item at the manifest's sha256,
       and the manifest itself at its frozen sha256
  V-1  (--verify-dir) each item exists under D with the manifest's sha256
"""
import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
DESIGN = HERE.parent
PIN_COMMIT = "ffb2b6289dde79a35f22f5d87256df0aa4d3289a"


def root() -> pathlib.Path:
    return pathlib.Path(subprocess.run(["git", "-C", str(HERE), "rev-parse", "--show-toplevel"],
                                       capture_output=True, text=True, check=True).stdout.strip())


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def git_blob(r: pathlib.Path, path: str):
    p = subprocess.run(["git", "-C", str(r), "show", f"{PIN_COMMIT}:{path}"], capture_output=True)
    return p.stdout if p.returncode == 0 else None


def pin_rows(text: str):
    """Rows of §3.1 and §3.2: (section, path, sha256)."""
    # Both tables have Path in column 2 and sha256 in column 3.
    rows, section = [], None
    for line in text.splitlines():
        if line.startswith("#"):
            section = "3.1" if line.startswith("### 3.1") else "3.2" if line.startswith("### 3.2") else None
            continue
        if section and line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 3:
                continue
            path = re.fullmatch(r"`([^`]+)`", cells[1])
            h = re.fullmatch(r"`([0-9a-f]{64})`", cells[2])
            if path and h:
                rows.append((section, path.group(1), h.group(1)))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default=str(DESIGN / "eb1" / "IS-EB1-1.input-set.json"))
    ap.add_argument("--verify-dir")
    ap.add_argument("--post-dispatch", help="SUPPLIED.sha256 written by the dispatcher")
    ap.add_argument("--frozen-manifest-sha", default="907709e54c77bb033ae4f8cceb1a5a28f856735cdec7f759a08b2849f4c761a8")
    a = ap.parse_args()
    r = root()
    fails, passes = [], 0

    def ok(cond, label):
        nonlocal passes
        if cond:
            passes += 1
        else:
            fails.append(label)

    account = (DESIGN / "EXECUTION_BASIS.md").read_text()
    rows = pin_rows(account)
    ok(len([x for x in rows if x[0] == "3.1"]) == 9, f"P-0 expected 9 rows in §3.1, got {len([x for x in rows if x[0]=='3.1'])}")
    ok(len([x for x in rows if x[0] == "3.2"]) == 5, f"P-0 expected 5 rows in §3.2, got {len([x for x in rows if x[0]=='3.2'])}")
    for section, path, h in rows:
        cur = sha((r / path).read_bytes())
        ok(cur == h, f"P-1 {path}: table {h[:16]} today {cur[:16]}")
        blob = git_blob(r, path)
        if path.endswith("coordinated-knowledge-work/WORKFLOW.md"):
            ok(blob is None or blob == b"", f"P-2 {path}: expected absent at {PIN_COMMIT[:10]}")
        else:
            ok(blob is not None and sha(blob) == h, f"P-2 {path}: differs at {PIN_COMMIT[:10]}")
    ceb = (r / "projects/chirality-app-v4/execution/_Coordination/CURRENT_EXECUTION_BASIS.md").read_text()
    for section, path, h in rows:
        if section == "3.1":  # the three manuals and the six definition-run methods (RV3 N4)
            ok(h in ceb, f"P-3 {path}: hash not in CURRENT_EXECUTION_BASIS")

    binding = r / "projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/BASIS_BINDING.md"
    table = {p: h for _, p, h in rows}
    bound = 0
    for line in binding.read_text().splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 3:
            pm = re.fullmatch(r"`([^`]+)`", cells[1]); hm = re.fullmatch(r"`([0-9a-f]{64})`", cells[2])
            if pm and hm:
                bound += 1
                p, h = pm.group(1), hm.group(1)
                ok(sha((r / p).read_bytes()) == h, f"P-4 {p}: BASIS_BINDING hash differs from today's bytes")
                ok(table.get(p) == h, f"P-4 {p}: BASIS_BINDING hash differs from the account's §3 row")
    ok(bound == 11, f"P-4 expected 11 bound rows in BASIS_BINDING.md, got {bound}")

    m = json.loads(pathlib.Path(a.manifest).read_text())
    schema_path = next(r.glob("projects/chirality-app-v4/execution/PKG-09_*/1_Working/DEL-09-11_*/Design/rrm.input-set-manifest.schema.json"))
    try:
        import jsonschema
        errs = list(jsonschema.Draft202012Validator(json.loads(schema_path.read_text())).iter_errors(m))
        ok(not errs, "M-1 schema: " + "; ".join(e.message for e in errs[:3]))
    except ImportError:
        fails.append("M-1 jsonschema not installed")
    paths = {i["path"]: i for i in m["items"]}
    drift = []
    for p, i in paths.items():
        f = r / p
        same = f.is_file() and sha(f.read_bytes()) == i["sha256"]
        if a.post_dispatch:
            if not same:
                drift.append(p)
        else:
            ok(same, f"M-2 {p}: manifest hash differs from today's bytes")
    acc = [p for p in paths if p.endswith("Design/EXECUTION_BASIS.md")]
    ok(len(acc) == 1 and paths[acc[0]]["standing"] == "project_file", "M-3 account missing or wrong standing")
    ok(not any(p.endswith(("EB1_QUESTION_KEY.md", "S2-E.md", "O-E.md")) for p in paths), "M-3 key, survey or owner notes supplied")
    for _, path, _ in rows:
        ok(path in paths, f"M-4 pin path not supplied: {path}")

    if a.post_dispatch:
        ok(sha(pathlib.Path(a.manifest).read_bytes()) == a.frozen_manifest_sha, "D-1 manifest is not the frozen one")
        sup = {}
        for line in pathlib.Path(a.post_dispatch).read_text().splitlines():
            if line.strip():
                h, p = line.split(None, 1)
                sup[p.strip().removeprefix("./")] = h
        for p, i in paths.items():
            ok(sup.get(p) == i["sha256"], f"D-1 {p}: supplied hash differs from the manifest")
        ok(sup.get(pathlib.Path(a.manifest).name) == a.frozen_manifest_sha, "D-1 supplied manifest is not the frozen one")
        print(f"post-dispatch drift (expected; informational): {len(drift)} item(s) changed since the read")
        for p in drift:
            print("  DRIFT", p)

    if a.verify_dir:
        d = pathlib.Path(a.verify_dir)
        for p, i in paths.items():
            f = d / p
            ok(f.is_file() and sha(f.read_bytes()) == i["sha256"], f"V-1 {p}: missing or differs in {d}")

    print(f"manifest sha256 {sha(pathlib.Path(a.manifest).read_bytes())}")
    print(f"account  sha256 {sha((DESIGN / 'EXECUTION_BASIS.md').read_bytes())}")
    print(f"pins checked: {len(rows)}; items: {len(paths)}")
    print(f"PASS {passes}  FAIL {len(fails)}")
    for f in fails:
        print("  FAIL", f)
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
