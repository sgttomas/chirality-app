# D-GOV-18 — Agent-index re-disposition (ORCHESTRATOR, EVALUATION, CHANGE, control-loop functions)

Status:       RULED
HumanRuling:  "I APPROVE D-GOV-18 items 1–8 at commit 9a900b3b76dda415cc4d41185350eb2e5a436302" (owner, 2026-07-21)
Ruling SHA:   9a900b3b76dda415cc4d41185350eb2e5a436302
Date:         2026-07-21
FramedBy:     D-GOV-11 runtime role ownership and Agent-2 construction forms; owner in-session direction, 2026-07-21; run `AGENT-INDEX-REDISPOSITION-20260721`
AcceptedBasis: `main@0c066652cd527eb1559f715e914262d2bda42602`

## Status note

This record is RULED. The eight items below were proposed at commit
`9a900b3b76dda415cc4d41185350eb2e5a436302` and approved by the owner's
verbatim ruling on 2026-07-21. The ruling itself modifies no live role,
retires no machinery, and executes no lifecycle act; implementation applies
only the ruled items' enumerated edits through the Item 8 PR sequence, each
merge separately human-approved.

## Decision to make

Eight separable matters re-disposing four agent-index roles and the two
control-loop artifact functions, superseding the D-GOV-11 disposition-matrix
rows for ORCHESTRATOR and EVALUATION. Each item is ruled independently on
ruling; unselected items produce no change.

## Item 1 — ORCHESTRATOR → PROJECT_SETUP (RENAME / NARROW)

Rename ORCHESTRATOR to PROJECT_SETUP (`agents/AGENT_ORCHESTRATOR.md` →
`agents/AGENT_PROJECT_SETUP.md`) and narrow the charter to one-time workspace
initialization, setup pipelines, and estimation. Function 4 (estimation)
stays. This supersedes the D-GOV-11 matrix row
"ORCHESTRATOR | RETAIN / EXPAND". The rename is atomic (Item 8, PR-3) and
carries every caller, delegation-edge, and validator key with it.

## Item 2 — EVALUATION as thin Agent 1 shell + `evaluation-protocol` skill (SLIM-TO-SHELL)

Full skill-demotion of EVALUATION is structurally infeasible: TASK cannot fan
out to multiple children; a skill carries no write authority; Agent 0 cannot
parent an Agent 2. EVALUATION is therefore realized as a thin Agent 1 shell
plus a new `evaluation-protocol` skill holding the method. The shell retains
the EVALUATION name, its subagents allowlist (TASK plus the eight
`AUDIT_*`/`EVALUATION_*` specialists), the `_Evaluation/` quarantine, and
fan-in validation. This supersedes the D-GOV-11 matrix row
"EVALUATION | EXPAND". The skill holds no write authority; the shell remains
the only surface that dispatches and validates.

## Item 3 — Control-loop functions split

Function 5 (control-loop artifact creation: `NEXT_INSTANCE_PROMPT.md`,
`NEXT_INSTANCE_STATE.md`) moves to HELPS_HUMANS. Function 3 (scan and report)
stays in PROJECT_SETUP. No other ORCHESTRATOR/PROJECT_SETUP function moves.

## Item 4 — CHANGE (RETAIN / SLIM, implemented now)

Slim `agents/AGENT_CHANGE.md` to authority semantics: routine-closeout
conditions, the `APPROVE:` / `APPROVE_DESTRUCTIVE:` gates,
no-silent-integration, branches-are-candidate-work, and coordination
handoffs. Method mechanics are left to agent judgment. A `change-method` skill
is recorded as a future Reuse Candidate under CHANGE's own routing protocol —
not created now. This is the concrete first slim tranche of the D-GOV-11
"REVIEW, CHANGE, RESEARCH | RETAIN / SLIM" row.

## Item 5 — REVIEW and SCOPE_CHANGE ruled SAFE

REVIEW and SCOPE_CHANGE are authority-gate roles and are ruled SAFE; each is
flagged future-slim only, with no change in this run. REVIEW's
`_Evaluation/Reviews/` default is confirmed canonical. The alternate
`_Reconciliation/Reviews/` piping is immutable pre-convention legacy; an
optional one-line historical note in `agents/AGENT_REVIEW.md` is permitted in
a later tranche, not required here.

## Item 6 — App Dev couplings deferred to the App Dev loop

The App Dev couplings — the frontend persona-resolution mapping
`ORCHESTRATE → 'ORCHESTRATOR'`
(`projects/chirality-app-dev/frontend/src/lib/shell/persona-resolution.ts:36`)
and its Jest expectation
(`projects/chirality-app-dev/frontend/src/__tests__/lib/persona-resolution.test.ts:24`),
plus App Dev `AGENTS.md` wording — are deferred by owner consent to the App
Dev project loop via an explicit handoff notice. Verified: these surfaces are
project-fenced and cause no root-PR CI breakage under the Item 8 sequence
(the root rename does not touch app-dev sources, and app-dev tests run under
the app-dev loop).

## Item 7 — Scope not granted

- No lifecycle acts.
- No specialist (`AUDIT_*` / `EVALUATION_*`) removal or downward migration.
- No root compatibility-machinery retirement.
- No rewriting of historical evidence: `execution/` run records, decision
  records, thesis, `domains/` artifacts, and `projects/` provenance are
  immutable.
- AUDIT_DECOMP undeclared-caller hygiene (REVIEW / SCOPE_CHANGE frontmatter)
  is recorded as a separate follow-on candidate, not part of this run.
- `tools/decomp/propose_gate4_kty.py` old-name seeds are recorded as a
  follow-on, not part of this run.

## Item 8 — Execution shape (five sequential PRs)

- **PR-0** — this ruling record and run scaffold (no role change).
- **PR-1** — CHANGE slim (Item 4).
- **PR-2** — EVALUATION shell + `evaluation-protocol` skill (Item 2), gated
  on closure of the App Dev in-flight EVALUATION fan-in.
- **PR-3** — atomic ORCHESTRATOR → PROJECT_SETUP rename (Item 1), including
  the `REQUIRED_DELEGATION_EDGES` key rename in
  `tools/validation/validate_agent_instructions.py:61` and an
  `OWNER_WORKFLOWS` legacy-accepting shim in
  `tools/validation/validate_scc_resolution_case.py:85` (accepts both the old
  and new names across the transition).
- **PR-4** — Function 5 move to HELPS_HUMANS (Item 3).

Subagent dispatch policy for every PR: Opus model, high reasoning effort,
sealed briefs, disjoint write scopes, one integration owner per stage. CHANGE
is the sole Git closeout. The human approves every merge.

## Caveats to adopt with any ruling

- No item has operative effect before its ruling; implementation applies only
  the ruled items' enumerated edits.
- A machine PASS from any validator referenced here is structural evidence
  only, never approval (D-GOV-02; D-GOV-17 M2 floor). Where ruled rename text
  trips a validator, the validator is corrected under review, never the ruled
  text.
- The App Dev follow-up (Item 6) is offer-only through the App Dev project's
  own instruments; this ruling writes no app-dev surface.

## Recorded ruling

The owner ruled in-session on 2026-07-21, binding to the proposal commit:

<!-- BEGIN OWNER RULING VERBATIM -->
I APPROVE D-GOV-18 items 1–8 at commit 9a900b3b76dda415cc4d41185350eb2e5a436302
<!-- END OWNER RULING VERBATIM -->

- Ruling SHA: `9a900b3b76dda415cc4d41185350eb2e5a436302` (the PROPOSED-state
  publication commit on branch `codex/agent-index-pr0-dgov18`, basis
  `main@0c066652cd527eb1559f715e914262d2bda42602`)
- Recorded by: HELP_HUMAN, run `AGENT-INDEX-REDISPOSITION-20260721`

## Supersession (effective)

This record supersedes the D-GOV-11 agent-disposition-matrix rows
"ORCHESTRATOR | RETAIN / EXPAND" (→ PROJECT_SETUP, RENAME / NARROW) and
"EVALUATION | EXPAND" (→ SLIM-TO-SHELL plus `evaluation-protocol` skill), and
records the concrete first CHANGE slim tranche of the
"REVIEW, CHANGE, RESEARCH | RETAIN / SLIM" row. D-GOV-11 otherwise remains in
force. No other D-GOV record is amended.
