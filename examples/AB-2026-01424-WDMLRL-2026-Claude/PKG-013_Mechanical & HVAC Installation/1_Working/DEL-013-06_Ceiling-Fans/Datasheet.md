# Datasheet — DEL-013-06: Ceiling Fans

---

## Identification

| Field | Value |
|---|---|
| **Deliverable ID** | DEL-013-06 |
| **Deliverable Name** | Ceiling Fans |
| **Package** | PKG-013 — Mechanical & HVAC Installation |
| **Project** | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| **Owner** | Camrose County |
| **Location** | SW 14–44–21–W4, near Ferintosh, Alberta |
| **Responsible Party** | Mechanical Contractor |
| **Activity Type** | Installation |
| **SOW Reference** | SOW-0040 |
| **Objective Linkage** | OBJ-001, OBJ-004 |
| **Contract Form** | CCDC 14–2013 Design-Build Stipulated Price Contract |
| **Completion Deadline** | December 31, 2026 |

---

## Attributes

| Attribute | Value | Source |
|---|---|---|
| **Fan Quantity** | 6 | SOW-0040 (R-01, Decomposition §8 Scope Ledger); App B-Elec (R-05) Electrical Notes |
| **Installation Location** | Main shop area (New North Shop) | App B-Elec (R-05) Electrical Notes; SOW-0040 |
| **Ceiling Height at Installation** | 35 ft | App B-Shop (R-04) building notes; App B-Elec (R-05) building notes |
| **Building Footprint (Main Shop)** | Approximately 130 ft wide x 100 ft deep (repair/main bay area) | App B-Shop (R-04) plan dimensions |
| **Fan Diameter / Model** | TBD — to be confirmed by Mechanical Engineer and Mechanical Contractor at design stage | — |
| **Motor Power per Fan** | TBD | — |
| **Voltage / Amperage per Fan** | TBD — ASSUMPTION: 120V single-phase, circuit type consistent with 15A or 20A receptacle circuits prevalent in main shop (App B-Elec, R-05). **Caution (B-002):** If HVLS fans are selected per Guidance P2, typical HVLS units require 208V/240V or 480V three-phase power, which would invalidate this assumption and materially change electrical circuit design (DEL-015 interface). Confirm with Mechanical Engineer and fan manufacturer once product is selected. | ASSUMPTION — potentially invalid for HVLS; see Guidance P2 |
| **Speed Control Type** | TBD — to be specified by Mechanical Engineer | — |
| **Mounting Type** | TBD — ASSUMPTION: direct ceiling/structural-purlin mount with downrod, given 35 ft ceiling height requiring extended downrod for effective air movement | ASSUMPTION |
| **Finish / Material** | TBD — ASSUMPTION: industrial-grade finish suitable for shop environment (dust, moisture, vehicle exhaust exposure). See Specification REQ-013-06-08 for environmental durability requirements and E-003 for IP/NEMA rating consideration. | ASSUMPTION |
| **Direction of Rotation** | TBD — ASSUMPTION: reversible (summer/winter mode) to address both destratification and cooling functions. See Specification REQ-013-06-11 for status of direction reversal requirement (mandatory vs. recommended — TBD per C-001). | ASSUMPTION |
| **Noise Rating** | TBD — must be acceptable for shop work environment (source: _DEPENDENCIES.md Constraint Notes). Specification REQ-013-06-10 requires numeric dBA limit to be determined (see A-002). | — |
| **Fan Positions (Layout)** | TBD — individual fan positions not explicitly shown on App B-Elec drawing; 6 individual position coordinates to be determined by Mechanical Engineer based on shop layout during design phase per Procedure Step 3 (B-001). Position determination is prerequisite for structural approval, electrical rough-in, and crane clearance verification. | — |

---

## Conditions

| Condition | Value | Source |
|---|---|---|
| **Operating Environment** | Industrial maintenance shop; exposure to vehicle exhaust, welding fumes, grease, dust | App B-Shop (R-04); _CONTEXT.md description |
| **Ambient Temperature Range** | TBD — Alberta climate; heated shop (high-recovery heating system present per DEL-013-01 / SOW-0035) | ASSUMPTION: heated to occupancy temperature in winter |
| **Ceiling Structure Type** | TBD — requires verification. App B-Shop (R-04) building notes reference "Concrete structure," but other documents reference "structural ceiling/purlin/beam" (Guidance P4) and "structural ceiling attachment points ... purlin" (Procedure Step 3.1). Concrete ceiling and steel purlin/beam are different mounting conditions requiring different hardware (concrete anchors vs. beam clamps). **Conflict B-003: verify against structural drawings (DEL-002) to confirm actual ceiling structure type.** See Guidance Conflict Table CF-013-06-03. | App B-Shop (R-04) — conflicted; see Conflict Table CF-013-06-03 |
| **Overhead Obstructions** | (2) 5-tonne overhead cranes on trolley operating in main shop area | App B-Shop (R-04); App B-Elec (R-05); RFP §3.4 |
| **Minimum Clearance (fan blade to floor)** | TBD — must comply with applicable Alberta Safety Codes and building code requirements. Specific numeric value and applicable code clause TBD (A-003). | _REFERENCES.md Standard References |
| **Minimum Clearance (fan blade to crane rail/hook)** | TBD — critical constraint given 5-tonne overhead cranes; requires structural/mechanical engineer coordination. Specific numeric value and applicable code clause TBD (A-003). | ASSUMPTION: critical clearance constraint |
| **Co-located Systems** | High-recovery heating (DEL-013-01), high-volume air exchanger (DEL-013-02), forced-air makeup (DEL-013-03), heavy equipment exhaust (DEL-013-04), welding exhaust (DEL-013-05) | _DEPENDENCIES.md; _CONTEXT.md |

---

## Construction

| Item | Description | Source |
|---|---|---|
| **Structural Support** | Fans to be mounted to structural ceiling attachment point (type TBD per B-003) capable of supporting fan dead load plus dynamic loading (vibration); structural engineer sign-off required. See Specification REQ-013-06-05. | _DEPENDENCIES.md Constraint Notes; _REFERENCES.md Approval Documents |
| **Mounting Hardware** | TBD — ASSUMPTION: manufacturer-supplied mounting bracket with downrod assembly; length TBD based on final mounting height determination. Fastener torque specifications to be sourced from manufacturer installation instructions once equipment is selected (A-005). | ASSUMPTION |
| **Electrical Supply** | Dedicated branch circuit(s) from main electrical panel; circuit amperage, voltage, and routing TBD by Electrical Contractor (DEL-015 scope interface). Note: voltage assumption (120V single-phase) may be invalid if HVLS fans are selected — see Attributes table (B-002). | _DEPENDENCIES.md; App B-Elec (R-05) |
| **Control Wiring** | TBD — wall-switch control or integrated control panel; must integrate with overall system operation per _DEPENDENCIES.md Constraint Notes. See Guidance Trade-offs table for control type decision criteria (D-003). | — |
| **Installation Performer** | Mechanical Contractor (primary); Electrical Contractor for branch circuit terminations (DEL-015 interface) | _CONTEXT.md; _DEPENDENCIES.md |
| **Quantity of Units** | 6 fans | SOW-0040; App B-Elec (R-05) |

---

## References

| Ref ID | Document | Relevance |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | Project scope, SOW-0040, design requirements §3.4 |
| R-04 | AB-2026-01424-Appendix B (Shop).pdf | Floor plan, ceiling height (35 ft), building dimensions |
| R-05 | AB-2026-01424-Appendix B (Electrical).pdf | Electrical notes: "6 Ceiling Fans for Main Shop"; circuit layout. **Note (E-001):** R-05 is referenced as a primary source in this deliverable but is not listed in _REFERENCES.md; reference alignment TBD. |
| — | WDMLRL_Decomposition_Claude.md | Deliverable entry (PKG-013, DEL-013-06), SOW-0040, OBJ-001/OBJ-004 |
| — | _CONTEXT.md | Deliverable identity, scope, key requirements |
| — | _DEPENDENCIES.md | Upstream/downstream constraints, co-located systems |
| — | _REFERENCES.md | Reference index for this deliverable |

---

## Semantic Lensing Enrichment Log (Pass 3)

The following warranted items from `_SEMANTIC_LENSING.md` were incorporated into this document during Pass 3:

| ItemID | Type | Action Taken |
|---|---|---|
| B-001 | TBD_Question | Enhanced Fan Positions row in Attributes with downstream dependency note and reference to Procedure Step 3 |
| B-002 | WeakStatement | Added caution note to Voltage/Amperage row regarding HVLS power requirements potentially invalidating 120V assumption |
| B-003 | Conflict | Updated Ceiling Structure Type in Conditions from asserted "Concrete structure" to TBD with conflict note; added reference to new Conflict Table entry CF-013-06-03 |
| A-005 | MissingSlot | Added torque specification note to Mounting Hardware in Construction |
| E-001 | Normalization | Added note to R-05 reference row regarding misalignment with _REFERENCES.md |
| A-003 | TBD_Question | Enhanced clearance rows in Conditions to note missing code clause and numeric value |
