# Semantic Lensing Register: DEL-001-05 Interior Elevations

**Generated:** 2026-02-26
**Deliverable Folder:** PKG-001_Architectural Design/1_Working/DEL-001-05_Interior-Elevations/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-001-05_Interior-Elevations/_CONTEXT.md
- _STATUS.md — DEL-001-05_Interior-Elevations/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md — DEL-001-05_Interior-Elevations/_SEMANTIC.md
- Datasheet.md — DEL-001-05_Interior-Elevations/Datasheet.md
- Specification.md — DEL-001-05_Interior-Elevations/Specification.md
- Guidance.md — DEL-001-05_Interior-Elevations/Guidance.md
- Procedure.md — DEL-001-05_Interior-Elevations/Procedure.md
- _REFERENCES.md — DEL-001-05_Interior-Elevations/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 3
  - Specification: 9
  - Guidance: 2
  - Procedure: 11
  - Multi: 3
- By matrix:
  - A: 4  B: 5  C: 3  F: 4  D: 3  X: 5  E: 4
- By type:
  - Conflict: 2
  - VerificationGap: 6
  - MissingSlot: 8
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 2
- Matrix parse errors: 0

---

## Matrix A — Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Stamping requirement ambiguity (P.Eng. vs. Architect) |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Code edition not specified |
| A:normative:judging | normative | judging | compliance determination | 0 | NO_ITEMS | Compliance determination is well-addressed via REQ-002 and verification table |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | Inspection coordination lacks procedural detail |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Steps 1-7 provide adequate procedural direction |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Practical execution steps are well-sequenced in Procedure |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | IFC Readiness Checklist in Procedure covers performance assessment |
| A:operative:reviewing | operative | reviewing | process audit | 1 | HAS_ITEMS | No post-IFC review or as-built reconciliation procedure |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Principles section adequately sets value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs table in Guidance addresses merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Verification table covers worth determination sufficiently |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | IFC Readiness Checklist serves as quality appraisal mechanism |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | Conflict | Multi | Guidance | Clarify whether IFC stamp requirement is P.Eng. stamp only (as stated in REQ-003) or whether Architect of Record stamp is also required/acceptable given these are architectural drawings. Specification says "P.Eng." but Procedure Step 7.2 says "Architect of Record / Professional Engineer of Record." | REQ-003 states "signed and stamped by a Professional Engineer (P.Eng.)" but Procedure Step 7.2 refers to "Architect of Record / Professional Engineer of Record for stamp and signature." In Alberta, architectural drawings may require an Architect stamp rather than a P.Eng. stamp. The prescriptive direction is inconsistent. | Specification.md; Procedure.md | Specification.md#REQ-003; Procedure.md#Step 7 — Issue for Construction (IFC) | Specification.md#REQ-003 ("P.Eng. licensed to practice in Alberta"); Procedure.md#Step 7.2 ("Architect of Record / Professional Engineer of Record") | Architect / Owner to confirm with Alberta professional licensing requirements | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Specify the applicable edition of the Alberta Building Code and National Building Code of Canada. Currently listed as "ASSUMPTION: likely applicable — specific edition TBD." | Mandatory practice requires identified code editions to confirm compliance. Without a specific edition, compliance determination is indeterminate. | Specification.md | Specification.md#Standards | — | AHJ / Architect | TBD |
| A-003 | A:normative:reviewing | MissingSlot | Procedure | Procedure | Add a step or sub-step describing how building inspection coordination with the County project representative (per R-01 section 3.3.2) integrates with the interior elevations IFC workflow. Currently, inspection coordination is noted in Datasheet Conditions but absent from Procedure steps. | Datasheet records the inspection coordination requirement but Procedure does not include a step for scheduling or facilitating building inspections related to interior elevation scope. Regulatory audit requires this linkage. | Datasheet.md; Procedure.md | Datasheet.md#Conditions ("Inspection Coordination"); Procedure.md#Steps (entire section scanned) | — | Architect / County | TBD |
| A-004 | A:operative:reviewing | MissingSlot | Procedure | Procedure | Add a post-IFC step or note addressing as-built reconciliation: how interior elevations are updated if field conditions differ from IFC drawings. | Procedure ends at IFC issuance. No process audit mechanism exists for post-IFC revisions or as-built reconciliation, which is standard practice for construction drawing sets. | Procedure.md | Procedure.md#Steps (entire section scanned — no post-IFC step) | — | Architect | TBD |

---

## Matrix B — Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Service Pit depth is TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Office dimensions TBD |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Drawing format/scale and sheet count TBD |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Dimensional data is consistently sourced to R-01 and R-04 |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Wash station vs. industrial wash sink ambiguity |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for coordination is adequate across documents |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Cross-reference network is comprehensive |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Septic tank impact on interior layout unclear |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding of deliverable purpose is well-established |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Sufficient expertise context provided in Guidance |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Knowledge coverage is adequate for the deliverable's scope |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs table in Guidance addresses essential discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment guidance is adequate |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic insight is provided through Guidance Considerations |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Principled reasoning is consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record the Service Pit depth as a TBD with responsible party (Structural Engineer) and expected resolution date. Currently noted as "TBD" only in Guidance. | Service Pit depth is an essential fact for interior elevations (trench wall elevation drawing) but is not recorded as a tracked TBD in the Datasheet Attributes table despite being identified in Guidance. | Guidance.md; Datasheet.md | Guidance.md#Service Pit / Trench Depth and Ventilation ("TBD — to be determined at final design"); Datasheet.md#Attributes (not listed) | — | Structural Engineer (DEL-002-06) | TBD |
| B-002 | B:data:sufficiency | WeakStatement | Datasheet | Datasheet | Add Office dimensions or explicit "TBD — Architect to determine at final design" entry to Attributes table, consistent with how other TBD items are recorded. | Office is listed as "Present; dimensions TBD at final design" but this is the only space without even approximate dimensions. Other spaces have at least conceptual dimensions from R-04. Adequate evidence for interior elevation drawing scope requires at minimum a TBD tracking entry. | Datasheet.md | Datasheet.md#Attributes ("Office" row) | — | Architect | TBD |
| B-003 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add Drawing Format/Scale and Number of Drawing Sheets as tracked TBD items with responsible party and expected resolution milestone. | Drawing Format/Scale and Number of Drawing Sheets are listed as TBD with no source, no responsible party, and no expected resolution date. For a comprehensive record, these should be tracked with resolution milestones. | Datasheet.md | Datasheet.md#Attributes ("Drawing Format / Scale" and "Number of Drawing Sheets" rows) | — | Architect | TBD |
| B-004 | B:information:necessity | Conflict | Multi | Guidance | Resolve whether the "Wash Station" on R-04 and the "separate industrial wash sink" in R-01 section 3.4 are the same element or two distinct fixtures, and update interior elevation scope accordingly. | This is already flagged as CFT-001-05-02 in Guidance Conflict Table. The lensing confirms it is a warranted essential signal gap: the number and identity of wash fixture locations shown on interior elevations depends on this resolution. | Guidance.md; Specification.md | Guidance.md#Conflict Table (CFT-001-05-02); Specification.md#REQ-001 | Guidance.md#CFT-001-05-02 Source A (R-04 "Wash Station"); Guidance.md#CFT-001-05-02 Source B (R-01 section 3.4 "separate industrial wash sink") | Architect to confirm with Owner at preliminary design review | TBD |
| B-005 | B:information:consistency | RationaleGap | Guidance | Guidance | Add rationale or design note explaining how the septic tank relocation question (CFT-001-05-01) may affect utility room interior elevation layout and plumbing coordination, so that the Architect can track this dependency. | CFT-001-05-01 flags the septic tank ambiguity but does not explain its potential impact on the interior elevation drawings themselves. The coherent message under this lens requires that the downstream effect on DEL-001-05 be made explicit. | Guidance.md | Guidance.md#Conflict Table (CFT-001-05-01) | — | Plumbing Engineer (PKG-006) | TBD |

---

## Matrix C — Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Compulsory Compliance Baseline | 1 | HAS_ITEMS | Accessible design requirement is assumption-only |
| C:normative:sufficiency | normative | sufficiency | Mandated Substantiation | 0 | NO_ITEMS | Substantiation through verification table is adequate |
| C:normative:completeness | normative | completeness | Obligatory Full Documentation | 1 | HAS_ITEMS | Interior finishes reference is incomplete |
| C:normative:consistency | normative | consistency | Mandated Harmonization | 0 | NO_ITEMS | Terminology is generally harmonized across documents |
| C:operative:necessity | operative | necessity | Operational Prerequisite | 0 | NO_ITEMS | Prerequisites are well-listed in Procedure |
| C:operative:sufficiency | operative | sufficiency | Practiced Execution Readiness | 0 | NO_ITEMS | Execution readiness is addressed by prerequisite table |
| C:operative:completeness | operative | completeness | Thorough Operational Scope | 1 | HAS_ITEMS | Electrical coordination input missing from prerequisites |
| C:operative:consistency | operative | consistency | Reliable Process Coherence | 0 | NO_ITEMS | Process steps are coherent and sequential |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Merit Foundation | 0 | NO_ITEMS | Merit foundation is established through OBJ linkage |
| C:evaluative:sufficiency | evaluative | sufficiency | Warranted Value Appraisal | 0 | NO_ITEMS | Value appraisal is covered by trade-offs analysis |
| C:evaluative:completeness | evaluative | completeness | Holistic Value Assessment | 0 | NO_ITEMS | Value assessment scope is adequate |
| C:evaluative:consistency | evaluative | consistency | Principled Value Consistency | 0 | NO_ITEMS | Value principles are consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Elevate the accessible design assumption in Guidance to a tracked requirement or explicit TBD in Specification. Currently, accessible design is noted only as an assumption in Guidance ("ASSUMPTION: Alberta building code accessible design requirements ... are likely applicable"). | The compulsory compliance baseline for a new building with washroom facilities almost certainly includes barrier-free requirements under Alberta code. This is too consequential to remain as only an assumption in Guidance without a corresponding requirement or tracked TBD in Specification. | Guidance.md; Specification.md | Guidance.md#Washroom / Locker Room — Accessible Design; Specification.md#Requirements (entire section scanned — no accessible design requirement) | — | Architect / AHJ | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add a requirement or cross-reference for interior finish specifications, linking DEL-001-05 interior elevation finish callouts to DEL-001-11 Architectural Specification and DEL-001-08 Finish Schedule. | Datasheet notes "Interior Finishes: TBD — to be specified by Architect in DEL-001-11." Specification REQ-001 lists spaces but does not include a requirement that finish callouts be shown. Procedure Step 3 addresses finishes but without a normative anchor in Specification, obligatory full documentation for finishes is incomplete. | Datasheet.md; Specification.md; Procedure.md | Datasheet.md#Construction ("Interior Finishes" row); Specification.md#Requirements (entire section); Procedure.md#Step 3 | — | Architect | TBD |
| C-003 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add electrical coordination input (PKG-004) to Procedure Prerequisites table, parallel to mechanical (PKG-003) and plumbing (PKG-006) entries. | Specification REQ-012 requires coordination with electrical discipline. Procedure Step 5.1 mentions issuing to electrical sub-consultants for coordination review, but the Prerequisites table does not list electrical design coordination input as a prerequisite. This creates an operational scope gap for the Architect's workflow. | Specification.md; Procedure.md | Specification.md#REQ-012; Procedure.md#Prerequisites ("Upstream Deliverables" table — no PKG-004 entry) | — | Architect / Electrical Engineer | TBD |

---

## Matrix F — Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Prescribed Minimum Standard | 1 | HAS_ITEMS | Guardrail height code reference is assumption |
| F:normative:sufficiency | normative | sufficiency | Regulatory Justification Threshold | 0 | NO_ITEMS | Justification through source citations is adequate |
| F:normative:completeness | normative | completeness | Exhaustive Regulatory Record | 1 | HAS_ITEMS | AHJ local amendments not confirmed |
| F:normative:consistency | normative | consistency | Standardized Regulatory Alignment | 0 | NO_ITEMS | Regulatory references are consistently cited |
| F:operative:necessity | operative | necessity | Foundational Activation Dependency | 1 | HAS_ITEMS | CAD/BIM platform is TBD |
| F:operative:sufficiency | operative | sufficiency | Demonstrated Preparedness | 0 | NO_ITEMS | Prerequisite readiness conditions are stated |
| F:operative:completeness | operative | completeness | Exhaustive Process Accounting | 0 | NO_ITEMS | Process steps are exhaustively accounted for |
| F:operative:consistency | operative | consistency | Systematic Repeatable Logic | 0 | NO_ITEMS | Process logic is systematically repeatable |
| F:evaluative:necessity | evaluative | necessity | Core Evaluative Criterion | 0 | NO_ITEMS | Core criteria are identified through OBJ mapping |
| F:evaluative:sufficiency | evaluative | sufficiency | Justified Quality Judgment | 0 | NO_ITEMS | Quality judgment is justified through verification methods |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Merit Accounting | 1 | HAS_ITEMS | No explicit quality gate between coordination and IFC |
| F:evaluative:consistency | evaluative | consistency | Dependable Valuation Standard | 0 | NO_ITEMS | Valuation standards are consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | WeakStatement | Procedure | Specification | Confirm mezzanine guardrail height code reference. Procedure Step 4.3 states "ASSUMPTION: 1,070 mm per NBC; confirm with AHJ." This prescribed minimum standard should be tracked as a TBD in Specification until confirmed. | The guardrail height is a life-safety minimum. Recording it only as an inline assumption in a Procedure drafting step (rather than a tracked normative requirement with verification) weakens the prescribed minimum standard. | Procedure.md; Specification.md | Procedure.md#Step 4.3; Specification.md#Requirements (no guardrail requirement present) | — | AHJ / Architect | TBD |
| F-002 | F:normative:completeness | TBD_Question | Specification | Specification | Confirm with AHJ which local amendments (Camrose County or Province of Alberta) apply beyond the Alberta Building Code and NBC base codes, and record in Standards table. | Standards table lists "NRC / AHJ local amendments" as "TBD — to be confirmed with County project representative." The exhaustive regulatory record requires this to be resolved or at minimum tracked with a responsible party and expected date. | Specification.md | Specification.md#Standards ("NRC / AHJ local amendments" row) | — | AHJ / County project representative | TBD |
| F-003 | F:operative:necessity | MissingSlot | Procedure | Procedure | Add CAD/BIM platform selection and drawing numbering convention as explicit prerequisite resolution milestones in the Prerequisites table, with responsible party and expected date. | Procedure lists "CAD or BIM authoring software (TBD)" and "Project drawing numbering convention (TBD)" under Tools and Resources but does not track them as foundational activation dependencies with resolution milestones. Without these, Step 1.3 (assign drawing numbers) and Step 4 (draft drawings) cannot proceed. | Procedure.md | Procedure.md#Tools and Resources | — | Architect | TBD |
| F-004 | F:evaluative:completeness | VerificationGap | Specification | Specification | Add a verification step or quality gate for the transition from coordination review (Step 5) to IFC stamping (Step 7). Currently, Step 6 checks only County preliminary approval, not resolution of coordination comments. | The Procedure has coordination review (Step 5) and then County approval check (Step 6) before IFC (Step 7), but there is no explicit quality gate verifying that all coordination comments are resolved (or tracked as TBD) before IFC stamping proceeds. Verification table row for REQ-012 says "no unresolved clashes at IFC issuance" but the Procedure does not enforce this check as a gate. | Specification.md; Procedure.md | Specification.md#Verification (REQ-012 row); Procedure.md#Step 5, Step 6, Step 7 | — | Architect | TBD |

---

## Matrix D — Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Established Binding Mandate | 0 | NO_ITEMS | Binding mandates (code, contract, stamping) are established |
| D:normative:applying | normative | applying | Enforced Compliance Gate | 1 | HAS_ITEMS | No explicit permit application step |
| D:normative:judging | normative | judging | Definitive Regulatory Ruling | 0 | NO_ITEMS | Regulatory ruling mechanisms are defined (permit, AHJ review) |
| D:normative:reviewing | normative | reviewing | Formal Uniformity Verification | 0 | NO_ITEMS | Uniformity verification is addressed through coordination review |
| D:operative:guiding | operative | guiding | Confirmed Workflow Trigger | 1 | HAS_ITEMS | No explicit go/no-go trigger for starting elevation drafting |
| D:operative:applying | operative | applying | Confirmed Task Performance | 0 | NO_ITEMS | Task performance steps are well-defined |
| D:operative:judging | operative | judging | Definitive Capability Finding | 0 | NO_ITEMS | Capability finding addressed through IFC checklist |
| D:operative:reviewing | operative | reviewing | Confirmed Routine Inspection | 0 | NO_ITEMS | Routine inspection process described in Step 7.1 |
| D:evaluative:guiding | evaluative | guiding | Purposeful Worth Benchmark | 0 | NO_ITEMS | OBJ-001 and OBJ-003 serve as worth benchmarks |
| D:evaluative:applying | evaluative | applying | Confirmed Merit Deployment | 0 | NO_ITEMS | Merit deployment addressed through trade-offs |
| D:evaluative:judging | evaluative | judging | Definitive Quality Ruling | 1 | HAS_ITEMS | No acceptance criteria for drawing quality beyond checklist |
| D:evaluative:reviewing | evaluative | reviewing | Confirmed Quality Review | 0 | NO_ITEMS | Quality review addressed through coordination review process |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | MissingSlot | Procedure | Procedure | Add a note or sub-step addressing building permit application timing relative to IFC drawing issuance. REQ-002 verification references "permit issuance by the County" but Procedure does not address when or how permit application occurs. | The enforced compliance gate of permit issuance is identified as a verification method for REQ-002 but is not operationalized in the Procedure. The Architect needs to know whether permit application precedes, accompanies, or follows IFC issuance. | Specification.md; Procedure.md | Specification.md#Verification (REQ-002 row: "Permit issuance; AHJ review"); Procedure.md#Steps (entire section scanned) | — | Owner / Architect | TBD |
| D-002 | D:operative:guiding | VerificationGap | Procedure | Procedure | Add an explicit readiness check or go/no-go criterion at the start of Step 4 (Draft Interior Elevation Drawings) confirming that sufficient coordination input from PKG-002, PKG-003, and PKG-006 has been received per Step 2. | Procedure Step 2 gathers coordination information and flags TBD items, but there is no confirmed workflow trigger between Step 2 and Step 4 that gates drafting on receipt of critical inputs (crane rail elevation, mezzanine deck height, trench depth). An Architect could proceed to drafting with critical inputs still outstanding. | Procedure.md | Procedure.md#Step 2; Procedure.md#Step 4 | — | Architect | TBD |
| D-003 | D:evaluative:judging | VerificationGap | Specification | Specification | Add acceptance criteria for drawing quality attributes (e.g., minimum scale, legibility standard, dimensioning conventions) beyond the binary pass/fail IFC checklist. | Specification verification methods are all procedural (review, check, coordination log) but include no acceptance criteria for the quality of the drawings themselves as communication documents. A definitive quality ruling requires measurable attributes. | Specification.md | Specification.md#Verification (entire table scanned) | — | Architect | TBD |

---

## Matrix X — Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Authoritative Initiation Criterion | 0 | NO_ITEMS | Initiation criteria are defined (County approval of DEL-001-01) |
| X:guiding:sufficiency | guiding | sufficiency | Calibrated Evidence Threshold | 1 | HAS_ITEMS | Coordination log requirements not specified |
| X:guiding:completeness | guiding | completeness | Validated Comprehensive Registry | 1 | HAS_ITEMS | No cross-reference register template |
| X:guiding:consistency | guiding | consistency | Authoritative Interpretive Harmony | 0 | NO_ITEMS | Interpretive guidance is consistent across documents |
| X:applying:necessity | applying | necessity | Actionable Compliance Minimum | 0 | NO_ITEMS | Compliance minimums are actionable through requirements |
| X:applying:sufficiency | applying | sufficiency | Demonstrated Execution Evidence | 1 | HAS_ITEMS | Verification method for REQ-012 is weak |
| X:applying:completeness | applying | completeness | Complete Execution Record | 0 | NO_ITEMS | Records table in Procedure is comprehensive |
| X:applying:consistency | applying | consistency | Repeatable Compliance Measure | 0 | NO_ITEMS | Compliance measures are repeatable |
| X:judging:necessity | judging | necessity | Pivotal Adjudication Basis | 0 | NO_ITEMS | Adjudication basis established through verification methods |
| X:judging:sufficiency | judging | sufficiency | Substantiated Determination Proof | 1 | HAS_ITEMS | REQ-004 verification relies on external deliverable |
| X:judging:completeness | judging | completeness | Total Adjudication Record | 0 | NO_ITEMS | Adjudication records are tracked in Records table |
| X:judging:consistency | judging | consistency | Harmonized Adjudication Logic | 0 | NO_ITEMS | Adjudication logic is consistent |
| X:reviewing:necessity | reviewing | necessity | Essential Scrutiny Basis | 1 | HAS_ITEMS | Internal QA review criteria not specified |
| X:reviewing:sufficiency | reviewing | sufficiency | Demonstrated Audit Scope | 0 | NO_ITEMS | Audit scope is demonstrated through IFC checklist |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Audit Record | 0 | NO_ITEMS | Audit records are comprehensive |
| X:reviewing:consistency | reviewing | consistency | Standardized Scrutiny Logic | 0 | NO_ITEMS | Scrutiny logic is standardized through checklist |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | MissingSlot | Procedure | Procedure | Define coordination log minimum requirements (format, fields, retention) in Procedure or as a cross-reference to a project-level standard. Procedure Step 2.5 and Step 5.3 reference a coordination log but provide no specification of its contents. | A calibrated evidence threshold for coordination requires that the coordination log have defined fields (date, discipline, item, resolution, status). Without this, the log's evidentiary value is indeterminate. | Procedure.md | Procedure.md#Step 2.5; Procedure.md#Step 5.3 | — | Architect | TBD |
| X-002 | X:guiding:completeness | MissingSlot | Procedure | Procedure | Add a discipline cross-reference register template or minimum content requirements. Procedure Records table lists "Discipline Cross-Reference Register" but provides no template or content specification. | A validated comprehensive registry requires that the cross-reference register's structure be defined. Currently it is only named in the Records table with no content guidance. | Procedure.md | Procedure.md#Records ("Discipline Cross-Reference Register" row) | — | Architect | TBD |
| X-003 | X:applying:sufficiency | VerificationGap | Specification | Specification | Strengthen verification method for REQ-012 (Discipline Coordination). "Coordination review documented; no unresolved clashes at IFC issuance" lacks specificity on what constitutes "documented" and what a "clash" is versus a tracked TBD. | Demonstrated execution evidence for discipline coordination requires clear pass/fail criteria. The current verification method for REQ-012 is qualitative only. | Specification.md | Specification.md#Verification (REQ-012 row) | — | Architect | TBD |
| X-004 | X:judging:sufficiency | VerificationGap | Specification | Specification | Add a verification mechanism for REQ-004 (County Preliminary Approval) that does not rely solely on the status of an external deliverable (DEL-001-01). Specify what documentation constitutes "County approval" and where it is filed. | REQ-004 verification is "Documented County approval of preliminary design (DEL-001-01) precedes IFC issuance." This relies entirely on the status of DEL-001-01 and does not specify what form the approval takes (letter, sign-off form, meeting minutes) or where the evidence is filed for DEL-001-05's record. | Specification.md | Specification.md#Verification (REQ-004 row) | — | Owner / County | TBD |
| X-005 | X:reviewing:necessity | MissingSlot | Procedure | Procedure | Define the criteria for the "final internal QA review" referenced in Step 7.1. Currently, Step 7.1 references the IFC Readiness Checklist but does not specify who conducts the review, whether it is independent of the drafter, or how findings are recorded. | Essential scrutiny basis requires that the internal QA review have defined roles, independence criteria, and a record of findings. The current reference to "final internal QA review" is procedurally vague. | Procedure.md | Procedure.md#Step 7.1 | — | Architect | TBD |

---

## Matrix E — Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Substantiated Directive Baseline | 1 | HAS_ITEMS | Renovation scope boundary not precisely defined |
| E:guiding:information | guiding | information | Calibrated Advisory Communication | 0 | NO_ITEMS | Advisory communication in Guidance is calibrated |
| E:guiding:knowledge | guiding | knowledge | Grounded Steering Expertise | 0 | NO_ITEMS | Steering expertise is grounded in source references |
| E:guiding:wisdom | guiding | wisdom | Principled Steering Vision | 0 | NO_ITEMS | Steering vision is principled through Guidance Principles |
| E:applying:data | applying | data | Documented Conformance Evidence | 1 | HAS_ITEMS | Inconsistent naming of building structure |
| E:applying:information | applying | information | Actionable Performance Narrative | 0 | NO_ITEMS | Performance narrative in Procedure is actionable |
| E:applying:knowledge | applying | knowledge | Demonstrated Practice Mastery | 0 | NO_ITEMS | Practice mastery demonstrated through detailed steps |
| E:applying:wisdom | applying | wisdom | Principled Action Awareness | 0 | NO_ITEMS | Action awareness through trade-offs is principled |
| E:judging:data | judging | data | Substantiated Ruling Evidence | 1 | HAS_ITEMS | Verification responsible parties inconsistent |
| E:judging:information | judging | information | Harmonized Ruling Narrative | 0 | NO_ITEMS | Ruling narrative is harmonized across verification tables |
| E:judging:knowledge | judging | knowledge | Comprehensive Ruling Command | 0 | NO_ITEMS | Ruling command is comprehensive through IFC checklist |
| E:judging:wisdom | judging | wisdom | Principled Ruling Clarity | 0 | NO_ITEMS | Ruling clarity is principled |
| E:reviewing:data | reviewing | data | Verified Examination Record | 0 | NO_ITEMS | Examination records are defined in Records table |
| E:reviewing:information | reviewing | information | Framed Inspection Narrative | 1 | HAS_ITEMS | Inspection report scope not defined for DEL-001-05 |
| E:reviewing:knowledge | reviewing | knowledge | Comprehensive Inspection Command | 0 | NO_ITEMS | Inspection command is adequate |
| E:reviewing:wisdom | reviewing | wisdom | Principled Examination Wisdom | 0 | NO_ITEMS | Examination wisdom is principled |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | RationaleGap | Guidance | Guidance | Add a note in Guidance Considerations clarifying the precise boundary of Old North Shop renovation scope for interior elevations: which rooms/walls are included, and the basis for including or excluding specific areas. | Guidance Principle 4 and Specification scope both reference the Old North Shop washroom and locker room renovation, but the precise boundary of what interior elevations are required for the renovation scope (e.g., only washroom/locker, or also mezzanine above?) is not stated. The substantiated directive baseline for renovation scope needs a clearer boundary definition. | Guidance.md; Specification.md | Guidance.md#Renovation Scope Integration; Specification.md#What This Deliverable Covers (paragraph 3) | — | Architect | TBD |
| E-002 | E:applying:data | Normalization | Multi | Guidance | Harmonize the description of the building structural system. Datasheet says "Concrete structure" while the building also has steel elements (cranes, mezzanine framing, steel plates). Consider whether "concrete structure with steel elements" or similar normalized description is more accurate for interior elevation context. | The Datasheet "Structural System" attribute says "Concrete structure" but multiple documents reference steel components (overhead cranes on trolley, mezzanine, steel plates in floor). For documented conformance evidence, the structural system description visible in interior elevations should be accurate. | Datasheet.md | Datasheet.md#Attributes ("Structural System" row); Datasheet.md#Construction (multiple steel references) | — | Structural Engineer / Architect | TBD |
| E-003 | E:judging:data | Normalization | Specification | Specification | Harmonize verification "Responsible" column entries. Some rows use "Architect" alone, others use "Architect / Structural Engineer" or "Architect / County." Establish a convention for primary vs. supporting responsible parties. | The Verification table uses inconsistent patterns for responsible party designation. REQ-001 lists "Architect" alone, REQ-005 lists "Architect / Structural Engineer," REQ-003 lists "Architect / County." A substantiated ruling evidence base should have a consistent convention for responsibility designation. | Specification.md | Specification.md#Verification (entire table) | — | Architect | TBD |
| E-004 | E:reviewing:information | RationaleGap | Procedure | Guidance | Add a note clarifying what "copies of complete inspection reports" (per R-01 section 3.3.2) means in the context of DEL-001-05 interior elevations: which inspections are anticipated, at what construction milestones, and what the Architect's role is in generating or receiving these reports. | Procedure Records table lists "Inspection Report Copies" but the framed inspection narrative does not explain what inspections are anticipated for interior elevation scope, when they occur, or who generates them. The link from the Records table to actual inspection events is unclear. | Procedure.md; Datasheet.md | Procedure.md#Records ("Inspection Report Copies" row); Datasheet.md#Conditions ("Inspection Coordination" row) | — | Architect / County | TBD |

---

## Lens Coverage Summary (All Matrices)

Total lens cells processed: 96
- Matrix A: 12 cells (4 with items, 8 no items)
- Matrix B: 16 cells (5 with items, 11 no items)
- Matrix C: 12 cells (3 with items, 9 no items)
- Matrix F: 12 cells (4 with items, 8 no items)
- Matrix D: 12 cells (3 with items, 9 no items)
- Matrix X: 16 cells (5 with items, 11 no items)
- Matrix E: 16 cells (4 with items, 12 no items)
- Cells with MATRIX_ERROR: 0
- Cells with NO_ITEMS: 68
- Cells with HAS_ITEMS: 28 (unique warranted items, not double-counted across lenses)
