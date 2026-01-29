# Guidance: DEL-11.02 Marine Loading Technical Specification

## Purpose

This guidance document supports the development of **Marine Loading Technical Specification** for **PKG-11 Marine Loading System**.

**Deliverable purpose:** Defines performance, materials, and workmanship requirements for the marine loading system, establishing the technical baseline for procurement, design verification, and acceptance testing of loading facilities at Fraser Surrey Terminal.
**Source:** Decomposition DEL-11.02 description.

**Classification:** Specification deliverable under the Process discipline, produced by the D&B Contractor.
**Source:** Datasheet.md §Identification.

**Objectives context (per decomposition Section 6):**
- **OBJ-1 Safe & Reliable Operation** — specification defines safety-critical requirements (ERC, leak detection, ESD integration)
- **OBJ-2 Throughput Capacity** — specification defines loading rate and system sizing for 1,000,000 MT/annum
- **OBJ-4 Operational Flexibility** — specification defines operating envelope for diverse vessel types
- **OBJ-7 Environmental Protection** — specification defines double-walled pipe, leak detection, and spill prevention requirements

**Source:** Datasheet.md §Objectives Mapping; Specification.md §Scope.

## Principles

**Engineering rationale (Process discipline — marine loading specification):**

1. **Performance-based requirements:** The specification should define *what the system must achieve* (performance outcomes) rather than *how to achieve it* (detailed design), allowing OEM flexibility within defined boundaries. This supports procurement efficiency and leverages vendor expertise (DEL-11.06).
   **Source:** Good practice **ASSUMPTION**; industry standard approach for equipment specifications.

2. **Verifiable requirements:** Every requirement should have a clear verification method (test, inspection, analysis, or review) enabling acceptance at FAT, SAT, or commissioning. Specification.md includes 58+ individual requirements, each with an assigned verification method.
   **Source:** Specification.md §4–§9 requirements structure; Datasheet.md §Deliverable Acceptance.

3. **Traceability to ER:** Requirements should trace to Employer's Requirements clauses; where ER references are not yet available, requirements are marked **TBD** to avoid unsubstantiated constraints. Compliance matrix (Specification.md §Compliance Matrix) maps requirements to ER clauses.
   **Source:** Specification.md §Compliance Matrix; Procedure.md §Step 8.

4. **Safety-first hierarchy:** Emergency release coupling (ERC), leak detection, and ESD integration requirements address the highest-risk scenarios (vessel drift, product release, fire/explosion). These support OBJ-1 Safe & Reliable Operation.
   **Source:** Specification.md §4.6 (ERC), §4.8 (Safety), §6 (Leak Detection); Decomposition OBJ-1.

5. **Environmental protection:** Double-walled pipe with annulus monitoring provides primary and secondary containment; specification defines detection, alarm, and response requirements supporting OBJ-7 Environmental Protection.
   **Source:** Specification.md §5 (Double-Walled Pipe), §6 (Leak Detection); Decomposition OBJ-7.

**ASSUMPTION:** Applicable codes/standards are defined by ER and project code register (to be referenced explicitly once available).

**Applicable standards context:**
- OCIMF (Oil Companies International Marine Forum) — marine loading arm design guidance (**TBD** applicability)
- ASME B31.3 — process piping design code (**TBD** applicability)
- API 2610 — terminal piping design (**TBD** applicability)
- IEC 61511 — safety instrumented systems for leak detection/ESD integration (**TBD** applicability)

**Source:** Specification.md §2 Applicable Documents; Datasheet.md §Standards (8 standards listed).

## Cross-Document Alignment Notes

| Alignment Check | Datasheet | Specification | Procedure |
|-----------------|-----------|---------------|-----------|
| Design basis parameters | §Conditions (11 parameters) | §3 Service/Design Basis (11 parameters) | §Prerequisites (Step 1) |
| Requirement structure | §Construction (5 sections) | §4–§8 (5 requirement sections with 58+ requirements) | §Steps 3-6 (draft requirements) |
| Interface list | §Interfaces (8 interfaces) | §4.7, §5, §6.3, §7, §8 (interface requirements) | §Steps (IDC Step 9) |
| Standards reference | §Standards (8 standards) | §2 Applicable Documents (6+ standards) | §Prerequisites |
| Acceptance criteria | §Deliverable Acceptance (5 criteria) | §Compliance Matrix | §Verification (6-item checklist) |

**Alignment verification (Pass 2/3):**
- Design basis: All 11 parameters consistent across Datasheet §Conditions and Specification §3
- Requirements: 5 specification sections (§4 Loading Arm with 32 requirements, §5 Double-Walled Pipe with 20 requirements, §6 Leak Detection with 14 requirements, §7 Nitrogen with 7 requirements, §8 Shelter with 5 requirements) = 58+ total requirements
- Interfaces: 8 interfaces in Datasheet align with specification sections and Procedure IDC review
- Standards: 8 standards in Datasheet, 6+ in Specification §2 (subset relevant to specification body)
- Acceptance: 5 criteria in Datasheet align with Procedure verification checklist (6 items includes Employer review)

**Cross-deliverable alignment:**
- Requirements written here govern DEL-11.01 drawings (interfaces and layouts)
- Requirements here are verified by DEL-11.03 calculations (sizing, envelope)
- Requirements here are reflected in DEL-11.04 datasheets (equipment parameters)
- Requirements here are demonstrated by DEL-11.05 test records (FAT/SAT)
- OEM capability against requirements here is confirmed by DEL-11.06 qualification

**Source:** Cross-references verified across all four documents.

Where ER clauses cannot be referenced, keep values as **TBD** and avoid introducing implied "defaults."

## Considerations

**Factors to consider during specification development:**

### Loading Arm Considerations (Specification §4 — MLA-001 to MLA-032)
- Powered arm type selection (hydraulic vs. electric drives) affects control system interface
- ERC type selection affects spill volume (MLA-022) and reset requirements (MLA-023)
- Reach/envelope (MLA-004 to MLA-008) must accommodate design vessel range (manifold heights, positions)
- OEM selection (DEL-11.06) influences available configurations and features
- Controls integration (MLA-025 to MLA-028) requires coordination with PKG-19/PKG-20
  **Source:** Specification.md §4; Procedure.md §Step 3; Datasheet.md §Interfaces.

### Double-Walled Pipe Considerations (Specification §5 — DWP-001 to DWP-020)
- Annulus monitoring method (DWP-010 to DWP-013) — vacuum, pressure, or liquid sensing affects maintenance and reliability
- Expansion provisions (DWP-017, DWP-018) must accommodate thermal growth and marine structure movement
- Low-point drainage (DWP-014, DWP-015) is critical for leak containment effectiveness
- Testing requirements (DWP-019, DWP-020) affect construction sequence
  **Source:** Specification.md §5; Procedure.md §Step 4; DEL-11.03 stress analysis.

### Leak Detection Considerations (Specification §6 — LDS-001 to LDS-014)
- Detection philosophy (LDS-001) must address all potential leak paths (annulus, drip trays, sumps)
- Detection methods (LDS-002, LDS-003) — technology selection affects reliability and maintenance
- Alarm vs. trip setpoints (LDS-007, LDS-008) balance nuisance alarms against response time
- Integration with ESD system (LDS-009) requires coordination with PKG-19/PKG-20/PKG-29 **TBD**
- Fail-safe design (LDS-013) ensures system defaults to safe state on sensor failure
  **Source:** Specification.md §6; Procedure.md §Step 5; Datasheet.md §Interfaces.

### Nitrogen Supply Considerations (Specification §7 — N2-001 to N2-007)
- Purpose (N2-001) — purge, inerting, or pressurization affects capacity requirements
- Supply source (N2-002) — facility system or dedicated affects interface definition
- Pressure and flow (N2-003, N2-004) must match loading arm and pipe requirements
  **Source:** Specification.md §7; Procedure.md §Step 6.

### Operator Shelter Considerations (Specification §8 — SHL-001 to SHL-005)
- Location (SHL-002) must balance visibility, access, and safety
- Building services interfaces (SHL-003) require coordination with PKG-22
- Control panel location (SHL-004) affects operator workflow
  **Source:** Specification.md §8; Procedure.md §Step 6; DEL-11.01 shelter drawings.

### Interface Considerations
- I&C interfaces (signals, power, communications) require coordination with PKG-19/PKG-20
- Civil/structural interfaces (foundations, supports) require coordination with PKG-06/PKG-08
- Building works interfaces (shelter) require coordination with PKG-22
- Utilities interfaces (nitrogen) require coordination with utilities package **TBD**
  **Source:** Datasheet.md §Interfaces (8 interfaces); Procedure.md §Step 9 (IDC).

## Trade-offs

**Competing concerns to evaluate:**

| Trade-off | Option A | Option B | Guidance |
|-----------|----------|----------|----------|
| OEM standard vs. custom | Accept OEM standard configuration | Specify custom requirements | Prefer OEM standard where it meets ER (DEL-11.06); custom specs increase cost and lead time |
| Prescriptive vs. performance | Detailed prescriptive requirements | Performance-based outcomes | Performance-based preferred (Principle #1); enables OEM innovation within safety bounds |
| ERC spill volume vs. response | Minimize spill volume (tight tolerance) | Allow larger spill for reliable release | Balance against environmental protection requirements (OBJ-7); see Specification MLA-022 |
| Leak detection sensitivity | High sensitivity (early detection) | Lower sensitivity (fewer nuisance alarms) | Tune for reliable detection without excessive false alarms; see Specification LDS-007, LDS-008 |
| Annulus monitoring method | Continuous pressure/vacuum monitoring | Periodic liquid sensing | Consider maintenance burden and detection speed; see Specification DWP-010 to DWP-013 |
| Extent of supply | Full marine loading system design by Contractor | Rely on OEM standard design | Clarify in Specification §1.4 Extent of Supply per Procedure Step 2 |

**ASSUMPTION:** Trade-off evaluation requires engineering judgment based on ER requirements, project stage, OEM capabilities, and coordination with adjacent packages.

## Examples

**Reference examples and precedents:**

Anticipated specification sections (from decomposition and scope):

| Section | Key Content | Requirement Count | Source Reference |
|---------|-------------|-------------------|------------------|
| §4 Loading Arm | Type, reach, ERC, materials, controls, safety | 32 requirements (MLA-001 to MLA-032) | DEL-11.06 OEM data, OCIMF guidelines |
| §5 Double-Walled Pipe | Design code, materials, annulus, testing | 20 requirements (DWP-001 to DWP-020) | ASME B31.3, API 2610 |
| §6 Leak Detection | Philosophy, devices, alarm/ESD, testing | 14 requirements (LDS-001 to LDS-014) | IEC 61511, project SIS requirements |
| §7 Nitrogen Supply | Purpose, source, pressure, interfaces | 7 requirements (N2-001 to N2-007) | Utilities design basis **TBD** |
| §8 Operator Shelter | Functional requirements, interfaces | 5 requirements (SHL-001 to SHL-005) | PKG-22 coordination |

**Source:** Specification.md §4–§8; Datasheet.md §Construction table; Procedure.md §Steps 3-6.

**Requirement verification matrix (example for each section):**
- Design review: Technical content verification (applies to most requirements)
- FAT: Factory acceptance testing (e.g., MLA-002 ERC, MLA-019 slew/luff speed)
- SAT: Site acceptance testing (e.g., MLA-026 remote control, LDS-007 leak alarm)
- Material certificates: Material compliance (e.g., MLA-013 wetted materials, DWP-005 inner pipe)
- Test records: Hydrostatic and leak testing (e.g., DWP-019, DWP-020)

**Source:** Specification.md verification columns for each requirement.

**Employer's Requirements expectations:** **TBD** until clause references are provided; see Specification.md §Compliance Matrix placeholder.

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| — | No conflicts identified at this stage | — | — | — | — | — |

*Note: Conflicts will be logged here when specific ER clauses are extracted and any discrepancies with decomposition scope, OEM capabilities, or technical standards are identified.*

---

**Pass 3 Enrichment Notes (Final Quality Check):**
- Verified cross-document alignment table: All 5 alignment checks confirmed accurate
  - Design basis: 11 parameters consistent across Datasheet/Specification/Procedure
  - Requirements: 5 sections with 58+ total (§4:32, §5:20, §6:14, §7:7, §8:5)
  - Interfaces: 8 interfaces with full traceability
  - Standards: 8 standards aligned
  - Acceptance: 5 criteria with 6-item verification checklist
- Verified all 5 Principles link to project objectives and Specification sections
- Verified 5 Considerations sections reference correct Specification requirement ID ranges
- Verified 6 Trade-offs reference appropriate Specification requirements (MLA-022, LDS-007, LDS-008, DWP-010 to DWP-013, §1.4)
- Verified Examples table includes all 5 specification sections with correct requirement counts
- Verified cross-deliverable alignment references (DEL-11.01 through DEL-11.06)
- Confirmed Conflict Table ready for use
- All TBDs and ASSUMPTIONs retained with explicit source citations
- Pass 3 complete — document ready for WORKING_ITEMS session
