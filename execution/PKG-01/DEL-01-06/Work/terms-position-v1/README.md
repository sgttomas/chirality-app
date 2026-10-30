# Retained supplier position, version 1

The owner approved the exact proposal at App revision
`6421c323408b010cfba575ecd8fa24865f403c00` on
`2026-10-30T22:36:59.004Z`. `approved-proposal.md` retains those exact bytes;
`owner-answer.json` retains the actual question/answer, message locator and
timestamp read from App Agent 0's thread. `owner-disposition.json` records its
bounded meaning. The owner receives, adopts and retains the agent-captured
publication and decides applicability, including first public distribution.
The owner did not perform the HTTP fetch; OpenAI did not send a direct reply.

`OpenAI.json` is the new explicit `chirality.distribution-terms-position/v1`
account, with `state: applicable_position_retained` and
`distribution_decision: not_made`. It binds the exact capture, approved proposal
and owner answer through SHA-256 references. The supplier-authored continuation
and exclusion, agent capture, owner receipt/adoption and applicability, recorder,
and separate distribution decision remain different facts. No release,
v3.0.1 replacement, SIWC change, legal conclusion, component-notice disposition,
supplier pin or package qualification follows from this representation.

The original `Evidence/PKG/terms/OpenAI.json`, closed PKG-v0.2 schema, prototype
and their identities remain unchanged historical inputs. New Work records do
not retroactively change `response_received` into a publication. Consumers must
explicitly choose this version; no fallback or automatic upgrade is provided.

## Schema and reader

`schema.json` is closed at each typed object. `unresolved` permits no owner
applicability object and may retain a position awaiting disposition, or null
when evidence is missing. `applicable_position_retained` requires both position
and owner-disposition artifacts. Position kind is `official_publication` or
`direct_response`, never inferred from a successful package check. A missing
publication/response date is null; retrieval/receipt and owner-event timestamps
are explicit. Conditions, exclusions and exact release/sign-in scope join the
owner disposition, not merely its supplier name.

The publication reader consumes the saved capture shape in
`../openai-app-server-publication-20261030.json`. The direct-response route is
tested with invented inputs only; it requires a separately captured
`chirality.supplier-response-capture/v1` object with `supplier`, `source_url`,
`received_at`, nullable `response_date`, `captured_by`, exact UTF-8
`response_text` and its `sha256`. It does not relabel a publication capture.

The versioned owner-disposition and optional separate public-distribution-event
shapes are in schema `$defs`. The reader checks their exact content, supplier,
kind, actor, scope, condition, exclusion and event joins. Publication authorship
is distinct from capture; owner applicability is distinct from the recorder.
A future owner-captured input can name that actual act; the current capture
names the agent and cannot be relabelled without contradicting its exact bytes.
Recorded distribution decisions need a separate event/answer. Even
then the checker reports `release_authorized: false`: it reports recorded
evidence consistency, not execution authority.
Its `recorded_distribution_decision` reports `not_made`, `approved` or `declined`
without converting that recorded statement into authority. A distribution event
can be recorded alongside unresolved terms; it does not settle them. Dates are
calendar-validated without optional JSON Schema format dependencies. Records
cannot predate their evidence/adoption/distribution events, and a recorded
release following an applicability disposition must have a separate message
and content and cannot predate that disposition.

Run from the repository root with the existing Python `jsonschema` dependency:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 app/packaging/terms/check.py \
  --evidence-root "$PWD" \
  --record execution/PKG-01/DEL-01-06/Work/terms-position-v1/OpenAI.json
PYTHONDONTWRITEBYTECODE=1 python3 app/tests/terms_position_test.py
```

All artifact paths are relative to the explicitly selected physical evidence
root; absolute paths, traversal, symlinks, hardlinks, special files and inputs
over 2 MiB refuse. Exact bytes are hashed before parsing; duplicate fields,
unknown formats, schema violations, contradictory joins and changing bytes
refuse. Inputs are re-read before return. No referenced URI is fetched, no
capture's scratch locator is opened, and no code in evidence is executed.
Exit 0 means consistent values/artifacts (including explicitly unresolved);
exit 2 means refusal. Neither is a legal or release verdict.

This is not an authenticity service or hostile-writer snapshot. A person can
fabricate a mutually consistent set of bytes; hashes and actor names do not
authenticate authors or decisions. Human source/act review remains required.
For this actual account, the agent read the real parent-thread answer and
independent review checked the offering, capture and proposed interpretation;
the new representation receives its own implementation review.

## Consumer selection

`app/packaging/static_distribution` still selects its frozen PKG-v0.2 terms
schema and PK-R4 reader; `static-distribution-input/1` cannot consume this record.
It remains `development-unverifiable`, with `verification_artifact: null`.
Do not replace a legacy `terms` reference with this record or move frozen pins.
This additive reader is the selected standalone terms-account check only.
A future package/receiving interface adopting v1 must name its reader/version
and preserve the historical cohort; that adoption is not part of this change.
