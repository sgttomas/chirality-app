"""Validate the PROPOSED policy-class configuration examples (R12-3). Prototype only.

  python3 -B validate_policy.py

Uses the subset validator kept in DEL-04-03's prototype folder (minischema.py).
Checks the schema, the valid P-01…P-06 configuration and the invalid records,
and two rules the schema subset does not express: record identities are
unique, and every catalog-class record that is "reserved to the person" is
not widenable.
"""

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(HERE)
WORKING = os.path.dirname(os.path.dirname(DESIGN))
sys.path.insert(0, glob.glob(os.path.join(WORKING, "DEL-04-03", "Design", "prototype"))[0])
from minischema import Registry, validate  # noqa: E402

reg = Registry()
sid = reg.load(os.path.join(DESIGN, "ACT_POLICY_CLASS_RECORD.schema.json"))
schema = reg.by_id[sid]
ok = True

valid = json.load(open(os.path.join(DESIGN, "ACT_POLICY_CLASS_RECORD.valid.example.json"), encoding="utf-8"))
errs = validate(valid, schema, reg)
ids = [r["recordId"] for r in valid["records"]]
print("valid configuration:", "PASS" if not errs else f"FAIL {errs[:3]}", "records", ids)
ok &= not errs
dup = len(ids) != len(set(ids))
bad_widen = [r["recordId"] for r in valid["records"]
             if r.get("humanActClass") == "reserved to the person" and r.get("widenable") != "no"]
print("unique identities:", "PASS" if not dup else "FAIL")
print("reserved records not widenable:", "PASS" if not bad_widen else f"FAIL {bad_widen}")
ok &= not dup and not bad_widen

for c in json.load(open(os.path.join(DESIGN, "ACT_POLICY_CLASS_RECORD.invalid.examples.json"), encoding="utf-8")):
    e = validate(c["instance"], schema, reg)
    print(f"{c['case']} invalid:", "PASS" if e else "FAIL (validated)", "-", (e[0][:100] if e else ""))
    ok &= bool(e)

print("RESULT:", "all expectations held" if ok else "failures")
sys.exit(0 if ok else 1)
