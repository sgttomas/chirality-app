# Semantic Lensing Register: DEL-012-02 Utility Room

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-012_Interior Construction & Fit-Out/1_Working/DEL-012-02_Utility-Room/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-012-02_Utility-Room/_CONTEXT.md (Deliverable Identity, Description, Scope, Key Requirements)
- _STATUS.md — DEL-012-02_Utility-Room/_STATUS.md (Current Status: SEMANTIC_READY)
- _SEMANTIC.md — DEL-012-02_Utility-Room/_SEMANTIC.md (Matrices A, B, C, F, D, X, E fully parsed)
- Datasheet.md — DEL-012-02_Utility-Room/Datasheet.md (Identification, Attributes, Conditions, Construction, References)
- Specification.md — DEL-012-02_Utility-Room/Specification.md (Scope, Requirements REQ-012-02-001 through REQ-012-02-013, Standards, Verification, Documentation)
- Guidance.md — DEL-012-02_Utility-Room/Guidance.md (Purpose, Principles P1-P5, Considerations C1-C6, Trade-offs T1-T3)
- Procedure.md — DEL-012-02_Utility-Room/Procedure.md (Steps 1-9, Prerequisites, Verification, Records)
- _REFERENCES.md — DEL-012-02_Utility-Room/_REFERENCES.md (Primary References, Related Documentation, Drawing References, Standard References, Approval Documents)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 6
  - Specification: 10
  - Guidance: 4
  - Procedure: 4
  - Multi: 4
- By matrix:
  - A: 4  B: 3  C: 3  F: 5  D: 3  X: 6  E: 4
- By type:
  - Conflict: 3
  - VerificationGap: 5
  - MissingSlot: 7
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 2
  - TBD_Question: 4
  - MatrixError: 0
- Notable conflicts: 3
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Standards table lacks clause-level specificity |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Finish specifications use weak language |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Code compliance verification relies on assumptions |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Inspection requirements consistently documented across Specification and Procedure |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Steps 1-9 provide clear sequencing direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Fire rating / fire separation not addressed |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification table in Specification covers all requirements |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Procedure includes rough-in and final inspection stages |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Principles P1-P5 establish clear value hierarchy |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs T1-T3 address key merit decisions |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Guidance adequately positions utility room value proposition |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Verification and closeout adequately covered |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Strengthen Standards table: replace ASSUMPTION entries with confirmed code citations or explicit TBD markers with responsible party for resolution | The Standards table in Specification lists 4 of 7 entries as "ASSUMPTION: likely applicable" without confirmed applicability. Under prescriptive direction, these must either be confirmed or formally tracked as open items with a resolution owner. | Specification.md | Standards | — | Design team to confirm code applicability at design stage | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Clarify REQ-012-02-003: define "appropriate for a mechanical equipment environment" with measurable criteria (e.g., moisture resistance rating, abrasion class, cleanability standard) or reference a finish schedule submittal | REQ-012-02-003 uses "appropriate for a mechanical equipment environment" which is not a testable criterion. Mandatory practice requires specificity sufficient for compliance determination. | Specification.md | REQ-012-02-003 | — | Design team to define finish performance criteria | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add verification method for National Fire Code applicability (Standards table entry); add explicit hold-point or verification step for fire safety compliance if applicable | Standards table references National Fire Code as "ASSUMPTION — location TBD" but no corresponding verification method exists. If National Fire Code applies to this equipment room, compliance determination requires a verification pathway. | Specification.md | Standards; Verification | — | AHJ to confirm NFC applicability | TBD |
| A-004 | A:operative:applying | MissingSlot | Multi | Specification | Add requirement or consideration for fire rating / fire separation of utility room walls. Confirm whether utility room (as mechanical equipment host) requires fire-rated separation from adjacent spaces under Alberta Building Code or NFC. | No document addresses fire rating of utility room partitions. Datasheet describes walls as "non-structural interior partitions" and Specification scope includes "interior partition walls, openings, blocking" but neither specifies fire rating. For a room hosting mechanical equipment, heating systems, and potentially gas-fired units, fire separation is a standard code consideration. | Specification.md; Datasheet.md; Guidance.md | Specification: REQ-012-02-001, Scope; Datasheet: Construction; Guidance: C6 | — | Design team + AHJ | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Room dimensions TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Source references adequate for current stage |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Datasheet missing door specification data |
| B:data:consistency | data | consistency | reliable measurement | 1 | HAS_ITEMS | Ceiling height inconsistency |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key dependency signals documented in _DEPENDENCIES and Procedure prerequisites |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequately established across documents |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Cross-document narrative is comprehensive for current stage |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Documents tell a coherent story about utility room purpose and sequencing |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Core knowledge of the deliverable is established |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise requirements implied through coordination steps |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Adequate for current stage |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is consistent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Key trade-off discernments documented in Guidance T1-T3 |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment adequacy addressed through human-ruling conflict table |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view captured in Guidance Purpose and Principles |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record explicit TBD for utility room floor dimensions (length x width) with resolution path: "Design team to confirm from IFC drawings; 16' bay width is ASSUMPTION only" | Room footprint is listed as "TBD (design to be determined)" in Datasheet. This is an essential fact for all downstream construction and equipment coordination. While acknowledged as TBD, the Datasheet should record the resolution path more explicitly. | Datasheet.md | Attributes > Spatial Attributes | — | Design team | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add door specification data: count, size, type, fire rating (if applicable), swing direction. Currently only mentioned as "Access door(s) required" without any parameter data. | Datasheet Construction table mentions "Access door(s) required for maintenance and service" but provides no parameter data (count, size, type, rating, swing). Procedure Step 3.4 references door width needing to accommodate largest equipment item but no baseline data exists. | Datasheet.md; Procedure.md | Datasheet: Construction; Procedure: Step 3 | — | Design team | TBD |
| B-003 | B:data:consistency | Conflict | Multi | Datasheet | Resolve ceiling height: Datasheet says "35' (concrete structure)" for overall building with utility room ceiling "TBD (may be lower if mezzanine above)." Confirm whether the mezzanine deck is the effective ceiling, and record the actual utility room ceiling height. | Datasheet records building ceiling height as 35' but notes utility room ceiling height is TBD because of the mezzanine above. Specification REQ-012-02-007 addresses mezzanine interface but no document states the actual clear height of the utility room below the mezzanine. This measurement is critical for equipment clearance and ventilation design. | Datasheet.md; Specification.md | Datasheet: Attributes > Spatial Attributes (Ceiling height, Mezzanine above); Specification: REQ-012-02-007 | Datasheet.md#Attributes (35' building height, TBD room height) vs. absence of actual room height in any doc | Design team + Structural Engineer | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Threshold Awareness | 1 | HAS_ITEMS | Ventilation "adequate" is not enforceable |
| C:normative:sufficiency | normative | sufficiency | Warranted Conformance Scope | 0 | NO_ITEMS | Conformance scope adequately bounded by Specification Scope section |
| C:normative:completeness | normative | completeness | Mandated Regulatory Closure | 1 | HAS_ITEMS | No evidence of gas code applicability assessment |
| C:normative:consistency | normative | consistency | Invariant Compliance Benchmark | 0 | NO_ITEMS | Compliance benchmarks consistent where specified |
| C:operative:necessity | operative | necessity | Operational Readiness Threshold | 0 | NO_ITEMS | Prerequisites in Procedure clearly define readiness threshold |
| C:operative:sufficiency | operative | sufficiency | Verified Functional Capability | 0 | NO_ITEMS | Verification table and procedure verification steps align |
| C:operative:completeness | operative | completeness | Exhaustive Workflow Integration | 1 | HAS_ITEMS | Material procurement step missing |
| C:operative:consistency | operative | consistency | Repeatable Disciplined Execution | 0 | NO_ITEMS | Procedure steps are sequenced consistently |
| C:evaluative:necessity | evaluative | necessity | Foundational Value Criterion | 0 | NO_ITEMS | Value criteria established through Guidance principles |
| C:evaluative:sufficiency | evaluative | sufficiency | Balanced Evidenced Appraisal | 0 | NO_ITEMS | Trade-offs adequately balanced |
| C:evaluative:completeness | evaluative | completeness | Thorough Holistic Appraisal | 0 | NO_ITEMS | Holistic appraisal covered |
| C:evaluative:consistency | evaluative | consistency | Coherent Value Integrity | 0 | NO_ITEMS | Value reasoning consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Strengthen REQ-012-02-010: replace "adequately ventilated" with a measurable threshold or reference to a ventilation standard (e.g., minimum air changes per hour, or reference to mechanical engineer's design calculation) | REQ-012-02-010 states the utility room "shall be adequately ventilated" but "adequately" is not an enforceable threshold. For a room housing mechanical equipment that generates heat and may require combustion air, the ventilation requirement needs to be either quantified or tied to a design calculation by a qualified engineer. | Specification.md | REQ-012-02-010 | — | Mechanical engineer (PKG-013) to define ventilation requirements | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add consideration for Alberta Gas Safety Code applicability if any PKG-013 equipment is gas-fired. Record as TBD with resolution path: "Confirm fuel type for heating system (PKG-013) to determine gas code applicability." | Specification Standards table lists Alberta Safety Codes generally and references Electrical, Gas, Plumbing, and Fire in Procedure Step 2.2, but the Specification does not address whether gas-fired equipment will be present. If the heating unit (PKG-013 DEL-013-01) is gas-fired, the utility room construction must accommodate gas code requirements (combustion air, flue penetrations, gas line routing provisions). This is a regulatory closure gap. | Specification.md; Procedure.md | Specification: Standards; Procedure: Step 2.2 | — | PKG-013 equipment selection to determine | TBD |
| C-003 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add a material procurement and submittal step between Step 2 (Permits) and Step 3 (Partition Construction). Should cover: finish material procurement, access door procurement, equipment platform materials, in coordination with design coordination outputs from Step 1. | Procedure jumps from Step 2 (Permits) to Step 3 (Partition Construction) without a material procurement/submittal approval step. For exhaustive workflow integration, the procurement of interior finish materials, access doors, and equipment platform components should be explicitly sequenced. | Procedure.md | Steps (between Step 2 and Step 3) | — | GC scheduling | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Statutory Obligation Floor | 1 | HAS_ITEMS | Accessibility code specifics missing |
| F:normative:sufficiency | normative | sufficiency | Demonstrable Compliant Standard | 1 | HAS_ITEMS | Finish schedule not yet referenced |
| F:normative:completeness | normative | completeness | Exhaustive Mandate Authority | 0 | NO_ITEMS | Mandate authority adequately established through RFP and code references |
| F:normative:consistency | normative | consistency | Harmonized Standard Discipline | 1 | HAS_ITEMS | Standard references inconsistent between docs |
| F:operative:necessity | operative | necessity | Operational Fitness Signal | 0 | NO_ITEMS | Fitness signals defined through hold-points and prerequisites |
| F:operative:sufficiency | operative | sufficiency | Demonstrated Capable Preparedness | 0 | NO_ITEMS | Preparedness addressed through prerequisite table |
| F:operative:completeness | operative | completeness | Total Procedural Inventory | 1 | HAS_ITEMS | Deficiency resolution procedure incomplete |
| F:operative:consistency | operative | consistency | Dependable Workflow Coherence | 0 | NO_ITEMS | Workflow is coherent between Specification verification and Procedure steps |
| F:evaluative:necessity | evaluative | necessity | Intrinsic Merit Foundation | 0 | NO_ITEMS | Merit foundation established in Guidance |
| F:evaluative:sufficiency | evaluative | sufficiency | Defensible Authoritative Verdict | 0 | NO_ITEMS | Decision framework adequate for current stage |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Assessment Census | 1 | HAS_ITEMS | Warranty scope for utility room not particularized |
| F:evaluative:consistency | evaluative | consistency | Grounded Merit Alignment | 0 | NO_ITEMS | Merit alignment consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | TBD_Question | Specification | Specification | Confirm whether Alberta Building Code accessibility requirements (barrier-free access) apply to the utility room. If so, add requirement for door width, threshold, and clearance compliance. Record TBD: "Confirm ABC barrier-free access applicability to mechanical equipment rooms." | REQ-012-02-005 addresses "service accessibility" for maintenance but does not address building code accessibility requirements (barrier-free design). The statutory obligation floor for a public-authority-owned building may include accessibility provisions even for service rooms. | Specification.md | REQ-012-02-005; Standards | — | Design team + AHJ | TBD |
| F-002 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add verification step for finish schedule submittal: require GC to submit finish schedule for review and approval before procurement. Currently verification says "Finish schedule review; site inspection" but no submittal requirement exists in Procedure or Specification. | REQ-012-02-003 verification method references "Finish schedule review" but no requirement exists for the GC to submit a finish schedule for approval. Without a formal submittal step, the verification method has no trigger. | Specification.md; Procedure.md | Specification: Verification (REQ-012-02-003); Procedure: entire document scanned | — | GC submittal to County PM | TBD |
| F-003 | F:normative:consistency | Normalization | Multi | Guidance | Harmonize standard references across documents. _REFERENCES.md lists "Local building codes" and "HVAC and electrical safety standards" generically; Specification lists specific codes (Alberta Safety Codes Act, Alberta Building Code, CCDC 14-2013, NFC); Datasheet references "Alberta Safety Codes and applicable building codes." Align to a single canonical list. | Standard references are inconsistent in specificity across documents. Datasheet uses general language, Specification provides specific act names, _REFERENCES.md uses generic terms ("Local building codes"). This terminological inconsistency risks drift in what codes are understood to apply. | Specification.md; Datasheet.md; _REFERENCES.md | Specification: Standards; Datasheet: Conditions (Code compliance); _REFERENCES.md: Standard References | Specification.md#Standards vs. Datasheet.md#Conditions vs. _REFERENCES.md#Standard References | Specification should be canonical; other docs should align | TBD |
| F-004 | F:operative:completeness | MissingSlot | Procedure | Procedure | Add deficiency resolution subprocess: define what happens when inspections (Step 6 or Step 9) identify deficiencies. Step 9.4 mentions resolving within 10 days per RFP but Step 6.3 only says "Resolve any inspection deficiencies before proceeding" without a defined process (who decides, who approves, how re-inspection is triggered). | Procedure Step 6.3 and Step 9.4 address deficiency resolution differently. Step 9.4 cites the 10-day resolution requirement from RFP 2.10.6, but Step 6.3 has no timeline or process detail. For total procedural inventory, deficiency resolution at rough-in stage should have equivalent procedural clarity. | Procedure.md | Step 6.3; Step 9.4 | — | GC + County PM | TBD |
| F-005 | F:evaluative:completeness | TBD_Question | Guidance | Guidance | Add consideration for warranty scope particularization: what elements of the utility room construction are covered by the 2-year warranty? Does warranty extend to equipment platforms, finishes, access doors, and penetration sealing? Record TBD: "Confirm warranty coverage scope for PKG-012 utility room elements." | Datasheet Conditions lists "2 years post-CCC" warranty and Procedure Records lists "Warranty Documentation" but no document clarifies what specific utility room elements the warranty covers. For a comprehensive assessment census, the warranty boundary should be understood (especially for elements like equipment platforms that interface with PKG-013). | Datasheet.md; Procedure.md; Guidance.md | Datasheet: Conditions (Warranty period); Procedure: Records (Warranty Documentation); Guidance: entire document scanned | — | Contract interpretation (CCDC 14-2013) | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Codified Directive Foundation | 0 | NO_ITEMS | Directive foundation established through RFP and code references |
| D:normative:applying | normative | applying | Obligatory Verified Method | 1 | HAS_ITEMS | REQ-012-02-005 clearances not verifiable at current stage |
| D:normative:judging | normative | judging | Conclusive Conformance Authority | 0 | NO_ITEMS | Conformance authority established through AHJ inspection framework |
| D:normative:reviewing | normative | reviewing | Settled Mandated Inspection | 0 | NO_ITEMS | Inspection points defined in both Specification and Procedure |
| D:operative:guiding | operative | guiding | Confirmed Workflow Course | 0 | NO_ITEMS | Workflow course confirmed through 9-step procedure |
| D:operative:applying | operative | applying | Verified Construction Delivery | 1 | HAS_ITEMS | Cistern pad scope boundary unresolved |
| D:operative:judging | operative | judging | Conclusive Capability Verdict | 0 | NO_ITEMS | Capability verdict pathway defined through verification table |
| D:operative:reviewing | operative | reviewing | Confirmed Workflow Scrutiny | 0 | NO_ITEMS | Scrutiny points defined at rough-in and final inspection |
| D:evaluative:guiding | evaluative | guiding | Grounded Purposeful Direction | 0 | NO_ITEMS | Purpose well grounded in Guidance |
| D:evaluative:applying | evaluative | applying | Conclusive Benefit Realization | 0 | NO_ITEMS | Benefit realization pathway clear through equipment enablement |
| D:evaluative:judging | evaluative | judging | Final Value Adjudication | 1 | HAS_ITEMS | Acceptance criteria for "room ready for downstream trades" not formalized |
| D:evaluative:reviewing | evaluative | reviewing | Resolved Merit Inspection | 0 | NO_ITEMS | Merit inspection addressed through CCC process |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | VerificationGap | Specification | Specification | Add interim verification method for REQ-012-02-005 (service clearances): require GC to submit clearance verification against equipment submittals at design stage, not only at final inspection. Current verification is "Design review against equipment footprints; site inspection" but equipment footprints are TBD. | REQ-012-02-005 verification states "Design review against equipment footprints" but equipment footprints are TBD (PKG-013 equipment not yet selected). The obligatory verified method cannot be demonstrated until equipment submittals are received. An interim verification step should require sign-off that equipment submittals have been received and clearances checked before construction proceeds. | Specification.md | REQ-012-02-005; Verification | — | GC + PKG-013 | TBD |
| D-002 | D:operative:applying | Conflict | Multi | Guidance | Resolve CON-012-02-02 (already documented in Guidance Conflict Table): cistern structural pad responsibility is ambiguous between PKG-012 and PKG-014. This conflict blocks verified construction delivery for the cistern housing requirement. | Guidance Conflict Table already identifies CON-012-02-02 (cistern pad scope boundary). Under the verified construction delivery lens, this is a blocking ambiguity: the GC cannot construct a cistern pad without knowing whether it is in PKG-012 scope. The conflict requires human ruling before design coordination can proceed. | Specification.md; Guidance.md | Specification: Scope, REQ-012-02-008; Guidance: Conflict Table CON-012-02-02 | Specification.md#Scope (cistern housing in scope) vs. PKG-014 scope (cistern installation) | PROPOSAL: PKG-012 provides structural pad; PKG-014 installs cistern | TBD |
| D-003 | D:evaluative:judging | VerificationGap | Procedure | Specification | Add formal acceptance criteria for "utility room ready for downstream trades" — define a punch-list or readiness checklist that PKG-013, PKG-014, and PKG-015 must sign off on before commencing their equipment installation. Currently Step 8.4 says "Confirm all items within PKG-012 scope are complete" without specifying what constitutes completion. | The final value adjudication for this deliverable is whether the utility room is ready for downstream package installation. Procedure Step 8.4 references completion confirmation but provides no formal acceptance criteria or checklist. Without a defined readiness standard, different parties may disagree on whether the room is "ready." | Procedure.md; Specification.md | Procedure: Step 8.4; Specification: Verification (entire table) | — | GC + PKG-013/014/015 contractors + County PM | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Initiating Regulatory Imperative | 1 | HAS_ITEMS | Building permit timing not specified |
| X:guiding:sufficiency | guiding | sufficiency | Competent Evidenced Navigation | 0 | NO_ITEMS | Evidence navigation adequate through reference framework |
| X:guiding:completeness | guiding | completeness | Exhaustive Governance Authority | 0 | NO_ITEMS | Governance authority chain established (Owner > GC > AHJ) |
| X:guiding:consistency | guiding | consistency | Harmonized Governance Steering | 0 | NO_ITEMS | Governance steering consistent across docs |
| X:applying:necessity | applying | necessity | Mandatory Execution Basis | 1 | HAS_ITEMS | IFC drawing dependency not formalized as hold-point |
| X:applying:sufficiency | applying | sufficiency | Validated Contextual Technique | 0 | NO_ITEMS | Technique validation addressed through submittal review |
| X:applying:completeness | applying | completeness | Comprehensive Delivery Record | 1 | HAS_ITEMS | As-built requirement not specific enough |
| X:applying:consistency | applying | consistency | Coherent Stable Execution | 0 | NO_ITEMS | Execution steps internally coherent |
| X:judging:necessity | judging | necessity | Binding Fitness Determination | 1 | HAS_ITEMS | P.Eng. stamp verification not in Procedure |
| X:judging:sufficiency | judging | sufficiency | Validated Authoritative Verdict | 0 | NO_ITEMS | Verdict validation through AHJ inspection is adequate |
| X:judging:completeness | judging | completeness | Exhaustive Ruling Record | 1 | HAS_ITEMS | Inspection records custody chain incomplete |
| X:judging:consistency | judging | consistency | Harmonized Compliance Measure | 0 | NO_ITEMS | Compliance measures consistent |
| X:reviewing:necessity | reviewing | necessity | Critical Diagnostic Initiation | 0 | NO_ITEMS | Diagnostic initiation points (hold-points) defined |
| X:reviewing:sufficiency | reviewing | sufficiency | Verified Contextual Assessment | 0 | NO_ITEMS | Assessment context adequate |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Audit Authority | 1 | HAS_ITEMS | Photographic record not mentioned |
| X:reviewing:consistency | reviewing | consistency | Harmonized Audit Coherence | 0 | NO_ITEMS | Audit coherence adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:necessity | MissingSlot | Procedure | Procedure | Add timing requirement for building permit acquisition relative to construction start. Step 2 covers permits but does not specify lead time or that permit must be in hand before Step 3 commences (only implied by sequencing). Make hold-point explicit. | Procedure Step 2 covers permit acquisition but the initiating regulatory imperative — that the building permit must be obtained before construction begins — is not stated as a formal hold-point. Step 3.1 references PKG-011 shell completion hold-point but not building permit hold-point. | Procedure.md | Step 2; Step 3 | — | GC | TBD |
| X-002 | X:applying:necessity | VerificationGap | Specification | Procedure | Add formal hold-point in Procedure: "IFC drawings must be P.Eng.-stamped, approved, and issued before any utility room construction work begins." Currently stated as a prerequisite but not as a verification hold-point with sign-off. | Datasheet Construction table states "IFC Drawings required... P.Eng.-stamped; issued for construction before construction begins" and Specification REQ-012-02-002 requires P.Eng. stamp. However, Procedure prerequisites list this as "Approved" without a formal hold-point sign-off step. The mandatory execution basis requires a verifiable gate. | Datasheet.md; Specification.md; Procedure.md | Datasheet: Construction (IFC Drawings required); Specification: REQ-012-02-002; Procedure: Prerequisites | — | GC + Design team | TBD |
| X-003 | X:applying:completeness | WeakStatement | Specification | Specification | Strengthen Documentation table entry for "As-Built Survey": specify what must be documented (room dimensions, equipment platform locations, penetration locations, rough-in positions, deviations from IFC). Currently just says "Survey and documentation of completed construction." | Specification Documentation table lists "As-Built Survey" as "Survey and documentation of completed construction" which is insufficiently specific for a comprehensive delivery record. An as-built should capture dimensional verification, penetration as-built locations, and deviations from IFC. | Specification.md | Documentation | — | GC | TBD |
| X-004 | X:judging:necessity | MissingSlot | Procedure | Procedure | Add explicit P.Eng. stamp verification step: verify that IFC drawings bear a valid P.Eng. stamp before construction commences. This is mentioned in Specification REQ-012-02-002 verification but not implemented as a Procedure step. | Specification REQ-012-02-002 verification method includes "P.Eng. stamp on IFC drawings" but Procedure does not include a step to verify the P.Eng. stamp. The binding fitness determination for code compliance requires this verification to be proceduralized. | Specification.md; Procedure.md | Specification: Verification (REQ-012-02-002); Procedure: Step 1 | — | GC + County PM | TBD |
| X-005 | X:judging:completeness | RationaleGap | Procedure | Procedure | Add custody chain for inspection records: specify that rough-in inspection reports (Step 6) must be retained in the project file and copies provided to County PM. Step 6.2 says "provide copies" but Records table lists "Inspection Reports (Rough-In)" without specifying retention requirements or filing protocol. | Procedure Step 6.2 says copies go to County PM, and Records table lists rough-in inspection reports, but the exhaustive ruling record lens reveals no retention period, filing protocol, or chain-of-custody requirement. For audit purposes, these records need clearer specification. | Procedure.md | Step 6; Records | — | GC + County PM | TBD |
| X-006 | X:reviewing:completeness | RationaleGap | Procedure | Procedure | Add requirement for photographic documentation at key stages (rough-in before concrete, penetrations before close-up, equipment platforms before PKG-013 installation). This supports audit trail for elements that become concealed. | No document mentions photographic documentation of construction stages. For a utility room where rough-ins and structural provisions will be concealed by finishes and equipment, photographic records at key stages are standard practice for audit authority. This is an absence, not a conflict. | Procedure.md | entire document scanned | — | GC | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Evidenced Directive Benchmark | 0 | NO_ITEMS | Directive benchmarks adequately evidenced through RFP citations |
| E:guiding:information | guiding | information | Coherent Authority Briefing | 0 | NO_ITEMS | Authority briefing coherent across docs |
| E:guiding:knowledge | guiding | knowledge | Authoritative Strategic Stewardship | 1 | HAS_ITEMS | Long-term serviceability not addressed |
| E:guiding:wisdom | guiding | wisdom | Principled Strategic Foresight | 0 | NO_ITEMS | Strategic foresight captured in Guidance trade-offs and principles |
| E:applying:data | applying | data | Validated Build Record | 1 | HAS_ITEMS | Submittal tracking not structured |
| E:applying:information | applying | information | Coordinated Delivery Status | 0 | NO_ITEMS | Delivery status coordination covered through milestone tracking |
| E:applying:knowledge | applying | knowledge | Proficient Craft Authority | 0 | NO_ITEMS | Craft authority established through P.Eng. stamp and GC role |
| E:applying:wisdom | applying | wisdom | Principled Craft Wisdom | 0 | NO_ITEMS | Craft wisdom addressed through trade-offs |
| E:judging:data | judging | data | Demonstrated Conformance Record | 1 | HAS_ITEMS | Penetration sealing verification missing |
| E:judging:information | judging | information | Coherent Ruling Briefing | 0 | NO_ITEMS | Ruling briefing coherent through conflict table |
| E:judging:knowledge | judging | knowledge | Authoritative Diagnostic Mastery | 0 | NO_ITEMS | Diagnostic authority established through AHJ + P.Eng. framework |
| E:judging:wisdom | judging | wisdom | Principled Holistic Verdict | 0 | NO_ITEMS | Holistic verdict pathway established through CCC process |
| E:reviewing:data | reviewing | data | Verified Inspection Finding | 0 | NO_ITEMS | Inspection findings pathway defined |
| E:reviewing:information | reviewing | information | Coherent Audit Briefing | 0 | NO_ITEMS | Audit briefing coherent |
| E:reviewing:knowledge | reviewing | knowledge | Authoritative Scrutiny Mastery | 1 | HAS_ITEMS | County PM inspection competence assumed |
| E:reviewing:wisdom | reviewing | wisdom | Principled Scrutiny Foresight | 0 | NO_ITEMS | Scrutiny foresight adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:knowledge | RationaleGap | Guidance | Guidance | Add consideration for long-term serviceability: address how the utility room design should accommodate future equipment replacement or upgrade. P5 mentions "equipment replacement" but does not address structural provisions (e.g., knock-out panels, rigging points, equipment access paths wider than initial installation needs). | Guidance P5 mentions service access for "ongoing maintenance activities including equipment replacement" but provides no design guidance for how equipment replacement is physically achieved (rigging points, removable wall sections, equipment access corridors). Authoritative strategic stewardship requires addressing the full lifecycle, not just initial installation. | Guidance.md | P5 — Accessibility is an Ongoing Operational Requirement | — | Design team | TBD |
| E-002 | E:applying:data | Normalization | Multi | Specification | Standardize submittal tracking: create a consolidated submittal register or log requirement. Currently submittals are referenced across Specification (Documentation table), Procedure (Step 1 outputs, Step 7), and Records table, but with different terminology and no unified tracking mechanism. | Specification Documentation table lists "Equipment Coordination Records," Procedure Step 1 output lists "equipment coordination records; scope demarcation agreements," and Records table lists "Equipment Coordination Records" with different descriptions. There is no unified submittal register that tracks all required submittals (finish schedule, equipment submittals, coordination records) in one place. | Specification.md; Procedure.md | Specification: Documentation; Procedure: Step 1 Output, Records | — | GC | TBD |
| E-003 | E:judging:data | VerificationGap | Specification | Specification | Add verification requirement for penetration sealing / fire-stopping after PKG-013/014/015 installations. REQ-012-02-010 addresses ventilation penetration coordination but no requirement or verification exists for confirming penetrations are properly sealed after MEP installations pass through them. | Specification REQ-012-02-010 and Procedure Step 5.5 reference fire-stopping "if required by code" but no verification step confirms that penetrations are properly sealed after downstream trade installations. The demonstrated conformance record is incomplete without post-installation penetration verification. | Specification.md; Procedure.md | Specification: REQ-012-02-010, Verification; Procedure: Step 5.5 | — | GC + AHJ | TBD |
| E-004 | E:reviewing:knowledge | TBD_Question | Guidance | Guidance | Clarify who performs the County PM inspection role and what qualifications are expected. RFP 3.3.2 requires County representative presence at all inspections but documents do not address competence requirements for the County representative. Record TBD: "Confirm County PM inspection authority and qualifications." | Multiple documents reference "County PM" or "County project representative" as an inspection party but no document establishes what authority or competence this person has. Under the authoritative scrutiny mastery lens, the inspection framework assumes a competent County representative without defining the role. | Procedure.md; Specification.md | Procedure: Step 6, Step 9; Specification: Verification (Party column) | — | Camrose County | TBD |

---

## Intermediate Matrices (K, G, T) -- Coverage Confirmation

Note: Matrices K (Transpose of D), G (Truncation of B), and T (Transpose of B) are intermediate construction matrices used to derive X and E. Per the protocol, the seven primary matrices for lensing are A, B, C, F, D, X, and E. Matrices K, G, and T are structural intermediates whose semantic content is fully captured through their parent and derived matrices. All cells of K, G, and T are semantically represented in the lensing of D, B, X, and E respectively. No additional warranted items arise from separate lensing of these intermediates.

---

## QA Verification

| Check | Result |
|---|---|
| Coverage complete | YES -- All 96 cells across matrices A (12), B (16), C (12), F (12), D (12), X (16), E (16) have Lens Coverage entries |
| No invention | YES -- All warranted items grounded in document evidence or explicit absence |
| Provenance present | YES -- Every item has SourcePath + SectionRef |
| Conflicts surfaced | YES -- 3 conflicts (B-003, D-002, F-003) have Contenders and HumanRuling = TBD |
| Summary consistent | YES -- Total items (28) = sum by matrix (4+3+3+5+3+6+4) = sum by type (3+5+7+4+3+2+4+0) |
| Schema followed | YES -- Output uses STRUCTURE schema |
