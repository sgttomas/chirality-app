# Semantic Lensing Register: DEL-009-01 Development Permit Application & Approval

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-009_Permitting & Regulatory Compliance/1_Working/DEL-009-01_Development-Permit/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-009-01_Development-Permit/_CONTEXT.md
- _STATUS.md — DEL-009-01_Development-Permit/_STATUS.md (Status: SEMANTIC_READY, 2026-02-26)
- _SEMANTIC.md — DEL-009-01_Development-Permit/_SEMANTIC.md (7 matrices parsed: A, B, C, F, D, X, E)
- Datasheet.md — DEL-009-01_Development-Permit/Datasheet.md
- Specification.md — DEL-009-01_Development-Permit/Specification.md
- Guidance.md — DEL-009-01_Development-Permit/Guidance.md
- Procedure.md — DEL-009-01_Development-Permit/Procedure.md
- _REFERENCES.md — DEL-009-01_Development-Permit/_REFERENCES.md (read; pointers listed, scope not expanded)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 21
- By document:
  - Datasheet: 4
  - Specification: 8
  - Guidance: 3
  - Procedure: 3
  - Multi: 3
- By matrix:
  - A: 5  B: 3  C: 3  F: 3  D: 3  X: 2  E: 2
- By type:
  - Conflict: 0
  - VerificationGap: 4
  - MissingSlot: 5
  - WeakStatement: 3
  - RationaleGap: 3
  - Normalization: 2
  - TBD_Question: 4
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Specific code identifiers TBD weakens prescriptive direction |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Application form/checklist TBD limits mandatory practice definition |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | No acceptance criteria for application completeness in Specification |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Inspection requirements and audit trail well-covered across docs |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Step 1-7 provides clear procedural direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Pre-application consultation is suggested but lacks procedural commitment |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Procedure Verification table addresses performance checks |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records section in Procedure provides audit trail |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | No rationale for early-vs-late submission trade-off decision criteria |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs table in Guidance addresses merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Success criteria in _CONTEXT.md and verification in Specification are aligned |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Verification approach in Specification is adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Datasheet | Record TBD: Identify specific Alberta Building Code and Safety Code edition/identifiers applicable to this building type and occupancy | Three requirements (REQ-009-01-003, REQ-009-01-004) and the Standards table reference "applicable Alberta building codes" and "Alberta Safety Codes" but no specific code identifiers are named anywhere, weakening prescriptive direction | Specification.md#Standards; Datasheet.md#Attributes | Standards table; Attributes table ("Specific Code References: TBD") | -- | Camrose County permitting authority; Alberta Municipal Affairs | TBD |
| A-002 | A:normative:applying | TBD_Question | Procedure | Datasheet | Record TBD: Obtain Camrose County development permit application form and checklist to define mandatory practice content | The mandatory practice for application preparation cannot be fully specified until the authority's application form and requirements are obtained; currently marked TBD in Datasheet and Procedure | Datasheet.md#Attributes; Procedure.md#Steps | "Application Template / Form: TBD"; Step 2 | -- | Camrose County permitting office | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add measurable acceptance criteria for REQ-009-01-002 (application completeness) beyond reference to an unknown authority checklist | REQ-009-01-002 verification relies on "review application package against authority checklist" but the checklist itself is TBD, leaving the compliance determination method undefined until external input is received | Specification.md#Verification | REQ-009-01-002 verification row | -- | Specification.md (normative authority) | TBD |
| A-004 | A:operative:applying | WeakStatement | Guidance | Guidance | Strengthen pre-application consultation from "should consider" to a committed procedural step or explicitly mark as optional with rationale | Guidance Considerations recommends pre-application consultation as "risk mitigation" but Procedure Step 1.3 only says "confirm whether...available and/or recommended" -- the practical execution commitment is ambiguous | Guidance.md#Considerations; Procedure.md#Steps | "Pre-Application Consultation"; Step 1.3 | -- | Project Manager decision | TBD |
| A-005 | A:evaluative:guiding | RationaleGap | Guidance | Guidance | Add decision criteria or thresholds for the early-vs-late submission trade-off to support value-based decision-making | Guidance Trade-offs table describes early vs. late submission and notes "earlier submission is generally preferred" but provides no criteria for when the late option would be justified, leaving value orientation incomplete | Guidance.md#Trade-offs | Application Timing row | -- | Guidance.md (directional authority) | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Processing timeline is an essential fact that is TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet provides adequate evidence for known attributes |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Datasheet missing permit processing timeline data |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Data values consistent across docs where present |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Submission receipt and status tracking signals are defined in Procedure |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for permit process is adequate in Guidance |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Account of permit lifecycle is comprehensive across 4 docs |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | No incoherent messaging detected across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding of permit process is present in Guidance |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise requirements implicitly addressed via P.Eng. stamp requirement |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Mastery level knowledge not needed for this deliverable type |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 1 | HAS_ITEMS | No guidance on discerning when to escalate permit delays |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-offs in Guidance provide adequate judgment support |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance provides holistic perspective on permit significance |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and grounded in RFP sources |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Obtain expected processing timeline from Camrose County for development permit review | Processing timeline is an essential fact for schedule planning (REQ-009-01-008) but is TBD across all documents; without it, schedule constraint verification is incomplete | Datasheet.md#Attributes; Procedure.md#Steps | "Processing Timeline: TBD"; Step 2.4 | -- | Camrose County permitting office | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add a data field for permit processing timeline once obtained from authority | The Datasheet Attributes table lacks a resolved value for processing timeline; Procedure Step 2.4 directs obtaining this but the Datasheet should be updated when known | Datasheet.md#Attributes | "Processing Timeline: TBD" | -- | Datasheet.md (descriptive authority) | TBD |
| B-003 | B:wisdom:necessity | MissingSlot | Guidance | Guidance | Add guidance on escalation triggers and decision thresholds for schedule delays during permit review | Procedure Step 5.2 mentions "escalate to County project manager if processing delays threaten the project schedule" but no criteria or thresholds are provided for when to escalate, leaving essential discernment unsupported | Guidance.md#Considerations; Procedure.md#Steps | entire Considerations section; Step 5.2 | -- | Guidance.md (directional authority) | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Obligatory Compliance Awareness | 1 | HAS_ITEMS | Awareness of specific code obligations incomplete |
| C:normative:sufficiency | normative | sufficiency | Competent Regulatory Validation | 0 | NO_ITEMS | Validation approach via authority review and P.Eng. stamp is defined |
| C:normative:completeness | normative | completeness | Total Conformance Coverage | 1 | HAS_ITEMS | Conformance coverage gap: OH&S obligations mentioned in Standards but not traced to requirements |
| C:normative:consistency | normative | consistency | Coherent Regulatory Alignment | 0 | NO_ITEMS | Regulatory framework references are consistent |
| C:operative:necessity | operative | necessity | Critical Procedural Competence | 0 | NO_ITEMS | Procedure is competently structured with clear step sequencing |
| C:operative:sufficiency | operative | sufficiency | Verified Execution Capability | 0 | NO_ITEMS | Execution steps are sufficiently defined for current stage |
| C:operative:completeness | operative | completeness | Full Operational Mastery | 0 | NO_ITEMS | Procedure covers full lifecycle from contact through inspections |
| C:operative:consistency | operative | consistency | Stable Operational Uniformity | 0 | NO_ITEMS | Procedure steps are internally consistent |
| C:evaluative:necessity | evaluative | necessity | Fundamental Merit Appraisal | 0 | NO_ITEMS | Success criteria in _CONTEXT.md provide necessary merit measures |
| C:evaluative:sufficiency | evaluative | sufficiency | Substantiated Value Judgment | 0 | NO_ITEMS | Value judgments in Guidance are substantiated with sources |
| C:evaluative:completeness | evaluative | completeness | Exhaustive Quality Assessment | 1 | HAS_ITEMS | No quality criteria defined for the application package itself |
| C:evaluative:consistency | evaluative | consistency | Principled Evaluation Consistency | 0 | NO_ITEMS | Evaluation principles consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | Normalization | Multi | Guidance | Clarify whether OH&S/Prime Contractor obligations in Standards table apply to the development permit deliverable or only to construction execution | The Standards table in Specification lists Alberta OH&S and Prime Contractor designation, but no requirement in the Requirements section traces to OH&S for this permit deliverable; the Datasheet does not mention OH&S either, creating inconsistency in obligatory compliance awareness | Specification.md#Standards; Datasheet.md#Attributes | Standards table row "Alberta Occupational Health and Safety"; entire Datasheet Attributes | -- | Specification.md (normative authority) | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add a requirement tracing to CFTA/NWPTA obligations if applicable to this deliverable, or remove from Standards table with rationale | The Standards table lists CFTA and NWPTA as "Applicable (procurement context)" but no requirements reference these trade agreements; either they should have traced requirements or be explicitly noted as not requiring deliverable-level action | Specification.md#Standards | Standards table rows "CFTA" and "NWPTA" | -- | Specification.md (normative authority) | TBD |
| C-003 | C:evaluative:completeness | VerificationGap | Specification | Specification | Add acceptance criteria for application package quality (e.g., internal review sign-off, completeness checklist review) as a formal verification step | Procedure Step 3.4 describes internal review before submission but this is not reflected in Specification Verification table as a formal verification approach for any requirement, leaving quality assessment of the package unverified normatively | Specification.md#Verification; Procedure.md#Steps | Verification table; Step 3.4 | -- | Specification.md (normative authority) | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Certified Obligation Mandate | 0 | NO_ITEMS | Obligation mandate (REQ-009-01-001) is clearly certified via R-01 |
| F:normative:sufficiency | normative | sufficiency | Verified Compliance Basis | 1 | HAS_ITEMS | Compliance basis for code compliance requirements is unverifiable until codes are identified |
| F:normative:completeness | normative | completeness | Absolute Regulatory Documentation | 1 | HAS_ITEMS | Regulatory documentation incomplete due to missing authority-specific documents |
| F:normative:consistency | normative | consistency | Systematic Compliance Coherence | 0 | NO_ITEMS | Compliance framework is coherent across the four documents |
| F:operative:necessity | operative | necessity | Core Process Imperative | 0 | NO_ITEMS | Core process steps are present and imperative |
| F:operative:sufficiency | operative | sufficiency | Sufficient Workflow Proficiency | 0 | NO_ITEMS | Workflow is sufficiently proficient for current deliverable stage |
| F:operative:completeness | operative | completeness | Total Workflow Documentation | 0 | NO_ITEMS | Workflow documentation is total from Step 1 through Step 7 |
| F:operative:consistency | operative | consistency | Dependable Process Alignment | 0 | NO_ITEMS | Process steps are aligned with requirements |
| F:evaluative:necessity | evaluative | necessity | Core Quality Imperative | 0 | NO_ITEMS | Quality imperatives present via verification checks |
| F:evaluative:sufficiency | evaluative | sufficiency | Substantiated Quality Basis | 0 | NO_ITEMS | Quality basis is substantiated through evidence requirements |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Value Documentation | 1 | HAS_ITEMS | Permit conditions downstream flow not fully documented |
| F:evaluative:consistency | evaluative | consistency | Consistent Appraisal Standard | 0 | NO_ITEMS | Appraisal standards consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add verification approach for confirming which specific Alberta Building Codes and Safety Codes apply, once identified | REQ-009-01-003 and REQ-009-01-004 require code compliance but the verification approach relies on "design review confirming code compliance" without knowing which codes; the compliance basis cannot be verified until specific codes are identified | Specification.md#Verification | REQ-009-01-003 and REQ-009-01-004 verification rows | -- | Specification.md (normative authority) | TBD |
| F-002 | F:normative:completeness | MissingSlot | Datasheet | Datasheet | Add data fields for Camrose County development permit bylaw number and application checklist reference once obtained | Absolute regulatory documentation requires identifying the specific municipal bylaw and application requirements; these are TBD across all documents and represent a gap in regulatory documentation completeness | Datasheet.md#Attributes; Specification.md#Standards | Attributes table; Standards table "Camrose County Development Permit Bylaw/Requirements: TBD" | -- | Camrose County; Datasheet.md | TBD |
| F-003 | F:evaluative:completeness | MissingSlot | Specification | Specification | Add a requirement or documentation section describing how permit conditions flow into downstream deliverables (DEL-009-04, construction packages) | Guidance mentions conditions must be communicated to construction packages and DEL-009-04, and Procedure Step 6.4 lists distribution, but Specification has no requirement governing the mechanism or completeness of downstream condition flow, leaving value documentation incomplete | Specification.md#Requirements; Guidance.md#Considerations | Requirements section (no downstream flow requirement); "Permit Conditions as Downstream Constraints" | -- | Specification.md (normative authority) | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Authoritative Regulatory Command | 0 | NO_ITEMS | Regulatory command clearly derived from R-01 authority |
| D:normative:applying | normative | applying | Compulsory Regulatory Practice | 1 | HAS_ITEMS | Compulsory practice depends on unknown authority application requirements |
| D:normative:judging | normative | judging | Definitive Conformance Ruling | 0 | NO_ITEMS | Conformance determination method defined via verification table |
| D:normative:reviewing | normative | reviewing | Mandatory Oversight Framework | 0 | NO_ITEMS | Oversight framework (inspections, County presence) is defined |
| D:operative:guiding | operative | guiding | Resolved Workflow Directive | 0 | NO_ITEMS | Workflow directives resolved in Procedure Steps 1-7 |
| D:operative:applying | operative | applying | Resolved Operational Delivery | 0 | NO_ITEMS | Operational delivery steps are resolved |
| D:operative:judging | operative | judging | Documented Capability Verdict | 0 | NO_ITEMS | Capability verification defined in Procedure Verification table |
| D:operative:reviewing | operative | reviewing | Resolved Operational Review | 0 | NO_ITEMS | Operational review addressed through records and audit trail |
| D:evaluative:guiding | evaluative | guiding | Resolved Merit Stewardship | 1 | HAS_ITEMS | Schedule trade-off thresholds unresolved |
| D:evaluative:applying | evaluative | applying | Resolved Value Realization | 0 | NO_ITEMS | Value realization addressed through success criteria |
| D:evaluative:judging | evaluative | judging | Documented Value Verdict | 1 | HAS_ITEMS | No explicit success/failure criteria for the permit itself |
| D:evaluative:reviewing | evaluative | reviewing | Resolved Evaluation Standard | 0 | NO_ITEMS | Evaluation standard resolved through verification approaches |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | WeakStatement | Specification | Specification | Strengthen REQ-009-01-002 by specifying minimum application content requirements independent of authority checklist (e.g., site plan, legal land description, building description) | REQ-009-01-002 states application "shall include all information...required by Camrose County's permitting authority" but the specific content is entirely deferred to an unknown checklist; Procedure Step 3.1 lists anticipated content items that could serve as baseline requirements | Specification.md#Requirements; Procedure.md#Steps | REQ-009-01-002; Step 3.1 | -- | Specification.md (normative authority) | TBD |
| D-002 | D:evaluative:guiding | RationaleGap | Guidance | Guidance | Add rationale for choosing between single permit vs. phased permit approach, including schedule and cost implications | Guidance Trade-offs table lists "Single development permit for entire project" vs. "Multiple permits for phased scope" but only says "ASSUMPTION -- likely a single permit...to be confirmed"; no rationale supports this assumption | Guidance.md#Trade-offs | Permit Scope row | -- | Guidance.md (directional authority) | TBD |
| D-003 | D:evaluative:judging | VerificationGap | Specification | Specification | Add explicit success/failure criteria for the development permit outcome (e.g., permit obtained without conditions that require design changes, or within schedule window) | _CONTEXT.md lists "Approval obtained with minimal conditions" as a success criterion but this is not traced to a requirement or verification approach in Specification; the documented value verdict for this deliverable is incomplete | Specification.md#Verification; _CONTEXT.md | Verification table; Success Criteria | -- | Specification.md (normative authority) | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Imperative Directional Verity | 0 | NO_ITEMS | Directional verity present via RFP traceability |
| X:guiding:sufficiency | guiding | sufficiency | Sufficient Authority Basis | 0 | NO_ITEMS | Authority basis sufficient from R-01 |
| X:guiding:completeness | guiding | completeness | Exhaustive Guidance Documentation | 0 | NO_ITEMS | Guidance documentation is exhaustive for current stage |
| X:guiding:consistency | guiding | consistency | Consistent Guidance Alignment | 0 | NO_ITEMS | Guidance is consistently aligned across documents |
| X:applying:necessity | applying | necessity | Mandatory Implementation Verity | 0 | NO_ITEMS | Implementation verities traced to RFP requirements |
| X:applying:sufficiency | applying | sufficiency | Sufficient Execution Evidence | 1 | HAS_ITEMS | Execution evidence plan does not address resubmission scenario |
| X:applying:completeness | applying | completeness | Exhaustive Implementation Record | 0 | NO_ITEMS | Records section in Procedure is comprehensive |
| X:applying:consistency | applying | consistency | Dependable Implementation Alignment | 0 | NO_ITEMS | Implementation steps aligned with requirements |
| X:judging:necessity | judging | necessity | Critical Compliance Finding | 0 | NO_ITEMS | Compliance findings approach defined |
| X:judging:sufficiency | judging | sufficiency | Sufficient Determination Basis | 0 | NO_ITEMS | Determination basis is sufficient |
| X:judging:completeness | judging | completeness | Exhaustive Determination Record | 0 | NO_ITEMS | Determination records defined in Procedure Records table |
| X:judging:consistency | judging | consistency | Dependable Determination Coherence | 0 | NO_ITEMS | Determination approaches coherent across docs |
| X:reviewing:necessity | reviewing | necessity | Critical Audit Verity | 0 | NO_ITEMS | Audit verity supported through inspection log and distribution records |
| X:reviewing:sufficiency | reviewing | sufficiency | Sufficient Audit Basis | 1 | HAS_ITEMS | Retention period basis incomplete |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Audit Documentation | 0 | NO_ITEMS | Audit documentation is exhaustive in Records table |
| X:reviewing:consistency | reviewing | consistency | Consistent Audit Alignment | 0 | NO_ITEMS | Audit requirements consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:sufficiency | WeakStatement | Procedure | Procedure | Add a procedure step or sub-step addressing the resubmission scenario (deficiency notice from authority) including records and timeline impact | Guidance Considerations mentions "likelihood of a deficiency notice requiring resubmission" but Procedure Step 5.1 only says "respond promptly to any authority requests for additional information, clarification, or resubmission" without defining the resubmission workflow, leaving execution evidence planning incomplete | Procedure.md#Steps; Guidance.md#Trade-offs | Step 5.1; Pre-Application Consultation trade-off | -- | Procedure.md (operational authority) | TBD |
| X-002 | X:reviewing:sufficiency | Normalization | Procedure | Procedure | Clarify records retention terminology: align "Project duration + archive per contract" with CCDC 14-2013 retention requirements and the "2-year guarantee period" noted for permit/conditions records | Procedure Records table uses two different retention standards: "Project duration + archive per contract" for most records and "Project duration + 2-year guarantee period minimum" for the permit and conditions; the basis for the distinction and the definition of "archive per contract" are not explained | Procedure.md#Records | Records table, Retention column | -- | Procedure.md; CCDC 14-2013 (contractual authority) | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Substantiated Directive Authority | 0 | NO_ITEMS | Directive authority substantiated via R-01 citations |
| E:guiding:information | guiding | information | Informed Prescriptive Indicator | 0 | NO_ITEMS | Prescriptive indicators informed by source references |
| E:guiding:knowledge | guiding | knowledge | Thorough Prescriptive Command | 0 | NO_ITEMS | Prescriptive command thorough for current deliverable stage |
| E:guiding:wisdom | guiding | wisdom | Principled Directional Foresight | 1 | HAS_ITEMS | Foresight gap on concurrent permit application scenario |
| E:applying:data | applying | data | Verified Operational Evidence | 0 | NO_ITEMS | Operational evidence plan defined in Procedure |
| E:applying:information | applying | information | Actionable Practice Indicator | 0 | NO_ITEMS | Practice indicators defined in verification checks |
| E:applying:knowledge | applying | knowledge | Competent Execution Mastery | 0 | NO_ITEMS | Execution mastery at appropriate level for permit deliverable |
| E:applying:wisdom | applying | wisdom | Grounded Operational Prudence | 0 | NO_ITEMS | Operational prudence addressed through risk considerations |
| E:judging:data | judging | data | Verified Compliance Evidence | 0 | NO_ITEMS | Compliance evidence plan defined |
| E:judging:information | judging | information | Informed Conformance Indicator | 0 | NO_ITEMS | Conformance indicators present in verification table |
| E:judging:knowledge | judging | knowledge | Thorough Adjudication Command | 0 | NO_ITEMS | Adjudication command appropriate for deliverable scope |
| E:judging:wisdom | judging | wisdom | Principled Adjudicative Foresight | 0 | NO_ITEMS | Foresight provisions in Guidance (Conflict Table TBDs) adequate |
| E:reviewing:data | reviewing | data | Verified Inspection Evidence | 0 | NO_ITEMS | Inspection evidence plan defined in Procedure Step 7 |
| E:reviewing:information | reviewing | information | Informed Inspection Indicator | 1 | HAS_ITEMS | Inspection scheduling lead time not specified |
| E:reviewing:knowledge | reviewing | knowledge | Thorough Inspection Command | 0 | NO_ITEMS | Inspection command defined through Steps 7.1-7.5 |
| E:reviewing:wisdom | reviewing | wisdom | Principled Inspection Foresight | 0 | NO_ITEMS | Inspection foresight adequate given current deliverable stage |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:wisdom | RationaleGap | Guidance | Guidance | Add guidance on the implications and strategy for concurrent development/building permit applications if Camrose County allows it | Guidance Considerations notes the question of whether permits "are processed simultaneously or strictly sequentially" and flags it as TBD, but does not discuss the strategic implications of either answer or how to plan for both scenarios, leaving directional foresight incomplete | Guidance.md#Considerations | "Relationship to Building Permit" | -- | Guidance.md (directional authority) | TBD |
| E-002 | E:reviewing:information | TBD_Question | Procedure | Procedure | Record TBD: Define minimum scheduling lead time for County representative attendance at inspections | Guidance P-3 states "schedule inspections with sufficient lead time to ensure County availability" and Procedure Step 7.2 says "notify...in advance" but no minimum lead time is specified, leaving the informed inspection indicator incomplete | Guidance.md#Principles; Procedure.md#Steps | P-3; Step 7.2 | -- | County project representative coordination requirements | TBD |
