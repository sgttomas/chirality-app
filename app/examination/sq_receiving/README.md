# SQ dossier file receiving

This separate offline receiver checks an explicitly selected SQ dossier, its
recorded direct EXP results and primary review against fixed source bytes. The
existing six-record canonical route is unchanged. A changed or missing pinned
source refuses; no fetch or caller-selected revision is used.

From the App directory, using the existing Python/jsonschema environment:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 examination/sq_receiving/receive.py \
  tests/group_b_sq_receiving_fixtures/development/selection.json \
  --selection-sha256 "$(cat tests/group_b_sq_receiving_fixtures/development/selection.sha256)"
PYTHONDONTWRITEBYTECODE=1 python3 tests/group_b_sq_receiving_test.py
```

The supplied digest must identify a previously frozen selection; calculating a
new digest does not authenticate a technical decision or adopt source changes.
Exit 0 means declared selection consistency and complete **selected** coverage.
Other results exit 1 and distinguish errors, incomplete inputs and unsupported
joins. A complete selection can retain fail, blocked or not-run outcomes. It
never establishes qualification, native observation, actual review, independence,
producer use or current reliance. Those flags remain false.

`pins.terms-v1.json` pins the SQ dossier schema, rules (`sq_dossier_rules.py`)
and step map, the canonical binding sources and the existing EXP/PKG validators.
`receive.py` verifies the fixed pin digest and every source byte before copying
the selected sources into a private temporary snapshot. The pinned `worker.py`
runs offline Python only against that snapshot. It invokes unchanged canonical
single-record binding checks, SQ `violations`, EXP record/review/change validators,
`review_join`, and citation-conditional `package_link`/`change_join`. It does not
pass an incomplete role set to canonical.py's six-role `check` API. The small
worker separates source execution from caller files; it is not hostile-process
isolation or authenticated filesystem custody.

A J1 or J2 step's result names its step and no scenario, since the result
format admits only V4-EXM scenarios. Its native route method must name the
operator the dossier records: person_operated for a person, ui_automation for
an agent. A step recorded as not done through the App's controls is reported as
an unsupported join, because the result format cannot say so. A step with
planned parts must carry each in its result's parts, none declared not
applicable. The report carries each journey's basis beside its outcomes.

In a selection, `review.results` is an object
mapping direct result slots to their full subject/configuration/criterion basis;
`changes[].pairs` is an array of closed before/after/nullable-rerun selections.
A dossier receives no invented EXP binding kind. Its exact selected bytes must
be uniquely cited by complete dossier ID in the review's evidence set for complete
review coverage. Direct result citations resolve to their actual selected slots,
including when prior snapshots have the same record ID. Missing dossier citation
is incomplete; a conflicting target refuses. Legacy helper unresolved references
remain in `existing_checks`; this receiver separately checks their selected map.

Native development with no package citation needs no package. Cited packages
receive byte/binding/candidate checks; existing package-link guarantees are claimed
only within that helper's current packaged-result preconditions. Its reported
prerequisite gaps are retained separately. A change citation requires selected
change/history coverage; no rerun is invented. Historical or reopened outcomes
remain attached to their original records, and missing snapshots are incomplete.

Only expressly selected local files are read. Duplicate/extra selection fields,
ambiguous IDs, changed hashes/support, traversal and links refuse. Opaque review
files are hashed without interpreting nested path/authority declarations. External
result/form/stimulus/supplier/criterion references remain reported obligations;
this is not a general evidence resolver or native-form checker. No run-evidence
folder is a runtime dependency. Source drift requires a named reviewed successor,
not a caller pin or fallback.

For the additive package/S4 route, use `receive_packages.py` with its explicit successor selection and independent
configuration; the original entry above remains its own source/record subject.
