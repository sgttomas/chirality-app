# Semantic Lensing Register: DEL-002-10 Structural Calculation Package

**Generated:** 2026-02-26
**Deliverable Folder:** PKG-002_Structural Design/1_Working/DEL-002-10_Calculation-Package/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-002-10_Calculation-Package/_CONTEXT.md
- _STATUS.md — DEL-002-10_Calculation-Package/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md — DEL-002-10_Calculation-Package/_SEMANTIC.md
- Datasheet.md — DEL-002-10_Calculation-Package/Datasheet.md
- Specification.md — DEL-002-10_Calculation-Package/Specification.md
- Guidance.md — DEL-002-10_Calculation-Package/Guidance.md
- Procedure.md — DEL-002-10_Calculation-Package/Procedure.md
- _REFERENCES.md — DEL-002-10_Calculation-Package/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 7
  - Specification: 9
  - Guidance: 5
  - Procedure: 4
  - Multi: 3
- By matrix:
  - A: 6  B: 4  C: 4  F: 4  D: 3  X: 4  E: 3
- By type:
  - Conflict: 2
  - VerificationGap: 5
  - MissingSlot: 6
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 5
  - MatrixError: 0
- Notable conflicts: 2
- Matrix parse errors: 0

---

## Matrix A — Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Code edition specificity gap |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | P.Eng. stamp process detail |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Code compliance verification specificity |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | No external audit/permit linkage |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Step 1 adequately establishes procedural direction |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Procedure Steps 2-4 cover practical execution adequately |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | Acceptance criteria for calc checks |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Procedure Step 5 QA review is adequate |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Purpose section covers value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs table addresses merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 1 | HAS_ITEMS | No criteria for evaluating calc package quality beyond pass/fail |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | QA review record covers this |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Datasheet | Datasheet | Clarify which specific NBC edition and CSA standard editions govern; replace "ASSUMPTION: likely applicable" with confirmed editions or explicit TBD with resolution trigger | The Governing Codes table uses "ASSUMPTION: likely applicable" for four of six entries, which is materially vague for a prescriptive-direction lens — the calculations cannot proceed to final without confirmed code editions | Datasheet.md | Governing Codes and Standards | — | PROPOSAL: Structural Engineer of Record confirms at design kickoff (Procedure Step 1a) | TBD |
| A-002 | A:normative:applying | MissingSlot | Specification | Procedure | Add explicit procedure step or prerequisite for how the P.Eng. stamp process is verified (e.g., stamp validation, license currency check) | REQ-011 requires P.Eng. stamp but neither Specification verification table nor Procedure Step 9 describe how stamp validity is confirmed (e.g., license in good standing, correct jurisdiction) | Specification.md, Procedure.md | REQ-011 verification row; Step 9 | — | PROPOSAL: Add a verification note in Procedure Step 9 referencing APEGA license verification | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add acceptance criteria specifying what constitutes a code-compliance pass (e.g., all limit states checked, load combinations per NBC Table 4.1.3.2) | REQ-010 verification says "Cover sheet lists codes used; Structural Engineer of Record confirms compliance" but does not define measurable acceptance criteria for compliance determination | Specification.md | Verification — REQ-010 | — | PROPOSAL: Structural Engineer of Record defines acceptance standard | TBD |
| A-004 | A:normative:reviewing | MissingSlot | Multi | Guidance | Add a note in Guidance or Procedure linking the calculation package to the building permit application process (PKG-009) and any municipal review requirements | Neither Guidance nor Procedure address how the calculation package supports regulatory audit by the authority having jurisdiction (AHJ) for building permit (PKG-009). Guidance mentions PKG-009 once but does not describe submission requirements. | Guidance.md, Procedure.md | entire document scanned | — | PROPOSAL: Guidance Considerations section | TBD |
| A-005 | A:operative:judging | WeakStatement | Specification | Specification | Strengthen verification for REQ-007 to include pass/fail criteria for crane runway beam design (e.g., deflection limits per crane manufacturer or code, fatigue check if applicable) | REQ-007 verification says "Crane end-reaction loads documented; manufacturer data or conservative assumption noted" but does not specify what acceptance thresholds determine a pass | Specification.md | Verification — REQ-007 | — | PROPOSAL: Structural Engineer of Record sets crane runway acceptance criteria | TBD |
| A-006 | A:evaluative:judging | RationaleGap | Guidance | Guidance | Add discussion of what distinguishes a high-quality calculation package from a minimally compliant one in the context of this project | Guidance Trade-offs table addresses system selection trade-offs but does not discuss quality benchmarks for the calculation package itself (e.g., calculation depth, presentation standard, peer review rigor) | Guidance.md | Trade-offs section | — | PROPOSAL: Guidance Considerations or new Quality Expectations section | TBD |

---

## Matrix B — Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Missing climatic load values |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Geotechnical data adequacy |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | TBD values in Datasheet |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Dimensions and capacities are consistently stated across documents |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (scope, exclusions, dependencies) are present |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context is adequate across documents |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Document set provides comprehensive account |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Foundation scope boundary terminology |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Structural engineering fundamentals appropriately addressed |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise requirements are clear |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Procedure provides thorough coverage |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs and Conflict Table provide essential discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment guidance is adequate |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance provides holistic perspective |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Obtain NBC Appendix C climatic data for Ferintosh/Camrose area (ground snow load Ss/Sr, wind pressure q, seismic Sa values) and populate Design Conditions table | Site seismicity, snow load, wind load, and design temperature are all listed as TBD in the Datasheet Design Conditions table. These are essential facts without which final calculations cannot proceed. | Datasheet.md | Design Conditions table | — | PROPOSAL: Structural Engineer of Record sources from NBC Appendix C | TBD |
| B-002 | B:data:sufficiency | TBD_Question | Datasheet | Datasheet | Record TBD: Confirm mezzanine design live load — either from Owner-specified storage intent or from NBC Table 4.1.5.3 minimum | Mezzanine Design Load is listed as "TBD" in Datasheet Design Conditions. Guidance discusses oil totes (~1 tonne each) but no numeric load value is established. This is a critical design input. | Datasheet.md | Design Conditions — Mezzanine Design Load; Key Design Parameters — Mezzanine Loading | — | PROPOSAL: Owner confirmation or Structural Engineer of Record per NBC | TBD |
| B-003 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add a row to Key Design Parameters for the lateral load resisting system type (TBD pending Structural Engineer of Record decision) | The Datasheet records building dimensions, crane capacity, and material type but does not record the lateral system type, which is a fundamental structural parameter. Guidance discusses the trade-off but no parameter slot exists in the Datasheet. | Datasheet.md | Key Design Parameters table | — | PROPOSAL: Add row with value TBD pending design kickoff | TBD |
| B-004 | B:information:consistency | Normalization | Multi | Guidance | Normalize terminology for the foundation scope boundary: use consistent phrasing across documents (e.g., "variable-price foundation scope (SOW-0019)" vs. "foundation pricing basis" vs. "Foundation Design Package") | The Datasheet uses "Foundation Pricing Basis: Normal ground conditions (variable-price per geotech results)"; Specification REQ-014 uses "foundation design scope (SOW-0019)"; Guidance Principle 3 uses "foundation pricing is negotiated post-geotech." While all refer to the same concept, the varying phrasing could cause drift in a multi-deliverable context. | Datasheet.md, Specification.md, Guidance.md | Datasheet: Key Design Parameters; Specification: REQ-014; Guidance: Principle 3 | — | PROPOSAL: Guidance vocabulary note establishing canonical term | TBD |

---

## Matrix C — Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforced Compliance Threshold | 1 | HAS_ITEMS | Threshold values not established |
| C:normative:sufficiency | normative | sufficiency | Validated Regulatory Baseline | 0 | NO_ITEMS | Regulatory baseline adequately addressed in Specification Standards table |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Scope | 1 | HAS_ITEMS | Possible missing regulatory reference |
| C:normative:consistency | normative | consistency | Harmonized Regulatory Coherence | 0 | NO_ITEMS | Regulatory references are harmonized across documents |
| C:operative:necessity | operative | necessity | Essential Operational Readiness | 1 | HAS_ITEMS | Prerequisites completeness |
| C:operative:sufficiency | operative | sufficiency | Competent Procedural Execution | 0 | NO_ITEMS | Procedure steps are sufficient for execution |
| C:operative:completeness | operative | completeness | Thorough Operational Coverage | 0 | NO_ITEMS | All structural subsystems covered in procedure |
| C:operative:consistency | operative | consistency | Standardized Process Integrity | 0 | NO_ITEMS | Process steps are standardized and consistent |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Merit Recognition | 0 | NO_ITEMS | Merit is recognized through Guidance Purpose section |
| C:evaluative:sufficiency | evaluative | sufficiency | Credible Worth Assessment | 1 | HAS_ITEMS | Missing assessment criteria |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Value Appraisal | 0 | NO_ITEMS | Value covered by Guidance trade-offs |
| C:evaluative:consistency | evaluative | consistency | Principled Value Consistency | 0 | NO_ITEMS | Value reasoning is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | VerificationGap | Specification | Specification | Add specific acceptance thresholds to REQ-008 verification (e.g., floor slab punching shear check, bearing stress check at embedment locations) | REQ-008 verification says "Floor slab calculations include load case for tracked/packer equipment at plate locations" — this confirms load case inclusion but not a pass/fail threshold. The enforced compliance threshold lens reveals no quantified acceptance criterion for this structural check. | Specification.md | Verification — REQ-008 | — | PROPOSAL: Structural Engineer of Record per CSA A23.3 limit states | TBD |
| C-002 | C:normative:completeness | TBD_Question | Specification | Specification | Confirm whether CSA S304 (Design of Masonry Structures) or other standards apply; if concrete tilt-up panels are used, confirm whether NBC Part 4 seismic provisions for tilt-up apply | Under the exhaustive regulatory scope lens, the Standards table covers NBC, CSA A23.3, CSA S16, and Alberta Safety Codes, but does not address whether tilt-up-specific provisions or other specialized standards (e.g., for service pit waterproofing design) may apply depending on structural system selection. | Specification.md | Standards table | — | PROPOSAL: Structural Engineer of Record confirms at design kickoff | TBD |
| C-003 | C:operative:necessity | MissingSlot | Procedure | Procedure | Add an explicit prerequisite or early step for confirming the structural system type before detailed calculations begin | The Procedure Prerequisites table lists "Structural system selection" as "TBD — Structural Engineer of Record decision at design kickoff" and notes it is "Not blocking for starting." However, under the Essential Operational Readiness lens, this is an essential operational decision that gates all subsequent calculation logic. No step explicitly captures the go/no-go decision point. | Procedure.md | Prerequisites table — Structural system selection | — | PROPOSAL: Add decision-point gate between Steps 1 and 2 | TBD |
| C-004 | C:evaluative:sufficiency | RationaleGap | Guidance | Guidance | Add rationale for why conservative assumptions (crane loads, foundation) are preferred over waiting for confirmed data, referencing schedule risk and contractual implications | The Trade-offs table lists the crane data and foundation trade-offs but the "Consideration" column does not explicitly state the risk/schedule rationale for choosing conservative assumptions over deferral. Under the credible worth assessment lens, the justification for the chosen approach needs to be defensible. | Guidance.md | Trade-offs table — Crane data availability row; Foundation prior to geotech row | — | PROPOSAL: Expand Consideration column or add Rationale subsection | TBD |

---

## Matrix F — Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandated Regulatory Foundation | 1 | HAS_ITEMS | Regulatory foundation incomplete |
| F:normative:sufficiency | normative | sufficiency | Substantiated Conformance Framework | 0 | NO_ITEMS | Conformance framework is substantiated |
| F:normative:completeness | normative | completeness | Absolute Conformance Authority | 0 | NO_ITEMS | Conformance scope is comprehensive |
| F:normative:consistency | normative | consistency | Stable Conformance Reasoning | 0 | NO_ITEMS | Reasoning is stable and consistent |
| F:operative:necessity | operative | necessity | Core Operational Fitness | 1 | HAS_ITEMS | Missing operational fitness criteria |
| F:operative:sufficiency | operative | sufficiency | Demonstrated Capable Performance | 0 | NO_ITEMS | Performance demonstration path is clear |
| F:operative:completeness | operative | completeness | Exhaustive Process Mastery | 0 | NO_ITEMS | Process coverage is exhaustive |
| F:operative:consistency | operative | consistency | Systematic Operational Coherence | 1 | HAS_ITEMS | Step numbering cross-reference |
| F:evaluative:necessity | evaluative | necessity | Foundational Merit Evidence | 0 | NO_ITEMS | Merit evidence addressed in Guidance Purpose |
| F:evaluative:sufficiency | evaluative | sufficiency | Defensible Value Justification | 0 | NO_ITEMS | Value justification is defensible |
| F:evaluative:completeness | evaluative | completeness | Absolute Appraisal Synthesis | 0 | NO_ITEMS | Appraisal scope is complete |
| F:evaluative:consistency | evaluative | consistency | Principled Appraisal Stability | 1 | HAS_ITEMS | Conflict table completeness |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | VerificationGap | Specification | Specification | Add verification approach for REQ-005 that specifies how "updated or confirmed" is determined (e.g., what constitutes a material difference in geotech findings vs. assumed conditions) | REQ-005 requires foundation calculations to be "updated or confirmed" following geotech delivery. The verification row says "Updated calculations issued following receipt of DEL-008-01; revision tracked in calculation log." This does not define the threshold for when confirmation vs. update is required — the mandated regulatory foundation lens reveals this gap. | Specification.md | Verification — REQ-005 | — | PROPOSAL: Structural Engineer of Record defines material-difference threshold | TBD |
| F-002 | F:operative:necessity | VerificationGap | Procedure | Procedure | Add explicit go/no-go criteria for Gate G-3 (preliminary calculations) specifying what level of completeness qualifies as "sufficient to support DEL-002-01" | Procedure Gate G-3 states "Preliminary calculations complete to support DEL-002-01" but does not define what calculations are minimally required for this gate. Under the Core Operational Fitness lens, the fitness threshold for the preliminary milestone needs specification. | Procedure.md | Verification — Gate G-3 | — | PROPOSAL: Define minimum calculation scope for preliminary design support | TBD |
| F-003 | F:operative:consistency | Normalization | Procedure | Procedure | Standardize the cross-reference format between Procedure steps and Specification requirements (e.g., each Procedure step should cite the REQ it satisfies) | Procedure Step 4 references "applicable load cases" and "limit states (ULS and SLS per NBC/CSA)" but does not cross-reference back to specific REQ numbers. Under the Systematic Operational Coherence lens, explicit traceability from procedure steps to requirements would improve coherence. | Procedure.md | Steps section — Step 4 | — | PROPOSAL: Add REQ cross-references in each Procedure step | TBD |
| F-004 | F:evaluative:consistency | Conflict | Guidance | Guidance | Resolve whether the gantry/crane conflict (C-002) should also appear in the Specification as a conditional requirement or assumption | Guidance Conflict Table C-002 identifies the gantry vs. overhead crane ambiguity, but Specification REQ-007 does not contain a conditional clause addressing this possibility. Under the Principled Appraisal Stability lens, the appraisal of this conflict should be consistent across the normative and directional documents. | Guidance.md, Specification.md | Guidance: Conflict Table C-002; Specification: REQ-007 | Guidance.md#Conflict Table C-002, Specification.md#REQ-007 | PROPOSAL: Add assumption statement to REQ-007 referencing C-002 | TBD |

---

## Matrix D — Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Established Authoritative Mandate | 1 | HAS_ITEMS | Mandate traceability |
| D:normative:applying | normative | applying | Enforced Compliance Protocol | 0 | NO_ITEMS | Compliance protocol is established in Specification and Procedure |
| D:normative:judging | normative | judging | Definitive Compliance Verdict | 0 | NO_ITEMS | Verification table provides verdict framework |
| D:normative:reviewing | normative | reviewing | Resolved Compliance Inspection | 0 | NO_ITEMS | QA review addresses this |
| D:operative:guiding | operative | guiding | Confirmed Process Governance | 0 | NO_ITEMS | Process governance established through Procedure |
| D:operative:applying | operative | applying | Verified Practical Delivery | 1 | HAS_ITEMS | Delivery format unspecified |
| D:operative:judging | operative | judging | Confirmed Capability Control | 0 | NO_ITEMS | Capability control addressed by verification gates |
| D:operative:reviewing | operative | reviewing | Confirmed Workflow Verification | 0 | NO_ITEMS | Workflow verification addressed by QA steps |
| D:evaluative:guiding | evaluative | guiding | Established Merit Direction | 0 | NO_ITEMS | Merit direction established in Guidance Purpose |
| D:evaluative:applying | evaluative | applying | Justified Value Deployment | 0 | NO_ITEMS | Value deployment justified through trade-offs |
| D:evaluative:judging | evaluative | judging | Definitive Worth Adjudication | 1 | HAS_ITEMS | No criteria for package acceptance by Owner |
| D:evaluative:reviewing | evaluative | reviewing | Anchored Merit Inspection | 0 | NO_ITEMS | QA review provides merit inspection |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:guiding | Normalization | Specification | Specification | Add explicit SOW traceability to each REQ (some have SOW references, REQ-003 and REQ-012 cite different source patterns) | REQ-001 cites "SOW-0012, SOW-0019"; REQ-002 cites "SOW-0022"; REQ-012 cites "Decomposition PKG-002 scope description; SOW-0012." The source-reference format is inconsistent, which under the Established Authoritative Mandate lens weakens traceability of the mandate. | Specification.md | Requirements section — Source lines | — | PROPOSAL: Standardize source citation format across all REQs | TBD |
| D-002 | D:operative:applying | MissingSlot | Procedure | Procedure | Add a step or note specifying the physical/digital delivery format for the calculation package (binder, PDF, electronic file naming convention) | Procedure Step 9 addresses P.Eng. stamp and issue but does not specify the delivery format. Under the Verified Practical Delivery lens, the practical form of delivery is a missing operational slot. | Procedure.md | Step 9 — P.Eng. Stamp and Issue | — | PROPOSAL: Add delivery format requirements to Step 9 or Records section | TBD |
| D-003 | D:evaluative:judging | MissingSlot | Specification | Specification | Add an acceptance criterion or milestone defining when the calculation package is considered "accepted" by the Owner/County (e.g., upon building permit issuance, upon County review of DEL-002-01) | Neither Specification nor Guidance define the conditions under which the calculation package is considered definitively accepted. Under the Definitive Worth Adjudication lens, this acceptance endpoint is missing. | Specification.md | entire document scanned | — | PROPOSAL: Add acceptance milestone linked to OBJ-001 or building permit | TBD |

---

## Matrix X — Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Cardinal Governance Purpose | 0 | NO_ITEMS | Governance purpose clear in Guidance |
| X:guiding:sufficiency | guiding | sufficiency | Substantiated Stewardship | 0 | NO_ITEMS | Stewardship adequately substantiated |
| X:guiding:completeness | guiding | completeness | Exhaustive Leadership Scope | 0 | NO_ITEMS | Leadership scope is exhaustive |
| X:guiding:consistency | guiding | consistency | Coherent Governance Alignment | 0 | NO_ITEMS | Governance is coherent |
| X:applying:necessity | applying | necessity | Vital Execution Foundation | 1 | HAS_ITEMS | Missing execution prerequisite |
| X:applying:sufficiency | applying | sufficiency | Justified Implementation Basis | 0 | NO_ITEMS | Implementation basis is justified |
| X:applying:completeness | applying | completeness | Comprehensive Execution Scope | 1 | HAS_ITEMS | Wash bay and stair calc detail |
| X:applying:consistency | applying | consistency | Uniform Execution Reliability | 0 | NO_ITEMS | Execution reliability is uniform |
| X:judging:necessity | judging | necessity | Binding Capability Finding | 1 | HAS_ITEMS | Capability finding for service pit |
| X:judging:sufficiency | judging | sufficiency | Qualified Determination Basis | 0 | NO_ITEMS | Determination basis is qualified |
| X:judging:completeness | judging | completeness | Thorough Judgment Authority | 0 | NO_ITEMS | Judgment authority is thorough |
| X:judging:consistency | judging | consistency | Stable Ruling Coherence | 0 | NO_ITEMS | Rulings are coherent |
| X:reviewing:necessity | reviewing | necessity | Foundational Audit Grounding | 1 | HAS_ITEMS | Revision tracking |
| X:reviewing:sufficiency | reviewing | sufficiency | Justified Audit Competence | 0 | NO_ITEMS | Audit competence is justified |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Audit Scope | 0 | NO_ITEMS | Audit scope is exhaustive |
| X:reviewing:consistency | reviewing | consistency | Uniform Audit Coherence | 0 | NO_ITEMS | Audit coherence is uniform |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Obtain or estimate equipment wheel/track loads for floor slab design — specific equipment models and weights are not stated in available sources | Datasheet lists steel plate embedments for "tracked/packer heavy equipment" but no equipment weight or wheel load data appears in any document. Under the Vital Execution Foundation lens, this is a necessary execution input that is missing. | Datasheet.md | Key Design Parameters — Steel Plate Locations; Scope of Calculations — Steel Plate Embedments | — | PROPOSAL: Owner or equipment supplier provides data; or Structural Engineer assumes conservative values | TBD |
| X-002 | X:applying:completeness | WeakStatement | Specification | Specification | Strengthen the scope description for wash bay and stair calculations (items 7 and 8 in Scope) to specify structural subsystem scope comparable to other items | Specification scope items 7 (wash bay) and 8 (stair) are described more briefly than items 1-6. Under the Comprehensive Execution Scope lens, the execution scope for these subsystems should be equally well-defined. | Specification.md | Scope — items 7 and 8 | — | PROPOSAL: Expand scope descriptions to match detail level of items 1-6 | TBD |
| X-003 | X:judging:necessity | VerificationGap | Specification | Specification | Add specific verification approach for REQ-009 service pit hydrostatic load case, making it conditional on geotech findings rather than unconditional | REQ-009 verification says "Pit structural calculations include lateral earth, hydrostatic (if applicable), and surcharge load cases." The "(if applicable)" condition has no defined trigger — what determines applicability? Under the Binding Capability Finding lens, this conditional verification needs a binding determination criterion. | Specification.md | Verification — REQ-009 | — | PROPOSAL: Link hydrostatic applicability to geotech report water table findings | TBD |
| X-004 | X:reviewing:necessity | WeakStatement | Procedure | Procedure | Clarify the calculation revision tracking mechanism in Procedure Records — specify what information a revision log entry must contain (date, reason, sections affected, reviewer) | Procedure Records table lists "Calculation Revision Log — Record of all revisions to the calculation package, with reason and date" but does not define minimum content fields. Under the Foundational Audit Grounding lens, the revision log needs a defined schema to ground audits. | Procedure.md | Records table — Calculation Revision Log | — | PROPOSAL: Add minimum-content specification for revision log entries | TBD |

---

## Matrix E — Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Guidance Record | 0 | NO_ITEMS | Guidance record is authoritative |
| E:guiding:information | guiding | information | Coherent Steering Intelligence | 0 | NO_ITEMS | Steering intelligence is coherent |
| E:guiding:knowledge | guiding | knowledge | Strategic Stewardship Mastery | 0 | NO_ITEMS | Stewardship mastery demonstrated |
| E:guiding:wisdom | guiding | wisdom | Holistic Governance Foresight | 1 | HAS_ITEMS | Long-term governance gap |
| E:applying:data | applying | data | Substantiated Performance Record | 0 | NO_ITEMS | Performance record is substantiated |
| E:applying:information | applying | information | Contextual Execution Intelligence | 0 | NO_ITEMS | Execution intelligence is contextual |
| E:applying:knowledge | applying | knowledge | Proficient Implementation Authority | 0 | NO_ITEMS | Implementation authority is proficient |
| E:applying:wisdom | applying | wisdom | Grounded Implementation Wisdom | 0 | NO_ITEMS | Implementation wisdom is grounded |
| E:judging:data | judging | data | Verified Determination Record | 1 | HAS_ITEMS | Determination record completeness |
| E:judging:information | judging | information | Contextual Ruling Intelligence | 0 | NO_ITEMS | Ruling intelligence is contextual |
| E:judging:knowledge | judging | knowledge | Masterful Adjudication Authority | 0 | NO_ITEMS | Adjudication authority is established |
| E:judging:wisdom | judging | wisdom | Principled Determination Foresight | 0 | NO_ITEMS | Determination foresight is principled |
| E:reviewing:data | reviewing | data | Substantiated Audit Record | 0 | NO_ITEMS | Audit record is substantiated |
| E:reviewing:information | reviewing | information | Coherent Inspection Intelligence | 0 | NO_ITEMS | Inspection intelligence is coherent |
| E:reviewing:knowledge | reviewing | knowledge | Comprehensive Inspection Mastery | 0 | NO_ITEMS | Inspection mastery is comprehensive |
| E:reviewing:wisdom | reviewing | wisdom | Principled Audit Foresight | 1 | HAS_ITEMS | Guarantee period audit |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:wisdom | RationaleGap | Guidance | Guidance | Add foresight discussion on how the calculation package should be structured for long-term maintainability (e.g., future building modifications, additions, or re-analysis during the guarantee period) | Guidance discusses immediate design and coordination concerns but does not address long-term governance of the calculation package. Under the Holistic Governance Foresight lens, the absence of a forward-looking maintenance perspective is a rationale gap. | Guidance.md | entire document scanned | — | PROPOSAL: Add a "Long-Term Considerations" subsection to Guidance | TBD |
| E-002 | E:judging:data | Conflict | Specification | Specification | Resolve whether the Specification Documentation section's "ASSUMPTION" label for minimum content contradicts the normative force of REQ-001 completeness requirement | Specification Documentation section header says "ASSUMPTION: Based on standard Alberta structural engineering practice and RFP scope requirements, the Calculation Package is anticipated to include (at minimum)..." while REQ-001 says the package "shall address all structural subsystems listed in the Scope section." The list in Documentation is framed as assumption-based while the requirement is mandatory. Under the Verified Determination Record lens, the evidentiary basis for completeness has conflicting authority signals. | Specification.md | Documentation — Minimum Content; Requirements — REQ-001 | Specification.md#Documentation — Minimum Content, Specification.md#REQ-001 | PROPOSAL: Remove ASSUMPTION label from Documentation minimum content or clarify its relationship to REQ-001 | TBD |
| E-003 | E:reviewing:wisdom | TBD_Question | Procedure | Procedure | Record TBD: Confirm records retention requirements — Procedure cites "construction period plus 2 years post-CCC" per RFP §2.10.2, but verify whether Alberta professional engineering obligations require longer retention | Procedure Retention section cites RFP §2.10 but notes Alberta Engineering and Geoscience Professions Act obligations "may" apply. Under the Principled Audit Foresight lens, the retention period should be definitively confirmed to ensure audit readiness over the full required period. | Procedure.md | Records — Retention | — | PROPOSAL: Structural Engineer of Record confirms APEGA retention requirements | TBD |
