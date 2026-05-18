# Decision Log — EST_DEL-04-02_2026-02-18_1100

## Decisions Applied During This Run

### DEC-EST-01: CBS Mapping Rule
**Date:** 2026-02-18
**Decision:** CBS codes assigned using CSI MasterFormat division-level proxy: 08-Doors (Division 08), 03-Concrete (Division 03), 07-Thermal (Division 07).
**Rationale:** No explicit CBS structure provided in brief or decomposition. MasterFormat divisions provide a deterministic, industry-standard mapping.
**Affected lines:** All 12 lines in Detail.csv.

### DEC-EST-02: EQ-02 Used for Overhead Door Pricing
**Date:** 2026-02-18
**Decision:** Used EQ-02 from Equipment_Pricing.csv ($13,500/each recommended) as the supply price for cold storage overhead doors rather than assembling from component rates.
**Rationale:** EQ-02 explicitly states "Cold storage building: 2 doors; standard duty" and includes motorized opener, insulation, and windows in the unit price. This is a direct match to DEL-04-02 scope (SOW-0302).
**Affected lines:** L-0402-01.

### DEC-EST-03: Person Door Pricing from Building Envelope Rates
**Date:** 2026-02-18
**Decision:** Used BE-11 ($1,800/each) from Building_Envelope_Rates.csv for person doors rather than EQ-03 ($2,000/each) from Equipment_Pricing.csv.
**Rationale:** BE-11 is the rate table entry for hollow metal door and frame (single, commercial) which is the standard item. EQ-03 exists in Equipment_Pricing.csv at a slightly higher price ($2,000) but is described identically. BE-11 was preferred as the primary rate table source for consistency with the RATE_TABLE basis. The difference is $400 total (2 doors x $200 delta).
**Affected lines:** L-0402-02.

### DEC-EST-04: Labour Included as Separate Line Items
**Date:** 2026-02-18
**Decision:** Installation labour is carried as separate line items (L-0402-08, L-0402-09, L-0402-10) rather than embedded in material unit rates.
**Rationale:** The rate table sources provide material/supply prices separately from labour rates. Separating labour provides better traceability and allows independent adjustment of labour productivity assumptions.
**Affected lines:** L-0402-08, L-0402-09, L-0402-10.

### DEC-EST-05: Scope Boundary -- Exit Lights and Switches Included
**Date:** 2026-02-18
**Decision:** Emergency exit lights (REQ-4202-11) and weatherproof switches (REQ-4202-12) are included in this estimate under DEL-04-02 rather than deferring to DEL-04-04 (Electrical).
**Rationale:** The Specification explicitly lists these as requirements of DEL-04-02. While the electrical feed is owned by DEL-04-04, the fixture/device supply and installation at door locations is part of the door/opening scope. The brief states "Door opener electrical feeds --> DEL-04-04" but does not exclude door-mounted devices from DEL-04-02.
**Affected lines:** L-0402-11, L-0402-12.

### DEC-EST-06: Fallback Not Triggered
**Date:** 2026-02-18
**Decision:** No fallback methods were used. All items were priced using RATE_TABLE evidence.
**Rationale:** FALLBACK_POLICY = STRICT, but it was not invoked because all line items had rate table evidence (direct or via reasonable assumption documented in Assumptions_Log.md). Lines L-0402-11 and L-0402-12 use `location TBD` for SourceRef but are still priced using RATE_TABLE method based on typical commercial pricing.
**Affected lines:** None required fallback.
