# Bounded supplier notice/source observations

From the repository root, run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 app/packaging/supplier_notices/observe.py /absolute/retained/vendor
python3 -m pytest -q app/tests/supplier_notice_observations_test.py
```

This reader accepts only the four exact retained 0.160.0 subject digests. It
records matched binary bytes/offsets and the manifest's actual main-binary
binding, then rechecks source hashes. It does not execute supplier code, fetch
source, validate a signature, infer notice applicability or write to the input.
The library CLI's output can be retained by the caller as ordinary evidence.

The owning DEL-01-06 Work/supplier-notice-associations account identifies precise
missing source/build/notice edges and next remedies. No version string is promoted
to authenticated upstream provenance; the tool does not assert the gaps closed.
The tests use invented binaries except for checking the saved observation's
declared subject/tool identities. No actual supplier or credential is executed.

For the current Codex 0.167.0 subject, `associate_0167.py` recomputes the
notice/source association records offline. It reads the canonical vendor tree
(manifest `158dd670…`), the frozen 0.160.0 tree, the committed root texts in
`codex-0.160.0/` and eight retained public metadata responses. It reuses the
no-follow reader in `app/packaging/static_distribution/check.py` and
`app/packaging/inventory.py`, executes nothing
and opens no network connection. `--check DIR` compares its output with the
retained records under DEL-01-06 `Work/supplier-notice-associations/codex-0.167.0/`.
`observe.py` and its saved output remain the 0.160.0 record.

`ripgrep_0167.py` recomputes the rg association the same way. It reads the
canonical 0.167.0 `rg`, the received Codex rg selector, the committed
`ripgrep-15.2.0/`, `pcre2-sys-0.2.10/`, `pcre2-10.46/` and `sljit-e51eabbf/`
terms texts, retained ripgrep tag/tree responses and `Cargo.lock`, and retained
pcre2-sys/PCRE2/sljit metadata and source text. `--check FILE` compares its output with
`codex-0.167.0/rg-ripgrep-15.2.0.json`. It is not a byte join with the selected
release archive.

`v8_0167.py` recomputes the code-mode-host V8-stack association the same way.
It reads retained Codex 0.167.0 tree responses and blob-verified Codex,
`v8/v8` and `seanh-oai/rusty_v8` source text, and the committed
`v8-15.2.124.1/` and `rusty_v8-350c5a85/` terms texts. `--check FILE` compares
its output with `codex-0.167.0/code-mode-host-v8.json`. It does not show what
the shipped host links.
