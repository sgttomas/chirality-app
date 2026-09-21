# D-GOV-43 review feedback, round 1, and dispositions

Origin: an independent reviewing agent engaged by the owner; relayed by the
owner on 2026-09-11 with the words "Let's iterate to get the best proposal
... You don't have to adopt everything, it's offered as feedback for your
consideration." The feedback is reproduced verbatim below, followed by
HELP_HUMAN's disposition of each point in revision 2 of the proposal.

## Feedback (verbatim)

> Please revise D-GOV-43 around the following aligned direction.
>
> The re-platform remains the intended architecture: the Electron main
> process owns a stock, version-pinned Codex App Server over stdio. Chirality
> supplies its conversational interface, roles and reusable workflows through
> supported upstream mechanisms.
>
> 1. Use T3-style authentication separation by default.
>
> Use a Chirality-specific effective Codex home/auth overlay that shares the
> appropriate user configuration and resources while keeping Chirality
> authentication separate. Do not default to the same authentication store
> used by the user's other Codex clients.
>
> Codex remains responsible for credentials and OAuth. Chirality must not
> copy existing credentials to populate the overlay. Verify the actual
> credential-backend behavior: signing into or out of Chirality should not
> sign another Codex client in or out. Describe shared configuration/session
> storage accurately; this is authentication separation, not complete
> filesystem or account-data isolation.
>
> 2. Add Chirality role instructions to Codex's normal instructions.
>
> Preserve the upstream base instructions and tool behavior. Supply the
> active Chirality role and selected workflow context through supported
> additive mechanisms. Demonstrate that delegated work receives the intended
> role instructions too.
>
> 3. Make governance simplification a primary deliverable.
>
> Remove obsolete requirements along with the mechanisms they governed. Do
> not recreate the retired daemon's admission, supplier-certification and
> identity-binding machinery under new names.
>
> For affected requirements and checks, establish their actual purpose, then
> retain, adapt or retire them. Historical evidence remains preserved, but
> need not be regenerated to resemble the new architecture.
>
> Update conflicting live contracts, scopes and notices in a coordinated
> tranche. Avoid repeated approval requests that merely restate an accepted
> decision. Retain meaningful human decisions and independent review.
>
> Remove cosmetic whitespace as an acceptance or merge condition. Drop README
> self-hash machinery unless an actual consumer needs it. Remove duplicate
> test execution where existing results establish the same thing; retain
> checks for distinct integration conditions.
>
> 4. Prove the complete product loop early.
>
> The functional spike must demonstrate:
> - Native Plan Mode, discussion and revision.
> - Execution with real file reads and tool use, including work exceeding
>   the former stream-silence timeout.
> - Saving a reusable workflow through conversation.
> - Reusing it on another assignment and iterating on it.
> - One real delegated task with the intended role instructions.
> - Quit/relaunch followed by a successful continuation.
> - Correct interruption and approval handling.
>
> This extends the existing demonstration rather than creating a broad new
> qualification program.
>
> 5. Keep protocol support faithful and implementation scope bounded.
>
> Generate bindings for the pinned version, but explicitly establish
> experimental-field support. The saved schema omits collaborationMode, and
> the saved T3 source augments its generated turn type. Plan Mode therefore
> needs an actual integration check.
>
> Preserve useful and unfamiliar activity for inspection without requiring
> bespoke UI for every upstream method. Keep renderer isolation, validated
> IPC and credential protection. Preserve the simple UI, prominent workflows
> and less prominent, read-only skill inspection.
>
> 6. Integrate efficiently.
>
> Reuse the existing conversation, plan, workflow, attachment and viewer
> components where appropriate. Define preservation/continuation for
> existing trial chats explicitly. Independently review the source before
> one consolidated signed build, then verify native behavior.
>
> Local-model integration remains deferred.
>
> The immediate target is a complete, reliable:
> plan → execute → save → reuse → iterate
> experience with Codex.
>
> Please revise the existing proposal accordingly and surface only
> consequential unresolved choices. The replacement should substantially
> reduce both implementation complexity and the governance needed to
> maintain it.

## Dispositions in revision 2

| Point | Disposition | Where |
|---|---|---|
| 1. Authentication separation by default | Adopted. Chirality effective home with private `auth.json`, shared configuration, resources and sessions; no credential copying; credential-backend behaviour (file versus OS keyring) verified in the spike so sign-in and sign-out are Chirality-scoped; direct use of the user's home is an explicit opt-in. Revision 1 had defaulted to the user's own home. | Ruling item 3, spike check S-8 |
| 2. Role instructions through normal Codex instructions | Adopted. Upstream base instructions preserved; role and workflow context through `developerInstructions` and additive turn input; project `AGENTS.md` discovery; delegated work verified to receive role instructions. | Ruling item 8, spike check S-5 |
| 3. Governance simplification as a primary deliverable | Adopted, including the coordinated tranche, the purpose test for affected checks, no re-creation of admission, certification or binding machinery, retirement of whitespace as a merge condition, removal of README self-hash machinery from this packet, and de-duplication of test execution. The coordinated single tranche across loops is surfaced as an explicit owner choice because it changes how loops adopt. | Ruling item 11, IMPACT.md "Purpose test", unresolved choice A |
| 4. Prove the complete loop early | Adopted verbatim as the measure of done, extending the R17 demonstration. | Ruling item 12 |
| 5. Faithful protocol, bounded scope | Adopted. Generated bindings plus an explicit experimental-field augmentation list (`collaborationMode` first), an integration check for Plan Mode, generic inspection for unfamiliar items, renderer isolation and validated IPC, prominent workflows and read-only skill inspection. | Ruling items 2 and 10 |
| 6. Integrate efficiently | Adopted. Reuse of existing components; explicit preservation of daemon-era trial chats (read-only by default, continuation surfaced as a choice); independent source review before one consolidated build; local models deferred. | Ruling items 5, 13, gates; unresolved choices B and C |

Not adopted: nothing in substance. One adaptation: the feedback's "coordinated
tranche" is recorded as a ruling item rather than assumed, because Root
doctrine currently makes each loop decide its own adoption.
