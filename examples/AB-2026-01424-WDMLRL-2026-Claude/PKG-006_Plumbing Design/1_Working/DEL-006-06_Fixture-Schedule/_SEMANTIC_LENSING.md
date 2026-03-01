# Semantic Lensing Register: DEL-006-06 Plumbing Fixture Schedule

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-006_Plumbing Design/1_Working/DEL-006-06_Fixture-Schedule/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-006-06_Fixture-Schedule/_CONTEXT.md (Deliverable Identity, Package PKG-006)
- _STATUS.md -- DEL-006-06_Fixture-Schedule/_STATUS.md (State: SEMANTIC_READY, 2026-02-26)
- _SEMANTIC.md -- DEL-006-06_Fixture-Schedule/_SEMANTIC.md (Matrices A, B, C, F, D, X, E parsed)
- Datasheet.md -- DEL-006-06_Fixture-Schedule/Datasheet.md (Identification, Attributes, Conditions, Construction)
- Specification.md -- DEL-006-06_Fixture-Schedule/Specification.md (Scope, REQ-001 through REQ-016, Standards, Verification)
- Guidance.md -- DEL-006-06_Fixture-Schedule/Guidance.md (Purpose, Principles, Considerations, Trade-offs, Examples)
- Procedure.md -- DEL-006-06_Fixture-Schedule/Procedure.md (Steps 1-9, Verification Checklist, Records)
- _REFERENCES.md -- DEL-006-06_Fixture-Schedule/_REFERENCES.md (R-01, R-06, SOW refs, OBJ refs)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 21
- By document:
  - Datasheet: 3
  - Specification: 9
  - Guidance: 4
  - Procedure: 4
  - Multi: 1
- By matrix:
  - A: 5  B: 3  C: 3  F: 3  D: 2  X: 3  E: 2
- By type:
  - Conflict: 0
  - VerificationGap: 5
  - MissingSlot: 5
  - WeakStatement: 4
  - RationaleGap: 3
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
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Accessibility code clause unspecified |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Emergency shower standard not confirmed |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Standards editions unconfirmed |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Verification table covers REQ-001 through REQ-016; audit trail adequate |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Steps 1-9 provide clear procedural direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Sump drain type/configuration unspecified |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Pre-Issue Checklist in Procedure covers performance checks |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Procedure Step 7 internal QC and records section adequate |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Principle 2 establishes industrial value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 1 | HAS_ITEMS | Trade-off 1 guidance on manufacturer vs performance spec lacks decision criteria |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Trade-off 2 in Guidance addresses granularity worth |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Procedure Step 7 and Pre-Issue Checklist serve quality review |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify which specific Alberta Building Code accessibility clauses apply to washroom fixtures; resolve ASSUMPTION tag in REQ-012 | REQ-012 states accessibility compliance is required but relies on an ASSUMPTION for the governing code clause. Without a specific code reference, compliance determination is ambiguous. | Specification.md | REQ-012 -- Accessibility Compliance | -- | Plumbing Engineer / Alberta Building Code | TBD |
| A-002 | A:normative:applying | TBD_Question | Specification | Specification | Confirm applicable emergency shower standard (ANSI/ASSE 1009 or equivalent) and record specific edition in Standards table | The emergency shower is safety-critical (Guidance Principle 4) but the governing standard is marked ASSUMPTION throughout. Mandatory practice requires a confirmed standard reference. | Specification.md | REQ-005, Standards table | -- | Plumbing Engineer / safety codes officer | TBD |
| A-003 | A:normative:judging | WeakStatement | Specification | Specification | Confirm and record specific editions of Alberta Building Code, Alberta Plumbing Code, and NPC in the Standards table | All three primary code references carry "ASSUMPTION: likely applicable (location TBD)" status. Compliance determination cannot proceed without confirmed editions. | Specification.md | Standards table | -- | Plumbing Engineer | TBD |
| A-004 | A:operative:applying | MissingSlot | Datasheet | Datasheet | Add sump drain type/configuration attributes (e.g., trench drain vs. point drain, material, trap type) to Drainage System Attributes or fixture table | Sump drains are required (REQ-004, SOW-0045) but Datasheet lists them only as a line item with no technical attributes. Practical execution requires material and configuration data. | Datasheet.md | Drainage System Attributes | -- | Plumbing Engineer | TBD |
| A-005 | A:evaluative:applying | RationaleGap | Guidance | Guidance | Add decision criteria or weighting factors for choosing manufacturer-named vs. performance specification approach per fixture category | Trade-off 1 identifies the choice but does not provide criteria for when to use each approach. The ASSUMPTION about "or approved equal" is not grounded in a stated rationale. | Guidance.md | Trade-off 1: Manufacturer Specification vs. Performance Specification | -- | Plumbing Engineer / project procurement | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Washroom fixture count for New North Shop is TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet fixture table provides adequate evidence from conceptual drawing |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Laundry fixture specifics missing |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Quantities consistently labeled as conceptual/minimum; measurement basis stated |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | SOW references provide essential traceability signals throughout |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequately established across documents |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | All four documents provide cross-referencing comprehensive accounts |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology inconsistency for wash station/sink |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Industrial context and design basis well established |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Engineering competence requirements clear (P.Eng. stamp, code review) |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Cross-discipline coordination table in Datasheet covers scope |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding of design-build workflow consistent across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Guidance Principles and Considerations provide essential judgment framing |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-offs section provides adequate judgment guidance |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Consideration A-E in Guidance covers holistic view |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Guidance principles internally consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add essential fixture data for New North Shop washroom: toilet count, lavatory count, and fixture types are TBD with no minimum stated | The New North Shop washroom is shown on the conceptual drawing with a drain label but no fixture detail. The Datasheet lists "Washroom Fixtures" for Old North Shop only. New North Shop washroom fixture data is an essential fact gap. | Datasheet.md | Fixtures Identified in Conceptual Plumbing Drawing | -- | Plumbing Engineer / Architect (floor plan) | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add laundry services fixture specifics: washer connection type, dryer vent/gas rough-in, hot/cold supply sizing | Laundry services row in Datasheet shows "TBD" for quantity and has no technical attributes. Guidance Examples table lists expected rough-in items but Datasheet does not carry them as data. | Datasheet.md | Fixtures Identified in Conceptual Plumbing Drawing -- Laundry Services row | -- | Plumbing Engineer | TBD |
| B-003 | B:information:consistency | Normalization | Multi | Guidance | Normalize terminology: "wash station" vs. "industrial wash sink" vs. "wash sink" -- adopt one canonical term and use consistently | Specification REQ-007 says "industrial wash sink (wash station)"; Guidance Examples table lists "Industrial Wash Sink" as category but "Stainless or cast iron wash sink / trough" as example; Datasheet uses "Wash Station". The RFP says "separate industrial wash sink." Inconsistent naming risks procurement confusion. | Datasheet.md, Specification.md, Guidance.md | Datasheet#Fixtures table, Specification#REQ-007, Guidance#Examples table | -- | Plumbing Engineer (choose canonical term) | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Obligatory Compliance Basis | 1 | HAS_ITEMS | Occupancy classification not stated |
| C:normative:sufficiency | normative | sufficiency | Mandated Adequacy Standard | 0 | NO_ITEMS | REQ-001 through REQ-016 provide mandated adequacy structure |
| C:normative:completeness | normative | completeness | Total Regulatory Coverage | 1 | HAS_ITEMS | Eyewash station not addressed |
| C:normative:consistency | normative | consistency | Harmonized Compliance Regime | 0 | NO_ITEMS | Compliance references consistently flagged as ASSUMPTION across docs |
| C:operative:necessity | operative | necessity | Critical Functional Threshold | 0 | NO_ITEMS | Procedure prerequisites table establishes critical thresholds |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Operational Readiness | 0 | NO_ITEMS | Step 3 and prerequisites adequately frame readiness |
| C:operative:completeness | operative | completeness | Total Operational Accounting | 0 | NO_ITEMS | Steps 1-9 cover full operational sequence |
| C:operative:consistency | operative | consistency | Disciplined Process Uniformity | 0 | NO_ITEMS | Procedure steps reference consistent source documents |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Worth Recognition | 0 | NO_ITEMS | Guidance Purpose section establishes intrinsic worth of schedule |
| C:evaluative:sufficiency | evaluative | sufficiency | Warranted Merit Judgment | 0 | NO_ITEMS | Trade-offs section frames merit judgment adequately |
| C:evaluative:completeness | evaluative | completeness | Exhaustive Worth Accounting | 1 | HAS_ITEMS | No lifecycle/maintenance value consideration |
| C:evaluative:consistency | evaluative | consistency | Principled Value Coherence | 0 | NO_ITEMS | Value principles consistent across Guidance |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | MissingSlot | Specification | Specification | Add building occupancy classification (e.g., Group F, Division 2 or 3 per ABC) to establish code-required minimum fixture counts | The binding compliance basis for plumbing fixture counts is the building occupancy classification under the Alberta Building Code. Neither Specification nor Datasheet states the occupancy classification. Without it, minimum fixture count requirements cannot be verified. | Specification.md, Datasheet.md | Specification#Standards, Datasheet#Design Conditions | -- | Architect / Plumbing Engineer | TBD |
| C-002 | C:normative:completeness | TBD_Question | Specification | Specification | Determine whether an eyewash station is required in addition to the emergency shower, and if so, add as a requirement | Emergency shower is specified (REQ-005) but Guidance Examples table mentions "ANSI-compliant combination shower/eyewash unit (ASSUMPTION)." If an eyewash is required, it should be a separate requirement or explicitly combined with the shower. Total regulatory coverage requires this to be resolved. | Specification.md, Guidance.md | Specification#REQ-005, Guidance#Examples table -- Emergency Shower row | -- | Plumbing Engineer / safety codes officer | TBD |
| C-003 | C:evaluative:completeness | RationaleGap | Guidance | Guidance | Add consideration for fixture lifecycle/maintenance value: replacement parts availability, industrial-grade warranty expectations, and long-term cost implications for rural location | Guidance addresses durability (Principle 2) and procurement (Trade-off 1) but does not consider lifecycle cost or maintenance burden. For a rural landfill facility, parts availability and long-term value are material to fixture selection worth. | Guidance.md | Principles, Considerations | -- | Plumbing Engineer / Owner (Camrose County) | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Absolute Compliance Mandate | 0 | NO_ITEMS | REQ-001 through REQ-016 establish compliance mandates |
| F:normative:sufficiency | normative | sufficiency | Prescribed Verification Standard | 1 | HAS_ITEMS | REQ-012 verification method weak |
| F:normative:completeness | normative | completeness | Exhaustive Regulatory Register | 0 | NO_ITEMS | Standards table lists applicable codes; ASSUMPTION flags are appropriate for current stage |
| F:normative:consistency | normative | consistency | Systematic Compliance Alignment | 0 | NO_ITEMS | Requirements align with SOW and RFP references |
| F:operative:necessity | operative | necessity | Vital Operational Prerequisite | 1 | HAS_ITEMS | Architectural floor plan dependency timing unclear |
| F:operative:sufficiency | operative | sufficiency | Competent Execution Assurance | 0 | NO_ITEMS | Procedure prerequisites table establishes execution assurance |
| F:operative:completeness | operative | completeness | Complete Process Mastery | 0 | NO_ITEMS | Procedure covers complete process |
| F:operative:consistency | operative | consistency | Systematic Operational Reliability | 0 | NO_ITEMS | Consistent references to upstream dependencies |
| F:evaluative:necessity | evaluative | necessity | Foundational Worth Imperative | 0 | NO_ITEMS | Guidance Purpose establishes foundational worth |
| F:evaluative:sufficiency | evaluative | sufficiency | Justified Appraisal Warrant | 0 | NO_ITEMS | Trade-offs provide appraisal warrant |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Valuation Authority | 1 | HAS_ITEMS | No verification of value trade-off outcomes |
| F:evaluative:consistency | evaluative | consistency | Principled Valuation Discipline | 0 | NO_ITEMS | Valuation principles consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | VerificationGap | Specification | Specification | Strengthen verification method for REQ-012 (Accessibility): specify which accessibility standard clauses to check and define pass/fail criteria | Verification table for REQ-012 says only "Confirm accessibility notes present for washroom fixtures." This does not verify actual compliance -- only presence of notes. Prescribed verification requires substantive checking criteria. | Specification.md | Verification table -- REQ-012 row | -- | Plumbing Engineer | TBD |
| F-002 | F:operative:necessity | WeakStatement | Procedure | Procedure | Clarify prerequisite timing: state whether architectural floor plans (DEL-001-02, DEL-001-10) must be at a specific milestone (e.g., Design Development, IFC) before fixture schedule production begins | Procedure Prerequisites table lists architectural plans as "Dependency; coordinate" but does not specify what stage they must reach. Vital operational prerequisite requires clarity on dependency timing. | Procedure.md | Prerequisites -- Upstream Documents and Information Required | -- | Project Manager / Architect | TBD |
| F-003 | F:evaluative:completeness | VerificationGap | Specification | Procedure | Add verification step confirming that fixture selections align with stated value principles (industrial durability, serviceability, rural supply chain access) | The Guidance establishes value criteria (Principle 2, Trade-off 1) but neither the Specification Verification table nor the Procedure Pre-Issue Checklist verifies that fixture selections actually meet these criteria. Comprehensive valuation authority requires a check. | Specification.md, Procedure.md | Specification#Verification table, Procedure#Pre-Issue Checklist | -- | Plumbing Engineer | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Established Directive Authority | 0 | NO_ITEMS | RFP and code references establish directive authority |
| D:normative:applying | normative | applying | Confirmed Obligatory Practice | 0 | NO_ITEMS | REQ-001 through REQ-016 confirm obligatory practices |
| D:normative:judging | normative | judging | Authoritative Conformance Ruling | 0 | NO_ITEMS | Verification table maps each requirement to a method |
| D:normative:reviewing | normative | reviewing | Confirmed Compliance Verification | 1 | HAS_ITEMS | REQ-013 verification weak |
| D:operative:guiding | operative | guiding | Established Process Direction | 0 | NO_ITEMS | Procedure Steps 1-9 establish clear process direction |
| D:operative:applying | operative | applying | Assured Operational Delivery | 0 | NO_ITEMS | Step 4 and Step 8 assure delivery |
| D:operative:judging | operative | judging | Confirmed Performance Competence | 0 | NO_ITEMS | P.Eng. review step confirms competence |
| D:operative:reviewing | operative | reviewing | Verified Process Dependability | 0 | NO_ITEMS | Step 7 internal QC provides process verification |
| D:evaluative:guiding | evaluative | guiding | Grounded Value Stewardship | 0 | NO_ITEMS | Guidance Purpose and Principles ground value stewardship |
| D:evaluative:applying | evaluative | applying | Warranted Worth Deployment | 1 | HAS_ITEMS | No mechanism to confirm worth deployment in procurement |
| D:evaluative:judging | evaluative | judging | Definitive Appraisal Verdict | 0 | NO_ITEMS | Trade-offs provide appraisal framework |
| D:evaluative:reviewing | evaluative | reviewing | Confirmed Worth Assurance | 0 | NO_ITEMS | Records section captures documentation for assurance |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:reviewing | VerificationGap | Specification | Specification | Strengthen verification method for REQ-013 (Code Compliance): specify which code sections to verify against and define what "code references present" means substantively | Verification table for REQ-013 says "Confirm code references present." This checks for presence of references, not correctness or completeness of code compliance. Confirmed compliance verification requires substantive checking. | Specification.md | Verification table -- REQ-013 row | -- | Plumbing Engineer | TBD |
| D-002 | D:evaluative:applying | VerificationGap | Procedure | Procedure | Add a procurement-readiness check in Pre-Issue Checklist confirming that fixture specifications are sufficient for contractor pricing and procurement | Guidance Purpose states the schedule serves "procurement and installation teams" and "defines what is to be purchased." But no verification step confirms the schedule is actually procurement-ready (e.g., sufficient detail for pricing). Warranted worth deployment requires this assurance. | Procedure.md | Pre-Issue Checklist | -- | Plumbing Engineer / procurement | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Governance Imperative | 0 | NO_ITEMS | Guidance Principles establish foundational governance |
| X:guiding:sufficiency | guiding | sufficiency | Justified Leadership Warrant | 0 | NO_ITEMS | P.Eng. stamp requirement provides leadership warrant |
| X:guiding:completeness | guiding | completeness | Exhaustive Directional Scope | 0 | NO_ITEMS | Guidance Considerations A-E cover directional scope |
| X:guiding:consistency | guiding | consistency | Harmonized Directional Alignment | 1 | HAS_ITEMS | Coordination signoff not formally tracked |
| X:applying:necessity | applying | necessity | Mandatory Implementation Basis | 0 | NO_ITEMS | SOW items provide mandatory implementation basis |
| X:applying:sufficiency | applying | sufficiency | Warranted Execution Competence | 0 | NO_ITEMS | Prerequisites table establishes competence inputs |
| X:applying:completeness | applying | completeness | Total Implementation Coverage | 1 | HAS_ITEMS | Cleanout/minor fittings boundary unclear |
| X:applying:consistency | applying | consistency | Coherent Execution Uniformity | 0 | NO_ITEMS | Consistent execution approach across steps |
| X:judging:necessity | judging | necessity | Binding Adjudication Basis | 0 | NO_ITEMS | Requirements provide binding adjudication basis |
| X:judging:sufficiency | judging | sufficiency | Justified Adjudication Warrant | 0 | NO_ITEMS | Verification methods provide adjudication warrant |
| X:judging:completeness | judging | completeness | Comprehensive Adjudication Scope | 1 | HAS_ITEMS | Verification of renovation scope fixtures weak |
| X:judging:consistency | judging | consistency | Harmonized Adjudication Standard | 0 | NO_ITEMS | Verification methods follow consistent pattern |
| X:reviewing:necessity | reviewing | necessity | Fundamental Assurance Basis | 0 | NO_ITEMS | Records section provides assurance basis |
| X:reviewing:sufficiency | reviewing | sufficiency | Justified Assurance Evidence | 0 | NO_ITEMS | Pre-Issue Checklist provides assurance evidence |
| X:reviewing:completeness | reviewing | completeness | Comprehensive Audit Authority | 0 | NO_ITEMS | Records table comprehensive |
| X:reviewing:consistency | reviewing | consistency | Harmonized Audit Assurance | 0 | NO_ITEMS | Audit structure consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:consistency | MissingSlot | Procedure | Procedure | Add a formal coordination signoff record (e.g., discipline signoff log) to Step 6 or Records section to track that Architect, Mechanical, and Electrical coordination is complete | Procedure Step 6 directs cross-discipline coordination and Pre-Issue Checklist says "Coordination complete -- signed off." But there is no defined record or signoff mechanism in the Records table. Harmonized directional alignment requires traceable coordination evidence. | Procedure.md | Step 6 -- Coordinate with Other Disciplines, Records table | -- | Project Manager | TBD |
| X-002 | X:applying:completeness | WeakStatement | Guidance | Specification | Clarify the boundary between fixtures scheduled in DEL-006-06 and minor fittings/accessories addressed in DEL-006-08 (Plumbing Specification); define what "cleanouts and minor accessories" includes | Guidance Trade-off 2 says cleanouts and minor accessories "may be addressed in the Specification (DEL-006-08) rather than the schedule" but the boundary is not defined. Total implementation coverage requires a clear scope boundary. | Guidance.md | Trade-off 2: Fixture Schedule Granularity | -- | Plumbing Engineer | TBD |
| X-003 | X:judging:completeness | VerificationGap | Specification | Specification | Add explicit verification method for Old North Shop renovation fixtures (SOW-0072 washroom renovation scope beyond urinal) to confirm complete coverage of existing fixture replacement/retention decisions | Verification table for REQ-008 mentions "Confirm urinal and washroom fixture entries" but does not address the broader renovation scope (SOW-0072 existing washroom renovation). The verification should confirm that existing fixtures being retained, replaced, or added are all accounted for. | Specification.md | Verification table -- REQ-008 row | -- | Plumbing Engineer | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Guidance Record | 0 | NO_ITEMS | Guidance provides authoritative record with source citations |
| E:guiding:information | guiding | information | Strategic Governance Clarity | 0 | NO_ITEMS | Guidance Purpose and Principles provide strategic clarity |
| E:guiding:knowledge | guiding | knowledge | Integrated Governance Command | 0 | NO_ITEMS | Cross-discipline coordination knowledge established |
| E:guiding:wisdom | guiding | wisdom | Principled Strategic Foresight | 1 | HAS_ITEMS | Cold climate implications underexplored |
| E:applying:data | applying | data | Verified Deployment Record | 0 | NO_ITEMS | Datasheet fixture table and Procedure outputs provide deployment records |
| E:applying:information | applying | information | Actionable Execution Clarity | 0 | NO_ITEMS | Procedure steps provide actionable clarity |
| E:applying:knowledge | applying | knowledge | Integrated Execution Mastery | 0 | NO_ITEMS | Steps 1-9 integrate execution knowledge |
| E:applying:wisdom | applying | wisdom | Seasoned Execution Judgment | 0 | NO_ITEMS | Procedure applies engineering judgment appropriately |
| E:judging:data | judging | data | Verified Evidentiary Record | 0 | NO_ITEMS | Verification table provides evidentiary structure |
| E:judging:information | judging | information | Coherent Ruling Clarity | 0 | NO_ITEMS | Verification methods coherent |
| E:judging:knowledge | judging | knowledge | Authoritative Verdict Expertise | 0 | NO_ITEMS | P.Eng. review provides verdict expertise |
| E:judging:wisdom | judging | wisdom | Principled Verdict Wisdom | 0 | NO_ITEMS | Guidance Conflict Table provides principled verdict framework |
| E:reviewing:data | reviewing | data | Confirmed Examination Record | 1 | HAS_ITEMS | As-built update trigger undefined |
| E:reviewing:information | reviewing | information | Coherent Audit Communication | 0 | NO_ITEMS | Records section provides coherent audit trail |
| E:reviewing:knowledge | reviewing | knowledge | Authoritative Audit Expertise | 0 | NO_ITEMS | P.Eng. stamp and code review provide audit expertise |
| E:reviewing:wisdom | reviewing | wisdom | Principled Audit Foresight | 0 | NO_ITEMS | Records include as-built update provision |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:wisdom | RationaleGap | Guidance | Guidance | Expand Consideration E (cold climate coordination) beyond emergency shower heat tracing: address freeze protection for cistern, exposed piping, and floor drain trap primers in Alberta winter conditions | Guidance Consideration E mentions heat tracing for the emergency shower but does not address broader cold climate implications for the fixture schedule (trap primers, freeze-protected floor drains, cistern freeze protection). For a facility in Alberta, principled strategic foresight requires addressing winter conditions comprehensively. | Guidance.md | Consideration E: Coordination with Electrical for Emergency Shower | -- | Plumbing Engineer / Mechanical Engineer | TBD |
| E-002 | E:reviewing:data | Normalization | Procedure | Procedure | Define the trigger and responsible party for the as-built update record: specify when (post-installation), who (Plumbing Engineer or contractor), and what constitutes a change requiring as-built revision | Records table lists "As-built update -- Post-construction as-built update to schedule if fixture changes occur during installation" but does not define what triggers the update, who is responsible, or what threshold of change requires revision. Confirmed examination record requires clear update criteria. | Procedure.md | Records table -- As-built update row | -- | Plumbing Engineer / Project Manager | TBD |
