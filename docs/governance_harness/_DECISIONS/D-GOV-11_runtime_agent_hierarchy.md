# D-GOV-11 — Runtime agent hierarchy and role ownership

Status:       RULED
HumanRuling:  Runtime hierarchy and role ownership approved by owner (Ryan Tufts), 2026-07-11
Ruling SHA:   de20b4ea57ae8889880ed650fb3980fccb5a9245
Date:         2026-07-11
FramedBy:     owner review of the D-GOV-10 candidate workflow-component architecture

## Ruling

The owner approved the following runtime semantics and implementation plan:

1. An agent is operationally an LLM supplied with instructions, declared
   files/context, tools, and permissions. Agent 0/1/2 identify runtime
   delegation positions; standards are external constraints, not agents.
2. HELP_HUMAN is the sole canonical Agent 0, named the Supervising Architect.
3. Agent 1 managers remain valid direct human entry points and may also operate
   under Agent 0 supervision.
4. Agent 2 has three lawful construction forms:
   - TASK plus skill and brief;
   - ephemeral bounded generalist plus sealed brief; or
   - dedicated specialist instruction package approved after proposal.
5. Runtime delegation is hierarchical. Many-to-many coordination occurs
   through governed filesystem artifacts, accepted snapshots, dependencies,
   and Git state.
6. HELPS_HUMANS remains Agent 1 and absorbs SKILLMAKER, TOOLMAKER,
   CONTEXT_TRANSPOSE, and the conversational design portion of DECOMP_BASE.
7. EVALUATION remains Agent 1 and absorbs the prior RECONCILIATION audit,
   coherence, toolbelt, validation, and decision-interface responsibilities.
8. RECONCILIATION is recreated as the Agent 1 manager for deliverable-corpus
   concordance against accepted project state, objectives, implementation and
   verification evidence, artifacts, lifecycle state, and Remaining work.
9. PDF2MD and DRAWING_EXTRACT remain Agent 1 because human input is required
   to establish source-specific targets, schemas, review posture, and recovery
   behavior before repetitive execution can proceed.
10. Root `AGENTS.md` carries the operative doctrine. Root `CLAUDE.md` contains
    only `@AGENTS.md`.
11. Instruction/governance changes precede runtime changes. The new
    RECONCILIATION contract consumes stable handoffs from both active
    concordance lanes; the runtime bridge follows rebase after those lanes
    land.

## Supersession

This record supersedes D-GOV-10 wherever D-GOV-10:

- treats Agent 0/1/2 as document-authority categories;
- leaves HELP_HUMAN as Agent 1;
- treats TASK as the exclusive Agent 2 construction form;
- merges EVALUATION into RECONCILIATION; or
- leaves the former DECOMP_BASE document as a live standard-agent instead of extracting its normative content.

D-GOV-10 remains in force for the standard/persona separation, routine Git
closeout semantics, component requalification, isolated implementation lane,
and staged compatibility-safe migration.

## Runtime transition rule

Until the managed delegation bridge is accepted, HELP_HUMAN must use durable
manager-launch briefs and handoff records for Agent 0 to Agent 1 delegation.
It must not claim executable nested delegation that the active runtime cannot
perform. Agent 1 direct entry remains supported throughout the transition.

## Dedicated Agent 2 rule

A persistent specialist `AGENT_*.md` requires a HELPS_HUMANS proposal that
demonstrates why TASK plus a skill or an ephemeral generalist is inadequate.
The proposal names the persistent runtime semantics, tools, context,
permissions, callers, compatibility posture, and removal/review condition.
The human approves creation before the file becomes live in `AGENTS.md`.

## Scope not granted

- No project deliverable or concordance artifact is modified by this ruling.
- No active Agent 2 file is removed without replacement and caller migration.
- No runtime gate is weakened; sealed context, pipeline approval, capability
  non-inheritance, path containment, and child-run evidence remain mandatory.
- Git facts do not become semantic acceptance.
