# CCE-MANAGER-TASK-01 — first connected TASK route options

Source/options assessment, 2026-10-09. Basis: main
`3cbfac7b8eb49aaee9ceb2068125319b1995f8aa` (merged PR #1188).
Prepared by WORKING_ITEMS for HELP_HUMAN and independent review. This is not
technical selection, accepted-contract amendment, implementation, supplier
qualification, or permission to launch. No model/native test or managed session
was executed or created for this assessment. The owner's no-memory direction
supersedes the run memory convention.

## Finding and recommendation

Current App v4 has no complete executable manager-to-TASK route. The smallest
D-independent target is **C's per-thread App dynamic-tool request feeding A's
genuine managed-session service**. C supplies the request transport; it does
not replace the actual governed child execution required by A. This continues
the proposed CCE-ROLE-SOURCE-01 and CCE-INIT-ORDER-01 source path, without
adopting those proposals or reopening completed Group A work.

| Route | Source-backed capability | Missing connected capability / consequence |
|---|---|---|
| A — Chirality-managed `delegate_agent` | D-GOV-35 recognizes genuine governed managed child sessions. V3 `ManagedDelegationService` accepts an injected `launchChild`, validates brief/context/scope inputs, writes evidence, and calls that launcher with instruction identity and bounded inputs. | No corresponding integrated v4 service/launcher. Reuse evidence is not v4 adoption. V3 writes LAUNCHED/RUNNING before the launcher returns: files alone cannot prove execution. Its `contextSealed`, `pipelineRunApproved`, and `approvalRef` inputs do not authenticate a person act. |
| B — stock native descendant | Protocol `ThreadItem.collabAgentToolCall` records sender, receiver thread IDs, tool, status and agent states; prompt/model/reasoningEffort are optional. D-GOV-35 permits the native class within its instruction-asserted limits. | Current `Composition::child_status` remains not-supplied. No witnessed supported carrier supplies full App common+TASK guidance and original child admission for the CCE join. A native prompt is not an App `SourceRequest`; class eligibility is not an executed TASK session. |
| C — App dynamic tool | Generated experimental 0.160.0 schema permits `ThreadStartParams.dynamicTools`, function/namespace specifications, `DynamicToolCallParams` with thread/turn/call/tool/arguments, and success/content response. | App registers no tools; `native_requests.rs` answers `item/tool/call` as known-app-unsupported, `app-rule:no-dynamic-tools`. Needs an actual offer, request custody, bounded handler/reply, and A's executor. Declaration is not stock supplier/model qualification. |
| C — App-owned MCP alternative | `mcpServer/tool/call` has a client request shape requiring server, threadId and tool. | It is an App-origin call to a configured MCP server, not agent-to-App initiation. No App-owned receiver/registration exists. Arbitrary thread config does not prove scoped ephemeral registration. Do not impersonate an agent request using this client operation. |
| D — person-start fallback | Ordinary App thread start exists. ROLE's person-selected continuation is a separate source obligation. | `compose_role` calls `Composition::new(..., false)` and primary TASK is refused; no C3 TASK command exists. A new reviewed person-requested entry could be a limited fallback, but a human action per task is not manager delegation and must not become routine work-graph approval UI. |

The dynamic-tool declaration applies to **fresh manager threads**: generated
resume/fork parameters have no `dynamicTools` property. Do not infer retrofit
registration. Host advertises experimental API capability, which does not
establish that a model can call this tool. No user configuration write,
provider switch, policy override, App-owned MCP server, or Group D service is
needed for the proposed transport. No failed route silently falls back to
another delegation class.

## Minimum additional source and implementation obligations

1. Adopt one bounded App function offered to an actually admitted HELP_HUMAN or
   WORKING_ITEMS conversation. Preserve native user configuration and policy.
2. Mint a private request handle from the original received tool call, binding
   the actual offer, Host/home/H5, thread/turn/call and exact arguments. Renderer
   JSON, role labels, copied receipts, history, or `delegated=true` cannot mint it.
3. Implement the Root-compatible managed-session lifecycle: sealed brief and
   context, declared scopes, actual launcher, reconstructible durable evidence
   and failure recovery. Missing service means refusal, not manufactured launch
   records. Deliberately review V3 reuse rather than import its booleans as proof.
4. Admit the real TASK start with exact common+full TASK guidance; bind its
   original start/fork/resume lineage and actual answer turn to private
   RoleSourceLease/capture custody. Guidance supply remains distinct from
   adoption; no actor, permission or production-standing promotion follows.
5. Resolve the still-proposed SL-4/fresh-child and WR notice/role/Host dispatch
   ordering before the connected producer. Preserve the separate manager review
   conversation. Pending-notice cut semantics and reverse-lock proof are not
   adopted by this recommendation.

Source ownership: Group A role/Host/EXEC owners receive the managed service,
role carrier and original admission obligations; Group C receives the bounded
request/status and answer-evidence join. GC-8 records that A-to-C relationship.
A future Group D receiver must not label App-managed thread creation as native
Fleet `dispatch_observed`. No reverse D prerequisite is proposed.

## First connected proof — proposed, not executed

Against the actual future App implementation with synthetic supplier transport:
admit a fresh manager thread carrying the one tool definition; receive the
original tool call; invoke the real managed launcher; observe one TASK
`thread/start` carrying exact common+TASK instruction bytes and then the exact
answer request. Assert both original native admission receipts and durable
managed-session evidence. Files, callback invocations, and generated types alone
are insufficient. Every result remains synthetic implementation evidence;
separately authorized stock supplier qualification and a real model answer are
still required for a genuine C3 answer.

Required negative cases: unoffered or copied call; wrong manager role, home or
H5; absent managed service; record-only launch; failed/partial TASK start;
missing or substituted TASK guidance; stale intent; and pending-notice races
before preparation, between preparation and the admission cut, and after the
cut under the eventually selected WR rule. Recheck continuation lineage and
reject using a generic bind/history receipt as original admission.

## Selection and consequence boundary

C+A is a technical candidate within the existing managed class and A-to-C
ordering; it does not inherently need an architectural ruling. Named source
adoption and independent review precede implementation. Escalate a concrete
owner conflict if selection would introduce a record-less delegation class,
change user policy ownership, misrepresent App threads as native Fleet dispatch,
or require Group D completion first. Do not seek a routine human graph approval
for each authorized manager assignment. This document creates no grant or
managed session and does not change accepted role/Host/WR/EXEC contracts.

## Exact consulted source identities

All SHA-256 values below identify whole files at the basis commit. `app/` is
relative to `projects/chirality-app-v4/`; other paths are repository-relative.
These are assessment evidence, not new production source pins. V3 was consulted
explicitly for reuse comparison; other full role bodies were not adopted.

| Source | SHA-256 |
|---|---|
| `app/src-tauri/resources/supplier/0.160.0/codex_app_server_protocol.schemas.json` | `7243ba241962af92ca60581f1a81808ebda4212a800f8b205f54703bcfd508c5` |
| `app/src-tauri/src/hosting.rs` | `7b9f306d7c6fc9ceeeb4178003521afcdafe5981370f0fc87418fdf35e2644b9` |
| `app/src-tauri/src/native_requests.rs` | `bb3317458e40ade1e623f86ed771c196a97e07ca7e4daa8a89931b3ea6ee6992` |
| `app/src-tauri/src/role_supply.rs` | `83e75542baa986924823ebdf7bcefa9d6761c623e536d92eb29fd2d603a81ec2` |
| `app/src-tauri/src/role_lifecycle.rs` | `549fe28fe8155217ac961a29bf3dfe43b9103de12ccad585f609894e411bf7b3` |
| `app/src-tauri/src/runtime_session.rs` | `15425f6a48b31570447ab498b2a7c92f7870b2700d75fc9de1aef891af221f97` |
| `app/src-tauri/src/lib.rs` | `5f6b5d0e818856c8699ab1341dde7e3b6358bbbde2868a922556d11feb49c79b` |
| `projects/chirality-app-dev/frontend/src/lib/harness/managed-delegation.ts` | `0a3dec1309bde70548daee39a48b280ece6886f837d8c4d4b40b85f4f6a6d180` |
| `docs/governance_harness/_DECISIONS/D-GOV-35_delegated_harness_native_class.md` | `e7c1e532a9d46cdc27957c85003515c46b5193e21438c905cf1cfb4e56433efa` |

Read-only source inspection and schema declaration comparison support this
assessment. No runtime, supplier, native launch or model result is claimed.
