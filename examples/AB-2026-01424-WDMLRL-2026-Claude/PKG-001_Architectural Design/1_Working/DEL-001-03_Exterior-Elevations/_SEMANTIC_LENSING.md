# Semantic Lensing Register: DEL-001-03 Exterior Elevations

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-001_Architectural Design/1_Working/DEL-001-03_Exterior-Elevations/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-001-03_Exterior-Elevations/_CONTEXT.md
- _STATUS.md — DEL-001-03_Exterior-Elevations/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md — DEL-001-03_Exterior-Elevations/_SEMANTIC.md
- Datasheet.md — DEL-001-03_Exterior-Elevations/Datasheet.md
- Specification.md — DEL-001-03_Exterior-Elevations/Specification.md
- Guidance.md — DEL-001-03_Exterior-Elevations/Guidance.md
- Procedure.md — DEL-001-03_Exterior-Elevations/Procedure.md
- _REFERENCES.md — DEL-001-03_Exterior-Elevations/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 6
  - Specification: 10
  - Guidance: 4
  - Procedure: 5
  - Multi: 3
- By matrix:
  - A: 6  B: 5  C: 3  F: 4  D: 3  X: 4  E: 3
- By type:
  - Conflict: 2
  - VerificationGap: 6
  - MissingSlot: 8
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 2
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 2
- Matrix parse errors: 0

---

## Matrix A — Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Occupancy classification unresolved |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | P.Eng. stamp requirement clear but wash bay door size is undetermined |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | ABC compliance verification approach incomplete |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | AHJ review scope not defined |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure steps are well-sequenced |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | CAD/BIM tool and drawing standards are TBD |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | QC checklist in Procedure is comprehensive |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Inter-discipline coordination review addressed in Procedure |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | No explicit quality/value criteria for exterior finish beyond "functional" |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Guidance T-01 addresses functional-vs-elaborate trade-off |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Guidance trade-offs address cost-benefit framing |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | QC checklist in Procedure covers quality review |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Datasheet | Specification | Record TBD: Confirm occupancy classification under Alberta Building Code (assumed Group F, Division 2) and its implications for exterior wall construction requirements | Occupancy class is marked as ASSUMPTION in Datasheet; prescriptive direction for exterior wall fire resistance and construction type depends on confirmed classification | Datasheet.md | Conditions table — "Occupancy class" row | — | PROPOSAL: AHJ or code consultant to confirm | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Clarify wash bay overhead door size requirement in REQ-003 by adding specific minimum height and width dimensions or referencing equipment specification source | REQ-003 states "sized to accommodate motor scraper-class equipment" without numeric dimension; this is insufficiently precise for mandatory practice — the door size directly affects the elevation drawing | Specification.md | REQ-003 — Overhead Door Openings | — | PROPOSAL: Architect to confirm with County equipment specs | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add verification approach for Alberta Building Code exterior wall provisions (fire resistance, accessibility at entries) beyond general "building permit authority review" | REQ-010 verification is "building permit authority review; code compliance register (DEL-009-04)" but no specific compliance checks for exterior wall construction type, fire resistance rating proximity to property lines, or accessible entrance provisions are enumerated | Specification.md | REQ-010; Verification table — REQ-010 row | — | PROPOSAL: Architect / code consultant | TBD |
| A-004 | A:normative:reviewing | MissingSlot | Specification | Specification | Add expected AHJ review scope for exterior elevations (what the permit authority will specifically check on these drawings) | No document describes what the AHJ will specifically review on exterior elevation sheets; this makes audit preparedness difficult to assess | Specification.md, Procedure.md | Specification: Standards table; Procedure: Step 12 | — | PROPOSAL: Architect to enumerate expected AHJ checks based on jurisdiction practice | TBD |
| A-005 | A:operative:applying | TBD_Question | Procedure | Procedure | Record TBD: Specify CAD/BIM software platform and project drawing standards (title block, scale conventions, sheet numbering) | Procedure lists CAD/BIM software as "TBD" and drawing standards as "TBD per Architect's office standard"; these are necessary operational inputs for producing the drawings | Procedure.md | Tools and Resources table | — | PROPOSAL: Architect to provide | TBD |
| A-006 | A:evaluative:guiding | RationaleGap | Guidance | Guidance | Add rationale for acceptable exterior finish quality level — explicitly link the industrial program to durability/maintenance expectations so the design intent is traceable | Guidance T-01 states "default to functional, durable, low-maintenance" but does not provide criteria for what constitutes acceptable quality for this facility type; this is a value orientation gap | Guidance.md | T-01 — Level of exterior finish detail | — | PROPOSAL: Architect + Owner | TBD |

---

## Matrix B — Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Compass orientation is assumed, not confirmed |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Wall cladding material is TBD with no source guidance |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Roof form/slope missing from all docs |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Dimensional data is consistently sourced from R-01 and R-04 |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Cross-reference signals between docs are present |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for design decisions is adequate in Guidance |
| B:information:completeness | information | completeness | comprehensive account | 1 | HAS_ITEMS | No mention of fenestration (windows) in Datasheet or Guidance |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | 24' dimension ambiguity (bay width vs. door opening) |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Design rationale present in Guidance for key decisions |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Coordination requirements well-articulated |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Documents collectively demonstrate thorough understanding of scope |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding of building program is consistent across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Key trade-offs identified in Guidance |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment calls on early resolution (T-03) are sound |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance covers breadth of design considerations |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is consistent with functional program |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | WeakStatement | Datasheet | Datasheet | Strengthen elevation face compass orientation from ASSUMPTION to confirmed fact, or explicitly flag as a blocking prerequisite for elevation production | Datasheet "Elevation Faces" section is entirely labeled ASSUMPTION with "exact compass orientation TBD pending site survey and civil design"; this is an essential fact needed before elevation drawings can be titled | Datasheet.md | Elevation Faces table header | — | PROPOSAL: Civil Engineer / site survey | TBD |
| B-002 | B:data:sufficiency | TBD_Question | Datasheet | Datasheet | Record TBD: Identify source or decision process for exterior cladding material selection — no RFP guidance, no conceptual drawing guidance, no Owner preference recorded | Wall material/cladding is "TBD — not specified in RFP or conceptual drawings" with no source column entry; there is no adequate evidence base for this essential design parameter | Datasheet.md | Key Exterior Elements table — "Wall material / cladding" row | — | PROPOSAL: Owner / Architect design decision | TBD |
| B-003 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add roof form/slope and roof material attributes to Datasheet with TBD values and identify decision source | Roof form/slope is listed as "TBD" in Datasheet Key Exterior Elements; roof system is "TBD" in Construction table. Neither Specification nor Guidance addresses how roof form will be determined, yet it directly affects elevation drawing content (roofline profile) | Datasheet.md | Key Exterior Elements — "Roof form / slope"; Construction — "Roof system" | — | PROPOSAL: Architect / Structural Engineer | TBD |
| B-004 | B:information:completeness | MissingSlot | Multi | Specification | Add statement in Specification scope regarding fenestration (windows): whether any are required, or explicitly state "no windows" if that is the design intent | Specification REQ list covers doors, mud sump, grade, materials, and structural coordination but makes no explicit statement about whether the building has windows. Specification scope line mentions "Exterior fenestration (windows, if any)" but no requirement addresses this. Datasheet has no window entries. Guidance is silent. For an industrial building this may be intentional but should be explicitly stated. | Specification.md, Datasheet.md, Guidance.md | Specification: Scope — "What this deliverable covers" bullet 3; entire Datasheet scanned for window references | — | PROPOSAL: Architect | TBD |
| B-005 | B:information:consistency | Conflict | Multi | Guidance | Resolve whether "24'" in conceptual drawing refers to structural bay centre-to-centre width or overhead door clear opening width; record resolution in Guidance conflict table and propagate to Specification REQ-003 and Datasheet | This conflict is already identified as CONF-001 in Guidance.md but has HumanRuling = TBD. It represents an information consistency gap: the same "24'" figure is used as door opening width in Specification REQ-003 and Datasheet, but its source is ambiguous. | Guidance.md, Specification.md, Datasheet.md | Guidance: CONF-001; Specification: REQ-003; Datasheet: Key Exterior Elements — "Overhead doors — repair bays" | Guidance.md#CONF-001 vs Specification.md#REQ-003 vs Datasheet.md#Key-Exterior-Elements | PROPOSAL: Structural Engineer + Architect to confirm | TBD |

---

## Matrix C — Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Compulsory Compliance Basis | 1 | HAS_ITEMS | Foundation type affects wall base detail on elevations |
| C:normative:sufficiency | normative | sufficiency | Mandated Adequacy Benchmark | 0 | NO_ITEMS | Verification table provides adequacy benchmarks for each REQ |
| C:normative:completeness | normative | completeness | Full Regulatory Coverage | 1 | HAS_ITEMS | National Building Code cross-reference is assumption-only |
| C:normative:consistency | normative | consistency | Harmonized Adherence Regime | 0 | NO_ITEMS | Standards table in Specification is consistent with Guidance P-07 |
| C:operative:necessity | operative | necessity | Critical Operational Prerequisite | 1 | HAS_ITEMS | Geotechnical report prerequisite status unclear |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Readiness Threshold | 0 | NO_ITEMS | Procedure prerequisites are well-defined |
| C:operative:completeness | operative | completeness | Exhaustive Process Coverage | 0 | NO_ITEMS | Procedure covers steps 1-12 comprehensively |
| C:operative:consistency | operative | consistency | Disciplined Execution Pattern | 0 | NO_ITEMS | Steps are logically sequenced with verification |
| C:evaluative:necessity | evaluative | necessity | Foundational Worth Criterion | 0 | NO_ITEMS | Core value proposition (permit + construction ref + coordination) is stated in Guidance Purpose |
| C:evaluative:sufficiency | evaluative | sufficiency | Justified Valuation Standard | 0 | NO_ITEMS | Guidance trade-offs provide sufficient value framing |
| C:evaluative:completeness | evaluative | completeness | Holistic Worth Accounting | 0 | NO_ITEMS | Three functions of elevations are described in Guidance Purpose |
| C:evaluative:consistency | evaluative | consistency | Principled Valuation Coherence | 0 | NO_ITEMS | Value framing is consistent across Guidance sections |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | MissingSlot | Specification | Specification | Add requirement or coordination note addressing how foundation type (TBD pending geotechnical) affects exterior elevation wall base detail and finished floor elevation datum | Datasheet lists foundation type as "TBD — pending geotechnical investigation"; Procedure Step 2 depends on FFE datum which depends on foundation design. But Specification has no requirement addressing how the elevation wall base condition varies with foundation type. This is a compulsory compliance basis gap. | Datasheet.md, Specification.md | Datasheet: Construction — "Foundation" row; Specification: REQ-002, REQ-007 | — | PROPOSAL: Structural / Geotechnical Engineer | TBD |
| C-002 | C:normative:completeness | WeakStatement | Specification | Specification | Strengthen Standards table entries for National Building Code and CSA standards from ASSUMPTION to confirmed applicability or remove if not applicable | Specification Standards table lists NBC and CSA standards with "ASSUMPTION: likely applicable; location TBD" — these are insufficiently grounded for full regulatory coverage claims | Specification.md | Standards table — NBC and CSA rows | — | PROPOSAL: Code consultant / Architect | TBD |
| C-003 | C:operative:necessity | WeakStatement | Procedure | Procedure | Clarify geotechnical report (DEL-008-01) prerequisite status: is it required before elevation production begins, or only before foundation wall base detail is finalized? | Procedure Prerequisites table lists geotechnical report as "Available (for foundation type info — informs wall base condition)" but its actual availability status is unknown and foundation type is TBD in Datasheet | Procedure.md, Datasheet.md | Procedure: Prerequisites — Input Documents table, last row; Datasheet: Construction — "Foundation" | — | PROPOSAL: Project Manager | TBD |

---

## Matrix F — Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Enforceable Governance Threshold | 1 | HAS_ITEMS | Fire resistance rating for exterior walls not addressed |
| F:normative:sufficiency | normative | sufficiency | Codified Clearance Standard | 1 | HAS_ITEMS | No acceptance criteria for exterior accessibility provisions |
| F:normative:completeness | normative | completeness | Total Conformance Command | 0 | NO_ITEMS | Requirements cover scope comprehensively for elevation content |
| F:normative:consistency | normative | consistency | Unified Conformance Logic | 0 | NO_ITEMS | Requirements are internally consistent |
| F:operative:necessity | operative | necessity | Mandatory Readiness Condition | 1 | HAS_ITEMS | County design direction on exterior materials is prerequisite but no mechanism to obtain |
| F:operative:sufficiency | operative | sufficiency | Verified Operational Preparedness | 0 | NO_ITEMS | Procedure verification table maps steps to evidence |
| F:operative:completeness | operative | completeness | Exhaustive Workflow Preparedness | 0 | NO_ITEMS | Workflow is complete from preliminary approval through permit |
| F:operative:consistency | operative | consistency | Calibrated Workflow Discipline | 0 | NO_ITEMS | Steps are consistently linked to source requirements |
| F:evaluative:necessity | evaluative | necessity | Essential Merit Evidence | 1 | HAS_ITEMS | No acceptance criteria for "durable, low-maintenance" exterior |
| F:evaluative:sufficiency | evaluative | sufficiency | Sound Worth Justification | 0 | NO_ITEMS | Trade-off rationale in Guidance is sound |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Merit Accounting | 0 | NO_ITEMS | Merit considerations are addressed in Guidance |
| F:evaluative:consistency | evaluative | consistency | Principled Merit Coherence | 0 | NO_ITEMS | Value reasoning is coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | MissingSlot | Specification | Specification | Add requirement addressing exterior wall fire resistance rating where proximity to property lines or adjacent buildings may trigger code requirements | REQ-010 references ABC compliance generally but no requirement specifically addresses fire resistance rating for exterior walls. Guidance P-07 mentions "exterior wall fire resistance where applicable (proximity to property lines or adjacent buildings)" but this is not captured as a Specification requirement. The existing Old North Shop adjacency may trigger fire separation requirements. | Specification.md, Guidance.md | Specification: REQ-010, REQ-012; Guidance: P-07 | — | PROPOSAL: Architect / code consultant | TBD |
| F-002 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add specific verification approach for accessible entrance provisions at exterior doors (REQ-010 references accessibility but no verification criteria exist for it) | REQ-010 mentions "accessibility provisions at entry points" as part of ABC compliance, but the Verification table entry for REQ-010 is only "building permit authority review; code compliance register (DEL-009-04)" with no specific acceptance criteria for accessibility at the exterior elevation level | Specification.md | REQ-010; Verification table — REQ-010 row | — | PROPOSAL: Architect / accessibility consultant | TBD |
| F-003 | F:operative:necessity | MissingSlot | Procedure | Procedure | Add a step or prerequisite mechanism for obtaining County design direction on exterior materials before REQ-008 can be satisfied | Procedure Prerequisites table lists "County design direction on exterior materials" as "Required for Finish Schedule (DEL-001-08)" but no Procedure step describes how to obtain this input. Without it, REQ-008 (material identification) cannot move beyond "TBD" keynotes. | Procedure.md | Prerequisites — "County design direction on exterior materials" row; Step 4 material keynotes | — | PROPOSAL: Architect / Project Manager | TBD |
| F-004 | F:evaluative:necessity | VerificationGap | Guidance | Specification | Add measurable acceptance criteria for exterior material durability and maintenance expectations referenced in Guidance T-01 | Guidance T-01 states "functional, durable, low-maintenance exterior materials" as the design default but no requirement or verification approach translates this into measurable acceptance criteria (e.g., expected service life, maintenance cycle, warranty requirements) | Guidance.md, Specification.md | Guidance: T-01; Specification: REQ-008, Verification table | — | PROPOSAL: Owner / Architect | TBD |

---

## Matrix D — Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Definitive Mandate Boundary | 0 | NO_ITEMS | Scope boundaries clearly defined in Specification |
| D:normative:applying | normative | applying | Obligatory Acceptance Enactment | 1 | HAS_ITEMS | Old North Shop interface acceptance criteria missing |
| D:normative:judging | normative | judging | Binding Conformance Verdict | 0 | NO_ITEMS | Verification table provides conformance verdicts |
| D:normative:reviewing | normative | reviewing | Resolved Compliance Scrutiny | 0 | NO_ITEMS | Building permit review process addressed |
| D:operative:guiding | operative | guiding | Resolved Process Steering | 0 | NO_ITEMS | Procedure steps provide clear steering |
| D:operative:applying | operative | applying | Confirmed Field Deployment | 1 | HAS_ITEMS | Revision control process not defined |
| D:operative:judging | operative | judging | Definitive Readiness Verdict | 0 | NO_ITEMS | QC checklist provides readiness gate |
| D:operative:reviewing | operative | reviewing | Confirmed Practice Examination | 0 | NO_ITEMS | Inter-discipline coordination review process defined |
| D:evaluative:guiding | evaluative | guiding | Grounded Worth Charter | 0 | NO_ITEMS | Guidance Purpose section establishes value charter |
| D:evaluative:applying | evaluative | applying | Justified Quality Realization | 1 | HAS_ITEMS | No quality gate between draft and IFC for elevation design quality |
| D:evaluative:judging | evaluative | judging | Definitive Worth Ruling | 0 | NO_ITEMS | P.Eng. review serves as quality verdict |
| D:evaluative:reviewing | evaluative | reviewing | Confirmed Worth Examination | 0 | NO_ITEMS | County review process addresses worth examination |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | VerificationGap | Specification | Specification | Add acceptance criteria for REQ-012 (interface with existing Old North Shop) specifying what constitutes a resolved interface condition (expansion joint type, weather seal, structural connection, or separation) | REQ-012 verification is "Interface condition shown; no unresolved gaps between new and existing building depicted" — this is circular (the gap is unresolved if the design decision itself is unresolved). Guidance P-05 and T-02 identify this as a complex design decision but no acceptance criteria define what a resolved interface looks like. | Specification.md, Guidance.md | Specification: REQ-012, Verification table; Guidance: P-05, T-02 | — | PROPOSAL: Architect / Structural Engineer | TBD |
| D-002 | D:operative:applying | MissingSlot | Procedure | Procedure | Add revision control process (drawing revision log, revision numbering convention, reason-for-revision tracking) to Procedure | Procedure Records table mentions "Revision history — Drawing revision log (Rev A, Rev B, etc.) with reason for each revision" but no step in the Procedure describes how revisions are managed, numbered, or tracked during the production process | Procedure.md | Records table — "Revision history" row; Steps 1-12 (none addresses revision control) | — | PROPOSAL: Architect | TBD |
| D-003 | D:evaluative:applying | RationaleGap | Guidance | Guidance | Add guidance on quality expectations for elevation drawing presentation (line weights, annotation density, keynote conventions) appropriate for IFC-level drawings versus preliminary-level drawings | Guidance does not address what differentiates a preliminary elevation (for County review) from an IFC elevation (for construction) in terms of drawing quality and content completeness. Procedure Step 9 implies a County review of draft elevations, but there is no guidance on what level of completeness is appropriate at that stage versus IFC. | Guidance.md, Procedure.md | Guidance: entire document scanned; Procedure: Step 9, Step 10 | — | PROPOSAL: Architect | TBD |

---

## Matrix X — Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Commanding Foundation Mandate | 0 | NO_ITEMS | Foundation mandates are traceable to RFP |
| X:guiding:sufficiency | guiding | sufficiency | Substantiated Leadership Basis | 0 | NO_ITEMS | Source traceability is present throughout |
| X:guiding:completeness | guiding | completeness | Complete Governance Command | 1 | HAS_ITEMS | Signage governance absent |
| X:guiding:consistency | guiding | consistency | Unified Constraint Integrity | 0 | NO_ITEMS | Constraints are consistently referenced |
| X:applying:necessity | applying | necessity | Critical Delivery Imperative | 1 | HAS_ITEMS | Bulk water fill location has no verification |
| X:applying:sufficiency | applying | sufficiency | Substantiated Delivery Proof | 0 | NO_ITEMS | Verification approaches are substantiated |
| X:applying:completeness | applying | completeness | Complete Delivery Archive | 0 | NO_ITEMS | Documentation and records sections are complete |
| X:applying:consistency | applying | consistency | Consistent Delivery Standard | 0 | NO_ITEMS | Delivery standards are consistent |
| X:judging:necessity | judging | necessity | Decisive Compliance Ruling | 1 | HAS_ITEMS | Existing building height not confirmed |
| X:judging:sufficiency | judging | sufficiency | Proven Assessment Threshold | 0 | NO_ITEMS | Assessment thresholds are defined in verification table |
| X:judging:completeness | judging | completeness | Total Assessment Record | 0 | NO_ITEMS | All requirements have verification entries |
| X:judging:consistency | judging | consistency | Calibrated Assessment Norm | 0 | NO_ITEMS | Verification approaches are calibrated to requirement type |
| X:reviewing:necessity | reviewing | necessity | Essential Audit Trigger | 1 | HAS_ITEMS | No audit trigger for cross-package consistency |
| X:reviewing:sufficiency | reviewing | sufficiency | Sufficient Audit Basis | 0 | NO_ITEMS | Records section provides audit basis |
| X:reviewing:completeness | reviewing | completeness | Full Audit Coverage | 0 | NO_ITEMS | Records and verification cover audit needs |
| X:reviewing:consistency | reviewing | consistency | Standardized Audit Norm | 0 | NO_ITEMS | Audit approach is standardized across requirements |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | MissingSlot | Datasheet | Datasheet | Add signage requirements or explicitly record "Signage: TBD — no RFP requirement identified" with a decision source for whether signage is needed | Datasheet lists "Signage: TBD" with no source and no decision pathway. Specification scope mentions exterior features but has no signage requirement. If signage is needed, it affects the elevation drawing; if not, it should be explicitly excluded. | Datasheet.md, Specification.md | Datasheet: Key Exterior Elements — "Signage" row; Specification: entire document scanned | — | PROPOSAL: Owner | TBD |
| X-002 | X:applying:necessity | VerificationGap | Specification | Specification | Add verification approach for bulk water fill exterior connection location (mentioned in Specification scope and Datasheet but no REQ or verification entry exists) | Specification scope includes "Bulk water fill exterior connection location" and Datasheet lists "Bulk water fill connection: Exterior location TBD" but there is no corresponding requirement (REQ) and no verification approach. This is a critical delivery item with no acceptance path. | Specification.md, Datasheet.md | Specification: Scope — "What this deliverable covers"; Datasheet: Key Exterior Elements — "Bulk water fill connection" | — | PROPOSAL: Plumbing Engineer / Architect | TBD |
| X-003 | X:judging:necessity | Normalization | Multi | Guidance | Normalize reference to existing Old North Shop height: Procedure Step 4 states "40' high or as existing" but no document confirms the existing building height; Datasheet states footprint (105' x 40') but not height | The existing building height is needed for the interface elevation (REQ-012) but is not recorded as a fact in any document. Procedure Step 4 introduces "40' high" as a number not present elsewhere, which may be an error (40' may be a plan dimension, not a height). | Procedure.md, Datasheet.md | Procedure: Step 4 — "Interface face" bullet; Datasheet: Existing Old North Shop footprint | — | PROPOSAL: Existing condition survey / Architect | TBD |
| X-004 | X:reviewing:necessity | VerificationGap | Specification | Procedure | Add a coordination verification checkpoint confirming that elevation drawings are consistent with all other IFC packages (PKG-002 through PKG-006) before P.Eng. stamp | Procedure Step 10.2 mentions confirming consistency with other IFC sets but the Verification table in Procedure has no explicit checkpoint for cross-package (not just cross-discipline within PKG-001) consistency | Procedure.md | Procedure: Step 10.2; Verification table — Step 10 row | — | PROPOSAL: Architect / Project Manager | TBD |

---

## Matrix E — Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Baseline Record | 1 | HAS_ITEMS | Existing building condition data absent |
| E:guiding:information | guiding | information | Informed Steering Directive | 0 | NO_ITEMS | Guidance provides informed steering |
| E:guiding:knowledge | guiding | knowledge | Authoritative Stewardship Command | 0 | NO_ITEMS | Discipline expertise requirements are addressed |
| E:guiding:wisdom | guiding | wisdom | Principled Steering Vision | 0 | NO_ITEMS | Trade-offs and principles are well-articulated |
| E:applying:data | applying | data | Verified Production Record | 0 | NO_ITEMS | Records section addresses production documentation |
| E:applying:information | applying | information | Informed Execution Narrative | 0 | NO_ITEMS | Procedure provides informed execution narrative |
| E:applying:knowledge | applying | knowledge | Proven Execution Proficiency | 0 | NO_ITEMS | Coordination with discipline experts is embedded in procedure |
| E:applying:wisdom | applying | wisdom | Prudent Execution Judgment | 0 | NO_ITEMS | Procedure notes and conditional steps reflect prudent judgment |
| E:judging:data | judging | data | Documented Verdict Evidence | 1 | HAS_ITEMS | CONF-002 area calculation needs resolution path |
| E:judging:information | judging | information | Informed Ruling Narrative | 0 | NO_ITEMS | Verification approaches provide ruling narrative |
| E:judging:knowledge | judging | knowledge | Comprehensive Judgment Command | 0 | NO_ITEMS | QC checklist is comprehensive |
| E:judging:wisdom | judging | wisdom | Principled Verdict Discernment | 0 | NO_ITEMS | P.Eng. review provides principled verdict |
| E:reviewing:data | reviewing | data | Substantiated Inspection Record | 0 | NO_ITEMS | Records section provides inspection record basis |
| E:reviewing:information | reviewing | information | Informed Scrutiny Narrative | 0 | NO_ITEMS | AHJ review process provides scrutiny narrative |
| E:reviewing:knowledge | reviewing | knowledge | Comprehensive Scrutiny Command | 1 | HAS_ITEMS | No mechanism for post-permit revision scrutiny |
| E:reviewing:wisdom | reviewing | wisdom | Principled Inspection Judgment | 0 | NO_ITEMS | Inspection judgment framework is adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | RationaleGap | Datasheet | Datasheet | Add existing Old North Shop condition data section: confirm existing building height, wall construction type, roof form, and interface wall condition as baseline data for REQ-012 and the interface elevation | Datasheet records existing building footprint (105' x 40') but no other existing building data. The new addition interface elevation (REQ-012) requires knowledge of existing conditions. This is an authoritative baseline record gap. | Datasheet.md | Existing Old North Shop footprint row; entire Datasheet scanned for existing building details | — | PROPOSAL: Existing condition survey | TBD |
| E-002 | E:judging:data | Conflict | Guidance | Guidance | Resolve CONF-002 (whether 13,000 sq ft is new addition only or includes existing building area) by recording confirmed ruling; propagate to Datasheet if area figure affects elevation scope | CONF-002 in Guidance identifies ambiguity about whether "approximately 13,000 square feet" refers to new addition only (130' x 100' = 13,000 consistent) or includes existing building area. While the Guidance conflict table records this, there is no resolution path or timeline. This affects documented verdict evidence for building scope. | Guidance.md, Datasheet.md | Guidance: CONF-002; Datasheet: Attributes — "Useable floor area" row | Guidance.md#CONF-002: R-01 §3.1 vs R-04 Appendix B | PROPOSAL: Owner / Contract administrator | TBD |
| E-003 | E:reviewing:knowledge | Normalization | Procedure | Procedure | Add step or note in Procedure addressing how post-permit AHJ deficiency responses (Step 12.2-12.3) trigger revision control and re-verification of previously completed QC checks | Procedure Step 12 addresses AHJ deficiency responses and drawing updates, but there is no linkage back to the QC checklist (Step 7) or coordination review (Step 8) to confirm that post-permit changes do not introduce new inconsistencies. This is a comprehensive scrutiny gap. | Procedure.md | Step 12.2, Step 12.3; Step 7 (QC checklist); Step 8 (coordination review) | — | PROPOSAL: Architect | TBD |
