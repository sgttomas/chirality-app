# Risk Register — PKG-25 Communications & IT

**Snapshot ID:** EST_PKG25_DRAFT_2026-01-29_0004
**Package:** PKG-25 Communications & IT
**Date:** 2026-01-29

---

## Purpose

This register identifies risks affecting the estimate accuracy and provides contingency rationale. Risks are categorized by driver and linked to affected cost buckets.

---

## R-2501: Network Architecture Undefined

**Risk Driver:** Scope uncertainty
**Cause:** Network design (DEL-25.01) not complete; bandwidth requirements, topology, redundancy, port counts TBD
**Consequence:** Equipment specifications and quantities unknown; cannot size switches, cabling, patch panels accurately
**Affected Buckets:** MAT (network equipment, cabling), CD (installation scope)
**Probability:** High (design incomplete)
**Impact:** High (±30-50% equipment cost; ±20-30% cabling cost)
**Suggested Mitigation:**
- Complete network architecture study and requirements definition
- Establish port count matrix (workstations, devices, control points)
- Define bandwidth requirements and future growth projections
- Obtain preliminary equipment specifications from vendors

**Contingency Handling:** Reflected in MAT contingency (25%) and CD contingency (30%)

**Related Assumptions:** A-2501, A-2502, A-2503, A-2512

---

## R-2502: No Vendor Quotes Available

**Risk Driver:** Pricing uncertainty
**Cause:** No vendor budgetary quotes for network equipment, cabling materials, installation labor
**Consequence:** Pricing based on allowances and industry assumptions; actual pricing may vary significantly
**Affected Buckets:** MAT (equipment and materials), CD (installation)
**Probability:** Certain (no quotes obtained)
**Impact:** Medium-High (±20-40% pricing variance typical at Class 5 maturity)
**Suggested Mitigation:**
- Obtain budgetary quotes from multiple network equipment vendors (Cisco, Juniper, HPE, Aruba)
- Obtain quotes from structured cabling installers
- Develop project-specific rate tables for labor and materials
- Validate assumptions against local market rates

**Contingency Handling:** Primary driver for elevated contingency rates (MAT 25%, CD 30%)

**Related Assumptions:** A-2509, A-2510, A-2511, A-2512, A-2513

---

## R-2503: Technology Selection Unknowns

**Risk Driver:** Scope/qty uncertainty
**Cause:** Cable category (Cat 6 vs Cat 6A), fiber grade (OM3 vs OM4), PoE requirements, connector types TBD
**Consequence:** Material costs may vary ±20-40% depending on selections
**Affected Buckets:** MAT (cables, equipment)
**Probability:** High (specifications not finalized per DEL-25.02)
**Impact:** Medium (Cat 6A premium ~30-50% over Cat 6; PoE switches premium ~30-40%)
**Suggested Mitigation:**
- Complete DEL-25.02 Communications Technical Specification
- Define performance requirements (bandwidth, distance, future-proofing)
- Conduct life-cycle cost analysis for technology options
- Obtain vendor pricing for each option

**Contingency Handling:** Reflected in MAT contingency (25%)

**Related Assumptions:** A-2502 (Cat 6/6A), A-2501 (fiber grades), A-2503 (PoE capability)

---

## R-2504: Building Layouts and TR Locations Unavailable

**Risk Driver:** Scope/qty uncertainty
**Cause:** Building layouts (PKG-21) not complete; telecommunications room (TR) locations, equipment room (ER) location TBD
**Consequence:** Cable routing distances and quantities unknown; cannot accurately estimate cabling materials and installation labor
**Affected Buckets:** MAT (cable quantities), CD (installation labor)
**Probability:** High (PKG-21 in early design phase)
**Impact:** Medium (±25-40% cable quantity variance typical)
**Suggested Mitigation:**
- Coordinate with PKG-21 Building Structures to obtain preliminary layouts
- Coordinate with PKG-22 Building Interior & MEP for equipment room locations
- Develop conceptual cable routing plan
- Establish telecommunications room (TR) count and locations

**Contingency Handling:** Reflected in MAT and CD contingency (25-30%)

**Related Assumptions:** A-2515 (TR locations), A-2501 (fiber routing), A-2502 (copper routing)

---

## R-2505: Integration with PKG-19 Control Systems Undefined

**Risk Driver:** Interface uncertainty
**Cause:** Integration requirements with PKG-19 Control Systems not defined; network segmentation, gateway devices, interface protocols TBD
**Consequence:** Integration scope and equipment requirements unknown; commissioning complexity TBD
**Affected Buckets:** MAT (interface equipment), COM (integration testing)
**Probability:** Medium (coordination in progress)
**Impact:** Low-Medium (interface equipment cost likely <$10k; commissioning impact <20%)
**Suggested Mitigation:**
- Coordinate with PKG-19 to define network integration architecture
- Clarify responsibilities for gateway devices, firewalls, network segmentation
- Define integration testing requirements and acceptance criteria
- Update DEL-25.01 and DEL-25.04 with integration scope

**Contingency Handling:** Reflected in COM contingency (30%)

**Related Assumptions:** A-2516 (integration scope), A-2517 (commissioning scope)

---

## R-2506: Quantities TBD (Physical Infrastructure)

**Risk Driver:** Qty uncertainty
**Cause:** Fiber cable lengths, copper cable lengths, port counts, patch panel quantities, TR counts all TBD pending design
**Consequence:** Cannot create unit-rate-based QTO; forced to use lump-sum allowances; estimate accuracy limited
**Affected Buckets:** MAT (all cabling and equipment), CD (all installation)
**Probability:** Certain (design not complete)
**Impact:** High (Class 5 estimate accuracy -30% / +50%)
**Suggested Mitigation:**
- Complete DEL-25.01 Communications Design Drawing Set
- Develop cable schedules (fiber and copper) with lengths and quantities
- Develop equipment schedules (switches, patch panels) with counts and specifications
- Transition from allowances to unit-rate pricing
- Re-run estimate to upgrade maturity to Class 4 or Class 3

**Contingency Handling:** Primary driver for overall contingency rate (28% blended)

**Related Assumptions:** A-2501 through A-2506, A-2509 through A-2513

---

## R-2507: Site Access and Terminal Coordination Constraints

**Risk Driver:** Productivity/schedule
**Cause:** Active marine terminal operations; security clearances required; work permits; escort requirements; operational restrictions
**Consequence:** Productivity may be reduced 10-20%; after-hours/weekend work may be required (10-20% premium); delays possible
**Affected Buckets:** CD (installation productivity), CI (coordination overhead)
**Probability:** High (terminal operations ongoing)
**Impact:** Medium (10-20% CD cost increase potential)
**Suggested Mitigation:**
- Conduct site visit and coordinate with Fraser Surrey Terminal operations
- Develop site-specific safety and access plan
- Obtain security clearance requirements and lead times
- Define work hour restrictions and permit procedures
- Plan construction sequencing to minimize operational disruption
- Budget for after-hours work if necessary

**Contingency Handling:** Reflected in CD and CI contingency (30%)

**Related Assumptions:** A-2507 (site conditions), A-2514 (terminal constraints)

---

## R-2508: Escalation Exposure

**Risk Driver:** Price
**Cause:** No escalation applied; estimate in January 2026 dollars; project duration 2-3 years
**Consequence:** Escalation 3-6% annually could add $34k-$100k (6-18% of base) to project cost
**Affected Buckets:** All (escalation applies to all CBS buckets)
**Probability:** High (multi-year project)
**Impact:** Medium (5-20% cost increase over project duration)
**Suggested Mitigation:**
- Obtain project schedule and cash flow curve
- Apply escalation factors by CBS and year
- Update `_CONFIG.md` escalation_mode=EXPLICIT
- Obtain labor agreement escalation rates
- Obtain material escalation projections from vendors
- Re-run estimate with escalation included

**Contingency Handling:** NOT reflected in contingency (escalation excluded per D-2509); separate risk item

**Related Decisions:** D-2509 (escalation mode = NONE)

---

## Risk Summary

| Risk ID | Risk Driver | Probability | Impact | Affected Buckets | Contingency Coverage |
|---------|-------------|-------------|--------|------------------|----------------------|
| R-2501 | Scope | High | High | MAT, CD | Partial (MAT 25%, CD 30%) |
| R-2502 | Price | Certain | Med-High | MAT, CD | Primary driver (MAT 25%, CD 30%) |
| R-2503 | Scope/Qty | High | Medium | MAT | Partial (MAT 25%) |
| R-2504 | Scope/Qty | High | Medium | MAT, CD | Partial (MAT 25%, CD 30%) |
| R-2505 | Interface | Medium | Low-Med | MAT, COM | Partial (COM 30%) |
| R-2506 | Qty | Certain | High | All | Primary driver (28% blended) |
| R-2507 | Productivity | High | Medium | CD, CI | Partial (CD 30%, CI 30%) |
| R-2508 | Price | High | Medium | All | NOT covered (escalation excluded) |

**Overall Risk Profile:** High (conceptual scope; no quotes; quantities TBD; site constraints)

**Contingency Adequacy:** Adequate for Class 5 estimate maturity; contingency covers scope/qty/price uncertainty but NOT escalation

**Recommended Actions:**
1. **High Priority:** Obtain vendor quotes (mitigates R-2502)
2. **High Priority:** Complete network architecture design (mitigates R-2501, R-2503, R-2506)
3. **High Priority:** Coordinate building layouts and TR locations (mitigates R-2504, R-2506)
4. **Medium Priority:** Coordinate PKG-19 integration requirements (mitigates R-2505)
5. **Medium Priority:** Develop site access plan (mitigates R-2507)
6. **Medium Priority:** Apply escalation to estimate (addresses R-2508)

---

**Risk Register Prepared By:** Estimating Agent
**Date:** 2026-01-29
**Status:** Complete
