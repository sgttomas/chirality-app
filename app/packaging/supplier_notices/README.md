# Supplier notice texts and associations

`components.json` lists, for the supplier tree of the declared pin, the components
known inside each member, the committed text that is each component's notice
(repository, revision, path, size and digests) and its standing. The tree itself is
read from the declared pin's `CANONICAL_DISTRIBUTION.json` (the pin is
`DECLARED_PIN` in `app/src-tauri/src/hosting.rs`); its executables are the files
with an execute bit that are neither libraries nor data, a rule that fits this record
(checked against its Mach-O count), not a general proof. The table is a reviewed
input: `../notices/coverage-review.json` binds its digest and lists each component's
standing and exact texts, and its reviewer updates that record. `reviewed_for_pin` names
the pin the table was reviewed against; when the declared pin differs,
`../notices/coverage.py` lists the table as an open component rather than assume
the old associations. Every committed text here is mapped into the package under
`third-party-notices/supplier/`; the voice libraries' licences ship inside the
supplier tree itself.

The folders are the components' root texts at the revisions `components.json`
names: `codex/` (the supplier's root LICENSE and NOTICE, equal at 0.160.0 and
0.167.0), `codex-skills-086ccc83/` (the two skill samples embedded in
`bin/codex`), the ripgrep chain (`ripgrep-15.2.0/`, `pcre2-sys-0.2.10/`,
`pcre2-10.46/`, `sljit-e51eabbf/`) and the V8 stack behind
`bin/codex-code-mode-host` (`v8-15.2.124.1/` with V8's 16 `third_party/` LICENSE
files at the same revision, `rusty_v8-350c5a85/`, ICU, libc++, libc++abi,
llvm-libc, and highway, fast_float, simdutf, dragonbox, FP16 and abseil-cpp as
Codex's `third_party/v8` build files pin them). Each row's `below_root` says what
was examined below the root. Where a root text points to files that are not held
(libc++ and libc++abi `CREDITS.TXT`, and the LLVM subdirectory licences), that is
its own uncovered row. Which component is in which binary is the supplier's
statement in its source, not read from the binary. The crates compiled into the
supplier's executables and into `rg` stay uncovered.

`codex-0.160.0/scripts/codex_package/` keeps the received rg release selector.

## Association readers

All three read retained inputs offline, execute nothing and draw no licence
conclusion. `--write DIR` / `--check DIR|FILE` compare against records the caller
keeps outside the repository; none is committed.

- `associate_0167.py` recomputes the Codex 0.167.0 root-text and inventory
  association from the canonical 0.167.0 tree, the frozen 0.160.0 tree and retained
  public metadata. It checks `codex/LICENSE` and `codex/NOTICE` against the
  `rust-v0.167.0` tree and reads its executables from the 0.167.0 record.
- `ripgrep_0167.py` recomputes the rg → ripgrep 15.2.0 → pcre2-sys → PCRE2/sljit
  association.
- `v8_0167.py` recomputes the code-mode-host V8-stack association.
- `observe.py` remains the 0.160.0 reader.

```sh
python3 -m pytest -q app/tests/supplier_notice_observations_test.py app/tests/supplier_notice_selectors_test.py
```
