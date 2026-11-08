# Owner-selected renderer menu capability narrowing

The owner's 2026-11-02 decision, “3. Ok you are approved to narrow as indicated,”
selects only removal of webview core:menu permission. This source change replaces
`core:default` in `app/src-tauri/capabilities/default.json` with the locked Tauri
2.11.1 component defaults below. Capability identifier, main-window scope and
origin configuration are unchanged. This grants no other permission, TCC, signing
or SEAL-C activation change.

```json
[
  "core:path:default",
  "core:event:default",
  "core:window:default",
  "core:webview:default",
  "core:app:default",
  "core:image:default",
  "core:resources:default",
  "core:tray:default"
]
```

The actual locked `tauri-2.11.1/build.rs::define_default_permission_set` expands
core:default to these eight components plus core:menu:default. The generated
ACL manifest is consumed by the integration test, not replaced by a hand-written
permission model. All 22 menu IPC commands are removed, with no lost non-menu
command grants. Adding another capability file or changing the Tauri version/
component expansion fails the focused test for explicit reassessment. No new
component will be inherited silently by a future supplier upgrade.

## Actual consumers and functionality

| Function | Existing route | Effect of this narrowing |
|---|---|---|
| Quit and gated Prepare capture sealing | Rust `lib.rs::app_menu` / `on_menu_event`; SEAL-C native confirmation and provider gates | Rust-owned menus stay; no Rust handler change |
| Waiting requests menu | Rust `native_waiting::append_menu` and `MenuObserver::update` | Rust construction/relabel/update stay |
| Waiting frontend wake and claims | `NativeWaitingBridge.tsx` uses event listen/unlisten plus App checkpoint/claim/finish commands | Event default and App-command IPC behavior stay |
| Workflow, conversation, setup and other App views | Existing frontend invoke calls and host command handlers | No command permission changes in this slice |
| Webview constructs/relabels/replaces/pops up a Tauri menu | core:menu IPC; no maintained frontend consumer found | Denied before menu handler execution |
| Native UI/Accessibility operator selecting existing controls/menus | OS/native route, subject to its actual authorization and availability | Not removed by IPC capability narrowing; effectiveness remains native qualification |

No maintained app/src menu/tray import or plugin:menu invocation was found at the
source basis. Existing core/event consumers remain. The Tauri tray component is
preserved as approved; its menu arguments use existing webview menu resource IDs
rather than creating arbitrary menu item payloads. This is not a general tray,
window, event, filesystem or webview-hardening project. Native menus and HTML/
browser context menus are not removed. New future frontend Tauri-menu features
would require an explicit permission decision rather than relying on the former
broad default.

## Agent versus human operation: precise distinction

An authorized UI/Accessibility agent can attempt the same existing native menu
selection or visible App control as an operator where the actual UI surface and
permission allow it. This narrowing does not remove that route. It removes the
webview's separate power to manufacture menu objects/IDs, relabel controls or
replace menus—capabilities an ordinary visible workflow did not need. Existing
App command paths remain available under their own host checks; no new generic
agent command or trusted caller is introduced.

Neither this permission change nor a native click establishes universal agent/
human functional parity. Native dialog/window accessibility and timing may
limit actual automation; source/mock checks cannot settle that. A request to
perform an action is distinct from the required affirmative native confirmation
and from the provider's authority checks. An agent performing an authorized
technical test remains agent-attributed. Actual owner acceptance, publication,
professional reliance and other person-reserved acts cannot be inferred from
an agent's click or successful command. SEAL-2 personal/native-origin/exclusive-
agent guarantees are not adopted.

Before this change, core:menu allowed web content to create a matching-ID menu
whose click reached the global listener without authenticated creator origin.
This specific webview construction/mutation route is now denied by IPC ACL on a
fresh narrowed build. The native listener itself still uses an ID, not an
origin-authentication token, and OS/native automation remains possible. The
current selection requires a macOS release build and compiled publisher selection
before SEAL-C is offered; dispatch without that eligibility is refused. The
provider still independently checks authority and policy. No source test is
relabelled as a native
or signed-production witness, and an already-running older process is not
claimed to have its resources revoked by a source change.

## Verification and receiving

`tests/menu_capability.rs` resolves the actual generated ACL with the locked
Tauri resolver, compares old/new command sets, checks exact capability/window/
origin scope and schema, and rejects additive capability files until reviewed.
It installs that resolved authority in Tauri's MockRuntime and sends actual IPC
requests: all menu commands must return permission refusal before argument
parsing, including a fabricated SEAL-C menu ID. A registered test App command
and Waiting-event listen/unlisten must succeed, while another window remains
outside the grant. These are actual mock IPC admission tests, not evidence that
an AppKit menu was operated. Existing native-waiting, enrollment, confirmation
and Quit source cohorts plus frontend Waiting bridge tests retain their value.

The focused integration test joins existing PR CI without removing any filter.
An initial macOS test using the Windows HTTP localhost origin received remote-origin
refusal. The corrected mock tests use the local `tauri://` origin for both menu
refusal and event/App-command admission. Actual native effectiveness and selected signed/
installed v4 functional testing remain separate, with no keychain or signing
activation implied by these source permissions.
