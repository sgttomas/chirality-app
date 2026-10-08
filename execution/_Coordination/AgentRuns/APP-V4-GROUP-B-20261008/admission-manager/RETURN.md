# B3 partial offline review and repair support

Base 45796bc1159 (merged PR #1119). Implementation author 809a7bfa85; repair
6acb23613a90; final evidence 15594c287d80. Manager integrated these without
changing canonical Design/schema/rules or any existing source manifest.

Maintained admission/admission_check.py validates EXP review/change-impact
records and explicitly selected result joins. It checks reviewer/author and
subject/configuration/criterion bindings, repair confirmation identity, prior
outcome/evidence preservation, reopening citations and rerun identities.
Opaque alias selections are tooling inputs, not new canonical schema meaning.
Other evidence/affected rows stay unresolved; actual complete affectedness,
review, repair, authorization and route admission are not established.

Independent review found F1: generic module names broke 10 existing B1 tests
when combined. Renamed modules and two-order regression repaired that original
failure. Reviewer confirmed 51 combined tests and both direct import orders.
All four maintained rule functions independently match canonical prototype AST.
Additional probes reject changed history/citations and duplicate identifiers.

Manager command (complete raw output in integration-tests.txt):
`python3 -m unittest discover -s projects/chirality-app-v4/app/tests -p 'group_b_*test.py' -v`
Result: 51 tests pass. Inputs/outputs and hashes are in admission-prep/F1-repair/;
earlier admission-prep evidence remains historical and identifies original code.
No real examiner result, rerun, browser/native run, human act or admission was
created. All fixtures and joined outputs are expressly invented file checks.

CI-26 full support identity and PKG successor joins remain pending separately.
A-IN/FP-2/W-4, DC-R/DC-N actual runner/tool checks, N-1 forms, fixture origins
and native package examination remain graph work. B9 is not duplicated: its
unresolved supplier obligation is already explicit. No Group B closure or 90%
claim. Parent handles PR/CI/integration after exact-head independent review;
merge latest main without rewriting and recheck affected inputs before PR.
