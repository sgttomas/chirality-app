# Datasheet — DEL-011-03 Drive-Through Repair Bays

**Document Type:** Datasheet (Descriptive)
**Deliverable ID:** DEL-011-03
**Deliverable Name:** Drive-Through Repair Bays
**Package:** PKG-011 — Building Structure & Envelope
**Revision:** R1 — 2026-02-26 (Pass 3 enrichment)
**Status:** SEMANTIC_READY

---

## Identification

| Field | Value |
|---|---|
| Deliverable ID | DEL-011-03 |
| Deliverable Name | Drive-Through Repair Bays |
| Package | PKG-011 — Building Structure & Envelope |
| Discipline | General Contractor (Structural / Envelope) |
| Type | Construction |
| Responsible Party | General Contractor |
| Covers SOW | SOW-0025 |
| Supports Objective | OBJ-001 |
| Project | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| Owner | Camrose County |
| Contract Form | CCDC 14-2013 Design-Build Stipulated Price Contract |
| Completion Deadline | December 31, 2026 |

**Source:** Decomposition S7, PKG-011 deliverable table; _CONTEXT.md; RFP S3.1, S3.4, Appendix B (Shop).

---

## Attributes

| Attribute | Value | Source |
|---|---|---|
| Number of repair bays | 2 (two drive-through) | RFP S3.1; Appendix B (Shop) |
| Bay width (each, nominal) | 24 feet (nominal dimension from conceptual drawing; whether this represents structural centerline, nominal bay width, or clear opening width is TBD pending IFC drawings -- see Normalization Note below) | Appendix B (Shop) -- plan dimensions |
| Bay depth / length | TBD -- IFC drawings not yet issued; overall New North Shop depth is 100' per Appendix B; individual bay depth within that envelope TBD | Appendix B (Shop) |
| Bay configuration | Drive-through (separate entrance and exit doors per bay) | RFP S3.1; Appendix B (Shop) |
| Bay door type | Overhead door(s) (motorised assumed) | RFP S3.1; Appendix B (Shop); SOW-0025 -- ASSUMPTION: motorised; door specification TBD per IFC drawings |
| Bay door width | TBD -- IFC drawings not yet issued; 24' bay width is the nominal reference dimension | Appendix B (Shop) |
| Bay door height | TBD -- IFC drawings not yet issued; must accommodate heavy equipment including tracked and packer class per RFP S3.4 context. ASSUMPTION: minimum 14-16 feet clear height likely needed for motor scraper class with raised attachments; confirm with equipment fleet dimensions (see Specification REQ-011-03-005 Note) | RFP S3.4 (general equipment sizing context) |
| Door weather seals | TBD -- weather seals (head, jamb, and floor seals) anticipated for heated bay in Alberta cold climate; specification TBD in IFC drawings | ASSUMPTION: weather seals appropriate for insulated/heated bay; lensing item C-002 |
| Door insulation | TBD -- insulated door panels anticipated given Alberta cold climate and heated interior; R-value selection criteria TBD pending design team and energy modelling input | ASSUMPTION: insulated doors appropriate; lensing item A-005 |
| Structural system | Concrete structure, 35-foot clear ceiling height | RFP S3.4; Appendix B (Shop) |
| Floor substrate | Concrete slab; steel plates embedded at strategic locations (note: steel plate embedments are DEL-011-02 scope but are integral to repair bay floors) | RFP S3.4; Appendix B (Shop); Decomposition SOW-0024 |
| Sump drains in repair bays | Required -- sump drains in each repair bay | RFP S3.4 (SOW-0045); installation by PKG-014 |
| Exhaust provisions | Exhaust hoses and fans for heavy equipment in repair bays required | RFP S3.4 (SOW-0038); supply/installation by PKG-013 |
| Overhead crane service | Two 5-tonne overhead cranes on trolley serve the main shop area including repair bays | RFP S3.4; Appendix B (Shop); SOW-0067; PKG-016 |
| Location within building | Main shop area of the New North Shop addition (130' x 100' footprint) | Appendix B (Shop) |
| Three-phase power | Building runs on three-phase power; power to overhead doors provided by PKG-015 | RFP S3.4; SOW-0051, SOW-0060 |

### Normalization Note -- Bay Width Dimension (Lensing B-002)

The 24-foot bay width appears in three different characterizations across the document set: Appendix B shows "24'" as a plan annotation dimension, Specification uses "nominally 24 feet wide," and Guidance references "nominal 24'" and "22'-24' clear width likely." It is not yet clear whether 24' represents the nominal structural bay dimension (centerline-to-centerline), the architectural rough opening width, or the clear opening width after wall thickness and column allowances. **The IFC drawings should establish the authoritative definition of the 24' dimension, distinguishing nominal bay width from clear opening width.** This is flagged as TBD. (Source: Lensing item B-002; Appendix B (Shop); ASSUMPTION: clear width will be slightly less than 24' nominal once wall thickness is applied.)

---

## Conditions

| Condition | Value | Source |
|---|---|---|
| Operating environment | Interior industrial -- maintenance and repair of heavy landfill equipment (tracked, packer, motor scraper class) | RFP S3.1, S3.4 |
| Equipment accommodation | Must accommodate large heavy construction equipment including motor scraper class | RFP S3.3.2; RFP S3.4 |
| Ceiling clearance | 35-foot concrete structure ceiling | RFP S3.4; Appendix B (Shop) |
| Overhead crane clearance | Crane runway beams and travel path serve repair bay area; structural clearances defined in DEL-002-07 (Crane Support Details) | Decomposition DEL-002-07; SOW-0067 |
| Climate | Alberta -- cold climate construction and operation; heated interior (high-recovery heating system, DEL-013-01) | ASSUMPTION: Alberta climate conditions; RFP S3.4 (heating requirement) |
| Floor drainage | Sump drains provided in each repair bay (DEL-014-04 scope) | RFP S3.4 |
| Ventilation | Exhaust hoses and fans for heavy equipment; high-volume air exchanger and makeup air also serve main shop area | RFP S3.4; SOW-0036, SOW-0037, SOW-0038 |
| Regulatory | Must comply with all applicable Alberta building codes, regulations, and Alberta Safety Codes | RFP S3.3.2, S3.4 |

---

## Construction

| Item | Value | Source |
|---|---|---|
| Structural material | Concrete (superstructure per DEL-011-01; concrete floor slab) | RFP S3.4; Appendix B (Shop) |
| Bay framing / wall | TBD -- defined in IFC structural drawings (DEL-002-03, DEL-002-04) | Decomposition DEL-002 series |
| Overhead doors | Overhead (roll-up or sectional) doors per each bay entrance and exit; specifications TBD in IFC drawings | RFP S3.1; SOW-0025; ASSUMPTION: sectional overhead doors typical for industrial bays of this class |
| Door hardware / operators | TBD -- IFC drawings; electrical power for overhead doors provided by PKG-015 (SOW-0060) | SOW-0060 |
| Door safety devices | TBD -- obstruction sensors and auto-reverse mechanism anticipated for motorised industrial overhead doors; specification TBD (see Specification REQ-011-03-015) | ASSUMPTION: required for motorised industrial doors per safety standards; lensing item A-002 |
| Steel plate embedments | Embedded steel plates at strategic floor locations for tracked/packer equipment (DEL-011-02 scope; integral to repair bay floor) | RFP S3.4; Appendix B (Shop); SOW-0024 |
| Sump drain installation | By PKG-014 (DEL-014-04) following structural rough-in | SOW-0045 |
| Exhaust rough-in | Provisions for exhaust hose drops and fan connections by PKG-013 (DEL-013-04) | SOW-0038 |
| Construction sequence | Foundation (DEL-010-01) -> Superstructure (DEL-011-01) -> Steel Embedments (DEL-011-02) -> Repair Bay structural completion including overhead door frames (this deliverable, DEL-011-03) -> MEP rough-in (PKG-013, PKG-014, PKG-015) | ASSUMPTION: standard construction sequencing; _DEPENDENCIES.md |
| Inspection requirements | County project representative to be present at all inspections; copies of all inspection reports to County | RFP S3.3.2 |
| IFC drawings required | All construction per IFC drawings stamped by P.Eng. licensed in Alberta | RFP S3.3.2 |
| As-built records | Red-line or digital as-built markups for bay dimensions and door rough openings required (feeds DEL-008-04 as-built survey) | Specification Documentation table; lensing item E-002 |

---

## References

| Ref | Document | Relevance |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | S3.1 (building program), S3.3.2 (scope of work), S3.4 (design requirements), S2.10 (guarantee period) |
| R-04 | AB-2026-01424-Appendix B (Shop).pdf | Conceptual floor plan -- bay widths (24'), layout, building footprint (130' x 100'), crane column positions, steel plate locations |
| Decomposition | WDMLRL_Decomposition_Claude.md | SOW-0025, PKG-011 deliverable table, DEL-011-03 entry, S7 |
| _CONTEXT.md | DEL-011-03 context file | Deliverable identification and anticipated artifacts |
| _DEPENDENCIES.md | DEL-011-03 dependencies file | Upstream: DEL-011-01, DEL-011-02; Downstream: PKG-012 |
| _SEMANTIC_LENSING.md | DEL-011-03 lensing register | Pass 3 enrichment worklist (21 items) |
