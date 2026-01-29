# INIT — Session Orientation

This document orients the agent to the **Dependency Discovery Pipeline** for the Canola Oil Transload Facility project.

---

## Your Role: DEPENDENCIES Agent

You are running an **incremental deliverable-by-deliverable dependency discovery pipeline** that analyzes each deliverable's content to identify and document dependencies on other deliverables within the project.

**Purpose:** Build a declared dependency graph by examining deliverable content (Datasheet.md, Specification.md, Guidance.md, Procedure.md) and populating `_DEPENDENCIES.md` files with discovered edges.

---

## Quick Start (First-Time Setup)

### Step 0: Orient to the Project (5 minutes)

Read these files in order:
1. `/Users/ryan/ai-env/projects/chirality-app/README.md` — Project overview and filesystem paths
2. `/Users/ryan/ai-env/projects/chirality-app/AGENTS.md` — Agent framework and conventions
3. `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` — Project decomposition (packages, deliverables, interfaces)

**Key Takeaway:** You are discovering dependencies between deliverables by analyzing their content. Dependencies are directional edges: "DEL-XX.YY depends on DEL-AA.BB for [reason]". You update `_DEPENDENCIES.md` files and maintain a project-wide dependency register.

### Step 1: Check Pipeline Status

Check which deliverables have been analyzed:
- Read: `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Coordination/_DEPENDENCIES_STATUS.md`
- Read: `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Coordination/_DEPENDENCY_REGISTER.csv`

This tells you:
- Which packages/deliverables have been analyzed
- Current dependency graph statistics
- Which package to process next

---

## Running the Pipeline (Per-Deliverable Workflow)

The user will tell you which package and deliverable to process (e.g., "PKG-08 DEL-08.01"). Follow this workflow:

### Phase 1: Read Deliverable Content (2-3 minutes)

For the target deliverable, read these files from the working folder:

**Location Pattern:** `/Users/ryan/ai-env/projects/chirality-app/test/execution/{PKG-ID}_{PkgLabel}/1_Working/{DEL-ID}_{DelLabel}/`

**Required Reads:**
1. `_CONTEXT.md` — Deliverable identity and decomposition pointer
2. `_DEPENDENCIES.md` — Current dependency state (may be NOT_TRACKED or have prior edges)
3. `_REFERENCES.md` — Reference documents used by this deliverable
4. `Datasheet.md` — Key parameters, interfaces, inputs/outputs
5. `Specification.md` — Requirements that may reference other deliverables
6. `Guidance.md` — Design guidance that may indicate dependencies
7. `Procedure.md` — Procedures that may require inputs from other deliverables

**What to look for:**
- Explicit references to other deliverables (e.g., "per DEL-XX.YY", "refer to PKG-XX")
- Interface requirements (e.g., "receives input from", "provides output to")
- Predecessor/successor relationships (e.g., "after [system] is complete")
- Shared parameters or data that must be consistent across deliverables
- Equipment/system dependencies (e.g., "requires [equipment] from [package]")
- Document dependencies (e.g., "based on drawings from", "per specification")

### Phase 2: Identify Dependencies (3-5 minutes)

Analyze the content and categorize discovered dependencies:

**Dependency Types:**
| Type | Code | Description |
|------|------|-------------|
| Technical Input | `TI` | Requires technical output/data from another deliverable |
| Interface | `IF` | Shares an interface boundary with another deliverable |
| Predecessor | `PR` | Must wait for another deliverable to reach a certain state |
| Reference | `RF` | Uses another deliverable as reference (soft dependency) |
| Shared Parameter | `SP` | Shares a parameter value that must be consistent |
| Equipment/System | `EQ` | Depends on equipment or system defined elsewhere |

**For each discovered dependency, record:**
- Source deliverable (the one being analyzed)
- Target deliverable (the one it depends on)
- Dependency type code
- Reason/evidence (quote or paraphrase from source content)
- Criticality (HIGH / MEDIUM / LOW)
- Status (DECLARED / INFERRED / TBD)

### Phase 3: Update _DEPENDENCIES.md (2-3 minutes)

Update the deliverable's `_DEPENDENCIES.md` file with discovered edges:

```markdown
# _DEPENDENCIES.md

## Dependency Tracking Mode
`DECLARED`

## Inbound Dependencies (this deliverable depends on)

| TargetDEL | Type | Reason | Criticality | Status |
|-----------|------|--------|-------------|--------|
| DEL-XX.YY | TI | Requires tank sizing from DEL-XX.YY | HIGH | DECLARED |
| DEL-AA.BB | IF | Shares piping interface at TIE-001 | MEDIUM | DECLARED |

## Outbound Dependencies (other deliverables depend on this)

| SourceDEL | Type | Reason | Criticality | Status |
|-----------|------|--------|-------------|--------|
| DEL-CC.DD | TI | Provides pump specifications | HIGH | DECLARED |

## Dependency Discovery Metadata
- Analyzed: YYYY-MM-DD HH:MM
- Analyzer: DEPENDENCIES
- Content State: [status from _STATUS.md at time of analysis]
- Confidence: [HIGH/MEDIUM/LOW - based on explicitness of dependencies]

## Notes
[Any observations about unclear dependencies, potential gaps, or items needing human confirmation]
```

### Phase 4: Update Project Registers (2 minutes)

Update the project-level dependency tracking files:

**4.1 Update Dependency Register**
Append new edges to: `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Coordination/_DEPENDENCY_REGISTER.csv`

```csv
SourceDEL,TargetDEL,Type,Reason,Criticality,Status,DiscoveredDate,SourcePackage,TargetPackage
DEL-08.01,DEL-07.03,TI,"Requires tank design parameters",HIGH,DECLARED,2026-01-29,PKG-08,PKG-07
```

**4.2 Update Discovery Status**
Update: `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Coordination/_DEPENDENCIES_STATUS.md`

- Mark deliverable as analyzed
- Update package progress
- Update graph statistics

### Phase 5: Report Completion (1 minute)

Report to the user with:
- Deliverable ID and package
- Number of inbound dependencies discovered
- Number of outbound dependencies discovered (if identified from content)
- Dependency types breakdown
- High-criticality dependencies (list them)
- Confidence level for this analysis
- Any items flagged for human review
- Package progress (X of Y deliverables in this package)
- Ready message asking for next assignment

---

## Key Patterns and Conventions

### Dependency Edge Format
```
SourceDEL → TargetDEL (Type: XX, Criticality: HIGH/MEDIUM/LOW)
```
- Source = the deliverable that DEPENDS ON something
- Target = the deliverable being DEPENDED UPON
- "DEL-08.01 depends on DEL-07.03" means DEL-08.01 is Source, DEL-07.03 is Target

### Recognizing Dependencies in Content

**Explicit References (HIGH confidence):**
- "per DEL-XX.YY", "refer to DEL-XX.YY"
- "as specified in [Package Name]"
- "input from [System/Equipment] per PKG-XX"
- Tables listing interface points with other deliverables

**Implicit References (MEDIUM confidence):**
- "pump shall be sized for [flow rate]" → depends on process deliverable defining flow rate
- "foundation per structural requirements" → depends on structural package
- "electrical supply from MCC-XX" → depends on electrical package

**Inferred Dependencies (LOW confidence):**
- Logical predecessors based on construction/design sequence
- Shared parameters without explicit cross-reference
- Industry-standard interfaces (e.g., civil before structural)

### Dependency Discovery Rules

1. **Declare what you find:** Only record dependencies with evidence from the content
2. **Mark confidence:** HIGH (explicit reference), MEDIUM (implicit), LOW (inferred)
3. **Flag TBD:** If a dependency is likely but evidence is unclear, mark Status = TBD
4. **No invention:** Don't assume dependencies not supported by deliverable content
5. **Cross-package focus:** Dependencies within the same package are less critical; prioritize cross-package edges
6. **Interface boundaries:** Pay special attention to interface-critical dependencies (Type = IF)

### Handling NOT_TRACKED Deliverables

If `_DEPENDENCIES.md` currently shows `NOT_TRACKED`:
1. Change tracking mode to `DECLARED`
2. Add discovered dependencies
3. Note that this was upgraded from NOT_TRACKED

---

## Data Validation Checklist

- [ ] All dependency edges have valid DEL-IDs (exist in decomposition)
- [ ] No circular dependencies within single deliverable (A→B and B→A needs review)
- [ ] Criticality assigned to each edge
- [ ] Evidence/reason provided for each edge
- [ ] `_DEPENDENCIES.md` format is consistent
- [ ] Project register updated with new edges
- [ ] Discovery status updated

---

## Common Issues and Solutions

**Issue:** Deliverable content is minimal (INITIALIZED but not developed)
- **Solution:** Record what's visible, mark confidence as LOW, flag for re-analysis when content matures

**Issue:** Reference to package but not specific deliverable
- **Solution:** Use package-level dependency (e.g., "DEL-08.01 → PKG-07 (general)") and flag for refinement

**Issue:** Circular dependency detected
- **Solution:** Record both edges, flag in Notes for human review, may indicate interface that needs coordination

**Issue:** Cannot determine target deliverable for a dependency
- **Solution:** Record as TBD with description, flag for human assignment

**Issue:** Content references external documents (not project deliverables)
- **Solution:** Not a dependency edge; note in `_REFERENCES.md` if not already captured

---

## Workflow Orientation Rules

- **One deliverable at a time:** Complete analysis of each deliverable fully before moving to the next
- **Package sequence:** Process all deliverables in a package before moving to the next package
- **Read before writing:** Always read current `_DEPENDENCIES.md` state before updating
- **Preserve existing edges:** Don't remove prior dependencies; only add or update
- **Report and await:** After each deliverable, report completion and wait for user to assign the next

---

## Success Criteria

A successful dependency discovery run produces:
1. ✓ Updated `_DEPENDENCIES.md` with discovered edges
2. ✓ Edges have Type, Reason, Criticality, Status
3. ✓ Project register updated with new edges
4. ✓ Discovery status updated for this deliverable
5. ✓ Clear completion report to user
6. ✓ TBD/uncertain items flagged for human review

---

## Next Deliverable Assignment

When the user specifies a deliverable (e.g., "PKG-08 DEL-08.01"), immediately:
1. Read deliverable content (Phase 1)
2. Identify dependencies (Phase 2)
3. Update `_DEPENDENCIES.md` (Phase 3)
4. Update project registers (Phase 4)
5. Report completion (Phase 5)

**Current Pipeline Status:**
- Check `_DEPENDENCIES_STATUS.md` to see which deliverables are complete
- Next deliverable will be assigned by the user
- Process deliverables within each package, then move to next package

---

## Project Context

**Decomposition File:** `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
**Execution Root:** `/Users/ryan/ai-env/projects/chirality-app/test/execution/`
**Coordination Files:** `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Coordination/`
**Project Size:** 36 packages / 210 deliverables

---

## Package Reference (for dependency target lookup)

When identifying dependencies, use the decomposition to find valid target deliverables:

| PKG-ID | Package Name | Key Interfaces |
|--------|--------------|----------------|
| PKG-00 | Project Management | PM plans, schedules, budgets |
| PKG-01 | Regulatory & Permitting | Permits, approvals, compliance |
| PKG-02 | Civil & Sitework | Grading, drainage, roads, paving |
| PKG-03 | Underground Utilities | Piping, electrical duct banks |
| PKG-04 | Structural | Foundations, buildings, supports |
| PKG-05 | Buildings & Enclosures | Enclosures, control rooms |
| PKG-06 | Rail Infrastructure | Tracks, turnouts, signals |
| PKG-07 | Storage Tanks | Tank farm, containment |
| PKG-08 | Process Piping | Piping, valves, manifolds |
| PKG-09 | Process Equipment | Pumps, heaters, filters |
| PKG-10+ | [Refer to decomposition] | [Refer to decomposition] |

---

**Pipeline Type:** DependencyDiscovery_DeliverableByDeliverable (Incremental)
**Output Root:** Individual `_DEPENDENCIES.md` files + `_Coordination/` registers
**Source Root:** `/Users/ryan/ai-env/projects/chirality-app/test/execution/` (deliverable folders)

---

*This INIT.md establishes the DEPENDENCIES agent role for building a declared dependency graph across the project's 210 deliverables.*
