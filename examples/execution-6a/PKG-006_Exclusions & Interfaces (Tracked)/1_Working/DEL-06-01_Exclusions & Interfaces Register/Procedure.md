# Procedure: DEL-06-01 Exclusions & Interfaces Register

---

## Purpose

This procedure describes:
1. How to **produce** the Exclusions & Interfaces Register during proposal and design development.
2. How to **maintain and operate** the register throughout the delivery lifecycle to ensure scope boundaries remain clear and controlled.

---

## Prerequisites

### References Required

| Reference | Purpose | Location |
|---|---|---|
| Addendum 03 §1.2 | Authority for SOW-0400 exclusion (pickled sand/salt storage removal) | `_Sources/AB-2024-07156-Penhold_Public Services Building Addendum03.pdf` |
| OSR (Appendix A) §10.2, §10.2.2 | Original scope reference for comparison; identifies what was superseded | `_Sources/` (location TBD — PDF not fully accessed) |
| Decomposition (Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md) | SOW ledger; PKG-006 description; DEC-006; OBJ-008 | `_Decomposition/` |
| Specification.md (this deliverable) | Requirements REQ-06-01-001 through REQ-06-01-008 | This deliverable folder |

### Upstream Dependencies

No upstream dependencies declared in `_DEPENDENCIES.md`. However, the following upstream inputs are functionally required:

| Input | Source | Notes |
|---|---|---|
| Confirmed scope ledger (IN/OUT status for all SOW items) | Decomposition; Addenda | Required to populate exclusions list; currently SOW-0400 is the only OUT item |
| Site plan concept | DEL-03-01 (Site Plan, Circulation and Parking) | Required to identify spatial interfaces |
| Design coordination matrix | DEL-01-01 (Integrated Design Management) | Required to cross-reference interface responsibilities |
| Project Controls setup | DEL-01-05 (Meetings, Documentation & Change Control) | Required to integrate register into change management workflow |

ASSUMPTION: Upstream dependency declarations in `_DEPENDENCIES.md` will be updated as design progresses.

### Personnel / Roles

| Role | Responsibility |
|---|---|
| Design-Builder PM | Overall register ownership; authorization of entries |
| Design Discipline Leads | Interface identification within their discipline |
| Design-Builder QA/QC | Review register at each milestone for completeness |

---

## Steps

### Phase A — Initial Register Setup (Proposal Phase)

**Step A1 — Populate the exclusions list from the scope ledger.**
- Review the full SOW ledger from the decomposition (or from the RFP/Addenda directly once accessed).
- Identify all items with status OUT.
- Confirm current OUT items: SOW-0400 (Pickled sand / sand-salt storage building, Addendum 03 §1.2).
- Enter each OUT item in the exclusions list with: SOW ID, status (OUT), description, authority reference, and notes.

**Step A2 — Confirm cold storage vs. sand/salt storage distinction.**
- Explicitly note in the exclusions list that SOW-0300–SOW-0304 (unheated cold storage building, 60'×100') remains IN scope.
- This step prevents the most probable inadvertent confusion between the two storage structures.
- Authority: DEC-006.

**Step A3 — Identify initial interfaces.**
- Review site plan concepts (when available) to identify spatial interfaces between in-scope and excluded/adjacent elements.
- Review utility coordination requirements (SOW-0110, cash allowance tie-ins) to identify utility interfaces.
- Populate the interface matrix with: Interface ID, in-scope element, adjacent system/procurement, interface description, status.
- Minimum expected interfaces at proposal stage: INT-001 (cold storage / future sand storage site interface); INT-002 (utility tie-in boundary); INT-003 (flood hazard / adjacent subdivision).

**Step A4 — Populate initial assumptions log.**
- Record all assumptions used to establish scope boundaries where the information is not explicitly confirmed.
- Assign each assumption an ID (ASM-XXX), description, basis, and status (Open).
- ASSUMPTION: At proposal stage, at minimum ASM-001 (future sand/salt shed siting) should be recorded.
- **Sourcing guidance (A-004 enhancement):** To systematically identify assumptions, the Design-Builder should:
  1. Review the scope boundaries identified in the decomposition, Addenda, and RFP to identify any scope edges that are not explicitly confirmed by a formal source.
  2. For each boundary edge, ask: "Is this scope boundary confirmed in a formal document, or are we making an assumption?" Examples:
     - Assumption about future sand/salt shed siting (not confirmed by site plan) → Record as ASM-001.
     - Assumption that cold storage will not share utilities with excluded sand/salt storage (inferred from DEC-006 but not explicitly detailed) → Record as ASM-002.
     - Assumption that utility stubs will be available at property boundary (cash allowance implies this, but tied-in location not confirmed) → Record as needed.
  3. For each assumption, record the basis (what drove the assumption?) and expected resolution milestone (when will we know if this assumption is correct?).
  4. This systematic approach ensures the assumptions log is comprehensive and supports proactive risk management per Guidance C4.

**Step A5 — Review register for completeness and consistency.**
- Confirm all required fields are populated (see REQ-06-01-001 through REQ-06-01-005).
- Cross-reference exclusions list against proposal pricing to confirm excluded items are not priced.
- Cross-reference exclusions list against concept design drawings (when available) to confirm excluded structures are not shown.
- **QA/QC sign-off requirement (A-005 enhancement):** Assign the Design-Builder's QA/QC representative to review the register for completeness before proposal submission. The QA/QC reviewer SHALL sign off on the register, confirming:
  1. All exclusions list entries are complete (SOW ID, status, description, authority, notes).
  2. All interface matrix entries are complete and use defined status vocabulary.
  3. All assumptions log entries are complete and use defined status vocabulary.
  4. No excluded items are inadvertently included in proposal pricing or drawings (cross-reference complete).
  5. The register is version-numbered and dated at the time of sign-off.
  6. A QA/QC sign-off record (e.g., initials, date, comment) is included in the Records table below, confirming review completion.

**Step A6 — Submit register as part of proposal package.**
- Include the register (Exclusions list + Interface matrix + Assumptions log) in the proposal submission.
- ASSUMPTION: Submission format (standalone document or embedded in a larger submission) to be confirmed with Owner.

---

### Phase B — Design Development Updates

**Step B1 — Review register at each design milestone.**
- At each design milestone (Design Development; 60% Detailed Design; 100% Detailed Design; IFC):
  - Confirm no new OUT items have arisen.
  - Confirm SOW-0400 remains out; cold storage building remains in scope.
  - Update interface matrix with any newly identified or confirmed interfaces.
  - Update assumptions log: mark assumptions as Confirmed or Revised if new information is available.

**Step B2 — Cross-reference with change control log.**
- Any proposed change order that affects scope boundaries must be reviewed against the exclusions/interfaces register before approval.
- If a proposed change would bring an excluded item into scope (e.g., if Owner requests the sand/salt storage building under this contract), the register must be updated with the new authority reference before the change is processed.
- Reference: DEL-01-05 (Change Control Log, Project Controls & Documentation).

**Step B3 — Discipline lead interface review.**
- At each design milestone, discipline leads (Civil, Structural, Mechanical, Electrical) confirm whether any new interfaces have been identified within their discipline.
- Update the interface matrix with confirmed interface details and resolution status.

---

### Phase C — Construction Phase Maintenance

**Step C1 — Monitor for scope boundary incidents.**
- During construction, monitor for any site activities that involve excluded scope items (e.g., any work related to pickled sand storage).
- If any such activity is identified, stop, document, and escalate to PM for review.
- **Escalation detail (F-002 enhancement):** The PM's next actions upon escalation SHALL include:
  1. Review the incident documentation and identify whether the activity was an inadvertent error, a proposed scope change, or an external factor (e.g., Town activity on adjacent land).
  2. If inadvertent error → Correct immediately; document the correction and root cause in the register's Revision History.
  3. If proposed scope change → Do NOT proceed; instead, initiate the formal change control process per DEL-01-05 (Change Control Log). Update this register only after the change has been formally approved and a new authority is added to the Standards section.
  4. If external factor → Document the nature of the external activity; assess whether it affects this contract's scope boundaries or interfaces; update the Interfaces matrix if needed.
  5. Notify the Design-Builder PM, who SHALL raise the incident and its resolution at the next scheduled progress meeting with the Owner.

**Step C2 — Resolve open assumptions.**
- As construction progresses and site conditions are confirmed, resolve open assumptions in the assumptions log.
- Mark each assumption as Confirmed, Revised, or Closed with supporting notes.

**Step C3 — Update register at construction milestones.**
- Update the register at significant construction milestones (e.g., site clearing, building envelope complete, substantial performance).
- Confirm all interfaces have been managed/resolved.

---

### Phase D — Closeout

**Step D1 — Final register review.**
- At closeout, confirm: all exclusions remain excluded from the final contract; all interfaces have been resolved or formally transferred to the appropriate party; all assumptions have been closed.
- **Explicit closeout verification (X-003 enhancement):** Before submitting the final register, verify the following:
  1. **All interface entries have reached a terminal status.** Each interface in the matrix SHALL have one of these statuses: Resolved, Transferred, or Closed. No interface should remain "Open" or "Confirmed" at closeout.
     - If an interface is still unresolved at closeout, the Design-Builder SHALL document the reason (e.g., "deferred to Owner for future procurement") and formally close it with a note explaining the deferral.
  2. **All assumption entries have reached a terminal status.** Each assumption SHALL have one of these statuses: Confirmed, Revised, or Closed. No assumption should remain "Open" at closeout.
     - If an assumption could not be confirmed by closeout (e.g., "future sand/salt shed siting still pending Town decision"), the Design-Builder SHALL document the assumption as "Closed (pending Owner)" with a note explaining the deferral and indicating the Owner's responsibility.
  3. **Exclusions list verification.** Cross-reference the final Exclusions list against the final contract scope, final design, and final cost estimates to confirm no excluded items appear.
  4. **Success metric assessment.** Complete the Success Metric section (Datasheet E-002) by documenting the effectiveness of the register in preventing scope drift and managing interfaces during the project lifecycle.

**Step D2 — Submit final register with closeout package.**
- Include the final register (Exclusions list + Interface matrix + Assumptions log) in the closeout documentation package (reference: DEL-01-07 — Commissioning, Training, Closeout & Warranty).
- ASSUMPTION: Register is included in As-Built documentation for future reference by the Town.

---

## Verification

| Check | How | When |
|---|---|---|
| Exclusions list is complete and accurate | Review against SOW ledger; confirm all OUT items are listed | Proposal; each design milestone; closeout |
| Excluded items are not priced or designed | Cross-reference register against proposal/design drawings and cost estimates | Proposal; each design milestone |
| Cold storage (IN) is not confused with sand/salt storage (OUT) | Confirm both structures are explicitly identified in register with correct status | Proposal; each design milestone |
| Interface matrix is current | Review against latest site plan and design drawings | Each design milestone |
| Assumptions log is current | Review open assumptions; confirm resolved assumptions are closed | Each design milestone; closeout |
| Register has been updated at each required milestone | Confirm version date and milestone reference on register | At each milestone |
| No excluded items re-introduced via change order | Cross-reference change control log against exclusions list | At each change event |

---

## Records

| Record | Description | Where Held |
|---|---|---|
| Exclusions list (versioned) | Table of all OUT scope items; version-controlled with dates and revision history | This deliverable folder; project document management system |
| Interface matrix (versioned) | Table of all identified interfaces; version-controlled with revision history | This deliverable folder; project document management system |
| Assumptions log (versioned) | Table of scope-boundary assumptions with status and resolution notes; version-controlled | This deliverable folder; project document management system |
| QA/QC sign-off record (A-005) | Design-Builder QA/QC review and approval of register completeness at each submission milestone | This deliverable folder; project document management system |
| Cross-reference to change control log | Record of any change events that affected scope boundaries | DEL-01-05 (Change Control Log) |
| Scope boundary incident log (F-002) | Record of any incidents during construction where excluded items nearly entered scope; includes escalation resolution | This deliverable folder; project document management system |
| Final register (closeout, X-003) | Final confirmed state of exclusions, interfaces, and assumptions; all interface statuses verified as terminal; all assumption statuses verified as terminal | Closeout package (DEL-01-07) |
| Register effectiveness assessment (C-003, E-002) | Post-closeout documentation of register effectiveness in preventing scope drift and managing interfaces; success metrics completed | Project archive / lessons learned documentation |
