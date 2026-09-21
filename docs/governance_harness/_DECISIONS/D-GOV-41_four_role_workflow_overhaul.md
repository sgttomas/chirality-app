# D-GOV-41 — Four-role agent and workflow overhaul

Status: OWNER-DIRECTED CANDIDATE IMPLEMENTATION — adoption/publication pending
Date: 2026-09-09
FramedBy: HELPS_HUMANS under HELP_HUMAN, FOUR_ROLE_OVERHAUL_20260909
AcceptedBasis: main@533332349a4607eee561d4ef90fb05a62d86519e
CandidateSHA: TBD
PublicationSHA: TBD
EffectiveSHA: TBD

## Recorded direction and boundary

The owner directed **“PLEASE IMPLEMENT THIS PLAN:”**, supplying the complete
“Four-role agent and workflow overhaul” plan in the Codex conversation. The
implementation brief is recorded in
`execution/_Coordination/AgentRuns/FOUR_ROLE_OVERHAUL_20260909/ACCEPTED_PLAN.md`;
SHA-256 `2df68af79712fb945e7b482ba88ba5585e53c1c757345bc3bcddd69d1e57ca10`.
That file is a labeled summary, not a substituted verbatim ruling or approval
of unknown future bytes. The original direction authorizes candidate Root
implementation and coordination notices. Merge, effective adoption, and
receiving-loop acceptance remain their owning human acts.

The preceding design discussion explicitly accepted the four roles, workflows
as rich methods, selected-only loading, Root-first implementation, a stripped
format with incompatible-consumer adoption hold, and a small coordinated team.
The owner removed experimental behavioral trials as a prerequisite. The
implementation tests fidelity and interface correctness.

## Prospective amendment

1. **Roles.** Retain HELP_HUMAN (0), HELPS_HUMANS and WORKING_ITEMS (1), and
   TASK (2). Human direct entry remains available through 0 or either 1.
   Type 2 is TASK or an ephemeral bounded executor; neither delegates.
   Existing subject-specific roles are retired with their methods and
   relationships carried into workflows or deterministic tools.
2. **Instruction format.** Role prose contains PROTOCOL, SPEC, STRUCTURE,
   RATIONALE. Runtime metadata moves to `agents/registry.json`; specialized
   execution configuration goes into optional workflow `execution.json`.
   Run briefs continue to bind actual context, permissions, scope, and returns.
3. **Workflow model.** `workflows/<name>/WORKFLOW.md` replaces the repository's
   skill package model. Workflows may branch, iterate, coordinate, and serve
   multiple compatible roles. They are explicitly selected and loaded by stage.
   `Workflow` replaces `TaskSkill` for new assignments; historical-input
   compatibility preserves matching selections and rejects conflicts.
4. **Design and implementation.** HELPS_HUMANS develops workflows, tools, and
   projects with the human. WORKING_ITEMS carries any explicitly bounded
   undertaking into implementation. Package/deliverable assignments keep their
   governing structure and boundaries. A workflow supplies a method without
   granting a new role, delegation, permission, or human decision right.
5. **Migration.** Relocate all 45 existing method packages and account for all
   34 role packages. The accepted mapping produces 71 workflow entrypoints.
   Preserve historical snapshots, accepted records, existing legacy status,
   human gates, artifact contracts, and independent review. Replace callers,
   validators, builders, and live references with the new relationships.
   The user subsequently directed omission of NEXT_INSTANCE_PROMPT.md and
   NEXT_INSTANCE_STATE.md contracts from workflow descriptions and resources;
   their original text remains historical evidence, with an explicit omission
   in the disposition ledger.
6. **Adoption.** Root publishes a coherent candidate contract and stages
   distribution changes. App and Runtime product implementations are outside
   this tranche. Incompatible consumers keep accepted instruction bases until
   their owning loops adopt the registry/loading interfaces together. Route
   notices to affected corpus/mirror owners; no automatic repin or release.

## Supersession scope

On effective Root adoption this instrument prospectively supersedes:

- D-GOV-10/11/13/14's component and named-role requirements only to the extent
  that they require the former roster, dedicated Type 2 packages, compulsory
  skill companions, prose runtime metadata, or root-embedded dispatch catalog.
- D-GOV-14's exact component-standard edition with this tranche's successor
  `WORKFLOW_COMPONENT_STANDARD.md`; unchanged authority, provenance, evidence,
  containment, human decisions, and accepted-state requirements remain.
- `CONTRACT.md` K-AGENTS-1's placement/catalog requirements; `SPEC.md` §0.2.1
  instruction-surface enumeration and §9 role-file/configuration contracts;
  `TYPES.md` §4 role/construction and undertaking vocabulary; related
  `DIRECTIVE.md` current-facing component and delegation descriptions.
- The current-facing registry interpretation of PRD_ROOT O-1/O-5. Historical
  transcription rows and their provenance remain unchanged.
- Earlier audit proposals' recommendations to retain additional durable roles;
  their source evidence and findings remain available.

D-GOV-35's two executable delegation classes remain. Scope containment, sealed
briefs, capability bounds, M2/G4, M3 frozen run bases, M6 notices, and human
acceptance rules remain. The registry states managed role eligibility and does
not invent native enforcement. Root historical product status and independent
Runtime/App authority instruments are unchanged.

## Application and assurance

The tranche manifest records authorization, integration ownership, changed
instruction surfaces, and notice routing. The run source manifest freezes the
original role/standard basis; candidate role hashes identify fresh-run adoption.
WORKING_ITEMS supplies disposition coverage, resolver and tool tests, required
Root checks, independent review, and final handoff. Hashes of final candidate
artifacts are evidence of exact content; they are not human acceptance.

Until the requisite merge/adoption act, this record and amended source files
are the authorized candidate. There is no effective-SHA assertion, downstream
adoption, lifecycle transition, or public-release claim.
