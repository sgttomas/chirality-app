# Root workflow runtime utilities

`agents/registry.json` declares the four roles. `resolve_workflow.py` resolves
ordered method selections, legacy compatibility fields, and requested
resources; it does not preload the library or launch an agent. App and Runtime
adoption remains a separate owning-loop decision.

```sh
python3 /declared/instruction/root/tools/workflow_runtime/resolve_workflow.py \
  --root /declared/instruction/root --role TASK --workflow domain-documents \
  --resource resources/brief.md --policy /authorized/run/policy.json
```

The JSON result includes the role, selected definition and resources with
SHA-256 hashes, execution configuration, effective tools, and absolute tool
paths. `TaskSkill` is accepted through `--task-skill`; its historical underscore
spelling resolves to hyphens. Both it and an unqualified legacy `Workflow` name
consume `workflows/legacy-methods.json`. Equal resolved identities resolve
once; genuinely different identities conflict; an unknown `TaskSkill` alias
fails. A source-qualified `Workflow` identity explicitly preserves its
historical workflow and bypasses alias conversion. `--method` accepts ordered
JSON references or source-qualified identities; distinct ordered methods stay
ordered. Results record original fields, mapping decisions, normalized methods,
and fully qualified resolved identities separately. `--legacy-agent` reads the
explicit legacy-agent map and preserves its historical workflow route.

A package's `compatible_roles` applies to the whole method. TASK receives a
bounded child workflow or a brief. Resources are selected explicitly through
repeatable `--resource` when exactly one method is selected; omitted resources
are not read. Missing resources, escaping symlinks, unsupported qualified
origins, unknown legacy aliases, and incompatible roles fail resolution.

## Policy composition and tools

`--policy` accepts an object with optional `host`, `brief`, and `bindings`
objects. Host and brief tool objects may independently declare `capabilities`
and `commands`. Execution companions provide the workflow restriction.
Capability lists intersect. Omitted restrictions inherit; an empty list denies.
Command policy is returned as `effective_tools.commands.all_of`: every layer
must permit an operation, with alternatives inside each layer. This preserves
scope intersections without pretending one glob can represent every overlap.

Command expressions retain `<interpreter> tools/path:<scope_glob>`. Bindings
supply explicit placeholder values, such as `scope_path`. Missing bindings
fail. `resolved_commands` provides absolute tool paths rooted at `--root`,
independently from the working directory. `command_allowed` evaluates declared
interpreter, tool and target claims against each layer. The host must determine
and enforce actual command effects; this helper is not a process or filesystem
sandbox. Capabilities and command expressions are different policy domains.

## Structured brief compatibility

`--brief brief.json --repo-root /active/checkout` normalizes structured inline
fields and an optional structured `INIT-TASK.md`. The latter may be a YAML
mapping or YAML frontmatter. Free prose needs interpretation into these fields
by the caller; the utility does not infer authorization from prose.

`InitTaskPath`/`INIT_TASK_PATH` explicitly selects the file; otherwise the
normalizer checks `ScopePath/INIT-TASK.md` and then the legacy
`DeliverablePath/INIT-TASK.md`. File values fill omitted inline fields. Inline
values take precedence, while disagreeing path fields or aliases fail.
`DeliverablePath` supplies the context anchor only when `ScopePath` is absent.
`TaskProfile: DELIVERABLE_TASK` remains a compatibility label with no additional
method or permissions; unsupported profiles fail.

`REPO_ROOT`, `INSTRUCTION_ROOT` and `WORKING_ROOT` tokens resolve independently.
The runtime supplies the active checkout and instruction root. An explicit
working root must remain in that checkout; otherwise the nearest project or
domain containing the concrete context anchor supplies it, with the checkout
root as the root-governance fallback. CWD does not choose the working root.
Scope must exist within that root. Write targets are explicit, contained paths
or patterns; symlink escapes fail. `ApplyEdits: false` (also the structured
adapter default) yields no writable targets. A scope or profile never grants
writes. For prose briefs, the caller first makes authorized targets explicit.

`AllowedTools`, when supplied to the structured adapter, uses full command
expressions and narrows the brief policy. Native capability restrictions are
provided separately in `--policy`. Hosts must also enforce explicit write
targets and the role's write ceiling. HELP_HUMAN remains read-only.

## Returns and source basis

Freeze the supplied role, workflow/resources, normalized brief and configuration
hashes at launch. Resolver input hashes mechanically record what this tool read;
they do not prove the host delivered that context to a model. Record the host's
actual context evidence separately. Adopt revised instructions between runs.

Keep successful completion, partial completion, blocked input, failed execution,
and the subject's acceptance verdict distinct. Return output paths and evidence,
resolved selections and policies, checks performed, unresolved questions, and
rerun requirements. Run records require an authorized destination like other
writes. A read-only executor returns its evidence to the caller's authorized
recorder. Companion resources are loaded when selected, with their paths and
hashes recorded; none is mandatory merely because older skill packages required
three companion files.
