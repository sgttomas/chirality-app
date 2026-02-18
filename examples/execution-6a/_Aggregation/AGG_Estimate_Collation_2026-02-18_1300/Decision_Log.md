# Decision Log -- AGG_Estimate_Collation_2026-02-18_1300

## DEC-AGG-001: DEL-05-05 Dual Scenario Treatment

**Decision:** Both DEL-05-05 line items (L-05-05-01 non-illuminated $12,000 and L-05-05-02 illuminated $22,000) are preserved in Project_Detail.csv. The primary scenario (non-illuminated, $12,000) is used in project-level totals and option summaries. The alternate (illuminated, $22,000) is noted but excluded from summation to avoid double-counting.

**Rationale:** The source estimate snapshot (EST_DEL-05-05_2026-02-18_1800) Summary.md explicitly states "The two scenarios are mutually exclusive (either/or), not additive." The brief cross-check value for DEL-05-05 is $12,000, confirming the primary scenario is the default for aggregation.

**Impact:** Project totals use $12,000 for DEL-05-05. If illuminated signage is elected, add $10,000 to totals. Both scenarios remain in Project_Detail.csv for audit.

---

## DEC-AGG-002: TBD Line Items Excluded from Totals

**Decision:** 12 line items across DEL-01-02 (1), DEL-01-03 (2), DEL-01-06 (2), and DEL-02-01 (7) have Amount=TBD. These are included in Project_Detail.csv but excluded from monetary totals.

**Rationale:** The source snapshots set Amount=TBD because pricing evidence was unavailable under their declared FALLBACK_POLICY=STRICT. The aggregation agent cannot fabricate prices. The items are preserved for traceability and to indicate scope that requires pricing in future iterations.

**Impact:** Base price excludes these 12 items. When pricing evidence becomes available, the affected deliverables should be re-estimated and a new aggregation run performed.

---

## DEC-AGG-003: Cash Allowance Reporting

**Decision:** The utility tie-in allowance ($35,000, DEL-03-04 line L-0304-12 per UU-12) is included in the PKG-003 subtotal and therefore in the Base Price. It is separately called out in the project summary for visibility. The FF&E allowance ($20,000, DEL-05-07) is in PKG-005 and NOT in the Base Price.

**Rationale:** The brief Section 7.2 specifies "Cash Allowances (separately carried)" with both items listed. However, the DEL-03-04 utility tie-in is a line item within a base-scope deliverable (PKG-003), while the FF&E is an optional item (PKG-005). The brief's package structure determines base vs optional classification. Both are separately identified for bidding transparency.

**Impact:** The $35,000 appears in both the Base Price total and the Cash Allowances separately-carried note. This is not double-counting; it is dual reporting (inclusion + visibility).

---

## DEC-AGG-004: No Prior Pipeline Snapshot

**Decision:** This is the first run for PIPELINE_ID=PENHOLD_PSB_6a. No prior `_LATEST.md` pointer exists for this pipeline. All 30 deliverables are treated as new additions (no merge logic required).

**Rationale:** Incremental pipeline behavior per PROTOCOL Function 4 requires checking for prior pipeline state. None exists. Clean-start.

**Impact:** None. Future runs under this pipeline ID will incorporate this snapshot as the baseline.

---

## DEC-AGG-005: Extracts Directory

**Decision:** Raw extract files are not duplicated into the `Extracts/` directory. The Source_Index.csv provides full paths to all source artifacts. Duplicating 330 files (30 snapshots x 11 artifact types) into Extracts/ would approximately double storage without adding audit value, since all source snapshots are immutable and co-located under `_Estimates/`.

**Rationale:** The PROTOCOL requires `Extracts/` to exist for audit. The directory is created (empty) and Source_Index.csv serves as the authoritative path index. Source artifacts remain at their original locations and are not modified.

**Impact:** Auditors should use Source_Index.csv to locate raw source artifacts under `_Estimates/`.
