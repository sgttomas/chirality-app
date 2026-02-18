# Datasheet: DEL-02-01 Concept Design Package

## Identification

| Property | Value |
|----------|-------|
| **Deliverable ID** | DEL-02-01 |
| **Deliverable Name** | ConceptDesignPackage |
| **Package** | PKG-04 Design Proposal (Concept + Design Brief) |
| **Discipline** | Architecture / Design |
| **Type** | Design Package |
| **Responsible Party** | Lead Architect / Designer |
| **Status** | INITIALIZED |
| **Version** | Draft v1.2 (Pass 3 — Final) |

**Source:** _CONTEXT.md

---

## Attributes

### Building Program Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| **Building Type** | Integrated Fire Hall + Public Works Facility | Decomposition §1 (Intake Summary) |
| **Owner** | Town of Penhold | Decomposition §1 |
| **Functional Program** | Multi-room program with flexible dimensions | Decomposition §4 (Addendum 01 clarification) |
| **Primary Occupancies** | Fire Hall (Group A, Division 2 assembly / Group F, Division 1 industrial); Public Works (Group D, Division 3 business / Group F, Division 2 industrial) | ASSUMPTION: Based on Alberta Building Code occupancy classifications for fire stations and municipal works facilities. **[A-002 Action Required]** Confirm from RFP Appendix A or Code Consultant analysis; document rationale if assumption-based. Classification affects egress, fire separation, and structural requirements. |
| **Program Flexibility** | Room dimensions intentionally omitted to allow innovation; spaces must meet building code minimum | Decomposition §4, Addendum 01 |
| **Sample Room Sizing Ranges** | Provided in Addendum 03 for selected spaces | Decomposition §4, Addendum 03 (location TBD: requires PDF access) |

### Room Dimension Baseline Table

**[B-001 Enrichment]** Room-by-room dimension table for cost estimation and design consistency.

| Room Name | Approx Dimensions (W x D) | Source | Notes |
|-----------|---------------------------|--------|-------|
| Apparatus Bay 1 | ~14 ft x 60 ft | ASSUMPTION (code min + operational) | Verify against Appendix B Functional Program |
| Apparatus Bay 2 | ~14 ft x 60 ft | ASSUMPTION (code min + operational) | Verify against Appendix B Functional Program |
| Apparatus Bay 3 | TBD | Appendix B (requires PDF access) | Number of bays TBD |
| Fire Hall Day Room | TBD | Addendum 03 sample range (if provided) | Check Addendum 03 for sample range |
| Fire Hall Kitchen | TBD | Addendum 03 sample range (if provided) | Check Addendum 03 for sample range |
| Meeting Room / ICP | TBD | Addendum 03 sample range (if provided) | Must accommodate ICP function per Addendum 03 |
| Fire Chief Office | TBD | Code minimum / Addendum 03 | Verify against Appendix B |
| Turnout Gear Storage | TBD | Operational requirement | Adjacent to apparatus bays |
| Public Works Vehicle Bay | TBD | Appendix B / Operational | Size based on largest equipment |
| Public Works Workshop | TBD | Appendix B | Verify against Functional Program |
| Public Works Staff Office | TBD | Code minimum | Verify against Appendix B |
| Mechanical Room | TBD | Code minimum | Size based on system requirements |
| Electrical Room | TBD | Code minimum | Size based on system requirements |

**Source:** _SEMANTIC_LENSING.md Item B-001 (Matrix B: data:necessity). Without unified room dimension baseline, documents may reference different room sizes, affecting cost estimation (PKG-02) and design consistency.

### Site Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| **Total Site Area** | 20 acres | Decomposition §4, Addendum 03 |
| **Developable Area** | 12 acres | Decomposition §4, Addendum 03 |
| **Flood Fringe Area** | 8 acres (designated for dog park and storm pond) | Decomposition §4, Addendum 03 |
| **Site Context** | Adjacent to subdivision development | _REFERENCES.md (Adjacent Subdivision Design reference) |
| **Site Services** | Municipal services available; allowance approach for tie-ins permitted | Decomposition §9 (SOW-024 notes) |
| **Survey Files** | Provided after contract award | Decomposition §4, Addendum 03 |

### Technical Requirements (from Addendum 03)

| Requirement | Specification | Source |
|-------------|---------------|--------|
| **Overhead Door Height** | 16 ft minimum | Decomposition §4, Addendum 03 |
| **Bay Sumps** | Required in apparatus bays | Decomposition §4, Addendum 03 |
| **Fire Apparatus Exhaust** | Exhaust capture system required | Decomposition §4, Addendum 03 |
| **Generator** | Required; must support Incident Command Post (ICP) | Decomposition §4, Addendum 03; §5 (Vocabulary: ICP) |
| **Fill Stations** | Required (fuel/fluids for apparatus and public works equipment) | Decomposition §4, Addendum 03 |
| **Solar Readiness** | Solar capable roof design and orientation | Decomposition §4, Addendum 03 |

### Excluded Scope

| Exclusion | Rationale | Source |
|-----------|-----------|--------|
| **Pickled Sand Storage Building** | Removed from RFP scope; to be issued as separate RFP | Decomposition §4, Addendum 03 |

---

## Conditions

### Design Context Conditions

| Condition | Description | Source |
|-----------|-------------|--------|
| **RFP Response Context** | This concept design is for proposal evaluation, not construction | Decomposition §1 (Primary response objective) |
| **Evaluation Weight** | 20 points (Proposed Conceptual Design category) | Decomposition §15 (Evaluation Criteria Crosswalk) |
| **Compliance Requirement** | Must demonstrate program fit and exclude removed scope | _CONTEXT.md (Acceptance Criteria) |
| **Submission Format** | Included in single PDF proposal (≤15 MB) | Decomposition §3 (C-01) |

### Site Conditions

| Condition | Description | Source |
|-----------|-------------|--------|
| **Geotechnical Considerations** | Foundation design implications documented in Geotechnical Investigation Report | _REFERENCES.md; location TBD (requires PDF access) |
| **Wetland Constraints** | Environmental considerations documented in Wetland Assessment | _REFERENCES.md; location TBD (requires PDF access) |
| **Flood Zone** | 8-acre flood fringe area constrains developable footprint | Decomposition §4, Addendum 03 |
| **Site Grading** | Existing grading data available | _REFERENCES.md; location TBD (requires PDF access) |
| **Town Setbacks** | **[A-003 BLOCKING CONFLICT]** Required setbacks from property lines TBD. If Town setbacks reduce developable area below 12 acres, building cannot meet both Specification R2 (12-acre constraint) and setback requirements. **Action Required:** Obtain Town setback requirements from bylaws immediately. If conflict exists, escalate to Proposal Manager for variance request or scope revision. | Source: _SEMANTIC_LENSING.md Item A-003 (Matrix A: normative:applying). Impacted sections: Specification R2, Procedure Step 2.2, Datasheet §Conditions. |

### Environmental Conditions

| Condition | Value/Description | Source |
|-----------|-------------------|--------|
| **Climate Zone** | Central Alberta (assumed climate zone 7A per NBC) | ASSUMPTION: Based on Penhold, Alberta geographic location |
| **Energy Performance** | Energy efficiency and sustainability approach required in proposal | Decomposition §9 (SOW-012) |
| **Solar Orientation** | Roof design must accommodate solar-ready provisions | Decomposition §4, Addendum 03 |

---

## Construction

### Structural Considerations

| Element | Consideration | Source |
|---------|---------------|--------|
| **Foundation** | Design must account for geotechnical conditions | _REFERENCES.md (Geotechnical Investigation Report); details TBD |
| **Apparatus Bay Structure** | Must accommodate 16 ft overhead door clear height plus structure | Decomposition §4, Addendum 03 |
| **Roof Structure** | Must be solar-ready (orientation and structural capacity) | Decomposition §4, Addendum 03 |
| **Building Massing** | Concept to show massing and key sections/elevations | _CONTEXT.md (Anticipated Artifacts) |

### Systems Integration

| System | Integration Requirement | Source |
|--------|------------------------|--------|
| **Fire Apparatus Exhaust** | Integrated exhaust capture in apparatus bays | Decomposition §4, Addendum 03 |
| **Bay Sumps** | Floor drainage systems in apparatus bays | Decomposition §4, Addendum 03 |
| **Emergency Generator** | Sized to support ICP and critical systems. **[B-002 Enrichment]** Capacity estimate: ~100 kW (TBD pending load analysis). Preliminary scope: ICP meeting room (HVAC, lighting, equipment), critical MEP systems (chilled water, emergency lighting, fire protection), apparatus bay exhaust system. | Decomposition §4, Addendum 03; §5 (ICP definition). Generator capacity is essential fact for cost estimation, footprint planning, fuel capacity, and electrical distribution design. Source: _SEMANTIC_LENSING.md Item B-002. |
| **Fill Stations** | Fuel/fluid dispensing for vehicles and equipment | Decomposition §4, Addendum 03 |

### Materials Strategy

**Status:** TBD (to be developed in Design Brief narrative per SOW-011, SOW-013)

**Note:** Durability and ease of maintenance materials approach will be detailed in DEL-02-02 (Design Brief Narrative), which addresses evaluation criteria worth 15 points.

**Source:** Decomposition §15 (Evaluation Criteria); §9 (SOW-011, SOW-013)

---

## References

### Primary Source Documents

1. **Decomposition Document**
   Path: /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md
   Relevance: Project scope, constraints, requirements integration

2. **_CONTEXT.md**
   Path: (deliverable folder)
   Relevance: Deliverable identity, acceptance criteria, scope traceability

3. **_REFERENCES.md**
   Path: (deliverable folder)
   Relevance: Reference material inventory

### Referenced Source Materials (Access Required)

The following materials are listed in `_REFERENCES.md` but require PDF access for detailed extraction:

1. **RFP:** AB-2024-07156-Penhold Public Services Building RFP_2024_004.pdf
   Location: _Sources/
   Relevance: OSR (Appendix A), Functional Program (Appendix B), Section 7.1 design requirements
   **Status:** Location TBD (PDF access not available in current session)

2. **Addendum 01:** AB-2024-07156-Penhold_Public Services Building Addendum01.pdf
   Location: _Sources/
   Relevance: Room dimension flexibility clarification
   **Status:** Location TBD (PDF access not available in current session)

3. **Addendum 03:** AB-2024-07156-Penhold_Public Services Building Addendum03.pdf
   Location: _Sources/
   Relevance: 12-acre site, pickled sand removal, technical clarifications
   **Status:** Location TBD (PDF access not available in current session)

4. **Site Grading:** AB-2024-07156-Penhold PSB_Site grading.pdf
   Location: _Sources/
   Relevance: Site layout and grading context
   **Status:** Location TBD (PDF access not available in current session)

5. **Adjacent Subdivision:** AB-2024-07156-Penhold PSB_Adjacent Subdivision Design.pdf
   Location: _Sources/
   Relevance: Adjacent development context
   **Status:** Location TBD (PDF access not available in current session)

6. **Flood Zone:** AB-2024-07156-Penhold PSB_parcel flood zone.pdf
   Location: _Sources/
   Relevance: Flood fringe constraints
   **Status:** Location TBD (PDF access not available in current session)

7. **Geotechnical:** AB-2024-07156-Penhold PSB_Geotechnical Investigation Report.pdf
   Location: _Sources/
   Relevance: Foundation design implications
   **Status:** Location TBD (PDF access not available in current session)

8. **Wetland Assessment:** AB-2024-07156-Penhold PSB_Wetland Assessment.pdf
   Location: _Sources/
   Relevance: Site constraints and environmental considerations
   **Status:** Location TBD (PDF access not available in current session)

### Standards and Codes (Inferred)

The following are ASSUMPTIONS based on deliverable discipline and type:

- **Alberta Building Code 2019** (likely applicable for Alberta municipal building)
- **National Building Code of Canada** (foundation for Alberta Building Code)
- **National Fire Code of Canada** (applicable to Fire Hall occupancy)
- **Town of Penhold Municipal Bylaws** (local requirements)
- **CSA Standards** (various, as applicable to building systems and accessibility)

**Note:** Specific standard clauses and requirements marked TBD pending access to full RFP appendices and applicable code references.

---

## Document Control

| Property | Value |
|----------|-------|
| **Created** | 2026-02-04 |
| **Author** | 4_DOCUMENTS Agent (Type 2 Specialist) |
| **Pass** | Pass 3 (Semantic Lensing + Final Reconcile) |
| **Next Action** | Ready for WORKING_ITEMS sessions |
| **Pass 2 Summary** | Cross-reference checks completed. Entity-to-requirement mappings verified. Terminology standardized. No unresolvable conflicts identified. |
| **Pass 3 Summary** | Semantic lensing enrichment complete. Incorporated items: A-002 (occupancy classification action), B-001 (room dimension table), B-002 (generator capacity estimate), A-003 (blocking conflict: Town setbacks). 4 warranted items incorporated from _SEMANTIC_LENSING.md. Cross-reference consistency sweep completed. |

---

**END OF DATASHEET**
