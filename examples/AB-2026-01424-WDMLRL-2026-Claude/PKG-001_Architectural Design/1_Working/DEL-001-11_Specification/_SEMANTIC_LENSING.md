# Semantic Lensing Register: DEL-001-11 Architectural Specification

**Generated:** 2026-02-26
**Deliverable Folder:** PKG-001_Architectural Design/1_Working/DEL-001-11_Specification/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-001-11_Specification/_CONTEXT.md (Identity: Architectural Specification, PKG-001, Discipline: Architect)
- _STATUS.md — DEL-001-11_Specification/_STATUS.md (Current State: SEMANTIC_READY, Last Updated: 2026-02-26)
- _SEMANTIC.md — DEL-001-11_Specification/_SEMANTIC.md (Matrices A, B, C, F, D, X, E parsed)
- Datasheet.md — DEL-001-11_Specification/Datasheet.md (Identification, Attributes, Conditions, Construction, References)
- Specification.md — DEL-001-11_Specification/Specification.md (Scope, Requirements, Standards, Verification, Documentation)
- Guidance.md — DEL-001-11_Specification/Guidance.md (Purpose, Principles, Considerations, Trade-offs, Conflict Table)
- Procedure.md — DEL-001-11_Specification/Procedure.md (Prerequisites, Steps 1-7, Verification, Records)
- _REFERENCES.md — DEL-001-11_Specification/_REFERENCES.md (R-01 RFP, R-04 Appendix B)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 2
  - Specification: 14
  - Guidance: 4
  - Procedure: 5
  - Multi: 3
- By matrix:
  - A: 5  B: 4  C: 3  F: 4  D: 3  X: 5  E: 4
- By type:
  - Conflict: 1
  - VerificationGap: 7
  - MissingSlot: 7
  - WeakStatement: 5
  - RationaleGap: 3
  - Normalization: 2
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Standards edition gap |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Steel plate spec TBD |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Occupancy classification missing |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | Permit inspection process gap |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Steps 1-7 adequately covered |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Procedure execution steps present |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification tables present in Spec and Procedure |
| A:operative:reviewing | operative | reviewing | process audit | 1 | HAS_ITEMS | Inter-discipline sign-off records gap |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Principles P-1 through P-5 address value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs T-1 through T-3 address merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Adequately covered by Guidance trade-off analysis |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | QA checks present in Procedure Verification table |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Identify specific Alberta Building Code edition and part references applicable to this project; replace "current edition" and "ASSUMPTION: applicable" with confirmed code citations | The Standards table lists ABC as "current edition" with "ASSUMPTION: applicable" and "location TBD" for specific clauses. This prescriptive direction lens reveals that the governing normative source is unresolved -- implementation decisions depend on which edition and parts apply. | Specification.md | Standards table (lines 95-99) | -- | PROPOSAL: Architect to confirm ABC edition and Safety Codes Act clause refs | TBD |
| A-002 | A:normative:applying | TBD_Question | Specification | Specification | Record TBD: Steel plate material grade, thickness, and surface finish per ARCH-014. Confirm whether Architect or Structural Engineer is authority for specifying. | ARCH-014 explicitly flags steel plate specification as TBD. Under the mandatory practice lens, this is a missing binding requirement that blocks specification of a required building element. | Specification.md | Requirements > Structural Form and Envelope > ARCH-014 | -- | PROPOSAL: Joint authority -- Architect and Structural Engineer per RFP SS3.4 | TBD |
| A-003 | A:normative:judging | MissingSlot | Specification | Specification | Add occupancy classification determination for the maintenance shop under Alberta Building Code. This drives fire separation, egress, plumbing fixture counts, and accessibility requirements. | The compliance determination lens reveals no occupancy classification is stated anywhere in the four documents. Code compliance review (Procedure Step 6) references it but the classification itself is absent from Specification. | Specification.md, Procedure.md | Specification.md#Standards; Procedure.md#Step 6: Code Review (6.2) | -- | PROPOSAL: Architect to determine per ABC | TBD |
| A-004 | A:normative:reviewing | VerificationGap | Procedure | Procedure | Add explicit procedure step or checklist item for building permit application and inspection scheduling with Camrose County permit authority. | The regulatory audit lens reveals that while Procedure Step 7 mentions P.Eng. stamping and inspection requests, there is no explicit step for building permit application or tracking of permit inspections -- the primary regulatory review mechanism for this project. | Procedure.md | Steps > Step 7: Final Review and Issuance | -- | PROPOSAL: Architect / Design-Builder | TBD |
| A-005 | A:operative:reviewing | MissingSlot | Procedure | Procedure | Add a record type for inter-discipline coordination review sign-off that captures discipline, reviewer name, date, and disposition for each coordinating discipline. | The process audit lens reveals that the Records table lists "Inter-Discipline Coordination Review Sign-Off" as a record but does not define its content or format. The Verification table references "Inter-discipline review sign-off" but provides no template or minimum content. | Procedure.md | Records table; Verification table | -- | PROPOSAL: Architect / Project Manager | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Overhead door height missing |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Utility room and office areas TBD |
| B:data:completeness | data | completeness | comprehensive record | 0 | NO_ITEMS | Datasheet attribute tables are comprehensive for known data |
| B:data:consistency | data | consistency | reliable measurement | 1 | HAS_ITEMS | Floor area "approximately" qualifier |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | SOW coverage signals clear |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequately captured across docs |
| B:information:completeness | information | completeness | comprehensive account | 1 | HAS_ITEMS | Insulation/envelope scope missing |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messages consistent across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Design-build context well understood in Guidance |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Discipline coordination approach adequate |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Domain coverage adequate for current stage |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding consistent across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Guidance principles demonstrate adequate discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-off analysis present |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view present in Guidance |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Multi | Datasheet | Record TBD: Overhead door heights for wash bay and repair bays. Confirm motor scraper equipment profile dimensions with County. | Essential fact lens: The wash bay and repair bay overhead door heights are not stated in any document. Guidance C-2 flags this but no numeric value or TBD placeholder appears in Datasheet Attributes or Specification Requirements. This is an essential design datum. | Datasheet.md, Specification.md, Guidance.md | Datasheet.md#Attributes; Specification.md#ARCH-012, ARCH-013; Guidance.md#C-2 | -- | PROPOSAL: County to confirm equipment dimensions; Architect to specify | TBD |
| B-002 | B:data:sufficiency | WeakStatement | Datasheet | Datasheet | Clarify TBD areas for Utility Room and Office Space with minimum area targets or state explicitly that these are Design-Builder discretion. | Adequate evidence lens: Datasheet lists Utility Room and Office Space as "Present (area TBD -- not stated in sources)." The Specification (ARCH-021, ARCH-022) repeats this. Without minimum area guidance, the Design-Builder has no adequacy threshold. | Datasheet.md, Specification.md | Datasheet.md#Attributes > New North Shop Addition; Specification.md#ARCH-021, ARCH-022 | -- | PROPOSAL: County to provide minimum area or confirm DB discretion | TBD |
| B-003 | B:data:consistency | WeakStatement | Specification | Specification | Clarify the tolerance or interpretation of "approximately" for the 13,000 sq ft useable area in ARCH-001. State whether this is a minimum, a target, or a tolerance band. | Reliable measurement lens: ARCH-001 states "approximately 13,000 sq ft." The verification method is "Drawing area schedule review" but the acceptance criterion for "approximately" is undefined. This ambiguity could change design decisions. | Specification.md | Requirements > General > ARCH-001 | -- | PROPOSAL: Owner/Architect to define tolerance | TBD |
| B-004 | B:information:completeness | MissingSlot | Specification | Specification | Add specification requirements for building envelope -- insulation, vapour barrier, and weather barrier systems appropriate for Alberta climate and concrete construction. | Comprehensive account lens: Guidance T-1 explicitly notes insulation and vapour barrier must be appropriate for concrete construction in Alberta climate, but no corresponding requirement exists in Specification. Procedure Step 4 lists Division 07 (Thermal and Moisture Protection) as a specification division but with "specific systems TBD." | Specification.md, Guidance.md, Procedure.md | Specification.md#Requirements (absent); Guidance.md#T-1; Procedure.md#Step 4 (4.2, Division 07) | -- | PROPOSAL: Architect to specify per ABC and climate requirements | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Obligatory Compliance Threshold | 1 | HAS_ITEMS | ABC edition unconfirmed |
| C:normative:sufficiency | normative | sufficiency | Prescribed Certification Basis | 1 | HAS_ITEMS | AAAL registration unresolved |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Coverage | 0 | NO_ITEMS | Coverage adequate for current drafting stage given TBDs are flagged |
| C:normative:consistency | normative | consistency | Codified Conformance Standard | 0 | NO_ITEMS | Standards table internally consistent |
| C:operative:necessity | operative | necessity | Operational Readiness Mandate | 1 | HAS_ITEMS | Existing conditions survey prerequisite |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Competency Proof | 0 | NO_ITEMS | Competency requirements adequately addressed |
| C:operative:completeness | operative | completeness | Full Capability Accounting | 0 | NO_ITEMS | Procedure prerequisites comprehensive |
| C:operative:consistency | operative | consistency | Repeatable Execution Fidelity | 0 | NO_ITEMS | Steps sequenced consistently |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Value Foundation | 0 | NO_ITEMS | Value drivers well articulated in Guidance P-1 |
| C:evaluative:sufficiency | evaluative | sufficiency | Warranted Valuation Basis | 0 | NO_ITEMS | Trade-off rationale adequate |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Merit Assessment | 0 | NO_ITEMS | Assessment coverage adequate |
| C:evaluative:consistency | evaluative | consistency | Principled Valuation Integrity | 0 | NO_ITEMS | Valuation principles consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | VerificationGap | Specification | Specification | Add verification method for confirming which ABC edition applies and documenting applicable code sections with clause-level traceability. | Obligatory Compliance Threshold lens: The threshold for compliance cannot be established until the specific code edition is confirmed. The Standards table has multiple "TBD" clause references. No verification step confirms the code edition selection itself. | Specification.md | Standards table; Verification table | -- | PROPOSAL: Architect to confirm and document | TBD |
| C-002 | C:normative:sufficiency | TBD_Question | Guidance | Guidance | Record TBD: Confirm whether AAAL (Alberta Association of Architects) registration is required and whether dual-stamp (P.Eng. + Architect) requirements apply for this project type and scale. | Prescribed Certification Basis lens: Guidance C-4 raises AAAL registration as an assumption but the question is unresolved. The certification basis for IFC documents may require both P.Eng. and AAAL stamps. This affects ARCH-005 and the entire IFC issuance process. | Guidance.md | Considerations > C-4: IFC Stamping Requirement | -- | PROPOSAL: Architect to confirm with AAAL and APEGA | TBD |
| C-003 | C:operative:necessity | VerificationGap | Procedure | Procedure | Add verification checkpoint confirming that the existing conditions survey (Step 2) has been completed and findings documented before proceeding to Step 4 (Draft Specification) for renovation scope. | Operational Readiness Mandate lens: Procedure Step 2 describes the existing conditions survey but there is no gate or verification check confirming completion before specification drafting begins in Step 4. Guidance P-3 explicitly warns that specifying renovation scope without existing conditions data risks producing inapplicable requirements. | Procedure.md, Guidance.md | Procedure.md#Step 2; Procedure.md#Verification table; Guidance.md#P-3 | -- | PROPOSAL: Architect / Project Manager | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Non-Negotiable Qualification Gate | 1 | HAS_ITEMS | Washroom fixture count gap |
| F:normative:sufficiency | normative | sufficiency | Certified Proof Threshold | 1 | HAS_ITEMS | Verification method weak for renovation |
| F:normative:completeness | normative | completeness | Total Certification Archive | 0 | NO_ITEMS | Documentation section adequate |
| F:normative:consistency | normative | consistency | Uniform Regulatory Alignment | 1 | HAS_ITEMS | Washroom/urinal scope conflict |
| F:operative:necessity | operative | necessity | Baseline Capability Requirement | 0 | NO_ITEMS | Prerequisites comprehensive |
| F:operative:sufficiency | operative | sufficiency | Proven Operational Sufficiency | 0 | NO_ITEMS | Adequately addressed |
| F:operative:completeness | operative | completeness | Total Proficiency Inventory | 0 | NO_ITEMS | Procedure coverage complete |
| F:operative:consistency | operative | consistency | Dependable Performance Norm | 0 | NO_ITEMS | Performance expectations consistent |
| F:evaluative:necessity | evaluative | necessity | Foundational Merit Anchor | 0 | NO_ITEMS | Value anchors established in Guidance |
| F:evaluative:sufficiency | evaluative | sufficiency | Substantiated Appraisal Claim | 1 | HAS_ITEMS | Guarantee period not traced to material specs |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Value Catalogue | 0 | NO_ITEMS | Value catalogue adequate |
| F:evaluative:consistency | evaluative | consistency | Stable Principled Benchmark | 0 | NO_ITEMS | Benchmarks stable |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | VerificationGap | Specification | Specification | Add minimum plumbing fixture counts for the new addition washroom (ARCH-023) based on ABC occupancy classification and occupant load. Cross-reference DEL-006-08. | Non-Negotiable Qualification Gate lens: ARCH-023 states washroom with "area and fixture count TBD." Fixture counts are code-driven non-negotiable requirements. Without occupancy classification (see A-003), this qualification gate cannot be passed. | Specification.md | Requirements > Interior Spaces > ARCH-023 | -- | PROPOSAL: Architect to determine per ABC based on occupancy classification | TBD |
| F-002 | F:normative:sufficiency | WeakStatement | Specification | Specification | Strengthen verification methods for renovation requirements ARCH-040 through ARCH-044. Each currently shows only "As-built survey; drawing review" but renovation scope specifics are all TBD. Add acceptance criteria that will apply once renovation scope is defined. | Certified Proof Threshold lens: The verification methods for renovation requirements are generic ("as-built survey; drawing review") but the requirements themselves are all "renovation scope specifics TBD." The proof threshold is undefined because neither the requirement nor its verification criteria are established. | Specification.md | Requirements > Old North Shop Renovation > ARCH-040 to ARCH-044; Verification table | -- | PROPOSAL: Architect after existing conditions survey | TBD |
| F-003 | F:normative:consistency | Conflict | Multi | Guidance | Confirm whether the urinal expansion (SOW-0074 / ARCH-044) applies to the Old North Shop existing washroom, the new addition washroom (ARCH-023), or both. Update Specification and Datasheet accordingly. | Uniform Regulatory Alignment lens: This repeats CONF-001 from Guidance.md Conflict Table. The RFP describes "a washroom" in the new addition (SS3.1) and urinal expansion in the Old North Shop renovation scope (SS3.4/SOW-0074). The normative alignment is unclear. | Specification.md, Guidance.md | Specification.md#ARCH-023, ARCH-044; Guidance.md#Conflict Table > CONF-001 | Specification.md#ARCH-023 vs. Specification.md#ARCH-044 per Guidance.md#CONF-001 | PROPOSAL: Urinal expansion applies to Old North Shop per SOW-0074 grouping; confirm with County | TBD |
| F-004 | F:evaluative:sufficiency | RationaleGap | Guidance | Guidance | Add rationale connecting the 2-year post-CCC guarantee period (Datasheet Conditions) to material and system specification choices. Explain how guarantee obligations should inform material selection and warranty requirements. | Substantiated Appraisal Claim lens: Guidance C-6 mentions the guarantee period but does not explain how it should inform specific material specification choices. The Specification contains no warranty alignment requirements. The appraisal claim that materials meet guarantee obligations has no substantiation mechanism. | Guidance.md, Specification.md | Guidance.md#C-6; Datasheet.md#Conditions (Guarantee Period); Specification.md#Requirements (absent) | -- | PROPOSAL: Architect to establish material warranty alignment criteria | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Authoritative Gatekeeping Mandate | 1 | HAS_ITEMS | Preliminary design approval gate |
| D:normative:applying | normative | applying | Enforced Verified Enactment | 0 | NO_ITEMS | Enforcement mechanisms adequate |
| D:normative:judging | normative | judging | Binding Conclusive Adjudication | 0 | NO_ITEMS | Adjudication paths defined via County approval |
| D:normative:reviewing | normative | reviewing | Obligatory Compliance Examination | 0 | NO_ITEMS | Code review step present |
| D:operative:guiding | operative | guiding | Established Process Stewardship | 0 | NO_ITEMS | Process stewardship defined in Procedure |
| D:operative:applying | operative | applying | Validated Direct Implementation | 1 | HAS_ITEMS | MasterFormat assumption |
| D:operative:judging | operative | judging | Conclusive Capability Verdict | 0 | NO_ITEMS | Capability assessment via verification tables |
| D:operative:reviewing | operative | reviewing | Confirmed Procedural Examination | 0 | NO_ITEMS | Procedure verification checks present |
| D:evaluative:guiding | evaluative | guiding | Grounded Priority Stewardship | 1 | HAS_ITEMS | OBJ-001/OBJ-003 traceability gap |
| D:evaluative:applying | evaluative | applying | Confirmed Value Realization | 0 | NO_ITEMS | Value realization tracked through IFC process |
| D:evaluative:judging | evaluative | judging | Authoritative Appraisal Ruling | 0 | NO_ITEMS | Appraisal addressed via County approval gates |
| D:evaluative:reviewing | evaluative | reviewing | Principled Merit Examination | 0 | NO_ITEMS | Merit examination via quality review |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:guiding | VerificationGap | Specification | Specification | Add verification method for ARCH-006 (preliminary design County approval) that specifies what constitutes "approval" -- written sign-off, meeting minutes, or other form. | Authoritative Gatekeeping Mandate lens: ARCH-006 requires County approval of preliminary design before finalizing, but the verification method ("County approval record") does not define what form approval takes or who has authority to grant it. The gatekeeping mandate is established but the gate mechanism is vague. | Specification.md | Requirements > General > ARCH-006; Verification table (ARCH-006 not explicitly listed) | -- | PROPOSAL: County project representative | TBD |
| D-002 | D:operative:applying | Normalization | Procedure | Multi | Confirm whether CSC MasterFormat is the required specification organizational standard or an assumption. If confirmed, state as a requirement in Specification.md Standards table; if not, remove assumption language. | Validated Direct Implementation lens: Procedure Step 4.1 states "Organize the specification using CSC MasterFormat or equivalent division structure" with "(ASSUMPTION: CSC MasterFormat is the standard for Alberta construction specifications)." The Specification Standards table lists it with "applicability TBD." Terminology is inconsistent between assumption and standard. | Procedure.md, Specification.md | Procedure.md#Step 4 (4.1); Specification.md#Standards table (CSC/MasterFormat) | -- | PROPOSAL: Confirm with County / industry practice | TBD |
| D-003 | D:evaluative:guiding | RationaleGap | Guidance | Guidance | Add explicit traceability from OBJ-001 and OBJ-003 to specific architectural requirements (ARCH-xxx IDs), explaining how each objective is satisfied by the specification. | Grounded Priority Stewardship lens: Guidance Purpose section references OBJ-001 and OBJ-003 and Specification Scope references the supported objectives in context, but there is no explicit traceability mapping from objectives to specific ARCH-xxx requirements. Priority stewardship requires demonstrating that the specification addresses both objectives comprehensively. | Guidance.md, Specification.md | Guidance.md#Purpose; Specification.md#Scope; Datasheet.md#Identification (Supports Objectives) | -- | PROPOSAL: Architect | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Commanding Governance Baseline | 0 | NO_ITEMS | Governance baseline established |
| X:guiding:sufficiency | guiding | sufficiency | Justified Steering Threshold | 1 | HAS_ITEMS | Site meeting attendance not tracked |
| X:guiding:completeness | guiding | completeness | Exhaustive Strategic Archive | 0 | NO_ITEMS | Archive strategy adequate |
| X:guiding:consistency | guiding | consistency | Aligned Directional Norm | 0 | NO_ITEMS | Directional alignment consistent |
| X:applying:necessity | applying | necessity | Verified Enactment Proof | 1 | HAS_ITEMS | No verification for ARCH-006/ARCH-007 |
| X:applying:sufficiency | applying | sufficiency | Demonstrated Action Evidence | 1 | HAS_ITEMS | Coordination evidence undefined |
| X:applying:completeness | applying | completeness | Exhaustive Implementation Archive | 0 | NO_ITEMS | Documentation requirements present |
| X:applying:consistency | applying | consistency | Consistent Deployment Measure | 0 | NO_ITEMS | Deployment measures consistent |
| X:judging:necessity | judging | necessity | Conclusive Threshold Ruling | 0 | NO_ITEMS | Threshold rulings defined |
| X:judging:sufficiency | judging | sufficiency | Sufficient Adjudication Basis | 0 | NO_ITEMS | Adjudication basis adequate |
| X:judging:completeness | judging | completeness | Exhaustive Adjudication Record | 1 | HAS_ITEMS | Missing verification for several ARCH reqs |
| X:judging:consistency | judging | consistency | Stable Adjudication Standard | 0 | NO_ITEMS | Standards stable |
| X:reviewing:necessity | reviewing | necessity | Critical Inspection Foundation | 0 | NO_ITEMS | Inspection foundations established |
| X:reviewing:sufficiency | reviewing | sufficiency | Sufficient Inspection Scope | 1 | HAS_ITEMS | Renovation inspection scope gap |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Inspection Record | 0 | NO_ITEMS | Records table present |
| X:reviewing:consistency | reviewing | consistency | Dependable Inspection Constancy | 0 | NO_ITEMS | Inspection approach consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | MissingSlot | Procedure | Procedure | Add record of mandatory site meeting attendance (March 3, 2026 per RFP SS3.2) as a prerequisite verification item. Procedure Step 1.5 references it but no verification or record is defined. | Justified Steering Threshold lens: The site meeting is a steering prerequisite (RFP SS3.2 mandatory attendance) but the Procedure only mentions it in passing (Step 1.5) without a verification check or record requirement. The threshold for having attended is not verifiable from current documents. | Procedure.md | Steps > Step 1 (1.5); Records table (absent) | -- | PROPOSAL: Project Manager | TBD |
| X-002 | X:applying:necessity | VerificationGap | Specification | Specification | Add explicit verification rows in the Verification table for ARCH-006 (County preliminary design approval) and ARCH-007 (inter-discipline coordination). Both are listed as requirements but absent from the Verification table. | Verified Enactment Proof lens: The Specification Verification table covers ARCH-001 through ARCH-005 and ARCH-010 through ARCH-044 but skips ARCH-006 and ARCH-007. These are General Architectural Requirements that require verification proof. | Specification.md | Requirements > General > ARCH-006, ARCH-007; Verification table | -- | PROPOSAL: Architect | TBD |
| X-003 | X:applying:sufficiency | WeakStatement | Specification | Specification | Define what constitutes adequate evidence of "inter-discipline coordination" for ARCH-007. Specify the coordination mechanism (meeting, written review, shared model) and minimum documentation. | Demonstrated Action Evidence lens: ARCH-007 requires coordination with all disciplines but the verification method is "Inter-discipline coordination review." No definition of what evidence demonstrates adequate coordination. | Specification.md | Requirements > General > ARCH-007; Verification table | -- | PROPOSAL: Architect / Project Manager | TBD |
| X-004 | X:judging:completeness | VerificationGap | Specification | Specification | Add verification rows for ARCH-012 (wash bay integration), ARCH-021 (utility room), ARCH-022 (office space), ARCH-024 (wash station), ARCH-025 (service pit), ARCH-032 (mezzanine stairs), ARCH-051 (mud sump), ARCH-052 (site grading coordination). These requirements have no corresponding Verification table entries. | Exhaustive Adjudication Record lens: The Verification table is not exhaustive -- several ARCH requirements lack corresponding verification entries. While grouped verification may be intended (e.g., "All renovation items"), individual requirements with specific acceptance criteria need traceable verification records. | Specification.md | Requirements tables (ARCH-012, 021, 022, 024, 025, 032, 051, 052); Verification table | -- | PROPOSAL: Architect | TBD |
| X-005 | X:reviewing:sufficiency | MissingSlot | Specification | Specification | Add inspection criteria or acceptance standards for renovation scope (ARCH-040 through ARCH-044) that can be applied during construction inspection. Current verification is "as-built survey; drawing review" which addresses design but not construction inspection. | Sufficient Inspection Scope lens: The renovation requirements all have verification as "As-built survey; drawing review" which verifies the design, not the construction outcome. For inspection sufficiency, construction-phase acceptance criteria are needed. These will likely depend on the existing conditions survey. | Specification.md | Requirements > Old North Shop Renovation > ARCH-040 to ARCH-044; Verification table | -- | PROPOSAL: Architect after existing conditions survey | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Steering Record | 0 | NO_ITEMS | Steering records defined |
| E:guiding:information | guiding | information | Comprehensive Steering Signal | 0 | NO_ITEMS | Signals adequate |
| E:guiding:knowledge | guiding | knowledge | Comprehensive Governance Acumen | 1 | HAS_ITEMS | Accessibility requirement gap |
| E:guiding:wisdom | guiding | wisdom | Principled Strategic Foresight | 0 | NO_ITEMS | Foresight adequately captured in Guidance trade-offs |
| E:applying:data | applying | data | Verified Implementation Record | 1 | HAS_ITEMS | Datasheet missing renovation existing conditions baseline |
| E:applying:information | applying | information | Reliable Deployment Report | 0 | NO_ITEMS | Deployment reporting adequate |
| E:applying:knowledge | applying | knowledge | Proven Implementation Mastery | 0 | NO_ITEMS | Implementation knowledge adequate |
| E:applying:wisdom | applying | wisdom | Principled Execution Foresight | 0 | NO_ITEMS | Execution foresight present in Guidance |
| E:judging:data | judging | data | Conclusive Judgment Record | 1 | HAS_ITEMS | Conflict resolution records undefined |
| E:judging:information | judging | information | Authoritative Verdict Account | 0 | NO_ITEMS | Verdict accounts present via Conflict Table |
| E:judging:knowledge | judging | knowledge | Authoritative Judgment Mastery | 0 | NO_ITEMS | Judgment mastery adequate |
| E:judging:wisdom | judging | wisdom | Principled Adjudication Wisdom | 0 | NO_ITEMS | Adjudication wisdom present |
| E:reviewing:data | reviewing | data | Verified Inspection Evidence | 0 | NO_ITEMS | Inspection evidence requirements present |
| E:reviewing:information | reviewing | information | Comprehensive Audit Report | 1 | HAS_ITEMS | No audit report format defined |
| E:reviewing:knowledge | reviewing | knowledge | Comprehensive Inspection Acumen | 0 | NO_ITEMS | Inspection acumen adequate |
| E:reviewing:wisdom | reviewing | wisdom | Principled Inspection Foresight | 0 | NO_ITEMS | Inspection foresight adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:knowledge | MissingSlot | Specification | Specification | Add consideration of accessibility requirements (barrier-free design) per Alberta Building Code for the maintenance shop. Procedure Step 6.5 mentions "accessibility requirements if applicable" but no requirement or guidance exists in Specification or Guidance. | Comprehensive Governance Acumen lens: Governance acumen requires awareness of all applicable regulatory domains. Accessibility/barrier-free design under ABC is not addressed in Specification requirements or Guidance considerations. Procedure Step 6.5 flags it parenthetically but defers. For an industrial building with office space and washrooms, ABC accessibility provisions likely apply at minimum to common areas. | Specification.md, Guidance.md, Procedure.md | Specification.md#Requirements (absent); Procedure.md#Step 6 (6.5); Guidance.md (absent) | -- | PROPOSAL: Architect to determine per ABC accessibility provisions | TBD |
| E-002 | E:applying:data | MissingSlot | Datasheet | Datasheet | Add a baseline data section for the existing Old North Shop conditions -- either as known attributes or as explicit "TBD pending survey" placeholders for floor area per space, structural condition, existing mechanical/electrical systems. | Verified Implementation Record lens: The Datasheet provides detailed attributes for the New North Shop Addition but the Old North Shop renovation scope has minimal data -- only "105 ft x 40 ft" footprint and "250 sq ft kitchenette." For verified implementation, the baseline record of existing conditions must be established. | Datasheet.md | Attributes > Old North Shop Renovation Scope | -- | PROPOSAL: Architect after existing conditions survey | TBD |
| E-003 | E:judging:data | RationaleGap | Guidance | Guidance | Add guidance on how Conflict Table rulings (CONF-001, CONF-002) should be documented and propagated to Specification and Datasheet once resolved. Define the conflict resolution record format. | Conclusive Judgment Record lens: The Guidance Conflict Table defines two conflicts with "Human Ruling = TBD" but there is no defined mechanism for recording the ruling, updating the affected documents, or maintaining a judgment audit trail. The judgment record is incomplete without a resolution process. | Guidance.md | Conflict Table (CONF-001, CONF-002) | -- | PROPOSAL: Architect / Project Manager | TBD |
| E-004 | E:reviewing:information | Normalization | Multi | Guidance | Normalize the term used for the material supply split between Owner and Contractor. Datasheet uses "Gravel Supply: Supplied by Landfill (Owner)" while Guidance CONF-002 uses "aggregate supply by Owner." Procedure Step 1.4 uses "aggregate supply vs. cement and prep." Standardize terminology. | Comprehensive Audit Report lens: An audit report requires consistent terminology. The material supply arrangement is described with varying terms across documents -- "gravel" (Datasheet), "aggregate" (Guidance, Procedure). While these may refer to the same material, the inconsistency risks confusion in audit and coordination with Civil specification (DEL-005-07). | Datasheet.md, Guidance.md, Procedure.md | Datasheet.md#Conditions (Gravel Supply); Guidance.md#Conflict Table > CONF-002; Procedure.md#Step 1 (1.4) | -- | PROPOSAL: Use consistent term per RFP language; confirm with County | TBD |
