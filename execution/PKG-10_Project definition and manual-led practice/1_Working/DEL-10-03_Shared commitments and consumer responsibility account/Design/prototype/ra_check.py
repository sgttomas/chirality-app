#!/usr/bin/env python3
"""RA checks (DEL-10-03 RA-v0.1 §5). Design prototype, not product code. Read-only.

  python3 ra_check.py              # run the checks; exit 0 only if all pass
  python3 ra_check.py --strict     # also fail when a cited supplier hash has moved
  python3 ra_check.py --self-test  # negative cases: each must be detected

Checks:
  H-1  every supplier Design and supplier SoW sha256 prefix cited in §1.2 and §3.1
       equals today's bytes. A moved supplier is reported as a NOTICE with a re-pin
       instruction (R23-21), not a failure (RV3 RA1-R2); --strict makes it a failure
  P-1  DEL-10-03's ACTIVE EXECUTION rows to DEL-02/03/04/05 deliverables equal the
       nine supplier entries S-1…S-9 (row IDs DEP-10-03-008…016)
  R-1  reverse scan: every ACTIVE row in any register targeting DEL-10-03 is either
       DEL-10-03's own, a supplier mirror listed in §3.1, or a listed consumer row
  R-2  every supplier SoW clause (CLM/REQ) naming DEL-10-03 is the one §3.1 cites
  F-1  F-RA1 still holds: DEL-04-01, DEL-05-01, DEL-05-02 have no mirror and no
       SoW clause naming DEL-10-03 (so a later mirror is noticed and the finding updated)
"""
import argparse
import csv
import glob
import hashlib
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
DESIGN = HERE.parent
TARGET = "DEL-10-03"

SUPPLIERS = {  # entry: (deliverable, register row, design file name)
    "S-1": ("DEL-02-01", "DEP-10-03-008", "WORKFLOW_DECLARATION.md"),
    "S-2": ("DEL-02-03", "DEP-10-03-009", "EXECUTION_COMPATIBILITY.md"),
    "S-3": ("DEL-02-04", "DEP-10-03-010", "ROLE_SUPPLY.md"),
    "S-4": ("DEL-03-01", "DEP-10-03-011", "CATALOG_AND_READ_BASIS.md"),
    "S-5": ("DEL-03-02", "DEP-10-03-012", "PROPOSAL_LIFECYCLE_AND_OUTCOMES.md"),
    "S-6": ("DEL-04-01", "DEP-10-03-013", "ACT_AND_POLICY_CONTRACT.md"),
    "S-7": ("DEL-04-03", "DEP-10-03-014", "RECORD_SEMANTICS.md"),
    "S-8": ("DEL-05-01", "DEP-10-03-015", "LOOP_RECEIVING_CONTRACT.md"),
    "S-9": ("DEL-05-02", "DEP-10-03-016", "PANEL_RECEIVING_CONTRACT.md"),
}
MIRRORS = {"DEP-02-01-040", "DEP-02-03-040", "DEP-02-04-018", "DEP-03-01-042",
           "DEP-03-02-033", "DEP-04-03-045"}
CONSUMER_ROWS = {"DEP-10-04-007", "DEP-11-01-008", "DEP-11-02-008"}
SOW_CLAUSES = {"DEL-02-01": {"CLM-002"}, "DEL-02-03": {"CLM-003"}, "DEL-02-04": {"CLM-002"},
               "DEL-03-01": {"CLM-002"}, "DEL-03-02": {"CLM-004"}, "DEL-04-03": {"REQ-005"},
               "DEL-04-01": set(), "DEL-05-01": set(), "DEL-05-02": set()}
F_RA1 = {"DEL-04-01", "DEL-05-01", "DEL-05-02"}


def execution_root() -> pathlib.Path:
    top = subprocess.run(["git", "-C", str(HERE), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True, check=True).stdout.strip()
    return pathlib.Path(top) / "projects/chirality-app-v4/execution"


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def folder(e: pathlib.Path, d: str) -> pathlib.Path:
    return pathlib.Path(glob.glob(str(e / f"PKG-*/1_Working/{d}_*"))[0])


def cited_prefixes(text: str):
    """(deliverable or design name) -> set of 8+ hex prefixes cited in §1.2 / §3.1 rows."""
    out = {}
    for line in text.splitlines():
        if not line.startswith("| S-"):
            continue
        entry = line.split("|")[1].strip()
        out.setdefault(entry, set()).update(re.findall(r"`([0-9a-f]{8,})…`", line))
    return out


def run(e: pathlib.Path, account: str, registers: dict, sows: dict, designs: dict, strict=False):
    fails, passes, notices = [], 0, []

    def ok(c, msg):
        nonlocal passes
        if c:
            passes += 1
        else:
            fails.append(msg)

    cited = cited_prefixes(account)
    for entry, (d, row, dname) in SUPPLIERS.items():
        ok(bool(cited.get(entry)), f"H-1 {entry} {d}: no hash cited")
        moved = [x for x in cited.get(entry, set()) if designs[d][:len(x)] != x and sows[d][:len(x)] != x]
        if moved:
            msg = (f"H-1 {entry} {d}: cited {moved} no longer matches today's Design ({designs[d][:16]}…) "
                   f"or SoW ({sows[d][:16]}…). Re-pin deliberately after reading the change (R23-21)")
            if strict:
                fails.append(msg)
            else:
                notices.append(msg)
    own = [r for r in registers[TARGET] if r["Status"] == "ACTIVE" and r["DependencyClass"] == "EXECUTION"
           and re.match(r"DEL-0[2-5]-", r["TargetDeliverableID"] or "")]
    ok({(r["TargetDeliverableID"], r["DependencyID"]) for r in own} ==
       {(d, row) for d, row, _ in SUPPLIERS.values()}, "P-1 DEL-10-03's supplier rows differ from S-1…S-9")
    for d, rows in registers.items():
        if d == TARGET:
            continue
        for r in rows:
            if r["Status"] == "ACTIVE" and (r["TargetDeliverableID"] or "") == TARGET:
                ok(r["DependencyID"] in MIRRORS | CONSUMER_ROWS, f"R-1 unlisted row {r['DependencyID']} ({d}) targets DEL-10-03")
    for d, sow in sows.items():
        found = {m.group(1) for m in re.finditer(r"^- \*\*((?:CLM|REQ)-\d+)\*\*[^\n]*DEL-10-03", sow_text[d], re.M)}
        ok(found == SOW_CLAUSES[d], f"R-2 {d}: SoW clauses naming DEL-10-03 {sorted(found)} != {sorted(SOW_CLAUSES[d])}")
    for d in F_RA1:
        mirror = [r for r in registers[d] if r["Status"] == "ACTIVE" and (r["TargetDeliverableID"] or "") == TARGET]
        ok(not mirror and not SOW_CLAUSES[d], f"F-1 {d} now has a mirror or clause: update F-RA1")
    return passes, fails, notices


sow_text = {}


def load(e: pathlib.Path):
    registers, sows, designs = {}, {}, {}
    for f in glob.glob(str(e / "PKG-*/1_Working/DEL-*/Dependencies.csv")):
        d = re.search(r"(DEL-\d\d-\d\d)_", f).group(1)
        registers[d] = list(csv.DictReader(open(f)))
    for d, _, dname in SUPPLIERS.values():
        fo = folder(e, d)
        sows[d] = sha(fo / "ScopeOfWork.md")
        sow_text[d] = (fo / "ScopeOfWork.md").read_text()
        designs[d] = sha(fo / "Design" / dname)
    return registers, sows, designs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    e = execution_root()
    account = (DESIGN / "RESPONSIBILITY_ACCOUNT.md").read_text()
    registers, sows, designs = load(e)
    if not a.self_test:
        passes, fails, notices = run(e, account, registers, sows, designs, a.strict)
        print(f"account sha256 {sha(DESIGN / 'RESPONSIBILITY_ACCOUNT.md')}")
        print(f"PASS {passes}  FAIL {len(fails)}  NOTICE {len(notices)}")
        for n in notices:
            print("  NOTICE", n)
        for f in fails:
            print("  FAIL", f)
        return 0 if not fails else 1
    # Negative cases: each mutation must produce a failure with the named check.
    cases = []
    d2 = dict(designs); d2["DEL-02-01"] = "0" * 64
    _, f_def, n_def = run(e, account, registers, sows, d2)
    print(f"self-test H-1 default: {'notice' if any(n.startswith('H-1') for n in n_def) and not any(f.startswith('H-1') for f in f_def) else 'WRONG'}")
    bad_h = not (any(n.startswith('H-1') for n in n_def) and not any(f.startswith('H-1') for f in f_def))
    cases.append(("H-1", run(e, account, registers, sows, d2, strict=True)))
    r2 = {k: list(v) for k, v in registers.items()}
    r2[TARGET] = [r for r in r2[TARGET] if r["DependencyID"] != "DEP-10-03-016"]
    cases.append(("P-1", run(e, account, r2, sows, designs)))
    r3 = {k: list(v) for k, v in registers.items()}
    extra = dict(r3["DEL-05-01"][0]); extra.update(DependencyID="DEP-05-01-999", Status="ACTIVE", TargetDeliverableID=TARGET)
    r3["DEL-05-01"].append(extra)
    cases.append(("R-1", run(e, account, r3, sows, designs)))
    cases.append(("F-1", run(e, account, r3, sows, designs)))
    saved = sow_text["DEL-05-02"]
    sow_text["DEL-05-02"] = saved + "\n- **CLM-099** received by DEL-10-03.\n"
    cases.append(("R-2", run(e, account, registers, sows, designs)))
    sow_text["DEL-05-02"] = saved
    bad = int(bad_h)
    for check, (_, fails, _n) in cases:
        hit = any(f.startswith(check) for f in fails)
        print(f"self-test {check}: {'detected' if hit else 'MISSED'}")
        bad += not hit
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
