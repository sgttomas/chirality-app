# Document Discovery Policy Plan

## Status

Reference. Not yet adopted as active documentation policy.

## Role

Policy Input

## Relationship

This note is a candidate policy basis for future documentation-governance updates. It is not currently the active implementation focus.

This note captures a proposed documentation policy and a small example patch
set before any actual edits are made.

## Purpose

Reduce maintenance drift in repository documentation by avoiding repeated
exhaustive lists of mutable repository contents when those lists are not
themselves the governed fact.

The central idea is:

- keep exhaustive maintained lists only where completeness is itself the point
- elsewhere, provide orientation plus discovery instructions

This is intended to improve both:

- documentation maintainability
- agent behavior in a changing repository

---

## Core Distinction

The proposal distinguishes between two documentation types.

### 1. Canonical indexes

These are documents whose purpose is to enumerate and govern a set of items.

Examples in the current repo:

- [`AGENTS.md`](/Users/ryan/ai-env/projects/chirality-app/AGENTS.md)
- [`tools/REGISTRY.md`](/Users/ryan/ai-env/projects/chirality-app/tools/REGISTRY.md)
- [`docs/REPO_INVENTORY.md`](/Users/ryan/ai-env/projects/chirality-app/docs/REPO_INVENTORY.md)

These may remain exhaustive.

### 2. Orientation documents

These are documents whose purpose is to explain structure, authority, and
discovery method.

These should generally avoid restating mutable exhaustive lists.

Instead they should:

1. orient the reader to the matter at hand
2. identify what is authoritative
3. instruct the agent or operator how to inspect live contents
4. explain what to do if live contents and canonical indexes disagree

---

## Proposed Policy

## Rule 1 — Exhaustive lists only where completeness is the purpose

A document should contain an exhaustive maintained list only when the list
itself is part of the document's governing role.

Good candidates:

- canonical indexes
- formal suite inventories
- release snapshots
- explicit allowlists / denylists

Poor candidates:

- overview notes
- onboarding docs
- narrative architecture explanations
- folder-orientation docs
- policy notes that only need to explain how discovery should work

## Rule 2 — Orientation docs should describe discovery, not duplicate inventory

When a document refers to a mutable folder or subsystem, prefer this pattern:

1. explain what the folder is for
2. identify the rule or canonical source that determines membership
3. explain what to read first
4. explain which canonical index governs it, if any
5. instruct the agent to inspect the live folder contents directly
6. require surfacing discrepancies rather than silently reconciling them

## Rule 3 — Distinguish authority from runtime reality

When canonical indexes and live filesystem contents differ, the agent should
not silently smooth over the difference.

Recommended rule:

- use the canonical index first when the question is governed membership,
  official inclusion, or allowed use
- use the live filesystem second when the question is what files or contents
  are physically present right now
- inspect live files for contents, implementation details, and current local
  state only after membership or authority has been established
- explicitly surface mismatches between the two

For governed sets such as indexed agents or registered tools, the live
filesystem should not silently override the canonical index.

## Rule 4 — Prefer one canonical place for mutable counts

Mutable counts of agents, skills, and tools should not be repeated across
multiple narrative documents.

Those counts should live in one canonical place and be referenced from
elsewhere.

This rule has already been partly implemented through:

- [`docs/REPO_INVENTORY.md`](/Users/ryan/ai-env/projects/chirality-app/docs/REPO_INVENTORY.md)

## Rule 5 — Prefer “how to inspect” language over “here is the list” language

Instead of:

- “The skills folder currently contains A, B, C”

Prefer:

- “Treat each immediate subfolder of `skills/` containing `SKILL.md` as one
  skill”
- “Read `skills/README.md` first”
- “Inspect the specific skill folder directly”
- “Do not assume hard-coded lists in this document are current”

---

## Why This Policy Is Worth Considering

### 1. It reduces drift

Repeated embedded lists become stale quickly.

### 2. It matches agentic operation better

Agents can inspect live folder contents cheaply and should often do so.

### 3. It clarifies governance

This policy makes it easier to distinguish:

- official indexed membership
- current filesystem contents
- orientation prose

### 4. It reduces maintenance burden

One canonical index plus many orientation docs is easier to maintain than many
semi-indexes.

---

## Proposed Agent Guidance Pattern

When describing a mutable folder, use wording like this:

- identify the folder's role
- say what immediate entries count
- identify the authoritative index or rule
- say what to read first
- instruct the agent to inspect the live folder directly
- require surfacing discrepancies

Template pattern:

```md
The `<folder>/` directory contains <role description>.

Agent guidance:
- Use <canonical source or membership rule> to determine what officially
  counts.
- Read <orientation or canonical file> first.
- Inspect the relevant folder or files directly after authority or membership
  has been established.
- Do not assume any hard-coded list in this document is current.
- If live contents and canonical indexes disagree, surface the discrepancy.
```

---

## Example Patch Set (Proposal Only)

The following are example edits that were proposed conceptually but are **not
applied** by this plan.

## 1. `skills/README.md`

### Intent

Keep it as an orientation document rather than a semi-index.

### Example change

Add a section like:

```md
## Discovery guidance

Treat `skills/` as a live skill root rather than relying on hard-coded lists
in narrative documents.

Agent guidance:

- Treat each immediate subfolder of `skills/` that contains `SKILL.md` as one
  repo-native skill.
- Read this file first for the shared contract.
- When a specific skill is requested, inspect that skill folder directly:
  - `SKILL.md`
  - `BRIEF_SCHEMA.md` if present
  - `TOOL_POLICY.md` if present
- `QA_CHECKS.md` if present
- Do not assume any other document's embedded skill list is current.
- If the live folder contents and a canonical index disagree, surface the
  discrepancy explicitly.
```

This folder-shape rule should be treated as the operative discovery rule only
while no separate canonical skill index exists.

### Why

This improves the file as an orientation contract and avoids turning it into a
second skill inventory.

## 2. `docs/REPO_INVENTORY.md`

### Intent

Keep it focused on counts, not membership enumeration.

### Example change

Add a section like:

```md
## Discovery Guidance

This file is for aggregate counts only. It is not the place to enumerate the
members of those sets.

Use these sources for discovery:

- for the governed agent suite: `AGENTS.md`
- for repo-native skills: inspect immediate subfolders of `skills/` that
  contain `SKILL.md`, unless a future canonical skill index supersedes that
  folder-shape rule
- for registered deterministic tools: `tools/REGISTRY.md`

If another document needs the exact members of one of these sets, it should
point to the canonical source above rather than restating the members inline.
```

### Why

This clarifies that the inventory file is about aggregate governed counts, not
about duplicating governed indexes.

## 3. `docs/thesis/appendix_b_agent_inventory.md`

### Intent

Preserve it as a canonical exhaustive appendix while making its role explicit.

### Example change

Adjust the introduction so it states:

- this appendix is a canonical governed inventory
- mutable aggregate counts are maintained separately in
  `docs/REPO_INVENTORY.md`
- narrative docs should reference this appendix or `AGENTS.md` rather than
  restating suite membership inline

### Why

This clarifies that not every document should try to act like this appendix.

---

## Proposed Adoption Strategy

If this policy is adopted, the recommended sequence is:

1. adopt the policy note itself
2. apply the pattern to one or two low-risk orientation docs first
3. review adjacent docs for repeated mutable enumeration
4. preserve exhaustive lists only in canonical indexes and intentional
   inventory appendices

Recommended first targets:

1. [`skills/README.md`](/Users/ryan/ai-env/projects/chirality-app/skills/README.md)
2. [`docs/REPO_INVENTORY.md`](/Users/ryan/ai-env/projects/chirality-app/docs/REPO_INVENTORY.md)

Optional later targets:

3. selected thesis orientation passages
4. folder-orientation notes under `plans/` or future docs

---

## Acceptance Criteria For Future Adoption

The policy will be considered well adopted when:

1. orientation docs stop duplicating mutable folder membership lists
2. canonical indexes remain clearly identified
3. canonical indexes remain exhaustive where completeness is part of their
   governing role
4. orientation docs do not redefine governed membership rules
5. agents are instructed how to inspect live contents directly
6. discrepancy handling is explicit rather than implicit
7. mutable counts remain centralized instead of being restated in narrative
   docs

---

## Short Summary

The proposed documentation pattern is:

- one canonical index where completeness matters
- many orientation documents that explain discovery instead of duplicating
  inventory

This should reduce drift, improve agent behavior, and make the governance
boundary between “official membership” and “live folder contents” much
clearer.
