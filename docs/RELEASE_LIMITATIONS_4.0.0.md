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

### LIM-013: "Decided" rests on the App's records folder, not on a verified capture

- **Id:** LIM-013
- **Exit criteria:** 5, 15
- **What is unavailable:** a check that a decision the App shows as decided
  was captured at its own act control. A decision package reads as decided,
  and a work item waiting on it as no longer waiting, from an act record held
  in this installation's records store outside the parts its import account
  names. The App does not verify that a record in that folder was captured at
  its act control. So a record file placed in the App's data folder by another
  program is not distinguished from the person's own recorded act. An act
  record in the project folder, in an imported package, or in a
  legacy-imported copy that the import account names is shown as a claim and
  decides nothing.
- **Why:** the decision view reads act records without resolving their
  capture evidence under the capture seal, which exists only in a signed App
  with its keychain.
- **What the person does instead:** the App's data folder is what the word
  "decided" rests on, and a record placed there by anything other than the
  App is not told apart from the App's own. Where a decision matters, decide
  it at the App's act control and check that the row names the actor, the
  alternative chosen and the capture time expected.
- **Basis:** DEL-06-02 (Decision row; AC-004); DEL-04-03 (Record authority;
  REQ-010); DEL-01-04 (the act control and its capture seal).
