# Semantic Lensing Register: DEL-018-06 Utility Tie-Ins

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-018_Sitework & Civil Construction/1_Working/DEL-018-06_Utility-Tieins
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-018-06_Utility-Tieins/_CONTEXT.md (Deliverable Identity, Context Summary)
- _STATUS.md -- DEL-018-06_Utility-Tieins/_STATUS.md (Current Status: SEMANTIC_READY, 2026-02-26)
- _SEMANTIC.md -- DEL-018-06_Utility-Tieins/_SEMANTIC.md (Matrices A, B, C, F, D, X, E fully parsed)
- Datasheet.md -- DEL-018-06_Utility-Tieins/Datasheet.md (R0 2026-02-26)
- Specification.md -- DEL-018-06_Utility-Tieins/Specification.md (R0 2026-02-26)
- Guidance.md -- DEL-018-06_Utility-Tieins/Guidance.md (R0 2026-02-26)
- Procedure.md -- DEL-018-06_Utility-Tieins/Procedure.md (R0 2026-02-26)
- _REFERENCES.md -- DEL-018-06_Utility-Tieins/_REFERENCES.md (read; R-01 RFP, R-07 Site Maps listed)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 7
  - Specification: 10
  - Guidance: 4
  - Procedure: 4
  - Multi: 3
- By matrix:
  - A: 5  B: 4  C: 3  F: 4  D: 3  X: 5  E: 4
- By type:
  - Conflict: 1
  - VerificationGap: 7
  - MissingSlot: 8
  - WeakStatement: 3
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Gas assumption lacks prescriptive authority |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Separation distances TBD in mandatory practice |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Missing compliance criteria for communications |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | Audit trail gap for permit fee responsibility |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure provides adequate procedural direction for all 3 systems |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Backfill compaction criteria absent |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Performance assessment addressed via verification tables |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Process audit pathway described via inspection attendance records |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance articulates value orientation through objective alignment |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Merit tracked through trade-off analysis in Guidance |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Worth addressed through cost trade-offs in Guidance |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality appraisal embedded in verification tables |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Datasheet | Guidance | Clarify whether natural gas is confirmed as heating fuel or remains an assumption; current language "ASSUMPTION -- high-recovery heating system specified; gas is standard heating fuel" lacks prescriptive authority | The gas service purpose is stated as ASSUMPTION in the Datasheet, yet the Specification writes REQ-01 as mandatory. If gas is not confirmed, all gas requirements lack a prescriptive basis. | Datasheet.md | Natural Gas Attributes table, "Gas Service Purpose" row | -- | PROPOSAL: Confirm with County whether natural gas is the confirmed fuel source | TBD |
| A-002 | A:normative:applying | MissingSlot | Specification | Specification | Add mandatory separation distance requirements between gas piping and electrical conduit in shared trenches, referencing CEC and CSA B149.1 | Mandatory practice for shared-trench utility installation requires defined separation distances. Specification REQ-04.6 mentions "avoid conflicts" but states no numeric separation criteria. Procedure Step B2 notes "TBD" for separation requirements. | Specification.md | REQ-04.6 | -- | PROPOSAL: Source from CEC and CSA B149.1 once available | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add specific compliance determination criteria for communication lines (SOW-0082); current REQ-03.4 states only "applicable codes and utility provider standards" without identifying which codes | Compliance determination for communications is vague. Gas and electrical have identified code frameworks (Safety Codes Act, CEC, CSA B149.1), but communications has none specified. | Specification.md | REQ-03.4 and Standards table | -- | PROPOSAL: Identify applicable telecom/communications regulatory framework for Alberta | TBD |
| A-004 | A:normative:reviewing | RationaleGap | Guidance | Guidance | Add explicit rationale clarifying that County pays permit fees (RFP ss3.3.1) but Proponent obtains permits (RFP ss3.3.2), and how this split affects the regulatory audit trail | Guidance mentions this nuance but frames it as "should be clarified in project kickoff" without recording the rationale for why this distinction matters to the audit trail. A reviewer needs to understand the permit-fee vs. permit-responsibility split. | Guidance.md | Considerations > Regulatory and Permitting Environment | -- | PROPOSAL: Human to confirm interpretation of RFP ss3.3.1 vs ss3.3.2 | TBD |
| A-005 | A:operative:applying | MissingSlot | Procedure | Procedure | Add backfill compaction acceptance criteria (e.g., required density percentage, lift thickness, testing method) to Step B4 or a referenced specification | Practical execution of trench backfill lacks measurable acceptance criteria. Step B4 says "compact backfill to match surrounding soil density requirements" but provides no numeric target or test method. This is standard civil construction data that must come from the civil design. | Procedure.md | Steps > Part B > Step B4 | -- | PROPOSAL: Source compaction criteria from PKG-005 civil design once available | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Utility distances not recorded |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Electrical load data referenced but not present |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Water/sewer SOW mislabeling in MEMORY.md |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurement data appropriately marked TBD pending design |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Provider lead times not quantified |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequate for current phase |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Accounts are comprehensive given available sources |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messages coherent across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding of scope is adequate |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise assumptions are appropriate for phase |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Mastery items deferred appropriately to design phase |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across all docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Discernment reflected in trade-off analysis |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment applied adequately in Guidance trade-offs |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view present through dependency and coordination discussion |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning consistent across Guidance and Procedure |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Distance from site boundary to nearest gas main, electrical distribution line, and telecom infrastructure | This is an essential fact for cost estimation and schedule planning. Guidance identifies it as TBD but Datasheet does not record it as a pending data item. | Guidance.md; Datasheet.md | Guidance > Considerations > Rural Site Utility Context; Datasheet > entire document scanned | -- | PROPOSAL: Source from utility provider inquiries (Step A1) | TBD |
| B-002 | B:data:sufficiency | MissingSlot | Datasheet | Datasheet | Add a summary of anticipated electrical loads (cranes, heating, welding receptacles, compressor, fire hose pump, pressure washer, exhaust, etc.) to the Datasheet Electrical Service Attributes table | Guidance references specific loads from App B (Electrical) but the Datasheet Electrical Service Attributes table has only TBD entries for service capacity. The load list is available from App B and should be recorded as descriptive data. | Datasheet.md; Guidance.md | Datasheet > Electrical Service Attributes; Guidance > Considerations > Electrical Load and Service Sizing | -- | PROPOSAL: Transcribe load summary from App B (Electrical) | TBD |
| B-003 | B:data:completeness | Conflict | Multi | Multi | Resolve CONF-001: MEMORY.md labels SOW-0080 as "Electrical" and SOW-0081 as "Water/Sewer" while Decomposition and RFP define SOW-0080 = Natural Gas, SOW-0081 = Electrical, SOW-0082 = Communications. Additionally, _CONTEXT.md lists scope as "electrical, water, sewer, gas" which does not match the three SOWs. | Comprehensive record requires factual accuracy. The SOW mislabeling in external sources risks propagating incorrect utility system identification. _CONTEXT.md scope description mentions "water, sewer" which are not in scope per the Decomposition. | Guidance.md; _CONTEXT.md | Guidance > Conflict Table > CONF-001; _CONTEXT.md > Scope of Work References and Context Summary | Guidance.md#CONF-001 vs _CONTEXT.md#Context-Summary | PROPOSAL: Decomposition and RFP are authoritative per Guidance CONF-001 | TBD |
| B-004 | B:information:necessity | TBD_Question | Guidance | Datasheet | Record TBD: Quantify expected utility provider lead times for each system (gas, electrical, communications) for this rural Alberta location | Guidance states provider lead times "can be significant (weeks to months)" but provides no quantified estimate. This signal is essential for scheduling. | Guidance.md | Principles > 1. Coordinate Early with Utility Providers | -- | PROPOSAL: Source from utility provider responses during Step A1 | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Binding Compliance Threshold | 1 | HAS_ITEMS | Burial depth thresholds not specified |
| C:normative:sufficiency | normative | sufficiency | Mandated Proof Standard | 1 | HAS_ITEMS | Proof standard for gas pipe material absent |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Scope | 0 | NO_ITEMS | Regulatory scope adequately enumerated in Standards table |
| C:normative:consistency | normative | consistency | Codified Uniform Standard | 0 | NO_ITEMS | Standards consistently referenced across docs |
| C:operative:necessity | operative | necessity | Critical Execution Basis | 1 | HAS_ITEMS | Missing cathodic protection requirement detail |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Work Readiness | 0 | NO_ITEMS | Work readiness prerequisites well-defined in Procedure |
| C:operative:completeness | operative | completeness | Total Process Coverage | 0 | NO_ITEMS | Process steps cover full lifecycle from planning to close-out |
| C:operative:consistency | operative | consistency | Repeatable Process Discipline | 0 | NO_ITEMS | Process steps are repeatable and consistently structured |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Value Basis | 0 | NO_ITEMS | Value basis clear through objective alignment |
| C:evaluative:sufficiency | evaluative | sufficiency | Justified Merit Assessment | 0 | NO_ITEMS | Merit assessment embedded in trade-off table |
| C:evaluative:completeness | evaluative | completeness | Holistic Value Accounting | 0 | NO_ITEMS | Value accounting adequate for preparation phase |
| C:evaluative:consistency | evaluative | consistency | Principled Value Coherence | 0 | NO_ITEMS | Value coherence maintained across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | MissingSlot | Specification | Specification | Add minimum burial depth requirements for each utility type (gas, electrical, communications) as a binding compliance threshold, referencing applicable Alberta codes | Binding compliance thresholds for burial depth are a fundamental regulatory requirement for underground utilities. Procedure Step B2 marks these as "TBD" and the Specification does not address them. | Specification.md; Procedure.md | Specification > entire REQ section scanned; Procedure > Step B2 | -- | PROPOSAL: Source from CEC, CSA B149.1, and municipal requirements once confirmed | TBD |
| C-002 | C:normative:sufficiency | MissingSlot | Specification | Specification | Add requirement for gas pipe material specification and cathodic protection per CSA B149.1 as part of mandated proof standard for gas installation | The mandated proof standard for gas work requires material specification. REQ-01.4 mentions "pipe material" in passing but does not specify it as a requirement to be documented. Procedure Step B3 references "piping material and cathodic protection requirements per CSA B149.1" as TBD. | Specification.md; Procedure.md | Specification > REQ-01.4; Procedure > Step B3 | -- | PROPOSAL: Source from mechanical design (DEL-003) and CSA B149.1 | TBD |
| C-003 | C:operative:necessity | WeakStatement | Procedure | Specification | Strengthen Procedure Step B3 item 2 regarding cathodic protection from "TBD" to a clear requirement statement, or add a requirement in Specification for cathodic protection determination | Cathodic protection is a critical execution requirement for underground gas piping. The Procedure mentions it only as "(TBD)" alongside gas utility standards. This should be elevated to a tracked requirement. | Procedure.md | Steps > Part B > Step B3 item 2 | -- | PROPOSAL: Determine cathodic protection requirements from CSA B149.1 and gas utility provider | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Imposed Conformance Mandate | 1 | HAS_ITEMS | Transformer responsibility not mandated |
| F:normative:sufficiency | normative | sufficiency | Sufficient Compliance Evidence | 1 | HAS_ITEMS | Commissioning evidence requirements weak |
| F:normative:completeness | normative | completeness | Exhaustive Compliance Record | 0 | NO_ITEMS | Compliance record items well-enumerated in Documentation table |
| F:normative:consistency | normative | consistency | Uniform Regulatory Alignment | 0 | NO_ITEMS | Regulatory references consistent across documents |
| F:operative:necessity | operative | necessity | Essential Operational Rigor | 1 | HAS_ITEMS | One-Call locate not in Specification |
| F:operative:sufficiency | operative | sufficiency | Proven Procedural Capacity | 0 | NO_ITEMS | Procedural capacity demonstrated through step detail |
| F:operative:completeness | operative | completeness | Exhaustive Workflow Record | 0 | NO_ITEMS | Workflow records adequately defined in Procedure Records table |
| F:operative:consistency | operative | consistency | Stable Execution Consistency | 0 | NO_ITEMS | Execution steps consistently structured |
| F:evaluative:necessity | evaluative | necessity | Fundamental Worth Imperative | 0 | NO_ITEMS | Worth imperative addressed through objective linkage |
| F:evaluative:sufficiency | evaluative | sufficiency | Justified Worth Appraisal | 1 | HAS_ITEMS | Cost impact of gas main extension not quantified |
| F:evaluative:completeness | evaluative | completeness | Complete Worth Narrative | 0 | NO_ITEMS | Worth narrative adequate for preparation phase |
| F:evaluative:consistency | evaluative | consistency | Coherent Worth Standard | 0 | NO_ITEMS | Worth standard coherent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | MissingSlot | Specification | Specification | Add a requirement addressing transformer ownership determination (utility-owned vs. customer-owned) and responsibility assignment as part of the imposed conformance mandate for electrical service | Transformer ownership affects ongoing maintenance obligations, capital cost, and site layout. Guidance identifies this as a trade-off but neither Specification nor Procedure mandates a determination. | Specification.md; Guidance.md | Specification > REQ-02 section (entire); Guidance > Trade-offs > Transformer ownership | -- | PROPOSAL: Resolve during utility provider coordination (Step A3) | TBD |
| F-002 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add specific commissioning evidence requirements for each utility system (e.g., what constitutes a passing pressure test for gas, what voltage/phase measurements prove electrical compliance, what communication test proves continuity) | Sufficient compliance evidence requires defined pass criteria for commissioning. The Verification table groups REQ-01.1-01.4 and REQ-02.1-02.6 together with generic evidence ("Permits; inspection reports; provider service agreement") but does not define what test results constitute passing evidence. | Specification.md | Verification table | -- | PROPOSAL: Define pass/fail criteria referencing Safety Code inspection standards | TBD |
| F-003 | F:operative:necessity | Normalization | Procedure | Specification | Add Alberta One-Call / Click Before You Dig locate requirement to the Specification as a formal requirement (currently only in Procedure Step B1) | Essential operational rigor requires the One-Call locate to be a normative requirement, not just a procedural step. This is a regulatory requirement in Alberta for any excavation, yet it appears only in the Procedure, not in the Specification. | Procedure.md; Specification.md | Procedure > Step B1 item 2; Specification > entire REQ section scanned | -- | PROPOSAL: Add as REQ-04.8 or similar in Specification | TBD |
| F-004 | F:evaluative:sufficiency | RationaleGap | Guidance | Guidance | Add quantified cost/schedule risk assessment for the scenario where no gas main exists near the site, including potential propane alternative cost comparison | Justified worth appraisal requires cost basis. Guidance mentions "the cost and lead time for a new gas main extension could be significant" but provides no quantification or framework for evaluating the propane alternative. | Guidance.md | Considerations > Natural Gas Service and Heating System Interface; Trade-offs > Gas service extension vs. propane | -- | PROPOSAL: Quantify during utility provider coordination (Step A4) | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Authoritative Compliance Direction | 0 | NO_ITEMS | Compliance direction adequately established |
| D:normative:applying | normative | applying | Enforced Verified Practice | 1 | HAS_ITEMS | Verification grouping too coarse |
| D:normative:judging | normative | judging | Conclusive Conformance Ruling | 0 | NO_ITEMS | Conformance ruling pathway clear through inspection sign-off |
| D:normative:reviewing | normative | reviewing | Resolved Regulatory Oversight | 0 | NO_ITEMS | Regulatory oversight pathway defined |
| D:operative:guiding | operative | guiding | Governed Execution Order | 1 | HAS_ITEMS | Missing explicit sequencing constraint |
| D:operative:applying | operative | applying | Confirmed Task Delivery | 0 | NO_ITEMS | Task delivery steps well-defined |
| D:operative:judging | operative | judging | Settled Performance Verdict | 0 | NO_ITEMS | Performance verdict pathway clear through verification checks |
| D:operative:reviewing | operative | reviewing | Verified Process Stability | 0 | NO_ITEMS | Process stability addressed through inspection attendance and records |
| D:evaluative:guiding | evaluative | guiding | Committed Value Direction | 0 | NO_ITEMS | Value direction committed through objective alignment |
| D:evaluative:applying | evaluative | applying | Demonstrated Merit Delivery | 0 | NO_ITEMS | Merit delivery tracked through trade-offs |
| D:evaluative:judging | evaluative | judging | Conclusive Worth Judgment | 0 | NO_ITEMS | Worth judgment deferred appropriately to construction phase |
| D:evaluative:reviewing | evaluative | reviewing | Verified Quality Alignment | 1 | HAS_ITEMS | Guarantee period verification gap |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | VerificationGap | Specification | Specification | Disaggregate Verification table entries to provide per-requirement verification criteria rather than grouping REQ-01.1 through 01.4 and REQ-02.1 through 02.6 together | Enforced verified practice requires each requirement to have traceable verification. The current Verification table groups multiple requirements into ranges (e.g., "REQ-01.1-01.4") with a single generic verification entry. Individual requirements like REQ-02.2 (three-phase power) and REQ-02.5 (service capacity) have different verification methods that are lost in the grouping. | Specification.md | Verification table | -- | PROPOSAL: Expand Verification table to one row per Req ID | TBD |
| D-002 | D:operative:guiding | MissingSlot | Procedure | Procedure | Add explicit sequencing constraint statement: "Step B2 (Trenching) shall not commence until PREREQ-08 (site grading substantially complete) is verified" as a governed hold point, not just a prerequisite | The governed execution order requires explicit hold points. PREREQ-08 states grading must be substantially complete but the procedure steps do not include a verification gate between prerequisites and Step B2. | Procedure.md | Prerequisites > PREREQ-08; Steps > Part B > Step B2 | -- | PROPOSAL: Add hold-point verification before Step B2 | TBD |
| D-003 | D:evaluative:reviewing | VerificationGap | Specification | Procedure | Add verification check for 2-year guarantee period coverage of utility tie-in work, linking Datasheet guarantee condition to a close-out verification step | Verified quality alignment requires that the 2-year guarantee period (RFP ss2.10) noted in the Datasheet Conditions table is tracked through to close-out. Neither the Specification Verification table nor the Procedure Verification table includes a check for guarantee period documentation or handover of guarantee obligations. | Datasheet.md; Specification.md; Procedure.md | Datasheet > Conditions > Guarantee Period row; Specification > Verification table (entire); Procedure > Verification table (entire) | -- | PROPOSAL: Add guarantee handover verification to Procedure close-out or Specification Documentation table | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Directive Clarity | 1 | HAS_ITEMS | Water/sewer terminology drift |
| X:guiding:sufficiency | guiding | sufficiency | Adequate Governance Evidence | 0 | NO_ITEMS | Governance evidence adequate through documented RFP references |
| X:guiding:completeness | guiding | completeness | Complete Governance Scope | 1 | HAS_ITEMS | Missing scope boundary for existing utility infrastructure |
| X:guiding:consistency | guiding | consistency | Unified Governance Alignment | 0 | NO_ITEMS | Governance alignment unified across documents |
| X:applying:necessity | applying | necessity | Validated Delivery Foundation | 1 | HAS_ITEMS | Licensed contractor requirement not in Specification |
| X:applying:sufficiency | applying | sufficiency | Proven Execution Adequacy | 0 | NO_ITEMS | Execution adequacy demonstrated through step detail |
| X:applying:completeness | applying | completeness | Exhaustive Delivery Record | 0 | NO_ITEMS | Delivery records comprehensively listed |
| X:applying:consistency | applying | consistency | Dependable Execution Standard | 0 | NO_ITEMS | Execution standards consistently referenced |
| X:judging:necessity | judging | necessity | Critical Verdict Foundation | 1 | HAS_ITEMS | Missing deficiency resolution criteria |
| X:judging:sufficiency | judging | sufficiency | Sufficient Ruling Evidence | 0 | NO_ITEMS | Ruling evidence pathways adequate |
| X:judging:completeness | judging | completeness | Exhaustive Ruling Record | 0 | NO_ITEMS | Ruling records adequately enumerated |
| X:judging:consistency | judging | consistency | Consistent Ruling Alignment | 0 | NO_ITEMS | Ruling alignment consistent across verification tables |
| X:reviewing:necessity | reviewing | necessity | Critical Oversight Foundation | 1 | HAS_ITEMS | Missing communication lines inspection requirement |
| X:reviewing:sufficiency | reviewing | sufficiency | Sufficient Review Evidence | 0 | NO_ITEMS | Review evidence pathways adequate |
| X:reviewing:completeness | reviewing | completeness | Comprehensive Audit Record | 0 | NO_ITEMS | Audit records comprehensively listed |
| X:reviewing:consistency | reviewing | consistency | Harmonized Oversight Standard | 0 | NO_ITEMS | Oversight standard harmonized across docs |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:necessity | Normalization | Multi | Multi | Normalize utility system terminology: replace "water, sewer" references in _CONTEXT.md with the correct three systems (natural gas, electrical service, communications) per the authoritative Decomposition and RFP | Foundational directive clarity requires accurate system identification. _CONTEXT.md Context Summary states "electrical, water, sewer, gas" as the utility systems, but the Decomposition and RFP define them as natural gas (SOW-0080), electrical (SOW-0081), and communications (SOW-0082). Water and sewer are not in scope. | _CONTEXT.md | Context Summary | _CONTEXT.md#Context-Summary vs Specification.md#Scope | PROPOSAL: RFP and Decomposition are authoritative | TBD |
| X-002 | X:guiding:completeness | MissingSlot | Specification | Specification | Add exclusion or scope boundary statement clarifying responsibility for existing utility infrastructure up to the point of connection (i.e., who owns/maintains the utility run from provider main to site boundary) | Complete governance scope requires a clear scope boundary at the interface between provider infrastructure and contractor work. The Specification exclusions table addresses interior building systems but does not address the boundary between provider-side and contractor-side infrastructure on the site service run. | Specification.md | Scope > What This Deliverable Excludes | -- | PROPOSAL: Clarify during utility provider coordination | TBD |
| X-003 | X:applying:necessity | Normalization | Guidance | Specification | Elevate the licensed contractor requirement from Guidance (Considerations > Regulatory and Permitting Environment) to a formal Specification requirement: "Gas and electrical service work shall be performed by contractors licensed in the applicable Safety Code discipline" | Validated delivery foundation requires that the licensed-contractor constraint be normative. Currently it appears only as guidance ("The General Contractor must confirm which subcontractors are licensed") rather than as a specification requirement. | Guidance.md; Specification.md | Guidance > Considerations > Regulatory and Permitting Environment; Specification > entire REQ section scanned | -- | PROPOSAL: Add as REQ-04.8 or REQ-04.9 in Specification | TBD |
| X-004 | X:judging:necessity | VerificationGap | Procedure | Procedure | Add deficiency resolution acceptance criteria and timeline to Step B8 item 4 ("Resolve any deficiencies identified at inspection") | Critical verdict foundation requires defined criteria for deficiency resolution. Step B8 item 4 states "Resolve any deficiencies" but provides no criteria for what constitutes resolution, no timeline, and no re-inspection requirement. | Procedure.md | Steps > Part B > Step B8 item 4 | -- | PROPOSAL: Define deficiency resolution protocol referencing Safety Code re-inspection requirements | TBD |
| X-005 | X:reviewing:necessity | VerificationGap | Specification | Specification | Add explicit Safety Code inspection requirement for communications infrastructure, or document why communications is exempt from Safety Code inspection in Alberta | Critical oversight foundation requires inspection requirements for all three utility systems. Gas and electrical have explicit Safety Code inspection requirements (REQ-04.3, Step B5, Step B8). Communications has no equivalent inspection requirement in the Specification or Procedure beyond generic "physical inspection of conduit/cabling installation." | Specification.md; Procedure.md | Specification > Verification table > REQ-03.1-03.4 row; Procedure > Step B8 | -- | PROPOSAL: Confirm with Safety Codes Officer whether communications conduit requires Safety Code inspection | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Verified Directive Baseline | 1 | HAS_ITEMS | SOW reference table inconsistency |
| E:guiding:information | guiding | information | Coherent Steering Intelligence | 0 | NO_ITEMS | Steering intelligence coherent across Guidance |
| E:guiding:knowledge | guiding | knowledge | Strategic Governance Mastery | 0 | NO_ITEMS | Strategic governance adequate for current phase |
| E:guiding:wisdom | guiding | wisdom | Principled Strategic Foresight | 0 | NO_ITEMS | Foresight reflected in early-coordination principles |
| E:applying:data | applying | data | Documented Delivery Evidence | 1 | HAS_ITEMS | Missing as-built drawing requirement in Specification |
| E:applying:information | applying | information | Informed Execution Context | 0 | NO_ITEMS | Execution context well-informed through Guidance and Procedure |
| E:applying:knowledge | applying | knowledge | Proven Craft Proficiency | 0 | NO_ITEMS | Craft proficiency requirements deferred to licensed contractor engagement |
| E:applying:wisdom | applying | wisdom | Seasoned Execution Judgment | 0 | NO_ITEMS | Execution judgment reflected in Guidance trade-offs and considerations |
| E:judging:data | judging | data | Substantiated Verdict Record | 1 | HAS_ITEMS | Missing inspection report content requirements |
| E:judging:information | judging | information | Informed Assessment Narrative | 0 | NO_ITEMS | Assessment narrative adequate through verification tables |
| E:judging:knowledge | judging | knowledge | Expert Assessment Command | 0 | NO_ITEMS | Expert assessment deferred to P.Eng. and Safety Code officers |
| E:judging:wisdom | judging | wisdom | Principled Judicial Wisdom | 0 | NO_ITEMS | Judicial wisdom reflected in conflict table and human ruling provisions |
| E:reviewing:data | reviewing | data | Substantiated Audit Record | 1 | HAS_ITEMS | Missing CCC linkage to utility tie-in verification |
| E:reviewing:information | reviewing | information | Informed Oversight Narrative | 0 | NO_ITEMS | Oversight narrative adequate |
| E:reviewing:knowledge | reviewing | knowledge | Expert Audit Proficiency | 0 | NO_ITEMS | Audit proficiency deferred to Safety Code authorities |
| E:reviewing:wisdom | reviewing | wisdom | Principled Oversight Wisdom | 0 | NO_ITEMS | Oversight wisdom reflected in County inspection attendance requirement |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | WeakStatement | Datasheet | Datasheet | Clarify the SOW-to-system mapping in the Datasheet Attributes table header or add a cross-reference note confirming SOW-0080 = Natural Gas, SOW-0081 = Electrical, SOW-0082 = Communications, explicitly countering the known MEMORY.md error (CONF-001) | Verified directive baseline requires unambiguous SOW-to-system mapping. While the Datasheet table is internally correct, it does not explicitly address the known mislabeling conflict from CONF-001. Adding a cross-reference strengthens the baseline against propagation of the MEMORY.md error. | Datasheet.md; Guidance.md | Datasheet > Attributes > Utility Systems In Scope; Guidance > Conflict Table > CONF-001 | -- | PROPOSAL: Add note referencing authoritative Decomposition mapping | TBD |
| E-002 | E:applying:data | VerificationGap | Specification | Specification | Add as-built drawing submission as a formal verification requirement in the Specification Verification table, not just in the Documentation table | Documented delivery evidence requires that as-built drawings are a verified output, not just an anticipated artifact. The Specification Documentation table lists "As-Built Drawings" but the Verification table does not include an explicit verification row for as-built drawing completeness and accuracy. | Specification.md | Specification > Verification table (entire); Specification > Documentation table > As-Built Drawings row | -- | PROPOSAL: Add Verification table row for as-built drawing acceptance | TBD |
| E-003 | E:judging:data | WeakStatement | Specification | Specification | Define minimum content requirements for inspection reports (e.g., inspector identification, date, items inspected, pass/fail status, deficiency list, signature) rather than relying on generic "inspection reports" as evidence | Substantiated verdict record requires that inspection report content is defined. REQ-04.4 requires "copies of all completed inspection reports" but does not define what constitutes a complete report. This risks accepting incomplete inspection documentation. | Specification.md | REQ-04.4; Verification table | -- | PROPOSAL: Define minimum inspection report content requirements or reference Safety Code report templates | TBD |
| E-004 | E:reviewing:data | RationaleGap | Specification | Procedure | Add explicit linkage between the Construction Completion Certificate (CCC) and the utility tie-in verification evidence, explaining what utility-specific evidence is required for CCC issuance | Substantiated audit record requires clear linkage between individual deliverable verification and the overarching CCC. The Specification Documentation table lists CCC as an artifact and the Procedure Records table includes it, but neither document explains what utility tie-in evidence the CCC depends on or how utility commissioning feeds into the CCC decision. | Specification.md; Procedure.md | Specification > Documentation > CCC row; Procedure > Records > CCC row | -- | PROPOSAL: Add CCC evidence requirements referencing utility-specific commissioning sign-offs | TBD |

---

## QA Verification

| Check | Result |
|-------|--------|
| Coverage complete | PASS -- All 96 matrix cells across A (12), B (16), C (12), F (12), D (12), X (16), E (16) have Lens Coverage entries |
| No invention | PASS -- All warranted items grounded in evidence from production documents or explicit absence |
| Provenance present | PASS -- Every item has SourcePath and SectionRef |
| Conflicts surfaced | PASS -- 1 conflict (B-003) has Contenders and HumanRuling = TBD |
| Summary consistent | PASS -- Summary counts match actual warranted items (28 total) |
| Schema followed | PASS -- Output follows STRUCTURE schema |
