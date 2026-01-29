# Risk Register — PKG-18 Lighting Estimate

**Snapshot ID:** EST_PKG18_DRAFT_2026-01-28_2400
**Date:** 2026-01-28

---

## Purpose

This register documents risks that could affect the PKG-18 Lighting estimate accuracy and provides mitigation recommendations. Each risk is assigned a unique ID (R-1801, R-1802, etc.) and categorized by driver type.

---

## Risk Entries

### R-1801: Hazardous Area Classification Extent Exceeds Assumptions

**Driver:** Scope / Specification

**Cause → Consequence:**
- **Cause:** Hazardous area classification study (anticipated in PKG-17 or PKG-24) defines more extensive classified zones than assumed (currently assumed 10-20% of fixtures)
- **Consequence:** Explosion-proof or Class I Division 1/2 fixtures required for larger area; these fixtures cost 2-4× standard LED fixtures

**Affected Buckets:**
- CBS: MAT (Materials), CD (Construction Directs)
- WBS: PKG-18 / All lighting deliverables

**Cost Impact Range:** $15,000-$100,000 CAD increase if classified area extent doubles

**Suggested Mitigation:**
- Obtain hazardous area classification drawings early in design (coordinate with PKG-17, PKG-24)
- Include in ER requirements extraction (Vol 2 Parts 1-3)
- Verify if any areas can use Zone 2 or non-incendive fixtures (lower cost than explosion-proof)
- Consider facility ventilation design to minimize classified zone extent

**Contingency Handling:** Included in 25% MAT and CD contingency; if classification exceeds 30% of fixtures, additional contingency recommended

---

### R-1802: ER Illumination Requirements Exceed Typical Standards

**Driver:** Scope / Quantity

**Cause → Consequence:**
- **Cause:** ER requirements (Vol 2 Parts 1-3) specify higher illuminance levels than IESNA typical values currently assumed (see A-1823)
- **Consequence:** More fixtures required to achieve higher illumination levels; increased material and installation costs

**Affected Buckets:**
- CBS: MAT, CD
- WBS: PKG-18 / DEL-18.01, DEL-18.03

**Cost Impact Range:** $30,000-$120,000 CAD increase if illuminance requirements 50-100% higher than assumed

**Suggested Mitigation:**
- Extract ER illumination requirements early (Vol 2 Parts 1-3)
- Perform preliminary illumination calculations (DEL-18.03) to validate fixture counts
- Optimize fixture selection for higher lumen output if needed
- Consider higher-mounted poles or higher-wattage fixtures to reduce total fixture count

**Contingency Handling:** Included in 25% MAT and CD contingency

---

### R-1803: Site Layout Changes Affecting Exterior Lighting Design

**Driver:** Interface / Scope

**Cause → Consequence:**
- **Cause:** Site layout, grading, or paving configuration changes during design development (PKG-01, PKG-02, PKG-04) affecting lighting pole locations and circuiting
- **Consequence:** Rework of lighting layout; potential increase in pole counts or wiring run lengths

**Affected Buckets:**
- CBS: E (Engineering rework), MAT (poles, wiring), CD (installation)
- WBS: PKG-18 / DEL-18.01, DEL-18.03

**Cost Impact Range:** $10,000-$50,000 CAD for design rework and incremental pole/wiring costs

**Suggested Mitigation:**
- Early coordination with civil discipline for site layout freeze
- Modular lighting design allowing relocation of poles if needed
- Over-size conduit to allow future circuit changes without trenching

**Contingency Handling:** Included in 25% E, MAT, CD contingency

---

### R-1804: Building Configuration Changes Affecting Interior Lighting

**Driver:** Interface / Scope

**Cause → Consequence:**
- **Cause:** Building layout, ceiling heights, or interior configuration changes during architectural design (PKG-21, PKG-22)
- **Consequence:** Interior fixture counts and types change; rework of lighting layouts and calculations

**Affected Buckets:**
- CBS: E, MAT, CD
- WBS: PKG-18 / DEL-18.01, DEL-18.03

**Cost Impact Range:** $15,000-$60,000 CAD for design rework and fixture adjustments

**Suggested Mitigation:**
- Coordinate with architectural discipline for building layout freeze before detailed lighting design
- Use modular fixture systems adaptable to different ceiling types
- Design flexible control zoning allowing reconfiguration

**Contingency Handling:** Included in 25% E, MAT, CD contingency

---

### R-1805: Control System Integration Complexity Higher Than Assumed

**Driver:** Interface / Specification

**Cause → Consequence:**
- **Cause:** PKG-19 Control Systems requires complex integration (BACnet, custom programming, real-time monitoring) beyond simple on/off control
- **Consequence:** Higher controls equipment cost, programming effort, commissioning complexity

**Affected Buckets:**
- CBS: MAT (controls hardware), CD (installation and programming), COM (commissioning)
- WBS: PKG-18 / DEL-18.02, DEL-18.05

**Cost Impact Range:** $20,000-$80,000 CAD for advanced controls and integration

**Suggested Mitigation:**
- Early coordination with PKG-19 to define control system architecture and integration requirements
- Define control interfaces and protocols in DEL-18.02 Lighting Technical Specification
- Obtain controls vendor quotes for integrated systems
- Consider phased controls implementation (basic first, advanced later)

**Contingency Handling:** Included in 25% MAT and CD contingency; COM contingency at 25%

---

### R-1806: Emergency Lighting Extent Beyond Code Minimum

**Driver:** Scope / Specification

**Cause → Consequence:**
- **Cause:** ER requirements or operational needs require emergency lighting coverage beyond code-minimum egress paths (e.g., all operational areas for safe shutdown)
- **Consequence:** Increased emergency fixture count and battery backup system size/cost

**Affected Buckets:**
- CBS: MAT, CD
- WBS: PKG-18 / DEL-18.01, DEL-18.02

**Cost Impact Range:** $15,000-$60,000 CAD if emergency lighting extent doubles

**Suggested Mitigation:**
- Extract ER emergency lighting requirements early
- Clarify operational requirements for emergency lighting coverage (egress only vs. operational areas)
- Consider emergency generator or UPS supply (PKG-17) instead of individual battery backup to reduce cost

**Contingency Handling:** Included in 25% MAT and CD contingency

---

### R-1807: LED Fixture Supply Chain and Lead Times

**Driver:** Schedule / Price

**Cause → Consequence:**
- **Cause:** LED lighting fixture supply chain constraints or long lead times (12-20 weeks typical for commercial/industrial fixtures)
- **Consequence:** Schedule delays or premium pricing for expedited delivery; potential substitution with higher-cost alternatives

**Affected Buckets:**
- CBS: MAT, P (Procurement expediting)
- WBS: PKG-18 / All deliverables

**Cost Impact Range:** $10,000-$40,000 CAD for expediting or alternative fixtures

**Suggested Mitigation:**
- Early procurement of long-lead lighting fixtures
- Obtain vendor quotes with lead time confirmation
- Identify alternate approved manufacturers in DEL-18.02 to avoid sole-source dependencies
- Order fixtures early based on preliminary design

**Contingency Handling:** Included in 25% MAT contingency

---

### R-1808: Design Changes from ER Requirements Not Yet Extracted

**Driver:** Scope / Specification

**Cause → Consequence:**
- **Cause:** ER requirements (Vol 2 Parts 1-3) contain specific lighting requirements not yet extracted (illuminance levels, fixture types, control requirements, etc.)
- **Consequence:** Design scope or performance requirements differ from assumptions; rework or cost adjustments required

**Affected Buckets:**
- CBS: All buckets (scope uncertainty)
- WBS: PKG-18 / All deliverables

**Cost Impact Range:** -20% to +50% of base estimate depending on ER requirements vs. assumptions

**Suggested Mitigation:**
- Prioritize ER requirements extraction for lighting sections (Vol 2 Parts 1-3)
- Engage Employer early for clarification of lighting performance expectations
- Build ER compliance matrix in DEL-18.02 to track requirements coverage

**Contingency Handling:** Primary driver for 25% overall contingency on this estimate

---

## Risk Summary Table

| Risk ID | Driver Type | Probability | Impact | CBS Affected | Contingency Coverage |
|---------|-------------|-------------|--------|--------------|----------------------|
| R-1801 | Scope/Spec | Medium | Medium-High | MAT, CD | 25% MAT/CD |
| R-1802 | Scope/Qty | Medium | Medium | MAT, CD | 25% MAT/CD |
| R-1803 | Interface/Scope | Medium | Low-Medium | E, MAT, CD | 25% E/MAT/CD |
| R-1804 | Interface/Scope | Medium | Low-Medium | E, MAT, CD | 25% E/MAT/CD |
| R-1805 | Interface/Spec | Medium | Medium | MAT, CD, COM | 25% MAT/CD/COM |
| R-1806 | Scope/Spec | Low-Medium | Medium | MAT, CD | 25% MAT/CD |
| R-1807 | Schedule/Price | Low-Medium | Low-Medium | MAT, P | 25% MAT/P |
| R-1808 | Scope/Spec | High | High | All | 25% All buckets |

**Overall Risk Assessment:** MEDIUM-HIGH (driven primarily by pre-conceptual design maturity and ER requirements uncertainty)

---

## Contingency Adequacy Assessment

**Base Contingency:** 25% overall

**Risk Coverage Analysis:**
- **Low-impact risks (R-1803, R-1804, R-1807):** Well-covered by 25% contingency
- **Medium-impact risks (R-1801, R-1802, R-1805, R-1806):** Adequately covered by 25% contingency assuming single risk realization
- **High-impact risk (R-1808):** ER requirements could drive significant scope changes; 25% contingency provides buffer but not full coverage for worst case

**Recommendation:** 25% contingency is appropriate for Class 5 (Order of Magnitude) estimate at pre-conceptual maturity. If multiple high-impact risks materialize simultaneously, estimate may exceed contingency allowance. Re-estimate after ER extraction and 30% design maturity to refine contingency.

---

**END OF RISK REGISTER**
