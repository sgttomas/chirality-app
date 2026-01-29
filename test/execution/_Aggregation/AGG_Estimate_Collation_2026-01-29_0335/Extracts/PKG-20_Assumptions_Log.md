# Assumptions Log — PKG-20 Field Instrumentation

## Overview

This log records all assumptions and allowances made during the estimating process for PKG-20 Field Instrumentation. Each assumption is assigned a unique ID (A-###) and referenced from the BOE, Detail.csv, and Decision_Log.

---

## Assumptions

### A-001: Site Conditions

| Field | Value |
|-------|-------|
| Assumption | Operating terminal with active operations; coordination required |
| Why Needed | Site conditions not explicitly defined for construction phase |
| Impacted WBS/CBS | CD, CI |
| Cost Impact | CI factor accounts for coordination overhead |
| Confidence | MED |
| Resolution Path | Confirm site access plan with Terminal operations |

---

### A-002: Cable Routing Method

| Field | Value |
|-------|-------|
| Assumption | Mix of cable tray, conduit, and direct burial routing |
| Why Needed | Cable routing design not complete |
| Impacted WBS/CBS | CD (installation), MAT (conduit) |
| Cost Impact | $18/m average installation cost |
| Confidence | LOW |
| Resolution Path | Complete DEL-20.01 cable routing drawings |

---

### A-003: Instrument Environment Rating

| Field | Value |
|-------|-------|
| Assumption | Outdoor marine/industrial environment; NEMA 4X or IP66 minimum |
| Why Needed | Environmental ratings not specified |
| Impacted WBS/CBS | MAT |
| Cost Impact | Premium for marine-rated instruments |
| Confidence | MED |
| Resolution Path | Confirm environmental specification in DEL-20.02 |

---

### A-004: Tank Instrumentation Density

| Field | Value |
|-------|-------|
| Assumption | 8 instruments per storage tank (level, temperature, pressure) |
| Why Needed | Instrument count not available from P&IDs |
| Impacted WBS/CBS | MAT, CD |
| Cost Impact | 24 tank instruments total (~$108k MAT) |
| Confidence | MED |
| Resolution Path | Develop tank instrument list from PKG-13 and P&IDs |

Breakdown per tank:
- 2× Level transmitters (redundant GWR)
- 2× Level switches (HH and H)
- 2× Temperature elements
- 1× Temperature transmitter
- 1× Pressure transmitter

---

### A-005: Railcar Unloading Instrumentation

| Field | Value |
|-------|-------|
| Assumption | 40 instruments total (32 flow indicators + 8 header instruments) |
| Why Needed | Detailed instrument index not available |
| Impacted WBS/CBS | MAT, CD |
| Cost Impact | ~$38k MAT for railcar unloading instruments |
| Confidence | MED |
| Resolution Path | Develop instrument list from PKG-10 scope |

---

### A-006: Marine Loading Instrumentation

| Field | Value |
|-------|-------|
| Assumption | 12 instruments for marine loading system |
| Why Needed | Marine loading instrument scope not detailed |
| Impacted WBS/CBS | MAT, CD |
| Cost Impact | ~$44k MAT for marine loading instruments |
| Confidence | MED |
| Resolution Path | Develop instrument list from PKG-11 scope |

---

### A-007: Transfer Piping Instrumentation

| Field | Value |
|-------|-------|
| Assumption | 30 instruments for transfer piping and pump systems |
| Why Needed | P&IDs not issued; instrument count estimated |
| Impacted WBS/CBS | MAT, CD |
| Cost Impact | ~$109k MAT for transfer piping instruments |
| Confidence | LOW |
| Resolution Path | Issue P&IDs from PKG-14 DEL-14.01 |

---

### A-008: Instrument Cable Quantity

| Field | Value |
|-------|-------|
| Assumption | 8,000 linear meters of instrument cable |
| Why Needed | Cable schedule not developed |
| Impacted WBS/CBS | MAT ($96k), CD ($144k) |
| Cost Impact | ~$240k total for cable supply and installation |
| Confidence | LOW |
| Resolution Path | Complete cable schedule from DEL-20.01 |

Basis: ~75m average run per instrument × 106 instruments

---

### A-009: Junction Box Quantity

| Field | Value |
|-------|-------|
| Assumption | 25 junction boxes distributed throughout facility |
| Why Needed | JB locations not designed |
| Impacted WBS/CBS | MAT ($70k), CD ($30k) |
| Cost Impact | ~$100k total for JB supply and installation |
| Confidence | LOW |
| Resolution Path | Complete DEL-20.01 JB location drawings |

Distribution assumed:
- Tank farm: 9 JBs (3 per tank)
- Railcar unloading: 8 JBs
- Marine loading: 4 JBs
- Transfer/pump area: 4 JBs

---

### A-010: Instrument Tubing and Fittings

| Field | Value |
|-------|-------|
| Assumption | Stainless steel tubing for process connections |
| Why Needed | Material specification not defined |
| Impacted WBS/CBS | MAT ($35k), CD ($25k) |
| Cost Impact | ~$60k total for tubing and installation |
| Confidence | MED |
| Resolution Path | Confirm tubing material in DEL-20.02 |

---

### A-011: Engineering Drawing Effort

| Field | Value |
|-------|-------|
| Assumption | ~35 I&C drawings at $2,500/sheet average |
| Why Needed | Drawing list not defined |
| Impacted WBS/CBS | E |
| Cost Impact | $85,000 for DEL-20.01 |
| Confidence | LOW |
| Resolution Path | Develop drawing list for PKG-20 |

---

### A-012: Technical Specification Effort

| Field | Value |
|-------|-------|
| Assumption | ~220 hours for specification development |
| Why Needed | Specification scope not defined |
| Impacted WBS/CBS | E |
| Cost Impact | $55,000 for DEL-20.02 |
| Confidence | MED |
| Resolution Path | Define specification outline |

---

### A-013: Design Calculation Effort

| Field | Value |
|-------|-------|
| Assumption | ~140 hours for instrument sizing calculations |
| Why Needed | Calculation scope not defined |
| Impacted WBS/CBS | E |
| Cost Impact | $35,000 for DEL-20.03 |
| Confidence | MED |
| Resolution Path | Define calculation list |

---

### A-014: Data Sheet Preparation

| Field | Value |
|-------|-------|
| Assumption | ~106 instrument data sheets at $600/sheet average |
| Why Needed | Data sheet count based on instrument count |
| Impacted WBS/CBS | E |
| Cost Impact | $65,000 for DEL-20.04 |
| Confidence | LOW |
| Resolution Path | Confirm instrument count from P&IDs |

---

### A-015: Test Record Documentation

| Field | Value |
|-------|-------|
| Assumption | ~160 hours for test procedures and record compilation |
| Why Needed | Test record scope not defined |
| Impacted WBS/CBS | E |
| Cost Impact | $40,000 for DEL-20.05 |
| Confidence | MED |
| Resolution Path | Define ITP requirements |

---

### A-016: Miscellaneous Switches

| Field | Value |
|-------|-------|
| Assumption | 12 miscellaneous pressure and temperature switches for alarms |
| Why Needed | Alarm switch count not specified |
| Impacted WBS/CBS | MAT |
| Cost Impact | $21,600 |
| Confidence | LOW |
| Resolution Path | Define alarm requirements from P&IDs |

---

### A-017: Instrument Supports and Mounting

| Field | Value |
|-------|-------|
| Assumption | $28,000 allowance for mounting hardware |
| Why Needed | Mounting details not designed |
| Impacted WBS/CBS | MAT |
| Cost Impact | $28,000 |
| Confidence | LOW |
| Resolution Path | Complete installation details in DEL-20.01 |

---

### A-018: Instrument Conduit System

| Field | Value |
|-------|-------|
| Assumption | $42,000 supply + $65,000 installation for conduit |
| Why Needed | Conduit routing not designed |
| Impacted WBS/CBS | MAT, CD |
| Cost Impact | $107,000 total |
| Confidence | LOW |
| Resolution Path | Complete conduit routing in DEL-20.01 |

---

### A-019: Instrument Installation Rate

| Field | Value |
|-------|-------|
| Assumption | $850/instrument average installation cost |
| Why Needed | Installation productivity not established |
| Impacted WBS/CBS | CD |
| Cost Impact | $90,100 for 106 instruments |
| Confidence | MED |
| Resolution Path | Validate with I&C contractor rates |

---

### A-020: Calibration and Loop Testing

| Field | Value |
|-------|-------|
| Assumption | $280/instrument calibration + $350/loop testing |
| Why Needed | Commissioning scope not defined |
| Impacted WBS/CBS | CD |
| Cost Impact | $66,780 for calibration and loop testing |
| Confidence | MED |
| Resolution Path | Define commissioning requirements |

---

## Assumption Summary by CBS

| CBS | # Assumptions | Total Cost Impact | Confidence |
|-----|---------------|-------------------|------------|
| E | 5 | $280,000 | LOW-MED |
| MAT | 12 | $592,000 | LOW-MED |
| CD | 8 | $421,000 | LOW-MED |
| CI | 2 | $79,000 | LOW |
| Overall | 20 | $1,535,000 | LOW |

---

## High-Impact Assumptions

| ID | Description | Cost Impact | Resolution Priority |
|----|-------------|-------------|---------------------|
| A-008 | Cable quantity (8,000 m) | $240,000 | High |
| A-007 | Transfer piping instruments (30 units) | $109,000 | High |
| A-009 | Junction box quantity (25 units) | $100,000 | Medium |
| A-004 | Tank instrumentation (24 units) | $108,000 | Medium |
| A-019 | Installation rate ($850/instrument) | $90,100 | Medium |

---

*Assumptions Log generated by ESTIMATING Agent | 2026-01-28*
