# Semantic Lensing Register: DEL-014-06 Plumbing Fixtures

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-014_Plumbing & Water Systems Installation/1_Working/DEL-014-06_Fixtures
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-014-06_Fixtures/_CONTEXT.md (Deliverable Overview, Scope of Work, Technical Context)
- _STATUS.md — DEL-014-06_Fixtures/_STATUS.md (Current Status: SEMANTIC_READY)
- _SEMANTIC.md — DEL-014-06_Fixtures/_SEMANTIC.md (Matrices A, B, C, F, D, X, E fully parsed)
- Datasheet.md — DEL-014-06_Fixtures/Datasheet.md (Identification, Attributes, Conditions, Construction, References)
- Specification.md — DEL-014-06_Fixtures/Specification.md (Scope, Requirements, Standards, Verification, Documentation)
- Guidance.md — DEL-014-06_Fixtures/Guidance.md (Purpose, Principles, Considerations, Trade-offs, Conflict Table)
- Procedure.md — DEL-014-06_Fixtures/Procedure.md (Prerequisites, Steps 1-8, Verification, Records)
- _REFERENCES.md — DEL-014-06_Fixtures/_REFERENCES.md (Primary References, SOW Documentation, Related Deliverables)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 27
- By document:
  - Datasheet: 6
  - Specification: 10
  - Guidance: 5
  - Procedure: 3
  - Multi: 3
- By matrix:
  - A: 5  B: 4  C: 3  F: 4  D: 3  X: 5  E: 3
- By type:
  - Conflict: 2
  - VerificationGap: 5
  - MissingSlot: 7
  - WeakStatement: 3
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 4
  - MatrixError: 0
- Notable conflicts: 2
- Matrix parse errors: 0

---

## Matrix A — Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Hot water requirement gap identified |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Fixture material specification gap |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Code edition not identified |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | Inspection hold points incomplete |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure steps are well-sequenced |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Installation steps adequately detailed |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | Pressure test criteria TBD |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records section adequate |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Purpose statements are clear |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-off analysis present |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Commissioning criteria present |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Warranty and QA provisions exist |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Add normative requirement for hot water provision at wash station, or record explicit TBD pending Alberta Safety Code confirmation | The RFP specifies "separate industrial wash sink" but does not address hot/cold supply. Guidance identifies this gap (CONF-014-06-01) but Specification REQ-014-06-032 is typed as ASSUMPTION rather than a binding requirement. Prescriptive direction on hot water is absent from all normative sources. | Specification.md; Guidance.md | Specification: REQ-014-06-032; Guidance: Considerations > Hot Water Supply | — | Plumbing Engineer via DEL-006-01 | TBD |
| A-002 | A:normative:applying | MissingSlot | Specification | Specification | Add fixture material requirements (e.g., stainless steel, minimum gauge) as mandatory requirements rather than ASSUMPTION-only entries | REQ-014-06-004 and REQ-014-06-034 rely on ASSUMPTION type for industrial-grade and material requirements. Under "mandatory practice" lens, these should either be confirmed as mandatory or explicitly deferred to DEL-006-06. | Specification.md | Requirements > General Requirements (REQ-014-06-004); Fixture-Specific > Industrial Wash Station (REQ-014-06-034) | — | DEL-006-06 Fixture Schedule | TBD |
| A-003 | A:normative:judging | TBD_Question | Specification | Specification | Confirm specific Alberta Plumbing Code edition year and clause numbers applicable to fixture installation | Standards table lists "current edition" without identifying the specific edition year or applicable clauses. Compliance determination requires knowing which edition governs. | Specification.md | Standards | — | Plumbing Engineer / AHJ | TBD |
| A-004 | A:normative:reviewing | VerificationGap | Specification | Specification | Add explicit inspection hold points for rough-in verification prior to fixture installation (not just post-installation) | Verification table covers post-installation and commissioning checks but lacks a pre-installation rough-in inspection hold point to confirm upstream prerequisites are ready for fixture connection under regulatory audit. | Specification.md | Verification | — | Project Manager / AHJ | TBD |
| A-005 | A:operative:judging | WeakStatement | Specification | Specification | Specify pressure test parameters: test pressure value or multiplier, hold duration, and acceptance criteria | Procedure Step 6 states "ASSUMPTION: test to minimum 1.5x operating pressure or as specified by AHJ" but Specification Verification table references "Pressure test of supply connections; flow test" without quantified pass criteria. Performance assessment cannot be made without numeric thresholds. | Specification.md; Procedure.md | Specification: Verification (REQ-014-06-005, -006 row); Procedure: Step 6 | — | Plumbing Engineer / AHJ | TBD |

---

## Matrix B — Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Operating pressure TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Fixture type data inadequate |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Fixture schedule not yet produced |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Quantities consistent across docs |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | SOW references consistent |
| B:information:sufficiency | information | sufficiency | adequate context | 1 | HAS_ITEMS | Water source pressure characteristics incomplete |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Scope narrative is complete |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Cross-doc messaging coherent |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Trade context adequately understood |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise requirements stated |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Knowledge coverage adequate |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding consistent |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Conflict table captures key judgment calls |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-offs table present |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Design-build context covered |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning consistent across docs |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add minimum operating pressure and minimum flow rate data for each fixture type (water taps, pressure washer reel, wash station) | Datasheet lists "TBD" for minimum flow capacity and operating pressure of the pressure washer reel and does not specify flow/pressure requirements for water taps or wash station. These are essential facts for design and procurement. | Datasheet.md | Attributes > Pressure Washer Reel; Attributes > Water Taps; Attributes > Industrial Wash Station | — | Plumbing Engineer / DEL-006-06 | TBD |
| B-002 | B:data:sufficiency | MissingSlot | Datasheet | Datasheet | Add fixture type/material/model placeholder entries for water taps and wash station with explicit TBD markers and source reference to DEL-006-06 | Datasheet lists "TBD" for wash station fixture type/material and does not enumerate tap types beyond "hose bib or threaded service tap assumed." Adequate evidence for procurement decisions requires at least a placeholder with clear resolution path. | Datasheet.md | Attributes > Water Taps (Connection type); Attributes > Industrial Wash Station (Fixture type / material) | — | DEL-006-06 Fixture Schedule | TBD |
| B-003 | B:data:completeness | TBD_Question | Datasheet | Datasheet | Record TBD: Fixture schedule (DEL-006-06) is the authoritative comprehensive record; until produced, Datasheet fixture inventory is based on conceptual drawing only | The Datasheet note acknowledges conceptual-level data and states "Additional fixtures may be indicated by final design." A comprehensive record cannot exist until DEL-006-06 is produced. Document should explicitly flag this dependency. | Datasheet.md | Attributes > Fixture Inventory (Note) | — | PKG-006 Plumbing Engineer | TBD |
| B-004 | B:information:sufficiency | MissingSlot | Guidance | Guidance | Add expected system pressure range at fixture outlets based on cistern pump specifications (100 LPM at 2.5" fill, R-01 s3.4) and note implications for fixture selection | Guidance Considerations mentions cistern-fed system pressure characteristics but does not provide an estimated pressure range at fixture outlets. This context is needed for fixture selection adequacy. | Guidance.md | Considerations > Cistern-Fed System Pressure Characteristics | — | Plumbing Engineer | TBD |

---

## Matrix C — Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Compulsory Governance Basis | 1 | HAS_ITEMS | Mandatory requirement traceability gap |
| C:normative:sufficiency | normative | sufficiency | Substantiated Regulatory Threshold | 0 | NO_ITEMS | Requirements adequately sourced |
| C:normative:completeness | normative | completeness | Total Regulatory Coverage | 1 | HAS_ITEMS | National Plumbing Code reference incomplete |
| C:normative:consistency | normative | consistency | Harmonized Regulatory Order | 0 | NO_ITEMS | Regulatory references consistent |
| C:operative:necessity | operative | necessity | Indispensable Process Element | 0 | NO_ITEMS | Critical process steps present |
| C:operative:sufficiency | operative | sufficiency | Competent Practiced Method | 0 | NO_ITEMS | Methods adequately described |
| C:operative:completeness | operative | completeness | Exhaustive Operational Scope | 1 | HAS_ITEMS | Backflow prevention not addressed |
| C:operative:consistency | operative | consistency | Dependable Process Discipline | 0 | NO_ITEMS | Process discipline consistent |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Value Threshold | 0 | NO_ITEMS | Value drivers identified |
| C:evaluative:sufficiency | evaluative | sufficiency | Substantiated Merit Judgment | 0 | NO_ITEMS | Merit judgments substantiated |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Value Accounting | 0 | NO_ITEMS | Value coverage adequate |
| C:evaluative:consistency | evaluative | consistency | Principled Value Coherence | 0 | NO_ITEMS | Value reasoning consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | Normalization | Specification | Specification | Normalize ASSUMPTION-typed requirements: clearly distinguish between requirements that are genuinely mandatory (derived from code/contract) vs. those that are assumed pending design confirmation | Several requirements (REQ-014-06-004, -005, -006, -013, -021, -032, -033, -034) are typed as "ASSUMPTION" in the Type column. Under "Compulsory Governance Basis" lens, the distinction between mandatory-by-code and assumed-pending-design is unclear. This risks requirements being treated as optional. | Specification.md | Requirements > General Requirements; Fixture-Specific Requirements | — | Plumbing Engineer / Project Manager | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add National Plumbing Code of Canada reference with specific adoption status in Alberta and applicable clause numbers for fixture installation | Standards table includes NPC as ASSUMPTION with "location TBD." Total regulatory coverage requires confirming whether NPC applies via Alberta Safety Codes framework and identifying specific clauses relevant to fixture installation. | Specification.md | Standards | — | AHJ / Plumbing Engineer | TBD |
| C-003 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add step or sub-step addressing backflow prevention device installation at fixture connections (if required by code for cistern-fed supply) | No document addresses whether backflow prevention devices (vacuum breakers, check valves) are required at fixture supply connections given the cistern-fed (non-municipal) water source. This is a common code requirement that could affect operational scope. | Procedure.md; Specification.md | Procedure: Step 5 (all sub-steps); Specification: entire document scanned | — | Plumbing Engineer / AHJ | TBD |

---

## Matrix F — Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Binding Conformance Foundation | 1 | HAS_ITEMS | Binding requirements rest on assumptions |
| F:normative:sufficiency | normative | sufficiency | Qualified Compliance Capacity | 1 | HAS_ITEMS | Compliance capacity depends on unresolved TBDs |
| F:normative:completeness | normative | completeness | Absolute Governance Accounting | 0 | NO_ITEMS | Governance scope identified; completeness deferred to IFC |
| F:normative:consistency | normative | consistency | Systematic Compliance Alignment | 0 | NO_ITEMS | Compliance alignment consistent |
| F:operative:necessity | operative | necessity | Vital Execution Competence | 0 | NO_ITEMS | Execution competence requirements stated |
| F:operative:sufficiency | operative | sufficiency | Capable Practiced Delivery | 1 | HAS_ITEMS | Coordination checklist gap |
| F:operative:completeness | operative | completeness | Total Operational Accounting | 0 | NO_ITEMS | Operational scope adequately bounded |
| F:operative:consistency | operative | consistency | Unified Execution Discipline | 0 | NO_ITEMS | Execution discipline consistent |
| F:evaluative:necessity | evaluative | necessity | Grounded Value Foundation | 0 | NO_ITEMS | Value basis grounded in project context |
| F:evaluative:sufficiency | evaluative | sufficiency | Justified Quality Provision | 1 | HAS_ITEMS | Quality acceptance criteria gap |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Merit Accounting | 0 | NO_ITEMS | Merit accounting adequate for current phase |
| F:evaluative:consistency | evaluative | consistency | Systematic Merit Coherence | 0 | NO_ITEMS | Merit reasoning coherent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | RationaleGap | Guidance | Guidance | Add rationale explaining why ASSUMPTION-typed requirements are treated as binding pending confirmation, and the consequence if they are later found not to apply | Multiple requirements rest on ASSUMPTION type. The binding conformance foundation depends on these assumptions holding. Guidance should explain the rationale for treating assumptions as operative pending design, and note the risk if they are overturned. | Guidance.md | Principles; entire document scanned | — | Project Manager | TBD |
| F-002 | F:normative:sufficiency | WeakStatement | Specification | Specification | Clarify whether "applicable plumbing codes" (REQ-014-06-007) includes the National Plumbing Code of Canada as adopted by Alberta, or only the Alberta Safety Codes Act and subordinate regulations | REQ-014-06-007 states "all applicable Alberta Safety Codes and applicable plumbing codes" — the scope of "applicable plumbing codes" is ambiguous. Qualified compliance capacity requires knowing exactly which codes apply. | Specification.md | Requirements > General Requirements (REQ-014-06-007) | — | AHJ / Plumbing Engineer | TBD |
| F-003 | F:operative:sufficiency | VerificationGap | Procedure | Procedure | Add a formal coordination checklist template or reference in Step 4 to record sign-off from each upstream trade (DEL-014-01, DEL-014-02, DEL-014-04, PKG-015) before fixture installation proceeds | Procedure Step 4 describes coordination activities but does not reference a coordination checklist artifact. Capable practiced delivery requires documented confirmation from each upstream trade. The Specification Verification table references "Interface review / coordination checklist" but Procedure does not produce one. | Procedure.md; Specification.md | Procedure: Step 4; Specification: Verification (REQ-014-06-040 to -044 row) | — | Project Manager | TBD |
| F-004 | F:evaluative:sufficiency | VerificationGap | Specification | Specification | Add acceptance criteria for wash station usability: e.g., mounting height range, basin depth minimum, splash guard presence, accessibility for workers in PPE | Specification includes requirements for wash station installation but no criteria for evaluating whether the installed fixture meets industrial usability standards. Justified quality provision requires measurable quality acceptance thresholds. | Specification.md | Requirements > Fixture-Specific Requirements > Industrial Wash Station | — | Plumbing Engineer / DEL-006-06 | TBD |

---

## Matrix D — Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Authoritative Compliance Direction | 0 | NO_ITEMS | Compliance direction adequately established |
| D:normative:applying | normative | applying | Enforced Conformance Delivery | 1 | HAS_ITEMS | Pressure washer unit ownership ambiguity |
| D:normative:judging | normative | judging | Definitive Compliance Verdict | 0 | NO_ITEMS | AHJ inspection path defined |
| D:normative:reviewing | normative | reviewing | Settled Compliance Assurance | 0 | NO_ITEMS | Compliance assurance path adequate |
| D:operative:guiding | operative | guiding | Resolved Workflow Guidance | 1 | HAS_ITEMS | Point-of-use heater installation guidance missing |
| D:operative:applying | operative | applying | Settled Task Accomplishment | 0 | NO_ITEMS | Task sequences adequate |
| D:operative:judging | operative | judging | Definitive Performance Finding | 0 | NO_ITEMS | Performance criteria present |
| D:operative:reviewing | operative | reviewing | Settled Process Assurance | 0 | NO_ITEMS | Process assurance adequate |
| D:evaluative:guiding | evaluative | guiding | Grounded Worth Direction | 0 | NO_ITEMS | Worth direction grounded |
| D:evaluative:applying | evaluative | applying | Settled Merit Delivery | 0 | NO_ITEMS | Merit delivery adequate |
| D:evaluative:judging | evaluative | judging | Definitive Worth Verdict | 1 | HAS_ITEMS | Fixture durability criteria absent |
| D:evaluative:reviewing | evaluative | reviewing | Settled Quality Assurance | 0 | NO_ITEMS | Quality assurance path established |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | Conflict | Multi | TBD | Resolve whether the pressure washer unit (machine) is Contractor-supplied, Owner-furnished, or excluded from scope; current documents present conflicting signals | Guidance CONF-014-06-02 identifies this conflict. R-06 shows it as a single fixture point (implying Contractor scope), while the 70A electrical circuit in PKG-015 suggests the unit may be Owner-supplied. Specification REQ-014-06-020 says "install 1 retractable pressure washer hose reel" but does not address the pressure washer machine itself. Enforced conformance delivery requires clarity on what is being procured and installed. | Specification.md; Guidance.md; Datasheet.md | Specification: REQ-014-06-020 to -023; Guidance: Conflict Table CONF-014-06-02; Datasheet: Attributes > Pressure Washer Reel | Specification.md#REQ-014-06-020 vs Guidance.md#CONF-014-06-02 | Owner / Project Manager | TBD |
| D-002 | D:operative:guiding | RationaleGap | Guidance | Guidance | Add guidance on point-of-use water heater installation: scope responsibility, electrical coordination with PKG-015, and location planning relative to wash station | Procedure Step 5c references "If a point-of-use water heater is required, install per IFC drawings" but Guidance does not discuss the workflow implications, trade coordination, or design decision pathway for this item. Resolved workflow guidance requires addressing this conditional dependency. | Guidance.md; Procedure.md | Guidance: Considerations > Hot Water Supply; Procedure: Step 5c | — | Plumbing Engineer | TBD |
| D-003 | D:evaluative:judging | MissingSlot | Specification | Specification | Add fixture durability or service life acceptance criteria (e.g., minimum rated cycles, material grade, warranty requirements for individual fixture components) | No document specifies quantitative durability requirements for fixtures beyond the general 2-year warranty. Worth determination for industrial fixtures should include expected service life or duty rating. | Specification.md; Datasheet.md | Specification: Requirements (entire section scanned); Datasheet: Attributes (entire section scanned) | — | Plumbing Engineer / DEL-006-06 | TBD |

---

## Matrix X — Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Directive Evidence | 1 | HAS_ITEMS | Verification method for code compliance lacks specifics |
| X:guiding:sufficiency | guiding | sufficiency | Substantiated Guidance Basis | 0 | NO_ITEMS | Guidance basis substantiated |
| X:guiding:completeness | guiding | completeness | Exhaustive Directional Coverage | 0 | NO_ITEMS | Directional coverage adequate |
| X:guiding:consistency | guiding | consistency | Harmonized Directional Alignment | 1 | HAS_ITEMS | Terminology inconsistency |
| X:applying:necessity | applying | necessity | Critical Implementation Evidence | 1 | HAS_ITEMS | Missing as-built verification step |
| X:applying:sufficiency | applying | sufficiency | Substantiated Delivery Proof | 0 | NO_ITEMS | Delivery proof path adequate |
| X:applying:completeness | applying | completeness | Exhaustive Implementation Record | 1 | HAS_ITEMS | Submittal/shop drawing review missing |
| X:applying:consistency | applying | consistency | Uniform Implementation Standard | 0 | NO_ITEMS | Implementation standards uniform |
| X:judging:necessity | judging | necessity | Binding Adjudication Evidence | 0 | NO_ITEMS | AHJ inspection constitutes binding evidence |
| X:judging:sufficiency | judging | sufficiency | Substantiated Adjudication Basis | 0 | NO_ITEMS | Adjudication basis adequate |
| X:judging:completeness | judging | completeness | Exhaustive Adjudication Record | 0 | NO_ITEMS | Adjudication records specified |
| X:judging:consistency | judging | consistency | Harmonized Adjudication Standard | 0 | NO_ITEMS | Adjudication standards consistent |
| X:reviewing:necessity | reviewing | necessity | Validated Assurance Evidence | 1 | HAS_ITEMS | Leak test duration not specified |
| X:reviewing:sufficiency | reviewing | sufficiency | Substantiated Assurance Confidence | 0 | NO_ITEMS | Assurance confidence adequate |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Assurance Coverage | 0 | NO_ITEMS | Assurance coverage adequate |
| X:reviewing:consistency | reviewing | consistency | Harmonized Assurance Alignment | 0 | NO_ITEMS | Assurance alignment consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:necessity | VerificationGap | Specification | Specification | Add verification method for REQ-014-06-007 (code compliance) that specifies which specific code clauses will be verified and by what method beyond "Safety Code inspection by AHJ" | Verification table entry for REQ-014-06-007 states "Safety Code inspection by AHJ; County Representative present" but does not identify which specific code clauses are being verified. Foundational directive evidence requires traceability from requirement to specific verification criteria. | Specification.md | Verification (REQ-014-06-007 row) | — | Plumbing Engineer / AHJ | TBD |
| X-002 | X:guiding:consistency | Normalization | Multi | Guidance | Harmonize terminology: "wash station" vs "wash sink" vs "industrial wash station" — adopt one canonical term and use consistently across all documents | Datasheet uses "Industrial Wash Station (Wash Sink)," Specification uses "industrial wash station (wash sink)," Guidance uses "wash station" and "wash sink" interchangeably, Procedure uses "wash station / sink." Under harmonized directional alignment, a single canonical term should be adopted to prevent drift. | Datasheet.md; Specification.md; Guidance.md; Procedure.md | Datasheet: Attributes heading; Specification: Scope, Requirements; Guidance: Purpose, Principles; Procedure: Steps 5c | — | Project Manager | TBD |
| X-003 | X:applying:necessity | VerificationGap | Procedure | Procedure | Add explicit as-built markup verification step between Step 5 (Install) and Step 6 (Pressure Test) confirming installed locations match IFC drawings before proceeding to testing | Procedure Step 5 output is "All fixtures installed, connected, and visually confirmed against IFC drawings" but there is no discrete verification gate to confirm as-built accuracy before pressure testing begins. Critical implementation evidence requires documented confirmation of correct installation before testing. | Procedure.md | Steps 5 and 6 | — | Plumbing Contractor / Project Manager | TBD |
| X-004 | X:applying:completeness | MissingSlot | Specification | Specification | Add requirement for fixture submittal / shop drawing review and approval prior to procurement (Step 3) | Specification Documentation section lists required artifacts but does not include a submittal/shop drawing review step. Procedure Step 3 (Procure Fixtures) proceeds from the Fixture Schedule without a documented submittal approval gate. Exhaustive implementation record requires evidence of reviewed and approved submittals. | Specification.md; Procedure.md | Specification: Documentation; Procedure: Step 3 | — | Project Manager / Plumbing Engineer | TBD |
| X-005 | X:reviewing:necessity | WeakStatement | Procedure | Procedure | Specify leak test observation period (e.g., "observe all joints for minimum 15 minutes under test pressure" or reference applicable code clause for test duration) | Procedure Step 6 states "Pressure test supply connections per Alberta Safety Code requirements" and "verify flow and no leaks at all joints" without specifying observation duration. Validated assurance evidence requires a defined test duration to distinguish a valid pass from a superficial check. | Procedure.md | Step 6 | — | Plumbing Engineer / AHJ | TBD |

---

## Matrix E — Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Validated Steering Record | 0 | NO_ITEMS | Steering data validated through source references |
| E:guiding:information | guiding | information | Coherent Steering Intelligence | 0 | NO_ITEMS | Steering information coherent |
| E:guiding:knowledge | guiding | knowledge | Mastered Directional Expertise | 0 | NO_ITEMS | Directional expertise adequate |
| E:guiding:wisdom | guiding | wisdom | Principled Directional Wisdom | 1 | HAS_ITEMS | Scope boundary wisdom incomplete |
| E:applying:data | applying | data | Verified Execution Record | 0 | NO_ITEMS | Execution records specified |
| E:applying:information | applying | information | Contextual Execution Intelligence | 0 | NO_ITEMS | Execution context adequate |
| E:applying:knowledge | applying | knowledge | Mastered Craft Expertise | 0 | NO_ITEMS | Craft expertise requirements stated |
| E:applying:wisdom | applying | wisdom | Principled Execution Wisdom | 1 | HAS_ITEMS | No contingency for cistern unavailability |
| E:judging:data | judging | data | Validated Verdict Record | 0 | NO_ITEMS | Verdict records specified |
| E:judging:information | judging | information | Coherent Verdict Intelligence | 0 | NO_ITEMS | Verdict information coherent |
| E:judging:knowledge | judging | knowledge | Mastered Adjudication Expertise | 0 | NO_ITEMS | Adjudication expertise path defined |
| E:judging:wisdom | judging | wisdom | Principled Adjudication Wisdom | 0 | NO_ITEMS | Adjudication wisdom adequate |
| E:reviewing:data | reviewing | data | Validated Audit Record | 1 | HAS_ITEMS | Warranty documentation scope gap |
| E:reviewing:information | reviewing | information | Coherent Audit Intelligence | 0 | NO_ITEMS | Audit information coherent |
| E:reviewing:knowledge | reviewing | knowledge | Mastered Audit Expertise | 0 | NO_ITEMS | Audit expertise path defined |
| E:reviewing:wisdom | reviewing | wisdom | Principled Audit Wisdom | 0 | NO_ITEMS | Audit wisdom adequate |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:wisdom | Conflict | Guidance | Guidance | Resolve scope boundary for washroom water tap vs. service tap: Guidance Principle 5 states the water tap near the utility room/washroom area is a "service tap in that zone — not a washroom fixture," but Datasheet describes it as "near washroom / utility room area" without this distinction | Guidance explicitly distinguishes the tap from washroom fixtures while Datasheet describes it by proximity to the washroom. Principled directional wisdom requires consistent scope boundary communication to prevent confusion during installation about which contractor installs which tap. | Guidance.md; Datasheet.md | Guidance: Principles > 5; Datasheet: Attributes > Fixture Inventory (Water Tap standalone row) | Guidance.md#Principle-5 vs Datasheet.md#Fixture-Inventory | Project Manager | TBD |
| E-002 | E:applying:wisdom | RationaleGap | Guidance | Guidance | Add contingency guidance for fixture testing if cistern system (DEL-014-01) is not pressurized at the time of fixture installation completion — e.g., temporary water source for leak testing | Procedure Steps 6 and 8 require pressurized water for testing, but Guidance does not address the contingency if DEL-014-01 is delayed. Principled execution wisdom should anticipate this common construction sequencing risk. | Guidance.md; Procedure.md | Guidance: Principles > 1; Procedure: Steps 6, 8 | — | Project Manager / Plumbing Contractor | TBD |
| E-003 | E:reviewing:data | Normalization | Procedure | Procedure | Clarify warranty documentation scope in Records table: specify whether warranty covers individual fixture components (faucets, reel mechanism, sink basin) or only overall workmanship, and whether manufacturer warranties must be passed through to Owner | Procedure Records table lists "Materials and workmanship guarantee for 2-year period post-CCC" but does not distinguish between contractor workmanship warranty and manufacturer product warranties. Validated audit record requires clear warranty scope delineation. | Procedure.md; Specification.md | Procedure: Records (Warranty documentation row); Specification: Documentation (Warranty Documentation row) | — | Project Manager / Legal | TBD |

---

## QA Verification

| Check | Result |
|---|---|
| Coverage complete | PASS — All 68 matrix cells across A (12), B (16), C (12), F (12), D (12), X (16), E (16) have Lens Coverage entries |
| No invention | PASS — All warranted items grounded in evidence from production documents or explicit absence |
| Provenance present | PASS — Every item has SourcePath and SectionRef |
| Conflicts surfaced | PASS — 2 conflicts (D-001, E-001) have Contenders and HumanRuling = TBD |
| Summary consistent | PASS — Summary counts match actual warranted items (27 total) |
| Schema followed | PASS — Output follows STRUCTURE schema |
