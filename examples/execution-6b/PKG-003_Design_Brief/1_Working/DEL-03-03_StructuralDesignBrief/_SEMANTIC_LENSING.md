# Semantic Lensing Register: DEL-03-03 Structural Design Brief

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/PKG-003_Design_Brief/1_Working/DEL-03-03_StructuralDesignBrief
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — `DEL-03-03_StructuralDesignBrief/_CONTEXT.md` (DEL-03-03, PKG-003, SOW-0011/SOW-0014, OBJ-004)
- _STATUS.md — `DEL-03-03_StructuralDesignBrief/_STATUS.md` (Current State: SEMANTIC_READY)
- _SEMANTIC.md — `DEL-03-03_StructuralDesignBrief/_SEMANTIC.md` (Matrices A, B, C, F, D, X, E parsed; 92 cells total)
- Datasheet.md — `DEL-03-03_StructuralDesignBrief/Datasheet.md` (Identification, Attributes, Conditions, Construction, References)
- Specification.md — `DEL-03-03_StructuralDesignBrief/Specification.md` (Scope, Requirements R-STR-01 through R-STR-13, Standards, Verification, Documentation)
- Guidance.md — `DEL-03-03_StructuralDesignBrief/Guidance.md` (Purpose, Principles P-001 through P-007, Considerations C-001 through C-007, Trade-offs T-001 through T-004, Examples)
- Procedure.md — `DEL-03-03_StructuralDesignBrief/Procedure.md` (Steps 1-7, Prerequisites, Verification Summary V-01 through V-07, Records, Notes/Pitfalls)
- _REFERENCES.md — `DEL-03-03_StructuralDesignBrief/_REFERENCES.md` (Package references, source documents, cross-references to DEL-02-03 and DEL-03-06)

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 18
- By document:
  - Datasheet: 3
  - Specification: 7
  - Guidance: 3
  - Procedure: 3
  - Multi: 2
- By matrix:
  - A: 3  B: 2  C: 2  F: 3  D: 2  X: 4  E: 2
- By type:
  - Conflict: 0
  - VerificationGap: 5
  - MissingSlot: 5
  - WeakStatement: 3
  - RationaleGap: 2
  - Normalization: 2
  - TBD_Question: 1
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Concrete apron design load not prescribed |
| A:normative:applying | normative | applying | mandatory practice | 0 | NO_ITEMS | Mandatory practices (sulphate class, air entrainment, single-system rule) well covered across all 4 docs |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Post-disaster importance exemption has no verification path |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit context covered by Verification table and Procedure V-01 through V-07 |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Steps 1-7 provide clear procedural direction |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Cold Storage floor system execution ambiguity |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification summary and requirement-level checks present |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Procedure V-01 through V-07 provide process audit checkpoints |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance P-001, P-005, T-001 establish value orientation for cost/flexibility/durability |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | OBJ-004 scoring alignment addressed in Guidance Purpose section |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Trade-offs T-001 through T-004 ground worth determination |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Procedure Step 7 final review provides quality appraisal checkpoint |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Datasheet | Specification | Clarify concrete apron design load basis -- Datasheet states "designed to support weight and operation of service vehicles" but no load class or axle load reference is given; Specification R-STR-10 does not include apron load criteria | The phrase "weight and operation of service vehicles" is vague enough that two engineers could produce materially different apron thicknesses; a proposal-stage commitment to a load class (e.g., AASHTO HS-20 or specific axle load) would strengthen credibility | Datasheet.md; Specification.md | Datasheet.md#Conditions "Concrete Aprons"; Specification.md#Requirements R-STR-10 | -- | Structural Engineer | TBD |
| A-002 | A:normative:judging | MissingSlot | Specification | Specification | Add verification approach for the post-disaster importance exemption claim -- Datasheet states "AHJ intends to exempt the PSB" but there is no requirement or verification entry confirming this exemption is documented or obtained | If the exemption is not confirmed, the entire lateral design basis could change; currently no requirement captures this dependency | Datasheet.md; Specification.md | Datasheet.md#Attributes "Post-Disaster Importance"; Specification.md#Verification (entire table scanned -- no entry for exemption) | -- | AHJ / Structural Engineer | TBD |
| A-003 | A:operative:applying | WeakStatement | Datasheet | Guidance | Clarify Cold Storage floor system options -- Datasheet lists "Cold Storage also gets 16' x 16' doors" and OSR §10.3.8 is cited for flooring but the Datasheet Conditions do not explicitly state whether the Cold Storage floor is slab-on-grade, gravel, or other; Procedure Step 2 references "OSR §10.3.8 Option 2" without defining the options | An author could misinterpret what floor system to propose for Cold Storage; Guidance C-002 partially addresses this but without linking to the floor treatment | Datasheet.md; Procedure.md | Datasheet.md#Conditions "Overhead Door Requirement"; Procedure.md#Step 2 "Cold Storage Building" | -- | Structural Engineer | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Ground snow load value missing |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Geotechnical evidence is thoroughly cited with specific values |
| B:data:completeness | data | completeness | comprehensive record | 0 | NO_ITEMS | Data record across Datasheet Conditions table is comprehensive |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Measurement values (kPa, m, mm, %) consistent across docs |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (clay unsuitable, till viable, frost depth) present in all docs |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Guidance Considerations C-001 through C-007 provide adequate context |
| B:information:completeness | information | completeness | comprehensive account | 1 | HAS_ITEMS | Wind load reference data absent |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Cross-document messaging on geotech constraints is coherent |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Guidance P-002, P-003, P-006 demonstrate fundamental understanding of geotech constraints |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | PE authorship requirement (R-STR-13) ensures competent expertise |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Deep coverage of USG1123 across all docs demonstrates mastery of site conditions |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | No contradictions in knowledge representation across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs T-001 through T-004 and Principles P-001, P-005 capture discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Multiple trade-off analyses (T-001 through T-004) provide adequate judgment basis |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Cross-deliverable coordination noted (DEL-02-03, DEL-03-06, DEL-04-02) |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and grounded in source data throughout |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Multi | Datasheet | Record TBD: NBCC ground snow load (Ss) and rain-on-snow (Sr) values for Penhold, Alberta -- these are essential inputs for R-STR-07 load path narrative but are not stated in any document; Procedure Step 3 marks them as "location TBD" | Snow load is a primary gravity design input; without the specific NBCC Appendix C value, the load path narrative cannot be verified as site-specific | Datasheet.md; Specification.md; Procedure.md | Datasheet.md#Conditions (entire table scanned -- no snow load entry); Specification.md#Requirements R-STR-07; Procedure.md#Step 3 "Gravity loads" | -- | Structural Engineer / NBCC Appendix C | TBD |
| B-002 | B:information:completeness | MissingSlot | Datasheet | Datasheet | Add NBCC reference wind pressure (q) for Penhold to Conditions table -- Procedure Step 3 references "NBCC reference wind pressure for Penhold (TBD)" and R-STR-07 requires lateral load narrative, but no wind pressure data appears in Datasheet | Wind is cited as likely governing lateral case (Guidance C-007); the absence of a specific reference pressure is a data gap for the load path section | Datasheet.md; Procedure.md | Datasheet.md#Conditions (entire table scanned); Procedure.md#Step 3 "Lateral loads" | -- | Structural Engineer / NBCC Appendix C | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | regulatory imperative | 0 | NO_ITEMS | Regulatory imperatives (ABC, NBCC, CAN/CSA A23.1) well covered in Specification Standards table |
| C:normative:sufficiency | normative | sufficiency | compliance substantiation | 1 | HAS_ITEMS | Sulphate testing gap not captured as a requirement |
| C:normative:completeness | normative | completeness | exhaustive regulatory coverage | 0 | NO_ITEMS | Standards table in Specification covers all cited regulatory instruments |
| C:normative:consistency | normative | consistency | regulatory coherence | 0 | NO_ITEMS | No regulatory conflicts identified |
| C:operative:necessity | operative | necessity | operational threshold | 0 | NO_ITEMS | Operational thresholds (frost depth, pile length, void) are specific and present |
| C:operative:sufficiency | operative | sufficiency | procedural adequacy | 0 | NO_ITEMS | Procedure Steps 1-7 are adequate for brief production |
| C:operative:completeness | operative | completeness | comprehensive execution | 1 | HAS_ITEMS | Eave height range stated as assumption but not captured in Specification |
| C:operative:consistency | operative | consistency | operational reliability | 0 | NO_ITEMS | Operational parameters consistent across docs |
| C:evaluative:necessity | evaluative | necessity | intrinsic merit | 0 | NO_ITEMS | Merit basis grounded in OBJ-004 scoring |
| C:evaluative:sufficiency | evaluative | sufficiency | justified valuation | 0 | NO_ITEMS | Valuation justified through trade-off analysis |
| C:evaluative:completeness | evaluative | completeness | holistic value assessment | 0 | NO_ITEMS | All value dimensions (cost, flexibility, durability, expansion) addressed |
| C:evaluative:consistency | evaluative | consistency | principled merit alignment | 0 | NO_ITEMS | Merit criteria aligned with RFP evaluation framework |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:sufficiency | RationaleGap | Guidance | Guidance | Add rationale note explaining that sulphate testing was not performed and Class S-2 is applied as a conservative precaution -- Guidance P-006 states this in passing but the rationale for applying the most severe class without test data should be more explicit for the evaluation committee | A reviewer might question why S-2 is specified without sulphate concentration data; making the conservative-precaution rationale explicit strengthens the brief's credibility | Guidance.md | Guidance.md#Principles P-006 | -- | Structural Engineer | TBD |
| C-002 | C:operative:completeness | MissingSlot | Specification | Specification | Add requirement or acceptance note for minimum eave height range -- R-STR-09 addresses door height and equipment clearance but does not state a minimum eave height; Guidance C-005 and Procedure Step 2 both reference "24-28 ft" as an assumption but this is not captured as a requirement or bounded parameter | Eave height directly governs structural frame cost and steel quantity; without a stated minimum, the requirement is incomplete for verification | Specification.md; Guidance.md; Procedure.md | Specification.md#Requirements R-STR-09; Guidance.md#Considerations C-005; Procedure.md#Step 2 | -- | Structural Engineer | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | obligatory compliance mastery | 0 | NO_ITEMS | Compliance mastery demonstrated through detailed USG1123 integration |
| F:normative:sufficiency | normative | sufficiency | statutory substantiation | 1 | HAS_ITEMS | Geotechnical report limitations acknowledgement weak in Specification |
| F:normative:completeness | normative | completeness | total regulatory accounting | 0 | NO_ITEMS | All regulatory instruments accounted for in Standards table |
| F:normative:consistency | normative | consistency | harmonized compliance standard | 0 | NO_ITEMS | Standards citations consistent across docs |
| F:operative:necessity | operative | necessity | operational precondition | 1 | HAS_ITEMS | Missing prerequisite for equipment clearance data |
| F:operative:sufficiency | operative | sufficiency | demonstrated competence | 0 | NO_ITEMS | Competence demonstrated through detailed geotech integration and PE authorship |
| F:operative:completeness | operative | completeness | total process assurance | 0 | NO_ITEMS | Process steps comprehensive |
| F:operative:consistency | operative | consistency | systematic process reliability | 0 | NO_ITEMS | Process steps internally consistent |
| F:evaluative:necessity | evaluative | necessity | foundational value discernment | 0 | NO_ITEMS | Value discernment grounded in RFP evaluation criteria |
| F:evaluative:sufficiency | evaluative | sufficiency | substantiated merit appraisal | 0 | NO_ITEMS | Merit substantiated through trade-offs and examples |
| F:evaluative:completeness | evaluative | completeness | exhaustive quality accounting | 1 | HAS_ITEMS | OBJ-005 contribution not structured as trackable |
| F:evaluative:consistency | evaluative | consistency | congruent value discipline | 0 | NO_ITEMS | Value discipline consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add verification check that the brief acknowledges USG1123 limitations (report prepared for Tagish Engineering, not Design-Builder; subsurface conditions may vary) -- R-STR-13 mentions geotechnical services responsibility but does not require the limitations acknowledgement; Guidance P-007 requires it but no corresponding verification entry exists | Without a verification check, the limitations acknowledgement could be omitted from the brief, creating a professional liability gap; Guidance P-007 specifically requires this but it has no matching Specification requirement or verification | Specification.md; Guidance.md | Specification.md#Requirements R-STR-13; Specification.md#Verification R-STR-13; Guidance.md#Principles P-007 | -- | Structural Engineer | TBD |
| F-002 | F:operative:necessity | MissingSlot | Procedure | Procedure | Add prerequisite for confirmed equipment clearance dimensions (dump truck raised box height, grader height, Type 1 apparatus + ladder height) -- Procedure P-PRE-05 requires bay count and footprint from DEL-03-01 but does not require confirmed equipment heights, which are essential for eave height determination (R-STR-09) | Without confirmed equipment dimensions, the eave height assumption (24-28 ft) cannot be validated; this is a necessary input that should be listed as a prerequisite | Procedure.md; Specification.md | Procedure.md#Prerequisites P-PRE-05; Specification.md#Requirements R-STR-09 | -- | Structural Engineer / Owner (equipment list) | TBD |
| F-003 | F:evaluative:completeness | VerificationGap | Specification | Specification | Add explicit traceability from Specification to OBJ-005 (Durability, 15 pts) contribution -- Datasheet Attributes states "supporting evidence for OBJ-005" and Guidance Purpose mentions OBJ-005 but no requirement in Specification tracks what structural content contributes to OBJ-005 scoring | OBJ-005 is worth 15 points (3x the weight of OBJ-004); if the brief's contribution to OBJ-005 is not tracked, the proposal team cannot verify that durability-relevant structural content is included | Datasheet.md; Specification.md; Guidance.md | Datasheet.md#Identification "Supporting Objectives"; Specification.md#Requirements (entire table scanned); Guidance.md#Purpose | -- | Lead Architect / Proposal Manager | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | definitive regulatory mandate | 0 | NO_ITEMS | Regulatory mandates clearly defined |
| D:normative:applying | normative | applying | binding compliance practice | 0 | NO_ITEMS | Compliance practices binding through R-STR-05, R-STR-06 |
| D:normative:judging | normative | judging | conclusive conformance ruling | 0 | NO_ITEMS | Conformance ruling possible through verification table |
| D:normative:reviewing | normative | reviewing | established oversight standard | 0 | NO_ITEMS | Oversight established through multi-party verification (SE self-check, Lead Architect, Proposal Manager) |
| D:operative:guiding | operative | guiding | grounded procedural direction | 0 | NO_ITEMS | Procedure grounded in geotech report and RFP |
| D:operative:applying | operative | applying | validated operational delivery | 1 | HAS_ITEMS | Coordination timing not specified |
| D:operative:judging | operative | judging | confirmed performance verdict | 0 | NO_ITEMS | Performance verdict achievable through V-01 through V-07 |
| D:operative:reviewing | operative | reviewing | assured process integrity | 0 | NO_ITEMS | Process integrity maintained through 7-step procedure |
| D:evaluative:guiding | evaluative | guiding | resolved merit orientation | 0 | NO_ITEMS | Merit orientation resolved toward OBJ-004 |
| D:evaluative:applying | evaluative | applying | confirmed merit deployment | 0 | NO_ITEMS | Merit deployed through examples EX-001, EX-003 |
| D:evaluative:judging | evaluative | judging | definitive quality ruling | 1 | HAS_ITEMS | No quality gate for brief persuasiveness |
| D:evaluative:reviewing | evaluative | reviewing | assured quality coherence | 0 | NO_ITEMS | Quality coherence addressed through cross-reference sign-off |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:operative:applying | VerificationGap | Procedure | Procedure | Add timing or sequencing constraint for DEL-02-02 and DEL-02-03 coordination -- Procedure P-PRE-03 and P-PRE-04 require these deliverables to be "drafted or substantially in progress" but no check confirms when coordination actually occurs before the brief is finalized; Step 6 describes coordination but has no timing gate | If DEL-02-02 (site plan) or DEL-02-03 (concept narrative) are not available when the Structural Engineer begins Step 2, the system selection and expansion direction could be based on assumptions that are later contradicted | Procedure.md | Procedure.md#Prerequisites P-PRE-03, P-PRE-04; Procedure.md#Step 6 | -- | Lead Architect | TBD |
| D-002 | D:evaluative:judging | RationaleGap | Guidance | Guidance | Add guidance on how to self-assess whether the brief's rationale is persuasive to a non-structural audience -- Guidance Purpose notes the audience includes "municipal stakeholders with varying levels of structural knowledge" but no principle or consideration addresses how to calibrate technical depth for a mixed evaluation panel | The brief is scored by an evaluation committee, not by structural engineers; without guidance on audience calibration, the author may produce a technically complete but unpersuasive document | Guidance.md | Guidance.md#Purpose | -- | Lead Architect / Proposal Manager | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | authoritative baseline mandate | 0 | NO_ITEMS | Baseline mandates established through NBCC, ABC, CAN/CSA |
| X:guiding:sufficiency | guiding | sufficiency | prescribed validation standard | 1 | HAS_ITEMS | Validation standard for Addendum 03 compliance incomplete |
| X:guiding:completeness | guiding | completeness | comprehensive directive scope | 0 | NO_ITEMS | Directive scope comprehensive across all docs |
| X:guiding:consistency | guiding | consistency | coherent governance standard | 0 | NO_ITEMS | Governance standards coherent |
| X:applying:necessity | applying | necessity | mandatory capability threshold | 0 | NO_ITEMS | Capability thresholds defined (PE registration, geotech services) |
| X:applying:sufficiency | applying | sufficiency | demonstrated execution adequacy | 0 | NO_ITEMS | Execution adequacy demonstrated through detailed procedure |
| X:applying:completeness | applying | completeness | exhaustive implementation scope | 1 | HAS_ITEMS | Cold Storage detailed design items missing from scope |
| X:applying:consistency | applying | consistency | reliable implementation standard | 0 | NO_ITEMS | Implementation standards consistent |
| X:judging:necessity | judging | necessity | essential adjudicative finding | 0 | NO_ITEMS | Adjudicative findings possible through verification table |
| X:judging:sufficiency | judging | sufficiency | warranted adjudicative proof | 1 | HAS_ITEMS | Verification relies entirely on narrative review |
| X:judging:completeness | judging | completeness | comprehensive adjudicative review | 0 | NO_ITEMS | Adjudicative review scope covers all 13 requirements |
| X:judging:consistency | judging | consistency | consistent adjudicative standard | 0 | NO_ITEMS | All verifications use same "narrative review" method consistently |
| X:reviewing:necessity | reviewing | necessity | mandatory audit baseline | 0 | NO_ITEMS | Audit baseline established through verification summary |
| X:reviewing:sufficiency | reviewing | sufficiency | adequate audit substantiation | 0 | NO_ITEMS | Audit substantiation adequate through V-01 to V-07 |
| X:reviewing:completeness | reviewing | completeness | exhaustive audit coverage | 1 | HAS_ITEMS | Terminology consistency check limited to Procedure Step 7 |
| X:reviewing:consistency | reviewing | consistency | standardized audit protocol | 0 | NO_ITEMS | Audit protocol standardized across verification entries |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:sufficiency | VerificationGap | Specification | Specification | Add explicit verification entry for Addendum 03 compliance as a whole -- Procedure Step 5 includes an "Addendum 03 compliance checklist" but no Specification requirement or verification entry validates that checklist against the full set of Addendum 03 structural items | Addendum 03 items (sumps, doors, solar) are distributed across multiple requirements (R-STR-08, R-STR-09, R-STR-10) but there is no single verification check confirming complete Addendum 03 coverage; Procedure embeds a checklist but Specification does not require it | Specification.md; Procedure.md | Specification.md#Verification (entire table); Procedure.md#Step 5 "Addendum 03 compliance checklist" | -- | Lead Architect | TBD |
| X-002 | X:applying:completeness | MissingSlot | Specification | Specification | Add scope inclusion or requirement for Cold Storage slab/floor system selection rationale -- Specification Scope Inclusions mention "Slab-on-grade design rationale for apparatus bays and workshop bays" but do not explicitly include the Cold Storage floor treatment; R-STR-02 covers Cold Storage framing and foundation but not its floor system | Cold Storage floor could be gravel, concrete slab, or other (OSR §10.3.8 provides options); without explicit scope coverage, this decision may be omitted from the brief | Specification.md; Datasheet.md | Specification.md#Scope Inclusions; Specification.md#Requirements R-STR-02; Datasheet.md#Conditions "Overhead Door Requirement" | -- | Structural Engineer | TBD |
| X-003 | X:judging:sufficiency | WeakStatement | Specification | Procedure | Strengthen verification method beyond "narrative review" for R-STR-07 load path -- all 13 requirements use "narrative review" as verification method, which is appropriate for a proposal-stage brief, but R-STR-07 (load path) involves technical claims about three load categories that could benefit from a cross-check against NBCC load tables | "Narrative review" for load path could mean anything from confirming the section exists to verifying load values are reasonable; for R-STR-07, a more specific check (e.g., "confirm cited load categories match NBCC for Penhold climatic data") would improve adjudicative rigor | Specification.md | Specification.md#Verification R-STR-07 | -- | Structural Engineer | TBD |
| X-004 | X:reviewing:completeness | Normalization | Procedure | Multi | Standardize building naming terminology -- Procedure Step 7 item 2 flags this ("Main Building" not "PSB" or "main structure") but no cross-document glossary or normalization table exists; Datasheet uses "Main Building" and "Cold Storage Building" consistently but Guidance C-002 uses "Cold Storage" without "Building" in places | Inconsistent building names across the final brief and proposal documents could confuse evaluators or create ambiguity about which structure is being discussed | Procedure.md; Guidance.md | Procedure.md#Step 7 item 2; Guidance.md#Considerations C-002 | -- | Lead Architect | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | absolute compliance obligation | 0 | NO_ITEMS | Compliance obligations clearly established |
| E:normative:sufficiency | normative | sufficiency | conclusive compliance evidence | 0 | NO_ITEMS | Compliance evidence pathway clear through verification table |
| E:normative:completeness | normative | completeness | exhaustive compliance scope | 0 | NO_ITEMS | Compliance scope exhaustive across 13 requirements |
| E:normative:consistency | normative | consistency | harmonized regulatory protocol | 0 | NO_ITEMS | Regulatory protocols harmonized across docs |
| E:operative:necessity | operative | necessity | validated operational imperative | 0 | NO_ITEMS | Operational imperatives validated through geotech integration |
| E:operative:sufficiency | operative | sufficiency | substantiated operational fitness | 1 | HAS_ITEMS | Slab live load assumption not substantiated |
| E:operative:completeness | operative | completeness | comprehensive operational scope | 0 | NO_ITEMS | Operational scope comprehensive |
| E:operative:consistency | operative | consistency | harmonized operational protocol | 0 | NO_ITEMS | Operational protocols consistent |
| E:evaluative:necessity | evaluative | necessity | fundamental quality obligation | 0 | NO_ITEMS | Quality obligations established through PE authorship and verification |
| E:evaluative:sufficiency | evaluative | sufficiency | substantiated quality evidence | 0 | NO_ITEMS | Quality evidence substantiated through examples and trade-offs |
| E:evaluative:completeness | evaluative | completeness | exhaustive quality fulfillment | 1 | HAS_ITEMS | No guidance on brief length or depth calibration |
| E:evaluative:consistency | evaluative | consistency | principled quality standard | 0 | NO_ITEMS | Quality standards principled and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:operative:sufficiency | VerificationGap | Procedure | Specification | Add verification that slab live load assumption (300-500 psf stated in Procedure Step 3) has a defensible basis -- this value appears only as an assumption with no source citation and no verification check; if stated in the brief, the evaluation committee may question it | The 300-500 psf range is a significant structural parameter that drives slab thickness and reinforcement; stating it without a cited basis (e.g., specific vehicle axle loads, manufacturer data, or industry standard) weakens the brief's credibility | Procedure.md; Specification.md | Procedure.md#Step 3 "Floor/slab live loads"; Specification.md#Verification R-STR-07 | -- | Structural Engineer | TBD |
| E-002 | E:evaluative:completeness | Normalization | Guidance | Guidance | Add guidance on expected brief length, depth, or page count -- Guidance states the brief is a "proposal-stage communication tool, not an engineering calculation package" but provides no indication of expected length or level of detail; for a 5-point evaluation criterion, calibrating the depth of treatment is important | Without length guidance, the author could produce either a single page or a 20-page document; for proposal preparation, approximate scope (e.g., "6-10 pages" or "2,000-3,000 words") helps calibrate effort and ensures the brief is neither superficial nor excessive | Guidance.md | Guidance.md#Purpose | -- | Lead Architect / Proposal Manager | TBD |
