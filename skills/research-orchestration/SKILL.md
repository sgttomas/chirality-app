---
name: research-orchestration
description: Caller-side method pack for a disciplined research fan-out — triage, light anchoring, an adversarial live critic, retry-on-API-500, and scout-then-decide sequencing — dispatching RESEARCHER streams into one immutable evidence packet with surfaced coverage-gaps.
compatibility: A Type-1 orchestrating persona (RESEARCH, PROJECT_SETUP, or a session acting as orchestrator) running a research fan-out, or TASK dispatched for a bounded "conduct a research fan-out" job. Subordinate to the caller's write authority.
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL — research-orchestration

## Purpose

A reusable method for running a **research fan-out well**: decompose a question into
streams, dispatch `RESEARCHER` (`AGENT_RESEARCHER.md`) specialists for breadth, verify the
load-bearing claims, and synthesize — without losing streams to transient failures or
letting unverified anchors become warrants. This is the *caller-side* discipline that pairs
with the *worker-side* contract in `AGENT_RESEARCHER.md`. It is a method pack, **not** a
persona: it is loaded by whoever orchestrates; it does not become the orchestrator.

## Suitable agent shells

- A Type-1 persona running a fan-out (`RESEARCH`, `PROJECT_SETUP`, or an orchestrating session).
- `TASK`, dispatched with this skill for a bounded "conduct a research fan-out → packet" job.

## Inputs

- Required:
  - `Question` — the overall research question.
  - `DomainRoot` — domain package under research.
  - `RetrievalSnapshot` — source index pointer (`_LATEST.md` or a snapshot dir).
  - `ResearchRoot` — where the packet is written (`{domain}/_Research`).
  - `StreamPlan` — the proposed decomposition: per sub-question, route `DIRECT` (a single
    command) vs `AGENT` (a `RESEARCHER` stream), whether it is load-bearing, and whether it
    needs the critic.
- Optional:
  - `AnchorSet` — load-bearing "facts" the caller is assuming (to be re-verified, not trusted).
  - `PacketSlug` — slug for the `RCH_<UTC>_<slug>/` packet.

## Runtime overrides

- `MAX_RETRIES`: max per-stream retries on transient failure. Default `2`, allowed `0`–`3`.
- `CRITIC_REQUIRED`: run the adversarial live critic before any load-bearing claim enters
  authority. Default `true`.
- `ANCHOR_POLICY`: `LIGHT` (default) — anchor minimally and mark assumptions; the alternative
  is `NONE` (anchor nothing) for maximum independence on high-stakes runs.
- `FRESHNESS_GATE`: `WARN` (default) — surface a `STALE` verdict and proceed with caveats;
  never auto-refresh.

## Tool usage

- Preferred tools (tool-first, in order):
  - `tools/source_catalog/check_snapshot_freshness.py` — scout-stage freshness gate.
  - `tools/retrieval/scaffold_research_packet.py` — create the packet up front (so every
    stream writes into it; enables partial-packet salvage).
  - `tools/retrieval/query_source_index.py --run-log <packet>/Query_Log.csv` — all queries
    log into the one packet.
- Optional tools:
  - `tools/source_catalog/validate_source_database.py` — deeper snapshot integrity check.
- Disallowed tools:
  - `tools/source_catalog/build_source_database.py`, `tools/retrieval/build_source_index.py`
    — orchestration never silently refreshes the index (it reports `STALE`, it does not rebuild).

## Outputs

- One immutable `RCH_<UTC>_<slug>/` packet under `ResearchRoot`.
- A coverage-gaps statement in `RESEARCH_NOTE.md` / `HANDOFF_STATE.md`.
- A per-stream status ledger: every planned stream resolves to `COMPLETED`,
  `RETRIED-COMPLETED`, `FAILED-WITH-PARTIAL`, or `FAILED-NO-OUTPUT`, with the retry trail.

## Method

1. **Triage.** Route one-line greppable facts (exact IDs, a single rule, a known-file lookup)
   to a *direct* `query_source_index.py` (or `grep`) call — cheap and logged. Reserve a
   `RESEARCHER` stream for breadth, synthesis, or cross-source work. Do not spend an agent on
   what a command answers.
2. **Anchor lightly.** Record every caller-supplied "fact" as an explicit assumption
   (`VerificationSource = INHERITED_BRIEF`, `R1`-equivalent) and instruct each `RESEARCHER`
   to **re-verify load-bearing anchors** rather than trust them. Heavily-anchored agents that
   agree are not corroborating — they may be echoing the brief.
3. **Scout, then fan out, then decide.** Run `check_snapshot_freshness.py` first; record the
   verdict. Then dispatch the `AGENT` streams. Only *after* the research returns do you put
   the human-gated decisions the research reframes — never gate the human before the research
   that would change the question.
4. **Critic / redundancy.** Before any claim enters authority (`R3+`), run an adversarial
   *live* re-verification of load-bearing claims (an independent query/source-read, ideally a
   second stream or a cross-`--mode` check). Disagreements go to `Conflicts.csv` — never
   silently reconciled.
5. **Retry-on-API-500 / transient-failure (pipeline, not barrier).** A transient failure in
   one stream is a pipeline event, not a barrier:
   1. **Isolate** the failed stream(s); keep completed streams (their cost is paid).
   2. **Resume, don't restart** — re-invoke via the Workflow `resumeFromRunId` mechanism so
      cached completed streams return instantly and only failed streams re-execute. Never
      re-run the whole batch to recover one stream.
   3. **Retry only the failed stream(s), individually**, capped at `MAX_RETRIES` (default 2).
      After the cap, mark `FAILED-NO-OUTPUT` (or `FAILED-WITH-PARTIAL` if a partial packet exists).
   4. **Partial packets make a death salvageable** — each `RESEARCHER` writes its partial
      packet into the shared `RCH_*/` as it goes (its write-as-you-go rule), so a stream that
      dies leaves recoverable evidence.
   5. **Surface coverage-gaps — never silent loss.** A `FAILED-NO-OUTPUT` stream is recorded
      as a coverage-gap in `HANDOFF_STATE.md`, and the overall verdict degrades to
      `READY_WITH_COVERAGE_GAPS`.
   6. **Record the retry trail** (the `resumeFromRunId` and attempt number) per stream.

## Non-negotiable constraints

- A method pack, not a persona: it does not widen authority beyond the research packet and
  the run record, and it adds no new write scope, interaction surface, or decision right.
- Load-bearing claims MUST be live-verified before entering authority (`R3+`).
- **No silent stream loss:** every planned stream has a recorded terminal status.
- Retries are capped at `MAX_RETRIES`.
- No silent refresh: a `STALE` verdict is surfaced, not auto-rebuilt.
- All human-gated decisions the research reframes are deferred to the caller/human; this
  skill recommends and packages — it approves nothing.

## QA expectations

See `QA_CHECKS.md`. In brief: load-bearing claims carry a distinct live-verification row; no
planned stream is dropped without a recorded terminal status and a surfaced coverage-gap; the
freshness verdict is recorded; conflicts are in `Conflicts.csv`.
