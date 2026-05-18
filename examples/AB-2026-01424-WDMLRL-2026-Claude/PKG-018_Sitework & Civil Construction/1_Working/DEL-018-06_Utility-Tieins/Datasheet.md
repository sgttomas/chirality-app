# Datasheet — DEL-018-06 Utility Tie-Ins

**Document Type:** Datasheet (descriptive)
**Deliverable ID:** DEL-018-06
**Package:** PKG-018 — Sitework & Civil Construction
**Revision:** R1 — 2026-02-26
**Produced by:** 4_DOCUMENTS Agent (Pass 3 — Semantic Lensing Enrichment)

---

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-018-06 |
| **Title** | Utility Tie-Ins |
| **Package** | PKG-018 — Sitework & Civil Construction |
| **Deliverable Type** | Construction |
| **Responsible Party** | General Contractor |
| **Contract Form** | CCDC 14-2013 Design-Build Stipulated Price |
| **Owner** | Camrose County |
| **Project** | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| **Site Location** | SW 14-44-21-W4, near Ferintosh, Alberta |
| **Completion Deadline** | December 31, 2026 |
| **SOW References** | SOW-0080, SOW-0081, SOW-0082 |
| **Objective Alignment** | OBJ-001, OBJ-005 |

Sources: _CONTEXT.md; Decomposition SS7 DEL-018-06 row; RFP SS1.0, SS3.1.

---

## Attributes

### Utility Systems In Scope

> **SOW Cross-Reference Note (per Decomposition SS3 and RFP SS3.3.2):** SOW-0080 = Natural Gas, SOW-0081 = Electrical Service, SOW-0082 = Communications. This mapping is authoritative per the Decomposition and RFP. Note: MEMORY.md and _CONTEXT.md contain incorrect SOW labeling (see Guidance CONF-001). [Enrichment: E-001, X-001]

| System | SOW Ref | Description | Source |
|--------|---------|-------------|--------|
| Natural Gas | SOW-0080 | Coordinate and execute natural gas tie-in to new shop addition | RFP SS3.3.2; Decomposition SS3 SOW-0080 |
| Electrical Service | SOW-0081 | Coordinate and execute electrical service tie-in; three-phase power required | RFP SS3.3.2, SS3.4; Decomposition SS3 SOW-0081; App B (Electrical) |
| Communication Lines | SOW-0082 | Coordinate and execute communication lines tie-in (includes antenna wiring for two-way radios per conceptual drawings) | RFP SS3.3.2; Decomposition SS3 SOW-0082; App B (Electrical) notes |

> **Note:** The three utility systems in scope are natural gas, electrical service, and communications. Water and sewer are **not** in scope for this deliverable, despite references in _CONTEXT.md and _REFERENCES.md to "water/sewer." The Decomposition (SS3 SOW-K) and RFP (SS3.3.2) are authoritative. [Enrichment: X-001, B-003]

### Utility Infrastructure Proximity

> **Note:** The following distances are essential data for cost estimation and schedule planning but are not documented in available sources. [Enrichment: B-001]

| Data Item | Value | Source |
|-----------|-------|--------|
| Distance from site boundary to nearest gas main | TBD | To be confirmed via utility provider inquiry (Procedure Step A1) |
| Distance from site boundary to nearest electrical distribution line | TBD | To be confirmed via utility provider inquiry (Procedure Step A1) |
| Distance from site boundary to nearest telecom infrastructure | TBD | To be confirmed via utility provider inquiry (Procedure Step A1) |

### Utility Provider Lead Times

> **Note:** Provider lead times are essential schedule planning data for this rural Alberta location. [Enrichment: B-004]

| System | Expected Lead Time | Source |
|--------|-------------------|--------|
| Natural Gas — new service connection | TBD (weeks to months — ASSUMPTION for rural Alberta) | To be quantified during utility provider coordination (Procedure Step A4) |
| Electrical Service — new three-phase service | TBD (weeks to months — ASSUMPTION for rural Alberta) | To be quantified during utility provider coordination (Procedure Step A3) |
| Communications — new service | TBD | To be quantified during utility provider coordination (Procedure Step A5) |

### Electrical Service Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| Power Type | Three-phase | RFP SS3.4 ("The proposed building shall run on three-phase power") |
| Service Entry Location | TBD | Utility routing plan not yet produced (civil design in PKG-005) |
| Service Capacity (total) | TBD | Dependent on electrical design (DEL-004) and utility provider confirmation |
| Primary Distribution Panel Location | TBD | Electrical design (DEL-004) |
| Metering | TBD | Utility provider requirements |

#### Anticipated Electrical Loads (from App B — Electrical)

> **Note:** The following load summary is transcribed from the conceptual electrical drawing (App B) and represents anticipated loads for service sizing purposes. Final loads are subject to confirmation through the electrical design (DEL-004). [Enrichment: B-002]

| Load Item | Notes | Source |
|-----------|-------|--------|
| Two 5-tonne overhead cranes | Crane power circuits | App B (Electrical); RFP SS3.4 |
| High bay lighting | Shop area illumination | App B (Electrical) |
| Heating systems (high-recovery) | Electrical components of heating; gas-fired units require electrical controls | RFP SS3.4; App B (Electrical) |
| Welding receptacles | High-voltage receptacles for welding equipment | App B (Electrical) |
| 40-amp compressor | Shop air compressor | App B (Electrical) |
| 70-amp fire hose pump | Fire protection pump | App B (Electrical) |
| 70-amp pressure washer | Wash bay pressure washer | App B (Electrical) |
| Exhaust fans | Shop ventilation exhaust | App B (Electrical) |
| Ceiling fans | Air circulation | App B (Electrical) |
| Overhead door operators | Motorized overhead doors | App B (Electrical) |
| Security/communications equipment | Security cameras, radio antenna, low-voltage systems | App B (Electrical) |

### Natural Gas Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| Gas Service Purpose | Heating system supply — **ASSUMPTION (unconfirmed)**: high-recovery heating system specified (RFP SS3.4); gas is standard heating fuel for industrial shop in Alberta. The RFP specifies SOW-0080 as "natural gas tie-in" but does not explicitly confirm gas as the heating fuel. If gas is not confirmed as the fuel source, all gas-related requirements (REQ-01 series in Specification) lack a prescriptive basis. Confirmation with County is warranted. [Enrichment: A-001] | RFP SS3.3.2 SOW-0080; RFP SS3.4 |
| Gas Service Entry Location | TBD | Utility routing plan not yet produced |
| Service Pressure/Volume | TBD | Dependent on mechanical design and provider |
| Gas Meter Location | TBD | Utility provider requirements |

### Communication Lines Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| Communications Purpose | Two-way radio antenna wiring; may include internet/telephone | App B (Electrical) note: "Antenna Wire for 2 Way Radios"; ASSUMPTION additional telecom services likely but not explicitly specified |
| Communications Entry Location | TBD | Utility routing plan not yet produced |
| Provider | TBD | To be determined during utility provider coordination |

---

## Conditions

| Condition | Description | Source |
|-----------|-------------|--------|
| **On Critical Path** | YES — utility tie-ins required for all facility operations | _DEPENDENCIES.md |
| **Permit Requirements** | All applicable Safety Code Permits required; permits obtained by General Contractor | RFP SS3.3.2; Decomposition SOW-0007 |
| **Utility Provider Coordination** | Required for all three systems prior to construction | RFP SS3.3.2 (mandate to "coordinate") |
| **Inspection Requirements** | County representative must be present at all inspections; copies of all inspection reports provided to County | RFP SS3.3.2; Decomposition SOW-0084, SOW-0085 |
| **Guarantee Period** | 2 years from Construction Completion Certificate (CCC) date | RFP SS2.10 |
| **Surety Bonding** | Performance Bond 50% and Labour & Material Payment Bond 50% of contract price | RFP SS2.12 |
| **Lien Holdback** | 10% of value of Work performed, per Prompt Payment and Construction Lien Act | RFP SS2.13.2 |
| **Site Preparation Dependency** | Trenching requires site grading completion (DEL-018-02) | _DEPENDENCIES.md |
| **Civil Design Dependency** | Utility routing corridors defined by civil design (PKG-005) | _DEPENDENCIES.md; ASSUMPTION |

---

## Construction

| Element | Description | Source |
|---------|-------------|--------|
| **Trenching** | Excavation of trenches for underground utility conduits/piping across site | ASSUMPTION — standard practice for rural site utility installation; no specific trench dimensions stated in RFP |
| **Conduit / Ductwork** | Underground duct/conduit installation for electrical and communication lines | ASSUMPTION — standard practice; specific conduit types TBD from electrical design |
| **Gas Piping** | Underground or above-grade gas piping from service point to building entry | ASSUMPTION — routing and material TBD from mechanical design |
| **Service Connection Points** | Connection at utility provider infrastructure and at building entry | ASSUMPTION — connection point details TBD from civil/electrical design |
| **Metering Installation** | Installation of gas, electrical, and any other required meters | ASSUMPTION — metering required by utility providers; specifics TBD |
| **Backfill and Restoration** | Trenches backfilled and surface restored per site grading plan | ASSUMPTION — standard civil construction practice |
| **Building Penetrations** | Utility entry penetrations through building foundation/wall | ASSUMPTION — coordinated with structural and mechanical design |
| **Testing and Commissioning** | System testing upon completion; County representative present at inspections | RFP SS3.3.2; Decomposition SOW-0084 |

---

## References

| Ref Code | Document | Section | Notes |
|----------|----------|---------|-------|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | SS3.3.2, SS3.4, SS2.10, SS2.12, SS2.13 | Primary scope authority |
| R-07 | AB-2026-01424-Appendix C - Site Maps.pdf | All pages | Site location; expansion area aerial showing existing building and construction area |
| -- | AB-2026-01424-Appendix B (Electrical).pdf | Electrical drawing notes | Three-phase power; antenna wiring for two-way radios; electrical loads |
| -- | WDMLRL_Decomposition_Claude.md | SS3 SOW-K, SS7 DEL-018-06, SS8 Scope Ledger | SOW definitions, deliverable mapping, objective associations |
| -- | _CONTEXT.md | All | Deliverable identity and context |
| -- | _DEPENDENCIES.md | All | Upstream/downstream dependencies |
