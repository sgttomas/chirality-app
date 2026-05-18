# Datasheet: DEL-05-06 — Option: Appliances & Laundry

## Identification

| Field | Value |
|---|---|
| **Deliverable ID** | DEL-05-06 |
| **Name** | Option — Appliances & Laundry |
| **Package** | PKG-005 — Optional Priced Items & Owner-Elected Additions |
| **Discipline** | Kitchen / Laundry |
| **Type** | Optional scope package (4-doc bundle) |
| **Responsible Party** | Design-Builder |
| **Scope Item** | SOW-0505 |
| **Supported Objective** | OBJ-010 |
| **Status** | Optional — not included in base price; Owner-elected |
| **Source Authority** | OSR §12.6 (RFP Appendix A, page 45); Functional Program §16.0 (RFP Appendix B, page 46) |

---

## Attributes

### Minimum Appliance List (from OSR §12.6 and Functional Program §16.0)

| Item | Minimum Quantity | Description | Source |
|---|---|---|---|
| Refrigerator with freezer | 2 | Residential-grade (default per Guidance P4); full-size with freezer compartment | OSR §12.6; Functional Program §16.0; Guidance P4 |
| Microwave | 2 | Counter-top or over-range; residential-grade acceptable | OSR §12.6; Functional Program §16.0 |
| Stove / oven with range hood | 1 set | Stove and oven combination; range hood included. **TBD (Semantic Lensing B-003):** Gas or electric fuel type not specified in OSR §12.6 -- affects rough-in scope, code compliance, and pricing | OSR §12.6; Functional Program §16.0 |
| Dishwasher | 1 | Built-in dishwasher; residential-grade acceptable | OSR §12.6; Functional Program §16.0 |
| Residential laundry set (washer + dryer) | 2 | Full laundry sets; washer and dryer per set | OSR §12.6 |

**Note:** OSR §12.6 states these as minimum quantities; Design-Builder may propose additional or upgraded items as part of the option pricing. The Functional Program §16.0 (Lunch Room/Kitchen) corroborates 2 fridges, range, stove, range hood, 2 microwaves, sink, and dishwasher for the kitchen area.

### Utility Connection Requirements *(Enrichment: B-002, Semantic Lensing -- MissingSlot)*

| Appliance Category | Electrical | Plumbing | Ventilation | Source |
|---|---|---|---|---|
| Refrigerator with freezer | **TBD** (typical: 120V/15A dedicated circuit per unit) | None typically required | None | ASSUMPTION (typical residential appliance requirements) |
| Microwave | **TBD** (typical: 120V/20A dedicated or shared circuit) | None | None | ASSUMPTION |
| Stove/oven | **TBD** (typical: 240V/40-50A dedicated circuit if electric; or gas supply + 120V if gas -- see B-003 TBD on fuel type) | None (unless gas -- gas supply line TBD) | Range hood exhaust duct -- **TBD** size and termination | ASSUMPTION |
| Dishwasher | **TBD** (typical: 120V/15A dedicated circuit) | Hot water supply, drain connection | None | ASSUMPTION |
| Residential washer | **TBD** (typical: 120V/15A dedicated circuit) | Hot and cold water supply, drain per set | None | ASSUMPTION |
| Residential dryer | **TBD** (typical: 240V/30A dedicated circuit if electric; or gas supply + 120V if gas) | None (condensate drain if condensing type) | Dryer exhaust duct per set -- **TBD** size and termination | ASSUMPTION |

**Note:** All electrical and plumbing data above is marked **TBD** pending DB basis-of-design appliance selections. Actual requirements depend on specific make/model. DB to confirm in Installation Coordination Notes (REQ-05-06-004).

### Location Context

| Area | Applicable Appliances |
|---|---|
| Lunch Room / Kitchen (Functional Program room 16.0) | Refrigerators, microwaves, stove/oven with range hood, dishwasher |
| Laundry / Locker Room area (Functional Program room 22.0 — ASSUMPTION: best-effort location) | Residential laundry sets (washers and dryers) |

**ASSUMPTION:** The laundry sets are located in or adjacent to the unisex locker room washing facility (Functional Program room 22.0). OSR §12.6 does not specify a room number; location is inferred from facility program context. **TBD (B-001, Semantic Lensing):** Confirm laundry set location with Owner or design team -- is it Functional Program room 22.0 (Unisex Locker Room) or another designated laundry room? This is an essential fact affecting rough-in design.

---

## Conditions

| Condition | Detail | Source |
|---|---|---|
| **Optional status** | This item is NOT included in base price; it is an Owner-elected optional addition | OSR §12.6; SOW-0505; OBJ-010 |
| **Separate pricing required** | Must be priced separately and transparently from base scope | Decomposition SOW-0505; OBJ-010 |
| **Minimum quantities apply** | Quantities listed are minimums; DB may propose higher quantities or upgraded specifications | OSR §12.6 |
| **Allowance/pricing format** | Pricing to include appliance unit costs plus installation coordination | _CONTEXT.md (anticipated artifacts) |
| **Install coordination required** | DB is responsible for coordinating installation with kitchen and laundry rough-ins | _CONTEXT.md (anticipated artifacts); ASSUMPTION: standard DB-design integration requirement |
| **Kitchen rough-in** | Kitchen area (room 16.0) includes sink; appliances connect to existing rough-in per DB design | Functional Program §16.0 |

---

## Construction

| Element | Detail | Source |
|---|---|---|
| **Delivery format** | Separate priced option package; 4-doc bundle | _CONTEXT.md |
| **Anticipated artifacts** | (1) Appliance list; (2) Allowances/pricing sheet; (3) Install coordination notes | _CONTEXT.md |
| **Appliance list content** | Itemized list of proposed appliances with make/model basis, quantities, unit prices, and total | ASSUMPTION: standard optional scope package practice |
| **Pricing sheet content** | Lump-sum or itemized option price, clearly separated from base contract price | OBJ-010; SOW-0505 |
| **Install coordination notes** | Notes on rough-in requirements, connection points, warranty/commissioning handover | ASSUMPTION: standard practice for appliance option packages |

---

## References

| Reference | Location | Notes |
|---|---|---|
| OSR §12.6 Appliances | RFP Appendix A (Owner Statement of Requirements), page 45 | Primary authority for appliance minimum list |
| Functional Program §16.0 Lunch Room/Kitchen | RFP Appendix B, page 46 | Corroborates kitchen appliance scope and room context |
| Functional Program §22.0 Unisex Locker Room | RFP Appendix B, page 46 | Authority for laundry set location (Semantic Lensing F-002: explicitly cited to ensure consistency with Location Context section above) |
| SOW-0505 | Decomposition §Phase 3 scope register | Scope item governing this optional deliverable |
| OBJ-010 | Decomposition §Phase 3 objectives | Objective: transparent, separable pricing for optional scope items |
| _CONTEXT.md | DEL-05-06 deliverable folder | Deliverable identification and anticipated artifacts |
