# Guidance — DEL-008-03 Construction Survey

**Document Type:** Guidance (directional)
**Deliverable:** DEL-008-03 Construction Survey
**Package:** PKG-008 Geotechnical Investigation & Surveying
**Project:** 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition
**Revision:** Pass 3 — 2026-02-26

---

## Purpose

The Construction Survey (DEL-008-03) exists as the essential spatial translation layer between the design intent expressed in IFC drawings and the physical construction work on the WDMLRL site. Without accurate, timely, and well-documented construction survey support, construction trades cannot correctly position foundations, walls, pads, drains, or utility connections; errors become embedded in permanent works.

The RFP explicitly requires the Design-Builder to "conduct preliminary, construction, and as-built survey" as part of the Proponent's services (RFP §3.3.2). The construction survey (SOW-0003) is therefore a contractual obligation, not an optional quality measure. The deliverable supports OBJ-001 (functional, code-compliant shop) and OBJ-002 (on-time completion by December 31, 2026) by ensuring construction proceeds from correct spatial information.

**Source:** RFP §3.3.2; WDMLRL_Decomposition_Claude.md §3 (SOW-0003), §5 (OBJ-001, OBJ-002)

---

## Principles

### Principle 1: Design-to-Field Traceability

Every staked element in the field must be traceable to a specific IFC drawing, sheet number, and revision. The value of construction survey is largely realized through the auditability of this chain: if a position error is discovered, the field notes should clearly show whether it was a survey error, a drawing interpretation error, or a design error. Maintaining this traceability also supports the as-built survey (DEL-008-04) and any warranty or defect discussions during the guarantee period.

**Source:** Inferred from RFP §3.3.2 (survey obligation), §2.10 (guarantee period obligations); WDMLRL_Decomposition_Claude.md §5 (OBJ-001)

### Principle 2: Control Continuity from Preliminary Survey

The construction survey must use the same control network established in the preliminary survey (DEL-008-02). Introducing a new, independent control network without reference to the preliminary survey control creates a risk of systematic error propagation — positions derived from different datums or benchmarks can produce alignment errors that are difficult to detect during construction but become apparent in as-built records.

**Source:** _DEPENDENCIES.md (upstream: DEL-008-02 Preliminary Survey); _REFERENCES.md (Related Deliverables)

### Principle 3: Drainage Grade Control is Critical

The site grading design must produce positive drainage and must not alter drainage conditions of neighbouring properties (RFP §3.4). This places a specific burden on the construction survey: the grade control lines set by the Surveyor must match the civil grading design intent, and any discrepancy between the design grades and actual ground conditions must be identified early. WDMLRL is a landfill site with significant existing earthworks; the expansion area aerials (Appendix C) show an active, varied-grade site where drainage design assumptions should be verified against actual as-graded conditions.

**Source:** RFP §3.4; WDMLRL_Decomposition_Claude.md §3 (SOW-0020, SOW-0021); Appendix C Site Maps

### Principle 4: Survey Must Track Construction Sequencing

Construction at a design-build project with a fixed December 31, 2026 deadline proceeds in overlapping phases. The Surveyor should work in close coordination with the construction schedule (PKG-019) so that staking and verification activities are available when trades need them — not as a one-time effort at the beginning of construction. Key construction milestones that require survey input include: foundation excavation layout, foundation form setting, slab-on-grade grade control, cistern pit layout, exterior pad staking, and subgrade verification before gravel placement.

**Source:** _DEPENDENCIES.md (external: construction schedule confirmation); WDMLRL_Decomposition_Claude.md §5 (OBJ-002); RFP §3.1 (deadline)

### Principle 5: Foundation Pricing is Geotech-Dependent

The RFP explicitly states that final foundation design and pricing is negotiated with the successful Proponent after the complete geotechnical report is available (RFP §4.8.2). This means that when construction survey begins, the foundation design may not be fully finalized. The Surveyor should be prepared to stake foundation extents once the final foundation design (DEL-002-11) is issued, and should confirm with the construction manager that the IFC foundation drawings are the final, stamped version before committing stakes.

**Source:** RFP §4.8.2; WDMLRL_Decomposition_Claude.md §5 (OBJ-006), §3 (SOW-0019, SOW-0304)

### Principle 6: Geotech-Dependent Timing Should Influence Survey Plan Phasing

The geotech-dependent foundation pricing mechanism (RFP §4.8.2) creates a sequencing risk that the Construction Survey Plan should explicitly address. Since final foundation design is negotiated post-geotech report, the survey plan should anticipate phased staking: an initial phase covering site elements with stable IFC drawings (site grading, driving surfaces, utility corridors), and a subsequent phase for foundation and structural elements once the final foundation IFC drawings are issued. The Construction Survey Plan (REQ-008-03-06a) should include re-staking provisions for any element staked from preliminary drawings that is later superseded by final foundation design.

This principle connects the normative requirement (REQ-008-03-02, IFC before staking) to the operational reality (Procedure Step B3, preliminary staking with flags) by providing the rationale for why phased staking and explicit re-staking provisions are warranted. [Lensing item B-004]

**Source:** RFP §4.8.2; Specification REQ-008-03-02; Guidance Trade-off 3; Procedure Step B3; WDMLRL_Decomposition_Claude.md §3 (SOW-0019, SOW-0304)

---

## Considerations

### Site Conditions

The expansion area for the new maintenance shop addition is adjacent to the existing maintenance shop building (visible in Appendix C aerial, expansion area highlighted). The site is within an active landfill facility. Surveyors should:

- Anticipate access coordination with the County and landfill operations
- Account for the active nature of the site (heavy equipment, variable surface conditions, dust)
- Reference the control network to stable monuments outside the active construction zone where possible
- Confirm clearing limits with the County (County is responsible for brushing and clearing per RFP §3.3.1) before survey control monuments are placed

**Source:** Appendix C Site Maps; RFP §3.3.1; WDMLRL_Decomposition_Claude.md §4 (SOW-0200, SOW-0201)

### Building Complexity Relevant to Survey

The 13,000 sq ft addition includes several elements that require careful survey positioning:

- **Service pit / trench:** A below-grade element requiring precise elevation control; errors in depth are difficult and costly to correct after concrete is placed. (RFP §3.4; SOW-0028)
- **Steel plates in slab:** Embedded steel plates at strategic locations for heavy tracked and packer equipment — positions must match structural drawings to ensure the equipment tracking pattern is not disrupted. (RFP §3.4; SOW-0024)
- **Drive-through bays and wash bay:** Alignment of bay doors and building axes must be consistent with the IFC architectural and structural drawings. (RFP §3.1; SOW-0025, SOW-0027a)
- **Cistern location:** The 50,000 L cistern (SOW-0041) and associated plumbing invert grades require accurate layout.
- **Mud sump:** Exterior to the building, requires both positional and grade control for proper drainage function. (RFP §3.4; SOW-0027b)

**Source:** RFP §3.1, §3.4; WDMLRL_Decomposition_Claude.md §3 (SOW-0024, SOW-0025, SOW-0027a, SOW-0027b, SOW-0028, SOW-0041)

### Coordination with Other PKG-008 Deliverables

The four PKG-008 deliverables form a sequential survey chain:
1. DEL-008-01 Geotechnical Investigation — informs foundation design
2. DEL-008-02 Preliminary Site Survey — establishes base control
3. DEL-008-03 Construction Survey (this deliverable) — guides construction
4. DEL-008-04 As-Built Survey — records what was built

Construction survey should document its control network in a format that facilitates handoff to the as-built survey team, even if that team is the same Surveyor.

**Source:** WDMLRL_Decomposition_Claude.md §7 (PKG-008 table); _REFERENCES.md (Related Deliverables)

### Cost and Schedule Impact of Survey Errors

Survey errors that propagate into constructed work create rework costs and schedule delays that are disproportionate to the cost of the survey itself. For a fixed-deadline project (December 31, 2026, per RFP §3.1), the schedule impact of rework is particularly significant because there is no schedule float for corrective work. Key risk areas include:

- **Foundation position errors:** Require excavation, re-forming, and re-pouring — the most costly rework category. The geotech-dependent foundation timing (RFP §4.8.2) compounds this risk if preliminary staking is not clearly flagged.
- **Slab grade errors:** Affect drainage compliance (RFP §3.4) and may require grinding, overlay, or re-pouring.
- **Utility corridor misalignment:** Can conflict with building structure or site grading, requiring re-routing.

The frequency of verification surveys (Trade-off 2) and the accuracy tolerances defined in the Construction Survey Plan (REQ-008-03-06, REQ-008-03-06a) should be calibrated with this cost/schedule risk in mind. Investing in more frequent verification at critical milestones (foundation, slab, subgrade) is generally justified by the disproportionate cost of rework at those stages. **ASSUMPTION**: specific cost/schedule quantification is not available from the RFP or decomposition; this is directional guidance based on standard construction risk assessment practice. [Lensing item C-003]

**Source:** RFP §3.1 (deadline); RFP §3.4 (drainage); RFP §4.8.2 (foundation timing); standard construction risk assessment practice (**ASSUMPTION**)

### County Inspection Requirements

The County project representative must be present at all inspections and shall be provided with copies of all completed inspection reports (RFP §3.3.2). Where survey-related field verifications constitute an inspection milestone, the County project manager should be notified in advance and records provided.

**Source:** RFP §3.3.2; WDMLRL_Decomposition_Claude.md §3 (SOW-0084, SOW-0085)

---

### Quality Acceptance Framework for the Survey Deliverable Package

Beyond the individual verification checks in the Procedure, the overall quality of the construction survey deliverable package should be assessed against the following quality attributes. This framework provides criteria for a quality review of the complete deliverable, as distinct from the step-by-step verification of individual records. [Lensing item D-003]

| Quality Attribute | Assessment Criteria | Source |
|-------------------|---------------------|--------|
| Accuracy achieved | All field verification records show pass results against the tolerances in the Construction Survey Plan; any failures are documented with resolution | REQ-008-03-06; Construction Survey Plan |
| Completeness of coverage | Staking records exist for every element in the REQ-008-03-03 element table; no IFC drawing element is missing a corresponding survey record | REQ-008-03-03; REQ-008-03-08 |
| Discrepancy resolution | All reported discrepancies (REQ-008-03-04) have documented resolutions with decision authority identified | REQ-008-03-04 |
| Control provenance | Chain-of-custody documentation is complete from DEL-008-02 receipt through DEL-008-04 transfer | REQ-008-03-08b |
| Timeliness | Survey activities were completed in time to support the construction schedule without causing delays | REQ-008-03-09 |
| Record quality | All records meet the minimum content requirements (REQ-008-03-08); records are systematically indexed | REQ-008-03-08; Procedure Records table |

**ASSUMPTION**: this quality framework is directional guidance for the Surveyor and Construction Manager; specific acceptance thresholds should be agreed before the Construction Survey Plan is finalized.

---

## Trade-offs

### Trade-off 1: Control Monument Placement vs. Site Activity

Placing control monuments within the active construction area makes them convenient for layout but risks disturbance by construction equipment. Placing them outside the active area protects them but introduces additional traversing or setup time. Standard practice is to use a combination: permanent benchmarks on stable ground outside the active zone, with temporary working control points within the site refreshed as needed.

**Recommendation (ASSUMPTION):** Establish at minimum two permanent control monuments outside the expected area of disturbance, tied to the preliminary survey control network, and use working control points within the construction zone that are re-established from permanents if disturbed.

**No source specifically requires this approach in the RFP or decomposition — this is directional guidance based on standard construction survey practice.**

### Trade-off 2: Survey Frequency vs. Schedule Efficiency

More frequent verification surveys reduce the risk of errors propagating through multiple construction stages but consume Surveyor time. Too-infrequent surveys increase rework risk, particularly for costly elements such as the foundation, slab, and service pit.

**Recommendation (ASSUMPTION):** Survey verification should occur at minimum: before foundation excavation, after excavation (before forming), after forming (before pour), after slab pour, and at subgrade completion before paving. The construction manager should confirm the milestone checkpoints.

**This is directional guidance; the specific frequency is TBD pending the construction schedule.**

### Trade-off 3: Foundation Staking Timing vs. Geotech Finalization

Staking the foundation before the geotech-informed final foundation design is issued risks re-staking. Waiting adds schedule risk.

**Recommendation (ASSUMPTION):** Use the preliminary foundation layout from the early IFC drawing set for rough excavation guidance; do not perform final foundation form staking until the P.Eng.-stamped foundation IFC drawings are confirmed by the structural engineer.

**Source for the problem context:** RFP §4.8.2; WDMLRL_Decomposition_Claude.md §3 (SOW-0019, SOW-0304)

---

## Examples

No project-specific survey examples are available from the RFP or conceptual drawings. The site maps (Appendix C) show:
- The existing maintenance shop building (the "Old North Shop" and existing facility) on the west side of the expansion area
- The expansion area (highlighted in green/yellow in Appendix C aerial) immediately east and north of the existing structure
- Active landfill operations visible across the broader site

These aerials can be used as orientation aids for initial site familiarization but are not substitutes for the IFC site survey drawings.

**Source:** Appendix C Site Maps

---

## Conflict Table (for human ruling)

No unresolvable conflicts were identified between available source documents for this deliverable at Pass 3 stage. The following gaps exist but are not inter-source conflicts. Gaps marked with an asterisk (*) were identified or refined during Pass 3 (Semantic Lensing Enrichment).

| Gap ID | Gap Statement | Location in Sources | Impact | Notes |
|--------|---------------|---------------------|--------|-------|
| GAP-001 | Specific horizontal and vertical accuracy tolerances for construction survey are not stated | RFP §3.3.2; decomposition SOW-0003 | REQ-008-03-06; REQ-008-03-06a | To be defined by licensed Surveyor in the Construction Survey Plan; standard Alberta practice is assumed. Pass 3 added REQ-008-03-06a requiring the plan be approved before field work. [A-001, C-001, X-001] |
| GAP-002 | Progress survey frequency and reporting cadence not defined | RFP §3.3.2; decomposition SOW-0003 | REQ-008-03-07; Procedure Steps | To be established in the Construction Survey Plan or construction schedule |
| GAP-003 | Specific construction survey artifacts (report format, deliverable list) are not enumerated in RFP | RFP §3.3.2 | Documentation section | Artifact list in Datasheet and Specification is based on standard practice (ASSUMPTION); marked as provisional in Datasheet [B-002] |
| GAP-004* | Geodetic datum, map projection, and vertical datum not declared | Datasheet; Specification; Procedure | All spatial data in all four documents | TBD — to be confirmed by Surveyor or derived from DEL-008-02 [B-001, B-003, E-001] |
| GAP-005* | Applicable Alberta survey standards not confirmed at clause level | Specification Standards section | Compliance determination for all requirements | All standards entries remain ASSUMPTION; Surveyor must confirm [A-003, F-002] |
| GAP-006* | Survey record retention period not defined | REQ-008-03-08a | Contract guarantee and professional obligations | TBD — pending confirmation of CCDC 14-2013 guarantee terms and Alberta Land Surveyors Act requirements [C-002] |
| GAP-007* | County inspection hold points for survey milestones not enumerated | RFP §3.3.2; Guidance; Procedure Step C7 | REQ-008-03-10; Procedure Step C7 | TBD — County PM / Construction Manager to enumerate [D-002] |
| GAP-008* | Upstream input availability dates not confirmed | Datasheet Upstream Inputs; _DEPENDENCIES.md | All prerequisites and scheduling | TBD — Design-Builder / Construction Manager to confirm [E-002] |
