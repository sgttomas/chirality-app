# Group B S4 synthetic test exchange

The cfg(test)-only hosting_s4_export module exports group-b-s1-reader-exchange.v1. It reuses the actual synthetic Host Fixture and Store setup, reads Host.distribution_evidence through its live native-held reference, and takes actualLt09 from Host.lifecycle_events. There is no production export or JSON reference rehydration API, new semantic authority, supplier execution or qualified claim.

Create a fresh private parent under the physical system temporary directory or /private/tmp. Set CHIRALITY_S4_EXPORT_ROOT to its absolute physical path. Run from app/src-tauri with the prepared offline Cargo environment:

```sh
cargo test --offline --lib export_group_b_s4_selected_and_unselected -- --ignored --exact hosting::successor::tests::s4_export::export_group_b_s4_selected_and_unselected --test-threads=1
```

The test exclusively creates selected/ and unselected/. Existing destinations refuse. Each contains exchange.json and publication/ with untouched raw members, including transport. selected additionally contains selected-source/ with untouched complete original declared closure; unselected has null selectedSourceMembers and no such directory. Member arrays are sorted POSIX paths with lowercase SHA256 and byte sizes. Paths, duplicate manifests, changed bytes, source closure mismatch and unavailable native read refuse. Copy readback must equal captured bytes. Output is diagnostic scratch, not a durable production store; partial failed exports are not valid exchanges and must not be reused.

Closed top-level fields are format, case, readback, actualLt09, members, producer, applicationCandidate, selectedSourceMembers. readback and actualLt09 preserve JSON values; raw artifact members are never reserialized. producer records checked-out sourceRevision, exact executing test executable SHA256, actual harness argv, sorted active features and kind synthetic-host-test. applicationCandidate is an explicit invented fixture input: revision INVENTED-S4-APP-REVISION, buildIdentity INVENTED-S4-APP-BUILD, standing invented-consumer-fixture. It is never derived from the harness identity.

For an exact source seam, run only after the exporter is committed and compile the harness at that exact revision. Initial author exports from an uncommitted candidate are precursor diagnostics: sourceRevision identifies checkout HEAD, not inclusion of uncommitted helper bytes. Their separate candidate manifest and harness hash preserve this distinction; they are not the positive exact-commit Group B receipt. A manager must rerun after committing the independently reviewed candidate. Even an exact committed exchange establishes only synthetic consumer behavior, not S3 qualification or native App/supplier operation.
