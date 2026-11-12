# Bundled IBM Plex font notice

The App frontend bundles ten IBM Plex WOFF2 files from `app/src/fonts/`, beside
one OFL text per family (Mono, Sans, Serif). `index.json` binds each to its size, SHA-256 and Git blob, and
records the declarations each font carries in its own OpenType `name` table:
copyright, family, subfamily, version and licence URL.

| Family | Files | Name-table copyright | Version |
|---|---:|---|---|
| IBM Plex Mono | 2 | Copyright 2017 IBM Corp. All rights reserved. | 2.3 |
| IBM Plex Sans | 5 | Copyright 2019 IBM Corp. All rights reserved. | 3.201 |
| IBM Plex Serif | 3 | Copyright 2020 IBM Corp. All rights reserved. | 2.6 |

Every file's licence URL is `http://scripts.sil.org/OFL`. Each family's text is the
SIL Open Font License 1.1 with that family's IBM copyright header, as its
`@fontsource` 5.3.0 tarball carries it. The Sans text keeps its name,
`LICENSE-IBM-Plex-OFL.txt`, because the frontend entry links it.

## Provenance

All ten fonts and the Sans text are Git-blob identical to v3 at shared Chirality
`485051eac923c759238948a54cd7bb094eee4899`,
`projects/chirality-app-dev/frontend/src/fonts/`, added there by commit
`f29b27a1fbf1c9a3b770923b2b74567b62f0c038` from the
`@fontsource/ibm-plex-{sans,serif,mono}` 5.3.0 tarballs. That claim is verified:
every font and every licence text equals, byte for byte, the member of its
family's tarball that the index names, and each tarball read from a local npm
cache has the SHA-512 integrity the index pins. No App lockfile pins these
tarballs (they are not npm dependencies of the App); the integrities are npm's
registry values. `check.py --generate --npm-cache DIR` rewrote the index and the
Mono and Serif texts from the tarballs; `--npm-cache DIR` alone rechecks them.

## Checks

From the repository root, with Python 3.11+:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 app/packaging/font_notice/check.py
PYTHONDONTWRITEBYTECODE=1 python3 app/packaging/font_notice/check.py --name-tables
PYTHONDONTWRITEBYTECODE=1 python3 app/tests/font_notice_test.py
```

The default check is pure Python. It refuses changed, missing, linked or extra
files in `app/src/fonts/`, a family without its licence text, and an upstream
claim whose evidence (pinned packages, a tarball member for every file) is not
complete in the index. After stripping comments and matching keywords
case-insensitively, it requires the `@font-face` sources in
`app/src/workspace.css` to equal the indexed fonts exactly, so remote or
extensionless sources refuse. It refuses `@import`, font references outside those
rules, and any `@font-face`, `FontFace(` or font-file reference in other frontend
sources (`app/index.html` and CSS/HTML/JS/TS under `app/src`). It requires exactly
one active licence link in the entry HTML. This is a lexical check, not a CSS
engine. `--name-tables` also decodes each WOFF2 `name` table with Node's
built-in Brotli and compares the recorded strings. No font data is executed.

`production_inputs/prepare.py` runs the default check against the selected source.
It maps `index.json` and the three OFL texts to `third-party-notices/fonts/`, which is
the bundle-visible notice copy. The frontend build separately embeds the fonts and
licence in the App executable. No candidate has been built with this mapping.

## Limits

The index records exact strings and bytes; it is not a licensing determination or
release approval. No Reserved Font Name appears in the shipped name tables or
licence texts.
