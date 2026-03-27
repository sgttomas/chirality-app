# Estimate Summary -- DEL-018-06 Utility Tie-Ins

**RunID:** EST_DEL-018-06_2026-03-26_1759
**Date:** 2026-03-26
**Basis of Estimate:** RATE_TABLE
**Currency:** CAD
**RUN_STATUS:** WARNINGS

---

## Basis of Estimate Used

| Field | Value |
|-------|-------|
| **Primary Method** | RATE_TABLE |
| **Fallback Policy** | ALLOW_ALLOWANCE |
| **Mixed Methods** | TRUE (allowed) |
| **Methods Actually Used** | RATE_TABLE (14 of 26 lines, 54%), ALLOWANCE (12 of 26 lines, 46%) |

Rate table data from Professional_Staff_Rates.csv, Construction_Labour_Rates.csv, Earthwork_Civil_Rates.csv, and Underground_Utility_Rates.csv provides unit rates for staff, trade labour, earthwork, and underground utility line items. Utility service connections (SOW-0080, SOW-0081, SOW-0082) and the new electrical pole/transformer relocation (SOW-0122) are priced as ALLOWANCE items because no provider quotes are available. ALLOW_MIXED_METHODS=TRUE permits this combination.

---

## Total Estimated Cost

| Category | Amount (CAD) | Lines | Notes |
|----------|-------------|-------|-------|
| Professional Services | $6,470.00 | 6 | PM, CPM, Supt, Cost Est, QA/QC, HSE |
| Utility -- Natural Gas (SOW-0080) | $25,000.00 | 1 | Allowance; 2" PVC 50 PSI confirmed |
| Utility -- Electrical (SOW-0081) | $45,000.00 | 1 | Allowance; three-phase |
| Utility -- Communications (SOW-0082) | $8,000.00 | 1 | Allowance |
| **Electrical Pole/Transformer Relocation (SOW-0122)** | **$55,000.00** | **1** | **NEW -- Allowance; Add. 3 Q7** |
| Earthworks | $5,625.00 | 2 | Trenching + backfill (75m assumed) |
| Underground Utilities | $26,250.00 | 4 | Conduit/piping + building penetrations |
| Permits and Admin | $3,000.00 | 2 | Safety Code permits + One-Call |
| Testing and Commissioning | $6,500.00 | 1 | All systems + pole relocation verification |
| Documentation | $4,500.00 | 1 | As-built drawings (expanded for SOW-0122) |
| Construction Labour | $14,755.20 | 6 | Plumber, electrician, operator, labourer + SOW-0122 support |
| **GRAND TOTAL** | **$200,100.20** | **26** | |

---

## Totals by Package

| WBS_PackageID | Currency | Amount_Total | Line Count |
|---|---|---|---|
| PKG-018 | CAD | $200,100.20 | 26 |

## Totals by Deliverable

| WBS_DeliverableID | Name | Currency | Amount_Total | Line Count |
|---|---|---|---|---|
| DEL-018-06 | Utility Tie-Ins | CAD | $200,100.20 | 26 |

## Totals by CBS (Cost Breakdown Structure)

| CBS | Description | Currency | Amount_Total | Line Count |
|---|---|---|---|---|
| CBS-02 | Project Management | CAD | $6,470.00 | 6 |
| CBS-05 | General Construction Labour | CAD | $14,755.20 | 6 |
| CBS-17 | Power Distribution & Equipment | CAD | $55,000.00 | 1 |
| CBS-22 | Earthwork, Surfacing & Landscaping | CAD | $5,625.00 | 2 |
| CBS-23 | Underground Utilities & Site Services | CAD | $26,250.00 | 4 |
| CBS-24 | Utility Connections | CAD | $78,000.00 | 3 |
| CBS-25 | Commissioning, Testing & Inspection | CAD | $6,500.00 | 1 |
| CBS-28 | Permits, Fees & Bonding | CAD | $3,000.00 | 2 |
| CBS-29 | General Requirements & Indirect | CAD | $4,500.00 | 1 |
| **Total** | | **CAD** | **$200,100.20** | **26** |

---

## Cost by SOW Reference

| SOW | Description | Estimated Cost (CAD) | Notes |
|-----|-------------|---------------------|-------|
| SOW-0080 | Natural Gas Tie-In | ~$44,000 | Gas service ($25,000) + proportional share of trenching, piping, labour, permits, inspections |
| SOW-0081 | Electrical Service Tie-In | ~$63,000 | Electrical service ($45,000) + proportional share of trenching, conduit, labour, permits, inspections |
| SOW-0082 | Communication Lines Tie-In | ~$17,000 | Communications ($8,000) + proportional share of trenching, conduit, inspections |
| **SOW-0122** | **Electrical Pole/Transformer Relocation** | **~$59,500** | **NEW: Pole relocation ($55,000) + support labour ($2,240) + proportional share of management, inspections, documentation** |
| Shared | Professional staff, documentation, permits, testing overhead | ~$16,600 | Cross-cutting coordination and admin |

Note: SOW-level breakdown is approximate. Many cost items are shared across multiple systems.

---

## Change vs Prior Estimate

| Metric | Prior (2026-02-27) | Current (2026-03-26) | Delta |
|---|---|---|---|
| Total Amount | $139,480.20 | $200,100.20 | +$60,620.00 (+43.5%) |
| Line Count | 23 | 26 | +3 |
| SOW Items Covered | 3 (SOW-0080, -0081, -0082) | 4 (+ SOW-0122) | +1 |
| Method | PARAMETRIC | RATE_TABLE + ALLOWANCE | Changed per brief |
| RUN_STATUS | WARNINGS | WARNINGS | Unchanged |

The increase is driven primarily by:
1. **SOW-0122 electrical pole/transformer relocation: +$55,000** (new scope, Add. 3 Q7)
2. **SOW-0122 support labour: +$2,240** (electrician + operator support)
3. **Management hours increase: +$880** (CPM, Supt, HSE hours for SOW-0122 coordination)
4. **Commissioning increase: +$1,500** (pole relocation verification)
5. **Documentation increase: +$1,000** (as-built scope expansion)

---

## Key Warnings and Coverage Gaps

1. **Electrical pole/transformer relocation (SOW-0122) is the largest source of uncertainty.** The $55,000 allowance is a mid-range estimate ($35,000-$85,000). Cost depends on: number of poles, transformer size/type, utility provider requirements, and site access conditions. A provider quote should be obtained immediately.

2. **Trench distance is assumed (75m).** Actual distance from utility service points to building is TBD pending civil design (PKG-005) and utility provider confirmation. Cost is linearly sensitive to this distance.

3. **Utility service connection costs are parametric allowances.** No quotes from utility providers are available. The gas ($25,000) and electrical ($45,000) allowances carry LOW confidence.

4. **Transformer ownership is unresolved.** If the electrical transformer is customer-owned rather than utility-owned, add $30,000 to $80,000 to the electrical service cost.

5. **Gas main extension risk.** If the site is far from the nearest gas main, a main extension could add $50,000 to $200,000+. The estimate assumes no main extension is required. Gas supply parameters (2" PVC, 50 PSI) are now confirmed (Add. 3, Q8), reducing sizing uncertainty but not distance risk.

6. **No contingency is included.** Given the number of LOW-confidence items and the new SOW-0122 scope, a 15-25% contingency would be warranted ($30,000-$50,000).
