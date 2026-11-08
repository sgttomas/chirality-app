# Retained root-text associations

This contribution implements local source preparation under DEL-01-06 OUT-001
and REQ-001/VER-001. It changes no commitment, acceptance, release condition or
supplier pin. Main `85505f95` still labelled twelve root-source rows missing;
ten now receive explicit retained-root candidate records. P6 remains open.

The source-controlled `app/packaging/notices/retained-root-associations.json`
is a fixed allowlist with package/version/archive/declared-licence subjects,
original crate-reported repository/revision/path, exact root metadata response
hashes, retained paths and byte identities. `transitive.py` checks its fixed
SHA-256 before opening its proof or any text. The `/3` inventory rows must equal
that allowlist, including unresolved facts and their unqualified standing.
Old `/2` remains accepted with its prior semantics and cannot silently carry
successor text labels. New rows remain in `missing_or_unverified` even when the
specific root file is available.

## Exact local inputs and preserved origins

| Root candidate | Retained source | Git blob |
|---|---|---|
| Dropbox `LICENSE` at `6032b6a9…` | Exact alloc-no-stdlib2.0.4 `.crate` member copied unchanged to `notices/retained/alloc-no-stdlib-2.0.4.LICENSE` (1,483 B) | `cd496ba72eb37e83a44958358d1f89a8a28cbc15` |
| jsonschema `LICENSE` at `21a061d6…` | Existing jsonschema0.58.5 direct-index licence asset (1,075 B) | `20c070f6401feda6f47be1b158f4f5a4a9d14062` |
| UNIC `LICENSE-APACHE` at both recorded revisions | Existing uuid1.23.1 direct-index asset (10,847 B) | `16fe87b06e802f094b3fbb0894b137bca2b16ef1` |
| UNIC `LICENSE-MIT` at both revisions | Existing serde1.0.229 direct-index asset (1,023 B); serde_json is an equal independently retained source | `31aa79387f27e730e33d871925e152e35e428031` |
| objc2 `LICENSE.md` at `8d214f54…` | Previously received exact overview (1,339 B), original custody unchanged | `540ae4c81adb5f64a9f61e222b688880da24300e` |

`proof.json` retains the selected path/blob/size root metadata and source
archive/member or direct-index provenance. The API-reported root response SHA
is recorded as reported, without signed-attestation or cryptographic
commit-to-tree proof claims. The selected public metadata and local-reuse
packets retain original hashes `d1724600…` and `f8961c52…`; they are not rebound.
Original private custody:

- `/Users/ryan/dev/chirality-t3/scratch/app-p6-metadata-HNijSW/` (original six
  metadata responses, decision packet and parent's direct-asset checks).
- `/Users/ryan/dev/chirality-t3/scratch/app-p6-local-reuse-hLueq3/` (both locked
  archive/member rechecks and independent byte comparisons).
- Exact alloc archive:
  `/Users/ryan/dev/chirality-t3/scratch/app-p6-notice-GOvdPTBa/cargo-home/registry/cache/index.crates.io-1949cf8c6b5b557f/alloc-no-stdlib-2.0.4.crate`.

The new retained alloc text was copied only after its full archive SHA-256
matched the retained receipt and its unique regular LICENSE member matched
size/SHA-256/Git blob. Existing direct-index assets were reused in place, not
relabelled as upstream downloads. No cache/install/source file was modified.

## Maintained derivation and checks

The `associate-local` command validates the existing graph, basis, lock identities,
member receipt and prior source locators, then derives the explicit text
successor. It does not re-resolve or regenerate the dependency graph:

```sh
python3 -B app/packaging/notices/transitive.py associate-local \
  --input /absolute/preserved/transitive-index.v2.json \
  --out /absolute/selected/transitive-index.v3.json
python3 -B app/packaging/notices/transitive.py check
```

For this contribution, the maintained command wrote the current source index.
It is idempotent for `/3`. The original `generate --cargo-home …` command also
uses these fixed associations after independently checking archive source
locators; its Cargo graph operation was not repeated for this unchanged graph.
`check --cargo-home …` still re-resolves the graph and re-reads every archive
when independently needed. The graph generation receipt remains its actual
prior Cargo execution, not a newly claimed run.

Source-only verification used normal `t3_slot.sh` admission, fresh scratch
CODEX_HOME/TMPDIR, and no network. Twenty focused transitive tests (six
subtests) pass. They cover the historical reader, deterministic graph-preserving
join, fixed source and subject selection, altered scope, missing simd/scheduler,
text drift and file/ancestor link refusal. Manifests, Cargo/npm locks, original
member digests, npm rows, archived source evidence, product configuration and
resource bindings remain unchanged. No App build or bundle verification is
claimed; actual inclusion is a later candidate-bound step.

Independent review found that importing the full static-distribution checker
also imported its optional `jsonschema` dependency, regressing the formerly
standard-library-only transitive CLI. Agent0 repaired that boundary directly:
`notices/retained_files.py` retains the four checked file/JSON primitives without
loading schema-validation code. The historical checker bytes and source pin are
unchanged. A real `-I -S` subprocess regression exercises help, check and the
legacy-to-successor join; all three failed before the repair because jsonschema
was unavailable. The fixed focused suite passes 21 tests and 9 subtests.

The hosted packaging shard separately found two fixtures passing a macOS
`/var` alias to the physical-path-only reader. A scratch TMPDIR alias reproduced
both failures locally. Resolving only each newly created fixture root repairs
the tests; reader link refusal is unchanged. All 21 tests and 9 subtests then
pass with that alias still present. Original logs and the two failing baselines
are retained in the root repair receipt; no full graph or Cargo run was added.

## Smallest remaining body request

Only these two previously proposed bodies remain unavailable within the bounded
retained input set. Neither is approved or retrieved:

| Immutable URL | Bytes | Git blob SHA-1 |
|---|---:|---|
| https://raw.githubusercontent.com/Nugine/simd/d74c030d9dc4f3cae02146d1f497ff62726ef09a/LICENSE | 1,062 | `2c7eabb59093ea117d73b20effdd0414f87b2af2` |
| https://raw.githubusercontent.com/open-i18n/rust-unic/5878605364af97a3358368a6eaef02104af2e016/COPYRIGHT.md | 608 | `0322ceec0b8f15aa2d74a6173c07cc8c6f3764b3` |

Total **1,670 bytes**; the UNIC copyright blob also matches revision
`8a6ce83063d90b91ae2ce59eddb803edd393fca9`. Outref's 1,062-byte LICENSE has a
different blob (`2ca354be…`) and is explicitly not substituted. Possession of
UNIC's two alternative licence texts does not elect one or close copyright/scope
obligations; absent crate paths remain unknown. objc2's file is an overview with
full-terms/SDK caveats. Scheduler archive size/verification and supplier
main/code-mode-host/rg/zsh source/binary/licence joins stay separate. No further
metadata, archive or body acquisition occurred. No P6 closure is claimed.
