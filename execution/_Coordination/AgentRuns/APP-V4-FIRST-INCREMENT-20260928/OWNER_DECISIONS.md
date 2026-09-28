# Owner decisions — APP-V4-FIRST-INCREMENT-20260928

Decision ID: `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`. Owner: Ryan. Recorder:
HELP_HUMAN (Claude Code session). Custody: the owner's answers to a structured
question in the active Claude Code chat, transcribed by the recorder on
2026-09-28. This is not a raw platform export and carries no platform timestamp.
The package presented was [DECISIONS_PENDING.md](DECISIONS_PENDING.md) as
committed in `8d3c66542`, together with the question texts below.

| Question presented | Owner's selected answer (exact label) |
|---|---|
| Which scope should this first 60% undertaking take? (Wave 1 is already running and is common to all options.) | "A: App/host spine (Recommended)" |
| OI-001: which human acts are always reserved to the person for the first increment? | "Five reserved acts (Recommended)" |
| OI-002: how should classifier-based routine permission modes be treated? | "App user setting; none in hosts (Recommended)" |
| OI-012: select a Codex App Server version pin now and run the protocol-generation spike? | "Pin 0.158.0 + spike (Recommended)" |

## Effects, stated at the scope decided

- **D1 scope.** This undertaking covers DEL-04-01, 04-02, 04-03, 03-01, 03-02,
  03-03, 03-04, 02-01, 02-03, 05-01, 05-02, 01-01 (boundary and pin), 09-06
  and 09-09. The standalone-App definitions (DEL-01-02…05, 02-02, 02-04) are
  left for a later undertaking; this one does not start them.
- **D2 OI-001 ruling (first increment, App/shared contracts).** The following
  are reserved to the person: (a) marking work checked; (b) accepting a
  proposal wherever the active autonomy requires a proposal; (c) engineering
  approval; (d) relying on a result for a professional purpose; (e) changing
  the autonomy grant or enabling external-agent access. No autonomy grant
  widens past a reserved act or a declared checkpoint. The host names and
  enforces its own list (V4-HI-30). Operation-specific additions are made when
  the concrete SWB operation is selected (OI-021). The ruling does not show
  that SWBPIPE has adopted this list or enforces it (DEP-001).
- **D3 OI-002 ruling.** In the App, routine tool-permission and sandbox modes
  (including any classifier-based mode) remain the user's own Codex setting
  per project/turn. They govern tool execution only and never stand in for a
  reserved or professional act. In hosts there is no classifier permission
  mode in the first increment; the SWB default proposal mode applies
  (V4-HI-41).
- **D4 OI-012.** Codex `0.158.0` (npm `@openai/codex` latest at 2026-09-28) is
  selected as the definition/generation pin for this undertaking. Spike W11 is
  authorized: a scratch-directory npm install of that version, generation of
  protocol TS/JSON Schema, and a record of observed facts. Upgrades are
  deliberate. The pin is re-examined before implementation starts. The
  selection does not establish qualification (DEP-005).

These rulings apply through the DEL-04-01 policy representation (OUT-002
"adopted decisions") and the affected v0.2 definitions. The `Open_Issues.csv`
rows and the frozen decomposition snapshot are not rewritten by this record;
the bounded closeout (C1) reconciles the pointers. Remaining open matters are
unchanged: OI-003, OI-008 (App implementation owner; proposal from W6), OI-009,
OI-013, OI-014, OI-018 and OI-021.

---

# Owner decisions (2) — `APP-V4-FIRST-INCREMENT-20260928-DECISION-2`

Owner: Ryan. Recorder: HELP_HUMAN. Custody: the owner's answers to a structured
question in the active Claude Code chat, transcribed on 2026-09-28. The
package presented was [DECISIONS_PENDING_2.md](DECISIONS_PENDING_2.md).

| Question presented | Owner's answer (exact text) |
|---|---|
| D5: When the App's Codex reads host model content through the external-agent channel, that content reaches the App conversation's model, which may be a cloud model. What boundary should apply? | "These are all open source projects and no worries about the code leaking.  I want to emphasize user flexibility here." |
| D6: Stock Codex dispatches tool calls itself, so the App has no guaranteed point to hold a run before a tool call at a workflow checkpoint. How should checkpoints be enforced in the first increment? | "Defer to SWBPIPE answer" |

## Effects (recorder's reading; the D5 answer was free text)

- **D5 — user flexibility.** Host content read through the external channel may
  flow to whatever model the person has selected for the App conversation,
  including a cloud model. The App imposes no local-only restriction and does
  not gate enablement on the model destination. For truthfulness, not as a
  gate, the App records each run's model destination and shows it in the
  channel status (DEL-03-03, DEL-04-03). A host may still restrict its own
  channel; that is host policy (DEP-001). V4-HOST-02 continues to govern the
  host's embedded agent. This reading follows option A without its "disclosed
  at enablement" gating element, because the owner emphasized flexibility.
- **D6 — deferred.** How the App holds its own runs at checkpoints stays
  `UNRESOLVED{D6}` until the SWBPIPE owner answers relay question SQ-02, which
  asks about constraint receipt and host-side holds. Meanwhile the drafts:
  - carry per-checkpoint *hold support*;
  - never claim an App hold they cannot enforce;
  - record "action during hold";
  - adopt neither interposed App code nor reliance on `turn/interrupt`.
