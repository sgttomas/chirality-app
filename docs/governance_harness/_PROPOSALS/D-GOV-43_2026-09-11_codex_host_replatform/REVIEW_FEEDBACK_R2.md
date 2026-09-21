# D-GOV-43 review feedback, round 2, and dispositions

Origin: the same independent reviewing agent engaged by the owner; relayed by
the owner on 2026-09-11 with the words "Once more consider the other agent's
feedback. Seek any further answers from me if needed. Otherwise update your
proposal for my direction." The feedback is reproduced verbatim below,
followed by HELP_HUMAN's disposition of each point in revision 3.

## Feedback (verbatim)

> Revision 2 is directionally ready. I support the recommendations for
> choices A, B and C, subject to the owner's ruling. Please make the
> following focused corrections without expanding the proposal process.
>
> 1. Reconcile the actual application material.
>
> AGENTS.proposed.patch still describes using the user's own authentication.
> Update it to describe Chirality-separated, Codex-managed authentication,
> shared configuration/resources, and additive role instructions.
>
> IMPACT.md still says residency requirements remain prospective and that
> the nine held bindings must be re-seated rather than dropped. Align those
> passages with the revised decision. Remove obsolete obligations outright
> where their purpose disappears.
>
> 2. Make coordinated authority explicit and bounded.
>
> This ruling should authorize the named Root, Runtime and App changes
> together. Notices record their application; they do not restart approval
> of the same decision.
>
> Keep independent review as an engineering responsibility, not a new human
> approval prompt. Bring back material scope changes or consequential
> findings, rather than routine implementation choices. This need not
> permanently change how unrelated project loops operate.
>
> 3. Do not preserve the old gate structure by renaming it.
>
> The purpose test should permit deleting whole families of obsolete checks.
> Do not automatically map nine historical bindings onto eight spike checks
> or preserve a 25-step packaging procedure.
>
> Group dispositions by shared purpose where sensible. A concise rationale
> and the reviewed Git changes are sufficient; do not build another
> elaborate register to demonstrate simplification.
>
> Retain normal dependency integrity, application signing and useful
> security checks. The prohibition concerns rebuilding the private
> supplier-admission system, not ordinary software integrity or
> request/session correctness.
>
> 4. Keep historical preservation inexpensive.
>
> Preserve old chats and evidence without promising continuation. Do not
> make a new history-import feature a release prerequisite merely to provide
> read-only preservation. Reuse an existing reader if straightforward;
> otherwise retain an accessible archive.
>
> Likewise, preserve executed checklists and packaging records unchanged.
> Create the new procedure and supersede their applicability rather than
> editing historical evidence.
>
> 5. Distinguish unfamiliar notifications from server requests.
>
> An unfamiliar notification can receive generic inspection. A server
> request needs an appropriate response or an explicit, visible unsupported
> outcome. A generic card alone must not leave Codex waiting indefinitely or
> imply approval.
>
> 6. Keep the MVP implementation bounded.
>
> Authentication separation is the default to implement and verify. Direct
> shared-authentication opt-in can be deferred; it adds another mode without
> helping the immediate target.
>
> The eight spike checks are a useful acceptance set, not a requirement to
> build two implementations or rerun every test after packaging. Reuse the
> production path and repeat only checks that exercise a distinct
> packaged/native condition.
>
> Proceed toward:
> plan → execute → save → reuse → iterate.
>
> Local-model implementation remains deferred. Preserve useful prior work,
> but remove its obsolete release obligations.

## Dispositions in revision 3

| Point | Disposition | Where |
|---|---|---|
| 1. Reconcile application material | Adopted. `AGENTS.proposed.patch` regenerated: shared configuration and resources, authentication separated for Chirality and custodied by Codex, additive instruction inputs preserving Codex's base instructions, no server request left unanswered; verified with `git apply --check`. `IMPACT.md` now retires K-RESIDENCY-1, SPEC §14.3/14.4 and the residency types, and retires the nine held bindings as a family instead of re-seating them. | Patch hunk 3; IMPACT Root table, Runtime table, load-bearing chain 1 |
| 2. Coordinated authority explicit and bounded | Adopted. Ruling item 11 authorizes the named Root, Runtime and App changes together; notices are records; the arrangement is bounded to this decision. Independent source review is an engineering responsibility; material scope changes and consequential findings return to the owner, routine choices do not. Choice A is folded into the ruling with the alternative noted. | Ruling item 11, gates 2 and 4 |
| 3. No renamed gate structure | Adopted. The purpose test is regrouped into six families; families 1 (private supplier admission and certification, including the nine bindings and the supplier packaging steps) and 2 (fixed-policy control) are retired outright; family 4 (ordinary software integrity: dependency integrity, signing, renderer isolation, request and session correctness) is retained. The Stage 9–13 procedure is superseded by a new short procedure. Rationale plus reviewed Git changes are the record; no register. | IMPACT "Purpose test by family", load-bearing chains; ruling item 11 |
| 4. Inexpensive historical preservation | Adopted. Trial chats preserved unchanged; viewable through the existing reader if straightforward, otherwise an accessible archive; no import feature as a prerequisite; no continuation promised. Executed checklists, packaging records, reviews and findings preserved unchanged with applicability superseded. Choice B folded into the ruling. | Ruling items 5 and 9; IMPACT App table and "Existing trial chats and executed records" |
| 5. Notifications versus server requests | Adopted. Unfamiliar notifications get generic inspection; every server request receives a response, an unfamiliar one an explicit JSON-RPC error and a visible "unsupported request" outcome; nothing waits indefinitely or implies approval. | Ruling item 2; patch hunk 3 |
| 6. Bounded MVP | Adopted. Separation is the only authentication mode implemented and verified; the direct shared-authentication opt-in is deferred. The eight checks are an acceptance set on the production path; after packaging only S-6, S-8 and signature/pin verification are repeated. Target restated as plan → execute → save → reuse → iterate. Local models deferred; residency requirements retired (choice C folded in) with useful prior work kept as reference. | Ruling items 3, 12, 13; gates 3 and 4 |

Not adopted: nothing. No further owner answers were needed; the three
revision-2 choices are folded into the ruling text with their alternatives
noted so the owner can strike any of them when ruling.
