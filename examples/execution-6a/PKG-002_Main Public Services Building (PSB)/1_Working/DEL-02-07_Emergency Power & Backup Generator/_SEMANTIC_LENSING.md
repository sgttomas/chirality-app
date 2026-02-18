# Semantic Lensing Register: DEL-02-07 Emergency Power & Backup Generator

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/PKG-002_Main Public Services Building (PSB)/1_Working/DEL-02-07_Emergency Power & Backup Generator/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md — DEL-02-07_Emergency Power & Backup Generator/_CONTEXT.md
- _STATUS.md — DEL-02-07_Emergency Power & Backup Generator/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md — DEL-02-07_Emergency Power & Backup Generator/_SEMANTIC.md
- Datasheet.md — DEL-02-07_Emergency Power & Backup Generator/Datasheet.md
- Specification.md — DEL-02-07_Emergency Power & Backup Generator/Specification.md
- Guidance.md — DEL-02-07_Emergency Power & Backup Generator/Guidance.md
- Procedure.md — DEL-02-07_Emergency Power & Backup Generator/Procedure.md
- _REFERENCES.md — DEL-02-07_Emergency Power & Backup Generator/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 28
- By document:
  - Datasheet: 5
  - Specification: 10
  - Guidance: 4
  - Procedure: 4
  - Multi: 5
- By matrix:
  - A: 5  B: 5  C: 4  F: 4  D: 3  X: 4  E: 3
- By type:
  - Conflict: 0
  - VerificationGap: 7
  - MissingSlot: 8
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 3
  - MatrixError: 0
- Notable conflicts: 0 (existing conflicts already captured in Guidance Conflict Table; no new cross-document conflicts found)
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | REQ-06 ATS sourced from ASSUMPTION only |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Generator spare capacity factor unspecified |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | CSA C282 applicability unconfirmed |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Verification table covers audit approach adequately |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure provides clear phased steps |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Load bank test duration unspecified |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification table in both Spec and Procedure covers this |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Records table adequate |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Principles section well-developed |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs section in Guidance covers merit assessment |
| A:evaluative:judging | evaluative | judging | worth determination | 1 | HAS_ITEMS | No acceptance criteria for cost-value tradeoff on essential loads scope |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Covered by existing verification approaches |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Strengthen REQ-06 source from ASSUMPTION to explicit code or standard reference for ATS requirement | REQ-06 ATS is sourced entirely from ASSUMPTION; no accessible normative source cited. For a prescriptive requirement this weakens enforceability. | Specification.md | REQ-06: ATS and Distribution | -- | CSA C282 or CEC if they mandate ATS for standby systems | TBD |
| A-002 | A:normative:applying | TBD_Question | Specification | Specification | Record TBD: Confirm spare capacity factor for generator sizing (25% stated as ASSUMPTION in Guidance; not specified in any accessible normative source) | The 25% spare capacity factor in Guidance Examples section and Procedure Step A4 is stated as ASSUMPTION. No normative source confirms it. This directly affects generator kW selection. | Guidance.md; Procedure.md | Guidance#Examples; Procedure#Step A4 | -- | Responsible electrical engineer / CSA C282 | TBD |
| A-003 | A:normative:judging | TBD_Question | Multi | Specification | Record TBD: Confirm CSA C282 applicability -- standard is listed as "ASSUMPTION: likely applicable" but has not been accessed or verified | CSA C282 is referenced as a governing standard in Specification REQ-08 and Standards table but its applicability is explicitly flagged as assumed. Compliance determination cannot proceed without confirming it applies. | Specification.md; Datasheet.md | Specification#REQ-08; Specification#Standards; Datasheet#References | -- | Design-Builder electrical engineer to confirm with AHJ | TBD |
| A-004 | A:operative:applying | WeakStatement | Procedure | Procedure | Specify load bank test minimum duration in Step C2 (currently "duration TBD" with ASSUMPTION of 2 hours) | Practical execution of commissioning requires a known test duration. The current wording defers to CSA C282 whose text has not been accessed. | Procedure.md | Step C2 -- Generator Load Bank Test | -- | CSA C282 or NFPA 110 | TBD |
| A-005 | A:evaluative:judging | MissingSlot | Specification | Guidance | Add rationale or acceptance criteria for how the essential loads list scope (minimum vs. full emergency operations) should be evaluated for adequacy | Worth determination for the essential loads scope trade-off (Trade-off 2 in Guidance) lacks any evaluative criteria in the Specification. How does one judge whether the essential loads list is sufficient vs. over-scoped? | Specification.md | REQ-02: Minimum Essential Loads | -- | Owner / Design-Builder | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Generator kW output is TBD |
| B:data:sufficiency | data | sufficiency | adequate evidence | 1 | HAS_ITEMS | Fuel consumption rate unknown |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Additional essential loads TBD |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Stated values (door sizes, fuel type) are consistent across docs |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | Altitude derating data missing |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for the deliverable is well-established |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Scope description is complete |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology inconsistency for door mechanism |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Design basis logic is well-documented |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Required personnel and roles specified |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Coverage across phases is comprehensive |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is consistent across docs |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs in Guidance show discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Design-Builder decision authority is clear |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Lifecycle coverage through Phase D adequate |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add placeholder row for generator output (kW) with explicit dependency on essential loads calculation completion | Generator output kW is listed as TBD in Datasheet but no dependency chain or timeline for resolution is recorded. This is the single most essential fact for this deliverable. | Datasheet.md | Attributes > Generator Unit | -- | Design-Builder electrical engineer | TBD |
| B-002 | B:data:sufficiency | MissingSlot | Datasheet | Datasheet | Add fuel consumption rate basis (L/hr at design load) as a required data field once generator model is selected | Fuel tank sizing (Step A5) depends on fuel consumption rate, which requires manufacturer data. No placeholder exists in Datasheet for this essential evidence. | Datasheet.md | Attributes > Generator Unit | -- | Generator manufacturer data | TBD |
| B-003 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add rows for anticipated additional essential loads (fire alarm, communications, SCBA room, PA system) with TBD demand values | Datasheet Essential Loads table lists "Additional essential loads" as a single TBD row. Breaking this into known candidate loads (mentioned in Specification REQ-02 Notes and Guidance P1) would improve completeness of the data record. | Datasheet.md | Attributes > Essential Loads (Minimum Required) | -- | Design-Builder electrical engineer | TBD |
| B-004 | B:information:necessity | MissingSlot | Datasheet | Datasheet | Add Penhold altitude and design temperature data relevant to generator derating | Procedure Step B1 notes altitude derating may apply but no altitude or design temperature data is recorded in any document. This is an essential signal for final generator sizing. | Datasheet.md; Procedure.md | Datasheet#Conditions; Procedure#Step B1 | -- | Site survey / climate data for Penhold, Alberta | TBD |
| B-005 | B:information:consistency | Normalization | Multi | Guidance | Normalize terminology: "secondary opening mechanism" vs. "secondary opening power integration" vs. "backup power" across documents | Datasheet uses "Door Secondary Opening Power Integration"; Specification uses "Bay Door Secondary Opening Mechanism" (REQ-03); Guidance uses "Door Secondary Opening"; Procedure uses "Door Secondary Opening Method". Minor inconsistency but risks drift. | Datasheet.md; Specification.md; Guidance.md; Procedure.md | entire document scanned | -- | Specification REQ-03 wording as canonical | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | regulatory imperative | 1 | HAS_ITEMS | NFPA 110 applicability unclear |
| C:normative:sufficiency | normative | sufficiency | conformance substantiation | 1 | HAS_ITEMS | No explicit conformance path for fuel storage |
| C:normative:completeness | normative | completeness | regulatory thoroughness | 0 | NO_ITEMS | Standards table in Specification is comprehensive |
| C:normative:consistency | normative | consistency | compliance coherence | 0 | NO_ITEMS | Compliance references are consistent |
| C:operative:necessity | operative | necessity | operational imperative | 0 | NO_ITEMS | Operational needs well-articulated in Guidance P1 |
| C:operative:sufficiency | operative | sufficiency | operational competence | 0 | NO_ITEMS | Procedure steps demonstrate competent execution path |
| C:operative:completeness | operative | completeness | operational thoroughness | 1 | HAS_ITEMS | No ATS transfer time requirement |
| C:operative:consistency | operative | consistency | procedural reliability | 0 | NO_ITEMS | Procedure phases are logically sequenced |
| C:evaluative:necessity | evaluative | necessity | essential merit | 0 | NO_ITEMS | Merit of emergency power well-justified |
| C:evaluative:sufficiency | evaluative | sufficiency | merit sufficiency | 0 | NO_ITEMS | Sufficient justification present |
| C:evaluative:completeness | evaluative | completeness | comprehensive merit | 1 | HAS_ITEMS | No discussion of noise/vibration impact on operations |
| C:evaluative:consistency | evaluative | consistency | value integrity | 0 | NO_ITEMS | Value reasoning is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Clarify NFPA 110 applicability: currently listed as "may be referenced" in Standards table -- confirm whether it is required or advisory | Specification Standards table lists NFPA 110 with "ASSUMPTION: may be referenced." This regulatory imperative is left ambiguous -- it either applies or it does not. | Specification.md | Standards table, NFPA 110 row | -- | AHJ / responsible engineer | TBD |
| C-002 | C:normative:sufficiency | VerificationGap | Specification | Specification | Add verification approach for REQ-07 fuel storage code compliance beyond "code compliance confirmed by responsible engineer" | REQ-07 verification says "code compliance confirmed by responsible engineer" but does not identify which code provisions must be checked (Alberta Fire Code thresholds, secondary containment, environmental). Conformance substantiation is vague. | Specification.md | Verification table, REQ-07 row | -- | Alberta Fire Code; responsible engineer | TBD |
| C-003 | C:operative:completeness | MissingSlot | Specification | Specification | Add ATS transfer time requirement or acceptance criterion (e.g., maximum seconds from utility failure to generator power on essential loads) | No ATS transfer time requirement exists in any document. Procedure Step C3 tests transfer but has no acceptance criterion for timing. For operational thoroughness, a maximum transfer time should be specified. | Specification.md; Procedure.md | Specification#REQ-06; Procedure#Step C3 | -- | CSA C282 or CEC; responsible engineer | TBD |
| C-004 | C:evaluative:completeness | MissingSlot | Guidance | Guidance | Add consideration for generator noise and vibration impact on facility operations and neighboring properties | Guidance Considerations section covers exhaust, refuelling, freeze protection, and security but omits noise/vibration. An outdoor diesel generator near an occupied facility creates operational merit considerations for noise abatement. | Guidance.md | Considerations section | -- | Municipal noise bylaws; manufacturer data | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | binding evidentiary standard | 1 | HAS_ITEMS | Seismic/anchorage requirements absent |
| F:normative:sufficiency | normative | sufficiency | prescribed acceptance threshold | 1 | HAS_ITEMS | No generator start time acceptance threshold |
| F:normative:completeness | normative | completeness | obligatory scope closure | 0 | NO_ITEMS | In-scope/out-of-scope boundaries clear |
| F:normative:consistency | normative | consistency | prescribed systemic fidelity | 0 | NO_ITEMS | Requirements are internally consistent |
| F:operative:necessity | operative | necessity | operational acumen | 0 | NO_ITEMS | Operational logic is sound |
| F:operative:sufficiency | operative | sufficiency | procedural fitness | 1 | HAS_ITEMS | No cold-start procedure for Alberta winter |
| F:operative:completeness | operative | completeness | operational scope mastery | 0 | NO_ITEMS | Phases A through D cover full lifecycle |
| F:operative:consistency | operative | consistency | procedural harmony | 0 | NO_ITEMS | Steps are harmonious |
| F:evaluative:necessity | evaluative | necessity | integral quality foundation | 0 | NO_ITEMS | Quality foundation established through trade-offs |
| F:evaluative:sufficiency | evaluative | sufficiency | principled merit acceptance | 0 | NO_ITEMS | Sufficient merit criteria present |
| F:evaluative:completeness | evaluative | completeness | integral worth coverage | 1 | HAS_ITEMS | Warranty/lifecycle cost not addressed |
| F:evaluative:consistency | evaluative | consistency | integral value fidelity | 0 | NO_ITEMS | Value reasoning is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | MissingSlot | Specification | Specification | Add requirement for generator seismic anchorage or confirm exemption based on post-disaster importance category ruling | Specification REQ-05 addresses outdoor location but no seismic anchorage requirement exists. Guidance notes the post-disaster exemption (OSR 10.3.5) may affect generator requirements but this is not resolved. Binding evidentiary standard requires this be addressed. | Specification.md; Guidance.md | Specification#REQ-05; Guidance#Post-Disaster Importance Category | -- | AHJ; OSR 10.3.5 ruling | TBD |
| F-002 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add acceptance criterion for generator start time (e.g., maximum seconds from ATS signal to generator reaching rated voltage/frequency) | No acceptance threshold for generator start time exists. The ATS transfer test in Procedure Step C3 tests transfer but has no time criterion. This is a standard acceptance parameter for standby generators. | Specification.md; Procedure.md | Specification#Verification table; Procedure#Step C3 | -- | CSA C282; manufacturer specs | TBD |
| F-003 | F:operative:sufficiency | RationaleGap | Guidance | Guidance | Add consideration for cold-start reliability in Penhold Alberta winter conditions (-30C or colder) and required block heater/battery heater provisions | Guidance mentions freeze protection briefly in the Considerations section (block heater, battery heater, enclosure listed as ASSUMPTION) but Procedure has no cold-start verification step. The procedural fitness for Alberta winter startup should be explicitly addressed. | Guidance.md; Procedure.md | Guidance#Generator Location and Service Access; Procedure#Phase C | -- | Manufacturer cold-start specs; Alberta climate data | TBD |
| F-004 | F:evaluative:completeness | RationaleGap | Guidance | Guidance | Add consideration for generator lifecycle cost and warranty requirements to support worth evaluation of the system | No document addresses generator warranty period, expected service life, or lifecycle cost considerations. For integral worth coverage of a 50-year building design life, the generator replacement cycle and warranty should be discussed. | Guidance.md | entire document scanned | -- | Manufacturer warranty; Owner expectations | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | authoritative mandate | 0 | NO_ITEMS | Mandates clear from Addendum 03 |
| D:normative:applying | normative | applying | enforced standard | 1 | HAS_ITEMS | Alberta Fire Code not accessible |
| D:normative:judging | normative | judging | binding conformance verdict | 0 | NO_ITEMS | Verification approaches adequate |
| D:normative:reviewing | normative | reviewing | authoritative assurance | 0 | NO_ITEMS | P.Eng. stamp requirement covers this |
| D:operative:guiding | operative | guiding | resolved process guidance | 0 | NO_ITEMS | Process guidance well-resolved in Procedure |
| D:operative:applying | operative | applying | capable enactment | 0 | NO_ITEMS | Steps A1-A8 are actionable |
| D:operative:judging | operative | judging | resolved performance verdict | 1 | HAS_ITEMS | No performance criterion for generator voltage/frequency regulation |
| D:operative:reviewing | operative | reviewing | resolved process assurance | 0 | NO_ITEMS | Records and verification adequate |
| D:evaluative:guiding | evaluative | guiding | resolved worth orientation | 0 | NO_ITEMS | Purpose statement in Guidance is clear |
| D:evaluative:applying | evaluative | applying | quality deployment | 0 | NO_ITEMS | Quality considerations addressed |
| D:evaluative:judging | evaluative | judging | resolved value judgment | 1 | HAS_ITEMS | No evaluation criterion for refuelling plan acceptability |
| D:evaluative:reviewing | evaluative | reviewing | resolved merit assurance | 0 | NO_ITEMS | Covered by existing review structure |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | VerificationGap | Specification | Specification | Add verification approach for Alberta Fire Code compliance for fuel storage -- currently referenced but standard text not accessible | Specification Standards table lists Alberta Fire Code with "Not directly accessible -- location TBD." No enforced standard can be applied if the standard text has not been obtained. Verification for REQ-07 relies on a standard the team has not yet accessed. | Specification.md | Standards table; Verification table REQ-07 | -- | Design-Builder to obtain Alberta Fire Code | TBD |
| D-002 | D:operative:judging | VerificationGap | Specification | Specification | Add performance acceptance criteria for generator voltage and frequency regulation under load (e.g., voltage within +/- X%, frequency within +/- Y Hz) | No performance verdict criteria exist for generator output quality. Load bank test in Procedure Step C2 tests load capacity but not output quality parameters. | Specification.md; Procedure.md | Specification#Verification table REQ-01; Procedure#Step C2 | -- | CSA C282; generator manufacturer specs | TBD |
| D-003 | D:evaluative:judging | WeakStatement | Guidance | Guidance | Clarify under Trade-off 3 what criteria the Owner should use to evaluate whether a refuelling plan is an acceptable alternative to full 72-hour tank autonomy | Trade-off 3 mentions a refuelling plan as a potential alternative but provides no criteria for judging its acceptability. The value judgment is deferred without guidance on how to resolve it. | Guidance.md | Trade-offs > Trade-off 3: Tank Size vs. Refuelling Plan | -- | Owner decision with fire operations input | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | governing priority | 0 | NO_ITEMS | Priorities clear |
| X:guiding:sufficiency | guiding | sufficiency | governing adequacy | 0 | NO_ITEMS | Guidance is adequate |
| X:guiding:completeness | guiding | completeness | governing scope | 0 | NO_ITEMS | Scope well-defined |
| X:guiding:consistency | guiding | consistency | governing coherence | 0 | NO_ITEMS | Governing documents are coherent |
| X:applying:necessity | applying | necessity | implementation foundation | 1 | HAS_ITEMS | Number of doors on generator unclear |
| X:applying:sufficiency | applying | sufficiency | deployment fitness | 1 | HAS_ITEMS | Electrical room coordination gap |
| X:applying:completeness | applying | completeness | deployment breadth | 0 | NO_ITEMS | Deployment scope is complete |
| X:applying:consistency | applying | consistency | deployment fidelity | 0 | NO_ITEMS | Deployment approach is consistent |
| X:judging:necessity | judging | necessity | adjudicative foundation | 1 | HAS_ITEMS | REQ-02 verification lacks demand calc threshold |
| X:judging:sufficiency | judging | sufficiency | adjudicative threshold | 0 | NO_ITEMS | Verification approaches have sufficient thresholds generally |
| X:judging:completeness | judging | completeness | adjudicative totality | 0 | NO_ITEMS | All 9 requirements have verification approaches |
| X:judging:consistency | judging | consistency | adjudicative fidelity | 0 | NO_ITEMS | Verification approaches are consistently structured |
| X:reviewing:necessity | reviewing | necessity | assurance foundation | 1 | HAS_ITEMS | No independent review/QA step for essential loads list |
| X:reviewing:sufficiency | reviewing | sufficiency | assurance adequacy | 0 | NO_ITEMS | P.Eng. stamp provides adequate assurance |
| X:reviewing:completeness | reviewing | completeness | assurance totality | 0 | NO_ITEMS | Records table is comprehensive |
| X:reviewing:consistency | reviewing | consistency | assurance fidelity | 0 | NO_ITEMS | Assurance approach is consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:applying:necessity | Normalization | Multi | Datasheet | Clarify exact number of overhead doors requiring generator backup power -- Datasheet says "fire apparatus bays and PW bays" without a count | Implementation foundation requires knowing the quantity of door operators on the essential loads panel. Datasheet and Specification reference doors generically without stating the count. DEL-02-04 coordination needed. | Datasheet.md; Specification.md | Datasheet#Door Secondary Opening Power Integration; Specification#REQ-03 | -- | DEL-02-04 door schedule | TBD |
| X-002 | X:applying:sufficiency | VerificationGap | Specification | Specification | Add verification that ATS location has been coordinated with electrical room layout in DEL-02-06 | REQ-09 verification says "coordination meeting record or coordination matrix" but deployment fitness requires confirming ATS physical location is resolved, not just that a meeting occurred. | Specification.md | Verification table, REQ-09 | -- | DEL-02-06 electrical lead | TBD |
| X-003 | X:judging:necessity | VerificationGap | Specification | Specification | Strengthen REQ-02 verification: add criterion that demand calculations demonstrate generator can serve all listed loads simultaneously | REQ-02 verification says "demand calculations provided" but does not require the calculations to demonstrate simultaneous service. The adjudicative foundation for load adequacy requires this explicit criterion. | Specification.md | Verification table, REQ-02 | -- | Responsible electrical engineer | TBD |
| X-004 | X:reviewing:necessity | MissingSlot | Procedure | Procedure | Add an independent review or peer check step for the essential loads list before it drives generator sizing | The essential loads list is the foundation of the entire deliverable but no review gate exists in the Procedure before it is used for generator sizing (Step A4). An assurance foundation step (e.g., review by operations/fire department staff) would reduce risk. | Procedure.md | Steps A3-A4 | -- | Design-Builder QA process; fire department input | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | binding governance foundation | 1 | HAS_ITEMS | Emission/environmental requirement absent |
| E:normative:sufficiency | normative | sufficiency | prescribed governance threshold | 0 | NO_ITEMS | Governance thresholds adequately prescribed |
| E:normative:completeness | normative | completeness | binding governance scope | 0 | NO_ITEMS | Governance scope is complete |
| E:normative:consistency | normative | consistency | binding governance fidelity | 0 | NO_ITEMS | Governance is consistent |
| E:operative:necessity | operative | necessity | operational governance basis | 1 | HAS_ITEMS | No emergency refuelling procedure |
| E:operative:sufficiency | operative | sufficiency | operational governance threshold | 0 | NO_ITEMS | Operational thresholds adequate |
| E:operative:completeness | operative | completeness | operational governance scope | 0 | NO_ITEMS | Scope is complete |
| E:operative:consistency | operative | consistency | operational governance fidelity | 0 | NO_ITEMS | Fidelity is maintained |
| E:evaluative:necessity | evaluative | necessity | value governance basis | 1 | HAS_ITEMS | No discussion of generator redundancy philosophy |
| E:evaluative:sufficiency | evaluative | sufficiency | value governance threshold | 0 | NO_ITEMS | Value thresholds adequate |
| E:evaluative:completeness | evaluative | completeness | value governance scope | 0 | NO_ITEMS | Value scope adequate |
| E:evaluative:consistency | evaluative | consistency | value governance fidelity | 0 | NO_ITEMS | Value fidelity maintained |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:necessity | Normalization | Specification | Specification | Add reference to applicable emission or environmental standards for outdoor diesel generator operation in Alberta | Specification Standards table covers electrical and fire codes but does not address diesel exhaust emission standards or environmental protection requirements that may apply to a permanently installed outdoor diesel generator. Binding governance foundation should include environmental requirements. | Specification.md | Standards table | -- | Alberta Environment and Parks; municipal bylaws | TBD |
| E-002 | E:operative:necessity | RationaleGap | Procedure | Procedure | Add emergency refuelling procedure or reference to logistics plan for fuel resupply during extended power outage | Procedure Phase D covers routine refuelling monitoring but does not address emergency refuelling logistics during an extended outage when the generator is running. Operational governance basis should address this scenario for a 72-hour runtime facility. | Procedure.md | Phase D: Operational Use | -- | Owner operations plan; fuel supplier agreement | TBD |
| E-003 | E:evaluative:necessity | MissingSlot | Guidance | Guidance | Add brief discussion of single-generator vs. redundant-generator philosophy and why single unit is appropriate (or flag if redundancy should be evaluated) | No document discusses whether a single generator is sufficient or whether redundancy should be considered for an emergency operations facility. For value governance basis, the single-unit assumption should be explicitly stated and justified. | Guidance.md | entire document scanned | -- | Owner risk tolerance; OBJ-002 | TBD |
