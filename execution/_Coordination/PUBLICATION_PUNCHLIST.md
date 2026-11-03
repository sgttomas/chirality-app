# macOS 4.0.0 publication punchlist

Basis: owner-reviewed direction on 2026-11-03, including both standalone journeys
before shipment. Baseline main `9670f734`; retained signed candidate `b3dd4145`
is from `f664ee1d`, stapled DMG `34ab5661`. This is a finite coordination index.
Requirements, implementation meaning and evidence stay in the owning deliverables.
Neither a checked row nor this document supplies owner acceptance or release.

## Audit of the previous release list

CURRENT_EXECUTION_BASIS already listed five remaining results: desktop/native
journeys; joined SWBPIPE evidence; supplier/package/installed custody; terms and
public distribution; and the owner decision packet. That list was not completed.

- Completed for the retained candidate: selected production build, profile and
  publisher joins, signing, notarization, stapling and static Gatekeeper checks.
- Implemented but not complete product evidence: setup/history/workflow UI
  slices and interruption/submission repairs. Source checks did not establish
  the owner's usable journey. The presentation deliverable explicitly retained
  that limit; coordination failed to keep it central.
- Still open: complete native journeys/recovery/access, joined SWBPIPE witness,
  supplier qualification and notice gaps, installed custody/enrollment results
  and the owner publication decision. OpenAI terms applicability is already
  adopted; a repeated terms acceptance is not a new gate.

## Bounded results

| ID | Result and finish condition | Standing / next action | Owning deliverables and delivery owner |
|---|---|---|---|
| P1 | Set up a project, select an existing workflow, supply inputs, run it to completion and find the results without agent interpretation of engineering controls. | OPEN; first product increment. Identify and repair actual obstacles in the current implementation, then observe the complete journey. | [J1](../PKG-02/DEL-02-02/Work/PUBLICATION_JOURNEYS.md#j1--use-an-existing-workflow), DEL-02-02 with DEL-01-04/05; product manager, Agent 0 integration. |
| P2 | Do useful work, create/trial/review/register a reusable workflow, return to unfinished work and later run the saved workflow with new inputs. | OPEN; follows P1 and must finish before 4.0.0. | [J2](../PKG-02/DEL-02-02/Work/PUBLICATION_JOURNEYS.md#j2--create-save-return-and-reuse), DEL-02-02; product manager, native examiner. |
| P3 | Applicable candidate-bound request/approval, cancellation, interruption/recovery, close/reopen/Quit and three access-mode results, with failures repaired or explicitly returned for owner disposition. | OPEN; reuse P1/P2 observations for their actual claims, add only the remaining required cases. No old unattended harness is resumed. | [Standalone qualification](../PKG-09/DEL-09-02/Work/STANDALONE_QUALIFICATION.md), DEL-01-01/02/03/04/05; native manager. |
| P4 | Actual installed S4/supplier custody and applicable SEAL-C enrollment/continuity evidence joined to the candidate. | OPEN; static joins are complete for b3dd4145, real installed/native results are not. Enrollment remains a concrete owner act. Rotation unavailable/SC-5 blocked is the accepted 4.0.0 limitation, not a pass. | [Signing join](../PKG-01/DEL-01-06/Work/SEAL_C_KEYCHAIN_SIGNING_JOIN.md), DEL-01-04/06 and DEL-09-02; runtime and packaging managers. |
| P5 | Joined live SWBPIPE workflow with actual host/model/configuration, controlled application, outcomes and attributable person acceptance, plus applicable lifecycle/recovery evidence. | OPEN; component results do not close it. App Agent 0 coordinates with SWBPIPE Agent 0; no SWB implementation authority transfers here. | [Local host qualification](../PKG-09/DEL-09-07/Work/LOCAL_HOST_QUALIFICATION.md); examination consumer and external SWB owner. |
| P6 | Qualified selected supplier pin and complete applicable shipped notice/source associations, with unresolved coverage explicitly resolved before release. | OPEN; source receipts/font notices are progress, not full coverage. Work from the existing gap account; no unapproved downloads. | [Cached notice inputs](../PKG-01/DEL-01-06/Work/CACHED_SHIPPED_NOTICE_INPUTS.md), DEL-01-01 and DEL-01-06; packaging with runtime qualification inputs. |
| P7 | Package the finished source; verify resource/profile/supplier identity, sign/notarize/staple and perform the applicable installed/quarantine witness on that final subject. | COMPLETE only for current signing/notary substeps; final product candidate remains OPEN. Preserve successful process/evidence; do not repackage every small UI change. Local unquarantined install is not W-0/W-2. | [Production input preparation](../PKG-01/DEL-01-06/Work/PRODUCTION_INPUT_PREPARATION.md), DEL-01-06; packaging manager. |
| P8 | Present the exact final candidate, joined results, limits and continuing obligations for the owner's publication decision and separately applicable replacement decision. | OPEN; no release authorized. Preserve existing terms applicability and distribution `not_made` until actual owner act. | [Owner packet scope](../PKG-11/DEL-11-03/ScopeOfWork.md), DEL-09-12/11-01/11-03 with DEL-01-06; Agent 0 and owner. |

## How this constrains work

P1 then P2 drive product implementation. P3/P4 gather applicable evidence from
those journeys; P5/P6 remain separate real release obligations. P7 final assembly
follows the product fixes; P8 is the owner decision, not an agent completion claim.
Windows remains after the initial macOS release. No new v3 comparison campaign,
VM work, rotation implementation or unrelated polish is introduced.

A row closes only with links to the owning deliverable's reconciled result and
applicable candidate evidence. A passing PR is an implementation step, not a
whole-journey pass. Preserve source checks and candidate evidence at their
actual identities; run additional checks only for changed behavior or a specific
unresolved claim. Do not reopen unchanged passing evidence merely because it
moves between owners.

New work must identify the open row it advances and a concrete finish condition.
If it changes the publication commitment or adds a new gate, bring the choice
to the owner. Improvements beyond the agreed result stay outside this push.
A stalled row names the next useful result and who can produce it; Agent 0
checks actual delivery rather than treating a dispatched brief as progress.
