# Semantic Lensing Register: DEL-03-05 Environmental Constraints, Flood Hazard & Regulatory Compliance

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/PKG-003_Site & Civil Works/1_Working/DEL-03-05_Environmental Constraints, Flood Hazard & Regulatory Compliance/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-03-05 identity, description, scope coverage (SOW-0102, SOW-0114), anticipated artifacts, open issues
- _STATUS.md — Current State: SEMANTIC_READY (last updated 2026-02-17)
- _SEMANTIC.md — Matrices A, B, C, F, D, X, E fully parsed (92 cells total)
- Datasheet.md — present; identification, attributes (site parcel, flood hazard, wetland/waterbody, environmental baseline), conditions, construction, references
- Specification.md — present; scope, REQ-3505-001 through REQ-3505-011, standards, verification, documentation
- Guidance.md — present; purpose, principles (5), considerations (6), trade-offs (3), examples, conflict table (2 entries)
- Procedure.md — present; production procedure (Steps A1-A7), implementation procedure (Steps B1-B5), prerequisites, verification, records
- _REFERENCES.md — present; 4 applicable references listed, open issue on floodway/fringe limits noted

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 19
- By document:
  - Datasheet: 4
  - Specification: 7
  - Guidance: 3
  - Procedure: 3
  - Multi: 2
- By matrix:
  - A: 5  B: 3  C: 2  F: 3  D: 2  X: 3  E: 1
- By type:
  - Conflict: 0
  - VerificationGap: 5
  - MissingSlot: 5
  - WeakStatement: 3
  - RationaleGap: 2
  - Normalization: 2
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 0 (2 conflicts already captured in Guidance.md conflict table; no new cross-document conflicts detected)
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Weak directive language on setback distances |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Missing mandatory setback distances |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Verification gap for fill placement |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulator coordination log and audit trail adequately addressed |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Missing procedure for Development Permit application |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Steps A1-A7 and B1-B5 adequately cover execution |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification tables in Specification and Procedure cover assessment |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records table in Procedure addresses audit trail |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | Rationale gap on OBJ-005/OBJ-008 linkage |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs in Guidance adequately address merit considerations |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Adequately addressed through avoidance hierarchy and trade-off analysis |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality assessment embedded in verification approach |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify whether setback distances from wetland boundaries (DW01, DW02, DW03, DD01, DD02, anthropogenic ditch) are prescriptive or to be determined by AEP approval conditions | REQ-3505-007 says "any required setbacks" but does not specify numeric setback distances or the source authority that will set them; this ambiguity could lead to different interpretations during design | Specification.md | REQ-3505-007 (Wetland/Setback Integration) | -- | AEP Water Act approval conditions; Town of Penhold | TBD |
| A-002 | A:normative:applying | MissingSlot | Datasheet | Datasheet | Add attribute row(s) for required setback distances from wetland boundaries, or record "TBD -- pending AEP approval conditions" | The Datasheet records wetland feature locations but not the setback distances that constrain site layout; this is a factual parameter that belongs in the Datasheet once known | Datasheet.md | Wetland/Waterbody Characteristics table | -- | AEP approval conditions | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add acceptance criteria for REQ-3505-010 (Fill Placement Compliance) specifying what evidence of Town/AEP acceptance constitutes verification | Verification table states "Confirm fill placement design reviewed by Town and AEP" but does not define what documentary evidence constitutes acceptable proof (e.g., written approval letter, stamped drawings, email confirmation) | Specification.md | Verification table -- REQ-3505-010 | -- | Design-Builder to propose; Owner to confirm | TBD |
| A-004 | A:operative:guiding | MissingSlot | Procedure | Procedure | Add procedural step for Town of Penhold Development Permit application, with timing relative to flood hazard confirmation (Step A3) and construction commencement | Guidance Consideration 6 identifies Development Permit as a prerequisite, and Procedure Step B1 references it, but no production step covers actually applying for or obtaining the Development Permit | Procedure.md | Part A (Steps A1-A7); Guidance Consideration 6 | -- | Design-Builder PM | TBD |
| A-005 | A:evaluative:guiding | RationaleGap | Guidance | Guidance | Add brief explanation of how this deliverable supports OBJ-005 and OBJ-008, including what outcomes those objectives target | _CONTEXT.md lists OBJ-005 and OBJ-008 as supported objectives, but Guidance does not explain how the deliverable contributes to achieving them; a reader cannot assess the value proposition without this context | Guidance.md | Purpose section | -- | Decomposition document (OBJ definitions) | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Missing factual record of Water Act application status |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Source citations in Datasheet are adequate |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Missing Waskasoo Creek setback/buffer distance |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Area measurements are consistent across documents |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key regulatory signals are present |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for each regulatory requirement is adequate |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Regulatory landscape is comprehensively described |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messages are coherent across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Flood hazard and wetland fundamentals adequately conveyed |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Required competencies listed in Procedure prerequisites |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Coverage of Alberta regulatory framework is thorough given available sources |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is consistent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 1 | HAS_ITEMS | Missing discernment on EPEA applicability |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-off analyses in Guidance provide adequate judgment |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view of constraints is adequately presented |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is consistent (avoidance hierarchy consistently applied) |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Current status of Water Act application (submitted / pending / approved / conditions issued) and date of last status check | This is an essential fact that gates construction (Principle 3 in Guidance, REQ-3505-005 in Specification) but is not recorded anywhere in the Datasheet; Consideration 1 in Guidance flags it as unresolved | Datasheet.md; Guidance.md | Datasheet -- Conditions table; Guidance -- Consideration 1 | -- | Town of Penhold / AEP | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add attribute for Waskasoo Creek minimum setback/buffer distance from project works, or record "TBD -- confirm with AEP/Town" | Waskasoo Creek is identified as the primary sensitive receiving water (Guidance Principle 5) and stormwater/sediment target, but no setback or buffer distance is recorded in the Datasheet; this is a binding spatial constraint if one exists | Datasheet.md | Environmental Baseline Characteristics table | -- | AEP / Town of Penhold | TBD |
| B-003 | B:wisdom:necessity | WeakStatement | Specification | Specification | Clarify applicability statement for Alberta EPEA and Public Lands Act in Standards table; either confirm applicability or remove with rationale | Standards table lists "Alberta Public Lands Act / Environmental Protection and Enhancement Act" with "May impose additional environmental obligations depending on project footprint" and accessibility "Not directly accessed -- location TBD; ASSUMPTION: potentially applicable"; this vague statement does not provide actionable direction | Specification.md | Standards table -- Alberta Public Lands Act / EPEA row | -- | Environmental consultant / AEP | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | regulatory imperative | 1 | HAS_ITEMS | Nesting season restriction needs specification-level treatment |
| C:normative:sufficiency | normative | sufficiency | compliance substantiation | 0 | NO_ITEMS | Compliance substantiation approach is adequate in Verification table |
| C:normative:completeness | normative | completeness | exhaustive regulatory coverage | 0 | NO_ITEMS | Regulatory landscape is comprehensively covered given available sources |
| C:normative:consistency | normative | consistency | coherent regulatory alignment | 0 | NO_ITEMS | Regulatory references are consistent across documents |
| C:operative:necessity | operative | necessity | operational readiness threshold | 1 | HAS_ITEMS | Missing erosion/sediment control timing |
| C:operative:sufficiency | operative | sufficiency | competent execution assurance | 0 | NO_ITEMS | Step-level detail in Procedure is sufficient for competent execution |
| C:operative:completeness | operative | completeness | comprehensive process accounting | 0 | NO_ITEMS | Both production and implementation workflows covered |
| C:operative:consistency | operative | consistency | standardized process discipline | 0 | NO_ITEMS | Process steps are consistent with verification checks |
| C:evaluative:necessity | evaluative | necessity | foundational value recognition | 0 | NO_ITEMS | Avoidance hierarchy establishes foundational value |
| C:evaluative:sufficiency | evaluative | sufficiency | credible value appraisal | 0 | NO_ITEMS | Trade-off analyses provide credible appraisal |
| C:evaluative:completeness | evaluative | completeness | holistic value accounting | 0 | NO_ITEMS | Value accounting is adequate through principles and trade-offs |
| C:evaluative:consistency | evaluative | consistency | principled value coherence | 0 | NO_ITEMS | Alberta Wetland Policy hierarchy consistently applied |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | VerificationGap | Specification | Specification | Add specific requirement for migratory bird nesting season restriction (approximately April 1 -- August 31) as a normative constraint on vegetation clearing timing, with verification approach | REQ-3505-008 mentions "nesting season awareness" and Procedure Step B2 references it, but no standalone requirement establishes the nesting season window as a binding constraint; the Specification verification table lacks a corresponding entry for nesting season compliance | Specification.md; Procedure.md | REQ-3505-008; Procedure Verification table (nesting season row exists but lacks a corresponding REQ) | -- | Alberta Wildlife Act; Migratory Birds Convention Act | TBD |
| C-002 | C:operative:necessity | MissingSlot | Procedure | Procedure | Add explicit step for installation timing of erosion and sediment control measures relative to ground disturbance commencement (currently referenced only in Step A6 mitigation notes and Step B2 monitoring) | Step A6 Section 4 drafts erosion/sediment control notes and Step B2 monitors them, but no production step covers the actual installation of erosion/sediment control measures before ground disturbance; this is an operational readiness threshold | Procedure.md | Steps A6 and B2 | -- | Site Superintendent / Environmental monitor | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | mandatory compliance authority | 1 | HAS_ITEMS | AEP name inconsistency |
| F:normative:sufficiency | normative | sufficiency | sufficient prescriptive competence | 0 | NO_ITEMS | Prescriptive competence is sufficient across requirements |
| F:normative:completeness | normative | completeness | total regulatory obligation scope | 1 | HAS_ITEMS | Missing requirement for Alberta Wildlife Act |
| F:normative:consistency | normative | consistency | uniform regulatory discipline | 1 | HAS_ITEMS | Inconsistent AEP naming |
| F:operative:necessity | operative | necessity | prerequisite operational awareness | 0 | NO_ITEMS | Prerequisites are clearly stated in Procedure |
| F:operative:sufficiency | operative | sufficiency | adequate operational competence | 0 | NO_ITEMS | Competency requirements stated in Procedure |
| F:operative:completeness | operative | completeness | complete operational mastery | 0 | NO_ITEMS | Procedure covers both production and implementation |
| F:operative:consistency | operative | consistency | uniform procedural standard | 0 | NO_ITEMS | Procedural steps are internally consistent |
| F:evaluative:necessity | evaluative | necessity | essential value judgment | 0 | NO_ITEMS | Value judgments are grounded in policy hierarchy |
| F:evaluative:sufficiency | evaluative | sufficiency | defensible value assessment | 0 | NO_ITEMS | Trade-off analysis provides defensible assessment |
| F:evaluative:completeness | evaluative | completeness | comprehensive worth inventory | 0 | NO_ITEMS | Worth considerations adequately inventoried |
| F:evaluative:consistency | evaluative | consistency | coherent worth standard | 0 | NO_ITEMS | Worth standards are coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | Normalization | Multi | Guidance | Standardize naming of the Alberta provincial environmental regulator: documents use both "Alberta Environment and Parks (AEP)" and "Alberta Environment and Protected Areas (AEP)" and "Alberta Environment and Protected Areas (formerly AEP)"; establish one canonical name with note on name change | The ministry was renamed; using multiple names risks confusion about whether different entities are being referenced; a single canonical term with a parenthetical note on the former name would prevent drift | Datasheet.md; Specification.md; Procedure.md | Datasheet -- Conditions table (Fill Placement Constraint); Specification -- REQ-3505-005, REQ-3505-011; Procedure -- Steps A2, B1 | -- | Current Government of Alberta ministry name | TBD |
| F-002 | F:normative:completeness | MissingSlot | Specification | Specification | Add requirement or standards reference for Alberta Wildlife Act / Migratory Birds Convention Act obligations related to nesting season vegetation clearing restrictions | Procedure Step B2 and Guidance Consideration 4 reference nesting season obligations, and Specification REQ-3505-008 mentions "wildlife disturbance mitigation" but no standalone requirement or standards entry addresses the specific legislative basis (Alberta Wildlife Act, Migratory Birds Convention Act) | Specification.md | Standards table; REQ-3505-008 | -- | Alberta Wildlife Act; federal Migratory Birds Convention Act | TBD |
| F-003 | F:normative:consistency | Normalization | Multi | Multi | Harmonize the naming of the anthropogenic ditch: Datasheet calls it "Anthropogenic Ditch (LC_20210520_045)" while Specification REQ-3505-007 lists it as "the anthropogenic ditch" without the field code; standardize to include both the common name and the field code consistently | Inconsistent naming of this feature across documents could cause confusion during field integration, particularly when comparing against the Wetland Assessment source document which uses the field code | Datasheet.md; Specification.md | Datasheet -- Wetland/Waterbody Characteristics; Specification -- REQ-3505-007 | -- | Wetland Assessment field nomenclature | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | established regulatory directive | 0 | NO_ITEMS | Regulatory directives are established across documents |
| D:normative:applying | normative | applying | enforced compliance practice | 0 | NO_ITEMS | Compliance practices are enforced through requirements |
| D:normative:judging | normative | judging | authoritative obligation ruling | 0 | NO_ITEMS | Obligations are clearly stated and sourced |
| D:normative:reviewing | normative | reviewing | settled compliance oversight | 0 | NO_ITEMS | Oversight mechanisms in Procedure are adequate |
| D:operative:guiding | operative | guiding | settled procedural guidance | 1 | HAS_ITEMS | Timing dependency between deliverables |
| D:operative:applying | operative | applying | confirmed execution delivery | 0 | NO_ITEMS | Execution delivery is confirmed through step-level detail |
| D:operative:judging | operative | judging | settled performance verdict | 0 | NO_ITEMS | Performance assessment is covered in verification tables |
| D:operative:reviewing | operative | reviewing | settled process conformity review | 0 | NO_ITEMS | Process conformity review is adequate |
| D:evaluative:guiding | evaluative | guiding | principled worth direction | 0 | NO_ITEMS | Worth direction established through avoidance hierarchy |
| D:evaluative:applying | evaluative | applying | justified merit enactment | 0 | NO_ITEMS | Merit enactment justified through trade-off analysis |
| D:evaluative:judging | evaluative | judging | settled value determination | 1 | HAS_ITEMS | Replacement fee currency question |
| D:evaluative:reviewing | evaluative | reviewing | settled quality assessment | 0 | NO_ITEMS | Quality assessment is settled through verification approach |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:operative:guiding | RationaleGap | Guidance | Guidance | Add explicit guidance on the timing dependency between this deliverable and DEL-03-02 (Grading, Earthworks, Drainage & Stormwater) -- specifically, which outputs from DEL-03-05 must be available before DEL-03-02 design can proceed, and vice versa | Consideration 5 notes the interface but does not specify the sequencing: must the flood hazard constraints map be finalized before DEL-03-02 grading design proceeds, or can they proceed concurrently? This is a procedural guidance gap that affects project scheduling | Guidance.md | Consideration 5 | -- | Design-Builder PM | TBD |
| D-002 | D:evaluative:judging | TBD_Question | Specification | Specification | Record TBD: Confirm current ABWRET-A wetland replacement fee with AEP; the $10,769.54 figure is from August 2021 and may have changed | REQ-3505-006 specifies payment of "$10,769.54" and includes a note to "confirm current fee determination with AEP prior to payment," but this remains an unresolved TBD that affects budget and compliance verification; the value determination is not settled until current fee is confirmed | Specification.md | REQ-3505-006 (Wetland Replacement Fee) | -- | AEP fee schedule | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | foundational directive authority | 0 | NO_ITEMS | Directives are authoritatively established |
| X:guiding:sufficiency | guiding | sufficiency | adequate governance confidence | 0 | NO_ITEMS | Governance approach is adequate |
| X:guiding:completeness | guiding | completeness | exhaustive governance scope | 0 | NO_ITEMS | Governance scope is comprehensive |
| X:guiding:consistency | guiding | consistency | harmonized directive coherence | 0 | NO_ITEMS | Directives are coherent across documents |
| X:applying:necessity | applying | necessity | prerequisite compliance action | 1 | HAS_ITEMS | Missing verification for prerequisite clearance |
| X:applying:sufficiency | applying | sufficiency | demonstrated practice adequacy | 0 | NO_ITEMS | Practice adequacy is demonstrated through step detail |
| X:applying:completeness | applying | completeness | comprehensive practice fulfillment | 1 | HAS_ITEMS | Missing as-built map update verification |
| X:applying:consistency | applying | consistency | consistent practice integrity | 0 | NO_ITEMS | Practice integrity is consistent |
| X:judging:necessity | judging | necessity | essential conformance judgment | 0 | NO_ITEMS | Conformance judgments are essential and present |
| X:judging:sufficiency | judging | sufficiency | defensible adjudication basis | 0 | NO_ITEMS | Adjudication basis is defensible |
| X:judging:completeness | judging | completeness | exhaustive adjudication scope | 1 | HAS_ITEMS | Missing closeout verification |
| X:judging:consistency | judging | consistency | principled adjudication coherence | 0 | NO_ITEMS | Adjudication is coherent |
| X:reviewing:necessity | reviewing | necessity | fundamental oversight scrutiny | 0 | NO_ITEMS | Oversight scrutiny is fundamental and present |
| X:reviewing:sufficiency | reviewing | sufficiency | adequate verification confidence | 0 | NO_ITEMS | Verification confidence is adequate |
| X:reviewing:completeness | reviewing | completeness | exhaustive audit coverage | 0 | NO_ITEMS | Audit coverage is comprehensive |
| X:reviewing:consistency | reviewing | consistency | principled audit integrity | 0 | NO_ITEMS | Audit integrity is principled |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | VerificationGap | Specification | Procedure | Add verification check confirming that all regulatory prerequisites (Water Act approval, Development Permit, fill placement acceptance) are documented as received before ground disturbance commences in affected areas | Procedure Step B1 lists pre-construction clearance activities but there is no single verification checkpoint that confirms all prerequisites are met; a formal gate review before construction mobilization in environmentally constrained areas would close this gap | Specification.md; Procedure.md | Specification Verification table; Procedure Step B1 | -- | Design-Builder PM / Owner | TBD |
| X-002 | X:applying:completeness | VerificationGap | Specification | Specification | Add verification approach for Step B5 closeout requirement: confirm flood hazard constraints map updated to reflect as-built conditions and confirmed flood limits at project closeout | Procedure Step B5 requires the flood hazard constraints map to be updated to reflect as-built conditions, but the Specification verification table only addresses the initial production of the map (REQ-3505-003) and confirmation of limits (REQ-3505-004), not the as-built update | Specification.md; Procedure.md | Specification Verification -- REQ-3505-003; Procedure Step B5 | -- | Design-Builder civil engineer | TBD |
| X-003 | X:judging:completeness | VerificationGap | Specification | Specification | Add verification approach for post-construction AEP condition compliance (Procedure Step B4): confirm all AEP conditions of approval have been satisfied and closed out with AEP confirmation | Procedure Step B4 requires post-construction condition compliance and AEP confirmation, but the Specification verification table does not include a corresponding verification entry for closeout of AEP conditions | Specification.md; Procedure.md | Specification Verification table (no entry for B4 closeout); Procedure Step B4 | -- | AEP / Design-Builder environmental consultant | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | enforceable regulatory foundation | 0 | NO_ITEMS | Regulatory foundation is enforceable and well-established |
| E:normative:sufficiency | normative | sufficiency | defensible governance assurance | 0 | NO_ITEMS | Governance assurance is defensible |
| E:normative:completeness | normative | completeness | total regulatory jurisdiction | 1 | HAS_ITEMS | Alberta Wildlife Act gap |
| E:normative:consistency | normative | consistency | coherent normative architecture | 0 | NO_ITEMS | Normative architecture is coherent |
| E:operative:necessity | operative | necessity | prerequisite conformance foundation | 0 | NO_ITEMS | Conformance prerequisites are established |
| E:operative:sufficiency | operative | sufficiency | sufficient performance evidence | 0 | NO_ITEMS | Performance evidence approach is sufficient |
| E:operative:completeness | operative | completeness | total operational fulfillment | 0 | NO_ITEMS | Operational fulfillment is comprehensive |
| E:operative:consistency | operative | consistency | unified operational discipline | 0 | NO_ITEMS | Operational discipline is unified across documents |
| E:evaluative:necessity | evaluative | necessity | fundamental value authority | 0 | NO_ITEMS | Value authority grounded in Alberta Wetland Policy |
| E:evaluative:sufficiency | evaluative | sufficiency | credible value stewardship | 0 | NO_ITEMS | Value stewardship is credible through trade-off analysis |
| E:evaluative:completeness | evaluative | completeness | comprehensive value fulfillment | 0 | NO_ITEMS | Value fulfillment adequately addressed |
| E:evaluative:consistency | evaluative | consistency | principled value architecture | 0 | NO_ITEMS | Value architecture is principled and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:completeness | WeakStatement | Specification | Specification | Strengthen the Standards table entry for "Alberta OHS Code" -- either clarify specific OHS obligations relevant to environmental constraint work (e.g., working near waterbodies, wildlife encounters) or remove if covered by DEL-01-03 H&S Plan | The Standards table entry for Alberta OHS Code states "General contractor health and safety obligations during construction near waterbodies" with an assumption of applicability "per SOW-0008"; this is too vague to constitute total regulatory jurisdiction -- either it belongs here with specifics or it is better addressed in the H&S deliverable | Specification.md | Standards table -- Alberta OHS Code row | -- | Design-Builder H&S lead / cross-reference DEL-01-03 | TBD |
