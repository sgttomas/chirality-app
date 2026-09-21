# D-GOV-35 — Delegated-Harness-Native Delegation Class

Status: RULED — APPLIED 2026-08-22; EFFECTIVE 8deca1489…
HumanRuling: `[click] "Approve as proposed"` — all eight proposed ruling items are ruled as written; complete recorded form transcribed below
Date: 2026-08-22
FramedBy: HELP_HUMAN managed run `ROOT_V3_PHASE0B_2026-08-22`, N1
AcceptedBasis: `main@abf3c1bf5996cd9333ad706df14e62df32fbbf0f`
RecordConvention: owner ruling recorded before publication; candidate, publication, and effective SHAs remain `TBD` until their respective Git acts
DecisionKey: `delegated_harness_native_class`
Supersedes: D-GOV-14 item 7 (exclusivity sentence only)
CandidateSHA: 294e846bc762b96ac780d49f0137f61eb4dde779
PublicationSHA: ade6ecf33d4e10dab1441aeedb240061e140ff1b
EffectiveSHA: 8deca1489a3e5921288f71d4960d555e183a6f3f

## Recorded ruling

The owner ruled R1-A in-session on 2026-08-22:

<!-- BEGIN R1-A OWNER RULING VERBATIM -->
R1-A — D-GOV-35 (delegated-harness-native delegation class): [click]
  "Approve as proposed".
  Subject bytes: `docs/governance_harness/_PROPOSALS/D-GOV-35_2026-08-22_delegated_harness_native_class/D-GOV-35.proposed.md`
  SHA-256 `924c1b098f1510bca9189e1ac06e4c2fd8e9d358a9fc3c4e42fdd04a53b69c88`;
  exact delta `AGENTS.proposed.patch` SHA-256
  `4455adda4199be5493e1f8d2171ebb4641f40666c35cf09e90adc935ff6355ee`
  against `AGENTS.md` SHA-256
  `268becd0bac9da8421b30089e4e4167a5e5f79bf3892d0f72ad41a63180a3aeb`.
  Recorded form: all eight proposed ruling items are ruled as written. D-GOV-14
  item 7 is superseded only in its sentence "managed child sessions are the
  sole executable app-harness delegation path"; the record-less SDK `Agent`
  bridge remains retired. Item 7 of D-GOV-35 resolves TM-ROOT-126 by
  prospectively superseding `docs/WORKFLOW_COMPONENT_STANDARD.md` §4.1
  ("Agent 0 delegates only to named Agent 1 roles."), `docs/TYPES.md` §4.3
  ("Agent 0 supervises only named Agent 1 managers."), and
  `docs/DBM_Agent_Instruction_Architecture.md` §2 ("Agent 0 delegates only to
  named Agent 1 roles. Agent 1 delegates to Agent 2.") with the ruled
  hierarchy: Agent 0 dispatches named Agent 1 managers and may directly
  dispatch bounded Agent 2 instances under the same sealed-brief,
  declared-scope, and durable-evidence requirements. The ruling is recorded
  per the D-GOV-34 convention (owner ruling recorded before publication;
  CandidateSHA / PublicationSHA / EffectiveSHA backfilled by their Git acts).
<!-- END R1-A OWNER RULING VERBATIM -->

Source:
`plans/steers/chirality_app_v3_root_ruling_record_r1_2026-08-22.md`, SHA-256
`a9879a87faaeb4cd4d5f16b2b4b0364543dff117e1b51c7e17d1efdcb20f377d`.

## Decision

The following eight items are ruled as written in the proposal:

1. **Two executable delegation classes.** Chirality recognizes
   `Chirality-managed` and `delegated-harness-native` delegation.
   `Chirality-managed` children continue to use `delegate_agent`, actual
   governed child sessions, sealed briefs, explicit child identity and role,
   declared context/tools/writes, and reconstructible run evidence.
   `delegated-harness-native` descendants use Codex App Server's native
   delegation inside the hard outer envelope and are not represented as
   Chirality-managed children.
2. **Managed-path preservation.** Managed child sessions remain the sole
   Chirality-managed executable path. The retired record-less SDK `Agent`
   bridge remains disabled, fail-closed, and non-model-visible. D-GOV-14 item
   7 is superseded only to remove its broader claim that no second executable
   App-harness class may exist.
3. **Primary entry and native controls.** Untyped, Agent 0, and Agent 1 primary
   Codex sessions may invoke native delegation. Chirality adds no native child
   allowlist, fan-out cap, model allocation, or scheduler; upstream/account
   limits apply. These absences do not relax the hard outer filesystem,
   network, process, canonical-root, account-identity, or policy envelope.
4. **No descent-to-role inference.** A native descendant is not automatically
   Agent 2. Native descent alone supplies no Agent 0/1/2 role, no TASK
   construction form, and no governed evidence classification.
5. **Codex role-entry parity.** Agent 0, Agent 1, and Agent 2 role entry is
   always offered for Codex sessions. When `G-ROLE` cannot mechanically prove
   non-delegation, explicit Agent 2/TASK mode remains offered and is labelled
   exactly `role not mechanically enforced`. Governed-workflow evidence from
   that mode is marked `instruction-asserted`.
6. **Calibrated K-SUBAGENT claim.** For the delegated-harness-native class,
   K-SUBAGENT non-delegation is instruction+config asserted, not
   mechanism-proven. This evidence qualification must remain visible wherever
   K-SUBAGENT-1, K-SUBAGENT-2, or K-SUBAGENT-3 conformance is claimed. It does
   not weaken hard filesystem, network, or process containment, and it may not
   be rewritten as proof that a native descendant could not delegate.
7. **Root hierarchy concordance.** Agent 0 may dispatch named Agent 1 managers
   and may directly dispatch bounded Agent 2 instances under root `AGENTS.md`.
   This prospectively supersedes the contrary sentence in
   `docs/WORKFLOW_COMPONENT_STANDARD.md` section 4.1, "Agent 0 delegates only
   to named Agent 1 roles." The allowed direct bounded Agent 2 path remains
   subject to the same sealed-brief, declared-scope, and durable-evidence
   requirements as Agent 1 dispatch. This resolves the normative
   prose-concordance decision underlying TM-ROOT-126; the application tranche
   must propagate the ruled meaning to the standard and reconcile the same
   stale sentence in `docs/TYPES.md` section 4.3 and
   `docs/DBM_Agent_Instruction_Architecture.md` section 2 before treating the
   documentary propagation as closed.
8. **Evidence is not authority.** Native session records, labels, role digests,
   instruction assertions, configuration assertions, and validation results
   are evidence only. They do not create an owner ruling, lifecycle approval,
   issuance, release, or reliance authority.

## Concordance disposition

This same N1 application tranche disposes the item 7 concordance obligation by
applying the ruled hierarchy wording to the three named current surfaces:
`docs/WORKFLOW_COMPONENT_STANDARD.md` section 4.1, `docs/TYPES.md` section 4.3,
and `docs/DBM_Agent_Instruction_Architecture.md` section 2. Those application
edits do not rewrite historical decision records or immutable evidence.

## Bound application and scope limits

The bounded DEL-02-03 M2 application tranche applies the exact reviewed Root
instruction delta, finalizes its live instruction-tranche manifest, routes the
App and Piping coordination notices, and records the Root-owned Chirality App
public-export regeneration as deferred to the next export release. Receiving
notices are coordination, not authority; each loop owns its follow-on.

This ruling and application do not lift any hold, including the ten
`HELD_UNAVAILABLE` bindings; do not change a pin, pointer, lifecycle state,
release status, or reliance authority; and do not authorize App implementation.
The record-less SDK `Agent` bridge remains retired.

## Publication posture

The owner ruling is recorded before publication following the D-GOV-34
convention. `CandidateSHA`, `PublicationSHA`, and `EffectiveSHA` remain `TBD`
until their respective Git acts and are backfilled only by a later routine act.
