# Semantic Lensing Register: DEL-01-06 Site Supervision, Logistics & Housekeeping

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/PKG-001_General Requirements & Delivery Controls/1_Working/DEL-01-06_Site Supervision, Logistics & Housekeeping/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-01-06 context (identity, description, scope SOW-0010/0111/0112, OBJ-008)
- _STATUS.md -- Current State: SEMANTIC_READY (2026-02-17)
- _SEMANTIC.md -- Matrices A, B, C, F, D, X, E parsed (7 matrices, 92 cells)
- Datasheet.md -- Present; identification, attributes, conditions, construction, references
- Specification.md -- Present; scope, REQ-01 through REQ-07, standards, verification, documentation
- Guidance.md -- Present; purpose, 5 principles, 5 considerations, 2 trade-offs, 2 examples
- Procedure.md -- Present; Part A (steps A1-A7), Part B (steps B1-B5), verification, records
- _REFERENCES.md -- Present; RFP 2024_004 (sections 7.3, 7.3.1, 7.3.2)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 26
- By document:
  - Datasheet: 2
  - Specification: 13
  - Guidance: 4
  - Procedure: 4
  - Multi: 3
- By matrix:
  - A: 5  B: 4  C: 3  F: 4  D: 3  X: 4  E: 3
- By type:
  - Conflict: 0
  - VerificationGap: 6
  - MissingSlot: 8
  - WeakStatement: 4
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
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | REQ-01 substitution process TBD |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Daily cleaning quality threshold undefined |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | CCDC 14-2013 applicability assumed |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Verification table present and adequate |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Part A/B well-structured |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Subcontractor non-compliance escalation missing |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification checks cover key requirements |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records table covers audit trail |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance provides adequate value framing |
| A:evaluative:applying | evaluative | applying | merit application | 1 | HAS_ITEMS | No criteria for evaluating plan quality |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Trade-offs section adequate |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Covered adequately |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | TBD_Question | Specification | Specification | Record TBD: Define Site Superintendent substitution process (Owner notification vs. approval requirement) | REQ-01 notes substitution process is "TBD pending contract review" -- this is a necessary prescriptive direction that remains unresolved | Specification.md | REQ-01: Site Superintendent -- Continuous Presence | -- | Contract / Owner | TBD |
| A-002 | A:normative:applying | WeakStatement | Specification | Specification | Clarify acceptance threshold for "clean" in daily cleaning obligation (REQ-02) -- what constitutes satisfactory daily cleaning vs. non-conformance? | REQ-02 mandates daily cleaning but provides no objective standard for what constitutes compliance; this could lead to disputes during execution | Specification.md | REQ-02: Daily Site and Building Cleaning | -- | Specification.md (PROPOSAL) | TBD |
| A-003 | A:normative:judging | TBD_Question | Specification | Specification | Confirm applicability of CCDC 14-2013 to site supervision obligations and identify specific relevant clauses | Standards table lists CCDC 14-2013 as "ASSUMPTION: likely applicable; specific clauses not reviewed" -- compliance determination cannot proceed without confirming applicability | Specification.md | Standards | -- | Contract / Owner | TBD |
| A-004 | A:operative:applying | MissingSlot | Multi | Procedure | Add subcontractor housekeeping non-compliance escalation procedure (warning, correction, back-charge) to Procedure Part B | Guidance Consideration 3 identifies subcontractor cleaning enforcement need; Procedure B2 mentions documenting non-conformances but lacks escalation path | Guidance.md, Procedure.md | Consideration 3: Subcontractor Cleaning Obligations; Step B2 | -- | Procedure.md (PROPOSAL) | TBD |
| A-005 | A:evaluative:applying | MissingSlot | Specification | Specification | Add acceptance criteria for evaluating quality of the five plan artifacts (completeness, internal consistency, coordination with referenced deliverables) | No criteria exist for judging whether the produced plans are adequate; Specification Documentation section lists artifacts but not acceptance standards | Specification.md | Documentation | -- | Specification.md (PROPOSAL) | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Laydown area size not quantified |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet attributes adequately sourced |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Missing environmental/weather protection data |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Consistent sourcing across Datasheet |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Road/traffic management signal missing |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context adequate for scope |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Covered across documents |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | PM vs Owner/PM terminology inconsistent |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Core concepts well-established |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | -- |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | -- |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | -- |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Guidance trade-offs adequate |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | -- |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | -- |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | -- |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add essential fact: approximate usable laydown area (in acres or sq ft) available during each major construction phase | Datasheet records "~20-acre parcel" but does not identify how much of that is available for laydown vs. building footprint, roads, and civil work zones -- this is an essential planning datum | Datasheet.md | Attributes; Conditions | -- | Datasheet.md (PROPOSAL) | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add data record for environmental/weather protection requirements for stored materials (temperature-sensitive, moisture-sensitive categories) | Datasheet records storage scope but omits any data on material protection requirements; Procedure A6 mentions "environmental sensitivity" as a storage rationale but no supporting data exists | Datasheet.md, Procedure.md | Attributes; Step A6 | -- | Datasheet.md (PROPOSAL) | TBD |
| B-003 | B:information:necessity | MissingSlot | Specification | Specification | Add requirement or note regarding road use/traffic management for material deliveries if adjacent public roads are affected | Procedure Step A2 identifies road use/traffic management as an assumption but Specification has no corresponding requirement; this is an essential signal for logistics planning | Specification.md, Procedure.md | entire document scanned; Step A2 | -- | Specification.md (PROPOSAL) | TBD |
| B-004 | B:information:consistency | Normalization | Multi | Guidance | Normalize terminology: "PM", "Owner/PM", and "Owner" are used interchangeably as the verification/acceptance authority across documents | Specification Verification uses "Owner/PM"; Procedure uses both "Owner/PM" and "PM" alone; Guidance uses "Owner" -- inconsistent terminology risks confusion about who has acceptance authority | Specification.md, Procedure.md, Guidance.md | Verification; Steps B2, B5; Purpose | -- | Guidance.md (PROPOSAL) | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | compulsory compliance foundation | 1 | HAS_ITEMS | Alberta OHS applicability assumed |
| C:normative:sufficiency | normative | sufficiency | regulatory adequacy standard | 0 | NO_ITEMS | Adequacy standards present via verification table |
| C:normative:completeness | normative | completeness | comprehensive regulatory coverage | 1 | HAS_ITEMS | NMS format applicability unclear |
| C:normative:consistency | normative | consistency | uniform regulatory coherence | 0 | NO_ITEMS | Regulatory references consistent |
| C:operative:necessity | operative | necessity | critical operational baseline | 0 | NO_ITEMS | Prerequisites well-defined |
| C:operative:sufficiency | operative | sufficiency | demonstrated operational readiness | 0 | NO_ITEMS | Procedure demonstrates readiness pathway |
| C:operative:completeness | operative | completeness | exhaustive operational accounting | 0 | NO_ITEMS | Five artifacts cover scope |
| C:operative:consistency | operative | consistency | reliable operational discipline | 0 | NO_ITEMS | Consistent across Procedure steps |
| C:evaluative:necessity | evaluative | necessity | fundamental value discernment | 0 | NO_ITEMS | Guidance values well-articulated |
| C:evaluative:sufficiency | evaluative | sufficiency | qualified merit threshold | 1 | HAS_ITEMS | Insurance/liability for offsite storage unspecified |
| C:evaluative:completeness | evaluative | completeness | comprehensive quality accounting | 0 | NO_ITEMS | -- |
| C:evaluative:consistency | evaluative | consistency | principled value alignment | 0 | NO_ITEMS | -- |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | TBD_Question | Specification | Specification | Confirm Alberta OHS Act and Regulations applicability to this deliverable's cleaning and site security obligations (currently listed as assumption) | Standards table records Alberta OHS as "ASSUMPTION: likely applicable" -- compulsory compliance foundation requires confirmed regulatory basis, not assumption | Specification.md | Standards | -- | Contract / Owner | TBD |
| C-002 | C:normative:completeness | WeakStatement | Specification | Specification | Clarify whether NMS format requirement applies to the five plan artifacts produced under this deliverable | Standards table notes NMS format "may affect format of site plans and cleaning specifications" -- this is too vague to guide plan production | Specification.md | Standards | -- | Specification.md (PROPOSAL) | TBD |
| C-003 | C:evaluative:sufficiency | MissingSlot | Specification | Specification | Add requirement for insurance/liability coverage documentation for offsite-stored materials | Guidance Consideration 5 identifies insurance/liability coverage as a merit threshold for offsite storage; Specification REQ-07 covers offsite storage responsibility but omits insurance requirement; Procedure A6 mentions it as an output but Specification has no matching requirement | Specification.md, Guidance.md, Procedure.md | REQ-07; Consideration 5; Step A6 | -- | Specification.md (PROPOSAL) | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | authoritative compliance imperative | 1 | HAS_ITEMS | Offsite storage cost assumption unresolved |
| F:normative:sufficiency | normative | sufficiency | prescribed conformance benchmark | 1 | HAS_ITEMS | Verification frequency not specified |
| F:normative:completeness | normative | completeness | total prescriptive closure | 0 | NO_ITEMS | Requirements cover RFP scope items |
| F:normative:consistency | normative | consistency | disciplined regulatory uniformity | 0 | NO_ITEMS | REQ sources consistently cited |
| F:operative:necessity | operative | necessity | foundational execution readiness | 1 | HAS_ITEMS | Plan acceptance timing unclear |
| F:operative:sufficiency | operative | sufficiency | competent operational sufficiency | 0 | NO_ITEMS | Procedure steps adequate |
| F:operative:completeness | operative | completeness | total operational command | 0 | NO_ITEMS | Five artifacts + execution steps cover scope |
| F:operative:consistency | operative | consistency | coherent procedural discipline | 0 | NO_ITEMS | -- |
| F:evaluative:necessity | evaluative | necessity | intrinsic quality imperative | 1 | HAS_ITEMS | No quality metrics for site logistics performance |
| F:evaluative:sufficiency | evaluative | sufficiency | substantiated merit adequacy | 0 | NO_ITEMS | -- |
| F:evaluative:completeness | evaluative | completeness | holistic quality completeness | 0 | NO_ITEMS | -- |
| F:evaluative:consistency | evaluative | consistency | principled quality coherence | 0 | NO_ITEMS | -- |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | WeakStatement | Specification | Specification | Strengthen REQ-07 assumption: confirm whether offsite storage costs rest with DB or are subject to contract negotiation | REQ-07 notes "ASSUMPTION: responsibility for offsite storage costs rests with the Design-Builder unless otherwise agreed in contract" -- this is an authoritative compliance imperative that should not rest on an assumption | Specification.md | REQ-07: Offsite Storage | -- | Contract / Owner | TBD |
| F-002 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add verification frequency/sampling rates for daily cleaning checks (e.g., "PM spot inspection minimum weekly") | Verification table lists "PM field inspection at start of each workday" for REQ-02 but also mentions "weekly sample" -- the prescribed conformance benchmark is ambiguous between daily and weekly check frequency | Specification.md | Verification (REQ-02 row) | -- | Specification.md (PROPOSAL) | TBD |
| F-003 | F:operative:necessity | VerificationGap | Procedure | Procedure | Clarify timing requirement: specify that all five plan artifacts must be accepted before or at construction mobilization (currently stated in Prerequisites but not as a verification gate) | Procedure Prerequisites state "All five plan artifacts approved or accepted by Owner/PM prior to or at construction mobilization" but this is not reflected as a formal verification check in the Verification table | Procedure.md | Prerequisites (Part B); Verification | -- | Procedure.md (PROPOSAL) | TBD |
| F-004 | F:evaluative:necessity | MissingSlot | Guidance | Guidance | Add discussion of quality indicators or performance metrics for site logistics effectiveness (e.g., delivery delays, laydown zone utilization, cleaning non-conformance rates) | No document identifies measurable quality indicators for evaluating how well site logistics and housekeeping are performing during construction; only binary pass/fail checks exist | Guidance.md | entire document scanned | -- | Guidance.md (PROPOSAL) | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | definitive compliance authority | 0 | NO_ITEMS | RFP cited as primary authority throughout |
| D:normative:applying | normative | applying | binding conformance practice | 1 | HAS_ITEMS | Laydown coordination with PKG-003 not formalized |
| D:normative:judging | normative | judging | conclusive compliance ruling | 0 | NO_ITEMS | Verification approaches defined |
| D:normative:reviewing | normative | reviewing | systematic compliance assurance | 0 | NO_ITEMS | Records table adequate |
| D:operative:guiding | operative | guiding | established operational stewardship | 0 | NO_ITEMS | Site Superintendent role well-defined |
| D:operative:applying | operative | applying | confirmed execution capability | 0 | NO_ITEMS | Procedure Part B adequate |
| D:operative:judging | operative | judging | definitive performance verdict | 1 | HAS_ITEMS | Final cleaning sign-off criteria lack specificity |
| D:operative:reviewing | operative | reviewing | integrated process assurance | 0 | NO_ITEMS | Cross-check step A7 covers integration |
| D:evaluative:guiding | evaluative | guiding | principled quality stewardship | 0 | NO_ITEMS | Guidance principles adequate |
| D:evaluative:applying | evaluative | applying | demonstrated value realization | 0 | NO_ITEMS | -- |
| D:evaluative:judging | evaluative | judging | conclusive quality determination | 1 | HAS_ITEMS | No criteria for "all foreign materials removed" |
| D:evaluative:reviewing | evaluative | reviewing | assured quality integrity | 0 | NO_ITEMS | -- |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | RationaleGap | Guidance | Guidance | Add rationale for how laydown/staging plan coordination with PKG-003 civil works should be formalized (interface agreement, joint review, or schedule linkage) | Multiple documents reference coordination with PKG-003 but no document explains the mechanism by which this coordination is achieved; Guidance Consideration 2 identifies the interface but not the coordination method | Guidance.md, Specification.md, Procedure.md | Consideration 2; REQ-06; Step A3 | -- | Guidance.md (PROPOSAL) | TBD |
| D-002 | D:operative:judging | VerificationGap | Specification | Specification | Add specific acceptance criteria for final cleaning sign-off beyond the general scope statement (e.g., visual inspection protocol, surface cleanliness standard, or Owner sign-off checklist) | REQ-04 verification says "Owner/PM final inspection sign-off" but does not define what the inspector evaluates beyond the general "all foreign materials removed" language -- this is insufficient for a definitive performance verdict | Specification.md | Verification (REQ-04 row); REQ-04 | -- | Specification.md (PROPOSAL) | TBD |
| D-003 | D:evaluative:judging | WeakStatement | Specification | Specification | Clarify "all other foreign materials" in REQ-04 final cleaning scope -- define what constitutes a foreign material vs. acceptable residual (e.g., construction adhesive residue, minor surface marks) | The phrase "all other foreign materials from inside and outside" is inherited from RFP but is ambiguous enough to create disputes about final cleaning completeness; a conclusive quality determination requires clearer boundaries | Specification.md | REQ-04: Final Cleaning | -- | Specification.md (PROPOSAL) | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | governing foundational imperative | 0 | NO_ITEMS | Foundational imperatives identified |
| X:guiding:sufficiency | guiding | sufficiency | directed adequacy benchmark | 1 | HAS_ITEMS | No benchmark for Superintendent qualifications |
| X:guiding:completeness | guiding | completeness | governed comprehensive scope | 0 | NO_ITEMS | Scope coverage adequate |
| X:guiding:consistency | guiding | consistency | directed systemic harmony | 0 | NO_ITEMS | Cross-deliverable references consistent |
| X:applying:necessity | applying | necessity | enacted foundational requirement | 0 | NO_ITEMS | Requirements enacted via REQ-01 through REQ-07 |
| X:applying:sufficiency | applying | sufficiency | verified adequacy standard | 1 | HAS_ITEMS | Offsite storage verification weak |
| X:applying:completeness | applying | completeness | confirmed comprehensive delivery | 0 | NO_ITEMS | All five artifacts listed |
| X:applying:consistency | applying | consistency | verified implementation coherence | 0 | NO_ITEMS | Procedure cross-checks in Step A7 |
| X:judging:necessity | judging | necessity | essential adjudicative foundation | 0 | NO_ITEMS | Verification table provides adjudicative basis |
| X:judging:sufficiency | judging | sufficiency | conclusive sufficiency judgment | 1 | HAS_ITEMS | Laydown zone verification lacks acceptance threshold |
| X:judging:completeness | judging | completeness | exhaustive adjudicative coverage | 0 | NO_ITEMS | All 7 REQs have verification entries |
| X:judging:consistency | judging | consistency | stable adjudicative coherence | 0 | NO_ITEMS | Verification methods consistent in approach |
| X:reviewing:necessity | reviewing | necessity | foundational assurance validation | 0 | NO_ITEMS | Records retention defined |
| X:reviewing:sufficiency | reviewing | sufficiency | validated sufficiency assurance | 0 | NO_ITEMS | -- |
| X:reviewing:completeness | reviewing | completeness | exhaustive assurance verification | 1 | HAS_ITEMS | Plan revision review timing vague |
| X:reviewing:consistency | reviewing | consistency | sustained assurance coherence | 0 | NO_ITEMS | -- |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | RationaleGap | Guidance | Guidance | Add rationale for what qualifications or experience the Site Superintendent should possess to satisfy "specified" and "qualified" expectations | REQ-01 requires the "specified Site Superintendent" and Datasheet attributes say "on-site, full duration" but no document defines what makes the Superintendent qualified or adequate for the role beyond being named in the proposal | Specification.md, Datasheet.md, Guidance.md | REQ-01; Attributes; entire document scanned | -- | Guidance.md (PROPOSAL) | TBD |
| X-002 | X:applying:sufficiency | VerificationGap | Specification | Specification | Strengthen verification for REQ-07 offsite storage: add requirement for DB to confirm offsite locations are "secured and accessible" with documented evidence (not just DB self-confirmation) | Verification table says "DB confirmation; PM may request site visit" -- this is the weakest verification approach in the table and relies on self-reporting for a risk-bearing obligation | Specification.md | Verification (REQ-07 row) | -- | Specification.md (PROPOSAL) | TBD |
| X-003 | X:judging:sufficiency | VerificationGap | Procedure | Procedure | Add acceptance threshold for laydown zone maintenance verification (e.g., zones marked, materials within designated areas, no encroachment on active work zones) | Procedure Verification table says "Site inspection against Laydown/Staging Plan" weekly, but provides no criteria for what constitutes a passing inspection | Procedure.md | Verification (Laydown zones maintained row) | -- | Procedure.md (PROPOSAL) | TBD |
| X-004 | X:reviewing:completeness | VerificationGap | Procedure | Procedure | Specify timing and trigger for plan artifact revision reviews (currently "at each major construction phase transition" -- define what constitutes a major phase transition) | Procedure Verification table says plan artifacts are reviewed "At each major construction phase transition" but does not define phase transitions; exhaustive assurance verification requires a defined review schedule | Procedure.md | Verification (All plan artifacts current row) | -- | Procedure.md (PROPOSAL) | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | authoritative regulatory foundation | 0 | NO_ITEMS | Regulatory foundations identified (with TBD items captured under A and C) |
| E:normative:sufficiency | normative | sufficiency | binding adequacy certification | 1 | HAS_ITEMS | No formal certification/sign-off for plan package |
| E:normative:completeness | normative | completeness | exhaustive compliance certification | 0 | NO_ITEMS | Scope coverage maps to all RFP sections |
| E:normative:consistency | normative | consistency | enduring regulatory alignment | 0 | NO_ITEMS | Consistent alignment to RFP |
| E:operative:necessity | operative | necessity | verified operational foundation | 0 | NO_ITEMS | Operational foundations defined |
| E:operative:sufficiency | operative | sufficiency | confirmed operational threshold | 0 | NO_ITEMS | Thresholds covered (with gaps captured under F and X) |
| E:operative:completeness | operative | completeness | comprehensive operational certification | 1 | HAS_ITEMS | No closeout certification for logistics/housekeeping scope |
| E:operative:consistency | operative | consistency | sustained operational coherence | 0 | NO_ITEMS | -- |
| E:evaluative:necessity | evaluative | necessity | validated quality foundation | 0 | NO_ITEMS | -- |
| E:evaluative:sufficiency | evaluative | sufficiency | substantiated quality acceptance | 0 | NO_ITEMS | -- |
| E:evaluative:completeness | evaluative | completeness | comprehensive quality realization | 0 | NO_ITEMS | -- |
| E:evaluative:consistency | evaluative | consistency | enduring quality integrity | 1 | HAS_ITEMS | Terminology normalization needed |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:sufficiency | RationaleGap | Guidance | Guidance | Add rationale for plan package acceptance process: who signs off, what constitutes formal acceptance, and whether acceptance is per-artifact or for the package as a whole | Procedure Prerequisites require "All five plan artifacts approved or accepted" but no document explains the acceptance mechanism; binding adequacy certification requires a defined process | Guidance.md, Procedure.md | entire document scanned; Prerequisites (Part B) | -- | Guidance.md (PROPOSAL) | TBD |
| E-002 | E:operative:completeness | MissingSlot | Procedure | Procedure | Add closeout step: confirm all site supervision, logistics, and housekeeping obligations are formally closed out (fencing removed or handed over, laydown areas restored, cleaning records archived) | Procedure ends at Step B5 (final cleaning) but does not address closeout of other logistics/housekeeping obligations (fencing removal, laydown restoration, storage plan closure); comprehensive operational certification requires a final closeout step | Procedure.md | Steps B1-B5 | -- | Procedure.md (PROPOSAL) | TBD |
| E-003 | E:evaluative:consistency | Normalization | Multi | Guidance | Normalize usage of "Design-Builder" vs. "DB" abbreviation across all four documents for enduring terminological consistency | Datasheet uses "Design-Builder (Site Superintendent)"; Specification uses both "Design-Builder" (formal) and does not abbreviate; Guidance and Procedure use "DB" freely as abbreviation -- while not ambiguous, inconsistent abbreviation practice could drift over time | Datasheet.md, Specification.md, Guidance.md, Procedure.md | entire document scanned | -- | Guidance.md (PROPOSAL) | TBD |
