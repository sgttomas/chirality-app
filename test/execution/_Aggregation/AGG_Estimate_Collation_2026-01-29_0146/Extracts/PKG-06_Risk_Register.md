# Risk Register

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG06_DRAFT_2026-01-28_2333 |
| Estimate Label | PKG06_DRAFT |
| Package Scope | PKG-06 Structural Steelwork |

---

## Contingency Method

**Method:** PCT_BY_BUCKET (percentage by CBS bucket with allowance-heavy adjustment)

**Rationale:** 100% of base estimate is allowance/parametric-based (no vendor quotes or detailed design); contingency percentages elevated above baseline to account for estimate immaturity and scope uncertainty.

**Reference:** Decision D-010; AGENT_ESTIMATING.md STRUCTURE: Fallback Typical Model (contingency defaults).

---

## Contingency Summary

| CBS | Base Amount (CAD) | Allowance Share | Base % | Adjustment | Final % | Contingency (CAD) |
|-----|------------------:|----------------:|-------:|-----------:|--------:|------------------:|
| E | $89,000 | 100% | 10% | +10% | 20% | $17,800 |
| PM | $120,000 | 100% (factor) | 10% | +5% | 15% | $18,000 |
| P | $27,000 | 100% (factor) | 10% | +5% | 15% | $4,100 |
| MAT | $1,301,000 | 100% | 15% | +10% | 25% | $325,300 |
| CD | $611,000 | 100% | 20% | +10% | 30% | $183,300 |
| CI | $115,000 | 100% (factor) | 20% | +10% | 30% | $34,500 |
| COM | $60,000 | 100% (factor) | 25% | +5% | 30% | $18,000 |
| **Total** | **$2,323,000** | | | | | **$601,000** |

**Total Contingency:** $601,000 (26% of base estimate)

---

## Risk Entries

### R-001: Structural Steel Tonnage Uncertainty

**Risk Driver:** Scope / Quantity

**Cause → Consequence:**
- **Cause:** No structural steel design drawings or tonnage estimate available (deliverables DEL-06.01, DEL-06.03 are INITIALIZED with quantities TBD).
- **Consequence:** Tonnage allowance (150 tonnes, Decision D-012) may be ±50% when design is complete, causing $450k-$1.35M variance in structural steel material cost (L006: $900k allowance).

**Affected Buckets:** MAT (structural steel supply), CD (erection labor)

**Suggested Mitigation:**
1. Prioritize structural steel design (DEL-06.01 drawings, DEL-06.03 calculations) to establish tonnage early.
2. Obtain preliminary tonnage estimate from process/equipment layouts (railcar unloading platforms, pipe racks).
3. Request vendor pre-design consultation to validate tonnage assumptions.

**Contingency Handling:** 25% contingency on MAT bucket ($325k) and 30% on CD bucket ($183k) provides buffer for tonnage variance.

---

### R-002: Fabrication and Galvanizing Cost Volatility

**Risk Driver:** Price

**Cause → Consequence:**
- **Cause:** No vendor budgetary quotes for structural steel fabrication or galvanizing; $6,000/tonne rate (Assumption A-006) is a typical BC rate without project-specific validation.
- **Consequence:** Fabrication/galvanizing rates may vary $5,000-$7,500/tonne depending on:
  - Steel complexity (connections, tight tolerances)
  - Galvanizing requirements (hot-dip vs other protective systems)
  - Delivery schedule (expedited vs standard lead time)
  - Market conditions (steel commodity pricing, fabricator capacity)

**Affected Buckets:** MAT (structural steel supply)

**Suggested Mitigation:**
1. Obtain 3 vendor budgetary quotes for fabrication and galvanizing.
2. Lock in steel pricing early if market volatility is anticipated.
3. Consider alternative protective systems (paint vs galvanizing) if cost becomes prohibitive.

**Contingency Handling:** 25% contingency on MAT ($325k) provides $225k buffer on $900k steel material allowance.

---

### R-003: Erection Productivity and Site Access

**Risk Driver:** Productivity / Schedule

**Cause → Consequence:**
- **Cause:** Steel erection productivity (25 hrs/tonne, Assumption A-007) is a typical range without project-specific validation; actual productivity depends on:
  - Site access constraints (active terminal operations, congestion)
  - Crane availability and positioning (shared with other trades)
  - Weather/seasonal constraints (wet season work)
  - Working hours restrictions (noise, terminal operations coordination)
- **Consequence:** Erection hours may vary 20-35 hrs/tonne, causing $285k-$500k variance in erection labor (L007: $356k allowance).

**Affected Buckets:** CD (erection labor), CI (indirect supervision/support)

**Suggested Mitigation:**
1. Develop detailed erection sequence and schedule with site access constraints mapped.
2. Confirm crane availability and capacity (shared resource coordination).
3. Plan for weather/seasonal delays (Fraser Surrey Terminal wet season considerations).
4. Consider modularization or pre-assembly to reduce field labor hours.

**Contingency Handling:** 30% contingency on CD ($183k) and CI ($35k) provides buffer for productivity variance.

---

### R-004: Platform/Gangway Layout and Quantity Variance

**Risk Driver:** Scope / Quantity

**Cause → Consequence:**
- **Cause:** No platform or gangway layout drawings available; handrail (400 m), grating (800 m²), and stairs/gangways (12 items) are rough allowances (Decisions D-013, Assumptions A-009, A-010, A-011).
- **Consequence:** Actual quantities may vary ±30-50% when layout is finalized, affecting:
  - Handrail: $66k-$132k range (vs $88k allowance)
  - Grating: $90k-$216k range (vs $144k allowance)
  - Stairs/gangways: $90k-$270k range (vs $180k allowance)

**Affected Buckets:** MAT (handrail/grating/stairs supply), CD (installation)

**Suggested Mitigation:**
1. Prioritize platform layout design (DEL-06.01) to establish handrail extents and grating areas.
2. Review railcar unloading station count (32 stations) and access requirements to validate stair/gangway count.
3. Obtain vendor standard sizes/pricing for pre-fabricated gangways to refine allowance.

**Contingency Handling:** 25% contingency on MAT and 30% on CD provides buffer for quantity variance (~$100k combined).

---

### R-005: Interface Coordination with Foundations (PKG-05)

**Risk Driver:** Interface / Scope

**Cause → Consequence:**
- **Cause:** Structural steel platforms/pipe racks require foundation support (assumed provided under PKG-05 Concrete Structures, Decision D-007); dependency tracking mode = NOT_TRACKED.
- **Consequence:** If foundation scope/responsibility is unclear or delayed:
  - Steel erection may be delayed waiting for foundations (schedule impact)
  - Foundation loads may not match steel design (re-work risk)
  - Anchor bolt/embedment coordination failures (field modifications)

**Affected Buckets:** PKG-06 CD (potential re-work or delay costs)

**Suggested Mitigation:**
1. Confirm foundation responsibility and scope via cross-package coordination (human coordination outside estimating agent).
2. Establish foundation design interface early (loads, anchor bolt layouts, elevations).
3. Include foundation readiness in steel erection schedule dependencies.

**Contingency Handling:** General contingency on CD/CI provides buffer for minor interface coordination issues; major scope gaps would require estimate revision.

---

### R-006: Pipe Support Coordination with Process Packages

**Risk Driver:** Interface / Scope

**Cause → Consequence:**
- **Cause:** Pipe supports and racks ($65k allowance, Assumption A-012) assumes piping design by others under process packages (PKG-10, PKG-11, etc.); pipe support responsibility may be shared or unclear.
- **Consequence:** If pipe support scope is larger than anticipated or responsibility is ambiguous:
  - PKG-06 pipe support allowance may be insufficient (scope growth)
  - Coordination delays between structural and process disciplines (schedule impact)

**Affected Buckets:** PKG-06 MAT/CD (pipe supports)

**Suggested Mitigation:**
1. Clarify pipe support responsibility in project scope document (structural vs process discipline).
2. Obtain piping layout drawings (process packages) to validate pipe support extents.
3. Coordinate pipe support design early (loads, attachment points, routing).

**Contingency Handling:** 25-30% contingency on MAT/CD provides buffer for moderate pipe support scope variance; significant scope growth would require estimate revision.

---

### R-007: Labor Rate and Equipment Cost Escalation

**Risk Driver:** Price / Schedule

**Cause → Consequence:**
- **Cause:** Pricing date is January 2026; no escalation applied (Decision D-011); if project execution is delayed or extends over multiple years, labor rates and equipment rental costs may increase.
- **Consequence:** If work occurs in 2027 or later, labor/equipment costs may escalate 3-5% per year (typical construction cost inflation).

**Affected Buckets:** CD (labor), CI (supervision), E (engineering labor)

**Suggested Mitigation:**
1. Establish project execution schedule and confirm pricing date validity.
2. If multi-year execution is anticipated, apply escalation factors or provide escalation allowance.
3. Lock in labor agreements or equipment rental rates early if possible.

**Contingency Handling:** Current contingency does not explicitly cover escalation; if escalation is required, set `escalation_mode: EXPLICIT` in config and re-run estimate.

---

### R-008: QA/QC and Weld Inspection Scope Variance

**Risk Driver:** Scope / Productivity

**Cause → Consequence:**
- **Cause:** Weld inspection hours (200 hrs, Assumption A-015) are estimated without connection count or inspection plan; actual inspection scope depends on:
  - Number of field welds (vs shop-welded connections)
  - Code requirements (CSA W59 or equivalent; extent of UT/MT NDE)
  - Inspection hold points and acceptance criteria
- **Consequence:** Inspection hours may vary 150-300 hrs, causing $16.5k-$33k variance (vs $22k allowance).

**Affected Buckets:** CD (inspection labor)

**Suggested Mitigation:**
1. Provide weld inspection plan and hold points (tied to DEL-06.02 specification and DEL-06.05 records).
2. Confirm code requirements and NDE extent early (structural design basis).
3. Coordinate inspector availability and schedule to avoid delays.

**Contingency Handling:** 30% contingency on CD ($183k) provides buffer for moderate inspection scope variance.

---

## Risk Summary by Category

| Risk Category | Number of Risks | Affected Base $ (CAD) | Mitigation Priority |
|---------------|----------------:|----------------------:|---------------------|
| Scope / Quantity | 3 (R-001, R-004, R-008) | $1,500,000 | HIGH (affects 65% of base) |
| Price | 2 (R-002, R-007) | $1,000,000 | MEDIUM (vendor quotes reduce) |
| Productivity / Schedule | 2 (R-003, R-007) | $500,000 | MEDIUM (site-specific data reduces) |
| Interface / Scope | 2 (R-005, R-006) | $200,000 | MEDIUM (coordination clarifies) |

---

## Contingency Allocation Rationale

**Total Contingency:** $601,000 (26% of $2,323,000 base)

**Justification:**
1. **Estimate Maturity:** 100% allowance/parametric-based (no vendor quotes, no detailed design) → elevated contingency required.
2. **Top Risks:** Structural steel tonnage uncertainty (R-001) and fabrication cost volatility (R-002) represent ~$900k of base estimate (39%) with ±25-50% variance potential.
3. **Allowance-Heavy Adjustment:** Per AGENT_ESTIMATING.md fallback model, contingency % increased by +5-10% for buckets with 100% allowance share.
4. **Comparison to Typical Ranges:**
   - E (Engineering): 20% (vs typical 10%) — justified by lack of design hours validation
   - MAT (Materials): 25% (vs typical 15%) — justified by no vendor quotes and tonnage uncertainty
   - CD (Construction Directs): 30% (vs typical 20%) — justified by productivity/site access unknowns
   - CI/COM: 30% (vs typical 20-25%) — justified by factor-based derivation without schedule validation

**Confidence Statement:** At 26% contingency, estimate provides reasonable buffer for allowance-based scope; however, contingency does NOT cover:
- Major scope additions (e.g., doubling of tonnage due to design changes)
- Significant market escalation (if work deferred to future years)
- Interface scope gaps requiring new work packages

---

**Risk Register compiled:** 2026-01-28 23:33
**Contingency Method Reference:** Decision_Log.md (D-010); AGENT_ESTIMATING.md STRUCTURE (Fallback Typical Model)
