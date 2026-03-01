# Guidance — DEL-011-02 Steel Plate Floor Embedments

**Document Type:** Guidance (directional)
**Deliverable ID:** DEL-011-02
**Revision:** R1 — 2026-02-26 (Pass 3 enrichment)
**Status:** SEMANTIC_READY

---

## Purpose

This deliverable exists to satisfy the Owner's explicit requirement for steel plate embedments in the repair bay concrete floors to enable safe and practical servicing of tracked and packer-type heavy equipment (RFP R-01 §3.4; SOW-0024). The steel plates protect the concrete slab from damage caused by the concentrated contact loads of tracked undercarriages and solid rubber or metal-padded packer equipment, and provide a durable wearing surface in high-load zones.

Within the project decomposition, DEL-011-02 is a construction deliverable under PKG-011 (Building Structure and Envelope), supporting OBJ-001: delivery of a code-compliant, fully functional maintenance shop addition that satisfies the County's operational program (Decomposition §5).

The downstream consumer is PKG-012 (Interior Construction and Fit-Out) and ultimately the equipment operations program — equipment must be able to enter and manoeuvre on the repair bay floor without slab damage.

---

## Principles

### 1. Follow the Structural Engineer's IFC Documents
This is a construction deliverable, not a design deliverable. The structural engineer (PKG-002, DEL-002-08) will determine plate sizes, thicknesses, grades, spacing, and anchorage details based on the specific equipment the County intends to service. The GC's role is to execute that design precisely. Do not substitute plate sizes, grades, or anchorage methods without written approval from the structural engineer of record.

### 2. Cast-in-Place is the Presumed Method
ASSUMPTION: The floor plan (Appendix B, R-04) and the reference to "steel plating in concrete" (RFP §3.4) implies the plates are cast into the slab during the concrete pour rather than surface-mounted after the fact. This assumption has significant implications for construction sequencing — the plates and their anchorage must be in place before the floor concrete is poured, meaning any coordination failures at this stage cannot be easily corrected without costly concrete removal and re-pour.

**Implication:** Confirm cast-in-place method with the structural engineer at the earliest opportunity. If surface-mounted plates were intended, the sequence, specification, and verification requirements differ substantially. This is flagged in the Conflict Table below (CON-011-02-01). This is identified as the single most consequential ambiguity in the deliverable. [Lensing ref: A-001]

### 3. Coordinate with DEL-011-01 Early
The concrete floor slab pour is the critical interface point. The steel plate embedment work must be fully coordinated with the concrete slab pour schedule under DEL-011-01. Late delivery of structural drawings (DEL-002-08) or late procurement of plates will delay the slab pour and impact the overall construction schedule.

**Source:** _DEPENDENCIES.md (upstream dependency: DEL-011-01); RFP §3.1 ("All Work... must be completed on or before December 31, 2026").

### 4. Inspection Hold Point Before Pour
A pre-pour inspection hold point is strongly recommended (ASSUMPTION: consistent with standard structural construction practice) to confirm that:
- All plates are correctly positioned per IFC drawings.
- Anchorage systems are correctly installed and welded.
- Plate surfaces are at the correct elevation to achieve flush finish after concrete placement and finishing.
- Formal pass/fail acceptance criteria are applied (see Specification REQ-011-02-06 Verification and Procedure Step 8). [Lensing ref: X-002, X-004]

Missing this hold point creates risk of non-compliant work that cannot be remedied without removing concrete.

### 5. Load Rating Documentation Is a Deliverable
The RFP anticipates load rating certification as an output (_CONTEXT.md Anticipated Artifacts). This is not simply a construction byproduct — it is a formal document from the structural engineer of record (P.Eng.) certifying the installed embedments meet the design load requirements. Coordinate with the structural engineer to ensure this certification is scoped and scheduled. TBD: Confirm whether certification is by calculation-based analysis only or includes physical load testing. [Lensing ref: D-003, F-001]

---

## Considerations

### Construction Sequencing Risk
The steel plate embedments are cast into the concrete slab, meaning their installation is a one-time, non-reversible step within the slab construction sequence. Any error in plate location, elevation, or anchorage discovered after the pour requires significant remediation effort. Coordination between the structural design team (DEL-002-08 drawing issuance) and the construction team must be completed well in advance of the scheduled slab pour.

### Drawing Availability
At the time of this document's drafting, DEL-002-08 (Steel Plate Embedment Plan, IFC) has not yet been issued. The Appendix B floor plan (R-04) is conceptual only — it shows approximate locations but does not provide construction-grade dimensions, plate specifications, or anchorage details. Construction shall not proceed based on the conceptual drawing alone.

**Escalation path for DEL-002-08 delay:** If DEL-002-08 IFC drawings are not issued in time for the scheduled slab pour, the following escalation protocol applies: [Lensing ref: X-001]
- TBD: Define who has authority to delay the pour (ASSUMPTION: GC project manager in coordination with structural engineer of record and Owner representative).
- TBD: Define minimum advance notice period required for pour delay notification to concrete subcontractor and County representative.
- TBD: Define how delay costs are allocated per contract terms (CCDC 14–2013 provisions for delays caused by design team).
- ASSUMPTION: The GC shall not proceed with slab pour in the affected zone without IFC-issued DEL-002-08 drawings; proceeding on conceptual drawings alone is not acceptable.

### Plate Count and Location Uncertainty
The Appendix B plan (R-04) shows multiple transverse steel plate bands in the main repair bay area and in the wash bay, but exact plate count, individual plate dimensions, and precise spacing are not determinable from the conceptual drawing. ASSUMPTION based on Appendix B: approximately four to six transverse bands in the repair bays and one to two bands in the wash bay, each spanning the approximate 24' bay width. Actual quantities and dimensions are TBD pending DEL-002-08.

### Surface Finish and Anti-Slip
ASSUMPTION: Plate top surfaces may require surface texture (checkered plate, grit blasting, or equivalent) to provide adequate traction for maintenance personnel working around or on the plates. This is not explicitly stated in the RFP. Confirm with the structural/architectural team whether anti-slip treatment is required, particularly in the wash bay where floors will be wet.

### Welding Qualifications
ASSUMPTION: Anchorage welding (stud welding or fillet welding of anchor bars) will need to be performed by a certified welding company under CSA W47.1 and inspected per CSA W59. The GC must confirm welding subcontractor qualifications prior to commencing embedment installation. This requirement should be confirmed in DEL-002-12. TBD: Confirm which specific standard (W47.1, W59, or both) governs acceptance/rejection of anchorage welds. [Lensing ref: A-003]

### Interface with Wash Bay
The wash bay also shows steel plate bands in the Appendix B floor plan. The wash bay is subject to water, cleaning chemicals, and potentially hydrocarbon contamination. Consider whether corrosion protection is required for embedded steel in this zone, or whether the structural engineer has accounted for this in the plate thickness specification.

**Corrosion protection decision criteria:** [Lensing ref: F-004]
The decision on corrosion protection for wash bay steel plate embedments should be framed by the following criteria:
1. **Exposure severity:** The wash bay environment (direct water exposure, cleaning chemicals, hydrocarbon contamination) differs materially from the repair bay (primarily dry mechanical contact). The corrosion exposure classification may differ between zones.
2. **Protection options:** (a) Hot-dip galvanizing, (b) epoxy or polyurethane coating, (c) sacrificial thickness allowance (additional plate thickness beyond structural requirement), (d) stainless steel or weathering steel selection. Each option has different cost, constructability, and maintenance implications.
3. **Service life alignment:** The corrosion protection strategy must be consistent with the expected service life (TBD — see Datasheet Conditions Service Life). A 40–50 year service life (ASSUMPTION) with no maintenance access to embedded steel surfaces requires a more durable protection strategy than a shorter replacement cycle.
4. **Interface compatibility:** Any coating or treatment must be compatible with the concrete interface (bond requirements for cast-in-place anchorage) and the wearing surface (equipment traffic).
- TBD: Structural engineer to address corrosion protection requirements in DEL-002-12 or DEL-002-08 for wash bay zone plates specifically.

### Service Life Decision Framing [Lensing ref: C-003]
The expected service life for the steel plate embedments is TBD. This decision has cascading implications:
- If designed for full building service life (ASSUMPTION: 40–50 years), material selection and corrosion protection must be specified for long-term durability with no access for maintenance or replacement of embedded components.
- If designed for a shorter replacement cycle, the embedment and anchorage system may need to be designed for future removal and replacement (surface-mounted may be more appropriate in that case — see CON-011-02-01).
- TBD: Owner and structural engineer to confirm service life expectation.

### County Representative Authority at Pre-Pour Hold Point [Lensing ref: X-005]
Procedure Step 8 requires "written sign-off from structural engineer and County representative" at the pre-pour hold point. TBD: Clarify whether the County project representative's role at the pre-pour hold point is:
- **(a) Formal approval gate:** County representative has veto authority and can block the pour independently of the structural engineer, or
- **(b) Witness/notification role:** County representative is present to observe and receive documentation, but the structural engineer's sign-off alone authorizes the pour.

This distinction affects scheduling (a formal gate requires the County representative's availability as a hard constraint) and risk allocation (a veto authority creates potential for County-caused delay). ASSUMPTION: Per RFP R-01 §3.3.2, the County representative must be "present for all inspections" — this suggests at minimum a witness role, but the contractual authority for pour authorization should be confirmed with the Owner/contract terms.

### Two-Year Guarantee Exposure
Steel plate embedments are subject to the two-year guarantee period (RFP §2.10.2). Given the heavy equipment loading they are designed for, any defect in anchorage, plate seating, or surface flush alignment is likely to manifest during this period and generate a warranty call. Quality control at the pre-pour inspection stage is the most cost-effective way to manage this risk.

---

## Trade-offs

| Trade-off | Option A | Option B | Recommended Direction |
|---|---|---|---|
| Embedment method | Cast-in-place (plates embedded during pour) | Surface-mounted (plates anchored to cured slab by drilling/epoxy or mechanical anchors) | Cast-in-place preferred for structural integrity and flush surface; ASSUMPTION — confirm with structural engineer |
| Plate extent | Plates spanning full bay width (per Appendix B pattern) | Localized pads at specific equipment contact points only | Full-width bands preferred per Appendix B conceptual layout; engineer to confirm |
| Surface treatment | Plain plate (mill finish) | Checkered or grit-blasted anti-slip finish | Anti-slip finish recommended for wash bay and wet areas (ASSUMPTION) |
| Corrosion protection (wash bay) | Sacrificial thickness / no coating | Active protection (galvanizing, epoxy coating) | TBD — depends on service life expectation and wash bay exposure severity; structural engineer to advise [Lensing ref: F-004] |

---

## Examples

Appendix B (R-04) is the only visual reference available. It shows the "Steel Plate" designation as parallel horizontal bands spanning the repair bay and wash bay widths at multiple intervals along the bay length. This pattern is consistent with providing a steel bearing surface for tracked equipment that travels lengthwise through the bays. No dimensional data or plate specifications are available from this source.

No additional worked examples are available from accessible sources. Further examples are TBD pending issuance of DEL-002-08.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CON-011-02-01 | Embedment method not explicitly stated: RFP §3.4 says "steel plating in concrete" (implying cast-in-place), but method (cast-in-place vs. post-installed surface mount) is not formally specified. Assumption of cast-in-place drives the entire construction sequence. If surface-mounted, sequence, specification, and verification change substantially. This is the single most consequential ambiguity in the deliverable. [Lensing ref: A-001] | RFP R-01 §3.4 ("steel plating in concrete") | No explicit specification document yet; DEL-002-08 not yet issued | Specification REQ-011-02-06, REQ-011-02-07; Procedure Steps 3–5; Guidance Principles 2, 4 | PROPOSAL: Structural engineer via DEL-002-08 to confirm method explicitly in IFC drawings. | TBD |
| CON-011-02-02 | Anti-slip surface finish requirement: not explicitly required in RFP or Appendix B, but wash bay and wet-floor conditions suggest it may be necessary for safety code compliance. Absence of requirement in sources makes this an unresolved design question. | No explicit RFP requirement | ASSUMPTION based on wash bay wet conditions and safety code general obligations (RFP §3.3.2) | Specification REQ-011-02-05; Datasheet Attributes; Guidance Considerations | PROPOSAL: Structural/architectural engineer to confirm whether anti-slip finish is required; default to checkered plate in wash bay as conservative assumption pending confirmation. | TBD |
| CON-011-02-03 | Exact plate locations in wash bay: Appendix B shows steel plate bands in both the main repair bays and the wash bay, but DEL-027a (Wash Bay Enclosure, PKG-011) and DEL-018-05 (Wash Bay Drainage, PKG-018) may have overlapping scope or conflicting requirements for the wash bay floor system. [Lensing ref: D-001] | Appendix B (R-04) showing steel plates in wash bay; SOW-0024 scope | SOW-0027a (wash bay structural scope, PKG-011) vs. SOW-0027b (drainage/mud sump scope, PKG-018) | Specification Scope; Datasheet Attributes; Procedure Steps | PROPOSAL: Confirm with project decomposition owner and structural engineer that wash bay steel plates are within DEL-011-02 scope and that floor drain locations in DEL-018-05 do not conflict with plate band locations per DEL-002-08. | TBD |
