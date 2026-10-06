# I2 RS supply correspondence — private implementation

2026-10-05. Fresh continuation of native TASK
`/root/group_a_execution_astra/rs_supply_design`, parent
`/root/group_a_execution_astra`, dispatched Astra/low; no descendants.
Parent granted a private exact-b44 implementation only. No maintained App,
Design, graph or CONTRACT_ISSUES changes; no Git/Cargo/native/auth/network or
download operations. Source V6 remains the reviewed technical basis, not
implementation review. No new skill/workflow activated.

## Result and frozen candidate

Private App:
`/var/folders/0s/50y7rb796d1bqdxmpcz6qg800000gn/T/chirality-rs-supply-o9jokxgg/app`.
It was copied from parent's stationary archive
`/private/tmp/chirality-wr-rs-b44-epkrjq_8/projects/chirality-app-v4/app`, whose
SOURCE.json binds exact `b44f6bfc1aa435d1160cc2701db46a54bd958a3c`.
The changed-file hash manifest and full reconstructable patch are in
`private-rs-supply-implementation/manifest.json` and `implementation.patch`.
No snapshot files outside that manifest were changed.

- `records.rs` gains only a nested `records::supply` module declaration.
- New `record_supply.rs` checks immutable WR-to-RS historical correspondence.
- New `record_supply_tests.rs` supplies six bounded test functions.
- Bundled RS schema equals V6-reviewed private schema; two new private fixture
  files carry its reviewed positive/negative examples. Schema manifest and the
  two existing policy-standing RS schema pins receive the exact new hash.
- No changes to shared lib/runtime/App/storage, WR resources/source, lifecycle,
  native or supplier code. Root must add the missing live producer connection.

## Concrete API and scope

WR owner and RS owner agreed once on
`workflow_workspace::publication::ProjectRecords` and `ResolvedRecord`.
RS uses `ProjectRecords::resolve(&str)`; `ResolvedRecord::{reference, body,
envelope, same_project}`. WR owns validation, immutable publication, recursive
basis resolution and pinned owning-project identity. These objects retain
historical evidence only, with private fields and no Deserialize.

`records::supply::correspond(&ResolvedRecord, &ResolvedRecord)` returns
`Result<HistoricalSupply, CorrespondenceError>`. It rejects wrong kinds,
projects, run/conversation/purpose, missing exact run_text basis, mismatched
composed-text method/value and wrong expected-workflow identity. The native
turn comes solely from the resolved WR check; absence returns
`MissingNativeTurn`, with no client-ID/ordinal fallback. It copies all six
WR states exactly, preserves check evidence limits and unknown adoption, and
retains sourceIdentity as JSON serialization of the complete workflow identity
tuple. That string is a tuple description, not a new minted identity, hash or
cross-source equivalence rule. The supplier reference retains its source.
Verified claims with unequal expected/observed method+value are refused.
Incomparable preserves its original methods through the check reference and
never becomes value-only equality.

`HistoricalSupply::{run, recorded_claim, limits}` is read-only access to a
historical reconstruction. It has no Deserialize/Clone or writer conversion.
There is deliberately no new append entrypoint consuming it. Existing generic
RS writer remains unchanged; a caller must not mistake historical schema
conformance for source-native supply. Each successful result explicitly says
historical correspondence only, no live witness/adoption/registration/lifecycle.

`read_correspondence(&ProjectRecords, &Value)` validates the complete RS entry,
resolves its supplier records in the explicit project, then compares recorded
run, native turn, thread, source tuple, purpose, content and state to the owning
WR records. It returns `HistoricalCorrespondence`, `LegacyOrdinalRetained` or
`Limited`, with explicit limits. Legacy workflow ordinal records are preserved
without an inferred native mapping. Unresolved/corrupt or mismatched references
stay limited. Historical `resolutionAtWrite` is not treated as current proof.
No transcript, native page or generated prompt is persisted.

## Missing live source seam, explicitly agreed with parent

WR's `CompletedSupplyCheck` has private fields, no Deserialize and no production
constructor. `PendingRecord::supply_check` will consume that token plus resolved
run_text; WR persistence is not itself native observation. Neither arbitrary
JSON nor coverage seal alone is sufficient: the seal proves page/query
coverage, not that a supplied comparison was calculated from those pages.

Parent confirmed the actual sole assembly point remains Root's
`WorkflowRun::check_native_supply`. Root must construct the completed-check
capability there while actual PreparedRunText, accepted page observations,
comparison, exact native thread/turn/client/item and source receipts are bound
together. Root then publishes WR and supplies a typed newly published completed
check to the future RS append integration. No fake factory or constructor is
included here. A run_text written before send remains preparation; failed send,
unknown turn or missing completed-check capability cannot become supplied R3.
Post-send WR/RS failures retain missing/pending facts and never trigger resend.

This is therefore a complete bounded historical receiving contribution, **not
full live R3 publication**. New append capability, actual Root connection,
cold resolver/disk integration, two-read/retry behavior and lifecycle remain
with the parent's connected assignment. The schema/example propagation is
private and does not claim maintained adoption.

## Checks and independent review

Rustfmt `--edition 2021` parsed/formatted the two new Rust files, exit 0.
Installed Python 3.13.7/jsonschema 4.26.0 validated the complete native fixture,
refused all seven complete negatives and retained three existing supplied-
guidance fixtures using only locally registered embedded schema identities.
`check_shapes.py` reproduces the shape check with retrieval explicitly disabled;
`validation.json` retains versions and limits. No Cargo/typecheck or Rust tests
executed: parent expressly retained the no-Cargo hold for this child.

Six Rust test functions cover exact six-state preservation, both text purposes,
full source tuple/composed identity, absent turn without client fallback,
wrong scope/basis/content, incompatible-method equality refusal, and complete
schema/exclusive-coordinate fixtures. These tests are authored, not reported
as passing. Actual WR resolver operations/cold reads and fresh source-backed
append still need connected tests after fan-in. No supplier/native/API or
product qualification is claimed. Fresh independent implementation review is
required; V6 reviewed only the source contract.

Read basis is the earlier CC-RS report's instruction/source set plus V6 final
review, parent's archive SOURCE.json, agreed WR API messages, maintained
schema_validation/workflow_workspace/hosting/native_history interfaces and
current schema pin manifests. App-v3 instructions remain excluded as recorded
in the earlier report. Parent remains sole integration owner.

## WRRS-1 successor

Independent implementation review found that the actual end_notice body has
no workflow tuple; the initial receiver and renamed-start test were wrong.
The original candidate above remains preserved. The named reviewed source
clarification, exact original-code negative, repaired original-start lineage,
actual end publisher/reader regression, 70 passing combined affected tests and
ordinary check are recorded in `private-rs-supply-endnotice-repair/REPAIR.md`,
with final patch, source manifests and canonical logs beside it. That private
successor supersedes the implementation above for review. No maintained
adoption or live Root producer/append is implied.
