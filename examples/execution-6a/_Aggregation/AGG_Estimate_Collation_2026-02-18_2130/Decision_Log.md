# Decision Log -- AGG_Estimate_Collation_2026-02-18_2130

## Decisions Carried Forward from Prior Snapshot

### DEC-AGG-001: DEL-05-05 Dual Scenario Treatment

**Decision:** Both DEL-05-05 line items (L-05-05-01 non-illuminated $12,000 and L-05-05-02 illuminated $22,000) are preserved in Project_Detail.csv. The primary scenario (non-illuminated, $12,000) is used in project-level totals and option summaries. The alternate (illuminated, $22,000) is noted but excluded from summation to avoid double-counting.

**Rationale:** Unchanged from prior snapshot.

---

### DEC-AGG-003: Cash Allowance Reporting

**Decision:** The utility tie-in allowance ($35,000, DEL-03-04 line L-0304-12 per UU-12) is included in the PKG-003 subtotal and therefore in the Base Price. It is separately called out in the project summary for visibility. The FF&E allowance ($20,000, DEL-05-07) is in PKG-005 and NOT in the Base Price.

**Rationale:** Unchanged from prior snapshot.

---

### DEC-AGG-005: Extracts Directory

**Decision:** Raw extract files are not duplicated into the `Extracts/` directory. Source_Index.csv provides full paths to all source artifacts.

**Rationale:** Unchanged from prior snapshot.

---

## New Decisions for This Snapshot

### DEC-AGG-006: Incremental Merge of 4 Updated Deliverables

**Decision:** Replace all rows for DEL-01-02, DEL-01-03, DEL-01-06, and DEL-02-01 in Project_Detail.csv with rows from the updated estimate snapshots (timestamp _2100). Carry forward all other deliverables unchanged from prior snapshot.

**Rationale:** The 4 updated snapshots resolve all 12 previously-TBD line items. The updates supersede the prior snapshots for these deliverables. The row count remains 266 (21 old rows replaced with 21 new rows). No structural changes to the collation.

**Impact:** Base price increases by $192,629 (from $6,633,217 to $6,825,846). TBD count decreases from 12 to 0.

---

### DEC-AGG-007: TBD Line Items Fully Resolved

**Decision:** DEC-AGG-002 (TBD Line Items Excluded from Totals) from the prior snapshot is now obsolete. All 12 previously-TBD line items have been resolved with pricing. No TBD exclusions remain.

**Rationale:** The 4 updated estimate snapshots provide pricing for all previously-unpriced items via RATE_TABLE (7 lines using Interior_Architectural_Rates.csv) and ALLOWANCE (5 lines using parametric estimates).

**Impact:** All 266 line items now contribute to monetary totals. No items are excluded due to TBD status.

---

### DEC-AGG-008: Method Mix Update for Resolved TBD Lines

**Decision:** The 12 resolved lines are classified as follows:
- 7 lines use RATE_TABLE method (DEL-02-01 interior finishes: partitions, floor, ceiling, accessibility, signage, paint, design fees)
- 5 lines use ALLOWANCE method (DEL-01-02 software, DEL-01-03 training + PPE, DEL-01-06 temp facilities + cleaning)

The ALLOWANCE lines were previously TBD under STRICT fallback policy. They are now priced via parametric allowances authorized by the ORCHESTRATOR TBD resolution pass (DEC-EST-005 in the source snapshots).

**Rationale:** The source estimates document the method change and authorization. The aggregation preserves the Method field as declared in the source Detail.csv.

**Impact:** Method mix shifts slightly: RATE_TABLE increases by 7 lines, ALLOWANCE increases by 5 lines, TBD decreases by 12 lines. Total priced amount increases accordingly.
