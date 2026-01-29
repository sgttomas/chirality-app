# Guidance: DEL-32.06 Code Compliance Installation & Test Records

## Purpose

Supports **Code Compliance Installation & Test Records** for **PKG-32**.

**Purpose:** Evidence of code compliance (Source: _CONTEXT.md)
**Type:** Record | **Discipline:** Project Delivery | **Responsible:** QA/QC
**Objective:** OBJ-6: Regulatory Compliance

## Principles

### 1. Multi-Code Compliance
Code compliance spans multiple codes (building, fire, electrical, plumbing, gas) and multiple authorities. Coordination across all codes required.

### 2. Progressive Inspection Requirement
Building authorities typically require progressive inspections at key construction stages (foundations, framing, fire protection, final). Missing an inspection can delay project.

### 3. Occupancy Permit as Final Gate
Occupancy permit is final authority approval to use facility. All code conditions must be satisfied before occupancy permit issued.

## Considerations

### Code Compliance Condition Categories (Typical)
- **Building code:** Structural compliance, building envelope, accessibility, seismic design verification
- **Fire code:** Fire protection systems (sprinklers, alarms, detection), exits/egress, fire separations, flammable liquid storage compliance
- **Electrical code:** Electrical installations, hazardous area classifications (canola oil facility), emergency power
- **Plumbing code:** Plumbing systems, drainage
- **Gas code:** Gas systems (if applicable)

### Inspection Types
- **Foundation inspections:** Before concrete pour
- **Framing inspections:** At framing stage
- **Rough-in inspections:** Electrical/plumbing/HVAC rough-in before concealment
- **Fire protection inspections:** Fire system installation and testing
- **Final inspections:** Pre-occupancy final inspection
- **Occupancy permit:** Final authority approval

### Interface with DEL-32.02
Building/fire/code permits (DEL-32.02) → Extract conditions → Assign to DEL-32.06 → Track compliance → Pass inspections → Obtain occupancy permit

## Trade-offs

### Progressive Inspection Coordination vs Construction Schedule
**Trade-off:** Coordinate inspections proactively (schedule confidence, inspector availability) vs reactively call inspections (faster execution, risk of inspector unavailability).
**Recommendation:** Proactive coordination; building inspector availability can be limited, and missed inspections delay project.

## Examples

**Example Building Permit Condition:**
"The following inspections are required: (1) Foundation inspection before concrete pour; (2) Framing inspection; (3) Rough-in inspection (electrical, plumbing); (4) Fire protection system inspection after installation; (5) Final inspection before occupancy. Occupancy permit will be issued upon satisfactory completion of all inspections and compliance with building, fire, and electrical codes."

**Compliance demonstration:**
- Schedule foundation inspection; pass inspection; file inspection report in DEL-32.06
- Schedule framing inspection; pass inspection; file report
- Schedule rough-in inspection; pass inspection; file report
- Schedule fire protection inspection; pass fire system tests; pass inspection; file test reports and inspection report
- Schedule final inspection; pass inspection; file report
- Apply for occupancy permit; receive occupancy permit; file permit in DEL-32.02 and DEL-32.06
- Log all inspections in DEL-32.07; file all records in DEL-32.08
