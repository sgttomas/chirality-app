# Source Index

## Snapshot Identification

| Property | Value |
|----------|-------|
| **Snapshot ID** | EST_DEL-02-01_2026-02-04_1323 |
| **Deliverable** | DEL-02-01 ConceptDesignPackage |

---

## Source Priority

Sources are listed in priority order per PROTOCOL Phase 2.2:

1. **Explicit Pricing Sources** - None available
2. **Rate Tables / Cost Libraries** - None available
3. **Quantity Sources** - Four Documents (Datasheet, Specification, Guidance, Procedure)
4. **Fallback Model** - Allowances used

---

## Sources Discovered

### Primary Sources (Four Documents)

| Source | Path | Relevance | Used For |
|--------|------|-----------|----------|
| _CONTEXT.md | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-04_Design Proposal (Concept + Design Brief)/1_Working/DEL-02-01_ConceptDesignPackage/_CONTEXT.md | Deliverable identity, acceptance criteria, scope traceability | Scope definition, acceptance criteria |
| Datasheet.md | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-04_Design Proposal (Concept + Design Brief)/1_Working/DEL-02-01_ConceptDesignPackage/Datasheet.md | Building program attributes, site attributes, technical requirements | Quantity/scope extraction |
| Specification.md | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-04_Design Proposal (Concept + Design Brief)/1_Working/DEL-02-01_ConceptDesignPackage/Specification.md | Requirements R1-R15, deliverable artifacts list | Scope definition, deliverable requirements |
| Guidance.md | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-04_Design Proposal (Concept + Design Brief)/1_Working/DEL-02-01_ConceptDesignPackage/Guidance.md | Design principles, considerations, trade-offs | Execution drivers, complexity factors |
| Procedure.md | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/PKG-04_Design Proposal (Concept + Design Brief)/1_Working/DEL-02-01_ConceptDesignPackage/Procedure.md | Production steps, team roles, QA requirements | Work breakdown, effort estimation |

### Agent Instruction Sources

| Source | Path | Relevance |
|--------|------|-----------|
| AGENTS.md | /Users/ryan/ai-env/projects/chirality-app-test/AGENTS.md | Agent framework, project structure |
| AGENT_ESTIMATING.md | /Users/ryan/ai-env/projects/chirality-app-test/agents/AGENT_ESTIMATING.md | Estimating protocol, spec, structure |

### Pricing Sources

| Source Type | Available | Path | Notes |
|-------------|-----------|------|-------|
| Vendor Quotes | NO | N/A | No quotes available for design services |
| Rate Tables | NO | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/_Estimates/_RateTables/ | Directory empty |
| Historical Data | NO | N/A | No comparable project data provided |
| _CONFIG.md | NO | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6/_Estimates/_CONFIG.md | File does not exist |

---

## Key Information Extracted

### From _CONTEXT.md

| Information | Value | Used In |
|-------------|-------|---------|
| Deliverable Name | ConceptDesignPackage | BOE, Summary |
| Package | PKG-04 Design Proposal (Concept + Design Brief) | CBS mapping |
| Discipline | Architecture / Design | CBS mapping (E) |
| Responsible Party | Lead Architect / Designer | Effort allocation |
| Acceptance Criteria | Program fit, excludes pickled sand, Addendum 03 requirements | QA scope |

### From Datasheet.md

| Information | Value | Used In |
|-------------|-------|---------|
| Building Type | Integrated Fire Hall + Public Works | Complexity factor |
| Developable Area | 12 acres | Site plan scope |
| Technical Requirements | 16 ft doors, sumps, exhaust, generator, fill stations, solar | L-007 |
| Blocking Conflict A-003 | Town setbacks TBD | Risk R-002 |
| Status | INITIALIZED | Estimate timing |

### From Specification.md

| Information | Value | Used In |
|-------------|-------|---------|
| Deliverable Artifacts | Site plan, floor plans, massing, sections, elevations, narrative | Work breakdown |
| Requirements Count | R1-R15 + system integration | Scope complexity |
| Blocking Conflict C-002 | Appendix B location TBD | Risk R-001 |
| Interfaces | DEL-02-02, DEL-02-03, PKG-02 | Coordination scope |

### From Guidance.md

| Information | Value | Used In |
|-------------|-------|---------|
| Evaluation Impact | 20 points (Conceptual Design) | Effort justification |
| Design Level | Schematic/concept for proposal | Effort sizing |
| Trade-offs | 4 documented trade-offs | Complexity factor |

### From Procedure.md

| Information | Value | Used In |
|-------------|-------|---------|
| Steps | 11 steps defined | Work breakdown |
| Team Roles | 7 roles (Architect, Civil, Structural, MEP, Code, PM) | Line item structure |
| Prerequisites | Tools, reference materials | A-006 assumption |
| QA Requirements | Self-review, peer review, cross-deliverable check | L-011, L-012 |

---

## Source Selection Decision

| Decision ID | Decision | Rationale |
|-------------|----------|-----------|
| D-002 | Use ALLOWANCE for all pricing | No rate tables or quotes available; straight-through pipeline requires pricing basis |

---

## Document Control

| Property | Value |
|----------|-------|
| **Created** | 2026-02-04 |
| **Author** | ESTIMATING Agent (Type 2) |

---

**END OF SOURCE INDEX**
