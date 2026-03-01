# Semantic Lensing Register: DEL-007-03 Planting & Restoration Plans

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-007_Landscape Architectural Design/1_Working/DEL-007-03_Planting-Plans/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-007-03_Planting-Plans/_CONTEXT.md (Deliverable Identity, Scope of Work Reference, Context Information)
- _STATUS.md — DEL-007-03_Planting-Plans/_STATUS.md (State: SEMANTIC_READY, Last Updated: 2026-02-26)
- _SEMANTIC.md — DEL-007-03_Planting-Plans/_SEMANTIC.md (Matrices A, B, C, F, D, X, E extracted)
- Datasheet.md — DEL-007-03_Planting-Plans/Datasheet.md (Identification, Attributes, Conditions, Construction, References)
- Specification.md — DEL-007-03_Planting-Plans/Specification.md (Scope, Requirements REQ-007-03-001 through -012, Standards, Verification, Documentation)
- Guidance.md — DEL-007-03_Planting-Plans/Guidance.md (Purpose, Principles P-1 through P-5, Considerations, Trade-offs, Conflict Table)
- Procedure.md — DEL-007-03_Planting-Plans/Procedure.md (Prerequisites, Steps 1-6, Verification, Records)
- _REFERENCES.md — DEL-007-03_Planting-Plans/_REFERENCES.md (Source Documents, Related Deliverables, Standards & Guidelines)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 29
- By document:
  - Datasheet: 4
  - Specification: 11
  - Guidance: 5
  - Procedure: 7
  - Multi: 2
- By matrix:
  - A: 5  B: 4  C: 3  F: 4  D: 3  X: 5  E: 5
- By type:
  - Conflict: 0
  - VerificationGap: 6
  - MissingSlot: 8
  - WeakStatement: 5
  - RationaleGap: 4
  - Normalization: 3
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 0 (2 conflicts already captured in Guidance.md Conflict Table; not duplicated here)
- Matrix parse errors: 0

---

## Matrix A — Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Standards table has multiple TBD entries |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Plant palette and density values TBD |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Verification approach for standards compliance is weak |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | County approval gate and IFC stamp review addressed adequately |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Ecological assessment step flagged as assumption |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Steps 1-6 provide adequate execution direction |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | No measurable performance criteria for vegetation establishment |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records section adequately covers audit trail |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance principles P-1 through P-5 provide adequate value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs section addresses merit balancing |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Guarantee period provides worth determination framework |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Verification table in Procedure covers quality appraisal |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Record TBD: Identify specific landscape-applicable standards/codes (Alberta Building Code landscape clauses, municipal bylaws, AALA standards) to replace generic TBD entries in Standards table | The Standards table lists five entries with "specific standard TBD" or "specific clauses TBD" -- prescriptive direction cannot be established without identifying the governing standards | Specification.md | ## Standards | -- | PROPOSAL: Landscape Architect to identify applicable standards; confirm with County | TBD |
| A-002 | A:normative:applying | TBD_Question | Datasheet | Datasheet | Record TBD: Confirm plant species selection, planting density/spacing, restoration phasing, and maintenance protocol values currently listed as TBD | Four critical mandatory practice parameters are TBD in the Datasheet Attributes table, blocking normative application of planting requirements | Datasheet.md | ## Attributes | -- | PROPOSAL: Landscape Architect to develop after site assessment | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add verification approach for standards compliance -- currently no method to confirm adherence to unidentified standards | REQ-007-03-005 through -008 rely on standards that are TBD; verification approaches reference "applicable native plant guidelines" and "standard conventions" without specifying what is being verified against | Specification.md | ## Verification | -- | PROPOSAL: Specification | TBD |
| A-004 | A:operative:guiding | WeakStatement | Procedure | Guidance | Clarify whether Step 1.2 ecological assessment is within scope or optional -- currently flagged as "ASSUMPTION based on standard landscape practice" | Procedural direction for Step 1 depends on whether an ecological assessment is in scope; the RFP does not explicitly require one, and the Procedure notes this, but does not resolve the question | Procedure.md | ### Step 1 — Site Context and Ecological Assessment | -- | PROPOSAL: Confirm with project team whether ecological assessment is in proponent scope | TBD |
| A-005 | A:operative:judging | MissingSlot | Specification | Specification | Add measurable performance criteria for vegetation establishment success (e.g., survival rate percentage, coverage percentage at defined intervals) | No quantitative performance assessment criteria exist for planting/restoration outcomes; verification relies on qualitative review only | Specification.md; Procedure.md | ## Verification; ## Verification | -- | PROPOSAL: Landscape Architect to propose criteria consistent with guarantee period obligations | TBD |

---

## Matrix B — Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Site soil data absent |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Climate zone stated as assumption |
| B:data:completeness | data | completeness | comprehensive record | 0 | NO_ITEMS | Datasheet provides comprehensive record of known parameters |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurement data not yet applicable at this stage |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Landfill regulatory constraints on planting unconfirmed |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequately provided across documents |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Documents together provide comprehensive account of scope |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology inconsistency for professional stamp |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Core landscape architecture knowledge framework present |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Documents appropriately defer to Landscape Architect expertise |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Documents acknowledge TBDs without claiming mastery |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent where present |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Conflict table and trade-offs demonstrate discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-off discussion adequate for current stage |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance provides holistic perspective on design decisions |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Principles P-1 through P-5 provide principled reasoning framework |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add essential site soil data (soil type, pH, compaction, contamination status) as TBD attributes requiring site assessment | No soil characterization data exists in any document; soil conditions are a fundamental fact for plant selection and restoration design, yet only mentioned as an assumption in Guidance Considerations | Datasheet.md; Guidance.md | ## Attributes; ### Site Context — Active Landfill Compound | -- | PROPOSAL: Landscape Architect site assessment | TBD |
| B-002 | B:data:sufficiency | WeakStatement | Datasheet | Datasheet | Strengthen climate zone attribution -- currently stated as "ASSUMPTION: Koppen BSk/Dfb transition" without citing a definitive source or hardiness zone | The climate zone classification drives plant palette selection but is stated as an assumption with no authoritative citation; Procedure Step 2.1 repeats this as "likely Canadian zone 3b-4a" -- also an assumption | Datasheet.md; Procedure.md | ## Conditions; ### Step 2 — Plant Palette Development | -- | PROPOSAL: Confirm hardiness zone from authoritative Canadian plant hardiness zone data | TBD |
| B-003 | B:information:necessity | TBD_Question | Guidance | Guidance | Record TBD: Determine whether landfill regulatory constraints restrict planting near waste cells, leachate systems, or gas migration zones within or adjacent to expansion area | Guidance Considerations section raises landfill regulatory context as a potential constraint but notes "No specific landfill-specific planting restrictions are stated in the RFP" -- this is an essential signal that must be resolved before planting zone design | Guidance.md | ### Landfill Regulatory Context | -- | PROPOSAL: Landscape Architect to consult with County and landfill operator | TBD |
| B-004 | B:information:consistency | Normalization | Multi | Guidance | Normalize terminology for professional stamp across documents: "P.Eng." vs "RLA" vs "RLA/AAL" vs "registered Landscape Architect" used inconsistently | The stamp requirement uses different terms across documents -- Specification REQ-009 says "professional engineer," Guidance says "RLA/AAL," Procedure says "P.Eng. or RLA" -- while the conflict is captured in CONF-007-03-001, the underlying terminology is not normalized | Specification.md; Guidance.md; Procedure.md | REQ-007-03-009; ### Drawing Set Completeness for IFC; ### Step 6 | -- | PROPOSAL: Normalize after CONF-007-03-001 ruling | TBD |

---

## Matrix C — Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Obligatory Governance Basis | 1 | HAS_ITEMS | Governance basis incomplete without identified standards |
| C:normative:sufficiency | normative | sufficiency | Defensible Compliance Method | 0 | NO_ITEMS | Verification table provides defensible methods for stated requirements |
| C:normative:completeness | normative | completeness | Total Regulatory Coverage | 1 | HAS_ITEMS | Regulatory coverage cannot be total with TBD standards |
| C:normative:consistency | normative | consistency | Uniform Regulatory Alignment | 0 | NO_ITEMS | Regulatory references are consistently cited where present |
| C:operative:necessity | operative | necessity | Critical Operational Foundation | 0 | NO_ITEMS | Procedure Steps 1-6 establish adequate operational foundation |
| C:operative:sufficiency | operative | sufficiency | Capable Execution Assurance | 0 | NO_ITEMS | Procedure provides capable execution pathway |
| C:operative:completeness | operative | completeness | Complete Process Mastery | 1 | HAS_ITEMS | Drawing standards not specified |
| C:operative:consistency | operative | consistency | Standardized Operational Coherence | 0 | NO_ITEMS | Procedure steps are internally coherent |
| C:evaluative:necessity | evaluative | necessity | Inherent Value Discernment | 0 | NO_ITEMS | Value framework established through principles and trade-offs |
| C:evaluative:sufficiency | evaluative | sufficiency | Warranted Quality Judgment | 0 | NO_ITEMS | Quality judgment framework adequate for current stage |
| C:evaluative:completeness | evaluative | completeness | Exhaustive Value Accounting | 0 | NO_ITEMS | Value accounting proportionate to deliverable maturity |
| C:evaluative:consistency | evaluative | consistency | Principled Value Coherence | 0 | NO_ITEMS | Value principles coherent across Guidance |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | RationaleGap | Specification | Guidance | Add rationale for why REQ-007-03-006 (plant schedule) and REQ-007-03-008 (planting details) are sourced as "ASSUMPTION based on standard drawing set conventions" rather than from an explicit RFP or standard requirement | These two requirements form part of the obligatory governance basis but are self-declared assumptions -- the rationale for their inclusion (and their expected scope) should be explicit to support defensibility | Specification.md | ### REQ-007-03-006; ### REQ-007-03-008 | -- | PROPOSAL: Guidance document rationale section | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add requirement or note addressing municipal/county landscape bylaws or approvals beyond the preliminary design gate (REQ-007-03-012) | Total regulatory coverage requires considering whether Camrose County has landscape bylaws, development permit conditions, or environmental setback requirements applicable to the landfill site -- none are mentioned | Specification.md; Guidance.md | ## Standards; ## Considerations | -- | PROPOSAL: Landscape Architect to confirm with County | TBD |
| C-003 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add reference to project drawing standards (title block format, scale conventions, layer naming, file format) applicable to the drawing set | Step 4 instructs drawing production but does not reference any project-level drawing standards or CAD standards -- complete process mastery requires knowing the format expectations | Procedure.md | ### Step 4 — Drawing Set Production | -- | PROPOSAL: Project team to provide drawing standards | TBD |

---

## Matrix F — Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandatory Compliance Literacy | 1 | HAS_ITEMS | Compliance literacy incomplete for unidentified standards |
| F:normative:sufficiency | normative | sufficiency | Justified Prescriptive Adequacy | 0 | NO_ITEMS | Requirements justified with source citations |
| F:normative:completeness | normative | completeness | Thorough Prescriptive Command | 1 | HAS_ITEMS | Missing requirement for erosion/sediment control |
| F:normative:consistency | normative | consistency | Harmonized Prescriptive Order | 1 | HAS_ITEMS | Objectives mapping is assumption-based |
| F:operative:necessity | operative | necessity | Fundamental Execution Awareness | 0 | NO_ITEMS | Procedure prerequisites establish execution awareness |
| F:operative:sufficiency | operative | sufficiency | Proficient Process Control | 0 | NO_ITEMS | Process control adequate through coordination steps |
| F:operative:completeness | operative | completeness | Comprehensive Operational Authority | 1 | HAS_ITEMS | No acceptance criteria for restoration methodology |
| F:operative:consistency | operative | consistency | Systematic Execution Reliability | 0 | NO_ITEMS | Steps are systematically ordered and consistent |
| F:evaluative:necessity | evaluative | necessity | Inherent Merit Awareness | 0 | NO_ITEMS | Merit awareness reflected in trade-offs |
| F:evaluative:sufficiency | evaluative | sufficiency | Justified Quality Determination | 0 | NO_ITEMS | Quality determination framework adequate |
| F:evaluative:completeness | evaluative | completeness | Complete Worth Authority | 0 | NO_ITEMS | Worth framework proportionate |
| F:evaluative:consistency | evaluative | consistency | Principled Quality Consistency | 0 | NO_ITEMS | Quality consistency maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | WeakStatement | Specification | Specification | Strengthen the note under Standards table -- "No landscape-specific standards or codes are explicitly cited in the RFP" should trigger a TBD action to identify which standards actually govern, not just acknowledge their absence | Mandatory compliance literacy requires knowing what must be complied with; the current note acknowledges absence but does not commit to resolution | Specification.md | ## Standards (Note) | -- | PROPOSAL: Landscape Architect to resolve before IFC | TBD |
| F-002 | F:normative:completeness | MissingSlot | Specification | Specification | Add requirement addressing erosion and sediment control during and immediately after construction, prior to vegetation establishment | REQ-007-03-003 addresses grading integration and REQ-007-03-007 addresses restoration phasing, but no requirement addresses interim erosion control between construction disturbance and vegetation establishment -- a prescriptive gap given the disturbed site context | Specification.md; Guidance.md | ## Requirements; ### Site Context — Active Landfill Compound | -- | PROPOSAL: Specification (normative) | TBD |
| F-003 | F:normative:consistency | WeakStatement | Datasheet | Datasheet | Clarify objectives mapping -- "ASSUMPTION: best-effort mapping per PKG-007 package-grouping heuristic; not confirmed at deliverable-ID level" for OBJ-001 and OBJ-003 | Harmonized prescriptive order requires that requirement traceability to objectives be confirmed rather than assumed; this weakens the requirements chain | Datasheet.md | ## Identification | -- | PROPOSAL: Confirm with project team | TBD |
| F-004 | F:operative:completeness | VerificationGap | Specification | Specification | Add acceptance criteria for restoration methodology (Step 3.4 in Procedure) -- currently no verification approach for soil preparation, seeding method, or establishment care requirements | REQ-007-03-007 requires a restoration strategy and phasing plan but the Verification table only checks for "phasing diagram present" -- the restoration methodology content (soil prep, seeding method, spacing) has no verification approach | Specification.md; Procedure.md | ## Verification (REQ-007-03-007); ### Step 3 | -- | PROPOSAL: Specification verification table | TBD |

---

## Matrix D — Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Established Directive Authority | 0 | NO_ITEMS | Directive authority established through RFP and DECOMP citations |
| D:normative:applying | normative | applying | Finalized Obligatory Execution | 1 | HAS_ITEMS | Cannot finalize execution without plant palette |
| D:normative:judging | normative | judging | Conclusive Conformance Verdict | 0 | NO_ITEMS | Verification table provides conformance verdict framework |
| D:normative:reviewing | normative | reviewing | Settled Compliance Reconciliation | 0 | NO_ITEMS | County approval gate provides reconciliation mechanism |
| D:operative:guiding | operative | guiding | Resolved Workflow Guidance | 0 | NO_ITEMS | Procedure steps provide resolved workflow |
| D:operative:applying | operative | applying | Finalized Operational Competence | 0 | NO_ITEMS | Operational steps sufficiently detailed for current stage |
| D:operative:judging | operative | judging | Concluded Capability Verdict | 1 | HAS_ITEMS | Personnel qualification criteria incomplete |
| D:operative:reviewing | operative | reviewing | Settled Workflow Assurance | 0 | NO_ITEMS | Records section provides workflow assurance |
| D:evaluative:guiding | evaluative | guiding | Established Merit Direction | 0 | NO_ITEMS | Principles establish merit direction |
| D:evaluative:applying | evaluative | applying | Finalized Worth Realization | 1 | HAS_ITEMS | Budget/cost constraints absent |
| D:evaluative:judging | evaluative | judging | Conclusive Value Ruling | 0 | NO_ITEMS | Trade-offs section provides value ruling framework |
| D:evaluative:reviewing | evaluative | reviewing | Settled Merit Reconciliation | 0 | NO_ITEMS | Guarantee period provides merit reconciliation mechanism |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | RationaleGap | Guidance | Guidance | Add rationale explaining how the design-build contract structure (CCDC 14-2013) affects the Landscape Architect's authority to finalize plant species and quantities -- i.e., whether the proponent has latitude to set the palette or whether County input constrains it beyond the preliminary design gate | The documents establish a County approval gate for preliminary design but do not explain the decision authority for final species selection and quantities under the design-build delivery model | Guidance.md; Specification.md | ## Principles; ### REQ-007-03-005 | -- | PROPOSAL: Guidance | TBD |
| D-002 | D:operative:judging | MissingSlot | Procedure | Procedure | Add qualification criteria or minimum competency requirements for the Landscape Architect (e.g., AALA membership, years of experience with restoration projects, familiarity with central Alberta plant communities) | Personnel/Expertise table states "Registered professional with expertise in central Alberta native plant communities" but this is descriptive, not verifiable -- no capability verdict can be concluded without measurable criteria | Procedure.md | ### Personnel/Expertise Required | -- | PROPOSAL: Procedure or Specification | TBD |
| D-003 | D:evaluative:applying | RationaleGap | Guidance | Guidance | Add discussion of budget or cost constraints as a factor in restoration depth vs. project cost trade-off -- currently the trade-off is described without reference to any budget envelope or cost target | The Restoration Depth vs. Project Cost trade-off acknowledges cost as a factor but provides no reference to actual budget constraints, making finalized worth realization impossible to assess | Guidance.md | ### Restoration Depth vs. Project Cost | -- | PROPOSAL: Project team to provide landscape budget allocation | TBD |

---

## Matrix X — Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Vital Instructional Foundation | 0 | NO_ITEMS | Instructional foundation established through Guidance principles |
| X:guiding:sufficiency | guiding | sufficiency | Warranted Directional Support | 1 | HAS_ITEMS | No verification that guidance principles were followed in design |
| X:guiding:completeness | guiding | completeness | Exhaustive Guidance Authority | 0 | NO_ITEMS | Guidance coverage adequate for current scope |
| X:guiding:consistency | guiding | consistency | Consistent Guidance Harmony | 0 | NO_ITEMS | Guidance internally consistent |
| X:applying:necessity | applying | necessity | Core Competence Evidence | 1 | HAS_ITEMS | No evidence collection for species selection rationale |
| X:applying:sufficiency | applying | sufficiency | Proficient Enactment Evidence | 0 | NO_ITEMS | Verification table provides enactment checks |
| X:applying:completeness | applying | completeness | Complete Enactment Authority | 1 | HAS_ITEMS | No verification for drawing completeness against SOW-0017 checklist |
| X:applying:consistency | applying | consistency | Reliable Enactment Coherence | 0 | NO_ITEMS | Cross-reference checks adequately described |
| X:judging:necessity | judging | necessity | Critical Conformance Basis | 0 | NO_ITEMS | Conformance basis established through requirements traceability |
| X:judging:sufficiency | judging | sufficiency | Informed Adjudication Evidence | 1 | HAS_ITEMS | Guarantee period verification lacks interim checkpoints |
| X:judging:completeness | judging | completeness | Exhaustive Assessment Authority | 0 | NO_ITEMS | Assessment coverage adequate for stated requirements |
| X:judging:consistency | judging | consistency | Consistent Ruling Alignment | 0 | NO_ITEMS | Verification approaches consistently structured |
| X:reviewing:necessity | reviewing | necessity | Fundamental Audit Basis | 0 | NO_ITEMS | Records section establishes audit basis |
| X:reviewing:sufficiency | reviewing | sufficiency | Informed Audit Confidence | 1 | HAS_ITEMS | Drawing revision log lacks required content definition |
| X:reviewing:completeness | reviewing | completeness | Comprehensive Inspection Authority | 0 | NO_ITEMS | Inspection coverage adequate |
| X:reviewing:consistency | reviewing | consistency | Reliable Inspection Coherence | 0 | NO_ITEMS | Inspection approaches coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | VerificationGap | Specification | Procedure | Add verification step confirming that the final planting plan design was reviewed against Guidance principles P-1 through P-5 | Warranted directional support requires evidence that the guidance principles were actually applied; no verification step links the final design back to the principles | Specification.md; Guidance.md | ## Verification; ## Principles | -- | PROPOSAL: Procedure verification table | TBD |
| X-002 | X:applying:necessity | VerificationGap | Procedure | Procedure | Add records requirement for species selection rationale documentation -- Step 2 instructs palette development but Records section lists "Plant palette and species selection rationale" without specifying required content | The Records table lists this record but does not define what constitutes adequate species selection rationale documentation; core competence evidence requires defined evidentiary content | Procedure.md | ## Records; ### Step 2 | -- | PROPOSAL: Define minimum content for species selection rationale record | TBD |
| X-003 | X:applying:completeness | WeakStatement | Specification | Specification | Clarify what constitutes the "SOW-0017 scope checklist" referenced in verification for REQ-007-03-001 -- this checklist does not appear to exist as a defined artifact | Verification for REQ-001 states "Drawing set review against SOW-0017 scope checklist" but no such checklist is defined or referenced; complete enactment authority requires a defined verification instrument | Specification.md | ## Verification (REQ-007-03-001) | -- | PROPOSAL: Create or reference a SOW-0017 scope checklist | TBD |
| X-004 | X:judging:sufficiency | VerificationGap | Specification | Specification | Add interim verification checkpoints for vegetation establishment during the 2-year guarantee period (e.g., inspections at 3-month, 1-year, 2-year post-planting) | REQ-007-03-011 verification states "Confirmed via contract administration and 2-year post-CCC monitoring" but defines no interim inspection points or success criteria; informed adjudication evidence requires defined checkpoints | Specification.md; Procedure.md | ## Verification (REQ-007-03-011); ## Records | -- | PROPOSAL: Specification and Procedure | TBD |
| X-005 | X:reviewing:sufficiency | MissingSlot | Procedure | Procedure | Define required content for "Drawing revision log" record (minimum: revision number, date, description of changes, approval) | The Records table lists "Drawing revision log" as "Record of drawing revisions with dates and reasons" but does not specify the required fields; informed audit confidence requires a defined record structure | Procedure.md | ## Records | -- | PROPOSAL: Procedure records definition | TBD |

---

## Matrix E — Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Foundational Guidance Record | 1 | HAS_ITEMS | Examples section empty |
| E:guiding:information | guiding | information | Situated Directional Clarity | 0 | NO_ITEMS | Directional clarity established through Guidance purpose and principles |
| E:guiding:knowledge | guiding | knowledge | Integrated Directional Mastery | 0 | NO_ITEMS | Knowledge framework adequate for Guidance role |
| E:guiding:wisdom | guiding | wisdom | Principled Guidance Foresight | 1 | HAS_ITEMS | No foresight on maintenance handover |
| E:applying:data | applying | data | Verified Implementation Record | 1 | HAS_ITEMS | No as-built or as-planted record requirement |
| E:applying:information | applying | information | Situated Delivery Account | 0 | NO_ITEMS | Delivery account adequately structured through Procedure |
| E:applying:knowledge | applying | knowledge | Integrated Execution Mastery | 0 | NO_ITEMS | Execution knowledge framework adequate |
| E:applying:wisdom | applying | wisdom | Principled Execution Foresight | 0 | NO_ITEMS | Trade-offs provide execution foresight |
| E:judging:data | judging | data | Verified Assessment Record | 1 | HAS_ITEMS | No quantitative success metrics |
| E:judging:information | judging | information | Situated Judgment Clarity | 0 | NO_ITEMS | Judgment clarity established through verification table |
| E:judging:knowledge | judging | knowledge | Integrated Judgment Authority | 0 | NO_ITEMS | Judgment authority framework adequate |
| E:judging:wisdom | judging | wisdom | Principled Judgment Foresight | 0 | NO_ITEMS | Conflict table provides judgment foresight |
| E:reviewing:data | reviewing | data | Verified Examination Record | 0 | NO_ITEMS | Records section provides examination record framework |
| E:reviewing:information | reviewing | information | Situated Inspection Clarity | 0 | NO_ITEMS | Inspection clarity adequate |
| E:reviewing:knowledge | reviewing | knowledge | Integrated Inspection Mastery | 1 | HAS_ITEMS | No post-CCC inspection methodology |
| E:reviewing:wisdom | reviewing | wisdom | Principled Inspection Foresight | 0 | NO_ITEMS | Guarantee period provides long-term inspection foresight |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | RationaleGap | Guidance | Guidance | Populate the Examples section with at least a reference to comparable landfill/municipal compound restoration projects or provide rationale for why no examples are available from the project documents | The Examples section states "No project-specific examples are available" and defers to the Landscape Architect; foundational guidance records benefit from precedent references even if only pointing to external sources | Guidance.md | ## Examples | -- | PROPOSAL: Landscape Architect to provide references | TBD |
| E-002 | E:guiding:wisdom | MissingSlot | Guidance | Guidance | Add a consideration addressing maintenance handover -- who is responsible for vegetation maintenance after construction completion and during the guarantee period, and what happens after the 2-year guarantee period expires | Principled guidance foresight requires considering the long-term stewardship of planted vegetation; the documents address the guarantee period but not the transition of maintenance responsibility from contractor to County/landfill operator | Guidance.md; Specification.md | ## Considerations; ### REQ-007-03-011 | -- | PROPOSAL: Guidance considerations | TBD |
| E-003 | E:applying:data | VerificationGap | Procedure | Procedure | Add requirement for as-planted record (as-built equivalent for planting) documenting actual species installed, quantities, locations, and any substitutions from the design drawings | Verified implementation record requires documentation of what was actually installed versus what was designed; no as-planted record is defined in the Records section | Procedure.md | ## Records | -- | PROPOSAL: Procedure records section | TBD |
| E-004 | E:judging:data | Normalization | Multi | Specification | Normalize references to vegetation establishment success -- Specification verification uses qualitative language ("review," "check," "confirm") while the guarantee period requirement (REQ-011) implies quantitative accountability | Verified assessment records require consistent evidentiary standards; the mismatch between qualitative verification language and quantitative guarantee obligations creates ambiguity about what constitutes successful vegetation establishment | Specification.md; Procedure.md | ## Verification; ## Verification | -- | PROPOSAL: Define quantitative success criteria in Specification | TBD |
| E-005 | E:reviewing:knowledge | Normalization | Procedure | Procedure | Add post-CCC vegetation monitoring methodology to Procedure or cross-reference to a separate monitoring protocol -- currently only "Guarantee period inspection records" are listed without a defined inspection methodology | Integrated inspection mastery requires not just records but a defined methodology for how post-CCC vegetation inspections are conducted, what is measured, and what triggers remediation | Procedure.md | ## Records; ## Verification | -- | PROPOSAL: Procedure or separate monitoring protocol | TBD |
