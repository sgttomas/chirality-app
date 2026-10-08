# C1 connector standing production increment

Author: harness-native TASK `/root/group_c_manager/connector_slice`,
`gpt-6-astra` low. Source `c3174f58460d748622e3a1be05fd6a0fa649df9b`
from `7311df06d8`, integrated without source changes as `a99ae55`.
Exact connector_standing.rs SHA-256:
`63d8dc45187be6551cecdd02ef46de08441a1a8c58b9f594022f45d553519c7e`.

The production Rust module is registered in the App library and exposes a
semantic input → standing → per-question-part route-needed projection. It
retains missing metadata, every assessed condition reason, connector-specific
tiers and simulation standing, computes exact CS-R1 reliance, refuses unknown
or absent promotion and empty-part reliance, and lists prohibited conclusions.
The only prior-file production edit is its module registration in lib.rs.

## Performed checks

- Full App library compilation with seven targeted `connector_standing::tests`
  tests: 7 passed, 410 unrelated tests filtered out. Offline, locked, approved
  existing Cargo cache and private Group C target; no download or supplier run.
- Test cases: all connector/envelope/condition/tier combinations and standing
  schema validity; 64 condition subsets; missing metadata; same question through
  all six conditions; mixed and uncovered parts; independent availability,
  including PEC absent with Domains stale; later semantic joins; invalid inputs.
- Historical EU-D1 prototype: 297/297 constructed rehearsal checks. This is a
  separate observation of the historical prototype, not validation of new
  production code or admitted source/provider evidence.
- Source formatting, diff checks and staged private-term check passed; identity
  checked as Ryan C Tufts before the implementation and integration commits.
- Initial default-cache Cargo attempt could not resolve pulldown-cmark offline.
  A subsequent shared-target attempt exited at a Tauri sandbox write failure.
  Neither is used as a pass. The successful run used the approved cache and a
  private Group C target; the existing artifacts were copied before use.

Portable rerun from repository root (use an approved offline dependency cache
and a private build target):

```sh
CARGO_NET_OFFLINE=true CHIRALITY_SKIP_CODEX=1 cargo test --offline --locked \
  --manifest-path projects/chirality-app-v4/app/src-tauri/Cargo.toml \
  connector_standing::tests --lib
```

## Scope and limits

This is a tested programmatic contribution to DEL-07-02 OUT-001/003, not
completion of its criteria. Receiving-owner assessments and the complete list
of required items are trusted semantic inputs. Descriptive coverage metadata
is retained but not verified. The module establishes neither provider evidence
nor coverage completeness, source correctness, qualification, release or
adoption. Simulation remains simulation even when its constructed facets permit
semantic reliance. No UI, source read/reconstruction, route account, persistence,
placement choice, duty performance, native/person act or operational witness is
produced. C2–C5 and CI-29/C3 carry the remaining Group C work.

Independent review is by a separate TASK and must cover the actual combined
candidate. Its record and required CI establish readiness for the first PR;
this evidence alone is not merge approval, Group C completion or a 90% gate.
