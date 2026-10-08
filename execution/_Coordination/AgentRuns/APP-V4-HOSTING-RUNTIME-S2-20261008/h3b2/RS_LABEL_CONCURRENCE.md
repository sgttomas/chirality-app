# H3B-2 — RS label-join technical concurrence

Decision: **CONCUR with a named, reviewed semantic correction** of the S1 lifecycle label join that strictly parses the legacy full label and joins it to both the observation's raw and parsed label, without modifying legacy event bytes or closed schema shapes. Recommend correction over indefinite version-bearing envelope deferral. This is technical owner assessment only: parent HELP_HUMAN coordinates authority for actual contract successor adoption. No source change or adoption is performed here.

Contributor: bounded TASK `/root/hosting_runtime_manager/rs_concurrence` under WORKING_ITEMS `/root/hosting_runtime_manager`, under HELP_HUMAN `/root`; harness-native delegation, no descendants. Date 2026-10-08. Scope: DEL-04-03 evidence/reference semantics for H3B-2. Existing RS placement concurrence remains; no pins, canonical source, qualification, MEMORY or production record writes. Only this temporary assessment is produced.

## Source-bound finding

At the requested revision below, Host `verify` retains the successful probe's full label using UTF-8-lossy decoding plus `trim()`, checks it against `codex-cli {DECLARED_PIN}`, and copies that label into `versionIdentity.observedVersionLabel`. Thus the concrete legacy field contains `codex-cli 0.160.0`, not `0.160.0`. It is the legacy stored full-label string, not untouched stdout bytes; preserve that distinction in claims.

S1 `observed` already checks its `raw_version_label` with full-match grammar `codex-cli ([0-9]+\.[0-9]+\.[0-9]+)\n?` and compares the captured version to `observed_label` and the pin. S1 `lifecycle` nevertheless directly compares the legacy full label with the parsed `observed_label`, causing a truthful Host record and matching observation to disagree. The lifecycle schema permits a string in `observedVersionLabel`; the incompatibility lies in the semantic join, not a missing field or incompatible closed shape.

## Recommended precise correction

Name this change `H3B-2 legacy-full-label join correction` and bind the changed semantic reader and its evidence by exact revision/digest. Retain both schema identities and shapes only with an explicit reviewed semantic revision and coordinated reader adoption; never imply that old S1 semantic readers already accept this corrected join.

For a lifecycle event with `versionIdentity`:

1. Require its declared pin to equal the observation pin, as before.
2. Strictly full-match the stored legacy label as `codex-cli ([0-9]+\.[0-9]+\.[0-9]+)`. Require the observation raw label to full-match its already defined grammar (the same text with at most one terminal LF). Do not parse by substring, general whitespace trimming, numeric coercion or loose version extraction.
3. Require the legacy parsed version, the independently parsed observation raw version, and `observed_label` to be equal as strings. Also require the full legacy string equal the observation raw label with only its single grammar-permitted terminal LF removed. Preserve both original strings unchanged. This makes the permitted display/probe framing difference explicit rather than a hidden normalization of evidence.
4. Keep all existing observation validity, outcome, generation, phase, standing, declared-pin and contradiction checks. No observed label, malformed raw label or disagreement becomes a missing-input/development success. This correction does not authorize qualification or verified production standing.

The terminal-LF handling applies solely to this semantic comparison. It never changes stored bytes or any artifact SHA-256 and never broadens the existing raw grammar to spaces, CRLF, multiple lines, arbitrary prefixes/suffixes, prerelease strings or a bare numeric legacy field. If broader supplier label formats are later needed, they require their own named reviewed grammar change.

This repair is faithful to RS §9's separation of source identity from interpreted evidence: exact-byte references continue to bind the actual legacy and observation artifacts; the parsed version is an explicitly derived comparison, not a rewritten source. A same-version label remains insufficient to establish distribution-content equality or qualification.

## Alternative and verification duty

Until the named correction is authorized, reviewed and adopted by affected producers/readers, defer publication/reliance of affected version-bearing successor envelopes explicitly. Preserve the original legacy event; do not strip its versionIdentity, rewrite its full label to a number, or declare the current reader passed. Deferral is a truthful temporary boundary, not closure of the mismatch.

The implementation review should exercise the actual unchanged Host-shaped full-label event against the corrected reader, with observation raw strings both with and without one LF; wrong legacy/raw/parsed/pin joins; malformed/bare labels; extra whitespace/CRLF/multiple lines; and existing generation/outcome/phase regressions. Update any synthetic fixture that wrongly encoded the legacy field as a parsed version, retaining historical fixture meaning. No runtime tests or supplier probes were performed in this assessment; source examination establishes the contradiction and recommended correction, not an implemented fix.

## Basis

Requested source revision: `c9a2b2d3f3e5e48130b15da988c74948f2ce290a`. Read via `git show` from the existing worktree because its current HEAD differs; no checkout or branch modification. Earlier RS §9/§6.2a/H5 reasoning and role/loop instruction sources are recorded in RS_CONCURRENCE.md and RS_PLACEMENT_CONCURRENCE.md. The following hashes identify exact Git blob bytes used for this bounded check.

| Repository-relative source | SHA-256 |
|---|---|
| `projects/chirality-app-v4/app/src-tauri/src/hosting.rs` | `e81074aa33110360ea14b34d0aed4ff49150ec09e935ea537674ffd152c20c58` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-B-20261008/distribution_successor/contracts/model.py` | `eeaa631cabb0b8650c542e4c38ce7ffeb59e40d7e40bf39d18f570a3b47a2e57` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-B-20261008/distribution_successor/contracts/observed-verification.s1.schema.json` | `7f61951db0ba0db5a886a4100847f51e1a3c86f0ceae4b074918a94f353368a1` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-B-20261008/distribution_successor/contracts/lifecycle-event.s1.schema.json` | `e5713e88c720b2c4a2a1463923596e18b53302e3fae9195d433190ed098d0181` |
