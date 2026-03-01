# Semantic Lensing Register: DEL-002-01 Preliminary Structural Design

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-002_Structural Design/1_Working/DEL-002-01_Preliminary-Design/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-002-01_Preliminary-Design/_CONTEXT.md (read successfully)
- _STATUS.md — DEL-002-01_Preliminary-Design/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md — DEL-002-01_Preliminary-Design/_SEMANTIC.md (read successfully; all 7 matrices parsed)
- Datasheet.md — DEL-002-01_Preliminary-Design/Datasheet.md (read successfully)
- Specification.md — DEL-002-01_Preliminary-Design/Specification.md (read successfully)
- Guidance.md — DEL-002-01_Preliminary-Design/Guidance.md (read successfully)
- Procedure.md — DEL-002-01_Preliminary-Design/Procedure.md (read successfully)
- _REFERENCES.md — DEL-002-01_Preliminary-Design/_REFERENCES.md (read successfully; lists R-01, R-04)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 5
  - Specification: 10
  - Guidance: 6
  - Procedure: 4
  - Multi: 3
- By matrix:
  - A: 5  B: 4  C: 4  F: 4  D: 3  X: 5  E: 3
- By type:
  - Conflict: 2
  - VerificationGap: 6
  - MissingSlot: 7
  - WeakStatement: 5
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
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Governing code editions not confirmed |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Code compliance statement is intent-only |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | AHJ confirmation missing |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit pathway adequately described via County approval cycle |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Concurrent architectural coordination timing unclear |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Procedure steps are well-structured for execution |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification checklist in Procedure covers performance assessment |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Internal QA review step present |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | No explicit value/benefit framing for Owner |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs in Guidance adequately address merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | County approval serves as worth determination gate |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Internal quality review step present in Procedure |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify specific NBC and ABC edition numbers applicable to this project (e.g., NBC 2020 or NBC 2025) rather than "current edition" | The Standards table (Specification S3) lists NBC and ABC as "current edition" with accessibility "Not directly accessible." Without a specific edition, the prescriptive direction for code compliance is ambiguous and could shift if editions change during the project. | Specification.md | S3 Standards table | -- | Structural Engineer + AHJ | TBD |
| A-002 | A:normative:applying | VerificationGap | Specification | Specification | Add verification approach for REQ-A03 (structural compatibility with Old North Shop) and REQ-A04 (mezzanine design load determination) | REQ-A03 and REQ-A04 appear in the Inferred Requirements table but have no corresponding entries in the Verification table (S4). If these are retained as requirements, they need verification approaches. | Specification.md | S2.2 Inferred Requirements; S4 Verification | -- | Structural Engineer | TBD |
| A-003 | A:normative:judging | TBD_Question | Multi | Specification | Record TBD: Confirm identity and contact for Authority Having Jurisdiction (AHJ) for structural permits in Camrose County | Compliance determination requires knowing who adjudicates. The AHJ is referenced generically ("Camrose County building department and Alberta Safety Codes Officers") but no specific contact or office is confirmed. | Specification.md; Procedure.md | Specification S3 note; Procedure Step 2.1 | -- | Project Manager | TBD |
| A-004 | A:operative:guiding | WeakStatement | Procedure | Procedure | Clarify timing dependency between DEL-002-01 and DEL-001-01 (Preliminary Architectural Design) -- sequential, concurrent, or gated? | Procedure Step 5 says "coordinate with Architect" and Prerequisites list DEL-001-01 as "TBD," but the procedural direction does not specify whether structural preliminary design must wait for, proceed concurrently with, or precede the architectural preliminary design. | Procedure.md | S2.1 Prerequisites; Step 5 | -- | Project Manager | TBD |
| A-005 | A:evaluative:guiding | MissingSlot | Guidance | Guidance | Add a brief value statement explaining why the preliminary design stage creates value for both the Owner and Design-Builder (risk reduction, cost certainty, schedule protection) | Guidance S1 Purpose explains the functional purpose but does not frame the value proposition in terms the Owner would use to evaluate the deliverable's worth. A value orientation lens suggests this would strengthen the Owner's understanding of why this gate matters. | Guidance.md | S1 Purpose | -- | Structural Engineer | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Service pit depth not stated |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet provides adequate sourced evidence for most parameters |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Old North Shop structural data incomplete |
| B:data:consistency | data | consistency | reliable measurement | 1 | HAS_ITEMS | Dimension source inconsistency |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (geotech dependency, variable-price) are present |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context provided is adequate across documents |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Documents provide comprehensive accounts within scope |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Mezzanine load-bearing extent inconsistency (CON-001) |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Structural engineering fundamentals are appropriately referenced |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Documents appropriately defer to Structural Engineer expertise |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Scope of knowledge coverage appropriate for preliminary stage |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Key judgment calls identified (system selection, foundation approach) |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-off analysis in Guidance provides adequate judgment framework |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view adequately covered at preliminary level |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add service pit/trench depth as a TBD parameter (standard range 1.2-1.5 m noted in Guidance but no value in Datasheet) | The service pit is a major structural element. Datasheet S2.1 lists plan dimensions (24 ft x 100 ft, ASSUMPTION) but depth is absent. Guidance S3.4 mentions standard depths (1.2-1.5 m) but this essential fact is missing from the Datasheet's parameter record. | Datasheet.md; Guidance.md | Datasheet S2.1; Guidance S3.4 | -- | Structural Engineer | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add structural attributes for Old North Shop renovation scope (existing structural system type, condition, connection interface parameters) | Datasheet S2.3 lists renovation items but not existing structural system type, material, or condition. If the preliminary design must address the connection/adjacency (REQ-A03), structural data about the existing building is an essential record gap. | Datasheet.md | S2.3 Existing Building | -- | Structural Engineer / Field Survey | TBD |
| B-003 | B:data:consistency | Conflict | Multi | Multi | Resolve service pit dimension provenance: Datasheet states "approx. 24 ft wide x 100 ft long (ASSUMPTION -- scale-read from conceptual drawing)" while Guidance states "approximately 24 ft wide x 100 ft long on the east side of the main shop (ASSUMPTION -- scale-read from conceptual drawing)." Both are assumptions but treated as parameters. | Both Datasheet and Guidance carry the same assumption-based dimension, but neither flags that this is unverified. As a reliable measurement, this should either be confirmed from the source or explicitly marked as TBD in both locations with consistent qualification. | Datasheet.md; Guidance.md | Datasheet S2.1 Service pit/trench row; Guidance S3.4 | Datasheet.md#S2.1; Guidance.md#S3.4 | County / Architect (App B Shop confirmation) | TBD |
| B-004 | B:information:consistency | Conflict | Multi | Specification | Surface CON-001 (mezzanine load-bearing extent) as a lensing item: App B legend says "Load Bearing Over Parts Room + Utility For Storage" while RFP/SOW references include wash bay | This conflict is already identified in Guidance Conflict Table as CON-001 but is not cross-referenced in the Specification requirements or Datasheet. The coherent message lens reveals the inconsistency is documented but not formally tracked in the normative document. | Guidance.md; Specification.md; Datasheet.md | Guidance Conflict Table CON-001; Specification REQ-007; Datasheet S2.1 Mezzanine row | Guidance.md#Conflict Table CON-001 source A vs source B | County (Owner) ruling | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Regulatory Imperative | 1 | HAS_ITEMS | Specific code clause references missing |
| C:normative:sufficiency | normative | sufficiency | Prescribed Competence | 1 | HAS_ITEMS | P.Eng. seal at preliminary stage unclear |
| C:normative:completeness | normative | completeness | Exhaustive Obligation | 0 | NO_ITEMS | Obligation coverage is thorough for preliminary stage |
| C:normative:consistency | normative | consistency | Enforced Coherence | 0 | NO_ITEMS | Normative statements are consistent across documents |
| C:operative:necessity | operative | necessity | Operational Prerequisite | 1 | HAS_ITEMS | Geotech report timing vs preliminary design unclear |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Readiness | 0 | NO_ITEMS | Readiness criteria adequately established |
| C:operative:completeness | operative | completeness | Total Execution Coverage | 0 | NO_ITEMS | Procedure steps cover execution end-to-end |
| C:operative:consistency | operative | consistency | Procedural Reliability | 0 | NO_ITEMS | Procedure is internally consistent |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Merit | 0 | NO_ITEMS | Merit is implicitly addressed via trade-off analysis |
| C:evaluative:sufficiency | evaluative | sufficiency | Validated Appraisal | 0 | NO_ITEMS | County approval cycle serves as validation |
| C:evaluative:completeness | evaluative | completeness | Holistic Valuation | 1 | HAS_ITEMS | No lifecycle cost or schedule impact framing |
| C:evaluative:consistency | evaluative | consistency | Principled Consistency | 0 | NO_ITEMS | Evaluative framework is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Strengthen code references from "likely applicable -- location TBD" to either confirmed references or explicit TBD items requiring AHJ confirmation | Under a Regulatory Imperative lens, the Standards table contains five entries marked "ASSUMPTION: likely applicable -- location TBD." These are presented as probable rather than confirmed, weakening the regulatory imperative. They should be either confirmed or formally recorded as open TBDs with a resolution pathway. | Specification.md | S3 Standards table | -- | Structural Engineer + AHJ | TBD |
| C-002 | C:normative:sufficiency | WeakStatement | Procedure | Procedure | Clarify whether P.Eng. seal/signature is required on the preliminary design presentation or only at IFC stage | Procedure Step 6.1 states "P.Eng. signature/seal for preliminary review -- ASSUMPTION: P.Eng. seal required on preliminary; confirmed at IFC stage as mandatory per SOW-0018." This creates ambiguity about prescribed competence at the preliminary stage. The Specification REQ-017 explicitly says "Not applicable at preliminary stage." The Procedure contradicts this with an assumption. | Procedure.md; Specification.md | Procedure Step 6.1; Specification S4 REQ-017 verification | Procedure.md#Step 6; Specification.md#S4 REQ-017 | Structural Engineer / Project Manager | TBD |
| C-003 | C:operative:necessity | RationaleGap | Guidance | Guidance | Add rationale for why the preliminary design can proceed without the geotechnical report, and what constraints this imposes on the foundation section of the presentation | Guidance S2.2 explains the geotech dependency but does not explicitly state why proceeding without it is acceptable for the preliminary stage, nor what limitations the Owner should understand about the foundation section. The Operational Prerequisite lens reveals a gap in explaining this sequencing rationale. | Guidance.md | S2.2 Geotechnical Dependency | -- | Structural Engineer | TBD |
| C-004 | C:evaluative:completeness | MissingSlot | Guidance | Guidance | Consider adding a section on schedule and cost implications of preliminary design decisions (e.g., how structural system selection affects construction timeline and budget) | The Holistic Valuation lens looks for comprehensive worth assessment. Guidance covers technical trade-offs (S4) but does not address how preliminary design choices affect project schedule, construction cost, or lifecycle value. This would strengthen the Owner's basis for approval. | Guidance.md | S4 Trade-offs | -- | Structural Engineer / Project Manager | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Obligatory Rigor | 1 | HAS_ITEMS | Seismic design parameters absent |
| F:normative:sufficiency | normative | sufficiency | Authorized Preparedness | 0 | NO_ITEMS | Requirements are sufficiently authorized by source references |
| F:normative:completeness | normative | completeness | Exhaustive Regulatory Scope | 1 | HAS_ITEMS | Environmental and fire code scope missing |
| F:normative:consistency | normative | consistency | Harmonized Conformity | 0 | NO_ITEMS | Normative requirements are internally consistent |
| F:operative:necessity | operative | necessity | Enabling Dependency | 1 | HAS_ITEMS | Survey dependency unresolved |
| F:operative:sufficiency | operative | sufficiency | Verified Capacity | 0 | NO_ITEMS | Capacity/resource requirements adequately stated |
| F:operative:completeness | operative | completeness | Comprehensive Proficiency | 0 | NO_ITEMS | Process steps are comprehensive |
| F:operative:consistency | operative | consistency | Repeatable Delivery | 0 | NO_ITEMS | Process is described for repeatability |
| F:evaluative:necessity | evaluative | necessity | Fundamental Justification | 0 | NO_ITEMS | Justification for deliverable existence is clear |
| F:evaluative:sufficiency | evaluative | sufficiency | Grounded Valuation | 0 | NO_ITEMS | Valuation approach (County approval) is grounded |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Worth | 1 | HAS_ITEMS | No acceptance criteria for presentation format |
| F:evaluative:consistency | evaluative | consistency | Steadfast Integrity | 0 | NO_ITEMS | Evaluative framework is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | MissingSlot | Datasheet | Datasheet | Add seismic design parameters (Seismic Hazard Index, Site Class, Importance Category) as TBD items in Conditions or Attributes table | Obligatory Rigor requires identification of all binding design inputs. The Datasheet S3 Conditions table references Alberta codes but does not list seismic design parameters. For a 35 ft concrete structure, seismic design is a fundamental input. Guidance S3.1 mentions "wind and seismic design" but no parameters appear in the Datasheet. | Datasheet.md; Guidance.md | Datasheet S3 Conditions; Guidance S3.1 | -- | Structural Engineer / NBC | TBD |
| F-002 | F:normative:completeness | TBD_Question | Specification | Specification | Record TBD: Determine whether fire code, environmental, or energy code requirements have structural implications for this building (fire separation walls, fire resistance ratings, insulation support) | Exhaustive Regulatory Scope requires checking all applicable regulatory domains. The Specification references building codes and safety codes but does not mention fire code structural requirements, environmental regulations, or energy code implications (thermal envelope support). For a 35 ft industrial building, fire separation between zones (wash bay, parts room, office) may require fire-rated structural assemblies. | Specification.md | S3 Standards | -- | Structural Engineer + AHJ | TBD |
| F-003 | F:operative:necessity | WeakStatement | Procedure | Procedure | Strengthen survey prerequisite from "helpful for preliminary structural understanding" to either required-before-start or explicitly-not-required with rationale | Procedure S2.1 lists "Preliminary survey of site (SOW-0002)" as "TBD -- required before construction; helpful for preliminary structural understanding of site constraints." The Enabling Dependency lens identifies this as a weak statement: is the survey an enabling dependency or not? The current phrasing leaves the decision ambiguous. | Procedure.md | S2.1 Prerequisites | -- | Project Manager | TBD |
| F-004 | F:evaluative:completeness | VerificationGap | Specification | Specification | Add acceptance criteria or verification approach for the presentation format and content sufficiency (beyond County approval -- what makes the presentation "sufficient" for internal QA?) | REQ-A01 states the presentation shall convey the structural system concept "clearly enough" for County approval. The verification (S4 REQ-A01) references "County review meeting or written comment cycle confirms acceptance." However, there is no internal acceptance criterion for what "clearly enough" means before submission. Comprehensive Worth requires that the deliverable's value can be assessed against criteria. | Specification.md | S4 REQ-A01 verification | -- | Structural Engineer | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Definitive Command | 0 | NO_ITEMS | Requirements provide definitive command |
| D:normative:applying | normative | applying | Enforced Qualification | 1 | HAS_ITEMS | Personnel qualification verification missing |
| D:normative:judging | normative | judging | Binding Verdict | 0 | NO_ITEMS | County approval serves as binding verdict mechanism |
| D:normative:reviewing | normative | reviewing | Confirmed Inspection | 0 | NO_ITEMS | Internal QA review step addresses inspection |
| D:operative:guiding | operative | guiding | Cleared Workflow | 0 | NO_ITEMS | Workflow is clear and sequential |
| D:operative:applying | operative | applying | Proven Delivery | 1 | HAS_ITEMS | No delivery format specification |
| D:operative:judging | operative | judging | Demonstrated Capability | 0 | NO_ITEMS | Verification checklist demonstrates capability assessment |
| D:operative:reviewing | operative | reviewing | Systematic Confirmation | 0 | NO_ITEMS | Systematic confirmation via checklist present |
| D:evaluative:guiding | evaluative | guiding | Justified Purpose | 0 | NO_ITEMS | Purpose is well-justified in Guidance S1 |
| D:evaluative:applying | evaluative | applying | Confirmed Value | 0 | NO_ITEMS | Value confirmation via County approval |
| D:evaluative:judging | evaluative | judging | Definitive Appraisal | 1 | HAS_ITEMS | No success criteria for the deliverable beyond County approval |
| D:evaluative:reviewing | evaluative | reviewing | Principled Scrutiny | 0 | NO_ITEMS | QA review step provides principled scrutiny |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | VerificationGap | Specification | Procedure | Add verification that the Structural Engineer assigned to DEL-002-01 holds a valid P.Eng. license in Alberta | Enforced Qualification requires that personnel qualifications are not just stated but verified. Procedure S2.2 states "Must be licensed to practice structural engineering in Alberta" but there is no verification step confirming this qualification before work begins. Specification REQ-017 addresses IFC stamping but not preliminary stage qualification. | Specification.md; Procedure.md | Specification REQ-017; Procedure S2.2 | -- | Project Manager | TBD |
| D-002 | D:operative:applying | MissingSlot | Specification | Specification | Add requirement or guidance on delivery format (digital PDF, printed package, presentation slides, or combination) for the preliminary design submission to County | Proven Delivery requires clarity on how the deliverable is physically delivered. Specification S5.2 lists typical contents but does not specify the format (PDF, printed drawings, slideshow, digital model). Procedure Step 8 says "Submit" but does not specify the medium. | Specification.md; Procedure.md | Specification S5.2; Procedure Step 8 | -- | Project Manager / County | TBD |
| D-003 | D:evaluative:judging | RationaleGap | Guidance | Guidance | Add criteria or indicators that would constitute a successful preliminary design beyond "County approves" (e.g., no major redesign required at final design stage, inter-discipline coordination issues resolved, all TBDs reduced) | Definitive Appraisal requires clear criteria for judging worth. The only success criterion is County approval (REQ-001 verification). There is no framework for appraising whether the preliminary design effectively seeds downstream work (Guidance S2.4 discusses seeding but not success metrics). | Guidance.md; Specification.md | Guidance S2.4; Specification S4 REQ-001 | -- | Structural Engineer / Project Manager | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Principled Foundation | 0 | NO_ITEMS | Foundation principles are established |
| X:guiding:sufficiency | guiding | sufficiency | Directed Competence | 0 | NO_ITEMS | Competence direction is adequate |
| X:guiding:completeness | guiding | completeness | Exhaustive Direction | 1 | HAS_ITEMS | Lateral load design guidance incomplete |
| X:guiding:consistency | guiding | consistency | Coherent Authority | 0 | NO_ITEMS | Authority references are coherent |
| X:applying:necessity | applying | necessity | Essential Qualification | 0 | NO_ITEMS | Qualifications are identified |
| X:applying:sufficiency | applying | sufficiency | Confirmed Effectiveness | 1 | HAS_ITEMS | No effectiveness confirmation for coordination process |
| X:applying:completeness | applying | completeness | Thorough Capability | 0 | NO_ITEMS | Capability coverage is thorough |
| X:applying:consistency | applying | consistency | Reliable Practice | 0 | NO_ITEMS | Practices described are reliable |
| X:judging:necessity | judging | necessity | Decisive Criterion | 1 | HAS_ITEMS | Crane clearance criterion not quantified |
| X:judging:sufficiency | judging | sufficiency | Informed Adjudication | 0 | NO_ITEMS | Adjudication pathways are informed |
| X:judging:completeness | judging | completeness | Comprehensive Adjudication | 1 | HAS_ITEMS | Verification table incomplete for inferred requirements |
| X:judging:consistency | judging | consistency | Standardized Judgment | 0 | NO_ITEMS | Judgment criteria are standardized |
| X:reviewing:necessity | reviewing | necessity | Substantiated Review | 0 | NO_ITEMS | Review requirements are substantiated |
| X:reviewing:sufficiency | reviewing | sufficiency | Organized Verification | 1 | HAS_ITEMS | Verification approaches lack measurable criteria |
| X:reviewing:completeness | reviewing | completeness | Thorough Audit | 0 | NO_ITEMS | Audit checklist is thorough |
| X:reviewing:consistency | reviewing | consistency | Coherent Inspection | 0 | NO_ITEMS | Inspection framework is coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | MissingSlot | Guidance | Guidance | Add a consideration section for lateral load resistance system selection (wind and seismic), including trade-offs analogous to those provided for wall systems (Guidance S4.1) | Exhaustive Direction: Guidance S3.1 mentions "Lateral load resistance (wind and seismic design for a tall structure)" as a consideration but does not develop it into a trade-off analysis or consideration section comparable to wall systems (S4.1), foundation (S4.2), or crane runway (S4.3). For a 35 ft structure, lateral system selection is a primary design decision. | Guidance.md | S3.1; S4 Trade-offs | -- | Structural Engineer | TBD |
| X-002 | X:applying:sufficiency | VerificationGap | Procedure | Procedure | Add a verification check for inter-discipline coordination sufficiency (e.g., coordination sign-off from each discipline, or a coordination issues register with no unresolved items at time of submission) | Confirmed Effectiveness: Procedure Step 5 describes coordination activities but Step 5 verification is only "Coordination log or meeting notes confirm cross-discipline review has occurred." Occurrence is not effectiveness -- there is no check that coordination actually resolved issues or achieved alignment. | Procedure.md | Step 5; Step 5 Verification | -- | Project Manager | TBD |
| X-003 | X:judging:necessity | VerificationGap | Specification | Specification | Add a verification item for crane hook clearance under the roof structure as a decisive criterion in the preliminary design | Decisive Criterion: Guidance S3.2 identifies "Clearance between crane hook height and ceiling/roof structure" as a key consideration. However, neither Specification nor Procedure includes a verification check for this clearance. For two 5-tonne cranes, insufficient hook height clearance would be a fundamental design failure. | Specification.md; Guidance.md | Guidance S3.2; Specification S4 REQ-004 | -- | Structural Engineer | TBD |
| X-004 | X:judging:completeness | VerificationGap | Specification | Specification | Add verification approaches for REQ-A03 and REQ-A04 to the Verification table, or explicitly state they are not verified at the preliminary stage | Comprehensive Adjudication: Specification S4 Verification table provides verification for REQ-001 through REQ-017 and REQ-A01, REQ-A02, but omits REQ-A03 (Old North Shop compatibility) and REQ-A04 (mezzanine design load). This leaves two inferred requirements without any adjudication pathway. (Overlaps with A-002; recorded here under the X-matrix verification lens for completeness.) | Specification.md | S2.2 Inferred Requirements; S4 Verification | -- | Structural Engineer | TBD |
| X-005 | X:reviewing:sufficiency | Normalization | Specification | Specification | Standardize verification language: some verification approaches use "shall confirm" (measurable) while others use "shall show" or "shall indicate" (less measurable). Normalize to a consistent verb hierarchy. | Organized Verification: The Verification table (S4) uses inconsistent verb strength: "shall confirm" (REQ-002, REQ-003, REQ-008, REQ-009, REQ-012, REQ-013), "shall show" (REQ-004, REQ-006, REQ-011), "shall indicate" (REQ-005). The verification sufficiency would benefit from a consistent verb hierarchy that distinguishes levels of evidence required. | Specification.md | S4 Verification | -- | Structural Engineer | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Evidence | 1 | HAS_ITEMS | Source traceability gap in Datasheet |
| E:guiding:information | guiding | information | Coherent Instruction | 0 | NO_ITEMS | Instructions are coherent across documents |
| E:guiding:knowledge | guiding | knowledge | Integrated Command | 0 | NO_ITEMS | Knowledge integration is adequate |
| E:guiding:wisdom | guiding | wisdom | Principled Foresight | 0 | NO_ITEMS | Foresight considerations (downstream seeding, geotech dependency) are present |
| E:applying:data | applying | data | Demonstrated Result | 0 | NO_ITEMS | Result demonstration pathway exists via County approval |
| E:applying:information | applying | information | Actionable Guidance | 0 | NO_ITEMS | Guidance is actionable |
| E:applying:knowledge | applying | knowledge | Proven Expertise | 0 | NO_ITEMS | Expertise requirements are established |
| E:applying:wisdom | applying | wisdom | Seasoned Pragmatism | 0 | NO_ITEMS | Pragmatic approach evident in trade-offs and assumptions |
| E:judging:data | judging | data | Grounded Determination | 1 | HAS_ITEMS | Concrete structure scope ambiguity (CON-002) |
| E:judging:information | judging | information | Situated Verdict | 0 | NO_ITEMS | Verdict mechanisms are situated in context |
| E:judging:knowledge | judging | knowledge | Informed Determination | 0 | NO_ITEMS | Determination pathways are informed |
| E:judging:wisdom | judging | wisdom | Equitable Benchmark | 0 | NO_ITEMS | Benchmarking approach is equitable |
| E:reviewing:data | reviewing | data | Authenticated Record | 1 | HAS_ITEMS | Record authentication provisions missing |
| E:reviewing:information | reviewing | information | Coherent Report | 0 | NO_ITEMS | Report structure is coherent |
| E:reviewing:knowledge | reviewing | knowledge | Substantiated Expertise | 0 | NO_ITEMS | Expertise substantiation is addressed |
| E:reviewing:wisdom | reviewing | wisdom | Methodical Oversight | 0 | NO_ITEMS | Oversight methodology is present (QA review, County approval) |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | Normalization | Datasheet | Datasheet | Standardize source citation format in Datasheet Attributes tables: some entries cite "RFP section, App B" while others cite "SOW-XXXX" or "Decomposition section." Add a legend or normalize to a consistent format. | Authoritative Evidence requires that data provenance is clear and traceable. The Datasheet uses multiple citation styles: some cells reference RFP sections and appendices (e.g., "RFP S3.1, App B (Shop)"), others reference SOW numbers (e.g., "SOW-0034, App B (Shop)"), and some reference decomposition sections (e.g., "Decomposition SOW-0019"). While individually traceable, the inconsistency could cause citation errors in downstream documents. | Datasheet.md | S2.1, S2.2, S2.3 Attributes tables | -- | Structural Engineer | TBD |
| E-002 | E:judging:data | RationaleGap | Guidance | Guidance | Add rationale for CON-002 interpretation: explain why "concrete structure" ambiguity matters for preliminary design decisions and what the default interpretation should be | Grounded Determination: CON-002 (Guidance Conflict Table) identifies that "concrete structure" may refer to walls/columns only, floor slab, or roof system as well. The conflict is identified but the rationale for why this distinction matters at the preliminary stage is not developed. The Guidance proposes an interpretation but does not explain the downstream consequences of each reading. | Guidance.md | Conflict Table CON-002 | -- | Structural Engineer | TBD |
| E-003 | E:reviewing:data | Normalization | Datasheet | Datasheet | Add version or revision tracking fields to the Datasheet identification table (revision number, date of last update, author) | Authenticated Record requires that records can be verified as current and authoritative. The Datasheet has no revision tracking fields. For a living document that will be updated as the preliminary design progresses, the absence of version control metadata could lead to confusion about which version was approved. | Datasheet.md | S1 Identification | -- | Project Manager | TBD |
