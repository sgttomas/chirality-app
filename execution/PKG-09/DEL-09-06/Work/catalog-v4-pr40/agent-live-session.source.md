# Embedded agent live session — implementation candidate

RT-E1 / DEL-16-06. The owner's activation authority in embedded-agent-host.md
applies. This increment implements the live binding and native lifecycle while
the compiled public Start gate permits the qualified ARM pin/profile and
refuses unqualified Intel. A minimal panel (below) starts a session only on the
person's explicit action; there is no automatic supplier start or environment
bypass. Native qualification uses a separate opt-in native-smoke process mode
of the actual app executable and the same internal runtime constructor.

## Trust and custody

The raw `embedded_agent_host` command admits at most 256 KiB before typed
interpretation, with a separate 32 MiB ingress allowance for derived values.
It derives the invoking main webview and bundled origin from Tauri, and native
resource and state paths from AppHandle. The model cannot select them. Windows
and Linux return isolation unavailable. macOS owns one lazy actor with a bounded
16-request channel, separately admitted 1 MiB stack/2 MiB thread allowance,
32 MiB state allowance and 1 MiB response allowance. No worker starts merely
from constructing the workspace session or checking availability.

Native registration issues a random workspace handle, generation, private
producer capability and separate protocol session token. Only the actual
workspace execution closure keeps the capability. It is absent from notices,
claims, model arguments, provider traffic, persisted settings and logs. This
trust boundary assumes the bundled workspace JavaScript, not arbitrary script
execution in the webview. Tool data never installs an execution producer.
The original JSON-RPC destination remains private to Protocol; completion uses
only an opaque requestRef. Claims remain one-shot on transport failure.

The producer publishes actual queue/read/job evidence before completion. The
native owner separately retains that record and checks exact completion-byte
equality, catalog validity, basis and job standing. A completion cannot create
its own evidence. Queued, detached, lost and unconfirmed delivery do not change
actual standing. Closed contexts accept late actuals for already claimed work;
there is no automatic domain replay. Every terminal path retires the workspace and closes its bridge before
cleanup releases the live runtime. Clean EOF, original supplier exit, requested
stop and protocol/transport/admission failure retain distinct lifecycle standing;
successful cleanup never erases a failure class or revives new claims.
Native take_actual transfers a copy of the
actual while preserving tombstones and historical references. The four retained
workspace contexts and their 64-call ledgers refuse capacity explicitly rather
than evicting outcome evidence; restarting the app loses ephemeral handles.
These limits do not provide durable audit/history.

The workspace owner supplies its actual immutable batch registration, proposal
standing and existing native solve receipt. Agent operations are stamped as
proposed/agent, with original request/thread/turn/call, basis and assumptions
outside the native intent schema. Supplier validation/source claims are reset.
The sole operation engine validates; only existing person Apply publishes a
model. Outcome hash/standing updates in that same synchronous publication.
Interruption withdraws only still-pending agent batches; a synchronous application
admission set prevents withdrawal once Apply has begun. It never cancels a solve
or claims rollback. Existing queue events preserve withdrawn/unknown standing.

Read producers bound pages before collecting rows. Cursors bind tool, basis,
offset and run. Summary counts do not serialize the model. Node pages preserve
source units and negative zero. Results use existing numerical overlay policy;
this initial adapter conservatively withholds retained-precision values rather
than substituting rounded binary64. Catalog version 3 adds the W9-A build
discriminators, a host stamp for the constant intent fields and a filter on
result reads ([host design](embedded-agent-host.md)); version 4 adds component,
support-configuration and deletion intents and a record read with exact before
texts. Criterion 17's remaining
discriminators, retained source-value presentation and the actual desktop
review witness remain open.

## Native lifecycle and the qualification harness

Live owns the admitted dual-family loopback relay, private runtime and original
supplier Child. It starts fixed initialize/thread/start protocol steps and holds
partial startup custody through cleanup and worker joins. Provider selection
loads the exact saved revision from the reviewed Store, including the person's
context window, which Start refuses when absent; the secret goes only
to the host relay. The child receives only a fresh relay capability. No profile,
credential, persistence format or TLS-trust permission is widened here.

The new narrow unsafe process_scope boundary uses SDK kqueue/kevent on that
retained original Child only: NOTE_EXIT, NOTE_EXITSTATUS and NOTE_FORK. It checks
FD_CLOEXEC. Fork, identity and observation errors latch permanently. It never
uses unsupported NOTE_TRACK/NOTE_CHILD, descendant snapshots, recursive ancestry
or signal authority. The inherited deny-process-fork policy, including
posix_spawn(self), covers supplier startup before observation is armed. A group
census alone is not proof of descendants. Native removal needs both original
group cleanup and a non-invalidated exit observation; unknown retains marker,
backing and refusal state. No later sample can repair invalidation.

The actor's ordinary quit hook requests close and exits the app only after
original group cleanup and distinct driver/relay joins. Cleanup unknown keeps
custody and refuses exit/restart rather than using saved PIDs. Hard-death cleanup
is not claimed by that quit hook and must pass the following native matrix.

The native-smoke mode reads bounded invented configuration from anonymous stdin,
resolves resources from its actual bundle and runs negative probes first, under
the very same profile builder with only the probe executable substituted. The
standalone preflight-only mode starts neither supplier nor relay. The
C probe requires EPERM for fork, posix_spawn(self) and forbidden exec. The Rust
probe checks private writes, outside reads/writes/symlink, both owned loopback
families, an unowned loopback alias/port, off-host, syslog, Users reads, listening
and exec. Missing records are not_run/unknown; terminating signal and first-record
standing are explicit. Fresh probe copies avoid invalidating a cached Mach-O
signature by rewriting an executed file.

The Python controller owns the actual app and anchor Popen objects. The app
holds its original SDK unreaped at a startup gate. While it is alive, the
controller arms original-process exit/fork observation and joins its owned
anchor to that group, then opens the protocol gate. The anchor preserves rescue
authority after app SIGKILL. It kills only its own group through a fixed command;
no recorded PID becomes signal authority. Owned-app and owned-anchor signals
use their original Popen handles. Liveness checks signal only zero.

Qualification order is a harmless summary-tool round trip, then stdin EOF and
app SIGKILL, each at idle, active-turn and pending-tool stages. Trigger records
follow bounded protocol draining and current stage/observer checks. A crash
result requires bounded control-reader completion through normal EOF, then a
stable full drain and terminal/failure validation. Final successful samples
recheck cancellation/safety and the deadline. Observed policy/observation failure
permanently forbids scope certification and runtime/marker removal while retaining
owned-group rescue. EOF/crash success requires original exit status zero and PID
absence, separately from group cleanup; a normal forced stop's status is not
relabelled as an EOF pass.

## Evidence and reconciliation

The selected ARM source/native candidate is qualified to the bounded lifecycle
and isolation extent below; the actual webview command/review journey remains
unexercised. Targeted checks cover controller EOF/cancellation/latching,
workspace authority, outcome-before-delivery, stale preparation, source pages,
late actuals and original native group preservation. The native run used the retained actual bundle resources with verified stock
0.160 bytes and current candidate native-smoke code in a fresh app copy. ARM evidence cannot qualify Intel; the
public gate remains unavailable on any unqualified architecture.

**Start defects the webview journey exposed (RT-E1 D4, 2026-10-31).** The first
run of the agent's journey in the real app window (prerequisite 2 of the D4 live
run) found that the merged agent could never start there, for two reasons:

- The workspace snapshot published the model hash only when
  `uiModelRevision === modelRevision.current`. Those counters advance on
  different events (each publication advances both, and the `[model]` layout
  effect advances `modelRevision` again), so they differ from the first load on
  (1 and 3 there) and Start always refused with "Open a model and wait for its
  fingerprint before starting." The binding rule is now: the hash owner records
  the model revision its hash was computed for, and the snapshot publishes the
  hash only when that equals `modelRevision.current`, read live from the owner,
  together with the existing generation and ownership checks. A hash from
  before an edit is therefore never published while the edited model's hash is
  pending, nor paired with a model an undo restored before React re-renders.
- The workspace and the operation engine write a hash value as `sha256:<hex>`,
  but the catalog's `hash` value is the 64 hex digits alone, so `register`
  refused every real basis. The session converts at the boundary, strictly in
  both directions: a workspace hash must be `sha256:` and 64 lowercase hex
  digits (`agentHash`, else `AGENT-ENGINE-HASH-FORM-REFUSED`), and a hash from
  the agent's basis must be 64 lowercase hex digits (`catalogHash`, else
  `AGENT-CATALOG-HASH-FORM-REFUSED`); nothing else passes through. The
  registered and updated basis, the current-basis comparison, the solve
  receipt comparison and the returned `evaluatedModelHash` and
  `outcomeModelHash` (with its proof record) use the catalog's form; the
  operation batch and its validation keep the engine's form.

Unit tests had used a hand-made hash and never a real project load, so neither
showed. `features/workspace/agentWorkspaceSnapshot.session.test.tsx` (load,
edit, pending hash, and undo read before React re-renders) and the
`embeddedAgentSession.test.ts` cases (engine-form workspace hashes, basis
updates, applied outcome and proof, validation inputs, and both refusals) now
cover them.

DEL-16-06 ScopeOfWork claims/ACs and all dependency conditions remain unchanged:
this implements their existing binding, proposal and cleanup duties, not their
acceptance. deliverable.yaml adds source/check pointers. DEL-08-01's exact unsafe
module list grows from twelve to thirteen only for process_scope, and its command
macro pin reflects the new command. No Cargo dependency or foreign block is
added; exact-set enforcement and report-release reach remain intact. Root routing
and runtime-read inventories are regenerated from the combined tree.

## Selected ARM native observation

Candidate `75b14f5027692a10d7267b33020ea536f431ab85`, macOS 26.6.2 ARM, used a
fresh native-smoke executable in a private copy of the retained app bundle.
The app had a valid ad-hoc hardened seal; deep/strict app verification and the
unchanged stock supplier's strict signature passed. Actual app SHA-256 was
`f508271616530b182962f8e07d7c715b49ce1cd191587e2da15cdd6a417ef72f`;
stock supplier SHA-256 was
`112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b`.
No acquisition, GUI launch or supplier re-sign occurred.

The standalone no-supplier/no-provider preflight passed three C EPERM checks
and all seventeen Rust checks. The native run repeated preflight before each
supplier start, then used the existing oMLX/model pin in agent-witness-pin.json.
The server ran outside slots under the 50 GiB headroom/exclusive monitor; the
fixture ran through the required slot wrapper. Only the pinned model was
requested. Results:

| Case | Original SDK exit | App standing | Cleanup |
|---|---|---|---|
| Harmless summary-tool round trip | 0 | Normal exit 0 | Native original group/join confirmed |
| EOF idle, active turn, pending tool | 0 in each case | Normal exit 0 in each | Native original group/join confirmed |
| App SIGKILL idle, active turn, pending tool | 0 in each case | SIGKILL in each | Original owned anchor cleanup confirmed |

All seven cases passed their bounded stage, exit, PID-liveness, complete-reader
and cancellation checks. No NOTE_FORK or observer invalidation occurred. The
inherited profile's independent fork/self-spawn denial covers the pre-arm
interval; silence after observer arm is not retrospective ancestry evidence.
All seven runtime/marker pairs were removed under their retained native or
fixture anchor authority, with no saved-PID signal. Hard app death still leaves
a product marker for fail-closed refusal until independently qualified recovery;
this experiment's external controller is not a product restart/sweeper route.

The matrix result JSON SHA-256 is
`141641028e0b328cd31fccdbeb1613f6a317b1d9666e8c70d8694b13ea9ffb65`;
standalone preflight JSON is
`210add4741bfc68a96654418c0a517dd7595cafdaf2ce1295100bb2c6c7e0906`.
Their retained local reports identify original app/anchor/supplier roles, stage
records, statuses and per-check results without credentials or arbitrary
supplier text. The source fixture and its regressions are maintained under
tools/ and src-tauri; no permanent check depends on those local report paths.

The outer supervisor returned failure because its own oMLX stop helper did not
complete its group proof. The raw supervisor result is retained as failed; it
is not relabelled as a successful original reap. Model unload was requested and
HTTP-acknowledged before shutdown. Subsequent read-only checks found port 8000
idle and no matching fixture/oMLX roles. A separate inert server start/stop,
with no model/supplier, recorded SIGKILL EPERM on the zombie-only group and
completed the original-group proof before the sole reap. Its JSON SHA-256 is
`adf56cb7ae756ee060d6a879c5d03e516beaf12135052c998f0e52df009b4b34`.
This establishes current resource closure without retroactive signal authority.

Independent permissions/session review of `4190ef19be` found one terminal
retirement defect, repaired with EOF/protocol closure and late-actual retention
regressions in `2415475d19`. No further source blocker was reported for this
constructor-based native matrix. Enabling the ARM native gate follows that
selected pin/profile evidence; there is still no launcher UI. Actual command,
workspace proposal/review, full operation vocabulary, full numerical source-value
presentation, AC-005 and criterion 17 remain open. Intel and other operating
systems remain unavailable; these observations do not widen the support range
or establish release, acceptance or a universal termination guarantee.

## Minimal panel

`features/embedded-agent/EmbeddedAgentPanel.tsx` is the Agent tab of the
Operations section, beside Batch review. It checks availability only when shown,
and an unqualified platform or a browser build shows unavailability. The person saves
a provider (local OpenAI-compatible or hosted HTTPS endpoint, model, and no key
or a key held only in native keychain custody), then explicitly starts, sends
messages, interrupts a turn and stops. The panel never stores a key in a
browser store, log, file or conversation. Agent changes enter Batch review for
the person's explicit Apply; sending a message applies nothing. Batch review and
applied receipts show an agent proposal's basis revision, declared assumptions
and original thread/turn/call reference.

The native owner reports turn standing (`turnActive`, `turnId`, `turnStatus`)
and keeps at most 128 conversation items and 64 KiB of text per workspace;
exceeding either stops the session with `message_limit`. The response allowance
is 1 MiB and each retained native actual with its frontend copy is admitted
within 512 KiB. A closed registration with no claimed work and no retained
actual is reclaimed so settings retries cannot exhaust the four contexts;
contexts that may still own a late actual are kept.

Evidence limits: component and frontend tests cover the panel and these bounds.
Actual webview command/review evidence, a native panel journey and criterion
17's expanded catalog journey remain open; this section does not qualify AC-005.
Version 3's W9-A component evidence does not supply them.
