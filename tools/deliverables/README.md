# Deliverable queries

Run from the selected Git repository with Python 3 and PyYAML. The repository
must have a resolvable `HEAD`; `--project` names an existing directory within it
and defaults to `projects/chirality-app-v4`:

```sh
python3 -m tools.deliverables --project projects/example check
python3 -m tools.deliverables --project projects/example neighborhood DEL-01-01
python3 -m tools.deliverables --project projects/example impact DEL-01-01
python3 -m tools.deliverables --project projects/example touches HEAD
python3 -m tools.deliverables --project projects/example dag-diff baseline-tag
```

Output is JSON; queries write nothing. The basis names HEAD and observed
working-tree changes. Every relationship cites its source file and need index.
Metadata can live in flat deliverable folders or package phase folders; no move
or migration is performed. Without the CLI, PyYAML, Git or HEAD, inspect the
relevant declarations and source evidence directly and state the query limit.

## Consumer-local declarations

`deliverable.yaml` requires `id` and a `needs` list. The `id` uses the numeric
DEL prefix for dependency binding; an accepted suffix-bearing PROJECT identity
and its metadata remain unchanged. A named DEL folder and that YAML binding
must agree. Optional `name`, `code_paths` and `checks`
describe the deliverable; paths and globs are project-relative. For example:

```yaml
id: DEL-01-01
needs:
  - from: DEL-02-01
    condition: Interface dimensions checked for the selected operating case.
    when: Before issuing the affected drawing.
    evidence: execution/PKG-01/DEL-01-01/Work/interface.md#basis
  - from: unknown
    condition: Identify the source of the equipment rating before its use.
  - from: external:recipient
    direction: downstream
    gating: false
    condition: Provide the agreed interface drawing for recipient review.
```

Every need has `from` and nonempty `condition`. Optional fields are `when`,
`gating` (boolean), and `evidence` (a project-relative path with an optional
section reference). Suppliers are local `DEL-nn-nn` IDs, `external:name`,
`doc:path`, `package:id`, or `unknown`. Preserve case, use, maturity and technical
holds in the condition and trigger. Distinct needs between the same endpoints
remain distinct declarations. `needs: []` means none declared yet; it is no
claim that the deliverable has no needs or that the set is complete.

Generic paths use the shared `Work/` convention. Follow the selected project's
adopted locality spelling, including App v4 and Piping's existing `Design/`.
Queries do not select, detect or migrate between locality folder names.

The consumer states native upstream needs; reverse links are generated. A
producer-local `direction: downstream` is available for an actual obligation to
a nonlocal recipient, not a second native consumer list. It is listed as an
output, not a required input. A consumer declaration does not create supplier
scope or approval authority. Authoring and refresh use `dependency-extract`;
existing declarations are changed for their meaning, never retired merely
because a source scan did not rediscover them.

## Observation limits

`neighborhood` shows direct inputs, outward obligations and native consumers.
`impact` follows native consumers transitively, including non-gating links.
`check` rejects malformed YAML, duplicate keys/IDs, identity disagreement,
invalid targets and escaping paths. Missing suppliers, planned paths and cycles
are observations with exit 0; malformed input returns exit 2 and any usable
partial result. Reported cycles contain present native DEL nodes only, include
non-gating relationships, and exclude external/outward/unknown targets. They
are not a complete project graph or execution-blocker verdict.

`gating` is retained as a declared distinction for an undertaking's judgment;
these queries neither filter by it nor evaluate its condition. A present path
or supplier declaration establishes presence only. Suitability remains unknown.
Queries never mark completion, treat a merge as acceptance, run referenced
checks, lift technical holds, or infer readiness from lifecycle. Assess the
actual condition for its intended use with evidence and appropriate checks.

`touches` matches Git diff paths against code paths and deliverable localities;
several deliverables may match. A single revision selects that commit's change
against its first parent (the empty tree for a root commit), regardless of
working-tree edits; explicit ranges are used as supplied. `PR:number` or a
GitHub PR URL requires authenticated `gh` and resolves base/head commits, then
diffs `base...head` locally. Both commits must be present; a missing commit is
an error, not a partial file list. This explicit network-capable selection is
not needed for local queries. Unmapped paths remain visible. On PRs,
`governance-harness` reports relevance and unmapped paths without failing its job.

`dag-diff` compares declarations at a supplied Git revision with working files,
preserving condition fields and multiplicity. Its name does not establish a
central DAG authority, accepted baseline, acyclicity or condition satisfaction.
No CSV/Markdown dependency register, central currency record, migration adapter
or lifecycle state is read or written by this method.
