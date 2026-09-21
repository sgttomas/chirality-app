# D-GOV-43 Proposal Packet — Codex Host Re-platform

Status: `RULED 2026-09-11` — the owner accepted revision 3 (text frozen at
commit `3ef2ef524956498f8923323dc6cf9d672dbeb50b`) with the post-build
clarification; the ruling record is
`docs/governance_harness/_DECISIONS/D-GOV-43_codex_host_replatform.md`.
The files in this packet are the proposal history and are not edited further.

Date: `2026-09-11`

Prepared by: `HELP_HUMAN`, Chirality v3 Codex-only MVP trial session

Accepted preparation basis: `main@a75adecf13f055c092ffa92809f66e7817c44242`

This is a candidate governed record. It does not amend `AGENTS.md`, the
ratified standards, Runtime or App governance, product source, packaging,
installations, trial evidence, or any downstream loop. Nothing becomes active
through this packet's authorship, validation, commit, push, or review. Only an
owner ruling can adopt the decision; the coordinated application tranche it
authorizes performs the propagation.

## Packet inventory

- `D-GOV-43.proposed.md` — the decision: findings, fourteen ruling items,
  the three folded choices with alternatives, surfaces touched, gates.
- `AGENTS.proposed.patch` — the exact inactive delta to `AGENTS.md`, verified
  with `git apply --check`.
- `IMPACT.md` — affected Root, Runtime, App and PEC surfaces, the purpose
  test by family, preservation of trial chats and executed records, notices.
- `REVIEW_FEEDBACK_R1.md`, `REVIEW_FEEDBACK_R2.md`, `REVIEW_FEEDBACK_R3.md`
  — the three rounds of independent review, verbatim, with each point's
  disposition. Round 3 endorsed revision 3 and added one clarification that
  accompanies the ruling rather than a further revision.
- `RULING_CANDIDATE.md` — the prepared `_DECISIONS` record, since
  transcribed with the owner's verbatim ruling into
  `_DECISIONS/D-GOV-43_codex_host_replatform.md` (historical).
- `docs/governance_harness/tranche_manifests/ROOT-DGOV43-PROPOSAL-20260911.yaml`
  — the proposal-candidate tranche manifest.

Packet integrity is the branch's Git history. No hash table or self-hash is
maintained.

## Owner direction of record

The owner's verbatim direction to prepare and iterate this packet is
transcribed in
`plans/steers/chirality_app_v3_codex_host_replatform_direction_2026-09-11.md`
and quoted in `D-GOV-43.proposed.md`.

## Validation posture

- The inactive patch applies cleanly with the literal command
  `git apply --check`.
- The tranche manifest validates in candidate-range mode; the agent-
  instruction and instruction-entrypoint validators pass.
- The candidate whitespace guard still runs in CI at this basis and passes;
  ruling item 11 proposes retiring it as a gate. The patch keeps its hunks
  anchored on non-blank lines only so the packet passes CI meanwhile.

Structural validation is evidence only. It is not semantic acceptance or an
owner ruling.

## Implementation handoff

The durable handoff for a separate implementing session is
`projects/chirality-app-dev/execution/_Coordination/AgentRuns/APP_V3_CODEX_HOST_REPLATFORM_20260912/HANDOFF.md`.
It requires the ruling record to exist before work starts.

## What the owner is asked to rule on

Fourteen ruling items in `D-GOV-43.proposed.md`: stock pinned App Server
owned by the App host with ordinary software integrity retained; faithful
transport with every server request answered; a Chirality effective Codex
home with separated authentication as the only MVP mode; user-chosen policy;
continuity from Codex with inexpensive preservation of daemon-era chats;
Codex-native authentication; daemon retirement; role and workflow
instructions through supported additive mechanisms; evidence from the full
stream with executed records preserved unchanged; roles, skills, workflows
and Plan Mode; governance simplification under a bounded coordinated
authority with a purpose test by family; the eight-check acceptance set on
the production path; local models deferred and residency requirements
retired; exclusions. The three revision-2 choices are folded into the ruling
with their alternatives noted; the owner may strike any of them.
