# Guidance: DEL-31.06 Asset Hierarchy

## Purpose

Provides structured asset information enabling effective operations, maintenance, and lifecycle asset management (OBJ-9).

**Source:** Decomposition DEL-31.06 (line 692); OBJ-9 (line 67, line 788)

## Principles

### Principle 1: Hierarchical Organization
Assets organized hierarchically to reflect physical and functional relationships.

### Principle 2: Unique Asset Identification
Each asset has unique tag enabling unambiguous identification across all documentation and systems.

### Principle 3: Consistency Across Documentation
Asset tags consistent across drawings (DEL-31.02), manuals (DEL-31.03, DEL-31.04), vendor documentation (DEL-31.05), warranties (DEL-31.08).

### Principle 4: CMMS Foundation
Asset Hierarchy is foundation for CMMS implementation—structure and data quality are critical.

### Principle 5: Criticality-Based Management
Asset criticality classification enables risk-based maintenance and resource prioritization.

## Considerations

### Asset Tagging Standard
Develop and apply consistent asset tagging standard (e.g., system-based tags, sequential numbering, intelligent vs. non-intelligent tags). Coordinate with Employer's existing standards if applicable.

### Hierarchical Depth
Balance detail (more levels, granular) vs. simplicity (fewer levels, manageable). Typical: Facility → Systems → Equipment; add Subsystems and Components only where beneficial.

### Asset Criticality Classification
Classify assets by criticality (critical, important, routine) based on consequence of failure. Supports risk-based maintenance prioritization.

### CMMS Integration
Coordinate with Employer's CMMS requirements early. Understand data format, required fields, import procedures.

### As-Built Baseline
Use As-Built Drawings (DEL-31.02) as baseline for asset identification and tagging.

### Lifecycle Updates
Asset Hierarchy is living document—establish process for updates (new assets, retirements, modifications).

## Trade-offs

### Intelligent vs. Non-Intelligent Asset Tags
Intelligent tags (encode information, e.g., P-101 = Pump in System 1, Item 01) vs. non-intelligent tags (sequential, e.g., ASSET-001). Intelligent tags are more descriptive but harder to manage long-term.

### Detail vs. Simplicity
More detailed hierarchy (many levels, many assets) provides granular data but increases management complexity. Balance based on facility complexity and Employer's needs.

## Examples

**Asset Hierarchy Example:**
- Level 1: COTF-PHASE1 (Facility)
  - Level 2: RCU-SYSTEM (Railcar Unloading System)
    - Level 3: RCU-PUMP-SYSTEM (Unloading Pump Subsystem)
      - Level 4: P-101A (Unloading Pump A)
      - Level 4: P-101B (Unloading Pump B)
    - Level 3: RCU-ARM-SYSTEM (Unloading Arm Subsystem)
      - Level 4: UA-01 through UA-32 (Unloading Arms)

**Asset Attributes Example:**
| Asset Tag | Description | Parent | Location | Criticality | Manufacturer | Model | Install Date | Warranty Exp |
|-----------|-------------|--------|----------|-------------|--------------|-------|--------------|--------------|
| P-101A | Unloading Pump A | RCU-PUMP-SYSTEM | Pump House | Critical | XYZ Pumps | Model 500 | 2026-06-01 | 2028-06-01 |

**Source:** _CONTEXT.md; Decomposition line 692
