# Semantic Lensing Register: DEL-05-02 Structural Durability and Maintenance

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/PKG-005_Building_Durability_and_Maintenance/1_Working/DEL-05-02_StructuralDurabilityAndMaintenance
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-05-02, PKG-005, Structural Durability / Narrative
- _STATUS.md -- Current State: SEMANTIC_READY (2026-02-17)
- _SEMANTIC.md -- 8 matrices parsed (A, B, C, F, D, K, X, E); 92 lens cells across A, B, C, F, D, X, E
- Datasheet.md -- Identification, Attributes, Conditions, Construction, References, Assumptions
- Specification.md -- 18 requirements (R-STR-01 through R-STR-18), Verification, Documentation, Assumptions, Conflicts
- Guidance.md -- Principles P-001 through P-004, Considerations C-001 through C-005, Trade-offs T-001 through T-003, Examples EX-001 through EX-003, Narrative writing guidance
- Procedure.md -- Phases A (Proposal), B (Detailed Design), C (Construction QC), D (Operations/Maintenance); Steps A1-A6, B1-B4, C1-C5, D1-D3; Verification checklist; Records
- _REFERENCES.md -- RFP Section 7.1.4, Appendix D (Geotechnical Report), cross-references DEL-02-03, DEL-05-01

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 18
- By document:
  - Datasheet: 4
  - Specification: 7
  - Guidance: 3
  - Procedure: 2
  - Multi: 2
- By matrix:
  - A: 4  B: 3  C: 2  F: 2  D: 2  X: 3  E: 2
- By type:
  - Conflict: 1
  - VerificationGap: 5
  - MissingSlot: 5
  - WeakStatement: 3
  - RationaleGap: 2
  - Normalization: 1
  - TBD_Question: 1
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Weak prescriptive statement on slab compressive strength |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Missing mandatory cold-weather curing duration |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Verification gap for R-STR-16 standards compliance |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit perspective adequately covered by Procedure Phase C and D |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure provides clear procedural direction across all phases |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Missing hold/witness points in construction procedure |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification checklist in Procedure covers performance assessment adequately |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Annual inspection and maintenance log adequately address process audit |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance P-001 and OBJ-005 alignment provide clear value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | EX-001 through EX-003 demonstrate merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Trade-offs T-001 through T-003 address worth determination |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Procedure D1 annual inspection addresses quality appraisal |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify minimum compressive strength for apparatus/PW bay slab-on-grade concrete (R-STR-05 says "low water-cement ratio" but does not specify a minimum strength; EX-001 in Guidance suggests 35 MPa while R-STR-02 specifies 32 MPa for below-grade only) | R-STR-05 omits a specific compressive strength for above-grade bay slabs subject to heavy vehicle traffic and freeze-thaw; the Guidance example implies 35 MPa but this is not formalized as a requirement | Specification.md; Guidance.md | Specification: R-STR-05; Guidance: EX-001 | Specification.md#R-STR-05 (no strength stated); Guidance.md#EX-001 (35 MPa mentioned) | Specification | TBD |
| A-002 | A:normative:applying | MissingSlot | Specification | Specification | Add cold-weather concrete curing duration requirement (R-STR-04 references CAN/CSA-A23.1 cold weather provisions but does not specify minimum curing period or protection duration) | Mandatory practice for cold-weather concrete placement lacks specificity that could affect implementation decisions in Alberta winter conditions | Specification.md | R-STR-04 | -- | Specification | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add verification method for R-STR-16 (standards compliance); current verification table says "Design check vs. all listed standards" but does not specify who performs the independent check or what evidence constitutes compliance | R-STR-16 lists 8 standards but the verification method is vague -- "design check" does not specify whether this is self-certification, peer review, or third-party audit | Specification.md | Verification: R-STR-16 row | -- | Specification | TBD |
| A-004 | A:operative:applying | MissingSlot | Procedure | Procedure | Add explicit hold/witness points in Phase C steps (e.g., mandatory hold before slab pour pending vapour barrier inspection sign-off; mandatory hold before foundation pour pending geotechnical PE bearing surface approval) | Procedure describes inspections but does not designate which are mandatory hold points vs. witness points, which affects whether construction can proceed without sign-off | Procedure.md | Phase C: Steps C2, C3 | -- | Procedure | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Missing reinforcement cover depth data |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Geotechnical data adequately cited with page references |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Missing seismic design parameters beyond site class |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Geotechnical measurements are consistently reported across documents |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key exposure signals (freeze-thaw, sulphate, chloride) are identified |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for each exposure is adequate across the four documents |
| B:information:completeness | information | completeness | comprehensive account | 1 | HAS_ITEMS | Carbonation exposure not addressed |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Exposure messaging is coherent across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding of corrosion, freeze-thaw, and foundation adequately conveyed |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise demonstrated through Guidance examples and Procedure phases |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Coverage across disciplines is thorough for structural scope |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Discernment shown in trade-offs and conservative design choices |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment adequately conveyed in Guidance trade-offs |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic insight demonstrated via discipline coordination and lifecycle cost |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Principled reasoning is consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add minimum concrete cover depths for reinforcement (clear cover to rebar) for each exposure class (below-grade, bay slabs, exterior); this is an essential factual parameter for durability design | Concrete cover depth is a fundamental durability parameter that directly governs corrosion protection of reinforcement; it is absent from Datasheet and Specification | Datasheet.md; Specification.md | Datasheet: Concrete Durability Parameters; Specification: entire document scanned | -- | Datasheet + Specification | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add seismic design parameters beyond Site Class C (e.g., spectral acceleration values Sa(0.2), Sa(1.0) for Penhold per NBCC) to complete the geotechnical parameter record | Datasheet lists seismic Site Class C but omits the spectral acceleration values needed for structural design; these are essential for foundation and frame design | Datasheet.md | Key Geotechnical Parameters table | -- | Datasheet | TBD |
| B-003 | B:information:completeness | RationaleGap | Guidance | Guidance | Add consideration for carbonation-induced corrosion as an exposure mechanism for above-grade concrete elements over a 50-year design life; explain whether carbonation is a material risk given the concrete quality specified | Carbonation is a recognized 50-year degradation mechanism for concrete reinforcement; the Guidance addresses sulphate, freeze-thaw, and chloride but is silent on carbonation | Guidance.md | Considerations section (entire section scanned) | -- | Guidance | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Mandatory Compliance Basis | 0 | NO_ITEMS | Mandatory compliance basis well-established across R-STR requirements |
| C:normative:sufficiency | normative | sufficiency | Regulatory Adequacy Threshold | 1 | HAS_ITEMS | DFT threshold for C2 zones not clearly mandatory |
| C:normative:completeness | normative | completeness | Complete Regulatory Scope | 0 | NO_ITEMS | Regulatory scope adequately complete for proposal stage |
| C:normative:consistency | normative | consistency | Uniform Regulatory Standard | 0 | NO_ITEMS | Standards references are uniform across documents |
| C:operative:necessity | operative | necessity | Essential Process Foundation | 0 | NO_ITEMS | Process foundations are adequately established |
| C:operative:sufficiency | operative | sufficiency | Proven Operational Method | 0 | NO_ITEMS | Methods are proven and cited to standards |
| C:operative:completeness | operative | completeness | Thorough Process Coverage | 0 | NO_ITEMS | Process coverage is thorough across four phases |
| C:operative:consistency | operative | consistency | Reliable Process Discipline | 0 | NO_ITEMS | Process discipline is reliable and consistent |
| C:evaluative:necessity | evaluative | necessity | Fundamental Value Criterion | 1 | HAS_ITEMS | Lifecycle cost estimate missing from Specification |
| C:evaluative:sufficiency | evaluative | sufficiency | Justified Quality Assessment | 0 | NO_ITEMS | Quality assessment is justified through examples and trade-offs |
| C:evaluative:completeness | evaluative | completeness | Exhaustive Value Accounting | 0 | NO_ITEMS | Value accounting adequate for proposal stage |
| C:evaluative:consistency | evaluative | consistency | Principled Value Consistency | 0 | NO_ITEMS | Consistent value principles across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:sufficiency | WeakStatement | Specification | Specification | Clarify whether C2 zone DFT of "~100 um" in R-STR-11 is a minimum requirement or a guideline; the tilde (~) makes it ambiguous as a regulatory adequacy threshold compared to C3 which specifies ">=150 um" | R-STR-11 uses approximate language ("~100 um") for C2 DFT while using precise language (">=150 um") for C3 DFT; this inconsistency could affect compliance determination | Specification.md | R-STR-11 | -- | Specification | TBD |
| C-002 | C:evaluative:necessity | VerificationGap | Specification | Specification | Add a requirement or verification point for lifecycle cost analysis to support the durability value proposition; Guidance and Procedure reference lifecycle cost but no Specification requirement mandates its production | Guidance T-001 and Procedure A6 reference lifecycle cost narrative but there is no corresponding requirement in Specification ensuring it is produced and verified | Specification.md; Guidance.md; Procedure.md | Specification: entire document scanned; Guidance: T-001; Procedure: Step A6 | -- | Specification | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandated Conformance Standard | 0 | NO_ITEMS | Conformance standards clearly mandated |
| F:normative:sufficiency | normative | sufficiency | Sufficient Compliance Proof | 1 | HAS_ITEMS | 56-day strength testing gap |
| F:normative:completeness | normative | completeness | Exhaustive Governance Record | 0 | NO_ITEMS | Governance records adequately specified |
| F:normative:consistency | normative | consistency | Coherent Governance Measure | 0 | NO_ITEMS | Governance measures are coherent |
| F:operative:necessity | operative | necessity | Critical Process Prerequisite | 0 | NO_ITEMS | Prerequisites are well-defined |
| F:operative:sufficiency | operative | sufficiency | Validated Procedural Capacity | 0 | NO_ITEMS | Procedural capacity is validated |
| F:operative:completeness | operative | completeness | Total Procedural Accounting | 0 | NO_ITEMS | Procedural accounting is complete across phases |
| F:operative:consistency | operative | consistency | Systematic Procedural Coherence | 1 | HAS_ITEMS | Terminology inconsistency on sump lining |
| F:evaluative:necessity | evaluative | necessity | Indispensable Quality Basis | 0 | NO_ITEMS | Quality basis is established |
| F:evaluative:sufficiency | evaluative | sufficiency | Defensible Merit Justification | 0 | NO_ITEMS | Merit justification is defensible |
| F:evaluative:completeness | evaluative | completeness | Holistic Quality Accounting | 0 | NO_ITEMS | Quality accounting is holistic |
| F:evaluative:consistency | evaluative | consistency | Principled Quality Coherence | 0 | NO_ITEMS | Quality coherence is principled |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add explicit acceptance/rejection criteria for 56-day concrete strength tests (R-STR-02 requires min 32 MPa at 56 days but verification table does not state what happens if 56-day strength falls below 32 MPa -- remediation protocol or rejection) | Sufficient compliance proof requires not only the test but also the consequence of failure; the verification matrix is silent on non-conformance actions for below-grade concrete | Specification.md | Verification: R-STR-02 row; R-STR-02 requirement text | -- | Specification | TBD |
| F-002 | F:operative:consistency | Normalization | Multi | Guidance | Normalize sump interior protection terminology: Specification R-STR-13 uses "epoxy coating, dense concrete, or stainless steel lining"; Guidance EX-001 uses "epoxy lining, stainless steel, or equivalent"; Procedure Step B2 uses "epoxy lining or stainless"; Datasheet uses "epoxy lining or equivalent" -- standardize the shortlist and terminology | Inconsistent terminology for sump interior protection options across documents could cause confusion during procurement and design; normalizing the vocabulary reduces drift risk | Specification.md; Guidance.md; Procedure.md; Datasheet.md | Spec: R-STR-13; Guidance: EX-001; Procedure: Step B2; Datasheet: Construction table | -- | Guidance (vocabulary note) + Specification (authoritative list) | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Binding Compliance Directive | 0 | NO_ITEMS | Binding directives are clear |
| D:normative:applying | normative | applying | Enforced Regulatory Fulfillment | 0 | NO_ITEMS | Regulatory fulfillment enforcement is addressed |
| D:normative:judging | normative | judging | Definitive Conformance Verdict | 0 | NO_ITEMS | Conformance verdict mechanisms exist in verification |
| D:normative:reviewing | normative | reviewing | Settled Compliance Assurance | 0 | NO_ITEMS | Compliance assurance is settled through inspection protocol |
| D:operative:guiding | operative | guiding | Resolved Operational Guidance | 1 | HAS_ITEMS | Missing guidance on structural monitoring instrumentation |
| D:operative:applying | operative | applying | Confirmed Process Deployment | 0 | NO_ITEMS | Process deployment is confirmed across phases |
| D:operative:judging | operative | judging | Settled Performance Verdict | 0 | NO_ITEMS | Performance verdicts addressed in verification |
| D:operative:reviewing | operative | reviewing | Settled Process Assurance | 0 | NO_ITEMS | Process assurance adequately settled |
| D:evaluative:guiding | evaluative | guiding | Grounded Quality Direction | 0 | NO_ITEMS | Quality direction is grounded in RFP and OBJ-005 |
| D:evaluative:applying | evaluative | applying | Justified Quality Practice | 1 | HAS_ITEMS | Waterproofing membrane not addressed for below-grade walls |
| D:evaluative:judging | evaluative | judging | Comprehensive Worth Verdict | 0 | NO_ITEMS | Worth verdict adequately addressed |
| D:evaluative:reviewing | evaluative | reviewing | Settled Quality Integrity | 0 | NO_ITEMS | Quality integrity is settled |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:operative:guiding | RationaleGap | Guidance | Guidance | Add consideration for whether structural health monitoring instrumentation (e.g., crack gauges, corrosion sensors on rebar) is warranted for a 50-year facility; explain the trade-off between instrumentation cost and early detection of concealed deterioration | Guidance addresses visual inspection thoroughly but does not discuss whether embedded monitoring instrumentation is appropriate for a 50-year design life; this is a gap in operational guidance for long-life infrastructure | Guidance.md | Considerations section (entire section scanned); Procedure Phase D | -- | Guidance | TBD |
| D-002 | D:evaluative:applying | TBD_Question | Datasheet | Datasheet | TBD: Is waterproofing membrane (beyond vapour barrier) required for below-grade foundation walls? Datasheet and Specification address positive drainage and sulphate-resistant concrete but are silent on exterior waterproofing membrane for below-grade walls -- consult geotechnical recommendations and building code | For a 50-year design life with groundwater at 3.0-4.0 m below grade, the question of whether below-grade walls need waterproofing membrane (not just drainage and sulphate-resistant concrete) is a justified quality practice concern | Datasheet.md; Specification.md | Datasheet: Construction table; Specification: R-STR-06, R-STR-07, R-STR-10 | -- | Structural Engineer / Geotechnical PE | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Authoritative Necessity Basis | 0 | NO_ITEMS | Authoritative necessity basis well-established |
| X:guiding:sufficiency | guiding | sufficiency | Prescribed Adequacy Assurance | 1 | HAS_ITEMS | Galvanizing inspection frequency gap |
| X:guiding:completeness | guiding | completeness | Comprehensive Directive Scope | 0 | NO_ITEMS | Directive scope is comprehensive |
| X:guiding:consistency | guiding | consistency | Coherent Directive Alignment | 0 | NO_ITEMS | Directive alignment is coherent |
| X:applying:necessity | applying | necessity | Mandatory Execution Basis | 0 | NO_ITEMS | Execution basis is mandatory where needed |
| X:applying:sufficiency | applying | sufficiency | Sufficient Deployment Proof | 1 | HAS_ITEMS | Missing concrete cover verification |
| X:applying:completeness | applying | completeness | Exhaustive Deployment Coverage | 0 | NO_ITEMS | Deployment coverage is exhaustive |
| X:applying:consistency | applying | consistency | Reliable Deployment Discipline | 0 | NO_ITEMS | Deployment discipline is reliable |
| X:judging:necessity | judging | necessity | Critical Adjudicative Ruling | 0 | NO_ITEMS | Adjudicative mechanisms are in place |
| X:judging:sufficiency | judging | sufficiency | Adequate Adjudicative Validation | 0 | NO_ITEMS | Validation is adequate |
| X:judging:completeness | judging | completeness | Exhaustive Adjudicative Scope | 0 | NO_ITEMS | Scope is exhaustive |
| X:judging:consistency | judging | consistency | Principled Adjudicative Standard | 0 | NO_ITEMS | Standards are principled |
| X:reviewing:necessity | reviewing | necessity | Critical Assurance Verification | 1 | HAS_ITEMS | Pile integrity testing not specified |
| X:reviewing:sufficiency | reviewing | sufficiency | Sufficient Assurance Revalidation | 0 | NO_ITEMS | Revalidation is sufficient |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Assurance Review | 0 | NO_ITEMS | Review coverage is exhaustive |
| X:reviewing:consistency | reviewing | consistency | Coherent Assurance Discipline | 0 | NO_ITEMS | Assurance discipline is coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | VerificationGap | Procedure | Procedure | Add galvanizing thickness verification method and frequency for field-installed members (Procedure Step C4 references ASTM A123 and ">=70 um" but field verification frequency is not specified beyond "Fabrication" -- post-transport damage checking needs explicit protocol) | Prescribed adequacy assurance requires field verification of galvanizing condition after transport and erection; current procedure only checks at fabrication | Procedure.md | Phase C: Step C4; Verification checklist: Galvanizing thickness row | -- | Procedure | TBD |
| X-002 | X:applying:sufficiency | VerificationGap | Specification | Specification | Add concrete cover depth verification to the inspection and testing plan (if B-001 is resolved and cover depths are specified, a corresponding verification method such as covermeter survey should be added) | If minimum cover depths are specified per B-001, there must be a corresponding deployment proof mechanism to verify they are achieved in construction | Specification.md | Inspection and Testing Plan | -- | Specification | TBD |
| X-003 | X:reviewing:necessity | MissingSlot | Specification | Specification | Add pile integrity testing requirement (e.g., PDA testing or equivalent) for driven pile foundations to verify critical assurance of pile capacity and embedment depth during construction | Specification R-STR-06 and R-STR-08 specify pile foundation requirements but the verification table does not include pile integrity testing; for a 50-year design life, pile installation verification is a critical assurance need | Specification.md | Verification: R-STR-06, R-STR-08 rows | -- | Specification | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Compulsory Governance Foundation | 0 | NO_ITEMS | Governance foundation is compulsory and well-documented |
| E:normative:sufficiency | normative | sufficiency | Validated Regulatory Sufficiency | 0 | NO_ITEMS | Regulatory sufficiency is validated through verification matrix |
| E:normative:completeness | normative | completeness | Total Regulatory Coverage | 0 | NO_ITEMS | Regulatory coverage is total for proposal stage |
| E:normative:consistency | normative | consistency | Harmonized Compliance Discipline | 1 | HAS_ITEMS | Conflict on concrete strength specification |
| E:operative:necessity | operative | necessity | Imperative Operational Certainty | 0 | NO_ITEMS | Operational certainty is established |
| E:operative:sufficiency | operative | sufficiency | Confirmed Operational Adequacy | 0 | NO_ITEMS | Operational adequacy is confirmed |
| E:operative:completeness | operative | completeness | Exhaustive Operational Accounting | 0 | NO_ITEMS | Operational accounting is exhaustive |
| E:operative:consistency | operative | consistency | Systematic Operational Reliability | 0 | NO_ITEMS | Operational reliability is systematic |
| E:evaluative:necessity | evaluative | necessity | Imperative Quality Foundation | 1 | HAS_ITEMS | Wear/abrasion resistance not addressed |
| E:evaluative:sufficiency | evaluative | sufficiency | Validated Quality Sufficiency | 0 | NO_ITEMS | Quality sufficiency is validated |
| E:evaluative:completeness | evaluative | completeness | Exhaustive Quality Determination | 0 | NO_ITEMS | Quality determination is exhaustive for scope |
| E:evaluative:consistency | evaluative | consistency | Principled Quality Assurance | 0 | NO_ITEMS | Quality assurance is principled |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:consistency | Conflict | Multi | TBD | Resolve inconsistency in bay slab compressive strength: Specification R-STR-02 requires "minimum 32 MPa at 56 days" for below-grade concrete; Guidance EX-001 states "minimum 35 MPa" for apparatus bay slab; R-STR-05 (bay slabs) does not specify a compressive strength -- clarify which value governs bay slab concrete | Documents disagree on the compressive strength for bay slab concrete: R-STR-02 says 32 MPa (for below-grade), EX-001 says 35 MPa (for bay slabs), and R-STR-05 (the bay slab requirement) is silent on strength. This creates compliance discipline ambiguity | Specification.md; Guidance.md | Specification: R-STR-02, R-STR-05; Guidance: EX-001 | Specification.md#R-STR-02 (32 MPa); Guidance.md#EX-001 (35 MPa); Specification.md#R-STR-05 (silent) | Specification (authoritative) | TBD |
| E-002 | E:evaluative:necessity | WeakStatement | Specification | Specification | Add abrasion/wear resistance requirement for bay slab concrete (apparatus and PW bays subject to heavy vehicle traffic including fire apparatus); specify minimum abrasion resistance class or surface hardener requirement | Bay slabs are subject to heavy vehicle traffic (fire apparatus, heavy equipment) but neither Specification nor Datasheet addresses abrasion/wear resistance as a quality foundation requirement distinct from freeze-thaw and chloride protection | Specification.md; Datasheet.md | Specification: R-STR-05; Datasheet: Primary Scope Elements table | -- | Specification | TBD |
