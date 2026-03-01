# Estimate Summary — EST_DEL-011-06_2026-02-27_0600

## Basis of Estimate

| Field | Value |
|---|---|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **Scope** | DEL-011-06 — Service Pit/Trench |
| **Package** | PKG-011 — Building Structure & Envelope |
| **Run Timestamp** | 2026-02-27T06:00:00-07:00 |

All pricing in this estimate is derived from parametric rates and assumptions. No quotes or historical actuals are available. Pit dimensions are assumed (12m L x 1.5m W x 1.5m D) based on typical heavy-equipment maintenance pit geometry; actual dimensions are TBD pending IFC structural drawings (DEL-002-06) and Owner equipment fleet data from Camrose County.

---

## Total by Deliverable

| WBS_DeliverableID | Deliverable Name | Amount (CAD) | Line Count |
|---|---|---|---|
| DEL-011-06 | Service Pit/Trench | **$97,160** | 19 |

---

## Total by CBS Category

| CBS | Description | Amount (CAD) | Line Count | % of Total |
|---|---|---|---|---|
| CONCRETE | Walls, floor slab, formwork, rebar, stairs, cold-weather protection | $53,210 | 6 | 54.8% |
| SAFETY | Railings, grating/cover, excavation safety measures | $12,995 | 3 | 13.4% |
| LABOUR | Construction labour — concrete placement and finishing | $8,400 | 1 | 8.6% |
| MEP_ROUGHIN | Ventilation, lighting, and floor drain rough-in provisions | $6,300 | 3 | 6.5% |
| MANAGEMENT | Project management and supervision | $5,640 | 1 | 5.8% |
| QA_QC | Concrete testing, as-built survey | $4,000 | 2 | 4.1% |
| FINISHES | Pit interior lining and finishing | $2,880 | 1 | 3.0% |
| WATERPROOFING | Damp-proofing at pit base and wall/slab interface | $2,520 | 1 | 2.6% |
| EARTHWORKS | Excavation of below-grade pit void | $1,215 | 1 | 1.3% |
| **TOTAL** | | **$97,160** | **19** | **100.0%** |

---

## Key Warnings and Coverage Gaps

1. **Pit dimensions are ASSUMED.** All quantities (excavation, concrete, formwork, rebar, waterproofing, lining, railings, grating) are derived from an assumed pit geometry of approximately 12m x 1.5m x 1.5m deep. These will change when IFC structural drawings (DEL-002-06) are issued and Owner equipment fleet data is confirmed. This is the single largest source of estimate uncertainty.

2. **No IFC structural drawings available.** Structural details, concrete mix design, reinforcing schedule, and interface details are all TBD. The concrete CBS category ($53,210 = 54.8% of total) is particularly sensitive to design changes.

3. **Several design decisions are unresolved** per Guidance Conflict Table:
   - C-011-06-01: Pit dimensions (depth, width, length)
   - C-011-06-02: Ventilation method (dedicated vs. integrated)
   - C-011-06-03: Floor drainage routing
   - C-011-06-04: Floor drainage scope boundary (this deliverable vs. PKG-014)

4. **Waterproofing, finishes, MEP rough-in, and excavation safety** have no direct price source support. These are parametric assumptions with LOW confidence.

5. **Provenance completeness is 58% overall.** 11 of 19 lines have direct price source references; 8 lines rely on parametric assumptions without direct rate source support.

6. **Cover/grating system type is TBD.** The estimate assumes removable steel bar grating at $250/m2. If solid steel plate covers are specified, the rate may increase significantly.

7. **Cold-weather concrete protection** is included as a $2,000 allowance. This may not apply if concrete is placed during warm months, or may be insufficient if extended cold-weather protection is needed.

---

## Estimate Confidence Assessment

| Aspect | Rating | Notes |
|---|---|---|
| Quantity certainty | LOW | All quantities derived from assumed dimensions; TBD pending IFC drawings |
| Rate quality | MEDIUM | Primary concrete rates from Structural_Concrete_Rates.csv (PARAMETRIC, MEDIUM confidence); several items use unsupported assumptions |
| Scope completeness | MEDIUM | All identified scope items from the four documents are included; unresolved scope boundaries exist for drainage |
| Overall confidence | LOW-MEDIUM | Suitable for budget planning; not suitable for firm bid pricing without IFC drawings |
