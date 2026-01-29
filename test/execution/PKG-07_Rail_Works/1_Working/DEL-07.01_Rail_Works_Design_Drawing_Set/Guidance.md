# Guidance: DEL-07.01 Rail Works Design Drawing Set

**Enrichment Status:** Pass 3 Complete (3-pass enrichment: Initial draft, Cross-reference enrichment, Final reconciliation)

## Purpose

This Guidance document provides non-normative direction for developing the Rail Works Design Drawing Set (DEL-07.01) that defines arrangement and details for PKG-07 rail works at the Canola Oil Transload Facility.

**Relationship to other documents:**
- **Specification.md** defines *what is required* (normative requirements)
- **Procedure.md** defines *how to produce and check* the deliverable (process workflow)
- **Guidance.md** (this document) explains *why and how to think* about the engineering and coordination considerations (non-normative)
- **Datasheet.md** captures *facts and attributes* about the deliverable

**Scope and intent:**
- Support development of drawings for new rail tracks (6 & 7), Track 5 restoration/modifications, ballast, and end stops (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:259, :265)
- Complement the Specification and Procedure without inventing requirements not present in the Employer's Requirements (Source: test/Volume_2_Part_1_Employers_Requirements.pdf; test/Volume_2_Part_2_Employers_Requirements.pdf, clauses TBD)
- Help engineers make informed decisions about drawing content, clarity, and coordination

## Principles

Engineering principles that underpin this deliverable (rationale for Specification requirements):

| Principle | Rationale | Specification Linkage |
|-----------|-----------|----------------------|
| **Scope clarity** | Tight scope definition (PKG-07: Tracks 5, 6, 7; ballast; end stops) prevents scope creep and construction ambiguity | Specification.md: Scope; Requirements FR-02 (differentiate new vs restoration) |
| **Completeness transparency** | Explicitly represent minimum anticipated artifacts (track layouts, profiles, ballast sections, end stop details) so reviewers can verify against decomposition | Specification.md: Requirements FR-01 (cover all anticipated artifacts) |
| **Consistency across deliverables** | Drawings must align with DEL-07.02 (technical specification) and DEL-07.03 (design calculations) to ensure coherent design package | Specification.md: Requirements FR-03, PR-01, PR-02 (traceability and consistency) |
| **Document control discipline** | Consistent sheet naming, notes, and metadata aligned to project practices ensures traceability and auditability | Specification.md: Requirements QR-01 (document control compliance) |
| **Assumption transparency** | Design assumptions must be traceable to calculations or explicitly tagged to prevent implicit assumptions becoming embedded requirements | Specification.md: Requirements QR-03 (assumption traceability) |

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:259, :265, :266-267; test/Volume_2_Part_1_Employers_Requirements.pdf, clauses TBD)

## Considerations

Practical considerations for developing the drawing set (supporting Specification requirements and Procedure workflow):

### Scope and Limits of Work

| Consideration | Guidance | Cross-Reference |
|---------------|----------|-----------------|
| **New works vs restoration** | Clearly differentiate Tracks 6/7 (new works) vs Track 5 (restoration/modifications) using limits-of-work notation, hatching, or notes | Specification.md: Requirements FR-02; Datasheet.md: Content (Additional Drawing Content Requirements) |
| **Interface boundaries** | Show interface points with adjacent packages (civil, process) without asserting unsourced requirements; note "coordinate with [Package]" rather than specifying interface details not yet confirmed | Specification.md: Requirements IR-01; Datasheet.md: Conditions (Interface boundaries) |
| **Employer-provided items** | Identify Employer-provided items at interface connections only; exclude from Contractor scope representation per decomposition boundary | Specification.md: Scope (Scope Exclusions); test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:47 |

### Coordination and Dependencies

| Consideration | Guidance | Cross-Reference |
|---------------|----------|-----------------|
| **External coordination** | Dependencies coordinated externally per NOT_TRACKED mode (see `_DEPENDENCIES.md`); confirm interface expectations before finalizing drawings | Specification.md: Requirements IR-02; Procedure.md: Prerequisites |
| **DEL-07.02 alignment** | Cross-check material/workmanship notes against Rail Works Technical Specification once available; update inputs/assumptions register if conflicts arise | Specification.md: Requirements PR-01, FR-03; Procedure.md: Steps 5 |
| **DEL-07.03 alignment** | Trace design loads, geometry, and assumptions to Design Calculations; ensure drawing notes reflect calculation basis | Specification.md: Requirements PR-02, QR-03; Procedure.md: Steps 3, 5 |

### Drawing Content and Clarity

| Consideration | Guidance | Cross-Reference |
|---------------|----------|-----------------|
| **Level of detail** | Balance detail completeness with readability; show enough to support construction without over-cluttering sheets | Specification.md: Requirements FR-04 to FR-07 (artifact content); Trade-offs section below |
| **Assumptions visibility** | Note design assumptions explicitly (e.g., "preliminary geometry pending survey," "ballast depth per calc DEL-07.03-XX"); tag unsourced assumptions as **ASSUMPTION** | Specification.md: Requirements QR-03; Procedure.md: Steps 3 |
| **Constructability focus** | Ensure details are constructible and communicate intent clearly; avoid ambiguous notes or incomplete sections | Specification.md: Verification (constructability/clarity check) |

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:47, :259, :266-267; Procedure.md; Specification.md)

## Trade-offs

Engineering trade-offs inherent in drawing development (informing judgment when applying Specification requirements):

| Trade-off | Option A | Option B | Guidance | Cross-Reference |
|-----------|----------|----------|----------|-----------------|
| **Detail level vs readability** | More dimensions/notes (supports constructability) | Fewer dimensions/notes (clearer sheets) | Include critical dimensions and notes required for construction; refer to DEL-07.02 for general workmanship; the "right" balance is **TBD** until ER drawing/detailing requirements identified | Specification.md: Requirements FR-04 to FR-07; Considerations (Drawing Content and Clarity) |
| **Assumption visibility** | Explicit assumption notes (transparent but clutters drawings) | Implicit assumptions (cleaner but risks miscommunication) | Explicitly note assumptions (e.g., "preliminary geometry," "pending survey"); trace to DEL-07.03 or tag **ASSUMPTION**; transparency outweighs clutter | Specification.md: Requirements QR-03; Procedure.md: Steps 3 |
| **Interface detail** | Show interface details in full (may conflict with external coordination) | Show interface callouts only (requires external coordination) | Show interface callouts without asserting unsourced requirements; defer detail to coordination workflow per NOT_TRACKED dependency mode | Specification.md: Requirements IR-01, IR-02; Considerations (Coordination and Dependencies) |
| **New vs restoration representation** | Separate sheet sets for new works vs restoration | Combined sheets with clear notation | Either approach acceptable if limits-of-work clearly differentiate Tracks 6/7 (new) from Track 5 (restoration); choose based on drawing scale and clarity | Specification.md: Requirements FR-02; Considerations (Scope and Limits of Work) |

## Examples (Anticipated Artifacts)

Illustrative examples of anticipated artifacts (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:265; Datasheet.md: Content):

### Example 1: Track Layout Plan

**Content:**
- Plan view showing Tracks 5, 6, 7 arrangement and alignment
- Limits of work with notation differentiating new works (Tracks 6/7) vs restoration (Track 5)
- Interface callouts for coordination with adjacent packages (e.g., "coordinate tie-in with civil grading PKG-02")
- Reference to DEL-07.03 for design basis

**Purpose:** Communicates spatial arrangement and construction scope (Specification.md: Requirements FR-01, FR-02, FR-04)

### Example 2: Rail Profile

**Content:**
- Longitudinal profile showing rail elevations and vertical geometry for each track
- Critical elevations and grade callouts
- Reference datum and benchmarks
- Design assumptions noted (e.g., "ballast depth per DEL-07.03-XX")

**Purpose:** Communicates vertical design and construction requirements (Specification.md: Requirements FR-01, FR-05, QR-03)

### Example 3: Ballast Section

**Content:**
- Typical cross-section showing ballast depth, material zones, and sub-base details
- Material specifications cross-referenced to DEL-07.02
- Dimensions and tolerances

**Purpose:** Communicates ballast construction requirements (Specification.md: Requirements FR-01, FR-06, PR-01)

### Example 4: End Stop Detail

**Content:**
- Detail drawing of end stop configuration, anchoring system, and clearances
- Material and fabrication notes cross-referenced to DEL-07.02
- Installation tolerances

**Purpose:** Communicates end stop design and installation requirements (Specification.md: Requirements FR-01, FR-07)

## Cross-Document Notes

### Guidance ↔ Specification

| Guidance Section | Specification Section | Relationship |
|------------------|----------------------|--------------|
| Principles | Requirements (all categories) | Principles provide rationale for requirements; each requirement has supporting principle |
| Considerations | Requirements (Functional, Interface, Quality) | Considerations offer practical direction for applying requirements |
| Trade-offs | Requirements (Quality), Verification | Trade-offs inform judgment when requirements allow flexibility; help interpret acceptance criteria |
| Examples | Requirements (Functional), Scope (Anticipated Artifacts) | Examples illustrate how anticipated artifacts satisfy functional requirements |

### Guidance ↔ Datasheet

| Guidance Section | Datasheet Section | Relationship |
|------------------|-------------------|--------------|
| Principles (Document control discipline) | Attributes (Drawing Set Metadata) | Principle supports metadata attribute requirements |
| Considerations (Drawing Content and Clarity) | Content (Additional Drawing Content Requirements) | Considerations elaborate on content requirements from Datasheet |
| Examples | Content (Anticipated Artifacts) | Examples illustrate anticipated artifacts listed in Datasheet |

### Guidance ↔ Procedure

| Guidance Section | Procedure Section | Relationship |
|------------------|-------------------|--------------|
| Considerations (Coordination and Dependencies) | Prerequisites, Steps 2, 5 | Considerations inform prerequisite confirmation and cross-check steps |
| Considerations (Drawing Content and Clarity) | Steps 3, 4 (inputs/assumptions register, draft production) | Considerations guide assumption documentation and draft content decisions |
| Trade-offs | Steps (production workflow) | Trade-offs help engineers make decisions during Procedure execution |
