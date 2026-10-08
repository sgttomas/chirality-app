# B-S4-LT23-SOURCE-ADOPTION-v1

Named technical source adoption for the existing LT09-only S4 file consumer.
Selected Host source: `5c9aabcfb400bab3ef1e283362dc378414621da7`.
Predecessor: `b7e9639d87b84af9a218e05f9e4f3c85fe00ebc0`.
Parent owns independent whole-head review and integration. This is no canonical
S1 rollout, terminal-evidence adoption, owner gate or qualification.

`pins.lt23-source-v1.json` is the fixed active selection, bound by a literal
consumer digest. It binds the preceding namespace pin-file bytes and explicitly
maps prior/new identity under reader_changes. The original pins.json,
pins.namespace-v1.json, f267/b7 fixture cohorts and prior evidence are preserved;
no caller override or fallback selects them for current receiving.

## Actual identity changes

Only `storeReaderSha256` changes within the full reader receipt:
`e78664f9b422344f246099062c9247e484277095d8df2e570f247a02d469c8de`
to `e89b7a56022fc2c5d0860788fa423a94d8072ca0ed184304183e5923ddbe8c57`.
The source is distribution_store_s1.rs, whose producer now permits actual LT09
and eligible same-generation LT23 event publication. Its reported
unsupportedEnvelopes boundary also changes to describe that producer support.
The semanticRevision label, readerSourceSha256, namespace authority source,
closure reader, store guards, schemas, label join, transitions and other receipt
identities are unchanged. Stable labels still do not imply identical source.

Separate selected-source pins renew hosting.rs, hosting_successor.rs and lib.rs
and add LT23_PUBLICATION.md. Hosting adds bounded asynchronous terminal scheduling
and same-source completion handling; this consumer does not reproduce that
behavior. Exact App revision/build remain distinct from partial reader digests.
Source changes and unchanged identities are recorded in the author adoption run.
The canonical EXP/PKG checker and six-record scope remain unchanged.

## Export cohort and limits

The new selected/unselected fixtures are byte-exact actual committed-source,
recompiled synthetic Host exports. Both contain actual LT09 events. Producer
provenance records source, executable digest, command/features and exchange
hashes. B checked bytes and executable passively, with no Rust/App build or native
launch. The application revision/build remains a separate invented consumer
fixture declaration; producer identity does not authenticate it.

The active consumer continues requiring LT09 and refuses LT23 substitution,
terminal capability/authority fields, old/mixed source receipts, byte changes
and false verified/custody claims. A producer capable of LT23 does not make an
LT09 export terminal proof. terminal_evidence_received and
terminal_authority_authenticated are false in every report.

The Host's separate terminal implementation retains pre-spawn observation bytes;
even its actual LT23 association is not renewed integrity, installed custody,
zero-descendant proof or qualification. This cohort tests none of its terminal
scheduling, Stop, worker, receiver-after-Stop or shutdown behavior. Native-held
references and namespace capabilities remain nonserialized. S3, actual App/build,
M1/native qualification, package witnesses, later LT23 receiving and release
remain separate. No second semantic reader or SQ package gate is introduced.
