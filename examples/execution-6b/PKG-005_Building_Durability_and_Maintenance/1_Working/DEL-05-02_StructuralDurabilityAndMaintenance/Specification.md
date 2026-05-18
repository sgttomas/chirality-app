# Specification: Structural Durability and Maintenance

**Deliverable ID:** DEL-05-02
**Document Type:** Normative (Requirements)
**Version:** Draft (Pass 3 — Semantic Lensing Enrichment)

---

## Scope

This specification defines the structural durability and maintenance strategy narrative for the Penhold Public Services Building project, specifically addressing:

**In Scope:**
- Corrosion protection strategy for structural steel, particularly in apparatus bay and Cold Storage environments
- Concrete durability design for freeze-thaw resistance (frost depth 2.0 m, Penhold) and chloride exposure (de-icing salts tracked from vehicles)
- Foundation longevity approach based on the existing 2021 geotechnical investigation (File USG1123, Union Street Geotechnical Ltd.) — no additional investigation authorized
- Slab-on-grade durability in apparatus and PW bays, including sump construction and drainage (bay sumps required per Addendum 03 §1.8)
- Structural element accessibility for inspection and maintenance throughout the 50-year (main building) and 20-year (Cold Storage) design lives
- Material selection philosophy aligned to operations environment (fire apparatus, heavy equipment, moisture, snow/salt)

**Out of Scope:**
- Architectural finishes (cladding, roofing, interior finishes) — covered in DEL-05-01
- Mechanical systems maintainability (HVAC, plumbing, equipment access, sump pump specification) — covered in DEL-05-03
- Electrical systems maintainability — covered in DEL-05-04
- Construction methodology and scheduling — covered in PKG-007 and PKG-009
- Detailed design development (50%, 100% IFC) — covered in PKG-006

---

## Requirements

### Structural System Design Life

| Building / Component | Minimum Design Life | Source |
|----------------------|-------------------|--------|
| Main Building (structural frame, foundations, slabs) | 50 years | RFP §7.1.4; Decomposition PKG-005 goal |
| Cold Storage Building (structural) | 20 years | RFP §7.1.4; Decomposition PKG-005 goal |
| Apparatus Bays (structural) | 50 years | RFP §7.1.4 |
| Public Works Bays (structural) | 50 years | RFP §7.1.4 |
| Slab-on-Grade (all bays) | 50 years (main) / 20 years (Cold Storage) | RFP §7.1.4 |

**R-STR-01:** The structural system shall be designed for a minimum 50-year service life for the main Public Services Building and 20 years for the Cold Storage building (unheated), with all materials, connections, and protective coatings selected accordingly.
*Source: RFP §7.1.4; Decomposition PKG-005 goal statement.*

### Concrete Durability — Sulphate Exposure

**R-STR-02:** All concrete in contact with native soil or cohesive fill shall be designed for severe sulphate attack (Class S-2) per CAN/CSA A23.1-2014, Table 3, using:
- Sulphate-Resistant Portland Cement (Type HS); or Type 10 cement combined with approximately 25% (by mass of cement) Type F or CI fly ash
- Minimum specified 56-day compressive strength of 32 MPa
- Maximum water-cement ratio of 0.45
- No calcium chloride or any other chloride-containing admixture
- No calcium salts as accelerating admixtures

*Source: Geotechnical Investigation Report (USG1123) §4.3, pp. 8–9; CAN/CSA A23.1-2014, Table 3.*

### Concrete Durability — Freeze-Thaw and Chloride Exposure

**R-STR-03:** All concrete exposed to freeze-thaw cycling and/or de-icing chemicals shall include air entrainment per CAN/CSA A23.1-2014, Clause 4.3.3 and Table 4, for the Penhold regional climate.

*Source: Geotechnical Investigation Report (USG1123) §4.3, p. 9; CAN/CSA A23.1-2014.*

**R-STR-04:** If concrete is placed during winter conditions, placement shall comply with the cold-weather provisions of CAN/CSA-A23.1, including but not limited to:
- Minimum curing and protection period as specified in CAN/CSA-A23.1 for the applicable exposure class and member type — **TBD: confirm specific minimum curing duration (e.g., 7 days above 10 C for sulphate-resistant concrete) during detailed design**
- Concrete temperature at placement shall not be below 5 C
- Heated enclosures or insulated blankets shall be used as required

*Source: Geotechnical Investigation Report (USG1123) §4.3, p. 9. Enrichment: Semantic Lensing A-002 — cold-weather curing duration specificity gap.*

**R-STR-05:** Slab-on-grade in apparatus and PW bays, subject to vehicle traffic, snow melt, and de-icing salt tracking, shall:
- Include air entrainment for freeze-thaw protection (per R-STR-03)
- Have a maximum water-cement ratio of 0.45 to resist chloride ingress
- Have a minimum compressive strength of **TBD** MPa — **ASSUMPTION: 32 MPa minimum per R-STR-02 applies as a floor; higher strength (e.g., 35 MPa) may be warranted for heavy vehicle traffic in apparatus bays. Structural Engineer to confirm during detailed design.** (See Conflict Table CON-004 in Guidance.md)
- Incorporate sealed construction and control joints to minimize water and salt infiltration
- Be underlaid by a minimum 150 mm layer of 20 mm screened/washed Radon Rock on compacted subgrade
- Include a polyethylene vapour/radon barrier conforming to CAN/CGSB-51.34-M, sealed, between the granular base and the concrete slab
- Be supported on subgrade compacted to a minimum 98% SPDD (ASTM D698); 100% SPDD for structural fills exceeding 1.2 m thickness

*Source: Geotechnical Investigation Report (USG1123) §7.1, items 3–7, pp. 25–26; Addendum 03 §1.8. Enrichment: Semantic Lensing A-001, E-001 — bay slab compressive strength gap identified; R-STR-02 specifies 32 MPa for below-grade, Guidance EX-001 suggests 35 MPa for bay slabs.*

### Bay Slab Abrasion and Wear Resistance

**R-STR-05A:** Apparatus bay and PW bay slab surfaces, subject to heavy vehicle traffic (fire apparatus, heavy equipment), shall incorporate abrasion/wear resistance provisions. **TBD: Specify minimum abrasion resistance class (e.g., AR-2 per CAN/CSA A23.1) or surface hardener requirement (e.g., dry-shake metallic aggregate or liquid densifier/hardener) during detailed design.**

**ASSUMPTION:** Bay slab concrete will be subject to significant abrasion from tire traffic, equipment movement, and snow/ice scraping. Abrasion resistance is a distinct durability requirement beyond freeze-thaw and chloride protection and should be explicitly addressed.

*Source: ASSUMPTION — industry best practice for apparatus bay flooring; Specification R-STR-05 (bay slab scope). Enrichment: Semantic Lensing E-002 — abrasion/wear resistance gap.*

---

### Foundation Design and Ground Contact

**R-STR-06:** Foundation system shall be designed per the 2021 geotechnical recommendations (File USG1123) and shall address:
- Shallow foundations (spread footings) founded on native sand (min. 0.61 m depth, ULS 300 kPa, SLS 100 kPa) or native till (min. 2.0 m depth, ULS 360 kPa, SLS 120 kPa), with a minimum 0.50 m buffer between footing base and clay stratum when bearing on sand; OR
- Driven steel pipe piles with minimum embedment of 5.3 m (to resist frost jacking) with open-end pipe recommended for piles terminating in till; OR
- Screw piles with upper helix installed below the 2.0 m frost depth
- One foundation system type shall be used per structure (do not mix systems supporting the same structure)
- Shallow foundations shall not be placed on organic, non-structural fill, soft, wet, frozen, or high-plastic soil (per geotech rec.)

*Source: Geotechnical Investigation Report (USG1123) §5.2, §5.3, §5.4, pp. 15–24; Geotechnical Report Summary item 5, p. 10.*

**R-STR-07:** All below-grade concrete for foundation elements shall comply with sulphate-resistant concrete requirements in R-STR-02. Calcium chloride and chloride-bearing admixtures shall not be used.

*Source: Geotechnical Investigation Report (USG1123) §4.3.*

**R-STR-08:** Foundation design shall account for adfreezing (frost jacking) stresses on piles: adfreeze stress = 100 kPa above the 2.0 m frost depth, for fine-grained soil in contact with steel. Minimum pile embedment shall be 5.3 m for driven piles in unheated structures to resist frost jacking.

*Source: Geotechnical Investigation Report (USG1123) §5.5.2, p. 24.*

**R-STR-09:** Pile-supported structures shall include a minimum void space between the underside of the pile-supported structure and the subgrade: 100 mm void if subgrade is sand; 150 mm void if subgrade is clay. This void accommodates frost heave and swelling clay movement without transferring load to the slab.

*Source: Geotechnical Investigation Report (USG1123) §5.5.3, p. 24.*

**R-STR-10:** Positive drainage shall be maintained around all structures. Finished grade adjacent to building shall be sloped a minimum of 3% over 3.0 m away from the building. No ponding shall be permitted adjacent to foundations or slab perimeters.

*Source: Geotechnical Investigation Report (USG1123) §5.1.2, p. 13.*

### Structural Steel Corrosion Protection

**R-STR-11:** All structural steel shall be protected against corrosion according to the applicable exposure class for its location:
- **C2 (Moderate):** Structural frame in protected exterior or dry interior locations — conventional paint systems acceptable (minimum DFT >=100 um)
- **C3 (High):** Structural elements in apparatus bays, PW bays, near 16 ft overhead doors, and other locations subject to de-icing salt tracking and regular moisture — enhanced paint systems (DFT >=150 um) or hot-dip galvanizing per ASTM A123
- **C4 (Very High):** Structural elements in Cold Storage (unheated, condensation risk) or areas with continuous moisture — hot-dip galvanizing (ASTM A123) or stainless steel elements

*Note: All DFT values are stated as minimums (>=) for specification clarity. Enrichment: Semantic Lensing C-001 — C2 DFT changed from approximate "~100 um" to minimum ">=100 um" for regulatory adequacy threshold consistency with C3/C4 language.*

**ASSUMPTION:** Final exposure class assignments shall be confirmed by the Structural Engineer during detailed design. The C2/C3/C4 framework is adapted from ISO 12944 / CSA G40.20-M.

*Source: ISO 12944 (corrosion protection by paint systems); ASSUMPTION: adapted to site conditions.*

**R-STR-12:** Corrosion protection strategy shall be documented in the durability narrative including:
- Paint system specification (primer, intermediate coat, topcoat) and dry film thickness (DFT)
- Galvanizing designation (ASTM A123 or equivalent) for elements in C3–C4 zones
- Fastener specification: stainless steel (304 or 316 grade) in C3–C4 zones; zinc-plated or hot-dip galvanized in C2 zones
- Surface preparation standard (SSPC, ISO, or CSA equivalent)
- Maintenance and touch-up protocol for 50-year design life

*Source: ASSUMPTION: Industry best practices for structural durability narrative content.*

### Bay Sump Construction and Durability

**R-STR-13:** Apparatus bays and PW bays shall be provided with sumps (confirmed required per Addendum 03 §1.8) to allow for snow melting and minor washing drainage. Sump construction shall satisfy:
- Interior surfaces protected against freeze-thaw cycling and chloride immersion using one of the following approved options (selection TBD during detailed design): **(a)** epoxy coating (chemically resistant, applied to prepared concrete substrate), **(b)** stainless steel lining (304 or 316 grade), or **(c)** high-density concrete with integral waterproofing admixture. *(Note: This is the authoritative shortlist for sump interior protection; all other documents shall reference this list. Enrichment: Semantic Lensing F-002 — terminology normalization.)*
- Reinforcing detailed to manage local stress concentrations around the sump opening; sump shall not create slab weak points
- Sump includes adequate drainage (pump outlet or gravity drain) sized and located in coordination with mechanical design (DEL-05-03)
- Sump is accessible for visual inspection and periodic cleaning without confined-space entry, unless classified as confined space and managed accordingly

*Source: Addendum 03 §1.8; Specification R-STR-05; coordination with DEL-05-03.*

### Overhead Door Structural Support

**R-STR-14:** Structural framing for apparatus bay and PW bay overhead doors shall accommodate a minimum 16 ft (approx. 4.88 m) clear opening height as required by Addendum 03 §1.10. Door header framing and jambs shall be designed for the structural loads of this door size and shall include impact protection provisions for the structural framing adjacent to door openings.

*Source: Addendum 03 §1.10.*

### Structural Element Accessibility for Inspection and Maintenance

**R-STR-15:** Structural elements shall be designed to allow inspection and maintenance without extraordinary intervention:
- Concrete slabs and sump areas shall have adequate clearance or access routes for visual inspection (spalling detection)
- Roof or elevated structural framing shall permit walkway or inspection-route access for visual inspection and coating touch-up
- Slab-to-structure connections and joint details shall facilitate drainage and avoid entrapment of debris or salt residue
- Penetrations (mechanical, electrical) through structural elements shall be sealed to prevent water infiltration and shall not compromise structural capacity

*Source: RFP §7.1.4 (ease of repair and maintenance); ASSUMPTION: Best practice for long-life infrastructure.*

### Standards Compliance

**R-STR-16:** Design shall comply with all applicable standards:

| Standard | Title | Application |
|----------|-------|-------------|
| National Building Code of Canada (NBCC) | Current edition (as adopted in Alberta) | Structural design loads, building envelope |
| Alberta Building Code (ABC) | Provincial adoption of NBCC | Local amendments; structural requirements |
| CAN/CSA A23.1-2014 | Concrete Durability and Design | Freeze-thaw, sulphate, chloride exposure classes; air entrainment; w/c ratios |
| CAN/CSA A23.2-14A | Concrete Materials and Methods | Materials, testing, acceptance |
| CAN/CGSB-51.34-M | Vapour Barriers | Polyethylene sheeting under slab on grade |
| ISO 12944 / CSA G40.20-M | Corrosion Protection (paint systems) | Steel protection; exposure classes; DFT |
| ASTM A123 | Galvanizing of Structural Steel | Hot-dip galvanizing specification |
| Canadian Foundation Engineering Manual, 4th Ed. (2006) | Foundation Engineering | Pile design; frost jacking; bearing capacity |

*Source: RFP §7.1.4; Geotechnical Investigation Report (USG1123); standard industry practice.*

---

## Verification

### Design Verification Approach

| Requirement | Verification Method | Verification Point | Responsibility |
|-------------|-------------------|-------------------|-----------------|
| **R-STR-01** (Design life) | Material specifications; design calculations | Conceptual design; 60% design review | Structural Engineer |
| **R-STR-02** (Sulphate concrete) | Concrete specs; cement supplier cert.; CSA A23.1 compliance; **56-day strength acceptance: if any 56-day cylinder result falls below 32 MPa, initiate non-conformance protocol — core testing of in-place concrete per CAN/CSA A23.2; if cores confirm deficiency, Structural Engineer to assess structural adequacy and prescribe remediation (repair, strengthening, or removal and replacement)** | Material submittals; concrete testing (56-day); non-conformance report if required | Contractor / QC Inspector / Structural Engineer |
| **R-STR-03/04** (Freeze-thaw / cold weather) | Air content testing; curing inspection | On-site concrete testing per placement | Contractor / QC Inspector |
| **R-STR-05** (Slab on grade) | Slab drawings; base course inspection; vapour barrier install | 60% design; construction inspection | Structural Engineer |
| **R-STR-05A** (Abrasion resistance) | Concrete mix design review; surface hardener product datasheet; post-placement surface hardness test (TBD) | Material submittals; construction inspection | Structural Engineer / Contractor |
| **R-STR-06** (Foundation system) | Foundation design drawings; geotech review; **if driven piles are selected: pile integrity testing (e.g., Pile Driving Analyzer (PDA) or equivalent dynamic load testing) on a representative sample of installed piles to verify capacity and embedment depth** | Detailed design; bearing surface inspection; pile installation and integrity testing records | Structural Eng. / Geotech PE |
| **R-STR-07/08** (Foundation concrete + frost jacking) | Type HS spec; pile length on drawings | Material submittals; pile installation record | Structural Eng. / Geotech PE |
| **R-STR-09** (Void space) | Drawing detail confirming void dimension | 60% design review; construction inspection | Structural Engineer |
| **R-STR-10** (Site drainage) | Grade drawings; site inspection after construction | Civil design; construction inspection | Civil / Structural Engineer |
| **R-STR-11/12** (Steel corrosion) | Coating schedule; DFT measurements; galvanizing certs. | Shop and field inspection | Contractor / Coatings Inspector |
| **R-STR-13** (Sump construction) | Sump detail drawings; epoxy/lining spec; drain coordination | 60% design; construction inspection | Structural + Mechanical Eng. |
| **R-STR-14** (Door framing) | Structural drawings; door header design | 60% design review | Structural Engineer |
| **R-STR-15** (Accessibility) | Walkway designs; inspection route plan | Detailed design | Structural Engineer |
| **R-STR-16** (Standards compliance) | Independent design review (peer review by qualified PE not involved in original design) verifying compliance against each listed standard; compliance documented via signed checklist referencing specific standard clauses | Design QC; PE seal; independent review report | Structural Engineer (PE) + Independent Reviewer |
| **R-STR-16A** (Lifecycle cost) | Lifecycle cost summary reviewed for completeness and reasonableness by project manager | Narrative review before proposal submission | Structural Engineer / Project Manager |

### Inspection and Testing Plan (Construction Phase)

- **Concrete testing:** Strength samples at 7, 28, and 56 days (especially for Type HS below-grade concrete)
- **Air content testing:** On-site slump and air content measurements for all freeze-thaw exposed concrete placements
- **Coating inspection:** DFT measurements; surface profile; holiday detection for painted steel
- **Sump lining:** Holiday detection or equivalent void inspection after epoxy/lining application
- **Concrete cover depth verification:** Covermeter survey on representative structural elements after formwork removal to confirm minimum clear cover to reinforcement is achieved per design drawings — **TBD: specify minimum cover depths per exposure class once B-001 (Datasheet cover depth data) is resolved** *(Enrichment: Semantic Lensing X-002)*
- **Joint sealing:** Inspection of joint sealant installation, depth, and cure
- **Vapour barrier:** Inspection of CAN/CGSB-51.34-M sheeting continuity and sealing before slab pour
- **Compaction:** Density testing at minimum 1 test per 500 m² of structural fill (per geotech rec.)

---

## Documentation

### Required Deliverable Artifacts

| Artifact | Format | Phase |
|----------|--------|-------|
| Structural Durability Narrative | Written (RFP §7.1.4 format, per proposal) | Proposal submission |
| Foundation Design Approach | Design calculations + drawings | Detailed design (post-award) |
| Concrete Specifications | Material specifications (CSA A23.1-2014 format) | Detailed design (post-award) |
| Corrosion Protection Specification | Coating schedule; DFT; product datasheets | Detailed design (post-award) |
| Sump Construction Detail Drawings | CAD drawings (section, drain detail) | Detailed design (post-award) |
| O&M Manual (Structural section) | Maintenance schedule, inspection checklist, material references | Project close-out |

**R-STR-16A:** The durability narrative shall include a lifecycle cost summary demonstrating the cost-effectiveness of the proposed durability strategy over the 50-year (main building) and 20-year (Cold Storage) design lives. The summary shall address, at minimum:
- Estimated initial cost premium for durability measures (sulphate-resistant concrete, galvanizing, air entrainment)
- Estimated maintenance costs over the design life (per the maintenance schedule in Procedure Step D2)
- Comparison of lifecycle cost for the proposed approach vs. a reduced-durability alternative (to justify the durability investment)

**ASSUMPTION:** Lifecycle cost analysis supports the OBJ-005 scoring value proposition. Guidance T-001 and Procedure Step A6 reference lifecycle cost narrative, but no Specification requirement previously mandated its production.

*Source: RFP §7.1.4 (durability narrative scope); Guidance T-001; Procedure Step A6. Enrichment: Semantic Lensing C-002 — lifecycle cost verification gap.*

**R-STR-17:** The durability narrative shall address all evaluation sub-criteria in RFP §7.1.4, including design approach, material selection, construction methods, and maintenance strategy aligned to the 50-year (main building) and 20-year (Cold Storage) design lives.

*Source: RFP §7.1.4; OBJ-005 (15 evaluation points).*

**R-STR-18:** The narrative shall be authored by the Structural Engineer and shall coordinate with DEL-05-01 (Architectural), DEL-05-03 (Mechanical), and DEL-05-04 (Electrical) durability narratives to ensure comprehensive coverage of OBJ-005.

*Source: Decomposition SOW-0013; DEC-009 (split by discipline).*

---

## Assumptions

1. **ASSUMPTION:** No additional geotechnical investigation beyond the 2021 report (USG1123) will be performed at proposal stage. Foundation design will rely on existing soil and sulphate data. Sulphate classification may be verified during detailed design (post-award) if Owner and Engineer agree, but design defaults to S-2.
   *Source: Decomposition DEC-013; RFP §7.3.4 (Subconsultants — geotech review responsibility).*

2. **ASSUMPTION:** Apparatus and PW bay sumps are internal in-floor features (not external ponds or retention structures). Sump durability is addressed through concrete protection and interior lining; drainage is coordinated with mechanical design.
   *Source: Addendum 03 §1.8; RFP Appendix A.*

3. **ASSUMPTION:** Structural steel exposure classes (C2, C3, C4) are appropriate for the identified environments. Final exposure class may be refined during 60% design phase based on detailed mechanical and site drainage design.
   *Source: ISO 12944; ASSUMPTION.*

4. **ASSUMPTION:** The Pickled Sand Storage building has been removed from the project (Addendum 03 §1.2). This deliverable does not address that structure.
   *Source: Addendum 03 §1.2.*

---

## Conflicts and Open Items

| Conflict ID | Issue | Status |
|-------------|-------|--------|
| CON-001 | Exact sulphate classification: geotechnical report assumes S-2 (severe) but laboratory testing was not performed. If post-award detailed design testing reveals lower sulphate levels, concrete specification for below-grade elements may be adjusted. | TBD — resolves at foundation design, post-award |
| CON-002 | Sump interior surface protection: multiple viable options (epoxy coating, stainless steel lining, dense concrete). Final selection depends on cost-benefit analysis. Narrative should identify the shortlisted approach. | TBD — resolves at 60% design review |
| CON-003 | Sump drainage responsibility boundary: structural engineer designs sump shell, reinforcing, and structural protection; mechanical engineer designs drainage (pump, overflow, piping). Interface requires formal agreement at Conceptual Design phase (DEL-02-03 / DEL-05-03 coordination). | TBD — requires mechanical design input |
| CON-004 | Bay slab compressive strength: R-STR-02 specifies 32 MPa at 56 days for below-grade sulphate exposure; Guidance EX-001 suggests 35 MPa for apparatus bay slabs; R-STR-05 (above-grade bay slabs) did not specify strength. Structural Engineer to confirm governing strength for bay slabs subject to heavy traffic, freeze-thaw, and chloride exposure. See Guidance.md Conflict Table CON-004. | TBD — Structural Engineer ruling required |
