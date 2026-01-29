# PROJECT DECOMPOSITION PROTOCOL

## Instructions for AI-assisted breakdown of engineering projects into actionable structure.

---

## Purpose

Extract tacit project knowledge through dialogue. Create buckets (packages, deliverables, documents) that enable work to proceed. Surface HOLDs early. Establish Action Items for tracking.

This protocol determines WHAT the project structure is. Execution of work items follows UNIFIED.

---

## Part 1: Pattern Library

### 1.1 Project Hierarchy

Self-similar at each level:

```
Project
  └── Package
        └── Deliverable
              └── Document
                    └── Task
```

Each level has:
- Scope definition
- Dependencies (what must complete before this can proceed)
- HOLDs (blockers requiring resolution)
- Action Item Log for tracking

### 1.2 HOLD Types

Five types of blockers that stop work:

| Type | Waiting For |
|------|-------------|
| **Decision** | A choice to be made (technical, commercial, organizational) |
| **Information** | Data, documents, or facts not yet available |
| **Clarification** | Ambiguity that must be resolved |
| **Resources** | People, equipment, budget, or access |
| **Approval** | Sign-off from authority |

**Risk of Change** is a modifier on any HOLD, not a standalone type. It flags HOLDs where the answer may shift.

### 1.3 Seven Needs (Pre-HOLD Signals)

Report these BEFORE they become HOLDs:

1. **Information** - "I will need X to proceed"
2. **Clarification** - "X is ambiguous"
3. **Priorities** - "Which of these matters more?"
4. **Decisions** - "This requires a choice"
5. **Opportunities** - "We could do X if we act now"
6. **Risks** - "X could go wrong"
7. **Approval** - "This will need sign-off"

### 1.4 Document Freeze States

Documents progress through approval gates (the DAG nodes):

```
Working → IFA → IFR → IFH → IFC → Issue for Use
```

| State | Meaning |
|-------|---------|
| Working | In development |
| IFA | Issued for Approval |
| IFR | Issued for Review |
| IFH | Issued for HAZOP (or equivalent study) |
| IFC | Issued for Construction |
| Issue for Use | Final, approved for implementation |

**Dependencies are expressed as:** "Document X must reach State Y before Document Z can enter State W"

### 1.5 Action Item Log Structure

Three levels with escalation:

| Level | Scope | Escalates To |
|-------|-------|--------------|
| Document Action Item | HOLDs blocking a single document | Package Action Item |
| Package Action Item | HOLDs blocking package progress | Project Action Item |
| Project Action Item | Cross-package and external HOLDs | Sponsor/Authority |

**Invariant fields for every Action Item entry:**

| Field | Purpose |
|-------|---------|
| Item Type | HOLD type or Need type |
| Status | Open / In Progress / Resolved / Deferred |
| HOLD Type | Decision / Information / Clarification / Resources / Approval |
| Priority | Critical / High / Medium / Low |
| Description | What is blocked and why |
| Responsible Party | Who owns resolution |
| Target Date | When resolution is needed |
| Updates | Running log of progress |

### 1.6 Nine Domains of Task Management

Every task exists in one cell of this 3×3 matrix:

|  | **Data** (What) | **Information** (How) | **Knowledge** (Why) |
|---|---|---|---|
| **What** | Action Item | Documentation | Approval |
| **How** | Assign | Work Methods | Check |
| **Why** | Prioritize | Plan | Decide |

Use this to classify where work is stuck or what kind of attention it needs.

### 1.7 Information Triage Categories

Incoming information routes to one of seven categories:

| Category | What belongs here |
|----------|-------------------|
| Scope | Changes to what's included/excluded |
| Schedule | Dates, sequences, milestones |
| Decision | Choices made or needed |
| Action | Work to be done |
| Deliverable | Outputs and their status |
| Contract | Commercial/legal matters |
| RISK | Threats and uncertainties |

File by WORK CONTEXT, not by source.

---

## Part 2: The Nine Phases

### Phase 1: Establish DOMAIN

Identify the operating context that constrains everything else.

**Elicit:**
- Industry and sector (upstream O&G, midstream, downstream, petrochemical, etc.)
- Engineering disciplines involved
- Regulatory jurisdiction
- Governing codes and standards
- Company standards and templates
- Key vocabulary and definitions

**Output:** DOMAIN context captured (may be verbal or documented)

---

### Phase 2: Gather Scope Materials

Collect everything that defines what the project must accomplish.

**Gather:**
- Contracts and SOWs
- Basis of Design documents
- Feasibility studies
- Reference projects
- Client requirements
- Regulatory requirements

**Triage inputs by category** (Scope, Schedule, Decision, Action, Deliverable, Contract, RISK)

**Output:** Inventory of scope materials with categorization

---

### Phase 3: Define PROJECT CONTEXT

Establish the project-level parameters.

**Elicit:**
- Project name and identifier
- Project objectives (what success looks like)
- Key stakeholders and their interests
- Approval authorities (who signs off on what)
- Major constraints (budget, schedule, technical, organizational)
- Known risks at project level

**Output:** PROJECT context established

---

### Phase 4: Define PACKAGES

Break the project into logical groupings of work.

**Elicit:**
- What are the natural divisions? (by discipline, by area, by system, by phase)
- What packages does the organization typically use?
- Are there contractual package boundaries?
- Which packages have external dependencies (vendors, client, other contractors)?

**For each package, capture:**
- Package ID and name
- Scope description
- Lead discipline/responsibility
- Known dependencies on other packages

**Output:** Package list with descriptions and cross-dependencies

---

### Phase 5: Define DELIVERABLES

Identify the concrete outputs for each package.

**For each package, elicit:**
- What documents/outputs must this package produce?
- What is the approval path for each?
- What inputs does each deliverable need?
- Who consumes each deliverable?

**For each deliverable, capture:**
- Deliverable ID and name
- Parent package
- Description
- Required approval state (IFA, IFR, IFC, etc.)
- Consuming parties

**Output:** Deliverable list organized by package

---

### Phase 6: Define DOCUMENTS and Approval Progression

Map the document structure and freeze state requirements.

**For each deliverable, elicit:**
- What documents comprise this deliverable?
- What freeze state must each reach?
- What is the sequence of approvals?
- Are there intermediate review gates?

**Build the DAG:**
- Document X at State Y → enables Document Z to reach State W
- Map the critical path through approval states

**Output:** Document list with freeze state targets and dependency DAG

---

### Phase 7: Identify DEPENDENCIES

Capture all blocking relationships.

**Types of dependencies:**
- **Internal:** Document A needs Document B at state X
- **Cross-package:** Package A blocked by Package B deliverable
- **External-client:** Waiting on client decision/approval/information
- **External-vendor:** Waiting on vendor data/quotes/deliverables
- **External-regulatory:** Waiting on permit/approval/clarification
- **External-other:** Third parties, site access, utilities, etc.

**For each dependency, capture:**
- What is blocked
- What is blocking it
- What state/condition clears the block
- Current status

**Output:** Dependency register

---

### Phase 8: Surface Initial HOLDs

Identify known blockers from the decomposition process.

**Review each package and deliverable for:**
- Missing information
- Unclear requirements
- Decisions not yet made
- Resources not yet secured
- Approvals not yet obtained

**Classify each by HOLD type and assign to appropriate Action Item level:**
- Document-level HOLDs → Document Action Item
- Package-level HOLDs → Package Action Item
- Cross-package or external HOLDs → Project Action Item

**Output:** Initial HOLD inventory assigned to Action Items

---

### Phase 9: Establish Action Items

Initialize the tracking structure.

**Create:**
- Project Action Item with all project-level HOLDs
- Package Action Item for each package with package-level HOLDs
- Template for Document Action Items (created as documents enter active work)

**For each Action Item entry, populate:**
- Item Type, Status, HOLD Type, Priority
- Description, Responsible Party, Target Date
- Initial update entry

**Output:** Active Action Items ready for use

---

## Part 3: Handoff to Execution

When decomposition is complete:

1. **Project structure exists:** Packages, deliverables, documents defined
2. **Dependencies mapped:** DAG of document states established
3. **HOLDs surfaced:** Initial blockers identified and assigned
4. **Action Items active:** Tracking structure in place

Individual work items (documents, tasks) are executed using UNIFIED protocol:
- DOMAIN established (Phase 1 carries forward)
- TASK defined for specific work item
- Four document types produced as applicable
- Engineer validates

---

## Four Questions This Prevents

Good project engineering prevents the team from ever asking:

1. **"What are the priorities?"** → The DAG and Action Items make this visible
2. **"Where is the information?"** → Scope materials are categorized and indexed
3. **"Which version is current?"** → Freeze states track document progression
4. **"What did we decide?"** → Decisions are logged in Action Items with rationale

---

## Operating Principle

The human has tacit knowledge about the project. The AI has throughput for structuring. Together through dialogue:

- AI proposes structure based on patterns
- Human corrects, refines, adds context
- AI captures and organizes
- Human validates

The buckets come first. Work flows into buckets. Information triages into buckets. HOLDs attach to buckets. Without structure, there is chaos.
