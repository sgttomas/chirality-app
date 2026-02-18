# Semantic Lensing Register: DEL-05-03 Option -- Access Control

**Generated:** 2026-02-17
**Deliverable Folder:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/PKG-005_Optional Priced Items & Owner-Elected Additions/1_Working/DEL-05-03_Option - Access Control/
**Warnings:** None

**Inputs Read:**
- _CONTEXT.md -- DEL-05-03 identity, SOW-0502, OBJ-010, anticipated artifacts
- _STATUS.md -- Current State: SEMANTIC_READY (2026-02-17)
- _SEMANTIC.md -- Matrices A, B, C, F, D, X, E parsed (all 7 result tables extracted)
- Datasheet.md -- Identification, Attributes, Conditions, Construction, References
- Specification.md -- REQ-AC-001 through REQ-AC-008, Standards, Verification, Documentation
- Guidance.md -- Purpose, Principles (5), Considerations (4), Trade-offs (3), Conflict Table
- Procedure.md -- Phase A (Steps A1-A6), Phase B (Steps B1-B6), Verification, Records
- _REFERENCES.md -- OSR Appendix A section 12.3 noted

**Purpose:** Apply CHIRALITY_FRAMEWORK matrix cells as lenses over the 4 Documents, capturing warranted enrichment inputs for a later enrichment pass.

---

## Summary

- Total warranted items: 27
- By document:
  - Datasheet: 5
  - Specification: 10
  - Guidance: 4
  - Procedure: 3
  - Multi: 5
- By matrix:
  - A: 5  B: 5  C: 3  F: 4  D: 3  X: 4  E: 3
- By type:
  - Conflict: 0
  - VerificationGap: 6
  - MissingSlot: 7
  - WeakStatement: 4
  - RationaleGap: 3
  - Normalization: 3
  - TBD_Question: 4
  - MatrixError: 0
- Notable conflicts: 0 (2 conflicts already captured in Guidance.md Conflict Table; no new cross-document conflicts found)
- Matrix parse errors: 0

---

## Matrix A -- Orientation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| A:normative:guiding | normative | guiding | prescriptive direction | 1 | HAS_ITEMS | Standards referenced as ASSUMPTION only |
| A:normative:applying | normative | applying | mandatory practice | 1 | HAS_ITEMS | Key fob minimum is stated but technology specifics TBD |
| A:normative:judging | normative | judging | compliance determination | 1 | HAS_ITEMS | Code compliance verification lacks specific acceptance criteria |
| A:normative:reviewing | normative | reviewing | regulatory audit | 0 | NO_ITEMS | AHJ inspection referenced in Verification table |
| A:operative:guiding | operative | guiding | procedural direction | 0 | NO_ITEMS | Phase A and Phase B procedures are present and adequately directed |
| A:operative:applying | operative | applying | practical execution | 1 | HAS_ITEMS | Missing fire alarm integration step |
| A:operative:judging | operative | judging | performance assessment | 0 | NO_ITEMS | Procedure verification checks cover key assessment points |
| A:operative:reviewing | operative | reviewing | process audit | 0 | NO_ITEMS | Step A6 internal review check addresses this |
| A:evaluative:guiding | evaluative | guiding | value orientation | 0 | NO_ITEMS | Guidance Purpose section adequately frames value proposition |
| A:evaluative:applying | evaluative | applying | merit application | 1 | HAS_ITEMS | No lifecycle cost or value-for-money framing |
| A:evaluative:judging | evaluative | judging | worth determination | 0 | NO_ITEMS | Trade-offs in Guidance address cost vs. granularity adequately |
| A:evaluative:reviewing | evaluative | reviewing | quality appraisal | 0 | NO_ITEMS | Commissioning report covers quality review |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A-001 | A:normative:guiding | WeakStatement | Specification | Specification | Strengthen standards applicability: currently all access-control-specific standards (UL 294, ANSI/BHMA A156.25, CSA C22.1) are listed as "ASSUMPTION: likely applicable; location TBD" -- confirm applicability or record as TBD_Question for Owner/AHJ | All normative standards for access control equipment are tagged as assumptions rather than confirmed prescriptive direction; this weakens the compliance basis for the entire deliverable | Specification.md | Standards table | -- | Specification.md | TBD |
| A-002 | A:normative:applying | TBD_Question | Datasheet | Datasheet | Record TBD: Confirm whether Alberta-specific access control licensing or installer certification requirements apply (e.g., Alberta Security Services and Investigators Act) | Mandatory practice for access control installation may require licensed security system installers under Alberta provincial regulation; no mention in any document | Datasheet.md; Specification.md | entire document scanned | -- | Owner/AHJ | TBD |
| A-003 | A:normative:judging | VerificationGap | Specification | Specification | Add specific acceptance criteria for REQ-AC-007 Code Compliance: define what constitutes satisfactory AHJ inspection outcome and which code sections must be demonstrated | Verification table says "Confirm door hardware and egress provisions comply with Alberta Building Code; AHJ inspection" but does not specify pass/fail criteria or which code clauses apply | Specification.md | Verification table, REQ-AC-007 row | -- | Specification.md | TBD |
| A-004 | A:operative:applying | MissingSlot | Procedure | Procedure | Add step in Phase B addressing fire alarm system integration coordination (door hold-open devices, fire alarm release of magnetic locks on alarm) | Procedure Step B3 coordinates with electrical trades and door hardware but omits fire alarm integration, which is standard practice for magnetic-lock-equipped doors on fire-separation paths | Procedure.md | Phase B: Step B3 -- Coordinate with Construction | -- | Procedure.md | TBD |
| A-005 | A:evaluative:applying | MissingSlot | Guidance | Guidance | Add a consideration addressing lifecycle cost and total cost of ownership (credential replacement, software licensing renewals, ongoing maintenance) to support Owner election decision | Guidance covers upfront pricing and trade-offs for granularity vs. cost but does not address ongoing operational cost, which is relevant to the Owner's value-for-money election decision | Guidance.md | Considerations section | -- | Guidance.md | TBD |

---

## Matrix B -- Conceptualization (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| B:data:necessity | data | necessity | essential fact | 1 | HAS_ITEMS | Number of zones not quantified |
| B:data:sufficiency | data | sufficiency | adequate evidence | 0 | NO_ITEMS | Room list from Functional Program provides adequate evidence |
| B:data:completeness | data | completeness | comprehensive record | 1 | HAS_ITEMS | Door schedule cross-reference incomplete |
| B:data:consistency | data | consistency | reliable measurement | 0 | NO_ITEMS | Consistent data across documents for scope boundaries |
| B:information:necessity | information | necessity | essential signal | 1 | HAS_ITEMS | No signal on system capacity/scalability |
| B:information:sufficiency | information | sufficiency | adequate context | 0 | NO_ITEMS | Context for shared-use access is adequate across docs |
| B:information:completeness | information | completeness | comprehensive account | 0 | NO_ITEMS | Account of operational context is comprehensive in Guidance |
| B:information:consistency | information | consistency | coherent message | 1 | HAS_ITEMS | Terminology inconsistency for lock types |
| B:knowledge:necessity | knowledge | necessity | fundamental understanding | 0 | NO_ITEMS | Access control design fundamentals are represented in Guidance |
| B:knowledge:sufficiency | knowledge | sufficiency | competent expertise | 0 | NO_ITEMS | Documents assume competent DB; appropriate for proposal stage |
| B:knowledge:completeness | knowledge | completeness | thorough mastery | 0 | NO_ITEMS | Depth of technical knowledge is appropriate for optional item |
| B:knowledge:consistency | knowledge | consistency | coherent understanding | 0 | NO_ITEMS | Understanding is coherent across the four documents |
| B:wisdom:necessity | wisdom | necessity | essential discernment | 1 | HAS_ITEMS | No guidance on decommissioning/removal if not elected later |
| B:wisdom:sufficiency | wisdom | sufficiency | adequate judgment | 0 | NO_ITEMS | Trade-offs in Guidance provide adequate judgment framing |
| B:wisdom:completeness | wisdom | completeness | holistic insight | 0 | NO_ITEMS | Holistic view is covered by Guidance Considerations |
| B:wisdom:consistency | wisdom | consistency | principled reasoning | 0 | NO_ITEMS | Reasoning is consistent across documents |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B-001 | B:data:necessity | WeakStatement | Datasheet | Datasheet | Clarify "Number of zones" attribute: currently "Multiple (exact number TBD)" -- add a minimum zone count derived from Functional Program room groupings or state explicitly that DB proposes count | The essential factual data point of zone quantity is materially vague; this affects pricing, device schedule scope, and verification | Datasheet.md | Attributes table, "Number of zones" row | -- | Datasheet.md | TBD |
| B-002 | B:data:completeness | MissingSlot | Datasheet | Datasheet | Add attribute for maximum cable run length or system topology constraint (e.g., max reader-to-panel distance) to inform device schedule feasibility | Device schedule references controller assignments but no data exists on system topology constraints that would affect feasibility of proposed layouts | Datasheet.md | Construction table | -- | Datasheet.md | TBD |
| B-003 | B:information:necessity | TBD_Question | Multi | Guidance | Record TBD: What is the expected total number of credentialed users (staff headcount across Fire and Public Works), and does the system need visitor/temporary credential capability? | No document states user population or visitor access requirements; these are essential signals for system sizing and credential management complexity | Datasheet.md; Specification.md; Guidance.md | entire document scanned | -- | Owner | TBD |
| B-004 | B:information:consistency | Normalization | Multi | Multi | Normalize lock hardware terminology: Specification REQ-AC-004 lists "magnetic lock, electric strike"; Guidance Trade-off 3 uses "Fail-safe locks" / "Fail-secure locks"; Procedure A3 uses "magnetic lock, electric strike" with "Fail-safe/fail-secure designation" -- adopt a consistent terminology table | Terminology for lock hardware types and their fail-mode classification varies in phrasing across documents, creating potential for misinterpretation in the device schedule | Specification.md; Guidance.md; Procedure.md | REQ-AC-004; Trade-offs section; Step A3 | -- | Guidance.md (vocabulary note) | TBD |
| B-005 | B:wisdom:necessity | RationaleGap | Guidance | Guidance | Add rationale addressing what happens if the Owner does not elect this option at award: are rough-in provisions included in base scope to preserve future retrofit feasibility, or is no provision made? | Guidance discusses the election decision but does not address the consequence of non-election -- whether conduit rough-in should still be included in base scope as a future-proofing measure; this is a consequential design decision | Guidance.md | Considerations -- Integration with Building Electrical and IT | -- | Guidance.md | TBD |

---

## Matrix C -- Formulation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| C:normative:necessity | normative | necessity | enforceable obligation | 1 | HAS_ITEMS | Obligation enforceability weakened by assumption tagging |
| C:normative:sufficiency | normative | sufficiency | compliance sufficiency | 0 | NO_ITEMS | Compliance framework is present, sufficient for proposal stage |
| C:normative:completeness | normative | completeness | exhaustive regulatory coverage | 1 | HAS_ITEMS | Missing fire code cross-reference |
| C:normative:consistency | normative | consistency | regulatory coherence | 0 | NO_ITEMS | Regulatory references are coherent across documents |
| C:operative:necessity | operative | necessity | operational prerequisite | 0 | NO_ITEMS | Prerequisites listed in Procedure are adequate |
| C:operative:sufficiency | operative | sufficiency | operational readiness | 0 | NO_ITEMS | Procedure provides sufficient operational readiness steps |
| C:operative:completeness | operative | completeness | comprehensive execution | 0 | NO_ITEMS | Phase A and B cover proposal through closeout |
| C:operative:consistency | operative | consistency | repeatable execution | 0 | NO_ITEMS | Steps are consistently structured and repeatable |
| C:evaluative:necessity | evaluative | necessity | intrinsic value criterion | 0 | NO_ITEMS | Value criteria established in Guidance Purpose |
| C:evaluative:sufficiency | evaluative | sufficiency | justified merit | 0 | NO_ITEMS | Merit justification is adequate for optional item framing |
| C:evaluative:completeness | evaluative | completeness | holistic appraisal | 1 | HAS_ITEMS | No appraisal of accessibility impact |
| C:evaluative:consistency | evaluative | consistency | principled valuation | 0 | NO_ITEMS | Valuation principles are consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C-001 | C:normative:necessity | WeakStatement | Specification | Specification | Strengthen REQ-AC-006 Integration requirement: currently prefixed with "ASSUMPTION" -- either confirm as a requirement based on standard practice or escalate to Owner for ruling | REQ-AC-006 (base building integration) is framed as an assumption rather than a confirmed enforceable obligation, yet integration coordination is essential for system function | Specification.md | REQ-AC-006 -- Integration with Base Building Systems | -- | Specification.md | TBD |
| C-002 | C:normative:completeness | MissingSlot | Specification | Specification | Add requirement or reference addressing Alberta Fire Code provisions for access-controlled doors on fire-separation paths (e.g., magnetic lock release on fire alarm, hold-open devices on fire doors) | Exhaustive regulatory coverage requires addressing fire code alongside building code for doors that serve both access control and fire separation functions; currently only building code egress is mentioned | Specification.md | REQ-AC-007 -- Code Compliance | -- | Specification.md | TBD |
| C-003 | C:evaluative:completeness | MissingSlot | Guidance | Guidance | Add consideration addressing accessibility impact: will access control hardware (readers, locks) affect barrier-free access for persons with disabilities (e.g., automatic door operators, reader mounting height per CSA B651)? | Holistic appraisal of the access control option should include its impact on accessibility compliance, which is a separate code requirement that intersects with door hardware changes | Guidance.md | Considerations section | -- | Guidance.md | TBD |

---

## Matrix F -- Requirements (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| F:normative:necessity | normative | necessity | mandatory compliance threshold | 1 | HAS_ITEMS | Threshold not quantified |
| F:normative:sufficiency | normative | sufficiency | regulatory verification capacity | 1 | HAS_ITEMS | Verification approach for standards compliance is generic |
| F:normative:completeness | normative | completeness | total conformance assurance | 0 | NO_ITEMS | Coverage is adequate for proposal-stage depth |
| F:normative:consistency | normative | consistency | uniform enforcement standard | 0 | NO_ITEMS | Enforcement standard is consistent across documents |
| F:operative:necessity | operative | necessity | critical process enabler | 0 | NO_ITEMS | Process enablers (prerequisites) are adequately stated |
| F:operative:sufficiency | operative | sufficiency | demonstrated capability | 1 | HAS_ITEMS | No DB qualification requirement stated |
| F:operative:completeness | operative | completeness | thorough implementation scope | 0 | NO_ITEMS | Implementation scope covered by Phase A and B |
| F:operative:consistency | operative | consistency | methodical consistency | 0 | NO_ITEMS | Steps are methodically consistent |
| F:evaluative:necessity | evaluative | necessity | core value determination | 0 | NO_ITEMS | Core value established in Guidance Purpose |
| F:evaluative:sufficiency | evaluative | sufficiency | sufficient value justification | 0 | NO_ITEMS | Value justification adequate for optional item |
| F:evaluative:completeness | evaluative | completeness | exhaustive worth account | 1 | HAS_ITEMS | No mention of warranty duration |
| F:evaluative:consistency | evaluative | consistency | stable valuation discipline | 0 | NO_ITEMS | Valuation framing is stable |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F-001 | F:normative:necessity | VerificationGap | Specification | Specification | Add measurable acceptance threshold for REQ-AC-001 Zoning Concept: define minimum criteria for what constitutes an adequate zoning concept (e.g., minimum number of distinct zone types, or coverage of all Functional Program rooms) | The mandatory compliance threshold for the zoning concept is stated as "review for adequacy" without defining what adequacy means in measurable terms | Specification.md | Verification table, REQ-AC-001 row | -- | Specification.md | TBD |
| F-002 | F:normative:sufficiency | VerificationGap | Specification | Specification | Add verification approach for confirming that the proposed system meets any applicable product certification standards (UL 294, CSA, ANSI/BHMA) -- currently verification table does not address product certification checks | Regulatory verification capacity requires a defined method to confirm equipment meets referenced standards; the Verification table addresses code compliance broadly but not product-level certification | Specification.md | Verification table; Standards table | -- | Specification.md | TBD |
| F-003 | F:operative:sufficiency | TBD_Question | Specification | Specification | Record TBD: Should the specification require the DB to demonstrate access control system design competence (e.g., prior project experience, qualified sub-trade, or manufacturer certification)? | Demonstrated capability for access control design and installation is not addressed; this is relevant because access control is a specialty sub-trade typically requiring manufacturer-certified installers | Specification.md | entire document scanned | -- | Owner | TBD |
| F-004 | F:evaluative:completeness | MissingSlot | Specification | Specification | Add requirement or note addressing warranty period for access control system components (manufacturer warranty and DB warranty period) -- currently only mentioned in Procedure B6 as "Transfer all warranties" without specifying duration | An exhaustive worth account requires stating expected warranty duration; Procedure references warranty transfer but neither Specification nor Datasheet specifies a minimum warranty period | Specification.md; Procedure.md | Documentation section; Step B6 | -- | Specification.md | TBD |

---

## Matrix D -- Objectives (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| D:normative:guiding | normative | guiding | definitive compliance directive | 0 | NO_ITEMS | Compliance direction is adequate given ASSUMPTION caveats |
| D:normative:applying | normative | applying | enforced verification practice | 1 | HAS_ITEMS | No field testing protocol defined |
| D:normative:judging | normative | judging | conclusive conformance ruling | 0 | NO_ITEMS | Conformance determination pathway exists through AHJ |
| D:normative:reviewing | normative | reviewing | systematic enforcement audit | 0 | NO_ITEMS | Audit mechanism exists via closeout review |
| D:operative:guiding | operative | guiding | decisive process direction | 0 | NO_ITEMS | Process direction is decisive for both phases |
| D:operative:applying | operative | applying | validated implementation | 1 | HAS_ITEMS | No integration test with base building systems |
| D:operative:judging | operative | judging | comprehensive performance ruling | 0 | NO_ITEMS | Performance assessment covered by commissioning |
| D:operative:reviewing | operative | reviewing | systematic process review | 0 | NO_ITEMS | Step A6 internal review is systematic |
| D:evaluative:guiding | evaluative | guiding | established value direction | 0 | NO_ITEMS | Value direction established in Guidance Purpose |
| D:evaluative:applying | evaluative | applying | justified merit delivery | 0 | NO_ITEMS | Merit delivery mechanism (separable pricing) is clear |
| D:evaluative:judging | evaluative | judging | conclusive merit verdict | 1 | HAS_ITEMS | No Owner decision criteria for election |
| D:evaluative:reviewing | evaluative | reviewing | disciplined quality audit | 0 | NO_ITEMS | Quality audit addressed through commissioning report |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D-001 | D:normative:applying | VerificationGap | Procedure | Procedure | Add a field testing protocol step in Phase B (between B4 and B5) specifying: door-by-door functional test checklist, credential read-range test, fail-safe/fail-secure confirmation under simulated power loss | Enforced verification practice requires a defined field testing protocol; Step B4 says "Test each controlled door" but does not specify a testing protocol or acceptance criteria | Procedure.md | Phase B: Step B4 -- Installation and Programming | -- | Procedure.md | TBD |
| D-002 | D:operative:applying | VerificationGap | Procedure | Procedure | Add integration test step in Phase B confirming access control system operates correctly with base building systems: network connectivity, emergency power switchover, fire alarm door release (if applicable) | Validated implementation requires confirming system-level integration, not just individual door operation; no integration test step exists in Phase B | Procedure.md | Phase B: Steps B4-B5 | -- | Procedure.md | TBD |
| D-003 | D:evaluative:judging | RationaleGap | Guidance | Guidance | Add guidance on what factors the Owner should consider when making the election decision (e.g., comparison to future retrofit cost, insurance implications, operational risk of no access control) | A conclusive merit verdict (Owner election) requires a decision framework; Guidance presents the option but does not explicitly outline decision criteria to support the Owner's go/no-go judgment | Guidance.md | Purpose section | -- | Guidance.md | TBD |

---

## Matrix X -- Verification (4x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| X:guiding:necessity | guiding | necessity | foundational directive authority | 0 | NO_ITEMS | Directive foundation is present via OSR and Functional Program |
| X:guiding:sufficiency | guiding | sufficiency | justified directive fitness | 0 | NO_ITEMS | Directives are fit for purpose at proposal stage |
| X:guiding:completeness | guiding | completeness | comprehensive directive scope | 1 | HAS_ITEMS | No directive on audit trail / event logging |
| X:guiding:consistency | guiding | consistency | coherent directive alignment | 0 | NO_ITEMS | Directives align coherently across documents |
| X:applying:necessity | applying | necessity | essential validated deployment | 1 | HAS_ITEMS | No deployment validation for credential management handover |
| X:applying:sufficiency | applying | sufficiency | sufficient deployment assurance | 0 | NO_ITEMS | Deployment assurance covered by commissioning steps |
| X:applying:completeness | applying | completeness | exhaustive implementation coverage | 0 | NO_ITEMS | Implementation coverage spans proposal through closeout |
| X:applying:consistency | applying | consistency | disciplined deployment standard | 0 | NO_ITEMS | Deployment standards are consistent |
| X:judging:necessity | judging | necessity | binding performance standard | 1 | HAS_ITEMS | No performance SLA or uptime requirement |
| X:judging:sufficiency | judging | sufficiency | justified adequacy finding | 0 | NO_ITEMS | Adequacy findings are justified through verification table |
| X:judging:completeness | judging | completeness | exhaustive adjudication | 0 | NO_ITEMS | Adjudication scope covers key requirements |
| X:judging:consistency | judging | consistency | consistent adjudicative standard | 0 | NO_ITEMS | Adjudicative standard is consistent across requirements |
| X:reviewing:necessity | reviewing | necessity | critical audit criterion | 0 | NO_ITEMS | Audit criteria present in Procedure verification table |
| X:reviewing:sufficiency | reviewing | sufficiency | adequate review assurance | 0 | NO_ITEMS | Review assurance is adequate |
| X:reviewing:completeness | reviewing | completeness | exhaustive review coverage | 1 | HAS_ITEMS | No periodic review or maintenance audit post-handover |
| X:reviewing:consistency | reviewing | consistency | uniform review discipline | 0 | NO_ITEMS | Review discipline is uniform |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| X-001 | X:guiding:completeness | MissingSlot | Multi | Specification | Add requirement addressing event logging and audit trail capability: system should log access events (granted, denied, forced entry) with timestamps for security review | Comprehensive directive scope should address audit trail functionality, which is a standard capability of access control systems and operationally important for a shared municipal facility; no document mentions event logging | Specification.md; Guidance.md | entire document scanned | -- | Specification.md | TBD |
| X-002 | X:applying:necessity | VerificationGap | Procedure | Procedure | Add a credential management handover step in Phase B (at B5 or B6): define who receives master credentials, how user credential enrollment is performed, and who is designated as system administrator | Essential validated deployment includes credential management handover to the Owner; Procedure B5 mentions "general user credential management" training but does not define the handover protocol for master/admin credentials | Procedure.md | Phase B: Step B5 -- Commissioning and Training | -- | Procedure.md | TBD |
| X-003 | X:judging:necessity | TBD_Question | Specification | Specification | Record TBD: Should the specification include a system availability/uptime requirement (e.g., 99.9% availability) given 24/7 Fire Department operations? | A binding performance standard for system reliability is absent; given the 24/7 operational context noted in Datasheet and Guidance, a system uptime expectation would be relevant | Specification.md; Datasheet.md | REQ-AC-006; Conditions -- 24/7 operations | -- | Owner | TBD |
| X-004 | X:reviewing:completeness | RationaleGap | Guidance | Guidance | Add guidance on recommended post-handover maintenance and periodic review schedule for the access control system (e.g., annual credential audit, firmware updates, battery replacement schedule) | Exhaustive review coverage should extend to post-occupancy; Guidance and Procedure address commissioning and closeout but not ongoing maintenance expectations that the Owner should plan for | Guidance.md; Procedure.md | entire document scanned | -- | Guidance.md | TBD |

---

## Matrix E -- Evaluation (3x4)

### Lens Coverage

| LensKey | RowLabel | ColLabel | LensValue | ItemCount | CoverageStatus | Notes |
|---|---|---|---|---:|---|---|
| E:normative:necessity | normative | necessity | compulsory compliance foundation | 0 | NO_ITEMS | Foundation is present through OSR and code references |
| E:normative:sufficiency | normative | sufficiency | confirmed regulatory sufficiency | 1 | HAS_ITEMS | Regulatory sufficiency not confirmed for all standards |
| E:normative:completeness | normative | completeness | absolute regulatory assurance | 0 | NO_ITEMS | Covered sufficiently for proposal-stage depth with ASSUMPTION caveats |
| E:normative:consistency | normative | consistency | uniform compliance discipline | 0 | NO_ITEMS | Compliance discipline is uniform across documents |
| E:operative:necessity | operative | necessity | essential operational mandate | 0 | NO_ITEMS | Operational mandates are clear |
| E:operative:sufficiency | operative | sufficiency | confirmed operational sufficiency | 0 | NO_ITEMS | Operational sufficiency confirmed through procedure steps |
| E:operative:completeness | operative | completeness | total operational verification | 1 | HAS_ITEMS | Cybersecurity not addressed |
| E:operative:consistency | operative | consistency | consistent operational discipline | 0 | NO_ITEMS | Operational discipline is consistent |
| E:evaluative:necessity | evaluative | necessity | fundamental merit authority | 0 | NO_ITEMS | Merit authority established through Owner election mechanism |
| E:evaluative:sufficiency | evaluative | sufficiency | validated worth sufficiency | 0 | NO_ITEMS | Worth sufficiency validated through separable pricing approach |
| E:evaluative:completeness | evaluative | completeness | comprehensive worth assessment | 1 | HAS_ITEMS | No comparison benchmark |
| E:evaluative:consistency | evaluative | consistency | stable merit discipline | 0 | NO_ITEMS | Merit discipline is stable and consistent |

### Warranted Items

| ItemID | LensKey | Type | AppliesToDoc | SuggestedEditDoc | CandidateInfo | WhyWarranted | SourcePath | SectionRef | Contenders | ProposedAuthority (PROPOSAL) | HumanRuling |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-001 | E:normative:sufficiency | Normalization | Multi | Multi | Normalize the ASSUMPTION tagging pattern: some requirements (REQ-AC-006, REQ-AC-007, REQ-AC-008) are prefixed "ASSUMPTION" while others (REQ-AC-001 through REQ-AC-005) are not; create a consistent mechanism to distinguish confirmed vs. unconfirmed requirements | Confirmed regulatory sufficiency requires clarity on which requirements are confirmed and which remain assumptions; the current mixed tagging pattern could lead to assumption-tagged requirements being treated as optional during implementation | Specification.md; Datasheet.md | REQ-AC-006, REQ-AC-007, REQ-AC-008; Attributes and Conditions tables | -- | Specification.md | TBD |
| E-002 | E:operative:completeness | WeakStatement | Specification | Specification | Add requirement or consideration addressing cybersecurity for the access control system: network-connected panels and management interfaces introduce cybersecurity risk that should be acknowledged (e.g., encrypted communications, secure network segment, default credential changes) | Total operational verification should address cybersecurity; REQ-AC-006 mentions "Network/data connectivity for system management interface" but no document addresses cybersecurity provisions for the access control system | Specification.md | REQ-AC-006 -- Integration with Base Building Systems | -- | Specification.md | TBD |
| E-003 | E:evaluative:completeness | Normalization | Datasheet | Datasheet | Add a comparative sizing attribute: approximate system scale (e.g., estimated number of controlled doors, number of credential holders) to give Owner a quantitative basis for evaluating the price against comparable municipal access control installations | Comprehensive worth assessment requires some quantitative basis for the Owner to evaluate whether the proposed price represents fair value; currently no quantitative scale indicator exists beyond "multiple zones" | Datasheet.md | Attributes table | -- | Datasheet.md | TBD |
