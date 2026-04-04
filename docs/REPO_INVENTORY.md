# Repository Inventory

This document is the **single canonical place** where mutable repository counts are maintained.

If another document needs to mention how many agents, skills, or tools the project currently has, it should reference this file rather than restating the number inline.

---

## Counting Rules

### Agents

- Count the **indexed agent suite** listed in [`AGENTS.md`](../AGENTS.md).
- Include only roles present in the Type 0, Type 1, and Type 2 tables.
- Exclude templates, deprecated files, experiments, and unindexed `AGENT_*.md` documents.

### Skills

- Count **repo-native skills** as immediate subfolders under [`skills/`](../skills/) that contain `SKILL.md`.

### Tools

- Count **registered deterministic tools** listed in [`tools/REGISTRY.md`](../tools/REGISTRY.md).
- Exclude backlog items and unregistered utility scripts.

---

## Current Counts

| Category | Count | Canonical Source |
|---|---:|---|
| Indexed agents | 44 | [`AGENTS.md`](../AGENTS.md) |
| Repo-native skills | 3 | [`skills/`](../skills/) |
| Registered deterministic tools | 55 | [`tools/REGISTRY.md`](../tools/REGISTRY.md) |

---

## Discovery Guidance

This file is for aggregate governed counts only. It is not the place to enumerate the members of those sets.

Use these sources for discovery:

- Indexed agents: [`AGENTS.md`](../AGENTS.md)
- Repo-native skills: inspect [`skills/`](../skills/) directly using the folder rule defined in [`skills/README.md`](../skills/README.md)
- Registered deterministic tools: [`tools/REGISTRY.md`](../tools/REGISTRY.md)

When canonical indexes and live filesystem contents differ:

- use the canonical index first for governed membership and official inclusion
- use the live filesystem second for current local presence and file contents
- surface the discrepancy explicitly rather than silently reconciling it

---

## Update Policy

Update this file when any of the following change:

- the indexed agent suite in [`AGENTS.md`](../AGENTS.md)
- the set of repo-native skills under [`skills/`](../skills/)
- the registered toolset in [`tools/REGISTRY.md`](../tools/REGISTRY.md)

The thesis and other narrative docs should reference this file instead of embedding these counts directly.
