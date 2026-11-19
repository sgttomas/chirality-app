---
name: chirality-app-workspace-setup
description: Guide users through workspace setup and account access.
metadata:
  kind: instruction
  surface: reference
---
# Set up your workspace

**Development-source guide, 1 November 2026. Not a completed desktop walkthrough.**

Use Desktop setup when the App asks for shared settings before Codex can start.
The App creates its own account home; setup does not sign you in or import
credentials from an existing home.

1. In **Desktop setup action**, choose a new account home. If an existing account
   is available, you may instead keep it and change only the next project.
2. For a new home, choose **Shared config.toml**, **Shared AGENTS.md** and
   **Shared skills directory**. Use their Browse controls, or enter an absolute
   path. An explicitly selected target may be missing; review any reported limits.
3. In **Project on next launch**, choose a directory or **No project**. For a new
   home, also explicitly select **Supplier for next launch**. The development
   supplier's displayed standing is not a qualification statement.
4. Select **Review setup effects**. If it is unavailable, the explanation above
   it identifies the next choice needed. While the App checks locations, wait
   for the result; repeated clicks do not submit another request.
5. Read the effects. Use **Edit setup choices**, or Escape within the review,
   to return without saving. To proceed, select the displayed save action and
   answer the App's native confirmation. Editing the local review cannot cancel
   a native question that is already open.
6. After a successful save, the choices apply on the next launch. The App does
   not quit, restart, sign in or change your current conversation for you.
   If setup fails or is cancelled, your entered choices stay available. Read
   the message, correct the cause and review again explicitly.

**Project trust.** Chirality's trust is on for a project you set up here,
unless you have switched it off. While it is on, Chirality marks the project as
trusted when it starts, continues or forks a conversation in the project's
folder, except in the cases named with the project's trust in Settings, and
Codex then loads the project's own instructions (its `AGENTS.md` files) and its
own Codex settings and rules (in the project's `.codex` folder). The review
states in full what that turns on, and the native confirmation carries the same
text or names it. With them, the project's own files can: start MCP server
programs on this Mac when a conversation starts, outside the sandbox, and have
Codex connect to MCP servers at addresses they name; set the shell environment
of the commands the agent runs, and through it have a start-up file of the
project's own run inside each of those commands, under the same access level as
that command; let commands run outside the sandbox without asking you, through
the project's rules, which Chirality cannot switch off while the project is
trusted; and stop new conversations from starting in the project, where Codex
cannot load the project's settings file, until the file is fixed or trust is
switched off. Read a project's `AGENTS.md` files and `.codex` folder before you
set up a project you did not write. You can switch trust off for a project in
Chirality while the project is open and its records can be written, and on
again with a confirmation; a change applies to conversations you start,
continue or fork after it. The release limitations give the limits (LIM-038).

**Setup details and source status** contains the current launch, resource and
supplier details. Problems that prevent setup remain visible above the form.

The connection overview distinguishes setup, connection and disconnection.
**Codex is connected** does not mean an account is signed in or a model chosen.
Use **Connection & access** for the existing account/provider and process
controls, and **New conversation** for an explicit model/access choice.
The navigation links open and focus their destination without starting Codex,
sending a message or replacing unsent work. Tab and Shift-Tab move through
native HTML controls; Enter activates a focused link or button, and Space
activates a focused button or disclosure summary.

Sign-in and the native confirmation retain their existing actor and
permission requirements. This guide does not authorize credentials, signing or
release. Verify the procedure on the selected release candidate before publishing
it as a release manual.
