# CBS Taxonomy -- Cost Breakdown Structure for ESTIMATING Agents

## Purpose

This document defines the canonical Cost Breakdown Structure (CBS) taxonomy for project AB-2026-01424 (WDMLRL Maintenance Shop Addition). All ESTIMATING agents MUST assign CBS codes from this taxonomy to every line item they produce.

## Problem Statement

During the initial estimation pipeline, 117 deliverable estimates were produced by independent ESTIMATING agents. Each agent independently chose CBS labels, resulting in 292 unique CBS values where approximately 30 canonical categories were intended. The same cost type appeared under many different labels (e.g., PM hours coded as "Management", "LABOUR-MGMT", "Professional Services -- Management", "MGMT-PM", etc.). This taxonomy was developed by analyzing all 292 original codes and mapping them to a unified two-level hierarchy.

## Taxonomy Structure

The CBS uses a two-level hierarchy:

- **CBS_L1** (19 categories): Broad cost type groupings
- **CBS_L2** (29 categories): Meaningful sub-categories within each L1

### L1 > L2 Hierarchy

```
Professional Services
    Design & Engineering              (CBS-01)
    Project Management                (CBS-02)
    Professional Staff                (CBS-03)
    Specialty Consulting              (CBS-04)

Construction Labour
    General Construction Labour       (CBS-05)
    Electrical Labour                 (CBS-06)
    Plumbing Labour                   (CBS-07)

Concrete
    Concrete & Foundations            (CBS-08)

Structural Steel & Metals
    Structural Steel & Fabrication    (CBS-09)

Building Envelope
    Cladding, Insulation & Waterproofing  (CBS-10)

Openings
    Doors, Windows & Glazing          (CBS-11)

Interior Construction
    Partitions, Finishes & Fit-Out    (CBS-12)

Mechanical
    HVAC Equipment & Distribution     (CBS-13)
    Controls & Commissioning          (CBS-14)
    Administration & Permits          (CBS-15)

Plumbing
    Plumbing Systems                  (CBS-16)

Electrical
    Power Distribution & Equipment    (CBS-17)
    Low Voltage & Communications      (CBS-18)
    Commissioning & Administration    (CBS-19)

Equipment
    Process & Facility Equipment      (CBS-20)

Materials
    General Materials & Supplies      (CBS-21)

Sitework & Civil
    Earthwork, Surfacing & Landscaping    (CBS-22)
    Underground Utilities & Site Services  (CBS-23)

Utilities
    Utility Connections               (CBS-24)

Commissioning & Testing
    Commissioning, Testing & Inspection   (CBS-25)

Quality, Safety & Environment
    HSE & Quality Assurance           (CBS-26)

Survey & Investigation
    Survey & Field Investigation      (CBS-27)

Permits, Fees & Insurance
    Permits, Fees & Bonding           (CBS-28)

General Conditions
    General Requirements & Indirect   (CBS-29)
```

## Usage Instructions for ESTIMATING Agents

1. **Every line item MUST have a CBS value.** Use the CBS_L2 value exactly as listed above (e.g., "Design & Engineering", not "Design" or "DESIGN").

2. **Choose the most specific applicable CBS_L2.** For example:
   - Architectural design labour: use "Design & Engineering" (CBS-01), not "Project Management" (CBS-02)
   - A PM's hours: use "Project Management" (CBS-02)
   - Professional staff allocation spanning PM + QA/QC + HSE: use "Professional Staff" (CBS-03)
   - Electrician labour installing conduit: use "Electrical Labour" (CBS-06)
   - Concrete foundation pour: use "Concrete & Foundations" (CBS-08)

3. **For mixed material+labour items**, use the CBS category that matches the dominant cost type. If truly inseparable, use "General Materials & Supplies" (CBS-21).

4. **For $0 scope-tracking items** (embedded effort, coordination items), use the CBS of the parent activity (e.g., design QA embedded in architect hours uses "Design & Engineering").

5. **Do NOT invent new CBS codes.** If a cost type does not clearly fit, use the closest match and note the ambiguity in the line item Notes field.

## Reference Data

The machine-readable taxonomy is in `CBS_Taxonomy.csv` (same directory). Schema:

| Column | Description |
|---|---|
| CBS_Code | Unique identifier (CBS-01 through CBS-29) |
| CBS_L1 | Level 1 category name |
| CBS_L2 | Level 2 sub-category name (use this as the CBS value) |
| Description | Detailed description of what belongs in this category |
| Examples | Example original CBS codes that map to this category |
| ApplicablePackages | WBS packages where this CBS category appeared in the initial estimate |

## Distribution by Category (Initial Estimate)

| CBS | Category | Amount (CAD) | % of Total |
|---|---|---:|---:|
| CBS-08 | Concrete & Foundations | 1,962,647 | 27.1% |
| CBS-01 | Design & Engineering | 809,875 | 11.2% |
| CBS-10 | Cladding, Insulation & Waterproofing | 673,906 | 9.3% |
| CBS-05 | General Construction Labour | 548,767 | 7.6% |
| CBS-20 | Process & Facility Equipment | 489,930 | 6.8% |
| CBS-09 | Structural Steel & Fabrication | 375,797 | 5.2% |
| CBS-02 | Project Management | 363,631 | 5.0% |
| CBS-21 | General Materials & Supplies | 312,050 | 4.3% |
| CBS-22 | Earthwork, Surfacing & Landscaping | 300,542 | 4.2% |
| CBS-13 | HVAC Equipment & Distribution | 229,350 | 3.2% |
| CBS-29 | General Requirements & Indirect | 191,884 | 2.7% |
| CBS-11 | Doors, Windows & Glazing | 182,040 | 2.5% |
| CBS-17 | Power Distribution & Equipment | 98,875 | 1.4% |
| CBS-16 | Plumbing Systems | 88,110 | 1.2% |
| CBS-25 | Commissioning, Testing & Inspection | 86,749 | 1.2% |
| CBS-03 | Professional Staff | 83,030 | 1.1% |
| CBS-24 | Utility Connections | 78,000 | 1.1% |
| CBS-28 | Permits, Fees & Bonding | 68,050 | 0.9% |
| CBS-23 | Underground Utilities & Site Services | 61,020 | 0.8% |
| CBS-26 | HSE & Quality Assurance | 42,765 | 0.6% |
| CBS-12 | Partitions, Finishes & Fit-Out | 40,574 | 0.6% |
| CBS-27 | Survey & Field Investigation | 34,560 | 0.5% |
| CBS-14 | Controls & Commissioning | 29,500 | 0.4% |
| CBS-04 | Specialty Consulting | 24,740 | 0.3% |
| CBS-06 | Electrical Labour | 19,930 | 0.3% |
| CBS-15 | Administration & Permits (Mech.) | 11,900 | 0.2% |
| CBS-07 | Plumbing Labour | 11,693 | 0.2% |
| CBS-18 | Low Voltage & Communications | 9,835 | 0.1% |
| CBS-19 | Commissioning & Admin (Elec.) | 8,760 | 0.1% |
| | **TOTAL** | **7,238,510** | **100.0%** |

## Version History

| Date | Author | Change |
|---|---|---|
| 2026-02-28 | CBS Normalization (aggregation post-processing) | Initial taxonomy created from analysis of 292 original CBS codes across 1,632 line items |
