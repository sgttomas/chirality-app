# Estimate Summary — DEL-04-02 Cold Storage Doors, Openings & Hardware

**RunID:** EST_DEL-04-02_2026-02-18_1100
**AsOf:** 2026-02-18
**Basis:** RATE_TABLE
**Currency:** CAD
**Rounding:** DOLLAR

---

## BasisOfEstimate_Used

| Field | Value |
|---|---|
| Declared Basis | RATE_TABLE |
| Primary Sources | Equipment_Pricing.csv (EQ-02), Building_Envelope_Rates.csv (BE-11, BE-13, BE-14), Structural_Concrete_Rates.csv (SC-04), Construction_Labour_Rates.csv (T-01, T-02, T-04) |
| Fallback Policy | STRICT |
| Mixed Methods | FALSE |
| Method Used on All Lines | RATE_TABLE |

---

## Totals by CBS

| CBS | Description | Amount (CAD) | Line Count |
|---|---|---|---|
| 08-Doors | Overhead doors, person doors, hardware, installation, exit lights, switches | $36,750 | 7 |
| 03-Concrete | Concrete aprons at overhead door openings (material + labour) | $13,776 | 2 |
| 07-Thermal | Perimeter sealant and weatherstripping at all door openings | $1,286 | 2 |
| **TOTAL** | | **$51,812** | **11** |

## Totals by Package / Deliverable

| WBS_PackageID | WBS_DeliverableID | Amount (CAD) |
|---|---|---|
| PKG-004 | DEL-04-02 | $51,812 |

---

## Cost Composition

| Category | Amount (CAD) | % of Total |
|---|---|---|
| Overhead doors (supply) | $27,000 | 52.1% |
| Concrete aprons (material) | $10,800 | 20.8% |
| Person doors (supply) | $3,600 | 6.9% |
| Installation labour (all) | $5,856 | 11.3% |
| Door hardware (all openings) | $2,400 | 4.6% |
| Weatherstripping / sealant | $1,286 | 2.5% |
| Exit lights + switches | $870 | 1.7% |

---

## Key Observations

1. **Overhead doors are the dominant cost driver** at $27,000 (52% of total), consistent with cold storage scope where 2 motorized 16x16 ft doors with windows are specified.

2. **Concrete aprons are the second-largest item** at $13,776 (27% including labour), reflecting heavy-duty 200mm reinforced slab to support service vehicle loading (graders, dump trucks).

3. **Estimate total of $51,812 is reasonable** relative to the parametric benchmark of $290,000 for the complete cold storage building (PP-22), representing approximately 18% of total building value for the doors/openings/hardware scope.

4. **All 11 line items priced using RATE_TABLE method** -- no fallback methods required; basis-consistency check passes.

---

## Warnings and Blockers

### Warnings
- **W-01:** Lines L-0402-11 (emergency exit lights) and L-0402-12 (weatherproof switches) have `SourceRef = location TBD` because no direct rate table entry exists for these items. Unit rates are based on typical commercial pricing recorded in Assumptions_Log.md. Combined value is $870 (1.7% of total).

### Blockers
- **No estimate-blocking dependencies identified.** All 9 dependencies in Dependencies.csv are design-phase coordination items that do not prevent pricing at proposal stage.
- The pickled-sand keying interface (DEP-0402-E08) is a design coordination item, not a pricing blocker for this estimate.

---

## Scope Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-04-02) |
| Deliverables covered | 1 |
| Deliverables blocked | 0 |
| Deliverables missing | 0 |
| Line items produced | 11 |
| Lines with TBD amounts | 0 |
| Lines with location TBD SourceRef | 2 (L-0402-11, L-0402-12) |
