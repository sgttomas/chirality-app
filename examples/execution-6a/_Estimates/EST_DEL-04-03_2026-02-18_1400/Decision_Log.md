# Decision Log

## Estimate Decisions

### DEC-EST-001 -- Foundation Type Selection: Screw Piles
- **Date:** 2026-02-18
- **Decision:** Selected screw piles (SC-14) as the proposed foundation system.
- **Rationale:** Geotechnical report (section 5.3) describes screw piles as "ideal" for this site. Screw piles provide superior frost-jacking resistance for unheated structures (upper helix below 2.0 m frost depth), do not require deep open excavation, and are cost-effective for light-to-moderate structural loads consistent with a PEMB cold storage building. Complies with REQ-01, REQ-02, REQ-03, REQ-04.
- **Alternatives Considered:** Shallow footings on sand/till (viable but requires 2.0 m excavation depth, potential groundwater issues); driven steel piles (viable but over-engineered for light structure; 5.3 m min embedment increases cost); post-and-frame/pole shed (Owner's cited example but geotech compliance pathway uncertain per Guidance [B-005]).
- **Source:** DEC-003 (DB proposes cost-effective foundation); Geotech Report section 5.3; Guidance > Foundation Option Assessment.

### DEC-EST-002 -- Floor System Selection: Full Concrete Slab-on-Grade
- **Date:** 2026-02-18
- **Decision:** Selected full concrete slab-on-grade (SC-03, 150mm with W/W mesh) as the proposed floor system.
- **Rationale:** Full concrete provides durable, flat operational surface suitable for equipment storage, potential forklift operations, and pallet racking. Per DEC-002, DB proposes one solution. Concrete slab provides better long-term durability than asphalt millings for an assumed 50-year design life. Concrete aprons are required at all doors regardless (REQ-06), so the incremental cost of extending concrete to the full floor is moderate vs. a hybrid asphalt millings + concrete strips approach. Sulphate-resistant mix per REQ-07.
- **Alternatives Considered:** Asphalt millings + concrete strips (lower cost, ~30-40% less for floor only, but shorter service life and less suitable for heavy equipment); no floor/gravel only (not appropriate for cold storage operations per SOW-0303).
- **Source:** DEC-002 (DB proposes one floor solution); SOW-0303; Guidance > Floor Option Assessment.

### DEC-EST-003 -- Pile Count: 20 Screw Piles
- **Date:** 2026-02-18
- **Decision:** Estimated 20 screw piles for 60'x100' clear-span PEMB.
- **Rationale:** A 60'x100' clear-span pre-engineered metal building typically has perimeter columns only (no interior columns for clear-span). Column spacing is typically 20-25 ft on the long sides and at each corner plus intermediate on the short sides. Estimated layout: long sides (100 ft) at ~20 ft spacing = 6 columns per side x 2 = 12; short sides (60 ft) at ~20 ft spacing = 4 columns per side x 2 = 8; minus 4 shared corners already counted = 16 minimum. Added 4 additional for bracing/door frame support = 20 total. This is an engineering estimate; actual count is PEMB-manufacturer-specific.
- **Source:** Typical PEMB engineering practice; PP-07 (6,000 sf footprint confirmed).

### DEC-EST-004 -- Rounding Applied: DOLLAR
- **Date:** 2026-02-18
- **Decision:** All line item amounts and totals are computed exactly, then the total is reported rounded to the nearest dollar per ROUNDING=DOLLAR control.
- **Source:** Brief optional controls.

### DEC-EST-005 -- CBS Mapping Rule
- **Date:** 2026-02-18
- **Decision:** CBS codes assigned per CSI MasterFormat divisions: 02-Sitework (below-slab preparatory work), 03-Concrete (formed/placed concrete and rebar), 05-Metals (steel piles and anchors), 31-Earthwork (excavation and subgrade prep).
- **Source:** Standard CSI MasterFormat classification; documented in Run_Context.md.

### DEC-EST-006 -- Concrete Apron Sizing
- **Date:** 2026-02-18
- **Decision:** Overhead door aprons sized at 16'x16' (matching door opening footprint = 23.8 m2 each, 2 doors = 47.6 m2, rounded to 48 m2). Person door aprons sized at approximately 1.5m x 2.0m each (2 doors = 6.0 m2). Overhead door aprons use 200mm reinforced slab (SC-04) for vehicle loads; person door aprons use 150mm mesh slab (SC-03) for pedestrian loads.
- **Rationale:** REQ-06 requires aprons at all overhead and person doors "designed for expected service vehicle loads." The 200mm reinforced rate (SC-04) is appropriate for overhead door aprons where vehicles transit; the 150mm mesh rate is adequate for person door aprons.
- **Source:** OSR section 10.3.10; SC-04 description "Heavy-duty slab for apparatus/shop bays; reinforced for vehicle loading"; SOW-0302 (2 OH doors + 2 person doors).

### DEC-EST-007 -- Granular Base Rate Derivation
- **Date:** 2026-02-18
- **Decision:** Used $15/m2 for 150mm granular base (radon rock) supply and placement.
- **Rationale:** No direct granular base line item exists in the rate tables. The SC-03 rate ($85/m2) for slab-on-grade "includes sub-base prep" per its notes, which means the granular base cost is partially embedded. However, the geotech requires a specific 150mm radon rock layer that may exceed what is included in SC-03. The $15/m2 rate is derived as a reasonable unit cost for supply and placement of screened/washed 20mm rock at 150mm depth, consistent with Alberta construction market rates. This introduces a potential double-count risk with SC-03's sub-base prep component.
- **Source:** Geotech Report section 7.1 item 6; typical Alberta granular material pricing.

### DEC-EST-008 -- Vapour Barrier Rate Derivation
- **Date:** 2026-02-18
- **Decision:** Used $5/m2 for polyethylene vapour barrier supply and installation.
- **Rationale:** No direct vapour barrier line item exists in the rate tables. The $5/m2 rate is a reasonable unit cost for 6-mil poly sheeting with laps and sealing per CAN/CGSB-51.34-M. This is a commonly used construction rate for this material.
- **Source:** REQ-08 sub-req 5; Geotech Report section 7.1 item 7; typical Alberta construction market rates.

### DEC-EST-009 -- Subgrade Preparation Rate Derivation
- **Date:** 2026-02-18
- **Decision:** Used $12/m2 for subgrade preparation (strip, scarify, compact, proof roll).
- **Rationale:** No direct subgrade preparation line item exists for building footprint work. The PB-06 parametric site rate ($16/sf = ~$172/m2) includes grading + paving + utilities + drainage + landscaping for total site area, which is far broader than building footprint subgrade prep. The $12/m2 rate is derived as a reasonable unit cost for the specific scope of stripping topsoil (~72mm), scarifying, compacting to 98% SPDD, and proof rolling a prepared building footprint. This is consistent with typical Alberta earthwork rates for a confined area.
- **Source:** Geotech Report section 7.1; PB-06 (partial reference); typical Alberta earthwork pricing.

## Scope Resolution Decisions

### DEC-EST-010 -- Excluded: Building Shell
- **Decision:** All building superstructure, cladding, roofing, and envelope costs are excluded. These belong to DEL-04-01 per cost ownership rules.

### DEC-EST-011 -- Excluded: Building Pad Preparation
- **Decision:** Rough grading, major earthworks, and site-level drainage beyond the building perimeter are excluded. These belong to DEL-03-02 per cost ownership rules. DEL-04-03 includes only the building footprint subgrade preparation and the first 3.0 m perimeter drainage (the drainage cost is not separately priced as it is a grading instruction, not a material cost).

### DEC-EST-012 -- Excluded: Electrical and Ventilation
- **Decision:** All electrical conduit, grounding, lighting, and ventilation provisions are excluded. These belong to DEL-04-04 per cost ownership rules.
