# B3 offline review/change support return

Source candidate: `809a7bfa850c7e6f6e25b48b66521dec8e98507a`, based on
`45796bc1159ef7903db37863d0c4a192975c0071`. TASK
`/root/group_b_manager/support_production` under WORKING_ITEMS
`/root/group_b_manager`; no delegation.

New `app/examination/admission/check.py` provides canonical EXP review and
change-impact file checks, plus an exact selected review-result and prior/
reopened/rerun path. Fifteen tests pass. The actual CLI ran on maintained
invented files; its reports explicitly withhold verified review/repair and
route admission. `SUPPORT_CHECK.json` binds exact source/tree/file identities,
commands, raw outputs, source origins/hashes and limitations.

The tool uses its own source lock and maintained transcriptions of EXP rules.
It preserves schema validity separately from stronger, explicit tooling joins.
The review join checks the caller's candidate/configuration/criterion, reviewer,
authors, review kind and reported independence. A repaired finding must cite the
selected reviewer as confirmer. The change join detects erased historical
outcome/evidence, the wrong case or rerun, missing change citations, and changed
criterion identity without the matching disposition citation. It performs no
act and establishes no authorization merely by finding that citation.

EXP v0.2 review subject identity and change from/to remain opaque strings.
Selection files are tool inputs, not new canonical schemas or inferred identity
encodings. Other evidence/affected rows remain unresolved. These selected joins
do not establish complete affectedness or excuse unreadable reliance, which
stays affected under EXP §6.2. Missing reruns remain missing; no observations,
reviewer separation, human acts, browser/native admission or qualification are
fabricated.

No existing examination/packaging/standalone manifest, Design, schema, SoW,
contract, graph or dependency record changed. CI26 remains pending. Parent
retains HOSTING/PKG successor compatibility and integration with newer main.
There is no new contract-amendment proposal from this bounded slice.

## Parent continuation

- Obtain independent review of this exact implementation/evidence and route any
  repairs here before integration.
- Add the explicit Python test/usage route to shared documentation/checks as
  appropriate; existing npm test does not include it.
- Keep B3 partial: CI26, full affectedness/reliance mapping, actual independent
  examination and route-admission execution remain their own work. This slice
  neither completes M1 nor admits a browser/native route.
- Merge receiving main without rewriting this author's basis and reassess any
  changed EXP source pins before final fan-in; do not silently refresh them.

The host's existing Git identity was used. Technical checks are not personal
owner review, governed acceptance or release.
