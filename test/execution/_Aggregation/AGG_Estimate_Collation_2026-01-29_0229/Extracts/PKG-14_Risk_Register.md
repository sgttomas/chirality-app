# Risk Register

## PKG-14 Process Piping Estimate

| ID | Risk Driver | Cause → Consequence | Affected CBS/WBS | Suggested Mitigation | Contingency Handling |
|----|-------------|---------------------|------------------|---------------------|---------------------|
| R-001 | Scope - Piping Quantities | No P&IDs or routing → Quantities may vary ±30% from estimates | MAT, CD / PKG-14 | Complete DEL-14.01 P&IDs and piping GAs | 25-30% contingency on piping items |
| R-002 | Scope - Header Sizing | No hydraulic calculations → Header sizes may change affecting costs | MAT / PKG-14 | Complete DEL-14.03 pipe sizing calculations | MAT contingency |
| R-003 | Technical - Transient Analysis | Surge analysis not complete → May require surge protection equipment | MAT, E / PKG-14 | Complete DEL-14.06, DEL-14.07 transient studies early | Engineering contingency; potential MAT adds |
| R-004 | Technical - Stress Analysis | Flexibility analysis not complete → Support quantities uncertain | MAT, CD / PKG-14 | Complete DEL-14.03 stress analysis | Support contingency |
| R-005 | Price - No Quotes | No vendor quotes for any items → All pricing via allowances | All CBS | Obtain budgetary quotes for large diameter pipe | Elevated contingency on all buckets |
| R-006 | Interface - PKG-10 | Rail unloading header interface → 32 connection points with tight tolerances | CD interface | Coordinate header routing with PKG-10 unloading arm positions | Interface alignment premium |
| R-007 | Interface - PKG-11 | Export pipe to marine loading → Single-wall to double-wall transition | CD interface | Define interface location and transition detail early | Transition piece costs |
| R-008 | Interface - PKG-13 | Tank nozzle connections → Nozzle schedule undefined | CD interface | Coordinate with PKG-13 for nozzle schedule and elevations | Spool piece fabrication |
| R-009 | Interface - PKG-15 | Pump piping interfaces → Pump selection affects suction/discharge requirements | MAT, CD interface | Coordinate with PKG-15 for pump nozzle data | Piping modifications |
| R-010 | Fabrication - Welder Availability | Coded welders required → May be labor constraint in BC market | CD / PKG-14 | Pre-qualify welding contractors; confirm welder availability | Labor contingency in CD |
| R-011 | Quality - NDE Rework | High NDE requirements on headers → Weld repair cycle risk | CD / PKG-14 | Weld procedure qualification; pre-production welds | 30% contingency on CD |
| R-012 | Schedule - Long Lead | Large diameter pipe procurement lead time | MAT / PKG-14 | Early material ordering; coordinate with DEL-14.04 line list | Schedule risk (not costed) |
| R-013 | Technical - Insulation Scope | Heat tracing requirements → May vary with process design | MAT, CD / PKG-14 | Confirm insulation/heat trace requirements in DEL-14.02 | Insulation contingency |
| R-014 | Scope - Phase 2 Provisions | Phase 2 connections → Stub-out quantity and complexity undefined | MAT, CD, E | Define Phase 2 interface requirements per OBJ-8 | Design contingency |
| R-015 | Commissioning - Flushing | Piping flushing requirements → May require extensive chemical cleaning | COM / PKG-14 | Define commissioning requirements in DEL-14.05 | 30% contingency on COM |
| R-016 | Environmental - Material Storage | Large pipe material on site → Laydown area and protection needs | CI / PKG-14 | Plan material staging and protection | CI factor |
| R-017 | Technical - Expansion Provisions | Thermal expansion requirements → Expansion loops/joints TBD | MAT / PKG-14 | Complete stress analysis DEL-14.03 early | Expansion joint allowance |

## Contingency Summary

| CBS | Base Amount | Contingency % | Contingency $ | Rationale |
|-----|-------------|---------------|---------------|-----------|
| E | $515,000 | 20% | $103,000 | All allowances; transient studies complexity; scope definition risk |
| MAT | $2,125,000 | 25% | $531,000 | All allowances; large quantity uncertainty; material pricing |
| CD | $1,975,000 | 30% | $593,000 | Piping fabrication/welding complexity; NDE rework potential; interface coordination |
| CI | $359,000 | 30% | $108,000 | Factor-based from CD; coordination complexity |
| PM | $298,000 | 15% | $45,000 | Factor-based |
| P | $42,000 | 15% | $6,000 | Factor-based |
| COM | $136,000 | 30% | $41,000 | Flushing/cleaning requirements; multi-system commissioning |
| **TOTAL** | **$5,450,000** | **26.2%** | **$1,427,000** | Weighted average |

## Contingency Method

**Method:** PCT_BY_BUCKET with allowance adjustment per fallback typical model

**Basis:**
- All line items are allowances (100% allowance-based estimate)
- Per fallback model: +10% above baseline contingency for buckets with ≥80% allowance share
- Piping package is scope-sensitive: quantities derive from P&IDs that don't yet exist
- Multiple interface packages create coordination risk
- Transient analysis outcomes may affect equipment requirements
- Applied across all CBS buckets due to LOW confidence level
