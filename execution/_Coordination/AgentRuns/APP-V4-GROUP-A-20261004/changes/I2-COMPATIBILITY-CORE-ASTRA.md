# Private I2 compatibility core preparation

2026-10-05. Fresh Astra/low native TASK `/root/group_a_execution_astra/workflow_record_lifecycle_fit`; parent `/root/group_a_execution_astra`. Existing Root/TASK/Loop and accepted EXEC/WR/ROLE basis retained. Skill read/applied: `.agents/skills/chirality-change/SKILL.md`; no Git operations authorized or performed. No maintained source/Design/schema/lib/runtime/App changes; no Cargo, tests, native/supplier/network/auth/download/delegation. Private parser/formatter only: rustfmt --edition 2021 on the two private modules, exit 0 (also parsed/formatted dedicated test module).

Private copy: `/private/tmp/chirality-i2-compat-core-zc_6up7q/app`. BASE_MANIFEST.json at its parent records copied App sources (excluding build/dependency output). CANDIDATE.json pins the only three contribution files. ORIGINAL_NEGATIVE_HELPER.rs preserves the original helper plus focused negative control. No wholesale-copy integration is allowed: unrelated current REC/other owners' files in the copy are basis only. Integrate only named patch files after current preimage verification and independent review.

## Concrete private API

`execution_compatibility::report::PreparedReport::prepare(&Selection, Basis, Occasion, evaluated_at, &Observations, RoleInForce)` reads the closed selection's exact snapshot declaration. Basis binds home/full generation/conversation, acting pin/surface and optional actual observation/edition. Root must supply these from its owners; the adapter is not a new authority factory. `Occasion::Selection` / `BeforeFirstAction` label CK-1/CK-2. `CatalogCoverage::{Unobserved,Partial,Complete}` distinguishes unread omission from observed absence. `channel_enabled:Option<bool>` retains unknown; harness signals remain unobserved by default and current0.160 does not borrow old0.158 presence rules. `RoleInForce` is the existing typed ROLE value: known role, observed no-role, or unknown original.

The immutable preparation retains declaration/findings, selection identity, role/supply reference, evaluation time and per-requirement purpose/fallback/outcome. `view(&current_basis)` computes old/not-current standing without mutating old bytes. Reports are advisory, explicitly unpublished, adoption unknown. `result()` is observational, not permission. No additional approval, workflow start gate, configuration mutation or send modification exists in this core.

The existing helper's two malformed-compatible_roles paths now preserve known Unsupported over independent NotEstablished, matching EXEC §3.5 first-applicable order. Partial missing entries are demoted to unknown before aggregate evaluation; known tool failure survives unknown role; observed no-role keeps the accepted unsupported role result. The consuming path must use owner-held thread RoleInForce, never the renderer's new-chat selection.

## Verification standing

Seven focused controls are authored: original known-tool-failure/unknown-role-declaration precedence; partial versus complete missing; observed no-role versus unknown versus actual role; unknown channel/optional requirement; known missing plus unknown role; current-pin refusal to borrow old account; immutable report currency/advisory/no-receipt.

**Not executed.** The original negative is a predicted failure from source, not an observed test failure. Cargo is withheld until manager grant; no compiler/type-check or test pass is claimed. Parser success establishes syntax only. Review and original-failure/repaired-backcheck remain required. The pure internal currency test deliberately does not qualify Root selection/preparation or actual native environment collection.

## EXEC report → RS R14 fit and remaining boundary

Accepted EXEC `compatibility-report.schema.json` requires current-phase fields including full workflow plus holding_library, host_id/catalog_edition/catalog_readable, surface H/E/X and channel_state enabled/not_enabled, report identity, occasion/time, requirements, workflow_unsupported, checkpoints, runtime_holds, limitations, evidence standing and model destination. The private preparation is **not serialized as that schema**: unavailable host/channel/edition input must not be filled with fictional enabled/not_enabled or a fabricated edition. This core preserves unknown instead, ready for Root's true source values and the owning EXEC format adapter. Full schema serialization/validation is not supplied here; no new field is adopted. Known source values, checkpoint report projection and schema validation are remaining serializer work before durable EXEC report publication.

RS kind `compatibility_report_ref` references `$defs/compatibilityReportRef`: required `report` evidenceRef, `occasion` string and `passResult` enum. The evidenceRef has kind `compatibility report`, reference and actual resolutionAtWrite. EXEC passes maps to RS `pass`; overall nonpass maps to `does not pass` (its workflow role/delegation reason remains in the report); unknown maps to `not established`. Do not put the private preparation ID in a resolved report reference, and do not label no publication “recorded.” W-1 writer already validates RS entries, but no writer/ref resolver for the actual EXEC report is supplied by this task. Exact physical report location remains owning-source allocation, not invented here. Report record fit and WR's pending publication are separate from lifecycle and source-owned text delivery.

## Limits and next step

This is a reviewable private core API, not whole compatibility completion. Await Cargo grant for original negative and unchanged repaired checks, inspect results, repair within this private scope, then fresh independent review. Root later consumes serially and supplies actual environment/role basis, CK occasion timing, visible report and record handoff. Actual0.160 environment collector/positive claims remain separate. No native or UI claim follows from parser validation.

## Candidate hashes

- `src-tauri/src/execution_compatibility.rs`: preimage `ecdfb8b01a1e6dbb42ef00992a8d990a841dbe6d1c66224064bd1facdfff9994`; postimage `73fe9cce5f059661fbc59c9e879618f2f3f8fa9bc5c9b5d02b0e8ecea144cf4b`
- `src-tauri/src/compatibility_report.rs`: preimage `None`; postimage `555b301fe54b8f1159c137fa0c159078e4c1eb88f44418d4ab62f51a508d0e1d`
- `src-tauri/src/compatibility_report_tests.rs`: preimage `None`; postimage `b3f277402b863b3c832cc3aafe3b1e763796db6ab488578b3116ce079bfd74ce`
- `/private/tmp/chirality-i2-compat-core-zc_6up7q/BASE_MANIFEST.json` SHA-256 `12938ea06a789db27523c69b389044cac2eb0aeb0bafe6ac67f356764cea0ada`
- `/private/tmp/chirality-i2-compat-core-zc_6up7q/ORIGINAL_NEGATIVE_HELPER.rs` SHA-256 `27067e883ef4f93360bc931248f0c6a6bcf70b8eaff4286419d53e1b6331dd82`
- `/private/tmp/chirality-i2-compat-core-zc_6up7q/compatibility-core.patch` SHA-256 `b7899403a299f637eb6198356134a997c2c6b5168bdd99b5d146fc679b85a91f`

## Granted Cargo verification — completed

Parent granted the sole private lane. Used CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home, shared assigned CARGO_TARGET_DIR, CARGO_NET_OFFLINE=true, CHIRALITY_SKIP_CODEX=1 and --offline --locked throughout. No download or actual supplier launch. Private source only; source contribution hashes above unchanged.

- Original helper compiled; the first exact-name filter selected zero tests (preserved original-negative.log, not counted). Copied its exact executable to original-tests. Running the full substring control then executed one test and **failed as required**: actual NotEstablished versus expected Unsupported (original-negative-executed.log; exit101). This is now an observed defect under unchanged EXEC §3.5 criterion, superseding the earlier predicted-only standing.
- Restored repaired helper; repaired-controls.log: **7/7 pass**, including the same original-negative criterion.
- Copied exact repaired executable to repaired-tests. Existing workflow_role_tests: **21/21 pass**, including required/optional/unknown tools, delegation negative precedence, fixed role and source-byte preservation.
- An additional role_lifecycle filter selected zero tests (existing-role-lifecycle.log, not counted). No whole role-lifecycle claim is made.
- cargo check --offline --locked --lib: exit0 (ordinary-check.log); existing/unused warnings retained, not treated as defects merely because warnings exist.

Cargo lane released after these checks; independent review remains ahead. Neither test suite exercises Root UI/writer integration or positive current-pin inventory. The private prepare API still lacks a connected Root caller; no whole compatibility completion claim.

## Clarified serialization source fit

The earlier language about unavailable host/edition must not be read as proof of a schema contradiction merely because fields are required. EXEC CR-4 explicitly supports “catalog unreadable”; schema host.catalog_readable=false can truthfully represent that while a previously observed host/edition remains known. RF-1 allows whole check not established. Prototype required_tool_check.py retains cat[edition] even when cat[readable] is false. Thus unreadable inventory with known edition/channel **is representable without any schema change**. A schema nonempty string alone does not dictate an ID algorithm or prohibit an explicit absence label, but no adopted sentinel-label convention for an entirely unobserved host/edition was found; this is an owning-source mapping question, not established incompatibility.

The narrower actual omission is channel state: schema `$defs/surface` requires channel_state and enumerates only enabled/not_enabled. EXEC §3.2 explicitly maps ADAPTER enabled→enabled, disabled→not_enabled, endpoint-unavailable→enabled; the latter does not mean unknown channel. The private core receives Option<bool>::None because no collector was provided, not because a source proved disabled. No accepted mapping from absence of observation to either value was found. Supply actual observed state where available; lack of a collector is not by itself a contract conflict or a reason to amend the schema. Required schema report fields should be prepared only after their actual source facts are supplied, or the report remains absent/prepared with the observed limitation under RF-3 (no partial pass). This preserves the core's unpublished standing.

If the owning EXEC/ADAPTER source confirms that full persistent reports must be emitted while channel observation is genuinely unavailable, the narrow proposal for its review is to add an explicit not-established channel representation (and matching prose/fixture/consumer mapping) or an adopted absent-observation variant; neither is adopted here. Otherwise the correct repair is the missing collector and report serializer, not a schema amendment. Parent/source owners decide under named reviewed change control; no extra human checkpoint is established.

R14 remains a reference to an actual evaluated/published report; the private preparation is not that receipt. Physical storage/ref resolution remains unsupplied, independent of the legality of known-edition unreadable-catalog reports.

## Verification artifact hashes

- `/private/tmp/chirality-i2-compat-core-zc_6up7q/original-tests` SHA-256 `5d2f61270406d35a27c3db5df6bab907b0a0d5dba160fef16da76ca1ed9eb36d`
- `/private/tmp/chirality-i2-compat-core-zc_6up7q/repaired-tests` SHA-256 `3bc6c4f0151e6f3816d7ffc03fd6d55962532e77d16229fcb7c5c53b6b9fbf2e`
- `/private/tmp/chirality-i2-compat-core-zc_6up7q/original-negative.log` SHA-256 `88abcb315a11b84ea0e7f1754fb9afa58875cb7f00c8d134119222f1ebcb726f`
- `/private/tmp/chirality-i2-compat-core-zc_6up7q/original-negative-executed.log` SHA-256 `8da4dfc2861e861b3f13caaad7cda148d7fcc9d6e81191c4bf351fd569e0d430`
- `/private/tmp/chirality-i2-compat-core-zc_6up7q/repaired-controls.log` SHA-256 `3b79024e87abb57cbb1363f55b84953108e1cc06c8f19d38d14a04787ca45d5e`
- `/private/tmp/chirality-i2-compat-core-zc_6up7q/existing-workflow-role.log` SHA-256 `0b22e711bce0304d259e25e11c5f7fcc69387a25033df44daa64d422c93183e3`
- `/private/tmp/chirality-i2-compat-core-zc_6up7q/existing-role-lifecycle.log` SHA-256 `7bd450565da4e8d58fe8bc6ae1c8932a44d9de9175015249c2383a1663a23b0d`
- `/private/tmp/chirality-i2-compat-core-zc_6up7q/ordinary-check.log` SHA-256 `53168500f54567fb05089a1617b8925544af9c865693bbf3d56689d091383b64`
