# SCA-001 — Run Summary

**Amendment ID:** SCA-001
**Date:** 2026-03-26
**Status:** COMPLETE

---

## Amendment Description
Incorporate Addenda 2, 3, and 4 into the WDMLRL Maintenance Shop Addition project decomposition. Structural system updated (precast concrete walls + steel roof), crane parameters established, overhead door type specified, mezzanine railing specified, interior wall material specified, gas supply parameters added, electrical pole relocation scope added, gas pipeline relocation added to County exclusions.

## Actions Taken

| # | Action | EntityID | Files Modified |
|---|--------|----------|----------------|
| 1 | ADD | SOW-0122 | Decomposition §3, §8; DEL-018-06/_CONTEXT.md |
| 2 | ADD (OUT) | SOW-0206 | Decomposition §4 |
| 3 | MODIFY | SOW-0022 | Decomposition §3; DEL-011-01/_CONTEXT.md |
| 4 | MODIFY | SOW-0067 | Decomposition §3; DEL-016-01/_CONTEXT.md, DEL-002-07/_CONTEXT.md |
| 5 | MODIFY | SOW-0025 | Decomposition §3; DEL-011-03/_CONTEXT.md, DEL-011-04/_CONTEXT.md, DEL-001-07/_CONTEXT.md |
| 6 | MODIFY | SOW-0032 | Decomposition §3; DEL-011-07/_CONTEXT.md, DEL-002-05/_CONTEXT.md |
| 7 | MODIFY | SOW-0011, SOW-0012 | Decomposition §3; DEL-001-02, -04, -05, -11/_CONTEXT.md; DEL-002-03, -04, -10, -12/_CONTEXT.md |
| 8 | MODIFY | SOW-0080 | Decomposition §3; DEL-018-06/_CONTEXT.md |
| 9 | ADD | R-08, R-09, R-10 | Decomposition §1 |

Additional decomposition edits: §2 (+2 vocab), §9 (counts + revision), §11 (+3 decisions), §12 (new Change Log)

## Pre-Change vs Post-Change Coverage

| Metric | Pre (PRE_SCA001) | Post (POST_SCA001) | Delta |
|---|---|---|---|
| Overall status | WARNINGS | OK | Improved |
| Packages declared | 21 | 21 | — |
| Packages found | 21 | 21 | — |
| Deliverables declared | 117 | 117 | — |
| Deliverables found | 117 | 117 | — |
| Forward coverage (packages) | 100% | 100% | — |
| Forward coverage (deliverables) | 100% | 100% | — |
| Scope items (IN) | 91 | 92 | +1 |
| Scope items (OUT) | 6 | 7 | +1 |
| Objectives covered | 8/8 | 8/8 | — |
| BLOCKERs | 0 | 0 | — |
| WARNINGs | 1 | 0 | -1 (resolved) |
| Revision | R1 | R2 | Updated |

**Resolved:** COV-001 (DeliverableCount 111→117 documentation error corrected)
**Regressions:** None

## Downstream Rerun Recommendations (not executed)

| Agent | Scope | Priority |
|---|---|---|
| DEPENDENCIES | PKG-001, PKG-002, PKG-011, PKG-016, PKG-018 | High |
| ESTIMATING | DEL-002-10 (structural calcs) | High |
| ESTIMATING | DEL-003-01, DEL-001-01 (preliminary designs) | Medium |
| ESTIMATING | DEL-018-06 (utility tie-ins — new scope) | Medium |

## Handoff to CHANGE

**Modified files for git staging:**

1. `_Decomposition/WDMLRL_Decomposition_Claude.md`
2. `PKG-001_Architectural Design/1_Working/DEL-001-02_Floor-Plans/_CONTEXT.md`
3. `PKG-001_Architectural Design/1_Working/DEL-001-04_Building-Sections/_CONTEXT.md`
4. `PKG-001_Architectural Design/1_Working/DEL-001-05_Interior-Elevations/_CONTEXT.md`
5. `PKG-001_Architectural Design/1_Working/DEL-001-07_Door-Window-Schedule/_CONTEXT.md`
6. `PKG-001_Architectural Design/1_Working/DEL-001-11_Specification/_CONTEXT.md`
7. `PKG-002_Structural Design/1_Working/DEL-002-03_Framing-Plans/_CONTEXT.md`
8. `PKG-002_Structural Design/1_Working/DEL-002-04_Structural-Sections/_CONTEXT.md`
9. `PKG-002_Structural Design/1_Working/DEL-002-05_Mezzanine-Details/_CONTEXT.md`
10. `PKG-002_Structural Design/1_Working/DEL-002-07_Crane-Support-Details/_CONTEXT.md`
11. `PKG-002_Structural Design/1_Working/DEL-002-10_Calculation-Package/_CONTEXT.md`
12. `PKG-002_Structural Design/1_Working/DEL-002-12_Specification/_CONTEXT.md`
13. `PKG-011_Building Structure & Envelope/1_Working/DEL-011-01_Superstructure/_CONTEXT.md`
14. `PKG-011_Building Structure & Envelope/1_Working/DEL-011-03_Repair-Bays/_CONTEXT.md`
15. `PKG-011_Building Structure & Envelope/1_Working/DEL-011-04_Doors-Entrances/_CONTEXT.md`
16. `PKG-011_Building Structure & Envelope/1_Working/DEL-011-07_Mezzanine/_CONTEXT.md`
17. `PKG-016_Crane & Lifting Equipment/1_Working/DEL-016-01_Overhead-Cranes/_CONTEXT.md`
18. `PKG-018_Sitework & Civil Construction/1_Working/DEL-018-06_Utility-Tieins/_CONTEXT.md`
19. `_ScopeChange/SCA-001_2026-03-26/` (entire snapshot folder — new)
20. `_Reconciliation/DecompCoverage/COV_PRE_SCA001_2026-03-26_1724/` (new)
21. `_Reconciliation/DecompCoverage/COV_POST_SCA001_2026-03-26_1748/` (new)

**Recommended commit message:**
```
scope: SCA-001 — Incorporate Addenda 2, 3, 4 (WDMLRL Maintenance Shop)

Actions: 9 (ADD:2, MODIFY:7)
Affected deliverables: DEL-001-02, -04, -05, -07, -11, DEL-002-03, -04, -05, -07, -10, -12, DEL-011-01, -03, -04, -07, DEL-016-01, DEL-018-06
```
