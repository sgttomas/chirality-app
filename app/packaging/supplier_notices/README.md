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
