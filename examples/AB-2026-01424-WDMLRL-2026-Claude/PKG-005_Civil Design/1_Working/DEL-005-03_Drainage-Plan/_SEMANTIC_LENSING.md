# Semantic Lensing Register: DEL-005-03 Drainage Plan

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-005_Civil Design/1_Working/DEL-005-03_Drainage-Plan/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-005-03_Drainage-Plan/_CONTEXT.md (Identification, Description, Scope of Work References, Anticipated Artifacts)
- _STATUS.md -- DEL-005-03_Drainage-Plan/_STATUS.md (Current Status: SEMANTIC_READY, dated 2026-02-26)
- _SEMANTIC.md -- DEL-005-03_Drainage-Plan/_SEMANTIC.md (Matrices A, B, C, F, D, X, E all present and parseable)
- Datasheet.md -- DEL-005-03_Drainage-Plan/Datasheet.md (Identification, Attributes, Conditions, Construction, References)
- Specification.md -- DEL-005-03_Drainage-Plan/Specification.md (Scope, Requirements REQ-001 through REQ-008, Standards, Verification, Documentation)
- Guidance.md -- DEL-005-03_Drainage-Plan/Guidance.md (Purpose, Principles, Considerations, Trade-offs, Conflict Table)
- Procedure.md -- DEL-005-03_Drainage-Plan/Procedure.md (Prerequisites, Phases A-E, Verification, Records)
- _REFERENCES.md -- DEL-005-03_Drainage-Plan/_REFERENCES.md (R-01, R-07 listed; no scope expansion)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 24
- By document:
  - Datasheet: 3
  - Specification: 9
  - Guidance: 5
  - Procedure: 5
  - Multi: 2
- By matrix:
  - A: 5  B: 4  C: 3  F: 3  D: 2  X: 4  E: 3
- By type:
  - Conflict: 0
  - VerificationGap: 5
  - MissingSlot: 7
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 2
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 0 (3 existing conflicts in Guidance Conflict Table are documented there; no new cross-document conflicts found)
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Design storm return period unspecified |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Standards table entries are assumptions |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Code compliance verification lacks specific code citations |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | No audit trail structure for regulatory submissions |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Phase A-E is well-structured |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Steps are clear and actionable |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification table in Procedure covers key checks |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records section provides adequate audit trail |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | No explicit priority ranking among competing design objectives |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs table in Guidance covers decision space |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Verification criteria exist for all requirements |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Internal review process described in Phase D |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Record TBD: What design storm return period and rainfall intensity apply to this site under Alberta standards and Camrose County requirements? | REQ-002 states parameters are "TBD pending civil engineer's determination" but no guidance on acceptable range or governing standard is provided. This is the single most consequential open normative parameter. | Specification.md | Requirements > REQ-002 | -- | Civil Engineer of record; Camrose County; Alberta Environment | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Strengthen Standards table entries from ASSUMPTION to confirmed applicability with specific edition/clause references once standards are researched | All five Standards table entries are tagged ASSUMPTION with "location TBD." Without confirmed standard citations, mandatory practice cannot be verified against the correct criteria. | Specification.md | Standards | -- | Civil Engineer of record | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add specific code clause references to REQ-006 verification method so compliance determination can be traced to named provisions | REQ-006 verification method says "Civil Engineer code review; permit authority review" but does not name which code clauses are checked. Compliance determination requires traceable criteria. | Specification.md | Verification > REQ-006 row | -- | Civil Engineer of record | TBD |
| A-004 | A:normative:reviewing | MissingSlot | Procedure | Procedure | Add a step or checklist item for assembling the regulatory submission package (permit application documentation) referencing Specification REQ-006 and Datasheet Conditions | Procedure Phase E covers IFC release and distribution but does not include a step for preparing the regulatory/permit submission package. Regulatory audit readiness requires this. | Procedure.md | Phase E -- IFC Release and Handoff | -- | Project Manager / Civil Engineer | TBD |
| A-005 | A:evaluative:guiding | RationaleGap | Guidance | Guidance | Add explicit priority ranking when positive drainage (REQ-001), neighbour non-alteration (REQ-003), and cost/constructability conflict | Guidance Principles section describes both positive drainage and neighbour non-alteration as hard requirements but does not state which takes priority if they conflict (e.g., if achieving positive drainage requires directing more flow toward a boundary). | Guidance.md | Principles | -- | Civil Engineer of record; Owner | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Existing topography data source not confirmed |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | R-07 site maps not extracted to text |
| B:data:completeness | data | completeness | comprehensive record | 0 | NO_ITEMS | Datasheet Attributes table is thorough |
| B:data:consistency | data | consistency | reliable measurement | 1 | HAS_ITEMS | Elevation datum not stated |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key interface signals documented |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequate for current stage |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Scope inclusions and exclusions well enumerated |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Cross-document messaging is consistent |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Drainage design fundamentals evident in Guidance |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Civil engineer competence assumed per P.Eng. requirement |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Adequate for current design stage |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Consistent understanding across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 1 | HAS_ITEMS | Landfill environmental context under-specified |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-offs table provides adequate judgment scaffold |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Cross-deliverable dependencies acknowledged |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning in Guidance is principled and traceable |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Confirm source and date of existing site topography data (DEL-008-02 survey); confirm whether pre-development drainage baseline has been established | Procedure Step A2 requires documenting pre-development drainage patterns, and Datasheet references the site survey (DEL-008-02), but no confirmation that this essential input data exists or its status. | Datasheet.md; Procedure.md | Datasheet > Attributes; Procedure > Phase A > Step A2 | -- | Civil Engineer / Survey team | TBD |
| B-002 | B:data:sufficiency | WeakStatement | Datasheet | Datasheet | Clarify accessibility status of R-07 (Appendix C site maps): "contents not extracted to text -- location TBD for specific site geometry" should be resolved before design proceeds | Datasheet References table notes R-07 is "present in _Sources/ but contents not extracted to text." Adequate evidence for drainage design requires usable site geometry data from this reference. | Datasheet.md | References > R-07 row | -- | Civil Engineer | TBD |
| B-003 | B:data:consistency | MissingSlot | Multi | Datasheet | Add elevation datum reference (geodetic or local) to Datasheet so all elevation values across drainage plan, grading plan, and calculation package use the same vertical reference | No document states the elevation datum. Procedure Step C2 references "spot elevations at critical drainage points" and Step C5 requires consistent "elevation datums" across deliverables, but the datum itself is not defined anywhere. | Datasheet.md; Procedure.md | Datasheet > entire document scanned; Procedure > Phase C > Step C5 | -- | Civil Engineer / Survey team | TBD |
| B-004 | B:wisdom:necessity | TBD_Question | Guidance | Guidance | Record TBD: Are there specific Alberta Environment and Protected Areas requirements for stormwater management at or near landfill sites that would impose additional constraints beyond standard municipal drainage? | Guidance mentions landfill proximity and environmental considerations in Principles and Considerations sections but flags them as ASSUMPTION. This is an essential discernment question that could materially change the design approach. | Guidance.md | Principles > The Site is a Landfill-Adjacent Facility; Considerations > Storm Return Period Selection | -- | Civil Engineer; Alberta Environment and Protected Areas | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Compliance Threshold | 1 | HAS_ITEMS | Enforceable threshold for storm capacity undefined |
| C:normative:sufficiency | normative | sufficiency | Certified Regulatory Warrant | 0 | NO_ITEMS | P.Eng. certification adequately addresses regulatory warrant |
| C:normative:completeness | normative | completeness | Absolute Compliance Coverage | 1 | HAS_ITEMS | Alberta Environment stormwater guidance not confirmed |
| C:normative:consistency | normative | consistency | Standardized Regulatory Norm | 0 | NO_ITEMS | Document set uses consistent normative language |
| C:operative:necessity | operative | necessity | Critical Procedural Execution | 0 | NO_ITEMS | Procedure steps are well-sequenced |
| C:operative:sufficiency | operative | sufficiency | Verified Competent Delivery | 0 | NO_ITEMS | Verification table addresses competent delivery |
| C:operative:completeness | operative | completeness | Comprehensive Process Fulfillment | 0 | NO_ITEMS | Five-phase procedure is comprehensive |
| C:operative:consistency | operative | consistency | Reproducible Process Discipline | 0 | NO_ITEMS | Procedure is reproducible as written |
| C:evaluative:necessity | evaluative | necessity | Inherent Value Principle | 0 | NO_ITEMS | Value principles clearly stated in Guidance |
| C:evaluative:sufficiency | evaluative | sufficiency | Defensible Merit Appraisal | 0 | NO_ITEMS | Trade-offs table supports defensible appraisal |
| C:evaluative:completeness | evaluative | completeness | Unified Value Portrait | 1 | HAS_ITEMS | Lifecycle/maintenance value not addressed |
| C:evaluative:consistency | evaluative | consistency | Principled Value Alignment | 0 | NO_ITEMS | Value reasoning is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | VerificationGap | Specification | Specification | Add enforceable threshold values to REQ-002 once design storm is selected (return period, rainfall intensity, and acceptable peak discharge rate at site boundary) | "Enforceable Compliance Threshold" lens reveals that REQ-002 has no quantified threshold. Verification method points to DEL-005-06 but without target values, verification cannot determine pass/fail. | Specification.md | Requirements > REQ-002; Verification > REQ-002 row | -- | Civil Engineer of record | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add a requirement or standards entry for Alberta Environment and Protected Areas stormwater management guidance once applicability is confirmed | "Absolute Compliance Coverage" lens reveals that the Standards table lists Alberta Environment guidance as ASSUMPTION. If it applies, compliance coverage is incomplete without it as a governing standard. | Specification.md | Standards > Alberta Environment row | -- | Civil Engineer; Alberta Environment | TBD |
| C-003 | C:evaluative:completeness | MissingSlot | Guidance | Guidance | Add a consideration for long-term maintenance requirements of drainage infrastructure (cleaning frequency, access for maintenance equipment, lifecycle cost implications) | "Unified Value Portrait" lens reveals that the Guidance Considerations section addresses design-stage decisions but does not discuss post-construction maintenance or lifecycle value of drainage elements. The wash bay mud sump explicitly requires excavator access for cleaning, but no broader maintenance consideration is stated. | Guidance.md | Considerations > entire section scanned | -- | Civil Engineer; Owner | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandatory Compliance Constraint | 0 | NO_ITEMS | Mandatory constraints are enumerated in Specification |
| F:normative:sufficiency | normative | sufficiency | Validated Conformance Benchmark | 1 | HAS_ITEMS | No benchmark values for runoff comparison |
| F:normative:completeness | normative | completeness | Comprehensive Regulatory Mandate | 0 | NO_ITEMS | Regulatory mandates covered; gaps already captured |
| F:normative:consistency | normative | consistency | Harmonized Compliance Stability | 0 | NO_ITEMS | Requirements are internally consistent |
| F:operative:necessity | operative | necessity | Foundational Work Activation | 1 | HAS_ITEMS | Geotech prerequisite status ambiguous |
| F:operative:sufficiency | operative | sufficiency | Proficient Method Reliability | 0 | NO_ITEMS | Methods described are standard civil practice |
| F:operative:completeness | operative | completeness | Total Operational Scope Control | 0 | NO_ITEMS | Scope control is well-defined via exclusion table |
| F:operative:consistency | operative | consistency | Coherent Performance Rigor | 0 | NO_ITEMS | Consistent across Specification and Procedure |
| F:evaluative:necessity | evaluative | necessity | Integral Worth Imperative | 0 | NO_ITEMS | Worth imperatives are clear |
| F:evaluative:sufficiency | evaluative | sufficiency | Warranted Excellence Standard | 0 | NO_ITEMS | Design excellence expectations proportionate to facility |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Quality Mastery | 1 | HAS_ITEMS | Drawing format standard not identified |
| F:evaluative:consistency | evaluative | consistency | Principled Merit Integrity | 0 | NO_ITEMS | Merit reasoning is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add pre-development vs. post-development runoff comparison benchmark values (or method for determining them) to REQ-003 verification | "Validated Conformance Benchmark" lens reveals REQ-003 verification says "pre- and post-development drainage patterns at site boundary" but provides no benchmark values or acceptable change threshold. Without a quantified conformance benchmark, the verification is subjective. | Specification.md | Requirements > REQ-003; Verification > REQ-003 row | -- | Civil Engineer of record | TBD |
| F-002 | F:operative:necessity | WeakStatement | Procedure | Procedure | Clarify geotech prerequisite: specify minimum data needed from DEL-008-01 before drainage design can proceed vs. what is needed before IFC release | Procedure Prerequisites table says geotech is needed but hedges: "partial design may be possible before final geotech, but IFC should not be released until geotech is reviewed." "Foundational Work Activation" requires clarity on what minimum input triggers design start vs. IFC gate. | Procedure.md | Prerequisites > Geotechnical investigation row | -- | Civil Engineer / Project Manager | TBD |
| F-003 | F:evaluative:completeness | WeakStatement | Specification | Specification | Clarify drawing format and CAD standard requirements: "TBD pending Civil Engineer's determination and any Owner-specified CAD or drawing standards" | "Exhaustive Quality Mastery" lens reveals the Documentation note says drawing format is TBD. For a deliverable whose primary output is a drawing set, the applicable drawing standard affects quality evaluation. | Specification.md | Documentation > Note at bottom | -- | Civil Engineer; Owner | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Resolved Binding Guidance | 0 | NO_ITEMS | Guidance Conflict Table addresses open binding guidance items |
| D:normative:applying | normative | applying | Verified Compulsory Enactment | 0 | NO_ITEMS | Requirements are linked to enactment via Procedure |
| D:normative:judging | normative | judging | Definitive Conformance Verdict | 1 | HAS_ITEMS | Missing explicit acceptance criteria format |
| D:normative:reviewing | normative | reviewing | Sustained Compliance Inspection | 0 | NO_ITEMS | Inspection coordination covered in Datasheet Conditions |
| D:operative:guiding | operative | guiding | Decisive Workflow Mobilization | 0 | NO_ITEMS | Procedure phases provide decisive workflow |
| D:operative:applying | operative | applying | Established Direct Technique | 0 | NO_ITEMS | CAD production technique referenced in Procedure |
| D:operative:judging | operative | judging | Bounded Effectiveness Verdict | 0 | NO_ITEMS | Verification table bounds effectiveness checks |
| D:operative:reviewing | operative | reviewing | Settled Workflow Rigor Check | 0 | NO_ITEMS | Phase D internal review provides rigor check |
| D:evaluative:guiding | evaluative | guiding | Settled Priority Direction | 0 | NO_ITEMS | Already captured as A-005 (priority ranking gap) |
| D:evaluative:applying | evaluative | applying | Proven Quality Enactment | 0 | NO_ITEMS | Quality enactment path through P.Eng. stamp is clear |
| D:evaluative:judging | evaluative | judging | Final Value Judgment | 1 | HAS_ITEMS | No Owner acceptance/sign-off step |
| D:evaluative:reviewing | evaluative | reviewing | Enduring Quality Assurance | 0 | NO_ITEMS | Warranty period and records provide QA basis |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:judging | VerificationGap | Specification | Specification | Add explicit pass/fail acceptance criteria format to Verification table (e.g., "drainage plan demonstrates X at Y threshold" rather than "engineering review") | "Definitive Conformance Verdict" lens reveals most verification methods in the Verification table use "Engineering review" or "Civil Engineer review" without stating what constitutes pass vs. fail. A definitive verdict requires stated acceptance criteria. | Specification.md | Verification table | -- | Civil Engineer of record | TBD |
| D-002 | D:evaluative:judging | MissingSlot | Procedure | Procedure | Add a step for Owner/County review and acceptance of the drainage plan deliverable (distinct from preliminary design approval of DEL-005-01) | "Final Value Judgment" lens reveals Procedure covers internal review (Phase D) and IFC release (Phase E) but has no step for Owner review and formal acceptance of the final drainage plan drawings. County preliminary approval of DEL-005-01 is a prerequisite, but acceptance of the final DEL-005-03 IFC set is not proceduralized. | Procedure.md | Phase E -- IFC Release and Handoff | -- | Project Manager; Owner | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Anchored Directive Foundation | 0 | NO_ITEMS | Directives are anchored to RFP and SOW |
| X:guiding:sufficiency | guiding | sufficiency | Warranted Contextual Steerage | 0 | NO_ITEMS | Context adequate for stage |
| X:guiding:completeness | guiding | completeness | Universal Governance Mastery | 0 | NO_ITEMS | Governance coverage appropriate |
| X:guiding:consistency | guiding | consistency | Harmonized Leadership Clarity | 1 | HAS_ITEMS | Terminology inconsistency detected |
| X:applying:necessity | applying | necessity | Authenticated Practice Basis | 1 | HAS_ITEMS | Aggregate specification gap |
| X:applying:sufficiency | applying | sufficiency | Proven Implementation Capability | 0 | NO_ITEMS | Implementation capability assumed via P.Eng. |
| X:applying:completeness | applying | completeness | Comprehensive Execution Mastery | 0 | NO_ITEMS | Execution steps comprehensive |
| X:applying:consistency | applying | consistency | Coherent Practice Stability | 0 | NO_ITEMS | Practice descriptions consistent |
| X:judging:necessity | judging | necessity | Definitive Determination Basis | 1 | HAS_ITEMS | REQ-008 verification lacks specificity |
| X:judging:sufficiency | judging | sufficiency | Authoritative Justified Finding | 0 | NO_ITEMS | Justification basis adequate |
| X:judging:completeness | judging | completeness | Exhaustive Determination Record | 0 | NO_ITEMS | Records section covers needed outputs |
| X:judging:consistency | judging | consistency | Stable Harmonized Assessment | 0 | NO_ITEMS | Assessment criteria consistent |
| X:reviewing:necessity | reviewing | necessity | Enduring Scrutiny Foundation | 0 | NO_ITEMS | Scrutiny foundation through P.Eng. review |
| X:reviewing:sufficiency | reviewing | sufficiency | Competent Justified Inspection | 0 | NO_ITEMS | Inspection responsibilities assigned |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Verification Scope | 1 | HAS_ITEMS | Interdisciplinary coordination check incomplete |
| X:reviewing:consistency | reviewing | consistency | Stable Verification Discipline | 0 | NO_ITEMS | Verification discipline consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:consistency | Normalization | Multi | Guidance | Normalize terminology: "wash bay mud sump" vs. "exterior mud sump" vs. "wash bay drainage" -- establish one canonical term in Guidance and use consistently across all documents | Across documents, the wash bay drainage element is referred to as "wash bay mud sump" (Datasheet), "exterior mud sump" (Specification REQ-007), "wash bay drainage system" (Specification REQ-007), and "mud sump" (Procedure). Harmonized leadership clarity requires a single canonical term. | Datasheet.md; Specification.md; Guidance.md; Procedure.md | Datasheet > Attributes > Wash Bay Mud Sump row; Specification > REQ-007; Guidance > Considerations > Separation of Process Water; Procedure > Phase B > Step B4 | -- | Civil Engineer | TBD |
| X-002 | X:applying:necessity | RationaleGap | Guidance | Guidance | Add rationale note on how County-supplied aggregate specification uncertainty affects drainage design assumptions (gravel permeability, erosion resistance) | Datasheet notes aggregate supply is County responsibility and Guidance notes aggregate specs should not be assumed. However, no rationale is provided for how to handle this uncertainty in design (e.g., design to worst-case permeability, or hold point pending aggregate spec). Authenticated practice basis requires a known input or documented assumption. | Datasheet.md; Guidance.md | Datasheet > Attributes > Aggregate Supply; Guidance > Considerations > County-Provided Aggregate | -- | Civil Engineer; County | TBD |
| X-003 | X:judging:necessity | VerificationGap | Specification | Specification | Strengthen REQ-008 verification: specify what "engineering review" of driving surface runoff capture entails (e.g., flow path tracing, catch area delineation) | REQ-008 is labeled ASSUMPTION and its verification is simply "Engineering review." Under "Definitive Determination Basis," a requirement tagged as assumed and with a generic verification method cannot produce a definitive finding. Either confirm the requirement or specify the verification test. | Specification.md | Requirements > REQ-008; Verification > REQ-008 row | -- | Civil Engineer of record | TBD |
| X-004 | X:reviewing:completeness | MissingSlot | Procedure | Procedure | Add utility crossing/conflict check to Phase D Step D2 coordination checklist (utility tie-ins SOW-0080/0081/0082 are mentioned but no explicit check for drainage structure vs. utility crossing clearances) | Procedure Step D2 mentions utility tie-in locations but the check is phrased passively ("utility routing may cross drainage structures"). Exhaustive verification scope requires an explicit check for vertical and horizontal clearance between drainage structures and utility crossings. | Procedure.md | Phase D > Step D2 | -- | Civil Engineer | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Validated Steering Evidence | 1 | HAS_ITEMS | Soil permeability data dependency |
| E:guiding:information | guiding | information | Coherent Steering Intelligence | 0 | NO_ITEMS | Steering information coherent across documents |
| E:guiding:knowledge | guiding | knowledge | Masterful Governance Command | 0 | NO_ITEMS | Governance relationships well-mapped |
| E:guiding:wisdom | guiding | wisdom | Principled Strategic Foresight | 0 | NO_ITEMS | Strategic foresight evident in Guidance trade-offs |
| E:applying:data | applying | data | Proven Execution Evidence | 0 | NO_ITEMS | Execution evidence path through records is clear |
| E:applying:information | applying | information | Contextual Practice Intelligence | 0 | NO_ITEMS | Practice context adequate |
| E:applying:knowledge | applying | knowledge | Masterful Craft Proficiency | 0 | NO_ITEMS | Craft proficiency assumed via P.Eng. |
| E:applying:wisdom | applying | wisdom | Prudent Craft Foresight | 1 | HAS_ITEMS | Climate change consideration absent |
| E:judging:data | judging | data | Validated Evidentiary Record | 0 | NO_ITEMS | Evidentiary record structure adequate |
| E:judging:information | judging | information | Transparent Judgment Account | 0 | NO_ITEMS | Judgment transparency addressed via Conflict Table |
| E:judging:knowledge | judging | knowledge | Masterful Adjudication Fluency | 0 | NO_ITEMS | Adjudication path through Civil Engineer clear |
| E:judging:wisdom | judging | wisdom | Principled Verdict Wisdom | 0 | NO_ITEMS | Principles sufficiently guide verdict |
| E:reviewing:data | reviewing | data | Verified Scrutiny Evidence | 0 | NO_ITEMS | Scrutiny evidence path through records adequate |
| E:reviewing:information | reviewing | information | Comprehensive Audit Intelligence | 1 | HAS_ITEMS | Permit authority review feedback loop missing |
| E:reviewing:knowledge | reviewing | knowledge | Masterful Verification Fluency | 0 | NO_ITEMS | Verification steps are fluent and traceable |
| E:reviewing:wisdom | reviewing | wisdom | Principled Audit Foresight | 0 | NO_ITEMS | Audit foresight adequate given current stage |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | Normalization | Datasheet | Datasheet | Add geotechnical data dependency as an explicit Conditions row (with status field) referencing DEL-008-01, aligned with Guidance and Procedure references to geotech | Guidance Principles and Procedure Prerequisites both reference the geotechnical investigation as a key input, but Datasheet Conditions lists it with different framing ("drainage design may be influenced by subsurface conditions" with ASSUMPTION tag). Normalizing the reference across all three documents would ensure consistent tracking of this validated steering evidence dependency. | Datasheet.md; Guidance.md; Procedure.md | Datasheet > Conditions > Geotech Dependency; Guidance > Principles > Geotechnical Data; Procedure > Prerequisites > Geotechnical investigation row | -- | Civil Engineer | TBD |
| E-002 | E:applying:wisdom | RationaleGap | Guidance | Guidance | Add a consideration for climate change factors in design storm selection (e.g., whether to apply an uplift factor to historical rainfall data per current Alberta guidance) | REQ-002 references "future storm events" and Guidance discusses design storm selection, but neither document addresses whether climate change projections should influence the design storm parameter. Prudent craft foresight for a drainage system with a multi-decade service life warrants at least acknowledging this factor. | Specification.md; Guidance.md | Specification > REQ-002; Guidance > Considerations > Storm Return Period Selection | -- | Civil Engineer; Alberta Environment | TBD |
| E-003 | E:reviewing:information | MissingSlot | Procedure | Procedure | Add a feedback loop step for incorporating permit authority review comments into the drainage plan (if permit authority requests revisions after submission) | Procedure Phase E distributes drawings to permit authority but does not include a step for receiving, reviewing, and incorporating permit authority feedback. Comprehensive audit intelligence requires a closed-loop process for regulatory review comments. | Procedure.md | Phase E -- IFC Release and Handoff | -- | Project Manager; Civil Engineer | TBD |
