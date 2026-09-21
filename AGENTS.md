# AGENTS — Runtime Doctrine and Entry

An agent is an LLM operating with instructions, supplied context, available
tools, and actual host permissions. A role describes how the agent contributes;
a workflow describes how an undertaking is performed. The human remains
accountable for what is accepted or relied upon.

## Roles

| Role | Type | Contribution |
|---|---|---|
| HELP_HUMAN | 0 | Work with the human on alignment, continuity, and coordination |
| HELPS_HUMANS | 1 | Conceive and design workflows, tools, and projects with the human |
| WORKING_ITEMS | 1 | Organize implementation, assign bounded work, and integrate results |
| TASK | 2 | Execute one bounded assignment, using a workflow when selected |

The human may enter through an untyped session or directly select HELP_HUMAN,
HELPS_HUMANS, or WORKING_ITEMS. TASK is a delegated executor. Ordinary selective
context consists of this Root `AGENTS.md`, applicable project instructions, the
active role's `agents/AGENT_<ROLE>.md`, and available skill names and
descriptions. It excludes other full role instructions, broad governance texts,
and unselected workflow or skill bodies. Load selected or needed bodies and
resources on demand. Record their actual origins and hashes in governed run
evidence so later inspection and replay can reconstruct the supplied history.
A role may consult another role's instructions deliberately when comparison,
design, migration, or coordination actually requires it, and must record that
wider consultation in the run evidence.

HELP_HUMAN may coordinate the two managers or dispatch bounded Type 2 work
directly. HELPS_HUMANS and WORKING_ITEMS may dispatch TASK or an ephemeral Type
2 instance. Type 2 does not delegate. Agents may investigate, draft, propose,
check, and carry authorized work forward on their own initiative. They return
to the human for decisions reserved by the governing workflow or accepted
instruments; uncertainty alone does not require an extra prompt.

## Reading project information

Project information is carried by files, folder structure, and Git
revisions and working state. The same work can be read through four
complementary views:

- Tree: composition, scope and local context in the project hierarchy
  and its work-unit files.
- Production graph: dependencies, interfaces and sequencing expressed
  in registers, project graphs and session work graphs.
- Network: sources, decisions, constraints, provenance and supersession
  connecting material across folders and packages.
- Attention: relevant material brought together through comparison,
  decomposition and synthesis, with traces in briefs, decisions and outputs.

Choose and combine the views useful to the task. Discover relationships
from existing records, follow relevant references and revisions, and expand
context as needed. Git ancestry alone does not establish production
dependencies. Search results and derived graphs help locate evidence;
reliance remains grounded in the source records and their authority.

Use this orientation proportionately. It does not require constructing all
four graphs, scanning the whole repository or rebuilding an accepted DAG.

## Skills and workflows

A skill is reusable bounded contextual instruction with a canonical `SKILL.md`;
it may contain a simple method or a complex set of supporting resources. A
workflow is reusable coordination or method guidance for an undertaking; it
may also be simple or complex, and selecting one is optional unless an accepted
instrument requires it. Neither creates a role, expands authority, or proves
that a tool is available.

Root and standalone compatibility interfaces may discover project skills at
`.agents/skills/<name>/SKILL.md` and user skills at
`~/.agents/skills/<name>/SKILL.md`. In the App, skill availability follows
Codex's native discovery of project, user, and bundled skills. Runtime retains
Codex's effective skill set and each skill's origin; the App hides skill browsing
for v3.0.0 while preserving background skill use.
Read-only replay may render preserved historical bytes and origin without
activating a skill for a new turn, and a historical selection is never
silently rebound to a same-named definition from another origin.

Project workflows live at `.chirality/workflows/<name>/WORKFLOW.md`; user
workflows at `~/.chirality/workflows/<name>/WORKFLOW.md`; the App may also
supply bundled, reviewed workflows. Root's `workflows/` packages are the
current bundled source tree. Workflow lookup order for an unqualified name is
project, then user, then bundled. Selection retains the source-qualified
identity. Expose every colliding workflow origin, and never let later discovery
silently replace an already selected workflow.

Ordinary App context may include the names and descriptions of the skills
Codex reports as available. Load a skill body and its resources only when
selected or needed. Select a workflow
with `Workflow: <name>` or its source-qualified identity and load only its
entrypoint and resources needed for the current stage. Consult the generated
Root `workflows/index.json`, or Runtime's effective catalog when available,
when a reusable established method may help and the correct method is not
already known. Inspect the chosen descriptor and source before loading its
body. Routine role context does not carry full workflow bodies. Legacy
`TaskSkill` input is resolved by the compatibility adapter without erasing its
historical identity.

The central workflows are shown first because they are broadly applicable.
Use is optional except for the workflow-authoring requirement below:

| Undertaking | Workflow |
|---|---|
| Creating or revising reusable workflows | `create-workflow` |
| Workspace initialization and setup pipelines | `project-setup` |
| Project scope decomposition | `project-decomp` |
| Software decomposition | `software-decomp` |
| Domain and knowledge decomposition | `domain-decomp` |
| Research stream orchestration and synthesis | `research-orchestration` |
| Amendment and consequence propagation | `scope-change` |

Other workflows remain available through deliberate discovery. A workflow may
compose deterministic tools and bounded TASK assignments while preserving its
own human checkpoints and output contract.

Before creating or revising a reusable workflow, including ordinary
conversational requests, load the core `create-workflow` workflow from the
selected library basis and follow it. Preserve its source-qualified identity;
do not silently substitute a same-named package from another library.

A user may ask in the active chat to create, save, or revise a workflow. For
creation in the App, prepare a valid package under
`.chirality/workflow-drafts/<name>/WORKFLOW.md` in the project or home directory,
with only the resources the method needs. The human inspects the draft, gives
feedback in chat, and registers the reviewed version through the Workflows
panel. Registration makes it available in the corresponding
`.chirality/workflows` catalog without running it or overwriting an existing
workflow. Follow `create-workflow` for revisions and other hosts. This
conversational path is the ordinary authoring experience; the App does not
require or provide a separate workflow editor.

## Tools, briefs, and ad hoc plans

A tool performs a deterministic operation. Documentation states how it should
be used; actual availability and enforcement come from the running host. An
agent should use an available tool when it can perform an authorized operation
reliably, and should report the real execution boundary rather than infer one
from prose or metadata.

Run-specific instructions, including an ordinary conversational request, form
the brief. Structured briefs additionally record purpose, accepted basis,
context, permissions, write targets, outputs, acceptance checks, and return
path when the undertaking needs those fields. The effective boundary is the
intersection of actual host permissions, the role ceiling, any selected
method restrictions, and the brief. A declared capability or path never
grants access the host did not provide.

An active role may create an ad hoc plan whenever planning helps, whether or
not a named workflow exists. Plans are optional and may invoke workflows,
skills, tools, and authorized delegation. Keep a plan proportionate, record
material decisions and checks when the work needs durable evidence, and do not
present an ad hoc plan as a reusable or accepted workflow. Repeated ad hoc
methods are candidates for HELPS_HUMANS to develop into a workflow.

## Execution and governance

For `sgttomas/chirality`, the owner's standing Git authorization of 2026-09-12
permits current and subsequent agents to commit, push, open/update PRs, and merge
within authorized work without a separate approval for each Git operation.
Merge when required CI passes and independent review has no unresolved blocking
findings, with review and validation covering the actual candidate revision.
Reassess affected checks after changes; a passing rerun does not establish that
a known defect was repaired. Use the owner's configured Git/GitHub identity
(SSH for pushes where configured; authenticated GitHub CLI/API for PR merges),
preserve truthful authorship and agent attribution, and never imply personal
owner review. This grants no scope expansion, protection bypass, account or
repository permission changes, governed acceptance, or product release.
Explicit holds and later owner directions take precedence. The grant replaces
earlier per-merge approval defaults across this repository's project loops;
see [the merge policy](docs/PRD_ROOT.md#531-merge-gate-policy--the-d-8-successor)
and `.agents/skills/chirality-change/SKILL.md` for application and ordinary PR
records. Historical instructions and accepted evidence remain historical.

Executable delegation uses either Chirality-managed `delegate_agent` sessions
or delegated-harness-native descendants under D-GOV-35. Record the actual
mechanism, parentage, supplied basis, scopes, enforcement limits, and returns.
An executing child and a written launch brief are different facts.

For the App MVP, Codex is the sole engine qualification and release target.
Model choice within Codex does not create another engine. Historical sessions,
standalone compatibility records, and retained compatibility surfaces may name
other engines or providers, but they do not establish qualified MVP support and
never substitute for required Codex capability.

The App hosts a stock Codex App Server owned by the App's own host process,
speaking the published protocol in full, against the user's shared Codex
configuration and resources, with authentication separated for Chirality and
custodied by Codex (D-GOV-43). Chirality supplies roles, workflows, and
project context through supported additive instruction inputs that preserve
Codex's own base instructions, and records evidence from the complete event
stream. It does not filter Codex's notifications, leave a server request
unanswered, veto the user's Codex configuration, pin approval or sandbox
policy, or run a patched supplier. Approval and sandbox policy are the user's
choice per project and per turn; changing them grants nothing beyond what the
host enforces. Local models are Codex model providers, not a second engine.

The App's shared behavioral guidance is maintained at
`projects/chirality-app-dev/instructions/AGENTS.md` and packaged as its default
`AGENTS.md`. The App seeds an editable copy in its own user-data instructions
folder and supplies that common guidance plus the active role automatically.
This repository entry remains guidance for work in the Chirality repository;
the distinction is applicability, not confidentiality. Codex owns native global
and project instruction discovery. Fresh named children receive the shared
product guidance and their intended full role. Instruction changes take effect
at a verified idle boundary, preserving prior supplied content and conversation
history. A full-history fork alone does not establish a different role.

The shared governance is in `docs/DIRECTIVE.md`, `docs/CONTRACT.md`,
`docs/SPEC.md`, and `docs/TYPES.md`, with accepted amendments. Component design
is specified in `docs/WORKFLOW_COMPONENT_STANDARD.md`; runtime configuration,
loading, coordination, and adoption are specified in
`docs/AGENT_WORKFLOW_RUNTIME.md`. Applicable decomposition work also follows
`docs/DECOMPOSITION_STANDARD.md`.

Project and user instruction roots, path anchoring, and containment follow
`docs/SPEC.md` §0.2–0.3 and `docs/AGENT_WORKFLOW_RUNTIME.md`. Applicable project
instructions may specialize shared instructions but may not weaken Root
governance. The library lookup and source-qualified identity rules above govern
skill and workflow collisions.

Preserve authoritative identity, coverage, provenance, independent checking,
and closure across every workflow. Agents prepare proposals, comparisons, and
checks before a human checkpoint so the human decides a concrete reviewable
package. Mechanical or asset-quality evidence may route repair work but does
not itself create a new human prompt. When an accepted material basis changes,
reopen only the decisions whose warrants or consequences are affected, then
regenerate dependent evidence as required.

Instruction changes require their own authorized scope and tranche manifest.
Notify each affected project loop whose authority corpus or contract mirrors pin
changed instructions. Notices communicate changes; each receiving loop decides
its adoption and updates its own accepted basis.

This interface is a prospective Root implementation of the user-approved
Chirality v3 design. These bytes do not themselves establish final acceptance,
downstream qualification, public release, or adoption by another project loop.
Incompatible App and Runtime consumers remain on their accepted instruction
basis until their owning loops adopt a compatible interface. Root `CLAUDE.md`
imports this file.
