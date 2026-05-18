# Datasheet: DEL-06-01 Exclusions & Interfaces Register

---

## Identification

| Field | Value |
|---|---|
| **Deliverable ID** | DEL-06-01 |
| **Name** | Exclusions & Interfaces Register |
| **Package** | PKG-006 — Exclusions & Interfaces (Tracked) |
| **Discipline** | Controls |
| **Type** | Controls register (4-doc bundle) |
| **Responsible Party** | Design-Builder |
| **Project** | Penhold Public Services Building (AB-2024-07156) |
| **RFP Reference** | AB-2024-07156-Penhold Public Services Building RFP_2024_004 |
| **Scope Coverage** | SOW-0400 |
| **Objective Support** | OBJ-008 |

---

## Attributes

### Register Format

| Attribute | Value |
|---|---|
| **Artifact Types** | Exclusions list; Interface matrix; Assumptions log |
| **Register State** | Active (tracked throughout proposal and delivery) |
| **Current Exclusion Count** | 1 (SOW-0400) |
| **Current Interface Count** | TBD -- to be determined during design development; expected to be populated at proposal submission (see Procedure Phase A, Step A3) |
| **Current Assumption Count** | TBD -- to be populated during proposal development; at minimum ASM-001 and ASM-002 should be recorded at proposal stage (see Guidance Examples and Procedure Phase A, Step A4) |

**Note (B-003 - Completeness Clarification):** The TBD counts above should be resolved no later than the proposal submission milestone. Specific timing expectations:
- **Interface Count**: To be determined during Design Development phase (once site plans and design concepts are available). Expected population: Proposal submission at the latest.
- **Assumption Count**: To be populated during proposal development. Initial expected count at proposal stage: minimum of 2 (ASM-001, ASM-002); final count TBD pending discovery of additional scope-boundary assumptions.
See Specification REQ-06-01-007 for milestone-based update schedule.

### Exclusions Register

| SOW ID | Status | Description | Authority | Notes |
|---|---|---|---|---|
| SOW-0400 | OUT | Pickled sand / sand-salt storage building (and associated containment pad/drainage requirements) removed from this procurement; will be procured separately by the Town. | Addendum 03 §1.2; DEC-006 | Cold storage building (SOW-0300–SOW-0304) remains IN scope. Do not include sand/salt shed or containment pad in base contract. |

### Interface Summary

**Interface Status Vocabulary:** Open | Confirmed | Resolved | Transferred | Closed. See Guidance section "Defined Status Vocabularies" for definitions.

| Interface ID | This Procurement (IN) | Adjacent Procurement / System | Interface Description | Status |
|---|---|---|---|---|
| INT-001 | Cold storage building (SOW-0300–SOW-0304) | Pickled sand/salt storage (future Town procurement) | Site boundary, grading, and drainage interface between cold storage building and future sand/salt shed location | Open -- confirm site layout coordination requirements during design |
| INT-002 | Site servicing / utility tie-ins (SOW-0110) | Town utility infrastructure | Utility stubs and service connections at property boundary; tie-ins treated as cash allowance | Open -- cash allowance; confirm stub locations with Town |
| INT-003 | Main building and site (PKG-002, PKG-003) | Adjacent subdivision development | Flood hazard constraints and site grading interface with adjacent subdivision design | Open -- Addendum 03 §1.1; Adjacent Subdivision Design exhibit |

### Assumptions Log (Initial Entries)

**Assumption Status Vocabulary:** Open | Confirmed | Revised | Closed. See Guidance section "Defined Status Vocabularies" for definitions.

| Assumption ID | Description | Basis | Status | Resolution Notes |
|---|---|---|---|---|
| ASM-001 | The future pickled sand/salt storage building (future Town procurement) will be sited to the east of the cold storage building, clear of the main building's emergency vehicle access routes. | Site plan review; ASSUMPTION -- site layout not confirmed | Open | Confirm with Town during site planning phase |
| ASM-002 | The in-scope cold storage building (SOW-0300–SOW-0304) does not share a foundation, structural system, or utilities with the excluded sand/salt storage building. | DEC-006 (cold storage confirmed in scope as separate structure); ASSUMPTION | Open | Confirm during DD |

**Note (B-001):** These entries are illustrative initial entries drawn from Guidance examples. Additional assumptions SHALL be identified and recorded during proposal development per Procedure Phase A, Step A4. Source: Guidance.md Examples section; Specification REQ-06-01-005.

---

## Success Metric

| Metric | Value | Status |
|---|---|---|
| **Register effectiveness measure under OBJ-008** | TBD -- Define quantitative or qualitative measure demonstrating the register has fulfilled its purpose (e.g., zero scope boundary incidents, all assumptions resolved by substantial completion). See Guidance P5 for OBJ-008 linkage. | TBD -- to be defined by Owner / Project Committee (E-002) |

---

## Conditions

| Condition | Value / Status |
|---|---|
| **Exclusion trigger** | Addendum 03 §1.2 — formal removal of pickled sand storage from procurement |
| **Prior scope reference** | OSR §10.2 / §10.2.2 — original scope included sand/salt storage |
| **Cold storage in scope** | CONFIRMED — SOW-0300–SOW-0304 remain in scope (DEC-006) |
| **Future procurement** | Town of Penhold will procure pickled sand storage separately (timing TBD) |
| **Impact on base pricing** | SOW-0400 excluded from base contract price |
| **Impact on optional items** | No optional items (SOW-0500–SOW-0506) affected by this exclusion |

---

## Construction

| Artifact | Description | Format | Expected Timing |
|---|---|---|---|
| Exclusions list | Tabular list of all scope items explicitly removed from this procurement, with authority references | Table in this register | Proposal submission; updated at each design milestone |
| Interface matrix | Tabular mapping of all interfaces between this contract scope and adjacent systems/procurements | Table in this register | Proposal submission; updated as interfaces are confirmed |
| Assumptions log | Log of assumptions underlying scope boundary decisions | Table in this register | Proposal submission; updated as assumptions are resolved or revised |

---

## References

| Reference | Location | Relevance |
|---|---|---|
| Addendum 03 §1.2 | `_Sources/AB-2024-07156-Penhold_Public Services Building Addendum03.pdf` | Formal removal of pickled sand/sand-salt storage from procurement |
| OSR (Appendix A) §10.2, §10.2.2 | `_Sources/` (location TBD — PDF not accessed) | Original scope that included sand/salt storage; superseded by Addendum 03 §1.2 |
| Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md — PKG-006 row; SOW-0400 row; DEC-006 | `_Decomposition/` | Decomposition authority for exclusion tracking and interface definition |
| DEC-006 | Decomposition §Decision Log | Decision record: pickled sand storage removed; cold storage confirmed in scope |
