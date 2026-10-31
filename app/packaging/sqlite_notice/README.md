# Exact cached SQLite source inputs

This preparation closes the *source availability* part of the previously
unverified SQLite input. `libsqlite3-sys 0.30.1`'s cached crate is 5,122,296 bytes;
its SHA-256 matches Cargo.lock. Its `sqlite3/sqlite3.c` declares SQLite 3.46.0
and source check-in `96c92aba00c8375bc32fafcdf12429c58bd8`. The index binds the
whole member and retains an exact first-42-line excerpt including its disclaimer/
blessing. The wrapper crate's complete LICENSE is separate; it is not substituted
for SQLite's own source notice. SQLCipher source also occurs in the archive,
but is not substituted for the selected ordinary `rusqlite` bundled route.

The archive build script selects `sqlite3/sqlite3.c` for the bundled SQLite
route; current App declares `rusqlite` with `bundled`. These source facts do not
prove an installed binary's linkage or all feature-unified runtime composition.
No compilation, source download or legal determination occurred. No resource
overlay is changed; actual inclusion is still unobserved. This supplements, but
does not expand the existing direct-runtime index into transitive completeness.

Run `python3 app/packaging/sqlite_notice/check.py` from the repository. With an
already available exact archive, add `--archive /absolute/libsqlite3-sys-0.30.1.crate`
to compare every retained byte and whole-member digest against that archive.
There is no fetch, extraction to disk, native execution or fallback.

The four supplier source/notice associations (Codex main/code-mode-host/rg/zsh)
remain unestablished by the retained platform tree; this SQLite source input
does not resolve them. No arbitrary system license or other version is substituted.
