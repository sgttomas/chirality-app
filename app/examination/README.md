# Offline examination record support


The current source selection is the **flat-deliverable migration successor**
(2026-10-09 efficiency reset). Its source paths and their dependent byte bindings
follow the current deliverable folders. Earlier pins and fixture bytes remain in
Git history. This successor changes source location and corresponding technical
identities only; it does not establish new publication, qualification, native
observation, or owner acceptance. The existing consistency checks and negative
fixtures retain their purpose. Review this source-selection change with the
migration PR before relying on the successor.

This maintained file tool validates EXP-v0.2 result records and PKG-v0.2 package
identity records against the unchanged canonical Design schemas and their
applicable semantic rules. It checks a selected pair against an explicit App
revision, build identity and Codex pin. It reads JSON files and prints a JSON
report; it does not launch the App, run Codex, contact a service or rewrite inputs.

From `projects/chirality-app-v4/app`, using Python 3.10+ and the already prepared
`jsonschema` 4.26.0 environment:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 examination/check.py validate result tests/group_b_fixtures/result.json
PYTHONDONTWRITEBYTECODE=1 python3 examination/check.py validate package tests/group_b_fixtures/package.json
PYTHONDONTWRITEBYTECODE=1 python3 examination/check.py package-link tests/group_b_fixtures/result.json tests/group_b_fixtures/package.json --revision INVENTED-REVISION --build INVENTED-BUILD --pin 0.160.0 --package-ref INVENTED-PACKAGE
PYTHONDONTWRITEBYTECODE=1 python3 tests/group_b_support_test.py
```

These fixtures are invented. The pair is consistent but its native witness and
FP-1(a), FP-1(b), FP-3 remain not run. Exit 0 means only the requested file checks
passed; exit 1 means schema/rule/link errors; exit 2 means unreadable or ambiguous
JSON or changed canonical sources. `reported_prerequisite_gaps` is separate from
record validity. Even an all-pass declaration leaves `option_b_reliance` and
`native_qualification` explicitly unestablished. Do not use exit 0 as a package
handoff or qualification gate.

`--package-ref` is the citation that the caller associates with the explicitly
selected package file. The tool checks equality with the result's citation and
reports both input byte hashes. It does not resolve free-form citations, infer
which package the writer meant, or verify the authenticity of any declared fact.

`sources.json` pins the canonical schemas, criterion documents and original
prototype rule sources. Source drift fails closed; adoption requires review and
an intentional pin update (see [Source pins](#source-pins) for the maintained
profiles). The maintained rules execute independently of the
prototypes. Reports identify the tool, maintained rules and source manifest by
hash. The existing EXP support fields retain their canonical meaning: in
particular `prototype_digest` is the pinned Design prototype, not this tool.
The package-link check requires that digest under EXP §4.4 although the schema
makes it optional; schema-only validation accepts its omission.

Implemented semantic checks are EXP-R1, R3, R4, R5 and PK-R1, R2, R3, R5–R9;
EXP-R2 is enforced by the result schema. The other rules concern review,
change-impact, vocabulary mapping or terms records and are outside this slice.
The package-link check detects changed revision/build/pin/support, wrong package
citation, a nonpackaged route/subject, and historical or reopened results. It
reports the Option B prerequisite gaps and incomplete package claims separately.
Option A records can be inspected against the existing schema/rules but never
adopt Option A or displace SIGN-1.

This is partial SCC-003 M1 support. M2 package production and install/launch
witness, M3 native smoke, evidence capture and digest resolution, runner admission,
independent review/change-impact support and SQ journey execution remain separate
work. No EXP VER criterion, DEL-01-06 package qualification, DEL-09-02 scenario,
human act, public release, or OI-011 SWB resolution follows from this tool.

## Source pins

Each reader verifies the files it reads against SHA-256 digests and refuses any
unexpected change. The digests of evolving sources are generated, not hand
maintained:

- the source profiles listed in `repin.py` (`PROFILES`) record the digests of
  the current files each reader compares, including other profiles they pin;
- `pins.lock.json` records the digests the readers formerly hard-coded in their
  own code (their profiles and helper sources) in its `current` section.

After a reviewed, legitimate change to a pinned source, re-derive and commit:

```sh
python3 app/examination/repin.py           # from the repository root
python3 app/examination/repin.py --check   # CI: exit 1 when pins and sources disagree
```

Repin repeats until profiles that pin other profiles agree, then refreshes the
lock. Its output, and the diff, name exactly which pinned bytes changed; that diff
is what review inspects. It changes digests only: selecting a different set of
sources remains a reviewed edit to the profile. It leaves historical identities
as recorded: Markdown documentary selections that fall back to frozen original
bytes, documentary projection digests and historical provenance fields.

The lock must hold exactly the entries catalogued in `repin.py` (`CURRENT` and
`FROZEN`) with 64-character lowercase hexadecimal digests; `--check` fails on a
missing, extra, malformed or reclassified entry. The `frozen` section mirrors
the retained distribution cohort receipts, whose digests are anchored as
immutable constants in `distribution_receiving/receive.py` and `terminal.py`.
Readers and both repin modes require the lock to equal those anchors, so editing
a receipt and its lock entry together is still refused; repin never rewrites
them. An unreadable or incomplete lock yields no digest, so each reader refuses
through its usual error report. Retained original sources stay in `support_identity/frozen/`, and the
frozen v1 declaration and binding schema keep their constants in
`support_identity/support_identity.py`.

Package receiving no longer pins `AGENTS.md`: the legacy static reader uses that
file only to locate its root and never reads its bytes, so the receiver writes a
marker into its producer snapshot. Readers that run inside a private snapshot
(SQ receiving and pre-run inputs) copy the same lock into it.
