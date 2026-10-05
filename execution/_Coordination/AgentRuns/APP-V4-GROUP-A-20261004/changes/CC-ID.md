# CC-ID — App record-entry identity minting

TASK `/root/group_a_execution/design_records_exec`, parent WORKING_ITEMS `/root/group_a_execution`, no delegation. Group A ordinary technical design authorized by parent; source owners are RS with C(TBD-003)/WD. Named change applied only to RS Design prose and this record; independent review required before product minting adoption. No schema, App/Cargo, prior CC-P-R, or other governed record changed.

RS §13.2 requires opaque `rec:…` minted by the writer unique across its logs. Current skeleton `rec:app:coord:<seq>` is tied to each log counter and can collide after approved multi-log allocation. Select secure UUIDv4 `rec:app:<canonical lowercase hyphenated uuid>` for new App record entries. Draw 16 secure OS bytes, then set version/variant: 128 total bits, 122 random bits. Uniqueness means one designated record across all App projects/libraries/writers/logs; random minting gives probabilistic collision resistance, not guaranteed uniqueness. Entropy failure refuses mint/append visibly; detected collision/disagreement refuses conflict without overwrite. Retain minted ID on late-write retry. Reader preserves all existing fixture/legacy/host IDs as opaque and never parses or remints them.

C §5.3/§U-C1 and WD §6.1/§U-03 describe content/revision identities and method-designation comparison; no source read makes these consumers parse RS `recordId`. RS L-2 compares content methods, not record-token encoding. This selects no content hash, revision framing/canonicalization, host identity method, capture/run-ID method or carriage-manifest representation; U-04 is not closed wholesale. Schema accepts existing opaque forms without narrowing. Original CC-P-R remains frozen historical evidence; its returned RS source version is superseded only by this named record-ID clarification.

**Cached feasibility (read-only, no download/build):** Cargo.lock already includes uuid 1.23.1 and getrandom 0.4.2. Their local source exists. uuid's `v4` feature enables `rng`, but `Uuid::new_v4()` returns a UUID without a Result; to meet fail-closed reporting prefer explicit `getrandom::fill(&mut [u8; 16]) -> Result`, then `uuid::Builder::from_random_bytes(bytes).into_uuid()`. Builder sets version/variant and preserves secure input; this avoids an opaque panic-only RNG failure path. Exact direct manifest admission and offline compile remain implementation owner's work; no new archive is evidenced necessary, and none is acquired here.

**Alternative considered:** a durable writer-unique random namespace plus monotonic counter can work, but requires atomically persisted allocation, restart/clone protection and cross-log reservation. Current seq is per-log and cannot supply it. UUIDv4 avoids creating that shared durable counter contract. A content hash would wrongly couple record identity to content/canonicalization and is excluded.

**Adoption checks/consumers:** App writer and any generated capture record-ID binding; AAC recovery/dedup by record/capture identity; multi-log reader/standing joins. Test injected entropy failure writes nothing; two logs with same seq get different record IDs; pending retry preserves its ID; explicit collision refuses; legacy opaque references resolve unchanged. Schema checks alone cannot prove uniqueness or failure behavior. No consumer code changed.

## Exact source hashes

Prior CC-P-R returned RS source `1e9866dc9141597e44013d664183fbffac9504e43d4cdf37d5c5229a5d883048`; new RS source below.

| Source | SHA-256 |
|---|---|
| `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/RECORD_SEMANTICS.md` | `97f5b90e68e160370eefb801ccc3a0e81c4f86c7ff0d1eadfe67bbf78d1b7e0f` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/Design/CATALOG_AND_READ_BASIS.md` | `0e3ba39cd926a2063fc93621c17ed39d1fc8622b2256f08005d1286e99795294` |
| `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-01_Portable workflow contract and shared allocation/Design/WORKFLOW_DECLARATION.md` | `262c9e5417cf67b56cf7c3678128ad406e8b4e2fda7057a07bebf04254ab2f31` |
| `projects/chirality-app-v4/app/src-tauri/src/records.rs` | `3e4299bbe617e258ef1a2c7cf78fc5a8ab5319d462676e99273ec27dbb63f35a` |
| `projects/chirality-app-v4/app/src-tauri/Cargo.lock` | `4318a283dcc25c594e6b99c2e7110495abc8cd89c45de9453cf0aaa5befa8549` |
| `/Users/ryan/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/uuid-1.23.1/Cargo.toml` | `0a69d6a24add8b53e2216bbb919501510595d64cf3eb03e542791c8056a897e5` |
| `/Users/ryan/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/uuid-1.23.1/src/builder.rs` | `d332dbf9380bd6275f8c416758a8971db875ce2a661440c8e476cc6f827736c9` |
| `/Users/ryan/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/uuid-1.23.1/src/v4.rs` | `083012653ceff1b1306998176b333863b515ebb46a22aa5c17c172462eb9bd4c` |
| `/Users/ryan/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/getrandom-0.4.2/src/lib.rs` | `68bd1f2daa0aec1b55da25c07744869728a8be25d7c7d127bc788cd50fd8687b` |

## V0-P P1 disposition

Reviewer V0-P returned storage/native READY with minor P1: current OF-9 still said paths not selected. Repaired OF-9 to name selected bounded App §13.7 allocation while preserving unselected host persistence/placement and other shared choices. No schema/code change; source consistency checked against §13.7 and U-05/U-16. Original CC-ID candidate record SHA-256 `053d762e765866f08006c9a444f218a747155340599f2cc6ddd2b7419f97b25e` remains associated with its initial return; this append and refreshed RS hash identify the P1 repaired candidate for reviewer backcheck.
