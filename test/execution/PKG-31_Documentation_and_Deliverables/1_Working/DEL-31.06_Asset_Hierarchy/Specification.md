# Specification: DEL-31.06 Asset Hierarchy

## Scope

Defines requirements for **Asset Hierarchy** within **PKG-31 Documentation & Deliverables**.

**Purpose:** Provides structured asset information for operations, maintenance, and lifecycle asset management per Employer's Requirements.

**Source:** Decomposition DEL-31.06 (line 692)

**Anticipated artifacts:** Asset hierarchy database/document

## Requirements

### Functional Requirements

**FR-01: Completeness** — Asset Hierarchy shall include all facility assets (equipment, systems, structures, buildings).

**FR-02: Hierarchical Structure** — Assets organized hierarchically (Facility → Systems → Subsystems → Equipment → Components).

**FR-03: Unique Asset Tagging** — Each asset assigned unique tag; tags aligned with As-Built Drawings (DEL-31.02).

**FR-04: Asset Attributes** — Asset attributes include: tag, description, parent, location, type, criticality, manufacturer, model, installation date, warranty expiration.

**FR-05: CMMS Compatibility** — Asset Hierarchy format compatible with CMMS data loading requirements.

### Performance Requirements

**PR-01: Data Accuracy** — Asset data accurate and reflects as-built facility configuration.

**PR-02: Format and Standards** — Asset tagging standard applied consistently; format per Employer's Requirements or industry standards.

### Interface Requirements

**IR-01: As-Built Drawings Interface** — Asset tags aligned with DEL-31.02.

**IR-02: O&M Manuals Interface** — Asset tags consistent across DEL-31.03 and DEL-31.04.

**IR-03: Vendor Documentation Interface** — Manufacturer/model information from DEL-31.05.

**IR-04: Warranty Interface** — Warranty expiration cross-referenced to DEL-31.08.

**IR-05: CMMS Interface** — Asset Hierarchy data loadable into Employer's CMMS.

### Quality Requirements

**QR-01: Data Quality** — Asset data complete, accurate, and validated.

**QR-02: Version Control** — Asset Hierarchy under version control; updates managed.

### Lifecycle Requirements

**LR-01: Lifecycle Cost Optimization** — Asset Hierarchy supports OBJ-9 by enabling effective asset management, risk-based maintenance, and lifecycle tracking.
- **Source:** OBJ-9 (line 67, line 788)

## Standards

- ISO 55000 (Asset Management) — **ASSUMPTION** if applicable
- ISO 14224 (Equipment Reliability Data) — **ASSUMPTION** if applicable
- Employer's Requirements — **TBD**

## Verification

1. **Completeness Review** — All assets included
2. **Data Quality Review** — Attributes accurate and complete
3. **Tagging Consistency Check** — Tags aligned with As-Built Drawings
4. **CMMS Compatibility Check** — Format compatible with CMMS

**Acceptance Criteria:** All assets included; data accurate; CMMS-compatible; Employer acceptance obtained

## Documentation

**Outputs:**
1. Asset Hierarchy Database (Excel, CMMS format, or per Employer's requirements)
2. Asset Hierarchy Document/Report (PDF summary)
3. Asset Tagging Standard Document

**Filing:** `3_Issued/`
