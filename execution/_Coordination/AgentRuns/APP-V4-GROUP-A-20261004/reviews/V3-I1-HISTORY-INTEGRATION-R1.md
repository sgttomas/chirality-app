# V3 R1 — shared history/ROLE integration repaired successor

Disposition: **READY for bounded shared integration fan-in**. HJ-1 is repaired at the exact candidate below. Independent same-reviewer TASK backcheck, 2026-10-05, `/root/group_a_execution/contract_reviewer`, parent `/root/group_a_execution`, gpt-6.1-sol/medium. Original NOT READY association remains in `V3-I1-HISTORY-INTEGRATION.md`; no model-diversity or broad qualification claim.

## Exact successor

Author record `changes/I1-HISTORY-INTEGRATION.md` with R1 append: SHA-256 `d14d1e3be1344db4db1dbf70fc4fa3a58916d3e47cc454e36bb8978825f0bcfb`.

| Source under app/ | SHA-256 |
|---|---|
| src-tauri/src/lib.rs | 4ab7de274ac32b661d1af1c540a30680c699597e22da07bca700fa5a3b79a989 |
| src-tauri/src/runtime_session.rs | ed2e61b60828a2cd39510e919cc00bff733185e68120fa5726684ae11a940601 |
| src-tauri/tests/history_integration.rs | d41b42bc40b349f24b56b9d61e20a2efd9a15b804f7a9d645e9ffe70624a3ca5 |
| src/App.tsx — unchanged | 316cd7b31c5d8b8857380779a02936e766c71374eebb12d406baebca2f4e1d4a |

Core whole-file input for focused fixture: `hosting.rs` SHA-256 `fe3d797cff2cc2bd89b41673052fa0cd6012ab1e24b8ad11b5c2ad5895075315`, with cfg(test)-only receipt-refusal extension. Production Host dependency is the separately reviewed repaired `0c381383a6c68d15bae9935b2ebca1e2f2f24099f27291714aaa72263a281a2d` association; this review does not replace its independent Host verdict.

## Repair backcheck

`claim_start` completes fallible supply-reference preparation before publishing a claim and leaves previous selection intact on error. The command captures postclaim work in a Result path and routes failure, generation mismatch, native error, malformed result and receiving-state refusal through `finalize_start_attempt`. Selection cleanup checks original conversation attempt ID and full owning generation. Role status uses matching attempt/G guards while access selection is locked; stale completion cannot overwrite a newer claim/status.

`start_dispatched` retains the genuine private SourceRequest before fallible PreparedStart construction. Refused preparation remains visible across later receipt reconciliation; absent PreparedStart cannot bind a role or admit the start. Actual dispatched effect remains uncertain or correlated as observed, with no synthetic no-send claim and no automatic resend. Source inspection of `ConversationSelection::started` confirms fallible checks precede its successful state mutation.

Earlier valid shared semantic warrants are retained: local/RPC identity distinction; current full-generation receiving joins; explicit read-only history and latest Continue admission; original frozen role context independent of current hints/selectors; no resumed role invention or copied native transcript/base/config receipt cache; existing request/ledger/observation/I3/text/interrupt paths. App source is unchanged, so prior frontend build/static-render evidence applies only within its recorded scope.

## Independent focused checks

From repository root, existing `CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home`, `CARGO_NET_OFFLINE=true`, `CHIRALITY_SKIP_CODEX=1`, `CHIRALITY_CODEX_BIN` unset. Exact command prefix: `cargo test --offline --locked --manifest-path projects/chirality-app-v4/app/src-tauri/Cargo.toml`.

| Suffix / preserved input | Actual result |
|---|---|
| `--test history_integration failed_no_effect_preclaim` | exit0; 1/1 PASS, 6 filtered; injected no-effect entropy failure preserves previous selection and later explicit claim |
| `--test history_integration every_postclaim_error` | exit0; 1/1 PASS, 6 filtered; dispatch/preparation/result/generation/mixed-envelope errors clean up; newer attempt/full-G controls preserve newer Starting |
| `--lib history_bridge_joined_session` | exit0; 1/1 PASS, 72 filtered; genuine private written receipt survives role preparation refusal and correlated response without binding/admission/resend |

The Core check uses `/bin/cat` as an own-code transport fixture, not a stock native supplier or model. No full35 repetition. Exclusive Cargo slot was released immediately after these three checks. Author35 passing checks remain author evidence, not substituted for the focused independent backcheck.

## Bounded manager documentation checks

`app/README.md` SHA-256 `b12f42a0d325aa6aeb779f173a6b4f71052a2181c68f3998bd89eb83f9a32dfd` contains numbered step11 and source-grounded Run controls: Read stored conversations, select/read metadata/turns/goal/items, opaque stream paging, and separate Continue admission. Retained process-local original-role versus cold Unknown and child-metadata limits match source. Backend witness and physical UI qualifications remain separate. The reviewer's earlier missing-step lookup assertion was corrected; no missing-step finding remains.

Current manager-maintained WORK_GRAPH observed SHA-256 `9f593abcd69fe792ab32416c7070a737033450234426c8f4a6452318547ba8d5` is an execution-state observation, not a frozen source pin. Its repaired Host/shared-review progression and retained physical UI/native lifetime/cold-role gaps do not inherit older live witness coverage into changed source.

CI11 followup `investigations/UV_STOCK_ROUTE_FOLLOWUP.md` SHA-256 `8d0c7a523dc865bef84d17b416f7c8d38583f3f2e1092af4cdb47181e44bbc91` distinguishes source-level direct local RPC admission from automatic hosted advertisement/eligible connection routing. Local verification service/key readiness alone does not establish backend credential/verifier registration, delivery or positive acceptance; truthful current third-party identity remains outside the stock automatic predicate. This is a bounded correspondence/truthfulness check against supplied investigation evidence, not new primary-source retrieval or primitive execution. No broad “no route exists” or completed acceptance claim is warranted.

## Remaining limits and method

No outstanding blocking finding in the repaired shared scope. Actual changed-source native stored-history/resume/role-lifetime examination, physical UI/IPC witness, persistent role-source custody/reconciliation, child-role supply, CI11 prerequisites and broader qualification remain unfinished with their owners. No whole ROLE or Group A completion, product release, adoption of untested native behavior, or closure of trusted persistent replay is granted. W1 and prior standing/custody limits are preserved.

Selected software-code-review skill and Root/TASK instruction hashes are recorded in the original review and unchanged for this backcheck. No delegation, network/auth/model/native supplier/Git operation or product/Design write; only the two assigned review records were written. Exact successor hashes were independently rechecked before this disposition.
