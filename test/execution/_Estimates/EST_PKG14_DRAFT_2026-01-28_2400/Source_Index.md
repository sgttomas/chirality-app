# Source Index

## PKG-14 Process Piping Estimate

### Sources Searched

| Source Type | Location | Result |
|-------------|----------|--------|
| Vendor quotes | Not found | None available |
| Budgetary proposals | Not found | None available |
| Rate tables | `_Estimates/_RateTables/` | Directory empty |
| Deliverable datasheets | PKG-14 deliverable folders | Not scaffolded; no quantities |
| Deliverable specifications | PKG-14 deliverable folders | Not scaffolded; no quantities |
| P&IDs | Not found | No piping layouts available |
| Line list | Not found | No line list available |
| Decomposition | Project decomposition file | Package scope only |
| Employer's Requirements | Vol 2 Parts 1-3 | Not yet indexed/available |

### Primary Pricing Sources Used

| Priority | Source | Coverage | Notes |
|----------|--------|----------|-------|
| 1 | None | 0% | No vendor quotes available |
| 2 | None | 0% | No rate tables available |
| 3 | Fallback Typical Model | 100% | All items priced via allowances |

### Quantity Sources Used

| Source | Coverage | Notes |
|--------|----------|-------|
| DEL-14.01 Datasheet | 0% | P&IDs and piping GAs not yet developed |
| DEL-14.02 Datasheet | 0% | Piping specification not yet developed |
| DEL-14.03 Datasheet | 0% | Stress analysis not yet developed |
| DEL-14.04 Datasheet | 0% | Line list not yet developed |
| DEL-14.05 Datasheet | 0% | Records scope TBD |
| DEL-14.06 Datasheet | 0% | Transient study not complete |
| DEL-14.07 Datasheet | 0% | Transient study not complete |
| DEL-14.08 Datasheet | 0% | Valve verification TBD |
| Parametric assumptions | 100% | Based on 32 station, 3 tank, terminal layout |

### Parametric Assumptions (Fallback)

| Parameter | Assumed Value | Basis |
|-----------|---------------|-------|
| Rail unloading headers | 250 lm @ 16-20 inch | 2 tracks × ~125m collection length |
| Header laterals | 100 lm @ 8-10 inch | 32 stations × ~3m each |
| Tank inlet headers | 150 lm @ 16-20 inch | Distribution to 3 × 15,000 MT tanks |
| Tank outlet manifold | 100 lm @ 16-20 inch | 3 tanks to pump suction |
| Export piping | 350 lm @ 12-16 inch | Pump discharge to marine loading interface |
| Recycle piping | 150 lm @ 8-12 inch | Return lines and tank transfer |
| Nitrogen distribution | 400 lm @ 2-4 inch | N2 to tanks, headers, marine loading |
| Small bore utility | 200 lm @ 1-2 inch | Drains, vents, sample points |
| Pipe supports | 300 units | ~1 per 5-6 lm for major lines |
| **Total piping** | **~1,700 lm** | All process piping in scope |

### Parametric Unit Rates Used

| Item | Supply Rate | Install Rate | Basis |
|------|-------------|--------------|-------|
| Large diameter pipe (16-20 inch) | $1,500/lm | $1,100/lm | Typical CS pipe with fittings |
| Medium diameter pipe (8-12 inch) | $800/lm | $800/lm | Typical CS pipe with fittings |
| Small diameter pipe (2-6 inch) | $300/lm | $400/lm | Typical CS/SS utility pipe |
| Pipe supports | $600/unit | $600/unit | Typical support fabrication |
| Insulation + heat trace | $200/lm | $150/lm | Cold weather protection |

### Reference Documents (Not Yet Available)

| Document | Expected Content | Status |
|----------|-----------------|--------|
| Volume 2 Part 1 ER | General requirements | Referenced but not provided |
| Volume 2 Part 2 ER | Civil & Process Mechanical | Referenced but not provided |
| Volume 2 Part 3 ER | E&I requirements | Referenced but not provided |
| P&IDs | Process flow, piping routing | Not yet developed (DEL-14.01) |
| Line list | Pipe sizes, materials, services | Not yet developed (DEL-14.04) |
| Piping GAs | Physical routing and layout | Not yet developed (DEL-14.01) |
| Stress analysis | Support schedule, expansion provisions | Not yet developed (DEL-14.03) |
| Transient studies | Surge requirements | Not yet developed (DEL-14.06, DEL-14.07) |

### Potential Pricing Sources (To Be Obtained)

| Source | Expected Impact | Priority |
|--------|-----------------|----------|
| Large diameter pipe supplier quotes | ~$1,550,000 (29% of base) | HIGH |
| Pipe support fabricator quotes | ~$360,000 (7% of base) | MEDIUM |
| Piping contractor rates | ~$1,975,000 CD base | HIGH |
| Insulation contractor quotes | ~$430,000 (8% of base) | MEDIUM |
| NDE contractor quotes | ~$125,000 (2% of base) | LOW |

### Interface Package Data Needed

| Package | Data Required | Impact |
|---------|--------------|--------|
| PKG-10 Railcar Unloading | Header connection locations | Rail header routing |
| PKG-11 Marine Loading | Export pipe interface point | Export pipe length |
| PKG-13 Storage Tanks | Nozzle schedule, elevations | Tank farm piping routing |
| PKG-15 Pumps | Pump nozzle locations, sizes | Suction/discharge spool pieces |
| PKG-16 Valves | Valve schedule, sizes | Inline valve provisions |
