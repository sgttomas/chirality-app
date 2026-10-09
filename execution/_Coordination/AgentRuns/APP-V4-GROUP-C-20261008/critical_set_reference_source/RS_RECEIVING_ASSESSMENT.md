# DEL-04-03 receiving — C3 critical-set references

New bounded source-receiving assessment assigned by HELP_HUMAN to
WORKING_ITEMS /root/distribution_integration_manager, independently checked by
existing distinct TASK /root/distribution_integration_manager/production_workflows.
This is not historical RS owner concurrence, adopted schema, product acceptance
or implementation authorization. Review was read-only; no tests or launches.

Basis: carrier PR #1197 exact source head
`eeb086e674ec6b7617c7b5c629773f4c819867d9`, now merged at
`3e8e1afc71e55abf88bada6e4ac0f6a7dbcb3b7a`. RS §§3,6,9,14 and the closed
RS_RECORD.schema.json evidenceRef shape were inspected. All three exact source
hashes below match the merged basis.

## Recommended receiving boundary

Keep the carrier an external versioned C3 journal, with explicitly adopted
resolver/reference semantics informed by RS. No RS amendment is inherently
required. The present proposal is honest about missing contracts and does not
contradict RS, but is not an adopted executable carrier.

| Concern | Exact mapping or gap |
|---|---|
| Kind and identity | Preserve actual evidence kind: receipt, content identity, conversation item, supply record, etc. A carrier reference may use carriage manifest only after semantic receiving selection. Artifact-local keys are not RS record IDs/kinds. That kind alone confers no compatibility or authority. |
| Method and custody | Distinguish raw-byte identity, pinned parsed-Value serialization, original source custody, generation/root and receipt scope. Equal bytes do not replace custody. Exact ref syntax, bounded resolver and retained immutable closure remain C3/storage owning contracts. |
| Write resolution | Preserve the original RS literal resolved / unresolvable / not supplied exactly and its historical observation. Never recalculate it from a later read. |
| Read diagnostics | Keep carrier resolved / not_supplied / missing / changed / unreadable / conflicting / not_checked separate. First grammar should make no cross-format projection into RS coarse values. not_checked means no assessment, not unresolvable. |
| Independent states | Conflicting refs can each resolve; stale relations or source closure need not invalidate exact historical bytes. Slot state, attempt outcome, source liveness and byte resolution are distinct domains. |
| Recorder and order | External envelope must define format/version, journal/revision, recorder, recording context, writer-local order and current commit/read identities. Actor/responsibility is not recorder. Timestamps/UUIDs create no global order. |
| Human acts | Manager reconciliation, journal confirmation, successful operations and matching target bytes cannot mint human_act. RS §6 HA-1/HA-2/HA-7 and §14.1a require actual capture provenance, actor/recorder separation and cold-replay restraint. |

The RS closed evidenceRef requires kind, ref, resolutionAtWrite and permits
claimedIdentity and method. Its kind enum includes carriage manifest,
conversation item, supply record and limit account. Read resolution is derived
by the RS reader, not an extra stored field. Referenced RS evidence keeps its
own actual literal and meaning separately from carrier diagnostics. A future
RS reader integration needs explicit receiving/resolver adoption; this note
neither defines its derived values nor extends its schema.

## Smallest owning change and amendment threshold

Group C/storage should complete the external envelope, reference syntax/resolver,
bounded retention, closure and write/read contract. Existing RS emits, if any,
must remain valid existing entries with unchanged evidenceRef fields. External
snapshot replacement is not RS append/correction: it must not rewrite an RS
record or import new writer ordering. RS §14 validation-before-append, retained
partial/correction history, read limits and failure visibility remain unchanged.

New RS kinds, fields/enums, order, capture, durability or reader semantics require
a named RS amendment and joined consumer adoption. Otherwise an external journal
with unchanged RS references needs its own contract and explicit receiving
adoption, not an RS format revision merely because diagnostics are richer.
No owner-level semantic ruling is inherently needed for the external route.
Escalate if it is intended to confer acceptance, human-act standing or new reliance
authority; do not derive those meanings from persistence or a complete closure.

## Independent finding

production_workflows independently supports this external-journal recommendation
at the exact carrier head above. It checked the stated RS sections and schema,
confirmed that no total state mapping is warranted and identified the envelope,
resolver, custody and amendment gaps retained here. Finding: no present RS
contradiction, not yet an adopted executable carrier. This is a new attributed
receiving assessment, not self-concurrence or historical owner approval.

## Source identities — SHA-256

- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-C-20261008/critical_set_reference_source/CRITICAL_SET_REFERENCE_CARRIER_v0.1_PROPOSAL.md`: `49ba1d89b8ee3a6a33d7ad68fae95cbedec8ccd72bb942887be457025487b796`
- `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/RECORD_SEMANTICS.md`: `910e4473575d06ba1cd4799c6ad29a31f19015b3e1665dae65641af68c4f8fae`
- `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/RS_RECORD.schema.json`: `84200fd0ad045c11ce82ca5531ea461388304c46c1ea49d30263de5d6fa0f72a`
