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

### LIM-024: The App does not show which plugins act in its Codex

- **Id:** LIM-024
- **Exit criteria:** 6
- **What is unavailable:** a view of which plugins are installed in the App's
  Codex, which hooks they bring, and when a hook decided a request. Plugins in
  the App's Codex are as the Codex settings the App uses have them: your own
  Codex settings, where the App's Codex uses them, or the App's own new
  settings, where you chose new settings at setup. With plugins on, a plugin
  you have installed can bring hooks, and such a hook can approve a request
  with no card, or refuse it. The level you set describes commands and file
  changes, not what a plugin's hooks decide.
- **Start-up connections:** while plugins are on, the App's Codex makes these
  connections when it starts, without sign-in:
  - github.com, to fetch the curated list of plugins;
  - api.github.com instead, if that fails;
  - chatgpt.com, for the curated list if both of those fail and no copy is
    kept yet, and for the list of featured plugins.
- **Why:** listing plugins and their hooks needs reads of Codex that the App
  has not shown to stay on this Mac at the pinned Codex version.
- **What the person does instead:** see and manage your plugins in your own
  Codex. To turn plugins off in the App's Codex, set `plugins = false` under
  `[features]` in the Codex settings the App uses. Where the App's Codex uses
  your own Codex settings, this turns them off in your own Codex too. If you
  turn plugins off and a plugin's hook was what stopped a command for you,
  choose a level in the App that asks before commands. A setting made outside
  the App, by whoever manages your Mac or account, the App does not change.
- **Basis:** DEL-01-05 (REQ-010). A fixture shows the start of the curated
  sync and the featured-list request with plugins on, and neither with
  `plugins = false` in the home's own settings (`app/supplier_checks/level`).
  The rest is read from Codex's source at tag rust-v0.167.0, commit
  086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a, and not shown:
  - the addresses and their order: `codex-rs/core-plugins/src/startup_sync.rs`
    lines 23-30 and 96-167;
  - the sync starts only with plugins on: `codex-rs/core-plugins/src/manager.rs`
    lines 769-790;
  - the featured list: `codex-rs/core-plugins/src/remote_legacy.rs` lines
    125-149, with the default address in
    `codex-rs/model-provider/src/chatgpt_base_url.rs` line 6;
  - plugins bring hooks: `codex-rs/hooks/src/engine/discovery.rs` lines 280-346;
  - a hook approves with no card, or refuses: `codex-rs/core/src/tools/approvals.rs`
    lines 594-621.

  Not established at the pinned Codex version: whether a plugin can add
  command rules, and whether listing installed plugins makes a network request
  when signed in.

### LIM-025: The App does not show which connected apps act in its Codex

- **Id:** LIM-025
- **Exit criteria:** 6
- **What is unavailable:** a view of which apps connected to your ChatGPT
  account are in the App's Codex, and which of their tools run without a card.
  Connected apps in the App's Codex are as the Codex settings the App uses
  have them: your own Codex settings, where the App's Codex uses them, or the
  App's own new settings, where you chose new settings at setup. Once you are
  signed in with your ChatGPT account, a connected app's tools are given to
  the App's Codex. Unless your settings set how a tool is approved, a tool the
  app marks read-only runs without a card. The level you set describes
  commands and file changes, not these tools.
- **Why:** at the pinned Codex version, the requests Codex offers for listing
  connected apps are marked experimental. The App has not shown that the
  read-only marks they report are the ones Codex uses to decide whether to
  ask.
- **What the person does instead:** manage your connected apps in ChatGPT. To
  turn them off in the App's Codex, set `apps = false` under `[features]` in
  the Codex settings the App uses. Where the App's Codex uses your own Codex
  settings, this turns them off in your own Codex too. An older
  `connectors = true` in the same settings turns them back on. A setting made
  outside the App, by whoever manages your Mac or account, the App does not
  change.
- **Basis:** DEL-01-05 (REQ-010). A fixture shows that `connectors = true`
  turns apps back on over `apps = false` (`app/supplier_checks/level`). The
  rest is read from Codex's source at tag rust-v0.167.0, commit
  086ccc833bc9cf01024ad2dd6af7dbd421b6bf9a, and not shown, because connected
  apps start only for a signed-in account:
  - the tools need apps on and a sign-in through Codex's backend:
    `codex-rs/codex-mcp/src/mcp/mod.rs` lines 358-360;
  - the automatic approval mode is the default:
    `codex-rs/connectors/src/app_tool_policy.rs` lines 233-270;
  - in it, a tool marked read-only needs no approval:
    `codex-rs/core/src/mcp_tool_call.rs` lines 2595-2626.
