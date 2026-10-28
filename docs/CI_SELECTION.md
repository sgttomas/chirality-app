# App development verification

`harness` combines repository checks and App verification. Every PR runs both;
unknown, renamed and deleted paths cannot cause a check to be silently omitted.
A failed, cancelled or skipped required job fails the aggregate. This standalone
repository does not select or execute SWBPIPE checks.

The App workflow retains the former monorepo's focused build, Rust, Node and
Python checks, plus frozen-source regression checks. Manual App workflow dispatch
retains the broader supplier-dependent route; it is not a release and remains
subject to the owner's authorization and App hold. No release workflow is present.

Frozen examination sources are verified locally without Git fetches. Toolchain
and package setup in hosted CI retain their existing versions. Local checks use
offline caches by default. A fresh clone needs the documented toolchains and
dependencies, not a sibling Chirality checkout.

Credential/conflict checks are retained. Same-repository PRs require the
`PRIVATE_TERMS` repository secret; its value is private and never committed.
Preserve merge commits for the migration PR so imported history remains reachable.
