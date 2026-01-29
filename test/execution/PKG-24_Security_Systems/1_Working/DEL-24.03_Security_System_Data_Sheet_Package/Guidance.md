# Guidance: DEL-24.03 Security System Data Sheet Package

## Purpose

This guidance document supports the assembly and submittal of the **Security System Data Sheet Package** for **PKG-24 Security Systems** at the Canola Oil Transload Facility.

**Deliverable objective:** Defines and substantiates security system in accordance with ER requirements by providing equipment datasheets that demonstrate compliance with the technical specification (DEL-24.02).

*Source: `_CONTEXT.md`; Decomposition Section 5 — PKG-24 (line 568)*

**Classification:** Data Sheet (equipment submittal package) under Specialty discipline, to be produced by D&B Contractor

**Project context:** This equipment submittal package bridges design and construction by documenting the specific equipment selected to implement the security system design (DEL-24.01) in compliance with technical requirements (DEL-24.02).

*Source: DEL-24.01 and DEL-24.02 as design and specification basis*

## Principles

### Equipment Submittal Philosophy

#### Purpose of Equipment Submittals
Equipment submittals serve multiple critical functions in the design-build process:

1. **Compliance verification:** Demonstrate that proposed equipment meets specification requirements
2. **Design validation:** Confirm equipment selection supports design performance objectives
3. **Procurement authorization:** Approved submittals authorize equipment purchase
4. **Installation reference:** Approved datasheets become reference for installation and testing
5. **As-built documentation:** Form basis for as-built records and O&M manuals

*Source: Standard construction procurement and submittal process*

#### Submittal as Contract Document
Once approved, the equipment submittal becomes a contract document:
- Contractor is obligated to provide equipment as submitted and approved
- Substitutions after approval require formal change process
- Installed equipment shall match approved datasheets (verified during installation)
- Deviations may be grounds for rejection during inspection/testing

*Implication: Submit equipment you intend to install; do not submit "placeholder" equipment*

*Source: Standard construction contract administration*

### Equipment Selection Strategy

#### Balancing Cost, Performance, and Risk

**Procurement considerations:**
- **Lowest cost:** May meet minimum specifications but limited performance margin, higher risk
- **Best value:** Balance of cost, performance, reliability, support, and warranty
- **Premium equipment:** Exceeds specifications, lower risk, but higher cost

**Project application (ASSUMPTION):**
- Select proven equipment from reputable manufacturers
- Prioritize reliability and maintainability for 24/7 industrial application (OBJ-1)
- Consider lifecycle cost (OBJ-9) — initial cost vs. maintenance/replacement costs
- Verify Terminal compatibility for integration components (DEC-05)

*Source: OBJ-1, OBJ-9 (Decomposition Section 2); DEC-05 (Section 7)*

#### "Approved Equivalent" Strategy

If DEL-24.02 specifies approved manufacturers or products:
- Approved equipment: Submit as specified, straightforward approval
- Equivalent equipment: Requires technical justification and acceptance
  - Demonstrate equal or superior performance
  - Show compatibility and interoperability
  - Provide cost and schedule comparison if requesting substitution
  - Risk: May be rejected or require additional review time

*Recommendation: Use specified products unless significant advantage to equivalent*

*Source: Standard specification compliance and substitution process*

### Submittal Quality and Completeness

#### First-Time Approval Strategy
Goal: Achieve "Approved" or "Approved as Noted" on first submittal to avoid schedule delays.

**Keys to first-time approval:**
1. **Read the specification carefully** — Understand all requirements in DEL-24.02
2. **Match design intent** — Ensure equipment aligns with DEL-24.01 design
3. **Demonstrate compliance explicitly** — Provide compliance matrix, not just datasheets
4. **Include all required documentation** — Certifications, test reports, integration docs
5. **Organize professionally** — Easy to navigate, clear table of contents, indexed
6. **Coordinate internally** — Review submittal before submission to catch errors

**Common reasons for "Revise and Resubmit":**
- Missing information or incomplete datasheets
- Non-compliance with specification requirements (not clearly demonstrated)
- Wrong equipment type or model (doesn't match design)
- Missing certifications or approvals
- Poor organization or unclear presentation

*Source: Standard submittal review process; common submittal deficiencies*

#### Compliance Matrix — Critical Tool

A compliance matrix explicitly shows specification requirement vs. equipment specification:

| Spec Requirement | Spec Section | Equipment Specification | Complies? | Comments |
|------------------|--------------|-------------------------|-----------|----------|
| Camera resolution: min 2MP | 2.2.1 | 4MP (2688×1520) | Yes — Exceeds | Provides margin for coverage |
| Operating temp: -20°C to +40°C | 2.2.1 | -40°C to +60°C | Yes — Exceeds | Suitable for harsh environment |
| IP rating: IP66 minimum | 2.2.1 | IP67 | Yes — Exceeds | Better weather protection |
| ONVIF Profile S | 2.2.1 | ONVIF Profile S certified | Yes | Certificate included in Appendix |

**Benefits:**
- Makes reviewer's job easy — clear pass/fail for each requirement
- Highlights where equipment exceeds specifications
- Identifies any deviations requiring justification
- Reduces review time and questions

*Recommendation: Include compliance matrix for each major equipment category*

*Source: Best practice for equipment submittals*

### Terminal Integration Considerations (DEC-05)

#### Integration Equipment Selection

For equipment integrating with Terminal systems per DEC-05:
- **Preferred approach:** Use Terminal-specified or compatible equipment
  - Reduces integration risk
  - Ensures support from Terminal IT/security operations
  - May expedite approval

- **Alternative approach:** Propose compatible equipment with strong justification
  - Provide integration documentation (protocols, APIs, compatibility testing)
  - Demonstrate advantages (cost, performance, features)
  - Coordinate with Terminal IT early for acceptance

**Integration documentation requirements:**
- Protocol specifications and communication standards
- API documentation for software integration
- Configuration guides and setup instructions
- Compatibility testing results or certifications
- Support and maintenance arrangements

*Source: DEC-05 (Decomposition Section 7); Terminal integration requirements*

## Considerations

### Factors to Consider During Equipment Selection and Submittal

#### 1. Design Alignment

**Verify equipment selection supports design:**
- Camera specifications achieve coverage analysis requirements from DEL-24.01
- NVR capacity supports retention period and recording parameters
- Access control capacity supports door count and user population
- Network equipment supports bandwidth and topology from design
- Mounting hardware compatible with design mounting methods

**Cross-check against design:**
- Equipment quantities match design schedules
- Equipment locations per design drawings (include tag numbers on datasheets)
- Equipment types match design intent (fixed vs. PTZ cameras, reader technology, etc.)

*Source: DEL-24.01 as design basis*

#### 2. Specification Compliance

**Systematically verify compliance with DEL-24.02:**
- Performance specifications (resolution, capacity, speed, accuracy)
- Environmental ratings (IP, IK, temperature, humidity)
- Electrical specifications (voltage, power, PoE class)
- Communication protocols (ONVIF, OSDP, TCP/IP)
- Certifications and approvals (UL/CSA, FCC, area classification)
- Materials and construction (corrosion resistance, vandal resistance)
- Integration requirements (Terminal compatibility)

**Document compliance:**
- Create compliance matrix for major equipment
- Highlight where equipment exceeds specifications (positive)
- Clearly identify and justify any deviations (if requesting substitution)

*Source: DEL-24.02 as specification basis*

#### 3. Environmental Suitability

**Fraser Surrey Terminal coastal marine environment:**
- Salt spray and corrosion — verify marine-grade materials and coatings
- High humidity — verify sealed enclosures, conformal coating on electronics
- Temperature extremes — verify operating temperature range adequate
- UV exposure — verify UV-resistant housings and cable jackets
- Vandal risk — verify IK ratings for accessible equipment

**Hazardous area requirements:**
- Verify equipment ratings for Class I Div 2 areas (if applicable) **TBD**
- Verify installation methods compatible with hazardous area requirements
- Include hazardous area certifications

*Source: Datasheet.md — Environmental conditions*

#### 4. Reliability and Maintainability (OBJ-1, OBJ-9)

**Reliability considerations:**
- Select equipment from reputable manufacturers with proven track record
- Verify equipment MTBF (Mean Time Between Failures) acceptable for 24/7 operation
- Consider redundancy for critical components (NVR, network switches) **TBD**
- Verify warranty terms and support availability

**Maintainability considerations:**
- Spare parts availability and lead times
- Standardization where possible (reduces spare parts inventory)
- Ease of access for maintenance (consider mounting locations)
- Firmware update and support lifecycle

*Source: OBJ-1 (Safe & Reliable Operation), OBJ-9 (Lifecycle Cost Optimization) — Decomposition Section 2*

#### 5. Cost and Schedule

**Procurement considerations:**
- Equipment availability and lead times (avoid long-lead items if possible)
- Pricing and budget compliance
- Warranty and support costs
- Training requirements and costs

**Schedule considerations:**
- Submittal review time (allow adequate time for review and resubmittal if needed)
- Equipment delivery time (coordinate with construction schedule)
- Factory acceptance testing time (if required) **TBD**

#### 6. Factory Acceptance Testing (FAT)

**For major equipment requiring FAT (TBD per DEL-24.02):**
- Plan FAT logistics (location, witnesses, schedule)
- Coordinate FAT procedure and acceptance criteria with designer/Employer
- Include FAT documentation in submittal (procedure, schedule, witness list)
- Budget time and cost for FAT (testing time, travel for witnesses)
- Plan for deficiency resolution and re-test if needed

*Source: DEL-24.02 — Quality assurance requirements*

## Trade-offs

### Competing Concerns to Evaluate

#### 1. Specified Equipment vs. Equivalent Substitution
**Trade-off:** Proposing equivalent equipment may offer cost savings or superior performance but adds approval risk and time.

**Considerations:**
- Approval risk: Equivalents may be rejected or require extensive justification
- Schedule risk: Additional review time, potential for resubmittal
- Integration risk: Compatibility with Terminal systems may be questioned (DEC-05)
- Cost/performance benefit: Must be significant to justify substitution risk

*Decision approach: Use specified equipment unless clear advantage; coordinate with designer early if proposing substitution*

#### 2. Minimum Specification vs. Performance Margin
**Trade-off:** Equipment barely meeting minimum specs saves cost but provides no margin; exceeding specs costs more but reduces risk.

**Considerations:**
- Design margin: Coverage analysis assumes certain camera performance; margin ensures performance if conditions vary
- Future-proofing: Higher-spec equipment may better support future needs (OBJ-8)
- Reliability: Higher-grade equipment typically more reliable (OBJ-1)
- Cost: Balance performance margin vs. budget

*Decision approach: Modest performance margin (10-20% above minimum) provides good balance*

*Source: OBJ-1, OBJ-8 (Decomposition Section 2)*

#### 3. Single Vendor vs. Multi-Vendor Solution
**Trade-off:** Single vendor provides unified support but may be more expensive; multi-vendor may save cost but complicates support.

**Considerations:**
- Integration complexity: Single vendor simplifies integration, multi-vendor requires careful compatibility verification
- Support and warranty: Single point of contact vs. multiple vendors (finger-pointing risk)
- Cost: Multi-vendor competitive pricing vs. single-vendor package pricing
- Flexibility: Multi-vendor allows best-of-breed selection

*Decision approach: Single vendor for critical integrated systems (VMS/NVR, access control platform); multi-vendor acceptable for peripheral equipment (cameras, readers, door hardware) if compliant with open standards*

#### 4. Current Model vs. End-of-Life Equipment
**Trade-off:** End-of-life or discontinued models may be discounted but have support and parts risks.

**Considerations:**
- Manufacturer support: End-of-life equipment may have limited firmware updates, technical support
- Spare parts: Discontinued models may have spare parts availability issues
- Warranty: Limited warranty period or support for discontinued models
- Cost savings: May be significant discounts on discontinued inventory

*Decision approach: Avoid end-of-life equipment for critical systems; current or recently released models preferred*

#### 5. Submittal Detail vs. Time to Prepare
**Trade-off:** Comprehensive submittal takes more time to prepare but increases approval likelihood.

**Considerations:**
- Approval probability: Thorough submittal with compliance matrices, certifications, integration docs increases first-time approval chance
- Schedule: Rushed submittal may result in "Revise and Resubmit," ultimately taking more time
- Quality: Professional, well-organized submittal reflects well on contractor

*Decision approach: Invest time in thorough submittal; schedule adequate time for preparation*

## Examples

### Submittal Package Structure Example

**DEL-24.03 Security System Data Sheet Package**

**Table of Contents:**
1. Introduction and Submittal Summary
2. Equipment Schedule (all equipment with tag numbers, locations, quantities)
3. Section 1: CCTV System
   - 1.1 Compliance Matrix — CCTV Equipment
   - 1.2 Fixed Camera Datasheets (by model)
   - 1.3 PTZ Camera Datasheets
   - 1.4 NVR Datasheets
   - 1.5 VMS Software Datasheet and Licensing
4. Section 2: Access Control System
   - 2.1 Compliance Matrix — Access Control Equipment
   - 2.2 Card Reader Datasheets (by model)
   - 2.3 Access Control Controller Datasheets
   - 2.4 Access Control Software Datasheet and Licensing
   - 2.5 Door Hardware Datasheets (electric strikes, mag locks, crash bars, REX, door position switches)
5. Section 3: Network Infrastructure
   - 3.1 Compliance Matrix — Network Equipment
   - 3.2 Network Switch Datasheets
   - 3.3 Fiber Optic Equipment Datasheets
   - 3.4 Cabling Specifications
6. Section 4: Power and UPS
   - 4.1 UPS Datasheets
   - 4.2 Power Supply Datasheets
7. Section 5: Accessories
   - 5.1 Mounting Hardware
   - 5.2 Miscellaneous Equipment
8. Appendices
   - Appendix A: Equipment Certifications (UL/CSA, IP/IK, ONVIF, etc.)
   - Appendix B: FAT Documentation (if applicable)
   - Appendix C: Terminal Integration Documentation
   - Appendix D: Installation Instructions Summary

**Equipment Index:** (Alphabetical and by tag number)

*Source: Standard equipment submittal package organization*

### Compliance Matrix Example

**CCTV Fixed Camera — Compliance Matrix**

| Requirement | DEL-24.02 Ref | Specified Value | Proposed Equipment | Complies? | Comments |
|-------------|---------------|-----------------|---------------------|-----------|----------|
| Resolution | 2.2.1 | Minimum 2MP (1920×1080) | 4MP (2688×1520) | ✓ Yes — Exceeds | Higher resolution provides better image detail |
| Frame rate | 2.2.1 | 30 fps minimum | 30 fps (configurable up to 60 fps) | ✓ Yes — Meets | Configurable for different zones |
| Compression | 2.2.1 | H.264 or H.265 | H.265 with Smart Codec | ✓ Yes — Meets | Reduces bandwidth/storage requirements |
| Low-light | 2.2.1 | 0.01 lux minimum | 0.005 lux color, 0.0005 lux B&W | ✓ Yes — Exceeds | Better low-light performance |
| WDR | 2.2.1 | 120 dB minimum | 140 dB True WDR | ✓ Yes — Exceeds | Improved high-contrast scene performance |
| Operating temp | 2.2.1 | -20°C to +40°C | -40°C to +60°C | ✓ Yes — Exceeds | Suitable for harsh coastal environment |
| IP rating | 2.2.1 | IP66 minimum | IP67 | ✓ Yes — Exceeds | Better dust and water protection |
| IK rating | 2.2.1 | IK10 for accessible locations | IK10 | ✓ Yes — Meets | Vandal-resistant |
| Power | 2.2.1 | PoE (IEEE 802.3af/at) | PoE+ (IEEE 802.3at), max 25W | ✓ Yes — Meets | Compatible with specified PoE switches |
| ONVIF | 2.2.1 | ONVIF Profile S | ONVIF Profile S certified | ✓ Yes — Meets | Certificate included in Appendix A |
| Materials | 2.2.1 | Marine-grade, corrosion-resistant | Aluminum alloy with powder coating, stainless steel hardware | ✓ Yes — Meets | Suitable for coastal environment |

**Overall Compliance: COMPLIANT — All requirements met or exceeded**

*Source: Example compliance matrix format for equipment submittals*

### Datasheet Content Example (Abbreviated)

**Fixed IP Camera Datasheet — Model XYZ-4000**

**Manufacturer:** [Camera Manufacturer Inc.]
**Model:** XYZ-4000 Fixed Bullet Camera
**Tag Numbers:** CAM-01 through CAM-45 (45 units) per DEL-24.01

**Key Specifications:**
- Image Sensor: 1/2.8" Progressive Scan CMOS
- Resolution: 4MP (2688×1520)
- Frame Rate: 30 fps @ 4MP (configurable)
- Lens: 2.8mm fixed (other lens options available)
- Field of View: 110° (H) × 58° (V) @ 2.8mm lens
- Compression: H.265+/H.265/H.264+/H.264
- Low-Light Performance: 0.005 lux @ F1.6 (color), 0.0005 lux (B&W)
- Wide Dynamic Range: 140 dB True WDR
- Operating Temperature: -40°C to +60°C
- Ingress Protection: IP67
- Impact Protection: IK10
- Power: PoE+ (IEEE 802.3at), 12 VDC (max 25W)
- ONVIF: Profile S certified (certificate attached)
- Dimensions: 290mm × 95mm × 95mm
- Weight: 1.2 kg
- Mounting: Wall/ceiling bracket included
- Certifications: UL, CSA, FCC, CE (certificates attached)

**Compliance Notes:**
- Exceeds minimum 2MP resolution requirement — provides 4MP for better image detail
- Exceeds minimum operating temperature range — rated to -40°C for extreme cold
- IP67 rating exceeds minimum IP66 requirement
- ONVIF Profile S certified for VMS interoperability

**Installation:** See manufacturer installation guide (attached). Wall/ceiling mounting bracket included. Conduit entry options provided for IP67 seal.

**Warranty:** 5-year manufacturer warranty on camera and housing.

*Source: Example abbreviated equipment datasheet content*

---

*Document status: Enriched draft — Pass 1*
*Enrichment date: 2026-01-28*
*Cross-references: Specification.md for submittal requirements; Datasheet.md for equipment scope; Procedure.md for submittal workflow*
