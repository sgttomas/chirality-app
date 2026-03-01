# Semantic Lensing Register: DEL-011-01 Concrete Superstructure

**Generated:** 2026-02-26
**Deliverable Folder:** PKG-011_Building Structure & Envelope/1_Working/DEL-011-01_Superstructure/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-011-01_Superstructure/_CONTEXT.md
- _STATUS.md — DEL-011-01_Superstructure/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md — DEL-011-01_Superstructure/_SEMANTIC.md
- Datasheet.md — DEL-011-01_Superstructure/Datasheet.md
- Specification.md — DEL-011-01_Superstructure/Specification.md
- Guidance.md — DEL-011-01_Superstructure/Guidance.md
- Procedure.md — DEL-011-01_Superstructure/Procedure.md
- _REFERENCES.md — DEL-011-01_Superstructure/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 27
- By document:
  - Datasheet: 4
  - Specification: 10
  - Guidance: 4
  - Procedure: 5
  - Multi: 4
- By matrix:
  - A: 4  B: 3  C: 4  F: 5  D: 3  X: 5  E: 3
- By type:
  - Conflict: 2
  - VerificationGap: 7
  - MissingSlot: 6
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 2
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Weak prescriptive direction for structural system selection |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Concrete testing standards assumed not prescribed |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Code edition not specified |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | County inspection coordination well covered across documents |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure provides adequate procedural direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Cold weather concreting not addressed |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification tables present in Specification and Procedure |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Inspection coordination log and County copies well addressed |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Principles and Considerations adequately orient value |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs section in Guidance addresses merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | No warranted items; verification criteria established |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality records coverage adequate in Procedure Records section |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify in REQ-011-01-01 whether "concrete structure" prescriptively requires all-concrete or permits hybrid steel/concrete structural systems (e.g., steel roof on concrete walls) | The RFP says "concrete structure" but the specific system is left TBD. Specification REQ-011-01-01 says "shall be a concrete structure" while Guidance C1 acknowledges the system type is unresolved. A hybrid system (e.g., steel roof deck on concrete columns) may or may not satisfy "concrete structure." The prescriptive direction is ambiguous. | Specification.md; Guidance.md | Specification: REQ-011-01-01; Guidance: C1 | — | PROPOSAL: Structural Engineer of Record to confirm whether hybrid is permitted under RFP intent | TBD |
| A-002 | A:normative:applying | MissingSlot | Specification | Specification | Add explicit requirement referencing CSA A23.1/A23.2 as mandatory standard for concrete materials and construction methods, removing ASSUMPTION status | Specification Standards table lists CSA A23.1/A23.2 with status "ASSUMPTION: applicable." This is a mandatory practice for concrete construction in Alberta but is not yet prescriptively required — only assumed. | Specification.md | Standards table — CSA A23.1/A23.2 row | — | PROPOSAL: Confirm with Structural Engineer and elevate from ASSUMPTION to confirmed | TBD |
| A-003 | A:normative:judging | TBD_Question | Multi | Specification | Record TBD: Which specific edition of the National Building Code of Canada (NBC) is adopted in Alberta for this project? Cite the applicable Alberta Building Code regulation. | Specification Standards table lists NBC "current Alberta-adopted edition" but does not identify the specific edition or Alberta regulation. Compliance determination requires knowing the exact code edition. | Specification.md | Standards table — NBC row | — | PROPOSAL: Owner or Building Inspector to confirm applicable code edition | TBD |
| A-004 | A:operative:applying | MissingSlot | Procedure | Procedure | Add cold-weather and hot-weather concreting provisions (or reference to applicable IFC specification section) addressing concrete placement temperature limits and curing protection for Alberta climate | Procedure addresses concrete placement in Steps 8, 13 but does not address cold-weather concreting requirements despite Alberta central region climate (Datasheet Conditions). Practical execution in cold climate requires specific provisions. | Procedure.md; Datasheet.md | Procedure: Steps 8, 13; Datasheet: Conditions — Climate zone | — | PROPOSAL: Reference CSA A23.1 cold/hot weather clauses when confirmed | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Mezzanine design load TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Source references adequate across documents |
| B:data:completeness | data | completeness | comprehensive record | 0 | NO_ITEMS | Datasheet Attributes and Construction tables are comprehensive |
| B:data:consistency | data | consistency | reliable measurement | 1 | HAS_ITEMS | Dimensional tolerances not specified |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (IFC, inspections, milestones) well identified |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequate in Guidance Considerations |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Documentation artifacts listed in Specification and Procedure |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Wash bay scope attribution inconsistency |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Guidance Principles convey fundamental understanding |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Trade-offs section shows competent expertise framing |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Cross-package dependency awareness demonstrated |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Documents show coherent understanding of construction sequence |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Guidance P4 (embedded items) shows essential discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-off framing shows adequate judgment |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view maintained across all 4 documents |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning consistent with available RFP information |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Specification | Datasheet | Record TBD: Mezzanine design live load (kPa or psf) — must be established by Structural Engineer of Record before mezzanine design proceeds | This is an essential fact required for structural sizing. Guidance C3 identifies the gap and provides context (oil totes ~1,000 kg each) but no numeric design load appears in any document. The Datasheet says "design load TBD per structural engineer." REQ-011-01-08 defers to DEL-002-10. The actual value is missing. | Datasheet.md; Specification.md; Guidance.md | Datasheet: Mezzanine load capacity; Spec: REQ-011-01-08; Guidance: C3 | — | PROPOSAL: Structural Engineer of Record (DEL-002-10) | TBD |
| B-002 | B:data:consistency | VerificationGap | Specification | Specification | Add dimensional tolerance criteria for building footprint (REQ-011-01-02) and ceiling height (REQ-011-01-01) — currently stated as approximate values without tolerance bands | REQ-011-01-02 uses "approximately 130 ft x 100 ft" and "approximately 13,000 sq ft." REQ-011-01-01 says "minimum 35 ft." Procedure Step 24 says "within dimensional tolerance of ~130' x 100'" but no tolerance is defined. Reliable measurement requires defined tolerances. | Specification.md; Procedure.md | Spec: REQ-011-01-01, REQ-011-01-02; Proc: Steps 23, 24 | — | PROPOSAL: Structural Engineer to specify dimensional tolerances in IFC drawings | TBD |
| B-003 | B:information:consistency | Normalization | Guidance | Guidance | Normalize wash bay structural scope reference: Guidance C5 refers to "DEL-011-05" for wash bay structural enclosure, but Specification scope lists wash bay enclosure under DEL-011-01 (this deliverable). Clarify whether DEL-011-05 is the correct reference or if wash bay structure is part of DEL-011-01. | Guidance C5 says "DEL-011-05 covers the structural enclosure (walls, roof, overhead door opening, steel plate floor)" for the wash bay. But Specification Scope says DEL-011-01 covers "The enclosed wash bay structural enclosure (single bay, motor scraper-sized)" and REQ-011-01-06 requires the wash bay enclosure. These are inconsistent. | Specification.md; Guidance.md | Spec: Scope — What This Deliverable Covers; Guidance: C5 | Specification.md#Scope (wash bay under DEL-011-01); Guidance.md#C5 (wash bay under DEL-011-05) | PROPOSAL: Confirm with decomposition whether wash bay structure is DEL-011-01 or DEL-011-05 | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Obligatory Threshold | 1 | HAS_ITEMS | Minimum concrete strength not specified |
| C:normative:sufficiency | normative | sufficiency | Prescribed Acceptability | 1 | HAS_ITEMS | Floor finish specification missing |
| C:normative:completeness | normative | completeness | Exhaustive Compliance Record | 0 | NO_ITEMS | Documentation section in Specification is adequate |
| C:normative:consistency | normative | consistency | Enforced Coherence | 1 | HAS_ITEMS | Terminology drift on overhead doors |
| C:operative:necessity | operative | necessity | Operational Criticality | 0 | NO_ITEMS | Critical-path identification clear in Guidance P1 and Procedure sequencing |
| C:operative:sufficiency | operative | sufficiency | Competence Benchmark | 0 | NO_ITEMS | Prerequisites establish competence requirements adequately |
| C:operative:completeness | operative | completeness | Comprehensive Workflow Record | 0 | NO_ITEMS | Procedure Records table comprehensive |
| C:operative:consistency | operative | consistency | Reliable Process Execution | 1 | HAS_ITEMS | Concrete curing criteria incomplete |
| C:evaluative:necessity | evaluative | necessity | Foundational Worth Appraisal | 0 | NO_ITEMS | Guidance Principles and OBJ linkage adequate |
| C:evaluative:sufficiency | evaluative | sufficiency | Adequate Merit Standard | 0 | NO_ITEMS | Verification checks provide merit standards |
| C:evaluative:completeness | evaluative | completeness | Holistic Merit Account | 0 | NO_ITEMS | Trade-offs and considerations provide holistic merit framing |
| C:evaluative:consistency | evaluative | consistency | Principled Valuation | 0 | NO_ITEMS | Value reasoning consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | VerificationGap | Specification | Specification | Add minimum concrete compressive strength (f'c) requirement or explicit deferral statement to IFC structural specification package (DEL-002-10) | REQ-011-01-01 through REQ-011-01-15 do not specify minimum f'c. Procedure Steps 14, 26 reference "f'c — TBD per structural design" and "specified f'c (TBD per IFC)." This is an obligatory threshold for concrete construction that is currently undefined. | Specification.md; Procedure.md | Spec: Requirements (absent); Proc: Steps 14, 26 | — | PROPOSAL: Structural Engineer to establish f'c in DEL-002-10; Specification to reference | TBD |
| C-002 | C:normative:sufficiency | WeakStatement | Procedure | Specification | Clarify required floor slab finish (e.g., hard trowel, burnished, broom) — currently only an ASSUMPTION in Procedure Step 13 | Procedure Step 13 says "ASSUMPTION: hard trowel finish for industrial use." The finish affects acceptability for tracked/packer equipment operating on the slab. No requirement in Specification addresses floor finish. | Procedure.md; Specification.md | Proc: Step 13; Spec: REQ-011-01-05 (floor slab — no finish spec) | — | PROPOSAL: Architectural/structural design team to specify in IFC | TBD |
| C-003 | C:normative:consistency | Normalization | Multi | Guidance | Normalize terminology: "overhead doors" vs "OH doors" vs "overhead door openings" — ensure consistent term across all documents. Also clarify whether the overhead doors themselves are in DEL-011-01 scope or only the structural rough openings. | Specification REQ-011-01-11 says "structural rough openings and frames for overhead doors." Procedure Step 21 says "Install overhead door frames and structural elements." Datasheet Construction says "Overhead doors — Structural rough openings and door frames." The scope boundary between structural opening and door supply/install is not consistently expressed. | Specification.md; Procedure.md; Datasheet.md | Spec: REQ-011-01-11; Proc: Step 21; DS: Construction — Overhead doors | — | PROPOSAL: Guidance to add vocabulary note clarifying structural vs. supply/install boundary | TBD |
| C-004 | C:operative:consistency | VerificationGap | Procedure | Procedure | Add concrete curing duration and minimum strength criteria before load application — currently Step 14 says "minimum specified compressive strength" without defining the threshold or duration | Reliable process execution requires knowing when the slab can accept loads. Step 14 references curing requirements but defers entirely to IFC. No interim criterion or minimum wait period is stated. | Procedure.md | Proc: Step 14 | — | PROPOSAL: Reference CSA A23.1 minimum curing requirements when standard is confirmed | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Binding Pass Criterion | 1 | HAS_ITEMS | Crane runway tolerance criteria absent |
| F:normative:sufficiency | normative | sufficiency | Prescribed Evidentiary Bar | 1 | HAS_ITEMS | Inspection evidence requirements weak |
| F:normative:completeness | normative | completeness | Total Regulatory Account | 1 | HAS_ITEMS | Safety Code permits not enumerated |
| F:normative:consistency | normative | consistency | Enforced Regulatory Rigor | 0 | NO_ITEMS | Regulatory references consistent across documents |
| F:operative:necessity | operative | necessity | Minimum Competence Gate | 0 | NO_ITEMS | Prerequisites establish minimum competence gates |
| F:operative:sufficiency | operative | sufficiency | Adequate Process Mastery | 0 | NO_ITEMS | Step detail adequate for construction procedure |
| F:operative:completeness | operative | completeness | Total Execution Mastery | 1 | HAS_ITEMS | Formwork removal/stripping criteria absent |
| F:operative:consistency | operative | consistency | Standardized Process Order | 0 | NO_ITEMS | Phase sequencing is logical and consistent |
| F:evaluative:necessity | evaluative | necessity | Essential Merit Gate | 0 | NO_ITEMS | Merit gates covered through verification tables |
| F:evaluative:sufficiency | evaluative | sufficiency | Acceptable Quality Level | 1 | HAS_ITEMS | Concrete surface repair criteria absent |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Quality Account | 0 | NO_ITEMS | Quality records enumerated in Procedure Records table |
| F:evaluative:consistency | evaluative | consistency | Principled Quality Harmony | 0 | NO_ITEMS | Quality criteria consistent where present |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | VerificationGap | Specification | Specification | Add crane runway alignment tolerance criteria (span, elevation, levelness) as a binding pass criterion for REQ-011-01-10, or explicitly require crane manufacturer tolerances to be documented in IFC | REQ-011-01-10 says structural capacity "shall be confirmed" and verification says "crane runway elevation and alignment verified." Guidance P5 says tolerances are "specified by the crane manufacturer." But no tolerance values or reference to manufacturer's tolerance document appears in the Specification. The binding pass criterion is undefined. | Specification.md; Guidance.md | Spec: REQ-011-01-10, Verification table row 10; Guidance: P5 | — | PROPOSAL: Crane manufacturer (DEL-016-01) to supply tolerances; incorporate into REQ-011-01-10 | TBD |
| F-002 | F:normative:sufficiency | WeakStatement | Specification | Specification | Strengthen verification evidence requirements: several verification entries say only "inspection report" or "inspection sign-off" without specifying what the inspection must confirm or what constitutes a pass | Specification Verification table entries for REQ-011-01-06 ("Dimensional verification; inspection sign-off"), REQ-011-01-09 ("Inspection; code compliance check"), and REQ-011-01-12 ("Inspection against door/window schedule") are minimal. The prescribed evidentiary bar is not specific enough to determine sufficiency of evidence. | Specification.md | Verification table — rows for REQ-011-01-06, -09, -12 | — | PROPOSAL: Expand each verification entry to specify measurable pass criteria | TBD |
| F-003 | F:normative:completeness | MissingSlot | Specification | Specification | Add enumeration of specific Safety Code permits required (building, electrical, plumbing, gas, etc.) or reference to DEL-009-03 permit register for total regulatory account | REQ-011-01-04 references "all applicable Alberta building codes and regulations, and all Alberta Safety Codes." Procedure P-07 says "All applicable Safety Code permits (DEL-009-03) are obtained." But neither document enumerates which specific permits apply to the superstructure scope. Total regulatory account is incomplete. | Specification.md; Procedure.md | Spec: REQ-011-01-04; Proc: P-07 | — | PROPOSAL: Building Inspector / Safety Codes Officer to confirm required permits; list in Specification or reference DEL-009-03 | TBD |
| F-004 | F:operative:completeness | MissingSlot | Procedure | Procedure | Add formwork stripping/removal step between concrete placement and next construction phase — currently no step addresses when and how formwork is removed and what inspection is required before stripping | Procedure covers forming (Steps 6, 9-11) and concrete placement (Steps 8, 13) but has no step for formwork removal. For cast-in-place concrete, formwork stripping timing is critical and depends on concrete strength. This is a gap in total execution mastery. | Procedure.md | Proc: Phase 2 and Phase 3 (absent between Steps 8-9 and Steps 13-14) | — | PROPOSAL: Add formwork removal step with minimum strength requirement per CSA A23.1 | TBD |
| F-005 | F:evaluative:sufficiency | WeakStatement | Specification | Specification | Add acceptance criteria for concrete surface defects (honeycombing, cold joints, cracking) — no quality acceptance threshold defined for concrete surface quality | No document defines acceptable quality level for concrete surface conditions. For an industrial maintenance shop with heavy equipment, surface defect acceptance criteria affect long-term durability. The acceptable quality level for the concrete work is undefined beyond the implicit "per IFC." | Specification.md | Spec: Requirements (absent); entire document scanned | — | PROPOSAL: Reference CSA A23.1 surface defect classification or specify in IFC | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Settled Regulatory Guidance | 0 | NO_ITEMS | Guidance P2 and P6 provide settled regulatory guidance |
| D:normative:applying | normative | applying | Enforced Proof Standard | 1 | HAS_ITEMS | P.Eng. stamp verification timing gap |
| D:normative:judging | normative | judging | Binding Conformance Ruling | 0 | NO_ITEMS | Conformance determination process established in Specification Verification |
| D:normative:reviewing | normative | reviewing | Mandated Oversight Rigor | 0 | NO_ITEMS | County inspection presence and report distribution well covered |
| D:operative:guiding | operative | guiding | Settled Workflow Guidance | 0 | NO_ITEMS | Procedure phases provide settled workflow guidance |
| D:operative:applying | operative | applying | Settled Operational Delivery | 0 | NO_ITEMS | Step-by-step construction sequence well established |
| D:operative:judging | operative | judging | Settled Capability Verdict | 0 | NO_ITEMS | Load verification steps in Procedure Phase 5 address capability verdict |
| D:operative:reviewing | operative | reviewing | Settled Procedural Compliance | 1 | HAS_ITEMS | No hold-point mechanism defined |
| D:evaluative:guiding | evaluative | guiding | Settled Quality Aim | 0 | NO_ITEMS | OBJ-001 and OBJ-002 linkage clearly established |
| D:evaluative:applying | evaluative | applying | Settled Worth Deployment | 1 | HAS_ITEMS | Schedule milestone criteria absent |
| D:evaluative:judging | evaluative | judging | Settled Merit Ruling | 0 | NO_ITEMS | Verification tables establish merit ruling criteria |
| D:evaluative:reviewing | evaluative | reviewing | Settled Valuation Integrity | 0 | NO_ITEMS | Records section ensures valuation integrity through document retention |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | VerificationGap | Specification | Procedure | Add verification step confirming P.Eng. stamp is present on IFC drawings before first concrete placement — Specification REQ-011-01-03 requires it, Procedure P-01 lists it as prerequisite, but no explicit verification checkpoint exists in the Procedure steps | REQ-011-01-03 verification says "Confirmation that IFC drawings are stamped before construction begins; copy of drawings on file." Procedure P-01 lists it as a prerequisite but Steps 1-4 (pre-construction) do not include an explicit verification action to confirm and document the stamp presence. The enforced proof standard lacks a procedural enforcement point. | Specification.md; Procedure.md | Spec: REQ-011-01-03 Verification; Proc: P-01, Steps 1-4 | — | PROPOSAL: Add explicit Step in Phase 1 to verify and document P.Eng. stamp presence | TBD |
| D-002 | D:operative:reviewing | MissingSlot | Procedure | Procedure | Add hold-point / stop-work mechanism: define which inspections are mandatory hold points (construction may not proceed until inspection passes) vs. witness points (construction may proceed if inspector is notified) | Procedure lists five inspections (Steps 7, 12, 16, 19, 22) and requires County representative presence, but does not distinguish between hold points and witness points. Settled procedural compliance requires clarity on whether construction must halt if an inspection is missed or failed. | Procedure.md | Proc: Steps 7, 12, 16, 19, 22 | — | PROPOSAL: Classify each inspection as Hold Point or Witness Point in Procedure and/or Specification | TBD |
| D-003 | D:evaluative:applying | VerificationGap | Specification | Specification | Add intermediate schedule milestones or duration targets for superstructure completion that demonstrate sufficient progress toward OBJ-002 (Dec 31, 2026 deadline) — currently only final deadline is stated | REQ-011-01-14 says work must be "substantially complete in sufficient time" for downstream work to finish by Dec 31, 2026. No intermediate milestones or duration targets are specified. Settled worth deployment for the schedule objective requires measurable progress indicators. | Specification.md | Spec: REQ-011-01-14 | — | PROPOSAL: Project Manager to establish milestone schedule; reference in Specification or Procedure | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Critical Steering Mandate | 1 | HAS_ITEMS | Cistern structural interface not in requirements |
| X:guiding:sufficiency | guiding | sufficiency | Adequate Steering Evidence | 0 | NO_ITEMS | Guidance provides adequate steering evidence |
| X:guiding:completeness | guiding | completeness | Complete Governance Record | 0 | NO_ITEMS | Governance record adequate through documentation artifacts |
| X:guiding:consistency | guiding | consistency | Coherent Governance Signal | 0 | NO_ITEMS | Governance signals coherent across documents |
| X:applying:necessity | applying | necessity | Essential Delivery Proof | 1 | HAS_ITEMS | Concrete delivery ticket requirement missing |
| X:applying:sufficiency | applying | sufficiency | Sufficient Deployment Evidence | 0 | NO_ITEMS | Deployment evidence framework sufficient |
| X:applying:completeness | applying | completeness | Full Deployment Record | 1 | HAS_ITEMS | As-built drawing requirement absent |
| X:applying:consistency | applying | consistency | Coherent Deployment Fidelity | 0 | NO_ITEMS | Deployment fidelity coherent across documents |
| X:judging:necessity | judging | necessity | Essential Judgment Fact | 1 | HAS_ITEMS | Service pit ventilation adequacy criteria absent |
| X:judging:sufficiency | judging | sufficiency | Sufficient Verdict Evidence | 0 | NO_ITEMS | Verification tables provide sufficient verdict evidence where defined |
| X:judging:completeness | judging | completeness | Complete Verdict Record | 0 | NO_ITEMS | Verification matrix in Specification covers all requirements |
| X:judging:consistency | judging | consistency | Reliable Verdict Coherence | 1 | HAS_ITEMS | Verification cross-reference inconsistency |
| X:reviewing:necessity | reviewing | necessity | Essential Audit Signal | 0 | NO_ITEMS | Audit signals (inspection reports, County copies) well defined |
| X:reviewing:sufficiency | reviewing | sufficiency | Sufficient Audit Evidence | 0 | NO_ITEMS | Records section provides sufficient audit evidence framework |
| X:reviewing:completeness | reviewing | completeness | Full Audit Record | 0 | NO_ITEMS | Audit record artifacts enumerated in Procedure Records |
| X:reviewing:consistency | reviewing | consistency | Consistent Audit Fidelity | 0 | NO_ITEMS | Audit fidelity consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:necessity | Conflict | Guidance | Multi | Resolve scope conflict: CONF-011-01-001 identifies the 50,000L water cistern inside the building footprint. Guidance identifies this as a conflict but no requirement in Specification addresses the structural provisions for the cistern (slab penetration, structural support). If the cistern is within DEL-011-01's structural envelope, structural provisions should appear as a requirement. | Guidance Conflict Table CONF-011-01-001 identifies this scope boundary issue. Specification scope exclusion table does not mention the cistern. No REQ addresses cistern structural provisions. This is a critical steering mandate gap — a major structural element may be missing from requirements. | Specification.md; Guidance.md | Spec: Scope (absent); Guidance: Conflict Table CONF-011-01-001 | Guidance.md#Conflict-Table (cistern structural interface acknowledged); Specification.md#Scope (cistern not mentioned) | PROPOSAL: Per CONF-011-01-001, structural rough-in under DEL-011-01, cistern supply/install under DEL-014-01. Add requirement for structural provisions. | TBD |
| X-002 | X:applying:necessity | MissingSlot | Procedure | Specification | Add requirement for concrete delivery tickets to be retained as quality records — essential delivery proof for concrete mix design traceability | Procedure Step 26 mentions "delivery tickets" in compile records but Specification Documentation table does not list delivery tickets as an artifact. Essential delivery proof for concrete requires mix design traceability through batch plant delivery tickets. | Procedure.md; Specification.md | Proc: Step 26; Spec: Documentation table | — | PROPOSAL: Add concrete delivery tickets to Specification Documentation artifacts | TBD |
| X-003 | X:applying:completeness | MissingSlot | Specification | Specification | Add requirement for structural as-built drawings (red-line markup of IFC drawings showing actual constructed conditions) — currently only as-built survey is referenced (DEL-008-04) for footprint confirmation | Specification Documentation lists installation records, inspection reports, and load verification but does not require as-built drawings. Procedure Step 24 references as-built survey for footprint but not as-built structural drawings. Full deployment record requires as-built drawing documentation. | Specification.md; Procedure.md | Spec: Documentation table; Proc: Step 24 | — | PROPOSAL: Add as-built structural drawings to Documentation artifacts | TBD |
| X-004 | X:judging:necessity | VerificationGap | Specification | Specification | Add verification criteria for service pit ventilation and lighting provisions (REQ-011-01-07) — requirement says "provisions for ventilation and lighting" but verification only says "Inspection prior to backfill/topping; dimensional check" without addressing ventilation/lighting adequacy | REQ-011-01-07 requires "provisions for ventilation and lighting" but the Verification table entry focuses only on dimensional inspection. No criterion addresses whether ventilation and lighting provisions (conduit sleeves, duct openings) are adequate. Essential judgment fact for this requirement is incomplete. | Specification.md | Spec: REQ-011-01-07, Verification table row 7 | — | PROPOSAL: Add verification criterion for ventilation/lighting sleeve/duct placement per MEP coordination drawings | TBD |
| X-005 | X:judging:consistency | Normalization | Datasheet | Datasheet | Normalize cross-references: Datasheet references "DEL-002-08" for steel plate embedment coordinates (Attributes — Steel plate embedments), but Specification REQ-011-01-05 references "DEL-002-08" for the embedment plan while Procedure Step 10 references "DEL-002-08 / DEL-011-02 scope." Clarify whether DEL-002-08 is the design drawing and DEL-011-02 is the installation tracking, and make this distinction consistent. | The relationship between DEL-002-08 (design) and DEL-011-02 (installation documentation) is implied but not consistently stated. This could cause confusion about which deliverable is the authority for embedment locations. | Datasheet.md; Specification.md; Procedure.md | DS: Attributes — Steel plate embedments; Spec: REQ-011-01-05; Proc: Step 10 | — | PROPOSAL: Guidance to add clarification note distinguishing DEL-002-08 (design) from DEL-011-02 (field tracking) | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Verified Guidance Datum | 0 | NO_ITEMS | Guidance data points verified against RFP and Appendix B |
| E:guiding:information | guiding | information | Coherent Steering Report | 0 | NO_ITEMS | Guidance Considerations provide coherent steering information |
| E:guiding:knowledge | guiding | knowledge | Integrated Steering Mastery | 1 | HAS_ITEMS | Roof structure scope needs clarification |
| E:guiding:wisdom | guiding | wisdom | Integrated Governance Wisdom | 0 | NO_ITEMS | Conflict table and trade-offs demonstrate governance wisdom |
| E:applying:data | applying | data | Verified Execution Record | 0 | NO_ITEMS | Execution records framework established |
| E:applying:information | applying | information | Coherent Execution Status | 0 | NO_ITEMS | Status reporting through inspections and milestones adequate |
| E:applying:knowledge | applying | knowledge | Integrated Execution Competence | 1 | HAS_ITEMS | Subcontractor qualification not addressed |
| E:applying:wisdom | applying | wisdom | Integrated Execution Judgment | 0 | NO_ITEMS | Trade-off analysis in Guidance shows execution judgment |
| E:judging:data | judging | data | Confirmed Ruling Record | 0 | NO_ITEMS | Ruling records (inspections, P.Eng. confirmations) defined |
| E:judging:information | judging | information | Coherent Ruling Account | 0 | NO_ITEMS | Verification table provides coherent ruling framework |
| E:judging:knowledge | judging | knowledge | Integrated Ruling Mastery | 0 | NO_ITEMS | Judgment criteria distributed appropriately across verification entries |
| E:judging:wisdom | judging | wisdom | Principled Ruling Insight | 0 | NO_ITEMS | Human ruling mechanism in Guidance Conflict Table preserves principled ruling |
| E:reviewing:data | reviewing | data | Confirmed Review Record | 0 | NO_ITEMS | Review records enumerated in Procedure Records |
| E:reviewing:information | reviewing | information | Coherent Review Account | 0 | NO_ITEMS | Inspection coordination log provides coherent review account |
| E:reviewing:knowledge | reviewing | knowledge | Integrated Scrutiny Mastery | 1 | HAS_ITEMS | 13,000 sq ft ambiguity unresolved in requirements |
| E:reviewing:wisdom | reviewing | wisdom | Principled Scrutiny Insight | 0 | NO_ITEMS | Documents show principled approach to gap identification |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:knowledge | WeakStatement | Datasheet | Guidance | Clarify roof structure scope: Datasheet Construction says "Roof structure — TBD per structural design" and Specification REQ-011-01-01 covers walls, columns, beams, and "roof structure" but the specific roof system (concrete, steel deck, pre-engineered) is not discussed in Guidance trade-offs. This is a significant structural system choice that lacks steering knowledge. | The roof structure is a major component of the superstructure but receives less analytical attention than the wall/column system. Guidance C1 discusses cast-in-place vs. tilt-up vs. precast for the structural frame but does not address the roof system as a separate design choice. Integrated steering mastery requires this. | Datasheet.md; Guidance.md | DS: Construction — Roof structure; Guidance: C1 | — | PROPOSAL: Add roof system as a consideration in Guidance C1 or as a new Consideration | TBD |
| E-002 | E:applying:knowledge | RationaleGap | Procedure | Guidance | Add rationale/guidance for structural subcontractor qualification requirements — Procedure addresses "General Contractor and their structural subcontractor(s)" but no document addresses what qualifications the structural subcontractor must hold | Procedure Purpose says the procedure "applies to the General Contractor and their structural subcontractor(s)." No document addresses subcontractor qualification (e.g., COR certification, concrete work experience, specific trade certifications). Integrated execution competence requires knowing who is qualified to perform the work. | Procedure.md | Proc: Purpose | — | PROPOSAL: Add to Guidance as a Consideration addressing subcontractor qualification expectations | TBD |
| E-003 | E:reviewing:knowledge | Conflict | Specification | Specification | Resolve CONF-011-01-002 in requirements: the 13,000 sq ft ambiguity (new addition only, or including renovated area) is identified in Guidance Conflict Table but REQ-011-01-02 uses "approximately 13,000 sq ft" without disambiguation. The requirement should state unambiguously which area is measured. | Guidance Conflict Table CONF-011-01-002 identifies this ambiguity and proposes that 13,000 sq ft refers to the new addition only. However, REQ-011-01-02 still carries the ambiguous language. Integrated scrutiny mastery requires the requirement itself to be unambiguous. | Specification.md; Guidance.md | Spec: REQ-011-01-02; Guidance: Conflict Table CONF-011-01-002 | Specification.md#REQ-011-01-02 ("approximately 13,000 sq ft"); Guidance.md#CONF-011-01-002 (proposes new addition only) | PROPOSAL: Per Guidance CONF-011-01-002, clarify REQ-011-01-02 to state "New North Shop addition" explicitly. Confirm with County. | TBD |
