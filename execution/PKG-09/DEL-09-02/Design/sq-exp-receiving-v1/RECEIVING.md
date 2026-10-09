# SQ-EXP-RECEIVING-v1 — executed dossier receiving supplement

Named technical change: **CC-SQ-EXP-RECEIVING-01**. Owner: DEL-09-02;
paired support owner: DEL-09-01, `Design/sq-exp-receiving-v1/METHOD_ADAPTATION.md`.
Standing: Design candidate for independent source review. The parent selected
this technical target; this file does not assert that source review, integration,
implementation or qualification has occurred. After independent Design READY,
the parent may release bounded implementation under its stated sequence. Actual
source adoption/integration is recorded by the owning loop against exact revisions;
Git presence and a record writer's declaration do not authenticate that event.

This additive contract specifies a **separate** `sq-exp-receiving-selection.v1`
consumer. It leaves SQ-v0.2/EXP-v0.2 records, their published schemas and existing
six-record canonical route unchanged. It introduces no record of a new kind and
no generic evidence resolver. Old dossier/source-lock bytes are never rewritten
to fit this route. Historical records outside its explicit conventions remain
on their existing consumers unless an identified correspondence selection fits.

## Governing sources and inherited obligations

Within DEL-09-02 Design, `../STANDALONE_QUALIFICATION.md` (SQ §§4–6),
`../sq.dossier.schema.json`, `../sq.step-map.json` and
`../prototype/check_sq.py` define the dossier and SQ-R1…R10. In DEL-09-01 Design,
`EXAMINATION_PROTOCOL.md` (EXP §§3.5, 4.4, 6–8), the three `exam.*.schema.json`
files and `prototype/check_exp.py` define EXP. Its
`support-identity-v1/METHOD.md`, `declaration.json` and `binding.schema.json`
define the published binding identity and the distinct six-record selection.
These references are maintained source files, not runtime dependencies on run
records. Historical drafting labels retain their accepted-source context.

Every selected result and dossier still requires its existing schema/rule
validation. Failed, blocked, not-run and inconclusive outcomes are not invalid
merely because unsuccessful. Opened examinations retain the obligation to record
every planned case; a receiver does not invent a not-run record for missing
bytes. SQ-SEQ6–9 still requires record/dossier validation, review, handoff and
reopening. EXP-R2/NB-3 permits native development without mandatory packaging;
its packaged not-run exception remains. Review standing and separation are
reported declarations, never acceptance or authenticated review performance.

The `app/examination/admission/admission_check.py` one-result `review_join`
leaves other evidence strings unresolved; this supplement accounts for those
references explicitly. Binding emission through `canonical.py:binding` does
not validate a record. No call to the current six-role `canonical.py:check`
with fewer roles satisfies that unchanged contract.

## S1: fixed sources, exact files, explicit citations

All fields below are **new receiving-contract selections**, not fields to insert
in SQ-v0.2 or EXP-v0.2 records. The separately implemented reader must pin SQ protocol/schema,
step map/prototype and their supplier-case source closure, plus the existing
canonical EXP declaration/method/schema and reused validators. The receiver
must compare source bytes before reading records. Same version labels do not
substitute for source hashes. Existing pins are not repointed.

The top-level closed object contains exactly:

| Field | Content |
|---|---|
| format | Literal `sq-exp-receiving-selection.v1` |
| purpose | Existing `current_producer_declaration` or `historical_correspondence`, uniform across selected EXP bindings |
| support | `{declaration_sha256, support_identity}`; the fixed canonical declaration SHA-256 and complete EXP tuple, compared to reader selection, not chosen by caller |
| candidate | Exact revision, build_identity, codex_pin to compare with dossier and direct candidate results |
| dossier | `{path, sha256}` for the original SQ JSON bytes |
| case_definition | `{ref, path, sha256}`; ref equals dossier.case_definition.ref and digest equals its sha256 after removing the literal `sha256:` prefix |
| artifacts | Array of `{slot, kind, record, binding}`. kind is result/review/change/package; record and binding are `{path, sha256}`; slot is a unique local selection identifier |
| steps | Array of `{scenario, step, result_slot}` for exactly the recorded dossier steps, including uncounted ones |
| review | Null or `{slot, subject_alias, reviewer_identity, author_identities, review_kind, reported_as_independent, results, evidence}`; results maps each reviewed direct result slot to its exact `{subject, configuration, criterion}` basis; evidence is defined below |
| packages | Array of `{ref, slot, result_slots}` for only package citations present in the dossier or selected candidate results |
| changes | Array of `{slot, from_alias, to_alias, pairs}`; each pair names before_slot, after_slot, nullable rerun_slot, exact before_basis and nullable rerun_basis |

The caller supplies the SHA-256 of the previously frozen selection bytes.
This establishes a selected input, not authority to adopt a contract. All
artifact digests are 64 lower-case hexadecimal characters, computed over raw
bytes without JSON normalization. Reject duplicate JSON keys, nonfinite JSON,
unknown fields, duplicate slots, ambiguous ID resolution, duplicate step maps,
unreferenced selected artifacts, or a path used for incompatible roles. Read
only explicitly contained POSIX relative files; reject absolute/traversal/link
substitution. No network retrieval, path guessing, ID substring parsing, or
searching adjacent directories. Link checks are best effort, not hostile
concurrent-filesystem custody.

Every EXP result/review/change and optional package has its own unchanged
canonical binding sidecar checked against exact record bytes and the fixed
support tuple. The **dossier has no EXP sidecar**: its exact bytes are selected,
its SQ schema and source identity are checked separately, and its string
support_revision must match the fixed EXP version. The case definition has no
EXP sidecar either. Source correspondence does not prove that it was declared
before the run or that the producer used these sources.

For each recorded step, `result_record` must equal the selected result's complete
record_id, not an annotation interpreted as an ID. Compare outcome exactly.
Require candidate basis and matching revision/build/pin; require native route
for the direct SQ step (SQ §4). New receiving convention: case owner
DEL-09-02, case_id equal step, scenario equal scenario, no case.part on that
aggregate step record. This convention is **new**; EXP permits other case/part
identities, so such records remain usable through their existing consumers but
are unsupported by this narrow receiver. No rewriting of old records.
Supplier-case result_ref and replay evidence remain separate from the direct
step result; no rehearsal replaces a native step.

## S2: review evidence and conditional attachments

`review.slot` selects the exact EXP review whose record_id equals
`dossier.examiner.review_record`. Null is allowed only when that citation is
absent. The examiner and reviewer are different roles; their names are not
forced equal. The reviewer fields and subject_alias are explicit frozen caller
selections. The alias is not parsed as an authenticated candidate identity;
this contract ties it to the separately selected candidate tuple. Require
review_kind v4_ops_34 for the dossier's primary required review; an additional
person review cannot substitute (EXP §7).

Reuse the unchanged review schema/rules and `review_join` for each direct result
claimed reviewed, supplying its full original basis. For a complete dossier
review, `results` covers every recorded direct step result. In addition,
`review.evidence_set` must contain exactly one citation equal to the complete
selected dossier.record_id, and its unique `review.evidence` entry must target
`{dossier:true}`. This new exact-ID convention permits no alias. That target
means the original dossier bytes selected by path and SHA-256, including handoff
and currency fields, not a reconstruction or an earlier dossier version. An
absent dossier citation or absent corresponding mapping makes review coverage
incomplete even if every direct result is covered. A contradictory target,
duplicate citation/mapping, or conflicting use of that ID refuses. The dossier
ID must not collide with a selected artifact ID. Only this complete selected
coverage may be reported as a complete dossier review; it does not prove that
the reviewer actually read the bytes (EXP RV-1; SQ-SEQ7–8).

`review.evidence` is an exact mapping for every string in `review.evidence_set`, with entries
`{ref, target}`; target is either `{slot}` for selected record bytes,
`{dossier:true}`, `{case_definition:true}`, or `{path,sha256}` for opaque evidence
bytes. Ref strings must match exactly and be unique. A result citation resolves
only to its matching record_id. A selected result cannot masquerade as opaque
bytes. Resolve the union of the one-result checker's unresolved references via
this mapping, without deleting them from the original review or claiming the
legacy checker resolved them. Each entry names one target; no inference from
nested path/digest objects. A missing mapped file is incomplete, a mismatching
hash or contradictory mapping is refused.

This is an explicit review-set file map, **not a general EXP evidence resolver**.
Opaque evidence is checked only for byte identity, not observation semantics,
producer use, or native provenance. Result evidence refs, form_ref, stimulus
refs, supplier result refs and criterion disposition refs outside the selected
review set remain reported external obligations; this receiver never claims all
evidence closure or native-form validation. A reviewed dossier references its
results by ID; review binds dossier bytes via the selection, avoiding a cyclic
embedded digest. Editing dossier handoff fields after review requires a new
selection and review coverage of those bytes, not silent digest refresh.

`packages=[]` is normal for native_development without package citations.
A citation triggers exact package file/binding and revision/build/pin/reference
checks. Reuse unchanged package schema and, where its preconditions hold,
`package_link`; retain prerequisite-gap output separately from structural
errors. That helper requires current native_packaged results, so do not force it
on native_development, historical results or not-run missing-package records.
For these cases report package-link scope unsupported/not evaluated; never claim
its guarantees. EXP-R2's not-run exception remains available. A dossier package
citation cannot be silently dropped merely because direct route is development.
No signing, package completeness or successful outcome is fabricated.

`changes=[]` is normal with no change citations. A dossier/result currency
change_ref triggers selection of that exact change ID and byte binding. Validate
all selected prior-result snapshots with EXP-R8. For each declared pair reuse
unchanged `change_join`; the before/after slots may share record_id only for that
explicit pair, while their different exact bytes remain separate. Resolve all
other affected rows explicitly; do not drop the legacy unresolved-row list.
No rerun is required when the change has none: rerun_slot/basis are null. A
claimed rerun requires its matching current result and all existing criterion
checks. Missing prior before/after bytes yield incomplete change-join coverage,
not an invented history. The current dossier's candidate comparison applies to
direct steps, not to historical before/after records. A selected change cannot
prove that every real-world affected case was listed, and a criterion
permission reference does not authenticate its authorization.

## S3: Report and validation order

1. Check fixed source bytes, frozen selection digest, syntax/containment, raw
   artifact hashes and individual canonical bindings; validate SQ/EXP schemas.
2. Run existing SQ-R1…R10 against pinned step map and supplier files; run existing
   EXP record/review/change validators on original records. Apply the separately
   specified joins above. Never turn binding emission into validation.
3. Report `selection_consistent`, `coverage` (complete/incomplete/unsupported),
   errors, missing selected inputs, unresolved external references, unchanged
   source-check outputs and reported outcomes/currency. Complete here means only
   this declared dossier/result/review/conditional-attachment selection, not
   native evidence completeness or successful examination.
4. A well-formed failed/blocked/not-run/inconclusive record can be consistent.
   Missing causes/limits or inconsistent aggregation refuse via existing rules.
   Non-recorded steps receive no result slots. With handoff false, an unfinished
   dossier may be consistent but incomplete. An opened examination with missing
   records retains its outstanding SQ-SEQ/EXP §6.1 obligations. Do not invent an
   outcome for a planned step. SQ-R8-invalid handoff/independence claims refuse.
5. A missing review without handoff/independence claims is incomplete, not an
   implicit exemption from SQ-SEQ7. Honest nonseparation can be consistent with
   both independence claims false. A dossier independence claim requires the
   selected review's matching true claim plus existing EXP-R6/SQ-R8 checks;
   it still does not authenticate actual independence. Open review findings are
   retained, never relabelled no_findings.
6. Historical/reopened dossiers or results retain reported outcomes and change
   links, and can be inspected as consistent history; report current_reliance
   false. Even current selections report qualification_established,
   actual_producer_use_verified, native_observation_verified,
   publication_authority_authenticated and method_adoption_authenticated false.
   Unknown assertion fields claiming verified authority refuse; preserved legacy
   declarations are reported as declarations rather than authenticated facts.

## S4: Source review and implementation obligations

The new choices selected for this route are: exact native direct-step aggregate
mapping to DEL-09-02/case_id=step/scenario/no part; exact dossier-ID review citation;
explicit selected review-set file mapping; and citation-conditional package/change
attachments. These are not retroactive requirements of legacy schemas. They
require the owning technical source disposition and a separately reviewed
implementation before a consumer claims this contract.

Implementation must preserve original record bytes and validators, capture the
complete fixed source closure (including SQ supplier-case files), and provide
invented positive/negative connected tests. No current source pin is repointed.
Only the new receiver may claim this new selection's limited consistency; the
existing six-record selection retains all six roles and mandatory joins.
Neither source review nor test success verifies native execution, actual reviewer
separation, signing, S3 custody, producer use, professional reliance or release.

The following source-level acceptance obligations are schematic conditions, not
executed tests or assertions that complete valid examination fixtures exist:

| Case | Selected condition or mutation | Required receiving behavior |
|---|---|---|
| 01/16 | Current native_development dossier with honest fail/not-run results; no package/change citations | No invented package or repair cycle; evaluate record consistency separately from outcomes |
| 02 | Dossier says pass while exact selected result says fail, even after rehash | Refuse outcome disagreement |
| 03 | Selected result has a different build, with refreshed hashes/binding | Refuse candidate mismatch |
| 04 | Recorded result citation remains but its selected bytes are absent | Incomplete; no complete receipt |
| 05 | Non-recorded planned step has no result/outcome; handoff false | Permit partial inspection; coverage incomplete and record obligation outstanding |
| 06 | Incomplete counted steps plus handoff true | Refuse SQ-R8 claim |
| 07 | Attempted native_packaged result cites absent package | Incomplete package selection; no complete receipt |
| 08 | Native_packaged not-run with missing-package reason and no package citation | Preserve EXP-R2 exception; package link not evaluated |
| 09 | Review adds evidence citation without mapping | Incomplete review closure; do not drop unresolved references |
| 10 | Historical/reopened result cites selected change with prior snapshots | Preserve outcome; current reliance false; missing required history incomplete |
| 11 | Independence claimed with declared nonseparation | Refuse EXP-R6 |
| 12 | Selection/binding adds adopted or other authority override field | Refuse unknown field |
| 13 | Record bytes change without matching digest/binding | Refuse exact-byte mismatch |
| 14 | Annotated string differs from complete result ID | Refuse; do not guess or parse an ID |
| 15 | Selected result evidence citation instead maps to opaque file | Refuse conflicting interpretation |
| 17 | Remove dossier-ID citation and mapping, retain every result citation, refresh hashes | Incomplete dossier review; contradictory dossier target instead refuses |

The cases retain the reviewed proposal's scope, including its repaired dossier
coverage boundary. A future implementation must test complete schema-valid
invented records, exact bytes and source drift; this Design-only contribution
provides no executable receiver, fixture qualification or implicit adoption.
