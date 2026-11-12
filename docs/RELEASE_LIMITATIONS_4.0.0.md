---
name: chirality-app-release-limitations-4-0-0
description: List the limitations the App 4.0.0 release carries, each with its reason.
metadata:
  kind: instruction
  surface: requirements
---
# Chirality App 4.0.0 release limitations

Companion to [`RELEASE_TARGET_4.0.0.md`](RELEASE_TARGET_4.0.0.md), for its
exit criterion 11. This is the single list of what the release does not do
that a person could expect of it. Agent 0 keeps it, with a reason for each
entry. The owner sees the whole list with the request for the verdict
(criterion 12), and what a person receives with the package is written from
it (DEL-01-06).

An entry states a limitation and its reason. It holds no status: an entry that
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
- **Exit criteria:** 7
- **What is unavailable:** once a person has protected registered workflows
  with their keychain, the key that seals registrations cannot be replaced
  with a new one.
- **Why:** the owner chose to leave rotation unavailable for 4.0.0.
- **What the person does instead:** no alternative is offered in 4.0.0.
- **Basis:** DEL-01-04 (keychain protection); DEL-01-06 REQ-007 (the release
  says so).
