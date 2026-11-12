# Worked example: moving a shared note

This is a constructed illustration. The product, people, observations, and
source labels below are fictional. No software was inspected, experiment run,
product observation independently verified, or human decision obtained. These labels
demonstrate how real evidence could support an account; they are not evidence
of any product. The arrangement is optional.

## Purpose and scope

Imagine investigating how moving a note between collections affects access and
undo, to inform the design of another notes application. Ari can edit both a
shared collection and a private collection. Bea can use the shared collection.
The illustrative configuration has no additional direct grants on the note.
A real record would also identify the product revision, role settings, source
locations, and reproducible setup.

## Illustrative observation record

| Label | Constructed observation or coverage limit |
| --- | --- |
| E1 | Ari and Bea can open the shared note through `/notes/n17`. Ari moves it to the private collection. Ari can still open the same link, and the text is unchanged. |
| E2 | After the move, Bea opens the link in a fresh view and receives an access-denied result. |
| E3 | In a separate move-and-undo trial with no intervening edits, Ari undoes the move. The note returns to the shared collection with the same link and text; Bea can open it again. |
| Q1 | Bea's already-open editor and any unsaved edits were not examined after the move. |
| Q2 | Undo after an intervening edit, and behaviour under additional access grants, were not examined. |

## Reader-facing reference account

**REF-MOVE-1 — Reorganisation, access, and reversal.** In the illustrated
configuration, moving the note preserves Ari's access through its existing
link and leaves its text unchanged (E1). The operation changes Bea's ability to
open that link in a fresh view (E2). Moving is therefore consequential to both
organisation and access in these conditions. The same visible link does not
establish how the application stores identity internally.

With no intervening edits, undo restores the prior collection, text, and tested
access (E3). This does not establish that undo reverses only the location change:
restoring an earlier snapshot could produce the same observed result. Q2 needs
a distinguishing experiment before either explanation is presented as fact.

The account leaves Bea's already-open editor unresolved (Q1). A new designer
cannot infer whether a later save succeeds, fails with recoverable text, or
loses unsaved work. These alternatives affect access, preservation of work, and
the meaning of undo together.

## Proposed departure and its consequences

**Proposal, not a human decision:** before a move changes who can access a note,
show the affected people and let the mover reconsider. This is desired new
behaviour, not an observation about the reference.

That proposal raises connected choices: which grants determine the affected
people, when access changes, and what an already-open editor should do. The
human can choose target behaviour with the reference uncertainty visible, or
request further investigation. Preserve REF-MOVE-1 when recording that choice.

## Return and check

The hypothetical packet would be a partial account awaiting independent
checking, useful for discussing product alternatives. It does not establish
the answer to Q1 or Q2 or readiness to rely on a complete access-and-undo model.
Carry those questions and the review obligation into any qualified next use.

Ask a reader to explain the move and propose its target behaviour using only
this account. They should distinguish the illustrated observations from the
unknowns and identify where a new choice is needed. Record consequential guesses
as gaps. The purpose is to support product conception; internal architecture and
implementation detail can remain open.
