# Current native child carrier — Codex 0.160.0

Bounded receiving evidence for ROLE §5.3 and DEL-02-04 REQ-002/003,
2026-10-11. The maintained opt-in
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

| Selected maintained bytes | Length | SHA-256 |
|---|---:|---|
| Common + WORKING_ITEMS parent | 5329 | `b329e41b30ea0373f44fbb401bd14b8e3a155a0acbf7ab7b70fe8bbf664c212c` |
| Common + TASK child | 5198 | `7fa6b946d43d27cd7b1b0e7c7ac16cbeb4f98da62a79f556ed1c8d44150dc4c4` |
| Native selected model template | 21779 | `e1bdd4f8f0df4b20f4a0ffc8a861ce819df45325d8cecdfb92e80379cf8d142e` |

The composition oracle reads the maintained shipped defaults and the existing
ROLE framing directly. It does not exercise Rust composition, the editable
App store, seeding, file publication or the App's actual start dispatch.

## Negative inputs and existing names

The six-case maintained check passed with ten captured provider requests:

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
name rather than guess that it is free. The collision fixture observes the
scratch home source; project/profile/session-defined names and the App's actual
collision handling still require connecting checks.

The child still has the native `spawn_agent` tool. TASK's prohibition on further
delegation is **stated, not enforced**. These captures prove neither instruction
conformance nor a tool-denial guarantee, and no further-delegation attempt was
made.

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
public fixtures. The observed
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
