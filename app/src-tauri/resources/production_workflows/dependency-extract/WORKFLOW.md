---
name: dependency-extract
description: Author or refresh a deliverable's consumer-local needs in deliverable.yaml from its scope, sources and intended use.
metadata:
  kind: instruction
  surface: workflow
---
# Declare local needs

Use this method during setup or when an undertaking changes the inputs a
Deliverable needs. The consumer's responsible contributor states what an input
must support. This includes useful needs formulated from accepted scope and
design, not just phrases that a text scan can extract. A declaration does not
create a producer commitment, supplier appointment, approval or technical waiver.

The result is the current `needs` list in the selected Deliverable's
`deliverable.yaml`, plus a concise return of changes, checks and unresolved
matters. Reverse links and work graphs are derived when needed. ScopeOfWork
remains the commitment and acceptance master; the locality is that scope and
this YAML. This method does not change those authorities, lifecycle or accepted
identities.

TASK may execute one bounded assignment; WORKING_ITEMS or HELPS_HUMANS may do
the same work directly. Do not delegate from TASK. For a multi-Deliverable
undertaking, the coordinator assigns disjoint local write targets and integrates
returns. See the [brief guide](resources/brief.md).

## Establish the locality and purpose

Resolve the project root, selected Deliverable, exact allowed write target and
intended use from the assignment. Read its existing `deliverable.yaml`,
`ScopeOfWork.md`, the code its `code_paths` name and the source
passages needed for this work. Use an identified accepted decomposition or reference index when
needed to confirm identity or resolve a source; do not choose authority by file
mtime. Read another locality or external source only within the authorized read
scope. Do not perform a project-wide census to refresh one consumer.

If the local file is missing, create it only when the assignment authorizes that
write and the stable identity is established. Otherwise return that gap. If the
identity, source meaning or write target is ambiguous, leave the affected part
unchanged and continue independent work. Missing source material
limits the claim of coverage; it does not authorize invented content.

The sole persistent write target is the selected `deliverable.yaml`. Within it,
change only `needs`, apart from supplying an established `id` when creating the
file. Preserve other fields and useful comments. Do not edit producer files,
ScopeOfWork, source originals or decomposition records. Do not
create a second dependency register, hand-maintained reverse links, graph, status table
or routine run history. This is an authoring method, not project migration.

## State each actual need

Use the existing native schema described in
[`tools/deliverables/README.md`](../../tools/deliverables/README.md):

- `from` and nonempty `condition` are required. `from` is an established native
  `DEL-nn-nn` identity, `external:name`, `doc:project-relative-path`,
  `package:id`, or `unknown`. Use the actual supported supplier or source. A
  package reference does not mean every Deliverable in that Package supplies
  the input. Do not invent identities, appointments or a supplier's internal WBS.
- `condition` states what the neighbour observably provides, in the provider's
  product terms, and its actual
  intended use, with material case, maturity, release conditions and technical
  holds. Test it: which acceptance criterion in the provider's scope makes this
  condition true, and could the provider meet all its criteria with this false?
  If none does, the need creates no obligation on the provider; return the gap. Distinguish preliminary use from later issue requirements. State a
  useful condition even when its source binding is unknown; preserve the raw
  source description or unresolved alternatives in that text.
- Optional `when` states the applicability or trigger, such as a material
  finding requiring a response. Preserve conditional needs without making every
  comment or iteration a mandatory revision gate.
- Optional `gating` records the intended coordination-gate classification.
  Preserve an existing classification unless its meaning actually changes.
  `false` never waives a technical condition or means an input is suitable.
  The query tool includes both values in native graphs and does not evaluate
  the classification, `condition` or `when` automatically.

Paths use POSIX separators, stay within the project, and may use a `::` or `#`
locus. Absolute paths and `..` escapes are invalid. A folder's descriptive
suffix is omitted from the numeric YAML `id` binding; the accepted canonical
DeliverableID and metadata remain unchanged. Report an inconsistency rather
than renumbering it.

An ordinary entry is upstream and belongs at the actual consumer. Do not copy
it into the native producer as a downstream mirror. An actual outward
obligation to a nonlocal recipient stays at its native producer with
`direction: downstream` and `gating: false`; in that entry `from` names the
recipient. Preserve the supplier's authorship and the native technical
producer/receiver and routing in the condition. Do not turn allocated supplier
work into native work. Report a discovered need at another native consumer to
that consumer's coordinator rather than writing outside the local boundary.

For example, these are two uses of one source, not duplicate endpoints:

```yaml
id: DEL-01-02
needs:
  - from: DEL-01-01
    condition: Preliminary interface dimensions support the coordination review; final issue dimensions remain required before release.
    when: Preparing the coordination review
    gating: false
  - from: DEL-01-01
    condition: Confirmed interface dimensions and ratings support issue of the affected connection design.
    when: Issuing the affected connection design
```

## Refresh by meaning

Compare proposed needs with existing entries by source, actual input/use, case,
condition, trigger and direction. Preserve separate cases between the same
endpoints. Reuse an unchanged declaration; do not append a duplicate because
another source repeats it, or merge cases merely because `from` matches.

A reference list, shared objective, hierarchy anchor or nearby equipment is not
by itself an execution need. Keep scope and objective traceability in their
existing masters. Formulate a need when the accepted work and intended use
support it; distinguish an uncertain source binding from an unsupported new
requirement. If a proposed condition would alter commitments, criteria or an
explicit hold, return that reserved choice without applying it.

Do not delete, retire or rewrite an existing need because a scan failed to find
its wording. Change or remove it only on evidence that its meaning changed,
was duplicated in full, or no longer applies to the authorized work. Explain the
substantive reason in the return or the existing change review; do not add row
IDs, timestamps, satisfaction states or an append-only history to YAML. An
amended or retired production obligation may still supply an artifact usable
for a particular condition; assess the actual input/use rather than retargeting
or deleting all affected needs automatically. Do not remove a need for being
met, because it still states what the Deliverable relies on. Add `when` where
the source states when the need applies.

## Save, check and return

Read the saved YAML back and apply the [local checks](resources/checks.md).
Use the existing native query tool where available and authorized; its Git,
HEAD and read-scope requirements, limits and direct-inspection fallback are in
the [tool guide](resources/tools.md). A tool failure is a finding, not a reason
to drop declarations or switch persistence formats. Repair ordinary local
format errors within the boundary; leave disputed meaning unchanged.

On interruption, compare the saved file with the authorized change and current
sources before resuming. Repeating an unchanged refresh must leave the needs
unchanged. Return the actual file, meaningful additions/changes/removals and
reasons, source coverage, checks performed and unresolved conditions or source
bindings. Report partial work plainly.
