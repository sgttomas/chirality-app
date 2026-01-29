# Assumptions Log

## Snapshot: EST_PKG19_DRAFT_2026-01-28_0015

This log records all assumptions and allowances made during estimate preparation for PKG-19 Control Systems.

---

## Assumptions

### A-001: Control Room Location

| Field | Value |
|-------|-------|
| ID | A-001 |
| Statement | Control system equipment installed in MCC building per PKG-21/22 |
| Why Needed | Control room location not explicitly defined |
| Impacted WBS/CBS | CD (installation), MAT (environmental ratings) |
| Cost Impact | Minimal; assumes climate-controlled environment |
| Confidence | MEDIUM |
| Resolution Path | Confirm control room location in site layout (PKG-21) |

---

### A-002: Site Access

| Field | Value |
|-------|-------|
| ID | A-002 |
| Statement | Normal industrial site access; no special access constraints for control system installation |
| Why Needed | Site access conditions not defined |
| Impacted WBS/CBS | CD, CI |
| Cost Impact | +10-20% if restricted access or extended distances |
| Confidence | MEDIUM |
| Resolution Path | Confirm site logistics in project execution plan |

---

### A-003: Redundant DCS/PLC Controllers

| Field | Value |
|-------|-------|
| ID | A-003 |
| Statement | Two redundant DCS/PLC controllers (primary and standby) |
| Why Needed | Redundancy level not specified; assumed for reliability (OBJ-1) |
| Impacted WBS/CBS | MAT |
| Cost Impact | $180,000 for controller pair vs. $90,000 for single |
| Confidence | MEDIUM |
| Resolution Path | Define redundancy requirements in DEL-19.02 specification |

---

### A-004: Three HMI Workstations

| Field | Value |
|-------|-------|
| ID | A-004 |
| Statement | Three HMI workstations: 2 operator stations + 1 engineering station |
| Why Needed | HMI count not specified |
| Impacted WBS/CBS | MAT, CD |
| Cost Impact | $75,000 materials + installation |
| Confidence | MEDIUM |
| Resolution Path | Define operator console arrangement in DEL-19.01 drawings |

---

### A-005: Three Remote HMI Panels

| Field | Value |
|-------|-------|
| ID | A-005 |
| Statement | Three remote HMI panels at: railcar unloading area, tank farm, marine loading platform |
| Why Needed | Remote HMI locations not specified |
| Impacted WBS/CBS | MAT, CD |
| Cost Impact | $45,000 materials + $24,000 installation |
| Confidence | LOW |
| Resolution Path | Define remote HMI requirements based on operations philosophy |

---

### A-006: I/O Point Count Estimate

| Field | Value |
|-------|-------|
| ID | A-006 |
| Statement | Estimated I/O count: 600-800 points based on facility scope |
| Why Needed | I/O list not available; PKG-20 instrumentation not complete |
| Impacted WBS/CBS | MAT (I/O modules) |
| Cost Impact | $120,000 based on estimate; could be +/- 30% |
| Confidence | LOW |
| Resolution Path | Complete PKG-20 instrumentation design and I/O list |

---

### A-007: I/O Module Quantity

| Field | Value |
|-------|-------|
| ID | A-007 |
| Statement | 40-50 I/O modules to support 600-800 I/O points |
| Why Needed | Module count derived from I/O point estimate |
| Impacted WBS/CBS | MAT |
| Cost Impact | ~$3,000/module average |
| Confidence | LOW |
| Resolution Path | Complete I/O list and module selection |

---

### A-008: Historian Tag Count

| Field | Value |
|-------|-------|
| ID | A-008 |
| Statement | Historian configured for 400-600 process and calculated tags |
| Why Needed | Tag count not defined |
| Impacted WBS/CBS | MAT (historian licensing), E (configuration) |
| Cost Impact | Licensing typically by tag count tier |
| Confidence | LOW |
| Resolution Path | Define tag requirements in historian specification |

---

### A-009: Network Switch Quantity

| Field | Value |
|-------|-------|
| ID | A-009 |
| Statement | 8-10 industrial network switches for control network |
| Why Needed | Network architecture not designed |
| Impacted WBS/CBS | MAT, CD |
| Cost Impact | $60,000 for switches |
| Confidence | LOW |
| Resolution Path | Complete network architecture design in DEL-19.01 |

---

### A-010: Fiber Optic Infrastructure

| Field | Value |
|-------|-------|
| ID | A-010 |
| Statement | 2,000 meters of fiber optic cable for control network backbone |
| Why Needed | Cable routing not designed; distances estimated |
| Impacted WBS/CBS | MAT, CD |
| Cost Impact | $80,000 materials + $80,000 installation |
| Confidence | LOW |
| Resolution Path | Complete cable routing design |

---

### A-011: Control Cabinet Quantity

| Field | Value |
|-------|-------|
| ID | A-011 |
| Statement | 6-8 control cabinets (main panels + field junction boxes) |
| Why Needed | Cabinet count not defined |
| Impacted WBS/CBS | MAT, CD |
| Cost Impact | $120,000 materials + $64,000 installation |
| Confidence | LOW |
| Resolution Path | Complete cabinet layout design in DEL-19.01 |

---

### A-012: HMI Graphics Screen Count

| Field | Value |
|-------|-------|
| ID | A-012 |
| Statement | 40-60 HMI graphics screens for operator interface |
| Why Needed | HMI scope not defined |
| Impacted WBS/CBS | E (HMI development) |
| Cost Impact | $30,000 for HMI graphics development |
| Confidence | LOW |
| Resolution Path | Define HMI screen list based on operations requirements |

---

### A-013: Standard Control System Complexity

| Field | Value |
|-------|-------|
| ID | A-013 |
| Statement | Standard industrial control system complexity (typical liquid terminal) |
| Why Needed | Control strategies not defined |
| Impacted WBS/CBS | E (software development) |
| Cost Impact | Complex sequences or batch operations would increase software cost |
| Confidence | MEDIUM |
| Resolution Path | Complete control narratives and P&IDs |

---

### A-014: No Safety Instrumented System (SIS)

| Field | Value |
|-------|-------|
| ID | A-014 |
| Statement | Basic Process Control System (BPCS) only; no separate SIS |
| Why Needed | SIS requirements not determined; HAZOP not complete |
| Impacted WBS/CBS | MAT, E |
| Cost Impact | SIS would add $200,000-400,000 if required |
| Confidence | LOW |
| Resolution Path | Complete HAZOP (PKG-27) and determine SIL requirements |

---

### A-015: Design Drawing Effort

| Field | Value |
|-------|-------|
| ID | A-015 |
| Statement | Control system design drawings effort: $60,000 (architecture + layouts) |
| Why Needed | No engineering estimate basis |
| Impacted WBS/CBS | E (DEL-19.01) |
| Cost Impact | As stated |
| Confidence | LOW |
| Resolution Path | Obtain engineering hours estimate from I&C discipline |

---

### A-016: Specification Effort

| Field | Value |
|-------|-------|
| ID | A-016 |
| Statement | Technical specification effort: $40,000 (DCS/PLC + HMI + historian specs) |
| Why Needed | No engineering estimate basis |
| Impacted WBS/CBS | E (DEL-19.02) |
| Cost Impact | As stated |
| Confidence | LOW |
| Resolution Path | Obtain engineering hours estimate from I&C discipline |

---

### A-017: Data Sheet Review Effort

| Field | Value |
|-------|-------|
| ID | A-017 |
| Statement | Data sheet package review effort: $20,000 |
| Why Needed | No engineering estimate basis |
| Impacted WBS/CBS | E (DEL-19.03) |
| Cost Impact | As stated |
| Confidence | MEDIUM |
| Resolution Path | Based on typical vendor submittal review process |

---

### A-018: Software Development Effort

| Field | Value |
|-------|-------|
| ID | A-018 |
| Statement | Software development effort: $120,000 (PLC logic $80k + HMI $30k + historian $10k) |
| Why Needed | No detailed software scope |
| Impacted WBS/CBS | E (DEL-19.04) |
| Cost Impact | Could be +/- 50% depending on control complexity |
| Confidence | LOW |
| Resolution Path | Define control strategies and complete software scope |

---

### A-019: Software License Costs

| Field | Value |
|-------|-------|
| ID | A-019 |
| Statement | Control system software licenses: $100,000 (DCS/PLC + HMI + historian) |
| Why Needed | No vendor pricing |
| Impacted WBS/CBS | MAT |
| Cost Impact | Highly vendor-dependent; range $50k-200k |
| Confidence | LOW |
| Resolution Path | Obtain vendor license pricing |

---

### A-020: Miscellaneous Materials

| Field | Value |
|-------|-------|
| ID | A-020 |
| Statement | Miscellaneous cables and terminations: $60,000 |
| Why Needed | No bill of materials |
| Impacted WBS/CBS | MAT, CD |
| Cost Impact | As stated |
| Confidence | LOW |
| Resolution Path | Complete cable schedule and termination count |

---

### A-021: QA/QC Documentation

| Field | Value |
|-------|-------|
| ID | A-021 |
| Statement | Installation quality records and documentation: $32,000 |
| Why Needed | No detailed QA/QC scope |
| Impacted WBS/CBS | CD (DEL-19.05) |
| Cost Impact | As stated |
| Confidence | MEDIUM |
| Resolution Path | Define QA/QC requirements |

---

### A-022: FAT/SAT Costs

| Field | Value |
|-------|-------|
| ID | A-022 |
| Statement | FAT $25,000 + SAT $20,000 + commissioning support $10,000 |
| Why Needed | No detailed test scope |
| Impacted WBS/CBS | COM |
| Cost Impact | As stated; travel costs assumed in allowance |
| Confidence | MEDIUM |
| Resolution Path | Define FAT/SAT scope and location |

---

## Assumption Summary

| ID | Short Description | Cost Impact | Confidence |
|----|-------------------|-------------|------------|
| A-001 | Control room in MCC building | Minimal | MEDIUM |
| A-002 | Normal site access | Minimal | MEDIUM |
| A-003 | Redundant controllers | $180,000 | MEDIUM |
| A-004 | 3 HMI workstations | $75,000 | MEDIUM |
| A-005 | 3 remote HMI panels | $69,000 | LOW |
| A-006 | 600-800 I/O points | Sizing basis | LOW |
| A-007 | 40-50 I/O modules | $120,000 | LOW |
| A-008 | 400-600 historian tags | $80,000 | LOW |
| A-009 | 8-10 network switches | $60,000 | LOW |
| A-010 | 2,000m fiber optic | $160,000 | LOW |
| A-011 | 6-8 control cabinets | $184,000 | LOW |
| A-012 | 40-60 HMI screens | Development basis | LOW |
| A-013 | Standard complexity | Basis | MEDIUM |
| A-014 | No SIS included | Exclusion | LOW |
| A-015 | Design drawing effort | $60,000 | LOW |
| A-016 | Specification effort | $40,000 | LOW |
| A-017 | Data sheet review | $20,000 | MEDIUM |
| A-018 | Software development | $120,000 | LOW |
| A-019 | Software licenses | $100,000 | LOW |
| A-020 | Misc cables/term | $60,000 | LOW |
| A-021 | QA/QC documentation | $32,000 | MEDIUM |
| A-022 | FAT/SAT costs | $55,000 | MEDIUM |
