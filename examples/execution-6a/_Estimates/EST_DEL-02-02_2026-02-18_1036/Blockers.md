# Blockers Report: EST_DEL-02-02_2026-02-18_1036

## Summary

**Critical blockers preventing meaningful estimate: 0**

No dependency or input gaps prevent the generation of a meaningful estimate for DEL-02-02. All major cost elements have rate table evidence and confirmed quantities. Minor uncertainties exist around support room sizing (ranges, not confirmed areas) and compressed air piping routing.

## Dependency-Derived Blockers

### Upstream Dependencies (from Dependencies.csv)

| DependencyID | Target | Type | Estimate Impact | Blocked? |
|---|---|---|---|---|
| DEP-0202-E01 | DEL-02-01 (Architectural Program) | PREREQUISITE | LOW -- floor plan zone allocation affects support room sizing; midpoint assumptions used | NO |
| DEP-0202-E02 | DEL-02-04 (Envelope/Doors) | INTERFACE | NONE -- overhead doors excluded from DEL-02-02 per cost ownership rules | NO |
| DEP-0202-E03 | DEL-02-05 (Mechanical) | INTERFACE | NONE -- exhaust systems and general plumbing excluded from DEL-02-02 | NO |
| DEP-0202-E04 | DEL-02-06 (Electrical/IT) | INTERFACE | NONE -- electrical excluded from DEL-02-02 | NO |
| DEP-0202-E05 | DEL-02-07 (Emergency Power) | INTERFACE | NONE -- generator excluded from DEL-02-02 | NO |
| DEP-0202-E06 | DEL-03-01 (Site Plan) | INTERFACE | NONE -- bay orientation does not materially change fit-up cost | NO |
| DEP-0202-E09 | Alberta Building Code | CONSTRAINT | NONE for pricing -- may affect compliance verification in later phases | NO |

### Information Gaps (not full blockers)

| Gap | Impact | Mitigation |
|---|---|---|
| Support room areas are ranges, not confirmed dimensions | Quantities vary +/- 15-25% | Midpoint assumptions used; flagged in Assumptions_Log |
| Compressed air piping routing not designed | Cost for piping is rough allowance | $20,000 allowance with +/- 25% range; flagged as ALLOWANCE method |
| Breathing air compressor system not specified | Wide price range ($45k-$65k) | Midpoint $55,000 used; LOW confidence flagged |
| Bunker gear locker specification not finalized | Unit rate range $1,800-$2,500 | Midpoint $2,200 used; MED confidence |
