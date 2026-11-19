---
name: chirality-app-send-and-interrupt
description: Guide users in sending messages and interrupting live turns.
metadata:
  kind: instruction
  surface: reference
---
# Send a message and interrupt a live turn

**Development-source guide, 2 November 2026. Not a completed desktop walkthrough.**

Choose the intended **Current-generation conversation** before sending. If
none is available, use **New conversation** or **History** to start or continue
one explicitly. Choosing a conversation does not send the text already in the
composer.

Write in **Text**. The message above it explains whether Codex is disconnected,
a conversation is missing, an operation is pending, or text is ready to send.
The ordinary text draft stays available when you change conversations or when
a send fails. Check the target before pressing **Send text**.

An optional model identifier applies to ordinary text turns only; leaving it
empty keeps the native conversation's model choice. It does not change the
conversation's role, access entry or home. If attachments are selected, **Send
text only** excludes them; use the separate attachment action to include them.
Do not assume an acknowledgment means the model completed the requested work.

The ordinary Send, plan/default, steering, attachment and turn-interrupt controls
allow one pending turn operation from this panel at a time. Repeated clicks or
switching between those controls do not queue a second request while its command
and follow-up view read are pending. Wait for the result before choosing another
action. If the connection has closed, these sends are unavailable and the draft
stays here; reconnect or inspect History rather than repeatedly pressing Send.
Attachment submissions keep the entire selected order and never fall back to a
text-only send after a refusal.

## When the agent asks you a question

When Codex offers the conversation's agent the question tool, the agent can
ask you through a request at any permission level. The question appears in the
conversation with the choices the agent offers and room for an answer in your
own words, and the conversation is counted among what is waiting on you until
you answer or decline. Nothing answers for you: the turn waits, however long
you take, and closing the window answers nothing.

Three limits apply:

- Only the conversation's own agent can ask this way. An agent it delegated
  work to cannot; it has to return its question to the agent you are talking
  with.
- A question that is still waiting when Codex stops (you stop or restart
  Codex, quit the App, or Codex ends unexpectedly) is not asked again
  afterwards. Chirality shows the question as a past request when its record
  is available and shows the turn status Codex reports. If the turn was last
  observed in progress and no later status is available, its outcome is
  unknown. Send a message to continue.
- An agent may also ask in a message. Chirality shows the message and uses
  Codex's reported turn status. Only a request makes the question count as
  waiting for your answer.

### A question the agent asks and goes on from

On some models Codex gives the agent a second way to ask, which does not wait:
the agent asks, its turn goes on, and nothing is held for your answer. The
question appears as a card at the agent's message, with the choices it offers
and room for your own answer. Choose or type, read the message the card shows
(each question you answered, in quotation marks, then the option you chose or
your own answer), and press **Send answers**: it is sent as your own next message in that conversation,
exactly as shown. Nothing is sent until you press, and you can as well answer by
writing a message yourself.

"Waiting on you" lists such a question as "the agent asked a question and went
on" until a message from you follows it. It is counted in the line's number
and not among the requests from Codex. Any later message from you ends that
listing, whatever it says; Chirality does not judge whether it answered the
question.

Its limits:

- Chirality lists such a question only after it has established the
  conversation's reading in the Codex process and home in use. Continuing
  from History does not establish that reading: until the conversation
  receives a message, "Waiting on you" names it as not read and says its
  status is incomplete. You can open a stored turn's items in History to see
  any question Codex returned, then reply by sending a message in the
  continued conversation.
- Only the conversation's own agent is given this way to ask. A question seen
  in a delegated agent's conversation is shown with no way to answer it
  there; the agent you are talking with can relay it.
- Nothing about such a question is kept across a relaunch.
- Sending from the card follows the rules of the message box's own Send: one
  operation at a time, the conversation open in front of you, and no earlier
  ordinary text send to it left unconfirmed. The card sends no model, effort
  or collaboration-mode choice from the message box. If the agent's turn is
  still running, the send goes the way the message box's Send goes then.

## Interrupt one observed live turn

1. Choose the conversation whose work you intend to interrupt.
2. Under **Interrupt a live turn**, choose an **Observed live turn**. The status
   explains why the action is unavailable if no live turn is currently observed.
3. Press **Interrupt selected live turn** once. Wait for the native turn status;
   an acknowledgment alone does not establish turn end or rollback.

New messages are paused during a Stop/Restart Codex operation. The separate
turn-interrupt control remains available if its source is still ready and the
turn is observed live, provided no operation in the conversation panel is
pending. It sends the exact selected generation/conversation/turn to the host,
which rechecks them. Once the source is stopping, closed or otherwise not ready,
this control is unavailable. It never confirms or dismisses a Stop/Restart
question for you.

If interruption is already requested, wait for status rather than repeating it.
If it fails, read the error; the App does not retry automatically and keeps your
ordinary text. No observed live turn is not proof that every activity or child
has ended. Interrupting a turn does not end the workflow run, settle a waiting
permission request or prove that delegated work has stopped.

After a restart, use [History](finding-conversations.md) to inspect prior work
and continue explicitly. Keep failed, partial and unknown outcomes distinct
from completion before deciding what to do next.
