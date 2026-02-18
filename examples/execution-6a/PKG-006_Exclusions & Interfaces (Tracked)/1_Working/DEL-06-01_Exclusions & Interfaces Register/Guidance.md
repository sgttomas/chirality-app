# Guidance: DEL-06-01 Exclusions & Interfaces Register

---

## Purpose

The Exclusions & Interfaces Register exists to establish and maintain a clear, documented boundary between what this Design-Build contract covers and what it does not. It serves three functions:

1. **Prevent inadvertent inclusion**: Excluded items, once formally removed (e.g., by addendum), can drift back into scope through design decisions, pricing, or change orders if not actively tracked. This register is the control mechanism.
2. **Clarify interfaces**: Where this contract's scope ends and another system or procurement begins, the interface must be documented so both parties understand responsibilities, handoff conditions, and design coordination requirements.
3. **Audit trail**: The assumptions log and authority references provide a traceable record of why scope boundaries were drawn as they were, supporting change management and dispute resolution.

Source: Decomposition PKG-006 description ("Explicitly excluded scope items tracked to prevent inadvertent inclusion and to clarify interfaces with other Town procurements"); SOW-0400 note ("Track as out-of-scope to avoid inadvertent inclusion").

---

## Principles

### P1 — Exclusions are formal, not informal
An exclusion is only valid when backed by a formal authority: RFP clause, Addendum, or confirmed Owner direction. Informal understandings or verbal agreements do not constitute a valid exclusion. Each exclusion entry must cite its authority.

Source: Decomposition SOW-0400 row — authority cited as "Addendum 03 §1.2 (removal) vs OSR §10.2/§10.2.2."

### P2 — Exclusions must be distinguished from adjacent in-scope items
The most significant risk for this register is confusion between:
- **SOW-0400 (OUT)**: Pickled sand / sand-salt storage building — excluded from this procurement
- **SOW-0300–SOW-0304 (IN)**: Unheated cold storage building (60'×100') — in scope

These two structures may be located in proximity on site. Explicit documentation of their distinct scope status is required throughout design and construction.

Source: DEC-006 (Decomposition Decision Log); _CONTEXT.md Decision Reference.

### P3 — Interfaces are design coordination items, not exclusions
An interface is not the same as an exclusion. An interface describes where in-scope work meets another system. Good interface documentation includes: the in-scope element, what it interfaces with, the nature of the interface (spatial, structural, utility, operational), and who is responsible for each side of the interface.

Source: ASSUMPTION — derived from standard project controls practice; no specific RFP clause accessed.

### P4 — The register is living; it must be updated
A register that is not updated is worse than no register — it creates false confidence. The register must be updated whenever: scope changes occur, interfaces are confirmed or revised, or assumptions are resolved.

Source: ASSUMPTION — derived from decomposition OBJ-008 ("change management") and design milestone structure (SOW-0006).

### P5 — Objective OBJ-008 frames this register's purpose
OBJ-008 calls for "a safe, controlled Design-Build delivery: H&S, quality, schedule/reporting, permitting/inspections, change management, and value optimization." The exclusions/interfaces register is a change management and scope control tool in direct service of this objective.

Source: Decomposition OBJ-008 description; DEL-06-01 deliverable table entry.

---

## Considerations

### C1 — Cold Storage vs. Sand/Salt Storage: Site Spatial Interface
The pickled sand/salt storage building (SOW-0400, OUT) was part of the original site program (OSR §10.2/§10.2.2). Its removal from this procurement does not eliminate it from the Town's long-term site plan — the Town will procure it separately. This creates a latent site interface: the Design-Builder's cold storage building (SOW-0300–SOW-0304) and the future sand/salt shed may share:
- Site boundary / setback
- Grading and drainage patterns
- Access routes

The Design-Builder should consider the likely future location of the sand/salt shed when siting the cold storage building, even though the sand/salt shed is not in scope.

Source: Addendum 03 §1.2 (removal of SOW-0400); DEC-006; ASSUMPTION regarding site spatial relationship.

### C2 — Utility Tie-In Boundary (SOW-0110, INT-002)
Site utility tie-ins (SOW-0110) are treated as a cash allowance, excluded from the base price but still the Design-Builder's design coordination responsibility. The interface between the in-scope utility distribution network and the Town's existing infrastructure at the property boundary should be documented in this register as an interface (not an exclusion).

Source: Decomposition SOW-0110 note ("Cash allowance; excluded from base price; DB still coordinates/integrates design + execution"); DEC-004.

### C3 — Flood Hazard / Adjacent Subdivision Interface (INT-003)
The site is subject to flood hazard constraints shown in the Adjacent Subdivision Design exhibit (Addendum 03 §1.1). This is an interface between this contract's site works and the adjacent development/planning authority, requiring coordination to avoid prohibited development areas. This is tracked in PKG-003 (DEL-03-05) but is noted here as a site-level interface condition.

Source: Decomposition SOW-0114; Adjacent Subdivision Design exhibit (in `_Sources/references/`).

### C4 — Assumptions Log as Risk Management
The assumptions log is not merely administrative — it is a risk management tool. Open assumptions represent latent risks: if an assumption is wrong, the scope boundary may be incorrect. Tracking which assumptions are open and which have been confirmed allows the Design-Builder and Owner to identify and resolve boundary risks proactively.

**Risk escalation pathway (B-004):** When an assumption remains unresolved beyond the milestone at which it was expected to be confirmed, the Design-Builder SHALL escalate the assumption using the following mechanism:
1. Flag the assumption as "at risk" in the assumptions log with the missed resolution milestone noted.
2. Notify the Design-Builder PM, who SHALL raise the unresolved assumption at the next scheduled progress meeting (per DEL-01-05, Meetings, Documentation & Change Control).
3. If the assumption has cost, schedule, or scope boundary implications, the PM SHALL initiate a formal notification to the Owner per the change management process (DEL-01-05 Change Control Log).
4. If a project risk register exists (TBD -- confirm with Project Controls whether a formal risk register is maintained under DEL-01-05 or OBJ-008), the unresolved assumption SHALL be cross-referenced to the risk register with a risk rating commensurate with its potential impact on scope boundaries.

**Rationale for risk escalation linkage (B-004 enhancement):** The mechanism above connects unresolved assumptions to formal risk management because an unresolved scope-boundary assumption creates project risk — the Design-Builder and Owner may make different decisions based on conflicting assumptions, or an assumption that turns out to be wrong may require rework or scope adjustment. By formalizing the escalation pathway, the team ensures that scope-boundary assumptions receive the same risk governance as other project risks. This directly supports OBJ-008 (safe, controlled delivery with change management).

Source: ASSUMPTION -- derived from standard project controls practice and OBJ-008 ("change management"); Decomposition DEL-01-05 (Meetings, Documentation & Change Control).

---

## Trade-offs

### T1 — Breadth vs. Manageability of the Interface Matrix
**Tension**: Capturing every possible interface (even minor ones) vs. keeping the matrix concise and useful.
**Resolution**: Capture all interfaces that have design coordination implications, financial implications (allowances, scope handoffs), or regulatory/approval implications. Minor proximity adjacencies without coordination requirements do not need entries.
**Rationale**: A matrix that is too broad becomes noise; one that is too narrow misses real coordination needs. The standard should be: if the Design-Builder needs to do something differently because of this interface, it belongs in the matrix.

Source: ASSUMPTION — derived from project controls best practice; no specific RFP clause accessed.

### T2 — Register Format vs. Integration with Other Controls Documents
**Tension**: Maintaining a standalone register vs. integrating exclusions/interfaces into other management documents (e.g., change control log, design coordination matrix).
**Resolution**: This register exists as a dedicated document because its scope-boundary function is distinct from change tracking and design coordination. Cross-references to other controls documents (DEL-01-05 change control log; DEL-01-01 design coordination matrix) are appropriate, but the exclusions/interfaces register remains a separate artifact.
**Rationale**: A dedicated register ensures the exclusion list does not get buried within other documents where it might be overlooked during scope reviews. Source: Decomposition PKG-006 description (dedicated package for this function).

---

## Examples

### Example: Exclusion Entry Format (SOW-0400)

| SOW ID | Status | Description | Authority | Notes |
|---|---|---|---|---|
| SOW-0400 | OUT | Pickled sand / sand-salt storage building (and associated containment pad/drainage requirements) removed from this procurement; to be procured separately by the Town. | Addendum 03 §1.2; DEC-006 | Cold storage building (SOW-0300–SOW-0304) remains IN scope. |

Source: Decomposition SOW-0400 row; DEC-006.

### Example: Assumption Entry Format

| Assumption ID | Description | Basis | Status | Resolution Notes |
|---|---|---|---|---|
| ASM-001 | The future pickled sand/salt storage building (future Town procurement) will be sited to the east of the cold storage building, clear of the main building's emergency vehicle access routes. | Site plan review; ASSUMPTION — site layout not confirmed | Open | Confirm with Town during site planning phase |
| ASM-002 | The in-scope cold storage building (SOW-0300–SOW-0304) does not share a foundation, structural system, or utilities with the excluded sand/salt storage building. | DEC-006 (cold storage confirmed in scope as separate structure); ASSUMPTION | Open | Confirm during DD |

Note: ASM-001 and ASM-002 above are illustrative examples of the format. Specific assumptions will be populated during proposal development.

---

## Defined Status Vocabularies

**Interface Status Vocabulary (standardized per E-001):**
- **Open**: Interface identified but not yet confirmed; coordination requirements unclear or not yet documented.
- **Confirmed**: Both parties have acknowledged the interface; design coordination is in progress; responsibilities are documented.
- **Resolved**: Design coordination is complete; handoff conditions (if applicable) are documented; no further coordination required.
- **Transferred**: Interface responsibility has been formally transferred to another party (e.g., to Owner or to future procurement); Design-Builder no longer responsible for active management.
- **Closed**: Interface has been completed or formally closed at project closeout; no outstanding items remain.

Source: Specification REQ-06-01-004; _SEMANTIC_LENSING.md item E-001 (Normalization).

**Assumption Status Vocabulary (standardized per E-001):**
- **Open**: Assumption is recorded; underlying condition has not yet been confirmed or revised.
- **Confirmed**: Assumption has been verified as correct based on confirmatory evidence (e.g., Owner direction, site inspection, design output).
- **Revised**: Assumption has been updated based on new information; revised understanding is documented in Resolution Notes field.
- **Closed**: Assumption has been confirmed and acted upon; no further action required, or it has been formally superseded by another assumption or requirement.

Source: Specification REQ-06-01-005; _SEMANTIC_LENSING.md item E-001 (Normalization).

---

## Considerations for Register Effectiveness (Enhancement C-003)

A well-maintained register should prevent scope drift and manage interfaces effectively. To evaluate whether this register is fulfilling its purpose, the Design-Builder and Owner should consider the following effectiveness metrics at closeout:

- **Scope boundary incidents prevented**: Were there any instances during proposal or design development where an excluded item was nearly included, but the register caught it and prevented inadvertent inclusion?
- **Assumptions resolved**: Were open assumptions resolved by the expected milestones? For any unresolved assumptions, were they formally escalated per the C4 risk escalation pathway?
- **Interfaces successfully managed**: Were all documented interfaces actively managed during design and construction, with both parties confirming their responsibilities?
- **Zero scope creep from excluded items**: At closeout, confirm that no excluded items (particularly SOW-0400) appear in any final design, cost, or construction records.

These metrics help the Design-Builder and Owner assess the register's value and determine whether register practices should be continued on future projects.

Source: _SEMANTIC_LENSING.md item C-003 (MissingSlot); enhancement rationale: holistic valuation of register's worth.

---

## Upstream Dependencies and Functional Inputs (Enhancement X-002)

While `_DEPENDENCIES.md` does not declare formal upstream dependencies for this deliverable, the register depends on functional inputs from other deliverables to be populated and maintained. Understanding how to obtain these inputs in the absence of formal dependency declarations is important to the Design-Builder's execution plan.

| Input | Upstream Deliverable | Why Needed | How to Obtain |
|---|---|---|---|
| Confirmed scope ledger (IN/OUT status for all SOW items) | Decomposition; SOW ledger | Required to populate the exclusions list accurately; ensures no OUT items are missed | Review Decomposition SOW ledger and all Addenda/RFP amendments; cross-reference against current project scope status at each milestone |
| Site plan concept | DEL-03-01 (Site Plan, Circulation, Parking & Operational Layout) | Required to identify spatial interfaces (cold storage vs. future sand/salt shed siting; grading/drainage; access) | Request draft site plan from Civil discipline lead at each design phase; review for interface implications |
| Design coordination matrix or interface list | DEL-01-01 (Integrated Design Management & Submission Packages) | Required to cross-reference interface responsibilities and confirm all design disciplines have identified their interfaces | Request design coordination matrix / interface log from Project Manager or Design Coordinator at each milestone |
| Project Controls setup / change management process | DEL-01-05 (Meetings, Documentation & Change Control) | Required to integrate register reviews into the change management workflow; ensures scope boundary changes are captured | Confirm with Project Manager that register is reviewed at change control meetings; confirm change control log cross-references exclusions/interfaces register |

**Rationale:** Functional dependencies exist even when not formally declared. The Design-Builder PM should establish a protocol to systematically request these inputs at each design milestone (Proposal → DD → 60% → 100% → IFC → Closeout) to ensure the register is current and integrated into project controls.

Source: _SEMANTIC_LENSING.md item X-002 (RationaleGap); Procedure.md Prerequisites (Upstream Dependencies section).

---

## Conflict Table (for human ruling)

No conflicts identified at Pass 1+2. The register is internally consistent with the decomposition and decision log. If OSR §10.2/§10.2.2 text (not yet accessed) contains language that contradicts Addendum 03 §1.2, that conflict should be recorded here once the OSR is accessed.

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| — | No conflicts identified at this stage | — | — | — | — | — |
