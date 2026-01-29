# Guidance: DEL-08.03 Marine Structures Design Calculations

## Purpose

This document provides **engineering rationale and decision-making guidance** to support production of Marine Structures Design Calculations that are traceable, checkable, code-compliant, and aligned to the Employer's Requirements (ER).

**Deliverable intent (source-anchored):** Provides the engineering basis and sizing/verification calculations for marine structures. *(Source: Decomposition line 283 + `_CONTEXT.md`)*

**Package scope context (source-anchored):** PKG-08 covers piling, access trestle, loading platform structure, catwalk, and abutments. *(Source: Decomposition line 275)*

---

## Principles (Engineering Intent, Non-Invented)

Because the governing ER clauses and referenced standards are not yet extracted into this package, this guidance avoids asserting specific code requirements. The following principles are based on standard engineering calculation practice:

### Traceability from Source to Result
- **Intent:** Every input value, assumption, and design criterion must be traceable to a source document (drawing, report, code, ER clause)
- **Rationale:** Independent checkers and reviewers must be able to verify inputs and assumptions; untraceable inputs create audit failures and disputes
- **Practice:** Maintain an input register with document numbers and revisions; cite specific sections/pages/tables for input values; label assumptions explicitly

### Explicit Assumptions and Conservative Estimates
- **Intent:** Distinguish assumptions from facts; state when assumptions are conservative or require confirmation
- **Rationale:** Assumptions may need to be updated when better information becomes available; conservative assumptions provide safety margin but may be uneconomical; explicit labeling enables systematic review and update
- **Practice:** Label all assumptions as "ASSUMPTION"; maintain a consolidated assumptions list; note if assumption is conservative or needs confirmation; update calculations when assumptions are confirmed or revised

### Checkability and Auditability
- **Intent:** Calculations must be organized and documented so an independent checker can verify methods, inputs, and results without redoing the entire calculation
- **Rationale:** Independent check is a quality requirement (R-004); poorly documented calculations are uncheckable and delay project; litigation risk if calculations cannot be audited years later
- **Practice:** Provide calculation narrative explaining approach; show intermediate steps and logic; summarize results in tables; organize calculations by topic; use clear notation and consistent units

### Code Compliance and Professional Standards
- **Intent:** Calculations must comply with applicable codes/standards and meet professional engineering standards of practice
- **Rationale:** ER requires code compliance; professional engineering seal (P.Eng.) requires adherence to professional standards; non-compliance creates liability and regulatory risk
- **Practice:** Reference code clauses used; document design criteria and acceptance criteria; verify unity checks and margins; ensure calculations are sealed by licensed P.Eng. if required

---

## Requirement Rationale Map

This section links each Specification requirement to its engineering rationale and key considerations.

### R-001: Calculation Package Coverage (Minimum)

**What it requires:**
- Minimum calculation artifacts per Decomposition line 283: pile capacity calculations, trestle structural calculations, mooring analysis
- Coverage of all PKG-08 scope elements per Decomposition line 275: piling, access trestle, loading platform structure, catwalk, abutments
- Scope coordination with related calculation deliverables (DEL-08.06, DEL-08.09, DEL-08.10)

**Rationale:**
- Decomposition defines minimum calculation scope; R-001 ensures these minimum calculations are produced
- Completeness check against scope ensures all structural elements have engineering basis
- Scope coordination avoids duplication (e.g., mooring analysis may be in DEL-08.09; berthing energy in DEL-08.06) and ensures no gaps

**Key Considerations:**
- **Scope boundaries:** What calculations are in DEL-08.03 vs DEL-08.06/08.09/08.10? *(Recommend: DEL-08.03 includes structural design calculations using loads from DEL-08.06/08.09/08.10; specialized reports (berthing energy, mooring analysis) provide load inputs to DEL-08.03; confirm scope coordination in kickoff)*
- **Platform, catwalk, abutment calculations:** Decomposition lists pile capacity and trestle calculations; are platform, catwalk, abutment calculations also required? *(Likely yes based on PKG-08 scope (line 275); confirm and add to calculation scope)*
- **Connection design:** Are connection calculations in DEL-08.03 or separate deliverable? *(Recommend: include connection design in DEL-08.03 as part of structural calculations; connections critical to structural integrity)*

**Sources:**
- Decomposition line 283 (anticipated calculation artifacts)
- Decomposition line 275 (PKG-08 scope statement)

---

### R-002: Traceable Inputs, Assumptions, and Results

**What it requires:**
- Input register with document numbers, revisions, dates
- Input parameters with sources and citations
- Assumptions explicitly labeled and listed
- Calculation narrative and results documentation

**Rationale:**
- Input traceability enables independent verification and auditability; inputs change during design (e.g., updated drawings, revised geotechnical report); traceable inputs enable systematic update when inputs change
- Explicit assumptions enable review, confirmation, and update; assumptions are design risks that must be managed
- Calculation narrative and results documentation enable checking, review, and future reference

**Key Considerations:**
- **Input register format:** How detailed should input register be? *(Recommend: tabular format with columns: Input description, Value/reference, Source document, Document revision, Date, Notes; comprehensive but not excessive)*
- **Assumption management:** How to track and update assumptions? *(Recommend: consolidated assumptions list in calculation package; flag assumptions needing confirmation; update calculations when assumptions confirmed or revised; consider assumptions register for project-wide tracking)*
- **Calculation narrative level of detail:** How much narrative vs calculation detail? *(Balance: sufficient narrative to explain approach and logic; avoid excessive text that obscures calculation; use figures/sketches to clarify geometry and load paths; intermediate steps shown but not every arithmetic operation)*
- **Software calculations:** How to document software use? *(Require: software name, version, validation status; model description and assumptions; input file listing or summary; output file printout; hand check or benchmark verification of software results)*

**Sources:**
- Standard engineering calculation practice
- Project-specific requirements TBD from ER or project engineering procedures

---

### R-003: Design Methods, Criteria, and Code Compliance (ER-Driven)

**What it requires:**
- Calculation methods and criteria comply with ER requirements and codes/standards
- Design criteria documented (load cases, material properties, allowable stresses/resistance factors, serviceability criteria)
- Acceptance criteria stated

**Rationale:**
- ER defines contractual design requirements; code compliance is mandatory for regulatory approval and professional standards
- Design criteria documentation ensures consistent approach across calculations and enables review/verification
- Acceptance criteria provide objective pass/fail metric for design adequacy

**Key Considerations:**
- **Applicable codes:** Which codes/standards govern? *(TBD from ER; likely: CSA S6 for bridge-type structures, CSA S16 for steel design, API RP 2A for marine structures; confirm editions from ER)*
- **Load cases and combinations:** What load cases apply (dead, live, wind, current, wave, berthing, mooring, seismic)? What load combinations (ULS, SLS) per code or ER? *(TBD from ER and codes; load combinations critical for design; ensure all applicable load cases considered)*
- **Design approach:** Allowable stress design (ASD) or limit states design (LSD)? *(Likely LSD per CSA codes; confirm from ER and codes; affects load factors, resistance factors, acceptance criteria)*
- **Marine environment factors:** How to account for marine exposure (corrosion, marine growth, scour)? *(Corrosion allowance if applicable; scour depth assessment per DEL-08.04 or marine codes; marine growth on piles increases drag loads; confirm approach from ER and codes)*
- **Serviceability criteria:** What deflection limits, vibration limits apply? *(Deflection limits per code or ER; vibration limits for equipment-supporting structures may be more stringent; confirm from ER or equipment vendors)*
- **Geotechnical design approach:** How to design piles (geotechnical capacity vs structural capacity; governing limit state)? *(Use geotechnical parameters from DEL-08.04; pile capacity is lesser of geotechnical capacity and structural capacity; check both axial and lateral capacity; consider pile group effects)*

**Sources:**
- Decomposition line 283 (implicit ER compliance)
- ER requirements TBD from ER Vol 2 Parts 1-2
- Codes/standards TBD from ER

---

### R-004: Independent Check and Professional Seal

**What it requires:**
- Independent check by qualified engineer not involved in original calculations
- Check documentation and sign-off
- Professional seal (P.Eng.) if required by ER or regulatory requirements

**Rationale:**
- Independent check is quality assurance best practice and typically required by project QA/QC procedures; catches errors, omissions, non-conformances before issue
- Professional seal (P.Eng.) is legal requirement for structural engineering work in BC and most Canadian jurisdictions; provides professional accountability and public protection
- Unsealed or unchecked calculations may not be acceptable for regulatory approval or construction

**Key Considerations:**
- **Independent check scope:** What does checker verify? *(Full check: inputs, assumptions, methods, calculations, results; spot check: selected calculations or critical elements; confirm scope from project QA/QC procedures; recommend full check for critical structural calculations)*
- **Checker qualifications:** What qualifications required for independent checker? *(Qualified engineer with relevant experience in marine structures or structural engineering; may not need to be P.Eng. for check role, but calculations must be sealed by P.Eng. for issue)*
- **Check documentation:** How to document check? *(Checker markup on calculations with comments; comment register with resolutions; checker sign-off when satisfied; all check documentation retained in project archive)*
- **Professional seal requirement:** Is P.Eng. seal required? *(Likely yes for structural calculations in BC; confirm from ER or BC Building Code / Professional Governance Act; seal applied by licensed P.Eng. taking responsibility for calculations; seal on cover sheet with signature and date)*
- **Professional liability:** Who takes professional responsibility for calculations? *(P.Eng. applying seal; ensure P.Eng. is qualified and comfortable with calculations; P.Eng. may require changes or additional verification before sealing)*

**Sources:**
- Standard EPC QA/QC practice
- Professional engineering licensing requirements in BC (Engineers and Geoscientists BC)
- Project-specific requirements TBD from ER

---

### R-005: Calculation Package Format and Document Control

**What it requires:**
- Calculation package numbering, revision control, issue status per project document control
- Calculation format and organization (cover sheet, TOC, input register, calculations, summary, appendices)
- Calculation deliverable format (hand calcs, spreadsheets, software)

**Rationale:**
- Document control enables traceability, version control, and approval tracking
- Organized calculation package improves usability for checking, review, and future reference
- Clear format standards improve consistency and reduce misunderstandings

**Key Considerations:**
- **Calculation package organization:** How to organize multi-topic calculation package? *(Recommend: organize by topic (pile capacity, trestle structural, mooring analysis); each topic as separate section with own TOC sub-entry; summary table of results for each topic; cross-reference between topics where applicable)*
- **Hand calculations vs spreadsheets vs software:** When to use each? *(Hand calcs: simple, transparent, easy to check; good for preliminary design or simple elements; Spreadsheets: moderate complexity, formulas visible, easy to update; good for repetitive calculations (member checks, load combinations); Software: complex analysis (frame analysis, FEA); requires verification and documentation; use when hand/spreadsheet impractical; often combination of all three)*
- **Spreadsheet best practices:** How to make spreadsheets checkable? *(Clear input/output sections; formulas visible (not hidden); color coding or notation for inputs/calcs/outputs; summary sheets separate from calculation sheets; version control; lock formula cells to prevent inadvertent changes; include hand check or benchmark verification)*
- **Software verification:** How to verify software calculations? *(Software validation: verify software is appropriate and validated for use; model verification: hand check of simple case or benchmark against known solution; output verification: check results for reasonableness, check units, check for errors/warnings; document software version and validation status)*
- **Calculation revision control:** How to revise calculations during design? *(Use revision numbers/letters per project document control; revision table on cover sheet showing revision, date, description, originator, checker; highlight or markup revised sections in revised calculations; retain superseded revisions in project archive)*

**Sources:**
- Standard engineering calculation practice
- Project-specific requirements TBD from ER and project engineering/document control procedures

---

## Calculation Scope Checklist

Use this checklist to verify all required calculations (per `Specification.md` R-001) are addressed in the calculation package:

| Calculation Topic | Scope Element(s) Covered | Required (per Decomp) | Status |
|---|---|---|---|
| Pile capacity calculations | Piling | Yes (line 283) | **TBD** |
| Trestle structural calculations | Access trestle | Yes (line 283) | **TBD** |
| Mooring analysis | Structure loads from mooring | Yes (line 283) | **TBD** *(coordinate scope with DEL-08.09)* |
| Platform structural calculations | Loading platform structure | Inferred (line 275 scope) | **TBD** |
| Catwalk structural calculations | Catwalk | Inferred (line 275 scope) | **TBD** |
| Abutment structural calculations | Abutments | Inferred (line 275 scope) | **TBD** |
| Connection design calculations | All structural elements | Inferred (part of structural calc) | **TBD** |
| Berthing loads on structure | Structure loads from berthing | Likely covered in DEL-08.06 | **TBD** *(coordinate scope)* |
| Current loads on structure | Environmental loads | Likely covered in DEL-08.10 | **TBD** *(coordinate scope)* |

**Verification:** For each calculation topic, confirm it is included in DEL-08.03 or explicitly covered by another deliverable (cross-reference). Document scope coordination agreements.

---

## Trade-offs and Decisions

### Model Fidelity vs Transparency for Review

**Trade-off:** Detailed finite element models provide accurate results but are complex and difficult to check; simplified hand calculations or frame models are more transparent but may be less accurate or require conservative assumptions.

**Considerations:**
- **Complexity of structure:** Simple, regular structures (e.g., trestle with repetitive bays) may be adequately analyzed with simplified methods; complex, irregular structures may require detailed FEA
- **Checkability:** Can independent checker verify model? Detailed FEA models difficult to check without re-running analysis; simplified models easier to check
- **Design stage:** Preliminary design may use simplified methods for speed; final design may require detailed analysis for accuracy and optimization

**Decision:** **TBD** *(Recommend: use appropriate level of analysis for structure complexity and design stage; provide sufficient documentation and hand checks to enable verification; for complex FEA models, supplement with simplified hand check or benchmark to verify results reasonableness)*

### Conservative Assumptions vs Operational Realism

**Trade-off:** Conservative assumptions (e.g., maximum vessel size, worst-case environmental loading, simultaneous load combinations) provide safety margin but may result in uneconomical design; realistic assumptions reduce cost but require accurate data and increase risk if assumptions prove incorrect.

**Considerations:**
- **Data availability:** Are accurate inputs available (e.g., design vessel characteristics, site-specific environmental data)? If not, conservative assumptions may be necessary
- **Consequence of under-design:** What is consequence if assumptions prove incorrect and structure is under-designed? Marine structures with high consequence of failure may warrant conservative assumptions
- **Cost sensitivity:** Is design highly sensitive to assumptions (e.g., pile size/length)? Conservative assumptions that significantly increase cost may warrant more detailed study to refine assumptions

**Decision:** **TBD** *(Recommend: use realistic assumptions when accurate data available; use conservative assumptions when data uncertain or consequence of failure high; label assumptions and sensitivity; consider parametric study if assumptions highly uncertain or cost-sensitive)*

### Load Combination Philosophy

**Trade-off:** Code-prescribed load combinations may not cover all credible load scenarios for marine structures (e.g., simultaneous berthing, mooring, and environmental loads); additional load combinations may be warranted but increase calculation effort.

**Considerations:**
- **Code requirements:** What load combinations are required by code or ER? *(TBD from CSA S6, API RP 2A, or ER)*
- **Marine-specific load scenarios:** Are there marine-specific load scenarios not covered by code (e.g., vessel breakaway, abnormal berthing, tug assist operations)? *(Consider accidental/abnormal load cases per ER or marine engineering practice)*
- **Load coincidence:** What is probability of simultaneous occurrence (e.g., maximum wind, wave, and current at same time; berthing during storm)? *(Some load combinations may be inherently conservative if loads unlikely to occur simultaneously; consider load coincidence factors or reduced load factors for low-probability combinations)*

**Decision:** **TBD** *(Recommend: start with code-required load combinations; add marine-specific load scenarios per ER or engineering judgment; document load combination rationale and any deviations from code; obtain Employer approval for non-standard load combinations if required)*

---

## Conflict Table (for human ruling)

No conflicts identified from sources currently present in this deliverable folder.

If conflicts arise during calculation development (e.g., contradictory ER requirements, conflicting code requirements, inconsistent input data), document them here for human ruling:

| Conflict ID | Conflict (short statement) | Source A (file + section) | Source B (file + section) | Impacted calculations | Proposed authority (PROPOSAL) | Human ruling (TBD) |
|---|---|---|---|---|---|---|
| *(none)* | - | - | - | - | - | - |

---

## Sources

- `test/execution/PKG-08_Marine_Structures/1_Working/DEL-08.03_Marine_Structures_Design_Calculations/_CONTEXT.md`
- `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (lines 271-291: PKG-08 scope statement at line 275; deliverables table; DEL-08.03 at line 283)
- `test/Volume_2_Part_1_Employers_Requirements.pdf` *(present in repo; content not extracted here; clause locations TBD)*
- `test/Volume_2_Part_2_Employers_Requirements.pdf` *(present in repo; content not extracted here; clause locations TBD)*
- Standard engineering calculation practice (for input traceability, assumptions documentation, checkability, code compliance, professional seal requirements)
