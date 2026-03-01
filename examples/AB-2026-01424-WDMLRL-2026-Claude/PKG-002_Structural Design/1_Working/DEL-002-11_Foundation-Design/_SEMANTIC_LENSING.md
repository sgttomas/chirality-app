# Semantic Lensing Register: DEL-002-11 Foundation Design Package (Variable-Price)

**Generated:** 2026-02-26
**Deliverable Folder:** PKG-002_Structural Design/1_Working/DEL-002-11_Foundation-Design/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-002-11_Foundation-Design/_CONTEXT.md
- _STATUS.md — DEL-002-11_Foundation-Design/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md — DEL-002-11_Foundation-Design/_SEMANTIC.md
- Datasheet.md — DEL-002-11_Foundation-Design/Datasheet.md
- Specification.md — DEL-002-11_Foundation-Design/Specification.md
- Guidance.md — DEL-002-11_Foundation-Design/Guidance.md
- Procedure.md — DEL-002-11_Foundation-Design/Procedure.md
- _REFERENCES.md — DEL-002-11_Foundation-Design/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 8
  - Specification: 10
  - Guidance: 4
  - Procedure: 2
  - Multi: 4
- By matrix:
  - A: 5  B: 3  C: 3  F: 4  D: 3  X: 5  E: 5
- By type:
  - Conflict: 1
  - VerificationGap: 6
  - MissingSlot: 8
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
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Seismic/snow/wind design values TBD |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Standards status all ASSUMPTION |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | No explicit code-edition verification method |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit path addressed via P.Eng. stamp and County approval |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Missing quality hold points |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Procedure steps are well-sequenced for execution |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Performance checks in Procedure Verification table |
| A:operative:reviewing | operative | reviewing | process audit | 1 | HAS_ITEMS | Peer review requirement weak |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Trade-offs section addresses value orientation adequately |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-off recommendations present and grounded |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Cost-performance tradeoffs documented in Guidance |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality appraisal covered by P.Eng. stamp and County review |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Datasheet | Datasheet | Confirm seismic zone, ground snow load, and wind load design values from NBC climatic data tables for project location (SW 14-44-21-W4, Ferintosh AB). Currently all marked "TBD -- location TBD." | Prescriptive direction for foundation design cannot be finalized without confirmed climatic/seismic design parameters. Three separate TBD entries exist (seismic zone, ground snow load, wind load) with no interim assumed values recorded. | Datasheet.md | Attributes table -- rows for "Seismic zone," "Ground snow load," "Wind load" | -- | PROPOSAL: Structural Engineer to confirm from NBC climatic appendix | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Clarify which edition of each standard (ABC, NBC, CSA A23.3, CSA S16, CSA A23.1/A23.2) governs. All entries in the Standards table carry "ASSUMPTION: applicable -- location TBD" status. Add confirmed edition years and Alberta adoption status. | Mandatory practice cannot be applied without knowing which edition of each code/standard is governing. The phrase "current edition" is ambiguous if the project spans multiple code-adoption dates. | Specification.md | Standards table | -- | PROPOSAL: Structural Engineer to confirm governing editions | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add verification step confirming which specific code edition was used in calculations and that it matches the Alberta-adopted edition at the time of design. | Compliance determination requires knowing not just that codes were followed, but that the correct edition was applied. No verification entry checks this. | Specification.md | Verification table -- REQ-004 row | -- | PROPOSAL: Structural Engineer | TBD |
| A-004 | A:operative:guiding | MissingSlot | Procedure | Procedure | Add explicit quality hold/gate points between phases (e.g., hold after Step 1.3 foundation concept before proceeding to cost estimate; hold after Step 2.3 calculations before drawing production). | Procedural direction would benefit from explicit hold points where work cannot proceed until a prior deliverable is reviewed. Currently, the phasing is sequential but no gates are formally identified. | Procedure.md | Steps -- Phase 1 and Phase 2 transitions | -- | PROPOSAL: Project Manager / Structural Engineer | TBD |
| A-005 | A:operative:reviewing | WeakStatement | Procedure | Procedure | Strengthen peer review requirement: Procedure Verification table states "Calculation package peer-reviewed by second engineer or senior reviewer" but this is the only mention. Add a step in Phase 2 requiring formal peer review sign-off before IFC stamp. | Process audit depends on a documented peer review step. The current mention is in the Verification table only, not in the procedural steps themselves, creating a risk it is treated as optional. | Procedure.md | Verification table -- "Structural calculations complete and internally consistent" row; Steps -- Step 2.7 | -- | PROPOSAL: Structural Engineer / QA Manager | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Frost depth assumption range vs. precision |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Bearing capacity assumption lacks range |
| B:data:completeness | data | completeness | comprehensive record | 0 | NO_ITEMS | Datasheet Attributes table is comprehensive for known parameters |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Data entries internally consistent within Datasheet |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key interface signals identified in Datasheet Conditions |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for each condition is adequate |
| B:information:completeness | information | completeness | comprehensive account | 1 | HAS_ITEMS | Groundwater assumption not in Datasheet |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messages across documents are coherent |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Structural engineering fundamentals properly invoked |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise requirements defined via P.Eng. stamp |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Scope of structural knowledge adequately covered |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding consistent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Key judgment calls identified (trade-offs in Guidance) |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-off section provides adequate judgment framing |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance provides holistic view of phasing and risk |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning consistent with variable-price logic throughout |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | WeakStatement | Datasheet | Datasheet | Specify assumed frost depth as a single design value (or narrow range) rather than "approximately 1.5-2.0 m." Procedure Step 1.1 uses the same range. A design calculation requires a single value or a clearly stated conservative bound. | Essential fact for foundation embedment depth is stated as a 0.5 m range, which is too wide for a footing depth calculation. The engineer must commit to a design value (e.g., "assume 2.0 m conservatively"). | Datasheet.md | Attributes table -- "Frost depth (design value)" row | -- | PROPOSAL: Structural Engineer | TBD |
| B-002 | B:data:sufficiency | MissingSlot | Datasheet | Datasheet | Add an assumed allowable bearing capacity range for normal ground conditions (e.g., 100-150 kPa as stated in Procedure Step 1.1) to the Datasheet Attributes table. Currently "TBD -- dependent on geotechnical report" with no interim assumption recorded in the Datasheet. | Adequate evidence for proposal-phase design requires a stated assumed bearing capacity. Procedure Step 1.1 provides 100-150 kPa but this does not appear in the Datasheet, which is the authoritative parameter register. | Datasheet.md, Procedure.md | Datasheet Attributes -- "Allowable bearing capacity" row; Procedure Steps -- Step 1.1 item 3 | -- | PROPOSAL: Structural Engineer | TBD |
| B-003 | B:information:completeness | MissingSlot | Datasheet | Datasheet | Add assumed groundwater condition to Datasheet Attributes table (e.g., "Groundwater: assumed absent under normal conditions per RFP 4.8.2 -- ASSUMPTION"). Procedure Step 1.1 mentions "no deleterious groundwater" but Datasheet has no groundwater entry. | Comprehensive account of subsurface assumptions is incomplete without a groundwater assumption record. This is stated in Procedure but absent from the Datasheet parameter register. | Datasheet.md, Procedure.md | Datasheet Attributes table (entire table scanned -- no groundwater row); Procedure Steps -- Step 1.1 item 3 | -- | PROPOSAL: Structural Engineer | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Prerequisite Standard | 1 | HAS_ITEMS | Safety Codes Act enforcement path unclear |
| C:normative:sufficiency | normative | sufficiency | Codified Capacity Threshold | 0 | NO_ITEMS | Threshold language present in requirements |
| C:normative:completeness | normative | completeness | Exhaustive Compliance Record | 1 | HAS_ITEMS | Missing Alberta Safety Codes Act verification |
| C:normative:consistency | normative | consistency | Harmonized Regulatory Coherence | 0 | NO_ITEMS | Regulatory references consistent across documents |
| C:operative:necessity | operative | necessity | Critical Operational Prerequisite | 0 | NO_ITEMS | Prerequisites table in Procedure is comprehensive |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Practical Capacity | 0 | NO_ITEMS | Practical capacity demonstrated through phased approach |
| C:operative:completeness | operative | completeness | Comprehensive Execution Coverage | 1 | HAS_ITEMS | Settlement analysis not in Specification requirements |
| C:operative:consistency | operative | consistency | Disciplined Process Alignment | 0 | NO_ITEMS | Process steps align with Specification requirements |
| C:evaluative:necessity | evaluative | necessity | Indispensable Worth Benchmark | 0 | NO_ITEMS | Worth benchmarks present (heavy industrial floor, motor scraper class) |
| C:evaluative:sufficiency | evaluative | sufficiency | Defensible Quality Appraisal | 0 | NO_ITEMS | Quality appraisal path defined through P.Eng. stamp |
| C:evaluative:completeness | evaluative | completeness | Holistic Value Accounting | 0 | NO_ITEMS | Trade-offs cover major value decisions |
| C:evaluative:consistency | evaluative | consistency | Principled Value Consistency | 0 | NO_ITEMS | Value reasoning consistent (do not under-design) |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | RationaleGap | Guidance | Guidance | Add guidance on Alberta Safety Codes Act compliance pathway -- how the foundation design is submitted for or assessed against Safety Codes (e.g., building permit review, Safety Codes Officer involvement). | Enforceable prerequisite standard: the Alberta Safety Codes Act is listed in the Standards table (Specification) as an explicit requirement, but no document explains the compliance pathway or what specific Safety Codes obligations apply to foundation design. | Specification.md, Guidance.md | Specification Standards table -- "Alberta Safety Codes Act" row; Guidance entire document scanned | -- | PROPOSAL: Project Manager / Structural Engineer | TBD |
| C-002 | C:normative:completeness | VerificationGap | Specification | Specification | Add verification entry for Alberta Safety Codes Act compliance (REQ-004 references it but the Verification table does not have a separate check for Safety Codes distinct from ABC/NBC). | Exhaustive compliance record requires that each regulatory obligation has a verification path. The Safety Codes Act is listed as a separate standard but shares a single verification row with ABC/NBC code compliance. | Specification.md | Verification table -- REQ-004 row; Standards table -- "Alberta Safety Codes Act" row | -- | PROPOSAL: Structural Engineer | TBD |
| C-003 | C:operative:completeness | MissingSlot | Specification | Specification | Add a requirement (or sub-requirement under REQ-003 or REQ-006) for settlement analysis -- differential and total settlement limits for the structure type. Procedure Step 2.3 includes "Settlement analysis: confirm acceptable differential settlement" but no corresponding Specification requirement exists. | Comprehensive execution coverage: the Procedure includes settlement analysis as a calculation task, but there is no normative requirement in the Specification mandating settlement limits or analysis. This means the Procedure prescribes work that is not formally required. | Specification.md, Procedure.md | Specification Requirements section (entire section scanned); Procedure Steps -- Step 2.3 item 2 | -- | PROPOSAL: Structural Engineer | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandatory Conformance Basis | 1 | HAS_ITEMS | Concrete mix design requirement missing |
| F:normative:sufficiency | normative | sufficiency | Authoritative Compliance Proof | 1 | HAS_ITEMS | No verification for IFC coordination |
| F:normative:completeness | normative | completeness | Total Statutory Coverage | 0 | NO_ITEMS | Statutory coverage adequate for identified codes |
| F:normative:consistency | normative | consistency | Governing Conformance Standard | 0 | NO_ITEMS | Conformance standards consistently referenced |
| F:operative:necessity | operative | necessity | Essential Readiness Condition | 0 | NO_ITEMS | Prerequisites identified in Procedure |
| F:operative:sufficiency | operative | sufficiency | Confirmed Delivery Capability | 1 | HAS_ITEMS | Crane data dependency unclear |
| F:operative:completeness | operative | completeness | Complete Capability Inventory | 0 | NO_ITEMS | Capability inventory complete in Procedure prerequisites |
| F:operative:consistency | operative | consistency | Uniform Delivery Standard | 0 | NO_ITEMS | Delivery standard consistent across phases |
| F:evaluative:necessity | evaluative | necessity | Fundamental Quality Imperative | 0 | NO_ITEMS | Quality imperatives addressed (heavy industrial standard) |
| F:evaluative:sufficiency | evaluative | sufficiency | Justified Worth Assessment | 1 | HAS_ITEMS | No rationale for foundation type assumption |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Appraisal Scope | 0 | NO_ITEMS | Appraisal scope adequate |
| F:evaluative:consistency | evaluative | consistency | Principled Appraisal Coherence | 0 | NO_ITEMS | Appraisal principles consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | MissingSlot | Specification | Specification | Add requirement referencing CSA A23.1/A23.2 for concrete materials and methods (mix design, placement, testing requirements). CSA A23.1/A23.2 is listed in the Standards table but no Specification requirement explicitly invokes it. | Mandatory conformance basis: CSA A23.1/A23.2 appears in the Standards table but has no corresponding requirement. If the standard is applicable, there should be a requirement governing concrete materials and methods for the foundation. | Specification.md | Standards table -- "CSA A23.1/A23.2" row; Requirements section (entire section scanned) | -- | PROPOSAL: Structural Engineer | TBD |
| F-002 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add verification entry for REQ-013 (IFC coordination). Currently the Verification table has an entry but the check ("foundation plan cross-referenced against... no unresolved clashes") does not specify who performs the coordination check or what evidence is retained. Strengthen to match the Procedure Step 2.5 discipline-by-discipline approach. | Authoritative compliance proof for inter-discipline coordination is weak. The verification approach is a single sentence whereas the Procedure devotes an entire step (Step 2.5) with five sub-steps to coordination. The verification should reflect this rigor. | Specification.md, Procedure.md | Specification Verification table -- REQ-013 row; Procedure Steps -- Step 2.5 | -- | PROPOSAL: Structural Engineer / Project Manager | TBD |
| F-003 | F:operative:sufficiency | TBD_Question | Multi | Procedure | Clarify at what point crane technical data (wheel loads, rail spacing, bridge span) must be available. Procedure lists it as a prerequisite but marks it "REQUIRED for crane column base and foundation design" without specifying if proposal-phase design can proceed without it, or if assumed crane loads should be used. | Confirmed delivery capability for crane base design depends on supplier data that may not be available during proposal phase. The Procedure does not address what to do if crane data is unavailable at proposal time. | Procedure.md, Guidance.md | Procedure Prerequisites table -- "Crane technical data" row; Guidance Considerations -- "Crane Support Interface" | -- | PROPOSAL: Structural Engineer / Procurement | TBD |
| F-004 | F:evaluative:sufficiency | RationaleGap | Guidance | Guidance | Add rationale for the assumption of spread footings as the baseline foundation type. The Trade-offs table recommends "Design for spread footings on assumed normal conditions" but does not explain why spread footings were selected over other options (e.g., drilled piers, helical piles) for this specific site and loading scenario. | Justified worth assessment: the assumed foundation type (spread footings) is a consequential design decision that drives cost estimates and construction approach. The current rationale is generic ("lower cost, simpler") without site-specific justification. | Guidance.md | Trade-offs table -- "Foundation type on assumed conditions" row | -- | PROPOSAL: Structural Engineer | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Resolved Authoritative Mandate | 0 | NO_ITEMS | Mandate is clear: variable-price + code-compliant design |
| D:normative:applying | normative | applying | Definitive Compliance Enactment | 1 | HAS_ITEMS | OBJ-001 mapping ambiguity |
| D:normative:judging | normative | judging | Conclusive Regulatory Ruling | 0 | NO_ITEMS | Regulatory ruling path defined via P.Eng. stamp |
| D:normative:reviewing | normative | reviewing | Resolved Governance Inspection | 0 | NO_ITEMS | County approval step provides governance review |
| D:operative:guiding | operative | guiding | Confirmed Process Stewardship | 1 | HAS_ITEMS | Schedule milestone gap |
| D:operative:applying | operative | applying | Resolved Delivery Execution | 0 | NO_ITEMS | Delivery execution well-defined in Procedure |
| D:operative:judging | operative | judging | Confirmed Efficacy Judgment | 0 | NO_ITEMS | Efficacy checks in Procedure Verification table |
| D:operative:reviewing | operative | reviewing | Resolved Process Verification | 0 | NO_ITEMS | Process verification addressed |
| D:evaluative:guiding | evaluative | guiding | Resolved Value Direction | 0 | NO_ITEMS | Value direction clear (do not under-design for cost) |
| D:evaluative:applying | evaluative | applying | Confirmed Worth Realization | 1 | HAS_ITEMS | No examples section populated |
| D:evaluative:judging | evaluative | judging | Definitive Valuation Scope | 0 | NO_ITEMS | Valuation scope addressed via cost estimate mechanism |
| D:evaluative:reviewing | evaluative | reviewing | Resolved Integrity Appraisal | 0 | NO_ITEMS | Integrity appraisal through P.Eng. stamp and peer review |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | Conflict | Multi | TBD | Resolve whether DEL-002-11 should formally support OBJ-001 ("Deliver a code-compliant, fully functional maintenance shop addition") in addition to OBJ-003 and OBJ-006. Guidance CFT-001 already flags this. Datasheet and Specification currently list OBJ-003, OBJ-006 only. | Definitive compliance enactment requires clarity on which objectives this deliverable formally serves. The foundation is intrinsic to OBJ-001 (code-compliant building) yet is not mapped to it. This was already identified in Guidance CFT-001 but has not been resolved. | Datasheet.md, Guidance.md | Datasheet Identification -- "Supports Objectives" row; Guidance Conflict Table -- CFT-001 | Datasheet.md#Identification (OBJ-003, OBJ-006) vs. Decomposition OBJ-001 | PROPOSAL: Accept current mapping per Guidance CFT-001 proposed authority, unless human rules otherwise | TBD |
| D-002 | D:operative:guiding | MissingSlot | Specification | Specification | Add schedule milestone requirement: specify when the proposal-phase foundation cost estimate must be ready (tied to proposal submission date) and when IFC foundation drawings must be complete (tied to construction start for PKG-010). REQ-014 says "sufficient time" but provides no dates or milestone references. | Confirmed process stewardship requires schedule clarity. REQ-014 uses the phrase "in sufficient time to support construction completion on or before December 31, 2026" which does not provide actionable milestone dates. | Specification.md | Requirements -- REQ-014 | -- | PROPOSAL: Project Manager / Structural Engineer | TBD |
| D-003 | D:evaluative:applying | MissingSlot | Guidance | Guidance | Populate the Examples section with at least one precedent reference (e.g., comparable industrial foundation designs in central Alberta glacial till conditions) or explicitly state why no examples are available and what the engineer should reference instead. | Confirmed worth realization benefits from precedent. The Guidance Examples section is "TBD" with a note to reference comparable structures, but no specific precedent is identified, reducing the practical utility of the section. | Guidance.md | Examples section | -- | PROPOSAL: Structural Engineer | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Confirmed Essential Authority | 0 | NO_ITEMS | Essential authority confirmed through RFP and code references |
| X:guiding:sufficiency | guiding | sufficiency | Authorized Scope Rationale | 1 | HAS_ITEMS | Exclusions list may be incomplete |
| X:guiding:completeness | guiding | completeness | Exhaustive Directive Purview | 0 | NO_ITEMS | Directive purview adequately covered |
| X:guiding:consistency | guiding | consistency | Coherent Directive Alignment | 0 | NO_ITEMS | Directives aligned across documents |
| X:applying:necessity | applying | necessity | Essential Enactment Foundation | 1 | HAS_ITEMS | REQ-006 equipment class vague |
| X:applying:sufficiency | applying | sufficiency | Viable Execution Evidence | 1 | HAS_ITEMS | Mezzanine loads not quantified |
| X:applying:completeness | applying | completeness | Exhaustive Implementation Record | 0 | NO_ITEMS | Implementation record structure adequate |
| X:applying:consistency | applying | consistency | Consistent Deployment Standard | 0 | NO_ITEMS | Deployment standard consistent |
| X:judging:necessity | judging | necessity | Mandatory Assessment Basis | 1 | HAS_ITEMS | No verification for ASSUMPTION items |
| X:judging:sufficiency | judging | sufficiency | Defensible Ruling Capacity | 0 | NO_ITEMS | Ruling capacity adequate for identified requirements |
| X:judging:completeness | judging | completeness | Exhaustive Judgment Purview | 0 | NO_ITEMS | Judgment purview covered by Verification tables |
| X:judging:consistency | judging | consistency | Coherent Judgment Standard | 0 | NO_ITEMS | Judgment standards consistent |
| X:reviewing:necessity | reviewing | necessity | Essential Audit Foundation | 1 | HAS_ITEMS | Transmittal record verification missing |
| X:reviewing:sufficiency | reviewing | sufficiency | Sufficient Audit Capacity | 0 | NO_ITEMS | Audit capacity sufficient for current scope |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Review Record | 0 | NO_ITEMS | Review record structure adequate |
| X:reviewing:consistency | reviewing | consistency | Consistent Audit Standard | 0 | NO_ITEMS | Audit standard consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | MissingSlot | Specification | Specification | Add explicit exclusion: "Foundation design for the existing Old North Shop or any renovation work (PKG-017)." The exclusions list mentions PKG-017 renovation but could be more explicit about what "foundation design for any structure other than the Addition" means in the context of potential shared site work. | Authorized scope rationale: the exclusion "Foundation design for any structure other than the Addition" is correct but the neighboring renovation scope (PKG-017 Old North Shop) could create scope boundary confusion if site grading or shared foundations are involved. | Specification.md | Scope -- "What This Deliverable Excludes" | -- | PROPOSAL: Project Manager | TBD |
| X-002 | X:applying:necessity | WeakStatement | Specification | Specification | Quantify or reference a specific equipment class for floor load design in REQ-006. "Heavy tracked and packer equipment (minimum motor scraper class)" is descriptive but does not provide a design load value (e.g., kPa or point load in kN). The engineer must determine this, and the requirement should either state the load or require the engineer to document the assumed load. | Essential enactment foundation: REQ-006 uses qualitative language ("motor scraper class") without a quantitative load value. Different motor scraper models have very different weights, and the requirement does not specify which class or weight to design for. | Specification.md | Requirements -- REQ-006 | -- | PROPOSAL: Structural Engineer | TBD |
| X-003 | X:applying:sufficiency | VerificationGap | Specification | Specification | Add verification approach for mezzanine load path (REQ-008): specify that the load path from mezzanine columns to footings must be documented in the calculation package, including the design live load assumed for the mezzanine. Currently the verification says "mezzanine dead + live load transferred to foundation elements; load path from mezzanine to footing documented" but does not require the assumed mezzanine live load to be stated. | Viable execution evidence: the mezzanine stores "heavy items including oil totes and pumping equipment" but no design live load is specified anywhere. The verification should require the assumed mezzanine live load to be documented and justified. | Specification.md | Verification table -- REQ-008 row; Requirements -- REQ-008 | -- | PROPOSAL: Structural Engineer | TBD |
| X-004 | X:judging:necessity | VerificationGap | Specification | Specification | Add a verification mechanism for tracking all ASSUMPTION items and confirming each is either validated or revised upon receipt of the geotechnical report (DEL-008-01). Currently, individual requirements mention assumptions but there is no consolidated tracking or verification step. | Mandatory assessment basis: the deliverable contains numerous ASSUMPTION tags (frost depth, bearing capacity, foundation type, groundwater, code editions) but no formal mechanism to verify that all assumptions are tracked and resolved post-geotech. | Specification.md, Datasheet.md | Specification Requirements (multiple); Datasheet Attributes (multiple "ASSUMPTION" entries) | -- | PROPOSAL: Structural Engineer | TBD |
| X-005 | X:reviewing:necessity | VerificationGap | Procedure | Procedure | Add verification check confirming that IFC drawing transmittal records are created and retained per Procedure Step 2.7 item 4. The Records table lists "IFC Drawing Transmittal Record" but the Procedure Verification table does not include a check for transmittal record completion. | Essential audit foundation: the Records table identifies transmittal records as required evidence, but the Verification table does not include a check for their creation, creating a gap between what is required to be recorded and what is verified. | Procedure.md | Verification table (entire table scanned); Records table -- "IFC Drawing Transmittal Record" row | -- | PROPOSAL: Project Manager | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Factual Basis | 1 | HAS_ITEMS | Datasheet construction section vs. Spec loads |
| E:guiding:information | guiding | information | Coherent Steering Narrative | 0 | NO_ITEMS | Steering narrative coherent across Guidance and Procedure |
| E:guiding:knowledge | guiding | knowledge | Commanding Expert Purview | 0 | NO_ITEMS | Expert purview adequately scoped |
| E:guiding:wisdom | guiding | wisdom | Principled Steering Judgment | 0 | NO_ITEMS | Steering judgment principles well-articulated in Guidance |
| E:applying:data | applying | data | Verified Execution Baseline | 1 | HAS_ITEMS | Building footprint units inconsistency |
| E:applying:information | applying | information | Coherent Execution Narrative | 0 | NO_ITEMS | Execution narrative coherent |
| E:applying:knowledge | applying | knowledge | Integrated Execution Mastery | 0 | NO_ITEMS | Execution mastery adequately described |
| E:applying:wisdom | applying | wisdom | Grounded Execution Judgment | 0 | NO_ITEMS | Execution judgment grounded in trade-offs |
| E:judging:data | judging | data | Defensible Assessment Record | 1 | HAS_ITEMS | Datasheet References location TBD entries |
| E:judging:information | judging | information | Coherent Verdict Narrative | 0 | NO_ITEMS | Verdict narrative coherent |
| E:judging:knowledge | judging | knowledge | Skilled Adjudication Mastery | 0 | NO_ITEMS | Adjudication mastery addressed through P.Eng. requirement |
| E:judging:wisdom | judging | wisdom | Principled Adjudication Insight | 0 | NO_ITEMS | Adjudication insight present in Guidance |
| E:reviewing:data | reviewing | data | Verified Examination Evidence | 1 | HAS_ITEMS | Documentation artifacts all TBD status |
| E:reviewing:information | reviewing | information | Coherent Audit Narrative | 0 | NO_ITEMS | Audit narrative coherent |
| E:reviewing:knowledge | reviewing | knowledge | Skilled Examination Mastery | 0 | NO_ITEMS | Examination mastery scoped |
| E:reviewing:wisdom | reviewing | wisdom | Principled Examination Insight | 1 | HAS_ITEMS | Variable-price renegotiation trigger unclear |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | Normalization | Multi | Datasheet | Normalize "steel plates embedded in concrete floor" (Datasheet Construction) with "steel plate embedment locations" (Specification REQ-006) and "steel plate embedments at strategic floor locations" (Guidance P-3). Adopt a consistent term (e.g., "steel plate embedments") and reference the Appendix B locations consistently. | Authoritative factual basis: the steel plate feature is described with slightly different phrasing across three documents, creating minor terminology drift. Consistent naming reduces ambiguity for the engineer and contractor. | Datasheet.md, Specification.md, Guidance.md | Datasheet Construction -- "Floor loads -- general" and "Embedments" rows; Specification Requirements -- REQ-006; Guidance Principles -- P-3 | -- | PROPOSAL: Structural Engineer | TBD |
| E-002 | E:applying:data | Normalization | Multi | Datasheet | Normalize unit convention: Datasheet uses imperial (130 ft x 100 ft, 35 feet, 24 ft) throughout, Procedure Step 1.1 also uses imperial, but assumed geotechnical parameters use metric (1.5-2.0 m, 100-150 kPa). Adopt a stated convention (e.g., "Imperial for architectural dimensions, metric for geotechnical parameters per Canadian engineering practice") or convert to a single system. | Verified execution baseline: mixed unit systems (imperial for building dimensions, metric for geotechnical parameters) are present across documents without an explicit convention statement. This is common in Canadian practice but should be acknowledged. | Datasheet.md, Procedure.md | Datasheet Attributes -- building footprint (ft), frost depth (m); Procedure Steps -- Step 1.1 | -- | PROPOSAL: Structural Engineer | TBD |
| E-003 | E:judging:data | Normalization | Datasheet | Datasheet | Update Datasheet References table to replace "location TBD" entries for NBC, ABC, CSA A23.3, CSA S16 with actual document locations or a note "To be sourced by Structural Engineer from reference library." The "location TBD" notation is ambiguous -- it could mean the document has not been obtained or that the reference location within the project file structure is unknown. | Defensible assessment record: four reference entries carry "location TBD" which weakens the reference traceability. These are industry-standard codes that the engineer of record must possess; the notation should clarify what "location TBD" means in this context. | Datasheet.md | References table -- NBC, ABC, CSA A23.3, CSA S16 rows | -- | PROPOSAL: Structural Engineer | TBD |
| E-004 | E:reviewing:data | RationaleGap | Specification | Guidance | Add rationale for why all Documentation artifacts are "TBD -- to be produced" and what governs the order/priority of their production. The Specification Documentation table lists five artifacts all at "TBD" status with no indication of which are produced first or dependencies between them. | Verified examination evidence: all five anticipated artifacts are listed as TBD with no production sequence or priority indicated. A reviewer cannot assess progress without understanding the expected order of production. | Specification.md | Documentation table | -- | PROPOSAL: Structural Engineer / Project Manager | TBD |
| E-005 | E:reviewing:wisdom | TBD_Question | Guidance | Guidance | Clarify the specific contractual mechanism under CCDC 14-2013 for the variable-price re-negotiation. Guidance P-1 and Procedure Step 2.1/2.8 reference re-negotiation per CCDC 14-2013 and RFP 4.8.2, but the specific CCDC clause or change order mechanism is not identified. The Structural Engineer and Project Manager need to know which CCDC provision governs. | Principled examination insight: the variable-price re-negotiation is a critical commercial mechanism but the specific CCDC 14-2013 clause is never cited. Without this, the re-negotiation process lacks contractual grounding in the design documents. | Guidance.md, Procedure.md | Guidance Principles -- P-1; Procedure Steps -- Step 2.1 item 2, Step 2.8 | -- | PROPOSAL: Project Manager / Contract Administrator | TBD |
