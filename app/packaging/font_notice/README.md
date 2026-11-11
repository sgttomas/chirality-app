# Bundled IBM Plex font notice

The App frontend bundles ten IBM Plex WOFF2 files and one OFL text from
`app/src/fonts/`. `index.json` binds each to its size, SHA-256 and Git blob, and
records the declarations each font carries in its own OpenType `name` table:
copyright, family, subfamily, version and licence URL.

| Family | Files | Name-table copyright | Version |
|---|---:|---|---|
| IBM Plex Mono | 2 | Copyright 2017 IBM Corp. All rights reserved. | 2.3 |
| IBM Plex Sans | 5 | Copyright 2019 IBM Corp. All rights reserved. | 3.201 |
| IBM Plex Serif | 3 | Copyright 2020 IBM Corp. All rights reserved. | 2.6 |

Every file's licence URL is `http://scripts.sil.org/OFL`. The retained text is the
SIL Open Font License 1.1 (4,429 bytes, SHA-256 `d0283623…d3fd`). Its header names
only the 2019 Sans copyright, so the index lists all three copyright notices.

## Provenance

All eleven files are Git-blob identical to v3 at shared Chirality
`485051eac923c759238948a54cd7bb094eee4899`,
`projects/chirality-app-dev/frontend/src/fonts/`, the source the frontend lane used.
They were added there by commit `f29b27a1fbf1c9a3b770923b2b74567b62f0c038`, whose
message names `@fontsource/ibm-plex-{sans,serif,mono}` 5.3.0 npm tarballs as the
source. That upstream claim is not verified: no tarball is available locally and
none was downloaded. `declared_upstream_verified` stays `false`.

## Checks

From the repository root, with Python 3.11+:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 app/packaging/font_notice/check.py
PYTHONDONTWRITEBYTECODE=1 python3 app/packaging/font_notice/check.py --name-tables
PYTHONDONTWRITEBYTECODE=1 python3 app/tests/font_notice_test.py
```

The default check is pure Python. It refuses changed, missing, linked or extra
files in `app/src/fonts/`. After stripping comments and matching keywords
case-insensitively, it requires the `@font-face` sources in
`app/src/workspace.css` to equal the indexed fonts exactly, so remote or
extensionless sources refuse. It refuses `@import`, font references outside those
rules, and any `@font-face`, `FontFace(` or font-file reference in other frontend
sources (`app/index.html` and CSS/HTML/JS/TS under `app/src`). It requires exactly
one active licence link in the entry HTML. This is a lexical check, not a CSS
engine. `--name-tables` also decodes each WOFF2 `name` table with Node's
built-in Brotli and compares the recorded strings. No font data is executed.

`production_inputs/prepare.py` runs the default check against the selected source.
It maps `index.json` and the OFL text to `third-party-notices/fonts/`, which is
the bundle-visible notice copy. The frontend build separately embeds the fonts and
licence in the App executable. No candidate has been built with this mapping.

## Limits

The index records exact strings and bytes. It is not a licensing determination,
complete third-party coverage or release approval. No Reserved Font Name appears
in the shipped name tables or retained text. Correspondence to the declared
`@fontsource` tarballs remains unverified.
