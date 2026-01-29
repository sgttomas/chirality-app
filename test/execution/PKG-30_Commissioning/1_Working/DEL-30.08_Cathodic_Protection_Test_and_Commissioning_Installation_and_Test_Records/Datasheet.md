# Datasheet: DEL-30.08 Cathodic Protection Test & Commissioning Installation & Test Records

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-30.08 |
| Name | Cathodic Protection Test & Commissioning Installation & Test Records |
| Package | PKG-30 Commissioning |
| Discipline | T&C (Testing & Commissioning) |
| Type | Record |
| Responsible | D&B Contractor (Commissioning Team) |
| Status | INITIALIZED |
| Project | Canola Oil Transload Facility — Phase 1 |

**Source:** `_CONTEXT.md`; Decomposition §5 PKG-30

## Attributes

| Attribute | Value |
|-----------|-------|
| Record Type | Cathodic Protection (CP) Commissioning and Test Records |
| Applicable Systems | Underground piping, buried steel structures, marine structures requiring corrosion protection |
| Record Format | CP commissioning test sheets, rectifier commissioning records, potential survey data, acceptance certificates |
| Approval Requirements | CP specialist, commissioning engineer, QC inspector, corrosion engineer, regulatory authority (if required) |
| Submittal Timing | Upon CP system commissioning; baseline for ongoing CP monitoring and maintenance |
| Retention Period | **TBD** — Permanent project records (lifecycle corrosion management baseline) |

**Source:** **ASSUMPTION** — CP commissioning record attributes

## Conditions

**Cathodic Protection Context:**

Provides evidence of completion, inspection, and testing for cathodic protection test & commissioning. CP systems protect underground piping and buried/submerged steel structures from corrosion, critical for long-term facility integrity and reliability (OBJ-1, OBJ-9).

**CP System Scope:**
- Underground product piping (railcar unloading lines, product transfer lines)
- Buried steel structures (if applicable)
- Marine structures (steel piles, sheet piling, submerged steel) — Marine environment highly corrosive
- Storage tank bottoms (if in contact with soil/groundwater)
- CP system components: Sacrificial anodes, impressed current systems, rectifiers, test stations, reference electrodes

**Facility Location:** Fraser Surrey Terminal — Coastal marine environment with high corrosivity for buried and submerged steel

**Source:** Decomposition §1.1 (Location: Fraser Surrey Terminal, marine environment); **ASSUMPTION** — CP system scope for canola oil facility with marine structures

## Construction

**Anticipated Artifacts:**

1. **CP Commissioning Test Sheets:**
   - CP system schematic and protected structure identification
   - Pre-commissioning continuity tests (anode-to-structure electrical continuity)
   - Electrical isolation verification (structure isolated from foreign structures)
   - Stray current surveys
   - Initial CP system energization records
   - Commissioning test data: Structure-to-electrolyte potentials, current output, protective current distribution

2. **Rectifier Settings:**
   - Rectifier commissioning records:
     - Rectifier ID and location
     - Nameplate data and design output
     - Initial settings: Voltage, current, tap settings
     - Output verification under load
     - Automatic controls testing (if applicable)
     - Safety features verification (overcurrent protection, lightning protection)

3. **Baseline Potentials:**
   - Baseline structure-to-electrolyte potential survey:
     - Test station locations and IDs
     - Reference electrode type (copper-copper sulfate or other)
     - Initial "CP-off" potentials (native potentials)
     - "CP-on" potentials after system energization
     - Polarization verification (shift from native to protected potential)
     - Criteria verification per NACE SP0169 or applicable standard: -850 mV criterion, 100 mV polarization shift, or other — **TBD**
   - Potential profile mapping along protected structures
   - Documentation of protective potential achieved

4. **Acceptance Records:**
   - CP system commissioning completion certificate
   - Compliance with design requirements and CP standards
   - Corrosion engineer acceptance
   - Regulatory authority acceptance (if required)
   - Recommendations for ongoing CP monitoring and maintenance

**Source:** Decomposition §5 DEL-30.08; **ASSUMPTION** — CP commissioning content per NACE SP0169 and CSA Z662 CP requirements

## References

- DEL-30.01 Commissioning Procedures — CP commissioning procedures
- DEL-30.02 Commissioning Plan — CP commissioning schedule
- CP system design documents (PKG-03, PKG-08, PKG-14) — Underground utilities, marine structures, process piping CP design
- NACE SP0169 — Control of External Corrosion on Underground or Submerged Metallic Piping Systems — **ASSUMPTION: likely applicable** — **location TBD**
- CSA Z662 — Cathodic protection requirements for pipelines — **location TBD**
- Employer's Requirements — **TBD: location** for CP commissioning requirements

**Source:** Decomposition §4, §5 (PKG-03, PKG-08, PKG-14); **ASSUMPTION: likely applicable** standards

---

## Document Cross-References

- **→ Specification.md:** Requirements for CP commissioning testing and acceptance
- **→ Guidance.md:** Rationale for CP system commissioning and corrosion protection
- **→ Procedure.md:** CP commissioning test execution process
