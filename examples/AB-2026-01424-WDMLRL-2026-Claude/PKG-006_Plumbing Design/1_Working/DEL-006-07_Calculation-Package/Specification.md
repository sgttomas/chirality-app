# Specification — DEL-006-07 Plumbing Calculation Package

---

## Scope

### What This Deliverable Covers

DEL-006-07 is the engineering calculation package for the plumbing and water systems design of the New North Shop Addition at the West Dried Meat Lake Regional Landfill, Camrose County, Alberta. It provides all sizing computations, design justifications, and code compliance verifications required to support the Issued for Construction (IFC) plumbing drawings under SOW-0016.

The calculation package covers the following systems:

- Water demand analysis for the New North Shop addition
- Water supply distribution sizing (from cistern through building distribution)
- Cistern fill and internal distribution pump selection and sizing
- Bulk water fill system sizing
- Pressure drop analysis across the distribution system
- Floor drain and drainage system sizing, including slope calculations
- Wash bay drainage sizing and connection to exterior mud sump
- Vent stack sizing
- Septic holding tank sizing and effluent loading
- Emergency shower supply and flow verification
- Code compliance matrices for all plumbing systems

### What This Deliverable Excludes

- Structural design of cistern supports, mud sump, or septic tank installation pit (PKG-002 scope)
- Mechanical/HVAC systems calculations (PKG-003 / DEL-003-06 scope)
- Electrical systems calculations (PKG-004 / DEL-004-08 scope)
- Civil drainage and grading calculations (PKG-005 / DEL-005-06 scope)
- Old North Shop plumbing calculations (washroom renovation, locker room, kitchenette, laundry services per SOW-0073, SOW-0074) — **scope TBD: human ruling required.** ASSUMPTION: this calculation package focuses on the New North Shop addition as the primary scope of SOW-0016. If scope is resolved to include Old North Shop renovation plumbing, additional requirements (including laundry hot/cold supply and drain per F-003) must be added. See Conflict Table CFT-001 in Guidance.md. Source: _SEMANTIC_LENSING.md items F-002, F-003, C-003.
- Construction-phase inspection and commissioning records (PKG-020 scope)

---

## Requirements

### REQ-001 — Cistern (Water Storage)

**Requirement:** The cistern shall have a minimum volume of 50,000 L, complete with all necessary plumbing.

**Source:** R-01 §3.4 (SOW-0041)

**Verification:** Calculation confirms tank volume ≥ 50,000 L; specification cross-reference to cistern data sheet.

---

### REQ-002 — Internal Distribution Pump

**Requirement:** The internal service water distribution pump shall be capable of delivering a minimum flow rate of 100 LPM. The cistern filling connection shall be 2.5 inches in diameter.

**Source:** R-01 §3.4 (SOW-0042)

**Verification:** Pump selection calculation confirms ≥ 100 LPM at required system head; connection diameter shown on drawings and confirmed in equipment data sheet.

---

### REQ-003 — Bulk Water Fill System

**Requirement:** A bulk water fill system with a high-volume pump for external filling shall be provided.

**Source:** R-01 §3.4 (SOW-0044)

**Verification:** Pump selection and pipe sizing calculation for bulk fill; flow rate TBD (specific flow rate not stated in RFP — ASSUMPTION: sized for motor-scraper class equipment filling; human ruling required on target flow rate). **Acceptance threshold TBD:** No target flow rate is specified in R-01; compliance cannot be verified until a flow rate target is established. Resolution path: Human ruling per CFT-002 in Guidance.md. Source: _SEMANTIC_LENSING.md item A-003.

---

### REQ-004 — Septic Holding Tank

**Requirement:** A 2,000 US gallon (approximately 7,571 L) septic holding tank shall be supplied and installed. The existing septic tank shall be removed.

**Source:** R-01 §3.4 (SOW-0043); R-06 drawing (septic tank shown at north perimeter)

**Verification:** Septic sizing calculation confirms 2,000 US gallon capacity is adequate for the anticipated occupancy load (ASSUMPTION: Alberta Environment or local authority approval required); confirmation that existing tank removal is included in construction scope.

---

### REQ-005 — Floor Drains

**Requirement:** Floor drains shall be installed throughout the shop as shown on the plumbing drawing. Sump drains shall be installed in the repair bays.

**Source:** R-01 §3.4 (SOW-0045); R-06 drawing (SOW-0046)

**Verification:** Drain locations confirmed against R-06 layout; drain sizing calculations performed per NPC (ASSUMPTION) for anticipated floor wash-down flow rates; slope calculations confirm positive drainage to each drain.

**Note:** The plumbing drawing (R-06) shows floor drains at the following locations: left repair bay, centre/right repair bay, wash bay, and south interior area. Quantities per bay to be confirmed by Plumbing Engineer against IFC drawing.

---

### REQ-006 — Wash Bay Drainage and Mud Sump

**Requirement:** The wash bay floor drain shall connect to an exterior mud sump sized for cleanout by excavator.

**Source:** R-01 §3.4; R-06 drawing (mud sump shown at east exterior of wash bay) (SOW-0027b)

**Verification:** Pipe sizing calculation for wash bay drain line to mud sump; sump volume sizing TBD (ASSUMPTION: sized to accept motor-scraper wash-down volumes; specific volume to be determined by Plumbing Engineer).

---

### REQ-007 — Emergency Shower

**Requirement:** An emergency shower shall be installed as shown on the plumbing drawing.

**Source:** R-06 drawing (SOW-0048); emergency shower shown on south wall near wash bay entrance

**Verification:** Flow rate and pressure supply calculation confirming emergency shower can deliver minimum flow as required by applicable safety standards. ASSUMPTION: ANSI Z358.1 (Emergency Eyewash and Shower Equipment) or equivalent Alberta occupational health and safety standard applies; specific standard TBD.

**TBD — Resolution required:** Confirm which emergency shower standard applies (ANSI Z358.1 or Alberta OHS equivalent) and obtain specific minimum flow rate (e.g., 75.7 LPM / 20 GPM per ANSI Z358.1 -- ASSUMPTION: location TBD) and minimum duration (e.g., 15 minutes per ANSI Z358.1 -- ASSUMPTION: location TBD) for use as acceptance values in verification. Resolution path: Plumbing Engineer to confirm with OH&S authority. Source: _SEMANTIC_LENSING.md item F-001.

---

### REQ-008 — Water Taps and Pressure Washer Reels

**Requirement:** Water taps and pressure washer reel(s) shall be installed as shown on the plumbing drawing.

**Source:** R-06 drawing (SOW-0049); drawing shows water tap and pressure washer reel at north bay area, and water tap at south area

**Verification:** Supply sizing calculation confirms adequate flow and pressure at tap and reel connections accounting for simultaneous use assumptions (ASSUMPTION: simultaneous demand factor TBD by Plumbing Engineer).

**Note on simultaneous demand:** The simultaneous demand factor is foundational to supply sizing for REQ-002, REQ-007, and REQ-008 but is currently TBD with no resolution method specified at the requirement level. The Plumbing Engineer must define the design simultaneous demand scenario (see Trade-off 3 in Guidance.md) and document the adopted factor in Step 2.3 of Procedure.md. Source: _SEMANTIC_LENSING.md item X-001.

---

### REQ-009 — Industrial Wash Station

**Requirement:** A separate industrial wash sink (wash station) shall be installed.

**Source:** R-01 §3.1 (SOW-0050); R-06 drawing (wash station shown at south wall)

**Verification:** Fixture connection sizing per NPC (ASSUMPTION); drain sizing calculation; connection confirmed on drawings.

---

### REQ-010 — Code Compliance

**Requirement:** All plumbing systems shall comply with applicable Alberta Safety Codes and governing plumbing codes.

**Source:** R-01 §3.3.2 (SOW-0008, SOW-0009)

**Verification:** Code compliance matrix included in calculation package; Safety Code permit obtained (PKG-009 scope).

---

### REQ-011 — P.Eng. Stamp

**Requirement:** All IFC plumbing drawings and supporting calculations shall be signed and stamped by a Professional Engineer licensed to practice in Alberta.

**Source:** R-01 §3.3.2 (SOW-0018)

**Verification:** Stamp and signature present on IFC drawings and calculation package cover sheet.

---

### REQ-012 — Washroom Plumbing

**Requirement:** Washroom plumbing (fixtures, supply, and drainage) shall be included for the new washroom within the New North Shop addition. Expanded washroom facilities including urinal shall be addressed.

**Source:** R-01 §3.4 (SOW-0074); R-06 drawing (washroom shown adjacent to utility room)

**Verification:** Fixture unit count, supply sizing, and drain sizing calculations for washroom; urinal fixture included per R-01 §3.4.

---

## Standards

| Standard / Code | Applicability | Status |
|---|---|---|
| National Plumbing Code of Canada (NPC) | Pipe sizing, fixture units, drainage, venting | ASSUMPTION: likely governing; edition TBD. Specific clause requirements cannot be derived until code edition is confirmed |
| Alberta Safety Codes Act — Plumbing Safety Code Order | Regulatory authority for plumbing installations in Alberta | ASSUMPTION: likely applicable; location TBD |
| ANSI Z358.1 (Emergency Eyewash and Shower) | Emergency shower flow and pressure requirements | ASSUMPTION: likely applicable; specific standard TBD |
| Alberta Environment / AER | Septic/holding tank siting and installation approval | ASSUMPTION: applicable; approval authority and requirements TBD |
| CCDC 14–2013 | Contract framework | R-01 §2.7 |

**Note:** No specific plumbing code editions or clause-level requirements are cited in the accessible source documents (R-01 and R-06). All standard citations above are marked ASSUMPTION pending review of applicable Safety Code order and permit conditions.

**Resolution path (TBD):** The Plumbing Engineer must confirm the applicable NPC edition and Alberta Safety Code Plumbing Order edition with the Safety Codes Officer at the permit pre-application stage. Until editions are confirmed, clause-level requirements cannot be derived and all code-based sizing references remain ASSUMPTION. Source: R-01 §3.3.2; _SEMANTIC_LENSING.md items A-001, C-001.

---

## Verification

| Requirement | Verification Approach |
|---|---|
| REQ-001 (Cistern volume) | Confirm ≥ 50,000 L in tank data sheet; calculation cover sheet sign-off |
| REQ-002 (Pump 100 LPM) | Pump curve analysis; system curve calculation; confirm operating point ≥ 100 LPM. The pump manufacturer's performance curve shall be included as evidence in the calculation package (see Records in Procedure.md — Equipment Performance Data Sheets). Source: _SEMANTIC_LENSING.md item X-003. |
| REQ-003 (Bulk water fill) | Pump selection calculation; pipe sizing calculation; flow rate TBD (see Conflict Table in Guidance.md) |
| REQ-004 (Septic 2,000 US gal) | Sizing calculation; confirm capacity per fixture unit loading; regulatory authority approval — **approval artifact TBD** (e.g., permit, approval letter, or compliance certificate from Alberta Environment / AER; specific evidence of approval to be defined by Plumbing Engineer). Source: _SEMANTIC_LENSING.md item D-001. |
| REQ-005 (Floor drains) | Drain count and location confirmed vs. R-06; slope and pipe sizing calculations. Minimum slope pass criterion: per NPC table for pipe diameter (ASSUMPTION: e.g., 1/4" per foot for pipes 3" and smaller, 1/8" per foot for pipes 4" and larger — specific values TBD once NPC edition is confirmed). Source: _SEMANTIC_LENSING.md item X-005. |
| REQ-006 (Wash bay / mud sump) | Drain line sizing; sump volume calculation |
| REQ-007 (Emergency shower) | Supply pressure and flow calculation vs. applicable standard |
| REQ-008 (Taps and reel) | Simultaneous demand calculation; pressure available at point of use |
| REQ-009 (Wash station) | Fixture unit count and drain sizing |
| REQ-010 (Code compliance) | Code compliance matrix included in calculation package; completeness verified by confirming all applicable NPC sections and Alberta Safety Code Plumbing Order sections are addressed (scope of matrix sections TBD — Plumbing Engineer to define once code edition is confirmed). Source: _SEMANTIC_LENSING.md item A-002. |
| REQ-011 (P.Eng. stamp) | Cover sheet sign-off by licensed Alberta P.Eng. |
| REQ-012 (Washroom) | Fixture unit count, supply and drain sizing |
| Calculation Accuracy (QA/QC) | Calculation correctness shall be verified through an independent check methodology (e.g., peer review, independent spot-check of critical calculations) as defined by the P.Eng. QA/QC standard for the project. ASSUMPTION: specific methodology TBD — P.Eng. to define the QA/QC standard for calculation review. Source: _SEMANTIC_LENSING.md item F-005. |

---

## SOW Traceability

The following table maps SOW items from the decomposition to requirements in this specification. Source: WDMLRL_Decomposition_Claude.md (PKG-006); _SEMANTIC_LENSING.md item X-002.

| SOW Item | Description | Mapped Requirement(s) |
|---|---|---|
| SOW-0041 | 50,000 L cistern with all necessary plumbing | REQ-001 |
| SOW-0042 | 100 LPM internal distribution pump, 2.5" fill connection | REQ-002 |
| SOW-0043 | 2,000 US gallon septic holding tank (replace existing) | REQ-004 |
| SOW-0044 | Bulk water fill system with high-volume pump | REQ-003 |
| SOW-0045 | Floor drains and sump drains in repair bays | REQ-005 |
| SOW-0046 | Floor drains throughout shop per drawing | REQ-005 |
| SOW-0027b | Wash bay drainage to exterior mud sump | REQ-006 |
| SOW-0048 | Emergency shower per drawing | REQ-007 |
| SOW-0049 | Water taps and pressure washer reels per drawing | REQ-008 |
| SOW-0050 | Industrial wash station | REQ-009 |
| SOW-0008 | Safety Code compliance | REQ-010 |
| SOW-0009 | Code compliance general | REQ-010 |
| SOW-0018 | P.Eng. stamp on IFC drawings and calculations | REQ-011 |
| SOW-0074 | Washroom plumbing including urinal | REQ-012 |
| SOW-0073 | Old North Shop washroom renovation / locker room | TBD — contingent on CFT-001 scope resolution |
| SOW-0016 | Complete final plumbing design | All REQs (umbrella SOW) |

---

## Documentation

The following artifacts are anticipated as components of this calculation package (from `_CONTEXT.md` — Anticipated Artifacts):

| Artifact | Status |
|---|---|
| Water demand and consumption calculations | To be produced |
| Water supply line sizing calculations | To be produced |
| Pressure drop and pump selection calculations | To be produced |
| Drainage system sizing and slope calculations | To be produced |
| Vent stack sizing calculations | To be produced |
| Septic system sizing calculations | To be produced |
| Code compliance matrices | To be produced |
| Design assumption documentation | To be produced |
| Equipment performance data sheets | To be produced |

All artifacts shall be assembled into a single coordinated calculation package. The package cover sheet shall bear the P.Eng. stamp and signature of the responsible Plumbing Engineer.

**Downstream use during guarantee period:** The calculation package serves as the design record referenced during the construction period and the subsequent 2-year guarantee period (R-01 §2.10). Design assumptions documented in the package will be the baseline for evaluating any warranty claims or operational issues related to plumbing system performance during the guarantee period. Source: R-01 §2.10; Guidance.md Purpose item 4; Datasheet.md Conditions; _SEMANTIC_LENSING.md item E-004.
