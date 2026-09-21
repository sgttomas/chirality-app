# Project management for AI software development teams

**Status:** theory draft, 2026-09-19. Agent-authored under Ryan Tufts's direction.
Explanatory and nonbinding; no owner acceptance of this text or empirical
validation is implied. This manual does not change an instruction, workflow,
permission, protected criterion, project scope or release gate.

This manual develops an account of how a human and an AI team organize software
work as its purpose, dependencies and implementation become better understood.
It begins with theory. The worked example will then examine `chirality/` and
the projects within `chirality/projects/`, looking for the predicted patterns,
their contradictions and meaningful absences.

## Reading order

1. [Theory](01_theory.md): the argument, vocabulary, project conditions,
   coordination patterns, continuity and shipping.
2. [Worked-example method](02_worked_example_method.md): prospective expectations,
   evidence selection and ways the case can challenge the theory. This is a
   study design, not completed case findings or an executable workflow.

The theory covers eight subjects: human direction and responsibility; entry
and changes of undertaking; requirements, decomposition and setup; dependency
resolution and execution; team construction; testing and integration;
maintaining continuity; and shipping. The four structures and four philosophical
perspectives connect these subjects rather than forming separate writing streams.

## Basis and status of the argument

The conceptual starting points are the owner's directions in this conversation
and the thesis as amended through [PR #819](https://github.com/sgttomas/chirality/pull/819).
The retained source basis is repository commit
`35d8b93aed1831c7579986d305b383521ca47c80`; the PR's thesis head is
`7af45b19f5445d366c25fbedba39e2b9be6fe0f6`.
Relative source links below are navigation; use that basis when reconstructing
what this draft read. Later source changes require an applicability assessment.

| Source | Use in this draft | Limit |
|---|---|---|
| [Owner directions](../../plans/evidence/2026-09-19_manual_theory/OWNER_DIRECTION.md) | Purpose, theory-first order, project example, separate continuity/shipping, phase-sensitive entry | Approval to draft is not acceptance of the resulting theory |
| [Thesis Chapter 3](../thesis/03_philosophical_framework.md), §§3.2–3.6 | Four philosophical perspectives; information, knowing and accountable reliance | An explanatory philosophical account, not proof of every proposed practice |
| [Thesis Chapter 4](../thesis/04_architecture.md), §4.3.5 | Four structures and their relations | The September additions identify their provisional evidential status |
| [Thesis Chapter 7](../thesis/07_se_design_analysis.md), §§7.3–7.4, 7.9–7.11 | Configuration, traceability, verification and human attention | Some named mechanisms describe older repository arrangements |
| [Thesis Chapter 9](../thesis/09_discussion.md), §§9.2.6, 9.3.7–9.4.8 | Over-proceduralization, project-delivery correspondence and limits of the case | No controlled validation or independent confirmation of universal structures |
| [Owner's four-structure record](../../plans/evidence/2026-09-19_owner_words_four_graph_structures.md) | Attribution of the four-structure proposal and warranted-confidence/attention measure | Transcription custody is distinct from independent authentication |
| [Cycle-driven resolution](../CYCLE_DRIVEN_RESOLUTION.md), §§2–4 | Objective-relative graphs, SCC resolution and limits | Existing Chirality doctrine; this manual neither broadens nor replaces it |
| [Root agent instructions](../../AGENTS.md) | Current operational role distinctions and delegation boundaries | Repository practice, not a universal prescription for every team |

These sources establish what the project proposes and records. They do not
independently establish that the theory generalizes. This pass does not verify
the thesis's external bibliography or offer legal/regulatory advice. The
thesis's own [warrant-status statement](../thesis/README.md#warrant-status)
governs how it describes itself; an agent's editorial review here does not
advance that status.

Sections labelled **proposition** contain explanatory claims to investigate.
**Practice implications** are recommendations derived from those claims.
Descriptions of Chirality's arrangements are identified as such. The later
case reading must preserve these differences.

## Continuation

The present draft has no worked-example verdict. Its next intellectual step is
to challenge the theory and prospective expectations, then reconstruct selected
Chirality episodes against identified sources. Generalization beyond the case
and independent external corroboration remain separate work. The drafting run
and review record are in
[the manual-theory evidence directory](../../plans/evidence/2026-09-19_manual_theory/).
