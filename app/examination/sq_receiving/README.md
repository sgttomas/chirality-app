# SQ dossier file receiving

This separate offline receiver implements the reviewed `SQ-EXP-RECEIVING-v1`
Design supplements in DEL-09-02 and DEL-09-01. It checks an explicitly selected
SQ dossier, its recorded direct EXP results and primary review against fixed
source bytes. The existing six-record canonical route is unchanged.

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

`pins.json` freezes the two supplements, SQ schema/prototype/step map and
supplier-case sources, canonical binding sources and existing EXP/PKG validators.
`receive.py` verifies the fixed pin digest and every source byte before copying
the selected sources into a private temporary snapshot. The pinned `worker.py`
runs offline Python only against that snapshot. It invokes unchanged canonical
single-record binding checks, SQ `violations`, EXP record/review/change validators,
`review_join`, and citation-conditional `package_link`/`change_join`. It does not
pass an incomplete role set to canonical.py's six-role `check` API. The small
worker separates source execution from caller files; it is not hostile-process
isolation or authenticated filesystem custody.

Selections follow the maintained DEL-09-02
`Design/sq-exp-receiving-v1/RECEIVING.md` contract. `review.results` is an object
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
