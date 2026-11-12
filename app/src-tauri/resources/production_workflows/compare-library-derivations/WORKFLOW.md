---
name: compare-library-derivations
description: Compare selected Library-derived project files with their actual sources and discuss which differences to retain, change or propose upstream.
metadata:
  kind: instruction
  surface: workflow
---
# Compare Library derivations

Compare selected Library-derived project documents when adopting a Library
release or when explicitly selected. The undertaking identifies the files and
target basis. Either the project's Agent 0 or the coordinator runs the comparison
under actual authority; the project's Agent 0 carries edits and integration.

## Map the sources

Identify the current project files, the target Library edition or exact
candidate revision, and any prior reconciled edition. Check
[`metadata.upstream`](../../docs/document-metadata.md#library-derivation)
against the actual sources and adoption evidence, or establish the mapping
where the field is absent.

Adapted `AGENTS.md` and `init-prompt.md` map to relevant
sections of [project-entry](../project-setup/resources/project-entry.md).
An adapted workflow maps to its actual Library source and needed resources.
Roles and methods consumed directly from the Library are resolved at their
selected basis. Product packaging and separately pinned assets retain their
own comparison and adoption routes.

## Compare and discuss

Compare the prior Library source, current project adaptation and target
Library source together. Read upstream changes alongside local differences,
following corresponding subjects where a template spans several project files.
Examine meaning, authority, links and required resources, including source moves.

Without a prior baseline, compare the current adaptation with the target and
state that historical change attribution is unavailable. A full comparison can
establish a fresh reconciliation basis. Where mapping or source content is
unavailable, identify the gap and continue the comparisons it permits.

For each consequential difference, discuss its evidence, practical effect and
project reason. Settle whether to keep it local, change it locally, propose a
reusable improvement upstream, or leave it unresolved. Deliberate adaptations
can remain. Send upstream candidates to Library Agent 0 with the bounded
problem, source basis, proposed change and consequences.

## Reconcile and return

Apply agreed edits within the undertaking's authority and run the project's
proportionate document, link and metadata checks. During adoption, add
`metadata.upstream` for the documents actually reconciled. Add or advance the
field only after the whole adapted document is reconciled against
the applicable source content of the recorded published edition, consequential
differences have justified dispositions, and required edits are present and
checked. Retained local adaptations permit advancement. After partial comparison
or unresolved applicability, leave the field unchanged; omit it where no
justified source/edition pair exists. If a candidate revision was examined,
check its final published source before recording that edition.

Return the compared files and exact bases, material differences and reasons,
dispositions, edits or proposals, checks and remaining decisions in the existing
conversation, PR or Work location. For an incomplete comparison, identify the
usable result, unexamined bounds, missing inputs, next action and actor.
