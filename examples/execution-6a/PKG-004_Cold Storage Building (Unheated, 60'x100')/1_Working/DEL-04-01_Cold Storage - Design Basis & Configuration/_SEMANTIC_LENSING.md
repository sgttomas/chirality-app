# Semantic Lensing Register: DEL-04-01 Cold Storage -- Design Basis & Configuration

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/PKG-004_Cold Storage Building (Unheated, 60'x100')/1_Working/DEL-04-01_Cold Storage - Design Basis & Configuration/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-04-01_Cold Storage - Design Basis & Configuration/_CONTEXT.md
- _STATUS.md -- DEL-04-01_Cold Storage - Design Basis & Configuration/_STATUS.md (Current State: SEMANTIC_READY)
- _SEMANTIC.md -- DEL-04-01_Cold Storage - Design Basis & Configuration/_SEMANTIC.md
- Datasheet.md -- DEL-04-01_Cold Storage - Design Basis & Configuration/Datasheet.md
- Specification.md -- DEL-04-01_Cold Storage - Design Basis & Configuration/Specification.md
- Guidance.md -- DEL-04-01_Cold Storage - Design Basis & Configuration/Guidance.md
- Procedure.md -- DEL-04-01_Cold Storage - Design Basis & Configuration/Procedure.md
- _REFERENCES.md -- DEL-04-01_Cold Storage - Design Basis & Configuration/_REFERENCES.md

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 18
- By document:
  - Datasheet: 2
  - Specification: 10
  - Guidance: 1
  - Procedure: 3
  - Multi: 2
- By matrix:
  - A: 4  B: 3  C: 2  F: 3  D: 2  X: 3  E: 1
- By type:
  - Conflict: 0
  - VerificationGap: 4
  - MissingSlot: 6
  - WeakStatement: 3
  - RationaleGap: 2
  - Normalization: 1
  - TBD_Question: 2
  - MatrixError: 0
- Notable conflicts: 0
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage (required)
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | WeakStatement on building height |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | MissingSlot for non-combustible construction verification |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | TBD_Question on ABC edition |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | Procedure covers AHJ coordination adequately |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Procedure Phase A-D steps are well-structured |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | TBD_Question on equipment list for cold storage |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Verification tables present in both Specification and Procedure |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Procedure records table covers audit trail |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance P2/P6 cover cost-effectiveness value clearly |
| A:evaluative:applying | evaluative | applying | merit application | 0 | NO_ITEMS | Trade-offs T1-T3 address merit application adequately |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Covered by evaluation criteria implicit in OBJ-004 |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | No gap; Procedure D1-D2 cover inspection and deficiency |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Clarify REQ-04-01-003 by adding a minimum numeric eave height or requiring DB to document proposed height with justification prior to design finalization | REQ-04-01-003 uses "minimum height sufficient to support safe operation" without a quantified threshold; the ASSUMPTION note acknowledges this is TBD but no acceptance criterion binds the DB to a specific clearance standard | Specification.md | REQ-04-01-003 | -- | Specification.md | TBD |
| A-002 | A:normative:applying | MissingSlot | Specification | Specification | Add verification method for REQ-04-01-010 non-combustible construction requirement (e.g., material data sheet review confirming non-combustible classification per ABC) | REQ-04-01-010 requires non-combustible construction but the Verification table entry only references "weather-tight" and "envelope review" without explicitly addressing non-combustible classification testing or evidence | Specification.md | Verification table, REQ-04-01-010 row | -- | Specification.md | TBD |
| A-003 | A:normative:judging | TBD_Question | Multi | Specification | Record TBD: Confirm which edition of the Alberta Building Code (ABC) governs this project and record it in the Standards table | The Standards table lists ABC as governing but does not identify the edition; the applicable edition determines structural load values and requirements | Specification.md | Standards table | -- | Owner/AHJ | TBD |
| A-004 | A:operative:applying | TBD_Question | Procedure | Guidance | Record TBD: Confirm which specific Public Works equipment types will be stored in the cold storage building (vs. main building) to establish minimum clear height | Guidance C2 raises this question and Procedure Step A1 depends on the answer, but no document records the confirmed equipment list; this is an external input needed from the Owner | Guidance.md; Procedure.md | Guidance C2; Procedure Step A1 | -- | Owner | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage (required)
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Missing importance category factor in Datasheet |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Datasheet Attributes and Conditions tables are adequately evidenced |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Missing ground snow load value |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Dimensions and sources are consistently cited |
| B:information:necessity | information | necessity | essential signal | 0 | NO_ITEMS | Key signals (size, unheated, clear-span) are present across all docs |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context is adequately provided in all documents |
| B:information:completeness | information | completeness | comprehensive account | 1 | HAS_ITEMS | Missing enumeration of applicable CSA standards |
| B:information:consistency | information | consistency | coherent message | 0 | NO_ITEMS | Messages are coherent across documents |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Structural and architectural basis is fundamentally understood |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Personnel prerequisites in Procedure establish competence |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | No gap; combined doc set demonstrates thorough coverage |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 0 | NO_ITEMS | Trade-offs and principles demonstrate discernment |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Guidance trade-offs provide adequate judgment basis |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view is present through Guidance considerations |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is principled and consistent across docs |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | MissingSlot | Datasheet | Datasheet | Add the building importance category (or exemption basis) as an Attribute entry with ABC reference | Datasheet records post-disaster exemption intent but does not state the actual importance category classification (e.g., Normal Importance per ABC) that determines structural load factors | Datasheet.md | Attributes table | -- | Datasheet.md | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add site-specific climatic design data (ground snow load, hourly wind pressure, seismic hazard values for Penhold, AB) as Conditions entries or reference to ABC Appendix C data | The Specification requires design for snow, wind, and lateral loads (REQ-04-01-006) but neither the Datasheet nor Specification records the actual numeric climatic design values; these are essential facts for structural design | Datasheet.md; Specification.md | Datasheet Conditions table; Specification REQ-04-01-006 | -- | Datasheet.md | TBD |
| B-003 | B:information:completeness | MissingSlot | Specification | Specification | Add a note in Standards table identifying that DB shall enumerate applicable CSA standards (e.g., CSA S136, CSA O86, CSA A23.3) during detailed design with a placeholder for DB response | The Standards table notes "specific applicable CSA standards to be identified by DB" but provides no placeholder structure for the DB to populate; this leaves a completeness gap in the normative record | Specification.md | Standards table | -- | Specification.md | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage (required)
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | Codified Obligation | 0 | NO_ITEMS | Obligations are codified in the 15 REQ entries |
| C:normative:sufficiency | normative | sufficiency | Regulatory Sufficiency | 1 | HAS_ITEMS | Verification gap for design life |
| C:normative:completeness | normative | completeness | Exhaustive Compliance | 0 | NO_ITEMS | Requirements cover all OSR sections comprehensively |
| C:normative:consistency | normative | consistency | Uniform Governance | 0 | NO_ITEMS | Governance is uniform across the requirement set |
| C:operative:necessity | operative | necessity | Operational Prerequisite | 0 | NO_ITEMS | Procedure prerequisites table is well-structured |
| C:operative:sufficiency | operative | sufficiency | Demonstrated Capability | 0 | NO_ITEMS | Personnel prerequisites and step structure demonstrate capability |
| C:operative:completeness | operative | completeness | Comprehensive Execution | 1 | HAS_ITEMS | Missing hold/witness points in construction phase |
| C:operative:consistency | operative | consistency | Standardized Operation | 0 | NO_ITEMS | Procedure steps follow a consistent pattern |
| C:evaluative:necessity | evaluative | necessity | Inherent Merit | 0 | NO_ITEMS | Merit basis established through OBJ-004 and Guidance Purpose |
| C:evaluative:sufficiency | evaluative | sufficiency | Substantiated Worth | 0 | NO_ITEMS | Trade-offs substantiate worth decisions |
| C:evaluative:completeness | evaluative | completeness | Holistic Valuation | 0 | NO_ITEMS | Holistic view provided by Guidance considerations |
| C:evaluative:consistency | evaluative | consistency | Principled Worth Alignment | 0 | NO_ITEMS | Value alignment is principled across docs |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:sufficiency | VerificationGap | Specification | Specification | Strengthen REQ-04-01-004 verification by specifying what evidence demonstrates 20-year design life (e.g., material manufacturer warranty data, accelerated weathering test data, or professional engineer attestation of material suitability) | The Verification table entry for REQ-04-01-004 says "Design brief / specification narrative review: confirm materials and system selections reference 20-year design life basis" but does not define what constitutes sufficient evidence of design life compliance | Specification.md | Verification table, REQ-04-01-004 row | -- | Specification.md | TBD |
| C-002 | C:operative:completeness | MissingSlot | Procedure | Procedure | Add hold points or witness points in Phase C construction steps (e.g., hold point after foundation/subgrade inspection before framing, hold point for envelope weather-tightness inspection before closeout) | Procedure Phase C steps C1-C6 describe construction activities but do not identify mandatory hold points or inspection witness points where work must stop for verification before proceeding; this is standard practice for construction procedures | Procedure.md | Phase C: Construction | -- | Procedure.md | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage (required)
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | Authoritative Obligation Basis | 0 | NO_ITEMS | Obligation basis is well-established through OSR sourcing |
| F:normative:sufficiency | normative | sufficiency | Demonstrated Conformance | 1 | HAS_ITEMS | Verification gap for envelope watertightness |
| F:normative:completeness | normative | completeness | Total Regulatory Coverage | 1 | HAS_ITEMS | Missing fire separation / spatial separation requirement |
| F:normative:consistency | normative | consistency | Coherent Regulatory Fidelity | 0 | NO_ITEMS | Requirements are coherently cross-referenced |
| F:operative:necessity | operative | necessity | Validated Readiness Basis | 0 | NO_ITEMS | Prerequisites are validated |
| F:operative:sufficiency | operative | sufficiency | Verified Execution Fitness | 0 | NO_ITEMS | Step structure demonstrates execution fitness |
| F:operative:completeness | operative | completeness | Exhaustive Implementation Scope | 1 | HAS_ITEMS | Rationale gap on geotechnical adequacy |
| F:operative:consistency | operative | consistency | Coordinated Process Discipline | 0 | NO_ITEMS | Process discipline is coordinated across phases |
| F:evaluative:necessity | evaluative | necessity | Validated Worth Imperative | 0 | NO_ITEMS | Worth imperative is validated through OBJ-004 |
| F:evaluative:sufficiency | evaluative | sufficiency | Calibrated Merit Justification | 0 | NO_ITEMS | Merit justification is calibrated in trade-offs |
| F:evaluative:completeness | evaluative | completeness | Exhaustive Worth Account | 0 | NO_ITEMS | Worth account is sufficient for this deliverable scope |
| F:evaluative:consistency | evaluative | consistency | Principled Valuation Coherence | 0 | NO_ITEMS | Valuation coherence is principled |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add verification method for envelope watertightness at joints (e.g., visual inspection per construction checklist, or water-spray test at critical joints) | REQ-04-01-010 requires "watertight at joints" but the Verification table entry does not specify how joint watertightness will be tested or confirmed during construction; "construction inspection / building envelope review" is too vague for a critical performance requirement on an unheated building | Specification.md | Verification table, REQ-04-01-010 row | -- | Specification.md | TBD |
| F-002 | F:normative:completeness | VerificationGap | Specification | Specification | Add a requirement or note regarding fire separation distance / spatial separation from the main building per ABC, or confirm that the cold storage building placement satisfies ABC spatial separation requirements | The Specification addresses code compliance generally (REQ-04-01-015) but does not specifically address fire separation or spatial separation distance from the main building, which is a standard ABC requirement for buildings on the same property; this may affect site placement (REQ-04-01-014) | Specification.md; Datasheet.md | REQ-04-01-014; REQ-04-01-015 | -- | Specification.md | TBD |
| F-003 | F:operative:completeness | RationaleGap | Guidance | Guidance | Add a consideration noting the DB's responsibility for geotechnical adequacy and how pole shed foundations (embedded posts) vs. conventional foundations differ in their geotechnical requirements; reference the Geotechnical Investigation Report (Appendix D) | Datasheet notes "DB responsible for adequacy of geotechnical information" and the Geotechnical Investigation Report is referenced, but Guidance does not discuss how geotechnical conditions may influence foundation/framing selection for the cold storage building; this is relevant because pole shed construction has different geotechnical requirements than slab-on-grade | Datasheet.md; Guidance.md | Datasheet Conditions table (Foundation ground conditions); Guidance C1 | -- | Guidance.md | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage (required)
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | Established Regulatory Mandate | 0 | NO_ITEMS | Regulatory mandate is established |
| D:normative:applying | normative | applying | Enforced Conformance Protocol | 0 | NO_ITEMS | Conformance protocol is enforced through requirements |
| D:normative:judging | normative | judging | Settled Compliance Ruling | 0 | NO_ITEMS | Compliance determination approach is settled |
| D:normative:reviewing | normative | reviewing | Confirmed Oversight Integrity | 0 | NO_ITEMS | Oversight integrity is confirmed through AHJ coordination |
| D:operative:guiding | operative | guiding | Validated Process Directive | 1 | HAS_ITEMS | Normalization issue on design submission milestones |
| D:operative:applying | operative | applying | Confirmed Implementation | 0 | NO_ITEMS | Implementation approach is confirmed |
| D:operative:judging | operative | judging | Settled Performance Verdict | 0 | NO_ITEMS | Performance assessment criteria are present |
| D:operative:reviewing | operative | reviewing | Confirmed Process Scrutiny | 0 | NO_ITEMS | Process scrutiny is confirmed |
| D:evaluative:guiding | evaluative | guiding | Confirmed Worth Direction | 1 | HAS_ITEMS | WeakStatement on aesthetic coordination scope |
| D:evaluative:applying | evaluative | applying | Settled Merit Enactment | 0 | NO_ITEMS | Merit enactment is settled |
| D:evaluative:judging | evaluative | judging | Concluded Worth Ruling | 0 | NO_ITEMS | Worth ruling is concluded through trade-offs |
| D:evaluative:reviewing | evaluative | reviewing | Confirmed Valuation Scrutiny | 0 | NO_ITEMS | Valuation scrutiny is confirmed |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:operative:guiding | Normalization | Multi | Multi | Normalize the design submission milestone names between Procedure Step B5 and RFP terminology; confirm whether "Foundation IFC" applies to cold storage (Procedure B5 hedges with "if applicable") | Procedure Step B5 lists design submission milestones including "Foundation IFC (if applicable to cold storage)" but Specification does not reference these milestone names; the milestone terminology should be consistent across the document set and clarified for the cold storage building | Procedure.md; Specification.md | Procedure Step B5; Specification entire document scanned | -- | Procedure.md | TBD |
| D-002 | D:evaluative:guiding | WeakStatement | Specification | Guidance | Clarify the scope of "aesthetic coordination" beyond door window profile and key matching; add guidance on whether cladding color, roof profile, or material type must coordinate with the main building or whether these are DB-discretionary | REQ-04-01-009 states "overall external appearance shall coordinate with the main building aesthetic" as a design objective but Guidance T3 only resolves the tension for cladding/roof, noting "full aesthetic parity is not required"; the Specification requirement remains ambiguous on what "coordinate" means beyond doors | Specification.md; Guidance.md | REQ-04-01-009; Guidance T3 | -- | Guidance.md | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage (required)
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | Grounded Directive Obligation | 0 | NO_ITEMS | Directive obligations are grounded |
| X:guiding:sufficiency | guiding | sufficiency | Justified Steering Adequacy | 0 | NO_ITEMS | Steering adequacy is justified |
| X:guiding:completeness | guiding | completeness | Exhaustive Directive Coverage | 1 | HAS_ITEMS | VerificationGap on condensation prevention |
| X:guiding:consistency | guiding | consistency | Harmonized Directive Alignment | 0 | NO_ITEMS | Directive alignment is harmonized |
| X:applying:necessity | applying | necessity | Obligatory Deployment Basis | 0 | NO_ITEMS | Deployment basis is established |
| X:applying:sufficiency | applying | sufficiency | Demonstrated Practice Scope | 0 | NO_ITEMS | Practice scope is demonstrated |
| X:applying:completeness | applying | completeness | Total Implementation Range | 1 | HAS_ITEMS | WeakStatement on ventilation approach |
| X:applying:consistency | applying | consistency | Consistent Practice Standard | 0 | NO_ITEMS | Practice standard is consistent |
| X:judging:necessity | judging | necessity | Essential Adjudication Basis | 0 | NO_ITEMS | Adjudication basis is established through verification tables |
| X:judging:sufficiency | judging | sufficiency | Proportionate Ruling Scope | 0 | NO_ITEMS | Ruling scope is proportionate |
| X:judging:completeness | judging | completeness | Exhaustive Adjudication Scope | 0 | NO_ITEMS | Adjudication scope covers all 15 requirements |
| X:judging:consistency | judging | consistency | Principled Ruling Discipline | 0 | NO_ITEMS | Ruling discipline is principled |
| X:reviewing:necessity | reviewing | necessity | Confirmed Audit Obligation | 1 | HAS_ITEMS | RationaleGap on warranty scope |
| X:reviewing:sufficiency | reviewing | sufficiency | Reviewed Fitness Adequacy | 0 | NO_ITEMS | Fitness adequacy is reviewed |
| X:reviewing:completeness | reviewing | completeness | Exhaustive Audit Coverage | 0 | NO_ITEMS | Audit coverage is exhaustive through records table |
| X:reviewing:consistency | reviewing | consistency | Disciplined Audit Alignment | 0 | NO_ITEMS | Audit alignment is disciplined |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | VerificationGap | Specification | Specification | Add a verification method for REQ-04-01-011 that includes a post-construction performance check for condensation (e.g., visual inspection during first winter season or temperature/humidity monitoring protocol) | The Verification table for REQ-04-01-011 only references "Mechanical design review (DEL-04-04)" but does not include a post-construction performance verification that the ventilation/air circulation system actually prevents condensation; design review alone is insufficient for a performance requirement in an unheated building subject to freeze-thaw cycling | Specification.md | Verification table, REQ-04-01-011 row | -- | Specification.md | TBD |
| X-002 | X:applying:completeness | WeakStatement | Specification | Specification | Strengthen REQ-04-01-011 to specify minimum performance criteria for the ventilation approach (e.g., "ventilation system shall maintain interior relative humidity below condensation threshold during winter storage conditions") or require DB to propose measurable acceptance criteria | REQ-04-01-011 requires "adequate ventilation or alternate air circulation to prevent condensation and icing" but "adequate" is undefined and no measurable performance standard is stated; the DB has no quantitative target to design against | Specification.md | REQ-04-01-011 | -- | Specification.md | TBD |
| X-003 | X:reviewing:necessity | RationaleGap | Procedure | Guidance | Add guidance on warranty scope and duration expectations for the cold storage building structural system, roofing, and doors, noting how the 20-year design life relates to typical warranty periods | Procedure Records table lists "Warranty certificates (structural system, doors, roofing)" but neither the Specification nor Guidance discusses warranty duration expectations or how warranty scope relates to the 20-year design life; this is a gap in the rationale for warranty requirements | Procedure.md; Specification.md | Procedure Records table; Specification entire document scanned | -- | Guidance.md | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage (required)
| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | Foundational Compliance Obligation | 0 | NO_ITEMS | Compliance obligation is foundationally established |
| E:normative:sufficiency | normative | sufficiency | Demonstrated Regulatory Fitness | 0 | NO_ITEMS | Regulatory fitness is demonstrated |
| E:normative:completeness | normative | completeness | Total Regulatory Assurance | 1 | HAS_ITEMS | Missing accessibility consideration |
| E:normative:consistency | normative | consistency | Harmonized Regulatory Order | 0 | NO_ITEMS | Regulatory order is harmonized |
| E:operative:necessity | operative | necessity | Confirmed Operational Foundation | 0 | NO_ITEMS | Operational foundation is confirmed |
| E:operative:sufficiency | operative | sufficiency | Demonstrated Operational Scope | 0 | NO_ITEMS | Operational scope is demonstrated |
| E:operative:completeness | operative | completeness | Total Operational Assurance | 0 | NO_ITEMS | Operational assurance is sufficient for scope |
| E:operative:consistency | operative | consistency | Disciplined Operational Coherence | 0 | NO_ITEMS | Operational coherence is disciplined |
| E:evaluative:necessity | evaluative | necessity | Settled Merit Obligation | 0 | NO_ITEMS | Merit obligation is settled |
| E:evaluative:sufficiency | evaluative | sufficiency | Demonstrated Worth Fitness | 0 | NO_ITEMS | Worth fitness is demonstrated |
| E:evaluative:completeness | evaluative | completeness | Total Valuation Assurance | 0 | NO_ITEMS | Valuation assurance is sufficient |
| E:evaluative:consistency | evaluative | consistency | Disciplined Valuation Coherence | 0 | NO_ITEMS | Valuation coherence is disciplined |

### Warranted Items
| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:completeness | MissingSlot | Specification | Specification | Add a note confirming whether ABC accessibility requirements apply to the cold storage building (an unheated ancillary storage building may be exempt, but this should be explicitly stated rather than assumed) | The Specification addresses code compliance generally (REQ-04-01-015) but does not mention accessibility requirements; for an unheated storage building with person doors, the ABC may or may not require barrier-free access; this should be confirmed rather than left implicit | Specification.md | REQ-04-01-015 | -- | Specification.md | TBD |
