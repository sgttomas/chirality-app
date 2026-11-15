---
name: chirality-app-release-limitations-4-0-0
description: List the limitations the App 4.0.0 release carries, each with its reason.
metadata:
  kind: instruction
  surface: requirements
---
# Chirality App 4.0.0 release limitations

Companion to [`RELEASE_TARGET_4.0.0.md`](RELEASE_TARGET_4.0.0.md), for its
exit criterion 12. This is the single list of what the release does not do
that a person could expect of it. Agent 0 keeps it, with a reason for each
entry. The owner sees the whole list with the request for the verdict
(criterion 13), and what a person receives with the package is written from
it (DEL-01-06).

An entry states a limitation, its reason and what it means for a person using
the App. It holds no status: an entry that
no longer applies is removed, and Git keeps its history.

## Entry form

Each entry is one subsection:

- **Id:** `LIM-nnn`, assigned in order and never reused.
- **Exit criteria:** the release target's exit criteria it affects, by number.
- **What is unavailable:** in the person's terms.
- **Why:** the reason, in one or two sentences.
- **What the person does instead:** the supported alternative, if any.
- **Basis:** the deliverable that governs it.

An entry is added in the same pull request that makes the limitation standing.

## Entries

### LIM-001: The capture-seal key cannot be rotated

- **Id:** LIM-001
- **Exit criteria:** 8
- **What is unavailable:** once a person has protected registered workflows
  with their keychain, the key that seals registrations cannot be replaced
  with a new one.
- **Why:** no rotation mechanism is built for 4.0.0.
- **What the person does instead:** nothing replaces it in 4.0.0; the key
  enrolled on an installation stays the key that seals and verifies
  registrations there.
- **Basis:** DEL-01-04 (keychain protection); DEL-01-06 REQ-007.

### LIM-002: The keychain-held approval policy can be stored a bounded number of times

- **Id:** LIM-002
- **Exit criteria:** 8
- **What is unavailable:** on an installation with keychain protection, the
  workflow approval policy can be stored 256 times in all, counting the first,
  written when protection is set up. Saving the policy unchanged also uses
  one. After that the policy can no longer be changed and stays as last
  stored.
- **Why:** each stored policy is kept as its own keychain item in a bounded
  sequence, so that an edit, deletion or replay outside the keychain cannot
  change the policy; writes past the bound are refused.
- **What the person does instead:** nothing replaces it in 4.0.0; once the
  allowance is used, further changes to the policy cannot be saved.
- **Basis:** DEL-01-04 (keychain protection); DEL-02-02 (the workflow
  approval policy).

### LIM-003: macOS on Apple Silicon only

- **Id:** LIM-003
- **Exit criteria:** 10
- **What is unavailable:** the App on Windows, on Intel Macs, or on a macOS
  earlier than 15.
- **Why:** 4.0.0 targets macOS on Apple Silicon first; Windows follows the
  macOS release.
- **What the person does instead:** use a Mac with Apple Silicon running
  macOS 15 or later.
- **Basis:** DEL-01-06; PRD V4-CST-02.

### LIM-004: No standalone OpenAI API-key access

- **Id:** LIM-004
- **Exit criteria:** 6
- **What is unavailable:** entering an OpenAI API key in the App as a way to
  reach a model.
- **Why:** it is omitted from this increment; the App reaches a model
  through the person's ChatGPT account.
- **What the person does instead:** sign in with a ChatGPT account.
- **Basis:** DEL-01-05; PRD V4-APP-02.

### LIM-005: v3 chats are not imported

- **Id:** LIM-005
- **Exit criteria:** 14
- **What is unavailable:** bringing conversations from v3 into v4. Existing
  data under the App's identity is left as it is: nothing imports, resets or
  reseals it.
- **Why:** no migration or import of v3 chats is selected for the initial
  delivery.
- **What the person does instead:** v3.0.1 stays available as the fallback
  for work and history kept there.
- **Basis:** DEL-11-01; PRD §8 and OQ-12.

### LIM-006: Released and examined as a standalone application

- **Id:** LIM-006
- **Exit criteria:** 1, 2
- **What is unavailable:** assurance about the App's use with a host
  application such as SWBPIPE, and Domains. 4.0.0 is released and examined as
  a standalone application; its use with a host is not examined for this
  release.
- **Why:** a live host journey is the host's own requirement and is outside
  this release; Domains follows in a later increment.
- **What the person does instead:** use the App standalone, with the
  workflows it ships and those the person registers.
- **Basis:** DEL-09-07 and DEL-09-11 (held outside 4.0.0); PRD §8.

### LIM-007: Records packages and log checkpoints are unsigned

- **Id:** LIM-007
- **Exit criteria:** 15
- **What is unavailable:** a signature on an exported records package, and a
  signed checkpoint over a records log. A package verifies as internally
  consistent with its own manifest and chain heads; it does not show which
  installation produced it, and a package whose records and manifests were
  replaced together still verifies. A records log shows a changed, removed or
  reordered line only where later lines still carry their original links: a
  change to the content of a log's last line that keeps its link, lines
  removed from its end, and an edit by someone who recomputes the links after
  it can go unshown.
- **Why:** no key is chosen to sign log checkpoints and export manifests.
- **What the person does instead:** verify a package with the verifier it
  carries, and establish where it came from by other means.
- **Basis:** DEL-04-03 (TBD-003; AC-009 and AC-011).

### LIM-008: Library workflows ship as their method text, without the Library's tools

- **Id:** LIM-008
- **Exit criteria:** 1, 10
- **What is unavailable:** the App includes every workflow of Chirality
  Library 3.4.0 as its method text and gives a selected workflow to the agent
  exactly as the Library wrote it. It does not include the rest of the
  Library. Some workflows name the Library's tools, a skill or role files,
  and the steps that use them cannot be done from the App alone. Reading
  every file of each of the 71 packages for tool, skill and role paths that
  exist in the Library release, 43 name a Library tool and a few name a role
  file or a skill; a tool or skill named in words without its path is not
  counted. These are counts of what the text names, not of what a run
  requires: the Library does not state, for a workflow, which of the tools it
  names are required and which are optional, conditional or historical. No
  workflow declares its required tools in the App's form, so before a run
  each one reads as "requirements not declared" and the App cannot say which
  of its tools are available or missing.
- **Why:** the owner's choice for 4.0.0 is that the workflows ship as written
  and the Library's tools and skills do not ship. Library 3.4.0 does not
  state a workflow's requirements in the App's portable form, and it has no
  packaged or installable distribution of its tools.
- **What the person does instead:** the tool steps of such a workflow need
  the Library tools it names to be present at their original relative paths.
  Obtain them from the Library edition the workflow names as its source
  (Chirality Library 3.4.0, tag `library-v3.4.0`), keeping their paths, the
  resources they need and their licence notices, and point the agent at them
  in the conversation. The whole Library is not needed for this.
- **Basis:** DEL-02-02 (AC-014, TBD-005); DEL-02-03 (the requirement check).

### LIM-014: An interrupted read log stops the records capability answering reads until the person renames it

- **Id:** LIM-014
- **Exit criteria:** 15
- **What is unavailable:** reads through a project's records capability, once
  an interruption has left the project's read log ending in a read that was
  not recorded completely (the App was stopped, or the Mac lost power, while
  it was recording a read). Until the person acts, every read asked for
  through that capability is refused, and the refusal, shown in full with the
  conversation records capability, says why. This does not prevent agents
  reading files directly. Nothing already recorded is lost: the cut-short
  read was never answered, and every read that was answered stays in the read
  log.
- **Why:** every read asked for through the records capability is recorded
  before it is answered, and the App does not cut, close or rewrite a line of
  the read log, so it cannot record another read after an unfinished one. In
  4.0.0 the App does not set the file aside by itself.
- **What the person does instead:** rename the read log, in the same folder,
  to exactly the name the refusal gives (it begins `records-reads.jsonl.torn-`);
  the refusal names the file with its full path. The App then starts a new
  read log at the next read. The renamed file stays in the records store and
  is included byte for byte in exports of the project's records. The records
  capability does not use it to answer reads.
- **Basis:** DEL-04-03 (REQ-011, AC-012; REQ-012).

### LIM-015: A local model server is not offered

- **Id:** LIM-015
- **Exit criteria:** 6
- **What is unavailable:** reaching a model through a local model server.
  This release does not offer a local model server; it comes in a later
  update. A conversation on a local provider defined in the person's own
  Codex settings is not offered either. In the home that uses the ChatGPT
  account, the App starts Codex on the built-in OpenAI provider whatever
  default provider the person's Codex settings name; a conversation saved
  earlier on another provider can be opened there and cannot run a message.
  Where a managed Codex requirement names another provider, that home's
  Codex does not report the built-in one, and the App starts no ChatGPT
  account conversation and says so.
- **Why:** this release concentrates on Codex with the ChatGPT account; a
  local model server follows in a later update.
  At the selected supplier version, Codex runs conversations only on the
  provider its process started with, so the App starts the account home's
  Codex on the built-in provider.
- **What the person does instead:** sign in with a ChatGPT account.
- **Basis:** DEL-01-05 (its section for 4.0.0; REQ-003, REQ-005 and AC-005
  for the account home); PRD V4-APP-02.

### LIM-016: A pause at a point is the agent's cooperation

- **Id:** LIM-016
- **Exit criteria:** 2, 4
- **What is unavailable:** a pause the App enforces. When a point or a
  declared checkpoint asks the agent to pause, whether it pauses is the
  agent's cooperation; the App does not stop it. Where the agent does end its
  turn, delegated agents and background commands may still be running. The
  App shows that the agent was asked to pause and, separately, whether a turn
  completed, and never says the work is held or blocked.
- **Why:** holds the App itself enforces are phased to the governance layer
  and are not built for 4.0.0.
- **What the person does instead:** read what is still running before relying
  on the pause, and stop a turn or Codex when work must not go on.
- **Basis:** DEL-02-03 (REQ-002, TBD-006); PRD V4-WF-05, V4-EXE-05.

### LIM-017: Reading is not limited at any permission level

- **Id:** LIM-017
- **Exit criteria:** 6
- **What is unavailable:** a permission level that limits what the agent can
  read. Every level limits where it may write, network for the commands it
  runs and when it asks; at every level Codex can read whatever the person's
  macOS account can read.
- **Why:** the levels the App offers in 4.0.0 limit writing, network and
  asking; none of them limits reading.
- **What the person does instead:** keep material the agent must not read out
  of the reach of the account the App runs under.
- **Basis:** DEL-01-04 and DEL-04-02 (the permission level); PRD V4-AUT-06.

### LIM-020: A reopened run's end notice is not saved if the project stops being attached as the run ends

- **Id:** LIM-020
- **Exit criteria:** 4, 15
- **What is unavailable:** saving the end-notice record of a run reopened after
  a restart when, after the run's end is saved and the notice's basis is read,
  the project stops being attached to its records before the notice's first
  writer binding (for example, the records store's record of the project's
  folder is removed from outside the App). The run's end and its earlier
  entries are saved; the end-notice record is not. The App says so at once,
  with the cause: the record was not saved, its contents are held only while
  the App runs and are lost when it quits, and nothing in the App can save it
  later. Resolving the cause afterwards (confirming the folder's project)
  does not save it.
- **Why:** the end-notice record does not carry the project identity it was
  prepared for, and saving it later would need that. Publication already
  requires the notice's basis, the run's start record, to be readable in the
  destination with the same conversation and run. That stops a write to an
  unrelated history, but it cannot tell apart two projects holding the same
  history, so it does not replace the missing identity.
- **What the person does instead:** nothing in the App can save this original
  notice record. The run's end itself is saved. The held notice's text is not
  exposed in the App for copying.
- **What would remove it:** a record that carries the project identity it was
  prepared for, so that a later save on the person's explicit act can be
  checked against it. That is a change to what a record holds and is not
  decided. The person's way out of this and other fenced states is designed
  with the abandon and recovery work.
- **Basis:** DEL-02-02 (end-notice text), DEL-02-03 (run end) and DEL-04-03
  (records); DEL-04-03 REQ-007 and AC-008.

### LIM-021: The App's working folders are never removed

- **Id:** LIM-021
- **Exit criteria:** 4, 6
- **What is unavailable:** removal of the folders the App makes for its own
  work, and of what is in them. They are in the folder named after Chirality's
  data folder with " Working Files" added, beside it. For 4.0.0 that is
  `~/Library/Application Support/com.chirality.app Working Files`. The
  first-use page's Technical details names it and says how many folders are
  there. They accumulate with use, by kind:
  - **Codex's temporary folders**, one for each start of Codex. Each holds
    whatever the commands Codex ran wrote to their temporary folder, which can
    be the person's own material. The App does not establish that none of
    them wrote sign-in material there. Before, these files went to the
    shared temporary folder, which macOS may clear by itself; now they stay
    until the person removes them.
  - **The connector's folders**, one for each use of the connector. Each
    holds what git writes while reading: its settings, and folders for
    objects and references. Git reads the project's own repository in place,
    with every network protocol refused, and the App puts no sign-in there.
  - **The version check's folders**, one each time Chirality prepares to start
    Codex; later version checks of that start reuse it. The App never puts a
    sign-in there: it runs Codex in one only to read its version label.

  A folder made is checked while it is made, and not again. The Working Files
  folder and the subtree in use are checked again each time a folder is made.
  The folder that holds the Working Files folder is checked once, when the
  Working Files folder is established. The check is that each is the person's
  own, private by mode, and carries no access-list entry that allows access (a
  list of deny entries only passes), and that the folder holding the Working
  Files folder belongs to the person's account or to the system, and gives no
  other account the right to write in it, by mode or by an allowing
  access-list entry. A start is refused
  where one of these does not hold. The App does not
  defend these folders against a process that can write in that place while
  it makes them: any process with the person's own rights outside a sandbox
  can, and Codex can where its writable roots include that place.
  Signing out in Chirality acts on Codex's own home, as before. It does not
  reach these folders, as it never reached the shared temporary folder.
- **Why:** removing a folder safely needs the App to show that nothing which
  can write in the Working Files folder could have put something else in its
  place. The App can show that only once it decides every folder it gives
  Codex to write in, which follows in a later version.
- **What the person does instead:** remove the Working Files folder, or the
  folders in it, when neither Chirality nor any Codex it started is running.
  Nothing in it is needed between launches.
  - If Chirality could not stop its Codex when it quit, a process named
    `codex` can still be running after Chirality has gone. Activity Monitor
    shows it by that name. Quit it there, or restart the Mac, before removing
    the folder.
  - Removing the folder while Chirality is running harms no conversation's
    record. But a command of a running conversation that needs its temporary
    folder fails, a connector read in progress can fail, and no new start of
    Codex or version check is made until Chirality is started again.
- **Basis:** DEL-01-01 (CLM-006).

### LIM-027: A command an agent left running can keep running after Codex ends abruptly

- **Id:** LIM-027
- **Exit criteria:** 6
- **What is unavailable:** a way in the App to end a command that an agent
  left running in the background, other than closing Codex. Such a command
  keeps running until it ends or until Codex closes normally, which is what
  stopping Codex, restarting Codex or quitting the App ordinarily does.
  Stopping a conversation does not end it. It keeps the access it was started
  with, even if you choose a narrower level afterwards. When Codex closes
  normally, it ends these commands as it closes. If Codex ends abruptly instead
  (it stops unexpectedly, or, when you stop Codex, restart Codex or quit the
  App, it does not answer and the App has to end it), such a command can keep
  running after Codex and the App are gone, with the access it was started
  with.
- **Why:** Codex runs some such commands apart from itself, so they do not
  end just because Codex does. The App does not yet offer a way to end running
  commands on their own.
- **What the person does instead:** stop Codex, restart Codex or quit the App
  when you want commands an agent left running to end; this ends them when
  Codex closes normally. If the App or Codex may have ended abruptly, open
  Activity Monitor, look for the program that command ran (the conversation
  shows the command the agent ran), and quit it.
- **Basis:** DEL-01-02 (stop) and DEL-01-04 (the permission level). The level
  fixtures show, at the pinned Codex version (`app/supplier_checks/level`):
  - stopping a turn leaves running commands running;
  - closing Codex's input, as the App's stop does first, ends them and what
    they started;
  - ending Codex at once can leave a command and what it started running;
  - Codex's request to end a conversation's running commands ends them while
    Codex runs.

  That the App does not send that request in this release is read from the
  App's code. Stop Codex, Restart Codex and Quit all close Codex this way: they close
  Codex's input first, and end it at once only if it has not closed within
  3 seconds. This is read from the App's code (`hosting.rs` `stop_inner`,
  reached from `codex_stop.rs` and from the quit path), not shown by a test.

### LIM-028: A project whose records store cannot be used cannot start a conversation

- **Id:** LIM-028
- **Exit criteria:** 1, 4, 15
- **What is unavailable:** starting Codex, and so a conversation or sign-in
  through it, for a project whose records store cannot be used: its configured
  location is refused or unreadable, its registry is not read whole, or the
  project's attachment is refused (for example its link to the store is
  missing). The App starts and its setup works; a conversation without a
  project is unaffected. The App shows the store's refusal with its cause.
- **Why:** before Codex starts for a project, the App takes the project's
  activity, which protects closing, disposal and re-association while Codex
  runs, and that step currently requires the project's records to be writable.
  Protecting the project does not need recording to work; the coupling is the
  present design, not a requirement.
- **What the person does instead:** resolve the store's cause the App shows
  (choose a usable records location, let the registry be read whole, or confirm
  the project's link), then start the conversation; or work in a conversation
  without a project meanwhile.
- **What would remove it:** the project's activity taken without requiring its
  records to be writable, with each record write refused visibly as now, so
  that conversation works and recording does not, and the App says so. That
  change is planned as its own unit.
- **Basis:** DEL-04-03 (records store, REQ-007), DEL-01-01 and DEL-01-04
  (starting Codex for a project); the owner's test that a person should not
  meet restriction that is not needed.

### LIM-029: Codex makes connections when it starts, and connects to OpenAI when the App reads your sign-in

- **Id:** LIM-029
- **Exit criteria:** 6
- **What is unavailable:** an App control over the connections the App's Codex
  makes. Codex makes them when it starts, and when the App asks it whether
  you're signed in. This release offers no App control for them.
- **What was observed:** with every connection refused, at Codex 0.167.0, the App's checks saw Codex try these hosts:
  - when it starts, before the App asks it anything, with a ChatGPT sign-in
    kept: chatgpt.com and auth.openai.com;
  - when it starts, with no sign-in kept: chatgpt.com, github.com and
    api.github.com;
  - when the App reads whether you're signed in, with a ChatGPT sign-in kept:
    chatgpt.com, and auth.openai.com. Codex's source says this read checks
    with OpenAI which ChatGPT workspace the kept sign-in belongs to and, if
    OpenAI refuses it as unauthorized, may try to renew the sign-in;
  - when the App reads whether you're signed in, with no sign-in kept: none;
  - when the App reads the list of models: none during the read;
  - when the App reads the list of your past conversations: none during the
    read.

  These are the hosts the checks saw Codex try when every connection was
  refused. Once a connection succeeds, Codex may connect to others.

  The maintained rows assert chatgpt.com at startup in both homes and during
  the kept-sign-in account read. The other hosts named above were observed
  in the Codex 0.167.0 runs; the rows do not assert that each appears.
- **Why:** the App reads whether you're signed in when Codex is ready and
  after you sign in, because without that reading you cannot see whether you
  are signed in, and so whether a message can be sent. The connections at
  start come before the App can show anything.
- **What the person does instead:** nothing is needed to use the App. With a
  ChatGPT sign-in kept and no network access, Codex starts but the read may
  not establish whether you're signed in; in that case the App says "It
  didn't say whether you're signed in." and offers to check again. If Codex
  reports no account, the App says you're not signed in.
- **Basis:** DEL-01-05 (REQ-001). The fixture rows
  `AccountRead.test_with_no_sign_in_the_account_read_contacts_nothing_and_reports_no_account`
  and
  `AccountRead.test_with_an_invented_sign_in_the_account_read_contacts_the_account_server_and_fails_when_refused`
  (`app/supplier_checks/level`). They run the pinned Codex in a home of their
  own: one with no sign-in, and one holding an invented sign-in that no server
  issued. Every connection goes to a loopback listener that refuses it and
  keeps only the host and port. The purpose of the sign-in read is read from
  Codex's source at tag rust-v0.167.0, not shown:
  `codex-rs/app-server/src/request_processors/account_processor/workspace_routing.rs`
  lines 258-293 (`get_account`) and 295-430 (`read_account`, which calls
  `get_accounts_check` on the ChatGPT base address and, if it is refused as
  unauthorized, tries to renew the sign-in).
