# Semantic Lensing Register: DEL-006-01 Preliminary Plumbing Design

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-006_Plumbing Design/1_Working/DEL-006-01_Preliminary-Design/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-006-01_Preliminary-Design/_CONTEXT.md (Deliverable identity, description, anticipated artifacts)
- _STATUS.md — DEL-006-01_Preliminary-Design/_STATUS.md (Status: SEMANTIC_READY, 2026-02-26)
- _SEMANTIC.md — DEL-006-01_Preliminary-Design/_SEMANTIC.md (Matrices A, B, C, F, D, X, E parsed)
- Datasheet.md — DEL-006-01_Preliminary-Design/Datasheet.md (Attributes, conditions, construction items, references)
- Specification.md — DEL-006-01_Preliminary-Design/Specification.md (Scope, REQ-001 through REQ-017, standards, verification)
- Guidance.md — DEL-006-01_Preliminary-Design/Guidance.md (Purpose, principles, considerations, trade-offs)
- Procedure.md — DEL-006-01_Preliminary-Design/Procedure.md (Steps 1-8, prerequisites, verification, records)
- _REFERENCES.md — DEL-006-01_Preliminary-Design/_REFERENCES.md (R-01, R-06, SOW-0010f, OBJ-003, OBJ-004)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 26
- By document:
  - Datasheet: 2
  - Specification: 13
  - Guidance: 6
  - Procedure: 2
  - Multi: 3
- By matrix:
  - A: 5  B: 3  C: 4  F: 5  D: 2  X: 4  E: 3
- By type:
  - Conflict: 1
  - VerificationGap: 5
  - MissingSlot: 6
  - WeakStatement: 4
  - RationaleGap: 4
  - Normalization: 2
  - TBD_Question: 4
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Code edition TBD weakens prescriptive direction |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Laundry connection stated as ASSUMPTION |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Code edition unknown prevents compliance determination |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit pathway adequately addressed via REQ-015/REQ-016 and Procedure Step 8 |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Steps 1-8 provide adequate procedural direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Hot water supply strategy absent |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification tables in Specification and Procedure cover performance assessment |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records section in Procedure provides audit trail |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | Cistern sizing adequacy not resolved |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs table in Guidance addresses merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Covered by verification and trade-off analysis |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality appraisal pathway present via County approval gate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify which edition of Alberta Building Code and National Plumbing Code of Canada governs this design; currently stated as "specific edition TBD" | The prescriptive direction for this deliverable is undermined when the governing code edition is unidentified; implementation decisions (pipe sizing, fixture spacing, vent requirements) depend on the specific edition. | Specification.md | Standards table; REQ-015 | -- | Plumbing Engineer to confirm at project kickoff | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Confirm whether laundry connection in new locker/change room is a contract requirement or an assumption; currently tagged "(ASSUMPTION)" in Datasheet and inferred in REQ-013 | REQ-013 includes laundry services but the RFP basis for laundry plumbing is labelled as an assumption. If the assumption is wrong, mandatory practice changes. | Datasheet.md, Specification.md | Datasheet > Renovation -- Old North Shop Plumbing; Specification > REQ-013 | -- | County or RFP addendum | TBD |
| A-003 | A:normative:judging | TBD_Question | Specification | Specification | Record TBD: Identify the applicable edition of Alberta Safety Codes (plumbing) and NPC to enable compliance determination at preliminary stage | Without the specific code edition, compliance determination cannot be completed. Procedure Step 5 references "applicable code -- TBD" for emergency shower travel distance. | Specification.md, Procedure.md | Specification > Standards table; Procedure > Step 5 item 1 | -- | Plumbing Engineer / Alberta Safety Codes authority | TBD |
| A-004 | A:operative:applying | MissingSlot | Multi | Guidance | Add consideration for hot water supply strategy (source, heating method, distribution) -- currently absent from all four documents despite fixtures requiring hot water (wash station, washroom, kitchenette, laundry) | Practical execution of plumbing design requires knowing whether hot water is provided (electric, gas, or other), yet no document addresses hot water generation or distribution. Multiple fixtures implicitly require it. | Datasheet.md, Specification.md, Guidance.md, Procedure.md | entire document scanned | -- | Plumbing Engineer | TBD |
| A-005 | A:evaluative:guiding | RationaleGap | Guidance | Guidance | Add rationale for accepting the 50,000 L cistern minimum without demand analysis; Guidance notes the gap but does not state whether preliminary design should proceed on the Owner's minimum or require analysis first | Guidance > Considerations > Cistern Sizing Adequacy raises the question but does not resolve the design direction for the preliminary stage. A value orientation is needed: accept the Owner minimum or flag it as a risk. | Guidance.md | Considerations > Cistern Sizing Adequacy | -- | Plumbing Engineer / Owner | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Existing plumbing condition unknown |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet evidence base is adequate for available sources |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Floor drain count incomplete |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurements are consistently sourced from R-01/R-06 |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (cistern-fed, off-grid, separated drainage) are present |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context is adequately provided across documents |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Document set provides comprehensive account of plumbing scope |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology drift on "wash station" vs "wash sink" |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding of cistern-fed off-grid plumbing is present in Guidance |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise requirements are addressed via P.Eng. stamp requirement |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Coverage is appropriate for preliminary design stage |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs table in Guidance provides discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment calls are documented with TBD where needed |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic coverage is adequate for preliminary stage |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Multi | Datasheet | Record TBD: Document existing plumbing rough-in condition in Old North Shop (what exists, what can be reused) -- currently unknown from available sources | Essential facts about the existing plumbing infrastructure are missing. Guidance notes "Existing plumbing condition: TBD (not documented in available sources)" but Datasheet does not record this gap. Renovation scope (REQ-013, REQ-014) depends on this data. | Guidance.md, Datasheet.md | Guidance > Considerations > Old North Shop Renovation Plumbing Scope; Datasheet > Renovation -- Old North Shop Plumbing | -- | Site survey / existing conditions assessment | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add floor drain count and locations for Old North Shop renovation areas (washroom, kitchenette, laundry) to Datasheet -- currently only new Addition floor drains are enumerated | Datasheet lists floor drain locations for Repair Bay 1, Repair Bay 2, and Wash Bay (from R-06) but does not enumerate drains for the renovation areas, which are also in scope per REQ-013/REQ-014. | Datasheet.md | Plumbing Systems -- Drainage | -- | R-06 review / Plumbing Engineer | TBD |
| B-003 | B:information:consistency | Normalization | Multi | Guidance | Normalize terminology: "industrial wash sink" vs "wash station" vs "industrial wash station (wash sink)" -- three variant terms used across documents for the same fixture | Datasheet uses "Industrial wash station (wash sink)", Specification uses "Industrial Wash Sink (Wash Station)", Guidance uses "wash station" only. Inconsistency risks drift in procurement and coordination. | Datasheet.md, Specification.md, Guidance.md | Datasheet > Plumbing Fixtures and Safety Equipment; Specification > REQ-012; Guidance > Examples | -- | Establish single term in Guidance, apply consistently | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Regulatory Threshold Awareness | 1 | HAS_ITEMS | Regulatory threshold unknown due to code edition TBD |
| C:normative:sufficiency | normative | sufficiency | Compliance Justification Capacity | 1 | HAS_ITEMS | Justification capacity limited without code edition |
| C:normative:completeness | normative | completeness | Total Obligation Coverage | 0 | NO_ITEMS | REQ-001 through REQ-017 provide comprehensive obligation coverage |
| C:normative:consistency | normative | consistency | Harmonized Regulatory Coherence | 0 | NO_ITEMS | Regulatory references are internally consistent |
| C:operative:necessity | operative | necessity | Functional Process Foundation | 1 | HAS_ITEMS | Freeze protection strategy absent from Specification |
| C:operative:sufficiency | operative | sufficiency | Contextual Performance Adequacy | 0 | NO_ITEMS | Performance context is adequate for preliminary stage |
| C:operative:completeness | operative | completeness | Comprehensive Operational Scope | 0 | NO_ITEMS | Procedure Steps 1-8 cover operational scope comprehensively |
| C:operative:consistency | operative | consistency | Stable Operational Coherence | 0 | NO_ITEMS | Operational coherence is stable across documents |
| C:evaluative:necessity | evaluative | necessity | Inherent Value Recognition | 0 | NO_ITEMS | Value proposition (County approval gate, coordination instrument) is recognized |
| C:evaluative:sufficiency | evaluative | sufficiency | Credible Worth Assessment | 1 | HAS_ITEMS | Emergency shower tempering trade-off unresolved |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Merit Accounting | 0 | NO_ITEMS | Merit accounting is comprehensive for preliminary stage |
| C:evaluative:consistency | evaluative | consistency | Principled Value Consistency | 0 | NO_ITEMS | Value reasoning is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | TBD_Question | Specification | Specification | Record TBD: Confirm whether ANSI Z358.1 (emergency shower standard) applies in Alberta jurisdiction and which edition, as this establishes the regulatory threshold for emergency shower design | Guidance references ANSI Z358.1 requirements but Specification does not list it in the Standards table. The regulatory threshold for emergency shower travel distance and tempering cannot be determined without this. | Specification.md, Guidance.md | Specification > Standards table; Guidance > Principle 3 | -- | Plumbing Engineer / Alberta OHS regulations | TBD |
| C-002 | C:normative:sufficiency | VerificationGap | Specification | Specification | Add verification approach for freeze protection provisions (REQ not currently present; Guidance identifies this as a consideration but no corresponding requirement exists) | Compliance justification for exterior plumbing (cistern fill, bulk water fill, mud sump connection) in Alberta climate cannot be demonstrated without a freeze protection requirement and its verification. Guidance > Considerations > Freeze Protection identifies the issue. | Specification.md, Guidance.md | Specification > Requirements (none present); Guidance > Considerations > Freeze Protection in Alberta Climate | -- | Plumbing Engineer | TBD |
| C-003 | C:operative:necessity | MissingSlot | Specification | Specification | Add a requirement for freeze protection strategy for exterior and exposed plumbing (cistern filling connection, bulk water fill, mud sump connection) | Functional Process Foundation requires addressing freeze protection as a core process element for an Alberta site. Guidance identifies it as a consideration, Procedure Step 2 item 5 references it, but no Specification requirement exists. | Specification.md | Requirements section (absent) | -- | Plumbing Engineer | TBD |
| C-004 | C:evaluative:sufficiency | RationaleGap | Guidance | Guidance | Add rationale for emergency shower tempering decision -- Trade-offs table lists it as "TBD" but does not provide enough context for the preliminary design to proceed or defer | The credible worth assessment of the emergency shower design depends on whether tempering is required. The trade-off is listed but unresolved, and the basis (NPC/ANSI Z358.1 in Alberta) is not established. | Guidance.md | Trade-offs table > Emergency shower tempering | -- | Plumbing Engineer / Code review | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandatory Conformance Baseline | 1 | HAS_ITEMS | Septic scope conflict |
| F:normative:sufficiency | normative | sufficiency | Demonstrated Compliance Rationale | 1 | HAS_ITEMS | REQ-017 verification is assumption-tagged |
| F:normative:completeness | normative | completeness | Exhaustive Regulatory Command | 0 | NO_ITEMS | Requirements REQ-001 through REQ-017 are comprehensive |
| F:normative:consistency | normative | consistency | Grounded Compliance Uniformity | 1 | HAS_ITEMS | Guarantee period not reflected in Specification |
| F:operative:necessity | operative | necessity | Critical Functional Awareness | 0 | NO_ITEMS | Procedure prerequisites identify all critical upstream inputs |
| F:operative:sufficiency | operative | sufficiency | Competent Execution Justification | 0 | NO_ITEMS | Execution pathway is justified |
| F:operative:completeness | operative | completeness | Total Implementation Accounting | 1 | HAS_ITEMS | Drain venting absent from Specification requirements |
| F:operative:consistency | operative | consistency | Principled Operational Stability | 0 | NO_ITEMS | Operational consistency is maintained |
| F:evaluative:necessity | evaluative | necessity | Fundamental Merit Awareness | 0 | NO_ITEMS | Value drivers are identified |
| F:evaluative:sufficiency | evaluative | sufficiency | Balanced Appraisal Competence | 0 | NO_ITEMS | Trade-off analysis provides balanced appraisal |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Worth Inventory | 1 | HAS_ITEMS | Pressure washer supply decision unresolved |
| F:evaluative:consistency | evaluative | consistency | Coherent Appraisal Integrity | 0 | NO_ITEMS | Appraisal is coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | Conflict | Specification | NA | Clarify scope of existing septic tank: RFP uses "potentially removal and relocate" while Decomposition records relocation as OUT of scope (D-002). Guidance CF-001 already surfaces this but Specification REQ-006 adopts the Decomposition position without noting the conflict. | Mandatory conformance baseline is contested: the RFP parenthetical is ambiguous about whether relocation is required. REQ-006 assumes removal-only but a County ruling is needed. | Specification.md, Guidance.md | Specification > REQ-006; Guidance > Conflict Table CF-001 | Specification.md#REQ-006 (removal only), Guidance.md#CF-001 (RFP ambiguity noted) | Decomposition D-002 decision preferred per Guidance CF-001 | TBD |
| F-002 | F:normative:sufficiency | VerificationGap | Specification | Specification | Strengthen REQ-017 verification: currently "(ASSUMPTION)" tagged -- replace with a defined verification method (e.g., coordination meeting minutes, clash-check record) | Demonstrated compliance rationale for interdisciplinary coordination is weak because the verification approach is assumption-tagged. A concrete verification method is needed. | Specification.md | REQ-017 verification clause | -- | Project Manager / Plumbing Engineer | TBD |
| F-003 | F:normative:consistency | MissingSlot | Specification | Specification | Add reference to the 2-year guarantee period (construction + 2 years post-CCC) in Specification scope or standards section -- currently in Datasheet only | Datasheet records the guarantee period from R-01 section 2.10, but Specification does not reference it. This is a contractual obligation that affects material selection at preliminary stage. | Datasheet.md, Specification.md | Datasheet > Conditions; Specification > entire document scanned | -- | Contract / R-01 section 2.10 | TBD |
| F-004 | F:operative:completeness | MissingSlot | Specification | Specification | Add a requirement for drain venting per applicable plumbing code -- Procedure Step 3 item 6 references "Design drain venting per applicable plumbing code (TBD)" but no corresponding requirement exists in Specification | Total Implementation Accounting requires that drain venting be tracked as a requirement, not just a procedure step. Without a Specification requirement, there is no verification target. | Specification.md, Procedure.md | Specification > Requirements (absent); Procedure > Step 3 item 6 | -- | Plumbing Engineer / NPC | TBD |
| F-005 | F:evaluative:completeness | RationaleGap | Guidance | Guidance | Add rationale for pressure washer supply decision (cistern-fed direct vs dedicated pressure booster) -- Trade-offs table lists "TBD" with minimal basis for choosing | Exhaustive worth inventory requires that this trade-off be resolved or explicitly deferred with documented reasoning. The current entry provides insufficient basis for engineering decision. | Guidance.md | Trade-offs table > Pressure washer supply | -- | Plumbing Engineer | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Established Regulatory Course | 0 | NO_ITEMS | Regulatory course is established via code references and County approval gate |
| D:normative:applying | normative | applying | Settled Obligation Enactment | 0 | NO_ITEMS | Obligations are enacted through REQ-001 to REQ-017 |
| D:normative:judging | normative | judging | Definitive Conformance Ruling | 0 | NO_ITEMS | Conformance ruling pathway exists via County approval and verification table |
| D:normative:reviewing | normative | reviewing | Settled Compliance Assurance | 0 | NO_ITEMS | Compliance assurance addressed through verification and records |
| D:operative:guiding | operative | guiding | Settled Operational Guidance | 1 | HAS_ITEMS | Dependencies status not tracked |
| D:operative:applying | operative | applying | Resolved Capability Deployment | 0 | NO_ITEMS | Capability deployment is resolved through procedure steps |
| D:operative:judging | operative | judging | Settled Delivery Verdict | 0 | NO_ITEMS | Delivery verdict mechanism exists via verification checks |
| D:operative:reviewing | operative | reviewing | Settled Process Inspection | 0 | NO_ITEMS | Process inspection addressed via records section |
| D:evaluative:guiding | evaluative | guiding | Settled Quality Direction | 1 | HAS_ITEMS | Mud sump gravity drainage assumption unverified |
| D:evaluative:applying | evaluative | applying | Resolved Quality Enactment | 0 | NO_ITEMS | Quality enactment pathways are present |
| D:evaluative:judging | evaluative | judging | Definitive Value Appraisal | 0 | NO_ITEMS | Value appraisal is addressed through trade-offs and verification |
| D:evaluative:reviewing | evaluative | reviewing | Settled Quality Assurance | 0 | NO_ITEMS | Quality assurance pathway present via County approval |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:operative:guiding | WeakStatement | Procedure | Procedure | Strengthen upstream dependency status: Procedure notes "_DEPENDENCIES.md currently has status NOT_TRACKED" and dependencies are "(ASSUMPTION: these are the logical sequencing dependencies)" -- clarify which dependencies are confirmed vs assumed | Settled Operational Guidance requires that the sequencing of upstream deliverables be confirmed, not assumed. The current formulation leaves the critical path uncertain. | Procedure.md | Prerequisites > Upstream Inputs > Note | -- | Project Manager | TBD |
| D-002 | D:evaluative:guiding | WeakStatement | Guidance | Guidance | Clarify whether gravity drainage for mud sump is confirmed feasible or assumed; currently stated as "ASSUMPTION -- gravity feasibility subject to floor elevation and sump depth" | Settled Quality Direction for the drainage system depends on whether gravity drainage to the mud sump is achievable. This assumption affects structural and civil coordination. | Guidance.md | Trade-offs table > Mud sump drainage | -- | Civil/Structural Engineer + survey data (DEL-008-02) | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Core Directional Foundation | 0 | NO_ITEMS | Directional foundation is established |
| X:guiding:sufficiency | guiding | sufficiency | Justified Guidance Competence | 0 | NO_ITEMS | Guidance is justified and competent |
| X:guiding:completeness | guiding | completeness | Comprehensive Guidance Authority | 0 | NO_ITEMS | Guidance authority is comprehensive |
| X:guiding:consistency | guiding | consistency | Coherent Guidance Stability | 0 | NO_ITEMS | Guidance is coherent and stable |
| X:applying:necessity | applying | necessity | Vital Competence Obligation | 1 | HAS_ITEMS | Emergency shower verification gap |
| X:applying:sufficiency | applying | sufficiency | Demonstrated Delivery Competence | 0 | NO_ITEMS | Delivery competence is demonstrated through procedure |
| X:applying:completeness | applying | completeness | Total Implementation Accounting | 1 | HAS_ITEMS | Overflow/vent not in requirements |
| X:applying:consistency | applying | consistency | Consistent Execution Integrity | 0 | NO_ITEMS | Execution integrity is consistent |
| X:judging:necessity | judging | necessity | Fundamental Outcome Determination | 1 | HAS_ITEMS | REQ-016 verification is vague |
| X:judging:sufficiency | judging | sufficiency | Justified Evaluation Finding | 0 | NO_ITEMS | Evaluation findings are justified |
| X:judging:completeness | judging | completeness | Exhaustive Judgment Mastery | 0 | NO_ITEMS | Judgment coverage is exhaustive for preliminary stage |
| X:judging:consistency | judging | consistency | Stable Judgment Coherence | 0 | NO_ITEMS | Judgment coherence is stable |
| X:reviewing:necessity | reviewing | necessity | Fundamental Assurance Basis | 1 | HAS_ITEMS | Washroom water tap function ambiguous |
| X:reviewing:sufficiency | reviewing | sufficiency | Justified Assurance Competence | 0 | NO_ITEMS | Assurance competence is justified |
| X:reviewing:completeness | reviewing | completeness | Comprehensive Audit Command | 0 | NO_ITEMS | Audit command is comprehensive through records section |
| X:reviewing:consistency | reviewing | consistency | Coherent Oversight Stability | 0 | NO_ITEMS | Oversight stability is coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | VerificationGap | Specification | Specification | Add verification criterion for emergency shower travel-distance compliance (REQ-010 verification only checks location consistency with R-06, not code-required travel distance from hazard zones) | Vital competence obligation for emergency shower requires verifying code compliance, not just location consistency. Guidance Principle 3 notes the 10-second travel requirement but REQ-010 verification does not test against it. | Specification.md, Guidance.md | Specification > REQ-010 verification; Guidance > Principle 3 | -- | Plumbing Engineer / applicable code | TBD |
| X-002 | X:applying:completeness | MissingSlot | Specification | Specification | Add requirement for cistern overflow and vent provisions -- Procedure Step 2 item 2 includes "Overflow and vent provisions" but no corresponding Specification requirement or verification exists | Total Implementation Accounting requires that cistern overflow and venting be tracked as a verifiable requirement. Currently it appears only in the Procedure as a design task. | Specification.md, Procedure.md | Specification > Requirements (absent); Procedure > Step 2 item 2 | -- | Plumbing Engineer / NPC | TBD |
| X-003 | X:judging:necessity | VerificationGap | Specification | Specification | Strengthen REQ-016 verification: "Preliminary design package includes sufficient information for permit preparation" is subjective -- add measurable acceptance criteria | Fundamental Outcome Determination for permit readiness requires an objective test. "Sufficient information" is not measurable and leaves the pass/fail condition to interpretation. | Specification.md | REQ-016 verification | -- | Plumbing Engineer / Safety Codes Officer | TBD |
| X-004 | X:reviewing:necessity | TBD_Question | Guidance | Guidance | Record TBD: Confirm function of the water tap shown at the south end of the utility room/washroom area on R-06 -- Guidance notes ambiguity but no resolution is documented | Fundamental Assurance Basis requires that all fixtures shown on the conceptual drawing be identified. Guidance > Considerations > Washroom Water Tap Location raises this but leaves it unresolved. | Guidance.md | Considerations > Washroom Water Tap Location | -- | Review of R-06 / County clarification | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Verified Directional Evidence | 0 | NO_ITEMS | Directional evidence is verified through R-01/R-06 sourcing |
| E:guiding:information | guiding | information | Contextualized Steering Signal | 1 | HAS_ITEMS | Mezzanine clearance conflict potential not tracked |
| E:guiding:knowledge | guiding | knowledge | Strategic Governance Mastery | 0 | NO_ITEMS | Strategic governance is adequate |
| E:guiding:wisdom | guiding | wisdom | Principled Governance Vision | 0 | NO_ITEMS | Governance vision is principled |
| E:applying:data | applying | data | Verified Execution Record | 0 | NO_ITEMS | Execution record is verifiable |
| E:applying:information | applying | information | Contextual Implementation Signal | 1 | HAS_ITEMS | SOW cross-reference gap |
| E:applying:knowledge | applying | knowledge | Demonstrated Implementation Mastery | 0 | NO_ITEMS | Implementation mastery is demonstrated |
| E:applying:wisdom | applying | wisdom | Principled Implementation Insight | 0 | NO_ITEMS | Implementation insight is principled |
| E:judging:data | judging | data | Verified Judgment Record | 0 | NO_ITEMS | Judgment records are verifiable |
| E:judging:information | judging | information | Contextual Adjudication Signal | 0 | NO_ITEMS | Adjudication signals are contextualized |
| E:judging:knowledge | judging | knowledge | Authoritative Assessment Mastery | 0 | NO_ITEMS | Assessment mastery is adequate |
| E:judging:wisdom | judging | wisdom | Principled Adjudicative Insight | 0 | NO_ITEMS | Adjudicative insight is principled |
| E:reviewing:data | reviewing | data | Verified Oversight Record | 1 | HAS_ITEMS | Normalization of SOW reference in Datasheet |
| E:reviewing:information | reviewing | information | Contextual Oversight Account | 0 | NO_ITEMS | Oversight account is contextualized |
| E:reviewing:knowledge | reviewing | knowledge | Comprehensive Oversight Mastery | 0 | NO_ITEMS | Oversight mastery is comprehensive |
| E:reviewing:wisdom | reviewing | wisdom | Principled Oversight Perspective | 0 | NO_ITEMS | Oversight perspective is principled |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:information | RationaleGap | Guidance | Guidance | Add mezzanine plumbing clearance as a coordination requirement or risk item -- Guidance notes the concern (cistern venting, drain vent stacks, overhead routing vs mezzanine structure and crane envelope) but no requirement or trade-off entry captures it | Contextualized Steering Signal for plumbing routing conflicts with the mezzanine and 35' ceiling crane envelope is raised in Guidance but not actionably tracked. There is no corresponding requirement in Specification or verification check in Procedure. | Guidance.md | Considerations > Mezzanine and Plumbing Clearance | -- | Plumbing Engineer / Structural Engineer | TBD |
| E-002 | E:applying:information | Normalization | Datasheet | Datasheet | Normalize SOW references in Datasheet Construction table: SOW-0047 noted as deleted/merged into SOW-0027b but SOW-0027b does not appear in the Datasheet References table | Contextual Implementation Signal requires consistent SOW traceability. SOW-0027b is referenced in Specification REQ-009 and Guidance Principle 2 but not in the Datasheet References or Construction table, creating a gap in the reference chain. | Datasheet.md, Specification.md | Datasheet > Construction > Note; Specification > REQ-009 | -- | Decomposition document | TBD |
| E-003 | E:reviewing:data | VerificationGap | Procedure | Procedure | Add verification check for wash bay drainage separation (no cross-connection between wash bay effluent and sanitary system) -- Procedure Verification table includes this but Specification verification for REQ-009 does not explicitly test separation | Verified Oversight Record requires that the drainage separation safety requirement (a core design principle per Guidance Principle 2) be verifiable at both the Specification and Procedure level. Specification REQ-009 verification checks mud sump connection but not separation from sanitary system. | Specification.md, Procedure.md | Specification > REQ-009 verification; Procedure > Verification > "Wash bay drain separated from sanitary drain" | -- | Plumbing Engineer | TBD |
