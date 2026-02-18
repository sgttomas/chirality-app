# Semantic Lensing Register: DEL-02-02 Firehall Apparatus Bays & Support Spaces

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/PKG-002_Main Public Services Building (PSB)/1_Working/DEL-02-02_Firehall Apparatus Bays & Support Spaces/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-02-02 context (PKG-002, Architecture/MEP, SOW-0202/0203/0205/0206, OBJ-002)
- _STATUS.md -- Current State: SEMANTIC_READY (as of 2026-02-17)
- _SEMANTIC.md -- Matrices A, B, C, F, D, X, E parsed (92 cells total)
- Datasheet.md -- DEL-02-02 identification, attributes, conditions, construction, references
- Specification.md -- DEL-02-02 scope, 17 requirements (REQ-0202-01 through REQ-0202-17), standards, verification, documentation
- Guidance.md -- DEL-02-02 purpose, 7 principles, considerations, trade-offs, examples, conflict table
- Procedure.md -- DEL-02-02 production steps (Phase A proposal, Phase B detailed design), verification, records
- _REFERENCES.md -- OSR Appendix A, Functional Program Appendix B, Addendum 03

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 5
  - Specification: 12
  - Guidance: 5
  - Procedure: 3
  - Multi: 3
- By matrix:
  - A: 5  B: 5  C: 4  F: 4  D: 3  X: 5  E: 2
- By type:
  - Conflict: 1
  - VerificationGap: 7
  - MissingSlot: 7
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Standards access status unresolved |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Compressed air specification weak |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | ABC compliance verification incomplete |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Apparatus dimensions assumption |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | |
| A:evaluative:applying | evaluative | applying | merit application | 1 | HAS_ITEMS | Sump sizing criteria absent |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Record TBD: Obtain full text of Alberta Building Code (ABC) and confirm NFPA 1, NFPA 1989, and Alberta OHS applicability with AHJ before detailed design | Standards table lists ABC as "location TBD" and NFPA 1/1989/OHS as "ASSUMPTION: likely applicable." Prescriptive direction cannot be confirmed without access to the actual normative texts. | Specification.md | ## Standards | -- | AHJ and MEP lead | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Clarify compressed air specification: pressure, volume, connection type, and whether breathing-air grade or shop-air grade is required for bay connections | REQ-0202-03 and REQ-0202-16 require compressed air but do not specify air quality grade (breathing air vs. shop air) or pressure/volume for bay connections. This ambiguity could change implementation. | Specification.md | REQ-0202-03; REQ-0202-16 | -- | Design-Builder MEP lead | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add acceptance criteria for ABC compliance verification: specify which ABC occupancy classification, egress travel-distance limits, and accessibility provisions apply to firehall wing | REQ-0202-17 requires ABC compliance but the verification entry only says "Confirm egress paths, occupant loads, and accessibility on drawings; AHJ review at permit stage." No specific ABC criteria are cited for self-check before AHJ submission. | Specification.md | REQ-0202-17; ## Verification | -- | Architect (Arch lead) | TBD |
| A-004 | A:operative:applying | TBD_Question | Procedure | Procedure | Record TBD: Confirm actual Type 1 engine and Type 1 aerial apparatus dimensions with Owner before finalizing bay geometry (Procedure Step 2.1 flags this as assumption) | Step 2.1 uses assumed apparatus dimensions (35-40 ft engine, 45+ ft aerial). These are critical to bay sizing; actual Owner fleet data is needed. | Procedure.md | ## Steps > Phase A > Step 2 | -- | Owner (Fire Department) | TBD |
| A-005 | A:evaluative:applying | MissingSlot | Specification | Specification | Add sump sizing criteria or acceptance basis for bay sumps (capacity, drainage rate, or reference standard) | REQ-0202-05 requires bay sumps but provides no sizing criteria. Guidance mentions snow accumulation from large apparatus and coordination with DEL-02-05, but no acceptance threshold exists. | Specification.md; Guidance.md | REQ-0202-05; ## Considerations > Bay Sump Sizing | -- | MEP lead | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Ceiling type unspecified |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Lighting levels TBD |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Datasheet status discrepancy |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | |
| B:information:sufficiency | information | sufficiency | adequate context | 1 | HAS_ITEMS | Contamination gradient not in Specification |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology drift: duty gear / bunker gear |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add ceiling type/height data for apparatus bays; currently "Not prescribed by Owner; DB to propose" -- record as design decision TBD with any constraints (e.g., minimum clearance above 16 ft doors) | Datasheet Conditions states ceiling type is "Not prescribed by Owner; DB to propose" but no minimum clear height above the 16 ft door is recorded as a factual constraint. This is an essential parameter for structural coordination. | Datasheet.md | ## Conditions | -- | Architect / Structural | TBD |
| B-002 | B:data:sufficiency | TBD_Question | Specification | Specification | Record TBD: Determine IES lighting level criteria for apparatus bays (Standards table lists "IES criteria TBD") | Standards table identifies IES Lighting Standards as applicable but marks specific criteria as TBD. Adequate evidence for lighting design cannot be established until these values are defined. | Specification.md | ## Standards | -- | Electrical Engineer | TBD |
| B-003 | B:data:completeness | Normalization | Datasheet | Datasheet | Update Datasheet Status field from "OPEN" to "SEMANTIC_READY" to match _STATUS.md current state | Datasheet Identification table shows "Status: OPEN (as of 2026-02-17)" but _STATUS.md shows "Current State: SEMANTIC_READY" as of the same date. This is a data-completeness discrepancy. | Datasheet.md; _STATUS.md | ## Identification | -- | Process (automated) | TBD |
| B-004 | B:information:sufficiency | RationaleGap | Guidance | Specification | Add contamination-gradient zoning as an explicit design requirement or acceptance criterion in Specification, not only as a Guidance principle | Guidance Principle 1 describes the contamination gradient as a layout driver, but Specification has no requirement that explicitly mandates zoning separation between apparatus (dirty) and office (clean) zones. The principle is only implied by REQ-0202-08's "access to office/shared areas." | Guidance.md; Specification.md | ## Principles > 1. Operational Sequence as Layout Driver; REQ-0202-08 | -- | Architect | TBD |
| B-005 | B:information:consistency | Normalization | Multi | Guidance | Standardize terminology: "Duty Gear Room" vs. "bunker gear locker room" -- documents use both terms interchangeably; clarify whether these are the same room or distinct spaces | Datasheet uses "Duty gear room area: 350-550 sf" and separately "Bunker gear lockers (quantity): 40." Specification REQ-0202-09 maps the locker room to "Duty Gear Room classification." Guidance Conflict CF-0202-02 flags the ambiguity. Terminology should be normalized across all documents. | Datasheet.md; Specification.md; Guidance.md | Datasheet ## Gear Storage Spaces; REQ-0202-09; Guidance ## Conflict Table CF-0202-02 | -- | Architect / Owner | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | obligatory compliance baseline | 1 | HAS_ITEMS | Fire gear storage climate control requirement unclear |
| C:normative:sufficiency | normative | sufficiency | regulatory defensibility | 0 | NO_ITEMS | |
| C:normative:completeness | normative | completeness | exhaustive regulatory coverage | 1 | HAS_ITEMS | Post-disaster classification gap |
| C:normative:consistency | normative | consistency | compliance coherence | 0 | NO_ITEMS | |
| C:operative:necessity | operative | necessity | operational readiness threshold | 1 | HAS_ITEMS | Simultaneous donning not formalized |
| C:operative:sufficiency | operative | sufficiency | demonstrated capability | 0 | NO_ITEMS | |
| C:operative:completeness | operative | completeness | comprehensive operational coverage | 0 | NO_ITEMS | |
| C:operative:consistency | operative | consistency | reliable operational discipline | 0 | NO_ITEMS | |
| C:evaluative:necessity | evaluative | necessity | fundamental merit criterion | 1 | HAS_ITEMS | No quality criteria for overhead door hardware |
| C:evaluative:sufficiency | evaluative | sufficiency | defensible value judgment | 0 | NO_ITEMS | |
| C:evaluative:completeness | evaluative | completeness | exhaustive merit accounting | 0 | NO_ITEMS | |
| C:evaluative:consistency | evaluative | consistency | principled evaluation standard | 0 | NO_ITEMS | |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Clarify whether "climate controlled" for fire gear storage (REQ-0202-13) means heated, cooled, or both; specify temperature/humidity range if applicable | REQ-0202-13 states "climate controlled per Functional Program" but no temperature or humidity range is given. The term "climate controlled" is ambiguous and could mean different things to different trades. | Specification.md | REQ-0202-13 | -- | Owner / MEP lead | TBD |
| C-002 | C:normative:completeness | RationaleGap | Guidance | Guidance | Add rationale explaining implications of AHJ post-disaster exemption on structural design, seismic category, and firehall wing construction requirements | Datasheet and Specification note that AHJ intends to exempt post-disaster importance category (OSR 10.3.5), but Guidance does not explain the design implications of this exemption vs. if it were classified as post-disaster. This is a significant structural and cost decision. | Datasheet.md; Specification.md; Guidance.md | Datasheet ## Conditions; REQ-0202-17; entire Guidance scanned | -- | Structural / AHJ | TBD |
| C-003 | C:operative:necessity | MissingSlot | Specification | Specification | Add operational performance requirement for simultaneous gear donning (e.g., minimum number of firefighters who can don gear simultaneously without interference) | Guidance Principle 5 states "The layout should allow two firefighters to don gear simultaneously without interference" but this is not captured as a Specification requirement. It is only an assumption in Guidance. | Guidance.md; Specification.md | Guidance ## Principles > 5; entire Specification scanned | -- | Owner (Fire Department) | TBD |
| C-004 | C:evaluative:necessity | WeakStatement | Specification | Specification | Define "'car wash' grade hardware" for overhead doors: specify the standard, rating, or performance criteria that constitute this grade | Datasheet and REQ-0202-02 reference "'car wash' grade hardware" (from OSR 10.3.9) but neither document defines what this means in terms of corrosion resistance rating, material specification, or applicable standard. | Specification.md; Datasheet.md | REQ-0202-02; Datasheet ## Apparatus Bays | -- | Architect / Door supplier | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | authoritative obligation clarity | 1 | HAS_ITEMS | Exhaust mitigation vs. exhaust ventilation distinction |
| F:normative:sufficiency | normative | sufficiency | sufficient regulatory substantiation | 0 | NO_ITEMS | |
| F:normative:completeness | normative | completeness | total compliance fulfillment | 1 | HAS_ITEMS | NFPA applicability unconfirmed |
| F:normative:consistency | normative | consistency | unified regulatory framework | 0 | NO_ITEMS | |
| F:operative:necessity | operative | necessity | validated operational preparedness | 1 | HAS_ITEMS | Emergency egress from bays |
| F:operative:sufficiency | operative | sufficiency | sufficient operational competence | 0 | NO_ITEMS | |
| F:operative:completeness | operative | completeness | total operational mastery | 0 | NO_ITEMS | |
| F:operative:consistency | operative | consistency | standardized operational coherence | 0 | NO_ITEMS | |
| F:evaluative:necessity | evaluative | necessity | intrinsic quality recognition | 1 | HAS_ITEMS | Floor finish specification gap |
| F:evaluative:sufficiency | evaluative | sufficiency | justified merit appraisal | 0 | NO_ITEMS | |
| F:evaluative:completeness | evaluative | completeness | comprehensive value mastery | 0 | NO_ITEMS | |
| F:evaluative:consistency | evaluative | consistency | harmonized merit standard | 0 | NO_ITEMS | |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | Normalization | Multi | Guidance | Clarify distinction between "vehicle exhaust mitigation" (REQ-0202-03, two connections per bay) and "direct exhaust ventilation" (REQ-0202-04, sized for two apparatus per bay); document whether these are the same system or separate systems | REQ-0202-03 uses "vehicle exhaust mitigation connections" and REQ-0202-04 uses "direct exhaust ventilation." Guidance Trade-off 3 discusses direct capture vs. dilution. The relationship between the two requirements needs explicit clarification to avoid scope confusion with DEL-02-05. | Specification.md; Guidance.md | REQ-0202-03; REQ-0202-04; ## Trade-offs > Trade-off 3 | -- | MEP lead | TBD |
| F-002 | F:normative:completeness | VerificationGap | Specification | Specification | Add verification approach for NFPA 1, NFPA 1989, and Alberta OHS applicability -- currently listed as assumptions with no verification step | Standards table lists NFPA 1, NFPA 1989, and Alberta OHS as "ASSUMPTION: likely applicable; confirm with AHJ/MEP lead" but no corresponding verification entry exists in the Verification table. | Specification.md | ## Standards; ## Verification | -- | AHJ / MEP lead | TBD |
| F-003 | F:operative:necessity | MissingSlot | Specification | Specification | Add emergency egress requirements specific to apparatus bays (e.g., personnel doors for pedestrian egress when overhead doors are closed, egress from between parked apparatus) | REQ-0202-17 references general ABC compliance for egress but no requirement addresses bay-specific pedestrian egress (personnel doors, travel distance from inside bays). Procedure Step 4.4 mentions ABC egress but only for support rooms. | Specification.md; Procedure.md | REQ-0202-17; Procedure ## Steps > Phase A > Step 4 | -- | Architect / AHJ | TBD |
| F-004 | F:evaluative:necessity | WeakStatement | Specification | Specification | Specify floor finish requirements beyond "concrete" and "sealed" -- e.g., minimum compressive strength, slip resistance rating, chemical resistance for decon areas, or reference to applicable standard | REQ-0202-06 requires "concrete" floors and Datasheet/Conditions says "Sealed concrete; resilient, easily cleaned of mud/dust." No performance specification exists for the concrete itself (strength, finish, slip resistance), particularly for decontamination areas where chemical exposure may occur. | Specification.md; Datasheet.md | REQ-0202-06; Datasheet ## Conditions | -- | Architect / Structural | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | definitive regulatory directive | 0 | NO_ITEMS | |
| D:normative:applying | normative | applying | enforced regulatory execution | 1 | HAS_ITEMS | Accessibility requirements not elaborated |
| D:normative:judging | normative | judging | conclusive conformance verdict | 0 | NO_ITEMS | |
| D:normative:reviewing | normative | reviewing | integrated compliance examination | 0 | NO_ITEMS | |
| D:operative:guiding | operative | guiding | confirmed operational governance | 1 | HAS_ITEMS | Coordination protocol not formalized |
| D:operative:applying | operative | applying | adequate operational delivery | 0 | NO_ITEMS | |
| D:operative:judging | operative | judging | settled performance authority | 0 | NO_ITEMS | |
| D:operative:reviewing | operative | reviewing | systematic procedural inspection | 0 | NO_ITEMS | |
| D:evaluative:guiding | evaluative | guiding | principled quality steering | 1 | HAS_ITEMS | Owner operational review not in verification |
| D:evaluative:applying | evaluative | applying | substantiated merit delivery | 0 | NO_ITEMS | |
| D:evaluative:judging | evaluative | judging | settled merit adjudication | 0 | NO_ITEMS | |
| D:evaluative:reviewing | evaluative | reviewing | integrated quality inspection | 0 | NO_ITEMS | |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | MissingSlot | Specification | Specification | Add accessibility requirements specific to firehall wing (e.g., which support spaces require barrier-free access under ABC, whether apparatus bays require accessible routes) | REQ-0202-17 references ABC accessibility generically ("as applicable") but no specific accessibility requirements are defined for firehall spaces. Volunteer fire departments have specific accessibility considerations that differ from general commercial occupancy. | Specification.md | REQ-0202-17 | -- | Architect / AHJ | TBD |
| D-002 | D:operative:guiding | MissingSlot | Procedure | Procedure | Add a formal coordination protocol or checklist for DEL-02-04, DEL-02-05, DEL-02-06, DEL-02-07 interfaces -- currently described as coordination references but no procedural mechanism for tracking interface resolution | Procedure lists upstream dependencies (DEL-02-04 through -07) and multiple steps reference coordination, but no formal coordination protocol (e.g., interface register, coordination meeting cadence, sign-off checklist) is defined. Specification Documentation section mentions "Coordination matrix" as a required artifact but Procedure does not include a step to produce it. | Procedure.md; Specification.md | Procedure ## Prerequisites; Specification ## Documentation | -- | Project Manager | TBD |
| D-003 | D:evaluative:guiding | VerificationGap | Procedure | Procedure | Add a verification step for Owner/Fire Department operational review of apparatus bay layouts before finalizing proposal submission | Procedure lists "Fire Department representative (Owner)" as required personnel but no verification step requires an explicit operational sign-off or walkthrough review by the Fire Department before proposal submission. | Procedure.md | ## Prerequisites > Personnel Required; ## Verification | -- | Architect / Owner | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | imperative readiness guidance | 1 | HAS_ITEMS | No pre-design readiness checklist |
| X:guiding:sufficiency | guiding | sufficiency | justified capability guidance | 0 | NO_ITEMS | |
| X:guiding:completeness | guiding | completeness | exhaustive stewardship oversight | 0 | NO_ITEMS | |
| X:guiding:consistency | guiding | consistency | unified governance benchmark | 0 | NO_ITEMS | |
| X:applying:necessity | applying | necessity | obligatory readiness fulfillment | 0 | NO_ITEMS | |
| X:applying:sufficiency | applying | sufficiency | demonstrated implementation adequacy | 1 | HAS_ITEMS | Bay services verification lacks specificity |
| X:applying:completeness | applying | completeness | exhaustive implementation delivery | 0 | NO_ITEMS | |
| X:applying:consistency | applying | consistency | standardized implementation discipline | 0 | NO_ITEMS | |
| X:judging:necessity | judging | necessity | mandatory conformance judgment | 1 | HAS_ITEMS | No hold/witness points defined |
| X:judging:sufficiency | judging | sufficiency | substantiated performance finding | 0 | NO_ITEMS | |
| X:judging:completeness | judging | completeness | exhaustive capability verdict | 1 | HAS_ITEMS | Missing verification for REQ-0202-13 climate control |
| X:judging:consistency | judging | consistency | consistent adjudication standard | 0 | NO_ITEMS | |
| X:reviewing:necessity | reviewing | necessity | fundamental compliance audit | 1 | HAS_ITEMS | No internal review gate before AHJ submission |
| X:reviewing:sufficiency | reviewing | sufficiency | substantiated procedural audit | 0 | NO_ITEMS | |
| X:reviewing:completeness | reviewing | completeness | exhaustive procedural review | 0 | NO_ITEMS | |
| X:reviewing:consistency | reviewing | consistency | reliable systematic audit | 0 | NO_ITEMS | |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:necessity | MissingSlot | Procedure | Procedure | Add a pre-design readiness checklist confirming all prerequisite inputs (Owner apparatus data, ABC full text, AHJ classification ruling) are available before commencing bay geometry | Procedure Step 2 launches directly into bay geometry without a gating check that essential input data has been obtained. Several assumptions are flagged in Steps 2.1 but no formal go/no-go criterion exists. | Procedure.md | ## Steps > Phase A > Step 2 | -- | Project Manager | TBD |
| X-002 | X:applying:sufficiency | VerificationGap | Specification | Specification | Strengthen verification for REQ-0202-03 (bay services): specify what "shown on layout drawings per bay" means -- confirm locations, quantities, and connection specifications (not just presence on drawing) | Verification table for REQ-0202-03 says "Confirm electrical, compressed air, and exhaust connections shown on layout drawings per bay." This checks presence but not adequacy of specification (connection type, sizing, spacing). | Specification.md | ## Verification > REQ-0202-03 | -- | MEP lead | TBD |
| X-003 | X:judging:necessity | VerificationGap | Procedure | Specification | Add hold points or witness points for critical construction milestones (e.g., sump installation before slab pour, exhaust connection rough-in before ceiling closure) | Neither Specification verification table nor Procedure defines construction-phase hold/witness points. For a firehall with embedded services in slab and ceiling, critical inspections are needed before concealment. | Specification.md; Procedure.md | ## Verification; Procedure ## Steps > Phase B | -- | Construction Manager / AHJ | TBD |
| X-004 | X:judging:completeness | VerificationGap | Specification | Specification | Add verification entry for REQ-0202-13 "climate controlled" fire gear storage -- no verification approach exists for confirming climate control is achieved | Verification table has entries for most requirements but REQ-0202-13 (fire gear storage, 200-350 sf, climate controlled) verification only says "Confirm 200-350 sf climate-controlled space on plan." It does not specify how "climate controlled" will be verified (temperature range, HVAC schedule confirmation). | Specification.md | ## Verification > REQ-0202-13 | -- | MEP lead | TBD |
| X-005 | X:reviewing:necessity | VerificationGap | Procedure | Procedure | Add an internal code-compliance review gate before AHJ permit submission to confirm all ABC requirements are addressed on drawings | Procedure Step 10.2 says "Confirm ABC compliance review completed" at 60%/100% milestones but does not describe a formal internal review process or checklist before AHJ submission. The verification table defers to "AHJ review; permit issuance" as the acceptance criterion for REQ-0202-17. | Procedure.md; Specification.md | Procedure ## Steps > Phase B > Step 10; Specification ## Verification > REQ-0202-17 | -- | Architect | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | enforced readiness compliance | 0 | NO_ITEMS | |
| E:normative:sufficiency | normative | sufficiency | justified compliance adequacy | 0 | NO_ITEMS | |
| E:normative:completeness | normative | completeness | total regulatory fulfillment | 1 | HAS_ITEMS | Conflict on gear room mapping |
| E:normative:consistency | normative | consistency | dependable compliance benchmark | 0 | NO_ITEMS | |
| E:operative:necessity | operative | necessity | essential capability governance | 0 | NO_ITEMS | |
| E:operative:sufficiency | operative | sufficiency | confirmed operational sufficiency | 0 | NO_ITEMS | |
| E:operative:completeness | operative | completeness | exhaustive operational command | 1 | HAS_ITEMS | Compressed air distribution gaps |
| E:operative:consistency | operative | consistency | unified operational standard | 0 | NO_ITEMS | |
| E:evaluative:necessity | evaluative | necessity | authoritative merit governance | 0 | NO_ITEMS | |
| E:evaluative:sufficiency | evaluative | sufficiency | confirmed merit sufficiency | 0 | NO_ITEMS | |
| E:evaluative:completeness | evaluative | completeness | exhaustive merit fulfillment | 0 | NO_ITEMS | |
| E:evaluative:consistency | evaluative | consistency | dependable merit benchmark | 0 | NO_ITEMS | |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:completeness | Conflict | Multi | TBD | Resolve whether "Duty Gear Room" (350-550 sf) is the bunker gear locker room or a separate space from "Fire Gear Storage" (200-350 sf); Guidance CF-0202-02 flags this but no ruling exists | Datasheet lists Duty Gear Room (350-550 sf) and Fire Gear Storage (200-350 sf) as separate entries. Specification REQ-0202-09 maps locker room to "Duty Gear Room classification." Guidance proposes a mapping but it remains unresolved. Without resolution, total regulatory fulfillment cannot be assessed -- the required locker room area is ambiguous. | Datasheet.md; Specification.md; Guidance.md | Datasheet ## Gear Storage Spaces; REQ-0202-09; Guidance ## Conflict Table CF-0202-02 | Datasheet.md#Gear Storage Spaces; Specification.md#REQ-0202-09; Guidance.md#Conflict Table CF-0202-02 | Owner | TBD |
| E-002 | E:operative:completeness | RationaleGap | Guidance | Guidance | Add rationale for compressed air distribution approach: explain whether ceiling-drop or wall-mount is preferred, and whether the same compressor room serves both SCBA cascade and bay compressed-air systems or if these are separate systems | Datasheet and Specification reference both "compressed air" for bays (REQ-0202-03) and a "compressed air compressor room" (REQ-0202-16) alongside the "SCBA/cascade room" (REQ-0202-11). The relationship between these rooms and systems is not explained in Guidance. It is unclear if one compressor room serves both shop air and breathing air or if these are separate. | Specification.md; Guidance.md; Datasheet.md | REQ-0202-03; REQ-0202-11; REQ-0202-16; entire Guidance scanned | -- | MEP lead | TBD |
