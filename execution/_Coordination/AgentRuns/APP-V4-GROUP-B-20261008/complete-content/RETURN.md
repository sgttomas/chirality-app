# B2 complete-content development candidate

Produced an actual unsigned Tauri App bundle from source
f79317be861bb63553512de3197b22d556268198 plus the maintained unsigned-overlay
patch in SOURCE.patch. BUILD_INPUTS.json binds the full selected App tree and
confirms every input still equals the isolated scratch copy after build.
The branch is codex/app-v4-b2-complete-content; no push performed.

## Physical result

All P0–P4 places are physically present. The final bundle has 56 regular files,
31 Mach-O files, and PKG file manifest
`cd0e8f7216d6c85b1b1cee96300e3b1f4aeaea15bbc6185214345290bdb83c15`.
BUNDLE_INVENTORY.json records every entry's hash, size, mode and link target
where applicable, plus read-only Mach-O signature metadata.

P1 is the complete approved cached 0.160.0 vendor tree. P1_COMPARISON.json proves
all 42 supplier files and every directory/link/mode equal after actual bundling.
P2 maps the full received production_workflows tree to Resources/workflows,
including MANIFEST.json and its exact candidate workflow. P3 maps the complete
instructions tree to Resources/instructions, including roles.json,
ROLE_SET_SOURCE_BINDING.json, AGENTS.md and all four role files.
P2_COMPARISON.json and P3_COMPARISON.json bind all source and final entries,
with zero differences, missing or extra entries. This is physical source equality,
not a new source-owner acceptance or runnable workflow registration.

## Operations and verification

The existing prepared npm dependencies and approved Cargo registry cache were
reused without downloads. Cargo home, target, scratch HOME and App build copy
were newly isolated; no shared target was used. command.json retains the exact
arguments and allowlisted environment using path-neutral placeholders.
The supplier overlay template retains the deliberate P1 mapping; actual input
hashes are in P1_COMPARISON.json. No Apple/Tauri signing or credential variables
were inherited. The offline locked build used explicit --features custom-protocol
and --no-sign in one build-and-bundle operation; no second bundling was needed.
COMPILED_FEATURES.json records the emitted library build fingerprint and the
actual custom-protocol feature. The source's production P2/P3 consumers were
compiled rather than relying on development fallback.

TypeScript/Vite and Rust/Tauri build passed, exit 0; build.log preserves the
path-neutral output, including 37 compiler warnings and the signing-skip line.
The received source already has independent component validation; this mapping
change was checked against the actual bundled resources and full inputs instead
of adding a test duplicating the configuration. No native or supplier binary was
executed. Read-only codesign display reports incidental linker-signed ad-hoc P0,
no team, no sealed resources, and unbound Info.plist; it is unqualified compiler
output. No signing, notarisation, stapling, install or native launch occurred.

P4 matches version 0.0.0, dev.chirality.app-v4.skeleton and proposed minimum
macOS 15.0, with no microphone usage string. Info.plist.json preserves it.
TOOL_IDENTITIES.json binds the tools by logical name and digest; installed CLI
bundle help confirmed --no-sign and --features support.

## Limits and return

Standing is complete-content physical development candidate only.
`package_complete:false`, `qualified:false`. Candidate LS-5/LS-8 runnable
registration remains refused; production source selection is not permission to
run the workflow. No S3 qualified distribution reference or H3B actual runtime
witness is supplied. Cached 0.160.0 does not select the qualification pin.
FP-1(a)'s content comparison operation passed for this development artifact;
FP-1(b), FP-2/W-4, FP-3/4/5, SIGN-1, M2/M3, SEAL-2, owner acts and release remain
unperformed or unsupplied. Production identity/minimum OS decisions remain open.
No Design, source lock, default config, central Rust/UI, work graph or MEMORY
was changed. The manager owns separate coordination evidence. Independent review
of the sealed candidate follows; this return does not impersonate that review.

TASK /root/group_b_successor/complete_content_build executed under
WORKING_ITEMS /root/group_b_successor using a native descendant; no delegation.
READ_BASIS.json binds supplied and consulted origins. Managed worktree and
sandbox permissions enforced the actual execution boundary. Owner Git identity
is Ryan C Tufts <ryan@chirality.ai>. Staged private-term validation is run before
committing with local machine names supplied through a private environment;
names are never printed or recorded. PR/integration belongs to the manager.
