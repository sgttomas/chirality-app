# Guidance — DEL-002-05 Mezzanine Framing Details

**Document Type:** Guidance (Directional)
**Deliverable ID:** DEL-002-05
**Deliverable Name:** Mezzanine Framing Details
**Revision:** R1 — 2026-02-26 (Pass 3 enrichment)
**Status:** SEMANTIC_READY

---

## 1. Purpose

This document explains **why** the Mezzanine Framing Details deliverable (DEL-002-05) exists, what design intent it must satisfy, and how the Structural Engineer of Record should approach key decisions. It is a directional companion to the normative Specification.md and is intended to make later Working Items sessions productive by surfacing the key principles, considerations, and known uncertainties.

### 1.1 Why this deliverable exists

The RFP explicitly requires a mezzanine storage level above the Parts Room, Utility Room, and Wash Bay of the New North Shop addition (R-01 §3.4; R-04 App B notes). The Owner's purpose is to provide elevated storage for heavy industrial consumables — primarily oil totes and oil pumping equipment — that must be kept accessible but off the main shop floor to preserve vehicle and equipment circulation space below.

This deliverable documents the structural system that achieves that function. It is a distinct drawing set within PKG-002 because the mezzanine introduces a secondary structural level within an otherwise single-storey concrete industrial building, requiring its own framing plan, sections, connection details, and stair details.

---

## 2. Principles

### 2.1 The mezzanine is a heavy-storage structure, not a light-occupancy one

The Owner's stated program — "several oil totes and oil pumping equipment" — implies point loads and distributed loads substantially above standard office or light storage mezzanines. An IBC tote (1,000 L) filled with oil weighs approximately 870–1,000 kg. Multiple totes placed in proximity can generate live loads significantly above the NBC minimum for light storage occupancies. The Structural Engineer of Record must:

1. Obtain from the Owner (or assume conservatively) the maximum number and arrangement of totes and equipment to be stored simultaneously.
2. Calculate the resulting design live load and compare to the ABC minimum for the applicable occupancy category.
3. Use the higher of the two values as the design live load.
4. State the design live load explicitly on the drawings.

Source: R-01 §3.4 ("capable of handling heavy items such as several oil totes and oil pumping equipment"); R-04 (App B notes: "Load Bearing Over Parts Room + Utility For Storage").

### 2.2 The mezzanine sits within a concrete-dominant building

The primary structure of the New North Shop is concrete (R-01 §3.4; R-04). The mezzanine framing will interface with this concrete structure at bearing points and column bases. The connection strategy must be designed early because:
- Post-installed anchors into concrete are less efficient and more inspection-intensive than cast-in-place embedments.
- If mezzanine column locations are known before concrete pours, cast-in-place anchor bolts or embed plates can be specified, reducing construction risk.
- Coordination with the concrete formwork / construction sequence is therefore a critical interface between DEL-002-05 and the construction scheduling.

ASSUMPTION: Cast-in-place embeds are preferred where column base locations can be confirmed before slab or wall pours. This is a design decision for the Structural Engineer of Record to confirm.

### 2.3 The stair is structurally part of this deliverable

The Appendix B floor plan shows "Stairs to Mezzanine" at the utility room / cistern boundary. The stair must be structurally framed and detailed — not assumed as a prefabricated unit or deferred to fit-out. Stair geometry, code compliance (ABC rise/run, handrail height), and integration with the mezzanine framing and main floor slab must all appear in this drawing set.

Note: DEL-002-09 is listed as a separate "Stair Details" deliverable in the decomposition. The Structural Engineer of Record should confirm scope boundaries between DEL-002-05 and DEL-002-09 to avoid gaps or duplication. See Conflict Table below.

### 2.4 Guardrails are a life-safety element

The mezzanine edge must be guarded per ABC. Guardrail design (height, spacing, load resistance) is a code-minimum requirement and must be explicitly detailed, not left to the contractor. Guardrail details are part of this drawing set.

---

## 3. Considerations

### 3.1 Mezzanine framing system selection

Two principal systems are available for industrial mezzanines within a concrete building:

**Option A — Steel framing (beams and columns):**
- Typical for industrial applications.
- Columns bear on concrete slab (base plate + anchor bolts).
- Beams span between columns and may bear on concrete walls or corbels.
- Deck: steel grating, concrete-on-composite deck, or checker plate.
- Advantages: speed of erection, clear-span capability, easy penetration routing.
- Disadvantages: requires fire protection consideration per ABC occupancy (TBD — see REQ-DS-017); corrosion protection for wash bay exposure (see REQ-DS-015).

**Option B — Concrete mezzanine (cast-in-place or precast):**
- Consistent with primary building material.
- Monolithic behavior; better durability in wash bay environment.
- Disadvantages: heavier; increased forming cost; less flexible for future modifications; requires earlier design commitment before slab pours.

ASSUMPTION: Steel framing is the more likely selection given industrial program, speed requirements, and typical practice for secondary-level mezzanines in concrete shop buildings. The Structural Engineer of Record should confirm.

Source: R-01 §3.4; R-04; ASSUMPTION (no explicit framing material specified in source documents).

### 3.2 Clearance below the mezzanine

The mezzanine floor height must leave adequate clearance below for:
- Fork truck or telehandler access to the parts room and utility room (TBD — Owner to confirm if fork access is required under the mezzanine).
- Overhead crane operation in the main shop — the crane rails are in the main bays, not over the mezzanine zone, but proximity must be confirmed.
- Wash bay operations: vehicles entering the wash bay will require door clearance and operational headroom. The wash bay is 24' wide (R-04 App B). The mezzanine overhead in the wash bay must not conflict with vehicle height or wash equipment.

ASSUMPTION: The mezzanine height above the main floor in the wash bay area must be confirmed against the largest vehicles (motor scraper class — R-01 §3.4). If the mezzanine conflicts with vehicle access, the structural design must address this (e.g., eliminate mezzanine over wash bay, or raise mezzanine height).

**This is a key coordination item** with the Architect (PKG-001) and Owner before the mezzanine elevation is fixed.

### 3.2.1 Mezzanine over Wash Bay — Value Assessment (C-004)

The mezzanine extent over the wash bay (per CF-DS-002) introduces additional structural and environmental complexity:
- **Additional structural complexity:** The wash bay span (24' wide per R-04) adds to the framing extent and may require additional columns or longer beam spans.
- **Corrosion protection cost:** Steel framing over the wash bay requires enhanced corrosion protection (see REQ-DS-015, §3.3 below), adding material and maintenance cost.
- **Vehicle clearance risk:** Motor scraper-class vehicles (R-01 §3.4) in the wash bay may conflict with mezzanine underside, potentially requiring the mezzanine to be raised or eliminated over this zone.

**Whether the incremental storage area gained by extending the mezzanine over the wash bay justifies this additional cost and complexity is TBD.** The Owner should evaluate whether the additional storage footprint over the wash bay (approximately 24' x the mezzanine depth) is operationally necessary relative to the cost/complexity premium. This evaluation links directly to the resolution of CF-DS-002 in the Conflict Table.

Source: R-01 §3.4 (wash bay); R-04 (App B — 24' wash bay width); Guidance §3.3 (corrosion); CF-DS-002 (Conflict Table).

### 3.3 Wash bay environment — corrosion and drainage

The wash bay is a wet, corrosive environment due to vehicle washing, mud, and chemical cleaners. Any steel framing elements within or above the wash bay require appropriate corrosion protection:
- Hot-dip galvanizing or appropriate paint system per applicable standards (see REQ-DS-015).
- Drainage must not be obstructed by mezzanine framing members.

Source: R-01 §3.4 (wash bay / mud sump); ASSUMPTION regarding corrosion protection — location TBD in applicable standards.

### 3.4 Coordination with cistern / water storage below

The Appendix B floor plan shows 50,000 L water storage in the utility room area, with the mezzanine stair also in this zone. The structural engineer must confirm:
- Column locations do not conflict with the cistern footprint or maintenance access.
- Stair location is confirmed with plumbing designer (PKG-006) and architect (PKG-001).

Source: R-04 (App B floor plan — "50,000 L Water Storage" label, "Stairs to Mezzanine" label in same zone).

### 3.5 Code edition confirmation

The exact edition of the Alberta Building Code applicable to this project is TBD pending building permit application. The Structural Engineer of Record must confirm the applicable code edition with the Camrose County permit authority before final design.

Source: R-01 §3.3.2 (requires compliance with "all applicable building codes and regulations").

---

## 4. Trade-offs

| Trade-off | Option A | Option B | Recommended Approach | Source |
|---|---|---|---|---|
| Mezzanine framing material | Steel (faster, lighter, flexible) | Concrete (durable, monolithic) | Confirm with Structural Engineer of Record — steel typical for this application (ASSUMPTION) | R-01 §3.4; ASSUMPTION |
| Deck system | Grating (open — drainage-friendly, but requires careful safety consideration in parts room) | Concrete-on-deck (solid — better for heavy loads, easier to walk on) | Concrete-on-composite deck preferred for heavy storage (ASSUMPTION); grating may be appropriate over wash bay for drainage | ASSUMPTION |
| Cast-in embeds vs. post-installed anchors | Cast-in: lower risk, lower cost, requires early coordination | Post-installed: flexible timing, higher inspection requirement, potentially higher cost | Cast-in embeds preferred where column locations fixed early (ASSUMPTION) | ASSUMPTION |
| Stair scope: DEL-002-05 vs. DEL-002-09 | Include stair in this set (single point of coordination) | Separate stair set (DEL-002-09) | See Conflict Table below — requires human ruling | Decomp §7 PKG-002 |

### 4.1 Deck System Selection Criteria (A-005, D-003)

The deck system choice significantly affects cost, maintenance, load distribution, and operational suitability. The following evaluation criteria should guide the Owner and Structural Engineer of Record in selecting the deck system. **The criteria below are directional; the Owner should weight them based on operational priorities.**

| Criterion | Grating Deck | Concrete-on-Composite Deck | Checker Plate | Source / Basis |
|---|---|---|---|---|
| **Load capacity** | Suitable for moderate distributed loads; concentrated loads require thicker sections or closer support spacing | Excellent for heavy distributed and concentrated loads (oil totes, equipment) | Good for moderate loads; deformation under heavy concentrated loads possible | ASSUMPTION — standard practice for industrial mezzanines |
| **Forklift/pallet jack traffic** | Unsuitable for rubber-tired equipment unless bar spacing is very close | Suitable — solid surface supports wheeled traffic | Suitable but may be slippery when oily | ASSUMPTION |
| **Drainage (wash bay zone)** | Excellent — open grating allows water and wash effluent to pass through | Poor — solid surface requires floor drains and slope design | Poor — solid surface requires drainage provisions | ASSUMPTION |
| **Maintenance / cleanability** | Difficult to clean; debris falls through | Easy to clean; standard shop floor maintenance | Moderate; oil collects in checker plate pattern | ASSUMPTION |
| **Approximate cost relative to grating (ASSUMPTION)** | Baseline | Higher (concrete topping, formwork, curing time) | Moderate | ASSUMPTION — no project-specific pricing available; order-of-magnitude comparison only |
| **Schedule impact** | Fast erection | Slower (concrete pour + cure) | Fast erection | ASSUMPTION |

> **TBD (A-005, D-003):** The Owner should confirm the following to support deck system selection:
> - Will forklift or pallet jack traffic operate on the mezzanine?
> - Is drainage through the deck required over the wash bay zone?
> - What is the Owner's priority weighting among load capacity, cost, schedule, and maintenance?
>
> Source: Guidance §3.1 options; Guidance §4 Trade-offs table.

### 4.2 Comparative Merit Summary — Framing/Deck Systems (F-004)

The following provides an order-of-magnitude comparison to support the Owner's decision. **All values are ASSUMPTION — no project-specific cost estimates are available. These are directional only.**

| System | Approximate Relative Cost | Approximate Schedule Impact | Key Maintenance Consideration |
|---|---|---|---|
| Steel framing + grating deck | Low–Moderate | Fastest (shop-fabricated, bolted erection) | Minimal structural maintenance; grating replacement straightforward |
| Steel framing + composite deck | Moderate–High | Moderate (concrete pour + cure adds 2–4 weeks — ASSUMPTION) | Concrete surface may crack under heavy loads; repair more complex |
| Concrete mezzanine | High | Slowest (forming, rebar, pour, cure, strip — adds 4–8 weeks — ASSUMPTION) | Most durable; lowest long-term maintenance; hardest to modify |

Source: ASSUMPTION — no project-specific data. Order-of-magnitude comparisons based on typical industrial construction practice. Structural Engineer of Record and Contractor should provide project-specific estimates before Owner decision.

---

## 5. Examples

No direct precedent examples are available from the accessible source documents. The following is contextual only:

- The Appendix B floor plan (R-04) shows the mezzanine labeled as "2nd Level Mezzanine Coffee Room" in the Old North Shop and "Overhead Mezzanine over Parts Room/Utility Room/Wash Bay" in the New North Shop. These are two distinct structures. Only the New North Shop mezzanine is within scope of DEL-002-05.
- Stair access to the Old North Shop mezzanine coffee room is not detailed in the available conceptual drawings. Its renovation (SOW-0071) is an architectural scope item in PKG-001/PKG-017, not structural design in PKG-002.

---

## 6. Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority (PROPOSAL) | Human Ruling |
|---|---|---|---|---|---|---|
| CF-DS-001 | Scope boundary between DEL-002-05 (Mezzanine Framing Details) and DEL-002-09 (Stair Details): the stair to the mezzanine could logically belong to either deliverable. The decomposition lists both as separate deliverables in PKG-002 but does not explicitly state which deliverable includes the mezzanine access stair structural details. | Decomp §7 PKG-002: DEL-002-05 "Mezzanine Framing Details" | Decomp §7 PKG-002: DEL-002-09 "Stair Details" | Specification.md §1.1 Scope; Procedure.md Step 3; drawing sheet list | PROPOSAL: Mezzanine access stair structural details be included in DEL-002-05 (this set), with DEL-002-09 covering any other stairs (e.g., if there are stairs to the service pit or other levels). Cross-reference between the two sets. Ruling required to confirm. | TBD |
| CF-DS-002 | The RFP §3.4 states "Mezzanine storage above utility and parts room..." — it does not explicitly mention the wash bay as a mezzanine location. However, Appendix B floor plan notes explicitly state "Overhead Mezzanine over Parts Room/Utility Room/Wash Bay." The scope of the mezzanine's lateral extent (whether it covers the wash bay or stops short) affects the structural system complexity and cost. See also §3.2.1 for value assessment. | R-01 §3.4 (text: mentions utility + parts room only) | R-04 App B (drawing notes: explicitly includes wash bay) | Specification.md REQ-DS-001; Datasheet.md §2.1; Procedure.md Step 3 | PROPOSAL: Follow Appendix B drawing notes (more detailed and more recent intent) — mezzanine spans over parts room, utility room, AND wash bay. However, structural engineer should confirm with Owner whether mezzanine over wash bay is structurally practical given vehicle clearance requirements. | TBD |

---

## 7. Vocabulary Note (X-004)

**Terminology normalization for construction inspection records:**

The following terms are used across the four production documents to describe inspection and review records generated during and after construction. To avoid confusion, the following vocabulary is established:

| Preferred Term | Meaning | Documents Using Variant Terms |
|---|---|---|
| **Field review report** | Written record produced by the Structural Engineer of Record documenting a site visit, observations, and any directives issued during construction. This is the design professional's record. | Procedure.md (Steps 5, 7, Records); Specification.md §4 uses "site inspection" in some contexts |
| **Inspection report** | Written record produced by or for the Safety Code authority (Camrose County inspector) documenting compliance inspection results. Copies provided to County per SOW-0085. | Specification.md §5.2; Procedure.md §5 Records |
| **Site review** | General term for a physical visit to the construction site by any party. Not a formal record type. | Procedure.md Step 7 |

> **Note (X-004):** "Field review report" and "inspection report" are distinct record types with different authors and purposes. Where earlier document text uses "site inspection" or "site review" interchangeably with either of these, the preferred terms above should govern interpretation. Source: Specification.md §4 (Field Verification); Procedure.md Steps 5, 7, and §5 Records.
