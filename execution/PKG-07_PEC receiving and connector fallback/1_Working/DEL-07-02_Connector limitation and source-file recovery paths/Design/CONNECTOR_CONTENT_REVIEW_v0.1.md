# CCR-v0.1 — positive content-only manager review

PROPOSED source-only message representation, independent review/technical
selection pending. Basis: 2254d6b2806158211411aa05f74001465ce829b4, after CCE-A2
and W2/R2 impact proposals merged. No implementation or accepted Host/ACT/RS
amendment. Proposed identifier `reviewed_content_only` is a technical candidate,
not an owner quote or adopted enum. Old message0.1 and account0.1–0.5 stay unchanged.

## 1. Exact new meaning

A genuinely observed manager-agent message can report a positive content review
of one exact answer/account without an integration plan. It binds original
answer text SHA-256, base-account SHA-256, question ID and one finding for every
answer claim; complete inherited gap pointers and contradiction IDs remain.
It means the manager emitted this content assessment, not that the answer is
true, professionally checked, accepted or integrated. A2's actual source-bound
manager authorship is still required for an observed-contribution claim.

Proposed contribution-message schema0.2 adds one review disposition:
`reviewed_content_only`. Its `plan_sha256` must be null. It is neither
`cannot_assess` nor `reviewed_for_integration`. A manager who actually completed
a positive content review must not be relabeled unable to assess to fit an old
reader. Report unsupported representation instead of silently losing meaning.
Existing changes_requested/cannot_assess also require null plan; existing
reviewed_for_integration requires a real plan hash, as already required by the
old semantic checker. This proposal adds those existing semantic conditions to
the new schema; no historical bytes or old schema are tightened in place.

The supplied fixture is authored test data, not a real manager message. The
checker verifies semantic byte/reference consistency only. No enum, label,
valid schema, receipt JSON or test fixture mints authorship, role, task scope,
grant, acceptance or actual duty performance.

## 2. Version and carrier boundary

Schema identities are explicitly0.1 versus0.2. The message payload itself has no
version field, preserving the existing message family shape; a future enclosing
producer/reader must select the exact schema version explicitly in its own
reviewed source/metadata. Do not select a version by permissive parsing or
retrying validators until one accepts. An old0.1 reader rejects the new enum.
Same-shape shared dispositions retain old meaning; no old content is rewritten.

This bounded slice defines the **message**, not a deployable new route account.
Current proposed account0.5 embeds message JSON as exact text but its semantic
consumer selects message0.1. A schema-only0.5 reader may accept that string;
that does NOT establish compatibility. The0.5 semantic checker rejects the new
review. Do not publish or relabel it as a valid0.5 account. A separate additive
account carrier/version and consumer adoption must explicitly bind message0.2,
retain bytes/receipt standing and display content review separately before any
production persistence is released. This boundary avoids silently changing old
cold-reader meaning while W2 integration representation is still under design.
No format0.6 is selected merely by numbering the next candidate.
The definition checker retains the existing0.5 artifact byte bound of262144
for this comparison; it does not select a new carrier allocation or replace
the final1MiB shared-payload check. A production reader needs both bounds.

## 3. Staleness, later plans and integration

Hash original emitted UTF-8, not a reserialization. Whitespace changes to the
answer invalidate the exact prior review even if parsed JSON is equal. Changed
base, cited support/claim identity or omitted limitation also invalidates the
binding. Keep previous genuine observation historical; no automatic rebinding.
Distinct conflicting reviews stay distinct and block an automatic winner; neither
last timestamp nor disposition strength chooses the accepted interpretation.

A later plan, manager write, fileChange or matching graph content does not upgrade
this review to reviewed_for_integration. New integration evidence needs its own
exact subject and separate manager contribution under the future reviewed W2
contract. W2 ordinary graph work does not inherit W1's controlled insert plan
merely because the old integration disposition used one. This content-only
message is not a graph-write prerequisite, an authority token or a replacement
for manager-linked observed integration; it can remain meaningful when no graph
work ever occurs.

A human reading the message performs no captured human act by that fact. A4/A5/
A6/A7/A12 are neither generated nor waived. The displayed human responsibilities
remain as actually evidenced, with outstanding/unknown distinctions preserved.

## 4. Source/consumer propagation

- C3 request producer may request this exact content-review kind/version only
  after source selection; the original request must bind the exact answer and
  base. Current native UI/Host code implements no such producer.
- Host/role source owners still need the combined capture/mint/recheck described
  by CCE-A2 and the received `C3_HOST_ROLE_JOIN_ASSESSMENT.md`. That assessment is
  source context, not an adopted or implemented interface. It requires actual
  role-source admission, bounded original request capture and guarded consume.
- Composer validates explicit message version, exact text/subject/coverage and
  limitations; its cold-consistency check is not private live custody.
- Future carrier and cold view show “recorded content review; integration not
  established” with current reference resolution and historical authorship limits.
  Unknown message version/disposition remains unsupported, never downgraded.
- RS owner reviews exact version/reference/recorder mapping before adopting new
  typed interfaces; no new RS run or human-act kind is created here.
- W2 integration and R2 recovery consume this exact artifact only under their own
  later reviewed carriers. No storage quota, retirement or CAM64 policy changes.

## 5. Definition checks and release stops

The fixture and checker cover old-reader refusal; null-plan requirement; exact
answer/base/question binding; claim coverage and uniqueness; inherited gap/
contradiction retention; unknown support; duplicate JSON keys; altered whitespace;
and a prohibited later-plan promotion. They also show old account shape acceptance
is insufficient because its existing semantic reader rejects the new meaning.
These are synthetic source-definition checks, not supplier/native tests or proof
that a manager actually reviewed anything. Content quality is not reducible to
string length or citation count; required references establish association only.

Stop before production on explicit carrier version/consumer adoption, original
Host/role mint/recheck and actual request-version producer. Independent review
and technical selection of this proposed enum/schema remain ahead. Neither this
slice nor a later merge adopts W2-M, R2-S storage, owner acceptance or product90.
