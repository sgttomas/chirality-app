# Semantic Lensing Register: DEL-01-05 Appendix H - Schedule B - Cost Breakdown

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/PKG-001_Proposal_Compliance_Commercial_and_Team_Qualifications/1_Working/DEL-01-05_AppendixH-ScheduleB-CostBreakdown
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-01-05_AppendixH-ScheduleB-CostBreakdown/_CONTEXT.md (deliverable identity, scope SOW-0006, objective OBJ-007)
- _STATUS.md -- DEL-01-05_AppendixH-ScheduleB-CostBreakdown/_STATUS.md (current state: SEMANTIC_READY)
- _SEMANTIC.md -- DEL-01-05_AppendixH-ScheduleB-CostBreakdown/_SEMANTIC.md (matrices A, B, C, F, D, X, E parsed; 92 cells total)
- Datasheet.md -- DEL-01-05_AppendixH-ScheduleB-CostBreakdown/Datasheet.md (identification, attributes, conditions, construction sections, references)
- Specification.md -- DEL-01-05_AppendixH-ScheduleB-CostBreakdown/Specification.md (scope, requirements R-01 through R-09, standards, verification V-01 through V-04)
- Guidance.md -- DEL-01-05_AppendixH-ScheduleB-CostBreakdown/Guidance.md (purpose, principles P-001 through P-007, considerations C-001 through C-005, trade-offs T-001 through T-004, examples)
- Procedure.md -- DEL-01-05_AppendixH-ScheduleB-CostBreakdown/Procedure.md (prerequisites, steps 1-7, verification V-01 through V-05, records)
- _REFERENCES.md -- DEL-01-05_AppendixH-ScheduleB-CostBreakdown/_REFERENCES.md (cross-references to DEL-01-04, DEL-01-06, DEL-01-03)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 18
- By document:
  - Datasheet: 4
  - Specification: 7
  - Guidance: 3
  - Procedure: 4
- By matrix:
  - A: 3  B: 2  C: 3  F: 3  D: 2  X: 3  E: 2
- By type:
  - Conflict: 1
  - VerificationGap: 5
  - MissingSlot: 5
  - WeakStatement: 2
  - RationaleGap: 2
  - Normalization: 2
  - TBD_Question: 1
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Tax treatment prescriptive gap |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Addendum acknowledgement placement ambiguity |
| A:normative:judging | normative | judging | compliance determination | 0 | NO_ITEMS | Compliance criteria well-addressed across docs |
| A:normative:reviewing | normative | reviewing | regulatory audit | 1 | HAS_ITEMS | Missing verification for tax separation |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Steps well-structured in Procedure |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Execution steps clear |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Performance criteria present in V-04 |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Process audit covered by V-01 through V-05 |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Value orientation clear in Guidance purpose |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Merit criteria well-supported |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Evaluation weight documented in Datasheet |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | QA/QC adequately covered |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | MissingSlot | Specification | Specification | Add a requirement (or sub-requirement under R-01 or R-07) explicitly requiring that taxes be shown separately from cost subtotals per RFP Section 8, as the Datasheet Conditions table states this but Specification has no corresponding requirement | Datasheet Conditions table states "Taxes must be separated from pricing subtotals; not embedded in unit costs" but Specification requirements R-01 through R-09 do not include a dedicated tax-separation requirement; this prescriptive direction is absent from the normative authority document | Datasheet.md, Specification.md | Datasheet.md#Conditions, Specification.md#Requirements | -- | Specification.md | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Clarify in R-09 whether the addendum acknowledgement line must appear on Schedule B specifically, or only anywhere within Appendix H; current language allows ambiguity about placement | R-09 states the acknowledgement "may appear on Schedule A header or as a dedicated section within Appendix H; if on Schedule A, it is referenced on Schedule B" -- the mandatory practice for Schedule B itself is ambiguous (reference vs. contain) | Specification.md | Specification.md#R-09 | -- | Specification.md | TBD |
| A-003 | A:normative:reviewing | VerificationGap | Specification | Specification | Add a verification check (or expand V-03) to explicitly verify that taxes are shown separately from pricing subtotals, as required by Datasheet Conditions | Datasheet records a tax separation condition sourced from RFP Section 8, but none of Specification's four verification items (V-01 through V-04) explicitly check for tax separation compliance | Specification.md, Datasheet.md | Specification.md#Verification, Datasheet.md#Conditions | -- | Specification.md | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Missing site area fact in Specification |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Evidence requirements present |
| B:data:completeness | data | completeness | comprehensive record | 0 | NO_ITEMS | Datasheet construction sections comprehensive |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurement references consistent |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals documented |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequate across docs |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Account is comprehensive |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Contingency percentage normalization |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Understanding requirements clear |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Expertise requirements present in roles |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Mastery expectations present |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding consistent |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Discernment topics adequately guided |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment guidance present |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic coverage adequate |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning principles consistent |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Specification | Datasheet | Record the 12-acre developable site area as a named attribute in Datasheet Attributes table; currently only mentioned incidentally in Specification scope text and Procedure Step 1 | The 12-acre site area is an essential fact used in Sitework cost estimation (Procedure Step 1, Specification scope) but is not recorded as a formal attribute in Datasheet; it appears only in narrative passages | Datasheet.md, Specification.md, Procedure.md | Datasheet.md#Attributes, Specification.md#Scope, Procedure.md#Step 1 | -- | Datasheet.md | TBD |
| B-002 | B:information:consistency | Normalization | Multi | Guidance | Normalize contingency percentage language: Guidance T-002 recommends "7%" as starting point, Procedure Step 2 states "Contingency: 7% of base contract cost", but neither Specification nor Datasheet specifies any contingency percentage -- clarify whether 7% is a recommendation or a requirement | Guidance (T-002) and Procedure (Step 2) both state 7% contingency, treating it as a settled value; Specification R-01 and Datasheet mention contingency as a line item but do not specify any percentage; the coherent message about this value is inconsistent in authority level across docs | Guidance.md, Procedure.md, Specification.md, Datasheet.md | Guidance.md#T-002, Procedure.md#Step 2, Specification.md#R-02, Datasheet.md#Construction Section 1 | -- | Guidance.md | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Regulatory Imperative | 1 | HAS_ITEMS | Bonding percentage not in Specification |
| C:normative:sufficiency | normative | sufficiency | Compliant Substantiation | 0 | NO_ITEMS | Substantiation requirements adequate |
| C:normative:completeness | normative | completeness | Exhaustive Compliance Scope | 1 | HAS_ITEMS | Missing landscaping/fencing in Specification |
| C:normative:consistency | normative | consistency | Regulatory Coherence | 0 | NO_ITEMS | Regulatory references coherent |
| C:operative:necessity | operative | necessity | Operational Prerequisite | 0 | NO_ITEMS | Prerequisites well-documented |
| C:operative:sufficiency | operative | sufficiency | Competent Practice | 0 | NO_ITEMS | Practice guidance sufficient |
| C:operative:completeness | operative | completeness | Comprehensive Execution | 0 | NO_ITEMS | Execution steps comprehensive |
| C:operative:consistency | operative | consistency | Systematic Discipline | 0 | NO_ITEMS | Discipline consistently applied |
| C:evaluative:necessity | evaluative | necessity | Foundational Merit | 0 | NO_ITEMS | Merit basis established |
| C:evaluative:sufficiency | evaluative | sufficiency | Defensible Valuation | 1 | HAS_ITEMS | Market reasonableness ranges inconsistency |
| C:evaluative:completeness | evaluative | completeness | Holistic Valuation | 0 | NO_ITEMS | Valuation scope complete |
| C:evaluative:consistency | evaluative | consistency | Calibrated Integrity | 0 | NO_ITEMS | Integrity calibration adequate |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | MissingSlot | Specification | Specification | Add bonding percentage (50% Performance Bond + 50% Labour & Materials Payment Bond) as a stated parameter within R-04 or as a new requirement, rather than relying solely on Datasheet to carry this regulatory fact | The 50%/50% bonding structure is a binding requirement (RFP Section 5.3.1) recorded in Datasheet Attributes and Construction Section 1, but Specification R-04 (CCIP Insurance Inclusion) does not state the bonding percentages; the regulatory imperative for bonding terms has no normative home in Specification | Datasheet.md, Specification.md | Datasheet.md#Construction Section 1 (GR-04, GR-05), Specification.md#R-04 | -- | Specification.md | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add Landscaping/Site Restoration and Site Fencing/Gates to Specification R-02 structural organization or R-05 checklist; currently these appear only in Datasheet (S-06, S-07) as ASSUMPTIONs and in Procedure Step 3 but are absent from Specification scope categories | Datasheet lists S-06 (Landscaping) and S-07 (Site Fencing) as assumption-based cost lines; Procedure Step 3 includes them in the populate steps; Specification R-02 Sitework list mentions "grading, utilities, drainage, parking, landscape" but omits fencing, and neither S-06 nor S-07 is reflected in R-05 Addendum 03 checklist; exhaustive compliance scope requires all costed items to have normative coverage | Datasheet.md, Specification.md, Procedure.md | Datasheet.md#Construction Section 3, Specification.md#R-02, Specification.md#R-05, Procedure.md#Step 3 | -- | Specification.md | TBD |
| C-003 | C:evaluative:sufficiency | Conflict | Procedure | Guidance | Resolve the inconsistency between Procedure V-04 market reasonableness ranges and Guidance C-003 option pricing guidance for access control: Procedure V-04 states "Access control: typical $30-60k for 6-10 controlled points" but Guidance C-003 does not provide a corresponding range, while Procedure's generator range ($40-80k) differs from no corresponding benchmark in Guidance | Procedure V-04 introduces specific dollar ranges for market reasonableness that do not appear in Guidance or Specification; these ranges function as de facto acceptance criteria but are embedded in a procedure document rather than a normative or evaluative source; defensible valuation requires consistent authority for benchmark ranges | Procedure.md, Guidance.md | Procedure.md#V-04, Guidance.md#C-003 | Procedure.md#V-04, Guidance.md#C-003 | Guidance.md | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Authoritative Mandate | 0 | NO_ITEMS | Mandates well-documented |
| F:normative:sufficiency | normative | sufficiency | Warranted Compliance | 1 | HAS_ITEMS | Missing verification for Option 6 exact amount |
| F:normative:completeness | normative | completeness | Total Regulatory Scope | 0 | NO_ITEMS | Regulatory scope complete |
| F:normative:consistency | normative | consistency | Mandated Alignment | 1 | HAS_ITEMS | Schedule A line mapping inconsistency |
| F:operative:necessity | operative | necessity | Process Foundation | 0 | NO_ITEMS | Process foundations established |
| F:operative:sufficiency | operative | sufficiency | Demonstrated Proficiency | 0 | NO_ITEMS | Proficiency demonstration adequate |
| F:operative:completeness | operative | completeness | Total Operational Scope | 0 | NO_ITEMS | Operational scope complete |
| F:operative:consistency | operative | consistency | Coordinated Standards | 0 | NO_ITEMS | Standards coordinated |
| F:evaluative:necessity | evaluative | necessity | Irreducible Criterion | 1 | HAS_ITEMS | Evaluation weight not in Specification |
| F:evaluative:sufficiency | evaluative | sufficiency | Justified Credibility | 0 | NO_ITEMS | Credibility justification present |
| F:evaluative:completeness | evaluative | completeness | Comprehensive Justification | 0 | NO_ITEMS | Justification comprehensive |
| F:evaluative:consistency | evaluative | consistency | Principled Valuation Standard | 0 | NO_ITEMS | Valuation standard consistent |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add an explicit verification check (in V-01 or V-03) that Additional Option 6 equals exactly $20,000; current V-01 checks "no blank cost cells" and V-03 checks "FF&E is shown only as Additional Option 6 ($20,000)" but the exact-amount verification is embedded in compliance narrative, not as a discrete pass/fail criterion | R-03 requires FF&E to be priced as $20,000 and V-03 mentions it in a checklist, but the warranted compliance test for the exact dollar amount is not called out as a standalone verification criterion with explicit pass condition | Specification.md | Specification.md#V-01, Specification.md#V-03 | -- | Specification.md | TBD |
| F-002 | F:normative:consistency | Normalization | Multi | Specification | Standardize Schedule A line numbering references: Specification R-06 uses "line 1-1" through "line 1-7" notation; Datasheet uses "Schedule A line 1-1" in one place but does not list all seven line mappings; Procedure V-02 repeats the full mapping -- ensure consistent notation and a single authoritative mapping table | The Schedule A line references (1-1 through 1-7) appear in Specification R-06 and Procedure V-02 but with different contextual framing; Datasheet only partially references these; mandated alignment requires one canonical mapping to prevent transcription errors | Specification.md, Datasheet.md, Procedure.md | Specification.md#R-06, Datasheet.md#Construction (Base Contract Total note), Procedure.md#V-02 | -- | Specification.md | TBD |
| F-003 | F:evaluative:necessity | RationaleGap | Guidance | Guidance | Add rationale in Guidance explaining why the 35-point evaluation weight (highest single criterion) matters for cost breakdown strategy and how it should influence the level of detail and transparency in Schedule B | Datasheet records "Part of 35-point Proposal Price criterion -- highest-weighted criterion overall" and Guidance Purpose mentions "35 of 100 evaluation points", but neither Guidance Principles nor Considerations explains how this irreducible evaluation criterion should shape cost breakdown decisions (e.g., whether to favor transparency over competitive concealment) | Datasheet.md, Guidance.md | Datasheet.md#Attributes (Evaluation weight), Guidance.md#Purpose | -- | Guidance.md | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Governing Authority | 0 | NO_ITEMS | Governing authority clear |
| D:normative:applying | normative | applying | Binding Fulfillment | 0 | NO_ITEMS | Fulfillment requirements clear |
| D:normative:judging | normative | judging | Definitive Compliance Ruling | 0 | NO_ITEMS | Compliance ruling criteria present |
| D:normative:reviewing | normative | reviewing | Resolved Oversight | 0 | NO_ITEMS | Oversight mechanisms present |
| D:operative:guiding | operative | guiding | Established Workflow | 1 | HAS_ITEMS | Freeze/unfreeze workflow gap |
| D:operative:applying | operative | applying | Validated Execution | 0 | NO_ITEMS | Execution validation present |
| D:operative:judging | operative | judging | Settled Performance Review | 0 | NO_ITEMS | Performance review settled |
| D:operative:reviewing | operative | reviewing | Finalized Process Audit | 0 | NO_ITEMS | Process audit finalized |
| D:evaluative:guiding | evaluative | guiding | Resolved Merit Standard | 0 | NO_ITEMS | Merit standard resolved |
| D:evaluative:applying | evaluative | applying | Validated Worth | 1 | HAS_ITEMS | Second storey cost impact |
| D:evaluative:judging | evaluative | judging | Decisive Justification | 0 | NO_ITEMS | Justification decisive |
| D:evaluative:reviewing | evaluative | reviewing | Settled Quality Review | 0 | NO_ITEMS | Quality review settled |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:operative:guiding | WeakStatement | Procedure | Procedure | Strengthen the freeze/unfreeze protocol in Step 7: currently states "No changes permitted after freeze except by joint approval from Commercial Lead and Project Manager" but does not describe the re-reconciliation steps required if Schedule B is reopened (only Note 1 mentions "Schedule B must be reopened and reconciled" without procedural detail) | The established workflow for post-freeze changes is stated as a constraint but lacks procedural direction for how to execute re-reconciliation; this could lead to inconsistent practices if Schedule A is revised late | Procedure.md | Procedure.md#Step 7, Procedure.md#Notes (Note 1) | -- | Procedure.md | TBD |
| D-002 | D:evaluative:applying | TBD_Question | Procedure | Guidance | Add guidance on how to handle the second storey option mentioned in Procedure Note 5 -- specifically, whether Schedule B should include a conditional line or whether this is an alternate pricing scenario to be documented in DEL-01-06 value alternatives | Procedure Note 5 states "If the Proponent's concept design includes a second storey, the vertical transportation and structural costs must be reflected in Buildings costs" but neither Specification nor Guidance addresses how this impacts Schedule B structure or whether it requires an alternate pricing line; validated worth requires clear guidance on conditional scope elements | Procedure.md, Guidance.md, Specification.md | Procedure.md#Notes (Note 5), Guidance.md (entire document scanned), Specification.md (entire document scanned) | -- | Guidance.md | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Governing Prerequisite | 0 | NO_ITEMS | Prerequisites well-governed |
| X:guiding:sufficiency | guiding | sufficiency | Substantiated Governance | 0 | NO_ITEMS | Governance substantiated |
| X:guiding:completeness | guiding | completeness | Exhaustive Guidance Scope | 1 | HAS_ITEMS | Missing guidance on format/export |
| X:guiding:consistency | guiding | consistency | Systematic Coherence | 0 | NO_ITEMS | Coherence systematic |
| X:applying:necessity | applying | necessity | Verified Enactment | 1 | HAS_ITEMS | No verification for prerequisite completion |
| X:applying:sufficiency | applying | sufficiency | Proven Capability | 0 | NO_ITEMS | Capability demonstration adequate |
| X:applying:completeness | applying | completeness | Comprehensive Delivery | 0 | NO_ITEMS | Delivery scope comprehensive |
| X:applying:consistency | applying | consistency | Reliable Implementation | 0 | NO_ITEMS | Implementation reliable |
| X:judging:necessity | judging | necessity | Grounded Determination | 0 | NO_ITEMS | Determination grounded |
| X:judging:sufficiency | judging | sufficiency | Warranted Judgment | 0 | NO_ITEMS | Judgment warranted |
| X:judging:completeness | judging | completeness | Exhaustive Adjudication | 0 | NO_ITEMS | Adjudication exhaustive |
| X:judging:consistency | judging | consistency | Principled Adjudication | 0 | NO_ITEMS | Adjudication principled |
| X:reviewing:necessity | reviewing | necessity | Validated Oversight | 1 | HAS_ITEMS | Cross-doc verification gap |
| X:reviewing:sufficiency | reviewing | sufficiency | Confirmed Adequacy | 0 | NO_ITEMS | Adequacy confirmed |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Audit Scope | 0 | NO_ITEMS | Audit scope exhaustive |
| X:reviewing:consistency | reviewing | consistency | Regulated Review Standard | 0 | NO_ITEMS | Review standard regulated |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | RationaleGap | Guidance | Guidance | Add guidance on the Schedule B formatting and export process (PDF vs Excel, font size, page layout) -- Procedure Step 7 specifies these details but Guidance provides no rationale for format choices or how formatting affects evaluator perception | Procedure Step 7 contains detailed formatting instructions (minimum 10pt font, PDF export, page numbers) but Guidance does not discuss why formatting matters for evaluator credibility or how format choices support the 35-point evaluation; exhaustive guidance scope should include rationale for submission format decisions | Procedure.md, Guidance.md | Procedure.md#Step 7, Guidance.md (entire document scanned) | -- | Guidance.md | TBD |
| X-002 | X:applying:necessity | VerificationGap | Procedure | Procedure | Add a prerequisite verification gate (or checklist) at the start of Step 3 confirming that all required inputs from the Prerequisites section have been obtained or explicitly flagged as TBD before cost population begins | Procedure lists 9 prerequisite inputs but Step 3 begins population without a formal check that prerequisites are satisfied; the only blocking dependency mentioned is DEL-01-04 (Schedule A); verified enactment requires confirmation that inputs are available before execution starts | Procedure.md | Procedure.md#Prerequisites, Procedure.md#Step 3 | -- | Procedure.md | TBD |
| X-003 | X:reviewing:necessity | VerificationGap | Specification | Specification | Add a verification item (or expand V-04) for cross-checking Schedule B terminology and cost category names against DEL-01-03 (Bonding and Insurance Evidence) -- currently V-04 only references DEL-01-04 and DEL-01-06 | Specification V-04 (Cross-Document Consistency Check) verifies consistency across DEL-01-04, DEL-01-05, and DEL-01-06, but does not include DEL-01-03 despite R-04 requiring CCIP cost consistency with DEL-01-03; validated oversight requires all cross-referenced deliverables to be included in verification scope | Specification.md | Specification.md#V-04, Specification.md#R-04 | -- | Specification.md | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Definitive Mandate | 0 | NO_ITEMS | Mandates definitive |
| E:normative:sufficiency | normative | sufficiency | Substantiated Mandate | 1 | HAS_ITEMS | Datasheet missing document format constraint |
| E:normative:completeness | normative | completeness | Absolute Regulatory Scope | 0 | NO_ITEMS | Regulatory scope absolute |
| E:normative:consistency | normative | consistency | Mandated Rigor | 0 | NO_ITEMS | Rigor mandated consistently |
| E:operative:necessity | operative | necessity | Verified Process Basis | 0 | NO_ITEMS | Process basis verified |
| E:operative:sufficiency | operative | sufficiency | Proven Operational Warrant | 0 | NO_ITEMS | Operational warrant proven |
| E:operative:completeness | operative | completeness | Exhaustive Process Coverage | 0 | NO_ITEMS | Process coverage exhaustive |
| E:operative:consistency | operative | consistency | Systematic Reliability | 0 | NO_ITEMS | Reliability systematic |
| E:evaluative:necessity | evaluative | necessity | Authenticated Merit | 0 | NO_ITEMS | Merit authenticated |
| E:evaluative:sufficiency | evaluative | sufficiency | Substantiated Quality | 1 | HAS_ITEMS | Missing building area attribute |
| E:evaluative:completeness | evaluative | completeness | Exhaustive Merit Scope | 0 | NO_ITEMS | Merit scope exhaustive |
| E:evaluative:consistency | evaluative | consistency | Calibrated Quality Standard | 0 | NO_ITEMS | Quality standard calibrated |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:sufficiency | MissingSlot | Datasheet | Datasheet | Add a Conditions entry or Attribute for the single-PDF submission constraint (15 MB limit per C-01) that applies to the Appendix H package containing Schedule B; Procedure Step 7 references this but Datasheet does not record it | Procedure Step 7 states "All components must be included within the single proposal PDF under 15 MB per C-01" but Datasheet Conditions table does not include this submission format constraint; the substantiated mandate for submission format lacks a factual record in the deliverable's primary data document | Procedure.md, Datasheet.md | Procedure.md#Step 7, Datasheet.md#Conditions | -- | Datasheet.md | TBD |
| E-002 | E:evaluative:sufficiency | VerificationGap | Datasheet | Datasheet | Record the approximate main building gross floor area (19,000-22,000 sq ft per Procedure Step 1 assumption) as a named attribute in Datasheet, as this is needed for the market reasonableness verification (V-04 cost-per-sq-ft calculation) and currently exists only as a procedural assumption | Procedure Step 1 and V-04 both rely on a building area figure (~19,000-22,000 sq ft) for cost-per-sq-ft reasonableness checks, but this essential parameter is not recorded in Datasheet Attributes; substantiated quality requires the key metric basis to be formally documented rather than embedded in procedural assumptions | Procedure.md, Datasheet.md | Procedure.md#Step 1, Procedure.md#V-04, Datasheet.md#Attributes | -- | Datasheet.md | TBD |
