# B2 candidate values — offline preparation

Source candidate: 462f66975d36cd10d5b8455193ada9517d28d353, the actual
merged first slice PR #1117. These are preparation recommendations, not
selected durable signing identity or qualification.

- **Minimum macOS candidate: 15.0.** Read-only `otool -l` inspection of all
  30 Mach-O files in the previously approved complete Codex 0.160.0 tree found
  the largest declared deployment minimum on `codex-resources/zsh/bin/zsh`:
  15.0. Main Codex, Code Mode host and rg declare 11.0; the voice tree declares
  14.0. The unmodified full tree includes zsh. Retained per-file digests and exact
  relevant load-command blocks are in SUPPLIER_DEPLOYMENT_TARGETS.json. A declared
  minimum is not an observed compatibility result. The actual built App's own
  deployment command must be checked before the first package; FP-2/W-4 and
  native compatibility remain unrun. Tauri-utils 2.9.1's config.rs defaults to
  10.13, so leaving that default would not faithfully describe all shipped code.
- **Bundle identifier candidate: dev.chirality.app-v4.** This preserves the
  current `dev.chirality.app-v4.skeleton` namespace while removing the development
  suffix. It remains distinct from App v3's `com.chirality.app`, preserving
  coexistence. That comparison supplies no domain ownership or signed-identity
  proof. No product config is changed merely by this recommendation.
- **Before first signing:** present the concrete candidate with its identifier,
  version, minimum OS, Developer ID team/name, actual resource inventory and
  signing plan to the owner. PKG I-4/SIGN-3 and later SEAL-2 require stability
  of signed identity across releases; do not imply owner selection of a permanent
  identity now. This is the existing account/signing point of need, not a new
  gate on offline preparation. Version and any team/profile remain unsupplied.

HELP_HUMAN's active coordination return expressly retained 15.0 and
`dev.chirality.app-v4` as candidate values with these limits, and directed
continued offline B2/B7 preparation. The message is a parent coordination
instruction, not a new owner signing act. No credential, download, native launch,
signature, notarization, product acceptance or 90% act occurred.
