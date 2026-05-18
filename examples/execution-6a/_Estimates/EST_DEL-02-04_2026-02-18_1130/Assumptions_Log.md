# Assumptions Log — EST_DEL-02-04_2026-02-18_1130

All assumptions are explicitly identified. Each assumption affects quantity derivation or rate selection and is traceable to specific Detail.csv line items.

## Geometric / Quantity Assumptions

### ASM-01: Building Footprint Area
- **Assumption:** Main PSB ground floor area is 18,000 sf (1,672 m2), based on functional program layout with 4 fire bays + 4 PW bays + office/admin + support spaces, with approximate dimensions ~160 ft x 110 ft.
- **Source:** PP-05 (Assumed_Project_Parameters.csv)
- **Confidence:** MEDIUM
- **Impact:** HIGH — affects nearly all line items (slab, roof, steel, envelope)
- **Affected Lines:** L-006, L-007, L-009, L-010, L-011, L-015, L-025, L-026

### ASM-02: Building Perimeter
- **Assumption:** Building perimeter is approximately 540 lf (165 lm), based on ~160 ft x 110 ft rectangular footprint.
- **Source:** Derived from PP-05 dimensional notes
- **Confidence:** MEDIUM
- **Impact:** HIGH — affects wall panels, masonry base, flashing, foundation perimeter items
- **Affected Lines:** L-004, L-013, L-014, L-017, L-018

### ASM-03: Bay Area
- **Assumption:** Total bay area (fire apparatus + PW shop) is approximately 12,000 sf (1,115 m2), based on 8 bays at approximately 1,500 sf each.
- **Source:** Derived from PP-11 (4 fire bays) + PP-12 (4 PW bays); bay size estimated from 16x16 ft doors + circulation/work space
- **Confidence:** MEDIUM
- **Impact:** MEDIUM — affects heavy-duty slab and bay floor sealer
- **Affected Lines:** L-006, L-025

### ASM-04: Office/Shared Area
- **Assumption:** Office and shared space area is approximately 6,000 sf (557 m2), calculated as 18,000 sf total minus 12,000 sf bay area.
- **Source:** Derived from PP-05 minus ASM-03
- **Confidence:** MEDIUM
- **Impact:** MEDIUM — affects standard slab and office floor sealer
- **Affected Lines:** L-007, L-026

### ASM-05: Average Wall Height
- **Assumption:** Average exterior wall height is 6.5 m (21.3 ft), accommodating 16 ft minimum clear door height plus structural depth and parapet.
- **Source:** Derived from SOW-0215 (16 ft min clear height) plus assumed structural depth and parapet
- **Confidence:** MEDIUM
- **Impact:** MEDIUM — affects gross wall area and all envelope quantities
- **Affected Lines:** L-013, L-014, L-016

### ASM-06: Gross Wall Area
- **Assumption:** Gross exterior wall area is approximately 1,073 m2 (perimeter 165 lm x average height 6.5 m).
- **Source:** Derived from ASM-02 x ASM-05
- **Confidence:** MEDIUM
- **Impact:** MEDIUM — base for net wall panel and masonry calculations
- **Affected Lines:** L-013, L-014, L-016

## Foundation Assumptions

### ASM-07: Screw Pile Count
- **Assumption:** 48 screw piles at approximately 3.5 m spacing around perimeter and at interior column lines.
- **Source:** Typical spacing for steel-framed institutional building on screw pile foundations; consistent with SC-14 description for Penhold soils
- **Confidence:** MEDIUM
- **Impact:** HIGH — directly determines foundation cost ($144,000)
- **Affected Lines:** L-001

### ASM-08: Pile Cap / Grade Beam Concrete Volume
- **Assumption:** Total concrete volume for pile caps and grade beams is 38 m3 (48 caps x ~0.4 m3 average + ~19 m3 grade beams).
- **Source:** Typical pile cap dimensions for screw pile foundations; grade beam between perimeter piles
- **Confidence:** MEDIUM
- **Impact:** LOW — $14,630 total
- **Affected Lines:** L-002

### ASM-09: Foundation Formwork (Pile Caps + Grade Beams)
- **Assumption:** 180 m2 of formwork for pile caps and grade beams combined.
- **Source:** Estimated from 48 caps x ~2 m2/cap + grade beam faces
- **Confidence:** MEDIUM
- **Impact:** LOW — $11,700 total
- **Affected Lines:** L-003

### ASM-10: Foundation Wall Formwork
- **Assumption:** Perimeter frost wall/stem wall formwork is 165 m2 (165 lm x ~1.0 m height average, both sides).
- **Source:** Typical frost wall depth for Penhold, AB climate
- **Confidence:** MEDIUM
- **Impact:** LOW — $12,375 total
- **Affected Lines:** L-004

### ASM-11: Reinforcing Steel Quantity (Foundations)
- **Assumption:** 4,800 kg of reinforcing steel for foundation system (~100 kg per pile cap average including grade beam rebar).
- **Source:** Typical reinforcing ratios for pile caps and grade beams
- **Confidence:** MEDIUM
- **Impact:** LOW — $15,600 total
- **Affected Lines:** L-005

### ASM-12: Anchor Bolt Count
- **Assumption:** 96 anchor bolts (2 per pile cap x 48 piles).
- **Source:** Minimum 2 anchor bolts per column base plate; conservative (some may require 4)
- **Confidence:** MEDIUM
- **Impact:** LOW — $4,320 total
- **Affected Lines:** L-008

## Structural Steel Assumptions

### ASM-13: Primary Steel Tonnage
- **Assumption:** Primary structural steel (W-shapes and HSS) is approximately 42,000 kg (~25 kg/m2 of building footprint x 1,672 m2).
- **Source:** Typical steel intensity for single-storey steel-framed institutional/municipal buildings with clear-span bays. Range is typically 20-30 kg/m2; 25 kg/m2 used as mid-range.
- **Confidence:** MEDIUM
- **Impact:** HIGH — $273,000 (largest single line item by amount)
- **Affected Lines:** L-009

### ASM-14: Miscellaneous Steel
- **Assumption:** 3,500 kg of miscellaneous steel (stairs, handrails, platforms, embed plates, lintels).
- **Source:** Typical for building of this size; ~2 kg/m2 of footprint
- **Confidence:** MEDIUM
- **Impact:** LOW — $31,500 total
- **Affected Lines:** L-012

## Envelope Assumptions

### ASM-15: Net Wall Panel Area (Insulated Metal Panels)
- **Assumption:** 730 m2 of insulated metal wall panels. Calculated as: gross wall area (1,073 m2) minus masonry base (200 m2) minus glazing/window openings (54 m2) minus overhead door openings (8 doors x ~23.5 m2/door = ~188 m2). Net = 1,073 - 200 - 54 - 188 = ~631 m2. Adjusted upward to 730 m2 to account for panel waste, returns at openings, and soffit areas.
- **Source:** Derived from ASM-06 minus deductions; waste/returns factor applied
- **Confidence:** MEDIUM
- **Impact:** MEDIUM — $135,050 total
- **Affected Lines:** L-013

### ASM-16: Masonry Base Course Area
- **Assumption:** 200 m2 of 200mm CMU base course at approximately 1.2 m height around the full perimeter (165 lm x 1.2 m).
- **Source:** Typical for municipal/institutional metal buildings with impact-resistant masonry base
- **Confidence:** MEDIUM
- **Impact:** LOW — $35,000 total
- **Affected Lines:** L-014

### ASM-17: Flashing and Trim Length
- **Assumption:** 380 lm of metal flashing and trim (corners, drip edges, window heads/sills, parapet cap, base flashing). Approximately 2.3x the building perimeter to account for multiple runs.
- **Source:** Typical for insulated metal panel buildings
- **Confidence:** MEDIUM
- **Impact:** LOW — $12,160 total
- **Affected Lines:** L-017

### ASM-18: Sealant Length
- **Assumption:** 520 lm of perimeter sealant at all openings, joints, and panel transitions. Approximately 3.1x the building perimeter.
- **Source:** Typical for insulated metal panel buildings with multiple opening types
- **Confidence:** MEDIUM
- **Impact:** LOW — $8,320 total
- **Affected Lines:** L-018

## Opening Assumptions

### ASM-19: Glazing Area
- **Assumption:** 54 m2 of commercial glazing, approximately 5% of gross wall area.
- **Source:** Typical for municipal operations facility; lower glazing ratio than office buildings due to bay/shop functions
- **Confidence:** MEDIUM
- **Impact:** LOW — $35,100 total
- **Affected Lines:** L-020

### ASM-20: Storefront Entries
- **Assumption:** 2 storefront entries (main public entry + secondary entry).
- **Source:** Typical for combined fire hall / public works building with separate public-facing and operational entries
- **Confidence:** MEDIUM
- **Impact:** LOW — $16,000 total
- **Affected Lines:** L-021

### ASM-21: Person Door Count (Single)
- **Assumption:** 12 single hollow metal person doors for bay access, service exits, and code-required egress.
- **Source:** Estimated based on 8 bays requiring egress doors + additional service/exterior doors per code requirements
- **Confidence:** MEDIUM
- **Impact:** LOW — $21,600 total
- **Affected Lines:** L-022

### ASM-22: Person Door Count (Double)
- **Assumption:** 2 sets of double hollow metal doors at main corridor/bay transitions.
- **Source:** Typical for separation between office/admin and bay areas in firehall/PW buildings
- **Confidence:** MEDIUM
- **Impact:** LOW — $6,800 total
- **Affected Lines:** L-023

## Other Assumptions

### ASM-23: Sump Rough-In Rate
- **Assumption:** Sump rough-in (blockout in structural slab) is estimated at $750 per location. This covers formwork, blockout framing, and PVC sleeve cast into the 200mm slab. The sump assembly, oil/water separator, and plumbing connection costs are excluded (DEL-02-05 scope per cost ownership rules).
- **Source:** Not directly from rate tables. Informed by MS-10 (bay sump assembly at $4,500 complete) with rough-in estimated as approximately 15-20% of complete assembly cost. This is a LOW confidence assumption.
- **Confidence:** LOW
- **Impact:** LOW — $6,000 total (8 x $750)
- **Affected Lines:** L-027
