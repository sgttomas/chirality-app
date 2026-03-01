# Semantic Lensing Register: DEL-014-03 Bulk Water Fill System

**Generated:** 2026-02-26
**Deliverable Folder:** PKG-014_Plumbing & Water Systems Installation/1_Working/DEL-014-03_Bulk-Water
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-014-03_Bulk-Water/_CONTEXT.md
- _STATUS.md — DEL-014-03_Bulk-Water/_STATUS.md (SEMANTIC_READY)
- _SEMANTIC.md — DEL-014-03_Bulk-Water/_SEMANTIC.md
- Datasheet.md — DEL-014-03_Bulk-Water/Datasheet.md (R0)
- Specification.md — DEL-014-03_Bulk-Water/Specification.md (R0)
- Guidance.md — DEL-014-03_Bulk-Water/Guidance.md (R0)
- Procedure.md — DEL-014-03_Bulk-Water/Procedure.md (R0)
- _REFERENCES.md — DEL-014-03_Bulk-Water/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 23
- By document:
  - Datasheet: 3
  - Specification: 10
  - Guidance: 3
  - Procedure: 5
  - Multi: 2
- By matrix:
  - A: 5  B: 2  C: 3  F: 3  D: 3  X: 3  E: 4
- By type:
  - Conflict: 2
  - VerificationGap: 5
  - MissingSlot: 6
  - WeakStatement: 3
  - RationaleGap: 2
  - Normalization: 3
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 2
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Backflow prevention and freeze protection codes cited as ASSUMPTION only |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Multiple REQs sourced to ASSUMPTION rather than confirmed mandatory authority |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | No specific Alberta Plumbing Code edition cited |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Safety Codes Officer inspection is addressed in Procedure and Specification Verification |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | Cistern interface ownership gap |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Procedure steps are well-sequenced for practical execution |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | Pump flow rate acceptance criterion is TBD |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Procedure records and verification table are adequate |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance P-1 and P-2 establish value orientation adequately |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Documents adequately position system as critical infrastructure |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | No gap identified; value proposition is clear |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Commissioning and verification checks address quality appraisal |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify REQ-014-03-06 source: replace ASSUMPTION classification with confirmed Alberta Plumbing Code clause reference for backflow prevention requirement | REQ-014-03-06 is classified as ASSUMPTION but backflow prevention is a code requirement; the prescriptive direction is asserted without confirmed regulatory citation | Specification.md | REQ-014-03-06 | -- | Plumbing engineer to confirm specific code clause | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Confirm classification of REQ-014-03-07 (Freeze Protection) and REQ-014-03-08 (Electrical Coordination) -- currently ASSUMPTION; elevate to Mandatory with code citation if warranted | Three requirements (REQ-06, 07, 08) carry ASSUMPTION classification, meaning mandatory practice is asserted without confirmed authority | Specification.md | REQ-014-03-07, REQ-014-03-08 | -- | Plumbing engineer / design team | TBD |
| A-003 | A:normative:judging | MissingSlot | Specification | Specification | Add specific Alberta Plumbing Code edition and year (e.g., NPC 2020 as adopted in Alberta) to Standards table | Standards table lists "Alberta Plumbing Code (NPC as adopted in AB)" but edition/year is noted as "location TBD"; compliance determination requires a specific code edition reference | Specification.md | Standards table | -- | PM / plumbing engineer to confirm applicable edition | TBD |
| A-004 | A:operative:guiding | MissingSlot | Procedure | Procedure | Add explicit interface ownership statement: which deliverable (DEL-014-03 or DEL-014-01) owns the cistern-side connection fitting and isolation valve | Step 2.4 states "confirm in writing which deliverable owns each component at the cistern interface" but the Procedure itself does not resolve this; procedural direction is incomplete at this boundary | Procedure.md | Step 2.4 — Cistern Inlet Connection | -- | Plumbing Contractor + PM to document scope split | TBD |
| A-005 | A:operative:judging | VerificationGap | Specification | Specification | Add quantitative acceptance criterion for pump flow rate in REQ-014-03-02 verification row (currently deferred to IFC design) | Verification table for REQ-014-03-02 says "measure flow rate against design spec" but design spec LPM is TBD; performance assessment cannot be performed without a numeric target | Specification.md | Verification table, REQ-014-03-02 row | -- | Plumbing engineer (PKG-006 IFC) | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Pump flow rate is an essential fact that is TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Available evidence from RFP is adequately documented in Datasheet |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Several Datasheet attributes are TBD |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Datasheet sourcing is consistent and traceable |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (scope, dependencies, exclusions) are present |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Guidance provides adequate context for the deliverable |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Documents together provide a comprehensive account |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Cross-document messaging is coherent |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding of system purpose is well-established |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Documents assume competent plumbing contractor; adequate |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | No gap identified |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is consistent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Guidance trade-offs section provides essential discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment calls (trade-offs T-1, T-2, T-3) are surfaced for decision |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Guidance provides holistic insight into system context |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning across Guidance is principled and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Confirm bulk fill pump flow rate (LPM) from plumbing engineer/IFC design. This is an essential fact required for downstream verification and procurement | Pump flow rate is the most critical performance datum for this system and remains TBD across all documents; without it, pump selection and acceptance testing cannot proceed | Datasheet.md | Attributes — Pump Flow Rate | -- | Plumbing engineer (PKG-006) | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add fill connection size, pipe material, and fill connection hardware type to Datasheet Attributes once resolved in IFC design; currently three TBD entries in Construction table | Datasheet Construction section has three TBD entries (Fill Line Pipe Material, Fill Connection Hardware, Pump Equipment specifics); comprehensive record is incomplete pending design | Datasheet.md | Construction table | -- | Plumbing engineer (PKG-006) | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Obligatory Regulatory Baseline | 1 | HAS_ITEMS | CSA B64 series listed as ASSUMPTION |
| C:normative:sufficiency | normative | sufficiency | Substantiated Conformance Warrant | 0 | NO_ITEMS | Conformance warrant chain (RFP -> Spec -> Verification) is present |
| C:normative:completeness | normative | completeness | Total Compliance Coverage | 0 | NO_ITEMS | All mandatory requirements have verification entries |
| C:normative:consistency | normative | consistency | Harmonized Regulatory Accord | 1 | HAS_ITEMS | Terminology inconsistency for plumbing code reference |
| C:operative:necessity | operative | necessity | Critical Operational Prerequisite | 1 | HAS_ITEMS | Missing prerequisite: cistern level monitoring coordination |
| C:operative:sufficiency | operative | sufficiency | Verified Execution Adequacy | 0 | NO_ITEMS | Procedure steps are sufficient for verified execution |
| C:operative:completeness | operative | completeness | Exhaustive Process Accounting | 0 | NO_ITEMS | Procedure phases 1-6 provide exhaustive process coverage |
| C:operative:consistency | operative | consistency | Uniform Process Discipline | 0 | NO_ITEMS | Procedure steps follow a consistent discipline |
| C:evaluative:necessity | evaluative | necessity | Foundational Worth Benchmark | 0 | NO_ITEMS | Worth benchmark established in Guidance P-1 |
| C:evaluative:sufficiency | evaluative | sufficiency | Defensible Worth Appraisal | 0 | NO_ITEMS | Value case is defensible |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Merit Landscape | 0 | NO_ITEMS | Merit landscape is adequately covered |
| C:evaluative:consistency | evaluative | consistency | Principled Worth Consistency | 0 | NO_ITEMS | Value statements are consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Confirm applicability of CSA B64 series for backflow prevention; if confirmed, change Status from "ASSUMPTION" to "Applicable" in Standards table | The obligatory regulatory baseline includes backflow prevention standards, but CSA B64 is listed with "ASSUMPTION -- confirm with plumbing engineer" status, weakening the regulatory foundation | Specification.md | Standards table — CSA B64 series | -- | Plumbing engineer | TBD |
| C-002 | C:normative:consistency | Normalization | Multi | Guidance | Harmonize plumbing code terminology: Specification says "Alberta Plumbing Code (NPC as adopted in AB)"; Guidance says "applicable plumbing code"; Datasheet says "Alberta plumbing code". Use a single canonical term throughout | Inconsistent terminology for the governing plumbing code across documents risks confusion about which specific code is authoritative | Specification.md; Guidance.md; Datasheet.md | Specification Standards table; Guidance C-4; Datasheet Conditions — Regulatory Environment | -- | PM to establish canonical term | TBD |
| C-003 | C:operative:necessity | MissingSlot | Procedure | Procedure | Add prerequisite or coordination step: confirm whether cistern level monitoring/overflow protection (if any under DEL-014-01) must be operational before bulk fill commissioning to prevent overfill during integration testing | Critical operational prerequisite: the Procedure does not address cistern overflow prevention during the fill test (Step 5.5); if the cistern has no overflow or level alarm, running the bulk fill pump could overfill the tank | Procedure.md | Prerequisites; Step 5.5 — Integration Test with DEL-014-01 | -- | Plumbing Contractor / DEL-014-01 scope to confirm | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandated Compliance Foundation | 0 | NO_ITEMS | Foundation is present via REQ-014-03-05 and REQ-014-03-09 |
| F:normative:sufficiency | normative | sufficiency | Warranted Regulatory Sufficiency | 1 | HAS_ITEMS | Pressure test parameters not specified |
| F:normative:completeness | normative | completeness | Total Regulatory Completeness | 0 | NO_ITEMS | Regulatory requirements appear complete at current design stage |
| F:normative:consistency | normative | consistency | Integrated Compliance Integrity | 0 | NO_ITEMS | Compliance requirements are internally consistent |
| F:operative:necessity | operative | necessity | Essential Execution Readiness | 1 | HAS_ITEMS | Electrical coordination verification gap |
| F:operative:sufficiency | operative | sufficiency | Proven Procedural Competence | 0 | NO_ITEMS | Procedures demonstrate adequate competence expectations |
| F:operative:completeness | operative | completeness | Comprehensive Execution Mastery | 0 | NO_ITEMS | Execution steps are comprehensive |
| F:operative:consistency | operative | consistency | Consistent Procedural Rigor | 0 | NO_ITEMS | Procedural rigor is consistent across phases |
| F:evaluative:necessity | evaluative | necessity | Indispensable Value Foundation | 1 | HAS_ITEMS | No explicit cost/schedule risk for design TBD items |
| F:evaluative:sufficiency | evaluative | sufficiency | Justified Valuation Threshold | 0 | NO_ITEMS | Value threshold is adequately justified |
| F:evaluative:completeness | evaluative | completeness | Total Valuation Panorama | 0 | NO_ITEMS | Valuation scope is adequate |
| F:evaluative:consistency | evaluative | consistency | Harmonized Valuation Integrity | 0 | NO_ITEMS | Consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add specific pressure test parameters (test pressure in kPa/psi, hold duration, pass/fail criteria) to Verification table for pressure testing, or reference the specific Alberta Plumbing Code clause that defines these parameters | Procedure Step 4.2 says "Pressure test the fill line per Alberta Plumbing Code requirements" and Specification Verification says "Zero leakage at required test pressure for required duration" but neither document states the actual test pressure or duration values; warranted regulatory sufficiency requires these to be specified or cited | Specification.md; Procedure.md | Specification Verification table — pressure test row; Procedure Step 4.2 | -- | Plumbing engineer / Alberta Plumbing Code reference | TBD |
| F-002 | F:operative:necessity | VerificationGap | Specification | Specification | Add verification method for REQ-014-03-08 (Electrical Coordination): specify what constitutes adequate proof of pre-coordination (e.g., signed coordination form, meeting minutes, motor nameplate comparison) | Verification table states "Coordination meeting record; motor nameplate vs. circuit specification" but does not define a passing condition or acceptance format; essential execution readiness requires a clear verification standard | Specification.md | Verification table — REQ-014-03-08 row | -- | PM / Plumbing Contractor | TBD |
| F-003 | F:evaluative:necessity | RationaleGap | Guidance | Guidance | Add a note in Guidance on schedule/cost risk implication of the multiple design-TBD items (pump flow rate, fill connection size, freeze protection method, backflow device type) that block procurement and could delay installation start | The indispensable value foundation includes timely delivery; Guidance does not flag the risk that multiple unresolved TBD items in Datasheet/Specification could delay procurement and installation beyond the December 2026 deadline | Guidance.md | Considerations section | -- | PM | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Definitive Regulatory Directive | 0 | NO_ITEMS | RFP and code references provide directive |
| D:normative:applying | normative | applying | Enforced Compliance Implementation | 1 | HAS_ITEMS | Prime Contractor OH&S obligations not flowed down |
| D:normative:judging | normative | judging | Definitive Conformance Closure | 0 | NO_ITEMS | Safety Codes Officer inspection provides conformance closure |
| D:normative:reviewing | normative | reviewing | Systematic Compliance Verification | 0 | NO_ITEMS | Verification table provides systematic coverage |
| D:operative:guiding | operative | guiding | Authoritative Execution Stewardship | 0 | NO_ITEMS | Procedure provides authoritative execution direction |
| D:operative:applying | operative | applying | Settled Skilled Accomplishment | 0 | NO_ITEMS | Procedure steps are clear for skilled execution |
| D:operative:judging | operative | judging | Conclusive Performance Verdict | 1 | HAS_ITEMS | Commissioning agent role unclear |
| D:operative:reviewing | operative | reviewing | Systematic Procedural Inspection | 0 | NO_ITEMS | Inspection steps are systematic |
| D:evaluative:guiding | evaluative | guiding | Settled Worth Direction | 0 | NO_ITEMS | Worth direction established in Guidance |
| D:evaluative:applying | evaluative | applying | Justified Worth Realization | 0 | NO_ITEMS | Adequately addressed |
| D:evaluative:judging | evaluative | judging | Definitive Value Closure | 1 | HAS_ITEMS | No explicit OBJ-004 sign-off criterion |
| D:evaluative:reviewing | evaluative | reviewing | Harmonized Worth Verification | 0 | NO_ITEMS | Warranty and closeout provisions address this |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | MissingSlot | Specification | Specification | Add requirement or note regarding Prime Contractor OH&S obligations (RFP section 2.15, Alberta OH&S) that apply during bulk fill system installation -- currently listed in Standards table but not referenced in any REQ | Enforced compliance implementation requires flowing down all applicable mandatory obligations; Alberta OH&S is in the Standards table but no requirement addresses OH&S obligations for this installation work | Specification.md | Standards table — Alberta OH&S row; Requirements section (absent) | -- | PM / Safety Coordinator | TBD |
| D-002 | D:operative:judging | RationaleGap | Guidance | Guidance | Clarify who performs the commissioning assessment for DEL-014-03: is it the Plumbing Contractor self-commissioning, an independent commissioning agent (DEL-020-01), or both? Specify the authority for issuing the conclusive performance verdict | Procedure references both "Plumbing Contractor / Commissioning Agent" (Phase 5) and DEL-020-01 (Building Systems Commissioning) but does not clarify which party has authority to issue the final performance acceptance for the bulk fill system | Procedure.md; Guidance.md | Procedure Step 5.6; Guidance C-5 | -- | PM to clarify commissioning authority | TBD |
| D-003 | D:evaluative:judging | VerificationGap | Specification | Specification | Add explicit verification criterion linking bulk fill system completion to OBJ-004 sign-off ("Install and commission all mechanical, plumbing, and water storage systems to operational readiness") | OBJ-004 is referenced in _CONTEXT.md and Datasheet but the Specification Verification table does not include a verification method that explicitly traces back to OBJ-004 closure; definitive value closure requires this traceability | Specification.md; Datasheet.md | Specification Verification table; Datasheet References — OBJ-004 | -- | PM | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Governance Orientation | 0 | NO_ITEMS | Governance orientation is established |
| X:guiding:sufficiency | guiding | sufficiency | Justified Directional Governance | 0 | NO_ITEMS | Directional governance is justified |
| X:guiding:completeness | guiding | completeness | Exhaustive Directional Mastery | 0 | NO_ITEMS | Guidance and Specification together provide comprehensive direction |
| X:guiding:consistency | guiding | consistency | Harmonized Governance Alignment | 0 | NO_ITEMS | Governance alignment is harmonized across documents |
| X:applying:necessity | applying | necessity | Indispensable Enactment Mandate | 1 | HAS_ITEMS | County notification requirement not in Procedure prerequisites |
| X:applying:sufficiency | applying | sufficiency | Substantiated Skill Deployment | 0 | NO_ITEMS | Skill deployment requirements are substantiated |
| X:applying:completeness | applying | completeness | Exhaustive Implementation Record | 0 | NO_ITEMS | Records section in Procedure is exhaustive |
| X:applying:consistency | applying | consistency | Standardized Practice Coherence | 1 | HAS_ITEMS | Inspection notification terminology inconsistency |
| X:judging:necessity | judging | necessity | Binding Outcome Determination | 0 | NO_ITEMS | Outcome determination is addressed in Verification |
| X:judging:sufficiency | judging | sufficiency | Substantiated Judgment Disposition | 0 | NO_ITEMS | Judgment dispositions are substantiated |
| X:judging:completeness | judging | completeness | Exhaustive Judgment Closure | 1 | HAS_ITEMS | As-built acceptance criteria unclear |
| X:judging:consistency | judging | consistency | Concordant Outcome Standard | 0 | NO_ITEMS | Outcome standards are concordant |
| X:reviewing:necessity | reviewing | necessity | Mandatory Verification Baseline | 0 | NO_ITEMS | Verification baseline is established |
| X:reviewing:sufficiency | reviewing | sufficiency | Substantiated Assurance Scope | 0 | NO_ITEMS | Assurance scope is adequate |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Assurance Record | 0 | NO_ITEMS | Assurance records are comprehensive |
| X:reviewing:consistency | reviewing | consistency | Harmonized Assurance Alignment | 0 | NO_ITEMS | Assurance alignment is adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | MissingSlot | Procedure | Procedure | Add explicit prerequisite or step: County project representative must be notified in advance of inspections (per RFP section 3.3.2); currently mentioned in Step 3.1 body text but not in Prerequisites table | The indispensable enactment mandate includes owner notification; RFP section 3.3.2 requires County representative presence at inspections, which is noted in Step 3.1 text but not formalized as a prerequisite or checklist item | Procedure.md | Prerequisites table; Step 3.1 | -- | PM | TBD |
| X-002 | X:applying:consistency | Normalization | Procedure | Procedure | Standardize inspection notification language: Step 3.1 says "County project representative must be notified and present at inspection per RFP section 3.3.2" but Step 4.3 says only "County project representative to be present" without citing RFP; use consistent phrasing | Standardized practice coherence requires uniform language for the same obligation across procedure steps | Procedure.md | Step 3.1; Step 4.3 | -- | -- | TBD |
| X-003 | X:judging:completeness | VerificationGap | Specification | Specification | Add acceptance criteria for as-built drawings (REQ-014-03-09 verification): define what constitutes an acceptable as-built mark-up (e.g., red-line of all deviations from IFC, signed by foreman, date-stamped) | Verification table says "As-built mark-up review; red-line as-built drawings" with no explicit pass/fail criteria; exhaustive judgment closure requires clear acceptance standard for this artifact | Specification.md | Verification table — REQ-014-03-09 row | -- | PM / Engineer of Record | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Verified Directional Anchor | 0 | NO_ITEMS | Directional anchor is verified through RFP and context references |
| E:guiding:information | guiding | information | Coherent Leadership Intelligence | 0 | NO_ITEMS | Leadership intelligence is coherent across Guidance |
| E:guiding:knowledge | guiding | knowledge | Integrated Governance Proficiency | 0 | NO_ITEMS | Governance proficiency is integrated |
| E:guiding:wisdom | guiding | wisdom | Principled Leadership Foresight | 1 | HAS_ITEMS | No winterization operations foresight |
| E:applying:data | applying | data | Verified Implementation Evidence | 0 | NO_ITEMS | Implementation evidence chain is adequate |
| E:applying:information | applying | information | Contextualized Execution Intelligence | 0 | NO_ITEMS | Execution intelligence is contextualized |
| E:applying:knowledge | applying | knowledge | Integrated Execution Mastery | 0 | NO_ITEMS | Execution mastery is integrated across Procedure phases |
| E:applying:wisdom | applying | wisdom | Principled Execution Judgment | 1 | HAS_ITEMS | No hold points defined |
| E:judging:data | judging | data | Verified Adjudication Record | 0 | NO_ITEMS | Adjudication records are specified |
| E:judging:information | judging | information | Contextualized Ruling Intelligence | 0 | NO_ITEMS | Ruling intelligence is contextualized |
| E:judging:knowledge | judging | knowledge | Integrated Adjudicative Mastery | 0 | NO_ITEMS | Adjudicative framework is integrated |
| E:judging:wisdom | judging | wisdom | Principled Adjudicative Wisdom | 0 | NO_ITEMS | Adjudicative wisdom is present in Guidance conflict table |
| E:reviewing:data | reviewing | data | Verified Audit Evidence | 1 | HAS_ITEMS | Conflict between Guidance and Specification on fill point scope |
| E:reviewing:information | reviewing | information | Coherent Assurance Intelligence | 0 | NO_ITEMS | Assurance intelligence is coherent |
| E:reviewing:knowledge | reviewing | knowledge | Integrated Verification Mastery | 0 | NO_ITEMS | Verification mastery is integrated |
| E:reviewing:wisdom | reviewing | wisdom | Principled Assurance Foresight | 0 | NO_ITEMS | Assurance foresight is adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:wisdom | TBD_Question | Guidance | Guidance | TBD: Address seasonal operational foresight -- should Guidance include a note on post-commissioning winterization protocol handoff to the Owner (who will operate the fill system seasonally)? O&M manual is required but Guidance does not flag the operational criticality of winterization as a lifecycle concern | Principled leadership foresight should anticipate that the bulk fill system will be used seasonally in Alberta and that freeze protection has operational implications beyond installation; the O&M manual requirement exists in Specification but Guidance does not frame this as a key lifecycle concern | Guidance.md; Specification.md | Guidance Considerations; Specification Documentation — O&M Manual | -- | PM / Owner to confirm operational expectations | TBD |
| E-002 | E:applying:wisdom | Normalization | Procedure | Procedure | Define explicit hold points (mandatory inspection/approval gates) in the Procedure: identify which steps require sign-off before proceeding (e.g., after Step 3.1 rough-in inspection, after Step 4.2 pressure test) vs. which can proceed without gate approval | Principled execution judgment requires clear hold-point discipline; the Procedure implies hold points (inspection before proceeding, per Step 3.2) but does not formally label any step as a mandatory hold point vs. a continuous-flow step | Procedure.md | Steps 3.1, 3.2, 4.2, 4.3 | -- | PM / Plumbing Contractor | TBD |
| E-003 | E:reviewing:data | Conflict | Multi | Specification | Resolve: Specification REQ-014-03-03 says fill point location is "on the north face of the building" citing Appendix B; Guidance T-1 discusses pump location as "indoor vs. outdoor" with no settled location. Confirm whether "north face" in REQ-014-03-03 refers to fill connection point only or also pump location | Verified audit evidence shows a potential conflict: the fill point location is cited as north face (Specification), but the pump location relative to the fill point is unresolved (Guidance T-1). These are different things but could be confused | Specification.md#REQ-014-03-03; Guidance.md#T-1 | REQ-014-03-03; T-1 — Pump Location | Specification.md#REQ-014-03-03 ("north face of the building"); Guidance.md#T-1 ("Indoor vs. Outdoor" -- unresolved) | Plumbing engineer (IFC design) | TBD |
| E-004 | E:reviewing:data | Conflict | Datasheet | Datasheet | Resolve: Datasheet Primary Function says "fill the cistern or take on water" implying bidirectional use (fill AND extraction); Specification REQ-014-03-01 says "enabling bulk water delivery or extraction at the exterior." Guidance P-1 says "sole mechanism for replenishing the cistern." Confirm whether extraction (taking water FROM cistern to truck) is in scope for DEL-014-03 or only filling | Datasheet and Specification both use "or" language suggesting bidirectional operation, but Guidance P-1 frames the system exclusively as a cistern fill mechanism; this creates ambiguity about whether the system must support water extraction from the cistern to vehicles | Datasheet.md#Attributes; Specification.md#REQ-014-03-01; Guidance.md#P-1 | Datasheet Attributes — Primary Function; Specification REQ-014-03-01; Guidance P-1 | Datasheet.md#Attributes ("fill the cistern or take on water"); Specification.md#REQ-014-03-01 ("delivery or extraction"); Guidance.md#P-1 ("sole mechanism for replenishing the cistern") | Owner / PM to confirm operational intent | TBD |
