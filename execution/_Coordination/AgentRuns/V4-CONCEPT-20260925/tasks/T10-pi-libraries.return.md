# Pi libraries (pi-ai, pi-agent-core) for a Tauri webview host: research return (T-task, read-only)

**Basis.** The Pi repo `earendil-works/pi` was read at main `d6af72e1857cfb10b41d8ff8e69f0d72b4cf6d31` (2026-09-25). All packages there are at **0.87.1**. I cite it below as `pi@d6af72e`. The Chirality repo was read at `bf90ffc4dbd52bab8592dd5cc7bde3cc20f0eb6b` (`REPO_ROOT@bf90ffc`). I also used npm registry metadata (read-only JSON), GitHub releases, issues and PRs, and one blog post. I wrote, installed and executed nothing, and my session made no repo changes.

---

## 1. Does `pi-agent-core` run in a browser or webview?

**Conclusion: it runs in a browser as-is from its root entry. The Node-only code sits behind separate subpath exports.** A host imports `@earendil-works/pi-agent-core` (root) and must not import `./node`, `./harness/env/nodejs` or `./experimental/pico3`.

**Package shape** [repo source] (`packages/agent/package.json@d6af72e`):
- Exports: `.`, `./node`, `./harness/context`, `./experimental/pico3`, `./harness/env/nodejs`, `./harness/runtime/reducer`, `./harness/session`, `./harness/session/testing`.
- There is no `"browser"` condition. Every export offers only `types` and `import`.
- `engines: node >=22.19.0`. That is advisory and bundlers ignore it.
- Dependencies are pinned exactly: `@earendil-works/chord`, `pi-ai`, `pi-telemetry` (all ^0.87.1), `diff 8.0.4`, `ignore 7.0.8`, `typebox 1.3.27`, `yaml 2.9.0`.

**Where the `node:` imports are** [repo source]. I batch-read all 107 non-test files in `packages/agent/src`. `node:` imports appear only in:
- `harness/env/nodejs.ts` (child_process, crypto, fs, os, path, url; plus `process.*`). It is reachable only via `./node` and `./harness/env/nodejs`.
- `harness/pico3/bash.ts` and `harness/pico3/jsonl.ts`. They are reachable only via `./experimental/pico3`.
- The root `src/index.ts` never re-exports `env/nodejs` or `pico3`.
- The harness tools (`tools/bash.ts`, `edit.ts`, `read.ts`, `write.ts`) and JSONL session I/O (`session/jsonl/io.ts`) go through an abstract `ExecutionEnv` / `FileSystem` interface.
- `utils/truncate.ts` feature-detects `globalThis.Buffer` and falls back to pure JS.

**`@earendil-works/chord`** [repo source] (`packages/chord@d6af72e`):
- Its description is "Application composition runtime for services, replicated state, RPC, and plugins" (facet services, JSON delta/replication, context/cancellation). The agent README says the facet-service primitives live there and that "The agent core does not export the service runtime."
- Its only runtime dependency is `esbuild 0.28.2`, and `sideEffects: false`.
- `esbuild` and all `node:` imports (crypto, fs/promises, module, os, path, url, **vm**) are confined to `src/node/*`, exposed via the `./node` and `./bundler` subpaths.
- chord's root, `./context` and `./delta` entries have no Node imports.
- The agent root imports chord only as types plus one value import from `@earendil-works/chord/context`.
- **Install-time caveat:** esbuild still gets installed. npm metadata shows 26 optional platform binaries and a `postinstall: node install.js` script, although none of it is bundled into browser output.

**Other dependencies** [npm registry metadata]:
- `diff@8.0.4`: no dependencies; `browser: ./dist/diff.js`.
- `yaml@2.9.0`: no dependencies; has a `browser` map.
- `ignore@7.0.8`: no dependencies. The library's master source guards `process` with `typeof process !== 'undefined'`; I read `kaelzhang/node-ignore@3a12e09` master, not the 7.0.8 tag.
- `typebox@1.3.27`: no dependencies; ESM only.
- `yaml` and `ignore` are used only by `harness/skills.ts` and `prompt-templates.ts`; `diff` only by `harness/tools/edit-diff.ts`.

**Continuous-integration evidence** [repo source]:
- `scripts/check-browser-smoke.mjs@d6af72e` bundles `scripts/browser-smoke-entry.ts` with esbuild `platform: "browser"`. That entry imports the pi-agent-core root (`Agent`, `streamProxy`, truncation and skill helpers, and more), pi-ai and pi-ai/compat. The script's stated purpose is to "catch accidental Node-only runtime imports in browser-facing package exports."
- A second bundle, `agent-treeshake-smoke-entry.ts`, asserts that an `Agent` + `createModels()` + single-provider bundle excludes `compat.ts`, `providers/all.ts` and every SDK except the chosen one.
- `npm run check` includes `check:browser-smoke`, and `.github/workflows/ci.yml` runs `npm run check` on main and on PRs.
- This check proves that the bundle resolves. It does not execute anything in a browser.

**Documentation** [docs]:
- The agent README Quick Start is runtime-neutral. It has a "Proxy Usage: For browser apps that proxy through a backend" section.
- It also states that the SQLite backend was split into `@earendil-works/pi-session-backend-sqlite-node` "so the core package does not pull in runtime builtins."

**History** [repo source]: the in-repo browser consumer `web-ui` was removed in `b141e1fa2460868686ffd19c5d4ced743eee6c24` (2026-05-20). npm `@earendil-works/pi-web-ui` stopped at 0.75.3. Today no first-party package exercises agent-core in a browser at runtime; only the smoke bundle does.

**What a host would do** [inference]:
- Use the root `Agent` or `agentLoop` with an explicit `streamFn` and host-generated `AgentTool`s.
- Avoid the `./node` and `pico3` subpaths.
- If it uses `AgentHarness`, it supplies its own `ExecutionEnv` / `FileSystem`, for example backed by Tauri commands.
- If it ever imported chord's `./node` or `./bundler`, or the harness `NodeExecutionEnv`, those parts would have to run in a Node sidecar. That would change the architecture.

## 2. `pi-ai` in the browser

**Documented support** [docs] (`packages/ai/README.md@d6af72e` §Browser Usage, §Bundling):
- "The library supports browser environments. The core entrypoint and provider factories are side-effect free and bundle cleanly."
- Keys must be passed explicitly or through an injected `CredentialStore`.
- Limits: Bedrock (`bedrock-converse-stream`) "is not supported in browser environments". "OAuth login flows are Node-only", and they are lazy-loaded behind bundler-opaque imports.
- The root entry imports no catalogs, provider factories or SDKs. `providers/<id>` pulls one catalog plus a lazy API wrapper. `compat` should be avoided.

**Source confirmation** [repo source]:
- Node access is guarded or deferred: `env-api-keys.ts` ("NEVER convert to top-level imports - breaks browser/Vite builds"), `utils/pi-user-agent.ts` (`process.getBuiltinModule`; returns `"pi (browser)"`), and the OAuth modules (dynamic `node:http` / `node:crypto`).
- The Bedrock implementation (`@smithy/node-http-handler`, `http-proxy-agent`, `https-proxy-agent`) loads only through an opaque import in `bedrock-converse-stream.lazy.ts`.
- The OpenAI and Anthropic clients are built with `dangerouslyAllowBrowser: true` (`api/openai-completions.ts:788-794`, `api/openai-responses.ts:275-278`, `api/anthropic-messages.ts:928-992`). Anthropic also sends `anthropic-dangerous-direct-browser-access`.
- **Install footprint:** pi-ai's `dependencies` include `@aws-sdk/client-bedrock-runtime`, `@google/genai`, `openai`, `@anthropic-ai/sdk`, the proxy agents and `@smithy/node-http-handler`. They are installed even when they are not bundled.

**Relevant API implementations** [docs + repo source]: under `@earendil-works/pi-ai/api/<id>`:
- `openai-completions` (Chat Completions)
- `openai-responses` (Responses)
- `anthropic-messages`
- also `azure-openai-responses`, `openai-codex-responses`, Google, Mistral and Bedrock.

Custom providers are built with `createProvider({ id, baseUrl, auth, models, api: openAICompletionsApi() })`. Mixed-API providers use a map keyed by `model.api`. Local-server compatibility flags include `compat.supportsDeveloperRole: false` and `supportsReasoningEffort: false`, which the README says "commonly applies to Ollama, vLLM, SGLang".

**Per-request `fetch` injection** [release notes]: added in 0.83.0 ("Added per-request `fetch` injection for supported text and image provider transports"). `types.ts:139-142` documents it as defaulting to `globalThis.fetch`. `openai-completions` passes it to the OpenAI client.

**Keyless local providers** are documented but not usable as written:
- [docs] The README example uses `auth: { apiKey: { resolve: async () => ({ auth: {} }) } }` and says "keyless local servers resolve as configured with no key."
- [repo source] That only marks the provider as configured. `openai-completions.ts:82-86` (`getClientApiKey`) throws `No API key for provider: <id>` unless an `apiKey` or an `authorization` header is present. Tests assert this for direct calls (`test/pre-generation-error.test.ts`). Under `Models` the error surfaces as a stream error (`api/lazy.ts`).
- [docs] The coding-agent's own guidance uses a dummy key: "The dummy key makes the model available to Pi; Ollama ignores it" (`packages/coding-agent/docs/models.md:55-64`).
- [issue/PR] A first-class `keyless` flag (#4498) was closed without merging.
- For oMLX this does not matter: the prior integration sent a Bearer credential.

## 3. Data behaviour (network calls beyond the model endpoint)

**Finding: in pi-ai core, pi-agent-core and pi-telemetry, nothing sends data by default to hosts other than the configured endpoint.** [repo source]

- I scanned all non-catalog files in `packages/ai/src` and `packages/telemetry/src` for `fetch(`, URLs, `WebSocket(`, `sendBeacon` and XHR.
  - Fixed-host fetches exist only in the OAuth login and refresh modules (claude.ai, auth.openai.com, openrouter.ai, auth.x.ai, auth.kimi.com, auth.meta.com, GitHub Copilot, Radius). These run only on explicit login or refresh.
  - The only dynamic-catalog fetch is the Radius provider (`providers/radius-config.ts:87` → `<gateway>/v1/config`), used when that provider is registered and refreshed with auth.
  - Built-in catalogs are JSON generated at build time and shipped in `dist/providers/data`.
  - `Models.refresh()` defaults to `allowNetwork: true`, but "Static built-in providers are no-ops for `refresh()`" [docs]. A custom provider without `fetchModels` makes no catalog calls.
- **pi-agent-core:** the only `fetch` is `streamProxy` (`proxy.ts:160`) to a caller-supplied `proxyUrl`.
- **pi-telemetry** [docs + repo source]: "no exporter, global current-span state, or dependency on a telemetry backend". It has zero dependencies and uses `NOOP_TELEMETRY_CONTEXT` by default.
- **Headers to the configured endpoint** [repo source]: `User-Agent: pi (<os>)` or `pi (browser)`. The OpenAI SDK also adds its own `x-stainless-*` headers [inference, from standard SDK behaviour]. When `compat.sendSessionAffinityHeaders` is set, session IDs are sent as `x-session-affinity` and similar headers.
- **pi-coding-agent (not proposed for the webview)** [repo source]: it can overlay catalogs from `https://pi.dev/api/models/providers/<id>` (`core/remote-catalog-provider.ts:13,105`). This happens only when `allowModelNetwork === true` (default false) and `PI_OFFLINE` is unset (`core/model-runtime.ts:96-97,223`).
- **Session sharing** [docs]: the root README's session-sharing request uses a separate opt-in tool (`badlogic/pi-share-hf`).
- **Session backends:** `sqlite-node` uses `node:sqlite` and is Node-only by design. I found no network code in it.

## 4. Stability and cadence

**Releases over the last four months** [release notes]: 41 GitHub releases from 0.76.0 (2026-05-27) to 0.87.1 (2026-09-22), spanning 12 minor versions:
- 0.76.0 (05-27), 0.77.0 (05-28), 0.78.0 (05-29), 0.78.1 (06-04)
- 0.79.0–0.79.10 (06-08 to 06-22)
- 0.80.0–0.80.10 (06-23 to 07-16)
- 0.81.0 and 0.81.1 (07-21)
- 0.82.0 (07-24), 0.82.1 (07-25)
- 0.83.0 (07-29)
- 0.84.0–0.84.4 (08-06 to 08-28)
- 0.85.0 (09-04), 0.85.1 (09-05)
- 0.86.0 (09-19), 0.86.1 (09-20)
- 0.87.0 (09-21), 0.87.1 (09-22)

**Stated policy** [repo source]:
- `.pi/skills/release.md@d6af72e`: "Lockstep versioning: all packages share one version… `patch` = fixes + additions, `minor` = breaking changes. No major releases."
- `AGENTS.md:26`: "Do not preserve backward compatibility unless the user asks for it."
- Direct external dependencies are pinned exactly, and `.npmrc` sets `min-release-age=2` (root README, Supply-chain hardening).
- There is no formal semver or 1.0 commitment.

**Breaking changes in pi-agent-core** [release notes] (`packages/agent/CHANGELOG.md@d6af72e`):
- 0.77.0: `model_select` / `thinking_level_select` events renamed.
- 0.80.0: `AgentHarnessOptions.models` required as the only auth path; `getApiKeyAndHeaders` removed; `compact()` and summaries take `Models`; `/base` entry removed.
- 0.81.0: `SessionStorage` contract changed; `uuidv7` moved to pi-ai; the `Agent` stream function became required (no default).
- 0.82.0: `AgentHarness` uses `toolContext` and `AgentHarnessTool` instead of `ExecutionEnv`.
- 0.84.0: v4 lane-based `Session` / `SessionStorage` / `SessionRepo`; legacy JSONL and in-memory repos removed; `FileSystem.renameFile()` required.
- **0.84.4 (a patch):** `prepareNextTurn` semantics changed.
- 0.87.0: `shouldStopAfterTurn` removed in favour of `finishTurn`.

**Breaking changes in pi-ai** [release notes] (`packages/ai/CHANGELOG.md@d6af72e`):
- 0.78.0: direct stream functions require `apiKey`.
- 0.80.0: root became core-only and side-effect-free; old global API moved to `/compat`; `Provider` → `ProviderId`; API modules moved to `api/*`; `/base` removed.
- **0.80.7 (patch):** `sendSessionIdHeader` removed.
- **0.80.8 (patch):** provider-scoped auth APIs; OAuth registry removed; `Models` request contract changed.
- 0.82.0: `getBuiltinModelDataUrl` → `getBuiltinModelDataGeneratedAt`.
- 0.83.0: TypeBox 1.3.7 (deprecated APIs removed).
- 0.84.0: `ModelsStreamTransforms` → `ModelsRequestTransforms`; abort signals required; `refreshModels` publish transaction.
- **0.84.3 (patch):** `GoogleThinkingLevel` renamed.
- 0.85.0: Cloudflare binding fetch replaced.
- **0.86.0:** `StreamFunction` input changed from `Context` to `TranscriptContext` (system prompt and tools moved into transcript system messages); `ToolCall.arguments` restricted to JSON values.
- **Unreleased:** image models unified into `Models`.

Breaking changes therefore also land in patch releases (0.80.7, 0.80.8, 0.84.3, 0.84.4), contrary to the stated policy.

**Package renames** [release notes + npm registry]:
- 0.74.0 (2026-05-07): "Updated repository links and package references for the move to `earendil-works/pi-mono` and `@earendil-works/*` package scopes" (coding-agent CHANGELOG). The repo later became `earendil-works/pi`.
- `@mariozechner/pi-ai` stopped at 0.73.1 (2026-05-07), deprecated with "please use @earendil-works/pi-ai instead going forward".
- For consumers this meant changing the package name. Nothing aliases the old scope for library users, although the coding-agent maps old-scope imports for extensions (`core/extensions/loader.ts:105-111`).

## 5. Governance and momentum

- **Ownership** [docs] (blog post of 2026-04-08, `mariozechner.at/posts/2026-04-08-ive-sold-out/`):
  - Mario Zechner joined Earendil, a software company building agent products, and transferred ownership of pi to it.
  - Decisions rest with Zechner, Armin and Colin. The pi name and logo are Earendil trademarks.
  - The MIT core is stated to remain MIT ("non-negotiable").
  - Future tiers are planned: Fair Source features and proprietary enterprise infrastructure.
  - The post anticipated a different npm name than the one that shipped (`@earendil-works/*`).
- **Organisation:** `earendil-works` "Earendil Works", Austria, created 2025-04-16.
- **npm maintainers** of `@earendil-works/pi-ai`: `mitsuhiko`, `badlogic`, `rwachtler`.
- **Contributors** [repo metadata]: 287. By commits: badlogic 3769, mitsuhiko 734, davidbrai 272, christianklotz 201, cristinaponcela 197, vegarsti 158. That is a heavy concentration on one maintainer.
- **Repo** [repo metadata]: created 2025-08-09; about 109k stars and 13.9k forks.
- **Activity since 2026-05-26** [repo metadata]: 2,267 commits; 3,498 issues created (about 1,033 in the last 30 days); 1,431 PRs opened, 440 merged. Currently 160 issues and 66 PRs are open.
- **Contribution policy** [docs] (`CONTRIBUTING.md@d6af72e`):
  - Issues and PRs from new contributors are auto-closed. Maintainers review them daily and grant `lgtmi` or `lgtm`.
  - PRs require prior `lgtm`.
  - "PRs that bloat the core will likely be rejected."
  - Maintainers write the changelog.
  - Longer-term plans are published as RFCs at rfc.earendil.com.

## 6. Tool calling with local models

**Mechanics** [repo source + docs]:
- Streamed arguments are parsed with `parseStreamingJson` (`utils/json-parse.ts:104-124`): JSON repair, then the `partial-json` library, then a fallback to `{}`.
- At `toolcall_end`, the "arguments [are] complete (but not yet validated)" [docs].
- `agent-loop.ts:690-768` runs an optional `prepareArguments` shim, then `validateToolArguments`.
- Validation (`utils/validation.ts`) does the following:
  - normalises optional nulls;
  - runs `Value.Convert` coercion;
  - coerces plain (non-TypeBox) JSON Schemas via `coerceWithJsonSchema`, so host-generated JSON-Schema tools are supported;
  - validates with the TypeBox `Compile` JIT.
- Failures become `isError: true` tool results that the model can retry.
- **Content-Security-Policy note** [docs]: the TypeBox README (`sinclairzx81/typebox@e0ac8ce`) says its compiler "offers automatic fallback to dynamic validation in JIT restricted environments".

**Known weaknesses, mostly reported against OpenAI-compatible or local servers** [issue/PR]:
- **#8501 and #9897:** truncated streams finalise partial arguments. Both were auto-closed; #9897 got a maintainer question.
- **#8858:** markdown-fenced `arguments` silently degrade to `{}`. Auto-closed.
- **#6635:** PR to recover tool calls that local servers (Ollama, LM Studio) emit in `content`. Not merged.
- **#9974:** llama.cpp Responses stream led to duplicated or corrupted tool calls being executed. Closed; attributed to llama.cpp's partial Responses implementation.
- **#9265:** O(n²) re-parsing of arguments on every delta "freezes the event loop". Open; fix PR #9461 is open.
- **#9569:** coercion of JSON-encoded object and array arguments. Open PR.
- **#9508:** OpenAI-specific fields, roles and auth sent to compatible providers cause 400/422 errors. Open.
- **#9216:** Ollama "terminated" errors, reported as a 0.84 to 0.85 regression. Open.
- **#3357:** first-class llama.cpp support landed in main in July 2026. For oMLX, a commenter suggested an `openai-completions` entry in `models.json`.

**Missing documentation** [inference]: I found no Pi documentation that quantifies tool-calling reliability for oMLX, Ollama or LM Studio. `docs/llama-cpp.md` notes that `--jinja` enables tool calling.

## 7. Chirality's prior integration and changes since 0.82.0

**What it was** [repo source] (`REPO_ROOT@bf90ffc`, `projects/chirality-runtime/packages/engine-pi-omlx`):
- 670 lines across 6 TypeScript files, depending on `@earendil-works/pi-coding-agent` and `pi-ai` pinned to exactly 0.82.0.
- It is Node-only: `node:crypto`, `node:fs`, `node:path`, `Buffer`.
- It used the coding-agent SDK, not agent-core:
  - `createAgentSession`, `ModelRuntime.create({ allowModelNetwork: false, InMemory* stores })`, `SessionManager.inMemory`, `SettingsManager.inMemory`;
  - a `DefaultResourceLoader` with five ambient-discovery disable flags and overrides;
  - `noTools: "all"` plus custom tools.
- It **bypassed pi-ai's transport**: a hand-written non-streaming `streamSimple` posts to `${baseUrl}/chat/completions` (`pi-turn-runtime.ts:184-219`). The reason is in `…/RUNTIME_EXECUTION_2026-09-06/IMPLEMENTATION/PI_BINDING_ASSESSMENT/ASSESSMENT.md`: at 0.82.0 the `openai-completions` client had no per-client fetch override for redirect and host guarding.
- SDK loading was deferred through non-literal dynamic imports to survive CommonJS/ESM bundling (commit `3a6adfc27`).
- Most of the code is Chirality governance: fingerprints, successor admission, and a symlink-safe bounded read tool.
- Development ran from roughly 2026-07-22 to 2026-09-09.
- README lines 128-140 record live client → daemon → Pi → oMLX validation with Pi 0.82.0, and add that there is "no obligation to keep unused implementations compiling".

**Pi changes since 0.82.0 that affect such an integration** [release notes]:
- **0.83.0:** per-request `fetch` injection. This removes the original reason for a custom transport. TypeBox 1.3.7 also removed some APIs.
- **0.84.0:** v4 session model, `renameFile` requirement, `ModelRuntime.setRuntimeApiKey()` options changed, RPC `message_update` no longer cumulative.
- **0.86.0:** `TranscriptContext` input. The prior custom `streamSimple` reads `context.systemPrompt` and `context.tools` (`pi-turn-runtime.ts:59-76,190,194`), so it would need `getCurrentSystemPrompt()` / `getCurrentTools()`. `ToolCall.arguments` must be JSON values.
- **0.87.0:** `shouldStopAfterTurn` removed, `SessionManager` canonical, `TurnEndEvent` / `ContextEditEntry` expanded.
- The agent-core event names the prior mapper relied on (`message_update` with `text_delta`, `message_end`, `tool_execution_end`) are unchanged (`packages/agent/src/types.ts:487-500`).
- [inference] A webview host could not reuse this package. `pi-coding-agent` depends on `undici`, `photon-node`, `cross-spawn`, `proper-lockfile`, `jiti` and others (its `package.json@d6af72e`). The equivalent would be `Agent` from agent-core plus a `createProvider` for oMLX. agent-core's `Agent` has no ambient resource discovery to disable.

---

## Risks and mitigations for a Tauri webview host (all [inference])

1. **API churn.** In four months there were 12 breaking-allowed minor versions, and breaking changes also shipped in patch releases.
   - Pin exact versions, including chord and telemetry, with a lockfile.
   - Keep Pi behind one thin host adapter covering `streamFn`, tools and events.
   - Upgrade deliberately, reading the "Breaking Changes" sections.
   - Use only the stable surface: `Agent`, `createModels`, `createProvider`, and `openai-completions` or `anthropic-messages`.
2. **Keyless and default-auth traps.** `auth: {}` fails at request time in `openai-completions`. Supply a placeholder `apiKey`, or an `authorization` header for oMLX's real key.
3. **CORS and secret exposure.** Webview requests to `http://127.0.0.1` need CORS preflight, because of `content-type` plus SDK and `User-Agent` headers. The key would also sit in JS memory. Inject `fetch` (0.83+) that routes through a Rust-side HTTP command or plugin. That layer can attach the credential, enforce the allowed host and `redirect: manual`, and keep the "only the configured endpoint" rule enforceable outside JS.
4. **Main-thread stalls.** Quadratic argument re-parsing (#9265, open) and TypeBox compilation would share the thread with React and the WASM engine. Run the agent in a Web Worker, or cap tool-argument size and output budgets.
5. **Tool-call reliability with local models.** Silent `{}` or partial arguments, tool calls embedded in `content`, and Responses-API quirks are all possible.
   - Prefer `openai-completions` over Responses for oMLX, matching the prior observed path.
   - Use a `prepareArguments` shim and strict host-side schema validation.
   - Treat `stopReason: "length"` or `"error"` with tool calls as a failure.
   - Keep tools idempotent and read-before-write.
6. **Accidental Node or network imports.** Importing `pi-ai/providers/all`, `compat`, `./node`, `pico3` or chord's `./node` / `./bundler` would pull in catalogs, SDKs or Node code. Add a bundle check, modelled on Pi's `check-browser-smoke.mjs`, that fails on those inputs. Do not register Radius or OAuth providers.
7. **Install footprint and supply chain.** esbuild's postinstall and binaries, plus the AWS, Google, OpenAI and Anthropic SDKs, are installed even when unused. Install with `--ignore-scripts` and audit the lockfile.
8. **Maintainer concentration and a gated contribution process.** Fixes depend on a small core team, and outside reports are auto-closed by default. Expect to carry local shims for local-model issues rather than waiting for upstream.
9. **Content-Security-Policy.** Without `unsafe-eval`, TypeBox falls back to dynamic validation, as documented. Verify under the app's actual CSP.

The load-bearing files are in Pi at `d6af72e`:
- `packages/agent/package.json`, `packages/agent/src/index.ts`
- `packages/chord/package.json`
- `packages/ai/src/api/openai-completions.ts:82-86,788-794`
- `packages/ai/src/utils/json-parse.ts`, `packages/ai/src/utils/validation.ts`
- `scripts/check-browser-smoke.mjs`, `.pi/skills/release.md`

In Chirality at `bf90ffc`: `projects/chirality-runtime/packages/engine-pi-omlx/src/pi-turn-runtime.ts` and `projects/chirality-runtime/README.md:128-140`.
