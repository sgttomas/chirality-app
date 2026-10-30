# Retained candidate: native setup/save/relaunch witness preparation

Prepared 2026-10-29 by the desktop release manager. **Not executed.** This is
the next bounded native witness, not a new qualification dossier or release
criterion. The existing workflow/recovery/access-mode commitments remain.
Agent0 owns execution coordination and owner-reserved choices. The prior
single-build clearance grants no GUI or supplier execution for this route.

## Exact artifact and inputs

Use only candidate `795362874d-a391547a5c5d`, built from
`795362874dd73a25cf8d9cbf8d7dc0f8fbd38a98`; its retained identification and
complete inventory are under
[`Evidence/EXP/795362874d-a391547a5c5d`](../Evidence/EXP/795362874d-a391547a5c5d/candidate-identification.json).
The bundle is:

```text
/private/tmp/chirality-desktop-current-ukt5ir80/target/debug/bundle/macos/Chirality App v4 (development 20261029).app
```

- Identifier: `dev.chirality.app-v4.candidate.20261029-ukt5ir80`.
- Executable: `Contents/MacOS/chirality-app-v4`; SHA-256
  `a0b29cf7120e9fabb1fd2e6e553d69c1a010312db6ae1f1005d572110806d48e`.
- Complete bundle identity:
  `chirality.app.bundle-tree.sha256/v2:a391547a5c5d485fc07b286e4177279717b2fc43ad7deff2f8f5bd983f24ae91`.
- Bundled supplier: `Contents/Resources/codex/bin/codex`, stock `0.160.0`,
  241,555,024 bytes, SHA-256
  `112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b`.
  Complete 42-file archive correspondence is retained; this is unqualified
  development standing, not authenticated acquisition or installed custody.

Fresh invented inputs have been created under
`/private/tmp/chirality-desktop-current-ukt5ir80/witness-inputs/`:

| Input | Relative path | Purpose |
|---|---|---|
| Shared configuration | `shared/config.toml` | File-auth storage, explicit no-model provider, plugins and analytics disabled |
| Shared guidance | `shared/AGENTS.md` | Tiny invented startup fixture; no client data or task |
| Shared skills | `shared/skills/` | Empty directory |
| Project | `project/` | Empty scratch project, deliberately chosen in setup |
| Fallback Codex home | `fallback-codex-home/` | Fresh empty process-level `CODEX_HOME`; never `~/.codex` |
| OS temporary parent | `tmp/` | Fresh probes and ordinary process temporary files |
| Network policy | `network-denied.sb` | Proposed inherited network denial and `~/.codex` read/write denial |
| Input account | `input-manifest.json` | Actual paths, SHA-256 values, proposed allowlisted environment; no execution result |

The configuration selects `desktop_witness_offline`, model
`no-model-do-not-send`, `wire_api = "responses"`, and base URL
`http://127.0.0.1:9/v1`. It starts no listener. No thread or turn is to be
started. These are synthetic startup inputs, not product defaults or one of
the three qualified access-mode witnesses. `cli_auth_credentials_store =
"file"`, `[features] plugins = false`, and `[analytics] enabled = false`
request file-auth and suppress those configured startup services. Configuration
alone is not a no-network guarantee.

## Why the two launches differ

Source basis is the built source's `lib.rs` `explicit_environment_launch` and
`run`, `desktop_startup.rs` `resolve`/`saved_launch`/`preview`, and
`desktop_setup_confirmation.rs` `prepare`/`confirm`.

The explicit startup selector tests presence of ten `CHIRALITY_*` variables,
including empty values. Omit all of them; do not set them to empty. The generic
`CODEX_HOME` variable does not select that route. With no saved request, phase A
has no valid host configuration and does not enter the supplier-start branch.
The setup action saves a pending request; it does not start Codex or apply a
live project/home switch. Phase B admits the saved request and automatically
starts a version probe and app-server handshake. **A successful relaunch cannot
also be described as supplier-free.**

The saved route creates a fresh App-owned account at the actual Tauri data root,
`account-homes/account-<opaque>`, not at a caller-chosen existing home. Expected
data root is:

```text
/Users/ryan/Library/Application Support/dev.chirality.app-v4.candidate.20261029-ukt5ir80
```

This new identifier namespace is the expected non-scratch App-data write
location. Platform UI may also create identifier-selected WebKit/cache state
under the real user's Library; that external state is separately observed,
not claimed to be scratch-only or covered by the App-data path. These effects
must be explicitly included in the reviewed execution. Do not
redirect `HOME`, adopt a real account, precreate a fake saved request, bypass
the native confirmation or replace the desktop route with environment startup.
Capture the actual displayed root and opaque account path before confirmation;
an unexpected root, existing request or existing home stops this witness.

## Containment and admission before either launch

1. Agent0/owner must explicitly authorize these GUI launches and phase B's
   stock-supplier startup. Obtain a concrete serialized window through the SWB
   manager. The owner must be present at the GUI before **each** launch, not
   only available later for the setup question. Resource clearance alone is
   not execution authority; await the relayed owner disposition.
   No model server, model turn, credential, sign-in, download, VM or build is
   part of this route.
2. Recheck the retained candidate against its inventory immediately before
   execution. Before **A**, record current absence of the three checked
   identifier-selected data locations. `check` preserves historical freshness;
   it does not perform that current absence check. Before **B**, those locations
   may contain this witness's expected A effects: compare the saved request,
   actual App-data root, account path and source identities with A's captured
   preview/outcome, rather than requiring absence again. A changed artifact,
   unrelated occupied namespace or changed/unexplained A effects refuses; do
   not remove material to manufacture a precondition.
3. Launch the exact executable directly, retaining its process/session ownership
   and stdout/stderr. Do not use Finder/LaunchServices to infer artifact identity.
   Use a clean allowlisted environment from the input account: actual existing
   `HOME`, `LANG`, explicit supplier `codex-path` plus system `PATH`, fresh
   `CODEX_HOME`, and `TMPDIR`. No credential/provider/proxy or `CHIRALITY_*`
   variables are inherited. The Host separately assigns its admitted account
   and fresh probe `CODEX_HOME` values to the supplier.
4. Proposed command prefix is `/usr/bin/sandbox-exec -f <network-denied.sb>`
   followed by the exact executable. The profile uses `(allow default)` with
   `(deny network*)` and read/write denial for `/Users/ryan/.codex`. The local
   provider URL is a stand-in, not an allowed network exception. The binary
   exists, but **this policy and native-WebKit compatibility are unexercised**.
   Refusal or UI failure is an observed blocked/failed pilot, not grounds to
   drop isolation or fall back to an unsandboxed launch. Inheritance is intended
   for the owned App/supplier process tree; no claim is made about unrelated
   OS services. This witness does not establish network-observability criteria.
5. Use the agreed slot wrapper and App-aware process-tree monitor. The shared
   guard alone omits this checkout/private target; see the retained build
   evidence. Proposed native window: at most one App at a time, two launches,
   at most ten minutes total, sampled shared RSS cap 64 GiB, system free floor
   22%, and stop for `exclusive.pending` or a coordinator's exclusive notice.
   The actual resource window and execution disposition belong in the run's
   coordination/evidence; a later exclusive notice supersedes availability.

## Owner actions and observations

**Phase A — setup and save, no supplier.** Owner opens Desktop setup, chooses
new setup, supplies the three exact shared paths, explicitly chooses the scratch
project and `bundled-owner-use-development`, then chooses **Review setup
effects**. Capture full preview and displayed source paths without recording
secrets. Pressing the webview's **Prepare home and save for next launch** opens
the real parented native question, titled **Desktop setup — next launch only**.
The owner must read the effects and personally choose **Prepare home and save
for next launch**. Its non-act/default alternative is **Leave setup unchanged**.
An agent must not press the affirmative control or label its click as an owner
act. Long effects may require the App's separately displayed full content and
digest; retain that actual presentation.

Observe the returned pending-request status, new account/config/guidance/skills
links, unchanged current launch and absence of a supplier generation. The owner
chooses normal **Quit Chirality**; if the native quit question is shown, the
owner chooses its actual quit action. Closing/hiding the window is not quit and
does not release process custody. Observe actual App exit before relaunch.

**Phase B — saved-request startup, no model.** Before launch, the present owner
confirms the same retained artifact/containment and the saved platform route's
exact App-data/account/project/shared references from A. This is the owner's
execution/route disposition, not an invented second App confirmation control
or a handshake result. Only then relaunch the same executable under the same
containment. Observe the actual `saved-request` admission, exact home,
project and resources, linked-source states, unverified-development supplier
standing, native generation and handshake outcome. Label probe, handshake and
supplier startup are actual execution only after this launch; no thread/turn,
approval, login, key entry, registration or model-provider request is initiated.
Capture error/unknown states as such. Then owner normally quits, with the native
question if presented. Preserve original supplier scope/exit evidence; never
signal a cached PID/PGID or an unrelated process.

Record the owner's own reported act separately from source/JSON/UI observations.
An owner's click does not by itself prove source binding, durable save, correct
relaunch or faithful human-act recording. Those observations keep their actual
evidence and limits; no A15/A16 act or workflow qualification is inferred.

## Expected effects, stopping and retention

Expected reads: exact bundle resources, the three invented shared references,
scratch project, new unique App-data namespace and ordinary OS/UI resources.
No real account configuration, credential store or other project's data is an
input. Expected new writes after owner confirmation/admission include the
unique App-data startup request and account links, fresh probe/home supplier
state, App runtime recovery/metadata/instructions/keys as actually initialized,
and scratch project `.chirality` identity/records initialization. Enumerate
actual paths from the preview and source/outcome; do not claim that only the
three symlinks can be written after operational startup. Capture metadata and
nonsecret setup/recovery facts, not credential contents.

Normal owner Quit is the first cleanup route. A hang, unexpected supplier/model
work, unavailable containment, unexpected path or exclusive-window notice stops
dependent work and returns the original owned process state. Any emergency
termination is limited to the original retained process/session ownership and
must preserve unknown outcomes; it is not an automatic substitute for the
owner's confirmation. Do not discover or signal other process groups.

Retain the candidate, caches/source export, witness inputs, logs and unique
App-data namespace until the witness and the owner's retention decision.
PR15 merging alone authorizes no deletion. Later cleanup must first establish
owned-process exit and exact exclusive namespace custody, retain necessary
evidence and remove only this undertaking's scratch/new namespace. No deletion
of owner material or another lane's fixtures is part of this brief.

Required return: exact source/artifact/config/policy and actual time, owner
confirmation attribution, phase A/B observations, process settlement, actual
writes, limitations and next remaining condition. A defined brief supplies none
of those execution outcomes.
