---
name: document-metadata
description: Document metadata.
metadata:
  kind: instruction
  surface: reference
---
# Document metadata

When typing a maintained Markdown document, begin with YAML frontmatter:

```yaml
---
name: project-entry
description: Establish a project's bootstrap, standing instructions and operating entry.
metadata:
  kind: instruction
  surface: reference
---
```

Use a stable lowercase identifier with hyphen-separated words, at most 64
characters, and a one-line description of purpose. For workflow and skill
entrypoints, retain the package name and existing description. Preserve existing
package-specific keys, including `metadata.applicability` where used. Validate
frontmatter against [the schema](document-metadata.schema.json).

Choose `metadata.kind` for the document's principal use:

| Kind | Use |
| --- | --- |
| `instruction` | Direct action under the applicable authority |
| `explanation` | Develop an account, definition or interpretation |
| `example` | Illustrate a case or arrangement |
| `proposal` | Present a change for decision |
| `historical-source` | Preserve an earlier source for identified uses |

Choose `metadata.surface` for its place in the project:

| Surface | Document home or contribution |
| --- | --- |
| `bootstrap` | `init-prompt.md` |
| `standing` | `AGENTS.md` |
| `operating-entry` | A retained `loop/LOOP_INIT.md`; the entry now lives in `AGENTS.md` |
| `role` | `agents/AGENT_*.md` |
| `workflow` | `WORKFLOW.md` |
| `skill` | `SKILL.md` |
| `tool` | Tool-use README |
| `reference` | Publications, explanations and supporting references |
| `requirements` | Product requirements |

Classify the document as a whole; retain distinctions within its body where it
contains examples, quoted sources or proposed changes. Keep status, date and
revision out of frontmatter; use Git for change history and resolved revisions
with dependent results. Preserve dated evidence and source citations in the
body when their meaning requires them.

Put the header above the `<init-prompt>` block. Paste only the block to start a
session. Keep `CLAUDE.md` exactly `@AGENTS.md`. Maintain execution declarations
with `deliverable.yaml` and the ScopeOfWork schema. Preserve frozen snapshots
and retained historical edition bytes at their selected source identities.

When adding metadata to a published source, keep its body and anchors stable.
Exclude the YAML header from rendered prose and regenerate affected derivatives
with the complete source fingerprint. Regenerate consumed workflow indexes when
package metadata changes. Consumers select revisions and adopt changes through
[their own route](../README.md#obtain-and-use-the-library).

## Library derivation

A project document adapted from a Library source may record that relationship
with optional `metadata.upstream`:

```yaml
metadata:
  kind: instruction
  surface: standing
  upstream:
    source: workflows/project-setup/resources/project-entry.md
    edition: library-v3.2.1
```

The example is illustrative. `source` is the repository-root-relative Library
source-file path. `edition` is the published Library edition against which the
adapted document was last reconciled. It is not the document's own version,
the project's overall Library selection, or a claim of identical content.
Deliberate local adaptations may remain after reconciliation.

Adapted project `AGENTS.md` and `init-prompt.md` use
`workflows/project-setup/resources/project-entry.md` as their source, with its
relevant sections. An adapted workflow uses its actual Library source file.
A matching filename does not establish derivation.

Both members are required when `upstream` is present. Omit the object where
there is no established Library derivation or justified reconciliation edition.
Canonical Library source documents need no upstream field. The Library's own
project entry documents are template adaptations like those of other projects.
Do not infer a baseline from the current Library selection or latest release. This object records one
source relationship, not a general reference or copy inventory.

Schema validation checks structure and edition-tag spelling. Inspect the
published edition to establish source identity and the correct mapping; the
schema cannot prove that the edition exists or reconciliation occurred.
Use [Compare Library derivations](../workflows/compare-library-derivations/WORKFLOW.md)
when the undertaking selects comparison and discussion. Add or advance the
field only after the whole adapted document has been reconciled against the
applicable content of that published source edition under project authority.
A partial comparison or a newer project-wide Library selection does not
advance it automatically.
