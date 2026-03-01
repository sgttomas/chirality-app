# Datasheet — DEL-015-01 Three-Phase Power Service

---

## Identification

| Field | Value |
|---|---|
| Deliverable ID | DEL-015-01 |
| Deliverable Title | Three-Phase Power Service |
| Package | PKG-015 — Electrical & Low-Voltage Installation |
| Project | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| Owner | Camrose County |
| Location | SW 14–44–21–W4, near Ferintosh, Alberta |
| Responsible Party | Electrical Contractor |
| Work Type | Installation |
| Contract Form | CCDC 14–2013 Design-Build Stipulated Price |
| Covers SOW | SOW-0051 (three-phase power supply), SOW-0081 (utility tie-in coordination) |
| Supports Objectives | OBJ-001 (code-compliant facility), OBJ-005 (electrical systems to operational readiness) |
| Decomposition Reference | WDMLRL_Decomposition_Claude.md §7 PKG-015 |

*[F-002] Note: SOW-0081 is described in the Decomposition as "Coordinate and execute electrical service tie-in." The Decomposition assigns SOW-0081 to DEL-018-06 (Utility Tie-Ins), but this deliverable coordinates the electrical portion of the tie-in under SOW-0051 scope. The SOW-0081 scope description has been normalized across documents to use consistent wording; see Guidance Conflict Table CON-015-01-004 for the scope boundary question.*

---

## Attributes

| Attribute | Value | Source |
|---|---|---|
| Service type | Three-phase AC electrical service | RFP §3.4; Decomposition SOW-0051 |
| Service voltage | TBD (ASSUMPTION: 208Y/120V or 480Y/277V 3-phase; to be confirmed by electrical design P.Eng. — PKG-004). **[A-001] Authority chain for voltage selection: TBD — it is unresolved whether the prescriptive authority is the utility (available voltages), the Owner (operational preference), or the design engineer (engineering judgment). REQ-015-01-002 defers to IFC drawings but does not state the prescriptive hierarchy. See Guidance Conflict Table CON-015-01-001.** | R-05 (App B-Elec — legend shows 120V and 240V branch circuits; service voltage not stated) |
| Service ampacity / size | TBD — to be established in IFC electrical design drawings. **[B-001] This is the single most critical sizing parameter for this deliverable. Target availability date: TBD — dependent on PKG-004 electrical design completion.** | Electrical design (PKG-004); not stated in RFP or App B-Elec |
| Distribution | Main distribution panel (MDP) feeding all branch circuits for shop addition | _CONTEXT.md; App B-Elec (circuit legend) |
| Metering | TBD — utility company metering requirements to be confirmed at tie-in coordination. **[X-006] Scope clarification needed: metering equipment is typically utility-owned and utility-installed in Alberta. This deliverable's scope is limited to providing the meter base per utility specifications; the meter itself is a utility-provided item. Terminology has been normalized — see also Specification In Scope item 2 and Procedure Step 2.2.** | SOW-0081; _DEPENDENCIES.md |
| Utility provider | TBD — local utility to SW 14–44–21–W4, Alberta. **[B-004] Identifying the specific utility provider is an essential prerequisite for all utility coordination activities (Procedure Steps 1.1, 1.2). Proponent to investigate during design phase.** | _DEPENDENCIES.md (upstream: utility company service connection) |
| Service entrance / point of connection | Electrical room within new building addition (ASSUMPTION based on service trench notation on App B-Elec drawing) | App B-Elec conceptual drawing |
| Service trench | Noted on conceptual drawing | App B-Elec (labeled "SERVICE TRENCH" on plan) |
| Grounding system | Required — type TBD per IFC design | Alberta Safety Code (ASSUMPTION: CSA C22.1 Section 10); PKG-004 design |
| Number of phases | 3 | RFP §3.4 |
| Number of wires | TBD (ASSUMPTION: 4-wire, 3-phase + neutral, or 3-wire depending on voltage system selected) | PKG-004 electrical design |

### Known Downstream Load Summary (from App B-Elec conceptual drawing)

| Load Description | Circuit Rating | Qty (approx.) |
|---|---|---|
| High bay lights — Main Shop | 15A 120V | 20 fixtures (5 rows x 4) |
| High bay lights — Wash Bay | 15A 120V | 6 fixtures (2 rows x 3) |
| 8' LED fixtures — Office, Utility, Parts Room | 15A 120V | 9 fixtures total |
| Ceiling fans — Main Shop | 15A 120V (ASSUMPTION) | 6 |
| General-purpose receptacles | 20A 120V | Multiple throughout |
| 240V 20A receptacles | 20A 240V | Multiple throughout |
| 240V 30A receptacles | 30A 240V | Multiple throughout |
| 240V 50A receptacles (welding) | 50A 240V | Multiple (welding station area) |
| Air compressor | 40A (rating noted on drawing) | 1 |
| Fire hose pump | 70A (rating noted on drawing) | 1 |
| Pressure washer | 70A (rating noted on drawing) | 1 |
| 5-tonne overhead cranes (x2) | TBD — crane power circuits | 2 |
| Overhead doors | TBD | Multiple |
| Exhaust fans | 15A 120V (ASSUMPTION) | Per plan |
| **[B-003] HVAC / mechanical loads** | **TBD — not enumerated on App B-Elec; may draw from MDP** | **TBD** |
| **[B-003] DEL-015-05 low-voltage system loads** | **TBD — backup power or power supply requirements for low-voltage systems not yet enumerated** | **TBD** |
| **[B-003] Future expansion loads** | **TBD — not shown on conceptual drawing; depends on spare capacity decision (see Guidance Trade-offs)** | **TBD** |

*Source: App B-Elec (Appendix B Electrical conceptual drawing). Circuit counts are approximate from conceptual drawing; IFC drawings govern.*

*[B-002] Note: The load counts and ratings above are derived from a conceptual drawing and are approximate. They are not sufficient evidence for final ampacity decisions. The IFC load schedule (PKG-004) will supersede this summary in all respects. See also Specification REQ-015-01-003, which carries the same caveat.*

---

## Conditions

| Condition | Value | Source |
|---|---|---|
| Jurisdiction | Province of Alberta, Canada | RFP §2.22 |
| Applicable codes | Alberta Safety Codes; Alberta Building Code; Canadian Electrical Code (CSA C22.1) — ASSUMPTION: CEC applies as Alberta adopts it | RFP §3.3.2 ("adhere to all Alberta Safety Codes") |
| IFC drawing requirement | All IFC drawings must be signed/stamped by P.Eng. licensed in Alberta | RFP §3.3.2 |
| Upstream dependency | Utility company service connection (external — outside deliverable scope) | _DEPENDENCIES.md |
| Upstream dependency | Electrical room / building structure ready (PKG-011) | _DEPENDENCIES.md |
| Upstream dependency | Electrical design (PKG-004) must be complete before installation proceeds | _CONTEXT.md; Decomposition §6 |
| Completion deadline | December 31, 2026 | RFP §3.1 |
| Inspection | All inspection requests submitted; County representative present; copies to County | RFP §3.3.2 |
| Guarantee period | 2 years post-CCC | RFP §2.10 |
| **[C-002] Site environmental conditions** | **TBD — the project is at a landfill site (SW 14-44-21-W4); site-specific code provisions for ambient temperature derating, altitude derating, or corrosive environment considerations may apply. PKG-004 design engineer and Alberta Safety Codes officer to determine applicability.** | **ASSUMPTION: landfill-adjacent sites may invoke specific CSA C22.1 or Alberta Safety Code clauses; location TBD in applicable code** |

---

## Construction

| Item | Description | Source |
|---|---|---|
| Service entrance | Physical service entry from utility, through service trench noted on conceptual drawing | App B-Elec |
| Main distribution panel (MDP) | Installed in electrical room of new shop addition; feeds all branch circuits | _CONTEXT.md; App B-Elec |
| Grounding and bonding | System grounding per applicable code; type TBD in IFC design | ASSUMPTION (standard practice); RFP §3.3.2 |
| Utility tie-in coordination | Proponent responsible for coordinating electrical tie-in (SOW-0081) | Decomposition SOW-0081; RFP §3.3.2 |
| Wiring method | TBD — per IFC electrical design | PKG-004 |
| Branch circuit distribution | MDP feeds all PKG-015 branch loads (DEL-015-02 through DEL-015-05) and special loads (cranes, overhead doors, compressor, pump, pressure washer) | App B-Elec; _DEPENDENCIES.md |
| Safety systems | Grounding, bonding, overcurrent protection per code | ASSUMPTION; RFP §3.3.2 |

---

## References

| Ref ID | Document | Relevance |
|---|---|---|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf (Main RFP) | §3.4 (three-phase power requirement), §3.3.2 (scope and code compliance), §2.10 (guarantee). **[E-001] Note: _REFERENCES.md cites R-01 as "Main RFP §3.4 (Electrical System Requirements)" — this is the same document. Reference descriptions have been normalized.** |
| R-05 | AB-2026-01424-Appendix B (Electrical).pdf (Electrical Layout Drawings) | Conceptual electrical layout, circuit legend, load list. **[E-001] Note: _REFERENCES.md cites R-05 as "Electrical Layout Drawings" — this is the same document. Reference descriptions have been normalized.** |
| SOW-0051 | Provide three-phase power supply to the building | Decomposition §3-G |
| SOW-0081 | Coordinate and execute electrical service tie-in | Decomposition §3-K |
| OBJ-001 | Core installation objectives | Decomposition §5 |
| OBJ-005 | Electrical systems to operational readiness | Decomposition §5 |
| WDMLRL_Decomposition_Claude.md | Project Decomposition R1 2026-02-25 | §6 PKG-015, §7 DEL-015-01, §3-G SOW-0051 |

---

## Enrichment Provenance (Pass 3)

*The following warranted items from `_SEMANTIC_LENSING.md` were incorporated into this document during Pass 3 enrichment:*

| ItemID | Type | Section Modified | Action Taken |
|---|---|---|---|
| A-001 | TBD_Question | Attributes (Service voltage) | Added authority chain gap notation and cross-reference to Conflict Table CON-015-01-001 |
| B-001 | TBD_Question | Attributes (Service ampacity) | Added criticality note and target availability date TBD |
| B-002 | WeakStatement | Known Downstream Load Summary (note) | Added caveat that conceptual counts are insufficient for ampacity decisions; IFC supersedes |
| B-003 | MissingSlot | Known Downstream Load Summary | Added rows for HVAC/mechanical loads, DEL-015-05 loads, and future expansion loads (all TBD) |
| B-004 | TBD_Question | Attributes (Utility provider) | Added prerequisite linkage note to Procedure Steps 1.1/1.2 |
| C-002 | MissingSlot | Conditions | Added site environmental conditions row for landfill-adjacent considerations |
| E-001 | Normalization | References | Normalized R-01 and R-05 descriptions with alignment notes to _REFERENCES.md |
| F-002 | Normalization | Identification (Covers SOW) | Normalized SOW-0081 scope description; added cross-reference to Conflict Table CON-015-01-004 |
| X-006 | Normalization | Attributes (Metering) | Clarified metering scope ownership (utility-owned vs. contractor-provided meter base) |
