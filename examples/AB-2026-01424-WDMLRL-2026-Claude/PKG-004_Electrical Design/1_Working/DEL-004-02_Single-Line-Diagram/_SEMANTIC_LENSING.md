# Semantic Lensing Register: DEL-004-02 Single-Line Diagram

**Generated:** 2026-02-26
**Deliverable Folder:** PKG-004_Electrical Design/1_Working/DEL-004-02_Single-Line-Diagram/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-004-02_Single-Line-Diagram/_CONTEXT.md
- _STATUS.md — DEL-004-02_Single-Line-Diagram/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md — DEL-004-02_Single-Line-Diagram/_SEMANTIC.md (Generated: 2026-02-26; all 7 matrices parsed)
- Datasheet.md — DEL-004-02_Single-Line-Diagram/Datasheet.md
- Specification.md — DEL-004-02_Single-Line-Diagram/Specification.md
- Guidance.md — DEL-004-02_Single-Line-Diagram/Guidance.md
- Procedure.md — DEL-004-02_Single-Line-Diagram/Procedure.md
- _REFERENCES.md — DEL-004-02_Single-Line-Diagram/_REFERENCES.md (read; R-01, R-05 listed)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 22
- By document:
  - Datasheet: 3
  - Specification: 7
  - Guidance: 4
  - Procedure: 5
  - Multi: 3
- By matrix:
  - A: 4  B: 3  C: 3  F: 3  D: 2  X: 4  E: 3
- By type:
  - Conflict: 0
  - VerificationGap: 5
  - MissingSlot: 6
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 2
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 0 (3 conflicts already captured in Guidance.md Conflict Table; not duplicated here)
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Weak statement on applicable code editions |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Missing mechanical load provision requirement |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Verification gap on code-edition confirmation |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit provisions adequately covered by REQ-SLD-007, REQ-SLD-008, and Procedure Step 9 |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Step 1-9 provide adequate procedural direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Missing drawing platform/format specification |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Performance assessment covered by Procedure verification table |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Procedure records section provides adequate audit trail |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Purpose section provides adequate value framing |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Objective alignment in Guidance and Procedure adequate |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Verification methods mapped to requirements in Specification |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Coordination review (Step 6) and County approval (Step 7) address quality appraisal |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify which specific CEC edition is applicable or add explicit requirement for Electrical Engineer to confirm edition before design proceeds | The Standards table lists CEC as "specific edition TBD per Alberta Safety Codes authority (location TBD)". As prescriptive direction, the normative document should either state the edition or contain an explicit requirement to confirm it as a gating action. | Specification.md | Standards table — CEC row | — | PROPOSAL: Electrical Engineer | TBD |
| A-002 | A:normative:applying | MissingSlot | Specification | Specification | Add requirement for mechanical equipment electrical provisions on the SLD (currently noted only in Guidance Considerations; no normative requirement exists) | Guidance.md identifies coordination with mechanical electrical loads as a consideration, but no REQ-SLD item mandates that mechanical equipment feeds appear on the SLD. This is a mandatory practice gap. | Guidance.md; Specification.md | Guidance.md#Coordination with Mechanical Electrical Loads; Specification.md#Requirements (entire section scanned) | — | PROPOSAL: Electrical Engineer | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add verification method for confirming that the specific CEC edition used is the edition currently adopted by Alberta Safety Codes | Standards table notes applicability but verification section has no check for code-edition confirmation. Compliance determination requires knowing which code edition governs. | Specification.md | Standards table; Verification table | — | PROPOSAL: Electrical Engineer / Safety Codes authority | TBD |
| A-004 | A:operative:applying | WeakStatement | Procedure | Procedure | Specify the drawing platform or format convention (CAD/BIM/PDF) for the SLD, or add explicit decision point for the Electrical Engineer to select and document it | Procedure Step 4.1 says "format: TBD -- per Electrical Engineer's standard CAD/BIM platform." For practical execution, the platform/format should be stated or have a resolution step. | Procedure.md | Steps > Step 4 -- Draft Single-Line Diagram > 4.1 | — | PROPOSAL: Electrical Engineer | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Missing exhaust fan count in Datasheet |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Load group table in Datasheet provides adequate evidence for most items |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Missing mechanical loads in Datasheet load inventory |
| B:data:consistency | data | consistency | reliable measurement | 1 | HAS_ITEMS | Ceiling fan rating TBD with no source path for resolution |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Cross-references between documents provide essential signals adequately |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Guidance Considerations section provides adequate context |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Documents collectively provide comprehensive account of SLD scope |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Documents are internally coherent on load inventory and hierarchy |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Guidance Principles provide adequate foundational understanding |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Procedure assumes competent electrical engineering expertise throughout |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Documents defer appropriately to professional judgment where TBDs exist |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding of distribution hierarchy is consistent across all four documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Guidance trade-offs section provides appropriate discernment framing |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-off table in Guidance provides adequate judgment framework |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance covers voltage, topology, crane, and low-voltage trade-offs |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is consistent and principle-based across Guidance |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add exhaust fan quantity and rating to Identified Load Groups table (currently listed as "As shown on electrical drawing" with no count or rating) | Exhaust fan is listed in Datasheet load group table but circuit/rating column says only "E symbol on conceptual drawing" with no count. As an essential fact for SLD sizing, the count and rating are needed. | Datasheet.md | Attributes > Identified Load Groups > Exhaust Fan(s) row | — | PROPOSAL: App B (Electrical) / Mechanical Engineer | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add mechanical equipment electrical loads (MUA unit, heating system, exhaust systems from PKG-003) to the Identified Load Groups table, even as TBD placeholders | Datasheet load inventory omits mechanical equipment electrical loads entirely. Guidance identifies these as needing coordination, but the descriptive record should enumerate them for comprehensive coverage. | Datasheet.md; Guidance.md | Datasheet.md#Attributes > Identified Load Groups; Guidance.md#Considerations > Coordination with Mechanical Electrical Loads | — | PROPOSAL: Mechanical Engineer / DEL-003-05 | TBD |
| B-003 | B:data:consistency | TBD_Question | Datasheet | Datasheet | Record TBD: Ceiling fan electrical rating (watts or amps) -- source needed from equipment selection or specification | Ceiling fan entry in Datasheet says "TBD -- rating per equipment selection" but does not indicate which deliverable or party will provide the rating. Reliable measurement requires a resolution path. | Datasheet.md | Attributes > Identified Load Groups > Ceiling Fans row | — | PROPOSAL: Equipment supplier / Electrical Engineer | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Obligatory Compliance Basis | 1 | HAS_ITEMS | Missing requirement for arc flash / short circuit analysis reference |
| C:normative:sufficiency | normative | sufficiency | Qualified Conformance Evidence | 0 | NO_ITEMS | Verification table maps each requirement to a method |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Coverage | 1 | HAS_ITEMS | Missing grounding/bonding requirement |
| C:normative:consistency | normative | consistency | Uniform Compliance Discipline | 0 | NO_ITEMS | Requirements consistently reference source SOWs and verification |
| C:operative:necessity | operative | necessity | Core Operational Foundation | 0 | NO_ITEMS | Procedure prerequisites table identifies all essential inputs |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Operational Capacity | 0 | NO_ITEMS | 9-step procedure demonstrates adequate operational capacity |
| C:operative:completeness | operative | completeness | Thorough Execution Coverage | 1 | HAS_ITEMS | Missing step for drawing numbering convention |
| C:operative:consistency | operative | consistency | Stable Procedural Reliability | 0 | NO_ITEMS | Procedure steps follow a logical, repeatable sequence |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Merit Foundation | 0 | NO_ITEMS | SLD as single source of truth for hierarchy is well-established |
| C:evaluative:sufficiency | evaluative | sufficiency | Justified Value Adequacy | 0 | NO_ITEMS | Guidance purpose and objective alignment provide justified value |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Worth Assessment | 0 | NO_ITEMS | Trade-offs and considerations sections cover major value decisions |
| C:evaluative:consistency | evaluative | consistency | Principled Valuation Coherence | 0 | NO_ITEMS | Value reasoning is consistent across Guidance |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | MissingSlot | Specification | Specification | Add requirement (or TBD placeholder) for arc flash hazard analysis or short-circuit current rating reference on SLD, if required by CEC/CSA Z462 for industrial facilities | An industrial maintenance shop with large dedicated circuits (70A pump, 70A pressure washer, cranes) may require arc flash labeling or short-circuit analysis. No requirement addresses this. Obligatory compliance basis lens suggests this is a gap. | Specification.md | Requirements (entire section scanned) | — | PROPOSAL: CEC / CSA Z462 / Electrical Engineer | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add requirement for grounding and bonding system representation on the SLD (service grounding electrode, bonding conductors, equipment grounding) | Exhaustive regulatory coverage lens reveals no requirement for grounding/bonding on the SLD. CEC requires grounding/bonding for all electrical installations; an industrial SLD typically shows the grounding system. | Specification.md | Requirements (entire section scanned) | — | PROPOSAL: CEC / Electrical Engineer | TBD |
| C-003 | C:operative:completeness | WeakStatement | Procedure | Procedure | Add step or sub-step for establishing drawing numbering convention and revision control scheme before drafting begins | Procedure Step 4.6 mentions "drawing number per project numbering convention (TBD)" but there is no prior step to establish or confirm the numbering convention. This weakens thorough execution coverage. | Procedure.md | Steps > Step 4 > 4.6 | — | PROPOSAL: Electrical Engineer / Project Manager | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Enforceable Regulatory Mandate | 1 | HAS_ITEMS | Permit application requirement absent |
| F:normative:sufficiency | normative | sufficiency | Sufficient Regulatory Proof | 0 | NO_ITEMS | P.Eng. stamp and County approval provide sufficient regulatory proof |
| F:normative:completeness | normative | completeness | Total Governance Assurance | 0 | NO_ITEMS | Standards table covers CEC, ABC, APEGA, CCDC 14 |
| F:normative:consistency | normative | consistency | Harmonized Regulatory Standard | 0 | NO_ITEMS | Regulatory references are harmonized across documents |
| F:operative:necessity | operative | necessity | Critical Functional Imperative | 1 | HAS_ITEMS | Voltage drop calculation not referenced in Procedure |
| F:operative:sufficiency | operative | sufficiency | Proven Delivery Competence | 0 | NO_ITEMS | Procedure demonstrates adequate delivery sequence |
| F:operative:completeness | operative | completeness | Total Process Mastery | 0 | NO_ITEMS | 9-step procedure with verification covers process fully |
| F:operative:consistency | operative | consistency | Reliable Process Uniformity | 0 | NO_ITEMS | Procedure is internally consistent and repeatable |
| F:evaluative:necessity | evaluative | necessity | Fundamental Quality Imperative | 0 | NO_ITEMS | Verification matrix provides fundamental quality checks |
| F:evaluative:sufficiency | evaluative | sufficiency | Substantiated Value Judgment | 1 | HAS_ITEMS | Missing rationale for sub-panel zoning decision |
| F:evaluative:completeness | evaluative | completeness | Holistic Quality Accounting | 0 | NO_ITEMS | Quality accounting is holistic across Specification verification and Procedure checks |
| F:evaluative:consistency | evaluative | consistency | Unified Quality Rationale | 0 | NO_ITEMS | Quality rationale is unified and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | VerificationGap | Specification | Specification | Add requirement or verification step for confirming that the electrical permit application includes the SLD, per Alberta Safety Codes Act requirements (SOW-0007, SOW-0009) | The Specification references permit obligations (SOW-0007, SOW-0009) in the Standards table but has no explicit requirement that the SLD be included in the permit application. Enforceable regulatory mandate lens reveals this gap. | Specification.md | Standards table; Verification table | — | PROPOSAL: Alberta Safety Codes / Electrical Engineer | TBD |
| F-002 | F:operative:necessity | VerificationGap | Procedure | Specification | Add verification step confirming voltage drop calculations for long feeder runs (130' x 100' building) are performed and SLD feeder sizes reflect results | Procedure Step 3.2 mentions voltage drop consideration but there is no corresponding verification in Specification or Procedure verification tables. For a critical functional imperative in a large industrial building, this should be verified. | Procedure.md; Specification.md | Procedure.md#Steps > Step 3 > 3.2; Specification.md#Verification table | — | PROPOSAL: Electrical Engineer / CEC | TBD |
| F-003 | F:evaluative:sufficiency | RationaleGap | Guidance | Guidance | Add rationale explaining under what conditions the MDP-only topology vs. zoned sub-panels decision should be made (currently listed as trade-off without decision criteria) | Guidance trade-off table lists "Single MDP with all circuits" vs. "MDP + zoned sub-panels" but the ASSUMPTION note provides no structured decision criteria. Substantiated value judgment requires clearer guidance on when to choose each option. | Guidance.md | Trade-offs table — Panel topology row | — | PROPOSAL: Electrical Engineer | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Resolved Governing Directive | 0 | NO_ITEMS | Governing directives (P.Eng. stamp, County approval) are resolved and clear |
| D:normative:applying | normative | applying | Confirmed Compulsory Practice | 0 | NO_ITEMS | Compulsory practices well-defined in Requirements section |
| D:normative:judging | normative | judging | Settled Conformance Ruling | 0 | NO_ITEMS | Conformance rulings mapped via verification table |
| D:normative:reviewing | normative | reviewing | Reconciled Regulatory Scrutiny | 0 | NO_ITEMS | County approval and P.Eng. stamp provide reconciled scrutiny |
| D:operative:guiding | operative | guiding | Resolved Workflow Direction | 0 | NO_ITEMS | 9-step procedure provides resolved workflow direction |
| D:operative:applying | operative | applying | Confirmed Active Delivery | 1 | HAS_ITEMS | Missing explicit deliverable handoff step |
| D:operative:judging | operative | judging | Confirmed Performance Proficiency | 0 | NO_ITEMS | Verification checks confirm performance at each stage |
| D:operative:reviewing | operative | reviewing | Reconciled Process Examination | 0 | NO_ITEMS | Internal review (Step 5) and interdisciplinary review (Step 6) cover process examination |
| D:evaluative:guiding | evaluative | guiding | Resolved Value Orientation | 0 | NO_ITEMS | Guidance purpose section provides resolved value orientation |
| D:evaluative:applying | evaluative | applying | Confirmed Merit Application | 1 | HAS_ITEMS | Missing statement on how SLD supports construction scheduling |
| D:evaluative:judging | evaluative | judging | Settled Worth Determination | 0 | NO_ITEMS | Verification and objective alignment provide settled worth determination |
| D:evaluative:reviewing | evaluative | reviewing | Reconciled Quality Appraisal | 0 | NO_ITEMS | County review and internal review provide quality appraisal |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:operative:applying | MissingSlot | Procedure | Procedure | Add step or sub-step for formal handoff of IFC SLD to electrical contractor (PKG-015) and other downstream users (PKG-013 installation, PKG-018 sitework) | Procedure ends at Step 9 with IFC issue and filing but does not describe how the SLD is delivered to the construction team. Confirmed active delivery lens suggests a handoff step is missing. | Procedure.md | Steps > Step 9 | — | PROPOSAL: Project Manager / Electrical Engineer | TBD |
| D-002 | D:evaluative:applying | RationaleGap | Guidance | Guidance | Add brief rationale explaining how early SLD issuance supports construction scheduling and procurement (Guidance Purpose mentions cost estimation but does not connect to schedule) | Guidance Purpose item 4 mentions "cost estimation and construction coordination" but does not explain the scheduling benefit. Confirmed merit application lens suggests this rationale gap weakens the value proposition. | Guidance.md | Purpose > item 4 | — | PROPOSAL: Electrical Engineer / Project Manager | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Purposeful Authority | 0 | NO_ITEMS | SLD as authority document is well-established in Guidance Principle 1 |
| X:guiding:sufficiency | guiding | sufficiency | Substantiated Directional Adequacy | 0 | NO_ITEMS | Guidance provides substantiated directional adequacy through principles and considerations |
| X:guiding:completeness | guiding | completeness | Total Directional Coverage | 1 | HAS_ITEMS | Missing guidance on emergency/standby power |
| X:guiding:consistency | guiding | consistency | Aligned Directional Coherence | 0 | NO_ITEMS | Direction is aligned and coherent across Guidance sections |
| X:applying:necessity | applying | necessity | Mandatory Execution Foundation | 0 | NO_ITEMS | Prerequisites table establishes mandatory execution inputs |
| X:applying:sufficiency | applying | sufficiency | Adequate Implementation Evidence | 1 | HAS_ITEMS | Missing verification of load inventory completeness before Step 4 |
| X:applying:completeness | applying | completeness | Complete Execution Accounting | 0 | NO_ITEMS | Procedure records section provides complete execution accounting |
| X:applying:consistency | applying | consistency | Consistent Applied Standard | 0 | NO_ITEMS | Procedure applies consistent standards throughout |
| X:judging:necessity | judging | necessity | Essential Adjudication Basis | 1 | HAS_ITEMS | Verification for REQ-SLD-010 cross-discipline coordination lacks specificity |
| X:judging:sufficiency | judging | sufficiency | Sufficient Adjudication Evidence | 0 | NO_ITEMS | Verification methods are sufficiently specified for most requirements |
| X:judging:completeness | judging | completeness | Thorough Adjudication Record | 0 | NO_ITEMS | Documentation table in Specification provides adequate record of adjudication |
| X:judging:consistency | judging | consistency | Unified Adjudication Standard | 0 | NO_ITEMS | Verification methods are consistent in type and format |
| X:reviewing:necessity | reviewing | necessity | Fundamental Inspection Basis | 1 | HAS_ITEMS | Missing Safety Codes inspection readiness check |
| X:reviewing:sufficiency | reviewing | sufficiency | Adequate Inspection Evidence | 0 | NO_ITEMS | Records and documentation provide adequate inspection evidence |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Inspection Record | 0 | NO_ITEMS | Records table in Procedure is comprehensive |
| X:reviewing:consistency | reviewing | consistency | Coherent Inspection Standard | 0 | NO_ITEMS | Inspection requirements are coherent across Procedure and Specification |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | TBD_Question | Guidance | Guidance | Record TBD: Does the facility require emergency or standby power provisions (e.g., emergency egress lighting, fire alarm panel backup)? If so, the SLD should include these circuits. | Total directional coverage lens reveals no mention of emergency/standby power in any document. An industrial maintenance shop may require emergency egress lighting at minimum. This is a necessary design input not yet addressed. | Guidance.md; Specification.md | Guidance.md#Considerations (entire section scanned); Specification.md#Requirements (entire section scanned) | — | PROPOSAL: Alberta Building Code / CEC / Electrical Engineer | TBD |
| X-002 | X:applying:sufficiency | VerificationGap | Procedure | Procedure | Add explicit verification gate between Step 1 (load inventory) and Step 4 (draft SLD) confirming that the load inventory is reviewed and accepted as complete before drafting begins | Procedure Step 1 produces the load inventory and Step 5 reviews the draft SLD against it, but there is no formal check that the inventory itself is complete before drafting begins. Adequate implementation evidence requires verifying inputs, not just outputs. | Procedure.md | Steps > Step 1; Steps > Step 5 | — | PROPOSAL: Electrical Engineer | TBD |
| X-003 | X:judging:necessity | WeakStatement | Specification | Specification | Strengthen REQ-SLD-010 verification method to specify which deliverables must sign off and what constitutes a passing cross-reference check | REQ-SLD-010 verification says "Cross-reference check between SLD and named deliverables prior to IFC issue" but does not specify who performs the check, what constitutes pass/fail, or whether all four named deliverables must be checked. Essential adjudication basis requires more specificity. | Specification.md | Verification table — REQ-SLD-010 row | — | PROPOSAL: Electrical Engineer / Project Manager | TBD |
| X-004 | X:reviewing:necessity | VerificationGap | Multi | Specification | Add verification step or record confirming the SLD package is ready for Safety Codes Officer inspection (SOW-0084, SOW-0085) | Procedure Records section mentions Safety Codes inspection availability (SOW-0084, SOW-0085) but neither Specification verification nor Procedure verification tables include a specific check for inspection readiness. Fundamental inspection basis requires an explicit gate. | Procedure.md; Specification.md | Procedure.md#Records (note at end); Specification.md#Verification table | — | PROPOSAL: Electrical Engineer / Safety Codes authority | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Factual Guidance | 0 | NO_ITEMS | Guidance is grounded in factual references throughout |
| E:guiding:information | guiding | information | Clear Directive Communication | 0 | NO_ITEMS | Guidance communicates directives clearly |
| E:guiding:knowledge | guiding | knowledge | Commanding Strategic Mastery | 1 | HAS_ITEMS | Missing guidance on future expansion or spare capacity |
| E:guiding:wisdom | guiding | wisdom | Principled Strategic Vision | 0 | NO_ITEMS | Trade-offs section provides principled strategic vision |
| E:applying:data | applying | data | Verified Execution Data | 1 | HAS_ITEMS | Normalization issue in load group naming |
| E:applying:information | applying | information | Actionable Delivery Report | 0 | NO_ITEMS | Procedure outputs at each step are actionable and clear |
| E:applying:knowledge | applying | knowledge | Integrated Practice Proficiency | 0 | NO_ITEMS | Procedure integrates cross-discipline practice adequately |
| E:applying:wisdom | applying | wisdom | Prudent Operational Judgment | 0 | NO_ITEMS | Procedure defers appropriately to professional judgment on TBDs |
| E:judging:data | judging | data | Grounded Evidentiary Verdict | 0 | NO_ITEMS | Verification methods are grounded in evidence |
| E:judging:information | judging | information | Communicated Assessment Finding | 0 | NO_ITEMS | Verification findings are communicable via records |
| E:judging:knowledge | judging | knowledge | Expert Assessment Command | 0 | NO_ITEMS | Expert assessment delegated to P.Eng. appropriately |
| E:judging:wisdom | judging | wisdom | Principled Judgment Wisdom | 0 | NO_ITEMS | Conflict table in Guidance defers to principled judgment |
| E:reviewing:data | reviewing | data | Substantiated Audit Record | 1 | HAS_ITEMS | Normalization of record naming between Specification and Procedure |
| E:reviewing:information | reviewing | information | Communicated Audit Findings | 0 | NO_ITEMS | Records and coordination logs provide audit communication |
| E:reviewing:knowledge | reviewing | knowledge | Expert Oversight Proficiency | 0 | NO_ITEMS | P.Eng. review provides expert oversight |
| E:reviewing:wisdom | reviewing | wisdom | Principled Oversight Wisdom | 0 | NO_ITEMS | County approval and regulatory framework provide principled oversight |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:knowledge | RationaleGap | Guidance | Guidance | Add consideration for spare capacity or future expansion provisions in the SLD (e.g., spare breaker spaces in panels, provision for future loads) | Commanding strategic mastery lens reveals no discussion of future expansion or spare capacity anywhere in the documents. For an industrial facility, designing for future flexibility is a standard engineering consideration. | Guidance.md | Considerations (entire section scanned) | — | PROPOSAL: Electrical Engineer / Owner | TBD |
| E-002 | E:applying:data | Normalization | Multi | Guidance | Normalize load group naming between Datasheet ("Fire Hose Pump Circuit") and Specification REQ-SLD-005 table ("Fire Hose Pump") and Procedure Step 1 ("fire hose pump") -- adopt consistent naming convention | Minor terminology drift exists across documents for the same equipment items (e.g., "Fire Hose Pump Circuit" vs. "Fire Hose Pump" vs. "fire hose pump (70A)"). Verified execution data requires consistent naming for traceability. | Datasheet.md; Specification.md; Procedure.md | Datasheet.md#Identified Load Groups; Specification.md#REQ-SLD-005 table; Procedure.md#Step 1 | — | PROPOSAL: Electrical Engineer | TBD |
| E-003 | E:reviewing:data | Normalization | Multi | Guidance | Normalize artifact naming between Specification Documentation table ("Drawing revision register") and Procedure Records table ("Revision Register") -- adopt consistent terminology | Specification Documentation table calls it "Drawing revision register" while Procedure Records table calls it "Revision Register." These likely refer to the same artifact but the inconsistent naming could cause confusion during audit. | Specification.md; Procedure.md | Specification.md#Documentation table; Procedure.md#Records table | — | PROPOSAL: Electrical Engineer / Project Manager | TBD |

---

**End of Semantic Lensing Register.**
