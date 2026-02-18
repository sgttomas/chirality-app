# Structural Design Brief -- Procedure

## Purpose

This procedure describes the steps for the Structural Engineer to author, coordinate, and verify the Structural Design Brief (DEL-03-03) as part of the PKG-003 Design Brief package for the Town of Penhold Public Services Building proposal (RFP 2024_004). The procedure covers production of the narrative from source review through internal sign-off.

---

## Prerequisites

| Prerequisite | Description | Status |
|--------------|-------------|--------|
| **P-PRE-01** | RFP and all Addenda reviewed | RFP: July 10, 2024; Addendum 01: July 11; Addendum 02: July 15; Addendum 03: July 31, 2024. All three must be integrated. Addendum 03 adds sumps, 16 ft doors, and solar roof requirements with structural implications. |
| **P-PRE-02** | Geotechnical Investigation Report read and key findings extracted | USG1123 (Feb 12, 2021, Union Street Geotechnical Ltd.). Minimum read: Executive Summary (pp.iv-v), §4.1.4, §4.1.5, §4.1.6, §4.2, §4.3, §5 intro + items 1-7, §5.2, §5.3, §5.5, §6, §7.1. Note the limitations section (p.v). |
| **P-PRE-03** | Structural Concept Narrative (DEL-02-03, PKG-002) is drafted or substantially in progress | This brief expands the concept narrative's rationale; both documents must be consistent and are authored by the same Structural Engineer. **Timing gate:** DEL-02-03 must be available before Step 2 (system selection) begins; if DEL-02-03 is not yet drafted, the Structural Engineer should not finalize system selection for this brief, as assumptions about structural system type could be contradicted. Confirm availability with Lead Architect before proceeding past Step 1. |
| **P-PRE-04** | Site concept plan (DEL-02-02) provides indication of site layout and potential expansion directions | Coordination with Civil Engineer on site orientation and available expansion faces. 12-acre developable site per Addendum 03 §1.1. **Timing gate:** DEL-02-02 must be available before Step 4 (expansion provisions) begins; the preferred expansion direction cannot be stated without site plan confirmation. If DEL-02-02 is not available, mark expansion direction as TBD and note the dependency. |
| **P-PRE-05** | Architectural Design Brief (DEL-03-01) provides building footprint, bay count, and adjacency layout | Minimum: know the number of apparatus bays, workshop bays, approximate bay widths, and floor plan zones. Apparatus bays 2,000-2,200 sf; workshop bays 2,000-2,200 sf per Addendum 03 §1.21. |
| **P-PRE-06** | Accessibility and Adaptability Narrative (DEL-03-06) authoring is underway | Confirm that DEL-03-06 will cross-reference the structural expansion provisions from this brief. |
| **P-PRE-07** | Confirmed equipment clearance dimensions available | Obtain confirmed heights for the tallest equipment that will use the facility: dump truck raised box height (~22 ft), grader height, Type 1 fire apparatus + ladder height. These dimensions are essential inputs for eave height determination (R-STR-09, R-STR-16). Without confirmed equipment dimensions, the eave height assumption (24-28 ft) cannot be validated. Source: Owner's equipment list or manufacturer data. ASSUMPTION: equipment list from Owner or OSR §10.3.5 provides sufficient basis; exact heights TBD. |

---

## Steps

### Step 1: Extract and document geotechnical constraints

Review USG1123 and produce a one-page internal summary note capturing the following confirmed values:

| Parameter | Value | Source |
|-----------|-------|--------|
| Stratigraphy | Topsoil / SC sand (to ~1.35 m) / CH clay (to ~3.17 m in BH101-108) / till (below) | USG1123 §4.1 |
| Clay classification | CH, high plasticity; Su avg 90 kPa (weighted; PP+SPT) | USG1123 §4.1.5 |
| Clay limitation | NOT recommended as bearing stratum for shallow foundations | USG1123 §5 items 2-3 |
| Till strength | Su avg 184 kPa; SPT N avg 32; moderate to good for deep foundations | USG1123 §4.1.6 |
| Groundwater | ~3.0-4.0 m below grade (piezometers, Feb 2021); varies near Waskasoo Creek | USG1123 §4.2, Table 4.3 |
| Sulphate class | S-2 (severe); Type HS cement, 32 MPa @ 56-day, max w/c 0.45; no calcium chloride | USG1123 §4.3 |
| Fly ash alternative | Type 10 + ~25% Type F or CI fly ash = equivalent to Type HS | USG1123 §4.3 |
| Air entrainment | Required for all concrete exposed to freeze-thaw (CAN/CSA A23.1-2014 §4.3.3) | USG1123 §4.3 |
| Frost depth | 2.0 m (Penhold region, historical data) | USG1123 §5.5.1 |
| Min pile length (unheated) | 5.3 m driven pipe pile (frost jacking resistance) | USG1123 §5.5.2 |
| Screw pile helix | Must be fully below 2.0 m frost depth | USG1123 §5.3, §5.5.2 |
| Frost heave void | 100 mm void (sand subgrade); 150 mm void (clay subgrade) under pile-supported structures | USG1123 §5.5.3 |
| Single system rule | One foundation system type per structure; mixing types not recommended | USG1123 §5 item 5 |
| Unheated structures | Shallow foundations on frost-active subgrade not recommended for unheated buildings | USG1123 §5 item 2 |
| Seismic Site Class | Site Class C; 360 < Vs < 760 m/s; Su > 100 kPa | USG1123 §6 |
| Slab: subgrade prep | Strip topsoil to native sand; compact 98% SPDD; 100% for fills >1.2 m | USG1123 §7.1 items 1-4 |
| Slab: radon sump | 100 mm diameter collection pipe, sealed top, near slab centre | USG1123 §7.1 item 5 |
| Slab: rock layer | 150 mm of 20 mm screened rock (max 10% passing 4 mm) on prepared subgrade | USG1123 §7.1 item 6 |
| Slab: vapour barrier | Polyethylene sheeting CAN/CGSB-51.34-M between rock and slab | USG1123 §7.1 item 7 |
| Slab: separation | Separation boards between grade slab and any structurally supported elements | USG1123 §7.1 item 10 |
| Slab: sleeves | Sleeves and telescoping connections for all pipes passing through slab | USG1123 §7.1 item 12 |

This note becomes internal working documentation. Key values must be carried consistently into the brief narrative.

**Verification V-01:** Internal note complete; values cross-checked against USG1123 source pages.

---

### Step 2: Select structural system and foundation type (or confirm concept selection)

Working from the Structural Concept Narrative (DEL-02-03) and geotechnical constraints:

**Main Building:**
- Confirm or select framing system type (PEMB, structural steel, CMU, or hybrid)
- Document key drivers: required clear spans for apparatus bays (column-free zone width); eave height required to clear 16 ft minimum overhead doors (16' x 16' per OSR §10.3.9) and tallest equipment (tandem dump trucks at ~22 ft dump height, graders, loaders); roof slope/orientation for solar (flat, south, west, or southwest per Addendum 03 §1.17); "car wash" grade door hardware
- Confirm foundation system: driven steel pipe piles OR screw piles bearing in till
  - If driven: open-end pipe piles; minimum embedment 5.3 m; consider PDA testing to increase phi from 0.4 to 0.5 per USG1123 §5.2.3
  - If screw: all helices below 2.0 m frost depth; shaft diameter example 140 mm, helix 508 mm; "ideal" per USG1123 §5.3
- Document commitment to single system per structure
- Document minimum 100 mm (sand) or 150 mm (clay) frost heave void under structure

**Cold Storage Building (60' x 100', unheated, 20-year design life):**
- If post-and-frame (pole shed): confirm whether helical micro-anchors are required to prevent frost heave of posts in frost-active clay zone; treated timber posts bearing on grade may heave in unheated building on CH clay subgrade -- address explicitly
- If concrete slab floor with Cold Storage Building option (OSR §10.3.8 Option 2): confirm grade-supported slab on compacted gravel per USG1123 §7.1; acknowledge frost heave potential and design approach
- Document rationale for Cold Storage structural choice relative to 20-year design life and unheated thermal condition

**Verification V-02:** System selection documented with rationale; consistent with DEL-02-03.

---

### Step 3: Develop load path narrative

Draft the load path section of the brief, addressing:

**Gravity loads:**
- Roof dead load (structural self-weight + cladding; with reserve for future solar PV installation; ASSUMPTION: minimum 15 psf solar dead load reserve -- confirm at detailed design)
- Roof live/snow load (per NBCC for Penhold, Alberta; ground snow load from NBCC Appendix C for central Alberta / Red Deer region; location TBD)
- Floor/slab live loads: apparatus bays and workshop bays to carry heavy vehicle loads (graders, dump trucks, loaders, fire apparatus -- specific loads TBD from manufacturer data at detailed design; ASSUMPTION: minimum 300-500 psf slab live load for heavy vehicle bays)

**Lateral loads:**
- Wind load: per NBCC reference wind pressure for Penhold (TBD from NBCC Appendix C)
- Seismic: per NBCC for Penhold using Site Class C (Vs = 360-760 m/s per USG1123 §6); ASSUMPTION: seismic likely not governing lateral case for central Alberta location, to be confirmed at detailed design
- Bracing system: identify whether wind/seismic resistance is provided by moment frames, braced bays, or masonry shear walls

**Slab-on-grade and sump detailing:**
- Apparatus bay and workshop bay slabs to bear on compacted gravel pad foundation on prepared subgrade (USG1123 §7.1)
- Sump locations (required in all bays per Addendum 03 §1.8): slab thickened and reinforced at penetration edges; waterproofing membrane continuity at sump box perimeter; sleeves/telescoping connections for drainage penetrations
- Radon sump: 100 mm collection pipe near slab centre, sealed top (USG1123 §7.1 item 5)
- Concrete aprons at all overhead door openings (OSR §10.3.10): aprons designed for service vehicle axle loads

**Verification V-03:** All three load categories addressed in draft narrative; slab, sump, and radon noted.

---

### Step 4: Draft future expansion provisions section

Address RFP §7.1.5 requirement with the following structure:

**Preferred expansion direction(s):** Based on site plan (DEL-02-02 coordination), identify which face(s) allow future bay addition. 12-acre developable site (Addendum 03 §1.1) provides significant expansion room. Confirm the end wall is designed as a non-load-bearing infill panel (metal stud or masonry block) that can be removed for bay extension without affecting primary structural framing.

**Framing provisions:**
- End-bay roof frames designed with connection capacity to accept future bay frames (bolted moment connections or splice plates at end-bay columns)
- Purlin and girt spacing at end bay compatible with matching future frame module
- If moment-frame structure: end columns sized to carry additional future tributary area with reserve capacity

**Foundation provisions:**
- State whether: (a) end piles are designed with reserve capacity for future expansion loads, or (b) a future pile row will be pre-installed at the expansion bay line during initial construction
- Grade beam or slab designed to be extended without full demolition; construction joint detail at expansion interface to be addressed at detailed design

**Utility provisions:**
- Structural brief notes that electrical, plumbing, and mechanical stub-outs for expansion are to be coordinated with other disciplines (cross-reference DEL-03-04, DEL-03-05, DEL-03-06)

**Verification V-04:** All four expansion sub-items (framing, foundation, direction, end wall removability) addressed.

---

### Step 5: Write and integrate the brief narrative

Combine sections from Steps 1-4 into a single coherent narrative in the following sequence:

1. **Opening paragraph:** purpose and scope of the structural brief; buildings covered; design lives (Main: 50 years; Cold Storage: 20 years)
2. **Geotechnical basis:** cite USG1123; key findings summary; limitations acknowledgement; commitment to retain qualified geotechnical services during construction
3. **Structural system selection -- Main Building:** system type; rationale (cost, flexibility, span, 50-year design life); key parameters (eave height, span, module); "car wash" grade hardware for doors
4. **Structural system selection -- Cold Storage:** system type; rationale; 20-year design life note; unheated condition addressed; frost heave design approach
5. **Foundation design approach:** system selected (driven or screw piles); why clay is not used as bearing stratum; till bearing rationale; single-system commitment; minimum embedment (5.3 m driven / helix below 2.0 m frost depth for screw); adfreezing addressed; frost heave void (100 or 150 mm)
6. **Concrete mix requirements:** sulphate class S-2; cement type; strength; w/c; no calcium chloride; air entrainment -- presented as site constraints, not optional
7. **Load path narrative:** gravity (roof dead + solar reserve, snow, heavy slab live); lateral (wind, seismic Site Class C); apparatus bay operational loads; load transfer to foundations
8. **Slab-on-grade and apparatus bay detailing:** subgrade preparation; radon sump; 150 mm screened rock + polyethylene sheet; separation boards; sump penetration detailing; aprons; sleeves
9. **Solar roof structural provisions:** reserve dead load strategy; orientation (flat/south/west/southwest); coordination with DEL-04-02
10. **Future expansion provisions:** preferred direction; end wall removability; framing provisions; foundation provisions; utility coordination note
11. **Post-disaster importance exemption status:** document whether AHJ has confirmed the exemption or note TBD with lateral design risk (R-STR-14)
12. **Geotechnical report limitations acknowledgement:** state USG1123 was prepared for Tagish Engineering Ltd., recommendations are not a design, and subsurface conditions may vary; state Design-Builder's commitment to retain qualified geotechnical services during construction (R-STR-15)
13. **OBJ-005 durability contribution:** identify structural content contributing to OBJ-005 scoring (sulphate-resistant concrete, frost protection, corrosion mitigation, design life framing) with explicit traceability (R-STR-17)
14. **Addendum 03 compliance summary:** table confirming all Addendum 03 structural items are addressed in the brief (R-STR-18)
15. **Closing statement:** commitment to Professional Engineer seal on all construction documents; geotechnical services responsibility

**Addendum 03 compliance checklist (embed or attach):**

| Addendum 03 Item | Section Reference in Brief | Requirement | Response |
|------------------|---------------------------|-------------|----------|
| Bay sumps -- all bays (§1.8) | Slab-on-grade section | R-STR-10 | Sump penetration detailing approach described |
| 16 ft minimum overhead doors (§1.10) | Structural system section | R-STR-09, R-STR-16 | Framing height accommodates 16' x 16' doors; eave height range stated |
| Solar-capable roof (§1.17) | Solar roof section | R-STR-08 | Reserve dead load strategy described; orientation stated |
| 12-acre developable site (§1.1) | Expansion provisions section | R-STR-11 | Expansion direction consistent with 12-acre site |
| Cold Storage floor system (§10.3.8) | Cold Storage system section | R-STR-02 | Floor system selection rationale included |

**Verification V-05:** All 18 requirements R-STR-01 through R-STR-18 are addressed in the narrative; Addendum 03 compliance confirmed.

---

### Step 6: Coordinate with PKG-003 lead and cross-reference deliverables

Before finalizing, confirm with Lead Architect (PKG-003 coordinator):

1. Expansion provisions in this brief are consistent with DEL-03-06 (Accessibility and Adaptability Narrative)
2. Structural system description is consistent with DEL-02-03 (Structural Concept Narrative, PKG-002)
3. Framing height and eave height assumptions are consistent with DEL-03-01 (Architectural Design Brief)
4. Solar roof structural reserve is consistent with DEL-04-02 (Mechanical Energy and Solar Readiness) and DEL-04-03 (Electrical Energy Efficiency)
5. No conflicting statements about structural system or foundation type appear in any other PKG-003 deliverable
6. Design life values (Main = 50 years; Cold Storage = 20 years) are used consistently across all PKG-003 deliverables

**Verification V-06:** Cross-reference sign-off from Lead Architect documented.

---

### Step 7: Final review and package for proposal

1. Confirm Professional Engineer's name and registration number are stated in brief (seal commitment or actual seal)
2. Confirm all terminology is consistent with other PKG-003 deliverables (e.g., "Main Building" not "PSB" or "main structure" inconsistently; "Cold Storage Building" not "cold storage")
3. Confirm all design life references are correct: Main Building = 50 years; Cold Storage = 20 years
4. Confirm Addendum 03 requirements are integrated (not only the base RFP): sumps, 16 ft doors, solar roof
5. Confirm no statements contradict the geotechnical report limitations: USG1123 is background information for the Design-Builder; subsurface conditions may vary
6. Confirm geotechnical services responsibility acknowledged per OSR §10.3.6: "Design-Builder is also responsible for retaining all necessary geotechnical services required to safely excavate material, certify imported material, certify the exposed and prepared subgrade"
7. Deliver to Proposal Manager for inclusion in PDF assembly (DEL-01-02)

**Verification V-07:** Final review checklist complete; brief cleared for proposal assembly.

---

## Verification Summary

| Verification ID | Check | Method |
|-----------------|-------|--------|
| V-01 | Geotechnical constraints extracted accurately with specific values | Internal note cross-checked against USG1123 source pages |
| V-02 | System selection documented with rationale; Cold Storage unheated condition addressed | Structural Engineer self-review |
| V-03 | All three load categories addressed; slab, sump, radon noted | Structural Engineer self-review |
| V-04 | Four expansion sub-items addressed (framing, foundation, direction, end wall) | Lead Architect review |
| V-05 | All 18 requirements (R-STR-01 to R-STR-18) present in narrative; Addendum 03 checklist complete | Lead Architect review |
| V-06 | Cross-references consistent with other PKG-003 deliverables; design life values confirmed | Lead Architect sign-off |
| V-07 | Final review checklist; PE commitment; geotechnical services responsibility confirmed | Proposal Manager |

---

## Records

| Record | Description | Where Filed |
|--------|-------------|-------------|
| Geotechnical constraints summary note (internal) | Working document from Step 1; table of confirmed USG1123 values | Structural Engineer project folder |
| System selection rationale note (internal) | Working document from Step 2; driven vs. screw trade-off documented | Structural Engineer project folder |
| Structural Design Brief narrative (final) | Primary deliverable; included in proposal PDF | DEL-03-03 folder; proposal assembly package |
| Cross-reference sign-off (from Lead Architect) | Confirmation of consistency across PKG-003 deliverables | DEL-03-03 folder |
| Addendum 03 compliance checklist | Confirmation that Addendum 03 structural items are addressed | DEL-03-03 folder or within brief narrative |

---

## Notes

**Pitfall 1:** Do not rely solely on the base RFP without integrating Addendum 03. Addendum 03 (Jul 31, 2024) adds bay sumps (§1.8), 16 ft overhead doors (§1.10), and solar-capable roof requirements (§1.17) that directly affect structural design. These must appear in the brief.

**Pitfall 2:** Do not describe shallow footings as a viable option for the Cold Storage Building without acknowledging the unheated condition and its interaction with frost-active clay. USG1123 §5 item 2 explicitly states that construction of unheated on-grade structures with movement-sensitive foundations is not recommended at this site.

**Pitfall 3:** Do not omit frost design specifics. The geotechnical report provides concrete values: frost depth = 2.0 m; minimum pile embedment (unheated) = 5.3 m; adfreezing stress = 100 kPa in fine-grained frozen soil above 2.0 m; frost heave void = 100 mm (sand) or 150 mm (clay). Using these values signals site-specific competence.

**Pitfall 4:** Do not describe the geotechnical report findings as if they are guarantees or if they were prepared for this Design-Builder. USG1123 was prepared for Tagish Engineering Ltd. The limitations section is explicit: "Our recommendations and conclusions are based upon the information obtained from the subsurface exploration... subsurface conditions may vary between the boreholes and over time." The brief should acknowledge this and note that the Design-Builder will retain qualified geotechnical services during construction.

**Pitfall 5:** Do not omit the single-foundation-system commitment (USG1123 §5 item 5). Mixing foundation types under the same structure is explicitly discouraged. Proposing mixed systems in the brief would raise a flag for technical reviewers.

**Pitfall 6:** Do not omit the radon sump requirement (USG1123 §7.1 item 5). The geotechnical engineer recommends a radon mitigation provision for the grade-supported slab. Including this in the brief signals thoroughness and occupant health awareness.

**Pitfall 7:** Do not mix "design life" of the building with the "warranty period" of 12 months. The 50-year and 20-year design life figures are performance life expectations used to frame material and system selections, not warranty commitments.
