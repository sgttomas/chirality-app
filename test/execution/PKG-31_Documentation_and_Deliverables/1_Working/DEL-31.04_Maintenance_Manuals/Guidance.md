# Guidance: DEL-31.04 Maintenance Manuals

## Purpose

Provides comprehensive, user-friendly guidance for maintaining facility equipment and systems, supporting safe and reliable operations (OBJ-1) and lifecycle cost optimization (OBJ-9).

**Source:** Decomposition DEL-31.04 (line 689); OBJ-1 (line 59), OBJ-9 (line 67)

## Principles

### Principle 1: Comprehensive Equipment Coverage
Maintenance Manuals must cover all equipment requiring maintenance — no gaps.

### Principle 2: Accuracy and Field Validation
Manuals must reflect as-built configurations and validated maintenance procedures.

### Principle 3: Maintenance Personnel-Centered Design
Write for maintenance technicians: clear language, step-by-step procedures, visual aids, safety emphasis.

### Principle 4: Safety First
Lockout/tagout, hazard identification, and safety precautions must be prominent. Maintenance activities often involve higher risk than operations.

### Principle 5: Lifecycle Maintenance Strategy
Blend preventive, predictive, and condition-based maintenance strategies based on equipment criticality and reliability data.

### Principle 6: Spare Parts Management
Accurate spare parts lists enable efficient maintenance and reduce downtime.

## Considerations

### As-Built Baseline
Use As-Built Drawings (DEL-31.02) for equipment configurations and locations.

### Vendor Documentation Integration
Leverage vendor manuals (DEL-31.05) for equipment-specific maintenance procedures; adapt and contextualize for facility use.

### Operations vs. Maintenance Scope
Clear delineation: Routine operator tasks (daily checks, basic troubleshooting) in Operation Manuals (DEL-31.03); maintenance activities (PM, repairs, overhauls) in Maintenance Manuals (DEL-31.04).

### Preventive Maintenance Scheduling
- Base PM schedules on vendor recommendations, industry standards, and equipment criticality
- Consider operating hours, calendar time, and condition triggers
- Align with facility operational schedule to minimize disruption

### Spare Parts Strategy
- Critical spares (long lead time, single source, high consequence of failure)
- Recommended spares (vendor recommended, moderate lead time)
- Consumables (routine replacement items)
- Standardization opportunities across equipment types

### Warranty Compliance
Ensure maintenance procedures comply with equipment warranty requirements (DEL-31.08, DEL-31.09) to avoid warranty voidance.

### Asset Tagging and CMMS Integration
Equipment tags and nomenclature consistent with Asset Hierarchy (DEL-31.06) to enable seamless Computerized Maintenance Management System (CMMS) integration.

### Lockout/Tagout and Permit-to-Work
Integrate facility lockout/tagout and permit-to-work procedures into maintenance procedures.

### Environmental and Regulatory Compliance
Include environmental compliance requirements (e.g., refrigerant handling, oil spill prevention, waste disposal) in maintenance procedures.

## Trade-offs

### PM Frequency vs. Cost
More frequent PM increases cost but may improve reliability. Optimize based on equipment criticality and reliability data over time.

### Equipment-Specific vs. Standardized Procedures
Equipment-specific procedures are more accurate but require more documentation effort. Standardize where possible (e.g., "pump maintenance general procedure") with equipment-specific supplements.

### Development Timing
Concurrent development (during design/construction) vs. post-commissioning. Concurrent enables readiness; post-commissioning enables field validation.

## Examples

**PM Procedure Example:**
"Pump P-101A Monthly Preventive Maintenance:
1. Lockout/tagout pump per LOTO-PM-001.
2. Inspect pump for leaks, vibration, noise.
3. Check bearing temperatures and lubrication levels.
4. Tighten packing gland if leaking.
5. Record observations in CMMS.
6. Remove lockout/tagout and return to service."

**Spare Parts List Example:**
| Part Number | Description | Qty | Lead Time | Criticality |
|-------------|-------------|-----|-----------|-------------|
| P101-SP-001 | Mechanical Seal | 1 | 8 weeks | Critical |
| P101-SP-002 | Bearing Set | 1 | 4 weeks | Recommended |

**Source:** _CONTEXT.md; Decomposition line 689
