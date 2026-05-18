# Assumptions_Log.md — EST_DEL-014-01_2026-02-27_0201

| AssumptionID | Assumption | Impact on Estimate | Source / Basis |
|---|---|---|---|
| ASM-001 | Cistern is located inside the heated building envelope (utility room area per R-06 plumbing drawing) | Reduces freeze protection cost; simplifies structural approach | Datasheet > Location within building; R-06 plumbing drawing |
| ASM-002 | Tank type is above-grade (within utility room) | Affects cistern cost and installation method; below-grade would increase cost (excavation, waterproofing) | Datasheet Lensing Item B-001: type TBD; plumbing drawing suggests interior placement |
| ASM-003 | Distribution pump is a single centrifugal pump (not duplex) | Duplex configuration would approximately double pump cost ($8,500 becomes ~$17,000) | Guidance Trade-offs: RFP mandates single-pump minimum; duplex is an option |
| ASM-004 | Distribution piping total run is approximately 60 metres | Piping cost scales linearly with length; actual routing TBD in IFC design | Parametric estimate based on building dimensions (~13,000 sqft footprint) and 3 distribution points |
| ASM-005 | Pipe material is copper or PEX (typical for interior service water) | Material choice affects unit rate; HDPE or stainless would change cost | Datasheet: pipe material TBD (Lensing A-002) |
| ASM-006 | Freeze protection applies to ~40 metres of piping in vulnerable locations | Full pipe insulation and heat trace on all runs would increase freeze protection cost | Specification REQ-014-01-008: method TBD; assumption that most piping is within heated envelope |
| ASM-007 | Water quality classification is non-potable service water | Potable classification would add water treatment equipment, additional testing, and more stringent backflow prevention — estimated additional $5,000-$15,000 if potable | Guidance Conflict Table CONF-014-01-01: classification unresolved |
| ASM-008 | Plumber labour productivity is typical for Alberta industrial construction | Productivity factors (weather, site access, material handling) not explicitly adjusted | Construction_Labour_Rates.csv basis; rural site may affect productivity |
| ASM-009 | Plumbing permit fee is approximately $1,500 for this scope | Actual fee depends on local authority having jurisdiction; could range from $500 to $3,000 | No fee schedule available in PRICE_SOURCES |
| ASM-010 | Commissioning of cistern system is coordinated with DEL-020-01 (Building Systems Commissioning) and does not require a separate commissioning agent engagement | If separate commissioning agent required, add ~$2,000-$4,000 | Procedure Phase 5; coordination assumed |
| ASM-011 | 2.5-inch filling connection is a standard cam-lock fitting | If flanged or specialized coupling required, cost may increase to ~$1,500-$2,500 | Datasheet Lensing Item E-001: coupling type TBD |
| ASM-012 | Backflow prevention is a single reduced-pressure zone (RPZ) device | If multiple devices required at multiple locations, cost increases proportionally | Specification REQ-014-01-011: device type and locations TBD |
