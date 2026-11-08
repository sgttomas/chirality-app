# Pending record-store and citation decisions

Recommendations below are unadopted. The [packet basis, LOOP choices and P2/P3/P5 map](../../../PKG-05/DEL-05-01/Work/PENDING_INTERPRETATIONS.md)
and [ACT companions](../../DEL-04-01/Work/PENDING_INTERPRETATIONS.md) belong to
this same decision. Source:
[issue 168](https://github.com/sgttomas/chirality-app/issues/168).

## Recommendation: decide the A15 exception explicitly

Recommend preserving the selected project-store/library split and making its
**A15-only exception** explicit in the broad PRD and Scope clauses together.
This narrows the universal outside-working-tree/project-export location claim
for A15 evidence; it is an owner decision, not a factual correction justified
by current code. Do not qualify all decisions as “project decisions” and leave
unspecified non-project acts outside the promise. Keep every other act, accepted
record and project-run obligation, the actual-actor rule, content binding,
append-only record authority, tamper-evidence and recovery obligations.

[Scope](../ScopeOfWork.md) CLM-001, REQ-001 and AC-001 and
[PRD](../../../../docs/PRD.md) V4-REC-02 broadly place human decisions and
records in the App store, outside the agent-edited working tree and exportable
with their project. Scope AX-006 explicitly retains A15 library acts/captures
at separate library paths. [RS](RECORD_SEMANTICS.md) §13.7/§13.8 likewise
migrates project records to the store but keeps the library rows unchanged;
U-STORE-2 selects “Evidence; re-register” across installations. These are
competing extents within current governing text, not merely old code.

The library exception means an in-project library's A15 evidence can remain
inside the working tree. Project export does not by itself prove that the
separate library act and capture accompanied it. The contract must state those
limits and require resolvable library evidence; no package or move witness is
inferred from choosing this allocation.

## Exact coherent companion candidates

Retain the unaffected sentences of each clause. The replacements below apply
only after the owner selects this interpretation; no normative file is edited
by this packet.

| Location | Before | Recommended candidate |
|---|---|---|
| PRD V4-REC-02, location sentence | “The person's decisions, accepted records and run records are kept by the App in its own records store, outside the working tree an agent edits, as ordinary append-only files linked to their project by a stable project identity and exportable with it (R-STORE).” | “The person's decisions, accepted records and run records are kept by the App in its own records store, outside the working tree an agent edits, as ordinary append-only files linked to their project by a stable project identity and exportable with it (R-STORE), except A15 workflow-library registration acts. A15 acts remain ordinary append-only library logs with linked capture evidence travelling with the library; project runs cite the applicable library evidence. This exception changes location and carriage, not attribution, content binding, integrity or recovery requirements.” |
| Scope CLM-001, location sentence | “The person's decisions, accepted records and run records are ordinary append-only files in the App's records store, outside the working tree an agent edits and linked to their project by a stable project identity (AX-006).” | “The person's decisions, accepted records and run records are ordinary append-only files in the App's records store, outside the working tree an agent edits and linked to their project by a stable project identity, except A15 library registration acts, whose append-only log and linked capture evidence stay with the library (AX-006; RS §13.7/§13.8). Project-run references identify the applicable library evidence.” |
| Scope REQ-001, first sentence | Ends “without relying on version control (AX-006).” | Retain that requirement and append: “The location/carriage exception is A15 library registration: its append-only act log and linked capture evidence shall travel with the library, and a project run's references shall resolve the applicable library evidence (AX-006; RS §13.7/§13.8). The exception supplies no missing act, capture or integrity/recovery evidence.” |
| Scope AC-001, first sentence | Places “human decisions, accepted records and run records” in the App store “linked to their project” | Replace that location phrase with “human decisions, accepted records and run records as ordinary append-only files in the App's records store, linked to their project, except A15 library registration acts, whose append-only log and linked capture evidence remain with the library and resolve from citing project runs”. Retain the definition-file and non-authoritative-session/derived-view requirements and the session-only negative. |
| Scope SOW-092 local-contribution cell | “Workflow definitions as ordinary project/workspace or library files; human decisions, accepted records and run records as ordinary append-only files in the App's records store, linked to their project (AX-006)” | “Workflow definitions as ordinary project/workspace or library files; human decisions, accepted records and run records as ordinary append-only files in the App's records store, linked to their project, with the A15 library-act/capture location and carriage exception in AX-006” |
| Scope AX-006, second and final location sentences | “SOW-092, CLM-001, REQ-001 and AC-001 now place human decisions, accepted records and run records in that store; workflow definitions stay project/workspace or library files.” / “…while A15 library acts and their captures retain the separate library paths specified there.” | “SOW-092, CLM-001, REQ-001 and AC-001 place human decisions, accepted records and run records in that store, with the explicit A15 library-act/capture exception; workflow definitions stay project/workspace or library files.” / “The A15 exception retains the separate library paths of RS §13.7/§13.8, including an in-project library; those acts and captures travel with the library, and citing project runs must resolve their applicable evidence.” |

The SOW-092 **current Scope mapping** is the amendment target; the frozen
accepted ScopeLedger row and accepted snapshots retain their bytes/identity.
REQ-001's unaffected export, ordinary-file and non-Git promises still govern;
AC-002–007 are not reduced or declared met. VER-001 must inspect the two owning
locations and references, not test only the easier project path. RS §13.7/§13.8,
DEL-02-02 registration/reuse meaning and the ACT A9 inventory must agree with
this exception. Existing YAML incoming act/descriptor, record and host-evidence
conditions still apply; none is waived.

Alternative: keep V4-REC-02/REQ-001/AC-001's universal location promise and
move A15 act/capture authority into the App store. That requires revising
AX-006, RS's library rows/U-STORE-2 and DEL-02-02's library portability/receipt
readers; define export and cross-installation evidence/re-registration behavior,
then implement lossless identity-preserving migration and capture resolution
with targeted persistence regression and independent scrutiny. It changes the
475c witness subject if implemented there. Do not silently copy an act into a
second authority, relocate captures or make old registration current merely
because a store copy exists. The existing library-carriage decision is why the
explicit exception is recommended, not because the implementation already uses it.

## Actual readers and what J2 can distinguish

[storage.rs](../../../../app/src-tauri/src/storage.rs) `library_log`,
`library_capture_dir` and `capture_file_for` route A15 to
`<library>/.chirality/records/acts.jsonl` and `<library>/.chirality/captures/`;
other project captures use the project store. The
[A15 capture/writer](../../../../app/src-tauri/src/act_control_a15.rs) uses that
library log and binds the native event to its frozen reviewed entries.
[workflow_record_store.rs](../../../../app/src-tauri/src/workflow_record_store.rs)
places reuse selection/run-text/supply-check records in the project's store
`workflow/` area; run/turn observations have their own project record path.
The [library fixtures](../../../../app/src-tauri/src/workflow_library_tests.rs)
and records-portable-reconstruction fixtures exercise bounded synthetic
capture/reopen/import relationships. Their evidence does not establish a
person's registration or the approved native J2 outcome.

The owner-approved J2 scope remains exact source
`475c9b8f9c868fe1be9d0e1ef33a9cdd72aec75f`: one registration, one fresh reuse
turn, twenty minutes, stop-only/no retries, preserving the current project and
old-046 store. The A15, storage and workflow-record readers cited above have
identical bytes at 475c and the packet's App source basis. These proposals change no bytes of that subject and require no
new launch, build, model use or acquisition. Record only what that authorized
observation establishes; an agent-operated native gesture or an A15-shaped
capture is not evidence of a personal human act.

| Actual finding on that subject | Effect on recommendation and evidence |
|---|---|
| A15 library log and capture resolve the reviewed revision; reuse selection/run-text/supply-check and applicable run observations resolve in the preserved project store | Supports retaining the allocation and its explicit exception. It establishes these observed development paths only; no person attribution, cross-installation portability, full acceptance or release follows. |
| A15 is only in the project store, or its capture resolves elsewhere | Recheck the exact source/configuration and observed root against the library contract. Return a consumer/custody discrepancy; do not adopt a broader or different exception to match it. Suspend any claim that this subject demonstrated the recommended split. |
| Library act exists but capture or exact reviewed-content relation is missing/unresolvable, or UI says registered without durable supporting evidence | Return incomplete registration evidence for repair/disposition. Do not invent, recapture, duplicate or relabel the act. Keep the contractual evidence obligation; this finding does not justify narrowing it. |
| Registration resolves but fresh reuse's project records do not, or project/store identity changes | Keep the registration result at its actual scope and return the missing/misbound reuse evidence. The approved stop rule applies; repair the actual project-record consumer before claiming reuse provenance. No change to the library exception follows merely from this failure. |
| Neither registration nor reuse completes before the stop | Preserve the partial result. The source-grounded recommendation remains provisional on implementation evidence; one unsuccessful attempt is not evidence for a different store contract. |

Successful J2 would advance P2 only at its actual subject; it would not close
P3's failure/recovery/access obligations or P5's joined-host record/actor
requirements. A later persistence repair needs its own authority, exact version,
consumer reconciliation and independent scrutiny; it cannot be smuggled into
this documentation packet or the unchanged J2 subject.

## AS / RS citation identity: correct the live citation, preserve its basis

AS §6 / VC-21 and RS §8 / VC-38 require the same settings-in/record-out
exchange. Comparing the bodies from **Settings-in** to section end finds only
two differences: AS says `LOOP-v0.8` and RS says `LOOP-v0.9`, both citing §5.3
DF-6. Replacing those two labels in RS with `LOOP-v0.8` makes the bodies
byte-identical. Both already enumerate pending, granted, declined, not granted
and unanswered at end, with the same actor/grant, comparison and evidence-limit
meaning. Current LOOP DF-6 supplies those states. This establishes a citation
difference, not different destination behavior or a model-interface adoption.

Recommend this minimal citation-only candidate:

- In **RS §8 only**, change the two `LOOP-v0.9 §5.3 DF-6` citations (each
  wraps across a line) to `LOOP-v0.8 §5.3 DF-6`. Keep the current DF-6 state
  vocabulary, schemas and all other exchange bytes. The v0.8 citation denotes
  the retained common exchange basis; it does not roll back current LOOP.
- Keep AS §6 and VC-21, RS VC-38's reference to the same states in current
  LOOP, and historical consumed-input claims unchanged. Do not claim historical
  *whole-file* equality between AS and RS; the equality requirement concerns
  these exchange bodies.

AS whole-file SHA-256 remains
`4eca598f13c8c0745f94c605b8940a094b55e57b9f7478c989824af229085857`,
selected by the policy-standing and A16 product bases. The assessed current RS
is `7a026314e98555341dfa0f47a61efe26bc8d91dfda607add48d47c8e95fe1b22`;
those product bases' older RS bindings describe different actual subjects.
The candidate would change current RS bytes and therefore requires checking
its actual live selectors/copies. It authorizes no historical repin. The ACT
source split and existing dynamic S-6 drift remain as described in the ACT note.

This is the **citation-only** disposition at the assessed basis. If the owner
also adopts LOOP's proposed `turn failed` destination-close cause, the AS
transition/schema and RS close-cause consumers need the separate substantive
amendment described in the LOOP note. That would change live AS identity;
retain `4eca598f…` as the historical product subject and establish any needed
new current consumer binding explicitly. Re-compare the resulting exchange
bodies and actual consumers; a citation correction cannot adopt the new cause
or preserve a claim that all of AS stayed byte-identical.

Alternative: update AS citations to v0.9. That also preserves the compared
exchange meaning but changes the whole AS file bound by both historical product
bases for no behavioral gain. A new explicit current adoption, if needed by a
live consumer, must be separate from those retained historical identities.
Keep both files unchanged if citation reconciliation is deferred; report the
two-label difference truthfully rather than claiming current byte equality.
No P2, P3 or P5 witness should wait for this citation-only work.

Next actor: App Agent 0 presents the A15-only exception and citation correction
with the ACT/LOOP companions to the owner, then assigns any selected amendment.
Final integration and the publication recommendation remain Agent 0's; acceptance
and release remain owner decisions. The RS register-direction no-change
disposition stands.
