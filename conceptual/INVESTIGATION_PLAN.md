# Investigation plan — Chirality App v4 conceptual undertaking

Standing: **proposed plan (agent).** An ad hoc plan under the selected
workflow `chirality-root:bundled:workflow:reverse-engineer-software`. It is
revised as findings and the owner's answers arrive; it is not a reusable
workflow and not an accepted commitment.

## Purpose and end point

Produce, with the owner, an independently reviewed **seed set** for Chirality
App v4 and present it for acceptance (OD-12): a PRD and the supporting core
documents that carry the product's purpose, users, activities, boundaries,
interfaces, constraints and means of examination, with preserved references,
open questions, and conditions for further work identified. The fresh
implementation session then establishes decomposition, setup, production
contracts, dependencies and route from the accepted seed (OD-13). This plan
ends at the owner's response to the seed set.

## Principles for proportion

- Investigate what a pending decision needs. A question the owner can answer
  from experience is asked, not researched.
- Read the reference through activities people accomplish, then open
  decisions and code only where they settle a consequential question.
- Prefer small, disposable experiments with stated limits over broad
  surveys when behaviour is uncertain (supplier fit, embedding, interaction
  modes).
- Keep the seed small: one PRD that reads as a whole, plus a supporting
  document only where a subject needs its own home.
- Old evidence supports only its own subject and revision; nothing inherited
  becomes a v4 requirement without the owner adopting it (OD-10).

## Stages

| # | Stage | What it establishes | Method and participants | Output | Status |
|---|---|---|---|---|---|
| A | Frame and pin | Working root, pinned revisions, fallback release, archive access, thesis transfer, run record | HELPS_HUMANS directly | [`../reference/`](../reference/), [`../foundation/`](../foundation/), run record | Done 2026-09-25 |
| B | First reading of the reference | What each body of material can support; candidate exemplars, lessons and tensions | Seven parallel read-only TASK investigations (thesis; manuals; App v3; App history and archives; Runtime, PEC and Root; SWBPIPE; supplier landscape); returns preserved verbatim | Returns in the run record; [`SOURCE_INVENTORY.md`](../reference/SOURCE_INVENTORY.md) | Done 2026-09-25 |
| C | First synthesis | Exemplars and lessons with evidence standing; the consequential product questions | HELPS_HUMANS | [`EXEMPLARS_AND_LESSONS.md`](EXEMPLARS_AND_LESSONS.md), [`QUESTIONS.md`](QUESTIONS.md) | Done (first cut) |
| D | Direction conversation | The owner's answers to the product questions: nucleus, embedded unit, workflow meaning, autonomy and gates, supplier stance, project-management scope, replacement conditions | Conversation; answers recorded verbatim in [`DECISIONS.md`](DECISIONS.md) | Decisions; revised questions | Next |
| E | Targeted investigations | Evidence the answers call for (see below) | TASK investigations and disposable experiments; the owner where hands-on use matters | Short findings notes, each tied to a question | After D |
| F | Draft the seed set | Candidate PRD and supporting documents | HELPS_HUMANS, drafting with the owner section by section where direction is still forming | `docs/` candidate | After D, overlapping E |
| G | Independent examination | Fidelity to the reference, coherence of departures, preserved material unchanged, open questions carried properly | A separately prepared reviewer that did not author the candidate — preferably a different model family (see Q-12); repair and backcheck | Review record | After F |
| H | Present for acceptance | The owner's actual response, bound to identified content | Decision record | [`DECISIONS.md`](DECISIONS.md); handoff to the implementation session | After G |

## Stage E — investigations held until the direction is clearer

Each runs only if the owner's answers make it relevant. Each states setup,
action, observation and the limit of what it can show.

| ID | Question it serves | Investigation | Candidate method |
|---|---|---|---|
| E1 | What of the v3 experience must survive? | Exercise the core loop (plan → execute → save a workflow → reuse → iterate; interruption; approval; restart) on v3.0.1 and record what helps and what obstructs | The owner and agent together, or agent-operated through computer use with the owner's permission. The installed copy is **3.0.0**; 3.0.1 is not installed. |
| E2 | Which host activities define the embedded claim? | Walk three representative SWBPIPE activities (a delegated model edit; an agent check of the engineer's work; a result review toward a report) through objects, operations, results and recovery | Development build of SWBPIPE; the unmerged live-control branch as the current agent seam |
| E3 | Which harness can supply what v4 needs? | Turn the owner's answers into a required-behaviour statement; shortlist; one disposable spike per leading candidate: host a harness beside a Tauri shell, expose two application tools, observe approvals, event stream, interruption and resume, delegation, and account or licence terms | Isolated scratch projects; no change to existing products; T7 §5 proposes seven such experiments (server-protocol harness in a Tauri shell, SDK-over-binary, minimal open harness with a local model, ACP client, build-your-own loop, MCP Apps in a Tauri webview, GUI operation three ways) |
| E4 | Structured tools, computer use, or both, per activity? | Run one SWBPIPE activity through typed tools and one external-tool step through computer use; compare what each party can perceive, do and recover | Disposable fixtures; invented engineering data only |
| E5 | Which project-management capabilities are product features? | Trace the coordination needs that actually arose in recent multi-agent work (App, Piping, PEC) against the manuals' purposes; separate product needs from the build method | Reading existing run records at the pinned revision |
| E6 | What does an application builder need to integrate v4? | Describe the integration journey for a new host from the SWBPIPE live-control and Runtime application-tools records | Reading plus a sketch contract |

## Checkpoints with the owner

1. **Now** — inventory, plan, questions, first exemplars (this return).
2. **Direction** — the owner answers or redirects the questions; answers recorded.
3. **Evidence** — results of the Stage E work the answers selected, with any
   revised questions.
4. **Draft** — PRD structure and the load-bearing sections, before completing
   the set.
5. **Seed set** — the reviewed candidate presented for acceptance.

Routine inspection, drafting and repair between checkpoints proceed without
further prompts. Decisions reserved to the owner are brought as concrete
choices with evidence and consequences.

## Records

The run record at
[`../execution/_Coordination/AgentRuns/V4-CONCEPT-20260925/`](../execution/_Coordination/AgentRuns/V4-CONCEPT-20260925/)
keeps the opening brief, each delegated brief and return verbatim, and their
timing and model. [`WORKING_RECORD.md`](WORKING_RECORD.md) keeps position,
open work and next steps. Git history carries the rest.
