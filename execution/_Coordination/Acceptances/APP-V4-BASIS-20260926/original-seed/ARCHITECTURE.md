# Chirality v4 — Architecture basis

**Status: DRAFT 1 — candidate, not accepted.** Companion to the
[PRD](PRD.md). It records the architecture the owner chose for v4.0
(D-16…D-20), the reasons, the alternatives set aside, and what is left for
the implementation session. The reasoning in full is in
`conceptual/MAINTAINABILITY_ANALYSIS.md` (§§1–3, 9–11); this document states
the result. Identifiers `V4-ARC-<nn>`.

## 1. Priorities and principles

The owner's priorities, in order (D-16–D-18):

1. **Maintainability** — the ongoing cost, for agents directed by one
   accountable person, of keeping the product correct and current while its
   suppliers, hosts and understanding change.
2. **Functionality** — the best harnesses' native capabilities are kept, not
   traded for portability.
3. **Local models and data privacy** — in host applications the local model
   server is the primary interface, and data goes nowhere else.

Principles that follow (analysis §3, with M-2 as restated in §9.2):

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

These were drawn from where Chirality's maintenance cost actually came from:
owning what a supplier already did, privately modifying a supplier,
generality before need, and process weight (analysis §2).

## 2. Overview

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
                                        Ollama) — or a cloud API if chosen
```

Shared by both tiers: the workflow format with declared checkpoints, skills,
the four roles' guidance, the record format, the capability-catalog contract,
and interface components where they fit (V4-SHR-01, -02).

## 3. The Chirality App

| ID | Decision | Reason |
|---|---|---|
| V4-ARC-01 | **Harness: Codex through the stock Codex App Server**, run from the App's own process, version-pinned, over its published protocol (JSON-RPC over stdio) | D-17, D-19; the v3 replatform showed that hosting the harness stock unblocked the product (analysis §2) |
| V4-ARC-02 | **Shell: Tauri 2 + React + Vite**, the same stack as SWBPIPE | D-20; one packaging pipeline and one main-process language across Chirality applications (analysis §11.2–11.3) |
| V4-ARC-03 | **No separate service.** v3's Node Runtime service and its socket API are not carried forward | Its only reason was reuse by host applications, which D-19 set aside; the v3 record rated the in-process topology "lowest maintenance" (analysis §11.2) |
| V4-ARC-04 | **Sign-in and models through Codex's own account methods**: ChatGPT sign-in and API key, with credentials held by Codex; local model servers as Codex model providers chosen per conversation (`modelProvider` on `thread/start`) | D-06, D-17 |
| V4-ARC-05 | **Native presentation.** Codex's items — plans, tool activity, delegation, requests — are presented in their native form; protocol types are generated from the pinned Codex version, with a small hand-kept supplement for experimental fields | M-2; D-GOV-43 finding 4 (L-05) |

**Properties the App must hold** (from v3's examined behaviour, X-03–X-05):

- The Codex process, the protocol session and the register of outstanding
  requests live in the main process, so that reloading or closing a window
  stops observation, not work, and outstanding approvals survive.
- Every server request is answered or explicitly declined; unknown requests
  receive an explicit error.
- Reconnection recovers actual state from Codex rather than a Chirality copy
  of the transcript.

**What carries over from v3** (T11): the Codex client logic and its restart
and request-answering rules (about 330 lines plus rules, ported); the
instruction composition and role configuration; the workflow catalog and
draft registration; the plan registry; the version-pin check; and the
interface pieces that carry v3's valuable interactions — request cards, the
plan panel, workflow draft review, turn phases and outcome states, attachment
import. **Not carried:** the service, its socket API and client, the Next.js
routes, the translation into Chirality event names, the multi-engine and
delegation layers, and the unreachable legacy code.

**Left to the implementation session:** how responsibilities divide between
the Rust main process and the TypeScript interface beyond the properties
above; whether Chirality keeps sign-in separate from the user's other Codex
clients (v3's overlay home) or shares it; API-key sign-in through the pinned
protocol (v3 used ChatGPT sign-in only); signing and notarisation of the App
and the Codex binaries under Tauri, including the entitlement v3 needed for
Codex's code-mode host; and the pinned Codex version (v3's last qualified pin
was 0.154.0; the upstream release on 2026-09-26 was 0.157.1).

## 4. Host applications

| ID | Decision | Reason |
|---|---|---|
| V4-ARC-10 | **Agent: a minimal Chirality agent loop** in the host, over the **OpenAI-compatible Chat Completions** interface with tool calls | D-20; the most stable interface every local server implements; a few hundred lines agents can read and repair (analysis §11.1) |
| V4-ARC-11 | **Model: the local model server by default**; a cloud model only if the user chooses one and supplies an API key | D-18 |
| V4-ARC-12 | **Network through the host.** The loop's requests pass through the host's own native layer, which enforces the configured endpoint and holds any key outside the interface's script | D-18; T10 risk 3 |
| V4-ARC-13 | **Tools from the host's capability catalog**, with arguments validated against the catalog's schemas before the host's own validation runs | V4-PAR-01…05; [host integration](HOST_INTEGRATION.md) |
| V4-ARC-14 | **A Chirality-defined boundary around the loop** — messages, tools, events, checkpoints — so the loop can be replaced by Pi's libraries or another library if hosts outgrow it | D-20; M-5 |

**Properties the host agent must hold:**

- In local operation it makes no network request other than to the
  configured model server (V4-HOST-02).
- It does not block the host's interface: long parsing and model streaming
  run off the interface's main thread where the host needs it (T10 risk 4).
- It treats truncated or malformed tool calls as failures to report, never
  as empty arguments to execute (T10 §6).
- It records runs in the shared record format, linking the host's receipts.

**Left to the implementation session:** where the loop runs within each host
(interface thread, worker, or native layer); the streaming and tool-call
parsing details; the conversation state and its persistence with the host
project; and the per-host panel built from shared components.

## 5. Shared layer

- **V4-ARC-20** A shared TypeScript layer carries the workflow format and its
  declared checkpoints, role guidance, the record format, the
  capability-catalog contract types, and interface components used by the
  App and hosts. Where it lives in the repository is the implementation
  session's decision.
- **V4-ARC-21** Hosts expose their capability catalog to external agents —
  such as the Chirality App's Codex — through an MCP server, which Codex
  supports natively, or a command-line interface, built from the same catalog
  (SWBPIPE's "controller first" path).
- **V4-ARC-22** Connectors (PEC, Domains) are read through their own
  interfaces; Chirality shows standing and freshness and falls back to files
  ([host integration](HOST_INTEGRATION.md) §8).

## 6. Supplier assumptions and pins

| Supplier | Used for | Assumption | If it fails |
|---|---|---|---|
| OpenAI Codex (Apache-2.0 CLI and App Server) | The App's harness | The App Server protocol stays published and supported for embedding; releases roughly weekly with schema changes | Pin; upgrade deliberately; keep experimental fields isolated. A second harness (Claude Code through its SDK) is added only on concrete need |
| Tauri 2 | App and host shell | Stable major version; WKWebView on macOS, WebView2 on Windows | Test interfaces in WebKit and Chromium; bundle a fixed WebView2 runtime on Windows if needed (analysis §11.3) |
| Local model servers (oMLX, LM Studio, Ollama) | Host models; optional App providers | Chat Completions with tool calls; oMLX also serves the Responses API Codex requires | Any compliant server can be substituted |
| Pi (MIT) | Upgrade path for the host loop only | Not a dependency at v4.0 | — |

Terms: OpenAI's written position on ChatGPT sign-in in a distributed
third-party application, and Anthropic's on any Claude sign-in, are
unconfirmed (PRD OQ-08). Neither affects the owner's own use.

## 7. Alternatives set aside

| Alternative | Why set aside | Where argued |
|---|---|---|
| A standard agent protocol (ACP) between Chirality and the harness | Reintroduces a translation layer that loses native features; the client is not thin | Analysis §9.1 |
| T3 Code as a gateway or a fork | Its interface is an alpha product's internal API facing a large rewrite; a fork would track very high churn | T8; analysis §5 |
| Chirality's own agent loop for the App | Recreates what the best harness provides | Analysis §5, M-1 |
| Pi's libraries for the host loop now | Frequent breaking changes by stated policy; the host needs a small part | T10; analysis §11.1 |
| Electron for the App | Defensible; set aside for one stack across applications | Analysis §11.2–11.3 |
| v3's separate Runtime service | Its premise (reuse by hosts) no longer holds | T11; analysis §11.2 |

## 8. Architecture risks

| Risk | Consequence | Mitigation |
|---|---|---|
| Codex protocol drift between versions | Upgrade work | Pinning, generated types, recorded-exchange tests, isolated experimental fields |
| WebKit on macOS differs from Chromium on Windows | Interface defects on one platform | Test in both engines; packaged-app smoke checks |
| Local models' tool calling is unreliable | Poor or refused proposals in hosts | Few, well-typed tools; strict validation; the host validates every operation; failures reported, not executed |
| Tauri signing and notarisation are new to the project | Release friction | Established once for the App and SWBPIPE together |
| Terms for distributing native sign-in | Limits distribution beyond the owner | Written answers before public release (OQ-08) |
