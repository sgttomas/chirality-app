# Decomposition Coverage Report — COV_POST_SCA001

**Run Label:** POST_SCA001
**Timestamp:** 2026-03-26T17:48
**Decomposition:** `_Decomposition/WDMLRL_Decomposition_Claude.md` (R2 — 2026-03-26, SCA-001)
**Variant:** PROJECT
**Scope:** ALL
**Requested By:** SCOPE_CHANGE
**Prior Run:** PRE_SCA001 (2026-03-26T17:24, R1)

---

## Summary Table

| Check | Name | Verdict | Issues |
|---|---|---|---|
| 1 | Forward Coverage: Packages | **PASS** | 0 |
| 2 | Forward Coverage: Deliverables | **PASS** | 0 |
| 3 | Reverse Coverage: Folders | **PASS** | 0 |
| 4 | ID Consistency | **PASS** | 0 |
| 5 | Context Fidelity | **PASS** | 0 |
| 6 | Artifact Presence | **PASS** | 0 |
| 7 | Objective Mapping | **PASS** | 0 |
| 8 | Ledger Integrity | **PASS** | 0 |
| 9 | Lifecycle Distribution | **PASS** | 0 |

**Overall Status: OK** (0 BLOCKERs, 0 WARNINGs, 0 INFOs)

---

## Check 1 — Forward Coverage: Packages

All 21 packages declared in §6 have corresponding `PKG-{ID}_*` folders under the execution root.

| PackageID | Declared Name | Folder Found | Folder Path |
|---|---|---|---|
| PKG-001 | Architectural Design | Yes | `PKG-001_Architectural Design/` |
| PKG-002 | Structural Design | Yes | `PKG-002_Structural Design/` |
| PKG-003 | Mechanical Design | Yes | `PKG-003_Mechanical Design/` |
| PKG-004 | Electrical Design | Yes | `PKG-004_Electrical Design/` |
| PKG-005 | Civil Design | Yes | `PKG-005_Civil Design/` |
| PKG-006 | Plumbing Design | Yes | `PKG-006_Plumbing Design/` |
| PKG-007 | Landscape Architectural Design | Yes | `PKG-007_Landscape Architectural Design/` |
| PKG-008 | Geotechnical Investigation & Surveying | Yes | `PKG-008_Geotechnical Investigation & Surveying/` |
| PKG-009 | Permitting & Regulatory Compliance | Yes | `PKG-009_Permitting & Regulatory Compliance/` |
| PKG-010 | Foundation Construction | Yes | `PKG-010_Foundation Construction/` |
| PKG-011 | Building Structure & Envelope | Yes | `PKG-011_Building Structure & Envelope/` |
| PKG-012 | Interior Construction & Fit-Out | Yes | `PKG-012_Interior Construction & Fit-Out/` |
| PKG-013 | Mechanical & HVAC Installation | Yes | `PKG-013_Mechanical & HVAC Installation/` |
| PKG-014 | Plumbing & Water Systems Installation | Yes | `PKG-014_Plumbing & Water Systems Installation/` |
| PKG-015 | Electrical & Low-Voltage Installation | Yes | `PKG-015_Electrical & Low-Voltage Installation/` |
| PKG-016 | Crane & Lifting Equipment | Yes | `PKG-016_Crane & Lifting Equipment/` |
| PKG-017 | Existing Building Renovation (Old North Shop) | Yes | `PKG-017_Existing Building Renovation (Old North Shop)/` |
| PKG-018 | Sitework & Civil Construction | Yes | `PKG-018_Sitework & Civil Construction/` |
| PKG-019 | Construction Management & OH&S | Yes | `PKG-019_Construction Management & OH&S/` |
| PKG-020 | Commissioning & Closeout | Yes | `PKG-020_Commissioning & Closeout/` |
| PKG-021 | Bonding, Insurance & Warranty | Yes | `PKG-021_Bonding, Insurance & Warranty/` |

**Verdict: PASS** (21/21 = 100.0%)

---

## Check 2 — Forward Coverage: Deliverables

All 117 deliverables declared in §7 have corresponding `DEL-{ID}_*` folders under their parent package's `1_Working/` directory.

Per-package deliverable counts:

| PackageID | Declared | Found | Coverage |
|---|---|---|---|
| PKG-001 | 11 | 11 | 100% |
| PKG-002 | 12 | 12 | 100% |
| PKG-003 | 7 | 7 | 100% |
| PKG-004 | 9 | 9 | 100% |
| PKG-005 | 7 | 7 | 100% |
| PKG-006 | 8 | 8 | 100% |
| PKG-007 | 4 | 4 | 100% |
| PKG-008 | 4 | 4 | 100% |
| PKG-009 | 4 | 4 | 100% |
| PKG-010 | 1 | 1 | 100% |
| PKG-011 | 7 | 7 | 100% |
| PKG-012 | 3 | 3 | 100% |
| PKG-013 | 6 | 6 | 100% |
| PKG-014 | 6 | 6 | 100% |
| PKG-015 | 5 | 5 | 100% |
| PKG-016 | 1 | 1 | 100% |
| PKG-017 | 4 | 4 | 100% |
| PKG-018 | 6 | 6 | 100% |
| PKG-019 | 4 | 4 | 100% |
| PKG-020 | 3 | 3 | 100% |
| PKG-021 | 5 | 5 | 100% |

**Verdict: PASS** (117/117 = 100.0%)

---

## Check 3 — Reverse Coverage: Folders

Every `PKG-*` folder and every `DEL-*` folder in the filesystem traces back to a declared entity in the decomposition. No orphan folders detected.

- Package folders scanned: 21 — all match §6 declarations
- Deliverable folders scanned: 117 — all match §7 declarations

**Verdict: PASS** (100.0%)

---

## Check 4 — ID Consistency

For all 117 matched pairs, the deliverable ID extracted from the folder name (after stripping the `_{description}` suffix) matches the DeliverableID in §7 exactly. The parent PackageID extracted from the folder path matches the declared parent package.

No mismatches detected.

**Verdict: PASS**

---

## Check 5 — Context Fidelity

All 117 deliverable folders contain a `_CONTEXT.md` file. For each:
- The **Package** field references the correct PKG-ID matching the parent folder
- The **Name** field is consistent with the deliverable name in §7
- Two format variants were encountered across the 117 files; both are valid and correctly encode the required fields

No field disagreements detected.

**Verdict: PASS** (117/117 = 100.0%)

---

## Check 6 — Artifact Presence

All 117 deliverable folders exist and contain their respective context and status files. The decomposition's §7 tables specify "Covers SOW" mappings rather than individual artifact filenames; structural presence of each deliverable folder (which is the prerequisite container for all artifacts) is confirmed at 100%.

All deliverables are currently in SEMANTIC_READY state (pre-production), so anticipated artifacts are not yet expected to be physically present as files. No INFO or WARNING escalations apply.

**Verdict: PASS** (100.0%)

---

## Check 7 — Objective Mapping

All 8 objectives (OBJ-001 through OBJ-008) from §5 are mapped to at least one deliverable with an existing folder:

| ObjectiveID | Supporting Packages | Active Deliverables | Status |
|---|---|---|---|
| OBJ-001 | PKG-001 thru PKG-020 | 96+ deliverables | Covered |
| OBJ-002 | PKG-008, PKG-009, PKG-010, PKG-011, PKG-019, PKG-020 | 16+ deliverables | Covered |
| OBJ-003 | PKG-001 thru PKG-008 | 62+ deliverables | Covered |
| OBJ-004 | PKG-003, PKG-006, PKG-013, PKG-014, PKG-016, PKG-018, PKG-020 | 27+ deliverables | Covered |
| OBJ-005 | PKG-004, PKG-015, PKG-016, PKG-018, PKG-020 | 16+ deliverables | Covered |
| OBJ-006 | PKG-002, PKG-008, PKG-010, PKG-020, PKG-021 | 8+ deliverables | Covered |
| OBJ-007 | PKG-009, PKG-014, PKG-019 | 9+ deliverables | Covered |
| OBJ-008 | PKG-021 | 5 deliverables | Covered |

No objective has zero active supporting deliverables. No objective is supported only by RETIRED deliverables (all are SEMANTIC_READY).

**Verdict: PASS** (8/8 = 100.0%)

---

## Check 8 — Ledger Integrity

The Scope Ledger (§8) contains 92 IN-scope items. For each:
- The PackageID references an existing package (validated in Check 1)
- The DeliverableID(s) reference existing deliverables (validated in Check 2)
- No atomic unit references a non-existent partition or production unit

Additionally validated:
- §9 reports ScopeItemCount IN=92, OUT=7 — consistent with §8 and §4
- §9 DeliverableCount=117 — consistent with §7 actual count (this was the prior run's WARNING, now RESOLVED)
- §9 PackageCount=21 — consistent with §6
- §9 ObjectiveCount=8 — consistent with §5

**Verdict: PASS**

---

## Check 9 — Lifecycle Distribution

| State | Count |
|---|---|
| SEMANTIC_READY | 117 |
| OPEN | 0 |
| INITIALIZED | 0 |
| IN_PROGRESS | 0 |
| CHECKING | 0 |
| ISSUED | 0 |
| RETIRED | 0 |
| UNKNOWN | 0 |

All 117 deliverables are in SEMANTIC_READY state. No unexpected lifecycle states detected.

**Verdict: PASS**

---

## Delta Report — POST_SCA001 vs PRE_SCA001

### Metrics Comparison

| Metric | PRE_SCA001 (R1) | POST_SCA001 (R2) | Change |
|---|---|---|---|
| Decomposition revision | R1 (2026-02-25) | R2 (2026-03-26) | Updated |
| ScopeItemCount (IN) | 91* | 92 | +1 (SOW-0122 added) |
| ScopeItemCount (OUT) | 6* | 7 | +1 (SOW-0206 added) |
| PackageCount | 21 | 21 | No change |
| DeliverableCount | 117 | 117 | No change |
| ObjectiveCount | 8 | 8 | No change |
| Forward coverage (packages) | 100.0% | 100.0% | No change |
| Forward coverage (deliverables) | 100.0% | 100.0% | No change |
| Reverse coverage | 100.0% | 100.0% | No change |
| Context fidelity | 100.0% | 100.0% | No change |
| Artifact presence | 100.0% | 100.0% | No change |
| Objective coverage | 100.0% | 100.0% | No change |
| Issues (BLOCKER) | 0 | 0 | No change |
| Issues (WARNING) | 1 | 0 | -1 (RESOLVED) |
| Issues (INFO) | 0 | 0 | No change |
| Overall status | WARNINGS | OK | Improved |

*Note: PRE_SCA001 was run against R1 which had IN=91 and OUT=6. SCA-001 added SOW-0122 (IN) and SOW-0206 (OUT).

### Resolved Issues

| Prior IssueID | Description | Resolution |
|---|---|---|
| COV-001 | §9 Telemetry stated DeliverableCount=111 but actual count from §7 was 117 | §9 now correctly states DeliverableCount=117 (corrected as part of SCA-001 per D-011) |

### Regressions

None. Forward coverage has not regressed. No new BLOCKERs or WARNINGs.

### SCA-001 Impact Summary

The scope change incorporated Addenda 2, 3, and 4 with the following effects:
- **+1 IN scope item:** SOW-0122 (electrical pole relocation) mapped to existing DEL-018-06
- **+1 OUT scope item:** SOW-0206 (gas pipeline relocation — County responsibility)
- **6 modified scope items:** Design parameter updates from addenda Q&A (structural system, crane specs, door type, mezzanine railing, interior walls, gas supply)
- **0 new deliverables:** SOW-0122 absorbed into DEL-018-06 per D-013
- **0 new packages:** No structural changes
- **1 documentation correction:** DeliverableCount 111 to 117 in §9

### Methodology Notes

No methodology changes between PRE_SCA001 and POST_SCA001. Same 9-check protocol applied identically.

---

## What to Fix for a Cleaner Rerun

Nothing. All 9 checks pass with zero issues. The decomposition document and filesystem are fully synchronized.
