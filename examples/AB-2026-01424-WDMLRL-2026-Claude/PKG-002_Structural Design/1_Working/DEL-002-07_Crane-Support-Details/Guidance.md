# Guidance — DEL-002-07 Crane Support Structure Details

---

## Purpose

DEL-002-07 exists to provide the Issued for Construction (IFC) structural drawing set for the overhead crane runway support system within the New North Shop addition. The crane support structure is a primary structural subsystem that enables the two 5-tonne overhead cranes to perform their intended function — moving heavy equipment and components within the main shop bays.

This deliverable directly supports:
- **OBJ-001**: Code-compliant, fully functional maintenance shop addition satisfying the County's operational program
- **OBJ-003**: Complete P.Eng.-stamped IFC design documentation across all disciplines before construction begins

Source: WDMLRL_Decomposition_Claude.md §5 (Objectives), §7 (DEL-002-07 entry); RFP §3.4; _CONTEXT.md

Without accurate crane support structure details, the building structure cannot be correctly formed, and the crane installation (PKG-016) cannot proceed safely or in compliance with code.

---

## Principles

### 1. Crane supplier data drives the structural design
The structural engineer cannot finalize runway beam sizing, corbel/bracket design, or connection details without the crane supplier's data sheet. The data sheet defines bridge end-truck wheel base, maximum wheel loads (including dynamic impact), and runway rail requirements. This is a critical upstream dependency that must be resolved early in the design sequence.

Source: ASSUMPTION (standard structural engineering practice for crane runway design; not explicitly stated in RFP)

### 2. Concrete structure context governs support configuration
The building is specified as a concrete structure with a 35' ceiling (RFP §3.4; App B). This means crane runway support will most likely take one of two forms:
- **Corbels cast into concrete columns** at the appropriate elevation, or
- **Dedicated crane columns** separate from or integral with the building columns

The final configuration is the structural engineer's decision, informed by crane span, capacity, column spacing, and constructability.

Source: RFP §3.4; App B (Shop) note list — ASSUMPTION for corbel/column interpretation

### 3. Runway elevation is constrained by the 35' ceiling and crane hook height
The required hook height under load determines the minimum runway beam bottom-of-rail elevation, which in turn determines the required support structure height. Crane selection (PKG-016) must confirm minimum hook height to verify that the 35' ceiling provides adequate clearance.

Source: RFP §3.4 (35' ceiling stated); ASSUMPTION that hook height verification is required

### 4. Two cranes may share a runway or operate on separate runways
The conceptual floor plan (App B) shows two cranes labeled "5 TON CRANE" positioned side by side in the main shop bays. This layout is consistent with two cranes sharing a common runway (two bridges on one pair of rails) or two independent parallel runways. The structural design must reflect the actual configuration selected.

Source: App B (Shop) floor plan — two crane positions visible in main shop bays

### 5. The "Gantry" label on the App B drawing is resolved as the same equipment
Per the decomposition decision D-001 (and Vocabulary Map), "Gantry" and the two 5-tonne overhead cranes are the same equipment shown differently in different areas of the conceptual drawing. The "Gantry" label near the wash bay on App B is treated as a reference to the same crane system, not a separate piece of equipment.

Source: WDMLRL_Decomposition_Claude.md — Vocabulary Map ("Gantry: Per D-001: same equipment as the 5-tonne overhead cranes shown differently on drawings"); SOW-0067 Notes

See also: Conflict Table below (CONF-007-01)

### 6. Terminology: "Gantry" vs. "Overhead crane" vs. "Crane"
**[F-002]** Across the four production documents and source materials, three terms are used for the same equipment: "gantry" (App B floor plan label), "overhead crane" (RFP §3.4), and "crane" (shorthand used throughout). Per D-001 resolution (Decomposition Vocabulary Map), these all refer to the same two 5-tonne overhead cranes. To prevent terminology drift:
- The preferred term in all production documents is **"overhead crane"** (matching RFP §3.4 language).
- The short form **"crane"** is acceptable in running text where the context is unambiguous.
- **"Gantry"** should appear only when referencing the App B drawing label, always with the D-001 resolution note.

This vocabulary convention should be applied consistently across Datasheet.md, Specification.md, Guidance.md, and Procedure.md.

Source: WDMLRL_Decomposition_Claude.md — Vocabulary Map; D-001 resolution. Proposed authority: D-001 resolution (PROPOSAL).

### 7. Coordination interface referencing convention
**[X-001]** Cross-references to the electrical coordination scope (crane power supply) use inconsistent identifiers across documents: Specification REQ-007-08 uses "SOW-0059 / DEL-004," Procedure uses "DEL-004" and "SOW-0059" separately in different steps. To prevent ambiguity about whether DEL-004 and SOW-0059 represent the same scope boundary, a consistent referencing convention should be adopted:
- Use **"DEL-004 (Electrical Design, SOW-0059)"** as the standard form when referencing the electrical coordination interface.
- If a coordination interface register is established at the project level, update references accordingly.

Source: Specification REQ-007-08; Procedure Steps 4.4, 5.2. Proposed authority: Design Coordinator (PROPOSAL).

---

## Considerations

### Design sequence considerations

**1. Crane procurement must lead structural drawings.**
The structural engineer requires the crane supplier data sheet before issuing IFC crane support drawings. The project schedule must ensure that crane supplier selection (PKG-016) is advanced sufficiently early to provide wheel load data to the structural designer. If crane data is not available when structural design proceeds, the structural engineer may need to use conservative assumed loads and confirm later — this should be documented in the calculation package (DEL-002-10).

**2. Geotechnical report affects column and foundation design.**
If the crane support columns bear independently (separate crane columns), their foundations are affected by the geotechnical conditions. The geotechnical report (PKG-008) is a prerequisite for the foundation scope.

Source: RFP §3.3.2; SOW-0001; SOW-0019 (foundation pricing dependent on geotech)

**3. Coordination with electrical must be explicit.**
Runway conductor bars or festoon cable systems require clearance from the runway beam and are typically mounted on the runway structure. The electrical engineer (DEL-004) needs to know the runway beam elevation and available clearance. A coordination note or envelope drawing is advisable.

Source: SOW-0059 — ASSUMPTION for coordination note requirement

**4. Building permit inspection coordination.**
The crane support structure is a significant structural element that will likely be subject to inspection under the Alberta Safety Codes Act building permit. Inspection hold points should be identified in the construction sequence.

Source: RFP §3.3.2 (all applicable Safety Code permits; all inspections coordinated); ASSUMPTION for inspection hold points

**5. Guarantee period implications for crane support structure.**
**[F-004]** The RFP §2.10.2 establishes a guarantee period of construction period plus 2 years post-CCC. Datasheet records this condition, but the implications for crane support structure design choices merit explicit consideration:
- **Fatigue classification:** The guarantee period alone does not define design life, but any fatigue-related failure during the guarantee period would be the Design-Builder's responsibility. The CMAA service class and fatigue classification should account for the anticipated duty cycle over at least the guarantee period.
- **Corrosion protection:** If the crane runway beams are steel within a concrete structure (a mixed environment), the protective coating system (galvanizing, paint system, or bare steel) should be selected considering the guarantee period exposure. At minimum, a coating system with a service life exceeding the guarantee period is prudent.
- **Rail and clip wear:** Rail clip tightness and rail wear should be considered relative to the expected crane usage over the guarantee period.

Source: Datasheet Conditions (Guarantee period — RFP §2.10.2); ASSUMPTION for design implications. Proposed authority: Structural Engineer (PROPOSAL).

**6. Post-installation commissioning and runway alignment survey.**
**[D-003]** The production documents cover design and IFC issuance but the quality lifecycle effectively ends at drawing issue. Consideration should be given to including:
- A post-installation runway alignment survey requirement (confirming rail straightness and elevation after crane runway erection and before crane commissioning).
- A commissioning review checkpoint where the structural engineer confirms the as-built condition matches the IFC design intent.
- A lessons-learned feedback loop to inform future crane support designs within the project or for similar facilities.

Source: ASSUMPTION (standard commissioning practice for crane runway systems); Procedure Records section (currently limited to design-phase records). Proposed authority: Project Manager (PROPOSAL).

### Design trade-off considerations

**Corbel vs. dedicated crane column:**
- Corbels cast into building columns reduce column count but require precise forming during concrete construction and may constrain column sizing.
- Dedicated crane columns provide design independence but add cost and coordination with the building grid.
- Choice depends on column spacing, bay dimensions, and crane span. The structural engineer selects the appropriate solution.

Source: ASSUMPTION (standard structural design trade-off)

**Runway rail type:**
- Standard crane rail sections (e.g., ASCE rail or ASTM crane rail) are preferred for higher-capacity cranes to limit web crippling and wear.
- For 5-tonne cranes, a wide-flange beam top flange may be acceptable if crane manufacturer permits.
- Rail selection affects runway beam flange width requirements.

Source: ASSUMPTION — CMAA Spec 70 guidance likely applicable; location TBD

---

## Trade-offs

| Trade-off | Option A | Option B | Recommended approach |
|---|---|---|---|
| Runway support type | Corbels on concrete building columns | Dedicated steel or concrete crane columns | TBD — structural engineer to determine based on column spacing, crane span, and crane loads. **[C-004]** Evaluation criteria for this decision should include: (1) cost impact (additional columns vs. larger column sizing for corbels), (2) constructability rating (corbel forming complexity vs. additional foundation work), (3) schedule impact (additional forming/curing time vs. independent steel column erection), (4) future flexibility (dedicated columns easier to modify independently of building structure). Source: ASSUMPTION (standard structural design evaluation factors). Proposed authority: Structural Engineer (PROPOSAL). |
| Runway beam material | Steel wide-flange (standard for crane runway) | Precast concrete runway beam | Steel wide-flange — ASSUMPTION; concrete runway beams are uncommon for this capacity. **[A-005]** Rationale: steel wide-flange sections are the industry-standard runway beam material for cranes in the 5-tonne capacity range due to favorable span-to-depth ratios, ease of rail attachment via bolted clips, field-adjustability of rail alignment, and ready availability of standard sections. Precast concrete runway beams are primarily used in heavy industrial applications (>50 tonne) where mass damping is beneficial and where precasting facilities are adjacent. For this project, the concrete structure provides the supports (columns/corbels) while steel beams provide the runway — a common hybrid configuration. Source: ASSUMPTION (standard structural engineering practice). |
| Crane arrangement | Two bridges on shared runway pair | Two independent parallel runways | TBD — dependent on bay layout confirmed in IFC drawings; App B suggests shared runway zone |
| Crane data timing | Proceed with assumed conservative wheel loads | Wait for crane supplier data before designing | ASSUMPTION: assumed loads approach may be necessary to maintain schedule; must be confirmed against actual loads |

---

## Examples

No worked examples are available from the accessible source documents. The conceptual floor plan (App B — Shop) provides spatial reference only. Detailed design examples shall be sourced from applicable CSA standards and CMAA specifications by the Structural Engineer.

---

## Future Considerations

**[E-001]** The current design scope addresses two 5-tonne overhead cranes. However, the crane support structure represents a long-life building component that may outlast the initial crane equipment. Strategic governance foresight suggests addressing the following:

- **Crane replacement or upgrade scenarios:** If the County's operational needs evolve to require higher-capacity cranes (e.g., 10-tonne), the runway beam and support structure sizing decision made now is effectively irreversible without major structural modification. The structural engineer should consider whether modest over-design of the runway supports (see Specification REQ-007-12 — Design Capacity Margin Documentation) provides meaningful future flexibility at minimal current cost.
- **Rail and runway beam replaceability:** The runway beam design should facilitate future rail replacement (bolted rail clips rather than welded) and, ideally, beam replacement without requiring structural modification to columns or corbels.
- **Electrical infrastructure growth:** The conductor bar or festoon system zone should accommodate potential future power requirements if crane capacity increases.

Source: ASSUMPTION — no explicit RFP or source requirement for future-proofing. This is a governance foresight consideration for the Owner's long-term facility planning. Proposed authority: Owner / Structural Engineer (PROPOSAL).

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CONF-007-01 | The App B (Shop) conceptual floor plan shows a "Gantry" label near the wash bay area, which could be interpreted as a third crane or separate gantry crane in addition to the two "5 TON CRANE" positions in the main bays. The decomposition (D-001, Vocabulary Map) resolves this as the same two 5-tonne cranes shown differently. However, if the wash bay requires an independent lifting device, the crane support structure scope changes materially. | App B (Shop) floor plan — "Gantry" label near wash bay | Decomposition D-001 / Vocabulary Map — "same equipment as the 5-tonne overhead cranes shown differently on drawings" | Datasheet.md — Gantry Note; Specification.md REQ-007-01; Procedure.md — Step 3 | Decomposition D-001 resolution stands pending human confirmation. If a separate gantry crane is required in the wash bay, DEL-002-07 scope and REQ-007-01 must be revised. | TBD |
| CONF-007-02 | The RFP §3.4 specifies cranes as "2 – 5-tonne overhead cranes on a trolley" (top-running implied). The App B floor plan shows two crane positions in the main shop bays. The exact runway configuration (shared runway vs. two independent parallel runways) is not confirmed in either source, affecting structural design significantly. | RFP §3.4 — "2 – 5-tonne overhead cranes on a trolley" | App B (Shop) — two "5 TON CRANE" positions visible side-by-side in main shop area | Specification.md REQ-007-01; Datasheet.md — Crane runway orientation; Guidance.md — Principles §4 | ASSUMPTION: shared runway or parallel runways both feasible; structural engineer to confirm based on crane supplier data and bay layout. Human confirmation of intended crane arrangement is recommended. | TBD |
| CONF-007-03 **[E-003]** | Multiple Specification verification rows and Procedure Step 5.2 reference "structural calculations (DEL-002-10)" as the verification method. It is unclear whether DEL-002-10 is a single calculation package covering all of PKG-002, or whether the crane support structure calculations form a dedicated, independently reviewable section within that package. If crane support calculations are embedded in a larger package without clear section boundaries, independent review of the crane support design becomes harder. | Specification.md — Verification table (multiple rows reference DEL-002-10 as verification method) | Procedure.md — Step 5.2 (DEL-002-10 coverage confirmation) | Specification.md ## Verification; Procedure.md Step 5.2 | DEL-002-10 should include a clearly identified, independently reviewable section for crane support structure calculations (PROPOSAL). Proposed authority: Structural Engineer (PROPOSAL). | TBD |

**Note [X-004]:** Conflicts CONF-007-01 and CONF-007-02 (and now CONF-007-03) carry HumanRuling = TBD. There is no defined process for how these rulings will be documented, by whom, or when. To prevent unresolved ambiguity from persisting into IFC issue: each human ruling should be recorded with (a) the ruling decision, (b) the date, (c) the rationale, and (d) the identity of the person making the ruling. Proposed authority for establishing the ruling process: Project Manager / Owner (PROPOSAL).
