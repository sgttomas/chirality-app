# Proposed App v4 code correctness CI — R1 owner decision packet

Status: PROPOSED; owner CI/network exception remains pending. No workflow installed, downloads, network access, builds, tests, shared Cargo use or CI execution occurred for this refresh. The original `CI_PROPOSAL.md` is preserved. Prepared by bounded TASK `/root/ci_proposal_refresh` for HELP_HUMAN `/root`, using delegated-harness-native execution with no descendants; sole write is this file. Model allocation requested: gpt-6.1-sol / medium. Read basis: HEAD `a7a6bf02b8e02a10e8a22946dbaf21b7c4670f70` plus concurrent modified/untracked Group A files, inspected 2026-10-05. This is source inspection, not frozen-candidate verification.

## Proposed owner choice and unchanged resource boundary

Authorize the exact YAML below at `.github/workflows/app-v4-code-checks.yml`: one GitHub-hosted macOS job capped at 30 minutes, Rust 1.92.0 minimal and Node 24.5.0, and bounded network bootstrap of the named Actions releases and Cargo/npm dependencies selected by the candidate's committed lockfiles. Except this workflow only from LOOP's per-file/source/size presentation requirement. Clean-runner compressed bytes, runtime, GitHub quota/billing rate and dollar cost remain unmeasured. The runner supplies Python 3 for local JSON/hash checks; its observed version is recorded, not independently pinned here.

Bootstrap sources remain GitHub source/actions, Node delivery through `actions/setup-node`, `static.rust-lang.org`, npm lockfile `resolved` URLs (currently registry.npmjs.org), and Cargo index/archive delivery from crates.io/static.crates.io. npm integrity and Cargo checksums apply. Actions `@v4` tags are mutable release references, not immutable SHA pins. `npm ci --ignore-scripts` prevents install lifecycle scripts; Vite still requires the selected prebuilt optional esbuild package. The earlier 29-file validator and two-file CommonMark local approvals do not authorize or measure clean CI bootstrap. Dependency changes still require their own reviewed authorized adoption.

No supplier binary, authentication, live model/provider turn, native UI witness, external host dispatch, Tauri bundler/signing tools, release artifact, cache service, branch-protection or account change is authorized by this proposal. Alternative: retain the prepared packet and continue authorized local offline checking. Parent retains custody of the actual owner answer.

## Changes supported by current source

- PROPOSAL: Expand checkout and triggers for current canonical test inputs
  - Evidence: `app/src-tauri/tests/catalog_adapter.rs::maintained_resources_match_identified_source_bytes`, `external_trace.rs::maintained_canonical_resources_and_examples_match_recorded_source_bytes`, `attachments.rs::embedded_assets_match_canonical_sources_and_produced_input_matches_actual_supplier_schema`; their resource manifests; `app/tests/validate-records.test.mjs::validators`; `app/src-tauri/schemas/manifest.json`.
  - Change: Use the matching precise directories in the YAML below. Existing direct Rust provenance checks require DEL-03-01/02/03, DEL-05-01/02 and DEL-09-01/09 in addition to old packet coverage.
  - Why: The old sparse checkout omits files read by the current full Rust suite and would fail independently of implementation correctness.
  - Risk: More repository blobs are fetched during checkout; clean byte total remains unknown. A path-filtered check should not become globally required for unrelated PRs without a separate applicability policy.
  - Status: PROPOSED
- PROPOSAL: Verify current maintained interface copies without rewriting them
  - Evidence: `app/src-tauri/schemas/sync.py`, `resources/runtime_core/manifest.json`, `resources/workflow_role/SOURCE_MAP.json`, and current resource manifests with `source`/`file` pairs.
  - Change: Add the non-mutating `schemas/sync.py` invocation and JSON byte/hash check shown below; include their canonical Design directories, including DEL-01-02/03/05 and DEL-02-01/02/04. Fail if copies or current map hashes differ; never use `--sync` in CI.
  - Why: Current builds consume embedded recovery/access/native-plan/WR/WD/EXEC/ROLE resources. A changed canonical interface with an unchanged copy can compile and validate against stale bytes; this check catches that real mismatch.
  - Risk: This is a newly recommended check, distinct from existing maintained tests. Reviewed interface adoption must update the map/copy together. Map hashes identify the current adopted resource edition; they do not certify every historical source revision forever.
  - Status: PROPOSED
- PROPOSAL: Keep omission reporting current
  - Evidence: `app/src-tauri/tests/handshake.rs` explicitly checks stock 0.160.0 and permits `CHIRALITY_SKIP_CODEX=1`; `app/tests/validate-records.test.mjs` skips hosting exports without a binary; `native_backend_smoke.rs` marks its authenticated live case ignored.
  - Change: Report all omitted supplier/authenticated/native/release coverage in job summary; unset supplier/backend/key variables; retain ordinary default `cargo test` without global `--ignored`.
  - Why: Green code CI cannot establish supplier or native product-use qualification.
  - Risk: Synthetic credential-safe RPC and native-page tests remain useful code checks but do not establish real credentials, OAuth, supplier receipt or a physical UI/IPC witness.
  - Status: PROPOSED

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
      - 'projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/**'
      - 'projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-03_Native plans, tools and delegation views/Design/**'
      - 'projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/**'
      - 'projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-05_Native OAuth-sign-in, API-key and local-provider access/Design/**'
      - 'projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-01_Portable workflow contract and shared allocation/Design/**'
      - 'projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-02_Workflow-making workspace and registration/Design/**'
      - 'projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/Design/**'
      - 'projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-04_Additive role selection and supply/Design/**'
      - 'projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/Design/**'
      - 'projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-02_Proposal, validation and outcome contract/Design/**'
      - 'projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/Design/**'
      - 'projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-01_Operation-policy and human-act distinctions/Design/**'
      - 'projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-02_Visible autonomy and result standing/Design/**'
      - 'projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/**'
      - 'projects/chirality-app-v4/execution/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-01_Minimal-loop and model receiving contract/Design/**'
      - 'projects/chirality-app-v4/execution/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-02_Host panel and shared interaction receiving/Design/**'
      - 'projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-01_Candidate examination infrastructure and evidence protocol/Design/**'
      - 'projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-09_External control and catalog-extension trace/Design/**'
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
            projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design
            projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-03_Native plans, tools and delegation views/Design
            projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design
            projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-05_Native OAuth-sign-in, API-key and local-provider access/Design
            projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-01_Portable workflow contract and shared allocation/Design
            projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-02_Workflow-making workspace and registration/Design
            projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/Design
            projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-04_Additive role selection and supply/Design
            projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/Design
            projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-02_Proposal, validation and outcome contract/Design
            projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/Design
            projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-01_Operation-policy and human-act distinctions/Design
            projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-02_Visible autonomy and result standing/Design
            projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design
            projects/chirality-app-v4/execution/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-01_Minimal-loop and model receiving contract/Design
            projects/chirality-app-v4/execution/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-02_Host panel and shared interaction receiving/Design
            projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-01_Candidate examination infrastructure and evidence protocol/Design
            projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-09_External control and catalog-extension trace/Design
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
          python3 --version
          printf '%s\n' 'OMITTED: supplier handshake, authenticated/live backend, native UI/IPC witness, packaging/release' >> "$GITHUB_STEP_SUMMARY"
      - name: Check maintained interface resources offline
        run: |
          python3 src-tauri/schemas/sync.py
          python3 - <<'PYCODE'
          from pathlib import Path
          import hashlib, json
          app = Path.cwd()
          root = app.parents[2]
          resources = app / "src-tauri/resources"
          checked = 0
          for mapping in sorted(resources.rglob("manifest.json")) + sorted(resources.rglob("SOURCE_MAP.json")):
              document = json.loads(mapping.read_text())
              rows = document if isinstance(document, list) else document.get("resources", [])
              for row in rows:
                  if "source" not in row:
                      continue
                  asset = mapping.parent / row.get("file", row.get("resource", ""))
                  source = root / row["source"]
                  original, embedded = source.read_bytes(), asset.read_bytes()
                  assert original == embedded, f"interface resource drift: {asset} <- {source}"
                  assert hashlib.sha256(original).hexdigest() == row["sha256"], f"resource map drift: {source}"
                  checked += 1
          assert checked > 0, "maintained interface resource maps absent"
          print(f"{checked} mapped interface resources match current source bytes and map hashes")
          PYCODE
      - name: Build frontend and Rust host; test offline
        env:
          CARGO_NET_OFFLINE: 'true'
          npm_config_offline: 'true'
        run: |
          unset CHIRALITY_CODEX_BIN CHIRALITY_CODEX_HOME CHIRALITY_CODEX_EXPECTED_SHA256
          unset CHIRALITY_RUN_NATIVE_BACKEND_SMOKE CHIRALITY_NATIVE_SMOKE_BIN CHIRALITY_NATIVE_SMOKE_AUTH_HOME
          unset OPENAI_API_KEY CODEX_API_KEY CODEX_ACCESS_TOKEN
          npm run build
          cargo build --locked --offline --manifest-path src-tauri/Cargo.toml
          cargo test --locked --offline --manifest-path src-tauri/Cargo.toml
          npm test
      - name: Require unchanged dependency locks
        if: always()
        run: git diff --exit-code -- package-lock.json src-tauri/Cargo.lock
```

## Required inputs versus added provenance checks

The entire `app/` subtree contains compile-time `include_str!`/`include_bytes!` schemas, supplier 0.160.0 generated protocol resources, WR/ROLE fixtures, source files and build/frontend configuration. These generated supplier schemas are already repository bytes: no generator or Codex executable is fetched or run.

Existing full-suite runtime reads outside `app/` are in attachment, catalog and external-trace canonical-resource tests, while Node Ajv reads DEL-01-01/04, DEL-02-03 and DEL-04-02/03 Design schemas. Those Node schemas are registered by their declared IDs unchanged, and both nested Cargo calls now use `--offline --locked`; the old packet's schema-rewriting and unlocked-nested-Cargo warnings are obsolete.

The proposed additional provenance step also consumes current source maps for hosting, policy/standing, runtime core and workflow-role resources. Its added checkout paths are justified by those exact maintained maps rather than a blanket execution-tree checkout. WR sources and copies matched at inspection, but concurrent implementation may supersede them. CommonMark `pulldown-cmark =0.13.4`, defaults off, is now in Cargo.toml/Cargo.lock, with locked `unicase` dependency; its approved local admission is distinct from this pending CI exception.

The old packet included dated `APP-V4-DESIGN-PASS-4-20261003/E/fixtures/FX-DP1` checkout coverage. Current maintained Rust tests read `app/tests/fixtures/FX-DP1`; `schemas/manifest.json` maps its schemas/fixtures to canonical Design files, not that run directory. R1 therefore removes the historical directory from triggers and checkout. Existing historical provenance remains as data: `resources/external_trace/own-code-inputs.json` names Group A change/review records and `external_trace.rs::own_code_inputs_and_missing_unknown_refused_claims_keep_separate_origin` reads its embedded bytes; it does not dereference those historical paths. Instruction/policy basis snapshots also retain dated origin references. No new CI assertion pins historical run records or claims their hashes must remain current. The newly proposed map check handles only file/resource rows naming current interface copies; it does not recursively certify historical instruction/basis metadata.

## Offline isolation and omitted evidence

Bootstrap is the only authorized network stage if the owner chooses this proposal. Cargo checking uses `--offline --locked` plus `CARGO_NET_OFFLINE=true`; Node receives `npm_config_offline=true`; JSON Schema registries use maintained local resources with retrieval disabled. These settings restrict dependency/schema retrieval and are not an OS-wide socket-denial proof for arbitrary code. Current maintained tests use synthetic data, owned temporary paths and local stand-in subprocesses (`/bin/cat`, bounded FIFO/sleep probes); no owner's home or credentials are supplied. Changes introducing external traffic require separate authorization. Job environment and explicit unsets prevent the known supplier/live-backend triggers in this YAML.

The handshake is explicitly skipped, and Node hosting-output validation separately reports a skip. Default Rust tests do not run the ignored authenticated backend greeting case. An ignored owned nonreader subprocess probe is invoked by its maintained watchdog with exact case/owned scratch environment; this is a local liveness test, not supplier coverage. Synthetic native-page, account/credential-canary, workflow receiving and transport tests exercise code boundaries only. Physical native dialogs/UI/IPC, authenticated OAuth/API-key/provider use, actual native history/Continue/child carriage, supplier binary/protocol qualification, process-kill durability/cold trust and external host joins retain their separate owning evidence obligations.

`cargo build` compiles the Tauri native host after the frontend build. It does not package `.app`/`.dmg`, sign, install, launch or release the product. `cargo test` covers maintained default unit/integration tests; `npm test` repeats the decide-flow integration once to own its export directory and validates outputs through Ajv. No global ignored suite or supplier provisioning is added. Final lock-drift rejection remains a backstop after locked fetch/build/test. No artifact upload or shared cache is added.

## Candidate standing and integration conditions

Current files include active uncommitted CommonMark/WR/access/native receiving work. This packet does not establish that those changes compile or pass, or that the 30-minute cold-run cap is sufficient. Before installation, parent must re-evaluate maps, dependency locks, test external reads and actual frozen integration candidate; record that revision and affected review. Source drift is a reason to refresh/recheck, not relax the interface contract or silently remove a failing check. The YAML parsed with installed PyYAML; its embedded Python parsed with `ast.parse` without execution; all 20 sparse-checkout directories exist. The proposed JSON checks have not been executed as tests here.

Group A owns code correctness within its produced slices. Group B retains packaging, examination protocol and supplier qualification; DEL-09-01 schemas consumed here are interface checks, not proof that examination occurred. Carry coverage/omissions to B when its loop opens, preserving DEP-09-09-012. No 90% readiness, gate acceptance, product release or deferred SWBPIPE/PEC/Domain witness is established.

MISSING: clean-runner byte total, cold runtime/billing observations, owner CI/bootstrap decision, actual frozen-candidate CI run.

NEEDS_HUMAN_RULING: authorize the bounded CI/network/runner exception described above or retain offline-only operation. No prior download authorization is broadened by this packet.

DEPENDENCY_NOTES: historical provenance references remain data, with obsolete dated checkout removed; CommonMark/WR WIP must receive current candidate review and tests; supplier/auth/native/external examination remains separate.

## Source fingerprints and inspection record

SHA-256 below identifies actual bytes read for this refresh, not a frozen product candidate. Root/TASK/LOOP were supplied or read as applicable instructions; Agent User Manual headings and delegation/decision context were consulted, Field Book read in full. Proposal-format was read and applied. No reusable Chirality workflow was authored or revised; this is a CI configuration decision packet. Concurrent writers may supersede these bytes. The original packet remains historical.

| Source (repository relative) | SHA-256 |
|---|---|
| `AGENTS.md` | `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977` |
| `agents/AGENT_TASK.md` | `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7` |
| `.agents/skills/proposal-format/SKILL.md` | `63e6d2545c31df939511a5a137c214d5444ca562f6abf9b048de3aa2f8dac59d` |
| `projects/chirality-app-v4/loop/LOOP_INIT.md` | `45c23cf477e23aff1d0152189caf7e8ebfb53eca42e3a1fae87a06af8c197f28` |
| `docs/alignment-manual/README.md` | `31217d30b0d2743bef0d7c1a54bb9a81814d56b24ff0961cf01d9532952e305f` |
| `docs/alignment-manual/CHIRALITY_AGENT_USER_MANUAL_v3.md` | `08ca0e40cd5157574a011bac57d539e77e9007a0d46494785da8b92745391b1a` |
| `docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Field_Book_v1.md` | `02d53a3966220001318aacf3f46e1b63b8695a098c81b20f4e3e1531b93024d3` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/CI_PROPOSAL.md` | `d36a58b201e16df9aba6cc68a04342c5f0f933502735187c1a1bbcfbea48775c` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/OWNER_DECISIONS.md` | `f92b299562be0c22151c5672067c37e611e0d6aa17e0353c60532c2b58f84637` |
| `projects/chirality-app-v4/execution/_Coordination/WorkGraphs/APP-V4-GROUP-A-20261004/WORK_GRAPH.md` | `2a6ff7e06ac60df96345927074e405b6c95ccbf968e0372f0d394aa85f48511e` |
| `projects/chirality-app-v4/app/README.md` | `29a5ab49c5f8667a15a36721806c654dc708477cb6a22a5ebaaad94cf4b73016` |
| `projects/chirality-app-v4/app/package.json` | `afd49df0c9ab9bb00bdacfc41a7f356f1347a36b82145e4974a6b5121f41c7e0` |
| `projects/chirality-app-v4/app/package-lock.json` | `1392f7926e008f71e103e91734b1a9e0e40477c68865ea482aa885954a3d25fa` |
| `projects/chirality-app-v4/app/tests/validate-records.test.mjs` | `8b0011f2d00b457527fcfea2e37f4c616be57e893abb84282a3128e0bcfd8a07` |
| `projects/chirality-app-v4/app/src-tauri/Cargo.toml` | `897dfa625fbb9c3666a92c9cbd6b12ff8bb86083b5ee050313832a71bca3b968` |
| `projects/chirality-app-v4/app/src-tauri/Cargo.lock` | `c1910cffc3fc311fc50cae1117d5aa379dc374142c643c3b22ad85998dbf86b2` |
| `projects/chirality-app-v4/app/src-tauri/build.rs` | `487059eaf8a947b80f20a9aacac038a5047b2ad69d2401b827376c67d6fe847f` |
| `projects/chirality-app-v4/app/src-tauri/tauri.conf.json` | `5f848cc760814808e8013aac972c1ecf90251818b41f4358ee0f342359c4b3ec` |
| `projects/chirality-app-v4/app/src-tauri/schemas/sync.py` | `65640c13b5540a756379bab7f39c01aa303df5521ec0f420ca00f0050ff36200` |
| `projects/chirality-app-v4/app/src-tauri/tests/access_integration.rs` | `e849dc6112456a22410636945272ff0b5e99b26c9c3bc4311b6a43d5165fca49` |
| `projects/chirality-app-v4/app/src-tauri/tests/act_storage.rs` | `55e19fe7c5d36c61f6ff37e24bd64a1979bc4a8e2dc5ce797106b0ca4e857a2d` |
| `projects/chirality-app-v4/app/src-tauri/tests/attachment_integration.rs` | `52c63ca004731927d1d1260cd9cebfc455ba71211384a191438bb06112c82f3f` |
| `projects/chirality-app-v4/app/src-tauri/tests/attachment_transport.rs` | `99df63749a5c310685221800c4b94b3610b6cb7e37ae71d034e8ddf3b434f9be` |
| `projects/chirality-app-v4/app/src-tauri/tests/attachments.rs` | `3d15eca729d4e8c5ff045a9386503d730a9c30ec8e7be3e8dc581feb7feda553` |
| `projects/chirality-app-v4/app/src-tauri/tests/catalog_adapter.rs` | `5e882af15c5525d539c94a2da12003d39c42c036427979f9df247e1f73a18c8b` |
| `projects/chirality-app-v4/app/src-tauri/tests/conversation_integration.rs` | `14710dba817269dd23cd9aa96a8281686944b7636758144d9bcc7162a0242694` |
| `projects/chirality-app-v4/app/src-tauri/tests/decide_flow.rs` | `19fbab599c4d1726ed9c35735b289375979d2dac76dfc1519787274eef511528` |
| `projects/chirality-app-v4/app/src-tauri/tests/decision_reader.rs` | `7fbd2ab9b271f2fda5c02d87d2306ca223122f1a0fc16ae9632a9583d9f778fe` |
| `projects/chirality-app-v4/app/src-tauri/tests/decision_standing.rs` | `8b3c6074a7e11248267aae9902fe1138a54ce6313d4dbc44abaedd62ff9214ff` |
| `projects/chirality-app-v4/app/src-tauri/tests/explicit_context.rs` | `aa3ea786b187306160e351e5236b680dd3e2a5862b15285a93dd5047a300c0ae` |
| `projects/chirality-app-v4/app/src-tauri/tests/external_observation.rs` | `255b1a0bdfee4a1a4cb09625da771da006c606b32e73f317a3ddeb30ba858a3d` |
| `projects/chirality-app-v4/app/src-tauri/tests/external_observation_integration.rs` | `1a59b14714d7be5a200d2848a0b15b71c8f71dea27b330659e2741548221eae8` |
| `projects/chirality-app-v4/app/src-tauri/tests/external_trace.rs` | `1a3116fe99f6b58835df6812da9ec402b75d86be31fbdf0f92f28af260ad3112` |
| `projects/chirality-app-v4/app/src-tauri/tests/handshake.rs` | `3c7878804866b95e3bd96ea2e566b478b37cc7d590c91a0518ae391e1a2c2406` |
| `projects/chirality-app-v4/app/src-tauri/tests/history_integration.rs` | `d41b42bc40b349f24b56b9d61e20a2efd9a15b804f7a9d645e9ffe70624a3ca5` |
| `projects/chirality-app-v4/app/src-tauri/tests/home_resources.rs` | `b35fe0622705bc3702de98f7b3d835921ac581af3b5de89297c53b22908bf64e` |
| `projects/chirality-app-v4/app/src-tauri/tests/hosting_contract.rs` | `ffb1aeefb0b7336a556059f21e2bf1ab4155d6f425d45efe7aaf6a66ac66ae7e` |
| `projects/chirality-app-v4/app/src-tauri/tests/native_backend_smoke.rs` | `5c966daca7731a64e5f1fc1af5032e183a1298f9411dd6bf881ce8cd6e5e153f` |
| `projects/chirality-app-v4/app/src-tauri/tests/native_history.rs` | `b473c4ddaacf52f0bf0aac60bb12efe1bd20a76a02e63cf68a122838a25d234e` |
| `projects/chirality-app-v4/app/src-tauri/tests/native_page_witness.rs` | `6bc02752d0cf33b09116fc15ac90f1c9bfc72b8040cf6f534299c7ab7660ebf0` |
| `projects/chirality-app-v4/app/src-tauri/tests/policy_standing.rs` | `d8332ea367081768e492951f0fea7c999b972085747014823d3ec7ac563dcc06` |
| `projects/chirality-app-v4/app/src-tauri/tests/reader_integration.rs` | `79a7a3970671e50336800e0ec73f9bc98ea904b5813a9f0b49a691bb52647878` |
| `projects/chirality-app-v4/app/src-tauri/tests/record_relations.rs` | `ad6ce8a460be42883560bb341eceb2be525e0fe768bd41f7bd6835c32971aa76` |
| `projects/chirality-app-v4/app/src-tauri/tests/recovery_startup.rs` | `778562fa9f550014753e6b31b91e05eae2c1b8925ac007fcb3f7a3a100b69a78` |
| `projects/chirality-app-v4/app/src-tauri/tests/role_lifecycle.rs` | `9c0fb4e5ad4ff4e2fed66ef4dea14edf23e32a21f9501af3c965860317f32885` |
| `projects/chirality-app-v4/app/src-tauri/tests/runtime_integration.rs` | `18ed6496863eb76cc950c96e162ddb955139a92d776a313c3a9e7a4591195ee2` |
| `projects/chirality-app-v4/app/src-tauri/tests/schema_validation.rs` | `1022c3026430fc3d3c14f86adb29e021df99f0b5bc9973578f8d24cac22a6985` |
| `projects/chirality-app-v4/app/src-tauri/tests/steering_integration.rs` | `33e826cc27dc5fc4498acfe982cacdedb2e5f2e8c25c4546eda7708bfd0511cd` |
| `projects/chirality-app-v4/app/src-tauri/tests/trace_integration.rs` | `7ff29f313f0824b8edb4688b0aad6390586bd71b4d93c3b13eb0e0a1f84b3ec7` |
| `projects/chirality-app-v4/app/src-tauri/tests/trace_receiving.rs` | `f6853c0cbedd0927f7634bec837615c1088dd7e7d3cd0c7716acf93166066ab4` |
| `projects/chirality-app-v4/app/src-tauri/tests/workflow_receiving.rs` | `bbe25bb3996cd3728625f3d79e01b0e9e1337c90f30f32df95ebc6c21fa4c370` |
| `projects/chirality-app-v4/app/src-tauri/tests/workflow_role.rs` | `7b6e97e5644c9235d3ca463ee794bb6e0030486e94c47266fea7a46f2f31d6ad` |
| `projects/chirality-app-v4/app/src-tauri/src/hosting.rs` | `c81e1d9638752a91589842bf695794b0cd4afe61aa85e8edb986aadf45a73a74` |
| `projects/chirality-app-v4/app/src-tauri/src/workflow_declaration.rs` | `db4ead65dc5d4cbc7fbd64fc9ce4c8f4d6112fac2091766658b0a3539341dd07` |
| `projects/chirality-app-v4/app/src-tauri/src/workflow_workspace.rs` | `93eeaf90dc9ed4c1ea2347c7bf026f58ea050bcaf72eb6d103b31aa263c6f97a` |
| `projects/chirality-app-v4/app/src-tauri/src/execution_compatibility.rs` | `ecdfb8b01a1e6dbb42ef00992a8d990a841dbe6d1c66224064bd1facdfff9994` |
| `projects/chirality-app-v4/app/src-tauri/schemas/manifest.json` | `7c11acfe9f4088b1c4703970341df82ebe2fc23c9938458b8f636af623d2ead5` |
| `projects/chirality-app-v4/app/src-tauri/resources/attachments/manifest.json` | `332688c5fccd2e0612f26c2cdbc7363f28661f157129ac7a106c0b5750edd247` |
| `projects/chirality-app-v4/app/src-tauri/resources/catalog_adapter/manifest.json` | `550d906b30a8c9a131bd548de2f8786385e9cbc0a8b0b32853fd7755ec6de0c4` |
| `projects/chirality-app-v4/app/src-tauri/resources/external_trace/manifest.json` | `4cb2d92b433ee58e6935ebc36068fe3882c772a5ee56603579740ec3c052774d` |
| `projects/chirality-app-v4/app/src-tauri/resources/external_trace/receiving/manifest.json` | `852ca9b5aebdf2ac7d274ebad54481e344225c4753ae2cf79035132a82d1007b` |
| `projects/chirality-app-v4/app/src-tauri/resources/external_trace/regressions/manifest.json` | `1173508bf005d2ce6036e525a2cf63dd2e68a5b753e01605678e4f25c56eff93` |
| `projects/chirality-app-v4/app/src-tauri/resources/hosting/manifest.json` | `b025c3d783b99266ba2826c4a03a1b5fddf8b495f34eb4ddf5c805c024648096` |
| `projects/chirality-app-v4/app/src-tauri/resources/policy_standing/manifest.json` | `c7f7f1c9ee384b5904a5c51491752d37fd57b3cc673dcfd9af7673cd7e82a640` |
| `projects/chirality-app-v4/app/src-tauri/resources/runtime_core/manifest.json` | `36e5e8f532667a1bc7c6a9e5c3d322b06e09c9bc9b8166c54fc02dac513b8cfc` |
| `projects/chirality-app-v4/app/src-tauri/resources/instructions/SOURCE_MAP.json` | `ca3ff9b483d70a3c4dbe818c520cc3a16c750cbf81aa5bee88460c09c7f92f82` |
| `projects/chirality-app-v4/app/src-tauri/resources/workflow_role/SOURCE_MAP.json` | `803df210394c61fa1223ec8efc618431a68028e53ea43294212855dcb61f33f7` |
| `projects/chirality-app-v4/app/src-tauri/resources/external_trace/exam.result-record.valid.examples.json` | `fcbd53d8936b9c73d8177a403795e438aab9dbc5e71b32f7f87ef4b121bec72e` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/hosting.client-request-record.schema.json` | `3264b5b31514f1477b48560d232f50edc3c00db5207b97557a0d4e7e0b9fa5a5` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/hosting.server-request-entry.schema.json` | `b295fc5891e3fee8435f1293f731a9939d43383ce80ec87b8a993f35b0adce7f` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/recovery.app-ledger-entry.schema.json` | `3f1d7f27f68a523c459ebcb9ce3dcd40a5de54fc4b9b16d20fd4e6b4c3f05c67` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-03_Native plans, tools and delegation views/Design/npt.plan-revision.schema.json` | `12395230e57d9397fca5d02fb011c70b6c9990992c459748f6daf8b8474b8a16` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-03_Native plans, tools and delegation views/Design/prototype/fixtures/native/plans.jsonl` | `08327e8d5f1f965a2b504665af4c83fb61cb0866614b638a2f9186dbf23b02ae` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/aac.capture-evidence.example.valid.json` | `e086bdafb4d24c13f24e8fecee151bd803633294adc51d43ed16fe8523528da4` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/aac.capture-evidence.schema.json` | `4405a1228e5982d948eb82776aaaf54d966d4305f8829a656473a523ad1ca4ba` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/aac.offer.example.valid.json` | `f80957322793888d13e0c48c2cc312f91ff38b7cf6c60b622a103cb8cf7e967f` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/aac.offer.schema.json` | `f2091fcf2583b6863370ba51d86f4c8671dbae5bbd6fe0e39046154d98c7d066` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/nir.attachment-supply-record.example.invalid.json` | `835cd85dcbed2f7c176e3750f430e75a183495a88d9fd2bf19302f097ef87da6` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/nir.attachment-supply-record.example.valid.json` | `ac5f161cf90a3d890dcc9dd49574b65ec8f793b3fb7a7dba99b42a78e948bbe3` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/nir.attachment-supply-record.schema.json` | `6562b8efacb75a3814f59b5918cdac9210e968f008059544864fa234e550a8c1` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-05_Native OAuth-sign-in, API-key and local-provider access/Design/access.conversation-selection.schema.json` | `e40fec6a0c0915f2842c00ae39761fa320fd83924cf56258abf63f1ffb1c0fed` |
| `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-01_Portable workflow contract and shared allocation/Design/workflow-declaration.invalid.example.json` | `16cf6486474570430d63de4e01a80c6dbe76237c72228c86c5462d5bc1d229f2` |
| `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-01_Portable workflow contract and shared allocation/Design/workflow-declaration.schema.json` | `bb01a004e40da89e20183876774afc2308a921376eee4cf75e0c66fcdb405337` |
| `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-01_Portable workflow contract and shared allocation/Design/workflow-declaration.valid.example.json` | `b484a5a2210a63f049be684799f21003d7d1001819b12c7edc27a44785b1e187` |
| `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-02_Workflow-making workspace and registration/Design/workspace-registration.schema.json` | `cfd6d3e252b72247d8e1ad0ced3b43b119c5785935002d493407757bd57066e9` |
| `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/Design/checkpoint-record-entries.schema.json` | `00d5203a2fa9d099b25f2f8da5732f2d869a18fd0846ebe33d25c9ae2ae135d3` |
| `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/Design/compatibility-report.schema.json` | `8e2bf4a257422fcc6184bc9222ed9e0d1d27be7a2807a3dd5ebe7d5e5bcafd24` |
| `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/Design/decision-package-file.example.valid.json` | `3ea08ff575698e769784e0c4788a21c01be81020ad0a3c0534114f5c87895fbe` |
| `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-04_Additive role selection and supply/Design/role-limit-account.schema.json` | `69ea538ccc2ac8a1763878427d7cce796cd3cc3e094c8aceee9c71e454b7f84c` |
| `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-04_Additive role selection and supply/Design/role-supply-record.schema.json` | `eaa6e682aa6077f8ab89858e3f52d0e91d7117b5c03ea4c68c72ec0d95c5f639` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/Design/catalog.example-invalid-2.json` | `c0816805795467a94bc470acf9361b673b1e4ec3b1b134fbd33ae3e96e71719b` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/Design/catalog.example-invalid-3.json` | `9eea2e878d0d7089f565d97b2e849a88370f48def08252b900e2d17e0f1f58a2` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/Design/catalog.example-invalid.json` | `cf3ac4ded0eb4146ee4b03777f485a7559c934232ea11bfec27f08bf16622fd9` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/Design/catalog.example-valid-2.json` | `c70a271019b5f8cca7a3ad78ea03d0dce3ae60c158f1e62af5adbe0755cc6ecf` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/Design/catalog.example-valid.json` | `1d8204017e4ab326fd1c3462c1f7ab1c2d6fec297137624d9001677306a2e12d` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/Design/catalog.schema.json` | `24d7db75d66f5119ad97957166f0e65287ffa7b510c5fb360c26fba00fccd99d` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/Design/edition_change_event.example-invalid.json` | `6b457001e93c45b6d8c9b1eb10595b15742f36f9f464b251caf6370eb26933da` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/Design/edition_change_event.example-valid.json` | `19c179c6c14201443661e3c8bb4f0b829d12d70fa151baf7dfdf6a83a6497d8d` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/Design/edition_change_event.schema.json` | `c0244a57a696d9b48e356788c26602b0f029b892bb80233b15741e3641c89759` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/Design/read_result.example-invalid-2.json` | `2fc0db909ba9cf124694652568d076980f1f4c8d614aa195a4dfbb427709ea11` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/Design/read_result.example-invalid.json` | `dd3bfc0b6b45daa26c117ccc87e79c0d781c862a9987eb20519e0ac402528739` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/Design/read_result.example-valid-2.json` | `62c8fb47a4d89acaa518a9f103ab6ce10d702a7d4ba3b95bab271b273036c60a` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/Design/read_result.example-valid-3.json` | `bb2f4fa362e04443b99a24fcaff75ac3ead9b48a136346473b55bb5e8af4a0e3` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/Design/read_result.example-valid.json` | `e8e4ecf32df9de0e05944acf014c13aa5f3b1e0405ee0ed39069655519f0d278` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/Design/read_result.schema.json` | `5f71d7184bd312af188b5200715d784b1d5d2aacf90758574ad4d1dfe9786c1e` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-02_Proposal, validation and outcome contract/Design/proposal.example-invalid.json` | `4627d69722b0fcfeb24938ba04ff2f6d4192c7ae99f1e48c6b11562320ba7ef7` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-02_Proposal, validation and outcome contract/Design/proposal.example-valid.json` | `1c1227936bf742402e23ce6153d8b4b5c235568073789135d759d4de2432a8d6` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-02_Proposal, validation and outcome contract/Design/proposal.schema.json` | `2c81bab4a72539722fab630fe8c5b65d0822c2682fbab489c44e842e02bdf07e` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-02_Proposal, validation and outcome contract/Design/proposal_state.example-invalid-2.json` | `ff7e84851d3e379e66b63856f8c0f20342121d8da309b508e5e318d0da94f7fd` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-02_Proposal, validation and outcome contract/Design/proposal_state.example-invalid.json` | `c8c5e7aa178e797f3da9d036b92b24cf49a1ed2f4c2a0b804b67dce7d2f16131` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-02_Proposal, validation and outcome contract/Design/proposal_state.example-valid-2.json` | `a39279c98eba5c7e9e389e40657afc1124142db79b7986a213e637817daffd3f` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-02_Proposal, validation and outcome contract/Design/proposal_state.example-valid-3.json` | `e3ef15f7735f416e0b3c69e675fb1487f0bc8f3f60e6cb2eda508a84704978f1` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-02_Proposal, validation and outcome contract/Design/proposal_state.example-valid.json` | `6b369692c11ca111f34fed8c31734dbc73dc1b5fcdace9ebae36acce873cf520` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-02_Proposal, validation and outcome contract/Design/proposal_state.schema.json` | `222de733c7dfa77f80cacb4365bd60dc6b4ed61ffbfad68848f0171874d1820f` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/Design/channel_status.example-invalid.json` | `be5413548efb0390dde5fe5bb00e2406413563c47c4c6b675f6983c16207c5f3` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/Design/channel_status.example-valid.json` | `06d201d1c0bb22dded889d4f394a3892674c35241385fa0f9e413bd34698b402` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/Design/channel_status.schema.json` | `49f3475c10b4d410acba975526e41737e2946180117d01f47b6644f56692d7f0` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/Design/checkpoint_observation.example-invalid.json` | `dd519fe6fe73a0fc7ec54f794d989de6c0e40bb6df1c759878ce57ffe9106f35` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/Design/checkpoint_observation.example-valid-2.json` | `20f92dbd98e7de1e6fd1968903484b4ff4543dfca201ffdbb015e5a104aba6fa` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/Design/checkpoint_observation.example-valid.json` | `69a033a7323c221775c00fb713a526861014652c74aa1c7f882ecdcd2d541cc0` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/Design/checkpoint_observation.schema.json` | `5d17aa548789b9143d6de5f27b9fe9fd1903baad46b73389d2b9a31d20ff1ed4` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/Design/external_dispatch_record.example-invalid.json` | `2c4c897366989371e36e393c9bf4deb8709f01b46f610ac5ae1a602f40360ba0` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/Design/external_dispatch_record.example-valid-2.json` | `8e2240355766706a21eb53950195dc7aec90ff1d0f0577e8fedf3d3c4247d846` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/Design/external_dispatch_record.example-valid.json` | `69b496d5f1c0d39a1493cdfea11f927597c1f0ebc1f2fd5dce95aa065295c9b3` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/Design/external_dispatch_record.schema.json` | `726d8787d1b9b2792a04eb5581d893c2faa76edefc622c0d18990a5225daa087` |
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-01_Operation-policy and human-act distinctions/Design/ACT_POLICY_CLASS_RECORD.invalid.examples.json` | `39af33974ba7253de85274b059d43ffd159f7f7629bfd42344ac06ab4e5b4a72` |
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-01_Operation-policy and human-act distinctions/Design/ACT_POLICY_CLASS_RECORD.schema.json` | `694a284f48155ab7a7d0e24d47ec809a06ec3a909dbb104a28374164d3f6cb7e` |
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-01_Operation-policy and human-act distinctions/Design/ACT_POLICY_CLASS_RECORD.valid.example.json` | `160722582d424c89b9c8bddce1b7cf278030ec8d5634f1ace6b4f1da7fd12f8a` |
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-02_Visible autonomy and result standing/Design/AS_SETTINGS_IN.invalid.examples.json` | `8ae502e1639832c518036a4243818624c3a87842b7f771b894c163c53d721eb8` |
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-02_Visible autonomy and result standing/Design/AS_SETTINGS_IN.schema.json` | `206045da42dae052621893c8e25487066b36ef8e8a3a7a28414b02137be07d62` |
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-02_Visible autonomy and result standing/Design/AS_SETTINGS_IN.valid.examples.json` | `58b58c81da2faba99a10109465f1d338d3636bd3c528426f38bd70e9eab01acb` |
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/RS_RECORD.schema.json` | `c94dbd441388f52de4dbce5b79859abf2a07223bf236f209eedcb6aee548e3e6` |
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/RS_RECORD.valid.act-log.example.jsonl` | `b34997bb5168b747a9fe0c91ffa2ca8f5708c518eb1844331b65b294d3895e0a` |
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/RS_RECORD.valid.app-chained-run.example.jsonl` | `eb39c986da31805136feec0f75f5daf0a62a3776708a9425665c95dad14559ce` |
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/RS_RECORD.valid.app-run.example.jsonl` | `cb9a8acf23733be0fd996d9162bb8a0ceb2d0e5344236500d45912eda7805e3e` |
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/RS_RECORD.valid.host-destinations.example.jsonl` | `0c7a79b213430aa740e5198de8ece9f39a3165f0b6f0f83cd7377c912b096688` |
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/RS_RECORD.valid.host-run.example.jsonl` | `b990fc7ea64e7931c7315a58145e2d5daeeb4a3b72d5266216d0467602ad376f` |
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/RS_RECORD.valid.run-not-started.example.jsonl` | `79cbb8efe8cf8eaf111e3c845fa33af915125a547f2779027b72c0012d98d14b` |
| `projects/chirality-app-v4/execution/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-01_Minimal-loop and model receiving contract/Design/LOOP_DESTINATION_REQUEST.example.invalid.json` | `5ecaf92eeb33b7098356a931c590319a636b3c4a2a80e9b99c626f6587d553ea` |
| `projects/chirality-app-v4/execution/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-01_Minimal-loop and model receiving contract/Design/LOOP_DESTINATION_REQUEST.example.valid.json` | `f3b70593fe6b2b2856bed513fdf9ae5894ce82da73f09b4adb847085465cc674` |
| `projects/chirality-app-v4/execution/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-01_Minimal-loop and model receiving contract/Design/LOOP_DESTINATION_REQUEST.schema.json` | `7b70146bd7a48b8691e132063447b4a9664db5b16135862d2b662e8cc516ac90` |
| `projects/chirality-app-v4/execution/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-01_Minimal-loop and model receiving contract/Design/LOOP_TOOL_CALL.example.invalid.json` | `a972c1626fafa2a3c0aadb1861ae1805a0efcfe7450f126d032f001ae3dfe039` |
| `projects/chirality-app-v4/execution/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-01_Minimal-loop and model receiving contract/Design/LOOP_TOOL_CALL.example.valid.json` | `27be3288c3de8454a4d0aca8e2571f463aa47a7d8766150a19e85c66c180abf6` |
| `projects/chirality-app-v4/execution/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-01_Minimal-loop and model receiving contract/Design/LOOP_TOOL_CALL.schema.json` | `8cb7c31598c068604da315800b4db7c4ce33537cb618efe144eb895ce4867c5d` |
| `projects/chirality-app-v4/execution/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-02_Host panel and shared interaction receiving/Design/PANEL_RETURN_INPUT.example.invalid.json` | `126c3b447036d333595f8975ddd07422945966d796765effdfdade11fde5ca53` |
| `projects/chirality-app-v4/execution/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-02_Host panel and shared interaction receiving/Design/PANEL_RETURN_INPUT.example.valid.json` | `b21cce2785aee194c0bfda7f8dcb5ba2de27d1620ca10b6ac6af57a114fcf714` |
| `projects/chirality-app-v4/execution/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-02_Host panel and shared interaction receiving/Design/PANEL_RETURN_INPUT.schema.json` | `c0f7cc5d5170005a0c0fb0bca247a60ed5aa385c88b64bfc1d50a2d2cc7bc18a` |
| `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-01_Candidate examination infrastructure and evidence protocol/Design/exam.result-record.invalid.examples.json` | `c4f15c47ac7d5f4345272664ae979c26e1086eb2a946c9d99f6afc3ddaee8772` |
| `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-01_Candidate examination infrastructure and evidence protocol/Design/exam.result-record.rule-violations.examples.json` | `55bc7c85bb61af3d50f170b5af47b6069631bb6ba981c943f20e84e4d03390fe` |
| `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-01_Candidate examination infrastructure and evidence protocol/Design/exam.result-record.schema.json` | `f7871c96cef25bb974aea73feca009ed3caf843db5077d80612f13b130af2081` |
| `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-01_Candidate examination infrastructure and evidence protocol/Design/exam.result-record.valid.examples.json` | `fcbd53d8936b9c73d8177a403795e438aab9dbc5e71b32f7f87ef4b121bec72e` |
| `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-09_External control and catalog-extension trace/Design/xt-result-record.example.invalid.json` | `e240b41f60a103246992c93c0650e8ae0a25a9eb742db5c3c257914f87f83f48` |
| `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-09_External control and catalog-extension trace/Design/xt-result-record.example.valid.json` | `d3d77934d739fbf4afbd3b05c2f98b26aaaf6436e785c2b525db1949aabcc2f8` |
| `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-09_External control and catalog-extension trace/Design/xt-result-record.schema.json` | `3b0ff2bbd1da8dab61147218b6c512146b58b4dc13eea6a2b1c60f7c5b697b4b` |
| `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-09_External control and catalog-extension trace/Design/xt-work-account.example.invalid.json` | `bdc743331c8d3ba72b518a5bb63ee4db2de28841bca1fa853c2e0b20a771eae4` |
| `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-09_External control and catalog-extension trace/Design/xt-work-account.example.valid.json` | `5aa22b7b4ec84a2d46d8a2efbbffb0ca8b9e3e382e6d9f6ba6a2783f01be0380` |
| `projects/chirality-app-v4/execution/PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-09_External control and catalog-extension trace/Design/xt-work-account.schema.json` | `ffe112712ce9a1e4383f37c0f2614496dda709f4bb6fe5f92230403db332a2b2` |
