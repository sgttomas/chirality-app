# STRUCTURE

## Descriptive — "What is it?"

This document defines the schema for project decomposition: the entities, their attributes, and their relationships.

---

## Domain (Optional)

The operating context that provides focus for decomposition. Emerges through scope alignment. Useful for directing the agent's attention but not a prerequisite — decomposition can proceed without explicit domain definition.

| Field | Description |
|-------|-------------|
| Context | Discipline, industry, or field |
| Vocabulary | Domain-specific terminology (if relevant) |

---

## Project

The top-level container for a decomposition exercise.

| Field | Description |
|-------|-------------|
| Name | Project identifier |
| Objectives | What success looks like |
| Contains | Packages |

---

## Package

A logical grouping of Deliverables. Entirely user-defined — a project can be packaged any way. Often organized by discipline or user type. Packages can be nested within other Packages if desired.

| Field | Description |
|-------|-------------|
| ID | Unique package identifier |
| Name | Descriptive name |
| Scope Description | What is included, what is excluded (distinct from the project's Scope of Work) |
| Organization Scheme | User-defined (by area, system, phase, discipline, etc.) |
| Decisions | Major decisions captured during decomposition |
| Contains | Deliverables (or nested Packages) |

---

## Deliverable

A unit of scope — an aspect of project scope that must be fulfilled through Artifacts. Deliverables are ideas, not tangible outputs. They represent what must be delivered.

| Field | Description |
|-------|-------------|
| ID | Unique deliverable identifier |
| Name | Descriptive name |
| Parent Package | Which Package contains this Deliverable |
| Description | What this Deliverable represents |
| Responsible Party | Who produces the Artifacts |
| Type | The Artifact type (all Artifacts within must be this type) |
| Contains | Artifacts (indefinite number, all same type) |

---

## Artifact

How a Deliverable is attained. Artifacts are the tangible outputs that fulfill the Deliverable. All Artifacts within a Deliverable must be of the same type.

| Field | Description |
|-------|-------------|
| ID | Unique artifact identifier |
| Name | Descriptive name |
| Parent Deliverable | Which Deliverable contains this Artifact |
| Type | Must match parent Deliverable's type |

Note: At decomposition time, Artifacts are anticipated rather than fully enumerated. A Deliverable may contain one Artifact (e.g., "3D Model") or many (e.g., hundreds of P&ID drawings).

---

## Type

A classification for Artifacts within a Deliverable. Types are conventional and user-defined. Examples include Drawing, Specification, Model, Report — but vary by domain. The agent should ask the user about artifact types rather than assume.

All Artifacts within a Deliverable must share the same Type. If different types are needed, they belong to different Deliverables.

---

## Relationships

### Containment

```
Project
  └── Package (can nest)
        └── Deliverable
              └── Artifact
```

- Project contains Packages
- Packages contain Deliverables (or nested Packages)
- Deliverables contain Artifacts
- Containment is strict (no overlap)
- Every Deliverable must belong to exactly one Package
- Every Artifact must belong to exactly one Deliverable

### Key Constraints

| Constraint | Description |
|------------|-------------|
| Artifact type consistency | All Artifacts in a Deliverable share the same type |
| Artifact quantity | Indefinite number of Artifacts per Deliverable |
| Package flexibility | Packages are entirely user-defined |
| Deliverable coverage | All scope must be represented in Deliverables |

---

## Hierarchy Properties

| Property | Description |
|----------|-------------|
| Self-similarity | Same structural pattern at each level |
| Strict containment | Each element belongs to exactly one parent |
