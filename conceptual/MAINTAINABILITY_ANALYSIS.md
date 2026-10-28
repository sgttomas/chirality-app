# Maintainability as the governing criterion — analysis

> **Revised 2026-09-26 after the owner's challenge (D-17).** The two-seam
> recommendation in §4–5 (ACP between Chirality and the agent) is withdrawn;
> see §9 for why it was wrong and the revised direction. §1–3 stand, with
> principle M-2 restated in §9.2; §7 is revised by §9.4. §10 (after D-18)
> separates the Chirality App's agent from the host applications' agent.
> §11 records the evidence after D-19; the owner chose §11.1 option M and
> §11.2's Tauri recommendation (D-20).

Standing: **interpretation and proposal (agent).** Written in response to
D-16 ("code maintainability is top of my concerns … The best ability is
maintainability"). It proposes principles and an architectural seam for the
v4 basis; nothing here is accepted until the owner says so. Facts about
external projects come from their published documentation and repository
metadata, read on 2026-09-25/26, and from T7 and T8; none has been tested
locally.

## 1. What maintainability has to mean here

The owner maintains Chirality through agents, as one accountable person
(AT §1 items 2 and 4). So maintainability is not a property of code alone. It
is **the ongoing cost and risk, for agents directed by one person, of keeping
the product correct and current while its suppliers, host applications and
the owner's own understanding keep changing.** That cost has six parts:

| Part | The question it asks |
|---|---|
| Owned code | How much must Chirality itself write, read, test and repair? |
| Imported change | How often do suppliers change something Chirality must follow, and how much work does each change cause? |
| Coupling | Where Chirality touches a supplier, is the seam a published, versioned, multi-vendor contract — or a product's internal API or a private modification? |
| Replaceability | If a supplier fades, changes terms or falls behind, what does it cost to swap it? |
| Comprehensibility | Can a fresh agent (or the owner) understand a part from the repository alone — conventional stack, standard formats, small modules? |
| Process weight | How much record-keeping, review and evidence work does every change carry? |

"Ability" (what a harness can do today) is a snapshot. Maintainability is
the rate at which that ability stays available at acceptable cost. That is
the sense in which "the best ability is maintainability."

## 2. Where Chirality's maintenance cost actually came from

The record is unusually clear. Across four generations the cost came from
the same four sources — **none of them a lack of capability**.

| Source | Evidence |
|---|---|
| **Owning what a supplier already does** | v1 ran a custom Anthropic loop, then a CLI subprocess, then cut over wholesale to the Claude Agent SDK "with no dual runtime path" to avoid "regression drift and duplicated maintenance" (`ORIG/.archive/frontend/docs/harness/harness-decisions.md` D-017; T4). v2's daemon re-derived state that Codex already persists (D-GOV-43 finding 5). |
| **Privately modifying a supplier** | The v3 daemon ran a patched Codex App Server "with private protocol extensions" that had to be re-patched on every upstream release and fell five releases behind (D-GOV-43 finding 3; T3, T5). |
| **Generality before need** | A provider-neutral engine vocabulary "retained from the Claude SDK and Pi eras" left Codex items with nothing to render them (D-GOV-43 finding 4); about 6,000 lines of multi-engine harness code remain reachable only from tests, and two engine packages compile but are wired to nothing (T3 R3; T5 §1.5). A2 kept about 2,600 lines of transport for future embedders that do not exist yet (T3 R1). |
| **Process weight** | About 1,022 governance artifacts by 2026-08-01, 30.1 % of changed lines in the one measured window; an early estimate of ~75 % of agent tokens spent on context, documentation and audits; 54 App deliverables never issued; 1,044 of 3,217 deliverable claims found stale (T3 §4–5; T4 §4). |

And the one change that most improved things was the opposite of all four:
D-GOV-43 deleted the daemon, the patches, the filters and the configuration
veto, hosted the supplier **stock** through its **published protocol**, and
the release followed within days (T3 §5; `APP_V3_CODEX_HOST_REPLATFORM_20260912/RUN_LOG.md`).

## 3. Proposed maintainability principles

| # | Principle | Lesson it answers |
|---|---|---|
| M-1 | **Own only what is distinctively Chirality's**: the workflow layer, the human–agent interface, the host-integration contracts, and the records of human acts. Everything a capable harness already does belongs to the harness. | Owning supplier functions |
| M-2 | **Meet every supplier at a published, versioned contract** — preferably one several vendors implement. Never at a product's internal API; never through a modified build. | Private modification; T3 Code's alpha internal API |
| M-3 | **Keep knowledge in open, harness-neutral formats**: `AGENTS.md`, `SKILL.md`, `WORKFLOW.md` (with its declared checkpoints, D-03), MCP tool schemas. Methods then survive any harness change. | Engine-specific vocabularies |
| M-4 | **Do not fork fast-moving upstreams.** Wrap them through their protocols, or contribute. | Re-patching every release |
| M-5 | **Generality only through standards.** Build for the harness in hand; let a standard protocol, not Chirality code, supply the ability to change harness later. | Speculative multi-engine layers |
| M-6 | **Few stacks, mainstream tools.** Every additional language, runtime or framework is a maintenance surface for agents; prefer what agents already read and write reliably, and avoid release-candidate frameworks. | Electron + Next + Node service + daemon for one consumer |
| M-7 | **Seams tested without live models.** Record real protocol exchanges once; test Chirality's side against them deterministically; keep live-model checks few and deliberate. | CI that could not exercise the real path |
| M-8 | **Records proportionate to decisions.** Keep what a later reader needs to reconstruct a human act or a reliance claim; nothing that no one reads. | Process weight; emission without consumption (L-06) |

## 4. Where the seams should be

Applying M-1 to M-5 to what Chirality must do puts two seams around the
harness, and both already have multi-vendor standards:

```text
 Professional
     │  (the application's own interface + the Chirality panel)
     ▼
 ┌──────────────────────────────┐
 │ Chirality client             │  owns: conversation and plan view, workflow
 │ (in each host, and the       │  selection and declared checkpoints, the
 │  standalone Workflow App)    │  four roles as instructions, records of
 └──────────────┬───────────────┘  human acts
                │  Agent Client Protocol (ACP)   ◄── seam 1
                ▼
 ┌──────────────────────────────┐
 │ Any ACP agent (the harness)  │  Codex (codex-acp), Claude Code
 │                              │  (claude-agent-acp), OpenCode, goose,
 │                              │  Gemini CLI, Copilot, Cursor, …
 └──────────────┬───────────────┘
                │  Model Context Protocol (MCP)  ◄── seam 2
                ▼
 ┌──────────────────────────────┐
 │ Host tools, per application  │  SWBPIPE: inspect, preview, submit
 │ (and connectors)             │  proposal, status; Domains: search;
 └──────────────────────────────┘  PEC: read-only coordination state
```

**Seam 1 — Chirality to the agent: ACP.** Verified from the protocol's
documentation and repositories (2026-09-26):

- A client starts a session with a working directory **and a list of MCP
  servers the agent should connect to**; the specification says clients
  "MAY use this ability to provide tools directly to the underlying language
  model by including their own MCP server." Every ACP agent must support MCP
  servers over stdio; HTTP is optional.
- The protocol carries what Chirality's interface needs: prompts and
  streamed updates (messages, tool calls, **plans**, mode changes),
  **permission requests** answered by the client, cancellation, optional
  session loading (resume), modes, authentication, and optional client-side
  file and terminal access.
- 37 agents are listed as implementing it natively (among them Gemini CLI, GitHub
  Copilot, goose, OpenCode, OpenHands, Cursor, Cline, JetBrains Junie, Mistral
  Vibe, Qwen Code); Claude Code, Codex and Pi through adapters.
- The adapters are maintained in the protocol's own organisation:
  `claude-agent-acp` (Apache-2.0) and `codex-acp` (Apache-2.0, copyright
  JetBrains). `codex-acp` offers **ChatGPT login, API key, or a custom
  OpenAI-compatible gateway**, a configurable model provider, plans,
  permission requests, skills, and client-provided MCP servers over stdio
  and HTTP. `claude-agent-acp` offers permission requests, nested subagent
  transcripts and client MCP servers.
- Rust and TypeScript SDKs exist (Apache-2.0), which fits a Tauri host
  (Rust) and a web interface (TypeScript) alike. The protocol is at version 1;
  it originated at Zed, and JetBrains became co-lead maintainer in February
  2026 (T7, from a third-party report).

**Seam 2 — the agent to the host: MCP.** The host's typed operations become
an MCP server. SWBPIPE's owner-accepted "CLI first over the live controller"
seam (inspect, preview, submit, status; no agent Apply; basis binding) maps
onto this directly: a small stdio MCP server can be a thin shim over the same
private bridge. Connectors fit the same seam: Domains as a search tool, PEC
as a read-only tool (PEC's own agent access class is designed for tool
calls, D-PEC-90). The owner's condition on SWBPIPE applies: any MCP adapter
must meet the current stateless protocol, which some bundled clients have
failed.

**What the owner's requirements become under this seam:**

| Requirement | How it is met | Chirality code needed |
|---|---|---|
| Not locked to one provider (D-05) | Any ACP agent; the user chooses per conversation | None beyond the ACP client |
| OAuth, API key and local, possibly at once (D-06) | Codex via `codex-acp` (ChatGPT, API key, custom gateway/provider); Claude Code via `claude-agent-acp` (the user's own sign-in or key); local through an agent with native local-model support (OpenCode, goose) or Codex's custom provider or Claude Code's base URL | Configuration only |
| Local model server required (D-05) | As above; the local server is the user's choice (oMLX, LM Studio, Ollama) | Configuration only |
| Host tools in SWBPIPE (D-02) | Host MCP server passed at session start | The host's MCP server (owned by the host project) |
| Declared checkpoints enforced (D-03) | Permission requests arrive at the client, which knows the workflow's declared checkpoints; the host enforces its own acts (Apply, Checked) | Chirality's checkpoint handling |
| Graduated autonomy (D-04) | Per-session agent modes and permission policy, chosen by the user; the client answers or forwards permission requests | Small |
| Records (D-07) | One normalised event stream (ACP `session/update`) for every agent, linked to host receipts | One recorder, not one per vendor |

## 5. The options, scored against the six parts

Qualitative; the reasoning is in the cells. "Owned code" counts only what
Chirality maintains.

| Option | Owned code | Imported change | Coupling | Replaceability | Comprehensibility | Notes |
|---|---|---|---|---|---|---|
| **A. ACP client + MCP host tools** | Smallest: an ACP client and the Chirality layer | Adapter and protocol releases, absorbed by their maintainers; Chirality follows protocol versions | Multi-vendor standard, versioned | A different harness is a configuration change | Standard formats and SDKs in mainstream languages | Lowest common denominator: vendor-only features beyond ACP are not used (see §6) |
| **B. Stock Codex App Server directly (the v3 path)** | Moderate: a Codex client plus v3's Runtime service if kept | Weekly Codex releases with schema drift (T7); Chirality regenerates and adapts | One vendor's published protocol | Changing harness means a second client | Known to this project | Richest Codex features (application tools, per-conversation provider, native plan mode); Claude models unreachable |
| **C. T3 Code as a gateway (`t3 serve`)** | Small, but a client for T3's API | Very high: alpha 0.0.x, ~1,500 commits a month, a pending rewrite of ~+341k/−171k lines, API not declared stable (T8) | A product's internal API, built on a release-candidate framework | Good across providers, but only through T3 | Large, unfamiliar framework (Effect 4 RC) | T3 itself uses ACP for several providers and is adding a generic ACP provider in its rewrite |
| **D. Fork T3 Code** | Very large (~0.5M lines of TypeScript) | Continuous rebasing against that churn | Private modification | Poor | Poor | The v3 patched-supplier lesson at a larger scale |
| **E. Own agent loop on a framework** | Largest: tools, sandbox, approvals, sessions | Model and framework APIs | Low-level, many | Good for models, poor for everything else | Depends on the team | Recreates what harnesses provide (M-1) |

On this reading, **option A serves the owner's reasons for liking T3 Code**
— many agents, no provider lock-in, less code in Chirality — **better than
T3 Code itself does**, because it reaches the same agents through the
standard T3 is itself converging on, rather than through T3's internal API.
T3 Code remains valuable as MIT-licensed reference code (provider-instance
and credential handling, the Codex sign-in overlay v3 already borrowed, UI
patterns) and as an app users may choose on their own.

## 6. What option A gives up, and what would answer it

| Given up or uncertain | Consequence | How to settle it without experiments |
|---|---|---|
| Vendor features beyond ACP: Codex application tools, per-conversation provider switching inside one server, Codex's native plan mode | Host tools move to MCP (the more portable route anyway); plans arrive as ACP plan updates; provider choice is per agent session | Read the adapters' feature lists and ACP's extension mechanism (both adapters already publish extensions for permissions and configuration) |
| Adapter lag behind vendor releases | New vendor features arrive later | Read the adapters' release history against the vendors' |
| Subagent visibility is a draft capability | Delegation inside the agent is less visible to the client | Read the draft and the adapter notes (claude-agent-acp documents its interim mechanism) |
| ACP began in editors (files, terminals, diffs) | Engineering objects do not fit ACP's primitives | They do not need to: domain objects travel over MCP, not ACP |
| MCP version support differs by agent | A host server may fail with an older client (SWBPIPE saw this) | Read each candidate agent's MCP support; require the current protocol |
| Terms for third-party clients using consumer sign-ins | Unchanged by the protocol choice: the adapter still uses the user's sign-in | Written confirmation from OpenAI and Anthropic, if and when v4 is distributed to others |
| Local-model quality | Outside Chirality's control under every option | Not a maintainability question |

## 7. Consequences for the rest of the architecture

- **The v3 Runtime service may no longer be needed.** With ACP, a host
  launches the agent (or its adapter) as a subprocess and speaks to it
  directly; Chirality's layer can live in the client. Removing a Node
  service from every host is itself a maintainability gain (M-1, M-6).
  To confirm by reading the Runtime's current responsibilities against ACP.
- **One interface component set for all hosts.** SWBPIPE is Tauri (Rust +
  React). If the Chirality panel is a React component set and the ACP client
  logic is small, the same pieces serve SWBPIPE and the standalone Workflow
  App. Building the standalone app on the same stack (Tauri) rather than v3's
  Electron + Next would leave one stack across every Chirality application.
  This is an option, not a finding.
- **Host integration belongs to each host project.** SWBPIPE owns its MCP
  server, as it owns its live controller today; Chirality owns the contract
  shape they share (inspect, preview, submit, status, basis binding).
- **Records get simpler.** One normalised stream from ACP for every agent,
  plus the host's own receipts (D-07), instead of one vocabulary per vendor.
- **Process weight is part of maintainability.** The build-method
  conversation (Q-11) should be judged by the same measure: every record
  should serve a decision, a reliance claim or recovery (M-8).

## 8. Questions for the owner

1. Do these eight principles express what you mean by maintainability, or
   would you change or rank them?
2. Should the v4 basis adopt the two seams — ACP to the agent, MCP to the
   host — as the architectural direction, with the particular agent left to
   the user's configuration?
3. Should the standalone App for Creating Workflows share SWBPIPE's stack
   (Tauri + React), so every Chirality application runs on one stack?

## 9. Revision after the owner's challenge (2026-09-26)

The owner rejected the ACP direction: building the ACP layer would be hard;
losing native Codex functionality is a big loss because "Those harnesses are
the best in the world"; native OAuth is essential; the aim is "to build
around the best harnesses in the world in the easiest to maintain manner"
(D-17, maintainability first, functionality second).

### 9.1 Why the ACP recommendation was wrong

1. **It repeated this project's own mistake.** D-GOV-43 found that v3's
   generic, multi-engine event vocabulary left Codex items "with nothing to
   render them" (finding 4). ACP is a better-maintained generic vocabulary,
   but an adapter still maps Codex's native items into it, and whatever ACP
   does not model is dropped or pushed into extensions. That is the same
   translation layer, maintained by someone else.
2. **It traded a certain loss for a hypothetical gain.** Replaceability of the
   harness is a benefit only if the harness has to be replaced. Losing native
   features (application tools, per-conversation model provider, native plan
   mode, the full event stream) is certain and immediate. Under M-5 —
   generality only on demand — the proposal failed its own test.
3. **It understated the client work.** An ACP client that renders every
   update, answers permissions, handles authentication and sessions, and then
   uses vendor extensions to recover lost features is substantial code, not a
   thin layer.
4. **It added a dependency.** Each adapter is a third party between Chirality
   and the harness, with its own release lag and its own defects.

### 9.2 Restated principle M-2

> **Meet each harness at its own published embedding interface, unmodified
> and pinned, and pass its native items through to native presentation.**
> No private modification, no generic vocabulary between Chirality and the
> harness.

Portability is sought where it costs no functionality: in content and host
tools, which the best harnesses already share natively — `AGENTS.md`,
skills (`SKILL.md`), workflow packages as files, and MCP servers.

### 9.3 The revised direction (proposal)

| Layer | Direction | Why it is maintainable | Functionality kept |
|---|---|---|---|
| Harness | **Codex through the stock Codex App Server**, pinned, over its published protocol (the v3 D-GOV-43 path) | A supported embedding surface; protocol types generated per version (`codex app-server generate-ts`); upgrades are deliberate dependency bumps, tested against recorded exchanges; experimental fields isolated | Full native loop, sandbox and approvals, plans, subagents, hooks, resume and fork, application tools, the full event stream |
| Sign-in | **Native OAuth** through Codex's own account methods (ChatGPT sign-in), plus API key; credentials held by Codex, kept separate from the user's other Codex clients (v3's overlay) | Codex owns credential handling | Native OAuth, as shipped in v3 |
| Local models | **Codex's own model providers**, chosen per conversation (`modelProvider` on `thread/start`); oMLX serves the Responses API Codex requires, as do LM Studio and Ollama | Configuration, not code | Local and cloud conversations side by side in one harness |
| Host tools | **MCP servers owned by each host** (SWBPIPE: inspect, preview, submit, status), with Codex's native application tools available where a host needs them to pass through Chirality | MCP is native to both leading harnesses; the host's server outlives any harness choice | Nothing lost; both routes are native |
| Knowledge and methods | `AGENTS.md`, skills, workflow packages as files | Read natively by the leading harnesses | Nothing lost |
| A second best harness | **Claude Code through the Claude Agent SDK**, added as a second native adapter **when there is a concrete need** — not built in advance | One more pinned, published interface; T3 Code's MIT adapters show the shape | Claude Code's native features, including its subagents and hooks |

**Honest limits of this direction:**

- It depends on OpenAI's continued support of the App Server protocol and on
  weekly Codex releases with schema drift; pinning makes upgrades
  deliberate but not free.
- Claude models are not available through the Codex harness. Claude Code
  natively means a second adapter. Anthropic's documentation does not allow
  third-party products to offer claude.ai sign-in without approval, so
  native OAuth for Claude in a distributed product needs Anthropic's written
  answer; API keys are clearly permitted.
- Codex's own sign-in inside a third-party app is shipped in v3 and described
  in OpenAI's App Server documentation; commercial terms for a distributed
  product were recorded as unconfirmed and still need OpenAI's written
  answer before wide release.

### 9.4 What this changes elsewhere

- **The v3 App Server work is an asset, not history.** The A2 service,
  the authentication overlay, request cards, plan handling and application
  tools are the tested base (S-1…S-8). The open maintainability question is
  narrower: whether every host needs v3's Node service, or whether a host can
  run the Codex binary directly and share one client library (a Tauri host
  already runs native binaries as sidecars). To settle by reading the Runtime's
  responsibilities, not by experiment.
- **Q-05 settles toward option A of the original question** (build on the
  incumbent) with M-5 governing any second harness.

## 10. Two agent tiers (after D-18, 2026-09-26)

The owner separated the two expressions: the Chirality App wraps the full
Codex experience; SWBPIPE may have a simpler agent with local models, and a
third priority applies there — the local model server as the primary
interface, a good experience that keeps up with developments, no dependence
on a third-party harness that sends data elsewhere, and **semantic parity**
(the agent can take the same actions as the human user).

### 10.1 Was the first proposal discarded too quickly?

In part. Its **insight** was right for hosts: a host should not be tied to one
vendor's heavy harness, and the host's operations should be defined once,
independently of any harness. Its **mechanism** is still not the best fit,
even for hosts. ACP puts a separate agent program — a coding harness with its
own shell and file tools, and its own network behaviour — between the host
and the model. For a local-first, private, simple agent that is one layer and
one data path too many. The simplest maintainable arrangement for a host
takes the model access and agent loop as a **library inside the host**, not a
harness beside it.

### 10.2 The host tier (proposal)

| Element | Proposal | Evidence and standing |
|---|---|---|
| Agent loop and model access | Pi's libraries, used inside the host: `pi-ai` (unified model API; custom providers for "local inference servers, proxies, or any OpenAI/Anthropic-compatible endpoint"; documented browser support) and `pi-agent-core` ("stateful agent with tool execution and event streaming") | Repository `earendil-works/pi`, MIT, read 2026-09-26; not the Pi coding-agent app. Chirality's Runtime ran Pi 0.82.0 against a loopback oMLX in a live validation (`projects/chirality-runtime/README.md` L131–136, historical record) |
| Model | The local model server by default (oMLX, LM Studio, Ollama); a cloud model by API key only if the user chooses | Configuration |
| Privacy | The library calls only the endpoint the host configures; Pi's telemetry package defines contracts with a no-op default and no exporter. The host can restrict network access to the local server | `packages/telemetry/README.md`; SWBPIPE's webview currently has no content-security policy (T6), which the host would set |
| Tools | **Generated from the host's own capability catalog** — the same definitions the human's interface uses (below) | SWBPIPE already has a capability catalog with disabled reasons and one applier route for every mutation (T6) |
| Experience | Simpler than Codex: conversation, workflow selection, proposal queue, checks, beside the host's own overlays (proposed rows, origins, checked tags — X-07) | Owner direction 2026-09-17 |
| Methods | The same workflow files, skills and role instructions the Chirality App uses | D-03, D-10 |

Maintainability of this tier: Chirality owns the tool binding, the workflow
and checkpoint handling and the panel; Pi owns model access and the loop and
keeps them current with new providers and models. Pi is pre-1.0 and releases
several times a week, so it is pinned and upgraded deliberately behind a thin
boundary; if it faltered, what sits behind that boundary is small enough to
replace with another library or a few hundred lines of Chirality's own. That
is a far smaller exposure than a harness application.

What the host tier gives up: a sandboxed shell and file editing (not needed —
the host's operations are the only actuators), and the harness-level depth of
Codex (long-horizon planning, compaction, subagents), which the owner
accepts for hosts. The agent's quality rests on the local model's tool
calling; the host validates every operation, so a weak model produces
refused or poor proposals, not damage.

To check by reading before relying on it: whether `pi-agent-core` itself
runs in a browser environment (its model library documents this; its
dependencies suggest it may, but it is not stated), or whether the host runs
it in a small Node process; and Pi's release notes for breaking changes.

### 10.3 Semantic parity, defined for the PRD

1. **One capability catalog per host.** Every operation a human can perform
   is described once: name, inputs, preconditions and disabled reasons,
   effects, result, errors.
2. **Same perception.** The agent reads the same views the human reads —
   tables, results, diagnostics — with the same standing marks.
3. **Same route.** Agent operations pass through the same validation and
   applier as the human's, with the same outcomes and errors.
4. **Three consumers of one definition.** The host's interface (the human),
   the host's embedded agent (tools), and an external agent such as the
   Chirality App's Codex (through the host's MCP server or CLI — the
   "controller first" path already adopted for SWBPIPE).
5. **Only human acts differ.** Accepting a proposal (within the autonomy the
   user has set, D-04), marking work checked, approving or relying on a
   result remain the human's acts; the agent can prepare them, never perform
   them in the human's name (the invariant awaiting confirmation, Q-04).

Defining parity once is itself the maintainable choice: a new operation added
for the human becomes available to both agents without separate work.

### 10.4 The whole picture

| | Chirality App (for creating workflows) | Host applications (SWBPIPE first) |
|---|---|---|
| Agent | Codex, stock App Server, pinned (§9.3) | Pi libraries inside the host (§10.2) |
| Models | The user's Codex sign-in, API key, or a local provider | Local model server by default; cloud by API key if chosen |
| Sign-in | Native OAuth through Codex | Not needed for local use |
| Experience | Full Codex: plans, approvals, subagents, tools | Simpler: conversation, workflows, proposals, checks, host overlays |
| Actions | Codex's own tools, plus hosts' MCP servers | The host's capability catalog |
| Shared | Workflow files with declared checkpoints; skills; the four roles' instructions; record format; the capability-catalog contract; panel components where they fit |

## 11. Evidence after D-19 (T10, T11) — two choices to put to the owner

Two reading investigations were run after the owner accepted the two-tier
direction. Neither changes the structure of D-19. Each bears on one choice
inside it.

### 11.1 The host tier: Pi, or a minimal loop of Chirality's own

**What T10 found about Pi** (`earendil-works/pi@d6af72e`, all packages 0.87.1):

- **It fits technically.** `pi-agent-core` runs in a browser from its root
  entry; Node-only code sits behind separate entry points, and Pi's own CI
  checks that the browser bundle resolves. `pi-ai` documents browser use.
  Nothing in the model library, agent library or telemetry package sends data
  anywhere but the configured endpoint by default.
- **It changes fast and says so.** Its release policy states "`minor` =
  breaking changes. No major releases", and its contributor guide says "Do
  not preserve backward compatibility unless the user asks for it" (both
  verified by HELPS_HUMANS). In four months: 41 releases across 12 minor
  versions, each allowed to break, and breaking changes also in four patch
  releases. The agent library changed its session model, turn-ending API and
  stream-function contract; the model library changed its context type and
  provider API.
- **Maintenance is concentrated and gated.** One maintainer holds most of
  the commits; reports from new contributors are closed automatically; the
  owning company plans paid tiers beside the MIT core.
- **Local-model tool calling has open issues**: truncated or fenced
  arguments silently becoming empty, quadratic re-parsing that freezes the
  interface, provider-specific fields rejected by compatible servers. A
  keyless local server needs a placeholder key.
- Chirality's earlier Pi integration used the Node-only coding-agent package
  and bypassed Pi's transport; it cannot be reused in a webview.

**What that means.** A host agent needs a small part of Pi: a loop that sends
messages, receives streamed tool calls, validates arguments against the
host's catalog, and calls the host's operations. Pi supplies that loop plus a
great deal the host does not use, under a policy of frequent breaking change.
The one interface every local server implements — OpenAI-compatible Chat
Completions with tool calls — has been stable for years.

| Option | Maintainability | Functionality | Local and private |
|---|---|---|---|
| **P. Pi libraries (as accepted in D-19)** | Upgrades are frequent breaking work, or pinning forgoes "keeping up"; large install footprint; fixes depend on a small gated team | Richer loop, multi-provider, and future session and compaction features | Good; the host must still route requests through its own process to control the endpoint |
| **M. A minimal Chirality loop over Chat Completions, with Pi as the upgrade path** | A few hundred lines agents can read and repair; one stable wire format; Chirality fixes local-model quirks itself | Enough for a simpler host agent; richer features added only when needed, possibly by adopting Pi then | Best; no third-party code between the host and the model |

**Recommendation: M.** The same boundary serves both: Chirality defines the
host agent's interface (messages, tools from the catalog, events,
checkpoints), so moving to Pi later is a contained change if the host agent
outgrows the minimal loop. This is M-5 — generality only on need — applied
to the host tier. **The choice is the owner's**, because D-19 named Pi.

### 11.2 The Chirality App: topology and stack

**What T11 found about v3** (`2b0572fe0`):

- v3 kept a separate Node service ("A2") on one premise, stated in its own
  record: "B remains the smaller choice only if the embedding intent is set
  aside." D-19 sets that intent aside — hosts use their own local agent — so
  the in-process topology ("B": the App's main process runs Codex directly)
  is now the lower-maintenance choice. The v3 record rated B as one process
  and "lowest maintenance".
- Of the Runtime's 20.2k source lines, about 4.8k are unwired and about 3.7k
  exist only for the service's socket boundary; the Codex client itself is
  about 330 lines. Codex is a native binary and does not need Node; only the
  service did.
- v3's valuable interface pieces (request cards, plan panel, workflow draft
  review, turn phases) port to another shell with modest change; its coupling
  to Next.js is shallow. The parts built on v3's translated event vocabulary
  would be rebuilt on Codex's native items, as M-2 requires anyway.

**The stack choice:**

| Option | For | Against |
|---|---|---|
| **Electron, in-process (drop Next and the service)** | Signing, notarisation and bundling of the Codex binaries are proven and scripted; the Node Codex client moves into main almost unchanged | Two application stacks across Chirality (Electron here, Tauri in SWBPIPE) |
| **Tauri + React/Vite (SWBPIPE's stack)** | One stack across every Chirality application; the Codex binary fits Tauri's sidecar model; components and panels can be shared with hosts | Signing and notarisation must be established for Tauri (SWBPIPE ships unsigned today, so that work would serve it too); the Codex host logic moves to Rust or runs in the webview with Rust piping its input and output; React 18 to 19 alignment |

**Recommendation: Tauri + React/Vite with the in-process topology.**
Maintainability is the first priority, and one stack serves it for as long as
Chirality lives; the extra cost is largely once-only. **The choice is the
owner's.**

### 11.3 Windows and the native-webview question (owner's reservation, 2026-09-26)

The owner asked how much risk Tauri's use of each platform's own web engine
poses for future Windows versions of the applications.

**Facts** (Tauri documentation, retrieved 2026-09-26; SWBPIPE at `2b0572fe0`):

- Tauri uses **WKWebView** (Safari's engine) on macOS, tied to the macOS
  version; **WebView2** (Microsoft Edge, i.e. Chromium) on Windows, evergreen
  and preinstalled on Windows 11; and WebKitGTK on Linux, which varies by
  distribution (`v2.tauri.app/reference/webview-versions/`).
- On Windows, Tauri can instead **bundle a fixed WebView2 runtime** (about
  180 MB) for version control and offline installs
  (`v2.tauri.app/distribute/windows-installer/`).
- A Tauri runtime that bundles Chromium (CEF) is **not official**; a community
  runtime exists and is verified on Linux only (tauri-apps issue #14963;
  `SableClient/tauri-runtime-cef`).
- **SWBPIPE's end-to-end tests run only in Chromium**, against the Vite
  development server (`apps/desktop/playwright.config.ts`: projects
  `chromium-desktop` and `chromium-compact`), while the shipped macOS app runs
  in WKWebView.

**Reading:**

1. **Windows is the lower-risk step for the web engine.** Under Tauri, Windows
   runs Chromium — the same engine Electron bundles and SWBPIPE's tests use.
   The engine that differs is **macOS's WebKit**, the platform shipped first.
2. **The divergence is present today, not a future Windows problem.**
   SWBPIPE ships on WebKit and tests on Chromium, so WebKit-specific defects
   can reach users unexamined.
3. **The Chirality App's shell choice does not remove the WebKit question.**
   Panel components shared with SWBPIPE must work in WebKit whichever shell
   the App uses. Electron would remove it only for App-only interface code.
4. **The mitigations are ordinary and cheap:** run the interface tests in both
   engines (Playwright's WebKit build is close to, though not identical with,
   WKWebView); a short smoke check of each packaged application on each
   platform; conservative web features, with Tauri's own file, dialog and
   clipboard interfaces instead of browser ones; and a fixed WebView2 runtime
   on Windows if exact versions matter.
5. **The larger Windows questions lie elsewhere:** oMLX runs only on Apple
   Silicon, so Windows users would use Ollama, LM Studio or llama.cpp — which
   the Chat Completions interface (§11.1, option M) already covers; code
   signing and SmartScreen reputation on Windows apply to either shell; Codex's
   Windows behaviour (notably sandboxing) is to be read up when Windows enters
   scope.

**Effect on §11.2.** The shell decision is less consequential than §11.2
implied, because the shared parts — React panels, TypeScript client logic,
the workflow layer — are shell-independent when kept behind a small shell
interface (as v3's `window.chirality` bridge already is). The choice turns on
packaging and main-process language: Tauri gives one signing pipeline and one
main-process language across all Chirality applications; Electron keeps
v3's proven signing of the Codex binaries and its Node code, and one engine
for App-only screens. Both are defensible; the recommendation stays Tauri,
with lower confidence, and the owner's preference on engine uniformity is a
sufficient reason to choose Electron for the App.

