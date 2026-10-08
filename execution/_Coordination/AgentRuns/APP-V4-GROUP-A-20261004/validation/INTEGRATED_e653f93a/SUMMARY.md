# Integrated J1–J5: full check

HELP_HUMAN (Claude Opus 5.5, 2026-10-07) ran the full suite on integration
merge `e653f93a1d`. That merge combines J1/J3 at `2e2a02844a` and J4/J5 at
`8d98de95a8` on top of J2 (`00eb79ca5e`). Its App bytes equal those of
`f1ec8d5589`, which was independently checked in review V12.

**Environment:** isolated offline Cargo home
(`dependencies/RESTORE_20261007.md`), stock Codex 0.160.0 complete package
(`bin/codex` sha256 `112fae7a…b4b`) with `codex-path` and `/usr/sbin` on
`PATH`. No network, credentials, model or UI.

| Step | Exit | Result | Log sha256 |
|---|---|---|---|
| `npm run build` | 0 | TypeScript and Vite pass | `f1ad2803a8cf476bb63366ba44dde8197079e81510ecf8b215c804a8a4e59051` |
| `cargo test --offline --locked --no-fail-fast` | 0 | 677 top-level passes, 0 failed, 3 ignored; 4 nested FIFO executions | `896ab1fe165f04c27fd40f4ad4b9c9c6e1411d4d73c45e9b1b8561f21d9c3212` |
| `npm test` | 0 | 3/3, including the stock handshake | `678d0dc81c2aef09dc1dfc39e7c3e0eac97de366353692389cbdfa2d3fc3f992` |
| `python3 schemas/sync.py` | 0 | 6 resources match | `fea59bb900e1e9438e2645cec44da4fbbe38c1e184ba04541fa447a5ad31fb55` |

V12 reproduced the same counts on a `git archive` of `f1ec8d5589`.
