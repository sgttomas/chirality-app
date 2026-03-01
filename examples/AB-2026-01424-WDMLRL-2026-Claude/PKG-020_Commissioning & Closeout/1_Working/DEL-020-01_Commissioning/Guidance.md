# Guidance — DEL-020-01: Building Systems Commissioning

**Document Type:** Guidance (directional)
**Deliverable ID:** DEL-020-01_Commissioning
**Package:** PKG-020 — Commissioning & Closeout
**Generated:** 2026-02-26 (Pass 1+2, P1_P2 run)
**Enriched:** 2026-02-26 (Pass 3, Semantic Lensing)

---

## Purpose

DEL-020-01 exists to ensure that the completed West Dried Meat Lake Regional Landfill Maintenance Shop Addition is not merely constructed, but is operationally ready — that all building systems work as designed, that County staff can operate and maintain them, and that the Owner receives documented evidence of this readiness.

Commissioning is the bridge between construction completion and facility occupancy. In the context of a design-build contract (CCDC 14–2013), the Proponent holds full responsibility for design, construction, and commissioning. This means the Proponent must not only build systems that meet specifications but must verify, test, document, and train on them before the facility passes to the Owner.

The deliverable directly supports:
- **OBJ-001** (code-compliant, fully functional facility): commissioning is the final verification that OBJ-001 has been achieved in the mechanical, electrical, and plumbing domains.
- **OBJ-002** (completion by December 31, 2026): commissioning must be planned and executed within the project schedule.
- **OBJ-004** (mechanical, plumbing, water systems operational readiness): commissioning is the operational readiness gate for these systems.
- **OBJ-005** (electrical and low-voltage systems operational readiness): commissioning is the operational readiness gate for these systems.

Sources: `_CONTEXT.md` Linked Objectives; Decomposition §5 OBJ-001, OBJ-002, OBJ-004, OBJ-005; Decomposition §7 DEL-020-01.

---

## Principles

### 1. Commission to design intent, not just to function

The standard for commissioning is not "does it turn on" but "does it perform as designed." Each system should be tested against its design parameters (flow rates, capacities, loads, temperatures, ventilation rates). ASSUMPTION: design parameters will be established in IFC documents from PKG-003 (mechanical), PKG-004 (electrical), and PKG-006 (plumbing) design packages.

### 2. Plan before testing

Commissioning is most effective when approached systematically from a written plan. A Commissioning Plan developed before testing begins — not discovered during testing — enables methodical coverage of all systems, clear assignment of responsibilities, and pre-agreed acceptance criteria. This avoids disputes at the acceptance stage. The Commissioning Plan is now a formal requirement (see Specification REQ-020-01-003A).

### 3. Sequence matters: construction complete before commissioning begins

Commissioning results are only meaningful if the system being tested is fully and correctly installed. Starting commissioning before construction is complete introduces rework, re-testing, and schedule risk. The declared upstream dependency on PKG-019 (construction management and QC sign-off) must be respected as a hard gate.

Source: `_DEPENDENCIES.md`; Decomposition PKG-020.

### 4. Owner coordination is required, not optional

The RFP explicitly requires coordination of inspections through the County project manager (RFP §3.1). Owner representatives should be involved in key acceptance milestones, not just informed after the fact. This supports the Owner's ability to observe and validate commissioning outcomes.

Source: RFP §3.1; REQ-020-01-011.

### 5. Documentation is part of the deliverable

Commissioning is not complete when the systems pass tests — it is complete when the evidence of those tests, and the knowledge to operate the systems, has been transferred to the Owner. O&M manuals, training records, and commissioning reports are deliverable artifacts, not optional extras.

Source: `_CONTEXT.md` Scope Definition; `_CONTEXT.md` Success Criteria.

---

## Considerations

### Schedule Pressure

The December 31, 2026 completion deadline (RFP §3.1; SOW-0091) is a hard contractual obligation. Commissioning is a late-stage activity that is vulnerable to schedule compression when construction runs long. Key considerations:

- Allow adequate commissioning time in the project schedule (TBD — depends on system complexity and contractor experience).
- Identify long-lead commissioning activities (e.g., crane load testing which may require specialized equipment or inspectors) early in project planning.
- Coordinate commissioning scheduling with the County project manager to ensure Owner availability for acceptance milestones.

ASSUMPTION: Adequate commissioning duration for an industrial facility of this scale and system complexity is at minimum several weeks. Specific duration is TBD pending Commissioning Plan.

**Note [B-003]:** Schedule risk for commissioning has not been quantified. A quantified schedule risk assessment should estimate (a) minimum commissioning duration based on system count and complexity, and (b) available float between expected construction completion and the December 31, 2026 deadline. Without quantifying the available commissioning window, schedule decisions lack a factual basis. This assessment requires the project schedule (once developed) as input. (Source: Guidance.md Considerations — Schedule Pressure; _SEMANTIC_LENSING.md B-003. ProposedAuthority: Project schedule — once developed.)

### Commissioning Agent Assignment

The `_STATUS.md` Outstanding Items list notes that Commissioning Agent assignment is still required. The Commissioning Agent is the responsible party for directing and managing commissioning activities. Early assignment is critical to allow the Commissioning Agent to:
- Review design documents during construction
- Develop the Commissioning Plan
- Coordinate pre-commissioning checks with trade contractors

Without an assigned Commissioning Agent, commissioning planning cannot proceed effectively. The Commissioning Agent must meet the qualification requirements established in Specification REQ-020-01-014.

Source: `_STATUS.md` Outstanding Items; Specification REQ-020-01-014.

### System Interdependencies

Several systems have interdependencies that affect commissioning sequence:

- Electrical systems must be energized before HVAC, plumbing pumps, cranes, and lighting can be functionally tested.
- Plumbing rough-in must be complete and pressure-tested before cistern fill and pump testing can occur.
- Crane installation and structural completion must be confirmed before load testing can proceed.
- Wash bay drainage and mud sump must be complete before wash bay commissioning.

ASSUMPTION: A commissioning sequence (system-by-system test order) should be established in the Commissioning Plan to manage these dependencies. The above ordering is inferred from standard industrial commissioning practice and the system descriptions in RFP §3.4.

### Crane Load Testing

The two 5-tonne overhead cranes represent a safety-critical commissioning item. Load testing of overhead cranes in Alberta is subject to specific safety code requirements. This testing:
- May require specialized equipment (test weights or calibrated load cells)
- May require a certified third-party inspector or Alberta Safety Codes Officer
- Should be scheduled with adequate lead time

Specific regulatory requirements are TBD (applicable Alberta Safety Code edition and section not cited in accessible sources — location TBD). See also Specification Note [C-001].

### Performance Criteria Definition

The RFP states that systems must be "commissioned and tested per specifications" and "performance criteria met or exceeded" (`_CONTEXT.md` Success Criteria), but the specific performance criteria per system are not detailed in the RFP or decomposition beyond the design parameters in RFP §3.4. Measurable acceptance criteria for each system (e.g., achieved HVAC air exchange rate, measured cistern pump flow rate in LPM, crane rated load confirmation) must be:
1. Derived from IFC design documents once complete.
2. Agreed with the Owner prior to testing.
3. Documented as part of the Commissioning Plan.

This is a known gap that must be resolved during design completion. Failure to establish criteria before testing risks acceptance disputes.

### Operator Training

The facility will be operated by County staff. Effective operator training requires:
- Identification of which County staff will operate/maintain each system
- Training content appropriate to operator skill level
- Adequate time for training before occupancy (not a last-minute activity)
- Documented evidence of training completion
- Verification of training effectiveness beyond attendance records (see Specification Note [E-002])

Who will conduct operator training is TBD — could be the Commissioning Agent, trade subcontractors, or equipment suppliers, depending on system complexity.

Source: `_CONTEXT.md` Scope Definition; MEMORY.md "Questions for Future Resolution."

### Seasonal Commissioning Considerations

**Note [C-003]:** Commissioning will likely occur in late 2026 (fall/winter) given the December 31 deadline and the dependency on construction completion. HVAC systems tested during cold weather may perform differently in summer conditions. Considerations:

- HVAC heating performance verified during winter commissioning may not reflect summer ventilation/cooling performance (if cooling is provided — TBD per design).
- The high volume air exchanger performance may vary with seasonal temperature differentials.
- Whether any post-commissioning seasonal performance verification is warranted during the 2-year guarantee period (RFP §2.10) should be considered.

ASSUMPTION: A seasonal re-verification provision, if warranted, would fall under the guarantee period obligations (PKG-021) rather than the initial commissioning scope. The Owner should determine whether seasonal performance monitoring is expected. (Source: _SEMANTIC_LENSING.md C-003. ProposedAuthority: Owner expectations; guarantee period provisions RFP §2.10.)

### Independent Verification

**Note [F-001]:** All commissioning verification is currently performed by the Commissioning Agent, with no independent validation layer specified except possible Safety Codes Officer involvement for cranes. For an industrial facility with safety-critical systems (cranes, electrical distribution, emergency showers), independent third-party verification may be warranted for select systems. Whether an independent commissioning authority review is required or recommended should be determined based on:

- Owner requirements and expectations
- CCDC 14-2013 provisions for independent verification
- System safety criticality (crane load testing is the most likely candidate)

ASSUMPTION: Independent third-party verification is not explicitly required by the RFP but may be warranted based on Owner risk tolerance. This is a project governance decision. (Source: _SEMANTIC_LENSING.md F-001. ProposedAuthority: CCDC 14-2013 provisions; Owner requirements.)

---

## Trade-offs

### Thoroughness vs. Schedule

More thorough commissioning (extended test durations, multiple test cycles, detailed performance trending) provides higher confidence in system performance but requires more time. Given the fixed December 31, 2026 deadline, the Commissioning Plan must balance thoroughness with schedule practicality.

PROPOSAL: Prioritize systems with the highest safety or operational criticality (cranes, cistern/pump for water supply, electrical distribution) for the most rigorous testing. Envelope systems (doors, lighting) can be verified by functional check.

### Commissioning Agent: Dedicated vs. Embedded in PM Role

The `_CONTEXT.md` lists "Commissioning Agent / PM" as the responsible party, suggesting the PM may assume commissioning responsibilities. A dedicated Commissioning Agent independent of construction management provides better objectivity in acceptance testing. Embedding commissioning in the PM role reduces cost but may reduce rigor.

PROPOSAL: If a dedicated Commissioning Agent is not engaged, the PM should establish a formal checklist-based protocol and engage trade foremen for system-specific testing, with County PM participation in key sign-offs. This is an ASSUMPTION of best practice — the human should confirm the intended approach. See also Specification REQ-020-01-014 (Commissioning Agent qualifications).

### Documentation Scope

Minimal documentation (test checklists and a one-page summary) satisfies the literal RFP requirement but may not serve the Owner's long-term operational needs. More comprehensive documentation (system-level O&M manuals, training videos, commissioning binders) is more useful but costs more time and effort to produce.

PROPOSAL: Confirm Owner expectations for documentation scope and format at project award.

### Dispute Resolution for Commissioning Acceptance

**Note [D-001]:** No dispute resolution mechanism is currently defined for commissioning acceptance disagreements. Given that:
- Acceptance criteria are largely TBD,
- The Commissioning Agent may be embedded in the PM role (reducing independence), and
- The Owner acceptance process is undefined (see Specification Note [F-003]),

the potential for disputes over whether a system has "passed" commissioning is elevated. Guidance:

- CCDC 14-2013 includes general dispute resolution provisions that may apply to commissioning acceptance disputes (specific section — location TBD).
- If the Owner and Proponent disagree on system acceptance, the ruling authority should be identified in advance (e.g., independent third party, contract administrator, or specific CCDC 14-2013 mechanism).
- Pre-agreeing acceptance criteria in the Commissioning Plan (per REQ-020-01-003A) is the primary risk mitigation for acceptance disputes.

ASSUMPTION: CCDC 14-2013 dispute resolution provisions apply to commissioning acceptance disputes unless the project agreement specifies otherwise. (Source: _SEMANTIC_LENSING.md D-001. ProposedAuthority: CCDC 14-2013 dispute resolution provisions.)

---

## Examples

ASSUMPTION: The following examples illustrate how commissioning might be structured for key systems on this project. They are drawn from standard industrial commissioning practice, not from a project-specific source.

### Example: Cistern and Pump Commissioning Sequence (ASSUMPTION — illustrative)

1. Verify cistern tank installation complete and passed pressure test.
2. Fill cistern with water supply; confirm capacity (50,000 L minimum).
3. Start pump; measure flow rate at fill connection (target: 100 LPM per RFP §3.4).
4. Verify 2.5 inch fill connection operates correctly.
5. Test automatic shutoff or float controls (if applicable — TBD per design).
6. Document results; obtain County PM sign-off.

### Example: Overhead Crane Commissioning Sequence (ASSUMPTION — illustrative)

1. Confirm structural crane supports and rail installation complete.
2. Confirm electrical power to crane circuits energized and tested.
3. Functional test: crane travel (bridge and trolley), hoist raise/lower, limit switches.
4. Load test: apply test load per Alberta Safety Code requirements (specific protocol TBD).
5. Confirm operator training on safe crane operation.
6. Document results; obtain Safety Codes Officer sign-off if required (TBD).

---

## Conflict Table (for human ruling)

No unresolvable conflicts identified at Pass 1+2 or Pass 3. The following items are flagged as gaps requiring resolution rather than conflicts between sources:

| Item ID | Gap Description | Source(s) | Impacted Sections | Proposed Resolution | Human Ruling |
|---|---|---|---|---|---|
| GAP-020-01-001 | Specific performance acceptance criteria per system are not defined in RFP or decomposition; only high-level design parameters are available | RFP §3.4; `_CONTEXT.md` Success Criteria | Specification REQ-020-01-004 through REQ-020-01-008; Procedure verification steps | Derive from IFC design documents; confirm with Owner before testing | TBD |
| GAP-020-01-002 | Commissioning Agent has not been assigned; responsible party role undefined in practice | `_STATUS.md` Outstanding Items; `_CONTEXT.md` Key Roles | All REQs; Procedure all steps; Specification REQ-020-01-014 | Assign Commissioning Agent as early priority action; define qualifications per REQ-020-01-014 | TBD |
| GAP-020-01-003 | Duration for commissioning activities is not specified; schedule risk vs. Dec 31, 2026 deadline is unquantified | RFP §3.1; SOW-0091 | Procedure Step 1 (scheduling); Guidance Note [B-003] | Develop commissioning schedule as part of overall project schedule at project award; quantify schedule risk | TBD |
| GAP-020-01-004 | Operator training format, content, and provider not defined | `_CONTEXT.md` Scope Definition; MEMORY.md | Specification REQ-020-01-009; Procedure Step 10 | Confirm with County at project award: who trains, what systems, what documentation | TBD |
| GAP-020-01-005 | Applicable Alberta Safety Code sections for crane load testing not identified in accessible sources | RFP §3.3.2 (general Safety Codes reference) | Specification REQ-020-01-008; Procedure Step 4; Note [C-001] | Identify applicable code during design phase; include in Commissioning Plan | TBD |
| GAP-020-01-006 | Fire protection systems: not mentioned in any source — unclear if provided | RFP §3.4 (not mentioned); Alberta Building Code | Specification In Scope (Note [C-002]); Datasheet Building Systems | Confirm with IFC design documents; document scope determination | TBD |
| GAP-020-01-007 | Old North Shop renovation scope: unclear if renovation-area systems require commissioning | RFP §3.1, §3.4 | Datasheet Facility Context (Note [B-002]) | Confirm scope with reference to RFP renovation sections | TBD |
| GAP-020-01-008 | Owner acceptance process for commissioning results undefined | CCDC 14-2013; RFP §2.14 | Specification REQ-020-01-011 (Note [F-003]); Procedure Step 11 | Define acceptance mechanism in Commissioning Plan or project agreement | TBD |
| GAP-020-01-009 | Commissioning dispute resolution mechanism undefined | CCDC 14-2013 | Guidance Trade-offs (Note [D-001]); Specification REQ-020-01-011 | Identify ruling authority from CCDC 14-2013 provisions | TBD |
