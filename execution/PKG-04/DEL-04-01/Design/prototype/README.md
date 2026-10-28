# DEL-04-01 policy-class record prototype (R12-3)

**This is a prototype, not product code.** It validates the PROPOSED
structure of the adopted policy-class configuration (ACT-POLICY-v0.8 §8.1,
`../ACT_POLICY_CLASS_RECORD.schema.json`) against its example instances:
P-01, P-01a and P-02…P-06 written as data
(`../ACT_POLICY_CLASS_RECORD.valid.example.json`) and three invalid records
(`../ACT_POLICY_CLASS_RECORD.invalid.examples.json`). It selects no
placement (OI-013, OI-014) and no content-identity method.

It uses the JSON Schema subset validator kept in DEL-04-03's prototype folder
(`minischema.py`; the subset is listed in that folder's README), plus two
checks the subset does not express: record identities are unique, and a
record whose class is *reserved to the person* is not widenable.

## Run

```text
cd "<this folder>"
python3 -B validate_policy.py
```

Python 3 standard library only (Python 3.13.7, macOS, 2026-09-30). The
output is recorded in `WAVE_B/B4.md` of run `APP-V4-DESIGN-PASS-2-20260930`.
