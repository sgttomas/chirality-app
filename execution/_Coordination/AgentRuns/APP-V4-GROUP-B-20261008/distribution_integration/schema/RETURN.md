# R2 inventory representation repair

TASK `/root/distribution_integration_manager/repair_inventory`, parent `/root/distribution_integration_manager`; harness-native bounded descendant, no delegation. Assigned source: `4c5f691c82d887d943849bf15a5efb9a99eec455`, isolated `codex/app-v4-distribution-schema-fix`. The parent brief is the authorization and write fence. Selected skill: repository chirality-change; no named workflow. Consulted origins and byte hashes are in SOURCE_HASHES.json; the proposal/graph were inspected for this bounded context, not adopted.

The schema now requires minimum and maximum length 64 for both SHA-256 fields, in addition to the lowercase-hex pattern. The pure-value model uses full-string matching for both fields and refuses malformed file digests in the manifest helper itself. It cannot compare malformed identical inventories equal. No manifest algorithm or valid fixture changed.

Ten maintained tests pass, including 22 digest/field cases covering trailing LF/CRLF, short/long values, uppercase, nonhex, whitespace, empty values and wrong types. The file-digest negatives independently recreate the old manifest serialization before checking both schema and combined validation and identical-value comparison; they also exercise helper refusal. Existing positive exact-byte/multibyte/order checks pass. See CHECKS.json and tests.txt.

Related audit: mode is an integer with 0–4095 bounds, not an anchored regex; seven malformed type/range cases reject at schema and comparison. Path semantic checks search the complete string for forbidden CR/LF/NUL/backslash and components; existing newline/path negatives now also check identical-value comparison refusal. Schema deliberately leaves path semantics to the model, as its description states. No path or mode contract repair was warranted.

Write fence preserved: only the new inventory schema, its distribution_identity prototype and this evidence directory. No Design Markdown, app code, shared graph or MEMORY changed. Parent owns integration, notices and any deliverable MEMORY record. R1 is outside this assignment.

The method remains proposed: value checks supply no supplier qualification, real filesystem scan, custody/provenance validation, production verifier, native/package/signing evidence or owner act. No supplier process, download, network, credential or shared Codex configuration access occurred. Independent review of the assembled candidate and receiving compatibility work remain with the parent.
