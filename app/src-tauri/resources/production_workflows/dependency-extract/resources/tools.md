# Native query support

Use the current `tools.deliverables` library when available. From its repository
root, with Python 3 and PyYAML, the relevant commands are:

```sh
python3 -m tools.deliverables --project <project> check
python3 -m tools.deliverables --project <project> neighborhood DEL-01-02
python3 -m tools.deliverables --project <project> impact DEL-01-02
```

Pass `<project>` explicitly; the shared-library CLI requires `--project`.
The project must be an existing
directory within the current Git repository, and that repository must have a
resolvable `HEAD`. When the library is supplied through `PYTHONPATH`, run from
the target Git repository with the same project/HEAD prerequisites. A new or
non-Git workspace is not required to initialize Git merely to use this method.

Every command loads all `deliverable.yaml` files beneath the selected project
and observes referenced path presence, even for a single neighbourhood or impact
query. Use it only when those reads are authorized. Otherwise inspect the
selected YAML and relevant source/target declarations directly. Follow only
connections needed for the assignment; if reverse-link coverage or structural
validation is incomplete, say so. This fallback uses the same local source of
truth, with no alternate persistence format or graph authority.

The CLI prints JSON and writes nothing. Its basis names HEAD and observed
working-tree changes. `check` rejects malformed YAML, duplicate keys/identities,
invalid identities, disagreement with a containing folder that names a DEL
identity, downstream native Deliverable mirrors and escaping paths with exit 2,
retaining any usable partial result. The folder check accepts a descriptive
suffix; it does not establish agreement with the accepted decomposition.
Missing source declarations, unresolved/external references, planned paths and
cycles can still return exit 0. `needs` retains case multiplicity;
`neighborhood` separates local outward entries as `outputs` from inputs.

Reported cycles contain native Deliverables only, using native upstream links;
external, document and package references and downstream entries are outside
that cycle projection. Both gating and non-gating native links participate.
`impact` likewise follows native consumers, including non-gating links. Neither
query evaluates `condition`, `when` or suitability, executes referenced checks,
or verifies an evidence locus. Presence means only presence. A missing
supplier declaration is an unresolved reference; an external/outward entry's
unknown presence is not an unmet-input verdict.

Read [the library reference](../../../tools/deliverables/README.md) for other
queries. Do not invoke migration or older CSV validators as a substitute for
local authoring. Tool absence, unsupported identity or Git failure belongs in
the return with the inspection actually performed; it grants no authority to
renumber accepted work or discard a need.
