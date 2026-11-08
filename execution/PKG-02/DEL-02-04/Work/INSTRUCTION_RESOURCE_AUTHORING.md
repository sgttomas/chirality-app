# App instruction documents and resource derivation — v1

The App role-guidance owner maintains the product instruction documents in
[`instructions-v1/`](instructions-v1/), as part of DEL-02-04's guidance and
source-identity outputs. The owner directed that the packaged instructions be
their own versioned documents under `Work/`, matching SWBPIPE's authoring
locality conceptually. This implementation is self-contained in App and reads
no sibling repository. Operational Library instructions remain separate.

## Source and output

The named source set is `instructions-v1`, with revisions identified by Git
and the exact per-file identities in
[`INSTRUCTION_RESOURCE_DERIVATION.json`](INSTRUCTION_RESOURCE_DERIVATION.json).
Its eight files were initially retained byte-for-byte and mode-for-mode from
App `f10e5c305f58e1c7abcf462f9c3518e35c7b6eec`'s packaged instruction tree:
product `AGENTS.md`, four `agents/AGENT_<ROLE>.md` documents, `roles.json`,
`ROLE_SET_SOURCE_BINDING.json` and `SOURCE_MAP.json`.

The generator copies the Work source bytes without text normalization or
composition into `app/src-tauri/resources/instructions/`. Files remain 0644;
the resource root and `agents/` remain 0755. No generated banner or extra file
is inserted into that product tree. The separate derivation manifest binds
each generated relative path to its Work source hash, length and mode.

From the App repository root, after an authorized source edit:

```sh
python3 -m tools.instruction_resources
python3 -m tools.instruction_resources --check
python3 -m unittest tools.test_instruction_resources
```

Edit the maintained Work documents, then regenerate and review their output
and derivation together. Do not edit the packaged copy directly. Generation
has a closed file set; it refuses unexpected entries, symbolic links,
hard-linked files, special files and wrong modes rather than deleting or
adopting them. The check is read-only and rejects stale resource bytes,
file sets, modes or derivation. Generation is deterministic and needs only
Python's standard library and this source export, without Git execution,
Library access, credentials, downloads or an App build. The repository CI
entry checks freshness and runs its focused regressions.

## Historical identities and retained meaning

`SOURCE_MAP.json` is an earlier authorship/source account with its original
pending-review and qualification limits. `ROLE_SET_SOURCE_BINDING.json`
retains the current four-role product basis
`89acac6a3983c605820496d0d121c73bb2297706`, selected documentary passages and
guidance identities. Neither is rewritten as a new authoring, qualification,
supply or adoption claim. Their prior App authorship remains as recorded;
the new derivation account identifies the maintenance locality of the same
bytes. The operational Library's fifth role is not a product migration.

The runtime continues to consume the same generated paths and bytes. Role
names, default flags, delegation semantics, composition, editable-copy
seeding, runtime policy and consumers are unchanged. A future substantive
guidance change still needs its applicable source/binding reconciliation;
freshness alone is not evidence that the content satisfies those contracts.

The SoW addition is a local production mapping for existing OUT-001/OUT-002
and REQ-004/REQ-005. It leaves the selected REQ-001–REQ-006 passages unchanged;
the retained documentary binding is checked without repinning it. Scope,
acceptance criteria, receiving owners and actual supplier/adoption evidence
remain as declared.

## OI-018 and session entry

This owner choice selects App-local authoring and derivation locality only.
It does not resolve portable instruction distribution, host/shared
allocation, adoption, retirement or precedence questions. OI-018's broader
owners and open host-distribution condition remain. No Library or SWBPIPE
implementation or packaging dependency is introduced.

Separately, `init/init-prompt.md` now ends its substantive instructions with
“Orient. Briefly report your understanding of the current basis and
boundaries. Await the owner's separate steering.” The following
initialization self-talk was removed as directed. The rest of that prompt
and `init/README.md` are unchanged; no YAML header is added. This session-entry
edit is not part of the packaged product instruction set.

## Verification and limits

The focused stdlib tests cover deterministic generation, source/manifest
freshness, exact bytes/modes, a source export without a sibling Library,
contained writes, refused aliases/special entries, the unchanged eight-file
payload and retained selected-passage binding. The existing packaged
four-role consumer check remains applicable. No product build, supplier,
model, native App, authentication, instruction-supply behavior or adoption
is established by these source checks.
