# Skills — Task Method Packs

This folder contains **repo-native skills**: reusable method packs that a bounded Type 2 agent may load at runtime.

Skills are **not agents**. They do not have their own decision rights, write scopes, or interaction surfaces. A skill is a method bundle that tells an agent:

- what task shape it is for,
- which tools are preferred or allowed,
- what runtime overrides matter,
- what outputs should exist,
- and how to QA the run.

The canonical loader for these skills is [`AGENT_TASK.md`](../agents/AGENT_TASK.md).

**Governed by:** HELPS_HUMANS (Type 1, `agents/AGENT_HELPS_HUMANS.md`), operating under `docs/WORKFLOW_COMPONENT_STANDARD.md`, which governs workflow-component design across agents, skills, tools, briefs, and workflow packages. HELPS_HUMANS owns skill design, contract evolution, and subsystem governance; its outcomes conform to standard R10 + R12 and §11.

## Why skills exist

Use a new skill when:
- the role stays the same,
- write authority is supplied by the bounded TASK brief,
- the interaction model stays the same,
- but the **method** and **toolchain** vary.

Do **not** create a new agent just because a bounded task has a different tool recipe.

## Precedence

When a skill is loaded by `TASK`, precedence is:

1. Human instructions in the run brief
2. `TASK` shell hard authorization boundary
3. Skill contract
4. Skill defaults

A skill must never widen write authority beyond what the TASK shell and effective bounded task brief allow.

## Skill dispatch and hydration

When a persona agent dispatches a TASK with `TaskSkill`, TASK automatically loads the skill's `SKILL.md` and companion files. This is the skill hydration guarantee — the worker gets the full contract without the orchestrator needing to reconstruct it in the dispatch prompt.

The authority split between companion files:
- **`SKILL.md`** — the authoritative method and output contract (extraction rules, format specs, canonical templates, non-negotiable constraints).
- **`BRIEF_SCHEMA.md`** — the dispatch contract (what the orchestrator must provide in the INIT-TASK brief to invoke this skill through TASK).
- **`TOOL_POLICY.md`** — the tool allowlist and preferences.
- **`QA_CHECKS.md`** — output validity checks.

The orchestrator provides runtime parameters via `RuntimeOverrides` and optional run-specific reinforcement via `CustomInstructions`. It does not duplicate the skill contract. See `docs/WORKFLOW_COMPONENT_STANDARD.md` §11.

## Folder contract

Each skill lives in its own folder:

```text
skills/
  <skill_name>/
    SKILL.md           # required; YAML frontmatter + Markdown body
    BRIEF_SCHEMA.md    # required; dispatch contract for TASK invocation
    TOOL_POLICY.md     # required
    QA_CHECKS.md       # required
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

The frontmatter is the portable discovery surface. The Markdown body is the Chirality execution guidance. `BRIEF_SCHEMA.md`, `TOOL_POLICY.md`, and `QA_CHECKS.md` are required Chirality-specific companion files layered on top of that core.

## Relationship to tools

Skills may reference deterministic tools under `tools/`, but should do so by **policy**, not by hidden assumption.

Good skill design makes tool usage explicit:
- preferred tools
- disallowed tools
- when to fall back from tools to manual/LLM reasoning

## Relationship to task briefs

Briefs and skills are orthogonal:

- **Brief** = run-specific authority, scope inputs, write permissions, overrides, and expected outputs
- **Skill** = method pack for a recurring task shape

Example:
- `ScopePath: /abs/path/to/deliverable`
- `RuntimeOverrides.DELIVERABLE_PATH: /abs/path/to/deliverable`
- `TaskSkill: deliverable-consistency`
- `ApplyEdits: false`

or:
- `ScopePath: /abs/path/to/pdf-work-dir`
- `TaskSkill: pdf2md`

The `metadata.chirality-task-profile` frontmatter field remains part of the repo metadata contract for compatibility and should normally be `NONE`. Non-`NONE` values are deprecated compatibility metadata, not write-scope grants.

Current example:
- `deliverable-consistency` should normally begin with `tools/validation/scan_deliverable_consistency.py`, then read only the flagged files and nearby context.

PDF2MD example:
- `PDF2MD` dispatches `TASK + pdf2md-page` for text transcription and, when `ASSET_MODE=prose`, dispatches `TASK + pdf2md-page-assets` for page-bounded figure/table/image discovery. Deterministic tools then materialize crops/CSVs, anchor page Markdown, aggregate the public asset manifest, and validate references.

Publication example:
- `DBM_PUBLISHER` first runs deterministic section mapping and section context packet generation, then dispatches `TASK + dbm-section-publish` once per approved publication section with its read-only context packet, then dispatches `TASK + dbm-publish` for package assembly, knowledge coverage/open-items records, and content adequacy. After assembly, `TASK + dbm-postauthor-concordance` builds a post-authoring evidence bundle using shared review-substrate tools and agent judgment to prepare candidate findings for human disposition. Optionally, `TASK + dbm-concordance-verify` provides semantic cross-section consistency observations. All DBM publication skills remain publication-local and should be confined to `_Publication/DBM/` scopes rather than mutating KTY-local truth.

Review example:
- `WORKING_ITEMS` dispatches `TASK + dbm-draft-review` to review a human-prepared draft DBM against the governed knowledge base. The skill runs deterministic substrate tools (`scan_section_coverage.py`, `extract_claims.py`, `scan_tbd_markers.py`, `check_body_thinness.py`) then uses agent judgment to compare the substrate against governed truth (KA artifacts, section map, publication rules, supersession state) and prepare candidate findings. The human dispositions findings through the REVIEW agent.

Software example:
- `WORKING_ITEMS` activates the project-local `software-workflow.json`, then dispatches `TASK` with one of `software-repository-reconnaissance`, `software-bounded-implementation`, `software-defect-diagnosis`, `software-test-planning`, or `software-code-review`. The skill carries the reasoning method; `tools/software_workflow/` discovers surfaces, selects and runs registered checks, validates write scope, compares structured contracts, and detects generated-file drift. See `docs/SOFTWARE_WORKFLOW_PROFILE.md`.

Legacy skills:
- `dbm-concordance-seed` — marked `chirality-skill-status: LEGACY`; no longer dispatched by DBM_PUBLISHER. Concordance has moved from pre-authoring gate to post-authoring evidence bundle review.

Active PROJECT/SOFTWARE production skill:
- `scope-of-work` — supports explicit `INIT`, `CONVERT`, and `VERIFY` modes for
  `SOW_V1`. Conversion is lossless, lifecycle-neutral, and confined to an
  exactly authorized isolated workspace. `four-documents` remains supported
  only for existing `LEGACY_FOUR_DOC` compatibility through rollback.

## Discovery guidance

Treat `skills/` as a live skill root rather than relying on hard-coded skill lists in narrative documents.

Agent guidance:
- Treat each immediate subfolder of `skills/` that contains `SKILL.md` as one repo-native skill.
- Read this file first for the shared contract.
- When a specific skill is requested, inspect that skill folder directly:
  - `SKILL.md`
  - `BRIEF_SCHEMA.md`
  - `TOOL_POLICY.md`
  - `QA_CHECKS.md`
- Use the live `skills/` folder rule above for skill counts; use [`AGENTS.md`](../AGENTS.md) and [`tools/REGISTRY.md`](../tools/REGISTRY.md) for agent and tool indexes.
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
