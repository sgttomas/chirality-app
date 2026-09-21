# D-GOV-35 — Delegated-Harness-Native Delegation Class

Status: `PROPOSED — AWAITING OWNER RULING`

Decision ID: `D-GOV-35`

Date: `2026-08-22`

Framed by: Root managed run `ROOT_V3_PHASE0_2026-08-22`, N1

Accepted preparation basis: `main@6b0c5219b6a2653e2fc491b1d998abcf78fcf776`

Supersedes if ruled: only D-GOV-14 item 7's exclusivity statement that
"managed child sessions are the sole executable app-harness delegation path",
as bounded below. D-GOV-14's other items and the retirement of the record-less
SDK `Agent` bridge are not disturbed.

## Decision requested

Approve or reject a second executable App-harness delegation class named
**delegated-harness-native**: descendants created through Codex App Server's
native delegation facility while the primary and every descendant remain
inside Chirality's hard outer filesystem, network, process, root/account, and
policy envelope.

Approval would preserve managed child sessions as the sole
**Chirality-managed** delegation path. The new class is not a compatibility
fallback to the retired record-less SDK `Agent` bridge, does not make Codex
native descendants Chirality-managed children, and does not represent native
delegation evidence as mechanically equivalent to managed-child evidence.

## Owner direction already recorded at G0

The owner ruled G0 A1 `Required, no Chirality cap`: untyped, Agent 0, and Agent
1 primary Codex sessions may use native delegation; Chirality imposes no child
allowlist, fan-out cap, model allocation, or scheduling policy on that native
facility, while upstream and account limits remain applicable.

The owner ruled G0 A2 `Not automatically Agent 2`: native descent alone does
not assign an Agent 2 role, construction form, authority, or evidence status.
A native descendant may remain untyped or may enter a role only through an
explicit role entry under the applicable session and workflow contract.

G0 A3 records the parity requirement and contains this verbatim owner text:

<!-- BEGIN G0 A3 OWNER TEXT VERBATIM -->
I understand the predicament, but I can also enforce within my local config file what the max number of agents can be in Codex. I understand I'm losing some control and potentially contradicting claims the project makes about itself, but that's a price I can pay because Codex is both very reliable and the external config is something reasonable to ask of a user (at this point in the product's development). But it's very important that I be able to perform the full Agent 0/1/2 functionality through the Codex App Session so that it can be close to parity with native Chirality agents. So my choice would be something like outcome 2.
<!-- END G0 A3 OWNER TEXT VERBATIM -->

Source:
`plans/steers/chirality_app_v3_g0_record_2026-08-22.md`, SHA-256
`86b9877c6bea08a9f79c2af2378d5d38722a09c1a10deb37f87211c76d2c290b`.

## Proposed ruling

If the owner approves this decision, the following becomes the ruled design:

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

## Surfaces touched by the proposed ruling

The ruling would touch these authority, contract, implementation, and
derivative surfaces; naming a surface does not authorize its mutation:

- `docs/governance_harness/_DECISIONS/D-GOV-14_pr188_review_closure.md`, item 7;
- root `AGENTS.md`, `## Delegation and Entry Rules`, through the inactive
  `AGENTS.proposed.patch` in this packet;
- ratified `docs/WORKFLOW_COMPONENT_STANDARD.md`, section 4.1, plus the
  concordance follow-ons in `docs/TYPES.md` section 4.3 and
  `docs/DBM_Agent_Instruction_Architecture.md` section 2 (TM-ROOT-126);
- App `docs/CONTRACT.md` K-SUBAGENT-1, K-SUBAGENT-2, and K-SUBAGENT-3;
- the D-APP-68 transcription at
  `projects/chirality-app-dev/execution/_Coordination/_DECISIONS/D-APP-68_PACKET_CONCORDANCE_RULINGS_2026-07-19.md`, especially disposition 4;
- DEL-08-04's SOW at
  `projects/chirality-app-dev/execution/PKG-08_Agent_Suite_Pipeline_Dispatch_and_Subagent_Governance/1_Working/DEL-08-04_Type_2_Subagent_Governance_Bridge/ScopeOfWork.md`;
- `projects/chirality-app-dev/frontend/src/lib/harness/subagent-governance.ts:205-213`,
  exact file SHA-256
  `2b2d750be8fb3974593599631f64f920bc3b3fd4512640545bf1a22e61ec215c`;
  and
- App and Piping authority-reference, packaged-instruction, contract-mirror,
  and immutable run-basis evidence enumerated in `IMPACT.md`.

Lines 205-213 currently deny untyped/generalist delegation requests that reach
the existing governance gate. App WP-06 must determine and implement the
required native-class integration under the App loop's own authority; no code
change is made or authorized by this Root Phase-0 proposal packet.

## Application, compatibility, and closure gates

Approval of this proposal would authorize only the ruled design. Application
still requires a bounded instruction tranche and the receiving App loop's own
SCA/deliverable work. At minimum:

1. apply the exact reviewed Root instruction delta through the D-GOV-35
   application tranche;
2. propagate the ruled normative concordance without silently rewriting
   historical D-GOV, D-APP, receipt, run-basis, or packaged-proof evidence;
3. route coordination notices to App and Piping; each loop independently
   adopts, amends, declines, or defers its follow-on;
4. execute App WP-06 for the App contract, SOW, runtime implementation, and
   tests under App authority;
5. preserve the `instruction-asserted` evidence label whenever `G-ROLE` does
   not mechanically prove non-delegation; and
6. validate the changed live surfaces and record remaining blockers in the
   owning handoff state.

No current hold, including any `HELD_UNAVAILABLE` binding, is lifted by the
proposal or by an owner ruling alone. No lifecycle, pointer, pin, release,
publication, or merge act is contained in this record.

## Owner ruling

`TBD — AWAITING OWNER RULING`

Authorship, review, validation, Git state, or later citation must not replace
the required owner act.

RULED 2026-08-22 — see `_DECISIONS/D-GOV-35_delegated_harness_native_class.md`
