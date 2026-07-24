# D-GOV-20 — Shared Runtime and Local-Agent Pilot

**Status:** RULED
**Date:** 2026-07-22
**Decision ID:** D-GOV-20
**Owner:** Ryan Tufts
**Companion rulings:** D-APP-73, D-T0-23, D-PEC-56
**Scope snapshot:** `projects/chirality-app-dev/execution/_ScopeChange/SCA-APP-003_2026-07-22_Shared_Runtime_Local_Agent_Pilot/`

## Owner direction

The owner supplied the decision-complete “Chirality Shared Runtime and Local-Agent Pilot” plan and explicitly instructed:

> PLEASE IMPLEMENT THIS PLAN

This is the owner act. This record transcribes its root-governance effect.

## Ruled architecture

1. Chirality’s executable agent harness becomes a root-owned `runtime/` workspace with provider-neutral contracts, orchestration, daemon, client, CLI, and safe engine adapters.
2. One opt-in per-user headless daemon exclusively owns runtime engines, credentials, sessions, delegation, tools, turn locks, interruption, and local-model residency.
3. The packaged Electron application supplies daemon mode so the existing app identity and encrypted `safeStorage` credential boundary remain single-owner.
4. Local control uses an authenticated project-scoped HTTP/1.1 API over a protected Unix-domain socket. No TCP control listener is authorized.
5. Runtime state beneath user data is operational and non-authoritative. Governed project truth, manifests, instructions, AgentRuns, approvals, and acceptance evidence remain checkout-contained.
6. Tracked `chirality.project.json` manifests declare stable project identity and authority references without secrets or machine-specific absolute paths. Registration stores resolved local paths and approval metadata outside the checkout; authority-affecting manifest changes require explicit re-registration.
7. Agent 0, Agent 1, and Agent 2 remain authority and responsibility contracts independent of engine or model. No durable model-to-role preference is established.
8. Humans and external agents may invoke Agent 1 directly; Agent 0 may govern Agent 1 managers; Agent 1 may delegate Agent 2 workers; Agent 2 may not delegate.
9. The initial vertical slice is one real Agent 1 run that delegates one bounded read-only task to one Pi/oMLX Agent 2 using the explicitly resident model, reviews the return, and emits canonical evidence and actual-model attribution.
10. The generic runtime, CLI, contracts, and safe adapters are eligible for the public Chirality App export. Credentials, machine state, and private PEC or Piping adapters are excluded.

## Local residency boundary

- The daemon manages at most one primary local LLM at a time.
- Activation is explicit; a run never loads, unloads, switches, aliases, or falls back automatically.
- Exact model IDs come from authenticated loopback oMLX status. Redirects, embedded URL credentials, remote hosts, and unsupported protocols remain denied.
- Switching drains active Pi turns within the ruled timeout, never force-interrupts them, and fails closed. A failed load after successful unload leaves `NO_MODEL`.
- Unknown helper, embedding, or reranking models are never unloaded automatically.
- Every transition appends redacted evidence and assigns a residency epoch referenced by local sessions and AgentRuns.

## Preserved authority

- D-GOV-11, D-GOV-12, and D-GOV-17 remain in force: hierarchy governs authority, delegation is bounded and evidenced, and actual models are attributed without becoming durable role doctrine.
- JSON/JSONL project evidence remains authoritative over daemon databases or caches.
- Project-specific tools and deterministic acts remain owned by their project/domain adapters and cannot be elevated by generic runtime transport.
- Human acts, release acts, lifecycle transitions, professional reliance, and production-data authority are not delegated by this ruling.

## Explicit exclusions

This ruling does not authorize automatic model scheduling, multiple simultaneous primary local LLMs, local Agent 1, piping, silent adapter fallback, remote oMLX, credential input through the initial CLI, production PEC mutation, or release/publication/issuance.

## Implementation gates

Governance convergence precedes runtime extraction. D-APP-72 closes independently before behavior-preserving promotion. Shared contracts and lockfiles have one serialized integration owner. Daemon/client/CLI, Desktop migration, PEC migration, security review, and regression review remain separately bounded. Public export occurs only after the app-dev and PEC vertical slices pass.
