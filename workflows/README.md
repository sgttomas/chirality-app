# Workflows

A workflow describes how to carry an undertaking through: its methods, decisions,
relationships, artifacts, and recovery. It can branch, iterate, and coordinate
several contributions. Agents bring the role; workflows bring the method; a brief
binds both to the present work.

## Select and load

Select explicitly with `Workflow: <name>`. The inventory is the immediate
subdirectories containing `WORKFLOW.md`. Discover names when needed; routine role
context loads no workflow catalog or bodies.

Resolve a selected workflow from any working directory:

```bash
python3 "$INSTRUCTION_ROOT/tools/workflow_runtime/resolve_workflow.py"   --root "$INSTRUCTION_ROOT" --role TASK --workflow audit-decomp
```

Supply `--resource CONTRACT.md` or another package-relative resource only when the
current stage needs it. The resolver returns selected context and fingerprints.
A workflow can be omitted for an assignment expressed entirely through its brief.

WORKING_ITEMS owns orchestration. TASK performs a bounded contribution, including
a separately specified stage of a larger workflow. HELPS_HUMANS can use a
compatible workflow while developing the design. Loading a method grants no
additional capabilities or decision rights.

## Package form and catalog

Each bundled package has canonical YAML metadata in the frontmatter of
`workflows/<name>/WORKFLOW.md`. Its `name` and `description` combine with the
compatible roles and restrictions in `execution.json`; the index generator
enumerates the package's contained resources. Optional resources hold detailed
contracts, templates, examples, or helpers. Package resources must remain
inside the package after real-path resolution.

`workflows/catalog.yaml` contains the bundled library identity and the ordered
set of central workflows shown by selectors. `workflows/index.json` is
generated from package metadata with
`python3 tools/validation/build_workflow_index.py`. Consumers use the index or
parse the canonical frontmatter and execution metadata themselves; Root's Python command is an
authoring and validation tool, not a production parser.

Optional `execution.json` provides compatible roles and capability/command
restrictions. Stage-specific resources are selected explicitly without changing
role compatibility. See
[the runtime contract](../docs/AGENT_WORKFLOW_RUNTIME.md). A command is invoked
through the available session tools, against the declared tool root. A documented
operation does not imply that the host exposes or enforces it.

## Compatibility and maintenance

`TaskSkill: <name>` remains a legacy input spelling only for names explicitly
mapped in [the converted-method ledger](legacy-methods.json). Supplying both
fields with different selections fails. [The legacy agent map](legacy-agents.json)
resolves retired names to the executing role and workflow or deterministic
audit tool; those names are not additional roles. Unconverted legacy methods
remain historical and are never inferred from files or prose.

Method libraries may exist at project, user, and bundled scope. Resolution uses
that precedence order. Identity is the complete tuple `source`, `sourceRootId`,
`kind`, and `name`; `sourceRootId` identifies the actual library root. Catalogs
expose every qualified collision and the selected candidate. A malformed
higher-precedence package blocks that unqualified identity instead of falling
through. Project files such as a flat `WORKFLOW.md` outside a package with
canonical metadata are documents only and never become discoverable methods.

Existing package names and legacy status survive this migration. In particular,
`dbm-concordance-seed` remains legacy; `four-documents` serves legacy production
compatibility while `scope-of-work` carries the current SOW_V1 method. Historical
briefs, snapshots, and pinned evidence retain their original identifiers.

HELPS_HUMANS helps develop or revise workflows; WORKING_ITEMS coordinates their
implementation. Validate a package with the Root workflow validator and review
whether its particular method, outputs, and recovery fit its intended use.

The Root replacement format is held for adoption by incompatible App and Runtime
consumers. Their owning loops must adopt the registry and loading contract before
using these files as their runtime basis. Export staging is not a release.
