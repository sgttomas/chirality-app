# Proposed App v4 code correctness CI — owner decision packet

Status: PROPOSED; no workflow installed, no download or CI run performed. Prepared by bounded TASK `/root/group_a_ci_proposal` for HELP_HUMAN `/root`, using delegated-harness-native execution, no further delegation. Sole write is this packet. Working sources were inspected at HEAD `cb5a88b29ac10fc0c09f9b6a44f497ab917e8a71` with concurrent Group A implementation edits; fingerprints below identify the actual read basis, not a frozen integration candidate.

## Recommended owner choice

Authorize one macOS code-check job with the exact YAML below at `.github/workflows/app-v4-code-checks.yml`, including GitHub-hosted macOS runner minutes and its bounded network bootstrap. Explicitly except **this workflow only** from LOOP's per-file/source/size download presentation: allow Rust 1.92.0 minimal toolchain, Node 24.5.0, the named GitHub Actions releases, and Cargo/npm dependencies selected by the candidate's committed lockfiles. Total compressed download bytes on a clean runner are **unmeasured**. Dependency changes must still be disclosed/reviewed in their own authorized change; this exception grants no unrelated package, supplier binary, auth or release download.

Alternative: keep this prepared workflow disabled and continue local offline checks. No authorization is recorded by this packet. Parent retains custody of the actual owner answer.

Sources of bootstrap traffic: GitHub source/actions and Node distribution delivery through `actions/setup-node`; Rust toolchain manifests/components from `static.rust-lang.org`; locked npm tarballs from the `resolved` URLs in `app/package-lock.json` (current registry.npmjs.org); Cargo index metadata and locked registry archives from crates.io/static.crates.io. Lockfile integrity/checksums are used by npm/Cargo. The previous 29-file, 3,223,082-byte approval is a local-cache incremental validator addition and cannot be presented as the clean CI runner total. No external Tauri bundler tools, signing assets or Codex binary are fetched.

The job uses existing project requirements Rust 1.92 and Node 24, narrowed to locally observed 1.92.0/24.5.0. Actions use existing repository `@v4` release references; those references are mutable and are **not** claimed to be immutable SHA pins. Tool versions and package resolutions are pinned. Action commit pinning may be reviewed separately; no unverified SHA is invented here.

## Exact proposed workflow

```yaml
name: App v4 code checks

on:
  pull_request:
    types: [opened, synchronize, reopened]
    paths:
      - '.github/workflows/app-v4-code-checks.yml'
      - 'projects/chirality-app-v4/app/**'
      - 'projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/**'
      - 'projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/**'
      - 'projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/Design/**'
      - 'projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-01_Operation-policy and human-act distinctions/Design/**'
      - 'projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-02_Visible autonomy and result standing/Design/**'
      - 'projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/**'
      - 'projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/E/fixtures/FX-DP1/**'
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: app-v4-code-checks-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}

jobs:
  code-checks:
    name: App v4 macOS code correctness
    runs-on: macos-14
    timeout-minutes: 30
    defaults:
      run:
        shell: bash
        working-directory: projects/chirality-app-v4/app
    env:
      CI: 'true'
      RUSTUP_TOOLCHAIN: '1.92.0'
      CHIRALITY_SKIP_CODEX: '1'
    steps:
      - name: Checkout candidate and exact test inputs
        uses: actions/checkout@v4
        with:
          persist-credentials: false
          filter: blob:none
          sparse-checkout: |
            projects/chirality-app-v4/app
            projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design
            projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design
            projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/Design
            projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-01_Operation-policy and human-act distinctions/Design
            projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-02_Visible autonomy and result standing/Design
            projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design
            projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/E/fixtures/FX-DP1
      - name: Bootstrap exact Node version (network permitted)
        uses: actions/setup-node@v4
        with:
          node-version: '24.5.0'
      - name: Bootstrap exact Rust version (network permitted)
        run: rustup toolchain install 1.92.0 --profile minimal
      - name: Bootstrap locked dependencies (network permitted)
        run: |
          npm ci --ignore-scripts --no-audit --no-fund
          cargo fetch --locked --manifest-path src-tauri/Cargo.toml --target "$(rustc -vV | sed -n 's/^host: //p')"
      - name: Record candidate and environment
        run: |
          git rev-parse HEAD
          sw_vers
          uname -m
          node --version
          npm --version
          rustc --version
          cargo --version
          shasum -a 256 package-lock.json src-tauri/Cargo.lock
          printf '%s\n' 'SUPPLIER HANDSHAKE: OMITTED (no Codex binary installed)' >> "$GITHUB_STEP_SUMMARY"
      - name: Build frontend and Rust host; test offline
        env:
          CARGO_NET_OFFLINE: 'true'
          npm_config_offline: 'true'
        run: |
          unset CHIRALITY_CODEX_BIN CHIRALITY_CODEX_HOME CHIRALITY_CODEX_EXPECTED_SHA256
          npm run build
          cargo build --locked --offline --manifest-path src-tauri/Cargo.toml
          cargo test --locked --offline --manifest-path src-tauri/Cargo.toml
          npm test
      - name: Require unchanged dependency locks
        if: always()
        run: git diff --exit-code -- package-lock.json src-tauri/Cargo.lock
```

## Coverage and integration conditions

This adds a separate path-filtered workflow; it changes no App v3, Piping, PEC or Root existing CI. Checkout's default PR merge ref checks the integration candidate; dispatch checks the selected branch/ref. Sparse checkout includes external schema and Pass 4 fixture consumers without checking out all historical multi-gigabyte evidence. No push trigger or cross-platform matrix is added. Do not mark this path-filtered job globally required for unrelated PRs without a separate applicability policy: a skipped workflow does not provide a stable not-applicable check.

Rust build checks the native Tauri host compile, then `cargo test` covers maintained units plus decision-flow and W-1 schema refusal integration tests. `npm test` runs the decision flow again to produce uniquely owned exports, then validates their external Design schemas through Ajv. The deliberate small duplicate integration run exercises the current existing test interface without source edits. Nested Cargo calls currently lack `--locked`; locked fetch/build/test resolve first and the final unchanged-lock check rejects drift. `npm ci --ignore-scripts` prevents install lifecycle downloads/execution; supported prebuilt optional esbuild package must be present for Vite. No package install occurs during tests. No cache/artifact service is added; GitHub job logs retain candidate/tool versions and test outputs.

Offline flags prevent npm/Cargo dependency retrieval during checking; they are **not an OS network-denial proof** for arbitrary test code. Current selected tests use local fixtures and no supplier when `CHIRALITY_CODEX_BIN` is unset. They read no owner credentials, sign in nowhere, and start no live model turn. Future test changes must preserve or separately authorize this scope.

The Rust handshake test returns successfully when `CHIRALITY_SKIP_CODEX=1`; Node separately marks hosting-record validation skipped. The summary explicitly identifies omission so a green job cannot be reported as supplier integration coverage. Current source still asserts 0.158.0 in handshake while the authorized development supplier is 0.160.0. Its arm64 binary SHA-256 is `112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b`, machine-local path `/Users/ryan/Library/Caches/chirality-dev/codex/0.160.0/codex` (provider/README.md). This binary/path does not establish a distribution for the CI runner architecture. Adding stock supplier coverage requires exact platform archive authorization/integrity and the matching version/generated-schema/handshake protocol check; it cannot reuse an arm64 hash on an Intel runner or assert the historical protocol silently.

Packet checks: the fenced YAML parsed with the already installed PyYAML; every proposed trigger/input directory exists. No workflow has been executed. In-flight P0 propagation has not been reviewed here. At inspection the Node schema validator still rewrites historical relative refs and asserts a positive rewrite count, while adopted RS uses the new declared identity. That existing check may fail until its authorized consumer propagation integrates; CI must expose the failure, not relax the Design criteria or report readiness in advance. Review the final scripts/input list at integration and extend triggers/sparse paths if ready Group A slices introduce new external test inputs. Failure from 30-minute timeout is a preparation observation, not a license to omit tests.

## Group A / Group B and resources

Group A owns correctness verification for its produced code and receives this check as part of I1–I5/V1/F1. Group B owns DEL-01-06 packaging plus DEL-09-01 examination and DEL-09-02 supplier qualification. This job produces no `.app`/`.dmg`, signature, installer, release artifact, product-use examination, practitioner witness or qualification result. It does not claim 90% readiness or owner gate acceptance. Carry the CI scope/omissions to B's graph when that loop opens, preserving A's recorded DEP-09-09-012 consumption of B's examination protocol.

One macOS job is capped at 30 minutes; synchronized PR updates cancel older PR runs. Actual runtime, GitHub plan/quota, billing rate and total clean-runner bytes are unknown; **no dollar or minute-cost estimate is established**. A cold build may exceed the cap. The owner choice accepts bounded runner use and known bootstrap scope with these uncertainties, or keeps CI disabled. No account settings, billing settings, branch protection or repository permission change is proposed.

## Source fingerprints

Actual filesystem bytes read once for this packet (SHA-256); active implementation can supersede these without rewriting their historical meaning. Root/TASK/LOOP and manual origins were loaded as instructions/guidance; other records were task evidence. Agent User Manual headings were consulted plus §§11 and the decision-package example; Field Book read in full. No workflow-authoring method was selected: this is a GitHub CI configuration proposal, not a reusable Chirality coordination workflow.

| Source | SHA-256 |
|---|---|
| `AGENTS.md` | `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977` |
| `agents/AGENT_TASK.md` | `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7` |
| `projects/chirality-app-v4/loop/LOOP_INIT.md` | `45c23cf477e23aff1d0152189caf7e8ebfb53eca42e3a1fae87a06af8c197f28` |
| `docs/alignment-manual/README.md` | `31217d30b0d2743bef0d7c1a54bb9a81814d56b24ff0961cf01d9532952e305f` |
| `docs/alignment-manual/CHIRALITY_AGENT_USER_MANUAL_v3.md` | `08ca0e40cd5157574a011bac57d539e77e9007a0d46494785da8b92745391b1a` |
| `docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Field_Book_v1.md` | `02d53a3966220001318aacf3f46e1b63b8695a098c81b20f4e3e1531b93024d3` |
| `projects/chirality-app-v4/app/package.json` | `afd49df0c9ab9bb00bdacfc41a7f356f1347a36b82145e4974a6b5121f41c7e0` |
| `projects/chirality-app-v4/app/package-lock.json` | `1392f7926e008f71e103e91734b1a9e0e40477c68865ea482aa885954a3d25fa` |
| `projects/chirality-app-v4/app/src-tauri/Cargo.toml` | `2d89ee516e013d3e8990c15a2eaeebb1ce08588934a26193bfb93b604e4f7d31` |
| `projects/chirality-app-v4/app/src-tauri/Cargo.lock` | `4318a283dcc25c594e6b99c2e7110495abc8cd89c45de9453cf0aaa5befa8549` |
| `projects/chirality-app-v4/app/README.md` | `a9a764698d351803cf8c8f93cdfdd0bc2e3de0c01e6a20e28525d6fc0e020c7f` |
| `projects/chirality-app-v4/app/tests/validate-records.test.mjs` | `fe519186229666a9641ca279ce7596684514f22aaf6d13ec01c7fe418007f54a` |
| `projects/chirality-app-v4/app/src-tauri/tests/handshake.rs` | `f355d77e6d812a44b01278490efb4d088a2b5f76237e844866ecde71c6e1c4b3` |
| `projects/chirality-app-v4/app/src-tauri/tests/schema_validation.rs` | `35521f3db314a3a956f5a6b47e41b7739b170ddda39e9c8b58536773f7f7ce62` |
| `projects/chirality-app-v4/execution/_Coordination/WorkGraphs/APP-V4-GROUP-A-20261004/WORK_GRAPH.md` | `f03cc9ce2285bbb55d150f6ddca5460213a6d3deea66fecae862b4fdad5a7669` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GRAPH-CLOSURE-20261004/GROUPS.md` | `d96c399755fe2369cab96d29f73744834a98d70678f2f273f9ad01b0b129940f` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/provider/README.md` | `19aaadac7b9a20b2dc8123997ea158e1b9832b9e26e323a104e9701c66fa082e` |
| `.github/workflows/harness-premerge.yml` | `b0748776af5e2014ce37bee91baffcd0d996134bba7301d220d8bcac42243907` |
| `.github/workflows/piping-desktop-e2e.yml` | `6d38e7420cf6a38eb2a58b5da422b82c5a141c7272aab27c3d4ed3aee6316338` |
