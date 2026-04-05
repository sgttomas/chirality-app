# Skills — Task Method Packs

This folder contains **repo-native skills**: reusable method packs that a bounded Type 2 agent may load at runtime.

Skills are **not agents**. They do not have their own decision rights, write scopes, or interaction surfaces. A skill is a method bundle that tells an agent:

- what task shape it is for,
- which tools are preferred or allowed,
- what runtime overrides matter,
- what outputs should exist,
- and how to QA the run.

The canonical loader for these skills is [`AGENT_TASK.md`](../agents/AGENT_TASK.md).

**Governed by:** SKILLMAKER (Type 1, `agents/AGENT_SKILLMAKER.md`), operating under the Type 0 standard `AGENT_HELPS_HUMANS.md` which governs workflow-component design across agents, skills, and tools. SKILLMAKER owns skill design, contract evolution, and subsystem governance; its outcomes conform to HELPS_HUMANS R10 + R12 and the "Design Outcomes for Skill Contracts" section.

## Why skills exist

Use a new skill when:
- the role stays the same,
- the write scope stays the same,
- the interaction model stays the same,
- but the **method** and **toolchain** vary.

Do **not** create a new agent just because a bounded task has a different tool recipe.

## Precedence

When a skill is loaded by `TASK`, precedence is:

1. Human instructions in the run brief
2. `TASK` shell hard boundaries
3. Active task profile (if any)
4. Skill contract
5. Skill defaults

A skill must never widen scope beyond what the agent shell and brief allow.

## Folder contract

Each skill lives in its own folder:

```text
skills/
  <skill_name>/
    SKILL.md           # required; YAML frontmatter + Markdown body
    BRIEF_SCHEMA.md    # optional but recommended
    TOOL_POLICY.md     # required
    QA_CHECKS.md       # optional but recommended
```

Optional extras are allowed, such as:
- `examples/`
- `notes/`
- helper templates used by humans while drafting run briefs

## Required contents of `SKILL.md`

Every `SKILL.md` should state:

- YAML frontmatter with at least:
  - `name`
  - `description`
- purpose and suitable task shapes
- required inputs
- optional runtime overrides
- output expectations
- whether the skill is safe for generic `TASK`
- any important non-negotiable constraints

The frontmatter is the portable discovery surface. The Markdown body is the Chirality execution guidance. `TOOL_POLICY.md` is a required Chirality-specific companion file; `BRIEF_SCHEMA.md` and `QA_CHECKS.md` are recommended Chirality-specific extensions layered on top of that core.

## Relationship to tools

Skills may reference deterministic tools under `tools/`, but should do so by **policy**, not by hidden assumption.

Good skill design makes tool usage explicit:
- preferred tools
- disallowed tools
- when to fall back from tools to manual/LLM reasoning

## Relationship to task profiles

Profiles and skills are orthogonal:

- **Task profile** = structural specialization of the agent
- **Skill** = method pack for a recurring task shape

Example:
- `TaskProfile: DELIVERABLE_TASK`
- `TaskSkill: deliverable-consistency`

or:
- no profile
- `TaskSkill: pdf2md`

Current example:
- `deliverable-consistency` should normally begin with `tools/validation/scan_deliverable_consistency.py`, then read only the flagged files and nearby context.

## Discovery guidance

Treat `skills/` as a live skill root rather than relying on hard-coded skill lists in narrative documents.

Agent guidance:
- Treat each immediate subfolder of `skills/` that contains `SKILL.md` as one repo-native skill.
- Read this file first for the shared contract.
- When a specific skill is requested, inspect that skill folder directly:
  - `SKILL.md`
  - `BRIEF_SCHEMA.md` if present
  - `TOOL_POLICY.md`
  - `QA_CHECKS.md` if present
- Use [`docs/REPO_INVENTORY.md`](../docs/REPO_INVENTORY.md) for canonical aggregate counts, not skill membership details.
- Do not assume any other document's embedded skill list is current.
- If live folder contents and a canonical index disagree, surface the discrepancy explicitly.

## Authoring rule of thumb

If a human or persona agent can say:

> "Run `TASK` with this skill, this scope, and these tool permissions"

and the run is well-bounded and auditable, it should probably be a skill, not a new top-level agent.

## Naming note

For new skills, use a `TaskSkill` token that matches the skill folder and `name` frontmatter exactly. Prefer lowercase letters, digits, and hyphens only.

## Validation

Run the deterministic validator after adding or renaming skills:

```sh
python3 tools/validation/validate_skill_metadata.py skills
```

This validator scans every immediate skill folder under `skills/`, not any one skill in particular. For example, it validates both `skills/pdf2md/` and `skills/deliverable-consistency/` using the same rules.

It validates both the basic authoring contract (`name`, `description`, folder alignment, required `TOOL_POLICY.md` presence) and the machine-consumed runtime contract (`metadata.chirality-*`, canonical `allowed-tools` syntax, and tool-path resolution under `tools/`).
