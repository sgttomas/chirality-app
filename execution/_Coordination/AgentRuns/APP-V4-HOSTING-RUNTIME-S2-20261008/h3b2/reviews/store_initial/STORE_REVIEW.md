# Independent first H3B-2 store review

**CHANGES REQUIRED — one blocking vendor-domain defect.** All 13 maintained hashes match STORE_FREEZE before review. LABEL semantic source and the exact two historical schemas retain the previously reviewed bytes. This review covers development-only Host-attempt storage and receiving, not a full S1 producer/reader or selected closure.

## P2 — Reject physical vendor overlap, not only lexical path overlap

`distribution_store.rs`, Store::open and Store::guard: both use `root.starts_with(vendor) || vendor.starts_with(root)` after merely opening the vendor without following links. On a case-insensitive filesystem, two differently cased paths can identify the same directory while failing both lexical comparisons. Confirmed on this host: app_data `/.../vendor`, vendor `/.../VENDOR`. Both exist as the same physical directory. Store::open succeeds and creates `vendor/runtime/distribution` inside the measured supplier tree.

This violates the explicit vendor-domain exclusion and performs writes before later Host revalidation could refuse changed supplier content. No symlink or hostile concurrent race is needed. Repair physical containment/equality checking, including case/alias behavior of the actual target filesystem, before creating runtime/distribution and during subsequent guards. Preserve no-follow traversal and existing native namespace protection. Do not rely on a later scan rejecting the side effect.

Independent reproduction: `reviewer_case_alias_vendor_overlap_is_rejected`, in the preserved temporary source copy and INDEPENDENT_TESTS.patch. It confirms the host's case alias exists, then fails because Store::open returns success. Log independent.log. No production source or branch was edited; no supplier executes. Target released for author repair.

## Passing controls and remaining assessment

Two additional controls pass: replacing a publication directory with byte-identical files refuses the retained physical reference; changes between initial exact read and final inventory to attempt mode, manifest bytes or extra membership all refuse. These supplement the maintained suite's ordinary hardlink/symlink/missing/replaced-root, foreign generation and no-overwrite vectors. They do not constitute complete hostile-race or OS snapshot guarantees.

Source inspection confirms exclusive no-follow staging, no-overwrite rename, fsync/readback before a returned reference, two digest-bound files and final full-inventory checking. Host publication precedes final vendor audit and short custody guards; evidence reads occur outside Inner and recheck H5/attempt before projection. Native setup requires the store for enabled configurations. The separate display field does not promote legacy supplier standing. The records truthfully retain secondary-home setup, restart recovery, selected closure, full S1 artifacts and canonical receiving as residual implementation. No additional confirmed blocking finding at this checkpoint; repaired candidate and affected tests need independent backcheck before readiness.

Original method/body/schema identity, owner concurrence and LABEL_READY are not silently upgraded to whole-S1 validation. No downloads, credentials, native supplier/App act, canonical source pin/Design/MEMORY change or model claim occurred in this review. Source hashes and parentage are in READ_BASIS.json.
