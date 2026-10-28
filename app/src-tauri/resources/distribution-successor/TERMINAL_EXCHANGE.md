# Synthetic terminal reader exchange v1

`group-b-s1-terminal-reader-exchange.v1` is a separate cfg(test)-only transport for Group B receiving tests. It leaves `group-b-s1-reader-exchange.v1` and its LT-09 exporter unchanged. This route uses an invented offline child, not the native App or supplier.

A completed case has `exchange.json`, `predecessor/publication/`, `terminal/publication/`, and, only for a selected case, `selected-source/`. Publication directories contain every untouched raw member, including transport. Original source/mirror locator strings are preserved as historical provenance; they are not rebased to exchange paths or instructions to read ambient paths.

The exchange top object is closed:

| Field | Value |
|---|---|
| format | `group-b-s1-terminal-reader-exchange.v1` |
| case | `selected` or `unselected` |
| producer | Same closed producer fields as the LT-09 exchange: sourceRevision, harnessExecutableSha256, command, features, kind |
| applicationCandidate | Explicit `INVENTED-S4-APP-REVISION`, `INVENTED-S4-APP-BUILD`, standing `invented-consumer-fixture` |
| predecessor | Closed object: readback, actualLt09, members |
| terminal | Closed object: readback, actualLt23, members |
| selectedSourceMembers | Complete original selected-source member array, or null with no selected-source directory |

Producer sourceRevision is lowercase 40-hex; harnessExecutableSha256 is lowercase 64-hex; command is the actual nonempty argv array; features are sorted unique strings; kind is `synthetic-host-test`. Member arrays are sorted by contained POSIX-relative path, with exact lowercase64 sha256 and integer byte size. Empty, absolute, dot/dotdot, backslash, duplicate and ancestor-collision paths refuse. Each publication's member paths resolve only within its own publication directory.

The producer captures an already installed LT-09 native reference, actual full event, successful Host read and raw closure before actual Stop. It retains native capabilities in memory, never reconstructs them from JSON. After the actual worker settles successfully, it obtains LT-23 through Host and re-reads the original predecessor through its retained Store/reference. It requires full H5 equality, increasing actual event sequence, distinct publication names, unchanged observation bytes/reference, exact whole legacy events, unchanged source association and complete original source bytes. Pending, unavailable, busy, worker failure or test deadline expiry cannot issue a completed exchange. No queue, retry or worker join is added.

The output is a fresh private directory under an explicitly supplied physical temporary parent. Descriptor-based no-follow traversal and exclusive creation remain associated through final marker publication. Copied bytes, full directory membership/modes, original native reads and actual source/event are rechecked. The final marker is created without overwrite only after these checks; partial output remains diagnostic. These are bounded observations, not an atomic snapshot or future integrity guarantee. Test waiting uses a finite polling deadline; filesystem calls are not thereby cancellable or given a product SLA.

## Invocation and source standing

Use the ignored Rust test `hosting::successor::tests::terminal_export::export_group_b_terminal_selected_and_unselected` with `CHIRALITY_TERMINAL_EXPORT_ROOT` set to an existing physical private temporary directory. Use the prepared offline Cargo environment and the shared target authorized by the owning run. It creates fresh `selected` and `unselected` children and refuses existing destinations.

A clean checkout plus byte equality between committed/current and compiled exporter, Host, fixture, Store and selection source is required for `exchange.json`. The actual harness executable digest and argv are retained. Usable receiving exports are rerun after reviewed source commit and recompilation. These checks do not authenticate the commit, build history, or an invented application candidate.

An explicitly requested `CHIRALITY_TERMINAL_DIAGNOSTIC=1` dirty-source run writes only `exchange.diagnostic.json`, never `exchange.json`. Its outer `DIAGNOSTIC_SOURCE.json` identifies the checkout base and compiled exporter hash and explicitly states that the base does not contain uncommitted work. Such output is a diagnostic precursor, not a completed receiving exchange. Group B must not accept the diagnostic filename as the completion marker.

No production semantics, canonical schemas/pins, supplier selection, issuer, S3, SEAL-2, restart hydration, history index or qualification is introduced. Independent source review and Group B named consumer adoption remain separate from producer test success.
