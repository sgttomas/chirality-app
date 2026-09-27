# Chirality v4 — Examination

**Status: DRAFT 1 — candidate, not accepted.** Companion to the
[PRD](PRD.md). It describes how v4 will be examined: the principal scenarios,
what verification and validation each covers, and the evidence each should
leave. Nothing here has been run; v4 is not built. Identifiers `V4-EXM-<nn>`.

## 1. Verification and validation

- **Verification** asks whether an identified build does what the PRD states.
  It uses the scenarios below, run against a named candidate, with outcomes
  recorded as passed, failed, blocked, not run or inconclusive.
- **Validation** asks whether v4 is fit for the work it is meant for. It
  needs practitioners doing realistic work, and at v4.0 the principal
  practitioner is the owner. Agent-operated scenarios support verification;
  they do not replace validation (T2 P11).

Examination uses invented engineering material only (V4-CST-06).

## 2. Evidence rules

- **V4-EXM-01** Every result names the candidate, the configuration (harness
  and model versions, model server), and the date.
- **V4-EXM-02** The seams are tested without live models where possible:
  real protocol exchanges are recorded once and replayed (M-7). Live-model
  runs are few and deliberate.
- **V4-EXM-03** A check that passed on an earlier candidate supports only that
  candidate; changed code reopens the affected scenarios.
- **V4-EXM-04** Interface scenarios run in both web engines the shells use
  (WebKit on macOS, Chromium on Windows), plus a short smoke check of each
  packaged application (analysis §11.3).
- **V4-EXM-05** The criteria in this document are protected during repair: a
  failure is diagnosed and fixed, not removed by weakening its criterion.

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

**V4-EXM-12 Three kinds of model access.** With ChatGPT sign-in, an API key,
and a local model server all configured, the person runs one conversation
with each and switches between them.
*Verifies* V4-APP-02.

**V4-EXM-13 Coordinating an agent fleet.** The person delegates two bounded
pieces of work with briefs, follows them on the undertaking's work graph,
examines the returns from the queue, and decides one matter from a decision
package.
*Verifies* V4-PM-01…06. *Observe:* the graph and records are files; the
views rebuild from them.

## 4. Scenarios — SWBPIPE as host

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
*Verifies* V4-HI-10…12, V4-AUT-03, V4-AUT-05.

**V4-EXM-22 Graduated autonomy.** The engineer allows direct application for
one class of low-consequence operation and keeps proposals for model
geometry. The agent applies the first kind with origin marks and undo, and
proposes the second. A workflow checkpoint stops the run for a human act.
*Verifies* V4-AUT-01, V4-HI-40…42, V4-WF-05.

**V4-EXM-23 Privacy in local operation.** During V4-EXM-20, all network
traffic from the host is observed. *Verifies* V4-HOST-02: no request goes
anywhere but the configured model server.

**V4-EXM-24 Parity by construction.** A new operation is added to SWBPIPE's
catalog. Without other changes, it appears in the interface, as a tool for
the embedded agent, and through the external interface, with the same
availability reasons. *Verifies* V4-PAR-05, V4-HI-03.

**V4-EXM-25 An external controller.** The Chirality App's Codex, with
SWBPIPE's external interface enabled, inspects the model and submits a
proposal; the engineer accepts it in SWBPIPE. *Verifies* V4-HI-50…52.

## 5. Scenarios — connectors and records

**V4-EXM-30 Connectors absent and stale.** With PEC stopped and a Domains
index older than its sources, the App shows the absence and the staleness
and falls back to the files. *Verifies* V4-CON-03, V4-HI-60…62.

**V4-EXM-31 Reconstructing a run.** A week after V4-EXM-20, someone
reconstructs from the project's files what was asked, what the agent
proposed, what the engineer accepted and what changed, with the host's
receipts. *Verifies* V4-REC-01…05, V4-HI-70…71.

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
  method, as the operating method describes; they may reopen parts of this
  basis for v5.0.

## 7. Replacing v3.0.1

The owner decides the replacement (V4-REP-01). The evidence presented for
that decision is: V4-EXM-10 and V4-EXM-11 passed on the candidate App (the
core loop at least at v3.0.1's level), and V4-EXM-20 passed on the candidate
App and SWBPIPE with a local model (one live embedded journey from request to
acceptance).
