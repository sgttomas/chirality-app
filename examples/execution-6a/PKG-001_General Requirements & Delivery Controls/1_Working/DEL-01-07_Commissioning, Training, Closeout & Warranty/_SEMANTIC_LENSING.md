# Semantic Lensing Register: DEL-01-07 Commissioning, Training, Closeout & Warranty

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/PKG-001_General Requirements & Delivery Controls/1_Working/DEL-01-07_Commissioning, Training, Closeout & Warranty/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-01-07 identity, PKG-001, Closeout discipline, SOW-0013..SOW-0016/SOW-0113, OBJ-009
- _STATUS.md -- Current state: SEMANTIC_READY (2026-02-17)
- _SEMANTIC.md -- 7 matrices (A, B, C, F, D, X, E) parsed successfully; 92 total cells
- Datasheet.md -- Present; identification, artifacts, formats, deficiency process attributes, conditions, dependencies, references
- Specification.md -- Present; 16 requirements (REQ-01-07-001..016), standards, verification table
- Guidance.md -- Present; 6 principles, 6 considerations, 4 trade-offs, 4 open items
- Procedure.md -- Present; Part A (8 proposal steps), Part B (13 execution steps), verification, records
- _REFERENCES.md -- Present; RFP 2024_004 (sections 7.3.6, 7.3.7, 7.4, 7.5, 7.6)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 2
  - Specification: 15
  - Guidance: 3
  - Procedure: 6
  - Multi: 2
- By matrix:
  - A: 5  B: 5  C: 3  F: 4  D: 3  X: 5  E: 3
- By type:
  - Conflict: 0
  - VerificationGap: 8
  - MissingSlot: 8
  - WeakStatement: 5
  - RationaleGap: 3
  - Normalization: 1
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Standards table has assumption-flagged entries lacking confirmed applicability |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | OSR abbreviation unresolved across documents |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | CCDC 14-2013 text not reviewed; impacts Substantial Performance definition |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | No acceptance criteria for REQ-01-07-007 regulatory approvals beyond occupancy permit |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure covers both proposal and execution phases adequately |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Commissioning report format undefined |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification tables present in both Specification and Procedure |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Process audit covered by verification checks in Procedure |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance P1-P6 principles provide adequate value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs T1-T4 address merit application adequately |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Deficiency monetary value process covers worth determination |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality appraisal covered through commissioning and verification |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Confirm applicability and access status of CCDC 14-2013, Alberta Building Code, Alberta OH&S Act, and Land Titles Act (currently flagged as ASSUMPTION in Standards table) | Four of five standards entries are assumption-flagged with "likely applicable" and "location TBD"; prescriptive direction cannot be confirmed without verifying which standards actually govern | Specification.md | Standards | -- | Review contract documents and confirm standard applicability | TBD |
| A-002 | A:normative:applying | Normalization | Multi | Multi | Confirm and standardize the expansion of "OSR" across all documents; currently assumed to mean "Owner's Site Representative" | OSR is used in REQ-01-07-011, Procedure Steps B11/B13, and Guidance Example without confirmed definition; inconsistent or incorrect expansion risks misidentifying the approval authority | Specification.md, Procedure.md, Guidance.md | REQ-01-07-011, Step B11, Step B13, Deficiency Process Sequence example | -- | RFP Section 1 Definitions | TBD |
| A-003 | A:normative:judging | TBD_Question | Specification | Specification | Obtain and review CCDC 14-2013 supplementary conditions to confirm whether they modify Substantial Performance definition or retention rights beyond RFP defaults | Guidance OI-01-07-001 flags that CCDC 14-2013 may alter the compliance determination framework for Substantial Performance and deficiency retention; without this text, compliance cannot be fully determined | Specification.md, Guidance.md | Standards table, OI-01-07-001 | -- | CCDC 14-2013 supplementary conditions | TBD |
| A-004 | A:normative:reviewing | VerificationGap | Specification | Specification | Add specific verification criteria for REQ-01-07-007 (regulatory approvals) beyond "Confirm occupancy permit and required regulatory approvals obtained"; enumerate which regulatory approvals are expected (building code, fire code, environmental, others) | The verification approach for REQ-01-07-007 is generic ("regulatory approvals") without specifying which approvals are required; for a combined firehall/public works facility, fire code inspections are particularly intensive (per Guidance C3) and should be explicitly listed | Specification.md | Verification table, REQ-01-07-007 | -- | Specification.md | TBD |
| A-005 | A:operative:applying | WeakStatement | Multi | Datasheet | Define format requirements for commissioning reports and training materials; currently listed as "TBD format" in Datasheet Documentation table | Datasheet lists "TBD format; electronic" for commissioning reports and training materials; Procedure Step B4 says "Document commissioning results in commissioning reports" without specifying format; practical execution cannot be standardized without defined deliverable format | Datasheet.md, Procedure.md | Documentation table (Required Artifacts), Step B4 | -- | Owner to confirm format requirements | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Surveyor licensing requirement not explicitly stated |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Training documentation evidence requirements weak |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Record retention periods mostly TBD |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Deficiency monetary value assignment process is consistent |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key information signals (5 SP prerequisites, warranty trigger) well documented |
| B:information:sufficiency | information | sufficiency | adequate context | 1 | HAS_ITEMS | Scoring weight for commissioning narrative not known |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Coverage of systems, processes, and deliverables is comprehensive |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Documents are internally coherent on key messages |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Principles P1-P6 establish adequate foundational understanding |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 1 | HAS_ITEMS | Cx agent/coordinator qualifications not specified |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | System-by-system coverage addressed in Guidance C5 and Procedure |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs T1-T4 demonstrate adequate discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment on timing and sequencing is adequate |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance provides holistic perspective on handover readiness |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Specification | Specification | Add explicit requirement that legal/as-built survey must be performed by a licensed Alberta Land Surveyor (ALS) | REQ-01-07-008 requires a "certified survey" and Guidance P6 states "must be conducted by a licensed surveyor" but the Specification does not name the licensing standard; the essential fact of surveyor licensing is present only in Guidance, not in the normative requirement | Specification.md, Guidance.md | REQ-01-07-008, Guidance P6 | -- | Specification.md | TBD |
| B-002 | B:data:sufficiency | WeakStatement | Procedure | Procedure | Strengthen training documentation requirements in Procedure Step B5 to specify what constitutes adequate evidence of training completion (e.g., sign-off sheets, competency demonstrations, attendee evaluations) | Procedure Step B5 lists "sign-in records; training completion records" but does not define what constitutes sufficient evidence that training was effective, not merely attended; this affects REQ-01-07-003 verification | Procedure.md | Step B5 | -- | Procedure.md | TBD |
| B-003 | B:data:completeness | WeakStatement | Procedure | Procedure | Define specific retention periods for records currently listed as "TBD" in the Procedure Records table; at minimum, establish whether warranty-period records are retained for warranty + 1 year or longer | Procedure Records table lists 6 entries with "Duration of warranty period + TBD" and 1 with "TBD after warranty expiry"; comprehensive record-keeping requires defined retention periods, not placeholders | Procedure.md | Records table | -- | Owner records policy / contract | TBD |
| B-004 | B:information:sufficiency | TBD_Question | Guidance | Guidance | Obtain RFP Section 8.3 scoring matrix weight for commissioning/closeout criteria to calibrate proposal narrative detail level | Guidance C4 and OI-01-07-002 flag that the specific scoring weight for commissioning in the evaluation matrix (RFP Section 8.3) has not been reviewed; this information is essential context for determining how detailed the proposal commissioning narrative should be | Guidance.md | C4, OI-01-07-002 | -- | RFP Section 8.3 | TBD |
| B-005 | B:knowledge:sufficiency | MissingSlot | Specification | Specification | Add qualification requirements for the commissioning agent/Cx coordinator role referenced in Procedure Step A2 | Procedure Step A2 references "commissioning agent/Cx coordinator role and responsibilities" but neither the Specification nor Datasheet specify required qualifications or certifications for this role; competent expertise for commissioning requires defined qualifications | Specification.md, Procedure.md | entire document scanned (Specification), Step A2 (Procedure) | -- | Specification.md | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | enforceable obligation | 0 | NO_ITEMS | 16 requirements well-defined with RFP source tracing |
| C:normative:sufficiency | normative | sufficiency | certified justification | 1 | HAS_ITEMS | Verification for training lacks objective acceptance criteria |
| C:normative:completeness | normative | completeness | exhaustive compliance coverage | 1 | HAS_ITEMS | Structural as-built drawings not mentioned in Specification REQ-01-07-004 |
| C:normative:consistency | normative | consistency | codified regulatory standard | 0 | NO_ITEMS | Regulatory standards consistently referenced where applicable |
| C:operative:necessity | operative | necessity | operational prerequisite | 0 | NO_ITEMS | Prerequisites well-defined for both phases in Procedure |
| C:operative:sufficiency | operative | sufficiency | demonstrated capability | 0 | NO_ITEMS | Capability demonstration covered through verification checks |
| C:operative:completeness | operative | completeness | comprehensive operational scope | 1 | HAS_ITEMS | No procedure step for warranty claim response during warranty period |
| C:operative:consistency | operative | consistency | disciplined operational control | 0 | NO_ITEMS | Procedure steps are sequentially disciplined and cross-referenced |
| C:evaluative:necessity | evaluative | necessity | intrinsic value threshold | 0 | NO_ITEMS | Value thresholds adequately established through SP gate and warranty |
| C:evaluative:sufficiency | evaluative | sufficiency | warranted quality appraisal | 0 | NO_ITEMS | Quality appraisal addressed through commissioning verification |
| C:evaluative:completeness | evaluative | completeness | exhaustive value accounting | 0 | NO_ITEMS | Value accounting covered through deficiency monetary values and SP gate |
| C:evaluative:consistency | evaluative | consistency | principled value consistency | 0 | NO_ITEMS | Value principles consistent across Guidance and Specification |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:sufficiency | VerificationGap | Specification | Specification | Add objective acceptance criteria for REQ-01-07-003 (Owner Staff Training) that go beyond "Review of training records and training material documentation" -- specify what constitutes certified justification that training was effective | Verification for REQ-01-07-003 says "Review of training records and training material documentation" but does not define what constitutes sufficient training evidence (attendance alone vs. competency demonstration); certified justification requires an objective standard | Specification.md | Verification table, REQ-01-07-003 | -- | Specification.md | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add "structural" to the disciplines listed in REQ-01-07-004 for as-built drawings; currently lists "electrical, mechanical, and plumbing" but omits structural despite Guidance Example listing it and Procedure Step B6 including it | REQ-01-07-004 lists "electrical, mechanical, and plumbing" for as-built drawings but the Guidance Example and Procedure Step B6 both include "structural" as a required discipline; exhaustive compliance coverage requires the normative requirement to match the expected scope | Specification.md | REQ-01-07-004 | -- | Specification.md | TBD |
| C-003 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add a procedure step or sub-step under Part B addressing warranty claim response process during the 12-month warranty period (between Step B12 and B13); Guidance P5 and Procedure Step A6 reference warranty claim response but no execution-phase step covers it | Procedure Step A6 (proposal phase) describes "Warranty claim response process during warranty period" but no execution-phase step (Part B) covers how the DB actually receives, tracks, and responds to warranty claims during the 12-month period; comprehensive operational scope requires this | Procedure.md | Part B (between Step B12 and B13), Step A6 | -- | Procedure.md | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | mandatory compliance foundation | 0 | NO_ITEMS | Compliance foundation solid with 16 requirements and RFP tracing |
| F:normative:sufficiency | normative | sufficiency | defensible conformance basis | 1 | HAS_ITEMS | Owner-approved format undefined |
| F:normative:completeness | normative | completeness | holistic conformance framework | 1 | HAS_ITEMS | No requirement for commissioning plan approval before execution |
| F:normative:consistency | normative | consistency | harmonized regulatory discipline | 0 | NO_ITEMS | Regulatory references harmonized across documents |
| F:operative:necessity | operative | necessity | validated operational foundation | 0 | NO_ITEMS | Operational foundation validated through prerequisites |
| F:operative:sufficiency | operative | sufficiency | verified operational readiness | 1 | HAS_ITEMS | No explicit readiness gate between construction completion and commissioning start |
| F:operative:completeness | operative | completeness | total operational proficiency | 0 | NO_ITEMS | Operational proficiency addressed across 21 steps |
| F:operative:consistency | operative | consistency | coherent performance standard | 0 | NO_ITEMS | Performance standards coherent across Specification verification and Procedure verification |
| F:evaluative:necessity | evaluative | necessity | fundamental quality criterion | 1 | HAS_ITEMS | No minimum quality standard for as-built drawing accuracy |
| F:evaluative:completeness | evaluative | completeness | comprehensive merit accounting | 0 | NO_ITEMS | Merit accounting covered through deficiency valuation and SP gate |
| F:evaluative:sufficiency | evaluative | sufficiency | substantiated quality judgment | 0 | NO_ITEMS | Quality judgment substantiated through verification approach |
| F:evaluative:consistency | evaluative | consistency | integrated quality coherence | 0 | NO_ITEMS | Quality coherence maintained across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | WeakStatement | Specification | Specification | Clarify what "Owner-approved format" means for digital deliverables in REQ-01-07-004 and REQ-01-07-005, or add a requirement that the DB shall confirm format with Owner prior to production (as noted in Guidance OI-01-07-003) | RFP Section 7.5 requires digital copy in "Owner-approved format" but this format is not defined; Guidance OI-01-07-003 flags this as an open item; the Specification requirement repeats the ambiguity without resolving it; defensible conformance requires a defined standard | Specification.md, Guidance.md | REQ-01-07-004, REQ-01-07-005, OI-01-07-003 | -- | Owner to specify | TBD |
| F-002 | F:normative:completeness | MissingSlot | Specification | Specification | Add a requirement for Owner review and approval of the commissioning plan prior to commissioning execution; currently REQ-01-07-001 covers proposal narrative and REQ-01-07-002 covers execution, but no requirement gates the plan approval between them | The holistic conformance framework has a gap between proposal (REQ-01-07-001) and execution (REQ-01-07-002); there is no requirement for the commissioning plan to be reviewed/approved by the Owner before execution begins, which is standard practice and would close the conformance loop | Specification.md | Between REQ-01-07-001 and REQ-01-07-002 | -- | Specification.md | TBD |
| F-003 | F:operative:sufficiency | VerificationGap | Procedure | Procedure | Add an explicit readiness verification gate between construction substantial completion and commissioning start in Procedure Part B; Procedure prerequisite says "Construction substantially complete" but no step verifies this before Step B4 | Procedure execution prerequisite states "Construction substantially complete" and Step B4 begins commissioning, but there is no explicit verification step or gate confirming readiness to commence commissioning; verified operational readiness requires a defined go/no-go check | Procedure.md | Execution Phase Prerequisites, Step B4 | -- | Procedure.md | TBD |
| F-004 | F:evaluative:necessity | RationaleGap | Guidance | Guidance | Add guidance on minimum acceptable accuracy standard for as-built drawings (e.g., how much deviation from design is acceptable before it must be recorded as a change); Guidance C1 addresses timing but not accuracy criteria | Guidance C1 discusses timing of as-built compilation but not the fundamental quality criterion of as-built drawing accuracy; for a permanent record, a minimum accuracy standard would help both the DB and Owner understand what "as-built" means in practice | Guidance.md | C1 | -- | Guidance.md | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | established regulatory mandate | 0 | NO_ITEMS | Regulatory mandates established via RFP and standards references |
| D:normative:applying | normative | applying | grounded compulsory practice | 0 | NO_ITEMS | Compulsory practices grounded in RFP requirements |
| D:normative:judging | normative | judging | definitive conformance verdict | 1 | HAS_ITEMS | SP gate verification lacks explicit checklist format |
| D:normative:reviewing | normative | reviewing | settled compliance oversight | 0 | NO_ITEMS | Compliance oversight addressed through verification tables |
| D:operative:guiding | operative | guiding | established procedural pathway | 0 | NO_ITEMS | Procedural pathway well-established across 21 steps |
| D:operative:applying | operative | applying | assured execution readiness | 1 | HAS_ITEMS | Subcontractor O&M submittal tracking not specified |
| D:operative:judging | operative | judging | confirmed performance judgment | 0 | NO_ITEMS | Performance judgment covered through verification |
| D:operative:reviewing | operative | reviewing | established process benchmark | 0 | NO_ITEMS | Process benchmarks established through timing references |
| D:evaluative:guiding | evaluative | guiding | definitive value direction | 0 | NO_ITEMS | Value direction provided through Guidance principles |
| D:evaluative:applying | evaluative | applying | grounded merit realization | 1 | HAS_ITEMS | No metrics for training effectiveness |
| D:evaluative:judging | evaluative | judging | conclusive worth ruling | 0 | NO_ITEMS | Worth ruling addressed through SP gate and warranty |
| D:evaluative:reviewing | evaluative | reviewing | assured merit soundness | 0 | NO_ITEMS | Merit soundness assured through comprehensive verification |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:judging | VerificationGap | Specification | Specification | Add a formal checklist or verification step for the Substantial Performance gate (REQ-01-07-006) that explicitly confirms receipt of each of the 5 required documents with date stamps and sign-off | REQ-01-07-006 defines the 5-document gate and Verification says "Confirm receipt of all 5 Substantial Performance documents by Owner" but does not specify the format of this confirmation; a definitive conformance verdict requires a structured sign-off mechanism | Specification.md | Verification table, REQ-01-07-006 | -- | Specification.md | TBD |
| D-002 | D:operative:applying | MissingSlot | Procedure | Procedure | Add a tracking mechanism or checklist step in Procedure Part B for monitoring subcontractor O&M submittal status against the requirements established in Step B1 | Procedure Step B1 establishes O&M submittal requirements with subcontractors at award, but there is no subsequent tracking step to monitor compliance; Guidance C2 warns that late submission is a common delay source, yet the procedure has no explicit tracking mechanism to assure execution readiness | Procedure.md | Step B1, entire Part B scanned | -- | Procedure.md | TBD |
| D-003 | D:evaluative:applying | VerificationGap | Specification | Specification | Add acceptance criteria for training effectiveness in the Verification table for REQ-01-07-003; current approach verifies documentation existence but not that training achieved its purpose of operational readiness | Verification for REQ-01-07-003 checks that training was delivered and documented but does not verify that Owner staff can actually operate systems; grounded merit realization requires verifying that training achieved its objective, not just that it occurred | Specification.md | Verification table, REQ-01-07-003 | -- | Specification.md | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | mandated foundational direction | 0 | NO_ITEMS | Foundational direction mandated through RFP and OBJ-009 |
| X:guiding:sufficiency | guiding | sufficiency | warranted directional competence | 0 | NO_ITEMS | Directional competence warranted through Guidance principles |
| X:guiding:completeness | guiding | completeness | exhaustive directional scope | 1 | HAS_ITEMS | No guidance on IT/telecom as-built drawing scope |
| X:guiding:consistency | guiding | consistency | coherent governance principle | 0 | NO_ITEMS | Governance principles coherent across documents |
| X:applying:necessity | applying | necessity | obligatory readiness fulfillment | 1 | HAS_ITEMS | No requirement for pre-commissioning system energization verification |
| X:applying:sufficiency | applying | sufficiency | demonstrated practice sufficiency | 0 | NO_ITEMS | Practice sufficiency demonstrated through verification approach |
| X:applying:completeness | applying | completeness | comprehensive delivery completeness | 1 | HAS_ITEMS | Datasheet missing artifact for warranty response tracking log |
| X:applying:consistency | applying | consistency | consistent practice discipline | 0 | NO_ITEMS | Practice discipline consistent across procedure steps |
| X:judging:necessity | judging | necessity | authoritative determination finding | 1 | HAS_ITEMS | Verification timing for REQ-01-07-009 is vague |
| X:judging:sufficiency | judging | sufficiency | warranted assessment evidence | 0 | NO_ITEMS | Assessment evidence warranted through verification approach |
| X:judging:completeness | judging | completeness | thorough adjudication scope | 0 | NO_ITEMS | Adjudication scope thorough across all 16 requirements |
| X:judging:consistency | judging | consistency | principled adjudication standard | 0 | NO_ITEMS | Adjudication standards principled and consistent |
| X:reviewing:necessity | reviewing | necessity | mandatory integrity requirement | 0 | NO_ITEMS | Integrity requirements mandatory through SP gate |
| X:reviewing:sufficiency | reviewing | sufficiency | verified audit sufficiency | 1 | HAS_ITEMS | No audit trail specified for deficiency correction verification |
| X:reviewing:completeness | reviewing | completeness | comprehensive audit coverage | 0 | NO_ITEMS | Audit coverage comprehensive across verification tables |
| X:reviewing:consistency | reviewing | consistency | disciplined audit assurance | 0 | NO_ITEMS | Audit assurance disciplined through consistent verification approach |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | RationaleGap | Guidance | Guidance | Add guidance on expected scope and level of detail for IT/telecom as-built drawings; Guidance Example lists "IT/telecom as-built drawings (conduit routing, panel locations)" but no principle or consideration addresses the unique challenges of IT/telecom documentation | Guidance Example mentions IT/telecom as-built drawings but Guidance C5 (scope of "all building systems" for training) does not explicitly address IT/telecom documentation complexity; for exhaustive directional scope, guidance should address whether IT/telecom as-builts require coordination with a separate IT consultant | Guidance.md | Example: As-Built Drawing Package Contents, C5 | -- | Guidance.md | TBD |
| X-002 | X:applying:necessity | VerificationGap | Specification | Specification | Add verification step or prerequisite confirming that all systems are installed, energized, and safe to commission before commissioning execution begins (REQ-01-07-002) | Procedure prerequisite states "Construction substantially complete" and "systems are installed and energized" but Specification REQ-01-07-002 and its verification do not require confirmation of system energization as a precondition; obligatory readiness fulfillment requires explicit verification of this precondition | Specification.md, Procedure.md | Verification table REQ-01-07-002, Execution Phase Prerequisites | -- | Specification.md | TBD |
| X-003 | X:applying:completeness | MissingSlot | Datasheet | Datasheet | Add "Warranty response tracking log" to the Anticipated Artifacts table in Datasheet; Guidance P5 requires a "clear process for tracking warranty issues" but no artifact captures this | Datasheet Anticipated Artifacts lists 6 artifacts but does not include a warranty response/tracking log as a separate deliverable; Guidance P5 requires demonstrating "a clear process for tracking warranty issues and responding within the warranty period"; comprehensive delivery completeness requires this artifact to be enumerated | Datasheet.md, Guidance.md | Anticipated Artifacts, P5 | -- | Datasheet.md | TBD |
| X-004 | X:judging:necessity | WeakStatement | Specification | Specification | Clarify verification timing for REQ-01-07-009 from "Prior to substantial performance claim" to specify when during construction the deficiency review process should begin; "at an appropriate time" in the requirement is intentionally flexible but the verification timing should be more precise | REQ-01-07-009 states "At an appropriate time during the project" for establishing trade punch lists; the verification timing says "Prior to substantial performance claim" which is an end-state check, not a trigger for when the process should begin; authoritative determination finding requires a clearer temporal anchor | Specification.md | REQ-01-07-009, Verification table | -- | Specification.md | TBD |
| X-005 | X:reviewing:sufficiency | VerificationGap | Specification | Procedure | Add a verification step specifying how deficiency correction is documented and audited (e.g., photographic evidence, sign-off sheets, re-inspection records) for REQ-01-07-011 | Verification for REQ-01-07-011 says "Confirm all deficiencies resolved to Owner and OSR satisfaction" but does not specify the audit trail for deficiency correction (what evidence of correction is required); verified audit sufficiency requires a defined documentation standard for each corrected item | Specification.md | Verification table, REQ-01-07-011 | -- | Procedure.md | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | imperative regulatory assurance | 1 | HAS_ITEMS | Warranty commencement trigger verification gap |
| E:normative:sufficiency | normative | sufficiency | verified regulatory sufficiency | 0 | NO_ITEMS | Regulatory sufficiency verified through standards and verification tables |
| E:normative:completeness | normative | completeness | exhaustive regulatory fulfillment | 0 | NO_ITEMS | Regulatory fulfillment exhaustive across 16 requirements |
| E:normative:consistency | normative | consistency | coherent regulatory discipline | 0 | NO_ITEMS | Regulatory discipline coherent across documents |
| E:operative:necessity | operative | necessity | essential operational mandate | 1 | HAS_ITEMS | No explicit step for Owner acceptance of delivered documents |
| E:operative:sufficiency | operative | sufficiency | demonstrated operational sufficiency | 0 | NO_ITEMS | Operational sufficiency demonstrated through comprehensive procedure |
| E:operative:completeness | operative | completeness | comprehensive operational delivery | 0 | NO_ITEMS | Operational delivery comprehensive across both phases |
| E:operative:consistency | operative | consistency | reliable operational governance | 0 | NO_ITEMS | Operational governance reliable across procedure steps |
| E:evaluative:necessity | evaluative | necessity | essential merit authority | 0 | NO_ITEMS | Merit authority established through SP gate and warranty framework |
| E:evaluative:sufficiency | evaluative | sufficiency | demonstrated merit sufficiency | 0 | NO_ITEMS | Merit sufficiency demonstrated through verification approach |
| E:evaluative:completeness | evaluative | completeness | comprehensive value realization | 1 | HAS_ITEMS | Datasheet missing interface with DEL-01-04 for AHJ coordination |
| E:evaluative:consistency | evaluative | consistency | principled merit governance | 0 | NO_ITEMS | Merit governance principled across all documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:necessity | VerificationGap | Specification | Specification | Add explicit verification that the warranty period commencement date (occupancy permit issuance date) is formally recorded and communicated to both parties for REQ-01-07-014 | Verification for REQ-01-07-014 says "Confirm warranty documentation issued; warranty period tracked from occupancy permit date" but does not specify that the actual commencement date must be formally recorded and agreed; imperative regulatory assurance requires an unambiguous trigger record | Specification.md | Verification table, REQ-01-07-014 | -- | Specification.md | TBD |
| E-002 | E:operative:necessity | MissingSlot | Procedure | Procedure | Add a formal Owner acceptance/sign-off step for each major deliverable package (as-built drawings, O&M manuals, commissioning reports) in Procedure Part B; current steps describe production and delivery but not formal acceptance | Procedure Steps B4-B8 describe producing and delivering documents but no step requires formal Owner acknowledgment of receipt and acceptance; essential operational mandate requires a handoff confirmation to close the delivery loop and trigger the SP gate (Step B10) | Procedure.md | Steps B4-B8, Step B10 | -- | Procedure.md | TBD |
| E-003 | E:evaluative:completeness | RationaleGap | Datasheet | Guidance | Add Datasheet interface entry and Guidance consideration for coordination between DEL-01-07 (commissioning/closeout) and DEL-01-04 (Permitting, Inspections & AHJ Coordination) for overlapping AHJ inspection and occupancy permit activities | Datasheet Dependencies table lists "All design disciplines," "Vendors and manufacturers," "Building Operations staff," and "Payment Certifier" but does not reference DEL-01-04 (Permitting, Inspections & AHJ Coordination) despite REQ-01-07-007 requiring regulatory approvals for occupancy and Guidance C3 discussing AHJ coordination; comprehensive value realization requires explicit interface tracking | Datasheet.md, Guidance.md | Dependencies and Interfaces, C3, REQ-01-07-007 | -- | Datasheet.md | TBD |
