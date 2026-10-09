# Historical B2 static supplier comparison

The existing reviewed Rust scanner compared the actual approved cached development
0.160.0 vendor tree with P1 in the retained unsigned B2 App. Result: equal for all
53 entries, including the root, 10 nested directories and 42 files. Complete raw
scanner JSON retains root/directory modes, file kinds, relative paths, sizes and
hashes. Comparison stdout is preserved; success is the explicit equal field,
not exit zero alone.

The scanner executable digest was verified before every invocation and afterward:
03f02e9417ca66544c7c06b154b5350186a4092131d4f334fd6ce3f1023dd792.
The operator-selected source is 543735f459eb7edd0d2ea6bd72a92e597c36dd36; its example
hash is 3bc4ed010a6f322a88b902bcfc90cc705cbe1cb79b1678bcb717ede376537a71.
The retained distribution_static/REVIEW.md independently used these executable
bytes. SOURCE_CHECK.json confirms current example and underlying preflight bytes
match that selected source. This is source/receipt consistency, not authenticated
compiler provenance. No new scanner was built or copied.

File-hash, directory-mode and missing-entry controls each changed only a small
copied inventory JSON. All three comparisons returned exit 0 and equal:false.
The actual trees were never modified. Both trees were scanned again afterward;
their complete inventories remained equal to the initial scans. Full retained
App entries before and after equal the previous BUNDLE_INVENTORY.json (excluding
signature metadata, which was not re-observed). Its file manifest remains
cd0e8f7216d6c85b1b1cee96300e3b1f4aeaea15bbc6185214345290bdb83c15.

## Reproduction and custody

RECEIPT.json records each argument array, exit, stdout digest, source origins and
identities. Substitute the selected physical scanner for <selected-scanner>,
the same approved cached vendor for <approved-cached-vendor>, and the retained
B2 App for <retained-bundle>. Resolve physical absolute paths and verify scanner
and artifact identities before running. The supplier path came from the retained
B2 supplier overlay, checked against the prior P1 record. The App path came from
complete-content/RETURN.md. No links were followed as selected roots. Scanner
stdout contains only relative tree entries; retained invocation paths are neutral.

Use `scan ABSOLUTE_TREE` for each source, then
`compare published.before.json packaged.before.json`. The complete inventories
are comparison inputs, not trust anchors. Controls remain individually identified
JSON files; repeat comparisons against them to verify false outcomes. No supplier
binary is ever an executable argument. The one-time initial availability scan
was repeated in the sealed before/after sequence; only that sealed sequence is
claimed by the receipt. No large copies, caches, installer or build were created.

## Standing and remaining inputs

This is historical development comparison only. Artifact source stays
f79317be861bb63553512de3197b22d556268198 plus overlay author
3269a2c288bdd3b34dbc7c3eb69f868e637a3cf6. Preparation source is
7262736ab1315e611426a5f012caef78c0ee64c2. Neither the newer scanner nor newer
checkout relabels the executable as current source or current S4.

The full prepare.py static-distribution consumer was not run: its required actual
installer bytes and corresponding legacy PKG identity do not exist for this
retained .app. No invented package, S1 envelope, S2 selection or trust reference
was made to satisfy it. This result supplies no S3, qualified pin, FP/native
qualification, signature verification, runtime/H5/Selected/Store event, signing,
release, or package_complete standing. Existing owner/signing and workflow
admission limits remain. No supplier/native App launch, download, new build,
cache cleanup or maintained-source/pin/Design edit occurred.

TASK /root/group_b_successor/complete_content_build under WORKING_ITEMS
/root/group_b_successor reused its clean existing worktree on a new branch;
no agent or worktree was created. Only this evidence directory changed. Official
staged private-term checking precedes commit; no machine names enter evidence.
Independent review follows the exact committed evidence and retained inputs.
