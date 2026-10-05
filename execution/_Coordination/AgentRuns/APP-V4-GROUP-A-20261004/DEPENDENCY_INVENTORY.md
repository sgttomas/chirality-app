# Offline dependency inventory — APP-V4-GROUP-A-20261004

Standing: bounded TASK return for `/root/group_a_execution`; inventory and recommendations only. No download approval, selected new dependency, authentication, live turn, application edit or Git mutation. Original offline brief was amended by parent to authorize read-only official registry metadata and HTTP HEAD requests only; that amendment was received and used as described below. Observation date 2026-10-04.

## Decision route

**Decision-ready preferred proposal:** pin `jsonschema = { version = "=0.58.5", default-features = false }`. Official tagged sources declare MSRV1.85.0 and draft2020-12 support. The refined prospective application lock requires **29 absent incremental archives totaling3,223,082 compressed bytes**, each named with official URL, HEAD size and registry SHA-256 below. It preserves current app dependency versions except regex-automata0.4.14→0.4.18 and reuses cached ahash0.8.12. Compilation/API correctness and runtime schema refusal are not yet tested.

**Frozen broader proposal requested by parent:** the isolated fresh validator lock has **49 absent archives totaling5,564,835 compressed bytes**. Every one has official HEAD Content-Length and registry SHA-256 in the49-archive tables. It includes foreign targets and avoidable updates; it is a complete upper-bound package set for that prospective lock, not the preferred application integration lock. Do not silently adopt tauri-utils/Tauri-family upgrades from earlier incomplete-metadata probes.

The four required same-release core archives total1,235,736 bytes, already included in each complete proposal. Metadata traffic, unpacked cache space and build output disk usage are outside these compressed-byte totals. No download approval or archive retrieval has occurred. Parent can present either precise artifact set for owner yes, then fetch only the approved set and verify each registry checksum. Native baseline cache verification remains with T0;192 old whole-platform archive misses are not additions caused by this validator.

CI-9 implementation must preserve RS W-1: validate before append; invalid instances, unresolved references, malformed schemas or validator setup failure refuse the write. Ajv in a test validates output after the fact and is not the runtime writer gate. Cached `schemars` derives/generates schemas; it does not satisfy the required instance validator.

## Current skeleton and cache evidence

- Actual working root: `/Users/ryan/.codex/worktrees/077c/chirality`. No Git command was run; root was recovered from supplied cwd and root `AGENTS.md` presence.
- Toolchain observed: rustc 1.92.0; Node v24.5.0; cargo/rustc at `/Users/ryan/.cargo/bin/`; npm/node at `/opt/homebrew/bin/`.
- No `app/node_modules/` or `app/src-tauri/target/` exists in this worktree at inspection. Prior walking-skeleton build evidence is historical, not a build of this checkout.
- Cargo.lock: 446 registry packages; 254 compressed archives present, totaling 18,582,712 bytes on disk; 192 archives and matching extracted source directories absent. This is the entire cross-platform lockfile, not a native-platform fetch requirement.
- npm package-lock.json: 136 packages; 77 exact locked tarballs have cache metadata and existing content files totaling 23,116,586 bytes. 59 absent entries are all optional foreign-platform binaries; no required darwin-arm64 tarball is missing. Metadata entries with absent content files: 0. Content presence/size was checked; archive integrity and installation were not rerun.
- Parent should serialize `cargo test --offline --locked --no-run` with its Cargo work to identify the native Rust closure. This child did not acquire Cargo build locks or run supplier processes. Missing foreign target crates below are not a request to download them.

| Direct Rust dependency | Locked version | Archive available |
|---|---|---|
| tauri | 2.11.1 | yes |
| tauri-build | 2.6.1 | yes |
| tauri-plugin-dialog | 2.7.2 | yes |
| serde | 1.0.229 | yes |
| serde_json | 1.0.151 | yes |
| sha2 | 0.10.9 | yes |
| libc | 0.2.189 | yes |

| Direct npm dependency | Exact manifest version | Local cache content |
|---|---|---|
| @tauri-apps/api | 2.11.0 | present |
| react | 19.2.7 | present |
| react-dom | 19.2.7 | present |
| @tauri-apps/cli | 2.11.1 | present |
| @types/react | 19.2.14 | present |
| @types/react-dom | 19.2.3 | present |
| @vitejs/plugin-react | 5.2.0 | present |
| ajv | 8.20.0 | present |
| typescript | 5.9.3 | present |
| vite | 7.3.6 | present |

## Feature needs and scope limits

| Feature slice | Dependency implication |
|---|---|
| W-1 schema gate (CI-9) | Candidate exact pin0.58.5 established by authorized official metadata; preferred29-archive incremental set3,223,082 bytes below. |
| Hosting, restart, request register, replay and context/role/workflow supply | No new third-party dependency is established by the present manifests or evidence; ready implementation can start with std, serde/serde_json, sha2 and existing Tauri APIs. This is not proof every future slice needs none. |
| Record append/repair, atomic capture, id/time choices, local projections | Existing primitives are available; placement/contract decisions and correctness work remain. Do not turn implementation gaps into speculative package requests. |
| `.app`/`.dmg` packaging | Historical bundle.active=false; bundle path was not tested. External bundler tools/assets are unclassified and their total is unknown. Requires a separate packaging build inventory when that scope is ready. |
| Other OS targets | Foreign target cache misses are listed for traceability; system SDK/toolchain needs and qualification are outside this inventory. |
| Real Codex/model path | Stock binary/provider/authentication are coordinated by parent; none inspected or downloaded here. |

## Exact missing Cargo archives (whole lockfile)

Size is **unknown for every row**: Cargo.lock/sparse index preserve checksums and dependency metadata, not compressed crate size. Targets and selected features must be resolved before requesting any of these artifacts. The rows identify potential files, not an approved download set.

| Package | Version | File/source | Size (bytes) |
|---|---|---|---|
| android_system_properties | 0.1.5 | https://static.crates.io/crates/android_system_properties/android_system_properties-0.1.5.crate | unknown |
| atk | 0.18.2 | https://static.crates.io/crates/atk/atk-0.18.2.crate | unknown |
| atk-sys | 0.18.2 | https://static.crates.io/crates/atk-sys/atk-sys-0.18.2.crate | unknown |
| atomic-waker | 1.1.2 | https://static.crates.io/crates/atomic-waker/atomic-waker-1.1.2.crate | unknown |
| bytemuck | 1.25.2 | https://static.crates.io/crates/bytemuck/bytemuck-1.25.2.crate | unknown |
| cairo-rs | 0.18.5 | https://static.crates.io/crates/cairo-rs/cairo-rs-0.18.5.crate | unknown |
| cairo-sys-rs | 0.18.2 | https://static.crates.io/crates/cairo-sys-rs/cairo-sys-rs-0.18.2.crate | unknown |
| cesu8 | 1.1.0 | https://static.crates.io/crates/cesu8/cesu8-1.1.0.crate | unknown |
| cfg-expr | 0.15.8 | https://static.crates.io/crates/cfg-expr/cfg-expr-0.15.8.crate | unknown |
| combine | 4.6.7 | https://static.crates.io/crates/combine/combine-4.6.7.crate | unknown |
| dbus | 0.9.12 | https://static.crates.io/crates/dbus/dbus-0.9.12.crate | unknown |
| dlopen2 | 0.8.2 | https://static.crates.io/crates/dlopen2/dlopen2-0.8.2.crate | unknown |
| dlopen2_derive | 0.4.3 | https://static.crates.io/crates/dlopen2_derive/dlopen2_derive-0.4.3.crate | unknown |
| field-offset | 0.3.6 | https://static.crates.io/crates/field-offset/field-offset-0.3.6.crate | unknown |
| foldhash | 0.1.5 | https://static.crates.io/crates/foldhash/foldhash-0.1.5.crate | unknown |
| futures-channel | 0.3.33 | https://static.crates.io/crates/futures-channel/futures-channel-0.3.33.crate | unknown |
| futures-core | 0.3.33 | https://static.crates.io/crates/futures-core/futures-core-0.3.33.crate | unknown |
| futures-executor | 0.3.33 | https://static.crates.io/crates/futures-executor/futures-executor-0.3.33.crate | unknown |
| futures-io | 0.3.33 | https://static.crates.io/crates/futures-io/futures-io-0.3.33.crate | unknown |
| futures-macro | 0.3.33 | https://static.crates.io/crates/futures-macro/futures-macro-0.3.33.crate | unknown |
| futures-sink | 0.3.33 | https://static.crates.io/crates/futures-sink/futures-sink-0.3.33.crate | unknown |
| futures-task | 0.3.33 | https://static.crates.io/crates/futures-task/futures-task-0.3.33.crate | unknown |
| futures-util | 0.3.33 | https://static.crates.io/crates/futures-util/futures-util-0.3.33.crate | unknown |
| gdk | 0.18.2 | https://static.crates.io/crates/gdk/gdk-0.18.2.crate | unknown |
| gdk-pixbuf | 0.18.5 | https://static.crates.io/crates/gdk-pixbuf/gdk-pixbuf-0.18.5.crate | unknown |
| gdk-pixbuf-sys | 0.18.0 | https://static.crates.io/crates/gdk-pixbuf-sys/gdk-pixbuf-sys-0.18.0.crate | unknown |
| gdk-sys | 0.18.2 | https://static.crates.io/crates/gdk-sys/gdk-sys-0.18.2.crate | unknown |
| gdkwayland-sys | 0.18.2 | https://static.crates.io/crates/gdkwayland-sys/gdkwayland-sys-0.18.2.crate | unknown |
| gdkx11 | 0.18.2 | https://static.crates.io/crates/gdkx11/gdkx11-0.18.2.crate | unknown |
| gdkx11-sys | 0.18.2 | https://static.crates.io/crates/gdkx11-sys/gdkx11-sys-0.18.2.crate | unknown |
| getrandom | 0.2.17 | https://static.crates.io/crates/getrandom/getrandom-0.2.17.crate | unknown |
| gio | 0.18.4 | https://static.crates.io/crates/gio/gio-0.18.4.crate | unknown |
| gio-sys | 0.18.1 | https://static.crates.io/crates/gio-sys/gio-sys-0.18.1.crate | unknown |
| glib | 0.18.5 | https://static.crates.io/crates/glib/glib-0.18.5.crate | unknown |
| glib-macros | 0.18.5 | https://static.crates.io/crates/glib-macros/glib-macros-0.18.5.crate | unknown |
| glib-sys | 0.18.1 | https://static.crates.io/crates/glib-sys/glib-sys-0.18.1.crate | unknown |
| gobject-sys | 0.18.0 | https://static.crates.io/crates/gobject-sys/gobject-sys-0.18.0.crate | unknown |
| gtk | 0.18.2 | https://static.crates.io/crates/gtk/gtk-0.18.2.crate | unknown |
| gtk-sys | 0.18.2 | https://static.crates.io/crates/gtk-sys/gtk-sys-0.18.2.crate | unknown |
| gtk3-macros | 0.18.2 | https://static.crates.io/crates/gtk3-macros/gtk3-macros-0.18.2.crate | unknown |
| hashbrown | 0.15.5 | https://static.crates.io/crates/hashbrown/hashbrown-0.15.5.crate | unknown |
| heck | 0.4.1 | https://static.crates.io/crates/heck/heck-0.4.1.crate | unknown |
| http-body | 1.1.0 | https://static.crates.io/crates/http-body/http-body-1.1.0.crate | unknown |
| http-body-util | 0.1.4 | https://static.crates.io/crates/http-body-util/http-body-util-0.1.4.crate | unknown |
| httparse | 1.10.1 | https://static.crates.io/crates/httparse/httparse-1.10.1.crate | unknown |
| hyper | 1.11.0 | https://static.crates.io/crates/hyper/hyper-1.11.0.crate | unknown |
| hyper-util | 0.1.20 | https://static.crates.io/crates/hyper-util/hyper-util-0.1.20.crate | unknown |
| iana-time-zone-haiku | 0.1.2 | https://static.crates.io/crates/iana-time-zone-haiku/iana-time-zone-haiku-0.1.2.crate | unknown |
| id-arena | 2.3.0 | https://static.crates.io/crates/id-arena/id-arena-2.3.0.crate | unknown |
| ipnet | 2.12.0 | https://static.crates.io/crates/ipnet/ipnet-2.12.0.crate | unknown |
| javascriptcore-rs | 1.1.2 | https://static.crates.io/crates/javascriptcore-rs/javascriptcore-rs-1.1.2.crate | unknown |
| javascriptcore-rs-sys | 1.1.1 | https://static.crates.io/crates/javascriptcore-rs-sys/javascriptcore-rs-sys-1.1.1.crate | unknown |
| jni | 0.21.1 | https://static.crates.io/crates/jni/jni-0.21.1.crate | unknown |
| jni-sys | 0.3.1 | https://static.crates.io/crates/jni-sys/jni-sys-0.3.1.crate | unknown |
| jni-sys | 0.4.1 | https://static.crates.io/crates/jni-sys/jni-sys-0.4.1.crate | unknown |
| jni-sys-macros | 0.4.1 | https://static.crates.io/crates/jni-sys-macros/jni-sys-macros-0.4.1.crate | unknown |
| js-sys | 0.3.100 | https://static.crates.io/crates/js-sys/js-sys-0.3.100.crate | unknown |
| leb128fmt | 0.1.0 | https://static.crates.io/crates/leb128fmt/leb128fmt-0.1.0.crate | unknown |
| libappindicator | 0.9.0 | https://static.crates.io/crates/libappindicator/libappindicator-0.9.0.crate | unknown |
| libappindicator-sys | 0.9.0 | https://static.crates.io/crates/libappindicator-sys/libappindicator-sys-0.9.0.crate | unknown |
| libdbus-sys | 0.2.7 | https://static.crates.io/crates/libdbus-sys/libdbus-sys-0.2.7.crate | unknown |
| libloading | 0.7.4 | https://static.crates.io/crates/libloading/libloading-0.7.4.crate | unknown |
| libredox | 0.1.18 | https://static.crates.io/crates/libredox/libredox-0.1.18.crate | unknown |
| memoffset | 0.9.1 | https://static.crates.io/crates/memoffset/memoffset-0.9.1.crate | unknown |
| ndk | 0.9.0 | https://static.crates.io/crates/ndk/ndk-0.9.0.crate | unknown |
| ndk-sys | 0.6.0+11769913 | https://static.crates.io/crates/ndk-sys/ndk-sys-0.6.0+11769913.crate | unknown |
| num_enum | 0.7.6 | https://static.crates.io/crates/num_enum/num_enum-0.7.6.crate | unknown |
| num_enum_derive | 0.7.6 | https://static.crates.io/crates/num_enum_derive/num_enum_derive-0.7.6.crate | unknown |
| objc2-cloud-kit | 0.3.2 | https://static.crates.io/crates/objc2-cloud-kit/objc2-cloud-kit-0.3.2.crate | unknown |
| objc2-core-data | 0.3.2 | https://static.crates.io/crates/objc2-core-data/objc2-core-data-0.3.2.crate | unknown |
| objc2-core-image | 0.3.2 | https://static.crates.io/crates/objc2-core-image/objc2-core-image-0.3.2.crate | unknown |
| objc2-core-location | 0.3.2 | https://static.crates.io/crates/objc2-core-location/objc2-core-location-0.3.2.crate | unknown |
| objc2-core-text | 0.3.2 | https://static.crates.io/crates/objc2-core-text/objc2-core-text-0.3.2.crate | unknown |
| objc2-quartz-core | 0.3.2 | https://static.crates.io/crates/objc2-quartz-core/objc2-quartz-core-0.3.2.crate | unknown |
| objc2-ui-kit | 0.3.2 | https://static.crates.io/crates/objc2-ui-kit/objc2-ui-kit-0.3.2.crate | unknown |
| objc2-user-notifications | 0.3.2 | https://static.crates.io/crates/objc2-user-notifications/objc2-user-notifications-0.3.2.crate | unknown |
| pango | 0.18.3 | https://static.crates.io/crates/pango/pango-0.18.3.crate | unknown |
| pango-sys | 0.18.0 | https://static.crates.io/crates/pango-sys/pango-sys-0.18.0.crate | unknown |
| prettyplease | 0.2.37 | https://static.crates.io/crates/prettyplease/prettyplease-0.2.37.crate | unknown |
| proc-macro-crate | 1.3.1 | https://static.crates.io/crates/proc-macro-crate/proc-macro-crate-1.3.1.crate | unknown |
| proc-macro-crate | 2.0.2 | https://static.crates.io/crates/proc-macro-crate/proc-macro-crate-2.0.2.crate | unknown |
| proc-macro-crate | 3.5.0 | https://static.crates.io/crates/proc-macro-crate/proc-macro-crate-3.5.0.crate | unknown |
| proc-macro-error | 1.0.4 | https://static.crates.io/crates/proc-macro-error/proc-macro-error-1.0.4.crate | unknown |
| proc-macro-error-attr | 1.0.4 | https://static.crates.io/crates/proc-macro-error-attr/proc-macro-error-attr-1.0.4.crate | unknown |
| r-efi | 5.3.0 | https://static.crates.io/crates/r-efi/r-efi-5.3.0.crate | unknown |
| r-efi | 6.0.0 | https://static.crates.io/crates/r-efi/r-efi-6.0.0.crate | unknown |
| redox_syscall | 0.5.18 | https://static.crates.io/crates/redox_syscall/redox_syscall-0.5.18.crate | unknown |
| redox_users | 0.5.2 | https://static.crates.io/crates/redox_users/redox_users-0.5.2.crate | unknown |
| reqwest | 0.13.4 | https://static.crates.io/crates/reqwest/reqwest-0.13.4.crate | unknown |
| serde_spanned | 0.6.9 | https://static.crates.io/crates/serde_spanned/serde_spanned-0.6.9.crate | unknown |
| slab | 0.4.12 | https://static.crates.io/crates/slab/slab-0.4.12.crate | unknown |
| softbuffer | 0.4.8 | https://static.crates.io/crates/softbuffer/softbuffer-0.4.8.crate | unknown |
| soup3 | 0.5.0 | https://static.crates.io/crates/soup3/soup3-0.5.0.crate | unknown |
| soup3-sys | 0.5.0 | https://static.crates.io/crates/soup3-sys/soup3-sys-0.5.0.crate | unknown |
| syn | 1.0.109 | https://static.crates.io/crates/syn/syn-1.0.109.crate | unknown |
| sync_wrapper | 1.0.2 | https://static.crates.io/crates/sync_wrapper/sync_wrapper-1.0.2.crate | unknown |
| system-deps | 6.2.2 | https://static.crates.io/crates/system-deps/system-deps-6.2.2.crate | unknown |
| tao-macros | 0.1.3 | https://static.crates.io/crates/tao-macros/tao-macros-0.1.3.crate | unknown |
| target-lexicon | 0.12.16 | https://static.crates.io/crates/target-lexicon/target-lexicon-0.12.16.crate | unknown |
| tokio-util | 0.7.19 | https://static.crates.io/crates/tokio-util/tokio-util-0.7.19.crate | unknown |
| toml | 0.8.2 | https://static.crates.io/crates/toml/toml-0.8.2.crate | unknown |
| toml_datetime | 0.6.3 | https://static.crates.io/crates/toml_datetime/toml_datetime-0.6.3.crate | unknown |
| toml_edit | 0.19.15 | https://static.crates.io/crates/toml_edit/toml_edit-0.19.15.crate | unknown |
| toml_edit | 0.20.2 | https://static.crates.io/crates/toml_edit/toml_edit-0.20.2.crate | unknown |
| toml_edit | 0.25.13+spec-1.1.0 | https://static.crates.io/crates/toml_edit/toml_edit-0.25.13+spec-1.1.0.crate | unknown |
| tower | 0.5.3 | https://static.crates.io/crates/tower/tower-0.5.3.crate | unknown |
| tower-http | 0.6.11 | https://static.crates.io/crates/tower-http/tower-http-0.6.11.crate | unknown |
| tower-layer | 0.3.3 | https://static.crates.io/crates/tower-layer/tower-layer-0.3.3.crate | unknown |
| tower-service | 0.3.3 | https://static.crates.io/crates/tower-service/tower-service-0.3.3.crate | unknown |
| tracing | 0.1.44 | https://static.crates.io/crates/tracing/tracing-0.1.44.crate | unknown |
| tracing-core | 0.1.36 | https://static.crates.io/crates/tracing-core/tracing-core-0.1.36.crate | unknown |
| try-lock | 0.2.5 | https://static.crates.io/crates/try-lock/try-lock-0.2.5.crate | unknown |
| unicode-xid | 0.2.6 | https://static.crates.io/crates/unicode-xid/unicode-xid-0.2.6.crate | unknown |
| version-compare | 0.2.1 | https://static.crates.io/crates/version-compare/version-compare-0.2.1.crate | unknown |
| vswhom | 0.1.0 | https://static.crates.io/crates/vswhom/vswhom-0.1.0.crate | unknown |
| vswhom-sys | 0.1.3 | https://static.crates.io/crates/vswhom-sys/vswhom-sys-0.1.3.crate | unknown |
| want | 0.3.1 | https://static.crates.io/crates/want/want-0.3.1.crate | unknown |
| wasi | 0.11.1+wasi-snapshot-preview1 | https://static.crates.io/crates/wasi/wasi-0.11.1+wasi-snapshot-preview1.crate | unknown |
| wasip2 | 1.0.4+wasi-0.2.12 | https://static.crates.io/crates/wasip2/wasip2-1.0.4+wasi-0.2.12.crate | unknown |
| wasip3 | 0.4.0+wasi-0.3.0-rc-2026-01-06 | https://static.crates.io/crates/wasip3/wasip3-0.4.0+wasi-0.3.0-rc-2026-01-06.crate | unknown |
| wasm-bindgen-futures | 0.4.73 | https://static.crates.io/crates/wasm-bindgen-futures/wasm-bindgen-futures-0.4.73.crate | unknown |
| wasm-encoder | 0.244.0 | https://static.crates.io/crates/wasm-encoder/wasm-encoder-0.244.0.crate | unknown |
| wasm-metadata | 0.244.0 | https://static.crates.io/crates/wasm-metadata/wasm-metadata-0.244.0.crate | unknown |
| wasm-streams | 0.5.0 | https://static.crates.io/crates/wasm-streams/wasm-streams-0.5.0.crate | unknown |
| wasmparser | 0.244.0 | https://static.crates.io/crates/wasmparser/wasmparser-0.244.0.crate | unknown |
| web-sys | 0.3.100 | https://static.crates.io/crates/web-sys/web-sys-0.3.100.crate | unknown |
| webkit2gtk | 2.0.2 | https://static.crates.io/crates/webkit2gtk/webkit2gtk-2.0.2.crate | unknown |
| webkit2gtk-sys | 2.0.2 | https://static.crates.io/crates/webkit2gtk-sys/webkit2gtk-sys-2.0.2.crate | unknown |
| webview2-com | 0.38.2 | https://static.crates.io/crates/webview2-com/webview2-com-0.38.2.crate | unknown |
| webview2-com-macros | 0.8.1 | https://static.crates.io/crates/webview2-com-macros/webview2-com-macros-0.8.1.crate | unknown |
| webview2-com-sys | 0.38.2 | https://static.crates.io/crates/webview2-com-sys/webview2-com-sys-0.38.2.crate | unknown |
| winapi | 0.3.9 | https://static.crates.io/crates/winapi/winapi-0.3.9.crate | unknown |
| winapi-i686-pc-windows-gnu | 0.4.0 | https://static.crates.io/crates/winapi-i686-pc-windows-gnu/winapi-i686-pc-windows-gnu-0.4.0.crate | unknown |
| winapi-util | 0.1.11 | https://static.crates.io/crates/winapi-util/winapi-util-0.1.11.crate | unknown |
| winapi-x86_64-pc-windows-gnu | 0.4.0 | https://static.crates.io/crates/winapi-x86_64-pc-windows-gnu/winapi-x86_64-pc-windows-gnu-0.4.0.crate | unknown |
| windows | 0.61.3 | https://static.crates.io/crates/windows/windows-0.61.3.crate | unknown |
| windows-collections | 0.2.0 | https://static.crates.io/crates/windows-collections/windows-collections-0.2.0.crate | unknown |
| windows-core | 0.61.2 | https://static.crates.io/crates/windows-core/windows-core-0.61.2.crate | unknown |
| windows-core | 0.62.2 | https://static.crates.io/crates/windows-core/windows-core-0.62.2.crate | unknown |
| windows-future | 0.2.1 | https://static.crates.io/crates/windows-future/windows-future-0.2.1.crate | unknown |
| windows-implement | 0.60.2 | https://static.crates.io/crates/windows-implement/windows-implement-0.60.2.crate | unknown |
| windows-interface | 0.59.3 | https://static.crates.io/crates/windows-interface/windows-interface-0.59.3.crate | unknown |
| windows-link | 0.1.3 | https://static.crates.io/crates/windows-link/windows-link-0.1.3.crate | unknown |
| windows-link | 0.2.1 | https://static.crates.io/crates/windows-link/windows-link-0.2.1.crate | unknown |
| windows-numerics | 0.2.0 | https://static.crates.io/crates/windows-numerics/windows-numerics-0.2.0.crate | unknown |
| windows-result | 0.3.4 | https://static.crates.io/crates/windows-result/windows-result-0.3.4.crate | unknown |
| windows-result | 0.4.1 | https://static.crates.io/crates/windows-result/windows-result-0.4.1.crate | unknown |
| windows-strings | 0.4.2 | https://static.crates.io/crates/windows-strings/windows-strings-0.4.2.crate | unknown |
| windows-strings | 0.5.1 | https://static.crates.io/crates/windows-strings/windows-strings-0.5.1.crate | unknown |
| windows-sys | 0.45.0 | https://static.crates.io/crates/windows-sys/windows-sys-0.45.0.crate | unknown |
| windows-sys | 0.59.0 | https://static.crates.io/crates/windows-sys/windows-sys-0.59.0.crate | unknown |
| windows-sys | 0.60.2 | https://static.crates.io/crates/windows-sys/windows-sys-0.60.2.crate | unknown |
| windows-sys | 0.61.2 | https://static.crates.io/crates/windows-sys/windows-sys-0.61.2.crate | unknown |
| windows-targets | 0.42.2 | https://static.crates.io/crates/windows-targets/windows-targets-0.42.2.crate | unknown |
| windows-targets | 0.52.6 | https://static.crates.io/crates/windows-targets/windows-targets-0.52.6.crate | unknown |
| windows-targets | 0.53.5 | https://static.crates.io/crates/windows-targets/windows-targets-0.53.5.crate | unknown |
| windows-threading | 0.1.0 | https://static.crates.io/crates/windows-threading/windows-threading-0.1.0.crate | unknown |
| windows-version | 0.1.7 | https://static.crates.io/crates/windows-version/windows-version-0.1.7.crate | unknown |
| windows_aarch64_gnullvm | 0.42.2 | https://static.crates.io/crates/windows_aarch64_gnullvm/windows_aarch64_gnullvm-0.42.2.crate | unknown |
| windows_aarch64_gnullvm | 0.52.6 | https://static.crates.io/crates/windows_aarch64_gnullvm/windows_aarch64_gnullvm-0.52.6.crate | unknown |
| windows_aarch64_gnullvm | 0.53.1 | https://static.crates.io/crates/windows_aarch64_gnullvm/windows_aarch64_gnullvm-0.53.1.crate | unknown |
| windows_aarch64_msvc | 0.42.2 | https://static.crates.io/crates/windows_aarch64_msvc/windows_aarch64_msvc-0.42.2.crate | unknown |
| windows_aarch64_msvc | 0.52.6 | https://static.crates.io/crates/windows_aarch64_msvc/windows_aarch64_msvc-0.52.6.crate | unknown |
| windows_aarch64_msvc | 0.53.1 | https://static.crates.io/crates/windows_aarch64_msvc/windows_aarch64_msvc-0.53.1.crate | unknown |
| windows_i686_gnu | 0.42.2 | https://static.crates.io/crates/windows_i686_gnu/windows_i686_gnu-0.42.2.crate | unknown |
| windows_i686_gnu | 0.52.6 | https://static.crates.io/crates/windows_i686_gnu/windows_i686_gnu-0.52.6.crate | unknown |
| windows_i686_gnu | 0.53.1 | https://static.crates.io/crates/windows_i686_gnu/windows_i686_gnu-0.53.1.crate | unknown |
| windows_i686_gnullvm | 0.52.6 | https://static.crates.io/crates/windows_i686_gnullvm/windows_i686_gnullvm-0.52.6.crate | unknown |
| windows_i686_gnullvm | 0.53.1 | https://static.crates.io/crates/windows_i686_gnullvm/windows_i686_gnullvm-0.53.1.crate | unknown |
| windows_i686_msvc | 0.42.2 | https://static.crates.io/crates/windows_i686_msvc/windows_i686_msvc-0.42.2.crate | unknown |
| windows_i686_msvc | 0.52.6 | https://static.crates.io/crates/windows_i686_msvc/windows_i686_msvc-0.52.6.crate | unknown |
| windows_i686_msvc | 0.53.1 | https://static.crates.io/crates/windows_i686_msvc/windows_i686_msvc-0.53.1.crate | unknown |
| windows_x86_64_gnu | 0.42.2 | https://static.crates.io/crates/windows_x86_64_gnu/windows_x86_64_gnu-0.42.2.crate | unknown |
| windows_x86_64_gnu | 0.52.6 | https://static.crates.io/crates/windows_x86_64_gnu/windows_x86_64_gnu-0.52.6.crate | unknown |
| windows_x86_64_gnu | 0.53.1 | https://static.crates.io/crates/windows_x86_64_gnu/windows_x86_64_gnu-0.53.1.crate | unknown |
| windows_x86_64_gnullvm | 0.42.2 | https://static.crates.io/crates/windows_x86_64_gnullvm/windows_x86_64_gnullvm-0.42.2.crate | unknown |
| windows_x86_64_gnullvm | 0.52.6 | https://static.crates.io/crates/windows_x86_64_gnullvm/windows_x86_64_gnullvm-0.52.6.crate | unknown |
| windows_x86_64_gnullvm | 0.53.1 | https://static.crates.io/crates/windows_x86_64_gnullvm/windows_x86_64_gnullvm-0.53.1.crate | unknown |
| windows_x86_64_msvc | 0.42.2 | https://static.crates.io/crates/windows_x86_64_msvc/windows_x86_64_msvc-0.42.2.crate | unknown |
| windows_x86_64_msvc | 0.52.6 | https://static.crates.io/crates/windows_x86_64_msvc/windows_x86_64_msvc-0.52.6.crate | unknown |
| windows_x86_64_msvc | 0.53.1 | https://static.crates.io/crates/windows_x86_64_msvc/windows_x86_64_msvc-0.53.1.crate | unknown |
| winnow | 0.5.40 | https://static.crates.io/crates/winnow/winnow-0.5.40.crate | unknown |
| winreg | 0.55.0 | https://static.crates.io/crates/winreg/winreg-0.55.0.crate | unknown |
| wit-bindgen | 0.51.0 | https://static.crates.io/crates/wit-bindgen/wit-bindgen-0.51.0.crate | unknown |
| wit-bindgen | 0.57.1 | https://static.crates.io/crates/wit-bindgen/wit-bindgen-0.57.1.crate | unknown |
| wit-bindgen-core | 0.51.0 | https://static.crates.io/crates/wit-bindgen-core/wit-bindgen-core-0.51.0.crate | unknown |
| wit-bindgen-rust | 0.51.0 | https://static.crates.io/crates/wit-bindgen-rust/wit-bindgen-rust-0.51.0.crate | unknown |
| wit-bindgen-rust-macro | 0.51.0 | https://static.crates.io/crates/wit-bindgen-rust-macro/wit-bindgen-rust-macro-0.51.0.crate | unknown |
| wit-component | 0.244.0 | https://static.crates.io/crates/wit-component/wit-component-0.244.0.crate | unknown |
| wit-parser | 0.244.0 | https://static.crates.io/crates/wit-parser/wit-parser-0.244.0.crate | unknown |
| x11 | 2.21.0 | https://static.crates.io/crates/x11/x11-2.21.0.crate | unknown |
| x11-dl | 2.21.0 | https://static.crates.io/crates/x11-dl/x11-dl-2.21.0.crate | unknown |

## Exact absent npm archives (optional foreign platforms)

All 59 are optional and do not match this macOS arm64 host. Sizes unknown locally. Exact source and version are from package-lock.json. Do not request these for native development.

| Package | Version | Source | Size (bytes) |
|---|---|---|---|
| @esbuild/aix-ppc64 | 0.28.1 | https://registry.npmjs.org/@esbuild/aix-ppc64/-/aix-ppc64-0.28.1.tgz | unknown |
| @esbuild/android-arm | 0.28.1 | https://registry.npmjs.org/@esbuild/android-arm/-/android-arm-0.28.1.tgz | unknown |
| @esbuild/android-arm64 | 0.28.1 | https://registry.npmjs.org/@esbuild/android-arm64/-/android-arm64-0.28.1.tgz | unknown |
| @esbuild/android-x64 | 0.28.1 | https://registry.npmjs.org/@esbuild/android-x64/-/android-x64-0.28.1.tgz | unknown |
| @esbuild/darwin-x64 | 0.28.1 | https://registry.npmjs.org/@esbuild/darwin-x64/-/darwin-x64-0.28.1.tgz | unknown |
| @esbuild/freebsd-arm64 | 0.28.1 | https://registry.npmjs.org/@esbuild/freebsd-arm64/-/freebsd-arm64-0.28.1.tgz | unknown |
| @esbuild/freebsd-x64 | 0.28.1 | https://registry.npmjs.org/@esbuild/freebsd-x64/-/freebsd-x64-0.28.1.tgz | unknown |
| @esbuild/linux-arm | 0.28.1 | https://registry.npmjs.org/@esbuild/linux-arm/-/linux-arm-0.28.1.tgz | unknown |
| @esbuild/linux-arm64 | 0.28.1 | https://registry.npmjs.org/@esbuild/linux-arm64/-/linux-arm64-0.28.1.tgz | unknown |
| @esbuild/linux-ia32 | 0.28.1 | https://registry.npmjs.org/@esbuild/linux-ia32/-/linux-ia32-0.28.1.tgz | unknown |
| @esbuild/linux-loong64 | 0.28.1 | https://registry.npmjs.org/@esbuild/linux-loong64/-/linux-loong64-0.28.1.tgz | unknown |
| @esbuild/linux-mips64el | 0.28.1 | https://registry.npmjs.org/@esbuild/linux-mips64el/-/linux-mips64el-0.28.1.tgz | unknown |
| @esbuild/linux-ppc64 | 0.28.1 | https://registry.npmjs.org/@esbuild/linux-ppc64/-/linux-ppc64-0.28.1.tgz | unknown |
| @esbuild/linux-riscv64 | 0.28.1 | https://registry.npmjs.org/@esbuild/linux-riscv64/-/linux-riscv64-0.28.1.tgz | unknown |
| @esbuild/linux-s390x | 0.28.1 | https://registry.npmjs.org/@esbuild/linux-s390x/-/linux-s390x-0.28.1.tgz | unknown |
| @esbuild/linux-x64 | 0.28.1 | https://registry.npmjs.org/@esbuild/linux-x64/-/linux-x64-0.28.1.tgz | unknown |
| @esbuild/netbsd-arm64 | 0.28.1 | https://registry.npmjs.org/@esbuild/netbsd-arm64/-/netbsd-arm64-0.28.1.tgz | unknown |
| @esbuild/netbsd-x64 | 0.28.1 | https://registry.npmjs.org/@esbuild/netbsd-x64/-/netbsd-x64-0.28.1.tgz | unknown |
| @esbuild/openbsd-arm64 | 0.28.1 | https://registry.npmjs.org/@esbuild/openbsd-arm64/-/openbsd-arm64-0.28.1.tgz | unknown |
| @esbuild/openbsd-x64 | 0.28.1 | https://registry.npmjs.org/@esbuild/openbsd-x64/-/openbsd-x64-0.28.1.tgz | unknown |
| @esbuild/openharmony-arm64 | 0.28.1 | https://registry.npmjs.org/@esbuild/openharmony-arm64/-/openharmony-arm64-0.28.1.tgz | unknown |
| @esbuild/sunos-x64 | 0.28.1 | https://registry.npmjs.org/@esbuild/sunos-x64/-/sunos-x64-0.28.1.tgz | unknown |
| @esbuild/win32-arm64 | 0.28.1 | https://registry.npmjs.org/@esbuild/win32-arm64/-/win32-arm64-0.28.1.tgz | unknown |
| @esbuild/win32-ia32 | 0.28.1 | https://registry.npmjs.org/@esbuild/win32-ia32/-/win32-ia32-0.28.1.tgz | unknown |
| @esbuild/win32-x64 | 0.28.1 | https://registry.npmjs.org/@esbuild/win32-x64/-/win32-x64-0.28.1.tgz | unknown |
| @rollup/rollup-android-arm-eabi | 4.62.2 | https://registry.npmjs.org/@rollup/rollup-android-arm-eabi/-/rollup-android-arm-eabi-4.62.2.tgz | unknown |
| @rollup/rollup-android-arm64 | 4.62.2 | https://registry.npmjs.org/@rollup/rollup-android-arm64/-/rollup-android-arm64-4.62.2.tgz | unknown |
| @rollup/rollup-darwin-x64 | 4.62.2 | https://registry.npmjs.org/@rollup/rollup-darwin-x64/-/rollup-darwin-x64-4.62.2.tgz | unknown |
| @rollup/rollup-freebsd-arm64 | 4.62.2 | https://registry.npmjs.org/@rollup/rollup-freebsd-arm64/-/rollup-freebsd-arm64-4.62.2.tgz | unknown |
| @rollup/rollup-freebsd-x64 | 4.62.2 | https://registry.npmjs.org/@rollup/rollup-freebsd-x64/-/rollup-freebsd-x64-4.62.2.tgz | unknown |
| @rollup/rollup-linux-arm-gnueabihf | 4.62.2 | https://registry.npmjs.org/@rollup/rollup-linux-arm-gnueabihf/-/rollup-linux-arm-gnueabihf-4.62.2.tgz | unknown |
| @rollup/rollup-linux-arm-musleabihf | 4.62.2 | https://registry.npmjs.org/@rollup/rollup-linux-arm-musleabihf/-/rollup-linux-arm-musleabihf-4.62.2.tgz | unknown |
| @rollup/rollup-linux-arm64-gnu | 4.62.2 | https://registry.npmjs.org/@rollup/rollup-linux-arm64-gnu/-/rollup-linux-arm64-gnu-4.62.2.tgz | unknown |
| @rollup/rollup-linux-arm64-musl | 4.62.2 | https://registry.npmjs.org/@rollup/rollup-linux-arm64-musl/-/rollup-linux-arm64-musl-4.62.2.tgz | unknown |
| @rollup/rollup-linux-loong64-gnu | 4.62.2 | https://registry.npmjs.org/@rollup/rollup-linux-loong64-gnu/-/rollup-linux-loong64-gnu-4.62.2.tgz | unknown |
| @rollup/rollup-linux-loong64-musl | 4.62.2 | https://registry.npmjs.org/@rollup/rollup-linux-loong64-musl/-/rollup-linux-loong64-musl-4.62.2.tgz | unknown |
| @rollup/rollup-linux-ppc64-gnu | 4.62.2 | https://registry.npmjs.org/@rollup/rollup-linux-ppc64-gnu/-/rollup-linux-ppc64-gnu-4.62.2.tgz | unknown |
| @rollup/rollup-linux-ppc64-musl | 4.62.2 | https://registry.npmjs.org/@rollup/rollup-linux-ppc64-musl/-/rollup-linux-ppc64-musl-4.62.2.tgz | unknown |
| @rollup/rollup-linux-riscv64-gnu | 4.62.2 | https://registry.npmjs.org/@rollup/rollup-linux-riscv64-gnu/-/rollup-linux-riscv64-gnu-4.62.2.tgz | unknown |
| @rollup/rollup-linux-riscv64-musl | 4.62.2 | https://registry.npmjs.org/@rollup/rollup-linux-riscv64-musl/-/rollup-linux-riscv64-musl-4.62.2.tgz | unknown |
| @rollup/rollup-linux-s390x-gnu | 4.62.2 | https://registry.npmjs.org/@rollup/rollup-linux-s390x-gnu/-/rollup-linux-s390x-gnu-4.62.2.tgz | unknown |
| @rollup/rollup-linux-x64-gnu | 4.62.2 | https://registry.npmjs.org/@rollup/rollup-linux-x64-gnu/-/rollup-linux-x64-gnu-4.62.2.tgz | unknown |
| @rollup/rollup-linux-x64-musl | 4.62.2 | https://registry.npmjs.org/@rollup/rollup-linux-x64-musl/-/rollup-linux-x64-musl-4.62.2.tgz | unknown |
| @rollup/rollup-openbsd-x64 | 4.62.2 | https://registry.npmjs.org/@rollup/rollup-openbsd-x64/-/rollup-openbsd-x64-4.62.2.tgz | unknown |
| @rollup/rollup-openharmony-arm64 | 4.62.2 | https://registry.npmjs.org/@rollup/rollup-openharmony-arm64/-/rollup-openharmony-arm64-4.62.2.tgz | unknown |
| @rollup/rollup-win32-arm64-msvc | 4.62.2 | https://registry.npmjs.org/@rollup/rollup-win32-arm64-msvc/-/rollup-win32-arm64-msvc-4.62.2.tgz | unknown |
| @rollup/rollup-win32-ia32-msvc | 4.62.2 | https://registry.npmjs.org/@rollup/rollup-win32-ia32-msvc/-/rollup-win32-ia32-msvc-4.62.2.tgz | unknown |
| @rollup/rollup-win32-x64-gnu | 4.62.2 | https://registry.npmjs.org/@rollup/rollup-win32-x64-gnu/-/rollup-win32-x64-gnu-4.62.2.tgz | unknown |
| @rollup/rollup-win32-x64-msvc | 4.62.2 | https://registry.npmjs.org/@rollup/rollup-win32-x64-msvc/-/rollup-win32-x64-msvc-4.62.2.tgz | unknown |
| @tauri-apps/cli-darwin-x64 | 2.11.1 | https://registry.npmjs.org/@tauri-apps/cli-darwin-x64/-/cli-darwin-x64-2.11.1.tgz | unknown |
| @tauri-apps/cli-linux-arm-gnueabihf | 2.11.1 | https://registry.npmjs.org/@tauri-apps/cli-linux-arm-gnueabihf/-/cli-linux-arm-gnueabihf-2.11.1.tgz | unknown |
| @tauri-apps/cli-linux-arm64-gnu | 2.11.1 | https://registry.npmjs.org/@tauri-apps/cli-linux-arm64-gnu/-/cli-linux-arm64-gnu-2.11.1.tgz | unknown |
| @tauri-apps/cli-linux-arm64-musl | 2.11.1 | https://registry.npmjs.org/@tauri-apps/cli-linux-arm64-musl/-/cli-linux-arm64-musl-2.11.1.tgz | unknown |
| @tauri-apps/cli-linux-riscv64-gnu | 2.11.1 | https://registry.npmjs.org/@tauri-apps/cli-linux-riscv64-gnu/-/cli-linux-riscv64-gnu-2.11.1.tgz | unknown |
| @tauri-apps/cli-linux-x64-gnu | 2.11.1 | https://registry.npmjs.org/@tauri-apps/cli-linux-x64-gnu/-/cli-linux-x64-gnu-2.11.1.tgz | unknown |
| @tauri-apps/cli-linux-x64-musl | 2.11.1 | https://registry.npmjs.org/@tauri-apps/cli-linux-x64-musl/-/cli-linux-x64-musl-2.11.1.tgz | unknown |
| @tauri-apps/cli-win32-arm64-msvc | 2.11.1 | https://registry.npmjs.org/@tauri-apps/cli-win32-arm64-msvc/-/cli-win32-arm64-msvc-2.11.1.tgz | unknown |
| @tauri-apps/cli-win32-ia32-msvc | 2.11.1 | https://registry.npmjs.org/@tauri-apps/cli-win32-ia32-msvc/-/cli-win32-ia32-msvc-2.11.1.tgz | unknown |
| @tauri-apps/cli-win32-x64-msvc | 2.11.1 | https://registry.npmjs.org/@tauri-apps/cli-win32-x64-msvc/-/cli-win32-x64-msvc-2.11.1.tgz | unknown |

## Supplied and consulted source identity

Mechanism: delegated-harness-native TASK descendant `/root/group_a_execution/dependency_inventory`, parent `/root/group_a_execution`; no further delegation. Assignment allowed one inventory output and offline cache inspection, and prohibited downloads, auth/live turns, app edits and Git operations. Root and TASK role remain the operative instruction basis. App v3 LOOP_INIT was accidentally consulted while locating v4; its distinct applicability was confirmed and it was not applied. No workflow or skill body selected for this bounded cache inspection.

| Source (repository-relative) | SHA-256 of observed bytes |
|---|---|
| `AGENTS.md` | `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977` |
| `agents/AGENT_TASK.md` | `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7` |
| `projects/chirality-app-v4/loop/LOOP_INIT.md` | `45c23cf477e23aff1d0152189caf7e8ebfb53eca42e3a1fae87a06af8c197f28` |
| `projects/chirality-app-v4/README.md` | `f1f90e46054a7e1c178736a4fa645ed9edb17538e94cd9329c2bf5e48a5136b8` |
| `projects/chirality-app-v4/app/README.md` | `a9a764698d351803cf8c8f93cdfdd0bc2e3de0c01e6a20e28525d6fc0e020c7f` |
| `projects/chirality-app-v4/app/EVIDENCE.md` | `ea5a8c5c3ecb2ee8d3632b03925a3cc0a75cc49bf9e70854124712b2decdd349` |
| `projects/chirality-app-v4/app/CONTRACT_ISSUES.md` | `b34507c62daec69fe2ca7152757757a31d6429d7786c797c7097e693f2675639` |
| `projects/chirality-app-v4/app/src-tauri/Cargo.toml` | `1d8d5836f49db0d385c150a9e94e9cd1492511009d6bcfebf9fbe2623d8063e8` |
| `projects/chirality-app-v4/app/src-tauri/Cargo.lock` | `7d585326a2c8bdd2e3183cfbfe29ad9de5ccacce2513eb95f4f8d9830d751e71` |
| `projects/chirality-app-v4/app/package.json` | `afd49df0c9ab9bb00bdacfc41a7f356f1347a36b82145e4974a6b5121f41c7e0` |
| `projects/chirality-app-v4/app/package-lock.json` | `1392f7926e008f71e103e91734b1a9e0e40477c68865ea482aa885954a3d25fa` |
| `projects/chirality-app-v4/execution/_Coordination/WorkGraphs/APP-V4-GROUP-A-20261004/WORK_GRAPH.md` | `921252cf288bcf4b49c0738f7276295fd46a2eda29d3c132d7f97c4e500dddea` |
| `projects/chirality-app-dev/loop/LOOP_INIT.md` | `8b975c10acf6c4394f5423d4def20aeb4583159c691e8d3d11a41ce7451e6a25` |

## Metadata amendment and access evidence

Parent authorized read-only crates.io/static.crates.io/registry.npmjs.org metadata/HEAD requests solely for package pins, dependency filenames, URLs and lengths; package archive/body downloads, installs and index mutation remain prohibited. Receipt confirmed to parent in coordination return.

- Official `https://crates.io/api/v1/crates/jsonschema` JSON request through default sandbox: DNS resolution unavailable (`Errno 8`).
- Same JSON request with approved `require_escalated`: Python TLS certificate verification failed because its local issuer store was unavailable. No TLS verification bypass attempted.
- System `curl --fail --silent --show-error --max-time 20` with approved escalation, same official JSON endpoint: HTTP 403. Certificate verification remained enabled.
- Web `open` of the same official endpoint: endpoint inaccessible. No successful registry response, exact version, size or dependency list was received.
- `cargo metadata --offline --locked --no-deps --format-version 1` in `app/src-tauri`: exit 0, seven declared dependencies and local targets reported, `resolve:null`. This command confirms manifest parsing; it does not resolve the transitive native graph or demonstrate a build. T0 owns actual builds.

The outstanding metadata issue is an actual access limitation, not a pending permission request. Parent can try another authorized official metadata transport or ask the owner to provide official version metadata. This initial access result was partly resolved by the subsequent official-source/HEAD route below. The complete incremental transitive total remains unknown and no complete download proposal can yet be made.

## Authorized official-source repair: confirmed candidate and archive sizes

A further parent brief amendment authorized official GitHub manifest/readme source-text reads and static.crates.io HEAD requests. No archive body, source package, index mutation, install or application edit occurred. System curl with normal TLS verification retrieved the tagged text successfully; web read of the tagged GitHub file views returned cache misses, but official release metadata was accessible. Release page identifies `rust-v0.58.5`, commit `21a061d`, published 2 October 2026.

Candidate: `jsonschema = { version = "=0.58.5", default-features = false }`.
This is a proposed compatible dependency declaration, not a compile-tested or adopted pin. Official tag workspace declares edition 2021 and MSRV 1.85.0, compatible with observed host Rust 1.92.0. The tagged README advertises draft 2020-12. Do not inherit master changes when implementing.

Default features are `resolve-http`, `resolve-file`, `tls-aws-lc-rs`, `idna`. Disabling defaults removes the validator's optional reqwest/rustls retrieval route and its default aws-lc TLS provider, and removes automatic file resolution. Do not enable `resolve-async`, `tls-ring`, `macros`, or foreign-language bindings for W-1 without a concrete need. Missing `idna` means IDN format support needs examination if the accepted schemas require it; ordinary draft/keyword validation is separate. The implementation still needs a local schema resource registry or explicit refusing retriever, and a negative unresolved-ref test; feature selection alone does not prove correct handling.

The mandatory companion requirements are caret `0.58.5`; for the size inventory below all four are deliberately proposed at exact 0.58.5. Parent must preserve that selection in the resolver lock or explicit constraints if newer compatible companions exist.

| Exact artifact | Official source | HEAD compressed bytes |
|---|---|---|
| jsonschema-0.58.5.crate | https://static.crates.io/crates/jsonschema/jsonschema-0.58.5.crate | 1,069,243 |
| jsonschema-regex-0.58.5.crate | https://static.crates.io/crates/jsonschema-regex/jsonschema-regex-0.58.5.crate | 14,904 |
| jsonschema-value-0.58.5.crate | https://static.crates.io/crates/jsonschema-value/jsonschema-value-0.58.5.crate | 92,056 |
| referencing-0.58.5.crate | https://static.crates.io/crates/referencing/referencing-0.58.5.crate | 59,533 |
| Subtotal (four files only) | Not a full dependency total | 1,235,736 |

Every HEAD returned HTTP/2 200; Content-Type application/gzip; 2 October 2026 Last-Modified dates. The direct archive response has `etag: fb350d59fba621fa3813340b671c8904`; companion ETags are `f42b36d03b9303e04c10f00c29c3f673`, `cf7a32450b1bf62d272cc552acb7e9e7`, `ed5ae391af44cf9fa8c7c00cc3f6062d` in table order. These response ETags are not registry checksum verification.

### Additional transitive implications

Source manifests establish these mandatory dependency families absent from the inspected archive cache: bytecount (^0.6), data-encoding (^2.9), email_address (^0.2.9), fancy-regex (^0.19), fraction (^0.17, default features disabled, with-bigint enabled), num-cmp (^0.1), strum (^0.28.0, derive enabled), unicode-general-category (^1.1), uuid-simd (^0.8, defaults disabled, std+detect), fluent-uri (^0.4.1, serde enabled), micromap (^0.3.0). These ranges are **not exact selected versions**; their archive sizes are unknown, and their own transitives remain unenumerated. Fraction's bigint path and strum's derive path add further closure work. The later refined resolver establishes exact incremental package versions and compressed bytes below; unpacked/build disk totals remain unknown.

Compatible cached candidates (not resolver selections): ahash0.8.12; itoa1.0.18; num-traits0.2.19; percent-encoding2.3.2; regex1.12.3; regex-syntax0.8.10; serde1.0.229; serde_json1.0.151; zmij1.0.23; parking_lot0.12.5; hashbrown0.17.1. Feature unification may affect existing application crates: serde_json receives float_roundtrip, ahash receives serde, and native referring components use additional regex/hashbrown features. The later refined scratch resolver lock establishes reusable cached archives and exact missing versions below. The upstream workspace lock, if consulted, would not alone establish this application's chosen target/feature closure.

Official source-text reads (all at the confirmed release tag; normal TLS; no archive bodies):

- https://raw.githubusercontent.com/Stranger6667/jsonschema/rust-v0.58.5/Cargo.toml
- https://raw.githubusercontent.com/Stranger6667/jsonschema/rust-v0.58.5/crates/jsonschema/Cargo.toml
- https://raw.githubusercontent.com/Stranger6667/jsonschema/rust-v0.58.5/README.md
- https://raw.githubusercontent.com/Stranger6667/jsonschema/rust-v0.58.5/crates/jsonschema-regex/Cargo.toml
- https://raw.githubusercontent.com/Stranger6667/jsonschema/rust-v0.58.5/crates/jsonschema-value/Cargo.toml
- https://raw.githubusercontent.com/Stranger6667/jsonschema/rust-v0.58.5/crates/jsonschema-referencing/Cargo.toml
- Release identity: https://github.com/Stranger6667/jsonschema/releases/tag/rust-v0.58.5

Decision interface: parent can now name four exact candidate files/sources/sizes. A yes limited to those four files would not authorize the remaining unknown transitive archives. Prefer completing the official registry resolution metadata inventory first; if the owner chooses staged authorization, keep each subsequent absent artifact explicit and never treat the four-file subtotal as a budget cap or all-inclusive approval.

## Isolated metadata resolver result (upper bound, not final app closure)

Parent explicitly authorized isolated scratch Cargo metadata resolution. `cargo generate-lockfile` succeeded for exact jsonschema0.58.5 defaults-off in `/private/tmp/chirality-schema-metadata-t6r_txcy`, with CARGO_HOME under that same scratch root. Only registry index metadata was received; no `cargo fetch`, online build or source archive retrieval occurred. The scratch lock selects 79 registry packages; 30 exact archives are already cached, 49 are absent. Its fresh resolution upgrades some otherwise reusable application versions and includes foreign target dependencies, so this is a bounded exact **upper-bound proposal**, not the final native application download set. A current-app-lock-preserving resolution remains preferable.

| Missing selected archive | Source | HEAD bytes |
|---|---|---|
| aho-corasick-1.1.5.crate | https://static.crates.io/crates/aho-corasick/aho-corasick-1.1.5.crate | 184315 |
| allocator-api2-0.2.21.crate | https://static.crates.io/crates/allocator-api2/allocator-api2-0.2.21.crate | 63622 |
| autocfg-1.5.1.crate | https://static.crates.io/crates/autocfg/autocfg-1.5.1.crate | 18911 |
| bitflags-2.13.2.crate | https://static.crates.io/crates/bitflags/bitflags-2.13.2.crate | 51678 |
| borrow-or-share-0.2.4.crate | https://static.crates.io/crates/borrow-or-share/borrow-or-share-0.2.4.crate | 5243 |
| bytecount-0.6.9.crate | https://static.crates.io/crates/bytecount/bytecount-0.6.9.crate | 18695 |
| data-encoding-2.11.1.crate | https://static.crates.io/crates/data-encoding/data-encoding-2.11.1.crate | 22651 |
| email_address-0.2.9.crate | https://static.crates.io/crates/email_address/email_address-0.2.9.crate | 21579 |
| fancy-regex-0.19.2.crate | https://static.crates.io/crates/fancy-regex/fancy-regex-0.19.2.crate | 235529 |
| fluent-uri-0.4.1.crate | https://static.crates.io/crates/fluent-uri/fluent-uri-0.4.1.crate | 51205 |
| fraction-0.17.0.crate | https://static.crates.io/crates/fraction/fraction-0.17.0.crate | 118037 |
| js-sys-0.3.106.crate | https://static.crates.io/crates/js-sys/js-sys-0.3.106.crate | 113772 |
| jsonschema-0.58.5.crate | https://static.crates.io/crates/jsonschema/jsonschema-0.58.5.crate | 1069243 |
| jsonschema-regex-0.58.5.crate | https://static.crates.io/crates/jsonschema-regex/jsonschema-regex-0.58.5.crate | 14904 |
| jsonschema-value-0.58.5.crate | https://static.crates.io/crates/jsonschema-value/jsonschema-value-0.58.5.crate | 92056 |
| libc-0.2.190.crate | https://static.crates.io/crates/libc/libc-0.2.190.crate | 853678 |
| micromap-0.3.0.crate | https://static.crates.io/crates/micromap/micromap-0.3.0.crate | 59760 |
| num-0.4.3.crate | https://static.crates.io/crates/num/num-0.4.3.crate | 9575 |
| num-bigint-0.4.8.crate | https://static.crates.io/crates/num-bigint/num-bigint-0.4.8.crate | 109961 |
| num-cmp-0.1.0.crate | https://static.crates.io/crates/num-cmp/num-cmp-0.1.0.crate | 15375 |
| num-complex-0.4.6.crate | https://static.crates.io/crates/num-complex/num-complex-0.4.6.crate | 30352 |
| num-integer-0.1.47.crate | https://static.crates.io/crates/num-integer/num-integer-0.1.47.crate | 23502 |
| num-iter-0.1.46.crate | https://static.crates.io/crates/num-iter/num-iter-0.1.46.crate | 10763 |
| num-rational-0.4.2.crate | https://static.crates.io/crates/num-rational/num-rational-0.4.2.crate | 28159 |
| outref-0.5.2.crate | https://static.crates.io/crates/outref/outref-0.5.2.crate | 5621 |
| r-efi-5.3.0.crate | https://static.crates.io/crates/r-efi/r-efi-5.3.0.crate | 64532 |
| redox_syscall-0.5.18.crate | https://static.crates.io/crates/redox_syscall/redox_syscall-0.5.18.crate | 30747 |
| ref-cast-1.0.27.crate | https://static.crates.io/crates/ref-cast/ref-cast-1.0.27.crate | 15335 |
| ref-cast-impl-1.0.27.crate | https://static.crates.io/crates/ref-cast-impl/ref-cast-impl-1.0.27.crate | 10194 |
| referencing-0.58.5.crate | https://static.crates.io/crates/referencing/referencing-0.58.5.crate | 59533 |
| regex-1.13.1.crate | https://static.crates.io/crates/regex/regex-1.13.1.crate | 157118 |
| regex-automata-0.4.18.crate | https://static.crates.io/crates/regex-automata/regex-automata-0.4.18.crate | 628707 |
| regex-syntax-0.8.11.crate | https://static.crates.io/crates/regex-syntax/regex-syntax-0.8.11.crate | 359055 |
| rustversion-1.0.23.crate | https://static.crates.io/crates/rustversion/rustversion-1.0.23.crate | 21013 |
| smallvec-1.16.2.crate | https://static.crates.io/crates/smallvec/smallvec-1.16.2.crate | 34874 |
| strum-0.28.0.crate | https://static.crates.io/crates/strum/strum-0.28.0.crate | 8550 |
| strum_macros-0.28.0.crate | https://static.crates.io/crates/strum_macros/strum_macros-0.28.0.crate | 30964 |
| unicode-general-category-1.1.0.crate | https://static.crates.io/crates/unicode-general-category/unicode-general-category-1.1.0.crate | 36486 |
| uuid-simd-0.8.0.crate | https://static.crates.io/crates/uuid-simd/uuid-simd-0.8.0.crate | 6959 |
| vsimd-0.8.0.crate | https://static.crates.io/crates/vsimd/vsimd-0.8.0.crate | 21377 |
| wasip2-1.0.4+wasi-0.2.12.crate | https://static.crates.io/crates/wasip2/wasip2-1.0.4+wasi-0.2.12.crate | 135311 |
| wasm-bindgen-0.2.129.crate | https://static.crates.io/crates/wasm-bindgen/wasm-bindgen-0.2.129.crate | 70859 |
| wasm-bindgen-macro-0.2.129.crate | https://static.crates.io/crates/wasm-bindgen-macro/wasm-bindgen-macro-0.2.129.crate | 9612 |
| wasm-bindgen-macro-support-0.2.129.crate | https://static.crates.io/crates/wasm-bindgen-macro-support/wasm-bindgen-macro-support-0.2.129.crate | 120366 |
| wasm-bindgen-shared-0.2.129.crate | https://static.crates.io/crates/wasm-bindgen-shared/wasm-bindgen-shared-0.2.129.crate | 13023 |
| windows-link-0.2.1.crate | https://static.crates.io/crates/windows-link/windows-link-0.2.1.crate | 6133 |
| wit-bindgen-0.57.1.crate | https://static.crates.io/crates/wit-bindgen/wit-bindgen-0.57.1.crate | 71227 |
| zerocopy-0.8.59.crate | https://static.crates.io/crates/zerocopy/zerocopy-0.8.59.crate | 287462 |
| zerocopy-derive-0.8.59.crate | https://static.crates.io/crates/zerocopy-derive/zerocopy-derive-0.8.59.crate | 137212 |

Whole prospective lock absent-archive HEAD total: **5,564,835 bytes**; unknown lengths: 0. This includes foreign targets and avoidable updates, and excludes metadata traffic/unpacked/build disk needs. Native minimum remains unresolved. Registry checksums are in the prospective lock, preserved at the scratch path; response lengths do not verify downloaded bytes.

### Frozen 49-archive upper-bound checksum addendum

| Package | Version | Registry SHA-256 |
|---|---|---|
| aho-corasick | 1.1.5 | c982642fa9e8606056828ee9a8505737230110bb1099153c79efe865c59d12ba |
| allocator-api2 | 0.2.21 | 683d7910e743518b0e34f1186f92494becacb047c7b6bf616c96772180fef923 |
| autocfg | 1.5.1 | f2032f911046de80f0a198e0901378627c33f59ea0ac00e363d481118bd70a53 |
| bitflags | 2.13.2 | 3ded4057c258ba199e2d26386d3af3780957ecaee6c4ef4041c6b4b8b97c0b06 |
| borrow-or-share | 0.2.4 | dc0b364ead1874514c8c2855ab558056ebfeb775653e7ae45ff72f28f8f3166c |
| bytecount | 0.6.9 | 175812e0be2bccb6abe50bb8d566126198344f707e304f45c648fd8f2cc0365e |
| data-encoding | 2.11.1 | 4583a4551df46e2792f82ceeac45e850d2e2d5debba0b91f102385cda5b11f06 |
| email_address | 0.2.9 | e079f19b08ca6239f47f8ba8509c11cf3ea30095831f7fed61441475edd8c449 |
| fancy-regex | 0.19.2 | d301f5bf187b3c295fce6468d3875037a0bccc5f6b151c63cac2f85babf21912 |
| fluent-uri | 0.4.1 | bc74ac4d8359ae70623506d512209619e5cf8f347124910440dbc221714b328e |
| fraction | 0.17.0 | e246562084dde8ebbcc943b261c406ce4f68e5032ec28029a251a47d6a295500 |
| js-sys | 0.3.106 | 7883d941dae510fb2d978fc3fe018c71c9e2892fd38854de3e8b92c2e5ad9cc5 |
| jsonschema | 0.58.5 | ea18b8d5e1469b1bdd6b349169305141316a7c26da27f239773b65c830c0f5d6 |
| jsonschema-regex | 0.58.5 | 854e9e22c420535035e95eed240cbfb4a5f4b7da74d122d63144e0c31926dbfd |
| jsonschema-value | 0.58.5 | 4e3bfac11ac357ec620880025757d38c67da8fd5b9ef5024d19f0f360002b4ca |
| libc | 0.2.190 | ce5d3ddc6d3fa000eb1536d85e147bfe31aacaba692ed6a876f95cb7c855be78 |
| micromap | 0.3.0 | c2a86d3146ed3995b5913c414f6664344b9617457320782e64f0bb44afd49d74 |
| num | 0.4.3 | 35bd024e8b2ff75562e5f34e7f4905839deb4b22955ef5e73d2fea1b9813cb23 |
| num-bigint | 0.4.8 | c89e69e7e0f03bea5ef08013795c25018e101932225a656383bd384495ecc367 |
| num-cmp | 0.1.0 | 63335b2e2c34fae2fb0aa2cecfd9f0832a1e24b3b32ecec612c3426d46dc8aaa |
| num-complex | 0.4.6 | 73f88a1307638156682bada9d7604135552957b7818057dcef22705b4d509495 |
| num-integer | 0.1.47 | 7ce2d95d4b3734dc35aa2f45e1aa22cd416814592a4f9d9205e11affd5b8e10b |
| num-iter | 0.1.46 | c92800bd69a1eac91786bcfe9da64a897eb72911b8dc3095decbd07429e8048b |
| num-rational | 0.4.2 | f83d14da390562dca69fc84082e73e548e1ad308d24accdedd2720017cb37824 |
| outref | 0.5.2 | 1a80800c0488c3a21695ea981a54918fbb37abf04f4d0720c453632255e2ff0e |
| r-efi | 5.3.0 | 69cdb34c158ceb288df11e18b4bd39de994f6657d83847bdffdbd7f346754b0f |
| redox_syscall | 0.5.18 | ed2bf2547551a7053d6fdfafda3f938979645c44812fbfcda098faae3f1a362d |
| ref-cast | 1.0.27 | 7e440fb4e4b4147295338efb76001ab9e4efc0e5839df2c47fc5ac2381d365c3 |
| ref-cast-impl | 1.0.27 | 92ecd8964f8453721699a1ed72037b0db49ce2f5a5138486ee89bed6f67cdf3a |
| referencing | 0.58.5 | 590efadb0a669f1712c1e3ab810a55d4c3d20d0127c455f7236dd0710aba0346 |
| regex | 1.13.1 | f020237b6c8eed93db2e2cb53c00c60a8e1bc73da7d073199a1180401450218d |
| regex-automata | 0.4.18 | ad8553b9b26413251cbf30e620595c7a41b3887f03da04579c0e6b0d6a06b4b2 |
| regex-syntax | 0.8.11 | d6f6ff9a378485b298a5286656da665ba74413d36db0979633275d2e708145d4 |
| rustversion | 1.0.23 | cf54715a573b99ac80df0bc206da022bcd442c974952c7b9720069370852e21f |
| smallvec | 1.16.2 | f9395f0f0eee849a9b707b2f06bb92a6a422090e2123bb2ef8e87a0e61892a8e |
| strum | 0.28.0 | 9628de9b8791db39ceda2b119bbe13134770b56c138ec1d3af810d045c04f9bd |
| strum_macros | 0.28.0 | ab85eea0270ee17587ed4156089e10b9e6880ee688791d45a905f5b1ca36f664 |
| unicode-general-category | 1.1.0 | 0b993bddc193ae5bd0d623b49ec06ac3e9312875fdae725a975c51db1cc1677f |
| uuid-simd | 0.8.0 | 23b082222b4f6619906941c17eb2297fff4c2fb96cb60164170522942a200bd8 |
| vsimd | 0.8.0 | 5c3082ca00d5a5ef149bb8b555a72ae84c9c59f7250f013ac822ac2e49b19c64 |
| wasip2 | 1.0.4+wasi-0.2.12 | b67efb37e106e55ce722a510d6b5f9c17f083e5fc79afc2badeb12cc313d9487 |
| wasm-bindgen | 0.2.129 | 9bb54f33acc68fd454578d9820b0bde1a1a3d17aa17bb7b6595806d02886d409 |
| wasm-bindgen-macro | 0.2.129 | 2e29d0c35b16e224a7eeb5cd2d25e3e1968fbd65604117b44d3b789d00ee8535 |
| wasm-bindgen-macro-support | 0.2.129 | 6f501a8bc3719dba86ef8ae4728879c08001bea749eb1333ac5b91e040e2a6b7 |
| wasm-bindgen-shared | 0.2.129 | 23f0c9c52aa7cd7d77769a4cfe2a9adb1b331f489a41d912ce14513d5ab995c6 |
| windows-link | 0.2.1 | f0805222e57f7521d6a62e36fa9163bc891acd422f971defe97d64e70d0a4fe5 |
| wit-bindgen | 0.57.1 | 1ebf944e87a7c253233ad6766e082e3cd714b5d03812acc24c318f549614536e |
| zerocopy | 0.8.59 | 6df92bf3d9227be3d53173901ddbffac2babc27ae50f397776ffd6dc33f800cb |
| zerocopy-derive | 0.8.59 | ac4f328cf2f05d084e496c3e9c3f33ed0a183656a16e1fcec4d464d8373aec82 |

## Refined existing-app-lock proposal (supersedes avoidable fresh-lock updates)

After copying 357 missing **existing local registry metadata records only** into the isolated scratch index (no archive/source copies), resetting the scratch application lock from the tracked lock and running `cargo update --workspace --offline`, resolution preserved existing application versions except regex-automata0.4.14→0.4.18. It added 29 packages plus that one updated package: ahash0.8.12 already cached, leaving29 absent incremental archives. The earlier tauri-utils/Tauri family update was caused by incomplete scratch metadata, not a demonstrated validator compatibility need; it is not present in this refined lock. No app or real Cargo cache was changed.

**Preferred incremental proposal: 29 exact absent archives; 3,223,082 compressed bytes.** Native baseline cache sufficiency remains with T0. These are all new selected packages; they are not the192 pre-existing foreign-platform archive misses. Download approval can be limited to this precise29-artifact set, while the49-artifact table above remains a separately frozen, broader proposal if the owner deliberately prefers it. Do not conflate the two totals.

| Exact missing artifact | Source | HEAD bytes | Registry SHA-256 |
|---|---|---|---|
| allocator-api2-0.2.21.crate | https://static.crates.io/crates/allocator-api2/allocator-api2-0.2.21.crate | 63622 | 683d7910e743518b0e34f1186f92494becacb047c7b6bf616c96772180fef923 |
| borrow-or-share-0.2.4.crate | https://static.crates.io/crates/borrow-or-share/borrow-or-share-0.2.4.crate | 5243 | dc0b364ead1874514c8c2855ab558056ebfeb775653e7ae45ff72f28f8f3166c |
| bytecount-0.6.9.crate | https://static.crates.io/crates/bytecount/bytecount-0.6.9.crate | 18695 | 175812e0be2bccb6abe50bb8d566126198344f707e304f45c648fd8f2cc0365e |
| data-encoding-2.11.1.crate | https://static.crates.io/crates/data-encoding/data-encoding-2.11.1.crate | 22651 | 4583a4551df46e2792f82ceeac45e850d2e2d5debba0b91f102385cda5b11f06 |
| email_address-0.2.9.crate | https://static.crates.io/crates/email_address/email_address-0.2.9.crate | 21579 | e079f19b08ca6239f47f8ba8509c11cf3ea30095831f7fed61441475edd8c449 |
| fancy-regex-0.19.2.crate | https://static.crates.io/crates/fancy-regex/fancy-regex-0.19.2.crate | 235529 | d301f5bf187b3c295fce6468d3875037a0bccc5f6b151c63cac2f85babf21912 |
| fluent-uri-0.4.1.crate | https://static.crates.io/crates/fluent-uri/fluent-uri-0.4.1.crate | 51205 | bc74ac4d8359ae70623506d512209619e5cf8f347124910440dbc221714b328e |
| fraction-0.17.0.crate | https://static.crates.io/crates/fraction/fraction-0.17.0.crate | 118037 | e246562084dde8ebbcc943b261c406ce4f68e5032ec28029a251a47d6a295500 |
| jsonschema-0.58.5.crate | https://static.crates.io/crates/jsonschema/jsonschema-0.58.5.crate | 1069243 | ea18b8d5e1469b1bdd6b349169305141316a7c26da27f239773b65c830c0f5d6 |
| jsonschema-regex-0.58.5.crate | https://static.crates.io/crates/jsonschema-regex/jsonschema-regex-0.58.5.crate | 14904 | 854e9e22c420535035e95eed240cbfb4a5f4b7da74d122d63144e0c31926dbfd |
| jsonschema-value-0.58.5.crate | https://static.crates.io/crates/jsonschema-value/jsonschema-value-0.58.5.crate | 92056 | 4e3bfac11ac357ec620880025757d38c67da8fd5b9ef5024d19f0f360002b4ca |
| micromap-0.3.0.crate | https://static.crates.io/crates/micromap/micromap-0.3.0.crate | 59760 | c2a86d3146ed3995b5913c414f6664344b9617457320782e64f0bb44afd49d74 |
| num-0.4.3.crate | https://static.crates.io/crates/num/num-0.4.3.crate | 9575 | 35bd024e8b2ff75562e5f34e7f4905839deb4b22955ef5e73d2fea1b9813cb23 |
| num-bigint-0.4.8.crate | https://static.crates.io/crates/num-bigint/num-bigint-0.4.8.crate | 109961 | c89e69e7e0f03bea5ef08013795c25018e101932225a656383bd384495ecc367 |
| num-cmp-0.1.0.crate | https://static.crates.io/crates/num-cmp/num-cmp-0.1.0.crate | 15375 | 63335b2e2c34fae2fb0aa2cecfd9f0832a1e24b3b32ecec612c3426d46dc8aaa |
| num-complex-0.4.6.crate | https://static.crates.io/crates/num-complex/num-complex-0.4.6.crate | 30352 | 73f88a1307638156682bada9d7604135552957b7818057dcef22705b4d509495 |
| num-integer-0.1.47.crate | https://static.crates.io/crates/num-integer/num-integer-0.1.47.crate | 23502 | 7ce2d95d4b3734dc35aa2f45e1aa22cd416814592a4f9d9205e11affd5b8e10b |
| num-iter-0.1.46.crate | https://static.crates.io/crates/num-iter/num-iter-0.1.46.crate | 10763 | c92800bd69a1eac91786bcfe9da64a897eb72911b8dc3095decbd07429e8048b |
| num-rational-0.4.2.crate | https://static.crates.io/crates/num-rational/num-rational-0.4.2.crate | 28159 | f83d14da390562dca69fc84082e73e548e1ad308d24accdedd2720017cb37824 |
| outref-0.5.2.crate | https://static.crates.io/crates/outref/outref-0.5.2.crate | 5621 | 1a80800c0488c3a21695ea981a54918fbb37abf04f4d0720c453632255e2ff0e |
| referencing-0.58.5.crate | https://static.crates.io/crates/referencing/referencing-0.58.5.crate | 59533 | 590efadb0a669f1712c1e3ab810a55d4c3d20d0127c455f7236dd0710aba0346 |
| regex-automata-0.4.18.crate | https://static.crates.io/crates/regex-automata/regex-automata-0.4.18.crate | 628707 | ad8553b9b26413251cbf30e620595c7a41b3887f03da04579c0e6b0d6a06b4b2 |
| strum-0.28.0.crate | https://static.crates.io/crates/strum/strum-0.28.0.crate | 8550 | 9628de9b8791db39ceda2b119bbe13134770b56c138ec1d3af810d045c04f9bd |
| strum_macros-0.28.0.crate | https://static.crates.io/crates/strum_macros/strum_macros-0.28.0.crate | 30964 | ab85eea0270ee17587ed4156089e10b9e6880ee688791d45a905f5b1ca36f664 |
| unicode-general-category-1.1.0.crate | https://static.crates.io/crates/unicode-general-category/unicode-general-category-1.1.0.crate | 36486 | 0b993bddc193ae5bd0d623b49ec06ac3e9312875fdae725a975c51db1cc1677f |
| uuid-simd-0.8.0.crate | https://static.crates.io/crates/uuid-simd/uuid-simd-0.8.0.crate | 6959 | 23b082222b4f6619906941c17eb2297fff4c2fb96cb60164170522942a200bd8 |
| vsimd-0.8.0.crate | https://static.crates.io/crates/vsimd/vsimd-0.8.0.crate | 21377 | 5c3082ca00d5a5ef149bb8b555a72ae84c9c59f7250f013ac822ac2e49b19c64 |
| zerocopy-0.8.59.crate | https://static.crates.io/crates/zerocopy/zerocopy-0.8.59.crate | 287462 | 6df92bf3d9227be3d53173901ddbffac2babc27ae50f397776ffd6dc33f800cb |
| zerocopy-derive-0.8.59.crate | https://static.crates.io/crates/zerocopy-derive/zerocopy-derive-0.8.59.crate | 137212 | ac4f328cf2f05d084e496c3e9c3f33ed0a183656a16e1fcec4d464d8373aec82 |

Minimal prospective lock SHA-256: `9dd1eef00caf87ecd0240e4c843b2d3ce6acf40f8affd9754b694408a78c11c5` at `/private/tmp/chirality-schema-metadata-t6r_txcy/Cargo.lock`.
Refined application prospective lock SHA-256: `4318a283dcc25c594e6b99c2e7110495abc8cd89c45de9453cf0aaa5befa8549` at `/private/tmp/chirality-schema-metadata-t6r_txcy/app-probe/Cargo.lock`.
Observed tracked application lock SHA-256: `7d585326a2c8bdd2e3183cfbfe29ad9de5ccacce2513eb95f4f8d9830d751e71`; untouched by this child.

Check registry SHA-256 after owner-approved artifact retrieval, before cache admission or build. Checksums derive from selected registry metadata; no package byte hash was verified here. Proposed exact locks are metadata-only evidence; compilation/API correctness and W-1 refusal tests remain future work.
