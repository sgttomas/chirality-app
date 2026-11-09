# Codex 0.167.0 notice/source associations

`associations.json` and `source-graph-proposal.json` are generated, and can be
rechecked, offline from retained inputs by
[`associate_0167.py`](../../../../../../app/packaging/supplier_notices/associate_0167.py):

```sh
python3 app/packaging/supplier_notices/associate_0167.py \
  <canonical 0.167.0 vendor> <frozen 0.160.0 vendor> <retained metadata dir> --check \
  execution/PKG-01/DEL-01-06/Work/supplier-notice-associations/codex-0.167.0
```

The reader requires the canonical vendor manifest `158dd670…`, the frozen 0.160.0
manifest `327effb9…` and the six retained public metadata responses whose
SHA-256 values `associations.json` records. It executes no supplier code and
opens no network connection. What the records establish, and what remains open,
is stated in [SHIPPED_NOTICE_COVERAGE.md](../../SHIPPED_NOTICE_COVERAGE.md).
