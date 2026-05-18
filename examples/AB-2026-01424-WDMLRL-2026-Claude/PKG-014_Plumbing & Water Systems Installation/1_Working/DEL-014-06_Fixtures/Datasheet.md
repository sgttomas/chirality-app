# Datasheet — DEL-014-06: Plumbing Fixtures

---

## Identification

| Field | Value |
|---|---|
| **Deliverable ID** | DEL-014-06 |
| **Title** | Plumbing Fixtures |
| **Package** | PKG-014 — Plumbing & Water Systems Installation |
| **Project** | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| **Owner** | Camrose County |
| **Location** | SW 14–44–21–W4, near Ferintosh, Alberta |
| **Responsible Party** | Plumbing Contractor |
| **Deliverable Type** | Installation |
| **Contract Form** | CCDC 14–2013 Design-Build Stipulated Price Contract |
| **Completion Deadline** | December 31, 2026 (source: R-01 §3.1) |

---

## Attributes

### Fixture Inventory

| Fixture / Assembly | Quantity | Location (per R-06) | SOW Ref | Notes |
|---|---|---|---|---|
| Water Tap & Pressure Washer Reel | 1 assembly | East wall of New North Shop main bay area | SOW-0049 | Shown as combined fixture point on plumbing drawing |
| Water Tap (standalone service tap) | 1 | Near washroom / utility room area (south end of building) | SOW-0049 | Service tap in the utility zone — not a washroom fixture (see Guidance Principle 5). Shown separately from pressure washer reel location |
| Industrial Wash Station | 1 | Near entrance / between shop and office zone | SOW-0050 | Canonical term: "industrial wash station." Referred to as "Wash Station" on conceptual drawings |

> Note: Exact fixture counts and specific locations are based on conceptual-level plumbing drawing (R-06, Appendix B — Plumbing). Final quantities and precise locations shall be confirmed by the IFC plumbing drawings (DEL-006-02, DEL-006-03). Additional fixtures may be indicated by final design. ASSUMPTION: the above represent the minimum fixture complement per the conceptual drawing.
>
> **Fixture Schedule Dependency (B-003):** The Plumbing Fixture Schedule (DEL-006-06) is the authoritative comprehensive record for all fixture data. Until DEL-006-06 is produced by the Plumbing Engineer (PKG-006), the fixture inventory above is based on the conceptual drawing only and is incomplete. All TBD values in the attribute tables below should be resolved via DEL-006-06. Source: Decomposition PKG-006.

### Pressure Washer Reel

| Attribute | Value | Source |
|---|---|---|
| Reel type | Retractable hose reel | R-06 (conceptual drawing notation) |
| Supply connection | From cistern distribution (DEL-014-01) | ASSUMPTION based on building water source |
| Dedicated electrical circuit | 70A (per SOW-0063 / App B-Elec) | Decomposition SOW-0063; electrical circuit provided by PKG-015 |
| Minimum flow capacity | TBD — resolve via DEL-006-06 Fixture Schedule and manufacturer data | Not specified at conceptual level; essential for design and procurement (B-001) |
| Operating pressure | TBD — resolve via DEL-006-06 Fixture Schedule and pump system design (DEL-014-01) | Not specified at conceptual level; essential for design and procurement (B-001) |

### Water Taps

| Attribute | Value | Source |
|---|---|---|
| Connection type | TBD — resolve via DEL-006-06 Fixture Schedule (hose bib or threaded service tap assumed) | ASSUMPTION — not specified in R-06; placeholder with clear resolution path per B-002 |
| Supply source | Cistern distribution system (DEL-014-01) | ASSUMPTION |
| Number of taps | Minimum 2 (1 near pressure washer reel location; 1 near utility room/washroom) | R-06 conceptual drawing |
| Tap material / model | TBD — resolve via DEL-006-06 Fixture Schedule | Not specified at conceptual level (B-002) |
| Minimum flow rate | TBD — resolve via DEL-006-06 and pump system design | Not specified at conceptual level; needed for design and procurement (B-001) |
| Minimum operating pressure | TBD — resolve via DEL-006-06 and pump system design (DEL-014-01) | Not specified at conceptual level (B-001) |
| Freeze protection | TBD (indoor installation assumed to minimize freeze risk) | ASSUMPTION |

### Industrial Wash Station

| Attribute | Value | Source |
|---|---|---|
| Description | Separate industrial wash station for personal hygiene / parts washing | R-01 §3.1; R-06 conceptual drawing |
| Location | Near main entrance / transition zone between shop and office/parts room | R-06 |
| Drain connection | To septic system via building DWV | ASSUMPTION — connected to DEL-014-02 via sanitary drain |
| Supply connection | From cistern distribution (DEL-014-01) | ASSUMPTION |
| Hot water provision | TBD — resolve during preliminary plumbing design (DEL-006-01); see CONF-014-06-01 in Guidance | Not specified in sources; ASSUMPTION: likely required per Alberta Safety Code workplace requirements |
| Fixture type / material | TBD — resolve via DEL-006-06 Fixture Schedule | Not specified at conceptual level (B-002); ASSUMPTION: stainless steel or equivalent for industrial use |
| Minimum flow rate | TBD — resolve via DEL-006-06 and pump system design | Not specified at conceptual level; essential for design (B-001) |
| Minimum operating pressure | TBD — resolve via DEL-006-06 and pump system design (DEL-014-01) | Not specified at conceptual level (B-001) |

---

## Conditions

| Condition | Value | Source |
|---|---|---|
| Indoor environment | All fixtures within conditioned building interior | R-01 §3.1; R-06 |
| Operating temperature range | TBD (building is heated; high-recovery heating system per SOW-0035) | ASSUMPTION |
| Water source | 50,000L cistern (DEL-014-01); pump rated at 100 LPM minimum | R-01 §3.4; Decomposition SOW-0041, SOW-0042 |
| Wastewater disposal | Septic holding tank, 2,000 US gallon (DEL-014-02) | R-01 §3.4 |
| Floor drains present in immediate vicinity | Yes — floor drains and sump drains in shop area (DEL-014-04) | R-06; Decomposition SOW-0045, SOW-0046 |
| Governing codes | Alberta Safety Codes (Plumbing Code); applicable building codes | R-01 §3.3.2, §3.4 |

---

## Construction

| Item | Value | Source |
|---|---|---|
| Contractor | Plumbing Contractor (sub under Design-Builder) | _CONTEXT.md; Decomposition PKG-014 |
| Upstream prerequisite | Cistern & distribution (DEL-014-01) must be installed and pressurized | _DEPENDENCIES.md |
| Upstream prerequisite | Septic system (DEL-014-02) must be installed and connected | _DEPENDENCIES.md |
| Upstream prerequisite | Floor drain rough-in (DEL-014-04) must be complete where fixture connects to DWV | _DEPENDENCIES.md |
| Upstream prerequisite | Building structure and interior walls complete to accommodate fixture mounting | _DEPENDENCIES.md; R-06 |
| IFC drawing reference | DEL-006-02 (Water Distribution Plans), DEL-006-03 (Drain & Vent Plans), DEL-006-06 (Fixture Schedule) | Decomposition PKG-006 |
| IFC drawing status | TBD — to be produced by Plumbing Engineer (PKG-006) | Decomposition |
| Inspection | All installation subject to Safety Code inspection; County representative to be present | R-01 §3.3.2 |
| Warranty | 2-year guarantee period post-CCC (construction period + 2 years) | R-01 §2.10 |

---

## References

| Ref # | Document | Relevance | Accessibility |
|---|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | §3.1 building program; §3.4 design requirements (wash sink, taps); §3.3.2 code compliance | Accessible |
| R-06 | AB-2026-01424-Appendix B (Plumbing).pdf | Conceptual plumbing layout showing water tap, pressure washer reel, industrial wash station locations | Accessible (conceptual only) |
| R-04 | AB-2026-01424-Appendix B (Shop).pdf | Floor plan showing industrial wash station location relative to building layout | Accessible (conceptual only) |
| Decomposition | WDMLRL_Decomposition_Claude.md | SOW-0049, SOW-0050; PKG-014 scope; DEL-014-06 entry | Accessible |
| DEL-006-06 | Fixture Schedule (PKG-006 output) | Authoritative fixture list and specifications | Not yet produced (TBD) |
| DEL-006-02/03 | Water Distribution & Drain/Vent Plans | Routing and connection details | Not yet produced (TBD) |
