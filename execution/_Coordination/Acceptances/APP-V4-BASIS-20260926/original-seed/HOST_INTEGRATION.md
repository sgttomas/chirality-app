# Chirality v4 — Host integration

**Status: DRAFT 1 — candidate, not accepted.** Companion to the
[PRD](PRD.md) and [architecture](ARCHITECTURE.md). It states the contract
each host application implements so that a person, the host's embedded
agent, and an external agent share one set of objects, operations and
results (semantic parity, D-18, D-19). Identifiers `V4-HI-<nn>`. Items marked
**[pending]** depend on an unconfirmed default.

The contract is expressed in terms of behaviour and data, not a particular
programming interface; each host implements it in its own code (M-1).

## 1. Who implements what

| Party | Responsibility |
|---|---|
| The host | Its domain objects and truth; the capability catalog; validation and the one route by which changes are applied; receipts; the human acts it offers; its interface |
| Chirality (shared layer) | The catalog contract types; the embedded agent loop; workflows and checkpoints; the agent panel components; the record format |
| The embedded agent | Acting through the catalog within the autonomy the person has set |
| An external agent | Acting through the same catalog, exposed as an MCP server or command-line interface |

## 2. The capability catalog

- **V4-HI-01** A host describes every operation a person can perform — reads
  and changes alike — once, in a capability catalog.
- **V4-HI-02** Each entry states:

  | Field | Content |
  |---|---|
  | Identity | A stable identifier and a version |
  | Purpose | What the operation does, in words a person and an agent both read |
  | Inputs | A schema for its arguments |
  | Availability | Its preconditions, and the reason it is unavailable when they do not hold (for example "Select a load case in the model tree first") |
  | Effects | Which objects it changes, if any |
  | Result | A schema for what it returns, including the standing of the result |
  | Errors | The errors it can return and what each means |
  | Human-act class | None; **may apply** within granted autonomy; **proposal only**; or **reserved** to the person (§5) |

- **V4-HI-03** The host's interface, its embedded agent's tools and its
  external interface are all generated from, or checked against, this one
  catalog. An operation added to the catalog becomes available to all three
  without separate work (V4-PAR-05).
- **V4-HI-04** An operation that is unavailable to the person is unavailable
  to the agent, with the same reason.

## 3. Perception

- **V4-HI-10** The agent reads through catalog read operations that return
  the same views the person sees — tables, results, diagnostics — with the
  same standing marks (V4-PAR-03).
- **V4-HI-11** Every read returns the **basis** it describes: an identity for
  the workspace, its generation, the model revision, and a canonical content
  hash. A later action cites the basis it relied on.
- **V4-HI-12** Results carry their standing — current or historical, the
  checks they passed, known limitations — so that an agent does not present a
  result with more confidence than the host gives it (L-10).

## 4. Changes

- **V4-HI-20** Every change, by person or agent, passes through the host's one
  validation and application route; there is no second route for agents
  (V4-PAR-04).
- **V4-HI-21** An agent's change carries its origin (for example an author
  type of "agent" with the conversation and workflow run it came from) and the
  basis it relied on.
- **V4-HI-22** Where the person has granted the autonomy, the agent may apply a
  change directly; the change is marked with its origin, can be undone, and
  can be checked later (V4-AUT-01).
- **V4-HI-23** Otherwise the change is a **proposal**, with this lifecycle:

  ```text
  drafted → validated → queued → accepted → applied (receipt)
                            ├──→ rejected
                            ├──→ withdrawn
                            └──→ stale   (its basis no longer holds)
  applied or not, if the outcome cannot be observed → outcome unknown
  ```

  A stale proposal is refused with its reason and may be re-drafted on the
  current basis. A later selection never retargets a proposal. Submitting the
  same proposal twice has one effect.
- **V4-HI-24** A proposal shows the person, in the host's own views, what will
  change: old and new values, the objects affected, and why (X-07).
- **V4-HI-25** `success` from an operation means it ran; it never means a
  person accepted anything. A submitted proposal reports "queued" until the
  host records acceptance and application.

## 5. Human acts

- **V4-HI-30** A host names the acts reserved to the person. At least:
  accepting a proposal where autonomy requires it; marking work checked;
  approving; and relying on a result for a professional purpose.
- **V4-HI-31** **[pending — Q-04]** The agent may prepare any of these acts
  and may ask for them; it never performs them or records them in the
  person's name (V4-AUT-03).
- **V4-HI-32** A human act binds to the content it concerns (for example a
  row's content hash) and lapses visibly when that content changes (X-20;
  SWBPIPE DEC-104's checked tag).
- **V4-HI-33** Acceptance of a proposed edit is not engineering approval. The
  interface says "accept", never "approve", for proposals (SWBPIPE design
  direction).

## 6. Autonomy settings

- **V4-HI-40** The person sets, per class of operation, whether the agent may
  apply directly or must propose. The setting is visible, can change during
  work, and is recorded with each run (D-04).
- **V4-HI-41** A host chooses conservative defaults for consequential
  operations. For SWBPIPE's model changes the default is proposal with
  row-by-row, multi-row or whole-batch acceptance, following the owner's
  direction of 2026-09-17; the person may widen it.
- **V4-HI-42** A workflow's declared checkpoints override autonomy: at a
  checkpoint the run waits for the person's act (V4-WF-05).

## 7. External agents

- **V4-HI-50** A host may expose its catalog to agents outside it — such as the
  Chirality App's Codex — as an MCP server using the current protocol, or as a
  command-line interface over its live controller. Both are built from the
  catalog and apply the same validation, autonomy settings and reserved acts.
- **V4-HI-51** An external agent cannot perform a reserved act. SWBPIPE's
  live-control design already has no external "apply".
- **V4-HI-52** External access is off unless the person enables it, and it is
  local to the machine.

## 8. Connectors

- **V4-HI-60** **Domains [pending — Q-07]** is read through its own query
  interface. Results locate evidence; they never prove membership or
  authority. Freshness is checked and shown.
- **V4-HI-61** **PEC** is read through its own interface when available. Every
  claim shows the commit it was examined through and its freshness. Presence
  information is never used for correctness. Chirality acts; PEC observes.
- **V4-HI-62** When a connector is absent or stale, the product says so and
  falls back to the files.
- **V4-HI-63** Files Chirality writes for coordination (work graphs, decision
  records) keep stable formats, because PEC reads them.

## 9. Records

- **V4-HI-70** Each workflow run leaves a compact record with the host project:
  the workflow and version, the conversation, the autonomy settings, the
  operations requested and their outcomes, the host receipts by reference, the
  human acts performed, and the model used (D-07).
- **V4-HI-71** The host's receipts, hashes and origin marks are the evidence of
  what changed; the run record links them and does not copy them.

## 10. Checklist for a new host

For the application builder (PRD §3):

1. Describe every operation once in a capability catalog (§2).
2. Route every change through one validation and application path (§4).
3. Return a basis with every read; check it on every change (§3–4).
4. Mark origins; offer undo; show proposals in the host's own views (§4).
5. Name the reserved human acts and bind them to content (§5).
6. Choose autonomy defaults for consequential operations (§6).
7. Add the Chirality panel from the shared components; wire the embedded loop
   to the catalog and the local model server through the host's network layer.
8. Write the host's own workflows and skills; test them in the Chirality App.
9. Optionally expose the catalog to external agents (§7).

## 11. SWBPIPE as the first host

What exists and what is missing, from T6 (read at `2b0572fe0` and the
unmerged live-control branch):

| Contract element | In SWBPIPE today | Gap |
|---|---|---|
| Capability catalog | A catalog of interface capabilities with reasons for unavailability (`capabilityCatalog.ts`) | Not yet the single source for agent tools; reads mostly reachable only from the interface |
| One route for changes | One operation applier for every mutation (Rust, also compiled to WebAssembly) | — |
| Origin | `author_type` includes "agent" in the operation schema | Per-row and per-cell origin marks not yet shown |
| Basis binding | Queued batches capture a basis model and hash; the live-control branch binds calls to app instance, session, project generation, model revision and content hash | Live-control branch not merged; native and human witnesses open |
| Proposals and acceptance | Review queue; atomic batches with one undo checkpoint | Row-level acceptance interface not implemented |
| Checked mark | Content-bound, lapses on change (DEC-104) | — |
| Agent checks the engineer's work | Directed by the owner (Review page) | Not implemented |
| Embedded agent panel | Placeholder, disabled ("Agent: not available yet") | The v4 embedded loop and panel |
| External agents | Command-line live control (inspect, preview, submit, status), no external apply | Merge and qualification |

These gaps belong to the SWBPIPE project's own work; the v4 replacement
condition (V4-REP-01) requires one live journey through them.
