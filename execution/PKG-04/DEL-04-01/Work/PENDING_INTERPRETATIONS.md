# Pending act and policy decisions

Recommendations below are unadopted. The [packet basis and LOOP decisions](../../../PKG-05/DEL-05-01/Work/PENDING_INTERPRETATIONS.md)
and the coupled [A15 store decision](../../DEL-04-03/Work/PENDING_INTERPRETATIONS.md)
form one owner decision packet. Source:
[issue 168](https://github.com/sgttomas/chirality-app/issues/168).

## Recommendation and governing meaning

Recommend repairing ACT's incomplete summaries while retaining its existing
A15 attribution and A16 decision rules. This does not add a new reserved act,
grant agent authority or change the D2/D3 policy. The coupled store exception
needs the explicit owner interpretation set out in DEL-04-03, rather than
assuming that adding A15 to A9 decides where its evidence belongs.

[Scope](../ScopeOfWork.md) REQ-002 already names registration as a person's
act and supplies that meaning to DEL-02-02 and DEL-01-04. In
[ACT](ACT_AND_POLICY_CONTRACT.md), §2.1 A15, §2.4, §2.5 and §4.7 require a
human-act record bound to the reviewed revision and native capture evidence.
A9's subject list alone omits A15. The A16 row and §2.5 already state that a
later A16 on the same unchanged package supersedes the earlier decision;
changed package content instead lapses the old act and needs a new request.
LC-6 summarizes only A12/A13 and settings-version evidence.

## A9 / A15: exact candidate and companion

| Location | Before | Recommended candidate |
|---|---|---|
| §2.1 A9, Subject | “An actually performed act of kind A4–A7, A10–A13, A16 (pass 4, R23-18), or an act-declined event” | “An actually performed act of kind A4–A7, A10–A13, A15–A16, or an act-declined event” |
| §2.4, lapse-state element | “Relative to current content (V4-HI-32). superseded for A12/A13.” | “Relative to current content (V4-HI-32). Superseded for A12/A13, and for A16 under §2.5; A15 follows its revision rule there.” |

Keep A9's recorder/evidence requirements, §2.4's act-kind inventory and the
A15/A16 detailed rules. The historical attribution in the A9 row describes
its earlier edit; its removal from the revised subject phrase does not alter
the historical source or product basis.

Alternative: omit A15 from A9 intentionally. That would require a separate
recording rule reconciled with §2.4/§4.7, RS HA-10 and the native registration
path, with no attribution gap. No source-grounded reason for that exception
was found; current recording requirements already include A15.

## LC-6 / A16: exact candidate and companions

Replace the current LC-6 row:

> superseded by ⟨act⟩ | A later A12 (or A13) on overlapping classes and scope
> is established | A12, A13 | — (a checkpoint it performed stays performed)
> | derived from settings versions

with:

> superseded by ⟨act⟩ | A12: a later A12 on overlapping classes and scope is
> established. A13: a later A13 is established by the host's enablement
> facility. A16: a later A16 decides the same unchanged package (§2.1/§2.5).
> | A12, A13, A16 | — (a checkpoint it performed stays performed; prior
> actions remain attributed to the decision then in force) | A12/A13: the
> corresponding control/enablement evidence; A16: the human-act entries and
> their evidenced decision order/relations, never settings versions alone

In LC-3's Leaves to cell, replace “LC-6 (A12, A13)” with “LC-6 (A12, A13,
A16)”. Its A15-stays-current rule remains. The §2.4 lapse-state companion
above makes the same inventory explicit. Keep LC-8 corrections distinct:
correcting a mis-recorded A16 is not a new decision. Do not make A16 inherit
A12's control-confirmation prerequisite, let another act kind supersede it,
or use append order alone to manufacture decision order.

Alternative: prohibit A16 supersession. That changes the detailed A16 rule,
RS lapse/decision relations and the decision view, requiring an owner policy
change. The recommendation preserves the existing same-package rule instead.
A revised package remains a different request with visible lapse, not silent
carryover of an earlier decision.

## Readers, fixtures and source identities

[act_policy.rs](../../../../app/src-tauri/src/act_policy.rs) includes A15 and
A16 in `ActKind` and its human-only distinction; the policy-standing integration
fixtures exercise their separation from operation permissions. The real
[A15 path](../../../../app/src-tauri/src/act_control_a15.rs) binds reviewed
entries, the frozen offer and native event, then writes a library act/capture;
its synthetic-event fixtures cover mismatch/refusal and retry custody. These
are implementation scenarios, not evidence of a person's actual act. The
[invoking-window repair account](../../../PKG-01/DEL-01-04/Work/A15_ORIGINAL_WINDOW_CONFIRMATION.md)
and [J2 account](../../../PKG-09/DEL-09-02/Work/J2_PARTIAL_ACTUAL_20261108.md)
retain their original subjects and native limits.

[decision_view.rs](../../../../app/src-tauri/src/decision_view.rs) checks A16's
requested kind, chosen alternative, exact package content, subject/scope and
recorded relations; the decide-flow fixtures exercise file capture, lapse and
decision projection. They are appropriate consumers for the summary repair,
not authority to invent the rule. Any later amendment must compare same-package
successors, changed-package lapse, correction and uncertain decision order;
existing synthetic passes establish only their own cases.

Current ACT SHA-256 is
`788590495aa6351d14f41e234650129779cc7824013139e6ee17321c06be46b6`.
The historical policy-standing and A16 product bases retain ACT
`597f13bda1fe1c1fa97b9db8ebc92483c2b43ebcbdc784d91be1f57fa93df5f2`.
A new summary amendment requires reconciliation of actual live documentary
selectors/copies; it does not renew those historical whole-file bindings or
repair the separately recorded dynamic S-6 drift by repinning. AS citation
identity is addressed in the coupled record-store note. Scopes and YAML
conditions remain unchanged by these proposals; no broader AC is closed.

## Effect and next actor

P2's approved exact-475c J2 observation stays independent: one registration,
one fresh reuse turn, twenty minutes, stop-only/no retries, preserving the
current project and old-046 store. Observe capture/record placement and exact
reviewed-content linkage without claiming a personal human act; the linked
store note states which findings change the recommendation. A native
confirmation or a valid A15-shaped record does not identify the operator as a
person or establish any A4–A7.

P3's later applicable act/recovery evidence must distinguish an act record,
its capture and its recording outcome. P5 must retain the host's actual actor,
control and evidence; no App rule or fixture demonstrates host enforcement.

Next actor: App Agent 0 brings the summary repairs and coupled store choice
to the owner. The contract and implementation owners then carry any selected
amendment with its live consumer reconciliation. Acceptance, final integration
and publication recommendation remain with their existing owners.
