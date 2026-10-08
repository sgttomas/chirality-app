# Offline static scanner contribution

Basis: `15f5c51818`; new branch `codex/app-v4-static-scanner`, preserving previous
role-work refs. TASK `/root/distribution_integration_manager/production_roles`,
native descendant of WORKING_ITEMS `/root/distribution_integration_manager`.
No delegation. Supplied brief and parent target disposition remain in native
harness history. New files only; existing scan/equal, Host, selection, semantics,
store, lib and Cargo manifest unchanged.

## CLI handshake

Unix scanner example `app/src-tauri/examples/distribution-static.rs`:

```sh
cargo build --offline --locked --example distribution-static
/path/to/target/debug/examples/distribution-static scan /absolute/physical/tree
/path/to/target/debug/examples/distribution-static compare expected.json actual.json
```

`scan` emits the existing public `distribution_preflight::scan` complete Inventory
JSON plus newline. Fields: method, algorithm, entries, manifest_sha256. Entries
include root `.` and directories with path/kind/mode; regular files additionally
have size/sha256. Existing scan rejects symlinks, hard-linked files, unsupported
types and observed changes. No JSON normalization or alternative tree algorithm.

`compare` deserializes both complete Inventory objects and calls unchanged public
`equal`. Output is `{"equal":true}` or `{"equal":false}` plus newline, exit0 for
either completed comparison. Read, parse, usage and scan errors are stderr and
nonzero, with no inventory stdout. This is equality, not schema/trust/authority
validation. Python packaging owner retains canonical contract validation and
source/selection responsibility. Manifest hash alone omits modes/types; compare
checks the complete entries. Neither command launches another process or mutates
the filesystem. Ordinary OS read/atime behavior is not suppressed.

Parent approved example target after offline Cargo metadata showed a src/bin
scanner would produce two binaries with no default-run. Final metadata has only
`chirality-app-v4` as bin and `distribution-static` as example; no Cargo edit.

## Actual checks

Prepared offline Cargo cache and isolated temporary target; no download, supplier,
probe, app/native window, credentials, Selected or Store construction.

- `cargo build --offline --locked --example distribution-static`: passed.
- Explicit scanner subprocess tests:

```sh
DISTRIBUTION_STATIC_BIN=/path/to/target/debug/examples/distribution-static \
  cargo test --offline --locked --test distribution_static_cli -- --ignored
```

Result: 4 passed, 0 failed, 0 ignored when explicitly invoked.

The four focused tests run the actual built executable against invented trees:
stable complete JSON/read-only content; bytes, modes and file-to-directory changes;
symlink/hardlink/wrong-root/argument refusals; equal, unequal, duplicate-path and
malformed-JSON compare cases. These cases are explicitly ignored by the ordinary
suite because an external scanner path must be intentionally supplied; no fallback
or guessed executable. Initial compile found unsupported uuid v4 constructor;
fixture now uses the existing opaque ID helper without a dependency change.
Existing unrelated unused/dead-code warnings remain.

Configured Ryan C Tufts <ryan@chirality.ai> and absent email environment overrides
are rechecked before commit; official staged private-term validator before commit.
Independent review and integration remain with parent; no push or release claimed.

## Consulted instruction and source identities

Read Root/TASK, project entry and applicable work graph; manual entry/Field Book
and change skill previously read in this continuing TASK session. No broader role
instructions activated. Current source hashes:

- AGENTS.md: `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977`
- agents/AGENT_TASK.md: `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7`
- .agents/skills/chirality-change/SKILL.md: `1a2b056263ec77e4104efdf99afe3fe76dda792334a243fb2f21c60bc9c81450`
- projects/chirality-app-v4/loop/LOOP_INIT.md: `c2e88f81439ed03578fee13fd7563082fefdfe11096d9134a59531eba3b985bd`
- app/src-tauri/src/distribution_preflight.rs: `b98786879402fc26c4c9d2beca558d71ef1fba5b54693d5905fae2d0d8e52411`

## Compare reader repair

Parent review identified that the original caller-path std::fs::read could block
on a FIFO and follow a leaf symlink. The example-only reader now checks regular
non-link metadata, opens with O_NOFOLLOW/O_NONBLOCK/O_CLOEXEC, checks the descriptor
is the same regular file, bounds reads to 64 MiB and refuses observed size/time
change during read. This remains equality input handling, not canonical inventory
semantics or an authority/trust admission. Existing library scan/equal unchanged.

Rebuilt the actual example offline and ran all explicit scanner tests: 5 passed,
0 failed, 0 ignored. Added negative cases for FIFO, leaf symlink, directory and
oversized sparse file in both expected/actual positions, each with a 3-second
child-process timeout and cleanup; all refused without timeout or stdout JSON.
Prior four scanner/equality tests passed unchanged. No supplier process or launch.

Repaired source SHA-256:
`3bc4ed010a6f322a88b902bcfc90cc705cbe1cb79b1678bcb717ede376537a71`.
Locally rebuilt example SHA-256:
`f8bb51b8894a8e913933ebd2a54f3ce0af1cbd38df65fad898a16b81398e68d7`.
