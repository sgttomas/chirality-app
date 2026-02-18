# Semantic Lensing Register: DEL-02-03 Public Works Shop Bays, Workshop & Support Spaces

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/PKG-002_Main Public Services Building (PSB)/1_Working/DEL-02-03_Public Works Shop Bays, Workshop & Support Spaces/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-02-03_Public Works Shop Bays, Workshop & Support Spaces/_CONTEXT.md
- _STATUS.md -- DEL-02-03_Public Works Shop Bays, Workshop & Support Spaces/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md -- DEL-02-03_Public Works Shop Bays, Workshop & Support Spaces/_SEMANTIC.md
- Datasheet.md -- DEL-02-03_Public Works Shop Bays, Workshop & Support Spaces/Datasheet.md
- Specification.md -- DEL-02-03_Public Works Shop Bays, Workshop & Support Spaces/Specification.md
- Guidance.md -- DEL-02-03_Public Works Shop Bays, Workshop & Support Spaces/Guidance.md
- Procedure.md -- DEL-02-03_Public Works Shop Bays, Workshop & Support Spaces/Procedure.md
- _REFERENCES.md -- DEL-02-03_Public Works Shop Bays, Workshop & Support Spaces/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 21
- By document:
  - Datasheet: 4
  - Specification: 7
  - Guidance: 3
  - Procedure: 3
  - Multi: 4
- By matrix:
  - A: 4  B: 3  C: 3  F: 3  D: 2  X: 4  E: 2
- By type:
  - Conflict: 0
  - VerificationGap: 6
  - MissingSlot: 6
  - WeakStatement: 3
  - RationaleGap: 2
  - Normalization: 2
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Locker expansion guidance lacks prescriptive threshold |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Sump count per bay unspecified |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | ABC fixture count verification missing |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit trail adequately covered in Procedure |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Steps are well-sequenced in Procedure |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Execution steps are clear |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | No quantified performance criteria for ventilation adequacy |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Process audit steps present in Procedure |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance P1-P7 provides strong value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Merit application addressed through workflow principles |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Trade-offs T1-T3 cover worth determination |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality appraisal covered via verification tables |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Guidance | Specification | Add a prescriptive expansion trigger or threshold for locker room growth from 40 to 50 lockers (e.g., occupancy percentage or staffing milestone that triggers expansion) | Guidance P5 states locker room should be expandable to 50 but no prescriptive trigger or dimensional requirement for the expansion zone is specified in Specification | Guidance.md | P5: The Locker Room Must Be Sized for 40 Now and Expandable to 50 | -- | Specification should carry expansion requirement | TBD |
| A-002 | A:normative:applying | TBD_Question | Specification | Specification | Record TBD: Confirm minimum number of sumps per bay (one or more) and whether each bay requires an oil/water separator or simple floor drain | REQ-2303-05 states sumps in all bays but does not specify quantity per bay or separator type; Addendum 03 section 1.8 says required but leaves count to design | Specification.md | REQ-2303-05: Bay Sumps | -- | Owner/DEL-02-05 Mech lead to confirm | TBD |
| A-003 | A:normative:judging | VerificationGap | Multi | Specification | Add acceptance criteria for ABC plumbing fixture count compliance for PW locker room, washrooms, and shop washroom (fixture count calculation against occupant load) | Guidance C4 flags fixture count compliance with ABC but neither Specification nor Procedure includes a verification check with quantified fixture counts | Specification.md; Procedure.md | REQ-2303-12; REQ-2303-15; Procedure Verification table | -- | ABC fixture schedule per occupancy | TBD |
| A-004 | A:operative:judging | WeakStatement | Procedure | Procedure | Clarify what constitutes "adequate" ventilation in the Procedure verification check for PW ventilation (e.g., air changes per hour target, CO concentration threshold, or reference to DEL-02-05 design criteria) | Procedure Verification table says "Ventilation system adequate for idling/occasional welding; confirmed by Mech lead" but provides no measurable acceptance criterion | Procedure.md | Verification table -- PW ventilation row | -- | DEL-02-05 mechanical design criteria | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Bay door width not explicitly stated |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Evidence chain from sources is adequate |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Missing equipment storage assignment table |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurements are consistently sourced |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Essential signals present across docs |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Contextual information sufficient |
| B:information:completeness | information | completeness | comprehensive account | 1 | HAS_ITEMS | Workshop half-and-half split not dimensioned |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messaging coherent across docs |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding evident in Guidance |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise requirements clear |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Coverage thorough for proposal stage |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding consistent |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-off discernment present in Guidance |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment adequately represented |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic perspective in Guidance principles |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Principled reasoning consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add overhead door clear width dimension (currently only 16 ft height is stated; door is noted as 16' x 16' in Spec but width is not in Datasheet attributes table as a separate attribute) | Datasheet records overhead door clear height (16 ft) and size (16' x 16') but does not explicitly record the clear opening width as a separate attribute; for equipment maneuvering validation the width is an essential datum | Datasheet.md | Shop Bay Configuration table | -- | Functional Program Equipment List / OSR | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add a vehicle-to-bay assignment table mapping each piece of PW equipment to its designated bay or storage location | Datasheet lists key equipment dimensions but does not record which vehicles are assigned to which bays; this assignment drives layout decisions and is referenced in Guidance P1 and Procedure Step 1 | Datasheet.md | Key Equipment Driving Bay Sizing table | -- | Design-Builder fleet assignment | TBD |
| B-003 | B:information:completeness | WeakStatement | Guidance | Guidance | Clarify the workshop area split ratio: provide approximate minimum dimensions or area split (e.g., minimum welding zone area, minimum storage zone area) rather than only stating "half and half" | Guidance C5 describes the workspace bay as "half welding/maintenance, half parts storage" but provides no dimensional guidance for what half means in practice; this ambiguity could lead to undersized welding clearances | Guidance.md | C5: Workshop Area Split Function | -- | Functional Program Row 28.0 / Owner | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Binding Compliance Imperative | 0 | NO_ITEMS | Binding requirements well-articulated |
| C:normative:sufficiency | normative | sufficiency | Substantiated Conformance | 1 | HAS_ITEMS | Accessibility compliance needs substantiation |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Coverage | 1 | HAS_ITEMS | Fire separation not addressed |
| C:normative:consistency | normative | consistency | Harmonized Regulatory Integrity | 0 | NO_ITEMS | Regulatory references consistent |
| C:operative:necessity | operative | necessity | Functional Prerequisite Threshold | 0 | NO_ITEMS | Functional prerequisites identified |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Operational Competence | 0 | NO_ITEMS | Operational competence requirements clear |
| C:operative:completeness | operative | completeness | Thorough Operational Coverage | 1 | HAS_ITEMS | Fueling/fluid handling not addressed |
| C:operative:consistency | operative | consistency | Systematic Process Reliability | 0 | NO_ITEMS | Process reliability adequately systematic |
| C:evaluative:necessity | evaluative | necessity | Foundational Merit Basis | 0 | NO_ITEMS | Merit basis established through principles |
| C:evaluative:sufficiency | evaluative | sufficiency | Defensible Quality Appraisal | 0 | NO_ITEMS | Quality appraisal defensible |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Worth Assessment | 0 | NO_ITEMS | Worth assessment comprehensive for scope |
| C:evaluative:consistency | evaluative | consistency | Principled Value Coherence | 0 | NO_ITEMS | Value coherence maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:sufficiency | VerificationGap | Specification | Specification | Add specific ABC accessibility requirements applicable to PW support spaces (e.g., accessible washroom stall dimensions, accessible path width through locker room, barrier-free shower requirement) | REQ-2303-17 states "shall meet Alberta Building Code accessibility requirements" but does not identify which specific accessibility provisions apply; verification is listed as "ABC compliance review by Architect" without measurable criteria | Specification.md | REQ-2303-17: Accessibility; Verification table | -- | ABC Part 3 barrier-free provisions | TBD |
| C-002 | C:normative:completeness | MissingSlot | Multi | Specification | Add requirement or note addressing fire separation between PW shop bays and PW support spaces (locker room, office) if required by ABC occupancy classification | No document addresses fire separation requirements between the shop bay volume (likely Group F, Division 3) and the PW support/office spaces; this is a regulatory requirement that affects layout | Specification.md; Guidance.md | entire document scanned | -- | ABC Part 3 occupancy separation | TBD |
| C-003 | C:operative:completeness | MissingSlot | Multi | Guidance | Add consideration addressing whether PW bays require vehicle fluid containment provisions (e.g., secondary containment for oil drip, fuel spill response provision) beyond snow-melt sumps | Sumps address snow melt and minor washing but no document addresses fluid containment for maintenance activities (oil changes, hydraulic fluid) which are part of the shop bay operational function | Specification.md; Guidance.md; Procedure.md | entire document scanned | -- | Environmental regulations / AHJ | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandated Conformance Foundation | 0 | NO_ITEMS | Mandated conformance foundation established |
| F:normative:sufficiency | normative | sufficiency | Adequate Compliance Demonstration | 1 | HAS_ITEMS | Floor finish for support spaces underspecified |
| F:normative:completeness | normative | completeness | Exhaustive Compliance Mastery | 0 | NO_ITEMS | Compliance coverage adequate for scope |
| F:normative:consistency | normative | consistency | Coherent Compliance Discipline | 0 | NO_ITEMS | Compliance discipline coherent |
| F:operative:necessity | operative | necessity | Critical Operational Prerequisite | 1 | HAS_ITEMS | Compressed air source not identified |
| F:operative:sufficiency | operative | sufficiency | Proven Operational Readiness | 0 | NO_ITEMS | Operational readiness sufficiently addressed |
| F:operative:completeness | operative | completeness | Exhaustive Operational Mastery | 0 | NO_ITEMS | Operational coverage adequate |
| F:operative:consistency | operative | consistency | Disciplined Operational Consistency | 0 | NO_ITEMS | Consistency maintained |
| F:evaluative:necessity | evaluative | necessity | Intrinsic Quality Foundation | 0 | NO_ITEMS | Quality foundations present |
| F:evaluative:sufficiency | evaluative | sufficiency | Substantiated Quality Basis | 0 | NO_ITEMS | Quality basis substantiated |
| F:evaluative:completeness | evaluative | completeness | Holistic Quality Mastery | 1 | HAS_ITEMS | Acoustic treatment not addressed |
| F:evaluative:consistency | evaluative | consistency | Principled Quality Consistency | 0 | NO_ITEMS | Quality consistency adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | Normalization | Datasheet | Multi | Normalize floor finish terminology: Datasheet says "Resilient material, easily cleaned (sealed concrete acceptable/desired)" for support spaces while Specification REQ-2303-08 only addresses bay floors; clarify whether support space floors are also sealed concrete or a different finish | Datasheet "Interior flooring -- support spaces" uses "resilient material" language while Guidance P6 says sealed concrete is "the required and preferred floor finish" for bay and shop areas; the scope of P6 relative to support spaces (locker room, office) is ambiguous | Datasheet.md; Guidance.md | Datasheet: Construction > Materials and Finishes; Guidance: P6 | -- | Owner preference / OSR section 10.3.8 | TBD |
| F-002 | F:operative:necessity | TBD_Question | Specification | Specification | Record TBD: Identify source of compressed air (dedicated compressor in shop area, or building-wide system) and confirm whether compressor sizing and location are within DEL-02-03 scope or DEL-02-05 | REQ-2303-09 requires hard-plumbed air lines but no document identifies the compressed air source equipment (compressor) or its sizing; this is a critical operational prerequisite for the air distribution system | Specification.md; Procedure.md | REQ-2303-09: Air Lines in Bays; Procedure Step 4 | -- | DEL-02-05 Mech lead / Owner | TBD |
| F-003 | F:evaluative:completeness | MissingSlot | Guidance | Guidance | Add consideration for acoustic separation between shop bays (high noise) and PW support spaces (office, locker room) including whether wall STC rating or acoustic treatment is warranted | No document addresses noise transmission from shop bay operations (vehicle idling, pneumatic tools, welding) to adjacent support spaces; this affects occupant comfort and could affect ABC compliance for office occupancy | Guidance.md | entire document scanned | -- | ABC noise/occupancy requirements | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Resolved Prescriptive Authority | 0 | NO_ITEMS | Prescriptive authority well-resolved through source citations |
| D:normative:applying | normative | applying | Confirmed Obligatory Practice | 0 | NO_ITEMS | Obligatory practices confirmed |
| D:normative:judging | normative | judging | Definitive Conformance Ruling | 0 | NO_ITEMS | Conformance rulings clear |
| D:normative:reviewing | normative | reviewing | Resolved Regulatory Oversight | 0 | NO_ITEMS | Regulatory oversight addressed |
| D:operative:guiding | operative | guiding | Resolved Procedural Foundation | 1 | HAS_ITEMS | Wash bay contingency procedure missing |
| D:operative:applying | operative | applying | Confirmed Execution Capability | 0 | NO_ITEMS | Execution capability confirmed |
| D:operative:judging | operative | judging | Resolved Performance Verdict | 0 | NO_ITEMS | Performance verdicts adequately addressed |
| D:operative:reviewing | operative | reviewing | Resolved Process Governance | 0 | NO_ITEMS | Process governance resolved |
| D:evaluative:guiding | evaluative | guiding | Resolved Value Commitment | 1 | HAS_ITEMS | 50-year lifecycle value not connected to material choices |
| D:evaluative:applying | evaluative | applying | Confirmed Merit Delivery | 0 | NO_ITEMS | Merit delivery confirmed |
| D:evaluative:judging | evaluative | judging | Definitive Worth Judgment | 0 | NO_ITEMS | Worth judgment adequately addressed |
| D:evaluative:reviewing | evaluative | reviewing | Resolved Quality Governance | 0 | NO_ITEMS | Quality governance resolved |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:operative:guiding | MissingSlot | Procedure | Procedure | Add a procedural step or decision gate addressing the wash bay option contingency: if Owner selects SOW-0500, describe the design modification path for converting bay 4 to wash bay (layout adjustments, plumbing rough-in, coordination with DEL-05-01) | Guidance C1 and Specification REQ-2303-01 note the wash bay option may replace a PW bay, but Procedure contains no step or decision gate for handling this contingency during design development | Procedure.md | Phase B steps (Steps 8-13) | -- | PM / Owner decision | TBD |
| D-002 | D:evaluative:guiding | RationaleGap | Guidance | Guidance | Add rationale connecting 50-year building life requirement to specific material/finish selection guidance for PW shop areas (e.g., why sealed concrete is appropriate for 50-year durability, what maintenance cycle is assumed) | Guidance P6 states sealed concrete is required but does not connect this to the 50-year design life rationale from OSR section 10.2; REQ-2303-18 references durability but Guidance lacks the interpretive bridge | Guidance.md | P6: Sealed Concrete Is the Required and Preferred Floor Finish | -- | OSR section 10.2 / 11.3 | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Directive Anchor | 0 | NO_ITEMS | Foundational directives anchored |
| X:guiding:sufficiency | guiding | sufficiency | Validated Directive Adequacy | 0 | NO_ITEMS | Directive adequacy validated |
| X:guiding:completeness | guiding | completeness | Exhaustive Directive Scope | 1 | HAS_ITEMS | Verification for locker expansion path missing |
| X:guiding:consistency | guiding | consistency | Coherent Directive Stewardship | 0 | NO_ITEMS | Directive stewardship coherent |
| X:applying:necessity | applying | necessity | Essential Implementation Readiness | 1 | HAS_ITEMS | No verification for equipment maneuvering simulation |
| X:applying:sufficiency | applying | sufficiency | Proven Implementation Adequacy | 0 | NO_ITEMS | Implementation adequacy proven |
| X:applying:completeness | applying | completeness | Comprehensive Implementation Breadth | 0 | NO_ITEMS | Implementation breadth comprehensive |
| X:applying:consistency | applying | consistency | Stable Implementation Integrity | 0 | NO_ITEMS | Implementation integrity stable |
| X:judging:necessity | judging | necessity | Critical Adjudication Finding | 1 | HAS_ITEMS | Structural clear height verification lacks explicit pass/fail |
| X:judging:sufficiency | judging | sufficiency | Justified Adjudication Basis | 0 | NO_ITEMS | Adjudication basis justified |
| X:judging:completeness | judging | completeness | Exhaustive Adjudication Scope | 0 | NO_ITEMS | Adjudication scope adequate |
| X:judging:consistency | judging | consistency | Principled Adjudication Integrity | 0 | NO_ITEMS | Adjudication integrity maintained |
| X:reviewing:necessity | reviewing | necessity | Critical Governance Oversight | 1 | HAS_ITEMS | Owner walkthrough scope underspecified |
| X:reviewing:sufficiency | reviewing | sufficiency | Validated Oversight Adequacy | 0 | NO_ITEMS | Oversight adequacy validated |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Oversight Breadth | 0 | NO_ITEMS | Oversight breadth adequate |
| X:reviewing:consistency | reviewing | consistency | Principled Oversight Integrity | 0 | NO_ITEMS | Oversight integrity maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | VerificationGap | Specification | Specification | Add verification method for locker room expansion feasibility to 50 lockers (e.g., layout review confirming expansion zone identified, or narrative confirming structural/spatial capacity for 10 additional lockers) | Guidance P5 requires expandability to 50 but no verification method exists in Specification or Procedure to confirm the expansion path is feasible | Specification.md | Verification table | -- | Guidance P5 / OBJ-007 | TBD |
| X-002 | X:applying:necessity | VerificationGap | Specification | Specification | Add verification method requiring equipment maneuvering template overlay (turning radius check for grader in bay) as a formal design review artifact, not just narrative confirmation | Specification verification for REQ-2303-02 says "Design review with equipment templates" but does not require a formal maneuvering template as a deliverable artifact; this is the primary sizing validation method | Specification.md | Verification table -- REQ-2303-02 | -- | Architect / equipment templates | TBD |
| X-003 | X:judging:necessity | VerificationGap | Procedure | Procedure | Specify minimum structural clear height acceptance criterion in the Procedure verification table (e.g., clear height >= 22 ft or >= tallest equipment operational height + safety margin) instead of the current qualitative "clear height >= tallest operational equipment height" | Procedure Verification table says "Clear height >= tallest operational equipment height; confirmed by Structural lead" but does not specify a numeric value or safety margin; CONF-2303-01 in Guidance identifies 22-24 ft as the assumed range but this is not in the acceptance criterion | Procedure.md | Verification table -- Structural clear height row | -- | CONF-2303-01 / Structural lead | TBD |
| X-004 | X:reviewing:necessity | RationaleGap | Procedure | Procedure | Clarify Owner walkthrough scope and acceptance criteria in the Procedure Records table (e.g., what constitutes "operational readiness" sign-off, which specific items the Owner inspects during the walkthrough) | Procedure Step 13 includes "Walk through locker room, PPE room, office, and washroom with Owner to confirm operational readiness" and Records table lists "Owner walkthrough sign-off record" but acceptance criteria for the walkthrough are not specified | Procedure.md | Step 13; Records table | -- | PM / Owner requirements | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Binding Foundational Obligation | 0 | NO_ITEMS | Binding obligations well-established |
| E:normative:sufficiency | normative | sufficiency | Validated Compliance Sufficiency | 1 | HAS_ITEMS | Standards table lacks specific section references |
| E:normative:completeness | normative | completeness | Exhaustive Regulatory Completeness | 0 | NO_ITEMS | Regulatory completeness adequate for scope |
| E:normative:consistency | normative | consistency | Principled Regulatory Coherence | 0 | NO_ITEMS | Regulatory coherence maintained |
| E:operative:necessity | operative | necessity | Essential Operational Foundation | 0 | NO_ITEMS | Operational foundation essential elements present |
| E:operative:sufficiency | operative | sufficiency | Demonstrated Operational Adequacy | 0 | NO_ITEMS | Operational adequacy demonstrated |
| E:operative:completeness | operative | completeness | Comprehensive Operational Breadth | 1 | HAS_ITEMS | Post-award coordination trigger missing |
| E:operative:consistency | operative | consistency | Disciplined Operational Integrity | 0 | NO_ITEMS | Operational integrity disciplined |
| E:evaluative:necessity | evaluative | necessity | Fundamental Quality Imperative | 0 | NO_ITEMS | Quality imperatives established |
| E:evaluative:sufficiency | evaluative | sufficiency | Demonstrated Value Sufficiency | 0 | NO_ITEMS | Value sufficiency demonstrated |
| E:evaluative:completeness | evaluative | completeness | Holistic Quality Completeness | 0 | NO_ITEMS | Quality completeness adequate |
| E:evaluative:consistency | evaluative | consistency | Principled Value Integrity | 0 | NO_ITEMS | Value integrity maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:sufficiency | Normalization | Specification | Specification | Normalize Standards table entries: replace "ASSUMPTION: likely applicable (location TBD in ABC)" with specific ABC part/section references where known, or explicitly mark as TBD requiring confirmation during design development | Specification Standards table uses "ASSUMPTION: likely applicable (location TBD in ABC)" for Alberta Building Code, NBC, and IES; this weakens compliance sufficiency validation and creates ambiguity about which code provisions govern | Specification.md | Standards table | -- | AHJ / Code consultant | TBD |
| E-002 | E:operative:completeness | VerificationGap | Procedure | Procedure | Add a coordination verification checkpoint at the start of Phase B (post-award) confirming that all DEL-02-xx interface commitments from Step 6 are still valid after contract award, and that scope selections (wash bay option) have been confirmed | Procedure Phase B jumps from proposal artifacts to post-award design without a formal checkpoint confirming proposal-stage coordination outcomes and Owner scope selections are still valid | Procedure.md | Phase B (between Step 7 and Step 8) | -- | PM / Architect | TBD |
