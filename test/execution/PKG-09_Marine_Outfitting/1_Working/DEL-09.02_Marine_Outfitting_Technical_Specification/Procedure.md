# Procedure: DEL-09.02 Marine Outfitting Technical Specification

## Purpose

This procedure defines the process for producing and verifying **Marine Outfitting Technical Specification** within **PKG-09 Marine Outfitting**.

**Decomposition definition (authoritative):** Defines performance, materials, and workmanship requirements for marine outfitting per Employer's Requirements. (**Source:** Decomposition, DEL-09.02 row)

**Deliverable type:** Specification
**Responsible party:** D&B Contractor

**Scope:** This procedure covers the specification development process from scope confirmation through issue preparation, including requirements extraction, drafting, checking, interdisciplinary coordination, and verification activities.

## Prerequisites

### Dependencies

Dependencies are coordinated externally (NOT_TRACKED). See `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`.

**Typical upstream inputs (confirm availability and maturity prior to commencement):**

| Input | Source | Required For | Specification § | Guidance § |
|-------|--------|--------------|-----------------|------------|
| Employer's Requirements (applicable clauses) | Employer | All requirements; scope; codes/standards; quality; submittals | SPEC § 1.1, 1.2, 1.6, 1.7, 2 (all) | — |
| Berthing energy calculation results | DEL-08.06 | Fender performance requirements (energy absorption, reaction force limits) | SPEC § 1.3, 2.1 | Guidance § Principles (Fenders) |
| Mooring analysis results | DEL-08.09 | Bollard capacity requirements (SWL, design loads) | SPEC § 1.3, 2.2 | Guidance § Principles (Bollards) |
| Fender system deflection characteristics | DEL-08.07 | Fender deflection characteristics for specification | SPEC § 2.1 | Guidance § Principles (Fenders) |
| Fender supplier design verification | DEL-08.08 | Fender suitability confirmation | SPEC § 2.1 | Guidance § Principles (Fenders) |
| Marine structure interface data and capacities | PKG-08 outputs (DEL-08.01, DEL-08.03) | Interface requirements; structural capacity verification | SPEC § 3.1 | Guidance § Considerations (Interface Coordination) |
| Applicable codes and standards | Employer / Regulatory Authority | Codes list; compliance requirements | SPEC § 1.2, Standards | Guidance § Considerations |
| Vendor/OEM preliminary data | Vendor | Material requirements; testing capabilities | SPEC § 2.1, 2.2, 2.3 | — |

### Reference Materials

- See `_REFERENCES.md` for applicable reference documents.
- See `0_References/` in package directory (`test/execution/PKG-09_Marine_Outfitting/0_References/`) for reference materials and reference index.
- Employer's Requirements (Vol 2 Part 1–3) — **TBD** (clauses applicable to marine outfitting to be extracted during specification development).
- Applicable codes and standards — **TBD** (as specified by Employer's Requirements and approvals; see `Specification.md § Standards` and `Guidance.md § Principles` for assumed standards list).

### Personnel Requirements

| Role | Requirement |
|------|-------------|
| Originator (Lead Specifier) | Qualified Marine discipline personnel with experience in marine terminal design, equipment specifications, and marine outfitting — **TBD** (qualifications per project quality plan) |
| Checker/Reviewer | Checker qualifications — **TBD** (independent of originator; qualified in Marine discipline or relevant specification experience) |
| IDC participants | Representatives from interfacing disciplines (PKG-08 Marine Structures, PKG-11 Marine Loading, PKG-26 Protective Coatings if applicable, others as needed) |
| Approver | **TBD** — per project authority matrix (typically Marine discipline lead or Package Manager) |

**ASSUMPTION:** Personnel competency and authority per project quality procedures and authority matrix.

### Tools and Resources

| Tool/Resource | Purpose | Status |
|---------------|---------|--------|
| Word processing software | Specification drafting | **TBD** — project-standard software (e.g., Microsoft Word, Google Docs) |
| Project document control system | Document numbering, revision control, transmittal | **TBD** — system to be established |
| Requirements extraction tool/template | Track ER clauses and requirements | **TBD** — **ASSUMPTION:** Spreadsheet or database for requirements traceability |
| Code/standard access | Reference codes and standards during drafting | **TBD** — library access or online subscriptions |

## Steps

### Step 1: Confirm Scope

**Objective:** Establish the specification scope and confirm scope boundaries.

**Actions:**
1. Review PKG-09 scope items and DEL-09.02 anticipated artifacts from the decomposition:
   - Fender specification
   - Bollard specification
   - Marine hardware specification
2. Review `Datasheet.md` Content Checklist for minimum specification content requirements.
3. Confirm what is included under "marine hardware specification":
   - Ladders (types, locations)
   - Life-saving equipment (types, coverage)
   - Miscellaneous items (toe rails, signage, Berth 10 upgrades/repairs)
4. Confirm scope boundaries with interfacing packages:
   - PKG-08 Marine Structures: Where does structural design end and outfitting begin? (e.g., are structural supports for fenders/bollards in PKG-08 or PKG-09?)
   - PKG-11 Marine Loading System: Interface scope boundaries (operational clearances, safety zones)
   - PKG-26 Protective Coatings (if applicable): Corrosion protection responsibility split
5. Document any scope clarifications or boundary decisions.
6. Prepare preliminary specification outline based on `Specification.md § 1` structure requirements and `Guidance.md § Examples (Typical Specification Sections)`.

**Inputs:** Decomposition, `Datasheet.md`, `Specification.md`, `Guidance.md`.
**Outputs:** Confirmed specification scope; scope clarification notes (if any); preliminary specification outline.
**Verification:** Specification scope addresses all `Datasheet.md` Content Checklist items and `Specification.md § 1–2` requirements; scope boundaries documented.

### Step 2: Extract Requirements from Sources

**Objective:** Collect and extract all requirements from Employer's Requirements, codes/standards, and design inputs.

**Actions:**
1. **Extract Employer's Requirements clauses:**
   - Identify applicable ER volumes and sections for marine outfitting (Vol 2 Part 1–3).
   - Extract clauses related to:
     - Scope and general requirements
     - Fender system requirements (performance, materials, testing)
     - Bollard requirements (capacity, materials, testing, proof load)
     - Ladder and access requirements (safety features, materials, codes)
     - Life-saving equipment requirements (types, coverage, regulations)
     - Corrosion protection requirements (coating systems, galvanizing)
     - Quality and inspection requirements (hold/witness points, certifications)
     - Submittal requirements (datasheets, certificates, calculations, ITPs)
   - Record ER clauses in requirements extraction log with traceability (ER volume, section, clause number).
2. **Identify applicable codes and standards:**
   - Extract codes/standards list from Employer's Requirements (if specified).
   - Supplement with industry-standard codes where ER is silent (coordinate with Project Manager / Technical Lead for approval):
     - PIANC guidelines for fender systems
     - BS 6349 or equivalent for bollards and mooring equipment
     - OSHA / CSA safety codes for ladders and access
     - Transport Canada or port authority requirements for life-saving equipment
     - Material standards (ASTM, ISO)
     - Welding standards (AWS)
   - Record codes/standards in requirements extraction log with applicability notes.
3. **Obtain design inputs:**
   - Request berthing energy analysis results (DEL-08.06) — extract design berthing energy, vessel characteristics, approach velocity, environmental conditions.
   - Request mooring analysis results (DEL-08.09) — extract bollard capacities (SWL), mooring line loads, environmental conditions.
   - Request fender system data (DEL-08.07, DEL-08.08) — extract deflection characteristics, performance data, supplier verification.
   - Request PKG-08 interface information — structural geometry, connection details, structural capacities for marine outfitting loads.
4. **Log missing inputs:**
   - For each missing input, record as **TBD** with action owner and target date.
   - Establish input register to track receipt and maturity of inputs.
5. **Prepare requirements extraction log:**
   - Tabulate all extracted requirements with source traceability (ER clause, code clause, calculation reference, project decision).
   - Organize by specification section (per preliminary outline from Step 1).

**Inputs:** Employer's Requirements (Vol 2 Part 1–3), codes/standards, design inputs (DEL-08.06, DEL-08.07, DEL-08.08, DEL-08.09, PKG-08 outputs), `Specification.md § 1–2`, `Guidance.md § Principles`.
**Outputs:** Requirements extraction log with source traceability; codes/standards list; design inputs register; missing inputs log with action owners.
**Verification:** Requirements extraction log is complete and organized by specification section; all sources cited; missing inputs have action owners assigned and reviewed with Project Manager or Package Lead.

### Step 3: Draft Specification

**Objective:** Draft specification sections with requirements derived from extracted sources.

**Actions:**
1. **Draft structure sections (per `Specification.md § 1`):**
   - **Scope and Definitions (§ 1.1):** Scope statement with inclusions/exclusions; definitions and abbreviations; referenced documents list (standards, codes, drawings, calculations, related deliverables).
   - **Applicable Codes and Standards (§ 1.2):** List of codes/standards from requirements extraction (Step 2); cite specific designations and editions.
   - **Design Basis (§ 1.3):** State design vessel characteristics, environmental conditions, service life (from requirements extraction and design inputs).
   - **Corrosion Protection Requirements (§ 1.4):** Define exposure classification (immersed, splash, atmospheric); specify coating systems, galvanizing, stainless steel requirements (from ER and PKG-08/PKG-26 coordination).
   - **Installation Requirements (§ 1.5):** Specify setting-out tolerances, fixing methods, environmental conditions for installation, interface requirements with PKG-08.
   - **Quality / Inspection Requirements (§ 1.6):** Specify inspection/testing requirements, hold/witness points, certification requirements, non-conformance procedures (from ER and project quality plan).
   - **Submittal Requirements (§ 1.7):** List required submittals (datasheets, certificates, calculations, ITPs) with cross-reference to DEL-09.03, DEL-09.04, DEL-09.05; specify submittal review/approval process.
2. **Draft equipment requirements sections (per `Specification.md § 2`):**
   - **Fender Requirements (§ 2.1):** Specify performance (energy absorption, reaction force limits, deflection characteristics), materials (rubber compound, steel backing, fasteners), workmanship (manufacturing quality, tolerances), testing (FAT, proof load if required), installation (mounting, alignment).
   - **Bollard Requirements (§ 2.2):** Specify performance (SWL, design load factors, proof load if required), materials (steel type/grade, base plate, anchor bolts, grout), workmanship (welding, finishing, tolerances), testing (proof load testing if required, NDT, material testing), installation (foundation, grouting, alignment).
   - **Marine Hardware Requirements (§ 2.3):** Specify ladder requirements (types, materials, safety features, structural requirements, fixing), life-saving equipment requirements (equipment list, performance, materials, installation), miscellaneous hardware requirements (Berth 10 upgrades, other items as applicable).
3. **Write requirements in verifiable terms:**
   - Each requirement should have clear acceptance criteria (what is acceptable/not acceptable).
   - Performance requirements should be measurable (energy in kJ, load in kN, deflection in mm or %).
   - Material requirements should cite specific standards/grades (e.g., "ASTM A572 Grade 50").
   - Test requirements should specify test method, acceptance criteria, reporting requirements.
   - Avoid vague language like "suitable," "appropriate," "adequate" without defining criteria.
4. **Cite sources for each requirement:**
   - Reference requirements extraction log for source traceability.
   - Format citations consistently (e.g., "(per ER Vol 2 Part 1 § 3.4.2)" or "(per BS 6349-4:2014 § 5.3)" or "(per DEL-08.06 § 4.2)").
   - Where a requirement is inferred or assumed, label **ASSUMPTION** and cite basis.
   - Where information is missing, mark **TBD** and note needed source/input.
5. **Cross-reference related deliverables:**
   - Reference DEL-09.01 drawings where implementation details are shown.
   - Reference DEL-09.03 calculations where performance is substantiated.
   - Reference DEL-09.04 datasheets where equipment compliance is demonstrated.
   - Reference DEL-09.05 records where installation/test compliance is verified.
6. **Ensure consistency with Guidance:**
   - Verify that requirements align with design principles and considerations in `Guidance.md`.
   - Check that trade-offs discussed in `Guidance.md` are resolved appropriately in requirements.

**Inputs:** Requirements extraction log (Step 2), specification outline (Step 1), `Specification.md § 1–2`, `Guidance.md § Principles and Considerations`.
**Outputs:** Draft specification document with all sections; requirements written in verifiable terms with source citations.
**Verification:** All `Datasheet.md` Content Checklist items addressed; all `Specification.md § 1–2` requirements met; requirements written in verifiable terms; all non-trivial requirements cite sources or marked TBD/ASSUMPTION.

### Step 4: Quality/Testing Requirements

**Objective:** Define inspection, testing, and certification requirements; define submittal requirements.

**Actions:**
1. **Define inspection and testing requirements for each equipment category:**
   - **Fenders:** Factory acceptance testing (FAT) — compression testing, deflection verification, visual inspection, dimensional verification; material property testing (rubber hardness, tensile strength); proof load testing (if required).
   - **Bollards:** Proof load testing (if required by ER/codes) — test load, procedure, acceptance criteria, reporting; non-destructive testing (visual, magnetic particle, ultrasonic) for welds; material testing (mill test reports, mechanical properties).
   - **Ladders:** Material testing (mill test reports, coating thickness); load testing (if required); dimensional verification; safety feature inspection (cage clearances, rung spacing).
   - **Life-saving equipment:** Performance testing per applicable regulations (buoyancy, strength, visibility); certifications (regulatory compliance, product certifications).
2. **Define hold and witness points:**
   - **Hold points:** Work shall not proceed without inspector approval (list critical activities requiring hold points).
   - **Witness points:** Inspector shall be notified but work may proceed if inspector not available (list activities requiring witness points).
   - **TBD:** Specific hold/witness points to be defined per project quality plan and Employer's Requirements (coordinate with project QA/QC lead).
3. **Define certification requirements:**
   - Material test reports (MTRs) / mill certificates for steel components
   - Welding procedure specifications (WPS) and welder qualifications (per AWS D1.1 or equivalent)
   - Coating inspection reports and dry film thickness (DFT) measurements (per coating system specification)
   - Proof load test certificates (bollards, if required) — test results, load curves, acceptance certification
   - Product certifications (life-saving equipment per regulations, ladder safety features per codes)
   - **TBD:** Specific certification requirements per ER and project quality plan.
4. **Define submittal requirements (cross-reference related deliverables):**
   - Data sheets (DEL-09.04) — specify format, content, approval process
   - Certificates and test reports — specify types, formats, approval requirements
   - Calculations (DEL-09.03) — specify scope of calculations required (fender energy absorption, bollard capacity, ladder structural adequacy)
   - Inspection and test plans (ITPs) — specify scope, format, approval process (cross-reference DEL-09.05)
   - Installation procedures — specify when required (complex installations, critical activities)
   - As-built documentation — specify requirements for as-installed conditions (revisions to DEL-09.01 drawings)
5. **Define submittal review and approval process:**
   - Specify submittal schedule and lead times (coordinate with construction schedule).
   - Specify review/approval workflow (contractor submission → engineer review → approval/comments).
   - Specify approval categories (e.g., "Approved," "Approved as Noted," "Revise and Resubmit").
   - **TBD:** Submittal process per project document control procedures.
6. **Cross-reference DEL-09.05 for installation test record requirements:**
   - Ensure specification requirements align with DEL-09.05 record-keeping expectations.
   - Specify what records shall be produced and retained (installation records, test reports, inspection checklists, certifications).

**Inputs:** Draft specification (Step 3), `Specification.md § 1.6, 1.7`, `Guidance.md § Principles`, project quality plan, Employer's Requirements.
**Outputs:** Quality/testing section of specification (§ 1.6); submittal requirements section (§ 1.7); hold/witness points list; certification requirements list.
**Verification:** Quality/testing requirements are complete and verifiable; hold/witness points identified; submittal requirements cross-reference related deliverables (DEL-09.03, DEL-09.04, DEL-09.05); requirements align with project quality plan and ER.

### Step 5: Self-Check

**Objective:** Verify completeness, consistency, traceability, and verifiability before circulating for IDC/independent check.

**Actions:**
1. **Verify coverage against `Datasheet.md` Content Checklist:**
   - Check that all Content Checklist items are addressed (either resolved or noted as TBD with action owner).
   - Verify that all decomposition-listed artifacts (fender specification, bollard specification, marine hardware specification) are covered.
2. **Verify compliance with `Specification.md § 1–2` requirements:**
   - Check that all structure sections (§ 1.1–1.7) are included and complete.
   - Check that all equipment requirements sections (§ 2.1–2.3) are included and complete.
   - Verify that interface/coordination requirements (§ 3) are addressed.
   - Verify that quality/traceability requirements (§ 4) are met.
3. **Verify internal consistency:**
   - Check terminology consistency (same terms used consistently throughout specification).
   - Check cross-references (all referenced documents, drawings, calculations, standards are listed and cited correctly).
   - Check units and values consistency (consistent use of SI units, values match across sections).
4. **Verify traceability:**
   - Check that each non-trivial requirement cites source (ER clause, code/standard clause, calculation reference, project decision).
   - Check that TBDs are marked and have noted source/input needed.
   - Check that ASSUMPTIONs are labeled and have cited basis.
   - Use requirements extraction log (Step 2) to verify traceability completeness.
5. **Verify verifiability:**
   - Check that requirements are written in verifiable terms (measurable criteria, clear acceptance criteria).
   - Check that test methods and acceptance criteria are specified where applicable.
   - Avoid vague language without defined criteria.
6. **Verify cross-document consistency:**
   - Check that specification requirements align with `Guidance.md` principles and considerations.
   - Check that specification structure matches `Datasheet.md` Content Checklist.
   - Check that requirements reference `Procedure.md` verification steps (e.g., "per Procedure § Step 6 IDC").
7. **Document self-check completion:**
   - Prepare self-check record/sign-off per project procedures.
   - Log any self-check issues found and resolved.

**Inputs:** Draft specification (Steps 3, 4), `Datasheet.md`, `Specification.md`, `Guidance.md`, requirements extraction log.
**Outputs:** Self-check record; self-check issues log (if any) with resolutions; specification ready for IDC.
**Verification:** Self-check completed and documented; all issues resolved or noted as TBD with action owners; specification meets all `Datasheet.md`, `Specification.md`, and traceability requirements.

### Step 6: Interdisciplinary Check (IDC)

**Objective:** Coordinate interface requirements and resolve conflicts with other disciplines/packages.

**Actions:**
1. **Identify IDC participants (per `Specification.md § 3`):**
   - **PKG-08 Marine Structures (mandatory):** Fender reaction forces, bollard loads, ladder attachment loads, structural capacity verification, corrosion protection coordination
   - **PKG-11 Marine Loading System (if applicable):** Operational clearances, safety zones, access requirements
   - **PKG-10 Railcar Unloading System (if applicable):** Access clearances, safety zones
   - **PKG-26 Protective Coatings (if applicable):** Coating system coordination
   - **Other disciplines as applicable:** Electrical (grounding, lighting), instrumentation, operations (operational requirements, access preferences)
2. **Define IDC scope and focus areas:**
   - Prepare IDC transmittal with clear scope statement (e.g., "Please review interface requirements in § 1.5 and § 3; confirm structural capacity for fender/bollard loads in § 2.1, 2.2; coordinate corrosion protection requirements in § 1.4").
   - Highlight specific requirements affecting other packages (load assumptions, interface details, corrosion protection).
3. **Circulate specification for IDC:**
   - Distribute draft specification to IDC participants with transmittal.
   - Request comments by specific date (coordinate with project schedule).
   - Provide comment response template if required by project procedures.
4. **Receive and log IDC comments:**
   - Collect comments from all IDC participants.
   - Log comments in comment resolution log (comment ID, commenter, section, comment text, proposed resolution).
5. **Review comments with IDC participants and resolve:**
   - **Accept:** Incorporate comment into specification; document acceptance in comment resolution log.
   - **Reject:** Provide justification for rejection; negotiate alternative solution if needed; document rejection and justification in comment resolution log.
   - **Negotiate:** Discuss with commenter to find mutually acceptable solution; document agreed resolution in comment resolution log.
   - For unresolved conflicts: escalate to Project Manager / Technical Lead for ruling.
6. **Update specification to incorporate IDC comment resolutions:**
   - Revise specification based on accepted comments and negotiated resolutions.
   - Track revisions (revision marks, change log) per project document control procedures.
7. **Document IDC completion and obtain sign-off:**
   - Prepare IDC record documenting IDC participants, comments received, comment resolutions.
   - Obtain IDC sign-off from participating disciplines (confirmation that interface requirements are coordinated and accepted).
   - **TBD:** IDC workflow and sign-off requirements per project procedures.

**Inputs:** Draft specification (Step 5 output), `Specification.md § 3`, IDC participant list.
**Outputs:** IDC record; comment resolution log; updated specification incorporating IDC resolutions; IDC sign-off from participating disciplines.
**Verification:** All IDC comments resolved and documented; interfaces coordinated; no unresolved conflicts (or escalated to PM/Technical Lead for ruling); IDC sign-off obtained.

### Step 7: Independent Check

**Objective:** Verify technical accuracy, code compliance, ER compliance, and verifiability by independent checker.

**Actions:**
1. **Assign independent checker:**
   - Select checker qualified in Marine discipline or specification experience; independent of originator per project quality procedures.
   - Provide checker with authority and resources to perform independent check.
2. **Provide checker with specification and supporting materials:**
   - Draft specification (IDC-resolved version from Step 6)
   - `Datasheet.md` (content checklist)
   - `Specification.md` (meta-requirements)
   - `Guidance.md` (design rationale and principles)
   - Requirements extraction log (source traceability)
   - ER requirements and applicable codes/standards
   - Design inputs (DEL-08.06, DEL-08.07, DEL-08.08, DEL-08.09, PKG-08 outputs)
   - Related deliverables (DEL-09.01, DEL-09.03, DEL-09.04, DEL-09.05 for cross-reference)
3. **Checker performs independent check per `Specification.md § Verification` check criteria:**
   - **Technical accuracy:** Requirements are technically sound; performance criteria are appropriate; material selections are suitable for marine environment; test requirements are adequate.
   - **ER compliance:** All ER requirements addressed; no deviations without justification; ER clauses correctly cited and interpreted.
   - **Code compliance:** All applicable codes/standards identified and requirements correctly applied; ladder safety features comply with safety codes; fender/bollard requirements comply with marine/port codes; life-saving equipment complies with regulatory requirements.
   - **Completeness:** All `Datasheet.md` Content Checklist items and `Specification.md § 1–2` requirements addressed; no scope gaps.
   - **Verifiability:** Requirements written in verifiable terms with measurable criteria; test methods and acceptance criteria specified; vague language eliminated or clarified.
   - **Traceability:** Each non-trivial requirement cites source or marked TBD/ASSUMPTION with justification; requirements extraction log supports citations.
   - **Consistency:** Cross-document consistency with `Guidance.md`, `Datasheet.md`, `Procedure.md`; internal consistency (terminology, values, references).
4. **Receive and log checker comments:**
   - Collect comments from checker.
   - Log comments in comment resolution log (similar format to IDC comments).
5. **Review comments with checker and resolve:**
   - **Accept:** Incorporate comment into specification; document acceptance.
   - **Reject:** Provide justification for rejection; negotiate alternative solution if needed; document rejection and justification.
   - **Negotiate:** Discuss with checker to find mutually acceptable solution; document agreed resolution.
   - For disagreements: escalate to Project Manager / Technical Lead for ruling.
6. **Update specification to incorporate checker comment resolutions:**
   - Revise specification based on accepted comments and negotiated resolutions.
   - Track revisions per project document control procedures.
7. **Obtain checker sign-off:**
   - Checker confirms that specification meets requirements and is ready for issue (acceptance that requirements are technically accurate, ER/code compliant, complete, verifiable, and traceable).
   - Checker sign-off recorded per project quality procedures.
   - **TBD:** Checker acceptance criteria and sign-off requirements per project quality procedures.

**Inputs:** Draft specification (Step 6 output), all supporting materials and references, `Datasheet.md`, `Specification.md`, `Guidance.md`, requirements extraction log.
**Outputs:** Checker comments; comment resolution log; updated specification incorporating checker resolutions; checker sign-off.
**Verification:** Checker sign-off obtained; all checker comments resolved and documented; specification meets all technical accuracy, ER/code compliance, completeness, verifiability, and traceability requirements.

### Step 8: Issue Preparation

**Objective:** Prepare specification for issue (review/approval or construction).

**Actions:**
1. **Apply final document control:**
   - Assign document number per project numbering system (if not already assigned).
   - Apply revision designation per project revision scheme (e.g., Rev 0 for first issue, Rev A/B/C for subsequent revisions).
   - Update document header/footer with document number, revision, date, project information.
   - Remove revision marks and draft watermarks (if applicable).
2. **Prepare issue package:**
   - **Format:** PDF for review/approval; editable format for internal development (per `Specification.md § Documentation`).
   - **Transmittal:** Prepare transmittal cover sheet listing document number, title, revision, purpose of issue (e.g., "For Review," "For Approval," "For Construction").
3. **Prepare issue records:**
   - Requirements extraction log (Step 2) — demonstrating source traceability
   - Self-check record (Step 5)
   - IDC record and comment resolution log (Step 6)
   - Checker sign-off and comment resolution log (Step 7)
   - (Optional) Compliance matrix if required by ER or project procedures — demonstrating ER clause compliance
4. **Update `_STATUS.md` when ready for CHECKING or ISSUED state:**
   - **CHECKING:** Specification issued for review/approval (placed in `2_Checking/To/`)
   - **ISSUED:** Specification approved and issued for construction (placed in `3_Issued/`)
   - Update status with date, revision, and brief description of issue.
5. **Archive previous revisions (if applicable):**
   - Archive superseded revisions per project records management procedures.
   - Retain records for audit trail and configuration management.

**Inputs:** Specification (Step 7 output), all check/sign-off records, project document control procedures.
**Outputs:** Issue-ready specification package; transmittal; supporting records (requirements extraction log, self-check, IDC, checker sign-off); updated `_STATUS.md`.
**Verification:** Specification package is complete and complies with project document control requirements; all check/sign-off records are complete and attached/referenced; `_STATUS.md` updated correctly with appropriate state and revision information.
**TBD:** Project document control procedures and issue protocols.

## Verification

**Summary of verification activities performed throughout this procedure:**

| Activity | Step | Criteria | Sign-off |
|----------|------|----------|----------|
| Scope confirmation | Step 1 | Specification scope addresses all `Datasheet.md` Content Checklist items and decomposition artifacts; scope boundaries documented | Originator |
| Requirements extraction | Step 2 | All required sources reviewed (ER, codes, design inputs); requirements logged with source traceability; missing inputs identified with action owners | Originator / Package Lead |
| Specification drafting | Step 3 | All sections drafted per `Specification.md § 1–2`; requirements written in verifiable terms; all non-trivial requirements cite sources | Originator |
| Quality/testing requirements | Step 4 | Inspection/testing requirements complete; hold/witness points identified; submittal requirements defined; cross-reference to DEL-09.03, DEL-09.04, DEL-09.05 | Originator |
| Self-check | Step 5 | Completeness, consistency, traceability, verifiability per `Specification.md § 4` | Originator |
| Interdisciplinary check (IDC) | Step 6 | Interface coordination with PKG-08, PKG-11, PKG-26; no unresolved conflicts | IDC participants |
| Independent check | Step 7 | Technical accuracy, ER/code compliance, completeness, verifiability, traceability | Checker |
| Issue readiness | Step 8 | Specification package complete; complies with document control requirements | Approver |

**Sign-off requirements (per project quality procedures):**

| Role | Signature | Purpose |
|------|-----------|---------|
| Originator | Required | Confirms self-check completed; specification meets requirements |
| IDC participants | Required | Confirms interfaces coordinated; no unresolved conflicts with interfacing packages |
| Checker | Required | Confirms independent check completed; specification is technically accurate, ER/code compliant, complete, verifiable, and traceable |
| Approver | Required | Authorizes issue for intended purpose (review/approval/construction) |

**ASSUMPTION:** Sign-off protocol and authority matrix per project quality procedures.

## Records

**Documentation outputs (per `Specification.md § Documentation` and `Datasheet.md`):**
- Fender specification
- Bollard specification
- Marine hardware specification
- (May be combined into a single technical specification document or separate documents, depending on project document control preferences)

**Record management:**

| Record | Location | Retention | Purpose |
|--------|----------|-----------|---------|
| Draft specification (in progress) | `1_Working/` | Per project procedures | Working files during development |
| Review package | `2_Checking/To/` | Per project procedures | Issue for review/approval |
| Issued specification | `3_Issued/` | Per project procedures | Final issue for construction; project record |
| Requirements extraction log | Deliverable folder or project QA system | Per project procedures | Source traceability; demonstrates ER compliance |
| Self-check record | Deliverable folder or project QA system | Per project procedures | Evidence of self-check completion |
| IDC record and comment resolution log | Deliverable folder or project QA system | Per project procedures | Evidence of interface coordination |
| Checker sign-off and comment resolution log | Deliverable folder or project QA system | Per project procedures | Evidence of independent check |
| Input register / status log | Deliverable folder | Per project procedures | Tracking of design inputs and status |
| Compliance matrix (if required) | Deliverable folder or project QA system | Per project procedures | Demonstrates ER clause-by-clause compliance |

**ASSUMPTION:** Electronic records managed in project document management system with appropriate access controls, backup/retention protocols, and audit trail.

**Cross-reference:** See `Datasheet.md § References` for related documents.
