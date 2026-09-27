# Chirality v4 — Examination

**Status: post-acceptance consolidation for the accepted decomposition basis;
independent substantive fidelity review [completed](../execution/_Coordination/AgentRuns/APP-V4-DEFINITION-20260926/SEED_FIDELITY_REVIEW.md).** Companion to the [PRD](PRD.md),
prepared after acceptance of composite **APP-V4-BASIS-20260926**, including
open matters and external dependencies. [PRD §0](PRD.md#0-basis-chronology-and-reading-this-set)
identifies the actual accepted sources; no earlier human hash-review of
these consolidated bytes is claimed. Existing `V4-EXM-<nn>` identities are
retained.

This is planned examination, not a report of executed v4 tests. No scenario
was run by this consolidation. Added coverage below derives from accepted
HTML decisions 03–07 and later U1–U3; exact operations, fixtures and sequencing
remain implementation-definition details in the owning SoWs. They add no
seven-gate process and require no product-wide empirical proof before
conceptual discussion or decomposition.

## 1. Verification and validation

- **Verification** asks whether an identified build does what the PRD states.
  It uses the scenarios below, run against a named candidate, with outcomes
  recorded as passed, failed, blocked, not run or inconclusive.
- **Validation** asks whether v4 is fit for the work it is meant for. It
  needs practitioners doing realistic work, and at v4.0 the principal
  practitioner is the owner. Agent-operated scenarios support verification;
  they do not replace validation (T2 P11).

Verification scenarios use invented engineering material (V4-CST-06).
Validation in use follows §6 with invented or owner-controlled material;
real/client data is not required. Domain corpus suitability and permission
for a later research fixture are established by its provider/admission
contract, not inferred here.

App-owned behavior is examined by its responsible undertaking. The external
SWBPIPE session owns its host implementation; the human relays coordination
through repository files (U1/U5). Host/connector observations require an
identified contribution, configuration and evidence from the responsible
owner. Neither a handoff nor a separate component pass establishes the joined
activity. Domains provider ownership/location and interfaces remain open;
this seed neither assigns its construction to App nor excludes a future
App/program allocation.

## 2. Evidence rules

- **V4-EXM-01** Every result names the candidate, the configuration (harness
  and model versions, model server), and the date.
- **V4-EXM-02** The seams are tested without live models where possible:
  real protocol exchanges are recorded once and replayed (M-7). Live-model
  runs are few and deliberate.
- **V4-EXM-03** A check that passed on an earlier candidate supports only that
  candidate; changed code reopens the affected scenarios.
- **V4-EXM-04** Interface scenarios run in WebKit and Chromium, with a
  short smoke check of each targeted packaged application. Preserve this
  deliberate cross-engine examination from the owner's M-06 reservation and
  analysis §11.3: it addresses shared-interface upkeep and later portability,
  while v4 shipping remains macOS-first. It does not select a Windows release
  or permit replacing a required native witness with browser evidence.
- **V4-EXM-05** The criteria in this document are protected during repair: a
  failure is diagnosed and fixed, not removed by weakening its criterion.

Static source paths, defined tests, historical passes and actual execution
on the selected v4 candidate remain distinct. The checked research's 51
claims at `e548d4cfada4d2105de6231516dc6e5fc4bd4689` do not qualify v4, prove
full coverage or isolate architecture causation. Changed later implementation
needs targeted applicability checks. New evidence remains bound to what was
actually observed; no measurements of maintenance or coordination savings
are invented (B-HTML evidence account).

## 3. Scenarios — the Chirality App

**V4-EXM-10 Create and reuse a workflow.** Starting from an empty project
folder, the person develops a plan with the agent, revises it, executes it
with real tool use, turns it into a workflow draft, reviews and registers it,
then reuses it on new inputs and refines it twice.
*Verifies* V4-APP-01, V4-WF-01…03. *Observe:* the plan's revisions; the
draft's review and explicit registration; no silent overwrite; the
workflow's declared part.

**V4-EXM-11 Interruption, approvals and restart.** During the run in
V4-EXM-10, the person stops a turn, closes and reopens the window, denies
one approval and grants another, then quits and relaunches the App and
continues the conversation.
*Verifies* V4-EXE-01…04. *Observe:* work continues when the window closes;
outstanding requests survive; nothing is shown as done that was not observed.
Distinguish closing an observer from interrupting work, provider state from
rendered state, primary-turn completion from active descendants, and request
settlement from received acknowledgment. An unavailable outcome stays
unknown rather than being reconstructed as success.

**V4-EXM-12 Three kinds of model access.** With ChatGPT sign-in, an API key,
and a local model server all configured, the person runs one conversation
with each and switches between them.
*Verifies* V4-APP-02.

**V4-EXM-13 Coordinating an agent fleet.** The person delegates two bounded
pieces of work with briefs, follows them on the undertaking's work graph,
examines the returns from the queue, and decides one matter from a decision
package.
*Verifies* V4-PM-01…06. *Observe:* the graph and records are files; the
views rebuild from them. To examine the accepted long-work/recovery purpose,
include a dependent contribution alongside independent ready work, a returned
item awaiting review, actual resource/worker ownership, a changed basis and
an interruption. Preserve what was reviewed/integrated and what still waits.
The exact small fixture is a SoW detail; no universal staffing number or
hundred-agent performance claim follows from it (B-HTML 05/07).

**V4-EXM-14 Workflow App/host round trip.** Following the first connected
activity's staged contract, carry a reviewed workflow from App to the host,
adapt/refine it and make the refinement usable in App. Exercise required-tool
availability, an explicit unsupported-capability outcome, checkpoint identity,
interruption and revision/replay history. *Covers* V4-WF-03…06 and the accepted
B-HTML 05 join. *Observe:* selected/resolved bytes, what was actually supplied
and provider-adopted, and observed behavior are separate. A portable file or
successful registration alone does not prove compatible execution. Host
participation is externally coordinated, not implemented by this undertaking.

## 4. Scenarios — SWBPIPE as host

These scenarios organize the first connected model-adjustment/checking
activity accepted in B-HTML 05 and qualified by U1/U5. They are coordinated
with the external SWBPIPE owner. Define their exact operation, autonomy,
interfaces and environment before dependent execution (PRD OQ-11). Domains
is not a prerequisite; its research/design extension is a later increment.
The existing supports/run-adjustment example below is a proposed fixture,
not an assignment to this App undertaking to build solver or host behavior.


**V4-EXM-20 Delegated model change with a local model** — *the replacement
journey (V4-REP-01).* On an invented piping model, the engineer asks the
embedded agent, running on the local model server, to add supports and adjust
a run. The agent reads the tables through the catalog, drafts a proposal,
and the engineer reviews the proposed rows in the tables, accepts some row by
row, rejects one, and applies. A solve follows.
*Verifies* V4-HOST-01…04, V4-PAR-01…04, V4-HI-20…25. *Observe:* proposed rows
and old and new values in the host's own tables; receipts; origin marks; a
stale proposal refused after an intervening edit.

**V4-EXM-21 The agent checks the engineer's work.** The engineer edits the
model, then asks the agent to check it. The agent's findings attach to rows
and results by reference without changing the tables.
*Verifies* V4-HI-10…12, V4-AUT-03's settled anti-impersonation distinction and
V4-AUT-05. Findings are not a recorded human Checked/approval act. Any
operation requiring the exact unresolved human-act policy waits for its
OQ-02 disposition rather than treating the old draft default as ruled.

**V4-EXM-22 Graduated autonomy.** The engineer allows direct application for
one class of low-consequence operation and keeps proposals for model
geometry. The agent applies the first kind with origin marks and undo, and
proposes the second. A workflow checkpoint stops the run for a human act.
*Verifies* V4-AUT-01, V4-HI-40…42, V4-WF-05 under an explicitly identified
operation policy. Preserve direct application, proposal acceptance, human
checking and professional reliance as different acts. The pending classifier
and always-reserved details are decided before their dependent criteria;
this scenario is not itself that decision.

**V4-EXM-23 Privacy in local operation.** During V4-EXM-20, all network
traffic from the host is observed. *Verifies* V4-HOST-02: no request goes
anywhere but the configured model server.

**V4-EXM-24 Catalog-extension trace and qualified criterion.** Trace one new
catalog operation through the human interface, embedded tools and external
adapter. Record generated behavior, additional work, availability reasons
and semantic outcomes. This directly examines the original V4-PAR-05 /
V4-HI-03 promise of all-actor availability without separate work. It supplies
evidence for the explicit OQ-10 disposition; it is not a pass merely because
common validation exists. If the absolute promise is retained, verify it
without other changes; if a narrower generated surface or later staging is
explicitly chosen, verify that identified criterion and preserve the
supersession. No weaker criterion is silently adopted (B-HTML 04).

**V4-EXM-25 An external controller.** The Chirality App's Codex, with
SWBPIPE's external interface enabled, inspects the model and submits a
proposal; the engineer accepts it in SWBPIPE. *Verifies* V4-HI-50…52. Join the
original inspected model basis through refusal/application to the host's
receipt; include an intervening edit and a lost acknowledgment/interruption.
Compare meaningful reads, non-mutating checks, validation and outcomes with
the embedded/human routes. Transport deduplication or independent Runtime/
Piping component passes do not prove the connected outcome (B-HTML 04–05).

## 5. Scenarios — connectors and records

**V4-EXM-30 Qualified, limited and absent connectors.** For a selected
receiving consumer, first trace one source pin through qualified PEC
extraction/response and the permitted receiving action. Then ask the same
coordination question with absent, stale, partial and failing feeds. Observe
coverage, freshness, source route and actual fallback responsibility; no
missing feed implies empty work or permission. An unqualified delivery is
reported as such, not as a failed demonstration of the finished product.
Retain the original combination of absent PEC and a stale Domains source,
and also distinguish the connectors' independent availability. The App is
the first intended PEC consumer; later Piping adoption has its own evidence.
*Covers* V4-CON-02…04, V4-HI-60…63 and B-HTML 06; no new v4 start gate.
Domains-specific receiving evidence joins its later increment (V4-EXM-32).

**V4-EXM-31 Reconstructing a run.** A week after V4-EXM-20, someone
reconstructs from the project's files what was asked, what the agent
proposed, what the engineer accepted and what changed, with the host's
receipts. *Verifies* V4-REC-01…05, V4-HI-70…71. Preserve what is unknown and the scope
of any actual human act. Records of source resolution or transport success
alone must not fill an unobserved provider/host outcome.

**V4-EXM-32 Domains research context to a design candidate — subsequent
increment.** With an identified provider/query contract and admitted test
sources, the external host's agent calls the domain search tool through its
research workflow, assembles context and produces a design candidate for
human approval. Observe source references, standing, freshness, relevant
inferences/gaps, the candidate identity and the actual scope of the human
act. Include unavailable or unsuitable research input so no context or
approval is invented. *Covers* V4-CON-01, -04, -05 and V4-HI-60, -64, -65,
directly from U1–U3. Provider/query-tool, workflow and host readiness are
points of need for this increment, not prerequisites to the initial D05
activity. The scenario selects no corpus/database technology. Domains
provider allocation remains open; SWBPIPE implementation is externally owned.

## 6. Validation in use

- **V4-EXM-40** The owner uses v4 for real design work of the owner's choosing
  over an agreed period, in both the Chirality App and SWBPIPE, with invented
  or owner-controlled data.
- **V4-EXM-41** What to notice, as design aims rather than scores: whether the
  results warranted confidence for the attention they took (the owner's
  measure, recorded 2026-09-19 in `plans/evidence/2026-09-19_owner_words_four_graph_structures.md`); where the person had to
  work around the product; where agent and person could not see the same
  thing; and where a record was needed and missing, or kept and never read.
- **V4-EXM-42** Observations go to the owning requirement, workflow or
  method, as the operating method describes; they may reopen affected
  commitments when new learning warrants it, including a future v5.0 basis.
  Compare useful like work across preparation, review, repair, integration,
  recovery and waiting by cause. Source size or elapsed historical time alone
  does not measure the architecture's lifetime benefit.

## 7. Replacing v3.0.1

The owner decides the replacement (V4-REP-01). The evidence presented for
that decision is: V4-EXM-10 and V4-EXM-11 passed on the candidate App (the
core loop at least at v3.0.1's level), and V4-EXM-20 passed on the candidate
App and SWBPIPE with a local model (one live embedded journey from request to
acceptance).


This evidence is for the human's replacement judgment, not blanket
all-project retirement or professional reliance. Staged coexistence preserves
history, current work and receiving responsibilities (B-HTML 07). Domains
joins subsequently under U2; PEC remains optional to start. Completion of
decomposition, prepared handoffs, accepted provider contracts and independent
component checks do not stand in for the applicable connected witnesses.
