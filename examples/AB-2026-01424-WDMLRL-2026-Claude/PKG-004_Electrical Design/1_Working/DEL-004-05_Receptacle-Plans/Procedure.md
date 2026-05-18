# Procedure — DEL-004-05 Receptacle Layout Plans

---

## Purpose

This procedure describes the steps for producing the Receptacle Layout Plans drawing set (DEL-004-05) to IFC quality. The output is a stamped, coordinated drawing set that locates and annotates all electrical receptacle outlets in the New North Shop addition, ready for permit submission and construction by the electrical contractor (PKG-015 / DEL-015-03).

---

## Prerequisites

### Reference Documents Required

| Item | Document | Status |
|---|---|---|
| Conceptual electrical drawing | R-05 — AB-2026-01424-Appendix B (Electrical).pdf | Available in _Sources/ |
| RFP design requirements | R-01 — AB-2026-01424-WDMLRL RFP.pdf S3.4 | Available in _Sources/ |
| Applicable electrical code | Alberta Safety Codes / CEC Part I | Must be obtained by Electrical Engineer — not in project sources |
| Architectural floor plan base | DEL-001-02 (Architectural Floor Plans) | Required upstream input — must be available before dimensioned layout can be produced |
| Preliminary electrical design approval | DEL-004-01 (Preliminary Electrical Design) — County-approved | Required per OBJ-003 / R-01 S3.3.2 |

### Upstream Deliverables (Declare Complete Before Proceeding to IFC)

| Deliverable | Why Needed | Expected Availability | Actual Availability |
|---|---|---|---|
| DEL-001-02 — Architectural Floor Plans | Provides dimensioned base for receptacle placement | TBD — per project schedule | TBD |
| DEL-004-01 — Preliminary Electrical Design | County approval of preliminary design required before final IFC issue | TBD — per project schedule | TBD |
| DEL-004-02 — Single-Line Diagram | Confirms service voltage, panel configuration, available circuits | TBD — per project schedule | TBD |
| DEL-004-03 — Power Distribution Plans | Coordination to avoid circuit conflicts with equipment power | TBD — per project schedule | TBD |

> **Enrichment (F-003):** Expected and actual availability date columns have been added to the upstream deliverables table. The Electrical Engineer or Project Manager shall record expected and actual receipt dates for each upstream input. This enables tracking of readiness status and provides early warning if upstream inputs are delayed. Source: standard project management practice; ASSUMPTION.

### Personnel / Qualifications

| Role | Qualification | Requirement Source |
|---|---|---|
| Electrical Engineer of Record | P.Eng. licensed in Province of Alberta | R-01 S3.3.2 |
| Electrical Designer / Drafter | Working under P.Eng. supervision | ASSUMPTION — standard practice |

### Tools / Software

| Item | Notes |
|---|---|
| CAD/BIM drafting software | TBD — Electrical Engineer's standard platform (see also Datasheet Construction section) |
| Code reference materials | CEC Part I current edition as adopted in Alberta — edition TBD (to be confirmed with AHJ per Specification REQ-005) |
| Architectural base drawing (electronic) | DEL-001-02 in compatible format |

---

## Steps

### Step 1 — Confirm Scope and County Input

**Timing constraint (D-002):** The scope confirmations in this step (items 1-3 below) shall be resolved before proceeding to Step 4 (drawing development). Steps 2 and 3 (obtaining and reviewing upstream inputs, establishing zones) may proceed in parallel with scope confirmation, but the Electrical Engineer shall not issue a drawing for internal review (Step 6) or preliminary submittal (Step 7) until all scope questions from this step are resolved or formally deferred with Project Manager approval.

1. Obtain County-supplied welding equipment specifications (R-01 S3.4 states "County to supply welding equipment specifications"). Confirm that 50 A/240 V is the correct rating (per D-009 assumption) or identify if a scope change is required. **Target receipt date: TBD — the Project Manager shall establish a deadline and escalation path for this input.**
2. Confirm with the project team whether the Old North Shop renovation (washroom, locker room, kitchenette) is included in this drawing set or addressed separately.
3. Confirm whether mezzanine receptacle coverage is required and what the intended use of the mezzanine will be.
4. Document all confirmations and any resulting scope adjustments.
> Source: R-01 S3.4; D-009; R-01 S3.1.

> **Enrichment (D-002):** A timing constraint has been added to clarify when Step 1 scope confirmations must be resolved relative to later steps. The original procedure listed scope questions but did not state when they must be answered, which could allow the design to proceed to IFC before scope questions are resolved. Source: standard design process practice; ASSUMPTION.

### Step 2 — Obtain and Review Upstream Inputs
1. Receive IFC-ready (or near-final) architectural floor plan base (DEL-001-02) for the new addition, confirmed dimensionally. Record actual receipt date in Prerequisites table.
2. Receive Single-Line Diagram (DEL-004-02) to confirm panel count, panel locations, and three-phase service configuration.
3. Receive Power Distribution Plans (DEL-004-03) to understand which circuits are dedicated to equipment and which are available for receptacle circuits.
> Source: OBJ-003; R-01 S3.3.2; ASSUMPTION — standard electrical drawing practice.

### Step 3 — Establish Layout Zones and Receptacle Program
1. Overlay the conceptual electrical drawing (R-05) on the architectural base to establish:
   - Zone boundaries (main shop bays, work bench, welding station, parts room, office, utility room, wash bay, mezzanine).
   - Initial receptacle placement per conceptual drawing as a starting point.
2. Develop a receptacle program listing each zone with:
   - Outlet type (15 A/120 V, 20 A/120 V, 20 A/240 V, 30 A/240 V, 50 A/240 V).
   - Preliminary count.
   - GFCI designation (wash bay minimum; review utility room and any other wet/damp locations — enumerate all qualifying locations per Specification REQ-004).
3. Verify that the receptacle program satisfies CEC Part I minimum requirements for the applicable occupancy classifications.
> Source: R-05 (App B-Elec); R-01 S3.4; CEC Part I (location TBD); ASSUMPTION.

### Step 4 — Develop Receptacle Layout Drawing(s)
1. Draft the receptacle layout on the architectural base, placing each outlet symbol at its planned location with correct symbol per legend.
2. Show all five receptacle types as defined in the legend (15 A, 20 A/120 V, 20 A/240 V, 30 A, 50 A).
3. Mark GFCI-protected outlets with appropriate notation.
4. Show mounting heights or provide a general note for mounting height standards (per Specification REQ-009).
5. Show panel designation and circuit number for each outlet or outlet group (coordinated with DEL-004-06), or reference DEL-004-06 for circuit assignments — per the circuit numbering convention determined by the Electrical Engineer (see Specification REQ-008 and Guidance Conflict Table CF-001).
6. Include an electrical legend on the drawing defining all receptacle symbols.
7. If AFCI or tamper-resistant receptacles are required per the Electrical Engineer's determination (Specification REQ-010), show appropriate notation.
> Source: R-05 (App B-Elec legend); REQ-001 through REQ-010 in Specification.md.

### Step 5 — Coordinate with Panel Schedules (DEL-004-06)
1. Assign each receptacle circuit to a specific panel circuit number (or confirm that DEL-004-05 references DEL-004-06 for this information — per the circuit numbering convention determined in Step 4.5).
2. Verify that the panel has sufficient breaker positions and ampacity for all receptacle circuits.
3. Verify three-phase load balance across receptacle circuits where practicable.
4. Cross-check that circuit numbers on the receptacle layout plan (if shown) match DEL-004-06 panel schedule entries.
> Source: R-01 S3.4 (three-phase power); ASSUMPTION — standard coordination practice.

> **Enrichment (F-004):** Steps 4.5 and 5.1 now reference the circuit numbering convention decision, aligning with the Specification REQ-008 enrichment and Guidance Conflict Table CF-001.

### Step 6 — Internal Quality Review
1. Engineer of Record reviews the drawing set against:
   - CEC Part I minimum receptacle coverage requirements for all occupancy types present.
   - GFCI requirements for wet/damp locations (all enumerated locations per REQ-004).
   - AFCI / tamper-resistant applicability determination (REQ-010).
   - Consistency with R-05 conceptual drawing (all five receptacle types represented; welding receptacles distributed per County intent).
   - Coordination with DEL-004-02, DEL-004-03, DEL-004-06.
   - Architectural coordination: confirm receptacle locations do not conflict with structural elements, door swings, or equipment clearances shown on DEL-001-02 (see Specification Verification — X-005).
2. **Intermediate quality gate (F-001):** Before applying P.Eng. stamp, the Electrical Engineer shall perform a documented self-check of the drawing against CEC Part I receptacle coverage rules. This self-check shall use a checklist covering at minimum:
   - All zones have receptacles of required types (REQ-003).
   - Wet/damp locations identified and GFCI-protected (REQ-004).
   - Code edition confirmed with AHJ (REQ-005).
   - Welding receptacle distribution meets quantitative threshold (REQ-002).
   - Mounting heights addressed (REQ-009).
   - AFCI / tamper-resistant determination documented (REQ-010).
   - Circuit numbers consistent with DEL-004-06 (REQ-008).
   - No conflicts with architectural elements (X-005).
   The completed checklist shall be retained as a QA record (see Records).
3. Resolve any discrepancies or TBD items identified during review.
> Source: R-01 S3.3.2; OBJ-003; CEC Part I (location TBD).

> **Enrichment (F-001):** An intermediate quality gate has been added. The original procedure relied solely on the P.Eng. stamp and AHJ permit as evidence of code compliance, with no documented intermediate QA step. The checklist provides traceability of the self-check. Source: R-01 S3.3.2 (code compliance required); standard engineering QA practice — ASSUMPTION.

### Step 7 — Preliminary Design Submission (if not yet approved)
1. If County approval of preliminary electrical design (DEL-004-01) has not yet been obtained, include receptacle layout in the preliminary submittal package. See Guidance Considerations (Phasing of Drawing Production) for guidance on level of detail expected at preliminary stage.
2. Address any County review comments before proceeding to IFC stamp.
> Source: R-01 S3.3.2; OBJ-003.

### Step 8 — P.Eng. Stamp and IFC Issue
1. **Pre-stamp checklist (A-004):** Before applying P.Eng. stamp, verify that the Safety Code permit application package is complete per AHJ requirements. Confirm that all required drawings, schedules, and supporting documents are assembled for permit submission.
2. Engineer of Record applies P.Eng. stamp (Alberta) to all IFC sheets.
3. Issue drawing set at IFC revision level. Record revision in Datasheet Revision History table.
4. Distribute to:
   - County project representative.
   - Electrical contractor (PKG-015).
   - Building permit / Safety Code permit application package.

> **Enrichment (A-004):** A pre-stamp checkpoint has been added for verifying Safety Code permit application package completeness. The original Step 8 referenced permit submission but did not include a check that the permit package is complete. Source: R-01 S3.3.2 (Safety Codes compliance, inspection coordination); standard permitting practice — ASSUMPTION.

> Source: R-01 S3.3.2; R-01 S3.3.2 (inspection coordination); OBJ-003.

---

## Verification

After completing the drawing set, verify the following before issuing IFC:

| Check | Pass Condition |
|---|---|
| All five receptacle types present | 15 A/120 V, 20 A/120 V, 20 A/240 V, 30 A/240 V, 50 A/240 V all shown with legend entries |
| Welding receptacles distributed | 50 A/240 V symbols appear in multiple main shop bay locations, not only at the welding station. **Quantitative threshold: TBD — minimum count per bay or maximum spacing to be defined by Electrical Engineer (see Specification REQ-002).** |
| GFCI designated | Wash bay receptacles noted as GFCI; all other wet/damp locations enumerated and GFCI-designated per REQ-004 |
| Zone coverage complete | All zones (main shop, work bench, welding station, parts room, office, utility room, wash bay) have receptacles shown; mezzanine addressed |
| Mounting heights addressed | Mounting heights shown on drawing or general note provided per REQ-009 |
| AFCI / tamper-resistant addressed | Applicability determination documented per REQ-010; if required, correct notation shown |
| Circuit numbers assigned | Each receptacle or group has a circuit number traceable to DEL-004-06 (or convention documented per REQ-008) |
| Legend present and complete | All symbols used in the drawing are defined in the legend |
| P.Eng. stamp applied | Alberta P.Eng. stamp present on each IFC sheet |
| Architectural base coordinated | Outlet locations do not conflict with structural elements, door swings, or equipment clearances shown on DEL-001-02 |
| Welding rating confirmed | County welder specifications reviewed; 50 A/240 V assumption confirmed or revised |
| Intermediate QA checklist complete | Step 6 self-check checklist completed and filed |
| Permit package completeness verified | Safety Code permit application package confirmed complete per AHJ requirements (Step 8.1) |

> **Enrichment (A-005):** The "Welding receptacles distributed" check now references a quantitative threshold to be defined by the Electrical Engineer, rather than the previous subjective "appear in multiple locations" criterion. Source: R-01 S3.4 ("multiple electrical plugs throughout the shop area"); Specification REQ-002.

---

## Records

The following evidence shall result from this procedure:

| Record | Description | Where Filed |
|---|---|---|
| IFC drawing set — Receptacle Layout Plans | Stamped IFC drawing sheet(s) | DEL-004-05_Receptacle-Plans / 1_Working (and issued to County) |
| County welder specification confirmation | Written confirmation of welder ratings from County | Project correspondence file |
| Scope confirmation memo | Written record of mezzanine and renovation scope decisions | Project correspondence file |
| Internal review checklist | Completed quality review checklist from Step 6 (intermediate QA gate) | Electrical Engineer's QA records |
| CEC Part I edition confirmation | Written record of confirmed code edition from AHJ | Electrical Engineer's QA records; also recorded in Specification Standards table |
| GFCI location enumeration | Documented list of wet/damp locations evaluated per REQ-004 | Electrical Engineer's QA records |
| AFCI / tamper-resistant determination | Documented determination of code applicability per REQ-010 | Electrical Engineer's QA records |
| Permit submission record | Evidence of Safety Code permit application including this drawing set | PKG-009 / DEL-009-03 |
