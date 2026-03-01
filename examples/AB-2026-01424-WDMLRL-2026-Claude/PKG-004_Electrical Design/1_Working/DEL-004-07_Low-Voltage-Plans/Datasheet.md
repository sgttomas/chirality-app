# Datasheet: DEL-004-07 Low-Voltage System Plans

---

## Identification

| Field | Value |
|---|---|
| **Deliverable ID** | DEL-004-07 |
| **Name** | Low-Voltage System Plans |
| **Package** | PKG-004 — Electrical Design |
| **Discipline** | Electrical Engineering |
| **Type** | Drawing Set |
| **Responsible Party** | Electrical Engineer |
| **Project** | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| **Owner** | Camrose County |
| **Contract Form** | CCDC 14–2013 Design-Build Stipulated Price Contract |
| **Completion Deadline** | December 31, 2026 |
| **SOW Coverage** | SOW-0014 (Complete final electrical design — three-phase power distribution, lighting, receptacles) |
| **Objectives Supported** | OBJ-001, OBJ-003, OBJ-005 |
| **Decomposition Ref** | WDMLRL_Decomposition_Claude.md §7, PKG-004 deliverables table |

---

## Attributes

### Low-Voltage Systems Covered

The following low-voltage systems are identified in the source drawings (AB-2026-01424-Appendix_B__Electrical_.pdf) and scope (SOW-0014, SOW-0064, SOW-0065):

| System | Description | Source |
|---|---|---|
| Security Camera Wiring | Wiring for security camera system throughout the facility | AB-2026-01424-Appendix_B__Electrical_.pdf (Electrical Notes bullet) |
| 2-Way Radio Antenna Wire | Antenna wiring for 2-way radio communications | AB-2026-01424-Appendix_B__Electrical_.pdf (Electrical Notes bullet) |
| Additional low-voltage systems | TBD — specific low-voltage subsystems (e.g., data/network, fire alarm, intercom, access control) not enumerated in available sources; to be confirmed or excluded at preliminary design (see Specification REQ-007-08) | TBD |

### Circuit/Load Data — Low-Voltage Systems

| Parameter | Value | Source |
|---|---|---|
| Security camera circuit type | TBD — voltage/amperage not specified in available sources. ASSUMPTION: If IP cameras selected, PoE (802.3af/at) over Cat 6; if analog, coaxial with dedicated power circuit. Confirm at preliminary design. | TBD; ASSUMPTION — see Guidance Trade-offs (IP vs. analog) |
| Security camera cable type | TBD — Cat 6 (if IP/PoE) or coaxial (if analog). Cable type depends on camera technology decision. | TBD; ASSUMPTION — Guidance §Security Camera System Context |
| Radio antenna cable type | TBD — coax type/gauge not stated in available sources. Confirm radio system type (VHF/UHF, digital/analog) to determine cable specification. | TBD |
| Number of camera locations | TBD — quantity per area and coverage zones not specified in available sources. Record target count per facility area at preliminary design. | TBD |
| Camera technology type | TBD — IP or analog; confirm with County at preliminary design (see Guidance Trade-offs) | TBD |
| NVR/DVR capacity and location | TBD — head-end equipment room/location not specified in available sources. Confirm NVR/DVR room assignment during preliminary design. | TBD; referenced in Procedure Step 4 and Guidance §Security Camera System Context |
| Number of radio antenna points | TBD — quantity and layout not specified in available sources. Depends on radio system type and in-building coverage requirements. | TBD |
| Radio system type | TBD — VHF/UHF, digital/analog, and whether in-building distribution is required. Confirm with County operations staff. | TBD |

### Facility Context (from Electrical Drawing)

| Area | Relevant Low-Voltage Scope | Source |
|---|---|---|
| Main Shop (130' × 100') | Security camera wiring (locations TBD); radio antenna wire (locations TBD) | App B-Elec; Decomp §2 Vocabulary Map |
| Wash Bay (24' wide, single bay) | Security camera wiring — locations TBD | App B-Elec |
| Parts/Tool Room | Security camera wiring — locations TBD | App B-Elec |
| Office | Security camera wiring — locations TBD | App B-Elec |
| Utility Room | Security camera wiring — locations TBD | App B-Elec |
| Old North Shop (renovation areas) | Low-voltage scope for renovated areas TBD | TBD |

---

## Conditions

| Condition | Value | Source |
|---|---|---|
| Governing jurisdiction | Province of Alberta | RFP §3.3.2, §2.22 |
| Code compliance requirement | All applicable Alberta Safety Codes | RFP §3.3.2 |
| IFC stamp requirement | Signed/stamped by P.Eng. licensed in Alberta | RFP §3.3.2; SOW-0018 |
| Building power supply | Three-phase (ASSUMPTION: 120/208V or 347/600V — voltage class not stated in sources). Note: For low-voltage system power supply (e.g., PoE switches, NVR), the applicable voltage is typically 120V single-phase from a branch circuit; confirm which building voltage class applies. | RFP §3.4; SOW-0051; ASSUMPTION — voltage class requires confirmation by Electrical Engineer |
| County preliminary design approval | Required before proceeding to final IFC drawings | RFP §3.3.2; SOW-0010d |
| Inspection coordination | County representative to be present at all inspections; copies of reports to County | RFP §3.3.2; SOW-0084, SOW-0085 |

---

## Construction

| Attribute | Value | Source |
|---|---|---|
| Drawing format — sheet size | TBD — not specified in available sources (common sizes: ARCH D 24"x36" or ARCH E 36"x48") | TBD |
| Drawing format — scale | TBD — not specified in available sources; confirm appropriate scale for facility dimensions (130' x 100' main shop) | TBD |
| Drawing format — CAD standard | TBD — CAD layer naming convention and file format not specified in available sources | TBD |
| Drawing format — title block | TBD — title block requirements not specified in available sources; confirm project-level standard | TBD |
| Drawing set contents | Low-voltage system plan(s) showing security camera wiring and radio antenna wire routing | App B-Elec; SOW-0064, SOW-0065 |
| Coordination required | Coordinate with Power Distribution Plans (DEL-004-03), Receptacle Plans (DEL-004-05), and Architectural Floor Plans (DEL-001-02) for routing and penetration locations | ASSUMPTION — standard multi-discipline coordination practice |
| IFC status | Final drawings to be IFC-stamped by P.Eng. | RFP §3.3.2; SOW-0018 |
| Preliminary design milestone | Preliminary Electrical Design (DEL-004-01) to receive County approval prior to final | SOW-0010d; Decomp §7 PKG-004 |

---

## References

> **Citation convention note:** Throughout this document and the companion Specification, Guidance, and Procedure documents, the formal reference identifier is used for traceability. The shorthand "App B-Elec" used in earlier drafts corresponds to R-05 below.

| Ref ID | Document | Relevance |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL_RFP.pdf | Main RFP — §3.3.2 scope, §3.4 design requirements, §1.0 services overview |
| R-05 | AB-2026-01424-Appendix_B__Electrical_.pdf (shorthand: App B-Elec) | Conceptual electrical layout, legend, and notes — primary source for low-voltage items |
| Decomp | WDMLRL_Decomposition_Claude.md | SOW-0064, SOW-0065, OBJ-005, PKG-004 deliverables table |
