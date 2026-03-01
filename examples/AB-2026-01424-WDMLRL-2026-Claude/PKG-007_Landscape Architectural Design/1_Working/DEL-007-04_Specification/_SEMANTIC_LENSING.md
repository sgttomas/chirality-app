# Semantic Lensing Register: DEL-007-04 Landscape Specification

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-007_Landscape Architectural Design/1_Working/DEL-007-04_Specification/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-007-04 Landscape Specification, PKG-007 Landscape Architectural Design
- _STATUS.md -- State: SEMANTIC_READY, Last Updated: 2026-02-26
- _SEMANTIC.md -- Matrices A, B, C, F, D, X, E parsed successfully
- Datasheet.md -- DEL-007-04 identification, attributes, conditions, construction, references
- Specification.md -- Scope, requirements (REQ-007-04-001 through REQ-007-04-061), standards, verification
- Guidance.md -- Purpose, principles, considerations, trade-offs, conflict table
- Procedure.md -- Prerequisites, 8-step production workflow, verification checks, records
- _REFERENCES.md -- Present; lists R-01, R-07, DECOMP_REF, related deliverables, standards

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 30
- By document (AppliesToDoc):
  - Datasheet: 2
  - Specification: 18
  - Guidance: 1
  - Procedure: 4
  - Multi: 5
- By matrix:
  - A: 5  B: 4  C: 3  F: 5  D: 4  X: 5  E: 4
- By type:
  - Conflict: 2
  - VerificationGap: 6
  - MissingSlot: 8
  - WeakStatement: 4
  - RationaleGap: 4
  - Normalization: 2
  - TBD_Question: 4
  - MatrixError: 0
- Notable conflicts: 2
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Weak statement on code applicability |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Missing compaction standards |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Verification gap for standards compliance |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Procedure Step 8 covers IFC/permit submission adequately |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Steps 1-8 provide adequate procedural direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | TBD on planting execution details |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification table in Specification and Procedure covers this |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Procedure verification checks address process review |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Principles section provides adequate value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 1 | HAS_ITEMS | No quality criteria for gravel surface performance |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Warranty requirements provide worth determination framework |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Verification checks in Procedure and Specification are adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify which specific Alberta building codes and safety codes apply to landscape and site works; current language "applicable Alberta building codes and regulations" is ambiguous | REQ-007-04-002 uses language "applicable Alberta building codes" without identifying which codes apply to landscape scope specifically; this could change implementation decisions regarding permits and inspections | Specification.md | Requirements > General Requirements > REQ-007-04-002 | -- | PROPOSAL: Landscape Architect to identify applicable codes | TBD |
| A-002 | A:normative:applying | MissingSlot | Specification | Specification | Add subgrade compaction standard (e.g., percentage of Standard Proctor density) for gravel driving surface areas | REQ-007-04-011 requires driving surface designed for motor scraper class equipment but no compaction standard is specified; this is a mandatory practice gap for construction execution | Specification.md | Requirements > Gravel Driving Surface > REQ-007-04-011 | -- | PROPOSAL: Civil Engineer / Landscape Architect coordination | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add specific acceptance criteria for Alberta Building Code and Safety Code compliance checks referenced in REQ-007-04-002 | Verification table entry for REQ-007-04-002 says "Inspection: Safety Code permit inspections; review by permit authority" but does not define what constitutes a passing inspection or which specific permits are required | Specification.md | Verification table > REQ-007-04-002 | -- | PROPOSAL: Landscape Architect with permit authority | TBD |
| A-004 | A:operative:applying | TBD_Question | Specification | Specification | Record TBD: What are the specific planting installation methods, soil preparation depths, and establishment period requirements for this site? Source: DEL-007-03 (Planting & Restoration Plans) | REQ-007-04-050 acknowledges content is TBD pending DEL-007-03 but practical execution details for planting remain entirely absent; cannot proceed with planting specification without this input | Specification.md | Requirements > Planting and Site Restoration > REQ-007-04-050 | -- | PROPOSAL: Landscape Architect upon DEL-007-03 completion | TBD |
| A-005 | A:evaluative:applying | MissingSlot | Specification | Specification | Add performance criteria for gravel driving surface (e.g., minimum bearing capacity, acceptable rutting depth, surface drainage slope) | No quantitative quality or performance metrics exist for the gravel driving surface beyond the general requirement for motor scraper class suitability; merit application requires measurable criteria | Specification.md | Requirements > Gravel Driving Surface | -- | PROPOSAL: Civil Engineer / Landscape Architect | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Site area dimension missing |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Pad dimensions TBD |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Planting data absent |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurement references to RFP sections are consistent across documents |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (scope, dependencies, interfaces) adequately communicated |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context provided in Guidance and Datasheet is adequate |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Documents collectively provide a comprehensive account of known scope |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology inconsistency for scope boundary |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding of site, scope, and constraints is present |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Documents appropriately defer to professional expertise (Landscape Architect) |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Acknowledged gaps (TBDs) are appropriate for scaffold state |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding of deliverable scope is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Guidance trade-offs section provides appropriate discernment framework |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-off table and conflict table provide adequate judgment scaffolding |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance provides holistic site-context and interface awareness |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Principles in Guidance are internally consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add expansion zone area dimension (metric) as an essential fact; currently listed as TBD | Site area for the expansion zone is listed as TBD in Datasheet Attributes; this is an essential fact needed for gravel quantity estimation and grading design | Datasheet.md | Attributes > Site area -- expansion zone | -- | PROPOSAL: Surveyor or Civil Engineer from PKG-005/PKG-008 | TBD |
| B-002 | B:data:sufficiency | TBD_Question | Multi | Datasheet | Record TBD: What are the cement pad dimensions, concrete mix design, and gravel pad dimensions? Source: DEL-007-02 and structural/civil coordination | REQ-007-04-020 and REQ-007-04-021 both note dimensions and specifications as TBD; adequate evidence for pad construction is absent | Specification.md; Datasheet.md | Requirements > Hardscape -- Pads; Attributes table | -- | PROPOSAL: Landscape Architect coordinating with Civil/Structural | TBD |
| B-003 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add planting data attributes: species list, soil preparation depth, planting sizes, spacing, and establishment period when available from DEL-007-03 | Datasheet has "TBD -- no specific planting schedule or species list" for planting/restoration areas; this represents a gap in comprehensive record for a major specification section | Datasheet.md | Attributes > Planting/restoration areas | -- | PROPOSAL: Landscape Architect upon DEL-007-03 | TBD |
| B-004 | B:information:consistency | Normalization | Multi | Guidance | Normalize scope boundary terminology: Datasheet uses "County/Landfill supplies gravel" while Specification uses "aggregate supplied by County/Landfill" and Guidance uses "County responsibilities explicitly excluded from the Proponent's scope" -- standardize "aggregate" vs "gravel" usage | The terms "gravel" and "aggregate" are used interchangeably across documents when referring to the County-supplied driving surface material; this inconsistency could cause confusion in procurement or construction communication | Datasheet.md; Specification.md; Guidance.md | Datasheet > Attributes > Aggregate supply; Specification > REQ-007-04-010; Guidance > Principles > 3 | -- | PROPOSAL: Landscape Architect to define preferred term in Guidance | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Compulsory Compliance Basis | 1 | HAS_ITEMS | Standards table has accessibility gaps |
| C:normative:sufficiency | normative | sufficiency | Demonstrated Regulatory Adequacy | 0 | NO_ITEMS | RFP-sourced requirements demonstrate adequate regulatory basis |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Coverage | 1 | HAS_ITEMS | Missing environmental regulation coverage |
| C:normative:consistency | normative | consistency | Harmonized Regulatory Integrity | 0 | NO_ITEMS | Regulatory references are consistent where present |
| C:operative:necessity | operative | necessity | Critical Operational Foundation | 0 | NO_ITEMS | Procedure prerequisites and steps establish adequate operational foundation |
| C:operative:sufficiency | operative | sufficiency | Proven Execution Capability | 0 | NO_ITEMS | Procedure steps are sufficient for the scaffold state |
| C:operative:completeness | operative | completeness | Comprehensive Operational Coverage | 1 | HAS_ITEMS | Geotechnical dependency gap |
| C:operative:consistency | operative | consistency | Reliable Procedural Alignment | 0 | NO_ITEMS | Procedure steps align with Specification requirements |
| C:evaluative:necessity | evaluative | necessity | Foundational Value Criterion | 0 | NO_ITEMS | Core value criteria (durability, drainage, compliance) established in Guidance |
| C:evaluative:sufficiency | evaluative | sufficiency | Substantiated Worth Assessment | 0 | NO_ITEMS | Trade-off table provides adequate assessment framework |
| C:evaluative:completeness | evaluative | completeness | Exhaustive Quality Accounting | 0 | NO_ITEMS | Quality criteria are proportionate to scaffold state |
| C:evaluative:consistency | evaluative | consistency | Consistent Valuation Integrity | 0 | NO_ITEMS | Valuation approach is consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Strengthen Standards table entries marked "ASSUMPTION: likely applicable; document not available for review": confirm applicability of Alberta Building Code, Alberta Safety Codes, and CSI/MasterFormat to this landscape scope | Three of six standards entries have accessibility noted as "ASSUMPTION" with "location TBD"; compulsory compliance basis requires confirmed applicability, not assumptions | Specification.md | Standards table | -- | PROPOSAL: Landscape Architect / Project Manager to confirm | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add applicable Alberta environmental regulations for mud sump effluent handling and site restoration on landfill-adjacent land | Guidance mentions "Alberta environmental regulations apply; specific requirements TBD" for mud sump but no environmental regulatory requirement appears in Specification; exhaustive regulatory coverage requires this | Guidance.md; Specification.md | Guidance > Considerations > Mud Sump; Specification > Standards table | -- | PROPOSAL: Environmental consultant or Landscape Architect | TBD |
| C-003 | C:operative:completeness | RationaleGap | Procedure | Guidance | Add rationale in Guidance for why geotechnical report (DEL-008-01) is critical to landscape specification -- explain how subsoil conditions affect pad design, planting soil, and grading | Procedure lists DEL-008-01 as prerequisite P5 but neither Guidance nor Specification explains how geotechnical data will specifically influence landscape specification decisions; comprehensive operational coverage requires this connection | Procedure.md | Prerequisites > P5 | -- | PROPOSAL: Landscape Architect | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Absolute Compliance Imperative | 1 | HAS_ITEMS | P.Eng. stamping requirement ambiguity |
| F:normative:sufficiency | normative | sufficiency | Sufficient Conformance Rigor | 0 | NO_ITEMS | Conformance rigor is adequate for sourced requirements |
| F:normative:completeness | normative | completeness | Total Regulatory Fulfillment | 1 | HAS_ITEMS | Drainage design standard missing |
| F:normative:consistency | normative | consistency | Uniform Compliance Coherence | 1 | HAS_ITEMS | Conflict on cement pad discipline assignment |
| F:operative:necessity | operative | necessity | Fundamental Process Imperative | 0 | NO_ITEMS | Process imperatives (steps, prerequisites) are adequate |
| F:operative:sufficiency | operative | sufficiency | Adequate Execution Fitness | 1 | HAS_ITEMS | Mud sump specification incomplete |
| F:operative:completeness | operative | completeness | Total Operational Fulfillment | 0 | NO_ITEMS | Operational coverage is proportionate to scaffold state |
| F:operative:consistency | operative | consistency | Steady Procedural Coherence | 0 | NO_ITEMS | Procedure and Specification are procedurally coherent |
| F:evaluative:necessity | evaluative | necessity | Essential Quality Imperative | 1 | HAS_ITEMS | Warranty failure criteria missing |
| F:evaluative:sufficiency | evaluative | sufficiency | Adequate Evaluative Competence | 0 | NO_ITEMS | Evaluative framework is adequate for current state |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Quality Fulfillment | 0 | NO_ITEMS | Quality framework is proportionate to scaffold state |
| F:evaluative:consistency | evaluative | consistency | Principled Quality Consistency | 0 | NO_ITEMS | Quality approach is consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | WeakStatement | Specification | Specification | Clarify REQ-007-04-003: state definitively whether P.Eng. stamping applies to landscape-specific drawings or only to engineering drawings in the IFC package; current ASSUMPTION note creates ambiguity on a compliance imperative | REQ-007-04-003 contains an ASSUMPTION about Landscape Architect coordinating with P.Eng.; for an absolute compliance imperative, the stamping scope must be unambiguous | Specification.md | Requirements > General Requirements > REQ-007-04-003 | -- | PROPOSAL: Project Manager / regulatory authority | TBD |
| F-002 | F:normative:completeness | MissingSlot | Specification | Specification | Add stormwater management / drainage design standard reference (e.g., Alberta municipal drainage standards or equivalent) to the Standards table | REQ-007-04-030 requires positive drainage and REQ-007-04-031 prohibits drainage impact on neighbors, but no drainage design standard is referenced in the Standards table; total regulatory fulfillment requires a cited standard | Specification.md | Standards table; Requirements > Site Drainage > REQ-007-04-030-031 | -- | PROPOSAL: Civil Engineer (PKG-005) / Landscape Architect | TBD |
| F-003 | F:normative:consistency | Conflict | Multi | NA | Resolve discipline assignment for cement pad specification: Guidance Conflict Table (CONF-007-04-01) identifies this as unresolved; Specification assigns requirements to Landscape Architect while PKG-005 civil scope may include "pad layout" | Two sources make potentially incompatible claims about cement pad specification authority; uniform compliance coherence requires resolution | Specification.md; Guidance.md | Specification > Requirements > Hardscape -- Pads; Guidance > Conflict Table > CONF-007-04-01 | Specification.md#Hardscape--Pads (Landscape scope); Guidance.md#Conflict-Table (PKG-005 civil scope noted) | PROPOSAL: Per CONF-007-04-01 proposal -- Civil for structural, Landscape for surface | TBD |
| F-004 | F:operative:sufficiency | VerificationGap | Specification | Specification | Add mud sump sizing criteria, material specification, and drainage connection requirements to REQ-007-04-040; current requirement states "sized to permit cleanout by excavator" without defining dimensions or material | Adequate execution fitness for the mud sump requires more than "sized to permit cleanout by excavator"; constructability depends on dimensional and material specifications | Specification.md | Requirements > Exterior Mud Sump > REQ-007-04-040 | -- | PROPOSAL: Plumbing Engineer (PKG-006) / Landscape Architect | TBD |
| F-005 | F:evaluative:necessity | MissingSlot | Specification | Specification | Add definition of warrantable failure criteria for landscape elements (planting survival rate, gravel surface condition, hardscape defects) per Guidance recommendation | REQ-007-04-060 establishes warranty obligation but does not define what constitutes a warrantable failure for different landscape elements; essential quality imperative requires this definition | Specification.md; Guidance.md | Specification > Requirements > Warranty > REQ-007-04-060; Guidance > Considerations > Warranty | -- | PROPOSAL: Landscape Architect | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Definitive Regulatory Direction | 0 | NO_ITEMS | Guidance Principles 1-5 provide adequate regulatory direction |
| D:normative:applying | normative | applying | Resolved Mandatory Practice | 1 | HAS_ITEMS | Topsoil stripping responsibility ambiguity |
| D:normative:judging | normative | judging | Conclusive Compliance Judgment | 1 | HAS_ITEMS | Verification approach for planting is TBD |
| D:normative:reviewing | normative | reviewing | Authoritative Conformance Audit | 0 | NO_ITEMS | Procedure Step 8 and verification table cover audit requirements |
| D:operative:guiding | operative | guiding | Grounded Procedural Guidance | 0 | NO_ITEMS | Procedure is well-grounded with explicit prerequisites |
| D:operative:applying | operative | applying | Resolved Execution Standard | 0 | NO_ITEMS | Execution standards are adequate for scaffold state |
| D:operative:judging | operative | judging | Conclusive Performance Judgment | 1 | HAS_ITEMS | No pass/fail thresholds for site inspection |
| D:operative:reviewing | operative | reviewing | Settled Process Audit | 0 | NO_ITEMS | Procedure verification checks are adequate |
| D:evaluative:guiding | evaluative | guiding | Grounded Quality Orientation | 0 | NO_ITEMS | Guidance principles provide adequate quality orientation |
| D:evaluative:applying | evaluative | applying | Resolved Merit Standard | 0 | NO_ITEMS | Merit standards are proportionate to scaffold state |
| D:evaluative:judging | evaluative | judging | Conclusive Worth Determination | 1 | HAS_ITEMS | Defect rectification timeline gap |
| D:evaluative:reviewing | evaluative | reviewing | Principled Quality Audit | 0 | NO_ITEMS | Quality audit framework is adequate in Procedure |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | WeakStatement | Specification | Specification | Clarify REQ-007-04-012 conditional language: "If topsoil stripping has not already been performed by the Owner, it is the Proponent's responsibility" -- define how this condition is determined and by whom | Resolved mandatory practice requires clear assignment; the conditional "if not already performed" creates ambiguity about who verifies this condition and what documentation is required | Specification.md | Requirements > Gravel Driving Surface > REQ-007-04-012 | -- | PROPOSAL: Project Manager to define verification protocol | TBD |
| D-002 | D:normative:judging | VerificationGap | Specification | Specification | Add verification approach details for planting requirements (REQ-007-04-050-052); current entry says "TBD pending DEL-007-03" without specifying what verification will look like | Conclusive compliance judgment for planting requirements cannot be made when the verification approach is entirely TBD; at minimum, define the types of inspection that will apply | Specification.md | Verification table > REQ-007-04-050-052 | -- | PROPOSAL: Landscape Architect | TBD |
| D-003 | D:operative:judging | VerificationGap | Procedure | Procedure | Add quantitative pass/fail criteria to Procedure verification checks V-004 and V-008: e.g., minimum compaction percentage, acceptable drainage slope range | Procedure V-004 says "Subgrade prep, gradation, compaction, and load capacity addressed" and V-008 says "Positive drainage and neighbor property protection explicitly specified" but neither defines measurable pass thresholds for conclusive performance judgment | Procedure.md | Verification > V-004, V-008 | -- | PROPOSAL: Civil Engineer / Landscape Architect | TBD |
| D-004 | D:evaluative:judging | RationaleGap | Specification | Guidance | Add rationale for the 10-day defect rectification timeline in REQ-007-04-061: explain why 10 days is appropriate for landscape defects (some defects like plant replacement may require seasonal timing) | REQ-007-04-061 requires rectification "within ten (10) days of written instruction" but seasonal planting constraints may make 10 days impractical for certain landscape defects; conclusive worth determination requires this context | Specification.md; Guidance.md | Specification > Requirements > Warranty > REQ-007-04-061; Guidance > Considerations > Warranty | -- | PROPOSAL: Landscape Architect | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Imperative Directional Basis | 0 | NO_ITEMS | Directional basis established in Guidance |
| X:guiding:sufficiency | guiding | sufficiency | Adequate Governance Framing | 1 | HAS_ITEMS | Drainage interface governance gap |
| X:guiding:completeness | guiding | completeness | Complete Directional Coverage | 0 | NO_ITEMS | Directional coverage is proportionate to scope |
| X:guiding:consistency | guiding | consistency | Coherent Directional Alignment | 0 | NO_ITEMS | Direction is coherent across documents |
| X:applying:necessity | applying | necessity | Critical Implementation Basis | 1 | HAS_ITEMS | Gravel gradation specification missing |
| X:applying:sufficiency | applying | sufficiency | Sufficient Practice Justification | 0 | NO_ITEMS | Practice justifications are adequate where requirements exist |
| X:applying:completeness | applying | completeness | Total Implementation Coverage | 1 | HAS_ITEMS | Transition zones not addressed |
| X:applying:consistency | applying | consistency | Uniform Practice Alignment | 0 | NO_ITEMS | Practices are uniformly aligned across documents |
| X:judging:necessity | judging | necessity | Decisive Adjudicative Basis | 1 | HAS_ITEMS | Material testing TBD |
| X:judging:sufficiency | judging | sufficiency | Adequate Judgment Justification | 0 | NO_ITEMS | Judgment justifications are adequate where verification exists |
| X:judging:completeness | judging | completeness | Exhaustive Adjudicative Coverage | 0 | NO_ITEMS | Coverage is proportionate; acknowledged TBDs are appropriate |
| X:judging:consistency | judging | consistency | Consistent Adjudicative Rigor | 0 | NO_ITEMS | Adjudicative rigor is consistent across verification entries |
| X:reviewing:necessity | reviewing | necessity | Essential Examination Basis | 0 | NO_ITEMS | Examination basis established in Procedure |
| X:reviewing:sufficiency | reviewing | sufficiency | Adequate Examination Rigor | 1 | HAS_ITEMS | Drainage conflict scope assignment |
| X:reviewing:completeness | reviewing | completeness | Comprehensive Examination Coverage | 0 | NO_ITEMS | Examination coverage is proportionate |
| X:reviewing:consistency | reviewing | consistency | Uniform Examination Integrity | 0 | NO_ITEMS | Examination approach is uniformly structured |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | RationaleGap | Guidance | Guidance | Add governance framing for PKG-005/PKG-007 drainage interface: define which party produces the drainage design standard, which party verifies landscape drainage conformance, and how discrepancies are resolved | Guidance Conflict Table has CONF-007-04-02 on drainage scope but no governance framing for how the interface is managed day-to-day during design; adequate governance framing requires this | Guidance.md | Conflict Table > CONF-007-04-02; Considerations > Drainage Integration | -- | PROPOSAL: Project Manager to define interface governance | TBD |
| X-002 | X:applying:necessity | TBD_Question | Specification | Specification | Record TBD: What gravel gradation and depth specifications apply to the driving surface? Source: County/Landfill aggregate supply specifications and Civil Engineer (PKG-005) | REQ-007-04-010 states final surface shall be gravel but no gradation or depth is specified; critical implementation basis for driving surface construction is absent | Specification.md; Guidance.md | Specification > Requirements > Gravel Driving Surface > REQ-007-04-010; Guidance > Considerations > Gravel Driving Surface | -- | PROPOSAL: Civil Engineer / County coordination | TBD |
| X-003 | X:applying:completeness | MissingSlot | Specification | Specification | Add specification for transition zones between gravel driving surfaces and cement/gravel pads as recommended in Guidance | Guidance Considerations > Gravel Driving Surface recommends specifying "transition zones between paved/cement pads and gravel surfaces" but no requirement exists in Specification for this; total implementation coverage gap | Guidance.md; Specification.md | Guidance > Considerations > Gravel Driving Surface; Specification > entire document scanned | -- | PROPOSAL: Landscape Architect | TBD |
| X-004 | X:judging:necessity | VerificationGap | Specification | Specification | Add material testing requirements for cement pads (e.g., concrete cylinder testing, compressive strength verification); current verification entry says "material testing TBD" | Verification table for REQ-007-04-020-022 states "material testing TBD"; decisive adjudicative basis requires defined testing | Specification.md | Verification table > REQ-007-04-020-022 | -- | PROPOSAL: Structural/Civil Engineer | TBD |
| X-005 | X:reviewing:sufficiency | Conflict | Multi | NA | Resolve drainage feature scope: CONF-007-04-02 identifies unresolved assignment of drainage features (swales, ditches) between PKG-005 Civil and PKG-007 Landscape; examination rigor requires clear assignment before verification can be designed | Two decomposition entries make potentially overlapping claims about drainage feature design scope; adequate examination rigor cannot be applied without clear scope ownership | Guidance.md; Specification.md | Guidance > Conflict Table > CONF-007-04-02; Specification > Requirements > Site Drainage | Guidance.md#CONF-007-04-02 (PKG-005 "site grading with drainage features"); Guidance.md#CONF-007-04-02 (PKG-007 "integration with civil grading") | PROPOSAL: Per CONF-007-04-02 proposal -- PKG-005 leads, PKG-007 integrates | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Verified Directional Evidence | 1 | HAS_ITEMS | Missing erosion control evidence |
| E:guiding:information | guiding | information | Integrated Directional Narrative | 0 | NO_ITEMS | Guidance provides integrated narrative |
| E:guiding:knowledge | guiding | knowledge | Comprehensive Directional Mastery | 0 | NO_ITEMS | Knowledge base is proportionate to scope |
| E:guiding:wisdom | guiding | wisdom | Principled Directional Judgment | 0 | NO_ITEMS | Guidance principles and trade-offs show adequate judgment |
| E:applying:data | applying | data | Substantiated Practice Evidence | 1 | HAS_ITEMS | Normalization needed on equipment class |
| E:applying:information | applying | information | Integrated Practice Narrative | 0 | NO_ITEMS | Practice narrative is integrated across documents |
| E:applying:knowledge | applying | knowledge | Comprehensive Execution Mastery | 0 | NO_ITEMS | Execution knowledge is proportionate to scaffold state |
| E:applying:wisdom | applying | wisdom | Principled Execution Judgment | 0 | NO_ITEMS | Trade-off table demonstrates execution judgment |
| E:judging:data | judging | data | Verified Adjudicative Evidence | 1 | HAS_ITEMS | Inspection hold points missing |
| E:judging:information | judging | information | Integrated Assessment Narrative | 0 | NO_ITEMS | Assessment narrative in Verification table is coherent |
| E:judging:knowledge | judging | knowledge | Comprehensive Adjudicative Mastery | 0 | NO_ITEMS | Adjudicative knowledge base is adequate |
| E:judging:wisdom | judging | wisdom | Principled Adjudicative Wisdom | 0 | NO_ITEMS | Adjudicative approach shows principled reasoning |
| E:reviewing:data | reviewing | data | Substantiated Review Evidence | 0 | NO_ITEMS | Review evidence framework is adequate |
| E:reviewing:information | reviewing | information | Integrated Review Narrative | 0 | NO_ITEMS | Review narrative in Procedure is integrated |
| E:reviewing:knowledge | reviewing | knowledge | Comprehensive Review Mastery | 1 | HAS_ITEMS | Rationale gap for County review timing |
| E:reviewing:wisdom | reviewing | wisdom | Principled Examination Wisdom | 0 | NO_ITEMS | Examination approach demonstrates principled reasoning |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | TBD_Question | Specification | Specification | Record TBD: What erosion control measures and standards apply to restored areas? REQ-007-04-052 states areas "shall be stabilized against erosion" but no standard or method is cited. Source: Landscape Architect professional judgment and applicable Alberta standards | Verified directional evidence for erosion control is limited to an ASSUMPTION-tagged requirement with no supporting data or standard reference | Specification.md | Requirements > Planting and Site Restoration > REQ-007-04-052 | -- | PROPOSAL: Landscape Architect / Environmental consultant | TBD |
| E-002 | E:applying:data | Normalization | Multi | Guidance | Normalize equipment class terminology: "large construction equipment" and "motor scraper class" are used variably; define "motor scraper class" explicitly (e.g., typical axle load, gross vehicle weight) in Datasheet or Guidance | Datasheet says "Designed for weight and turning radius of large construction equipment (motor scraper class)" while Specification says "large construction equipment of motor scraper class" -- the parenthetical vs. direct usage differs and "motor scraper class" itself is undefined | Datasheet.md; Specification.md | Datasheet > Attributes > Gravel driving surface requirement; Specification > REQ-007-04-011 | -- | PROPOSAL: Civil Engineer to define design vehicle parameters | TBD |
| E-003 | E:judging:data | VerificationGap | Procedure | Procedure | Add inspection hold points to Procedure for gravel driving surface compaction and cement pad concrete placement; Procedure Step 4 references "inspection hold points" but none are enumerated | Procedure Step 4.1 requires "Define quality control requirements (testing, inspection hold points)" but the Verification table does not list specific hold points; verified adjudicative evidence requires defined inspection milestones | Procedure.md | Steps > Step 4 > 4.1; Verification table | -- | PROPOSAL: Landscape Architect / Construction Manager | TBD |
| E-004 | E:reviewing:knowledge | RationaleGap | Procedure | Guidance | Add rationale for County review sequencing: explain why DEL-007-01 must be approved before specification finalization and what happens if County directs changes that conflict with already-approved DEL-007-02/DEL-007-03 | Procedure Step 7 states County approval of DEL-007-01 must be on file before IFC, and Step 7.2 says "incorporate any County-directed changes," but no guidance exists for managing conflicts between County changes and approved upstream deliverables | Procedure.md; Guidance.md | Procedure > Steps > Step 7; Guidance > entire document scanned | -- | PROPOSAL: Project Manager | TBD |
