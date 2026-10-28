# Offline EXP review and change-impact checks

This maintained file tool checks EXP-v0.2 review/change-impact records and
selected relationships to result records. It performs no review, rerun, route
admission, human act or qualification. CI26's complete support-identity issue
remains pending. This directory's name is not an admission claim.

Use Python 3.10+ with the already prepared `jsonschema` environment. From `app/`:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 examination/admission/admission_check.py validate review tests/group_b_admission_fixtures/review.json
PYTHONDONTWRITEBYTECODE=1 python3 examination/admission/admission_check.py validate change tests/group_b_admission_fixtures/change.json --result tests/group_b_admission_fixtures/after.json
PYTHONDONTWRITEBYTECODE=1 python3 examination/admission/admission_check.py review-join --review tests/group_b_admission_fixtures/review.json --result tests/group_b_admission_fixtures/rerun.json --selection tests/group_b_admission_fixtures/review-selection.json
PYTHONDONTWRITEBYTECODE=1 python3 examination/admission/admission_check.py change-join --change tests/group_b_admission_fixtures/change.json --before tests/group_b_admission_fixtures/before.json --after tests/group_b_admission_fixtures/after.json --rerun tests/group_b_admission_fixtures/rerun.json --selection tests/group_b_admission_fixtures/change-selection.json
PYTHONDONTWRITEBYTECODE=1 python3 tests/group_b_admission_test.py
```

The fixtures are invented. Exit 0 means only the requested checks passed; exit 1
means schema/rule/join errors; exit 2 means unreadable/ambiguous input, an invalid
selection, or source drift. JSON inputs are read without rewriting them; duplicate
keys and non-JSON numeric constants are refused. Every input is hashed in the
report. The canonical sources, schemas and original rule prototype are pinned by
`sources.json`; maintained rules execute independently of the prototype. No
network schema retrieval or dated-run dependency is used.

`validate review` applies the unchanged canonical schema and EXP-R6/R7.
`validate change` applies its schema and EXP-R8 against the supplied `--result`
records (repeat that argument for more records). Every cited prior result must
be supplied and historical/reopened with the change citation. Result inputs get
the canonical result schema and applicable EXP-R1/R3/R4/R5 checks. Duplicate
result IDs refuse rather than silently selecting one.

`review-join` checks one candidate result against the caller's selection:
opaque review subject alias, exact reviewer and author identities, review kind,
reported independence and exact result `subject`, `configuration`, `criterion`
objects. The selected result must be cited. Each repaired finding's
`confirmed_by` must name this reviewer's identity under EXP §7 RV-5. Duplicate
finding/evidence identifiers are ambiguous and refuse this tooling join.
Additional-person and honestly non-independent records remain valid on their
own terms; they cannot replace a different review kind/independence claim in the
selection. Other evidence references are returned unresolved. The tool does not
verify actual author separation, model-family exposure, reading, finding
repair, or the truth of any reported identity.

`change-join` checks one selected prior result before and after reopening,
with an optional rerun. The original record must remain byte-content equivalent
as JSON values except for its currency; prior outcome/evidence cannot be erased.
Exactly one affected row must cite it and the correct case. The rerun, when
supplied, must have a new result ID, the same complete case identity, current
currency citing this change, and exactly the selected subject/configuration/
criterion. Changed criterion identity requires `criterion_disposition` with a
matching disposition citation on the rerun (EXP §6.3). This checks the citation;
it does not authorize a criterion change or prove that authorization exists.

Without a rerun, its row must not claim one and the selection's `rerun_basis`
must be null. The report keeps `rerun_not_supplied: true`; no result is invented.
Other affected rows are returned unresolved. This is not a complete reliance-map
check: the owner must still account for all recorded results, and unreadable
reliance is affected under EXP §6.2. Supplying one pair never proves the remaining
cases unaffected.

The selection JSON files are explicit tool arguments, **not new canonical record
schemas**. Their exact fields are illustrated in the maintained fixtures. Review
`subject.identity` and change `from`/`to` are opaque strings in v0.2; the tool
matches them to caller-supplied aliases and checks associated structured bases
without claiming that it established the alias's real-world meaning. This
preserves the existing contract instead of inventing an identity encoding.

All reports retain `review_or_repair_verified: false` and
`route_admission: not_established`. Browser/native DC-R/DC-N checks, N-1 forms,
actual execution, complete support identity, and governed acceptance stay with
their own work. Existing examination and packaging source locks are untouched.
