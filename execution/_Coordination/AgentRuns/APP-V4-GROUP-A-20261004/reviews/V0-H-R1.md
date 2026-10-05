# V0-H-R1 — independent CC-H repair backcheck

Date: 2026-10-04. Reviewer: `/root/group_a_execution/hosting_contract_review`, same independent TASK reviewer under `/root/group_a_execution`; delegated-harness-native, no descendants. Root remains `/Users/ryan/.codex/worktrees/077c/chirality`. Own write: this file only; original V0-H remains unchanged.

## Disposition

**Ready for manager fan-in at definition-package scope.** No unresolved blocking, major or minor finding in this focused backcheck. H-M1/H-M2/H-M3 from [V0-H.md](V0-H.md) are repaired on the exact successor. This is not a supplier qualification, owner acceptance, product propagation completion, pin/default decision, stage gate or release.

Reviewed sealed `changes/CC-H.md` SHA-256 `b5b4544ae5c5f9983e87c8d044869e4af7906d03332f8821d4e77a7587f50ae9`; **28/28 candidate output hashes match**, checked both before source review and at report creation. No SUP1 0.160 source edits were included. Original V0-H standing is historical; this successor disposition supersedes its three open findings for the reviewed repaired definition only.

## Finding dispositions and evidence

| Finding | Disposition | Independent examination |
|---|---|---|
| H-M1 incompatible server-request schema identity | Repaired | Successor `$id` is `urn:chirality:del-01-01:hosting-boundary:v0.10:server-request-entry`, distinct from base v0.9. Valid integer fixture passes old schema and fails new; valid composite fixture passes new and fails old. CC-H R1 explicitly instructs outside registries to adopt v0.10. No implicit integer fallback introduced. |
| H-M2 fixed access session identity | Repaired | `App` creates a UUID session and permits explicit fixture injection; state export uses its owning session; `network_view` requires that session as a keyword argument. Two independent App instances export distinct sessions. Same injected session with account/api-key homes produces distinct full objects. An explicitly aligned hosting fixture, access state and network snapshot export equal generation objects. The fixture alignment is an offline model witness, not a claim that product integration executed. |
| H-M3 full-object answer crashes | Repaired | `answer` compares explicit input against the full current identity before internal integer lookup. Current full object accepts a valid outstanding answer; wrong session, home, counter and bare integer refuse; closed generation refuses. Independent two-Boundary scenario with reused `srv-o2` supplier id refuses the foreign session and leaves exported register/lifecycle records identical, then accepts the current object's answer. No TypeError and no session/home truncation. Omitted identity remains the explicitly instance-scoped internal operation, as documented. |

## Verification performed

- Re-read affected prototype implementations, their changed callers/tests, server schema identity, prototype README and CC-H R1 repair account; consulted original review and preserved authority assessment.
- Full access suite: **11/11**, **19 emitted records** validate, including distinct App sessions, thread-start model classification and user-choice/plugin behavior.
- Focused hosting rerun: **CC-H-answer-identity, CC-H, CC-H-mismatch, SCHEMA-records, SCHEMA-fixtures and VC-27 all passed**; **20 emitted records** validate and lifecycle/register tables remain **24/13**.
- Independent negative/round-trip checks described in the table passed with existing Python standard-library prototypes. Historical old schema loaded read-only using `git show e916ad1789:<path>`; no Git mutation.
- `git diff --check` for both Design fences passed.
- No unrelated full-suite repetition was needed: original V0-H records the full hosting run and separately asserted unchanged local socket fixture pass. R1 changes affect identity exports/answer/schema resource identity; focused checks cover those changes. No new socket/network/supplier execution was performed for R1.

## Remaining consumer obligations

The definition preserves full `{appSession, home, spawnCounter}` identity across all three hosting schema shapes and access-state/network shapes. Internal counters remain scoped caches only. Product/receiving consumers must adopt exact identities and schema resources, including server v0.10, lifecycle/client v0.9 and access state/network v0.3; historical readers must retain explicit old-version handling rather than reinterpret old integer records as new ones.

CC-A owns its NIR generation consumer; that moving candidate was not reviewed. DEL-01-02 recovery, DEL-01-04 interaction/display, DEL-04-03 ingestion and DEL-03-03 destination receiving plus located downstream GUIDE/packaging/qualification consumers remain manager/owning-loop propagation. These are required adoption work, not unresolved defects in the repaired definition. Reconcile GUIDE source hashes last and carry GC-8 notices through affected work graphs.

CI-7/8 definition assessment from V0-H remains supported: LT-04 requires full normal verification; LT-24 retains explicit unverified-development standing without permitting mismatch, and handshake remains required. Thread-start contact is disclosed as model traffic before a turn with actual/expected source and sampling limits distinct. User provider/model/plugin/approval/sandbox choice, no new veto/default and outstanding supplier qualification obligations are preserved. The product's hash-only verification, all exported identity consumers and provider-dependent expected-network display still require actual propagation/tests. Supplier version advance has its own basis and rechecks.

## Identity and reading evidence

Role/Root/loop/manual/skill/authority origins remain those recorded in V0-H; no extra role, workflow, delegation or instruction amendment. Only the new repair sources were added to that retained reading scope. Exact repaired output fingerprints are the 28-output table in the sealed CC-H above. The following hashes bind this return's immediate records:

- Original `reviews/V0-H.md` — `74da13495b22c6edfbfec862ac8340b58f14389ec702dddd16d45eab8c500195`
- Repair `changes/CC-H.md` — `b5b4544ae5c5f9983e87c8d044869e4af7906d03332f8821d4e77a7587f50ae9`
