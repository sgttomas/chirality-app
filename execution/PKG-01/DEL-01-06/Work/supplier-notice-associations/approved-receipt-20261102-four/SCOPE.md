# Four approved source receipts and resolved rg/zsh selector joins — 2026-11-02

Parent relayed the owner's approval: "You are approved to download those four
files." It covered exactly the four files in
[`../approved-receipt-20261102/next-source-proposal.json`](../approved-receipt-20261102/next-source-proposal.json),
2,978 bytes in total, at Codex commit `a956835d020762cb2b570053af06f643a11c0ecc`.
Exactly those bodies were received, with no credentials, redirects, extra files
or archives. Each response was refused unless it was HTTP 200 from the exact URL,
read with a size cap of expected size plus one, and matched the exact size and
Git blob. `receipt.json` retains HTTP metadata, SHA-256, timestamps and the
verification result. The bytes are under `sources/`; they were read as text and
never executed. Private custody is recorded in the receipt and stays preserved.
The patch's diff context lines begin with a space, so `git diff --check` reports
them. The exact received bytes are preserved; no whitespace exception is configured.

| File | Bytes | Git blob |
|---|---:|---|
| `.github/scripts/verify-zsh-manifest.sh` | 350 | `cb9bab09…61a3` |
| `codex-rs/shell-escalation/patches/zsh-exec-wrapper.patch` | 998 | `99cdcadc…72a2` |
| `scripts/codex_package/ripgrep.py` | 862 | `155c5d32…b38b` |
| `scripts/codex_package/zsh.py` | 768 | `e4ecc2de…66b0` |

Line references below are to these files and to the eleven files already received
in [`../approved-receipt-20261102`](../approved-receipt-20261102/SCOPE.md).
Retained binaries are those in the cached stock 0.160.0 vendor tree; byte offsets
come from a read-only search, not execution.

## zsh: release selector resolved; byte join still open

- `rust-release.yml` pins `CODEX_ZSH_RELEASE_TAG: codex-zsh-v0.1.0` and
  `CODEX_ZSH_MANIFEST_SHA256: c534eab8…a1` (lines 19–20). It downloads that release's
  `codex-zsh` manifest and runs `verify-zsh-manifest.sh` on it (lines 729–735). The
  script only checks the file's SHA-256 against the pinned value (lines 8–12).
- The workflow passes that verified manifest to `resolve_zsh_bin(spec, manifest)`
  and fails if the target is missing (lines 737–750). `zsh.py` uses the in-tree
  `codex-zsh` descriptor only when no manifest is passed (lines 12–28). The
  release therefore does **not** use the in-tree `rust-v0.134.0-alpha.3`
  descriptor; that descriptor is a default, not the release route.
- The selected binary is copied into `signed_root` (line 752). It is signed with
  identifier `com.openai.codex.zsh`, hardened runtime and a timestamp, then notarized
  (lines 755–774), and packaged through `--zsh-bin` (line 988).
- `rust-release-zsh.yml` builds the `codex-zsh` artifact from `ZSH_COMMIT
  77045ef899e53b9598bebc5a41db93a548a40ca6` plus `ZSH_PATCH
  codex-rs/shell-escalation/patches/zsh-exec-wrapper.patch` (lines 9–10). The build
  script clones `https://git.code.sf.net/p/zsh/code`, checks out that commit, applies
  the patch (lines 24–27) and archives only `Src/zsh` (lines 58–61).
- The received patch changes `zexecve` in `Src/exec.c`: when `EXEC_WRAPPER` is
  nonempty and its first character is not blank, it executes the wrapper with the original path as its first
  argument. The retained zsh (`d715e06e…3b15`) contains `EXEC_WRAPPER\0` once
  (offset 585,164) and the describe string `zsh-5.9.0.3-test-87-g77045ef` (offset
  597,539). A read-only `codesign -d` display shows identifier
  `com.openai.codex.zsh`, hardened runtime and a secure timestamp of 2026-10-01.
  All of this is consistent with this recipe. These are strings and signature
  metadata, not a byte join or signature verification.

**Remaining zsh gaps:**
1. The `codex-zsh-v0.1.0` manifest body (its digest is known; its size is not
   established here) and the archive it names.
2. A comparison of that archive's member with the retained binary, accounting for
   the release signing step, or a supplier build/signing attestation.
3. zsh's own licence text at `77045ef8`. The artifact build copies no licence, and
   the retained package ships none.

The patch is a modification by the Codex project. Its licence comes from that
repository, and this record makes no licence determination.

## rg: release selector resolved; earlier version reading corrected

- `rust-release.yml` calls `fetch_rg(spec)` with no override (lines 742, 751). It
  signs the result with identifier `com.openai.codex.rg`, hardened runtime and a
  timestamp, then notarizes it (lines 755–774) and packages it through `--rg-bin`
  (line 987). `ripgrep.py` fetches through the in-tree DotSlash manifest
  `scripts/codex_package/rg` unless `--rg-bin` is given (lines 8–32).
- That manifest selects `ripgrep-15.2.0-aarch64-apple-darwin/rg` from a 1,764,284-byte
  archive with SHA-256 `3750b2e9…73e4` (lines 6–16).
- The retained rg (`7c7d5b09…739b`) contains `15.2.0` immediately followed by
  `e89fff89ac` and next to ripgrep's "(JIT is available)" text (offset 2,907,359).
  That is consistent with ripgrep's version-plus-revision format. The `16.0.0`
  string recorded earlier starts at offset 3,660,433 (the earlier record's
  3,660,432 is its preceding NUL). It sits between "ARM-64 64bit (little
  endian + unaligned)" and PCRE2's own version `10.46 2025-08-27`. That context is
  consistent with PCRE2's Unicode version, not a ripgrep version. The earlier
  README reading "likely ripgrep 16.0.0" is superseded by this evidence. The
  retained binary is consistent with the recipe's ripgrep 15.2.0 plus a statically
  linked PCRE2 10.46. A read-only `codesign -d` display shows identifier
  `com.openai.codex.rg`, hardened runtime and a secure timestamp of 2026-10-01,
  matching the signing step. These are strings and signature metadata, not a
  byte join or signature verification.

**Remaining rg gaps:**
1. The selected 1,764,284-byte archive is not acquired. Retrieving it needs its
   own owner approval naming that file, source and size.
2. A comparison of its `rg` member with the retained binary, accounting for the
   release signing step, or a supplier attestation.
3. The ripgrep licence/notice files and PCRE2's licence for the linked version.
   The retained package ships the binary without them.

`dotslash.py` (the extraction helper) was not requested or received. The selector
evidence above does not depend on it.

## Unchanged

The main binary and code-mode-host associations are unaffected by these four files.
None of the four complete binary/source/notice associations is yet closed. This
record is not a licensing determination, complete or transitive notice coverage,
supplier pin qualification, or release approval. No signing or native act occurred.
