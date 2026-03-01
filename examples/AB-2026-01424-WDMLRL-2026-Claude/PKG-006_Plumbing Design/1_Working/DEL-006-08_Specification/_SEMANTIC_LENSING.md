# Semantic Lensing Register: DEL-006-08 Plumbing Specification

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-006_Plumbing Design/1_Working/DEL-006-08_Specification/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-006-08_Specification/_CONTEXT.md
- _STATUS.md — DEL-006-08_Specification/_STATUS.md (SEMANTIC_READY)
- _SEMANTIC.md — DEL-006-08_Specification/_SEMANTIC.md
- Datasheet.md — DEL-006-08_Specification/Datasheet.md
- Specification.md — DEL-006-08_Specification/Specification.md
- Guidance.md — DEL-006-08_Specification/Guidance.md
- Procedure.md — DEL-006-08_Specification/Procedure.md
- _REFERENCES.md — DEL-006-08_Specification/_REFERENCES.md (read; R-01, R-06 listed)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 2
  - Specification: 11
  - Guidance: 5
  - Procedure: 6
  - Multi: 4
- By matrix:
  - A: 5  B: 4  C: 3  F: 4  D: 3  X: 5  E: 4
- By type:
  - Conflict: 1
  - VerificationGap: 7
  - MissingSlot: 7
  - WeakStatement: 5
  - RationaleGap: 4
  - Normalization: 2
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Emergency shower standard citation TBD |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Hot water provision unspecified |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Safety Code edition unconfirmed |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit provisions addressed in Procedure Phase 4-5 |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Freeze protection method TBD |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Practical execution steps well covered in Procedure |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | Bulk fill pump performance criteria absent |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Process audit covered via QA review and coordination steps |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Value orientation addressed in Guidance Principles |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Merit application implicit in material/workmanship standards |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Worth determination addressed through verification criteria |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality appraisal covered through QA review in Procedure |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Record TBD: Confirm applicable emergency shower standard (ANSI Z358.1 or Alberta Safety Code equivalent) and add specific citation to SPEC-PLB-071 | SPEC-PLB-071 states "Specific standard citation TBD"; prescriptive direction requires a definitive standard reference to govern emergency shower design | Specification.md | Emergency Shower (SPEC-PLB-071) | -- | Plumbing Engineer to confirm | TBD |
| A-002 | A:normative:applying | MissingSlot | Specification | Specification | Add requirement for hot water provision (source type, capacity, location) as a mandatory practice item; currently absent from all SPEC-PLB requirements | Hot water is needed for laundry (SOW-0073) and potentially washroom/wash station, but no SPEC-PLB requirement addresses hot water supply equipment | Specification.md; Guidance.md | Specification: entire Requirements section scanned; Guidance: Considerations > Laundry Services | -- | Plumbing Engineer | TBD |
| A-003 | A:normative:judging | WeakStatement | Specification | Specification | Clarify which specific edition of Alberta Safety Codes (Plumbing Code) and National Plumbing Code applies; current language says "edition TBD" | Compliance determination requires a specific code edition to judge against; the Standards section explicitly marks edition as TBD for both Alberta Safety Code and NPC | Specification.md | Standards | -- | Plumbing Engineer | TBD |
| A-004 | A:operative:guiding | TBD_Question | Guidance | Guidance | Record TBD: Specify freeze protection method for drain traps (trap primers, glycol, heated drain bodies, or other); currently listed as a trade-off with no resolution | Procedural direction for Alberta climate freeze protection is critical for operational reliability but method selection is deferred entirely to design stage without a recommended approach | Guidance.md | Considerations > Industrial-Grade Drainage; Trade-offs | -- | Plumbing Engineer | TBD |
| A-005 | A:operative:judging | VerificationGap | Specification | Specification | Add performance acceptance criteria for bulk water fill pump (flow rate, pressure, connection test protocol) to the Verification section | SPEC-PLB-060 requires a high-volume pump but no quantitative performance threshold is stated; Verification references "commissioning flow test" without pass/fail criteria | Specification.md | Bulk Water Fill System (SPEC-PLB-060); Verification (SPEC-PLB-060 row) | -- | Plumbing Engineer | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Floor drain count uncertain |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Key dimensional data present in Datasheet |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Water treatment artifact gap |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurements consistent across documents |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Drainage routing signal absent |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequate for most systems |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | System descriptions comprehensive |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology drift on wash sink/station |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding of off-grid context well established |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise requirements addressed through P.Eng. requirement |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | System knowledge coverage adequate |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding consistent across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Key discernment items captured in Guidance Conflict Table |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment provisions adequate (trade-offs documented) |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view established through cross-discipline coordination |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Principled reasoning consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | WeakStatement | Datasheet | Datasheet | Clarify floor drain count: Datasheet states "approx. 5 shown" with "exact count pending IFC drawings"; record confirmed count or state explicitly as TBD with method to resolve | Essential facts require precision; the approximate floor drain count creates ambiguity for pipe sizing and drainage design | Datasheet.md | Key Dimensional/Quantity Data (Floor drain locations row) | -- | App B-Plumbing drawing; Plumbing Engineer | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add data entry for water treatment/conditioning system status (either parameters if applicable, or explicit "not required" determination with rationale) | _CONTEXT.md anticipated artifacts include "Water treatment and conditioning specifications" but no data exists in Datasheet for this system; Guidance notes it may be omitted if not required | Datasheet.md; Guidance.md | Datasheet: Systems Covered (entire table); Guidance: Considerations > Water Treatment/Conditioning | -- | Plumbing Engineer | TBD |
| B-003 | B:information:necessity | MissingSlot | Specification | Specification | Add requirement(s) specifying drainage routing destinations for shop floor drains and sump drains (septic vs. dedicated industrial collection vs. mud sump) | SPEC-PLB-042 acknowledges routing destination as TBD; this is an essential signal for downstream design and installation that remains unresolved | Specification.md | Drainage (SPEC-PLB-042) | -- | Plumbing Engineer; CON-PLB-001 in Guidance | TBD |
| B-004 | B:information:consistency | Normalization | Multi | Guidance | Normalize terminology: "wash sink" vs. "wash station" vs. "industrial wash sink" used interchangeably across documents; establish single canonical term | Terminology drift risks miscommunication between specification and installation; Datasheet uses "Industrial wash sink (wash station)", Specification uses "industrial wash sink (wash station)", Guidance uses "wash station" alone | Datasheet.md; Specification.md; Guidance.md | Datasheet: Systems Covered; Specification: SPEC-PLB-024; Guidance: Principles > Off-Grid Water and Waste | -- | Plumbing Engineer | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Baseline | 1 | HAS_ITEMS | Cistern material/installation unspecified |
| C:normative:sufficiency | normative | sufficiency | Governed Competence | 0 | NO_ITEMS | Competence provisions adequate (P.Eng. requirement, QA review) |
| C:normative:completeness | normative | completeness | Exhaustive Governance | 1 | HAS_ITEMS | Venting system absent |
| C:normative:consistency | normative | consistency | Mandated Coherence | 0 | NO_ITEMS | Internal coherence across requirements adequate |
| C:operative:necessity | operative | necessity | Critical Capability | 0 | NO_ITEMS | Critical capabilities identified and addressed |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Fitness | 0 | NO_ITEMS | Fitness demonstration covered through verification steps |
| C:operative:completeness | operative | completeness | Comprehensive Execution | 1 | HAS_ITEMS | Pressure test criteria TBD |
| C:operative:consistency | operative | consistency | Repeatable Fidelity | 0 | NO_ITEMS | Process repeatability adequate through phased procedure |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Criterion | 0 | NO_ITEMS | Quality criteria established through material/workmanship standards |
| C:evaluative:sufficiency | evaluative | sufficiency | Justified Worth | 0 | NO_ITEMS | Justification basis adequate (RFP, code references) |
| C:evaluative:completeness | evaluative | completeness | Holistic Valuation | 0 | NO_ITEMS | Valuation scope covers all systems |
| C:evaluative:consistency | evaluative | consistency | Principled Consistency | 0 | NO_ITEMS | Consistent quality principles applied |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Strengthen SPEC-PLB-012: specify cistern material type, structural support method, and installation approach; current language says "shall be specified" without stating the actual requirement | An enforceable baseline requires concrete material and method specifications, not a meta-requirement to "specify" them; this is self-referential | Specification.md | Water Storage - Cistern (SPEC-PLB-012) | -- | Plumbing Engineer | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add plumbing vent system requirements; drainage venting is a code-required element absent from the specification's requirements sections | Exhaustive governance of plumbing requires vent system specifications (required by National Plumbing Code for all drainage systems); no SPEC-PLB requirement addresses venting | Specification.md | entire Requirements section scanned | -- | Plumbing Engineer; National Plumbing Code | TBD |
| C-003 | C:operative:completeness | VerificationGap | Procedure | Procedure | Add specific pressure test parameters to Step 5.1: test pressure (value or code reference), hold duration, and pass/fail criteria; currently states "TBD" | Comprehensive execution of testing requires defined acceptance thresholds; Procedure Step 5.1 references "test pressure and duration per applicable Safety Code -- TBD" | Procedure.md | Phase 5 (Step 5.1); Verification (Specification completeness row) | -- | Plumbing Engineer; Alberta Safety Code (Plumbing) | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Absolute Compliance Basis | 1 | HAS_ITEMS | Septic permissibility unconfirmed |
| F:normative:sufficiency | normative | sufficiency | Verifiable Mandate | 1 | HAS_ITEMS | Emergency shower verification gap |
| F:normative:completeness | normative | completeness | Exhaustive Codification | 0 | NO_ITEMS | Codification scope adequate for current stage |
| F:normative:consistency | normative | consistency | Uniform Governance | 0 | NO_ITEMS | Governance uniform across requirements |
| F:operative:necessity | operative | necessity | Validated Operational Core | 1 | HAS_ITEMS | Cistern adequacy validation absent |
| F:operative:sufficiency | operative | sufficiency | Confirmed Capacity | 0 | NO_ITEMS | Capacity confirmation addressed through commissioning tests |
| F:operative:completeness | operative | completeness | Total Operational Readiness | 0 | NO_ITEMS | Operational readiness covered through phased procedure |
| F:operative:consistency | operative | consistency | Methodical Stability | 0 | NO_ITEMS | Methodical procedure structure consistent |
| F:evaluative:necessity | evaluative | necessity | Fundamental Worthiness | 0 | NO_ITEMS | Worthiness basis established through code compliance |
| F:evaluative:sufficiency | evaluative | sufficiency | Warranted Appraisal | 1 | HAS_ITEMS | Guarantee period verification gap |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Warrant | 0 | NO_ITEMS | Warrant scope adequate |
| F:evaluative:consistency | evaluative | consistency | Principled Dependability | 0 | NO_ITEMS | Dependability principles consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | RationaleGap | Guidance | Guidance | Add rationale confirming that a septic holding tank (vs. septic field or treatment system) is permissible under Alberta Environmental Protection/Safety Code at this specific site location; currently marked as assumption | Absolute compliance basis requires confirmation that the chosen waste disposal method is legally permissible; Guidance notes this as an assumption requiring Plumbing Engineer confirmation | Guidance.md | Considerations > Septic Holding Tank vs. Treatment System | -- | Plumbing Engineer; Alberta Environment | TBD |
| F-002 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add quantitative acceptance criteria for emergency shower: flow rate, temperature range, duration, and reach-time from hazard; current requirements reference "applicable Safety Code" without specifying measurable thresholds | A verifiable mandate requires testable acceptance criteria; SPEC-PLB-072 defers all parameters to design stage without even placeholder values | Specification.md | Emergency Shower (SPEC-PLB-071, SPEC-PLB-072); Verification (SPEC-PLB-070 row) | -- | Plumbing Engineer; ANSI Z358.1 or Alberta equivalent | TBD |
| F-003 | F:operative:necessity | RationaleGap | Guidance | Guidance | Add rationale for cistern sizing adequacy: document whether 50,000 L meets full operational demand profile (pressure washing, wash bay, washroom, laundry, emergency shower reserve, and refill turnaround) | Validated operational core requires evidence that the cistern capacity is adequate; Guidance notes this as an assumption but no demand analysis is referenced | Guidance.md | Principles > Cistern-Centric System Design | -- | Plumbing Engineer; DEL-006-07 Calculation Package | TBD |
| F-004 | F:evaluative:sufficiency | VerificationGap | Specification | Procedure | Add verification method for 2-year guarantee period obligations: define how defect reporting, rectification tracking, and warranty claims are managed; Verification section lists only "Guarantee records maintained" without acceptance criteria | Warranted appraisal of quality requires a verifiable guarantee administration process; SPEC-PLB-008 states the obligation but verification is vague | Specification.md; Procedure.md | Specification: Verification (SPEC-PLB-008 row); Procedure: Records | -- | PM; CCDC 14-2013 | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Commanding Regulatory Anchor | 0 | NO_ITEMS | Regulatory anchor established through Alberta Safety Codes framework |
| D:normative:applying | normative | applying | Enforced Protocol | 1 | HAS_ITEMS | Submittal review protocol incomplete |
| D:normative:judging | normative | judging | Definitive Ruling | 0 | NO_ITEMS | Ruling mechanisms in place (P.Eng. stamp, Safety Codes Officer) |
| D:normative:reviewing | normative | reviewing | Sovereign Standard Review | 0 | NO_ITEMS | Standard review covered through coordination and QA |
| D:operative:guiding | operative | guiding | Grounded Process Navigation | 1 | HAS_ITEMS | Information exchange milestone gap |
| D:operative:applying | operative | applying | Proven Implementation | 0 | NO_ITEMS | Implementation steps well defined in Procedure |
| D:operative:judging | operative | judging | Capability Confirmation | 0 | NO_ITEMS | Capability confirmed through commissioning tests |
| D:operative:reviewing | operative | reviewing | Stable Procedural Scrutiny | 0 | NO_ITEMS | Procedural scrutiny covered through QA review step |
| D:evaluative:guiding | evaluative | guiding | Grounded Merit Direction | 0 | NO_ITEMS | Merit direction provided through Guidance principles |
| D:evaluative:applying | evaluative | applying | Proven Quality Deployment | 1 | HAS_ITEMS | Material quality standards underspecified |
| D:evaluative:judging | evaluative | judging | Conclusive Merit Judgment | 0 | NO_ITEMS | Merit judgment covered through verification criteria |
| D:evaluative:reviewing | evaluative | reviewing | Grounded Quality Assurance | 0 | NO_ITEMS | QA grounded in procedure and verification |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | MissingSlot | Procedure | Procedure | Add submittal review acceptance criteria: define what constitutes conformance vs. non-conformance for shop drawings and product submittals in Step 4.1; currently only says "for conformance with specification" | Enforced protocol requires defined acceptance/rejection criteria for submittal review to ensure consistent enforcement | Procedure.md | Phase 4 (Step 4.1) | -- | Plumbing Engineer | TBD |
| D-002 | D:operative:guiding | MissingSlot | Procedure | Procedure | Add information exchange milestones and drawing issue dates for interdisciplinary coordination referenced in Step 1.4; currently only says "establish" without defining expected timeline or sequence | Grounded process navigation requires concrete milestone dates or sequencing logic for the six coordinating disciplines; the step is procedurally hollow without them | Procedure.md | Phase 1 (Step 1.4) | -- | PM; Plumbing Engineer | TBD |
| D-003 | D:evaluative:applying | WeakStatement | Specification | Specification | Strengthen material quality requirements: SPEC-PLB-022 says pipe material "shall be specified" and SPEC-PLB-043 says drain specifications "shall include" material types but neither states actual material standards or acceptable types | Proven quality deployment requires concrete material specifications (e.g., acceptable pipe materials, ASTM standards) rather than deferred self-referential requirements | Specification.md | Water Distribution (SPEC-PLB-022); Drainage (SPEC-PLB-043) | -- | Plumbing Engineer | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Commanding First Principle | 0 | NO_ITEMS | First principles well established (off-grid context, code compliance) |
| X:guiding:sufficiency | guiding | sufficiency | Justified Steering | 1 | HAS_ITEMS | Simultaneous demand justification absent |
| X:guiding:completeness | guiding | completeness | Exhaustive Coverage Scope | 0 | NO_ITEMS | Coverage scope adequate across all systems |
| X:guiding:consistency | guiding | consistency | Harmonized Authority | 0 | NO_ITEMS | Authority harmonized across documents |
| X:applying:necessity | applying | necessity | Mandatory Action Basis | 1 | HAS_ITEMS | Existing septic removal procedure underspecified |
| X:applying:sufficiency | applying | sufficiency | Sufficient Conformance | 0 | NO_ITEMS | Conformance mechanisms adequate |
| X:applying:completeness | applying | completeness | Total Implementation Record | 0 | NO_ITEMS | Implementation records defined in Procedure |
| X:applying:consistency | applying | consistency | Standardized Workmanship | 0 | NO_ITEMS | Workmanship standards referenced consistently |
| X:judging:necessity | judging | necessity | Binding Factual Verdict | 1 | HAS_ITEMS | Safety Codes Officer role underspecified |
| X:judging:sufficiency | judging | sufficiency | Competent Determination | 0 | NO_ITEMS | Determination competence addressed through P.Eng. requirement |
| X:judging:completeness | judging | completeness | Exhaustive Assessment Record | 0 | NO_ITEMS | Assessment records defined in Procedure |
| X:judging:consistency | judging | consistency | Coherent Ruling Standard | 0 | NO_ITEMS | Ruling standards coherent |
| X:reviewing:necessity | reviewing | necessity | Core Verification Basis | 1 | HAS_ITEMS | Sanitary flow test criteria weak |
| X:reviewing:sufficiency | reviewing | sufficiency | Sufficient Audit Evidence | 0 | NO_ITEMS | Audit evidence requirements defined |
| X:reviewing:completeness | reviewing | completeness | Complete Inspection Archive | 1 | HAS_ITEMS | O&M manual scope undefined |
| X:reviewing:consistency | reviewing | consistency | Dependable Audit Calibration | 0 | NO_ITEMS | Audit calibration consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | RationaleGap | Guidance | Guidance | Add rationale for simultaneous demand scenario analysis: document expected concurrent water demands and how pump sizing addresses them (e.g., pressure washer + wash station + washroom simultaneously) | Justified steering of pump selection requires documented demand scenarios; Guidance mentions this as an assumption deferred to DEL-006-07 but provides no bounding scenarios for the Plumbing Engineer | Guidance.md | Principles > Cistern-Centric System Design | -- | Plumbing Engineer; DEL-006-07 | TBD |
| X-002 | X:applying:necessity | WeakStatement | Specification | Specification | Strengthen SPEC-PLB-031: add environmental requirements for existing septic tank removal (contaminated soil handling, decommissioning protocol, disposal requirements) | Mandatory action basis for septic removal requires more than "shall be removed"; environmental and safety obligations for removing an existing septic tank in Alberta are not addressed | Specification.md | Septic/Sanitary System (SPEC-PLB-031) | -- | Plumbing Engineer; Alberta Environment | TBD |
| X-003 | X:judging:necessity | VerificationGap | Multi | Specification | Add clarity on Safety Codes Officer inspection milestones: define which inspection hold points are mandatory and when the Safety Codes Officer must be present vs. notified | Binding factual verdict from Safety Codes Officer requires defined inspection hold points; Specification says "at inspection milestone" and Procedure says "coordinate" but neither defines the mandatory hold points | Specification.md; Procedure.md | Specification: Verification (All SPEC-PLB row); Procedure: Phase 4 (Step 4.3) | -- | Alberta Safety Codes Officer; PM | TBD |
| X-004 | X:reviewing:necessity | VerificationGap | Procedure | Specification | Add acceptance criteria for sanitary drainage test (Step 5.6): define what constitutes successful connection and function (flow rate, leak test, backflow check) | Core verification basis for sanitary system requires testable pass/fail criteria; Step 5.6 says "confirm connections and function" without measurable thresholds | Procedure.md | Phase 5 (Step 5.6) | -- | Plumbing Engineer | TBD |
| X-005 | X:reviewing:completeness | MissingSlot | Procedure | Procedure | Add O&M manual content scope: define which equipment requires O&M documentation (cistern, pumps, septic tank, emergency shower, water heater if applicable) and minimum content requirements | Complete inspection archive requires defined O&M deliverables; Procedure Records section lists "O&M manuals" without specifying scope, content requirements, or equipment coverage | Procedure.md | Records (O&M manuals row) | -- | PM; Plumbing Engineer | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Reference Base | 1 | HAS_ITEMS | Reference base incomplete |
| E:guiding:information | guiding | information | Coherent Situational Briefing | 0 | NO_ITEMS | Situational briefing well provided in Guidance |
| E:guiding:knowledge | guiding | knowledge | Integrated Strategic Depth | 0 | NO_ITEMS | Strategic depth adequate through cross-discipline coordination |
| E:guiding:wisdom | guiding | wisdom | Sovereign Foresight | 0 | NO_ITEMS | Foresight provisions adequate in Guidance trade-offs |
| E:applying:data | applying | data | Verified Practice Record | 1 | HAS_ITEMS | As-built verification gap |
| E:applying:information | applying | information | Contextual Delivery Account | 0 | NO_ITEMS | Delivery context well documented |
| E:applying:knowledge | applying | knowledge | Validated Trade Mastery | 0 | NO_ITEMS | Trade mastery addressed through P.Eng. and QA |
| E:applying:wisdom | applying | wisdom | Principled Delivery Insight | 0 | NO_ITEMS | Delivery insight adequate in Guidance |
| E:judging:data | judging | data | Verified Evidentiary Finding | 0 | NO_ITEMS | Evidentiary basis defined through test records |
| E:judging:information | judging | information | Transparent Judgment Account | 0 | NO_ITEMS | Judgment transparency adequate |
| E:judging:knowledge | judging | knowledge | Authoritative Assessment Mastery | 0 | NO_ITEMS | Assessment mastery addressed through P.Eng. role |
| E:judging:wisdom | judging | wisdom | Principled Adjudicative Insight | 1 | HAS_ITEMS | Conflict resolution process absent |
| E:reviewing:data | reviewing | data | Verified Inspection Finding | 0 | NO_ITEMS | Inspection findings defined through records |
| E:reviewing:information | reviewing | information | Comprehensive Audit Account | 0 | NO_ITEMS | Audit account addressed through records |
| E:reviewing:knowledge | reviewing | knowledge | Comprehensive Verification Mastery | 0 | NO_ITEMS | Verification mastery covered |
| E:reviewing:wisdom | reviewing | wisdom | Principled Verification Wisdom | 1 | HAS_ITEMS | Septic conflict partially resolved |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | Normalization | Multi | Datasheet | Normalize reference identifiers: _REFERENCES.md uses R-01 and R-06; Datasheet References section uses the same scheme; Specification and Guidance cite by document name and section only. Establish whether Ref IDs should appear consistently across all documents | Authoritative reference base requires consistent citation format to support traceability; the reference ID scheme is used in some documents but not others | Datasheet.md; Specification.md; Guidance.md; _REFERENCES.md | Datasheet: References; Specification: Requirements (Source columns); Guidance: throughout | -- | PM | TBD |
| E-002 | E:applying:data | VerificationGap | Procedure | Procedure | Add acceptance criteria for as-built drawing review (Step 5.8): define what constitutes "all field changes captured" and who verifies accuracy against IFC drawings | Verified practice record requires a defined acceptance standard for as-built accuracy; Step 5.8 and the Verification table say "All field changes captured" without defining the verification method or responsible reviewer | Procedure.md | Phase 5 (Step 5.8); Verification (As-built accuracy row) | -- | Plumbing Engineer; PM | TBD |
| E-003 | E:judging:wisdom | RationaleGap | Guidance | Guidance | Add conflict resolution procedure: define how CON-PLB items are escalated, decided, and recorded when human rulings are needed; currently all three CON-PLB items have "TBD" rulings with no process to resolve them | Principled adjudicative insight requires a defined decision process, not just a list of unresolved questions; the Conflict Table captures conflicts but provides no resolution workflow | Guidance.md | Conflict Table (for human ruling) | -- | PM; Owner | TBD |
| E-004 | E:reviewing:wisdom | Conflict | Multi | Guidance | Surface conflict: RFP s3.4 uses "removal and relocate" for existing septic tank; Decomposition D-002 resolves as "removal IN, relocation OUT"; Guidance CON-PLB-003 proposes following D-002 but marks Human Ruling as TBD; confirm Owner direction | Principled verification wisdom requires that this conflict be definitively resolved before specification is finalized; the conflict is identified but unresolved | Guidance.md; Specification.md | Guidance: Conflict Table (CON-PLB-003); Specification: SPEC-PLB-031 | Guidance.md#Conflict Table (CON-PLB-003: follow D-002) vs. RFP s3.4 ("removal and relocate") | PM; Owner (Camrose County) | TBD |

---

**End of Semantic Lensing Register.**
