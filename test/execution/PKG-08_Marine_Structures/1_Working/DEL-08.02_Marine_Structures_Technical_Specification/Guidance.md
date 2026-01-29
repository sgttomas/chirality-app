# Guidance: DEL-08.02 Marine Structures Technical Specification

## Purpose

This document provides **engineering rationale and decision-making guidance** to support development of a Marine Structures Technical Specification that is complete, auditable, constructible, and aligned to the Employer's Requirements (ER).

**Deliverable intent (source-anchored):** Defines performance, materials, and workmanship requirements for marine structures per ER requirements. *(Source: Decomposition line 282 + `_CONTEXT.md`; specific ER clause locations TBD)*

**Package scope context (source-anchored):** PKG-08 covers piling, access trestle, loading platform structure, catwalk, and abutments. *(Source: Decomposition line 275)*

---

## Principles (Engineering Intent, Non-Invented)

Because the governing ER clauses and referenced standards are not yet extracted into this package, this guidance avoids asserting specific code/standard requirements. The following principles are based on standard technical specification practice and the decomposition scope:

### Traceability and Auditability
- **Intent:** Every "shall" requirement in the specification must be traceable to an ER clause, code/standard clause, or approved design basis document
- **Rationale:** Technical specifications are contractual documents; unsourced requirements create liability and are unenforceable
- **Practice:** Maintain a requirements traceability matrix (RTM) mapping each "shall" requirement to its source (ER clause number, code clause number, or design basis document reference)

### Separation of Requirements from Guidance
- **Intent:** Distinguish mandatory requirements ("shall") from recommended practices ("should") and informative guidance ("may")
- **Rationale:** Constructors must know what is mandatory vs recommended; mixing requirements and guidance creates confusion and disputes
- **Practice:** Use "shall" only for mandatory requirements; use "should" for recommended practices; use "may" for permissible options

### Constructibility and Clarity
- **Intent:** Specifications must provide clear, unambiguous requirements that fabricators and constructors can follow
- **Rationale:** Vague or conflicting requirements cause RFIs, delays, and disputes; overly prescriptive requirements may be unconstructible or uneconomical
- **Practice:** Review specifications with fabricators/constructors before issue (constructability review); use standard industry terminology; avoid ambiguous terms like "appropriate" or "adequate" without defining criteria

### Marine Environment Considerations
- **Intent:** Specifications must address marine environment exposure (corrosion, marine growth, tidal/wave action, vessel impacts)
- **Rationale:** Marine structures have unique durability and performance requirements compared to land-based structures
- **Practice:** Specify marine-grade materials, corrosion protection systems appropriate for marine exposure classification, inspection/maintenance provisions for submerged/intertidal components

---

## Requirement Rationale Map

This section links each Specification requirement to its engineering rationale and key considerations.

### R-001: Specification Coverage (Minimum)

**What it requires:**
- Minimum specification artifacts per Decomposition line 282: marine piling specification, structural steel specification (marine)
- Coverage of all PKG-08 scope elements per Decomposition line 275: piling, access trestle, loading platform structure, catwalk, abutments

**Rationale:**
- Decomposition defines the minimum deliverable scope; R-001 ensures these minimum specifications are produced
- Completeness check against scope ensures no scope element lacks specification coverage
- Separate specifications for piling vs structural steel reflect different materials, fabrication processes, installation methods, and inspection requirements

**Key Considerations:**
- **Specification breakdown strategy:** Should trestle, platform, catwalk, abutments each have separate structural steel specifications, or can they share a common specification? *(Trade-off: more specifications = more specificity but more documents to manage; recommend: single structural steel specification with sections for each component type; TBD based on ER requirements and project preferences)*
- **Scope boundaries:** What is included vs excluded in each specification? *(e.g., Are pile splices included in piling spec or structural steel spec? Are cathodic protection systems in piling spec or separate spec? TBD based on ER and design basis)*
- **Interface to other packages:** Are fenders/bollards/ladders (PKG-09 scope) covered in a separate specification or noted as interface in DEL-08.02? *(TBD based on package boundaries and design coordination)*

**Sources:**
- Decomposition line 282 (anticipated artifacts list)
- Decomposition line 275 (PKG-08 scope statement)

---

### R-002: ER-Driven Requirements Capture

**What it requires:**
- Specifications incorporate all applicable ER requirements for marine structures materials, performance, workmanship, inspection/testing, documentation
- ER clauses, codes/standards, requirements traceability: TBD

**Rationale:**
- ER is the contractual requirements document; compliance is mandatory
- Decomposition states deliverable is "per ER requirements" (line 282), so ER clauses must be identified and incorporated
- Requirements traceability enables compliance verification and audit trail; reduces disputes over interpretation

**Key Considerations:**
- **ER clause identification:** Which ER clauses apply to marine structures specifications? *(TBD; requires systematic review of ER Vol 2 Parts 1-2; likely sections on materials, workmanship, inspection/testing, QA/QC, submittals)*
- **Code/standard compliance:** Which codes/standards are mandated by ER vs referenced for best practice? *(TBD; ER may mandate specific codes/editions; specifications must reference correct editions)*
- **Conflicts between ER and codes:** If ER requirements conflict with standard codes, how are conflicts resolved? *(Typical: ER takes precedence; note conflicts and seek Employer clarification; TBD based on ER hierarchy-of-requirements clause)*
- **ER interpretation:** Are there ambiguous or unclear ER clauses that require clarification? *(If yes, prepare Request for Information (RFI) or clarification request to Employer; document assumptions in specification and flag for confirmation)*

**ASSUMPTION:** ER Vol 2 Parts 1-2 contain marine structures specification requirements; specific clauses/sections TBD pending extraction.

**Sources:**
- Decomposition line 282 ("per ER requirements")
- ER Vol 2 Parts 1-2 PDFs (available in repo; content not yet extracted)

---

### R-003: Technical Specification Structure and Content

**What it requires:**
- Specifications include required minimum content sections (scope, definitions, references, materials, fabrication, installation, corrosion protection, inspection/testing, submittals/records)
- Content completeness: all sections included or marked TBD with resolution plan

**Rationale:**
- Complete specification structure ensures all aspects of materials, fabrication, installation, inspection are addressed
- Standard section structure improves usability for fabricators/constructors and reduces ambiguity
- Missing sections create gaps in requirements that cause RFIs and construction delays

**Key Considerations:**
- **Marine Piling Specification:**
  - **Materials:** What pile types and grades are required? *(TBD from DEL-08.03 design calculations and ER; likely: steel pipe piles per ASTM A252 or API Spec 2B; grade/wall thickness TBD based on geotechnical and structural design)*
  - **Corrosion protection:** What coating systems or cathodic protection are required for marine environment? *(TBD from ER and marine corrosion design basis; likely: marine-grade epoxy coatings for splash zone, below-waterline coatings or cathodic protection for submerged zone)*
  - **Installation:** What pile driving criteria and minimum penetration are required? *(TBD from DEL-08.04 geotechnical report; driving criteria based on pile capacity and soil resistance)*
  - **Pile integrity testing:** What testing is required (e.g., PDA, sonic echo, load testing)? *(TBD from ER and geotechnical recommendations; may vary based on pile type and loading)*
- **Structural Steel Specification (Marine):**
  - **Materials:** What steel grades are required for marine environment? *(TBD from DEL-08.03 design calculations and ER; likely: CSA G40.21 Grade 350W or ASTM A709 Grade 50W for weathering steel, or equivalent with corrosion protection)*
  - **Corrosion protection:** What coating systems are required for marine exposure? *(TBD from ER and marine corrosion design basis; likely: multi-coat epoxy or polyurethane coating systems; coating thickness and application requirements TBD from SSPC/NACE standards or ER)*
  - **Welding:** What welding standards and qualifications are required? *(TBD from ER; likely: CSA W59 for Canadian projects or AWS D1.1 if specified; welder qualifications, WPS, NDT requirements TBD)*
  - **Marine environment exposure classification:** What exposure zones apply (splash zone, tidal zone, atmospheric zone)? *(TBD from design basis; affects coating system selection and inspection requirements)*
  - **Cathodic protection:** Is cathodic protection required? *(TBD from ER and marine corrosion design basis; may be required for submerged/intertidal components; if yes, specify type (sacrificial anodes or impressed current) and design criteria)*
- **Section content depth:** How detailed should each section be? *(Typical: provide performance requirements and acceptance criteria; reference industry standards for detailed procedures; avoid over-prescribing methods unless required by ER or critical for performance)*

**Sources:**
- Standard marine engineering technical specification practice
- ER requirements TBD from ER Vol 2 Parts 1-2
- Project specification template TBD from ER or project procedures

---

### R-004: Interface Coordination

**What it requires:**
- Cross-references and coordination with related deliverables (DEL-08.01 drawings, DEL-08.03 calculations, DEL-08.04 geotechnical, DEL-08.05 installation/test records)
- Interface points noted in specifications

**Rationale:**
- Specifications must be consistent with drawings (materials noted on drawings must match specification grades)
- Specifications must be informed by calculations (material grades and connection details must satisfy structural design requirements)
- Specifications must be testable (inspection/testing requirements must align with installation/test records scope)
- Cross-references enable users to navigate between related documents and avoid conflicting information

**Key Considerations:**
- **Interface to DEL-08.01 Marine Structures Design Drawing Set:**
  - Ensure materials noted on drawings (e.g., "Steel per SPEC-08-002") reference correct specification number and section
  - Ensure drawing notes for welding, coatings, tolerances are consistent with specification requirements
  - **Coordination mechanism:** Review drawings against specifications during IDC check; resolve discrepancies before issue — **TBD**
- **Interface to DEL-08.03 Marine Structures Design Calculations:**
  - Ensure material grades specified meet structural design requirements (yield strength, tensile strength)
  - Ensure connection details specified (bolt grades, weld sizes) match calculation requirements
  - **Coordination mechanism:** Provide calculations to specification writer; cross-check material grades and connection details — **TBD**
- **Interface to DEL-08.04 Marine Geotechnical Report:**
  - Ensure piling specification driving criteria and minimum penetration are consistent with geotechnical recommendations
  - Ensure pile capacity assumptions in specification align with geotechnical pile capacity
  - **Coordination mechanism:** Extract pile capacity and installation criteria from DEL-08.04; incorporate into piling specification — **TBD**
- **Interface to DEL-08.05 Marine Structures Installation & Test Records:**
  - Ensure inspection/testing requirements in specifications are documented in installation/test records
  - Ensure submittal requirements in specifications align with records scope (e.g., specification requires pile driving logs; DEL-08.05 includes pile driving logs)
  - **Coordination mechanism:** Cross-check specification submittal/testing requirements against DEL-08.05 scope during IDC — **TBD**

**Sources:**
- Standard EPC practice for multi-discipline coordination
- Decomposition scope indicates interfaces to DEL-08.01, DEL-08.03, DEL-08.04, DEL-08.05
- `_DEPENDENCIES.md` (mode: NOT_TRACKED; dependencies coordinated externally)

---

### R-005: Document Control / Metadata

**What it requires:**
- Compliance with project document control requirements (numbering, revision, header/footer)

**Rationale:**
- Document control enables traceability, version control, and approval tracking
- Construction and regulatory approvals require controlled documents with clear revision status
- Project-wide consistency in numbering/revisioning simplifies document management

**Key Considerations:**
- **Document numbering scheme:** How are specifications numbered? *(TBD; typical: discipline code + package code + type code + sequence, e.g., SPEC-MAR-08-001 for piling, SPEC-MAR-08-002 for structural steel)*
- **Revision scheme:** What revision codes are used (A/B/C for internal; 0/1/2 for issued)? *(TBD from project document control procedures)*
- **Header/footer template:** What information is required in headers/footers? *(TBD from project specification template; typically: document title, document number, revision, date, page number, project name, classification)*
- **Integration with document management system:** How are specifications submitted, tracked, and archived in project document management system? *(TBD from project document control procedures)*

**ASSUMPTION:** Project document control procedures exist and are defined in ER or project document control plan; clause/section location TBD.

**Sources:**
- Standard EPC practice for document control
- Project-specific requirements TBD from ER and project document control plan

---

## Specification Content Checklist

Use this checklist to verify all required content sections (per `Specification.md` R-003) are addressed in each specification:

### Marine Piling Specification Content Checklist

| Section | Content Summary | Status |
|---|---|---|
| Scope and Applicability | Pile types covered; exclusions; interface to other specs | **TBD** |
| Definitions and Abbreviations | Terms/acronyms defined | **TBD** |
| Referenced Standards and Codes | Codes for materials, fabrication, installation, testing (with editions) | **TBD** |
| Materials | Pile material grades; coatings; fasteners; welding consumables; material testing/certification | **TBD** |
| Fabrication and Workmanship | Fabrication tolerances; welding requirements; surface prep; coating application; shop inspection | **TBD** |
| Installation Requirements | Driving criteria; installation tolerances; minimum penetration; cut-off elevations; driving records | **TBD** |
| Inspection and Testing | NDT; pile integrity testing; load testing; acceptance criteria | **TBD** |
| Submittals and Records | Shop drawings; material certs; welding docs; test reports; as-builts | **TBD** |

**Verification:** For each section, confirm content is populated from ER, codes/standards, or design basis. If content cannot yet be determined, mark **TBD** with resolution plan.

### Structural Steel Specification (Marine) Content Checklist

| Section | Content Summary | Status |
|---|---|---|
| Scope and Applicability | Components covered (trestle, platform, catwalk, abutments); exclusions; interface to other specs | **TBD** |
| Definitions and Abbreviations | Terms/acronyms defined | **TBD** |
| Referenced Standards and Codes | Codes for materials, fabrication, welding, erection (with editions) | **TBD** |
| Materials | Steel grades; bolts/fasteners; welding consumables; coatings; material testing/certification | **TBD** |
| Fabrication and Workmanship | Fabrication tolerances; welding requirements; bolting; surface prep; coating application; shop inspection | **TBD** |
| Erection/Installation Requirements | Erection tolerances; bolting/welding procedures; field welding; temporary bracing; erection sequence | **TBD** |
| Corrosion Protection | Marine exposure classification; coating systems; surface prep standards; coating inspection; cathodic protection | **TBD** |
| Inspection and Testing | Weld inspection (visual, NDT); dimensional inspection; bolting; coating; acceptance criteria | **TBD** |
| Submittals and Records | Shop drawings; material certs; WPS/WPQ; test reports; as-builts | **TBD** |

**Verification:** For each section, confirm content is populated from ER, codes/standards, or design basis. If content cannot yet be determined, mark **TBD** with resolution plan.

---

## Trade-offs and Decisions

### Prescriptive vs Performance-Based Specifications

**Trade-off:** Prescriptive specifications specify exact materials, methods, and procedures; performance-based specifications specify performance criteria and allow contractor flexibility in means/methods.

**Considerations:**
- **Prescriptive:** Provides more control over quality; reduces variability; may be less constructible or cost-effective; requires detailed knowledge of methods
- **Performance-based:** Allows contractor innovation; may be more cost-effective; requires clear performance criteria and acceptance testing; may have higher risk if performance not achieved

**Decision:** **TBD** *(depends on ER approach and project risk tolerance; likely: hybrid approach with prescriptive requirements for critical items (e.g., material grades, corrosion protection) and performance-based requirements for less critical items (e.g., fabrication methods))*

### Fabrication and Installation Tolerances

**Trade-off:** Tight tolerances improve fit and finish but increase fabrication/installation cost and difficulty; loose tolerances reduce cost but may affect performance, aesthetics, or interfacing components.

**Considerations:**
- Tolerances must be achievable with standard fabrication/construction methods and equipment
- Tolerances must satisfy structural design requirements (e.g., load eccentricity limits)
- Tolerances must be compatible with interfacing components (e.g., fender mounting plates, loading arm support structures)

**Decision:** **TBD** *(recommend: adopt industry standard tolerances from codes/standards (e.g., CSA S16, AISC) unless tighter tolerances required by design; verify with fabricator/constructor during constructability review)*

### Marine Corrosion Protection Strategy

**Trade-off:** Multiple coating systems available (epoxy, polyurethane, zinc-rich primers, etc.); cathodic protection (sacrificial anodes vs impressed current); trade-offs in initial cost, durability, maintenance requirements.

**Considerations:**
- Marine exposure classification (splash zone, tidal zone, submerged zone, atmospheric zone)
- Coating durability and service life requirements (design life per ER: TBD)
- Maintenance access and maintenance intervals (accessibility of submerged/intertidal components)
- Compatibility with materials and fabrication processes

**Decision:** **TBD** *(requires marine corrosion design basis; typical: multi-coat epoxy or polyurethane coating systems for above-water components; cathodic protection (sacrificial anodes) for submerged/intertidal steel components; confirm from ER and marine engineering standards)*

---

## Conflict Table (for human ruling)

No conflicts identified from sources currently present in this deliverable folder.

If conflicts arise during specification development (e.g., contradictory ER requirements, conflicting code requirements), document them here for human ruling:

| Conflict ID | Conflict (short statement) | Source A (file + section) | Source B (file + section) | Impacted sections | Proposed authority (PROPOSAL) | Human ruling (TBD) |
|---|---|---|---|---|---|---|
| *(none)* | - | - | - | - | - | - |

---

## Sources

- `test/execution/PKG-08_Marine_Structures/1_Working/DEL-08.02_Marine_Structures_Technical_Specification/_CONTEXT.md`
- `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (lines 271-291: PKG-08 scope statement at line 275; deliverables table; DEL-08.02 at line 282)
- `test/Volume_2_Part_1_Employers_Requirements.pdf` *(present in repo; content not extracted here; clause locations TBD)*
- `test/Volume_2_Part_2_Employers_Requirements.pdf` *(present in repo; content not extracted here; clause locations TBD)*
- Standard marine engineering technical specification practice (for specification structure, content, constructibility, corrosion protection)
