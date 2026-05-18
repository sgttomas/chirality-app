# Datasheet — DEL-011-07 Mezzanine Structure & Stairs

---

## Identification

| Field | Value |
|---|---|
| **Deliverable ID** | DEL-011-07 |
| **Name** | Mezzanine Structure & Stairs |
| **Package** | PKG-011 — Building Structure & Envelope |
| **Discipline** | General Contractor (Structural Construction) |
| **Type** | Construction |
| **Responsible Party** | General Contractor |
| **Project** | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| **Owner** | Camrose County |
| **Contract Form** | CCDC 14–2013 Design-Build Stipulated Price Contract |
| **Completion Deadline** | December 31, 2026 |
| **Guarantee Period** | Construction period + 2 years post-CCC (Source: RFP §2.10.2) |

---

## Attributes

| Attribute | Value | Source |
|---|---|---|
| **Mezzanine Location** | Overhead, spanning above parts room, utility room, and wash bay | RFP §3.4; App B (Shop) floor plan |
| **Mezzanine Function** | Storage of heavy items including oil totes and oil pumping equipment | RFP §3.4 |
| **Load Bearing Designation** | Load-bearing (heavy items); specific load rating TBD per structural engineer design | RFP §3.4; App B note: "Load Bearing Over Parts Room + Utility For Storage" |
| **Mezzanine Floor Area** | TBD — extent spans parts room (~400 sq ft) + utility room + wash bay (24' wide bay); total area TBD per IFC drawings (DEL-002-05). **Note:** This is an essential datum required by downstream activities including procurement, structural design verification, and cost estimation. Resolution depends on Structural Engineer of Record / IFC drawings and on resolution of CFT-011-07-01 (mezzanine extent over wash bay). (Enriched per B-001) | ASSUMPTION: derived from App B floor plan layout; exact dimensions TBD |
| **Stair Configuration** | Stairs to mezzanine; single stair run shown on App B floor plan near utility room / 50,000L water storage zone | App B (Shop) floor plan |
| **Stair Width** | TBD per structural design and Alberta Safety Codes. **Note:** Minimum code-required stair width should be identified at design stage to confirm compliance with R-03 and R-04. Alberta Safety Codes (and underlying NBC provisions for means of egress) establish minimum widths; the Structural Engineer (DEL-002-09) should confirm the design width meets or exceeds the code minimum. (Enriched per B-002) | Alberta Safety Codes / Structural Engineer DEL-002-09; **location TBD** |
| **Railing / Guardrail** | Required (ASSUMPTION: Alberta Safety Codes require guardrails at open edges of elevated platforms); configuration TBD per structural design |
| **Structural System** | TBD — ASSUMPTION: steel-framed mezzanine bearing on the concrete superstructure, consistent with building's concrete structure and 35' ceiling. **Note:** Guidance Trade-offs table (row 1) identifies steel framing as the likely structural system. Once the structural system is confirmed by the Structural Engineer of Record, update this attribute and the Material Specifications attribute accordingly. (Enriched per E-001) | App B: "Concrete Structure (35' Ceiling)"; see also Guidance.md Trade-offs |
| **Floor Deck Type** | TBD per structural engineer (ASSUMPTION: steel deck with concrete topping or open grating, consistent with heavy storage use) |
| **Building Ceiling Height** | 35 feet (overall building) | App B (Shop) notes; RFP §3.4 |
| **Mezzanine Elevation** | TBD per structural design. **Note:** The mezzanine elevation shall provide, at minimum: (a) sufficient clear height below the mezzanine for vehicle/equipment access in the wash bay zone (motor-scraper-sized equipment per RFP §3.1, §3.4); and (b) sufficient clear height above the mezzanine deck for storage operations including placement/retrieval of oil totes. Specific minimum clearance values TBD per Structural Engineer and Architectural coordination (DEL-002-05). (Enriched per X-001) | RFP §3.1, §3.4; App B; ASSUMPTION: constraint bounds required for verification |

---

## Conditions

| Condition | Value | Source |
|---|---|---|
| **Operating Environment** | Interior, heated maintenance shop addition | RFP §3.1, §3.4 |
| **Expected Loads** | Heavy storage: oil totes (multiple), oil pumping equipment | RFP §3.4 |
| **Upstream Structural Dependency** | Mezzanine loads transfer to main concrete superstructure (DEL-011-01); attachment points may use floor embedments (DEL-011-02) | _DEPENDENCIES.md |
| **Downstream Interface** | Mezzanine flooring and interior finishes fall under PKG-012 Interior Construction & Fit-Out | _DEPENDENCIES.md |
| **Code Environment** | Alberta Safety Codes Act; applicable Alberta building codes and regulations. **Note:** For consistent terminology across documents, "Alberta Safety Codes" refers to the legislation (Safety Codes Act and associated regulations), "Safety Codes Officer" refers to the inspection authority, and "Safety Code permit" refers to the permit instrument. See Guidance.md Definitions section for full terminology usage. (Enriched per X-002) | RFP §3.3.2 |
| **IFC Drawings Required** | All construction drawings must be P.Eng.-stamped and issued for construction prior to construction start | RFP §3.3.2 |

---

## Construction

| Item | Value | Source |
|---|---|---|
| **Scope Items Covered** | SOW-0032 (mezzanine storage structure), SOW-0033 (load-bearing capability), SOW-0034 (stairs to mezzanine) | Decomposition §3.D, §8 |
| **Related Design Deliverable** | DEL-002-05 Mezzanine Framing Details; DEL-002-09 Stair Details (PKG-002 Structural Design) | Decomposition §7, PKG-002 |
| **Building Context** | New North Shop addition; concrete structure; ~13,000 sq ft useable area; 130' x 100' footprint per App B | RFP §3.1; App B |
| **Material Specifications** | TBD per P.Eng.-stamped IFC structural drawings. **Note:** Once the structural system trade-off is resolved (steel framing vs. concrete — see Guidance.md Trade-offs table), update this field with the confirmed material type and cross-reference the applicable material standard (e.g., CSA S16 for steel, CSA A23.3 for concrete elements). (Enriched per E-001) |
| **Connection to Superstructure** | Mezzanine framing bears on or connects to concrete superstructure (DEL-011-01); connection details TBD per structural engineer | ASSUMPTION |
| **Anticipated Artifacts** | Mezzanine structural installation documentation; stair and railing installation records; load capacity certification and inspections; safety compliance testing reports; as-built documentation (see Specification R-10) | _CONTEXT.md; Specification.md |

---

## References

| Ref # | Document | Relevance |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | §3.4 Design Requirements (mezzanine storage and load-bearing); §2.10 Guarantee Period |
| R-04 | AB-2026-01424-Appendix B (Shop).pdf | Floor plan showing mezzanine location, stair location, and notes re load-bearing storage |
| — | Decomposition: WDMLRL_Decomposition_Claude.md | §3.D (SOW-0032, SOW-0033, SOW-0034), §7 PKG-011 deliverables, §8 Scope Ledger |
| — | _CONTEXT.md | Deliverable identification, type, anticipated artifacts |
| — | _DEPENDENCIES.md | Upstream/downstream dependency declarations |

---

## Enrichment Log (Pass 3)

| Item ID | Type | Change Applied | Source |
|---|---|---|---|
| B-001 | TBD_Question | Added downstream-dependency and resolution note to Mezzanine Floor Area attribute | _SEMANTIC_LENSING.md B-001; Datasheet.md Attributes |
| B-002 | TBD_Question | Added minimum code-width identification note to Stair Width attribute | _SEMANTIC_LENSING.md B-002; Alberta Safety Codes / DEL-002-09; **location TBD** |
| X-001 | WeakStatement | Added constraint statement (clear height below/above) to Mezzanine Elevation attribute | _SEMANTIC_LENSING.md X-001; RFP §3.1, §3.4; App B |
| E-001 | Normalization | Cross-referenced Guidance Trade-offs for Structural System and Material Specifications; added update-trigger note | _SEMANTIC_LENSING.md E-001; Guidance.md Trade-offs |
| X-002 | Normalization | Added terminology clarification note to Code Environment condition | _SEMANTIC_LENSING.md X-002; see Guidance.md Definitions |
