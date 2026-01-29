# Assumptions Log

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG23_DRAFT_2026-01-28_2400 |
| Package | PKG-23 Fire Protection |
| Date | 2026-01-28 |

## Assumption Entries

### A-001: Fire Water Loop Piping Scope

**Assumption:** Fire water loop includes approximately 500-800 LM of underground ductile iron pipe (DN150-DN300) serving tank farm, railcar unloading area, and marine loading platform, plus 200-400 LM of above-ground steel pipe (DN100-DN200) for risers and equipment connections.

**Why Needed:** No design drawings or pipe routing available; fire water loop scope required for materials and construction estimate.

**Impacted WBS/CBS:**
- WBS: DEL-23.01, DEL-23.02, DEL-23.05
- CBS: MAT (fire water piping), CD (excavation and installation)

**Cost Impact:** $230,000 - $350,000 CAD (materials)

**Confidence:** LOW

**Resolution Path:** Complete DEL-23.01 fire water loop layout drawings; complete DEL-23.03 hydraulic calculations for pipe sizing

---

### A-002: Fire Hydrant Quantity

**Assumption:** Fire hydrant system includes 8-12 dry-barrel fire hydrants (rated for -40°C per BC climate), 2 fire department connections (FDC), and associated hose bibs at key locations throughout the facility.

**Why Needed:** No fire protection zone plan or hydrant layout available; hydrant quantity required for materials and installation estimate.

**Impacted WBS/CBS:**
- WBS: DEL-23.01, DEL-23.04, DEL-23.05
- CBS: MAT (fire hydrants and accessories), CD (installation)

**Cost Impact:** $100,000 - $150,000 CAD (materials + installation)

**Confidence:** LOW

**Resolution Path:** Complete DEL-23.01 hydrant location drawings; confirm hydrant spacing per NFPA 24 and local fire department requirements

---

### A-003: Fire Water Valves and Fittings

**Assumption:** Fire water system includes 12-18 isolation valves (OS&Y gate valves), 4-6 post-indicator valves (PIV), 2-4 check valves, and associated fittings for loop sectionalizing and equipment isolation.

**Why Needed:** No valve schedule or system schematic available; valve quantities required for materials estimate.

**Impacted WBS/CBS:**
- WBS: DEL-23.01, DEL-23.02
- CBS: MAT (valves and fittings)

**Cost Impact:** $40,000 - $70,000 CAD

**Confidence:** LOW

**Resolution Path:** Complete DEL-23.01 fire water system schematic; develop valve schedule

---

### A-004: Fire Alarm Control Panel

**Assumption:** Fire alarm system includes 1 addressable fire alarm control panel (FACP) per ULC-S527 with network interface for DCS integration (PKG-19), battery backup per NFPA 72, and 1-2 remote annunciator panels at key operator locations.

**Why Needed:** No fire alarm system design available; FACP scope required for materials and installation estimate.

**Impacted WBS/CBS:**
- WBS: DEL-23.01, DEL-23.02, DEL-23.04
- CBS: MAT (FACP and accessories)

**Cost Impact:** $50,000 - $80,000 CAD

**Confidence:** LOW

**Resolution Path:** Complete DEL-23.01 fire alarm system drawings; confirm FACP size based on device count; coordinate with PKG-19 control systems for DCS integration

---

### A-005: Fire Detection and Notification Devices

**Assumption:** Fire alarm system includes approximately:
- 40-60 heat detectors (rate-of-rise and fixed temperature)
- 15-25 flame detectors (UV/IR or multi-spectrum for outdoor areas)
- 10-20 smoke detectors (photoelectric for buildings/control rooms)
- 20-30 manual pull stations
- 40-60 notification appliances (horn/strobe combinations)

**Why Needed:** No fire alarm device schedule available; device quantities required for materials and wiring estimate.

**Impacted WBS/CBS:**
- WBS: DEL-23.01, DEL-23.04, DEL-23.05
- CBS: MAT (detection devices, notification appliances, wiring)

**Cost Impact:** $150,000 - $220,000 CAD (devices + wiring)

**Confidence:** LOW

**Resolution Path:** Complete DEL-23.01 fire alarm device layout; develop device schedule based on fire protection zones and detection requirements

---

### A-006: Foam Concentrate Storage and Proportioning

**Assumption:** Foam suppression system includes 1 foam concentrate storage tank (2,000-4,000 gallon capacity) and 1 foam proportioning system (balanced pressure proportioner or bladder tank type) sized for simultaneous protection of largest tank plus exposures.

**Why Needed:** No foam system design or fire water demand calculation available; foam storage and proportioning scope required for materials and installation estimate.

**Impacted WBS/CBS:**
- WBS: DEL-23.01, DEL-23.02, DEL-23.03, DEL-23.04
- CBS: MAT (foam tank, proportioner, foam concentrate)

**Cost Impact:** $150,000 - $220,000 CAD

**Confidence:** LOW

**Resolution Path:** Complete DEL-23.03 foam system sizing calculations per NFPA 11/16; confirm foam concentrate type (AR-AFFF 3% assumed); obtain budgetary quotes from foam equipment vendors

---

### A-007: Tank Foam Discharge Systems

**Assumption:** Tank foam system includes foam chambers or foam makers for each of 3 × 15,000 MT storage tanks, with foam piping from proportioning system to each tank top, foam application rate per NFPA 11/16 for Class IIIA combustible liquids.

**Why Needed:** No tank foam system design available; tank foam discharge scope required for materials and installation estimate.

**Impacted WBS/CBS:**
- WBS: DEL-23.01, DEL-23.04
- CBS: MAT (foam chambers, foam piping), CD (installation)

**Cost Impact:** $120,000 - $180,000 CAD

**Confidence:** LOW

**Resolution Path:** Complete DEL-23.03 foam system calculations for 3 × 15,000 MT tanks; confirm foam discharge device type (foam chamber vs foam maker); coordinate with PKG-13 storage tanks for mounting details

---

### A-008: Marine Loading Foam System

**Assumption:** Marine loading foam system includes foam monitors or nozzles on the marine loading platform for protection during ship loading operations, with foam piping from main proportioning system, per NFPA 11/16 requirements.

**Why Needed:** No marine loading foam design available; marine foam scope required for materials and installation estimate.

**Impacted WBS/CBS:**
- WBS: DEL-23.01, DEL-23.04
- CBS: MAT (foam monitors, foam piping), CD (installation)

**Cost Impact:** $80,000 - $120,000 CAD

**Confidence:** LOW

**Resolution Path:** Complete DEL-23.01 marine loading foam layout; confirm foam discharge device type (monitors vs nozzles); coordinate with PKG-08/PKG-09 marine structures for mounting details

---

### A-009: Fire Water and Fire Alarm Material Pricing

**Assumption:** Fire protection material pricing uses typical market rates for fire protection systems in BC Lower Mainland as of January 2026:
- Underground ductile iron pipe: $200-350/LM depending on diameter
- Above-ground steel pipe: $150-250/LM depending on diameter
- Dry-barrel fire hydrant: $8,000-15,000 each (rated for -40°C)
- Fire department connection: $5,000-8,000 each
- Addressable FACP: $40,000-60,000 depending on capacity
- Heat/smoke detectors: $300-600 each installed
- Flame detectors: $2,000-4,000 each installed
- Manual pull stations: $400-800 each installed
- Horn/strobe devices: $500-1,000 each installed

**Why Needed:** No vendor quotes or rate tables available; material pricing required for MAT bucket estimate.

**Impacted WBS/CBS:**
- WBS: DEL-23.01, 23.02, 23.04
- CBS: MAT (Materials)

**Cost Impact:** Material allowances are based on these assumed unit rates; actual costs may vary ±20-30% depending on market conditions and specifications

**Confidence:** LOW

**Resolution Path:** Obtain budgetary quotes from fire protection equipment suppliers and vendors; update _RateTables/ with project-specific unit costs

---

### A-010: Fire Alarm Wiring and Conduit

**Assumption:** Fire alarm wiring includes approximately 3,000-5,000 LM of fire alarm cable per ULC-S139, with conduit routing through outdoor areas, junction boxes, and weatherproof enclosures for field devices.

**Why Needed:** No fire alarm wiring design available; wiring scope required for materials and installation estimate.

**Impacted WBS/CBS:**
- WBS: DEL-23.01
- CBS: MAT (fire alarm cable, conduit, enclosures), CD (wiring installation)

**Cost Impact:** $50,000 - $80,000 CAD

**Confidence:** LOW

**Resolution Path:** Complete DEL-23.01 fire alarm wiring diagrams; develop cable schedule based on device locations and routing

---

### A-011: Foam System Material Pricing

**Assumption:** Foam system material pricing uses typical market rates:
- Foam concentrate storage tank (atmospheric, carbon steel): $15,000-25,000 depending on capacity
- Foam proportioning system (balanced pressure or bladder tank): $60,000-100,000 depending on capacity
- Foam chambers/makers for tanks: $20,000-40,000 each depending on tank size
- Foam monitors: $10,000-20,000 each
- Foam concentrate (AR-AFFF 3%): $15-25/gallon
- Foam piping (carbon steel Schedule 40): $80-150/LM installed

**Why Needed:** No vendor quotes for foam equipment available; foam material pricing required for MAT bucket estimate.

**Impacted WBS/CBS:**
- WBS: DEL-23.01, 23.02, 23.04
- CBS: MAT (foam system equipment)

**Cost Impact:** Foam system allowances are based on these assumed unit rates; actual costs may vary ±20-30% depending on market conditions and foam type selection

**Confidence:** LOW

**Resolution Path:** Obtain budgetary quotes from foam system vendors; confirm foam concentrate type and quantity requirements

---

### A-012: Engineering Labor Hours

**Assumption:** Engineering effort for PKG-23 includes approximately 900-1,200 hours total for all 5 deliverables, distributed across:
- Fire protection engineers (senior + intermediate): 500-700 hours (DEL-23.01, 23.02, 23.03, 23.04)
- CAD technicians: 250-350 hours (DEL-23.01 drawing production)
- QA/QC reviewers: 150-200 hours (interdisciplinary checks, code compliance review)

**Why Needed:** No engineering labor hour budgets or resource loading available; engineering hours required for E bucket estimate.

**Impacted WBS/CBS:**
- WBS: All DEL-23.xx deliverables
- CBS: E (Engineering)

**Cost Impact:** $150,000 - $200,000 CAD (assuming blended rate $145-175/hr for fire protection engineering and CAD)

**Confidence:** LOW

**Resolution Path:** Provide engineering labor hour breakdown by discipline and deliverable; provide project labor rate table

---

### A-013: Fire Water Loop Installation Productivity

**Assumption:** Fire water loop installation productivity is standard for underground utility work in BC Lower Mainland:
- Excavation and backfill: 25-40 LM/day depending on trench depth and ground conditions
- Pipe laying (underground): 30-50 LM/day depending on pipe diameter
- Above-ground pipe installation: 20-35 LM/day including supports

**Why Needed:** No productivity data or crew compositions available; installation productivity required for CD bucket estimate.

**Impacted WBS/CBS:**
- WBS: DEL-23.01
- CBS: CD (Construction Directs)

**Cost Impact:** Installation costs are based on assumed productivity rates; actual costs may vary ±15-25% depending on site conditions and crew experience

**Confidence:** LOW

**Resolution Path:** Provide site logistics plan; confirm ground conditions per PKG-02 geotechnical data; coordinate with PKG-03 underground utilities for shared excavation opportunities

---

### A-014: Fire Water Loop Installation Cost

**Assumption:** Fire water loop installation includes trench excavation, pipe laying, valve installation, thrust blocks, hydrostatic testing, and backfill for approximately 700-1,200 total LM of pipe.

**Why Needed:** No construction estimate or take-off available; installation cost required for CD bucket estimate.

**Impacted WBS/CBS:**
- WBS: DEL-23.01, DEL-23.05
- CBS: CD (Construction Directs)

**Cost Impact:** $250,000 - $350,000 CAD

**Confidence:** LOW

**Resolution Path:** Complete DEL-23.01 fire water loop layout; coordinate with PKG-03 underground utilities for shared trenching; obtain budgetary quotes for installation

---

### A-015: Fire Hydrant Installation Cost

**Assumption:** Fire hydrant installation includes concrete pads, hydrant assembly installation, valve box installation, thrust block construction, and connection to fire water loop for 8-12 hydrants plus 2 FDC units.

**Why Needed:** No installation estimate available; hydrant installation cost required for CD bucket estimate.

**Impacted WBS/CBS:**
- WBS: DEL-23.04, DEL-23.05
- CBS: CD (Construction Directs)

**Cost Impact:** $45,000 - $70,000 CAD

**Confidence:** LOW

**Resolution Path:** Complete DEL-23.01 hydrant location drawings; coordinate with local fire department for FDC locations and requirements

---

### A-016: Fire Alarm System Installation Cost

**Assumption:** Fire alarm system installation includes FACP mounting and wiring, conduit installation (3,000-5,000 LM), device mounting (120-175 devices total), cable pulling and termination, and system programming and testing.

**Why Needed:** No installation estimate available; fire alarm installation cost required for CD bucket estimate.

**Impacted WBS/CBS:**
- WBS: DEL-23.01, DEL-23.05
- CBS: CD (Construction Directs)

**Cost Impact:** $80,000 - $110,000 CAD

**Confidence:** LOW

**Resolution Path:** Complete DEL-23.01 fire alarm wiring diagrams; develop device schedule; coordinate with PKG-17/PKG-19 for power supply and DCS integration

---

### A-017: Foam System Installation Cost

**Assumption:** Foam system installation includes foam tank installation, proportioning system installation, foam piping to tanks (approximately 200-400 LM), foam chamber/maker mounting on 3 tanks, marine loading foam system installation, and system testing and commissioning.

**Why Needed:** No installation estimate available; foam system installation cost required for CD bucket estimate.

**Impacted WBS/CBS:**
- WBS: DEL-23.04, DEL-23.05
- CBS: CD (Construction Directs)

**Cost Impact:** $125,000 - $175,000 CAD

**Confidence:** LOW

**Resolution Path:** Complete DEL-23.01 foam system layout; coordinate with PKG-13 storage tanks and PKG-08/PKG-09 marine structures for mounting details; obtain installation budgetary quotes

---

### A-018: Construction Labor Productivity

**Assumption:** Construction labor productivity is standard for BC Lower Mainland (productivity factor = 1.0); no site-specific constraints that would reduce productivity.

**Why Needed:** No site logistics plan or access constraints available; productivity factor required for construction labor pricing.

**Impacted WBS/CBS:**
- WBS: All construction-related deliverables
- CBS: CD (Construction Directs), CI (Construction Indirects)

**Cost Impact:** Neutral (baseline productivity); if site constraints exist, CD and CI costs may increase 10-30%

**Confidence:** MEDIUM

**Resolution Path:** Provide site logistics plan with access restrictions, working hours, traffic management, seasonal constraints; adjust productivity factors accordingly

---

### A-019: Terminal Operations Coordination

**Assumption:** Fire protection installation can be coordinated with ongoing terminal operations; working hours may be restricted in active areas; some night work may be required for tie-ins.

**Why Needed:** No coordination plan available; terminal interface affects construction schedule and costs.

**Impacted WBS/CBS:**
- WBS: All construction-related deliverables
- CBS: CD (Construction Directs for coordination), CI (Construction Indirects)

**Cost Impact:** Terminal coordination may add 5-15% to CD/CI costs; included in allowances

**Confidence:** MEDIUM

**Resolution Path:** Coordinate with DP World terminal operations; develop fire protection installation sequence to minimize operational disruption (OBJ-5)

---

### A-020: Fire Water Supply Source

**Assumption:** Fire water supply is from municipal water system with adequate pressure for fire protection demand; no dedicated fire pump required for base estimate.

**Why Needed:** No fire water supply source confirmation available; supply source affects equipment requirements.

**Impacted WBS/CBS:**
- WBS: DEL-23.03 (affects hydraulic calculations)
- CBS: MAT, CD (fire pump would add significant cost if required)

**Cost Impact:** If fire pump required, add $150,000-300,000 CAD to estimate

**Confidence:** LOW

**Resolution Path:** Confirm municipal fire water supply pressure and flow; complete DEL-23.03 hydraulic calculations; determine if fire pump required per NFPA 20

---

### A-021: Product Classification

**Assumption:** CSD canola oil is classified as Class IIIA combustible liquid per NFPA 30 (flash point typically >93°C / 200°F), which determines fire protection requirements.

**Why Needed:** Product classification drives fire protection system design requirements.

**Impacted WBS/CBS:**
- WBS: All PKG-23 deliverables
- CBS: All (fire protection requirements based on product classification)

**Cost Impact:** Class IIIA combustible liquid requires foam protection per NFPA 30; foam system is ~27% of estimate

**Confidence:** MEDIUM

**Resolution Path:** Confirm CSD canola oil flash point and NFPA 30 classification; review insurance and AHJ requirements for additional protection measures

---

### A-022: Design Codes and Standards

**Assumption:** Fire protection design is per NFPA standards (NFPA 30, 24, 11, 16, 72, 20) and Canadian codes (NBCC 2020, BCFC, ULC standards).

**Why Needed:** Code basis determines system requirements and equipment specifications.

**Impacted WBS/CBS:**
- WBS: All PKG-23 deliverables
- CBS: All (code compliance affects design and equipment)

**Cost Impact:** Included in base estimate; non-standard requirements may add 5-15% to costs

**Confidence:** MEDIUM

**Resolution Path:** Extract fire protection requirements from Employer's Requirements Volume 2 Part 1; confirm AHJ jurisdiction and any additional requirements

---
