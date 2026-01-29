# Risk Register — PKG-24 Security Systems Estimate

**Snapshot ID:** EST_PKG24_DRAFT_2026-01-28_0030
**Date:** 2026-01-28

This register documents risks affecting the PKG-24 Security Systems estimate and their impact on cost uncertainty.

---

## R-001: Equipment Pricing Uncertainty (No Vendor Quotes)

**Risk Driver:** Pricing uncertainty
**Cause:** No vendor quotes or rate tables available; 100% allowance-based equipment pricing
**Consequence:** Actual equipment costs may vary significantly from allowance estimates
**Affected Buckets:** MAT ($359k base), CD installation ($244k base)
**Probability:** High (no quotes obtained)
**Impact:** Medium to High (equipment is 43% of base estimate)
**Suggested Mitigation:**
- Obtain budgetary quotes from 2-3 security system integrators
- Request equipment pricing for CCTV cameras, NVR, VMS, access control components
- Obtain turnkey system pricing for comparison
**Contingency Handling:** MAT bucket contingency 25% addresses pricing uncertainty

---

## R-002: Camera Quantity Uncertainty (Coverage Design Incomplete)

**Risk Driver:** Scope/quantity uncertainty
**Cause:** Camera count based on engineering judgment; DEL-24.01 coverage design not complete
**Consequence:** Actual camera count may range from 15-30 units (vs 21 estimated)
**Affected Buckets:** MAT (cameras), CD (installation), possibly CI/PM/COM
**Probability:** High (design incomplete)
**Impact:** Medium (camera equipment + installation is ~$117k or 14% of base)
**Sensitivity:**
- -25% cameras (16 total): -$74k base, -$96k total
- +25% cameras (26 total): +$78k base, +$102k total
**Suggested Mitigation:**
- Complete DEL-24.01 coverage analysis with camera placement optimization
- Validate coverage requirements with Employer
- Consider phased deployment (initial coverage + future expansion capability)
**Contingency Handling:** MAT and CD bucket contingencies (25-30%) address quantity uncertainty

---

## R-003: Access Control Point Quantity Uncertainty

**Risk Driver:** Scope uncertainty
**Cause:** Access control point count based on assumption; DEL-24.01 layout not complete
**Consequence:** Actual controlled door/gate count may range from 8-18 (vs 12 estimated)
**Affected Buckets:** MAT (readers, controllers, door hardware), CD (installation)
**Probability:** Medium (typical access control scope for industrial facility)
**Impact:** Low to Medium (access control equipment + installation is ~$71k or 8.5% of base)
**Sensitivity:**
- -33% doors (8 total): -$19k base
- +50% doors (18 total): +$29k base
**Suggested Mitigation:**
- Complete DEL-24.01 access control layout with Employer input on security zoning
- Clarify operational access control philosophy (perimeter only vs full facility)
**Contingency Handling:** MAT and CD bucket contingencies address quantity uncertainty

---

## R-004: Underground Conduit Routing and Coordination

**Risk Driver:** Interface/coordination complexity
**Cause:** Conduit routing TBD; must coordinate with PKG-03 underground utilities, PKG-17 electrical
**Consequence:** Underground conduit installation may require more trenching/boring than estimated if coordination opportunities limited
**Affected Buckets:** CD (conduit installation $95k)
**Probability:** Medium (coordination complexity typical on industrial projects)
**Impact:** Medium (conduit installation is 11% of base)
**Suggested Mitigation:**
- Early coordination with PKG-03 for shared trench opportunities
- Develop integrated underground routing plan
- Consider overhead routing alternatives where feasible
**Contingency Handling:** CD bucket contingency 30% addresses coordination risk

---

## R-005: Coastal Marine Environment Equipment Durability

**Risk Driver:** Environmental conditions
**Cause:** Coastal marine environment (salt spray, humidity, corrosion) requires premium equipment ratings
**Consequence:** Equipment failures or premature degradation if inadequate environmental protection; may require equipment upgrades
**Affected Buckets:** MAT (equipment specifications)
**Probability:** Medium (environmental conditions known; premium equipment specified in allowances)
**Impact:** Medium (equipment replacement/upgrade cost; already reflected in unit cost allowances with 15-30% premium)
**Suggested Mitigation:**
- Specify IP66/IP67 minimum for outdoor equipment
- Require marine-grade materials (stainless steel, powder-coated aluminum)
- Include corrosion resistance testing in equipment specifications (DEL-24.02)
- Plan for accelerated equipment replacement cycle (5-7 years vs 10+ years typical)
**Contingency Handling:** MAT bucket contingency 25% includes environmental risk premium

---

## R-006: Terminal Integration Complexity and Protocol Compatibility

**Risk Driver:** Interface/integration uncertainty
**Cause:** Terminal security system integration requirements TBD per DEC-05; protocols, credentials, network topology unknown
**Consequence:** Integration may require additional software licensing, middleware, network security equipment, or custom development
**Affected Buckets:** MAT (software), CD (integration labor), COM (integration testing)
**Probability:** Medium to High (integration requirements not defined; DEC-05 indicates separate CCTV and access control interfaces)
**Impact:** Medium ($43k for VMS + access control software; integration testing included in commissioning)
**Suggested Mitigation:**
- Obtain Terminal security integration specification early
- Engage Terminal IT/security operations in design review
- Specify open protocols (ONVIF for CCTV, OSDP for access control) to maximize compatibility
- Budget for integration testing and Terminal coordination (included in commissioning allowance)
**Contingency Handling:** MAT, CD, and COM bucket contingencies address integration uncertainty

---

## R-007: Terminal Operations Continuity Constraints (OBJ-5)

**Risk Driver:** Productivity/schedule constraints
**Cause:** Installation must minimize disruption to existing Terminal operations per OBJ-5; phased installation likely required
**Consequence:** Reduced productivity (10-20%); extended installation duration; additional coordination labor
**Affected Buckets:** CD (installation labor), CI (site supervision and coordination)
**Probability:** Medium to High (operational continuity is explicit objective)
**Impact:** Medium (installation productivity reduction reflected in labor hour allowances; contingency addresses further degradation)
**Suggested Mitigation:**
- Develop phased installation plan coordinated with Terminal operations
- Schedule work during low-activity periods where possible
- Maintain close coordination with Terminal security and operations staff
- Budget for extended installation duration in indirects (CI factor includes coordination overhead)
**Contingency Handling:** CD and CI bucket contingencies (30%) address productivity risk

---

## R-008: Escalation Exposure (No Escalation Applied)

**Risk Driver:** Price escalation over project duration
**Cause:** Estimate in January 2026 dollars; no escalation applied per D-004
**Consequence:** Actual costs may be 3-6% higher per year over 2-3 year project duration
**Affected Buckets:** All CBS buckets
**Probability:** High (escalation is typical over multi-year projects)
**Impact:** Medium to High
- 1 year @ 3%: +$25k
- 2 years @ 3-4% per year: +$50-84k
- 3 years @ 3-6% per year: +$75-157k
**Suggested Mitigation:**
- Update pricing at each design milestone (30%, 60%, 90%, IFC)
- Obtain firm pricing commitments from vendors before procurement
- Consider fixed-price contracts to transfer escalation risk
- Monitor market conditions (equipment, labor, commodity pricing)
**Contingency Handling:** Contingency does NOT include escalation; escalation is additional exposure beyond contingency

---

## R-009: Technology Refresh and Obsolescence

**Risk Driver:** Technology lifecycle
**Cause:** Security technology evolves rapidly; 5-7 year equipment refresh cycle vs 15-20 year infrastructure design life
**Consequence:** Equipment may become obsolete or unsupported during project; may require specification updates
**Affected Buckets:** MAT (equipment specifications)
**Probability:** Medium (technology refresh is normal for security systems)
**Impact:** Low for initial deployment (equipment current as of 2026); Medium for lifecycle (already flagged in BOE design life assumptions)
**Suggested Mitigation:**
- Specify current-generation equipment (avoid end-of-life products)
- Require open protocols (ONVIF, OSDP) to minimize vendor lock-in
- Design for future technology upgrades (network infrastructure, power capacity, mounting provisions)
- Plan for equipment refresh in lifecycle cost analysis (outside this estimate scope)
**Contingency Handling:** Not explicitly addressed in contingency (technology refresh is long-term lifecycle issue)

---

## R-010: Privacy and Regulatory Compliance (PIPEDA, Port Security)

**Risk Driver:** Regulatory compliance uncertainty
**Cause:** Privacy requirements (PIPEDA) and port security regulations may impose additional requirements
**Consequence:** May require additional data retention controls, access controls, audit logging, signage, or security assessments
**Affected Buckets:** E (compliance documentation), MAT (software features), CD (installation adjustments)
**Probability:** Low to Medium (compliance requirements are predictable but not fully detailed)
**Impact:** Low (compliance features typically included in commercial security software; incremental cost for additional controls is minor)
**Suggested Mitigation:**
- Review privacy legislation (PIPEDA) requirements for video surveillance
- Review port authority security requirements
- Include privacy compliance in DEL-24.02 specification
- Design system with audit trails, access controls, and data retention policies
- Budget for signage and privacy notifications
**Contingency Handling:** E and MAT bucket contingencies include compliance risk

---

**Risk Register Complete**
**Total Risks:** 10
**Prepared By:** Estimating Agent
**Date:** 2026-01-28

---

## Risk Summary by Category

| Risk Category | Count | Primary Impact |
|---------------|-------|----------------|
| Pricing/Quote Uncertainty | 1 (R-001) | MAT, CD |
| Scope/Quantity Uncertainty | 3 (R-002, R-003, R-004) | MAT, CD |
| Environmental/Durability | 1 (R-005) | MAT |
| Integration/Interface | 2 (R-006, R-007) | MAT, CD, COM |
| Escalation | 1 (R-008) | All CBS |
| Technology/Lifecycle | 1 (R-009) | MAT |
| Regulatory/Compliance | 1 (R-010) | E, MAT, CD |

---

## Contingency Allocation Rationale

The 26% blended contingency rate ($213k on $833k base) addresses the following risk categories:

1. **Pricing uncertainty (R-001):** No vendor quotes; 100% allowance-based
   - MAT bucket 25% contingency
   - CD bucket 30% contingency

2. **Quantity uncertainty (R-002, R-003):** Engineering judgment equipment quantities pending design
   - MAT and CD buckets elevated contingency rates (25-30%)

3. **Coordination and integration complexity (R-004, R-006, R-007):** Underground routing, Terminal integration per DEC-05, operational continuity
   - CD bucket 30% contingency
   - COM bucket 30% contingency
   - CI bucket 30% contingency

4. **Environmental and regulatory risk (R-005, R-010):** Coastal marine environment, privacy/security compliance
   - MAT bucket 25% contingency includes environmental premium
   - E bucket 20% contingency includes compliance documentation risk

5. **Technology risk (R-009):** Moderate; equipment specifications current as of 2026; open protocols specified
   - MAT bucket 25% contingency

**Note:** Escalation risk (R-008) is NOT addressed by contingency; escalation is exposure beyond the $1,047k estimate total and should be tracked separately.

---

## Risk Mitigation Priority (Top 5)

| Priority | Risk ID | Mitigation Action | Expected Benefit |
|----------|---------|-------------------|------------------|
| 1 | R-001 | Obtain vendor quotes from 2-3 security system integrators | Reduce pricing uncertainty; potential to lower contingency 5-10% |
| 2 | R-002 | Complete DEL-24.01 coverage design with camera counts and locations | Reduce quantity uncertainty; refine camera count estimate |
| 3 | R-006 | Obtain Terminal integration specification (protocols, network, credentials) | Reduce integration uncertainty; refine software and commissioning estimates |
| 4 | R-004 | Coordinate underground routing with PKG-03, PKG-17, PKG-25 | Reduce coordination risk; potentially lower conduit installation cost |
| 5 | R-008 | Update pricing at each design milestone; obtain firm pricing before procurement | Manage escalation exposure; update estimate with current market pricing |
