# Guidance — DEL-008-04 As-Built Survey

---

## Purpose

DEL-008-04 exists to create a permanent, authoritative record of the West Dried Meat Lake Regional Landfill Maintenance Shop Addition as it was actually constructed. Unlike design drawings — which represent intent — the as-built survey documents reality: the actual positions, elevations, and configurations of all constructed elements.

This deliverable serves three primary downstream purposes:

1. **Verification:** Confirming that construction conforms to the approved IFC design drawings, supporting the Construction Completion Certificate (CCC) process under the CCDC 14-2013 contract (RFP §2.14).
2. **Operational baseline:** Providing Camrose County with accurate spatial data for future operations, maintenance, and facility management at the WDMLRL site (SW 14-44-21-W4).
3. **Future modifications:** Establishing a reliable reference for any future additions, expansions, or infrastructure modifications at the site.

Sources: _CONTEXT.md (description); _DEPENDENCIES.md (notes); WDMLRL_Decomposition_Claude.md (OBJ-001, OBJ-002); RFP ss2.14.

**Evaluating long-term utility:** While these three downstream purposes are clearly identified, there is currently no defined mechanism for evaluating whether the as-built survey deliverable successfully serves them after delivery. Considerations for long-term utility evaluation include: (a) usability for future facility modifications -- is the format and level of detail sufficient for future design teams? (b) compatibility with County GIS or asset management systems -- TBD; (c) durability of the datum and coordinate system for future reference. The Owner and Facility Manager should consider specifying success criteria for long-term utility at project execution. [Lensing: D-003]

---

## Principles

### P-1: Conduct survey after construction, not before
The integrity of an as-built survey depends on all construction being complete — or at minimum substantially complete — before field work begins. Premature as-built surveys create records that do not reflect final conditions and require re-work. The _DEPENDENCIES.md confirms construction completion as the primary prerequisite.

### P-2: Maintain datum continuity with the construction survey
DEL-008-03 (Construction Survey) established the horizontal and vertical control network used throughout construction. The as-built survey must reference the same datum to allow direct comparison of design intent (set out from the control network) against actual constructed conditions. Using a different or inconsistent datum undermines the construction verification function of the deliverable. Source: _DEPENDENCIES.md (DEL-008-03 upstream).

**Contingency -- control point disturbance:** At an active landfill construction site, there is a realistic risk that DEL-008-03 control points may have been disturbed or destroyed during construction. The Surveyor should verify control point integrity during Step 2.1 (field survey). If control points are found disturbed, the Surveyor must exercise professional judgment to re-establish control from unaffected points or alternative references, and document the basis for any re-establishment in the final report. This contingency should be planned for during pre-field preparation (Step 1.1). Source: _DEPENDENCIES.md; professional practice. [Lensing: B-003]

### P-3: Document actual conditions, not design intent
The surveyor's task is to measure and record what is in the ground and on the site — not to reproduce the IFC drawings. Where deviations from design are found, those deviations must be accurately documented and reported, not silently corrected or omitted.

### P-4: Completeness supports long-term value
As-built surveys that omit components (underground infrastructure, grading, utility tie-ins) create gaps that can cause significant problems for future facility managers. For a landfill maintenance facility that includes underground cistern, septic, and drainage infrastructure, complete documentation of all accessible as-built information is important. Source: RFP §3.4 (project components).

### P-5: Record documentation is a project closeout requirement
The as-built survey is a final closeout deliverable. It must be delivered before project closeout can be completed. Under the CCDC 14-2013 contract, all work must be complete by December 31, 2026 (RFP §3.1). The as-built survey schedule must account for this deadline and the time required for construction to reach substantial completion.

---

## Considerations

### Construction timeline constraint
The project must be fully complete by December 31, 2026 (RFP §3.1; OBJ-002). The as-built survey can only proceed after substantial construction completion. The Proponent should plan the as-built survey carefully within the overall project schedule to allow sufficient time for field work and documentation without jeopardizing the project completion deadline.

### Site access at a working landfill
The WDMLRL is an active landfill operation (Appendix C aerial shows active earthworks). Survey field work must be coordinated with site operations to ensure safe and unobstructed access to all areas to be surveyed. ASSUMPTION: site access coordination is the Proponent's responsibility as Prime Contractor (RFP §2.15).

### Owner-performed pre-works scope boundary
Camrose County performed brushing/clearing, bulk cut and fill, and aggregate supply (RFP §3.3.1). The as-built survey documents the final constructed state, which incorporates the combined effects of County pre-works and Proponent construction. The surveyor should be aware of this split scope when interpreting deviations from design: some grade variations may trace to County pre-works rather than Proponent construction.

### Underground and partially obscured infrastructure
The project includes underground or partially buried infrastructure: cistern, septic holding tank, drainage features, and utility tie-ins. As-built documentation of underground infrastructure is typically limited to what is observable during or immediately after installation. If underground infrastructure locations were not captured during DEL-008-03 (Construction Survey), the as-built survey may need to rely on construction records and contractor-marked as-built drawings. The surveyor should confirm the availability of these records before commencing work.

### Accuracy standard gap
The RFP (§3.3.2) does not specify numerical accuracy requirements for the as-built survey. The Surveyor should seek Owner direction on required accuracy before field work, and should apply professional judgment and applicable AOLS standards in the absence of explicit Owner direction. This gap should be flagged to the project manager at project execution.

### Relationship to Construction Completion Certificate
The as-built survey supports the Owner's issuance of the Construction Completion Certificate (CCC) under RFP ss2.14. The survey provides objective evidence that construction has been completed as designed. Accordingly, as-built survey findings that reveal material deviations from IFC drawings may affect CCC issuance and should be reported promptly to the project manager.

### Terminology normalization -- septic system
The RFP ss3.4 describes a "2,000 US Gallon Septic holding tank (potentially removal and relocate existing septic tank)." This element is referenced with varying granularity across the production documents: the Datasheet records capacity and relocation scope; the Specification lists it as a component to document; the Procedure describes field collection of lid location and tank footprint. All references should use the consistent term "septic holding tank" and note the 2,000 US gallon capacity where relevant. The relocation question (whether the existing tank was removed and a new one installed, or the existing tank was relocated) should be confirmed with the Owner and documented in the as-built record. See GAP-007. [Lensing: B-004]

---

## Trade-offs

| Trade-off | Option A | Option B | Guidance |
|---|---|---|---|
| Survey timing | Wait for 100% construction completion | Survey at substantial completion with punch list items outstanding | ASSUMPTION: Surveying at substantial completion is generally acceptable for primary structural and site elements; however, final site grading, utility connections, and surface finishes should be verified as complete before the as-built survey is finalized. Confirm with Owner. |
| Underground infrastructure documentation | Full documentation of all subsurface elements using available records | Document only above-grade and visible elements | ASSUMPTION: Best practice for a facility with long design life is to document underground infrastructure to the extent possible. If construction records (contractor markups) are available, incorporate them into the as-built record. |
| Deliverable format | Full CAD drawing set with data files | PDF drawings only | ASSUMPTION: Format should be agreed with the Owner at project execution. A digital format (CAD or equivalent) with a PDF deliverable provides greater long-term utility. **Cost/schedule consideration:** Full CAD deliverables require more drafting effort and software capability but yield a reusable, editable record suitable for future design work. PDF-only deliverables are lower cost to produce but cannot be readily modified or integrated with GIS/asset management systems. For a long-life landfill maintenance facility, the incremental cost of CAD is likely justified. TBD -- Owner to confirm. [Lensing: F-003] |

---

## Examples

No project-specific as-built survey examples are available from the accessible source set. General as-built survey conventions for Alberta industrial facility construction apply. TBD -- examples may be referenced at project execution from the following potential sources: (a) AOLS practice guidelines or sample deliverables for as-built surveys (if published); (b) similar Camrose County facility records from previous WDMLRL construction phases; (c) comparable Alberta industrial facility as-built survey deliverables from the Surveyor's portfolio. The Surveyor and PM should identify and reference applicable examples during pre-field preparation to inform the approach and deliverable format. [Lensing: X-001]

---

## Conflict Table (for human ruling)

No unresolvable conflicts identified at Pass 1+2. The following gaps are noted as requiring Owner direction rather than being conflicts:

| Gap ID | Description | Source | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|
| GAP-001 | Accuracy standard not specified in RFP. Without a prescribed accuracy standard, normative direction for field work is incomplete. [Lensing: A-001] | RFP ss3.3.2 (silent); _REFERENCES.md (generic) | Specification REQ-005; Guidance Considerations; Datasheet Attributes (Horizontal/Vertical Accuracy Class) | AOLS professional standards apply by default; Owner should confirm | TBD |
| GAP-002 | Deliverable format (CAD / PDF / digital data) not specified. Has cost/schedule and long-term utility implications. [Lensing: B-002, F-003] | RFP ss3.3.2 (silent) | Specification Documentation section; Datasheet Attributes; Guidance Trade-offs table | Owner to specify at project execution | TBD |
| GAP-003 | Specific components list for as-built documentation not enumerated in RFP beyond the general phrase "as-built survey." Confirmation must be documented. [Lensing: C-001] | RFP ss3.3.2 | Specification REQ-002 | Surveyor and PM to agree scope with Owner at project initiation | TBD |
| GAP-004 | Conformance tolerance for construction verification (REQ-003) is undefined. Comparison against IFC drawings cannot produce a definitive pass/fail result without a measurable threshold. Deviation classification criteria (within tolerance / minor / material) also undefined. [Lensing: A-003, C-002, C-003, E-002] | Specification REQ-003; Procedure Step 3.4 | Specification REQ-003 + Verification table; Procedure Step 3.4; Specification Documentation (deviation table) | Owner + Surveyor to define tolerance and classification criteria | TBD |
| GAP-005 | Professional sealing requirement for as-built drawings is TBD. Whether deliverable requires ALS signature/seal affects legal standing. [Lensing: D-001] | Procedure Records table; Alberta Surveys Act (not accessible) | Specification Documentation; Procedure Records table | Alberta Surveys Act + Owner | TBD |
| GAP-006 | Owner acceptance criteria for as-built deliverable are undefined. Procedure Step 5.4 requires written acceptance but no evaluation criteria exist. [Lensing: D-002] | Procedure Step 5.4; Specification Verification table (REQ-006) | Specification Verification table; Procedure Step 5 | Owner | TBD |
| GAP-007 | Septic system terminology inconsistent across documents. "2,000 US gallon septic holding tank" (Datasheet) vs. "septic holding tank and associated infrastructure" (Specification) vs. "septic system location (holding tank)" (Procedure). Relocation scope question unresolved. [Lensing: B-004] | RFP ss3.4; Datasheet Construction table; Specification REQ-002; Procedure Step 2.3 | Datasheet, Specification, Procedure (all references to septic system) | Owner + Surveyor | TBD |
| GAP-008 | IFC drawing availability not confirmed. REQ-003 requires comparison against IFC drawings but no prerequisite confirms their availability, source, or format. [Lensing: X-003] | Specification REQ-003; Procedure Step 1.2; Procedure Prerequisites | Specification REQ-003; Procedure Steps 1.2, 3.4 | Project Manager / Design team | TBD |
| GAP-009 | Independent peer review requirement is TBD. AOLS standards (not accessible) may require independent review for permanent legal records. [Lensing: X-004] | Specification Standards table; Procedure Step 4 | Specification Documentation; Procedure Step 4 | AOLS professional standards | TBD |
