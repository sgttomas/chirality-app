# SKILL TEMPLATE

Use this template when creating a new repo-native skill under `skills/`.

Skill contracts conform to the design outcomes specified in `AGENT_HELPS_HUMANS.md` (Type 0) under its "Design Outcomes for Skill Contracts" section and compliance requirements R10 + R12. `AGENT_SKILLMAKER.md` (Type 1 manager) owns skill contract evolution and subsystem governance. New skills must pass `tools/validation/validate_skill_metadata.py`.

## `SKILL.md`

```md
---
name: <skill-name>
description: <what the skill does and when to use it>
compatibility: <optional; shell/profile compatibility note>
allowed-tools: <optional; comma-space delimited command specs — see format below>
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: <NONE or profile token>
---

# SKILL — <skill-name>

## Purpose
What recurring bounded task this skill supports.

## Suitable agent shells
- TASK
- <optional profile constraints>

## Inputs
- Required:
  - <field>
- Optional:
  - <field>

## Runtime overrides
- <KEY>: meaning, default, allowed values

## Tool usage
- Preferred tools:
  - tools/<path>
- Optional tools:
  - tools/<path>
- Disallowed tools:
  - <tool or class of tool>

## Outputs
- <artifact>

## Non-negotiable constraints
- <constraint>

## QA expectations
- <check>
```

## `BRIEF_SCHEMA.md`

**Required.** Every skill must include this file.

This is the dispatch contract — what the orchestrator must provide in the INIT-TASK brief to invoke this skill through TASK. When TASK loads a skill via `TaskSkill`, it also loads `BRIEF_SCHEMA.md`.

Document:
- required brief fields (with types, defaults, examples)
- optional fields
- `RuntimeOverrides` guidance (what each override means, allowed values)
- recommended `CustomInstructions` content for format-critical defense-in-depth (format reminders, completion checklists, canonical output references)
- `CustomInstructions` carry run-specific reinforcement; they do not replace skill hydration. The contract in `SKILL.md` remains authoritative.

## `TOOL_POLICY.md`

**Required.** Every skill must include this file. Implicit tool assumptions are a design defect (see `AGENT_HELPS_HUMANS.md` Design Outcomes for Skill Contracts).

Use these canonical section headings (exact-string-match; case-sensitive):

H2 headings:
- `## Preferred tool order`
- `## Allowed deterministic tools`
- `## Expected use of reasoning`
- `## Disallowed use`
- `## Write boundary`

H3 subheadings under `## Allowed deterministic tools`:
- `### TASK-enforced` — tools from the `allowed-tools` frontmatter; enforced by TASK shell at load time
- `### Operationally invoked` — tools named in `## Tool usage` body; agent-guided, not TASK-enforced

Content floor: `## Allowed deterministic tools` (with both H3 subsections), `## Disallowed use`, and `## Write boundary` must be present on every skill. `## Preferred tool order` and `## Expected use of reasoning` may be skipped when no content applies.

## `QA_CHECKS.md`

**Required.** Every skill must include this file.

Document:
- minimum output validity checks
- failure reporting expectations
- any required evidence or logs

## `allowed-tools` format

The `allowed-tools` frontmatter field is machine-consumed by TASK during skill resolution. It must follow this canonical format exactly:

- Comma-space (`, `) delimited list of command specs
- Each spec: `<interpreter> <repo-relative-tool-path>:<scope_glob>`
- No flags, no extra arguments, no commas inside a spec
- `<interpreter>` is a single token (e.g., `python3`)
- `<repo-relative-tool-path>` is a single token relative to repo root (e.g., `tools/validation/scan_deliverable_consistency.py`)
- `<scope_glob>` follows the final `:` (e.g., `*`)

Example (single tool):
```
allowed-tools: python3 tools/validation/scan_deliverable_consistency.py:*
```

Example (multiple tools):
```
allowed-tools: python3 tools/pdf2md/rasterize_pdf.py:*, python3 tools/pdf2md/postprocess_page.py:*
```

If `allowed-tools` is malformed, TASK will reject the skill with an error. Omit the field entirely if the skill has no deterministic tool requirements.

## Naming

- Folder name should be the `TaskSkill` token used in briefs.
- `name` frontmatter should match the folder name.
- Prefer lowercase ASCII folder names using letters, digits, and hyphens only, e.g. `pdf2md`, `requirement-extract`, `table-reflow`.

## Validation

After creating or updating a skill, run:

```sh
python3 tools/validation/validate_skill_metadata.py skills
```

This checks all skill folders under `skills/`. It does not target one named skill unless you point it at a narrower root yourself.
