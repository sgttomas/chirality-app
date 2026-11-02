# Find and continue a past conversation

**Development-source guide, 1 November 2026. Not a completed desktop walkthrough.**

Use **History** in the workspace navigation to open the history panel. This
moves keyboard focus there without reading or starting a conversation.

1. Connect to the intended Codex home using **Connection & access**. History
   belongs to that home; another home can have different conversations.
2. Choose **Newest first** or **Oldest first**, then **Read stored conversations**.
   Wait for the requested page. No automatic retry is made if the read fails.
3. Use **Find in received conversations** to search the IDs and previews already
   received. The count covers those rows only. It does not search unread pages
   or other homes. Use the page controls explicitly to read more, or **Clear
   search** to restore the received list. Changing home or generation clears
   this local filter.
4. Choose a **Stored conversation**. Filtering never changes this selection;
   a selected row outside the search remains labelled in the chooser. Select
   **Read turns** and then **Read items for this turn** to inspect prior work.
   Metadata and goal reads are separate. Each page's source and limits remain
   available; a returned status describes that read, not necessarily live work.
5. Only when you want to open it for new messages, choose **Continue selected
   conversation**. The App waits for a matching continuation response before
   changing the operational conversation. A failed or superseded continuation
   leaves your current selection and unsent work intact. It does not resend a
   prior message for you.

Reading is separate from continuing. A history page, empty result or exhausted
cursor does not establish that every conversation, turn or child has been seen.
If a refresh fails, retained rows are previous observations, not a fresh success.
Inspect the visible error and source details before retrying explicitly.

Continuation also differs from recovering the whole undertaking. Check the
workflow, outstanding requests and reported limits before starting more work.
Original role evidence can remain unknown after a restart. Neither tool success
nor a rendered transcript establishes review, acceptance or a person's act.
