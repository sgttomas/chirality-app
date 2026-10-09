# Critical-set grammar — bounded Host/storage receiving review

CONCUR as a conditional source grammar at final proposal SHA2562a3487133c3b62789f0eb0ddfdff3d9d929447c79ceb76dcc910c0374a0fcdf6. Cases SHA25674f5111652d62d0857452b0bbd077410cd1b584325478ba60300e493c458f037 (83 designed cases); basis SHA2567afb772f1b8a3989daf08339d1c89f21d13da8272225e4fef6720312cccdd54d. All10 source pins verified at their declared revisions. No parser/implementation tests, code, process, new agent/worktree or RS adoption performed.

## Exact findings and backcheck

Reviewed initial supplied repaired cut1bf3db8cd1ce8e20a912a158cf2d68774124022b8ba82004599565b305c7e884. Two additional Host/storage findings were returned to Group C:

1. Original Host request identity was incorrectly required to have a received receipt position. Actual SourceRequest can be registered with no attempt, or completely written while no response/event exists; send/attempt positions cannot be substituted for receive counters. Final2a3487 repairs Source and §10: request receipt_position=null, actual request_attempt_position nullable and source-owned; event receipt positions remain separately required. This records actual request facts without a fabricated reply/cut or premature authorship.
2. Historical-only artifact edges did not clearly carry their classification into retention/source dependencies. This could indirectly require all old snapshot retention despite the historical exception. Final2a3487 explicitly propagates REQUIRED/HISTORICAL_ONLY through both sources and artifacts, with any independent required path winning; unresolved attempts and their sources remain required. Missing optional historical retention source is still diagnosed, without blocking the resolved current recorded subset solely for that optional branch.

Both exact repairs address the findings; no remaining blocking Host/storage source contradiction identified. Earlier combined repairs remain appropriate: every required dependency needs actual resolved read state; unknown source owner/namespace is null rather than invented from recording context; Prior/Final→Attempt normal form avoids mandatory back-reference cycles; exact final-account subject/binding checks do not turn cold matching bytes into original confirmation.

## Host/role and method boundary

The new request-position field belongs only to this proposed external grammar; it does not change Host H5 or REC records. Current SourceRequest/SourceEvidence can retain original frame/ref/write/result facts, but those public projections cannot reconstruct a live source capability. Received response/item/terminal require actual source classification and generation-local receipt identity. A request source alone cannot complete answer/review custody. Closure, late frames, copied roles, imported history and equal bytes preserve their limitations.

Method tags remain proposed dispatch names, not existing exports. Before supported observation adoption, map each use to its exact owner method and required native tuple: requestRef/RPC/source write, event classification/position, role supply origin, file identity and attempt/commit source. AA-CAP-PF1's domain-separated parsed-frame digest, compact Host frame serialization and an artifact's raw-byte SHA256 are not interchangeable. Freeze serializer/version and projection/redaction limits; never call parsed-Value bytes original wire identity. The dormant AA-CAP/core and call-custody manager handoff supply no production CCE RoleSourceLease or authored answer/review producer.

Unknown/unmapped methods must stay unsupported as §7 states. A future reader must not implement nominal enum recognition as successful method resolution. It may report recorded consistency and gaps while source_authenticity remains not_established_by_cold_bytes and live_authority not_restored.

## Storage and acquisition boundary

Typed lookup, computed required closure, no orphan/cycle policy and required-wins classification are coherent as designed constraints. Every external-envelope ref stays in its own inventories; current descriptor/hash/confirmation cannot become a self-edge into the manifest. Cold original_confirmation_source remains null; a live confirmation requires actual storage custody outside deserialized data. Current-byte observation does not establish committed freshness or prior acknowledgement merely because journal/revision fields are present.

Historical-only absence does not license deleting required old bytes or attempts. Prior-state comparison is necessary for replacement-preservation proof; without it that proof remains unassessed. Dependencies cannot be demoted by editing lists or relabeling an unresolved attempt. The acyclic normal form retains exact intended subject while omitting the circular subject_record backlink; it does not remove a real dependency.

Before reader code, select and prove bounded original-byte acquisition, numeric-string comparison, parser depth/width/count/string limits, graph work/visited-state bounds and issue-output limits, including external inventories and prior-state loading. No read_to_end-before-cap or unbounded recursive resolution. Total retention includes raw artifacts, metadata, staging and unresolved leftovers; small manifests are not small storage. Immutable namespace/store, locking, quota, retention and retirement remain unimplemented/unselected. Acquire storage outside Host/role live locks; preserve original immutable observations and recheck owning revisions rather than recreate authority while resolving cold files.

## Contract consequence

No accepted Host/REC amendment is required merely for this external source grammar and historical/gap distinctions. Actual adoption of a source exporter, combined CCE mint, method mapping, new durable payload/ref retention or reader dispatch requires named owning review; it is not supplied by this concurrence. Existing account0.1–0.4 publication and read-only0.5 remain unaffected; no journal gate or implicit0.6 is introduced. Rich diagnostic states stay separate from original RS literals and no automatic coarse projection is supplied. This reviewer is not the DEL-04-03 owner and gives no RS adoption.

Group C retains semantic integration. N/S/D/T/Q, carrier selection, native/producer authenticity, PM05 and whole-product readiness remain open. The83 cases are definition obligations, not executed behavioral evidence.
