# Current native child carrier — Codex 0.160.0

Bounded receiving evidence for ROLE §5.3 and DEL-02-04 REQ-002/003.
The original observation below is dated 2026-10-11; the current maintained
standalone collision extension is described separately. The maintained opt-in
[check](../../../../app/supplier_checks/child_roles.py) observes the stock
supplier through its published App Server and a scripted loopback Responses
fixture. The fixture supplies one native `collaboration.spawn_agent` call and
then returns HTTP400. It makes no model prediction or authenticated request.
Each case has its own scratch Codex home and project; an OS sandbox allows
localhost only. The person's Codex home and configuration are not written.

The identified input is the already acquired macOS arm64 0.160.0 binary,
SHA-256 `112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b`.
The check refuses any other binary before execution. This identity check
does not qualify the supplier tree or distribution.

## Observed carrier and byte meaning

`thread/start.config` accepts the role-owned dotted keys
`agents.TASK.description` and `agents.TASK.config_file`. A valid TOML file
contains `developer_instructions` with the complete common + TASK composition.
Its description appears in the actual parent's `spawn_agent.agent_type`
catalog. A completed native `subAgentActivity` item with `kind: started`
supplies `agentThreadId`; a correlated `thread/read` reports `agentRole: TASK`
and the correct `parentThreadId`. This is the current observed identity surface;
ROLE's historical `collabAgentToolCall.receiverThreadIds` account remains at its
original supplier version.

Both `fork_turns: none` and `fork_turns: all` carry the exact complete TASK
composition at the child's provider boundary. Neither carries the parent's
App composition in its place. The separately identified native model template
is byte-equal in parent and child, retaining SHA-256
`e1bdd4f8f0df4b20f4a0ffc8a861ce819df45325d8cecdfb92e80379cf8d142e`.
The child's native team context changes; whole-prompt equality is not claimed.

| Historical selected maintained bytes (2026-10-11) | Length | SHA-256 |
|---|---:|---|
| Common + WORKING_ITEMS parent | 5329 | `b329e41b30ea0373f44fbb401bd14b8e3a155a0acbf7ab7b70fe8bbf664c212c` |
| Common + TASK child | 5198 | `7fa6b946d43d27cd7b1b0e7c7ac16cbeb4f98da62a79f556ed1c8d44150dc4c4` |
| Native selected model template | 21779 | `e1bdd4f8f0df4b20f4a0ffc8a861ce819df45325d8cecdfb92e80379cf8d142e` |

The composition oracle reads the maintained shipped defaults and the existing
ROLE framing directly. It does not exercise Rust composition, the editable
App store, seeding, file publication or the App's actual start dispatch.

## Negative inputs and existing names

The original six-case maintained check passed on 2026-10-11 with ten captured
provider requests:

| Case | Bounded observation |
|---|---|
| Baseline, no custom role override | App TASK description absent from the native tool catalog |
| Missing role file | Start succeeds; App TASK description is absent |
| Malformed TOML role file | Start succeeds; App TASK description is absent |
| Scratch person-defined TASK | `config/read` at the selected cwd exposes TASK; withholding the App override preserves its native description |
| Clean child | Complete TASK bytes, native template and parent/child metadata match |
| Full-history child | The same identities and byte checks match |

Accepted `thread/start` or a named role alone therefore cannot establish child
supply. Unexpected or unreadable effective configuration must withhold an App
name rather than guess that it is free. That original collision fixture observes the
scratch home's config-table source; it does not establish standalone-name
coverage. Project/profile/session-defined names and the App's actual collision
handling still require connecting checks.

The child still has the native `spawn_agent` tool. TASK's prohibition on further
delegation is **stated, not enforced**. These captures prove neither instruction
conformance nor a tool-denial guarantee, and no further-delegation attempt was
made.

## Current maintained standalone collision extension

The check now also creates a synthetic standalone `agents/task.toml` in its
fresh Codex home, with the native `name`, `description` and
`developer_instructions` fields. It requires `config/read` to return
`agents:null` while the actual native role catalog retains the person's TASK
description. The fixture deliberately sends an empty `thread/start.config` for
this known collision, verifies that no App child keys were sent and that the
standalone definition and config bytes remain unchanged. This is fixture
withholding based on its constructed source, not the App's still-unbuilt generic
discovery or collision handling. A null config value alone establishes no name
availability; raw role-catalog text or file presence establishes no complete
origin coverage either.

A current rerun on 2026-10-14 passed seven maintained cases with eleven captured
provider requests. Its report SHA-256 is
`fc7794d477269c9e314dd2a901597a9df6299a26182e0a7268bfb3a287137f97`, binding
checker SHA-256
`85a4128ecad1545e3707aa14f671cd5634337f460eb3a127d1e58d745ec92e9d` and the
complete private decoded frames/requests. The current common + WORKING_ITEMS
composition is 5565 bytes, SHA-256
`d9f0157a93b2e1108e5c1e6fead237b0a84b98879f477f7bf2df9c47747ce852`.
The common + TASK composition is 5434 bytes, SHA-256
`9c6cb2b8fb3b431cc890ac4dd4f63ed06aa0d697fe8e38ef5319807cbf13bf50`. The
clean and full-history controls both retain those complete child bytes, the
same separately identified native model template, and correlated child/parent
metadata. None of those controls establishes actual App child publication or
complete native configuration-origin discovery.

The fixture child receives fresh `HOME` and `CODEX_HOME` paths, explicit file
authentication custody and a localhost-only OS sandbox; this child check also
denies reads under the real macOS `/Users` tree, with an exact-path exception
only for the selected, resolved and hash-identified
executable, preserving the documented acquired-path input without admitting its
siblings or supplier tree. The current seven-case rerun used an owned copy under
`/Users` at a path containing spaces, quotes and non-ASCII characters; the same
sandbox denied a synthetic sibling marker. Both owned files
were removed after the check. The shared Native helper keeps
`CODEX_HOME` unchanged across the records-delivery fixture's cold reopen and
sets only its local child environment. No person's configuration or shared
keyring is used. Current source components and compositions are bound by each
new report; the historical byte table and original report hash below continue
to identify their original observation, rather than today's maintained defaults.

## Repeatable receiving check and remaining App join

On macOS, with the identified supplier already acquired:

```sh
python3 projects/chirality-app-v4/app/supplier_checks/child_roles.py \
  --codex /absolute/acquired/vendor/aarch64-apple-darwin/bin/codex
```

The check prints a private temporary evidence path, then a report. Decoded consumed native
frames, complete captured JSON requests and effective configurations stay there;
the report binds their exact file hashes, the checker, source components and
actual invocation. These traces preserve decoded fields and text, rather than
claiming raw wire-byte identity or a complete notification census. They are not
public fixtures. The original 2026-10-11 observed
report SHA-256 is
`c64b7c12557bc4c0fdf8d28efbe8f5a346f95d171ca69a7c09282f29164fd3be`;
independent scrutiny reads those complete decoded inputs rather than treating hashes as
proof. Temporary deletion would leave the stated observations and identities,
not recoverable evidence files.

The current App still supplies no child-role configuration. U-R3 remains open
for the App join: read effective configuration in the actual generation/cwd,
withhold existing or unknown names, freeze the actual edited guidance, publish
and verify content-bound child files, carry only the additive role keys, and
reconcile observed child identities against what that conversation supplied.
Untyped/built-in children retain unknown guidance. App cold reconciliation,
native discovery in a real user project, supplier/model adoption, behavior,
qualification, human acceptance and release remain unestablished. No ScopeOfWork
commitment, criterion, owner stage gate or PRD open question changes here.
