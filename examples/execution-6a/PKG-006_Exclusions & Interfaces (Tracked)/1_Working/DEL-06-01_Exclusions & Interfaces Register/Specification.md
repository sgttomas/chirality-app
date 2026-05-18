# Specification: DEL-06-01 Exclusions & Interfaces Register

---

## Scope

### In Scope

This deliverable covers:

1. **Exclusions register** — a maintained list of all scope items formally removed from this procurement, with traceability to the authority source (RFP, Addendum, Owner direction).
2. **Interface matrix** — a tabular record of all significant interfaces between this contract scope and adjacent systems, procurements, or authorities.
3. **Assumptions log** — a structured record of assumptions underlying scope boundary decisions, with resolution status.
4. **Ongoing maintenance** — the register is a living document to be updated at each design and construction milestone.

### Out of Scope

- Physical design, construction, or pricing of excluded items (e.g., the pickled sand/salt storage building is NOT designed or priced by the Design-Builder under this contract).
- Decisions about future procurement timelines for excluded items (Town of Penhold responsibility).
- Any scope items marked IN across all other packages.

---

## Requirements

### REQ-06-01-001 — Exclusion Tracking
The Design-Builder SHALL maintain a register of all scope items formally excluded from this procurement.

- Currently required entry: SOW-0400 (Pickled sand / sand-salt storage building).
- Authority: Addendum 03 §1.2; DEC-006 (Decomposition Decision Log).
- Each entry SHALL include: SOW ID, status (OUT), description, authority reference, and notes.

### REQ-06-01-002 — No Inadvertent Inclusion
The Design-Builder SHALL ensure that excluded items are not included in the base contract scope, design, or pricing.

- ASSUMPTION: This requirement applies throughout proposal, design development, and construction phases.
- The exclusions register SHALL be referenced during scope reviews, design reviews, and change management processes to prevent scope creep from excluded items.
- **Acceptance criterion (A-002):** At each design milestone, the Design-Builder SHALL provide explicit written confirmation (sign-off) that excluded items (a) do not appear in design drawings, (b) are not included in cost estimates or pricing, and (c) are not referenced in specifications except as exclusion notes. A scope review that cannot demonstrate all three conditions is considered a fail. Source: Addendum 03 §1.2 ("Proponents should not include the pickled sand storage building in their proposals"); Specification REQ-06-01-001.

### REQ-06-01-003 — Interface Identification
The Design-Builder SHALL identify and document all significant interfaces between this contract scope and:
- Adjacent or future Town procurements (e.g., future pickled sand/salt storage procurement)
- Town utility infrastructure (at service boundaries)
- Adjacent site developments or constraints

- ASSUMPTION: Interfaces shall be documented as they are identified, with the register updated at each design milestone.

### REQ-06-01-004 — Interface Documentation Content
Each interface entry in the interface matrix SHALL include:
- Interface ID
- In-scope element (this procurement)
- Adjacent system/procurement
- Interface description
- Resolution status -- using the defined vocabulary: Open, Confirmed, Resolved, Transferred, Closed (see Guidance "Defined Status Vocabularies" for definitions) (E-001)

**Interface resolution criteria (D-002):** An interface entry is considered "Resolved" when: (a) both parties have confirmed their respective responsibilities, (b) design coordination for the interface is complete, and (c) handoff conditions (if applicable) are documented. Until all three conditions are met, the interface remains Open or Confirmed. Source: ASSUMPTION -- derived from standard project controls practice; to be confirmed with Owner.

### REQ-06-01-005 — Assumptions Log Maintenance
The assumptions log SHALL record:
- All assumptions underlying scope boundary decisions (e.g., assumptions about future procurement scope)
- Assumption ID, description, basis, status (using the defined vocabulary: Open, Confirmed, Revised, Closed -- see Guidance "Defined Status Vocabularies" for definitions) (E-001), and resolution notes

**Assumption resolution criteria (D-003):** An assumption is considered adequately resolved when: (a) the underlying condition has been confirmed or revised based on verifiable information (e.g., Owner direction, site confirmation, design development output), and (b) the resolution basis is documented in the Resolution Notes field. An assumption that cannot be confirmed or revised by the relevant milestone SHALL be escalated per the risk escalation pathway in Guidance C4. Source: ASSUMPTION -- derived from standard project controls practice; to be confirmed with Owner.

### REQ-06-01-006 — Cold Storage Confirmation
The Design-Builder SHALL explicitly confirm in the register that the unheated cold storage building (SOW-0300–SOW-0304, PKG-004) remains IN scope, distinguishing it from the excluded pickled sand/salt storage building.

- Authority: DEC-006; Decomposition SOW-0400 row note ("cold storage remains in scope").

### REQ-06-01-007 — Register Updates
The register SHALL be updated at the following milestones:
- Proposal submission
- Design Development milestone
- 60% Detailed Design review
- Any change event that affects scope boundaries

- ASSUMPTION (D-001): Update frequency derived from design milestone schedule per SOW-0006 / DEL-01-01 (Integrated Design Management). Authority basis for this update frequency is currently assumption-based; confirm with Project Controls or cite specific contract clause (e.g., RFP §7.1.8 design milestone schedule or CCDC 14-2013 supplementary conditions). Source: Decomposition SOW-0006; RFP §7.1.8 (location TBD).

**Version control requirement (X-001):** Each register update SHALL include a version number, revision date, and brief change description (change log). The register SHALL maintain a revision history table to support traceability across milestones. Source: ASSUMPTION -- derived from standard document control practice; consistent with Procedure Records table which references "versioned" artifacts.

### REQ-06-01-008 — Objective Alignment (OBJ-008)
The register supports OBJ-008 (safe, controlled Design-Build delivery including change management and value optimization). Scope boundary clarity is required to support effective change management.

- ASSUMPTION (PACKAGE_HEURISTIC): Association with OBJ-008 is confirmed by explicit decomposition mapping (SOW-0400 / PKG-006 row; OBJ-008 column in deliverable table).

---

## Standards

| Standard / Reference | Applicability | Accessibility | Confirmation Status |
|---|---|---|---|
| Addendum 03 §1.2 | Governing authority for SOW-0400 exclusion: "we are removing the Pickled Sand Storage building from the project and will be issuing a separate RFP in the future" | PDF in `_Sources/AB-2024-07156-Penhold_Public Services Building Addendum03.pdf` -- **text accessed and confirmed** | CONFIRMED |
| OSR (Appendix A) §10.2, §10.2.2 | Original scope reference superseded by Addendum 03; contains original scope that included sand/salt storage | PDF in `_Sources/` (location TBD -- not accessed). **TBD (B-002):** Obtain and review OSR text to confirm no conflict with Addendum 03 §1.2. | TBD -- text not accessed |
| RFP §7.3 (Documentation requirements) | General documentation obligations applicable to register maintenance | **ASSUMPTION (A-001):** likely applicable; location TBD. Prescriptive direction cannot be fully established until confirmed. | ASSUMPTION -- unconfirmed |
| CCDC 14-2013 (with Town supplementary conditions) | Contract basis; change management and scope management obligations | **ASSUMPTION (A-001, C-001):** likely applicable to scope management procedures. TBD: Confirm whether supplementary conditions contain specific scope management or exclusion-tracking obligations applicable to this register. To be confirmed by Human / Design-Builder legal. | ASSUMPTION -- unconfirmed |
| AHJ notifications (Alberta Building Code / municipal permits) | TBD: Consider whether formally excluding a structure from a permitted project triggers any AHJ notification or approval requirement (C-002) | ASSUMPTION: Applicability unknown. If the pickled sand storage was part of the original building permit application, its removal may require AHJ notification. | TBD -- to be investigated |

---

## Verification

| Requirement | Verification Approach | Pass/Fail Criteria (A-003) |
|---|---|---|
| REQ-06-01-001 (Exclusion tracking) | Review register at each milestone; confirm SOW-0400 entry present with authority reference. Cross-reference against complete SOW ledger (X-004) to confirm no other excluded items are missed. | **Pass:** All OUT items from SOW ledger are present in register with complete fields (SOW ID, status, description, authority, notes). Verification includes systematic check that all SOW items have been assessed for IN/OUT status and none are missing from either list. **Fail:** Any OUT item is missing or any required field is blank; any SOW item has not been assessed for scope status. |
| REQ-06-01-002 (No inadvertent inclusion) | Scope review at design milestones; cross-reference register against pricing and design scope. Explicit sign-off required (A-002). | **Pass:** Written confirmation that excluded items do not appear in (a) design drawings, (b) cost estimates/pricing, (c) specifications except as exclusion notes. **Fail:** Any excluded item found in drawings, pricing, or specifications without exclusion notation. |
| REQ-06-01-003 (Interface identification) | Review interface matrix at each milestone; confirm interfaces identified and documented | **Pass:** All known interfaces documented with required fields per REQ-06-01-004. **Fail:** A known interface is undocumented or missing required fields. |
| REQ-06-01-004 (Interface content) | Review each interface entry for completeness of required fields and use of defined status vocabulary | **Pass:** All five required fields populated; status uses defined vocabulary (Open/Confirmed/Resolved/Transferred/Closed). **Fail:** Any entry missing required fields or using undefined status terms. |
| REQ-06-01-005 (Assumptions log) | Review assumptions log at each milestone; confirm open assumptions are tracked and resolved per resolution criteria (D-003) | **Pass:** All assumptions have ID, description, basis, status (using defined vocabulary), and resolution notes where applicable. **Fail:** Any assumption missing required fields; any assumption flagged as unresolvable without escalation per C4 pathway. |
| REQ-06-01-006 (Cold storage confirmation) | Confirm cold storage (SOW-0300–SOW-0304) is present in active scope; confirm SOW-0400 is listed as OUT | **Pass:** Register explicitly states SOW-0300–SOW-0304 IN and SOW-0400 OUT with DEC-006 authority. **Fail:** Either entry missing or status incorrect. |
| REQ-06-01-007 (Register updates) | Confirm register version number, revision date, and change log entry align with milestone dates (X-001) | **Pass:** Register version date is within 5 business days of milestone date; change log entry present for each update. **Fail:** Version date does not correspond to a milestone or change log is absent. |
| REQ-06-01-008 (OBJ-008 alignment) | Change management process references register; scope reviews cite register | **Pass:** Evidence that change management procedures (DEL-01-05) reference this register; scope review minutes cite register review. **Fail:** No evidence of register integration into change management workflow. |

---

## Documentation

### Required Artifacts

| Artifact | Description | Responsible |
|---|---|---|
| Exclusions list | Table of all OUT scope items with authority references | Design-Builder |
| Interface matrix | Table of all identified interfaces between this contract and adjacent systems/procurements | Design-Builder |
| Assumptions log | Table of scope-boundary assumptions with status | Design-Builder |

### Submission

- Register artifacts are bundled within this 4-doc deliverable (DEL-06-01).
- Register is updated and resubmitted at each design milestone (Proposal → DD → 60% → 100% → IFC → Construction changes).
- ASSUMPTION: Register submission format (standalone document vs. embedded in other submissions) to be confirmed with Owner/Project Committee.
