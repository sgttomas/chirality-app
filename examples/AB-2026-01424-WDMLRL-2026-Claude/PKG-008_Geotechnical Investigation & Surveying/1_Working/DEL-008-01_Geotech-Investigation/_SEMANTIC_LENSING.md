# Semantic Lensing Register: DEL-008-01 Geotechnical Investigation & Report

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-008_Geotechnical Investigation & Surveying/1_Working/DEL-008-01_Geotech-Investigation/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-008-01_Geotech-Investigation/_CONTEXT.md (present; read)
- _STATUS.md -- DEL-008-01_Geotech-Investigation/_STATUS.md (present; read; state=SEMANTIC_READY)
- _SEMANTIC.md -- DEL-008-01_Geotech-Investigation/_SEMANTIC.md (present; read; 7 matrices parsed)
- Datasheet.md -- DEL-008-01_Geotech-Investigation/Datasheet.md (present; read)
- Specification.md -- DEL-008-01_Geotech-Investigation/Specification.md (present; read)
- Guidance.md -- DEL-008-01_Geotech-Investigation/Guidance.md (present; read)
- Procedure.md -- DEL-008-01_Geotech-Investigation/Procedure.md (present; read)
- _REFERENCES.md -- DEL-008-01_Geotech-Investigation/_REFERENCES.md (present; read; pointers listed, scope not expanded)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 21
- By document:
  - Datasheet: 2
  - Specification: 8
  - Guidance: 2
  - Procedure: 5
  - Multi: 4
- By matrix:
  - A: 4  B: 2  C: 3  F: 3  D: 3  X: 4  E: 2
- By type:
  - Conflict: 0
  - VerificationGap: 5
  - MissingSlot: 5
  - WeakStatement: 3
  - RationaleGap: 3
  - Normalization: 2
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Standards lack clause-level specificity |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Professional seal requirement basis TBD |
| A:normative:judging | normative | judging | compliance determination | 0 | NO_ITEMS | Verification table in Specification covers compliance checks adequately |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | No audit/review cycle defined for report quality |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Step 1-7 provides adequate procedural direction |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Procedure Steps 3-5 cover field execution adequately |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | No quantified performance criteria for investigation program adequacy |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Procedure verification table covers process checks |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance addresses commercial value orientation via RFP 4.8.2 |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Documents address merit through professional responsibility |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Foundation pricing mechanism serves as worth determination |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Internal review noted in Procedure Step 6.2 |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify which specific clause-level requirements from listed standards (ASTM D, CFEM, NBC/ABC, Alberta EGPA) apply to this investigation; currently all marked "ASSUMPTION: likely applicable; location TBD" | Five standards are listed as likely applicable but none have confirmed clause-level applicability; this leaves the prescriptive direction for the investigation materially ambiguous | Specification.md | Standards | -- | PROPOSAL: Geotechnical Engineer to confirm applicable standard clauses before investigation program finalization | TBD |
| A-002 | A:normative:applying | TBD_Question | Specification | Specification | Record TBD: Confirm whether Alberta EGPA requires professional engineer seal on geotechnical reports specifically, and cite the regulatory basis | REQ-009 requires preparation by Geotechnical Engineer but the seal/stamp requirement is marked ASSUMPTION with no regulatory basis confirmed; this is a mandatory practice question that must be resolved before report issuance | Specification.md | REQ-009 — Prepared by Geotechnical Engineer; Verification — REQ-009 row | -- | PROPOSAL: Consult Alberta APEGA or Engineering and Geoscience Professions Act for seal requirements | TBD |
| A-003 | A:normative:reviewing | MissingSlot | Specification | Specification | Add acceptance criteria for independent technical review of the geotechnical report before Owner delivery (e.g., peer review or senior review requirement) | Procedure Step 6.2 mentions internal senior review as ASSUMPTION but Specification has no corresponding requirement or verification entry for report quality review prior to issuance | Specification.md | Verification | -- | PROPOSAL: Specification should include review requirement if standard practice warrants it | TBD |
| A-004 | A:operative:judging | MissingSlot | Specification | Specification | Add quantified acceptance criteria for investigation program adequacy (e.g., minimum borehole count relative to footprint area, minimum investigation depth relative to foundation influence zone) | No measurable performance thresholds exist for assessing whether the investigation program is adequate; Procedure Step 2.3 lists TBD items but Specification provides no criteria to judge sufficiency of the program | Specification.md | Requirements; Verification | -- | PROPOSAL: Geotechnical Engineer to propose minimum program parameters for Owner acceptance | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Structural load data missing as input |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Report content elements in Datasheet are adequate for evidence planning |
| B:data:completeness | data | completeness | comprehensive record | 0 | NO_ITEMS | Datasheet Construction table covers anticipated record elements |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Procedure addresses measurement reliability through standard methods |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Groundwater monitoring duration unspecified |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Guidance Considerations section provides adequate context |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Report sections enumerated in Procedure Step 6.1 are comprehensive |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Documents are internally consistent on scope and purpose |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Professional responsibility and geotechnical expertise addressed |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Responsible party identified as Geotechnical Engineer throughout |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Scope covers full investigation-to-report lifecycle |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding of deliverable purpose is consistent across all docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Guidance trade-offs section exercises appropriate discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Professional judgment deferred to Geotechnical Engineer appropriately |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Cross-package dependencies and commercial implications addressed |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning from RFP sources is principled and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Multi | Procedure | Record TBD: Obtain anticipated structural loads and foundation configuration preferences from Structural Engineer (PKG-002) as essential input to investigation program design | Guidance and Procedure both identify this coordination as ASSUMPTION/standard practice, but no mechanism ensures these essential facts are available before investigation program design; without load data, bearing capacity analysis scope cannot be properly defined | Guidance.md; Procedure.md | Guidance -- Considerations -- Foundation type and loading; Procedure -- Step 2.2 | -- | PROPOSAL: Structural Engineer (PKG-002) provides preliminary load data before Step 2 of Procedure | TBD |
| B-002 | B:information:necessity | WeakStatement | Procedure | Procedure | Clarify whether groundwater monitoring is a single-reading observation during drilling or requires extended monitoring (standpipe/piezometer installation and repeat readings over time) | Procedure Step 3.4 states "Install groundwater monitoring wells or standpipes if required by investigation program (TBD)" but does not define the signal that triggers this decision or the monitoring duration; this ambiguity could affect the adequacy of groundwater characterization | Procedure.md | Step 3 -- Mobilize and Conduct Field Investigation -- Step 3.4 | -- | PROPOSAL: Geotechnical Engineer determines monitoring approach; document decision rationale in investigation program | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Compulsory Regulatory Baseline | 1 | HAS_ITEMS | Regulatory baseline for geotech practice not confirmed |
| C:normative:sufficiency | normative | sufficiency | Mandated Compliance Threshold | 0 | NO_ITEMS | REQ-001 through REQ-010 establish compliance thresholds |
| C:normative:completeness | normative | completeness | Exhaustive Regulatory Scope | 1 | HAS_ITEMS | Environmental assessment applicability unresolved |
| C:normative:consistency | normative | consistency | Binding Regulatory Alignment | 0 | NO_ITEMS | Documents are aligned on regulatory references |
| C:operative:necessity | operative | necessity | Operational Prerequisite Baseline | 0 | NO_ITEMS | Prerequisites table in Procedure is thorough |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Execution Readiness | 0 | NO_ITEMS | Readiness gates defined in Procedure verification table |
| C:operative:completeness | operative | completeness | Full Process Traceability | 1 | HAS_ITEMS | Records table lacks traceability for investigation program changes |
| C:operative:consistency | operative | consistency | Reliable Process Calibration | 0 | NO_ITEMS | Process steps are sequentially consistent |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Worth Benchmark | 0 | NO_ITEMS | Commercial value benchmark established via RFP 4.8.2 |
| C:evaluative:sufficiency | evaluative | sufficiency | Demonstrated Merit Sufficiency | 0 | NO_ITEMS | Merit demonstrated through downstream enablement |
| C:evaluative:completeness | evaluative | completeness | Holistic Valuation Scope | 0 | NO_ITEMS | Value scope includes technical and commercial dimensions |
| C:evaluative:consistency | evaluative | consistency | Principled Valuation Integrity | 0 | NO_ITEMS | Valuation reasoning is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | RationaleGap | Guidance | Guidance | Add rationale for why specific Alberta regulatory requirements (EGPA, Safety Codes Act) are relevant or not relevant to the geotechnical investigation itself (as distinct from the building design) | The Specification Standards table notes that Safety Codes Act applicability to geotech report "specifically is ASSUMPTION" -- Guidance should explain the reasoning for including or excluding these regulatory instruments from the compulsory baseline | Specification.md; Guidance.md | Specification -- Standards; Guidance -- Principles -- Professional responsibility | -- | PROPOSAL: Geotechnical Engineer or project legal counsel to confirm regulatory applicability | TBD |
| C-002 | C:normative:completeness | WeakStatement | Specification | Specification | Resolve whether environmental assessment is in or out of scope for this investigation; currently stated as "TBD if applicable per provincial regulation" | Specification Out of Scope states environmental assessment is "not mentioned in RFP scope for this deliverable; TBD if applicable per provincial regulation" -- this leaves the exhaustive regulatory scope incomplete because a provincial environmental requirement could apply to subsurface investigation on a landfill site | Specification.md | Scope -- Out of Scope | -- | PROPOSAL: Confirm with regulatory authority whether environmental assessment is triggered by investigation on active landfill | TBD |
| C-003 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add a record type for investigation program revisions/changes made during field work (e.g., additional boreholes, changed depths, modified test program) | Procedure Records table lists the approved investigation program but has no provision for documenting changes to the program during execution; full process traceability requires capturing deviations from the approved program | Procedure.md | Records | -- | PROPOSAL: Add "Investigation program change log" to Records table | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Statutory Factual Foundation | 0 | NO_ITEMS | REQ-001 through REQ-005 provide statutory factual foundation via RFP citations |
| F:normative:sufficiency | normative | sufficiency | Mandated Evidence Competence | 1 | HAS_ITEMS | Verification for REQ-009 is assumption-based |
| F:normative:completeness | normative | completeness | Total Regulatory Command | 0 | NO_ITEMS | Requirements span investigation through delivery |
| F:normative:consistency | normative | consistency | Regulatory Predictability Doctrine | 0 | NO_ITEMS | Requirements are internally consistent |
| F:operative:necessity | operative | necessity | Critical Activation Criterion | 1 | HAS_ITEMS | No explicit go/no-go gate for field mobilization |
| F:operative:sufficiency | operative | sufficiency | Accountable Operational Preparedness | 0 | NO_ITEMS | Prerequisites table addresses preparedness |
| F:operative:completeness | operative | completeness | End-to-End Provenance Register | 0 | NO_ITEMS | Records table provides end-to-end provenance |
| F:operative:consistency | operative | consistency | Repeatable Audit Dependability | 0 | NO_ITEMS | Process is sequentially consistent |
| F:evaluative:necessity | evaluative | necessity | Foundational Worth Evidence | 1 | HAS_ITEMS | Cost estimate / budget for investigation not addressed |
| F:evaluative:sufficiency | evaluative | sufficiency | Proven Appraisal Competence | 0 | NO_ITEMS | Commercial competence addressed via pricing mechanism |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Quality Record | 0 | NO_ITEMS | Quality documentation covered in Records table |
| F:evaluative:consistency | evaluative | consistency | Calibrated Appraisal Consistency | 0 | NO_ITEMS | Appraisal framework consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | VerificationGap | Specification | Specification | Strengthen verification approach for REQ-009 by identifying the specific regulatory basis for professional seal/stamp requirement rather than relying on ASSUMPTION | Verification row for REQ-009 states "ASSUMPTION on seal requirement; TBD on specific regulatory basis" -- without confirmed regulatory basis, mandated evidence competence for this requirement is incomplete | Specification.md | Verification -- REQ-009 row | -- | PROPOSAL: Cite specific APEGA or EGPA regulation for seal requirement | TBD |
| F-002 | F:operative:necessity | VerificationGap | Procedure | Procedure | Add an explicit go/no-go readiness gate checklist before field mobilization (Step 3) consolidating all prerequisites into a single activation criterion | Procedure has prerequisites and verification checks but no single consolidated mobilization-readiness gate; the critical activation criterion for field work is implied but not formalized as a hold point | Procedure.md | Prerequisites; Verification -- "Site access confirmed" and "Investigation program accepted" rows | -- | PROPOSAL: Add formal mobilization hold point between Step 2 and Step 3 | TBD |
| F-003 | F:evaluative:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: What is the budget or cost allowance for the geotechnical investigation within the overall project cost estimate? | No document addresses the cost of performing the investigation itself; given the variable-price foundation mechanism (RFP 4.8.2), the investigation cost relative to the foundation pricing adjustment is foundational worth evidence that should be documented | Datasheet.md | Attributes | -- | PROPOSAL: Project Manager or Estimating team to provide investigation budget figure | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Established Binding Authority | 0 | NO_ITEMS | RFP sections cited provide binding authority |
| D:normative:applying | normative | applying | Enforced Compliance Action | 0 | NO_ITEMS | Requirements enforce compliance actions |
| D:normative:judging | normative | judging | Definitive Conformance Ruling | 0 | NO_ITEMS | Verification table enables conformance determination |
| D:normative:reviewing | normative | reviewing | Established Oversight Doctrine | 1 | HAS_ITEMS | No Owner review/approval cycle defined for draft report |
| D:operative:guiding | operative | guiding | Confirmed Operational Steering | 0 | NO_ITEMS | Procedure provides clear operational direction |
| D:operative:applying | operative | applying | Confirmed Delivery Capacity | 0 | NO_ITEMS | Delivery capacity addressed through prerequisites and steps |
| D:operative:judging | operative | judging | Traceable Capability Ruling | 1 | HAS_ITEMS | No criteria for ruling on lab testing adequacy |
| D:operative:reviewing | operative | reviewing | Reliable Workflow Verification | 0 | NO_ITEMS | Procedure verification table covers workflow checks |
| D:evaluative:guiding | evaluative | guiding | Grounded Merit Direction | 0 | NO_ITEMS | Guidance grounds merit in critical-path and commercial value |
| D:evaluative:applying | evaluative | applying | Confirmed Value Realization | 1 | HAS_ITEMS | No metric for confirming report enabled design progression |
| D:evaluative:judging | evaluative | judging | Conclusive Valuation Finding | 0 | NO_ITEMS | Foundation pricing negotiation serves as valuation mechanism |
| D:evaluative:reviewing | evaluative | reviewing | Stable Merit Review | 0 | NO_ITEMS | Quality review addressed in Procedure Step 6.2 |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:reviewing | MissingSlot | Multi | Procedure | Add a step for Owner review/comment period on draft report before final issuance, or explicitly document that no draft review cycle is planned | No document defines whether the Owner reviews a draft before final issuance; Procedure goes directly from internal review (Step 6.2) to delivery (Step 7); an established oversight doctrine would include the Owner's review opportunity | Procedure.md; Specification.md | Procedure -- Step 6; Specification -- Verification -- REQ-001 row | -- | PROPOSAL: Confirm with Owner whether draft review is required or report is delivered as final only | TBD |
| D-002 | D:operative:judging | VerificationGap | Procedure | Specification | Add acceptance criteria for laboratory testing completeness and quality (e.g., minimum number of tests per soil type, QA/QC requirements for lab results) | Procedure Step 4.3 says "review laboratory results for completeness and quality; request re-testing if results are anomalous" but provides no criteria for what constitutes complete or acceptable lab quality; traceable capability ruling requires defined acceptance thresholds | Procedure.md; Specification.md | Procedure -- Step 4; Specification -- Verification | -- | PROPOSAL: Geotechnical Engineer defines lab QA/QC criteria in investigation program | TBD |
| D-003 | D:evaluative:applying | VerificationGap | Specification | Specification | Add a verification entry confirming that the geotechnical report was actually used as input to foundation design (PKG-002), not just delivered | REQ-002 requires report "used during design process" and verification says "Confirmed by presence of geotech report in foundation design package as cited reference" but this is a downstream check with no timing or tracking mechanism in this deliverable's verification plan | Specification.md | Verification -- REQ-002 row | -- | PROPOSAL: Add downstream confirmation milestone to Procedure or project schedule | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Priority Indicator | 0 | NO_ITEMS | Critical path priority clearly established |
| X:guiding:sufficiency | guiding | sufficiency | Validated Guidance Evidence | 0 | NO_ITEMS | Guidance is well-evidenced from RFP sources |
| X:guiding:completeness | guiding | completeness | Complete Directional Register | 1 | HAS_ITEMS | Service pit recommendations not in Specification requirements |
| X:guiding:consistency | guiding | consistency | Calibrated Steering Alignment | 0 | NO_ITEMS | Steering is consistent across documents |
| X:applying:necessity | applying | necessity | Actionable Execution Trigger | 0 | NO_ITEMS | Contract award and site access serve as execution triggers |
| X:applying:sufficiency | applying | sufficiency | Proven Execution Competence | 0 | NO_ITEMS | Geotechnical Engineer role provides execution competence |
| X:applying:completeness | applying | completeness | Complete Execution Record | 1 | HAS_ITEMS | Photographic documentation not specified |
| X:applying:consistency | applying | consistency | Standardized Execution Metric | 0 | NO_ITEMS | Execution methods deferred to professional judgment consistently |
| X:judging:necessity | judging | necessity | Critical Verdict Basis | 1 | HAS_ITEMS | Deleterious materials determination criteria undefined |
| X:judging:sufficiency | judging | sufficiency | Qualified Verdict Proof | 0 | NO_ITEMS | Verification table provides sufficient proof points |
| X:judging:completeness | judging | completeness | Exhaustive Verdict Record | 0 | NO_ITEMS | Verification covers all requirements |
| X:judging:consistency | judging | consistency | Calibrated Verdict Standard | 0 | NO_ITEMS | Verdict standards are consistent |
| X:reviewing:necessity | reviewing | necessity | Mandatory Audit Indicator | 0 | NO_ITEMS | Verification checks serve as audit indicators |
| X:reviewing:sufficiency | reviewing | sufficiency | Sufficient Audit Readiness | 0 | NO_ITEMS | Records table supports audit readiness |
| X:reviewing:completeness | reviewing | completeness | Complete Audit Documentation | 1 | HAS_ITEMS | Transmission format not specified |
| X:reviewing:consistency | reviewing | consistency | Standardized Audit Clarity | 0 | NO_ITEMS | Audit approach is clear and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | Normalization | Multi | Specification | Align service pit coverage: Guidance and Procedure address service pit recommendations (excavation, lateral earth pressure, groundwater) but Specification requirements do not include a requirement for service pit geotechnical characterization | Guidance (Considerations -- Service pit) and Procedure (Steps 5.8, 6.1) include service pit analysis but no Specification requirement mandates it; the directional register is incomplete because a topic addressed operationally lacks normative backing | Guidance.md; Procedure.md; Specification.md | Guidance -- Considerations -- Service pit; Procedure -- Steps 5.8, 6.1; Specification -- Requirements (service pit absent) | -- | PROPOSAL: Add REQ for service pit geotechnical characterization in Specification if warranted | TBD |
| X-002 | X:applying:completeness | MissingSlot | Procedure | Procedure | Add photographic documentation requirement for field investigation (borehole locations, soil samples, site conditions, equipment used) | Procedure Step 3 covers field execution but does not mention photographic records; field photographs are standard practice for geotechnical investigations and support complete execution records | Procedure.md | Step 3 -- Mobilize and Conduct Field Investigation | -- | PROPOSAL: Add photo documentation to Step 3 and Records table | TBD |
| X-003 | X:judging:necessity | RationaleGap | Guidance | Guidance | Add guidance on what constitutes "deleterious subgrade material" in the context of RFP 4.8.2 and how the determination of normal vs. abnormal ground conditions should be made | REQ-004 and Procedure Step 5.6 require assessment relative to "normal ground conditions without any deleterious subgrade material" baseline but no document defines what constitutes deleterious material or the threshold for departing from the normal-conditions baseline; this is the critical verdict basis for the commercial pricing mechanism | Specification.md; Procedure.md; Guidance.md | Specification -- REQ-004; Procedure -- Step 5.6; Guidance -- Principles -- Normal ground conditions baseline | -- | PROPOSAL: Geotechnical Engineer defines criteria in consultation with Owner before report finalization | TBD |
| X-004 | X:reviewing:completeness | RationaleGap | Datasheet | Guidance | Add rationale for report transmission format (hard copy, electronic, number of copies) and any Owner requirements for report format | Datasheet Attributes lists "Report recipient: Owner (Camrose County)" and Procedure Step 7.1 says "Transmit the complete geotechnical report to the Owner" but neither specifies format, medium, or number of copies; complete audit documentation requires the transmission format to be defined | Datasheet.md; Procedure.md | Datasheet -- Attributes -- Report recipient; Procedure -- Step 7 | -- | PROPOSAL: Confirm Owner requirements for report format and number of copies | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Validated Steering Datum | 0 | NO_ITEMS | Steering data from RFP is validated and cited |
| E:guiding:information | guiding | information | Coherent Steering Narrative | 0 | NO_ITEMS | Guidance provides coherent narrative |
| E:guiding:knowledge | guiding | knowledge | Strategic Navigational Command | 0 | NO_ITEMS | Critical path and downstream dependency strategy is clear |
| E:guiding:wisdom | guiding | wisdom | Principled Strategic Foresight | 0 | NO_ITEMS | Trade-offs section exercises strategic foresight |
| E:applying:data | applying | data | Quantified Performance Record | 1 | HAS_ITEMS | No quantified schedule target for investigation |
| E:applying:information | applying | information | Situated Delivery Narrative | 0 | NO_ITEMS | Delivery narrative is well-situated in project context |
| E:applying:knowledge | applying | knowledge | Demonstrated Operational Craft | 0 | NO_ITEMS | Professional craft deferred to Geotechnical Engineer |
| E:applying:wisdom | applying | wisdom | Skilled Delivery Prudence | 0 | NO_ITEMS | Prudence demonstrated through ASSUMPTION flagging |
| E:judging:data | judging | data | Evidentiary Ruling Benchmark | 0 | NO_ITEMS | Verification benchmarks adequately defined for most requirements |
| E:judging:information | judging | information | Situated Adjudication Signal | 0 | NO_ITEMS | Adjudication signals are situated in verification table |
| E:judging:knowledge | judging | knowledge | Adjudicative Evidentiary Command | 0 | NO_ITEMS | Evidence chain from requirements to verification is traceable |
| E:judging:wisdom | judging | wisdom | Principled Adjudicative Prudence | 0 | NO_ITEMS | Prudent approach to ASSUMPTION vs confirmed requirements |
| E:reviewing:data | reviewing | data | Transparent Verification Datum | 1 | HAS_ITEMS | Verification timing not fully specified |
| E:reviewing:information | reviewing | information | Transparent Audit Narrative | 0 | NO_ITEMS | Audit narrative is transparent in verification table |
| E:reviewing:knowledge | reviewing | knowledge | Proficient Verification Command | 0 | NO_ITEMS | Verification approach shows proficiency |
| E:reviewing:wisdom | reviewing | wisdom | Principled Oversight Acuity | 0 | NO_ITEMS | Oversight approach is principled |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:applying:data | Normalization | Multi | Datasheet | Add a target date or schedule duration for the geotechnical investigation and report in the Datasheet Attributes; align with REQ-010 critical path timing requirement | REQ-010 states the investigation "must be delivered as early as practicable" but no quantified schedule target (date or duration) exists in any document; Datasheet lists project completion deadline (Dec 31, 2026) but no investigation-specific milestone date | Specification.md; Datasheet.md | Specification -- REQ-010; Datasheet -- Attributes -- Project completion deadline | -- | PROPOSAL: Project Manager to set target date for investigation completion in project schedule and record in Datasheet | TBD |
| E-002 | E:reviewing:data | VerificationGap | Specification | Specification | Specify verification timing for REQ-001 and REQ-003 more precisely (e.g., within N days of report delivery, or at foundation pricing negotiation meeting) | Specification Verification for REQ-001 says "Owner receipt and written acknowledgment" and REQ-003 says "Foundation pricing negotiation initiated using report" but neither specifies when these verifications should occur relative to report delivery; transparent verification data requires defined timing | Specification.md | Verification -- REQ-001 row; Verification -- REQ-003 row | -- | PROPOSAL: Define verification timing windows in Specification or Procedure | TBD |
