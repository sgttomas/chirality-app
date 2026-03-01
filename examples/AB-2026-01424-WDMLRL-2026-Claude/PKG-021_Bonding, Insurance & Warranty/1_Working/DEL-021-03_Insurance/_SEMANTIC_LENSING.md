# Semantic Lensing Register: DEL-021-03 Insurance Package

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-021_Bonding, Insurance & Warranty/1_Working/DEL-021-03_Insurance
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-021-03_Insurance/_CONTEXT.md (Deliverable Overview, Scope Definition, Success Criteria)
- _STATUS.md — DEL-021-03_Insurance/_STATUS.md (Status: SEMANTIC_READY)
- _SEMANTIC.md — DEL-021-03_Insurance/_SEMANTIC.md (Matrices A, B, C, F, D, X, E parsed)
- Datasheet.md — DEL-021-03_Insurance/Datasheet.md (Coverage types, limits, conditions, construction artifacts)
- Specification.md — DEL-021-03_Insurance/Specification.md (Requirements REQ-INS-001 through REQ-INS-010, verification, documentation)
- Guidance.md — DEL-021-03_Insurance/Guidance.md (Purpose, principles, considerations, trade-offs, conflict table)
- Procedure.md — DEL-021-03_Insurance/Procedure.md (Phases 1-3, steps 1-14, verification, records)
- _REFERENCES.md — DEL-021-03_Insurance/_REFERENCES.md (read; primary and related references listed)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 19
- By document:
  - Datasheet: 5
  - Specification: 7
  - Guidance: 4
  - Procedure: 3
- By matrix:
  - A: 4  B: 3  C: 2  F: 3  D: 2  X: 3  E: 2
- By type:
  - Conflict: 1
  - VerificationGap: 3
  - MissingSlot: 5
  - WeakStatement: 3
  - RationaleGap: 2
  - Normalization: 3
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | CGL vs. auto terminology conflict affects prescriptive direction |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Insurer qualification requirement is assumed, not mandated |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | No acceptance criteria for insurer financial strength |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | No audit trail mechanism for mid-project policy changes |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure covers phase-gated workflow adequately |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Steps 1-14 provide sufficient execution detail |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification table in Procedure covers performance checks |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records section in Procedure supports process audit |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Purpose section addresses value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs table in Guidance addresses merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Limit adequacy vs. premium cost trade-off addressed |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | County acceptance confirmation serves as quality appraisal |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | Conflict | Multi | Specification | Clarify whether REQ-INS-001 covers CGL (Commercial General Liability) or solely automobile/auto-liability policy; align terminology across Datasheet, Specification, and Guidance | RFP section 4.2.1 heading says "Standard automobile, bodily injury, and property damage insurance" but Decomposition SOW-0102 uses "CGL". Guidance CONF-INS-001 flags this but it remains unresolved in the normative documents. Different interpretations would yield different policy types and coverage scopes. | Specification.md, Datasheet.md, Guidance.md | Specification.md#REQ-INS-001, Datasheet.md#Required Coverage Types and Limits, Guidance.md#Conflict Table | Specification.md#REQ-INS-001 ("automobile, bodily injury, and property damage"), Guidance.md#CONF-INS-001 (proposes combined CGL + auto interpretation) | PROPOSAL: County or legal counsel to confirm policy type interpretation | TBD |
| A-002 | A:normative:applying | WeakStatement | Datasheet | Specification | Add explicit requirement for insurer qualification (licensed to conduct business in Alberta) rather than relying on assumption | Datasheet lists "Insurer Qualifications" as an artifact with an ASSUMPTION note. This is a mandatory practice concern: if this is actually required, it should be a normative requirement, not an assumption in a descriptive document. | Datasheet.md | Datasheet.md#Construction (Insurer Qualifications row) | | PROPOSAL: Specification.md should contain a requirement if insurer licensing is obligatory | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add acceptance criteria for insurer financial strength or licensing status in the Verification table | Specification Verification table checks policy limits and endorsements but has no verification step for insurer qualification (financial rating, Alberta licensing). Under the compliance determination lens, this is a gap in how compliance is judged. | Specification.md | Specification.md#Verification | | PROPOSAL: Add verification row for insurer licensing | TBD |
| A-004 | A:normative:reviewing | MissingSlot | Procedure | Procedure | Add a step or record entry for documenting and auditing mid-project policy changes (endorsements, renewals, insurer changes) beyond just renewal certificates | Procedure Step 12 addresses renewal certificates but does not describe how to handle mid-project policy amendments, insurer changes, or coverage modifications. Under a regulatory audit lens, this is a gap in the audit trail for policy lifecycle events. | Procedure.md | Procedure.md#Phase 3: Ongoing Maintenance | | PROPOSAL: Procedure.md add audit log mechanism for policy lifecycle events | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | RFP section reference discrepancy |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Coverage types and limits adequately evidenced from RFP |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Missing builder's risk / course of construction insurance consideration |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Coverage limits are consistently stated as $5M across documents |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (coverage types, timing, additional insured) present |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for each coverage type adequate in Guidance Considerations |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Information coverage appears comprehensive across the four documents |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | RFP section reference inconsistency between _CONTEXT.md and Datasheet |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Guidance provides fundamental understanding of insurance principles |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Broker engagement guidance provides sufficient expertise direction |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Guidance Considerations cover WCB, E&O, environmental, and subcontractor topics |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs table provides essential discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment guidance for blanket vs. specific endorsements adequate |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance provides holistic insurance program view |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning consistent across Guidance sections |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | Normalization | Multi | Datasheet | Normalize the RFP section reference for insurance: _CONTEXT.md cites "RFP section 2.12" while Datasheet and Specification cite "RFP section 4.2" as the governing source | _CONTEXT.md Regulatory Context says "Based on Main RFP section 2.12 (Insurance Requirements)" but Datasheet Identification table says "Governing Source: RFP section 4.2". These may be different sections or one may be in error. This is an essential fact discrepancy that could cause confusion about which RFP section is authoritative for insurance. | _CONTEXT.md, Datasheet.md | _CONTEXT.md#Regulatory Context, Datasheet.md#Identification | _CONTEXT.md#Regulatory Context ("RFP section 2.12"), Datasheet.md#Identification ("RFP section 4.2") | PROPOSAL: Confirm correct RFP section number(s) and align across all documents | TBD |
| B-002 | B:data:completeness | TBD_Question | Datasheet | Datasheet | Confirm whether builder's risk / course of construction insurance is required or whether it falls under "other insurance as County may reasonably require" (REQ-INS-005) | For a design-build construction project, builder's risk insurance is a standard coverage type. The RFP section 4.2 does not list it explicitly, but CCDC 14-2013 typically addresses it. Under the comprehensive record lens, this is a potential gap in the data inventory. | Datasheet.md, Specification.md | Datasheet.md#Required Coverage Types and Limits, Specification.md#REQ-INS-005 | | PROPOSAL: Review CCDC 14-2013 insurance provisions when contract is accessible | TBD |
| B-003 | B:information:consistency | Normalization | Multi | Datasheet | Align _REFERENCES.md section reference ("section 2.12") with Datasheet governing source ("section 4.2") | _REFERENCES.md Primary References says "Section section 2.12 -- Insurance Requirements and Coverage Specifications" while Datasheet uses "section 4.2". This reinforces the section reference discrepancy identified in B-001 and adds another location where the inconsistency appears. | _REFERENCES.md, Datasheet.md | _REFERENCES.md#Primary References, Datasheet.md#Identification | _REFERENCES.md ("section 2.12"), Datasheet.md ("section 4.2") | PROPOSAL: Single correct section reference to be confirmed and applied consistently | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Obligatory Compliance Foundation | 1 | HAS_ITEMS | CCDC 14-2013 insurance clauses not yet accessible |
| C:normative:sufficiency | normative | sufficiency | Certified Regulatory Acceptance | 0 | NO_ITEMS | County acceptance process addressed in Procedure Step 10 |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Adherence | 1 | HAS_ITEMS | E&O tail coverage not addressed normatively |
| C:normative:consistency | normative | consistency | Harmonized Compliance Standard | 0 | NO_ITEMS | Compliance standards consistently referenced |
| C:operative:necessity | operative | necessity | Core Execution Prerequisite | 0 | NO_ITEMS | Pre-procurement trigger (award notification) clearly stated |
| C:operative:sufficiency | operative | sufficiency | Capable Performance Assurance | 0 | NO_ITEMS | Phase-gated procedure provides capable assurance |
| C:operative:completeness | operative | completeness | Comprehensive Execution Coverage | 0 | NO_ITEMS | Steps 1-14 provide comprehensive coverage of the execution lifecycle |
| C:operative:consistency | operative | consistency | Systematic Operational Uniformity | 0 | NO_ITEMS | Procedure steps follow consistent format |
| C:evaluative:necessity | evaluative | necessity | Foundational Merit Criterion | 0 | NO_ITEMS | Risk transfer purpose clearly articulated as foundational merit |
| C:evaluative:sufficiency | evaluative | sufficiency | Defensible Value Appraisal | 0 | NO_ITEMS | Trade-offs table provides defensible value reasoning |
| C:evaluative:completeness | evaluative | completeness | Holistic Value Accounting | 0 | NO_ITEMS | Cost, coverage scope, and owner protection all accounted for |
| C:evaluative:consistency | evaluative | consistency | Principled Value Consistency | 0 | NO_ITEMS | Value principles consistent across Guidance |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | TBD_Question | Specification | Specification | Record TBD: Obtain and review CCDC 14-2013 insurance clauses (GC 11.1 or equivalent) to confirm whether the contract form imposes additional insurance requirements beyond RFP section 4.2 | Under the Obligatory Compliance Foundation lens, the normative base must include all binding insurance obligations. CCDC 14-2013 is referenced as the contract form but its insurance clauses are not accessible. The Specification Standards table correctly flags this as "Not accessible in source set" but no action item exists to close this gap. | Specification.md | Specification.md#Standards (CCDC 14-2013 row) | | PROPOSAL: Obtain CCDC 14-2013 at contract execution (DEL-021-04) and reconcile with requirements | TBD |
| C-002 | C:normative:completeness | RationaleGap | Guidance | Guidance | Add rationale or recommendation regarding E&O tail coverage / extended reporting period requirement, with explicit connection to the 2-year guarantee period | Guidance Considerations section mentions E&O tail coverage as an ASSUMPTION-level recommendation but does not connect it to a normative requirement or explain what happens if tail coverage is not obtained. Under the Exhaustive Regulatory Adherence lens, this gap means a potential post-completion exposure is identified but not resolved. | Guidance.md | Guidance.md#Considerations (Professional Liability E&O Scope) | | PROPOSAL: Guidance should state whether tail coverage is recommended or required, with rationale linked to guarantee period | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandatory Compliance Certification | 1 | HAS_ITEMS | Missing explicit requirement for insurance certificate format |
| F:normative:sufficiency | normative | sufficiency | Prescribed Competence Threshold | 0 | NO_ITEMS | Broker engagement guidance sufficient |
| F:normative:completeness | normative | completeness | Exhaustive Regulatory Obligation | 1 | HAS_ITEMS | Subcontractor insurance flow-down not normatively addressed |
| F:normative:consistency | normative | consistency | Uniform Compliance Protocol | 0 | NO_ITEMS | Compliance protocol consistently described |
| F:operative:necessity | operative | necessity | Operational Activation Prerequisite | 0 | NO_ITEMS | Contract award trigger clearly established |
| F:operative:sufficiency | operative | sufficiency | Capable Operational Sufficiency | 0 | NO_ITEMS | Procedure provides sufficient operational detail |
| F:operative:completeness | operative | completeness | Total Operational Command | 0 | NO_ITEMS | Procedure covers full lifecycle (procurement through maintenance) |
| F:operative:consistency | operative | consistency | Disciplined Operational Consistency | 0 | NO_ITEMS | Consistent step formatting and phase structure |
| F:evaluative:necessity | evaluative | necessity | Intrinsic Worth Indicator | 0 | NO_ITEMS | Risk transfer purpose clearly stated |
| F:evaluative:sufficiency | evaluative | sufficiency | Justified Worth Assessment | 0 | NO_ITEMS | Trade-off analysis provides justified assessment |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Valuation Scope | 1 | HAS_ITEMS | No cost estimate or budget range for insurance program |
| F:evaluative:consistency | evaluative | consistency | Principled Valuation Alignment | 0 | NO_ITEMS | Valuation principles consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | WeakStatement | Specification | Specification | Clarify whether ACORD 25 or equivalent certificate format is a mandatory requirement or merely an assumption; if mandatory, add as a normative requirement | Procedure Step 5 states "ASSUMPTION: Standard ACORD 25 or equivalent forms are used" and Datasheet lists "Standard ACORD-form or equivalent certificates" with "ASSUMPTION: standard industry practice; format not prescribed in RFP". Under the Mandatory Compliance Certification lens, the certification format is ambiguous -- it is referenced operationally but never normatively required. | Specification.md, Procedure.md, Datasheet.md | Specification.md#Documentation, Procedure.md#Step 5, Datasheet.md#Construction | | PROPOSAL: Either add REQ-INS-011 for certificate format or explicitly note format is not mandated | TBD |
| F-002 | F:normative:completeness | WeakStatement | Specification | Specification | Strengthen subcontractor insurance flow-down from ASSUMPTION to explicit requirement or confirmed exclusion; clarify whether the Proponent must require subcontractors to carry independent coverage | Specification Exclusions says "ASSUMPTION: each subcontractor is responsible for their own insurance". Guidance repeats this as ASSUMPTION. Under the Exhaustive Regulatory Obligation lens, the subcontractor insurance obligation is identified but never resolved -- it is stated as an assumption in three different documents without a definitive position. | Specification.md, Guidance.md, Datasheet.md | Specification.md#What This Deliverable Excludes, Guidance.md#Considerations (Subcontractor Insurance), Datasheet.md#Conditions (Subcontractor insurance) | | PROPOSAL: Confirm with County at contract negotiation; resolve ASSUMPTION to requirement or exclusion | TBD |
| F-003 | F:evaluative:completeness | MissingSlot | Datasheet | Datasheet | Add estimated budget range or cost considerations for the insurance program to support comprehensive valuation | Under the Comprehensive Valuation Scope lens, there is no cost data or budget range for insurance premiums anywhere in the four documents. Guidance Trade-offs mentions "premium cost" as a factor but provides no estimates. For a deliverable in the Commercial category, cost information would support valuation completeness. | Datasheet.md, Guidance.md | Datasheet.md#entire document scanned, Guidance.md#Trade-offs | | PROPOSAL: Add insurance cost estimate section to Datasheet when quotes are obtained | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Prescriptive Regulatory Closure | 1 | HAS_ITEMS | Open ASSUMPTION items prevent regulatory closure |
| D:normative:applying | normative | applying | Enforced Capability Resolution | 0 | NO_ITEMS | Capability requirements sufficiently enforced through REQ-INS series |
| D:normative:judging | normative | judging | Definitive Obligation Ruling | 0 | NO_ITEMS | Requirements trace to RFP source sections |
| D:normative:reviewing | normative | reviewing | Settled Regulatory Inspection | 0 | NO_ITEMS | Verification table supports inspection |
| D:operative:guiding | operative | guiding | Resolved Workflow Initiation | 0 | NO_ITEMS | Phase 1 initiation clearly resolved |
| D:operative:applying | operative | applying | Settled Operational Delivery | 0 | NO_ITEMS | Steps provide settled delivery sequence |
| D:operative:judging | operative | judging | Resolved Performance Verdict | 0 | NO_ITEMS | Procedure Verification table covers performance verdicts |
| D:operative:reviewing | operative | reviewing | Settled Process Examination | 0 | NO_ITEMS | Records section supports process examination |
| D:evaluative:guiding | evaluative | guiding | Resolved Worth Orientation | 0 | NO_ITEMS | Purpose and Principles provide worth orientation |
| D:evaluative:applying | evaluative | applying | Concluded Merit Application | 0 | NO_ITEMS | Merit considerations applied through trade-offs |
| D:evaluative:judging | evaluative | judging | Final Worth Determination | 1 | HAS_ITEMS | No mechanism to assess whether coverage is optimized vs. merely compliant |
| D:evaluative:reviewing | evaluative | reviewing | Settled Quality Review | 0 | NO_ITEMS | County acceptance serves as quality review |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:guiding | MissingSlot | Specification | Guidance | Add an ASSUMPTION resolution tracker or index that lists all open ASSUMPTIONs across the four documents with their resolution status and decision owner | Under the Prescriptive Regulatory Closure lens, multiple ASSUMPTIONs are scattered across Datasheet (4), Specification (2), Guidance (4), and Procedure (4). These prevent normative closure because they represent unresolved decision points. No single location tracks them for resolution. | Datasheet.md, Specification.md, Guidance.md, Procedure.md | entire document scanned (all four) | | PROPOSAL: Guidance or a metadata file should contain an ASSUMPTION register | TBD |
| D-002 | D:evaluative:judging | RationaleGap | Guidance | Guidance | Add guidance on how to evaluate whether the insurance program is optimized (not just compliant), considering project-specific risk factors such as landfill-adjacent environmental exposure | Under the Final Worth Determination lens, the Guidance Trade-offs table mentions "consider higher limits for auto/CGL only if project risk profile warrants" but provides no framework for making that determination. For a landfill-adjacent construction site, the worth determination of environmental coverage adequacy is particularly relevant. | Guidance.md | Guidance.md#Trade-offs, Guidance.md#Considerations (Environmental Liability Sub-Coverage) | | PROPOSAL: Add risk-based coverage optimization guidance | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Prescribed Activation Baseline | 0 | NO_ITEMS | Activation baseline (award notification trigger) clearly prescribed |
| X:guiding:sufficiency | guiding | sufficiency | Adequate Directive Framing | 0 | NO_ITEMS | Guidance framing is adequate |
| X:guiding:completeness | guiding | completeness | Exhaustive Directive Coverage | 0 | NO_ITEMS | Guidance covers all major topics |
| X:guiding:consistency | guiding | consistency | Harmonized Directive Stability | 0 | NO_ITEMS | Directive messaging is stable |
| X:applying:necessity | applying | necessity | Required Execution Competence | 1 | HAS_ITEMS | No competence criteria for insurance broker selection |
| X:applying:sufficiency | applying | sufficiency | Sufficient Implementation Proof | 0 | NO_ITEMS | Certificate and endorsement submission provides sufficient proof |
| X:applying:completeness | applying | completeness | Total Implementation Record | 1 | HAS_ITEMS | No checklist for complete policy review before County submission |
| X:applying:consistency | applying | consistency | Consistent Implementation Alignment | 0 | NO_ITEMS | Implementation steps align with requirements |
| X:judging:necessity | judging | necessity | Foundational Adjudicative Datum | 0 | NO_ITEMS | Verification approach per requirement provides adjudicative data |
| X:judging:sufficiency | judging | sufficiency | Sufficient Adjudicative Proof | 0 | NO_ITEMS | Certificate review approach provides sufficient proof |
| X:judging:completeness | judging | completeness | Exhaustive Adjudicative Record | 1 | HAS_ITEMS | Verification table missing cross-reference to Datasheet sub-coverages |
| X:judging:consistency | judging | consistency | Uniform Adjudicative Standard | 0 | NO_ITEMS | Verification approach consistent across requirements |
| X:reviewing:necessity | reviewing | necessity | Foundational Audit Trigger | 0 | NO_ITEMS | Policy expiry dates serve as audit triggers |
| X:reviewing:sufficiency | reviewing | sufficiency | Sufficient Audit Evidence | 0 | NO_ITEMS | Records section provides sufficient evidence base |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Audit Documentation | 0 | NO_ITEMS | Records table covers key documentation types |
| X:reviewing:consistency | reviewing | consistency | Consistent Audit Standard | 0 | NO_ITEMS | Audit approach consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | MissingSlot | Procedure | Procedure | Add broker selection criteria or minimum qualifications (e.g., experience with Alberta construction, CCDC contracts, landfill-adjacent projects) | Guidance Principle 2 says "requires a broker experienced with Alberta construction projects and CCDC contract requirements" but Procedure Step 2 only says "Brief Insurance Broker" without specifying how the broker is selected or what qualifications are needed. Under the Required Execution Competence lens, the competence criteria for a key execution role are missing from the operational document. | Procedure.md, Guidance.md | Procedure.md#Step 2, Guidance.md#Principles (Principle 2) | | PROPOSAL: Add broker qualification criteria to Procedure prerequisites or Step 1 | TBD |
| X-002 | X:applying:completeness | VerificationGap | Procedure | Procedure | Expand the Step 8 checklist to include verification of all six sub-coverages under REQ-INS-001 (currently the checklist only confirms top-level policy presence, not sub-coverage completeness) | Procedure Step 8 checklist checks for high-level document presence but does not verify that all six sub-coverages under section 4.2.1 (non-owned auto, independent subcontractors, contractual liability, broad form property damage, environmental liability, product and completed operations) are individually confirmed. Under the Total Implementation Record lens, this is an incomplete verification checkpoint. | Procedure.md, Specification.md | Procedure.md#Step 8, Specification.md#REQ-INS-001 | | PROPOSAL: Expand Step 8 checklist or add sub-coverage verification step | TBD |
| X-003 | X:judging:completeness | VerificationGap | Specification | Specification | Add verification cross-reference confirming that each of the six sub-coverages under REQ-INS-001 is individually verified, not just the aggregate policy limit | Specification Verification table row for REQ-INS-001 says "confirm $5M limit and all six sub-coverages listed" but does not specify how each sub-coverage is individually verified (e.g., by endorsement review, by schedule confirmation). Under the Exhaustive Adjudicative Record lens, the verification approach lacks granularity for sub-requirements. | Specification.md | Specification.md#Verification (REQ-INS-001 row) | | PROPOSAL: Break REQ-INS-001 verification into sub-coverage verification steps | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Authoritative Guidance Record | 0 | NO_ITEMS | Guidance record is authoritative with source citations |
| E:guiding:information | guiding | information | Coherent Guidance Signal | 0 | NO_ITEMS | Guidance signals are coherent |
| E:guiding:knowledge | guiding | knowledge | Commanding Directive Expertise | 0 | NO_ITEMS | Guidance demonstrates domain expertise |
| E:guiding:wisdom | guiding | wisdom | Grounded Directive Wisdom | 0 | NO_ITEMS | Wisdom-level guidance present in trade-offs and considerations |
| E:applying:data | applying | data | Verified Execution Record | 1 | HAS_ITEMS | Missing record-keeping for broker communications |
| E:applying:information | applying | information | Coherent Execution Status | 0 | NO_ITEMS | Execution status tracking adequate through phase gates |
| E:applying:knowledge | applying | knowledge | Demonstrated Implementation Mastery | 0 | NO_ITEMS | Implementation steps demonstrate sufficient mastery |
| E:applying:wisdom | applying | wisdom | Sound Implementation Judgment | 0 | NO_ITEMS | Implementation judgment sound (60-day renewal lead time, etc.) |
| E:judging:data | judging | data | Verified Evidentiary Record | 0 | NO_ITEMS | Evidentiary records specified in Procedure Records table |
| E:judging:information | judging | information | Structured Judgment Report | 0 | NO_ITEMS | Verification table provides structured judgment framework |
| E:judging:knowledge | judging | knowledge | Commanding Adjudicative Authority | 0 | NO_ITEMS | Requirements trace to RFP sections providing authority |
| E:judging:wisdom | judging | wisdom | Principled Judicial Insight | 0 | NO_ITEMS | Conflict table preserves human ruling rights |
| E:reviewing:data | reviewing | data | Verified Audit Record | 1 | HAS_ITEMS | No version control or revision tracking mechanism specified for insurance documents |
| E:reviewing:information | reviewing | information | Structured Audit Report | 0 | NO_ITEMS | Records table provides structured audit framework |
| E:reviewing:knowledge | reviewing | knowledge | Commanding Audit Proficiency | 0 | NO_ITEMS | Audit approach demonstrates proficiency |
| E:reviewing:wisdom | reviewing | wisdom | Principled Audit Wisdom | 0 | NO_ITEMS | Retention periods aligned with guarantee period |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:applying:data | MissingSlot | Procedure | Procedure | Add a record type for broker correspondence and instructions log (documenting what was communicated to the broker and when) | Procedure Steps 1-3 involve briefing and instructing the broker but the Records table does not include a record type for broker communications. Under the Verified Execution Record lens, there is no evidentiary trail for what instructions were given to the broker, which could be important if a coverage dispute arises. | Procedure.md | Procedure.md#Records | | PROPOSAL: Add "Broker Instructions and Correspondence Log" to Records table | TBD |
| E-002 | E:reviewing:data | Normalization | Datasheet | Datasheet | Add document revision tracking convention or version history section to Datasheet to support audit record integrity as insurance documents evolve through the project lifecycle | Datasheet header shows "Revision: Draft P1" but there is no revision history table or version control mechanism. All four production documents share this pattern. Under the Verified Audit Record lens, as insurance documents are updated (renewals, amendments), the lack of revision tracking could compromise audit trail integrity. | Datasheet.md | Datasheet.md#header (Revision field) | | PROPOSAL: Add revision history table to Datasheet (and consider for all four documents) | TBD |
