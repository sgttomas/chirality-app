# Datasheet: DEL-08.07 Fender System Deflection Characteristics Data Package

## Identification

| Field | Value |
|---|---|
| Deliverable ID | DEL-08.07 |
| Name | Fender System Deflection Characteristics Data Package |
| Package | PKG-08 Marine Structures |
| Discipline | Marine |
| Type | Document Package |
| Responsible | D&B Contractor |
| Lifecycle State | INITIALIZED |

## Description

**Purpose (source-anchored):** Defines and substantiates fender system deflection characteristics data package in accordance with ER requirements. *(Source: Decomposition line 287 + `_CONTEXT.md`)*

**Deliverable objective:** Provides technical characteristics of selected fender system, demonstrating it can absorb design berthing energy (from DEL-08.06) while generating acceptable reaction forces on marine structure.

## Minimum Artifact Content

*(Source: Decomposition line 287)*

| Artifact | Description | Status |
|---|---|---|
| Fender deflection curves | Energy-deflection and reaction-deflection performance curves | Required |
| Manufacturer data | OEM technical datasheets, dimensions, material specs | Required |
| Compliance certificates | Test certificates, material certificates, quality conformance | Required |

## Package Metadata (TBD)

| Attribute | Value |
|---|---|
| Package number | **TBD** *(e.g., PKG-MAR-08-001)* |
| Fender type/model | **TBD** *(rubber cell / cone / foam-filled / arch / other)* |
| Manufacturer/supplier | **TBD** |
| Number of fenders | **TBD** *(from DEL-08.01 arrangement)* |
| Test standard basis | **ASSUMPTION:** PIANC or manufacturer standard *(confirm from ER)* |

## Fender Performance Data (TBD)

| Parameter | Description | Status |
|---|---|---|
| Rated energy absorption (E) | Energy at rated deflection | **TBD** kN·m *(must ≥ design energy from DEL-08.06)* |
| Rated reaction force (R) | Maximum reaction at rated deflection | **TBD** kN *(input to DEL-08.03 structural design)* |
| Rated deflection | Deflection at rated performance | **TBD** % or mm |
| Performance curve basis | Temperature and velocity reference conditions | **TBD** *(typically 23°C, standard velocity)* |
| Hull pressure | Maximum contact pressure on vessel | **TBD** kPa *(typically < 500 kPa to avoid hull damage)* |
| Fender dimensions | Height, width, projection | **TBD** mm *(from OEM datasheet)* |
| Fender weight | Unit weight | **TBD** kg *(for handling and structural loading)* |

## Performance Curve Adjustment Factors (ASSUMPTION)

*ASSUMPTION based on PIANC/BS 6349-4 guidance (confirm from ER and OEM data):*

| Factor | Description | Typical Range | Application |
|---|---|---|---|
| Temperature (Ct) | Rubber stiffness vs temperature | 0.85–1.10 | Low temp → higher reaction; high temp → lower reaction |
| Velocity (Cv) | Dynamic stiffening | 1.0–1.15 | High velocity → higher reaction |
| Angle (Ca) | Angular berthing effect | 0.9–1.0 | Reduced contact area |
| Manufacturing tolerance | Performance variation | ±10% typical | Design margin for variability |

*Confirm applicable factors from ER, standards, and supplier recommendations.*

## Interfaces (Advisory)

*Dependencies NOT_TRACKED; interfaces for context:*

| Related Deliverable | Interface |
|---|---|
| DEL-08.06 Berthing Energy Calculation | Input: design energy → fender selection |
| DEL-08.08 Fender Supplier Verification | Output: performance data → supplier verification |
| DEL-08.03 Marine Structures Calculations | Output: reaction forces → structural design |
| DEL-08.01 Marine Structures Drawings | Output: dimensions/arrangement |
| PKG-09 Marine Outfitting | Fender installation (mounting, hardware) |

## Cross-Document Links

- **Requirements:** `Specification.md` R-001 through R-006
- **Guidance:** `Guidance.md` (performance curve interpretation, checklist)
- **Workflow:** `Procedure.md` (compilation steps)

## Key TBDs

1. ER clauses for fender data package requirements
2. Fender type/model selected
3. OEM performance curves and certificates
4. Performance adjustment factors per ER/standards

## Sources

- Decomposition line 287
- ER Vol 2 Parts 1-2 *(TBD)*
