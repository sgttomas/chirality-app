# Datasheet: DEL-32.06 Code Compliance Installation & Test Records

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-32.06 |
| Name | Code Compliance Installation & Test Records |
| Package | PKG-32 Regulatory & Permits |
| Discipline | Project Delivery |
| Type | Record |
| Responsible | D&B Contractor (QA/QC) |
| Status | INITIALIZED |

**Source:** _CONTEXT.md; Decomposition Section 5

## Attributes

| Attribute | Value |
|-----------|-------|
| Purpose | Provides evidence of code compliance (building codes, fire codes, electrical codes, etc.) |
| Scope | Documentation demonstrating compliance with building permit, development permit, fire permit, and other code-related permit conditions |
| Related Deliverable (Upstream) | DEL-32.02 (Permits — building/fire/code permits contain conditions) |
| Record Type | Compliance records (building inspections, fire system tests, code compliance certificates, authority inspections) |
| Regulatory Authorities | City of Surrey (or applicable local authority), fire authority, electrical/gas authorities |
| Format | **TBD** — Per permit conditions and authority inspection requirements |

**Source:** _CONTEXT.md; Decomposition Section 5; **ASSUMPTION** labels as noted

**Key entities:** Building/Fire/Code Permits (DEL-32.02), Permit Conditions, Compliance Records, Compliance Register, Authority Inspection Records

## Conditions

**Regulatory Context:**
- **Authorities:** City of Surrey (or applicable local authority), fire authority, electrical authority, gas authority, plumbing authority — **TBD**: Confirm jurisdictions
- **Jurisdictions:** Building codes, fire codes, electrical codes, plumbing codes, gas codes
- **Project scope triggering code compliance:** Building construction, fire protection systems, electrical systems, storage of flammable/combustible liquids (canola oil) — **ASSUMPTION**: Based on project scope
- **Permits application:** Submitted per DEL-32.01 — **TBD**
- **Permits issued:** Recorded in DEL-32.02 — **TBD**

**Typical code compliance condition categories (anticipated):**
- Building code compliance (structural, envelope, accessibility, seismic)
- Fire code compliance (fire protection systems, exits, separation, flammable liquid storage)
- Electrical code compliance (electrical installations, hazardous area classifications)
- Plumbing code compliance (plumbing systems)
- Gas code compliance (if applicable)
- Authority inspections (building inspectors, fire inspectors, electrical inspectors)
- Occupancy permits and final certifications

**Scope boundary:** Building, fire, electrical, plumbing, gas code permit conditions; other permits in DEL-32.03, 32.04, 32.05

## Construction

**Production:** Similar pattern to DEL-32.03/04/05:
1. Extract building/fire/code permit conditions from DEL-32.02
2. Establish compliance tracking
3. Execute compliance activities (building inspections, fire system tests, electrical inspections, code compliance measures)
4. Collect evidence (inspection reports, test certificates, photos, as-built drawings)
5. Coordinate authority inspections per permit conditions
6. Obtain occupancy permits and final certifications
7. Compile and file compliance records

(See Procedure.md)

**Anticipated artifacts:** Code compliance certificates, inspection records (Source: Decomposition Section 5)

## References

**Primary sources:** _CONTEXT.md, Decomposition Section 5, Specification.md, Guidance.md, Procedure.md

**Related deliverables:**
- DEL-32.01 (Permit Applications) — building/fire/code permit applications
- DEL-32.02 (Permits) — upstream: building/fire/code permits, conditions extracted
- DEL-32.07, DEL-32.08 (Correspondence) — authority inspection records and correspondence
- Construction packages (all packages) — construction generates compliance evidence; building packages (PKG-22, 23, 24, 25, 26) especially relevant

**Standards:** Building codes (BC Building Code, National Building Code) — **TBD**; Fire codes (BC Fire Code, NFPA) — **TBD**; Electrical codes (Canadian Electrical Code) — **TBD**; Employer's Requirements — **location TBD**; ISO 9001:2015 — **ASSUMPTION**

**Dependencies:** NOT_TRACKED
