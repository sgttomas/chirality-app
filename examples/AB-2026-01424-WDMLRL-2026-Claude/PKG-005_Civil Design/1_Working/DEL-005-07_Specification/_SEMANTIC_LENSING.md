# Semantic Lensing Register: DEL-005-07 Civil Specification

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-005_Civil Design/1_Working/DEL-005-07_Specification/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-005-07_Specification/_CONTEXT.md
- _STATUS.md — DEL-005-07_Specification/_STATUS.md (state: SEMANTIC_READY)
- _SEMANTIC.md — DEL-005-07_Specification/_SEMANTIC.md
- Datasheet.md — DEL-005-07_Specification/Datasheet.md
- Specification.md — DEL-005-07_Specification/Specification.md
- Guidance.md — DEL-005-07_Specification/Guidance.md
- Procedure.md — DEL-005-07_Specification/Procedure.md
- _REFERENCES.md — DEL-005-07_Specification/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 3
  - Specification: 13
  - Guidance: 4
  - Procedure: 5
  - Multi: 3
- By matrix:
  - A: 5  B: 4  C: 3  F: 4  D: 3  X: 5  E: 4
- By type:
  - Conflict: 1
  - VerificationGap: 7
  - MissingSlot: 5
  - WeakStatement: 5
  - RationaleGap: 3
  - Normalization: 2
  - TBD_Question: 5
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Drainage design storm return period lacks prescriptive direction |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | County aggregate testing responsibility unresolved |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Code compliance verification approach is generic |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit mechanisms adequately addressed across documents |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Missing procedural direction for erosion/sediment control during construction |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Practical execution steps are well structured in Procedure |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Performance assessment covered by Verification tables |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Process audit covered by Step 8 internal quality review |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | Warranty and guarantee period obligations lack value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Merit application adequately covered in trade-off analysis |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Worth determination addressed through verification approach |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality appraisal covered by QC/testing requirements in Documentation table |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify REQ-CIVIL-003 by recording the applicable Alberta stormwater standard that will determine return period, or explicitly record this as a TBD requiring Civil Engineer input | REQ-CIVIL-003 states the design storm return period "shall be determined by the Civil Engineer" but does not identify which Alberta standard or municipal guidance applies; this is a materially ambiguous prescriptive direction that could produce different designs depending on interpretation | Specification.md | REQ-CIVIL-003 -- Future Storm Event Accommodation | -- | Civil Engineer | TBD |
| A-002 | A:normative:applying | Conflict | Multi | Specification | Resolve whether Proponent or County is responsible for testing County-supplied aggregate to confirm specification compliance; record ruling in Specification and Procedure | Datasheet states aggregate supply is County responsibility (SOW-0203), but the civil specification must set quality requirements. Who tests incoming material is unresolved -- this is already flagged as CF-CIVIL-02 in Guidance but remains TBD | Guidance.md; Datasheet.md | Guidance.md#Conflict Table CF-CIVIL-02; Datasheet.md#Attributes (Aggregate Supply) | Guidance.md#CF-CIVIL-02 (Decomposition SOW-0203 vs RFP/CCDC 14-2013) | Civil Engineer / County PM | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add specific acceptance criteria for REQ-CIVIL-011 (Code Compliance) beyond referencing DEL-009-04; identify which code sections apply to civil scope | REQ-CIVIL-011 verification references a code compliance register (DEL-009-04) and inspection reports but does not identify specific code clauses against which compliance will be judged; compliance determination requires traceable clause-level criteria | Specification.md | REQ-CIVIL-011 -- Code Compliance; Verification table row for REQ-CIVIL-011 | -- | Civil Engineer | TBD |
| A-004 | A:operative:guiding | MissingSlot | Specification | Specification | Add requirement for erosion and sediment control (ESC) plan during civil construction, or clarify if this is addressed in another deliverable | Guidance mentions dust control and erosion/sediment control as site context considerations, but no corresponding requirement exists in Specification.md and no procedural step addresses ESC plan preparation. This is a gap in operative procedural direction for construction-phase controls | Specification.md; Guidance.md | Guidance.md#Site Context -- Active Landfill; Specification.md#Requirements (entire section scanned) | -- | Civil Engineer | TBD |
| A-005 | A:evaluative:guiding | MissingSlot | Specification | Guidance | Add guidance on warranty and guarantee period obligations for civil works under CCDC 14-2013, particularly for driving surface durability and drainage performance | Guidance references the 2-year guarantee period (Purpose section) but neither Specification nor Guidance defines what constitutes acceptable performance during the guarantee period for civil elements (e.g., driving surface rutting tolerance, drainage function maintenance). This value orientation gap could affect dispute resolution | Specification.md; Guidance.md | Guidance.md#Purpose; Specification.md#Requirements (entire section scanned) | -- | Civil Engineer | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Motor scraper design parameters not recorded as essential facts |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet provides adequate evidence with source tracing |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Frost depth data absent pending geotech |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurements consistently referenced from RFP and appendices |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Missing signal on County pre-work completion status |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequately provided across documents |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Comprehensive account of scope and interfaces provided |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messages are coherent across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding of civil design requirements established |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise requirements (P.Eng.) clearly stated |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Thorough treatment of civil design domain |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Consistent understanding across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 1 | HAS_ITEMS | Missing discernment on sequencing risk if geotech is late |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-off analysis demonstrates adequate judgment |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view of project context provided |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and traceable throughout |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: specific motor scraper model or class (axle load, gross vehicle weight, turning radius) that defines the design vehicle for driving surface design | REQ-CIVIL-004 and REQ-CIVIL-005 reference "motor scraper-class" equipment but no specific axle load, weight, or turning radius values are recorded. These are essential facts needed before design can proceed | Datasheet.md; Specification.md | Datasheet.md#Attributes (Driving Surface Load Requirement); Specification.md#REQ-CIVIL-004, REQ-CIVIL-005 | -- | Civil Engineer / County Operations | TBD |
| B-002 | B:data:completeness | TBD_Question | Datasheet | Datasheet | Record TBD: anticipated frost penetration depth for site location and applicable frost protection design standard | Frost depth is a critical design input for subgrade preparation. Guidance identifies this as critical but no data value or reference standard is recorded in Datasheet. Geotechnical report (DEL-008-01) will provide this, but the expected range or design standard should be identified | Datasheet.md; Guidance.md | Datasheet.md#Conditions (Geotechnical Data); Guidance.md#Frost and Subgrade Conditions | -- | Geotechnical Engineer | TBD |
| B-003 | B:information:necessity | TBD_Question | Multi | Procedure | Record TBD: confirm with County whether topsoil stripping has been completed before construction mobilization; define how this confirmation will be obtained | CF-CIVIL-01 in Guidance identifies this conditional but no mechanism exists in Procedure for obtaining the essential signal of whether County pre-work is complete. Step 1.4 references the conflict but does not specify a verification method | Guidance.md; Procedure.md | Guidance.md#CF-CIVIL-01; Procedure.md#Step 1 item 4 | -- | County PM / Civil Engineer | TBD |
| B-004 | B:wisdom:necessity | RationaleGap | Procedure | Guidance | Add guidance on schedule risk and contingency approach if geotechnical report (DEL-008-01) delivery is delayed relative to civil design timeline | Procedure Step 2 depends on receiving the geotech report but provides no discernment on what happens if it is delayed. Given that the specification cannot be completed without geotech values, the schedule dependency risk needs explicit guidance | Procedure.md; Guidance.md | Procedure.md#Step 2; Guidance.md#Geotechnical-Informed Design | -- | Project Manager | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Regulatory Compliance Threshold | 1 | HAS_ITEMS | Specific regulatory thresholds for stormwater not established |
| C:normative:sufficiency | normative | sufficiency | Competent Governance Standard | 0 | NO_ITEMS | Governance standards adequately framed via P.Eng. and code references |
| C:normative:completeness | normative | completeness | Total Compliance Coverage | 1 | HAS_ITEMS | Environmental compliance coverage incomplete |
| C:normative:consistency | normative | consistency | Harmonized Enforcement Regime | 0 | NO_ITEMS | Enforcement regime consistently referenced (CCDC, codes, P.Eng.) |
| C:operative:necessity | operative | necessity | Core Operational Capability | 0 | NO_ITEMS | Core operational capabilities defined through procedure steps |
| C:operative:sufficiency | operative | sufficiency | Verified Competent Practice | 0 | NO_ITEMS | Competent practice verified through QC and testing requirements |
| C:operative:completeness | operative | completeness | Comprehensive Process Mastery | 0 | NO_ITEMS | Process coverage is comprehensive across 10 procedure steps |
| C:operative:consistency | operative | consistency | Uniform Systematic Execution | 0 | NO_ITEMS | Systematic execution approach consistent throughout |
| C:evaluative:necessity | evaluative | necessity | Inherent Merit Recognition | 1 | HAS_ITEMS | Compaction testing acceptance criteria not specified |
| C:evaluative:sufficiency | evaluative | sufficiency | Defensible Value Assessment | 0 | NO_ITEMS | Value assessment defensible through trade-off analysis |
| C:evaluative:completeness | evaluative | completeness | Holistic Quality Appraisal | 0 | NO_ITEMS | Quality appraisal mechanisms in place |
| C:evaluative:consistency | evaluative | consistency | Principled Value Consistency | 0 | NO_ITEMS | Value principles consistently applied |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Strengthen REQ-CIVIL-003 by identifying the specific Alberta regulatory threshold or municipal standard that establishes the minimum design storm return period for this site classification | The "Regulatory Compliance Threshold" lens reveals that REQ-CIVIL-003 defers the design storm return period entirely to the Civil Engineer without identifying a regulatory floor. For a landfill site, Alberta Environment and Protected Areas may impose specific stormwater management requirements that establish a binding threshold | Specification.md | REQ-CIVIL-003 -- Future Storm Event Accommodation | -- | Civil Engineer / Alberta Environment | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add requirement addressing Alberta environmental regulatory compliance for construction at an active landfill site (e.g., EPEA approval conditions, landfill operating approval conditions affecting civil works) | Under "Total Compliance Coverage," the specification addresses Alberta Building Code and Safety Codes but does not address environmental regulatory requirements that may apply to civil works at an active landfill (e.g., runoff quality, sediment discharge). This is a completeness gap in normative coverage | Specification.md | Specification.md#Standards table; Specification.md#Requirements (entire section scanned) | -- | Civil Engineer / Environmental | TBD |
| C-003 | C:evaluative:necessity | VerificationGap | Specification | Specification | Add specific compaction acceptance criteria (e.g., minimum percent Standard Proctor density) as a verification threshold for subgrade and granular base, or explicitly mark as TBD pending geotech | Under "Inherent Merit Recognition," compaction testing is listed as a verification approach (REQ-CIVIL-004) but no acceptance value or standard is specified. Without a defined threshold, merit recognition (pass/fail determination) during construction is impossible | Specification.md | Specification.md#Verification table (REQ-CIVIL-004); Specification.md#Documentation (Quality control and testing) | -- | Geotechnical Engineer / Civil Engineer | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Obligatory Conformance Foundation | 1 | HAS_ITEMS | Foundation for pad structural requirements incomplete |
| F:normative:sufficiency | normative | sufficiency | Verified Regulatory Adequacy | 0 | NO_ITEMS | Regulatory adequacy framework sufficient for current state |
| F:normative:completeness | normative | completeness | Total Regulatory Command | 1 | HAS_ITEMS | Submittals requirements not specified |
| F:normative:consistency | normative | consistency | Coherent Regulatory Discipline | 0 | NO_ITEMS | Regulatory references consistent across documents |
| F:operative:necessity | operative | necessity | Essential Procedural Ground | 1 | HAS_ITEMS | Pre-construction survey step missing |
| F:operative:sufficiency | operative | sufficiency | Demonstrated Skilled Proficiency | 0 | NO_ITEMS | Skilled proficiency requirements established through P.Eng. stamp |
| F:operative:completeness | operative | completeness | Thorough Operational Authority | 0 | NO_ITEMS | Operational steps are thorough |
| F:operative:consistency | operative | consistency | Stable Methodical Practice | 0 | NO_ITEMS | Practice is methodical and stable across procedure |
| F:evaluative:necessity | evaluative | necessity | Foundational Quality Significance | 1 | HAS_ITEMS | Material gradation acceptance criteria absent |
| F:evaluative:sufficiency | evaluative | sufficiency | Substantiated Quality Judgment | 0 | NO_ITEMS | Quality judgments substantiated through verification table |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Evaluation Authority | 0 | NO_ITEMS | Evaluation authority established through P.Eng. review |
| F:evaluative:consistency | evaluative | consistency | Principled Quality Coherence | 0 | NO_ITEMS | Quality principles coherent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | WeakStatement | Specification | Specification | Strengthen REQ-CIVIL-008 to specify concrete mix design requirements (minimum compressive strength, air entrainment for freeze-thaw) or explicitly defer to structural engineer with cross-reference to PKG-002 | REQ-CIVIL-008 (Cement and Gravel Pads) references Appendix B for layout but does not establish obligatory conformance requirements for concrete material properties. For pads subjected to heavy equipment, mix design is a necessary conformance foundation | Specification.md | REQ-CIVIL-008 -- Cement and Gravel Pads | -- | Civil Engineer / Structural Engineer | TBD |
| F-002 | F:normative:completeness | MissingSlot | Specification | Specification | Add requirement for construction submittals (shop drawings, material certificates, mix designs) that the contractor must provide before civil work commences | The Documentation table lists submittals requirements as an anticipated artifact, but no corresponding requirement in Specification.md mandates submittals. Total regulatory command requires that the submittals obligation be normatively stated | Specification.md | Specification.md#Documentation table (General conditions and submittals requirements); Specification.md#Requirements (entire section scanned) | -- | Civil Engineer | TBD |
| F-003 | F:operative:necessity | MissingSlot | Procedure | Procedure | Add procedural step for pre-construction condition survey to document existing site grades and drainage conditions before civil works begin | The procedure assumes the site will be ready for civil works after County pre-works but does not include a step to formally survey and document existing conditions. This is essential procedural ground for verifying REQ-CIVIL-002 (no alteration of neighbouring drainage) | Procedure.md | Procedure.md#Steps (entire section scanned); Specification.md#REQ-CIVIL-002 | -- | Civil Engineer | TBD |
| F-004 | F:evaluative:necessity | VerificationGap | Specification | Specification | Add acceptance criteria for aggregate gradation (granular base and surface gravel) or record as TBD pending geotechnical and material source confirmation | Material gradation is foundational quality significance for driving surface performance. The Documentation table lists material gradation testing as a record, but Specification does not specify gradation bands or reference a standard (e.g., Alberta Transportation specifications). Without this, quality judgment during construction has no basis | Specification.md | Specification.md#Documentation table (Quality control and testing); Specification.md#Verification table (REQ-CIVIL-004) | -- | Civil Engineer / Geotechnical Engineer | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Binding Conformance Instruction | 1 | HAS_ITEMS | Handoff criteria for County bulk works undefined |
| D:normative:applying | normative | applying | Ratified Compulsory Enactment | 0 | NO_ITEMS | Compulsory enactment mechanisms in place (P.Eng., IFC issue) |
| D:normative:judging | normative | judging | Conclusive Conformance Ruling | 0 | NO_ITEMS | Conformance ruling approach adequate |
| D:normative:reviewing | normative | reviewing | Resolved Oversight Scrutiny | 0 | NO_ITEMS | Oversight scrutiny covered through County approval and P.Eng. review |
| D:operative:guiding | operative | guiding | Grounded Actionable Guidance | 1 | HAS_ITEMS | Missing guidance on construction sequencing constraints |
| D:operative:applying | operative | applying | Validated Skill Deployment | 0 | NO_ITEMS | Skill deployment validated through P.Eng. and procedure |
| D:operative:judging | operative | judging | Authoritative Performance Ruling | 0 | NO_ITEMS | Performance ruling authority established |
| D:operative:reviewing | operative | reviewing | Resolved Procedural Inspection | 0 | NO_ITEMS | Procedural inspection covered by Step 8 |
| D:evaluative:guiding | evaluative | guiding | Grounded Merit Guidance | 0 | NO_ITEMS | Merit guidance provided in trade-offs and principles |
| D:evaluative:applying | evaluative | applying | Validated Merit Enactment | 0 | NO_ITEMS | Merit enactment validated through design approach |
| D:evaluative:judging | evaluative | judging | Conclusive Quality Ruling | 1 | HAS_ITEMS | Inspection hold points not defined |
| D:evaluative:reviewing | evaluative | reviewing | Grounded Merit Scrutiny | 0 | NO_ITEMS | Merit scrutiny mechanisms adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:guiding | WeakStatement | Guidance | Specification | Define binding handoff criteria (finished subgrade elevation tolerance, compaction standard) that County bulk cut and fill must achieve before Proponent civil works can begin | Guidance identifies the need for handoff criteria (Coordination with County-Performed Bulk Works) but neither Specification nor Guidance defines measurable acceptance criteria for the County-to-Proponent handoff. Without binding conformance instruction, the transition point is ambiguous | Guidance.md; Specification.md | Guidance.md#Coordination with County-Performed Bulk Works; Specification.md#Excluded table | -- | Civil Engineer / County PM | TBD |
| D-002 | D:operative:guiding | RationaleGap | Guidance | Guidance | Add guidance on construction sequencing constraints imposed by active landfill operations (e.g., access restrictions, operating hours, haul route conflicts) | Guidance mentions "sequenced to minimize interference with landfill operations" but does not provide grounded actionable guidance on specific constraints. The Civil Engineer needs operational context from the County to develop a workable construction sequence | Guidance.md | Guidance.md#Site Context -- Active Landfill | -- | County Operations / Civil Engineer | TBD |
| D-003 | D:evaluative:judging | VerificationGap | Procedure | Specification | Define inspection hold points (e.g., subgrade approval before granular placement, compaction testing before surface placement) in Specification or Procedure | Procedure Step 6 references "inspection hold points" in Part 3: Execution of specification sections but these are not defined in either Specification or Procedure verification tables. Without defined hold points, conclusive quality ruling during construction cannot occur at the right time | Procedure.md; Specification.md | Procedure.md#Step 6 (Part 3: Execution); Specification.md#Verification table | -- | Civil Engineer | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Binding Operational Imperative | 0 | NO_ITEMS | Binding operational imperatives identified |
| X:guiding:sufficiency | guiding | sufficiency | Informed Compliance Counsel | 1 | HAS_ITEMS | Standards editions not specified |
| X:guiding:completeness | guiding | completeness | Total Conformance Scope | 0 | NO_ITEMS | Conformance scope adequately defined |
| X:guiding:consistency | guiding | consistency | Harmonized Conformance Standard | 1 | HAS_ITEMS | Terminology inconsistency for pad types |
| X:applying:necessity | applying | necessity | Obligatory Competence Basis | 0 | NO_ITEMS | Competence basis established |
| X:applying:sufficiency | applying | sufficiency | Proficient Compliance Deployment | 0 | NO_ITEMS | Compliance deployment approach adequate |
| X:applying:completeness | applying | completeness | Exhaustive Implementation Mastery | 1 | HAS_ITEMS | Missing implementation detail for mud sump scope split |
| X:applying:consistency | applying | consistency | Coherent Implementation Standard | 0 | NO_ITEMS | Implementation standards coherent |
| X:judging:necessity | judging | necessity | Binding Quality Determination | 1 | HAS_ITEMS | Surface tolerance criteria absent |
| X:judging:sufficiency | judging | sufficiency | Competent Compliance Proof | 0 | NO_ITEMS | Compliance proof mechanisms adequate |
| X:judging:completeness | judging | completeness | Exhaustive Compliance Authority | 0 | NO_ITEMS | Compliance authority established |
| X:judging:consistency | judging | consistency | Reliable Execution Standard | 0 | NO_ITEMS | Execution standards reliable |
| X:reviewing:necessity | reviewing | necessity | Verified Procedural Foundation | 1 | HAS_ITEMS | No record retention requirement specified |
| X:reviewing:sufficiency | reviewing | sufficiency | Sufficient Audit Evidence | 0 | NO_ITEMS | Audit evidence mechanisms adequate |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Audit Coverage | 0 | NO_ITEMS | Audit coverage addressed |
| X:reviewing:consistency | reviewing | consistency | Reliable Audit Discipline | 0 | NO_ITEMS | Audit discipline consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | WeakStatement | Specification | Specification | Specify editions/years of Alberta Building Code and Alberta Safety Codes applicable to this project, or record as TBD with instruction for Civil Engineer to confirm | The Standards table lists "Alberta Building Code (ABC) -- current edition" and "Alberta Safety Codes" without specifying editions. Informed compliance counsel requires identifying the specific edition in force at time of design to ensure a stable compliance baseline | Specification.md | Specification.md#Standards table | -- | Civil Engineer | TBD |
| X-002 | X:guiding:consistency | Normalization | Multi | Guidance | Harmonize terminology for pad types across documents: "cement pads" (Datasheet, Specification) vs "concrete pads" (Guidance) -- clarify whether these refer to the same elements | Datasheet and Specification use "cement pads" while Guidance uses "Cement Pad Specifications" heading but describes "concrete mix design requirements." The terms "cement" and "concrete" are technically different materials. Using both risks confusion during procurement and construction | Datasheet.md; Specification.md; Guidance.md | Datasheet.md#Construction (Cement Pads); Specification.md#REQ-CIVIL-008; Guidance.md#Cement Pad Specifications | -- | Civil Engineer | TBD |
| X-003 | X:applying:completeness | RationaleGap | Guidance | Guidance | Expand mud sump scope division rationale to include a definitive list of civil vs plumbing vs structural scope items with cross-references to PKG-002 and PKG-006 deliverables | The trade-off table recommends a scope split for the mud sump but the Guidance does not provide exhaustive implementation detail for the boundary. REQ-CIVIL-009 says "interface with PKG-002 and PKG-006" without specifying which physical elements are civil scope | Guidance.md; Specification.md | Guidance.md#Trade-offs (Mud sump scope division); Specification.md#REQ-CIVIL-009 | -- | Civil Engineer / Plumbing Engineer / Structural Engineer | TBD |
| X-004 | X:judging:necessity | VerificationGap | Specification | Specification | Add surface grade tolerance acceptance criteria (e.g., maximum deviation from design elevation) for finished driving surface and grading plan verification | REQ-CIVIL-001 (Positive Drainage) verification references slope calculations but does not define acceptable grade tolerance. A binding quality determination for grading requires a measurable tolerance standard | Specification.md | Specification.md#Verification table (REQ-CIVIL-001); Specification.md#REQ-CIVIL-001 | -- | Civil Engineer | TBD |
| X-005 | X:reviewing:necessity | VerificationGap | Procedure | Procedure | Add requirement for record retention period and format for civil construction records (material test reports, inspection reports, as-built documentation) | Procedure Records table lists records that shall result from the procedure but does not specify retention period, format, or handover requirements. Verified procedural foundation for future audits requires that record-keeping obligations be explicit | Procedure.md | Procedure.md#Records table | -- | Project Manager / Civil Engineer | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Specification Baseline | 1 | HAS_ITEMS | Baseline missing for County aggregate quality |
| E:guiding:information | guiding | information | Harmonized Regulatory Counsel | 0 | NO_ITEMS | Regulatory counsel harmonized across documents |
| E:guiding:knowledge | guiding | knowledge | Proficient Specification Mastery | 0 | NO_ITEMS | Specification mastery demonstrated in structure and coverage |
| E:guiding:wisdom | guiding | wisdom | Prudent Specification Foresight | 1 | HAS_ITEMS | Climate adaptation foresight absent |
| E:applying:data | applying | data | Verified Execution Evidence | 0 | NO_ITEMS | Execution evidence mechanisms in place |
| E:applying:information | applying | information | Coherent Implementation Report | 0 | NO_ITEMS | Implementation reporting adequate |
| E:applying:knowledge | applying | knowledge | Proficient Implementation Authority | 0 | NO_ITEMS | Implementation authority established |
| E:applying:wisdom | applying | wisdom | Prudent Implementation Wisdom | 0 | NO_ITEMS | Implementation wisdom reflected in procedure |
| E:judging:data | judging | data | Binding Quality Evidence | 1 | HAS_ITEMS | Testing frequency not specified |
| E:judging:information | judging | information | Informed Compliance Finding | 0 | NO_ITEMS | Compliance finding mechanisms adequate |
| E:judging:knowledge | judging | knowledge | Proficient Governance Command | 0 | NO_ITEMS | Governance command established |
| E:judging:wisdom | judging | wisdom | Principled Governance Foresight | 0 | NO_ITEMS | Governance foresight adequate |
| E:reviewing:data | reviewing | data | Verified Audit Record | 1 | HAS_ITEMS | As-built documentation requirement absent |
| E:reviewing:information | reviewing | information | Coherent Inspection Report | 0 | NO_ITEMS | Inspection reporting covered |
| E:reviewing:knowledge | reviewing | knowledge | Proficient Audit Authority | 0 | NO_ITEMS | Audit authority established |
| E:reviewing:wisdom | reviewing | wisdom | Principled Audit Foresight | 0 | NO_ITEMS | Audit foresight adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | TBD_Question | Datasheet | Datasheet | Record TBD: minimum aggregate quality requirements (gradation band, PI limits, LA abrasion, freeze-thaw durability) that County-supplied aggregate must meet for use as driving surface material | The authoritative specification baseline for aggregate quality is absent. Datasheet records that aggregate is County-supplied but does not establish the quality baseline the County must meet. Without this, the specification cannot set an authoritative material standard | Datasheet.md; Specification.md | Datasheet.md#Attributes (Aggregate Supply); Specification.md#REQ-CIVIL-004 | -- | Civil Engineer | TBD |
| E-002 | E:guiding:wisdom | TBD_Question | Guidance | Guidance | Record TBD: confirm whether climate change adaptation factors should be applied to design storm calculations for this site, given active landfill context and long design life | Prudent specification foresight for drainage design at a landfill site should consider whether current design storm standards adequately account for increasing storm intensity. This is not addressed in any document and represents a foresight gap that could affect long-term drainage adequacy | Specification.md; Guidance.md | Specification.md#REQ-CIVIL-003; Guidance.md#Trade-offs (Drainage design storm frequency) | -- | Civil Engineer / County PM | TBD |
| E-003 | E:judging:data | VerificationGap | Specification | Specification | Add testing frequency requirements for compaction and material gradation testing during construction (e.g., minimum tests per volume of fill or per area of driving surface) | Binding quality evidence requires not just what to test but how often. The Verification table and Documentation table reference compaction and gradation testing but do not specify minimum testing frequencies. Without frequency requirements, testing adequacy during construction cannot be verified | Specification.md | Specification.md#Verification table (REQ-CIVIL-004); Specification.md#Documentation table | -- | Civil Engineer | TBD |
| E-004 | E:reviewing:data | Normalization | Procedure | Procedure | Add requirement for civil as-built drawings and specification deviations to be documented and retained as verified audit records | Procedure Records table lists IFC drawings and specification as permanent records but does not address as-built documentation (recording deviations between IFC and actual construction). For a verified audit record, as-built civil drawings should be explicitly required | Procedure.md | Procedure.md#Records table | -- | Civil Engineer / Project Manager | TBD |
