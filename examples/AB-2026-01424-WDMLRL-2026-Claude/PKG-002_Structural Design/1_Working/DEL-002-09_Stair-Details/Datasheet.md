# Datasheet — DEL-002-09 Stair Details

---

## Identification

| Field | Value |
|---|---|
| **Deliverable ID** | DEL-002-09 |
| **Name** | Stair Details |
| **Package** | PKG-002 — Structural Design |
| **Discipline** | Structural Engineering |
| **Type** | Drawing Set |
| **Responsible Party** | Structural Engineer |
| **Scope of Work Reference** | SOW-0012 |
| **Objective References** | OBJ-001, OBJ-003 |
| **Project** | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| **Owner** | Camrose County |
| **Contract Form** | CCDC 14–2013 Design-Build Stipulated Price Contract |
| **Completion Deadline** | December 31, 2026 |
| **Decomposition Revision** | R1 — 2026-02-25 |

---

## Attributes

> **[B-002] Completeness note:** Multiple TBD entries remain in this table (live load design value, tread/riser dimensions, number of stair runs, stair width, stair material, handrail/guardrail specification). These represent gaps in the comprehensive data record needed for IFC drawing production. Resolve by establishing the design basis per Procedure Step 2 and confirming Alberta Building Code edition per [A-001].

| Attribute | Value | Source |
|---|---|---|
| **Stair function** | Access to overhead mezzanine from main shop floor level | R-04 (App B floor plan); decomposition SOW-0034 |
| **Mezzanine location served** | Above Parts Room, Utility Room, and Wash Bay | R-04 (App B floor plan note) |
| **Mezzanine load requirement** | Load-bearing for heavy items (oil totes, oil pumping equipment) | R-01 §3.4; decomposition SOW-0033 |
| **Building structure type** | Concrete structure | R-01 §3.4; R-04 (App B note) |
| **Clear ceiling height** | 35 ft (building ceiling) | R-01 §3.4; R-04 (App B note) |
| **Building footprint** | 130 ft × 100 ft (New North Shop portion) | R-04 (App B floor plan dimensions) |
| **Stair location (conceptual)** | Between Utility Room and 50,000 L Water Storage, east side of Utility Room area | R-04 (App B floor plan, "Stairs to Mezzanine" label) |
| **Number of stair runs** | TBD (Structural Engineer to determine based on IFC design) | ASSUMPTION |
| **Stair structural material** | TBD (steel or concrete; to be determined by Structural Engineer). **Note:** Material selection determines governing material standard -- CSA S16 (steel) or CSA A23.3 (concrete) -- and associated mandatory fabrication/erection codes. Resolve before specifying mandatory practice requirements. | ASSUMPTION; [A-002] |
| **Stair width** | TBD (minimum per applicable Alberta Building Code; specific edition and clause to be confirmed -- see [A-001]). Essential datum for structural detailing; must be established before IFC drawing production. | ASSUMPTION; [B-001] |
| **Handrail / guardrail requirement** | Required per applicable Alberta Safety Codes | ASSUMPTION — location TBD |
| **Tread/riser dimensions** | TBD (to be calculated per Alberta Building Code) | ASSUMPTION |
| **Live load design** | TBD (to be calculated per applicable structural standard; mezzanine is heavy-storage use). **Note:** Once established, this value must be recorded as an explicit acceptance criterion in Specification REQ-002 verification. See [X-003]. | ASSUMPTION |
| **Seismic design category** | TBD -- Confirm whether seismic design requirements apply to the stair structure under the Alberta Building Code / NBC for this geographic location (SW 14-44-21-W4, central Alberta) and building type. See [C-003]. | ASSUMPTION; location TBD |
| **Fire rating requirement** | TBD -- Confirm whether the stair requires fire-rated enclosure or structural fire protection under the Alberta Building Code for this occupancy and height (35 ft industrial building). See [C-002]. | ASSUMPTION; location TBD |
| **Barrier-free / accessibility** | TBD -- Confirm whether barrier-free / accessibility requirements under the Alberta Building Code apply to this stair (e.g., if the mezzanine requires an accessible route, a stair alone may not satisfy it). See [F-002]. | ASSUMPTION; location TBD |
| **P.Eng. stamp required** | Yes — licensed in Province of Alberta | R-01 §3.3.2 |

---

## Conditions

| Condition | Value | Source |
|---|---|---|
| **Geographic location** | SW 14–44–21–W4, near Ferintosh, Alberta | R-01 §1.0 |
| **Climate zone** | Alberta Central region | R-01 §1.0 |
| **Governing jurisdiction** | Province of Alberta | R-01 §3.3.2 |
| **Applicable codes** | Alberta Building Code (location TBD), Alberta Safety Codes | R-01 §3.3.2, §3.4 |
| **Geotechnical conditions** | TBD — geotechnical investigation to be conducted by Proponent | R-01 §3.3.2, §4.8.2 |
| **Design-build delivery** | Design-builder responsible for all design decisions consistent with RFP requirements | R-01 §3.4 |
| **County approval** | Preliminary design must receive County approval prior to IFC | R-01 §3.3.2 |

---

## Construction

| Item | Value | Source |
|---|---|---|
| **Construction package** | PKG-011 — Building Structure & Envelope (DEL-011-07 Mezzanine Structure & Stairs) | Decomposition §PKG-011 |
| **Construction SOW** | SOW-0032 (mezzanine), SOW-0033 (load-bearing requirement), SOW-0034 (stairs) | Decomposition Scope Ledger |
| **Drawing set purpose** | Issued For Construction (IFC) drawing set — stair structural details for contractor use | R-01 §3.3.2 |
| **Related structural deliverables** | DEL-002-05 (Mezzanine Framing Details), DEL-002-04 (Structural Sections & Details), DEL-002-03 (Structural Framing Plans) | Decomposition PKG-002 |
| **Structural calculation support** | DEL-002-10 (Structural Calculation Package) | Decomposition PKG-002 |
| **Structural specification** | DEL-002-12 (Structural Specification) | Decomposition PKG-002 |

---

## References

| Ref | Document | Relevance |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | §3.3.2 (design requirements — stamping, code compliance); §3.4 (design requirements — mezzanine, stair concept) |
| R-04 | AB-2026-01424-Appendix B (Shop).pdf | Conceptual floor plan showing "Stairs to Mezzanine" location and mezzanine extent |
| Decomposition | WDMLRL_Decomposition_Claude.md | SOW-0034, SOW-0033, SOW-0032; PKG-002 scope; PKG-011 construction; OBJ-001, OBJ-003 |

---

## Semantic Lensing Enrichment Trace (Pass 3)

| ItemID | Type | Action Taken |
|---|---|---|
| A-002 | TBD_Question | Annotated stair structural material TBD with note on material-standard dependency (CSA S16 vs. CSA A23.3) |
| B-001 | MissingSlot | Annotated stair width TBD with essential-datum note and cross-reference to A-001 |
| B-002 | MissingSlot | Added completeness note to Attributes section header summarizing all TBD gaps |
| C-002 | MissingSlot | Added fire rating requirement row as TBD (location TBD in ABC) |
| C-003 | TBD_Question | Added seismic design category row as TBD (location TBD in ABC/NBC) |
| F-002 | MissingSlot | Added barrier-free / accessibility row as TBD (location TBD in ABC) |
