# PROBLEM

## Purpose

Instructions for Claude on what an instance-level PROBLEM contains and how to produce one.

When Claude completes the task-discovery portion of INTAKE (after HANDOFF exists), Claude produces a PROBLEM — a structured representation of the specific task that will guide artifact production.

The human does not read or fill out this document. Claude populates it through conversation.

---

## 1. What PROBLEM Captures

PROBLEM captures **instance-level parameters** — things specific to the immediate task.

---

## 2. Subject

Claude must discover and record:

| Field | What to Elicit |
|-------|----------------|
| Title | A short name for this task |
| Subject | What is being documented (equipment, system, process, project) |
| Summary | One paragraph describing what this effort will produce |

### How to Elicit

Ask:
- "What do you need to document?"
- "Can you give me a short name for this task?"
- "What will you have when we're done?"

---

## 3. Context

Claude must discover and record:

| Field | What to Elicit | Required |
|-------|----------------|----------|
| Background | Why this documentation is needed now | Yes |
| Trigger | What initiated this work (project phase, incident, audit, new equipment) | No |
| Stakeholders | Who will use or review these documents | No |

### How to Elicit

Ask:
- "Why do you need this documentation now?"
- "What triggered this work?"
- "Who's going to use these documents?"

---

## 4. Governing Standards

Claude must discover and record:

| Field | What to Elicit | Required |
|-------|----------------|----------|
| Codes | Specific code sections that apply to this task | Yes |
| Standards | Industry or company standards for this task | No |
| Regulations | Regulatory requirements for this task | No |

### How to Elicit

Ask:
- "What codes apply specifically to this work?" (May inherit from HANDOFF)
- "Are there project-specific standards?"
- "Any regulatory requirements beyond the usual?"

---

## 5. References

**This is the most important section.** Claude does not invent engineering content — Claude extracts, organizes, and structures information from source materials. Without references, there is nothing to work from.

### What to Gather

| Material Type | Examples | Required |
|---------------|----------|----------|
| Process inputs | P&IDs, PFDs, heat and material balances | Yes, if they exist |
| Calculations | Hydraulic calcs, load calcs, sizing sheets | Yes, if they exist |
| Vendor materials | Cut sheets, datasheets, quotes, proposals | Yes, if they exist |
| Existing documents | Prior specs, similar equipment docs | No, but valuable |
| Templates | Company or project templates | No, but valuable |
| Standards extracts | Relevant code sections | No, Claude can reference |

### How to Elicit

Claude should ask early and be persistent:
- "What materials do you have that I should work from?"
- "Do you have P&IDs, calcs, vendor datasheets?"
- "Any existing specs for similar equipment I can reference?"
- "Can you share those files with me?"

**Better inputs produce better outputs.** Claude should make this clear without being annoying.

### Working From References

Once materials are shared:
- Claude reads and extracts relevant information
- Claude asks clarifying questions about the materials
- Claude cross-references between documents
- Claude identifies gaps or inconsistencies
- Claude traces artifact content back to sources

---

## 6. Deliverables

Claude must discover and record:

| Field | What to Elicit |
|-------|----------------|
| Document types needed | Which of the domain's document types are required |
| Schema adjustments | Any modifications to standard schemas for this task |

### How to Elicit

Using document types from HANDOFF:
- "For this task, which do you need: Datasheet? Specification? Guidance? Procedure?"
- "All of them, or just some?"
- "Any sections you'd add or skip for this particular task?"

---

## 7. Downstream Use

Claude must discover and record:

| Field | What to Elicit | Required |
|-------|----------------|----------|
| Purpose | What documents will be used for | Yes |
| Audience | Who will read and act on them | Yes |
| Lifecycle | How long documents must remain valid | No |

### How to Elicit

Ask:
- "What will these documents be used for?"
- "Who's the audience — procurement, construction, operations?"
- "How long do these need to stay current?"

---

## 8. Constraints

Claude must discover and record:

| Field | What to Elicit | Required |
|-------|----------------|----------|
| Technical | Technical limitations or boundaries | No |
| Schedule | Time constraints | No |
| Budget | Cost constraints | No |
| Organizational | Approval requirements, access limitations | No |

### How to Elicit

Ask:
- "Any technical constraints I should know about?"
- "What's your timeline?"
- "Any budget or approval constraints?"

---

## 9. Open Questions

Claude must discover and record:

| Field | What to Elicit |
|-------|----------------|
| Questions | What the engineer knows they don't know |
| Destinations | Where answers would go (if known) |

### How to Elicit

Ask:
- "What are you unsure about?"
- "Anything you're still figuring out?"
- "What questions do you have that you don't have answers to yet?"

---

## 10. Success Criteria

Claude must discover and record:

| Field | What to Elicit |
|-------|----------------|
| Criteria | How the engineer will know documentation is complete and acceptable |

### How to Elicit

Ask:
- "How will you know we're done?"
- "What would make this documentation successful?"
- "Who needs to approve the final result?"

---

## 11. Confirming PROBLEM

Before producing artifacts, Claude:

1. Summarizes understanding of the task
2. Lists deliverables and key parameters
3. Asks engineer to confirm or adjust

Claude does not proceed to artifact production until PROBLEM is confirmed.

---

## 12. Storing PROBLEM

Claude may:
- Hold PROBLEM in context for immediate use
- Save PROBLEM as a file for reference or multi-session work

---

## 13. For Claude

When producing a PROBLEM:

1. Work through sections 2-10 via conversation
2. Don't present as a form — ask questions naturally
3. Build structure from answers
4. Confirm with engineer before proceeding to artifacts
5. Use PROBLEM + HANDOFF to guide artifact production
