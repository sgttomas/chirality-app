# Owner decisions requested — APP-V4-FIRST-INCREMENT-20260928

Prepared by HELP_HUMAN, 2026-09-28. **Answered:** the owner selected the
recommended option for D1–D4; see [OWNER_DECISIONS.md](OWNER_DECISIONS.md).
The text below is the package as presented.
Wave 1 of the [work graph](../../WorkGraphs/APP-V4-FIRST-INCREMENT-20260928/WORK_GRAPH.md)
proceeds without these answers; unruled values stay `UNRESOLVED` in the drafts.
The answers change what is finalized in Wave 2 and whether the pin spike runs.

## D1 — Scope of this first undertaking

| Option | Contents | Trade-off |
|---|---|---|
| **A (recommended)** — App/host contract spine | DEL-04-01, 04-02, 04-03, 03-01, 03-02, 03-03, 03-04, 02-01, 02-03, 05-01, 05-02, 01-01 (boundary + pin), 09-06, 09-09 | Covers every contribution the connected activity needs from the App/shared side, plus both DAG roots. About 14 deliverables in 2 waves; its size fits review and integration capacity. The standalone-App definitions become the next undertaking and consume these results. |
| B — spine + standalone App | A plus DEL-01-02, 01-03, 01-04, 01-05, 02-02, 02-04 | Brings the V4-REP-01 core loop's design forward, but needs a third wave. Native/workspace work would be defined before the pin and the OI-008/OI-009 answers exist. |
| C — narrow | DEL-04-01, 03-01, 03-02, 04-03 only | Quickest to close, but leaves the loop/panel, workflow and adapter joins undefined, and the relay questions weaker. |

## D2 — OI-001 always-reserved human acts (PRD OQ-02; V4-HI-30)

Point of need: before operation-policy production contracts (DEL-04-01 is a
supplier of about 20 consumers). The settled distinctions S1–S12 in the basis
already cover what is *not* reserved: an agent's success, queue position, receipt
or preparation never counts as an act.

- **Recommended:** for the first increment, reserve to the person: (a) marking
  work checked; (b) accepting a proposal wherever the active autonomy requires
  a proposal; (c) engineering approval; (d) relying on a result for a
  professional purpose; (e) changing the autonomy grant or enabling external
  agent access. No autonomy grant can widen past a reserved act or a declared
  checkpoint. The host names and enforces its own list (V4-HI-30). The
  original-seed "at least" list becomes this ruling for App/shared contracts.
  Operation-specific additions are made when a concrete SWB operation is
  selected (OI-021).
- Alternative: reserve only professional reliance now (current HI-30 wording)
  and decide the others per operation. This keeps flexibility, but about 20
  consumers carry `UNRESOLVED` labels longer.
- Alternative: keep OI-001 open through this undertaking. The definitions stay
  `UNRESOLVED`, and DEL-04-01 cannot finalize its policy representation.

## D3 — OI-002 classifier-based routine permissions (V4-AUT-04)

- **Recommended:** in the App, routine tool-permission and sandbox modes
  (including any classifier-based mode) remain the user's own Codex setting
  per project/turn, consistent with Root D-GOV-43. They govern tool execution
  only and never stand in for a reserved or professional act. In hosts, no
  classifier permission mode in the first increment: the SWB default proposal
  mode applies (V4-HI-41).
- Alternative: allow a classifier mode in hosts for read/examine operations
  only. This needs a classifier design and host enforcement evidence, which
  the first increment doesn't have.
- Alternative: keep it open.

## D4 — OI-012 Codex version pin (App implementation owner; owner visibility requested)

Local observation, 2026-09-28: npm `@openai/codex` latest = **0.158.0**
(modified 2026-09-28T05:16Z). Local install is 0.130.0 with a missing vendor
binary (not usable). 0.154.0 and 0.157.1 are dated evidence only.

- **Recommended:** select 0.158.0 as the definition/generation pin for this
  undertaking, then run spike W11. W11 installs it in a scratch directory
  (npm download, about 100 MB order), generates the protocol TypeScript/JSON
  Schema, and records observed fields against DEL-01-01's boundary. Later
  upgrades are deliberate and go through the recorded-exchange regression
  method. The pin is re-examined before implementation starts.
- Alternative: defer the pin until implementation starts. This keeps DEL-01-01
  version-independent now, but leaves the protocol facts behind native/recovery
  designs unobserved.

## Not requested now (routed elsewhere)

- MCP vs CLI seam, wire representation, proposal identity/idempotency: agreed
  between App integration owners and the SWBPIPE owner (DEL-03-03 TBD-007,
  DEL-03-01 TBD-003). They go into the W9 relay questions. Draft Piping PR #885
  (private live-control JSON CLI) is observed context, not a commitment.
- OI-008 Rust/TS division: the App implementation owner's proposal comes from W6.
- OI-003 extension promise, OI-021 first operation, OI-013/014 placement: stay
  at their points of need; they carry `UNRESOLVED` in the drafts.
