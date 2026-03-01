# Semantic Lensing Register: DEL-006-05 Septic System Details

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-006_Plumbing Design/1_Working/DEL-006-05_Septic-Details/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-006-05_Septic-Details/_CONTEXT.md (Identification, Description, Anticipated Artifacts)
- _STATUS.md — DEL-006-05_Septic-Details/_STATUS.md (Status: SEMANTIC_READY, dated 2026-02-26)
- _SEMANTIC.md — DEL-006-05_Septic-Details/_SEMANTIC.md (Matrices A, B, C, F, D, X, E parsed; Audit PASS)
- Datasheet.md — DEL-006-05_Septic-Details/Datasheet.md (Identification, Attributes, Conditions, Construction, References)
- Specification.md — DEL-006-05_Septic-Details/Specification.md (Scope, Requirements, Standards, Verification, Documentation)
- Guidance.md — DEL-006-05_Septic-Details/Guidance.md (Purpose, Principles, Considerations, Trade-offs, Conflict Table)
- Procedure.md — DEL-006-05_Septic-Details/Procedure.md (Prerequisites, Steps 1-6, Verification, Records)
- _REFERENCES.md — DEL-006-05_Septic-Details/_REFERENCES.md (Primary References R-01 and R-06; Internal References SOW-0016, OBJ-001, OBJ-003, OBJ-004)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 22
- By document:
  - Datasheet: 5
  - Specification: 8
  - Guidance: 2
  - Procedure: 4
  - Multi: 3
- By matrix:
  - A: 5  B: 4  C: 3  F: 3  D: 3  X: 2  E: 2
- By type:
  - Conflict: 1
  - VerificationGap: 4
  - MissingSlot: 5
  - WeakStatement: 3
  - RationaleGap: 2
  - Normalization: 3
  - TBD_Question: 4
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A — Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Specific safety code editions TBD |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Tank capacity unit normalization needed |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Verification gap for code compliance |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit pathway adequately described across docs |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure provides adequate procedural direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Existing tank removal execution details TBD |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Performance assessment covered in Procedure verification table |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Process audit covered via internal QA step (Procedure Step 4) |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | Rationale gap for tank sizing acceptance |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Merit application adequately covered by trade-offs in Guidance |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Worth determination covered via verification and County approval |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality appraisal addressed through IFC review process |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Record TBD: Confirm specific Alberta Safety Codes edition and Alberta Private Sewage Systems Standard of Practice edition applicable to this holding tank installation | Prescriptive direction lens reveals that the governing standards are referenced generically but no specific edition or clause numbers are identified; this leaves normative guidance incomplete. | Specification.md | Standards | — | Plumbing Engineer / AHJ | TBD |
| A-002 | A:normative:applying | Normalization | Multi | Datasheet | Normalize tank capacity units: state both 2,000 US gallons and metric equivalent consistently, and clarify whether the metric value (~7,571 L) is an assumption or confirmed conversion | Mandatory practice lens shows the metric equivalent is flagged as "ASSUMPTION" in both Datasheet and Specification but is needed for Alberta regulatory submissions which may use metric. Inconsistent treatment risks confusion. | Datasheet.md; Specification.md | Attributes — Septic Holding Tank; Capacity and Performance | — | Plumbing Engineer (PROPOSAL) | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add verification method for REQ-007 (clearance/setback compliance): specify which Alberta regulation clause defines required setbacks and how numeric compliance will be confirmed | Compliance determination lens reveals REQ-007 requires clearances "as required by applicable Alberta regulations" but the verification row (REQ-007) only states "Drawing annotation review" without naming the regulation that establishes the numeric setback values. | Specification.md | Requirements — REQ-007; Verification — REQ-007 | — | Plumbing Engineer / AHJ (PROPOSAL) | TBD |
| A-004 | A:operative:applying | TBD_Question | Procedure | Procedure | Record TBD: Add step or sub-step for existing tank content pump-out and disposal procedure, including applicable Alberta environmental regulation references | Practical execution lens reveals that existing tank removal is in scope (SOW-0043) and Guidance notes contents must be pumped out and disposed per environmental regulations, but Procedure Step 1 does not include a sub-step for this activity. | Procedure.md; Guidance.md | Step 1 — Confirm Scope and Existing Conditions; Existing Tank (Guidance) | — | Plumbing Engineer / Environmental (PROPOSAL) | TBD |
| A-005 | A:evaluative:guiding | RationaleGap | Guidance | Guidance | Add rationale for accepting the RFP-specified 2,000 US gallon tank size versus requiring independent engineer verification, including decision threshold for scope change | Value orientation lens reveals Guidance discusses sizing rationale as an assumption but does not articulate the decision threshold at which the Plumbing Engineer should formally escalate to the Owner if code requires a larger tank. | Guidance.md | Sizing Rationale | — | Plumbing Engineer / Owner (PROPOSAL) | TBD |

---

## Matrix B — Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Existing tank location not documented |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Geotech dependency unresolved |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Construction section has many TBD entries |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurements present are consistent across docs |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Essential signals (scope, location, capacity) present |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for holding tank vs treatment system adequate in Guidance |
| B:information:completeness | information | completeness | comprehensive account | 1 | HAS_ITEMS | Drain field mentioned in Context but not in production docs |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Message consistent across four documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding of holding tank design adequately conveyed |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise requirements (P.Eng.) clearly stated |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Adequate for current drafting stage |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding consistent across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Key discernment items (holding vs treatment, removal vs relocation) present |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment items present in Guidance trade-offs |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view adequate for current stage |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning consistent across docs |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add existing septic tank location data (coordinates or site reference) once field verification is complete; currently absent from all documents | Essential fact lens reveals the existing tank location is a necessary datum for the removal scope but is not recorded anywhere. Guidance notes it "is not explicitly shown on conceptual drawings." | Datasheet.md; Guidance.md | Construction — Existing tank removal; Existing Tank (Guidance) | — | Site investigation (PROPOSAL) | TBD |
| B-002 | B:data:sufficiency | TBD_Question | Datasheet | Datasheet | Record TBD: Confirm soil percolation data availability and whether it is needed for a holding tank (not a treatment system) | Adequate evidence lens reveals soil percolation data is listed as TBD and dependent on geotech (DEL-008-01). For a holding tank without drain field, percolation data may not be required; clarify whether it is needed for this design type. | Datasheet.md | Conditions — Soil percolation data | — | Plumbing Engineer / Geotech Engineer (PROPOSAL) | TBD |
| B-003 | B:data:completeness | WeakStatement | Datasheet | Datasheet | Clarify which Construction table TBD entries are genuinely pending design vs. which require external input before proceeding | Comprehensive record lens reveals the Construction section contains 8 TBD entries. Some are design decisions (inlet/outlet), some await external data (bedding/backfill from geotech), and some are assumptions (electrical, pump-out). Distinguishing these categories would improve planning. | Datasheet.md | Construction | — | Plumbing Engineer (PROPOSAL) | TBD |
| B-004 | B:information:completeness | Normalization | Multi | Guidance | Reconcile _CONTEXT.md anticipated artifacts (drain field layout, soil absorption system, distribution box, pump station) with production documents that describe a holding tank only, not a treatment/drain-field system | Comprehensive account lens reveals _CONTEXT.md lists "Drain field layout and design," "Soil absorption system details," and "Distribution box and manifold details" as anticipated artifacts, but all four production documents describe a holding tank (no drain field). This discrepancy should be resolved. | _CONTEXT.md; Guidance.md | Anticipated Artifacts (_CONTEXT); Principles — Holding tank, not a treatment system (Guidance) | — | Project Manager / Plumbing Engineer (PROPOSAL) | TBD |

---

## Matrix C — Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Compulsory Compliance Threshold | 1 | HAS_ITEMS | Compliance threshold for private sewage unclear |
| C:normative:sufficiency | normative | sufficiency | Binding Compliance Validation | 0 | NO_ITEMS | Validation pathway (Safety Codes Officer inspection) stated |
| C:normative:completeness | normative | completeness | Obligatory Scope Fulfillment | 1 | HAS_ITEMS | Scope boundary for effluent management unclear |
| C:normative:consistency | normative | consistency | Binding Conformance Alignment | 0 | NO_ITEMS | Conformance alignment consistent across docs |
| C:operative:necessity | operative | necessity | Operational Readiness Prerequisite | 0 | NO_ITEMS | Prerequisites adequately listed in Procedure |
| C:operative:sufficiency | operative | sufficiency | Execution Confidence Assurance | 0 | NO_ITEMS | Execution steps provide adequate assurance |
| C:operative:completeness | operative | completeness | Procedural Scope Completeness | 1 | HAS_ITEMS | Missing commissioning/handover step |
| C:operative:consistency | operative | consistency | Operational Procedural Reliability | 0 | NO_ITEMS | Procedure steps internally consistent |
| C:evaluative:necessity | evaluative | necessity | Fundamental Worth Criterion | 0 | NO_ITEMS | Worth criteria (code compliance, operational readiness) stated |
| C:evaluative:sufficiency | evaluative | sufficiency | Benefit Justification Adequacy | 0 | NO_ITEMS | Justification adequate via Guidance purpose section |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Worth Accounting | 0 | NO_ITEMS | Worth accounting adequate for deliverable scope |
| C:evaluative:consistency | evaluative | consistency | Principled Worth Consistency | 0 | NO_ITEMS | Worth principles consistent across docs |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Clarify whether "all applicable Alberta Safety Codes" (REQ-005) includes the Alberta Private Sewage Systems Standard of Practice as a mandatory standard or whether a separate compliance path applies to holding tanks | Compulsory compliance threshold lens reveals the normative threshold is stated generically. For a holding tank at a rural site, the specific regulatory pathway (Private Sewage vs. building code plumbing) materially affects design decisions. | Specification.md | Standards; Requirements — REQ-005 | — | AHJ / Plumbing Engineer (PROPOSAL) | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add scope clarification for effluent management: confirm that no effluent disposal design is required (holding tank = pump-out only) and remove or qualify "Effluent management" TBD in Datasheet | Obligatory scope fulfillment lens reveals Datasheet lists "Effluent management" as TBD with a note "drain field or effluent disposal design details TBD." This contradicts Guidance Principle 1 (holding tank, not a treatment system). The scope boundary should be explicit. | Datasheet.md; Guidance.md | Construction — Effluent management; Principles — Holding tank, not a treatment system | — | Plumbing Engineer (PROPOSAL) | TBD |
| C-003 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add a commissioning or handover verification step after IFC issue (Step 6) to confirm the installed system matches the drawing set, as referenced by OBJ-004 (commission all plumbing systems to operational readiness) | Procedural scope completeness lens reveals the Procedure ends at IFC issue (Step 6) but does not include a step for confirming that the constructed installation matches the drawings. Guidance references commissioning (DEL-020-01) as a downstream dependency. | Procedure.md; Guidance.md | Steps (after Step 6); Purpose (Guidance — commissioning reference) | — | Project Manager / Plumbing Engineer (PROPOSAL) | TBD |

---

## Matrix F — Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Obligatory Verification Foundation | 1 | HAS_ITEMS | Verification gap for permit verification |
| F:normative:sufficiency | normative | sufficiency | Binding Evidence Proficiency | 0 | NO_ITEMS | Evidence requirements (P.Eng. stamp, drawing review) adequate |
| F:normative:completeness | normative | completeness | Binding Verification Thoroughness | 1 | HAS_ITEMS | Incomplete verification for assumptions |
| F:normative:consistency | normative | consistency | Steadfast Compliance Coherence | 0 | NO_ITEMS | Compliance requirements coherent across docs |
| F:operative:necessity | operative | necessity | Operational Dependability Baseline | 0 | NO_ITEMS | Operational baseline adequately established |
| F:operative:sufficiency | operative | sufficiency | Procedural Execution Proficiency | 0 | NO_ITEMS | Execution proficiency covered by P.Eng. requirement |
| F:operative:completeness | operative | completeness | Exhaustive Operational Assurance | 0 | NO_ITEMS | Operational assurance adequate for design deliverable |
| F:operative:consistency | operative | consistency | Dependable Procedural Harmony | 0 | NO_ITEMS | Procedure steps align with Specification requirements |
| F:evaluative:necessity | evaluative | necessity | Essential Merit Awareness | 0 | NO_ITEMS | Merit awareness reflected in Guidance purpose |
| F:evaluative:sufficiency | evaluative | sufficiency | Merit Validation Proficiency | 0 | NO_ITEMS | Validation pathways adequate |
| F:evaluative:completeness | evaluative | completeness | Thorough Merit Accounting | 1 | HAS_ITEMS | No acceptance criteria for pump-out access |
| F:evaluative:consistency | evaluative | consistency | Principled Merit Coherence | 0 | NO_ITEMS | Merit principles coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | VerificationGap | Specification | Specification | Add verification method or cross-reference for confirming that a separate Safety Code permit is obtained specifically for the private sewage system (REQ-006 references DEL-009-03 but does not specify how to verify the septic-specific permit vs. the building permit) | Obligatory verification foundation lens reveals REQ-006 states permits "shall be obtained" and verification points to "Permit documentation (DEL-009-03)" but does not clarify whether a separate private sewage permit is required (Procedure Step 2.4 flags this as TBD). | Specification.md; Procedure.md | Verification — REQ-006; Step 2 — 2.4 | — | Permit Coordinator / AHJ (PROPOSAL) | TBD |
| F-002 | F:normative:completeness | VerificationGap | Specification | Specification | Add verification step for confirming that all ASSUMPTION-sourced requirements (REQ-007 through REQ-010) are validated against actual regulatory and engineering findings before IFC issue | Binding verification thoroughness lens reveals that REQ-007, REQ-008, REQ-009, and REQ-010 are all sourced from "ASSUMPTION" rather than from explicit RFP or SOW requirements. The verification table confirms them via drawing review, but there is no step to validate the underlying assumptions before they become binding. | Specification.md | Requirements — REQ-007 to REQ-010; Verification | — | Plumbing Engineer (PROPOSAL) | TBD |
| F-003 | F:evaluative:completeness | VerificationGap | Specification | Procedure | Add measurable acceptance criterion for pump-out access (REQ-010): specify minimum vehicle clearance, turning radius, or access road width to make "pump-out vehicle access route confirmed" verifiable | Thorough merit accounting lens reveals REQ-010 requires pump-out access provisions but neither the specification verification table nor the Procedure verification table defines measurable criteria for what constitutes adequate vehicle access. | Specification.md; Procedure.md | Verification — REQ-010; Verification (Procedure) — Pump-out access shown | — | Plumbing Engineer / Operations (PROPOSAL) | TBD |

---

## Matrix D — Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Definitive Governance Foundation | 1 | HAS_ITEMS | Conflict on removal vs relocation scope |
| D:normative:applying | normative | applying | Compulsory Proof Enactment | 0 | NO_ITEMS | Proof enactment (P.Eng. stamp, code compliance) covered |
| D:normative:judging | normative | judging | Definitive Conformance Verdict | 0 | NO_ITEMS | Conformance verdict pathway (Safety Codes Officer) stated |
| D:normative:reviewing | normative | reviewing | Binding Oversight Scrutiny | 0 | NO_ITEMS | Oversight (County review, AHJ inspection) addressed |
| D:operative:guiding | operative | guiding | Reliable Workflow Orientation | 1 | HAS_ITEMS | Workflow dependency sequencing weak |
| D:operative:applying | operative | applying | Definitive Implementation Competence | 0 | NO_ITEMS | Implementation competence covered by P.Eng. requirement |
| D:operative:judging | operative | judging | Definitive Capability Verdict | 0 | NO_ITEMS | Capability assessment covered in Procedure Step 4 |
| D:operative:reviewing | operative | reviewing | Definitive Operational Review | 0 | NO_ITEMS | Operational review via County approval step (Step 5) |
| D:evaluative:guiding | evaluative | guiding | Definitive Quality Aspiration | 0 | NO_ITEMS | Quality aspirations stated in Guidance purpose |
| D:evaluative:applying | evaluative | applying | Definitive Quality Realization | 0 | NO_ITEMS | Quality realization pathway adequate |
| D:evaluative:judging | evaluative | judging | Definitive Benefit Assessment | 1 | HAS_ITEMS | No lifecycle cost consideration |
| D:evaluative:reviewing | evaluative | reviewing | Definitive Excellence Scrutiny | 0 | NO_ITEMS | Excellence scrutiny covered through review process |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:guiding | Conflict | Multi | NA | Surface existing conflict: RFP section 3.4 parenthetical suggests relocation may be in scope; Decomposition D-002 explicitly resolves removal IN / relocation OUT. Guidance CONF-001 already identifies this. Confirm human ruling. | Definitive governance foundation lens confirms the only identified conflict between sources. This is already captured in Guidance Conflict Table as CONF-001 but HumanRuling remains TBD. | Guidance.md; Specification.md | Conflict Table — CONF-001 (Guidance); Excluded — relocation (Specification) | Guidance.md#Conflict Table (RFP section 3.4 parenthetical) vs. Specification.md#Excluded (Decomposition D-002) | Decomposition D-002 (PROPOSAL) | TBD |
| D-002 | D:operative:guiding | WeakStatement | Procedure | Procedure | Clarify prerequisite dependency sequencing: state explicitly which prerequisites are hard-blocks (must be complete before starting) vs. soft-dependencies (can proceed with noted TBD assumptions) | Reliable workflow orientation lens reveals the Procedure Prerequisites table lists 8 prerequisites but does not distinguish blocking from non-blocking dependencies. The geotech report (DEL-008-01) is acknowledged as "if not yet available, proceed with conservative assumptions" but other dependencies (e.g., Preliminary Civil Design, Drain & Vent Plans) have no such qualifier. | Procedure.md | Prerequisites | — | Plumbing Engineer / Project Manager (PROPOSAL) | TBD |
| D-003 | D:evaluative:judging | RationaleGap | Guidance | Guidance | Add lifecycle cost or operational cost consideration for the holding tank: pump-out frequency estimate, annual operating cost implication, and whether this was factored into the Owner's decision to specify a holding tank | Definitive benefit assessment lens reveals no lifecycle or operating cost information is present in any document. For a holding tank requiring periodic pump-out at a rural site, this is a material value consideration that informs whether the specified 2,000 gallon size is adequate. | Guidance.md | entire document scanned | — | Owner / Plumbing Engineer (PROPOSAL) | TBD |

---

## Matrix X — Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Leadership Guidance Prerequisite | 0 | NO_ITEMS | Leadership prerequisites (County approval, P.Eng.) stated |
| X:guiding:sufficiency | guiding | sufficiency | Leadership Validation Proficiency | 0 | NO_ITEMS | Validation pathways adequate |
| X:guiding:completeness | guiding | completeness | Exhaustive Leadership Scope | 0 | NO_ITEMS | Leadership scope covered |
| X:guiding:consistency | guiding | consistency | Steadfast Leadership Harmony | 0 | NO_ITEMS | Leadership direction consistent |
| X:applying:necessity | applying | necessity | Applied Execution Baseline | 1 | HAS_ITEMS | Tank material not specified |
| X:applying:sufficiency | applying | sufficiency | Applied Achievement Justification | 0 | NO_ITEMS | Achievement justification adequate |
| X:applying:completeness | applying | completeness | Exhaustive Execution Fulfillment | 0 | NO_ITEMS | Execution scope adequate for design deliverable |
| X:applying:consistency | applying | consistency | Dependable Execution Harmony | 0 | NO_ITEMS | Execution steps harmonized with specifications |
| X:judging:necessity | judging | necessity | Foundational Judgment Criterion | 0 | NO_ITEMS | Judgment criteria (code compliance, drawing review) established |
| X:judging:sufficiency | judging | sufficiency | Ruling Validation Proficiency | 1 | HAS_ITEMS | No hold/witness point for backfill |
| X:judging:completeness | judging | completeness | Exhaustive Ruling Scope | 0 | NO_ITEMS | Ruling scope adequate |
| X:judging:consistency | judging | consistency | Steadfast Ruling Dependability | 0 | NO_ITEMS | Ruling criteria consistent |
| X:reviewing:necessity | reviewing | necessity | Foundational Audit Criterion | 0 | NO_ITEMS | Audit criteria (P.Eng. stamp, permit) stated |
| X:reviewing:sufficiency | reviewing | sufficiency | Audit Validation Proficiency | 0 | NO_ITEMS | Validation proficiency adequate |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Audit Fulfillment | 0 | NO_ITEMS | Audit records list adequate |
| X:reviewing:consistency | reviewing | consistency | Dependable Audit Harmony | 0 | NO_ITEMS | Audit approach consistent across docs |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | MissingSlot | Datasheet | Datasheet | Add tank material specification or performance specification criteria (precast concrete, polyethylene, fibreglass) with selection rationale; currently listed only as a trade-off in Guidance | Applied execution baseline lens reveals that tank material is TBD in the Datasheet Construction table and listed as a trade-off in Guidance, but no attribute entry exists in the Datasheet Attributes section for tank material. This is an essential execution parameter. | Datasheet.md; Guidance.md | Construction (Datasheet); Trade-offs — Tank material (Guidance) | — | Plumbing Engineer (PROPOSAL) | TBD |
| X-002 | X:judging:sufficiency | MissingSlot | Procedure | Procedure | Add a hold point or witness point for tank installation inspection before backfill, referencing the testing requirement noted in Procedure Step 3.3 (water test) | Ruling validation proficiency lens reveals Procedure Step 3.3 mentions "Testing requirements before backfill (e.g., water test)" as an installation note but the Procedure verification table and Specification verification table do not include a specific hold point for pre-backfill inspection. This is standard practice for buried tank installations. | Procedure.md; Specification.md | Step 3 — 3.3; Verification (Procedure); Verification (Specification) | — | Plumbing Engineer / Inspector (PROPOSAL) | TBD |

---

## Matrix E — Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Reference Baseline | 1 | HAS_ITEMS | Normalization issue with Discipline naming |
| E:guiding:information | guiding | information | Authoritative Orientation Clarity | 0 | NO_ITEMS | Orientation clarity adequate |
| E:guiding:knowledge | guiding | knowledge | Comprehensive Governance Insight | 0 | NO_ITEMS | Governance insight adequate |
| E:guiding:wisdom | guiding | wisdom | Principled Governance Vision | 0 | NO_ITEMS | Governance vision adequate in Guidance |
| E:applying:data | applying | data | Dependable Execution Evidence | 1 | HAS_ITEMS | Invert elevation data missing |
| E:applying:information | applying | information | Applied Performance Clarity | 0 | NO_ITEMS | Performance clarity adequate |
| E:applying:knowledge | applying | knowledge | Applied Execution Expertise | 0 | NO_ITEMS | Expertise requirements clear |
| E:applying:wisdom | applying | wisdom | Principled Execution Judgment | 0 | NO_ITEMS | Execution judgment adequately guided |
| E:judging:data | judging | data | Authoritative Verdict Evidence | 0 | NO_ITEMS | Verdict evidence pathways stated |
| E:judging:information | judging | information | Comprehensive Verdict Clarity | 0 | NO_ITEMS | Verdict clarity adequate |
| E:judging:knowledge | judging | knowledge | Comprehensive Judgment Expertise | 0 | NO_ITEMS | Judgment expertise (P.Eng.) stated |
| E:judging:wisdom | judging | wisdom | Principled Verdict Sagacity | 0 | NO_ITEMS | Verdict sagacity covered via Guidance trade-offs |
| E:reviewing:data | reviewing | data | Comprehensive Inspection Evidence | 0 | NO_ITEMS | Inspection evidence requirements stated |
| E:reviewing:information | reviewing | information | Comprehensive Audit Clarity | 0 | NO_ITEMS | Audit clarity adequate |
| E:reviewing:knowledge | reviewing | knowledge | Comprehensive Audit Expertise | 0 | NO_ITEMS | Audit expertise requirements clear |
| E:reviewing:wisdom | reviewing | wisdom | Principled Audit Sagacity | 0 | NO_ITEMS | Audit sagacity adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | Normalization | Datasheet | Datasheet | Normalize discipline naming: _CONTEXT.md uses "Plumbing Engineer" as discipline; Datasheet uses "Plumbing Engineering." Align to one form across all deliverable files. | Authoritative reference baseline lens reveals a minor but actionable naming inconsistency between the context file and the Datasheet identification table for the discipline field. | _CONTEXT.md; Datasheet.md | (Discipline field in _CONTEXT.md); Identification — Discipline (Datasheet) | — | Project Manager (PROPOSAL) | TBD |
| E-002 | E:applying:data | TBD_Question | Specification | Datasheet | Record TBD: Capture building drain invert elevation at point of connection to septic tank, and tank inlet/outlet invert elevations, once coordination with DEL-006-03 is complete | Dependable execution evidence lens reveals that invert elevations are referenced in Procedure (Steps 3.2 and 4.3) and Guidance (coordination table) as coordination items with DEL-006-03, but no placeholder data entries exist in the Datasheet for these critical design parameters. | Datasheet.md; Procedure.md | Construction (Datasheet — Inlet/outlet connections TBD); Step 3 — 3.2 (Procedure) | — | Plumbing Engineer (PROPOSAL) | TBD |
