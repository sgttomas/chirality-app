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
- **Why:** it is omitted from this increment; the access modes are the
  ChatGPT account and a local model server.
- **What the person does instead:** sign in with a ChatGPT account, or
  configure a local model server.
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

### LIM-011: A local model server is set up in the App, on the same machine, with a key

- **Id:** LIM-011
- **Exit criteria:** 6
- **What is unavailable:** a conversation on a local provider defined in the
  person's own Codex settings; a conversation with a model server on another
  machine; and a local model server that requires no key. Preparing or
  starting the local connection, and entering its key, are refused while
  a system Codex configuration file exists (`/etc/codex/config.toml`,
  `/etc/codex/managed_config.toml` or `/etc/codex/requirements.toml`) or a
  managed Codex preference is set, whatever they contain. Removing or
  renaming such a file is the person's or their administrator's own act; the
  App does not ask for it. In the home that
  uses the ChatGPT account, the App starts Codex on the built-in OpenAI
  provider whatever default provider the person's Codex settings name; a
  conversation saved earlier on another provider can be opened there and
  cannot run a message. Where a managed Codex requirement names another
  provider, that home's Codex does not report the built-in one, and the App
  starts no ChatGPT account conversation and says so. In the local model home, Codex's plugin traffic is
  always off, whatever the person's Codex plugin setting. Changing the local
  server's address removes the saved key, except when restoring the address
  the App recorded for the saved key; that restoration keeps the key and does
  not require a prepared connection. An existing conversation continues
  only when the model name now set matches the model Codex recorded for it,
  and then uses the server at the address now set; otherwise it cannot
  continue under the current settings. In a session already using the local
  home, a change to the local model settings cannot be used until the App is
  quit and reopened; the local connection is unavailable meanwhile. Changing
  an existing server address requires the local connection to be prepared
  first so Codex can sign out, even if no key was saved. After key entry has
  been begun in a Codex session, including an entry that was cancelled or
  failed, the address cannot be changed until Codex is restarted for the
  local model home. After the App has ended unexpectedly,
  the local connection is refused while the earlier Codex process for the
  local model home, or a program it started, still holds the App's lock for
  that home; that process normally ends by itself within a minute, and
  quitting and reopening the App does not end it. If an otherwise
  valid local-home configuration is changed outside the App to name an
  address different from the one recorded for its saved key, preparation is
  refused and the App offers to restore the recorded address. A local-home
  configuration that is no longer in the App's own form cannot be read or
  repaired from the App. If the App's record of the address a saved key was
  entered for is removed outside the App, the App refuses preparation and
  further requests and replies that could send the key in that home, and
  offers no repair; this does not stop work already running in Codex, and a
  turn that was waiting for an answer stays waiting until it is interrupted. The protection of a saved key rests on the
  files of the local model home being changed only by the App and its Codex:
  it does not survive their removal or replacement from outside while an
  earlier Codex process of that home is still running.
- **Why:** at the selected supplier version, Codex runs conversations only on
  the provider its process started with, so account and local access use
  separate homes; the App does not reconfigure a prepared local connection in
  place. The release requires a local credential, limits the server to this
  machine to keep the key and conversation content from travelling off it
  without the protections that requires, does not prepare or start the local
  home under a system or managed Codex configuration because the App cannot
  establish what such a layer would do to that home's settings, and requires a prepared local
  connection to confirm removal of the saved key before an address change so
  that key cannot be sent to another server. For the same reason it starts
  Codex for the local model home only when it can take that home's lock,
  which an earlier Codex process and any program that inherited it hold
  until they let go of it or end, and does not move the address under a key
  entry that Codex may still be saving.
- **What the person does instead:** set the local server's address and model
  name in the App's local model settings and run the model server on the
  same machine with a key. To change the address, prepare the local
  connection (and if key entry was begun in this Codex session, restart Codex
  for the local model home first), save the new address, quit and reopen the
  App, prepare the connection again and enter the key again. Where the App
  offers to restore the address a saved key was entered for, use that; it
  keeps the key. To use a different model name,
  save it, quit and reopen the App, and start a new conversation. If the
  refusal that the App's lock for the local model home is held continues for
  more than a few minutes, a Codex process started earlier for that home
  (named `codex`), a program it started, or another copy of the App still
  holds it; the App cannot tell which program it is. End that program in
  Activity Monitor, or log out of the Mac and back in.
- **Basis:** DEL-01-05 (REQ-003, REQ-010, AC-003, AC-005, AC-008, AC-011);
  PRD V4-APP-02.
