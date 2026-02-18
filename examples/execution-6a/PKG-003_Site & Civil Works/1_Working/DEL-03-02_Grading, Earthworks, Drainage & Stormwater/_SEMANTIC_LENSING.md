# Semantic Lensing Register: DEL-03-02 Grading, Earthworks, Drainage & Stormwater

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/PKG-003_Site & Civil Works/1_Working/DEL-03-02_Grading, Earthworks, Drainage & Stormwater/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-03-02; PKG-003; Civil/Geotechnical coordination; SOW-0105, SOW-0106; OBJ-005
- _STATUS.md -- Current State: SEMANTIC_READY (as of 2026-02-17)
- _SEMANTIC.md -- Matrices A, B, C, F, D, X, E parsed successfully (92 cells total)
- Datasheet.md -- Present and read (site conditions, earthworks parameters, drainage parameters, excavation cut slopes, conditions, construction elements)
- Specification.md -- Present and read (REQ-3201 through REQ-3215; standards; verification matrix)
- Guidance.md -- Present and read (purpose, principles, considerations, trade-offs, examples, conflict table)
- Procedure.md -- Present and read (Part A proposal production steps A-1 through A-9; Part B construction phases B-1 through B-7; verification checks; records)
- _REFERENCES.md -- Present and read (OSR, Geotech Report, Site Grading drawings)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 5
  - Specification: 10
  - Guidance: 5
  - Procedure: 3
  - Multi: 5
- By matrix:
  - A: 5  B: 4  C: 3  F: 4  D: 4  X: 5  E: 3
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

### Lens Coverage (required)

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Weak prescriptive direction for dewatering |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Missing mandatory practice for cut/fill balance |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Municipal development standards compliance gap |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit provisions adequately covered |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedural direction well-established in Part A and Part B |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Dewatering execution gap |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Performance assessment covered via verification tables |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Process audit covered via records and geotech certification |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | Value rationale for compaction frequency missing |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Merit application adequately addressed |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Worth determination adequately addressed |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality appraisal mechanisms present |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Guidance | Guidance | Clarify prescriptive direction for dewatering requirements during excavation (Guidance Considerations mentions dewatering anticipation but no prescriptive minimum or method is stated) | Guidance mentions "dewatering plans should be anticipated" but this is vague for excavations that will encounter groundwater at 3-4 m; no prescriptive direction on dewatering method, discharge, or monitoring | Guidance.md | Considerations > Groundwater management during construction | -- | Geotech Report USG1123 | TBD |
| A-002 | A:normative:applying | MissingSlot | Specification | Specification | Add requirement for cut/fill balance estimation or documentation as a mandatory practice deliverable | Specification covers individual earthworks requirements but does not mandate a cut/fill balance analysis; Datasheet notes "Cut/fill balance: TBD" but no requirement drives its resolution | Specification.md; Datasheet.md | Construction > Cut/fill balance; entire Specification scanned | -- | Civil Engineer | TBD |
| A-003 | A:normative:judging | TBD_Question | Multi | Specification | Record TBD: Confirm which Municipal Development Standards (Town of Penhold) apply to grading and drainage design and add as normative requirements | Specification Standards table lists "Municipal Development Standards (Town of Penhold)" as "ASSUMPTION: likely applicable; location TBD" -- compliance determination cannot proceed without confirming applicability | Specification.md | Standards table | -- | Owner / Town of Penhold | TBD |
| A-004 | A:operative:applying | MissingSlot | Procedure | Procedure | Add dewatering procedure steps for excavations approaching 3-4 m depth where groundwater will be encountered | Procedure Part B covers excavation safety (B-2) and drainage construction (B-6) but contains no step for dewatering during construction; Guidance identifies this as an anticipated need | Procedure.md; Guidance.md | Part B phases B-2 through B-6; Considerations > Groundwater management | -- | Geotechnical Engineer | TBD |
| A-005 | A:evaluative:guiding | RationaleGap | Guidance | Guidance | Add rationale for why minimum compaction testing frequency of 1 per lift per 500 m2 is appropriate (or whether higher frequency is warranted in high-risk zones) | Guidance Trade-offs section notes "minimum frequency should be treated as a floor, not a ceiling" and mentions high-risk areas, but does not explain how to determine when higher frequency is warranted | Guidance.md | Trade-offs > Proof rolling vs. compaction testing | -- | Geotechnical Engineer | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage (required)

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Cut/fill quantities TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Geotech report vintage concern |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Missing sulphate test data |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurements from geotech report consistently cited |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals adequately identified |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequately provided |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Account is comprehensive for available sources |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology normalization needed |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding of site conditions present |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise roles identified |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Thorough mastery of geotech parameters present |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Key discernments captured in Guidance |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment adequately reflected in trade-offs |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view present across documents |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Principled reasoning consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add cut/fill quantity estimates or record as formal TBD requiring post-award resolution | Datasheet Construction table states "Cut/fill balance: TBD (cut/fill plan shown in TPN46 Sheet C2 and C3; quantities not extracted)" -- this is an essential fact for cost estimation and earthworks planning | Datasheet.md | Construction > Cut/fill balance | -- | Civil Engineer / TPN46 analysis | TBD |
| B-002 | B:data:sufficiency | WeakStatement | Datasheet | Datasheet | Strengthen the geotech report vintage condition to explicitly state what "insufficient" means and what triggers supplemental investigation | Datasheet Conditions table notes "Geotechnical report vintage: Report dated Feb 2021; conditions may have changed; DB may need supplemental geotech if insufficient" but the threshold for "insufficient" is undefined | Datasheet.md | Conditions > Geotechnical report vintage | -- | Geotechnical Engineer | TBD |
| B-003 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add note that laboratory sulphate testing was not performed and the S-2 classification is conservative/precautionary | Guidance mentions "Laboratory testing was not performed for water-soluble sulphate content" but this important qualification is absent from Datasheet where the S-2 classification is stated as fact | Datasheet.md; Guidance.md | Datasheet > Site Conditions > Sulphate attack designation; Guidance > Considerations > Sulphate attack on concrete | -- | Geotechnical Engineer | TBD |
| B-004 | B:information:consistency | Normalization | Multi | Guidance | Normalize terminology: "MUSC SC" vs "medium plastic (SC)" vs "clayey sand" are used interchangeably; establish canonical term | The sand layer is referred to as "Clayey Sand (MUSC SC)" in Datasheet, "medium plastic (SC)" in Guidance, and "sand" generically in Specification; this inconsistency could cause confusion in material acceptance | Datasheet.md; Guidance.md; Specification.md | Datasheet > Sand layer; Guidance > Principles > 3; Specification > REQ-3204 | -- | Geotechnical Engineer | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage (required)

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Compliance Threshold | 1 | HAS_ITEMS | NBC/ABC applicability gap |
| C:normative:sufficiency | normative | sufficiency | Regulatory Adequacy Standard | 0 | NO_ITEMS | Regulatory adequacy standards referenced |
| C:normative:completeness | normative | completeness | Full Regulatory Coverage | 1 | HAS_ITEMS | Incomplete standards accessibility |
| C:normative:consistency | normative | consistency | Regulatory Conformance Integrity | 0 | NO_ITEMS | Conformance integrity consistent |
| C:operative:necessity | operative | necessity | Critical Operational Prerequisite | 0 | NO_ITEMS | Prerequisites well-documented |
| C:operative:sufficiency | operative | sufficiency | Competent Execution Baseline | 0 | NO_ITEMS | Execution baseline adequate |
| C:operative:completeness | operative | completeness | Total Operational Coverage | 1 | HAS_ITEMS | Permanent erosion control gap |
| C:operative:consistency | operative | consistency | Reliable Process Fidelity | 0 | NO_ITEMS | Process fidelity consistent |
| C:evaluative:necessity | evaluative | necessity | Core Quality Imperative | 0 | NO_ITEMS | Core quality imperatives captured |
| C:evaluative:sufficiency | evaluative | sufficiency | Satisfactory Merit Standard | 0 | NO_ITEMS | Merit standards sufficient |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Quality Account | 0 | NO_ITEMS | Quality account comprehensive |
| C:evaluative:consistency | evaluative | consistency | Principled Quality Fidelity | 0 | NO_ITEMS | Quality fidelity principled and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | TBD_Question | Specification | Specification | Record TBD: Confirm applicability of Alberta National Building Code (NBC) and Alberta Building Code (ABC) to site grading and drainage; add as enforceable standards if applicable | Specification Standards table lists NBC and ABC as "ASSUMPTION: likely applicable; location TBD" -- these are potentially enforceable compliance thresholds that remain unconfirmed | Specification.md | Standards table | -- | Owner / AHJ (Town of Penhold) | TBD |
| C-002 | C:normative:completeness | WeakStatement | Specification | Specification | Clarify status of inaccessible external standards (Alberta OHS Code Part 32, CAN/CSA A23.1-2014, City of Red Deer Aggregate Spec) -- indicate whether DB is expected to self-source or whether Owner will provide | Three external standards are referenced as normative but marked "not directly accessible" or "text not reproduced"; full regulatory coverage requires DB to have access to these standards | Specification.md | Standards table | -- | Owner | TBD |
| C-003 | C:operative:completeness | MissingSlot | Specification | Specification | Add requirement for permanent erosion control / slope stabilization after construction is complete (seeding, armoring, or other) | Procedure Phase B-7 mentions "Stabilize completed slopes (seeding or other permanent erosion control) promptly after grading is complete" but no corresponding Specification requirement exists; only temporary erosion control (REQ-3213) is specified | Specification.md; Procedure.md | REQ-3213; Phase B-7 | -- | Civil Engineer | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage (required)

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandatory Compliance Basis | 0 | NO_ITEMS | Compliance basis well-established |
| F:normative:sufficiency | normative | sufficiency | Prescribed Compliance Sufficiency | 1 | HAS_ITEMS | Stormwater pond sizing gap |
| F:normative:completeness | normative | completeness | Exhaustive Statutory Scope | 1 | HAS_ITEMS | Drainage outlet design criteria gap |
| F:normative:consistency | normative | consistency | Mandated Standard Coherence | 0 | NO_ITEMS | Standards coherently referenced |
| F:operative:necessity | operative | necessity | Essential Execution Threshold | 1 | HAS_ITEMS | Topographic survey timing gap |
| F:operative:sufficiency | operative | sufficiency | Adequate Capability Assurance | 0 | NO_ITEMS | Capability assurance adequate |
| F:operative:completeness | operative | completeness | Exhaustive Capability Scope | 0 | NO_ITEMS | Capability scope complete |
| F:operative:consistency | operative | consistency | Stable Operational Coherence | 0 | NO_ITEMS | Operational coherence stable |
| F:evaluative:necessity | evaluative | necessity | Fundamental Merit Threshold | 0 | NO_ITEMS | Merit thresholds identified |
| F:evaluative:sufficiency | evaluative | sufficiency | Acceptable Valuation Baseline | 1 | HAS_ITEMS | Cost implications of fill import underexplored |
| F:evaluative:completeness | evaluative | completeness | Total Valuation Comprehension | 0 | NO_ITEMS | Valuation comprehension adequate for this stage |
| F:evaluative:consistency | evaluative | consistency | Principled Valuation Stability | 0 | NO_ITEMS | Valuation principles stable |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add acceptance criteria for stormwater retention pond sizing (capacity, design storm event, outlet flow rate) | REQ-3212 requires a stormwater retention pond but specifies no sizing criteria, design storm event, or outlet flow rate; Verification table says "Drawing review (pond design)" without quantitative acceptance criteria | Specification.md | REQ-3212; Verification table > REQ-3212 | -- | Civil Engineer / Municipal standards | TBD |
| F-002 | F:normative:completeness | MissingSlot | Specification | Specification | Add drainage outlet design criteria (outlet protection type, sizing, energy dissipation requirements) for complete statutory scope | REQ-3211 and REQ-3213 reference erosion protection at drainage outlets but do not specify outlet design criteria (protection type, sizing, velocity limits); this leaves the scope of "erosion protection" open to interpretation | Specification.md | REQ-3211; REQ-3213 | -- | Civil Engineer | TBD |
| F-003 | F:operative:necessity | VerificationGap | Procedure | Procedure | Add verification step confirming topographic survey is completed and reconciled with TPN46 before grading plan finalization | Procedure Phase B-1 step 1 mentions obtaining a current topographic survey and reconciling with TPN46, but no verification check confirms this essential execution threshold is met before proceeding | Procedure.md | Phase B-1 step 1; Verification table | -- | Civil Engineer | TBD |
| F-004 | F:evaluative:sufficiency | RationaleGap | Guidance | Guidance | Add rationale or estimation guidance for imported granular fill quantities and cost impact to support pricing at proposal stage | Guidance Trade-offs discusses import vs. reuse but provides no basis for estimating import quantities or cost impact; at proposal stage this is a fundamental merit threshold for competitive pricing | Guidance.md | Trade-offs > Import clean granular fill vs. reuse native soil | -- | Civil Engineer / Estimator | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage (required)

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Established Regulatory Directive | 0 | NO_ITEMS | Regulatory directives established |
| D:normative:applying | normative | applying | Resolved Compliance Mandate | 1 | HAS_ITEMS | Unresolved compliance mandate for pond approvals |
| D:normative:judging | normative | judging | Definitive Conformance Ruling | 0 | NO_ITEMS | Conformance rulings deferred appropriately to human |
| D:normative:reviewing | normative | reviewing | Mandated Uniformity Review | 0 | NO_ITEMS | Uniformity review mechanisms present |
| D:operative:guiding | operative | guiding | Grounded Procedural Guidance | 1 | HAS_ITEMS | Seasonal earthworks scheduling gap |
| D:operative:applying | operative | applying | Resolved Operational Deployment | 0 | NO_ITEMS | Operational deployment resolved |
| D:operative:judging | operative | judging | Settled Performance Verdict | 1 | HAS_ITEMS | Ponding assessment criteria gap |
| D:operative:reviewing | operative | reviewing | Resolved Process Verification | 0 | NO_ITEMS | Process verification resolved |
| D:evaluative:guiding | evaluative | guiding | Grounded Value Alignment | 0 | NO_ITEMS | Value alignment grounded |
| D:evaluative:applying | evaluative | applying | Resolved Merit Deployment | 0 | NO_ITEMS | Merit deployment resolved |
| D:evaluative:judging | evaluative | judging | Definitive Quality Verdict | 1 | HAS_ITEMS | No hold/release criterion for subgrade |
| D:evaluative:reviewing | evaluative | reviewing | Resolved Quality Reassessment | 0 | NO_ITEMS | Quality reassessment resolved |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | Conflict | Multi | TBD | Surface conflict: DEL-03-02 REQ-3212 requires stormwater pond construction, but Guidance Conflict Table C3202-02 notes the pond location may be in flood fringe requiring approvals from DEL-03-05 scope; the mandate is unresolved until regulatory outcome is known | REQ-3212 mandates a stormwater retention pond with specific location, but this location may require environmental/municipal approvals that are outside this deliverable's scope; proceeding without approval would be non-compliant | Specification.md; Guidance.md | REQ-3212; Conflict Table > C3202-02 | Specification.md#REQ-3212; Guidance.md#Conflict-Table-C3202-02 | Owner / DEL-03-05 | TBD |
| D-002 | D:operative:guiding | MissingSlot | Procedure | Procedure | Add guidance on seasonal earthworks scheduling constraints (avoid spring thaw, wet seasons) as a procedural prerequisite or scheduling constraint | Guidance Considerations discusses seasonal earthworks windows as a schedule risk, but Procedure contains no step or prerequisite addressing seasonal timing; this grounded procedural guidance is absent | Procedure.md; Guidance.md | Procedure > Part B prerequisites; Guidance > Considerations > Soil moisture conditioning | -- | Design-Builder | TBD |
| D-003 | D:operative:judging | VerificationGap | Specification | Specification | Add acceptance criteria for "no ponding" verification -- define what constitutes acceptable drainage performance (e.g., time to drain, observation period after storm event, acceptable ponding depth/duration) | REQ-3203 states "No water shall be permitted to pond" and Procedure Verification checks include "No ponding on site: Visual inspection after rain event" but no quantitative or temporal criteria are provided for settling a performance verdict | Specification.md; Procedure.md | REQ-3203; Procedure Verification > No ponding on site | -- | Civil Engineer | TBD |
| D-004 | D:evaluative:judging | VerificationGap | Specification | Specification | Add explicit hold point or release criterion for subgrade acceptance (geotechnical sign-off required before proceeding to next phase) | Specification Verification table lists geotech certification for REQ-3214 but does not establish a formal hold point preventing structure or paving placement until certification is received; Procedure Phase B-5 implies this sequence but it is not a formal quality verdict gate | Specification.md; Procedure.md | Verification table > REQ-3214; Phase B-5 step 2 | -- | Geotechnical Engineer | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage (required)

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Directive Grounding | 0 | NO_ITEMS | Foundational directives grounded |
| X:guiding:sufficiency | guiding | sufficiency | Authoritative Sufficiency Benchmark | 1 | HAS_ITEMS | Missing drainage design benchmark |
| X:guiding:completeness | guiding | completeness | Comprehensive Guidance Scope | 0 | NO_ITEMS | Guidance scope comprehensive |
| X:guiding:consistency | guiding | consistency | Uniform Guidance Integrity | 0 | NO_ITEMS | Guidance integrity uniform |
| X:applying:necessity | applying | necessity | Applied Essential Requirement | 1 | HAS_ITEMS | Compaction verification gap for embankment slopes |
| X:applying:sufficiency | applying | sufficiency | Practiced Capability Adequacy | 0 | NO_ITEMS | Capability adequacy practiced |
| X:applying:completeness | applying | completeness | Executed Implementation Scope | 1 | HAS_ITEMS | As-built survey scope not fully specified |
| X:applying:consistency | applying | consistency | Executed Practice Dependability | 0 | NO_ITEMS | Practice dependability consistent |
| X:judging:necessity | judging | necessity | Essential Adjudicative Criterion | 1 | HAS_ITEMS | Slope geometry verification criteria gap |
| X:judging:sufficiency | judging | sufficiency | Sufficient Adjudicative Ruling | 0 | NO_ITEMS | Adjudicative rulings sufficient |
| X:judging:completeness | judging | completeness | Exhaustive Adjudicative Scope | 0 | NO_ITEMS | Adjudicative scope adequate |
| X:judging:consistency | judging | consistency | Consistent Adjudicative Integrity | 0 | NO_ITEMS | Adjudicative integrity consistent |
| X:reviewing:necessity | reviewing | necessity | Essential Reassessment Criterion | 1 | HAS_ITEMS | No reassessment trigger for geotech report adequacy |
| X:reviewing:sufficiency | reviewing | sufficiency | Adequate Reassessment Verification | 0 | NO_ITEMS | Reassessment verification adequate |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Reassessment Scope | 0 | NO_ITEMS | Reassessment scope exhaustive |
| X:reviewing:consistency | reviewing | consistency | Uniform Reassessment Fidelity | 0 | NO_ITEMS | Reassessment fidelity uniform |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | MissingSlot | Guidance | Guidance | Add authoritative benchmark or design standard for drainage design (e.g., design storm return period, rainfall intensity-duration-frequency data for Penhold area) | No design storm event or IDF curve reference is provided in any document; the stormwater retention pond and drainage ditch must be sized to a standard but no benchmark is stated | Guidance.md; Specification.md | entire document scanned | -- | Civil Engineer / Municipal standards | TBD |
| X-002 | X:applying:necessity | VerificationGap | Specification | Specification | Add verification method for fill embankment slope compaction (REQ-3209 specifies 150 mm lifts at 98% SPDD but Verification table only says "Field inspection of fill slopes; geotechnical personnel observation" without referencing compaction testing) | REQ-3209 requires fill slopes to be placed in 150 mm lifts at 98% SPDD, but the Verification table entry for REQ-3209 references only "Field inspection" and "geotechnical personnel observation" without specifying compaction testing -- inconsistent with REQ-3205 verification approach | Specification.md | REQ-3209; Verification table > REQ-3209 | -- | Geotechnical Engineer | TBD |
| X-003 | X:applying:completeness | WeakStatement | Specification | Specification | Clarify as-built survey scope in Documentation table -- specify whether it includes stormwater pond geometry, drainage ditch as-built, and slope grades in addition to building contours | Documentation table lists "As-Built Topographic Survey: Final contours, building outline, service connections, finished floor elevations" per SOW-0113, but does not explicitly include stormwater pond, drainage ditch, or slope grades which are critical civil elements of this deliverable | Specification.md | Documentation > As-Built Topographic Survey | -- | Civil Engineer | TBD |
| X-004 | X:judging:necessity | Normalization | Multi | Multi | Normalize slope geometry expression across documents: Specification uses prose description ("3H:1V for slopes over 3.0 m"), Datasheet uses table format, Procedure uses mixed notation; align to consistent format | Cut slope and fill slope geometry is expressed differently across Specification (REQ-3208, REQ-3209), Datasheet (Excavation Cut Slopes table), and Procedure (Phase B-4 step 7); while values are consistent, the presentation format varies, risking misread in field application | Specification.md; Datasheet.md; Procedure.md | REQ-3208; REQ-3209; Excavation Cut Slopes table; Phase B-4 step 7 | -- | Civil Engineer | TBD |
| X-005 | X:reviewing:necessity | TBD_Question | Specification | Specification | Record TBD: Define trigger criteria for when the existing Geotech Report (USG1123, Feb 2021) is deemed "insufficient" and supplemental investigation is required | REQ-3214 states DB shall undertake additional investigation "if the existing Geotech Report is found insufficient" but no criteria define what constitutes insufficiency; this is an essential reassessment criterion needed for operational planning | Specification.md | REQ-3214 | -- | Geotechnical Engineer / Owner | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage (required)

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Binding Regulatory Foundation | 0 | NO_ITEMS | Regulatory foundation adequately binding |
| E:normative:sufficiency | normative | sufficiency | Prescribed Sufficiency Benchmark | 1 | HAS_ITEMS | Fill slope >6 m review gap |
| E:normative:completeness | normative | completeness | Total Regulatory Completeness | 0 | NO_ITEMS | Regulatory completeness adequate for available sources |
| E:normative:consistency | normative | consistency | Enforceable Regulatory Fidelity | 0 | NO_ITEMS | Regulatory fidelity enforceable |
| E:operative:necessity | operative | necessity | Critical Operational Foundation | 0 | NO_ITEMS | Operational foundation critical elements present |
| E:operative:sufficiency | operative | sufficiency | Sufficient Operational Competence | 0 | NO_ITEMS | Operational competence sufficient |
| E:operative:completeness | operative | completeness | Complete Operational Accounting | 1 | HAS_ITEMS | Spoil disposal accounting gap |
| E:operative:consistency | operative | consistency | Dependable Operational Consistency | 0 | NO_ITEMS | Operational consistency dependable |
| E:evaluative:necessity | evaluative | necessity | Fundamental Quality Grounding | 0 | NO_ITEMS | Quality grounding fundamental and present |
| E:evaluative:sufficiency | evaluative | sufficiency | Adequate Quality Standard | 0 | NO_ITEMS | Quality standards adequate |
| E:evaluative:completeness | evaluative | completeness | Comprehensive Quality Coverage | 1 | HAS_ITEMS | Cross-deliverable coordination gap |
| E:evaluative:consistency | evaluative | consistency | Consistent Quality Integrity | 0 | NO_ITEMS | Quality integrity consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:sufficiency | VerificationGap | Specification | Specification | Add verification trigger or process for fill slopes exceeding 6.0 m (REQ-3209 states review by qualified Geotechnical Engineer is required but no verification method is listed for this specific condition) | REQ-3209 includes a conditional requirement ("Fill slopes over 6.0 m in height require review by a qualified Geotechnical Engineer") but the Verification table entry for REQ-3209 does not address this conditional trigger; prescribed sufficiency benchmark is incomplete | Specification.md | REQ-3209; Verification table > REQ-3209 | -- | Geotechnical Engineer | TBD |
| E-002 | E:operative:completeness | MissingSlot | Procedure | Procedure | Add step or note for spoil disposal management (unsuitable excavated material, high-plastic clay, organics) -- where, how, and environmental requirements | Procedure Phase B-3 step 3 mentions "Dispose of unsuitable material (high-plastic clay, organics) off-site" but no procedural detail, record, or verification check exists for spoil disposal; this is a gap in complete operational accounting | Procedure.md | Phase B-3 step 3 | -- | Design-Builder / Environmental | TBD |
| E-003 | E:evaluative:completeness | Normalization | Multi | Guidance | Add cross-deliverable coordination note for sulphate resistance requirements shared with DEL-03-03 (aprons) and DEL-03-04 (utility structures) | Guidance mentions "This affects concrete specification across multiple PKG-003 deliverables and must be coordinated with DEL-03-03 and DEL-03-04" but no formal coordination mechanism or vocabulary note exists to ensure consistent quality coverage across deliverables | Guidance.md | Considerations > Sulphate attack on concrete | -- | Civil Engineer | TBD |
