# C3-P bounded route-account persistence — CRP-R2 repair

TASK `/root/group_c_successor/route_persistence` returns the repaired backend
under WORKING_ITEMS `/root/group_c_successor`. Exact source/output hashes and
historical observations are in `C3_PERSISTENCE_BASIS.json`. This commit is an
author candidate; independent backcheck and manager integration remain required.
No push or merge was performed by this child.

## Selected source and original finding

The original candidate `e660d7431de637da7e8dbe9d9bddc0c6847838c8` implemented
CRP-v0.2 and passed 25 connector checks. Independent review reproduced two
blocking failures on its integrated equivalent: after the writer's temporary
name was replaced, cleanup deleted the foreign replacement and publication
linked foreign bytes before detecting a final mismatch. Those original passes
did not cover or disprove the defect. The original candidate and its evidence
remain in Git; no earlier result is recast as a safety pass.

An intermediate identity-check repair passed 27 checks but retained a final
check-to-unlink race. It was not claimed READY or committed. HELP_HUMAN's
relayed technical selection, source owner, independent source review and fleet
concurrence produced the now-adopted CRP-v0.3:

- Source `3d9a91a98872fda1837aad1a91e710345c614f28`, file
  `Design/CONNECTOR_ROUTE_PLACEMENT_v0.3.md`, SHA-256
  `e52f5ed0b9c3be99a50a834101470ecfc67078aab0e5dc90e9bc201706a6598e`.
- Independent source READY `0d1b8c62bb`; affected concurrence `873f23b906`;
  technical adoption `0a77c18972`.

These exact successor records were read from Git. This implementation return
contains no Design/schema-semantic or manager-graph changes. The successor
consciously changes the late-source-substitution criterion; the old stronger
promise is not represented as having been implemented.

## Current implementation

The public Rust library accepts schema-valid caller accounts in format 0.1 or
0.2 through an explicit opened project. Exact maintained route/standing schema
resources compile with retrieval disabled and are byte-compared to Design.
The caller's content, recorder/time provenance and duty standing survive
serialization. Shape validity establishes no source truth/custody, semantic
reference truth, actual performance or authority.

UUID-v4 filenames are independent of account identities. Descendants of
`.chirality/records/connectors/route-accounts/` are opened no-follow relative to
retained handles. Root/ancestor identities are compared before writing and
after publication. The private exclusively created temporary is flushed and
synced (including macOS `F_FULLFSYNC`); immediately before publication its
name must still identify the original regular-file inode and exact intended
hash. Observed substitution refuses publication.

Publication uses macOS `renameatx_np(RENAME_EXCL)` or Linux
`renameat2(RENAME_NOREPLACE)`, with no replacing-rename or link/unlink fallback.
Ordinary success consumes the temporary name atomically and preserves its inode.
The directory sync and final regular-file identity/hash/account/version checks
must pass before a binding returns. **There is no automatic pathname unlink
on any path.** Definite failures retain the known temporary name for explicit
reconciliation. Collision preserves the destination. Unsupported capability
refuses; ambiguous syscall outcomes remain uncertain.

Exclusive rename still resolves a mutable source name. A replacement after the
last check can move a foreign entry to the final name, disrupting its former
name. Postchecks reject that foreign inode even if bytes are identical. Error
attempts retain original temp/final paths, intended account/version/hash,
root/directory/file identities and explicit observed/absent/unreadable final
observations. The store preserves entries and never rolls back, relocates or
retries. Observed hash/type details describe only the safely read buffer or
metadata, not a stable snapshot. This is the selected CRP-R2 residual, not an
excluded race.

Cold discovery retains distinct invalid-name, malformed, unknown-version,
symlink/nonregular/hard-link, temporary, duplicate and unreadable issues.
Duplicate identities retain every path with no winner. Missing and incomplete
discovery remain distinct. Held-reference resolution checks path, account,
version, hash and filesystem identity; reconciliation rechecks the intended
binding without searching elsewhere. An explicit legacy relative reference
uses the same checks, without a crawl. A relocated whole project can preserve
identities; copying bytes into a different directory does not silently adopt
new identities or transfer authority.

An unbound discovered account is inspected claimed content, **not evidence
that this writer successfully committed it**. A foreign schema-valid file can
be discovered after the late race while reconciliation of the original attempt
still refuses. This is a backend seam only: no Tauri command, UI, actual source
reconstruction, provider joining or receiving-owner adoption is supplied.

## Executed checks

One private APFS copy-on-write target clone from inactive C1 artifacts was
reused; actual candidate files were rebuilt and executed. The approved Group A
Cargo home, `CARGO_NET_OFFLINE=true` and `CHIRALITY_SKIP_CODEX=1` were used.
No download, supplier/native App launch or credentials. Rust/Cargo 1.92.0;
macOS 26.6.2 arm64. From `app/src-tauri`:

```text
cargo test --offline --locked connector_ --lib -- --nocapture
31 passed; 0 failed; 0 ignored; 423 filtered out
```

24 route-store checks and 7 existing connector-standing checks passed. Two
nested processes additionally exited deliberately with code 73 at interruption
boundaries; they are not extra top-level passes or supplier executions.

| Requirement | Actual observation |
|---|---|
| Exact versions and CI-29 | Both versions round-trip with distinct supplied IDs; unsupported versions, invalid source-free claims and performed-duty shapes refuse. Complete evidence-field shape is still only a claim. |
| Restart/move/root alias | Cold content and bytes match; relocated project resolves the same bound identities; stale root refuses; selected root alias displays its resolved path. |
| Identity/path containment | IDs never become filenames; invalid account creates no store. Escape/non-normal references refuse. Every symlink/non-directory ancestor refuses. |
| No-replace and concurrency | Repeated collision preserves original bytes and retains visible temp entries. Eight distinct writers succeed; eight same-target contenders yield one success/seven collisions with seven recovery temporaries. |
| Cold conflicts and permission failure | Malformed/unknown/duplicate/link/FIFO/unreadable entries remain distinct. Read-only directory refuses; an unreadable directory is incomplete, not empty. Retained temporaries never become accounts. |
| CRP-R1 root/ancestor race | Moving/replacing each opened ancestor or root never directs publication into replacement. Mismatch is uncertain. Restoring exact identities permits explicit read-only reconciliation, with no retry. |
| Transient directory movement | Test observes publication outside current project tree followed by restore-before-postcheck success; this proves only the bounded observed comparison. A later mismatch refuses reliance. |
| Original temp substitution finding | After temporary sync, different or identical foreign bytes/new inode refuse before publication; injected failure leaves foreign replacement and moved-aside intended bytes intact. Observed symlink/directory/disappearance also refuses with no cleanup. |
| CRP-R2 after-final-check residual | Foreign account, same-byte foreign inode, symlink and directory are injected immediately after final precheck. Exclusive rename moves foreign entry; postcheck returns uncertainty; original moved-aside content and foreign content remain; no rollback/retry occurs. Existing-target variants preserve both destination and substituted source. |
| No late cleanup | Success consumes temp; a foreign entry recreated at the old name followed by injected failure remains untouched. No unlink helper/syscall remains in production. |
| Unsupported and ambiguous outcome | Real exclusive-rename syscall with an injected unsupported flag returns refusal with source retained and no fallback. Injected EIO yields uncertainty, explicit absent-final observation, and retained temp. This EIO is not an actual storage-device failure. |
| Interruption and readback | Before-publication abrupt exit leaves visible temp; after-exclusive-rename exit leaves no temp alias and a cold-inspectable final file, without proving writer completion. Content/inode tampering fails intended reference reconciliation. |
| Legacy | Only explicitly supplied legacy binding resolves; no broad discovery/migration. |

Test expectation changes follow the reviewed successor: collision/error
leftovers are now required, and successful exclusive rename has no temporary
hard-link alias. Original safety assertions (no deletion of observed foreign
replacement; observed precheck substitution refuses) are retained. Late foreign
movement is asserted honestly, not hidden by a weakened assertion of success.

The installed SDK rename manual/headers and approved libc declarations were
consulted. A separate scratch probe observed ordinary inode-preserving rename,
EEXIST preserving both names and late source substitution moving foreign bytes.
The maintained tests above now exercise those behaviors through the actual
product seam, plus its error/return handling.

`rustfmt` and `git diff --check` pass. Staged private-term screening with
`--from-host` precedes the repair commit; exact result accompanies the return.

## Remaining limits

macOS real-file behavior is tested. Linux is implemented but not compiled/run
here; other platforms refuse opening. Successful sync calls are observed,
not physical power-loss/hardware qualification. Actual device fsync failure
and induced mid-stream readdir failure were not witnessed. The invalid-flag
negative exercises a real syscall refusal, not a separately mounted filesystem
without exclusive-rename support.

Pre/post checks do not exclude transient directory moves or source-name
replacement after the final check. Cold reads are not filesystem snapshots or
proof of past successful writer operations. Broader source reconstruction,
semantic/custody verification, native UI, provider acts and consumer adoption
remain outside this contribution. SEAL-2 stays held. No instruction, graph,
frontend, other runtime module, Design semantics, MEMORY, credentials, sign-in,
provider/person act, qualification, acceptance, release or 90% claim changed.
