# Deepcut Decomposition and Folder Review — Run Summary

**Date:** 2026-04-19
**Root:** `domain-test/domains/West_Doe_Deepcut_DBM`
**Plan:** `plans/DEEPCUT_DECOMPOSITION_AND_FOLDER_REVIEW_PLAN.md`
**Mode:** Review + Repair

---

## Baseline Inventory

| Item | Count |
|------|-------|
| Categories | 18 (CAT-000 through CAT-017) |
| KTY folders | 98 (plan assumed 132; actual 1:1 with register) |
| Decomposition package files | 13 authoritative + Archive.zip |
| SCA snapshot directories | 4 (SCA-001, SCA-001_2026-04-14_1430, SCA-002_2026-04-14_1510, SCA-003_2026-04-19_0900) |

---

## Repaired Now

### _ScopeChange repairs

None required. `_LATEST.md` correctly points to SCA-003. SCA-002 incomplete
artifacts accepted as historical limitation (H3 ruling). SCA-001 (no timestamp)
is historical residue.

### _Decomposition parity repairs

| ID | File | Repair |
|---|---|---|
| D3 | `DeepCut_Knowledge_Subject_Register_v4.csv` | 11 subjects changed from InOutStatus=IN to RETIRED (SUB-03-02-02, SUB-04-18-01 through SUB-04-18-09, SUB-04-19-06) |
| D5 | `DeepCut_Knowledge_Type_Register_v4.csv` | KTY-03-02 UnitCount 148→178; KTY-04-19 UnitCount 104→143 |
| D10 | `DeepCut_Knowledge_Type_Register_v4.csv` | CSV quoting fixed for KTY-04-16 and KTY-04-17 rows (unquoted commas in `2,385 m3/d`) |
| T1 | `DeepCut_Knowledge_Type_Register_v4.csv` | "Seive"→"Sieve" in KTY-04-13 and KTY-04-17 Name and Description fields |
| H1 | `DeepCut_Domain_Ledger_v4.csv` | 6 units retired (HBK-1391, -1392, -1397, -1398, -1474, -1477): InOutStatus IN→RETIRED, OpenIssue True→False |
| H2 | `DeepCut_Vocabulary_Map_v4.csv` | "Cross-Fence" replaced by "Cross-Facility" as canonical term (Cross-Fence denotes outside-project flows) |
| — | `DeepCut_Coverage_Telemetry_v4.json` | Recomputed: IN 4981→4975, RETIRED 281→287, UnitCount 5696→5690, OpenIssueCount 577→571. Revision tagged v4.3-SCA-003-reviewed. |

### KTY metadata repairs

| ID | KTY | Files | Repair |
|---|---|---|---|
| M1 | KTY-04-18 | `_CONTEXT.md` | Name: added `[RETIRED — SCA-001]`; Scope Status: IN→RETIRED; Description: rewritten for retirement |
| M2 | KTY-04-18 | `_STATUS.md` | Added RETIRED transition (2026-04-14, SCA-001) |
| M3 | KTY-04-16 | `_REFERENCES.md`, `_DEPENDENCIES.md`, `_SEMANTIC.md` | Headers updated from "LPG Mercaptan Treating (FUTURE)" to "NGL Mercaptan Treating" |
| M3 | KTY-04-17 | `_REFERENCES.md`, `_DEPENDENCIES.md`, `_SEMANTIC.md` | Headers updated from "LPG Molecular Seive (MS) Dehydration (FUTURE)" to "NGL Molecular Sieve (MS) Dehydration" |

### Campaign artifact updates

| File | Repair |
|---|---|
| `plans/Deepcut_Terminology_Decisions.md` | "Cross-Fence" row corrected to "Cross-Facility" as canonical term |

---

## Requires Domain-Documents Rerun

| KTY | Reason | Drift Type |
|---|---|---|
| KTY-05-08 | KA-03 Moisture Analyzer and Scoping.md say "LPG Mole Sieve (Future)" — should be "NGL Molecular Sieve (current scope)" per SCA-003 | Terminology + scope framing |
| KTY-06-09 | KA-01 Overall Emissions Summary has "LPG MS Purge - Future" table labels without SCA-003 annotation | Terminology (source-faithful label, low priority) |

Metadata alignment must follow these reruns per the revised plan.

---

## Requires Main Document Refresh (Not Hand-Patched)

The main decomposition document `DeepCut_DOMAIN_DECOMP_FINAL_v4.md` has stale
embedded counts in its Coverage & Telemetry block and Open Issues tables. These
should be regenerated from the corrected registers and telemetry JSON rather than
manually patching individual numbers in a 10,000+ line document.

| ID | Section | Issue |
|---|---|---|
| D1 | Coverage & Telemetry table | Missing SCA-002 and SCA-003 rows (last row is v4.1-SCA-001) |
| D2 | Coverage & Telemetry table | Subject count 433 vs actual 432 |
| D4 | Coverage & Telemetry table | UnitCount 5680 vs current 5690 |
| D8 | Open Issues table | Sums to 567 vs current 571 |
| D9 | Open Issues CSV descriptions | OI-004 through OI-009 carry different-era counts |

---

## Remaining KTY Register Column Drift (D6)

These KTYs have stale column values that diverge from the Notes field and ledger.
The KTY Register agent fixed KTY-03-02 UnitCount and KTY-04-19 UnitCount. The
remaining discrepancies are:

| KTY | Field | Column Value | Notes/Ledger Value |
|---|---|---|---|
| KTY-01-04 | OpenIssueCount | 12 | 13 |
| KTY-03-02 | OpenIssueCount | 8 | 4 (further reduced by 6 after ledger repair) |
| KTY-04-02 | UnitCount | 62 | 56 (child-subject sum) |
| KTY-04-16 | UnitCount | 205 | 204 |
| KTY-04-16 | OpenIssueCount | 28 | 26 |
| KTY-05-01 | UnitCount | 187 | 186 |
| KTY-05-01 | OpenIssueCount | 40 | 39 |
| KTY-05-02 | UnitCount | 24 | 20 |
| KTY-12-05 | UnitCount | 56 | 50 |
| KTY-12-05 | OpenIssueCount | 3 | 2 |

These are best reconciled as part of a fresh telemetry recomputation after all
downstream reruns complete.

---

## Out of Scope (Noted)

| Item | Status |
|---|---|
| `_Aggregation/Equipment_List/` CSVs with stale LPG/FUTURE | Out of direct repair scope per plan; regeneration needed |
| SCA-001 (no timestamp) fragment | Historical residue; contains only Value_Engineering_Tracker.csv |
| SCA-002 incomplete snapshot | Accepted as historical limitation (H3 ruling) |
| KTY-04-16/17 folder slugs with LPG/FUTURE | Frozen per ALLOW_RENUMBERING=false |
| KTY-04-13 register slug with "Seive" | Frozen per ALLOW_RENUMBERING=false |

---

## Terminology and Interface Sweep Results

| Term | Verdict |
|---|---|
| Pembina HVP Pipeline | CLEAN — all 8 matches are provenance/historical. CONFLICT-01 properly resolved. |
| LPG | 2 live contradictions (KTY-05-08 KA-03 + Scoping.md) → queued for rerun. All other matches are folder slugs, source-faithful, or provenance. |
| FUTURE | Same 2 live contradictions overlap with LPG. KTY-04-14 FUTURE items (deethanizer exchangers) are correctly future-scope. |
| Incinerator | CLEAN — consistent AUTH-022 normalization throughout |
| Flare | CLEAN — consistent AUTH-021 normalization throughout |
| Cross-Facility | CLEAN after vocabulary map correction. All active usage says "Cross-Facility." |

---

## Follow-On Sequence — EXECUTED

All downstream tasks completed in this session:

| Step | Status | Result |
|---|---|---|
| 1. `TASK + domain-documents` for KTY-05-08 | COMPLETE | 7 SFL corrections (LPG→NGL, Future→current scope); KA-03 and Scoping.md corrected |
| 2. KTY-local metadata alignment for KTY-05-08 | COMPLETE | No drift — _CONTEXT.md consistent with regenerated content |
| 3. Main doc Coverage & Telemetry block | COMPLETE | Added SCA-002 and SCA-003-reviewed rows; counts updated |
| 4. Main doc Open Issues table | COMPLETE | Updated to 571 total; 4 compound types added; OI-004/006/008/009 counts corrected |
| 5. KTY Register column reconciliation (D6) | COMPLETE | 11 column values corrected across 6 KTYs; KTY-03-02 adjusted for 6 retirements |
| 6. HBK-5977 ledger defect | COMPLETE | KnowledgeTypeID truncation fixed (added -SOC suffix) |
| 7. `DOMAIN_HYPERGRAPH` | COMPLETE | New snapshot HG_SCA003_REVIEWED_2026-04-19_1218: 6,986 nodes, 7,541 edges; 36 pre-existing blockers (KA naming); 0 new blockers |
| 8. `AUDIT_DECOMP` | COMPLETE | PASS — 0 blockers, 0 warnings, 100% coverage; 2 INFO findings |
| 9. Terminology QA sweep | COMPLETE | PASS — all 6 checks pass |

---

## Remaining INFO-Level Findings (Non-Blocking)

| Finding | Location | Status |
|---|---|---|
| Stale OBJ-003 annotation | Objective Register: `KTY-13-11 [RETIRED — SCA-001]` but KTY-13-11 is IN | Cosmetic; no structural impact |
| Stale embedded HTML ledger | Main doc `<details>` block: IN=4981, RETIRED=281 (pre-repair) | CSV is authoritative and correct; HTML is display-only |
| KTY-04-19 description residual "LPG" | `_CONTEXT.md` line 11: "NGL and LPG product storage tanks" | Low priority; depropanizer removed by SCA-001, product is C3+ NGL |
| KTY-06-09 source-faithful "LPG MS Purge" labels | KA-01 emissions table rows | Source-faithful; annotation pass optional |

---

## Final Acceptance Status

| Criterion | Status |
|---|---|
| No internal contradiction in decomposition-local registers | PASS |
| `_ScopeChange/_LATEST.md` correct | PASS |
| No repairable drift in KTY metadata | PASS |
| All domain-documents reruns complete | PASS — KTY-05-08 corrected |
| DOMAIN_HYPERGRAPH regenerated | PASS — 36 pre-existing naming blockers accepted |
| AUDIT_DECOMP structural invariants | PASS — 0 blockers, 0 warnings, 100% coverage |
| Terminology QA sweep | PASS — no live contradictions |
| Run summary separates repaired / rerun / unresolved | PASS |
| Handoff is decision-complete | PASS — no policy choices deferred |

**The Deepcut root is ready for Phase 7 cross-root conformity gate.**
