---
name: audit-dep-closure
description: Inspect consumer-local deliverable.yaml needs and derive bounded dependency findings without changing declarations or evaluating readiness.
metadata:
  kind: instruction
  surface: workflow
---
# Inspect local dependency declarations

Use this read-only method for a concrete structural or coordination question:
checking selected declarations, examining a neighbourhood, or identifying
consumers affected by a change. The sources are consumer-local
`deliverable.yaml` needs. Reverse links and graphs are generated views, not a
second dependency authority. The workflow name does not imply that conditions
are closed or that a project DAG must be accepted.

TASK returns a bounded contribution to its caller. The assignment supplies the
project root, question, selected Deliverables or change, authorized read scope
and any accepted inventory needed for the requested coverage claim. Read
relevant ScopeOfWork or source evidence only as the question requires.
This method changes no files and requires no snapshot folder, pointer, run
record, central graph, lifecycle transition or acceptance checkpoint. Return
findings in the conversation or the caller's existing review.

## Resolve scope and available support

Establish which localities and references the question covers. Use an explicit
accepted identity basis when checking agreement or missing localities; do not
select authority by file mtime or silently normalize accepted identities.
The presence of YAML files alone is not an independent inventory of expected
Deliverables. If an inventory was not supplied or authorized, describe coverage
as the declarations inspected rather than claiming all expected work is present.

Use `tools.deliverables` when available, with Python 3 and PyYAML:

```sh
python3 -m tools.deliverables --project <project> check
python3 -m tools.deliverables --project <project> neighborhood DEL-01-02
python3 -m tools.deliverables --project <project> impact DEL-01-02
```

Run from the library's repository root, or use the supplied library on
`PYTHONPATH` from the target repository. Resolve `<project>` explicitly rather
than relying on the App v4 default. The selected project must be an existing
directory within that Git repository; every command requires a resolvable
`HEAD`. The reported basis is HEAD plus observed working-tree changes, while
the declarations are read from the current working files.

All commands load every `deliverable.yaml` beneath the selected project and
observe referenced path presence, including for a single neighbourhood query.
Use them only within the authorized read scope. When the tool, Git/HEAD or the
wider read permission is unavailable, directly inspect the selected YAML and
relevant source/target declarations. Follow only necessary connections; report
limits on reverse-link coverage and structural checking. Do not initialize Git,
migrate artifacts or invoke a different persistence method merely to run this
query. Tool details are in
[`tools/deliverables/README.md`](../../tools/deliverables/README.md).

## Inspect facts before topology

Start with parse errors, duplicate identities, invalid targets or paths and
missing declarations. `check` reports structural errors with exit 2 and may
return usable partial results. Exit 0 also permits unresolved suppliers,
external references, missing paths and cycles. It is not an adequacy verdict.
A malformed file is excluded from usable parsed declarations; disclose the
resulting coverage limit before interpreting the graph.

For each material finding, cite the actual file and `needs[index]`, or its exact
source locus, and preserve `from`, `condition`, `when`, `gating` and direction.
Indices identify the inspected file version, not permanent row identities.
Distinguish:

- A native source declaration absent from the inspected project, an existing
  source outside a bounded direct-inspection scope, and a source not yet bound
  (`from: unknown`). Do not merge these into one missing-input conclusion.
- External or package references whose availability is unassessed, document
  path presence, and actual outward obligations (`direction: downstream`). An
  outward entry belongs to its native producer and is an output, not an unmet
  input to that producer.
- Distinct uses, maturity conditions or triggers between the same endpoints.
  A topology projection may collapse endpoints; the underlying cases and their
  multiplicity remain part of the finding.

`check` verifies YAML shape and supported identities/paths, rejects downstream
native Deliverable mirrors, and checks `id` agreement when the containing
folder names a DEL identity, including a descriptive suffix. It does not check
ScopeOfWork completeness, accepted decomposition agreement or whether a need
covers the actual intended use. Compare those sources directly only when the
question calls for it. An empty list is structurally possible and makes no
completeness claim. Do not require hierarchy anchors as dependencies.

## Interpret the selected view

`neighborhood` separates direct inputs, outward `outputs` and derived consumers.
`impact` follows native consumers transitively, including non-gating links; it
is a relevance view rather than an execution-order or change-obligation verdict.
Read the actual consumer conditions before recommending further work.

The CLI's cycle projection contains native Deliverables and upstream native
links only. External, document and package references and downstream entries
remain in the local declarations but are outside that projection. Both gating
and non-gating native links participate. Report reciprocal relationships with
their actual cases and uses; a mutual design relationship can represent staged
information or iteration. Do not remove directions, force acyclicity, change
`gating`, or route every cycle into a separate case-resolution procedure.

The tool does not automatically evaluate `condition`, `when` or `gating`, run
referenced checks, verify evidence loci or establish supplier availability.
Suitability remains unknown in its output. A present declaration, path, merged
change or successful query cannot establish an input's adequacy, completion,
acceptance, engineering release or readiness. `gating: false` does not waive an
actual technical condition. Name a specific unresolved input/use before
recommending that dependent work wait; preserve technical holds and reserved
owner decisions.

When sequencing is the actual question, return the relevant conditions for
[`construct-local-work-graph`](../construct-local-work-graph/WORKFLOW.md) to
assess in that undertaking. Do not add an accepted-DAG currency check or make a
project graph an ordinary prerequisite to work.

## Return the bounded result

State the question and selected scope, files or query basis actually inspected,
commands and outcomes where used, findings with local evidence, unavailable
coverage and any specific unresolved choices. Separate structural faults from
unresolved references and from conditions requiring technical judgment. Return
partial findings when inputs fail; do not reinterpret omitted declarations as
no dependencies.

On interruption or a changed source, reread the affected declaration and rerun
only the query needed to resolve the remaining question. Generated views are
replaceable and need not be committed. Repairs to declarations belong in a
separately authorized local authoring assignment, using
[`dependency-extract`](../dependency-extract/WORKFLOW.md). This read-only audit
does not silently repair meaning or establish closure by writing a report.
