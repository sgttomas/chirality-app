# Summary — EST_DEL-008-04_2026-02-27_0700

## Basis of Estimate

| Field | Value |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| CURRENCY | CAD |
| FALLBACK_POLICY | ALLOW_PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE |
| Scope | DEL-008-04 As-Built Survey |
| Package | PKG-008 Geotechnical Investigation & Surveying |

The estimate is based on parametric hour estimates for professional staff roles priced at rates from Professional_Staff_Rates.csv. Project Manager (6 hr) and Cost Estimator (4 hr) hours are sourced from Level_of_Effort.csv. Surveyor (R-21) hours (60 hr total) are parametrically estimated because the LOE source shows "TBD" for this role on DEL-008-04; the FALLBACK_POLICY=ALLOW_PARAMETRIC authorizes this approach.

## Totals

### By Package / Deliverable

| WBS_PackageID | WBS_DeliverableID | CBS | Amount (CAD) | Line Count |
|---|---|---|---|---|
| PKG-008 | DEL-008-04 | Professional Services | 9,930 | 13 |
| **Total** | | | **9,930** | **13** |

### By Role

| Role | RoleID | Hours | Rate (CAD/hr) | Amount (CAD) |
|---|---|---|---|---|
| Surveyor | R-21 | 60 | 140 | 8,400 |
| Project Manager | R-01 | 6 | 165 | 990 |
| Cost Estimator | R-08 | 4 | 135 | 540 |
| **Total** | | **70** | | **9,930** |

### By Phase (Surveyor hours only)

| Phase | Description | Hours | Amount (CAD) |
|---|---|---|---|
| Step 1 | Pre-Field Preparation | 8 | 1,120 |
| Step 2 | Field Survey | 17 | 2,380 |
| Step 3 | Office Reduction and Drawing Preparation | 28 | 3,920 |
| Step 4 | Internal QA Review | 3 | 420 |
| Step 5 | Submission to Owner and Revision Cycle | 4 | 560 |
| **Surveyor Total** | | **60** | **8,400** |

**Note:** Phase subtotals include only Surveyor (R-21) hours. PM and CE hours are project-level overhead allocated across all phases. Step 6 (Final Deadline Check) is an administrative checkpoint with no incremental cost.

### Comparison to DEL-008-03 (Construction Survey)

| Metric | DEL-008-03 | DEL-008-04 | Ratio |
|---|---|---|---|
| Surveyor hours | 178 | 60 | 0.34x |
| Total amount (CAD) | 26,450 | 9,930 | 0.38x |

The as-built survey is approximately one-third the effort of the construction survey. This is reasonable because: (a) the as-built survey is a single post-construction field event versus the construction survey's multiple visits spanning the entire construction phase; (b) as-built survey uses control already established by DEL-008-03; (c) no staking or grade control activities are required; (d) the primary effort is in office drawing preparation and reporting rather than field work.

## Key Warnings and Coverage Gaps

1. **Surveyor hours are fully parametric.** The Level_of_Effort.csv source provides "TBD" for Surveyor hours on DEL-008-04. All 60 Surveyor hours are agent-estimated based on scope analysis of the four deliverable documents. Confidence is MEDIUM overall.

2. **Deliverable format is TBD (GAP-002).** The estimate assumes a combined CAD + PDF deliverable, which is the most likely scenario per Guidance trade-off analysis. If PDF-only is acceptable, drawing preparation effort (DL-007) could decrease by approximately 4 hours ($560). If full CAD with additional data exports is required, effort could increase by approximately 4 hours ($560).

3. **No equipment costs included.** The estimate covers professional staff time only. Survey equipment (total station, GNSS, levels) is assumed included in the Surveyor's hourly rate. If equipment is priced separately, the estimate will understate total cost.

4. **No travel/mobilization costs.** A single mobilization to the WDMLRL site (SW 14-44-21-W4, ~30 km south of Camrose) is required for field work. If a separate mobilization charge applies, it is not included.

5. **No field technician / survey assistant hours.** The rate table includes only the Surveyor (R-21) role. If a two-person survey crew is required, actual field cost may be higher.

6. **One revision cycle assumed.** ITEM-011 / DL-011 includes one round of Owner review comments and revision. If multiple revision cycles are required, additional Surveyor hours would be needed.

7. **Accuracy standard and conformance tolerance are TBD.** Per Guidance GAP-001 and GAP-004, these affect the rigor of the IFC comparison (Step 3.4) but do not materially affect the estimated effort unless the Owner requires a significantly more rigorous verification process.
