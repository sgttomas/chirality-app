# T8: T3 Code, local models and fit for Chirality v4

## Basis and boundary

Retrieved 2026-09-25 local time. GitHub timestamps below are UTC and some fall on 2026-09-26.

| Source | Pin |
|---|---|
| pingdotgg/t3code `main` | `a21b42cec478b093cdc50cc2105b5368ea8b3546` (2026-09-26T04:58Z) |
| T3 Orchestrator V2 branch (PR #2829 head) | `70629cdddbe2c29749e8dce588b1828580b2777b` |
| openai/codex `main` | `e72da2b53805894878023d01949a25a082e0a5cb`; latest release `rust-v0.157.1`, 2026-09-26 |
| jundot/omlx `main` | `3f2d07e8dff257119329e0a2e9821df81182f05d` |
| REPO_ROOT | `866897631` |

**Boundary deviation.** To summarise the T3 repository tree, I wrote one temporary file outside REPO_ROOT, in the session scratchpad: `/private/tmp/claude-501/-Users-ryan-ai-env-projects-chirality--claude-worktrees-chirality-app-v4-architecture-9f35c4/ce70a31a-1c4a-4722-bce3-ee5a8e96d1cf/scratchpad/t3tree.txt`. It is a path and size listing from `gh api`, about 23k lines. This breaks the "do not create any local file" instruction. I left it in place because deleting files is also outside my boundary; remove it if wanted. I created or changed nothing else and ran nothing beyond read-only `gh` queries and web reads.

---

## 1. What T3 Code is today

- **Purpose.** The README calls it an "agent harness control surface". AGENTS.md calls it "a minimal GUI for coding agents": a Node WebSocket server wraps provider CLIs and agents and serves web, desktop and mobile clients. It positions itself as an open-source "bring-your-own-subscription" alternative to Claude Desktop, the Codex App, Cursor Glass and Conductor. [repo source: `README.md`, `AGENTS.md` @a21b42c]
- **Owners and backing.**
  - The LICENSE copyright is "T3 Tools Inc." [repo source: `LICENSE`]
  - The Terms of Service name T3 Tools, Inc., San Francisco. [vendor/project docs: https://t3.codes/terms-of-service]
  - t3.tools presents Ping Labs, founded by Theo, Mark and Julius, backed by Y Combinator. Its products include T3 Code, T3 Chat and UploadThing, and it claims more than 280,000 T3 Code developers. [vendor/project docs: https://t3.tools/]
  - The security contact is security@ping.gg, via `.github/SECURITY.md` and https://t3.codes/security-policy. [repo source; issue #9881]
- **License.** First-party code is MIT. [repo source: `LICENSE`, `apps/server/package.json`] The non-MIT parts are vendored read-only references and third-party notices:
  - `.repos/alchemy-effect` is Apache-2.0; `.repos/effect-smol` is MIT.
  - `third-party-licenses.config.json` lists Apache-2.0, BSD-2/3, CC0, ISC and Unlicense components.
  - Provider logos are third-party marks. [repo source; the trademark point is inference]
- **Architecture.** [repo source: `AGENTS.md`, `docs/internals/overview.md`, `pnpm-workspace.yaml`]
  - A pnpm monorepo containing `apps/server` (the `t3` package, v0.0.42), `apps/web` (React/Vite), `apps/desktop` (Electron 44.4.2; productName "T3 Code (Alpha)"), `apps/mobile` (React Native/Expo), `apps/marketing`, `packages/contracts`, `packages/client-runtime`, `packages/shared`, `packages/effect-codex-app-server` (a schema-generated Codex client) and `packages/effect-acp`.
  - The server is heavily built on Effect 4.0.0-rc.115, with TypeScript 7.0.2 and Vite+.
  - The runtime is Node: engines `^22.16 || ^23.11 || >=24.10`, and SQLite uses a Node client (`packages/shared/src/nodeSqliteClient.ts`). Bun is not the runtime; it appears only in dev instructions.
  - The `t3` CLI ships as a Node single-executable binary. [issue #12628]
  - The server is event-sourced (commands → decider → events → projector), and each turn ends with a hidden git-ref checkpoint.
- **Size.** Excluding tests and generated code: `apps/server/src` has about 491 files (6.4 MB), `apps/web/src` about 837 files (7.9 MB) and `apps/mobile/src` about 602 files (3.4 MB). [repo source: tree] That is roughly 0.5M+ lines of TypeScript. [inference]
- **Stability label.** "We are very very early in this project. Expect bugs." Versions are 0.0.x, and the desktop product name is "T3 Code (Alpha)". [repo source]
- **Roadmap.** A new orchestrator ("V2", PR #2829, open since 2026-05-27) is +341,405/−171,218 lines across 1,612 files and 715 commits. It adds a Pi provider, a generic "ACP Registry" provider and an MCP toolkit for cross-provider delegation (`t3_code__delegate_task`, thread launch/send/wait). [issue/PR discussion: PR #2829 body; repo source: V2 tree] In July 2026 a maintainer wrote "we're not adding providers right now. we'll reconsider this after our new orchestrator has shipped". [issue/PR discussion: PR #4355, juliusmarminge 2026-07-23]

## 2. Providers and how each is driven

Six providers are on `main`: Codex, Claude, Cursor, Grok Build, OpenCode and Antigravity. [repo source: README, `apps/server/src/provider/Drivers/`]

| Provider | Transport | Sign-in | Notes |
|---|---|---|---|
| **Codex** | Spawns `codex app-server` over stdio JSON-RPC, using the user's binary. Per-instance "Launch arguments" are appended (`codexLaunchArgs.ts`). Uses `thread/start`, `thread/resume` and `turn/start`. [repo source: `CodexSessionRuntime.ts`] | User's own `codex login`: ChatGPT OAuth or API key. Several accounts via separate `CODEX_HOME`, or a shared home plus a "shadow home" holding a private `auth.json`. [vendor/project docs: `docs/user/providers-codex.md`] | T3 maps its four permission modes to fixed `approvalPolicy`/`sandbox`/`approvalsReviewer` values. Plan mode uses `collaborationMode` with T3-authored `developer_instructions`. Async questions and MCP elicitations are handled, and child threads (subagents) are registered. T3 does not set `developerInstructions`, `baseInstructions`, `modelProvider` or `dynamicTools` at thread start. It recognises `item/tool/call` but registers no dynamic tools. [repo source: `CodexSessionRuntime.ts` L515–565, `CodexAdapter.ts` L846] |
| **Claude** | `@anthropic-ai/claude-agent-sdk` ^0.3.276 `query()`, with `pathToClaudeCodeExecutable` pointing at the user's `claude` binary. [repo source: `ClaudeAdapter.ts` L4901–4955] | User's own `claude auth login` (subscription or Console). Several accounts via `CLAUDE_CONFIG_DIR` per instance. [vendor/project docs: `docs/user/providers-claude.md`] | System prompt is the `claude_code` preset plus an appended T3 runtime block. `settingSources: user, project, local`, so CLAUDE.md, `.claude/skills` and project MCP load natively. `canUseTool` drives approvals, AskUserQuestion and ExitPlanMode (plan mode). Resume and fork use session IDs; subagents are tracked. |
| **Cursor, Grok, Antigravity** | Agent Client Protocol (`packages/effect-acp`, `provider/acp/*`). [repo source] | Cursor: `agent login`. Grok: `grok login`. Antigravity: in-app Google sign-in, or a Gemini API key or Vertex (Agent Platform). [repo source: `settings.ts`] | |
| **OpenCode** | Starts or connects to `opencode serve` via `@opencode-ai/sdk`, using `session.promptAsync`. Locally spawned servers get T3's `t3-code` MCP server added. [issue/PR discussion: #13068 triage] | `opencode auth login`, or OpenCode's own provider config. | An external server URL and password are supported. [vendor/project docs: `docs/user/providers-opencode.md`] |

Cross-cutting behaviour:
- **Instances.** Instances per driver are user-defined slugs. Each has its own environment variables (with a "sensitive" redaction flag), binary path and custom models. [repo source: `packages/contracts/src/providerInstance.ts`, `settings.ts`]
- **Injected T3 MCP server.** T3 injects its own `t3-code` MCP server (preview browser, pull-request and device tools) into Codex through `-c mcp_servers.t3-code.url=…` and into Claude through `mcpServers`. [repo source: `CodexAdapter.ts` L2295–2310, `ClaudeAdapter.ts` L4943]
- **Default permission mode** for new threads is **Full access**. [vendor/project docs: `docs/user/permission-modes.md`]

## 3. Local models (the owner's direct question)

**Short answer:**
- T3 Code has **no native local-model provider or "OSS" switch**. It did not "port" Codex's `--oss` as a feature.
- Local models **do work through pass-through**, because T3 runs the user's own harness binaries with their own configuration.
- Maintainers treat this as a supported path: they triage and accept bugs on it.
- It is not documented for Codex and has open rough edges.
- Theo's reported stance (2026-03-10): "Does T3 Code support local models? No… Locally runnable models are not capable of meaningful engineering work." [third-party: search snippet of https://x.com/theo/status/2031169047119933460; the post itself returned HTTP 402, so it is unverified]

By route:

1. **Codex with a custom `model_providers` entry: works, partially documented, with known bugs.**
   - The Codex instance "Launch arguments" are passed to `codex app-server`. Only `-c`, `--config`, `--enable` and `--disable` are forwarded to `codex exec`, which does T3 text generation. [repo source: `codexLaunchArgs.ts`]
   - A custom `CODEX_HOME` whose `config.toml` sets `model_provider` also works. [issue/PR discussion: #4729]
   - Users run `-c model_provider="cliproxy" -c model_providers.cliproxy.base_url=… env_key=… wire_api="responses"` to local models. [issue/PR discussion: #11873, #13436]
   - Known issues:
     - #13436: replies from custom providers can be truncated. Labelled `accepted`; fix PR #13583 is open.
     - #11873: Usage Limits shows JSON-RPC −32600 warnings.
     - #4729: the provider card shows a false "authentication could not be verified" warning.
     - #644: `-p <profile>` in launch arguments made app-server exit with code 2 (reported 2026-09-12).
   - Local models are added via **Add custom model**, since the model picker comes from `model/list` plus custom models. [repo source: `CodexProvider.ts` L265–490]
   - The docs mention no OpenAI base-URL variable for Codex, and a triager confirmed this path "needs experimenting". [issue/PR discussion: #4941]
2. **Claude Code with `ANTHROPIC_BASE_URL`: documented pattern.**
   - The docs cover OpenRouter and "Other routers/local router" using per-instance env vars `ANTHROPIC_BASE_URL`, `ANTHROPIC_AUTH_TOKEN` and an empty `ANTHROPIC_API_KEY`, each in a separate `CLAUDE_CONFIG_DIR`, plus custom model IDs. [vendor/project docs: `docs/user/providers-claude.md`]
   - Gotcha: T3 sends explicit model slugs, so `ANTHROPIC_DEFAULT_*_MODEL` alias mapping never applies. [issue/PR discussion: #4149, open]
3. **OpenCode's own providers: the maintainer-recommended path.**
   - "you can use opencode to do this now". [issue/PR discussion: #1720, juliusmarminge 2026-04-17]
   - #4239 (T3 forced an empty OpenCode config) is closed.
   - #13068 (llama.cpp grammar error on the T3 path) is open. It is attributed mainly upstream, with T3's roughly 20 extra MCP tool schemas as a trigger.
   - Users report running local models this way. [issue/PR discussion: discussion #7366]
4. **Not on `main`:** Pi (which supports local models) and a generic ACP Registry provider exist only on the unmerged V2 branch. [repo source: V2 tree `Drivers/PiDriver.ts`, `AcpRegistryDriver.ts`]
5. **Requests closed without a native provider:** #190 (Ollama/local), #1947 (Ollama first-class), #1720 (OpenAI-compatible local), #3890 (custom endpoint), #4941 (OpenAI-compatible by base URL), #6032 (Ollama Cloud). Many closed on 2026-08-15, when feature requests moved to Ideas discussions. [issue/PR discussion] Open proposals include discussion #7366, which asks for a generic OpenAI-compatible driver.

**What Codex itself supports.** [repo source: openai/codex `codex-rs/model-provider-info/src/lib.rs` @e72da2b; vendor/project docs: https://learn.chatgpt.com/docs/config-file/config-advanced]
- `[model_providers.<id>]` takes `base_url`, `env_key`, `wire_api`, `requires_openai_auth` and headers.
- `WireApi` has **only `responses`**. `wire_api = "chat"` is rejected with an explicit removal error.
- `ollama` and `lmstudio` are built-in, reserved OSS provider IDs (ports 11434 and 1234; experimental `CODEX_OSS_BASE_URL`/`CODEX_OSS_PORT`), selected by `--oss` / `--local-provider` / `oss_provider`.
- Because app-server takes `-c` overrides rather than `--oss`, the app-server equivalent is `-c model_provider="lmstudio"`. [inference]
- `ThreadStartParams` accepts per-thread `modelProvider` and `config`, so one app-server could run OAuth and local threads side by side. T3 does not use this. [repo source: `codex-rs/app-server-protocol/schema/typescript/v2/ThreadStartParams.ts`]

**oMLX.** [repo source: jundot/omlx @3f2d07e, Apache-2.0, about 22k stars]
- Serves `POST /v1/responses` (`omlx/server.py` L6917), `/v1/chat/completions` and Anthropic `/v1/messages`. The README endpoint table omits `/v1/responses`, but the code has it.
- Ships first-party integrations:
  - `integrations/codex.py` writes `model_provider = "omlx"` with `base_url`, `env_key = "OMLX_API_KEY"` and optionally `model_context_window`. `wire_api` is left at its default of responses.
  - `integrations/claude.py` sets `ANTHROPIC_BASE_URL`, `ANTHROPIC_AUTH_TOKEN` and an empty `ANTHROPIC_API_KEY`, and requires at least 48K context.
  - There is also an OpenCode integration.
- oMLX refuses non-loopback binds without an API key.
- oMLX therefore *targets* both the Codex and Claude Code wire shapes. Whether its Responses implementation covers everything Codex sends (freeform apply_patch, reasoning items, parallel tool calls, long agentic turns) is **unknown until tested**. [inference]

## 4. Coexisting credential modes (OAuth, API key, local)

- **T3.** Yes, as separate provider instances shown together in the model picker; each thread is bound to one instance. [repo source: `providerInstance.ts`; vendor/project docs: `install.md` "Add another provider instance… API keys or a custom base URL"] Example set: "Claude (subscription)" with the default config dir; "Claude API" with `ANTHROPIC_API_KEY` marked sensitive; "Claude oMLX" with its own `CLAUDE_CONFIG_DIR` and base URL; "Codex (ChatGPT)"; "Codex oMLX" via launch arguments.
- **Switching within a thread.** Allowed only between instances with the same continuation key:
  - Codex keys on the shared `CODEX_HOME` path alone, not launch arguments (`CodexHomeLayout.ts` L55–64). An OAuth instance and an oMLX instance sharing `~/.codex` would therefore be offered as switchable. What Codex does when the provider changes mid-thread is untested. [repo source; the outcome is inference]
  - Claude switches only within the same config directory. [vendor/project docs]
- **Text generation** (titles, commit and PR text) has its own selectable instance and model. The default is `codex`/`gpt-6-luna`, so a local-only user must repoint it. [repo source: `settings.ts` L1228, `model.ts` L164]
- **Underlying harnesses.**
  - Codex keeps one `auth.json` per home (ChatGPT or API key), plus `env_key` credentials per custom provider, and can choose a provider per process or per thread. [repo source]
  - Claude Code's credentials are per process: OAuth in the config dir, or API key / base URL through environment variables. [vendor/project docs; inference on the mechanism]

## 5. Embeddability and extension

- **Headless server: yes.**
  - `t3 serve` with `--port`, `--host`, `--base-dir`/`T3CODE_HOME`, `--no-browser` and `--bootstrap-fd` (used by Electron to hand over a bootstrap token), and `t3 service install` for a macOS LaunchAgent. [repo source: `apps/server/src/cli/config.ts`; vendor/project docs: `install.md`]
  - HTTP contract (Effect HttpApi): `/.well-known/t3/environment`, `/oauth/token`, `/api/auth/websocket-ticket`, `/api/orchestration/{snapshot,shell,threads/:id}` and `POST /api/orchestration/dispatch`. The dispatch endpoint takes `ClientOrchestrationCommand` values such as `project.create`, `thread.create`, `thread.turn.start`, `thread.approval.respond` and `thread.user-input.respond`. [repo source: `packages/contracts/src/environmentHttp.ts`, `orchestration.ts`]
  - The WebSocket carries typed Effect RPC. Every RPC checks scopes; auth uses pairing, bearer or DPoP tokens with scoped grants. [repo source: `docs/internals/environment-auth.md`]
  - Third parties already drive it. One team built "an external orchestrator client" (`t3 pair` → `/oauth/token` → dispatch) that "works very well overall". [issue/PR discussion: #8319] A maintainer pointed a Stream Deck plugin at read-only pairing plus `orchestration.subscribeShell`. [issue/PR discussion: #10929]
  - No stability guarantee for external clients is stated, and V2 will reshape orchestration. [inference]
- **A SWBPIPE-class Tauri host** could: [inference, based on the facts above]
  - (a) run `t3` as a sidecar: a Node single-executable binary for Apple Silicon only, with no Intel `t3` executable (`install.md`).
  - (b) embed T3's own web UI in a webview, which brings T3's UI and branding.
  - (c) write a Rust client for the HTTP dispatch plus WebSocket RPC.
  
  A native SWBPIPE agent panel means (c) or a fork.
- **Application tools.**
  - There is no host-tool API. T3 passes no Codex `dynamicTools` and no Claude in-process SDK MCP (`createSdkMcpServer` is not used). [repo source]
  - Its own toolkit is fixed (preview, pull requests, device; `apps/server/src/mcp/toolkits/`).
  - A host can still provide typed tools as an **MCP server registered in the harness's native config**: `-c mcp_servers.<name>.url=…` in the Codex instance launch arguments, `~/.codex/config.toml`, or a Claude project `.mcp.json`. [inference; the mechanism mirrors T3's own `-c mcp_servers.t3-code…` use]
- **Instructions, skills, roles, workflows.**
  - Codex reads AGENTS.md natively. Claude loads CLAUDE.md and skills through `settingSources`.
  - The composer supports `$skill` and `/` commands for provider skills. [vendor/project docs: `docs/user/composer.md` §Commands and skills]
  - T3 adds its own instructions: runtime info, PR-linking rules, browser and device tool guidance, and its Plan-mode text. [repo source: `RuntimeInstructions.ts`, `CodexDeveloperInstructions.ts`]
  - T3 has **no concept of roles or WORKFLOW.md packages**. Chirality's four roles could be approximated with native AGENTS.md, skills and Claude subagents, but selecting a role and carrying Chirality evidence would need a fork or a separate client. [inference]
- **Fork vs contribute upstream.**
  - CONTRIBUTING: "We are not actively accepting contributions right now". It favours small fixes; large or feature PRs are "least likely"; external PRs are labelled `vouch:unvouched`; features go to Ideas. [repo source: `CONTRIBUTING.md`]
  - AGENTS.md: "A large number of our users run forks". The contracts deliberately keep `ProviderDriverKind` an open slug so forks can add drivers such as "a fork's `ollama`". [repo source]
  - A fork would track very high churn: 1,522 commits in September 2026 and the pending V2 rewrite. Module boundaries are clean in principle: adapters under `apps/server/src/provider`, contracts in `packages/contracts`. [inference]

## 6. Terms and risk

- **T3's own terms.** "You bring and configure your own coding-agent harness and provider"; users are "responsible for reviewing those providers' terms". The services are provided "as is". [vendor/project docs: https://t3.codes/terms-of-service]
- **Anthropic.** "Unless previously approved, Anthropic does not allow third party developers to offer claude.ai login or rate limits for their products, including agents built on the Claude Agent SDK." Claude Code branding is not permitted, and the Commercial Terms govern. [vendor/project docs: https://code.claude.com/docs/en/agent-sdk/overview]
  - The help centre says the planned Agent SDK billing change is paused. Agent SDK and third-party app usage "still draw from your subscription's usage limits". [vendor/project docs: https://support.claude.com/en/articles/15036540]
  - T3 relies on the user's own `claude` login through the SDK. Early community debate about ban risk is in #991. [issue/PR discussion]
  - Whether a Chirality/SWBPIPE distribution that relies on users' subscriptions is permitted **needs written confirmation**. [inference; consistent with the T7 return]
- **OpenAI.** Codex CLI is Apache-2.0 and forking is permitted. No public statement was found approving third-party apps that use "Sign in with ChatGPT"; developers are still asking. [issue/PR discussion: openai/codex discussion #8338, 2025-12 to 2026-08]
- **Dependencies.** Effect 4 **release candidate**, Electron 44, TypeScript 7 and Node ≥22.16. T3 publishes provider-version compatibility ranges and warns when a CLI falls outside them. [repo source: `pnpm-workspace.yaml`, `providerCompatibility.ts`]
- **Security posture.** [repo source / vendor/project docs]
  - Default permission is **Full access**.
  - OpenCode's password and Antigravity's API key are "Stored in plain text"; environment secrets are redacted to clients.
  - PostHog usage telemetry is on by default (provider, model, token totals; no prompts). Opt out with `T3CODE_TELEMETRY_ENABLED=false`. [`docs/user/telemetry.md`]
  - A security policy and safe harbour are published.

## 7. Momentum and maintenance

- **Popularity.** 23,579 stars, 6,113 forks, 379 contributors including anonymous, 4,458 commits on `main`. The repository was created 2026-02-08. [repo source: GitHub API]
- **Concentration.** Commits by juliusmarminge: 2,245 (about 50%); t3dotgg: 527; maria-rcks: 277. The bus factor is effectively one or two people. [repo source for counts; inference for bus factor]
- **Commits per month in 2026.** Feb 532, Mar 628, Apr 228, May 93, Jun 410, Jul 364, Aug 681, Sep 1,522 (through the 26th). [repo source]
- **Releases.**
  - Stable 0.0.x: about 50 releases between 2026-03-02 and v0.0.42 on 2026-09-16.
  - Nightly and preview builds: all releases per month grew from 27 in March to 178 in August and 133 in September. [release notes: `gh api releases`]
- **Issue and PR load.** 887 open issues, 1,413 open PRs, 3,875 merged PRs. [repo source: search API]
- **Breaking changes.** Contracts deliberately stay decodable across versions (open driver slugs, forward-compatible fields). The V2 orchestrator rewrite is the major pending change. [repo source; PR #2829]

## 8. Disposable local experiments

Use scratch directories only, with an isolated `--base-dir`/`T3CODE_HOME` and never `~/.t3/userdata` (T3's own AGENTS.md warns against it). The owner must approve any install.

- **E1: T3 + Codex + oMLX.**
  - *Setup:* T3 v0.0.42 desktop or `t3 serve`. A "codex_omlx" instance with launch arguments `-c model_provider="omlx" -c model_providers.omlx.name="oMLX" -c model_providers.omlx.base_url="http://127.0.0.1:<port>/v1" -c model_providers.omlx.env_key="OMLX_API_KEY" -c model_context_window=<n>`, the environment variable `OMLX_API_KEY` marked sensitive, and a custom model matching the oMLX alias. Scratch git repo.
  - *Action:* in Supervised mode, run a multi-file edit with shell commands, a Plan-mode turn, a restart and resume, and a text-generation title. Also switch mid-thread with a ChatGPT instance sharing the same `CODEX_HOME`.
  - *Observe:* apply_patch and tool calls, approval prompts, truncation (#13436), provider-card warnings (#4729, #11873), resume, and what happens on the provider switch.
  - *Limit:* conflates model quality with oMLX Responses fidelity; 0.0.x churn.
- **E2: T3 + Claude Code, three instances.**
  - *Setup:* a subscription instance (default dir), an API-key instance (`CLAUDE_CONFIG_DIR=~/.claude_api`) and an oMLX instance (`ANTHROPIC_BASE_URL`, `ANTHROPIC_AUTH_TOKEN`, empty `ANTHROPIC_API_KEY`, custom model).
  - *Action:* the same tasks as E1, plus a subagent, a project skill (`$skill`), project `.mcp.json` and `/compact`.
  - *Observe:* per-thread selection, credential isolation, auth-status display, the alias issue (#4149), and oMLX context scaling.
  - *Limit:* the terms question stays open.
- **E3: T3 driven headlessly by a toy Tauri host with one application tool.**
  - *Setup:* `t3 serve --host 127.0.0.1 --port <p> --base-dir <scratch> --no-browser`, then `t3 pair --label tauri --ttl 30m`. In the toy Rust app, embed a streamable-HTTP MCP server with one typed tool, registered through Codex instance launch arguments `-c mcp_servers.swbpipe.url="http://127.0.0.1:<q>/mcp"` (or `.mcp.json` for Claude).
  - *Action:* exchange the pairing credential at `/oauth/token`, then dispatch `project.create`, `thread.create` and `thread.turn.start`. Read `/api/orchestration/threads/:id`. Answer an approval with `thread.approval.respond`. Optionally get a WebSocket ticket and subscribe.
  - *Observe:* whether HTTP alone suffices, event latency, how tool-call approvals and elicitations surface, and the effort of a Rust client for the Effect RPC framing.
  - *Limit:* the API is not declared stable, and V2 may change contracts.
- **E4 (optional): OpenCode + oMLX through T3,** compared with E1.
- **E5 (optional): V2 branch + Pi + oMLX,** built from source, as a preview of post-V2 capability.

## 9. Fit against the owner's requirements (all inference)

- **A local model server is required.** Achievable today only through each harness's own configuration (Codex custom provider, Claude base URL, OpenCode), not as a T3 feature. It works, but with open bugs and little documentation, and the owner's stated position is sceptical of local models. Native Pi and ACP-registry routes depend on V2 merging. This is the weakest fit.
- **Not constraining.**
  - What passes through: the user's own binaries, configuration, AGENTS.md, skills and MCP.
  - What T3 imposes:
    - fixed permission-mode mappings;
    - its own injected instructions and MCP tools;
    - no dynamic tools, per-thread `modelProvider` or custom developer instructions;
    - no role or workflow model.
- **Easiest to maintain.** Using T3 unmodified as a separate app is low effort for Chirality. Embedding or forking means tracking a very large, fast-moving, alpha, Effect-RC codebase with closed contributions and a pending 500k-line-delta rewrite.
- **Multi-provider.** A strong fit: six providers on `main`, with more coming via ACP and Pi in V2.
- **OAuth, API key and local at once.** Yes, as parallel instances with per-thread choice. Mid-thread switching is limited.
- **Mac first.** Yes. The desktop app ships for arm64 and x64; the `t3` CLI is Apple Silicon only.
- **Embeddable in SWBPIPE-class hosts.**
  - Possible as a sidecar server or a webview UI.
  - A native agent panel with typed host tools needs a custom client plus MCP-registered tools, or a fork.
  - D-GOV-43's direct stock-Codex-app-server hosting remains the alternative with per-thread `modelProvider` and `dynamicTools` available.

## 10. Known, unknown, how to find out

- **Known:** architecture, providers and transports, the pass-through local-model routes and their bugs, the multi-instance credential model, the headless HTTP/WebSocket API, the contribution policy, momentum figures, and that oMLX exposes `/v1/responses` and `/v1/messages` with its own Codex and Claude integrations.
- **Unknown, and how to settle each:**

| Question | How to find out |
|---|---|
| Does oMLX's Responses implementation cover everything Codex sends? | E1 |
| What does Codex do when the provider changes mid-thread? | E1 |
| Is the external API stable, and what will V2 change and when? | Watch PR #2829; ask in an Ideas discussion |
| Would maintainers accept a host-tool or instructions extension point? | Ideas discussion; #7366 is the nearest |
| Are subscriptions permitted in a distributed Chirality/SWBPIPE? | Written vendor confirmation from Anthropic and OpenAI |
| How much work is a Rust client for the Effect RPC over WebSocket? | E3 |
| Is Theo's March 2026 statement on local models still his current stance? | The post was not directly retrievable; ask in an Ideas discussion |
