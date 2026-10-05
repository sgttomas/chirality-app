# V2-I5-TRACE-ACCOUNT — independent original local account review

2026-10-05. **NOT READY for the original I5 account's EXP semantic-conformance claim: I5-1 requires repair and sealed successor backcheck.** Valid XT coverage/custody/no-qualification behavior below remains supported. This holds this I5 contribution, not unrelated I1–4 production or PR1086's frozen source.

Independent TASK `/root/group_a_execution/aac_contract_review`, delegated-harness-native child of WORKING_ITEMS `/root/group_a_execution`, no delegation. Applied retained software-code-review skill to frozen source/tests/resources and exact XT/EXP/DEP09-09-012 obligations. Read original return, full module/tests, relevant schema semantics, XT X-R1…5/§5.1 and EXP §3.1/R1/R4/R5. Only this report written. Manager granted a short focused reproduction slot, released promptly; no product/Design/schema/Git changes, network/auth/model/native/supplier execution. Scratch compiler harness was removed after result capture.

## Captured original candidate

Original external_trace.rs SHA `d1aa1f3f7fecaf587fff298569db5ec05ab0432a6657d6feca03addc3ae59767`; tests SHA `95921cd486a1a1a5280bd1468702dc5cc647bb7902b723602c4a264ba562c9cb`; I5-TRACE-ACCOUNT.md SHA `7d41f6908e10ea567e6c62ce7801159bcff32df5856d0ef09fec8115196b8f83`. These matched the supplied candidate when read and before the focused reproduction. Ten maintained schema/example resources independently matched exact source bytes and manifest hashes.

The original owner is intentionally repairing after the confirmed finding. At report close source/test/return had advanced to `22d9ad6b…`/`1a3116fe…`/`d4952e1d…`; they are **not** certified by this original review. Parent confirmed preservation of original control/raw invalid input and will commission the sealed successor. No “unchanged final hash” claim or verdict on moving repair bytes is made.

## Blocking finding

**I5-1 [P1] EXP-R1 overlap is accepted as a semantically valid supplied record.** Original location: external_trace.rs `semantic`, ExaminationResult branch. It compares the top outcome with aggregate(parts) but never inspects parts_not_applicable or checks disjointness against run-part IDs.

Trigger: unchanged maintained illustrative EXP-EX-08 has four passing run parts and P22-G declared not applicable. Change only `parts_not_applicable[0].part` to `parts[0].part`, P22-A. The result remains schema-valid with top outcome pass, but P22-A is both run/passed and declared not applicable. EXP §3.1/EXP-R1/R23-19 says a not-applicable part is excluded from aggregation and **never also appears among run parts**. Shape validity cannot enforce this cross-list condition.

Impact: the account returns refusal=None / observed_supplied_record for a known semantic conflict, so its EXP-R1 validity guarantee is incomplete and the receiving manager could rely on a result violating its protected applicability basis. Global joined-witness counts remain false: the reproduction does not claim an actual host witness or an executed passing suite. Correct raw-byte retention does not cure the missing semantic refusal.

Repair: compare run-part and declared-not-applicable identities before aggregation; refuse overlap with a precise reason while retaining original bytes/document. Preserve pre-run declaration/fixture binding and original applicable-not-run rules. Do not remove offending parts or weaken schema/criterion. Add unchanged valid EXP-EX-08 and the shape-valid single-field overlap control; assess repeated part identities explicitly where they could obscure applicability. Freeze repaired source/tests and backcheck affected EXP semantics.

## Independent focused reproduction

Installed standard Draft202012Validator accepts the original EXP-EX-08 and the overlap mutation against unchanged exam.result-record schema. Canonical JSON SHA of the mutated semantic input (sorted keys, compact separators) is `b0379aa05e723d945f89d52fd24d9648d8de637c1f8bf114c1445c1de3c2e6bc`, recoverable from the maintained fixture and exact mutation above.

A scratch Rust test compiled the exact frozen external_trace/schema_validation modules, linking existing cached serde_json/jsonschema artifacts; rustc exit0. The unchanged original control was accepted. The same account received the overlap with the existing test envelope candidate:local-1 / origin:local-1 / ExaminationResult and explicitly supplied NativeSupplier category, retaining the fixture's scenario/route as a **source claim**, not actual native evidence. The original document is ILLUSTRATIVE, not a real candidate. Bytes remained exact, top outcome pass, refusal **None**. Assertion requiring EXP-R1 refusal failed **exit101, 0 passed/1 failed**, 0.07s; unrelated included setup test was filtered. No nine-test duplicate suite ran.

Recoverable essential assertion:

```rust
let mut overlap = original_exp_ex_08.clone();
overlap["parts_not_applicable"][0]["part"] = overlap["parts"][0]["part"].clone();
let entry = account.receive(supplied_record_of(overlap));
assert!(entry.refusal().is_some()); // Actual original result: None.
```

Author's original result is **9/9 pass**, eight I5 functions plus included AAC setup test, at its recorded frozen source. Those tests were independently read; they omit the overlap. Repeating unchanged success cannot establish repair of this known conflict.

## Supported boundaries and remaining consumption

Declared-ID/no-retrieval registry checks schema before semantic rules. Malformed JSON, schema failures and candidate/origin/source envelope mismatch retain exact raw bytes and parsed document where possible. Original subject/configuration/date/case claims are not rewritten into actual observations. Work-account checks require the full **39 rows** (H/E/X×12 plus X native mapping, E tool offering and App-X configuration), reject duplicates/wrong receiving surface/C8 mismatches and keep unobserved changes/other work unknown. Schema binds XT case family/witness and EXP basis/subject/route; supplied source references do not authenticate host/candidate or prove case execution.

XT aggregate failure/blocked/not-run/mixed outcomes remain distinct; blocked carries a cause. Native-needed and actor≠recorder guards preserve owning evidence meanings. OI003 ruling claims are refused within this local-only scope. Actual-host/extension observed attachments are not admitted; supplied-record categories are not promoted to joined observation. Snapshot keeps not_supplied joined standing and no V4-EXM24/25 count. Own-code result/review references remain bounded source inputs, not native supplier/host/extension capability or one-effect proof. No effort/cost/savings criterion is invented.

DEP09-09-012 supplies B's authored examination protocol, not completed native/host examination. This local account has no blanket prerequisite on completing all I1–4 modules. After I5-1 repair, actual API/record consumption still needs its candidate/source/case association and explicit source-claim versus actual-observation display. H/E/X same-operation/edition trace, extension, A13/engineer acts, host application/receipt/view and native/packaged/host qualification remain unperformed/deferred with OI003 unresolved. No dispatch, host effect, scope cut or release follows from storing this account.

Return: bounded original I5-1 repair/backcheck, reuse unaffected schema/custody/work-row assessment, preserve original failure and candidate history. Do not reopen unrelated production or complete the missing trace witnesses on paper.
