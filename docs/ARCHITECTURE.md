# Chirality v4 — Architecture basis

**Status: post-acceptance consolidation for the accepted decomposition basis;
independent substantive fidelity review [completed](../execution/_Coordination/AgentRuns/APP-V4-DEFINITION-20260926/SEED_FIDELITY_REVIEW.md).** Companion to the [PRD](PRD.md). The
owner accepted the composite **APP-V4-BASIS-20260926**, including open matters
and external dependencies, before these consolidated bytes were authored.
See [PRD §0](PRD.md#0-basis-chronology-and-reading-this-set) for source keys,
chronology and the acceptance record; no prior human hash-review of this
post-act text is claimed. Identifiers `V4-ARC-<nn>` are retained. Amended by
scope-change amendment SCA-V4-001, accepted 2026-09-29, for owner
decisions DEC-4 and DEC-5 (PRD §0).

This basis carries the scoped D-19/D-20 choices and accepted HTML decisions
01–07. The original analysis explains their history; technical realization,
selected pins and receiving responsibilities are developed in SoWs and their
derivatives. SWBPIPE implementation is externally owned and coordinated
through the human (U1/U5); this document does not commission that work.

## 1. Priorities and principles

The owner's priorities for the harness/host choices, in order (D-16–D-18;
B-HTML 02), are:

1. **Maintainability** — the ongoing cost, for agents directed by one
   accountable person, of keeping the product correct and current while its
   suppliers, hosts and understanding change.
2. **Functionality** — the best harnesses' native capabilities are kept, not
   traded for portability.
3. **Local models and data privacy** — a host's agent runs on a local model
   server the user controls or on a cloud model the person chooses (OAuth
   sign-in or API key), with no default between them. It sends data only to
   the selected model service and to destinations the person has allowed, and
   every destination contacted is recorded and shown (V4-HOST-01/02; DEC-4,
   DEC-5). The later Domains connector must preserve the applicable data
   boundary; its deployment is unresolved, not an implicit exception (PRD
   OQ-03).

These priorities do not impose a universal ranking on all program choices.
The retained design principles (original analysis §3, with M-2 restated in
§9.2) are applied through concrete consumer responsibilities and the accepted
HTML recommendations:

| # | Principle |
|---|---|
| M-1 | Own only what is distinctively Chirality's: the workflow layer, the human–agent interface, the host-integration contract, and the records of human acts. |
| M-2 | Meet each harness at its own published embedding interface, unmodified and pinned, and pass its native items through to native presentation. No private modification; no generic vocabulary between Chirality and a harness. |
| M-3 | Keep knowledge in open formats: `AGENTS.md`, `SKILL.md`, workflow files, tool schemas. |
| M-4 | Do not fork fast-moving upstreams. |
| M-5 | Generality only on need; build for the harness and library in hand. |
| M-6 | Few stacks, mainstream tools; avoid release-candidate frameworks. |
| M-7 | Test the seams without live models: record real exchanges once, test against them; keep live checks few. |
| M-8 | Keep records proportionate to decisions, reliance and recovery. |

The original analysis associated maintenance burden with duplicated supplier
work, private modifications, premature generality and process weight. The
checked histories qualify that interpretation: successful supplier-host work
combined several interventions, retained an application-owned service, and
included a silence pass before a later keepalive repair. These are useful
lessons, not isolated causal proof or measured lifetime savings (B-HTML,
findings and decision 02).

## 2. Intended v4 relationships

This is the chosen direction to develop, not evidence of a built/qualified
end-to-end system. The App owns its supplier-hosting path; each engineering
host owns its domain path. A shared contract does not itself require a shared
service (B-HTML 02). The depicted SWBPIPE path needs the externally owned
implementation and explicit receiving agreement.

```text
 ┌───────────────────────────── Chirality App (Tauri + React) ─────────────┐
 │  Interface: conversation, plans, requests, workflows, fleet views       │
 │  Chirality layer: roles, workflows + checkpoints, records               │
 │  Main process: owns the Codex App Server child, protocol, open requests │
 └───────────────┬─────────────────────────────────────────────────────────┘
                 │ Codex App Server protocol (JSON-RPC over stdio), pinned
                 ▼
          Codex (stock) ── ChatGPT sign-in · API key · local provider
                 │
                 │ MCP (host tools, for an external controller)
                 ▼
 ┌──────────────────────── Host application, e.g. SWBPIPE (Tauri) ─────────┐
 │  Host interface ◄──── capability catalog ────► embedded agent loop      │
 │  (tables, views)      (one definition)          (Chirality, minimal)    │
 │  Host validation and application route           │                      │
 └──────────────────────────────────────────────────┼──────────────────────┘
                                                    │ Chat Completions,
                                                    │ through the host's
                                                    ▼ own network layer
                                        Local model server (oMLX, LM Studio,
                                        Ollama) or a cloud model (OAuth
                                        sign-in or API key), as the person
                                        chooses; other destinations only if
                                        the person allows them
```

Shared by both tiers: the workflow format with declared checkpoints, skills,
the four roles' guidance, the record format, the capability-catalog contract,
and interface components where they fit (V4-SHR-01…03). In the subsequent
Domains increment, the host's agent uses a search-tool call within a research
workflow to query the domain database, build context and prepare a design
candidate for human approval (U2/U3). Provider, tool and host integration are
separate responsibilities; the initial connected activity has no Domains
prerequisite. PEC delivery is retired; no coordination-provider replacement is needed.

## 3. The Chirality App

| ID | Decision | Reason |
|---|---|---|
| V4-ARC-01 | **Harness: Codex through the stock Codex App Server**, run from the App's own process, version-pinned, over its published protocol (JSON-RPC over stdio) | Recorded D-17/D-19 choice, retained by B-HTML 02; historical successful repairs support useful properties without proving topology-only causation |
| V4-ARC-02 | **Shell: Tauri 2 + React + Vite**, the same stack as SWBPIPE | D-20; one packaging pipeline and one main-process language across Chirality applications (analysis §11.2–11.3) |
| V4-ARC-03 | **No separate v3 Runtime service in the App target.** Its Node service and socket API are not carried forward as the App hosting topology | D-20 explicitly selected direct App-owned hosting. This is the chosen direction, not a claim that the retained service caused every historical failure or that a service is always wrong |
| V4-ARC-04 | **Sign-in and models through Codex's own account methods**: ChatGPT sign-in and API key, with credentials held by Codex; local model servers as Codex model providers chosen per conversation (`modelProvider` on `thread/start`) | D-06, D-17 |
| V4-ARC-05 | **Native presentation.** Codex's items — plans, tool activity, delegation, requests — are presented in their native form; protocol types are generated from the pinned Codex version, with a small hand-kept supplement for experimental fields | M-2; D-GOV-43 finding 4 (L-05) |

**Properties the App must hold** (X-03–X-05; B-HTML 02/05). Source paths and
historical checks motivate these properties but do not qualify a new v4
candidate:

- The Codex process, the protocol session and the register of outstanding
  requests live in the main process, so that reloading or closing a window
  stops observation, not work, and outstanding approvals survive.
- Every server request is answered or explicitly declined; unknown requests
  receive an explicit error.
- Reconnection recovers actual state from Codex rather than a Chirality copy
  of the transcript. Unknown outcomes remain unknown; request settlement or
  a reply-write attempt is not guaranteed received acknowledgment.
- Workflow source resolution, the actual supplied/provider-adopted basis and
  observed behavior are distinguishable. Conversation recovery alone does
  not establish recovery of a branching undertaking's ownership, returned
  work, review, integration or still-active descendants (B-HTML 05).

**Reuse candidates from v3** (T11, checked as historical source leads):
the Codex client logic and its restart and request-answering rules; the
instruction composition and role configuration; the workflow catalog and
draft registration; the plan registry; the version-pin check; and the
interface pieces that carry v3's valuable interactions — request cards, the
plan panel, workflow draft review, turn phases and outcome states, attachment
import. Reuse must account for its receiving contract and actual candidate
checks. **Not selected for the target:** the old service/socket client and
Next.js hosting routes, generic translation into Chirality event names, and
obsolete multi-engine/delegation wrappers. Preserve native supplier delegation
required by V4-APP-01. Historical code is retained as evidence until its
retirement is explicitly accounted for; this paragraph is not deletion
permission (B-HTML 07).

**Process placement (OI-008), decided by the owner on 2026-10-10:** "The Rust
host owns everything that writes the person's files or the App's records,
talks to Codex, or captures a person's act. The web view presents, and sends
only what the person initiates. It never writes records or operates the act
control." This generalizes the owner's earlier rulings for the workflow draft
workspace ("A, proceed with the Rust host.") and the fleet records, and it
keeps the properties above. Where shared contracts and components live stays
open (OI-014).

**Left to the implementation session:** whether Chirality keeps sign-in
separate from the user's other Codex clients (v3's overlay home) or shares
it; API-key sign-in through the pinned
protocol; signing and notarisation of the App and Codex binaries under Tauri,
including applicable entitlements; and the actual supplier version. The
original investigation recorded a v3 pin of 0.154.0 and a then-current
upstream 0.157.1; those are dated evidence, not the v4 pin. Confirm protocol
fields, account/provider behavior and packaging against the selected supplier
before dependent implementation/qualification, without reopening the chosen
supplier direction as though it were unanswered.

## 4. Host applications

| ID | Decision | Reason |
|---|---|---|
| V4-ARC-10 | **Agent: a minimal Chirality agent loop** in the host, over the **OpenAI-compatible Chat Completions** interface with tool calls | Recorded D-20 choice. Compatibility and maintenance effort must be established for the selected server and implementation; the original size/stability expectations are not qualification |
| V4-ARC-11 | **Model: local or cloud, as the person chooses, with no default** — a local model server the user controls, or a cloud model reached by OAuth sign-in or an API key | D-18; DEC-4 |
| V4-ARC-12 | **Network through the host.** The loop's requests pass through the host's own native layer, which allows only the selected model service and the destinations the person has allowed, records every destination contacted, and holds any key or sign-in credential outside the interface's script | D-18; DEC-4; DEC-5; T10 risk 3 |
| V4-ARC-13 | **Tools from the host's capability catalog**, with arguments validated against the catalog's schemas before the host's own validation runs | V4-PAR-01…05; [host integration](HOST_INTEGRATION.md) |
| V4-ARC-14 | **A Chirality-defined boundary around the loop** — messages, tools, events, checkpoints — so the loop can be replaced by Pi's libraries or another library if hosts outgrow it | D-20; M-5 |

**Properties the host agent must hold:**

- It sends data only to the model service the person selected and to
  destinations the person has allowed (V4-HOST-02; DEC-5):
  - the allow list works at two levels, a category switch (web access, MCP
    servers, other APIs, …) and named destinations within each category;
    the selected model service, and its sign-in service for a chosen cloud
    model, are always allowed by the person's model choice;
  - an MCP server is allowed only if it follows the stateless MCP revision
    2026-07-28; a server that does not is not offered and cannot be allowed;
  - the agent may ask for a destination during its work, and only the person
    grants it — once, for this run or always, for the destination or its
    category; only the requesting call waits, and a decline is reported to
    the agent as "destination not allowed by the person";
  - analytics or usage reporting, a silent switch to another model or
    provider, and background downloads or updates stay off unless the
    person turns them on;
  - every destination contacted is recorded and shown, in any model mode.

  An MCP server or other outside process can make its own network calls;
  unless it is sandboxed, the host can only decide whether to start it and
  record what it declares. Allow lists locked by an organization and
  enforced sandboxing of outside processes belong to a later governance
  phase. This property governs a host's embedded agent; the App's own Codex
  keeps the person's Codex configuration, approval and sandbox choices.
- It does not block the host's interface: long parsing and model streaming
  run off the interface's main thread where the host needs it (T10 risk 4).
- It treats truncated or malformed tool calls as failures to report, never
  as empty arguments to execute (T10 §6).
- It records runs in the shared record format, linking the host's receipts.

**Left to the responsible host's implementation definition:** where the loop
runs (interface thread, worker or native layer), streaming/tool-call parsing,
conversation persistence, and the host panel's use of reusable components.
For SWBPIPE, those choices and implementation belong to the external session;
the App/shared-contract work communicates its interface needs through the
human and repository coordination files (U1/U5). A prepared handoff is not a
receiving commitment or evidence of delivery.

## 5. Shared layer

- **V4-ARC-20** Shared contracts cover workflow/checkpoint meaning, role
  guidance, record identity, catalog semantics and human acts. Reusable
  TypeScript types and interface components can carry the repeated parts
  used by App and hosts; their exact allocation follows actual consumer
  responsibilities in the SoWs. Compatible local implementations, a shared
  library and a service have different costs. Shared meaning does not
  prescribe one executable service; broader common execution needs a concrete
  shared responsibility that justifies it (B-HTML 01–02).
- **V4-ARC-21** Hosts expose their capability catalog to external agents —
  such as the Chirality App's Codex — through an MCP server, which Codex
  supports natively, or a command-line interface, built from the same catalog
  (SWBPIPE's "controller first" path).
- **V4-ARC-22** Optional connectors and Domains have distinct receiving
  contracts. Show standing, coverage and freshness; qualified, limited and
  absent paths remain distinct. Domains joins a later host research/design
  increment, with provider ownership/deployment still open. PEC is retired
  as an active provider; retained compatibility is not a delivery dependency.
  No successor service or adapter is required by that retirement.

Renewing shared material must account for existing packaging, tool paths,
source-qualified selection/supply and other consumers. Historical placement
is not v4 authority, and moving a folder does not discharge those
responsibilities. Staged coexistence retains source history and current
selectors while each affected consumer adopts its identified basis
(B-HTML 01/07).

## 6. Supplier assumptions and pins

This table carries dated investigation assumptions to be verified against the
implementation's selected pins. It is not a fresh supplier survey or a claim
that every named server already satisfies the whole host activity.

| Supplier | Used for | Assumption | If it fails |
|---|---|---|---|
| OpenAI Codex (Apache-2.0 CLI and App Server) | The App's harness | The App Server protocol stays published and supported for embedding; releases roughly weekly with schema changes | Pin; upgrade deliberately; keep experimental fields isolated. A second harness (Claude Code through its SDK) is added only on concrete need |
| Tauri 2 | App and host shell | Stable major version; WKWebView on macOS, WebView2 on Windows | Test interfaces in WebKit and Chromium; bundle a fixed WebView2 runtime on Windows if needed (analysis §11.3) |
| Local model servers (oMLX, LM Studio, Ollama) | Host models; optional App providers | Chat Completions with tool calls; oMLX also serves the Responses API Codex requires | A candidate substitute needs the selected interface/tool-call qualification |
| Pi (MIT) | Upgrade path for the host loop only | Not a dependency at v4.0 | — |

Terms: OpenAI's written position on ChatGPT sign-in in a distributed
third-party application, and Anthropic's on any Claude sign-in, are
unconfirmed (PRD OQ-08). The original seed distinguished the owner's own use from distribution;
this document supplies no legal or supplier-terms conclusion. OQ-08 remains
at its point of need.

## 7. Alternatives set aside

These are the original choice rationales, not current supplier quality
measurements. D-19/D-20 remain intentional decisions. Later consequential
learning can warrant an explicit revision; unselected alternatives do not
become requirements by being recorded.

| Alternative | Why set aside | Where argued |
|---|---|---|
| A standard agent protocol (ACP) between Chirality and the harness | Reintroduces a translation layer that loses native features; the client is not thin | Analysis §9.1 |
| T3 Code as a gateway or a fork | Its interface is an alpha product's internal API facing a large rewrite; a fork would track very high churn | T8; analysis §5 |
| Chirality's own agent loop for the App | Recreates what the best harness provides | Analysis §5, M-1 |
| Pi's libraries for the host loop now | Frequent breaking changes by stated policy; the host needs a small part | T10; analysis §11.1 |
| Electron for the App | Defensible; set aside for one stack across applications | Analysis §11.2–11.3 |
| v3's separate Runtime service | Not selected for the direct-hosting target in D-20; retained-service history is contrary evidence to universal claims against services | T11; analysis §11.2; B-HTML 02 |

## 8. Architecture risks

| Risk | Consequence | Mitigation |
|---|---|---|
| Codex protocol drift between versions | Upgrade work | Pinning, generated types, recorded-exchange tests, isolated experimental fields |
| WebKit on macOS differs from Chromium on Windows | Interface defects on one platform | Test in both engines; packaged-app smoke checks |
| Local models' tool calling is unreliable | Poor or refused proposals in hosts | Few, well-typed tools; strict validation; the host validates every operation; failures reported, not executed |
| Tauri signing and notarisation are new to the App target | Release friction | App owns its package evidence; coordinate reusable knowledge with the external SWBPIPE owner without claiming one project qualifies the other |
| Terms for distributing native sign-in | Limits distribution beyond the owner | Written answers before public release (OQ-08) |
| Cross-host semantics are mistaken for transport success | A catalog or successful call can hide differing basis, validation or outcomes | Define the operation contract and trace a connected candidate, including refusal/unknown paths; V4-PAR-05 remains explicitly open |
| Connector timing or ownership is implicit | Dependent work starts without a usable provider input | Retain actual owner or unresolved allocation, contribution and point of need; first activity proceeds without Domains/PEC, later integration requires its own inputs |
