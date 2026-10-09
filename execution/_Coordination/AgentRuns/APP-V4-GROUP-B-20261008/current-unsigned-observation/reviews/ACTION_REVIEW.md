# Independent proposed signing-action annex review

READY as proposed point-action preparation at `383073bf3d6f478d48043c511c870d4f2e8f5098`. ACTION_ANNEX.md SHA256 `a92b3f7616d7a4f6e726f4f7efef04d58340ae09636a4dc77603152f0d8ff14d`. No blocking findings. This does not record owner selection or authorize execution.

Independent TASK `/root/group_b_successor/complete_content_review`, under WORKING_ITEMS `/root/group_b_successor`, read the complete annex, unchanged signing decision, exact cc18 resource/inventory evidence and selected PKG read_tree.py source, and checked local codesign(1) semantics. Existing review checkout reused. None of the annex commands, copies, signing operations, identity/keychain lookups or artifact mutations were performed.

## Source and command assessment

The exact unsigned App/ZIP identities, source/build and physical paths agree with the separately reviewed artifact. The new fixed experiment path is distinct; refusal covers existing objects including dangling symlinks. It authorizes no removal/reuse. Mandatory checks bind original entries/root modes/sizes/bytes/link targets and ZIP bytes before copy and after copying/signing. Copy equality plus different device/inode pairs for every regular file prevents original hard-link aliases. The approved vendor and copied P1 must match exact source and recorded inventories before and after signing. No original overwrite or supplier-signing target is present.

The read_tree prototype emits sizes and entry identities but excludes the root; the annex explicitly requires separate root-mode comparison and complete size/member checking. Its compare/manifest helpers must not be used as a shortcut around those additional mandatory gates. Physical-root/no-concurrent-writer checks remain required; this is bounded controlled-file handling, not hostile-filesystem isolation.

Signing commands target only the explicit copied P0 and outer App, with hardened runtime and secure timestamp, no entitlements file and no --deep signing. The first omission of --force is conditioned on observing this copy's reviewed linker-signed state. Local codesign(1) expressly allows replacement of linker signatures without --force; the ordinary signature from that operation is then explicitly replaced at the outer App with --force. Changed pre-sign signature state stops rather than broadening flags. The --deep --strict command is verification only.

Post-sign requirements compare actual team and Developer ID authority with the owner's selection, runtime/timestamp/entitlements and sealed-resource status. Full-copy changes are restricted to P0 signature bytes and outer sealing records; all other bytes/modes/links must remain equal. Any error, mismatch or unexplained change stops; no automatic supplier repair or stronger-flag retry. New signed identities and separate actor/recorder evidence are required. No signed archive, notarisation, stapling, Gatekeeper/native launch or installer is included.

## Authority and remaining conditions

NOW on the current development CF5/no-extra-entitlements candidate versus DEFER is a later owner choice, not a prerequisite to accepting unsigned B2. Actual non-secret Developer ID name/team, account direction and Apple timestamp-service contact require owner selection. Keychain/private-key prompts remain personal owner handling; credential collection/discovery/export and autoapproval are excluded. A secure timestamp request is not described as offline.

The no-extra-entitlements purpose remains limited and excludes SEAL-2 qualification. FP1(a)/(b) operations do not imply FP3, qualified supplier, S4/S3, native witness, LS5/LS8 admission or release. Existing signing-decision CF6 DMG/CF7/notarisation distinctions remain unchanged. Exact unsigned originals remain temporary and must not be lost or silently substituted. Parent retains owner presentation and any later execution decision; this review supplies no actual signing success.

Instruction basis remains recorded Root/TASK/App-loop/chirality-change and bounded software-code-review method `ee085d589c44f912d11a59eead8edac214f0343761d26b0d33e886a979888bca`. Prior artifact/signing reviews are disclosed context. No new agents/worktrees, build, download, credentials or MEMORY operations.
