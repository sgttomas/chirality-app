# Compiled synthetic startup observation

Basis `8e120c8c9f`, branch `codex/app-v4-compiled-selection`. TASK native descendant
`/root/distribution_integration_manager/production_roles` under WORKING_ITEMS
`/root/distribution_integration_manager`; no delegation. Actual brief and parent
dispositions are retained in native harness history. Root/TASK, project entry and
change conventions read in this continuing session; no wider role adopted.

The default-off `synthetic-distribution-anchor` feature is independent of
custom-protocol and distribution-successor. Every new include_bytes is gated by
both that feature and debug_assertions. Enabling it without debug assertions is
a compile error. No ordinary feature-off helper resource resolution or reads.
This no-I/O claim applies to this helper only, not the rest of App startup.

Actual App setup calls observe_startup once with a lazy native resource_dir
closure. The helper uses only its fixed distribution-development-reference child.
AppState retains its JSON result and host_status clones it without rechecking.
Enabled results always say development-unverifiable, observedAt app-startup,
currentTrust false, with matched or refused outcome. Disabled builds say disabled.
No command takes a resource path/hash and no result creates a Selected, Store,
Host verification or production availability. This is an observation at startup,
not a trust decision and not proof of current unchanged files.

## Exact resource layout

Parent approved these destination aliases to preserve existing attestation path
relations, without editing existing synthetic source bytes:

| Native destination | Source under resources/ |
|---|---|
| distribution-development-reference/build-selection.s2.json | distribution-development-reference/build-selection.s2.json |
| distribution-development-reference/expected.json | distribution-successor/synthetic-expected.json |
| distribution-development-reference/attestation.json | distribution-successor/synthetic-attestation.json |
| distribution-development-reference/synthetic-evidence.json | distribution-successor/synthetic-evidence.json |

The unchanged public preflight scan reads this closed four-file set with its
existing no-follow/stability rules. Exactly root plus four regular files must be
present, each size/hash equal to the compiled byte source. Extra, missing, linked,
type-substituted or mutually consistent replacement documents refuse. Modes are
observed and returned only: no mode acceptance/integrity claim is made. Runtime
does not add a general resolver or duplicate Selected semantics. Tests validate
the fixed expected/attestation schemas, selector identity, author/pin and every
declared evidence relation. The synthetic evidence remains synthetic.

Packaging changes belong to the packaging owner. Existing Host/preflight/selection/
semantics/store/build.rs/pins and existing resource bytes are unchanged.

## Source bindings

- `AGENTS.md`: `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977`
- `agents/AGENT_TASK.md`: `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7`
- `.agents/skills/chirality-change/SKILL.md`: `1a2b056263ec77e4104efdf99afe3fe76dda792334a243fb2f21c60bc9c81450`
- `projects/chirality-app-v4/loop/LOOP_INIT.md`: `c2e88f81439ed03578fee13fd7563082fefdfe11096d9134a59531eba3b985bd`
- `projects/chirality-app-v4/app/src-tauri/src/distribution_preflight.rs`: `b98786879402fc26c4c9d2beca558d71ef1fba5b54693d5905fae2d0d8e52411`
- `projects/chirality-app-v4/app/src-tauri/resources/distribution-successor/synthetic-expected.json`: `f93f8d60649f27b0890ad021d606d58abfcce85e48c82d47181b8b6f9bf149e3`
- `projects/chirality-app-v4/app/src-tauri/resources/distribution-successor/synthetic-evidence.json`: `159d63ddba6a68e91a403359e0a20e26bc8ff8b761f7bad9cd2b75e219d232e3`
- `projects/chirality-app-v4/app/src-tauri/resources/distribution-successor/synthetic-attestation.json`: `f7a270126f4e7c6a651c7969e538fadcae0d85d610881d5b2b2d2abb94362754`
- `projects/chirality-app-v4/app/src-tauri/resources/distribution-development-reference/build-selection.s2.json`: `f0c369a18de5ed9a35dda4519bc89944f9a41824c1b5c52e2d9ec3e723761133`

## Offline checks

Prepared Cargo cache, isolated temporary target, CHIRALITY_SKIP_CODEX=1. No
supplier process, probe, credentials, native App window, download or release.
The tests compile the actual App library and invoke the same helper used by setup.

- `cargo test --offline --locked --lib compiled_anchor`: 1 passed; disabled
  closure panics if resolved, so no helper lookup occurs.
- `cargo test --offline --locked --features custom-protocol --lib compiled_anchor`:
  1 passed, still disabled. Existing local frontend build artifacts serve Tauri
  compilation only; no UI/package witness or qualification claimed.
- `cargo test --offline --locked --features synthetic-distribution-anchor --lib compiled_anchor`:
  3 passed for actual-resource matches/refusals and fixed schema/relations.
- `cargo rustc --offline --locked --lib --features synthetic-distribution-anchor -- -C debug-assertions=no`:
  expected exit101 with the explicit debug-only compile_error. This tests the
  exact non-debug cfg guard, not a full --release dependency/package build.
- `git diff --check`: passed. Existing unused/dead-code warnings remain.

Initial default test compile found the new AppState field absent from one existing
local fixture constructor; that constructor now gives the field an explicit
not-observed fixture value. No fixture startup I/O introduced.

Configured Ryan C Tufts <ryan@chirality.ai> and absent author/committer/EMAIL
overrides verified; official staged privacy check precedes commit. Independent
review, packaging integration and any actual App observation remain with parent.

Combined debug `--features custom-protocol,synthetic-distribution-anchor` with
`--lib compiled_anchor`: 3 passed. Custom-protocol is neither required nor an
implicit enable for the synthetic feature. Production availability stayed false
in the matched fixture tests.
