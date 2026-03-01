# Semantic Lensing Register: DEL-002-12 Structural Specification

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-002_Structural Design/1_Working/DEL-002-12_Specification/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-002-12_Specification/_CONTEXT.md
- _STATUS.md — DEL-002-12_Specification/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md — DEL-002-12_Specification/_SEMANTIC.md
- Datasheet.md — DEL-002-12_Specification/Datasheet.md
- Specification.md — DEL-002-12_Specification/Specification.md
- Guidance.md — DEL-002-12_Specification/Guidance.md
- Procedure.md — DEL-002-12_Specification/Procedure.md
- _REFERENCES.md — DEL-002-12_Specification/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 4
  - Specification: 13
  - Guidance: 4
  - Procedure: 4
  - Multi: 3
- By matrix:
  - A: 5  B: 4  C: 3  F: 4  D: 3  X: 5  E: 4
- By type:
  - Conflict: 0
  - VerificationGap: 6
  - MissingSlot: 7
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 5
  - MatrixError: 0
- Notable conflicts: 1 (cross-reference to Guidance CON-002, not a new warranted item)
- Matrix parse errors: 0

---

## Matrix A — Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Weak prescriptive language on concrete system selection |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | No mandatory practice for corrosion protection of embedments |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Code edition unconfirmed |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit pathway addressed via P.Eng. stamp and AHJ permit |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Missing procedural direction for Old North Shop as-built acquisition |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Procedure steps cover practical execution adequately |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | Mezzanine live load not quantitatively confirmed |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Process audit pathway covered by Step 8 internal review |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Value orientation expressed through Guidance principles |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs table addresses merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Trade-off recommended approaches address worth determination |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | QA review covered by Procedure Step 8 |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify whether REQ-001 "concrete structure" is prescriptive of the material system only or also prescribes the construction method (tilt-up vs. cast-in-place vs. precast) | Specification REQ-001 states "concrete structure" as the system but Guidance Consideration 1 notes the RFP does not prescribe the concrete construction method. The normative document should explicitly state whether the construction method is open or constrained. | Specification.md; Guidance.md | Specification#REQ-001; Guidance#Consideration 1 | — | Structural Engineer | TBD |
| A-002 | A:normative:applying | MissingSlot | Specification | Specification | Add mandatory corrosion protection requirements for steel embedment plates in the concrete floor (industrial environment with wash bay proximity) | Guidance Consideration 3 identifies corrosion protection as a design factor for steel embedments but no corresponding normative requirement exists in Specification.md. This is a mandatory practice gap under the normative-applying lens. | Specification.md; Guidance.md | Specification#REQ-003; Guidance#Consideration 3 | — | Structural Engineer | TBD |
| A-003 | A:normative:judging | TBD_Question | Specification | Specification | Record TBD: Confirm applicable NBC edition with AHJ. Currently marked ASSUMPTION (NBC 2019). Compliance determination cannot proceed until code edition is confirmed. | REQ-010 and the Standards table both note the applicable code edition as an ASSUMPTION. Compliance determination under this lens requires a confirmed code reference. | Specification.md | Specification#REQ-010; Specification#Standards | — | AHJ / Structural Engineer | TBD |
| A-004 | A:operative:guiding | MissingSlot | Procedure | Procedure | Add a sub-step under Step 7 for acquiring as-built drawings of the Old North Shop, or explicitly recording their absence and the fallback to field measurements | Procedure Step 7.2 mentions reviewing as-built drawings "if they exist" but provides no procedural direction for how to acquire them or whom to contact. The operative-guiding lens flags this as an absent procedural pathway. | Procedure.md | Procedure#Step 7 | — | Design-Build PM | TBD |
| A-005 | A:operative:judging | TBD_Question | Specification | Specification | Record TBD: Confirm mezzanine design live load with Owner. The 4.8 kPa / 100 psf figure is labeled ASSUMPTION and requires Owner confirmation before performance assessment can proceed. | REQ-005 notes an assumed live load that "must be confirmed." The operative-judging lens flags that performance assessment of the mezzanine design cannot be completed without a confirmed load value. | Specification.md | Specification#REQ-005 | — | Owner / Structural Engineer | TBD |

---

## Matrix B — Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Snow/wind/seismic loads TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Geotechnical data TBD |
| B:data:completeness | data | completeness | comprehensive record | 0 | NO_ITEMS | Datasheet records are comprehensive for available inputs |
| B:data:consistency | data | consistency | reliable measurement | 1 | HAS_ITEMS | Bay dimensions labeled approximate |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Essential signals present across documents |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context is adequate for Pass 1 stage |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Documents provide comprehensive accounts within source constraints |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Cross-document messaging is coherent |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding of structural scope is present |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise requirements addressed via P.Eng. requirement |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Scope mastery appropriate for Pass 1 |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 1 | HAS_ITEMS | Crane fatigue class discernment needed |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment calls appropriately deferred to Structural Engineer |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic insight addressed through Guidance considerations |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning principles are consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Snow loads, wind loads, and seismic design category for project location (SW 14-44-21-W4, Ferintosh AB) must be determined from applicable code | These are essential facts required for structural design. They are listed as TBD in the Datasheet Conditions table. Without these values, no structural sizing can proceed. | Datasheet.md | Datasheet#Conditions | — | Structural Engineer / NBC lookup | TBD |
| B-002 | B:data:sufficiency | TBD_Question | Datasheet | Datasheet | Record TBD: Geotechnical investigation report (DEL-008-01) is pending. Foundation interface parameters cannot be established until geotech data is available. | The geotechnical conditions row in the Datasheet is TBD. Adequate evidence for foundation-superstructure interface design is missing. | Datasheet.md | Datasheet#Conditions | — | PKG-008 / Geotechnical Engineer | TBD |
| B-003 | B:data:consistency | WeakStatement | Datasheet | Datasheet | Clarify whether bay dimensions in the Drive Bay Layout table are nominal design targets or approximate conceptual values not to be relied upon for structural design | The Datasheet Drive Bay Layout note states dimensions are "approximate" and "subject to structural design." This creates ambiguity about whether these are reliable measurements for design input or merely illustrative. | Datasheet.md | Datasheet#Drive Bay Layout | — | Structural Engineer / Architect | TBD |
| B-004 | B:wisdom:necessity | RationaleGap | Guidance | Guidance | Add rationale for selecting CMAA crane fatigue classification. Guidance Consideration 2 identifies the need but does not provide sufficient discernment criteria for the landfill maintenance use case. | Essential discernment is needed to choose between CMAA Class B/C (moderate) and Class D/E (heavy). The trade-off table notes this as an ASSUMPTION but the reasoning basis for the selection is thin. | Guidance.md | Guidance#Consideration 2; Guidance#Trade-offs | — | Structural Engineer / Owner (usage frequency data) | TBD |

---

## Matrix C — Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Obligation | 1 | HAS_ITEMS | Embedment load requirements unspecified |
| C:normative:sufficiency | normative | sufficiency | Certified Threshold | 1 | HAS_ITEMS | Acceptance thresholds missing for several REQs |
| C:normative:completeness | normative | completeness | Exhaustive Compliance Record | 0 | NO_ITEMS | Compliance record structure is present (Verification table) |
| C:normative:consistency | normative | consistency | Harmonized Rigor | 0 | NO_ITEMS | Normative rigor is consistent across requirements |
| C:operative:necessity | operative | necessity | Operational Catalyst | 0 | NO_ITEMS | Operational catalysts (prerequisites) are identified in Procedure |
| C:operative:sufficiency | operative | sufficiency | Feasible Competence | 0 | NO_ITEMS | Personnel and tool prerequisites address feasible competence |
| C:operative:completeness | operative | completeness | Comprehensive Delivery | 0 | NO_ITEMS | Procedure steps cover delivery sequence comprehensively |
| C:operative:consistency | operative | consistency | Predictable Discipline | 0 | NO_ITEMS | Procedure is disciplined and sequenced |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Standard | 1 | HAS_ITEMS | No explicit quality standard for specification document itself |
| C:evaluative:sufficiency | evaluative | sufficiency | Warranted Judgment | 0 | NO_ITEMS | Judgment calls are warranted and deferred appropriately |
| C:evaluative:completeness | evaluative | completeness | Holistic Reckoning | 0 | NO_ITEMS | Holistic view addressed through Guidance |
| C:evaluative:consistency | evaluative | consistency | Principled Congruence | 0 | NO_ITEMS | Principles are congruent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | VerificationGap | Specification | Specification | Add enforceable load requirements for steel embedment plates (track/packer equipment loads, impact factors). Currently REQ-003 states embedments shall be provided but does not specify the design load as an enforceable obligation. | Under the Enforceable Obligation lens, REQ-003 lacks quantified or referenced load criteria. The requirement is functional ("accommodate track and packer type heavy equipment") but does not bind to a specific load standard or calculation method. | Specification.md | Specification#REQ-003 | — | Structural Engineer | TBD |
| C-002 | C:normative:sufficiency | VerificationGap | Specification | Specification | Add quantitative acceptance thresholds to the Verification table for REQ-004 (service pit structural capacity) and REQ-007 (mud sump excavator load capacity). Currently verification is "confirmed on IFC drawings" without stating what constitutes passing. | Under the Certified Threshold lens, several verification approaches lack measurable pass/fail criteria. "Confirmed on IFC drawings" and "field inspection" are methods but not thresholds. | Specification.md | Specification#Verification | — | Structural Engineer | TBD |
| C-003 | C:evaluative:necessity | MissingSlot | Guidance | Guidance | Add a quality standard or acceptance benchmark for the Structural Specification document itself (e.g., completeness checklist, peer review criteria, MasterFormat compliance check) | Under the Intrinsic Standard lens, there is no explicit quality benchmark defined for the specification deliverable as a document product. The Procedure verification table lists checks but the Guidance document does not articulate the standard those checks serve. | Guidance.md | Guidance#entire document scanned | — | Structural Engineer / QA Lead | TBD |

---

## Matrix F — Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Irrefutable Prerequisite | 1 | HAS_ITEMS | Crane specifications are an irrefutable prerequisite, still TBD |
| F:normative:sufficiency | normative | sufficiency | Certified Demonstration | 1 | HAS_ITEMS | No demonstration path for fire rating |
| F:normative:completeness | normative | completeness | Unified Codification | 0 | NO_ITEMS | Requirements are codified in REQ-001 through REQ-011 |
| F:normative:consistency | normative | consistency | Confirmed Coherence | 1 | HAS_ITEMS | Scope boundary inconsistency for Old North Shop |
| F:operative:necessity | operative | necessity | Executable Readiness | 0 | NO_ITEMS | Prerequisites table addresses readiness |
| F:operative:sufficiency | operative | sufficiency | Demonstrated Capability | 0 | NO_ITEMS | P.Eng. requirement demonstrates capability |
| F:operative:completeness | operative | completeness | Integrated Fulfillment | 0 | NO_ITEMS | Procedure covers fulfillment path |
| F:operative:consistency | operative | consistency | Systematic Stability | 0 | NO_ITEMS | Procedure steps are systematically sequenced |
| F:evaluative:necessity | evaluative | necessity | Core Valuation | 1 | HAS_ITEMS | No explicit valuation criteria for trade-off decisions |
| F:evaluative:sufficiency | evaluative | sufficiency | Founded Evaluation | 0 | NO_ITEMS | Trade-offs table provides founded evaluation |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Rationale | 0 | NO_ITEMS | Rationale is present in Guidance |
| F:evaluative:consistency | evaluative | consistency | Principled Steadiness | 0 | NO_ITEMS | Evaluative framework is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | TBD_Question | Multi | Specification | Record TBD: Crane manufacturer specifications (wheel loads, runway gauge, bridge span, CMAA service class) are an irrefutable prerequisite for crane runway structural design. Source and timeline for obtaining these specs must be established. | REQ-002 requires crane supports but crane specs are TBD. Procedure Step 3 addresses this but the Specification does not include a conditional hold or fallback requirement. | Specification.md; Procedure.md | Specification#REQ-002; Procedure#Step 3 | — | Owner / Proponent procurement | TBD |
| F-002 | F:normative:sufficiency | MissingSlot | Specification | Specification | Add fire resistance rating requirement for the concrete structural system. Guidance Consideration 1 references fire rating as a performance requirement but no corresponding REQ exists in Specification.md. | Under the Certified Demonstration lens, the specification must demonstrate code compliance including fire resistance. Guidance mentions "fire rating" as a performance requirement to be specified but no normative requirement captures it. | Specification.md; Guidance.md | Specification#entire document scanned; Guidance#Consideration 1 | — | NBC / Structural Engineer | TBD |
| F-003 | F:normative:consistency | Normalization | Multi | Guidance | Normalize scope boundary language for Old North Shop renovation. Specification REQ-008 includes the renovation; Specification Scope section excludes "construction execution" but renovation involves assessment of existing structure which blurs the line between design and investigation. | Under the Confirmed Coherence lens, the scope boundary for the Old North Shop renovation work is not consistently delineated between design scope (DEL-002-12) and investigation/assessment scope. | Specification.md; Procedure.md | Specification#REQ-008; Specification#Scope; Procedure#Step 7 | — | Structural Engineer / PM | TBD |
| F-004 | F:evaluative:necessity | RationaleGap | Guidance | Guidance | Add core valuation criteria for the concrete system type trade-off. The trade-off table lists options but does not articulate what factors (cost, schedule, quality, site constraints) should be weighted and by whom. | Under the Core Valuation lens, the trade-off between tilt-up, cast-in-place, and precast concrete lacks explicit evaluation criteria. The recommended approach defers entirely to the Structural Engineer without stating what the Owner values most. | Guidance.md | Guidance#Trade-offs | — | Owner / Structural Engineer | TBD |

---

## Matrix D — Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Resolved Directive | 0 | NO_ITEMS | Directives are resolved through REQ set |
| D:normative:applying | normative | applying | Definitive Enactment | 1 | HAS_ITEMS | No definitive statement on structural system for mezzanine |
| D:normative:judging | normative | judging | Codified Ruling | 0 | NO_ITEMS | Codified rulings present in REQ-009, REQ-010 |
| D:normative:reviewing | normative | reviewing | Confirmed Examination | 0 | NO_ITEMS | Examination pathway via P.Eng. review and AHJ permit |
| D:operative:guiding | operative | guiding | Resolved Guidance | 0 | NO_ITEMS | Guidance principles are resolved |
| D:operative:applying | operative | applying | Verified Delivery | 1 | HAS_ITEMS | No verification step for coordination package delivery |
| D:operative:judging | operative | judging | Holistic Capability Verdict | 0 | NO_ITEMS | Capability verdict addressed through Procedure verification table |
| D:operative:reviewing | operative | reviewing | Stable Examination | 0 | NO_ITEMS | Stable examination covered by internal review |
| D:evaluative:guiding | evaluative | guiding | Resolved Purpose | 0 | NO_ITEMS | Purpose is clearly articulated in Guidance |
| D:evaluative:applying | evaluative | applying | Substantiated Value | 1 | HAS_ITEMS | OBJ-003 traceability incomplete |
| D:evaluative:judging | evaluative | judging | Justified Appraisal | 0 | NO_ITEMS | Appraisal framework present in trade-offs |
| D:evaluative:reviewing | evaluative | reviewing | Sustained Scrutiny | 0 | NO_ITEMS | Scrutiny sustained through verification checks |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | WeakStatement | Specification | Specification | Clarify whether the mezzanine structural system is concrete, steel, or open to either. REQ-005 requires a "load-bearing mezzanine" but does not specify the material system, while REQ-001 mandates a concrete structure overall. | Under the Definitive Enactment lens, the mezzanine material system is ambiguous. If the building is a concrete structure, is the mezzanine also concrete, or can it be structural steel? This affects design scope and standards (CSA A23.3 vs. CSA S16). | Specification.md | Specification#REQ-005; Specification#REQ-001 | — | Structural Engineer | TBD |
| D-002 | D:operative:applying | VerificationGap | Procedure | Procedure | Add a verification step or checklist confirming that the structural coordination package (Step 6) was issued to all required disciplines and that responses were received and resolved | Under the Verified Delivery lens, Procedure Step 6 directs issuance of a coordination package but there is no verification step confirming it was delivered and closed out. The Procedure verification table mentions "coordination log closed out" but no step produces or closes this log. | Procedure.md | Procedure#Step 6; Procedure#Verification | — | Design-Build PM | TBD |
| D-003 | D:evaluative:applying | Normalization | Specification | Specification | Add explicit traceability statement linking the Structural Specification deliverable to OBJ-003 ("complete, P.Eng.-stamped IFC design documentation"). Currently OBJ-003 is referenced in the Scope section but not in the Documentation or Verification sections. | Under the Substantiated Value lens, the value of DEL-002-12 to OBJ-003 is stated in the Scope section but not carried through to verification. The deliverable's contribution to OBJ-003 should be traceable at the verification level. | Specification.md | Specification#Scope; Specification#Documentation; Specification#Verification | — | PM | TBD |

---

## Matrix X — Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Established Prerequisite | 1 | HAS_ITEMS | Prerequisite for preliminary structural design approval missing timeline |
| X:guiding:sufficiency | guiding | sufficiency | Defined Competence | 0 | NO_ITEMS | Competence defined via P.Eng. requirement |
| X:guiding:completeness | guiding | completeness | Authoritative Mastery | 0 | NO_ITEMS | Mastery scope addressed through standards list |
| X:guiding:consistency | guiding | consistency | Harmonized Standard | 1 | HAS_ITEMS | Mixed unit systems |
| X:applying:necessity | applying | necessity | Validated Essential | 1 | HAS_ITEMS | Verification approach for REQ-008 lacks validated baseline |
| X:applying:sufficiency | applying | sufficiency | Demonstrated Proof | 0 | NO_ITEMS | Demonstration paths exist for most requirements |
| X:applying:completeness | applying | completeness | Total Mastered Fulfillment | 0 | NO_ITEMS | Fulfillment path addressed through IFC package assembly |
| X:applying:consistency | applying | consistency | Reliable Accord | 0 | NO_ITEMS | Accord between documents is reliable |
| X:judging:necessity | judging | necessity | Imperative Awareness | 1 | HAS_ITEMS | No awareness criterion for variable-price scope trigger |
| X:judging:sufficiency | judging | sufficiency | Adjudicated Credential | 0 | NO_ITEMS | Credential (P.Eng.) is adjudicated |
| X:judging:completeness | judging | completeness | Comprehensive Ruling | 0 | NO_ITEMS | Comprehensive ruling structure present in Verification table |
| X:judging:consistency | judging | consistency | Calibrated Judgment | 0 | NO_ITEMS | Judgment is calibrated across verification approaches |
| X:reviewing:necessity | reviewing | necessity | Confirmed Dependability | 0 | NO_ITEMS | Dependability confirmed through multi-discipline review |
| X:reviewing:sufficiency | reviewing | sufficiency | Audited Competence | 0 | NO_ITEMS | Audit of competence via internal QA review |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Audit Trail | 1 | HAS_ITEMS | Records table missing inspection report retention detail |
| X:reviewing:consistency | reviewing | consistency | Enduring Conformity | 0 | NO_ITEMS | Conformity pathway consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:necessity | WeakStatement | Procedure | Procedure | Clarify the timeline dependency between DEL-002-01 (Preliminary Structural Design) approval and DEL-002-12 finalization. The prerequisite is listed but no sequencing constraint or hold point is stated. | Under the Established Prerequisite lens, the prerequisite for County approval of the preliminary structural design (DEL-002-01) is listed in the Procedure prerequisites table but is not carried into the Steps as a gate or hold point. | Procedure.md | Procedure#Prerequisites | — | PM / Structural Engineer | TBD |
| X-002 | X:guiding:consistency | Normalization | Datasheet | Multi | Normalize unit system across documents. Datasheet uses imperial (ft, sq ft) with one metric reference in Specification (4.8 kPa / 100 psf). Establish whether the project convention is imperial, metric, or dual. | Under the Harmonized Standard lens, the unit system is inconsistent. The Datasheet and RFP references are imperial; the Specification and Guidance introduce metric values (kPa) alongside imperial. A convention should be stated. | Datasheet.md; Specification.md; Guidance.md | Datasheet#Building Geometry; Specification#REQ-005; Guidance#Consideration 4 | — | Structural Engineer / Owner convention | TBD |
| X-003 | X:applying:necessity | VerificationGap | Specification | Specification | Add verification baseline for REQ-008 (Old North Shop mezzanine renovation). The verification approach states "structural assessment report reviewed" but no criteria for what constitutes an acceptable assessment are specified. | Under the Validated Essential lens, verification of the Old North Shop renovation requires a baseline (existing capacity vs. required capacity) that is not yet defined. The verification row assumes an assessment report will exist but does not define acceptance criteria. | Specification.md | Specification#Verification (REQ-008) | — | Structural Engineer | TBD |
| X-004 | X:judging:necessity | MissingSlot | Specification | Specification | Add a requirement or procedural trigger for how deleterious subgrade material discovery (per RFP S4.8.2) affects the superstructure design scope and triggers re-evaluation of the Structural Specification | Under the Imperative Awareness lens, the variable-price foundation scope trigger (deleterious subgrade) could affect the superstructure design (e.g., different foundation system changing load paths). REQ-011 addresses geotech coordination but does not address the scope change trigger. | Specification.md; Procedure.md | Specification#REQ-011; Procedure#Step 2.4 | — | PM / Owner | TBD |
| X-005 | X:reviewing:completeness | MissingSlot | Procedure | Procedure | Add detail to the Records table specifying what structural inspection reports must be retained, their format, and retention period, per RFP S3.3.2 requirement that the County representative receives inspection reports | Under the Exhaustive Audit Trail lens, the Procedure Records table references "Inspection reports (copies)" but does not specify which inspections, what format, or how the RFP S3.3.2 requirement for County receipt is fulfilled operationally. | Procedure.md | Procedure#Records | — | PM / Structural Engineer | TBD |

---

## Matrix E — Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Baseline | 1 | HAS_ITEMS | No authoritative baseline for existing Old North Shop structure |
| E:guiding:information | guiding | information | Authoritative Communication | 0 | NO_ITEMS | Communication pathways identified in Procedure |
| E:guiding:knowledge | guiding | knowledge | Masterful Insight | 0 | NO_ITEMS | Insight level appropriate for Pass 1 |
| E:guiding:wisdom | guiding | wisdom | Authoritative Foresight | 1 | HAS_ITEMS | No foresight on future expansion or adaptability |
| E:applying:data | applying | data | Established Performance | 1 | HAS_ITEMS | Service pit edge load criteria missing |
| E:applying:information | applying | information | Verified Account | 0 | NO_ITEMS | Accounts are verified against RFP sources |
| E:applying:knowledge | applying | knowledge | Demonstrated Proficiency | 0 | NO_ITEMS | Proficiency demonstration via P.Eng. pathway |
| E:applying:wisdom | applying | wisdom | Demonstrated Sagacity | 0 | NO_ITEMS | Sagacity demonstrated in Guidance trade-offs |
| E:judging:data | judging | data | Validated Determination | 0 | NO_ITEMS | Determinations are validated against RFP |
| E:judging:information | judging | information | Calibrated Account | 0 | NO_ITEMS | Accounts are calibrated and sourced |
| E:judging:knowledge | judging | knowledge | Verified Mastery | 0 | NO_ITEMS | Mastery verification via P.Eng. + peer review |
| E:judging:wisdom | judging | wisdom | Calibrated Prudence | 0 | NO_ITEMS | Prudence reflected in ASSUMPTION labeling |
| E:reviewing:data | reviewing | data | Audited Provenance | 1 | HAS_ITEMS | Source column missing from Specification Verification table |
| E:reviewing:information | reviewing | information | Thorough Audit Report | 0 | NO_ITEMS | Audit reporting addressed in Procedure Records |
| E:reviewing:knowledge | reviewing | knowledge | Audited Oversight | 0 | NO_ITEMS | Oversight audited through multi-discipline review |
| E:reviewing:wisdom | reviewing | wisdom | Enduring Judgment | 0 | NO_ITEMS | Enduring judgment supported by conflict table in Guidance |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | RationaleGap | Multi | Guidance | Add guidance on how to establish the authoritative baseline for the existing Old North Shop mezzanine structure (e.g., as-built drawings, field survey, destructive testing) when no as-built data is available | Under the Authoritative Baseline lens, there is no baseline data for the existing Old North Shop structure. REQ-008 requires renovation; Procedure Step 7 requires assessment; but neither Guidance nor the Datasheet establishes what constitutes an authoritative baseline for the existing conditions. | Datasheet.md; Specification.md; Guidance.md; Procedure.md | Specification#REQ-008; Procedure#Step 7; Datasheet#Structural Elements; Guidance#Consideration 5 | — | Structural Engineer | TBD |
| E-002 | E:guiding:wisdom | MissingSlot | Guidance | Guidance | Add a consideration for future building adaptability or expansion. The RFP and current documents address only the immediate program. Authoritative Foresight lens suggests considering whether the structural system should accommodate future expansion (e.g., additional bays, crane capacity upgrades). | Under the Authoritative Foresight lens, no document addresses whether the structural design should accommodate any future growth or adaptability. This may be intentional (fixed program) but should be explicitly stated. | Guidance.md | Guidance#entire document scanned | — | Owner / PM | TBD |
| E-003 | E:applying:data | VerificationGap | Specification | Specification | Add specific performance criterion for service pit edge loads in the Verification table. REQ-004 references "applicable equipment loads at the edges" but the Verification row does not specify what load case or factor of safety constitutes passing. | Under the Established Performance lens, the service pit verification approach ("pit dimensions and structural capacity confirmed on IFC drawings") does not establish what performance level (load case, FOS) constitutes acceptance. | Specification.md | Specification#REQ-004; Specification#Verification | — | Structural Engineer | TBD |
| E-004 | E:reviewing:data | VerificationGap | Specification | Specification | Add a Source/Provenance column to the Specification Verification table linking each verification approach back to the requirement source and applicable standard clause | Under the Audited Provenance lens, the Specification Verification table lists requirement-verification pairs but does not trace back to the source standard or code clause that dictates the verification method. This weakens audit traceability. | Specification.md | Specification#Verification | — | Structural Engineer | TBD |

---

## Conflict Register (cross-matrix)

The following conflict was identified across multiple lenses and is elevated here for visibility:

| Conflict ID | Description | Lenses | Contenders | HumanRuling |
|---|---|---|---|---|
| XCON-001 | Steel embedment plate locations: RFP S3.4 describes performance intent ("accommodate track and packer type heavy equipment") while Appendix B shows specific plate locations on the floor plan. It is unclear whether the Appendix B layout is prescriptive or illustrative. This conflict was previously identified in Guidance CON-002 and surfaces under multiple lenses (A:normative:applying, C:normative:necessity, F:normative:consistency). | A:normative:applying; C:normative:necessity | Guidance.md#Conflict Table CON-002; Specification.md#REQ-003 | TBD — already recorded in Guidance CON-002 |

---

*This register was generated by CHIRALITY_LENS and is intended for consumption by a subsequent enrichment agent. It does not modify any production documents.*
