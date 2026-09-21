---
name: create-workflow
description: Create or revise a reusable Chirality workflow through conversation, package it in the intended library, and verify discovery and readiness for reuse.
---
# Create a workflow

Use this method when creating or revising a reusable workflow, including a
request to save a useful plan from ordinary conversation. The result is a
locatable method another person or agent can adapt to a later undertaking.
Choose the reasoning, writing approach, plan, and delegation that suit the work;
a small workflow can be a single file. The human reviews the proposed method
before it is registered for reuse. This method grants no host permissions and
does not require a particular agent roster or Git process.

## Establish purpose and destination

Understand what the workflow should accomplish, when it applies, and what a
useful outcome looks like. Use the conversation and relevant existing methods as
the basis; make consequential assumptions explicit. Distinguish reusable method
from this run's assignment, private facts, credentials, and local paths.

Use the selected library basis and inspect its current descriptor and package
before editing. Registered project-specific methods live at
`<project>/.chirality/workflows/<name>/WORKFLOW.md`; personal methods useful
across projects live at `~/.chirality/workflows/<name>/WORKFLOW.md`. Resolve the actual
project or user root from the available host context. Editing a bundled library
is a separate library-maintenance scope; Root's bundled source is `workflows/`.
Do not infer permission to change an installed bundle from permission to save a
personal or project workflow.

Inspect existing names in the relevant libraries. An unqualified name resolves
project, then user, then bundled; retain the selected source-qualified identity
(`source`, `sourceRootId`, `kind`, `name`). Expose collisions and make an intended
revision or override clear. Preserve the prior revision through the library's
available revision mechanism or an authorized retained copy outside discovery;
do not overwrite unrelated work or silently replace a selected origin. If the
intended existing package is ambiguous, resolve that ambiguity before writing it.

## Write the reusable method

Explain the purpose, outcomes, and applicability in terms useful to a future
reader. Make these facts identifiable, using whatever prose and structure suits
the undertaking:

- Inputs and their source or quality requirements; outputs and where they go.
- Dependencies and the decisions or conditions that determine order, branches,
  iteration, and completion.
- Responsibilities where they affect execution, including who integrates
  contributions if delegation is useful. Respect active roles; TASK does not
  delegate. Name tools only when their availability can be established, and
  provide a practical fallback or limitation when needed.
- Checks that meaningfully establish output quality; treatment of incomplete
  inputs, failed checks, interrupted work, recovery, and handoff.
- Which requirements are essential and which choices a later agent should adapt
  to the domain, scale, risk, and human's purpose.

Keep run-specific scope and permissions in the assignment. Parameterize useful
variation and explain how to supply it, without inventing an exhaustive form.
Carry forward applicable domain constraints and human checkpoints; repository
software-development governance is not a default for general App workflows.
Use examples or supporting resources only when they improve reuse.

## Review before registration

Prepare a draft for the human to inspect and discuss before it enters the
reusable library. In Chirality App, write the proposed package at
`<project>/.chirality/workflow-drafts/<name>/WORKFLOW.md` or
`~/.chirality/workflow-drafts/<name>/WORKFLOW.md`, with its supporting files
inside that draft package. Use ordinary files and directories, without symbolic
or hard links. Ordinary file permissions, including executable helpers, are
preserved on registration; special permission bits are not. Do not write it to
`.chirality/workflows` yet.
The Workflows panel lists these packages under **Ready for review**. Tell the
human where to open the draft; do not claim that it is registered.

The human can read the instructions and included files, choose **Request
changes in chat**, and guide revisions until satisfied. Keep revisions in the
draft location. **Register workflow** publishes the exact reviewed draft; a
changed draft requires another inspection. Existing registered names are not
overwritten by this control: use a distinct name to preserve an existing
workflow. Revision of a registered method is a separate explicit amendment,
with its earlier version preserved and the exact changes accepted before any
replacement. Do not automatically execute the newly registered workflow.

When using another host without these controls, present the complete proposed
instructions and resource inventory through an inspectable file or the
conversation, invite feedback, and wait for explicit acceptance before
registering through the available file tools. A request to create a workflow
is permission to prepare it, not a substitute for reviewing the finished method.

## Package and discover

The package folder and frontmatter `name` must match: 1–64 lowercase letters or
digits in nonempty hyphen-separated segments. `WORKFLOW.md` starts with YAML
frontmatter delimited by complete `---` lines, containing that `name` and a
nonempty `description` that explains when to select the method. The body needs
no prescribed headings or exact prose template.

Optional `execution.json` uses `schema_version: 1` and `compatible_roles`, with
optional `tools` restrictions; consult the selected library's runtime contract
before adding it. Omitting it inherits compatibility; empty restriction lists
deny rather than grant capability. Metadata never proves host enforcement.
Optional resources must resolve inside the package, including through symlinks;
link them at the point of use and load only what the stage needs.

A flat Markdown document is not a discoverable package. For project and personal
libraries, after the reviewed package is registered, re-query the effective workflow
catalog through available host capabilities and inspect its qualified entry.
Do not claim a refresh or successful discovery without observing it. If the
host cannot expose the catalog, report that verification as outstanding.

For an authorized Root bundled-library edit, register the package in
`workflows/catalog.yaml` navigation and regenerate `workflows/index.json` with
`python3 tools/validation/build_workflow_index.py` from that source root.
Central membership is a library-maintenance choice, not a requirement for every
new workflow. Use that library's actual authoring rules; a generated index is
derived from package metadata, not a substitute for it.

## Check and return

Read the saved package back. Check metadata, name, resource containment, links,
and intended source identity using available library validators. Walk through
a representative use, including a plausible failure or interruption, to check
that the inputs, outputs, decisions, and recovery are usable. Scale further
execution checks to the method; distinguish a walkthrough from a real run.

In the Root source tree, useful references are `workflows/README.md`,
`workflows/catalog.schema.json`, `docs/AGENT_WORKFLOW_RUNTIME.md`, and
`tools/workflow_runtime/README.md`. Focused structural checks are
`python3 tools/validation/validate_workflow_metadata.py` and
`python3 tools/validation/build_workflow_index.py --check`. These are Root
source tools, not assumed App tools; use the selected host's actual validation
capabilities for project and personal libraries.

Return the saved absolute path and qualified library identity, what was created
or revised, how to select it again, and what was verified. Distinguish package
validation, observed discovery, and evidence of successful reuse. Name any
remaining limitations, blockers, or rerun needs so another participant can
continue without reconstructing the conversation.
