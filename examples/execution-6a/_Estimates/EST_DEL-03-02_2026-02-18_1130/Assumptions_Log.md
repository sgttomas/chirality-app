# Assumptions Log: EST_DEL-03-02_2026-02-18_1130

All assumptions below are required because specific quantities or design parameters are TBD at the proposal stage. Each assumption is traceable to the source that identifies the gap and to the Detail.csv line(s) affected.

## ASM-001 — Common Excavation Quantity (Cut)

| Field | Value |
|---|---|
| ID | ASM-001 |
| Assumption | Net cut volume assumed at 3,000 m3 |
| Rationale | Datasheet item B-001 states cut/fill quantities are TBD; TPN46 shows cut/fill plan but quantities are not extracted. Site is generally flat with minor grades sloping east (Geotech Report 2.1). 3,000 m3 is a conservative estimate for grade correction on a 4.5-acre developed area with minor topographic relief. |
| Affected Lines | L-003 |
| Impact if Wrong | +/- $15/m3. If actual cut is 5,000 m3, cost increases by ~$30,000. If 1,500 m3, cost decreases by ~$22,500. |
| Resolution Path | Civil engineer to extract cut/fill volumes from TPN46 or post-award topographic survey. |

## ASM-002 — Engineered Fill Quantity (Import)

| Field | Value |
|---|---|
| ID | ASM-002 |
| Assumption | Net imported granular fill assumed at 2,000 m3 |
| Rationale | Building pads require granular base (300-450 mm depth per EC-05). Additional fill may be needed for grade correction where cut is insufficient. 2,000 m3 accounts for partial import beyond what cut material can provide. |
| Affected Lines | L-004 |
| Impact if Wrong | +/- $30/m3. If actual import is 4,000 m3, cost increases by ~$60,000. Highly sensitive assumption. |
| Resolution Path | Cut/fill balance analysis required per REQ-3216. |

## ASM-003 — Subgrade Compaction Volume

| Field | Value |
|---|---|
| ID | ASM-003 |
| Assumption | Subgrade compaction volume estimated at 4,000 m3 covering building pads and primary access routes |
| Rationale | Main building pad (1,672 m2) + cold storage pad (557 m2) = 2,229 m2 at ~0.5 m depth = ~1,115 m3 for pads alone. Additional 2,885 m3 for access routes, staging areas, and areas requiring in-situ compaction. |
| Affected Lines | L-007 |
| Impact if Wrong | Moderate. At $6/m3, variance of 1,000 m3 = $6,000. |
| Resolution Path | Refined during detailed grading design. |

## ASM-004 — Drainage Swale Length

| Field | Value |
|---|---|
| ID | ASM-004 |
| Assumption | Surface drainage swale length assumed at 400 linear metres |
| Rationale | TPN46 Sheet D-1 shows a proposed drainage ditch; length not extracted. 400 lm is estimated for primary site perimeter drainage on a ~4.5-acre developed area, accounting for building perimeter drainage routing to the stormwater pond on the east side. |
| Affected Lines | L-009 |
| Impact if Wrong | At $55/lm, variance of 100 lm = $5,500. |
| Resolution Path | Measure from TPN46 or post-award site plan. |

## ASM-005 — Stormwater Retention Pond Excavation Volume

| Field | Value |
|---|---|
| ID | ASM-005 |
| Assumption | Pond excavation volume assumed at 2,500 m3 |
| Rationale | Pond shown on TPN46 Sheets C2-C4 on east side of site. Sizing criteria (design storm return period, duration, capacity, outlet flow rate) are all TBD per REQ-3212 / item F-001. 2,500 m3 is a working assumption for a municipal stormwater retention pond serving a ~4.5-acre developed site with no storm sewer. |
| Affected Lines | L-010 |
| Impact if Wrong | High. At $15/m3, variance of 1,000 m3 = $15,000. Pond may be significantly larger or smaller depending on design storm criteria. |
| Resolution Path | Civil engineer to determine pond sizing per municipal development standards (item A-003) and REQ-3212 criteria. AEPA Water Act approval status (external gate) may also affect pond design. |

## ASM-006 — Stormwater Pond Outlet Control and Protection

| Field | Value |
|---|---|
| ID | ASM-006 |
| Assumption | Outlet control structure and erosion protection priced at $15,000 lump sum |
| Rationale | No explicit rate table line item for pond outlet structures. Rate is extrapolated from EC-08 drainage rates and professional judgment for a basic outlet control structure with rip-rap energy dissipation. REQ-3218 identifies outlet design criteria as TBD. |
| Affected Lines | L-011 |
| Impact if Wrong | Moderate. Could range from $8,000 (simple rip-rap apron) to $30,000 (engineered outlet control structure). |
| Resolution Path | Civil engineer to specify outlet design per REQ-3218 and municipal standards. |

## ASM-007 — AEPA Water Act Conservative Assumptions

| Field | Value |
|---|---|
| ID | ASM-007 |
| Assumption | No explicit cost premium added for AEPA Water Act compliance, but pond and drainage estimates include conservative quantities |
| Rationale | Brief states AEPA Water Act approval PENDING. Environmental compliance costs (consultant fees) belong to DEL-03-05. Physical earthwork costs near waterway are captured in pond excavation (L-010) and drainage (L-009) at conservative quantities. If additional mitigation earthwork is required, cost increase would be incremental to L-003 and L-010. |
| Affected Lines | L-009, L-010, L-011 |
| Impact if Wrong | If AEPA requires additional setbacks or mitigation earthwork, cost could increase by $10,000-$50,000 depending on scope. |
| Resolution Path | DEL-03-05 regulatory approval process; AEPA decision. |

## ASM-008 — Topsoil Replacement and Seeding Area

| Field | Value |
|---|---|
| ID | ASM-008 |
| Assumption | Disturbed area requiring topsoil replacement and seeding estimated at 10,000 m2 |
| Rationale | Total developed area ~18,211 m2 (4.5 acres per PP-10). Subtract building footprints (~2,229 m2) and paved areas (est. ~6,000 m2 for parking, access, aprons -- priced under DEL-03-03). Remaining ~10,000 m2 of disturbed unpaved area requires restoration. |
| Affected Lines | L-012 |
| Impact if Wrong | At $11/m2, variance of 2,000 m2 = $22,000. |
| Resolution Path | Refined during detailed site plan layout (DEL-03-01 input). |

## ASM-009 — Civil Design Fee Base

| Field | Value |
|---|---|
| ID | ASM-009 |
| Assumption | Civil design fee calculated at 2.5% of DEL-03-02 construction subtotal ($460,548) |
| Rationale | Professional_Design_Fees.csv DF-02 recommends 2.5% (range 2.0%-3.0%) of site/civil construction cost. Fee base is limited to DEL-03-02 construction lines (L-001 through L-014) to avoid double-counting with DEL-03-01/03-03/03-04 design fees. |
| Affected Lines | L-015 |
| Impact if Wrong | If construction subtotal changes due to quantity refinement, design fee adjusts proportionally. At 2.5%, every $100,000 change in construction cost = $2,500 change in fee. |
| Resolution Path | Fee percentage confirmed with design team; base adjusted as quantities firm up. |
