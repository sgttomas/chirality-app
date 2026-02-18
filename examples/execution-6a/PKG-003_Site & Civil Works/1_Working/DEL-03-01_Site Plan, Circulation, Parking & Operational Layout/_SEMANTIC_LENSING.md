# Semantic Lensing Register: DEL-03-01 Site Plan, Circulation, Parking & Operational Layout

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/PKG-003_Site & Civil Works/1_Working/DEL-03-01_Site Plan, Circulation, Parking & Operational Layout/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-03-01_Site Plan, Circulation, Parking & Operational Layout/_CONTEXT.md (read successfully)
- _STATUS.md -- DEL-03-01_Site Plan, Circulation, Parking & Operational Layout/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md -- DEL-03-01_Site Plan, Circulation, Parking & Operational Layout/_SEMANTIC.md (read successfully; 7 matrices parsed: A, B, C, F, D, X, E)
- Datasheet.md -- DEL-03-01_Site Plan, Circulation, Parking & Operational Layout/Datasheet.md (read successfully)
- Specification.md -- DEL-03-01_Site Plan, Circulation, Parking & Operational Layout/Specification.md (read successfully)
- Guidance.md -- DEL-03-01_Site Plan, Circulation, Parking & Operational Layout/Guidance.md (read successfully)
- Procedure.md -- DEL-03-01_Site Plan, Circulation, Parking & Operational Layout/Procedure.md (read successfully)
- _REFERENCES.md -- DEL-03-01_Site Plan, Circulation, Parking & Operational Layout/_REFERENCES.md (read successfully)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 27
- By document:
  - Datasheet: 5
  - Specification: 10
  - Guidance: 4
  - Procedure: 3
  - Multi: 5
- By matrix:
  - A: 7  B: 4  C: 3  F: 4  D: 3  X: 4  E: 2
- By type:
  - Conflict: 1
  - VerificationGap: 6
  - MissingSlot: 5
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 5
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Weak prescriptive language on parking count |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Missing mandatory accessibility standard details |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Flood hazard compliance verification incomplete |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | AHJ identification gap |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure provides adequate procedural direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Vehicle dimension specifics TBD |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification table adequately covers performance assessment |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records section adequate |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | Lifecycle cost rationale gap |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs section provides adequate merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 1 | HAS_ITEMS | No evaluation criteria for proposal scoring |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Adequately covered by verification checks |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Strengthen REQ-11 parking count requirement; replace "adequate parking" with specific minimum stall count or provide calculation methodology reference | REQ-11 uses "adequate parking" without defining a numeric threshold or calculation basis; this is materially ambiguous for implementation. The ASSUMPTION note acknowledges the gap but does not resolve it. | Specification.md | REQ-11: Adequate Parking and Exterior Storage Space | -- | Specification.md (REQ-11) | TBD |
| A-002 | A:normative:applying | TBD_Question | Specification | Specification | Record TBD: Identify applicable accessible parking stall requirements (Alberta Building Code or Town of Penhold Land Use Bylaw) and add to Standards table | The Standards table lists Alberta Building Code as an ASSUMPTION with "location TBD." Accessible parking stall counts and dimensions are mandatory practice under building/accessibility codes but the specific requirements are not stated. | Specification.md | Standards table | -- | Alberta Building Code / Town of Penhold Land Use Bylaw | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add verification method for flood hazard boundary determination authority -- specify which regulatory body (AEP, municipality) provides the authoritative flood boundary for compliance determination | REQ-10 references the Adjacent Subdivision Design exhibit for the flood boundary, but does not identify which authority (AEP or municipal) has jurisdiction for compliance determination. Guidance mentions AEP as a possible authority but hedges with "if applicable." | Specification.md; Guidance.md | REQ-10; Guidance Principle 4 | -- | Specification.md (REQ-10) | TBD |
| A-004 | A:normative:reviewing | MissingSlot | Multi | Specification | Add identification of all Authorities Having Jurisdiction (AHJ) for site plan approval (municipal development authority, AEP flood hazard, Alberta transportation for road access) | No document explicitly lists the AHJs that must review/approve the site plan. Regulatory audit readiness requires knowing which authorities will review. | Specification.md; Procedure.md | entire document scanned | -- | Specification.md (Standards section) | TBD |
| A-005 | A:operative:applying | TBD_Question | Multi | Datasheet | Record TBD: Confirm specific fire apparatus dimensions (Type 1 engine and Type 1 aerial) for swept-path analysis; source from Fire Department or apparatus manufacturer specifications | Multiple documents flag this as TBD/ASSUMPTION. Without confirmed vehicle dimensions, the turning template deliverable cannot be validated. | Datasheet.md; Guidance.md; Procedure.md | Datasheet Circulation & Parking; Guidance Considerations - Turning Radius; Procedure Step 4 | -- | Fire Department apparatus specifications | TBD |
| A-006 | A:evaluative:guiding | RationaleGap | Guidance | Guidance | Add rationale for surfacing zone boundary decisions -- explain why specific areas are designated aggregate vs. asphalt beyond the OSR minimum (lifecycle cost, dust control, operational frequency considerations) | Guidance Principle 3 notes surfacing zones are design decisions but does not provide lifecycle cost or operational frequency rationale to guide boundary placement beyond the OSR minimum requirements. | Guidance.md | Principles - Section 3 | -- | Guidance.md | TBD |
| A-007 | A:evaluative:judging | MissingSlot | Specification | Guidance | Add proposal evaluation criteria or scoring rubric references for site plan quality assessment (if available from RFP evaluation criteria) | The site plan is a proposal submission element but no document captures how the Owner will evaluate/score site plan quality. This affects "worth determination" of the design. | Specification.md | entire document scanned | -- | RFP evaluation criteria | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Missing parcel boundary coordinates |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Geotechnical report sufficiency unclear |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Cold storage siting parameters incomplete |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurements consistently referenced to TPN46 |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Waskasoo Ave road access permit requirements |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequately provided across docs |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Documents provide comprehensive information coverage |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Information messaging is coherent across docs |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding well established |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise requirements stated |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Adequate for deliverable scope |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding coherent across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Adequately addressed through trade-offs |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment guidance adequate |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view provided in Guidance |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning consistent across docs |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add parcel boundary coordinates or reference datum for site plan base map (UTM or local grid coordinates from TPN46 C-1) | The Datasheet provides legal description and acreage but no coordinate reference datum. The civil engineer needs a coordinate system to produce the site plan. TPN46 C-1 has this but it is not recorded as a parameter. | Datasheet.md | Site Identity table | -- | TPN46 C-1 sheet or civil survey files | TBD |
| B-002 | B:data:sufficiency | WeakStatement | Datasheet | Datasheet | Clarify geotechnical report scope and confirm whether it covers the full developable area or only the proposed building pad area | Datasheet references the Geotechnical Investigation Report but states DB is "responsible for determining sufficiency." The report's geographic coverage within the parcel is not recorded as a data attribute. | Datasheet.md | Circulation & Parking - Geotechnical reference row | -- | Geotechnical Investigation Report (Appendix D) | TBD |
| B-003 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add cold storage building siting parameters (setback from main building, access requirements, orientation constraints) as explicit data attributes | Datasheet does not include any attributes specific to the cold storage building (60x100 ft) siting, though it is part of the site plan scope. Procedure Step 2.3 references it but no data parameters exist. | Datasheet.md | entire document scanned | -- | PKG-004 DEL-04-01 | TBD |
| B-004 | B:information:necessity | TBD_Question | Multi | Specification | Record TBD: Determine whether a road access permit or approach agreement with the County or Province is required for the Waskasoo Avenue (RR280) access point | Waskasoo Avenue is identified as RR280 (Range Road 280), which may be under provincial or county jurisdiction. Access road connection to a range road may require an approach permit. No document addresses this regulatory signal. | Specification.md; Guidance.md | REQ-03; Guidance Considerations - Access Road Design | -- | Alberta Transportation or Red Deer County | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Regulatory Imperative | 1 | HAS_ITEMS | Land Use Bylaw parking requirements unknown |
| C:normative:sufficiency | normative | sufficiency | Warranted Conformance | 0 | NO_ITEMS | Conformance pathways adequately described |
| C:normative:completeness | normative | completeness | Exhaustive Compliance Scope | 1 | HAS_ITEMS | Emergency access code requirements |
| C:normative:consistency | normative | consistency | Steadfast Regulatory Coherence | 0 | NO_ITEMS | Regulatory references consistent across docs |
| C:operative:necessity | operative | necessity | Operational Prerequisite | 0 | NO_ITEMS | Prerequisites well documented |
| C:operative:sufficiency | operative | sufficiency | Competent Practice | 0 | NO_ITEMS | Practice guidance adequate |
| C:operative:completeness | operative | completeness | Thorough Operational Coverage | 0 | NO_ITEMS | Operational steps thoroughly covered |
| C:operative:consistency | operative | consistency | Disciplined Operational Reliability | 0 | NO_ITEMS | Procedure is internally consistent |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Worth Criterion | 0 | NO_ITEMS | Value criteria adequately established |
| C:evaluative:sufficiency | evaluative | sufficiency | Defensible Merit Assessment | 1 | HAS_ITEMS | Defensibility of parking count assumption |
| C:evaluative:completeness | evaluative | completeness | Holistic Worth Account | 0 | NO_ITEMS | Holistic coverage adequate |
| C:evaluative:consistency | evaluative | consistency | Principled Value Coherence | 0 | NO_ITEMS | Value reasoning consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | TBD_Question | Multi | Specification | Record TBD: Obtain Town of Penhold Land Use Bylaw parking requirements for institutional/industrial use and record minimum stall count as a binding requirement | The regulatory imperative for parking count is unresolved. Specification REQ-11 and Guidance both note this as an ASSUMPTION. The Land Use Bylaw likely sets a mandatory minimum that has not been sourced. | Specification.md; Guidance.md; Procedure.md | REQ-11; Guidance Parking Count; Procedure Step 5 | -- | Town of Penhold Land Use Bylaw | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add fire access route requirements from Alberta Fire Code or applicable municipal fire bylaws (minimum road width, surface load capacity, turnaround dimensions, signage) | The exhaustive compliance scope lens reveals that fire access route design criteria beyond turning radii are absent. Alberta Fire Code typically specifies minimum 6m road width, signage, and fire lane markings for emergency access routes. Only turning radii are addressed. | Specification.md | REQ-03; REQ-04 | -- | Alberta Fire Code / National Fire Code of Canada | TBD |
| C-003 | C:evaluative:sufficiency | WeakStatement | Procedure | Procedure | Strengthen parking count calculation in Step 5 -- replace ASSUMPTION-based range (60-100 stalls) with a defensible methodology referencing occupancy calculations, shift patterns, and bylaw minimums | The parking count methodology in Procedure Step 5 uses an unsupported arithmetic assumption (FD personnel + PW personnel). A defensible merit assessment requires a methodology traceable to code or operational analysis. | Procedure.md | Steps - Phase A - Step 5 | -- | Procedure.md | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Authoritative Statutory Obligation | 1 | HAS_ITEMS | Professional seal timing unclear |
| F:normative:sufficiency | normative | sufficiency | Demonstrated Regulatory Adequacy | 0 | NO_ITEMS | Adequacy demonstration pathways clear |
| F:normative:completeness | normative | completeness | Comprehensive Obligation Mastery | 1 | HAS_ITEMS | Snow storage and winter operations |
| F:normative:consistency | normative | consistency | Unified Regulatory Integrity | 0 | NO_ITEMS | Regulatory references unified |
| F:operative:necessity | operative | necessity | Critical Process Foundation | 1 | HAS_ITEMS | Coordination protocol with PKG-002 |
| F:operative:sufficiency | operative | sufficiency | Calibrated Process Proficiency | 0 | NO_ITEMS | Process proficiency adequate |
| F:operative:completeness | operative | completeness | Exhaustive Process Mastery | 0 | NO_ITEMS | Process coverage thorough |
| F:operative:consistency | operative | consistency | Consistent Operational Discipline | 0 | NO_ITEMS | Operational steps consistent |
| F:evaluative:necessity | evaluative | necessity | Foundational Merit Basis | 0 | NO_ITEMS | Merit basis established |
| F:evaluative:sufficiency | evaluative | sufficiency | Calibrated Worth Justification | 1 | HAS_ITEMS | Future expansion quantification |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Value Mastery | 0 | NO_ITEMS | Value coverage adequate |
| F:evaluative:consistency | evaluative | consistency | Principled Appraisal Integrity | 0 | NO_ITEMS | Appraisal principles consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | Normalization | Multi | Specification | Clarify professional seal requirements across project phases -- Specification REQ-08 requires sealed drawings; Procedure Step 7 hedges with ASSUMPTION about proposal-stage seal; reconcile into a clear phase-gate statement | The statutory obligation for Alberta-registered civil engineer seal is stated in Specification but the Procedure introduces uncertainty about when the seal is required. This inconsistency could affect compliance. | Specification.md; Procedure.md | REQ-08; Procedure Step 7.1 | -- | Specification.md (REQ-08) | TBD |
| F-002 | F:normative:completeness | MissingSlot | Datasheet | Datasheet | Add snow storage and winter operations considerations as site attributes -- snow storage areas, winter access maintenance zones, and de-icing constraints for the site plan | The comprehensive obligation mastery lens reveals no mention of snow storage areas or winter operations in any document, despite this being a northern Alberta site where winter site operations are a significant design driver. | Datasheet.md | entire document scanned | -- | Municipal winter operations standards; Owner operational requirements | TBD |
| F-003 | F:operative:necessity | VerificationGap | Procedure | Procedure | Add explicit coordination checkpoint with PKG-002 architectural team -- define when building footprint dimensions must be confirmed and by whom before site plan can be finalized | Procedure Step 2 references coordination with PKG-002 but does not specify a formal coordination checkpoint, information exchange format, or hold point. This is a critical process foundation gap. | Procedure.md | Steps - Phase A - Step 2 | -- | Procedure.md | TBD |
| F-004 | F:evaluative:sufficiency | WeakStatement | Specification | Guidance | Add quantified future expansion capacity targets -- specify what percentage of developable area should remain unoccupied or how much additional building area should be accommodable | REQ-13 requires future expansion consideration but provides no quantified targets. The calibrated worth justification lens asks whether the requirement is specific enough to evaluate compliance. "Minimize cost and disruption" is not measurable. | Specification.md | REQ-13: Future Expansion Consideration | -- | Guidance.md | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Resolved Prescriptive Authority | 1 | HAS_ITEMS | TPN46 prescriptive status unresolved |
| D:normative:applying | normative | applying | Enforced Obligation Fulfillment | 0 | NO_ITEMS | Obligation fulfillment pathways clear |
| D:normative:judging | normative | judging | Conclusive Compliance Verdict | 0 | NO_ITEMS | Compliance determination methods adequate |
| D:normative:reviewing | normative | reviewing | Resolved Regulatory Oversight | 0 | NO_ITEMS | Oversight pathway described |
| D:operative:guiding | operative | guiding | Grounded Procedural Direction | 0 | NO_ITEMS | Procedural direction grounded |
| D:operative:applying | operative | applying | Calibrated Practical Delivery | 1 | HAS_ITEMS | Design software/tools not specified |
| D:operative:judging | operative | judging | Conclusive Performance Judgment | 0 | NO_ITEMS | Performance judgment criteria adequate |
| D:operative:reviewing | operative | reviewing | Resolved Process Assurance | 0 | NO_ITEMS | Process assurance adequate |
| D:evaluative:guiding | evaluative | guiding | Grounded Value Direction | 0 | NO_ITEMS | Value direction established |
| D:evaluative:applying | evaluative | applying | Calibrated Merit Application | 1 | HAS_ITEMS | Cross-deliverable coordination value |
| D:evaluative:judging | evaluative | judging | Conclusive Worth Determination | 0 | NO_ITEMS | Worth determination adequate |
| D:evaluative:reviewing | evaluative | reviewing | Resolved Quality Assurance | 0 | NO_ITEMS | QA pathway adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:guiding | Conflict | Guidance | Guidance | Resolve CON-01 (TPN46 prescriptive status) -- Guidance identifies the conflict but human ruling is TBD; the Resolved Prescriptive Authority lens confirms this is a blocking ambiguity for design direction | CON-01 in Guidance identifies that TPN46 may be prescriptive or indicative. Specification REQ-02 treats it as prescriptive ("shall follow the footprint defined"). Addendum 03 Section 1.20 implies post-award refinement is expected. These are in tension. | Guidance.md; Specification.md | Guidance CON-01; Specification REQ-02 | Specification.md#REQ-02 ("shall follow the footprint defined"); Guidance.md#CON-01 (proposed resolution treats as prescriptive for zone/area, exact coordinates refinable) | Specification.md (REQ-02) | TBD |
| D-002 | D:operative:applying | RationaleGap | Procedure | Guidance | Add guidance on recommended design software/tools for swept-path analysis and site plan production (e.g., AutoTURN, Vehicle Tracking, AutoCAD Civil 3D) to support calibrated practical delivery | Procedure Step 4 references "swept-path analysis (using software or manual overlay)" and Procedure Prerequisites mention "ASSUMPTION: Swept-path analysis software or overlay templates" but no specific tool recommendation or minimum capability is provided. | Procedure.md | Steps Phase A Step 4; Prerequisites | -- | Guidance.md | TBD |
| D-003 | D:evaluative:applying | Normalization | Multi | Guidance | Standardize cross-deliverable coordination references -- use consistent format for referencing DEL-03-02, DEL-03-03, DEL-03-04, DEL-03-05 interface points across all four documents | Documents reference sibling deliverables (DEL-03-02 through DEL-03-05) inconsistently: Specification uses "covered by DEL-03-XX" in exclusions but "coordination with DEL-03-XX" in verification; Procedure uses "DEL-03-02 interface" notation. A consistent cross-reference convention would reduce drift. | Specification.md; Procedure.md; Guidance.md | Specification Scope/Verification; Procedure Steps; Guidance throughout | -- | Guidance.md | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Directive Imperative | 0 | NO_ITEMS | Foundational directives adequately established |
| X:guiding:sufficiency | guiding | sufficiency | Warranted Directive Competence | 1 | HAS_ITEMS | Design review competence criteria |
| X:guiding:completeness | guiding | completeness | Comprehensive Directive Scope | 0 | NO_ITEMS | Directive scope comprehensive |
| X:guiding:consistency | guiding | consistency | Steadfast Directive Coherence | 0 | NO_ITEMS | Directives coherent |
| X:applying:necessity | applying | necessity | Essential Calibrated Enforcement | 1 | HAS_ITEMS | Verification stage definitions |
| X:applying:sufficiency | applying | sufficiency | Warranted Implementation Proficiency | 0 | NO_ITEMS | Implementation guidance sufficient |
| X:applying:completeness | applying | completeness | Exhaustive Implementation Coverage | 1 | HAS_ITEMS | Missing cold storage verification |
| X:applying:consistency | applying | consistency | Dependable Implementation Stability | 0 | NO_ITEMS | Implementation approach stable |
| X:judging:necessity | judging | necessity | Binding Adjudicative Finding | 0 | NO_ITEMS | Adjudicative criteria adequate |
| X:judging:sufficiency | judging | sufficiency | Warranted Adjudicative Sufficiency | 0 | NO_ITEMS | Sufficiency criteria met |
| X:judging:completeness | judging | completeness | Exhaustive Adjudicative Completeness | 0 | NO_ITEMS | Adjudication coverage complete |
| X:judging:consistency | judging | consistency | Principled Adjudicative Consistency | 0 | NO_ITEMS | Adjudicative consistency maintained |
| X:reviewing:necessity | reviewing | necessity | Essential Assurance Foundation | 1 | HAS_ITEMS | Peer review process undefined |
| X:reviewing:sufficiency | reviewing | sufficiency | Warranted Assurance Adequacy | 0 | NO_ITEMS | Assurance mechanisms adequate |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Assurance Completeness | 0 | NO_ITEMS | Assurance coverage adequate |
| X:reviewing:consistency | reviewing | consistency | Principled Assurance Integrity | 0 | NO_ITEMS | Assurance integrity maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | VerificationGap | Specification | Specification | Add qualification requirements for design reviewers in the Verification table -- specify that "Design review" must be performed by Alberta-registered civil engineer or equivalent qualified professional | The Verification table lists "Design review" as the method for most requirements but does not specify the competence or qualification of the reviewer. For warranted directive competence, the reviewer's qualifications should be explicit. | Specification.md | Verification table | -- | Specification.md | TBD |
| X-002 | X:applying:necessity | VerificationGap | Specification | Specification | Define verification stage timing more precisely -- distinguish between "proposal design review" and "IFC design review" stages; several requirements need verification at both stages | The Verification table uses "Design review" and "Proposal submission" as stages but does not clearly define when each verification occurs in the project lifecycle. Calibrated enforcement requires precise stage definitions. | Specification.md | Verification table | -- | Specification.md | TBD |
| X-003 | X:applying:completeness | VerificationGap | Specification | Specification | Add verification item for cold storage building site integration -- confirm cold storage footprint location, access route, surface treatment, and turning access are verified in the site plan | The Verification table has no specific check for the cold storage building (60x100 ft) integration into the site plan, though the Scope and Procedure reference it. Exhaustive implementation coverage requires this. | Specification.md | Verification table | -- | Specification.md | TBD |
| X-004 | X:reviewing:necessity | VerificationGap | Procedure | Procedure | Add internal peer review checkpoint before proposal submission -- specify that site plan package undergoes civil engineering peer review before assembly into Design Brief | Procedure Step 7 describes assembly but no internal peer review or QA check is prescribed before the deliverable package is submitted. Essential assurance foundation requires a review gate. | Procedure.md | Steps Phase A Step 7 | -- | Procedure.md | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Definitive Regulatory Foundation | 0 | NO_ITEMS | Regulatory foundation established |
| E:normative:sufficiency | normative | sufficiency | Demonstrated Prescriptive Sufficiency | 0 | NO_ITEMS | Prescriptive sufficiency demonstrated |
| E:normative:completeness | normative | completeness | Exhaustive Regulatory Fulfillment | 1 | HAS_ITEMS | Stormwater interface for site plan |
| E:normative:consistency | normative | consistency | Integral Regulatory Steadfastness | 0 | NO_ITEMS | Regulatory consistency maintained |
| E:operative:necessity | operative | necessity | Resolved Operational Imperative | 0 | NO_ITEMS | Operational imperatives resolved |
| E:operative:sufficiency | operative | sufficiency | Demonstrated Operational Adequacy | 0 | NO_ITEMS | Operational adequacy demonstrated |
| E:operative:completeness | operative | completeness | Holistic Operational Fulfillment | 0 | NO_ITEMS | Operational coverage holistic |
| E:operative:consistency | operative | consistency | Disciplined Operational Integrity | 0 | NO_ITEMS | Operational integrity maintained |
| E:evaluative:necessity | evaluative | necessity | Resolved Intrinsic Worth Imperative | 1 | HAS_ITEMS | Dust and environmental impact |
| E:evaluative:sufficiency | evaluative | sufficiency | Demonstrated Worth Sufficiency | 0 | NO_ITEMS | Worth sufficiency demonstrated |
| E:evaluative:completeness | evaluative | completeness | Holistic Value Realization | 0 | NO_ITEMS | Value realization adequate |
| E:evaluative:consistency | evaluative | consistency | Principled Value Integrity | 0 | NO_ITEMS | Value integrity maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:completeness | Normalization | Specification | Specification | Clarify the interface boundary between DEL-03-01 site plan surface drainage (positive drainage shown on site plan) and DEL-03-02 stormwater management -- both documents claim responsibility for drainage direction | REQ-09 requires positive drainage coordination with DEL-03-02, but the Specification exclusions state drainage is "covered by DEL-03-02." The overlap/interface boundary for who shows what on which drawing is not precisely defined, risking either gap or duplication. | Specification.md | REQ-09; Scope - What This Deliverable Excludes | -- | Specification.md | TBD |
| E-002 | E:evaluative:necessity | RationaleGap | Guidance | Guidance | Add consideration of dust and environmental impact from aggregate yard areas on adjacent properties and operations -- this affects the intrinsic worth assessment of aggregate vs. paved surfaces | Guidance Trade-off 1 addresses aggregate vs. asphalt cost but does not discuss dust generation, environmental runoff, or impact on adjacent properties (residential areas, dog park) from extensive aggregate surfacing. This is a resolved intrinsic worth imperative gap. | Guidance.md | Trade-offs - Trade-off 1 | -- | Guidance.md | TBD |
