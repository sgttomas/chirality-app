# Semantic Lensing Register: DEL-03-03 Pavements, Aggregate Yard Areas & Concrete Aprons

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/PKG-003_Site & Civil Works/1_Working/DEL-03-03_Pavements, Aggregate Yard Areas & Concrete Aprons/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-03-03, PKG-003 Site & Civil Works, Civil discipline
- _STATUS.md -- Current State: SEMANTIC_READY (2026-02-17)
- _SEMANTIC.md -- All 7 matrices (A, B, C, F, D, X, E) parsed successfully
- Datasheet.md -- Present and read
- Specification.md -- Present and read
- Guidance.md -- Present and read
- Procedure.md -- Present and read
- _REFERENCES.md -- Present and read (OSR and Geotechnical Investigation Report listed)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 22
- By document:
  - Datasheet: 4
  - Specification: 8
  - Guidance: 3
  - Procedure: 3
  - Multi: 4
- By matrix:
  - A: 5  B: 3  C: 3  F: 4  D: 2  X: 3  E: 2
- By type:
  - Conflict: 1
  - VerificationGap: 5
  - MissingSlot: 5
  - WeakStatement: 4
  - RationaleGap: 2
  - Normalization: 3
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4) -- Canonical

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Freeze-thaw class assumption not confirmed as prescriptive requirement |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Aggregate yard minimum depth TBD |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Concrete apron reinforcing verification gap |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit pathways covered adequately |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure provides adequate procedural direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Geofabric placement layer position unclear |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Compaction/density testing adequately covered |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | QA records and review process adequate |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Value orientation articulated in Guidance principles |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs section addresses merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 1 | HAS_ITEMS | Design life mismatch not addressed in Specification |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality appraisal covered in Procedure verification table |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify whether air-entrainment for freeze-thaw exposure is a mandatory requirement or assumption; confirm applicable freeze-thaw exposure class per CAN/CSA A23.1-2014 | REQ-03-03-08 includes air-entrainment as an ASSUMPTION but does not state it as a firm requirement with a specific exposure class. This could change the concrete mix design. | Specification.md | REQ-03-03-08 | -- | Specification.md | TBD |
| A-002 | A:normative:applying | TBD_Question | Datasheet | Datasheet | Record TBD: Aggregate yard minimum compacted thickness (currently TBD in Datasheet); confirm design depth based on heaviest equipment loading | The aggregate yard compacted thickness is listed as TBD in the Datasheet and stated as an ASSUMPTION (300 mm) in the Specification. This is a necessary design parameter that must be confirmed by the pavement designer. | Datasheet.md | Aggregate Yard Specification | -- | Pavement designer / Design-Builder | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add verification criteria for concrete apron structural design (slab thickness, reinforcing layout, joint spacing) -- currently only mix design is verified | The Specification verification table covers concrete mix design but not the structural adequacy of the apron slab itself. No acceptance criteria for slab thickness or reinforcing are specified. | Specification.md | Verification | -- | Specification.md | TBD |
| A-004 | A:operative:applying | Normalization | Multi | Guidance | Clarify geofabric placement position: Datasheet shows geofabric at bottom of cross-section (below SGSB), while Procedure Step B-2 states geofabric at "SGSB/Base interface" (above SGSB). Standardize terminology and layer position. | The geofabric placement description is inconsistent between documents. The Datasheet cross-section tables list geotextile as the bottom layer, while Procedure Step B-2 line 5 places it at the SGSB/Base interface. This affects field execution. | Datasheet.md, Procedure.md | Pavement Cross-Section tables; Step B-2 | Datasheet.md#Pavement Cross-Section: Light Duty, Procedure.md#Step B-2 | Geotechnical engineer | TBD |
| A-005 | A:evaluative:judging | MissingSlot | Specification | Guidance | Add design life expectations and maintenance cycle acknowledgment for pavement surfaces (Guidance discusses 15-20 year resurfacing but Specification has no corresponding requirement) | Guidance notes pavement maintenance cycles (15-20 year resurfacing) and asks whether design accommodates future lifts, but neither Specification nor Datasheet record design life for pavements. This is a value/worth gap -- the facility has a 50-year design life but pavement design life is unstated. | Guidance.md, Specification.md | Design Life Alignment; entire Specification scanned | -- | Specification.md | TBD |

---

## Matrix B -- Conceptualization (4x4) -- Canonical

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Apron dimensions TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Geotech report provides adequate evidence base |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Industrial/Collector cross-section in Datasheet but not clearly mapped to a zone |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurement units and values consistent across documents |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (loading, frost, sulphate) adequately communicated |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context provided in Guidance principles |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Account of surfacing zones comprehensive |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Compaction standard inconsistency for aggregate yard |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding of subgrade and design method well-established |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Design expertise requirements stated |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Mastery of pavement design adequately demonstrated |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Consistent understanding across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Key trade-offs and judgments documented |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-off section provides adequate judgment context |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view of surfacing system provided |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning consistent with load-matching philosophy |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Concrete apron dimensions per door location (currently TBD in Datasheet); requires architectural overhead door locations and vehicle swept path analysis | Apron dimensions are listed as TBD in the Datasheet. This is an essential design fact that cannot be resolved until architectural door locations are confirmed. | Datasheet.md | Concrete Apron Specification | -- | Architectural drawings / Design-Builder | TBD |
| B-002 | B:data:completeness | WeakStatement | Datasheet | Datasheet | Clarify applicability of Industrial/Collector Route (2,000,000 ESALs) cross-section: this section appears in the Datasheet but no zone is assigned to it; clarify that it is a conditional fallback for Zone A if ESAL analysis exceeds 800,000 | The Datasheet includes a third pavement cross-section (2M ESALs) that is not mapped to any zone in the Surfacing Zone Summary. The Specification REQ-03-03-04 Note explains the conditional use but the Datasheet does not. | Datasheet.md | Pavement Cross-Section: Industrial/Collector Route | -- | Datasheet.md | TBD |
| B-003 | B:information:consistency | Conflict | Multi | Multi | Resolve aggregate yard compaction standard: Specification REQ-03-03-05 states 98% SPDD; Procedure Step B-4 also states 98% SPDD; however Datasheet Compaction Standards table shows subgrade at 98% but does not separately list aggregate yard compaction. Confirm that aggregate yard compaction is 98% SPDD (not 100% as for structural layers) and add explicit entry to Datasheet Compaction Standards table. | The Datasheet Compaction Standards table lists subgrade at 98% and SGSB/Base at 100%, but does not have a separate row for aggregate yard compaction. The Specification and Procedure agree on 98% for aggregate. The Datasheet omission could lead to the 100% standard being applied by default. | Datasheet.md, Specification.md, Procedure.md | Compaction Standards (Datasheet); REQ-03-03-05 (Spec); Step B-4 (Procedure) | Datasheet.md#Compaction Standards, Specification.md#REQ-03-03-05 | Specification.md | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | enforceable regulatory basis | 1 | HAS_ITEMS | Alberta Building Code not confirmed as applicable |
| C:normative:sufficiency | normative | sufficiency | substantiated compliance warrant | 0 | NO_ITEMS | Compliance substantiation adequate via Geotech Report |
| C:normative:completeness | normative | completeness | exhaustive regulatory coverage | 1 | HAS_ITEMS | Missing standard for HMA material specification |
| C:normative:consistency | normative | consistency | harmonized regulatory standard | 0 | NO_ITEMS | Standards references consistent |
| C:operative:necessity | operative | necessity | essential operational threshold | 0 | NO_ITEMS | Operational thresholds (compaction, density) well-defined |
| C:operative:sufficiency | operative | sufficiency | proven operational competence | 0 | NO_ITEMS | Competence requirements stated |
| C:operative:completeness | operative | completeness | thorough operational coverage | 1 | HAS_ITEMS | Testing frequency not specified in Specification |
| C:operative:consistency | operative | consistency | standardized operational discipline | 0 | NO_ITEMS | Operational discipline consistent across docs |
| C:evaluative:necessity | evaluative | necessity | foundational merit criterion | 0 | NO_ITEMS | Merit criteria established in Guidance principles |
| C:evaluative:sufficiency | evaluative | sufficiency | defensible value appraisal | 0 | NO_ITEMS | Value appraisal in trade-offs section |
| C:evaluative:completeness | evaluative | completeness | comprehensive worth assessment | 0 | NO_ITEMS | Worth assessment adequate |
| C:evaluative:consistency | evaluative | consistency | principled value coherence | 0 | NO_ITEMS | Value reasoning coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Clarify Alberta Building Code applicability: Standards table lists "Alberta Building Code (current edition)" with "location TBD" and "General site construction" but no specific sections cited. Either confirm specific applicable sections or remove if not directly applicable to paving. | The Alberta Building Code is listed as a standard but with no specific sections or requirements tied to it. This weakens the enforceable regulatory basis -- it is unclear what obligation it creates for this deliverable. | Specification.md | Standards | -- | Specification.md | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add HMA material specification standard (e.g., Alberta Transportation specifications for HMAC, or City of Red Deer paving specification) to Standards table; currently no standard governs HMA mix design or material properties | The Specification requires HMAC surface courses but references no material specification standard for the asphalt mix itself. Only the compaction testing standard (Marshall Method) is referenced. The HMA mix design standard is absent. | Specification.md | Standards | -- | Specification.md | TBD |
| C-003 | C:operative:completeness | VerificationGap | Procedure | Specification | Add compaction testing frequency requirements to Specification (Procedure uses ASSUMPTIONs: 1 test per 500 m2 per lift for SGSB, 1 per 1000 m3 for aggregate); these frequencies need to be established as requirements | The Procedure includes compaction testing frequencies but marks them as ASSUMPTIONs. No testing frequency is specified in the Specification. Without specified frequencies, the testing regime is indeterminate. | Procedure.md, Specification.md | Step B-2, Step B-4; Verification table (Spec) | -- | Specification.md | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | authenticated regulatory mandate | 1 | HAS_ITEMS | CAN/CSA A23.1 not directly accessed |
| F:normative:sufficiency | normative | sufficiency | warranted regulatory authority | 0 | NO_ITEMS | Regulatory authority adequately warranted via Geotech Report |
| F:normative:completeness | normative | completeness | exhaustive compliance dominion | 1 | HAS_ITEMS | Transition zone requirements missing |
| F:normative:consistency | normative | consistency | coherent regulatory alignment | 0 | NO_ITEMS | Regulatory references internally consistent |
| F:operative:necessity | operative | necessity | confirmed functional foundation | 0 | NO_ITEMS | Functional foundations confirmed |
| F:operative:sufficiency | operative | sufficiency | demonstrated process proficiency | 0 | NO_ITEMS | Process proficiency adequately demonstrated |
| F:operative:completeness | operative | completeness | exhaustive procedural command | 1 | HAS_ITEMS | Cold weather paving restrictions missing |
| F:operative:consistency | operative | consistency | disciplined performance coherence | 0 | NO_ITEMS | Performance coherence maintained |
| F:evaluative:necessity | evaluative | necessity | foundational quality imperative | 1 | HAS_ITEMS | No quality requirement for surface smoothness/ride quality |
| F:evaluative:sufficiency | evaluative | sufficiency | warranted quality justification | 0 | NO_ITEMS | Quality justification adequate |
| F:evaluative:completeness | evaluative | completeness | exhaustive quality dominion | 0 | NO_ITEMS | Quality domain adequately covered for current scope |
| F:evaluative:consistency | evaluative | consistency | harmonized quality coherence | 0 | NO_ITEMS | Quality standards coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | RationaleGap | Specification | Guidance | Add rationale note in Guidance explaining that CAN/CSA A23.1-2014 is referenced via the Geotechnical Investigation Report but the full standard text has not been directly accessed; note implications for verifying freeze-thaw and sulphate class requirements | The Specification and Datasheet reference CAN/CSA A23.1-2014 but note "direct access TBD." The requirement is derived from the Geotech Report's interpretation. Without direct standard access, the regulatory mandate is authenticated only second-hand. | Specification.md, Datasheet.md | REQ-03-03-08; Standards; References | -- | Guidance.md | TBD |
| F-002 | F:normative:completeness | MissingSlot | Specification | Specification | Add requirement for transition zone design between surfacing types (e.g., Zone A to Zone C, Zone B to Zone D) addressing edge support, differential settlement, and drainage at transitions | Guidance mentions transition zones as a consideration but no requirement exists in the Specification. Transition zone failure is a common pavement deficiency mode that should be addressed prescriptively. | Specification.md, Guidance.md | entire Specification scanned; Guidance Considerations: Transition Zones | -- | Specification.md | TBD |
| F-003 | F:operative:completeness | MissingSlot | Procedure | Procedure | Add cold weather paving restrictions/requirements for HMA placement (minimum ambient and surface temperature thresholds); Procedure Step B-5 addresses cold weather concrete but Step B-6 (HMA) does not | The Procedure addresses cold weather concrete protection but omits temperature restrictions for HMA paving. Paving below minimum temperatures results in inadequate compaction and premature failure. | Procedure.md | Step B-6 | -- | Procedure.md | TBD |
| F-004 | F:evaluative:necessity | MissingSlot | Specification | Specification | Add surface finish/smoothness requirement for asphalt pavements (e.g., straightedge tolerance or IRI requirement for Zone A fire apparatus routing where emergency vehicle ride quality matters) | No surface smoothness or ride quality acceptance criterion is specified for HMA pavements. For fire apparatus routing (Zone A), surface quality affects emergency response vehicle handling. | Specification.md | entire Specification scanned | -- | Specification.md | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | authoritative rule governance | 0 | NO_ITEMS | Rule governance adequately established |
| D:normative:applying | normative | applying | enforced compliance practice | 0 | NO_ITEMS | Compliance practices enforced through requirements |
| D:normative:judging | normative | judging | binding conformance judgment | 1 | HAS_ITEMS | Geotechnical engineer sign-off scope unclear |
| D:normative:reviewing | normative | reviewing | systematic compliance integrity | 0 | NO_ITEMS | Compliance review processes adequate |
| D:operative:guiding | operative | guiding | grounded method governance | 0 | NO_ITEMS | Method governance well-grounded in Procedure |
| D:operative:applying | operative | applying | confirmed task delivery | 0 | NO_ITEMS | Task delivery steps comprehensive |
| D:operative:judging | operative | judging | resolved operational fitness | 0 | NO_ITEMS | Operational fitness criteria defined |
| D:operative:reviewing | operative | reviewing | systematic operational rigor | 0 | NO_ITEMS | Operational rigor maintained through verification table |
| D:evaluative:guiding | evaluative | guiding | grounded merit governance | 0 | NO_ITEMS | Merit governance grounded in Guidance principles |
| D:evaluative:applying | evaluative | applying | confirmed value realization | 1 | HAS_ITEMS | No as-built survey requirement for aggregate yard depth |
| D:evaluative:judging | evaluative | judging | definitive value judgment | 0 | NO_ITEMS | Value judgment criteria present |
| D:evaluative:reviewing | evaluative | reviewing | systematic value integrity | 0 | NO_ITEMS | Value integrity maintained through records |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:judging | WeakStatement | Procedure | Procedure | Clarify scope of geotechnical engineer sign-off: Step B-1 requires sign-off before SGSB placement, but it is unclear whether the geotechnical engineer must also sign off on SGSB compaction, base course compaction, and aggregate yard preparation before subsequent layers | The Procedure requires geotechnical sign-off for subgrade but does not state whether subsequent layers also require geotechnical inspection/approval. The binding conformance judgment scope is ambiguous. | Procedure.md | Step B-1, Step B-2 | -- | Procedure.md | TBD |
| D-002 | D:evaluative:applying | VerificationGap | Specification | Specification | Add verification method for aggregate yard compacted depth (e.g., test pit or survey confirmation of finished aggregate thickness vs. design thickness) | The Specification requires aggregate depth per design report but the Verification table has no method to confirm the as-built aggregate thickness. Only gradation and compaction are verified, not depth. | Specification.md | Verification table, REQ-03-03-05 | -- | Specification.md | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | authoritative foundational mandate | 0 | NO_ITEMS | Foundational mandates well-established |
| X:guiding:sufficiency | guiding | sufficiency | substantiated guidance authority | 0 | NO_ITEMS | Guidance authority substantiated |
| X:guiding:completeness | guiding | completeness | holistic governance coverage | 0 | NO_ITEMS | Governance coverage adequate |
| X:guiding:consistency | guiding | consistency | principled governance discipline | 0 | NO_ITEMS | Governance discipline consistent |
| X:applying:necessity | applying | necessity | mandatory delivery foundation | 1 | HAS_ITEMS | Prerequisite tracking gap |
| X:applying:sufficiency | applying | sufficiency | justified execution sufficiency | 0 | NO_ITEMS | Execution sufficiency justified |
| X:applying:completeness | applying | completeness | comprehensive execution coverage | 0 | NO_ITEMS | Execution coverage comprehensive |
| X:applying:consistency | applying | consistency | reliable execution discipline | 0 | NO_ITEMS | Execution discipline reliable |
| X:judging:necessity | judging | necessity | definitive fitness benchmark | 1 | HAS_ITEMS | HMA thickness verification gap |
| X:judging:sufficiency | judging | sufficiency | substantiated adequacy verdict | 0 | NO_ITEMS | Adequacy verdicts substantiated |
| X:judging:completeness | judging | completeness | exhaustive capability verdict | 0 | NO_ITEMS | Capability verdicts adequate |
| X:judging:consistency | judging | consistency | consistent capability judgment | 0 | NO_ITEMS | Capability judgments consistent |
| X:reviewing:necessity | reviewing | necessity | fundamental audit threshold | 1 | HAS_ITEMS | No hold point defined for paving operations |
| X:reviewing:sufficiency | reviewing | sufficiency | substantiated inspection rigor | 0 | NO_ITEMS | Inspection rigor substantiated |
| X:reviewing:completeness | reviewing | completeness | exhaustive integrity examination | 0 | NO_ITEMS | Integrity examination adequate |
| X:reviewing:consistency | reviewing | consistency | harmonized inspection discipline | 0 | NO_ITEMS | Inspection discipline harmonized |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | Normalization | Procedure | Procedure | Standardize prerequisite reference: Procedure lists "PKG-004 or equivalent" for architectural overhead door locations but _CONTEXT.md shows cold storage is in PKG-004; clarify whether overhead door locations come from PKG-002 (PSB architectural) and/or PKG-004 (cold storage) | The Procedure prerequisite table references "PKG-004 or equivalent" for overhead door locations. This is ambiguous -- the PSB architectural deliverables are in PKG-002 while PKG-004 is cold storage. The prerequisite source should be precise. | Procedure.md | Design Phase Prerequisites | -- | Procedure.md | TBD |
| X-002 | X:judging:necessity | VerificationGap | Specification | Specification | Add field verification method for HMA layer thickness (e.g., core sampling after paving to confirm 75 mm or 100 mm thickness achieved); current verification references "field measurement during construction" but does not specify how thickness is verified after placement | The Specification Verification table for REQ-03-03-03/04 states "field measurement during construction" but does not specify how HMAC thickness is verified after paving. Core sampling or other post-paving thickness verification should be specified. | Specification.md | Verification table, REQ-03-03-03/04 | -- | Specification.md | TBD |
| X-003 | X:reviewing:necessity | RationaleGap | Procedure | Guidance | Add rationale for hold points in construction sequence: Procedure defines geotechnical sign-off as a hold point after proof rolling (Step B-1) but does not explicitly designate other hold points (e.g., before HMA paving, before concrete pour). Clarify which steps are mandatory hold points vs. inspection points. | The distinction between mandatory hold points and routine inspection points is not articulated. Only Step B-1 geotechnical sign-off is clearly a hold point. For concrete pours and HMA paving, it is unclear whether work can proceed without explicit approval. | Procedure.md | Steps B-1 through B-6 | -- | Guidance.md | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | definitive regulatory obligation | 0 | NO_ITEMS | Regulatory obligations definitively stated |
| E:normative:sufficiency | normative | sufficiency | proven regulatory sufficiency | 0 | NO_ITEMS | Regulatory sufficiency proven through standards |
| E:normative:completeness | normative | completeness | exhaustive regulatory jurisdiction | 1 | HAS_ITEMS | Drainage interface gap |
| E:normative:consistency | normative | consistency | stable regulatory governance | 0 | NO_ITEMS | Regulatory governance stable |
| E:operative:necessity | operative | necessity | established operational obligation | 0 | NO_ITEMS | Operational obligations established |
| E:operative:sufficiency | operative | sufficiency | verified operational adequacy | 0 | NO_ITEMS | Operational adequacy verified through procedures |
| E:operative:completeness | operative | completeness | comprehensive operational jurisdiction | 1 | HAS_ITEMS | Coordination with site grading deliverable |
| E:operative:consistency | operative | consistency | disciplined operational consistency | 0 | NO_ITEMS | Operational consistency maintained |
| E:evaluative:necessity | evaluative | necessity | foundational value obligation | 0 | NO_ITEMS | Value obligations founded |
| E:evaluative:sufficiency | evaluative | sufficiency | justified merit sufficiency | 0 | NO_ITEMS | Merit sufficiency justified |
| E:evaluative:completeness | evaluative | completeness | comprehensive value jurisdiction | 0 | NO_ITEMS | Value jurisdiction comprehensive |
| E:evaluative:consistency | evaluative | consistency | disciplined value governance | 0 | NO_ITEMS | Value governance disciplined |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:completeness | VerificationGap | Specification | Specification | Add verification method for drainage cross-slope compliance at pavement-to-drainage-infrastructure interface (REQ-03-03-11 requires runoff to drainage infrastructure but verification only checks minimum 2% slope, not that drainage actually reaches infrastructure) | REQ-03-03-11 requires runoff to be "directed to site drainage infrastructure" but the verification method only checks cross slope magnitude, not the drainage path connectivity. The regulatory jurisdiction of this requirement extends to the drainage connection but verification does not. | Specification.md | Verification table, REQ-03-03-11 | -- | Specification.md | TBD |
| E-002 | E:operative:completeness | Normalization | Multi | Guidance | Clarify coordination interface with DEL-03-02 (Grading, Earthworks, Drainage & Stormwater): Procedure prerequisites reference "site grading deliverable" and REQ-03-03-11 references "site drainage infrastructure" but the specific deliverable ID (DEL-03-02) is not cited. Standardize cross-references. | Multiple documents reference the site grading/drainage deliverable generically rather than by its deliverable ID (DEL-03-02). This creates a normalization risk where the interface is not precisely traceable. | Specification.md, Procedure.md | REQ-03-03-11; Design Phase Prerequisites | -- | Multi | TBD |
