# P3 production role candidate

Basis: `015f9763ead9294b3857038e5d9cbaf2f9816244`. Executor: TASK
`/root/distribution_integration_manager/production_roles`, native descendant
of WORKING_ITEMS `/root/distribution_integration_manager`; no delegation.
Actual brief and subsequent dispositions are in native harness history.

The production `resources/instructions/roles.json` derives exactly four roles
from WD §5.1 and ROLE §4.1, with the current guidance file paths and delegation
relationships. The versioned serialization is an implementation choice.
All `default_for_new_chat` values are false under the parent-relayed HELP_HUMAN
candidate disposition. U-R11 remains with App role-guidance owner before release;
U-R6 remains with App/shared contract owners before allocation. This app-local
candidate placement settles neither matter. No prototype data is authority.
`ROLE_SET_SOURCE_BINDING.json` binds the exact role asset, current guidance,
SoW, WD, ROLE and unchanged historical SOURCE_MAP. Historical guidance/source-map
bytes were not changed. No instruction amendment, release or whole-pin refresh.

`Composition::new` validates the production set before any composition and
records its exact-byte identity privately. `compose_role` and seeding validate
the set in the actual App path. Missing/duplicate/unknown roles, multiple defaults,
wrong meanings, paths and delegation relationships refuse with role-set-invalid.
`start_record` exposes selection.roleSet; the actual HistorySession dispatch
receipt keeps roleSet across reconciliation. Identity hashes source bytes without
JSON normalization. Modified editable guidance stays modified and missing guidance
refuses rather than silently falling back. TASK delegation stays stated, not
enforced; native child supply stays not-supplied.

## Shared wiring to integrate after this frozen contribution

In `lib.rs`, `thread_start`, add `"roleSet":composition.role_set_identity()`
to both `role_supply_status` JSON objects (starting and final). Replace the
`let composition = runtime_session::compose_role(&root, role)?;` line with:

```rust
let composition = match runtime_session::compose_role(&root, role) {
    Ok(composition) => composition,
    Err(reason) => {
        *home.role_supply_status.lock().unwrap() = json!({
            "state":"refused-before-send", "selection":role,
            "roleSet":role_supply::content(role_supply::BUNDLED_ROLE_SET),
            "reason":reason, "adoption":"unknown"
        });
        return Err(reason);
    }
};
```

The existing actual Host join test
`history_bridge_joined_session_consumes_genuine_history_and_frozen_role_start_receipts`
can gain an assertion after reconcile that `session.snapshot(None)["startReceipts"][0]["roleSet"]` retains `content(BUNDLED_ROLE_SET)`;
P3 does not edit hosting.rs.
The metadata accessor `bundled_role_set()` returns role rows and `default_role()`;
use this for an explicit role-list/preselection consumer rather than another default.
All-false currently agrees with the existing no-role draft selection.

## Limits

No download, supplier process, model call, credentials, native window, package
release or consumer adoption. Existing TASK primary-entry refusal remains unchanged;
this bounded asset work does not settle that separate existing selection behavior.
Cold role-source persistence is still the prior owner’s unfinished work. Start
receipt identity custody here is process-local. Parent owns shared wiring and
independent review before integration. No push performed.

The physical package correspondence helper is
`runtime_session::verify_production_instructions_root(root)`. Before production
start, the native owner must call it using the actual
`app.path().resource_dir()?.join("instructions")`, with native errors converted
to the command's String error type; no development/embedded fallback. It
opens all path components through retained parent descriptors with O_NOFOLLOW
on Unix and compares roles, common guidance, all four roles and the new source
binding to compiled exact bytes. Non-Unix targets explicitly refuse. The return
identifies correspondence, not release qualification. This helper needs the
parent's native resource/start wiring to become the physical-package gate.

## Checks on this contribution

Offline Rust, prepared Cargo cache, isolated temporary target, supplier skip enabled:

- `cargo test --offline --locked --lib p3_`: 5 passed on final code.
- `cargo test --offline --locked --test role_lifecycle --test history_integration --test workflow_role`: role_lifecycle 9 and history_integration 7 passed; workflow_role executable contains 0 test-harness cases (not counted as behavioral coverage).
- `cargo test --offline --locked --lib workflow_role_tests`: 21 passed on final code.
- `cargo test --offline --locked --lib history_bridge_joined_session_consumes_genuine_history_and_frozen_role_start_receipts`: 1 passed after receipt identity retention; later changes added package verification and relocated test module, not this receipt behavior.
- `git diff --check`: passed.

Initial sandbox build was refused because generated worktree files lie outside
inherited writable roots; scoped escalation completed it. Initial regression
compilation exposed P3 test-module placement under a source file reused by
standalone integration tests. Moving the P3 module to runtime_session repaired
that import failure; affected suites above passed afterwards. Existing unused/
dead-code warnings remain; no new supplier result inferred from compilation.

Configured identity verified Ryan C Tufts <ryan@chirality.ai>; author/committer/
EMAIL environment overrides absent. Official staged private-term validation is
required immediately before this contribution's commit. The commit is the frozen
candidate identity returned to the manager; acceptance/review stay separate.
