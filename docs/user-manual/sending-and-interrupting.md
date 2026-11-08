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
