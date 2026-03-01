# Semantic Lensing Register: DEL-005-05 Civil Sections & Details

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-005_Civil Design/1_Working/DEL-005-05_Civil-Sections/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-005-05_Civil-Sections/_CONTEXT.md
- _STATUS.md — DEL-005-05_Civil-Sections/_STATUS.md (state: SEMANTIC_READY)
- _SEMANTIC.md — DEL-005-05_Civil-Sections/_SEMANTIC.md
- Datasheet.md — DEL-005-05_Civil-Sections/Datasheet.md
- Specification.md — DEL-005-05_Civil-Sections/Specification.md
- Guidance.md — DEL-005-05_Civil-Sections/Guidance.md
- Procedure.md — DEL-005-05_Civil-Sections/Procedure.md
- _REFERENCES.md — DEL-005-05_Civil-Sections/_REFERENCES.md (read; pointers only, scope not expanded)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 2
  - Specification: 13
  - Guidance: 3
  - Procedure: 5
  - Multi: 5
- By matrix:
  - A: 6  B: 3  C: 4  F: 4  D: 3  X: 5  E: 3
- By type:
  - Conflict: 2
  - VerificationGap: 7
  - MissingSlot: 5
  - WeakStatement: 5
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 2
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4) -- Canonical

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Weak statement on code references |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | IFC stamp verification gap |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Code compliance specificity gap |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | Missing inspection hold-point detail |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure provides adequate procedural direction |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Step-by-step execution is well covered in Procedure |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | Verification lacks quantitative acceptance criteria |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Procedure verification table covers process audit adequately |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance principles section addresses value orientation |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs section in Guidance covers merit application |
| A:evaluative:judging | evaluative | judging | worth determination | 1 | HAS_ITEMS | No acceptance criteria for cost/value trade-offs |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Procedure verification table covers quality checks |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify specific Alberta Safety Code volumes/editions applicable to civil site work (e.g., Alberta Building Code part/section) in REQ-005-05-011 or Standards table | REQ-005-05-011 references "applicable Alberta Safety Codes" without identifying specific volumes or editions; this ambiguity could lead to different interpretations of compliance scope | Specification.md | REQ-005-05-011; Standards table | — | Civil engineer / permit authority | TBD |
| A-002 | A:normative:applying | VerificationGap | Specification | Specification | Add verification approach for drawing sheet completeness against the anticipated artifact list (i.e., confirm all detail types in _CONTEXT.md are addressed or formally deferred) | Specification lists 12 requirements with verification approaches, but no verification entry confirms that the full set of anticipated artifact types from _CONTEXT.md has been addressed in the final drawing set | Specification.md | Verification table | — | Civil engineer | TBD |
| A-003 | A:normative:judging | TBD_Question | Specification | Specification | Record TBD: Which specific Alberta Safety Code volumes and municipal bylaw references govern compliance determination for civil site work at this site? Consult permit authority and Camrose County planning department | Compliance determination requires knowing the specific codes; the Standards table lists "specific applicable volumes/editions TBD" and "Camrose County Development/Building Permit Conditions — Not yet issued — TBD" | Specification.md | Standards table | — | Permit authority / Camrose County | TBD |
| A-004 | A:normative:reviewing | MissingSlot | Procedure | Procedure | Add inspection hold-point or witness-point requirements for regulatory/County review prior to cover-up of civil elements (e.g., subgrade inspection before gravel placement) | Procedure Step 12 addresses IFC stamp and issue but does not identify specific inspection hold-points where the permit authority or County representative must witness or approve work before it is covered. RFP references County inspection involvement. | Procedure.md | Step 12: IFC Stamp and Issue | — | Civil engineer / County project representative | TBD |
| A-005 | A:operative:judging | VerificationGap | Specification | Specification | Add quantitative acceptance criteria for gravel section thickness verification (e.g., minimum compacted depth measurement method, tolerance) | REQ-005-05-002 and REQ-005-05-003 require design for motor scraper load and gravel material specification, but the Verification table relies on "design review" and "drawing review" without specifying measurable acceptance thresholds for the as-built section | Specification.md | Verification table — REQ-005-05-002, REQ-005-05-003 | — | Civil engineer / geotech report | TBD |
| A-006 | A:evaluative:judging | RationaleGap | Guidance | Guidance | Add rationale for the standard-vs-project-specific detail trade-off decision criteria — what determines when a standard detail is acceptable vs. when a project-specific detail is required? | Guidance Trade-offs table proposes using standard details by reference where applicable, but does not articulate the decision criteria for determining when a standard detail is sufficient vs. when project conditions require a custom detail | Guidance.md | Trade-offs table — row 2 | — | Civil engineer | TBD |

---

## Matrix B -- Conceptualization (4x4) -- Canonical

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Missing geotechnical data values |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet provides adequate evidence from available sources |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Incomplete reference list |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurements from source documents are consistently cited |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (drainage, load, stamp) are present |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for design decisions is adequate given available inputs |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Documents provide comprehensive narrative accounts |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology inconsistency across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental engineering understanding is reflected in Guidance |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Documents reflect competent civil engineering expertise |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Mastery is demonstrated through comprehensive procedure |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Engineering understanding is consistent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Guidance principles reflect appropriate discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-off judgments are appropriate |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Cross-package coordination shows holistic awareness |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Geotechnical design parameters (CBR, frost depth, subgrade classification, groundwater depth) are essential facts required for section design. Consult PKG-008 geotechnical report when available | Datasheet references geotechnical input as required but no geotechnical parameter values are recorded. These are essential facts for section design that cannot be assumed. | Datasheet.md | Conditions table — Geotechnical Input | — | PKG-008 geotechnical consultant | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add reference entry for Appendix B (Shop) drawing (R-04) in _REFERENCES.md; _REFERENCES.md currently lists only R-01 and R-07 but Datasheet.md cites R-04 (Appendix B) | _REFERENCES.md lists only two primary references (R-01 and R-07) while Datasheet.md cites three accessed references including R-04 (Appendix B Shop). The reference register is incomplete. | _REFERENCES.md; Datasheet.md | _REFERENCES.md — Primary References; Datasheet.md — References table | — | Document controller | TBD |
| B-003 | B:information:consistency | Normalization | Multi | Guidance | Normalize terminology: "motor scraper" vs. "large construction equipment" — clarify in Guidance whether "motor scraper" is the governing design vehicle or one example of the design vehicle class | Specification REQ-005-05-002 uses "large construction equipment, including a motor scraper" while Guidance Principle 2 treats "motor scraper" as the specific design vehicle. Datasheet uses "large construction equipment, including motor scraper." The governing design vehicle identity should be unambiguous. | Specification.md; Guidance.md; Datasheet.md | REQ-005-05-002; Guidance Principle 2; Datasheet Attributes — Driving Surface Design Criterion | — | Civil engineer | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Obligatory Compliance Threshold | 1 | HAS_ITEMS | Missing compaction standard reference |
| C:normative:sufficiency | normative | sufficiency | Justified Conformance Baseline | 1 | HAS_ITEMS | Weak conformance baseline for drainage |
| C:normative:completeness | normative | completeness | Total Regulatory Coverage | 1 | HAS_ITEMS | Incomplete regulatory reference set |
| C:normative:consistency | normative | consistency | Harmonized Regulatory Adherence | 0 | NO_ITEMS | Regulatory references are consistently applied across documents |
| C:operative:necessity | operative | necessity | Essential Operational Readiness | 0 | NO_ITEMS | Procedure prerequisites table adequately captures readiness |
| C:operative:sufficiency | operative | sufficiency | Capable Methodical Execution | 0 | NO_ITEMS | Procedure steps are methodically organized |
| C:operative:completeness | operative | completeness | Comprehensive Process Delivery | 0 | NO_ITEMS | 12-step procedure covers full delivery process |
| C:operative:consistency | operative | consistency | Standardized Operational Control | 0 | NO_ITEMS | Process control is standardized through prerequisite checks |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Merit Recognition | 0 | NO_ITEMS | Guidance recognizes intrinsic merit of construction clarity |
| C:evaluative:sufficiency | evaluative | sufficiency | Warranted Professional Appraisal | 1 | HAS_ITEMS | Missing P.Eng. review scope statement |
| C:evaluative:completeness | evaluative | completeness | Holistic Worth Assessment | 0 | NO_ITEMS | Trade-offs table provides holistic assessment |
| C:evaluative:consistency | evaluative | consistency | Principled Valuation Coherence | 0 | NO_ITEMS | Value judgments are consistently principled |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Specify the compaction standard to be used (e.g., ASTM D698 Standard Proctor, ASTM D1557 Modified Proctor, or equivalent Alberta standard) in REQ-005-05-003 or Standards table | The obligation to specify compaction requirements is stated in REQ-005-05-003 ("compaction requirements") but no specific compaction test standard is named. Procedure Step 9 references "Proctor, ASTM D698 or equivalent" but this is in a general notes context, not as a normative requirement. | Specification.md; Procedure.md | REQ-005-05-003; Procedure Step 9.1 | — | Civil engineer / geotech report | TBD |
| C-002 | C:normative:sufficiency | WeakStatement | Specification | Specification | Strengthen REQ-005-05-004 to specify minimum cross-fall slope percentage or reference the drainage plan as the governing source for slope values | REQ-005-05-004 requires "positive site drainage" and that "grades direct surface runoff away from building foundations" but does not specify minimum slopes or reference a quantitative standard for what constitutes "positive drainage" in gravel surface conditions | Specification.md | REQ-005-05-004 | — | Civil engineer / drainage design (DEL-005-03) | TBD |
| C-003 | C:normative:completeness | MissingSlot | Specification | Specification | Add specific Alberta Infrastructure or Transportation standards for gravel road/surface design to the Standards table, or record as TBD with the source to consult | Standards table lists "Alberta Infrastructure Technical Standards" as an ASSUMPTION with "Not cited directly in RFP — location TBD." Total regulatory coverage requires identifying the actual applicable standard(s). | Specification.md | Standards table — Alberta Infrastructure Technical Standards row | — | Civil engineer | TBD |
| C-004 | C:evaluative:sufficiency | MissingSlot | Procedure | Specification | Add a statement defining the scope of the P.Eng. engineering review (Step 10) — specifically, what constitutes an acceptable level of engineering review for this drawing set before the stamp is applied | Procedure Step 10 describes the internal engineering review activities but does not state what constitutes a sufficient review (e.g., independent check, back-check of calculations, peer review). The professional appraisal scope is undefined. | Procedure.md | Step 10: Internal Engineering Review | — | Civil engineer of record | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Authoritative Mandate Constraint | 1 | HAS_ITEMS | Missing frost depth constraint |
| F:normative:sufficiency | normative | sufficiency | Substantiated Conformance Benchmark | 1 | HAS_ITEMS | Conformance benchmark gap for gravel gradation |
| F:normative:completeness | normative | completeness | Exhaustive Governance Scope | 0 | NO_ITEMS | Governance scope is addressed, pending permit conditions |
| F:normative:consistency | normative | consistency | Systematic Prescriptive Clarity | 0 | NO_ITEMS | Prescriptive requirements are systematically clear |
| F:operative:necessity | operative | necessity | Fundamental Process Prerequisite | 1 | HAS_ITEMS | Survey datum prerequisite gap |
| F:operative:sufficiency | operative | sufficiency | Demonstrated Methodical Capability | 0 | NO_ITEMS | Procedure demonstrates methodical capability |
| F:operative:completeness | operative | completeness | Exhaustive Operational Authority | 0 | NO_ITEMS | Operational authority is established through P.Eng. stamp requirement |
| F:operative:consistency | operative | consistency | Systematic Procedural Stability | 0 | NO_ITEMS | Procedure steps are systematic and stable |
| F:evaluative:necessity | evaluative | necessity | Fundamental Worth Awareness | 0 | NO_ITEMS | Guidance reflects worth awareness through principles |
| F:evaluative:sufficiency | evaluative | sufficiency | Justified Quality Authority | 0 | NO_ITEMS | Quality authority is justified through P.Eng. requirement |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Appraisal Authority | 1 | HAS_ITEMS | Missing constructability review as formal requirement |
| F:evaluative:consistency | evaluative | consistency | Principled Worth Transparency | 0 | NO_ITEMS | Worth considerations are transparent in trade-offs |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | TBD_Question | Specification | Specification | Record TBD: What is the design frost depth for central Alberta at this site? This is a binding constraint on subbase depth. Consult PKG-008 geotechnical report. | Guidance identifies frost depth as a key geotech input and notes freeze-thaw is relevant for subbase design, but no requirement in Specification addresses frost depth as a mandatory constraint on section design. This is a binding need that is absent from the normative document. | Guidance.md; Specification.md | Guidance — Considerations — Alberta freeze-thaw context; Specification — entire Requirements section scanned | — | PKG-008 geotechnical consultant | TBD |
| F-002 | F:normative:sufficiency | WeakStatement | Specification | Specification | Strengthen REQ-005-05-003 to specify the conformance benchmark for gravel gradation — either reference DEL-005-07 specification section or state the governing standard for gradation testing | REQ-005-05-003 requires the section detail to "specify gravel material type, gradation, depth, and compaction requirements" but the conformance benchmark for what constitutes acceptable gradation is not identified. The note says "pending geotechnical report and Civil Specification" but no test standard is named. | Specification.md | REQ-005-05-003 | — | Civil engineer / DEL-005-07 | TBD |
| F-003 | F:operative:necessity | VerificationGap | Procedure | Procedure | Add a prerequisite check for survey datum confirmation — Procedure should include a step to confirm the survey datum and benchmark before drafting sections with elevation references | Procedure Step 2 addresses geotechnical inputs but does not include a step for confirming the survey datum reference point. Sections that reference elevations (drainage inverts, finished grades) require a confirmed datum as a fundamental process prerequisite. | Procedure.md | Step 2: Obtain Geotechnical Inputs; Prerequisites table | — | PKG-008 surveyor | TBD |
| F-004 | F:evaluative:completeness | RationaleGap | Guidance | Guidance | Add rationale for whether constructability review by the contractor (PKG-018) is expected as part of the quality appraisal process, or whether this is optional given the design-build contract form | Procedure Step 11 mentions circulating sheets to PKG-018 "if contractor is engaged at time of design" but there is no rationale in Guidance for why or when constructability review provides value, or whether the CCDC 14-2013 contract form requires or encourages it | Guidance.md; Procedure.md | Guidance — entire document scanned; Procedure Step 11 | — | Project manager / contract administrator | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Resolved Directive Authority | 0 | NO_ITEMS | Directive authority is resolved through P.Eng. stamp requirement |
| D:normative:applying | normative | applying | Enforced Compliance Baseline | 1 | HAS_ITEMS | Conflict on aggregate supply vs. specification |
| D:normative:judging | normative | judging | Definitive Conformance Ruling | 0 | NO_ITEMS | Conformance ruling process is addressed in Procedure Step 10/12 |
| D:normative:reviewing | normative | reviewing | Formal Accountability Inspection | 0 | NO_ITEMS | Accountability inspection addressed through IFC stamp and transmittal |
| D:operative:guiding | operative | guiding | Resolved Operational Steering | 0 | NO_ITEMS | Procedure provides resolved operational steering |
| D:operative:applying | operative | applying | Confirmed Practical Delivery | 1 | HAS_ITEMS | Conflict on civil-plumbing boundary |
| D:operative:judging | operative | judging | Definitive Execution Evaluation | 0 | NO_ITEMS | Procedure verification table provides execution evaluation approach |
| D:operative:reviewing | operative | reviewing | Resolved Procedural Review | 0 | NO_ITEMS | Interdisciplinary review process is defined |
| D:evaluative:guiding | evaluative | guiding | Resolved Worth Guidance | 0 | NO_ITEMS | Guidance principles provide resolved worth guidance |
| D:evaluative:applying | evaluative | applying | Confirmed Quality Deployment | 1 | HAS_ITEMS | Drawing register not in Specification as a required artifact |
| D:evaluative:judging | evaluative | judging | Definitive Valuation Ruling | 0 | NO_ITEMS | Trade-offs table provides valuation rulings |
| D:evaluative:reviewing | evaluative | reviewing | Resolved Merit Accountability | 0 | NO_ITEMS | Records table in Procedure supports merit accountability |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | Conflict | Multi | TBD | Surface conflict: Datasheet states aggregate is "Supplied by County (OUT of Proponent scope)" while Specification REQ-005-05-003 requires the section detail to "specify gravel material type, gradation, depth, and compaction requirements" — if County-supplied aggregate does not meet design gradation, compliance enforcement baseline is unresolved | Guidance CONF-005-05-01 already identifies this conflict. The Enforced Compliance Baseline lens confirms this is a genuine normative-applying conflict: the compliance baseline for gravel specification cannot be enforced if the supply is out of scope. | Datasheet.md; Specification.md; Guidance.md | Datasheet — Conditions — Aggregate Supply; Specification — REQ-005-05-003; Guidance — CONF-005-05-01 | Datasheet.md#Conditions (County supply); Specification.md#REQ-005-05-003 (gradation specification) | Civil engineer — confirm County aggregate meets design gradation | TBD |
| D-002 | D:operative:applying | Conflict | Multi | Guidance | Surface conflict: Guidance Trade-off row 3 proposes "civil shows exterior sump construction including connection stub to building; plumbing shows interior drain piping to stub" but Specification REQ-005-05-006 requires the civil detail to show "connection to the wash bay drain" without specifying where the boundary is. Procedure Step 5.2 says "confirm with PKG-006" but the boundary definition is not formalized | The practical delivery boundary between civil and plumbing scope at the mud sump is described differently across documents. A formal boundary definition is needed to confirm practical delivery scope. | Specification.md; Guidance.md; Procedure.md | Specification — REQ-005-05-006; Guidance — Trade-offs row 3; Procedure — Step 5.2 | Specification.md#REQ-005-05-006 (connection to wash bay drain); Guidance.md#Trade-offs (connection stub boundary) | Civil engineer / PKG-006 plumbing engineer | TBD |
| D-003 | D:evaluative:applying | VerificationGap | Specification | Specification | Add the drawing register as a required output artifact in Specification Documentation section, with verification that all anticipated detail types are accounted for (issued or formally deferred) | Procedure Step 1.2 requires preparing a drawing register, and Procedure Verification confirms it is used for completeness checking, but Specification Documentation section lists only "Required Artifacts" from _CONTEXT.md without requiring a drawing register as a controlled output. Quality deployment is incomplete without this. | Specification.md; Procedure.md | Specification — Documentation; Procedure — Step 1.2, Verification table | — | Civil engineer | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Imperative Clarity | 1 | HAS_ITEMS | Missing requirement for retaining wall decision |
| X:guiding:sufficiency | guiding | sufficiency | Justified Steering Competence | 0 | NO_ITEMS | Guidance provides justified steering |
| X:guiding:completeness | guiding | completeness | Total Directive Comprehension | 0 | NO_ITEMS | Directives are comprehensively documented |
| X:guiding:consistency | guiding | consistency | Coherent Governance Stability | 0 | NO_ITEMS | Governance is coherent across documents |
| X:applying:necessity | applying | necessity | Obligatory Implementation Basis | 1 | HAS_ITEMS | Missing implementation basis for edge restraints |
| X:applying:sufficiency | applying | sufficiency | Validated Delivery Proficiency | 0 | NO_ITEMS | Delivery proficiency is validated through procedure steps |
| X:applying:completeness | applying | completeness | Exhaustive Implementation Record | 1 | HAS_ITEMS | Incomplete coordination record requirement |
| X:applying:consistency | applying | consistency | Stable Execution Coherence | 0 | NO_ITEMS | Execution approach is coherent across documents |
| X:judging:necessity | judging | necessity | Authoritative Assessment Foundation | 1 | HAS_ITEMS | Missing assessment basis for drainage slope verification |
| X:judging:sufficiency | judging | sufficiency | Substantiated Determination Basis | 0 | NO_ITEMS | Determination bases are substantiated through reference to upstream inputs |
| X:judging:completeness | judging | completeness | Total Assessment Documentation | 0 | NO_ITEMS | Assessment documentation approach is comprehensive |
| X:judging:consistency | judging | consistency | Coherent Conformance Measure | 0 | NO_ITEMS | Conformance measures are coherent |
| X:reviewing:necessity | reviewing | necessity | Obligatory Oversight Foundation | 1 | HAS_ITEMS | Missing transmittal acknowledgment verification |
| X:reviewing:sufficiency | reviewing | sufficiency | Validated Oversight Competence | 0 | NO_ITEMS | Oversight competence is validated through review steps |
| X:reviewing:completeness | reviewing | completeness | Total Oversight Record | 0 | NO_ITEMS | Records table in Procedure provides total oversight record |
| X:reviewing:consistency | reviewing | consistency | Stable Accountability Measure | 0 | NO_ITEMS | Accountability measures are stable and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:necessity | VerificationGap | Specification | Specification | Add a verification step or decision gate for the retaining wall inclusion/exclusion decision — the verification table has no entry for confirming whether retaining walls are required or formally excluded | Guidance notes retaining wall applicability depends on DEL-005-02 grading design and proposes omitting from first issue. However, no verification entry in Specification or Procedure confirms the decision was made and documented. A formal decision record is a foundational imperative. | Specification.md; Guidance.md | Specification — Verification table (no retaining wall entry); Guidance — Considerations — Retaining wall applicability | — | Civil engineer | TBD |
| X-002 | X:applying:necessity | WeakStatement | Specification | Specification | Clarify REQ-005-05-010 to specify what types of edge restraint are anticipated or reference the design standard governing edge restraint selection | REQ-005-05-010 requires "any required edging or restraint" at pad interfaces without specifying what constitutes adequate restraint or referencing a design standard. The implementation basis is weak. | Specification.md | REQ-005-05-010 | — | Civil engineer | TBD |
| X-003 | X:applying:completeness | MissingSlot | Procedure | Procedure | Add a step or substep requiring formal documentation of interdisciplinary coordination outcomes (not just "record and resolve") — specify the coordination log format or minimum content requirements | Procedure Step 11.2 says "Record and resolve all coordination comments" but does not specify what constitutes an adequate coordination record. For an exhaustive implementation record, the coordination documentation requirements should be defined. | Procedure.md | Step 11: Interdisciplinary Coordination Review | — | Civil engineer / project manager | TBD |
| X-004 | X:judging:necessity | VerificationGap | Specification | Specification | Add a quantitative verification approach for drainage slope adequacy — specify minimum cross-fall slope or reference the drainage plan (DEL-005-03) as the authoritative source for slope values used in assessment | Specification Verification for REQ-005-05-004 says "Confirm all finished grades in sections slope away from structures to drainage features" but provides no quantitative threshold for what constitutes adequate slope. The authoritative assessment foundation for drainage slope verification is missing. | Specification.md | Verification table — REQ-005-05-004 | — | Civil engineer / DEL-005-03 | TBD |
| X-005 | X:reviewing:necessity | VerificationGap | Procedure | Procedure | Add a verification step confirming that IFC transmittal acknowledgment has been received from all required parties (Owner, contractor, permit authority) before the deliverable is considered complete | Procedure Step 12.3 lists issue recipients and Records table mentions "IFC transmittal records — Confirmed delivery" but the Verification table entry is "Transmittal records confirm receipt by Owner and contractor" without including permit authority. Oversight foundation requires all recipients. | Procedure.md | Step 12.3; Verification table — IFC set issued and acknowledged; Records table | — | Project manager | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Verified Authority Record | 1 | HAS_ITEMS | Normalization of reference IDs |
| E:guiding:information | guiding | information | Contextual Steering Indicator | 0 | NO_ITEMS | Contextual steering is well communicated |
| E:guiding:knowledge | guiding | knowledge | Comprehensive Governance Mastery | 0 | NO_ITEMS | Governance knowledge is comprehensive |
| E:guiding:wisdom | guiding | wisdom | Prudent Governance Perspective | 0 | NO_ITEMS | Governance perspective is prudent |
| E:applying:data | applying | data | Validated Implementation Evidence | 1 | HAS_ITEMS | Normalization of TBD notation |
| E:applying:information | applying | information | Contextual Implementation Signal | 0 | NO_ITEMS | Implementation signals are contextually adequate |
| E:applying:knowledge | applying | knowledge | Demonstrated Operational Mastery | 0 | NO_ITEMS | Operational mastery is demonstrated |
| E:applying:wisdom | applying | wisdom | Prudent Implementation Judgment | 0 | NO_ITEMS | Implementation judgments are prudent |
| E:judging:data | judging | data | Authoritative Verdict Evidence | 0 | NO_ITEMS | Verdict evidence is authoritatively sourced |
| E:judging:information | judging | information | Contextualized Verdict Account | 0 | NO_ITEMS | Verdict accounts are contextualized |
| E:judging:knowledge | judging | knowledge | Comprehensive Determination Mastery | 0 | NO_ITEMS | Determination mastery is demonstrated |
| E:judging:wisdom | judging | wisdom | Prudent Appraisal Discernment | 0 | NO_ITEMS | Appraisal discernment is prudent |
| E:reviewing:data | reviewing | data | Validated Inspection Evidence | 1 | HAS_ITEMS | Missing as-built survey verification |
| E:reviewing:information | reviewing | information | Contextual Accountability Signal | 0 | NO_ITEMS | Accountability signals are contextually appropriate |
| E:reviewing:knowledge | reviewing | knowledge | Demonstrated Oversight Authority | 0 | NO_ITEMS | Oversight authority is demonstrated |
| E:reviewing:wisdom | reviewing | wisdom | Principled Oversight Judgment | 0 | NO_ITEMS | Oversight judgment is principled |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:data | Normalization | Multi | Datasheet | Normalize reference identifiers: Datasheet uses "R-01", "R-04", "R-07" with dashes while _REFERENCES.md uses "R-01", "R-07" with bold formatting and different descriptive text. Adopt a single reference ID format and ensure all documents cite the same canonical reference table. | Reference identifiers are used inconsistently in format and completeness between Datasheet.md References table and _REFERENCES.md. For a verified authority record, the reference data should use a single canonical format. | Datasheet.md; _REFERENCES.md | Datasheet — References table; _REFERENCES.md — entire file | — | Document controller | TBD |
| E-002 | E:applying:data | Normalization | Multi | Guidance | Normalize TBD notation: documents use "TBD", "TBD —", "(TBD)", "type TBD", "— TBD", and "values are TBD" inconsistently. Adopt a single TBD notation convention (e.g., "TBD" with parenthetical context) and document it in Guidance or a general notes convention. | TBD placeholders are used throughout all four documents with inconsistent formatting. For validated implementation evidence, TBD items should use a normalized notation to support automated tracking and resolution verification. | Specification.md; Procedure.md; Datasheet.md; Guidance.md | entire documents scanned | — | Document controller / civil engineer | TBD |
| E-003 | E:reviewing:data | RationaleGap | Guidance | Guidance | Add rationale for whether as-built survey verification of civil sections is expected as part of the inspection evidence, and if so, at what stage (pre-cover, post-compaction, final grade) | Procedure Records table lists "Survey data (PKG-008) — Filed as upstream input reference" but does not address as-built survey verification of the constructed civil sections. For validated inspection evidence, the deliverable should clarify whether as-built survey verification is within scope or is handled separately. | Procedure.md; Guidance.md | Procedure — Records table; Guidance — entire document scanned | — | Civil engineer / County project representative | TBD |
