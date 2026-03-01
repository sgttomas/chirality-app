# Semantic Lensing Register: DEL-002-06 Service Pit / Trench Structural Details

**Generated:** 2026-02-26
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-002_Structural Design/1_Working/DEL-002-06_Service-Pit-Details/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-002-06_Service-Pit-Details/_CONTEXT.md
- _STATUS.md — DEL-002-06_Service-Pit-Details/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md — DEL-002-06_Service-Pit-Details/_SEMANTIC.md
- Datasheet.md — DEL-002-06_Service-Pit-Details/Datasheet.md
- Specification.md — DEL-002-06_Service-Pit-Details/Specification.md
- Guidance.md — DEL-002-06_Service-Pit-Details/Guidance.md
- Procedure.md — DEL-002-06_Service-Pit-Details/Procedure.md
- _REFERENCES.md — DEL-002-06_Service-Pit-Details/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the production documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 21
- By document:
  - Datasheet: 5
  - Specification: 9
  - Guidance: 2
  - Procedure: 3
  - Multi: 2
- By matrix:
  - A: 4  B: 3  C: 3  F: 3  D: 3  X: 3  E: 2
- By type:
  - Conflict: 1
  - VerificationGap: 5
  - MissingSlot: 5
  - WeakStatement: 3
  - RationaleGap: 2
  - Normalization: 2
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 1
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4) -- Canonical

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Weak NBC edition statement |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Equipment load as mandatory practice TBD |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | OH&S confined space determination missing |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Regulatory audit provisions adequately covered across docs |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure steps provide adequate procedural direction |
| A:operative:applying | operative | applying | practical execution | 0 | NO_ITEMS | Practical execution steps are clear in Procedure |
| A:operative:judging | operative | judging | performance assessment | 1 | HAS_ITEMS | Missing performance criteria for pit depth |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | QA review step present in Procedure |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Value orientation addressed in Guidance trade-offs |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Merit application consistent across docs |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Worth determination covered via cost/schedule trade-offs |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Quality appraisal covered in Procedure Step 7 |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify NBC edition: confirm "NBC 2019" is the applicable edition and whether Alberta-specific amendments apply, or record as TBD pending confirmation from AHJ | Specification R-006 and Datasheet Conditions both state "NBC 2019" as ASSUMPTION with "location TBD." Prescriptive direction lens reveals this is a governing code citation that remains unconfirmed -- the edition drives structural load requirements. | Specification.md; Datasheet.md | Specification#R-006; Datasheet#Conditions | -- | PROPOSAL: Structural Engineer to confirm applicable NBC edition with AHJ | TBD |
| A-002 | A:normative:applying | TBD_Question | Specification | Specification | Record TBD: Obtain specific equipment load data (axle loads, track footprint, contact pressure) from Owner before finalizing R-002 requirements | Under "mandatory practice" lens, R-002 requires design for heavy equipment loading but the actual load values are TBD. Without this data, the mandatory practice cannot be applied. This is acknowledged in CON-002 in Guidance but not captured as a formal TBD in Specification. | Specification.md; Guidance.md | Specification#R-002; Guidance#CON-002 | -- | PROPOSAL: Owner (Camrose County) is the source | TBD |
| A-003 | A:normative:judging | MissingSlot | Specification | Specification | Add requirement or note addressing whether the service pit qualifies as a "confined space" under Alberta OH&S Code and what compliance determinations follow | Guidance P-4 raises the confined space question but Specification has no corresponding requirement addressing this compliance determination. If the pit is a confined space, additional design requirements apply. | Specification.md; Guidance.md | Specification#Requirements (entire section); Guidance#P-4 | -- | PROPOSAL: Structural Engineer and OH&S consultant | TBD |
| A-004 | A:operative:judging | MissingSlot | Specification | Specification | Add acceptance criteria for minimum pit depth (working clearance) -- currently TBD with no performance threshold stated | Under "performance assessment" lens, pit depth is identified as TBD in Datasheet but no minimum performance criterion is stated in Specification R-003. The Structural Engineer needs a clearance target to assess against. | Specification.md; Datasheet.md | Specification#R-003; Datasheet#Conceptual Dimensions | -- | PROPOSAL: Owner to specify minimum clearance; Structural Engineer to confirm | TBD |

---

## Matrix B -- Conceptualization (4x4) -- Canonical

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Pit depth essential fact missing |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Available evidence (App B dimensions) is acknowledged as conceptual |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Incomplete geotech data record |
| B:data:consistency | data | consistency | reliable measurement | 1 | HAS_ITEMS | Dimension ambiguity (clear vs. overall) |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Essential signals (RFP requirements) captured |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context framing adequate in Guidance |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Documents provide comprehensive account of known information |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Cross-document messaging is coherent |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Fundamental understanding of structural design well-articulated |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | P.Eng. competence requirement clear |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Knowledge coverage appropriate for design-stage documents |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding consistent across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Guidance trade-offs show essential discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Judgment calls adequately framed as requiring human ruling |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view of interfaces and dependencies captured |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Principled reasoning consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | TBD_Question | Datasheet | Datasheet | Record TBD: Pit depth is an essential fact for structural design; source required (Owner equipment clearance requirement + geotech frost depth) | Pit depth is listed as "TBD" in the Datasheet Conceptual Dimensions table. This is the most critical missing essential fact -- structural wall design, excavation scope, waterproofing extent, and cost all depend on it. | Datasheet.md | Datasheet#Conceptual Dimensions | -- | PROPOSAL: Owner (equipment clearance) + Geotech (DEL-008-01) | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add a geotechnical parameters placeholder section or table to Datasheet to receive geotech data when DEL-008-01 is available | The Datasheet lists geotech dependency in a general way but has no structured placeholder for the specific geotechnical parameters (bearing capacity, GWT, frost depth, Ka) that will be essential data inputs. A comprehensive record lens suggests this slot should exist. | Datasheet.md | Datasheet#Geotechnical / Site Conditions | -- | PROPOSAL: Structural Engineer upon receipt of DEL-008-01 | TBD |
| B-003 | B:data:consistency | Conflict | Multi | Multi | Resolve whether "24' x 100'" represents interior clear dimensions or overall dimensions -- Datasheet and Specification both cite the dimension but CON-001 in Guidance identifies ambiguity | Guidance CON-001 identifies this explicitly. Under "reliable measurement" lens, the same dimension pair appears in Datasheet (Conceptual Dimensions table) and Specification (R-003) but its interpretation is uncertain. This is already logged as CON-001 in Guidance, confirming the conflict is known. | Datasheet.md; Specification.md; Guidance.md | Datasheet#Conceptual Dimensions; Specification#R-003; Guidance#CON-001 | Datasheet.md#Conceptual Dimensions ("24 ft width, 100 ft length"); Guidance.md#CON-001 ("unclear whether exterior wall, interior clear, or approximate") | PROPOSAL: Owner/Architect to confirm; treat as interior clear per Guidance CON-001 | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Authoritative Mandate Basis | 1 | HAS_ITEMS | Standards cited as ASSUMPTION |
| C:normative:sufficiency | normative | sufficiency | Certified Justification Standard | 1 | HAS_ITEMS | Justification for standards not confirmed |
| C:normative:completeness | normative | completeness | Full Regulatory Coverage | 0 | NO_ITEMS | Regulatory coverage is comprehensive for identified codes |
| C:normative:consistency | normative | consistency | Harmonized Compliance Regime | 0 | NO_ITEMS | Compliance regime consistently stated across docs |
| C:operative:necessity | operative | necessity | Critical Operational Foundation | 0 | NO_ITEMS | Operational prerequisites well-enumerated in Procedure |
| C:operative:sufficiency | operative | sufficiency | Validated Working Practice | 0 | NO_ITEMS | Working practices described at appropriate level |
| C:operative:completeness | operative | completeness | Comprehensive Process Accounting | 1 | HAS_ITEMS | Independent check procedure underspecified |
| C:operative:consistency | operative | consistency | Calibrated Operational Discipline | 0 | NO_ITEMS | Procedure steps consistently structured |
| C:evaluative:necessity | evaluative | necessity | Intrinsic Value Imperative | 0 | NO_ITEMS | Core value proposition clear (functional pit for equipment servicing) |
| C:evaluative:sufficiency | evaluative | sufficiency | Defensible Worth Judgment | 0 | NO_ITEMS | Trade-offs in Guidance support defensible judgments |
| C:evaluative:completeness | evaluative | completeness | Holistic Value Reckoning | 0 | NO_ITEMS | Value considerations comprehensively covered |
| C:evaluative:consistency | evaluative | consistency | Principled Value Coherence | 0 | NO_ITEMS | Value framing consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Strengthen standards citations: CSA A23.3, CSA S16, NBC 2019 are all stated as ASSUMPTION. Add a note that the Structural Engineer shall confirm applicable editions at project start. | Under "Authoritative Mandate Basis" lens, the normative foundation requires confirmed standards. All three primary standards (NBC 2019, CSA A23.3, CSA S16) are cited as "ASSUMPTION: likely applicable; location TBD." This weakens the authoritative mandate basis for the deliverable. | Specification.md | Specification#R-004; Specification#R-005; Specification#R-006; Specification#Standards | -- | PROPOSAL: Structural Engineer to confirm at project initiation | TBD |
| C-002 | C:normative:sufficiency | VerificationGap | Specification | Specification | Add verification method for confirming which standard editions are applicable -- currently R-004, R-005, R-006 verification methods assume the standard but do not verify the standard selection itself | "Certified Justification Standard" lens reveals the verification methods for R-004/R-005/R-006 check that the standard is cited on drawings, but do not include a step to verify that the correct edition/standard was selected in the first place. | Specification.md | Specification#Verification | -- | PROPOSAL: Structural Engineer of Record | TBD |
| C-003 | C:operative:completeness | VerificationGap | Procedure | Procedure | Clarify the independent check requirement in Step 4: specify who performs the check (second P.Eng. vs. senior engineer), what it covers, and what records it produces | Procedure Step 4 verification states "independent check by a second P.Eng. or senior engineer (ASSUMPTION -- required as standard practice)." Under "Comprehensive Process Accounting," this is underspecified: scope of check, checker qualifications, and output record are not defined. | Procedure.md | Procedure#Step 4 | -- | PROPOSAL: Structural Engineer of Record / Firm QA standard | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Binding Conformance Ground | 0 | NO_ITEMS | Conformance ground adequately established via code references |
| F:normative:sufficiency | normative | sufficiency | Mandated Adequacy Threshold | 1 | HAS_ITEMS | Waterproofing adequacy threshold missing |
| F:normative:completeness | normative | completeness | Exhaustive Regulatory Inventory | 0 | NO_ITEMS | APEGA is listed in Specification Standards table; regulatory inventory complete |
| F:normative:consistency | normative | consistency | Coherent Prescriptive Order | 0 | NO_ITEMS | Prescriptive order consistent |
| F:operative:necessity | operative | necessity | Verified Functional Precondition | 0 | NO_ITEMS | Prerequisites well-defined in Procedure |
| F:operative:sufficiency | operative | sufficiency | Demonstrated Procedural Competence | 0 | NO_ITEMS | Competence requirements stated |
| F:operative:completeness | operative | completeness | Total Operational Inventory | 1 | HAS_ITEMS | Concrete mix design parameters not enumerated |
| F:operative:consistency | operative | consistency | Disciplined Process Alignment | 0 | NO_ITEMS | Process alignment consistent |
| F:evaluative:necessity | evaluative | necessity | Fundamental Merit Grounding | 0 | NO_ITEMS | Merit grounding established via OBJ-001, OBJ-003 |
| F:evaluative:sufficiency | evaluative | sufficiency | Substantiated Merit Verdict | 0 | NO_ITEMS | Merit substantiation adequate |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Merit Accounting | 1 | HAS_ITEMS | Cost impact of geotech unknowns not quantified |
| F:evaluative:consistency | evaluative | consistency | Principled Appraisal Harmony | 0 | NO_ITEMS | Appraisal framing consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add verification criterion for R-009 waterproofing: specify the adequacy threshold (e.g., waterproofing system type selection based on GWT from geotech, or minimum performance standard) | R-009 states waterproofing is "TBD pending geotech" and verification is "drawing review for waterproofing notation." Under "Mandated Adequacy Threshold," the verification only checks notation presence, not that the system is adequate for the actual conditions. | Specification.md | Specification#R-009; Specification#Verification | -- | PROPOSAL: Structural Engineer after geotech receipt | TBD |
| F-002 | F:operative:completeness | MissingSlot | Datasheet | Datasheet | Add concrete material specification parameters to Datasheet (f'c, rebar grade, minimum cover) as TBD placeholders | Procedure Step 6 (6.2) requires general notes with concrete compressive strength (f'c), reinforcement grade, and minimum cover. These are not listed in the Datasheet Structural System Attributes. Under "Total Operational Inventory," these are essential operational parameters missing from the descriptive register. | Datasheet.md; Procedure.md | Datasheet#Structural System Attributes; Procedure#Step 6 | -- | PROPOSAL: Structural Engineer | TBD |
| F-003 | F:evaluative:completeness | RationaleGap | Guidance | Guidance | Add a note on cost/schedule risk quantification for the geotech-dependent design decisions (depth, waterproofing, wall thickness) -- Guidance C-2 mentions "significant cost and schedule risk" but provides no framework for bounding it | Under "Exhaustive Merit Accounting," the cost and schedule impact of geotech unknowns (groundwater, frost depth, bearing capacity) is mentioned qualitatively in Guidance C-2 and C-6 but not quantified or bounded. A risk register entry or bounding estimate would improve merit accounting. | Guidance.md | Guidance#C-2; Guidance#C-6 | -- | PROPOSAL: Structural Engineer / Project Manager | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Established Directive Authority | 0 | NO_ITEMS | Directive authority well-established via RFP citations |
| D:normative:applying | normative | applying | Enforced Adequacy Standard | 1 | HAS_ITEMS | Design life not confirmed as requirement |
| D:normative:judging | normative | judging | Definitive Conformance Ruling | 0 | NO_ITEMS | Conformance ruling mechanisms in place (P.Eng. stamp, AHJ) |
| D:normative:reviewing | normative | reviewing | Resolved Governance Verification | 0 | NO_ITEMS | Governance verification via P.Eng. stamp and inspection records |
| D:operative:guiding | operative | guiding | Confirmed Operational Guidance | 0 | NO_ITEMS | Operational guidance confirmed in Procedure |
| D:operative:applying | operative | applying | Proven Execution Capacity | 0 | NO_ITEMS | Execution capacity well-addressed |
| D:operative:judging | operative | judging | Definitive Performance Determination | 1 | HAS_ITEMS | Cover system load rating not traceable |
| D:operative:reviewing | operative | reviewing | Confirmed Procedural Rigor | 0 | NO_ITEMS | Procedural rigor addressed in Steps 7-8 |
| D:evaluative:guiding | evaluative | guiding | Grounded Worth Direction | 0 | NO_ITEMS | Worth direction grounded in OBJ-001, OBJ-003 |
| D:evaluative:applying | evaluative | applying | Resolved Merit Enactment | 0 | NO_ITEMS | Merit enactment consistent |
| D:evaluative:judging | evaluative | judging | Comprehensive Worth Ruling | 1 | HAS_ITEMS | Cover system cost-benefit not framed |
| D:evaluative:reviewing | evaluative | reviewing | Resolved Quality Examination | 0 | NO_ITEMS | Quality examination mechanisms in place |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | WeakStatement | Datasheet | Specification | Clarify design life requirement: Datasheet states "ASSUMPTION: consistent with 50-year building design life per NBC" but this is not carried into Specification as a requirement | Under "Enforced Adequacy Standard," a 50-year design life assumption appears in the Datasheet Conditions but is not expressed as a requirement in Specification. If the pit design life differs from the building design life, this could affect material durability, waterproofing, and rebar cover decisions. | Datasheet.md; Specification.md | Datasheet#Conditions; Specification#Requirements (entire section) | -- | PROPOSAL: Owner/Structural Engineer to confirm | TBD |
| D-002 | D:operative:judging | VerificationGap | Specification | Specification | Add explicit verification method for cover system load rating: Specification R-002 verification references DEL-002-10 calculation package but does not require the load rating to be marked on the cover system drawing detail | Under "Definitive Performance Determination," the cover system load rating is a key performance parameter. The verification for R-002 checks the calculation package but does not require the rated capacity to appear on the structural drawing itself -- the document that the contractor will use. | Specification.md; Procedure.md | Specification#R-002; Specification#Verification; Procedure#Step 6 (S-[x].6) | -- | PROPOSAL: Structural Engineer | TBD |
| D-003 | D:evaluative:judging | RationaleGap | Guidance | Guidance | Add cost-benefit framing for the cover system options in T-3: the three options (grating, steel plates, hinged covers) are described functionally but without cost or lead-time comparison to support a worth ruling | Under "Comprehensive Worth Ruling," Guidance T-3 presents three cover system options but frames them only in terms of structural characteristics, not cost, availability, or lead time. A comprehensive worth ruling requires these additional dimensions. | Guidance.md | Guidance#T-3 | -- | PROPOSAL: Structural Engineer / Cost Estimator | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Grounded Priority Foundation | 0 | NO_ITEMS | Priority foundation clear (geotech-first, load-first) |
| X:guiding:sufficiency | guiding | sufficiency | Justified Stewardship Frame | 0 | NO_ITEMS | Stewardship framing adequate in Guidance |
| X:guiding:completeness | guiding | completeness | Total Directive Compass | 1 | HAS_ITEMS | Drainage slope direction not addressed |
| X:guiding:consistency | guiding | consistency | Harmonized Directive Alignment | 0 | NO_ITEMS | Directive alignment consistent |
| X:applying:necessity | applying | necessity | Proven Competence Basis | 0 | NO_ITEMS | Competence basis established (P.Eng. requirement) |
| X:applying:sufficiency | applying | sufficiency | Justified Competence Evidence | 0 | NO_ITEMS | Competence evidence mechanisms in place |
| X:applying:completeness | applying | completeness | Complete Competence Record | 0 | NO_ITEMS | Competence records covered in Procedure |
| X:applying:consistency | applying | consistency | Consistent Performance Standard | 0 | NO_ITEMS | Performance standards consistently applied |
| X:judging:necessity | judging | necessity | Decisive Assessment Anchor | 1 | HAS_ITEMS | Geotech-dependent decisions lack fallback assessment criteria |
| X:judging:sufficiency | judging | sufficiency | Substantiated Assessment Finding | 0 | NO_ITEMS | Assessment findings substantiated where data exists |
| X:judging:completeness | judging | completeness | Total Assessment Authority | 0 | NO_ITEMS | Assessment authority comprehensive for available scope |
| X:judging:consistency | judging | consistency | Reliable Assessment Calibration | 0 | NO_ITEMS | Assessment calibration consistent |
| X:reviewing:necessity | reviewing | necessity | Verified Oversight Foundation | 1 | HAS_ITEMS | No hold point for geotech receipt |
| X:reviewing:sufficiency | reviewing | sufficiency | Justified Examination Rigor | 0 | NO_ITEMS | Examination rigor appropriate |
| X:reviewing:completeness | reviewing | completeness | Total Examination Scope | 0 | NO_ITEMS | Examination scope covered by checklist |
| X:reviewing:consistency | reviewing | consistency | Consistent Oversight Calibration | 0 | NO_ITEMS | Oversight calibration consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | MissingSlot | Specification | Specification | Add requirement or note for pit floor drainage slope direction and gradient -- Procedure Step 4.2 mentions drainage slope coordination with PKG-006, but no requirement exists in Specification | Under "Total Directive Compass," pit floor drainage slope is mentioned as an operational step (Procedure 4.2) but has no corresponding directive in Specification. The slope direction and gradient are structural design decisions that should be coordinated and specified. | Specification.md; Procedure.md | Specification#R-009; Procedure#Step 4 (4.2) | -- | PROPOSAL: Structural Engineer + Plumbing Engineer (PKG-006) | TBD |
| X-002 | X:judging:necessity | TBD_Question | Procedure | Procedure | Add decision criteria for proceeding with preliminary design before geotech: Step 3.2 lists assumed parameters but does not state when re-assessment is required or what magnitude of deviation from assumptions triggers redesign | Under "Decisive Assessment Anchor," Procedure Step 3.2 provides assumed geotech parameters for preliminary design, but no threshold or trigger criteria exist to determine when actual geotech data deviates enough from assumptions to require redesign. This is a necessary assessment anchor for the design process. | Procedure.md | Procedure#Step 3 (3.2) | -- | PROPOSAL: Structural Engineer of Record | TBD |
| X-003 | X:reviewing:necessity | VerificationGap | Procedure | Procedure | Add a formal hold point or gate in the Procedure for receipt of DEL-008-01 geotech report before IFC stamp (Step 8) -- currently the dependency is noted but not enforced as a procedural gate | Under "Verified Oversight Foundation," the geotech report (DEL-008-01) is listed as a prerequisite and its absence is managed via assumptions in Step 3. However, there is no formal hold point preventing IFC stamp without either receiving the geotech report or formally documenting the decision to proceed without it. Step 8.3 notes it but as a soft check. | Procedure.md | Procedure#Step 8 (8.3); Procedure#Prerequisites | -- | PROPOSAL: Project Manager / Structural Engineer | TBD |

---

## Matrix E -- Evaluation (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:guiding:data | guiding | data | Substantiated Governance Record | 0 | NO_ITEMS | Governance record substantiated with RFP references |
| E:guiding:information | guiding | information | Integrated Governance Intelligence | 0 | NO_ITEMS | Governance intelligence integrated across docs |
| E:guiding:knowledge | guiding | knowledge | Commanding Governance Expertise | 0 | NO_ITEMS | Governance expertise adequately represented |
| E:guiding:wisdom | guiding | wisdom | Principled Strategic Discernment | 0 | NO_ITEMS | Strategic discernment shown in Guidance principles |
| E:applying:data | applying | data | Verified Performance Record | 1 | HAS_ITEMS | SOW-0012 vs SOW-0028 coverage overlap |
| E:applying:information | applying | information | Contextual Performance Intelligence | 0 | NO_ITEMS | Performance context adequate |
| E:applying:knowledge | applying | knowledge | Validated Technical Mastery | 0 | NO_ITEMS | Technical mastery appropriate for stage |
| E:applying:wisdom | applying | wisdom | Seasoned Craft Judgment | 0 | NO_ITEMS | Craft judgment reflected in trade-offs |
| E:judging:data | judging | data | Substantiated Evidentiary Ruling | 0 | NO_ITEMS | Evidentiary rulings adequately grounded |
| E:judging:information | judging | information | Integrated Adjudication Insight | 0 | NO_ITEMS | Adjudication insight consistent |
| E:judging:knowledge | judging | knowledge | Authoritative Adjudication Mastery | 0 | NO_ITEMS | Adjudication mastery appropriate |
| E:judging:wisdom | judging | wisdom | Principled Adjudication Wisdom | 0 | NO_ITEMS | Adjudication wisdom reflected in conflict table |
| E:reviewing:data | reviewing | data | Verified Inspection Record | 1 | HAS_ITEMS | Inspection records cross-reference incomplete |
| E:reviewing:information | reviewing | information | Integrated Oversight Intelligence | 0 | NO_ITEMS | Oversight intelligence consistent |
| E:reviewing:knowledge | reviewing | knowledge | Commanding Inspection Expertise | 0 | NO_ITEMS | Inspection expertise requirements covered |
| E:reviewing:wisdom | reviewing | wisdom | Principled Oversight Wisdom | 0 | NO_ITEMS | Oversight wisdom reflected in QA provisions |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:applying:data | Normalization | Datasheet | Multi | Normalize SOW references: Datasheet Identification lists "SOW-0028, SOW-0012" under Covers SOW, while _CONTEXT.md mentions only SOW-0012. Clarify which SOW items this deliverable covers and ensure consistency across _CONTEXT.md and Datasheet. | Under "Verified Performance Record," the SOW coverage should be traceable. The Datasheet identifies two SOW items (SOW-0028 for service pit, SOW-0012 for final structural design), while _CONTEXT.md references only SOW-0012. This risks traceability drift. | Datasheet.md; _CONTEXT.md | Datasheet#Identification; _CONTEXT.md#Description | -- | PROPOSAL: Project decomposition owner | TBD |
| E-002 | E:reviewing:data | Normalization | Multi | Multi | Normalize references to the inspection/field-verification deliverable: Specification R-006 references "DEL-009-04" for inspection records, but this deliverable is not mentioned in Datasheet Construction table or Procedure Records table. Add cross-reference. | Under "Verified Inspection Record," Specification R-006 verification method cites DEL-009-04 (inspection records) but this deliverable ID does not appear in the Datasheet Construction section or Procedure Records section, creating an incomplete cross-reference for a reviewer. | Specification.md; Datasheet.md; Procedure.md | Specification#R-006 Verification; Datasheet#Construction; Procedure#Records | -- | PROPOSAL: Project decomposition owner | TBD |

---

*End of Semantic Lensing Register.*
