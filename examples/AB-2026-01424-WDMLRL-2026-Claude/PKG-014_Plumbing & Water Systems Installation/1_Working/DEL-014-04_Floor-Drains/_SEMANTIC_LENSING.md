# Semantic Lensing Register: DEL-014-04 Floor Drains & Sump Drains

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-014_Plumbing & Water Systems Installation/1_Working/DEL-014-04_Floor-Drains
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-014-04_Floor-Drains/_CONTEXT.md (Deliverable Overview, Scope of Work, Technical Context)
- _STATUS.md — DEL-014-04_Floor-Drains/_STATUS.md (Status: SEMANTIC_READY)
- _SEMANTIC.md — DEL-014-04_Floor-Drains/_SEMANTIC.md (Matrices A, B, C, F, D, X, E parsed)
- Datasheet.md — DEL-014-04_Floor-Drains/Datasheet.md (Identification, Attributes, Conditions, Construction, References)
- Specification.md — DEL-014-04_Floor-Drains/Specification.md (Scope, Requirements REQ-014-04-01 through -10, Standards, Verification, Documentation)
- Guidance.md — DEL-014-04_Floor-Drains/Guidance.md (Purpose, Principles, Considerations, Trade-offs, Conflict Table)
- Procedure.md — DEL-014-04_Floor-Drains/Procedure.md (Prerequisites, Steps Phase 1-6, Verification, Records)
- _REFERENCES.md — DEL-014-04_Floor-Drains/_REFERENCES.md (Primary References, SOW Documentation, Related Deliverables)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 27
- By document:
  - Datasheet: 3
  - Specification: 10
  - Guidance: 3
  - Procedure: 8
  - Multi: 3
- By matrix:
  - A: 5  B: 3  C: 4  F: 5  D: 3  X: 4  E: 3
- By type:
  - Conflict: 2
  - VerificationGap: 5
  - MissingSlot: 9
  - WeakStatement: 3
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
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Oil/grease interceptor prescriptive gap |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Specific NPC edition not identified |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Acceptance criteria for load rating lack numeric threshold |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Inspection requirements are well-covered across documents |
| A:operative:guiding | operative | guiding | procedural direction | 1 | HAS_ITEMS | No procedure step for oil/grease interceptor coordination |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Execution steps are well-sequenced in Procedure |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification table in Procedure covers performance checks |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records section covers audit trail adequately |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | No rationale for drainage path separation (septic vs. mud sump) |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs table in Guidance addresses material merit |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Quality criteria addressed via load ratings and code compliance |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality documentation artifacts are listed |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | MissingSlot | Specification | Specification | Add requirement for oil/grease interceptor determination: "The Plumbing Engineer shall determine whether an oil/grease interceptor is required upstream of the septic connection per NPC and Alberta environmental regulations, and the determination shall be documented." | Guidance identifies CFT-014-04-02 (oil/grease interceptor ambiguity) but there is no corresponding prescriptive requirement in Specification to mandate a design determination. The conflict table entry alone is not normative. | Guidance.md, Specification.md | Guidance.md#Conflict Table CFT-014-04-02; Specification.md#Requirements (absent) | — | Plumbing Engineer (PKG-006) | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Clarify which edition of the National Plumbing Code of Canada applies. Replace "applicable edition, location TBD" with specific edition year or add a mechanism for the Plumbing Engineer to confirm the applicable edition before procurement. | REQ-014-04-04 and REQ-014-04-05 both reference NPC but state "location TBD" for the specific edition. Without identifying the edition, mandatory practice cannot be verified against a fixed standard. | Specification.md | Specification.md#REQ-014-04-04, #REQ-014-04-05, #Standards | — | Plumbing Engineer / AHJ | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add numeric acceptance criterion for heavy-duty grate load rating (e.g., "minimum H-20 loading per AASHTO or equivalent") or require the Plumbing Engineer to specify the minimum load class in IFC design. | REQ-014-04-06 requires grates "rated for wheel loads and track loads" but the verification method is "Submittal of grate/frame product data confirming load rating" without a numeric threshold to judge compliance against. | Specification.md | Specification.md#REQ-014-04-06, #Verification | — | Plumbing Engineer / Structural Engineer | TBD |
| A-004 | A:operative:guiding | MissingSlot | Procedure | Procedure | Add a procedure step (e.g., Step 1.5 or within Phase 1) for the Plumbing Contractor to coordinate with the Plumbing Engineer on oil/grease interceptor requirements before procurement, referencing Guidance CFT-014-04-02. | Guidance flags oil/grease interceptor as a design-phase determination (Considerations section) and Conflict Table CFT-014-04-02, but Procedure contains no corresponding step to trigger this coordination. | Procedure.md, Guidance.md | Procedure.md#Phase 1; Guidance.md#Considerations — Oil/Grease Separation | — | Plumbing Engineer (PKG-006) | TBD |
| A-005 | A:evaluative:guiding | RationaleGap | Guidance | Guidance | Add rationale paragraph in Purpose or Principles explaining why the septic vs. mud sump drainage path separation matters (environmental regulation, sediment management, septic system protection) and what consequences follow if the paths are inadvertently cross-connected. | Guidance Purpose section mentions two functional zones but does not explain the regulatory or operational rationale for keeping them separate. The Considerations section notes it "should be confirmed" but does not explain the consequences of failure. | Guidance.md | Guidance.md#Purpose, #Considerations — Drainage to Septic vs. Drainage to Mud Sump | — | Plumbing Engineer / Environmental regulator | TBD |

---

## Matrix B — Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Drain count not confirmed |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | TBD attributes in Datasheet |
| B:data:completeness | data | completeness | comprehensive record | 0 | NO_ITEMS | Datasheet attribute tables are comprehensive given design-build stage |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurement data is consistently TBD across docs (appropriate for stage) |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Emergency shower drain sizing signal missing |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for each drain zone is adequately provided |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | All drain zones are accounted for across documents |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messaging is coherent across the four documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental plumbing knowledge is appropriately represented |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise requirements are addressed via submittals and inspections |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Mastery expectations are covered by trade qualifications |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is consistent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Discernment is reflected in conflict table and trade-off table |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment calls are appropriately deferred to design phase |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view is present in Guidance considerations |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is consistent with design-build approach |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | WeakStatement | Datasheet | Datasheet | Clarify whether the "total of four (4) floor drain symbols in the repair bay / main shop area" from the note in Attributes is consistent with Guidance stating "3 floor drains shown in the upper bay areas; 1 floor drain shown in a lower repair bay area." Confirm these describe the same 4 drains to avoid ambiguity. | The Datasheet note says "four (4) floor drain symbols" while Guidance breaks this down as "3 + 1" in different sub-areas. Although numerically consistent, the different framing could cause confusion about whether these are the same drains or different counts. | Datasheet.md, Guidance.md | Datasheet.md#Attributes — Floor Drain Locations (Note); Guidance.md#Considerations — Drain Count and Locations | — | IFC plumbing drawings (DEL-006-03) | TBD |
| B-002 | B:data:sufficiency | TBD_Question | Datasheet | Datasheet | Record TBD: Confirm whether the 8 TBD entries in Datasheet System Configuration (floor drain type, sump drain type, trap requirements, body material, grate material, body diameter/outlet size, flow rate capacity, temperature range) will all be resolved by IFC design or whether any require owner input before design. | Multiple essential data attributes are TBD in Datasheet. While expected in design-build, there is no mechanism documented to track which TBDs are resolved by design vs. which need owner decisions. | Datasheet.md | Datasheet.md#System Configuration, #Conditions | — | Plumbing Engineer (PKG-006) / Owner | TBD |
| B-003 | B:information:necessity | MissingSlot | Specification | Specification | Add a requirement or note addressing emergency shower drain sizing: the drain must be sized to handle the full flow rate of the emergency shower/eye wash unit (typically 75.7 L/min for shower per ANSI Z358.1). Reference interface with DEL-014-05. | Specification REQ-014-04-01 mentions the emergency shower drain by reference to drawing locations but provides no sizing or flow-rate signal. Guidance Examples section mentions "sized to handle full shower flow rate" but this is flagged as assumption and not normative. | Specification.md, Guidance.md | Specification.md#REQ-014-04-01; Guidance.md#Examples | — | Plumbing Engineer / DEL-014-05 | TBD |

---

## Matrix C — Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Authority | 1 | HAS_ITEMS | Alberta Building Code not confirmed as applicable |
| C:normative:sufficiency | normative | sufficiency | Certified Adequacy | 1 | HAS_ITEMS | Plumbing contractor certification/licensing not stated |
| C:normative:completeness | normative | completeness | Comprehensive Conformance | 0 | NO_ITEMS | Conformance requirements are comprehensively listed given known codes |
| C:normative:consistency | normative | consistency | Codified Uniformity | 0 | NO_ITEMS | Code references are consistently applied across docs |
| C:operative:necessity | operative | necessity | Operational Prerequisite | 1 | HAS_ITEMS | Prerequisite for IFC drawings lacks explicit hold-point |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Capability | 0 | NO_ITEMS | Capability demonstration via submittals and inspections is adequate |
| C:operative:completeness | operative | completeness | Thorough Execution | 0 | NO_ITEMS | Execution phases 1-6 are thorough |
| C:operative:consistency | operative | consistency | Reliable Process Control | 1 | HAS_ITEMS | Tolerance values for drain elevation not specified |
| C:evaluative:necessity | evaluative | necessity | Inherent Worth | 0 | NO_ITEMS | Value proposition is clear (water management, safety, code compliance) |
| C:evaluative:sufficiency | evaluative | sufficiency | Substantiated Merit | 0 | NO_ITEMS | Merit is substantiated through functional purpose statements |
| C:evaluative:completeness | evaluative | completeness | Comprehensive Valuation | 0 | NO_ITEMS | All value dimensions are addressed |
| C:evaluative:consistency | evaluative | consistency | Principled Consistency | 0 | NO_ITEMS | Valuation principles are consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Confirm whether the Alberta Building Code is a binding authority for this deliverable's plumbing scope. The Standards table lists it as "ASSUMPTION: applicable; location TBD." Either confirm applicability or remove to avoid implying an unverified obligation. | The Standards table includes Alberta Building Code with "ASSUMPTION" qualifier. If it is enforceable authority, the qualifier should be removed and the specific provision cited. If not confirmed, it should not appear in a normative standards table without qualification. | Specification.md | Specification.md#Standards | — | AHJ / Safety Code Officer | TBD |
| C-002 | C:normative:sufficiency | MissingSlot | Specification | Specification | Add a requirement that the Plumbing Contractor hold a valid Alberta plumbing trade license/certification, or reference the contractual mechanism (CCDC 14-2013) that ensures this. | No document states the required qualifications for the Plumbing Contractor. "Certified Adequacy" lens asks whether the entity performing normative work is demonstrably qualified. The CCDC contract form may address this, but it is not stated in the deliverable documents. | Specification.md | Specification.md#Requirements (absent); entire document scanned | — | Contract / Owner | TBD |
| C-003 | C:operative:necessity | VerificationGap | Procedure | Procedure | Add an explicit hold-point or gate in Procedure Phase 2 stating: "Do not commence underground rough-in until IFC plumbing drawings (DEL-006-03) have been received and reviewed per Step 1.1." Currently the prerequisite table states the dependency but there is no procedural enforcement. | The prerequisite table lists IFC drawings as required, but the procedure steps do not include an explicit hold-point that prevents work from starting without them. In a design-build context where IFC may be delayed, this is an operational risk. | Procedure.md | Procedure.md#Prerequisites — IFC Plumbing Drawings; #Phase 2 | — | Project Manager | TBD |
| C-004 | C:operative:consistency | MissingSlot | Multi | Specification | Add elevation tolerance for drain body installation (e.g., +/- 3mm from design elevation, or per IFC drawing tolerances). Procedure Verification table says "Drain top at finished floor level (or designed depression) +/- tolerance per IFC drawings" but no tolerance is defined in Specification. | Procedure references "tolerance per IFC drawings" for drain elevation verification but Specification does not define or require a tolerance. If IFC drawings also omit this, there is no acceptance criterion for elevation accuracy. | Specification.md, Procedure.md | Specification.md#REQ-014-04-03 (no tolerance); Procedure.md#Verification — "Drain bodies at correct elevation" | — | Plumbing Engineer / IFC drawings | TBD |

---

## Matrix F — Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandatory Certification | 1 | HAS_ITEMS | No requirement for Safety Code permit number documentation |
| F:normative:sufficiency | normative | sufficiency | Established Compliance Threshold | 0 | NO_ITEMS | Compliance threshold approach (inspect + document) is established |
| F:normative:completeness | normative | completeness | Total Regulatory Coverage | 1 | HAS_ITEMS | Local Camrose County amendments not confirmed |
| F:normative:consistency | normative | consistency | Standardized Regulatory Discipline | 0 | NO_ITEMS | Regulatory discipline is consistently applied |
| F:operative:necessity | operative | necessity | Verified Readiness | 1 | HAS_ITEMS | No readiness verification for commissioning handoff |
| F:operative:sufficiency | operative | sufficiency | Competent Delivery Readiness | 0 | NO_ITEMS | Delivery readiness pathway is sufficiently described |
| F:operative:completeness | operative | completeness | Exhaustive Work Coverage | 1 | HAS_ITEMS | Pipe slope verification missing from procedure |
| F:operative:consistency | operative | consistency | Disciplined Process Rigor | 0 | NO_ITEMS | Process rigor is maintained through phased approach |
| F:evaluative:necessity | evaluative | necessity | Validated Significance | 0 | NO_ITEMS | Significance is validated through purpose and objectives |
| F:evaluative:sufficiency | evaluative | sufficiency | Warranted Quality Judgment | 0 | NO_ITEMS | Quality judgment pathway via submittals and inspections is adequate |
| F:evaluative:completeness | evaluative | completeness | Total Quality Recognition | 1 | HAS_ITEMS | No warranty or deficiency-period requirements stated |
| F:evaluative:consistency | evaluative | consistency | Harmonized Value Discipline | 0 | NO_ITEMS | Value discipline is harmonized across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | MissingSlot | Procedure | Procedure | Add to Records table: "Plumbing permit number and issuance date" as a mandatory record. Procedure prerequisites require the permit but Records does not require documenting the permit identification. | Procedure prerequisite states "Plumbing permit must be in place before commencing installation" but the Records table does not include the permit as a retained record. For mandatory certification, the permit itself should be documented. | Procedure.md | Procedure.md#Prerequisites — Building permit; #Records (absent) | — | Plumbing Contractor / PM | TBD |
| F-002 | F:normative:completeness | TBD_Question | Specification | Specification | Record TBD: Confirm whether Camrose County has any local plumbing amendments or additional requirements beyond provincial Safety Codes. REQ-014-04-05 lists "Any local Camrose County amendments or requirements (TBD)" — this needs resolution before construction. | REQ-014-04-05 includes "Any local Camrose County amendments or requirements (TBD)" as a compliance obligation but this remains unresolved. Total regulatory coverage requires this to be confirmed or ruled out. | Specification.md | Specification.md#REQ-014-04-05 | — | Camrose County / AHJ | TBD |
| F-003 | F:operative:necessity | MissingSlot | Procedure | Procedure | Add a commissioning-readiness check or prerequisite in Phase 6 before Step 6.3: verify all prior inspections passed, all tests documented, and as-builts prepared before engaging commissioning agent (DEL-020-01). | Step 6.3 says "Coordinate with Commissioning Agent" but does not define a readiness gate to confirm all prior phases are complete before commissioning. "Verified Readiness" lens requires an explicit readiness check before handoff. | Procedure.md | Procedure.md#Phase 6 — Step 6.3 | — | PM / Commissioning Agent | TBD |
| F-004 | F:operative:completeness | VerificationGap | Procedure | Procedure | Add a verification check for pipe slope: "Verify all drain piping installed at minimum slopes per IFC drawings and NPC requirements. Document slope measurements." Currently, Step 2.2 requires maintaining pipe slopes but no verification step confirms them. | Step 2.2 states "Maintain specified pipe slopes" but the Verification table does not include a pipe slope check. Exhaustive work coverage requires verifying all installed work attributes. | Procedure.md | Procedure.md#Phase 2 — Step 2.2; #Verification (absent) | — | Plumbing Contractor / Inspector | TBD |
| F-005 | F:evaluative:completeness | MissingSlot | Specification | Specification | Add a requirement or note regarding warranty/deficiency period obligations for the floor drain installation, or reference the CCDC 14-2013 warranty provisions that apply. | No document addresses post-completion warranty or deficiency-period obligations for the drain installation. Total quality recognition requires acknowledgment of the quality assurance window beyond substantial completion. | Specification.md | Specification.md#entire document scanned; Procedure.md#entire document scanned | — | Contract (CCDC 14-2013) / Owner | TBD |

---

## Matrix D — Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Authoritative Mandate | 0 | NO_ITEMS | Mandates are clearly established via code references |
| D:normative:applying | normative | applying | Binding Practice Standard | 1 | HAS_ITEMS | Scope boundary not formalized as binding |
| D:normative:judging | normative | judging | Definitive Compliance Ruling | 0 | NO_ITEMS | Compliance determination pathway is clear |
| D:normative:reviewing | normative | reviewing | Institutional Audit Regime | 0 | NO_ITEMS | Audit regime via Safety Code inspections is established |
| D:operative:guiding | operative | guiding | Assured Process Stewardship | 1 | HAS_ITEMS | No designated project lead for drain coordination |
| D:operative:applying | operative | applying | Proven Field Craftsmanship | 0 | NO_ITEMS | Field craft expectations are adequately described |
| D:operative:judging | operative | judging | Work Completion Verification | 0 | NO_ITEMS | Completion verification is addressed in Phase 5-6 |
| D:operative:reviewing | operative | reviewing | Systematic Method Assurance | 0 | NO_ITEMS | Method assurance through phased inspections is systematic |
| D:evaluative:guiding | evaluative | guiding | Affirmed Value Priority | 0 | NO_ITEMS | Value priorities (safety, code compliance, functionality) are affirmed |
| D:evaluative:applying | evaluative | applying | Confirmed Excellence Practice | 0 | NO_ITEMS | Excellence practices are addressed through submittals |
| D:evaluative:judging | evaluative | judging | Conclusive Quality Verdict | 1 | HAS_ITEMS | No final acceptance criterion aggregating all checks |
| D:evaluative:reviewing | evaluative | reviewing | Established Quality Regime | 0 | NO_ITEMS | Quality regime is established through inspection records |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | Conflict | Multi | TBD | Resolve wash bay drain scope boundary: SOW-0027b/DEL-018-05 includes "floor drains and mud sump connection" in the General Contractor's civil scope, while DEL-014-04/SOW-0046 assigns floor drain installation to the Plumbing Contractor. The overlap at the wash bay drain is unresolved. | This conflict is already identified as CFT-014-04-01 in Guidance but has no binding resolution mechanism in Specification. A "Binding Practice Standard" lens requires the scope boundary to be formalized as a normative requirement, not just a conflict-table entry. | Specification.md, Guidance.md | Guidance.md#Conflict Table CFT-014-04-01; Specification.md#REQ-014-04-08 | Guidance.md#CFT-014-04-01 (SOW-0046/DEL-014-04 vs. SOW-0027b/DEL-018-05) | IFC plumbing and civil drawings / written scope boundary agreement | TBD |
| D-002 | D:operative:guiding | RationaleGap | Guidance | Guidance | Add a note in Principles or Considerations identifying who is responsible for overall drainage coordination across the multiple interfaces (DEL-014-02, DEL-014-05, DEL-014-06, DEL-018-05, PKG-011, PKG-006). Currently each interface is mentioned but no single stewardship role is identified. | Multiple interfaces are described across documents but there is no statement of who provides process stewardship across all drain-related interfaces. In a design-build context with multiple contractors, this gap risks coordination failures. | Guidance.md, Procedure.md | Guidance.md#Principles (all), #Considerations; Procedure.md#Prerequisites | — | PM / Design-Builder | TBD |
| D-003 | D:evaluative:judging | VerificationGap | Specification | Specification | Add a final acceptance requirement that aggregates all individual verification checks into a single deliverable acceptance criterion (e.g., "DEL-014-04 is accepted when all verification items in the Verification table are passed and documented, all records in the Documentation table are submitted, and all conflict table rulings are resolved"). | Specification Verification table lists individual checks per requirement but there is no aggregated acceptance criterion that defines when DEL-014-04 as a whole is considered complete and accepted. "Conclusive Quality Verdict" requires a definitive closure statement. | Specification.md | Specification.md#Verification (individual checks only) | — | PM / Owner | TBD |

---

## Matrix X — Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Imperative | 0 | NO_ITEMS | Foundational imperatives are established |
| X:guiding:sufficiency | guiding | sufficiency | Established Governance | 0 | NO_ITEMS | Governance structure is established |
| X:guiding:completeness | guiding | completeness | Exhaustive Directive Scope | 1 | HAS_ITEMS | Trap primer locations not scoped |
| X:guiding:consistency | guiding | consistency | Transparent Directive Alignment | 0 | NO_ITEMS | Directives are aligned across documents |
| X:applying:necessity | applying | necessity | Essential Practice Foundation | 0 | NO_ITEMS | Practice foundations are established |
| X:applying:sufficiency | applying | sufficiency | Demonstrated Workmanship | 1 | HAS_ITEMS | No workmanship standard referenced |
| X:applying:completeness | applying | completeness | Total Installation Record | 0 | NO_ITEMS | Installation record requirements are complete |
| X:applying:consistency | applying | consistency | Consistent Craft Standard | 0 | NO_ITEMS | Craft standards are consistently referenced |
| X:judging:necessity | judging | necessity | Decisive Proof Basis | 1 | HAS_ITEMS | Functional test lacks quantitative criteria |
| X:judging:sufficiency | judging | sufficiency | Adequate Conformance Proof | 0 | NO_ITEMS | Conformance proof through inspections is adequate |
| X:judging:completeness | judging | completeness | Exhaustive Ruling Record | 0 | NO_ITEMS | Ruling records are comprehensively listed |
| X:judging:consistency | judging | consistency | Reliable Ruling Coherence | 0 | NO_ITEMS | Rulings are coherent across verification methods |
| X:reviewing:necessity | reviewing | necessity | Critical Assurance Basis | 0 | NO_ITEMS | Assurance basis through Safety Code inspections is critical and established |
| X:reviewing:sufficiency | reviewing | sufficiency | Adequate Oversight Threshold | 1 | HAS_ITEMS | County PM presence requirement not in Procedure verification |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Oversight Record | 0 | NO_ITEMS | Oversight records are comprehensively listed |
| X:reviewing:consistency | reviewing | consistency | Consistent Oversight Assurance | 0 | NO_ITEMS | Oversight assurance is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | MissingSlot | Specification | Specification | Add clarification of which drain locations require trap primers or trap seal protection devices. REQ-014-04-07 mentions "where drains are subject to infrequent use and evaporation risk" but does not identify which specific locations those are. | Exhaustive directive scope requires that guidance on trap primer applicability be specific enough to act on. Currently the requirement is conditional ("where... subject to infrequent use") but no document identifies which drains qualify. | Specification.md, Guidance.md | Specification.md#REQ-014-04-07; Guidance.md#Principles 4 | — | Plumbing Engineer | TBD |
| X-002 | X:applying:sufficiency | Normalization | Multi | Guidance | Add a note in Guidance clarifying the workmanship standard that applies: is it NPC, Alberta Safety Codes, manufacturer installation instructions, or a combination? The term "workmanship" does not appear in any document, yet the deliverable is an installation scope. | No document references a workmanship standard or installation quality standard beyond code compliance and product submittals. For an installation deliverable, "Demonstrated Workmanship" requires a reference standard for what constitutes acceptable installation quality. | Specification.md, Procedure.md | Specification.md#entire document scanned; Procedure.md#entire document scanned | — | Contract (CCDC 14-2013) / Plumbing Engineer | TBD |
| X-003 | X:judging:necessity | VerificationGap | Procedure | Procedure | Add quantitative acceptance criteria for functional water test: specify maximum time for water to clear drain (e.g., "water shall drain completely within X seconds of pour"), and specify minimum water volume for the test. Currently "flows freely without backup or pooling" is subjective. | Procedure Step 5.3 defines a functional water test but uses subjective language ("flows freely," "no backup or pooling") without quantitative thresholds. Decisive proof requires measurable criteria. | Procedure.md | Procedure.md#Phase 5 — Step 5.3; #Verification — "All drains drain freely" | — | Plumbing Engineer / NPC | TBD |
| X-004 | X:reviewing:sufficiency | Normalization | Procedure | Procedure | Normalize oversight language: Specification REQ-014-04-09 requires "County project representative shall be present for all inspections" but Procedure only mentions County PM presence for rough-in (Step 2.4) and final (Step 5.2) inspections, not for the pre-pour coordination (Step 2.1) or functional test (Step 5.3). Clarify which inspections require County presence. | Specification says "all inspections" require County PM presence, but Procedure selectively mentions County PM for only some inspection steps. This inconsistency could lead to missed oversight at certain hold-points. | Specification.md, Procedure.md | Specification.md#REQ-014-04-09; Procedure.md#Step 2.4, #Step 5.2 (present) vs. #Step 2.1, #Step 5.3 (absent) | Specification.md#REQ-014-04-09 vs. Procedure.md#Steps 2.1, 5.3 | Specification governs (PROPOSAL) | TBD |

---

## Matrix E — Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Documented Advisory Foundation | 0 | NO_ITEMS | Advisory foundation is documented in Guidance |
| E:guiding:information | guiding | information | Transparent Governance Counsel | 0 | NO_ITEMS | Governance counsel is transparent in Guidance |
| E:guiding:knowledge | guiding | knowledge | Authoritative Governance Mastery | 0 | NO_ITEMS | Governance knowledge is adequate |
| E:guiding:wisdom | guiding | wisdom | Prudent Holistic Stewardship | 1 | HAS_ITEMS | No lesson-learned or risk-register linkage |
| E:applying:data | applying | data | Documented Delivery Evidence | 0 | NO_ITEMS | Delivery evidence requirements are documented |
| E:applying:information | applying | information | Integrated Field Communication | 1 | HAS_ITEMS | No communication protocol for multi-contractor coordination |
| E:applying:knowledge | applying | knowledge | Proficient Trade Mastery | 0 | NO_ITEMS | Trade mastery expectations are adequate |
| E:applying:wisdom | applying | wisdom | Prudent Craft Judgment | 0 | NO_ITEMS | Craft judgment is supported by trade-off table |
| E:judging:data | judging | data | Authoritative Judgment Record | 0 | NO_ITEMS | Judgment records are specified |
| E:judging:information | judging | information | Transparent Verdict Account | 0 | NO_ITEMS | Verdict accounts through inspection reports are transparent |
| E:judging:knowledge | judging | knowledge | Authoritative Verdict Mastery | 0 | NO_ITEMS | Verdict authority is established via Safety Code inspector |
| E:judging:wisdom | judging | wisdom | Principled Adjudicative Wisdom | 0 | NO_ITEMS | Adjudicative wisdom is reflected in conflict table |
| E:reviewing:data | reviewing | data | Complete Inspection Evidence | 0 | NO_ITEMS | Inspection evidence requirements are complete |
| E:reviewing:information | reviewing | information | Transparent Audit Account | 0 | NO_ITEMS | Audit accounts are transparently defined |
| E:reviewing:knowledge | reviewing | knowledge | Authoritative Oversight Competence | 0 | NO_ITEMS | Oversight competence is established |
| E:reviewing:wisdom | reviewing | wisdom | Principled Oversight Wisdom | 1 | HAS_ITEMS | No mechanism for capturing inspection lessons or deviations |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:wisdom | RationaleGap | Guidance | Guidance | Add a brief risk statement or lessons-learned note in Considerations acknowledging common failure modes for floor drain installations in heavy equipment shops (e.g., drain body movement during pour, trap seal loss, grate failure under load). This provides prudent stewardship context for field decisions. | Guidance Considerations addresses design-build context, drainage path separation, oil/grease, and inspection sequencing, but does not mention common installation failure modes. Prudent holistic stewardship requires foresight based on known risks. | Guidance.md | Guidance.md#Considerations (absent) | — | Plumbing Engineer / experienced installer | TBD |
| E-002 | E:applying:information | Normalization | Procedure | Procedure | Add a communication protocol note in Prerequisites or Phase 1 specifying the mechanism for multi-contractor coordination (e.g., "All coordination with PKG-011, PKG-018, PKG-006, DEL-014-05, and DEL-014-06 contractors shall be documented via [RFI / coordination log / email to PM]"). | Procedure references coordination with multiple contractors (PKG-011 for concrete, PKG-018 for mud sump, PKG-006 for design) but specifies no communication protocol or documentation mechanism for field communication. "Integrated Field Communication" requires a stated method. | Procedure.md | Procedure.md#Prerequisites, #Phase 1, #Phase 2 | — | PM / Design-Builder | TBD |
| E-003 | E:reviewing:wisdom | Conflict | Datasheet | Multi | Resolve inconsistency in wash bay drain routing description: Datasheet Construction section states "wash bay floor drain connects to mud sump exterior drainage system (DEL-018-05 scope boundary TBD at IFC design)" while Datasheet System Configuration states "Floor and sump drains route to septic holding tank via drain/vent system" without excluding the wash bay drain. Guidance correctly distinguishes the two paths. | Datasheet System Configuration describes "floor and sump drains" routing to septic without carving out the wash bay drain, which routes to the mud sump instead. This is internally inconsistent within Datasheet and inconsistent with Guidance Purpose section which correctly separates the two drainage paths. | Datasheet.md, Guidance.md | Datasheet.md#System Configuration ("Connection to septic") vs. Datasheet.md#Construction ("Wash bay connection"); Guidance.md#Purpose | Datasheet.md#System Configuration vs. Datasheet.md#Construction vs. Guidance.md#Purpose | Guidance.md Purpose section (correctly distinguishes paths) (PROPOSAL) | TBD |

---

## QA Verification

| Check | Validation | Result |
|-------|-----------|--------|
| Coverage complete | Every matrix cell (96 total: A=12, B=16, C=12, F=12, D=12, X=16, E=16) has a Lens Coverage entry | PASS — 96 entries present |
| No invention | All warranted items grounded in evidence from production documents or explicit absence therein | PASS — all items reference specific document sections or confirmed absences |
| Provenance present | Every item has SourcePath + SectionRef | PASS — 27/27 items have provenance |
| Conflicts surfaced | Conflicts have Contenders and HumanRuling = TBD | PASS — 2 conflict items (D-001, E-003) have contenders and HumanRuling = TBD |
| Summary consistent | Summary counts match actual warranted items | PASS — 27 items total; by-matrix: 5+3+4+5+3+4+3=27; by-type: 2+5+9+3+3+3+2+0=27; by-doc: 3+10+3+8+3=27 |
| Schema followed | Output uses the STRUCTURE schema exactly | PASS |
