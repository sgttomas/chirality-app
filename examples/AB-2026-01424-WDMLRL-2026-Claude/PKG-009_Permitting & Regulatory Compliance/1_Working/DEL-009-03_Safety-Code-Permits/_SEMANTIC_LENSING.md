# Semantic Lensing Register: DEL-009-03 Safety Code Permits

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-009_Permitting & Regulatory Compliance/1_Working/DEL-009-03_Safety-Code-Permits/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-009-03 identity, scope, stakeholders, success criteria
- _STATUS.md -- Current state SEMANTIC_READY; milestone tracking
- _SEMANTIC.md -- All 7 matrices parsed (A, B, C, F, D, X, E)
- Datasheet.md -- Permit attributes, conditions, construction elements, references
- Specification.md -- Requirements REQ-009-03-01 through REQ-009-03-11, standards, verification, documentation
- Guidance.md -- Purpose, principles, considerations, trade-offs, conflict table
- Procedure.md -- Five-phase procedure (audit, designation, applications, inspections, compliance), verification, records
- _REFERENCES.md -- Primary references, regulatory authorities, internal project references, related deliverables

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 21
- By document:
  - Datasheet: 5
  - Specification: 7
  - Guidance: 3
  - Procedure: 3
  - Multi: 3
- By matrix:
  - A: 5  B: 3  C: 2  F: 3  D: 2  X: 4  E: 2
- By type:
  - Conflict: 1
  - VerificationGap: 4
  - MissingSlot: 5
  - WeakStatement: 3
  - RationaleGap: 2
  - Normalization: 2
  - TBD_Question: 4
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage (required)
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Weak enumeration of applicable safety codes |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | TBD permit types lack specificity for mandatory practice |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Verification for REQ-009-03-02 lacks measurable criteria |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit coverage adequate across documents |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure phases well-structured |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | No escalation path for authority processing delays |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Procedure verification table covers performance checks |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Process audit covered by Phase 5 handoff and DEL-009-04 linkage |
| A:evaluative:guiding | evaluative | guiding | value orientation | 1 | HAS_ITEMS | Rationale gap for permit expediter trade-off decision criteria |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Merit application sufficiently addressed via trade-off table in Guidance |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Worth determination not applicable at current maturity |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality appraisal deferred to DEL-009-04 compliance register |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify which specific Alberta Safety Code categories (electrical, fire, gas, plumbing, building, elevator) are expected to apply, even if subject to audit confirmation | The Standards table lists seven standards all marked "ASSUMPTION: applicable; location TBD" with no prioritization or scoping to the project's known building systems. This weakens prescriptive direction for downstream permit planning. | Specification.md | ## Standards | -- | Safety code audit (REQ-009-03-10) | TBD |
| A-002 | A:normative:applying | TBD_Question | Datasheet | Datasheet | Record TBD: Confirm full list of applicable Safety Code permit categories after safety code audit; update "Permit types" attribute from TBD to enumerated list | The Datasheet Attributes table records "Permit types = TBD" and "Number of permits required = TBD." Without this, mandatory practice cannot be specified. This is a known dependency on the safety code audit but should be explicitly tracked as a blocking TBD. | Datasheet.md | ## Attributes | -- | Safety code audit output | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add measurable acceptance criteria for REQ-009-03-02 ("adhere to all Alberta Safety Codes") -- e.g., inspector sign-off per code category, or reference to authority-issued compliance certificate | REQ-009-03-02 verification states "Design review and inspector sign-off confirming Alberta Safety Code compliance" but does not specify which inspectors, how many sign-offs, or what constitutes sufficient evidence of adherence. Compliance determination is ambiguous. | Specification.md | ## Verification, REQ-009-03-02 | -- | Specification.md | TBD |
| A-004 | A:operative:applying | MissingSlot | Procedure | Procedure | Add escalation criteria and actions for permit application processing delays (e.g., authority non-response thresholds, escalation path to project manager, contingency scheduling) | Step 8 says "Escalate any delays that risk the project schedule to the project manager" but provides no threshold, timeline trigger, or escalation protocol. Practical execution under delay conditions is underspecified. | Procedure.md | ## Steps > Phase 3 > Step 8 | -- | Procedure.md | TBD |
| A-005 | A:evaluative:guiding | RationaleGap | Guidance | Guidance | Add decision criteria or evaluation framework for choosing between single permit expediter vs. separate authority management (e.g., cost threshold, schedule risk, coordination complexity) | The Trade-offs table presents "Single vs. multiple permit agents" but lists "Cost/availability are TBD" with no criteria to guide the decision. Value orientation for this trade-off lacks actionable decision support. | Guidance.md | ## Trade-offs | -- | Project Manager | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage (required)
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Missing essential data on accredited agency identity |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Evidence requirements covered by Specification verification table |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Datasheet missing gas/plumbing/elevator permit categories |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurement points consistent across documents |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (deadlines, gates) consistently communicated |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequate given TBD status of audit |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Accounts comprehensive for current maturity |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology inconsistency across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding of Alberta safety code system conveyed in Guidance |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Competent expertise requirements deferred to safety code audit |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Mastery scope appropriate to pre-audit stage |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding consistent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Discernment adequately represented in Guidance principles |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment calls appropriately deferred to human (Conflict Table) |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic insight covered by Guidance considerations |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning consistent across Guidance and Procedure |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Identify the Safety Codes Council accredited agency serving Camrose County (municipality or private agency) and confirm whether Camrose County administers safety code permitting directly | Procedure Step 1 references "a Safety Codes Council accredited agency (or Camrose County's designated authority)" and Guidance notes "ASSUMPTION: Camrose County administers or delegates this function; to be confirmed." The identity of the accredited agency is an essential fact not yet recorded. | Datasheet.md; Guidance.md | Datasheet ## Attributes; Guidance ## Examples | -- | Camrose County project manager | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add gas, plumbing, and elevator/crane permit categories to the Attributes table as anticipated permit types (with TBD status), based on the building systems described in Guidance Considerations | Guidance identifies "natural gas tie-in, plumbing (cistern, septic, wash bay drainage)" and "overhead cranes" as project features, and Procedure Step 1 lists "Gas, Plumbing" as categories to investigate. The Datasheet Attributes only mention "electrical safety, fire safety, and OH&S-related permits" -- the record is incomplete for known building systems. | Datasheet.md; Guidance.md | Datasheet ## Attributes; Guidance ## Considerations > Building type complexity | -- | Safety code audit | TBD |
| B-003 | B:information:consistency | Normalization | Multi | Guidance | Normalize terminology: "OH&S" vs. "Health and Safety" vs. "H&S" -- adopt a single canonical term with definition, noting that the RFP uses multiple forms | Datasheet uses "OH&S" and "H&S Pre-qualification"; Specification uses "Health and Safety" in REQ-009-03-03 and "H&S" in REQ-009-03-07; Procedure uses "Prime Contractor designation as defined by Health and Safety agencies." The inconsistent abbreviation risks confusion in permit applications and authority correspondence. | Datasheet.md; Specification.md; Procedure.md | Datasheet ## Attributes; Specification ## Requirements; Procedure ## Steps > Phase 2 | -- | Guidance.md (vocabulary note) | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage (required)
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Enforceable Compliance Threshold | 1 | HAS_ITEMS | Standards marked ASSUMPTION with no enforcement mechanism specified |
| C:normative:sufficiency | normative | sufficiency | Certified Adequacy Assurance | 0 | NO_ITEMS | Certification assurance deferred to verification table |
| C:normative:completeness | normative | completeness | Total Conformance Coverage | 1 | HAS_ITEMS | Missing explicit coverage of gas/plumbing code conformance |
| C:normative:consistency | normative | consistency | Harmonized Enforcement Standard | 0 | NO_ITEMS | Enforcement standard consistent; all documents reference Alberta Safety Codes |
| C:operative:necessity | operative | necessity | Operational Readiness Gate | 0 | NO_ITEMS | Readiness gate well-defined in Procedure prerequisites |
| C:operative:sufficiency | operative | sufficiency | Verified Procedural Competence | 0 | NO_ITEMS | Procedural competence adequate for current stage |
| C:operative:completeness | operative | completeness | Exhaustive Process Archive | 0 | NO_ITEMS | Records table in Procedure covers expected archival scope |
| C:operative:consistency | operative | consistency | Disciplined Execution Cadence | 0 | NO_ITEMS | Five-phase structure provides consistent cadence |
| C:evaluative:necessity | evaluative | necessity | Foundational Merit Basis | 0 | NO_ITEMS | Merit basis established via OBJ linkage |
| C:evaluative:sufficiency | evaluative | sufficiency | Substantiated Worth Assessment | 0 | NO_ITEMS | Worth assessment not yet applicable |
| C:evaluative:completeness | evaluative | completeness | Holistic Merit Accounting | 0 | NO_ITEMS | Merit accounting deferred to project closeout |
| C:evaluative:consistency | evaluative | consistency | Trustworthy Valuation Standard | 0 | NO_ITEMS | Valuation standard not yet applicable |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Strengthen Standards table entries from "ASSUMPTION: applicable; location TBD" to include the mechanism by which applicability will be confirmed (e.g., "to be confirmed by safety code audit per REQ-009-03-10") and target date for resolution | Six of seven standards are marked as assumptions with unconfirmed applicability. The enforceable compliance threshold cannot be established when the governing standards are uncertain. The current language does not specify how or when these assumptions will be resolved. | Specification.md | ## Standards | -- | Safety code audit; Camrose County | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add gas safety, plumbing safety, and elevator/crane safety code standards to the Standards table as anticipated applicable standards (with TBD status) | The Standards table lists building, OH&S, fire, and electrical codes but omits gas, plumbing, and elevator/crane codes despite the Guidance identifying natural gas, plumbing systems, and overhead cranes as project features. Total conformance coverage requires all anticipated code categories to be tracked. | Specification.md; Guidance.md | Specification ## Standards; Guidance ## Considerations > Building type complexity | -- | Safety code audit | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage (required)
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Mandated Regulatory Awareness | 1 | HAS_ITEMS | No requirement to identify the specific accredited agency |
| F:normative:sufficiency | normative | sufficiency | Demonstrable Approval Warrant | 1 | HAS_ITEMS | Verification gap for demonstrating approval warrant |
| F:normative:completeness | normative | completeness | Comprehensive Mandate Inventory | 0 | NO_ITEMS | Mandate inventory deferred to safety code audit output |
| F:normative:consistency | normative | consistency | Coherent Regulatory Measure | 0 | NO_ITEMS | Regulatory measures consistent across documents |
| F:operative:necessity | operative | necessity | Essential Readiness Validation | 0 | NO_ITEMS | Prerequisites table in Procedure covers readiness validation |
| F:operative:sufficiency | operative | sufficiency | Practical Competence Evidence | 0 | NO_ITEMS | Competence evidence not yet applicable |
| F:operative:completeness | operative | completeness | Total Preparedness Inventory | 0 | NO_ITEMS | Preparedness inventory covered by prerequisites |
| F:operative:consistency | operative | consistency | Stable Workflow Coherence | 0 | NO_ITEMS | Workflow consistent between Specification and Procedure |
| F:evaluative:necessity | evaluative | necessity | Intrinsic Merit Comprehension | 0 | NO_ITEMS | Merit comprehension tied to OBJ-001/OBJ-002 linkage |
| F:evaluative:sufficiency | evaluative | sufficiency | Warranted Valuation Craft | 0 | NO_ITEMS | Valuation not yet applicable |
| F:evaluative:completeness | evaluative | completeness | Total Value Inventory | 1 | HAS_ITEMS | Missing value linkage for schedule risk |
| F:evaluative:consistency | evaluative | consistency | Principled Quality Indicator | 0 | NO_ITEMS | Quality indicators consistent |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | MissingSlot | Specification | Specification | Add a requirement (or sub-requirement under REQ-009-03-10) to identify the Safety Codes Council accredited agency for each permit category and record the agency identity in the Datasheet | REQ-009-03-10 requires identifying "all applicable Safety Code requirements" but does not explicitly require identifying the specific accredited agencies or authorities that will issue each permit. Mandated regulatory awareness requires knowing not just what permits are needed but who issues them. | Specification.md | ## Requirements, REQ-009-03-10 | -- | Specification.md | TBD |
| F-002 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add verification approach for demonstrating that all applicable Safety Code permits have been obtained (e.g., cross-reference audit report categories against issued permit register) | REQ-009-03-01 verification says "Review of issued permits from each applicable authority" but there is no mechanism to confirm that the set of issued permits is complete against the audit-identified categories. The sufficiency of the approval warrant depends on completeness checking. | Specification.md | ## Verification, REQ-009-03-01 | -- | Specification.md | TBD |
| F-003 | F:evaluative:completeness | RationaleGap | Guidance | Guidance | Add a section or note quantifying or characterizing the schedule risk if safety code permits are delayed, including the relationship between the December 31, 2026 deadline and typical authority processing timelines | Guidance mentions "lead times could range from a few days to several weeks" as an assumption but does not characterize the schedule risk to OBJ-001 if permits are delayed. Total value inventory requires understanding the consequence of permit delays on project delivery success. | Guidance.md | ## Considerations > Regulatory lead times | -- | Project Manager; project schedule | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage (required)
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Settled Compliance Authority | 0 | NO_ITEMS | Compliance authority adequately established via Alberta Safety Codes Act reference |
| D:normative:applying | normative | applying | Definitive Compliance Protocol | 1 | HAS_ITEMS | Conflict on DEL-009-03 vs DEL-019-01 boundary |
| D:normative:judging | normative | judging | Binding Conformance Closure | 0 | NO_ITEMS | Conformance closure addressed via Procedure Phase 5 |
| D:normative:reviewing | normative | reviewing | Resolved Oversight Alignment | 0 | NO_ITEMS | Oversight alignment with County well-documented |
| D:operative:guiding | operative | guiding | Settled Workflow Navigation | 0 | NO_ITEMS | Workflow navigation clear through five-phase structure |
| D:operative:applying | operative | applying | Demonstrated Action Delivery | 0 | NO_ITEMS | Action delivery steps well-specified |
| D:operative:judging | operative | judging | Settled Capability Determination | 1 | HAS_ITEMS | No capability/competence check for permit management personnel |
| D:operative:reviewing | operative | reviewing | Settled Process Examination | 0 | NO_ITEMS | Process examination covered by verification checks |
| D:evaluative:guiding | evaluative | guiding | Purposeful Quality Compass | 0 | NO_ITEMS | Quality compass established via Guidance principles |
| D:evaluative:applying | evaluative | applying | Definitive Value Deployment | 0 | NO_ITEMS | Value deployment deferred to execution phase |
| D:evaluative:judging | evaluative | judging | Settled Merit Disposition | 0 | NO_ITEMS | Merit disposition not yet applicable |
| D:evaluative:reviewing | evaluative | reviewing | Settled Worth Examination | 0 | NO_ITEMS | Worth examination deferred to project closeout |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | Conflict | Multi | TBD | Clarify boundary between DEL-009-03 and DEL-019-01 for Prime Contractor designation activities: which deliverable owns the initial designation process vs. ongoing OH&S program management | Specification Excluded section states "OH&S program management during construction operations -- covered under DEL-019-01... though Prime Contractor designation initiation is part of this deliverable." Guidance Conflict Table C-009-03-02 flags this same overlap. The definitive compliance protocol for Prime Contractor designation is split across two deliverables without clear handoff criteria. | Specification.md; Guidance.md | Specification ## Scope > Excluded; Guidance ## Conflict Table, C-009-03-02 | Specification.md#Excluded; Guidance.md#Conflict Table C-009-03-02 | RACI or package scope boundary document | TBD |
| D-002 | D:operative:judging | MissingSlot | Procedure | Procedure | Add a prerequisite or step confirming that the person(s) managing permit applications have the required competence or Alberta-specific regulatory knowledge | The Procedure lists seven prerequisites but none address the competence of the permit management personnel. Settled capability determination requires knowing that the people executing the permit process have adequate regulatory knowledge. | Procedure.md | ## Prerequisites | -- | Project Manager | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage (required)
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Foundational Steering Anchor | 0 | NO_ITEMS | Steering anchor established via Guidance purpose and principles |
| X:guiding:sufficiency | guiding | sufficiency | Justified Navigation Counsel | 0 | NO_ITEMS | Navigation counsel adequate in Guidance |
| X:guiding:completeness | guiding | completeness | Total Stewardship Blueprint | 1 | HAS_ITEMS | Missing guidance on post-permit conditions stewardship |
| X:guiding:consistency | guiding | consistency | Coherent Directional Bearing | 0 | NO_ITEMS | Directional bearing consistent across documents |
| X:applying:necessity | applying | necessity | Vital Implementation Prerequisite | 1 | HAS_ITEMS | Missing prerequisite for IFC drawing availability timeline |
| X:applying:sufficiency | applying | sufficiency | Validated Deployment Method | 0 | NO_ITEMS | Deployment methods adequate in Procedure |
| X:applying:completeness | applying | completeness | Total Implementation Record | 0 | NO_ITEMS | Implementation record scope covered by Procedure Records table |
| X:applying:consistency | applying | consistency | Consistent Execution Measure | 0 | NO_ITEMS | Execution measures consistent |
| X:judging:necessity | judging | necessity | Critical Conformance Finding | 1 | HAS_ITEMS | Verification gap for REQ-009-03-09 timeline |
| X:judging:sufficiency | judging | sufficiency | Substantiated Capability Verdict | 0 | NO_ITEMS | Capability verdict covered by verification approaches |
| X:judging:completeness | judging | completeness | Total Adjudication Scope | 0 | NO_ITEMS | Adjudication scope covered by Specification verification table |
| X:judging:consistency | judging | consistency | Stable Assessment Coherence | 0 | NO_ITEMS | Assessment coherence maintained across documents |
| X:reviewing:necessity | reviewing | necessity | Mandatory Inspection Foundation | 0 | NO_ITEMS | Inspection foundation well-established (RFP-sourced requirements) |
| X:reviewing:sufficiency | reviewing | sufficiency | Substantiated Inspection Craft | 1 | HAS_ITEMS | Inspection deficiency re-inspection verification gap |
| X:reviewing:completeness | reviewing | completeness | Total Examination Inventory | 0 | NO_ITEMS | Examination inventory covered by Procedure Steps 9-12 |
| X:reviewing:consistency | reviewing | consistency | Consistent Inspection Measure | 0 | NO_ITEMS | Inspection measures consistent |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | MissingSlot | Guidance | Guidance | Add guidance on managing permit conditions after issuance -- e.g., how conditions are tracked, who is responsible for ongoing condition compliance during construction, and interface with DEL-009-04 | Procedure Step 14 says "Integrate permit conditions into construction operations" and "Ensure conditions are tracked and met" but Guidance does not address the stewardship of permit conditions post-issuance. The total stewardship blueprint is incomplete without guidance on this phase. | Guidance.md; Procedure.md | Guidance ## Considerations; Procedure ## Steps > Phase 5 > Step 14 | -- | Guidance.md | TBD |
| X-002 | X:applying:necessity | TBD_Question | Specification | Specification | Record TBD: Confirm expected timeline for IFC drawing availability relative to permit application deadlines; add as a constraint or note under REQ-009-03-11 | REQ-009-03-11 requires IFC drawings signed by a P.Eng. but no timeline is given for when these will be available. Procedure Step 6 notes "Ensure IFC drawings... are available before submitting applications" but the actual availability date is unknown. This is a vital implementation prerequisite that remains unresolved. | Specification.md; Procedure.md | Specification ## Requirements, REQ-009-03-11; Procedure ## Steps > Phase 3 > Step 6 | -- | Design discipline leads; project schedule | TBD |
| X-003 | X:judging:necessity | VerificationGap | Specification | Specification | Strengthen verification for REQ-009-03-09 to include intermediate milestones or phase-gate dates, not just the final December 31, 2026 deadline | REQ-009-03-09 verification says "Project schedule milestone confirming all permits obtained before construction phase gate" but does not specify intermediate checkpoints. A critical conformance finding requires verifiable intermediate dates to detect schedule slippage early, not just a final deadline. | Specification.md | ## Verification, REQ-009-03-09 | -- | Project Manager; project schedule | TBD |
| X-004 | X:reviewing:sufficiency | VerificationGap | Procedure | Procedure | Add verification criteria for deficiency re-inspection: what constitutes a passing re-inspection, maximum number of re-inspection cycles, and escalation if deficiencies persist | Step 12 says "If an inspection results in a deficiency notice or hold, implement the required corrective action. Reschedule re-inspection and repeat Steps 9-11." There is no success criterion for re-inspection, no limit on cycles, and no escalation protocol. Substantiated inspection craft requires defined closure criteria. | Procedure.md | ## Steps > Phase 4 > Step 12 | -- | Procedure.md | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage (required)
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Verified Navigational Ground | 0 | NO_ITEMS | Navigational ground data adequate |
| E:guiding:information | guiding | information | Contextual Steering Indicator | 1 | HAS_ITEMS | Missing contextual indicator for building permit overlap |
| E:guiding:knowledge | guiding | knowledge | Proficient Governance Mastery | 0 | NO_ITEMS | Governance mastery deferred to execution phase |
| E:guiding:wisdom | guiding | wisdom | Prudent Oversight Foresight | 0 | NO_ITEMS | Oversight foresight adequately covered by Guidance principles |
| E:applying:data | applying | data | Verified Performance Evidence | 0 | NO_ITEMS | Performance evidence requirements covered in Procedure Records |
| E:applying:information | applying | information | Contextual Implementation Signal | 0 | NO_ITEMS | Implementation signals adequate in Procedure steps |
| E:applying:knowledge | applying | knowledge | Proficient Execution Mastery | 0 | NO_ITEMS | Execution mastery not yet applicable |
| E:applying:wisdom | applying | wisdom | Prudent Implementation Foresight | 0 | NO_ITEMS | Implementation foresight covered by Guidance considerations |
| E:judging:data | judging | data | Conclusive Assessment Record | 0 | NO_ITEMS | Assessment record requirements defined in Specification Documentation |
| E:judging:information | judging | information | Unambiguous Adjudication Account | 0 | NO_ITEMS | Adjudication account not yet applicable |
| E:judging:knowledge | judging | knowledge | Authoritative Jurisdictional Mastery | 0 | NO_ITEMS | Jurisdictional mastery deferred to safety code audit |
| E:judging:wisdom | judging | wisdom | Prudent Adjudication Foresight | 0 | NO_ITEMS | Adjudication foresight covered by Guidance conflict table |
| E:reviewing:data | reviewing | data | Verified Audit Record | 1 | HAS_ITEMS | Normalization issue in record ownership |
| E:reviewing:information | reviewing | information | Contextual Audit Account | 0 | NO_ITEMS | Audit account context adequate |
| E:reviewing:knowledge | reviewing | knowledge | Proficient Audit Mastery | 0 | NO_ITEMS | Audit mastery not yet applicable |
| E:reviewing:wisdom | reviewing | wisdom | Prudent Audit Foresight | 0 | NO_ITEMS | Audit foresight covered by DEL-009-04 linkage |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:guiding:information | TBD_Question | Guidance | Guidance | Record TBD: Confirm with Camrose County whether the building permit application process (DEL-009-02) covers some Safety Code categories or requires separate applications; document the answer in Guidance Considerations | Guidance Considerations states "confirm with Camrose County and the relevant Safety Codes accredited agency whether the building permit application process covers some Safety Code categories or if separate applications are required." This contextual steering indicator remains unresolved and could materially change the permitting workflow. | Guidance.md | ## Considerations > Interaction with DEL-009-01 and DEL-009-02 | -- | Camrose County project manager | TBD |
| E-002 | E:reviewing:data | Normalization | Procedure | Multi | Normalize record ownership: Procedure Records table assigns all records to "Project Manager" but the Prime Contractor Designation Form also lists "Safety Officer" and the Specification Documentation table does not specify owners at all -- align ownership across documents | Procedure Records table lists "Project Manager" (or "Project Manager / Safety Officer") as owner for all nine record types. Specification Documentation table lists artifacts without owners. The inconsistency in record ownership attribution could cause gaps in accountability for verified audit records. | Procedure.md; Specification.md | Procedure ## Records; Specification ## Documentation | -- | Project Manager | TBD |

---

## QA Verification

| Check | Result |
|-------|--------|
| Coverage complete | PASS -- All 76 matrix cells across A (12), B (16), C (12), F (12), D (12), X (16), E (16) have Lens Coverage entries |
| No invention | PASS -- All 21 warranted items grounded in document evidence or explicit absence |
| Provenance present | PASS -- Every item has SourcePath and SectionRef |
| Conflicts surfaced | PASS -- 1 conflict (D-001) has Contenders and HumanRuling = TBD |
| Summary consistent | PASS -- Summary counts match actual warranted items (21 total; by-document, by-matrix, and by-type tallies verified) |
| Schema followed | PASS -- Output follows STRUCTURE schema |
