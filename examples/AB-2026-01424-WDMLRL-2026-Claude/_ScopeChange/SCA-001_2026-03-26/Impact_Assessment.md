# SCA-001 — Impact Assessment

**Amendment ID:** SCA-001
**Date:** 2026-03-26

## Summary

| Metric | Value |
|---|---|
| Total atomic actions | 9 |
| New IN-scope items | 1 (SOW-0122) |
| New OUT-scope items | 1 (SOW-0206) |
| Modified IN-scope items | 6 |
| New deliverables | 0 (SOW-0122 maps to existing DEL-018-06) |
| New references | 3 (R-08, R-09, R-10) |
| Dependency orphan risk | 0 |
| Estimates flagged stale | 3 certain, 3 advisory |
| Schedule staleness risk | None (no schedule artifacts exist) |

## Affected Deliverables

### PKG-001 (Architectural Design)
- DEL-001-02, DEL-001-04, DEL-001-05, DEL-001-07, DEL-001-11
- Reason: Interior walls precast concrete; door type specification

### PKG-002 (Structural Design)
- DEL-002-03, DEL-002-04, DEL-002-05, DEL-002-07, DEL-002-10, DEL-002-12
- Reason: Structural system change; crane parameters; interior walls

### PKG-011 (Building Structure & Envelope)
- DEL-011-01, DEL-011-03, DEL-011-04, DEL-011-07
- Reason: Precast walls + steel roof; door type; mezzanine railing

### PKG-016 (Crane & Lifting Equipment)
- DEL-016-01
- Reason: Crane design parameters established

### PKG-018 (Sitework & Civil Construction)
- DEL-018-06
- Reason: New SOW-0122 scope; gas supply parameters

## Stale Estimates
- **EST_DEL-002-10** — structural calc package (STALE: material system changed)
- **EST_DEL-003-01** — preliminary mechanical (POTENTIALLY STALE: gas supply defined)
- **EST_DEL-001-01** — preliminary architectural (POTENTIALLY STALE: wall material changed)

## Recommended Downstream Reruns
1. DEPENDENCIES re-extraction: PKG-001, PKG-002, PKG-011, PKG-016, PKG-018
2. ESTIMATING re-run: DEL-002-10 (mandatory), DEL-003-01 (advisory), DEL-001-01 (advisory)
